# Proposal B — Robust, future-proof redesign of `ClaudeProcess` prompt delivery

> Design-only. No package files modified. Target source of truth at proposal
> time:
> `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/cli/pipeline/process.py`
> (`ClaudeProcess`, lines 24-203).

---

## 1. Summary

The current `ClaudeProcess` couples **prompt content** to **argv layout** by passing
the prompt as the value of `-p` (see `process.py:85-86`). Linux caps a single
argv element at `MAX_ARG_STRLEN = PAGE_SIZE * 32 = 128 KiB`, so `execve()`
fails (`OSError: [Errno 7] Argument list too long`) once a roadmap step embeds a
PRD (~181 KB) plus a TDD (~157 KB). Proposal B replaces the argv-bound prompt
with a `PromptSource` abstraction and a small **delivery-strategy** layer.
Default delivery becomes **stdin streaming via `Popen(stdin=PIPE)`** (Anthropic
documents `claude -p` as "useful for pipes" — when the positional `prompt` is
omitted, claude reads stdin); a `@file` indirection strategy is available for
trustless / observable cases. Backwards compatibility is preserved: every existing
caller passing `prompt=str` keeps working unchanged, and `PortifyProcess`'s
"insert `--add-dir` before `-p`" override evolves into a structured hook that no
longer depends on the literal `-p` token being in argv.

---

## 2. Architectural framing

**Today (`process.py:71-91`):**

```python
def build_command(self) -> list[str]:
    cmd = [..., "-p", self.prompt]   # prompt is argv element
    cmd.extend(self.extra_args)
    return cmd
```

`self.prompt` is a `str` that travels through `subprocess.Popen` directly into
`execve(2)`. The kernel's argv strlen check fires **before any of our Python
code can react**, so `try/except OSError` around `Popen` is the only failure
mode and we lose the run.

`roadmap/executor.py:735-742`, `validate_executor.py:104-110`, and
`tasklist/executor.py:115-120` already log a warning when the composed prompt
exceeds `_EMBED_SIZE_LIMIT` (120 KB) but *cannot do anything about it* —
because the abstraction below them only knows how to deliver via argv.

**Missing abstraction.** There is no notion of *how* a prompt is delivered to
the child. Today: `prompt: str` → argv. We need:

- **`PromptSource`** — a typed value object that knows the prompt's bytes (or a
  way to materialize them: literal string, generator, file path, captured
  artifact, future JSON tool input) and its size.
- **`PromptDelivery` strategy** — given a `PromptSource`, return:
    1. the argv mutations required (e.g. `["-p", literal]`, or `[]` if stdin),
    2. a `Popen` stdin disposition (`DEVNULL`, `PIPE`, or a file handle),
    3. a "post-spawn" callable that writes the bytes (no-op for argv).

This is the **smallest** addition that fixes the root cause — argv coupling —
rather than the symptom (a 128 KB prompt). It also gives us a natural seam for
the planned migration to `--input-format=stream-json` (a sequence of JSON tool
input objects on stdin), which will *only* ever be a stdin/file delivery.

---

## 3. Proposed design

### 3.1 New types (additive, in `pipeline/process.py`)

```python
# pipeline/prompt_source.py  (new module, kept tiny so imports stay cheap)

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol, Union

# --- The contract ---------------------------------------------------------

class PromptSource(Protocol):
    """A prompt that knows how to feed itself to a child process."""
    @property
    def size_bytes(self) -> int: ...
    def iter_chunks(self, chunk_size: int = 64 * 1024) -> Iterable[bytes]: ...
    def to_str(self) -> str:
        """Materialize the full prompt as text (for logging digests, tests)."""
        ...

# --- Concrete sources -----------------------------------------------------

@dataclass(frozen=True)
class StringPrompt:
    text: str
    @property
    def size_bytes(self) -> int:
        return len(self.text.encode("utf-8"))
    def iter_chunks(self, chunk_size: int = 64 * 1024):
        data = self.text.encode("utf-8")
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
    def to_str(self) -> str:
        return self.text

@dataclass(frozen=True)
class FilePrompt:
    path: Path
    @property
    def size_bytes(self) -> int:
        return self.path.stat().st_size
    def iter_chunks(self, chunk_size: int = 64 * 1024):
        with self.path.open("rb") as fh:
            while True:
                buf = fh.read(chunk_size)
                if not buf:
                    return
                yield buf
    def to_str(self) -> str:
        return self.path.read_text(encoding="utf-8", errors="replace")

# --- Delivery strategy ----------------------------------------------------

# Hard kernel limit; leave 1 KB headroom for argv-other elements.
ARGV_INLINE_BUDGET = 127 * 1024  # bytes, conservative under 128 KiB

@dataclass
class DeliveryPlan:
    """How a PromptSource will reach the child process."""
    mode: str                      # "argv" | "stdin" | "file"
    argv_for_prompt: list[str]     # what to splice into command, e.g. ["-p", "..."] or []
    stdin_disposition: object      # subprocess.DEVNULL | subprocess.PIPE | file handle
    write_after_spawn: bool        # True iff caller must write to child's stdin

class PromptDelivery(Protocol):
    def plan(self, source: PromptSource) -> DeliveryPlan: ...
    def write(self, source: PromptSource, child_stdin) -> None: ...

class StdinDelivery:
    """Default. Writes prompt to claude's stdin; argv carries no prompt."""
    def plan(self, source):
        return DeliveryPlan(
            mode="stdin",
            argv_for_prompt=[],          # no -p; claude reads stdin
            stdin_disposition=subprocess.PIPE,
            write_after_spawn=True,
        )
    def write(self, source, child_stdin):
        try:
            for chunk in source.iter_chunks():
                child_stdin.write(chunk)
        finally:
            try:
                child_stdin.close()
            except BrokenPipeError:
                pass  # claude exited early; surfaced via wait()

class ArgvDelivery:
    """Legacy / small-prompt path. Used when source.size_bytes <= ARGV_INLINE_BUDGET
    AND the caller explicitly opts in; not the default."""
    def plan(self, source):
        return DeliveryPlan(
            mode="argv",
            argv_for_prompt=["-p", source.to_str()],
            stdin_disposition=subprocess.DEVNULL,
            write_after_spawn=False,
        )
    def write(self, source, child_stdin):
        return  # no-op

class AutoDelivery:
    """Picks argv if it fits the budget, otherwise stdin. Default for the public
    API so the existing 'small prompt' shape (sprint, audit) does not change
    observable behavior unless it has to."""
    def __init__(self, *, budget: int = ARGV_INLINE_BUDGET):
        self._budget = budget
    def plan(self, source):
        if source.size_bytes <= self._budget:
            return ArgvDelivery().plan(source)
        return StdinDelivery().plan(source)
    def write(self, source, child_stdin):
        StdinDelivery().write(source, child_stdin)
```

> **Why a strategy and not just "always stdin"?** Two reasons. (1) Existing
> debug logs and sprint debug hooks log argv slices (`process.py:131-135`,
> `sprint/process.py:42-47`); flipping every small-prompt sprint phase to
> stdin would silently change observability for everything, not just the
> roadmap callers that need it. (2) Some future workflows want a pure pipe
> (no `-p` at all), and others want `claude --resume` style operations where
> `-p` carries a small directive and the *body* arrives on stdin. The
> strategy makes both expressible without further refactor.

### 3.2 Refactored `ClaudeProcess.start()` (sequence)

```
start(self):
    1. ensure output_file.parent exists
    2. open self._stdout_fh / self._stderr_fh on output_file / error_file
    3. source   := self._prompt_source            # built in __init__
    4. delivery := self._delivery                  # AutoDelivery() by default
    5. plan     := delivery.plan(source)
    6. cmd      := self.build_command(plan=plan)   # NOTE the new kwarg
    7. popen_kwargs:
         stdin  = plan.stdin_disposition
         stdout = self._stdout_fh
         stderr = self._stderr_fh
         env    = self.build_env(...)
         preexec_fn = os.setpgrp
    8. self._process := Popen(cmd, **popen_kwargs)
    9. on_spawn(pid)
   10. _log_spawn(pid, cmd, plan, source)         # see §7
   11. if plan.write_after_spawn:
           self._writer_thread := Thread(
               target=delivery.write, args=(source, self._process.stdin),
               name=f"claude-stdin-{pid}", daemon=True)
           self._writer_thread.start()
   12. return self._process
```

`build_command()` becomes:

```python
def build_command(self, *, plan: DeliveryPlan | None = None) -> list[str]:
    plan = plan or AutoDelivery().plan(self._prompt_source)
    cmd = [
        "claude", "--print", "--verbose",
        self.permission_flag, "--no-session-persistence",
        "--tools", "default",
        "--max-turns", str(self.max_turns),
        "--output-format", self.output_format,
    ]
    cmd.extend(plan.argv_for_prompt)         # [] for stdin/file, ["-p", text] for argv
    if self.model:
        cmd.extend(["--model", self.model])
    cmd.extend(self.extra_args)
    return cmd
```

`wait()` and `terminate()` are unchanged in shape but gain one detail (§5):
both `join()` the writer thread (with a small bounded timeout) before closing
file handles to avoid leaking the pipe writer.

### 3.3 New `__init__` signature (additive only)

```python
def __init__(
    self,
    *,
    prompt: str | PromptSource,                  # str remains accepted
    output_file: Path,
    error_file: Path,
    max_turns: int = 100,
    model: str = "",
    permission_flag: str = "--dangerously-skip-permissions",
    timeout_seconds: int = 6300,
    output_format: str = "stream-json",
    extra_args: list[str] | None = None,
    on_spawn=None, on_signal=None, on_exit=None,
    env_vars: dict[str, str] | None = None,
    delivery: PromptDelivery | None = None,      # NEW; default = AutoDelivery()
):
    if isinstance(prompt, str):
        self._prompt_source: PromptSource = StringPrompt(prompt)
        self.prompt = prompt                     # kept for backwards compat / tests
    else:
        self._prompt_source = prompt
        self.prompt = prompt.to_str() if prompt.size_bytes <= 64 * 1024 else ""
    self._delivery = delivery or AutoDelivery()
    ...
```

`self.prompt` remains a public attribute so any caller / test that touches it
still sees a string for small prompts. For huge prompts it's an empty string
(documented), and code that needs the bytes uses `self._prompt_source`.

---

## 4. Compatibility strategy

### 4.1 Direct `ClaudeProcess(prompt=str, ...)` callers (6 sites)

| Caller | Path | Behavior under proposal |
| --- | --- | --- |
| `roadmap/executor.py:749` | composes ≤120 KB today, may exceed | AutoDelivery picks stdin when needed; no caller change |
| `roadmap/validate_executor.py:117` | same shape | same |
| `roadmap/remediate_executor.py:245` | same shape | same |
| `tasklist/executor.py:127` | same shape | same |
| `sprint/executor.py:1254` | uses subclass below | unchanged |
| `cleanup_audit/process.py:CleanupAuditProcess` (subclass) | calls `super().__init__(prompt=…)` | unchanged |

All four roadmap-style call sites today carry a defensive size warning
(`_EMBED_SIZE_LIMIT = 120 KB`) but no fallback. Those warnings can be **removed
or downgraded to debug** once `AutoDelivery` lands, because the abstraction
makes the size question moot. The warnings stay until the rollout step
(§9) confirms stdin path works in production.

### 4.2 Subclass `sprint.process.ClaudeProcess` (`sprint/process.py:88-121`)

It only adds an `__init__`/`build_prompt()`. Inherits `start/wait/terminate` and
the new `build_command(plan=...)` unchanged. Sprint debug log of `cmd[:3]`
(`sprint/process.py:42-47`) is compatible: `cmd[:3]` is still
`['claude', '--print', '--verbose']`. **No churn.**

### 4.3 Subclass `cleanup_audit.process.CleanupAuditProcess`

Same situation as sprint. **No churn.**

### 4.4 Subclass `cli_portify.process.PortifyProcess` — the hard constraint

Today (`cli_portify/process.py:185-215`):

```python
def build_command(self) -> list[str]:
    cmd = super().build_command()
    ...
    try:
        p_idx = cmd.index("-p")
        cmd[p_idx:p_idx] = add_dir_args
    except ValueError:
        cmd.extend(add_dir_args)
    return cmd
```

The override depends on the literal `-p` token being in the parent's argv. If
we silently switch to stdin delivery, `cmd.index("-p")` raises `ValueError` and
the `except` clause appends `--add-dir` flags **after** all other args —
which currently still works (claude accepts `--add-dir` after `-p`'s body), but
crucially `extra_args` (§3.1, line `cmd.extend(self.extra_args)`) would precede
the `--add-dir`. That's a behavior change.

**Evolution path for PortifyProcess:**

1. The base class signature becomes `build_command(*, plan: DeliveryPlan | None = None)`.
   `super().build_command()` (no args) keeps working — it computes its own
   plan via `AutoDelivery`.
2. We expose a stable **insertion anchor** that does not depend on `-p`:

   ```python
   class ClaudeProcess:
       _ADD_DIR_ANCHOR = "--max-turns"   # last fixed-position flag before model/extra
       def insert_pre_prompt_args(self, args: list[str]) -> None:
           """Subclass hook: splice argv just before model/extra/prompt args."""
           cmd = self._build_in_progress
           anchor = self._ADD_DIR_ANCHOR
           # ...
   ```

   Even simpler: provide an explicit `pre_prompt_args: list[str]` list that
   `build_command()` interpolates at a stable position (after `--output-format
   <fmt>`, before `argv_for_prompt`, before `--model`, before `extra_args`).
   `PortifyProcess` then sets `self._pre_prompt_args` in `__init__`
   instead of overriding `build_command()`, and the override can be deleted.
3. Until `PortifyProcess` is migrated, **keep its current override working**.
   Migration plan in two beats:
    - **Beat 1 (this patch).** `build_command()` always emits `-p` argv when
      `AutoDelivery` chose argv mode (which is the case for all current Portify
      use because Portify prompts are tiny — they're @path-prefixed file
      references, not embedded files). Portify's `cmd.index("-p")` keeps
      working unchanged. **No Portify change required.**
    - **Beat 2 (follow-up).** Add `pre_prompt_args` mechanism to base; rewrite
      `PortifyProcess.build_command()` to use it. Remove the `-p` index search.
      Portify becomes stdin-safe for free.

So the proposal preserves PortifyProcess **bit-for-bit** in beat 1: argv layout
is identical for prompts ≤127 KB.

### 4.5 The `prompt: str` constructor argument

Kept verbatim. `isinstance(prompt, str)` wraps in `StringPrompt`. Tests asserting
`proc.prompt == "..."` still pass.

---

## 5. Pipe / stdin mechanics

### 5.1 Open / write / close ordering

```
Popen(cmd, stdin=PIPE, stdout=fh, stderr=fh)         # 1
on_spawn(pid)                                        # 2 (debug log first)
spawn writer thread:                                 # 3
    for chunk in source.iter_chunks():
        proc.stdin.write(chunk)
    proc.stdin.close()                               # 4 -- EOF lets claude proceed
return proc                                          # 5

wait():                                              # later
    proc.wait(timeout=timeout_seconds)               # 6
    writer_thread.join(timeout=5)                    # 7 -- usually already done
    on_exit; close output/error fhs                  # 8
```

`proc.stdin.close()` is the EOF that tells claude "prompt is complete". Without
it, claude blocks forever waiting for more bytes. **The `try/finally close in
StdinDelivery.write` is non-negotiable.**

### 5.2 Deadlock analysis

A two-pipe deadlock (parent reads stdin while child fills stdout) is the classic
hazard. **It does not apply here** because `stdout` and `stderr` are connected
to plain files (`self._stdout_fh`, `self._stderr_fh` from
`process.py:114-115`). The kernel buffers them via the page cache; they never
block the writer. So:

- **No threading is required for correctness.** A blocking inline write loop
  in the parent before `wait()` would work.
- **Threading is required for cancellability.** The roadmap executor poll loop
  (`roadmap/executor.py:763-775`) checks `cancel_check()` while polling
  `proc._process.poll()`. If we did the write inline before that loop, a
  cancellation request could not interrupt a 5 MB stdin write. So: a daemon
  writer thread, joined in `wait()`, is the better default.

### 5.3 Streaming for >1 MB prompts

`StringPrompt.iter_chunks` chunks at 64 KB; pipes are 64 KB on Linux by default,
so we never overflow. For `FilePrompt` (future), `iter_chunks` reads in 64 KB
blocks straight from the file — never loads the full prompt into Python. A 100
MB prompt streams in O(1) memory.

### 5.4 Sync vs async

Async (`asyncio.create_subprocess_exec`) is a temptation but a layering
violation: callers (`roadmap/executor.py:763-775`) are blocking, with their own
poll loops. A daemon `threading.Thread` is sufficient and integrates with the
existing poll/wait/terminate code without async-coloring callers.

### 5.5 Termination interaction

If `terminate()` fires while the writer is mid-write, the writer hits
`BrokenPipeError` on `write` (after SIGTERM closes claude's stdin) — caught and
swallowed. `terminate()` calls `writer_thread.join(timeout=2)` so we don't
leak a thread. SIGKILL path: same; the kernel tears down the pipe; the
exception is caught.

---

## 6. Edge cases & failure modes

| # | Case | Behavior under proposal |
| --- | --- | --- |
| 1 | **SIGTERM mid-write** | Writer thread sees `BrokenPipeError`/`OSError`; caught in `StdinDelivery.write`; thread exits; `terminate()` joins with 2s timeout. |
| 2 | **EPIPE on claude early-exit** | claude crashes/segfaults before reading stdin → writer's `write()` raises `BrokenPipeError`; caught. claude's exit code surfaces via `wait()`. Operator sees error_file contents. |
| 3 | **Writer thread crash** (e.g., bug in `iter_chunks`) | Wrap `delivery.write(...)` in try/except, capture exception in `self._writer_exc`. `wait()` raises if non-zero exit code AND `self._writer_exc is not None` so the operator gets the actual cause, not just claude's stderr. |
| 4 | **UTF-8 multibyte boundaries** | `iter_chunks` chunks **bytes**, not characters. Mid-codepoint splits are fine because the receiving side reassembles a byte stream. `StringPrompt` encodes with `utf-8` once up-front in `iter_chunks`; we never split by character index. |
| 5 | **NUL bytes in prompt** | Allowed. `subprocess` argv path forbids NULs (raises `ValueError`); stdin path passes NULs through. We document this as a *gain* over the legacy path — closes a latent bug. |
| 6 | **Prompt mutability after Popen** | `StringPrompt` is `frozen=True`. `FilePrompt` reads at write time, so a file rewritten between `__init__` and `start()` would be picked up — a TOCTOU window. Mitigation: optional `FilePrompt.snapshot()` that copies bytes to a `BytesIO` at construction time; documented in `FilePrompt`'s docstring. |
| 7 | **TOCTOU between size_bytes and write** | `AutoDelivery.plan()` calls `source.size_bytes` once. If a `FilePrompt` grows between `plan()` and `write()`, we may have planned `argv` for a now-too-big file. Mitigation: re-check size in `ArgvDelivery.write` (no-op anyway) and **never** materialize the string twice. With `StringPrompt` (the only delivery used in beat 1), the size is final at construction. |
| 8 | **Env var leakage to child stdin pipe** | Stdin is a kernel pipe FD; environment is unrelated. No exposure path. (`build_env()` in `process.py:93-108` is unchanged.) |
| 9 | **Observability gap on huge stdin** | See §7 — we log a SHA-256 of the first/last 4 KB plus total size, written to a sidecar file. |
| 10 | **Process group + writer thread + setpgrp race** | `preexec_fn=os.setpgrp` (`process.py:123-124`) runs in the child between `fork` and `exec`. Writer thread starts in the parent *after* `Popen` returns, so by the time it writes, the child is already in its own process group. No race. |
| 11 | **Empty prompt** | `StringPrompt("")` → `size_bytes=0`. `AutoDelivery` picks argv (`-p ""`), preserving prior behavior. We do **not** silently switch to stdin for empty strings. |
| 12 | **Prompt larger than 2 GB** | `Popen.stdin` is a kernel pipe; size is irrelevant, the streaming write handles it. Practical bound is the timeout. We log a WARNING at >100 MB so operators notice runaway composition. |
| 13 | **Windows portability** | Existing code uses `os.setpgrp` behind a `hasattr` guard. Our writer thread + `Popen(stdin=PIPE)` is pure cross-platform. No regression. |
| 14 | **`extra_args` containing `-p`** | If a caller has historically passed a second `-p` in `extra_args` (it would be a bug, but possible), `cmd.index("-p")` in PortifyProcess returns the **first** `-p`, which is now possibly absent (stdin mode). Mitigation: keep the `except ValueError` fallback path correct — append `--add-dir` in a stable position (we leave Portify's existing fallback alone in beat 1). |
| 15 | **`subprocess.Popen` raises `OSError` for argv-size at exec** | Kernel raises EPERM/E2BIG; we catch in `start()` and re-raise as a typed `PromptTooLargeForArgv` error referencing the chosen delivery (should never happen with `AutoDelivery` correctly configured; this is the canary). |

---

## 7. Observability

**Today** (`process.py:131-135`, `sprint/process.py:42-47`): `cmd[:3]` is logged
which is `['claude', '--print', '--verbose']`. The prompt is the *fourth+*
argv element today and not logged. So the existing logs **already do not show
the prompt** — surprising but true. What this means: the observability story
for argv mode is *already* "look at the cmd separately if you care."

**Proposal:**

1. Keep the existing `cmd[:3]` log identical (no churn for log scrapers).
2. Add a **new structured log line** at spawn:

   ```
   _log.info(
       "spawn pid=%d delivery=%s prompt_bytes=%d prompt_sha256=%s",
       pid, plan.mode, source.size_bytes, _digest(source),
   )
   ```

   `_digest(source)` reads up to 4 KB head + 4 KB tail and SHA-256s the
   concatenation with size as salt. Constant time, never holds the full prompt.
3. Add a **prompt sidecar file** alongside `output_file`, gated on a config
   flag (default on for roadmap, off for sprint to avoid noise):
   `output_file.with_suffix(".prompt")` containing the full bytes. This is the
   operator's "what did claude actually see?" answer for stdin mode. It's
   written by the writer thread by `tee`-ing chunks: write to pipe, then to
   file. Rotation/cleanup uses the same lifecycle as the output file.
4. For `--input-format=stream-json` (future), the sidecar becomes JSON-Lines
   so `jq` works.

The `cmd[:3]` log is still fine: it never showed the prompt anyway. The new
structured line + sidecar is the actual upgrade.

---

## 8. Test plan (pytest)

Tests live under
`/config/workspace/Coder/.dev/architectural/claude-process-stdin-patch/tests_proposed/`
in design mode; the durable home in the package is
`tests/cli/pipeline/test_claude_process_delivery.py`.

### 8.1 Fixtures

```python
@pytest.fixture
def big_prompt() -> str:
    """200 KB prompt — well above MAX_ARG_STRLEN."""
    return "x" * (200 * 1024)

@pytest.fixture
def echo_claude(tmp_path) -> Path:
    """A fake `claude` binary that echoes argv and stdin to its output file."""
    script = tmp_path / "claude"
    script.write_text("""#!/usr/bin/env python3
import sys, os, json
out = {"argv": sys.argv, "stdin": sys.stdin.read()}
print(json.dumps(out))
""")
    script.chmod(0o755)
    return script

@pytest.fixture
def patched_path(echo_claude, monkeypatch):
    monkeypatch.setenv("PATH", f"{echo_claude.parent}:{os.environ['PATH']}")
    yield
```

### 8.2 Required asserts

```python
def test_argv_path_unchanged_for_small_prompt(patched_path, tmp_path):
    proc = ClaudeProcess(
        prompt="hello",
        output_file=tmp_path / "out", error_file=tmp_path / "err",
    )
    proc.start(); proc.wait()
    out = json.loads((tmp_path / "out").read_text())
    assert "-p" in out["argv"]
    assert "hello" in out["argv"]
    assert out["stdin"] == ""

def test_stdin_path_for_huge_prompt(patched_path, tmp_path, big_prompt):
    proc = ClaudeProcess(
        prompt=big_prompt,
        output_file=tmp_path / "out", error_file=tmp_path / "err",
    )
    proc.start(); proc.wait()
    out = json.loads((tmp_path / "out").read_text())
    assert "-p" not in out["argv"]                 # KEY assertion
    assert out["stdin"] == big_prompt              # full body delivered

def test_no_argv_element_exceeds_max_arg_strlen(patched_path, tmp_path, big_prompt):
    """The patch's correctness invariant. Probe build_command() directly."""
    proc = ClaudeProcess(
        prompt=big_prompt,
        output_file=tmp_path / "out", error_file=tmp_path / "err",
    )
    plan = AutoDelivery().plan(proc._prompt_source)
    cmd = proc.build_command(plan=plan)
    assert all(len(elem.encode("utf-8")) <= 127 * 1024 for elem in cmd)

def test_portify_add_dir_flags_still_present(patched_path, tmp_path):
    """PortifyProcess regression: --add-dir must appear before -p."""
    proc = PortifyProcess(
        prompt="small", output_file=tmp_path / "out", error_file=tmp_path / "err",
        work_dir=tmp_path, workflow_path=tmp_path / "wf",
    )
    proc.start(); proc.wait()
    out = json.loads((tmp_path / "out").read_text())
    argv = out["argv"]
    assert "--add-dir" in argv
    assert argv.index("--add-dir") < argv.index("-p")

def test_sigterm_mid_write_no_thread_leak(patched_path, tmp_path):
    huge = "y" * (5 * 1024 * 1024)        # 5 MB
    proc = ClaudeProcess(
        prompt=huge, output_file=tmp_path / "out", error_file=tmp_path / "err",
    )
    proc.start()
    proc.terminate()                       # immediately
    # writer thread must be joined within 2s
    assert not any(t.name.startswith("claude-stdin-") and t.is_alive()
                   for t in threading.enumerate())

def test_utf8_multibyte_round_trip(patched_path, tmp_path):
    prompt = "🦀" * 50_000                  # ~200 KB UTF-8
    proc = ClaudeProcess(
        prompt=prompt, output_file=tmp_path / "out", error_file=tmp_path / "err",
    )
    proc.start(); proc.wait()
    out = json.loads((tmp_path / "out").read_text())
    assert out["stdin"] == prompt           # no decode corruption

def test_observability_sidecar_written(patched_path, tmp_path, big_prompt):
    proc = ClaudeProcess(
        prompt=big_prompt, output_file=tmp_path / "out", error_file=tmp_path / "err",
    )
    proc.start(); proc.wait()
    sidecar = (tmp_path / "out").with_suffix(".prompt")
    assert sidecar.exists()
    assert sidecar.stat().st_size == len(big_prompt.encode("utf-8"))

def test_subclass_sprint_unchanged(...):
    """Sprint phase prompts (~few KB) take argv path; cmd[:3] log unchanged."""

def test_subclass_cleanup_audit_unchanged(...):
    """CleanupAuditProcess inherits delivery; small prompts use argv."""
```

### 8.3 Negative test

```python
def test_argv_too_large_raises_typed_error(monkeypatch, tmp_path):
    """If a caller bypasses AutoDelivery and forces ArgvDelivery on a 200 KB
    prompt, we want a typed PromptTooLargeForArgv, not OSError(E2BIG)."""
    proc = ClaudeProcess(
        prompt="z" * (200 * 1024),
        output_file=tmp_path / "out", error_file=tmp_path / "err",
        delivery=ArgvDelivery(),
    )
    with pytest.raises(PromptTooLargeForArgv):
        proc.start()
```

### 8.4 Running

`uv run pytest tests/cli/pipeline/test_claude_process_delivery.py -v` — fits the
project's UV-only rule (CLAUDE.md "Python Environment").

---

## 9. Rollout

### 9.1 Immediate (operator pain right now)

The package is `pipx`-installed at
`/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/`.

**Option A — vendored override module (recommended for speed).**

Drop a single file at the project's `src/superclaude/cli/pipeline/process.py`
(after pulling the package into `src/`) implementing the new design, and ship
it via `make sync-dev` per CLAUDE.md "Component Sync" rules. Rebuild pipx env:
`pipx install --force /path/to/repo`.

**Option B — monkey-patch shim.**

A tiny `superclaude_stdin_patch.py` script:

```python
import superclaude.cli.pipeline.process as _p
_orig_start = _p.ClaudeProcess.start
def _patched_start(self):
    if len(self.prompt.encode("utf-8")) > 127 * 1024:
        # ... write via stdin, omit -p from cmd
    else:
        return _orig_start(self)
_p.ClaudeProcess.start = _patched_start
```

Loadable via `PYTHONSTARTUP` or a CLI shim. Useful for hotfix; **not durable**.

### 9.2 Durable (upstream)

1. Open PR against `superclaude` repo with the full `PromptSource` /
   `PromptDelivery` design from §3.
2. Land in two beats:
    - Beat 1: introduce abstraction + `AutoDelivery`; preserve `-p` argv for all
      prompts ≤127 KB. Ship.
    - Beat 2: add `pre_prompt_args` mechanism; migrate `PortifyProcess` to it;
      delete `cmd.index("-p")` search; consider making stdin the *default* even
      for small prompts (so observability story is uniform).
3. Bump minor version (e.g., `0.x.0 → 0.(x+1).0`) — additive API, but the
   default `AutoDelivery` is a behavior change for prompts >127 KB.
4. Update `roadmap/executor.py:735-742`, `validate_executor.py:104-110`,
   `tasklist/executor.py:115-120`: drop the `_EMBED_SIZE_LIMIT` warning (it's
   no longer relevant) — or downgrade to debug.
5. Document in `CHANGELOG.md`: "Roadmap step prompts can now exceed 128 KB."
6. Pipx upgrade: `pipx upgrade superclaude`.

### 9.3 Validation

Per project CLAUDE.md "Validation should be done via the .github actions" — add
a CI job that runs the test plan in §8 against a fake `claude` shim. No
one-off scripts.

---

## 10. Risk register (top 5, ranked likelihood × impact)

| # | Risk | L | I | Score | Mitigation |
| --- | --- | --- | --- | --- | --- |
| 1 | **PortifyProcess regression** — `cmd.index("-p")` raises after default flips to stdin | M | H | 6 | Beat 1 keeps argv for all prompts ≤127 KB. Portify prompts are tiny → always argv → no behavior change. Beat 2 introduces `pre_prompt_args` and removes the dependency on the `-p` token. CI test asserts `--add-dir` precedes `-p`. |
| 2 | **Writer thread deadlock or leak** if stdin close path is missed (e.g., exception in `iter_chunks` before close) | M | H | 6 | `try/finally close` in `StdinDelivery.write`. `wait()`/`terminate()` always join with timeout. Test `test_sigterm_mid_write_no_thread_leak`. |
| 3 | **Observability regression** for operators reading `cmd[:3]` logs | H | L | 3 | `cmd[:3]` log is unchanged. Add structured spawn line + sidecar `.prompt` file for the new path. Document in changelog. |
| 4 | **claude CLI behavior change** — Anthropic could alter stdin semantics | L | H | 3 | Pin `claude` CLI version range in installation docs. Keep `ArgvDelivery` available as escape hatch. Sidecar file means we always have the prompt for replay. |
| 5 | **Prompt size explosion** — pipeline composers may stop bounding prompts now that stdin "just works" | M | M | 4 | Add the 100 MB WARNING gate (§6 case 12). Surface `prompt_bytes` in metrics so dashboards alert on growth. |

---

## 11. Open questions

1. **Should stdin become the default for all prompts (incl. small ones) in
   beat 2, or only for prompts above the budget?** Pro-uniform: simpler model,
   single observability path. Pro-hybrid: smaller diff for sprint/audit logs.
   *Recommendation: hybrid (`AutoDelivery`) until a release window allows the
   uniform switch.*
2. **Where should the `.prompt` sidecar file live?** Same dir as `output_file`
   is convenient but bloats artifact dirs. Alternative: a global
   `~/.cache/superclaude/prompts/<sha>` keyed by digest. *Pending operator
   input.*
3. **Should `--input-format=stream-json` be designed in beat 1 or beat 2?**
   The `PromptDelivery` interface accommodates it; the concrete
   `StreamJsonDelivery` can be deferred. *Defer to beat 2; not in scope for
   the 128 KB unblock.*
4. **Failure semantics when claude exits 0 but writer crashed mid-prompt.**
   Today: not possible (argv is atomic). Proposal: claude got a truncated
   prompt and may still exit 0 if it produced *some* output. We promote
   writer exceptions to a non-zero exit code in `wait()`. *Confirm: is exit
   code 99 (`E_PROMPT_INCOMPLETE`) acceptable, or do we re-raise from
   Python?*
5. **Backpressure / timeout calibration.** If claude reads stdin slowly (e.g.,
   server overloaded), our writer thread blocks on the 64 KB pipe. Should we
   add a max-write-stall timeout, or rely on the existing
   `timeout_seconds=6300`? *Recommend deferring; the 6300 s wait timeout is
   already the upper bound.*
6. **Should `prompt: str` be deprecated in favor of `prompt: PromptSource`
   over time?** Cleaner API, but creates churn for every test. *Recommend
   keeping str support indefinitely; it's the 90% case.*

---

### Appendix A — Cited line ranges

- `pipeline/process.py:71-91` — current `build_command` w/ `-p` argv.
- `pipeline/process.py:110-137` — `start()` with `stdin=DEVNULL`, `cmd[:3]` debug log.
- `pipeline/process.py:139-194` — `wait`/`terminate`/`_close_handles` lifecycle.
- `cli_portify/process.py:185-215` — PortifyProcess `cmd.index("-p")` insertion.
- `sprint/process.py:88-121` — sprint subclass.
- `cleanup_audit/process.py:22-47` — audit subclass.
- `roadmap/executor.py:719-759` — primary caller, embed-size warning.
- `roadmap/validate_executor.py:100-127` — sibling caller, same shape.
- `tasklist/executor.py:115-137` — sibling caller, same shape.
- `roadmap/executor.py:320-327` — `_MAX_ARG_STRLEN = 128 * 1024`, `_EMBED_SIZE_LIMIT = 120 KB`.
