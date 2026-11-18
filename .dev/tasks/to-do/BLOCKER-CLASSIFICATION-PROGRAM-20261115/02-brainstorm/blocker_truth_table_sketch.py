"""Design sketch v2: blocker truth table (not framework code). Run: uv run python <this file>.

v2 fixes found by the adversarial debate (see nested/adversarial-1/adversarial/diff-analysis.md, X-007,
and invariant-probe.md INV-007): a skipped (UNSET) answer must never lower a verdict, and a false-statement
answer E that was not obtained must not count as "not wrong".
States per answer: Y, N, U (unsettled), UNSET (should have been answered, was not),
NA (only for M and C: code found no list to judge against, so the question cannot apply; treated as N).
"""
from itertools import product

Y, N, U, UNSET, NA = "Y", "N", "U", "UNSET", "NA"
ORDER = {"NOTE": 0, "FOLLOW_UP": 1, "SHOW_USER": 2, "BLOCKING": 3}
BANDS = {"S": (0.10, 0.30)}  # safety flags early: a missed safety finding costs the most
DEFAULT_BAND = (0.30, 0.70)


def tri(q, p):
    """Probability (or None for a failed or skipped call) to a state."""
    if p is None:
        return UNSET
    lo, hi = BANDS.get(q, DEFAULT_BAND)
    return Y if p >= hi else N if p <= lo else U


def wrong(w, e):
    """Wrong outcome (W) or false statement (E): Y if either is Y; N only if BOTH are N; UNSET if both unset."""
    if Y in (w, e):
        return Y
    if w == N and e == N:
        return N
    if w == UNSET and e == UNSET:
        return UNSET
    return U  # a missing or unsettled partner can never read as "not wrong"


WD = {  # (wrong, decision depends) -> verdict
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
    # an unsettled or missing safety, missing-item or constraint answer is never filed as a follow-up
    if any(x in (U, UNSET) for x in (s, m, c)) and ORDER[base] < ORDER["SHOW_USER"]:
        return "SHOW_USER"
    return base


STATES = (Y, N, U, UNSET)
MC_STATES = STATES + (NA,)
CASES = [(s, m, c, w, e, d) for s in STATES for m in MC_STATES for c in MC_STATES
         for w in STATES for e in STATES for d in STATES]


def run_checks():
    # 1 exhaustive: every combination has exactly one outcome
    for case in CASES:
        assert verdict(*case) in ORDER
    # 2 monotone over answered states: raising an answered input (N < U < Y) never lowers the verdict
    rank = {N: 0, NA: 0, U: 1, Y: 2}
    bad_mono = 0
    for case in CASES:
        for i in range(6):
            if case[i] in rank:
                for new in (N, U, Y):
                    if rank[new] >= rank[case[i]]:
                        alt = list(case)
                        alt[i] = new
                        if ORDER[verdict(*alt)] < ORDER[verdict(*case)]:
                            bad_mono += 1
    # 3 no silent demotion: a verdict below SHOW_USER means no completion of the UNSET answers could block
    bad_demote = 0
    for case in CASES:
        v = verdict(*case)
        if ORDER[v] < ORDER["SHOW_USER"]:
            unset_idx = [i for i in range(6) if case[i] == UNSET]
            for fill in product((Y, U, N), repeat=len(unset_idx)):
                alt = list(case)
                for i, f in zip(unset_idx, fill):
                    alt[i] = f
                if verdict(*alt) == "BLOCKING":
                    bad_demote += 1
    return len(CASES), bad_mono, bad_demote


if __name__ == "__main__":
    n, bad_mono, bad_demote = run_checks()
    print("cases", n, "monotonicity violations (answered states)", bad_mono,
          "silent-demotion violations", bad_demote)
    print("tri(S,0.2)", tri("S", 0.2), "tri(W,0.5)", tri("W", 0.5), "tri(W,None)", tri("W", None))
    assert bad_mono == 0 and bad_demote == 0
