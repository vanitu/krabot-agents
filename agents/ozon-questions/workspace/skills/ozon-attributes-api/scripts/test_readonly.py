#!/usr/bin/env python3
"""Test read-only commands of ozon_attributes.py against the live Ozon Seller API.

Prerequisites:
    export OZON_CLIENT_ID=<your_client_id>
    export OZON_API_KEY=<your_api_key>
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("ozon_attributes.py")


def run_cmd(*args):
    """Run ozon_attributes.py with given args and return parsed JSON."""
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


def find_first_leaf(node):
    """Recursively find first leaf node with type_id (end of tree branch)."""
    children = node.get("children", [])
    if not children and node.get("type_id") is not None:
        return node
    for child in children:
        leaf = find_first_leaf(child)
        if leaf:
            return leaf
    # fallback: any node with type_id even if it has children
    if node.get("type_id") is not None:
        return node
    return None


def main():
    client_id = os.environ.get("OZON_CLIENT_ID")
    api_key = os.environ.get("OZON_API_KEY")
    if not client_id or not api_key:
        print("Error: OZON_CLIENT_ID and OZON_API_KEY environment variables must be set.")
        sys.exit(1)

    all_passed = True
    leaf_category_id = None
    leaf_type_id = None
    sample_attribute_id = None

    # 1. Test tree
    print("\n=== Testing tree ===")
    data = run_cmd("tree", "--language", "RU")
    if data is None:
        all_passed = False
    elif "error" in data:
        print(f"[FAIL] tree returned error: {data['error']}")
        all_passed = False
    else:
        all_passed &= check_keys(data, ["result"], "tree")
        if data.get("result"):
            leaf = find_first_leaf(data["result"][0])
            if leaf:
                leaf_category_id = leaf.get("description_category_id")
                leaf_type_id = leaf.get("type_id")
                print(f"[INFO] Found leaf category_id={leaf_category_id}, type_id={leaf_type_id}")

    # 2. Test attributes
    print("\n=== Testing attributes ===")
    if leaf_category_id and leaf_type_id:
        data = run_cmd(
            "attributes",
            "--description-category-id", str(leaf_category_id),
            "--type-id", str(leaf_type_id),
            "--language", "RU",
        )
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] attributes returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(data, ["result"], "attributes")
            if data.get("result"):
                for attr in data["result"]:
                    if attr.get("dictionary_id", 0) > 0:
                        sample_attribute_id = attr.get("id")
                        print(f"[INFO] Found attribute with dictionary_id={attr.get('dictionary_id')}: id={sample_attribute_id}")
                        break
    else:
        print("[SKIP] attributes — no leaf category/type found to test with.")

    # 3. Test attribute-values
    print("\n=== Testing attribute-values ===")
    if leaf_category_id and leaf_type_id and sample_attribute_id:
        data = run_cmd(
            "attribute-values",
            "--attribute-id", str(sample_attribute_id),
            "--description-category-id", str(leaf_category_id),
            "--type-id", str(leaf_type_id),
            "--limit", "20",
            "--last-value-id", "0",
            "--language", "RU",
        )
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] attribute-values returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(data, ["result", "has_next"], "attribute-values")
    else:
        print("[SKIP] attribute-values — no suitable attribute found to test with.")

    # 4. Test attribute-values-search
    print("\n=== Testing attribute-values-search ===")
    if leaf_category_id and leaf_type_id and sample_attribute_id:
        data = run_cmd(
            "attribute-values-search",
            "--attribute-id", str(sample_attribute_id),
            "--description-category-id", str(leaf_category_id),
            "--type-id", str(leaf_type_id),
            "--limit", "10",
            "--value", "а",
        )
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] attribute-values-search returned error: {data['error']}")
            all_passed = False
        else:
            all_passed &= check_keys(data, ["result"], "attribute-values-search")
    else:
        print("[SKIP] attribute-values-search — no suitable attribute found to test with.")

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
