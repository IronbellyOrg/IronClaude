# D-0036 — Implementation notes (Task T02.16)

## Why `default_timeout` defaults to 30 s

The roadmap surfaces NFR-PERF1 (HOME setup p50 ≤ 2.0 s at 15-eval parallel,
T02.15) and NFR-REL1 (per-eval timeout kills + reaps, T03.x). Neither
specifies a hard floor for the *prompt-ready* wait — that is an eval-body
budget, not a driver budget. 30 s is the largest value that still feels
"snappy" if a developer is staring at a doctor-style smoke test, while
being generous enough that the rare cold-start (cold pip cache, fresh
HOME, MCP gateway not yet warm) does not flake the harness. Each eval
body that needs a tighter or looser budget overrides via the per-call
`timeout=` kwarg — the default is the floor, not a hard ceiling.

## Why `inject_prompt` writes `\r\n`, not `\n`

Claude Code's REPL is line-oriented in canonical PTY mode (the `pexpect`
default). The line discipline strips the `\r` on input, so the child
sees `\n` either way — but writing `\r\n` matches what a real terminal
emitter sends (a CR keystroke followed by the LF that the line
discipline appends). Several Claude Code edge cases noted in the
upstream ptytest fork (the original `PtySession.inject_prompt`
implementation) rely on this exact byte sequence. Matching the upstream
contract verbatim minimizes the drift surface during T02.01's vendored
SHA reviews.

## Why `read_stdout` is non-blocking by default

The cliEval orchestrator runs each eval in its own thread, and `Expect`
primitives (`Expect.stdout.contains`, etc.) need to assert against the
output stream incrementally rather than waiting for EOF. `pexpect`
exposes `read_nonblocking` for exactly this purpose; we proxy it
directly and swallow `pexpect.TIMEOUT` / `pexpect.EOF` into a clean
empty-string return so callers can write `while not_yet_seen:
chunk = driver.read_stdout()` loops without a try/except around every
read.

The `timeout=0` fast-path was the obvious alternative, but
`read_nonblocking` with a small positive timeout (say 0.2 s) is more
forgiving across slow CI hosts. We let the caller pick by exposing
`timeout` as a kwarg with the driver default as the fall-back.

## Why `wait_exit` uses `expect(EOF, timeout=...)` instead of `child.wait()`

`pexpect.spawn.wait()` does not accept a timeout parameter; it blocks
indefinitely. The cliEval orchestrator needs to enforce per-eval
timeouts (NFR-REL1), so we emulate a timed wait by issuing
`expect(EOF, timeout=T)` — which blocks until the PTY closes (i.e., the
child has exited) or `T` seconds elapse. The subsequent `child.wait()`
call is a no-op reaper at that point and populates `exitstatus` /
`signalstatus` without blocking.

The bare `child.wait()` raises `ExceptionPexpect` when pexpect believes
the child is still alive; we swallow it because `expect(EOF)` already
established that the child is gone — any residual race is benign and the
next attribute read on `child.exitstatus` returns the correct value.

## Why we cache `_exit_code` on the driver

Two reasons:

1. **Idempotency.** `wait_exit` is called by the orchestrator
   (T03.x) once when the eval completes, and may be called again by the
   reporter (T03.x) when it generates the per-eval summary. The cache
   avoids issuing a second `expect(EOF)` against a closed PTY (which
   would raise `EOF` again and break the contract).
2. **Signal-termination capture.** `close()` is called by `__exit__`
   whether or not `wait_exit` ran. If a test terminates the child via
   `terminate(force=True)` and then exits the `with` block without
   calling `wait_exit`, `close()` still populates `_exit_code` from
   `child.signalstatus` so the test can read `driver.exit_code` after
   the context manager closes.

## Why we re-export the error classes via `cli/eval/__init__.py`

The cliEval orchestrator (T03.x) catches `PtyDriverError` at the top of
each eval thread to translate driver failures into structured
`EvalOutcome` artifacts. Routing the imports through the package's
`__init__.py` keeps the orchestrator's import list flat and aligns with
the pattern already established for `HomeContainmentViolation` /
`HookDeployFailed` / `SchemaError` (all exported the same way).

## Why no test for the real `claude` REPL prompt

`claude --help` is the only `claude`-invocation that is reliably
non-interactive across versions; the REPL prompt format has churned
between releases (FR-G1 risk R1, R-013). The opt-in smoketest exercises
the spawn + exit-code path against the real binary without anchoring on
any particular prompt format. Tests that need the actual REPL prompt
will live in the eval bodies (Phase 5), where they can be parametrized
on a `claude` version pin set by `eval doctor`.

## Why we do NOT shell out to `pexpect.spawnu`

`pexpect.spawn(...)` with `encoding="utf-8"` is the modern equivalent of
the legacy `spawnu` constructor — pexpect's own docs flag `spawnu` as
deprecated. We stay on the canonical entry point so future pexpect
upgrades (NFR-MAINT1 `pexpect>=4.9` floor) do not surface deprecation
warnings inside the harness.

## Known limitations

* **Cooked-mode line discipline.** `write_stdin("abcde")` writes the
  five characters to the PTY but the child's `sys.stdin.readline()` will
  not return until a line terminator arrives. The test
  `test_write_stdin_does_not_append_newline` documents this by writing
  the terminator in a separate call and asserting on the absence of any
  `"got="` output in the interim. Callers that need raw input must
  switch the PTY to raw mode themselves (out of scope for v1).
* **Negative exit codes only on signal.** A child that exits with a
  *signal* gets `-SIGNUM`; a child that exits with a *negative status
  set via `_exit(-1)`* is impossible at the POSIX level (the kernel
  masks the status to 8 bits unsigned), so the negative-on-signal
  contract is unambiguous.
* **No streaming `read_stdout` cursor.** Each `read_stdout` call drains
  whatever pexpect has buffered; callers that need a single
  monotonically-growing transcript build it by concatenating chunks
  themselves (the round-trip test does exactly this). The
  `PtyStream` ANSI/buffer layer (T02.17) wraps this into a proper
  line-iterator with a `PtyTimeout`-aware deadline.
