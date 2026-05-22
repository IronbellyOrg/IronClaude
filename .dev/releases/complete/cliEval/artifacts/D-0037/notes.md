# D-0037 — Implementation notes (Task T02.17)

## Why the ANSI catch-all uses `[\x20-\x7E]` instead of just Fe

The original draft only matched 7-bit C1 (Fe) single-byte escapes —
`[@A-Z\\-_]`. That regex passed the SGR / CSI / OSC tests but failed on
`\x1B=` (DECPAM, Set Application Keypad), an Fp-range Fs single-byte
escape `claude` emits during keypad-mode reset. The fix broadens the
single-byte alternative to the full `[\x20-\x7E]` printable range and
keeps it as the **last** alternative so multi-byte sequences (CSI, OSC,
DCS) still bind their full payload before the catch-all has a chance.

The catch-all is intentionally permissive. ANSI streams in the wild
contain a long tail of vendor-specific singletons (DEC's
`\x1B7`/`\x1B8` cursor save/restore, charset selectors `\x1B(B`, etc.).
Enumerating every legitimate final-byte value would invite hidden gaps
when a new sequence appears in a `claude` minor release. Over-stripping
a stray printable byte after ESC is a far cheaper failure than leaving
a colour-reset in the buffer where it can break `Expect.contains` —
that bias is explicit in the spec.

## Why the iterator raises `PtyTimeout` instead of `StopIteration`

The first draft swallowed `PtyTimeout` into `StopIteration` so a
`for line in stream:` loop would exit cleanly on a stall. That is the
**wrong** default for the Expect primitives: a stalled child looks
identical to a finished one, and assertions like `Expect.stdout.contains`
silently pass-by-omission when the child hangs.

The spec change: iteration propagates the timeout. The cost is that a
naive caller doing `for line in stream:` must wrap in
`try / except PtyTimeout:` if they want graceful termination — but
that's the **correct** call site for that decision. Callers that want
the "iterate forever" semantics call `read_line()` directly and decide
their own per-line budget.

`close()` is the only way to make iteration stop cleanly. The context
manager wires this up: `with PtyStream(driver) as stream:` always
closes on scope exit.

## Why `read_line(timeout=0)` is rejected

`pexpect.read_nonblocking(timeout=0)` already exists for "drain whatever
is buffered now"; the equivalent at the PtyStream layer would be
`stream.drain()`. We make this distinction enforceable by rejecting
`timeout=0` outright — callers who want a non-blocking poll use the
explicit method instead of an overloaded `read_line(0)` call. This
matches the strict-arg policy in the rest of the cliEval module
(`PtyDriver.__init__` rejects `default_timeout <= 0` for the same
reason).

## Why `poll_interval` defaults to 100 ms

The orchestrator runs up to 15 evals in parallel (NFR-PERF1, T02.15).
A `poll_interval` of `0.1` keeps each idle stream's CPU footprint
negligible (one syscall per 100 ms × 15 streams = ~150 wake-ups/s,
under 1 % of a core on a typical dev host) while still responding to
new output within a tenth of a second — well below human perception
and inside the timing tolerance of every Expect assertion in the
roadmap. Tighter intervals (`0.01`) are available for slow-tick tests
that want to confirm coalescing without the wall-clock cost; the
tests in `test_pty_stream.py::test_slow_stream_eventually_returns_line`
exercise this path.

## Why the chunk-source coercion accepts both methods and callables

The standard call site is `PtyStream(driver)` where `driver` is a
`PtyDriver`. But the unit tests want to drive PtyStream with scripted
chunks that have no pexpect dependency — and the eventual `Expect`
shim (T04.07) may wrap the driver in additional layers (think
`MockDriver` for record/replay, `BoundedDriver` for time-stop tests).

The coercion is therefore: if `source` has a `read_stdout` method, use
that. Otherwise, if `source` is callable, treat it as the chunk
producer directly. The unit tests use `scripted_reader` and
`delayed_reader` helpers built on `collections.deque` to feed
deterministic chunk sequences without any I/O.

## Why `drain()` exists separately from `read_line()`

A common failure mode in PTY-driven evals: the child emits its final
output without a trailing newline (e.g. `--version` prints `1.2.3` and
exits). Without `drain()`, the trailing fragment is stuck in the
buffer forever — `read_line` will keep timing out because there's no
`\n`, even though the child has exited and there is nothing more to
read.

`drain()` is the explicit escape hatch: after the child exits, call
`drain()` once to flush whatever fragment is left. The fragment is
returned ANSI-stripped (consistent with the rest of the buffer) and
the internal buffer is reset to `""`. Tests pin this contract via
`test_drain_returns_unterminated_remainder`.

## Why we expose `buffer` as a read-only property

Diagnostic value. When an Expect assertion fails because the child
sent the right text but never a newline, the assertion site needs to
know what's pending. Exposing `stream.buffer` lets the cliEval
artifact writer (Phase 4) attach the unterminated fragment to the
failure record — without it, the only way to see the pending bytes
would be to monkeypatch the regex or grep the raw PTY transcript.

The property returns a plain string snapshot; mutation of the returned
value cannot reach the internal buffer because Python strings are
immutable. There is no setter.

## Vendoring + import strategy

PtyStream's only third-party-shaped dependency is the regex it builds
in `ANSI_ESCAPE_RE`; everything else uses `re`, `time`, and
`collections` from the stdlib. There is no vendored regex library
because the catch-all + family alternatives fit in five short
patterns. If a future suite needs Unicode VT-220 sequences (4-byte
final bytes), we can extend the catch-all to `[\x20-\xFF]` without
disturbing callers.
