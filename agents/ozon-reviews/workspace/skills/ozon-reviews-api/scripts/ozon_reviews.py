#!/usr/bin/env python3
"""Ozon Seller API — Reviews skill CLI."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = "https://api-seller.ozon.ru"


def _headers():
    client_id = os.environ.get("OZON_CLIENT_ID")
    api_key = os.environ.get("OZON_API_KEY")
    if not client_id or not api_key:
        print(json.dumps({"error": "Missing OZON_CLIENT_ID or OZON_API_KEY environment variables"}, ensure_ascii=False))
        sys.exit(1)
    return {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }


def _post(path, payload):
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_headers(), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            if not body:
                return {}
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            err = json.loads(body)
        except Exception:
            err = {"error": body or str(exc)}
        return {"error": err, "status_code": exc.code}
    except Exception as exc:
        return {"error": str(exc)}


def cmd_list(args):
    payload = {"limit": args.limit, "sort_dir": args.sort_dir}
    if args.status:
        payload["status"] = args.status
    if args.last_id is not None:
        payload["last_id"] = args.last_id
    result = _post("/v1/review/list", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_info(args):
    result = _post("/v1/review/info", {"review_id": args.review_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_count(_args):
    result = _post("/v1/review/count", {})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_change_status(args):
    result = _post("/v1/review/change-status", {
        "review_ids": args.review_ids.split(","),
        "status": args.status,
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_comment_create(args):
    payload = {"review_id": args.review_id, "text": args.text}
    if args.mark_processed:
        payload["mark_review_as_processed"] = True
    if args.parent_comment_id:
        payload["parent_comment_id"] = args.parent_comment_id
    result = _post("/v1/review/comment/create", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_comment_delete(args):
    result = _post("/v1/review/comment/delete", {"comment_id": args.comment_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_comment_list(args):
    payload = {"review_id": args.review_id, "limit": args.limit}
    if args.offset is not None:
        payload["offset"] = args.offset
    if args.sort_dir:
        payload["sort_dir"] = args.sort_dir
    result = _post("/v1/review/comment/list", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Ozon Reviews API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="Get list of reviews")
    p_list.add_argument("--status", choices=["ALL", "UNPROCESSED", "PROCESSED"], default="ALL")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.add_argument("--sort-dir", choices=["ASC", "DESC"], default="ASC")
    p_list.add_argument("--last-id", default="")
    p_list.set_defaults(func=cmd_list)

    # info
    p_info = sub.add_parser("info", help="Get review info")
    p_info.add_argument("--review-id", required=True)
    p_info.set_defaults(func=cmd_info)

    # count
    p_count = sub.add_parser("count", help="Get review counts by status")
    p_count.set_defaults(func=cmd_count)

    # change-status
    p_cs = sub.add_parser("change-status", help="Change review status")
    p_cs.add_argument("--review-ids", required=True, help="Comma-separated review IDs")
    p_cs.add_argument("--status", required=True, choices=["PROCESSED", "UNPROCESSED"])
    p_cs.set_defaults(func=cmd_change_status)

    # comment-create
    p_cc = sub.add_parser("comment-create", help="Create a comment on a review")
    p_cc.add_argument("--review-id", required=True)
    p_cc.add_argument("--text", required=True)
    p_cc.add_argument("--mark-processed", action="store_true", help="Mark review as processed")
    p_cc.add_argument("--parent-comment-id", default="")
    p_cc.set_defaults(func=cmd_comment_create)

    # comment-delete
    p_cd = sub.add_parser("comment-delete", help="Delete a comment")
    p_cd.add_argument("--comment-id", required=True)
    p_cd.set_defaults(func=cmd_comment_delete)

    # comment-list
    p_cl = sub.add_parser("comment-list", help="List comments on a review")
    p_cl.add_argument("--review-id", required=True)
    p_cl.add_argument("--limit", type=int, default=20)
    p_cl.add_argument("--offset", type=int, default=0)
    p_cl.add_argument("--sort-dir", choices=["ASC", "DESC"], default="ASC")
    p_cl.set_defaults(func=cmd_comment_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
