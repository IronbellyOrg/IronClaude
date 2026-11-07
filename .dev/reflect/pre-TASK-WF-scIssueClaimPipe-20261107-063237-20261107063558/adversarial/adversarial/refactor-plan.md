# Refactoring Plan: merge into Variant 1

Base: `variant-1-original.md` (reviewer 1, sonnet, analyzer). Output: `merged-output.md` (merged review card) and `../merged-verdict.yaml`.
Fix-location vocabulary used below: **plan only** = the plan author can fix it by editing the plan; **design first** = `source.md`/`docs/designs/sc-issue-claim-pipeline-flag.md` must be amended before the plan is right.

## Overview

- Base findings kept: all nine from V1, with classes and severities changed as Round 2 settled them.
- Incorporated: V3 (C-007, C-009, U-004, C-011, C-013), V2 (C-008 grade, C-010), invariant probe (INV-002, 003, 004, 006, 008, 009 as MEDIUM, INV-005, 010, 013 as LOW), Round 2 (N-001).
- Merged finding groups: 6 blocking, 6 non-blocking Drift (MEDIUM), 5 minor/notes.
- Overall risk: Medium. All changes are edits to the card; no repository file changes.

## Planned Changes

### Change 1: reclassify V1 findings 1 and 2 from Regression to Drift
- Source: Round 2 (all three advocates), `debate-round2.md`.
- Target: V1 deviations 1 and 2.
- Approach: replace. Finding 2 (write-verb audit): Drift, HIGH, **blocking** (suite certainly fails; unnamed test file; guidance missing). Finding 1 (inventory test): Drift, MEDIUM, non-blocking (self-heals at Task 4 acceptance for the script row and at Task 7 for the template row; never gating).
- Risk: Low.

### Change 2: merge INV-001 and INV-002 into finding 2
- Source: invariant probe. Add: Tasks 1, 3 and 4 also edit audited files; the template's push and commit lines need a category; editing an already-classified line without updating its key fails the stale-key test (INV-001 kept at LOW: the claim that `--submit` makes those lines false is not established).
- Risk: Low.

### Change 3: tracked-files data (V1 finding 3 + V3 advisory 2 + INV-003 + INV-005)
- Merge into one **blocking** finding: Drift, MEDIUM-HIGH. The `worktree` output needs a machine-readable tracked-files field (stdout of the subcommand, not the `worktree.json` record); when `git ls-files` fails the copy must not overwrite a differing file (data-loss guard).
- Fix location: design first (source.md §8.3 output schema), then Tasks 2 and 4.

### Change 4: fork safety for the launch prompt (V3 advisory 3 / C-013 + INV-007)
- New **blocking** finding (security): the `submit` block's PR check must name `--repo IronbellyOrg/IronClaude` on every gh call; the fork-safety scan or a new pin must cover `templates/launch-prompt.md`.
- Fix location: design first (§9, §13), then Tasks 5 and 7.

### Change 5: shared return contract (INV-004)
- New **blocking** finding: SKILL.md:101-115 is one contract for both modes; Task 7's "replace the claim-mode return contract with the ten fields" would drop `status`, `issue_number`, `next_steps_path` or alter create mode; ST-10 would still pass.
- Fix location: design first (§10 wording: extend, do not replace), then Task 7.

### Change 6: ST-4 rule (V1 finding 5 + V3 advisory 1 + INV-006)
- Merge into one **blocking** finding: ST-4 must use whole-token matching limited to orca command lines (`--pr` is a prefix of `--prompt`; `--issue-url` exists in refs/claim.md:49 and clickup_claim.py), and it must survive ruff wrapping the launch argv (parse the argv with `ast` instead of scanning lines).
- Fix location: design first (§13 ST-4), then Task 7.

### Change 7: missing required tests and dropped safeguards (V1 finding 6 + V2 findings 1-3 + V3 findings 5-7 + V1 finding 9)
- Merge into one **blocking** finding (missing required deliverables): LA-7, ARG-1 across all subcommands (Task 1 can only test `preflight`), ST-5 template row, ST-6 Wave 8 half, Task 6 timeout detail ("check Orca before re-running"), hand_command note (not governed by the hook), pending record stays. Grade the Task 6 safeguards MEDIUM (V2), the ARG-1 part LOW-MEDIUM.
- Fix location: plan only.

### Change 8: non-blocking Drift (MEDIUM)
- M-1 inventory test red windows (Change 1 finding): add the files-table row in Tasks 1 and 5 (plan only).
- M-2 launch warning precedence and `enforcement_hook` value on `already_launched`; worktree has the same collision (V1 finding 4 + INV-008) (design first).
- M-3 SKILL.md claim steps 6 and 7 (MEDIUM, V3) and SKILL.md/command `description` (LOW), plus other stale command text issue.md:71, :100 and the Outputs row (V1 finding 8) (plan only).
- M-4 Tasks 7 and 9 do not depend on Task 3 (V3 finding 2) (plan only).
- M-5 re-claim rewrites launch-prompt.md and the copy while an agent is running (INV-009) (design first).
- M-6 a create that times out is indistinguishable from a failed create in `run()` (N-001, Round 2 advocate 3) (plan only: Task 1 marks timeouts, Task 2 adds a create-timeout case).

### Change 9: minor findings and notes (non-blocking)
- Orca-dependency constraint absent from Constraints (V2 finding 5 / C-010) LOW, plan only.
- Task 2 too large; format check only in Task 9; design-doc edits in Phase 3 vs design section 16 (V3 findings 8-10 / C-011) LOW notes; V3 withdrew most of the lint point because the implement protocol runs `make lint` per task as a non-gating extra.
- Pending-store intermediate directory modes (C-014), already_launched time field and `-k` filter naming (C-015), pending store grows without the hook (INV-010), Task 9 never runs tests/docs, ASCII-only HOW-WE-WORK row (INV-013).
- The `--repo` literal ban in commands/issue.md (U-004): ADDRESSED (Task 3's acceptance runs that test); kept as a note for the implementer.

### Change 10: add what no card had
- Every merged finding gets a fix and a fix location (Completeness.4 and Risk.2 were NOT MET for all three cards).
- Add an "Advisory correctness gaps" section with the three V1 advisory items (corrected), kept non-gating.
- Fix V1's two wrong citations in place (done before the debate): plan:130, source.md:357 removed.

## Changes NOT Being Made

| Diff point | Alternative | Why rejected |
|---|---|---|
| S-002, X-001 | V1 and V3's Regression label for the test-order window | Round 2: all three advocates accepted Drift; the final repository state is correct and the check is non-gating |
| X-004 / V3 finding 5 | "ARG-1 and LA-7 never named" at MEDIUM as written | Overstated: Task 1 tests a bad-subcommand exit and Task 5 tests `--submit` with `worktree`; kept only the missing per-subcommand coverage |
| Wave 6 hand-off overlap | V1's new LOW issue | Advocate 2 and advocate 3 showed plan:124-133 gives Task 7 the final wording; no separate defect |
| C-011 lint gate | V3 finding 9 as a deviation | Withdrawn in Round 2: `make lint` runs per task as a non-gating extra (sc-implement-protocol SKILL.md:132-154); format-check gap kept as a note |
| INV-001 premise | Probe's "`--submit` makes the classified lines false" | The classified lines describe the skill, which remains the only writer; a launched agent is a separate session |
| A-005 | "Green between tasks is required" | Rejected as a universal rule; only acceptance gates and the final state must be green |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Low | Labels only | Revert the card edit |
| 3-7 | Medium | New blocking findings change the verdict to FAIL | Each cites a verified file:line; evidence-validator re-Reads them |
| 8-9 | Low | Non-blocking | n/a |

## Review Status

Auto-approved (non-interactive). Reviewed by the merge-executor's pre-merge check of every citation.
