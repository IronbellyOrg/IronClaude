"""Per-run detail + tests for: sonnet+2luna (b4-sonnet-luna2), ember+2luna (g1 x4, b4-muse-ember-luna2, e2 rep), sonnet+luna+ember (g3 x4, n5-sonnet-ember),
plus sonnet+2luna+2ember (h2 x4) as the nearest tried relative of 'sonnet + 2x luna + ember'."""
import json, glob, os, itertools, random, statistics as st, collections, csv, re
exec(open("/tmp/final-table.py").read().split("rows = {}")[0])  # reuse helpers: E, PK, DS, AL, DE, GT, excl, metrics, SH
FAM = {
 "sonnet + 2x luna": ["b4-sonnet-luna2", "j1-sonnet-luna2-r1", "j1-sonnet-luna2-r2", "j1-sonnet-luna2-r3", "j1-sonnet-luna2-r4", "j1-sonnet-luna2-r5"],
 "ember + 2x luna": ["g1-ember-luna2-r1", "g1-ember-luna2-r2", "g1-ember-luna2-r3", "g1-ember-luna2-r4", "b4-muse-ember-luna2", "e2-ember-luna2-rep"],
 "sonnet + luna + ember": ["g3-sonnet-luna-ember-r1", "g3-sonnet-luna-ember-r2", "g3-sonnet-luna-ember-r3", "g3-sonnet-luna-ember-r4", "n5-sonnet-ember"],
 "sonnet + 2x luna + 2x ember (h2)": ["h2-sonnet-luna2-ember2-r1", "h2-sonnet-luna2-ember2-r2", "h2-sonnet-luna2-ember2-r3", "h2-sonnet-luna2-ember2-r4"],
}
def run(row):
    d = {}
    for p in PK:
        sf = glob.glob(f"{E}/arms/scoring/combos/{row}/{p}/*/score.json")
        if sf: d[p] = metrics(row, p, json.load(open(sf[0])))
    if len(d) < 3: return None
    return dict(any=d[DS]["any"] + d[AL]["any"], rb=d[DS]["rb"] + d[AL]["rb"], jb=d[DS]["jb"] + d[AL]["jb"], wb=d[DS]["wb"] + d[AL]["wb"],
                ctl=d[DE]["any"], cwb=d[DE]["wb"], tok=sum(x["tok"] for x in d.values()), el=sum(x["el"] for x in d.values()), rs=sum(x["rs"] for x in d.values()),
                flagged=[p[:8] for p in PK if (row, p) in excl])
R = {f: {r: run(r) for r in rows} for f, rows in FAM.items()}
for f, rs in R.items():
    print(f"\n== {f}")
    print("row | DR found | real blk | judge blk | wrong blk | ctl found | ctl wb | tokens | elapsed s | audit-flagged pkgs")
    for r, m in rs.items():
        if m: print(f"{r} | {m['any']} | {m['rb']} | {m['jb']} | {m['wb']} | {m['ctl']} | {m['cwb']} | {m['tok']:,} | {m['el']:.0f} | {m['flagged']}")
    ms = [m for m in rs.values() if m]
    if ms:
        for k in ("any", "rb", "wb", "ctl", "cwb", "tok", "el"):
            v = [m[k] for m in ms]
            print(f"  {k}: mean {st.mean(v):.2f} sd {st.pstdev(v):.2f} min {min(v)} max {max(v)}")
        print(f"  flagged row-packages: {sum(len(m['flagged']) for m in ms)} of {3*len(ms)}")
# tests: ember+2luna vs sonnet+luna+ember, and vs h2
def perm(a, b, n=20000, seed=1):
    random.seed(seed); obs = abs(st.mean(a) - st.mean(b)); pool = a + b; c = 0
    for _ in range(n):
        random.shuffle(pool); x, y = pool[:len(a)], pool[len(a):]
        if abs(st.mean(x) - st.mean(y)) >= obs - 1e-12: c += 1
    return c / n
def vals(f, k): return [m[k] for m in R[f].values() if m]
print("\nPERMUTATION p (two-sided) on run-level values")
for a, b in (("sonnet + 2x luna", "ember + 2x luna"), ("sonnet + 2x luna", "sonnet + luna + ember"), ("sonnet + 2x luna", "sonnet + 2x luna + 2x ember (h2)"), ("ember + 2x luna", "sonnet + luna + ember")):
    for k in ("any", "rb", "wb", "ctl", "cwb", "tok", "el"):
        A, B = vals(a, k), vals(b, k)
        print(f"{a} vs {b} | {k}: {st.mean(A):.2f} vs {st.mean(B):.2f} p={perm(A, B):.3f}")
# reviewer-level quality in these rows: dropped findings (block ok false) and source.md reads
print("\nREVIEWER-LEVEL in these rows (by model): runs, block-ok-false (findings dropped by merge), never-referenced-source.md")
nosrc = collections.defaultdict(set)
for line in open("/tmp/audit-C/flags.tsv"):
    c = line.rstrip("\n").split("\t")
    if len(c) >= 6 and c[0] == "2-nosrc": nosrc[(c[1], c[2][:14], c[3])].add(1)
dropped = collections.defaultdict(set)
for line in open("/tmp/audit-D/flags.tsv"):
    c = line.rstrip("\n").split("\t")
    if len(c) >= 6 and c[0] == "2-blockok": dropped[(c[1], c[2][8:22] if c[2].startswith("TASK-WF-") else c[2][:14], c[3])].add(1)
for f, rws in FAM.items():
    cnt = collections.defaultdict(lambda: [0, 0, 0])
    for r in rws:
        for p in PK:
            for mf in glob.glob(f"{E}/{p}/reviews/combos/{r}/t*.meta.json"):
                if "attempt" in mf: continue
                m = json.load(open(mf)); mod = SH.get(m["expected_model"], "?"); rid = m["reviewer_id"]
                c = cnt[mod]; c[0] += 1; c[1] += (r, p[8:22], rid) in dropped; c[2] += (r, p[8:22], rid) in nosrc
    print(f"{f}: " + "; ".join(f"{m} runs {v[0]} dropped {v[1]} nosrc {v[2]}" for m, v in cnt.items()))
