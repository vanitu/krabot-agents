#!/usr/bin/env python3
"""Test read-only commands of ozon_product_info.py against the live Ozon Seller API.

Prerequisites:
    export OZON_CLIENT_ID=<your_client_id>
    export OZON_API_KEY=<your_api_key>
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("ozon_product_info.py")


def run_cmd(*args):
    """Run ozon_product_info.py with given args and return parsed JSON."""
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
    sample_offer_id = None
    sample_product_id = None
    sample_sku = None

    # 1. Test attributes to find a real product
    print("\n=== Testing attributes ===")
    data = run_cmd("attributes", "--limit", "10")
    if data is None:
        all_passed = False
    elif "error" in data:
        print(f"[FAIL] attributes returned error: {data['error']}")
        all_passed = False
    else:
        all_passed &= check_keys(data, ["result", "total", "last_id"], "attributes")
        if data.get("result"):
            first = data["result"][0]
            sample_offer_id = first.get("offer_id")
            sample_product_id = first.get("id")
            sample_sku = first.get("sku")
            print(f"[INFO] Found product offer_id={sample_offer_id}, product_id={sample_product_id}, sku={sample_sku}")

    # 2. Test info-list
    print("\n=== Testing info-list ===")
    if sample_sku:
        data = run_cmd("info-list", "--sku", str(sample_sku))
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] info-list returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(data, ["items"], f"info-list --sku {sample_sku}")
    else:
        print("[SKIP] info-list — no SKU found to test with.")

    # 3. Test description
    print("\n=== Testing description ===")
    if sample_offer_id:
        data = run_cmd("description", "--offer-id", str(sample_offer_id))
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] description returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(
                data,
                ["result"],
                f"description --offer-id {sample_offer_id}",
            )
            if "result" in data:
                all_passed &= check_keys(
                    data["result"],
                    ["description", "id", "name", "offer_id"],
                    "description result structure",
                )
    else:
        print("[SKIP] description — no offer_id found to test with.")

    # 4. Test full-info
    print("\n=== Testing full-info ===")
    if sample_offer_id:
        data = run_cmd("full-info", "--offer-id", str(sample_offer_id))
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] full-info returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(
                data,
                ["info", "attributes", "attributes_enriched", "description"],
                f"full-info --offer-id {sample_offer_id}",
            )
            enriched = data.get("attributes_enriched", [])
            if enriched:
                first_enriched = enriched[0]
                all_passed &= check_keys(
                    first_enriched,
                    ["attribute_id", "attribute_name", "values"],
                    "attributes_enriched first item structure",
                )
                if first_enriched.get("values"):
                    all_passed &= check_keys(
                        first_enriched["values"][0],
                        ["dictionary_value_id", "raw_value", "resolved_value"],
                        "attributes_enriched value structure",
                    )
            else:
                print("[SKIP] attributes_enriched deep check — no enriched attributes returned.")
    else:
        print("[SKIP] full-info — no offer_id found to test with.")

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
