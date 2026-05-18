"""Tests for pipeline/process.py -- ClaudeProcess output_format and command building."""

from __future__ import annotations

import sys
from unittest.mock import patch

from superclaude.cli.pipeline.process import ClaudeProcess


class TestClaudeProcessCommand:
    def test_default_output_format_stream_json(self, tmp_path):
        p = ClaudeProcess(
            prompt="test",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        assert p.output_format == "stream-json"
        cmd = p.build_command()
        idx = cmd.index("--output-format")
        assert cmd[idx + 1] == "stream-json"

    def test_text_output_format(self, tmp_path):
        p = ClaudeProcess(
            prompt="test",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
            output_format="text",
        )
        cmd = p.build_command()
        idx = cmd.index("--output-format")
        assert cmd[idx + 1] == "text"

    def test_required_flags(self, tmp_path):
        p = ClaudeProcess(
            prompt="hello",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        cmd = p.build_command()
        assert "claude" in cmd
        assert "--print" in cmd
        assert "--verbose" in cmd
        assert "--no-session-persistence" in cmd
        assert "--tools" in cmd
        assert "default" in cmd
        assert "--dangerously-skip-permissions" in cmd
        # Prompt is delivered via stdin, never as a -p argv value.
        assert "-p" not in cmd
        assert "hello" not in cmd

    def test_with_model(self, tmp_path):
        p = ClaudeProcess(
            prompt="test",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
            model="opus",
        )
        cmd = p.build_command()
        assert "--model" in cmd
        idx = cmd.index("--model")
        assert cmd[idx + 1] == "opus"

    def test_without_model(self, tmp_path):
        p = ClaudeProcess(
            prompt="test",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        cmd = p.build_command()
        assert "--model" not in cmd

    def test_extra_args(self, tmp_path):
        p = ClaudeProcess(
            prompt="test",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
            extra_args=["--file", "/tmp/spec.md"],
        )
        cmd = p.build_command()
        assert "--file" in cmd
        assert "/tmp/spec.md" in cmd

    def test_max_turns_in_command(self, tmp_path):
        p = ClaudeProcess(
            prompt="test",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
            max_turns=100,
        )
        cmd = p.build_command()
        idx = cmd.index("--max-turns")
        assert cmd[idx + 1] == "100"

    def test_tools_default_in_command(self, tmp_path):
        p = ClaudeProcess(
            prompt="test",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        cmd = p.build_command()
        assert "--tools" in cmd
        assert cmd[cmd.index("--tools") + 1] == "default"


class TestClaudeProcessEnv:
    def test_removes_claudecode_env(self, tmp_path):
        p = ClaudeProcess(
            prompt="test",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        with patch.dict(
            "os.environ", {"CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "cli"}
        ):
            env = p.build_env()
            assert "CLAUDECODE" not in env
            assert "CLAUDE_CODE_ENTRYPOINT" not in env


class TestClaudeProcessStreamJsonCompat:
    """Verify stream-json output produces identical subprocess args to sprint."""

    def test_stream_json_matches_sprint_flags(self, tmp_path):
        p = ClaudeProcess(
            prompt="/sc:task-unified test prompt",
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
            max_turns=50,
            output_format="stream-json",
            permission_flag="--dangerously-skip-permissions",
        )
        cmd = p.build_command()

        # These flags must all be present for sprint compatibility
        assert cmd[0] == "claude"
        assert "--print" in cmd
        assert "--verbose" in cmd
        assert "--dangerously-skip-permissions" in cmd
        assert "--no-session-persistence" in cmd
        assert "--tools" in cmd
        assert "default" in cmd
        assert "--output-format" in cmd
        idx = cmd.index("--output-format")
        assert cmd[idx + 1] == "stream-json"
        assert "--max-turns" in cmd
        idx2 = cmd.index("--max-turns")
        assert cmd[idx2 + 1] == "50"


class TestClaudeProcessStdinDelivery:
    """Prompt is delivered via stdin, not argv.

    Replaces the legacy ``-p <prompt>`` transport, which tripped the Linux
    MAX_ARG_STRLEN = 128 KB per-argv-entry ceiling. Stdin has no such limit.
    """

    def _patch_claude_binary(self, cmd_override: list[str]):
        """Patch build_command() to return a Python-based stand-in for `claude`."""
        return patch.object(ClaudeProcess, "build_command", return_value=cmd_override)

    def test_build_command_excludes_prompt(self, tmp_path):
        """-p and the prompt value must never appear in argv."""
        prompt = "Do the thing.\nWith a multi-line body."
        p = ClaudeProcess(
            prompt=prompt,
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        cmd = p.build_command()
        assert "-p" not in cmd
        assert prompt not in cmd
        # No element of cmd should equal the prompt (defensive — covers partial escape).
        assert not any(arg == prompt for arg in cmd)

    def test_start_writes_prompt_to_stdin(self, tmp_path):
        """Child process receives the prompt byte-for-byte on stdin."""
        prompt = "Hello from stdin!\nLine 2."
        stand_in = [
            sys.executable,
            "-c",
            "import sys; sys.stdout.write(sys.stdin.read())",
        ]
        p = ClaudeProcess(
            prompt=prompt,
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        with self._patch_claude_binary(stand_in):
            p.start()
            rc = p.wait()
        assert rc == 0
        assert (tmp_path / "out.txt").read_text(encoding="utf-8") == prompt

    def test_stdin_handles_large_payload(self, tmp_path):
        """A 200 KB prompt — historical crash size — is delivered without OSError."""
        payload = "x" * (200 * 1024)  # 200 KB, above old 128 KB execve ceiling
        stand_in = [
            sys.executable,
            "-c",
            "import sys; sys.stdout.write(sys.stdin.read())",
        ]
        p = ClaudeProcess(
            prompt=payload,
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        with self._patch_claude_binary(stand_in):
            p.start()
            rc = p.wait()
        assert rc == 0
        received = (tmp_path / "out.txt").read_text(encoding="utf-8")
        assert len(received) == len(payload)
        assert received == payload

    def test_broken_pipe_tolerated(self, tmp_path):
        """Child exits before reading stdin — parent must not raise."""
        # Child exits immediately with rc=0 and ignores stdin.
        stand_in = [sys.executable, "-c", "import sys; sys.exit(0)"]
        p = ClaudeProcess(
            prompt="a" * (1024 * 1024),  # 1 MB — forces the write to flush real bytes
            output_file=tmp_path / "out.txt",
            error_file=tmp_path / "err.txt",
        )
        with self._patch_claude_binary(stand_in):
            # Must not raise BrokenPipeError out of start().
            p.start()
            rc = p.wait()
        assert rc == 0


class TestClaudeProcessOutputFileCollision:
    """C2 — Per-task subprocesses must NOT overwrite each other. The fix
    introduces `SprintConfig.task_output_file(phase, task)` /
    `task_error_file(phase, task)` helpers that produce per-task paths.
    This test exercises that machinery end-to-end with real subprocesses.
    """

    def _patch_claude_binary(self, cmd_override):
        return patch.object(ClaudeProcess, "build_command", return_value=cmd_override)

    def test_two_starts_distinct_output_files_preserve_both_outputs(self, tmp_path):
        from superclaude.cli.sprint.models import Phase, SprintConfig, TaskEntry

        phase = Phase(number=2, file=tmp_path / "phase-2-tasklist.md")
        phase.file.write_text("# Phase 2\n")
        index = tmp_path / "tasklist-index.md"
        index.write_text("- phase-2-tasklist.md\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[phase],
            start_phase=2,
            end_phase=2,
            max_turns=5,
        )

        task_a = TaskEntry(task_id="T02.01", title="A", description="d")
        task_b = TaskEntry(task_id="T02.02", title="B", description="d")

        # C2 helpers must produce distinct paths — this is the assertion the
        # test is load-bearing on (helpers from models.py:475-479).
        out_a = config.task_output_file(phase, task_a)
        out_b = config.task_output_file(phase, task_b)
        err_a = config.task_error_file(phase, task_a)
        err_b = config.task_error_file(phase, task_b)
        assert out_a != out_b, "task_output_file produced identical paths for distinct tasks"
        assert err_a != err_b, "task_error_file produced identical paths for distinct tasks"

        config.results_dir.mkdir(parents=True, exist_ok=True)

        stand_in = [
            sys.executable,
            "-c",
            "import sys; sys.stdout.write(sys.stdin.read())",
        ]

        p_a = ClaudeProcess(
            prompt="AAA",
            output_file=out_a,
            error_file=err_a,
        )
        p_b = ClaudeProcess(
            prompt="BBB",
            output_file=out_b,
            error_file=err_b,
        )

        with self._patch_claude_binary(stand_in):
            p_a.start()
            rc_a = p_a.wait()
            p_b.start()
            rc_b = p_b.wait()

        assert rc_a == 0
        assert rc_b == 0
        text_a = out_a.read_text(encoding="utf-8")
        text_b = out_b.read_text(encoding="utf-8")
        assert text_a == "AAA", f"Expected AAA in out_a, got {text_a!r}"
        assert text_b == "BBB", f"Expected BBB in out_b, got {text_b!r}"
        # Cross-contamination guard — proves per-task path resolution prevented collision
        assert "BBB" not in text_a
        assert "AAA" not in text_b
