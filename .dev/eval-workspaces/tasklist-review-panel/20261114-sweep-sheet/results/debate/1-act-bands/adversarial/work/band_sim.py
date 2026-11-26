"""Exact binomial arithmetic for the act-band debate. Planning bands only; no run data, no ground truth."""
import math
from math import comb

BANDS = {"C1": (.10,.40), "C2": (.20,.45), "C3": (.03,.15), "C4": (.50,.75),
         "C5": (.35,.60), "C6": (.05,.30), "C7": (.15,.35), "C8": (.40,.65)}
NS = (5, 10, 18, 30)

def pmf(n, p):
    return [comb(n, k) * p**k * (1-p)**(n-k) for k in range(n+1)]

def wilson(k, n, z=1.645):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return max(0, c-h), min(1, c+h)

def p_in_band(n, p, lo, hi):
    return sum(w for k, w in enumerate(pmf(n, p)) if lo-1e-12 <= k/n <= hi+1e-12)

def p_overlap(n, p, lo, hi):
    tot = 0
    for k, w in enumerate(pmf(n, p)):
        a, b = wilson(k, n)
        if a <= hi and b >= lo: tot += w
    return tot

print("A. P(observed k/n inside the point band) when the TRUE rate is the band midpoint")
print("class band        " + "".join(f"n={n:<6}" for n in NS))
allin = {n: 1.0 for n in NS}
for c, (lo, hi) in BANDS.items():
    mid = (lo+hi)/2
    row = [p_in_band(n, mid, lo, hi) for n in NS]
    for n, v in zip(NS, row): allin[n] *= v
    print(f"{c}    {lo:.2f}-{hi:.2f} mid={mid:.3f} " + "".join(f"{v:<8.2f}" for v in row))
print("P(all 8 classes inside band, each true rate = midpoint, independent): " + ", ".join(f"n={n}: {allin[n]:.4f}" for n in NS))
print()
print("B. same, TRUE rate exactly at the band edge (lo) -> a correct prediction at its edge")
for c, (lo, hi) in BANDS.items():
    print(c, " ".join(f"n={n}:{p_in_band(n, lo, lo, hi):.2f}" for n in NS), "| at hi:", " ".join(f"n={n}:{p_in_band(n, hi, lo, hi):.2f}" for n in NS))
print()
print("C. P(90% Wilson interval overlaps the band) when TRUE rate = band midpoint; and when TRUE rate = 0.15 below lo / above hi (clearly wrong)")
for c, (lo, hi) in BANDS.items():
    mid = (lo+hi)/2
    w = hi-lo
    lo_wrong = max(0.005, lo - w)   # one band-width below
    hi_wrong = min(0.995, hi + w)   # one band-width above
    print(c, " ".join(f"n={n}: mid {p_overlap(n, mid, lo, hi):.2f} / wrong-low {p_overlap(n, lo_wrong, lo, hi):.2f} / wrong-high {p_overlap(n, hi_wrong, lo, hi):.2f}" for n in (10, 18)))
print()
print("D. Quantisation: observed rates available at n=5 and which fall inside each band")
for c, (lo, hi) in BANDS.items():
    ks = [k for k in range(6) if lo <= k/5 <= hi]
    print(c, "n=5 allowed k:", ks, "of 0..5")
print()
print("E. Band widths vs one-sided binomial sd at midpoint, n=18 (planted: 6 plans x 3 runs)")
for c, (lo, hi) in BANDS.items():
    mid = (lo+hi)/2
    print(c, f"width={hi-lo:.2f} sd(n=18)={math.sqrt(mid*(1-mid)/18):.3f} sd(n=10)={math.sqrt(mid*(1-mid)/10):.3f}")
print()
print("F. Pooled band: classes weighted equally, mean of lows / highs")
lows = sum(b[0] for b in BANDS.values())/8; highs = sum(b[1] for b in BANDS.values())/8
print(f"pooled band {lows:.3f}-{highs:.3f}; pooled mid {(lows+highs)/2:.3f}")
for n in (40, 80, 160):
    mid=(lows+highs)/2
    print(f" n={n}: P(in pooled band | true=mid)={p_in_band(n, mid, lows, highs):.2f}; P(in band | true=0.10 (planning model badly wrong))={p_in_band(n,0.10,lows,highs):.2f}; true=0.60: {p_in_band(n,0.60,lows,highs):.2f}")
