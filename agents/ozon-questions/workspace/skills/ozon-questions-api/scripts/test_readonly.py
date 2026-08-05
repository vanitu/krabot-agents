#!/usr/bin/env python3
"""Test read-only commands of ozon_questions.py against the live Ozon Seller API.

Prerequisites:
    export OZON_CLIENT_ID=<your_client_id>
    export OZON_API_KEY=<your_api_key>
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("ozon_questions.py")


def run_cmd(*args):
    """Run ozon_questions.py with given args and return parsed JSON."""
    cmd = [sys.executable, str(SCRIPT), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[FAIL] Command failed: {' '.join(args)}")
        print(f"stderr: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"[FAIL] Invalid JSON output for: {' '.join(args)}")
        print(f"stdout: {result.stdout}")
        print(f"exc: {exc}")
        return None


def check_keys(data, keys, label):
    """Check that all expected keys exist in data dict."""
    missing = [k for k in keys if k not in data]
    if missing:
        print(f"[FAIL] {label} — missing keys: {missing}")
        return False
    print(f"[PASS] {label}")
    return True


def main():
    client_id = os.environ.get("OZON_CLIENT_ID")
    api_key = os.environ.get("OZON_API_KEY")
    if not client_id or not api_key:
        print("Error: OZON_CLIENT_ID and OZON_API_KEY environment variables must be set.")
        sys.exit(1)

    all_passed = True
    question_id_for_details = None
    sku_for_details = None

    # 1. Test count
    print("\n=== Testing count ===")
    data = run_cmd("count")
    if data is None:
        all_passed = False
    elif "error" in data:
        print(f"[FAIL] count returned error: {data['error']}")
        all_passed = False
    else:
        all_passed &= check_keys(data, ["all", "new", "processed", "unprocessed", "viewed"], "count")

    # 2. Test list with multiple filtration patterns
    print("\n=== Testing list with different filters ===")
    list_configs = [
        ("ALL",),
        ("NEW",),
        ("UNPROCESSED",),
        ("PROCESSED",),
        ("VIEWED",),
    ]

    for (status,) in list_configs:
        label = f"list --status {status}"
        data = run_cmd("list", "--status", status, "--last-id", "")
        if data is None:
            all_passed = False
            continue
        if "error" in data:
            print(f"[FAIL] {label} returned error: {data['error']}")
            all_passed = False
            continue

        passed = check_keys(data, ["questions", "last_id"], label)
        all_passed &= passed

        if passed and data.get("questions") and not question_id_for_details:
            question_id_for_details = data["questions"][0].get("id")
            sku_for_details = data["questions"][0].get("sku")

        # Test pagination if has_next hint exists and last_id is present
        if status == "ALL" and data.get("last_id"):
            pag_label = f"list pagination --last-id {data['last_id']}"
            pag_data = run_cmd("list", "--status", status, "--last-id", data["last_id"])
            if pag_data is None:
                all_passed = False
            elif "error" in pag_data:
                print(f"[FAIL] {pag_label} returned error: {pag_data['error']}")
                all_passed = False
            else:
                all_passed &= check_keys(pag_data, ["questions", "last_id"], pag_label)

    # 3. Test info and answer-list if we have a question_id
    print("\n=== Testing info & answer-list ===")
    if question_id_for_details:
        data = run_cmd("info", "--question-id", question_id_for_details)
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] info returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(
                data,
                ["id", "text", "status", "sku"],
                f"info --question-id {question_id_for_details}",
            )

        if sku_for_details:
            data = run_cmd(
                "answer-list",
                "--question-id", question_id_for_details,
                "--sku", str(sku_for_details),
            )
            if data is None:
                all_passed = False
            elif "error" in data:
                print(f"[FAIL] answer-list returned error: {data['error']}")
                all_passed = False
            else:
                all_passed &= check_keys(
                    data,
                    ["answers", "last_id"],
                    f"answer-list --question-id {question_id_for_details}",
                )
        else:
            print("[SKIP] answer-list — no SKU found to test with.")
    else:
        print("[SKIP] info & answer-list — no questions found to test with.")

    # Summary
    print("\n=== SUMMARY ===")
    if all_passed:
        print("All available read-only tests passed.")
        sys.exit(0)
    else:
        print("Some tests failed or were skipped.")
        sys.exit(1)


if __name__ == "__main__":
    main()
