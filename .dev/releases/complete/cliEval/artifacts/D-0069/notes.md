# D-0069 — Implementation notes

## Why this task was test-only

T04.01 (D-0064) shipped the full `Expect.stderr` / `Expect.stdout`
bodies alongside the package skeleton. Both primitives already
supported:

* Three named arguments: `contains`, `regex`, `not_contains` (each
  `Optional[str]`, default `None`).
* A shared `_stream_predicate` engine so any regression in one surfaces
  on both.
* Defensive ANSI re-strip via `_strip_ansi` → `ANSI_ESCAPE_RE` so raw
  transcript fixtures match clean.
* Failure payloads with `expected` / `actual` (DM-005) and a
  primitive-tagged callable name for JSONL logging.

T04.07's deliverable is the **per-primitive acceptance harness** that
touches every named argument and the ANSI-strip invariant on both
streams. No body changes were required to
`src/superclaude/cli/eval/expect.py`.

## Decisions

1. **Double-strip ANSI on the predicate side, even though PtyStream
   already strips upstream.** PtyStream is the on-the-wire producer,
   but `ctx.stdout` / `ctx.stderr` are typed `str` and could in theory
   be sourced from a non-PtyStream path in the future (manifest-loaded
   transcript fixtures, test-injected buffers, replay tooling). The
   defensive re-strip costs one regex `sub` per assertion and removes
   an entire failure mode where a hidden `\x1B[0m` would silently
   break a substring check. `test_stdout_strips_ansi_csi_before_match`
   pins both the match side (PASS) and the leak side (FAIL on a
   literal escape) so a future producer that *fails* to strip can't
   regress the contract.

2. **Evaluation order: `contains` → `regex` → `not_contains`.** When
   multiple predicates are supplied, the first failing check produces
   the failure payload — the rest short-circuit. This matches the
   declaration order in the signature so manifest authors reading
   `Expect.stdout(contains=..., regex=..., not_contains=...)` see the
   same priority the runtime applies.
   `test_stdout_contains_runs_before_regex` pins it.

3. **No-args is a degenerate PASS.** `Expect.stdout()` with no
   predicates returns `passed=True` rather than raising a
   "no-predicate" error at construction time. Rationale: manifest
   authors sometimes want a sentinel assertion that the stream is
   *reachable* (the EvalContext was populated) without making any
   content claim. A construction-time raise would force them to invent
   a no-op regex (`r"."` or similar) just to satisfy the API.
   `test_stdout_no_args_passes_on_empty_buffer` and
   `test_stderr_no_args_passes_on_empty_buffer` pin the no-op contract.

4. **`actual` field carries the *full* stripped buffer, not a truncation.**
   The Reporter (T03.13) renders unified diffs over the buffer when
   building the failure section; truncation at the predicate layer
   would force the Reporter to either re-fetch the artifact or emit
   incomplete context. Memory is bounded by the per-eval log cap
   enforced upstream by the orchestrator (T03.15), so handing the full
   buffer down is safe.

5. **Symmetric test matrix across the two primitives.** Both streams
   get all 11 argument-coverage cases (contains × pass/fail, regex ×
   pass/fail, not_contains × pass/fail, plus the ANSI-strip variants
   on both, plus the envelope + declarative checks). Originally I
   considered parametrizing across stream names to halve the file, but
   the asymmetric ANSI variants (CSI on stdout, OSC on stderr) and the
   distinct fixture inputs read more clearly as named tests. A future
   change that adds a 4th argument can drop into the same matrix
   without disturbing the existing layout.

## What was NOT changed in src/

* `Expect.stderr` and `Expect.stdout` bodies in
  `src/superclaude/cli/eval/expect.py` were already complete after
  T04.01. The T04.07 acceptance suite is purely additive.
* `_stream_predicate`, `_strip_ansi`, `_named_callable`, and
  `_timed_result` helpers were untouched.

## Followups deferred

* Test that `Expect.stdout` and `Expect.stderr` share golden output
  shape when a single eval emits to both streams (planned for the
  TEST-007 reporter contract suite, T04.17).
* Performance benchmark on >1 MB ANSI-laden buffers (planned alongside
  the disk-budget regression suite, T03.19).
* Manifest-loader smoke test pairing `Expect.from_mapping` with a
  fully assembled `expects:` block (planned alongside the manifest
  loader landing in T05.x).

## Linked artifacts

* Spec: `D-0069/spec.md`
* Evidence: `evidence/T04.07/pytest-output.txt`
* Source: `src/superclaude/cli/eval/expect.py` (`Expect.stderr`,
  `Expect.stdout`, `_stream_predicate`)
* Test module: `tests/cli/eval/test_expect_stdio.py`
* Roadmap: R-069, depends on T04.01 (D-0064), T02.17 (D-0037)
