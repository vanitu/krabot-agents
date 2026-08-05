#!/usr/bin/env python3
"""Batch orchestrator for answering Ozon buyer questions.

Three-phase workflow:
  Phase A (prepare-batch): fetch up to N unprocessed questions,
  build contexts, save batch prompt and metadata.

  Phase B (finalize-batch): read subagent answers JSON array,
  filter by score thresholds, generate individual final reports,
  combined JSON, and upload-ready payload.

  Phase C (apply-batch): post filtered answers to Ozon API.

Settings are read from {skillDir}/settings.json (created with defaults
if missing). CLI flags always override settings.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent
SETTINGS_FILE = SKILL_DIR / "settings.json"
SKILL_SCRIPTS = SKILL_DIR / "scripts"
OZON_QUESTIONS_SCRIPT = WORKSPACE_DIR / "skills" / "ozon-questions-api" / "scripts" / "ozon_questions.py"
PROMPTS_DIR = WORKSPACE_DIR / "data" / "qa_prompts"
REPORTS_DIR = WORKSPACE_DIR / "data" / "qa_reports"

sys.path.insert(0, str(SKILL_SCRIPTS))

from prepare_context import build_context, build_batch_prompt

DEFAULT_SETTINGS = {
    "batch_size": 10,
    "lookup_period_days": 7,
    "dry_run": True,
    "auto_schedule_enabled": False,
    "auto_schedule_interval_minutes": 60,
    "min_accuracy_score": 7,
    "min_sufficiency_score": 7,
}


def load_settings():
    """Load agent settings from JSON. Create with defaults if missing."""
    if SETTINGS_FILE.exists():
        try:
            data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            merged = dict(DEFAULT_SETTINGS)
            merged.update(data)
            return merged
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[WARN] Failed to read settings: {exc}. Using defaults.", file=sys.stderr)
    else:
        SETTINGS_FILE.write_text(
            json.dumps(DEFAULT_SETTINGS, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[INFO] Created default settings: {SETTINGS_FILE}", file=sys.stderr)
    return dict(DEFAULT_SETTINGS)


def run_ozon_questions_list(status="UNPROCESSED", date_from=None):
    """Fetch question list from Ozon API. Returns list of question dicts."""
    cmd = [sys.executable, str(OZON_QUESTIONS_SCRIPT), "list", "--status", status]
    if date_from:
        cmd.extend(["--date-from", date_from])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] ozon_questions.py list failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON from ozon_questions.py list:\n{result.stdout}\n{exc}", file=sys.stderr)
        sys.exit(1)

    if "error" in data:
        print(f"[ERROR] API error: {data['error']}", file=sys.stderr)
        sys.exit(1)

    questions = data.get("questions", [])
    if not isinstance(questions, list):
        print("[ERROR] Unexpected response format: 'questions' is not a list", file=sys.stderr)
        sys.exit(1)
    return questions


def prepare_batch(max_questions, lookup_days, dry_run, output_dir):
    """Phase A: fetch questions, build contexts, save batch prompt + metadata."""
    date_from = None
    if lookup_days:
        cutoff = datetime.now() - timedelta(days=lookup_days)
        date_from = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"[INFO] Looking back {lookup_days} days (from {date_from})...", file=sys.stderr)

    print(f"[INFO] Fetching up to {max_questions} UNPROCESSED questions...", file=sys.stderr)
    raw_questions = run_ozon_questions_list(date_from=date_from)

    if not raw_questions:
        print("[INFO] No unprocessed questions found.", file=sys.stderr)
        sys.exit(0)

    raw_questions = raw_questions[:max_questions]
    print(f"[INFO] Processing {len(raw_questions)} questions...", file=sys.stderr)

    contexts = []
    skipped = []
    for q in raw_questions:
        question_id = q.get("id", "")
        if not question_id:
            skipped.append({"reason": "missing question_id", "raw": q})
            continue
        try:
            ctx = build_context(question_id)
            contexts.append(ctx)
            print(f"[INFO] Context ready for {question_id}", file=sys.stderr)
        except RuntimeError as exc:
            skipped.append({"question_id": question_id, "reason": str(exc)})
            print(f"[WARN] Skipped {question_id}: {exc}", file=sys.stderr)

    if not contexts:
        print("[ERROR] No contexts could be built. All questions skipped.", file=sys.stderr)
        for s in skipped:
            print(f"  - {s}", file=sys.stderr)
        sys.exit(1)

    batch_prompt = build_batch_prompt(contexts)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(output_dir) if output_dir else PROMPTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = out_dir / f"batch_{timestamp}.txt"
    meta_path = out_dir / f"batch_{timestamp}.json"

    prompt_path.write_text(batch_prompt, encoding="utf-8")

    metadata = {
        "timestamp": timestamp,
        "status": "prepared",
        "dry_run": dry_run,
        "question_count": len(contexts),
        "question_ids": [ctx["question_info"]["id"] for ctx in contexts],
        "context_paths": [ctx["context_path"] for ctx in contexts],
        "prompt_path": str(prompt_path),
        "skipped": skipped,
    }
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 60)
    print("BATCH PREPARED")
    if dry_run:
        print("MODE: DRY RUN — reports will be generated, but NO answers will be posted to Ozon.")
    print("=" * 60)
    print(f"Questions ready:   {len(contexts)}")
    print(f"Questions skipped: {len(skipped)}")
    print(f"Prompt file:       {prompt_path}")
    print(f"Metadata file:     {meta_path}")
    print()
    print("NEXT STEP: Run a subagent with the prompt file.")
    print("Then run: python3 answer_question.py finalize-batch \\")
    print(f"  --batch-metadata {meta_path} \\")
    print("  --answers-json <subagent_output.json>")
    print("=" * 60)
    print()

    print(json.dumps(metadata, ensure_ascii=False, indent=2))


def finalize_batch(batch_metadata_path, answers_json_path, dry_run, output_dir=None):
    """Phase B: read subagent answers, filter by scores, generate reports + combined JSON."""
    batch_metadata_path = Path(batch_metadata_path)
    answers_json_path = Path(answers_json_path)

    if not batch_metadata_path.exists():
        print(f"[ERROR] Batch metadata not found: {batch_metadata_path}", file=sys.stderr)
        sys.exit(1)
    if not answers_json_path.exists():
        print(f"[ERROR] Answers JSON not found: {answers_json_path}", file=sys.stderr)
        sys.exit(1)

    metadata = json.loads(batch_metadata_path.read_text(encoding="utf-8"))
    answers_raw = json.loads(answers_json_path.read_text(encoding="utf-8"))

    if isinstance(answers_raw, dict) and "answers" in answers_raw:
        answers = answers_raw["answers"]
    elif isinstance(answers_raw, list):
        answers = answers_raw
    else:
        print(f"[ERROR] Answers JSON must be a list or {{answers: [...]}}. Got: {type(answers_raw)}", file=sys.stderr)
        sys.exit(1)

    settings = load_settings()
    min_acc = settings.get("min_accuracy_score", 7)
    min_suf = settings.get("min_sufficiency_score", 7)

    question_ids = metadata.get("question_ids", [])
    context_paths = metadata.get("context_paths", [])
    id_to_context_path = dict(zip(question_ids, context_paths))

    reports_dir = Path(output_dir) if output_dir else REPORTS_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    results = []
    matched = 0
    unmatched = []
    filtered = []

    for ans in answers:
        qid = ans.get("question_id", "")
        if qid not in id_to_context_path:
            unmatched.append(ans)
            print(f"[WARN] Answer with unknown question_id skipped: {qid}", file=sys.stderr)
            continue

        acc = ans.get("accuracy_score", 0) or 0
        suf = ans.get("sufficiency_score", 0) or 0
        if acc < min_acc or suf < min_suf:
            filtered.append({"question_id": qid, "accuracy_score": acc, "sufficiency_score": suf})
            print(f"[INFO] Filtered out {qid} (acc={acc}, suf={suf}) below thresholds (acc>={min_acc}, suf>={min_suf})", file=sys.stderr)
            continue

        context_path = id_to_context_path[qid]
        ctx_data = json.loads(Path(context_path).read_text(encoding="utf-8"))
        sku = ctx_data.get("question_info", {}).get("sku")

        tmp_json = Path(f"/tmp/answer_{qid}.json")
        tmp_json.write_text(json.dumps(ans, ensure_ascii=False, indent=2), encoding="utf-8")

        report_path = reports_dir / f"final_{qid}_{timestamp}.md"
        cmd = [
            sys.executable,
            str(SKILL_SCRIPTS / "generate_answer.py"),
            "--context-json", context_path,
            "--fill-json", str(tmp_json),
            "--output", str(report_path),
        ]
        gen_result = subprocess.run(cmd, capture_output=True, text=True)
        if gen_result.returncode != 0:
            print(f"[ERROR] generate_answer.py failed for {qid}:\n{gen_result.stderr}", file=sys.stderr)
            continue

        try:
            output = json.loads(gen_result.stdout)
        except json.JSONDecodeError:
            output = {"report_path": "unknown"}

        matched += 1
        results.append({
            "question_id": qid,
            "sku": sku,
            "answer": ans.get("answer", ""),
            "sufficiency_score": ans.get("sufficiency_score"),
            "accuracy_score": ans.get("accuracy_score"),
            "reasoning": ans.get("reasoning", ""),
            "report_path": output.get("report_path", ""),
        })

    combined = {
        "timestamp": timestamp,
        "dry_run": dry_run,
        "batch_metadata": str(batch_metadata_path),
        "total_questions": len(question_ids),
        "answered": matched,
        "unmatched_answers": len(unmatched),
        "filtered_by_score": len(filtered),
        "score_thresholds": {"min_accuracy_score": min_acc, "min_sufficiency_score": min_suf},
        "results": results,
    }
    combined_path = reports_dir / f"batch_{timestamp}.json"
    combined_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")

    upload_payload = {
        "timestamp": timestamp,
        "dry_run": dry_run,
        "answers": [
            {"question_id": r["question_id"], "sku": r["sku"], "text": r["answer"]}
            for r in results
        ],
    }
    ai_qa_path = WORKSPACE_DIR / "data" / "ai_questions_answers.json"
    ai_qa_path.parent.mkdir(parents=True, exist_ok=True)
    ai_qa_path.write_text(json.dumps(upload_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 60)
    print("BATCH FINALIZED")
    if dry_run:
        print("MODE: DRY RUN — reports generated, but NO answers were posted to Ozon.")
    print("=" * 60)
    print(f"Total questions:      {len(question_ids)}")
    print(f"Filtered by score:    {len(filtered)}")
    print(f"Unmatched answers:    {len(unmatched)}")
    print(f"Final reports:        {matched}")
    print(f"Combined JSON:        {combined_path}")
    print(f"Upload payload:       {ai_qa_path}")
    print()
    for r in results:
        print(f"- {r['question_id']}: {r['answer'][:60]}... (S:{r['sufficiency_score']}/A:{r['accuracy_score']})")
    print("=" * 60)
    print()


def apply_batch(batch_metadata_path, answers_json_path, dry_run):
    """Phase C: post filtered answers to Ozon API."""
    batch_metadata_path = Path(batch_metadata_path)
    answers_json_path = Path(answers_json_path)

    if not batch_metadata_path.exists():
        print(f"[ERROR] Batch metadata not found: {batch_metadata_path}", file=sys.stderr)
        sys.exit(1)
    if not answers_json_path.exists():
        print(f"[ERROR] Answers JSON not found: {answers_json_path}", file=sys.stderr)
        sys.exit(1)

    answers_data = json.loads(answers_json_path.read_text(encoding="utf-8"))
    results = answers_data.get("results", [])
    if not results:
        print("[INFO] No answers to apply.", file=sys.stderr)
        sys.exit(0)

    total = len(results)
    success = 0
    failed = []

    print()
    print("=" * 60)
    if dry_run:
        print("APPLY BATCH — DRY RUN")
        print("No answers will be posted to Ozon.")
    else:
        print("APPLY BATCH")
        print("Posting answers to Ozon...")
    print("=" * 60)
    print()

    for r in results:
        qid = r.get("question_id", "")
        sku = r.get("sku")
        text = r.get("answer", "")

        if not sku:
            failed.append({"question_id": qid, "error": "missing sku"})
            print(f"[SKIP] {qid}: missing sku", file=sys.stderr)
            continue

        if dry_run:
            print(f"[DRY RUN] Would post to {qid} (SKU {sku}): {text[:80]}...")
            success += 1
            continue

        cmd = [
            sys.executable, str(OZON_QUESTIONS_SCRIPT), "answer-create",
            "--question-id", qid,
            "--sku", str(sku),
            "--text", text,
        ]
        post_result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            resp = json.loads(post_result.stdout)
        except json.JSONDecodeError:
            resp = {"error": post_result.stdout or post_result.stderr}

        if post_result.returncode != 0 or "error" in resp:
            err_msg = resp.get("error", resp) if isinstance(resp, dict) else str(resp)
            failed.append({"question_id": qid, "error": err_msg})
            print(f"[FAIL] {qid}: {err_msg}", file=sys.stderr)
        else:
            success += 1
            print(f"[OK] {qid}: posted successfully")

    print()
    print("=" * 60)
    print("APPLY BATCH COMPLETE")
    print("=" * 60)
    print(f"Total attempted: {total}")
    print(f"Successful:      {success}")
    print(f"Failed:          {len(failed)}")
    if failed:
        print()
        print("Failures:")
        for f in failed:
            print(f"  - {f['question_id']}: {f['error']}")
    print("=" * 60)
    print()

    summary = {
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "dry_run": dry_run,
        "total": total,
        "success": success,
        "failed": failed,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main():
    settings = load_settings()

    parser = argparse.ArgumentParser(description="Batch orchestrator for Ozon question answering")
    parser.add_argument(
        "--settings",
        default=str(SETTINGS_FILE),
        help="Path to agent settings JSON",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prep = subparsers.add_parser("prepare-batch", help="Fetch questions and build batch prompt")
    prep.add_argument(
        "--max", type=int, default=settings.get("batch_size", 10),
        help="Max questions to fetch (default: from settings)",
    )
    prep.add_argument(
        "--lookup-days", type=int, default=settings.get("lookup_period_days", 7),
        help="How many days back to look (default: from settings)",
    )
    prep.add_argument(
        "--dry-run", action="store_true", default=settings.get("dry_run", True),
        help="Dry run mode: do not post answers to Ozon",
    )
    prep.add_argument(
        "--output-dir",
        help="Directory to save prompt and metadata (default: workspace/data/qa_prompts)",
    )

    fin = subparsers.add_parser("finalize-batch", help="Generate reports from subagent answers")
    fin.add_argument("--batch-metadata", required=True, help="Path to batch metadata JSON from prepare-batch")
    fin.add_argument("--answers-json", required=True, help="Path to subagent answers JSON array")
    fin.add_argument(
        "--dry-run", action="store_true", default=settings.get("dry_run", True),
        help="Dry run mode: do not post answers to Ozon",
    )
    fin.add_argument(
        "--output-dir",
        help="Directory to save reports (default: workspace/data/qa_reports)",
    )

    app = subparsers.add_parser("apply-batch", help="Post filtered answers to Ozon API")
    app.add_argument("--batch-metadata", required=True, help="Path to batch metadata JSON")
    app.add_argument("--answers-json", required=True, help="Path to combined answers JSON from finalize-batch")
    app.add_argument(
        "--dry-run", action="store_true", default=settings.get("dry_run", True),
        help="Dry run mode: do not post answers to Ozon",
    )

    args = parser.parse_args()

    if args.command == "prepare-batch":
        prepare_batch(args.max, args.lookup_days, args.dry_run, args.output_dir)
    elif args.command == "finalize-batch":
        finalize_batch(args.batch_metadata, args.answers_json, args.dry_run, args.output_dir)
    elif args.command == "apply-batch":
        apply_batch(args.batch_metadata, args.answers_json, args.dry_run)


if __name__ == "__main__":
    main()
