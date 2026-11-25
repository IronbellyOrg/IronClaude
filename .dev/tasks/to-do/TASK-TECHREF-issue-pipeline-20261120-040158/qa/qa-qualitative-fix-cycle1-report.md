# QA Fix Log - A.10.5 qualitative gate, fix cycle 1

**Task file edited:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/TASK-TECHREF-issue-pipeline-20261120-040158.md
**Source finding:** B-1 in /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/qa/qa-qualitative-sufficiency-report.md (gates fail open when a QA agent returns nothing usable)
**Date:** 2026-11-20
**Fix cycle:** 1
**Scope:** B-1 only. Medium findings (M-1 to M-8) and Notes (N-1 to N-9) were not applied.

Status: Complete

## Edits applied (all via Edit, targeted; checklist stays at 83 `- [ ]` items, verified with `grep -c '^- \[ \]'`; file grew by one line, the new Key constraints bullet)

| # | Location | Edit |
|---|----------|------|
| 1 | Execution Context, Key Constraints (new bullet after "Granularity and parallelism") | Added the labelled "Report-validity rule (applies to every gate)": a report counts only if the file exists, carries `Status: Complete` (or its prompt's closing marker, for example `## QA Complete`) and has a line-anchored verdict (`VERDICT: PASS\|FAIL`, `## Verdict: PASS\|FAIL`, `## Overall Verdict: PASS\|FAIL`, which are the forms the prompts already require). Required counts 3 / 6 / 7 / 2. Re-spawn once; if still invalid, synthetic BLOCKING finding (HIGH, `synthetic-dnsp`, affected range = lens/files, recommendation "Manual review required: partition agent failed twice"). Synthetic findings are not agent-fixable, get no gap-fill or fix edit, stay open in F_2 and F_3, and are cleared only by manual review via `team-lead`. Same test applies to verification reports. Non-QA items keep the old escape. |
| 2 | Steps 3.1, 3.2, 3.3 (Gate 1 report agents, 3) | Replaced "log the blocker, then mark complete" with: invalid-report test, log blocker, re-spawn ONCE with the same prompt, if still invalid log `SYNTHETIC-DNSP REQUIRED: <lens>`, then mark complete (Step 3.4 records the synthetic finding). |
| 3 | Steps 5.7, 5.8, 5.9, 5.10, 5.11, 5.12 (Gate 2 report agents, 6) | Same wording; each names its lens and its partition's `assigned_files` (synth-01..03 or synth-04..06); consolidation Step 5.13 records the synthetic finding. |
| 4 | Steps 6.2 to 6.8 (Gate 3 report agents, 7) | Same wording; each names its lens; consolidation Step 6.9 records the synthetic finding. |
| 5 | Steps 6.19, 6.20 (Gate 4 report agents, 2) | Same wording; consolidation Step 6.21 records the synthetic finding. (18 spawn items in total; `SYNTHETIC-DNSP REQUIRED` occurs 18 times; no old "If the agent cannot complete, log the specific blocker" wording remains in any rf-analyst, rf-qa or rf-qa-qualitative spawn item.) |
| 6 | Step 3.4 (Gate 1 consolidation) | Replaced the "If a report is missing ..." sentence with a REPORT-VALIDITY CHECK: exactly 3 valid reports named; re-spawn once only if the spawn item did not; for each still-invalid report write ONE synthetic BLOCKING finding (ID `SYN-<lens>`, HIGH, `synthetic-dnsp`, affected range, evidence = Task Log blocker entry, fixed recommendation string, marked NOT FIXABLE BY AGENTS) counted in F_1; record valid-report count (n of 3); verdict FAIL. Gap-fill count changed to "F_1 minus synthetic findings"; gap-fill item rule says "per non-synthetic BLOCKING gap"; added the only-synthetic case (`No gap-filling possible (only synthetic findings)`). Blocker is logged, item marked complete, synthetic finding carries the failure forward. |
| 7 | Step 5.13 (Gate 2 consolidation) | Same REPORT-VALIDITY CHECK for exactly 6 valid reports (partitions 1 and 2 of each of the three report types); synthetic finding ID `SYN-<lens>-p<partition>`, affected range = the partition's `assigned_files` slice verbatim; the Step 5.14 fix agent must leave it untouched; valid-report count (n of 6) recorded. |
| 8 | Step 6.9 (Gate 3 consolidation) | Same check for exactly 7 valid reports; Step 6.10 fix agent must leave synthetic findings untouched; count (n of 7). |
| 9 | Step 6.21 (Gate 4 consolidation) | Same check for exactly 2 valid reports; Step 6.22 fix agent must leave synthetic findings untouched; count (n of 2). |
| 10 | Steps 3.8, 5.17, 6.13, 6.25 (cycle-1 decision items) | F_2 now also counts unresolved synthetic findings from the consolidated file; added VERIFICATION-REPORT VALIDITY (overrides the item's missing-report escape): a verification report counts only if valid (a `SKIPPED:` stub is valid only when F_1 = 0); if F_1 > 0 and one is missing or invalid, re-spawn that verification agent once with its item's prompt, then add one synthetic BLOCKING finding to F_2 so the decision cannot be PASS. Decision order and halt strings are unchanged. |
| 11 | Steps 3.13, 5.22, 6.18, 6.30 (final verdict items) | Same treatment for F_3 (cycle-2 verification reports and unresolved synthetic findings). |
| 12 | Step 6.31 (QA completeness check) | Now verifies the valid review-1 report counts per gate (Gate 1: 3, Gate 2: 6, Gate 3: 7, Gate 4: 2, each file named) and that no synthetic BLOCKING finding is unresolved; a logged blocker never excuses a missing or invalid QA report; summary table gains "Valid review-1 reports (n of required)" and "Unresolved synthetic findings" columns; the STOP condition now also fires on a count below required or an unresolved synthetic finding; the "unable to complete due to missing files" escape excludes missing or invalid QA reports. |
| 13 | Step 7.2 (task outputs exist) | Added: a logged blocker never excuses a missing or invalid QA artefact; verify valid-report counts 3 / 6 / 7 / 2 and no unresolved synthetic finding; record counts in the table; a shortfall is a BLOCKING anomaly logged in `### Phase 6 - Assembly and QA Findings` and `### Follow-Up Items Identified`. |
| 14 | Step 7.6 (complete the task) | One clause added so Step 7.2's finding takes effect: status is not set to Done when Step 6.31 or 7.2 recorded a valid-report shortfall or an unresolved synthetic finding. Not named in the instruction list; it is the minimal link that makes edit 13 block completion. |

## Design choices to note

- The prompts require `## Verdict: PASS|FAIL` and `Status: Complete`, not the literal `VERDICT: PASS`. The rule accepts the forms the prompts already require plus `VERDICT: PASS|FAIL`, so no agent prompt had to change.
- Re-spawn happens in the spawn item; the consolidation item only re-spawns if the Task Log shows the spawn item did not, so an agent is never run more than twice.
- A synthetic finding cannot be repaired by a gap-fill or fix agent. Outcome by construction: it stays in F_2 and F_3, so the decision ends in HALT-MONOTONICITY (or the hard cap) and escalates to `team-lead`, which matches "Manual review required".
- Agent counts, lenses, fix_authorization flags, halt strings and decision order were not changed.

## Not done (out of scope for this fix)

- The fix-agent prompts (Steps 5.14, 5.19, 6.10, 6.15, 6.22, 6.27) were not edited; they are protected only by the consolidated-file marker "NOT FIXABLE BY AGENTS" and the instruction in the consolidation items.
- Medium findings M-1 to M-8 and Notes N-1 to N-9 remain open for later cycles.

## Verification

- `grep -c '^- \[ \]'` returns 83 (unchanged); `wc -l` 2,366 (was 2,365).
- `SYNTHETIC-DNSP REQUIRED` count 18; `REPORT-VALIDITY CHECK` count 4; `VERIFICATION-REPORT VALIDITY` count 8; `Report-validity rule` count 33.
- Spot-read of the Key Constraints bullet, Step 5.17 and Step 6.31 after editing: coherent.

## QA Complete

VERDICT: PASS (fix log only; B-1 edits applied, re-review by the verification agent still required)
