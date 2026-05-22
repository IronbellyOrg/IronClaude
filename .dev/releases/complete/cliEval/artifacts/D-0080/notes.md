# D-0080 — Implementation notes

## Module-level decisions

* **Layout + Reporter seam, not end-to-end run.** The full
  `superclaude eval run` orchestrator loop is a T04.10 forward
  dependency; gating this test on T04.10 would have made it a
  forward-skip module (mirroring D-0079). Instead the contract is
  anchored at the seam where reproducibility actually lives: the
  `artifact_layout` helpers (FR-G4 source-of-truth) and the
  `Reporter.write()` step. The test materializes the FR-G4 tree
  directly inside `tmp_path` via `compose_run_dir` +
  `allocate_per_eval_paths`, writes synthetic per-eval files, and
  drives `Reporter.write()` to render `summary.json`. When T04.10
  lands and wires the orchestrator, it will reuse these same layout
  helpers — so a closure that emits them is automatically conformant
  to the invariants this module pins. No skips are needed.

* **Real Python traceback, not a hand-crafted string.** Test 5
  raises and catches a real `RuntimeError` and runs the captured
  exception through `traceback.format_exception(...)` to build the
  fixture traceback. This exercises the exact stringification
  contract production code will hit — line breaks preserved, leading
  indentation preserved, `Traceback (most recent call last):` header
  intact. A hand-crafted string would have proven only that the test
  agrees with itself.

* **Same traceback string asserted at two layers.** Test 5 holds
  both the JSONL channel (live, append-only) and the summary channel
  (post-run, rendered) in one test. A future refactor that drops the
  traceback at either layer (e.g., truncating in the summary while
  keeping it in the JSONL) fails this single test — rather than
  appearing as a partial pass where one layer guards the other.

* **Cross-link paths are run-relative POSIX.** Per DM-001, every
  `EvalOutcome.artifacts` value is a POSIX path **relative to the
  run directory**. The `_per_eval_artifacts_map` helper enforces
  this when building fixtures: it composes each per-eval file path,
  takes the `.relative_to(run_dir)`, and converts to POSIX with
  `.as_posix()`. Test 6 then resolves each value back against the
  run directory and asserts the resulting path exists. This is the
  load-bearing convention that makes the artifact tree
  **relocatable** — tar the run dir, extract anywhere, every
  cross-link still resolves.

## Reproducibility invariant

```
compose_run_id(suite_name, started_at) =
    f"{HHMMSSZ}-{sha256(suite_name || ISO-Z-instant)[:8]}"
```

The `sha256(...)[:8]` suffix is the load-bearing reproducibility
guarantee:

* Same `(suite_name, started_at)` → byte-identical run-id → byte-
  identical run dir → byte-identical cross-link strings → byte-
  identical `summary.json`.
* Different `suite_name` OR different `started_at` → different
  run-id (collision probability ≈ 2⁻³² per axis, negligible at
  human-operator scale).

Test 2 pins both halves explicitly. Test 7 reinforces by replaying
the same fixture twice and asserting byte-equality on the rendered
`summary.json` (modulo the run-dir prefix, which is the only
absolute path in the tree).

## Why eight tests, not five

The phase-4 tasklist names five acceptance criteria. The module ships
eight tests:

* Tests 1-5 map 1:1 to AC-1 through AC-4 plus the JSONL existence half
  of AC-2 (which is two sub-assertions split for diagnostic clarity:
  "the file exists" vs "the file is JSON-parseable line-by-line").
* Test 6 is AC-5 (the cross-link contract).
* Test 7 is a reinforcement of AC-1 + AC-5: byte-stability across
  replays — the property that makes "reproducibility" mean something
  observable rather than a layout convention.
* Test 8 is a negative guard on `parse_run_dir_components` — it raises
  on paths that do not match the FR-G4 layout. Without this, a future
  loosening of the parser could silently accept malformed paths and
  the round-trip in test 1 would still pass. Test 8 is cheap
  insurance.

The eighth test could have lived in `test_artifact_layout.py` (T04.13)
but the negative guard depends on the same imports and fixture style
as the other reproducibility tests, so keeping it adjacent reduces
maintenance friction.

## Fixture construction

```python
_STARTED_AT  = "2026-05-20T15:58:38Z"  # ISO-Z, fixed for reproducibility
_FINISHED_AT = "2026-05-20T15:59:30Z"  # 52 s after; arbitrary but stable
_SUITE_NAME  = "real"                  # canonical real-suite name
```

These constants are module-level so test 2 (deterministic run dir),
test 7 (byte-stable replay), and the rest of the module all hash to
the same run-id. Changing any of them shifts every assertion in the
file.

## Helpers

* `_make_traceback(message)` — raises + catches a `RuntimeError`,
  returns `traceback.format_exception(...)` joined. Used by test 5
  and test 7 to build realistic tracebacks.
* `_write_pass_per_eval(run_dir, eval_id)` — materializes a
  passing-eval subtree (`logs.jsonl` with two events, an empty
  `tty.transcript`, an `artifacts/` directory).
* `_write_errored_per_eval(run_dir, eval_id, traceback_str)` —
  materializes an ERRORED-eval subtree with the traceback inside the
  `result.failure` event of `logs.jsonl`.
* `_per_eval_artifacts_map(run_dir, eval_id)` — builds the
  run-relative POSIX `Mapping[str, str]` an `EvalOutcome.artifacts`
  field carries.
* `_build_summary(run_dir, ...)` — builds a `RunSummary` with
  `RunCounts` + `RunTotals` consistent with the supplied
  `EvalOutcome` list; returns the summary + the rendered
  `summary.json` Path.

## Hand-off to T04.10

When T04.10 wires `eval_run` end-to-end:

1. The orchestrator must call `compose_run_dir` / `compose_run_id`
   for the run-dir layout — tests 1, 2, 7 verify this implicitly.
2. The per-eval emitter (T03.05) must drop `logs.jsonl` and the
   PtyDriver (T03.04) must drop `tty.transcript` at the pinned
   filenames inside `compose_per_eval_dir(...)` — tests 3, 4 verify.
3. The exception handler must capture `traceback.format_exception(...)`
   into both the JSONL `result.failure.traceback` event AND the
   `ExpectFailure.traceback` field rendered into `summary.json` —
   test 5 verifies.
4. The `EvalOutcome.artifacts` mapping must contain run-relative
   POSIX paths to the three well-known names — test 6 verifies.

If the T04.10 closure satisfies these four steps the entire D-0080
suite stays green with no edits here.
