#!/usr/bin/env python3
"""
Convert eval_merged.json into a readable Markdown report.

Reads:
  - data/qa_benchmark/eval_merged.json

Writes:
  - data/qa_benchmark/eval_report.md
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVAL_PATH = os.path.join(
    BASE_DIR, "data", "qa_benchmark", "version2_test", "eval_merged.json"
)
OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "qa_benchmark", "version2_test", "eval_report.md"
)


def escape_md(text: str) -> str:
    if not text:
        return ""
    return text.replace("|", "\\|").replace("\n", " ")


def main():
    with open(EVAL_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = [
        "# Отчёт по оценке AI-ответов",
        "",
        f"Всего вопросов: {len(data)}",
        "",
        "---",
        "",
    ]

    for i, item in enumerate(data, 1):
        lines.append(f"## {i}. {escape_md(item.get('question_text', ''))}")
        lines.append("")
        lines.append(f"**SKU:** `{item.get('sku')}`  ")
        lines.append(f"**Question ID:** `{item.get('question_id')}`  ")
        lines.append(f"**Published:** {item.get('published_at', '')}")
        lines.append("")
        lines.append("### Человеческий ответ")
        lines.append(f"> {escape_md(item.get('human_answer', '—'))}")
        lines.append("")
        lines.append("### AI-ответ")
        lines.append(f"> {escape_md(item.get('ai_answer', '—'))}")
        lines.append("")
        lines.append("### Оценки")
        lines.append(f"- **Sufficiency:** {item.get('sufficiency_score', '—')} / 10")
        lines.append(f"- **Accuracy:** {item.get('accuracy_score', '—')} / 10")
        lines.append("")
        lines.append("### Reasoning")
        lines.append(f"{item.get('reasoning', '—')}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Summary stats
    suff_scores = [item.get("sufficiency_score", 0) or 0 for item in data]
    acc_scores = [item.get("accuracy_score", 0) or 0 for item in data]

    lines.append("## Сводка")
    lines.append("")
    lines.append(
        f"- **Средняя sufficiency_score:** {sum(suff_scores) / len(suff_scores):.2f}"
    )
    lines.append(
        f"- **Средняя accuracy_score:** {sum(acc_scores) / len(acc_scores):.2f}"
    )
    lines.append(
        f"- **Мedian sufficiency_score:** {sorted(suff_scores)[len(suff_scores) // 2]:.1f}"
    )
    lines.append(
        f"- **Мedian accuracy_score:** {sorted(acc_scores)[len(acc_scores) // 2]:.1f}"
    )
    lines.append("")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Report saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
