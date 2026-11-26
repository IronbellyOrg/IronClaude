"""REQ-21 (marker `freeze`): extractor recall and precision on plans with defects seeded by a second author.

Written, not run by the build: `fixtures/recall/` is a step 14 deliverable (TESTING F-RECALL; it cannot be written by the
author of the extractors, AO-4). While it is absent every test here FAILS with "fixtures/recall missing"; none skips, so
the freeze script cannot pass without the fixtures.

Layout this file reads (the contract for the step 14 author), one folder per plan under `fixtures/recall/`:

    <plan-id>/seeded.md      the plan with the seeded defects
    <plan-id>/seeds.json     a JSON list of {"class": "C1".."C8", "quote": "<exact quote of seeded.md>"}
    <plan-id>/source.md      optional, the plan's source document (E5 runs only with it)
    <plan-id>/snapshot/      optional, a git checkout the repository-search extractors (E2 to E4) search; no folder, no search
    AUTHORS.md               who seeded, and that they had not read the extractors

A seed is found by an extractor when one of its candidates (the `find` output, before selection) has the class of the
seed and an anchor that holds the quote or is held in it (whitespace flattened). Recall is pooled over all plans;
precision of an extractor is its candidates that hit a seed over all its candidates, and is printed, not gated.
"""

import json
from pathlib import Path

import pytest

from scaffold import fnd
from sweep import extractors, plan
from sweep.extractors import Ctx

pytestmark = pytest.mark.freeze

RECALL = Path(__file__).resolve().parents[1] / "fixtures" / "recall"
MIN_PLANS = 3
RECALL_FLOOR = 0.8
GATED = ("E1", "E2", "E3", "E4", "E7")
CLASS_EXTRACTOR = {
    "C1": "E1", "C6": "E1", "C4": "E2", "C8": "E3", "C5": "E4", "C2": "E5", "C7": "E7", "C3": "E6",
}  # fmt: skip


def plan_dirs() -> list[Path]:
    if not RECALL.is_dir():
        pytest.fail("fixtures/recall missing")
    dirs = sorted(p for p in RECALL.iterdir() if (p / "seeds.json").is_file())
    if len(dirs) < MIN_PLANS:
        pytest.fail(
            f"fixtures/recall missing: {len(dirs)} plans with a seeds.json, at least {MIN_PLANS} needed"
        )
    return dirs


def run_all() -> list[tuple[Path, list[dict], dict[str, list]]]:
    """(plan dir, seeds, {extractor id: its candidates}) for every plan; only `find` runs."""
    out = []
    for d in plan_dirs():
        doc = plan.read(d / "seeded.md")
        src = d / "source.md"
        snap = d / "snapshot"
        ctx = Ctx(
            doc,
            source=plan.read(src) if src.is_file() else None,
            snapshot=snap if snap.is_dir() else None,
        )
        seeds = json.loads((d / "seeds.json").read_text(encoding="utf-8"))
        found = {
            eid: find(doc, ctx) for eid, (find, _) in extractors.EXTRACTORS.items()
        }
        out.append((d, seeds, found))
    return out


def hits(cand, seed) -> bool:
    a, q = fnd.flat(cand.anchor_text), fnd.flat(seed["quote"])
    return cand.cls == seed["class"] and (a in q or q in a)


def tally():
    """Per extractor: seeds of its classes, seeds found, candidates, candidates that hit a seed (pooled over plans)."""
    t = {eid: dict(seeds=0, found=0, cands=0, true=0) for eid in extractors.EXTRACTORS}
    for _, seeds, found in run_all():
        for eid, cands in found.items():
            mine = [s for s in seeds if CLASS_EXTRACTOR.get(s["class"]) == eid]
            t[eid]["seeds"] += len(mine)
            t[eid]["found"] += sum(any(hits(c, s) for c in cands) for s in mine)
            t[eid]["cands"] += len(cands)
            t[eid]["true"] += sum(any(hits(c, s) for s in seeds) for c in cands)
    return t


def test_recall_per_extractor():
    t = tally()
    low = []
    for eid in GATED:
        n, k = t[eid]["seeds"], t[eid]["found"]
        recall = k / n if n else 0.0
        print(f"{eid}: recall {k}/{n} = {recall:.2f}")
        if n == 0 or recall < RECALL_FLOOR:
            low.append(f"{eid} {k}/{n}")
    assert not low, f"recall under {RECALL_FLOOR} (or no seeds) for: {', '.join(low)}"


def test_precision_reported():
    t = tally()
    for eid in sorted(t):
        c, k = t[eid]["cands"], t[eid]["true"]
        print(f"{eid}: precision {k}/{c}" + (f" = {k / c:.2f}" if c else " = n/a"))
    assert set(t) == set(extractors.EXTRACTOR_IDS)


def test_e6_marked_experimental():
    items = [c for _, _, found in run_all() for c in found["E6"]]
    for c in items:
        assert c.features.get("experimental") is True, c.anchor_text
        assert c.to_dict()["features"]["experimental"] is True
