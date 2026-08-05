#!/usr/bin/env python3
"""Generate answer scaffold or final report from a prepared context package.

Does NOT require Ozon credentials.

Scaffold mode (default):
    python3 generate_answer.py --context-json path/to/context.json

Final report mode:
    python3 generate_answer.py --context-json path/to/context.json --fill-json path/to/answer.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent
REPORTS_DIR = WORKSPACE_DIR / "data" / "qa_reports"


def read_context(path=None):
    if path:
        data = Path(path).read_text(encoding="utf-8")
    else:
        data = sys.stdin.read()
    if not data.strip():
        print("[ERROR] No input data provided.", file=sys.stderr)
        sys.exit(1)
    return json.loads(data)


def read_answer_json(path):
    data = Path(path).read_text(encoding="utf-8")
    return json.loads(data)


def save_report(context, answer_data, path):
    q = context.get("question_info", {})
    a = answer_data or {}
    lines = [
        f"# Ответ на вопрос — {q.get('id', 'unknown')}",
        "",
        "## Информация о вопросе",
        "",
        f"- **ID:** {q.get('id')}",
        f"- **Автор:** {q.get('author_name')}",
        f"- **SKU:** {q.get('sku')}",
        f"- **Дата:** {q.get('published_at')}",
        f"- **Ссылка:** {q.get('product_url')}",
        "",
        "## Вопрос",
        "",
        f"> {q.get('text')}",
        "",
        "## Контекст товара",
        "",
        context.get("product_context", ""),
        "",
        "## Ответ",
        "",
        a.get("answer", "_ответ пока не сформирован_"),
        "",
        "## Оценка достаточности информации",
        "",
        str(a.get("sufficiency_score", "_оценка пока не проставлена_")),
        "",
        "## Оценка точности ответа",
        "",
        str(a.get("accuracy_score", "_оценка пока не проставлена_")),
        "",
        "## Отчёт и reasoning",
        "",
        a.get("reasoning", "_reasoning пока не заполнен_"),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def save_draft_report(context, path):
    return save_report(context, {}, path)


def main():
    parser = argparse.ArgumentParser(description="Generate answer report from prepared context")
    parser.add_argument("--context-json", help="Path to context JSON file produced by prepare_context.py")
    parser.add_argument("--fill-json", help="Path to JSON with answer, sufficiency_score, accuracy_score, reasoning")
    parser.add_argument("--output", "-o", help="Path for the output report (default: auto-generated)")
    args = parser.parse_args()

    context = read_context(args.context_json)
    q = context.get("question_info", {})

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.fill_json:
        answer_data = read_answer_json(args.fill_json)
        report_name = f"final_{q.get('id', 'unknown')}_{timestamp}.md"
    else:
        answer_data = {}
        report_name = f"draft_{q.get('id', 'unknown')}_{timestamp}.md"

    report_path = Path(args.output) if args.output else REPORTS_DIR / report_name
    report_path_str = save_report(context, answer_data, report_path)

    print(f"[INFO] Report saved to: {report_path_str}", file=sys.stderr)

    result = {
        "question_info": q,
        "product_context": context.get("product_context", ""),
        "rules": context.get("rules", ""),
        "example": context.get("example", ""),
        "agent_prompt": context.get("agent_prompt", ""),
        "context_path": context.get("context_path", ""),
        "report_path": report_path_str,
        "answer": answer_data.get("answer", ""),
        "sufficiency_score": answer_data.get("sufficiency_score"),
        "accuracy_score": answer_data.get("accuracy_score"),
        "reasoning": answer_data.get("reasoning", ""),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
