#!/usr/bin/env python3
"""
Download image from URL to file.
Usage: python3 download_image.py <url> <output_path>
Output: {"success": true, "path": "..."} or {"error": "..."}
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path


def download(url: str, output_path: str, timeout: int = 30) -> dict:
    """Download image with timeout."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Use urlopen with timeout instead of urlretrieve
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as response:
        with open(output_path, "wb") as f:
            f.write(response.read())

    return {"success": True, "path": str(path.resolve())}


def main():
    parser = argparse.ArgumentParser(description="Download image from URL")
    parser.add_argument("url", help="Image URL")
    parser.add_argument("output", help="Output file path")
    parser.add_argument(
        "--timeout", type=int, default=30, help="Download timeout in seconds"
    )
    args = parser.parse_args()

    try:
        result = download(args.url, args.output, args.timeout)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
