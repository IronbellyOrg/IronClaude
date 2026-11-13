"""All valid source.md-era rows: model-presence effects on defect-rich catch / blocking / wrong blockers, plus which model sets are untried."""
import json, glob, os, itertools, collections, statistics as st
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
SH = {"claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "gpt-6-luna": "luna", "gpt-6.1-terra": "terra", "gpt-6.1-sol": "sol",
      "grok-4.7": "grok", "muse-wonder-1.0": "wonder", "muse-ember-1.0": "ember"}
ok = lambda r: (r.endswith("-src") or r.startswith("b4-") or r.endswith("-ember") or r[:1] in "egh" and r[1:2].isdigit()
                or r in ("sol-alone-src", "terra-alone-src")) and "contaminated" not in r and "superseded" not in r and "quarantine" not in r
rows = []
for row in sorted(os.listdir(f"{E}/combos")):
    if not ok(row): continue
    sc = {p: glob.glob(f"{E}/arms/scoring/combos/{row}/{p}/*/score.json") for p in (DS, AL, DE)}
    if not all(sc.values()): continue
    S = {p: json.load(open(v[0])) for p, v in sc.items()}
    models = []
    for mf in sorted(glob.glob(f"{E}/{DS}/reviews/combos/{row}/t*.meta.json")):
        if "attempt" in mf: continue
        models.append(SH.get(json.load(open(mf))["expected_model"], "?"))
    any_ = sum(len(S[p]["gt_covered_any"]) for p in (DS, AL)); blk = sum(len(S[p]["gt_covered_blocking"]) for p in (DS, AL))
    wb = sum(S[p]["wrong_blockers"] for p in (DS, AL)); ctl = len(S[DE]["gt_covered_any"]); cwb = S[DE]["wrong_blockers"]
    tok = 0
    for p in (DS, AL, DE):
        for cf in glob.glob(f"{E}/{p}/reviews/combos/{row}/t*.cost.json"): tok += json.load(open(cf))["total_output_tokens_all"]
    rows.append(dict(row=row, models=tuple(sorted(models)), any=any_, blk=blk, wb=wb, ctl=ctl, cwb=cwb, tok=tok))
print("rows:", len(rows), "distinct model multisets:", len({r["models"] for r in rows}))
fam = collections.defaultdict(list)
for r in rows: fam[r["models"]].append(r)
print("\nPER-MODEL presence effect (rows with vs without), defect-rich found /14, blocking /8, wrong blockers, control /2")
for m in ("sonnet", "haiku", "grok", "luna", "terra", "sol", "ember", "wonder"):
    w = [r for r in rows if m in r["models"]]; wo = [r for r in rows if m not in r["models"]]
    f = lambda L, k: (st.mean(x[k] for x in L) if L else float("nan"))
    print(f"{m:7s} with n={len(w):2d} any={f(w,'any'):.2f} blk={f(w,'blk'):.2f} wb={f(w,'wb'):.2f} ctl={f(w,'ctl'):.2f} | without n={len(wo):2d} any={f(wo,'any'):.2f} blk={f(wo,'blk'):.2f} wb={f(wo,'wb'):.2f} ctl={f(wo,'ctl'):.2f}")
print("\nTOP rows by defect-rich found (then blocking):")
for r in sorted(rows, key=lambda r: (-r["any"], -r["blk"], r["wb"]))[:10]:
    print(f"  {r['row']:28s} {'+'.join(r['models']):40s} any={r['any']} blk={r['blk']} wb={r['wb']} ctl={r['ctl']} tok={r['tok']:,}")
print("\nrows with blocking >=3:", [(r["row"], r["blk"]) for r in rows if r["blk"] >= 3])
print("rows with control 2/2:", [(r["row"]) for r in rows if r["ctl"] == 2])
pool = ["sonnet", "haiku", "grok", "luna", "terra", "sol", "ember"]
tried = {r["models"] for r in rows}
print("\nUNTRIED 2-model and 3-model sets from the available pool (multisets, no repeats):")
for k in (2, 3):
    print(f" size {k}:", [" + ".join(c) for c in itertools.combinations(sorted(pool), k) if tuple(sorted(c)) not in tried])
print("tried multisets with sonnet:", sorted("+".join(m) for m in tried if "sonnet" in m))
print("tried multisets with grok:", sorted("+".join(m) for m in tried if "grok" in m))
print("tried multisets with sol:", sorted("+".join(m) for m in tried if "sol" in m))
print("\nhard ceiling: DR any per row max =", max(r["any"] for r in rows), "; DR any distribution:", sorted(collections.Counter(r["any"] for r in rows).items()))
