# Proposal A — Minimal Blast-Radius Patch: Pipe Large Prompts via stdin

**Author:** SuperClaude design pass
**Date:** 2026-04-30
**Target file:** `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/pipeline/process.py`
**Failure mode being fixed:** `OSError: [Errno 7] Argument list too long` raised by `execve()` when a single argv element (the prompt) exceeds Linux's `MAX_ARG_STRLEN = PAGE_SIZE * 32 = 131,072 bytes`. Observed in `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/roadmap/executor.py:749` when a step prompt embeds a 181 KB PRD plus a 157 KB TDD (~338 KB composed).

---

## 1. Summary

The base `ClaudeProcess` in `pipeline/process.py` passes the full prompt as a single `argv` element via the `-p <PROMPT>` flag (line 85-86). Any single argv element above `MAX_ARG_STRLEN` (128 KiB on Linux) is rejected by `execve(2)`, which is the bug currently breaking roadmap steps that inline-embed large input files. The fix is to drop the `-p <PROMPT>` pair from `argv` when the prompt is large and instead feed the prompt through the child's `stdin`, which the `claude` CLI already supports in `--print` mode (the positional prompt argument is documented as optional, with stdin used when it is omitted). The patch is local to `pipeline/process.py`. PortifyProcess remains compatible because its `--add-dir` insertion is keyed by *position before any prompt-bearing flag*, and we will preserve a stable insertion anchor. Backwards compatibility is preserved for all small prompts and for every existing constructor signature.

## 2. Decision Summary — Threshold-stdin (recommended)

**Three modes considered:**

| Mode | Pro | Con |
|---|---|---|
| **A. Always-stdin** | One code path, no branching, easiest to test | Subtle behavioral change for every existing caller; loses argv visibility in `ps`/`/proc`/log lines that currently grep prompts; harder to debug interactively (cannot copy/paste argv into a terminal); breaks any subclass or test that pattern-matches on `cmd.index("-p")` and expects a payload there. |
| **B. Threshold-stdin (recommended)** | Behavior unchanged for ~all current callers (every tasklist/validate/remediate path already gates at `_EMBED_SIZE_LIMIT = 120 KB` per `roadmap/executor.py:324`, well under the threshold); only the truly-large case (the bug) takes the new path; existing tests remain green. | Two paths to maintain. Threshold must be conservative. |
| **C. Opt-in flag (constructor kwarg)** | Surgical — only roadmap callers need to change | Forces every caller site to know about argv limits; defeats "minimal blast radius" in the calling code; future large prompts in untouched call sites still crash. |

**Recommendation: Mode B (threshold-stdin) with the threshold set at 96 KiB (`PROMPT_STDIN_THRESHOLD = 96 * 1024`).**

Rationale:
- The kernel hard limit on a single argv element is 128 KiB. Past callers already self-policed at 120 KiB (see `_EMBED_SIZE_LIMIT` derivation in `roadmap/executor.py:319-328`). Setting the stdin trigger at 96 KiB means: (a) every prompt that is currently legal stays on the legacy `-p` path; (b) prompts in the warning-zone (120 KiB+) and over-limit prompts (>128 KiB) automatically take the safe path; (c) we leave a 32 KiB margin for argv-environment-overhead so we never come close to `ARG_MAX` (~2 MiB total) issues either.
- Caller code does not change. The `_EMBED_SIZE_LIMIT` warning in `roadmap/executor.py:735-742` becomes purely advisory and the operation succeeds where it previously crashed.
- Subclass behavior is unchanged for the small-prompt case, which is every current PortifyProcess invocation (Portify prompts are short; they reference files via `--add-dir`).

## 3. Proposed Patch

### 3.1 Imports and module-level constants

**Before** (`pipeline/process.py:12-22`):
```python
from __future__ import annotations

import logging
import os
import signal
import subprocess
from pathlib import Path
from typing import Callable, Optional

_log = logging.getLogger("superclaude.pipeline.process")
```

**After:**
```python
from __future__ import annotations

import logging
import os
import signal
import subprocess
import threading
from pathlib import Path
from typing import Callable, Optional

_log = logging.getLogger("superclaude.pipeline.process")

# Linux MAX_ARG_STRLEN = PAGE_SIZE * 32 = 131,072 bytes. We pass the prompt
# via stdin once it crosses this conservative threshold, which leaves margin
# for the rest of argv, environment, and a small safety factor against
# kernel-version differences. Below the threshold we keep the legacy
# `-p <PROMPT>` form so behavior, ps(1) output, and tests are unchanged.
PROMPT_STDIN_THRESHOLD: int = 96 * 1024  # 98,304 bytes

# Maximum we will ever try to feed the child via stdin. Set generously high;
# the only purpose is to fail fast on pathological inputs (e.g., 1 GiB) so
# we don't sit forever blocked on a write. Override via env if needed.
PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))
```

### 3.2 `build_command()` — gate on prompt size, with a stable anchor

**Before** (`pipeline/process.py:71-91`):
```python
    def build_command(self) -> list[str]:
        """Build the claude CLI command."""
        cmd = [
            "claude",
            "--print",
            "--verbose",
            self.permission_flag,
            "--no-session-persistence",
            "--tools",
            "default",
            "--max-turns",
            str(self.max_turns),
            "--output-format",
            self.output_format,
            "-p",
            self.prompt,
        ]
        if self.model:
            cmd.extend(["--model", self.model])
        cmd.extend(self.extra_args)
        return cmd
```

**After:**
```python
    def _use_stdin_for_prompt(self) -> bool:
        """Return True iff the prompt is large enough to require stdin delivery.

        Encoded byte length matters (not character count); UTF-8 multibyte
        scripts can exceed the threshold even with short string len().
        """
        try:
            return len(self.prompt.encode("utf-8")) >= PROMPT_STDIN_THRESHOLD
        except (UnicodeEncodeError, AttributeError):
            # Treat as "large" — pushing through stdin avoids any argv-encoding
            # surprise the OS would otherwise hit on our behalf.
            return True

    def build_command(self) -> list[str]:
        """Build the claude CLI command.

        For small prompts (< PROMPT_STDIN_THRESHOLD bytes), the legacy
        ``-p <prompt>`` form is preserved verbatim so existing subclasses,
        tests, and operator workflows (ps/journalctl greps) are unaffected.

        For large prompts, ``-p`` and the prompt are omitted from argv;
        the prompt is delivered through stdin in ``start()``. The CLI is
        documented to read the prompt from stdin in ``--print`` mode when
        the positional prompt argument is absent.

        Subclasses that need to insert flags relative to the prompt should
        anchor on the sentinel returned by ``_prompt_anchor_flag()`` rather
        than literal ``"-p"``, since ``-p`` is no longer guaranteed to be
        present.
        """
        cmd = [
            "claude",
            "--print",
            "--verbose",
            self.permission_flag,
            "--no-session-persistence",
            "--tools",
            "default",
            "--max-turns",
            str(self.max_turns),
            "--output-format",
            self.output_format,
        ]
        if not self._use_stdin_for_prompt():
            cmd.extend(["-p", self.prompt])
        # else: prompt is fed via stdin in start(); --print already engaged.

        if self.model:
            cmd.extend(["--model", self.model])
        cmd.extend(self.extra_args)
        return cmd

    def _prompt_anchor_flag(self) -> str:
        """Return the argv element that subclasses should insert flags BEFORE.

        Stable across the small-prompt (-p path) and large-prompt (stdin path)
        modes. Always returns ``--output-format``, which is present in either
        case immediately preceding the prompt-delivery flags.

        Subclasses replace ``cmd.index("-p")`` with
        ``cmd.index(self._prompt_anchor_flag()) + 2`` (skip the flag and its
        value) to compute the safe insertion index.
        """
        return "--output-format"
```

### 3.3 `start()` — open stdin pipe, write the prompt, close it before wait

**Before** (`pipeline/process.py:110-137`):
```python
    def start(self) -> subprocess.Popen:
        """Launch the claude process."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        self._stdout_fh = open(self.output_file, "w")
        self._stderr_fh = open(self.error_file, "w")

        popen_kwargs = {
            "stdin": subprocess.DEVNULL,
            "stdout": self._stdout_fh,
            "stderr": self._stderr_fh,
            "env": self.build_env(env_vars=self._extra_env_vars),
        }
        if hasattr(os, "setpgrp"):
            popen_kwargs["preexec_fn"] = os.setpgrp

        self._process = subprocess.Popen(self.build_command(), **popen_kwargs)
        ...
```

**After:**
```python
    def start(self) -> subprocess.Popen:
        """Launch the claude process.

        For small prompts, stdin is DEVNULL (legacy behavior).
        For large prompts, stdin is a PIPE; we spawn a daemon thread that
        writes the prompt and closes the write end. Writing in a thread
        prevents deadlock if the child writes more to stderr than the OS
        pipe buffer (64 KB) holds before reading our stdin. (Stdout/stderr
        go to file FDs, not PIPE, so the only synchronous deadlock risk
        is on stdin itself if we tried to write a >64 KB prompt
        synchronously while the child was busy.)
        """
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Sanity check before spending FDs.
        prompt_bytes: bytes | None = None
        if self._use_stdin_for_prompt():
            prompt_bytes = self.prompt.encode("utf-8", errors="strict")
            if len(prompt_bytes) > PROMPT_MAX_BYTES:
                raise ValueError(
                    f"Prompt size {len(prompt_bytes)} bytes exceeds "
                    f"PROMPT_MAX_BYTES={PROMPT_MAX_BYTES}; refusing to spawn. "
                    f"Override via SUPERCLAUDE_PROMPT_MAX_BYTES env var."
                )

        self._stdout_fh = open(self.output_file, "w")
        self._stderr_fh = open(self.error_file, "w")

        popen_kwargs = {
            "stdin": subprocess.PIPE if prompt_bytes is not None else subprocess.DEVNULL,
            "stdout": self._stdout_fh,
            "stderr": self._stderr_fh,
            "env": self.build_env(env_vars=self._extra_env_vars),
        }
        if hasattr(os, "setpgrp"):
            popen_kwargs["preexec_fn"] = os.setpgrp

        self._process = subprocess.Popen(self.build_command(), **popen_kwargs)
        self._stdin_thread: threading.Thread | None = None
        self._stdin_error: BaseException | None = None

        if prompt_bytes is not None:
            # Background-write the prompt so we don't block start() on a
            # multi-MB write. The thread closes the write end when done,
            # giving the child EOF on stdin (claude requires EOF to begin
            # processing in --print mode).
            stdin_fh = self._process.stdin
            assert stdin_fh is not None  # narrow for type-checkers

            def _writer() -> None:
                try:
                    # Use os.write in a loop to handle short writes/EINTR.
                    fd = stdin_fh.fileno()
                    view = memoryview(prompt_bytes)
                    n = 0
                    total = len(view)
                    while n < total:
                        try:
                            written = os.write(fd, view[n:])
                        except BrokenPipeError:
                            # Child exited before consuming the prompt;
                            # exit code surfaces in wait().
                            break
                        except InterruptedError:
                            continue
                        if written == 0:
                            break
                        n += written
                except Exception as exc:  # noqa: BLE001 — diagnostic only
                    self._stdin_error = exc
                finally:
                    try:
                        stdin_fh.close()
                    except Exception:
                        pass

            self._stdin_thread = threading.Thread(
                target=_writer,
                name=f"claude-stdin-writer-{self._process.pid}",
                daemon=True,
            )
            self._stdin_thread.start()

        if self._on_spawn is not None:
            self._on_spawn(self._process.pid)

        _log.debug(
            "spawn pid=%d cmd=%s prompt_via=%s prompt_bytes=%d",
            self._process.pid,
            str(self.build_command()[:3]),
            "stdin" if prompt_bytes is not None else "argv",
            len(prompt_bytes) if prompt_bytes is not None else len(self.prompt),
        )

        return self._process
```

### 3.4 `wait()` and `terminate()` — join the writer thread

In `wait()` (line 139) and `terminate()` (line 153), add a `_join_stdin_writer()` call before `_close_handles()`:

```python
    def _join_stdin_writer(self, timeout: float = 5.0) -> None:
        """Best-effort join on the prompt-writer thread.

        Runs after process exit. The thread is a daemon, so leaks are
        bounded by interpreter lifetime; this just ensures the close()
        on stdin has happened before we tear down handles, and surfaces
        any write-side error to the log.
        """
        t = getattr(self, "_stdin_thread", None)
        if t is None:
            return
        t.join(timeout=timeout)
        if t.is_alive():
            _log.warning(
                "stdin writer thread did not exit within %.1fs (pid=%s)",
                timeout, self._process.pid if self._process else "?"
            )
        if self._stdin_error is not None:
            _log.warning("stdin writer error: %r", self._stdin_error)
```

Insert `self._join_stdin_writer()` immediately before `self._close_handles()` in:
- `wait()` (line 150)
- `terminate()` (line 194, both success and SIGKILL paths)

### 3.5 No constructor change

The public signature `ClaudeProcess(prompt: str, ...)` is unchanged. No new required args; no new optional args. Existing call sites at `roadmap/executor.py:749`, `roadmap/validate_executor.py:117`, `roadmap/remediate_executor.py:245`, `tasklist/executor.py:127`, `sprint/process.py:108` continue to work.

## 4. PortifyProcess Compatibility

The hard constraint is the override at `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/cli_portify/process.py:185-215`. It calls `super().build_command()`, then locates `cmd.index("-p")` and inserts `--add-dir` flags immediately before that index.

**Two scenarios:**

1. **Portify prompt < 96 KiB (the only case that exists today and the foreseeable case):** `super().build_command()` still contains `-p`, `cmd.index("-p")` succeeds, the existing logic is byte-for-byte unchanged. ✅

2. **Portify prompt ≥ 96 KiB (theoretical future case):** `super().build_command()` no longer contains `-p`. `cmd.index("-p")` raises `ValueError`. The existing code already handles this with `except ValueError: cmd.extend(add_dir_args)` (lines 209-213) — but appending `--add-dir` *after* `extra_args` is incorrect for `claude`'s flag-parsing semantics; flag ordering matters because `claude` interprets unknown trailing args as the prompt positional. The `extra_args` is currently empty for Portify in practice, so it's safe today, but fragile.

**Minimal subclass change (recommended, guarded one-liner):**

In `cli_portify/process.py:209-213`, replace:
```python
        try:
            p_idx = cmd.index("-p")
            cmd[p_idx:p_idx] = add_dir_args
        except ValueError:
            cmd.extend(add_dir_args)
```
with:
```python
        # Anchor on --output-format which is always present immediately before
        # the prompt-delivery flags (regardless of whether the prompt is on
        # argv via -p or fed via stdin). +2 skips the flag and its value.
        try:
            anchor = cmd.index(self._prompt_anchor_flag())
            insert_at = anchor + 2
        except ValueError:
            # _prompt_anchor_flag() (--output-format) is always present in
            # the base build_command(), so this branch is unreachable; kept
            # for defense-in-depth.
            insert_at = len(cmd)
        cmd[insert_at:insert_at] = add_dir_args
```

This change uses the new `_prompt_anchor_flag()` helper from §3.2, makes the Portify subclass robust to the stdin path, and is **two lines net change** in `cli_portify/process.py`. It is also strictly equivalent to the current behavior for all existing Portify invocations (both `-p` and `--output-format` are present, and `--add-dir` flags land in the same relative position because no other flag is between `--output-format <fmt>` and `-p` in `build_command()`).

If we want truly zero subclass change, we accept the second-scenario fragility. Given the recommendation is to land both diffs together (they total ~6 lines), I recommend the small subclass tweak.

## 5. Stdin Write Strategy

**Chosen approach: `Popen(stdin=PIPE)` + background daemon thread that writes & closes, then `wait()` then `_join_stdin_writer()`.**

### Why not `proc.communicate(input=prompt_bytes)`?
- `communicate()` insists on managing stdout/stderr too. Our stdout/stderr are already redirected to file FDs (which is a deliberate design — log persistence, tail viewers like `update_tail_pane()` in `sprint/executor.py:1248`). Calling `communicate()` after that setup either is a no-op for stdout/stderr (because they aren't PIPEs) or fights with our existing file-based redirection.
- `communicate()` also blocks the calling thread until the child exits, which would break the cancellation-polling pattern used at `roadmap/executor.py:763-775`, `validate_executor.py:131-140`, `tasklist/executor.py:141`, and `sprint/executor.py:1270`.

### Why not a temp-file + shell redirection (`bash -c 'claude ... < /tmp/promptfile'`)?
- Adds a shell process to every invocation and re-introduces argv-quoting concerns.
- Temp-file lifecycle becomes a cleanup-on-crash problem (covered for completeness in §6).
- No advantage on Linux: the OS pipe buffer is fine for our needs (see deadlock analysis below).

### Why not a synchronous write in the main thread before `wait()`?
- The OS pipe buffer is **64 KiB** on Linux. If the prompt is ≥64 KiB, `write()` will block until the child reads. The child is `claude`, which:
  1. Parses argv,
  2. Initializes,
  3. Starts reading stdin until EOF.
- During (1)-(2) the child can also write to stderr (banner, log lines). Stderr is a file FD on our side, **not a PIPE**, so child stderr writes never block on us. ✅
- However, if claude buffers stdin *internally* in chunks smaller than the prompt (e.g., reads 4KB at a time, processing each chunk), our synchronous main-thread write could still serialize 64KB-at-a-time. Not a deadlock, but it pessimizes start-up latency for multi-MB prompts.
- A daemon writer thread fully decouples us. The cost is one Python thread per active subprocess (negligible — there is exactly one active claude subprocess per executor at any time).

### The actual deadlock argument

The classic stdin/stdout PIPE deadlock requires both ends to fill simultaneously. Here:
- **stdin** (parent→child): can fill the 64 KiB OS buffer with our 338 KB prompt. Parent waits for child to drain.
- **stdout** (child→parent): goes to a regular file FD, not a PIPE. Cannot block the child.
- **stderr** (child→parent): goes to a regular file FD, not a PIPE. Cannot block the child.

So the child can never block on output, which means it will eventually drain stdin. **Therefore there is no deadlock with a synchronous write either** — the write will complete in O(prompt_size / read_chunk_size) syscalls. We use a thread anyway because: (a) it isolates a slow child's stdin-read from the parent's polling loop; (b) it keeps `start()` returning promptly so the cancellation-polling and TUI updates begin immediately; (c) it means the parent's signal handling continues to work the entire time, even for absurdly large prompts.

### Buffer ordering and EOF

`os.write(fd, buf)` is used over `stdin_fh.write()` to bypass Python's `io.BufferedWriter` flush logic and handle short writes / `EINTR` explicitly. After the loop, `stdin_fh.close()` issues the EOF that `claude --print` requires before it begins processing. Closing in `finally` guarantees EOF even on exception. Without EOF, `claude` will block reading stdin forever.

## 6. Edge Cases & Failure Modes

| # | Case | Mitigation |
|---|---|---|
| 1 | **SIGTERM mid-write.** The signal handler at `sprint/executor.py:1271` calls `proc_manager.terminate()`, which sends SIGTERM to the child's pgrp. The child dies; the parent's writer thread gets `BrokenPipeError` on its next `os.write`. | The `_writer` closure catches `BrokenPipeError` and exits cleanly; `_join_stdin_writer()` then joins the dead thread (immediate). No orphaned FDs; daemon=True ensures interpreter exit cannot hang on it. |
| 2 | **Short writes / EPIPE if claude crashes during write.** `os.write()` may return fewer bytes than requested under load. | The writer loop iterates until `n == total` and treats `BrokenPipeError` and `written == 0` as terminal conditions. The error is logged via `self._stdin_error` and surfaced in `_join_stdin_writer()`. The child's exit code (non-zero) is what callers actually check. |
| 3 | **Encoding (UTF-8 BOM, surrogates).** `self.prompt.encode("utf-8", errors="strict")` will raise `UnicodeEncodeError` on lone surrogates. | Strict encoding fails fast with a clear traceback at `start()` time, before fork. Better than silent corruption. If callers ever need lenient encoding we can add `errors="surrogateescape"` as an opt-in. BOM bytes (U+FEFF) round-trip fine; `claude` strips/handles them per its own input parser. |
| 4 | **Embedded NULs in prompt.** Argv-form (`-p <prompt>`) silently truncates at the first `\x00` because `execve` uses C strings. Stdin form preserves them. | This is a *latent improvement*: previously NUL-bearing prompts were silently truncated at arg-build time. The new path delivers them faithfully. If `claude` rejects NULs that's a CLI behavior, not our bug. Document this difference in the docstring. |
| 5 | **NamedTemporaryFile cleanup on crash.** | Not applicable — we do not use a temp file. The thread + PIPE approach has no on-disk state to leak. |
| 6 | **Windows portability.** Linux-only `os.setpgrp`, `os.killpg`, `os.getpgid` are already gated by `hasattr` checks (lines 123, 159). The stdin path uses `os.write` and `threading.Thread`, both portable; `subprocess.PIPE` works identically on Windows. | Patch is at least as portable as the current code. The threshold itself is Linux-driven (Windows `CreateProcess` has a different ~32 KiB limit on the *whole* command line, not per-arg) — Windows users would actually benefit from the stdin path triggering more eagerly, which they already get because their composed prompts hit the 96 KiB threshold sooner. |
| 7 | **Env var inheritance.** Unchanged — `build_env()` (line 93) is still called, still strips `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`. | No regression. |
| 8 | **Max prompt size sanity check.** A 1 GiB string would consume RAM and fork a doomed child. | New `PROMPT_MAX_BYTES` (default 16 MiB, `SUPERCLAUDE_PROMPT_MAX_BYTES`-overridable) raises `ValueError` before Popen. |
| 9 | **Threshold straddling.** A prompt at exactly 95 KiB takes argv path; at 96 KiB takes stdin. | Documented in the comment. The 32 KiB margin between the threshold and the kernel limit is large enough that no realistic prompt is at risk. Tests should cover both sides of the boundary (§7). |
| 10 | **Logging the prompt.** `_log.debug` previously hashed `cmd[:3]` only, so no leakage; we add `prompt_bytes=N` (size, not content) and `prompt_via=stdin|argv` for diagnostics. | No PII leakage delta. |
| 11 | **`ps`/`/proc/<pid>/cmdline` no longer shows the prompt** for the stdin path. | This is intentional — and arguably a security improvement (prompts can contain secrets pasted into PRDs/TDDs). Operators who currently grep for prompt fragments in process listings need to grep the output/error files instead, which were already the durable record of what was run (those files are written by `_stdout_fh`/`_stderr_fh`, see lines 114-115). Worth calling out in release notes. |
| 12 | **Re-entrancy of `start()`.** Currently undefined (would orphan the previous Popen). Patch does not change this. | Out of scope. |
| 13 | **Prompt mutated after construction.** `self.prompt` is read in both `_use_stdin_for_prompt()` and the writer thread. If a caller mutates `self.prompt` between `__init__` and `start()`, only the encoded copy in `prompt_bytes` is used by the writer. | Snapshot semantics: encode once, capture in closure, immune to subsequent mutations. |
| 14 | **`wait()` called without `start()`.** Existing bug, not introduced. | Out of scope. |

## 7. Test Plan

All tests live alongside existing pipeline tests. Use the project's `pytest` runner via `uv run pytest` (per global instructions).

### 7.1 Fixtures

```python
# tests/cli/pipeline/conftest.py (new)
@pytest.fixture
def mock_claude_bin(tmp_path: Path) -> Path:
    """A mock 'claude' that echoes its stdin to its stdout file and exits 0.

    Lets us assert end-to-end that the prompt was delivered, regardless
    of which path (argv vs stdin) was used.
    """
    script = tmp_path / "claude"
    script.write_text(
        "#!/usr/bin/env bash\n"
        "# Mock claude: dump argv to stderr, dump stdin to stdout.\n"
        "echo \"ARGV: $@\" >&2\n"
        "cat\n"
    )
    script.chmod(0o755)
    return script

@pytest.fixture
def small_prompt() -> str:
    return "hello world"  # ~11 bytes

@pytest.fixture
def boundary_prompt_under() -> str:
    # 95 KiB: stays on argv path
    return "x" * (95 * 1024)

@pytest.fixture
def boundary_prompt_over() -> str:
    # 97 KiB: takes stdin path
    return "y" * (97 * 1024)

@pytest.fixture
def huge_prompt() -> str:
    # 400 KiB: well over MAX_ARG_STRLEN; the failing-in-prod case
    return "z" * (400 * 1024)
```

### 7.2 Unit tests on `build_command()` and `_use_stdin_for_prompt()`

```python
def test_build_command_keeps_p_flag_for_small_prompt(small_prompt, tmp_path):
    proc = ClaudeProcess(prompt=small_prompt,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    cmd = proc.build_command()
    assert "-p" in cmd
    assert small_prompt in cmd

def test_build_command_omits_p_flag_for_large_prompt(huge_prompt, tmp_path):
    proc = ClaudeProcess(prompt=huge_prompt,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    cmd = proc.build_command()
    assert "-p" not in cmd
    assert huge_prompt not in cmd

def test_argv_total_byte_size_bounded_for_huge_prompt(huge_prompt, tmp_path):
    proc = ClaudeProcess(prompt=huge_prompt,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    cmd = proc.build_command()
    largest_arg = max(len(a.encode("utf-8")) for a in cmd)
    assert largest_arg < 128 * 1024, (
        f"At least one argv element is {largest_arg} bytes; this would "
        f"trigger E2BIG on execve.")

def test_threshold_boundary_under(boundary_prompt_under, tmp_path):
    proc = ClaudeProcess(prompt=boundary_prompt_under,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    assert not proc._use_stdin_for_prompt()

def test_threshold_boundary_over(boundary_prompt_over, tmp_path):
    proc = ClaudeProcess(prompt=boundary_prompt_over,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    assert proc._use_stdin_for_prompt()
```

### 7.3 End-to-end with mock claude binary

```python
def test_huge_prompt_delivered_via_stdin(huge_prompt, tmp_path, mock_claude_bin, monkeypatch):
    # Place mock on PATH ahead of any real claude
    monkeypatch.setenv("PATH", f"{mock_claude_bin.parent}:{os.environ['PATH']}")
    out, err = tmp_path / "out", tmp_path / "err"
    proc = ClaudeProcess(prompt=huge_prompt, output_file=out, error_file=err,
                        max_turns=1, output_format="text")
    proc.start()
    rc = proc.wait()
    assert rc == 0
    # Mock echoes stdin to stdout: prompt was delivered.
    assert out.read_text() == huge_prompt
    # Mock writes argv to stderr: confirm -p is absent.
    assert "-p " not in err.read_text()

def test_small_prompt_still_uses_argv(small_prompt, tmp_path, mock_claude_bin, monkeypatch):
    monkeypatch.setenv("PATH", f"{mock_claude_bin.parent}:{os.environ['PATH']}")
    out, err = tmp_path / "out", tmp_path / "err"
    proc = ClaudeProcess(prompt=small_prompt, output_file=out, error_file=err,
                        max_turns=1, output_format="text")
    proc.start()
    rc = proc.wait()
    assert rc == 0
    # Mock cats stdin (which is /dev/null in this path) → empty stdout.
    assert out.read_text() == ""
    # And -p shows up in the argv echo.
    assert "-p " in err.read_text()
```

### 7.4 Failure-mode tests

```python
def test_prompt_max_bytes_guard(tmp_path, monkeypatch):
    monkeypatch.setattr("superclaude.cli.pipeline.process.PROMPT_MAX_BYTES", 1024)
    proc = ClaudeProcess(prompt="a" * 2048,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    with pytest.raises(ValueError, match="exceeds PROMPT_MAX_BYTES"):
        proc.start()

def test_terminate_during_stdin_write_no_hang(huge_prompt, tmp_path, mock_claude_bin, monkeypatch):
    # Mock that sleeps before reading stdin so we can SIGTERM mid-write.
    slow = mock_claude_bin.parent / "claude"
    slow.write_text("#!/usr/bin/env bash\nsleep 30\ncat\n")
    monkeypatch.setenv("PATH", f"{slow.parent}:{os.environ['PATH']}")
    proc = ClaudeProcess(prompt=huge_prompt,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    proc.start()
    proc.terminate()
    assert proc._stdin_thread is None or not proc._stdin_thread.is_alive()
```

### 7.5 PortifyProcess regression

```python
def test_portify_add_dir_insertion_unchanged_for_small_prompt(tmp_path):
    proc = PortifyProcess(prompt="short", output_file=tmp_path / "o",
                         error_file=tmp_path / "e",
                         work_dir=tmp_path, workflow_path=tmp_path)
    cmd = proc.build_command()
    # --add-dir <work_dir> appears between --output-format and -p
    of_idx = cmd.index("--output-format")
    add_dir_idx = cmd.index("--add-dir")
    p_idx = cmd.index("-p")
    assert of_idx < add_dir_idx < p_idx

def test_portify_add_dir_insertion_works_for_large_prompt(tmp_path):
    proc = PortifyProcess(prompt="x" * (200 * 1024), output_file=tmp_path / "o",
                         error_file=tmp_path / "e",
                         work_dir=tmp_path, workflow_path=tmp_path)
    cmd = proc.build_command()
    assert "-p" not in cmd
    assert "--add-dir" in cmd
    of_idx = cmd.index("--output-format")
    add_dir_idx = cmd.index("--add-dir")
    # Insertion still after --output-format <value>
    assert add_dir_idx == of_idx + 2
```

## 8. Rollout / Patch-Delivery Mechanism

The package is installed via `pipx`, so editing `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/pipeline/process.py` directly works but is fragile (any `pipx upgrade` reverts it).

**Immediate-unblock recommendation: vendored monkey-patch in the project repo.**

Drop a small module under `/config/workspace/Coder/.dev/claude_process_stdin_patch.py` that, at import time, replaces `superclaude.cli.pipeline.process.ClaudeProcess.build_command` and `.start` with the patched versions. Wire it into the project entrypoint (e.g., a `sitecustomize.py` or a wrapper script) so any `superclaude` invocation from this repo gets the fix. Pros: immediate, reversible, survives `pipx upgrade` (the patch lives in the consumer repo). Cons: requires the entry point to import the patch module before any `superclaude` command runs — risk of "forgot to wire it up" errors if the user invokes the bare `superclaude` CLI.

**Durable-fix recommendation: upstream PR + wheel rebuild.**

Open a PR against the SuperClaude source repo (the source-of-truth path is `src/superclaude/cli/pipeline/process.py` per the user's global `CLAUDE.md`). Workflow:
1. Branch `fix/claude-process-stdin-large-prompts`.
2. Apply diffs from §3.1-3.4 to `src/superclaude/cli/pipeline/process.py` and the §4 tweak to `src/superclaude/cli/cli_portify/process.py`.
3. Add the §7 tests under `tests/cli/pipeline/`.
4. Run `make sync-dev`, `make verify-sync`, `make test`.
5. PR with proposal_a.md as the design doc.
6. After merge & release, `pipx upgrade superclaude` ships the fix everywhere.

Compared alternatives:
- **Wheel rebuild without upstream PR.** Builds a private wheel and `pipx install --force` from local. Works, but creates a fork and the next `pipx upgrade` stomps it. Use only if the upstream PR is rejected.
- **`sitecustomize.py` hook.** A `sitecustomize.py` placed in the pipx venv's `site-packages/` is auto-imported. Could install the monkey-patch globally. Pros: zero changes to call sites. Cons: invisible; future maintainers won't know it exists; pipx upgrade may or may not preserve it depending on packaging metadata. Discouraged.

**Recommended path: ship the monkey-patch today (§8 paragraph 2) and open the upstream PR in parallel (§8 paragraph 3). When the PR lands and a new release is cut, `pipx upgrade superclaude` makes the monkey-patch redundant; remove it then.**

## 9. Open Questions

1. **Does `claude --print` actually read prompt from stdin when the positional argument is omitted, on the version pinned by this venv?** The brief asserts this from the CLI's documented behavior, but no test in the current code base exercises it. **Required validation:** spawn `claude --print --tools default --max-turns 1 --output-format text` with a small prompt on stdin and confirm a sensible exit. If the CLI requires an empty positional `""` placeholder (some CLIs do), `build_command()` needs to keep `-p ""`. This is the single biggest unknown and should be the first thing verified before merging.
2. **Does `claude --print` require any specific stdin EOL or framing (e.g., final newline)?** The current argv form passes the prompt verbatim. The patch encodes verbatim and closes; if `claude` requires a trailing newline before EOF, prompts that previously worked may regress. Mitigation: append `b"\n"` defensively if testing reveals this.
3. **Should the threshold be configurable per-caller?** The brief asks for opt-in vs always vs threshold; we picked threshold. If a caller (e.g., a debug-run wrapper) wants to force the argv path for `ps`-grep-debugging, they currently can't. Adding a kwarg `force_prompt_via: Literal["auto", "argv", "stdin"] = "auto"` is a one-line extension if requested, but increases blast radius.
4. **What is the actual upper bound `claude` tolerates for stdin?** We chose `PROMPT_MAX_BYTES=16 MiB` somewhat arbitrarily. The CLI may have its own internal limits (token-window concerns aside). Worth probing.
5. **Is there a Windows user base?** If yes, the Windows `CMD.EXE` cmdline limit (~32 KiB total) means our 96 KiB threshold is effectively never reached on Windows because `claude` itself would already have failed at the call boundary. Patch is still safe (we just go to stdin earlier), but the threshold could be lowered on Windows for symmetry.
6. **Logging prompt size in production:** is `prompt_bytes=N` in debug logs acceptable, or do we need to gate it behind a verbosity level for sensitivity reasons? (Sizes are not content, but in some compliance contexts even sizes are signal.)
7. **Does any existing test mock `subprocess.Popen` and assert specifically on `cmd.index("-p")` or `cmd[-1] == prompt`?** A grep across the source tree before merging is cheap insurance. If yes, those tests will fail under the stdin path with large fixtures and need updating.

---

**End of Proposal A.**
