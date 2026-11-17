merged_from: reviewer-1, reviewer-2, invariant-probe

<!-- Merged review card. Base variant: variant-1-original.md (reviewer-1, analyzer persona, haiku class). Merge date: 2026-11-16. Non-base sources: variant-2-original.md (reviewer-2, qa persona, opus class) and invariant-probe.md (Round 2.5 fault-finder). Plan: refactor-plan.md. -->
<!-- PLAN = .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md ; PF = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115 (written out in full in the citations below). -->

## Verdict
NEEDS-REVISION. Two blocking findings (2): Task 3's required in-place rerun overwrites its own evidence file (data loss), and Task 4's "new text" graders still receive the old rule through the SubagentStart hook.

## Findings

<!-- Source: Variant 1 F1 (base), with the Round 2 fix and probe INV-001, INV-002, INV-003 -->
F1 | severity MAJOR | blocking true | category data-loss | Task 3 tells the executor to re-run `08-test/evaluate.py` from PF "first". The script derives its folder from its own location and writes `results.md` there unconditionally, so the rerun replaces PF `08-test/results.md` and deletes its hand-added lines 54 to 93 (the diagnosis, AUCs, limits, kappa and per-kind split); no script in PF regenerates them. `results.md` is staged and was never committed, and the `git add .dev/tasks` that the executor runs re-stages the tree, so the old content would survive only as an unreferenced git object. The rerun also breaks the plan's own rule that only the spec is edited outside `./artifacts/`, and Task 3's "confirm the figures still match" then compares the file with itself. The plan must decide: no in-place rerun (cite the hand-added figures from the file; any reproducibility check runs on a real copy of `05-scoring/`, `07-classifier/` and `08-test/` and compares only lines 1 to 52), plus an acceptance line that detects a change in `results.md` (a SHA-256 before and after, or the git blob id `d9616dd28fbb08daa565b11c69ef75cb7819f274`; a hash detects a change but does not prevent it). | citations:
- PLAN:52 "from PF first and confirm the figures still match the file"
- PLAN:21 "The only file outside `./artifacts/` that a task here edits"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/08-test/evaluate.py:110 "(HERE / "results.md").write_text("\n".join(out) + "\n")"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/08-test/evaluate.py:11 "HERE = Path(__file__).resolve().parent"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/08-test/results.md:54 "## Diagnosis (added by hand after the run;"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/08-test/results.md:83-89 "## Spec section 7.6 items measured (added after the run)"
- src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:36 "`.dev/tasks/` is always staged (`git add .dev/tasks`)"

<!-- Source: invariant probe INV-006 (no reviewer card reported it); grade ruled by the judge -->
F2 | severity MAJOR | blocking true | category other | Task 4 grades each of the 318 findings under "the old rule text" and "the new rule text" with three blind agents. Every subagent in a session with the `pragmatic` output style gets the old rule (the sentence at `pragmatic.md:225`) injected by the SubagentStart hook `pragmatic-subagent.js`, so the "new text" arm is graded with the old rule still in context. That biases the old-to-new movement count, the headline number the owner reads in Task 10, toward "no change", and neither Task 4 nor its acceptance lines name the confound. The same confound affects the stage 3 seeded-recall passes. The plan must record it as a stated limit of the movement counts, or name a way to spawn the graders without the injection and record how. | citations:
- src/superclaude/hooks/hooks.json:173 "node \"$HOME/.claude/hooks/pragmatic-subagent.js\""
- src/superclaude/output-styles/pragmatic.md:225 "Grade every review finding as blocking or minor. Blocking is a real defect"
- PLAN:65 "Spawn three blind agents that did not write the rule or the spec."
- PLAN:69 "the old-to-new movement counts and the three-agent spread"
- PLAN:136 "the one file the owner reads before saying go for stage 1"

<!-- Source: invariant probe INV-005 -->
F3 | severity MINOR | blocking false | category missing-requirement | Task 9's sweep misses two stale spec lines. Besides section 7.4, 7.6 and 12, the spec still says "Over-fitting the classifier to 30 to 40 rows" in the section 14 risk register and "whether a calibration table of 30 or more scored findings will exist in time" in section 17.3. Task 9's acceptance grep (`15 to 20\|was empty`) matches neither, so per-task QA passes with both stale lines in place. Add the two lines to the edit list and widen the grep (for example `30 to 40 rows\|30 or more scored`). Section 17 also contradicts the plan's statement that a Grep found nothing there. | citations:
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:1011 "RK8 | Over-fitting the classifier to 30 to 40 rows"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:1108 "whether a calibration table of 30 or more scored findings will exist in time"
- PLAN:123 "a Grep when the plan was written found none there"
- PLAN:126 "`grep -n "15 to 20\|was empty"`"

<!-- Source: invariant probe INV-007 -->
F4 | severity MINOR | blocking false | category other | Task 5's cluster rule does not keep repeats on one side. The six keyword clusters of `06-blocker-characteristics.md` cover 43 of the 318 rows (the 82 blocker descriptions only; the 236 non-blocker rows were never clustered), and the file names the clusters but not their keywords. Task 5 places "rows in no cluster" at random, so repeats of one defect among the other rows can land in both halves, and the acceptance line checks only the named clusters. State the keywords, apply them to all 318 rows and group exact repeats before the random split. | citations:
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/06-blocker-characteristics.md:26 "hit 54 matches and cover 43 distinct rows; 39 rows match none"
- PLAN:77 "rows in no cluster are split at random with a recorded seed"
- PLAN:81 "No cluster named in PF `06-blocker-characteristics.md` appears in both halves"

<!-- Source: both calibrators, Round 2 (opus advocate) and probe INV-012 -->
F5 | severity MINOR | blocking false | category missing-requirement | Task 10's acceptance lines omit what its body asks for. Its body asks for the owner-decision list (OD3, OD4) and the five findings that matter most, but its acceptance lines (PLAN:139 to 142) require neither, so per-task QA would pass a summary without them. Task 10 will also report the stage ledger from `stage-requests/README.md`, whose stage 0 row still reads "(filled when generated)" while this package exists, and PLAN:21 forbids editing that file. One added acceptance line fixes the first; the second needs a decision (allow the ledger row to be updated, or have Task 10 name this package id itself). | citations:
- PLAN:136 "the five findings of this stage that matter most for the stage 1 go"
- PLAN:139-142 "the headline number or result for each of Tasks 1 to 9"
- .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/source.md:17 "the stage ledger of `stage-requests/README.md` (which stage packages exist)"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:17 "(filled when generated)"
- PLAN:21 "The only file outside `./artifacts/` that a task here edits"

<!-- Source: Variant 2 F2, graded Medium by the debate (C-003) -->
F6 | severity MINOR | blocking false | category other | Task 2's frame is left to the executor. Task 2 does not say how the executor identifies and de-duplicates minor findings across the run-2 QA folder (139 files in mixed formats) or how the code decides that a flaw "appears uncorrected". The executor chooses, and no acceptance line requires the choice to be written in the result file. Task 2's reproducible script records the frame in code, so the result is not wrong, but the estimate rests on a choice nobody must state. | citations:
- PLAN:42 "of de-duplicated minor findings from Gates 2 to 5 and the final validation"
- PLAN:45-48 "reports hits, n, the seed and a Wilson 95 percent interval computed by"
- .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/gate5-cycle-control.md:1 "# Gate 5 cycle control (Items 6.62 and 6.67)"

<!-- Source: Variant 2 F3(b), debate C-005, probe INV-011 -->
F7 | severity MINOR | blocking false | category other | Tasks 5 and 6 both include the Task 2 sample. Task 5 records the reviewer-called-minor set (the Task 2 sample) in `stage0-heldout-ids.json` and Task 6 adds the same sample to the fresh-findings set, while stage 2 is told to evaluate both sets; pooling them counts the same findings twice. PLAN:77 also says the fresh findings are "never placed in either half" yet part of them is recorded by Task 5 itself. Name one home for the sample, or tell stage 2 not to pool. | citations:
- PLAN:77 "are a third population and are never placed in either half"
- PLAN:90 "add the reviewer-called-minor sample of Task 2"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:32 "Stage 2 evaluates the classifier on the fresh-findings set, the held-out half"

<!-- Source: Variant 2 F3(a), debate C-004 (minor note) -->
F8 | severity MINOR | blocking false | category other | Task 7's recall sizing will fall back to advisory. At an expected recall of 0.90 to 0.95 a 5-point Wilson half-width needs about 73 to 138 planted defects per gating class, which a fresh short spec cannot hold, so every gating class will almost certainly use the advisory fallback that PLAN:104 allows. Nothing goes wrong, but the stage 3 pass line will then be advisory. | citations:
- PLAN:100 "state a minimum n per gating class (safety, decision-bearing, missing)"
- PLAN:104 "or marks that class's pass line advisory and shows the interval"

<!-- Source: Variant 2 F1, debate C-002, T1 calibrator -->
F9 | severity MINOR | blocking false | category missing-requirement | The always-staged constraint is missing from the plan. `source.md` asks to keep the constraint that `.dev/tasks/` is always staged and never described as "never staged"; the plan's Constraints do not carry it. The global instructions still bind the executor, so no task behaves differently. | citations:
- .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/source.md:13 "`.dev/tasks/` is always staged and never described as "never staged""
- PLAN:17-26 "## Constraints"

<!-- Source: invariant probe INV-009 -->
F10 | severity MINOR | blocking false | category unpassable-check | Task 6's disjointness check cannot fail. Task 6 checks each fresh finding id against the master table, but the ids use different formats (`F1` to `F17` in the merged card, `F-B01-001` style in the master table), so the check passes whatever the content. The populations are disjoint in fact (different source and date); the check should compare source paths. | citations:
- PLAN:95 "a check of each ID against PF `04-historical/master-table.md` finds none"
- .dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/adversarial/merged-review-card.md:19 "F1 | MAJOR | blocking true | contradiction"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/04-historical/master-table.md:7 "| F-B01-001 | S-002 |"

<!-- Source: invariant probe INV-010 -->
F11 | severity MINOR | blocking false | category other | Some Evidence paths in the master table can be read only through git. 15 master-table rows cite files marked `@E2`, which were read with `git show` from the branch `origin/ironbelly/eval-tasklist-review-panel` and do not exist in this worktree. Task 8's rule "cited path and line exist" fails those rows unless the executor uses `git show` on that branch, which the plan does not say, so the verified-evidence count is silently lower by up to 15 of 318. | citations:
- PLAN:110 "when the cited path and line in its `Evidence` column exist"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/01-historical-inventory.md:11 "`@E2` in a path means the file was read from `origin/ironbelly/eval-tasklist-review-panel`"

## Checked
<!-- Source: Checked bullets of Variant 1 and Variant 2 (duplicates dropped), plus the probe's count checks -->
- Task 9's stale-table targets exist where the plan says: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:572` "15 to 20 rows" and `:609` "was empty", stage 0 row at `:944`; these are not invented anchors. RT1 and RT2 are in section 13.2 (`:985-986`) and M12 is in section 13.1 (`:974`). The drafted safety-miss definition agrees with RT1 and with "zero safety misses" in section 12 (`:946-947`).
- The three staging decisions in Task 9 match `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:27-29`, and the stage ledger file exists (`README.md:13-21`).
- Task 4: `src/superclaude/output-styles/pragmatic.md:221` and `:231` are the bullets the plan names, and the section 4.1 digest block is at `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:195-207`.
- The seeded-set fallback is explicit, not an unpassable sizing check: PLAN:104 permits an advisory pass line with the resulting interval.
- No task edits anything under `src/`, `tests/`, `.claude/` or `plugins/`. Only Task 9 edits a file outside `./artifacts/`, and that file is the spec in PF (PLAN:21, PLAN:123).
- Count check: 318 rows in PF `04-historical/master-table.md` and in each of `blind-table-1.md`, `blind-table-2.md` and `blind-table-3.md`; 1908 = 318 x 3 x 2 grades (PLAN:68).
- Count check: Task 6's card holds 17 findings (`.dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/adversarial/merged-review-card.md:70`, "F1 to F17").
- Count check: the plan has 10 tasks in 4 phases (PLAN:28, 59, 84, 117).
- The C-001 fix (no in-place rerun, run on a real copy) leaves PF untouched apart from Task 9's spec edit: Task 1 is read-only `grep -rn`; Tasks 2, 4, 6, 7, 8 and 10 write only under `./artifacts/`; the only other in-PF write is a gitignored bytecode cache.
- Task 9's edit breaks no earlier task's evidence: no task after Task 9 reads the spec, Task 1's counts grep `src/`, `plugins/` and `.claude/` and not PF, and Task 4 uses section 4.1, which Task 9 does not edit.

## Self-report
confidence: 0.85
reviewer_model_self_report: merged by adversarial pipeline; base reviewer-1 (haiku class), incorporated reviewer-2 (opus class) and the fault-finder probe
