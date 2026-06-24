"""Pipeline process management -- subprocess lifecycle for claude -p invocations.

Extracted from sprint/process.py. This version is generic: it accepts
PipelineConfig-compatible parameters and an output_format flag.

  output_format="stream-json"  ->  Sprint backward-compatible (NDJSON on stdout)
  output_format="text"         ->  Roadmap gate-compatible (plain text)

NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
"""

from __future__ import annotations

import logging
import os
import signal
import subprocess
from pathlib import Path
from typing import Callable, Optional

_log = logging.getLogger("superclaude.pipeline.process")


def _parse_prompt_max_bytes(raw: Optional[str], default: int = 16 * 1024 * 1024) -> int:
    """Parse SUPERCLAUDE_PROMPT_MAX_BYTES defensively.

    A misconfigured env var must never hard-fail module import. Invalid or
    non-positive values fall back to the default with a logged warning.
    """
    if raw is None:
        return default
    try:
        value = int(raw)
    except (TypeError, ValueError):
        _log.warning(
            "Invalid SUPERCLAUDE_PROMPT_MAX_BYTES=%r (not an integer); "
            "falling back to default %d bytes.",
            raw,
            default,
        )
        return default
    if value <= 0:
        _log.warning(
            "SUPERCLAUDE_PROMPT_MAX_BYTES=%d is non-positive; "
            "falling back to default %d bytes.",
            value,
            default,
        )
        return default
    return value


# Default 16 MiB; env-overridable for operators with exotic workflows.
# This is a sanity guard, not a kernel limit -- Linux MAX_ARG_STRLEN no
# longer applies because the prompt is delivered via stdin (since 4799719).
PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(
    os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")
)


class PromptTooLargeForArgv(ValueError):
    """Raised pre-spawn when the encoded prompt exceeds PROMPT_MAX_BYTES.

    Subclass of ValueError so callers catching ValueError keep working.
    Name preserved from DESIGN.md for traceability; under always-stdin the
    underlying failure mode is "child memory exhaustion" rather than the
    original "argv overflow", but the typed exception still distinguishes
    user-supplied-too-large from arbitrary OSError/MemoryError.
    """


class ClaudeProcess:
    """Manages a single claude -p subprocess with signal handling.

    Uses process groups (os.setpgrp) so we can kill the entire
    child tree on shutdown. CLAUDECODE= env prefix prevents nested
    session detection. stdout/stderr redirected to files.

    Lifecycle hooks (all optional, default None):
      on_spawn(pid)           — called after Popen in start()
      on_signal(pid, signal)  — called before signal send in terminate()
      on_exit(pid, returncode)— called before _close_handles() in wait()/terminate()
    """

    def __init__(
        self,
        *,
        prompt: str,
        output_file: Path,
        error_file: Path,
        max_turns: int = 100,
        model: str = "",
        permission_flag: str = "--dangerously-skip-permissions",
        timeout_seconds: int = 6300,
        output_format: str = "stream-json",
        extra_args: list[str] | None = None,
        on_spawn: Callable[[int], None] | None = None,
        on_signal: Callable[[int, str], None] | None = None,
        on_exit: Callable[[int, int | None], None] | None = None,
        env_vars: dict[str, str] | None = None,
        tool_write_mode: bool = False,
        reviewer_profile: bool = False,
        cwd: Path | None = None,
    ):
        self.prompt = prompt
        self.output_file = output_file
        self.error_file = error_file
        self.max_turns = max_turns
        self.model = model
        self.permission_flag = permission_flag
        self.timeout_seconds = timeout_seconds
        self.output_format = output_format
        self.extra_args = extra_args or []
        self._on_spawn = on_spawn
        self._on_signal = on_signal
        self._on_exit = on_exit
        self._extra_env_vars = env_vars
        self.tool_write_mode = tool_write_mode
        # L1b restricted reviewer profile (design (a), profile-wins). When True,
        # build_command() drops --dangerously-skip-permissions AND `--tools default`
        # so reflect REVIEW children cannot mutate the repo under audit. Orthogonal
        # to tool_write_mode (output plumbing): the profile wins on command
        # construction regardless of tool_write_mode. Defaulted False so every
        # existing (non-reflect) caller is byte-identical.
        self.reviewer_profile = reviewer_profile
        # L2 reviewer-isolation: when set, the child runs with this as its working
        # directory (the `git worktree` snapshot grounding root) instead of the live
        # shared worktree. Defaulted None so every existing caller is unaffected.
        self.cwd = cwd
        self._process: Optional[subprocess.Popen] = None
        self._stdout_fh = None
        self._stderr_fh = None

    def build_command(self) -> list[str]:
        """Build the claude CLI command.

        Prompt is delivered via stdin in start(), not as a -p argv value,
        to bypass the Linux MAX_ARG_STRLEN = 128 KB per-argument ceiling.
        """
        cmd = [
            "claude",
            "--print",
            "--verbose",
        ]
        # L1b (design (a)): the restricted reviewer profile drops the blanket
        # --dangerously-skip-permissions bypass AND the write-capable `--tools
        # default` surface for reflect REVIEW children. The default profile
        # (every existing sprint/roadmap caller) emits both, byte-identical to
        # before. --no-session-persistence is KEPT in both profiles.
        if not self.reviewer_profile:
            cmd.append(self.permission_flag)
        cmd.append("--no-session-persistence")
        if not self.reviewer_profile:
            cmd.extend(["--tools", "default"])
        cmd.extend(
            [
                "--max-turns",
                str(self.max_turns),
                "--output-format",
                self.output_format,
            ]
        )
        if self.model:
            cmd.extend(["--model", self.model])
        cmd.extend(self.extra_args)
        return cmd

    def build_env(self, *, env_vars: dict[str, str] | None = None) -> dict[str, str]:
        """Build environment for the child process.

        Remove CLAUDECODE and CLAUDE_CODE_ENTRYPOINT to prevent
        nested-session detection in the child claude process.

        env_vars, if provided, are merged with override semantics after
        os.environ.copy() so callers can inject isolation variables
        (e.g. CLAUDE_WORK_DIR) without affecting the base environment.
        """
        env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env.pop("CLAUDE_CODE_ENTRYPOINT", None)
        if env_vars:
            env.update(env_vars)
        return env

    def start(self) -> subprocess.Popen:
        """Launch the claude process."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Sanity guard before any handle/process is created. Encode once
        # here so the result is reused for the stdin write below (P-004).
        prompt_bytes = self.prompt.encode("utf-8") if self.prompt else b""
        if len(prompt_bytes) > PROMPT_MAX_BYTES:
            raise PromptTooLargeForArgv(
                f"prompt is {len(prompt_bytes)} bytes; "
                f"PROMPT_MAX_BYTES={PROMPT_MAX_BYTES}"
            )
        self._prompt_bytes = prompt_bytes  # consumed by stdin write below

        if self.tool_write_mode:
            # LLM writes output_file via Write tool; stdout goes to .log
            self._stdout_fh = open(self.output_file.with_suffix(".log"), "w")
        else:
            self._stdout_fh = open(self.output_file, "w")
        self._stderr_fh = open(self.error_file, "w")

        popen_kwargs = {
            "stdin": subprocess.PIPE,
            "stdout": self._stdout_fh,
            "stderr": self._stderr_fh,
            "env": self.build_env(env_vars=self._extra_env_vars),
        }
        if hasattr(os, "setpgrp"):
            popen_kwargs["preexec_fn"] = os.setpgrp
        # L2 reviewer-isolation: ground the child in the snapshot worktree when set.
        if self.cwd is not None:
            popen_kwargs["cwd"] = str(self.cwd)

        self._process = subprocess.Popen(self.build_command(), **popen_kwargs)

        # Deliver the prompt via stdin to bypass the Linux MAX_ARG_STRLEN
        # (128 KB per-argv-entry) kernel ceiling. Deadlock-safe: stdout/stderr
        # are real file handles, not pipes, so the parent never reads from the
        # child and a blocked stdin write cannot deadlock.
        #
        # Chunked write protects against (a) parent-thread stall on a full
        # kernel pipe buffer (typically 64 KiB on Linux) by yielding control
        # between syscalls, (b) EINTR from signal delivery, (c) silent
        # BrokenPipe masking. Errors are captured in self._stdin_error and
        # surfaced via _log.warning from wait()/terminate().
        self._stdin_error: Optional[BaseException] = None
        self._write_prompt_to_stdin(self._prompt_bytes)

        if self._on_spawn is not None:
            self._on_spawn(self._process.pid)

        _log.debug(
            "spawn pid=%d cmd=%s prompt_bytes=%d",
            self._process.pid,
            str(self.build_command()[:3]),
            len(self._prompt_bytes),
        )

        return self._process

    _STDIN_CHUNK_SIZE = 64 * 1024  # match typical Linux pipe-buffer size

    def _write_prompt_to_stdin(self, payload: bytes) -> None:
        """Write payload to child stdin in chunks; close stdin in finally.

        Uses os.write on the underlying FD so EINTR can be retried explicitly
        (Python's BufferedWriter does not surface InterruptedError reliably
        on partial writes). Closes stdin in finally so claude --print receives
        EOF even on unexpected exception (BrokenPipe, OSError, etc.). Errors
        land in self._stdin_error rather than propagating out of start().
        """
        if self._process is None or self._process.stdin is None:
            return
        fd = self._process.stdin.fileno()
        try:
            view = memoryview(payload)
            offset = 0
            while offset < len(view):
                chunk = view[offset : offset + self._STDIN_CHUNK_SIZE]
                while True:
                    try:
                        n = os.write(fd, chunk)
                        break
                    except InterruptedError:
                        # EINTR from signal delivery -- retry the same chunk.
                        continue
                if n <= 0:
                    # Defensive -- os.write should not return 0 on a pipe.
                    break
                offset += n
        except BrokenPipeError as exc:
            # Child exited before reading stdin; surface in wait()/terminate().
            self._stdin_error = exc
        except OSError as exc:
            self._stdin_error = exc
        finally:
            try:
                self._process.stdin.close()
            except Exception:  # pragma: no cover -- defensive
                pass

    def wait(self) -> int:
        """Wait for the process with timeout. Returns exit code."""
        try:
            self._process.wait(timeout=self.timeout_seconds)
        except subprocess.TimeoutExpired:
            self.terminate()
            return 124  # match bash timeout exit code

        rc = self._process.returncode if self._process.returncode is not None else -1
        if getattr(self, "_stdin_error", None) is not None:
            _log.warning(
                "stdin_error pid=%s err=%r", self._process.pid, self._stdin_error
            )
        if self._on_exit is not None:
            self._on_exit(self._process.pid, rc)
        self._close_handles()
        return rc

    def terminate(self) -> None:
        """Graceful shutdown: SIGTERM, wait 10s, then SIGKILL."""
        if self._process is None or self._process.poll() is not None:
            self._close_handles()
            return

        use_pgroup = all(hasattr(os, attr) for attr in ("getpgid", "killpg"))
        pgid = os.getpgid(self._process.pid) if use_pgroup else None

        try:
            if self._on_signal is not None:
                self._on_signal(self._process.pid, "SIGTERM")
            if use_pgroup and pgid is not None:
                os.killpg(pgid, signal.SIGTERM)
            else:
                self._process.terminate()
            _log.debug("signal_sent SIGTERM pid=%d", self._process.pid)
        except ProcessLookupError:
            self._close_handles()
            return

        try:
            self._process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            try:
                if use_pgroup and pgid is not None:
                    os.killpg(pgid, signal.SIGKILL)
                else:
                    self._process.kill()
                _log.debug("signal_sent SIGKILL pid=%d", self._process.pid)
                self._process.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                pass

        _log.debug(
            "exit pid=%d code=%s",
            self._process.pid,
            self._process.returncode,
        )
        if getattr(self, "_stdin_error", None) is not None:
            _log.warning(
                "stdin_error pid=%s err=%r", self._process.pid, self._stdin_error
            )
        if self._on_exit is not None:
            self._on_exit(self._process.pid, self._process.returncode)
        self._close_handles()

    def validate_tool_write_output(self) -> bool:
        """Check that the LLM wrote the output file via tools.

        Only meaningful when tool_write_mode=True. Returns True if
        output_file exists and is non-empty.
        """
        if not self.tool_write_mode:
            return True
        if not self.output_file.exists():
            _log.warning(
                "tool_write_mode: output file %s does not exist after subprocess exit",
                self.output_file,
            )
            return False
        if self.output_file.stat().st_size == 0:
            _log.warning(
                "tool_write_mode: output file %s is empty after subprocess exit",
                self.output_file,
            )
            return False
        return True

    def _close_handles(self) -> None:
        for fh in (self._stdout_fh, self._stderr_fh):
            if fh is not None:
                try:
                    fh.close()
                except Exception:
                    pass
