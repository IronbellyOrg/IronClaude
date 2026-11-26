"""For each panel containing 2 reviewers of the same model (defect-rich pkgs): GT caught by run A, run B, union, overlap, wrong blockers."""
import json, collections
a = json.load(open("/tmp/attrib.json"))
g = collections.defaultdict(list)
for row, p, rid, mod, ga, gb, w in a:
    if p != "DE": g[(row, p, mod)].append((rid, set(ga), set(gb), w))
agg = collections.defaultdict(lambda: dict(n=0, a=0, b=0, uni=0, ov=0, gain=0, wb=0, bestsingle=0))
print("row pkg model | runA runB | union overlap | wb(A,B)")
for (row, p, mod), rs in sorted(g.items()):
    if len(rs) < 2: continue
    (r1, a1, b1, w1), (r2, a2, b2, w2) = rs[0], rs[1]
    u = a1 | a2
    print(f"{row:22s} {p} {mod:6s} | {sorted(a1)} {sorted(a2)} | union={len(u)} overlap={len(a1&a2)} | wb {w1},{w2}")
    s = agg[mod]; s["n"] += 1; s["a"] += len(a1); s["b"] += len(a2); s["uni"] += len(u); s["ov"] += len(a1 & a2)
    s["bestsingle"] += max(len(a1), len(a2)); s["gain"] += len(u) - max(len(a1), len(a2)); s["wb"] += w1 + w2
print("\nmodel | doubled panel-pkgs | avg GT per single run | avg union | gain of 2nd run over best single (total) | overlap total | wrong blockers total")
for m, s in agg.items():
    print(f"{m}: panels={s['n']} avg_single={(s['a']+s['b'])/(2*s['n']):.2f} avg_union={s['uni']/s['n']:.2f} gain_total={s['gain']} (per panel {s['gain']/s['n']:.2f}) overlap={s['ov']} wb={s['wb']}")
