#!/usr/bin/env python3
"""Build a single work-list JSON for the Agent to fill with AI answers.

Usage:
    python3 build_answer_batch.py --ground-truth workspace/data/qa_benchmark/ground_truth_20260413.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent
DATA_DIR = WORKSPACE_DIR / "data" / "qa_benchmark"
CONTEXTS_DIR = DATA_DIR / "contexts"


def main():
    parser = argparse.ArgumentParser(description="Build agent work-list for AI answer generation")
    parser.add_argument("--ground-truth", required=True, help="Path to ground_truth JSON file")
    args = parser.parse_args()

    gt_path = Path(args.ground_truth)
    if not gt_path.exists():
        print(f"[ERROR] Ground truth file not found: {gt_path}", file=sys.stderr)
        sys.exit(1)

    gt = json.loads(gt_path.read_text(encoding="utf-8"))
    if not isinstance(gt, list):
        print("[ERROR] Ground truth must be a JSON array", file=sys.stderr)
        sys.exit(1)

    entries = []
    for item in gt:
        qid = item.get("question_id")
        context_path = CONTEXTS_DIR / f"{qid}.json"
        if not context_path.exists():
            print(f"[WARN] Context not found for {qid}, skipping", file=sys.stderr)
            continue

        context = json.loads(context_path.read_text(encoding="utf-8"))
        agent_prompt = context.get("agent_prompt", "")
        if not agent_prompt:
            print(f"[WARN] Empty agent_prompt for {qid}, skipping", file=sys.stderr)
            continue

        entries.append({
            "question_id": qid,
            "question_text": item.get("question_text", ""),
            "human_answer": item.get("human_answer", ""),
            "context_path": str(context_path),
            "agent_prompt": agent_prompt,
            "ai_answer": "",
            "sufficiency_score": None,
            "accuracy_score": None,
            "reasoning": "",
        })

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = DATA_DIR / f"answer_batch_{timestamp}.json"
    out_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[INFO] Built answer batch with {len(entries)} entries: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
