# Issue watcher plan review

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.72
citations_total: 20
citations_revalidated: 20
citations_dropped: 2
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

## Summary
The plan has five tasks in four phases and passes its generation structure check. Advisory review retains five medium gaps and one low map omission; it does not approve implementation or rollout. The plan was not changed from these findings. Two reviewers reached full comparison agreement after rebuttal, but the invariant probe leaves two medium limitations, so agreement is not complete review coverage or test evidence.

Calibrated review confidence is conservatively .72, inherited from reviewer scores .74 and .72, not a new measurement. The independent evidence gate rechecked all 20 draft citations, verified 18 and dropped two invalid extraction quotes. Their rows were removed; the advisory result remains partial, not an implementation approval.

## Inferred requirements (Pass 2)
Paths below are checkout-relative. S means `.dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/source.md`; P means its sibling `TASK-WF-rollOutTheIssueW-20261109-000305.md`. The following extraction rows survived the independent exact-quote check; structural matching is not proof that the every-fixture gate is satisfied.

| INF id | Verbatim quote supplied upstream | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | replace the _assumed_shape fixtures with captured real gh and Orca output after the owner-run live test (FU-1) | S:7 | Task 5 |
| INF-004 | prepare the shadow-run, lock, restart and cron steps (FU-2) as owner-run checklist items | S:7 | Task 4 |
| INF-005 | keep enabled false until the owner flips it | S:7 | Constraints and Task 4 |
| INF-006 | is written up as `docs/designs/issue-watcher-live-test.md` (FU-1) | S:22 | Owner item and Task 5 precondition |
| INF-007 | then the six-field cron entry `0 */5 * * * *` (FU-2) | S:22 | Task 4 |
| INF-008 | Watcher test suite; must still pass after the fixture swap | S:32 | Task 5 |
| INF-009 | a reviewed 24-hour shadow run, the two-process lock test and the state-directory restart test, after which `enabled` becomes `true` | S:22 | Task 4 and owner items |
| INF-010 | FU-2 also covers a persisted `state_dir` if `$HOME` is not persistent | S:42 | Task 4 |

POSTSCRIPT: The independent validator dropped INF-002 and INF-003 because their literal ellipses were not verbatim source quotations. They were removed, not silently repaired. See `evidence-validation.md`. Of ten extracted rows, eight survived: parsed 0, surviving inferred 8, mapped 8, unmapped 0, union structural coverage 8/8 = 1.00; parsed-only coverage remains undefined and deviation density over the surviving mapping remains 0. These numbers describe the surviving extraction only and do not establish complete source extraction or satisfaction of the every-fixture obligation. The two actual documentation tasks remain in the plan; deleting invalid extraction rows does not delete those obligations.

## Plan gaps
All are pre-execution plan gaps, not post-execution regressions. Evidence citations below refer to the merged review; the independent validator traced its cited implementation and plan evidence, not merely reviewer agreement.

### Reason-column check rejects non-reason words (F1, medium)
- **Location/evidence:** `adversarial/merged-review.md:40-44`.
- **Mapped task / spec:** Task 2, source obligation to correct the reason table.
- **Classification/rationale:** plan-gap; the zero-miss check scans backticked state/command words as though they were reason keys.
- **Default remediation:** Limit extraction to the reasons column and save a zero-unexplained-miss check; this does not prove subsequent tasks pass.

### Retained captures are outside the token check (F2, medium)
- **Location/evidence:** `adversarial/merged-review.md:16-20`.
- **Mapped task / spec:** Owner handover and Task 5, safe retained capture evidence.
- **Classification/rationale:** plan-gap; redaction is required, but the explicit scan covers destination fixtures rather than retained captures.
- **Default remediation:** Verify retained captures as well as fixtures before staging them; token matching alone cannot prove all private identifiers are removed. No leak was found.

### All-fixture prerequisite conflicts with partial completion (QA-02, medium)
- **Location/evidence:** `adversarial/merged-review.md:22-26`.
- **Mapped task / spec:** Task 5, source's every-guessed-fixture obligation.
- **Classification/rationale:** plan-gap; the goal/precondition require every capture while the task body and acceptance allow uncaptured fixtures.
- **Default remediation:** Keep full replacement blocked until every required capture is substituted, unless the owner expressly changes the gate. An effort estimate is not that authorization. The prior unsupported coverage-matrix allegation is excluded.

### Replacement instruction omits the consumed raw envelope (QA-03, medium)
- **Location/evidence:** `adversarial/merged-review.md:28-32`.
- **Mapped task / spec:** Task 5, replacement of tested fixture data.
- **Classification/rationale:** plan-gap; the demonstrated include-response consumer reads raw, not payload. Existing stderr wording is not treated as defective.
- **Default remediation:** Specify and verify the consumed raw destination and capture stream without authorizing production-parser changes.

### Captured values need matching test expectations (QA-04, medium)
- **Location/evidence:** `adversarial/merged-review.md:34-38`.
- **Mapped task / spec:** Task 5, test-suite preservation after fixture substitution.
- **Classification/rationale:** plan-gap; a changed retained Date/login/id can invalidate fixed expectations. The whole test file is already permitted, so this is missing instruction, not a forbidden edit or universal capture failure.
- **Default remediation:** Explicitly include fixture-dependent expectation maintenance, separately from parser-shape mismatches.

### New section needs a matching runbook map (F4, low)
- **Location/evidence:** `adversarial/merged-review.md:46-50`.
- **Mapped task / spec:** Task 4, coherent owner-run checklist.
- **Classification/rationale:** plan-gap; the section map stops at 15 while the plan adds section 16. This is not a Task 4 acceptance blocker.
- **Default remediation:** Include the in-place section-map update.

Withdrawn required fixes: the cron count is already implied and the scheduler-sentence location is navigation advice, not a defect (`adversarial/merged-review.md:52-56`).

## Review limitations
- **Task 3 review coverage, medium:** Neither card fully checks each capture-sheet command against its builder or the preservation boundary. This is unreviewed scope, not a proven Task 3 defect (`adversarial/merged-review.md:60`).
- **Conditional capture-format interaction, medium:** Already-CRLF captures can interact with test-only newline conversion. No actual capture format or runtime failure was observed; inspect actual framing before classifying failures as production-parser mismatches (`adversarial/merged-review.md:61-62`).
- **Owner boundary:** Live test, live-test record, shadow run, lock/restart tests, enabling and cron installation remain owner-run; configuration stays false (`adversarial/merged-review.md:63-64`). No such actions or tests ran in this planning task.
- Two model-class reviewer slots were used, but vendor diversity is single and calibrator diversity is degraded. No independent-vendor validation is claimed.
- Requirement labels were sparse: parsed-only coverage is undefined; inferred matching is structural and must not be read as satisfaction of the contradictory every-fixture gate.
- Ten snapshotted input hashes were rechecked unchanged before synthesis. The original snapshot contains per-file hashes, not a stored aggregate tree hash; full newly-added-linked-file discovery was not proven. The final contract records this integrity limitation.
- No memory document was written outside this output directory because the brief forbids documentation changes. No implementation, fixture replacement, runtime verification, scheduling or enablement is authorized by this report.

## Inferred-claim audit
- `citations_inferred: 0`; non-load-bearing inferred-claim fraction: 0/20 = 0.00.
- The eight surviving inferred requirement-extraction rows are quote-pinned source obligations, not inferred report claims.
- Citation budget: full reread of all 20 original draft occurrences, 18 verified, two dropped. The final report retains the 18 verified occurrences; counters preserve the original validation population. No command/test result was passed through without execution evidence.

## Recommendations
### Recommendation R-001: Resolve the every-fixture gate before authorizing execution
- **File:** P (reviewed plan path defined above).
- **Change:** In separately authorized planning, make the all-fixture prerequisite and completion rule agree; preserve full replacement unless the owner explicitly changes the obligation.
- **Verifier:** Read Task 5 goal, prerequisite, body and acceptance together and confirm they require the same capture set.
- **Linked gaps:** QA-02.
- **Priority:** P1.

### Recommendation R-002: Clarify fixture maintenance and capture verification
- **File:** P, Tasks 2, 4 and 5.
- **Change:** In separately authorized planning, specify the reason-column check, retained-capture verification, raw destination, capture-dependent assertions and runbook map update.
- **Verifier:** Compare the revised instructions against the six retained evidence blocks; future implementation must run the existing watcher suite, not infer a pass from these repairs.
- **Linked gaps:** F1, F2, F4, QA-03, QA-04.
- **Priority:** P1 (F4 alone is P2).

### Recommendation R-003: Preserve unreviewed boundaries before later fixture substitution
- **File:** P, Task 3 and Task 5 evidence instructions.
- **Change:** Require row-by-row builder/preservation evidence and actual capture-framing inspection, while leaving live actions and enablement with the owner.
- **Verifier:** Review saved command mappings and unchanged prose, then distinguish capture-format/test-adapter failures from production-parser mismatches using actual captured evidence; no parser rewrite is authorized here.
- **Linked gaps:** two medium probe residuals.
- **Priority:** P1.

This is an advisory-only handoff. No recommendation was applied to the gated plan. The executor for an approved workflow plan is `/sc:implement`, but it was not invoked and execution is not approved by this report.
