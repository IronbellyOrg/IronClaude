"""E2 static ranking (deterministic rules, no model).

Order: (1) explicit-reference pairs, (2) shared id across different sections, (3) shared path basename, (4) a frozen diverse
distant-pair sample (random.Random(seed) over the remaining pool, stratified by section distance).  Inside tiers 1-3 the
tie-break is section distance (descending) then pid.  Section distance = difference of section ordinals in the document.
"""
from __future__ import annotations

import random


def section_distance(pair) -> int:
    return abs(pair.a.section_ord - pair.b.section_ord)


def tier(pair) -> int:
    f = pair.features
    if f.get("explicit_ab") or f.get("explicit_ba"):
        return 1
    if f.get("shared_ids") and pair.a.section_ord != pair.b.section_ord:
        return 2
    if f.get("shared_paths"):
        return 3
    return 4


def bucket(d: int) -> int:
    return 0 if d == 0 else 1 if d <= 2 else 2 if d <= 5 else 3


def rank(pool, seed: int = 0) -> list:
    """Return the pool in static order.  Pure function of (pool, seed)."""
    tiers = {1: [], 2: [], 3: [], 4: []}
    for p in pool:
        tiers[tier(p)].append(p)
    out = []
    for t in (1, 2, 3):
        out += sorted(tiers[t], key=lambda p: (-section_distance(p), p.a.pid, p.b.pid))
    rest = sorted(tiers[4], key=lambda p: (p.a.pid, p.b.pid))
    rng = random.Random(seed)
    strata = {0: [], 1: [], 2: [], 3: []}
    for p in rest:
        strata[bucket(section_distance(p))].append(p)
    for k in strata:
        rng.shuffle(strata[k])
    order = [3, 2, 1, 0]                       # most distant stratum first
    i = 0
    while any(strata[k] for k in order):
        k = order[i % 4]
        if strata[k]:
            out.append(strata[k].pop(0))
        i += 1
    return out


def reason_for(pair) -> str:
    f = pair.features
    bits = []
    ab = list(f.get("explicit_ab") or []) + list(f.get("explicit_ba") or [])
    if ab:
        bits.append("explicit reference (" + ", ".join(dict.fromkeys(ab)) + ")")
    if f.get("shared_ids"):
        bits.append("both mention " + ", ".join(f["shared_ids"][:3]))
    if f.get("shared_paths"):
        bits.append("both name " + ", ".join(f["shared_paths"][:2]))
    if f.get("shared_terms") and not bits:
        bits.append("both use " + ", ".join(f["shared_terms"][:2]))
    if f.get("shared_numunits") and not bits:
        bits.append("both state " + ", ".join(f["shared_numunits"][:2]))
    if f.get("shared_rare_words") and not bits:
        bits.append("share rare words " + ", ".join(f["shared_rare_words"][:3]))
    return "; ".join(bits) or "candidate pair"
