"""frozen/ against ground truth (R-07) and the pins file (R-02, R-30). Reads ground truth; touches no reviewer path."""

import json

import audit
from r4help import EVAL, PKGS, R4, run


def test_harness_text_has_no_gt_overlap():
    texts = audit.harness_texts(str(R4 / "frozen"))
    a1 = {"brief-a1.txt": (R4 / "frozen" / "brief-a1.txt").read_text()}
    hits, a1_hits = [], []
    for p in PKGS:
        gt = json.load(open(EVAL / p / "ground-truth.json"))["items"]
        hits += audit.gt_overlap(texts, gt)
        a1_hits += audit.gt_overlap(a1, gt)
    print("brief-a1.txt overlap (reported, not asserted):", a1_hits)
    assert hits == []


def test_pins_check_out():
    r = run(["sha256sum", "-c", "pins.sha256"], cwd=R4 / "frozen")
    assert r.returncode == 0, r.stdout + r.stderr
    pinned = r.stdout
    for f in ("judge-one.sh", "findings.py", "ledger.py", "merged-requirements.md", "values.py", "results.py", "arm_summary.py"):
        assert f in pinned
