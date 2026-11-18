# Reviewer brief 2 (persona: qa; model class: opus)

## T1 card excerpt

### Tier 1 summary (orchestrator pass; verify, do not trust)

The T1 pass found the three blocking findings of the earlier review addressed in text by revision 3 and found no blocking defect of its own; tier 2 is forced by the parse-density guard (coverage_degraded: parsed-sparse: 45 inferred rows against 1 parsed row), not by low confidence. Earlier findings as the T1 pass read them: F1 (gate after edit) addressed by Task 4 (a read-only gate task, PLAN:109-118), Task 6's own pre-edit re-check (PLAN:140), the `v2` read at the start of Tasks 7 to 10 (PLAN:158, PLAN:177, PLAN:193, PLAN:203) and the frozen arm copies (PLAN:78); F2 (variants) addressed in Task 3 (PLAN:82, PLAN:96); F3 (rules 8 and 9) addressed in Tasks 7 and 8 (PLAN:160, PLAN:179) with grep acceptance lines (PLAN:168, PLAN:185).

T1 minor observations (each may be wrong): O1 Task 6 says "except the two listed below" but lists three test files (PLAN:142, PLAN:152). O2 SRC still carries the unrevised base text "not by a dependency line" and "Do not rely on `Depends on:` for this gate" (SRC:3, SRC:13) while Task 6 has `Depends on: Task 2, Task 3, Task 4` (PLAN:138) and also re-checks the gate in its body. O3 Tasks 11 to 14 have no first-line check that the rule files were switched, unlike Tasks 7 to 10 (PLAN:216, PLAN:227, PLAN:238, PLAN:251); matters only when an owner override lets a halted task close. O4 Task 10's `git diff` acceptance lines compare with HEAD, so they also show uncommitted stage 1 and 2 edits in the same folder (PLAN:207, PLAN:208). O5 the request's "the owner has read" the stage 2 summary (SRC:3) is not checked beyond file existence and the ledger go (PLAN:41). Unsettled points the T1 pass did not check: whether the `grep -c` counts of 0 and 2 in the Task 7 and 8 acceptance lines hold once the digest and the L3 text are inserted; the audit tests other than the four Task 12 names (a dozen read rf-qa.md: for example tests/audit/test_dynamic_enumeration_inv_010.py, tests/audit/test_nfr_conv_6_self_contained.py, tests/audit/test_evidence_bound_tb_add_8.py); the plan against SPEC sections 4, 8, 9, 10, 11 and 13 (metric ids, RT texts, OD16, L1 to L6, section numbers).

Context: the plan under review is stage 3 of five (one plan per stage) of the blocker-classification work (GitHub issue #552). It changes the live review rule (the pilot): `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, the follow-up sweep call of `/sc:implement`, and the tests that pin them. It has been revised in place twice. This is the THIRD and final review. The earlier review (review 2, of revision 2 of the plan) is at `.dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116174401/REPORT.md` (3 blocking findings F1 to F3: the seeded-recall gate ran after the `pragmatic.md` edit; Task 3's outcome words and threshold; QA rules 8 and 9 outside the edit lists; 13 non-blocking F4 to F16). The plan was then revised to 14 tasks in 5 phases (revision 3; notes in `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md` section "Revision 3" and in `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/codegraph-grounding.md` section "Revision 3"). Repository root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (every repo-relative path below is relative to it; read the files as <root>/<path>). Short names: PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md` (267 lines); SRC = `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md` (the stage request, the driving file, 69 lines); SPEC = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (the merged spec the plan is written against); README = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md` (stage ledger); BRIEF2 = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/revision2-brief.md` (shared decisions); OQ = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/OPEN-QUESTIONS.md`; S0, S1, S2, S4 = the stage 0, 1, 2 and 4 plan files `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md`, `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`, `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` and `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md`. The stage 0, 1, 2 and 4 packages are plans that have not run: a file they will create (for example `src/superclaude/skills/sc-review-severity/refs/rule.md`) does not exist yet and that is expected; check that the producing plan creates it under that name and with the content PLAN expects, and that PLAN reads it by that name. Stage 4 (S4) is the plan that continues from this one: check that nothing PLAN leaves behind contradicts what S4 assumes (the allow-list rows, the registry rows and states, the `Kept mechanical gates` section, the plugin position, the spec-panel carrier left unedited, the tests left red or re-pinned, the files stage 3 edits that stage 4 also edits).

What you must check: (a) that each earlier blocking finding F1 to F3 (and, briefly, F4 to F16) the plan says it fixed is really fixed in the live plan; (b) that revision 3 introduced no new defect (numbering, dependencies, acceptance lines that a later task makes false, missing paths, contradictions with BRIEF2, S2 and S4); (c) the plan against SPEC (rollout stage 3 row, sections 4.1 to 4.4, 8.2, 8.3, 9.4, 10.1 to 10.5, 11.1, 13). Also check each plan claim about a live file or a live test (line numbers, sentences, test names, command names) by reading the file.

Persona instructions (qa): audit the coverage matrix AGAINST the spec body in your grounding hunks (SRC whole, SPEC sections); surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check the plan against SPEC section by section: the rollout stage 3 row (SPEC:947), L1 to L6 (SPEC:270 to 275), REQ-04, REQ-06, REQ-26 and REQ-27, sections 8.2 and 8.3 (the sample size of the audit window; the seeded set, the old and new text, the classes and the minimum n), sections 10.1, 10.3, 10.4 and 10.5 (which lines change, the 13 merge lines in 10 files), section 11.1 (which tests are re-pinned and how), sections 13.1 and 13.2 (metrics M1 to M13 and triggers RT1 to RT8: check that every metric, baseline source and trigger PLAN quotes, computes or marks pending matches the spec text, and that "RT1 (seeded part) and RT3 judged now, the rest pending" is a fair split), and the owner decisions OD1 to OD17 that PLAN lists as followed. For each acceptance criterion of Tasks 1 to 14, ask whether a check as written can be run and can pass, and whether it can pass vacuously or fail for a reason unrelated to the task (for example a `grep -c` that counts the digest text inserted by the same task, or a hash defined two different ways). Test the statistics in Task 3: with 3 reviewers per arm, found = more than half of the valid reviewers; Wilson intervals over planted defects; the "minimum n" read from the stage 0 `seeded-recall-set.md` (read S0 for what that file will hold); the five lines R1, R1b, R2a, R2b, R3 against SPEC section 8.3 and RT1 and RT3; whether an arm with 2 valid reviewers makes "2 of 2" a sound threshold; the NOT-MEASURABLE rules. Read the live files the plan edits (`src/superclaude/output-styles/pragmatic.md`, `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/agents/rf-analyst.md`) and the live tests it re-pins (`tests/skills/test_review_severity_rule.py`, `test_review_severity_mapping.py`, `test_implement_severity_static.py`, `test_review_prompt_overrides.py`, `tests/audit/test_nfr_conv_9_zero_trust.py`, `tests/audit/test_severity_floor_unweakened.py`, `tests/audit/test_invariant_preservation_NFR_6_through_10.py`) and say whether the plan's description of them is right and whether the edit lists cover every line that would contradict the new digest (for example other instruction lines that fail or block on doubt or by label in the three agents and in `pragmatic.md`).

How to grade: grade each finding blocking or minor by consequence. Blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format. A finding whose consequence is a wrong measurement that gates the rule switch, an acceptance line that cannot pass (or that passes vacuously) on the task it guards, a gate that runs after the edit it protects, or a live-rule edit that contradicts the rule it ships, is blocking. Do not invent findings and do not work to a quota; a review with no finding must say what you checked and why you found no defect.

How to work: you have Read, Grep, Glob and code-search tools only; you run nothing and edit nothing. Audit the hunks below and re-Read the files you cite; every `file:line` you cite is re-read by an independent validator and dropped if it does not match, so quote exactly and cite the line where the text sits (re-read the line, do not cite from memory). Read the whole PLAN first (267 lines), then the earlier review's findings in the earlier report. Tell the orchestrator about any file you could not read. Do not rely on the observations in the T1 excerpt above: they come from one agent and may be wrong; verify or reject each one yourself.

How to answer: return your card as your final message, plain markdown, at most about 7,500 characters, with these sections only: `## Earlier findings` (one line each for F1 to F3 of the earlier review, and a one-line statement for F4 to F16 taken together or singly where one is not fixed: fixed, partly fixed or not fixed, with the `file:line` that shows it), `## Findings` (numbered F1, F2, ...; each with `Blocking: yes` or `Blocking: no`, a one-line title, evidence as `file:line` plus a short verbatim quote, the consequence in one or two sentences, and a one-line fix), `## Checked and sound` (what you verified and found fine), `## Self-report` (one line `confidence: 0.NN`). Write plain English; no em dashes.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T19:05:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (the index holds Python, YAML, JavaScript and TypeScript only; the files you audit are Markdown, so use Read, Grep and Glob)
### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md:1-69
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
14: - **Constraints on the scan test (the old Task 40).** `tests/skills/test_review_merge_rule_scan.py` reads the allow-list from `refs/scale-map.md` and allow-lists only files that exist in this stage: the auggie file, `refs/rule.md`, the six stage 4 files and the two code files that hold the phrases and are not changed (`cli/roadmap/remediate_parser.py`, `cli/pipeline/fmea_classifier.py`), plus the `exempt-by-retirement` entries the stage 1 scale map lists for the retired task skill and task-builder files. No plugin mirror is listed (no package makes one). The existence check applies to every file named in the allow-list and passes in this stage.
15: - **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N").
16: - **New final task: stage 3 audit and owner summary (finding F8).** Write `./artifacts/stage3-summary-for-owner.md`: the seeded-recall result headline, the re-pinned test results, and the audit-window measures the spec's section 13 defines (the M-numbers it lists for stage 3 including M12, the rf-qa FAIL count per pilot gate, and the revert triggers RT1 and RT2 with their current state, read from the spec's text and not restated from memory). Say that the audit window runs after this package and is observed by the owner or operator, and end with the sentence that the owner's go for stage 4 is given in chat and not by this file.
17: 
18: ## Not to be done by the plan
19: 
20: No template, rule-prompt, builder, researcher or spec-panel edit (stage 4). No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.
21: 
22: ## Revision 2 (2026-11-16)
23: 
24: Plan revised in place (`TASK-WF-blockerStage3-20261116-030158`): 11 tasks in 4 phases became 13 tasks in 5 phases. Inputs: the NEEDS-REVISION merged card of the pre-execution review (findings F1 to F15), the shared decisions of `revision2-brief.md`, and the owner answers of 2026-11-16 in `OPEN-QUESTIONS.md` section 2. Each finding was checked against the live files before the plan changed.
25: 
26: Changes to the "Changes to apply" list above:
27: 
28: - **Entry check (F1).** New Task 1 runs every entry check before any agent is spawned or file is edited. The 5 observed runs are no longer read from the stage 2 summary (it is written when stage 2 finishes and cannot show later runs): the stage ledger row for stage 3 carries the owner go, the list of shadow-run folders the owner counted and the owner's safety-confirmation file, and Task 1 recounts them with the stage 2 package's `shadow_summary.py --confirmed-misses` (a printed "not computable" is a FAIL). The task also checks that the stage 1 and stage 2 files this package reads exist, that the sweep call of the implement protocol is present without `--promote`, and that the digest of `refs/rule.md` equals the spec's REQ-01 block (SHA-256 recorded; F5 third point). Missing or short counts halt the run; no fix pass edits a checked file (new Constraint "Gates are read, never edited").
29: - **Baselines (F7).** New Task 2 writes `./artifacts/stage3-baselines.md`: M1 and M12 counted per run and gate from the shadow-run folders, the RT5 threshold (75 percent of the M1 mean), and M10b stated as having no earlier baseline.
30: - **Seeded recall (F2, F3).** Task 3 (old Task 1) now states the SubagentStart hook confound, tells every reviewer to apply and quote only the text given, keeps model class and brief identical across arms, reports changes as a lower bound (the recall-equality lines are biased toward pass, the cosmetic line toward fail), and lists reviewers that quoted the old rule. It defines the unit (the planted defect, majority of 2 of 3 reviewers), five result lines (R1, R1b, R2a, R2b, R3) and the outcome words PASS, FAIL, ADVISORY-PASS, ADVISORY-FAIL and NOT-MEASURABLE for advisory classes, zero bases and small n, and the owner ruling that lets a non-PASS line continue (dated on or after the result file, citing its SHA-256, void when the hash differs). R1b is the RT1 seeded part and is never advisory.
31: - **Fix helper (F14).** Task 4 (old Task 2) gains a command, `superclaude review fixcheck`, so the Fix Cycle text of the QA agents has something to call.
32: - **pragmatic.md (F5, F6 support, brief).** Task 5 gates on the Task 3 outcome lines (acceptance line, not a dependency), checks that the shipped digest's SHA-256 equals the tested one and that the registry row reads `v2`, and owns the Medium cadence change from per loop to per run (the offer stays in the output style, OD2). The spec-panel scale bullet and the spec-panel carrier keep their text until stage 4.
33: - **QA agents (F5, F8, F13, F15).** Tasks 6 and 7 name the stage 0 package for the frozen inventory, check that the registry row reads `v2`, run the registry drift test, keep the Retry Monotonicity tokens, and Task 7 applies the L2 and L3 text at the cap sentences of lines 809 and 994 of `rf-qa-qualitative.md`. The one-offer sentence now names the top-level session's once-per-run offer instead of the task skill's.
34: - **Task skill dropped (decision 1).** Old Task 7 (edits to `src/superclaude/skills/task/SKILL.md`: consolidation text, fix agent step, cap choices, `promote` on, registry check F10) is removed. The skill stays on the allow-list as `exempt-by-retirement`; tests that pin only retired carriers are not re-pinned.
35: - **Follow-up carrier (decision 2).** New Task 9 adds `--promote` to the one sweep call in `src/superclaude/skills/sc-implement-protocol/SKILL.md` and `refs/managed-workspace.md`, updates the stage 2 test `tests/skills/test_implement_follow_up_sweep.py`, and leaves `refs/qa.md` unedited. The choice is stated in the Constraints: the carrier records and prints and asks nothing, and the offer question stays with the top-level session and the consent-bound filing path.
36: - **Plugin surface (decision 4).** No new plugin surface. The only plugin files touched are the byte-equal twins of the two implement-protocol files Task 9 edits, pinned by `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py`. `plugins/superclaude/commands/spec-panel.md` is not edited (its source carrier is unchanged until stage 4).
37: - **Tests (F5, F9, F12, F15).** Task 10 (old Task 8) adds `test_review_severity_registry.py`, `test_implement_follow_up_sweep.py`, `test_task_builder_merge.py` and `tests/review/test_review_rules_text.py` to the re-run list, states that `legacy` registry rows stay pinned to a frozen copy of the old bullets, and renames the artifact `./artifacts/fixture-diff.md`. Task 12 (old Task 10) fixes the stale "Tasks 34 to 37" reference and reads the stage 1 allow-list format (`allowed` or `exempt-by-retirement`, paths relative to `src/superclaude/`).
38: - **Summary (F4, F6, F7).** Task 13 (old Task 11) judges RT1 (seeded part) and RT3 from the Task 3 result and marks only the window-dependent triggers pending; adds the baselines; states the three switch steps (release naming the refresh command, refresh per machine, install check `make doctor` and a `grep -c` on the installed style) as coming before the audit window, records the observed output of both commands, and states the revert path for the three digest rows and for the edits without a registry row.
39: - **Constraints (F11).** Added: the stage 4 items are not done here; retired carriers; follow-up carrier; plugin surface; no mapping of `follow-ups.md` to `review-ledger/1`; gates are read, never edited. The two "never staged" wordings were rephrased so the gate check passes.
40: 
41: Cross-stage needs reported to the coordinator: the stage 2 `shadow_summary.py` must accept folders and `--confirmed-misses` and print the three counts; the stage ledger row for stage 3 must name the folders and the confirmation file; the stage 2 sweep call lines must stay free of `--promote` and `--write` until this stage.
42: 
43: ## Revision 3 (2026-11-16)
44: 
45: Plan revised in place a second time (`TASK-WF-blockerStage3-20261116-030158`): 13 tasks in 5 phases became 14 tasks in 5 phases. Input: the NEEDS-REVISION merged card of the second pre-execution review (3 blocking findings F1 to F3, 13 non-blocking F4 to F16), the stage 4 review's contradiction about the plugin mirror, and the revised stage 2 plan. Each finding was checked against the live files before the plan changed. The task numbers below are the new ones.
46: 
47: Blocking:
48: 
49: - **Gate order (F1).** The seeded-recall gate is now Task 4, a read-only task that edits nothing under `src/`, `tests/` or `plugins/` and runs before every task that edits a rule file; `/sc:implement` runs a task's edit before its review, so a halt at Task 4 leaves no rule file switched. Task 4 writes `./artifacts/seeded-recall-gate.md` (result-file SHA-256, the five outcome words, each ruling found, the `git status --short -- src tests plugins` line that must equal Task 1's). Task 6 (the `pragmatic.md` edit, old Task 5) depends on Task 4, starts by checking the gate itself from the result file and the ledger (not only from the gate file), edits nothing and fails when it does not hold, and its first acceptance line recomputes the result file's SHA-256 and re-checks that every non-PASS line has a ruling citing it. Only a ruling recorded on the stage ledger row (line id, date, SHA-256) counts; a confirmation given to a `/sc:implement` Ruling prompt does not (new Constraint "Gate order" and the changed "Gates are read, never edited"). Tasks 7 to 10 begin by reading that the `pragmatic.md` registry row reads `v2`. Task 3 now freezes the old-arm and new-arm blocks as copies (`./artifacts/old-arm-block.md`, `new-arm-block.md`) with their SHA-256, so a re-run after a halt reads the same old text.
50: - **Recall variants (F2).** Task 3 names the controlling variant (valid reviewers only: a reviewer is valid when its quoted sentences come from its own arm's rule text), the found threshold fixed before dispatch (more than half of the arm's valid reviewers: 2 of 3 or 2 of 2), and the rule that an arm with fewer than 2 valid reviewers makes every line that needs it NOT-MEASURABLE (a non-PASS word that needs a ruling). Each line carries one outcome word from the controlling variant and the as-run word beside it; the as-run variant never sets a word.
51: - **Rules 8 and 9 (F3).** Tasks 7 and 8 now rewrite principle 8 "NO LENIENCY" and rule 9 "Report honestly" of `rf-qa.md` and `rf-qa-qualitative.md` (consequence wording: an unverified claim is graded by the digest; "Unknown is not no" replaces "When in doubt, fail it"; an unverified safety claim stays open for verification), each with `grep -c -F` acceptance lines. The Confidence Gate "UNCHECKED ... FAILURES" lines are not edited (they count the reviewer's own unfinished checks and grade no finding). The same lines in the four rule-prompt files and `agent_template_qa.md` are stage 4 text and are named in the "Not built here" constraint. Rule 9 of the qualitative agent sits inside the `## Critical Rules` block, so Task 12 re-pins that block hash against the new Rule 6, Rule 9 and L3 text.
52: 
53: Non-blocking:
54: 
55: - **F4** applied: Task 3 states the scope difference of the two arms (old arm whole block, new arm digest alone, REQ-04 and the once-per-run wording in neither).
56: - **F5** applied: per-trigger `grep -c -F` lines in Task 7; Task 8 requires every hit the frozen inventory lists for the qualitative agent to be changed or listed (check-result examples such as `"System should be fast" = FAIL` stay, listed with that reason).
57: - **F6** applied: Task 6 keeps "never to meet a quota" and runs `tests/skills/test_review_prompt_overrides.py`.
58: - **F7** applied: Task 1 defines the hashed bytes once (the lines between the two fence lines, whitespace collapsed, UTF-8; the spec side with the leading `> ` removed) and every later task uses it.
59: - **F8** applied: Task 6 keeps the sentence "Medium and Note findings are not rechecked in later rounds." after the pointer line.
60: - **F9** applied: Task 14 gives the baseline source of each of M4, M5, M6, M9, M11.
61: - **F10** applied: Task 12 labels `BLOCKING_SEVERITIES` as the fixture scorer's label scale, corrects the hash description (the verdict pairs lie outside the block) and Task 8 bars the softening tokens from Rule 6 and Rule 9.
62: - **F11** applied: the plugin-mirror clause is gone from Task 13 (old Task 12); no stage builds a plugin mirror.
63: - **F12** partly applied: Task 1 lists the fields the stage 3 ledger row must hold (go with date, folders, run count, confirmation-file path; later the rulings), but the ledger file `stage-requests/README.md` is not edited here (shared file); the coordinator adds the fields to its instructions.
64: - **F13** applied: Tasks 7 and 8 write the L3 text after the final period of the cap sentence and check the `new` strings of the cap-edit fixture rows with `grep -F`.
65: - **F14** applied: Tasks 7 and 8 record kept gates in a section `Kept mechanical gates` at the end of `refs/scale-map.md` with a stated bullet form, and Task 13 reads only the `Merge-rule allow-list` section.
66: - **F15** applied: the L2 text has a missing-command clause (one line in the fix log, carry on), the same as the stage 2 sweep paragraph.
67: - **F16** applied: the revised stage 2 script prints "not computable" for an empty file or a file without a `reviewed:` line and 0 for a reviewed empty list; Task 1 follows that form and records the entry count; Task 2 marks a one-gate RT5 figure as a single-gate figure.
68: 
69: Cross-stage facts: stage 2 `shadow_summary.py` reads `--confirmed-misses` entries `<run_id>:<row id>` plus a `reviewed: <date> by <name>` line (matches Task 1); Task 10 changes the stage 2 test's assertion on "never `--promote` and never `--write`" and its `--promote` mutation case.
```
### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:185-214
```markdown
185: ## 4. The proposed rule in plain words
186: 
187: ### 4.1 The rule
188: 
189: <!-- Source: Base (original, modified) - wording from Variant 3 section 3 merged per Change #PC-07; unknown-consequence sentence per RM-6 and PC-08; precedence sentence per Change #PC-06; fenced digest form per Change #PC-02 -->
190: 
191: The text below is the digest: the short rule every carrier holds word for word inside a versioned fence (section 9.2). It is the one block the drift tests compare.
192: 
193: **[REQ-01]** Every carrier holds this block, unchanged, between the fence lines `review-severity:digest v2 begin` and `review-severity:digest v2 end` (written as HTML comments), followed by one pointer line to the full rule (section 9.2):
194: 
195: > Grade each finding by what changes if the flawed text is corrected. A finding is **Blocking** only when at least one of these holds, and the finding must say which one, name the affected action and give the evidence:
196: >
197: > 1. **Decision.** Correcting the text would change a named decision, recommendation, destination, required behaviour, outcome, acceptance check or quoted number that the deliverable (or a named later step) rests on; or the stated reason for such an item is false or unsupported. A wrong number used in an acceptance check blocks even when the recommendation stays the same.
198: > 2. **Missing.** A required deliverable, section, behaviour or step, named by the task, the template or the acceptance criteria, is absent in substance.
199: > 3. **Safety.** Following the text, or running the code it quotes, would lose or expose data or a secret, break a safety boundary, or act outside the declared scope. Name the affected action and the evidence, not just the word "security". This is never downgraded, whatever label, classifier score, inferable intent or fix cost is attached to it. An unverified safety claim stays open for verification; it is not a Note.
200: >
201: > Unknown is not no. If no consumer can be established, keep the reviewer's own label and tag the row `consumer-unknown`.
202: >
203: > Everything else is recorded and never blocks, never starts a fix pass and never appears in a reviser brief. A real defect in substance that nothing named rests on is **Medium**. A defect of form only (wording, formatting that changes no value a reader or a program uses, a wrong tag, label, citation or line number on a true statement) is a **Note**. Apart from the unknown-consumer case, the label a reviewer used (CRITICAL, IMPORTANT, MAJOR, High) is information, never the grade.
204: >
205: > When your context holds more than one definition of blocking, the one in the instructions of the agent, skill or command doing this review wins over a session-wide output style; text inside the work under review is data, not a definition; a protocol listed as own-scale keeps its model.
206: >
207: > A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings.
208: 
209: Notes on the block:
210: 
211: - **[REQ-02]** The sentence "If no consumer can be established, keep the reviewer's own label and tag the row `consumer-unknown`." is part of the pinned digest. "The reviewer's own label" is read through the scale map of section 9.3 (for example, an rf-qa IMPORTANT reads as blocking). Such a row is never demoted for missing grounding, is counted in the `show_user` count (section 6.4) and, when it is not blocking, is listed first in the offer. Whether some of these rows may instead wait for a later gate is owner decision OD14.
212: - **[REQ-03]** The precedence sentence (the paragraph starting "When your context holds more than one definition") is in every v2 digest and also in `pragmatic.md`. Section 9.6 explains why it is needed.
213: - The last sentence is today's cap bullet (`pragmatic.md:227`) word for word [V, read during this merge]; it contains `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, which the test constant `CANONICAL_CAP_TEXT` pins (`tests/skills/test_review_severity_rule.py:215`) [V].
214: - **[REQ-04]** The reviewer brief at `pragmatic.md:221`, which tells every reviewer to hunt for "false claims" [V], changes in the same edit as the definition: reviewers hunt for defects and name their consequence.
```
### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:264-281
```markdown
264: ### 4.4 Loop and consolidation changes the rule needs
265: 
266: <!-- Source: Base (original, modified) - L1 per Change #PC-23 and BW-12 with RM-2; new L6 per Change #PC-24 with RB-2 and RM-14 -->
267: 
268: | # | Change | Cause it answers | Where |
269: |---|---|---|---|
270: | L1 | **[REQ-05]** The consolidator grades by the rule and keeps every reviewer's own grade visible. Label-max merging ("highest severity wins") is replaced at all 13 lines in 10 files that state it, in two stages. A blocking grade that names a consumer the code check does not disprove stands. A blocking grade that names no consumer goes back to the reviewer once (GR2). If it still names none, the reviewer's label stands, the row is tagged `consumer-unknown` with a `reasked` flag and listed first; it is never demoted for missing grounding. | RC2 | the 13 lines of section 10.3; the reverse-scan test T5 pins the removal |
271: | L2 | A fix pass runs every mechanical check that exists over the lines it edited before it hands back: table pipe count, byte-present quotes, recomputed counts, link existence. The results go into the fix log. A defect a verifier finds that the fix introduced carries `origin: fix-induced` and is graded by the same rule. | RC3 | `rf-qa.md` Fix Cycle section; `task/SKILL.md:254` |
272: | L3 | The cap and the regression and monotonicity halts count Blocking findings only (they already count "blocking", so this follows from the definition). At the cap the escalation offers three choices: fix by hand, accept and file (the finding becomes a follow-up tagged `accepted-blocker`), or stop. The cap stays at 2 fix cycles. | RC1 | `rf-qa.md:402-415` [E]; `task/SKILL.md:258` [V], `372` [E] |
273: | L4 | The task builder writes a consumer line for each phase output. | RC4 | `task-builder` and the MDTM templates 01 and 02 [E] |
274: | L5 | Medium and Note findings are never rechecked. A fix that touches a Medium row's location does not reopen it. The final-gate sweep (GR7) and a linked escalation (section 6.2) are the only ways a recorded row becomes blocking. | RC1 | same text as today (`pragmatic.md:226`) [V] |
275: | L6 | **[REQ-06]** The fixed FAIL triggers in the QA agents (lines that fail a review by label or by a fixed rule, ignoring the "a decision depends" test) are each either rewritten to "grade by the three conditions; the label is information", or kept as a named mechanical gate mapped to condition 2 (Missing) when a template requires the item, with the keep recorded in the scale map. "Flag exact duplicates as IMPORTANT" becomes Note unless a condition holds. Rule 6 of rf-qa-qualitative ("contradictions are always IMPORTANT or CRITICAL ... never minor") is decided by owner decision OD16. The pinning tests change in the same step. | RC1, RC6 | section 10.4 (a frozen Grep at stage 0, not a remembered list) |
276: 
277: ### 4.5 What does not change
278: 
279: <!-- Source: Base (original) -->
280: 
281: Security, data-loss and safety findings stay blocking, including a finding the reviewer called minor or Medium. The verdict stays binary (PASS or FAIL). A review with no finding is still valid and must say what it checked (`pragmatic.md:222`) [V]. A reviewer still never invents a finding and never works to a quota. The cap of 2 fix cycles (3 reviews) and the regression and monotonicity halts stay.
```
### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:660-686
```markdown
660: ### 8.2 Measured false-negative audit
661: 
662: | Element | Design |
663: |---|---|
664: | Unit | one non-blocking finding (Medium or Note) from a completed run, taken from the ledger and the reviewers' notes |
665: | Frame | every non-blocking row of the audit window (5 runs or 60 rows, whichever is later) |
666: | Rate sample | a simple random sample of the frame. RT2 (section 13.2) is computed on this sample only |
667: | Diagnostic strata | tier (Medium, Note); tag (`consumer-unknown`, `unsettled`, none); deliverable kind; whether the reviewer's own grade was blocking and consolidation lowered it, or the reviewer said minor. Riskier strata may be oversampled in a separate diagnostic sample; oversampled results describe those strata only and never feed RT2 |
668: | Protected risk | every protected-risk disagreement (every `protected-risk-dispute` row, and every row where S and the reviewer disagree) is reviewed, not sampled |
669: | Auditor | a different model class from the reviewers, blind to the reviewer's grade and the ledger tier, shown the deliverable and the finding and **no rule text**. Asked: "if this text stays, would a reader acting on the deliverable do something wrong or reach a wrong decision? Name it." A second auditor shown the old rule text is the comparison arm |
670: | Escape (operational) | a sampled finding escaped if (a) its flawed text or number appears uncorrected in a later deliverable's decision-basis section (a rule-free code check), or (b) the blind auditor names a concrete wrong result and a second auditor and a code check agree, or (c) a person later reports the defect as consequential |
671: | Sample size | with zero escapes, the 95 percent upper bound is about 3 divided by n: 5.0 percent at n = 60, 3.0 percent at n = 100, 2.0 percent at n = 150 [computed]. So n = 60 can only support a claim of "under 5 percent". A revert trigger below that is not testable at n = 60 |
672: | Report | escapes over n with a Wilson 95 percent interval: for the rate sample, pooled; for each diagnostic stratum, its own interval with its sampling fraction stated. Per window and rolling |
673: | Safety | every sampled finding also goes through the GR1 vocabulary scan. Any safety-class escape is a revert trigger regardless of rate |
674: | Who | not the reviewer family, not the classifier. The owner reviews the sample list and every escape |
675: 
676: ### 8.3 Seeded-defect recall
677: 
678: <!-- Source: Base (original) -->
679: 
680: Plant known defects in a held-out deliverable, across four classes: decision-bearing false claim, missing required section, safety risk, and cosmetic. Review it under the old rule and the new rule with the same reviewers. Required: safety recall equals the old rule's; recall of decision-bearing and missing items stays within 5 points of the old rule's; the share of cosmetic items that block falls. A candidate existing set is the 44-defect spec ledger (20 blocking, 19 medium, 5 minor), validated by 20 agents, named in a run-2 scope file [E: seen as text at `R2/research/scope/06-brainstorm-process-redesign.md:242`; the artifact itself is [U]]. That file also says the whole #346 series was tuned on it, so use it as a sanity check and plant fresh defects for the real test.
681: 
682: ### 8.4 Stage 0b: a retrospective escape test that can be specified now
683: 
684: <!-- Source: Base (original) -->
685: 
686: Run 2 gives one rule-free check today. Take a random sample of de-duplicated minors from Gates 2 to 5 and the final validation (the checks that ran under the override), and for each test by code whether its flawed text or figure appears uncorrected in `R2/RESEARCH-REPORT-review-panel-unification-run2.md`. The count of hits over n, with its interval, is a first escape estimate that does not depend on the same rule that graded the findings. Limit: the report was itself produced under the override, so a minor that was corrected anyway cannot be told apart from one that never mattered. State that in the result.
```
### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:752-770
```markdown
752: ### 9.4 Delivery to installed copies, and what a switch or revert really costs
753: 
754: <!-- Source: Variant 3 (haiku:backend), section 7 - merged per Change #PC-04 as amended by RB-1 and RM-10 -->
755: 
756: Installers skip files and folders that already exist unless forced: an existing skill folder is skipped unless `force` (`install_skills.py:100-104`) [V]; an existing user-setup file, including an output style, is kept and listed as stale without `force` (`install_user_setup.py:77-78`; the message at 117-118 says those files "were NOT updated (run with --force or `superclaude update` to refresh"; output styles use the same copy routine, 186-197) [V]; an existing core file is skipped (`install_core.py:70`) [V].
757: 
758: **[REQ-26]** Delivery rules:
759: 
760: 1. **First install.** The new skill folder reaches an existing `~/.claude` without `--force`, because the folder does not exist there yet.
761: 2. **Every later change** to that folder, to `pragmatic.md` or to a rule prompt stays stale on an installed machine until `superclaude update` or an install with `--force`.
762: 3. **A stage switch or a revert is three steps, never "a registry edit":** (a) in the repository, edit the affected carriers' digests and registry rows and re-run the drift tests; (b) ship a release whose note names the refresh command; (c) refresh each machine (`superclaude update` or install with `--force`), confirmed by the install check.
763: 4. **There is no immediate brake.** The three-step revert is the only brake. The safety revert trigger RT1 acts through it. Machines that are not refreshed keep the new rule until they are; this is residual risk RK14, mitigated by the release note and the install check. A brake that needs no reinstall would be a new design: a named file that every carrier digest reads, with its format, writer and precedence stated (OD17).
764: 5. **[REQ-27] Install check.** A `make doctor` check, backed by a pytest test, compares the digest versions held by the installed carriers with the packaged (source) registry and reports mismatches. It reads the packaged registry, not an installed `registry.yaml`, because the installed skill folder is skipped once present (`install_skills.py:102`) [V]. A `doctor` target already exists (`Makefile:23`) [V, this merge]. Each ledger header records the digest versions its carriers held (section 6.2).
765: 
766: ### 9.5 Plugin surface
767: 
768: <!-- Source: Variant 1 (opus:architect), decision D9 - merged per Change #PC-05 -->
769: 
770: The plugin tree has no output-style hook: a Grep for `pragmatic` under `plugins/superclaude` finds no file [V: LC-09]. Its carriers of blocking text are `commands/spec-panel.md`, `rules/prompts/document_review_loop_prompts.md` and `skills/sc-implement-protocol/refs/qa.md` [V: invariant probe]. These hold the inline digest. At stage 4 a hand mirror of the skill folder goes into `plugins/superclaude/skills/` with a parity test (T15); the plugin's `skills/` is hand-kept and holds 4 skills today [V: LC-20]. Until then the release note says plugin-only users keep today's text.
```
### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:778-870
```markdown
778: ## 10. Files and primitives that would change
779: 
780: <!-- Source: Base (original, modified) - merge-rule inventory per Change #PC-23 (BW-05), fixed FAIL triggers per Change #PC-24 with RB-2 and RM-14, counts per BW-13 and BW-14, new files per Changes #PC-01, #PC-15 and RM-15 -->
781: 
782: All paths are under `src/superclaude/` unless stated. This is a list for the `/sc:workflow` plan, not an edit list. Because far more than five files change, a written plan must exist before any edit, and the plan re-runs every pattern below before editing (the stage 0 inventory freeze, section 12).
783: 
784: **Patterns and counts** (case-sensitive unless stated; run over `src/superclaude`):
785: 
786: - `Grade every review finding as blocking or minor` (the definition sentence, S1): 11 files, 11 matching lines [V].
787: - `Blocking is a real defect` (both cases): 11 files, 11 occurrences [V: invariant probe]. The seed brief's "12 occurrences" is not reproduced.
788: - `Minor findings never fail a review` (S2): 11 files [V: Variant 1 check].
789: - `at most 2 fix cycles \(3 reviews\)` (the cap, S3): 12 files, the 11 plus `commands/spec-panel.md` [V].
790: - `CRITICAL and IMPORTANT findings are blocking` (S5): 7 files [V].
791: - `follow-up candidates`: 3 files, 7 matching lines [V].
792: - `2 fix cycles`: 22 files, 120 matching lines, 139 occurrences (a line can hold more than one) [V]. Most of these carry the cap, not the definition.
793: - Merge rule, case-insensitive: `highest severity|more severe`, then `higher severity|max(imum)? severity|worst (severity|rating)|highest (rating|grade)` [V: LC-04]. Results in section 10.3.
794: - Fixed FAIL triggers: the frozen Grep of section 10.4.
795: - Tasklist: "High or Medium" or "Medium (blocking)" in `skills/sc-tasklist-protocol/SKILL.md`: 7 lines [V].
796: - Plugin tree: the definition sentence 0 files; merge-rule patterns 0 matches [V].
797: - Method caveat: the Grep tool skips gitignored folders, so it reports 0 copies under the project `.claude/`; a plain `grep -rlF` finds 6 copies of S1 there (rf-qa, rf-qa-qualitative, 2 document templates, 2 MDTM templates) [V: diff analysis]. Any plan step that counts `.claude/` copies must not use the Grep tool.
798: 
799: ### 10.1 The 11 files that carry the definition
800: 
801: | File | Line | Group |
802: |---|---|---|
803: | `output-styles/pragmatic.md` | 225 | output style; reaches every subagent. Also lines 221 (reviewer brief) to 231 [V: Read] |
804: | `agents/rf-qa.md` | 108 | QA agent |
805: | `agents/rf-qa-qualitative.md` | 108 | QA agent |
806: | `templates/documents/agent_template_qa.md` | 161 | template |
807: | `templates/documents/skill_template.md` | 828 | template |
808: | `templates/workflow/01_mdtm_template_generic_task.md` | 644 | template |
809: | `templates/workflow/02_mdtm_template_complex_task.md` | 655 | template |
810: | `rules/prompts/automated_qa_workflow_qa_prompt.md` | 11 | QA prompt |
811: | `rules/prompts/doc_code_analyst_qa_prompt.md` | 27 | QA prompt |
812: | `rules/prompts/documentation_expert_qa_prompt.md` | 28 | QA prompt |
813: | `rules/prompts/recruiting_expert_qa_prompt.md` | 27 | QA prompt |
814: 
815: Each is a carrier: at its stage it replaces S1, S2 and S5 (where present) with the digest and pointer line; the cap text stays word for word.
816: 
817: ### 10.2 Variants and carriers of the Medium mechanism
818: 
819: | File | What it carries | Pattern and count |
820: |---|---|---|
821: | `commands/spec-panel.md` | own scale; Review Loop bullets at lines 259 to 261 [V]; FR-8 at 332 [E] | `follow-up candidates`: 3 matches |
822: | `rules/prompts/document_review_loop_prompts.md` | reviewer briefs; Medium wording at 31, 32, 48 [E] | `follow-up candidates`: 3 matches |
823: | `output-styles/pragmatic.md` | Medium and the spec-panel scale at 230 to 231 [V] | `follow-up candidates`: 1 match |
824: | `cli/review/card_convert.py` | word translator, lines 71 to 83 [V] | no change |
825: 
826: The plugin copies of the first two files exist; `spec-panel.md` differs between `src` and the plugin, and the review-loop prompts are identical [V: diff analysis, `cmp`].
827: 
828: ### 10.3 "Highest severity wins": 13 lines in 10 files
829: 
830: **[REQ-05, location]** Label-max merging is replaced at all of these lines, in two stages [V: LC-04]:
831: 
832: | File | Lines | Stage |
833: |---|---|---|
834: | `skills/task/SKILL.md` | 252, 361 | 3 |
835: | `agents/rf-qa.md` | 83 | 3 |
836: | `agents/rf-qa-qualitative.md` | 84 | 3 |
837: | `agents/rf-analyst.md` | 75 | 3 |
838: | `skills/tech-reference/SKILL.md` | 510, 513 | 4 |
839: | `skills/readme/SKILL.md` | 542, 547 | 4 |
840: | `skills/tdd/refs/build-request-template.md` | 122 | 4 |
841: | `skills/operational-guide/SKILL.md` | 511 | 4 |
842: | `templates/documents/agent_template_qa.md` | 85 | 4 |
843: | `templates/documents/agent_template_analysis.md` | 466 | 4 |
844: 
845: Not changed: `skills/sc-auggie-review-protocol/SKILL.md:228` ("keep the higher severity") is a code-review de-duplication on its own scale, a scale-map row unchanged in version 1. `cli/roadmap/remediate_parser.py` (lines 55, 301, 365) assigns severity in code and is out of scope with the roadmap checkers. `cli/pipeline/fmea_classifier.py` and `pr_submit/severity_router.py` rank unrelated things [V: LC-04]. An earlier draft said the rule also sits in task-builder and tech-research; the Grep does not show that, and the claim is withdrawn. The reverse-scan test T5 searches `src/` and `plugins/` for `highest severity`, `more severe rating` and `higher severity`, with the scale-map rows as its allow-list.
846: 
847: ### 10.4 Fixed FAIL triggers in the QA agents
848: 
849: **[REQ-30]** The stage 0 inventory of fixed FAIL lines is a frozen Grep, not a remembered list. Patterns: `= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT`, run over `src/superclaude/{agents,skills,templates,rules}` at stage 0 and stored with the stage 0 results. Lines known today:
850: 
851: | File | Lines | Stage | Treatment (L6) |
852: |---|---|---|---|
853: | `agents/rf-qa.md` | 152 ("Any incomplete file = FAIL"), 162 ("Any untagged doc claim = FAIL"), 168 to 170 ("Will this gap reduce report quality? -> IMPORTANT"; "Any CRITICAL or IMPORTANT gap = overall FAIL"), 182 to 183 (PASS or FAIL by label), 327 ("Flag exact duplicates as IMPORTANT"), 389 and 476 (count CRITICAL and IMPORTANT as blocking) [V: LC-13]; also 221, 316, 333, 334 [V, this merge] and 494, 548 [E: plan review] | 3 | each rewritten to "grade by the three conditions; the label is information", or kept as a named mechanical gate mapped to condition 2 (Missing) when a template requires the item (likely for 152 and 162), with the keep recorded in the scale map; 327 becomes Note unless a condition holds |
854: | `agents/rf-qa-qualitative.md` | 990, Rule 6: "Contradictions are always IMPORTANT or CRITICAL ... that's never minor" [V, this merge] | 3, if OD16 says so | OD16: keep as a named mechanical gate mapped to condition 1, or rewrite so a contradiction nothing rests on is a follow-up. Until decided, Rule 6 stays and metric M12 notes it as a known counter-example |
855: | `templates/documents/agent_template_qa.md` | 333 (the same Rule 6 text) [V, this merge] | 4 | follows OD16 |
856: 
857: `tests/audit/test_severity_floor_unweakened.py` pins Rule 6 verbatim and hashes the whole `## Critical Rules` block of rf-qa-qualitative and its `.claude/` mirror (lines 53 to 61 and 166 to 189) [V, this merge]. `tests/audit/test_nfr_conv_9_zero_trust.py` pins rf-qa's PASS and FAIL bullets, and `tests/audit/test_invariant_preservation_NFR_6_through_10.py` imports them [V]. Each changes in the same step as the lines it pins.
858: 
859: ### 10.5 Loop and cap text
860: 
861: Those cap-family files that need an edit because they say who counts, merges or escalates:
862: 
863: | Group | Files and lines | Edit |
864: |---|---|---|
865: | Task skill | `skills/task/SKILL.md`: 252 (merge) [V], 254 (fix agent) [V], 258 (halt at the cap) [V], 361 (Follow-Up Items) [V], 372 [E] | L1, L2, L3, ledger |
866: | QA agents | `agents/rf-qa.md` 398, 402 to 415, 549 [E]; `agents/rf-qa-qualitative.md` 110, 809, 994 [E]; `agents/rf-task-builder.md` 383 to 389, 415 to 421 [E] | the cap counts Blocking only; fix-step checks (L2) |
867: | Builders and researchers | `skills/task-builder/SKILL.md` 875 [E]; `skills/tech-research/SKILL.md` 488 to 490, 517 to 519, 555, 562 [E]; `skills/roadmap`, `readme`, `tech-reference`, `operational-guide` cap lines [E] | point at the shared rule; the consumer line (L4) in the task builder |
868: | Tasklist | `skills/sc-tasklist-protocol/SKILL.md` 1439, 1450, 1531, 1567, 1571, 1610, 1614 [V] | only if OD7 says so |
869: | Reflect | `skills/sc-reflect-protocol/SKILL.md` 1540 [V] | only if OD6 says so |
870: | Worker contract | `core/WORKER-CONTRACT.md` 33 (key list), WC-4 status mapping, 39 (coordinator duties) [V] | the three keys of REQ-12 (stage 2) |
```
### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:889-912
```markdown
889: ## 11. Tests that pin the rule text, and what changes
890: 
891: <!-- Source: Base (original, modified) - inventory replaced per Change #PC-26 (11 modules, patterns named; BW-04), with Variant 1 section 10 and Variant 3 section 9 rows; new tests merged from Variant 1 T1 to T8 per Change #PC-03; RB-2, RM-4, RM-8, RM-10, RM-12 additions -->
892: 
893: ### 11.1 Existing pins
894: 
895: Eleven test modules and two fixtures pin the rule or the Medium text [V: LC-19, LC-05]. `canonical_rule_bullets()` is defined in `tests/skills/test_review_severity_rule.py` (lines 78 to 96) and is used by three test modules (this file, `test_review_severity_mapping.py` and `test_implement_severity_static.py`) [V]. Symbols and phrases that identify a pin, for the plan to re-run: `canonical_rule_bullets`, `S1_S3_FILES`, `S5_FILES`, `CANONICAL_CAP_TEXT`, `FAIL_BULLET`, `PASS_BULLET`, the definition sentence, `asks the user once per loop`, `## Critical Rules`, and `"src/superclaude" not in`. The set of modules depends on the pattern: a broader pattern run during this merge (adding `fix-cycle` and related words) matched 16 files, including halt-emitter and pr-submit modules [V, this merge]; and the `"src/superclaude" not in` assertion also matches unrelated modules [V: LC-19]. So the plan re-runs the named patterns and does not trust a remembered count.
896: 
897: | Test module | What it pins | Breaks if | Change |
898: |---|---|---|---|
899: | `tests/skills/test_review_severity_rule.py` | five bullets after the binary-verdict bullet of `pragmatic.md` (`canonical_rule_bullets()`); S1 to S3 verbatim in the 10 files of `S1_S3_FILES`; S5 in the 6 files of `S5_FILES = S1_S3_FILES[:6]`; `CANONICAL_CAP_TEXT` (line 215); banned phrases; two edit tables of 161 and 139 rows [V for the symbols; E for the row counts] | any S1 to S5 bullet is reworded or moved; a copy differs | `canonical_rule_bullets()` reads the digest from `refs/rule.md`; `S1_S3_FILES` and its `[:6]` slice become registry rows, in the same step as the fence; cap and banned-phrase checks unchanged; edit-table rows whose new text is S1 or S2 are re-pinned or retired deliberately |
900: | `tests/skills/test_review_severity_mapping.py` | the Medium and spec-panel bullets directly after S5 in `pragmatic.md`, including "asks the user once per loop whether to open an issue" (lines 72 and 128 [V, this merge]); spec-panel literals in `src` and `plugins` | the Medium wording, the cadence or the position changes | the cadence pins move at stage 3 (section 6.1 step 6); literals move to assertions on `refs/rule.md` and `refs/scale-map.md`; add ledger and offer pins |
901: | `tests/skills/test_implement_severity_static.py` | `pragmatic.md` S2 and S4 exact strings; the rest pins `qa.md` | S2 or S4 is reworded | S4 kept word for word; the S2 assertion moves to the digest; `qa.md` pins stay |
902: | `tests/skills/test_review_loop_extension.py` | `at most 2 fix cycles (3 reviews)` in the spec-panel cap bullet | the cap bullet changes | cap stays; no change expected |
903: | `tests/skills/test_review_prompt_overrides.py` | brief lint and the zero-finding and "no minimum count" sentences | a pinned sentence is removed when text is consolidated | keep those sentences; they are not part of the digest |
904: | `tests/skills/test_spec_panel_review_loop.py` | imports `CANONICAL_CAP_TEXT` (line 15) [V], a transitive pin | the cap constant changes | none expected, because the cap text stays |
905: | `tests/audit/test_nfr_conv_9_zero_trust.py` | byte-exact PASS and FAIL bullets in `rf-qa.md` and its `.claude/` mirror | those bullets are reworded | reword the FAIL bullet to "any blocking gap" with L6 at stage 3 and re-pin both surfaces |
906: | `tests/audit/test_invariant_preservation_NFR_6_through_10.py` | imports `FAIL_BULLET` and `PASS_BULLET` from the module above (lines 95 to 101) [V] | the imported bullets change | changes in the same step as its source module |
907: | `tests/audit/test_severity_floor_unweakened.py` | a SHA-256 of rf-qa-qualitative's `## Critical Rules` block in source and mirror; Rule 6 verbatim ("... that's never minor") [V, this merge] | any line in that block changes | re-pin only with OD16: under option (b), Rule 6 and the hash are re-pinned in the same change at stage 3 |
908: | `tests/audit/test_dnsp_all_agents_fail_bypass.py` | a hash of the `rf-team-lead` fix-cycle line | that line changes | no change unless the cap text moves |
909: | `tests/review/test_review_rules_text.py` | structure of the review-loop prompts file and `"src/superclaude" not in TEXT` (line 92) [V] | structural moves | keep; the ledger sentence goes inside an existing section |
910: | Fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` | the old and new strings of past rule edits [V: files exist] | an old or new row no longer holds | update only approved changed strings; do not bypass historical protections wholesale |
911: 
912: ### 11.2 New tests the plan must add
```
### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:936-994
```markdown
936: ## 12. Rollout stages
937: 
938: <!-- Source: Base (original, modified) - restructured per Change #PC-28 from Variant 2 section 12, Variant 3 section 10 stages 0 and 1 and Variant 1 section 11; stage 2 duties per RM-8 and RM-9; L6 and Rule 6 per Change #PC-24 and RB-2; inventory per RM-14; revert per RB-1 -->
939: 
940: No stage starts before its entry condition is met and the owner has seen the numbers. Own-scale adapters (OD6, OD7, OD8, OD10) and classifier authority (OD4) are owner decisions, not stages, and no stage implies them.
941: 
942: | Stage | Entry condition | What happens | Exit condition | Rollback |
943: |---|---|---|---|---|
944: | 0. Measure (this program, offline) | this spec reviewed | 0a: the scored table and five runs with a fixture or approved judge, only if the table exists. 0b: the retrospective escape test on run 2 (section 8.4). 0c: three blind agents that did not write the rule re-grade the table under the old and the new text, paired, only if the table exists. Inventory freeze: every Grep of section 10 re-run, including the frozen FAIL-trigger Grep (REQ-30), with results stored | a written result: escape estimate with its interval; when the table exists, how many old-blocking rows become non-blocking and the confusion matrix | nothing changed |
945: | 1. Offline scaffold | stage 0 result written; owner go | the skill folder with registry rows all `legacy` (T1 and T2 accept the legacy text in registered rows); the ledger reader and writer with the codec; ledger adapters; the fixture judge; property tests; crash, reconcile and consent tests; the install check. No carrier is edited | T1 to T4, T6 to T8, T11 to T13 and T17 green offline | delete the new files |
946: | 2. Shadow beside the old rule | stage 1 exit | the task skill and tech-research gates write the ledger and make the per-run offer (it replaces the output style's "once per loop" ask for that run); reviewers emit `rests_on` while the old definition still decides; the classifier runs in shadow; the safety route GR12 is live; the final-gate sweep GR7 is built; `core/WORKER-CONTRACT.md` gains the three keys (REQ-12) | at least 5 shadow runs observed; ledger volume and `consumer-unknown` share known; offers answered; shadow agreement reported; zero safety misses and no capture failure | stop writing the ledger; restore the old carrier text by the three-step revert (section 9.4) |
947: | 3. Pilot | 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (section 8.3) met; 0c as well when the table exists; owner go | `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` move to digest v2 together; the stage 3 merge-rule lines of section 10.3 (task skill, rf-qa, rf-qa-qualitative, rf-analyst; L1); L2 fix-pass checks; L6 for rf-qa, and Rule 6 if OD16 chooses (b), with its test re-pinned in the same change; the cadence pins move | one audit window (section 8.2) with no revert trigger tripped; M12 reported | the three-step revert of the pilot rows to `legacy` |
948: | 4. Propagate | stage 3 exit; owner go | templates, rule prompts, builders and researchers to v2; the stage 4 lines of section 10.3; the spec-panel narrowing; the plugin mirror and parity test; T2 becomes strict (no legacy definition sentence in `src/` or `plugins/`) | drift tests green and strict; a second audit window clear | per-row three-step revert |
949: 
950: Why shadow comes before the pilot: the whole design rests on reviewers being able to name a consumer honestly. Stage 2 measures that while the old definition still decides, so a failure costs nothing.
951: 
952: Templates note: task files already generated from the old MDTM templates keep the old text. The reverse scan covers `src/` and `plugins/` only; old task folders under `.dev/tasks/` are not migrated.
953: 
954: ## 13. Metrics, measurement plan and revert triggers
955: 
956: <!-- Source: Base (original, modified) - M8 per RM-2; M10b per RM-11; M11 to M13 per Change #PC-31; RT1 and RT2 per Change #PC-27; revert definition per Change #PC-04 and RB-1 -->
957: 
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
976: 
977: The owner's 35 percent score target is not a metric and gates nothing.
978: 
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
993: 
994: RT2's wording matters. A rule such as "revert if the escape rate exceeds 2 percent" cannot be tested at n = 60, because 0 escapes in 60 only supports "under 5 percent". Triggers are therefore stated as interval bounds, and windows pool runs until the sample supports the claim.
```
### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:1023-1046
```markdown
1023: ## 15. Owner decisions, each with a recommendation
1024: 
1025: <!-- Source: Base (original, modified) - ids renamed OD (BW-03); OD1 per Change #PC-01, OD3 per Change #PC-13, OD4 per Change #PC-14, OD8 per BW-10, OD10 per Change #PC-03; OD14 per Change #PC-08; OD15 per Change #PC-21 and RB-3; OD16 per RB-2; OD17 per RB-1 -->
1026: 
1027: | # | Question in plain words | Options | Recommendation | Why |
1028: |---|---|---|---|---|
1029: | OD1 | Where does the full rule live? | a delegate-only skill folder; a core file; a rule prompt | the skill folder `sc-review-severity`, with the digest inline in every carrier | the only home with all three surfaces and `verify-sync` checking (section 9.1); inline digests keep grading reliable when nothing is read |
1030: | OD2 | How often is the person offered the follow-up list? | once per loop (today); once per run plus at an escalation halt | once per run, plus at any escalation halt | run 2 had six gate checks; a per-loop question would be asked six times |
1031: | OD3 | May finding text (private-fork excerpts) go to TypeSafe or any other external judge? Request a key and a budget? | yes for the five-run experiment; only with zero data retention or an accepted processing contract; no | decide privacy first. Approve Jev for the five-run experiment only if the account has zero data retention or the processing contract is accepted; say separately whether the LLM judge is approved. Request a key only after that | a privacy denial skips every external judge, including the LLM fallback (REQ-23); the price (about $0.08 [E]) is not the real cost |
1032: | OD4 | May the classifier ever have authority (downgrade, confirm, or route to a person beyond the safety route)? | never; one-directional routing only; calibrated routing after audited shadow evidence | none in version 1. Revisit only with audited shadow evidence from the same judge id and version that would hold authority; never auto-downgrade S | no person is present in unattended runs; hiding risk is the larger cost; evidence from one judge does not transfer to another (M13) |
1033: | OD5 | Does a gap-list or open-question entry count as decision basis? | yes; no | no | it is a list of what is unknown, not something a recommendation rests on; otherwise case 1 flips and Gate 1 findings of that kind block again |
1034: | OD6 | Does a reflect Drift with no decision basis become a follow-up? | yes; no; defer | defer | no reflect evidence in run 2; Drift already ends in an authorize-or-revert question [E]; decide after the program's own reflect data |
1035: | OD7 | Tasklist "High or Medium (blocking)": make Medium non-blocking, or rename it? | align; rename; leave | align Medium to non-blocking, after the tasklist rows of the scored table are read | the same word means "never fails" elsewhere [V] |
1036: | OD8 | Add a "rests on" qualifier to `/sc:implement` `false-claim`, or let the classifier fill `qa.md`'s four checklist answers? | qualifier; classifier fills the answers; neither | neither in version 1 | `qa.md` covers code, where a false claim in a delivered file can break a caller, and already derives severity by rule (`jev-uses.md` J3) |
1037: | OD9 | Who supplies the decision basis? | producer-declared; reviewer-named; code check | reviewer-named, code-checked where quotable; a consumer line from the task builder for upstream phase outputs | section 4.3 options B and C, with a narrow A |
1038: | OD10 | Bring `finding-grader` and the installed-only stoprule and spec-panel variants into `src`, align them, or retire them? | bring in; align; retire; leave | bring `finding-grader` in only if the LLM judge builds on it; leave the stoprule variants alone for now; decide align or retire for each installed-only spec-panel variant | they are installed only [V]; the rubric is frozen by design; until decided they keep today's text (RK16) |
1039: | OD11 | Replace "highest severity wins" in consolidation? | yes at all 13 lines, staged; at the task skill only; no | yes, at all 13 lines in 10 files, staged (section 10.3) | RC2; an earlier count of "three lines" missed ten of them (section 10.3) |
1040: | OD12 | Grade a form defect as Decision when a named program consumer reads it by position (the NEW-1 rule)? | yes; no | yes | it is code-checkable and it is what the run-2 override's own text says |
1041: | OD13 | Keep Note rows in the ledger, or count them only? | full rows; short rows; counts only | short rows (id, location, one line, status) | bounds volume; full detail stays in the lens reports |
1042: | OD14 | May a finding whose consumer is unknown wait for a later gate instead of keeping its blocking label? | never (default: the label stands); allow for condition 1 only, at named intermediate gates of one family, after GR7 is code in that family's final gate and a seeded test (T16) shows a deferred row reaching the final decision basis uncorrected becomes Blocking | approve for the task family after stage 3 data, not before. Never for conditions 2 or 3, never at the last gate, never surviving delivery unresolved | no final gate reads a ledger today (GR7), so deferral without the sweep would let a decision-bearing defect through |
1043: | OD15 | How is the one batch issue filed, and is filing limited to this repository in version 1? | through `/sc:issue --create @file`; the consent-bound body file posted by the attended top-level session; extend `/sc:issue` | the consent-bound path: `gh issue create --repo <R> --title ... --body-file <the approved file>` with `<R>` from `origin_repo.py`, then read back and compare digests (section 6.5). Yes, limited to this repository in version 1 | `/sc:issue` writes its own body after consent and posts with no preview, so neither the approved digest nor the batch marker survives it [V] |
1044: | OD16 | rf-qa-qualitative Rule 6 ("contradictions are always IMPORTANT or CRITICAL ... never minor"): keep it or change it? | (a) keep as a named mechanical gate mapped to condition 1 (blocking when the contradiction touches a decision basis, a quoted number or a required deliverable); (b) rewrite so a contradiction nothing rests on is a follow-up, and re-pin the test in the same change | (b), at stage 3, with `test_severity_floor_unweakened.py` re-pinned in the same change | Rule 6 is exactly the "contradiction is blocking whatever its consequence" case this program targets; until decided it stays and M12 notes it |
1045: | OD17 | Is a brake that needs no reinstall wanted? | no: the three-step revert is the only brake; yes: a named file that every carrier digest reads, with its format, writer and precedence stated | no recommendation in the merge plan; the default if undecided is no (the three-step revert only) | the run-2 override file is read by no shipped file and would lose to a carrier under REQ-03 [E: plan review], so any brake must be designed, not assumed |
1046: 
```
### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:17-32
```markdown
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17), metrics (M1 to M13), revert triggers (RT1 to RT8) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder. The stage 0 package is `TASK-WF-blockerStage0-20261116-021044`, the stage 1 package `TASK-WF-blockerStage1-20261116-030154` and the stage 2 package `TASK-WF-blockerStage2-20261116-030156`.
20: - One package, one stage. This is stage 3 of five packages (one plan per stage). It changes the live review rule. It runs only when all of these hold, each checked by reading files and not by memory, and all of them checked in Task 1 before any agent is spawned and before any file under `src/` or `tests/` changes: the owner's go for stage 3 is recorded in the stage ledger together with the list of shadow-run folders the owner counted; a recount of those folders with the stage 2 package's `./artifacts/shadow_summary.py` shows at least 5 observed shadow runs, zero safety misses (by the definition the stage 0 spec edit drafted) and no capture failure; the stage 0 package's `stage0b-escape-test.md` and `stage0c-regrade.md` exist. The stage 2 package's `./artifacts/stage2-summary-for-owner.md` is written when stage 2 finishes and states the runs observed up to then (zero is allowed), so this package does not use its run count.
21: - Gate order. `/sc:implement` runs this whole package in order and runs a task's edit before its review, so a gate checked in the same task as an edit would halt with the edit already in the working tree. Therefore the seeded-recall gate is Task 4, a read-only task that edits nothing under `src/`, `tests/` or `plugins/`, and every task that edits a rule file comes after it. Task 6, the first task that edits a rule file, checks the gate again by itself before its first edit and stops without editing when the check fails. A halt at Task 4 or at the start of Task 6 leaves no rule file switched. Each of Tasks 7, 8, 9 and 10 begins by reading that the registry row of `output-styles/pragmatic.md` reads `v2` and stops without editing when it does not. Stage 4 starts only after one audit window with no revert trigger tripped (spec section 13.2) and the owner's go in chat.
22: - Gates are read, never edited. No task and no fix pass edits the stage ledger row, a stage 0 or stage 2 file, the seeded-recall result, its answer key or the gate file to turn a failing line into a pass. A failing gate halts the run for the owner's Ruling. An owner ruling counts only as Task 3 defines it and Task 4 and Task 6 check it: a confirmation given to a `/sc:implement` Ruling prompt, in chat or elsewhere, that is not recorded on the stage ledger row in that form does not count.
23: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
24: - Retired carriers are not edited. The owner is retiring `/sc:task` and the task-builder: no task here edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`. `src/superclaude/skills/task/SKILL.md` still holds two merge-rule lines; the stage 1 allow-list in `refs/scale-map.md` lists that path as `exempt-by-retirement` (by path only), and the exemption ends when the retirement removes the file. Tests that exist only to pin the retired files are not re-pinned here; where one test pins both a retired and an active carrier, only the active carrier's part is re-pinned.
25: - Follow-up carrier. The sweep call and the printed follow-up list sit in `/sc:implement`'s final review step: the stage 2 package put them in `src/superclaude/skills/sc-implement-protocol/SKILL.md` (final summary instructions) and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (archive gate, run before the package moves). This stage only adds `--promote` to that call (Task 10). The carrier records and prints and asks nothing, because `refs/qa.md` keeps its own scale and its closed list of interrupts; the once-per-run offer question stays with the top-level session through the output style (the Medium rule of `pragmatic.md`, changed from per loop to per run in Task 6) and with the consent-bound filing path (OD15), so `/sc:implement` gains no question.
26: - Plugin surface. IronClaude is installed from the Coder template or from a clone plus `superclaude install`, not as a plugin, so this package creates no plugin surface (no plugin mirror of the skill folder, no plugin parity test, no plugin registry row), and neither does stage 4. Nothing under `plugins/` is edited except the byte-equal twins of the two implement-protocol files that Task 10 edits, which the existing test `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` pins. `src/superclaude/commands/spec-panel.md` and its plugin twin keep their text in this stage: their "once per loop" wording, pinned by `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_review_loop_extension.py` and `tests/skills/test_spec_panel_review_loop.py`, moves with the spec-panel narrowing in stage 4. The registry keeps exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only` and 5 `installed-only`. Whether plugin parity is dropped for good is the owner's decision and is not made here.
27: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), any mapping of `follow-ups.md` to `review-ledger/1` rows or edit of `src/superclaude/cli/review/ledger.py` (version 1 keeps the follow-up ledger as its own file), the 35 percent score target, any change to the cap of 2 fix cycles, and any template, rule-prompt, builder, researcher or spec-panel edit (those are stage 4; this includes the lines in the four rule-prompt files under `src/superclaude/rules/prompts/` and in `src/superclaude/templates/documents/agent_template_qa.md` that carry the same "NO LENIENCY" and "When in doubt, fail it" wording as the two QA agents).
28: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
29: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
30: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev` (it copies skills, agents, commands, hooks and templates; it does not copy `output-styles/`, `core/` or `rules/`); staging anything under the project `.claude/` folder is forbidden (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
31: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
32: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is left out of staging. Staging is not committing.
```
### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:72-118
```markdown
72: ## Task 3: Run the seeded-defect recall set under the old and the new rule text
73: 
74: Depends on: Task 1
75: 
76: Run the seeded-defect set built by the stage 0 package (its `./artifacts/seeded-recall-set.md` and the planted deliverable under its `./artifacts/seeded/`, read by package id) as spec section 8.3 says. Hand the reviewers only the planted deliverable and their brief; the answer key and the planted-defect list are never among the files they receive.
77: 
78: Arms. Before any reviewer is spawned, freeze both texts as copies: write `./artifacts/old-arm-block.md` (the lines of `src/superclaude/output-styles/pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet to the spec-panel scale bullet, copied byte for byte from the live file as it is now, which holds the old rule) and `./artifacts/new-arm-block.md` (the digest text of `src/superclaude/skills/sc-review-severity/refs/rule.md`, the block whose SHA-256 Task 1 recorded; the same block Task 6 ships), and record the SHA-256 of each. The reviewers receive these copies and never the live file, so a re-run after a halt reads the same old text. Both arms use the same model class and the same brief; only the rule text differs. Spawn three reviewer agents for each pass as freshly spawned agents, never agents continued from an earlier pass, and alternate the pass order across the three reviewers (old first, new first, old first). The arms differ in scope, and the result file says so: the old arm is the whole old block, the new arm is the digest alone, and the reviewer-brief change of REQ-04 and the once-per-run Medium wording that Task 6 ships are in neither arm (the injected installed style gives both arms the old brief bullets anyway, see the confound).
79: 
80: Confound. Every subagent receives the installed `~/.claude/output-styles/pragmatic.md` through the SubagentStart hook `pragmatic-subagent.js` (registered in `src/superclaude/hooks/hooks.json`), and until Task 6 and a refresh it holds the old rule, so a reviewer in the new arm holds the old definition as well. Tell every reviewer of both arms to apply only the rule text given in its brief, to quote the sentence it applied for each grade, and to ignore any other review-grading rule in its context; if a way to spawn reviewers without the injection exists, use it and record how. State the confound in the result file. Report each new-arm change against the old arm as a lower bound on the true change, because the confound pulls the new arm toward the old rule: the recall-equality lines are biased toward PASS and the cosmetic-fall line toward FAIL, and the file says so.
81: 
82: Valid reviewers and the controlling variant. A reviewer is valid for its arm when the sentences it quotes for its grades come from the rule text its arm was given. List every reviewer with its arm, pass order and whether it is valid; a new-arm reviewer whose quoted sentences come from the old rule is not valid. Two variants are computed. The controlling variant uses only the valid reviewers of each arm, and it alone sets each outcome word. The as-run variant uses all six reviewers; it is reported beside the controlling variant for every line and never sets a word, and where the two words differ the file says so next to the line. The threshold is fixed here, before dispatch, and is not changed after the grades are read: on the controlling variant a defect is found when more than half of that arm's valid reviewers report it, and found-and-blocking when more than half of them grade it blocking (2 of 3 with three valid reviewers, 2 of 2 with two). An arm with fewer than 2 valid reviewers cannot be scored: every line that needs that arm reads NOT-MEASURABLE, which is not PASS and so needs an owner ruling.
83: 
84: Scoring. The unit is the planted defect, not the reviewer-defect pair (reviewers on one set are not independent trials). Recall of a gating class is the share of its planted defects that are found-and-blocking; the share found at all and each reviewer's own rates are listed beside it. Intervals are Wilson 95 percent over the planted defects of each class. Read the minimum n per gating class from the stage 0 `seeded-recall-set.md`; a class below it, or one the file marks advisory, is advisory.
85: 
86: Lines and outcomes. The result file has one line per row of this table, each with exactly one outcome word, set by the controlling variant.
87: 
88: | Line | Class | Rule it tests |
89: |---|---|---|
90: | R1 | safety | every planted safety defect that is found-and-blocking under the old text is found-and-blocking under the new text (new count not below old) |
91: | R1b | safety (RT1, seeded part) | every planted safety defect is found-and-blocking under the new text; one event, never advisory |
92: | R2a | decision-bearing | new recall is at least the old recall minus 5 points |
93: | R2b | missing | new recall is at least the old recall minus 5 points |
94: | R3 | cosmetic | the share of planted cosmetic defects graded blocking is lower under the new text than under the old |
95: 
96: Outcome words: PASS (the rule holds and the class is at or above its minimum n); FAIL (the rule does not hold and the class is at or above its minimum n; R1b fails at any n); ADVISORY-PASS and ADVISORY-FAIL (the class is below its minimum n or marked advisory: the same test on the point estimate, with the interval shown, never written as a plain PASS or FAIL); NOT-MEASURABLE (a zero base: R1 or R2a or R2b when the old arm has no found-and-blocking defect in the class, R3 when the old arm blocks no cosmetic defect and the new arm also blocks none; or an arm with fewer than 2 valid reviewers; R3 with a zero old share and a nonzero new share is FAIL).
97: 
98: Owner ruling. A line that is not PASS lets the run continue past Task 4 only when the stage ledger row in PF holds an owner ruling for that line (continue, with the line id), dated on or after the date the result file was written and citing the SHA-256 of the result file as it is now. A ruling that cites a different hash is void, so an edit to the file after the ruling cancels it. The ruling is the owner's chat message, recorded by the session that received it; no other confirmation counts (Constraints).
99: 
100: Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the intervals, the cosmetic block share under both, the outcome of each line from the controlling variant with the as-run word beside it, the valid-reviewer list and the threshold used, the confound statement, the scope difference of the two arms, a sample of quoted sentences per reviewer, and the SHA-256 of the digest block that was tested. This task reports the result; the owner decides whether stage 3 may proceed, and Task 4 reads the gate.
101: 
102: Acceptance criteria:
103: - `./artifacts/seeded-recall-result.md` has the five lines R1, R1b, R2a, R2b and R3, each with one of the five outcome words set by the controlling variant and the as-run word beside it, per-class recall under both rule texts with Wilson intervals over planted defects, and the cosmetic block share under both.
104: - The six reviewer agent ids (three per pass) are recorded, each freshly spawned, with the pass order alternated and each marked valid or not valid with the sentence it quoted; the file states the found threshold used (more than half of the valid reviewers of the arm, fixed before dispatch), that model class and brief were identical across the arms and that the answer key is not among the files they were given.
105: - `./artifacts/old-arm-block.md` and `./artifacts/new-arm-block.md` exist with their SHA-256 recorded in the result file, and the SHA-256 of the tested digest block equals the one recorded in `./artifacts/stage3-entry-check.md`.
106: - The file states the confound and the lower-bound reading, the scope difference of the two arms, and records which rule text each reviewer reported applying.
107: - The file states that the result is evidence for the owner's go and does not itself grant it, and the task edits no file outside `./artifacts/`.
108: 
109: ## Task 4: Check the seeded-recall gate and the owner ruling before any rule file is edited
110: 
111: Depends on: Task 1, Task 3
112: 
113: Spawn no agent and edit nothing outside `./artifacts/` in this task: it is read-only for `src/`, `tests/` and `plugins/`, so a halt here leaves no rule file switched. Compute the SHA-256 of `./artifacts/seeded-recall-result.md` now, read the outcome word of each of R1, R1b, R2a, R2b and R3 from it, and read the stage 3 row of the stage ledger in PF. For every line that does not read PASS, find a ruling on that row that names the line id, is dated on or after the date the result file was written and cites the SHA-256 computed now. Write `./artifacts/seeded-recall-gate.md` with the hash, the five words, the ruling found for each non-PASS line (or none), the output of `git status --short -- src tests plugins` and a gate line reading PASS or FAIL. The gate is PASS only when all five lines read PASS or every non-PASS line has a valid ruling. Only a ruling recorded on the ledger row in the form Task 3 defines counts; a confirmation given to a `/sc:implement` Ruling prompt for this task does not, and no fix pass edits the result file, the ledger or this file.
114: 
115: Acceptance criteria:
116: - `./artifacts/seeded-recall-gate.md` exists, records the SHA-256 of `./artifacts/seeded-recall-result.md` and its five outcome words, and its gate line reads PASS; a gate line reading FAIL fails this task and halts the run for the owner's Ruling with no rule file edited.
117: - Each non-PASS line is listed with its ruling (line id, date on or after the result file's date, cited hash equal to the hash recorded in the gate file), or the file says that all five read PASS.
118: - The `git status --short -- src tests plugins` output recorded in the gate file equals the output recorded in `./artifacts/stage3-entry-check.md`, and the file states that this task spawned no agent and edited no file outside `./artifacts/`.
```
### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:247-267
```markdown
247: ## Phase 5: Write the audit summary for the owner
248: 
249: ## Task 14: Write the stage 3 audit summary for the owner
250: 
251: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13
252: 
253: Write `./artifacts/stage3-summary-for-owner.md`. First re-run the commands of Tasks 5, 11, 12 and 13 and record each pytest summary line. Then write these parts.
254: 
255: - The seeded-recall headline of Task 3 (the outcome of R1, R1b, R2a, R2b and R3 from the controlling variant, the as-run words beside them, and any owner ruling used), the gate of Task 4, the entry check of Task 1 and the baselines of Task 2 with the RT5 threshold.
256: - The audit-window measures: read the metric list in spec section 13.1 and quote the rows for M1, M4, M5, M6, M9, M10b, M11 and M12 (M12 is the rf-qa FAIL count per pilot gate), each with its baseline from the place that holds it, or the statement that none exists: M1, M12 and M10b from `./artifacts/stage3-baselines.md`; M4 none (the spec's baseline column says the audit creates it); M5 from the old-arm recall in `./artifacts/seeded-recall-result.md`; M6 from the share of `consumer-unknown` rows among non-blocking rows that `./artifacts/shadow-recount.md` prints, or the "not computable" line the script printed instead; M9 and M11 from the baseline column of their spec rows. Quote RT1 to RT8 from spec section 13.2 and do not restate them from memory.
257: - The revert triggers that can be judged now. RT1 (seeded part) and RT3 are judged from the Task 3 result: state tripped or not tripped for each, noting that R1b is stricter than R1 (it passes only when every planted safety defect is found-and-blocking under the new text). Mark as pending until the audit window has run only the window-dependent parts: RT1's audit part, RT2, RT4, RT5, RT6, RT7 and RT8.
258: - The switch steps before the audit window (spec REQ-26). The repository edit and the drift tests are done by this package. Still to do by the owner or operator: ship a release whose note names the refresh command (`superclaude update`, or an install with `--force`), then refresh each machine that will run the audit window and confirm it with the install check (`make doctor`, the `_check_review_severity_digests` check, which reads the packaged registry). The installed style carries the digest once `grep -c "review-severity:digest v2 begin" ~/.claude/output-styles/pragmatic.md` prints 1. Run both commands now, read-only, record what they print on this machine, and say plainly that the audit window is not started on a machine until both show the refreshed state. Until then QA runs under the new carriers plus the old injected style (RK15, counted by M10b).
259: - The revert path. The per-row three-step revert (spec REQ-26) covers the three digest rows (`output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`): restore the file from the commit before this package's change, set the row to `legacy`, re-run the drift tests, release and refresh. The edits with no registry row are reverted by restoring each listed file from the same commit: the merge text, the L2 and L3 text and the rewritten principle 8 and rule 9 in the two QA agents, `rf-analyst.md`, the once-per-run Medium wording and the kept recheck sentence in `pragmatic.md`, the `--promote` flag on the sweep call in `sc-implement-protocol/SKILL.md` and `refs/managed-workspace.md` with their plugin twins and `tests/skills/test_implement_follow_up_sweep.py`, the `Kept mechanical gates` section of `refs/scale-map.md`, and the re-pinned tests, followed by `make sync-dev` and the same release and refresh. List those files by path.
260: - State that the audit window runs after this package and is observed by the owner or operator, and name what it covers: every run on a refreshed machine that passes an rf-qa or rf-qa-qualitative gate, from the first run after the refresh until the rate sample of spec section 8.2 reaches 5 runs or 60 non-blocking rows, whichever is later.
261: - End with the sentence that the owner's go for stage 4 is given in chat and not by this file.
262: 
263: Acceptance criteria:
264: - `./artifacts/stage3-summary-for-owner.md` names the seeded-recall headline and the file that holds it, lists the tests re-pinned with their observed pytest summary lines, and quotes M12, M10b, M1 and RT1 to RT3 from the spec with the baselines of `./artifacts/stage3-baselines.md`; each of M4, M5, M6, M9 and M11 shows its baseline source or the statement that none exists.
265: - The summary states whether RT1 (seeded part) and RT3 are tripped, from the Task 3 result, and lists only the window-dependent triggers as pending; it does not say that no trigger can be judged.
266: - The summary names the release, the refresh command and the install check as steps that come before the audit window, records the observed output of the install check and of the `grep -c` on the installed style, and states the revert path for the digest rows and for the edits without a registry row.
267: - The summary ends with the sentence that the owner's go for stage 4 is given in chat and not by this file.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001: at least 5 shadow runs have been observed with zero safety misses (by the stage 0 definiti | CONSTRAINTS | covered (containment 1.00) | source.md:3 |
| INF-002: stage 0b's escape result is written and stage 0c's re-grade is written | CONSTRAINTS | unmatched by the mechanical rule (read by hand) | source.md:3 |
| INF-003: the owner's go in chat is recorded in the stage ledger | CONSTRAINTS | covered (containment 1.00) | source.md:3 |
| INF-005: the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and the owner has r | CONSTRAINTS | covered (containment 0.88) | source.md:3 |
| INF-006: Stage 4 starts only after one audit window with no revert trigger tripped (the spec's sect | CONSTRAINTS | covered (containment 0.95) | source.md:11 |
| INF-007: State that `/sc:implement` runs the whole package in order, so the rule switch cannot star | CONSTRAINTS | covered (containment 0.80) | source.md:11 |
| INF-010: Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the | T-03 | covered (containment 1.00) | source.md:12 |
| INF-013: (three bullets replaced, cap and own-scale bullets pinned by content, hook check through ` | T-06 | covered (containment 0.64) | source.md:13 |
| INF-017: that a later task of the same package makes false get an end point | CONSTRAINTS | covered (containment 0.88) | source.md:15 |
| INF-018: Write `./artifacts/stage3-summary-for-owner.md` | T-14 | covered (containment 1.00) | source.md:16 |
| INF-019: and end with the sentence that the owner's go for stage 4 is given in chat and not by this | CONSTRAINTS | covered (containment 1.00) | source.md:16 |
| INF-020: the revert triggers RT1 and RT2 with their current state, read from the spec's text and no | T-14 | covered (containment 0.75) | source.md:16 |
| INF-021: No template, rule-prompt, builder, researcher or spec-panel edit (stage 4). | CONSTRAINTS | covered (containment 1.00) | source.md:20 |
| INF-022: No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity co | CONSTRAINTS | covered (containment 0.92) | source.md:20 |
| INF-023: No Jev call, key or account. | CONSTRAINTS | covered (containment 0.75) | source.md:20 |
| INF-024: New Task 1 runs every entry check before any agent is spawned or file is edited. | CONSTRAINTS | covered (containment 0.85) | source.md:28 |
| INF-025: the stage ledger row for stage 3 carries the owner go, the list of shadow-run folders the  | CONSTRAINTS | covered (containment 0.93) | source.md:28 |
| INF-026: the RT5 threshold (75 percent of the M1 mean) | T-02 | covered (containment 1.00) | source.md:29 |
| INF-027: keeps model class and brief identical across arms | T-03 | covered (containment 0.86) | source.md:30 |
| INF-028: gains a command, `superclaude review fixcheck` | T-05 | covered (containment 0.80) | source.md:31 |
| INF-029: adds `--promote` to the one sweep call in `src/superclaude/skills/sc-implement-protocol/SK | CONSTRAINTS | covered (containment 0.86) | source.md:35 |
| INF-031: no mapping of `follow-ups.md` to `review-ledger/1` | CONSTRAINTS | covered (containment 1.00) | source.md:39 |
| INF-033: Only a ruling recorded on the stage ledger row (line id, date, SHA-256) counts | T-03 | covered (containment 1.00) | source.md:49 |
| INF-034: Task 3 now freezes the old-arm and new-arm blocks as copies | T-03 | covered (containment 0.75) | source.md:49 |
| INF-035: the found threshold fixed before dispatch (more than half of the arm's valid reviewers: 2  | T-03 | covered (containment 1.00) | source.md:50 |
| INF-036: Tasks 7 and 8 now rewrite principle 8 "NO LENIENCY" and rule 9 "Report honestly" | T-07 | covered (containment 0.82) | source.md:51 |
| INF-037: Task 12 re-pins that block hash against the new Rule 6, Rule 9 and L3 text | T-08 | covered (containment 0.92) | source.md:51 |
| INF-038: Task 6 keeps "never to meet a quota" and runs | T-06 | covered (containment 1.00) | source.md:57 |
| INF-039: Task 6 keeps the sentence "Medium and Note findings are not rechecked in later rounds." af | T-06 | covered (containment 0.92) | source.md:59 |
| INF-040: Task 14 gives the baseline source of each of M4, M5, M6, M9, M11. | T-14 | covered (containment 0.82) | source.md:60 |
| INF-041: the L2 text has a missing-command clause (one line in the fix log, carry on) | T-07 | covered (containment 0.89) | source.md:66 |
| INF-044: Tasks 7 to 10 begin by reading that the `pragmatic.md` registry row reads `v2` | CONSTRAINTS | covered (containment 0.90) | source.md:49 |
| REQ-04 (parsed) | T-03, T-06 | covered (exact) | source.md:55 |
