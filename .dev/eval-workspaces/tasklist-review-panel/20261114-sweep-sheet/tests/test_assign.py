"""Item-to-reviewer assignment (DESIGN 7, TESTING REQ-20) on synthetic item lists; no repository, no model."""

import itertools

import pytest

from sweep import assign

PANELS = assign.load_panels()
SEARCH_CLASSES = ("C4", "C5", "C6", "C8")
READ_CLASSES = ("C1", "C2", "C3", "C7")
EV = [{"path": "a.py", "line": 1, "text": "x"}]


def item(n, route, evidence=True, cls=None, priority=None):
    cls = cls or (SEARCH_CLASSES if route == "search" else READ_CLASSES)[n % 4]
    return {
        "item_id": f"S{n}",
        "class": cls,
        "route": route,
        "priority": 100 - n if priority is None else priority,
        "evidence": list(EV) if evidence else [],
    }


def twelve(routes):
    """12 items with evidence, priority descending in list order; `routes` is a string of s (search) and r (read)."""
    return [item(n, "search" if c == "s" else "read") for n, c in enumerate(routes, 1)]


def check_invariants(items, a):
    for rid, ids in a.reviewers.items():
        assert len(ids) <= a.caps[rid]
    for it in items:
        who = a.item_reviewers.get(it["item_id"], [])
        assert len(who) == len(set(who)) <= 2
        if not who:
            assert a.dropped[it["item_id"]] == "dropped:cap_slots"
        else:
            assert it["item_id"] not in a.dropped
        for rid in who:
            assert it["item_id"] in a.reviewers[rid]
    assert sum(len(v) for v in a.reviewers.values()) == sum(
        len(v) for v in a.item_reviewers.values()
    )


def test_caps_sum_24_all_panels():
    assert set(PANELS) == {"primary", "haiku", "sonnet"}
    for name, cfg in PANELS.items():
        assert sum(cfg[r]["cap"] for r in assign.ROLES) == 24, name
    assert [PANELS["primary"][r]["cap"] for r in assign.ROLES] == [8, 8, 8]
    assert [PANELS["haiku"][r]["cap"] for r in assign.ROLES] == [6, 9, 9]
    assert [PANELS["sonnet"][r]["cap"] for r in assign.ROLES] == [6, 9, 9]
    a = assign.assign(twelve("srsrsrsrsrss"), "sonnet", seed=3)
    assert a.caps == {"t1b-1": 6, "t4-1": 9, "t3-1": 9}


@pytest.mark.parametrize(
    "routes",
    [
        "sssssssrrrrr",
        "rrrrrsssssss",
        "srsrsrsrsrss",
        "rsrsrsrsrsss",
        "ssrrssrrssrs",
        "srrsssrssrsr",
    ],
)
def test_primary_12_items_fills_caps(routes):
    items = twelve(routes)
    assert routes.count("s") == 7
    a = assign.assign(items, "primary", seed=1)
    assert a.loads == {"t2b-1": 8, "t4-1": 8, "t3-1": 8}
    assert sum(a.loads.values()) == 24 == sum(a.replicas.values())
    assert not a.replica_dropped and not a.dropped
    check_invariants(items, a)


def test_primary_every_search_read_arrangement_fills_caps():
    """All 792 ways to place 7 search items among 12 priorities end at 8, 8, 8 (the pass-2 retry, DESIGN 7.2 worked check)."""
    for pos in itertools.combinations(range(12), 7):
        items = twelve("".join("s" if n in pos else "r" for n in range(12)))
        a = assign.assign(items, "primary", seed=1)
        assert a.loads == {"t2b-1": 8, "t4-1": 8, "t3-1": 8}, pos
        assert not a.replica_dropped and not a.dropped, pos
        check_invariants(items, a)


def test_haiku_only_evidence_items():
    # evidence-bearing C4/C5/C8 are allowed; an empty-evidence C4, a C6 search item and read items are not
    items = [
        item(1, "search", cls="C4"),
        item(2, "search", cls="C6"),
        item(3, "search", evidence=False, cls="C4"),
        item(4, "search", cls="C5"),
        item(5, "read", cls="C1"),
        item(6, "search", cls="C8"),
        item(7, "read", cls="C7"),
        item(8, "search", cls="C8"),
        item(9, "search", cls="C5"),
        item(10, "read", cls="C2"),
        item(11, "search", cls="C4"),
        item(12, "search", cls="C6"),
    ]
    a = assign.assign(items, "haiku", seed=2)
    by_id = {it["item_id"]: it for it in items}
    s_items = a.reviewers["t2-1"]
    assert s_items, "the haiku reviewer takes the allowed items"
    for iid in s_items:
        assert by_id[iid]["evidence"] and by_id[iid]["class"] in ("C4", "C5", "C8")
    assert a.loads["t2-1"] <= 6
    check_invariants(items, a)
    # the allowed items fill the haiku reviewer first: all six allowed items are on it
    allowed = {"S1", "S4", "S6", "S8", "S9", "S11"}
    assert set(s_items) == allowed
    # no S reviewer when it may take none
    none_allowed = [item(n, "search", cls="C6") for n in range(1, 5)]
    b = assign.assign(none_allowed, "haiku", seed=2)
    assert b.reviewers["t2-1"] == []
    assert all(len(v) == 2 for v in b.item_reviewers.values())


def test_no_evidence_replica_1():
    items = [
        item(1, "search", evidence=False),
        item(2, "read", evidence=False),
        item(3, "read"),
    ]
    a = assign.assign(items, "primary", seed=4)
    assert a.replicas == {"S1": 1, "S2": 1, "S3": 2}
    assert len(a.item_reviewers["S1"]) == 1
    assert len(a.item_reviewers["S2"]) == 1
    assert len(a.item_reviewers["S3"]) == 2
    assert not a.replica_dropped
    check_invariants(items, a)


@pytest.mark.parametrize("panel", ["primary", "haiku", "sonnet"])
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_no_duplicate_reviewer_per_item(panel, seed):
    for routes in ("sssssssrrrrr", "rrrrrrrrrrrr", "ssssssssssss", "srsrsrsrsrsr"):
        items = twelve(routes)
        a = assign.assign(items, panel, seed=seed)
        for iid, who in a.item_reviewers.items():
            assert len(who) == len(set(who)), (panel, routes, iid)
        check_invariants(items, a)


def test_replica_dropped_lowest_priority_first_and_cap_slots():
    # haiku panel, 12 read items: S may take none, the lunas hold 18 slots for 24 wanted
    items = twelve("rrrrrrrrrrrr")
    a = assign.assign(items, "haiku", seed=0)
    assert a.loads == {"t2-1": 0, "t4-1": 9, "t3-1": 9}
    assert a.replica_dropped == ["S7", "S8", "S9", "S10", "S11", "S12"]
    assert not a.dropped
    check_invariants(items, a)
    # one reviewer left (cap 8): 12 items, 8 kept (descending priority), 4 logged dropped:cap_slots
    b = assign.assign(items, "primary", available={"t4-1"}, seed=0)
    assert b.loads == {"t4-1": 8}
    assert b.dropped == {f"S{n}": "dropped:cap_slots" for n in range(9, 13)}
    assert set(b.reviewers["t4-1"]) == {f"S{n}" for n in range(1, 9)}
    check_invariants(items, b)


def test_failure_never_raises_survivor_load():
    items = twelve("sssssssrrrrr")
    for panel in PANELS:
        a = assign.assign(items, panel, seed=5)
        for dead in list(a.reviewers):
            b = assign.fail(a, dead)
            assert dead not in b.reviewers and dead not in b.caps
            for rid in b.reviewers:
                assert b.reviewers[rid] == a.reviewers[rid]  # same items, same order
                assert len(b.reviewers[rid]) == len(a.reviewers[rid]) <= b.caps[rid]
            assert set(b.lost_replica) == set(a.reviewers[dead])
            assert all(dead not in who for who in b.item_reviewers.values())
            # a second failure on top of the first keeps the same property
            for dead2 in list(b.reviewers):
                c = assign.fail(b, dead2)
                for rid in c.reviewers:
                    assert c.reviewers[rid] == a.reviewers[rid]
        assert a.lost_replica == []  # the input is not modified
    with pytest.raises(ValueError):
        assign.fail(assign.assign(items, "primary", seed=5), "nobody")


def test_two_reviewers_replica_1():
    items = twelve("sssssssrrrrr")
    for avail in ({"t4-1", "t3-1"}, {"t2b-1", "t3-1"}):
        a = assign.assign(items, "primary", available=avail, seed=6)
        assert set(a.reviewers) == avail
        assert set(a.replicas.values()) == {1}
        assert all(len(who) == 1 for who in a.item_reviewers.values())
        assert not a.dropped and not a.replica_dropped
        for rid, ids in a.reviewers.items():
            assert (
                len(ids)
                <= PANELS["primary"][{"t2b-1": "S", "t4-1": "L1", "t3-1": "L2"}[rid]][
                    "cap"
                ]
            )
        check_invariants(items, a)
    # S and one luna in the haiku panel (caps 6 and 9): replica 1, the haiku restriction and the caps still hold
    b = assign.assign(
        twelve("ssssssssssss"), "haiku", available={"t2-1", "t4-1"}, seed=6
    )
    assert b.loads["t2-1"] <= 6 and b.loads["t4-1"] <= 9
    assert set(b.replicas.values()) == {1}
    assert sum(b.loads.values()) == 12 - len(b.dropped)


def test_order_shuffled_per_reviewer_deterministic():
    items = twelve("sssssssrrrrr")
    a = assign.assign(items, "primary", seed=7)
    again = assign.assign(items, "primary", seed=7)
    assert a.to_json() == again.to_json()
    # a reviewer's list is a permutation of what it was given, not the priority order
    for rid, ids in a.reviewers.items():
        assert sorted(ids) == sorted(set(ids))
    assert any(
        ids != sorted(ids, key=lambda i: int(i[1:])) for ids in a.reviewers.values()
    )

    # the two lunas share items; some seed gives them different relative orders, and the order follows the seed
    def common(x):
        shared = set(x.reviewers["t4-1"]) & set(x.reviewers["t3-1"])
        return {r: [i for i in x.reviewers[r] if i in shared] for r in ("t4-1", "t3-1")}

    assert any(
        common(assign.assign(items, "primary", seed=s))["t4-1"]
        != common(assign.assign(items, "primary", seed=s))["t3-1"]
        for s in range(6)
    )
    orders = {
        tuple(assign.assign(items, "primary", seed=s).reviewers["t4-1"])
        for s in range(6)
    }
    assert len(orders) > 1
    # the shuffle does not change who gets what
    other = assign.assign(items, "primary", seed=8)
    assert {r: sorted(v) for r, v in other.reviewers.items()} == {
        r: sorted(v) for r, v in a.reviewers.items()
    }
