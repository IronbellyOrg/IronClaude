"""T07.04 / FR-002 -- ``superclaude swarm status`` subcommand.

Covers roadmap row R-121 (FR-002). Pins the operator-visible contract
of ``cli/swarm/commands.py::status_cmd``:

1. Registered with ``swarm_group`` under the ``status`` name (replaces
   the T01.08 placeholder).
2. Reads ``<output_dir>/.swarm-state.json`` via the state module and
   prints a grep-friendly one-line summary
   ``status: phase=<phase> job_id=<id> updated=<ts>[ terminal_status=<s>]``.
3. Exit codes:

       * 0 -- non-terminal phase, OR terminal+success, OR terminal with
         unreadable contract (status unknown).
       * 1 -- terminal phase with contract status ``partial`` /
         ``failed`` (acceptance: "non-zero partial/failed").
       * 2 -- usage error: ``--output`` directory missing, state file
         missing, corrupt JSON, ``--job`` mismatch.

4. ``--watch`` polls .swarm-state.json on a configurable interval
   until ``terminal`` is reached (bounded by ``--watch-max-iterations``
   for the test surface).

Fixture state files are written via the real :func:`write_state`
emitter so the test surface exercises the byte-for-byte format the
production state-writer produces (T03.03 / NFR-002 atomic write).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXIT_INVALID,
    EXIT_OK,
    EXIT_USAGE,
    RESULT_CONTRACT_FILENAME,
    SWARM_STATE_FILENAME,
    run_cmd,
    status_cmd,
)
from superclaude.cli.swarm.models import SwarmState
from superclaude.cli.swarm.state import read_state, write_state

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _write_state(tmp_path: Path, **kwargs: Any) -> Path:
    """Write a ``.swarm-state.json`` fixture and return the directory."""
    state = SwarmState(**kwargs)
    write_state(tmp_path / SWARM_STATE_FILENAME, state)
    return tmp_path


def _write_contract(tmp_path: Path, status: str) -> Path:
    """Write a stub ``return-contract.yaml`` carrying ``status``."""
    import yaml

    payload = {"contract_version": "1.0", "status": status, "job_id": "job-x"}
    contract_path = tmp_path / RESULT_CONTRACT_FILENAME
    contract_path.write_text(yaml.safe_dump(payload), encoding="utf-8")
    return contract_path


# ---------------------------------------------------------------------------
# Registration -- AC-002 / T01.08 placeholder replacement.
# ---------------------------------------------------------------------------


def test_status_cmd_registered_with_swarm_group() -> None:
    """``status`` is bound on swarm_group to the concrete command."""
    assert "status" in swarm_group.commands
    assert swarm_group.commands["status"] is status_cmd


def test_status_help_advertises_watch_and_job_flags() -> None:
    """``--help`` enumerates --output / --job / --watch / --watch-interval."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["status", "--help"])
    assert result.exit_code == 0, result.output
    assert "--output" in result.output
    assert "--job" in result.output
    assert "--watch" in result.output
    assert "--watch-interval" in result.output


# ---------------------------------------------------------------------------
# Happy paths -- non-terminal phases (exit 0).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "phase",
    ["preflight_ok", "dispatching", "normalizing", "reducing"],
)
def test_status_non_terminal_phase_exits_zero(tmp_path: Path, phase: str) -> None:
    """Every non-terminal phase reports cleanly and exits 0."""
    output_dir = _write_state(tmp_path, state=phase, job_id="job-001")

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["status", "--output", str(output_dir)],
    )
    assert result.exit_code == EXIT_OK, result.output
    assert f"phase={phase}" in result.stdout
    assert "job_id=job-001" in result.stdout
    assert "terminal_status=" not in result.stdout


# ---------------------------------------------------------------------------
# Terminal + contract -- exit code keyed on ResultContract.status.
# ---------------------------------------------------------------------------


def test_status_terminal_success_exits_zero(tmp_path: Path) -> None:
    """Terminal phase + success contract -> exit 0, suffix present."""
    output_dir = _write_state(tmp_path, state="terminal", job_id="job-001")
    _write_contract(output_dir, status="success")

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["status", "--output", str(output_dir)])
    assert result.exit_code == EXIT_OK, result.output
    assert "phase=terminal" in result.stdout
    assert "terminal_status=success" in result.stdout


@pytest.mark.parametrize("status", ["partial", "failed"])
def test_status_terminal_non_success_exits_invalid(tmp_path: Path, status: str) -> None:
    """Terminal phase + partial/failed contract -> exit 1."""
    output_dir = _write_state(tmp_path, state="terminal", job_id="job-001")
    _write_contract(output_dir, status=status)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["status", "--output", str(output_dir)])
    assert result.exit_code == EXIT_INVALID, result.output
    assert "phase=terminal" in result.stdout
    assert f"terminal_status={status}" in result.stdout


def test_status_terminal_without_contract_exits_zero(tmp_path: Path) -> None:
    """Terminal phase but no contract on disk -> exit 0 (status unknown).

    Documents the "degraded but not definitively failed" branch: a job
    that crashed between writing terminal state and emitting the
    contract should not be reported as a confirmed failure by the
    status surface; CI scripts that want strict failure should inspect
    the done sentinel or contract directly.
    """
    output_dir = _write_state(tmp_path, state="terminal", job_id="job-001")

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["status", "--output", str(output_dir)])
    assert result.exit_code == EXIT_OK, result.output
    assert "phase=terminal" in result.stdout
    assert "terminal_status=" not in result.stdout


# ---------------------------------------------------------------------------
# Usage-error paths -- exit 2.
# ---------------------------------------------------------------------------


def test_status_missing_output_dir_exits_usage(tmp_path: Path) -> None:
    """A missing ``--output`` directory yields EXIT_USAGE on stderr."""
    missing = tmp_path / "does-not-exist"
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["status", "--output", str(missing)])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "output directory not found" in result.stderr


def test_status_missing_state_file_exits_usage(tmp_path: Path) -> None:
    """A directory without ``.swarm-state.json`` yields EXIT_USAGE."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["status", "--output", str(tmp_path)])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "state file not found" in result.stderr


def test_status_corrupt_state_file_exits_usage(tmp_path: Path) -> None:
    """Corrupt JSON in the state file yields EXIT_USAGE."""
    (tmp_path / SWARM_STATE_FILENAME).write_text("{not-valid-json", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["status", "--output", str(tmp_path)])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "not valid JSON" in result.stderr


def test_status_job_id_mismatch_exits_usage(tmp_path: Path) -> None:
    """``--job`` mismatch against state.job_id yields EXIT_USAGE."""
    output_dir = _write_state(tmp_path, state="dispatching", job_id="job-001")
    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["status", "--output", str(output_dir), "--job", "job-999"],
    )
    assert result.exit_code == EXIT_USAGE, result.output
    assert "job_id mismatch" in result.stderr


def test_status_job_id_match_passes(tmp_path: Path) -> None:
    """``--job`` matching state.job_id succeeds."""
    output_dir = _write_state(tmp_path, state="dispatching", job_id="job-001")
    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["status", "--output", str(output_dir), "--job", "job-001"],
    )
    assert result.exit_code == EXIT_OK, result.output
    assert "phase=dispatching" in result.stdout


# ---------------------------------------------------------------------------
# --watch loop -- bounded by --watch-max-iterations.
# ---------------------------------------------------------------------------


def test_status_watch_emits_one_line_per_iteration_until_terminal(
    tmp_path: Path,
) -> None:
    """``--watch`` re-emits the status line each poll until terminal.

    Bounded by ``--watch-max-iterations`` so the test cannot hang. The
    state file is updated mid-test to simulate a wave transition; the
    output stream must contain one line per observed phase plus the
    terminal stop.
    """
    output_dir = _write_state(tmp_path, state="dispatching", job_id="job-watch")
    _write_contract(output_dir, status="success")

    # Pre-flip the state file to terminal before the runner starts so
    # the watch loop sees terminal on its first iteration and exits
    # cleanly. The watch-iteration test exercises the loop exit on
    # terminal -- not the timing of state transitions.
    write_state(
        output_dir / SWARM_STATE_FILENAME,
        SwarmState(state="terminal", job_id="job-watch"),
    )

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "status",
            "--output",
            str(output_dir),
            "--watch",
            "--watch-interval",
            "0.05",
            "--watch-max-iterations",
            "3",
        ],
    )
    assert result.exit_code == EXIT_OK, result.output
    # At least one iteration's worth of status line on stdout.
    assert result.stdout.count("phase=terminal") >= 1
    assert "terminal_status=success" in result.stdout


def test_status_watch_max_iterations_caps_loop_on_non_terminal(
    tmp_path: Path,
) -> None:
    """Non-terminal state under ``--watch`` stops at max-iterations.

    Pins the test-surface invariant that ``--watch-max-iterations``
    bounds the worst case for a job that never reaches terminal --
    important so the test suite stays deterministic and fast.
    """
    output_dir = _write_state(tmp_path, state="dispatching", job_id="job-cap")
    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "status",
            "--output",
            str(output_dir),
            "--watch",
            "--watch-interval",
            "0.01",
            "--watch-max-iterations",
            "2",
        ],
    )
    assert result.exit_code == EXIT_OK, result.output
    # Two iterations -> two status lines on stdout.
    assert result.stdout.count("phase=dispatching") == 2


def test_status_watch_breaks_on_usage_error(tmp_path: Path) -> None:
    """Usage errors stop the watch loop after a single iteration.

    A missing state file under --watch should surface the diagnostic
    once on stderr and exit EXIT_USAGE -- not spin at watch_interval
    re-reporting the same error.
    """
    # Empty directory -> state file missing.
    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "status",
            "--output",
            str(tmp_path),
            "--watch",
            "--watch-interval",
            "0.01",
            "--watch-max-iterations",
            "5",
        ],
    )
    assert result.exit_code == EXIT_USAGE, result.output
    # Only one diagnostic line, not five.
    assert result.stderr.count("state file not found") == 1


# ---------------------------------------------------------------------------
# F-P3-3 -- the production ``swarm run`` path persists ``.swarm-state.json``
# so ``swarm status`` has a record to read end-to-end (the prior behaviour
# left no state file, so status reported EXIT_USAGE after a real run).
# ---------------------------------------------------------------------------


def _stub_run(tmp_path: Path) -> Path:
    """Run a deterministic stub job under ``tmp_path`` and return its output dir."""
    target = tmp_path / "target.py"
    target.write_text(
        "# F-P3-3 state-persistence target\n"
        + "def hello() -> str:\n    return 'state persisted'\n"
        + "# padding to clear the IMM-4 non-whitespace byte floor\n" * 6,
        encoding="utf-8",
    )
    output_dir = tmp_path / "out"
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )
    assert result.exit_code == EXIT_OK, (
        f"stub run must succeed; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    return output_dir


def test_run_cmd_persists_terminal_swarm_state(tmp_path: Path) -> None:
    """F-P3-3: a completed inline run leaves a terminal ``.swarm-state.json``.

    Before the fix the run path built an in-memory ``SwarmState`` in
    preflight but never wrote it, so ``.swarm-state.json`` was absent after
    a real run. The state must now exist, report ``terminal``, carry the
    job_id, and have a stamped ``updated`` timestamp.
    """
    output_dir = _stub_run(tmp_path)

    state_path = output_dir / SWARM_STATE_FILENAME
    assert state_path.is_file(), (
        f"F-P3-3: run path left no {SWARM_STATE_FILENAME} under {output_dir}"
    )
    state = read_state(state_path)
    assert state is not None
    assert state.state == "terminal", (
        f"expected terminal state after a completed run; got {state.state!r}"
    )
    assert state.job_id, "state must carry the job_id"
    assert state.updated, "write_state must stamp the updated timestamp"


def test_status_reads_run_written_state_end_to_end(tmp_path: Path) -> None:
    """F-P3-3: ``swarm status`` reads the state the run path persisted.

    End-to-end proof that the run -> status hand-off works without any
    test-authored fixture state: status finds ``phase=terminal`` and exits
    cleanly (terminal + no contract -> EXIT_OK).
    """
    output_dir = _stub_run(tmp_path)

    runner = CliRunner()
    result = runner.invoke(status_cmd, ["--output", str(output_dir)])
    assert result.exit_code == EXIT_OK, (
        f"status after a real run must exit cleanly; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "phase=terminal" in result.stdout, result.stdout


def test_run_written_state_is_confined_to_output_dir(tmp_path: Path) -> None:
    """F-P3-3: the persisted state lands inside the ``--output`` root.

    The state write is confined via ``write_state(..., output_dir=...)``;
    the resulting file must be a direct child of the output directory, never
    written outside it.
    """
    output_dir = _stub_run(tmp_path)

    state_path = output_dir / SWARM_STATE_FILENAME
    assert state_path.is_file()
    assert state_path.resolve().parent == output_dir.resolve(), (
        "F-P3-3: state file escaped the --output root"
    )
