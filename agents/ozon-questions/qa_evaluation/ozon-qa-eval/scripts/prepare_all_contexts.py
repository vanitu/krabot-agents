#!/usr/bin/env python3
"""Bulk-run prepare_context.py for all questions in a ground-truth file.

Resumable: skips questions whose context file already exists.

Usage:
    python3 prepare_all_contexts.py --ground-truth workspace/data/qa_benchmark/ground_truth_20260413.json
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent
CONTEXTS_DIR = WORKSPACE_DIR / "data" / "qa_benchmark" / "contexts"
PREPARE_SCRIPT = SKILL_DIR.parent / "ozon-question-answer" / "scripts" / "prepare_context.py"


def main():
    parser = argparse.ArgumentParser(description="Bulk prepare contexts for benchmark questions")
    parser.add_argument("--ground-truth", required=True, help="Path to ground_truth JSON file")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between API calls in seconds")
    args = parser.parse_args()

    ground_truth_path = Path(args.ground_truth)
    if not ground_truth_path.exists():
        print(f"[ERROR] Ground truth file not found: {ground_truth_path}", file=sys.stderr)
        sys.exit(1)

    CONTEXTS_DIR.mkdir(parents=True, exist_ok=True)

    data = json.loads(ground_truth_path.read_text(encoding="utf-8"))
    total = len(data)
    succeeded = 0
    skipped = 0
    failed = 0

    for idx, item in enumerate(data, start=1):
        qid = item.get("question_id")
        if not qid:
            print(f"[{idx}/{total}] Skipping entry without question_id", file=sys.stderr)
            failed += 1
            continue

        out_file = CONTEXTS_DIR / f"{qid}.json"
        if out_file.exists():
            print(f"[{idx}/{total}] Context already exists for {qid}, skipping", file=sys.stderr)
            skipped += 1
            continue

        print(f"[{idx}/{total}] Preparing context for {qid}...", file=sys.stderr)
        cmd = [sys.executable, str(PREPARE_SCRIPT), "--question-id", qid]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[ERROR] prepare_context.py failed for {qid}:\n{result.stderr}", file=sys.stderr)
            failed += 1
            continue

        try:
            context = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            print(f"[ERROR] Invalid JSON from prepare_context.py for {qid}:\n{result.stdout}\n{exc}", file=sys.stderr)
            failed += 1
            continue

        out_file.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
        succeeded += 1
        time.sleep(args.delay)

    print(f"\n[INFO] Done. Total: {total}, Succeeded: {succeeded}, Skipped: {skipped}, Failed: {failed}", file=sys.stderr)


if __name__ == "__main__":
    main()
