#!/usr/bin/env python3
"""Ozon Seller API — Description Category / Attributes skill CLI."""

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


def cmd_tree(args):
    payload = {}
    if args.language:
        payload["language"] = args.language
    result = _post("/v1/description-category/tree", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_attributes(args):
    payload = {
        "description_category_id": args.description_category_id,
        "type_id": args.type_id,
    }
    if args.language:
        payload["language"] = args.language
    result = _post("/v1/description-category/attribute", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_attribute_values(args):
    payload = {
        "attribute_id": args.attribute_id,
        "description_category_id": args.description_category_id,
        "type_id": args.type_id,
        "limit": args.limit,
    }
    if args.last_value_id is not None:
        payload["last_value_id"] = args.last_value_id
    if args.language:
        payload["language"] = args.language
    result = _post("/v1/description-category/attribute/values", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_attribute_values_search(args):
    payload = {
        "attribute_id": args.attribute_id,
        "description_category_id": args.description_category_id,
        "type_id": args.type_id,
        "limit": args.limit,
        "value": args.value,
    }
    result = _post("/v1/description-category/attribute/values/search", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Ozon Description Category / Attributes API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # tree
    p_tree = sub.add_parser("tree", help="Get description category tree")
    p_tree.add_argument("--language", default="DEFAULT", choices=["DEFAULT", "RU", "EN", "TR", "ZH_HANS"])
    p_tree.set_defaults(func=cmd_tree)

    # attributes
    p_attr = sub.add_parser("attributes", help="Get attributes for category + type")
    p_attr.add_argument("--description-category-id", required=True, type=int)
    p_attr.add_argument("--type-id", required=True, type=int)
    p_attr.add_argument("--language", default="DEFAULT", choices=["DEFAULT", "RU", "EN", "TR", "ZH_HANS"])
    p_attr.set_defaults(func=cmd_attributes)

    # attribute-values
    p_av = sub.add_parser("attribute-values", help="Get dictionary values for an attribute")
    p_av.add_argument("--attribute-id", required=True, type=int)
    p_av.add_argument("--description-category-id", required=True, type=int)
    p_av.add_argument("--type-id", required=True, type=int)
    p_av.add_argument("--limit", required=True, type=int)
    p_av.add_argument("--last-value-id", type=int, default=0)
    p_av.add_argument("--language", default="DEFAULT", choices=["DEFAULT", "RU", "EN", "TR", "ZH_HANS"])
    p_av.set_defaults(func=cmd_attribute_values)

    # attribute-values-search
    p_avs = sub.add_parser("attribute-values-search", help="Search dictionary values for an attribute")
    p_avs.add_argument("--attribute-id", required=True, type=int)
    p_avs.add_argument("--description-category-id", required=True, type=int)
    p_avs.add_argument("--type-id", required=True, type=int)
    p_avs.add_argument("--limit", required=True, type=int)
    p_avs.add_argument("--value", required=True, help="Search string (min 2 chars)")
    p_avs.set_defaults(func=cmd_attribute_values_search)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
