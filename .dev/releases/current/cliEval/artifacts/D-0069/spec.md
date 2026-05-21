# D-0069 — `Expect.stderr` / `Expect.stdout` primitive spec (COMP-010.5)

**Task:** T04.07 (Phase 4, Roadmap R-069 / COMP-010.5)
**Module:** `src/superclaude/cli/eval/expect.py` — `Expect.stderr`, `Expect.stdout`
**Tests:** `tests/cli/eval/test_expect_stdio.py` (23 cases)
**Status:** Implemented 2026-05-20

## Signatures

```python
Expect.stderr(
    contains: Optional[str] = None,
    regex: Optional[str] = None,
    not_contains: Optional[str] = None,
) -> ExpectCallable

Expect.stdout(
    contains: Optional[str] = None,
    regex: Optional[str] = None,
    not_contains: Optional[str] = None,
) -> ExpectCallable
```

Both primitives share the same internal predicate engine
(`_stream_predicate` in `expect.py`); only the buffer source differs.
`Expect.stderr` reads from `ctx.stderr`; `Expect.stdout` reads from
`ctx.stdout`. The returned callables have type
`ExpectCallable = Callable[[EvalContext], ExpectResult]` (DM-009) and
carry `__name__` equal to `"stderr"` / `"stdout"` so the runner's JSONL
log records the originating primitive.

## ANSI-strip dependency (COMP-011 / T02.17)

The buffer source is the **ANSI-stripped** transcript fed by
`PtyStream` (T02.17 / D-0037). `PtyStream` strips CSI / OSC / DCS /
SOS / PM / APC bursts before assembling line-buffered output, so by the
time the engine sees `ctx.stdout` / `ctx.stderr` the buffer is plain
text. The predicate engine then **re-strips ANSI** via
`_strip_ansi(text)` → `ANSI_ESCAPE_RE.sub("", text)` so manifests that
load raw transcript fixtures still get clean substring / regex matches.

This double-strip is intentional. `PtyStream` is the on-the-wire
producer; the re-strip in the predicate engine guards against:

* Fixture transcripts captured by hand (no PTY in the loop).
* Future producers that feed `ctx.stdout` / `ctx.stderr` from a non-
  PtyStream path.
* Test authors who paste literal colour escapes into a regression
  pinning a bug that previously leaked through.

`test_stdout_strips_ansi_csi_before_match`,
`test_stderr_strips_ansi_osc_before_match`, and
`test_stdout_not_contains_after_ansi_strip` pin this contract.

## Argument semantics

| Arg | Type | Pass condition |
|---|---|---|
| `contains` | `Optional[str]` | `contains in buf` after ANSI-strip. |
| `regex` | `Optional[str]` | `re.compile(regex).search(buf)` is not `None` after ANSI-strip. |
| `not_contains` | `Optional[str]` | `not_contains not in buf` after ANSI-strip. |

`None` means "no check for this axis". All three default to `None`; a
no-argument invocation trivially passes (records the buffer length only).
`test_stdout_no_args_passes_on_empty_buffer` and
`test_stderr_no_args_passes_on_empty_buffer` pin the no-op contract.

## Evaluation order

Inside the predicate engine, given `buf = _strip_ansi(source(ctx))`:

1. If `contains is not None` and `contains not in buf` → FAIL with
   `expected={"contains": contains}`, `actual=buf`, message
   `f"{name} missing substring {contains!r}"`.
2. Else if `regex is not None` and `compiled.search(buf) is None` →
   FAIL with `expected={"regex": regex}`, `actual=buf`, message
   `f"{name} did not match regex {regex!r}"`.
3. Else if `not_contains is not None` and `not_contains in buf` →
   FAIL with `expected={"not_contains": not_contains}`, `actual=buf`,
   message `f"{name} unexpectedly contained {not_contains!r}"`.
4. Otherwise PASS with `details={"stream": name}`, message
   `f"{name} predicates satisfied"`.

The first failing check produces the `ExpectResult.failure` (DM-005);
`test_stdout_contains_runs_before_regex` pins the ordering.
`test_stdout_all_three_predicates_pass_together` covers the
all-pass composition path.

## Failure payload

| Branch | `expected` | `actual` | Message |
|---|---|---|---|
| `contains` miss | `{"contains": str}` | `str` (full buffer) | `{name} missing substring {contains!r}` |
| `regex` miss | `{"regex": str}` | `str` (full buffer) | `{name} did not match regex {regex!r}` |
| `not_contains` violation | `{"not_contains": str}` | `str` (full buffer) | `{name} unexpectedly contained {not_contains!r}` |

`name` is the originating primitive (`"stdout"` or `"stderr"`).
`actual` is the full ANSI-stripped buffer so the Reporter (T03.13)
can render context around the miss without re-fetching the artifact.

## Test matrix (`tests/cli/eval/test_expect_stdio.py`)

| # | Test | Stream | Argument under test | Direction |
|---|---|---|---|---|
| 1 | `test_stdout_contains_passes_when_substring_present` | stdout | `contains` | PASS |
| 2 | `test_stdout_contains_fails_when_substring_absent` | stdout | `contains` | FAIL |
| 3 | `test_stdout_regex_passes_on_match` | stdout | `regex` | PASS |
| 4 | `test_stdout_regex_fails_on_no_match` | stdout | `regex` | FAIL |
| 5 | `test_stdout_not_contains_passes_when_absent` | stdout | `not_contains` | PASS |
| 6 | `test_stdout_not_contains_fails_when_present` | stdout | `not_contains` | FAIL |
| 7 | `test_stderr_contains_passes_when_substring_present` | stderr | `contains` | PASS |
| 8 | `test_stderr_contains_fails_when_substring_absent` | stderr | `contains` | FAIL |
| 9 | `test_stderr_regex_passes_on_match` | stderr | `regex` | PASS |
| 10 | `test_stderr_regex_fails_on_no_match` | stderr | `regex` | FAIL |
| 11 | `test_stderr_not_contains_passes_when_absent` | stderr | `not_contains` | PASS |
| 12 | `test_stderr_not_contains_fails_when_present` | stderr | `not_contains` | FAIL |
| 13 | `test_stdout_strips_ansi_csi_before_match` | stdout | ANSI CSI strip | PASS + FAIL |
| 14 | `test_stderr_strips_ansi_osc_before_match` | stderr | ANSI OSC strip | PASS |
| 15 | `test_stdout_not_contains_after_ansi_strip` | stdout | `not_contains` post-strip | FAIL |
| 16 | `test_stdout_contains_runs_before_regex` | stdout | evaluation order | FAIL |
| 17 | `test_stdout_all_three_predicates_pass_together` | stdout | composition | PASS |
| 18 | `test_from_mapping_threads_stdout_contains` | stdout | declarative form | PASS |
| 19 | `test_from_mapping_threads_stderr_not_contains` | stderr | declarative form | PASS |
| 20 | `test_stdout_result_carries_primitive_name_and_timing` | stdout | DM-009 envelope | PASS |
| 21 | `test_stderr_result_carries_primitive_name_and_timing` | stderr | DM-009 envelope | PASS |
| 22 | `test_stdout_no_args_passes_on_empty_buffer` | stdout | no-args degenerate | PASS |
| 23 | `test_stderr_no_args_passes_on_empty_buffer` | stderr | no-args degenerate | PASS |

All 23 cases pass under
`uv run pytest tests/cli/eval/test_expect_stdio.py -v` in 0.17 s on
2026-05-20.

## Shared predicate engine

Both primitives delegate to the module-level `_stream_predicate(*, name,
source, contains, regex, not_contains)` helper. The helper:

* Compiles `regex` once at construction time.
* Closes over the `source(ctx) -> str` accessor so the same predicate
  body services both `ctx.stdout` and `ctx.stderr`.
* Tags the resulting callable with `__name__ = name` via
  `_named_callable` so the runner's JSONL log records `stdout` /
  `stderr` rather than `_run`.

This shared engine is the reason the test matrix is symmetric across
the two primitives — any regression in the engine surfaces on both.

## Downstream consumers

* T05.02 (E1, sticky lifecycle) — `Expect.stdout(contains="ready")`
  pins the boot banner.
* T05.04 (E3, matcher-coverage) — `Expect.stderr(regex=r"Error:")`
  asserts the expected error surface when a matcher is missing.
* T05.06..T05.16 (E5..E15) — most evals layer
  `Expect.stdout(not_contains="Traceback")` as a smoke guard so any
  unexpected Python traceback bubbles to FAIL even when the exit code
  is zero.

## Linked roadmap entries

* R-069 — COMP-010.5 / D-0069
* Depends on: T04.01 (Expect package skeleton, D-0064), T02.17
  (PtyStream ANSI strip, D-0037)
* Used by: T05.02..T05.16 (eval suite)
