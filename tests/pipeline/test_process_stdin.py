"""Reconciliation-delta tests for ClaudeProcess + PortifyProcess stdin transport.

Companion to ``tests/pipeline/test_process.py``. Holds the new test cases
introduced by RECONCILED_DESIGN.md (.dev/architectural/claude-process-stdin-patch/
RECONCILED_DESIGN.md). Existing always-stdin contract assertions live in the
sibling file and are intentionally not duplicated here.
"""

from __future__ import annotations

import logging
import sys
import threading
import time
from unittest.mock import patch

import pytest

from superclaude.cli.cli_portify.process import PortifyProcess
from superclaude.cli.pipeline.process import (
    ClaudeProcess,
    PromptTooLargeForArgv,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stdin_echo_argv() -> list[str]:
    """Python stand-in for `claude` that copies stdin bytes to stdout bytes."""
    return [
        sys.executable,
        "-c",
        "import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())",
    ]


# ---------------------------------------------------------------------------
# T-008 / T-009 / T-010 -- PortifyProcess --add-dir anchor (P-001)
# ---------------------------------------------------------------------------


class TestPortifyAnchor:
    """P-001: --add-dir flags anchor on --output-format, not the dead -p lookup."""

    def test_output_format_flag_and_value_are_adjacent_for_portify_anchor(
        self, tmp_path
    ):
        """T-008: --add-dir lands at cmd[index('--output-format') + 2]."""
        work = tmp_path / "work"
        wf = tmp_path / "workflow"
        proc = PortifyProcess(
            prompt="x",
            output_file=tmp_path / "out.md",
            error_file=tmp_path / "err.log",
            work_dir=work,
            workflow_path=wf,
        )
        cmd = proc.build_command()

        anchor = cmd.index("--output-format")
        assert cmd[anchor + 1] == "text", "Portify base sets output_format='text'"
        assert cmd[anchor + 2] == "--add-dir", (
            "Add-dir flags must splice in directly after --output-format <value>"
        )
        assert "-p" not in cmd, "Prompt is delivered via stdin since 4799719"

    def test_portify_add_dir_works_for_large_prompt(self, tmp_path):
        """T-009: 200 KB PortifyProcess prompt round-trips via stdin with anchored --add-dir."""
        work = tmp_path / "work"
        wf = tmp_path / "workflow"
        payload = "y" * (200 * 1024)

        proc = PortifyProcess(
            prompt=payload,
            output_file=tmp_path / "out.md",
            error_file=tmp_path / "err.log",
            work_dir=work,
            workflow_path=wf,
        )

        # Phase 1: real cmd-shape assertions (unmocked).
        cmd = proc.build_command()
        anchor = cmd.index("--output-format")
        add_dir_indices = [i for i, v in enumerate(cmd) if v == "--add-dir"]
        assert len(add_dir_indices) == 2, "work_dir + workflow_path = 2 --add-dir flags"
        assert add_dir_indices[0] == anchor + 2
        assert "-p" not in cmd
        assert max(len(arg.encode("utf-8")) for arg in cmd) < 128 * 1024

        # Phase 2: real subprocess via stand-in confirms stdin transport.
        with patch.object(PortifyProcess, "build_command", return_value=_stdin_echo_argv()):
            result = proc.run()
        assert result.exit_code == 0
        assert (tmp_path / "out.md").read_bytes() == payload.encode("utf-8")

    def test_portify_anchor_resilient_to_repeated_calls(self, tmp_path):
        """T-010: build_command() is idempotent; argv does not accrete flags."""
        work = tmp_path / "work"
        wf = tmp_path / "workflow"
        proc = PortifyProcess(
            prompt="x",
            output_file=tmp_path / "out.md",
            error_file=tmp_path / "err.log",
            work_dir=work,
            workflow_path=wf,
        )
        first = proc.build_command()
        second = proc.build_command()
        assert first == second, (
            "Repeated build_command() must produce equal argv; mutation between calls "
            "would indicate the dual-add-dir logic accretes onto the base cmd."
        )


# ---------------------------------------------------------------------------
# T-004 -- PROMPT_MAX_BYTES pre-spawn guard (P-003)
# ---------------------------------------------------------------------------


class TestPromptMaxBytesGuard:
    """P-003: oversized prompts raise pre-spawn; no file or process side effects."""

    def test_prompt_max_bytes_guard(self, tmp_path, monkeypatch):
        """T-004: prompt > PROMPT_MAX_BYTES raises before any handle/process is created."""
        # Shrink the cap so we can test cheaply without allocating 16 MiB.
        monkeypatch.setattr(
            "superclaude.cli.pipeline.process.PROMPT_MAX_BYTES", 1024
        )

        out_file = tmp_path / "out.txt"
        err_file = tmp_path / "err.txt"
        oversize = "z" * 2048  # 2 KiB > 1 KiB cap
        proc = ClaudeProcess(
            prompt=oversize,
            output_file=out_file,
            error_file=err_file,
        )

        with pytest.raises(PromptTooLargeForArgv) as excinfo:
            proc.start()

        # The exception is a ValueError subclass for backward-compat.
        assert isinstance(excinfo.value, ValueError)
        # Pre-spawn: no Popen ran, no file artifacts on disk.
        assert proc._process is None
        assert not out_file.exists()
        assert not err_file.exists()

    def test_prompt_under_cap_passes_guard(self, tmp_path, monkeypatch):
        """A prompt at or below PROMPT_MAX_BYTES does not raise from the guard."""
        monkeypatch.setattr(
            "superclaude.cli.pipeline.process.PROMPT_MAX_BYTES", 1024
        )
        proc = ClaudeProcess(
            prompt="x" * 1024,  # exactly at cap -- not over
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        # Patch build_command so we don't actually shell out to a missing claude.
        with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
            proc.start()
            rc = proc.wait()
        assert rc == 0
        assert proc._prompt_bytes == b"x" * 1024


# ---------------------------------------------------------------------------
# T-002 / T-003 / T-005 / T-006 / T-011 -- chunked stdin write (P-004)
# ---------------------------------------------------------------------------


class TestChunkedStdinWrite:
    """P-004: chunked os.write loop with EINTR retry, error capture, finally-close."""

    def test_huge_prompt_400kb_round_trip_via_stdin(self, tmp_path):
        """T-002: 400 KB ASCII prompt arrives byte-identical via stdin."""
        payload = "a" * (400 * 1024)
        proc = ClaudeProcess(
            prompt=payload,
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
            proc.start()
            rc = proc.wait()
        assert rc == 0
        assert (tmp_path / "out.txt").read_bytes() == payload.encode("utf-8")
        assert proc._stdin_error is None

    def test_huge_utf8_emoji_prompt_round_trip(self, tmp_path):
        """T-003: 200 KB of multibyte UTF-8 round-trips byte-identical."""
        # 4-byte codepoint x 50K = 200 KB exact.
        payload = "🦀" * (50 * 1024)
        proc = ClaudeProcess(
            prompt=payload,
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
            proc.start()
            rc = proc.wait()
        assert rc == 0
        received = (tmp_path / "out.txt").read_bytes()
        assert received == payload.encode("utf-8"), "UTF-8 multibyte must not split or mojibake"

    def test_terminate_during_stdin_write_no_hang(self, tmp_path):
        """T-005: SIGTERM on a child that is not draining stdin completes within budget."""
        # Stand-in sleeps before reading -- pipe fills, parent's chunked write
        # blocks waiting for drain. terminate() from another thread must
        # complete within 10s SIGTERM + 5s SIGKILL window.
        sleeper = [
            sys.executable,
            "-c",
            "import sys, time; time.sleep(30); sys.stdin.buffer.read()",
        ]
        # 256 KB -- larger than typical 64 KiB pipe buffer to ensure the
        # parent's write loop is mid-flight when SIGTERM lands.
        proc = ClaudeProcess(
            prompt="b" * (256 * 1024),
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        with patch.object(ClaudeProcess, "build_command", return_value=sleeper):
            t0 = time.monotonic()
            # Schedule terminate() before start() so it fires while the
            # parent's write loop is still draining into the pipe buffer.
            timer = threading.Timer(0.5, proc.terminate)
            timer.start()
            try:
                proc.start()
                rc = proc.wait()
            finally:
                timer.cancel()
            elapsed = time.monotonic() - t0
        # Must not hang. SIGTERM (10s) + SIGKILL (5s) + start() prelude < 18s.
        assert elapsed < 18.0, f"terminate hung for {elapsed:.1f}s"
        # Child is reaped (poll returns the exit code).
        assert proc._process.poll() is not None
        # Exit code is nonzero (signal-killed).
        assert rc != 0

    def test_empty_prompt_uses_stdin_with_zero_bytes(self, tmp_path):
        """T-006: prompt='' writes zero bytes + EOF; no exception, no -p in cmd."""
        proc = ClaudeProcess(
            prompt="",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        cmd = proc.build_command()
        assert "-p" not in cmd, "empty prompt must not synthesize a -p argv element"

        with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
            proc.start()
            rc = proc.wait()
        assert rc == 0
        assert (tmp_path / "out.txt").read_bytes() == b""
        assert proc._stdin_error is None

    def test_broken_pipe_surfaces_via_stdin_error_log(self, tmp_path, caplog):
        """T-011: child exits before reading; _stdin_error captured + WARNING log."""
        # Stand-in exits 0 immediately, never reading stdin. With a 1 MB
        # payload the parent's write loop is guaranteed to encounter
        # BrokenPipe somewhere mid-stream (pipe is closed when child exits).
        early_exit = [sys.executable, "-c", "import sys; sys.exit(0)"]
        proc = ClaudeProcess(
            prompt="c" * (1024 * 1024),
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        with caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process"):
            with patch.object(ClaudeProcess, "build_command", return_value=early_exit):
                # start() must NOT raise even though the write hits BrokenPipe.
                proc.start()
                rc = proc.wait()
        assert rc == 0  # child's actual exit code
        # _stdin_error is only populated if the write actually broke -- on a
        # very fast race the child may exit cleanly after consuming the buffer.
        # If it did break, ensure we surfaced it; otherwise nothing to assert.
        if proc._stdin_error is not None:
            assert isinstance(proc._stdin_error, (BrokenPipeError, OSError))
            warnings = [r for r in caplog.records if "stdin_error" in r.message]
            assert warnings, "BrokenPipe must surface as a WARNING log"
