"""Wave 1B coverage (D13): Pass-1 regex check, Pass-2 quote verification, containment matching.
Usage: uv run python coverage.py <spec> <tasklist> <inf-rows.tsv> <out.json>
Deterministic: pure string arithmetic, no LLM.
"""
import json
import re
import sys

spec_p, plan_p, tsv_p, out_p = sys.argv[1:5]
spec = open(spec_p).read().split("\n")
plan_text = open(plan_p).read()
plan = plan_text.split("\n")

ID_REGEX = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")


def strip_fences(lines):
    out, fence = [], False
    for ln in lines:
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        out.append("" if fence else ln)
    return out


parsed_spec = sorted(set(m.group(0) for ln in strip_fences(spec) for m in ID_REGEX.finditer(ln)))
parsed_plan = sorted(set(m.group(0) for ln in strip_fences(plan) for m in ID_REGEX.finditer(ln)))

# task items = "## Task N:" sections; constraint bullets listed separately (secondary view)
items, cur = {}, None
for ln in plan:
    m = re.match(r"## Task (\d+):", ln)
    if m:
        cur = "T%s" % m.group(1)
        items[cur] = []
        continue
    if ln.startswith("## "):
        cur = None
    if cur:
        items[cur].append(ln)
cons = {}
in_c = False
n = 0
for ln in plan:
    if ln.startswith("## Constraints"):
        in_c = True
        continue
    if in_c and ln.startswith("## "):
        in_c = False
    if in_c and ln.startswith("- "):
        n += 1
        cons["C%d" % n] = ln

STOP = set("a an the and or but nor of in on at to for from by with without as is are was were be been being it its this that these those not no than then so if when while which who whom whose into onto over under after before between both either each any all only also may must shall should can could will would do does did has have had there their they them we our you your i he she his her".split())


def words(s):
    s = s.casefold()
    return [w for w in re.findall(r"[a-z0-9_]+", s) if w not in STOP]


item_words = {k: set(words(" ".join(v))) for k, v in items.items()}
cons_words = {k: set(words(v)) for k, v in cons.items()}

rows, bad = [], []
for i, ln in enumerate(open(tsv_p).read().rstrip("\n").split("\n"), 1):
    lineno, quote = ln.split("\t", 1)
    lineno = int(lineno)
    rid = "INF-%03d" % i
    if quote not in spec[lineno - 1]:
        bad.append((rid, lineno, "quote not on cited line"))
        continue
    w = words(quote)
    ws = set(w)
    best = (0.0, None)
    for k, v in item_words.items():
        r = len(ws & v) / len(ws) if ws else 0
        if r > best[0] + 1e-9:
            best = (r, k)
    bestc = (0.0, None)
    for k, v in cons_words.items():
        r = len(ws & v) / len(ws) if ws else 0
        if r > bestc[0] + 1e-9:
            bestc = (r, k)
    matched = best[0] >= 0.6
    rows.append({
        "requirement_id": rid, "source": "inferred", "citation": "source.md:%d" % lineno, "quote": quote,
        "match_method": "containment" if matched else "none",
        "matched_task_ids": [best[1]] if matched else [],
        "best_ratio": round(best[0], 4), "best_task": best[1],
        "best_constraint": bestc[1], "best_constraint_ratio": round(bestc[0], 4),
    })

total = len(rows)
matched = sum(1 for r in rows if r["match_method"] == "containment")
union_pct = round(matched / total, 4) if total else None
res = {
    "parsed_spec_ids": parsed_spec, "parsed_plan_ids": parsed_plan,
    "parsed_count": len(parsed_spec), "inferred_count": total,
    "coverage_pct": None if not parsed_spec else 0.0,
    "coverage_pct_union": union_pct, "coverage_undefined": (not parsed_spec and total == 0),
    "coverage_degraded": "parsed-sparse" if total > len(parsed_spec) else None,
    "matched": matched, "unmatched": [r["requirement_id"] for r in rows if r["match_method"] == "none"],
    "invalid_rows_dropped": bad, "task_items": sorted(items), "constraint_items": sorted(cons), "rows": rows,
}
json.dump(res, open(out_p, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
for r in rows:
    if r["match_method"] == "none":
        print("UNMATCHED", r["requirement_id"], r["citation"], r["best_ratio"], r["best_task"], "| constraint", r["best_constraint"], r["best_constraint_ratio"], "|", r["quote"][:90])
