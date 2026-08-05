---
name: ozon-question-answer
description: Skill for answering Ozon buyer questions. Supports both single-question context preparation and batch prompt building for up to 10 questions at once.
---

# Ozon Question Answer Skill

Prepares a complete context package for answering a buyer question on Ozon. The skill is split into two scripts:

1. **`prepare_context.py`** — fetches question info and product context from Ozon APIs, loads rules and example, and builds a detailed agent prompt. **Requires Ozon credentials.**
2. **`generate_answer.py`** — reads the prepared context and produces a draft report with placeholders for the final answer, scores, and reasoning. **Does not require Ozon credentials.**

## Prerequisites

- `OZON_CLIENT_ID` and `OZON_API_KEY` must be set for `prepare_context.py`
- `ozon-questions-api` and `ozon-product-info-api` skills must be present
- `{baseDir}/resources/answer_rules.md` and `{baseDir}/resources/answer_example.md` should exist

## Usage

### Step 1: Prepare context

```bash
python3 {baseDir}/scripts/prepare_context.py --question-id 019d635f-6903-73fa-ad3f-92852ea7d588
```

This prints a structured JSON to `stdout` and saves a copy to:
```
workspace/data/qa_contexts/context_<question_id>_<timestamp>.json
```

### Step 2: Generate answer scaffold

```bash
python3 {baseDir}/scripts/generate_answer.py --context-json workspace/data/qa_contexts/context_019d635f_20260414_185300.json
```

Or pipe directly:

```bash
python3 {baseDir}/scripts/prepare_context.py --question-id 019d635f-6903-73fa-ad3f-92852ea7d588 | python3 {baseDir}/scripts/generate_answer.py
```

### Output of `generate_answer.py`

The script prints a JSON object containing:

| Key | Description |
|-----|-------------|
| `question_info` | Metadata about the buyer question |
| `product_context` | Clean, human-readable product description and attributes |
| `rules` | Contents of `answer_rules.md` |
| `example` | Contents of `answer_example.md` |
| `agent_prompt` | Pre-formatted prompt ready for AI analysis |
| `context_path` | Path to the saved context JSON |
| `draft_report_path` | Path to the saved draft Markdown report |
| `answer` | Empty string (to be filled by AI or agent) |
| `sufficiency_score` | `null` (to be filled) |
| `accuracy_score` | `null` (to be filled) |
| `reasoning` | Empty string (to be filled) |

## Typical workflow

### Batch pipeline (recommended)

The batch orchestrator works in two phases because the Python script cannot invoke the Agent tool directly.

**Phase A — Prepare batch:**
```bash
python3 {baseDir}/scripts/answer_question.py prepare-batch
python3 {baseDir}/scripts/answer_question.py prepare-batch --max 5
python3 {baseDir}/scripts/answer_question.py prepare-batch --lookup-days 3
```

Defaults are read from `{baseDir}/settings.json` (created automatically if missing). CLI flags override settings.

This will:
1. Fetch up to `batch_size` (or `--max`) UNPROCESSED questions from Ozon API, going back `lookup_period_days` (or `--lookup-days`)
2. Build context for each question (with product cache)
3. Build a single batch prompt containing all questions
4. Save the batch prompt to `workspace/data/qa_prompts/batch_<timestamp>.txt`
5. Save batch metadata to `workspace/data/qa_prompts/batch_<timestamp>.json`
6. Print paths and instructions to stdout

**Phase B — Run subagent (parent agent only):**

The parent AI agent reads the saved prompt file and runs a subagent via the `Agent` tool with that prompt. The subagent must return a JSON array:
```json
[
  {"question_id": "...", "answer": "...", "sufficiency_score": 8, "accuracy_score": 9, "reasoning": "..."},
  ...
]
```

Save the subagent output to a file (e.g., `answers.json`).

**Phase C — Finalize batch:**
```bash
python3 {baseDir}/scripts/answer_question.py finalize-batch \
  --batch-metadata workspace/data/qa_prompts/batch_20260413_185300.json \
  --answers-json answers.json
```

This will:
1. Match each answer to the corresponding question by `question_id`
2. Filter out answers below `min_accuracy_score` / `min_sufficiency_score` thresholds
3. Generate individual final Markdown reports for passing answers only
4. Save a combined JSON report and an upload-ready payload to `workspace/data/ai_questions_answers.json`
5. Print a summary to stdout

### Phase D — Apply batch (upload to Ozon)

```bash
python3 {baseDir}/scripts/answer_question.py apply-batch \
  --batch-metadata workspace/data/qa_prompts/batch_20260413_185300.json \
  --answers-json workspace/data/qa_reports/batch_20260413_185300.json
```

This posts each filtered answer to Ozon via the `ozon-questions-api` skill.
In dry-run mode it prints a preview without making API calls.

### Single-question step-by-step (manual)

```bash
# 1. Prepare context
python3 {baseDir}/scripts/prepare_context.py --question-id 019d635f-6903-73fa-ad3f-92852ea7d588

# 2. Extract prompt
python3 {baseDir}/scripts/build_prompt.py --question-id 019d635f-6903-73fa-ad3f-92852ea7d588 > prompt.txt

# 3. Run subagent with prompt.txt (via Agent tool)

# 4. Save answer.json with keys: answer, sufficiency_score, accuracy_score, reasoning

# 5. Finalize report
python3 {baseDir}/scripts/finalize_answer.py \
  --question-id 019d635f-6903-73fa-ad3f-92852ea7d588 \
  --answer-json answer.json
```

## Output files

- Context JSON: `workspace/data/qa_contexts/context_<question_id>_<timestamp>.json`
- Draft report: `workspace/data/qa_reports/draft_<question_id>_<timestamp>.md`
- Final report: `workspace/data/qa_reports/final_<question_id>_<timestamp>.md`
- Batch prompt: `workspace/data/qa_prompts/batch_<timestamp>.txt`
- Batch metadata: `workspace/data/qa_prompts/batch_<timestamp>.json`
- Combined batch report: `workspace/data/qa_reports/batch_<timestamp>.json`
- Raw subagent output (on parse failure): `workspace/data/qa_reports/raw_<question_id>_<timestamp>.txt`
