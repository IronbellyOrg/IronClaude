# Refactoring Plan

## Overview

- Base variant: Variant 2 (`variant-2-original.md`, reviewer-2 card, qa persona, opus class); base score 0.8465 against 0.791
- Incorporated: Variant 1 (F2, F3, the single-cause statement of F1), the five HIGH and UNADDRESSED invariant probe entries (INV-001, INV-002, INV-004, INV-005, INV-006) and the MEDIUM/LOW entries that sharpen a finding
- Planned changes: 12 (merged findings F1 to F15; some merge several sources)
- Risk: Low (additive and corrective edits to a review card; no plan file is touched)
- PLAN = `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md`. Paths are repo-relative. Every citation below was read from a card, a debate file or the probe, and spot-checked against live files by the orchestrator; the Wave 5 evidence validator re-reads them all.

## Planned Changes

The merged card keeps the base card's four sections (Verdict, Findings, Checked, Self-report) and the finding line format `F<n> | severity | blocking | category | claim | citations`. The merged findings are:

### Change 1: F1 (blocking, MAJOR, unpassable-check): the owner gates cannot be enforced by `/sc:implement`
- Source: V2 F1 (base) narrowed by Round 2 and probe INV-010, INV-011, INV-020.
- Claim: the operator who follows "Run `/sc:implement` on one phase at a time and stop at each gate" gets a run that cannot stop. `/sc:implement` takes one plan file, has no phase option, treats `## Phase N` as a group heading, fails with `E-PLAN-CHANGED` when the plan changes after the first task, and has no pause or ask path for an owner go. Constraints do reach QA, but only as a breach visible in the diff and quotable from the plan, which an owner's chat message never is. No task has an acceptance line that requires a recorded owner go, and PLAN:20 sets four go points (Phase 2, 3, 4 and 5), not three. The fix needs a decision the plan does not make: one managed plan per stage (the later plans read `./artifacts/` paths that would then sit in another package), or a gate task per boundary whose acceptance line accepts only an owner Ruling (a fix pass cannot invent one). The "inevitable bypass" wording of the first draft is dropped.
- Citations: PLAN:20; PLAN:139; src/superclaude/skills/sc-implement-protocol/SKILL.md:56; :87; :46; :105; src/superclaude/skills/sc-implement-protocol/refs/qa.md:52; :61; :247-249.

### Change 2: F2 (blocking, MAJOR, safety): Task 31 gates nothing and the fix is not a dependency line
- Source: V2 F2 (base) plus probe INV-001 and INV-002.
- Claim: the Phase 4 executor moves `pragmatic.md` to digest v2 even when seeded recall fails. PLAN:20 lists "the seeded-recall result of Task 31" as an entry condition, but Task 31 is the first task inside Phase 4 and only reports; Task 33 "Depends on: Task 31, Task 32". `/sc:implement` ignores `Depends on` lines and runs tasks in source order, so a stronger dependency line would also gate nothing. The only lever it honours is an acceptance line on Task 33 (for example that `./artifacts/seeded-recall-result.md` shows pass on all three requirements); a failure of that line halts the run and only an owner Ruling continues it. Task 31 cannot move to Phase 3, because source.md puts the run in Phase 4.
- Citations: PLAN:20; PLAN:376; PLAN:394; src/superclaude/skills/sc-implement-protocol/SKILL.md:91; :109; src/superclaude/skills/sc-implement-protocol/refs/qa.md:49; :247-249; .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md:15.

### Change 3: F3 (blocking, MAJOR, unpassable-check): Task 40's allow-list names a plugin mirror that Task 46 creates later
- Source: V1 F1 and V2 F3 second half (agreed, C-001) plus probe INV-008 and INV-015.
- Claim: the Task 40 executor gets a failing test in Phase 4. Task 40 allow-lists "`refs/rule.md` and its plugin mirror path" and requires a failure "when a file named there does not exist", but the mirror is created only in Task 46 (Phase 5). Task 13's allow-list text does not list the mirror either, while Task 40 reads its allow-list from Task 13's section. Leaving the mirror off the list instead fails the scan after Task 46 copies `rule.md` and `scale-map.md` into `plugins/superclaude/`, which the scan covers. The plan must choose how the entry is staged; the three problems with Tasks 13, 40 and 46 (this finding, F9 and F13) need one combined fix.
- Citations: PLAN:164; PLAN:170; PLAN:477; PLAN:482; PLAN:546; PLAN:549.

### Change 4: F4 (blocking, MAJOR, contradiction): Task 41 gives the analysis template a digest and a registry row the registry does not have
- Source: V1 F2 (unique to V1; confirmed by V2's advocate and probe INV-009, INV-012).
- Claim: the executor following Task 41 inserts a digest into `agent_template_analysis.md` and sets its registry row to `v2`, but Task 16 lists exactly 11 `digest` rows and none is for that template, and the live file has no definition sentence, only the merge-rule line. An unregistered fence fails the T2 reverse scan; a twelfth `digest` row breaks the "exactly 11 rows" check. The plan must choose: merge-rule text only for this template (then "five template files" becomes four), or a registered twelfth carrier.
- Citations: PLAN:199; PLAN:203; PLAN:303; PLAN:490; PLAN:493; PLAN:494; src/superclaude/templates/documents/agent_template_analysis.md:466.

### Change 5: F5 (blocking, MAJOR, unpassable-check): Task 25's T3 check fails on `commands/spec-panel.md:220` and its twins
- Source: V2 F4 (base) plus probe INV-007.
- Claim: Task 25's "passes" check fails in Phase 2. T3 fails when a carrier contains `src/superclaude`, and pointer-only rows go through T3; Task 16 registers `commands/spec-panel.md` as pointer-only and that file holds a `src/superclaude/` path at line 220. The plugin twin holds the same path (line 218), and the five installed-only variants hold it too, so editing line 220 alone still fails or breaks the twin parity of Task 45. The plan must choose: exempt `pointer-only` and `installed-only` rows from the path check (and keep the test off `~/.claude`), or edit every twin.
- Citations: PLAN:303; PLAN:199; src/superclaude/commands/spec-panel.md:220; plugins/superclaude/commands/spec-panel.md:218; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:918.

### Change 6: F6 (blocking, MAJOR, unpassable-check): later tasks make earlier acceptance lines false, so the final review cannot pass (NEW, probe INV-004)
- Source: probe INV-004 (no card reported it).
- Claim: the managed archive gate has a fresh reviewer verify every task's acceptance lines against the final files, and `issues` stops with `E-ARCHIVE-BLOCKED`. At least four lines are false by then: Task 16 (digest rows at state `legacy`, 19 rows in all) after Tasks 33 to 35, 41, 42 and 46; Task 25 ("passes with all `digest` rows at `legacy`") after the same tasks; Task 27 (the sentence "Preserve the highest severity rating when duplicates disagree" still appears) after Task 37 removes it; Task 13 (the allow-list lists the six stage 4 files) after Tasks 41 and 43 remove them. The package can never archive. The plan must say how superseded lines are scoped (for example "until Task N") or the final review will block.
- Citations: src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:55; :62; PLAN:203; PLAN:306; PLAN:333; PLAN:170; PLAN:446.

### Change 7: F7 (blocking, MAJOR, missing-requirement): the fresh-findings set and the held-out split are never evaluated
- Source: V1 F3 (base-incorporated), widened by probe INV-006; grade ruled by the judge.
- Claim: the executor can finish all 46 tasks without evaluating the classifier on the fresh-findings population or on the held-out half. Task 6 states the evaluation "is run at stage 2, not here"; no task after Phase 1 consumes `./artifacts/fresh-findings.md`, records judge answers or writes an evaluation result, and Task 5's held-out split is likewise never used. The spec names the held-out evaluation as plan work. Classifier authority is off (OD4), so no decision rests on the result, but the deliverable is required and the owner's stage 2 exit numbers depend on it.
- Citations: PLAN:87; PLAN:93; PLAN:79; PLAN:328; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:934.

### Change 8: F8 (blocking, MAJOR, missing-requirement): the Phase 3 to 5 entry numbers are undefined or have no task (NEW, probe INV-005)
- Source: probe INV-005.
- Claim: PLAN:20 requires "at least 5 observed shadow runs with zero safety misses and no capture failure", but "safety miss" is defined nowhere in the plan, and the stage 2 exit items (ledger volume, `consumer-unknown` share, offers answered, shadow agreement) and the stage 3 audit-window numbers (revert triggers) have no task that measures or reports them. The spec says no stage starts before the owner has seen the numbers. A gate task that only records the owner's go (the F1 fix) is therefore not enough: the owner has no numbers to read.
- Citations: PLAN:20; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:940; :946; :947.

### Change 9: F9 (MINOR, non-blocking): Task 46 copies the skill folder before adding the plugin `canonical` registry row
- Source: V1 F4 and V2 F5 (agreed, C-002), plus probe INV-008 (second file).
- Claim: the plugin mirror's `registry.yaml` differs from the source immediately before the T15 parity check; add the row first or repeat the copy. The same ordering applies to `refs/scale-map.md` if F3's fix edits it. Part of the combined fix of F3.
- Citations: PLAN:546; PLAN:549.

### Change 10: F10 (MINOR, non-blocking): the seeded-recall pass line can be met on an underpowered set (probe INV-003)
- Claim: Task 7 lets the sizing "state plainly which classes cannot reach it", and "safety recall equals the old rule's" sets no tolerance; at about 0.95 expected recall a 5-point Wilson half-width needs about 70 planted defects per gating class, which does not fit a "fresh short spec". With small n, both texts can find every safety defect and pass by equality while saying little. State a minimum n or call the pass line advisory.
- Citations: PLAN:97; PLAN:102; PLAN:376.

### Change 11: F11 (MINOR, non-blocking): Task 31 does not alternate the order or require fresh spawns (probe INV-018)
- Claim: Task 31 says "Spawn the same three reviewer agents twice" with no order alternation, while Task 4 alternates; if "same" means the same running agents, the second pass has seen the planted defects and inflates new-rule recall.
- Citations: PLAN:376; PLAN:64.

### Change 12: F12 (MINOR, non-blocking): T3 may fail a `pointer-only` row before its pointer exists (probe INV-019)
- Claim: the `pointer-only` files get their pointer only in Tasks 42 and 45, so a T3 that fails a pointer-only row without a pointer fails Task 25 in Phase 2 for `document_review_loop_prompts.md`; state that T3 checks such a row only once its pointer is present.
- Citations: PLAN:303; PLAN:502; PLAN:535.

### Change 13: F13 (MINOR, non-blocking): wording-dependent scan trips in `scale-map.md` and `rule.md`
- Source: V2 F3 first half (C-007, ruled minor) plus probe INV-014.
- Claim: Task 13's section "names the files allowed to contain the phrases"; an executor who writes the three phrases literally trips Task 40's scan on `scale-map.md` and its plugin copy; a path-only list avoids it. Likewise `rule.md` quoting the old definition sentence would fail Task 46's grep and the strict T2 scan. State that both files must not quote the phrases or the old sentence.
- Citations: PLAN:164; PLAN:170; PLAN:152; PLAN:477; PLAN:551.

### Change 14: F14 (MINOR, non-blocking): coverage-matrix omissions in the review run (V2 F6, C-009)
- Claim: the matrix omits requirement-bearing source lines 22, 41, 43 and 47 and maps four rows to the Constraints block (`best_task: 0`); the plan covers them all (Tasks 16, 20, 25, 33, 37, 38). Matrix quality only; the matrix is a review-run artifact.
- Citations: .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md:22; source.md:41; source.md:43; source.md:47; PLAN:401; PLAN:455.

### Change 15: F15 (MINOR, non-blocking): installed reference files cite `.dev/` package paths (probe INV-016)
- Claim: Task 15 tells `refs/classifier-questions.md`, an installed file, to cite `./artifacts/classifier-input-availability.md` and PF `08-test/results.md`; neither resolves in an installed `~/.claude/skills/` copy. T3 checks only for `src/superclaude`, so nothing catches it.
- Citations: PLAN:188; PLAN:303.

## Changes NOT Being Made

- V2's "Tasks 11 to 46 therefore run straight through" is NOT kept; replaced by the narrower F1 claim that the executor has no mechanism to stop for an owner go (debate points C-005, A-001).
- V2 F3 is split: the missing-mirror half stays blocking (F3); the wording-dependent self-trip half is minor (F13).
- The base card's Checked section is kept; V1's Checked bullets are folded in where they add a verified anchor.
- No probe MEDIUM/LOW entry that the debate marked ADDRESSED (INV-009, INV-012, INV-013, INV-015, INV-017, INV-020) becomes a finding; INV-011 (four go points) is folded into F1.

## Risk Summary

All changes are text edits to one review card; rollback is re-copying `variant-2-original.md`. Risk is that a probe-sourced finding (F6, F8) is graded too high: both cite concrete protocol lines and are marked with their source so the evidence validator can drop them if a citation fails.

## Review Status

Auto-approved (non-interactive).
