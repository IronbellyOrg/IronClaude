"""B/bin/panel-post: DESIGN 6.1 cases."""
import concurrent.futures as cf
import json

from conftest import CAND_A


def test_builds_envelope(world):
    world.board()
    r = world.post("--move", "M1", "--cmd", "grep -rln greeting tests/", "--anchor", CAND_A, "--item", "tests/test_other.py", "--n", "1")
    assert r.returncode == 0 and r.stdout.strip() == "posted f-0"
    f = world.board_lines()[0]
    assert f["id"] == "f-0" and f["from"] == "sw-1" and f["to"] == "*" and f["run"] == "run1/pkg"
    assert isinstance(f["t"], int) and f["kind"] == "fact" and f["v"] == "panel-msg/1" and f["n"] == 1
    assert world.post("--move", "M7", "--cmd", "grep -rn greeting .", "--item", "CHANGELOG.md").stdout.strip() == "posted f-1"


def test_unknown_flag(world):
    world.board()
    r = world.post("--move", "M1", "--claim", "x", "--cmd", "ls", "--item", "tests/test_other.py")
    assert r.returncode == 1 and r.stdout.startswith("rejected: unknown_flag")
    assert world.board_lines() == []


def test_rank_and_trim_to_600(world):
    world.board()
    longs = []
    for i in range(4):
        p = f"tests/test_{'a' * 60}{i}.py"
        (world.SB / "repo" / p).write_text("x\n")
        longs.append(p)
    others = []
    for i in range(3):
        p = f"src/{'b' * 60}{i}.py"
        (world.SB / "repo" / p).write_text("x\n")
        others.append(p)
    # given out of rank order: others first, then the root doc, then unnamed tests
    args = []
    for p in others + ["CHANGELOG.md"] + longs:
        args += ["--item", p]
    r = world.post("--move", "M2", "--cmd", "grep -rl " + "z" * 150 + " tests src", "--anchor", CAND_A, *args)
    assert r.stdout.strip() == "posted f-0", r.stdout
    f = world.board_lines()[0]
    line = (world.B / "msgs/board.jsonl").read_text().splitlines()[0]
    assert len(line.encode()) <= 600
    ranked = longs + ["CHANGELOG.md"] + others
    assert 1 <= len(f["items"]) < 8 and f["items"] == ranked[:len(f["items"])]  # lowest-ranked dropped first


def test_concurrent_posts(world):
    world.board(k=8)
    def one(i):
        return world.post("--move", "M1", "--cmd", f"grep -rln w{i} tests/", "--item", "tests/test_other.py").stdout.strip()
    with cf.ThreadPoolExecutor(8) as ex:
        outs = list(ex.map(one, range(8)))
    assert sorted(outs) == sorted(f"posted f-{i}" for i in range(8))
    lines = world.board_lines()
    assert len(lines) == 8 and len({x["id"] for x in lines}) == 8
    assert sorted(x["cmd"] for x in lines) == sorted(f"grep -rln w{i} tests/" for i in range(8))
    assert all(json.loads(json.dumps(x)) for x in lines)
