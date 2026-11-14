"""Fault-injection tests F-1..F-14 (DESIGN.md section 6.2)."""

import json

from conftest import ctx_text


# F-6: snapshot failure -> snapshot_missing 1, zero deliveries (same mechanism as T-7)
def test_f6_snapshot_failure(board, tmp_path):
    outs = [board.call("t4-1", "reader", transcript=tmp_path / "nope.jsonl") for _ in range(13)]
    assert all(o == "" for o in outs)
    assert len(board.events("t4-1", "snapshot_missing")) == 1 and board.events("t4-1", "inject") == []


# F-7: a garbage line in tele/ does not change the hook's output
def test_f7_corrupt_board_line(board, tmp_path):
    from conftest import Board
    clean = Board(tmp_path / "clean")
    board.tele("t2b-1", "\x00garbage{")
    a = [board.call("t2b-1", "searcher") for _ in range(10)]
    b = [clean.call("t2b-1", "searcher") for _ in range(10)]
    assert [bool(x) for x in a] == [bool(x) for x in b] and ctx_text(a[9]) == ctx_text(b[9])


# F-14: env -i PATH=/usr/bin:/bin gives the same decisions and outputs
def test_f14_environment_cleared(board, tmp_path):
    from conftest import Board
    other = Board(tmp_path / "envi")
    env = {"PATH": "/usr/bin:/bin"}
    a = [board.call("t2b-1", "searcher") for _ in range(11)]
    b = [other.call("t2b-1", "searcher", env=env) for _ in range(11)]
    assert a == b
    strip = lambda evs: [{k: v for k, v in e.items() if k not in ("ms",)} for e in evs if e["ev"] != "t"]  # noqa: E731
    assert strip(board.metrics("t2b-1")) == strip(other.metrics("t2b-1"))
    assert json.loads(a[5]) and json.loads(a[9])


# ---------------------------------------------------------------- runner faults (stub claude)
def test_f8_hang_killed_at_deadline(runner):
    import time
    for collab in (1, 0):
        if collab:
            runner.settings("t2b-1")
        runner.write_run(hang_ms=int(time.time() * 1000) + 3000)
        (runner.stub / "count").unlink(missing_ok=True)
        runner.plan("sleep 60")
        t = time.time()
        r = runner.run(collab=collab)
        took = time.time() - t
        assert r.returncode == 1 and took < 3 + 5 + 3  # TERM at the deadline, KILL at most 5 s later (+ start-up)
        m = runner.meta()
        assert m["hang_kill"] is True and m["valid"] is False and runner.calls() == 1  # no time left for a retry


def test_f9_failed_block_then_isolated_retry(runner):
    from conftest import finding, json_reply, report
    runner.settings("t2b-1")
    runner.plan(f"replay {runner.file(json_reply('incomplete'))}", f"replay {runner.file(json_reply(report(finding())))}")
    assert runner.run(collab=1).returncode == 0
    m = runner.meta()
    assert m["attempts"] == 2 and m["retry_isolated"] is True and "--settings" not in runner.argv(2)


def test_f10_binary_missing_twice(runner):
    runner.plan("exit 127")
    r = runner.run(collab=0)
    assert r.returncode == 1 and runner.calls() == 2
    assert all(runner.argv(k)[runner.argv(k).index("--model") + 1] == "muse-ember-1.0" for k in (1, 2))
    assert runner.meta()["valid"] is False and not (runner.d / "reviews" / "t2b-1.fallback.log").exists()


def test_f13_hook_error_does_not_kill_review(runner, tmp_path):
    """The stub runs the real hook from --settings for 8 tool calls; the hook's inputs break mid-run."""
    from conftest import Board, finding, json_reply, report
    b = Board(tmp_path / "f13")
    s = runner.settings("t2b-1", board=str(b.dir))
    assert str(b.dir) in s
    (b.dir / "ctx" / "index.json").write_text("{broken")  # every checkpoint now fails inside the hook
    runner.plan(f"hooks 8 {runner.file(json_reply(report(finding())))}")
    r = runner.run(collab=1)
    assert r.returncode == 0, r.stderr
    assert runner.meta()["valid"] is True
    assert [m for m in b.metrics("t2b-1") if m["ev"] == "hook_error"]
    assert all(x == "rc=0" for x in (runner.stub / "hook-rc.1").read_text().split())


# ---------------------------------------------------------------- summary faults (collab_summary.py)
def test_f1_classifier_mislabel_listed(pkg1):
    """The live index lost its keys/paths, so a real M1 call by a peer is missed live and M1 is injected anyway."""
    import json as _j

    from conftest import FIX
    b = pkg1.board
    ix = _j.loads((FIX / "index.json").read_text())
    ix["paths"], ix["keys"] = ["nothing/here.py"], ["zzzz"]
    (b.dir / "ctx" / "index.json").write_text(_j.dumps(ix))
    b.tele("t4-1", _j.dumps({"n": 1, "t": 0, "rid": "t4-1", "sub": False, "tool": "Bash", "input": {"command": "grep -rln merge_guard tests/"}}))
    b.call("t2b-1", "searcher", tool="Read", inp={"file_path": b.src}, order="M1,M2,M7,M4")
    for _ in range(5):
        out = b.call("t2b-1", "searcher", order="M1,M2,M7,M4")
    assert "No panel member" in out and b.events("t2b-1", "inject")[0]["move"] == "M1"
    assert pkg1.summary("pre").returncode == 0
    spot = pkg1.audit()["spot_check"]
    assert any(s.get("move") == "M1" and s["post_hoc"] == "covered" for s in spot)


def test_f3_reviewer_ignores_injection(pkg1):
    from test_collab_summary import searcher_with_m2
    searcher_with_m2(pkg1, then_cmd="ls -la")
    assert pkg1.summary("pre").returncode == 0
    s = [x for x in pkg1.collab_json()["slots"] if x["move"] == "M2"][0]
    assert s["move_executed"] is False
    assert sum(1 for x in pkg1.collab_json()["slots"] if x["move_executed"] is True) == 0


def _plant(p, line, text, inject_id=None):
    import json as _j
    b = p.board
    (b.dir / "msgs").mkdir(exist_ok=True)
    if line is not None:
        (b.dir / "msgs" / "radar.jsonl").write_text(_j.dumps(line) + "\n")
    if inject_id:
        (b.dir / "metrics").mkdir(exist_ok=True)
        with (b.dir / "metrics" / "t4-1.jsonl").open("a") as f:
            f.write(_j.dumps({"ev": "inject", "id": inject_id, "t": 1, "n": 8, "move": "M3", "slot_type": "static", "task_hint": [], "text": text}) + "\n")


def test_f4_leak_quarantines(tmp_path, root):
    from conftest import CAT, Pkg
    base = {"v": "panel-msg/1", "id": "m-t4-1-08", "run": "r", "from": "radar", "to": "t4-1", "t": 1, "kind": "move", "move": "M3"}
    cases = [(dict(base, anchor="Create the guard"), CAT["moves"]["M3"], "m-t4-1-08"),   # an anchor key
             (base, CAT["moves"]["M3"] + " Look at Task 3.", "m-t4-1-08"),                # text differs from the catalogue
             (base, None, None)]                                                         # board line, no inject event
    for i, (line, text, iid) in enumerate(cases):
        p = Pkg(tmp_path / f"c{i}", root, row=f"el2-c1-r{i + 1}")
        _plant(p, line, text, iid)
        r = p.summary("pre")
        assert r.returncode == 3, (i, r.stdout, r.stderr)
        assert (p.d / "QUARANTINED").read_text().strip()


def test_f8_slo_breach_from_hang(pkg1):
    pkg1.review("t4-1", "", end_ms=179_000, hang_kill=True, valid=False)
    assert pkg1.summary("pre").returncode == 0
    c = pkg1.collab_json()
    assert c["slo_breach"] is True and c["reviewers"]["t4-1"]["hang_kill"] is True
