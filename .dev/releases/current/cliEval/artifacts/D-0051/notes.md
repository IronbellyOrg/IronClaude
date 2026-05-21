# D-0051 — Implementation Notes

## Design choices

* **Contract-by-absence, not contract-by-loop.** The runner has no
  retry code path. The "policy" is enforced by (a) refusing any
  non-zero `retry_count` at construction time and (b) a test that
  counts executor calls per `EvalOutcome` and asserts they stay at 1.
  This matches design-spec §13 ("deterministic single-pass run") and
  keeps the implementation surface minimal so R3-mit (T05.23) can add
  the retry-once branch in a single, reviewable place later.

* **Validation in `__init__`, not in `run`.** Raising at construction
  time means a misconfigured orchestrator wiring is caught before any
  `EvalSpec` is dispatched. The orchestrator (T03.15) builds one
  `EvalRunner` per eval up front, so the early raise stops a parallel
  run before the first thread spawns.

* **Constants on `EvalRunner` rather than at module level.** The
  retry-policy semantics belong to the runner; future R3-mit will be a
  method on `EvalRunner` (or a strategy injected into it). Putting
  `DEFAULT_RETRY_COUNT` and `MCP_FLAKY_TAG` on the class keeps the
  rename surface to one type. Importers reach them via
  `EvalRunner.DEFAULT_RETRY_COUNT` (already imported in every
  test/orchestrator that touches the runner).

* **`MCP_FLAKY_TAG = "MCP-flaky"` literal.** Chosen to match the
  design-spec §14 R3 entry verbatim (`"MCP-server-flaky" tag distinct
  from "hook-broken"`). The shorter form `"MCP-flaky"` was preferred
  because it is the form `decisions.md §B` uses for OQ-10. Either
  spelling is fine; the constant is the single source of truth so the
  rename, if any, is mechanical.

## What changed

```
M  src/superclaude/cli/eval/runner.py    +30 -1
A  tests/cli/eval/test_retry_policy.py   +334 (new)
A  docs/eval/retry.md                    +109 (new)
A  .dev/releases/current/cliEval/artifacts/D-0051/spec.md     (this set)
A  .dev/releases/current/cliEval/artifacts/D-0051/notes.md
A  .dev/releases/current/cliEval/artifacts/D-0051/evidence.md
A  .dev/releases/current/cliEval/evidence/T03.08/pytest-retry-policy.txt
A  .dev/releases/current/cliEval/evidence/T03.08/pytest-regression-cli-eval.txt
A  .dev/releases/current/cliEval/evidence/T03.08/SUMMARY.md
```

## Regression surface

* `tests/cli/eval/test_runner_class.py` — 11 tests against `EvalRunner`.
  Default `retry_count` does not change call signatures, so all tests
  continue to pass without modification.
* `tests/cli/eval/test_signal_handling.py` — 25 tests against the
  NFR-REL1 path. Unrelated to retry policy; all pass.
* Full `tests/cli/eval/` suite — **828 passed, 1 warning** (the
  pre-existing pty/forkpty `DeprecationWarning` that lands on hosts
  with `pty.openpty()` paths).

## Open follow-ups (out of scope for T03.08)

* **OQ-10 closure (`decisions.md §B`).** The exact MCP-flaky failure
  taxonomy is still empirical-only. T05.23 (R3-mit) cannot land its
  retry-once branch until OQ-10 closes; the constant is the agreed
  hand-off point.
* **EvalSpec `tags` field.** R3-mit will need a `tags: tuple[str, ...]`
  field on `EvalSpec` (the schema does not currently surface one). Two
  follow-on tasks belong to T05.23: the schema bump + the runner
  branch.
* **Orchestrator wiring.** RunOrchestrator (T03.15) does not yet pass
  `retry_count`. Today the orchestrator falls through to the default
  (`0`) which is correct; once R3-mit lands the orchestrator may pass
  a non-zero value for the MCP-flaky path.

## Cross-references

* `.dev/releases/current/cliEval/design-spec.md` §13 — Bounded retry.
* `.dev/releases/current/cliEval/decisions.md` §B — OQ-10 deferral.
* `.dev/releases/current/cliEval/artifacts/D-0050/spec.md` — NFR-REL1
  signal handling (sibling reliability deliverable).
* `docs/eval/retry.md` — user-facing documentation.
* `src/superclaude/cli/eval/runner.py` — implementation.
