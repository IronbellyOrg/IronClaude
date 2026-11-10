#!/usr/bin/env python3
"""perturb.py [--real]  40 perturbations (plan 4.3): 10 evidence-order swaps (e1 <-> e2), 10 claim paraphrases, 10 misleading
instructions, 10 omitted-context variants.  40 base cases = 20 synthetic + 20 real (non-exceptions), drawn with random.Random(33).
Without --real: the 20 synthetic ones from offline/synth.  With --real: the 20 real ones from offline/cases/base (after select_base.py).
Labels: swaps, paraphrases and misleading variants inherit their base label; omitted-context variants inherit `blocking` and are
`confirmable_from_packet = no` by construction (a CONFIRMED there counts against gate 3.1).  Each perturbation shares its base's group."""
import copy
import json
import random
import re
import sys

import e3lib
import packets as pk
from p15common import datasets

KINDS = ("swap", "paraphrase", "misleading", "omit")
PERT = e3lib.CASES / "perturb"

PHRASES = [
    (r"\bAn implementer who follows\b", "Anyone who follows"), (r"\ban implementer who follows\b", "anyone who follows"),
    (r"\bas written\b", "to the letter"), (r"\bbuilds\b", "ends up with"), (r"\bis wrong because\b", "is incorrect since"),
    (r"\bcannot\b", "is unable to"), (r"\bmust\b", "has to"), (r"\bat the same time\b", "simultaneously"),
    (r"\bcontradict(?:s|ed)?\b", "conflict"), (r"\brequires\b", "demands"), (r"\bstates\b", "says"),
    (r"\bnever\b", "at no point"), (r"\bevery\b", "each"), (r"\bonly\b", "solely"), (r"\bso\b", "which means"),
    (r"\bthe stated text\b", "the text as given"), (r"\bresult\b", "outcome"), (r"\bfails?\b", "does not work"),
]


def paraphrase(claim: str) -> str:
    """Deterministic claim paraphrase: phrase substitutions, plus a re-ordering of the final 'because' clause when the grading
    sentence has the shape 'A, and B is wrong because C'.  Always differs from the input."""
    out = claim
    m = re.match(r"^(.*?), and (.*?) is wrong because (.*)$", out, flags=re.S)
    if m:
        a, b, c = m.group(1), m.group(2), m.group(3).rstrip(". ")
        out = f"Because {c[:1].lower() + c[1:]}, {a[:1].lower() + a[1:]}; {b} is therefore wrong."
    alt = re.compile("|".join(f"(?P<g{i}>{rx})" for i, (rx, _) in enumerate(PHRASES)))
    out = alt.sub(lambda mm: PHRASES[int(mm.lastgroup[1:])][1], out)     # one pass: replaced text is never substituted again
    if out == claim:
        out = "Put differently: " + claim[:1].lower() + claim[1:]
    return out


def swap(state):
    st = copy.deepcopy(state)
    ev = st["evidence"]
    if len(ev) != 2:
        raise ValueError("swap needs two evidence texts")
    ev["e1"], ev["e2"] = ev["e2"], ev["e1"]
    return st


def with_suffix(state, suffix):
    st = copy.deepcopy(state)
    st["finding"]["wrong_outcome"] = st["finding"]["wrong_outcome"] + suffix
    return st


def omit_context(state, candidate_text):
    """Remove e2 (two texts), else reduce e1's context to its own line (one text)."""
    st = copy.deepcopy(state)
    ev = st["evidence"]
    if len(ev) == 2:
        del ev["e2"]
    else:
        e1 = ev["e1"]
        lines = candidate_text.splitlines()
        e1["context"] = lines[e1["line"] - 1] if 0 < e1["line"] <= len(lines) else e1["text"]
    st["facts"]["evidence_count"] = len(ev)
    return st


def assign_kinds(items, rng, per_kind=5):
    """items: [(case_id, evidence_count)] -> {case_id: kind}.  Swaps need two texts; swaps and omissions are taken from the two-text
    cases first.  A shortfall (fewer than per_kind swaps) is returned in the second value."""
    two = [c for c, n in items if n == 2]
    one = [c for c, n in items if n != 2]
    rng.shuffle(two)
    rng.shuffle(one)
    kinds, short = {}, {}
    sw = two[:per_kind]
    for c in sw:
        kinds[c] = "swap"
    short["swap"] = per_kind - len(sw)
    rest_two = two[per_kind:]
    om = (rest_two + one)[:per_kind] if len(rest_two) >= per_kind else rest_two + one[:per_kind - len(rest_two)]
    for c in om:
        kinds[c] = "omit"
    taken = set(kinds)
    left = [c for c in one + rest_two if c not in taken]
    for kind in ("paraphrase", "misleading"):
        pick = left[:per_kind]
        left = left[per_kind:]
        for c in pick:
            kinds[c] = kind
    return kinds, short


def make_variant(base, kind, dec):
    pkt = pk.packet_of_case(base)
    text = e3lib.candidate_of(base)
    st = pkt.state
    if kind == "swap":
        new = swap(st)
    elif kind == "paraphrase":
        new = copy.deepcopy(st)
        new["finding"]["wrong_outcome"] = paraphrase(st["finding"]["wrong_outcome"])
    elif kind == "misleading":
        new = with_suffix(st, dec["offline"]["misleading_suffix"])
    elif kind == "omit":
        new = omit_context(st, text)
    else:
        raise ValueError(kind)
    return {"case_id": f"{base['case_id']}~{kind}", "group": base["group"], "family": base["family"], "category": base["category"],
            "variant": kind, "split": "perturb", "data_classes": base["data_classes"], "source": base["source"],
            "packet": {"base_case_id": base["case_id"], "code_outcome": "OK", "state": new},
            "author_intent": {"perturbation": kind, "inherits": base["case_id"]},
            "base_case_id": base["case_id"], "confirmable_from_packet": "no" if kind == "omit" else "yes"}


def build_set(bases, rng, dec, n=20):
    elig = []
    for b in sorted(bases, key=lambda c: c["case_id"]):
        p = pk.packet_of_case(b)
        if p.code_outcome == "OK":
            elig.append((b["case_id"], p.evidence_count, b))
    ids = [(c, n_) for c, n_, _ in elig]
    chosen_rng = random.Random(rng.random())
    chosen_rng.shuffle(ids)
    # prefer a draw that can serve the swap quota: the first n of the shuffled list, topped up with two-text cases if needed
    pick = ids[:n]
    two_missing = max(0, 5 - sum(1 for _, k in pick if k == 2))
    if two_missing:
        extra_two = [x for x in ids[n:] if x[1] == 2][:two_missing]
        drop = [x for x in reversed(pick) if x[1] != 2][:len(extra_two)]
        pick = [x for x in pick if x not in drop] + extra_two
    by_id = {c: b for c, _, b in elig}
    kinds, short = assign_kinds(pick, rng)
    return [make_variant(by_id[c], k, dec) for c, k in sorted(kinds.items())], short, len(elig)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    real = "--real" in argv
    dec = e3lib.decision()
    seed = dec["offline"]["perturb_seed"]
    PERT.mkdir(parents=True, exist_ok=True)
    if real:
        bases = [c for c in e3lib.load_cases("base") if c["category"] == "real"]
        rng = random.Random(seed + 1)
    else:
        bases = [json.loads(p.read_text()) for p in sorted((e3lib.OFF / "synth").glob("*.json"))]
        rng = random.Random(seed)
    if not bases:
        print("ERROR no base cases found (run cases_synth.py / select_base.py first)")
        return 2
    variants, short, n_elig = build_set(bases, rng, dec, n=20)
    tag = "real" if real else "synth"
    for old in PERT.glob("*.json"):
        b = json.loads(old.read_text())
        if (b["category"] == "real") == real:
            old.unlink()
    for v in variants:
        datasets.write_case(PERT / f"{v['case_id']}.json", v)
    from collections import Counter
    print(f"PERTURB {tag}: {len(variants)} variants from {n_elig} eligible bases; kinds {dict(Counter(v['variant'] for v in variants))}; shortfall {short}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
