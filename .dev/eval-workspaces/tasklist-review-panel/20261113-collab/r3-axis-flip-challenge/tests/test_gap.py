import json
import random

from conftest import ANCH, R3, cand_line, candidate
from superclaude.cli.review import findings as F

from r3lib import digest

RT = json.loads((R3 / "config/routing.json").read_text())
CAND = candidate()


def test_gap_share():
    n_gap = n = 0
    for s in range(1000):
        rng = random.Random(s)
        slots = digest.fill_slots(1, ["r"] * 5, ["g"] * 5, rng, RT["gap_probability"])
        n += 1
        n_gap += slots[0]["slot_type"] == "gap"
    assert abs(n_gap / n - 0.333) <= 0.045


def test_deterministic():
    a = digest.fill_slots(3, list("abc"), list("xyz"), random.Random(7), 1 / 3)
    b = digest.fill_slots(3, list("abc"), list("xyz"), random.Random(7), 1 / 3)
    assert a == b


def test_gap_never_overlaps_anchor_spans():
    anchors = [cand_line(ANCH[k]) for k in ANCH]
    pool = digest.gap_pool(CAND, anchors, RT, random.Random(1))
    assert pool
    spans = [s for a in anchors for s in F.locate(CAND, a)]
    for g in pool:
        for a, b in F.locate(CAND, g):
            assert not any(x <= a < y for x, y in spans)


def test_empty_real_queue():
    slots = digest.fill_slots(
        6, [], ["g1", "g2", "g3", "g4", "g5", "g6"], random.Random(3), 1 / 3
    )
    for s in slots:
        if s["slot_type"] == "real":
            assert s["item"] is None
        else:
            assert s["item"] is not None


def test_gap_and_real_render_alike():
    cat = json.loads((R3 / "config/catalogue.json").read_text())
    real = {"anchor": cand_line(ANCH["only"]), "move": "M3", "from": "t2b-1"}
    gap = {"anchor": cand_line(ANCH["never"]), "move": "M8", "from": "t2b-1"}
    meta = {"to": "t4-1", "run": "r/p", "t_ms": 1}
    lr, lg = (json.loads(x) for x in digest.render_lines([real, gap], meta))
    assert list(lr) == list(lg)
    p = digest.render_prompt(
        [real, gap],
        (R3 / "config/phase2-frame.txt").read_text(),
        cat,
        {"cand": "/c", "sha": "s", "src": "/s"},
    )
    for word in ("gap", "real", "decoy", "t2b-1", "t4-1"):
        assert word not in p.lower().replace("really", "")
    for line in digest.render_lines([real, gap], meta):
        o = json.loads(line)
        assert not ({"gap", "real", "decoy"} & set(o)) and "gap" not in o["kind"]
