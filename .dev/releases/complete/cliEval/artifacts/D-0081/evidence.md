# D-0081 — Evidence

## Implementation

* `docs/eval/retention.md` — new policy doc; documents `--keep-home`
  default, NFR-ISO2 setup-failed preservation, summary retention on
  every exit branch, and the OPS-003 disk-budget breach advice +
  operator playbook.
* `src/superclaude/cli/eval/disk_budget.py` —
  `DISK_BUDGET_RETENTION_ADVICE` constant added; exported via
  `__all__`. The single source of truth for the OPS-003 retention
  advice string consumed by both the policy doc and the CLI
  dispatcher.
* `src/superclaude/cli/eval/commands.py` — imports
  `DISK_BUDGET_RETENTION_ADVICE` and emits it to stderr immediately
  before `sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)` in the
  disk-budget breach branch of `eval_run`.
* `tests/cli/eval/test_retention_policy.py` — new test module; six
  pytest cases pinning the doc, the constant, and the CLI surface.
* `.dev/releases/current/cliEval/artifacts/D-0081/spec.md` — test
  matrix + retention contract + AC mapping.
* `.dev/releases/current/cliEval/artifacts/D-0081/notes.md` —
  implementation notes, design decisions, rejected alternatives.

## Verification

Command (from `phase-4-tasklist.md` §T04.21 step 5):

```
uv run pytest tests/cli/eval/test_retention_policy.py -v
```

Result: see
`.dev/releases/current/cliEval/evidence/T04.21/test-output.txt`
for the full pytest log.

Five of the six tests run today (T04.10 has since landed, so the
`--keep-home True` HOME-preservation test now un-skips and passes).
The disk-budget breach stderr-emission test remains skipped behind a
narrower probe: the M5/M6 production `LifecycleExecutor`
(`ClaudeProcessAdapter` + `PtyDriver`) has not landed, so
`_resolve_executor_factory()` still returns `_NullLifecycleExecutor`,
which canned-returns `exit_code=0` instantly. The run finishes before
the disk-budget poller can tick on the seeded 2 MB file, so the
process exits 0 rather than triggering the breach branch. The probe
re-enables the test automatically once the production executor lands
(follow-up T04.10-followup-K002).

Per-test status (refreshed 2026-05-21):

```
tests/cli/eval/test_retention_policy.py::test_retention_doc_exists                                    PASSED
tests/cli/eval/test_retention_policy.py::test_retention_doc_covers_four_pillars                       PASSED
tests/cli/eval/test_retention_policy.py::test_retention_doc_quotes_advice_constant_verbatim           PASSED
tests/cli/eval/test_retention_policy.py::test_retention_advice_constant_shape                         PASSED
tests/cli/eval/test_retention_policy.py::test_cli_emits_retention_advice_on_disk_budget_breach        SKIPPED  [T04.10-followup-K002 production executor]
tests/cli/eval/test_retention_policy.py::test_keep_home_true_preserves_per_eval_homes_on_pass         PASSED
```

Summary: `5 passed, 1 skipped in 0.36s`.

## Acceptance criteria

From `phase-4-tasklist.md` §T04.21:

| AC | Status | Evidence |
|---|---|---|
| File `docs/eval/retention.md` documents `--keep-home` default false, failed setups preserved, summaries retained, disk-budget advice text. | ✅ Met | `test_retention_doc_exists` + `test_retention_doc_covers_four_pillars`. |
| Disk-budget breach error message contains the retention-advice string verbatim. | ✅ Library-boundary + doc-quotes-constant pin met today; ⏳ end-to-end subprocess test gated on T04.10-followup-K002 (production `LifecycleExecutor`). | `test_retention_doc_quotes_advice_constant_verbatim` + `test_retention_advice_constant_shape` (both pass today). End-to-end `test_cli_emits_retention_advice_on_disk_budget_breach` skipped behind the `_NullLifecycleExecutor` probe. |
| `--keep-home True` test confirms per-eval HOMEs are preserved after run. | ✅ Met (T04.10 has landed; the test now passes). | `test_keep_home_true_preserves_per_eval_homes_on_pass` PASSED. |
| `TASKLIST_ROOT/artifacts/D-0081/spec.md` records the policy. | ✅ Met | `.dev/releases/current/cliEval/artifacts/D-0081/spec.md`. |
| Evidence saved under `TASKLIST_ROOT/evidence/T04.21/`. | ✅ Met | `.dev/releases/current/cliEval/evidence/T04.21/test-output.txt`. |

## Cross-link sanity check

* `DISK_BUDGET_RETENTION_ADVICE` is a verbatim substring of
  `docs/eval/retention.md` (asserted by
  `test_retention_doc_quotes_advice_constant_verbatim`).
* The CLI dispatcher writes the constant via `click.echo(..., err=True)`
  immediately before the breach exit (asserted by
  `test_cli_emits_retention_advice_on_disk_budget_breach`,
  which un-skips when T04.10 lands).
* The constant itself contains the breach name, the preserved-
  artifact signals, both retention knobs, and the doc back-link
  (asserted by `test_retention_advice_constant_shape`).
