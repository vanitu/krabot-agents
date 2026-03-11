#!/usr/bin/env python3
"""
Create async image generation task. Returns task_id immediately.
Usage: python3 create_task.py "prompt" [--size SIZE] [--n NUM] [--negative TEXT] [--model MODEL]
Output: {"task_id": "xxx", "status": "PENDING"}
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
        raise ValueError(f"Invalid region: {region}. Use: singapore, virginia")
    return urls[region]


def create_task(
    api_key: str,
    base_url: str,
    prompt: str,
    size: str,
    n: int,
    negative_prompt: str,
    model: str,
) -> str:
    url = f"{base_url}/api/v1/services/aigc/image-generation/generation"

    data = {
        "model": model,
        "input": {"messages": [{"role": "user", "content": [{"text": prompt}]}]},
        "parameters": {"size": size, "n": n},
    }
    if negative_prompt:
        data["parameters"]["negative_prompt"] = negative_prompt

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result["output"]["task_id"]


def main():
    parser = argparse.ArgumentParser(description="Create image generation task")
    parser.add_argument("prompt", help="Text prompt")
    parser.add_argument("--size", default="1280*1280", help="Image size")
    parser.add_argument("--n", type=int, default=1, help="Number of images (1-4)")
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--model", default="wan2.6-t2i", help="Model name")
    args = parser.parse_args()

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    region = os.environ.get("DASHSCOPE_REGION")

    if not api_key or not region:
        print(json.dumps({"error": "Missing DASHSCOPE_API_KEY or DASHSCOPE_REGION"}))
        sys.exit(1)

    try:
        base_url = get_base_url(region)
        task_id = create_task(
            api_key, base_url, args.prompt, args.size, args.n, args.negative, args.model
        )
        print(json.dumps({"task_id": task_id, "status": "PENDING"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
