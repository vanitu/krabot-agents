---
name: ozon-reviews-skill
description: Work with Ozon Seller API reviews endpoints — list, read, comment on, and change status of product reviews.
---

# Ozon Reviews Skill

Interact with the Ozon Seller API to manage customer reviews and comments.

## Prerequisites

The following environment variables must be set (provided during onboarding):
- `OZON_CLIENT_ID` — your numeric seller identifier
- `OZON_API_KEY` — your Ozon Seller API key

## Usage

All commands are executed via the Python CLI script:

```bash
python3 {baseDir}/scripts/ozon_reviews.py <command> [options]
```

### Commands

#### `list` — Get list of reviews

```bash
python3 {baseDir}/scripts/ozon_reviews.py list --status UNPROCESSED --limit 50 --sort-dir ASC --last-id ""
```

| Option | Description |
|--------|-------------|
| `--status` | `ALL` (default), `UNPROCESSED`, `PROCESSED` |
| `--limit` | 20–100, default 20 |
| `--sort-dir` | `ASC` (default) or `DESC` |
| `--last-id` | Pagination cursor, default `""` |

#### `info` — Get detailed review info

```bash
python3 {baseDir}/scripts/ozon_reviews.py info --review-id "<uuid>"
```

#### `count` — Get review counts by status

```bash
python3 {baseDir}/scripts/ozon_reviews.py count
```

Returns `total`, `processed`, and `unprocessed` counts.

#### `change-status` — Mark reviews as processed/unprocessed

```bash
python3 {baseDir}/scripts/ozon_reviews.py change-status --review-ids "id1,id2,id3" --status PROCESSED
```

#### `comment-create` — Reply to a review

```bash
python3 {baseDir}/scripts/ozon_reviews.py comment-create \
  --review-id "<uuid>" \
  --text "Спасибо за отзыв!" \
  --mark-processed
```

| Option | Description |
|--------|-------------|
| `--review-id` | Target review UUID |
| `--text` | Comment text |
| `--mark-processed` | Also set review status to `PROCESSED` |
| `--parent-comment-id` | (optional) Reply to a specific comment |

#### `comment-delete` — Delete a comment

```bash
python3 {baseDir}/scripts/ozon_reviews.py comment-delete --comment-id "<uuid>"
```

#### `comment-list` — List comments on a review

```bash
python3 {baseDir}/scripts/ozon_reviews.py comment-list --review-id "<uuid>" --limit 20 --offset 0 --sort-dir ASC
```

## Typical workflow

1. **List unprocessed reviews**
   ```bash
   python3 {baseDir}/scripts/ozon_reviews.py list --status UNPROCESSED --limit 50
   ```

2. **Get full review details** (optional)
   ```bash
   python3 {baseDir}/scripts/ozon_reviews.py info --review-id "<review_id>"
   ```

3. **Post a reply**
   ```bash
   python3 {baseDir}/scripts/ozon_reviews.py comment-create \
     --review-id "<review_id>" \
     --text "Благодарим за обратную связь!" \
     --mark-processed
   ```

## Output

All commands print JSON to stdout. On API errors the script returns a JSON object with `error` and `status_code` fields.
