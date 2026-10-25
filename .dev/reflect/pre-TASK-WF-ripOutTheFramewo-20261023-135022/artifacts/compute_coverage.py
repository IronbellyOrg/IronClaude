"""Deterministic UC-1 containment map, scoped to reflection output only."""
import json
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent
ROOT = OUT.parents[2]
extraction = yaml.load((OUT / "artifacts/coverage-extraction.yaml").read_text(), Loader=yaml.BaseLoader)
source = ROOT / extraction["source_file"]
plan = source.parent / "TASK-WF-ripOutTheFramewo-20261023-134610.md"
lines = plan.read_text().splitlines()
stopwords = set(extraction["matching_proposal"]["stopwords"])


def words(text):
    return set(re.findall(r"[a-z0-9]+", re.sub(r"'s\b", "", text.casefold()))) - stopwords


tasks = []
for task, span in extraction["matching_proposal"]["task_blocks"].items():
    start, end = map(int, span.split("-"))
    tasks.append((task, words("\n".join(lines[start - 1:end]))))
rows = []
source_lines = source.read_text().splitlines()
for row in extraction["inferred_rows"]:
    span = list(map(int, row["lines"].split("-")))
    text = " ".join(" ".join(source_lines[span[0] - 1:span[-1]]).split())
    assert row["quote"] in text, (row["id"], row["quote"], text)
    tokens = words(row["quote"])
    scores = [(task, len(tokens & task_words) / len(tokens)) for task, task_words in tasks]
    best_task, best_score = max(scores, key=lambda pair: pair[1])
    rows.append({**row, "source": "inferred", "citation": f"{source.relative_to(ROOT)}:{row['lines']}", "content_words": sorted(tokens), "ratios": {task: round(score, 4) for task, score in scores}, "matched_task_ids": [best_task] if best_score >= 0.6 else [], "match_method": "containment" if best_score >= 0.6 else "none"})
parsed = re.findall(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b", source.read_text())
assert parsed == []
unmapped = [row["id"] for row in rows if not row["matched_task_ids"]]
result = {"parsed_count": 0, "inferred_count": len(rows), "total_tasks": len(tasks), "coverage_pct": None, "coverage_pct_union": round((len(rows) - len(unmapped)) / len(rows), 4), "unmapped_requirements": [], "unmapped_requirements_union": unmapped, "coverage_undefined": False, "coverage_degraded": "parsed-sparse", "S_scope": len(tasks), "S_domains": 3, "domains": ["code", "infra", "docs"], "S_dev_density": round(len(unmapped) / len(rows), 4), "tokenization": extraction["matching_proposal"]["tokenization"], "stopwords": sorted(stopwords), "rows": rows}
(OUT / "artifacts/coverage-matrix.yaml").write_text(yaml.safe_dump(result, sort_keys=False))
print(json.dumps(result, indent=2))
