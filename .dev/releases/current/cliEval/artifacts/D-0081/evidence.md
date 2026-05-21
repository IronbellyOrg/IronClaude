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

Four of the six tests run today; the two end-to-end CLI tests
(disk-budget breach stderr emission; `--keep-home True`
HOME-preservation) are skipped behind the
`_skip_unless_t0410_landed()` probe — the same self-clearing
forward-dependency pattern that sibling module
`tests/cli/eval/test_exit_codes.py` (D-0079) uses for the 0/1/3
exit-code paths. The skip diagnostic names the missing T04.10
deliverables so the suite re-enables itself once T04.10 lands.

Per-test status:

```
tests/cli/eval/test_retention_policy.py::test_retention_doc_exists                                    PASSED
tests/cli/eval/test_retention_policy.py::test_retention_doc_covers_four_pillars                       PASSED
tests/cli/eval/test_retention_policy.py::test_retention_doc_quotes_advice_constant_verbatim           PASSED
tests/cli/eval/test_retention_policy.py::test_retention_advice_constant_shape                         PASSED
tests/cli/eval/test_retention_policy.py::test_cli_emits_retention_advice_on_disk_budget_breach        SKIPPED  [T04.10 forward dep]
tests/cli/eval/test_retention_policy.py::test_keep_home_true_preserves_per_eval_homes_on_pass         SKIPPED  [T04.10 forward dep]
```

## Acceptance criteria

From `phase-4-tasklist.md` §T04.21:

| AC | Status | Evidence |
|---|---|---|
| File `docs/eval/retention.md` documents `--keep-home` default false, failed setups preserved, summaries retained, disk-budget advice text. | ✅ Met | `test_retention_doc_exists` + `test_retention_doc_covers_four_pillars`. |
| Disk-budget breach error message contains the retention-advice string verbatim. | ✅ Library-boundary + doc-quotes-constant pin met today; ⏳ end-to-end subprocess test gated on T04.10. | `test_retention_doc_quotes_advice_constant_verbatim` + `test_retention_advice_constant_shape` (both pass today). End-to-end `test_cli_emits_retention_advice_on_disk_budget_breach` skipped behind `_t0410_missing()`. |
| `--keep-home True` test confirms per-eval HOMEs are preserved after run. | ⏳ Test authored, skipped pending T04.10 (run-loop closure). | `test_keep_home_true_preserves_per_eval_homes_on_pass` skipped behind `_skip_unless_t0410_landed()`. |
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
