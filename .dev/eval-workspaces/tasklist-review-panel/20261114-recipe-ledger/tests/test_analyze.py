"""REQ-17 (the check itself), REQ-29, REQ-30, REQ-39, REQ-42 and REQ-43 (analysis side) on the F-RUNS-RL fixture.
Tier B file under test: analysis/analyze.py, built locally. The ground truth is fixtures/gt/synthetic-gt.json only; no
test reads a study file."""

import ast
import json
import shutil
from pathlib import Path

import pytest
from analysis_support import fixture

from analysis import analyze as az
from analysis import judge_audit as ja
from fixtures.runs import make_runs as mr

RL = Path(__file__).resolve().parents[1]
ABS = 1e-9


@pytest.fixture(scope="module")
def fx(tmp_path_factory):
    return fixture(tmp_path_factory)


@pytest.fixture(scope="module")
def fx_d6(tmp_path_factory):
    return fixture(tmp_path_factory, "d6fail")


def near(got, want):
    assert got == pytest.approx(want, abs=ABS), (got, want)


# ---------------------------------------------------------------- REQ-39


def test_metrics_match_expected_json(fx):
    exp = mr.EXPECTED
    for arm, want in exp["arms"].items():
        got = fx.metrics["arms"][arm]["pooled"]
        for key, value in want.items():
            if key == "class_reach":
                for cls, (hits, trials) in value.items():
                    assert (got[key][cls]["hits"], got[key][cls]["trials"]) == (
                        hits,
                        trials,
                    ), (arm, cls)
                assert set(got[key]) == set(value), (
                    arm
                )  # a class with no item does not appear
            else:
                assert got[key] == pytest.approx(value, abs=ABS), (arm, key)
    for arm, docs in exp["documents"].items():
        for doc, want in docs.items():
            for key, value in want.items():
                near(fx.metrics["arms"][arm]["documents"][doc][key], value)
    for name, value in exp["shares"].items():
        near(fx.metrics["shares"][name]["value"], value)
    d1 = fx.metrics["gates"]["RL"]["D1"]
    for doc in ("doc-a", "doc-b"):
        for key, value in exp["d1"][doc].items():
            near(d1["per_doc"][doc][key], value)
    assert d1["kills"] == exp["d1"]["kills"]
    near(d1["kill_rate"], exp["d1"]["kill_rate"])
    gates = fx.metrics["gates"]["RL"]
    near(gates["D2"]["diff"], exp["gates"]["D2_diff"])
    near(gates["D7"]["gain_over_k"], exp["gates"]["D7_gain"])
    assert [gates["D3"]["candidate"], gates["D3"]["control"]] == exp["gates"]["D3"]
    for cls, points in exp["ablation"].items():
        near(fx.metrics["ablation"][cls]["points"], points)
    t = fx.metrics["time"]
    for key, name in (
        ("b", "b"),
        ("breakeven", "breakeven_row_cost_14"),
        ("c", "luna_cost_per_row"),
        ("cap", "luna_row_cap"),
    ):
        near(t[name]["planned"], exp["time"][key][0])
        near(t[name]["measured"], exp["time"][key][1])


def test_expected_json_is_the_written_out_expectation():
    on_disk = json.loads(
        (RL / "fixtures" / "runs" / "expected.json").read_text(encoding="utf-8")
    )
    assert on_disk == json.loads(json.dumps(mr.EXPECTED))


def test_one_definition_of_found_fraction():
    """An AST search of RL: each metric function of analyze.py is defined in analysis/analyze.py and nowhere else."""
    defs = {}
    for path in sorted(RL.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            names = []
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
                names = [node.name]
            elif isinstance(node, ast.Assign):
                names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                names = [node.target.id]
            for name in names:
                defs.setdefault(name, set()).add(str(path.relative_to(RL)))
    assert "found_fraction" in az.METRIC_FUNCTIONS
    for name in az.METRIC_FUNCTIONS:
        assert defs.get(name) == {"analysis/analyze.py"}, (name, defs.get(name))


def test_wilson_known_values():
    lo, hi = az.wilson(3, 5)
    assert (round(lo, 4), round(hi, 4)) == (0.2307, 0.8824)
    assert az.wilson(0, 5)[0] == 0.0
    near(az.wilson(0, 5)[1], 3.8416 / 8.8416)
    near(az.wilson(5, 5)[0], 5 / 8.8416)
    assert az.wilson(5, 5)[1] == 1.0
    assert az.wilson(0, 0) == (None, None)


def test_bootstrap_resamples_documents_then_runs():
    cand = {"a": [0.5] * 5, "b": [1.0] * 5}
    ctrl = {"a": [0.0] * 5, "b": [0.0] * 5}
    diffs = az.bootstrap_diff(cand, ctrl, seed=3, n=400)
    # documents are drawn first: with two documents the pooled difference can only be 0.5, 0.75 or 1.0; a pool that
    # mixed the runs of both documents would give other values
    assert set(diffs) == {0.5, 0.75, 1.0}
    assert diffs == az.bootstrap_diff(cand, ctrl, seed=3, n=400)  # seeded
    assert diffs != az.bootstrap_diff(cand, ctrl, seed=4, n=400)


def test_bootstrap_then_runs_inside_a_document():
    ctrl = {"a": [0.0] * 4}
    diffs = az.bootstrap_diff({"a": [0.0, 1.0, 0.0, 1.0]}, ctrl, seed=1, n=300)
    assert (
        set(diffs) <= {0.0, 0.25, 0.5, 0.75, 1.0} and len(set(diffs)) > 2
    )  # the runs of the chosen document vary


# ---------------------------------------------------------------- REQ-29


def fake_runs(label, doc, elapsed, blocks=None, kills=0):
    blocks = blocks or range(1, len(elapsed) + 1)
    return [
        {
            "id": f"{label}-{doc}-{b}",
            "label": label,
            "doc": doc,
            "block": b,
            "timing": {"panel_elapsed_s": e},
            "meta": {"reviewers": {"x": {"killed": i < kills}, "y": {}, "z": {}}},
        }
        for i, (b, e) in enumerate(zip(blocks, elapsed, strict=True))
    ]


def test_d1_uses_medians():
    """The mean ratio is 1.73, the median and the 90th percentile ratios are 1.0: the gate decides on the medians."""
    cand = fake_runs("RL", "d", [100] * 10 + [900])
    ctrl = fake_runs("Z0", "d", [100] * 11)
    d = az.d1(cand, ctrl)
    row = d["per_doc"]["d"]
    near(row["ratio_median"], 1.0)
    near(row["ratio_p90"], 1.0)
    near(row["ratio_mean"], (1000 + 900) / 11 / 100)
    assert row["ratio_mean"] > 1.35 and d["pass"] is True


def test_d1_fails_on_the_median_ratio():
    d = az.d1(fake_runs("RL", "d", [136] * 5), fake_runs("Z0", "d", [100] * 5))
    assert (
        d["per_doc"]["d"]["ratio_median"] == pytest.approx(1.36) and d["pass"] is False
    )
    assert (
        az.d1(fake_runs("RL", "d", [135] * 5), fake_runs("Z0", "d", [100] * 5))["pass"]
        is True
    )  # 1.35 is allowed


def test_d1_p90_and_kills_limits():
    slow_tail = fake_runs(
        "RL", "d", [100, 100, 100, 100, 160]
    )  # p90 = 100 + .6 x 60 = 136 -> ratio 1.36 passes
    assert az.d1(slow_tail, fake_runs("Z0", "d", [100] * 5))["pass"] is True
    tail = fake_runs(
        "RL", "d", [100, 100, 100, 100, 200]
    )  # p90 = 160 -> 1.6 fails although the median ratio is 1
    assert az.d1(tail, fake_runs("Z0", "d", [100] * 5))["pass"] is False
    ctrl = fake_runs("Z0", "d", [100] * 5)
    one = az.d1(
        fake_runs("RL", "d", [100] * 5, kills=1), ctrl
    )  # 1 of 15 reviewer runs is 6.7%: allowed
    assert one["pass"] is True and one["kill_rate"] == pytest.approx(1 / 15)
    two = az.d1(fake_runs("RL", "d", [100] * 5, kills=2), ctrl)  # 2 of 15 is 13.3%
    assert two["pass"] is False and two["kills"] == 2


def test_d1_same_block_only():
    cand = fake_runs("RL", "d", [120, 120, 120], blocks=[1, 2, 3])
    ctrl = fake_runs("Z0", "d", [100, 100, 100, 9999], blocks=[1, 2, 3, 9])
    d = az.d1(cand, ctrl)["per_doc"]["d"]
    near(d["ratio_median"], 1.2)
    assert d["ignored_control_runs"] == [
        "Z0-d-9"
    ]  # the Z0 run of another block is ignored
    with pytest.raises(ValueError, match="no same-block control run"):
        az.d1(fake_runs("RL", "d", [120, 120], blocks=[1, 4]), ctrl)


def test_d1_on_the_fixture_is_per_document(fx):
    d1 = fx.metrics["gates"]["RL"]["D1"]
    assert set(d1["per_doc"]) == {"doc-a", "doc-b"} and d1["pass"] is True
    assert all(v["ignored_control_runs"] == [] for v in d1["per_doc"].values())


def test_mean_and_median_reported(fx, tmp_path):
    pooled = fx.metrics["arms"]["RL"]["pooled"]
    assert {"elapsed_mean", "elapsed_median", "elapsed_p90"} <= set(pooled)
    row = fx.metrics["gates"]["RL"]["D1"]["per_doc"]["doc-a"]
    assert (
        {"mean", "median", "p90"} <= set(row["candidate"])
        and "ratio_mean" in row
        and "ratio_median" in row
    )
    text = az.build_report(fx.metrics)
    assert "elapsed_mean" in text and "elapsed_median" in text
    assert "mean ratio" in text and "median ratio" in text
    out = tmp_path / "out"
    rc = az.main(
        [
            "all",
            "--stage",
            "1",
            "--runs",
            str(fx.fx.runs),
            "--scoring",
            str(fx.fx.scoring),
            "--gt",
            str(fx.fx.gt),
            "--out",
            str(out),
            "--boot",
            "50",
        ]
    )
    assert rc == 0
    d1 = json.loads((out / "d1.json").read_text(encoding="utf-8"))
    assert d1["RL"]["per_doc"]["doc-a"]["ratio_mean"] > 0  # d1.json carries both


# ---------------------------------------------------------------- REQ-30


def test_kills_retries_per_arm(fx):
    for arm, want in mr.EXPECTED["arms"].items():
        got = fx.metrics["arms"][arm]["pooled"]
        for key in (
            "kills",
            "reviewer_runs",
            "retries",
            "fallbacks",
            "invalid",
            "check_skipped",
        ):
            assert got[key] == want[key], (arm, key)


def test_zero_findings_for_killed(fx):
    run = fx.by_id["stage1-rl-doc-a-r3"]  # t4-1 was killed
    assert "t4-1" not in az.reviewers(run) and az.report_text(run, "t4-1") == ""
    assert az.nonprobe_findings(az.report_text(run, "t4-1")) == 0
    assert (
        az.run_nonprobe(run) == 2
    )  # one free line from each of the two reviewers that finished
    cells = [r for r in fx.rows if r["run"] == run["id"] and r["reviewer_id"] == "t4-1"]
    assert cells and not any(
        r["selection"] or r["act"] or r["merge_survival"] for r in cells
    )
    z0 = fx.by_id["stage1-z0-doc-a-r3"]  # t3-1 was killed
    assert az.run_nonprobe(z0) == 4
    assert not any(
        r["merge_survival"]
        for r in fx.rows
        if r["run"] == z0["id"] and r["reviewer_id"] == "t3-1"
    )


def test_reask_counted_apart_from_retries(fx):
    rl = fx.metrics["arms"]["RL"]["pooled"]
    assert (rl["reasks"], rl["retries"]) == (1, 1)
    reasked = fx.by_id["stage1-rl-doc-b-r2"]["meta"]
    retried = fx.by_id["stage1-rl-doc-b-r1"]["meta"]
    assert (
        reasked["reask"] == ["t2b-1"] and reasked["retries"] == 0
    )  # a re-ask is not a retry
    assert retried["retries"] == 1 and retried["reask"] == []
    assert fx.metrics["arms"]["K"]["pooled"]["reasks"] == 0
    header = az.build_report(fx.metrics).split("| arm |")[1].splitlines()[0]
    assert "retries" in header and "reasks" in header


# ---------------------------------------------------------------- REQ-42


def test_nonprobe_findings_per_run(fx):
    for arm, want in mr.EXPECTED["arms"].items():
        near(
            fx.metrics["arms"][arm]["pooled"]["nonprobe_findings_per_run"],
            want["nonprobe_findings_per_run"],
        )


def line(**kw):
    return json.dumps({"id": "F", "claim": "c", **kw})


def report(*lines):
    return (
        "## Findings block\n\n```findings-v1\n"
        + "\n".join(lines)
        + "\n```\n\nverdict: PASS\n"
    )


def test_promoted_lines_not_counted_as_reviewer_findings(fx):
    text = report(
        line(),
        line(probe="C4.2"),
        line(src="ledger"),
        line(probe="C7.2", src="ledger", **{"class": "C7"}),
    )
    assert az.nonprobe_findings(text) == 1  # only the line with neither key counts
    assert (
        az.nonprobe_findings(report(line(probe=None, src=None), line(src="other"))) == 2
    )
    run = fx.by_id["stage1-rl-doc-b-r5"]
    promoted = az.report_text(
        run, "t3-1"
    )  # the report that reaches the merge: one free line and one promoted line
    assert len(az.finding_lines(promoted)) == 2 and az.nonprobe_findings(promoted) == 1
    raw = (run["dir"] / "reviews" / "t3-1.md").read_text(encoding="utf-8")
    assert len(az.finding_lines(raw)) == 1  # the raw message has no promoted line
    linked = az.report_text(run, "t2b-1")  # a free line and a finding linked by `probe`
    assert len(az.finding_lines(linked)) == 2 and az.nonprobe_findings(linked) == 1


def test_d6_failure_blocks_adoption(fx, fx_d6):
    ok = fx.metrics["gates"]["RL"]
    assert (
        ok["D6"]["pass"] is True
        and fx.metrics["decisions"]["RL"]["decision"] == "adopt"
    )
    g = fx_d6.metrics["gates"]["RL"]
    assert (
        g["D2"]["pass"] is True and g["D3"]["pass"] is True
    )  # the effect and the consistency gates hold
    assert g["D6"]["pass"] is False and list(g["D6"]["regressed_items"]) == ["doc-a/A1"]
    near(g["D6"]["regressed_items"]["doc-a/A1"]["candidate"], 0.6)
    near(g["D6"]["regressed_items"]["doc-a/A1"]["control"], 0.8)
    dec = fx_d6.metrics["decisions"]["RL"]
    assert (
        dec["decision"] == "do not adopt"
        and dec["blocking_failed"] == ["D6"]
        and dec["failed"] == ["D6"]
    )
    assert "do not adopt" in az.build_report(fx_d6.metrics)


def test_decide_does_not_adopt_with_d6_failed_and_everything_else_passing():
    gates = {g: {"pass": True} for g in ("D1", "D2", "D3", "D4", "D7")}
    gates["D6"] = {"pass": False, "blocking": True}
    dec = az.decide(gates)
    assert dec["decision"] == "do not adopt" and dec["blocking_failed"] == ["D6"]
    gates["D6"] = {"pass": True, "blocking": True}
    assert az.decide(gates)["decision"] == "adopt"
    gates["D7"] = {
        "pass": None,
        "status": "no K runs",
    }  # a gate that was not evaluated is not a pass
    assert az.decide(gates)["failed"] == ["D7"]
    gates["D7"] = {"pass": True}
    assert az.decide(gates, stage=2)["failed"] == ["D5"]  # D5 is required from Stage 2


def test_d5_planted_detection_and_claim_scope(fx):
    sets = {"doc-a": "planted", "doc-b": "decision"}
    g = az.gates_for(
        "RL", "Z0", "K", az.split_arms(fx.runs), fx.gt, fx.scores, sets, az.SEED, 50
    )
    assert g["D5"]["pass"] is True  # C2 0.8, C4 1.0, C5 0.6 reach 0.40; C8 does not
    assert g["D5"]["general_classes_holding"] == ["C2", "C4", "C5"]
    none = az.gates_for(
        "RL", "Z0", "K", az.split_arms(fx.runs), fx.gt, fx.scores, {}, az.SEED, 50
    )
    assert none["D5"]["pass"] is None
    clean = az.gates_for(
        "RL",
        "Z0",
        "K",
        az.split_arms(fx.runs),
        fx.gt,
        fx.scores,
        {"doc-b": "clean"},
        az.SEED,
        50,
    )
    assert clean["D4"]["clean_blocking_diff"] == 0.0 and clean["D4"]["pass"] is True


# ---------------------------------------------------------------- REQ-17


def test_compliance_report_on_fixture(fx, capsys):
    want = mr.EXPECTED["compliance"]
    got = az.compliance(az.run_dirs_of([fx.fx.runs]))
    assert (
        got["runs_checked"] == want["runs_checked"]
        and got["reviewer_runs"] == want["reviewer_runs"]
    )
    assert got["reviewers_without_ledger_file"] == want["reviewers_without_ledger_file"]
    assert got["ledger_missing"]["count"] == want["ledger_missing_count"]
    near(got["ledger_missing"]["rate"], 2 / 23)
    assert got["ledger_missing"]["pass"] is True
    assert got["recipe_missing"] == want["recipe_missing"]
    assert (got["quote_plan"]["rows_with_quote"], got["quote_plan"]["ok"]) == (
        want["quote_rows"],
        want["quote_ok"],
    )
    near(got["quote_plan"]["share"], 22 / 23)
    assert got["format_errors"] == want["format_errors"]
    assert got["none_found"] == want["none_found"]
    assert got["over_budget"] == want["over_budget"] and got["reask"] == want["reask"]
    for rid, mean in want["rows_per_reviewer"].items():
        near(got["rows_per_reviewer"][rid], mean)
    assert az.main(["compliance", "--runs", str(fx.fx.runs)]) == 0
    printed = capsys.readouterr().out
    for word in (
        "ledger_missing: 2 of 23",
        "recipe_missing per class: {'C3': 1, 'C7': 1}",
        "22 of 23",
        "format errors: 1",
        "none_found per class: {'C3': 6}",
    ):
        assert word in printed


def test_compliance_fails_above_ten_percent(fx, tmp_path):
    runs = tmp_path / "runs"
    runs.mkdir()
    for name in (
        "stage1-rl-doc-b-r4",
        "stage1-rl-doc-b-r5",
    ):  # 1 of 6 ledgers is missing: 16.7%
        shutil.copytree(fx.fx.runs / name, runs / name)
    assert az.main(["compliance", "--runs", str(runs)]) == 1
    assert (
        az.compliance(az.run_dirs_of([runs / "stage1-rl-doc-b-r5"]))["ledger_missing"][
            "pass"
        ]
        is True
    )


# ---------------------------------------------------------------- DESIGN 12.5: the ledger metrics per arm


def test_ledger_metrics_per_arm_match_expected(fx):
    for arm, want in mr.EXPECTED["ledger_metrics"].items():
        got = fx.metrics["arms"][arm]["pooled"]
        y = got["reask_yield"]
        for name, (runs, mean) in want["reask_yield"].items():
            assert y[name]["runs"] == runs, (arm, name)
            if mean is None:
                assert y[name]["found_fraction_mean"] is None
            else:
                near(y[name]["found_fraction_mean"], mean)
        # an arm that writes no ledger and no check.json counts zero everywhere
        zero = {
            "over_budget": {"recipe": 0, "lens": 0},
            "recipe_missing": {},
            "unknown_item": 0,
            "classes_lost": {},
            "reask_asked": 0,
            "reask_accepted": 0,
            "none_found_share": {},
            "rows_per_lens": {},
        }
        for key, value in {
            **zero,
            **{k: v for k, v in want.items() if k != "reask_yield"},
        }.items():
            if key == "none_found_share":
                assert {
                    c: [v["none_found"], v["ran"]] for c, v in got[key].items()
                } == value, arm
                for c, v in got[key].items():
                    near(v["share"], value[c][0] / value[c][1])
            elif key == "rows_per_lens":
                assert set(got[key]) == set(value), arm
                for rid, mean in value.items():
                    near(got[key][rid], mean)
            else:
                assert got[key] == value, (arm, key)


def test_ledger_metrics_per_document_and_in_the_report(fx):
    doc_b = fx.metrics["arms"]["RL"]["documents"]["doc-b"]  # r2 is the re-asked run
    assert doc_b["reask_yield"]["with"] == {
        "runs": 1,
        "found_fraction_mean": pytest.approx(2 / 3),
    }
    near(doc_b["reask_yield"]["without"]["found_fraction_mean"], (10 / 3 - 2 / 3) / 4)
    assert fx.metrics["arms"]["RL"]["documents"]["doc-a"]["classes_lost"] == {
        "C1": 1,
        "C3": 1,
    }
    assert doc_b["recipe_missing"] == {"C3": 1} and doc_b["over_budget"] == {
        "recipe": 0,
        "lens": 0,
    }
    text = az.build_report(fx.metrics)
    for word in (
        "## Ledger checks and re-asks per arm",
        "| RL | 0 | 1 | {'C3': 1, 'C7': 1} | 0 | {'C1': 1, 'C3': 1} | 1 | 1 | 0.667 (1) | 0.630 (9) |",
        "| RL | C3 | 6 | 6 | 1.000 |",
        "| RL | C2 | 0 | 14 | 0.000 |",
        "| RL | t3-1 | 4.000 |",
        "| RL | t2b-1 | 5.500 |",
        "## Reach per class per reviewer id",
        "| RL | C4 | t2b-1 | 10 | 8 | 7 | 7 | 9 |",
    ):
        assert word in text, word


def led(rid, rows, **kw):
    return {
        "rid": rid,
        "ledger_missing": False,
        "recipe_missing": [],
        "unknown_item": [],
        "rows": rows,
        **kw,
    }


def lrow(item, over=None, none_found=False, unknown=False):
    return {
        "item": item,
        "over_budget": over,
        "none_found": none_found,
        "unknown_item": unknown,
    }


def test_ledger_counts_on_synthetic_ledgers():
    """The fixture has no unknown_item and no recipe-budget overrun; these ledgers do. Counted by hand:
    unknown_item 2 (the two entries of the second ledger); over_budget recipe 1 (C4.3), lens 1 (C5.2); recipe_missing
    C6 once; C5 ran in 2 ledgers (the unknown C5.9 row of the third does not count), NONE FOUND in 1; C4 ran in 2
    ledgers, NONE FOUND in 1 although it has two such rows there (a reviewer-run is counted once); the missing
    ledger counts for nothing; rows per lens: t2b-1 (4 + 3 rows) / 2 = 3.5, t3-1 1 row."""
    a = led(
        "t2b-1",
        [
            lrow("C4.1", none_found=True),
            lrow("C4.2", none_found=True),
            lrow("C4.3", over="recipe"),
            lrow("C5.1", none_found=True),
        ],
        recipe_missing=["C6"],
    )
    b = led(
        "t2b-1",
        [lrow("C4.1"), lrow("C5.1"), lrow("C5.2", over="lens")],
        unknown_item=["X1", "C9.1"],
    )
    c = led("t3-1", [lrow("C5.9", unknown=True)])
    gone = led("t3-1", [], ledger_missing=True)
    got = az.ledger_counts([a, b, c, gone])
    assert got["unknown_item"] == 2
    assert got["over_budget"] == {"recipe": 1, "lens": 1}
    assert got["recipe_missing"] == {"C6": 1}
    assert got["none_found_share"] == {
        "C4": {"none_found": 1, "ran": 2, "share": 0.5},
        "C5": {"none_found": 1, "ran": 2, "share": 0.5},
    }
    assert got["rows_per_lens"] == {"t2b-1": 3.5, "t3-1": 1.0}
    assert az.ledger_counts([])["none_found_share"] == {}


def test_reask_yield_groups_runs_and_leaves_an_empty_group_none():
    y = az.reask_yield([0.5, 1.0, 0.0], [True, False, False])
    assert y == {
        "with": {"runs": 1, "found_fraction_mean": 0.5},
        "without": {"runs": 2, "found_fraction_mean": 0.5},
    }
    assert az.reask_yield([0.5], [False])["with"] == {
        "runs": 0,
        "found_fraction_mean": None,
    }


# ---------------------------------------------------------------- REQ-43, analysis side


def test_audit_judges_subcommand(fx, tmp_path, capsys):
    assert az.main(["audit-judges", "stage1", "--scoring-dir", str(fx.fx.scoring)]) == 0
    assert "bad = 0" in capsys.readouterr().out
    bad = tmp_path / "scoring"
    shutil.copytree(fx.fx.scoring, bad)
    label = next(p.name for p in sorted(bad.iterdir()) if p.is_dir())
    (bad / label / "judge.err").write_text(
        "API Error: 529 overloaded_error\n", encoding="utf-8"
    )
    out = tmp_path / "audit.json"
    assert (
        az.main(
            ["audit-judges", "stage1", "--scoring-dir", str(bad), "--out", str(out)]
        )
        == 1
    )
    audit = json.loads(out.read_text(encoding="utf-8"))
    assert audit["bad"] == 1
    assert [(i["label"], i["flags"]) for i in audit["items"] if not i["ok"]] == [
        (label, ["api_error"])
    ]


def test_sample_second_judge_subcommand(fx, capsys):
    names = [r["id"] for r in fx.runs]
    argv = [
        "sample-second-judge",
        "--seed",
        "7",
        "--runs-dir",
        str(fx.fx.runs),
        "--stage",
        "stage1",
    ]
    assert az.main(argv) == 0
    first = capsys.readouterr().out.split()
    assert len(first) == round(0.15 * 40) == 6 and set(first) <= set(names)
    assert first == ja.sample(names, 7)  # the sample of judge_audit.py, not another one
    assert (
        az.main(argv) == 0 and capsys.readouterr().out.split() == first
    )  # repeats for a fixed seed
    assert (
        az.main(
            [
                "sample-second-judge",
                "--seed",
                "8",
                "--runs-dir",
                str(fx.fx.runs),
                "--stage",
                "stage1",
            ]
        )
        == 0
    )
    assert capsys.readouterr().out.split() != first


def test_all_stops_on_a_run_without_a_valid_score(fx, tmp_path, capsys):
    scoring = tmp_path / "scoring"
    shutil.copytree(fx.fx.scoring, scoring)
    first = next(
        line.split("\t")[0]
        for line in (scoring / "labels.tsv").read_text().splitlines()
        if line.endswith("first")
    )
    (scoring / first / "score.json").unlink()
    argv = [
        "all",
        "--stage",
        "1",
        "--runs",
        str(fx.fx.runs),
        "--scoring",
        str(scoring),
        "--gt",
        str(fx.fx.gt),
        "--out",
        str(tmp_path / "o"),
        "--boot",
        "20",
    ]
    assert az.main(argv) == 1
    assert "E_UNSCORED" in capsys.readouterr().err
    assert az.main([*argv, "--allow-unscored"]) == 0


# ---------------------------------------------------------------- K3: the ground truth has no default


def test_ground_truth_path_has_no_default(monkeypatch, capsys):
    monkeypatch.delenv("RL_GT", raising=False)
    assert az.main(["all", "--stage", "1"]) == 2
    assert az.main(["ablate-report"]) == 2
    assert "no default" in capsys.readouterr().err
    src = (RL / "analysis" / "analyze.py").read_text(encoding="utf-8")
    assert (
        "20261111-a1" not in src
        and "20261113-collab" not in src
        and "holdout-gt" not in src
    )


def test_ablate_report_subcommand(fx, capsys):
    argv = [
        "ablate-report",
        "--gt",
        str(fx.fx.gt),
        "--runs",
        str(fx.fx.runs),
        "--stage",
        "1",
    ]
    assert az.main(argv) == 0
    out = capsys.readouterr().out
    assert (
        "C4: other classes gain 1.75 points (1 of 57 rows)" in out
        and "limit 15: pass" in out
    )


def test_compliance_reports_the_strict_reading_next_to_the_lenient_one(fx, capsys):
    """Owner order 2026-11-15: forgiven slips are counted, and a strict reading (nothing forgiven) is printed per arm."""
    got = az.compliance(az.run_dirs_of([fx.fx.runs]))
    st = got["strict"]
    # the fixture holds no forgiven slip, so the two readings agree
    assert st["forgiven_reports"] == 0 and st["forgiven_by_kind"] == {}
    assert (
        st["ledger_missing_strict"]["count"] == got["ledger_missing"]["count"]
        and st["ledger_missing_strict"]["pass"] is True
    )
    az.main(["compliance", "--runs", str(fx.fx.runs)])
    assert "strict reading (nothing forgiven): ledger_missing 2 of 23" in capsys.readouterr().out
    # a forgiven slip makes the report count as missing in the strict reading only
    ledgers = [
        {"forgiven": ["heading_between"], "rows": []},
        {"forgiven": [], "rows": [{"item": "C4.1", "item_raw": "R-C4.1"}]},
        {"forgiven": [], "rows": [{"item": "C4.1"}]},
    ]
    assert [az._forgiven_in(x) for x in ledgers] == [True, True, False]
    assert az._forgiven_kinds(ledgers) == {"heading_between": 1, "item_affix": 1}
