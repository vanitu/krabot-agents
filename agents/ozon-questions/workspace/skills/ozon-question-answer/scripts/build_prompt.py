#!/usr/bin/env python3
"""Build and print the agent prompt for a given Ozon question_id.

Usage:
    python3 build_prompt.py --question-id <uuid>
"""

import argparse
import sys
from pathlib import Path

# Allow importing prepare_context from sibling script
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from prepare_context import build_context


def main():
    parser = argparse.ArgumentParser(description="Build agent prompt for an Ozon buyer question")
    parser.add_argument("--question-id", required=True, help="Ozon question UUID")
    args = parser.parse_args()

    try:
        ctx = build_context(args.question_id)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    print(ctx["agent_prompt"])


if __name__ == "__main__":
    main()
