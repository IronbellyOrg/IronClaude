"""hooks/harvest-hook.sh (R-18): DESIGN 6.1 cases."""
import json

from conftest import BIN, run


def settings(w):
    out = w.tmp / "settings-sw.json"
    run(["bash", str(BIN / "make-settings.sh"), "sweeper", "--board", str(w.B), "--t0-ms", str(w.conf["t0_ms"]),
         "--finish-ms", str(w.conf["finish_ms"]), "--out", str(out)], env=w.env, check=True)
    return out


GREP_TESTS = {"command": "grep -rln greeting tests/"}
GREP_OUT = {"stdout": "tests/test_app.py\ntests/test_other.py\n"}


def test_m1_unopened_unnamed_test_first(world):
    world.board()
    s = settings(world)
    out = world.call_hook(s, tool="Bash", tool_input={"command": "grep -rn greeting tests/ ."},
                          response={"stdout": "CHANGELOG.md:2:- greeting wording\ntests/test_other.py:1:# checks the greeting\ntests/test_app.py:1:x\n"})
    assert out == ""
    f = world.board_lines()[0]
    assert f["from"] == "hv-1" and f["move"] == "M1" and f["items"][0] == "tests/test_other.py:1"
    assert "CHANGELOG.md:2" in f["items"] and not any(i.startswith("tests/test_app.py") for i in f["items"])
    assert "anchor" not in f and "n" not in f


def test_named_and_opened_excluded(world):
    world.board()
    (world.B / "state/opened.txt").write_text("tests/test_other.py\n")
    s = settings(world)
    world.call_hook(s, tool="Bash", tool_input=GREP_TESTS, response=GREP_OUT)
    assert world.board_lines() == []


def test_board_items_excluded(world):
    world.board()
    world.seed({"items": ["tests/test_other.py"]})
    s = settings(world)
    world.call_hook(s, tool="Bash", tool_input=GREP_TESTS, response=GREP_OUT)
    assert len(world.board_lines()) == 1


def test_m2_and_m7_signatures(world):
    world.board()
    s = settings(world)
    world.call_hook(s, tool="Bash", tool_input={"command": "grep -rl greeting src"}, response={"stdout": "src/other.py\n"})
    world.call_hook(s, tool="Bash", tool_input={"command": "grep -n greeting README.md CHANGELOG.md"},
                    response={"stdout": "README.md:1:readme greeting\n"})
    assert [f["move"] for f in world.board_lines()] == ["M2", "M7"]


def test_find_delete_posts_nothing(world):
    world.board()
    s = settings(world)
    world.call_hook(s, tool="Bash", tool_input={"command": "find tests -delete"}, response={"stdout": "tests/test_other.py\n"})
    assert world.board_lines() == []


def test_read_posts_nothing(world):
    world.board()
    s = settings(world)
    world.call_hook(s, tool="Read", tool_input={"file_path": "tests/test_other.py"}, response="tests/test_other.py\n")
    assert world.board_lines() == []


def test_grep_tool_synthesised(world):
    world.board()
    s = settings(world)
    world.call_hook(s, tool="Grep", tool_input={"pattern": "greeting", "path": str(world.SB / "repo/tests")},
                    response={"filenames": [str(world.SB / "repo/tests/test_other.py")], "mode": "files_with_matches"})
    f = world.board_lines()[0]
    assert f["cmd"] == "grep -rn -- 'greeting' tests" and f["items"] == ["tests/test_other.py"] and f["move"] == "M1"


def test_shared_cap_across_writers(world):
    world.board(k=1)  # cap 2
    s = settings(world)
    assert world.post("--move", "M7", "--cmd", "grep -rn greeting .", "--item", "README.md").stdout.startswith("posted")
    world.call_hook(s, tool="Bash", tool_input=GREP_TESTS, response=GREP_OUT)
    assert [f["from"] for f in world.board_lines()] == ["sw-1", "hv-1"]
    assert world.post("--move", "M7", "--cmd", "grep -rn greeting .", "--item", "CHANGELOG.md").stdout.strip() == "rejected: over_cap"
    world.call_hook(s, tool="Bash", tool_input={"command": "grep -rl greeting src"}, response={"stdout": "src/other.py\n"})
    rej = [json.loads(x) for x in (world.B / "msgs/rejected.jsonl").read_text().splitlines()]
    assert [(r["from"], r["reason"]) for r in rej] == [("sw-1", "over_cap"), ("hv-1", "over_cap")]
    assert len(world.board_lines()) == 2


def test_never_prints(world):
    world.board()
    s = settings(world)
    for tool, inp, resp in [("Bash", GREP_TESTS, GREP_OUT), ("Read", {"file_path": "x"}, "x"), ("Glob", {"pattern": "tests/*.py"}, {"filenames": []})]:
        assert world.call_hook(s, tool=tool, tool_input=inp, response=resp) == ""
