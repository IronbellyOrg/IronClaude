# Refactoring Plan

## Overview

- Base variant: Variant 1 (`variant-1-original.md`, reviewer-1 card, analyzer persona, haiku class), chosen by the tiebreaker (correctness criteria 9 against 7; combined scores 0.7525 against 0.7905 are within 5 percent and the two scoring passes disagree on the winner).
- Incorporated: Variant 2 (F1 to F3, its Checked bullets) and the invariant probe entries INV-002, INV-005, INV-006, INV-007, INV-009, INV-010, INV-011, INV-012, plus the Task 10 gap from the calibrators and Round 2.
- Merged findings: 11 (F1 and F2 blocking; F3 to F7 Medium, non-blocking; F8 to F11 minor, non-blocking).
- Risk: Low (edits to a review card only; no plan file is touched).
- PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md`; PF = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115`. Every citation below was taken from a card, a debate file or the probe, and the orchestrator re-read the ones for F1, F2, F3, F4 and F11 against the live files; the Wave 5 validators re-read all of them.

## Planned Changes

The merged card keeps the sections Verdict, Findings, Checked and Self-report, and the finding format `F<n> | severity | blocking | category | claim | citations` with a bullet list of citations.

### Change 1: F1 (MAJOR, blocking true, data-loss): Task 3's in-place rerun overwrites its evidence source
- Source: base V1 F1, with the fix from Round 2 and the probe INV-001, INV-002, INV-003.
- Claim: Task 3 tells the executor to re-run `08-test/evaluate.py` from PF "first". The script derives its folder from its own location and writes `results.md` there unconditionally, so the rerun replaces PF `08-test/results.md` and deletes its hand-added lines 54 to 93 (the diagnosis, AUCs, limits, kappa and per-kind split); no script in PF regenerates them. `results.md` is staged and was never committed, and the `git add .dev/tasks` that the executor runs re-stages the tree, so the old content would survive only as an unreferenced git object. The rerun also breaks the plan's own rule that only the spec is edited outside `./artifacts/`, and Task 3's "confirm the figures still match" then compares the file with itself. The plan must decide: no in-place rerun (cite the hand-added figures from the file; any reproducibility check runs on a real copy of `05-scoring/`, `07-classifier/` and `08-test/` and compares only lines 1 to 52), plus an acceptance line that detects a change in `results.md` (a SHA-256 before and after, or the git blob id `d9616dd28fbb08daa565b11c69ef75cb7819f274`; a hash detects a change but does not prevent it).
- Citations: PLAN:52; PLAN:21; PF/08-test/evaluate.py:110; PF/08-test/evaluate.py:11; PF/08-test/results.md:54; PF/08-test/results.md:83-89; src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:36.

### Change 2: F2 (MAJOR, blocking true, other): Task 4's graders carry the old rule through the SubagentStart hook
- Source: probe INV-006 (no card reported it); grade ruled by the judge.
- Claim: Task 4 grades each of the 318 findings under "the old rule text" and "the new rule text" with three blind agents. Every subagent in a session with the `pragmatic` output style gets the old rule (the sentence at `pragmatic.md:225`) injected by the SubagentStart hook `pragmatic-subagent.js`, so the "new text" arm is graded with the old rule still in context. That biases the old-to-new movement count, the headline number the owner reads in Task 10, toward "no change", and neither Task 4 nor its acceptance lines name the confound. The same confound affects the stage 3 seeded-recall passes. The plan must record it as a stated limit of the movement counts, or name a way to spawn the graders without the injection and record how.
- Citations: src/superclaude/hooks/hooks.json:173; src/superclaude/output-styles/pragmatic.md:225; PLAN:65; PLAN:69; PLAN:136.

### Change 3: F3 (MINOR, blocking false, missing-requirement): Task 9's sweep misses two stale spec lines
- Source: probe INV-005.
- Claim: besides section 7.4, 7.6 and 12, the spec still says "Over-fitting the classifier to 30 to 40 rows" in the section 14 risk register and "whether a calibration table of 30 or more scored findings will exist in time" in section 17.3. Task 9's acceptance grep (`15 to 20\|was empty`) matches neither, so per-task QA passes with both stale lines in place. Add the two lines to the edit list and widen the grep (for example `30 to 40 rows\|30 or more scored`). Section 17 also contradicts the plan's statement that a Grep found nothing there.
- Citations: PF/02-brainstorm/merged-requirements.md:1011; PF/02-brainstorm/merged-requirements.md:1108; PLAN:123; PLAN:126.

### Change 4: F4 (MINOR, blocking false, other): Task 5's cluster rule does not keep repeats on one side
- Source: probe INV-007.
- Claim: the six keyword clusters of `06-blocker-characteristics.md` cover 43 of the 318 rows (the 82 blocker descriptions only; the 236 non-blocker rows were never clustered), and the file names the clusters but not their keywords. Task 5 places "rows in no cluster" at random, so repeats of one defect among the other rows can land in both halves, and the acceptance line checks only the named clusters. State the keywords, apply them to all 318 rows and group exact repeats before the random split.
- Citations: PF/06-blocker-characteristics.md:26; PLAN:77; PLAN:81.

### Change 5: F5 (MINOR, blocking false, missing-requirement): Task 10's acceptance lines omit what its body asks for
- Source: both calibrators, Round 2 (opus advocate) and probe INV-012.
- Claim: Task 10's body asks for the owner-decision list (OD3, OD4) and the five findings that matter most, but its acceptance lines (PLAN:139 to 142) require neither, so per-task QA would pass a summary without them. Task 10 will also report the stage ledger from `stage-requests/README.md`, whose stage 0 row still reads "(filled when generated)" while this package exists, and PLAN:21 forbids editing that file. One added acceptance line fixes the first; the second needs a decision (allow the ledger row to be updated, or have Task 10 name this package id itself).
- Citations: PLAN:136; PLAN:139-142; .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/source.md:17; PF/stage-requests/README.md:17; PLAN:21.

### Change 6: F6 (MINOR, blocking false, other): Task 2's frame is left to the executor
- Source: V2 F2, graded Medium by the debate (C-003).
- Claim: Task 2 does not say how the executor identifies and de-duplicates minor findings across the run-2 QA folder (139 files in mixed formats) or how the code decides that a flaw "appears uncorrected". The executor chooses, and no acceptance line requires the choice to be written in the result file. Task 2's reproducible script records the frame in code, so the result is not wrong, but the estimate rests on a choice nobody must state.
- Citations: PLAN:42; PLAN:45-48; .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/gate5-cycle-control.md:1.

### Change 7: F7 (MINOR, blocking false, other): Tasks 5 and 6 both include the Task 2 sample
- Source: V2 F3(b), debate C-005, probe INV-011.
- Claim: Task 5 records the reviewer-called-minor set (the Task 2 sample) in `stage0-heldout-ids.json` and Task 6 adds the same sample to the fresh-findings set, while stage 2 is told to evaluate both sets; pooling them counts the same findings twice. PLAN:77 also says the fresh findings are "never placed in either half" yet part of them is recorded by Task 5 itself. Name one home for the sample, or tell stage 2 not to pool.
- Citations: PLAN:77; PLAN:90; PF/stage-requests/README.md:32.

### Change 8: F8 (MINOR, blocking false, other): Task 7's recall sizing will fall back to advisory
- Source: V2 F3(a), debate C-004 (minor note).
- Claim: at an expected recall of 0.90 to 0.95 a 5-point Wilson half-width needs about 73 to 138 planted defects per gating class, which a fresh short spec cannot hold, so every gating class will almost certainly use the advisory fallback that PLAN:104 allows. Nothing goes wrong, but the stage 3 pass line will then be advisory.
- Citations: PLAN:100; PLAN:104.

### Change 9: F9 (MINOR, blocking false, missing-requirement): the always-staged constraint is missing from the plan
- Source: V2 F1, debate C-002, T1 calibrator.
- Claim: `source.md` asks to keep the constraint that `.dev/tasks/` is always staged and never described as "never staged"; the plan's Constraints do not carry it. The global instructions still bind the executor, so no task behaves differently.
- Citations: .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/source.md:13; PLAN:17-26.

### Change 10: F10 (MINOR, blocking false, unpassable-check): Task 6's disjointness check cannot fail
- Source: probe INV-009.
- Claim: Task 6 checks each fresh finding id against the master table, but the ids use different formats (`F1` to `F17` in the merged card, `F-B01-001` style in the master table), so the check passes whatever the content. The populations are disjoint in fact (different source and date); the check should compare source paths.
- Citations: PLAN:95; .dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/adversarial/merged-review-card.md:19; PF/04-historical/master-table.md:7.

### Change 11: F11 (MINOR, blocking false, other): some Evidence paths in the master table can be read only through git
- Source: probe INV-010.
- Claim: 15 master-table rows cite files marked `@E2`, which were read with `git show` from the branch `origin/ironbelly/eval-tasklist-review-panel` and do not exist in this worktree. Task 8's rule "cited path and line exist" fails those rows unless the executor uses `git show` on that branch, which the plan does not say, so the verified-evidence count is silently lower by up to 15 of 318.
- Citations: PLAN:110; PF/01-historical-inventory.md:11.

## Changes NOT Being Made

- V2's PASS-with-notes verdict is NOT kept; the merged verdict is NEEDS-REVISION (X-001, conceded by V2's advocate).
- V1's claim that the rerun deletes "Task 9's evidence pointer" is narrowed: the path survives, the content it cites does not.
- V2's "a short spec cannot hold that many defects" is softened to "will almost certainly use the advisory fallback".
- Probe entries INV-003, INV-004, INV-008 and INV-013 (ADDRESSED, LOW) are used only as Checked bullets, not findings.

## Risk Summary

All changes are text edits to one review card; rollback is re-copying `variant-1-original.md`. Risk is that F2 (the hook confound), found only by the probe, is graded too high; it cites the hook file and the old-rule sentence and the validators will re-read both.

## Review Status

Auto-approved (non-interactive).
