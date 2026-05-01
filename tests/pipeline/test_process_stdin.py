"""Reconciliation-delta tests for ClaudeProcess + PortifyProcess stdin transport.

Companion to ``tests/pipeline/test_process.py``. Holds the new test cases
introduced by RECONCILED_DESIGN.md (.dev/architectural/claude-process-stdin-patch/
RECONCILED_DESIGN.md). Existing always-stdin contract assertions live in the
sibling file and are intentionally not duplicated here.
"""

from __future__ import annotations

import sys
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
