"""Uniform rescoring of every arm with central/score_themes.blocking_findings; permutation test of per-run mean blockers vs the fresh baseline."""
import sys, pathlib, json, random, statistics as S
sys.path.insert(0, 'central'); import score_themes as sc
A = '.dev/orca-command-refactor/review/audit.md'
def blk(p): p = pathlib.Path(p); return len(sc.blocking_findings(p)) if p.exists() else None
def runs(base, pre, n, subs=('aud', 'aud2')):
    out = {}
    for i in range(1, n + 1):
        r = f"{pre}{i}"; out[r] = [blk(f"{base}/{r}/{s}/ws/{A}") for s in subs]
    return out
arms = {
 'stored baseline (Stage 2 a3)': {f'a3-r{i}': [blk(f'p11/runs/a3-r{i}/aud/ws/{A}'), blk(f'p12/baseline-audit2/a3-r{i}/ws/{A}')] for i in range(1, 7)},
 'FRESH baseline (a3, now)': runs('p16/base-drift/runs', 'a3d-r', 6),
 'ab1 k=3 union+verify (replayed)': runs('p12/ab1/runs', 'b1-r', 6),
 'ab2 verify gate k=1': runs('p12/ab2/runs', 'b2-r', 6),
 'ab3 final gate': runs('p12/ab3/runs', 'b3-r', 6),
 'PN1 panel+merge+ledger': runs('p13/ab1/runs', 'b1-r', 6),
 'PN2 mechanical lint': runs('p13/ab2/runs', 'l2-r', 6),
 'ab4 lint+k2(AC sweep)+verify': runs('p16/ab4/runs', 'd4-r', 6),
 'HAIKU baseline': runs('p14/haiku-baseline/runs', 'a3-r', 6),
 'HAIKU ab1': runs('p12/ab1/runs', 'b1h-r', 4),
 'HAIKU ab2': runs('p12/ab2/runs', 'b2h-r', 4),
 'HAIKU ab3': runs('p12/ab3/runs', 'b3h-r', 4),
 'HAIKU ab4': runs('p16/ab4/runs', 'd4h-r', 4),
}
def runmeans(d): return [sum(v) / len(v) for v in ([x for x in vs if x is not None] for vs in d.values()) if v]
def perm(a, b, it=20000, seed=1):
    random.seed(seed); obs = S.mean(a) - S.mean(b); pool = a + b; k = 0
    for _ in range(it):
        random.shuffle(pool)
        if abs(S.mean(pool[:len(a)]) - S.mean(pool[len(a):])) >= abs(obs) - 1e-12: k += 1
    return k / it
res = {}
fresh = runmeans(arms['FRESH baseline (a3, now)']); hb = runmeans(arms['HAIKU baseline'])
for name, d in arms.items():
    vals = [x for vs in d.values() for x in vs if x is not None]
    rm = runmeans(d); ref = hb if name.startswith('HAIKU') else fresh
    p = None if name in ('FRESH baseline (a3, now)', 'HAIKU baseline') else perm(rm, ref)
    res[name] = {'n_runs': len(rm), 'n_audits': len(vals), 'BLK': round(S.mean(vals), 3), 'sd': round(S.stdev(vals), 2) if len(vals) > 1 else None, 'p_vs_ref': p}
    print(f"{name:34s} runs {len(rm)} audits {len(vals):2d} BLK {S.mean(vals):.2f} sd {res[name]['sd']}  p_vs_ref {p}")
json.dump(res, open('final_score.json', 'w'), indent=1)
