#!/usr/bin/env python3
"""Finalize an answer by combining a prepared context with subagent output.

Usage:
    python3 finalize_answer.py --question-id <uuid> --answer-json path/to/answer.json
    # or pipe the answer JSON:
    cat answer.json | python3 finalize_answer.py --question-id <uuid>
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = SCRIPT_DIR.parent.parent.parent
CONTEXTS_DIR = WORKSPACE_DIR / "data" / "qa_contexts"


def find_latest_context(question_id):
    pattern = f"context_{question_id}_*.json"
    files = sorted(CONTEXTS_DIR.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No context files found for question_id {question_id} in {CONTEXTS_DIR}")
    return files[0]


def main():
    parser = argparse.ArgumentParser(description="Finalize answer report from context + subagent JSON")
    parser.add_argument("--question-id", required=True, help="Ozon question UUID")
    parser.add_argument("--answer-json", help="Path to JSON file with answer data")
    parser.add_argument("--output", "-o", help="Path for the output report (default: auto-generated)")
    args = parser.parse_args()

    try:
        context_path = find_latest_context(args.question_id)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    if args.answer_json:
        answer_data = Path(args.answer_json).read_text(encoding="utf-8")
    else:
        answer_data = sys.stdin.read()

    if not answer_data.strip():
        print("[ERROR] No answer data provided.", file=sys.stderr)
        sys.exit(1)

    # Validate JSON
    try:
        json.loads(answer_data)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid answer JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    # Write answer JSON to temp file for generate_answer.py
    tmp_json = Path(f"/tmp/answer_{args.question_id}.json")
    tmp_json.write_text(answer_data, encoding="utf-8")

    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "generate_answer.py"),
        "--context-json", str(context_path),
        "--fill-json", str(tmp_json),
    ]
    if args.output:
        cmd.extend(["--output", args.output])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] generate_answer.py failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(result.stdout)
        sys.exit(0)

    report_path = output.get("report_path", "unknown")
    print(f"[INFO] Final report saved to: {report_path}", file=sys.stderr)
    print()
    print("=" * 60)
    print("ВОПРОС:")
    print(output.get("question_info", {}).get("text", "N/A"))
    print()
    print("ОТВЕТ:")
    print(output.get("answer", "N/A"))
    print()
    print(f"Sufficiency: {output.get('sufficiency_score', 'N/A')} / 10")
    print(f"Accuracy:    {output.get('accuracy_score', 'N/A')} / 10")
    print("=" * 60)
    print()
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
