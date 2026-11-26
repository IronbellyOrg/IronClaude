"""lib/normalize.py (design 2.6 step 5; R-02)."""

import json

from r4help import DE, EVAL, R4, REPO, run
from superclaude.cli.review import findings as fd

CAND = (EVAL / DE / "candidate.md").read_text()
FLAT = fd.flat(CAND)


def report(lines):
    return "review: 1 of 3\nbody\n\n## Findings block\n\n```findings-v1\n" + "\n".join(json.dumps(x) for x in lines) + "\n```\nverdict: FAIL\n"


def line(**kw):
    d = {"id": "F1", "severity": "MAJOR", "blocking": True, "category": "other", "anchor": FLAT[100:160], "refs": [], "claim": "c"}
    d.update(kw)
    return d


def norm(tmp_path, text):
    raw, final, parse = tmp_path / "r.md", tmp_path / "f.md", tmp_path / "p.json"
    raw.write_text(text)
    r = run(["uv", "run", "--frozen", "--project", REPO, "python", R4 / "lib" / "normalize.py", raw, final, parse])
    assert r.returncode == 0, r.stderr
    return final.read_text(), json.loads(parse.read_text())


def test_long_anchor_truncated_and_locatable(tmp_path):
    long_anchor = CAND[CAND.index("## Task 1"):][:400]
    assert len(fd.flat(long_anchor)) > 250
    out, p = norm(tmp_path, report([line(anchor=long_anchor), line(id="F2")]))
    res = fd.parse_block(out)
    a = res["findings"][0]["anchor"]
    assert a == fd.flat(long_anchor)[:200] and fd.locate(CAND, a)
    assert p["ok"] is True and p["truncated"] == 1


def test_long_claim_and_unchanged_lines(tmp_path):
    other = json.dumps(line(id="F2"))
    text = report([line(claim="x " * 200)]).replace("```\nverdict", other + "\n```\nverdict")
    out, p = norm(tmp_path, text)
    assert len(fd.parse_block(out)["findings"][0]["claim"]) == 300
    assert other in out.splitlines()  # untouched line byte-identical


def test_anchor_with_line_breaks(tmp_path):
    a = FLAT[200:240].replace(" ", "\n", 2)
    out, p = norm(tmp_path, report([line(anchor=a)]))
    assert p["ok"] is True and p["truncated"] == 0


def test_bad_severity(tmp_path):
    out, p = norm(tmp_path, report([line(severity="HIGH")]))
    assert p["ok"] is False and p["errors"][0]["msg"] == "severity must be CRITICAL, MAJOR or MINOR"


def test_no_block(tmp_path):
    out, p = norm(tmp_path, "review: 1 of 3\nno block\n")
    assert p["ok"] is False


def test_idempotent(tmp_path):
    long_anchor = CAND[CAND.index("## Task 1"):][:400]
    out1, _ = norm(tmp_path, report([line(anchor=long_anchor)]))
    (tmp_path / "again").mkdir()
    out2, p2 = norm(tmp_path / "again", out1)
    assert out1 == out2 and p2["truncated"] == 0
