"""Label agreement, adjudication and truth merging (contract J8).  Labels are dicts: case_id -> {field: value, ..., "confidence": "high|low"}."""
import json


def _key(v):
    return json.dumps(v, sort_keys=True)


def agreement(l1: dict, l2: dict, fields) -> dict:
    out = {}
    common = sorted(set(l1) & set(l2))
    for f in fields:
        pairs = [(_key(l1[c].get(f)), _key(l2[c].get(f))) for c in common if f in l1[c] and f in l2[c]]
        n = len(pairs)
        if not n:
            out[f] = {"raw": None, "kappa": None, "n": 0}
            continue
        po = sum(a == b for a, b in pairs) / n
        cats = {a for a, _ in pairs} | {b for _, b in pairs}
        pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
        kappa = None if abs(1 - pe) < 1e-12 else (po - pe) / (1 - pe)
        out[f] = {"raw": po, "kappa": kappa, "n": n}
    return out


def to_adjudicate(l1: dict, l2: dict, fields) -> list:
    out = []
    for c in sorted(set(l1) | set(l2)):
        if c not in l1 or c not in l2:
            out.append(c); continue
        a, b = l1[c], l2[c]
        if any(_key(a.get(f)) != _key(b.get(f)) for f in fields) or a.get("confidence") == "low" or b.get("confidence") == "low":
            out.append(c)
    return out


def merge_truth(l1: dict, l2: dict, adj: dict, fields):
    """truth: case_id -> {field: value}.  Agreed, high-confidence cases keep their labels; adjudicated cases take the ADJ label.
    A field the adjudicator answers `undecidable` stays `undecidable` and the case is listed in disputes with unresolved=True."""
    truth, disputes = {}, []
    for c in sorted(set(l1) | set(l2) | set(adj)):
        if c in adj:
            a = adj[c]
            truth[c] = {f: a.get(f) for f in fields}
            disputes.append({"case_id": c, "L1": l1.get(c), "L2": l2.get(c), "ADJ": a, "reason": a.get("reason", ""),
                             "unresolved": any(a.get(f) == "undecidable" for f in fields)})
        elif c in l1 and c in l2:
            truth[c] = {f: l1[c].get(f) for f in fields}
        else:
            disputes.append({"case_id": c, "L1": l1.get(c), "L2": l2.get(c), "ADJ": None,
                             "reason": "label missing and no adjudication", "unresolved": True})
    return truth, disputes
