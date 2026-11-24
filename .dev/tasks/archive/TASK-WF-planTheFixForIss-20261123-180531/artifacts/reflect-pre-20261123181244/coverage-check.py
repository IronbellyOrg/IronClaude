"""Deterministic content-word coverage matching for this pre-review.

Reads the parent-persisted extracted rows and original input files. Writes no
files; stdout is the machine result for parent persistence.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

STOPWORDS = frozenset(
    "a an the and or but for to of in on at by with from as is are was were be "
    "been being do does did not no only that this it its their them then than "
    "can could should would must shall will before after instead".split()
)


def words(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold())) - STOPWORDS


def main() -> None:
    rows_path, plan_path, spec_path = map(Path, sys.argv[1:4])
    rows = json.loads(rows_path.read_text())
    plan = plan_path.read_text()
    spec = spec_path.read_text()
    tasks = []
    for match in re.finditer(r"(?ms)^## Task (\d+):.*?(?=^## (?:Phase|Task) |\Z)", plan):
        tasks.append((int(match[1]), match[0]))
    result = []
    for row in rows:
        assert row["quote"] in spec, row
        tokens = words(row["quote"])
        assert tokens
        scores = [(len(tokens & words(body)) / len(tokens), number) for number, body in tasks]
        ratio, task = max(scores, key=lambda item: (item[0], -item[1]))
        result.append({**row, "source": "inferred", "ratio": round(ratio, 4),
                       "matched_task_ids": [task] if ratio >= 0.6 else [],
                       "match_method": "containment" if ratio >= 0.6 else "none"})
    unmapped = [row["id"] for row in result if not row["matched_task_ids"]]
    print(json.dumps({"total_tasks": len(tasks), "parsed_count": 0,
                      "inferred_count": len(result), "coverage_pct": None,
                      "coverage_pct_union": round((len(result) - len(unmapped)) / len(result), 4),
                      "coverage_degraded": "parsed-sparse", "coverage_undefined": False,
                      "unmapped_requirements": [], "unmapped_requirements_union": unmapped,
                      "S_dev_density": round(len(unmapped) / len(result), 4),
                      "stopwords": sorted(STOPWORDS), "matrix": result}, indent=2))


if __name__ == "__main__":
    main()
