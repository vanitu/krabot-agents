---
name: ozon-attributes-api
description: Work with Ozon Seller API description-category endpoints — get category tree, product attributes, and dictionary values.
---

# Ozon Attributes API Skill

Interact with the Ozon Seller API to retrieve product category trees, attributes, and dictionary values.

## Prerequisites

The following environment variables must be set (provided during onboarding):
- `OZON_CLIENT_ID` — your numeric seller identifier
- `OZON_API_KEY` — your Ozon Seller API key

## Usage

All commands are executed via the Python CLI script:

```bash
python3 {baseDir}/scripts/ozon_attributes.py <command> [options]
```

### Commands

#### `tree` — Get description category tree

```bash
python3 {baseDir}/scripts/ozon_attributes.py tree --language RU
```

| Option | Description |
|--------|-------------|
| `--language` | `DEFAULT` (default), `RU`, `EN`, `TR`, `ZH_HANS` |

#### `attributes` — Get attributes for category + type

```bash
python3 {baseDir}/scripts/ozon_attributes.py attributes \
  --description-category-id 17027492 \
  --type-id 970778135 \
  --language RU
```

| Option | Description |
|--------|-------------|
| `--description-category-id` | Category ID from the tree |
| `--type-id` | Type ID from the tree |
| `--language` | `DEFAULT` (default), `RU`, `EN`, `TR`, `ZH_HANS` |

#### `attribute-values` — Get dictionary values for an attribute

```bash
python3 {baseDir}/scripts/ozon_attributes.py attribute-values \
  --attribute-id 85 \
  --description-category-id 17054869 \
  --type-id 97311 \
  --limit 100 \
  --last-value-id 0 \
  --language RU
```

| Option | Description |
|--------|-------------|
| `--attribute-id` | Attribute ID from `attributes` |
| `--description-category-id` | Category ID |
| `--type-id` | Type ID |
| `--limit` | Page size (1–2000) |
| `--last-value-id` | Pagination cursor (default `0`) |
| `--language` | `DEFAULT` (default), `RU`, `EN`, `TR`, `ZH_HANS` |

#### `attribute-values-search` — Search dictionary values

```bash
python3 {baseDir}/scripts/ozon_attributes.py attribute-values-search \
  --attribute-id 85 \
  --description-category-id 17054869 \
  --type-id 97311 \
  --limit 20 \
  --value "Essence"
```

| Option | Description |
|--------|-------------|
| `--attribute-id` | Attribute ID |
| `--description-category-id` | Category ID |
| `--type-id` | Type ID |
| `--limit` | Page size (1–100) |
| `--value` | Search string (min 2 characters) |

## Typical workflow

1. **Get category tree**
   ```bash
   python3 {baseDir}/scripts/ozon_attributes.py tree --language RU
   ```

2. **Get attributes for a leaf category + type**
   ```bash
   python3 {baseDir}/scripts/ozon_attributes.py attributes \
     --description-category-id 200000933 \
     --type-id 93080
   ```

3. **Get dictionary values for an attribute**
   ```bash
   python3 {baseDir}/scripts/ozon_attributes.py attribute-values \
     --attribute-id 85 \
     --description-category-id 17054869 \
     --type-id 97311 \
     --limit 100
   ```

4. **Search dictionary values**
   ```bash
   python3 {baseDir}/scripts/ozon_attributes.py attribute-values-search \
     --attribute-id 85 \
     --description-category-id 17054869 \
     --type-id 97311 \
     --limit 20 \
     --value "Sun"
   ```

## Output

All commands print JSON to stdout. On API errors the script returns a JSON object with `error` and `status_code` fields.
