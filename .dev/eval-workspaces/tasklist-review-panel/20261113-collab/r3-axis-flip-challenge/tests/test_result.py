import json

from conftest import ALIAS, CONTROL, DESIGNSPEC, EVAL

from r3lib import metrics

GTS = {
    p: json.loads((EVAL / p / "ground-truth.json").read_text())
    for p in (DESIGNSPEC, ALIAS, CONTROL)
}


def S(anyc, blk, wrong=0):
    return {"gt_covered_any": anyc, "gt_covered_blocking": blk, "wrong_blockers": wrong}


def test_fields():
    real = {
        p: {it["id"] for it in GTS[p]["items"] if it.get("blocking_in_implement")}
        for p in GTS
    }
    ds_blk = (
        sorted(real[DESIGNSPEC])[:2] + ["GT10"]
        if "GT10" not in real[DESIGNSPEC]
        else sorted(real[DESIGNSPEC])[:2]
    )
    scores = {
        DESIGNSPEC: S(["GT1", "GT2", "GT3", "GT10"], ds_blk, 2),
        ALIAS: S(["GT4"], ["GT4"], 1),
        CONTROL: S(["GT1"], [], 3),
    }
    out = metrics.score_fields(scores, GTS)
    exp_real = len(set(ds_blk) & real[DESIGNSPEC]) + len({"GT4"} & real[ALIAS])
    assert (
        out["found14"] == 5
        and out["judge_blocking"] == len(ds_blk) + 1
        and out["real_blocking8"] == exp_real
    )
    assert (
        out["wrong_blockers"] == 3
        and out["control_found2"] == 1
        and out["control_wrong_blockers"] == 3
    )
    assert sum(len(real[p]) for p in (DESIGNSPEC, ALIAS)) == 8


def test_reach():
    assert metrics.score_fields({CONTROL: S(["GT1"], [])}, GTS)["reach"] is True
    assert metrics.score_fields({DESIGNSPEC: S(["GT3"], [])}, GTS)["reach"] is False


def test_gt_text_leak():
    q = next(
        it["plan_quote"]
        for it in GTS[CONTROL]["items"]
        if len(it.get("plan_quote") or "") >= 12
    )
    clean = json.dumps({"v": "panel-msg/1", "from": "a", "anchor": q})
    leaky = json.dumps({"v": "panel-msg/1", "from": "a", "move": q[:20], "anchor": "x"})
    leak, overlap = metrics.gt_leak_counts([clean, leaky], {CONTROL: GTS[CONTROL]})
    assert leak == 1 and overlap == 1
