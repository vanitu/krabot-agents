---
name: ozon-reviews-workflow
description: Orchestrate the Ozon review processing pipeline — classify reviews, post template replies, prepare AI batches, mark processed, generate human-friendly reports, and auto-cleanup.
---

# Ozon Reviews Workflow

Automated business-logic layer for handling Ozon seller reviews end-to-end.

## What it does

1. Fetches up to 200 newest unprocessed reviews via `ozon-reviews-api` (sorted by newest first, limited to the last 7 days).
2. Classifies reviews into 4 groups:
   - **A:** 4–5 stars, **empty user text**, no photos/videos → random generic template reply
   - **B:** 4–5 stars, **empty user text**, has photos/videos → random photo-aware template reply
   - **C:** 4–5 stars, **contains user-written text** → prepare batch for AI-generated personalized reply
   - **D:** All other reviews (rating < 4) → skip
3. Skips any 4–5 star reviews that **already have an official seller reply**.
4. Posts template replies for groups A and B and marks them `PROCESSED`.
5. Saves intermediate state to `data/stage1_results.json`.
6. If group C exists, writes `data/pending_ai_reviews.json` and waits for AI replies.
7. After AI replies are applied, generates a single final Markdown report and automatically deletes all temporary JSON files.

## Two-stage flow

### Stage 1 — Templates

```bash
python3 {baseDir}/scripts/process_reviews.py
```

After this run:
- Groups A and B are fully handled and marked processed.
- Group C is saved to `data/pending_ai_reviews.json` waiting for AI replies.
- Intermediate state is stored in `data/stage1_results.json`.
- **If there is no group C**, the final report is created immediately and `stage1_results.json` is removed.

### Stage 2 — AI replies

The agent reads `data/pending_ai_reviews.json`, generates personalized replies respecting `resources/company_rules.md`, and saves them to:

```json
{
  "answers": [
    {"review_id": "...", "text": "..."},
    {"review_id": "...", "text": "..."}
  ]
}
```

Then apply them:

```bash
python3 {baseDir}/scripts/process_reviews.py --apply-ai data/ai_reviews_answers.json
```

This posts the AI replies, marks group C as processed, generates the **single final report** in `data/report_YYYYMMDD_HHMMSS.md`, and cleans up:
- `data/stage1_results.json`
- `data/pending_ai_reviews.json`
- `data/ai_reviews_answers.json`

### Dry-run mode

To preview what would happen without posting real comments:

```bash
python3 {baseDir}/scripts/process_reviews.py --dry-run
python3 {baseDir}/scripts/process_reviews.py --dry-run --apply-ai data/ai_reviews_answers.json
```

In dry-run, no files are deleted and no real API changes are made.

## Files used

| File | Purpose |
|------|---------|
| `../../resources/generic_templates.json` | Template pool for group A |
| `../../resources/photos_templates.json` | Template pool for group B |
| `../../resources/company_rules.md` | Rules for AI-generated replies |
| `../../data/stage1_results.json` | Intermediate state between stages (auto-created, auto-removed) |
| `../../data/pending_ai_reviews.json` | Batch prepared for AI (auto-created, auto-removed) |
| `../../data/ai_reviews_answers.json` | AI-generated answers (agent-created, auto-removed) |
| `../../data/report_*.md` | Final summary reports (persisted) |

## Output

Only final reports remain in `workspace/data/`. All temporary JSON files are cleaned up automatically.
