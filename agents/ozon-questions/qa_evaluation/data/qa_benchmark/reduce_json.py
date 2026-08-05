import json
import sys

src = "/Users/vanitu/PaxSoftProjects/krabot/krabot-agents/agents/ozon-questions/workspace/data/qa_benchmark/ground_truth_20260415_133501.json"
dst = "/Users/vanitu/PaxSoftProjects/krabot/krabot-agents/agents/ozon-questions/workspace/data/qa_benchmark/eval_data.json"

with open(src, "r", encoding="utf-8") as f:
    data = json.load(f)

reduced = []
for item in data:
    reduced.append({
        "question_id": item.get("question_id"),
        "sku": item.get("sku"),
        "question_text": item.get("question_text"),
    })

with open(dst, "w", encoding="utf-8") as f:
    json.dump(reduced, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(reduced)} records to {dst}")
