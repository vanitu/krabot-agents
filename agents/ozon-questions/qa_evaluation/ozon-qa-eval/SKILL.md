---
name: ozon-qa-eval
description: Benchmark skill for evaluating AI-generated Ozon buyer question answers against human answers. Scripts handle Ozon data extraction and file preparation; the Agent performs AI answer generation and scoring interactively.
---

# Ozon QA Evaluation Skill

This skill automates the data-heavy parts of a benchmark pipeline while leaving the LLM-driven steps to the Agent.

## Stages

### 1. Extract Ground Truth
```bash
python3 workspace/skills/ozon-qa-eval/scripts/extract_ground_truth.py --limit 20
```
Fetches `PROCESSED` questions and their human answers from Ozon, saving:
- `workspace/data/qa_benchmark/ground_truth_<timestamp>.json`

### 2. Prepare Contexts
```bash
python3 workspace/skills/ozon-qa-eval/scripts/prepare_all_contexts.py \
  --ground-truth workspace/data/qa_benchmark/ground_truth_<timestamp>.json
```
Runs `prepare_context.py` for each question, saving per-question context JSONs to:
- `workspace/data/qa_benchmark/contexts/<question_id>.json`

Skips already-existing context files so the run is resumable.

### 3. Build Answer Batch
```bash
python3 workspace/skills/ozon-qa-eval/scripts/build_answer_batch.py \
  --ground-truth workspace/data/qa_benchmark/ground_truth_<timestamp>.json
```
Creates a single work-list JSON:
- `workspace/data/qa_benchmark/answer_batch_<timestamp>.json`

Each entry contains `question_id`, `question_text`, `human_answer`, `agent_prompt`, and empty fields for `ai_answer`, `sufficiency_score`, `accuracy_score`, `reasoning`.

**Agent step:** The Agent reads the batch file, generates answers for each entry, and writes the completed results to `workspace/data/qa_benchmark/ai_results_<timestamp>.json`.

### 4. Build Eval Batch
```bash
python3 workspace/skills/ozon-qa-eval/scripts/build_eval_batch.py \
  --ground-truth workspace/data/qa_benchmark/ground_truth_<timestamp>.json \
  --ai-results workspace/data/qa_benchmark/ai_results_<timestamp>.json
```
Creates a CSV with columns:
- `question_id`, `question_text`, `human_answer`, `ai_answer`, `match_score`, `ai_accuracy_score`

Saved to:
- `workspace/data/qa_benchmark/eval_batch_<timestamp>.csv`

**Agent step:** The Agent reads the CSV, compares each pair, fills in `match_score` and `ai_accuracy_score`, and writes the final evaluated file to `workspace/data/qa_benchmark/final_eval_<timestamp>.csv`.

## Design Constraints
- **No LLM calls inside scripts** — they only use Ozon APIs and local files.
- **Resumable** — context preparation skips existing files; SKU cache avoids redundant Ozon product calls.
- **Sequential with delays** — respects Ozon API rate limits.
