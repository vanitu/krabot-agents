#!/usr/bin/env python3
"""Ozon Seller API — Product Info skill CLI."""

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


def cmd_info_list(args):
    payload = {}
    if args.offer_ids:
        payload["offer_id"] = [s.strip() for s in args.offer_ids.split(",") if s.strip()]
    if args.product_ids:
        payload["product_id"] = [s.strip() for s in args.product_ids.split(",") if s.strip()]
    if args.sku:
        payload["sku"] = [s.strip() for s in args.sku.split(",") if s.strip()]
    if not payload:
        print(json.dumps({"error": "At least one of --offer-ids, --product-ids, or --sku is required"}, ensure_ascii=False))
        sys.exit(1)
    result = _post("/v3/product/info/list", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_attributes(args):
    filter_payload = {}
    if args.offer_id:
        filter_payload["offer_id"] = [s.strip() for s in args.offer_id.split(",") if s.strip()]
    if args.product_id:
        filter_payload["product_id"] = [s.strip() for s in args.product_id.split(",") if s.strip()]
    if args.sku:
        filter_payload["sku"] = [s.strip() for s in args.sku.split(",") if s.strip()]
    if args.visibility:
        filter_payload["visibility"] = args.visibility

    payload = {"filter": filter_payload}
    if args.limit is not None:
        payload["limit"] = args.limit
    if args.last_id is not None:
        payload["last_id"] = args.last_id
    if args.sort_by:
        payload["sort_by"] = args.sort_by
    if args.sort_dir:
        payload["sort_dir"] = args.sort_dir

    result = _post("/v4/product/info/attributes", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_description(args):
    payload = {"offer_id": args.offer_id}
    if args.product_id is not None:
        payload["product_id"] = args.product_id
    result = _post("/v1/product/info/description", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _fetch_category_attributes(category_id, type_id, language="DEFAULT"):
    """Fetch attribute names for a category+type. Returns {attribute_id: name}."""
    print(f"[INFO] Fetching category attributes for category_id={category_id}, type_id={type_id}, lang={language}", file=sys.stderr)
    payload = {"description_category_id": category_id, "type_id": type_id}
    if language:
        payload["language"] = language
    result = _post("/v1/description-category/attribute", payload)
    mapping = {}
    if "error" in result:
        print(f"[WARN] Failed to fetch category attributes: {result['error']}", file=sys.stderr)
        return mapping
    for attr in result.get("result", []):
        mapping[attr.get("id")] = attr.get("name", "")
    print(f"[INFO] Loaded {len(mapping)} attribute name(s)", file=sys.stderr)
    return mapping


def _fetch_category_attribute_values(category_id, type_id, attribute_id, language="DEFAULT"):
    """Fetch dictionary values for an attribute. Returns {dictionary_value_id: value}."""
    print(f"[INFO] Fetching dictionary values for attribute_id={attribute_id}, category_id={category_id}, type_id={type_id}, lang={language}", file=sys.stderr)
    values_map = {}
    last_value_id = 0
    pages = 0
    while True:
        payload = {
            "attribute_id": attribute_id,
            "description_category_id": category_id,
            "type_id": type_id,
            "limit": 2000,
            "last_value_id": last_value_id,
        }
        if language:
            payload["language"] = language
        result = _post("/v1/description-category/attribute/values", payload)
        pages += 1
        if "error" in result:
            print(f"[WARN] Failed to fetch dictionary values for attribute_id={attribute_id}: {result['error']}", file=sys.stderr)
            break
        for entry in result.get("result", []):
            values_map[entry.get("id")] = entry.get("value", "")
        if not result.get("has_next"):
            break
        # Safety break: if no progress, stop
        if result.get("result"):
            last_value_id = result["result"][-1].get("id", last_value_id)
        else:
            break
    print(f"[INFO] Loaded {len(values_map)} dictionary value(s) for attribute_id={attribute_id} in {pages} page(s)", file=sys.stderr)
    return values_map


def _enrich_attributes(attr_result, language="DEFAULT"):
    """Build an enriched attributes list from raw v4/product/info/attributes result."""
    items = attr_result.get("result", [])
    if not items:
        print("[INFO] No attribute items to enrich", file=sys.stderr)
        return []
    product = items[0]
    category_id = product.get("description_category_id")
    type_id = product.get("type_id")
    raw_attrs = product.get("attributes", [])
    if not category_id or not type_id or not raw_attrs:
        print(f"[INFO] Missing category_id={category_id}, type_id={type_id}, or raw_attrs count={len(raw_attrs)} — skipping enrichment", file=sys.stderr)
        return []

    print(f"[INFO] Enriching {len(raw_attrs)} attribute(s) for category_id={category_id}, type_id={type_id}", file=sys.stderr)
    name_map = _fetch_category_attributes(category_id, type_id, language)
    # Cache value maps per attribute_id
    values_cache = {}
    dict_lookup_count = 0
    cached_lookup_count = 0

    enriched = []
    for attr in raw_attrs:
        attr_id = attr.get("id")
        attr_name = name_map.get(attr_id, "")
        enriched_values = []
        needs_values = False
        for v in attr.get("values", []):
            dvid = v.get("dictionary_value_id", 0)
            raw = v.get("value", "")
            resolved = raw
            if dvid and dvid > 0:
                needs_values = True
            enriched_values.append({
                "dictionary_value_id": dvid,
                "raw_value": raw,
                "resolved_value": resolved,
            })

        if needs_values:
            if attr_id not in values_cache:
                values_cache[attr_id] = _fetch_category_attribute_values(category_id, type_id, attr_id, language)
                dict_lookup_count += 1
            else:
                cached_lookup_count += 1
                print(f"[INFO] Using cached dictionary values for attribute_id={attr_id}", file=sys.stderr)
            vmap = values_cache[attr_id]
            for ev in enriched_values:
                dvid = ev["dictionary_value_id"]
                if dvid and dvid > 0 and dvid in vmap:
                    ev["resolved_value"] = vmap[dvid]

        enriched.append({
            "attribute_id": attr_id,
            "attribute_name": attr_name,
            "values": enriched_values,
        })
    print(f"[INFO] Enrichment complete: {dict_lookup_count} dictionary fetch(es), {cached_lookup_count} cache hit(s), {len(enriched)} attribute(s) total", file=sys.stderr)
    return enriched


def cmd_full_info(args):
    # Determine identifier
    identifier_type = None
    identifier_value = None
    if args.offer_id:
        identifier_type = "offer_id"
        identifier_value = args.offer_id
    elif args.product_id:
        identifier_type = "product_id"
        identifier_value = str(args.product_id)
    elif args.sku:
        identifier_type = "sku"
        identifier_value = str(args.sku)
    else:
        print(json.dumps({"error": "One of --offer-id, --product-id, or --sku is required"}, ensure_ascii=False))
        sys.exit(1)

    print(f"[INFO] full-info started with {identifier_type}={identifier_value}", file=sys.stderr)

    # Step 1: info-list
    info_payload = {identifier_type: [identifier_value]}
    print(f"[INFO] Calling info-list...", file=sys.stderr)
    info_result = _post("/v3/product/info/list", info_payload)
    if "error" in info_result:
        print(f"[ERROR] info-list failed: {info_result['error']}", file=sys.stderr)
        print(json.dumps({"error": info_result["error"], "stage": "info-list"}, ensure_ascii=False, indent=2))
        return
    items = info_result.get("items", [])
    if not items:
        print("[WARN] info-list returned no items", file=sys.stderr)
        print(json.dumps({"error": "Product not found", "stage": "info-list"}, ensure_ascii=False, indent=2))
        return
    item = items[0]
    offer_id = item.get("offer_id")
    product_id = item.get("id")
    print(f"[INFO] info-list OK: offer_id={offer_id}, product_id={product_id}", file=sys.stderr)

    # Step 2: attributes (use offer_id if available, else product_id)
    attr_filter = {}
    if offer_id:
        attr_filter["offer_id"] = [offer_id]
    elif product_id:
        attr_filter["product_id"] = [str(product_id)]
    print(f"[INFO] Calling attributes...", file=sys.stderr)
    attr_result = _post("/v4/product/info/attributes", {"filter": attr_filter, "limit": 1})
    if "error" in attr_result:
        print(f"[WARN] attributes failed: {attr_result['error']}", file=sys.stderr)
    else:
        print(f"[INFO] attributes OK: {len(attr_result.get('result', []))} product(s)", file=sys.stderr)

    # Step 3: description
    desc_payload = {"offer_id": offer_id} if offer_id else {"product_id": product_id}
    print(f"[INFO] Calling description...", file=sys.stderr)
    desc_result = _post("/v1/product/info/description", desc_payload)
    if "error" in desc_result:
        print(f"[WARN] description failed: {desc_result['error']}", file=sys.stderr)
    else:
        print("[INFO] description OK", file=sys.stderr)

    # Step 4: enrich attributes with human-readable names and dictionary values
    print("[INFO] Starting attribute enrichment...", file=sys.stderr)
    attributes_enriched = _enrich_attributes(attr_result, language="DEFAULT")

    merged = {
        "info": item,
        "attributes": attr_result,
        "attributes_enriched": attributes_enriched,
        "description": desc_result,
    }
    print(f"[INFO] full-info complete. Outputting merged JSON.", file=sys.stderr)
    print(json.dumps(merged, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Ozon Product Info API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # info-list
    p_il = sub.add_parser("info-list", help="Get product info list by identifiers")
    p_il.add_argument("--offer-ids", default="", help="Comma-separated offer IDs")
    p_il.add_argument("--product-ids", default="", help="Comma-separated product IDs")
    p_il.add_argument("--sku", default="", help="Comma-separated SKUs")
    p_il.set_defaults(func=cmd_info_list)

    # attributes
    p_attr = sub.add_parser("attributes", help="Get product attributes")
    p_attr.add_argument("--offer-id", default="", help="Comma-separated offer IDs")
    p_attr.add_argument("--product-id", default="", help="Comma-separated product IDs")
    p_attr.add_argument("--sku", default="", help="Comma-separated SKUs")
    p_attr.add_argument("--visibility", default="ALL", help="Visibility filter")
    p_attr.add_argument("--limit", type=int, help="Page size (1–1000)")
    p_attr.add_argument("--last-id", default="", help="Pagination cursor")
    p_attr.add_argument("--sort-by", choices=["sku", "offer_id", "id", "title"], help="Sort field")
    p_attr.add_argument("--sort-dir", choices=["asc", "desc"], help="Sort direction")
    p_attr.set_defaults(func=cmd_attributes)

    # description
    p_desc = sub.add_parser("description", help="Get product description")
    p_desc.add_argument("--offer-id", required=True, help="Offer ID")
    p_desc.add_argument("--product-id", type=int, help="Optional product ID")
    p_desc.set_defaults(func=cmd_description)

    # full-info
    p_full = sub.add_parser("full-info", help="Get full product info (info + attributes + description)")
    p_full.add_argument("--offer-id", help="Offer ID")
    p_full.add_argument("--product-id", type=int, help="Product ID")
    p_full.add_argument("--sku", help="SKU")
    p_full.set_defaults(func=cmd_full_info)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
