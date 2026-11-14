"""bin/anon.sh (R-29)."""
import json
import os
import re
import shutil

from conftest import BIN, run


def merged(world, extra=""):
    ev, out, sbr = world.eval, world.out, world.sbr
    return f"""review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: {ev}/PKG/candidate.md sha256 abc
reviewers:
- t2b-1: report {out}/runs/row1/PKG/reviews/t2b-1.final.md, block ok true
- t4-1: report relative/path/t4-1.final.md, block ok true
- t3-1: report {sbr}/sb/abcd1234/PKG/x.md, block ok true

#### L1.t4-1 (F1)
- claim: The original wording stays in tests/test_other.py (fact f-3 from sw-1, see {sbr}/board/abcd1234/PKG/msgs/board.jsonl).
- anchor: "the original greeting text"
{{"id":"F1","origin":"peer","anchor":"x"}} {{"origin":"own","id":"F2"}}
Search result to check yourself (not a finding; no conclusion attached). hv-1 panel-msg/1 panel-post
{extra}"""


def anon(world, text, *extra, script=None):
    src = world.tmp / "merged-1.md"
    src.write_text(text)
    d = world.out / "scoring/op1/PKG"
    r = run(["bash", str(script or BIN / "anon.sh"), "--merged", str(src), "--out-dir", str(d), *extra], env=world.env)
    return r, d


def test_strips_and_replaces(world):
    r, d = anon(world, merged(world), "--row", "row-a", "--runid", "abcd1234")
    assert r.returncode == 0, r.stderr
    L = r.stdout.strip()
    assert L in "QRSTUV" and json.loads((d / "label-key.json").read_text()) == {"label": L, "opaque": "op1"}
    t = (d / L / "merged-anon.md").read_text()
    for bad in ("t2b-1", "t4-1", "t3-1", '"origin"', "f-3", "sw-1", "hv-1", "/board/", "panel-msg", "panel-post",
                "Search result to check yourself", "not a finding; no conclusion attached", str(world.eval), str(world.out),
                str(world.sbr), "abcd1234"):
        assert bad not in t, bad
    assert re.search(r"\bR1\b", t) and "R3" in t
    assert t.count("report <redacted>") == 3
    assert "candidate: <candidate file> sha256" in t
    assert "original wording" in t  # "original" is not the origin key


def test_label_not_reused(world):
    labels = {anon(world, merged(world))[0].stdout.strip() for _ in range(6)}
    assert labels == set("QRSTUV")
    r, _ = anon(world, merged(world))
    assert r.returncode == 3


def test_row_name_and_runid_trace_fails(world):
    r, _ = anon(world, merged(world, extra="row-a leaked"), "--row", "row-a")
    assert r.returncode == 4
    r, _ = anon(world, merged(world, extra="id deadbeef leaked"), "--runid", "deadbeef")
    assert r.returncode == 4


def test_origin_key_survives_without_strip(world):
    cp = world.tmp / "copy/bin"
    cp.mkdir(parents=True)
    os.symlink(BIN / "lib", cp / "lib")
    body = (BIN / "anon.sh").read_text()
    body = re.sub(r"# BEGIN strip.*?# END strip\n", "", body, flags=re.S)
    (cp / "anon.sh").write_text(body)
    r, _ = anon(world, merged(world), script=cp / "anon.sh")
    assert r.returncode == 4
    shutil.rmtree(world.tmp / "copy")
