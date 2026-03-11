#!/usr/bin/env python3
"""
Check task status. Returns current status and URLs if complete.
Usage: python3 check_status.py <task_id>
Output: {"status": "PENDING|RUNNING|SUCCEEDED|FAILED", "urls": [...], "error": "..."}
"""

import argparse
import json
import os
import sys
import urllib.request


def get_base_url(region: str) -> str:
    urls = {
        "singapore": "https://dashscope-intl.aliyuncs.com",
        "virginia": "https://dashscope-us.aliyuncs.com",
    }
    if region not in urls:
        raise ValueError(f"Invalid region: {region}")
    return urls[region]


def extract_urls(result: dict) -> list:
    urls = []
    for choice in result.get("choices", []):
        for item in choice.get("message", {}).get("content", []):
            if "image_url" in item:
                urls.append(item["image_url"])
    return urls


def check_task(api_key: str, base_url: str, task_id: str) -> dict:
    url = f"{base_url}/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        output = result.get("output", {})
        status = output.get("task_status", "UNKNOWN")

        response = {"status": status}

        if status == "SUCCEEDED":
            response["urls"] = extract_urls(output)
        elif status == "FAILED":
            response["error"] = (
                f"{output.get('code', 'Unknown')}: {output.get('message', 'No details')}"
            )

        return response


def main():
    parser = argparse.ArgumentParser(description="Check task status")
    parser.add_argument("task_id", help="Task ID to check")
    args = parser.parse_args()

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    region = os.environ.get("DASHSCOPE_REGION")

    if not api_key or not region:
        print(json.dumps({"error": "Missing DASHSCOPE_API_KEY or DASHSCOPE_REGION"}))
        sys.exit(1)

    try:
        base_url = get_base_url(region)
        result = check_task(api_key, base_url, args.task_id)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
