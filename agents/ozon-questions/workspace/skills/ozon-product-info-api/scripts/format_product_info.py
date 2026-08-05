#!/usr/bin/env python3
"""Format full product info into clean, AI-friendly text.

Usage:
    python3 format_product_info.py --sku 3263580114
    python3 format_product_info.py --offer-id 8806164178058
    python3 format_product_info.py --product-id 3266916011
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("ozon_product_info.py")

# Attributes that are noisy for AI question answering
NOISY_ATTRIBUTE_NAMES = {
    "ТН ВЭД коды ЕАЭС",
    "Код продавца",
    "Название модели (для объединения в одну карточки)",
    "Название модели (для объединения в одну карточку)",
    "#Хештеги",
    "Объединить в похожие товары",
    "Единиц в одном товаре",
}


def run_full_info(identifier_type, identifier_value):
    cmd = [
        sys.executable,
        str(SCRIPT),
        "full-info",
        f"--{identifier_type}",
        str(identifier_value),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] full-info failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON from full-info:\n{result.stdout}\n{exc}", file=sys.stderr)
        sys.exit(1)


def clean_description(text):
    if not text:
        return ""
    # Minimal HTML tag stripping for readability
    replacements = [
        ("<br/>", "\n"),
        ("<br>", "\n"),
        ("<ul>", ""),
        ("</ul>", ""),
        ("<li>", "- "),
        ("</li>", ""),
        ("<p>", ""),
        ("</p>", ""),
        ("<b>", "**"),
        ("</b>", "**"),
        ("<strong>", "**"),
        ("</strong>", "**"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text.strip()


def format_product(data):
    info = data.get("info", {})
    description_data = data.get("description", {})
    enriched = data.get("attributes_enriched", [])

    lines = []

    # Title
    name = info.get("name", "Неизвестный товар")
    lines.append(f"# {name}")
    lines.append("")

    # Basic info
    sku = info.get("sku")
    offer_id = info.get("offer_id")
    product_id = info.get("id")
    price = info.get("price", "")
    currency = info.get("currency_code", "")
    if sku:
        lines.append(f"- **SKU:** {sku}")
    if offer_id:
        lines.append(f"- **Артикул:** {offer_id}")
    if product_id:
        lines.append(f"- **Ссылка на товар:** https://www.ozon.ru/product/{product_id}")
    if price:
        lines.append(f"- **Цена:** {price} {currency}".strip())

    # Stocks
    stocks = info.get("stocks", {}).get("stocks", [])
    if stocks:
        stock_parts = []
        for s in stocks:
            src = s.get("source", "").upper()
            present = s.get("present", 0)
            stock_parts.append(f"{src}: {present}")
        lines.append(f"- **Наличие:** {', '.join(stock_parts)}")

    # Images
    images = info.get("images", [])
    primary = info.get("primary_image", [])
    all_images = []
    if primary and isinstance(primary, list):
        all_images.extend(primary)
    all_images.extend([img for img in images if img not in all_images])
    if all_images:
        lines.append("- **Изображения:**")
        for img in all_images[:5]:
            lines.append(f"  - {img}")

    lines.append("")

    # Description
    desc = description_data.get("result", {}).get("description", "")
    if desc:
        lines.append("## Описание")
        lines.append(clean_description(desc))
        lines.append("")

    # Attributes
    if enriched:
        lines.append("## Характеристики")
        lines.append("")
        for attr in enriched:
            attr_name = attr.get("attribute_name", "").strip()
            if not attr_name:
                continue
            if attr_name in NOISY_ATTRIBUTE_NAMES:
                continue
            vals = attr.get("values", [])
            if not vals:
                continue
            parts = [v.get("resolved_value") or v.get("raw_value", "") for v in vals]
            parts = [p for p in parts if p]
            if not parts:
                continue
            joined = ", ".join(parts)
            lines.append(f"- **{attr_name}:** {joined}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Format Ozon product info for AI prompts")
    parser.add_argument("--sku", help="Ozon SKU")
    parser.add_argument("--offer-id", help="Offer ID (артикул)")
    parser.add_argument("--product-id", help="Product ID")
    args = parser.parse_args()

    identifier_type = None
    identifier_value = None
    if args.sku:
        identifier_type = "sku"
        identifier_value = args.sku
    elif args.offer_id:
        identifier_type = "offer_id"
        identifier_value = args.offer_id
    elif args.product_id:
        identifier_type = "product_id"
        identifier_value = args.product_id
    else:
        print("Error: One of --sku, --offer-id, or --product-id is required.", file=sys.stderr)
        sys.exit(1)

    data = run_full_info(identifier_type, identifier_value)
    print(format_product(data))


if __name__ == "__main__":
    main()
