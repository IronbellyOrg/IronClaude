"""T07.05 / FR-003 -- ``superclaude swarm logs`` subcommand.

Covers roadmap row R-122 (FR-003). Pins the operator-visible contract
of ``cli/swarm/commands.py::logs_cmd``:

1. Registered with ``swarm_group`` under the ``logs`` name (replaces
   the T01.08 placeholder).
2. Reads ``<output_dir>/execution-log.md`` by default; ``--jsonl``
   switches to ``<output_dir>/execution-log.jsonl``. ``--tail`` is the
   shorthand for ``--jsonl --follow``.
3. ``--follow`` polls the log on ``--watch-interval`` seconds and
   emits any appended bytes until ``.swarm-state.json`` reaches
   ``terminal`` (or the operator interrupts). Bounded by
   ``--watch-max-iterations`` for the test surface.
4. Exit codes:

       * 0 -- one-shot dump succeeded, OR follow loop exited cleanly.
       * 2 -- usage error: ``--output`` directory missing, log file
         missing, ``--job`` mismatch with the state's recorded job_id.

Fixture log files are written via the real :class:`Logger` so the test
surface exercises the byte-for-byte format the production logger
produces (T03.04 dual-format JSONL + Markdown emission).
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXECUTION_LOG_JSONL_FILENAME,
    EXECUTION_LOG_MD_FILENAME,
    EXIT_OK,
    EXIT_USAGE,
    SWARM_STATE_FILENAME,
    logs_cmd,
)
from superclaude.cli.swarm.logging_ import Logger
from superclaude.cli.swarm.models import EventRecord, SwarmState
from superclaude.cli.swarm.state import write_state


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _seed_logger(tmp_path: Path) -> Logger:
    """Return a Logger pointing at execution-log.{jsonl,md} in ``tmp_path``."""
    return Logger(
        jsonl_path=tmp_path / EXECUTION_LOG_JSONL_FILENAME,
        md_path=tmp_path / EXECUTION_LOG_MD_FILENAME,
    )


def _seed_events(tmp_path: Path, count: int = 3) -> Logger:
    """Write ``count`` deterministic events to both log surfaces."""
    logger = _seed_logger(tmp_path)
    for index in range(count):
        logger.log_event(
            EventRecord(
                event_type="worker_start",
                timestamp=f"2026-06-01T09:00:0{index}+00:00",
                worker_index=index,
                payload={"slot": index},
            )
        )
    return logger


def _write_terminal_state(tmp_path: Path, job_id: str = "job-x") -> None:
    """Stamp ``.swarm-state.json`` at ``terminal`` so follow exits cleanly."""
    write_state(
        tmp_path / SWARM_STATE_FILENAME,
        SwarmState(state="terminal", job_id=job_id),
    )


# ---------------------------------------------------------------------------
# Registration -- AC-002 / T01.08 placeholder replacement.
# ---------------------------------------------------------------------------


def test_logs_cmd_registered_with_swarm_group() -> None:
    """``logs`` is bound on swarm_group to the concrete command."""
    assert "logs" in swarm_group.commands
    assert swarm_group.commands["logs"] is logs_cmd


def test_logs_help_advertises_format_and_follow_flags() -> None:
    """``--help`` enumerates --output / --jsonl / --md / --follow / --tail."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["logs", "--help"])
    assert result.exit_code == 0, result.output
    assert "--output" in result.output
    assert "--job" in result.output
    assert "--jsonl" in result.output
    assert "--md" in result.output
    assert "--follow" in result.output
    assert "--tail" in result.output
    assert "--lines" in result.output


# ---------------------------------------------------------------------------
# Default one-shot dump -- markdown surface.
# ---------------------------------------------------------------------------


def test_logs_default_dumps_markdown(tmp_path: Path) -> None:
    """Default invocation dumps execution-log.md to stdout."""
    _seed_events(tmp_path, count=3)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["logs", "--output", str(tmp_path)])

    assert result.exit_code == EXIT_OK, result.output
    md_text = (tmp_path / EXECUTION_LOG_MD_FILENAME).read_text(encoding="utf-8")
    assert result.stdout == md_text
    # Sanity: three events => three lines.
    assert result.stdout.count("worker_start") == 3


def test_logs_default_when_md_missing_exits_usage(tmp_path: Path) -> None:
    """Missing execution-log.md is EXIT_USAGE with a stderr diagnostic."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["logs", "--output", str(tmp_path)])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "log file not found" in result.stderr
    assert EXECUTION_LOG_MD_FILENAME in result.stderr


# ---------------------------------------------------------------------------
# --jsonl dump -- canonical JSONL surface.
# ---------------------------------------------------------------------------


def test_logs_jsonl_dumps_jsonl_file(tmp_path: Path) -> None:
    """``--jsonl`` switches to execution-log.jsonl."""
    _seed_events(tmp_path, count=2)

    runner = CliRunner()
    result = runner.invoke(
        swarm_group, ["logs", "--output", str(tmp_path), "--jsonl"]
    )

    assert result.exit_code == EXIT_OK, result.output
    jsonl_text = (tmp_path / EXECUTION_LOG_JSONL_FILENAME).read_text(
        encoding="utf-8"
    )
    assert result.stdout == jsonl_text
    # Every line parses as JSON (no Markdown noise leaking through).
    for line in result.stdout.splitlines():
        assert json.loads(line)["event_type"] == "worker_start"


def test_logs_jsonl_when_missing_exits_usage(tmp_path: Path) -> None:
    """Missing execution-log.jsonl is EXIT_USAGE."""
    # Seed only the markdown surface so the .jsonl path is absent.
    (tmp_path / EXECUTION_LOG_MD_FILENAME).write_text(
        "- [t] e worker=-: \n", encoding="utf-8"
    )
    runner = CliRunner()
    result = runner.invoke(
        swarm_group, ["logs", "--output", str(tmp_path), "--jsonl"]
    )
    assert result.exit_code == EXIT_USAGE, result.output
    assert EXECUTION_LOG_JSONL_FILENAME in result.stderr


# ---------------------------------------------------------------------------
# --lines tail cap on one-shot dump.
# ---------------------------------------------------------------------------


def test_logs_lines_caps_dump_to_last_n(tmp_path: Path) -> None:
    """``--lines N`` emits only the last N lines on one-shot dump."""
    _seed_events(tmp_path, count=5)

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["logs", "--output", str(tmp_path), "--lines", "2"],
    )
    assert result.exit_code == EXIT_OK, result.output
    output_lines = result.stdout.splitlines()
    assert len(output_lines) == 2
    # Last two events have indices 3 and 4.
    assert "worker=3" in output_lines[0]
    assert "worker=4" in output_lines[1]


def test_logs_lines_jsonl_caps_to_last_n(tmp_path: Path) -> None:
    """``--lines N --jsonl`` emits the last N JSONL records."""
    _seed_events(tmp_path, count=4)

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "logs",
            "--output",
            str(tmp_path),
            "--jsonl",
            "--lines",
            "2",
        ],
    )
    assert result.exit_code == EXIT_OK, result.output
    out_lines = result.stdout.splitlines()
    assert len(out_lines) == 2
    indices = [json.loads(line)["worker_index"] for line in out_lines]
    assert indices == [2, 3]


# ---------------------------------------------------------------------------
# --tail / --follow -- live tail loop bounded for the test surface.
# ---------------------------------------------------------------------------


def test_logs_follow_seeds_then_exits_on_terminal(tmp_path: Path) -> None:
    """``--follow`` emits the seed then exits when state reaches terminal.

    With the state file already at ``terminal``, the follow loop should
    print the existing log contents (seed phase) and exit on the first
    iteration of the polling loop without spinning.
    """
    _seed_events(tmp_path, count=2)
    _write_terminal_state(tmp_path, job_id="job-follow")

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "logs",
            "--output",
            str(tmp_path),
            "--follow",
            "--watch-interval",
            "0.01",
            "--watch-max-iterations",
            "1",
        ],
    )
    assert result.exit_code == EXIT_OK, result.output
    assert result.stdout.count("worker_start") == 2


def test_logs_tail_shorthand_is_jsonl_follow(tmp_path: Path) -> None:
    """``--tail`` is shorthand for ``--jsonl --follow``."""
    _seed_events(tmp_path, count=2)
    _write_terminal_state(tmp_path, job_id="job-tail")

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "logs",
            "--output",
            str(tmp_path),
            "--tail",
            "--watch-interval",
            "0.01",
            "--watch-max-iterations",
            "1",
        ],
    )
    assert result.exit_code == EXIT_OK, result.output
    # JSONL surface -- every emitted line parses as JSON.
    for line in result.stdout.splitlines():
        json.loads(line)


def test_logs_follow_max_iterations_caps_loop_on_non_terminal(
    tmp_path: Path,
) -> None:
    """Non-terminal state under --follow stops at watch-max-iterations."""
    _seed_events(tmp_path, count=1)
    # State exists but is non-terminal -> follow loop polls until cap.
    write_state(
        tmp_path / SWARM_STATE_FILENAME,
        SwarmState(state="dispatching", job_id="job-cap"),
    )

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "logs",
            "--output",
            str(tmp_path),
            "--follow",
            "--watch-interval",
            "0.01",
            "--watch-max-iterations",
            "2",
        ],
    )
    assert result.exit_code == EXIT_OK, result.output
    # Seed only -- no new bytes appeared, so output is the seed text.
    assert result.stdout.count("worker_start") == 1


def test_logs_follow_emits_appended_lines(tmp_path: Path) -> None:
    """Follow loop emits bytes appended after the seed phase.

    Writer thread appends one extra event partway through the polling
    window; the follow loop must surface that line before terminating
    on the state-terminal signal flipped by the writer.
    """
    logger = _seed_events(tmp_path, count=1)
    write_state(
        tmp_path / SWARM_STATE_FILENAME,
        SwarmState(state="dispatching", job_id="job-appender"),
    )

    barrier = threading.Event()

    def _appender() -> None:
        # Give the runner time to print the seed and enter the loop.
        barrier.wait(timeout=2.0)
        time.sleep(0.05)
        logger.log_event(
            EventRecord(
                event_type="worker_done",
                timestamp="2026-06-01T09:01:00+00:00",
                worker_index=99,
                payload={"slot": 99},
            )
        )
        # Flip to terminal so the follow loop exits without hitting the
        # iteration cap.
        write_state(
            tmp_path / SWARM_STATE_FILENAME,
            SwarmState(state="terminal", job_id="job-appender"),
        )

    appender = threading.Thread(target=_appender, daemon=True)
    appender.start()
    barrier.set()

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "logs",
            "--output",
            str(tmp_path),
            "--follow",
            "--watch-interval",
            "0.02",
            "--watch-max-iterations",
            "50",
        ],
    )
    appender.join(timeout=2.0)

    assert result.exit_code == EXIT_OK, result.output
    assert "worker_start" in result.stdout
    assert "worker_done" in result.stdout
    assert "worker=99" in result.stdout


def test_logs_follow_missing_log_exits_usage(tmp_path: Path) -> None:
    """``--follow`` against an absent log file is EXIT_USAGE up-front."""
    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        [
            "logs",
            "--output",
            str(tmp_path),
            "--follow",
            "--watch-interval",
            "0.01",
            "--watch-max-iterations",
            "1",
        ],
    )
    assert result.exit_code == EXIT_USAGE, result.output
    assert "log file not found" in result.stderr


# ---------------------------------------------------------------------------
# --job validation against .swarm-state.json.
# ---------------------------------------------------------------------------


def test_logs_job_id_mismatch_exits_usage(tmp_path: Path) -> None:
    """``--job`` mismatch with state.job_id is EXIT_USAGE."""
    _seed_events(tmp_path, count=1)
    write_state(
        tmp_path / SWARM_STATE_FILENAME,
        SwarmState(state="dispatching", job_id="job-001"),
    )
    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["logs", "--output", str(tmp_path), "--job", "job-999"],
    )
    assert result.exit_code == EXIT_USAGE, result.output
    assert "job_id mismatch" in result.stderr


def test_logs_job_id_match_passes(tmp_path: Path) -> None:
    """``--job`` matching state.job_id succeeds."""
    _seed_events(tmp_path, count=1)
    write_state(
        tmp_path / SWARM_STATE_FILENAME,
        SwarmState(state="dispatching", job_id="job-001"),
    )
    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["logs", "--output", str(tmp_path), "--job", "job-001"],
    )
    assert result.exit_code == EXIT_OK, result.output
    assert "worker_start" in result.stdout


def test_logs_without_state_file_skips_job_validation(tmp_path: Path) -> None:
    """A missing state file does not block --job validation.

    The log surface should still be readable for a partial run that
    crashed before state was written. --job is best-effort: without a
    state file, the check is a no-op and the dump proceeds.
    """
    _seed_events(tmp_path, count=1)
    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["logs", "--output", str(tmp_path), "--job", "anything"],
    )
    assert result.exit_code == EXIT_OK, result.output
    assert "worker_start" in result.stdout


# ---------------------------------------------------------------------------
# --output validation.
# ---------------------------------------------------------------------------


def test_logs_missing_output_dir_exits_usage(tmp_path: Path) -> None:
    """Non-existent ``--output`` directory yields EXIT_USAGE."""
    missing = tmp_path / "does-not-exist"
    runner = CliRunner()
    result = runner.invoke(
        swarm_group, ["logs", "--output", str(missing)]
    )
    assert result.exit_code == EXIT_USAGE, result.output
    assert "output directory not found" in result.stderr


# ---------------------------------------------------------------------------
# Parametrized smoke -- both surfaces dump cleanly in one-shot mode.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("flag", ["--md", "--jsonl"])
def test_logs_both_surfaces_dump_cleanly(tmp_path: Path, flag: str) -> None:
    """Both ``--md`` and ``--jsonl`` produce non-empty output and exit 0."""
    _seed_events(tmp_path, count=2)
    runner = CliRunner()
    result = runner.invoke(
        swarm_group, ["logs", "--output", str(tmp_path), flag]
    )
    assert result.exit_code == EXIT_OK, result.output
    assert result.stdout.strip(), f"expected non-empty stdout under {flag}"
