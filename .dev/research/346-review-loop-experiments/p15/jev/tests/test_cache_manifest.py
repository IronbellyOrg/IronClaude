import json

import pytest

from jevlib.budget import Budget
from jevlib.cache import ResponseCache
from jevlib.client import JevClient
from jevlib.journal import Journal
from jevlib.manifest import update
from jevlib.questions import build_request, noul
from jevlib.transport import MockStep, MockTransport, fake_answer

ST = {"m": "hello"}


def qs(true="It is so."):
    return {"q": noul("Is it so?", true, "It is not so.")}


def mk(tmp_path, steps, cache, phase="calibration", journal="j.jsonl"):
    b = Budget(tmp_path / "b.json", ceiling_usd=1.0, ceiling_input_tokens=10**7)
    t = MockTransport(steps)
    c = JevClient(experiment="T", phase=phase, budget=b, journal=Journal(tmp_path / journal), transport=t, live=True,
                  cache=cache, sleep=lambda s: None)
    return c, t


def go(c, q=None, cls=None):
    return c.ask(ST, q or qs(), case_id="a", qset_version="v", data_classes=cls or {"synthetic"}, purpose="t")


@pytest.fixture(autouse=True)
def _key(monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", "FAKEJEVKEY" + "7" * 30)


def body(q=None):
    return fake_answer(build_request(ST, q or qs()), 1, 0.3)


def test_cache_hit_same_request(tmp_path):
    cache = ResponseCache(tmp_path / "cache")
    c, t = mk(tmp_path, [MockStep(200, body())], cache)
    r1 = go(c)
    r2 = go(c)
    assert r1.status == r2.status == "ok" and len(t.calls) == 1
    assert r2.attempts == 0 and r2.answers == r1.answers


def test_cache_invalidated_by_wording_change(tmp_path):
    cache = ResponseCache(tmp_path / "cache")
    q2 = qs("It is certainly so.")
    c, t = mk(tmp_path, [MockStep(200, body()), MockStep(200, body(q2))], cache)
    go(c); go(c, q2)
    assert len(t.calls) == 2


def test_cache_invalidated_by_model_change(tmp_path):
    cache = ResponseCache(tmp_path / "cache")
    r = build_request(ST, qs())
    r2 = build_request(ST, qs(), model="jev-1.13.0")
    from jevlib.questions import request_sha256
    assert request_sha256(r) != request_sha256(r2)


def test_cache_forbidden_in_live_phase(tmp_path):
    with pytest.raises(ValueError):
        mk(tmp_path, [], ResponseCache(tmp_path / "cache"), phase="live")
    with pytest.raises(ValueError):
        ResponseCache(tmp_path / "c2", phase="live")


def test_cache_stores_only_ok(tmp_path):
    cache = ResponseCache(tmp_path / "cache")
    c, t = mk(tmp_path, [MockStep(422, {"d": 1}), MockStep(200, body())], cache)
    assert go(c).status == "invalid"
    assert go(c).status == "ok" and len(t.calls) == 2


def test_manifest_counts_by_class(tmp_path):
    c, t = mk(tmp_path, [MockStep(200, body()), MockStep(200, body())], None, phase="smoke")
    go(c, cls={"synthetic"})
    c.ask({"m": "spec text"}, qs(), case_id="b", qset_version="v", data_classes={"s1_spec"}, purpose="t")
    out = update(tmp_path / "j.jsonl", tmp_path / "manifest.json")
    assert out["counts"]["smoke"]["synthetic"]["logical_calls"] == 1
    assert out["counts"]["smoke"]["s1_spec"]["logical_calls"] == 1
    assert out["counts"]["smoke"]["synthetic"]["input_tokens"] > 0
    assert out["models"] == ["jev-1.14.0"] and out["first_ts"] <= out["last_ts"]
    assert json.loads((tmp_path / "manifest.json").read_text())["schema"] == "jev-manifest/1"
