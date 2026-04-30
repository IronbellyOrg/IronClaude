<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (Proposal A — minimal-blast-radius) -->
<!-- Incorporated strengths: Variant 2 (Proposal B — typed errors, sidecar, streaming chunks, multibyte test, empty-prompt explicitness, risk-register format, line-range appendix) -->
<!-- Merge date: 2026-04-30 -->

# Unified Design — `ClaudeProcess` stdin-delivery patch for prompts > MAX_ARG_STRLEN

**Author:** SuperClaude /sc:adversarial merge
**Date:** 2026-04-30
**Target file:** `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/pipeline/process.py`
**Source of truth (per CLAUDE.md):** `src/superclaude/cli/pipeline/process.py`
**Failure mode being fixed:** `OSError: [Errno 7] Argument list too long` raised by `execve()` when a single argv element (the prompt) exceeds Linux's `MAX_ARG_STRLEN = PAGE_SIZE * 32 = 131,072 bytes`. Observed in `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/roadmap/executor.py:749` when a step prompt embeds a 181 KB PRD plus a 157 KB TDD (~338 KB composed).

---

## 1. Summary

<!-- Source: Base (original) -->
The base `ClaudeProcess` in `pipeline/process.py` passes the full prompt as a single `argv` element via `-p <PROMPT>` (line 85-86). Any single argv element above `MAX_ARG_STRLEN` (128 KiB on Linux) is rejected by `execve(2)`. The fix is to drop the `-p <PROMPT>` pair from `argv` when the encoded prompt size meets or exceeds `PROMPT_STDIN_THRESHOLD = 96 KiB`, and instead feed the prompt through the child's `stdin`, which `claude --print` reads when the positional prompt argument is omitted. The patch is local to `pipeline/process.py` plus a 2-line tweak in `cli_portify/process.py`. Backwards compatibility is preserved for all small prompts and for every existing constructor signature.

## 2. Decision Summary

<!-- Source: Base (original, modified) — adopt B's risk-register table format (Change #6) -->

**Threshold-stdin (selected from three candidate modes).** Below 96 KiB the legacy `-p <prompt>` argv form is preserved verbatim; at or above 96 KiB the prompt is delivered through the child's stdin.

| Mode                | Pro                                                                        | Con                                                                                                          |
|---------------------|----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Always-stdin        | Single code path                                                           | Behavior change for every caller; loses argv visibility in `ps`/log lines; breaks tests that pin argv shape   |
| Threshold-stdin ✓   | Behavior unchanged for ~all current callers; only the bug case takes the new path | Two paths to maintain; threshold must be conservative                                                          |
| Opt-in flag         | Surgical                                                                   | Forces every call site to know about argv limits; future large prompts in untouched call sites still crash   |

**Threshold:** `PROMPT_STDIN_THRESHOLD = 96 * 1024` bytes.

Rationale:
- Linux's per-arg `MAX_ARG_STRLEN` is 128 KiB. The 32 KiB margin accommodates other argv elements, environment-variable budget pressure on `ARG_MAX` (≈2 MiB total), and kernel-version drift.
- The existing `_EMBED_SIZE_LIMIT = 120 KB` warning at `roadmap/executor.py:319-328` operationalizes the same threshold concept; we land below it so the warning becomes purely advisory and the operation succeeds where it previously crashed.
- Empty prompts (size 0) explicitly stay on the argv path as `-p ""` to preserve legacy behavior. <!-- Source: Variant 2, Section 6 case 11 — merged per Change #5 -->

## 3. Proposed Patch

### 3.1 Imports, module-level constants, typed error

<!-- Source: Base (original, modified) — incorporate B's typed error (Change #1) -->

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
from typing import Callable, Iterator, Optional

_log = logging.getLogger("superclaude.pipeline.process")

# Linux MAX_ARG_STRLEN = PAGE_SIZE * 32 = 131,072 bytes (128 KiB). At or above
# this threshold we deliver the prompt via stdin instead of `-p <PROMPT>`,
# leaving margin for the rest of argv, environment, and a small safety factor
# against kernel-version differences. Below the threshold we keep the legacy
# `-p <PROMPT>` form so behavior, ps(1) output, and tests are unchanged.
PROMPT_STDIN_THRESHOLD: int = 96 * 1024  # 98,304 bytes

# Maximum we will ever try to feed the child via stdin. Set generously high;
# the only purpose is to fail fast on pathological inputs (e.g., 1 GiB) so we
# don't sit forever blocked on a write. Override via env if needed.
PROMPT_MAX_BYTES: int = int(
    os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024)
)


class PromptTooLargeForArgv(ValueError):
    """Raised when a caller forces argv-mode delivery on a prompt that
    would exceed the kernel's per-argument size limit. Replaces the
    generic OSError(7, "Argument list too long") with a typed exception
    that carries delivery-mode context.
    """
```

### 3.2 `build_command()` — gate on prompt size, with a stable anchor

<!-- Source: Base (original) -->

**Before** (`pipeline/process.py:71-91`):
```python
def build_command(self) -> list[str]:
    """Build the claude CLI command."""
    cmd = [
        "claude", "--print", "--verbose",
        self.permission_flag, "--no-session-persistence",
        "--tools", "default",
        "--max-turns", str(self.max_turns),
        "--output-format", self.output_format,
        "-p", self.prompt,
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
    scripts can exceed the threshold even with short string len(). Empty
    prompts (size 0) take the argv path (`-p ""`) to preserve legacy
    behavior; we never silently switch to stdin for empty strings.
    """
    try:
        size = len(self.prompt.encode("utf-8"))
    except (UnicodeEncodeError, AttributeError):
        # Treat as "large" — pushing through stdin avoids any argv-encoding
        # surprise the OS would otherwise hit on our behalf.
        return True
    if size == 0:
        return False
    return size >= PROMPT_STDIN_THRESHOLD

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
        "claude", "--print", "--verbose",
        self.permission_flag, "--no-session-persistence",
        "--tools", "default",
        "--max-turns", str(self.max_turns),
        "--output-format", self.output_format,
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

### 3.3 `start()` — open stdin pipe, stream prompt in chunks, close before wait

<!-- Source: Base (original, modified) — incorporate B's chunked streaming (Change #3) and prompt-sidecar (Change #2) -->

```python
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
    prompt_sidecar: bool = False,   # <-- NEW; opt-in observability for stdin mode
):
    # ... (existing fields unchanged) ...
    self._prompt_sidecar = prompt_sidecar


def _iter_prompt_chunks(self, chunk_size: int = 64 * 1024) -> Iterator[bytes]:
    """Encode and yield the prompt in chunks. Streams from the source
    string without materializing the full bytes in memory. Mid-codepoint
    boundaries are valid in a byte stream because the receiving side
    reassembles bytes; we slice the *string* by character index, encode
    each slice, and the receiver concatenates verbatim.
    """
    text = self.prompt
    n = len(text)
    i = 0
    # Slice by characters; encode each slice. For a 100 MB prompt this
    # holds at most chunk_size * ~4 bytes (UTF-8 worst case) in memory.
    char_chunk = max(1, chunk_size // 4)  # conservative for 4-byte UTF-8
    while i < n:
        yield text[i:i + char_chunk].encode("utf-8", errors="strict")
        i += char_chunk


def start(self) -> subprocess.Popen:
    """Launch the claude process.

    For small prompts (< PROMPT_STDIN_THRESHOLD), stdin is DEVNULL and
    the prompt rides argv via -p (legacy behavior).

    For large prompts, stdin is a PIPE; we spawn a daemon thread that
    streams the prompt and closes the write end. Streaming avoids holding
    the full encoded prompt in memory for very large composed inputs.
    Closing stdin is the EOF that `claude --print` requires before it
    begins processing; without close(), claude blocks reading stdin
    forever.

    Stdout/stderr are file FDs (not PIPEs), so the classic two-pipe
    deadlock does not apply: the child can never block on output, and
    therefore will eventually drain stdin.
    """
    self.output_file.parent.mkdir(parents=True, exist_ok=True)

    via_stdin = self._use_stdin_for_prompt()

    # Sanity check before spending FDs.
    prompt_total_bytes = 0
    if via_stdin:
        prompt_total_bytes = len(self.prompt.encode("utf-8"))
        if prompt_total_bytes > PROMPT_MAX_BYTES:
            raise PromptTooLargeForArgv(
                f"Prompt size {prompt_total_bytes} bytes exceeds "
                f"PROMPT_MAX_BYTES={PROMPT_MAX_BYTES}; refusing to spawn. "
                f"Override via SUPERCLAUDE_PROMPT_MAX_BYTES env var."
            )

    self._stdout_fh = open(self.output_file, "w")
    self._stderr_fh = open(self.error_file, "w")

    # Optional sidecar — operator-inspection record of what claude saw
    # when stdin mode hides the prompt from `ps` and the existing log.
    sidecar_fh = None
    if via_stdin and self._prompt_sidecar:
        sidecar_path = self.output_file.with_suffix(".prompt")
        sidecar_fh = open(sidecar_path, "wb")

    popen_kwargs = {
        "stdin": subprocess.PIPE if via_stdin else subprocess.DEVNULL,
        "stdout": self._stdout_fh,
        "stderr": self._stderr_fh,
        "env": self.build_env(env_vars=self._extra_env_vars),
    }
    if hasattr(os, "setpgrp"):
        popen_kwargs["preexec_fn"] = os.setpgrp

    self._process = subprocess.Popen(self.build_command(), **popen_kwargs)
    self._stdin_thread: threading.Thread | None = None
    self._stdin_error: BaseException | None = None

    if via_stdin:
        stdin_fh = self._process.stdin
        assert stdin_fh is not None  # narrow for type-checkers
        chunks = self._iter_prompt_chunks()

        def _writer() -> None:
            try:
                fd = stdin_fh.fileno()
                for chunk in chunks:
                    view = memoryview(chunk)
                    n = 0
                    total = len(view)
                    while n < total:
                        try:
                            written = os.write(fd, view[n:])
                        except BrokenPipeError:
                            return  # child exited early; surfaced via wait()
                        except InterruptedError:
                            continue
                        if written == 0:
                            return
                        n += written
                    if sidecar_fh is not None:
                        sidecar_fh.write(chunk)
            except Exception as exc:  # noqa: BLE001 — diagnostic only
                self._stdin_error = exc
            finally:
                try:
                    stdin_fh.close()
                except Exception:
                    pass
                if sidecar_fh is not None:
                    try:
                        sidecar_fh.close()
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
        "spawn pid=%d cmd=%s prompt_via=%s prompt_bytes=%d sidecar=%s",
        self._process.pid,
        str(self.build_command()[:3]),
        "stdin" if via_stdin else "argv",
        prompt_total_bytes if via_stdin else len(self.prompt),
        bool(sidecar_fh) if via_stdin else False,
    )

    return self._process
```

### 3.4 `wait()` and `terminate()` — join the writer thread

<!-- Source: Base (original) -->

```python
def _join_stdin_writer(self, timeout: float = 5.0) -> None:
    """Best-effort join on the prompt-writer thread. Runs after process
    exit. The thread is a daemon, so leaks are bounded by interpreter
    lifetime; this just ensures the close() on stdin has happened before
    we tear down handles, and surfaces any write-side error to the log.
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
- `wait()` (currently line 150)
- `terminate()` (currently line 194 — both success and SIGKILL paths)

### 3.5 No public constructor change beyond opt-in `prompt_sidecar`

The public signature `ClaudeProcess(prompt: str, ..., prompt_sidecar: bool = False)` adds **one** kwarg with a default value. Existing call sites at `roadmap/executor.py:749`, `roadmap/validate_executor.py:117`, `roadmap/remediate_executor.py:245`, `tasklist/executor.py:127`, `sprint/process.py:108` continue to work unmodified. Roadmap-family callers may opt into the sidecar by passing `prompt_sidecar=True` as a follow-up improvement.

## 4. PortifyProcess Compatibility

<!-- Source: Base (original) -->

The hard constraint is the override at `cli_portify/process.py:185-215`. It calls `super().build_command()`, then locates `cmd.index("-p")` and inserts `--add-dir` flags immediately before that index.

**Two scenarios:**

1. **Portify prompt < 96 KiB (the only case that exists today):** `super().build_command()` still contains `-p`, `cmd.index("-p")` succeeds, the existing logic is byte-for-byte unchanged.

2. **Portify prompt ≥ 96 KiB (theoretical future case):** `super().build_command()` no longer contains `-p`. `cmd.index("-p")` raises `ValueError`; existing fallback at lines 209-213 appends `--add-dir` *after* `extra_args`, which `claude` flag-parsing accepts but is fragile.

**Subclass change (2 lines net):**

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
# the prompt-delivery flags (regardless of whether the prompt is on argv
# via -p or fed via stdin). +2 skips the flag and its value.
try:
    anchor = cmd.index(self._prompt_anchor_flag())
    insert_at = anchor + 2
except ValueError:
    # _prompt_anchor_flag() (--output-format) is always present in the
    # base build_command(), so this branch is unreachable; kept for
    # defense-in-depth.
    insert_at = len(cmd)
cmd[insert_at:insert_at] = add_dir_args
```

This is strictly equivalent to the current behavior for all existing Portify invocations (both `-p` and `--output-format` are present, and `--add-dir` flags land in the same relative position because no flag is between `--output-format <fmt>` and `-p` in `build_command()`). It also makes Portify stdin-safe for the future large-prompt case.

A unit test pins the contract: `build_command()` must emit `--output-format` and its value as adjacent argv elements; if any future flag is inserted between them, CI catches the violation.

## 5. Stdin Write Strategy

<!-- Source: Base (original) -->

**Chosen approach:** `Popen(stdin=PIPE)` + background daemon thread that writes & closes, then `wait()` then `_join_stdin_writer()`.

### Why not `proc.communicate(input=prompt_bytes)`?
- `communicate()` insists on managing stdout/stderr too. Our stdout/stderr are already redirected to file FDs — log persistence, tail viewers like `update_tail_pane()` in `sprint/executor.py:1248`. `communicate()` would fight with our existing file-based redirection.
- `communicate()` blocks the calling thread until the child exits, breaking the cancellation-polling pattern at `roadmap/executor.py:763-775`, `validate_executor.py:131-140`, `tasklist/executor.py:141`, and `sprint/executor.py:1270`.

### Why not a synchronous in-thread write?
- The OS pipe buffer is **64 KiB** on Linux. If the prompt is ≥64 KiB, a synchronous `write()` blocks until the child reads.
- Stdout/stderr go to file FDs, **not PIPEs**, so the child can never block on output, which means it will eventually drain stdin. **No deadlock with synchronous write either** — the write completes in O(prompt_size / read_chunk_size) syscalls. We use a thread anyway because: (a) it isolates a slow child's stdin-read from the parent's polling loop; (b) it keeps `start()` returning promptly so cancellation-polling and TUI updates begin immediately; (c) signal handling continues to work the entire time, even for absurdly large prompts.

### Why streaming chunks rather than a single full-buffer encode?
<!-- Source: Variant 2, Section 5.3 — merged per Change #3 -->
For ordinary roadmap usage (~300 KB), full-buffer encode is fine. For audit-pipeline composition (multi-MB) or future workflows that compose larger inputs, full-buffer encode doubles peak heap. `_iter_prompt_chunks(64 KB)` streams; the writer thread feeds the kernel pipe at the kernel's own pace. Memory pressure stays at one chunk plus the kernel's 64 KB pipe buffer.

### EOF
`stdin_fh.close()` in `finally` is non-negotiable. `claude --print` requires EOF to begin processing. Closing in `finally` guarantees EOF even on exception.

## 6. Edge Cases & Failure Modes

<!-- Source: Base (original, modified) — adopt B's risk-register format and add B's UTF-8 / sidecar / TOCTOU coverage -->

| #  | Case                                                              | Mitigation                                                                                                                                                                                                                          |
|----|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | SIGTERM mid-write                                                 | Writer's `os.write` raises `BrokenPipeError`; caught and returned cleanly. `_join_stdin_writer(timeout=5)` joins; daemon=True bounds leak to interpreter lifetime                                                                       |
| 2  | Short writes / EPIPE if claude crashes during write               | Loop iterates until `n == total`; treats `BrokenPipeError` and `written == 0` as terminal; error logged via `self._stdin_error`. The child's exit code (non-zero) is what callers actually check                                       |
| 3  | UTF-8 BOM, surrogates, multibyte                                  | `errors="strict"` fails fast on lone surrogates. Multibyte chunks split mid-codepoint are valid in a byte stream — receiving side reassembles                                                                                          |
| 4  | Embedded NULs in prompt                                           | Argv path silently truncates at first `\x00` (execve uses C strings). Stdin path preserves them — latent improvement                                                                                                                  |
| 5  | NamedTemporaryFile cleanup on crash                               | N/A — no temp file used                                                                                                                                                                                                              |
| 6  | Windows portability                                               | Linux-only `os.setpgrp`/`os.killpg`/`os.getpgid` already gated by `hasattr` checks. `os.write`, `threading.Thread`, `subprocess.PIPE` all portable. Windows `CreateProcess` 32 KiB total cmdline limit means stdin path triggers more eagerly there |
| 7  | Env var inheritance                                               | Unchanged — `build_env()` (line 93) still strips `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`                                                                                                                                            |
| 8  | Max prompt size sanity check                                      | `PROMPT_MAX_BYTES` (default 16 MiB; `SUPERCLAUDE_PROMPT_MAX_BYTES`-overridable) raises `PromptTooLargeForArgv` before Popen                                                                                                            |
| 9  | Threshold straddling                                              | Documented: at exactly 95 KiB takes argv path; at 96 KiB takes stdin. Tests cover both sides of the boundary                                                                                                                            |
| 10 | Logging the prompt                                                | Existing `cmd[:3]` log unchanged. New fields `prompt_via`, `prompt_bytes`, `sidecar` are size/mode metadata, not content                                                                                                              |
| 11 | `ps`/`/proc/<pid>/cmdline` no longer shows prompt for stdin path  | Intentional — and arguably a security improvement. Operators who need to inspect what claude saw can opt in to the `prompt_sidecar=True` constructor kwarg                                                                            |
| 12 | Empty prompt                                                      | `_use_stdin_for_prompt()` returns False for size 0 → argv path with `-p ""` preserved                                                                                                                                                 |
| 13 | Prompt mutated after construction                                 | `self.prompt` is read in `_use_stdin_for_prompt()` and lazily in `_iter_prompt_chunks()`. If a caller mutates `self.prompt` between `__init__` and `start()`, the mutation is observed (caveat emptor; existing behavior unchanged) |
| 14 | Re-entrancy of `start()`                                          | Existing pre-condition (already undefined behavior); patch does not change                                                                                                                                                            |
| 15 | Sidecar disk usage                                                | Off by default. Roadmap callers should opt in only when needed. Cleanup follows `output_file` lifecycle                                                                                                                              |

## 7. Test Plan

<!-- Source: Base (original, modified) — incorporate B's UTF-8 multibyte test (Change #4) and explicit empty-prompt test (Change #5) -->

All tests live alongside existing pipeline tests under `tests/cli/pipeline/`. Run via `uv run pytest tests/cli/pipeline/test_claude_process_delivery.py -v` (per CLAUDE.md "Python Environment").

### 7.1 Fixtures

```python
# tests/cli/pipeline/conftest.py (new)
@pytest.fixture
def mock_claude_bin(tmp_path: Path) -> Path:
    """Mock claude that dumps argv to stderr and stdin to stdout."""
    script = tmp_path / "claude"
    script.write_text(
        "#!/usr/bin/env bash\n"
        "echo \"ARGV: $@\" >&2\n"
        "cat\n"
    )
    script.chmod(0o755)
    return script

@pytest.fixture
def small_prompt() -> str:
    return "hello world"

@pytest.fixture
def empty_prompt() -> str:
    return ""

@pytest.fixture
def boundary_prompt_under() -> str:
    return "x" * (95 * 1024)

@pytest.fixture
def boundary_prompt_over() -> str:
    return "y" * (97 * 1024)

@pytest.fixture
def huge_prompt() -> str:
    return "z" * (400 * 1024)

@pytest.fixture
def emoji_prompt() -> str:
    """200 KB UTF-8 prompt of 4-byte codepoints."""
    return "🦀" * 50_000
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
    """The patch's correctness invariant — no argv element approaches MAX_ARG_STRLEN."""
    proc = ClaudeProcess(prompt=huge_prompt,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    cmd = proc.build_command()
    largest_arg = max(len(a.encode("utf-8")) for a in cmd)
    assert largest_arg < 128 * 1024

def test_threshold_boundary_under(boundary_prompt_under, tmp_path):
    proc = ClaudeProcess(prompt=boundary_prompt_under,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    assert not proc._use_stdin_for_prompt()

def test_threshold_boundary_over(boundary_prompt_over, tmp_path):
    proc = ClaudeProcess(prompt=boundary_prompt_over,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    assert proc._use_stdin_for_prompt()

def test_empty_prompt_uses_argv_with_empty_p_value(empty_prompt, tmp_path):
    """Empty prompts preserve `-p ""` (legacy behavior); no silent stdin switch."""
    proc = ClaudeProcess(prompt=empty_prompt,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    assert not proc._use_stdin_for_prompt()
    cmd = proc.build_command()
    assert "-p" in cmd
    assert "" in cmd  # the empty prompt value
```

### 7.3 End-to-end with mock claude binary

```python
def test_huge_prompt_delivered_via_stdin(huge_prompt, tmp_path, mock_claude_bin, monkeypatch):
    monkeypatch.setenv("PATH", f"{mock_claude_bin.parent}:{os.environ['PATH']}")
    out, err = tmp_path / "out", tmp_path / "err"
    proc = ClaudeProcess(prompt=huge_prompt, output_file=out, error_file=err,
                        max_turns=1, output_format="text")
    proc.start()
    rc = proc.wait()
    assert rc == 0
    assert out.read_text() == huge_prompt
    assert "-p " not in err.read_text()

def test_small_prompt_still_uses_argv(small_prompt, tmp_path, mock_claude_bin, monkeypatch):
    monkeypatch.setenv("PATH", f"{mock_claude_bin.parent}:{os.environ['PATH']}")
    out, err = tmp_path / "out", tmp_path / "err"
    proc = ClaudeProcess(prompt=small_prompt, output_file=out, error_file=err,
                        max_turns=1, output_format="text")
    proc.start()
    rc = proc.wait()
    assert rc == 0
    assert out.read_text() == ""           # stdin = DEVNULL → empty
    assert "-p " in err.read_text()        # argv echo confirms -p

def test_huge_utf8_emoji_prompt_round_trip(emoji_prompt, tmp_path, mock_claude_bin, monkeypatch):
    """Multibyte UTF-8 chunk boundaries do not corrupt the prompt."""
    monkeypatch.setenv("PATH", f"{mock_claude_bin.parent}:{os.environ['PATH']}")
    out, err = tmp_path / "out", tmp_path / "err"
    proc = ClaudeProcess(prompt=emoji_prompt, output_file=out, error_file=err,
                        max_turns=1, output_format="text")
    proc.start()
    rc = proc.wait()
    assert rc == 0
    assert out.read_text() == emoji_prompt
```

### 7.4 Failure-mode tests

```python
def test_prompt_max_bytes_guard(tmp_path, monkeypatch):
    monkeypatch.setattr("superclaude.cli.pipeline.process.PROMPT_MAX_BYTES", 1024)
    proc = ClaudeProcess(prompt="a" * 2048,
                        output_file=tmp_path / "o", error_file=tmp_path / "e")
    with pytest.raises(PromptTooLargeForArgv, match="exceeds PROMPT_MAX_BYTES"):
        proc.start()

def test_terminate_during_stdin_write_no_hang(huge_prompt, tmp_path, mock_claude_bin, monkeypatch):
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
    assert add_dir_idx == of_idx + 2

def test_output_format_flag_and_value_are_adjacent(tmp_path):
    """Pin the contract that _prompt_anchor_flag() depends on."""
    proc = ClaudeProcess(prompt="x", output_file=tmp_path / "o",
                        error_file=tmp_path / "e", output_format="text")
    cmd = proc.build_command()
    of_idx = cmd.index("--output-format")
    assert cmd[of_idx + 1] == "text"  # value immediately follows flag
```

### 7.6 Sidecar test

```python
def test_prompt_sidecar_written_when_opted_in(huge_prompt, tmp_path, mock_claude_bin, monkeypatch):
    monkeypatch.setenv("PATH", f"{mock_claude_bin.parent}:{os.environ['PATH']}")
    out = tmp_path / "out"
    proc = ClaudeProcess(prompt=huge_prompt, output_file=out, error_file=tmp_path / "err",
                        prompt_sidecar=True, max_turns=1, output_format="text")
    proc.start()
    proc.wait()
    sidecar = out.with_suffix(".prompt")
    assert sidecar.exists()
    assert sidecar.read_bytes() == huge_prompt.encode("utf-8")

def test_no_sidecar_by_default(huge_prompt, tmp_path, mock_claude_bin, monkeypatch):
    monkeypatch.setenv("PATH", f"{mock_claude_bin.parent}:{os.environ['PATH']}")
    out = tmp_path / "out"
    proc = ClaudeProcess(prompt=huge_prompt, output_file=out, error_file=tmp_path / "err",
                        max_turns=1, output_format="text")
    proc.start()
    proc.wait()
    assert not out.with_suffix(".prompt").exists()
```

## 8. Rollout / Patch-Delivery Mechanism

<!-- Source: Base (original) -->

**Immediate-unblock recommendation: vendored monkey-patch in the project repo.**

Drop a small module under `/config/workspace/Coder/.dev/claude_process_stdin_patch.py` that, at import time, replaces `superclaude.cli.pipeline.process.ClaudeProcess.build_command` and `.start` with the patched versions. Wire it into the project entrypoint (e.g., a wrapper script for `superclaude`) so any invocation from this repo gets the fix. Pros: immediate, reversible, survives `pipx upgrade`. Cons: requires the entry point to import the patch module before any `superclaude` command runs.

**Durable-fix recommendation: upstream PR + wheel rebuild.**

Open a PR against the SuperClaude source repo (source-of-truth path: `src/superclaude/cli/pipeline/process.py` per the user's global `CLAUDE.md`). Workflow:
1. Branch `fix/claude-process-stdin-large-prompts`.
2. Apply diffs from §3.1-3.5 to `src/superclaude/cli/pipeline/process.py` and the §4 tweak to `src/superclaude/cli/cli_portify/process.py`.
3. Add the §7 tests under `tests/cli/pipeline/`.
4. Run `make sync-dev`, `make verify-sync`, `make test`.
5. PR with this merged design as the design doc.
6. After merge & release, `pipx upgrade superclaude` ships the fix everywhere.
7. Per CLAUDE.md "Validation should be done via the .github actions" — add a CI job that runs §7 against a fake `claude` shim. No one-off scripts.

**Recommended path: ship the monkey-patch today and open the upstream PR in parallel. When the PR lands and a new release is cut, `pipx upgrade superclaude` makes the monkey-patch redundant; remove it then.**

## 9. Risk Register & Open Questions

<!-- Source: Variant 2, Section 10 — risk register format merged per Change #6 -->

### 9.1 Risk Register (top 6, ranked likelihood × impact)

| # | Risk                                                                                          | L | I | Score | Mitigation                                                                                                                                                                          |
|---|-----------------------------------------------------------------------------------------------|---|---|-------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | **A-001 / INV-005**: pinned `claude` does not actually read stdin in `--print` mode when positional prompt is omitted | M | H | 6 | **P0 release-gate test**: `echo "respond OK" \| claude --print --tools default --max-turns 1 --output-format text`. If false, pivot to `--input-format=stream-json` framing or sentinel `-p ""` |
| 2 | PortifyProcess `cmd.index("-p")` raises ValueError for large Portify prompts (theoretical)    | L | M | 2 | §4 tweak anchors on `--output-format` instead; CI test covers both small and large Portify prompts                                                                                  |
| 3 | Writer thread leak if stdin close path is missed                                              | L | H | 3 | `try/finally close()` in writer; `_join_stdin_writer(timeout=5)` in both `wait()` and `terminate()`; daemon=True bounds leak                                                       |
| 4 | Prompt size explosion now that stdin "just works"                                             | M | M | 4 | `PROMPT_MAX_BYTES` cap (16 MiB default, env-overridable); `_log.debug` records `prompt_bytes` for monitoring                                                                         |
| 5 | claude CLI behavior change in a future Anthropic release                                      | L | H | 3 | Pin `claude` CLI version range. Sidecar file (when opted in) gives prompt replay capability                                                                                          |
| 6 | Sidecar file disk-bloat                                                                       | L | L | 1 | Off by default; opt-in via `prompt_sidecar=True`; document cleanup as operator responsibility in beat 1, automate in beat 2                                                         |

### 9.2 Open Questions (carry-forward)

1. **Does `claude --print` actually read prompt from stdin when the positional argument is omitted, on the version pinned by this venv?** **Required validation before merging** (Risk #1).
2. **Does `claude --print` require a specific stdin EOL or framing (e.g., final newline)?** Verify during the §9.1 Risk #1 probe.
3. **Should the threshold be configurable per-caller?** Current design says no. If a caller wants to force argv path for `ps`-grep-debugging, a follow-up `force_prompt_via: Literal["auto", "argv", "stdin"] = "auto"` kwarg is a one-line extension.
4. **Logging prompt size in production:** is `prompt_bytes=N` in debug logs acceptable, or do we need to gate it behind a verbosity level?
5. **Should `_EMBED_SIZE_LIMIT` warnings at call sites be downgraded to debug?** Defer until stdin path proves stable in production.

## 10. Beat-2 Follow-ups (deferred from this design)

These are **not** part of the immediate patch but are recorded so they don't get lost:

- Introduce `pre_prompt_args: list[str]` mechanism on `ClaudeProcess`; migrate `PortifyProcess` to set `_pre_prompt_args` instead of overriding `build_command()`.
- Consider promoting stdin to the default delivery for all prompts (not just >96 KiB) once observability sidecar is mature.
- Add `--input-format=stream-json` delivery for tool-use orchestration workflows.
- Automated cleanup policy for `.prompt` sidecars (TTL or per-pipeline rotation).
- Optional `PromptSource` Protocol if/when @file or stream-json delivery actually ships and a second concrete source is needed (until then it's premature abstraction).

## 11. Appendix — Cited Line Ranges

<!-- Source: Variant 2, Appendix A — merged per Change #7 -->

- `pipeline/process.py:71-91` — current `build_command` with `-p` argv.
- `pipeline/process.py:110-137` — `start()` with `stdin=DEVNULL`, `cmd[:3]` debug log.
- `pipeline/process.py:139-194` — `wait`/`terminate`/`_close_handles` lifecycle.
- `cli_portify/process.py:185-215` — `PortifyProcess.cmd.index("-p")` insertion.
- `sprint/process.py:88-121` — sprint subclass.
- `cleanup_audit/process.py:22-47` — audit subclass.
- `roadmap/executor.py:719-759` — primary caller, embed-size warning.
- `roadmap/validate_executor.py:100-127` — sibling caller, same shape.
- `tasklist/executor.py:115-137` — sibling caller, same shape.
- `roadmap/executor.py:319-328` — `_MAX_ARG_STRLEN = 128 * 1024`, `_EMBED_SIZE_LIMIT = 120 KB`.
- `sprint/executor.py:1248-1271` — TUI tail-pane updater + signal handler.
- `roadmap/executor.py:735-742` — composed-prompt size warning that is currently advisory-only.

---

**End of Unified Design.**
