"""T-1: panel-msg/1 coverage validator (R-06, R-08, R-38)."""
import json

import pytest
from conftest import CT, cand_text
from r5.panelmsg import Ctx, candidate_tasks, validate


def ctx(k=2, receivers=("t1b-1",)):
    return Ctx(candidate_tasks(cand_text(CT)), set(receivers), k, "row/pkg")


def card(**kw):
    c = {"v": "panel-msg/1", "id": "c-t1b-1-1", "run": "row/pkg", "from": "watcher", "to": "t1b-1", "t": 1731500000123,
         "kind": "coverage", "items": ["T9"]}
    c.update(kw)
    return json.dumps(c)


def test_accepts_good_cards():
    assert validate(card(), ctx())[0]
    assert validate(card(items=["T9", "T12"]), ctx())[0]
    c = ctx(receivers=("t4-1", "t3-1"))
    assert validate(card(to="t3-1", id="c-t3-1-1"), c)[0]


@pytest.mark.parametrize("key", ["claim", "severity", "category", "note", "n", "anchor", "move", "zzz"])
def test_rejects_forbidden_and_unknown_keys(key):
    c = json.loads(card())
    c[key] = "x"
    assert not validate(json.dumps(c), ctx())[0]


@pytest.mark.parametrize("line", [
    card(items=["T9"] * 1 + ["T1"] * 0, id="x" * 600),  # over 600 bytes
    card(**{"from": "t4-1"}),
    card(to="t3-1"),
    card(items=[]),
    card(items=["T1", "T2", "T3"]),
    card(items=["T9", "T9"]),
    card(items=["T99"]),
    card(items=["Task 9"]),
    "{not json",
])
def test_rejects_bad_lines(line):
    assert not validate(line, ctx())[0]


def test_size_limit_is_600_bytes():
    assert len(card(id="x" * 600).encode()) > 600


def test_duplicate_id_rejected():
    c = ctx()
    assert validate(card(), c)[0]
    assert not validate(card(), c)[0]
