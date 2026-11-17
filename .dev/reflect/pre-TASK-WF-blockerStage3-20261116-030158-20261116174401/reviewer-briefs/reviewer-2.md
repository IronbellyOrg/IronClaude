# Reviewer brief 2 (persona: qa; model class: opus)

## T1 card excerpt

### Coverage, acceptance and requirement observations

O2. The two arms of Task 3 do not hold the same scope. PLAN:76 old arm = the lines of `pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet (line 221) to the spec-panel scale bullet (line 231), about ten bullets: reviewer brief, zero-finding rule, conflict rule, binary verdict, the five definition bullets, Medium and spec-panel. New arm = "the digest section of refs/rule.md" only (the REQ-01 block, SPEC:195-207). PLAN:76 says "only the rule text differs", but the new arm lacks the reviewer-brief, zero-finding and binary-verdict bullets the old arm has, and Task 5 ships a REQ-04 reviewer-brief change (PLAN:125) and the Medium cadence change that no arm tests.

O4. A fixed grading line outside the freeze patterns stays in both QA agents. src/superclaude/agents/rf-qa.md:100 reads "an unverified or 'probably fine' claim is blocking" (rule 8, NO LENIENCY) and src/superclaude/agents/rf-qa-qualitative.md:99 carries the same sentence. S0:34 freezes the REQ-30 patterns plus "Any CRITICAL or IMPORTANT issue exists"; "it FAILS" and "is blocking" in rule 8 match none. Tasks 6 and 7 edit S1, S2, S5 (about line 108), the merge rule, the fixed FAIL triggers of the freeze and (Task 7) Rule 6, so rule 8 would stand beside a digest that makes an unverified claim blocking only under a named condition (an unverified safety claim stays open, SPEC:199).

O5. A pinned sentence sits inside the bullet Task 5 rewrites. pragmatic.md:221 holds "never to meet a quota"; tests/skills/test_review_prompt_overrides.py:244 asserts it in the flattened style file. PLAN:125 asks only that reviewers "hunt for defects and name their consequence instead of hunting for false claims" and PLAN:195 requires that test to pass unchanged, but Task 5 neither names the sentence nor runs that test (PLAN:134).

O8. Task 1 compares the digest section of `refs/rule.md` with "the REQ-01 block of the spec ... once whitespace is collapsed" (PLAN:43); the spec block is a blockquote with `> ` markers and bold (SPEC:195-207). The comparison rule (strip quote markers) is implied, not stated. S1:49 says the digest is that block word for word, so the check can pass.

### Fixes of the first review that the Tier 1 pass found to hold

F1 (entry checks before any spawn or edit): Task 1 reads files only, writes `./artifacts/stage3-entry-check.md`, recounts with `shadow_summary.py --confirmed-misses` (S2:138 builds that script with that option and the "not computable" line), and checks the stage 0, 1 and 2 files by the names those plans create (S0:37 inventory freeze, S0:44 escape test, S0:69 regrade, S0:106 seeded set, S1:49 rule.md, S1:66 scale-map, S1:223 registry test, S2:41 sweep.py, S2:56 follow_ups_cmd.py, S2:113 and S2:79). F2: PLAN:78 states the hook confound (hooks.json:173 runs pragmatic-subagent.js; the installed style holds the old rule), identical model class and brief, and the lower-bound reading. F3: PLAN:82-94 define the five lines, the outcome words and the owner ruling that must cite the file's SHA-256. F4: Task 13 (PLAN:232) names release, refresh and install check; Makefile `sync-dev` copies skills, agents, commands, hooks and templates and has no step for output-styles (Makefile:109-157; SPEC:885). F5: the registry test sits in Tasks 5, 6, 7 and 10 and each of those tasks checks the row reads `v2`; Task 1 and Task 3 compare one digest SHA-256. F6: PLAN:231 judges RT1 (seeded part) and RT3 now. F7: Task 2 counts M1, M12, M10b baselines and the RT5 threshold.

Live-line checks that hold: pragmatic.md:225, :226, :229 are the three definition bullets; rf-qa.md:83 and rf-qa-qualitative.md:84 and rf-analyst.md:75 carry the merge rule; rf-qa.md:152, :162, :168-170, :182-183, :327, :389, :402, :476, :549 and rf-qa-qualitative.md:240, :291, :362, :429, :500, :567, :746, :784, :809, :990, :994 match PLAN:140 and PLAN:154; skills/task/SKILL.md:252 and :361 are the only retired hits; tests/skills/test_review_severity_rule.py holds `test_ej_fixtures_are_byte_copies_of_the_plan_tables` (:275) and `test_h_implement_protocol_plugin_twins_byte_equal` (:371); the twins are equal today; src/superclaude/cli/review/__init__.py lists nine names (panel_cmd, merge_cmd, ledger_cmd, telemetry_cmd, lint_cmd, estimate_cmd, cluster_cmd, verify_cmd, manifest_cmd; lint_cmd and estimate_cmd have no module), so the seven subcommands Task 4 expects to see in `--help` exist.

### Recommendations

R1. Task 5 body: read the seeded-recall result and the ruling before the first edit (O1). R2. Task 3: one sentence stating what the new arm holds besides the digest, and which variant decides each outcome word (O2, O3). R3. Tasks 6 and 7: add rule 8 "an unverified or probably fine claim is blocking" to the rewrite list (O4). R4. Task 5: name "never to meet a quota" as kept and run `test_review_prompt_overrides.py` (O5). R5. Task 13: M6 baseline source (O6).

Context: the plan under review is stage 3 of five (one plan per stage) of the blocker-classification work (GitHub issue #552). It changes the live review rule (the pilot): `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, the follow-up sweep call of `/sc:implement`, and the tests that pin them. It was revised in place on 2026-11-16 after a first review whose merged card (7 blocking findings F1 to F7, 8 non-blocking F8 to F15) is at `.dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116030420/adversarial/merged-review-card.md`. This is the re-review. Repository root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (every repo-relative path below is relative to it; read the files as <root>/<path>). Short names: PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md`; SRC = `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md` (the stage request, the driving file); SPEC = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (the merged spec the plan is written against); README = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md` (stage ledger); S0, S1, S2 = the stage 0, 1 and 2 plan files under `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/`, `...Stage1-20261116-030154/`, `...Stage2-20261116-030156/` (same file names as the folder id plus `.md`). The stage 0, 1 and 2 packages are plans that have not run: a file they will create (for example `src/superclaude/skills/sc-review-severity/refs/rule.md`) does not exist yet and that is expected; check that the producing plan creates it under that name and that PLAN reads it by that name.

What you must check: (a) that each first-review blocking finding the plan says it fixed is really fixed in the live plan: the entry checks before any spawn or edit (Task 1), the old-rule confound of the seeded-recall passes through the SubagentStart hook (Task 3), the gate outcomes (Task 3 outcome words, Task 5 gate), the release, refresh and install steps (Task 13), the registry drift check (Tasks 5, 6, 7, 10), the revert-trigger wording (Task 13) and the baselines (Task 2, Task 13); (b) that the revision introduced no new defect: task numbering and `Depends on` edges, acceptance lines that a later task of this package makes false without an end point ("until Task N"), paths that do not exist, and contradictions with the decisions of `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/revision2-brief.md` (retired task skill and task-builder are not edited; no plugin surface; `/sc:implement` final-step carrier edits without touching `refs/qa.md`); (c) the plan against SPEC (rollout stage 3 row, section 4.1 to 4.4, 8.3, 9.4, 10.1 to 10.5, 11.1, 13). Also check each plan claim about a live file or a live test (line numbers, sentences, test names, command names) by reading the file.

How to grade: grade each finding blocking or minor by consequence. Blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format. A finding whose consequence is a wrong measurement that gates the rule switch, or a live-rule edit that contradicts the rule it ships, is blocking. Do not invent findings and do not work to a quota; a review with no finding must say what you checked and why you found no defect.

How to work: you have Read, Grep, Glob and code-search tools only; you run nothing. Audit the hunks below and re-Read the files you cite; every `file:line` you cite is re-read by an independent validator and dropped if it does not match, so quote exactly and cite the line where the text sits (re-read the line, do not cite from memory). Read the whole PLAN first (241 lines). Tell the orchestrator about any file you could not read. Do not rely on the observations above: they come from one agent and may be wrong; verify or reject each one yourself.

How to answer: return your card as your final message, plain markdown, at most about 7,000 characters, with these sections only: `## First-review findings` (one line each for F1 to F7 of the first review: fixed, partly fixed or not fixed, with the `file:line` that shows it), `## Findings` (numbered F1, F2, ...; each with `Blocking: yes` or `Blocking: no`, a one-line title, evidence as `file:line` plus a short verbatim quote, the consequence in one or two sentences, and a one-line fix), `## Checked and sound` (what you verified and found fine), `## Self-report` (one line `confidence: 0.NN`). Write plain English; no em dashes.

Persona instructions (qa): audit the coverage matrix AGAINST the spec body in your grounding hunks (SRC whole, SPEC sections); surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check the plan against SPEC section by section: the rollout stage 3 row (SPEC:947), L1 to L6 (SPEC:270 to 275), REQ-04 and REQ-26 and REQ-27, section 8.3 (the seeded set and the old and new text), section 10.1 and 10.4 and 10.5 (which lines change), section 11.1 (which tests are re-pinned and how), section 13.1 and 13.2 (metrics M1 to M13 and triggers RT1 to RT8: check that every metric, baseline source and trigger PLAN quotes or computes matches the spec text). For each acceptance criterion of Tasks 1 to 13, ask whether a check as written can be run and can pass, and whether it can pass vacuously or fail for a reason unrelated to the task. Read the live tests the plan re-pins (`tests/skills/test_review_severity_rule.py`, `test_review_severity_mapping.py`, `test_implement_severity_static.py`, `test_review_prompt_overrides.py`, `tests/audit/test_nfr_conv_9_zero_trust.py`, `tests/audit/test_severity_floor_unweakened.py`, `tests/audit/test_invariant_preservation_NFR_6_through_10.py`) and the live files the plan edits (`src/superclaude/output-styles/pragmatic.md`, `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/agents/rf-analyst.md`) and say whether the plan's description of them is right and whether the plan's edit list covers every line that would contradict the new digest.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T17:44:11Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md:1-41
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
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:187-214
```markdown
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

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:268-275
```markdown
268: | # | Change | Cause it answers | Where |
269: |---|---|---|---|
270: | L1 | **[REQ-05]** The consolidator grades by the rule and keeps every reviewer's own grade visible. Label-max merging ("highest severity wins") is replaced at all 13 lines in 10 files that state it, in two stages. A blocking grade that names a consumer the code check does not disprove stands. A blocking grade that names no consumer goes back to the reviewer once (GR2). If it still names none, the reviewer's label stands, the row is tagged `consumer-unknown` with a `reasked` flag and listed first; it is never demoted for missing grounding. | RC2 | the 13 lines of section 10.3; the reverse-scan test T5 pins the removal |
271: | L2 | A fix pass runs every mechanical check that exists over the lines it edited before it hands back: table pipe count, byte-present quotes, recomputed counts, link existence. The results go into the fix log. A defect a verifier finds that the fix introduced carries `origin: fix-induced` and is graded by the same rule. | RC3 | `rf-qa.md` Fix Cycle section; `task/SKILL.md:254` |
272: | L3 | The cap and the regression and monotonicity halts count Blocking findings only (they already count "blocking", so this follows from the definition). At the cap the escalation offers three choices: fix by hand, accept and file (the finding becomes a follow-up tagged `accepted-blocker`), or stop. The cap stays at 2 fix cycles. | RC1 | `rf-qa.md:402-415` [E]; `task/SKILL.md:258` [V], `372` [E] |
273: | L4 | The task builder writes a consumer line for each phase output. | RC4 | `task-builder` and the MDTM templates 01 and 02 [E] |
274: | L5 | Medium and Note findings are never rechecked. A fix that touches a Medium row's location does not reopen it. The final-gate sweep (GR7) and a linked escalation (section 6.2) are the only ways a recorded row becomes blocking. | RC1 | same text as today (`pragmatic.md:226`) [V] |
275: | L6 | **[REQ-06]** The fixed FAIL triggers in the QA agents (lines that fail a review by label or by a fixed rule, ignoring the "a decision depends" test) are each either rewritten to "grade by the three conditions; the label is information", or kept as a named mechanical gate mapped to condition 2 (Missing) when a template requires the item, with the keep recorded in the scale map. "Flag exact duplicates as IMPORTANT" becomes Note unless a condition holds. Rule 6 of rf-qa-qualitative ("contradictions are always IMPORTANT or CRITICAL ... never minor") is decided by owner decision OD16. The pinning tests change in the same step. | RC1, RC6 | section 10.4 (a frozen Grep at stage 0, not a remembered list) |
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:676-680
```markdown
676: ### 8.3 Seeded-defect recall
677: 
678: <!-- Source: Base (original) -->
679: 
680: Plant known defects in a held-out deliverable, across four classes: decision-bearing false claim, missing required section, safety risk, and cosmetic. Review it under the old rule and the new rule with the same reviewers. Required: safety recall equals the old rule's; recall of decision-bearing and missing items stays within 5 points of the old rule's; the share of cosmetic items that block falls. A candidate existing set is the 44-defect spec ledger (20 blocking, 19 medium, 5 minor), validated by 20 agents, named in a run-2 scope file [E: seen as text at `R2/research/scope/06-brainstorm-process-redesign.md:242`; the artifact itself is [U]]. That file also says the whole #346 series was tuned on it, so use it as a sanity check and plant fresh defects for the real test.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:752-764
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
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:799-815
```markdown
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
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:828-871
```markdown
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
871: | Routing doc | `core/HOW-WE-WORK.md` 65 [E] | the level text names the cap; check wording |
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:893-910
```markdown
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
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:936-948
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
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:958-992
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
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:70-103
```markdown
70: ## Task 3: Run the seeded-defect recall set under the old and the new rule text
71: 
72: Depends on: Task 1
73: 
74: Run the seeded-defect set built by the stage 0 package (its `./artifacts/seeded-recall-set.md` and the planted deliverable under its `./artifacts/seeded/`, read by package id) as spec section 8.3 says. Hand the reviewers only the planted deliverable and their brief; the answer key and the planted-defect list are never among the files they receive.
75: 
76: Arms. The old arm holds today's rule text (the lines of `src/superclaude/output-styles/pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet to the spec-panel scale bullet, read at run time). The new arm holds the digest section of `src/superclaude/skills/sc-review-severity/refs/rule.md` (the block whose SHA-256 Task 1 recorded; the same block Task 5 ships). Both arms use the same model class and the same brief; only the rule text differs. Spawn three reviewer agents for each pass as freshly spawned agents, never agents continued from an earlier pass, and alternate the pass order across the three reviewers (old first, new first, old first).
77: 
78: Confound. Every subagent receives the installed `~/.claude/output-styles/pragmatic.md` through the SubagentStart hook `pragmatic-subagent.js` (registered in `src/superclaude/hooks/hooks.json`), and until Task 5 and a refresh it holds the old rule, so a reviewer in the new arm holds the old definition as well. Tell every reviewer of both arms to apply only the rule text given in its brief, to quote the sentence it applied for each grade, and to ignore any other review-grading rule in its context; if a way to spawn reviewers without the injection exists, use it and record how. State the confound in the result file. Report each new-arm change against the old arm as a lower bound on the true change, because the confound pulls the new arm toward the old rule: the recall-equality lines are biased toward PASS and the cosmetic-fall line toward FAIL, and the file says so. List every new-arm reviewer whose quoted sentences come from the old rule and report the recall lines both with and without that reviewer's grades.
79: 
80: Scoring. The unit is the planted defect, not the reviewer-defect pair (three reviewers on one set are not independent trials). A defect is found when at least 2 of the 3 reviewers report it, and found-and-blocking when at least 2 of the 3 grade it blocking. Recall of a gating class is the share of its planted defects that are found-and-blocking; the share found at all and each reviewer's own rates are listed beside it. Intervals are Wilson 95 percent over the planted defects of each class. Read the minimum n per gating class from the stage 0 `seeded-recall-set.md`; a class below it, or one the file marks advisory, is advisory.
81: 
82: Lines and outcomes. The result file has one line per row of this table, each with exactly one outcome word.
83: 
84: | Line | Class | Rule it tests |
85: |---|---|---|
86: | R1 | safety | every planted safety defect that is found-and-blocking under the old text is found-and-blocking under the new text (new count not below old) |
87: | R1b | safety (RT1, seeded part) | every planted safety defect is found-and-blocking under the new text; one event, never advisory |
88: | R2a | decision-bearing | new recall is at least the old recall minus 5 points |
89: | R2b | missing | new recall is at least the old recall minus 5 points |
90: | R3 | cosmetic | the share of planted cosmetic defects graded blocking is lower under the new text than under the old |
91: 
92: Outcome words: PASS (the rule holds and the class is at or above its minimum n); FAIL (the rule does not hold and the class is at or above its minimum n; R1b fails at any n); ADVISORY-PASS and ADVISORY-FAIL (the class is below its minimum n or marked advisory: the same test on the point estimate, with the interval shown, never written as a plain PASS or FAIL); NOT-MEASURABLE (a zero base: R1 or R2a or R2b when the old arm has no found-and-blocking defect in the class, R3 when the old arm blocks no cosmetic defect and the new arm also blocks none; R3 with a zero old share and a nonzero new share is FAIL).
93: 
94: Owner ruling. A line that is not PASS lets Task 5 proceed only when the stage ledger row in PF holds an owner ruling for that line (continue, with the line id), dated on or after the date the result file was written and citing the SHA-256 of the result file as it is now. A ruling that cites a different hash is void, so an edit to the file after the ruling cancels it. The ruling is the owner's chat message, recorded by the session that received it.
95: 
96: Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the intervals, the cosmetic block share under both, the outcome of each line, the confound statement, a sample of quoted sentences per reviewer, and the SHA-256 of the digest block that was tested. This task reports the result; the owner decides whether stage 3 may proceed.
97: 
98: Acceptance criteria:
99: - `./artifacts/seeded-recall-result.md` has the five lines R1, R1b, R2a, R2b and R3, each with one of the five outcome words, per-class recall under both rule texts with Wilson intervals over planted defects, and the cosmetic block share under both.
100: - The six reviewer agent ids (three per pass) are recorded, each freshly spawned, with the pass order alternated; the file states that model class and brief were identical across the arms and that the answer key is not among the files they were given.
101: - The file states the confound and the lower-bound reading, and records which rule text each reviewer reported applying.
102: - The SHA-256 of the tested digest block equals the one recorded in `./artifacts/stage3-entry-check.md`.
103: - The file states that the result is evidence for the owner's go and does not itself grant it, and the task edits no file outside `./artifacts/`.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:136-161
```markdown
136: ## Task 6: Move rf-qa.md to digest v2 and rewrite its fixed FAIL triggers
137: 
138: Depends on: Task 4, Task 5
139: 
140: Edit `src/superclaude/agents/rf-qa.md`: replace S1, S2 and S5 (the definition bullet and the bullets beside it, today around line 108) with the digest and pointer; replace the merge rule ("take the more severe rating for shared items", today line 83) with the L1 text (the consolidator grades by the rule, keeps every reviewer's grade visible, and sends a blocking grade that names no consumer back once); add the L2 pre-handback step to the Fix Cycle section (before handing back, the fix agent runs `superclaude review fixcheck` over the lines it edited and writes every result, passes included, into the fix log; a defect a verifier finds on those lines carries `origin: fix-induced` and is graded by the same rule); at each of its two cap sentences ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", today in the Fix Cycle bullet near line 402 and in numbered rule 10 "Maximum 2 fix cycles" near line 549) add the L3 three choices (fix by hand, accept and file as an `accepted-blocker` follow-up, or stop) and one sentence that the halt message carries the top-level session's once-per-run offer, which this agent does not make, so a halt shows one offer; and for each fixed FAIL trigger listed in the stage 0 package's `./artifacts/stage0-inventory-freeze.md` (read by package id) for this file (spec section 10.4: "Any incomplete file = FAIL", "Any untagged doc claim = FAIL", the "Will this gap reduce report quality? -> IMPORTANT" and "Any CRITICAL or IMPORTANT gap = overall FAIL" bullets, the PASS and FAIL bullets by label near lines 182 to 183, "Flag exact duplicates as IMPORTANT", and the count-CRITICAL-and-IMPORTANT-as-blocking lines) either rewrite it to "grade by the three conditions; the label is information" or keep it as a named mechanical gate mapped to condition 2 (Missing) and record the keep, with its reason, in `refs/scale-map.md`; "Flag exact duplicates as IMPORTANT" becomes Note unless a condition holds. Set the registry row of `agents/rf-qa.md` to `v2`. Run `make sync-dev` afterwards.
141: 
142: Acceptance criteria:
143: - `grep -n "more severe rating" src/superclaude/agents/rf-qa.md` prints nothing.
144: - Every FAIL-trigger line in the stage 0 frozen inventory for `rf-qa.md` is either changed or listed as a kept mechanical gate in `refs/scale-map.md` with a reason.
145: - The PASS and FAIL bullets are reworded to "any blocking gap", and the file holds exactly one digest and its registry row reads `v2` (`grep -n -A6 "agents/rf-qa.md" src/superclaude/skills/sc-review-severity/refs/registry.yaml` shows state `v2`).
146: - The L2 step naming `superclaude review fixcheck` is present in the Fix Cycle section, and the L3 three choices with the one-offer sentence sit beside each of the two places the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" appears (`grep -c` of that sentence still prints 2).
147: - `grep -c "Retry Monotonicity Protocol" src/superclaude/agents/rf-qa.md` and `grep -c "INV-012" src/superclaude/agents/rf-qa.md` each print 1 or more (`tests/skills/test_task_builder_merge.py` pins those tokens).
148: - `uv run pytest tests/skills/test_review_severity_registry.py -v` passes.
149: 
150: ## Task 7: Move rf-qa-qualitative.md to digest v2, rewrite its eight FAIL-by-label pairs and apply OD16
151: 
152: Depends on: Task 4, Task 5
153: 
154: Edit `src/superclaude/agents/rf-qa-qualitative.md`: replace S1, S2 and S5 (today around line 108) with the digest and pointer; replace the merge rule (today line 84) with the L1 text; add the L2 pre-handback step to its fix-cycle text and the L3 three choices with the one-offer sentence beside each cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" (today at lines 809 and 994; line 994 is rule 10 inside the `## Critical Rules` block whose hash Task 11 re-pins; the cap sentence itself stays word for word); rewrite or keep as named mechanical gates, recorded in `refs/scale-map.md`, the eight verdict pairs that fail a review on "Any CRITICAL or IMPORTANT issue exists" (the FAIL bullet today at lines 240, 291, 362, 429, 500, 567, 746 and 784, each with its PASS bullet one line above; the list is in the stage 0 package's `./artifacts/stage0-inventory-freeze.md`, read by package id); and rewrite Rule 6 ("Contradictions are always IMPORTANT or CRITICAL ... that's never minor", today line 990) per OD16 option (b), so a contradiction nothing rests on is a follow-up, and keep contradictions that touch a decision basis, a quoted number or a required deliverable as Blocking under condition 1. Set the registry row of `agents/rf-qa-qualitative.md` to `v2`. Run `make sync-dev` afterwards.
155: 
156: Acceptance criteria:
157: - `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/agents/rf-qa-qualitative.md` prints 0, or each remaining line is listed in `refs/scale-map.md` with its reason.
158: - `grep -n "that's never minor" src/superclaude/agents/rf-qa-qualitative.md` prints nothing, and the new Rule 6 text names the decision-basis exception.
159: - The file holds exactly one digest, no `more severe rating` text, and its registry row reads `v2` (`grep -n -A6 "agents/rf-qa-qualitative.md" src/superclaude/skills/sc-review-severity/refs/registry.yaml` shows state `v2`).
160: - The cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still prints a `grep -c` of 2, each with the three choices and the one-offer sentence, and the L2 step naming `superclaude review fixcheck` is present.
161: - `uv run pytest tests/skills/test_review_severity_registry.py -v` passes. `tests/audit/test_severity_floor_unweakened.py` is red from this task until Task 11 re-pins the `## Critical Rules` block hash in the same change set.
```


### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:192-220
```markdown
192: Update `tests/skills/test_review_severity_rule.py` (`canonical_rule_bullets()` reads the digest from `refs/rule.md`; `S1_S3_FILES` and its `[:6]` slice `S5_FILES` become registry rows of kind `digest`, dispatched by registry state: rows at `v2` (`pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`) are checked against the digest, and rows still at `legacy` (the eight template and rule-prompt files, until stage 4) stay pinned to a frozen copy of the old three bullets held as literal constants in the test; the cap-text and banned-phrase checks stay, and `CANONICAL_CAP_TEXT` stays asserted against the output style only, as today), `tests/skills/test_review_severity_mapping.py` (the pragmatic Medium pin moves from "once per loop" to the once-per-run wording and its position check reads the Medium bullet after the digest and pointer instead of after the old S5 bullet, with new assertions on `refs/rule.md` and `refs/scale-map.md`; the spec-panel pins on "once per loop" stay unchanged because the spec-panel carrier is not edited in this stage), `tests/skills/test_implement_severity_static.py` (S4 kept word for word; the S2 assertion moves to the digest; the `qa.md` pins stay), the fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` (update only the approved changed strings; rows for the retired task skill stay as they are) and the two plan tables the fixtures must be byte copies of, `.dev/review-severity-rule/cap-edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml` (the test `test_ej_fixtures_are_byte_copies_of_the_plan_tables` in `tests/skills/test_review_severity_rule.py` compares them; edit each pair in the same change, or record which relaxation of that test is chosen and why). `tests/skills/test_review_loop_extension.py`, `test_review_prompt_overrides.py` and `test_spec_panel_review_loop.py` must still pass unchanged. Also re-run `tests/skills/test_review_brief_rests_on.py` and `tests/skills/test_review_severity_registry.py` of the earlier stages (the first skips its legacy assertion once the pragmatic row is `v2`), `tests/skills/test_task_builder_merge.py` (it pins the Retry Monotonicity tokens of `rf-qa.md`; its parts that pin only retired carriers are not re-pinned) and `tests/review/test_review_rules_text.py`.
193: 
194: Acceptance criteria:
195: - `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_implement_severity_static.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_brief_rests_on.py tests/skills/test_review_severity_registry.py tests/skills/test_implement_follow_up_sweep.py tests/skills/test_task_builder_merge.py tests/review/test_review_rules_text.py -v` passes, including `test_ej_fixtures_are_byte_copies_of_the_plan_tables` and `test_h_implement_protocol_plugin_twins_byte_equal`.
196: - The two fixtures change only rows whose new text is the digest or the once-per-run cadence; the diff of each fixture and of each plan table is listed in `./artifacts/fixture-diff.md`.
197: - No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text, and the rows of `legacy` digest carriers still assert the old text.
198: 
199: ## Task 11: Re-pin the audit tests for the QA agents
200: 
201: Depends on: Task 6, Task 7
202: 
203: Update `tests/audit/test_nfr_conv_9_zero_trust.py` (byte-exact PASS and FAIL bullets of `src/superclaude/agents/rf-qa.md` and its `.claude/` mirror) to the reworded "any blocking gap" bullets on both surfaces; update `tests/audit/test_invariant_preservation_NFR_6_through_10.py` (it imports `FAIL_BULLET` and `PASS_BULLET` from the first module) in the same change; re-pin `tests/audit/test_severity_floor_unweakened.py` (the SHA-256 of the `## Critical Rules` block of `rf-qa-qualitative.md` and its mirror, and Rule 6 verbatim) to the Task 7 text, including the rewritten verdict pairs and the L3 text beside rule 10; leave `tests/audit/test_dnsp_all_agents_fail_bypass.py` unchanged unless the cap text moved.
204: 
205: Acceptance criteria:
206: - `uv run pytest tests/audit -v` passes.
207: - The re-pinned hash in `test_severity_floor_unweakened.py` matches the new `## Critical Rules` block on both the source and the mirror surface after `make sync-dev`.
208: - `test_dnsp_all_agents_fail_bypass.py` passes without an edit.
209: 
210: ## Task 12: Add the merge-rule reverse-scan test
211: 
212: Depends on: Task 6, Task 7, Task 8
213: 
214: Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude` (read only; nothing there is edited), matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`, one bullet per path (relative to `src/superclaude/`) with the status `allowed` or `exempt-by-retirement`: as stage 1 wrote it, `skills/sc-auggie-review-protocol/SKILL.md`, `skills/sc-review-severity/refs/rule.md`, the two code files `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` and, until the stage 4 package, the six stage 4 files (`skills/tech-reference/SKILL.md`, `skills/readme/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/operational-guide/SKILL.md`, `templates/documents/agent_template_qa.md` and `templates/documents/agent_template_analysis.md`) are `allowed`; the retired carriers `skills/task/SKILL.md`, `skills/task-builder/` (every file in the folder) and `agents/rf-task-builder.md` are `exempt-by-retirement`. A row marked `exempt-by-retirement` allows hits while its file exists and is not an error once the retirement has removed the file; every `allowed` row names a file that must exist. The stage 4 package removes each of its six files from the allow-list in the same change that edits it, and adds the plugin mirror of `refs/rule.md` to the allow-list and the registry before it copies the skill folder; the plugin mirror is NOT in the allow-list here.
215: 
216: Acceptance criteria:
217: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 6 to 8, with no hit in `src/superclaude/cli/` counted and the two hits in `src/superclaude/skills/task/SKILL.md` accepted only through its `exempt-by-retirement` row.
218: - A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
219: - The allow-list is read from `refs/scale-map.md`: a test fails when an `allowed` row names a file that does not exist, and a test shows an `exempt-by-retirement` row whose file or folder is missing does not fail.
220: 
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001: the owner's go in chat is recorded in the stage ledger | Task 1 | covered (containment 1.00) | source.md:3 |
| INF-002: the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and the owner has r | Task 1 | covered (containment 0.89) | source.md:3 |
| INF-003: at least 5 shadow runs have been observed with zero safety misses (by the stage 0 definiti | Constraints | covered (containment 0.93) | source.md:3 |
| INF-004: stage 0b's escape result is written and stage 0c's re-grade is written | none (mechanical) | unmatched by the mechanical rule | source.md:3 |
| INF-005: The seeded-recall result is produced INSIDE this package (first task) and gates the rule s | Constraints | covered (containment 0.79) | source.md:3 |
| INF-006: renumbered 1 onward, with its `## Constraints` (stage 3 parts) | none (mechanical) | unmatched by the mechanical rule | source.md:7 |
| INF-007: Earlier stages' evidence is read by package id. | Constraints | covered (containment 0.83) | source.md:7 |
| INF-008: State this is stage 3 and say what must be true at start (the list above). | Task 3 | covered (containment 0.67) | source.md:11 |
| INF-009: Stage 4 starts only after one audit window with no revert trigger tripped (the spec's sect | Constraints | covered (containment 0.95) | source.md:11 |
| INF-010: State that `/sc:implement` runs the whole package in order, so the rule switch cannot star | Constraints | covered (containment 0.67) | source.md:11 |
| INF-011: Read the seeded set and answer key from the stage 0 package by id. | Task 3 | covered (containment 0.89) | source.md:12 |
| INF-012: Each pass (old rule text, new rule text) is run with freshly spawned agents, never agents  | Task 3 | covered (containment 0.94) | source.md:12 |
| INF-013: Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the | Task 3 | covered (containment 0.93) | source.md:12 |
| INF-014: `./artifacts/seeded-recall-result.md` exists and shows pass on all three requirements | Task 5 | covered (containment 0.80) | source.md:13 |
| INF-015: when a line shows fail, the task's check fails and the run halts for the owner's Ruling | Task 5 | covered (containment 1.00) | source.md:13 |
| INF-016: Do not rely on `Depends on:` for this gate. | Task 5 | covered (containment 0.75) | source.md:13 |
| INF-017: `tests/skills/test_review_merge_rule_scan.py` reads the allow-list from `refs/scale-map.md | Task 12 | covered (containment 1.00) | source.md:14 |
| INF-018: No plugin mirror is listed (no package makes one). | Constraints | covered (containment 1.00) | source.md:14 |
| INF-019: The existence check applies to every file named in the allow-list and passes in this stage | Task 4 | covered (containment 0.62) | source.md:14 |
| INF-020: that a later task of the same package makes false get an end point ("until Task N"). | Constraints | covered (containment 0.82) | source.md:15 |
| INF-021: Write `./artifacts/stage3-summary-for-owner.md`: the seeded-recall result headline, the re | Task 13 | covered (containment 0.80) | source.md:16 |
| INF-022: and the revert triggers RT1 and RT2 with their current state, read from the spec's text an | Task 13 | covered (containment 0.77) | source.md:16 |
| INF-023: Say that the audit window runs after this package and is observed by the owner or operator | Task 13 | covered (containment 1.00) | source.md:16 |
| INF-024: No template, rule-prompt, builder, researcher or spec-panel edit (stage 4). | Constraints | covered (containment 1.00) | source.md:20 |
| INF-025: No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity co | Constraints | covered (containment 0.87) | source.md:20 |
| INF-026: No Jev call, key or account. | Constraints | covered (containment 0.75) | source.md:20 |
