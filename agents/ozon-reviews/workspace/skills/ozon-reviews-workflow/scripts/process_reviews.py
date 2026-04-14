#!/usr/bin/env python3
"""Ozon Reviews Workflow Orchestrator.

Stages:
  1. Default run: fetches unprocessed reviews, posts template replies for A/B,
     prepares AI batch for C, saves intermediate state.
  2. --apply-ai: posts AI-generated replies for C, generates final report, cleans up.
"""

import argparse
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
API_SCRIPT = WORKSPACE / "skills" / "ozon-reviews-api" / "scripts" / "ozon_reviews.py"
RESOURCES = WORKSPACE / "resources"
DATA_DIR = WORKSPACE / "data"

GENERIC_TEMPLATES = RESOURCES / "generic_templates.json"
PHOTOS_TEMPLATES = RESOURCES / "photos_templates.json"
COMPANY_RULES = RESOURCES / "company_rules.md"
STAGE1_PATH = DATA_DIR / "stage1_results.json"
PENDING_AI_PATH = DATA_DIR / "pending_ai_reviews.json"

DRY_RUN = False


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def run_api(*args):
    cmd = [sys.executable, str(API_SCRIPT), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] API command failed: {' '.join(args)}")
        print(f"stderr: {result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON from API: {result.stdout}", file=sys.stderr)
        return None


def fetch_unprocessed_reviews(max_reviews=200, max_age_days=7):
    reviews = []
    last_id = ""
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    while len(reviews) < max_reviews:
        limit = min(100, max_reviews - len(reviews))
        data = run_api("list", "--status", "UNPROCESSED", "--limit", str(limit), "--sort-dir", "DESC", "--last-id", last_id)
        if data is None or "error" in data:
            print(f"[ERROR] Failed to fetch reviews: {data}", file=sys.stderr)
            break
        batch = data.get("reviews", [])
        if not batch:
            break
        for r in batch:
            pub = _parse_published_at(r.get("published_at"))
            if pub and pub < cutoff:
                # Since sorted DESC, all remaining reviews are older — stop pagination
                print(f"[INFO] Reached {max_age_days}-day cutoff. Stopping pagination.")
                return reviews
            reviews.append(r)
        if not data.get("has_next"):
            break
        last_id = data.get("last_id", "")
        if not last_id:
            break
    return reviews


def load_templates(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_company_rules():
    if COMPANY_RULES.exists():
        return COMPANY_RULES.read_text(encoding="utf-8")
    return ""


def post_comment(review_id, text, mark_processed=True):
    if DRY_RUN:
        print(f"[DRY-RUN] Would post comment to {review_id}: {text}")
        return {"dry_run": True}
    args = ["comment-create", "--review-id", review_id, "--text", text]
    if mark_processed:
        args.append("--mark-processed")
    return run_api(*args)


def mark_processed(review_ids):
    if not review_ids:
        return []
    if DRY_RUN:
        print(f"[DRY-RUN] Would mark {len(review_ids)} reviews as PROCESSED")
        return [{"dry_run": True}]
    results = []
    for i in range(0, len(review_ids), 100):
        batch = review_ids[i:i + 100]
        data = run_api("change-status", "--review-ids", ",".join(batch), "--status", "PROCESSED")
        results.append(data)
    return results


def _parse_published_at(raw):
    if not raw:
        return None
    try:
        # Ozon returns ISO 8601 with microseconds and Z suffix, e.g. 2021-02-10T16:43:20.296742Z
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except Exception:
        return None


def group_reviews(reviews):
    groups = {"A": [], "B": [], "C": [], "D": []}
    for r in reviews:
        rating = r.get("rating", 0)
        text = (r.get("text") or "").strip()
        photos_amount = r.get("photos_amount", 0)
        videos_amount = r.get("videos_amount", 0)
        has_media = photos_amount > 0 or videos_amount > 0

        if rating < 4:
            groups["D"].append(r)
            continue

        if not text:
            if not has_media:
                groups["A"].append(r)
            else:
                groups["B"].append(r)
        else:
            groups["C"].append(r)
    return groups


def process_templates(groups):
    generic = load_templates(GENERIC_TEMPLATES)
    photos = load_templates(PHOTOS_TEMPLATES)
    results = {"A": [], "B": [], "errors": []}

    for r in groups["A"]:
        text = random.choice(generic)
        resp = post_comment(r["id"], text, mark_processed=True)
        if resp and "error" in resp:
            results["errors"].append({"review_id": r["id"], "group": "A", "error": resp["error"]})
        else:
            results["A"].append({"review_id": r["id"], "text": text})

    for r in groups["B"]:
        text = random.choice(photos)
        resp = post_comment(r["id"], text, mark_processed=True)
        if resp and "error" in resp:
            results["errors"].append({"review_id": r["id"], "group": "B", "error": resp["error"]})
        else:
            results["B"].append({"review_id": r["id"], "text": text})

    return results


def write_pending_ai(groups):
    if not groups["C"]:
        return None
    ensure_data_dir()
    payload = {
        "reviews": [
            {
                "review_id": r["id"],
                "rating": r.get("rating"),
                "text": r.get("text", ""),
                "photos_amount": r.get("photos_amount", 0),
                "videos_amount": r.get("videos_amount", 0),
                "published_at": r.get("published_at", ""),
            }
            for r in groups["C"]
        ],
        "company_rules": load_company_rules(),
        "instructions": (
            "Для каждого отзыва в массиве reviews подготовь персонализированный ответ продавца. "
            "Учти company_rules. Ответ должен быть вежливым, кратким (до 300 символов), по существу. "
            "Верни результат в виде JSON-объекта с ключом 'answers', где каждый элемент содержит 'review_id' и 'text'."
        ),
    }
    with open(PENDING_AI_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return str(PENDING_AI_PATH)


def write_stage1(groups, template_results, pending_ai_path):
    ensure_data_dir()
    payload = {
        "timestamp": datetime.now().isoformat(),
        "groups": {
            k: [{"id": r["id"], "text": r.get("text", ""), "rating": r.get("rating"), "photos_amount": r.get("photos_amount", 0), "videos_amount": r.get("videos_amount", 0)} for r in v]
            for k, v in groups.items()
        },
        "template_results": template_results,
        "pending_ai_path": pending_ai_path,
    }
    with open(STAGE1_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def write_report(groups, template_results, ai_results, report_path=None):
    ensure_data_dir()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if report_path is None:
        report_path = DATA_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    else:
        report_path = Path(report_path)

    a_items = template_results.get("A", [])
    b_items = template_results.get("B", [])
    a_samples = list(dict.fromkeys([i["text"] for i in a_items]))[:3]
    b_samples = list(dict.fromkeys([i["text"] for i in b_items]))[:3]
    ai_samples = list(dict.fromkeys([i["text"] for i in ai_results if "error" not in i]))[:3]
    errors = template_results.get("errors", []) + [i for i in ai_results if "error" in i]

    total_handled = len(a_items) + len(b_items) + len(ai_results)
    total_fetched = sum(len(v) for v in groups.values())

    lines = [
        f"# Отчёт по обработке отзывов — {now}",
        "",
        "## Сводка",
        "",
        f"За этот прогон мы проверили **{total_fetched}** необработанных отзывов.",
        f"Из них **{total_handled}** получили ответ продавца, а **{len(groups.get('D', []))}** были пропущены (рейтинг ниже 4★).",
        "",
        "### Результат по группам",
        "",
        f"- **Простые отзывы (без текста, без фото):** {len(a_items)} — отправлены шаблонные благодарности.",
        f"- **Отзывы с фото/видео (без текста):** {len(b_items)} — отправлены шаблонные благодарности с упоминанием медиа.",
        f"- **Отзывы с текстом от покупателя:** {len(ai_results)} — отправлены персонализированные AI-ответы.",
        f"- **Пропущено:** {len(groups.get('D', []))} (низкий рейтинг или уже есть официальный ответ).",
        "",
    ]

    if a_samples:
        lines.extend(["## Примеры шаблонных ответов (без фото)", ""])
        for text in a_samples:
            lines.append(f"- {text}")
        lines.append("")

    if b_samples:
        lines.extend(["## Примеры шаблонных ответов (с фото/видео)", ""])
        for text in b_samples:
            lines.append(f"- {text}")
        lines.append("")

    if ai_samples:
        lines.extend(["## Примеры AI-ответов", ""])
        for text in ai_samples:
            lines.append(f"- {text}")
        lines.append("")

    lines.extend(["## Статус обработки", ""])
    if total_handled > 0:
        lines.append("✅ Все подходящие отзывы обработаны. Отчёт готов.")
    else:
        lines.append("ℹ️ На этот раз не было отзывов, требующих ответа.")
    lines.append("")

    lines.extend(["## Ошибки", ""])
    if errors:
        lines.append(f"Всего ошибок: {len(errors)}.")
        for err in errors[:3]:
            lines.append(f"- Отзыв не обработан: {err['error']}")
        if len(errors) > 3:
            lines.append(f"_...и ещё {len(errors) - 3} ошибки_")
    else:
        lines.append("Ошибок не возникло.")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return str(report_path)


def cleanup_files(*paths):
    for p in paths:
        if not p:
            continue
        path = Path(p)
        if DRY_RUN:
            print(f"[DRY-RUN] Would remove {path.name}")
            continue
        if path.exists():
            path.unlink()
            print(f"[INFO] Removed {path.name}")


def apply_ai_answers(ai_path):
    ensure_data_dir()

    if not STAGE1_PATH.exists():
        print("[ERROR] stage1_results.json not found. Run stage 1 first.")
        return

    with open(STAGE1_PATH, "r", encoding="utf-8") as f:
        stage1 = json.load(f)

    groups = {k: v for k, v in stage1["groups"].items()}
    template_results = stage1.get("template_results", {})

    with open(ai_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    answers = data.get("answers", [])
    if not answers:
        print("[WARN] No answers found in AI file.")
        # Still generate report even if no AI answers
        report_path = write_report(groups, template_results, [])
        print(f"[INFO] Report saved: {report_path}")
        cleanup_files(STAGE1_PATH, PENDING_AI_PATH, ai_path)
        return

    if DRY_RUN:
        print(f"[DRY-RUN] Would apply {len(answers)} AI-generated answers")
        for ans in answers:
            print(f"[DRY-RUN]   → {ans.get('review_id')}: {ans.get('text', '').strip()}")
        report_path = write_report(groups, template_results, answers)
        print(f"[INFO] Report saved: {report_path}")
        cleanup_files(STAGE1_PATH, PENDING_AI_PATH, ai_path)
        return

    results = []
    review_ids = []
    for ans in answers:
        review_id = ans.get("review_id")
        text = ans.get("text", "").strip()
        if not review_id or not text:
            results.append({"review_id": review_id or "unknown", "error": "missing review_id or text"})
            continue
        resp = post_comment(review_id, text, mark_processed=True)
        if resp and "error" in resp:
            results.append({"review_id": review_id, "text": text, "error": resp["error"]})
        else:
            results.append({"review_id": review_id, "text": text})
            review_ids.append(review_id)

    mark_processed(review_ids)

    report_path = write_report(groups, template_results, results)
    print(f"[INFO] Report saved: {report_path}")
    cleanup_files(STAGE1_PATH, PENDING_AI_PATH, ai_path)


def main():
    parser = argparse.ArgumentParser(description="Ozon Reviews Workflow Orchestrator")
    parser.add_argument("--apply-ai", help="Path to JSON with AI-generated answers for group C")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without posting real comments or changing statuses")
    args = parser.parse_args()

    global DRY_RUN
    DRY_RUN = args.dry_run
    if DRY_RUN:
        print("[INFO] Running in DRY-RUN mode. No real comments will be posted.")

    if args.apply_ai:
        apply_ai_answers(args.apply_ai)
        return

    # Stage 1: fetch and process templates
    print("[INFO] Fetching unprocessed reviews...")
    reviews = fetch_unprocessed_reviews(max_reviews=200)
    print(f"[INFO] Fetched {len(reviews)} reviews")

    groups = group_reviews(reviews)
    print(f"[INFO] Grouped: A={len(groups['A'])}, B={len(groups['B'])}, C={len(groups['C'])}, D={len(groups['D'])}")

    print("[INFO] Posting template replies for groups A and B...")
    template_results = process_templates(groups)

    processed_ids = [r["id"] for r in groups["A"] + groups["B"]]
    if processed_ids:
        print(f"[INFO] Marking {len(processed_ids)} reviews as processed...")
        mark_processed(processed_ids)

    ai_path = write_pending_ai(groups)
    if ai_path:
        print(f"[INFO] AI batch prepared: {ai_path}")

    write_stage1(groups, template_results, ai_path)
    print(f"[INFO] Stage 1 complete. State saved to {STAGE1_PATH.name}")

    if template_results.get("errors"):
        print(f"[WARN] {len(template_results['errors'])} errors occurred during template posting.")

    # If no AI pending, generate final report immediately
    if not ai_path:
        print("[INFO] No AI reviews pending. Generating final report...")
        report_path = write_report(groups, template_results, [])
        print(f"[INFO] Report saved: {report_path}")
        cleanup_files(STAGE1_PATH)


if __name__ == "__main__":
    main()
