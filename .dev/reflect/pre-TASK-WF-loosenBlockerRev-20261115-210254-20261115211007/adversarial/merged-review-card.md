merged_from: reviewer-1, reviewer-2, invariant-probe

<!-- Merged review card. Base variant: variant-2-original.md (reviewer-2, qa persona, opus class). Merge date: 2026-11-15. Non-base sources incorporated: variant-1-original.md (reviewer-1, haiku class: F4, F7, the single-cause statement of F3 and F9) and invariant-probe.md (fault-finder: F1 narrowing, F2, F3, F5, F6, F7, F8, F10 to F13, F15). Plan: adversarial/adversarial/refactor-plan.md (15 merged findings). Debate points C-001 to C-009 and A-001 to A-002 come from debate-transcript.md. -->
<!-- PLAN = .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md. All other paths are repo-relative. -->

## Verdict

NEEDS-REVISION: 8 blocking findings; the main cause is that the plan's owner gates and entry conditions cannot be enforced by `/sc:implement`, and several acceptance checks fail on files the plan itself creates, registers or later changes.

## Findings

<!-- Source: Base (reviewer-2 F1), narrowed by debate C-005 and A-001 and by probe INV-010, INV-011, INV-020; the "Tasks 11 to 46 run straight through" claim and the "inevitable bypass" wording are dropped -->
F1 | severity MAJOR | blocking true | unpassable-check | The operator who follows "Run `/sc:implement` on one phase at a time and stop at each gate" gets a run that cannot stop. `/sc:implement` takes one plan file, has no phase option, treats `## Phase N` as a group heading, fails with `E-PLAN-CHANGED` when the plan changes after the first task, and has no pause or ask path for an owner go. Constraints do reach QA, but only as a breach visible in the diff and quotable from the plan, which an owner's chat message never is. No task has an acceptance line that requires a recorded owner go, and PLAN:20 sets four go points (Phase 2, 3, 4 and 5), not three. The fix needs a decision the plan does not make: one managed plan per stage (the later plans read `./artifacts/` paths that would then sit in another package), or a gate task per boundary whose acceptance line accepts only an owner Ruling (a fix pass cannot invent one). | citations:
- PLAN:20 "Run `/sc:implement` on one phase at a time and stop at each gate"
- PLAN:139 "Depends on: Task 10"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:56 "Known options: `--spec`, `--prd`, `--tasklist`, `--resume`, `--ledger`, `--skip-final-review`"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:87 "`## Phase N` is a group heading, not a task"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:46 "hash differs from the pin after the first `T<id>: start`"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:105 "`## Constraints` / `## Out of scope` / `## Non-goals` / `## Non-negotiable`"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:52 "the reviewer can quote that text"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:61 "byte-present in the plan Constraints or a task instruction"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:247-249 "executor-invented approval"

<!-- Source: Base (reviewer-2 F2), corrected by probe INV-001 and INV-002 -->
F2 | severity MAJOR | blocking true | safety | The Phase 4 executor moves `pragmatic.md` to digest v2 even when seeded recall fails. PLAN:20 lists "the seeded-recall result of Task 31" as an entry condition, but Task 31 is the first task inside Phase 4 and only reports; Task 33 "Depends on: Task 31, Task 32". `/sc:implement` ignores `Depends on` lines and runs tasks in source order, so a stronger dependency line would also gate nothing. The only lever it honours is an acceptance line on Task 33 (for example that `./artifacts/seeded-recall-result.md` shows pass on all three requirements); a failure of that line halts the run and only an owner Ruling continues it. Task 31 cannot move to Phase 3, because source.md puts the run in Phase 4. | citations:
- PLAN:20 "the seeded-recall result of Task 31"
- PLAN:376 "This task reports the result; the owner decides whether stage 3 may proceed."
- PLAN:394 "Depends on: Task 31, Task 32"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:91 "Ignore MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`) except `independent`"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:109 "Default sequential in source order."
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:49 "Output an AC requires is absent"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:247-249 "operator Ruling"
- .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md:15 "is part of stage 3 entry and is a Phase 4 task"

<!-- Source: Base (reviewer-2 F3 second half) and variant 1 (reviewer-1 F1), agreed by debate C-001, plus probe INV-008 and INV-015 -->
F3 | severity MAJOR | blocking true | unpassable-check | The Task 40 executor gets a failing test in Phase 4. Task 40 allow-lists "`refs/rule.md` and its plugin mirror path" and requires a failure "when a file named there does not exist", but the mirror is created only in Task 46 (Phase 5). Task 13's allow-list text does not list the mirror either, while Task 40 reads its allow-list from Task 13's section. Leaving the mirror off the list instead fails the scan after Task 46 copies `rule.md` and `scale-map.md` into `plugins/superclaude/`, which the scan covers. The plan must choose how the entry is staged; the three problems with Tasks 13, 40 and 46 (this finding, F9 and F13) need one combined fix. | citations:
- PLAN:164 "names the files allowed to contain the phrases"
- PLAN:170 "lists the auggie file, `refs/rule.md` and the six stage 4 files"
- PLAN:477 "`refs/rule.md` and its plugin mirror path"
- PLAN:482 "a test fails when a file named there does not exist"
- PLAN:546 "add a `canonical` registry row for the plugin mirror"
- PLAN:549 "plugin mirror of `refs/rule.md` is accepted by the reverse scan"

<!-- Source: Variant 1 (reviewer-1 F2), unique to V1; confirmed by the debate advocates and probe INV-009, INV-012 -->
F4 | severity MAJOR | blocking true | contradiction | The executor following Task 41 inserts a digest into `agent_template_analysis.md` and sets its registry row to `v2`, but Task 16 lists exactly 11 `digest` rows and none is for that template, and the live file has no definition sentence, only the merge-rule line. An unregistered fence fails the T2 reverse scan; a twelfth `digest` row breaks the "exactly 11 rows" check. The plan must choose: merge-rule text only for this template (then "five template files" becomes four), or a registered twelfth carrier. | citations:
- PLAN:199 "Two rows of kind `pointer-only`"
- PLAN:203 "exactly 11 rows of kind `digest`"
- PLAN:303 "a fence opener and has no registry row of any kind"
- PLAN:490 "Each gets the digest and pointer"
- PLAN:493 "Each of the five template files holds exactly one digest"
- PLAN:494 "Their registry rows say `v2`"
- src/superclaude/templates/documents/agent_template_analysis.md:466 "take the more severe rating for shared items"

<!-- Source: Base (reviewer-2 F4), widened by probe INV-007 -->
F5 | severity MAJOR | blocking true | unpassable-check | Task 25's "passes" check fails in Phase 2. T3 fails when a carrier contains `src/superclaude`, and pointer-only rows go through T3; Task 16 registers `commands/spec-panel.md` as pointer-only and that file holds a `src/superclaude/` path at line 220. The plugin twin holds the same path (line 218), and the five installed-only variants hold it too, so editing line 220 alone still fails or breaks the twin parity of Task 45. The plan must choose: exempt `pointer-only` and `installed-only` rows from the path check (and keep the test off `~/.claude`), or edit every twin. | citations:
- PLAN:303 "`pointer-only` rows are checked by T3 only"
- PLAN:199 "Two rows of kind `pointer-only`"
- src/superclaude/commands/spec-panel.md:220 "`src/superclaude/examples/release-spec-template.md`"
- plugins/superclaude/commands/spec-panel.md:218 "`src/superclaude/examples/release-spec-template.md`"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:918 "a carrier contains `src/superclaude`"

<!-- Source: Probe INV-004 (no card reported it); Task 13 allow-list citations PLAN:490 and PLAN:513 added at the orchestrator's instruction -->
F6 | severity MAJOR | blocking true | unpassable-check | Later tasks make earlier acceptance lines false, so the final review cannot pass. The managed archive gate has a fresh reviewer verify every task's acceptance lines against the final files, and `issues` stops with `E-ARCHIVE-BLOCKED`. At least four lines are false by then: Task 16 (digest rows at state `legacy`, 19 rows in all) after Tasks 33 to 35, 41, 42 and 46; Task 25 ("passes with all `digest` rows at `legacy`") after the same tasks; Task 27 (the sentence "Preserve the highest severity rating when duplicates disagree" still appears) after Task 37 removes it; Task 13 (the allow-list lists the six stage 4 files) after Tasks 41 and 43 remove them. The package can never archive. The plan must say how superseded lines are scoped (for example "until Task N") or the final review will block. | citations:
- src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:55 "It verifies every task's AC against the real files"
- src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:62 "`issues` → STOP `E-ARCHIVE-BLOCKED`"
- PLAN:203 "2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all"
- PLAN:306 "passes with all `digest` rows at `legacy`"
- PLAN:333 "Preserve the highest severity rating when duplicates disagree"
- PLAN:170 "lists the auggie file, `refs/rule.md` and the six stage 4 files"
- PLAN:446 "`grep -n "highest severity" src/superclaude/skills/task/SKILL.md` prints nothing"
- PLAN:490 "remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of Task 40"
- PLAN:513 "remove those four files from the allow-list of Task 40"

<!-- Source: Variant 1 (reviewer-1 F3), widened by probe INV-006; blocking grade ruled by the judge (debate C-004) -->
F7 | severity MAJOR | blocking true | missing-requirement | The executor can finish all 46 tasks without evaluating the classifier on the fresh-findings population or on the held-out half. Task 6 states the evaluation "is run at stage 2, not here"; no task after Phase 1 consumes `./artifacts/fresh-findings.md`, records judge answers or writes an evaluation result, and Task 5's held-out split is likewise never used. The spec names the held-out evaluation as plan work. Classifier authority is off (OD4), so no decision rests on the result, but the deliverable is required and the owner's stage 2 exit numbers depend on it. | citations:
- PLAN:87 "must be tested apart from the 318 scored rows"
- PLAN:93 "is run at stage 2, not here"
- PLAN:79 "lists the finding ids of the tuning half, the held-out half"
- PLAN:328 "its verdict is recorded and gates nothing"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:934 "The plan also runs behavioural fixture replays and the held-out evaluation."

<!-- Source: Probe INV-005 (no card reported it) -->
F8 | severity MAJOR | blocking true | missing-requirement | The Phase 3 to 5 entry numbers are undefined or have no task. PLAN:20 requires "at least 5 observed shadow runs with zero safety misses and no capture failure", but "safety miss" is defined nowhere in the plan, and the stage 2 exit items (ledger volume, `consumer-unknown` share, offers answered, shadow agreement) and the stage 3 audit-window numbers (revert triggers) have no task that measures or reports them. The spec says no stage starts before the owner has seen the numbers. A gate task that only records the owner's go (the F1 fix) is therefore not enough: the owner has no numbers to read. | citations:
- PLAN:20 "at least 5 observed shadow runs with zero safety misses and no capture failure"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:940 "the owner has seen the numbers"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:946 "reviewers emit `rests_on` while the old definition still decides"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:947 "at least 5 shadow runs observed with zero safety misses and no capture failure"

<!-- Source: Variant 1 (reviewer-1 F4) and base (reviewer-2 F5), agreed by debate C-002, plus probe INV-008 (second file) -->
F9 | severity MINOR | blocking false | other | Task 46 copies the skill folder into the plugin before adding the plugin `canonical` registry row. The plugin mirror's `registry.yaml` differs from the source immediately before the T15 parity check; add the row first or repeat the copy. The same ordering applies to `refs/scale-map.md` if the F3 fix edits it. Part of the combined fix of F3. | citations:
- PLAN:546 "add a `canonical` registry row for the plugin mirror"
- PLAN:549 "plugin mirror of `refs/rule.md` is accepted by the reverse scan"

<!-- Source: Probe INV-003 -->
F10 | severity MINOR | blocking false | sufficiency | The seeded-recall pass line can be met on an underpowered set. Task 7 lets the sizing "state plainly which classes cannot reach it", and "safety recall equals the old rule's" sets no tolerance; at about 0.95 expected recall a 5-point Wilson half-width needs about 70 planted defects per gating class, which does not fit a "fresh short spec". With small n, both texts can find every safety defect and pass by equality while saying little. State a minimum n or call the pass line advisory. | citations:
- PLAN:97 "or state plainly which classes cannot reach it and why"
- PLAN:102 "safety recall equals the old rule's"
- PLAN:376 "safety recall equals the old rule's"

<!-- Source: Probe INV-018 -->
F11 | severity MINOR | blocking false | other | Task 31 does not alternate the order or require fresh spawns. It says "Spawn the same three reviewer agents twice" with no order alternation, while Task 4 alternates; if "same" means the same running agents, the second pass has seen the planted defects and inflates new-rule recall. | citations:
- PLAN:376 "Spawn the same three reviewer agents twice"
- PLAN:64 "with the order of the two texts alternated"

<!-- Source: Probe INV-019 -->
F12 | severity MINOR | blocking false | unpassable-check | T3 may fail a `pointer-only` row before its pointer exists. The `pointer-only` files get their pointer only in Tasks 42 and 45, so a T3 that fails a pointer-only row without a pointer fails Task 25 in Phase 2 for `document_review_loop_prompts.md`; state that T3 checks such a row only once its pointer is present. | citations:
- PLAN:303 "`pointer-only` rows are checked by T3 only"
- PLAN:502 "its registry row is of kind `pointer-only` and stays so"
- PLAN:535 "Edit `src/superclaude/commands/spec-panel.md`"

<!-- Source: Base (reviewer-2 F3 first half), ruled minor by debate C-007, plus probe INV-014 -->
F13 | severity MINOR | blocking false | unpassable-check | Wording-dependent scan trips in `scale-map.md` and `rule.md`. Task 13's section "names the files allowed to contain the phrases"; an executor who writes the three phrases literally trips Task 40's scan on `scale-map.md` and its plugin copy; a path-only list avoids it. Likewise `rule.md` quoting the old definition sentence would fail Task 46's grep and the strict T2 scan. State that both files must not quote the phrases or the old sentence. | citations:
- PLAN:164 "names the files allowed to contain the phrases"
- PLAN:170 "lists the auggie file, `refs/rule.md` and the six stage 4 files"
- PLAN:152 "Create `src/superclaude/skills/sc-review-severity/refs/rule.md`"
- PLAN:477 "`refs/rule.md` and its plugin mirror path"
- PLAN:551 "\"Grade every review finding as blocking or minor\" src/superclaude plugins/superclaude` prints nothing"

<!-- Source: Base (reviewer-2 F6), debate C-009 -->
F14 | severity MINOR | blocking false | missing-requirement | Coverage-matrix omissions in the review run. The matrix omits requirement-bearing source lines 22, 41, 43 and 47 and maps four rows to the Constraints block (`best_task: 0`); the plan covers them all (Tasks 16, 20, 25, 33, 37, 38). Matrix quality only; the matrix is a review-run artifact. | citations:
- .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md:22 "are exempt from the \"no unregistered fence opener\" scan"
- .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md:41 "Acceptance checks that pin a line number pin the content instead"
- .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md:43 "Task 31's list also names `tests/skills/test_review_brief_rests_on.py`"
- .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md:47 "Wording slips: Task 11's \"exactly the 11 carriers\""
- PLAN:401 "`grep -n "pragmatic" src/superclaude/hooks/hooks.json` still matches"
- PLAN:455 "Update `tests/skills/test_review_severity_rule.py`"

<!-- Source: Probe INV-016 -->
F15 | severity MINOR | blocking false | other | Installed reference files cite `.dev/` package paths. Task 15 tells `refs/classifier-questions.md`, an installed file, to cite `./artifacts/classifier-input-availability.md` and PF `08-test/results.md`; neither resolves in an installed `~/.claude/skills/` copy. T3 checks only for `src/superclaude`, so nothing catches it. | citations:
- PLAN:188 "cite PF `08-test/results.md` and `./artifacts/classifier-input-availability.md`"
- PLAN:303 "no carrier contains `src/superclaude`"

## Checked

- Every change the request lists has a task. Three owner gates, and the "one pass" sentence is removed (PLAN:20; no match for "one pass"). Stage 0a record: Task 3. Seeded set: defined in Task 7, run in Task 31. Fresh findings held out of the split: Tasks 5 and 6. Input availability: Task 8. Input supplier: Task 20. Registry with 11/1/2/5 rows and no task-skill row: Task 16 (PLAN:199-204). Markdown-only scan: Task 40. Stage 2 sweep only records: Task 26. Content pins: Tasks 27, 28 and 33.
- One sweep and one offer, in src/superclaude/skills/task/SKILL.md:288 "Post-Completion Validation (Final Phase Only)". Neither skill contains "sweep" today. tech-research runs inside /task (src/superclaude/skills/tech-research/SKILL.md:614).
- Cap-sentence lines match the live files: task SKILL :258, :372, :409; tech-research :490, :555; src/superclaude/agents/rf-qa.md:402 and :549.
- Merge-rule lines match: rf-qa :83, src/superclaude/agents/rf-qa-qualitative.md:84, src/superclaude/agents/rf-analyst.md:75, task SKILL :252 and :361, src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:228. Plugins have none today.
- FAIL bullets at rf-qa-qualitative :240 to :784 (8 lines), Rule 6 at :990, src/superclaude/templates/documents/agent_template_qa.md:158, :161 and :333.
- S1, S2 and S5 sit at src/superclaude/output-styles/pragmatic.md:225, :226 and :229. Exactly 11 files hold the definition sentence.
- Code and test anchors exist. Subcommand tuple, with no clash for `classify`: src/superclaude/cli/review/__init__.py:19-29. `run_doctor`: src/superclaude/cli/doctor.py:17. `CANONICAL_CAP_TEXT`, `S1_S3_FILES` and the byte-copy test: tests/skills/test_review_severity_rule.py:181-283. Both plan tables are under `.dev/review-severity-rule/`. The pragmatic hook entry: src/superclaude/hooks/hooks.json:173. The plugin has 4 skills today.
- Classifier limits match the 5-run result. The Task 3 figures equal .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/08-test/results.md:87. The missing-item, constraint and contradiction questions are gated on code-supplied inputs (Tasks 20 to 22), consistent with results.md:74. The lower bound shown beside the band is allowed by merged-requirements.md:570. No task gives the classifier any authority (PLAN:261).
- The not-built list holds. No task edits `sc-implement-protocol/refs/qa.md`, the severity code in `cli/**/*.py`, or the cap of 2 fix cycles.
- Record-only sweeping explicitly tests unchanged gate outcomes: PLAN:319, PLAN:322.
- One final sweep and offer belong to the task skill; tech-research gets neither duplicate: PLAN:328, PLAN:342.
- The legacy-text pin stops applying once its registry row reaches v2: PLAN:364, PLAN:368.
- Reviewer-1 changed no files and ran no commands or tests; its described failures follow from written requirements, not observed execution.

## Self-report

confidence: 0.85
reviewer_model_self_report: merged by adversarial pipeline; base reviewer-2 (opus class), incorporated reviewer-1 (haiku class) and the fault-finder probe
