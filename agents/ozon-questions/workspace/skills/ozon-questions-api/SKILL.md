---
name: ozon-questions-api
description: Work with Ozon Seller API questions and answers endpoints — list, read, answer, delete answers, and change status of customer product questions.
---

# Ozon Questions API Skill

Interact with the Ozon Seller API to manage customer product questions and answers.

## Prerequisites

The following environment variables must be set (provided during onboarding):
- `OZON_CLIENT_ID` — your numeric seller identifier
- `OZON_API_KEY` — your Ozon Seller API key

## Usage

All commands are executed via the Python CLI script:

```bash
python3 {baseDir}/scripts/ozon_questions.py <command> [options]
```

### Commands

#### `list` — Get list of questions

```bash
python3 {baseDir}/scripts/ozon_questions.py list --status UNPROCESSED --last-id ""
```

| Option | Description |
|--------|-------------|
| `--status` | `ALL` (default), `NEW`, `VIEWED`, `PROCESSED`, `UNPROCESSED` |
| `--date-from` | Start date filter (ISO 8601) |
| `--date-to` | End date filter (ISO 8601) |
| `--last-id` | Pagination cursor, default `""` |

#### `info` — Get detailed question info

```bash
python3 {baseDir}/scripts/ozon_questions.py info --question-id "<uuid>"
```

#### `count` — Get question counts by status

```bash
python3 {baseDir}/scripts/ozon_questions.py count
```

Returns `all`, `new`, `processed`, `unprocessed`, and `viewed` counts.

#### `change-status` — Mark questions as processed/viewed/new

```bash
python3 {baseDir}/scripts/ozon_questions.py change-status --question-ids "id1,id2,id3" --status PROCESSED
```

#### `answer-create` — Post an answer to a question

```bash
python3 {baseDir}/scripts/ozon_questions.py answer-create \
  --question-id "<uuid>" \
  --sku 123456789 \
  --text "Да, конечно!"
```

| Option | Description |
|--------|-------------|
| `--question-id` | Target question UUID |
| `--sku` | Ozon SKU identifier |
| `--text` | Answer text (2–3000 characters) |

#### `answer-delete` — Delete an answer

```bash
python3 {baseDir}/scripts/ozon_questions.py answer-delete --answer-id "<uuid>" --sku 123456789
```

#### `answer-list` — List answers on a question

```bash
python3 {baseDir}/scripts/ozon_questions.py answer-list \
  --question-id "<uuid>" \
  --sku 123456789 \
  --last-id ""
```

## Typical workflow

1. **List unprocessed questions**
   ```bash
   python3 {baseDir}/scripts/ozon_questions.py list --status UNPROCESSED
   ```

2. **Get full question details** (optional)
   ```bash
   python3 {baseDir}/scripts/ozon_questions.py info --question-id "<question_id>"
   ```

3. **Post an answer**
   ```bash
   python3 {baseDir}/scripts/ozon_questions.py answer-create \
     --question-id "<question_id>" \
     --sku 123456789 \
     --text "Спасибо за вопрос! Да, данная модель доступна в нескольких цветах."
   ```

4. **Mark as processed**
   ```bash
   python3 {baseDir}/scripts/ozon_questions.py change-status \
     --question-ids "<question_id>" --status PROCESSED
   ```

## Output

All commands print JSON to stdout. On API errors the script returns a JSON object with `error` and `status_code` fields.
