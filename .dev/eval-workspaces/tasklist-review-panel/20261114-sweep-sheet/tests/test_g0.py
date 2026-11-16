"""REQ-22, REQ-35, DESIGN 14.1: the offline selection-recall gate G0 and its leave-one-class-out ablation.
Only fixtures/gt/synthetic-gt.json and fixtures/plans/p_basic.md are used. Lines of p_basic that matter (a quote on line L
covers another quote when the texts match or the lines are within 4: GT8 28, GT2 30, GT1 34, GT5 40, GT4 45, GT3 54,
GT6 59, GT7 66)."""

import json
import subprocess
import sys

import pytest
from helpers import SW

from analysis import g0
from fixtures.repos.build_repo import build_repo

PLAN = SW / "fixtures" / "plans" / "p_basic.md"
SOURCE = SW / "fixtures" / "plans" / "source.md"
GT_FILE = SW / "fixtures" / "gt" / "synthetic-gt.json"
GT = json.loads(GT_FILE.read_text())["items"]
TEXT = PLAN.read_text()
QUOTE = {g["id"]: g["plan_quote"] for g in GT}


def at(line, text="unrelated words here"):
    return {"anchor_text": text, "location": {"line_start": line, "line_end": line}}


@pytest.fixture
def doc(tmp_path):
    repo = build_repo(tmp_path).repo
    return g0.load_doc("p_basic", PLAN, SOURCE, repo, GT_FILE)


def test_recall_definitions():
    # three candidates: the quote of GT1 (line 34: covers GT1, and GT2 four lines above), "Source sections: 2.2" (line 42:
    # GT5 two lines above, GT4 three below), the quote of GT3 (line 54)
    candidates = [
        at(34, QUOTE["GT1"]),
        at(42, "Source sections: 2.2"),
        at(54, QUOTE["GT3"]),
    ]
    items = [candidates[0], candidates[2]]  # the selection keeps the first and the last
    ext = g0.recall(GT, candidates, TEXT)
    sel = g0.recall(GT, items, TEXT)
    assert (
        ext["covered"] == ["GT1", "GT2", "GT3", "GT4", "GT5"] and ext["recall"] == 5 / 8
    )
    assert sel["covered"] == ["GT1", "GT2", "GT3"] and sel["recall"] == 3 / 8
    per = lambda r: {c: t["recall"] for c, t in r["per_class"].items()}  # noqa: E731
    assert per(ext) == {
        "C1": 1,
        "C2": 1,
        "C3": 1,
        "C4": 1,
        "C5": 1,
        "C6": 0,
        "C7": 0,
        "C8": 0,
    }
    assert per(sel) == {
        "C1": 1,
        "C2": 1,
        "C3": 1,
        "C4": 0,
        "C5": 0,
        "C6": 0,
        "C7": 0,
        "C8": 0,
    }
    assert sel["per_class"]["C3"] == {"covered": 1, "total": 1, "recall": 1.0}
    assert g0.recall(GT, [], TEXT)["recall"] == 0.0
    with pytest.raises(g0.G0Error, match="no ground-truth"):
        g0.recall([], items, TEXT)
    # pooled over two documents: 3 of 8 and 5 of 8 items give 8 of 16
    pooled, per_class = g0._pooled(
        [(GT, {"GT1", "GT2", "GT3"}), (GT, {"GT1", "GT2", "GT3", "GT4", "GT5"})]
    )
    assert pooled == 0.5 and per_class["C1"] == {
        "covered": 2,
        "total": 2,
        "recall": 1.0,
    }
    assert per_class["C4"] == {"covered": 1, "total": 2, "recall": 0.5}


def test_covers_by_span_within_3():
    gt1 = GT[0]  # the quote of GT1 is on line 34
    assert g0.covers(at(34, QUOTE["GT1"]), gt1, TEXT)  # the text matches
    assert g0.covers(
        at(30), gt1, TEXT
    )  # 4 lines above: within 3 lines in the rule of FND.same_defect
    assert not g0.covers(at(29), gt1, TEXT)  # 5 lines above
    assert g0.covers(at(38), gt1, TEXT) and not g0.covers(
        at(39), gt1, TEXT
    )  # and below
    # a text contained in the quote counts at 12 characters or more; a short one does not
    assert g0.covers(at(81, "returns an empty result for an empty report"), gt1, TEXT)
    assert not g0.covers(at(81, "empty report"[:5]), gt1, TEXT)
    # a quote that is not in the plan has no span: only the text can match
    assert not g0.covers(
        at(34),
        {"id": "X", "class": "C1", "plan_quote": "a sentence that the plan lacks"},
        TEXT,
    )


def test_random_baseline_deterministic(doc):
    view = g0.prepass_view(doc, 1)
    assert len(view["candidates"]) == 12  # the plan has 12 candidates in all
    a = g0.baseline_a([doc], [view], draws=200, seed=5, cap=3)
    assert a == g0.baseline_a([doc], [view], draws=200, seed=5, cap=3)
    assert a != g0.baseline_a([doc], [view], draws=200, seed=6, cap=3)
    assert len(a) == 200 and all(
        x * 8 == int(x * 8) and 0 <= x <= 1 for x in a
    )  # steps of 1/8: 8 items
    b = g0.baseline_b([doc], [view], draws=200, seed=5, cap=3)
    assert b == g0.baseline_b([doc], [view], draws=200, seed=5, cap=3)
    # a pick of 12 from 12 candidates is all of them: every draw equals the extraction recall (1.0 on this plan)
    assert set(g0.baseline_a([doc], [view], draws=20, seed=1, cap=12)) == {1.0}
    assert set(g0.baseline_b([doc], [view], draws=20, seed=1, cap=12)) == {1.0}


def test_beats_needs_a_margin_and_a_small_tail():
    draws = [0.1] * 95 + [0.95] * 5  # 5% of the draws are at or above 0.9
    assert g0.beats(0.9, draws)
    assert not g0.beats(0.9, [0.1] * 80 + [0.95] * 20)  # 20% reach it
    assert not g0.beats(0.5, [0.5] * 100)  # equal to the mean is not above it
    assert not g0.beats(0.05, draws)  # below the mean


def test_gate_pass_and_fail(doc):
    kw = {"seeds": [1, 2, 3], "cap": 3, "draws": 300, "role": "decision"}
    ok = g0.evaluate([doc], floor=0.4, **kw)
    bad = g0.evaluate([doc], floor=0.99, **kw)
    # the same data: a sheet of 3 items reaches 4 of the 8 ground-truth items on every seed, the candidates reach all 8
    assert (
        ok["selection"]["recall_by_seed"] == {1: 0.5, 2: 0.5, 3: 0.5}
        and ok["extraction"]["recall"] == 1.0
    )
    assert (ok["pass"]["floor"], ok["pass"]["gate"]) == (True, True)
    assert (bad["pass"]["floor"], bad["pass"]["gate"]) == (False, False)
    assert (
        ok["selection"] == bad["selection"] and ok["baseline_a"] == bad["baseline_a"]
    )  # only the floor differs
    # the derivation part is the random baseline: with 12 candidates a random pick of 3 is as good as the rank here
    der = g0.evaluate([doc], floor=None, **{**kw, "role": "derivation"})
    assert der["baseline_a"]["beats_random"] is False and der["pass"]["gate"] is False
    # both parts: the floor can be met and the gate still fail on the baseline
    both = g0.evaluate([doc], floor=0.4, **{**kw, "role": "both"})
    assert (
        both["pass"]["floor"],
        both["pass"]["beats_random"],
        both["pass"]["gate"],
    ) == (True, False, False)
    # no floor, a decision role: no verdict, not a pass
    assert g0.evaluate([doc], floor=None, **kw)["pass"]["gate"] is None
    with pytest.raises(g0.G0Error, match="role"):
        g0.evaluate([doc], role="nonsense")


def test_ablation_report_synthetic(doc):
    ab = g0.ablate([doc], seeds=[1, 2, 3])
    # the full sheet holds all 12 candidates: removing a class changes no other class's recall
    assert sorted(ab["removed"]) == [f"C{n}" for n in range(1, 9)]
    for cls, changes in ab["removed"].items():
        assert sorted(changes) == sorted(
            c for c in ab["removed"] if c != cls
        )  # every other class is named
        assert all(abs(x) <= 0.15 for x in changes.values())
    assert (
        ab["limit"] == 0.15
        and ab["within_limit"] is True
        and ab["largest_change"] == 0.0
    )
    text = g0.render(ab)
    assert (
        all(f"without C{n}:" in text for n in range(1, 9))
        and "within the limit" in text
    )
    # a sheet of 3 slots: dropping C8 frees a slot that moves C3 up and takes C2 down by a whole item each
    tight = g0.ablate([doc], seeds=[1, 2, 3], cap=3)
    assert tight["removed"]["C8"]["C2"] == -1.0 and tight["removed"]["C8"]["C3"] == 1.0
    assert (
        tight["within_limit"] is False
        and tight["largest_change"] == 1.0
        and "OVER the limit" in g0.render(tight)
    )


def manifest(tmp_path, doc):
    p = tmp_path / "manifest.json"
    entry = {
        "candidate": str(PLAN),
        "source": str(SOURCE),
        "repo": str(doc["repo"]),
        "gt": str(GT_FILE),
        "set": "holdout",
    }
    p.write_text(json.dumps({"docs": {"p_basic": entry}}))
    return p


def test_command_line(doc, tmp_path, capsys):
    m = manifest(tmp_path, doc)
    base = [
        "--manifest",
        str(m),
        "--docs",
        "holdout",
        "--seeds",
        "1,2",
        "--cap",
        "3",
        "--draws",
        "100",
    ]
    out = tmp_path / "out" / "g0.json"
    assert (
        g0.main([*base, "--floor", "0.4", "--out", str(out)]) == 0
    )  # holdout: the floor decides
    assert (
        json.loads(out.read_text())["pass"]["gate"] is True
        and "PASS" in capsys.readouterr().out
    )
    assert (
        g0.main([*base, "--floor", "0.99"]) == 1 and "FAIL" in capsys.readouterr().out
    )
    # the floor comes from a pre-registration file, and there is no default floor
    prereg = tmp_path / "prereg.json"
    prereg.write_text(json.dumps({"selection_recall_floor": 0.4}))
    assert g0.main([*base, "--floor-from", str(prereg)]) == 0
    capsys.readouterr()
    assert g0.main(base) == 2 and "no floor" in capsys.readouterr().err
    assert g0.main([*base, "--floor-from", str(tmp_path / "missing.json")]) == 2
    # derivation: the baseline decides and no floor is needed (here it is not met: 12 candidates, a sheet of 3)
    assert (
        g0.main(
            [
                "--manifest",
                str(m),
                "--docs",
                "p_basic",
                "--role",
                "derivation",
                "--cap",
                "3",
                "--draws",
                "100",
            ]
        )
        == 1
    )
    # the ablation
    assert g0.main(["--manifest", str(m), "--docs", "holdout", "--ablate"]) == 0
    assert "within the limit" in capsys.readouterr().out
    assert (
        g0.main(["--manifest", str(m), "--docs", "holdout", "--ablate", "--cap", "3"])
        == 1
    )
    assert g0.main(["--manifest", str(m), "--docs", "nope", "--floor", "0.4"]) == 2
    assert (
        g0.main([*base, "--floor", "0.4", "--out", "/var/tmp/sw-g0-refused.json"]) == 2
    )


def test_help_and_no_ground_truth_path_in_the_script():
    r = subprocess.run(
        [sys.executable, "-I", "-B", str(SW / "analysis" / "g0.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0 and "--ablate" in r.stdout and "--floor-from" in r.stdout
    src = (SW / "analysis" / "g0.py").read_text()
    # the file never builds a ground-truth path of its own: the only paths are the ones that the command line gives
    assert (
        "ground-truth*.json" not in src
        and ".dev/eval-workspaces" not in src
        and "20261111" not in src
    )
