import pytest

from p15common import datasets as DS
from p15common import labels as LB


def case(cid, group, **kw):
    c = {"case_id": cid, "group": group, "family": "f", "category": "c", "variant": "base", "split": "calibration",
         "data_classes": ["synthetic"], "source": {"kind": "synthetic", "paths": [], "url": None},
         "packet": {"before": "a", "after": "b"}, "author_intent": {"expect": "closed"}}
    c.update(kw)
    return c


def test_split_groups_keeps_variants_together():
    groups = [f"g{i}" for i in range(20)]
    sp = DS.split_groups(groups * 3, 7, {"calibration": 10, "heldout": 10})
    assert set(sp) == set(groups) and sorted(set(sp.values())) == ["calibration", "heldout"]
    assert sum(1 for v in sp.values() if v == "heldout") == 10
    # variants of a base case share a group, hence a split
    cases = [case(f"g3-v{i}", "g3") for i in range(4)]
    assert len({sp[c["group"]] for c in cases}) == 1


def test_split_deterministic():
    groups = [f"g{i}" for i in range(15)]
    a = DS.split_groups(groups, 3, {"calibration": 0.6, "heldout": 0.4})
    b = DS.split_groups(list(reversed(groups)), 3, {"calibration": 0.6, "heldout": 0.4})
    c = DS.split_groups(groups, 4, {"calibration": 0.6, "heldout": 0.4})
    assert a == b and a != c
    assert sum(v == "calibration" for v in a.values()) == 9
    with pytest.raises(ValueError):
        DS.split_groups(groups, 1, {"x": 10, "y": 10})


def test_label_packet_strips_author_intent(tmp_path):
    c = case("c1", "g1")
    p = DS.label_packet(c, ["before", "after"])
    assert p == {"case_id": "c1", "packet": {"before": "a", "after": "b"}}
    assert "author_intent" not in str(p) and "split" not in p and "variant" not in str(p)
    assert DS.label_packet(c, ["before"])["packet"] == {"before": "a"}
    bad = case("c2", "g1", packet={"nested": {"author_intent": 1}})
    with pytest.raises(ValueError):
        DS.write_case(tmp_path / "x.json", bad)
    DS.write_case(tmp_path / "cal" / "c1.json", c)
    assert DS.load_cases(tmp_path)[0]["case_id"] == "c1"
    with pytest.raises(ValueError):
        DS.write_case(tmp_path / "y.json", {k: v for k, v in c.items() if k != "group"})


def _labels(pairs):
    l1 = {f"c{i}": {"closed": a} for i, (a, b) in enumerate(pairs)}
    l2 = {f"c{i}": {"closed": b} for i, (a, b) in enumerate(pairs)}
    return l1, l2


def test_kappa_known_values():
    pairs = [("yes", "yes")] * 20 + [("yes", "no")] * 5 + [("no", "yes")] * 10 + [("no", "no")] * 15
    l1, l2 = _labels(pairs)
    r = LB.agreement(l1, l2, ["closed"])["closed"]
    assert r["n"] == 50 and abs(r["raw"] - 0.7) < 1e-9 and abs(r["kappa"] - 0.4) < 1e-9
    l1, l2 = _labels([("yes", "yes")] * 5 + [("no", "no")] * 5)
    assert LB.agreement(l1, l2, ["closed"])["closed"]["kappa"] == 1.0


def test_merge_truth_disputes_listed():
    l1 = {"c1": {"closed": "yes", "confidence": "high"}, "c2": {"closed": "yes", "confidence": "high"},
          "c3": {"closed": "no", "confidence": "low"}, "c4": {"closed": "no", "confidence": "high"}}
    l2 = {"c1": {"closed": "yes", "confidence": "high"}, "c2": {"closed": "no", "confidence": "high"},
          "c3": {"closed": "no", "confidence": "high"}, "c4": {"closed": "no", "confidence": "high"}}
    adj = LB.to_adjudicate(l1, l2, ["closed"])
    assert adj == ["c2", "c3"]
    a = {"c2": {"closed": "no", "reason": "text shows it is not closed"}, "c3": {"closed": "undecidable", "reason": "unclear"}}
    truth, disputes = LB.merge_truth(l1, l2, a, ["closed"])
    assert truth["c1"] == {"closed": "yes"} and truth["c2"] == {"closed": "no"} and truth["c4"] == {"closed": "no"}
    assert [d["case_id"] for d in disputes] == ["c2", "c3"]
    assert disputes[0]["reason"] == "text shows it is not closed" and disputes[1]["unresolved"] is True
