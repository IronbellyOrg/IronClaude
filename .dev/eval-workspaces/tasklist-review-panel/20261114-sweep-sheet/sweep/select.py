"""Item selection (DESIGN 5.1 steps 4 and 5, DD-4).

`sweep.extractors.run_extractors` has already done steps 1 to 3 (top K per class by pre_priority, K_single when only
one class has candidates, `attach` for the kept ones). `select` takes its result and chooses at most `cap` (12) items
from the candidates whose evidence was computed:

    k          the number of classes that have such a candidate
    pass A     the highest-priority candidate of every class, in the class order C4, C8, C5, C2, C1, C6, C7, C3
    pass B     the second candidate of every class, same order, while slots remain
    pass C     the rest by descending priority, at most ceil(cap / k) items per class
    class C3   never more than 1 item (E6 is experimental); `cap` and K come from config/values.json
    ties       earlier plan line, then sha256(str(seed) + anchor_text), as in step 2 (then extractor id and kind)

Status set here, for every candidate whose evidence was computed:
    `selected`
    `dropped:quota`    class C3 already holds its one item
    `dropped:ceiling`  the class already holds ceil(cap / k) items
    `dropped:cap12`    the sheet already holds `cap` items
(checked in that order). Candidates that never got evidence keep `dropped:pre_rank` from run_extractors.
`no_evidence_slot` (listed in DESIGN 4.1) has no rule in 5.1 and is never set.

Nothing here reads a clock, the network or a random source; the same candidates and seed give the same selection.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

from sweep import extractors

CLASS_ORDER = ("C4", "C8", "C5", "C2", "C1", "C6", "C7", "C3")
SINGLE_ITEM_CLASSES = {"C3": 1}  # class -> most items (DESIGN 4.7, 5.1 step 4)

STATUS_SELECTED = "selected"
STATUS_QUOTA = "dropped:quota"
STATUS_CEILING = "dropped:ceiling"
STATUS_CAP = "dropped:cap12"
EXPERIMENTAL_EXTRACTORS = ("E6",)


@dataclass
class Selection:
    seed: int | str
    k: int  # classes with a candidate whose evidence was computed
    cap: int
    ceiling: int  # ceil(cap / k); 0 when k is 0
    items: list[dict]  # items.json rows S1, S2, ... in descending priority
    candidates: list[dict]  # candidates.json rows, one per candidate, in input order

    def items_json(self) -> dict:
        return {"seed": self.seed, "items": self.items}

    def candidates_json(self) -> dict:
        return {"seed": self.seed, "candidates": self.candidates}


def _key(seed, c: extractors.Candidate):
    """Higher priority first; ties by earlier plan line, then sha256(seed + anchor_text)."""
    digest = hashlib.sha256((str(seed) + c.anchor_text).encode("utf-8")).hexdigest()
    return (-c.priority, c.location["line_start"], digest, c.extractor, c.kind)


def select(cands, seed=0, constants: dict | None = None) -> Selection:
    """Choose the items among `cands` (the list run_extractors returns) and set each candidate's status."""
    cap = int((constants or extractors.load_constants())["cap"])
    pool = [c for c in cands if c.evidence_computed]
    groups: dict[str, list] = {}
    for c in sorted(pool, key=lambda c: _key(seed, c)):
        groups.setdefault(c.cls, []).append(c)
    k = len(groups)
    ceiling = math.ceil(cap / k) if k else 0
    limit = {cls: min(ceiling, SINGLE_ITEM_CLASSES.get(cls, ceiling)) for cls in groups}
    chosen: list = []
    ids: set[int] = set()
    held = dict.fromkeys(groups, 0)

    def take(c) -> None:
        if len(chosen) < cap and held[c.cls] < limit[c.cls] and id(c) not in ids:
            chosen.append(c)
            ids.add(id(c))
            held[c.cls] += 1

    for rank in (0, 1):  # pass A, pass B
        for cls in CLASS_ORDER:
            if cls in groups and rank < len(groups[cls]):
                take(groups[cls][rank])
    for c in sorted(pool, key=lambda c: _key(seed, c)):  # pass C
        take(c)

    for c in pool:
        if id(c) in ids:
            c.status = STATUS_SELECTED
        elif c.cls in SINGLE_ITEM_CLASSES and held[c.cls] >= limit[c.cls]:
            c.status = STATUS_QUOTA
        elif held[c.cls] >= ceiling:
            c.status = STATUS_CEILING
        else:
            c.status = STATUS_CAP

    items, item_of = [], {}
    for n, c in enumerate(sorted(chosen, key=lambda c: _key(seed, c)), 1):
        item_of[id(c)] = f"S{n}"
        items.append(
            {
                "item_id": f"S{n}",
                "class": c.cls,
                "extractor": c.extractor,
                "kind": c.kind,
                "anchor_text": c.anchor_text,
                "location": dict(c.location),
                "evidence": [dict(e) for e in c.evidence],
                "priority": c.priority,
                "route": c.route,
                "experimental": c.extractor in EXPERIMENTAL_EXTRACTORS,
            }
        )
    rows = []
    for c in cands:
        row = c.to_dict()
        row["drop_reason"] = (
            c.status.split(":", 1)[1] if c.status.startswith("dropped:") else None
        )
        row["item_id"] = item_of.get(id(c))
        rows.append(row)
    return Selection(seed, k, cap, ceiling, items, rows)


def dumps(obj) -> str:
    """JSON as DESIGN 2.4 writes it: sorted keys, ensure_ascii False, trailing newline."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=1) + "\n"


def write(out_dir, sel: Selection) -> None:
    """Write candidates.json and items.json into out_dir (the caller makes the folder)."""
    out = Path(out_dir)
    (out / "candidates.json").write_text(dumps(sel.candidates_json()), encoding="utf-8")
    (out / "items.json").write_text(dumps(sel.items_json()), encoding="utf-8")
