# D-0036 — COMP-007 PtyDriver wrapping pexpect.spawn (Task T02.16)

**Task**: T02.16 (Phase 2 — cliEval harness)
**Tier**: STANDARD
**Risk**: Medium
**Roadmap**: R-036 / COMP-007 (PtyDriver)
**Cross-links**: D-0023 (T02.01 vendored ptytest fork — runtime source of
`pexpect>=4.9`), D-0034 (T02.14 hook adapter — sibling of the per-eval HOME
flow), D-0035 (T02.15 HOME setup perf baseline — concurrency cap the driver
runs under), D-0037 (T02.17 PtyStream — direct downstream consumer of
`PtyDriver.read_stdout`).

## Goal

Provide a thin, well-tested wrapper around `pexpect.spawn` so the cliEval
harness can drive the real `claude` binary through a pseudo-terminal exactly
the way a human user does — no in-process SDK shortcut, no subprocess
without a TTY. This is the FR-G1 "real subprocess discipline" load-bearing
component: every eval body that needs to interact with `claude` does so
through this class, and every `claude --help`-style smoke check the harness
emits during `eval doctor` flows through the same code path.

## Driver contract

### Constructor

```python
PtyDriver(
    command: str | list[str],
    *,
    env: dict[str, str] | None = None,
    cwd: Path | str | None = None,
    prompt_ready_pattern: str | re.Pattern[str] = DEFAULT_PROMPT_READY_PATTERN,
    default_timeout: float = 30.0,
    encoding: str | None = "utf-8",
    dimensions: tuple[int, int] = (40, 120),
) -> None
```

The constructor validates arguments and stores them. It does **not** spawn
the child — that happens on `spawn()` or `__enter__`. This split keeps
construction cheap and matches the cliEval orchestrator's "build many
drivers, spawn them in parallel" pattern (T03.16).

### COMP-007 method set (T02.16 AC bullet 1)

| Method                                 | Behavior                                                                 |
|----------------------------------------|--------------------------------------------------------------------------|
| `expect_prompt_ready(timeout=None)`    | Block until the prompt-ready pattern matches; return PTY buffer captured *before* the match. |
| `inject_prompt(text: str)`             | `child.send(text + "\r\n")` then flush — Claude-Code-idiomatic write.    |
| `write_stdin(data: str \| bytes) -> int` | Raw write to the child's stdin; **no** newline appended.                  |
| `read_stdout(size=-1, timeout=None)`   | Non-blocking read of up to `size` bytes from the PTY; returns `""` when idle. |
| `wait_exit(timeout=None) -> int`       | Wait for the child to exit; return its exit code.                        |

Two error classes carry timeout / EOF signals up to the caller:

* `PtyDriverTimeout` — raised by `expect_prompt_ready` and `wait_exit` when
  the timeout budget elapses with the child still alive (and pattern still
  unseen).
* `PtyDriverEOF` — raised by `expect_prompt_ready` when the child closes
  its PTY (typically a crash) before emitting the prompt-ready pattern.

A `PtyDriverNotStarted` guard fires when any I/O method is called before
`spawn()`. `PtyDriverError` is the shared base, so callers can `except
PtyDriverError:` to catch the entire surface.

### Default prompt-ready pattern (DEFAULT_PROMPT_READY_PATTERN)

```python
DEFAULT_PROMPT_READY_PATTERN: str = r"[>$] *\r*\n"
```

Matches a bare `>` or `$` followed by optional whitespace and a CR/LF
terminator. The pattern relies on the newline terminator rather than the
`$` end-of-string anchor because `pexpect` compiles patterns without the
MULTILINE flag and its incremental PTY buffer almost always has trailing
CR/LF after the marker — an unanchored match against the newline is both
more permissive and more reliable. Callers that need a binary-specific
pattern (e.g. when the real `claude` REPL emits a `╭─` framed prompt)
override `prompt_ready_pattern` at construction.

### Exit-code semantics (T02.16 AC bullet 3)

`wait_exit` returns:

* `int >= 0` — POSIX exit code from `child.exitstatus`.
* `int < 0`  — POSIX-convention `-SIGNUM` when the child was killed by a
  signal (signal code lifted from `child.signalstatus`).

The negative-on-signal contract lets callers distinguish `exit(124)`
(timeout exit) from `SIGTERM` cleanly — important because the orchestrator
(T03.x) maps signal termination and explicit `exit(124)` to different
outcome statuses (`INTERRUPTED` vs `TIMEOUT`).

`wait_exit` is idempotent after the child has exited: the captured exit
code is cached on `_exit_code` and returned on subsequent calls without
re-driving `expect(EOF)`.

### Lifecycle hygiene

* `is_alive() -> bool` — `pexpect.spawn.isalive()` proxy.
* `terminate(force: bool = False)` — SIGTERM by default, SIGKILL when
  `force=True`. Safe to call on an already-exited child.
* `close()` — close the PTY fd and force-close on `pexpect.ExceptionPexpect`
  so we never leak the fd. Also pulls the exit code one last time so
  callers that go straight to `close()` (no `wait_exit`) still get
  `driver.exit_code` populated.
* `__enter__` / `__exit__` — context-manager support: enters with a fresh
  spawn, exits with `terminate()` + `close()`. Used by every interactive
  test in `tests/cli/eval/test_pty_driver.py`.

### Import strategy

```python
try:
    from superclaude.cli.eval.pty import pexpect as _pexpect  # vendored
except ImportError:
    import pexpect as _pexpect                                # fallback
```

The vendored path is the long-term home (NFR-MAINT1 / T02.01). The
fall-back keeps the module importable while T02.01's vendored sources are
still landing. Once T02.01 ships, the fall-back becomes dead code — this
is intentional, not a long-term escape hatch.

## Acceptance criteria mapping (T02.16)

| AC bullet                                                                                                          | Evidence                                                                                                                                                  |
|---|---|
| `PtyDriver` in `src/superclaude/cli/eval/pty_driver.py` exposes the 5 methods.                                     | `test_method_surface_matches_comp_007_contract` — introspects `inspect.getmembers(PtyDriver, predicate=inspect.isfunction)` and asserts the five names.    |
| A unit test spawns a real `claude --help` (or test-stub) subprocess via PTY and `expect_prompt_ready()` returns.   | `test_expect_prompt_ready_returns_before_timeout_against_stub` (always runs) + `test_real_claude_help_smoketest` (opt-in; skipped when binary absent).    |
| `wait_exit()` captures and returns the subprocess exit code accurately.                                            | `test_wait_exit_captures_exit_code_from_stub[0,1,42,124]` parametrized + `test_wait_exit_reports_signal_termination_as_negative` + idempotency test.       |

The four extra test groups beyond the three AC bullets are defense in
depth — every public method has at least one positive test and one
failure-mode test, and the lifecycle (`spawn`/`terminate`/`close`) is
covered by the context-manager round-trips that wrap every interactive
test.

## FR-G1 satisfaction

The cliEval roadmap's FR-G1 ("real subprocess discipline") forbids any
in-process Anthropic SDK path under `cli/eval/`. `PtyDriver` satisfies the
constructive half of that requirement by being the sole entry point for
spawning a `claude` subprocess in the harness:

1. The constructor accepts `command: str | list[str]`; the cliEval
   orchestrator passes `["claude", *args]` exclusively.
2. The spawn path is `pexpect.spawn` — a literal POSIX `fork` + `execve`
   inside a fresh PTY. There is no Python-level shortcut that bypasses the
   binary.
3. Per-eval isolation is applied through `env=HomeIsolation.env()` — the
   driver does not look at `os.environ` directly, so a forgotten env
   override cannot leak the host's `$HOME` into the child.

The negative half ("no SDK imports under `cli/eval/`") is enforced by the
ban-import lint rule landed in T03.x (`COMP-013` / D-0038 family). The two
together close FR-G1.

## Out-of-scope (delegated downstream)

* ANSI stripping + line buffering → T02.17 `PtyStream` / D-0037.
* `claude` version pinning + capability discovery → `eval doctor`
  subcommand and `CapabilityGates` (Phase 1).
* SIGINT cancellation + timeout reaping → T03.x `EvalRunner` (calls
  `terminate(force=True)` then `wait_exit`).

Each of these consumes `PtyDriver` rather than reaching into pexpect
directly — the driver is the single concentration point for the PTY
contract.
