# ruff: noqa: N803  (B is the design's own symbol)
"""Owner-authorised time-cap exception (OVERRIDE.md): TIME_CAP_EXCEPTION=1 on and off.

Pure rule (values.cap_exception), the deadlines CLI, launch.sh (row id, stamps, refusals, hook K), collab_summary columns,
results row stamp and columns, and alarms.py keeping the exception rows apart from the rows that obeyed the cap.
"""

import copy
import hashlib
import importlib.util
import json
import re

import pytest
from conftest import R1, TOOLS, Pkg, jload, run
from test_alarms import P as ALARM_PKG
from test_alarms import alarms
from test_alarms import row as alarm_row
from test_launch import DS, L
from test_results import AL, DE, build, results

spec = importlib.util.spec_from_file_location("values", TOOLS / "values.py")
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)

# the real el2 / design-package values (values/el2/TASK-WF-design-20261108-041415.json): both roles measured k = 0
VAL = {"critical_role": "reader", "finish_offset_s": 40.17760022888186, "guard_offset_s": 40.17760022888186, "hang_offset_s": 145.464,
       "k": {"reader": 0, "searcher": 0}, "panel": "el2", "pkg": DE, "B_f": 96.976,
       "turn_p90": {"searcher": 4.765, "reader": 26.275}, "T_report_p90": {"searcher": 9.445, "reader": 64.465},
       "E_p90": {"searcher": 56.922, "reader": 123.56}, "source_runs": ["el2-c0-r1", "el2-c0-r2", "el2-c0-r3"], "computed_utc": "x"}


# ---------------------------------------------------------------- the pure rule
def test_rule_on_forces_k_and_widens_timers():
    before = copy.deepcopy(VAL)
    v, info = V.cap_exception(VAL, 1)
    assert VAL == before  # the input (the values file content) is never modified
    assert v["k"] == {"reader": 1, "searcher": 1} and info["forced_roles"] == ["reader", "searcher"] and info["k_measured"] == {"reader": 0, "searcher": 0}
    assert v["hang_offset_s"] == pytest.approx(3.0 * 96.976) and v["hang_offset_s"] == pytest.approx(290.928)
    assert v["finish_offset_s"] == pytest.approx(40.1776 + (290.928 - 145.464), abs=1e-3)  # the finish offset moves with the hang guard
    assert v["guard_offset_s"] == v["finish_offset_s"]
    assert info["hang_offset_s_orig"] == 145.464 and info["finish_offset_s_orig"] == VAL["finish_offset_s"]
    assert v["B_f"] == VAL["B_f"] and v["turn_p90"] == VAL["turn_p90"]  # nothing else changes


def test_rule_off_and_nothing_to_force_return_the_input_unchanged():
    assert V.cap_exception(VAL, 0)[0] is VAL
    ok = dict(VAL, k={"reader": 1, "searcher": 2})  # no measured 0: a package that obeyed the cap keeps every value
    v, info = V.cap_exception(ok, 1)
    assert v is ok and info["forced_roles"] == []


def test_rule_only_the_zero_role_is_forced():
    mixed = dict(VAL, k={"reader": 2, "searcher": 0})
    v, info = V.cap_exception(mixed, 1)
    assert v["k"] == {"reader": 2, "searcher": 1} and info["forced_roles"] == ["searcher"]


def test_rule_hang_guard_is_a_max_never_a_cut():
    wide = dict(VAL, hang_offset_s=10 * VAL["B_f"])  # an existing guard above 3 x B_f stays; the finish offset then does not move
    v, _ = V.cap_exception(wide, 1)
    assert v["hang_offset_s"] == wide["hang_offset_s"] and v["finish_offset_s"] == wide["finish_offset_s"] and v["k"] == {"reader": 1, "searcher": 1}


def test_rule_on_every_real_values_file():
    files = sorted((R1 / "values").glob("*/*.json"))
    assert len(files) == 9
    for f in files:
        v0 = jload(f)
        v, info = V.cap_exception(v0, 1)
        for role, n in v0["k"].items():
            assert v["k"][role] == (1 if n == 0 else n) and v["k"][role] >= n
        if info["forced_roles"]:
            assert v["hang_offset_s"] == pytest.approx(max(v0["hang_offset_s"], 3.0 * v0["B_f"]))
            assert v["finish_offset_s"] - v["hang_offset_s"] == pytest.approx(v0["finish_offset_s"] - v0["hang_offset_s"])
        else:
            assert v is v0


# ---------------------------------------------------------------- the deadlines CLI
def put_values(root, panel="el2", pkg=DE, **kw):
    v = dict(VAL, panel=panel, pkg=pkg, **kw)
    body = json.dumps(v, indent=1) + "\n"
    d = root / "values" / panel
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{pkg}.json").write_text(body)
    (d / f"{pkg}.json.sha256").write_text(f"{hashlib.sha256(body.encode()).hexdigest()}  {pkg}.json\n")
    return v


def deadlines(root, collab, *extra, panel="el2", pkg=DE, t0=1000):
    return run(["uv", "run", "python", str(TOOLS / "values.py"), "deadlines", panel, pkg, str(collab), str(t0), "--root", str(root), *extra])


def test_deadlines_off_is_exactly_the_old_output_and_on_is_the_rule(root):
    put_values(root)
    off = json.loads(deadlines(root, 1).stdout)
    assert off["k"] == {"reader": 0, "searcher": 0} and off["HANG_MS"] == 1000 + round(1000 * 145.464)
    assert off["FINISH_MS"] == 1000 + round(1000 * 40.17760022888186) and off["GUARD_MS"] == off["FINISH_MS"]
    assert "time_cap_exception" not in off and "cap_exception" not in off  # off: the old key set, nothing added
    on = json.loads(deadlines(root, 1, "--cap-exception", "1").stdout)
    assert on["k"] == {"reader": 1, "searcher": 1} and on["time_cap_exception"] is True
    assert on["HANG_MS"] == 1000 + round(1000 * 3.0 * 96.976) and on["B"] == 96.976
    assert on["FINISH_MS"] == 1000 + round(1000 * (40.17760022888186 + 3.0 * 96.976 - 145.464)) and on["GUARD_MS"] == on["FINISH_MS"]
    assert on["cap_exception"]["forced_roles"] == ["reader", "searcher"]
    assert {k: v for k, v in on.items() if k in off and k not in ("k", "HANG_MS", "FINISH_MS", "GUARD_MS", "finish_offset_s", "guard_offset_s", "hang_offset_s")} \
        == {k: v for k, v in off.items() if k not in ("k", "HANG_MS", "FINISH_MS", "GUARD_MS", "finish_offset_s", "guard_offset_s", "hang_offset_s")}
    assert json.loads(deadlines(root, 1).stdout) == off  # asking for the exception changed nothing on disk


def test_deadlines_exception_is_collab1_only_and_needs_the_values_file(root):
    put_values(root)
    r = deadlines(root, 0, "--cap-exception", "1")
    assert r.returncode == 2 and "collab 1" in r.stderr
    assert deadlines(root, 1, "--cap-exception", "1", pkg=DS).returncode == 2  # no values file for DS: refused, no planning fallback


# ---------------------------------------------------------------- launch.sh
def k0_env(tmp_path, root):
    e = L(tmp_path, root)
    put_values(root, pkg=DS, B_f=100.0, hang_offset_s=150.0, finish_offset_s=50.0, guard_offset_s=50.0)
    e.set_gates(S3=False)
    return e


def hook_k(settings_file):
    cmd = jload(settings_file)["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
    return re.findall(r"'([^']*)'", cmd)[7]  # radar-hook.sh BOARD RUN RID ROLE T0 FINISH GUARD K ...


def test_launch_override_on(tmp_path, root):
    e = k0_env(tmp_path, root)
    r = e.launch(collab=1, rep=0, TIME_CAP_EXCEPTION=1)
    assert r.returncode == 0, r.stdout + r.stderr
    row = "el2-c1x-r0"
    run_json = jload(e.d(row) / "run.json")
    assert jload(root / "runs" / row / "run.json")["time_cap_exception"] is True
    assert run_json["time_cap_exception"] is True and run_json["k"] == {"searcher": 1, "reader": 1}
    assert run_json["HANG_MS"] - run_json["T0_MS"] == 300_000  # max(1.5 B, 3.0 B) with B = 100 s
    assert run_json["FINISH_MS"] - run_json["T0_MS"] == 200_000 and run_json["GUARD_MS"] == run_json["FINISH_MS"]  # 50 + (300 - 150)
    assert run_json["cap_exception"]["k_measured"] == {"reader": 0, "searcher": 0}
    assert {hook_k(p) for p in (e.d(row) / "settings").iterdir()} == {"1"}
    assert "CAP_EXCEPTION" in e.log(row)
    c = jload(e.d(row) / "collab.json")
    assert c["time_cap_exception"] is True and c["B_A1"] == 100.0 and c["forced_k"] == 1 and set(c["delivered"]) == {"t2b-1", "t4-1", "t3-1"}
    assert c["elapsed_over_baseline"] == pytest.approx(c["elapsed_s"] / 100.0) and all(rv["k"] == 1 for rv in c["reviewers"].values())
    x = jload(root / "results" / f"{row}.json")
    assert x["time_cap_exception"] is True and x["collab"] == 1 and x["rep"] == 0 and x["forced_k"] == 1
    p = x["packages"][DS]
    assert p["B_A1"] == 100.0 and p["forced_k"] == 1 and p["k_measured"] == {"reader": 0, "searcher": 0} and p["hang_offset_s"] == 300.0
    assert p["elapsed_over_baseline"] == pytest.approx(p["elapsed_s"] / 100.0) and p["delivered"] == c["delivered"]
    assert not (root / "results" / "el2-c1-r0.json").exists()  # a row that obeyed the cap has its own id


@pytest.mark.parametrize("env", [{}, {"TIME_CAP_EXCEPTION": 0}])  # unset and 0 are both "off"
def test_launch_override_off_changes_nothing(tmp_path, root, env):
    e = k0_env(tmp_path, root)
    assert e.launch(collab=1, rep=0, **env).returncode == 0
    row = "el2-c1-r0"
    run_json = jload(e.d(row) / "run.json")
    assert run_json["k"] == {"reader": 0, "searcher": 0} and run_json["HANG_MS"] - run_json["T0_MS"] == 150_000
    assert run_json["FINISH_MS"] - run_json["T0_MS"] == 50_000 and "time_cap_exception" not in run_json and "cap_exception" not in run_json
    assert "time_cap_exception" not in jload(root / "runs" / row / "run.json")
    assert {hook_k(p) for p in (e.d(row) / "settings").iterdir()} == {"0"}
    assert "CAP_EXCEPTION" not in e.log(row)
    c = jload(e.d(row) / "collab.json")
    assert not {"time_cap_exception", "B_A1", "elapsed_over_baseline", "forced_k", "delivered"} & set(c)
    x = jload(root / "results" / f"{row}.json")
    assert not {"time_cap_exception", "forced_k"} & set(x) and "B_A1" not in x["packages"][DS]
    assert not (root / "runs" / "el2-c1x-r0").exists()


@pytest.mark.parametrize("val,collab", [("2", 1), ("", 1), ("yes", 1), ("1", 0)])
def test_launch_refuses_bad_override_values(tmp_path, root, val, collab):
    e = k0_env(tmp_path, root)
    r = e.launch(collab=collab, rep=0, TIME_CAP_EXCEPTION=val)
    assert r.returncode == 2 and "TIME_CAP_EXCEPTION" in r.stderr
    assert not (root / "runs").exists()  # nothing ran


def test_launch_override_needs_the_gates_and_values_like_any_collab1_row(tmp_path, root):
    e = k0_env(tmp_path, root)
    r = e.launch(collab=1, rep=1, TIME_CAP_EXCEPTION=1)  # rep >= 1 needs S3
    assert r.returncode == 2 and "S3" in r.stderr
    e.set_gates(S0=False)
    assert e.launch(collab=1, rep=0, TIME_CAP_EXCEPTION=1).returncode == 2
    e.set_gates()
    (root / "values" / "el2" / f"{DS}.json.sha256").write_text("0" * 64 + f"  {DS}.json\n")
    r = e.launch(collab=1, rep=0, TIME_CAP_EXCEPTION=1)
    assert r.returncode == 2 and "Spike 4" in r.stderr


# ---------------------------------------------------------------- collab_summary columns
def test_collab_summary_columns_only_with_the_exception(tmp_path, root):
    off = Pkg(tmp_path / "a", root, row="el2-c1-r0")
    assert off.summary().returncode == 0
    assert "time_cap_exception" not in off.collab_json()
    p = Pkg(tmp_path / "b", root, row="el2-c1x-r0")
    p.run.update({"time_cap_exception": True, "B": 100.0, "k": {"searcher": 1, "reader": 1},
                  "cap_exception": {"forced_k": 1, "k_measured": {"searcher": 0, "reader": 0}, "forced_roles": ["reader", "searcher"]}})
    p.write_run()
    assert p.summary().returncode == 0
    c = p.collab_json()
    assert c["time_cap_exception"] is True and c["B_A1"] == 100.0 and c["forced_k"] == 1 and c["forced_roles"] == ["reader", "searcher"]
    assert c["elapsed_s"] == 100.0 and c["elapsed_over_baseline"] == pytest.approx(1.0)
    assert c["delivered"] == {"t2b-1": 0, "t4-1": 0, "t3-1": 0} and c["k_measured"] == {"searcher": 0, "reader": 0}


# ---------------------------------------------------------------- results row
def test_results_row_id_and_stamp(root, tmp_path):
    a1 = build(root, tmp_path, "el2-c1x-r1")
    for p in (DS, AL, DE):
        f = root / "runs" / "el2-c1x-r1" / p / "collab.json"
        c = jload(f)
        c.update({"time_cap_exception": True, "B_A1": 116.0, "elapsed_over_baseline": 120.0 / 116.0, "forced_k": 1,
                  "k_measured": {"searcher": 0, "reader": 0}, "forced_roles": ["reader", "searcher"], "delivered": {"t2b-1": 1, "t4-1": 0, "t3-1": 1}})
        f.write_text(json.dumps(c))
        (root / "runs" / "el2-c1x-r1" / p / "run.json").write_text(json.dumps({"k": {"searcher": 1, "reader": 1}, "values": "x", "T0_MS": 0, "HANG_MS": 348_000}))
    assert results(root, a1, "el2-c1x-r1").returncode == 0
    x = jload(root / "results" / "el2-c1x-r1.json")
    assert x["time_cap_exception"] is True and x["collab"] == 1 and x["rep"] == 1 and x["panel"] == "el2" and x["forced_k"] == 1
    assert x["status"] == "complete" and x["found_14"] == 4  # the scoring is the normal one
    q = x["packages"][DS]
    assert q["B_A1"] == 116.0 and q["delivered"]["t2b-1"] == 1 and q["hang_offset_s"] == 348.0 and q["elapsed_over_baseline"] == pytest.approx(120.0 / 116.0)
    assert results(root, a1, "el2-c1x-r1").returncode == 2  # duplicate refused as before


def test_results_rejects_a_baseline_exception_row_id(root, tmp_path):
    assert results(root, build(root, tmp_path, "el2-c0-r1"), "el2-c0x-r1").returncode != 0


# ---------------------------------------------------------------- alarms: no mixing
def test_alarms_keep_exception_rows_apart(root):
    def cx(rep, **kw):
        r = alarm_row(1, rep, **kw)
        r.update({"row": f"el2-c1x-r{rep}", "time_cap_exception": True, "status": "complete"})
        r["packages"][ALARM_PKG].update({"B_A1": 116.0, "elapsed_over_baseline": 2.2, "forced_k": 1, "k_measured": {"searcher": 0, "reader": 0},
                                         "forced_roles": ["reader", "searcher"], "delivered": {"t2b-1": 1, "t4-1": 0, "t3-1": 1}, "hang_offset_s": 348.0})
        return r
    base = [alarm_row(0, 1), alarm_row(0, 2), alarm_row(1, 1), alarm_row(1, 2)]
    clean, _ = alarms(root, base)
    # an exception row that would fire every alarm (huge Jaccard, few ledger rows, 3x elapsed, snapshot failures, other moves) and a smoke row
    mixed, _ = alarms(root, base + [cx(1, jac=0.9, ledger=1, elapsed=348.0, snap=3, inj={"M9": 5}), cx(0)])
    for key in ("convergence", "snapshot", "arms", "blocks", "same_gaps"):
        assert mixed[key] == clean[key]
    rows = {r["row"]: r for r in mixed["time_cap_exception"]["rows"]}
    assert set(rows) == {"el2-c1x-r1", "el2-c1x-r0"}  # rep 0 is listed here although the arm-level checks ignore smoke rows
    pk = rows["el2-c1x-r1"]["packages"][ALARM_PKG]
    assert pk["B_A1"] == 116.0 and pk["elapsed_s"] == 348.0 and pk["elapsed_over_baseline"] == 2.2 and pk["forced_k"] == 1 and pk["delivered"]["t4-1"] == 0
    assert clean["time_cap_exception"]["rows"] == []
