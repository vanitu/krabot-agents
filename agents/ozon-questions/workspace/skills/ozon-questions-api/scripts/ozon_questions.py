#!/usr/bin/env python3
"""Ozon Seller API — Questions skill CLI."""

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
    payload = {}
    if args.status:
        payload["status"] = args.status
    if args.date_from:
        payload["date_from"] = args.date_from
    if args.date_to:
        payload["date_to"] = args.date_to
    if args.last_id is not None:
        payload["last_id"] = args.last_id
    result = _post("/v1/question/list", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_info(args):
    result = _post("/v1/question/info", {"question_id": args.question_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_count(_args):
    result = _post("/v1/question/count", {})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_change_status(args):
    result = _post("/v1/question/change-status", {
        "question_ids": args.question_ids.split(","),
        "status": args.status,
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_answer_create(args):
    result = _post("/v1/question/answer/create", {
        "question_id": args.question_id,
        "sku": args.sku,
        "text": args.text,
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_answer_delete(args):
    result = _post("/v1/question/answer/delete", {
        "answer_id": args.answer_id,
        "sku": args.sku,
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_answer_list(args):
    payload = {"question_id": args.question_id, "sku": args.sku}
    if args.last_id is not None:
        payload["last_id"] = args.last_id
    result = _post("/v1/question/answer/list", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Ozon Questions API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="Get list of questions")
    p_list.add_argument("--status", choices=["ALL", "NEW", "VIEWED", "PROCESSED", "UNPROCESSED"], default="ALL")
    p_list.add_argument("--date-from", default="", help="Start date filter (ISO 8601)")
    p_list.add_argument("--date-to", default="", help="End date filter (ISO 8601)")
    p_list.add_argument("--last-id", default="", help="Pagination cursor")
    p_list.set_defaults(func=cmd_list)

    # info
    p_info = sub.add_parser("info", help="Get question info")
    p_info.add_argument("--question-id", required=True)
    p_info.set_defaults(func=cmd_info)

    # count
    p_count = sub.add_parser("count", help="Get question counts by status")
    p_count.set_defaults(func=cmd_count)

    # change-status
    p_cs = sub.add_parser("change-status", help="Change question status")
    p_cs.add_argument("--question-ids", required=True, help="Comma-separated question IDs")
    p_cs.add_argument("--status", required=True, choices=["NEW", "VIEWED", "PROCESSED"])
    p_cs.set_defaults(func=cmd_change_status)

    # answer-create
    p_ac = sub.add_parser("answer-create", help="Create an answer to a question")
    p_ac.add_argument("--question-id", required=True)
    p_ac.add_argument("--sku", required=True, type=int, help="Ozon SKU")
    p_ac.add_argument("--text", required=True, help="Answer text (2–3000 chars)")
    p_ac.set_defaults(func=cmd_answer_create)

    # answer-delete
    p_ad = sub.add_parser("answer-delete", help="Delete an answer")
    p_ad.add_argument("--answer-id", required=True)
    p_ad.add_argument("--sku", required=True, type=int)
    p_ad.set_defaults(func=cmd_answer_delete)

    # answer-list
    p_al = sub.add_parser("answer-list", help="List answers on a question")
    p_al.add_argument("--question-id", required=True)
    p_al.add_argument("--sku", required=True, type=int)
    p_al.add_argument("--last-id", default="")
    p_al.set_defaults(func=cmd_answer_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
