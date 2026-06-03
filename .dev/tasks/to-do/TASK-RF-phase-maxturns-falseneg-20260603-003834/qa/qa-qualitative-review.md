# QA Report — Task File Qualitative Review

**Topic:** Fix IronClaude sprint executor PASS_RECOVERED for per-task error_max_turns false-negative
**Date:** 2026-06-03
**Phase:** task-qualitative
**Fix cycle:** N/A

---

## Overall Verdict: FAIL (1 IMPORTANT plan-omission fixed in-place; 1 MINOR citation fixed in-place)

Per the no-leniency rule, ANY issue → FAIL. Both issues found were fixable in-place
in the task file (the production code is not yet executed — this is a plan, so plan
defects are fixed by amending the task file). After the in-place fixes, the plan is
sound and would execute correctly. See Actions Taken.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `uv run pytest tests/sprint/test_executor.py`, `make lint`, `make verify-sync` all map to real targets; verify-sync passes unchanged since edits are src/ Python + tests/, not synced `.claude/` components (confirmed: sprint pkg is not a synced component dir) |
| 2 | Project convention compliance | none | PASS | Edits target `src/superclaude/cli/sprint/{models,executor}.py` + `tests/sprint/test_executor.py` — correct side of sync boundary; task explicitly forbids `git add .claude/`; UV-only honored in 6.1/6.2/6.3 |
| 3 | Intra-phase execution-order simulation | none | PASS | 2.1 (is_success) → 3.1 (helper) → 3.2 (recovery branch uses helper) → 4.1 (.is_success aggregation depends on 2.1) → 5.x (tests need 3.x+4.1) → 6.x gates. Each item's inputs produced by earlier items. No forward dependency. |
| 4 | Function signature verification | none | PASS | `TaskStatus` @models.py:39-53, `is_success` body `== PASS` @49, `is_failure` @53; `PhaseStatus.PASS_RECOVERED` @219; switch @executor.py:1015-1020; aggregation @1278 (`all(r.status == TaskStatus.PASS ...)`). ALL live-verified exact. |
| 5 | Module context analysis | AX-3 | FAIL→FIXED | `aggregate_task_results`@executor.py:296 + `AggregatedPhaseReport.status`@213-221 count only `== PASS`/`== FAIL`; a PASS_RECOVERED task → counted as neither → status PARTIAL/FAIL. Production-imported by preflight.py:208 + eval reporter. Task omitted this consumer of the new success status. Fixed by adding Step 4.2. |
| 6 | Downstream consumer analysis | AX-3 | FAIL→FIXED | Same as #5 — the aggregation enum-counting surface is a downstream consumer of TaskStatus the new member silently breaks (latent). Also verified: kpi.py (no TaskStatus refs), tui.py (renders `.status.value`, no exhaustive TaskStatus match), summarizer.py, logging_.py (`.status.value`) all render a new member safely — no other consumer needs changes. |
| 7 | Test validity | none | PASS | Tests write fake NDJSON to `config.task_output_file(phase, tasks[0])` — the EXACT path the recovery branch reads (results_dir/phase-N-task-ID-output.txt @models.py:503). Not vacuous; exercises real `detect_error_max_turns` + helper. mkdir gotcha real and flagged (results_dir=release_dir/results not pre-created by _make_config). |
| 8 | Test coverage of primary use case | none | PASS | 4 tests: positive recovery (5.1), genuine-failure guard (5.2), genuine-timeout/exit-124 phase-still-fails (5.3), overran-without-completion (5.4). Strong assertions `== PASS_RECOVERED` / `is_success` / phase-level mandated, NOT `!= FAIL`. |
| 9 | Error path coverage | none | PASS | Helper required to catch FileNotFoundError/OSError → return False (mirrors detect_error_max_turns safe-default @monitor.py:46-49); empty/truncated/missing-file → False. Guard C (5.4) tests the no-completion path. |
| 10 | Runtime failure-path trace | none | PASS | input(exit≠0,≠124) → switch else → detect_error_max_turns(path) AND helper(path) → PASS_RECOVERED → result → 1278 `.is_success` → PhaseStatus.PASS → 1610 `status.is_failure` False → phase continues. Traced end-to-end; no break. exit 124 stays INCOMPLETE (untouched). |
| 11 | Completion-scope honesty | none | PASS | Open Questions are genuine (PhaseStatus surfacing OPTIONAL, gated-vs-fallback design choice); none are silently answered elsewhere then ignored. Primary gated form required; fallback explicitly documented with Guard-C-NA handling. |
| 12 | Ambient-dependency completeness | none | PASS | detect_error_max_turns already imported @executor.py:37; Path already imported; no `__init__.py`/CLI/registry touchpoint for a private module-level helper. Step 1.5 verifies the import. (The aggregate_task_results consumer was the one missing touchpoint — see #5, now added as 4.2.) |
| 13 | Kwarg sequencing red flags | none | PASS | No "add kwarg before add param" pattern. Helper (3.1) added before its caller branch (3.2); no signature change to `_run_task_subprocess`/factory (Decision 5 — path recomputed in-caller). |
| 14 | Function-existence claims verified | none | PASS | `task_output_file` EXISTS @models.py:502 (used live @executor.py:1101,1112); `detect_error_max_turns` EXISTS @monitor.py:37; `_task_completed_before_overrun` correctly described as NEW (grep: 0 hits — does not exist yet, as the task states). |
| 15 | Cross-reference accuracy | AX-1 | FAIL→FIXED | Task frontmatter related_docs + Execution Context cite `config.task_output_file` at "config.py @502-503" / "task_output_file @502-503". The method actually lives in `models.py:502-503`, NOT config.py. Coincidentally same line numbers. Body method-calls resolve fine at runtime; only the metadata attribution is wrong. Fixed citation in frontmatter. |

## Summary
- Checks passed: 12 / 15 (after in-place fixes: 15/15)
- Checks failed: 3 (items 5, 6 = same root AX-3 omission; item 15 = AX-1 citation drift)
- Critical issues: 0
- Important issues: 1 (AggregatedPhaseReport/aggregate_task_results not updated for PASS_RECOVERED)
- Minor issues: 1 (config.py vs models.py citation slip)
- Issues fixed in-place: 2 (added Step 4.2; corrected frontmatter citation)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | task plan: Phase 4 (missing item) vs executor.py:296-334 (`aggregate_task_results`) + executor.py:213-221 (`AggregatedPhaseReport.status`) | The task introduces success-valued `TaskStatus.PASS_RECOVERED` and switches the INLINE phase aggregation (1278) to `.is_success`, but leaves the PARALLEL aggregation surface `aggregate_task_results` untouched. It counts `tasks_passed = sum(== PASS)` / `tasks_failed = sum(== FAIL)` only; a PASS_RECOVERED task is counted as NEITHER, so `AggregatedPhaseReport.status` returns `"PARTIAL"`/`"FAIL"` and `to_markdown` emits `EXIT_RECOMMENDATION: HALT` for a recovered-but-passing phase. This surface is production-imported (preflight.py:208, cli/eval/reporter.py) and heavily tested. Not a CRITICAL false-negative for THIS bug because the production per-task path does not route through it today (preflight only emits PASS/FAIL), but it is a latent semantic inconsistency the new status creates — a clean AX-3 omission. | Add a checklist item updating `aggregate_task_results` to count PASS_RECOVERED as a pass (e.g. `r.status.is_success`) so `tasks_passed`/`status` stay coherent with the new enum. (APPLIED as Step 4.2.) |
| 2 | MINOR | task frontmatter related_docs (line ~22) + spawn metadata | `config.task_output_file` / `task_output_file @502-503` attributed to `config.py`; the method is defined in `models.py:502-503` on SprintConfig (config.py:502-503 is `parse_tasklist_file`'s docstring). Line numbers coincidentally match, which masks the slip. Body items call `config.task_output_file(...)` as a method so runtime is unaffected; only the documentation pointer misleads a reader/executor doing discovery. | Correct the file attribution to models.py in the frontmatter. (APPLIED.) |

## Actions Taken
- Fixed issue #1 by inserting **Step 4.2** into Phase 4 of the task file: an item that
  reads `aggregate_task_results`/`AggregatedPhaseReport` @executor.py:296-334/213-221,
  updates the `tasks_passed` count (and confirms `.status`) to treat PASS_RECOVERED as a
  pass via `.is_success`, and adds/extends a unit test asserting a PASS_RECOVERED result
  is counted as passed and yields `status == "PASS"`. Verified the edit landed and is
  ordered after Step 4.1 (which establishes `is_success`) and before Phase 5.
- Fixed issue #2 by correcting the related_docs description in the frontmatter from
  "config.task_output_file @502" / "config.py" attribution to `models.py:502-503`.
  Verified the edit landed.
- Re-verified after fixes: the added Step 4.2 references only real symbols
  (`aggregate_task_results`@296, `AggregatedPhaseReport.status`@213, `tasks_passed`@323),
  uses the existing `is_success` semantics established in Step 2.1, and the existing tests
  `test_aggregate_all_pass`@820 / `test_aggregate_mixed_results`@832 give a clear extension
  pattern.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
Relied on rf-qa PASS for the following (skipped structural re-checking) and verified a
semantic counterpart for each with my own tool engagement:
- Relied on rf-qa PASS for #4 (granularity) and #5 (evidence-based real paths + line numbers)
  → semantic counterpart verified: I independently Read models.py:39-53, executor.py:1015-1020
  and :1278, monitor.py:37, config/models task_output_file:502-503 and grepped every TaskStatus
  enumeration site. rf-qa verified the line numbers EXIST; I verified the CONTENT at those lines
  matches what the items claim AND that the citation file-attribution was WRONG (issue #2) —
  a semantic defect rf-qa's structural PASS did not surface.
- Relied on rf-qa PASS for #6 (no contradicted/unverified findings; recovery target consistently
  PASS_RECOVERED) → semantic counterpart verified: I traced the full runtime data-flow
  (switch → 1278 → 1610) AND swept ALL downstream consumers of TaskStatus across the sprint
  package (executor aggregate_task_results, kpi, tui, summarizer, logging_, preflight, eval
  reporter). rf-qa's structural PASS did not check whether a NEW enum member breaks a parallel
  production-imported aggregation surface — it does (issue #1, the load-bearing finding of this
  review). This is the case where rf-qa PASS was INSUFFICIENT and my own tool work was required.
- Relied on rf-qa PASS for #9 (test assertions are strong, not `!= FAIL`) → semantic counterpart
  verified: I Read the actual fixture conventions (_make_config:34, TestPerTaskOrchestration:596,
  _fail_factory:618, test_per_task_timeout:715, fake-NDJSON in test_monitor.py:140-145) and
  confirmed the proposed tests write to the exact path the recovery branch reads (non-vacuous)
  and that the two-`result`-line NDJSON shape the helper requires is an established convention.

## Self-Audit
1. Factual claims independently verified against source code: ~22 (every line citation in the
   task + the full downstream-consumer sweep). Specifically verified: TaskStatus shape/properties,
   PhaseStatus.PASS_RECOVERED, the switch, the inline aggregation, aggregate_task_results +
   AggregatedPhaseReport.status, detect_error_max_turns, task_output_file/results_dir derivation,
   the test fixtures, the fake-NDJSON convention, and that `_task_completed_before_overrun` does
   not yet exist.
2. Files Read/grepped: models.py, executor.py (5 regions), monitor.py, config.py, test_executor.py
   (4 regions), test_monitor.py, kpi.py, tui.py, summarizer.py, logging_.py, preflight.py refs,
   research/04-gap-fill-crux-reconciliation.md.
3. Why trust this review: I did NOT find 0 issues — I found a load-bearing AX-3 omission
   (the aggregate_task_results consumer) by sweeping every TaskStatus consumer in the package,
   plus an AX-1 citation slip, each backed by exact file:line evidence shown above.
4. Web research performed: none (all checks were local-file-bound). Tavily not invoked; no fallback.

## Confidence
- Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 9 | Grep/Bash: 8 | Glob: 0 (Bash ls used for inventory)

## Recommendations
- The two in-place fixes resolve both findings. After the task executes, the executor will:
  (a) recover overran-but-completed tasks to PASS_RECOVERED, (b) pass them through BOTH the inline
  phase aggregation AND aggregate_task_results coherently, (c) keep exit-124 timeouts failing.
- Optional (already correctly marked OPTIONAL in the task): surfacing PhaseStatus.PASS_RECOVERED
  for recovered phases — not required for the fix; leaving it out is fine.

## QA Complete

VERDICT: FAIL (both issues fixed in-place; plan is now sound. No unfixable issues remain.)
