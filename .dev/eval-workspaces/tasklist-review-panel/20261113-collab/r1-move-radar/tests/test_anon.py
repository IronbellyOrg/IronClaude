"""T-14: anon.sh removes every arm and reviewer marker before the judge."""

import re

from conftest import A1DIR, PKG, R1, TOOLS, jload, run


def test_anon(root):
    row = "el2-c1-r3"
    d = root / "runs" / row / PKG
    d.mkdir(parents=True)
    (d / "merged-1.md").write_text(
        f"candidate: {A1DIR}/{PKG}/candidate.md sha256 abc\n"
        f"report {root}/runs/{row}/{PKG}/reviews/t2b-1.md, report {R1}/runs/{row}/{PKG}/reviews/t4-1.md\n"
        f"Reviewer t3-1 and t4-1 agree with t2b-1. Sandbox /tmp/evalsb-collab-r1/{PKG}/repo/src/x.py\n"
        '{"lid":"L1","origin":"own","claim":"x"}\n')
    r = run(["bash", str(TOOLS / "anon.sh"), row, PKG, "--root", str(root)])
    assert r.returncode == 0, r.stderr
    out_dir = r.stdout.strip()
    key = jload(d / "label-key.json")
    assert re.fullmatch(r"[0-9a-f]{12}", key["opaque"]) and key["label"] in "QRSTUV"
    assert out_dir == f"{root}/scoring/{key['opaque']}/{PKG}/{key['label']}"
    text = open(f"{out_dir}/merged-anon.md").read()
    assert not re.search(r"\bt[0-9a-z]+-[0-9]+\b", text)
    assert "/tmp/evalsb-collab-r1" not in text and "/tmp/evalsb/" in text
    assert "r1-move-radar" not in text.replace("<EVAL>", "") and "origin" not in text and row not in text
    assert "candidate: <candidate file> sha256" in text and "report <redacted>" in text
    assert "Reviewer R2 and R3 agree with R1" in text  # sorted ids t2b-1 < t3-1 < t4-1 -> R1, R2, R3
    assert not list((root / "scoring").rglob("label-key.json"))
    # a re-run reuses the key
    assert run(["bash", str(TOOLS / "anon.sh"), row, PKG, "--root", str(root)]).stdout.strip() == out_dir
