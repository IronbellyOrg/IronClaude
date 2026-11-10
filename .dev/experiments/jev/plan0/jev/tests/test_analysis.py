import json
import math

import pytest

from p15common import analysis as A
from p15common import harnesslib as H

AUD_OUT = H.AUD_OUT


def test_baseline_sonnet_blk_1_50_from_files():
    b = A.baseline_sonnet()
    assert b["n_audits"] == 12 and abs(b["B_BLK"] - 1.50) < 1e-9
    assert b["provisional"] is False and b["single_audit"] is False
    assert b["loop_pass"] == "6/6" and b["escalations"] == 0 and b["a_base"] == 100424 and b["b_base"] == 169468


def test_replicas_1_50_each():
    b = A.baseline_sonnet()
    assert abs(b["AUD1"] - 1.50) < 1e-9 and abs(b["AUD2"] - 1.50) < 1e-9


def test_growth_mean_median():
    b = A.baseline_sonnet()
    assert round(b["growth_mean_pct"], 2) == 1.41 and round(b["growth_median_pct"], 2) == 0.97


def test_baseline_sonnet_constants_fallback_are_provisional(tmp_path):
    b = A.baseline_sonnet(None, runs_dir=tmp_path / "none", audit2_dir=tmp_path / "none2")
    assert b["provisional"] is True and b["B_BLK"] == 1.50 and b["n_audits"] == 0 and b["growth_mean_pct"] == 1.41


def test_d6_table():
    for L, want in ((1.8, 2.35), (2.0, 2.69), (1.25, 1.42), (1.5, 1.84), (1.65, 2.10)):
        assert A.d6_limit(L) == want, L
    dec = {"baseline": {"a_base": 100424, "audit_base": 69044, "b_base": 169468}}
    assert A.d6_limit(1.25, dec) == 1.42


def test_cost_ratios_loop_only_and_b_reported():
    r = A.cost_ratios(100424, 69044)
    assert abs(r["R_LOOP"] - 1.0) < 1e-12 and abs(r["R_B"] - 1.0) < 1e-12 and r["A"] == 100424 and r["B"] == 169468
    r = A.cost_ratios(150000, 70000)
    assert math.isclose(r["R_LOOP"], 150000 / 100424) and math.isclose(r["R_B"], 220000 / 169468)
    assert A.cost_ratios(None, None)["R_LOOP"] is None


def test_final_verdict_haiku_pending_and_disagree():
    assert A.final_verdict("ADOPT", "pending") == "ADOPT (Haiku robustness pending)"
    assert A.final_verdict("ADOPT", "agrees") == "ADOPT"
    assert A.final_verdict("ADOPT", "disagrees") == "INCONCLUSIVE"
    assert A.final_verdict("DROP", "agrees") == "DROP"
    assert A.final_verdict("INCONCLUSIVE", "pending") == "INCONCLUSIVE"


def test_haiku_condition_states():
    hb = {"H_BLK": 2.0, "fail_rate": 0.17, "provisional": True}
    ok = [{"complete": True, "BLK": 1.0, "harness_failure": False} for _ in range(4)]
    assert A.haiku_condition(ok, hb)["state"] == "agrees"
    assert abs(A.haiku_condition(ok, hb)["HR"] - 0.5) < 1e-12
    worse = [{"complete": True, "BLK": 2.5, "harness_failure": False} for _ in range(4)]
    assert A.haiku_condition(worse, hb)["state"] == "disagrees"
    failing = ok[:2] + [{"complete": False, "harness_failure": True}] * 2
    assert A.haiku_condition(failing, hb)["state"] == "disagrees"          # failure rate 0.5 > 0.17 + 0.25
    assert A.haiku_condition([], hb)["state"] == "pending"
    assert A.haiku_condition(ok, None)["state"] == "pending"


def row(**kw):
    r = {"arm": "g3c", "arm_label": "x", "stratum": "sonnet", "role": "test", "n_planned": 6, "n_completed": 6, "runs_dir": "/x",
         "metrics": {k: None for k in A.METRIC_KEYS}, "design_metrics": {}, "haiku": None,
         "jev": {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0, "model": "jev-1.14.0"},
         "verdict": "INCONCLUSIVE", "rule": "r", "extension_used": False}
    r.update(kw)
    return r


def test_extension_once_only():
    res = {"rows": [row(), row(arm="g3b", role="control", verdict="CONTROL")]}
    assert A.extension_allowed(res) is True
    assert A.extension_allowed({"rows": [row(verdict="ADOPT")]}) is False
    assert A.extension_allowed({"rows": [row(extension_used=True, n_planned=9)]}) is False
    assert A.extension_allowed({"rows": [row(n_planned=9)]}) is False
    assert A.extension_allowed({"rows": [row(stratum="haiku")]}) is False


def good_results():
    return {"experiment": "E3", "design_id": "p15-E3", "decision_file": {"path": "/x", "sha256": "0"}, "stage": "live",
            "status": "complete", "rows": [row()], "blocked_downstream": [], "notes": []}


def test_write_results_rejects_bad_verdict(tmp_path):
    p = tmp_path / "results.json"
    A.write_results(p, good_results())
    d = json.loads(p.read_text())
    assert d["schema"] == "p15-results/1" and d["generated_utc"]
    bad = good_results(); bad["rows"][0]["verdict"] = "WINNER"
    p2 = tmp_path / "bad.json"
    with pytest.raises(ValueError, match="verdict"):
        A.write_results(p2, bad)
    assert not p2.exists()
    bad = good_results(); del bad["rows"][0]["metrics"]["R_LOOP"]
    with pytest.raises(ValueError, match="R_LOOP"):
        A.write_results(p2, bad)
    bad = good_results(); del bad["rows"][0]["rule"]
    with pytest.raises(ValueError):
        A.write_results(p2, bad)
    assert not p2.exists()


def _haiku_dir(tmp_path, with_aud2):
    base = tmp_path / "hb"
    (base / "runs").mkdir(parents=True)
    runs = []
    for k in (1, 2):
        run = f"a3-r{k}"
        for sub, ok in (("aud", True), ("aud2", with_aud2)):
            if ok:
                f = base / "runs" / run / sub / "ws" / AUD_OUT
                f.parent.mkdir(parents=True)
                f.write_text("review\nBlocking finding ids: B1, B2.\n\n## B1 something\nbody\n\n## B2 other\nbody\n\nverdict: FAIL\n")
        runs.append({"run": run, "loop_verdict": "PASS", "reviews": 2, "growth_pct": 3.0, "loop_tokens": 100000,
                     "audit_tokens": 50000, "audit1_blocking": 9})
    (base / "results.json").write_text(json.dumps({"runs": runs, "harness_failure_rate": 0.17}))
    return base / "results.json"


def test_baseline_haiku_single_audit_flag(tmp_path):
    p = _haiku_dir(tmp_path, with_aud2=False)
    hb = A.baseline_haiku(None, path=p)
    assert hb["single_audit"] is True and hb["provisional"] is True and hb["n"] == 2
    assert hb["H_BLK"] == 2.0 and hb["H_LOOP"] == 100000 and hb["loop_pass"] == 2 and hb["fail_rate"] == 0.17
    p2 = _haiku_dir(tmp_path / "two", with_aud2=True)
    hb2 = A.baseline_haiku(None, path=p2)
    assert hb2["single_audit"] is False and hb2["n_audits"] == 4
    assert A.baseline_haiku(None, path=tmp_path / "missing.json") is None
    real = A.baseline_haiku(None)         # the real p14 file, whatever its state today
    assert real is None or real["n"] >= 1 and isinstance(real["single_audit"], bool)


def test_run_metrics_and_arm_summary(tmp_path):
    cfg = H.ExpConfig(root=tmp_path / "e", design_id="d", pattern_root="e", run_rx=".*", decision_path=tmp_path / "d.toml",
                      loop_steps=["R1", "J1", "V1", "R2"], coordinator_steps={"J1"})
    states = []
    for k, (b1, b2, loop_end) in enumerate([(2, 1, "PASS"), (0, 0, "VERIFIED-PASS"), (3, 3, "ESCALATED")], 1):
        run = f"g9b-r{k}"
        for sub, nb in (("aud", b1), ("aud2", b2)):
            f = cfg.runs_dir / run / sub / "ws" / AUD_OUT
            f.parent.mkdir(parents=True, exist_ok=True)
            ids = ", ".join(f"B{i}" for i in range(1, nb + 1))
            body = "".join(f"\n## B{i} thing\nbody\n" for i in range(1, nb + 1))
            f.write_text(f"Blocking finding ids: {ids}.\n{body}\nverdict: {'FAIL' if nb else 'PASS'}\n")
        states.append({"run": run, "arm": "g9b", "stratum": "sonnet", "complete": True, "lost": False, "relaunch": {}, "manual": [],
                       "loop_end": loop_end, "final_spec": {"bytes": 57763 + 577},
                       "log": {"R1": {"output_tokens": 1000}, "J1": {"kind": "coordinator", "output_tokens": 0},
                               "V1": {"output_tokens": 500}, "R2": {"output_tokens": 700},
                               "AUD": {"output_tokens": 300}, "AUD2": {"output_tokens": 100}}})
    states.append({"run": "g9b-r4", "arm": "g9b", "stratum": "sonnet", "complete": False, "lost": True, "relaunch": {}, "manual": [], "log": {}})
    ms = [A.run_metrics(s, cfg) for s in states]
    assert ms[0]["BLK"] == 1.5 and ms[0]["LOOP"] == 2200 and ms[0]["AUD_tokens"] == 200 and ms[0]["reviews"] == 2 and ms[0]["fix_cycles"] == 1
    assert abs(ms[0]["growth_pct"] - 1.0) < 0.01 and ms[2]["escalated"] is True and ms[3]["complete"] is False and ms[3]["harness_failure"]
    s = A.arm_summary(ms)
    assert s["n_completed"] == 3 and s["loop_pass"] == "2/3" and s["escalations"] == 1
    assert abs(s["BLK"] - 1.5) < 1e-9 and s["A_mean"] == 2200 and s["B_mean"] == 2400 and s["AUD1"] == (2 + 0 + 3) / 3


def test_replica_agreement():
    def rule(runs, which):
        return "ADOPT" if sum(runs[w] for w in which) < 2 else "DROP"
    agree, det = A.replica_agreement(rule, {1: 1, 2: 1})
    assert agree and det == {"audit1": "ADOPT", "audit2": "ADOPT"}
    agree, det = A.replica_agreement(rule, {1: 1, 2: 5})
    assert not agree
