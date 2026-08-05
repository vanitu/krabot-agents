#!/usr/bin/env python3
"""Build a CSV evaluation batch from ground truth and AI results.

Columns: question_id, question_text, human_answer, ai_answer, match_score, ai_accuracy_score

Usage:
    python3 build_eval_batch.py \
        --ground-truth workspace/data/qa_benchmark/ground_truth_20260413.json \
        --ai-results workspace/data/qa_benchmark/ai_results_20260413.json
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent
DATA_DIR = WORKSPACE_DIR / "data" / "qa_benchmark"


def main():
    parser = argparse.ArgumentParser(description="Build evaluation CSV batch")
    parser.add_argument("--ground-truth", required=True, help="Path to ground_truth JSON file")
    parser.add_argument("--ai-results", required=True, help="Path to ai_results JSON file")
    args = parser.parse_args()

    gt_path = Path(args.ground_truth)
    ai_path = Path(args.ai_results)

    for p in (gt_path, ai_path):
        if not p.exists():
            print(f"[ERROR] File not found: {p}", file=sys.stderr)
            sys.exit(1)

    gt = {item["question_id"]: item for item in json.loads(gt_path.read_text(encoding="utf-8"))}
    ai_results = {item["question_id"]: item for item in json.loads(ai_path.read_text(encoding="utf-8"))}

    common_ids = sorted(set(gt.keys()) & set(ai_results.keys()))
    if not common_ids:
        print("[ERROR] No matching question_id found between ground truth and AI results", file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = DATA_DIR / f"eval_batch_{timestamp}.csv"

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["question_id", "question_text", "human_answer", "ai_answer", "match_score", "ai_accuracy_score"],
        )
        writer.writeheader()
        for qid in common_ids:
            writer.writerow({
                "question_id": qid,
                "question_text": gt[qid].get("question_text", ""),
                "human_answer": gt[qid].get("human_answer", ""),
                "ai_answer": ai_results[qid].get("ai_answer", ""),
                "match_score": "",
                "ai_accuracy_score": "",
            })

    print(f"[INFO] Built eval batch with {len(common_ids)} rows: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
