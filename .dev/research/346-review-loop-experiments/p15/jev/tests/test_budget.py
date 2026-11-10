import multiprocessing
import pytest

from jevlib.budget import Budget, BudgetExhausted
from jevlib.client import JevClient
from jevlib.journal import Journal
from jevlib.questions import noul


def mkb(tmp_path, usd=1.0, tok=1_000_000, name="b.json"):
    return Budget(tmp_path / name, ceiling_usd=usd, ceiling_input_tokens=tok)


def test_reserve_phase_refuses_when_over_ceiling(tmp_path):
    b = mkb(tmp_path, tok=1000)
    b.reserve_phase("p1", 600)
    with pytest.raises(BudgetExhausted):
        b.reserve_phase("p2", 500)
    b.reserve_phase("p2", 400)
    assert b.state()["committed_tokens"] == 1000


def test_draw_and_settle_actual(tmp_path):
    b = mkb(tmp_path)
    b.reserve_phase("p", 1000)
    d = b.draw("p", 300)
    assert b.state()["committed_tokens"] == 1000
    b.settle(d, 120)
    s = b.state()
    assert s["spent_tokens"] == 120 and s["committed_tokens"] == 820
    assert abs(s["spent_usd"] - 120 * 0.042 / 1e6) < 1e-12


def test_usage_missing_charged_at_estimate(tmp_path):
    b = mkb(tmp_path)
    d = b.draw("free", 500)
    b.settle(d, None)
    assert b.state()["spent_tokens"] == 500
    import json
    assert json.loads((tmp_path / "b.json").read_text())["draws"][d]["usage_missing"] is True


def test_release_returns_unused(tmp_path):
    b = mkb(tmp_path, tok=1000)
    b.reserve_phase("p", 900)
    with pytest.raises(BudgetExhausted):
        b.reserve_phase("q", 500)
    d = b.draw("p", 100); b.settle(d, 100)
    b.release_phase("p")
    assert b.state()["committed_tokens"] == 100
    b.reserve_phase("q", 800)


def test_token_ceiling_binds_before_usd(tmp_path):
    b = mkb(tmp_path, usd=100.0, tok=1000)
    with pytest.raises(BudgetExhausted):
        b.reserve_phase("p", 1001)
    b2 = mkb(tmp_path, usd=0.0001, tok=10**12, name="b2.json")     # USD binds: 0.0001 / 0.042e-6 = 2380 tokens
    with pytest.raises(BudgetExhausted):
        b2.reserve_phase("p", 2400)
    b2.reserve_phase("p", 2300)


def test_draw_beyond_reservation_uses_global_headroom(tmp_path):
    b = mkb(tmp_path, tok=1000)
    b.reserve_phase("p", 100)
    b.draw("p", 400)                     # overflows the reservation but fits globally
    with pytest.raises(BudgetExhausted):
        b.draw("p", 700)


def _worker(path, n, out):
    b = Budget(path, ceiling_usd=10.0, ceiling_input_tokens=10**9)
    for _ in range(n):
        d = b.draw("p", 10)
        b.settle(d, 7)


def test_concurrent_draws_locked(tmp_path):
    path = tmp_path / "c.json"
    Budget(path, ceiling_usd=10.0, ceiling_input_tokens=10**9)
    ps = [multiprocessing.Process(target=_worker, args=(path, 40, None)) for _ in range(2)]
    [p.start() for p in ps]; [p.join() for p in ps]
    assert all(p.exitcode == 0 for p in ps)
    s = Budget(path, ceiling_usd=10.0, ceiling_input_tokens=10**9).state()
    assert s["spent_tokens"] == 80 * 7
    import json
    assert len(json.loads(path.read_text())["draws"]) == 80


def test_budget_exhausted_mid_phase_is_refused_not_raised_by_ask(tmp_path):
    b = mkb(tmp_path, tok=50)
    c = JevClient(experiment="T", phase="p", budget=b, journal=Journal(tmp_path / "j.jsonl"), live=False)
    r = c.ask({"m": "hello"}, {"q": noul("Is it?", "yes it is", "no it is not")}, case_id="x", qset_version="v",
              data_classes={"synthetic"}, purpose="t")
    assert (r.status, r.error) == ("refused", "budget_exhausted")
