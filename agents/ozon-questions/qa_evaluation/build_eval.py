#!/usr/bin/env python3
"""
Build an evaluation file by joining AI-generated answers with ground truth.

Reads:
  - data/qa_benchmark/answers/bulk_answers_merged.json
  - data/qa_benchmark/ground_truth_20260415_133501.json

Joins on `question_id` and writes:
  - data/qa_benchmark/eval_merged.json

Each output item contains:
  question_id, sku, question_text, published_at,
  human_answer, ai_answer, sufficiency_score, accuracy_score, reasoning
"""

import json
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANSWERS_PATH = os.path.join(BASE_DIR, "data", "qa_benchmark", "answers", "bulk_answers_merged.json")
GROUND_TRUTH_PATH = os.path.join(BASE_DIR, "data", "qa_benchmark", "ground_truth_20260415_133501.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "qa_benchmark", "eval_merged.json")


def main():
    if not os.path.exists(ANSWERS_PATH):
        print(f"Answers file not found: {ANSWERS_PATH}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(GROUND_TRUTH_PATH):
        print(f"Ground truth file not found: {GROUND_TRUTH_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(ANSWERS_PATH, "r", encoding="utf-8") as f:
        answers = json.load(f)

    with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    answers_by_id = {item["question_id"]: item for item in answers}

    merged = []
    for gt_item in ground_truth:
        qid = gt_item["question_id"]
        ai = answers_by_id.get(qid, {})

        merged.append({
            "question_id": qid,
            "sku": gt_item.get("sku"),
            "question_text": gt_item.get("question_text"),
            "published_at": gt_item.get("published_at"),
            "human_answer": gt_item.get("human_answer"),
            "ai_answer": ai.get("answer"),
            "sufficiency_score": ai.get("sufficiency_score"),
            "accuracy_score": ai.get("accuracy_score"),
            "reasoning": ai.get("reasoning"),
        })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"Merged {len(merged)} items")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
