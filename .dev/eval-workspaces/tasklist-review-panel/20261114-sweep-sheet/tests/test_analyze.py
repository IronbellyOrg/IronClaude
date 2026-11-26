"""REQ-29, REQ-30, REQ-39, REQ-42: the metrics of DESIGN 14.3 over synthetic run folders (F-RUNS).
Every number below that is written as a literal was worked out by hand from the tables of fixtures/runs/make_runs.py."""

import ast
import json
import shutil
import subprocess
import sys

import pytest
from helpers import SW

from analysis import analyze
from fixtures.runs import make_runs

GT = SW / "fixtures" / "gt" / "synthetic-gt.json"


@pytest.fixture
def world(tmp_path):
    return make_runs.build(tmp_path)


def classes_of(runs):
    return {d: analyze.load_classes(GT, d) for d in sorted({r.doc for r in runs})}


def close(got, want, path="metrics"):
    """Every key of `want` is in `got` with an equal value (floats within 1e-9)."""
    if isinstance(want, dict):
        assert isinstance(got, dict), path
        for k, v in want.items():
            assert k in got, f"{path}.{k} is missing"
            close(got[k], v, f"{path}.{k}")
    elif isinstance(want, list):
        assert len(got) == len(want), path
        for i, (g, w) in enumerate(zip(got, want)):
            close(g, w, f"{path}[{i}]")
    elif isinstance(want, float):
        assert got == pytest.approx(want, abs=1e-6), path
    else:
        assert got == want, path


def test_metrics_match_expected_json(world):
    runs = analyze.load_runs(world.runs)
    got = analyze.metrics(runs, classes_of(runs))
    want = json.loads((world.root / "expected.json").read_text())
    assert sorted(got["arms"]) == ["K", "SS", "Z0"] == sorted(want["arms"])
    close(got, want)
    # hand-worked literals, so that the oracle and the code cannot share a mistake
    z = got["arms"]["Z0"]["docs"]["synth-a"]
    assert z["found_fraction"]["per_run"] == [0.375, 0.25, 0.5, 0.25, 0.375]
    assert z["found_fraction"]["mean"] == 0.35
    assert z["found_blocking_fraction"]["per_run"] == [0.25, 0.125, 0.25, 0.125, 0.25]
    assert z["found_blocking_fraction"]["mean"] == 0.2
    assert z["share_runs_found_half"] == 0.2  # one run of five finds 4 of 8
    assert (z["consistent_items"], z["stable_hit_rate"]) == (3, 0.75)
    # the found sets {123}{12}{1234}{13}{123} give 10 pairs: 2/3 3/4 2/3 1 1/2 1/3 2/3 1/2 3/4 2/3 = 6.5, mean 0.65
    assert z["run_jaccard"] == pytest.approx(0.65)
    ss = got["arms"]["SS"]["pooled"]  # 22 + 21 items found over 10 runs of 8
    assert ss["runs"] == 10 and ss["found_fraction"]["mean"] == pytest.approx(43 / 80)
    # the per-class reach: class C1 is item GT1, found in 5 of 5 Z0 runs of synth-a and 0 of 5 of synth-b
    c1 = got["arms"]["Z0"]["pooled"]["class_reach"]["C1"]
    assert (c1["found"], c1["trials"], c1["reach"]) == (5, 10, 0.5)
    assert c1["wilson"] == pytest.approx([0.2366, 0.7634], abs=1e-3)


def test_wilson_interval_literals():
    assert analyze.wilson(0, 0) is None
    lo, hi = analyze.wilson(0, 5)
    assert lo == 0.0 and hi == pytest.approx(0.4345, abs=1e-3)
    lo, hi = analyze.wilson(5, 5)
    assert hi == 1.0 and lo == pytest.approx(0.5655, abs=1e-3)


def test_one_definition_of_found_fraction():
    """REQ-39: an AST search over SW finds each metric name defined only in analysis/analyze.py.

    A definition is a top-level function or class anywhere, or a top-level assignment outside tests/ (a test's own constant
    or a local variable that happens to share a name is not a second definition of the metric)."""
    here = SW / "analysis" / "analyze.py"
    defined = {}
    for path in SW.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        in_tests = "tests" in path.relative_to(SW).parts
        for node in ast.parse(path.read_text(encoding="utf-8")).body:
            names = []
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.append(node.name)
            elif not in_tests and isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                names += [t.id for t in targets if isinstance(t, ast.Name)]
            for n in names:
                if n in analyze.METRICS:
                    defined.setdefault(n, set()).add(path)
    assert "found_fraction" in defined
    for name in analyze.METRICS:
        assert defined.get(name) == {here}, (name, defined.get(name))
        assert callable(getattr(analyze, name))


def d1_of(world, arm="SS"):
    return analyze.d1_inputs(analyze.load_runs(world.runs, scores=False), arm)


def test_d1_uses_medians(world):
    d1 = d1_of(world)
    a, b = d1["docs"]["synth-a"], d1["docs"]["synth-b"]
    # SS synth-a: 135 140 190 145 138 -> median 140 (mean 149.6); Z0: 100 110 95 120 105 -> median 105
    assert (a["arm_median"], a["base_median"]) == (140.0, 105.0)
    assert a["ratio"] == pytest.approx(140 / 105)
    assert a["ratio"] != pytest.approx(149.6 / 106)  # a mean ratio would differ
    # SS synth-b: 130 150 128 160 142 -> 142; Z0: 80 90 85 70 110 -> 85
    assert (b["arm_median"], b["base_median"]) == (142.0, 85.0)
    assert b["ratio"] == pytest.approx(142 / 85, abs=1e-6)
    # 90th percentile by linear interpolation at rank 3.6: SS synth-a sorted 135 138 140 145 190 -> 145 + 0.6 * 45 = 172;
    # Z0 synth-a sorted 95 100 105 110 120 -> 110 + 0.6 * 10 = 116
    assert a["arm_p90"] == 172.0 and a["base_p90"] == 116.0
    # one of 15 reviewers was killed: intention to treat keeps the killed and fallback runs in
    assert d1["reviewers_launched"] == 30 and d1["reviewers_killed"] == 1
    assert d1["kill_share"] == pytest.approx(1 / 30, abs=1e-6)


def test_d1_same_block_only(world):
    base = d1_of(world)
    stray = dict(make_runs.specs(("Z0",), ("synth-a",))[0], rep=9, block=9, secs=9999.0)
    run = make_runs.write_run(world.runs, world.scoring, stray, "jffff01")
    after = d1_of(world)
    assert after["docs"]["synth-a"]["ratio"] == base["docs"]["synth-a"]["ratio"]
    assert after["docs"]["synth-a"]["base_runs"] == 5
    assert after["docs"]["synth-a"]["ignored_base_runs"] == [run.name]
    # a base arm with no run in any block of the arm: the call raises instead of comparing across blocks
    for p in world.runs.glob("z0-synth-b-*"):
        shutil.rmtree(p)
    with pytest.raises(analyze.AnalysisError, match="synth-b: no Z0 run"):
        d1_of(world)


def test_mean_and_median_reported(world, tmp_path):
    runs = analyze.load_runs(world.runs)
    el = analyze.group_metrics(
        [r for r in runs if r.arm == "Z0" and r.doc == "synth-b"]
    )["elapsed_s"]
    assert (el["mean"], el["median"]) == (87.0, 85.0)  # 80 90 85 70 110
    out = tmp_path / "out" / "metrics.json"
    rc = analyze.main(
        ["metrics", "--runs", str(world.runs), "--gt", str(GT), "--out", str(out)]
    )
    assert rc == 0
    got = json.loads(out.read_text())["arms"]["Z0"]["docs"]["synth-b"]["elapsed_s"]
    assert (
        got["mean"] == 87.0 and got["median"] == 85.0 and got["p90"] == 102.0
    )  # 70 80 85 90 110: 90 + 0.6 * 20
    assert (
        out.read_text().endswith("\n")
        and json.loads(out.read_text())["schema"] == "sweep-metrics/1"
    )


def test_kills_retries_per_arm(world):
    runs = analyze.load_runs(world.runs)
    pooled = analyze.metrics(runs)["arms"]
    count = {
        arm: tuple(
            pooled[arm]["pooled"][k]
            for k in ("kills", "retries", "fallbacks", "invalid")
        )
        for arm in pooled
    }
    assert count == {"Z0": (0, 0, 0, 0), "K": (0, 1, 0, 1), "SS": (1, 0, 1, 0)}
    assert pooled["SS"]["docs"]["synth-a"]["fallbacks"] == 1
    assert pooled["SS"]["docs"]["synth-b"]["kills"] == 1


def test_zero_findings_for_killed(world):
    runs = {r.name: r for r in analyze.load_runs(world.runs)}
    run = runs["ss-synth-b-r4"]
    # the killed reviewer left a report with 3 lines behind; it contributes nothing, and nor do its tokens
    stray = world.runs / run.name / "normalised" / "t4-1.md"
    assert stray.read_text().count('"id"') == 3
    assert run.reviewers["t4-1"] == {
        "status": "killed",
        "attempts": 1,
        "tokens": 0,
        "nonprobe": 0,
    }
    # the other two: t2b-1 has 1 non-probe line, t3-1 has 1 non-probe and 2 probe lines
    assert analyze.nonprobe_findings(run) == 2
    inv = runs["k-synth-b-r2"]
    assert (
        inv.reviewers["t3-1"]["status"] == "invalid"
        and inv.reviewers["t3-1"]["nonprobe"] == 0
    )


def test_nonprobe_findings_per_run(world):
    runs = analyze.load_runs(world.runs)
    got = analyze.metrics(runs)["arms"]
    # SS synth-a: reviewers (1,1,1) (1,1,0) (1,1,2) (2,1,1) (1,0,1) -> 3 2 4 4 2; the probe and ledger lines are not in it
    assert got["SS"]["docs"]["synth-a"]["nonprobe_findings"]["per_run"] == [
        3,
        2,
        4,
        4,
        2,
    ]
    assert got["SS"]["docs"]["synth-a"]["nonprobe_findings"]["mean"] == 3.0
    report = (world.runs / "ss-synth-a-r1" / "normalised" / "t3-1.md").read_text()
    assert (
        report.count('"probe": "S') == 3
    )  # 3 probe lines are in the file and are not counted
    # Z0 has no sheet: its non-probe count is simply every line
    assert got["Z0"]["docs"]["synth-a"]["nonprobe_findings"]["per_run"] == [
        4,
        3,
        5,
        4,
        3,
    ]


def test_promoted_lines_not_counted_as_reviewer_findings(world):
    runs = {r.name: r for r in analyze.load_runs(world.runs)}
    run = runs["ss-synth-a-r5"]
    text = (world.runs / run.name / "normalised" / "t4-1.md").read_text()
    assert text.count('"src": "ledger"') == 2  # two promoted lines sit in this report
    assert run.reviewers["t4-1"]["nonprobe"] == 1  # only its own finding counts
    assert analyze.nonprobe_findings(run) == 2  # t2b-1 1 + t3-1 0 + t4-1 1


def test_z0_raw_reads_the_raw_reports(tmp_path):
    w = make_runs.build(tmp_path, arms=make_runs.ALL_ARMS)
    run = w.runs / "z0raw-synth-a-r1"
    assert (run / "reviews" / "t2b-1.md").is_file() and not (
        run / "normalised" / "t2b-1.md"
    ).exists()
    runs = analyze.load_runs(w.runs)
    assert analyze.nonprobe_findings({r.name: r for r in runs}["z0raw-synth-a-r1"]) == 3
    want = json.loads((w.root / "expected.json").read_text())
    close(analyze.metrics(runs, classes_of(runs)), want)
    assert sorted(want["arms"]) == ["K", "SS", "Z0", "Z0-raw"]


def test_unscored_run_and_unwritable_output_are_refused(world, tmp_path):
    (world.runs / "z0-synth-a-r1" / "scoring" / "label-key.json").unlink()
    with pytest.raises(analyze.AnalysisError, match="no judge score file"):
        analyze.load_runs(world.runs)
    assert (
        len(analyze.load_runs(world.runs, scores=False)) == 30
    )  # the time inputs need no judge
    rc = analyze.main(
        [
            "d1",
            "--runs",
            str(world.runs),
            "--arm",
            "SS",
            "--out",
            "/var/tmp/sw-d1-refused.json",
        ]
    )
    assert rc == 1


def test_command_line_help():
    # -B: `-I` ignores PYTHONDONTWRITEBYTECODE, and the script imports scaffold, so it would leave a __pycache__ in SW
    before = set(SW.rglob("__pycache__"))
    r = subprocess.run(
        [sys.executable, "-I", "-B", str(SW / "analysis" / "analyze.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0 and "metrics" in r.stdout and "d1" in r.stdout
    assert set(SW.rglob("__pycache__")) == before
