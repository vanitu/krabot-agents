#!/usr/bin/env python3
"""Prepare a complete context package for answering an Ozon buyer question.

Requires Ozon credentials (OZON_CLIENT_ID + OZON_API_KEY).

Usage:
    python3 prepare_context.py --question-id <uuid>
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent
RESOURCES_DIR = SKILL_DIR / "resources"
DATA_DIR = WORKSPACE_DIR / "data" / "qa_contexts"
CACHE_DIR = WORKSPACE_DIR / "data" / "product_cache"
CACHE_TTL_SECONDS = 604800  # 1 week
OZON_QUESTIONS_SCRIPT = SKILL_DIR.parent / "ozon-questions-api" / "scripts" / "ozon_questions.py"
FORMAT_SCRIPT = SKILL_DIR.parent / "ozon-product-info-api" / "scripts" / "format_product_info.py"
RULES_FILE = RESOURCES_DIR / "answer_rules.md"
EXAMPLE_FILE = RESOURCES_DIR / "answer_example.md"


def run_ozon_question_info(question_id):
    cmd = [sys.executable, str(OZON_QUESTIONS_SCRIPT), "info", "--question-id", question_id]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] ozon_questions.py info failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON from ozon_questions.py:\n{result.stdout}\n{exc}", file=sys.stderr)
        sys.exit(1)


def run_format_product_info(sku):
    cmd = [sys.executable, str(FORMAT_SCRIPT), "--sku", str(sku)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] format_product_info.py failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def get_cached_product_context(sku):
    """Return cached product context if it exists and is not expired."""
    cache_file = CACHE_DIR / f"{sku}.json"
    if not cache_file.exists():
        return None
    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        cached_at = datetime.fromisoformat(data.get("cached_at", "1970-01-01T00:00:00"))
        age_seconds = (datetime.now() - cached_at).total_seconds()
        if age_seconds > CACHE_TTL_SECONDS:
            print(f"[INFO] Cache expired for SKU {sku} (age={age_seconds:.0f}s)", file=sys.stderr)
            return None
        print(f"[INFO] Cache hit for SKU {sku} (age={age_seconds:.0f}s)", file=sys.stderr)
        return data.get("product_context", "")
    except Exception as exc:
        print(f"[WARN] Failed to read cache for SKU {sku}: {exc}", file=sys.stderr)
        return None


def save_product_context_cache(sku, product_context):
    """Save product context to cache file."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{sku}.json"
    cache_file.write_text(
        json.dumps({
            "cached_at": datetime.now().isoformat(),
            "sku": sku,
            "product_context": product_context,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def read_file(path):
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def build_agent_prompt(question_text, product_context, rules, example):
    return f"""Ты — ассистент продавца на маркетплейсе Ozon. Твоя задача — подготовить структурированный ответ на вопрос покупателя, основываясь исключительно на предоставленной карточке товара.

---

## Вопрос покупателя

{question_text}

---

## Карточка товара (контекст)

{product_context}

---

## Правила генерации ответов

{rules}

---

## Пример структурированного отчёта

{example}

---

## Инструкция

На основе всего вышеизложенного подготовь:

1. **Ответ** — краткий, вежливый и точный ответ на вопрос покупателя (на русском языке).
2. **Оценка достаточности информации** — шкала от 0 до 10, насколько полно карточка товара позволяет ответить на вопрос.
3. **Оценка точности ответа** — шкала от 0 до 10, насколько точен предложенный ответ по отношению к источнику.
4. **Отчёт и reasoning** — краткое объяснение, почему дан именно такой ответ, на каком атрибуте/разделе карточки он основан, и какие риски ошибки.

Верни результат в виде JSON-объекта со следующими ключами:
- `answer` (строка)
- `sufficiency_score` (число)
- `accuracy_score` (число)
- `reasoning` (строка)
"""


def build_batch_prompt(contexts):
    """Build a single prompt for a batch of questions.

    Args:
        contexts: List of dicts returned by build_context(), each containing
                  question_info and product_context.

    Returns:
        A single prompt string ready for the subagent.
    """
    if not contexts:
        raise ValueError("contexts list cannot be empty")

    rules = contexts[0].get("rules", "")
    example = contexts[0].get("example", "")

    prompt_parts = [
        "Ты — ассистент продавца на маркетплейсе Ozon. Твоя задача — подготовить структурированные ответы на несколько вопросов покупателей, основываясь исключительно на предоставленных карточках товаров.",
        "",
        "---",
        "",
        "## Правила генерации ответов",
        "",
        rules,
    ]

    if example:
        prompt_parts.extend([
            "",
            "---",
            "",
            "## Пример структурированного отчёта",
            "",
            example,
        ])

    prompt_parts.extend([
        "",
        "---",
        "",
        "## Вопросы покупателей и контекст товаров",
        "",
    ])

    for idx, ctx in enumerate(contexts, start=1):
        q = ctx.get("question_info", {})
        prompt_parts.extend([
            f"### Вопрос {idx}",
            "",
            f"- **question_id**: {q.get('id', '')}",
            f"- **SKU**: {q.get('sku', '')}",
            f"- **Текст вопроса**: {q.get('text', '')}",
            "",
            "#### Карточка товара (контекст)",
            "",
            ctx.get("product_context", ""),
            "",
            "---",
            "",
        ])

    prompt_parts.extend([
        "## Инструкция",
        "",
        f"Для каждого из {len(contexts)} вопросов выше подготовь:",
        "",
        "1. **Ответ** — краткий, вежливый и точный ответ на вопрос покупателя (на русском языке).",
        "2. **Оценка достаточности информации** — шкала от 0 до 10, насколько полно карточка товара позволяет ответить на вопрос.",
        "3. **Оценка точности ответа** — шкала от 0 до 10, насколько точен предложенный ответ по отношению к источнику.",
        "4. **Отчёт и reasoning** — краткое объяснение, почему дан именно такой ответ, на каком атрибуте/разделе карточки он основан, и какие риски ошибки.",
        "",
        "Верни результат в виде JSON-МАССИВА, содержащего ровно по одному объекту для каждого вопроса (в том же порядке, что и выше). Каждый объект должен содержать следующие ключи:",
        '- `question_id` (строка)',
        '- `answer` (строка)',
        '- `sufficiency_score` (число)',
        '- `accuracy_score` (число)',
        '- `reasoning` (строка)',
        "",
        "Верни ТОЛЬКО JSON-массив, без markdown-форматирования (без ```json), без дополнительного текста до или после массива.",
    ])

    return "\n".join(prompt_parts)


def build_context(question_id):
    """Prepare full context package for a given question_id.

    Returns a dict with keys:
        question_info, product_context, rules, example, agent_prompt, context_path
    """
    raw_question = run_ozon_question_info(question_id)

    if "error" in raw_question:
        raise RuntimeError(f"API returned error: {raw_question['error']}")

    q = raw_question
    question_info = {
        "id": q.get("id", ""),
        "text": q.get("text", ""),
        "sku": q.get("sku"),
        "product_url": q.get("product_url", ""),
        "author_name": q.get("author_name", ""),
        "published_at": q.get("published_at", ""),
    }

    sku = question_info.get("sku")
    if not sku:
        raise RuntimeError("Question response missing 'sku' field")

    product_context = get_cached_product_context(sku)
    if product_context is None:
        product_context = run_format_product_info(sku)
        save_product_context_cache(sku, product_context)

    rules = read_file(RULES_FILE)
    example = read_file(EXAMPLE_FILE)

    agent_prompt = build_agent_prompt(
        question_info["text"],
        product_context,
        rules,
        example,
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    context_path = DATA_DIR / f"context_{question_info['id']}_{timestamp}.json"
    context_path.write_text(
        json.dumps({
            "question_info": question_info,
            "product_context": product_context,
            "rules": rules,
            "example": example,
            "agent_prompt": agent_prompt,
            "context_path": str(context_path),
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "question_info": question_info,
        "product_context": product_context,
        "rules": rules,
        "example": example,
        "agent_prompt": agent_prompt,
        "context_path": str(context_path),
    }


def main():
    parser = argparse.ArgumentParser(description="Prepare context for answering an Ozon buyer question")
    parser.add_argument("--question-id", required=True, help="Ozon question UUID")
    args = parser.parse_args()

    try:
        result = build_context(args.question_id)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"[INFO] Context saved to: {result['context_path']}", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
