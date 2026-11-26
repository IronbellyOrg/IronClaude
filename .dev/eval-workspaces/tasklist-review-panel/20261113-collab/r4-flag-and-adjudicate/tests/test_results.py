"""lib/results.py with fixture scores and fixture ground truth (design 5.2)."""

import json

from r4help import AL, DE, DS, PKGS

import results

GT = {
    DS: [{"id": "GT1", "blocking_in_implement": True, "plan_quote": "the alpha beta gamma delta sentence"},
         {"id": "GT2", "blocking_in_implement": False, "plan_quote": "q2"},
         {"id": "GT3", "blocking_in_implement": True, "plan_quote": "q3"}],
    AL: [{"id": "GT1", "blocking_in_implement": True, "plan_quote": "q4"}, {"id": "GT2", "blocking_in_implement": False, "plan_quote": "q5"}],
    DE: [{"id": "GT1", "blocking_in_implement": False, "plan_quote": "q6"}, {"id": "GT2", "blocking_in_implement": False, "plan_quote": "q7"}],
}
SCORES = {
    DS: {"gt_covered_any": ["GT1", "GT2", "GT3"], "gt_covered_blocking": ["GT1", "GT2"], "wrong_blockers": 2, "ledger_rows_total": 9, "ledger_rows_blocking": 4},
    AL: {"gt_covered_any": ["GT1"], "gt_covered_blocking": ["GT1"], "wrong_blockers": 1, "ledger_rows_total": 5, "ledger_rows_blocking": 2},
    DE: {"gt_covered_any": ["GT2"], "gt_covered_blocking": [], "wrong_blockers": 3, "ledger_rows_total": 4, "ledger_rows_blocking": 3},
}


def make_row(tmp_path, failed=None):
    ev = tmp_path / "eval"
    row = tmp_path / "runs" / "r1"
    for p in PKGS:
        (ev / p).mkdir(parents=True)
        (ev / p / "ground-truth.json").write_text(json.dumps({"items": GT[p]}))
        pd = row / p
        (pd / "scoring").mkdir(parents=True)
        (pd / "reviews").mkdir()
        (pd / "panel.json").write_text(json.dumps({"flagger": "t2b-1", "reviewers": [{"rid": r} for r in ("t2b-1", "t4-1", "t3-1")]}))
        for r in ("t2b-1", "t4-1", "t3-1"):
            (pd / "reviews" / f"{r}.meta.json").write_text(json.dumps({"output_tokens_all": 10, "dropped_lines": 0, "reask": False}))
        (pd / "status").write_text("judge_failed\n" if p == failed else "ok\n")
        if p != failed:
            (pd / "scoring" / "score.json").write_text(json.dumps(SCORES[p]))
        slots = []
        if p == DS:
            slots = [{"id": "c0", "recipient": "t4-1", "card_form": "challenge", "status": "delivered", "converted": True,
                      "converted_fids": ["F3"], "passed_line": False, "card_task": "T2"}]
            (pd / "ledger.json").write_text(json.dumps({"rows": [{"lid": "L1", "anchor": "x the alpha beta gamma delta sentence y",
                                                                  "members": [{"reviewer_id": "t4-1", "fid": "F3"}]}]}))
        (pd / "collab.json").write_text(json.dumps({"elapsed_s": 100.0, "overhead_pct": 5.0, "slots": slots, "cards_sent": len(slots),
                                                    "cards_delivered": len(slots), "reviewers": {}}))
    (row / "run.json").write_text(json.dumps({"row": "r1", "panel": "EL2", "arm": "F7"}))
    return ev, row


def test_totals(tmp_path, monkeypatch):
    ev, row = make_row(tmp_path)
    monkeypatch.setattr(results, "EVAL", str(ev))
    out = results.build(str(row))
    assert out["valid"] is True
    assert out["found_14"] == 4 and out["real_blocking_8"] == 2 and out["judge_blocking"] == 3
    assert out["wrong_blockers"] == 3 and out["control_found_2"] == 1 and out["control_wrong_blockers"] == 3
    assert out["output_tokens"] == 90
    c = out["collab"][DS]["conversions"]["challenge"]
    assert c == {"delivered": 1, "converted": 1, "credited": 1, "uncredited": 0}
    assert out["reach"] is True and "DS:GT1" in out["reach_ids"]
    assert out["collab"][DS]["early_tasks_only"] is True


def test_failed_package_nulls_totals(tmp_path, monkeypatch):
    ev, row = make_row(tmp_path, failed=AL)
    monkeypatch.setattr(results, "EVAL", str(ev))
    out = results.build(str(row))
    assert out["valid"] is False
    for k in ("found_14", "real_blocking_8", "judge_blocking", "wrong_blockers", "control_found_2", "control_wrong_blockers"):
        assert out[k] is None
    assert out["packages"][AL]["status"] == "judge_failed"
