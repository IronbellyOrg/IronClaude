"""joint_report.py on invented data: lever rule, as-run against rerun-substituted, control pooling. No real ground truth is read."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DOCS = {"D1": 10, "D2": 10}


def make(tmp, found_b, found_a, killed_original=False):
    gt = tmp / "gt"
    for d, n in DOCS.items():
        (gt / d).mkdir(parents=True)
        items = [{"id": f"GT{i+1}", "blocking_in_implement": i < 3} for i in range(n)]
        (gt / d / "ground-truth.json").write_text(json.dumps({"items": items}))
    sc, runs, inv = tmp / "sc", tmp / "runs", tmp / "inv"
    for p in (sc, runs, inv):
        p.mkdir()
    labels = []
    k = 0

    def add(root, run, doc, found, killed=False):
        nonlocal k
        k += 1
        label = f"j{k:03d}"
        labels.append(f"{label}\t{run}\t{doc}\tfirst")
        (sc / label).mkdir()
        (sc / label / "score.json").write_text(json.dumps({"gt_covered_any": [f"GT{i}" for i in range(found)], "gt_covered_blocking": [],
                                                           "ledger_rows_blocking": 1, "blocking_rows_gt_matched": 0, "wrong_blockers": 1, "ledger_rows_total": 3}))
        (root / run).mkdir()
        (root / run / "run.json").write_text(json.dumps({"reviewers": {"r": {"killed": killed, "status": "ok"}}}))
        (root / run / "timing.json").write_text(json.dumps({"panel_elapsed_s": 100.0}))

    for d in DOCS:
        for r in range(1, 6):
            add(runs, f"stagesp-z0-{d}-r{r}", d, found_b)
            add(runs, f"stagesp-z0-sonnet-{d}-r{r}", d, found_a)
    if killed_original:
        add(inv, "stagesp-z0-sonnet-D1-r1.original-0041", "D1", 0, killed=True)
    (sc / "labels.tsv").write_text("\n".join(labels) + "\n")
    return gt, sc, runs, inv


def run(tmp, gt, sc, runs, inv=None):
    args = [sys.executable, "-I", str(HERE / "joint_report.py"), "--gt", str(gt), "--out", str(tmp / "out"), "--draws", "300",
            "--source", f"stronger={sc}:{runs}" + (f":{inv}" if inv else ""),
            "--arm-rule", "stronger:stagesp-z0-sonnet-=A", "--arm-rule", "stronger:stagesp-z0-=B"]
    r = subprocess.run(args, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.loads((tmp / "out" / "metrics.json").read_text()), (tmp / "out" / "REPORT.md").read_text()


def test_lever_needs_difference_and_lower_bound(tmp_path):
    gt, sc, runs, inv = make(tmp_path, found_b=2, found_a=5)  # +0.30 on both documents
    m, rep = run(tmp_path, gt, sc, runs)
    assert m["stronger_panel"]["A"]["lever"] is True and "LEVER" in rep
    tmp2 = tmp_path / "second"
    tmp2.mkdir()
    gt, sc, runs, inv = make(tmp2, found_b=2, found_a=2)
    m, _ = run(tmp2, gt, sc, runs)
    assert m["stronger_panel"]["A"]["lever"] is False


def test_as_run_uses_the_moved_aside_original_and_substituted_uses_the_rerun(tmp_path):
    gt, sc, runs, inv = make(tmp_path, found_b=2, found_a=5, killed_original=True)
    m, _ = run(tmp_path, gt, sc, runs, inv)
    a_run, a_sub = m["views"]["as_run"]["stronger/A"], m["views"]["rerun_substituted"]["stronger/A"]
    assert a_run["killed_runs"] == 1 and a_sub["killed_runs"] == 0
    assert a_run["found_fraction"] < a_sub["found_fraction"]
