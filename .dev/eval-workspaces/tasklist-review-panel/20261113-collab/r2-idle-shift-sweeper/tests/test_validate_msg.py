"""lib/validate-msg.sh (R-06, R-08, D-4): DESIGN 6.1 cases."""
import json
import time

import pytest
from conftest import BIN, CAND_A, run

V = str(BIN / "lib/validate-msg.sh")


def fact(**kw):
    f = {"v": "panel-msg/1", "id": "f-0", "run": "run1/pkg", "from": "sw-1", "to": "*", "t": int(time.time() * 1000),
         "kind": "fact", "move": "M1", "anchor": CAND_A, "items": ["tests/test_other.py"], "cmd": "grep -rln greeting tests/"}
    f.update(kw)
    return {k: v for k, v in f.items() if v is not None}


def check(world, f):
    line = f if isinstance(f, str) else json.dumps(f)
    r = run(["bash", V, "--board", str(world.B), "--line", line])
    return r.returncode, r.stdout.strip()


@pytest.fixture
def w(world):
    world.board(k=2)
    return world


def test_accept_m1(w):
    assert check(w, fact()) == (0, "ok")


def test_accept_m2_count_zero(w):
    assert check(w, fact(move="M2", n=0, cmd="grep -rlc greeting docs")) == (0, "ok")


def test_accept_witness_source_line(w):
    assert check(w, fact(move="M9", items=["source.md:2"], anchor=None)) == (0, "ok")


def test_too_long(w):
    f = fact()
    f["run"] = "x" * 600
    assert len(json.dumps(f, separators=(",", ":"))) > 600
    assert check(w, json.dumps(f, separators=(",", ":"))) == (1, "reject too_long")


@pytest.mark.parametrize("key,reason", [("claim", "forbidden_key:claim"), ("severity", "forbidden_key:severity"),
                                        ("category", "forbidden_key:category"), ("foo", "unknown_key:foo")])
def test_keys(w, key, reason):
    assert check(w, fact(**{key: "x"})) == (1, f"reject {reason}")


def test_bad_json(w):
    assert check(w, "{not json") == (1, "reject bad_json")


def test_kind_card(w):
    assert check(w, fact(kind="card")) == (1, "reject bad_kind")


def test_move_m3(w):
    assert check(w, fact(move="M3")) == (1, "reject bad_move")


def test_anchor_11_chars(w):
    assert check(w, fact(anchor=CAND_A[:11])) == (1, "reject bad_anchor")


def test_anchor_not_in_candidate(w):
    assert check(w, fact(anchor="this sentence is not in the plan")) == (1, "reject anchor_not_in_candidate")


def test_anchor_whitespace_flattened_accepted(w):
    assert check(w, fact(anchor="so that   every\n greeting uses the new wording")) == (0, "ok")


def test_nine_items(w):
    assert check(w, fact(items=["tests/test_other.py"] * 9)) == (1, "reject too_many_items")


@pytest.mark.parametrize("item,reason", [("/etc/passwd", "bad_item:/etc/passwd"), ("../x", "bad_item:../x"),
                                         ("tests/missing.py", "item_missing:tests/missing.py"),
                                         ("tests/test_other.py:9999", "item_missing:tests/test_other.py:9999")])
def test_items(w, item, reason):
    assert check(w, fact(items=[item])) == (1, f"reject {reason}")


def test_second_witness(w):
    assert w.post("--move", "M9", "--cmd", "grep -n greeting " + w.conf["source"], "--item", "source.md:2").stdout.startswith("posted")
    assert check(w, fact(move="M6", items=["source.md:3"], anchor=None)) == (1, "reject second_witness")


def test_n_negative(w):
    assert check(w, fact(n=-1)) == (1, "reject bad_n")


@pytest.mark.parametrize("cmd", ["rm -rf tests", "sed -i s/a/b/ x", "find . -delete", "grep x > f", "grep x; ls",
                                 "grep $(id) .", "grep x . # note", "grep x & ls", "grep `id` .", "grep x | xargs rm",
                                 "find . -exec cat {} +", "cat /etc/passwd", "grep x /etc/passwd", ""])
def test_bad_cmd(w, cmd):
    assert check(w, fact(cmd=cmd)) == (1, "reject bad_cmd")


def test_cmd_required(w):
    f = fact()
    del f["cmd"]
    assert check(w, f) == (1, "reject bad_cmd")


def test_cmd_allowed_forms(w):
    for c in ["git grep -n greeting", "git ls-files tests", "grep -rn x tests/ | wc -l", "ls tests",
              "grep -n greeting " + w.conf["cand_dir"] + "/candidate.md"]:
        assert check(w, fact(cmd=c)) == (0, "ok"), c


def test_over_cap(world):
    world.board(k=1)  # cap 2k = 2
    for _ in range(2):
        assert world.post("--move", "M1", "--cmd", "grep -rln greeting tests/", "--item", "tests/test_other.py").stdout.startswith("posted")
    assert check(world, fact()) == (1, "reject over_cap")


def test_after_finish(w):
    assert check(w, fact(t=w.conf["finish_ms"] + 1)) == (1, "reject after_finish")
