"""Blocker classifier: truth table and confidence (program artifact, not framework code).

Logic copied from 02-brainstorm/blocker_truth_table_sketch.py (version 2, 6,400 combinations, 0 violations of
exhaustiveness, monotonicity over answered states, and no silent demotion). Run the checks:
    uv run python truth_table.py
Classify a judge answer file (JSON lines, one finding per line, keys id,S,W,E,M,C,D with probabilities 0..1 or null):
    uv run python truth_table.py answers.jsonl
Prints one JSON line per finding: id, states, verdict, confidence.
"""
import json
import sys
from itertools import product

Y, N, U, UNSET, NA = "Y", "N", "U", "UNSET", "NA"
ORDER = {"NOTE": 0, "FOLLOW_UP": 1, "SHOW_USER": 2, "BLOCKING": 3}
BANDS = {"S": (0.10, 0.30)}  # safety flags early: a missed safety finding costs the most
DEFAULT_BAND = (0.30, 0.70)


def tri(q, p):
    if p is None:
        return UNSET
    lo, hi = BANDS.get(q, DEFAULT_BAND)
    return Y if p >= hi else N if p <= lo else U


def wrong(w, e):
    if Y in (w, e):
        return Y
    if w == N and e == N:
        return N
    if w == UNSET and e == UNSET:
        return UNSET
    return U  # a missing or unsettled partner never reads as "not wrong"


WD = {
    (Y, Y): "BLOCKING", (Y, U): "SHOW_USER", (Y, N): "FOLLOW_UP", (Y, UNSET): "SHOW_USER",
    (U, Y): "SHOW_USER", (U, U): "SHOW_USER", (U, N): "FOLLOW_UP", (U, UNSET): "SHOW_USER",
    (N, Y): "NOTE", (N, U): "NOTE", (N, N): "NOTE", (N, UNSET): "NOTE",
}


def verdict(s, m, c, w, e, d):
    if s == Y:
        return "BLOCKING"
    if m == Y or c == Y:
        base = "BLOCKING"
    else:
        wr = wrong(w, e)
        base = "SHOW_USER" if wr == UNSET else WD[(wr, d)]
    if any(x in (U, UNSET) for x in (s, m, c)) and ORDER[base] < ORDER["SHOW_USER"]:
        return "SHOW_USER"
    return base


def confidence(v, p):
    """Weakest-link confidence from the raw probabilities (None counts as 0)."""
    g = lambda k: p.get(k) or 0.0
    if v == "BLOCKING":
        if tri("S", p.get("S")) == Y:
            return g("S")
        if tri("M", p.get("M")) == Y or tri("C", p.get("C")) == Y:
            return max(g("M"), g("C"))
        return min(max(g("W"), g("E")), g("D"))
    if v in ("FOLLOW_UP", "NOTE"):
        return 1 - min(1.0, g("S") + g("M") + g("C") + min(max(g("W"), g("E")), g("D")))
    return None


def classify(p):
    st = {q: tri(q, p.get(q)) for q in "SWEMCD"}
    v = verdict(st["S"], st["M"], st["C"], st["W"], st["E"], st["D"])
    return st, v, confidence(v, p)


STATES = (Y, N, U, UNSET)
CASES = [(s, m, c, w, e, d) for s in STATES for m in STATES + (NA,) for c in STATES + (NA,)
         for w in STATES for e in STATES for d in STATES]


def run_checks():
    for case in CASES:
        assert verdict(*case) in ORDER
    rank = {N: 0, NA: 0, U: 1, Y: 2}
    bad_mono = bad_demote = 0
    for case in CASES:
        for i in range(6):
            if case[i] in rank:
                for new in (N, U, Y):
                    if rank[new] >= rank[case[i]]:
                        alt = list(case)
                        alt[i] = new
                        bad_mono += ORDER[verdict(*alt)] < ORDER[verdict(*case)]
        if ORDER[verdict(*case)] < ORDER["SHOW_USER"]:
            idx = [i for i in range(6) if case[i] == UNSET]
            for fill in product((Y, U, N), repeat=len(idx)):
                alt = list(case)
                for i, f in zip(idx, fill):
                    alt[i] = f
                bad_demote += verdict(*alt) == "BLOCKING"
    return len(CASES), bad_mono, bad_demote


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for line in open(sys.argv[1]):
            if line.strip():
                p = json.loads(line)
                st, v, c = classify(p)
                print(json.dumps({"id": p["id"], "states": st, "verdict": v, "confidence": c}))
    else:
        n, bm, bd = run_checks()
        print("cases", n, "monotonicity violations", bm, "silent-demotion violations", bd)
        assert bm == 0 and bd == 0
        assert classify({"S": 0.9, "W": 0.1, "E": 0.1, "M": 0.1, "C": 0.1, "D": 0.1})[1] == "BLOCKING"
        assert classify({"S": 0.0, "W": 0.0, "E": 0.0, "M": 0.0, "C": 0.0, "D": 0.0})[1] == "NOTE"
        assert classify({"S": None, "W": 0.0, "E": 0.0, "M": 0.0, "C": 0.0, "D": 0.0})[1] == "SHOW_USER"
        print("ok")
