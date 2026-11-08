<!-- persisted verbatim by the orchestrator from the reviewer's final message; the reviewer returned markdown instead of the requested YAML -->
# Reflect Reviewer — Deviation Findings

**Reviewer persona**: qa — coverage and acceptance  
**Grounding root**: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher`  
**Diff scope**: Explicit pre-execution tasklist review; no executed implementation diff supplied  
**Timestamp**: 2026-11-07T19:04:14+00:00  
**Total deviations**: 2

These findings concern **planned verification coverage**, not observed runtime regressions. The authorized decisions and declared differences were treated as the review baseline.

## Deviations

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|----------|----------|---------------|----------------------|----------|
| R2-001 | Drift | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:475` | **Final revalidation lacks independent revocation tests.** Step 6.2 requires rejection when a label disappears, approval is voided, or Project status changes immediately before dispatch. Step 6.7 explicitly tests closure, changed assignees, timeout and exhausted reserved budget, but does not require those three revocation scenarios. Initial eligibility tests would remain green if the implementation accidentally reused initial approval/Project evidence at revalidation. **Fix Step 6.7:** add independently parametrized lost-trigger/approval-label, revoked-approval and changed-Project-status re-read cases. Each starts eligible, changes only the final read, and asserts `revalidation_failed`, no entry and no launcher call. Run through Steps 6.10 and 9.4. | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:879` — “the re-read failure skips”; `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:460` — “a closed issue, a lost label, a voided approval or a changed Project status”; same tasklist, `:475` — “a re-read showing the issue closed gives `revalidation_failed`”. | MEDIUM |
| R2-002 | Drift | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:472` | **The cycle’s stderr-fallback wiring is not exercised by the planned tests.** Step 2.8 tests the fallback formatter in isolation; Step 6.6 checks ordinary audit appends for each exit code. Neither requires an audit-append failure or final-save failure during a real cycle. Consequently, removing the fallback call from the cycle could leave the specified tests passing while violating AC-14. **Fix Step 6.6:** inject an append `OSError` and a final-save failure separately, execute `run_cycle`, and assert the exact five-key stderr JSON fallback, the required reason/exit, and lock release. Run through Steps 6.10 and 9.4. | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:887` — “Every exit writes a schema-valid audit line or the stderr fallback”; same design, `:722` — “`kind`, `ts`, `host`, `exit`, `reason` only”; `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:460` — “with `audit.stderr_fallback` when the append fails”; same tasklist, `:472` — “each of the exits … appends exactly one parseable cycle line”; `:212` — “`stderr_fallback` emits only `kind`, `ts`, `host`, `exit`, `reason`”. | MEDIUM |

Both are grounded coverage gaps. Neither asserts that implementation code already contains the corresponding defect. Step 9.17’s final semantic trace is a useful backstop, but the concrete test-writing items should not depend on that later reviewer discovering these missing scenarios.

## Adherence summary

- **Spec units audited:** 25 acceptance criteria.
- **Fully adherent planned coverage:** 23.
- **Authorized expansion:** 0 newly identified | **Necessary deviation:** 0 newly identified | **Drift:** 2 | **Regression:** 0.
- **Additional semantic checks:** all 46 rows of the reviewer brief’s Coverage slice.
- **Best-practice grade:** 4/5.
- **Self-confidence:** 0.91.

The counts use AC-1 through AC-25 as the atomic units. Coverage-slice rows overlap those criteria and are not counted again. Authorized register decisions are incorporated into the baseline rather than counted as new defects.

### Acceptance-criterion coverage

“Covered” below means adequately specified **in the plan**, not implemented or passing. Step numbers refer to the reviewed tasklist.

| Criterion | Judgement | Implementation items | Test-writing items | Test-running items / checks |
|---|---|---|---|---|
| AC-1 | Covered | 6.2, 7.1 | 6.6, 8.2 | 6.10, 8.9, 9.4 |
| AC-2 | Covered | 3.1a, 3.1c, 6.2 | 3.6, 3.7, 6.6 | 3.8, 6.10, 9.4 |
| AC-3 | Covered | 2.2, 3.1c, 6.2 | 2.6, 3.7, 6.7 | 2.10, 3.8, 6.10, 9.4 |
| AC-4 | Covered | 2.2, 6.2 | 2.7, 6.7 | 2.10, 6.10, 9.4 |
| AC-5 | Covered | 4.1c, 6.2 | 6.7 | 6.10, 9.4 |
| AC-6 | **Partially covered** | 4.1b, 4.1c, 6.2 | 6.7, 8.2 | 6.10, 8.9, 9.4; R2-001 identifies missing revalidation cases |
| AC-7 | Covered | 5.1 | 5.4, 8.3 | 5.9, 8.9, 9.4 |
| AC-8 | Covered | 5.1, 6.2 | 5.4, 5.5, 6.7 | 5.9, 6.10, 9.4 |
| AC-9 | Covered | 5.1, 6.2, 6.3, 7.1 | 5.4, 6.8, 7.4 | 5.9, 6.10, 7.7, 9.4 |
| AC-10 | Covered | 3.1b, 4.1c, 6.2, 7.2 | 3.7, 4.5, 6.8, 7.5 | 3.8, 4.6, 6.10, 7.7, 9.4 |
| AC-11 | Covered | 4.1b, 6.2 | 4.3, 8.5 | 4.6, 8.9, 8.10, 9.4 |
| AC-12 | Covered | 6.2 | 6.6 | 6.10, 9.4 |
| AC-13 | Covered | 4.1c, 6.2 | 4.3, 4.5, 6.7 | 4.6, 6.10, 9.4 |
| AC-14 | **Partially covered** | 2.3, 6.2, 7.1, 7.2 | 2.8, 6.6, 7.4, 7.5 | 2.10, 6.10, 7.7, 9.4; R2-002 identifies missing cycle-failure injection |
| AC-15 | Covered | 6.1, 6.2 | 6.5, 6.6 | 6.10, 9.4 |
| AC-16 | Covered | 5.1, 6.2 | 5.4, 5.7, 6.6 | 5.9, 6.10, 9.4 |
| AC-17 | Covered | 7.1, 7.2 | 7.4, 7.5 | 7.7, 9.4 |
| AC-18 | Covered | 3.1b, 4.1c, 6.2, 7.2 | 3.6, 4.5, 6.6, 7.5 | 3.8, 4.6, 6.10, 7.7, 9.4 |
| AC-19 | Covered under DF-55 | 2.1, 6.1, 6.2 | 2.5, 6.6 | 2.10, 6.10, 9.4 |
| AC-20 | Covered | 3.1a | 3.6, 8.3 | 3.8, 8.9, 9.4 |
| AC-21 | Covered | 2.1 and package import restrictions | 8.6 | 8.9, 9.4, 9.13 |
| AC-22 | Covered | 4.1b, 4.1c, 6.2 | 6.8, 8.4 | 6.10, 8.9, 8.10, 9.4 |
| AC-23 | Covered under authorized gate substitutions | Scope restrictions | 8.8; gate-only evidence also required | 9.5, 9.7–9.11, 9.15 |
| AC-24 | Covered | 6.3 | 6.9 | 6.10, 9.4 |
| AC-25 | Covered | Module boundaries and mirrored contracts | 5.6, 5.7, 5.8, 8.8 | 5.9, 8.9, 9.4 |

### Coverage-slice semantic judgments

Lexical matches were not accepted as proof, and lexical misses were not treated as defects.

| Requirement | Judgement | Task items | Semantic assessment |
|---|---|---|---|
| T-2 | Covered | 4.1c, 4.4, 6.2, 6.7 | Backoff implementation, boundary tests and cycle behavior are specified despite the missing exact token. |
| INF-006 | Covered | 9.1, 9.2 | Deployment remains owner-gated; no cron/live execution is added. |
| INF-008 | Covered | 5.1, 6.2, 8.3, 9.15 | Pull/claim-only architecture and integer-only prompt are carried into implementation and checks. |
| INF-009 | Covered | 3.1a, 3.6, 8.3 | Concrete argv/query restrictions prohibit GitHub and Project writes. |
| INF-016 | Covered | 3.1a, 6.2, 6.8, 8.3, 9.15 | Non-goals are reflected in package scope, read-only calls and no automatic retry. |
| INF-022 | Covered | 2.2, 3.1a, 4.1a, 8.8, 9.7 | New AST boundary tests and existing architecture lint cover the actual requirement. |
| INF-037 | Covered | 6.1, 6.5 | Project-ID validation and invalid-value tests are specified. |
| INF-042 | Covered | 6.1, 6.5 | Unknown top-level and nested configuration keys are explicitly rejected and tested. |
| INF-044 | Covered | 5.1, 6.1, 6.2, 7.1, 6.5, 6.6, 7.4 | Exit-2 conditions have implementation and behavioral checks. |
| INF-051 | Covered | 6.1, 6.5 | Exit precedence is tested pairwise, not merely mentioned. |
| INF-055 | Covered | 3.1a–3.1c, 3.6, 3.7 | Builders, classification, timeout injection and complete paging are assigned. |
| INF-089 | Covered | 2.2, 3.1a, 3.6, 8.3 | Project comparison stays in Python; the query/argv tests constrain interpolation. |
| INF-101 | Covered | 2.3, 2.8, 8.7 | Closed audit keys and hostile-text checks cover the forbidden-key requirement. |
| INF-108 | Covered | 5.6–5.8, 6.9, 8.2–8.8, 9.4 | Every named cross-cutting test has a creating item and a directory-wide running item. |
| INF-123 | Covered under DF-05 | 7.7, 9.5, 9.6, 9.19 | Local full-suite execution is expressly replaced; full suite remains CI-only. |
| INF-124 | Covered | 3.9, 5.10, 7.8, 9.7 | Lint-running items exist, including final-tree lint. |
| INF-128 | Covered | 6.2, 6.7, 6.8 | One launch per cycle is exercised by S1 and acceptance-property cases. |
| INF-129 | Covered | 3.1b, 3.7, 6.7, 6.8 | Ordinary/reserved counters and whole-cycle budget behavior are tested. |
| INF-135 | Covered | 2.6, 3.7, 6.7 | Approval actors, relabelling, incomplete history and edits have explicit cases. |
| INF-139 | Covered | 5.4, 8.3 | Edge inputs plus seeded hostile values and recorded launch prompts are checked. |
| INF-142 | Covered | 4.5, 6.8, 7.5 | Reset preservation of consumption and the long-run launch property are explicit. |
| INF-147 | Covered | 6.5, 6.6 | Shared-failure scenarios and exit-precedence tests provide behavioral coverage. |
| INF-151 | Covered under DF-55 | 2.5, 6.6 | Real runner timeout and fake-clock cycle cutoff form the authorized split. |
| INF-001 | Covered | 4.1b, 6.2, 6.7, 8.2 | Durable pre-spawn state and one ordinary top-level launch are checked at the call boundary. |
| INF-002 | Covered | 6.8, 8.4, 8.5, 9.2 | At-most-once is supported by long-run, crash and concurrency tests; residual limits are documented. |
| INF-017 | Covered | 2.2, 6.2, 6.6, 6.7 | Project failure closes eligibility; missing scope voids the cycle. |
| INF-020 | Covered | 4.1b, 4.3 | Directory fsync is both assigned and observed by a counting wrapper. |
| INF-023 | Covered | 8.8, 9.9, 9.15 | Import restrictions, dependency verification and unchanged dependency metadata support the requirement. |
| INF-028 | Covered | 6.3, 7.1, 7.4 | Status schema, health exits, no runner calls and unchanged mtimes are tested. |
| INF-034 | Covered | 6.1, 6.5, 7.1, 7.4 | Commands share configuration validation and test the shared behavior. |
| INF-038 | Covered | 6.1, 6.2, 6.5, 6.6 | Account-ID type/range validation and runtime mismatch behavior are explicit. |
| INF-052 | Covered | 4.1b, 4.3, 6.6, 8.5 | Lock contention and inode replacement are covered; no external work follows lock rejection. |
| INF-057 | Covered | 4.1a–4.1c, 4.3–4.5 | Store responsibilities, transitions, lock and atomic save are concretely decomposed. |
| INF-078 | Covered | 6.7, 8.2, 8.4 | Pending snapshots and crash reruns check the durable launch-counter argument. |
| INF-113 | Covered | 2.4, 6.4, 7.4, 8.1, 8.2 | Fake teardown guards and restricted PATH stubs prevent real tool calls. |
| INF-125 | Covered under DF-09 | 9.8 | The pinned replacement includes the full-tree format check, not only changed files. |
| INF-126 | Covered | 9.9 | Dependency verification has an explicit running item. |
| INF-127 | Covered with disclosed limitation | 6.1, 9.12 | Python-floor inspection and forbidden-API scanning are assigned; local 3.10 execution is not claimed. |
| INF-130 | Covered | 4.1c, 4.5, 6.8 | Rolling-window boundaries and six-launch cap have explicit tests. |
| INF-131 | Covered within owner-follow-up boundary | 3.2–3.5, 5.2, 9.1, 9.2 | Assumed fixtures are created now; captured replies/live-test record remain owner work. |
| INF-133 | Covered | 6.6, 8.2 | Initial login/discovery order and early-stop scenarios are specified. |
| INF-146 | **Partially covered** | 2.8, 6.6, 7.4, 7.5 | Rotation and normal lines are covered; cycle fallback integration is R2-002. |
| INF-148 | Covered | 5.4, 5.7, 6.6 | Origin failure and parser parity have independent tests. |
| INF-152 | Covered | 3.6, 8.3 | Literal argv checks and cross-cycle scans apply the corrected REST-only GET rule. |
| INF-153 | Covered | 8.6, 8.9, 9.4 | The AST detector includes mutation guards and is selected by test-running items. |
| INF-155 | Covered under authorized gate substitutions | 9.4–9.16, 9.19 | Final checks and evidence recording are assigned; no new dependency is permitted. |

### Named test files and checks

All **19 test files** named in design sections 11–12 have a creating item and an item selecting them for execution.

| Test-file identity | Creating item(s) | Initial running item |
|---|---|---|
| Runner module test | 2.5 | 2.10 |
| Predicates module test | 2.6, 2.7 | 2.10 |
| Audit module test | 2.8 | 2.10 |
| GitHub module test | 3.6, 3.7 | 3.8 |
| Record module test | 4.3–4.5 | 4.6 |
| Launch module test | 5.4, 5.5 | 5.9 |
| Find-Orca parity test | 5.6 | 5.9 |
| Origin parity test | 5.7 | 5.9 |
| Marker contract test | 5.8 | 5.9 |
| Cycle module test, including fifty-cycle and acceptance properties | 6.5–6.8 | 6.10 |
| SLO helper test | 6.9 | 6.10 |
| CLI module test | 7.4, 7.5 | 7.7 |
| CLI subprocess end-to-end test | 8.2 | 8.9 |
| Security invariants test | 8.3 | 8.9 |
| Crash injection test | 8.4 | 8.9 |
| Concurrency test | 8.5 | 8.9 |
| No-shell test | 8.6 | 8.9 |
| No-text test | 8.7 | 8.9 |
| Module boundaries test | 8.8 | 8.9 |

Step 9.4 selects the complete test directory again; Steps 8.10 and 9.6 select it under xdist. The test directory is `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch`.

The named checks also have concrete coverage: C1–C5 with five reruns, deterministic lock contention, fifty cycles, the acceptance property, AST no-shell and import-boundary detectors with mutation guards, hostile-text sentinels, marker parity, assumed-fixture parsing, dependency/sync gates and full-tree formatting. The two findings concern missing **scenarios inside existing files**, not missing files or absent test-running commands.

## Notes

- **Review boundary:** This was a pre-execution review. No implementation correctness, observed test pass, runtime regression or actual commit outcome is asserted.
- **Beyond-matrix search:** The design sections were inspected beyond the supplied matrix leads. No additional requirement was established as both absent from the matrix and wholly unassigned by task items. The two findings instead expose incomplete behavioral verification of assigned requirements.
- **Authorized differences:** The local affected-subset gate, pinned formatter, runtime-generated stubs, five command names, split timeout test and declared Open Questions were not reported as defects. In particular, the declared omission of `re-approved` emission was not turned into a finding.
- **Gate equivalence:** The affected subset is not equivalent to the entire repository suite. Its narrower scope is authorized and disclosed; the final record must retain “full suite: CI only.”
- **Other brief leads:** The checkpoint sequence captures BASE before the single commit, checks the staged allowlist and halts on commit/hook failure. Unverified reply shapes are consistently assigned to assumed fixtures and an owner-run deployment follow-up.
- **Self-audit:** All 25 acceptance criteria and all 46 Coverage-slice rows received semantic judgments. Named test creation was distinguished from test execution. Formatter/helper unit coverage was not mistaken for error-path integration coverage. No advisory no-spec correctness finding was established.

No commands, tests, edits or Git operations were performed. Remaining risk is planned-test adequacy; passing execution evidence and live reply-shape validation were not checked.


## Calibration (blind, attached by the orchestrator)

```yaml
calibrated_confidence: 0.85
calibrator_model_class: opus
calibrator_diversity: degraded
dimension_scores:
  citation_grounding: 0.95
  coverage_completeness: 0.85
  deviation_classification_clarity: 0.8
  risk_surface_coverage: 0.75
  recommendation_actionability: 0.9
finding_confidence:
  R2-001: 0.85
  R2-002: 0.8
```
