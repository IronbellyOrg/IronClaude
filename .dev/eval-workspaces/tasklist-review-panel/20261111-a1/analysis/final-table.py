"""FINAL table: valid-era rows grouped by reviewer-model multiset, two views:
  AS-SCORED  = every valid-era row-package with a score
  AUDIT-CLEAN = row-packages with no EXCLUDE flag of a harness/integrity type from audits A,B(incomplete/short),D,E,F
Blocking is reported two ways: JUDGE (gt_covered_blocking as recorded) and REAL (judge-blocking AND the GT item has blocking_in_implement=true).
Per-package means are summed across the two defect-rich packages (designSpec /10 GT, alias /4 GT; real-blocking /5 + /3)."""
import json, glob, os, csv, collections, statistics as st, itertools, random, sys
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
PK = [DS, AL, DE]
SH = {"claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "gpt-6-luna": "luna", "gpt-6.1-terra": "terra", "gpt-6.1-sol": "sol", "grok-4.7": "grok", "muse-wonder-1.0": "wonder", "muse-ember-1.0": "ember"}
def valid(r):
    return ((r.endswith("-src") or r.startswith("b4-") or r.endswith("-ember") or (r[:1] in "egh" and r[1:2].isdigit()) or r in ("sol-alone-src", "terra-alone-src"))
            and not any(x in r for x in ("contaminated", "superseded", "quarantine", "invalid")) and not r.startswith(("i1-", "i2-")))
GT = {p: {i["id"]: i["blocking_in_implement"] for i in json.load(open(f"{E}/{p}/ground-truth.json"))["items"]} for p in PK}
def fullpkg(s):
    for p in PK:
        if p.startswith(s) or s.startswith(p[:12]) and p.startswith(s[:12]): return p
    return None
# exclusion flags
BAD_CHECKS = {"A": None, "B": ("1-incomplete", "1-short"), "D": ("2-blockok", "3-conserve", "3-dropped-blocking", "1-path", "5-stale"), "E": None, "F": ("3-completeness",)}
excl = collections.defaultdict(set)  # (row,pkg) -> reasons
for k, chk in BAD_CHECKS.items():
    f = f"/tmp/audit-{k}/flags.tsv"
    if not os.path.exists(f): continue
    for i, line in enumerate(open(f)):
        c = line.rstrip("\n").split("\t")
        if i == 0 or len(c) < 6 or c[4] != "EXCLUDE": continue
        if chk and c[0] not in chk: continue
        pk = fullpkg(c[2]); pkgs = [pk] if pk else PK
        for p in pkgs: excl[(c[1], p)].add(f"{k}:{c[0]}")
def metrics(row, p, S):
    s = S
    anyl = s["gt_covered_any"]; jb = s["gt_covered_blocking"]
    rb = [g for g in jb if GT[p].get(g)]
    cost = [json.load(open(f)) for f in glob.glob(f"{E}/{p}/reviews/combos/{row}/t*.cost.json")]
    return dict(any=len(anyl), jb=len(jb), rb=len(rb), wb=s["wrong_blockers"], tok=sum(c["total_output_tokens_all"] for c in cost),
                rs=sum(c["total_wall_s"] for c in cost), el=max(c["total_wall_s"] for c in cost) if cost else 0)
rows = {}
for row in sorted(os.listdir(f"{E}/combos")):
    if not valid(row): continue
    models = []
    for mf in sorted(glob.glob(f"{E}/{DS}/reviews/combos/{row}/t*.meta.json")):
        if "attempt" in mf: continue
        models.append(SH.get(json.load(open(mf))["expected_model"], "?"))
    d = {}
    for p in PK:
        sf = glob.glob(f"{E}/arms/scoring/combos/{row}/{p}/*/score.json")
        if sf: d[p] = metrics(row, p, json.load(open(sf[0])))
    if d: rows[row] = (tuple(sorted(models)), d)
def fam_stats(view):
    fam = collections.defaultdict(lambda: {p: [] for p in PK})
    nrows = collections.Counter()
    for row, (models, d) in rows.items():
        for p, m in d.items():
            if view == "clean" and (row, p) in excl: continue
            fam[models][p].append(m)
    out = {}
    for models, by in fam.items():
        def mean(p, k): return st.mean(x[k] for x in by[p]) if by[p] else float("nan")
        n = {p: len(by[p]) for p in PK}
        if min(n[DS], n[AL]) == 0: continue
        any_ = mean(DS, "any") + mean(AL, "any"); rb = mean(DS, "rb") + mean(AL, "rb"); jb = mean(DS, "jb") + mean(AL, "jb"); wb = mean(DS, "wb") + mean(AL, "wb")
        tok = sum(mean(p, "tok") for p in PK if n[p]); rs = sum(mean(p, "rs") for p in PK if n[p]); el = sum(mean(p, "el") for p in PK if n[p])
        ctl = mean(DE, "any") if n[DE] else float("nan"); cwb = mean(DE, "wb") if n[DE] else float("nan")
        sd_any = st.pstdev([x["any"] for x in by[DS]]) if n[DS] > 1 else float("nan")
        out[models] = dict(n=n, any=any_, rb=rb, jb=jb, wb=wb, ctl=ctl, cwb=cwb, tok=tok, rs=rs, el=el)
    return out
def table(view, minn):
    S = fam_stats(view)
    L = ["| Panel | Runs DS/AL/ctl | Found /14 | Real blocking /8 | Judge-blocking | Wrong blockers (DR) | Control found /2 | Ctl wrong blk | Tokens | Wall rev-s / elapsed s | Found per 100k tok | Real-blk per 100k tok |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    keys = sorted([k for k, v in S.items() if min(v["n"][DS], v["n"][AL]) >= minn], key=lambda k: (-S[k]["any"], -S[k]["rb"]))
    for k in keys:
        v = S[k]; n = v["n"]
        L.append(f"| {' + '.join(k)} | {n[DS]}/{n[AL]}/{n[DE]} | {v['any']:.2f} | {v['rb']:.2f} | {v['jb']:.2f} | {v['wb']:.2f} | {v['ctl']:.2f} | {v['cwb']:.2f} | {v['tok']:,.0f} | {v['rs']:,.0f} / {v['el']:,.0f} | {100000*v['any']/v['tok']:.2f} | {100000*v['rb']/v['tok']:.2f} |")
    return "\n".join(L), S
asd, S_all = table("all", 1)
cln, S_cln = table("clean", 1)
nex = sum(1 for (r, p) in excl if r in rows and p in rows[r][1]); tot = sum(len(d) for _, d in rows.values())
hdr = f"valid-era rows: {len(rows)}; row-packages scored: {tot}; row-packages carrying an audit EXCLUDE flag (A,B incomplete/short,D,E,F): {nex}"
open("/tmp/final-table.md", "w").write(hdr + "\n\n### AS SCORED (all valid-era row-packages)\n" + asd + "\n\n### AUDIT-CLEAN (row-packages with no EXCLUDE flag)\n" + cln + "\n")
json.dump({",".join(k): v for k, v in S_cln.items()}, open("/tmp/final-clean.json", "w"), indent=1)
json.dump({",".join(k): v for k, v in S_all.items()}, open("/tmp/final-all.json", "w"), indent=1)
print(open("/tmp/final-table.md").read())
