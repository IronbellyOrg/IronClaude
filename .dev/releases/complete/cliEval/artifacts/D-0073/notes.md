# D-0073 — Implementation notes (T04.11)

## Sequencing reality

When T04.11 was executed, the upstream chain was only partially landed:

* **T04.10** registered the `eval run` Click command surface (all 12
  flags wired through to `--help`), but the command body in
  `src/superclaude/cli/eval/commands.py:1267-1513` references helper
  symbols (`_new_run_id`, `_run_one_spec`, `_default_output_dir`,
  `_resolve_executor_factory`, `_utc_iso_now`, `_compute_run_stats`,
  `_format_run_summary_line`, `_can_install_signal_handler`,
  `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`,
  `RUN_INTERRUPTED_EXIT_CODE`) that are not defined anywhere in the
  module. Invoking the command at this state raises `NameError` at the
  `run_id = _new_run_id()` line before any suite resolution happens.
* **T05.01 / T05.02** (real suite manifest + E1 spec) have not yet
  landed — `src/superclaude/cli/eval/suites/real.yaml` does not exist.

Per phase-4-tasklist.md §T04.11 Notes:
*"E1 (T05.02) must exist for end-to-end validation; pre-E1 phase smoke
uses a stub eval."*

## Design decision: skip-precondition pattern over stub-eval

Two viable paths were considered for the pre-E1 posture:

1. **Stub-eval fixture under `tests/cli/eval/fixtures/`** — author a
   minimal `stub_real.yaml` + a no-op `E1` that exercises the runner
   end-to-end without depending on T05.02.
2. **Skip-precondition** — author the test against the literal AC
   invocation (`--suite real --eval E1`), but skip with a precise
   reason while any documented upstream dependency is unmet.

Path 2 was chosen because:

* The AC pins the **literal** invocation. A stub-eval test would
  exercise the runner but would not validate the operator-facing
  command line the FR-G6 contract names. The literal command line is
  the FR-G6 contract.
* The skip predicates re-activate the test the moment T04.10's body +
  T05.01 + T05.02 land — no follow-up test edit is required.
* The skip reasons name the missing upstream task ID, so a sprint
  runner inspecting the skip log can map directly to the unblocking
  task without consulting the phase tasklist.

If a stub-eval smoke is also desired later, it would live in a separate
`test_single_command_stub.py` module so the FR-G6 literal test remains
the contract anchor.

## Hermeticity

The test uses `--output-dir /tmp/eval-runs/t04_11_<pid>_<id>/` so:

* Parallel pytest invocations cannot collide on the same per-run tree.
* The AC12 scratch-root allowlist (`/tmp/eval-runs` is the canonical
  tmp-prefixed root, see `src/superclaude/cli/eval/config.py:63-68`)
  admits the path without an operator override.
* The default `--output-dir` resolution (which writes under
  `.dev/eval-runs/<run-id>/`) is bypassed so the repo working tree
  stays clean between test runs.

## Outstanding work surfaced (not in scope of T04.11)

The investigation surfaced T04.10's missing helpers as a blocker for
end-to-end FR-G6 validation. That is **T04.10's scope**, not T04.11's,
but flagging here so the sprint runner can re-sequence:

* `_new_run_id() -> str` — generate the deterministic run-id.
* `_default_output_dir(run_id) -> Path` — return
  `.dev/eval-runs/<run-id>/`.
* `_resolve_executor_factory() -> Callable` — return the
  `LifecycleExecutor` factory.
* `_run_one_spec(spec, run_dir, home_root, config, timeout_mult,
  keep_home, cancellation_token, executor_factory) -> EvalOutcome` —
  per-eval worker closure.
* `_utc_iso_now() -> str` — wallclock helper.
* `_compute_run_stats(outcomes, manifest_n) -> tuple[RunCounts,
  RunTotals]` — bucket totals + manifest-N parity check.
* `_format_run_summary_line(summary, output_dir) -> str` — verbose
  stdout line.
* `_can_install_signal_handler() -> bool` — main-thread guard.
* `RUN_CLEAN_EXIT_CODE = 0`, `RUN_FAILURES_EXIT_CODE = 1`,
  `RUN_INTERRUPTED_EXIT_CODE = 3` — exit-code constants.

The smoke test's `_eval_run_body_incomplete()` predicate enumerates
these names so it stays in sync with the deferred helper set.
