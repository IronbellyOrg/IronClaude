"""Deterministic Pass-2 containment match for the UC-1 coverage map (refs/coverage-mapping.md).

Pure string arithmetic, no model. Usage:
  uv run python coverage_match.py <source.md> <tasklist.md> <inf-rows.json> <out.json>
"""
import json
import re
import sys

STOP = set(
    "a an the and or but nor of to in on at by for with from as into onto over under per via is are was were "
    "be been being am do does did have has had will would should shall can could may might must it its this "
    "that these those there their them they we us our you your i he she his her which who whom whose what "
    "when where while than then so if also".split()
)


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.casefold()) if w not in STOP}


def main(src_path: str, plan_path: str, rows_path: str, out_path: str) -> int:
    src_lines = open(src_path, encoding="utf-8").read().splitlines()
    plan = open(plan_path, encoding="utf-8").read()
    rows = json.load(open(rows_path, encoding="utf-8"))
    # task items: "## Task N:" heading to the next "## " heading
    tasks = {}
    for m in re.finditer(r"^## Task (\d+):.*?(?=^## |\Z)", plan, re.S | re.M):
        tasks[int(m.group(1))] = m.group(0)
    twords = {n: words(t) for n, t in tasks.items()}
    out, invalid = [], []
    for r in rows:
        line = src_lines[r["line"] - 1]
        if r["quote"] not in line:
            invalid.append(r["id"])  # quote does not match its cited line: dropped at emission
            continue
        qw = words(r["quote"])
        best_n, best_ratio = None, 0.0
        for n in sorted(twords):  # ties: first task in order wins
            ratio = len(qw & twords[n]) / len(qw) if qw else 0.0
            if ratio > best_ratio:
                best_n, best_ratio = n, ratio
        matched = best_ratio >= 0.6
        out.append({
            "requirement_id": r["id"], "source": "inferred", "citation": f"source.md:{r['line']}",
            "content_words": len(qw), "best_task": best_n, "best_ratio": round(best_ratio, 4),
            "match_method": "containment" if matched else "none",
            "matched_task_ids": [best_n] if matched else [],
        })
    total = len(out)
    matched_n = sum(1 for o in out if o["match_method"] == "containment")
    summary = {
        "parsed_count": 0, "inferred_count": total, "invalid_dropped": invalid,
        "coverage_pct": None, "coverage_pct_union": round(matched_n / total, 4) if total else None,
        "unmapped_requirements": [],
        "unmapped_requirements_union": [o["requirement_id"] for o in out if o["match_method"] == "none"],
        "S_dev_density": round((total - matched_n) / total, 4) if total else None,
        "coverage_degraded": "parsed-sparse" if total > 0 else None,
        "task_count": len(tasks),
    }
    json.dump({"summary": summary, "matrix": out}, open(out_path, "w", encoding="utf-8"), indent=2)
    print(json.dumps(summary, indent=2))
    for o in out:
        print(f"{o['requirement_id']}  {o['match_method']:11}  best=Task {o['best_task']}  ratio={o['best_ratio']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:5]))
