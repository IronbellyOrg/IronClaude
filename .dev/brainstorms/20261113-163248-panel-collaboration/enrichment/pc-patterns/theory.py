"""Within-model tests for the three candidate theories."""
import json, collections, statistics as st, os, re
R = json.load(open("/tmp/pc-patterns/records_gt.json"))
ORDER = ["ember", "luna", "haiku", "sonnet", "grok", "terra", "wonder"]
by = collections.defaultdict(list)
for r in R:
    by[r["model"]].append(r)
HARD = {"I5", "I7", "B7", "B8", "I6", "B1", "B2", "B3", "I4"}  # cross-doc/missing-task + satisfiability
def mean(x):
    x = [v for v in x if v is not None]; return sum(x) / len(x) if x else float("nan")
def med(x):
    x = [v for v in x if v is not None]; return st.median(x) if x else float("nan")
def hard(r): return len(HARD & set(r["gt"]))
def anyg(r): return len(r["gt"])

print("## Theory test A: reasoning budget. Model-level medians and within-model split at the model's own median thinking tokens\n")
print("| model | median thinking tok | median wall s | GT-proxy hits/run (all) | hard hits/run | low-think: hits/run | high-think: hits/run | low-think: hard/run | high-think: hard/run |")
print("|---|---|---|---|---|---|---|---|---|")
pts = []
for m in ORDER:
    rs = by[m]; md = med([r["thinking_tok"] for r in rs])
    lo = [r for r in rs if (r["thinking_tok"] or 0) <= md]; hi = [r for r in rs if (r["thinking_tok"] or 0) > md]
    pts.append((md, mean([anyg(r) for r in rs])))
    print(f"| {m} | {md:.0f} | {med([r['wall_s'] for r in rs]):.0f} | {mean([anyg(r) for r in rs]):.2f} | {mean([hard(r) for r in rs]):.2f} | {mean([anyg(r) for r in lo]):.2f} (n={len(lo)}) | {mean([anyg(r) for r in hi]):.2f} (n={len(hi)}) | {mean([hard(r) for r in lo]):.2f} | {mean([hard(r) for r in hi]):.2f} |")
# spearman over models
def rank(v):
    s = sorted(range(len(v)), key=lambda i: v[i]); r = [0]*len(v)
    for k, i in enumerate(s): r[i] = k
    return r
a = rank([p[0] for p in pts]); b = rank([p[1] for p in pts]); n = len(a)
rho = 1 - 6 * sum((x - y) ** 2 for x, y in zip(a, b)) / (n * (n * n - 1))
print(f"\nSpearman rho across the 7 models, median thinking tokens vs GT-proxy hits/run: {rho:.2f}\n")

print("## Theory test B: search scope. Repo files touched per run, split into files the plan names and files it does not\n")
print("| model | plan-named files/run | not-plan-named files/run | share of runs touching any not-plan-named test file | share touching test_worker_contract.py (DE) | share touching CHANGELOG.md (DS) | DE I7 proxy hit | DS I5 proxy hit |")
print("|---|---|---|---|---|---|---|---|")
for m in ORDER:
    rs = by[m]
    pn = mean([len(r["plan_named_opened"]) for r in rs]); nn = mean([len(set(r["repo_files"]) - set(r["plan_named_opened"])) for r in rs])
    nt = sum(any(f.startswith("tests/") and f not in r["plan_named_opened"] for f in r["repo_files"]) for r in rs) / len(rs)
    de = [r for r in rs if r["pkg"] == "DE"]; ds = [r for r in rs if r["pkg"] == "DS"]
    wc = sum(any(f.endswith("test_worker_contract.py") for f in r["repo_files"]) for r in de) / len(de)
    cl = sum(any(f.endswith("CHANGELOG.md") for f in r["repo_files"]) for r in ds) / len(ds)
    print(f"| {m} | {pn:.1f} | {nn:.1f} | {100*nt:.0f}% | {100*wc:.0f}% | {100*cl:.0f}% | {100*mean(['I7' in r['gt'] for r in de]):.0f}% | {100*mean(['I5' in r['gt'] for r in ds]):.0f}% |")
# do runs that touched test_worker_contract find I7?
de = [r for r in R if r["pkg"] == "DE"]
t = [r for r in de if any(f.endswith("test_worker_contract.py") for f in r["repo_files"])]
u = [r for r in de if r not in t]
print(f"\nDE runs touching test_worker_contract.py: {len(t)} (models {dict(collections.Counter(r['model'] for r in t))}); I7 proxy hit among them {sum('I7' in r['gt'] for r in t)}/{len(t)}; among the other {len(u)} runs {sum('I7' in r['gt'] for r in u)}/{len(u)}\n")

print("## Theory test C: report shape. Volume, locality and grading\n")
print("| model | findings/run | share of runs with <=1 finding | blocking share of findings | local findings (one section, no anchor2) | category other | missing-requirement findings/run | non-blocking findings/run |")
print("|---|---|---|---|---|---|---|---|")
for m in ORDER:
    rs = by[m]; F = [f for r in rs for f in r["findings"]]
    loc = sum(len(f["secs"]) <= 1 and not f["has_anchor2"] for f in F) / len(F)
    print(f"| {m} | {mean([r['n_findings'] for r in rs]):.2f} | {100*sum(r['n_findings'] <= 1 for r in rs)/len(rs):.0f}% | {100*sum(f['blk'] for f in F)/len(F):.0f}% | {100*loc:.0f}% | {100*sum(f['cat']=='other' for f in F)/len(F):.0f}% | "
          f"{sum(f['cat']=='missing-requirement' for f in F)/len(rs):.2f} | {sum(not f['blk'] for f in F)/len(rs):.2f} |")
print("\nWithin-model: GT-proxy hits/run by findings-count tercile (low / mid / high)\n")
print("| model | low | mid | high |"); print("|---|---|---|---|")
for m in ORDER:
    rs = sorted(by[m], key=lambda r: r["n_findings"]); k = len(rs) // 3
    parts = [rs[:k], rs[k:2*k], rs[2*k:]]
    print(f"| {m} | " + " | ".join(f"{mean([anyg(r) for r in p]):.2f} (findings {mean([r['n_findings'] for r in p]):.1f})" for p in parts) + " |")

print("\n## Skill invocation (luna, grok): runs that called the sc:spec-panel Skill vs runs that did not\n")
print("| model | skill runs | findings/run (skill) | findings/run (no skill) | GT hits/run (skill) | GT hits/run (no skill) | repo files (skill) | repo files (no skill) |")
print("|---|---|---|---|---|---|---|---|")
for m in ["luna", "grok"]:
    s = [r for r in by[m] if r["used_skill"]]; n = [r for r in by[m] if not r["used_skill"]]
    print(f"| {m} | {len(s)}/{len(by[m])} | {mean([r['n_findings'] for r in s]):.2f} | {mean([r['n_findings'] for r in n]):.2f} | {mean([anyg(r) for r in s]):.2f} | {mean([anyg(r) for r in n]):.2f} | {mean([r['n_repo_files'] for r in s]):.1f} | {mean([r['n_repo_files'] for r in n]):.1f} |")
