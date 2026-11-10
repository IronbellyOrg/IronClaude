import json
import os
import pathlib
import shutil

import pytest

import build_matrix as bm

FIX = pathlib.Path(__file__).parent / "fixtures"
SP = bm.SP
AUD_OUT = bm.AUD_OUT
SPEC = bm.SPEC


def fx(name):
    return json.loads((FIX / name).read_text())


def design(tmp_path, did, fixture=None, as_name="metrics.json"):
    d = tmp_path / did
    d.mkdir(parents=True, exist_ok=True)
    if fixture:
        shutil.copy(FIX / fixture, d / as_name)
    return {"design_id": did, "label": f"label {did}", "path": str(d)}


def write_audit(path, nblk, prefix="B"):
    path.parent.mkdir(parents=True, exist_ok=True)
    ids = ", ".join(f"{prefix}{i}" for i in range(1, nblk + 1))
    body = "".join(f"\n## {prefix}{i} some defect\nbody text\n" for i in range(1, nblk + 1))
    path.write_text((f"Blocking finding ids: {ids}.\n{body}\n" if nblk else "") + f"verdict: {'FAIL' if nblk else 'PASS'}\n")


@pytest.fixture(autouse=True)
def _clean():
    bm.WARNINGS.clear(); bm.SOURCES.clear(); bm.BLOCKED.clear()


def test_adapter_baseline_sonnet(tmp_path):
    runs, a2 = tmp_path / "runs", tmp_path / "a2"
    for k in range(1, 7):
        write_audit(runs / f"a3-r{k}/aud/ws" / AUD_OUT, k % 3)
        write_audit(a2 / f"a3-r{k}/ws" / AUD_OUT, 2)
        spec = runs / f"a3-r{k}/aud/ws" / SPEC
        spec.parent.mkdir(parents=True, exist_ok=True)
        spec.write_bytes(b"x" * (57763 + 577 * k))
    (row,) = bm.adapt_baseline_sonnet({"design_id": "stage2-a3", "runs_dir": str(runs), "audit2_dir": str(a2)})
    assert row["verdict"] == "BASELINE" and row["role"] == "baseline" and row["n_completed"] == 6
    assert abs(row["BLK"] - (sum(k % 3 for k in range(1, 7)) + 12) / 12) < 1e-9
    assert row["R_LOOP"] == 1.0 and row["R_B"] == 1.0 and row["A_mean"] == 100424 and row["provisional"] is False
    assert abs(row["growth_mean_pct"] - 577 * 3.5 / 57763 * 100) < 1e-6
    (single,) = bm.adapt_baseline_sonnet({"design_id": "x", "runs_dir": str(runs), "audit2_dir": str(tmp_path / "none")})
    assert single["provisional"] is True


def test_adapter_baseline_haiku(tmp_path):
    d = design(tmp_path, "p14-haiku-a3", "p14_results.json", "results.json")
    write_audit(tmp_path / "p14-haiku-a3/runs/a3-r1/aud/ws" / AUD_OUT, 1)       # rescored: 1 (reported 2)
    (row,) = bm.adapt_baseline_haiku(d)
    assert row["role"] == "baseline" and row["stratum"] == "haiku" and row["verdict"] == "BASELINE"
    assert row["provisional"] is True and row["HR"] == 1.0                      # single audit so far
    assert abs(row["BLK"] - (1 + 3) / 2) < 1e-9 and row["blk_mismatch"] is True
    assert row["A_mean"] == 170000 and abs(row["R_LOOP"] - 170000 / 100424) < 1e-9 and row["loop_pass"] == "1/2"
    write_audit(tmp_path / "p14-haiku-a3/runs/a3-r1/aud2/ws" / AUD_OUT, 3)
    write_audit(tmp_path / "p14-haiku-a3/runs/a3-r2/aud/ws" / AUD_OUT, 2)
    write_audit(tmp_path / "p14-haiku-a3/runs/a3-r2/aud2/ws" / AUD_OUT, 2)
    (row2,) = bm.adapt_baseline_haiku(d)
    assert row2["provisional"] is False and abs(row2["BLK"] - 2.0) < 1e-9


def test_adapter_p12_ab1(tmp_path):
    rows = bm.adapt_p12_ab1(design(tmp_path, "p12-ab1", "p12_ab1_metrics.json"))
    s, h = rows
    assert s["verdict"] == "ADOPT" and s["haiku_pending"] is True and s["n_completed"] == 6 and s["BLK"] == 1.25
    assert s["A_mean"] == 120000 and s["R_LOOP"] == 1.195 and s["B_mean"] == 190000 and s["R_B"] == 1.121
    assert abs(s["growth_mean_pct"] - 2.0) < 1e-9 and s["loop_pass"] == "6/6" and s["rule"] == "ADOPT conditions met"
    assert s["missing_keys"] == [] or all("." in k for k in s["missing_keys"])
    assert h["stratum"] == "haiku" and h["BLK"] == 1.5 and abs(h["growth_mean_pct"] - 3.0) < 1e-9 and h["loop_pass"] == "4/4"


def test_adapter_p12_ab2(tmp_path):
    s, h = bm.adapt_p12_ab2(design(tmp_path, "p12-ab2", "p12_ab2_metrics.json"))
    assert s["verdict"] == "ADOPT" and s["BLK"] == 1.0 and s["A_mean"] == 110000 and s["R_LOOP"] == 1.095 and s["B_mean"] == 175000
    assert s["loop_pass"] == "6/6" and s["rule"] == "ADOPT conditions met" and s["n_completed"] == 6
    assert h["stratum"] == "haiku" and h["BLK"] == 1.4 and h["A_mean"] == 160000 and abs(h["growth_mean_pct"] - 3.1) < 1e-9


def test_adapter_p12_ab3(tmp_path):
    s, = bm.adapt_p12_ab3(design(tmp_path, "p12-ab3", "p12_ab3_metrics.json"))
    assert s["verdict"] == "DROP" and s["BLK"] == 1.75 and s["A_mean"] == 130000 and s["R_LOOP"] == 1.294
    assert abs(s["growth_mean_pct"] - 2.5) < 1e-9 and s["loop_pass"] == "5/6" and s["rule"] == "DROP-2 (cost clause)"


def test_adapter_p13_ab1(tmp_path):
    d = design(tmp_path, "p13-pn1")
    rows = bm.adapt_p13_ab1(d, runner=lambda path: (fx("p13_ab1_compute.json"), []))
    (s,) = rows
    assert s["verdict"] == "DROP" and s["verdict_raw"] == "DROP-2" and "COST-HOLD" in s["notes"]
    assert s["BLK"] == 1.17 and s["A_mean"] == 132480 and s["B_mean"] == 202480 and abs(s["growth_mean_pct"] - 5.0) < 1e-9
    assert s["loop_pass"] == "3/6" and s["n_completed"] == 6 and "R_LOOP 1.32" in s["rule"]


def test_adapter_p13_ab2(tmp_path):
    d = design(tmp_path, "p13-pn2", "p13_ab2_results.json", "results.json")
    s, h = bm.adapt_p13_ab2(d)
    assert s["verdict"] == "ADOPT" and s["haiku_pending"] is True and s["BLK"] == 0.9 and s["AUD1"] == 0.8 and s["AUD2"] == 1.0
    assert s["A_mean"] == 110000 and s["B_mean"] == 178000 and s["R_LOOP"] == 1.095 and s["growth_mean_pct"] == 1.2 and s["loop_pass"] == "6/6"
    assert s["rule"].startswith("BLK_T 0.90") and h["stratum"] == "haiku" and h["BLK"] == 1.2


def test_adapter_p13_ab3(tmp_path):
    d = design(tmp_path, "p13-pn3", "p13_ab3_gate_fail.json", "gate.json")
    (r,) = bm.adapt_p13_ab3(d)
    assert r["verdict"] == "NO-GO-OFFLINE" and r["stratum"] == "offline" and r["role"] == "offline-gate" and r["rule"] == "gate: F1 FALSIFIED"
    assert r["BLK"] is None and r["n_completed"] == 0


def test_adapter_p15(tmp_path):
    rows = bm.adapt_p15(fx("p15_results.json"))
    assert [r["arm"] for r in rows] == ["g3c", "g3b", "g3ch"]
    t = rows[0]
    assert t["design_id"] == "p15-E3" and t["verdict"] == "ADOPT" and t["haiku_pending"] is True and t["BLK"] == 1.0
    assert t["A_mean"] == 105000 and t["R_LOOP"] == 1.05 and t["B_mean"] == 173000 and t["growth_mean_pct"] == 1.3
    assert t["jev_input_tokens"] == 9000 and t["jev_usd"] == 0.000378 and t["rule"].startswith("R-ADOPT")
    assert rows[1]["verdict"] == "CONTROL" and rows[1]["role"] == "control"
    assert bm.BLOCKED == [{"from": "E3", "experiment": "E4", "reason": "E1 smoke false closure"}]
    assert bm.adapt_p15({"schema": "other"}) == []


def test_missing_file_pending(tmp_path):
    for fn, name in ((bm.adapt_p12_ab1, "p12-ab1"), (bm.adapt_p12_ab2, "p12-ab2"), (bm.adapt_p12_ab3, "p12-ab3"), (bm.adapt_p13_ab2, "p13-pn2")):
        (r,) = fn(design(tmp_path, name))
        assert r["verdict"] == "PENDING" and r["BLK"] is None and r["n_completed"] == 0 and r["missing_keys"]
    (r,) = bm.adapt_p13_ab3(design(tmp_path, "p13-pn3"))
    assert r["verdict"] == "PENDING" and r["stratum"] == "offline"
    (r,) = bm.adapt_baseline_haiku(design(tmp_path, "p14-haiku-a3"))
    assert r["verdict"] == "PENDING" and r["role"] == "baseline"
    (r,) = bm.adapt_p13_ab1(design(tmp_path, "p13-pn1"), runner=lambda p: (None, []))
    assert r["verdict"] == "PENDING"


def test_verdict_normalization_table():
    table = {"ADOPT": ("ADOPT", False), "ADOPT (Haiku robustness pending)": ("ADOPT", True), "DROP": ("DROP", False),
             "DROP-1": ("DROP", False), "DROP-4": ("DROP", False), "INCONCLUSIVE": ("INCONCLUSIVE", False),
             "INCONCLUSIVE (Sonnet ADOPT, Haiku stratum points the other way)": ("INCONCLUSIVE", False),
             "NO-GO-OFFLINE": ("NO-GO-OFFLINE", False), "FALSIFIED ; live: NOT RUN (gate)": ("NO-GO-OFFLINE", False),
             "BLOCKED": ("BLOCKED", False), "BLOCKED-BUDGET": ("BLOCKED", False), "NOT RUN": ("PENDING", False),
             "PENDING": ("PENDING", False), "": ("PENDING", False), None: ("PENDING", False), "BASELINE": ("BASELINE", False),
             "CONTROL": ("CONTROL", False)}
    for raw, (v, hp) in table.items():
        got, flags = bm.normalize_verdict(raw)
        assert (got, flags["haiku_pending"]) == (v, hp), raw
    v, flags = bm.normalize_verdict("MAYBE")
    assert v == "UNMAPPED" and flags["unmapped"]
    row = bm.mkrow(design_id="d")
    bm.set_verdict(row, "MAYBE", "d")
    assert any("UNMAPPED" in w for w in bm.WARNINGS)


def test_haiku_rows_hr_against_haiku_baseline(tmp_path):
    designs = [{"design_id": "p14-haiku-a3", "label": "hb", "adapter": "baseline_haiku", "path": str(tmp_path / "p14-haiku-a3")},
               {"design_id": "p12-ab2", "label": "ab2", "adapter": "p12_ab2", "path": str(tmp_path / "p12-ab2")}]
    design(tmp_path, "p14-haiku-a3", "p14_results.json", "results.json")
    design(tmp_path, "p12-ab2", "p12_ab2_metrics.json")
    write_audit(tmp_path / "p14-haiku-a3/runs/a3-r1/aud/ws" / AUD_OUT, 2)
    write_audit(tmp_path / "p14-haiku-a3/runs/a3-r2/aud/ws" / AUD_OUT, 2)
    dp = tmp_path / "designs.json"
    dp.write_text(json.dumps(designs))
    m, errors = bm.build(sp=tmp_path, designs_path=dp)
    rows = {(r["design_id"], r["arm"]): r for r in m["rows"]}
    hb, h = rows[("p14-haiku-a3", "a3h")], rows[("p12-ab2", "b2h")]
    assert hb["BLK"] == 2.0 and hb["HR"] == 1.0
    assert abs(h["HR"] - 1.4 / 2.0) < 1e-9 and h["stratum"] == "haiku" and h["provisional"] is True
    assert m["rows"][0]["role"] == "baseline"                       # baseline rows first
    assert rows[("p12-ab2", "b2")]["HR"] is None


def test_p15_discovery_and_schema_check(tmp_path):
    (tmp_path / "p15/e3").mkdir(parents=True)
    shutil.copy(FIX / "p15_results.json", tmp_path / "p15/e3/results.json")
    bad = fx("p15_results.json")
    bad["experiment"] = "E9"; bad["design_id"] = "p15-E9"
    del bad["rows"][0]["metrics"]["R_LOOP"]
    bad["rows"][1]["verdict"] = "WINNER"
    (tmp_path / "p15/e9").mkdir(parents=True)
    (tmp_path / "p15/e9/results.json").write_text(json.dumps(bad))
    other = tmp_path / "p15/e1"; other.mkdir()
    (other / "results.json").write_text(json.dumps({"schema": "something-else"}))          # ignored, not an error
    dp = tmp_path / "designs.json"; dp.write_text("[]")
    m, errors = bm.build(sp=tmp_path, designs_path=dp)
    assert {r["design_id"] for r in m["rows"]} == {"p15-E3"}
    assert any("R_LOOP" in e for e in errors) and any("WINNER" in e for e in errors)
    assert any("p15/e9" in w for w in m["warnings"])
    assert m["blocked_downstream"] == [{"from": "E3", "experiment": "E4", "reason": "E1 smoke false closure"}]


def test_rescore_baseline_12_audits_1_50():
    (row,) = bm.adapt_baseline_sonnet({"design_id": "stage2-a3"})
    assert abs(row["BLK"] - 1.50) < 1e-9 and abs(row["AUD1"] - 1.5) < 1e-9 and abs(row["AUD2"] - 1.5) < 1e-9
    assert row["blk_mismatch"] is False and row["provisional"] is False and row["n_completed"] == 6
    assert round(row["growth_mean_pct"], 2) == 1.41


def test_rescore_runs_strata_and_arm(tmp_path):
    runs = tmp_path / "runs"
    for name, a1, a2, st in (("g3c-r1", 1, 3, {"arm": "g3c", "stratum": "sonnet"}), ("g3bh-r1", 2, 2, {"arm": "g3b"}), ("g3c-r2", 0, 0, {"arm": "g3c"})):
        write_audit(runs / name / "aud/ws" / AUD_OUT, a1)
        write_audit(runs / name / "aud2/ws" / AUD_OUT, a2)
        (runs / name / "state.json").write_text(json.dumps({**st, "log": {"R1": {}, "R2": {}}, "loop_end": "PASS"}))
    write_audit(runs / "g3c-r3" / "aud/ws" / AUD_OUT, 1)          # no audit 2: not counted
    rs = bm.rescore_runs(runs)
    assert rs["sonnet"]["n"] == 2 and rs["haiku"]["n"] == 1 and rs["haiku"]["BLK"] == 2.0 and rs["sonnet"]["BLK"] == 1.0
    assert rs["sonnet"]["reviews_mean"] == 2
    assert bm.rescore_runs(runs, arm="g3c")["sonnet"]["n"] == 2 and "haiku" not in bm.rescore_runs(runs, arm="g3c")
    assert bm.rescore_runs(tmp_path / "nothing") == {}


def snap(paths, only=None):
    out = {}
    for base in paths:
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "runs", "journal", "sb", ".pytest_cache")]
            for f in files:
                if only and f not in only:
                    continue
                p = os.path.join(root, f)
                try:
                    out[p] = os.stat(p).st_mtime_ns
                except OSError:
                    pass
    return out


def test_builder_writes_only_central():
    dirs = [SP / "p11", SP / "p12", SP / "p13", SP / "p14", SP / "exp346"]
    before = snap(dirs)
    before15 = snap([SP / "p15"], only={"results.json"})
    cen_before = {p.name for p in bm.CENTRAL.iterdir()}
    assert bm.main([]) in (0, 1)
    assert snap(dirs) == before and snap([SP / "p15"], only={"results.json"}) == before15
    assert {p.name for p in bm.CENTRAL.iterdir()} >= cen_before
    assert (bm.CENTRAL / "matrix.json").exists() and (bm.CENTRAL / "MATRIX.md").exists()
    assert not [p for p in bm.CENTRAL.iterdir() if p.name.endswith(".tmp") or ".tmp" in p.name]


def test_p13_ab1_side_effect_guard(tmp_path, monkeypatch):
    tree = tmp_path / "ab1"
    (tree / "runs").mkdir(parents=True)
    (tree / "RESULTS.md").write_text("# x\n\nDECISION: INCONCLUSIVE (3 runs)\n")
    (tree / "harness.py").write_text("# stub")

    class P:
        returncode = 0
        stdout = json.dumps(fx("p13_ab1_compute.json")) + "\n"
        stderr = ""

    def fake_run(*a, **kw):
        (tree / "touched.txt").write_text("side effect")
        return P()

    monkeypatch.setattr(bm.subprocess, "run", fake_run)
    data, changed = bm.run_compute_results(tree)
    assert data is None and changed == ["touched.txt"]
    (tree / "touched.txt").unlink()
    rows = bm.adapt_p13_ab1({"design_id": "p13-pn1", "label": "x", "path": str(tree)})
    assert bm.WARNINGS == ["p13_ab1 compute_results modified files"]
    assert rows[0]["source"] == "RESULTS.md" and rows[0]["verdict"] == "INCONCLUSIVE" and rows[0]["BLK"] is None
    # a clean run returns the data
    monkeypatch.setattr(bm.subprocess, "run", lambda *a, **kw: P())
    data, changed = bm.run_compute_results(tree)
    assert changed == [] and data["final"] == "DROP-2"
    # the `runs/` subtree is live-experiment territory and is not part of the guard
    def fake_run2(*a, **kw):
        (tree / "runs" / "state.json").write_text("{}")
        return P()
    monkeypatch.setattr(bm.subprocess, "run", fake_run2)
    assert bm.run_compute_results(tree)[1] == []


def test_real_disk_build_succeeds():
    m, errors = bm.build()
    rows = {(r["design_id"], r["arm"]): r for r in m["rows"]}
    a3 = rows[("stage2-a3", "a3")]
    assert a3["verdict"] == "BASELINE" and abs(a3["BLK"] - 1.5) < 1e-9 and a3["R_LOOP"] == 1.0 and a3["R_B"] == 1.0
    hb = rows[("p14-haiku-a3", "a3h")]
    assert hb["verdict"] == "BASELINE" and hb["stratum"] == "haiku" and hb["HR"] == 1.0 and isinstance(hb["provisional"], bool)
    pn3 = rows[("p13-pn3", "c3")]
    assert pn3["verdict"] == "NO-GO-OFFLINE" and pn3["role"] == "offline-gate"
    for (did, arm), r in rows.items():
        assert r["verdict"] != "UNMAPPED", (did, arm)
        if did.startswith("p12-"):
            assert r["verdict"] in ("PENDING", "ADOPT", "DROP", "INCONCLUSIVE", "BLOCKED"), (did, r["verdict"])
    assert not [w for w in m["warnings"] if "unknown" in w.lower() or "UNMAPPED" in w]
    assert [r["role"] for r in m["rows"][:2]] == ["baseline", "baseline"]
    assert not errors or all("results.json" in e for e in errors)


def test_check_mode_exit_codes(tmp_path):
    assert bm.main(["--check"]) in (0, 1)
    md = bm.render_md(bm.build()[0]["rows"], "now", [], [])
    assert md.startswith("# CENTRAL MATRIX") and "## Sonnet stratum" in md and "## Haiku stratum" in md and "## Offline gates" in md
