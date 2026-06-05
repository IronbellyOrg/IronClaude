"""T03.03 -- ``cli/swarm/state.py`` atomic-write contract.

Covers the acceptance criteria from
``.dev/releases/Current/MultiModelSwarm/tasklist/phase-3-tasklist.md``::

* State transitions go through tmp+``os.replace``; no
  ``open(path, "w")`` writes the live path directly.
* ``read_state`` returns a :class:`SwarmState` on success, ``None`` if
  missing, raises on corrupt JSON.
* Mid-write kill leaves no partial state file (verified by
  subprocess + ``SIGKILL``).
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from superclaude.cli.swarm.models import SwarmState
from superclaude.cli.swarm.state import read_state, write_state


# ---------------------------------------------------------------------------
# Module-level static guards.
# ---------------------------------------------------------------------------


def test_state_module_has_no_direct_open_write_for_live_path() -> None:
    """AC: ``no open(path, "w")`` writes the live state path directly.

    Mirrors the phase-3 validation grep
    (``grep -nE 'open\\(.*".*state.*\\.json.*w' src/superclaude/cli/swarm/state.py``)
    so the rule is enforced inside the test lane too.
    """
    state_module_src = Path(
        "src/superclaude/cli/swarm/state.py"
    ).read_text(encoding="utf-8")
    assert ".tmp" in state_module_src, "atomic-write tmp idiom missing"
    assert "os.replace" in state_module_src, "atomic-write os.replace missing"
    forbidden = 'open(path, "w"'
    assert forbidden not in state_module_src, (
        f"state.py must not call {forbidden!r} -- writes go through tmp + "
        "os.replace per NFR-002."
    )


# ---------------------------------------------------------------------------
# read_state -- happy path, missing-file, corrupt JSON.
# ---------------------------------------------------------------------------


def test_read_state_returns_none_when_missing(tmp_path: Path) -> None:
    """Missing files surface as ``None`` (resume short-circuit)."""
    target = tmp_path / ".swarm-state.json"
    assert read_state(target) is None


def test_read_state_round_trip(tmp_path: Path) -> None:
    """``write_state`` then ``read_state`` reconstructs the same instance."""
    target = tmp_path / ".swarm-state.json"
    write_state(target, SwarmState(state="dispatching", job_id="job-001"))

    loaded = read_state(target)
    assert loaded is not None
    assert loaded.state == "dispatching"
    assert loaded.job_id == "job-001"
    assert loaded.updated, "write_state must stamp updated timestamp"


def test_read_state_raises_on_corrupt_json(tmp_path: Path) -> None:
    """Corrupt JSON surfaces as :class:`json.JSONDecodeError`."""
    target = tmp_path / ".swarm-state.json"
    target.write_text("{not-valid-json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        read_state(target)


def test_read_state_raises_on_invalid_state_value(tmp_path: Path) -> None:
    """Shape-valid JSON with unknown ``state`` Literal raises ``ValueError``.

    The dataclass ``__post_init__`` enforces the Literal allowlist;
    ``read_state`` must surface that error rather than silently
    constructing a SwarmState with a bogus state.
    """
    target = tmp_path / ".swarm-state.json"
    target.write_text(
        json.dumps({"state": "bogus", "job_id": "", "updated": ""}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        read_state(target)


# ---------------------------------------------------------------------------
# write_state -- atomicity, tmp-file cleanup, updated stamp, parent mkdir.
# ---------------------------------------------------------------------------


def test_write_state_stamps_updated(tmp_path: Path) -> None:
    """``write_state`` always rewrites ``updated`` even when caller leaves it blank."""
    target = tmp_path / ".swarm-state.json"
    state = SwarmState(state="preflight_ok", job_id="job-002", updated="")

    write_state(target, state)

    on_disk = json.loads(target.read_text(encoding="utf-8"))
    assert on_disk["updated"]
    # The instance is mutated in-place so callers can see the stamp too.
    assert state.updated == on_disk["updated"]


def test_write_state_creates_parent_directory(tmp_path: Path) -> None:
    """Missing parent dirs are created before the tmp+replace dance."""
    target = tmp_path / "nested" / "deeper" / ".swarm-state.json"
    write_state(target, SwarmState(job_id="job-003"))

    assert target.exists()
    loaded = read_state(target)
    assert loaded is not None
    assert loaded.job_id == "job-003"


def test_write_state_leaves_no_tmp_file(tmp_path: Path) -> None:
    """After a clean write the tmp sibling must not linger."""
    target = tmp_path / ".swarm-state.json"
    write_state(target, SwarmState(job_id="job-004"))

    tmp_sibling = target.with_suffix(target.suffix + ".tmp")
    assert not tmp_sibling.exists()


def test_write_state_overwrites_existing(tmp_path: Path) -> None:
    """Subsequent writes replace the file atomically (last-write-wins)."""
    target = tmp_path / ".swarm-state.json"
    write_state(target, SwarmState(state="preflight_ok", job_id="job-005"))
    write_state(target, SwarmState(state="terminal", job_id="job-005"))

    loaded = read_state(target)
    assert loaded is not None
    assert loaded.state == "terminal"


# ---------------------------------------------------------------------------
# IMM-6 mid-write-kill: SIGKILL between tmp write and os.replace.
# ---------------------------------------------------------------------------


def test_mid_write_kill_leaves_no_partial_state_file(tmp_path: Path) -> None:
    """SIGKILL mid-write must leave the live path either pristine or absent.

    Strategy: launch a subprocess that monkey-patches ``os.replace`` to
    ``SIGKILL`` itself instead of performing the swap. The tmp sibling
    will have been written by then, but the live path must not exist
    yet. After the kill we assert:

      * the live ``path`` does NOT exist (atomic swap never happened);
      * the tmp sibling may or may not exist (it is a *staging* file,
        not a partial *live* file).

    This is the NFR-002 / IMM-6 atomicity guarantee at the state-module
    level. The broader IMM-6 sweep across every writer lives in
    ``tests/swarm/test_imm6_atomic_write.py`` (T03.13).
    """
    target = tmp_path / ".swarm-state.json"
    repo_root = Path(__file__).resolve().parents[2]

    script = textwrap.dedent(
        f"""
        import os, signal, sys
        sys.path.insert(0, {str(repo_root / "src")!r})

        from superclaude.cli.swarm.models import SwarmState
        from superclaude.cli.swarm import state as state_mod

        def _suicide(*_a, **_kw):
            os.kill(os.getpid(), signal.SIGKILL)

        state_mod.os.replace = _suicide
        state_mod.write_state({str(target)!r}, SwarmState(job_id="job-kill"))
        """
    ).strip()

    completed = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        timeout=15,
    )

    # SIGKILL exits with -SIGKILL on POSIX. Anything else means the
    # subprocess crashed before reaching the os.replace site (bad
    # import path, etc.) and the test is meaningless.
    assert completed.returncode == -signal.SIGKILL, (
        f"subprocess exit code {completed.returncode}; "
        f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
    )

    assert not target.exists(), (
        "Mid-write kill left a partial state file at the live path; "
        "tmp+os.replace contract violated."
    )


def test_post_kill_rerun_produces_clean_state(tmp_path: Path) -> None:
    """After a mid-write kill, re-running ``write_state`` must succeed.

    No locks, no leftover tmp file should block the next attempt.
    Covers the idempotency arm of IMM-6.
    """
    target = tmp_path / ".swarm-state.json"
    # Simulate the leftover-tmp-from-prior-crash scenario.
    tmp_sibling = target.with_suffix(target.suffix + ".tmp")
    tmp_sibling.write_text("garbage-from-prior-run", encoding="utf-8")

    write_state(target, SwarmState(state="normalizing", job_id="job-recover"))

    loaded = read_state(target)
    assert loaded is not None
    assert loaded.state == "normalizing"
    # Live path is clean; tmp sibling is cleared by the successful replace.
    assert not tmp_sibling.exists()
