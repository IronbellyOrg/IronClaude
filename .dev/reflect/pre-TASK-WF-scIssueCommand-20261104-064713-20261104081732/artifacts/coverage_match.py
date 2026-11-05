"""Deterministic Step 1B containment matcher (refs/coverage-mapping.md, D13).

Usage: uv run --no-project python coverage_match.py <spec> <tasklist> <requirements.json> <out.json>
Checks every INF quote is a verbatim substring of its cited spec line (rows that
fail are dropped), then matches each surviving row to the single task with the
highest content-word containment ratio (>= 0.6 to count as matched).
"""

import json
import re
import sys

STOP = set(
    "a an the and or but nor of to in on at by for with from into onto as is are be been was were "
    "it its this that these those than then if not no so do does did has have had will would can could "
    "should shall must may each every any all both either neither one only also".split()
)


def words(text):
    return [w for w in re.findall(r"[a-z0-9_]+", text.lower()) if w not in STOP]


def main(spec, tasklist, reqs_path, out_path):
    spec_lines = open(spec, encoding="utf-8").read().splitlines()
    plan = open(tasklist, encoding="utf-8").read()
    parts = re.split(r"^## Task (\d+):", plan, flags=re.M)
    tasks = [(f"Task {parts[i]}", parts[i + 1]) for i in range(1, len(parts), 2)]
    task_words = [(tid, set(words(body))) for tid, body in tasks]
    rows, dropped = [], []
    for r in json.load(open(reqs_path, encoding="utf-8")):
        line = spec_lines[r["line"] - 1] if 0 < r["line"] <= len(spec_lines) else ""
        if r["quote"] not in line:
            dropped.append({"id": r["id"], "reason": "quote not on cited line"})
            continue
        qw = set(words(r["quote"]))
        best = max(((len(qw & tw) / len(qw), tid) for tid, tw in task_words), key=lambda x: x[0])
        ratio = round(best[0], 4)
        rows.append({
            "requirement_id": r["id"], "citation": f"source.md:{r['line']}", "quote": r["quote"],
            "matched_task_ids": [best[1]] if ratio >= 0.6 else [],
            "match_method": "containment" if ratio >= 0.6 else "none",
            "best_task": best[1], "ratio": ratio, "source": "inferred",
        })
    matched = sum(1 for x in rows if x["match_method"] != "none")
    total = len(rows)
    out = {
        "parsed_count": 0, "inferred_count": total, "inferred_dropped": dropped,
        "coverage_pct": None, "coverage_pct_union": round(matched / total, 4) if total else None,
        "unmapped_requirements": [],
        "unmapped_requirements_union": [x["requirement_id"] for x in rows if x["match_method"] == "none"],
        "S_dev_density": round((total - matched) / total, 4) if total else None,
        "task_count": len(tasks), "matrix": rows,
    }
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "matrix"}, indent=1))
    for x in rows:
        print(x["requirement_id"], x["match_method"], x["best_task"], x["ratio"])


if __name__ == "__main__":
    main(*sys.argv[1:5])
