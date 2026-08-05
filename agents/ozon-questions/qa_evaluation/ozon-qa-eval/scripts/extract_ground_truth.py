#!/usr/bin/env python3
"""Extract processed Ozon questions that have human answers.

Usage:
    python3 extract_ground_truth.py --limit 50
    python3 extract_ground_truth.py --date-from 2026-04-01 --date-to 2026-04-10
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent
DATA_DIR = WORKSPACE_DIR / "data" / "qa_benchmark"
OZON_QUESTIONS_SCRIPT = SKILL_DIR.parent / "ozon-questions-api" / "scripts" / "ozon_questions.py"


def run_ozon(*args):
    cmd = [sys.executable, str(OZON_QUESTIONS_SCRIPT), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] ozon_questions.py {' '.join(args)} failed:\n{result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON from ozon_questions.py {' '.join(args)}:\n{result.stdout}\n{exc}", file=sys.stderr)
        return None


def fetch_answer_text(question_id, sku):
    data = run_ozon("answer-list", "--question-id", question_id, "--sku", str(sku))
    if data is None or "error" in data:
        return None
    answers = data.get("answers", [])
    if not answers:
        return None
    # Prefer the first non-empty text answer
    for ans in answers:
        text = ans.get("text", "").strip()
        if text:
            return text
    return None


def main():
    parser = argparse.ArgumentParser(description="Extract processed Ozon questions with human answers")
    parser.add_argument("--limit", type=int, default=0, help="Max questions to collect (0 = unlimited)")
    parser.add_argument("--status", choices=["ALL", "NEW", "VIEWED", "PROCESSED", "UNPROCESSED"], default="PROCESSED", help="Question status filter")
    parser.add_argument("--date-from", default="", help="Start date filter (ISO 8601)")
    parser.add_argument("--date-to", default="", help="End date filter (ISO 8601)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between API calls in seconds")
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Fetching {args.status} questions from Ozon...", file=sys.stderr)

    collected = []
    limit = args.limit if args.limit > 0 else None
    last_id = ""
    page = 0

    while True:
        page += 1
        list_args = ["list", "--status", args.status, "--last-id", last_id]
        if args.date_from:
            list_args += ["--date-from", args.date_from]
        if args.date_to:
            list_args += ["--date-to", args.date_to]

        list_data = run_ozon(*list_args)
        if list_data is None or "error" in list_data:
            print(f"[ERROR] Failed to fetch question list on page {page}", file=sys.stderr)
            break

        questions = list_data.get("questions", [])
        if not questions:
            print(f"[INFO] No more questions on page {page}", file=sys.stderr)
            break

        print(f"[INFO] Page {page}: fetched {len(questions)} question(s)", file=sys.stderr)

        for q in questions:
            if limit is not None and len(collected) >= limit:
                break

            qid = q.get("id")
            sku = q.get("sku")
            text = q.get("text", "").strip()
            if not qid or not sku or not text:
                print(f"[WARN] Skipping question due to missing id/sku/text", file=sys.stderr)
                continue

            print(f"[collecting {len(collected) + 1}] Fetching answer for {qid}...", file=sys.stderr)
            human_answer = fetch_answer_text(qid, sku)
            time.sleep(args.delay)

            if not human_answer:
                print(f"[WARN] No human answer for {qid}, skipping", file=sys.stderr)
                continue

            collected.append({
                "question_id": qid,
                "sku": sku,
                "question_text": text,
                "human_answer": human_answer,
                "product_url": q.get("product_url", ""),
                "published_at": q.get("published_at", ""),
            })

        if limit is not None and len(collected) >= limit:
            print(f"[INFO] Reached limit of {limit} collected entries", file=sys.stderr)
            break

        last_id = list_data.get("last_id", "")
        if not last_id:
            print(f"[INFO] No more pages to fetch", file=sys.stderr)
            break

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = DATA_DIR / f"ground_truth_{timestamp}.json"
    out_path.write_text(json.dumps(collected, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[INFO] Saved {len(collected)} entries to: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
