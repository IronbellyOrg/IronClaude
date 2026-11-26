"""Variant 3 arithmetic: planning bands only; no run data, no ground truth. Exact binomial, independent trials (ignores clustering)."""
from math import comb, sqrt

BANDS = {"C1": (.10, .40), "C2": (.20, .45), "C3": (.03, .15), "C4": (.50, .75),
         "C5": (.35, .60), "C6": (.05, .30), "C7": (.15, .35), "C8": (.40, .65)}
# s ranges per class from MR 3.1(d) (C1, C6: union of the two rows)
S = {"C1": (.35, .70), "C2": (.40, .70), "C3": (.25, .50), "C4": (.80, .95),
     "C5": (.65, .90), "C6": (.35, .70), "C7": (.40, .65), "C8": (.85, .95)}


def pmf(n, p):
    return [comb(n, k) * p**k * (1 - p)**(n - k) for k in range(n + 1)]


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0, c - h), min(1, c + h)


def p_point_in(n, p, lo, hi):
    return sum(w for k, w in enumerate(pmf(n, p)) if lo - 1e-12 <= k / n <= hi + 1e-12)


def p_wholly_outside(n, p, lo, hi):
    """P(95% Wilson (z=1.96, as analyze.py WILSON_Z) interval lies wholly below lo or wholly above hi)."""
    tot = 0
    for k, w in enumerate(pmf(n, p)):
        a, b = wilson(k, n)
        if b < lo or a > hi:
            tot += w
    return tot


print("1. Rule 'wholly outside' flag rate, truth at band midpoint (false alarm), n = 10 / 15 / 18 / 30")
fa = {n: 1.0 for n in (10, 15, 18, 30)}
for c, (lo, hi) in BANDS.items():
    m = (lo + hi) / 2
    r = [p_wholly_outside(n, m, lo, hi) for n in (10, 15, 18, 30)]
    for n, v in zip((10, 15, 18, 30), r):
        fa[n] *= (1 - v)
    print(c, " ".join(f"n={n}:{v:.3f}" for n, v in zip((10, 15, 18, 30), r)))
print("P(no class flagged | all truths at midpoint):", {n: round(v, 3) for n, v in fa.items()})

print("\n2. Same rule, truth one full band-width below lo / above hi (clamped to [0.01,0.99])")
for c, (lo, hi) in BANDS.items():
    w = hi - lo
    lowt, hit = max(.01, lo - w), min(.99, hi + w)
    print(c, f"low-truth {lowt:.2f}:", " ".join(f"n={n}:{p_wholly_outside(n, lowt, lo, hi):.2f}" for n in (10, 18, 30)),
          f"| high-truth {hit:.2f}:", " ".join(f"n={n}:{p_wholly_outside(n, hit, lo, hi):.2f}" for n in (10, 18, 30)))

print("\n3. Default band, literal unconditional act (stage_rows: not-selected = no act) when the planning model is exactly right")
print("   expected unconditional rate = act_mid x s_mid; P(point inside band) and P(wholly below) at n=10 / 18")
for c, (lo, hi) in BANDS.items():
    m = (lo + hi) / 2
    s = sum(S[c]) / 2
    u = m * s
    print(c, f"band {lo:.2f}-{hi:.2f} act_mid {m:.3f} s_mid {s:.3f} -> expected {u:.3f}",
          f"inside:{p_point_in(10, u, lo, hi):.2f}/{p_point_in(18, u, lo, hi):.2f}",
          f"wholly-below:{p_wholly_outside(10, u, lo, hi):.2f}/{p_wholly_outside(18, u, lo, hi):.2f}")

print("\n4. Pooled band 0.223-0.456 (equal class weights) with an unregistered class mix: expected pooled rate if the mix is all-C4 / all-C3 / even")
mids = {c: (lo + hi) / 2 for c, (lo, hi) in BANDS.items()}
print("even mix", round(sum(mids.values()) / 8, 3), "| C4-heavy (50% C4, rest even)", round(.5 * mids["C4"] + .5 * (sum(mids.values()) - mids["C4"]) / 7, 3),
      "| C3,C6,C1 only (even)", round((mids["C3"] + mids["C6"] + mids["C1"]) / 3, 3))
