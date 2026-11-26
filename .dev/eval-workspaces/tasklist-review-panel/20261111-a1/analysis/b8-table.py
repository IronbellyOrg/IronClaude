"""Final replicate table: per family mean (range) over runs, wall/tokens, and 2x-vs-1x deltas. Reads judge score.json + reviewer cost.json."""
import json, glob, os, math, statistics as st, re
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
PKGS = [DS, AL, DE]
def rows_g(n): return [f"{n}-r{i}" for i in range(1, 5)]
FAM = [  # (family label, models, doubled-note, rows)
 ("ember + luna (1x baseline)", "ember, luna", "-", rows_g("g9-ember-luna")),
 ("ember + 2x luna", "ember, luna x2", "luna 2x", rows_g("g1-ember-luna2") + ["b4-muse-ember-luna2", "e2-ember-luna2-rep"]),
 ("2x ember + luna", "ember x2, luna", "ember 2x", rows_g("g5-ember2-luna") + ["e3-ember2-luna"]),
 ("2x luna + 2x ember", "luna x2, ember x2", "luna 2x, ember 2x", rows_g("g6-luna2-ember2")),
 ("ember + terra", "ember, terra", "-", rows_g("g8-ember-terra")),
 ("sonnet + ember", "sonnet, ember", "-", rows_g("g2-sonnet-ember")),
 ("sonnet + luna + ember", "sonnet, luna, ember", "-", rows_g("g3-sonnet-luna-ember") + ["n5-sonnet-ember"]),
 ("haiku + ember + terra", "haiku, ember, terra", "-", rows_g("g4-haiku-ember-terra") + ["terra-muse-haiku-ember"]),
 ("haiku + 2x luna", "haiku, luna x2", "luna 2x (no 1x baseline)", rows_g("g7-haiku-luna2") + ["r1-haiku-luna2-src"]),
 ("(ref, single run) grok + ember + luna", "grok, ember, luna", "-", ["e1-grok-ember-luna"]),
 ("(ref, single run) haiku + ember + luna", "haiku, ember, luna", "-", ["e5-haiku-ember-luna"]),
 ("(ref, single run) haiku + 2x ember", "haiku, ember x2", "ember 2x", ["e6-haiku-ember2"]),
]
def score(row, p):
    fs = glob.glob(f"{E}/arms/scoring/combos/{row}/{p}/*/score.json")
    return json.load(open(fs[0])) if fs else None
def cost(row, p):
    cs = [json.load(open(f)) for f in glob.glob(f"{E}/{p}/reviews/combos/{row}/t*.cost.json")]
    return sum(c["total_output_tokens_all"] for c in cs), sum(c["total_wall_s"] for c in cs), max(c["total_wall_s"] for c in cs)
def rowstats(row):
    a = b = w = tok = rs = el = 0; ca = cb = cw = 0
    for p in PKGS:
        s = score(row, p)
        if s is None: return None
        t, ws, mx = cost(row, p); tok += t; rs += ws; el += mx
        n_any, n_blk, wb = len(s["gt_covered_any"]), len(s["gt_covered_blocking"]), s["wrong_blockers"]
        if p == DE: ca, cb, cw = n_any, n_blk, wb
        else: a += n_any; b += n_blk; w += wb
    return dict(any=a, blk=b, wb=w, cany=ca, cblk=cb, cwb=cw, tok=tok, rsec=rs, el=el)
def agg(rows):
    R = [r for r in (rowstats(x) for x in rows) if r]
    f = lambda k: [r[k] for r in R]
    m = lambda k: sum(f(k)) / len(R)
    return dict(n=len(R), R=R, any=m("any"), anyr=(min(f("any")), max(f("any"))), blk=m("blk"), blkr=(min(f("blk")), max(f("blk"))), wb=m("wb"),
                cany=m("cany"), cblk=m("cblk"), cwb=m("cwb"), tok=m("tok"), rsec=m("rsec"), el=m("el"),
                sd_any=(st.stdev(f("any")) if len(R) > 1 else float("nan")), sd_blk=(st.stdev(f("blk")) if len(R) > 1 else float("nan")),
                sd_cany=(st.stdev(f("cany")) if len(R) > 1 else float("nan")))
out = []
A = {fam[0]: agg(fam[3]) for fam in FAM}
out.append("| Combo | Models | 2x model | Runs | Defect-rich found /14 mean (range) | Blocking /8 mean (range) | Wrong blockers (DR) | Control found /2 | Control wrong blk | Tokens (mean) | Wall: reviewer-s summed / elapsed s |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|")
for lab, models, dbl, rows in FAM:
    a = A[lab]
    if a["n"] == 0: out.append(f"| {lab} | {models} | {dbl} | 0 | not scored | | | | | | |"); continue
    out.append(f"| {lab} | {models} | {dbl} | {a['n']} | {a['any']:.1f} ({a['anyr'][0]}-{a['anyr'][1]}) | {a['blk']:.1f} ({a['blkr'][0]}-{a['blkr'][1]}) | {a['wb']:.1f} | {a['cany']:.2f} | {a['cwb']:.2f} | {a['tok']:,.0f} | {a['rsec']:,.0f} / {a['el']:,.0f} |")
def delta(lab2, lab1, why):
    x, y = A[lab2], A[lab1]
    if x["n"] == 0 or y["n"] == 0: return f"| {why} | n/a | | | | | |"
    def d(k, sdk):
        dv = x[k] - y[k]
        se = math.sqrt((x[sdk] ** 2 / x["n"] if x["n"] > 1 else 0) + (y[sdk] ** 2 / y["n"] if y["n"] > 1 else 0))
        flag = "within noise" if abs(dv) < 2 * se else "beyond noise"
        return f"{dv:+.2f} ({flag})"
    return (f"| {why} | {x['n']} vs {y['n']} | {d('any','sd_any')} | {d('blk','sd_blk')} | {x['wb']-y['wb']:+.1f} | {d('cany','sd_cany')} | "
            f"{x['tok']-y['tok']:+,.0f} | {x['rsec']-y['rsec']:+,.0f} / {x['el']-y['el']:+,.0f} |")
out2 = ["| Doubling vs the 1x baseline (ember + luna) | Runs (2x vs 1x) | Delta defect-rich found | Delta blocking | Delta wrong blockers | Delta control found | Delta tokens | Delta wall (reviewer-s / elapsed) |", "|---|---|---|---|---|---|---|---|"]
out2.append(delta("ember + 2x luna", "ember + luna (1x baseline)", "2nd luna (ember + luna x2 vs ember + luna)"))
out2.append(delta("2x ember + luna", "ember + luna (1x baseline)", "2nd ember (ember x2 + luna vs ember + luna)"))
out2.append(delta("2x luna + 2x ember", "ember + luna (1x baseline)", "2nd luna AND 2nd ember"))
out2.append(delta("2x luna + 2x ember", "ember + 2x luna", "2nd ember on top of 2x luna"))
out2.append(delta("2x luna + 2x ember", "2x ember + luna", "2nd luna on top of 2x ember"))
# reviewer-level control GT2 proxy: does at least one reviewer of model M raise the single_select/option-name read-back defect
pat = re.compile(r"single_select_option|option (name|id)|numeric (option )?id|value.*name.*(select|option)|read-?back.*(name|id)", re.I)
def block(f):
    t = open(f).read(); m = re.search(r"```findings-v1\n(.*?)```", t, re.S); return m.group(1) if m else ""
def hitrate(rows, model):
    hits = panels = 0
    for r in rows:
        d = f"{E}/{DE}/reviews/combos/{r}"; got = []
        for mf in glob.glob(f"{d}/t*.meta.json"):
            if "attempt" in mf: continue
            if json.load(open(mf))["expected_model"] == model: got.append(bool(pat.search(block(mf.replace(".meta.json", ".md")))))
        if got: panels += 1; hits += any(got)
    return hits, panels
out3 = ["| Model | 1x panels: at least one reviewer raises control GT2 | 2x panels: at least one of the two raises it |", "|---|---|---|"]
h1, n1 = hitrate(FAM[0][3], "gpt-6-luna"); h2, n2 = hitrate(FAM[1][3], "gpt-6-luna")
out3.append(f"| luna | {h1}/{n1} | {h2}/{n2} |")
h1, n1 = hitrate(FAM[0][3], "muse-ember-1.0"); h2, n2 = hitrate(FAM[2][3], "muse-ember-1.0")
out3.append(f"| ember | {h1}/{n1} | {h2}/{n2} |")
open("/tmp/b8-final.md", "w").write("\n".join(out) + "\n\n" + "\n".join(out2) + "\n\n" + "\n".join(out3) + "\n")
print(open("/tmp/b8-final.md").read())
