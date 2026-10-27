# D-0037 — COMP-011 PtyStream ANSI/buffer layer (Task T02.17)

**Task**: T02.17 (Phase 2 — cliEval harness)
**Tier**: STANDARD
**Risk**: Low
**Roadmap**: R-037 / COMP-011 (PtyStream)
**Cross-links**: D-0036 (T02.16 PtyDriver — upstream chunk producer feeding
`read_stdout`); D-CP02-MID-T13-T17 (Phase 2 mid-checkpoint that gates this
landing); downstream D-0?? Expect.stdout / Expect.stderr primitives (T04.07)
that consume the line iterator.

## Goal

Provide a thin, well-tested adapter that sits between `PtyDriver.read_stdout`
and the cliEval Expect primitives. The PTY emits a stream of bytes
decorated with ANSI escape sequences (colour, cursor moves, title-set OSC
bursts) and arbitrarily framed line boundaries — Expect assertions need
**clean text lines** instead. PtyStream is the concentration point for that
normalization: ANSI strip + line buffer + stall detection in one place, so
every downstream assertion uses the same canonical view of the transcript.

## Stream contract

### Constructor

```python
PtyStream(
    source: PtyDriver | Callable[[float], str],
    *,
    timeout: float = 5.0,            # default per-line wall-clock budget
    poll_interval: float = 0.1,      # max per-poll wait passed to source
    strip_ansi: bool = True,         # apply ANSI_ESCAPE_RE before buffering
    keep_newline: bool = False,      # retain \r\n on yielded lines
) -> None
```

The constructor coerces `source` into a `(timeout: float) -> str` callable.
For a `PtyDriver`, that means binding `read_stdout(timeout=...)`; for any
other callable, it is used verbatim. This dual mode lets the unit tests
drive PtyStream with scripted chunk producers that have no pexpect
dependency.

### COMP-011 method set (T02.17 AC bullet 1)

| Method                       | Behavior                                                                              |
|------------------------------|---------------------------------------------------------------------------------------|
| `read_line(timeout=None)`    | Block up to `timeout` seconds; return next complete ANSI-stripped line (no `\r\n`).   |
| `drain() -> str`             | Return whatever (ANSI-stripped) unterminated bytes remain in the buffer; clears it.   |
| `close()`                    | Mark the stream closed; subsequent reads raise `PtyStreamError`.                      |
| `__iter__` / `__next__`      | Iteration calls `read_line()` with the default timeout; propagates `PtyTimeout`.      |
| `__enter__` / `__exit__`     | Context manager. Exit always calls `close()`.                                         |
| `closed` (property)          | Boolean — whether `close()` was called.                                               |
| `buffer` (property)          | Read-only view of the current unterminated fragment for diagnostics.                  |

### Iteration vs. timeout — design choice

`__next__` deliberately propagates `PtyTimeout` instead of collapsing it
into `StopIteration`. Reason: downstream `Expect.stdout.contains(...)` and
`Expect.stderr.contains(...)` primitives treat a stalled stream as a
**deterministic failure** ("the binary hung for N seconds while we were
looking for X"), not as "stream exhausted". Collapsing both into
`StopIteration` would let a hung child look like a clean end-of-stream and
silently mask the assertion. Iteration stops cleanly only when the stream
has been `close()`-d.

### ANSI escape stripping

The `ANSI_ESCAPE_RE` regex covers four sequence families:

| Family                         | Pattern fragment                | Examples                              |
|--------------------------------|---------------------------------|---------------------------------------|
| CSI (control sequence)         | `\[[0-?]*[ -/]*[@-~]`           | SGR (`\x1B[31m`), cursor (`\x1B[1;1H`), EL/ED, mode set |
| OSC (operating-system command) | `\][^\x07\x1B]*?(?:\x07\|\x1B\\)` | Title set (`\x1B]0;ttl\x07`), hyperlinks |
| DCS / SOS / PM / APC           | `[PX^_].*?\x1B\\`               | Device control strings, PM messages   |
| ESC + single printable         | `[\x20-\x7E]`                   | DECPAM (`\x1B=`), DECPNM, IND/NEL, charset selectors |

The catch-all alternative is **listed last** so the multi-byte alternatives
match in preference to a single-byte strip; non-greedy quantifiers on the
OSC and DCS alternatives prevent a single match from spanning several
escape bursts.

`strip_ansi=False` bypasses the regex entirely — used for transcript
recording where byte-for-byte fidelity matters more than searchability.

### Failure modes

* **`PtyTimeout`** — raised by `read_line` when the budget elapses with no
  complete line in the buffer. The exception message includes the size of
  the unterminated buffer fragment so a debugger can see how much partial
  output is stuck.
* **`PtyStreamError`** — raised when `read_line` is called after `close()`.
  Also serves as the shared base class so `except PtyStreamError:` catches
  the entire surface, `PtyTimeout` included.

### Read loop discipline

`read_line` runs the following loop:

1. Try to pop a `\n`-terminated line from the buffer; return if found.
2. If the wall-clock budget is exhausted, raise `PtyTimeout`.
3. Wait `min(poll_interval, remaining_budget)` for the next chunk via the
   coerced reader callable.
4. If a chunk arrived, strip ANSI (when enabled) and append to the buffer.
5. Loop.

The `poll_interval` knob exists so an idle stream does not spin the CPU on
busy-wait — passing `0.1` (the default) keeps the loop responsive while
deferring the actual wait to the underlying read.

## Acceptance criteria mapping (T02.17)

| AC bullet                                                                                                  | Evidence                                                                                                                                                       |
|---|---|
| `PtyStream` strips ANSI escape sequences from byte chunks and yields line-buffered output.                 | `test_strips_ansi_csi_sgr`, `test_strips_osc_title_set`, `test_buffers_partial_lines`, `test_yields_multiple_lines_in_order`, plus four targeted regex tests.   |
| `PtyTimeout` is raised when no new line arrives within the configured timeout.                             | `test_raises_pty_timeout_when_no_line_arrives`, `test_per_call_timeout_overrides_default`, `test_timeout_reports_pending_buffer_size`, `test_pty_timeout_is_pty_stream_error`. |
| ANSI test fixture is normalized to identical plain-text output across runs.                                | `test_identical_plain_text_across_runs` — runs the fixture three times and asserts byte-identical lists; `test_iteration_yields_all_clean_lines` covers the iterator path. |
| `TASKLIST_ROOT/artifacts/D-0037/spec.md` documents the API.                                                | This deliverable's `spec.md` + `notes.md`.                                                                                                                      |

## FR-G1 / FR-G2 satisfaction

PtyStream does not spawn anything itself; it only normalizes output from
PtyDriver. FR-G1 ("real subprocess discipline") is therefore inherited
from PtyDriver — every byte PtyStream sees came from a real `fork`+`execve`
through pexpect. FR-G2 ("no in-process SDK") is irrelevant for this layer.

PtyStream's contribution to the harness's *truthfulness* properties is the
ANSI strip + line buffer: an Expect assertion that finds `"ERROR"` in
`stream.read_line()` is finding it in text the child actually printed, not
in a colour-reset prefix the harness happened to append.

## Out-of-scope (delegated downstream)

* **Stream multiplexing across stdout + stderr.** PtyDriver merges them
  into a single PTY by design (the user-facing terminal is one stream).
  Tests that need stderr separation use a second `subprocess.PIPE` flow
  outside the PtyDriver path.
* **Pattern-based expect (`expect("> ", timeout=)`).** That contract lives
  on `PtyDriver.expect_prompt_ready`; PtyStream's `read_line` is a strict
  line iterator.
* **Persistent transcript recording.** PtyStream surfaces clean text in
  memory; whether and how it is written to disk is a job for the cliEval
  artifact writer (Phase 4).
