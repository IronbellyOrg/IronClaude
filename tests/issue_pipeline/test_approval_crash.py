"""Task 3: a kill at the worst moment leaves rows that stop a second start.

Mirrors tests/issue_watch/test_crash_injection.py: a child process does the write
and is killed before its caller can proceed; the parent then reads the disk.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from superclaude.cli.issue_pipeline import approval_record as ar

H = "0123456789abcdef" * 4
T = "2026-11-16T10:00:00Z"


def _killed_after(code: str, directory: Path) -> None:
    """Run ``code`` (with ``ar`` and ``d`` bound) in a child that then SIGKILLs itself."""
    script = (
        "import os, signal\n"
        "from superclaude.cli.issue_pipeline import approval_record as ar\n"
        f"d = {str(directory)!r}\n"
        f"{code}\n"
        "os.kill(os.getpid(), signal.SIGKILL)\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, timeout=60
    )
    assert proc.returncode == -9, proc.stderr.decode()[-300:]


def test_a_killed_record_create_is_on_disk_as_recorded(tmp_path: Path) -> None:
    d = tmp_path / "a"
    ar.init_dir(d)
    ar.adopt_create(d, 9, "plan", T)
    ar.adopt_mark(d, 9, "plan", "started", "ctx_1", T)
    _killed_after(
        f"ar.record_create(d, 9, 'plan', {H!r}, 'label', 'e1', 'u1', {T!r})", d
    )
    assert ar.record_show(d, 9, "plan", H)["state"] == "recorded"


def test_a_kill_between_worker_start_and_adopt_mark_blocks_a_second_start(
    tmp_path: Path,
) -> None:
    d = tmp_path / "b"
    ar.init_dir(d)
    _killed_after(
        f"ar.adopt_create(d, 9, 'plan', {T!r})", d
    )  # worker-start ran, adopt-mark never did
    assert ar.adopt_show(d, 9, "plan")["state"] == "reserved"
    try:
        ar.adopt_create(d, 9, "plan", T)
    except ar.ApprovalError as exc:
        assert exc.reason == "uncertain-launch"
    else:
        raise AssertionError("a second start was allowed")


def test_duplicate_approval_and_a_crash_before_the_reply_give_at_most_one_instruction(
    tmp_path: Path,
) -> None:
    d = tmp_path / "c"
    ar.init_dir(d)
    ar.adopt_create(d, 9, "plan", T)
    ar.adopt_mark(d, 9, "plan", "started", "ctx_1", T)
    ar.record_create(d, 9, "plan", H, "label", "e1", "u1", T)
    ar.record_create(
        d, 9, "plan", H, "comment", "c1", "u1", T
    )  # duplicate approval, other channel
    # the coordinator records the instruction first (write-ahead), then replies; it dies before the reply
    _killed_after(f"ar.record_mark(d, 9, 'plan', {H!r}, 'instructed', {T!r})", d)
    assert ar.record_show(d, 9, "plan", H)["state"] == "instructed"
    # the next coordinator pass cannot record a second instruction, so it sends none
    try:
        ar.record_mark(d, 9, "plan", H, "instructed", T)
    except ar.ApprovalError as exc:
        assert exc.reason == "bad-move"
    else:
        raise AssertionError("a second continuation instruction was allowed")
    # the adoption row still holds exactly one start
    assert ar.adopt_show(d, 9, "plan")["state"] == "started"
    assert (
        len(list(d.glob("adoption-*.json"))) == 1
        and len(list(d.glob("approval-*.json"))) == 1
    )
