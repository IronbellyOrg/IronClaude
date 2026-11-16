"""Task 3: two processes at once never make a second row."""

from __future__ import annotations

import multiprocessing as mp
import time
from pathlib import Path

from superclaude.cli.issue_pipeline import approval_record as ar

H = "0123456789abcdef" * 4
T = "2026-11-16T10:00:00Z"


def _retry(fn):
    """Call ``fn`` until it is not lock-held, as the verbs tell a caller to."""
    for _ in range(2000):
        try:
            return fn()
        except ar.ApprovalError as exc:
            if exc.reason != "lock-held":
                return ("refused", exc.reason)
            time.sleep(0.002)
    raise AssertionError("lock never freed")


def _create_worker(directory: str, n: int, start, out) -> None:
    start.wait()
    out.put(_retry(lambda: ar.record_create(directory, 9, "plan", H, "comment", f"c{n}", f"u{n}", T))["result"])


def _adopt_worker(directory: str, start, out) -> None:
    start.wait()
    try:
        out.put(ar.adopt_create(directory, 9, "plan", T)["result"])
    except ar.ApprovalError as exc:
        out.put(exc.reason)


def _run(target, args_for) -> list:
    ctx = mp.get_context("fork")
    start, out = ctx.Event(), ctx.Queue()
    procs = [ctx.Process(target=target, args=args_for(n, start, out)) for n in range(6)]
    for p in procs:
        p.start()
    start.set()
    results = [out.get(timeout=30) for _ in procs]
    for p in procs:
        p.join(timeout=30)
        assert p.exitcode == 0
    return results


def test_concurrent_record_create_makes_one_row_and_one_winner(tmp_path: Path) -> None:
    d = tmp_path / "a"
    ar.init_dir(d)
    ar.adopt_create(d, 9, "plan", T)
    ar.adopt_mark(d, 9, "plan", "started", "ctx_1", T)
    results = _run(_create_worker, lambda n, s, o: (str(d), n, s, o))
    assert sorted(results) == ["created"] + ["exists"] * 5
    assert len(list(d.glob("approval-*.json"))) == 1
    assert len(ar.record_show(d, 9, "plan", H)["evidence"]) == 6  # every retry appended


def test_concurrent_adopt_create_has_one_reserved_winner(tmp_path: Path) -> None:
    d = tmp_path / "b"
    ar.init_dir(d)
    results = _run(_adopt_worker, lambda n, s, o: (str(d), s, o))
    assert results.count("created") == 1
    assert all(r in ("created", "uncertain-launch", "lock-held") for r in results)
    assert len(list(d.glob("adoption-*.json"))) == 1
    assert ar.adopt_show(d, 9, "plan")["state"] == "reserved"
