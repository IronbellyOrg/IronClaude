"""REQ-41: reach per stage. Rows of stages.jsonl have the five stage fields, the class and the reviewer id; the selection
rule is the one of FND.same_defect; the values on the F-RUNS-RL fixture equal the hand-computed ones in make_runs.py.
Tier B file under test: analysis/analyze.py (built locally)."""

import json
from pathlib import Path

import pytest
from analysis_support import fixture

from analysis import analyze as az
from fixtures.runs import make_runs as mr

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
ROW_KEYS = {
    "run",
    "arm",
    "doc",
    "item",
    "class",
    "blocking_in_implement",
    "reviewer_id",
    "extraction",
    "selection",
    "act",
    "merge_survival",
    "judge_credit",
}


@pytest.fixture(scope="module")
def fx(tmp_path_factory):
    return fixture(tmp_path_factory)


def cell(fx, run, item, rid):
    (row,) = [
        r
        for r in fx.rows
        if (r["run"], r["item"], r["reviewer_id"]) == (run, item, rid)
    ]
    return row


def test_stage_rows_schema(fx, tmp_path):
    # one row per (run, ground-truth item, reviewer): 4 arms x (5 runs x 4 items + 5 runs x 3 items) x 3 reviewers
    assert len(fx.rows) == 4 * (5 * 4 + 5 * 3) * 3 == 420
    classes = {i["class"] for items in fx.gt.values() for i in items}
    for r in fx.rows:
        assert set(r) == ROW_KEYS
        assert r["extraction"] is None  # no extractor in RL
        assert r["selection"] in (True, False, None) and r["act"] in (True, False, None)
        assert isinstance(r["merge_survival"], bool)
        assert set(r["judge_credit"]) == {"any", "blocking"}
        assert r["class"] in classes and r["reviewer_id"] in {"t2b-1", "t3-1", "t4-1"}
    rl = [r for r in fx.rows if r["arm"] == "RL"]
    assert len(rl) == 105 and sum(r["selection"] is None for r in rl) == 24
    assert all(r["selection"] is None for r in fx.rows if r["arm"] != "RL")
    # a run whose check was skipped or that fell back has null selection and act, a run with a ledger has booleans
    for run in ("stage1-rl-doc-a-r2", "stage1-rl-doc-a-r5"):
        assert all(
            r["selection"] is None and r["act"] is None
            for r in fx.rows
            if r["run"] == run
        )
    assert all(
        isinstance(r["selection"], bool)
        for r in fx.rows
        if r["run"] == "stage1-rl-doc-b-r3"
    )
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
            "20",
        ]
    )
    assert rc == 0
    written = [
        json.loads(x)
        for x in (out / "stages.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(written) == 420 and all(set(r) == ROW_KEYS for r in written)


def test_selection_covers_rule():
    plan = (PLANS / "p_basic.md").read_text(encoding="utf-8")
    item = "Every module under `src/exporter/` returns an empty result for an empty report."  # line 34
    covers = az.covers
    assert covers(item, item, plan)
    assert covers(
        f"- {item} Extra words.", item, plan
    )  # the quote contains the item's text
    assert covers(
        "returns an empty result for an empty report", item, plan
    )  # the item contains the quote
    assert covers(
        " ".join(item.split()), item.replace(" returns", "\n returns"), plan
    )  # whitespace is flattened
    near = '- `render(rows, fmt="ndjson")` returns one JSON object per row, one object per line.'  # line 33
    assert covers(near, item, plan)  # the spans lie within 3 lines
    assert covers("Acceptance criteria:", item, plan)  # line 32, two lines above
    far = "update the count from 3 report formats to 4 report formats"  # line 40
    assert not covers(far, item, plan)
    assert not covers(far, item, None)  # without the candidate only containment counts
    assert not covers("", item, plan) and not covers(item, "", plan)
    assert not covers("this text is nowhere in the plan", item, plan)


def test_selection_counts_only_accepted_within_budget_rows():
    plan = (PLANS / "p_basic.md").read_text(encoding="utf-8")
    quote = "Every module under `src/exporter/` returns an empty result for an empty report."
    base = {
        "item": "C4.2",
        "quote_plan": quote,
        "quote_other": "",
        "unknown_item": False,
        "over_budget": None,
    }
    assert az.covering_rows([base], quote, plan) == [base]
    assert az.covering_rows([dict(base, over_budget="lens")], quote, plan) == []
    assert az.covering_rows([dict(base, over_budget="recipe")], quote, plan) == []
    assert az.covering_rows([dict(base, unknown_item=True)], quote, plan) == []
    assert az.covering_rows(
        [dict(base, quote_plan="", quote_other=quote)], quote, plan
    )  # quote_other counts too
    assert (
        az.covering_rows([dict(base, quote_plan="")], quote, plan) == []
    )  # an OK row with no quote selects nothing


def test_stage_values_on_fixture(fx):
    for run, item, rid, sel, act, merge, any_, blocking in mr.EXPECTED["stage_cells"]:
        row = cell(fx, run, item, rid)
        got = (
            row["selection"],
            row["act"],
            row["merge_survival"],
            row["judge_credit"]["any"],
            row["judge_credit"]["blocking"],
        )
        assert got == (sel, act, merge, any_, blocking), (run, item, rid)
    want = mr.EXPECTED["stages"]
    rl = [r for r in fx.rows if r["arm"] == "RL"]
    assert len(rl) == want["rl_rows"]
    assert sum(r["selection"] is True for r in rl) == want["selection"]
    assert sum(r["act"] is True for r in rl) == want["act"]
    checked = [r for r in rl if r["selection"] is not None]
    assert sum(r["merge_survival"] for r in checked) == want["merge_survival_checked"]
    assert (
        sum(r["merge_survival"] for r in rl if r["selection"] is None)
        == want["merge_survival_by_anchor"]
    )


def test_stage_rates_per_class_and_reviewer(fx):
    c4 = fx.metrics["stages"]["RL"]["C4"]
    want = mr.EXPECTED["stage_rates_rl_c4"]
    assert (c4["items"], c4["judge_credit_any"], c4["judge_credit_blocking"]) == (
        want["items"],
        want["judge_credit_any"],
        want["judge_credit_blocking"],
    )
    for rid in ("t2b-1", "t3-1"):
        assert c4["by_reviewer"][rid] == want[rid], rid
    assert (
        fx.metrics["stages"]["Z0"]["C4"]["by_reviewer"]["t2b-1"]["ledger_rows"] == 0
    )  # no ledger in Z0
    assert set(fx.metrics["stages"]) == {"Z0-raw", "Z0", "K", "RL"}


def test_blocking_flag_of_the_item_is_carried(fx):
    assert (
        cell(fx, "stage1-rl-doc-a-r1", "A1", "t2b-1")["blocking_in_implement"] is True
    )
    assert (
        cell(fx, "stage1-rl-doc-a-r1", "A2", "t2b-1")["blocking_in_implement"] is False
    )
