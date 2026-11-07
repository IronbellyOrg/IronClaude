"""Deterministic containment for this review; writes only sibling review outputs."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[2]
STOPWORDS = frozenset("a an the and or but nor for so yet at by from in into of on onto to with without as is are was were be been being do does did can could may might must shall should will would not no only its it this that these those their them they we you your our even after before then than if when while also".split())


def words(text):
    return set(re.findall(r"[a-z0-9]+", text.casefold())) - STOPWORDS


def containment(quote, text):
    tokens = words(quote)
    return len(tokens & words(text)) / len(tokens) if tokens else 0.0


assert containment("the safe refresh", "safe refresh") == 1.0
assert containment("safe refresh edited", "safe refresh") == 2 / 3
assert containment("safe refresh", "plain shell") == 0.0

spec = (PACKAGE / "source.md").read_text()
plan = (PACKAGE / (PACKAGE.name + ".md")).read_text()
parsed = list(dict.fromkeys(re.findall(r"\b(?:R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b", spec)))
assert not parsed, "This run's source was checked as an unlabeled paragraph"
parts = re.split(r"(?m)^## Task (\d+):", plan)
tasks = [("Task " + parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]
assert len(tasks) == 2
rows = json.loads((HERE / "inferred-requirements.json").read_text())
assert rows
for row in rows:
    assert row["source"] == "inferred"
    assert row["quote"] in spec, row["id"]
    scored = [(containment(row["quote"], text), index, name) for index, (name, text) in enumerate(tasks)]
    score, _, name = max(scored, key=lambda entry: (entry[0], -entry[1]))
    row.update(containment_ratio=round(score, 6), matched_task_ids=[name] if score >= .6 else [], match_method="containment" if score >= .6 else "none")
matched = sum(bool(r["matched_task_ids"]) for r in rows)
result = {"parsed_count": 0, "inferred_count": len(rows), "task_count": len(tasks), "coverage_pct": None, "coverage_pct_union": round(matched / len(rows), 4), "coverage_undefined": False, "coverage_degraded": "parsed-sparse", "unmapped_requirements": [], "unmapped_requirements_union": [r["id"] for r in rows if not r["matched_task_ids"]], "S_dev_density": (len(rows) - matched) / len(rows), "stopword_set": sorted(STOPWORDS), "tokenization": "lowercase unique alphanumeric word tokens", "rows": rows}
(HERE / "coverage-matrix.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k not in ("rows", "stopword_set")}, indent=2))
