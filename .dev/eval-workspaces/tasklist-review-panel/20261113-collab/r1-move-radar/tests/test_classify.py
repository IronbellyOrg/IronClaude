"""T-3: radar-classify.jq signatures, negatives and the never-unobservable property."""

import json

import pytest
from conftest import FIX, PKG, TOOLS, run

SB = "/tmp/sbX"
REPO = f"{SB}/{PKG}/repo"
SRC = f"{SB}/cand/{PKG}/source.md"


def classify(records):
    lines = "\n".join(json.dumps(r) for r in records) + "\n"
    r = run(["jq", "-R", "-c", "--slurpfile", "ix", str(FIX / "index.json"), "--arg", "srcpath", SRC,
             "-f", str(TOOLS / "radar-classify.jq")], stdin=lines)
    assert r.returncode == 0, r.stderr
    return [json.loads(x)["sig"] for x in r.stdout.splitlines()]


def bash(cmd):
    return {"n": 1, "t": 0, "rid": "x", "sub": False, "tool": "Bash", "input": {"command": cmd}}


def tool(name, **inp):
    return {"n": 1, "t": 0, "rid": "x", "sub": False, "tool": name, "input": inp}


POS = [
    ("M1", bash("grep -rn merge_guard tests/")),
    ("M1", tool("Grep", pattern="merge_guard", path=f"{REPO}/tests")),
    ("M2", bash("grep -l x src/")),
    ("M2", bash("ls docs | wc -l")),
    ("M2", tool("Grep", pattern="x", path="src", output_mode="count")),
    ("M4", bash('grep -n "HOW-WE-WORK" docs/guide.md')),
    ("M4", bash("grep -n HOW-WE-WORK docs/guide.md")),
    ("M7", bash("grep -rn 43 .")),
    ("M7", tool("Grep", pattern="43")),
    ("M7", bash("grep 43 CHANGELOG.md")),
    ("SRC_OPENED", tool("Read", file_path=SRC)),
    ("SRC_OPENED", bash(f"sed -n 1,80p {SRC}")),
    ("UNNAMED_TEST", tool("Read", file_path=f"{REPO}/tests/x/test_y.py")),
]
NEG = [
    ("M1", bash("grep -rn merge_guard src/")),
    ("M1", bash("grep -rn unrelated_word tests/")),
    ("UNNAMED_TEST", tool("Read", file_path=f"{REPO}/tests/app/test_core.py")),
    ("M4", bash('grep -n "HOW-WE-WOR" docs/guide.md')),
    ("M2", bash("grep -rn x src/ | head -c 500")),
    ("M2", bash("grep -n x f; ls -la")),
    ("M2", bash("grep -n x f && sort -c f")),
]


@pytest.mark.parametrize("sig,rec", POS, ids=[f"{s}-{i}" for i, (s, _) in enumerate(POS)])
def test_positive(sig, rec):
    assert sig in classify([rec])[0]


@pytest.mark.parametrize("sig,rec", NEG, ids=[f"not-{s}-{i}" for i, (s, _) in enumerate(NEG)])
def test_negative(sig, rec):
    assert sig not in classify([rec])[0]


def test_sub_records_never_counted():
    rec = dict(bash("grep -rn merge_guard tests/"), sub=True)
    assert classify([rec]) == [[]]


def test_corrupt_line_skipped():
    r = run(["jq", "-R", "-c", "--slurpfile", "ix", str(FIX / "index.json"), "--arg", "srcpath", SRC,
             "-f", str(TOOLS / "radar-classify.jq")], stdin='{"n":1,"tool":"Ba\n' + json.dumps(bash("grep -l x src/")) + "\n")
    assert r.returncode == 0 and [json.loads(x)["sig"] for x in r.stdout.splitlines()] == [["M2"]]


def test_never_emits_unobservable_moves():
    out = classify([r for _, r in POS + NEG])
    assert all(s not in {"M3", "M5", "M6", "M8", "M9", "M10"} for sigs in out for s in sigs)
