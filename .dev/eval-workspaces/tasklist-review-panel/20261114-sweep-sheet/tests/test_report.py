"""REQ-31, REQ-40, REQ-42, REQ-45, REQ-17, DD-7: the gates, the three shares, the claim, the break-even values, the report.
Run folders are synthetic (fixtures/runs/make_runs.py); the numbers marked as hand-worked come from its tables:
mean found fraction Z0-raw 16/80, Z0 25/80, K 32/80, SS 43/80 (8 items, 10 runs per arm)."""

import json
import re

import pytest

from analysis import analyze
from fixtures.runs import make_runs
from scaffold import clock, judge


@pytest.fixture
def world(tmp_path):
    return make_runs.build(tmp_path, arms=make_runs.ALL_ARMS)


def build_custom(root, tweak):
    """Runs of Z0, K and SS written from the tables after `tweak(spec)` changed each spec (see make_runs.specs)."""
    runs, scoring = root / "runs" / "stage1", root / "scoring" / "stage1"
    runs.mkdir(parents=True)
    specs = make_runs.specs()
    z0_secs = {(s["doc"], s["rep"]): s["secs"] for s in specs if s["arm"] == "Z0"}
    for n, s in enumerate(specs, 1):
        tweak(s, z0_secs)
        make_runs.write_run(runs, scoring, s, f"j{n:06x}")
    return runs


def fast_ss(s, z0_secs):
    """SS as fast as Z0 on the same document and replicate, so that gate D1 is not what fails."""
    if s["arm"] == "SS":
        s["secs"] = z0_secs[(s["doc"], s["rep"])]


def fast_ss_keeping_gt3(s, z0_secs):
    fast_ss(s, z0_secs)
    if (s["arm"], s["doc"], s["rep"]) == ("SS", "synth-a", 4):
        s["found"] = s["found"] | {"GT3"}  # SS now reaches GT3 in 4 of 5 runs, like Z0


def gates_of(root, tweak):
    runs = analyze.load_runs(build_custom(root, tweak))
    return runs, analyze.gates(runs)


def test_three_shares_separate(world):
    runs = analyze.load_runs(world.runs)
    sh = analyze.shares(runs)
    assert [(s["label"], s["formula"]) for s in sh] == [
        ("H share", "Z0 - Z0raw"),
        ("Prompting share", "K - Z0"),
        ("Redesign share", "SS - Z0"),
    ]
    # 25/80 - 16/80, 32/80 - 25/80, 43/80 - 25/80
    assert [s["value"] for s in sh] == [0.1125, 0.0875, 0.225]
    text = analyze.render_report(
        runs, analyze.gates(runs), sh, analyze.ledger_headings(runs)
    )
    lines = [ln for ln in text.splitlines() if ln.startswith("- ") and "share (" in ln]
    assert lines == [
        "- H share (Z0 - Z0raw): 0.1125",
        "- Prompting share (K - Z0): 0.0875",
        "- Redesign share (SS - Z0): 0.2250",
    ]


def test_no_summed_headline(world):
    runs = analyze.load_runs(world.runs)
    text = analyze.render_report(
        runs, analyze.gates(runs), analyze.shares(runs), analyze.ledger_headings(runs)
    )
    names = ("H share", "Prompting share", "Redesign share")
    for line in text.splitlines():
        assert sum(n.lower() in line.lower() for n in names) <= 1, line
        if "share (" in line:
            assert "+" not in line and "total" not in line.lower(), line
    # the shares are never added in the numbers either
    assert not re.search(r"0\.4250|0\.3250|0\.5250", text)
    # a share is computed over the documents that both of its arms ran
    only_a = [r for r in runs if not (r.arm == "Z0-raw" and r.doc == "synth-b")]
    h = analyze.shares(only_a)[0]
    assert h["documents"] == ["synth-a"] and h["value"] == pytest.approx(0.35 - 9 / 40)


def test_breakeven_values():
    assert analyze.breakeven_values(100) == {"prepass_s": 14.0, "per_item_s": 2.75}
    at = analyze.breakeven_values(122)
    assert at["prepass_s"] == pytest.approx(21.7, abs=0.05)
    assert at["per_item_s"] == pytest.approx(3.71, abs=0.01)


def test_report_shows_planned_and_measured(world):
    runs = analyze.load_runs(world.runs)
    values = {**clock.load_values(), "spike": {"runs": 5, "c_luna": 2.1}}
    lines = analyze.breakeven_lines(runs, values)
    assert (
        "Pre-pass seconds: planned 8 s, measured 0.59 s; break-even 14.0 s at b = 100 and 21.7 s at b = 122."
        in lines
    )
    assert (
        "Seconds per item (luna): planned 2 s, measured 2.10 s; break-even 2.75 s at b = 100 and 3.71 s at b = 122."
        in lines
    )
    # b of a document: the median of the Z0 runs' slowest reviewer (secs - 10 in the fixture: 90 100 85 110 95)
    assert (
        "b of synth-a (Z0 slowest reviewer, median): planned not set, measured 95.0 s."
        in lines
    )
    text = analyze.render_report(
        runs,
        analyze.gates(runs),
        analyze.shares(runs),
        analyze.ledger_headings(runs),
        values=values,
    )
    section = text.split("## Time and break-even")[1].split("##")[0]
    for ln in section.splitlines():
        if ln.startswith("- "):
            assert "planned" in ln and "measured" in ln, ln
    # without a spike record the measured cost per item is said to be missing, not invented
    none = analyze.breakeven_lines(
        None, {k: v for k, v in values.items() if k != "spike"}
    )
    assert any("measured not measured yet (no spike record)" in ln for ln in none)


def test_claim_template_text(world):
    runs = analyze.load_runs(world.runs)
    text = analyze.render_report(
        runs, analyze.gates(runs), analyze.shares(runs), analyze.ledger_headings(runs)
    )
    req45 = (
        "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), "
        "and only for Redesign 1 at the high end of its range"
    )
    assert analyze.CLAIM == req45
    assert text.count(f"The Sweep Sheet {req45}.") == 1
    # no other sentence says "consistent" for a class
    for line in text.splitlines():
        if "consistent" in line.lower():
            assert not re.search(r"\b[CI][1-8]\b", line), line
    assert len(re.findall(r"\bI4\b", text)) == 1


def test_d6_failure_blocks_adoption(tmp_path):
    runs, g = gates_of(tmp_path, fast_ss)
    st = {k: v["status"] for k, v in g["gates"].items()}
    # D2 (0.225 over Z0) and D3 (9 consistent items against 5) pass; D6 fails because SS reaches GT3 of synth-a in 3 of 5 runs
    # where Z0 reaches it in 4 of 5, a drop of 0.2 against the 0.10 allowed
    assert (st["D1"], st["D2"], st["D3"], st["D6"], st["D7"]) == (
        "pass",
        "pass",
        "pass",
        "fail",
        "pass",
    )
    assert (st["D4"], st["D5"]) == (
        "pending",
        "pending",
    )  # no clean twins, no planted set
    assert g["gates"]["D2"]["difference"] == pytest.approx(0.225)
    assert g["gates"]["D2"]["lower_bound"] > 0.04
    assert (
        g["gates"]["D3"]["arm_consistent_items"],
        g["gates"]["D3"]["base_consistent_items"],
    ) == (
        9,
        5,
    )  # SS: 5 in synth-a (GT1 2 3 5 6) and 4 in synth-b (GT4 5 6 8); Z0: 3 and 2
    assert g["gates"]["D6"]["failing_items"] == [
        {"doc": "synth-a", "item": "GT3", "base_reach": 0.8, "arm_reach": 0.6}
    ]
    assert g["gates"]["D6"]["items_checked"] == 5
    out = g["outcome"]
    assert (
        out["result"] == "do not adopt"
        and out["blocking"] == ["D6"]
        and out["failed"] == ["D6"]
    )
    assert out["text"] == "do not adopt: D6 (blocking) failed"
    text = analyze.render_report(
        runs, g, analyze.shares(runs), analyze.ledger_headings(runs)
    )
    assert "Outcome: do not adopt: D6 (blocking) failed." in text


def test_gates_with_d6_met_are_pending_not_adopted(tmp_path):
    # the control: SS also reaches GT3 in 4 of 5 runs, so D6 passes; D4 and D5 still lack data, so the result is not "adopt"
    _, g = gates_of(tmp_path, fast_ss_keeping_gt3)
    assert (
        g["gates"]["D6"]["status"] == "pass" and g["gates"]["D6"]["failing_items"] == []
    )
    assert g["outcome"]["result"] == "pending" and g["outcome"]["blocking"] == []
    assert g["outcome"]["pending"] == ["D4", "D5"]


def test_d1_fails_when_the_arm_is_slow(world):
    runs = analyze.load_runs(world.runs)
    g = analyze.gates(runs)
    d1 = g["gates"]["D1"]
    # SS median 142 against Z0 median 85 on synth-b: 1.67 > 1.35
    assert d1["status"] == "fail"
    assert d1["inputs"]["primary"]["docs"]["synth-b"]["ratio"] == pytest.approx(
        142 / 85, abs=1e-5
    )
    assert "D1" in g["outcome"]["failed"]


def test_bootstrap_is_seeded_and_resamples_documents(world):
    runs = analyze.load_runs(world.runs)
    ss, z0 = analyze._arm(runs, "SS"), analyze._arm(runs, "Z0")
    a = analyze.bootstrap_lower(ss, z0, seed=1, n=300)
    assert a == analyze.bootstrap_lower(ss, z0, seed=1, n=300)
    assert a != analyze.bootstrap_lower(ss, z0, seed=2, n=300)
    assert a < analyze.mean_found(ss) - analyze.mean_found(z0)
    with pytest.raises(analyze.AnalysisError, match="no document"):
        analyze.bootstrap_lower(ss, [r for r in z0 if r.doc == "nope"])


def test_gates_need_both_arms(world):
    runs = [r for r in analyze.load_runs(world.runs) if r.arm != "Z0"]
    with pytest.raises(analyze.AnalysisError, match="SS and Z0"):
        analyze.gates(runs)


def test_twin_and_planted_gates_use_their_own_sets(tmp_path):
    runs = analyze.load_runs(build_custom(tmp_path, fast_ss))
    sets = {"synth-a": "holdout", "synth-b": "twin"}
    twin_runs = [r for r in runs if r.doc == "synth-b"]
    assert {r.doc for r in analyze.decision_runs(runs, sets)} == {"synth-a"}
    for r in (
        twin_runs
    ):  # a clean twin: every blocking row of a merged ledger is a wrong blocker
        rows = [{"blocking": r.arm == "SS", "members": []}] * 2
        (r.path / "merged").mkdir()
        (r.path / "merged" / "ledger.json").write_text(json.dumps({"rows": rows}))
    d4 = analyze.gates(runs, sets=sets)["gates"]["D4"]
    # 2 blocking rows per SS run against none for Z0: 2.0 > 0.7
    assert d4["twin_blocking_difference"] == 2.0 and d4["status"] == "fail"
    classes = {
        d: {f"GT{n}": f"C{n}" for n in range(1, 9)} for d in ("synth-a", "synth-b")
    }
    d5 = analyze.gates(
        runs, sets={"synth-a": "holdout", "synth-b": "planted"}, classes=classes
    )["gates"]["D5"]
    # planted detection of SS on synth-b, class C4 = GT4: found in 5 of 5; C5: 5 of 5; C6: 4 of 5; C8 (GT8): 5 of 5; C2: 0 of 5
    assert d5["planted_detection"] == {
        "C2": 0.0,
        "C4": 1.0,
        "C5": 1.0,
        "C6": 0.8,
        "C8": 1.0,
    }
    assert d5["planted_classes_passing"] == ["C4", "C5", "C6", "C8"]
    assert (
        d5["status"] == "pending"
    )  # the documentation arm and the spec set have no runs yet


def make_compliance(root, missing_per_run):
    for k, missing in enumerate(missing_per_run, 1):
        run = root / f"c{k}"
        (run / "check").mkdir(parents=True)
        (run / "check" / "check.json").write_text(
            json.dumps(
                {
                    "ledger_missing": missing,
                    "format_errors": 1 if k == 1 else 0,
                    "format_induced_demotions": 0,
                }
            )
        )
        for i, rid in enumerate(("t2b-1", "t3-1", "t4-1")):
            ok = not (
                k == 1 and i == 0
            )  # one reviewer wrote a quote that is not in the candidate
            rows = [
                {
                    "item": "S1",
                    "verdict": "PROBLEM",
                    "quote_plan": "a quote",
                    "quote_plan_ok": ok,
                },
                {
                    "item": "S2",
                    "verdict": "OK",
                    "quote_plan": "",
                    "quote_plan_ok": False,
                },
            ]
            (run / "check" / f"{rid}.ledger.json").write_text(
                json.dumps({"ledger": {"rows": rows}})
            )
    return root


def test_compliance_go_no_go(tmp_path):
    ok = make_compliance(tmp_path / "ok", [["t4-1"], [], [], [], []])
    r = analyze.compliance(ok)
    # 5 runs of 3 reviewers; 1 ledger missing in 15 is 0.0667, within the 10% limit; 14 of 15 quotes are in the candidate
    assert (r["runs"], r["reviewers_checked"], r["ledger_missing"]) == (5, 15, 1)
    assert (
        r["ledger_missing_rate"] == pytest.approx(1 / 15, abs=1e-6) and r["go"] is True
    )
    assert (r["quote_rows"], r["quote_plan_ok_share"], r["format_errors"]) == (
        15,
        pytest.approx(14 / 15, abs=1e-6),
        1,
    )
    bad = make_compliance(tmp_path / "bad", [["t4-1"], ["t3-1"], [], [], []])
    r = analyze.compliance(bad)  # 2 of 15 is 0.1333
    assert (
        r["ledger_missing_rate"] == pytest.approx(2 / 15, abs=1e-6) and r["go"] is False
    )
    out = tmp_path / "out" / "compliance.json"
    assert analyze.main(["compliance", "--runs", str(ok), "--out", str(out)]) == 0
    assert analyze.main(["compliance", "--runs", str(bad), "--out", str(out)]) == 1
    assert json.loads(out.read_text())["go"] is False
    with pytest.raises(analyze.AnalysisError, match="no run with check"):
        analyze.compliance(tmp_path / "out")


def test_ledger_headings_counted_in_z0_and_k(world):
    runs = analyze.load_runs(world.runs)
    assert analyze.ledger_headings(runs) == {
        "Z0": {"reports": 30, "with_ledger_heading": 0},
        "K": {
            "reports": 29,
            "with_ledger_heading": 0,
        },  # one K reviewer was invalid: no report
    }
    f = world.runs / "z0-synth-a-r1" / "normalised" / "t2b-1.md"
    f.write_text(f.read_text() + "\n## Ledger\n\n| lid |\n")
    k = world.runs / "k-synth-a-r2" / "normalised" / "t3-1.md"
    k.write_text("## Ledger\n" + k.read_text())
    got = analyze.ledger_headings(analyze.load_runs(world.runs))
    assert (got["Z0"]["with_ledger_heading"], got["K"]["with_ledger_heading"]) == (1, 1)


def test_all_writes_every_output(tmp_path):
    w = make_runs.build_stage_runs(tmp_path)
    packages = tmp_path / "packages.json"
    packages.write_text(json.dumps({"packages": {}}))
    out = tmp_path / "out" / "stage-s"
    argv = ["all", "--runs", str(w.runs), "--out", str(out), "--gt", str(w.gt)]
    argv += [
        "--cand-root",
        str(w.cand_root),
        "--packages",
        str(packages),
        "--label",
        "fixture",
    ]
    assert analyze.main(argv) == 0
    names = {p.name for p in out.iterdir()}
    assert names >= {
        "metrics.json",
        "gates.json",
        "d1.json",
        "stages.jsonl",
        "ok_rate_planted.json",
        "judge_audit.json",
        "report.md",
    }
    rows = [json.loads(x) for x in (out / "stages.jsonl").read_text().splitlines()]
    assert len(rows) == 16 and {r["run"] for r in rows} == {
        "ss-stage-r1",
        "z0-stage-r1",
    }
    report = (out / "report.md").read_text()
    assert (
        report.startswith("# Sweep Sheet analysis (fixture)")
        and "## Judge audit" in report
    )
    # D7 has no checklist runs: pending, never passed by default
    assert (
        json.loads((out / "gates.json").read_text())["gates"]["D7"]["status"]
        == "pending"
    )


def test_audit_judges_and_sample_second_judge_commands(world, tmp_path, capsys):
    runs = sorted(p.name for p in world.runs.iterdir())
    for name in runs:  # the sample is drawn over the runs that have a merged report
        (world.runs / name / "merged").mkdir()
        (world.runs / name / "merged" / "merged-1.md").write_text("x")
    capsys.readouterr()
    assert (
        analyze.main(["sample-second-judge", "--runs", str(world.runs), "--seed", "7"])
        == 0
    )
    assert capsys.readouterr().out.split() == judge.sample(runs, 7)
    out = tmp_path / "judge_audit.json"
    # the synthetic judge folders hold only a score file: every one is flagged (no judge output, no merged report)
    assert (
        analyze.main(["audit-judges", "--runs", str(world.runs), "--out", str(out)])
        == 1
    )
    got = json.loads(out.read_text())
    assert (got["checked"], got["bad"]) == (len(runs), len(runs))
    assert "judge_missing" in got["items"][0]["problems"]


def test_stage_names_resolve_as_documented():
    """TESTING section 5: `all --stage 1` reads SW/runs/stage1; `audit-judges stage1` names the folder."""
    ns = analyze.argparse.Namespace
    assert (
        analyze._runs_dir(ns(cmd="all", runs=None, stage="1"))
        == analyze.SW / "runs" / "stage1"
    )
    assert (
        analyze._runs_dir(ns(cmd="audit-judges", runs=None, stage="stage1"))
        == analyze.SW / "runs" / "stage1"
    )
    assert (
        analyze._runs_dir(ns(cmd="all", runs="/tmp/x", stage="1")).as_posix()
        == "/tmp/x"
    )
    with pytest.raises(analyze.AnalysisError, match="stage name"):
        analyze._runs_dir(ns(cmd="all", runs=None, stage=None))
