"""py/results_row.py (DESIGN 5.4) from fixture score.json files and fixture ground truth."""
import json

from conftest import CONTROL, PKGS, pyrun

RICH = [p for p in PKGS if p != CONTROL]


def tree(world, scores, api_error_pkg=None):
    rd = world.out / "runs/row1"
    rd.mkdir(parents=True)
    for f, v in {"panel": "EL2", "panel_collab": "1", "sweeper_model": "muse-ember-1.0", "started_at": "t", "finished_at": "u"}.items():
        (rd / f).write_text(v + "\n")
    for p in PKGS:
        pd = rd / p
        (pd / "reviews").mkdir(parents=True)
        (pd / "sweeper").mkdir()
        (pd / "t0").write_text("1000")
        (pd / "DONE").write_text("x")
        (pd / "merged-1.md").write_text("m")
        (pd / "audit.json").write_text(json.dumps({"ok": True}))
        (pd / "collab.json").write_text(json.dumps({"k": 2, "elapsed_s": 100.0, "overhead_pct": 0, "values_sha256": "v",
                                                    "ledger_rows": 3, "reviewers": {}, "sweeper": {"facts_posted": 1, "start_t": 2000},
                                                    "isolated_for": [], "echo_rate": None, "own_line_jaccard": None, "slo_breach": False}))
        (pd / "reviews/t4-1.cost.json").write_text(json.dumps({"total_output_tokens_all": 110, "reask_output_tokens": 10}))
        (pd / "sweeper/sw-1.meta.json").write_text(json.dumps({"output_tokens": 7}))
        if p in scores:
            d = world.out / "scoring/op1" / p
            (d / "Q").mkdir(parents=True)
            (d / "label-key.json").write_text(json.dumps({"label": "Q", "opaque": "op1"}))
            (d / "Q/score.json").write_text(json.dumps(scores[p]))
            res = "API Error: 500" if p == api_error_pkg else "score.json written"
            (d / "Q/judge.json").write_text(json.dumps([{"type": "result", "result": res}]))


def sc(any_, blk, wrong):
    return {"gt_covered_any": any_, "gt_covered_blocking": blk, "wrong_blockers": wrong}


def build(world):
    r = pyrun("results_row.py", "--row", "row1", "--opaque", "op1", "--out", str(world.out / "results/row1.json"), env=world.env)
    assert r.returncode == 0, r.stderr
    return json.loads((world.out / "results/row1.json").read_text())


def test_fields(world):
    # GT1 blocking_in_implement true, GT2 false (conftest)
    tree(world, {RICH[0]: sc(["GT1", "GT2"], ["GT1", "GT2"], 1), RICH[1]: sc(["GT1"], ["GT2"], 2), CONTROL: sc(["GT1"], [], 3)})
    row = build(world)
    assert row["found_14"] == 3 and row["judge_blocking"] == 3 and row["real_blocking_8"] == 1
    assert row["wrong_blockers"] == 3 and row["control_found_2"] == 1 and row["control_wrong_blockers"] == 3
    assert row["output_tokens"] == {"total": 3 * 117, "reviewers": 300, "sweeper": 21, "reask": 30}
    assert row["arm"] == "F4" and row["invalid"] == [] and row["collab"]["sweeper_start_t_s"][CONTROL] == 1.0


def test_missing_score_is_null(world):
    tree(world, {RICH[0]: sc(["GT1"], [], 0), CONTROL: sc([], [], 0)})
    row = build(world)
    assert row["found_14"] is None and row["real_blocking_8"] is None and row["wrong_blockers"] is None
    assert any("unscored" in x for x in row["invalid"])


def test_api_error(world):
    tree(world, {p: sc(["GT1"], [], 0) for p in PKGS}, api_error_pkg=CONTROL)
    row = build(world)
    assert row["per_package"][CONTROL]["judge_api_error"] and row["control_found_2"] is None
    assert any("API Error" in x for x in row["invalid"])
