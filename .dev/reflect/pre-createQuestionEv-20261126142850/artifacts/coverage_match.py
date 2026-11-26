"""Deterministic UC-1 coverage match (refs/coverage-mapping.md), parsed and inferred rows.

Pure string arithmetic, no model.
  parsed rows : exact token match of the requirement id in a task item of the plan
  inferred rows: content-word containment >= 0.6 against a single task item
Usage: uv run python coverage_match.py <source.md> <tasklist.md> <inf-rows.json> <out.json>
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
ID_RE = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.casefold()) if w not in STOP}


def main(src_path, plan_path, rows_path, out_path) -> int:
    src_lines = open(src_path, encoding="utf-8").read().splitlines()
    plan = open(plan_path, encoding="utf-8").read()
    inf_rows = json.load(open(rows_path, encoding="utf-8"))
    tasks = {}
    for m in re.finditer(r"^## Task (\d+):.*?(?=^## |\Z)", plan, re.S | re.M):
        tasks[int(m.group(1))] = m.group(0)
    twords = {n: words(t) for n, t in tasks.items()}

    # Pass 1: parsed ids, outside fenced code
    parsed, fenced = [], False
    for i, line in enumerate(src_lines, 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for m in ID_RE.finditer(line):
            if m.group(1) not in [p["requirement_id"] for p in parsed]:
                parsed.append({"requirement_id": m.group(1), "source": "parsed", "citation": f"source.md:{i}"})
    out = []
    for p in parsed:
        hits = sorted(n for n, t in tasks.items() if re.search(r"\b" + re.escape(p["requirement_id"]) + r"\b", t))
        p.update({"matched_task_ids": hits, "match_method": "exact" if hits else "none"})
        out.append(p)

    # Pass 2: inferred rows, quote must be verbatim on the cited line
    invalid = []
    for r in inf_rows:
        if r["quote"] not in src_lines[r["line"] - 1]:
            invalid.append(r["id"])
            continue
        qw = words(r["quote"])
        best_n, best = None, 0.0
        for n in sorted(twords):
            ratio = len(qw & twords[n]) / len(qw) if qw else 0.0
            if ratio > best:
                best_n, best = n, ratio
        ok = best >= 0.6
        out.append({"requirement_id": r["id"], "source": "inferred", "citation": f"source.md:{r['line']}",
                    "best_task": best_n, "best_ratio": round(best, 4),
                    "matched_task_ids": [best_n] if ok else [], "match_method": "containment" if ok else "none"})

    par = [o for o in out if o["source"] == "parsed"]
    inf = [o for o in out if o["source"] == "inferred"]
    pm = sum(1 for o in par if o["match_method"] != "none")
    um = sum(1 for o in out if o["match_method"] != "none")
    summary = {
        "parsed_count": len(par), "inferred_count": len(inf), "invalid_dropped": invalid,
        "coverage_pct": round(pm / len(par), 4) if par else None,
        "coverage_pct_union": round(um / len(out), 4) if out else None,
        "unmapped_requirements": [o["requirement_id"] for o in par if o["match_method"] == "none"],
        "unmapped_requirements_union": [o["requirement_id"] for o in out if o["match_method"] == "none"],
        "S_dev_density": round((len(out) - um) / len(out), 4) if out else None,
        "coverage_degraded": "parsed-sparse" if len(inf) > len(par) else None,
        "task_count": len(tasks),
    }
    json.dump({"summary": summary, "matrix": out}, open(out_path, "w", encoding="utf-8"), indent=2)
    print(json.dumps(summary, indent=2))
    for o in out:
        if o["match_method"] == "none":
            print("UNMAPPED", o["requirement_id"], o.get("best_ratio", ""), o.get("best_task", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:5]))
