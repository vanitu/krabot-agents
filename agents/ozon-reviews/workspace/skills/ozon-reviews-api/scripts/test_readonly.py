#!/usr/bin/env python3
"""Test read-only commands of ozon_reviews.py against the live Ozon Seller API.

Prerequisites:
    export OZON_CLIENT_ID=<your_client_id>
    export OZON_API_KEY=<your_api_key>
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("ozon_reviews.py")


def run_cmd(*args):
    """Run ozon_reviews.py with given args and return parsed JSON."""
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
    review_id_for_details = None

    # 1. Test count
    print("\n=== Testing count ===")
    data = run_cmd("count")
    if data is None:
        all_passed = False
    elif "error" in data:
        print(f"[FAIL] count returned error: {data['error']}")
        all_passed = False
    else:
        all_passed &= check_keys(data, ["total", "processed", "unprocessed"], "count")

    # 2. Test list with multiple filtration patterns
    print("\n=== Testing list with different filters ===")
    list_configs = [
        ("ALL", "ASC"),
        ("UNPROCESSED", "DESC"),
        ("PROCESSED", "ASC"),
    ]

    for status, sort_dir in list_configs:
        label = f"list --status {status} --sort-dir {sort_dir}"
        data = run_cmd("list", "--status", status, "--limit", "20", "--sort-dir", sort_dir, "--last-id", "")
        if data is None:
            all_passed = False
            continue
        if "error" in data:
            print(f"[FAIL] {label} returned error: {data['error']}")
            all_passed = False
            continue

        passed = check_keys(data, ["reviews", "has_next", "last_id"], label)
        all_passed &= passed

        if passed and data.get("reviews") and not review_id_for_details:
            review_id_for_details = data["reviews"][0].get("id")

        # Test pagination if has_next is true (only for first config to save requests)
        if status == "ALL" and sort_dir == "ASC" and data.get("has_next") and data.get("last_id"):
            pag_label = f"list pagination --last-id {data['last_id']}"
            pag_data = run_cmd("list", "--status", status, "--limit", "20", "--sort-dir", sort_dir, "--last-id", data["last_id"])
            if pag_data is None:
                all_passed = False
            elif "error" in pag_data:
                print(f"[FAIL] {pag_label} returned error: {pag_data['error']}")
                all_passed = False
            else:
                all_passed &= check_keys(pag_data, ["reviews", "has_next", "last_id"], pag_label)

    # 3. Test info and comment-list if we have a review_id
    print("\n=== Testing info & comment-list ===")
    if review_id_for_details:
        data = run_cmd("info", "--review-id", review_id_for_details)
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] info returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(
                data,
                ["id", "rating", "text", "status", "sku"],
                f"info --review-id {review_id_for_details}",
            )

        data = run_cmd("comment-list", "--review-id", review_id_for_details, "--limit", "20")
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] comment-list returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(
                data,
                ["comments", "offset"],
                f"comment-list --review-id {review_id_for_details}",
            )
    else:
        print("[SKIP] info & comment-list — no reviews found to test with.")

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
