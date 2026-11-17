# Reviewer brief 1 (persona: analyzer; model class: haiku)

## T1 card excerpt

### Deviation and risk observations

- O1, gate evidence cannot exist by construction. Task 1 acceptance line 2 requires the stage 2 package's `stage2-summary-for-owner.md` to state "at least 5 observed shadow runs with zero safety misses and no capture failure". The stage 2 plan (`.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md`, Task 7 acceptance, line 114) has that file state "the number of shadow runs observed so far (zero is allowed)" and write it at the end of the package, before any shadow run is observed (the Constraints of both plans say the runs come over time and no task produces them). A summary written at the end of stage 2 therefore says zero or fewer than 5. Nothing in the stage 3 plan regenerates it (for example by running stage 2's `./artifacts/shadow_summary.py` over the shadow-run folders) or names another file that holds the count of 5.
- O2, a path that does not exist in this package. Task 4 (rf-qa) and Task 5 (rf-qa-qualitative) read the frozen FAIL-trigger inventory from `./artifacts/stage0-inventory-freeze.md`. In a split plan `./artifacts/` is this package's folder, but that file is written by the stage 0 package (`TASK-WF-blockerStage0-20261116-021044.md`, Task 1 acceptance, line 37). Task 1 of this plan says "read by package id" for the stage 0 files; Tasks 4 and 5 do not. Task 4's acceptance ("Every FAIL-trigger line in the frozen inventory for `rf-qa.md` is either changed or listed...") has no input file as written.
- O3, the seeded-recall measurement carries the old rule in both passes. The hook `src/superclaude/hooks/hooks.json:173` runs `pragmatic-subagent.js`, which reads `~/.claude/output-styles/pragmatic.md` (today byte-identical to the `src/` file) and injects it into every subagent at start. A reviewer spawned for the "new rule text" pass therefore holds the old three definition bullets from the hook AND the digest from its brief. The stage 0 plan names this confound in Task 4 (acceptance: "states the old-rule injection confound, how the graders were instructed...") and its own review report flagged it; Task 1 of this plan does not mention it, and its acceptance lines do not require the result file to state it. The result gates the rule switch (Task 3).
- O4, the pass or fail rule is undefined. Task 1 asks for "a pass or fail line for each of the three requirements" and Task 3 requires pass on all three, but nothing says how "safety recall equals the old rule's" is judged on a small planted set (point equality, interval overlap, tolerance). The stage 0 plan Task 7 expects that the set cannot reach the size for a 5-point interval and then marks that class's pass line advisory. A class marked advisory cannot "show pass", so Task 3's check would halt for the owner's Ruling by construction. The source (spec section 8.3) also says "with the same reviewers"; Task 1 says fresh agents per pass but not that both passes use the same reviewer configuration (model class, brief).
- O5, order of work. The six-agent seeded run is the task body; the entry checks (owner go in the ledger, stage 2 summary, stage 0b and 0c files) are acceptance lines checked after it. The body never says to check them first, so the expensive spawn runs even when the go is missing. The ledger rows `Package id` for stages 1 to 3 are blank today, and Task 1 does not name the stage 0 package id (`TASK-WF-blockerStage0-20261116-021044`) it reads from.
- O6, stale numbering from the renumbering. Task 10 acceptance line 1 says the scan test passes "on the current tree after Tasks 34 to 37" (those tasks are 4 to 7 here; the plan has 11 tasks). Task 8 acceptance names `./artifacts/t38-fixture-diff.md` (old task number). Both are copied from the base plan.
- O7, a check that cannot detect what it names. Task 7 acceptance line 4 runs `grep -n "sc-review-severity" src/superclaude/skills/sc-review-severity/refs/registry.yaml` and says it "shows no row for `skills/task/SKILL.md`"; that pattern matches the skill folder name, not the `skills/task/SKILL.md` row, so it neither finds nor excludes that row. (Copied from base Task 37.)
- O8, grounding that holds. I re-read these against the live tree: `pragmatic.md` lines 221, 225, 226, 227, 228, 229 hold the bullets Tasks 3 names; the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" appears 2 times in `rf-qa.md` (lines 402 and 549), 2 times in `rf-qa-qualitative.md` (not edited by Task 5, consistent with spec L3 which lists `rf-qa.md` and `task/SKILL.md`) and 3 times in `task/SKILL.md` (Task 7 expects all three); `rf-qa-qualitative.md` has the eight "Any CRITICAL or IMPORTANT issue exists" lines at 240, 291, 362, 429, 500, 567, 746, 784 and Rule 6 ("never minor") at 990; the phrase scan over the listed directories hits exactly the six stage 4 files, the auggie file, and the four files Tasks 4 to 7 edit (no hit under `plugins/superclaude`), so the Task 10 allow-list plus the stage 3 edits leave a clean scan; the test names Task 8 and 9 cite exist (`canonical_rule_bullets`, `S1_S3_FILES`, `S5_FILES = S1_S3_FILES[:6]`, `CANONICAL_CAP_TEXT`, `test_ej_fixtures_are_byte_copies_of_the_plan_tables`, `FAIL_BULLET` and `PASS_BULLET` imported from `test_nfr_conv_9_zero_trust`).

### Recommendations

- Task 1: name the stage 0 package id; add a first step that checks the entry conditions before spawning; define the pass rule and what an advisory class does at Task 3's gate; state that both passes use the same reviewer set and how the injected old rule is handled in the new-rule pass, and require the result file to state it.
- Task 1 acceptance line 2 (or a new step): name where the count of 5 observed shadow runs is read (for example run stage 2's `shadow_summary.py` over the shadow-run folders and write the output into this package).
- Tasks 4 and 5: read the inventory from the stage 0 package by id.
- Constraints: add the stage 4 edit ban. Task 10: replace "Tasks 34 to 37" by "Tasks 4 to 7". Task 7: grep for `skills/task/SKILL.md` in the registry. Task 8: rename the diff artifact.

Context: the plan under review is stage 3 of five (one plan per stage) of the blocker-classification work (GitHub issue #552). It changes the live review rule (the pilot): `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md` and the task skill. The program folder is `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115` (spec: `02-brainstorm/merged-requirements.md`; stage ledger: `stage-requests/README.md`; this stage's request: `stage-requests/stage3-request.md`, which the plan's `source.md` copies). The earlier 46-task plan `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/` is the base text of this plan; its pre-execution review `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md` found 8 blocking defects. Check that the findings of that report that touch stage 3 are resolved in this plan (in particular F2, F10 and F11: the seeded-recall gate, its sample size, fresh spawns with alternated order; F3, F9 and F13: the allow-list staging; F6: acceptance lines that a later task makes false; F8: the numbers the owner needs), and look for NEW defects that splitting the plan into stages introduced (cross-package reads, renumbering, files read from another package, checks that now point at the wrong place).

How to grade: grade each finding blocking or minor by consequence. Blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format. A finding whose consequence is a wrong measurement that gates the rule switch is blocking. Do not invent findings and do not work to a quota; a review with no finding must say what you checked and why you found no defect.

How to work: you have Read, Grep, Glob and code-search tools only. Audit the hunks below and re-Read the files you cite; every `file:line` you cite is re-read by an independent validator and dropped if it does not match, so quote exactly and cite the line where the text sits. Tell the orchestrator about any file you could not read.

How to answer: return your card as your final message, plain markdown, at most about 6,000 characters, with these sections only: `## Findings` (numbered F1, F2, ...; each with `Blocking: yes` or `Blocking: no`, a one-line title, evidence as `file:line` plus a short verbatim quote, the consequence in one or two sentences, and a one-line fix), `## Checked and sound` (what you verified and found fine), `## Self-reported confidence` (0.00 to 1.00). No DONE/NEXT table and no preamble.

Persona instructions (analyzer): look for deviations and internal contradictions between tasks, and for acceptance checks that cannot pass as written (a check that needs a file or state nothing produces, or that a task's own edit or a later task breaks). Walk the `Depends on:` edges and the cross-package reads: for each file this plan reads from the stage 0, stage 1 or stage 2 package, confirm in the producing plan's acceptance lines that the file is written, at which path, and that what it contains is what this plan expects. Check that each grep-style acceptance check would print what the task says against the live files. Test the T1 card's observations (O1 to O8) against the live files and the producing plans before you agree or disagree, and say so when you disagree. Also probe two questions the card does not settle: whether `make sync-dev` reaches the installed output style that the SubagentStart hook reads, and whether Task 3's instruction to run the tests that Task 8 re-pins is consistent with the plan's own rule that a line a later task makes false carries an end point.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:14:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:17-27
```markdown
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
20: - One package, one stage. This is stage 3 of five packages (one plan per stage). It changes the live review rule. It runs only when all of these hold, each checked by reading files and not by memory (Task 1 checks them): the owner's go for stage 3 is recorded in the stage ledger; the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and states at least 5 observed shadow runs with zero safety misses (by the definition the stage 0 spec edit drafted) and no capture failure; the stage 0 package's `stage0b-escape-test.md` and `stage0c-regrade.md` exist. `/sc:implement` runs this whole package in order, so the rule switch cannot start unless Task 1's checks and the seeded-recall result pass. Stage 4 starts only after one audit window with no revert trigger tripped (spec section 13.2) and the owner's go in chat.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
24: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
25: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
26: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
27: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:31-41
```markdown
31: ## Task 1: Run the seeded-defect recall set under the old and the new rule text
32: 
33: Run the seeded-defect set built by the stage 0 package (its `./artifacts/seeded-recall-set.md` and the planted deliverable under its `./artifacts/seeded/`, read by package id) as spec section 8.3 says. Spawn three reviewer agents for each pass (old rule text, new rule text) as freshly spawned agents, never agents continued from an earlier pass, and alternate the pass order across the three reviewers on the planted deliverable, once with today's rule text (the definition bullets and the Medium bullet of `src/superclaude/output-styles/pragmatic.md`) and once with the digest of spec section 4.1, never showing them the answer key. Score each planted defect as found or missed and as blocking or not, per class. Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts, the share of cosmetic defects that block under each, the Wilson 95 percent intervals, and a pass or fail line for each of the three requirements named in the stage 0 package's `seeded-recall-set.md` (safety recall equals the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the cosmetic block share falls). This task reports the result; the owner decides whether stage 3 may proceed.
34: 
35: Acceptance criteria:
36: - The stage ledger `stage-requests/README.md` in PF has an owner go for stage 3 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
37: - The stage 2 package's `./artifacts/stage2-summary-for-owner.md` (read by package id) states at least 5 observed shadow runs with zero safety misses and no capture failure.
38: - The stage 0 package's `./artifacts/stage0b-escape-test.md` and `./artifacts/stage0c-regrade.md` exist.
39: - `./artifacts/seeded-recall-result.md` holds per-class recall under both rule texts with intervals, the cosmetic block share under both, and a pass or fail line for each of the three requirements.
40: - The reviewer agent ids are recorded and the answer key is not among the files they were given.
41: - The file states that the result is evidence for the owner's go and does not itself grant it.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:55-67
```markdown
55: ## Task 3: Move pragmatic.md to digest v2
56: 
57: Depends on: Task 1, Task 2
58: 
59: Edit `src/superclaude/output-styles/pragmatic.md`: replace the three definition bullets (the one that begins "Grade every review finding as blocking or minor", the one that begins "Minor findings never fail a review", and the one that begins "On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking", today lines 225, 226 and 229) with the digest of REQ-01 inside its fence plus the pointer line naming `~/.claude/skills/sc-review-severity/refs/rule.md` first and `.claude/skills/sc-review-severity/refs/rule.md` second. The cap bullet and the own-model bullet ("A protocol that defines its own severity model, such as `/sc:implement`") stay word for word (the cap sentence is also the last sentence of the digest). Move the Medium and spec-panel bullets into the full rule and scale map, and change the reviewer brief bullet ("Every review agent MUST review as an independent reader") so reviewers hunt for defects and name their consequence instead of hunting for "false claims" (REQ-04). Set the registry row of `output-styles/pragmatic.md` to `v2`. Run `make sync-dev` and then the existing tests that Task 8 re-pins.
60: 
61: Acceptance criteria:
62: - `./artifacts/seeded-recall-result.md` exists and shows pass on all three requirements (safety recall equal to the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the cosmetic block share falls); when a line shows fail, this check fails and the run halts for the owner's Ruling. This task does not rely on `Depends on` for the gate.
63: - `src/superclaude/output-styles/pragmatic.md` holds exactly one fenced digest equal to the digest section of the skill's `refs/rule.md` and its registry row says `v2`.
64: - The cap sentence ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings") and the own-model bullet still appear word for word (`grep -c` of each sentence prints 1 or more).
65: - The hook `pragmatic-subagent.js` still finds and injects the file: `grep -n "pragmatic" src/superclaude/hooks/hooks.json` still matches and `src/superclaude/output-styles/pragmatic.md` exists.
66: - The new pointer line names `~/.claude/skills/sc-review-severity/refs/rule.md` before the `.claude/` copy and contains no `src/superclaude` path.
67: - `uv run pytest tests/skills/test_review_brief_rests_on.py -v` passes (its legacy assertion is skipped now that the row is `v2`).
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:69-79
```markdown
69: ## Task 4: Move rf-qa.md to digest v2 and rewrite its fixed FAIL triggers
70: 
71: Depends on: Task 3
72: 
73: Edit `src/superclaude/agents/rf-qa.md`: replace S1, S2 and S5 (the definition bullet and the bullets beside it, today around line 108) with the digest and pointer; replace the merge rule ("take the more severe rating for shared items", today line 83) with the L1 text (the consolidator grades by the rule, keeps every reviewer's grade visible, and sends a blocking grade that names no consumer back once); add the L2 pre-handback checks to the Fix Cycle section; at each of its two cap sentences ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", today in the Fix Cycle bullet near line 402 and in numbered rule 10 "Maximum 2 fix cycles" near line 549) add the L3 three choices (fix by hand, accept and file as an `accepted-blocker` follow-up, or stop) and the one-offer sentence naming the task skill's end-of-run offer; and for each fixed FAIL trigger listed in `./artifacts/stage0-inventory-freeze.md` for this file (spec section 10.4: "Any incomplete file = FAIL", "Any untagged doc claim = FAIL", the "Will this gap reduce report quality? -> IMPORTANT" and "Any CRITICAL or IMPORTANT gap = overall FAIL" bullets, the PASS and FAIL bullets by label near lines 182 to 183, "Flag exact duplicates as IMPORTANT", and the count-CRITICAL-and-IMPORTANT-as-blocking lines) either rewrite it to "grade by the three conditions; the label is information" or keep it as a named mechanical gate mapped to condition 2 (Missing) and record the keep in `refs/scale-map.md`; "Flag exact duplicates as IMPORTANT" becomes Note unless a condition holds. Set the registry row to `v2`.
74: 
75: Acceptance criteria:
76: - `grep -n "more severe rating" src/superclaude/agents/rf-qa.md` prints nothing.
77: - Every FAIL-trigger line in the frozen inventory for `rf-qa.md` is either changed or listed as a kept mechanical gate in `refs/scale-map.md` with a reason.
78: - The PASS and FAIL bullets are reworded to "any blocking gap" and the file holds exactly one digest.
79: - The L2 fix-cycle checks are present in the Fix Cycle section, and the L3 three choices with the one-offer sentence sit beside each of the two places the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" appears (`grep -c` of that sentence still prints 2).
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:81-91
```markdown
81: ## Task 5: Move rf-qa-qualitative.md to digest v2, rewrite its eight FAIL-by-label pairs and apply OD16
82: 
83: Depends on: Task 3
84: 
85: Edit `src/superclaude/agents/rf-qa-qualitative.md`: replace S1, S2 and S5 (today around line 108) with the digest and pointer; replace the merge rule (today line 84); rewrite or keep as named mechanical gates, recorded in `refs/scale-map.md`, the eight verdict pairs that fail a review on "Any CRITICAL or IMPORTANT issue exists" (the FAIL bullet today at lines 240, 291, 362, 429, 500, 567, 746 and 784, each with its PASS bullet one line above; the list is in `./artifacts/stage0-inventory-freeze.md`); and rewrite Rule 6 ("Contradictions are always IMPORTANT or CRITICAL ... that's never minor", today line 990) per OD16 option (b), so a contradiction nothing rests on is a follow-up, and keep contradictions that touch a decision basis, a quoted number or a required deliverable as Blocking under condition 1. Update the registry row to `v2`.
86: 
87: Acceptance criteria:
88: - `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/agents/rf-qa-qualitative.md` prints 0, or each remaining line is listed in `refs/scale-map.md` with its reason.
89: - `grep -n "that's never minor" src/superclaude/agents/rf-qa-qualitative.md` prints nothing, and the new Rule 6 text names the decision-basis exception.
90: - The file holds exactly one digest and no `more severe rating` text.
91: - `tests/audit/test_severity_floor_unweakened.py` is updated in Task 9 in the same change set; the file's `## Critical Rules` block hash is re-pinned there.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:106-116
```markdown
106: ## Task 7: Switch the task skill's consolidation, fix and escalation text and turn the sweep on
107: 
108: Depends on: Task 2, Task 3
109: 
110: Edit `src/superclaude/skills/task/SKILL.md`: the Findings Consolidation step and the Follow-Up Items consolidation sentence replace "Preserve the highest severity rating when duplicates disagree" with the L1 text and keep the ledger writing of the stage 2 package; the Fix Agent step requires the L2 mechanical checks before handing back and the `origin: fix-induced` tag; the Conditional Proceed step counts Blocking findings only and, at each cap sentence ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", today at the Conditional Proceed step, the Escalation item and the Fidelity Verification step), offers three choices (fix by hand, accept and file as an `accepted-blocker` follow-up, or stop) without changing the cap of 2 fix cycles (L3); and the sweep call of the stage 2 package is switched to `promote` on, so a swept Medium row becomes Blocking at the last gate. The skill gets no registry row (it is not a digest carrier).
111: 
112: Acceptance criteria:
113: - `grep -n "highest severity" src/superclaude/skills/task/SKILL.md` prints nothing.
114: - The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" is still present at each place it appears today, each with the three choices and the statement that the cap is unchanged.
115: - The sweep call in "Post-Completion Validation (Final Phase Only)" states `promote` on.
116: - `grep -n "sc-review-severity" src/superclaude/skills/sc-review-severity/refs/registry.yaml` shows no row for `skills/task/SKILL.md`.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:118-127
```markdown
118: ## Task 8: Re-pin the severity tests in tests/skills
119: 
120: Depends on: Task 3, Task 4, Task 5, Task 7
121: 
122: Update `tests/skills/test_review_severity_rule.py` (`canonical_rule_bullets()` reads the digest from `refs/rule.md`; `S1_S3_FILES` and its `[:6]` slice `S5_FILES` become registry rows of kind `digest`; the cap-text and banned-phrase checks stay, and the cap text constant `CANONICAL_CAP_TEXT` stays asserted against the output style only, as today), `tests/skills/test_review_severity_mapping.py` (the Medium and cadence pins move from "once per loop" to the once-per-run wording and to assertions on `refs/rule.md` and `refs/scale-map.md`), `tests/skills/test_implement_severity_static.py` (S4 kept word for word; the S2 assertion moves to the digest; the `qa.md` pins stay), the fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` (update only the approved changed strings) and the two plan tables the fixtures must be byte copies of, `.dev/review-severity-rule/cap-edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml` (the test `test_ej_fixtures_are_byte_copies_of_the_plan_tables` in `tests/skills/test_review_severity_rule.py` compares them; edit each pair in the same change, or record which relaxation of that test is chosen and why). `tests/skills/test_review_loop_extension.py`, `test_review_prompt_overrides.py` and `test_spec_panel_review_loop.py` must still pass unchanged. Also add `tests/skills/test_review_brief_rests_on.py` of the stage 2 package to the list of tests re-run, because its legacy assertion is skipped once the pragmatic row is `v2`.
123: 
124: Acceptance criteria:
125: - `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_implement_severity_static.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_brief_rests_on.py -v` passes, including `test_ej_fixtures_are_byte_copies_of_the_plan_tables`.
126: - The two fixtures change only rows whose new text is the digest or the once-per-run cadence; the diff of each fixture and of each plan table is listed in `./artifacts/t38-fixture-diff.md`.
127: - No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:140-149
```markdown
140: ## Task 10: Add the merge-rule reverse-scan test
141: 
142: Depends on: Task 4, Task 5, Task 6, Task 7
143: 
144: Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude`, matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`: `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, `src/superclaude/skills/sc-review-severity/refs/rule.md`, and, until the stage 4 package, the six stage 4 files (`src/superclaude/skills/tech-reference/SKILL.md`, `src/superclaude/skills/readme/SKILL.md`, `src/superclaude/skills/tdd/refs/build-request-template.md`, `src/superclaude/skills/operational-guide/SKILL.md`, `src/superclaude/templates/documents/agent_template_qa.md` and `src/superclaude/templates/documents/agent_template_analysis.md`). The stage 4 package removes each of those files from the allow-list in the same change that edits it, and adds the plugin mirror of `refs/rule.md` to the allow-list and the registry before it copies the skill folder; the plugin mirror is NOT in the allow-list here.
145: 
146: Acceptance criteria:
147: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 34 to 37, with no hit in `src/superclaude/cli/` counted.
148: - A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
149: - The allow-list is read from `refs/scale-map.md` and a test fails when a file named there does not exist.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:154-163
```markdown
154: ## Task 11: Write the stage 3 audit summary for the owner
155: 
156: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10
157: 
158: Write `./artifacts/stage3-summary-for-owner.md`: the seeded-recall result headline from Task 1, the re-pinned test results, and the audit-window measures the spec's section 13 defines for stage 3 (read the metric list in section 13.1 including M12, the rf-qa FAIL count per pilot gate, and the revert triggers RT1 and RT2 in section 13.2 with their current state; quote their text from the spec and do not restate it from memory). State that the audit window runs after this package and is observed by the owner or operator, name which runs and gates it covers, and end with the sentence that the owner's go for stage 4 is given in chat and not by this file.
159: 
160: Acceptance criteria:
161: - `./artifacts/stage3-summary-for-owner.md` names the seeded-recall headline and the file that holds it, lists the tests re-pinned with their observed pass counts, and quotes RT1, RT2 and M12 from the spec.
162: - The summary states the revert command per carrier row (the spec's three-step revert) and that no revert trigger can be judged until the audit window has run.
163: - The summary ends with the sentence that the owner's go for stage 4 is given in chat and not by this file.
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:106-115
```markdown
106: ## Task 7: Write the shadow summary script and the stage 2 owner summary
107: 
108: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6
109: 
110: Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers and prints the stage 2 exit numbers the spec defines in its section 12 stage 2 row (as edited by the stage 0 package: ledger volume per run, the share of rows tagged `consumer-unknown`, offers made and answered, the shadow agreement figures, the count of runs observed, the count of safety misses by the stage 0 definition, and the count of capture failures), with a test over fixture ledgers under `./artifacts/`. Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline from Task 6, the script's output over the shadow runs that exist so far (zero runs is a valid and stated result), the sweep and offer wiring results from Tasks 1 to 5, the limits, and the sentence that the owner's go for stage 3 is given in chat and not by this file.
111: 
112: Acceptance criteria:
113: - `./artifacts/shadow_summary.py` runs with `uv run python ./artifacts/shadow_summary.py --help` and its fixture test passes (the command and the pytest or script output are recorded in the summary).
114: - `./artifacts/stage2-summary-for-owner.md` names the headline of Tasks 1 to 6 with the file that holds it, states the number of shadow runs observed so far (zero is allowed), and states plainly that the stage 3 entry needs at least 5 observed runs with zero safety misses.
115: - The summary ends with the sentence that the owner's go for stage 3 is given in chat and not by this file.
```

### .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md:31-38
```markdown
31: 
32: ## Task 1: Freeze the pattern inventory of spec section 10
33: 
34: Re-run, with plain `grep -rn` (not the Grep tool, which skips gitignored folders and so misses the project `.claude/` copies) over `src/superclaude`, `plugins/superclaude` and the project `.claude/` folder, every pattern the spec lists in section 10: the definition sentence `Grade every review finding as blocking or minor` (spec: 11 files), `Blocking is a real defect` (11), `Minor findings never fail a review` (11), `at most 2 fix cycles \(3 reviews\)` (12), `CRITICAL and IMPORTANT findings are blocking` (7), `follow-up candidates` (3 files, 7 lines), `2 fix cycles` (22 files, 120 lines), the two merge-rule patterns of section 10.3 (13 lines in 10 files), the tasklist pattern `High or Medium` and `Medium (blocking)` in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (7 lines), and the fixed FAIL-trigger patterns of REQ-30 (`= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT`) with one more pattern, `Any CRITICAL or IMPORTANT issue exists` (not in the spec; the review of the first plan found 8 lines in `src/superclaude/agents/rf-qa-qualitative.md` and 1 in `src/superclaude/templates/documents/agent_template_qa.md`), all over `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates` and `src/superclaude/rules`. Write the counts and every hit line to `./artifacts/stage0-inventory-freeze.md`.
35: 
36: Acceptance criteria:
37: - `./artifacts/stage0-inventory-freeze.md` exists and has one table row per pattern with the columns pattern, scope, spec count, observed count and difference.
38: - Every fixed FAIL-trigger pattern, including `Any CRITICAL or IMPORTANT issue exists`, has its hit lines (file, line number, text) listed, so later tasks use this list and not a remembered one.
```

### .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md:60-77
```markdown
60: - The file states in one paragraph that this is not a Jev run, that the judge shares a model family with the scorers and that the questions were finalised after the table was read, so it measures consistency with the panel and not accuracy on new findings.
61: - The file states that no classifier authority follows from it (OD4).
62: 
63: ## Phase 2: Re-grade and split the scored table
64: 
65: ## Task 4: Re-grade the scored table under the old and the new rule text (spec stage 0c)
66: 
67: Depends on: Task 1
68: 
69: Use the 318 findings in PF `04-historical/master-table.md` through the blind copies `blind-table-1.md`, `blind-table-2.md` and `blind-table-3.md` in the same folder (columns ID, Category, Description brief, Context only). Spawn three blind agents that did not write the rule or the spec. Each re-grades every finding twice, in a paired design with the order of the two texts alternated: once under today's rule text (the lines of `src/superclaude/output-styles/pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet to the spec-panel scale bullet, today lines 221 to 231) and once under the digest of spec section 4.1 (REQ-01, the block between the quoted lines). Record each agent id and every grade in `./artifacts/stage0c-grades.jsonl` and write `./artifacts/stage0c-regrade.md` with the confusion matrix against the panel consensus in PF `05-scoring/consensus.md` (blocker at mean 4.0 or higher), how many findings graded blocking under the old text become non-blocking under the new text, the spread among the three agents, and the rows that moved from non-blocking to blocking. Every subagent in this session receives the installed output style, which holds the old rule, through the SubagentStart hook `pragmatic-subagent.js` (registered in `src/superclaude/hooks/hooks.json`), so the new-text arm is graded with the old rule still in its context. Tell each grader to apply only the rule text it is given, to quote the sentence it applied for each grade, and to ignore any other review-grading rule in its context; if a way to spawn graders without the injection exists, use it and record how. State the confound in the result file and report the movement counts as a lower bound on the change, because the confound biases them toward no change.
70: 
71: Acceptance criteria:
72: - `./artifacts/stage0c-grades.jsonl` has 318 findings times 3 agents times 2 texts, 1908 grades, each with agent id, text version and the order position.
73: - `./artifacts/stage0c-regrade.md` carries the confusion matrix with counts, the old-to-new movement counts and the three-agent spread, and states that the table holds only findings filed as blocking.
74: - The file lists the ids of the agents used and states that none of them wrote the digest or the spec.
75: - Rows the old text and the new text grade differently and that the panel calls a blocker are listed by id, since they are the recall risk.
76: - `./artifacts/stage0c-regrade.md` states the old-rule injection confound, how the graders were instructed, shows the quoted sentence each grader applied for a sample of grades, and reports the movement counts as a lower bound.
77: 
```

### .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md:104-112
```markdown
104: ## Task 7: Define and size the seeded-defect recall set (spec section 8.3)
105: 
106: Plant known defects in a held-out deliverable so a later task can measure recall under the old and the new rule text. The four classes are a decision-bearing false claim, a missing required section, a safety risk and a cosmetic defect. The held-out deliverable is a fresh short spec written for this purpose under `./artifacts/seeded/` (not a document any rule text was tuned on; the spec notes the 44-defect spec ledger named in the run-2 scope file as a sanity check only, because the whole #346 series was tuned on it). Size the set so a 5-point change in recall is visible: state the arithmetic (with n planted defects per class, the Wilson 95 percent half-width at the expected recall) and state a minimum n per gating class (safety, decision-bearing, missing) so the half-width is at most 5 points at the expected recall, and plant at least that many defects of each gating class. Where the deliverable cannot hold that many, state the n reached, the interval that results, and that the recall pass line for that class is advisory for the owner. Compute the n that gives a 5-point Wilson half-width at expected recalls of 0.90 and 0.95 (the review of this plan estimated about 140 and about 83 planted defects) and state whether the deliverable can hold that many; if it cannot, the advisory fallback is the expected outcome and the file says so. State also that the stage 3 package runs each pass (old rule text, new rule text) with freshly spawned agents and alternates the pass order across the three reviewers. Write the sizing argument and the planted-defect list (class, location, the planted text and the correct text, and the consumer a reviewer should name) to `./artifacts/seeded-recall-set.md`, and keep the answer key separate from what reviewers read.
107: 
108: Acceptance criteria:
109: - `./artifacts/seeded-recall-set.md` holds the sizing argument with the numbers and the planted-defect list with at least one defect in each of the four classes.
110: - The file states a minimum n for each gating class and the Wilson half-width it gives, or marks that class's pass line advisory and shows the interval the owner will see.
111: - The planted deliverable exists under `./artifacts/seeded/` and the answer key is in a file reviewers are never given (named in `./artifacts/seeded-recall-set.md`).
112: - The file states the three spec requirements the run must meet (safety recall equals the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the share of cosmetic items that block falls) and that the stage 3 package runs the set.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:13-21
```markdown
13: ## Stage ledger
14: 
15: | Stage | Request file | Base tasks (revised plan) | Package id | Owner go (date, where) |
16: |---|---|---|---|---|
17: | 0 Measurement | `stage0-request.md` | 1 to 10 | `TASK-WF-blockerStage0-20261116-021044` (generated 2026-11-16; its pre-execution review says NEEDS-REVISION, 2 blocking findings, so revise before running it) | not needed (no change under `src/`) |
18: | 1 Offline scaffold | `stage1-request.md` | 11 to 25 | | |
19: | 2 Shadow | `stage2-request.md` | 26 to 30 | | |
20: | 3 Pilot | `stage3-request.md` | 31 to 40 | | |
21: | 4 Propagation | `stage4-request.md` | 41 to 46 | | |
```

### src/superclaude/hooks/scripts/pragmatic-subagent.js:1-20
```javascript
1: #!/usr/bin/env node
2: 
3: const fs = require('fs');
4: const os = require('os');
5: const path = require('path');
6: 
7: const stylePath = path.join(os.homedir(), '.claude', 'output-styles', 'pragmatic.md');
8: 
9: try {
10:   const source = fs.readFileSync(stylePath, 'utf8');
11:   const instructions = source.replace(/^---[\s\S]*?---\s*/, '');
12:   const output = {
13:     hookSpecificOutput: {
14:       hookEventName: 'SubagentStart',
15:       additionalContext: `PRAGMATIC MODE ACTIVE\n\n${instructions}`,
16:     },
17:   };
18:   process.stdout.write(JSON.stringify(output));
19: } catch (error) {
20:   process.stderr.write(`Failed to load Pragmatic instructions from ${stylePath}: ${error.message}\n`);
```

### src/superclaude/output-styles/pragmatic.md:221-229
```markdown
221: - Every review agent MUST review as an independent reader who did not produce the work: look for concrete defects (wrong behaviour, false claims, missing deliverables, security or data-loss risk) and report each one with evidence, never to confirm the work is correct and never to meet a quota.
222: - A zero-finding result is valid. When a review finds no defect, it MUST state what it checked (scope, files, claims, behaviours) and why it concluded no defect exists, rather than reporting a bare "no issues found". Never invent a finding to avoid a zero, and never treat a zero as suspect by itself; an unreadable or missing input is incomplete, not zero.
223: - When two component, research, or output files conflict on the same component or claim, the gate MUST first determine whether one source is accurate from authoritative evidence. If one source is verified accurate, use it and continue. If the conflict cannot be resolved, record BOTH conflicting versions with an explicit searchable contradiction marker that cites both file paths and flag the conflict for resolution; NEVER silently pick one version and assert it as fact.
224: - Every review agent MUST produce a binary verdict: PASS or FAIL. There is no "conditional pass" and no partial pass.
225: - Grade every review finding as blocking or minor. Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk. Minor is cosmetic, wording, formatting, citation format, a nit, style, or a moved line number on a true claim.
226: - Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. Minor findings are not rechecked in later rounds and never trigger a fix pass on their own. Only blocking findings produce FAIL.
227: - A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings.
228: - A protocol that defines its own severity model, such as `/sc:implement` (`~/.claude/skills/sc-implement-protocol/refs/qa.md`), applies that model and its own escalation path.
229: - On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking and MINOR findings are minor; grade by the definition above, not by the label, so a finding labelled IMPORTANT that is only wording is minor.
```

### src/superclaude/hooks/hooks.json:165-180
```json
165:             "timeout": 1
166:           }
167:         ]
168:       },
169:       {
170:         "hooks": [
171:           {
172:             "type": "command",
173:             "command": "node \"$HOME/.claude/hooks/pragmatic-subagent.js\"",
174:             "timeout": 5
175:           }
176:         ]
177:       }
178:     ],
179:     "SubagentStop": [
180:       {
```

### .dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116030420/artifacts/phrase-scan.txt:1-14
```text
1: src/superclaude/agents/rf-qa.md:83:- Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items)
2: src/superclaude/agents/rf-qa-qualitative.md:84:- Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items)
3: src/superclaude/agents/rf-analyst.md:75:- Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items, merge g
4: src/superclaude/skills/readme/SKILL.md:542:- Step 3.2: Consolidate all 5 reports into `${TASK_DIR}qa/qa-consolidated-research-findings.md`. Union all findings, take more 
5: src/superclaude/skills/readme/SKILL.md:547:- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE instances of each of the 5 agent 
6: src/superclaude/skills/tdd/refs/build-request-template.md:122:- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst + QA i
7: src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:228:   - Findings on the same `file:line` with similar titles → merge, keep the higher severity and union the 
8: src/superclaude/skills/tech-reference/SKILL.md:510:- **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst instances and MUL
9: src/superclaude/skills/tech-reference/SKILL.md:513:  1. **Consolidate findings:** Merge all 5 agent reports into a single findings list at `${TASK_DIR}qa/qa-research-cons
10: src/superclaude/skills/operational-guide/SKILL.md:511:- **Parallel partitioning for large workloads:** When >6 research files exist, DOUBLE agent counts: spawn 4 rf-analy
11: src/superclaude/skills/task/SKILL.md:252:6. **Findings Consolidation (M3 Step 5)** — After ALL lens agents (Steps 3-5) return, read all QA reports and consolidate into 
12: src/superclaude/skills/task/SKILL.md:361:2. **Consolidate findings:** Read all QA reports. Merge findings into a single consolidated findings list at the designated path 
13: src/superclaude/templates/documents/agent_template_analysis.md:466:- Merging partition reports after all instances complete (union of findings, take the more severe ratin
14: src/superclaude/templates/documents/agent_template_qa.md:85:- Merging partition reports after all instances complete (union of findings, take the more severe rating for s
```

## Coverage slice

| Requirement | Mechanical match | Status (orchestrator manual read) | Spec citation |
|---|---|---|---|
| INF-001: the owner's go in chat is recorded in the stage ledger | Task 1, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:3 |
| INF-002: the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and the owner has read it | Task 1, ratio 0.889 | covered (mechanical match, not independently confirmed) | source.md:3 |
| INF-003: at least 5 shadow runs have been observed with zero safety misses (by the stage 0 definition) and no capture f... | Task 1, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:3 |
| INF-004: stage 0b's escape result is written and stage 0c's re-grade is written | none (best Task 1 ratio 0.375) | covered: Task 1 acceptance line 3 | source.md:3 |
| INF-005: The seeded-recall result is produced INSIDE this package (first task) and gates the rule switch by an acceptan... | Task 3, ratio 0.643 | covered (mechanical match, not independently confirmed) | source.md:3 |
| INF-011: Read the seeded set and answer key from the stage 0 package by id. | Task 1, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:12 |
| INF-012: Each pass (old rule text, new rule text) is run with freshly spawned agents, never agents continued from an ea... | Task 1, ratio 0.941 | covered (mechanical match, not independently confirmed) | source.md:12 |
| INF-013: Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the intervals, the cosm... | Task 1, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:12 |
| INF-014: `./artifacts/seeded-recall-result.md` exists and shows pass on all three requirements | Task 3, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:13 |
| INF-015: when a line shows fail, the task's check fails and the run halts for the owner's Ruling | Task 3, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:13 |
| INF-016: Keep the other lines (three bullets replaced, cap and own-scale bullets pinned by content, hook check through ... | Task 3, ratio 0.778 | covered (mechanical match, not independently confirmed) | source.md:13 |
| INF-017: reads the allow-list from `refs/scale-map.md` and allow-lists only files that exist in this stage: the auggie ... | Task 10, ratio 0.933 | covered (mechanical match, not independently confirmed) | source.md:14 |
| INF-018: The plugin mirror is NOT in the allow-list here (stage 4 adds it). The existence check applies to every file n... | Task 10, ratio 0.769 | covered (mechanical match, not independently confirmed) | source.md:14 |
| INF-019: that a later task of the same package makes false get an end point ("until Task N"). | none (best Task 11 ratio 0.444) | partial: rule stated in Constraints 'Pins are by content'; no acceptance line carries an end point | source.md:15 |
| INF-023: No template, rule-prompt, builder, researcher or spec-panel edit (stage 4). | none (best Task 3 ratio 0.444) | NOT STATED in the plan | source.md:20 |

