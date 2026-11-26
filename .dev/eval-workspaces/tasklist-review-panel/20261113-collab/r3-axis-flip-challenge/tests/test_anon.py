from r3lib import metrics

MERGED = """# Merged review 1
candidate: /tmp/evalsb-collab-r3/cand/TASK-WF-x/candidate.md sha256 abc
- t4-1: report /home/x/20261113-collab/r3-axis-flip-challenge/runs/el2-c1-20261113T000000Z-ab12/TASK-WF-x/reviews/t4-1.md
- t2b-1: report runs/el2-c1-x/TASK-WF-x/reviews/t2b-1.p1norm.md
#### L1.t4-1 (P2-F1)
claim text; see {"id":"P2-F1","origin":"peer"} and {"origin":"own","id":"F1"} at /tmp/evalsb-collab-r3/TASK-WF-x/repo/a.py
#### L2.t2b-1 (F1)
"""


def test_redacted():
    out, rep = metrics.anonymise(MERGED)
    assert not rep["residue"], rep
    for bad in (
        "t4-1",
        "t2b-1",
        "P2-F1",
        '"origin"',
        "/tmp/evalsb-collab-r3",
        "p1norm",
        "/runs/",
    ):
        assert bad not in out
    assert "#### L1.R2 (f1)" in out and "#### L2.R1 (f2)" in out


def test_same_findings_same_text():
    # the real merged report carries finding ids only in "#### <lid>.<rid> (<id>)" headings
    a = "\n".join(ln for ln in MERGED.splitlines() if not ln.startswith("claim text"))
    b = (
        a.replace("P2-F1", "F7")
        .replace('"origin":"peer"', '"origin":"own"')
        .replace("el2-c1-20261113T000000Z-ab12", "el2-c0-20261114T000000Z-cd34")
    )
    assert metrics.anonymise(a)[0] == metrics.anonymise(b)[0]


def test_residue_detected():
    _, rep = metrics.anonymise(MERGED + "\nsee board/t4-1.digest.jsonl\n")
    assert rep["residue"]
