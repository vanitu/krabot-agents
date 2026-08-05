#!/usr/bin/env python3
"""
Merge all batch answer JSON files into a single output file.

Looks for files matching:
  data/qa_benchmark/answers/bulk_answers_batch_*.json

Concatenates their arrays and writes:
  data/qa_benchmark/answers/bulk_answers_merged.json
"""

import json
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANSWERS_DIR = os.path.join(BASE_DIR, "data", "qa_benchmark", "answers")
OUTPUT_FILENAME = "bulk_answers_merged.json"


def main():
    pattern = "bulk_answers_batch_"
    files = [
        f for f in os.listdir(ANSWERS_DIR)
        if f.startswith(pattern) and f.endswith(".json")
    ]

    if not files:
        print(f"No batch files found in {ANSWERS_DIR}", file=sys.stderr)
        sys.exit(1)

    # Sort by the numeric suffix so order is deterministic
    def sort_key(name):
        core = name[len(pattern):].replace(".json", "")
        try:
            return int(core)
        except ValueError:
            return core

    files.sort(key=sort_key)

    merged = []
    for name in files:
        path = os.path.join(ANSWERS_DIR, name)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"Warning: {name} does not contain a JSON array, skipping.", file=sys.stderr)
            continue
        merged.extend(data)
        print(f"Loaded {len(data):3d} answers from {name}")

    output_path = os.path.join(ANSWERS_DIR, OUTPUT_FILENAME)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"\nTotal merged answers: {len(merged)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
