#!/usr/bin/env python3
"""Integration test for the full Ozon Reviews workflow.

WARNING: This test posts REAL comments for unprocessed 4-5 star reviews.
Run only in a real Ozon Seller account with that understanding.

Prerequisites:
    export OZON_CLIENT_ID=<your_client_id>
    export OZON_API_KEY=<your_api_key>
"""

import json
import os
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
API_SCRIPT = WORKSPACE / "skills" / "ozon-reviews-api" / "scripts" / "ozon_reviews.py"
WORKFLOW_SCRIPT = WORKSPACE / "skills" / "ozon-reviews-workflow" / "scripts" / "process_reviews.py"
DATA_DIR = WORKSPACE / "data"


def run_script(script_path, *args):
    cmd = [sys.executable, str(script_path), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def parse_json_stdout(stdout):
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        print(f"[FAIL] Invalid JSON: {exc}")
        print(f"stdout: {stdout}")
        return None


def main():
    client_id = os.environ.get("OZON_CLIENT_ID")
    api_key = os.environ.get("OZON_API_KEY")
    if not client_id or not api_key:
        print("Error: OZON_CLIENT_ID and OZON_API_KEY must be set.")
        sys.exit(1)

    all_passed = True

    # 1. Test API connectivity
    print("\n=== 1. API Connectivity (count) ===")
    rc, stdout, stderr = run_script(API_SCRIPT, "count")
    if rc != 0:
        print(f"[FAIL] count command failed. stderr: {stderr}")
        all_passed = False
    else:
        data = parse_json_stdout(stdout)
        if data is None:
            all_passed = False
        elif "error" in data:
            print(f"[FAIL] count returned error: {data['error']}")
            all_passed = False
        else:
            print(f"[PASS] count: total={data.get('total')}, unprocessed={data.get('unprocessed')}")

    # 2. Run workflow stage 1
    print("\n=== 2. Workflow Stage 1 (process_reviews.py) ===")
    rc, stdout, stderr = run_script(WORKFLOW_SCRIPT)
    print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    if rc != 0:
        print("[FAIL] process_reviews.py exited with non-zero code")
        all_passed = False
    else:
        print("[PASS] process_reviews.py completed")

    # 3. Verify report created
    print("\n=== 3. Report file created ===")
    reports = sorted(DATA_DIR.glob("report_*.md"))
    if not reports:
        print("[FAIL] No report file found in data/")
        all_passed = False
        latest_report = None
    else:
        latest_report = reports[-1]
        print(f"[PASS] Report found: {latest_report.name}")

    # 4. Check pending AI batch
    pending_path = DATA_DIR / "pending_ai_reviews.json"
    ai_answers_path = DATA_DIR / "test_ai_answers.json"
    if pending_path.exists():
        print("\n=== 4. AI Batch exists, testing --apply-ai ===")
        with open(pending_path, "r", encoding="utf-8") as f:
            pending = json.load(f)

        reviews = pending.get("reviews", [])
        if reviews:
            # Generate a single dummy AI answer for the first review
            dummy = {
                "answers": [
                    {
                        "review_id": reviews[0]["review_id"],
                        "text": "Благодарим за подробный отзыв! Рады, что покупка оправдала ожидания.",
                    }
                ]
            }
            with open(ai_answers_path, "w", encoding="utf-8") as f:
                json.dump(dummy, f, ensure_ascii=False, indent=2)

            rc, stdout, stderr = run_script(WORKFLOW_SCRIPT, "--apply-ai", str(ai_answers_path))
            print(stdout)
            if stderr:
                print(stderr, file=sys.stderr)
            if rc != 0:
                print("[FAIL] --apply-ai exited with non-zero code")
                all_passed = False
            else:
                print("[PASS] --apply-ai completed")

            # Verify report was updated
            if latest_report:
                content = latest_report.read_text(encoding="utf-8")
                if "AI-ответы (Группа C) — опубликованы" in content or "опубликованы" in content:
                    print("[PASS] Report was updated with AI results")
                else:
                    print("[WARN] Report may not contain AI section yet (possible delay)")
        else:
            print("[SKIP] pending_ai_reviews.json exists but contains no reviews")
    else:
        print("\n=== 4. AI Batch ===")
        print("[SKIP] No pending_ai_reviews.json found (group C was empty)")

    # 5. Verify template replies were attempted
    print("\n=== 5. Template replies attempted ===")
    if latest_report:
        content = latest_report.read_text(encoding="utf-8")
        has_a = "Группа A" in content
        has_b = "Группа B" in content
        if has_a or has_b:
            print(f"[PASS] Report mentions groups: A={has_a}, B={has_b}")
        else:
            print("[INFO] No template groups mentioned — likely no matching reviews")
    else:
        all_passed = False

    # Cleanup test artifact
    if ai_answers_path.exists():
        ai_answers_path.unlink()
        print(f"[INFO] Cleaned up {ai_answers_path.name}")

    # Summary
    print("\n=== SUMMARY ===")
    if all_passed:
        print("Integration test passed.")
        sys.exit(0)
    else:
        print("Integration test had failures.")
        sys.exit(1)


if __name__ == "__main__":
    main()
