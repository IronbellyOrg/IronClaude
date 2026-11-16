"""Item selection and the rank table (DESIGN 5.1 steps 4 and 5, 5.2, DD-4, DD-10; TESTING REQ-19).

The two-phase flow (`run_extractors`, then `select`) runs on invented candidates made by extractors defined in this
file, on the 200 set-word sentences of fixtures/plans/gen_setwords.py with the real E1, and, for the rank table, on
the real extractors with fixtures/plans/p_basic.md. Git runs only in repositories built under /tmp.
"""

import hashlib
import json
import math
from pathlib import Path

import pytest

from fixtures.plans import gen_setwords
from fixtures.repos.build_repo import build_repo
from sweep import extractors, plan, rank, select
from sweep.extractors import Candidate, Ctx

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
CLASS_OF = {  # one extractor id per class, for the invented extractors
    "C1": "E1",
    "C2": "E5",
    "C3": "E6",
    "C4": "E2",
    "C5": "E4",
    "C6": "E1",
    "C7": "E7",
    "C8": "E3",
}
STATUSES = {
    "selected",
    "dropped:pre_rank",
    "dropped:quota",
    "dropped:ceiling",
    "dropped:cap12",
}


def sentence(cls, i):
    return f"Sentence {cls}-{i:03d} says every row is covered."


def make_doc(classes, n=30):
    lines = ["# Plan", "", "## Task 1: demo", ""]
    lines += [sentence(c, i) for c in classes for i in range(n)]
    return plan.parse("\n".join(lines) + "\n")


def cand(cls, i, pre, line=None):
    return Candidate(
        extractor=CLASS_OF[cls],
        cls=cls,
        kind="test",
        anchor_text=sentence(cls, i),
        location={"task": "T1", "line_start": line or 5 + i, "line_end": line or 5 + i},
        pre_priority=pre,
    )


def registry(spec, seen=None, priority=None):
    """spec: {class: [(i, pre_priority), ...]}. attach gives each candidate evidence and priority(pre, i, cls)."""
    priority = priority or (lambda pre, i, cls: pre)
    groups = {}  # extractor id -> its classes (C1 and C6 share E1)
    for cls in spec:
        groups.setdefault(CLASS_OF[cls], []).append(cls)
    reg = {}
    for eid, classes in groups.items():

        def find(doc, ctx, classes=classes):
            return [cand(cls, i, pre) for cls in classes for i, pre in spec[cls]]

        def attach(batch, ctx):
            for cls in {c.cls for c in batch}:
                if seen is not None:
                    seen.setdefault(cls, []).append(
                        [c.anchor_text for c in batch if c.cls == cls]
                    )
            for c in batch:
                i = int(c.anchor_text.split("-")[1].split()[0])
                c.evidence = [
                    {"path": "plan", "line": c.location["line_start"], "text": "x"}
                ]
                c.priority = priority(c.pre_priority, i, c.cls)

        reg[eid] = (find, attach)
    return reg


def flow(spec, seed=1, constants=None, **kw):
    """The two-phase flow of DD-10, then the selection."""
    seen = {}
    ctx = Ctx(make_doc(sorted(spec)), seed=seed, constants=constants)
    cands = extractors.run_extractors(ctx, registry(spec, seen, **kw))
    return cands, select.select(cands, seed, ctx.constants), seen


def by_class(sel):
    out = {}
    for it in sel.items:
        out[it["class"]] = out.get(it["class"], 0) + 1
    return out


def rows(n, pre=lambda i: 50):
    return [(i, pre(i)) for i in range(n)]


def setwords_flow(seed=7, n=200):
    doc = plan.parse(gen_setwords.generate(n, 12))
    ctx = Ctx(doc, seed=seed)
    cands = extractors.run_extractors(ctx)
    return cands, select.select(cands, seed, ctx.constants)


# ---------------------------------------------------------------- REQ-19: the five named tests


def test_200_setword_sentences():
    cands, sel = setwords_flow()
    assert len(cands) >= 200
    classes = {c.cls for c in cands}
    # set words give C1 and C6; the "first N files" bounds also give E4 count triggers (class C5)
    assert classes == {"C1", "C5", "C6"}
    assert len(sel.items) <= 12 and len(sel.items) == 12
    got = by_class(sel)
    assert set(got) == classes and sel.k == 3  # every triggered class has at least 1
    assert max(got.values()) <= math.ceil(12 / sel.k)  # fair-share ceiling
    # attach ran only on the top K of each class (DD-10); the rest never got evidence
    for cls in classes:
        group = [c for c in cands if c.cls == cls]
        assert sum(c.evidence_computed for c in group) == 8
        assert all(
            c.status == "dropped:pre_rank" for c in group if not c.evidence_computed
        )
    assert [it["item_id"] for it in sel.items] == [f"S{n}" for n in range(1, 13)]
    again = setwords_flow()[1]  # same input and seed: same selection
    assert select.dumps(again.items_json()) == select.dumps(sel.items_json())
    assert select.dumps(again.candidates_json()) == select.dumps(sel.candidates_json())


@pytest.mark.parametrize("cls, want", [("C1", 12), ("C4", 12), ("C3", 1)])
def test_single_class_fills_12(cls, want):
    spec = {cls: rows(30, lambda i: 3 * i)}
    cands, sel, seen = flow(spec)
    assert [len(b) for b in seen[cls]] == [12]  # attach ran on the class's top 12
    top = sorted(cands, key=lambda c: -c.pre_priority)[:12]
    assert {c.anchor_text for c in cands if c.evidence_computed} == {
        c.anchor_text for c in top
    }
    assert sum(c.status == "dropped:pre_rank" for c in cands) == 18
    assert (sel.k, sel.ceiling) == (1, 12)
    assert len(sel.items) == want and set(by_class(sel)) == {cls}
    if (
        cls == "C3"
    ):  # the experimental class holds one item; the other 11 are quota drops
        assert sum(c.status == "dropped:quota" for c in cands) == 11
        assert sel.items[0]["experimental"] is True
    else:
        assert not any(it["experimental"] for it in sel.items)
        assert sum(c.status == "selected" for c in cands) == 12


@pytest.mark.parametrize("k", range(2, 9))
def test_fair_share_ceiling(k):
    classes = list(select.CLASS_ORDER[:k])
    # the first class of the order outranks every other one by far: rank must not let it crowd the rest out
    spec = {c: rows(10) for c in classes}
    prio = lambda pre, i, cls: 99 - i if cls == classes[0] else 10 + i  # noqa: E731
    cands, sel, _ = flow(spec, priority=prio)
    ceiling = math.ceil(12 / k)
    got = by_class(sel)
    assert sel.ceiling == ceiling and sel.k == k
    assert len(sel.items) == 12 and set(got) == set(classes)
    assert all(1 <= n <= ceiling for n in got.values())
    assert got[classes[0]] == min(
        ceiling, 12 - (k - 1)
    )  # the favourite takes only its share
    # the drop reasons: a full class is `ceiling`, a full sheet is `cap12`
    statuses = {c.status for c in cands if c.evidence_computed}
    assert statuses <= {"selected", "dropped:ceiling", "dropped:cap12", "dropped:quota"}
    assert "dropped:ceiling" in statuses and ("dropped:quota" in statuses) == (k == 8)


def test_fair_share_with_c3_among_three_classes():
    spec = {"C4": rows(10), "C8": rows(10), "C3": rows(10)}
    cands, sel, _ = flow(spec)
    assert by_class(sel) == {"C4": 4, "C8": 4, "C3": 1}  # ceil(12/3) = 4; C3 holds 1
    assert len(sel.items) == 9  # a quota is never refilled from other classes
    c3 = [c for c in cands if c.cls == "C3" and c.evidence_computed]
    assert sorted(c.status for c in c3) == ["dropped:quota"] * 7 + ["selected"]
    for cls in ("C4", "C8"):
        assert {c.status for c in cands if c.cls == cls and c.evidence_computed} == {
            "selected",
            "dropped:ceiling",
        }


def test_class_order_and_ties():
    # pass B: the second item of the classes in the fixed order while slots remain; priority does not matter here
    order = ["C4", "C8", "C5", "C2", "C1", "C6", "C7", "C3"]
    assert list(select.CLASS_ORDER) == order
    spec = {c: rows(2) for c in order}
    prio = lambda pre, i, cls: (  # noqa: E731
        80
        if i == 0
        else (
            40 if cls in ("C1", "C6", "C7", "C3") else 20
        )  # the late classes' second items rank higher
    )
    cands, sel, _ = flow(spec, priority=prio)
    second = {
        c.cls for c in cands if c.status == "selected" and "-001" in c.anchor_text
    }
    assert second == {"C4", "C8", "C5", "C2"}  # 8 first items + 4 second items = 12
    assert len(sel.items) == 12 and by_class(sel)["C3"] == 1
    # pass A: with cap 5 the first five classes of the order get their item, the others are dropped for the cap
    cands, sel, _ = flow(
        spec, constants={"K": 8, "K_single": 12, "cap": 5}, priority=prio
    )
    assert {it["class"] for it in sel.items} == set(order[:5])
    assert {
        c.cls for c in cands if c.status == "dropped:cap12" and "-000" in c.anchor_text
    } == set(order[5:])


def test_ties_earlier_line_then_seeded_hash_and_item_numbers():
    # equal priority in one class: the earlier plan line first
    spec = {"C1": [(i, 50) for i in (5, 3, 9, 1)]}  # lines 10, 8, 14, 6
    cands, sel, _ = flow(spec, constants={"K": 8, "K_single": 12, "cap": 3})
    assert [it["location"]["line_start"] for it in sel.items] == [6, 8, 10]
    assert [it["item_id"] for it in sel.items] == ["S1", "S2", "S3"]
    drop = next(c for c in cands if c.status != "selected")
    assert drop.location["line_start"] == 14 and drop.status == "dropped:ceiling"
    # the same line and priority: sha256(seed + anchor_text) decides; the seed moves the pick
    a, b = sentence("C1", 5), sentence("C1", 6)

    def find(d, ctx):
        return [
            Candidate("E1", "C1", "k", t, {"task": "T1", "line_start": 9, "line_end": 9}, pre_priority=50)
            for t in (a, b)
        ]  # fmt: skip

    def attach(batch, ctx):
        for c in batch:
            c.evidence = []

    picks = set()
    for seed in range(1, 9):
        ctx = Ctx(
            make_doc(["C1"]), seed=seed, constants={"K": 8, "K_single": 12, "cap": 1}
        )
        out = extractors.run_extractors(ctx, {"E1": (find, attach)})
        s = select.select(out, seed, ctx.constants)
        want = min(
            (a, b), key=lambda t: hashlib.sha256((str(seed) + t).encode()).hexdigest()
        )
        assert [it["anchor_text"] for it in s.items] == [want]
        picks.add(want)
    assert picks == {a, b}
    # items run in descending priority, ties as above
    cands, sel, _ = flow(
        {"C1": rows(6), "C4": rows(6)}, priority=lambda pre, i, cls: 40 + 7 * i
    )
    prios = [it["priority"] for it in sel.items]
    assert prios == sorted(prios, reverse=True)


def test_candidate_log_complete(tmp_path):
    cands, sel = setwords_flow(seed=11)
    select.write(tmp_path, sel)
    log = json.loads((tmp_path / "candidates.json").read_text(encoding="utf-8"))
    items = json.loads((tmp_path / "items.json").read_text(encoding="utf-8"))
    assert log["seed"] == 11 and items["seed"] == 11  # the seed is recorded
    assert len(log["candidates"]) == len(cands) >= 200
    assert [r["anchor_text"] for r in log["candidates"]] == [
        c.anchor_text for c in cands
    ]
    for r in log["candidates"]:
        assert r["status"] in STATUSES
        if r["status"].startswith("dropped:"):
            assert r["drop_reason"] == r["status"].split(":", 1)[1]
            assert r["item_id"] is None
        else:
            assert r["drop_reason"] is None and r["item_id"]
    assert (
        sum(r["status"] == "selected" for r in log["candidates"])
        == len(items["items"])
        == 12
    )
    assert (
        sum(r["status"] == "dropped:pre_rank" for r in log["candidates"])
        == len(cands) - 3 * 8
    )
    assert {r["item_id"] for r in log["candidates"] if r["item_id"]} == {
        i["item_id"] for i in items["items"]
    }
    # every item row matches its candidate row
    row_of = {r["item_id"]: r for r in log["candidates"] if r["item_id"]}
    for it in items["items"]:
        r = row_of[it["item_id"]]
        assert (it["anchor_text"], it["class"], it["priority"]) == (
            r["anchor_text"],
            r["class"],
            r["priority"],
        )
    # JSON as DESIGN 2.4 writes it
    text = (tmp_path / "candidates.json").read_text(encoding="utf-8")
    assert text.endswith("\n") and text == select.dumps(json.loads(text))
    assert str(tmp_path) not in text


def test_no_candidate_gives_an_empty_selection():
    sel = select.select([], 3, {"cap": 12})
    assert (sel.items, sel.candidates, sel.k, sel.ceiling) == ([], [], 0, 0)


def test_e4_item_with_zero_unnamed_hits_is_dropped_under_a_full_selection(tmp_path):
    """Deferred from Task 14: such an item keeps its pre_priority and loses to items with unnamed hits."""
    files = {
        "NOTES.md": "The 7 zebra stripes are here.\n",
        "ROOT_A.md": "The 8 lion manes are here.\n",
        "docs/a.md": "The 7 zebra stripes, 8 lion manes and 9 otter dens are here.\n",
    }
    repo = build_repo(tmp_path, extra=files).repo
    e4 = [
        "Edit `docs/a.md` so that it lists 7 zebra stripes.",
        "Edit `docs/a.md` so that it lists 8 lion manes.",
        "Edit `docs/a.md` so that it lists 9 otter dens.",
    ]
    others = [
        "C1",
        "C4",
        "C8",
        "C2",
        "C7",
    ]  # with C5 that makes k = 6 and a ceiling of 2
    text = "## Task 1: Change the guide\n\n" + "\n\n".join(e4) + "\n\n"
    text += "\n\n".join(sentence(c, i) for c in others for i in range(3)) + "\n"
    doc = plan.parse(text)
    reg = registry({c: rows(3) for c in others}, priority=lambda pre, i, cls: 90 + i)
    reg["E4"] = (extractors.find_e4, extractors.attach_e4)
    ctx = Ctx(doc, snapshot=repo, seed=4)
    cands = extractors.run_extractors(ctx, reg)
    sel = select.select(cands, 4, ctx.constants)
    c5 = sorted((c for c in cands if c.cls == "C5"), key=lambda c: c.priority)
    assert len(c5) == 3 and sel.k == 6 and len(sel.items) == 12
    zero, *rest = c5
    assert zero.features["unnamed_hits"] == 0 and zero.priority == zero.pre_priority
    assert all(
        c.features["unnamed_root_hits"] == 1 and c.priority > zero.priority
        for c in rest
    )
    assert zero.status.startswith("dropped:") and {c.status for c in rest} == {
        "selected"
    }
    assert zero.anchor_text not in [it["anchor_text"] for it in sel.items]


# ---------------------------------------------------------------- the rank table (DESIGN 5.2)

# DESIGN 5.2, typed again by hand: row -> (base, {signal: most it adds}, {signal: most it removes}, range)
DESIGN_52 = {
    "E1.completeness": (30, {"bound_none": 25, "scope_differs": 25, "extra_set_words": 10}, {}, (30, 90)),
    "E1.universal": (30, {"names_path": 20, "extra_set_words": 10, "limiter_line": 20, "enforcing_test": 20}, {}, (30, 100)),
    "E2": (25, {"no_match": 45, "near_miss": 20, "selector_zero": 5}, {}, (25, 95)),
    "E3": (40, {"long_stem": 10, "distinctive": 10, "unnamed_test_files": 45, "unnamed_other_files": 10, "gate_names_none": 10}, {"common_stem": 20}, (20, 100)),
    "E4": (30, {"count_change": 10, "long_needle": 10, "unnamed_root_hit": 20, "unnamed_hits": 30}, {}, (30, 100)),
    "E5": (30, {"missing_identifiers": 60}, {}, (45, 90)),
    "E6": (20, {"read_occurrences": 15}, {}, (25, 35)),
    "E7": (30, {"zero_overlap_clauses": 30, "shared_tokens": 10}, {}, (55, 70)),
}  # fmt: skip


def test_rank_table_holds_the_design_numbers():
    assert set(rank.RANK_TABLE) == set(DESIGN_52)
    for key, (base, plus, minus, rng) in DESIGN_52.items():
        row = rank.RANK_TABLE[key]
        assert (row["base"], row["plus"], row["minus"]) == (base, plus, minus), key
        assert (row["lo"], row["hi"]) == rng, key


def test_rank_table_sha256_is_published_and_moves_with_a_weight():
    text = rank.canonical()
    assert rank.rank_table_sha256 == hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert len(rank.rank_table_sha256) == 64
    assert json.loads(text) == json.loads(json.dumps(rank.RANK_TABLE))
    changed = json.loads(text)
    changed["E2"]["plus"]["no_match"] += 1
    assert rank.sha256(changed) != rank.rank_table_sha256


def test_rank_table_follows_the_extractor_constants(monkeypatch):
    # the table reads the constants the extractors use: changing one constant changes the table on a reload
    import importlib

    before = rank.rank_table_sha256
    monkeypatch.setattr(extractors, "E2_NO_MATCH", 46)
    try:
        importlib.reload(rank)
        assert rank.RANK_TABLE["E2"]["plus"]["no_match"] == 46
        assert rank.rank_table_sha256 != before
    finally:
        monkeypatch.undo()
        importlib.reload(rank)
    assert rank.RANK_TABLE["E2"]["plus"]["no_match"] == 45
    assert rank.rank_table_sha256 == before


def test_rank_table_agrees_with_the_priorities_the_extractors_give(tmp_path):
    """Every pre_priority and priority of the real extractors on p_basic.md lies in its table row's range."""
    repo = build_repo(tmp_path).repo
    doc = plan.parse((PLANS / "p_basic.md").read_text(encoding="utf-8"))
    src = plan.parse((PLANS / "source.md").read_text(encoding="utf-8"))
    ctx = Ctx(doc, source=src, snapshot=repo, seed=0)
    cands = extractors.run_extractors(ctx)
    assert {c.extractor for c in cands} == {"E1", "E2", "E3", "E4", "E5", "E6", "E7"}
    seen = set()
    for c in cands:
        row = rank.RANK_TABLE[rank.row_key(c.extractor, c.kind)]
        seen.add(rank.row_key(c.extractor, c.kind))
        assert row["lo"] <= c.pre_priority <= row["hi"], (c.extractor, c.kind)
        if c.evidence_computed:
            assert row["lo"] <= c.priority <= row["hi"], (c.extractor, c.kind)
    assert {
        "E1.completeness",
        "E1.universal",
        "E2",
        "E3",
        "E4",
        "E5",
        "E6",
        "E7",
    } <= seen
