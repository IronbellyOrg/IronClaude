"""T-16: results.py row values, null sums for an invalid package, duplicate refusal."""

import json

from conftest import TOOLS, jload, run

DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
GT = {DS: [("GT1", True), ("GT2", True), ("GT3", False)], AL: [("GT1", True), ("GT2", False)], DE: [("GT1", False), ("GT2", False)]}
SCORE = {DS: (["GT1", "GT2", "GT3"], ["GT1", "GT3"], 1), AL: (["GT1"], ["GT1", "GT2"], 2), DE: (["GT2"], [], 1)}


def build(root, tmp_path, row, bad=None):
    a1 = tmp_path / "a1"
    for p, items in GT.items():
        (a1 / p).mkdir(parents=True, exist_ok=True)
        (a1 / p / "ground-truth.json").write_text(json.dumps({"items": [{"id": i, "blocking_in_implement": b} for i, b in items]}))
        d = root / "runs" / row / p
        (d / "reviews").mkdir(parents=True)
        (d / "status").write_text("invalid\n" if p == bad else "ok\n")
        (d / "label-key.json").write_text(json.dumps({"opaque": f"op{p[-6:]}", "label": "S"}))
        (d / "collab.json").write_text(json.dumps({"elapsed_s": 120.0, "baseline_elapsed_s": 116, "ledger_rows": 4, "slots": [], "reviewers": {}}))
        (d / "run.json").write_text(json.dumps({"k": {"searcher": 2, "reader": 2}, "values": "planning"}))
        for rid in ("t2b-1", "t4-1", "t3-1"):
            (d / "reviews" / f"{rid}.cost.json").write_text(json.dumps({"total_output_tokens_all": 1000}))
        s = root / "scoring" / f"op{p[-6:]}" / p / "S"
        s.mkdir(parents=True)
        a, b, w = SCORE[p]
        (s / "score.json").write_text(json.dumps({"gt_covered_any": a, "gt_covered_blocking": b, "wrong_blockers": w}))
    return a1


def results(root, a1, row):
    return run(["uv", "run", "python", str(TOOLS / "results.py"), row, "--root", str(root), "--a1", str(a1)])


def test_row_values(root, tmp_path):
    a1 = build(root, tmp_path, "el2-c1-r3")
    r = results(root, a1, "el2-c1-r3")
    assert r.returncode == 0, r.stderr
    x = jload(root / "results" / "el2-c1-r3.json")
    assert (x["found_14"], x["real_blocking_8"], x["judge_blocking"], x["wrong_blockers"]) == (4, 2, 4, 3)
    assert (x["control_found_2"], x["control_wrong_blockers"]) == (1, 1)
    assert x["output_tokens"] == 9000 and x["status"] == "complete" and x["panel"] == "el2" and x["collab"] == 1 and x["rep"] == 3
    assert x["packages"][DS]["real_blocking"] == ["GT1"]  # GT3 is judge-blocking but not blocking_in_implement
    assert results(root, a1, "el2-c1-r3").returncode == 2  # duplicate row id refused
    assert len((root / "results" / "results.jsonl").read_text().splitlines()) == 1


def test_invalid_package_gives_null_sums(root, tmp_path):
    a1 = build(root, tmp_path, "sl2-c0-r1", bad=AL)
    assert results(root, a1, "sl2-c0-r1").returncode == 0
    x = jload(root / "results" / "sl2-c0-r1.json")
    assert x["status"] == "incomplete" and x["found_14"] is None and x["output_tokens"] is None
    assert x["control_found_2"] == 1  # DE alone is still ok
