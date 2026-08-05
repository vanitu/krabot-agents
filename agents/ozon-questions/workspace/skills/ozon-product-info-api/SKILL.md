---
name: ozon-product-info-api
description: Work with Ozon Seller API product info endpoints — get product details, attributes, description, and aggregated full info.
---

# Ozon Product Info API Skill

Interact with the Ozon Seller API to retrieve product details, attributes, and descriptions.

## Prerequisites

The following environment variables must be set (provided during onboarding):
- `OZON_CLIENT_ID` — your numeric seller identifier
- `OZON_API_KEY` — your Ozon Seller API key

## Usage

All commands are executed via the Python CLI script:

```bash
python3 {baseDir}/scripts/ozon_product_info.py <command> [options]
```

### Commands

#### `info-list` — Get product info by identifiers

```bash
python3 {baseDir}/scripts/ozon_product_info.py info-list --sku "123456789"
```

| Option | Description |
|--------|-------------|
| `--offer-ids` | Comma-separated offer IDs (артикулы) |
| `--product-ids` | Comma-separated product IDs |
| `--sku` | Comma-separated SKUs |

> At least one identifier list is required.

#### `attributes` — Get product attributes

```bash
python3 {baseDir}/scripts/ozon_product_info.py attributes \
  --offer-id "test123" \
  --limit 100 \
  --sort-by offer_id \
  --sort-dir asc
```

| Option | Description |
|--------|-------------|
| `--offer-id` | Comma-separated offer IDs |
| `--product-id` | Comma-separated product IDs |
| `--sku` | Comma-separated SKUs |
| `--visibility` | Visibility filter, default `ALL` |
| `--limit` | Page size (1–1000) |
| `--last-id` | Pagination cursor |
| `--sort-by` | `sku`, `offer_id`, `id`, `title` |
| `--sort-dir` | `asc` or `desc` |

#### `description` — Get product description

```bash
python3 {baseDir}/scripts/ozon_product_info.py description --offer-id "test123"
```

| Option | Description |
|--------|-------------|
| `--offer-id` | Required offer ID |
| `--product-id` | Optional product ID |

#### `full-info` — Get aggregated full product info

Convenience command that calls `info-list`, `attributes`, and `description` in one go and returns a merged result.

```bash
python3 {baseDir}/scripts/ozon_product_info.py full-info --sku "123456789"
```

| Option | Description |
|--------|-------------|
| `--offer-id` | Offer ID |
| `--product-id` | Product ID |
| `--sku` | SKU |

> Exactly one of `--offer-id`, `--product-id`, or `--sku` is required.

**Output structure:**
```json
{
  "info": { /* product from info-list */ },
  "attributes": { /* result from attributes */ },
  "description": { /* result from description */ }
}
```

## Typical workflow

1. **Get basic product info**
   ```bash
   python3 {baseDir}/scripts/ozon_product_info.py info-list --sku "123456789"
   ```

2. **Get product attributes**
   ```bash
   python3 {baseDir}/scripts/ozon_product_info.py attributes --offer-id "test123" --limit 100
   ```

3. **Get product description**
   ```bash
   python3 {baseDir}/scripts/ozon_product_info.py description --offer-id "test123"
   ```

4. **Get everything at once**
   ```bash
   python3 {baseDir}/scripts/ozon_product_info.py full-info --offer-id "test123"
   ```

## Output

All commands print JSON to stdout. On API errors the script returns a JSON object with `error` and `status_code` fields.
