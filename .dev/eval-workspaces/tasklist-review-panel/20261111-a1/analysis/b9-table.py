"""Batch 9 table: h1/h2 families vs the 2x luna + 2x ember (g6) and haiku/sonnet reference families. Reuses b8-table.py helpers."""
import math, json, glob, re
src = open("/tmp/b8-table.py").read().split("out = []")[0]
exec(src)
def rg(n, k=4): return [f"{n}-r{i}" for i in range(1, k + 1)]
FAM2 = [
 ("2x luna + 2x ember (g6)", "luna x2, ember x2", rg("g6-luna2-ember2")),
 ("haiku + 2x luna + 2x ember (h1)", "haiku, luna x2, ember x2", rg("h1-haiku-luna2-ember2")),
 ("sonnet + 2x luna + 2x ember (h2)", "sonnet, luna x2, ember x2", rg("h2-sonnet-luna2-ember2")),
 ("(ref) haiku + 2x luna", "haiku, luna x2", rg("g7-haiku-luna2") + ["r1-haiku-luna2-src"]),
 ("(ref) sonnet + ember", "sonnet, ember", rg("g2-sonnet-ember")),
 ("(ref) sonnet + luna + ember", "sonnet, luna, ember", rg("g3-sonnet-luna-ember") + ["n5-sonnet-ember"]),
 ("(ref) ember + luna", "ember, luna", rg("g9-ember-luna")),
]
A2 = {f[0]: agg(f[2]) for f in FAM2}
L = ["| Combo | Models | Runs | Defect-rich found /14 mean (range) | Blocking /8 mean (range) | Wrong blockers (DR) | Control found /2 | Control wrong blk | Tokens (mean) | Wall: reviewer-s summed / elapsed s | Found per 100k tokens |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for lab, models, rows in FAM2:
    a = A2[lab]
    if not a["n"]: L.append(f"| {lab} | {models} | 0 | not scored | | | | | | | |"); continue
    L.append(f"| {lab} | {models} | {a['n']} | {a['any']:.1f} ({a['anyr'][0]}-{a['anyr'][1]}) | {a['blk']:.1f} ({a['blkr'][0]}-{a['blkr'][1]}) | {a['wb']:.1f} | {a['cany']:.2f} | {a['cwb']:.2f} | {a['tok']:,.0f} | {a['rsec']:,.0f} / {a['el']:,.0f} | {100000*a['any']/a['tok']:.1f} |")
def dl(l2, l1, why):
    x, y = A2[l2], A2[l1]
    if not x["n"] or not y["n"]: return f"| {why} | n/a |"
    def d(k, sdk):
        dv = x[k] - y[k]; se = math.sqrt((x[sdk] ** 2 / x["n"]) + (y[sdk] ** 2 / y["n"]))
        return f"{dv:+.2f} ({'within noise' if abs(dv) < 2 * se else 'beyond noise'})"
    return f"| {why} | {x['n']} vs {y['n']} | {d('any','sd_any')} | {d('blk','sd_blk')} | {x['wb']-y['wb']:+.1f} | {d('cany','sd_cany')} | {x['tok']-y['tok']:+,.0f} | {x['rsec']-y['rsec']:+,.0f} / {x['el']-y['el']:+,.0f} |"
L += ["", "| Effect of adding one reviewer | Runs | Delta defect-rich found | Delta blocking | Delta wrong blockers | Delta control found | Delta tokens | Delta wall (reviewer-s / elapsed) |", "|---|---|---|---|---|---|---|---|",
      dl("haiku + 2x luna + 2x ember (h1)", "2x luna + 2x ember (g6)", "adding haiku to 2x luna + 2x ember"),
      dl("sonnet + 2x luna + 2x ember (h2)", "2x luna + 2x ember (g6)", "adding sonnet to 2x luna + 2x ember"),
      dl("sonnet + 2x luna + 2x ember (h2)", "(ref) sonnet + luna + ember", "2nd luna + 2nd ember on top of sonnet + luna + ember"),
      dl("sonnet + 2x luna + 2x ember (h2)", "(ref) sonnet + ember", "2x luna + 1 more ember on top of sonnet + ember"),
      dl("haiku + 2x luna + 2x ember (h1)", "(ref) haiku + 2x luna", "2x ember on top of haiku + 2x luna"),
      dl("haiku + 2x luna + 2x ember (h1)", "sonnet + 2x luna + 2x ember (h2)" if False else "(ref) haiku + 2x luna", "(dup) see above")]
L = [x for x in L if "(dup)" not in x]
open("/tmp/b9-final.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
