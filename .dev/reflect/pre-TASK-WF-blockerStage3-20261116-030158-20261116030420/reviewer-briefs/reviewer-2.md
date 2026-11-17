# Reviewer brief 2 (persona: qa; model class: opus)

## T1 card excerpt

### Coverage and acceptance

The source has no labelled requirement ids (parsed_count 0). Step 1B.0 Pass 2 emitted 25 quote-pinned inferred rows (`artifacts/coverage-matrix.yaml`; each quote is a verbatim substring of its cited `source.md` line). The deterministic containment rule (60 percent of a quote's content words inside ONE task) matched 18 of 25, so the mechanical `coverage_pct_union` is 0.72. The rule is noisy on prose. Manual mapping of the seven unmatched rows:

- INF-004 (stage 0b and 0c results are written): Task 1 acceptance line 3 (files `stage0b-escape-test.md` and `stage0c-regrade.md` exist). Covered; wording differs from the source.
- INF-006 (reuse the base tasks renumbered, with the Constraints) and INF-008, INF-010 (state stage 3 and the entry list; state that `/sc:implement` runs the whole package in order): the Constraints bullet "One package, one stage". Covered.
- INF-019 (acceptance lines a later task makes false get an end point): the Constraints bullet "Pins are by content" states the rule, but no acceptance line in the 11 tasks carries an "until Task N" end point (grep of the plan finds "until Task" only in the Constraints). Whether any line needs one is not argued anywhere.
- INF-023 (no template, rule-prompt, builder, researcher or spec-panel edit): NOT stated in the plan. The Constraints bullet "Not built here" lists the Jev call, `qa.md`, the own-scale primitives, `cli/**/*.py`, the 35 percent target and the cap, but not the stage 4 edit ban.
- INF-025 (no Jev call, key or account): the Constraints bullet "Not built here". Covered.

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

Persona instructions (qa): own the coverage and acceptance surface. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. For each source requirement, check that the task which claims it carries it in an acceptance line a verifier can run; check each acceptance line is satisfiable (the file, command, count or state it names exists or is created by an earlier task, and prints what the line says); check the plan's claims against the spec sections it cites (section 8.3 seeded recall, the section 12 stage 3 row, the section 13.1 metrics including M12, the section 13.2 triggers RT1 and RT2) and judge whether the prior review's recommendations R-002 to R-006 are resolved for stage 3. Test the T1 card's observations against the live files before you agree or disagree, and say so when you disagree.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:14:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md:1-20
```markdown
1: # Stage 3 plan request: pilot the new rule (issue #552)
2: 
3: Fourth of five plan packages (see `stage-requests/README.md`). This package changes the live review rule in `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md` and the task skill. Generate it only when ALL of these hold, each verified by reading the files and not by memory: the owner's go in chat is recorded in the stage ledger; the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and the owner has read it; at least 5 shadow runs have been observed with zero safety misses (by the stage 0 definition) and no capture failure; stage 0b's escape result is written and stage 0c's re-grade is written. The seeded-recall result is produced INSIDE this package (first task) and gates the rule switch by an acceptance line, not by a dependency line.
4: 
5: ## Base text
6: 
7: Reuse Tasks 31 to 40 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 4, stage 3; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 3 parts). Earlier stages' evidence is read by package id.
8: 
9: ## Changes to apply
10: 
11: - **Constraints.** State this is stage 3 and say what must be true at start (the list above). Stage 4 starts only after one audit window with no revert trigger tripped (the spec's section 13.2 triggers RT1 and RT2) and the owner's go in chat. State that `/sc:implement` runs the whole package in order, so the rule switch cannot start unless the first tasks pass.
12: - **Task 1 (the old Task 31, seeded recall run).** Read the seeded set and answer key from the stage 0 package by id. Each pass (old rule text, new rule text) is run with freshly spawned agents, never agents continued from an earlier pass, and the pass order is alternated across the three reviewers. Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the intervals, the cosmetic block share under both, and a pass or fail line for each of the three spec requirements.
13: - **Task for pragmatic.md (the old Task 33).** Its acceptance lines gain: `./artifacts/seeded-recall-result.md` exists and shows pass on all three requirements (safety recall equal to the old rule's, decision-bearing and missing recall within 5 points, cosmetic block share falls); when a line shows fail, the task's check fails and the run halts for the owner's Ruling. Keep the other lines (three bullets replaced, cap and own-scale bullets pinned by content, hook check through `src/superclaude/hooks/hooks.json`). Do not rely on `Depends on:` for this gate.
14: - **Constraints on the scan test (the old Task 40).** `tests/skills/test_review_merge_rule_scan.py` reads the allow-list from `refs/scale-map.md` and allow-lists only files that exist in this stage: the auggie file, `refs/rule.md` and the six stage 4 files. The plugin mirror is NOT in the allow-list here (stage 4 adds it). The existence check applies to every file named in the allow-list and passes in this stage.
15: - **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N").
16: - **New final task: stage 3 audit and owner summary (finding F8).** Write `./artifacts/stage3-summary-for-owner.md`: the seeded-recall result headline, the re-pinned test results, and the audit-window measures the spec's section 13 defines (the M-numbers it lists for stage 3 including M12, the rf-qa FAIL count per pilot gate, and the revert triggers RT1 and RT2 with their current state, read from the spec's text and not restated from memory). Say that the audit window runs after this package and is observed by the owner or operator, and end with the sentence that the owner's go for stage 4 is given in chat and not by this file.
17: 
18: ## Not to be done by the plan
19: 
20: No template, rule-prompt, builder, researcher or spec-panel edit (stage 4). No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.
```

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

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:93-101
```markdown
93: ## Task 6: Replace the merge rule in rf-analyst.md
94: 
95: Depends on: Task 3
96: 
97: Edit `src/superclaude/agents/rf-analyst.md`, the line that reads "union of findings, take the more severe rating for shared items, merge gap compila...", to the L1 text: union the findings, keep each reviewer's own grade visible, and let the consolidator grade by the rule; keep the rest of the line (the gap compilation) unchanged.
98: 
99: Acceptance criteria:
100: - `grep -n "more severe rating" src/superclaude/agents/rf-analyst.md` prints nothing.
101: - The gap-compilation words that followed on the line are still present.
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

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:129-138
```markdown
129: ## Task 9: Re-pin the audit tests for the QA agents
130: 
131: Depends on: Task 4, Task 5
132: 
133: Update `tests/audit/test_nfr_conv_9_zero_trust.py` (byte-exact PASS and FAIL bullets of `src/superclaude/agents/rf-qa.md` and its `.claude/` mirror) to the reworded "any blocking gap" bullets on both surfaces; update `tests/audit/test_invariant_preservation_NFR_6_through_10.py` (it imports `FAIL_BULLET` and `PASS_BULLET` from the first module) in the same change; re-pin `tests/audit/test_severity_floor_unweakened.py` (the SHA-256 of the `## Critical Rules` block of `rf-qa-qualitative.md` and its mirror, and Rule 6 verbatim) to the Task 5 text, including the rewritten verdict pairs; leave `tests/audit/test_dnsp_all_agents_fail_bypass.py` unchanged unless the cap text moved.
134: 
135: Acceptance criteria:
136: - `uv run pytest tests/audit -v` passes.
137: - The re-pinned hash in `test_severity_floor_unweakened.py` matches the new `## Critical Rules` block on both the source and the mirror surface after `make sync-dev`.
138: - `test_dnsp_all_agents_fail_bypass.py` passes without an edit.
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

### .dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md:39-55
```markdown
39: | # | Blocking | Finding |
40: |---|---|---|
41: | F1 | yes | The three owner gates (four go points in PLAN:20) cannot be enforced: `/sc:implement` has no phase option, no pause path, ignores a plan edited after the first task, and QA anchors a constraint breach only in a diff. |
42: | F2 | yes | Task 31 only reports the seeded-recall result and Task 33 depends on it finishing, not passing. A stronger `Depends on` line would gate nothing because `/sc:implement` ignores it; only an acceptance line on Task 33 works, and Task 31 cannot move out of Phase 4. |
43: | F3 | yes | Task 40's allow-list names the plugin mirror of `rule.md` and requires every named file to exist, but Task 46 creates the mirror later; Task 13's allow-list text does not list it. |
44: | F4 | yes | Task 41 gives `agent_template_analysis.md` a digest and a `v2` registry row, but the registry has exactly 11 digest rows without it and the file has no definition sentence. |
45: | F5 | yes | Task 25's T3 check fails on `commands/spec-panel.md:220` (and its plugin twin, line 218, and the installed variants). |
46: | F6 | yes | Later tasks make earlier acceptance lines false (Tasks 16, 25, 27, 13), so the final review cannot pass and the package cannot archive. New, from the probe. |
47: | F7 | yes | The fresh-findings set and the held-out split are never evaluated by any task. |
48: | F8 | yes | "Safety miss" is defined nowhere, and the stage 2 and 3 exit numbers have no task that measures them, so the owner has no numbers to read at the gates. New, from the probe. |
49: | F9 | no | Task 46 copies the skill folder before adding the plugin `canonical` registry row (part of the F3 combined fix). |
50: | F10 | no | The seeded-recall pass line has no minimum sample size. |
51: | F11 | no | Task 31 does not alternate pass order or require fresh spawns. |
52: | F12 | no | T3 may fail a `pointer-only` row before its pointer exists. |
53: | F13 | no | Wording-dependent scan trips: `scale-map.md` naming the three phrases, `rule.md` quoting the old sentence. |
54: | F14 | no | Coverage-matrix omissions in the review run. |
55: | F15 | no | Installed reference files cite package-relative `.dev/` paths. |
```

### .dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md:89-127
```markdown
89: ### Recommendation R-002: Gate Task 33 on the seeded-recall result by an acceptance line
90: 
91: - **File:** the same plan, Task 33 (and Task 31)
92: - **Change:** Add an acceptance line to Task 33 requiring `./artifacts/seeded-recall-result.md` to show pass on all three requirements; keep Task 31 in Phase 4. State a minimum sample size or call the pass line advisory, and require fresh spawns with alternated order.
93: - **Verifier:** Task 33's acceptance lines name the result file; Task 31 names fresh spawns and the alternation.
94: - **Linked deviation(s):** F2, F10, F11
95: - **Priority:** P0
96: 
97: ### Recommendation R-003: Fix the Task 13, 40 and 46 allow-list trio together
98: 
99: - **File:** the same plan, Tasks 12, 13, 40, 46
100: - **Change:** Choose one staging for the plugin-mirror entry (for example Task 40 allow-lists only existing files, and Task 46 adds the mirror to the allow-list and the registry before it copies the folder). Require `scale-map.md` to list files by path without the three phrases, and require `rule.md` not to quote the old definition sentence. Add a re-run of the merge-rule scan to Task 46's acceptance lines.
101: - **Verifier:** `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py -v` is named in Tasks 40 and 46.
102: - **Linked deviation(s):** F3, F9, F13
103: - **Priority:** P0
104: 
105: ### Recommendation R-004: Settle the registry and T3 contradictions
106: 
107: - **File:** the same plan, Tasks 16, 25, 41, 45
108: - **Change:** Decide that `agent_template_analysis.md` gets the merge-rule text only (then Task 41 covers four template files), or add a twelfth registered carrier. Exempt `pointer-only` and `installed-only` rows from the `src/superclaude` path check, keep the test off `~/.claude`, and check a pointer-only row only once its pointer is present.
109: - **Verifier:** Task 16 and Task 41 counts agree; Task 25's T3 text names the exemptions.
110: - **Linked deviation(s):** F4, F5, F12
111: - **Priority:** P0
112: 
113: ### Recommendation R-005: Scope the acceptance lines that later tasks supersede
114: 
115: - **File:** the same plan, Tasks 13, 16, 25, 27
116: - **Change:** Add "until Task N" (or "at the end of this phase") to each acceptance line that a later task makes false, so the final review does not read it as a standing requirement.
117: - **Verifier:** a re-read of Tasks 13, 16, 25 and 27 shows each superseded line with its end point.
118: - **Linked deviation(s):** F6
119: - **Priority:** P0
120: 
121: ### Recommendation R-006: Give the fresh-findings set and the held-out split a consuming task
122: 
123: - **File:** the same plan (a new Phase 3 task, or reword PLAN:93)
124: - **Change:** Add a stage 2 task that runs the classifier on `./artifacts/fresh-findings.md`, the held-out half and the reviewer-called-minor set with a recorded judge, and writes the result for the owner; or state that the evaluation is deferred past this plan and why.
125: - **Verifier:** `grep -n "fresh-findings" <plan>` finds a task after Phase 1 that consumes the file.
126: - **Linked deviation(s):** F7
127: - **Priority:** P0
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:676-680
```markdown
676: ### 8.3 Seeded-defect recall
677: 
678: <!-- Source: Base (original) -->
679: 
680: Plant known defects in a held-out deliverable, across four classes: decision-bearing false claim, missing required section, safety risk, and cosmetic. Review it under the old rule and the new rule with the same reviewers. Required: safety recall equals the old rule's; recall of decision-bearing and missing items stays within 5 points of the old rule's; the share of cosmetic items that block falls. A candidate existing set is the 44-defect spec ledger (20 blocking, 19 medium, 5 minor), validated by 20 agents, named in a run-2 scope file [E: seen as text at `R2/research/scope/06-brainstorm-process-redesign.md:242`; the artifact itself is [U]]. That file also says the whole #346 series was tuned on it, so use it as a sanity check and plant fresh defects for the real test.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:942-948
```markdown
942: | Stage | Entry condition | What happens | Exit condition | Rollback |
943: |---|---|---|---|---|
944: | 0. Measure (this program, offline) | this spec reviewed | 0a: the scored table and five runs with a fixture or approved judge, only if the table exists. 0b: the retrospective escape test on run 2 (section 8.4). 0c: three blind agents that did not write the rule re-grade the table under the old and the new text, paired, only if the table exists. Inventory freeze: every Grep of section 10 re-run, including the frozen FAIL-trigger Grep (REQ-30), with results stored | a written result: escape estimate with its interval; when the table exists, how many old-blocking rows become non-blocking and the confusion matrix | nothing changed |
945: | 1. Offline scaffold | stage 0 result written; owner go | the skill folder with registry rows all `legacy` (T1 and T2 accept the legacy text in registered rows); the ledger reader and writer with the codec; ledger adapters; the fixture judge; property tests; crash, reconcile and consent tests; the install check. No carrier is edited | T1 to T4, T6 to T8, T11 to T13 and T17 green offline | delete the new files |
946: | 2. Shadow beside the old rule | stage 1 exit | the task skill and tech-research gates write the ledger and make the per-run offer (it replaces the output style's "once per loop" ask for that run); reviewers emit `rests_on` while the old definition still decides; the classifier runs in shadow; the safety route GR12 is live; the final-gate sweep GR7 is built; `core/WORKER-CONTRACT.md` gains the three keys (REQ-12) | at least 5 shadow runs observed; ledger volume and `consumer-unknown` share known; offers answered; shadow agreement reported; zero safety misses and no capture failure | stop writing the ledger; restore the old carrier text by the three-step revert (section 9.4) |
947: | 3. Pilot | 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (section 8.3) met; 0c as well when the table exists; owner go | `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` move to digest v2 together; the stage 3 merge-rule lines of section 10.3 (task skill, rf-qa, rf-qa-qualitative, rf-analyst; L1); L2 fix-pass checks; L6 for rf-qa, and Rule 6 if OD16 chooses (b), with its test re-pinned in the same change; the cadence pins move | one audit window (section 8.2) with no revert trigger tripped; M12 reported | the three-step revert of the pilot rows to `legacy` |
948: | 4. Propagate | stage 3 exit; owner go | templates, rule prompts, builders and researchers to v2; the stage 4 lines of section 10.3; the spec-panel narrowing; the plugin mirror and parity test; T2 becomes strict (no legacy definition sentence in `src/` or `plugins/`) | drift tests green and strict; a second audit window clear | per-row three-step revert |
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:958-975
```markdown
958: ### 13.1 Metrics
959: 
960: | # | Metric | Definition | Baseline source | Direction |
961: |---|---|---|---|---|
962: | M1 | Blocking findings per gate | F_0 under the rule in force, unique findings, not summed reviewer duplicates | stage 2 paired data. Run-2 reference: Gate 1 11 (old rule), Gate 2 23 reviewer-level and 8 consolidated, Gate 3 2 [V] | down |
963: | M2 | Fix cycles and third reviews per gate | count | stage 2 | down |
964: | M3 | Gate wall-clock | from the run's own logs, not from cycle-control headers, which are not clock times [V] | stage 2 | down |
965: | M4 | Escape rate | escapes over n in the audit rate sample, with a Wilson interval (section 8.2) | none; the audit creates it | at or below the trigger |
966: | M5 | Seeded-defect recall | per class, new rule against old rule (section 8.3) | the old rule, same planted set | not below the old rule's |
967: | M6 | `consumer-unknown` share of non-blocking rows | count | stage 2 | down over time |
968: | M7 | Ledger size and offer outcome | rows per run; share of offers answered; filed, declined, ignored | stage 2 | answered, not ignored |
969: | M8 | Reviewer disagreement | findings where the reviewers' own grades differ, and how many of them end `consumer-unknown` with the `reasked` flag | stage 2 | down |
970: | M9 | Fix-induced findings per fix pass | `origin: fix-induced` count over fix passes | Gate 1 of run 2: 2 findings in 1 fix pass [V] | down |
971: | M10 | Classifier agreement, kappa, recall on validated blockers, flip rate, S misses | section 7.6 | the scored table | reported, not gated |
972: | M10b | Mixed rule versions | the share of reviewer runs that saw two different rule versions (the injected output style and the carrier digest), per carrier version | stage 3 | zero after stage 4 |
973: | M11 | Cause of each extra fix cycle | each extra fix cycle attributed to fix-induced, definition-driven or other findings | run 2 Gate 1: the second cycle was forced by the fix-induced NEW-1 and NEW-2 [V] | definition-driven cycles down |
974: | M12 | rf-qa FAIL count per pilot gate | FAIL verdicts per gate in the stage 3 pilot; flat counts falsify the pilot. Rule 6 is reported as a known counter-example until OD16 is decided | stage 2 | down |
975: | M13 | Shadow results by judge | every shadow metric split by judge id and version | stage 2 | reported; evidence for OD4 counts only for the judge that would hold authority |
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:979-992
```markdown
979: ### 13.2 Revert triggers
980: 
981: A revert means: restore the previous digest for the stage in force through the three-step revert of section 9.4 (repository edit and drift tests, a release naming the refresh command, a refresh on each machine) and go back to the stage before. There is no faster brake in version 1 (section 9.4, OD17). Each trigger is stated with what it can actually detect.
982: 
983: | # | Trigger | Detects | Note on power |
984: |---|---|---|---|
985: | RT1 | Any safety-class escape in the audit or the seeded set, or any confirmed safety finding that ended as a plain follow-up | a Safety finding graded Medium or Note | a single event; needs no sample size; acts through the three-step revert |
986: | RT2 | In an audit window, the 95 percent Wilson lower bound on the escape rate of the simple random sample exceeds 2 percent | a rate that is confidently above 2 percent | at n = 60 this is 4 or more escapes (3 of 60 gives a lower bound of about 1.7 percent; 4 of 60 about 2.6 percent) [computed]. Oversampled strata never feed this trigger. Two escapes in a window is a yellow flag: the owner reviews each one |
987: | RT3 | Seeded recall of decision-bearing or missing items falls more than 5 points below the old rule, or safety recall falls below it | a rule that is simply too loose | the planted set must be large enough to see 5 points; size it in the plan |
988: | RT4 | The owner reports a decision-bearing defect that shipped from the ledger | escape type (c) | counts as an escape in M4 |
989: | RT5 | After 5 runs under stage 3, M1 is not at least 25 percent lower than stage 2 | no benefit | a stop-and-investigate trigger, not an automatic revert, and not tied to the 35 percent target |
990: | RT6 | M9 is not lower than baseline | L2 is not working | fix L2; the rule can stay |
991: | RT7 | M6 exceeds 40 percent of non-blocking rows | the decision basis is not being supplied | redesign L4 and the consumer line; the 40 percent is a placeholder to set from stage 2 |
992: | RT8 | The offer is ignored in 3 consecutive runs | ledger rot | redesign the offer; not a rule revert |
```

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:372-382
```markdown
372: ## Task 31: Run the seeded-defect recall set under the old and the new rule text
373: 
374: Depends on: Task 7
375: 
376: Run the set of Task 7 (`./artifacts/seeded-recall-set.md` and the planted deliverable under `./artifacts/seeded/`) as spec section 8.3 says. Spawn the same three reviewer agents twice on the planted deliverable, once with today's rule text (the definition bullets and the Medium bullet of `src/superclaude/output-styles/pragmatic.md`) and once with the digest of spec section 4.1, never showing them the answer key. Score each planted defect as found or missed and as blocking or not, per class. Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts, the share of cosmetic defects that block under each, the Wilson 95 percent intervals, and a pass or fail line for each of the three requirements of Task 7 (safety recall equals the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the cosmetic block share falls). This task reports the result; the owner decides whether stage 3 may proceed.
377: 
378: Acceptance criteria:
379: - `./artifacts/seeded-recall-result.md` holds per-class recall under both rule texts with intervals, the cosmetic block share under both, and a pass or fail line for each of the three requirements.
380: - The reviewer agent ids are recorded and the answer key is not among the files they were given.
381: - The file states that the result is evidence for the owner's go and does not itself grant it.
382: 
```

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:473-482
```markdown
473: ## Task 40: Add the merge-rule reverse-scan test
474: 
475: Depends on: Task 34, Task 35, Task 36, Task 37
476: 
477: Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude`, matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`: `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, `src/superclaude/skills/sc-review-severity/refs/rule.md` and its plugin mirror path, and, until Phase 5, the six stage 4 files (`src/superclaude/skills/tech-reference/SKILL.md`, `src/superclaude/skills/readme/SKILL.md`, `src/superclaude/skills/tdd/refs/build-request-template.md`, `src/superclaude/skills/operational-guide/SKILL.md`, `src/superclaude/templates/documents/agent_template_qa.md` and `src/superclaude/templates/documents/agent_template_analysis.md`). Each Phase 5 task that edits one of those files removes it from the allow-list in the same change.
478: 
479: Acceptance criteria:
480: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 34 to 37, with no hit in `src/superclaude/cli/` counted.
481: - A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
482: - The allow-list is read from `refs/scale-map.md` and a test fails when a file named there does not exist.
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

## Coverage slice

| Requirement | Mechanical match | Status (orchestrator manual read) | Spec citation |
|---|---|---|---|
| INF-001: the owner's go in chat is recorded in the stage ledger | Task 1, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:3 |
| INF-002: the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and the owner has read it | Task 1, ratio 0.889 | covered (mechanical match, not independently confirmed) | source.md:3 |
| INF-003: at least 5 shadow runs have been observed with zero safety misses (by the stage 0 definition) and no capture f... | Task 1, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:3 |
| INF-004: stage 0b's escape result is written and stage 0c's re-grade is written | none (best Task 1 ratio 0.375) | covered: Task 1 acceptance line 3 | source.md:3 |
| INF-005: The seeded-recall result is produced INSIDE this package (first task) and gates the rule switch by an acceptan... | Task 3, ratio 0.643 | covered (mechanical match, not independently confirmed) | source.md:3 |
| INF-006: renumbered 1 onward, with its `## Constraints` (stage 3 parts) | none (best Task 1 ratio 0.2) | covered: Constraints 'One package, one stage' | source.md:7 |
| INF-007: Earlier stages' evidence is read by package id. | Task 1, ratio 0.833 | covered (mechanical match, not independently confirmed) | source.md:7 |
| INF-008: State this is stage 3 and say what must be true at start (the list above). | none (best Task 11 ratio 0.5) | covered: Constraints | source.md:11 |
| INF-009: Stage 4 starts only after one audit window with no revert trigger tripped (the spec's section 13.2 triggers RT... | Task 11, ratio 0.824 | covered (mechanical match, not independently confirmed) | source.md:11 |
| INF-010: State that `/sc:implement` runs the whole package in order, so the rule switch cannot start unless the first t... | none (best Task 3 ratio 0.4) | covered: Constraints | source.md:11 |
| INF-011: Read the seeded set and answer key from the stage 0 package by id. | Task 1, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:12 |
| INF-012: Each pass (old rule text, new rule text) is run with freshly spawned agents, never agents continued from an ea... | Task 1, ratio 0.941 | covered (mechanical match, not independently confirmed) | source.md:12 |
| INF-013: Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the intervals, the cosm... | Task 1, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:12 |
| INF-014: `./artifacts/seeded-recall-result.md` exists and shows pass on all three requirements | Task 3, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:13 |
| INF-015: when a line shows fail, the task's check fails and the run halts for the owner's Ruling | Task 3, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:13 |
| INF-016: Keep the other lines (three bullets replaced, cap and own-scale bullets pinned by content, hook check through ... | Task 3, ratio 0.778 | covered (mechanical match, not independently confirmed) | source.md:13 |
| INF-017: reads the allow-list from `refs/scale-map.md` and allow-lists only files that exist in this stage: the auggie ... | Task 10, ratio 0.933 | covered (mechanical match, not independently confirmed) | source.md:14 |
| INF-018: The plugin mirror is NOT in the allow-list here (stage 4 adds it). The existence check applies to every file n... | Task 10, ratio 0.769 | covered (mechanical match, not independently confirmed) | source.md:14 |
| INF-019: that a later task of the same package makes false get an end point ("until Task N"). | none (best Task 11 ratio 0.444) | partial: rule stated in Constraints 'Pins are by content'; no acceptance line carries an end point | source.md:15 |
| INF-020: Write `./artifacts/stage3-summary-for-owner.md`: the seeded-recall result headline, the re-pinned test results... | Task 11, ratio 1.0 | covered (mechanical match, not independently confirmed) | source.md:16 |
| INF-021: the M-numbers it lists for stage 3 including M12, the rf-qa FAIL count per pilot gate, and the revert triggers... | Task 11, ratio 0.913 | covered (mechanical match, not independently confirmed) | source.md:16 |
| INF-022: Say that the audit window runs after this package and is observed by the owner or operator, and end with the s... | Task 11, ratio 0.933 | covered (mechanical match, not independently confirmed) | source.md:16 |
| INF-023: No template, rule-prompt, builder, researcher or spec-panel edit (stage 4). | none (best Task 3 ratio 0.444) | NOT STATED in the plan | source.md:20 |
| INF-024: No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superc... | Task 3, ratio 0.667 | covered (mechanical match, not independently confirmed) | source.md:20 |
| INF-025: No Jev call, key or account. | none (best Task 1 ratio 0.25) | covered: Constraints 'Not built here' | source.md:20 |

