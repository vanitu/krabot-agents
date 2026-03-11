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


def download(url: str, output_path: str) -> dict:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, output_path)
    return {"success": True, "path": output_path}


def main():
    parser = argparse.ArgumentParser(description="Download image from URL")
    parser.add_argument("url", help="Image URL")
    parser.add_argument("output", help="Output file path")
    args = parser.parse_args()

    try:
        result = download(args.url, args.output)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
