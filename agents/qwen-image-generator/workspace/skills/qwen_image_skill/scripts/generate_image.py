#!/usr/bin/env python3
"""
Generate images using DashScope Wan text-to-image API.
Handles async task creation, polling, and image download.
"""

import argparse
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional


def get_base_url(region: str) -> str:
    """Get base URL for the specified region."""
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
    size: str = "1280*1280",
    n: int = 1,
    negative_prompt: str = "",
    model: str = "wan2.6-t2i",
) -> str:
    """Create async image generation task. Returns task_id."""
    import json
    import urllib.request

    url = f"{base_url}/api/v1/services/aigc/image-generation/generation"

    data = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]
        },
        "parameters": {
            "size": size,
            "n": n,
        }
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

    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
        if "output" not in result or "task_id" not in result["output"]:
            raise RuntimeError(f"Failed to create task: {result}")
        return result["output"]["task_id"]


def poll_task(
    api_key: str,
    base_url: str,
    task_id: str,
    poll_interval: int = 10,
    max_attempts: int = 60,
) -> dict:
    """Poll task until completion. Returns result dict with status and urls."""
    import json
    import urllib.request

    url = f"{base_url}/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    for attempt in range(max_attempts):
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        output = result.get("output", {})
        status = output.get("task_status", "UNKNOWN")

        if status == "SUCCEEDED":
            return output
        elif status == "FAILED":
            code = output.get("code", "Unknown")
            message = output.get("message", "No details")
            raise RuntimeError(f"Task failed: {code} - {message}")

        print(f"  Status: {status} (attempt {attempt + 1}/{max_attempts})", file=sys.stderr)
        time.sleep(poll_interval)

    raise TimeoutError(f"Task did not complete within {max_attempts * poll_interval} seconds")


def download_image(url: str, output_path: str) -> None:
    """Download image from URL to file."""
    urllib.request.urlretrieve(url, output_path)


def extract_image_urls(result: dict) -> list:
    """Extract image URLs from task result."""
    urls = []
    choices = result.get("choices", [])
    for choice in choices:
        content = choice.get("message", {}).get("content", [])
        for item in content:
            if "image_url" in item:
                urls.append(item["image_url"])
    return urls


def main():
    parser = argparse.ArgumentParser(description="Generate images using DashScope API")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--output", "-o", help="Output file path (for single image)")
    parser.add_argument("--size", default="1280*1280",
                       help="Image size: 1280*1280, 1104*1472, 1472*1104, 1696*960, 960*1696")
    parser.add_argument("--n", type=int, default=1, help="Number of images (1-4)")
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--model", default="wan2.6-t2i",
                       help="Model: wan2.6-t2i (default) or wan2.5-t2i-preview")
    parser.add_argument("--poll-interval", type=int, default=10, help="Polling interval in seconds")
    parser.add_argument("--max-attempts", type=int, default=60, help="Maximum polling attempts")

    args = parser.parse_args()

    # Get environment variables
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    region = os.environ.get("DASHSCOPE_REGION")

    if not api_key:
        print("Error: DASHSCOPE_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    if not region:
        print("Error: DASHSCOPE_REGION environment variable not set (singapore or virginia)", file=sys.stderr)
        sys.exit(1)

    base_url = get_base_url(region)

    print(f"Creating task for: {args.prompt[:50]}...", file=sys.stderr)

    try:
        task_id = create_task(
            api_key=api_key,
            base_url=base_url,
            prompt=args.prompt,
            size=args.size,
            n=args.n,
            negative_prompt=args.negative,
            model=args.model,
        )
        print(f"Task created: {task_id}", file=sys.stderr)

        print("Waiting for completion...", file=sys.stderr)
        result = poll_task(
            api_key=api_key,
            base_url=base_url,
            task_id=task_id,
            poll_interval=args.poll_interval,
            max_attempts=args.max_attempts,
        )

        image_urls = extract_image_urls(result)
        print(f"Generated {len(image_urls)} image(s)", file=sys.stderr)

        # Download images
        if args.output and len(image_urls) == 1:
            download_image(image_urls[0], args.output)
            print(f"Saved to: {args.output}", file=sys.stderr)
        else:
            output_dir = Path(args.output).parent if args.output else Path(".")
            output_dir.mkdir(parents=True, exist_ok=True)

            for i, url in enumerate(image_urls):
                ext = Path(url).suffix or ".png"
                if args.output:
                    if len(image_urls) == 1:
                        filename = args.output
                    else:
                        stem = Path(args.output).stem
                        filename = f"{stem}_{i+1}{ext}"
                else:
                    filename = f"generated_{i+1}{ext}"

                filepath = output_dir / filename
                download_image(url, str(filepath))
                print(f"Saved to: {filepath}", file=sys.stderr)

        # Also print URLs for reference
        for url in image_urls:
            print(url)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
