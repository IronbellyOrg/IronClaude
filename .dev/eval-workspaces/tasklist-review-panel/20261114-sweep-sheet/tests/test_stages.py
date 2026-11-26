"""REQ-41: reach logged per stage (extraction, selection, act, merge survival, judge credit), the rubber-stamp measure.
The scenario is built by fixtures/runs/make_runs.py (build_stage_runs) on fixtures/plans/p_basic.md and the synthetic ground
truth; the expected values below were worked out by hand from the line numbers of the plan (a quote on line L covers another
quote when the text matches or the two lines are within 4 lines: 28 GT8, 30 GT2, 34 GT1, 40 GT5, 45 GT4, 54 GT3, 59 GT6, 66 GT7)."""

import json

import pytest

from analysis import analyze
from fixtures.runs import make_runs

STAGES = ("extraction", "selection", "act", "merge_survival", "judge_credit")
GT = json.loads(make_runs.GT_FILE.read_text())["items"]
FLAG = {"T": True, "F": False, "N": None}


def flags(word):
    """'TTFFN' -> (True, True, False, False, None): the five stages in the order of STAGES."""
    return tuple(FLAG[c] for c in word)


@pytest.fixture
def world(tmp_path):
    w = make_runs.build_stage_runs(tmp_path)
    w.loaded = {r.name: r for r in analyze.load_runs(w.runs)}
    w.cand = (w.cand_root / "synth-a" / "candidate.md").read_text()
    return w


def rows_of(loaded, cand, name):
    return {
        r["item"]: tuple(r[s] for s in STAGES)
        for r in analyze.stage_rows(loaded[name], GT, cand)
    }


def test_stage_rows_schema(world):
    rows = analyze.stage_rows(world.loaded["ss-stage-r1"], GT, world.cand)
    assert [r["item"] for r in rows] == [f"GT{n}" for n in range(1, 9)]
    for r, g in zip(rows, GT):
        assert set(r) == {
            "run",
            "arm",
            "doc",
            "item",
            "class",
            "blocking_in_implement",
            *STAGES,
        }
        assert r["run"] == "ss-stage-r1" and r["arm"] == "SS" and r["doc"] == "synth-a"
        assert (r["class"], r["blocking_in_implement"]) == (
            g["class"],
            g["blocking_in_implement"],
        )
        assert all(
            isinstance(r[s], bool) for s in STAGES
        )  # a sheet run has every stage
    plain = analyze.stage_rows(world.loaded["z0-stage-r1"], GT, world.cand)
    # no extractor and no sheet in an arm without a pre-pass: those two stages are null, not false
    assert all(r["extraction"] is None and r["selection"] is None for r in plain)
    assert all(isinstance(r[s], bool) for r in plain for s in STAGES[2:])


def test_stage_values_on_fixture(world):
    # stages in order: extraction, selection, act, merge survival, judge credit
    sheet = {
        "GT1": "TTTTT",  # the item of its quote, a supported PROBLEM row, its finding is merged, credited
        "GT2": "TTTTF",  # reached only through the 3-line rule (GT1's item is 4 lines away)
        "GT3": "TFFFF",  # a candidate that the top-K cut dropped
        "GT4": "FFFFT",  # no candidate at all; the judge still credits a free-review finding
        "GT5": "TTTFF",  # the act is a promoted line that the merge did not keep
        "GT6": "TTTTT",  # the second reviewer's finding is a member of the merged row
        "GT7": "TTFFF",  # selected, but the PROBLEM row has no support: not an act
        "GT8": "FFFFF",  # 6 lines from the nearest item
    }
    got = rows_of(world.loaded, world.cand, "ss-stage-r1")
    assert got == {k: flags(v) for k, v in sheet.items()}
    plain = {
        "GT1": "NNTFF",  # F2 anchors its text, F2 is not in the merge
        "GT2": "NNTFF",  # F2 again, through the 3-line rule
        "GT3": "NNFFF",
        "GT4": "NNFFF",
        "GT5": "NNFFF",
        "GT6": "NNTTT",  # F1 anchors its text and is in the merge
        "GT7": "NNFFF",
        "GT8": "NNFFF",
    }
    got = rows_of(world.loaded, world.cand, "z0-stage-r1")
    assert got == {k: flags(v) for k, v in plain.items()}


def test_missing_inputs_give_null_not_false(world):
    (world.runs / "ss-stage-r1" / "merged" / "ledger.json").unlink()
    loaded = {r.name: r for r in analyze.load_runs(world.runs)}
    got = rows_of(loaded, world.cand, "ss-stage-r1")
    # no merged ledger: survival is unknown, and the stages before it are unaffected
    assert all(v[3] is None for v in got.values())
    assert got["GT1"][:3] == (True, True, True)


def test_covers_rule_literals():
    q = "Every module under `src/exporter/` returns an empty result for an empty report."
    spans = [(33, 34)]
    assert analyze.covers(q, None, q, spans)
    assert analyze.covers("returns an empty result for an empty report", None, q, spans)
    # text of under 12 characters is not a match by containment
    assert not analyze.covers("empty", None, q, spans)
    # the quote is on line 34 (span 33 to 34, half-open). Line 30 (span 29 to 30) is 4 lines away: the rule of
    # FND.same_defect (a start at most 3 beyond the other's end) counts it. Line 29 is 5 lines away and does not count.
    assert analyze.covers("unrelated words here", (29, 30), q, spans)
    assert not analyze.covers("unrelated words here", (28, 29), q, spans)
    assert analyze.covers(
        "unrelated words here", (37, 38), q, spans
    )  # line 38, 4 lines after
    assert not analyze.covers("unrelated words here", (38, 39), q, spans)
    assert not analyze.covers("unrelated words here", None, q, spans)


def test_ok_rate_planted(world):
    runs = list(world.loaded.values())
    gt = {"synth-a": {"text": world.cand, "items": GT}}
    got = analyze.ok_rate_planted(runs, gt, {"synth-a": "planted"})
    # rows on selected items: t2b-1 PROBLEM on S1 S3 S4 S5 and t3-1 OK on S1 S3 S5, PROBLEM on S4 -> 8 rows, 3 OK
    assert (got["rows"], got["ok"], got["ok_rate"]) == (8, 3, 0.375)
    # a row counts for each class of the items it covers: S1 covers GT1 (C1) and GT2 (C2)
    per = {c: (v["rows"], v["ok"], v["ok_rate"]) for c, v in got["per_class"].items()}
    assert per == {
        "C1": (2, 1, 0.5),
        "C2": (2, 1, 0.5),
        "C5": (2, 1, 0.5),
        "C6": (2, 0, 0.0),
        "C7": (2, 1, 0.5),
    }
    # a document that is not in the planted set is not measured
    none = analyze.ok_rate_planted(runs, gt, {})
    assert (none["rows"], none["ok_rate"]) == (0, None)
