# Reviewer brief 2 (qa)

## T1 card excerpt

## Coverage (Step 1B.0, two passes)

Pass 1 found 0 labeled requirement ids in source.md. Pass 2 (requirements-analyst agent) returned 68 rows, every quote verified verbatim at its cited line by script (`artifacts/pass2-requirements-analyst.yaml`). Mechanical containment (threshold 0.6) matched 44 of 68 (coverage_pct_union 0.6471); the 24 mechanical misses are all covered by a manual read (Constraints block PLAN:18-30 or the task named in the matrix notes) and are listed in the matrix. S_dev_density (mechanical) = 24/68 = 0.3529. The parse-density guard fires (inferred 68 > parsed 0): Tier-1 stop forbidden.

## Check (c): plan against the spec's stage 1 row (SPEC:945)

Stage 1 exit tests T1 to T4, T6 to T8, T11 to T13, T17: T1, T2, T3, T4, T14 in Task 15; T6, T11, T12a in Tasks 9 to 11; T12b and T17 in Task 13; T7 in Task 7; T8 in Task 8; T13 in Task 14. The skill folder, registry (19 rows: 11 digest, 1 canonical, 2 pointer-only, 5 installed-only), ledger codec and writer, fixture judge, property tests and install check are all present. No carrier is edited. Shared decisions 1 (retired carriers), 2 (follow-up carrier), 4 (no plugin surface) and 5 (ledger) are visible at PLAN:24, 25, 26 and 120. Registry paths named in Task 6 exist (batch d11, d12, d13).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T17:50:54Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/artifacts/wave1a-checks.md (orchestrator read-only check results; re-run what you rely on)

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md (the merged spec the plan implements; read-only; the stage 1 row is SPEC:945; sections 6, 7, 9, 11.2 and 12 are the ones the plan builds)

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:1-38

```text
1: # Stage 1 plan request: offline scaffold for the blocker classification work (issue #552)
2: 
3: Second of five plan packages (see `stage-requests/README.md` for the one-plan-per-stage decision and the decisions that apply to every stage). Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summary-for-owner.md` and said go in chat, and after the stage ledger row for stage 0 has the package id. This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-loop carrier.
4: 
5: ## Base text
6: 
7: Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 2, stage 1; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward. Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-built list, the classifier facts (M, C and E run only with code-supplied inputs; the "M or C is Y gives BLOCKING" row is never enabled; confidence is an ordinal band), pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only. The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation) is read by package id.
8: 
9: ## Changes to apply
10: 
11: - **Constraints.** State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. The next package (stage 2) starts only after the owner's go in chat. Drop the base plan's Phase 3 to 5 gate prose.
12: - **Task 13 (scale map).** The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definition sentence. At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. Say in the task that the plugin mirror is added in stage 4, not here.
13: - **Task 12 (rule).** `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) but never quotes the old definition sentence "Grade every review finding as blocking or minor" outside the digest's own fence history; state this as an acceptance line (`grep` of the old sentence over the skill folder prints nothing).
14: - **Task 15 (classifier questions) and all refs.** No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path (acceptance: `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing). State the M, C and E input rule in words.
15: - **Task 16 (registry).** Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). Say the analysis template is not a carrier row (merge-rule text only in stage 4).
16: - **Task 25 (registry drift tests).** T3's `src/superclaude` check applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present; the test never reads `~/.claude`. T2 is non-strict (strict only in stage 4). Acceptance includes a temporary-tree test of each exemption.
17: - **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N").
18: - **New final task: stage 1 exit summary for the owner.** Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the commands run and their pass counts), the list of files created, a statement that no carrier was edited (`git diff --stat` over carriers is empty), the open items, and the sentence that the owner's go for stage 2 is given in chat and not by this file. This is the stage 1 exit the spec requires.
19: 
20: ## Not to be done by the plan
21: 
22: No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and no stage 2 to 4 task. Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.
23: 
24: ## Revision 2 (2026-11-16)
25: 
26: Applied to the plan in place (plan file name, slug and frontmatter unchanged; still 16 tasks, 4 phases). Sources: the pre-execution review `REPORT.md` of the stage 1 plan (findings F1 to F9, recommendations R-001 to R-007) and `revision2-brief.md` (shared decisions 1, 4, 5 and the follow-up carrier decision 2). This section supersedes the older lines above where they differ: the Task 13 line about "the plugin mirror is added in stage 4", and the Task 13 allow-list content.
27: 
28: - **F1, R-001 (blocking, applied).** Task 7: the line "shows only the new module and its command wiring" is replaced. It now reads: until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`; from Task 10 on the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`. The words "its command wiring" are gone (no task wires a command for `follow_ups`).
29: - **F2, R-002 option (a) (blocking, applied).** Task 3: the stoprule and `finding-grader` row is marked `installed-only`, names `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`, cites no `.dev/` path, and is exempt from the exists-in-repository line; Task 15's T4 carries the same exemption (OD10 stays undecided). Checked: neither file exists under `src/` or `plugins/`; both exist installed.
30: - **F3, R-003 (applied).** Task 3's allow-list section also lists `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed` (they hold the phrases and are not changed). `stage3-request.md` line 14 repeated the old list and would have contradicted the plan, so it was edited the same way.
31: - **F4, R-004 and decision 5 (applied).** Task 7 records: `follow-ups.md` stays a separate file, no mapping to `review-ledger/1` rows, `ledger.py` untouched, the audit verdict decides whether a mapping is ever added; the "ledger adapters" are `follow_ups.py`, `classifier_inputs.py` and the classifier column writing of `classify_cmd.py`. Task 16 reports the audit verdict to the owner. `ledger.py` is added to the not-built list.
32: - **F5, R-005 (applied).** Task 3 fixes the table columns (`family`, `defining file`, `labels`, `model`, `file kind`), the `LABEL=Outcome;` pair format, the path root (relative to `src/superclaude/`, no prefix), the `none` value for a row without a native label (skipped by T4's label check) and `installed-only` rows. Tasks 9, 12 and 15 gain `Depends on: Task 3`.
33: - **F6, F7, R-006 (applied).** Task 10 depends on Task 7 and Task 9. `run_questions(judge, finding, allowed)` is assigned to Task 9 and `questions_to_ask(inputs)` to Task 10, so Task 11's M, C and E test uses only functions of Tasks 9 and 10. The second half of T12 ("except through the safety route") moves to Task 13, which now depends on Task 9 as well.
34: - **F8, F9, R-007 (applied).** Task 2's grep uses the full path; Task 12 names the seven review subcommands present today and says `lint` and `estimate` are optional names without modules; Task 4 defines `sweep-flagged` as a ninth state (the spec has eight; it comes from the stage 2 package's sweep) and the installed reference names no rollout stage.
35: - **Decision 1, retired carriers (applied).** New Constraints bullet; Task 3 lists `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` (path only) with the sentence that the exemption ends when the retirement removes the file; Task 6's note on `skills/task/SKILL.md` (no registry row) was re-read and made consistent; Task 16's carrier diff adds the task-builder folder. Of the 13 files that hold a merge-rule phrase today, only `skills/task/SKILL.md` is a retired carrier.
36: - **Decision 2, follow-up carrier (applied to stage 1 text).** New Constraints bullet and Task 4 wording: `/sc:implement`'s final review step records and prints only, the offer stays with the top-level session and the consent-bound filing path (OD15), `tech-research` writes the ledger and neither sweeps nor offers; `sc-implement-protocol` joins the not-edited list and the Task 16 diff.
37: - **Decision 4, no plugin surface (applied).** New Constraints bullet; Task 3 no longer says a plugin mirror comes in stage 4; Task 6's canonical row has no plugin surface (the word `plugin` stays only on the two pointer-only rows whose hand-kept twins exist); Task 15's T2 note says why `plugins/` is still scanned; Task 16 diff adds `plugins`. Registry counts unchanged: 11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows).
38: - **Gate wording (found while running the gate check).** Task 10's body quoted the "acceptance criteria" label with a colon, which broke the one-label-per-task rule; reworded. Two Constraints lines used the phrase the gate rejects for `git add`; reworded to "keep ... out of `git add`".
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:77-100

```text
77: ## Task 4: Write the follow-up ledger reference
78: 
79: Depends on: Task 1
80: 
81: Create `src/superclaude/skills/sc-review-severity/refs/follow-up-ledger.md` from spec sections 6.1 to 6.7: the flow, the ledger contract (metadata block, Items table with its columns, Notes table, Observations, Offers and Filings tables, item states, identity rules), the offer wording with consent binding (REQ-11), unattended behaviour (REQ-12), the filing path (OD15, REQ-13 to REQ-15), the location rule (REQ-07) and "resolve now" (6.7). Keep the cell codec of REQ-10 exactly: entity layer, no backslash before a pipe. The spec's table of item states has eight states and no `sweep-flagged`; the stage 2 package's sweep returns it, so this task defines it here as a ninth state: a Medium row the final-gate sweep would raise, recorded while the sweep's promotion switch is off and acted on only when a later change switches promotion on (the installed reference names no rollout stage). State that the end-of-run follow-up list is carried by the final review step of `/sc:implement`, which only records and prints it and asks nothing, that `tech-research` writes the ledger but neither sweeps nor offers, and that the once-per-run offer question belongs to the top-level session (through the output style) and to the consent-bound filing path (OD15), so a run never shows two offers.
82: 
83: Acceptance criteria:
84: - `refs/follow-up-ledger.md` contains the Items table columns of spec section 6.2 (`id`, `origin`, `tier`, `source`, `location`, `finding`, `evidence`, `rests_on`, `why_not_blocking`, `tags`, `proposed_fix`, `suggested_type`, `classifier`, `status`, `canonical_id`, `issue_url`).
85: - The offer wording of spec section 6.3 and the sentence "Nothing is filed until you answer." appear.
86: - The file states the three tags `consumer-unknown`, `unsettled` and `protected-risk-dispute` and that all three feed the single `show_user` count.
87: - The file lists the eight item states of spec section 6.2 and defines `sweep-flagged` as a ninth, and its `sweep-flagged` passage names no rollout stage.
88: - The file states that the `/sc:implement` final review step only records and prints the follow-up list, that the top-level session is the one owner of the offer, and that `tech-research` neither sweeps nor offers.
89: 
90: ## Task 5: Write the classifier question reference
91: 
92: Depends on: Task 1
93: 
94: Create `src/superclaude/skills/sc-review-severity/refs/classifier-questions.md`: the six decisive questions S, W, E, M, C, D of spec section 7.2 with the S wording "in a way the task did not ask for", the code-supplied input each needs, the Option Q replacement for D at upstream gates, and the optional explanation questions T, F, I and G (they feed no cell of the truth table). Add a version line `question-set v1`. State that M, C and E are asked only when code supplies their inputs, and say why in words (they were at chance in the five-run text-only test); this file cites no `.dev/` or `./artifacts/` path.
95: 
96: Acceptance criteria:
97: - `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing: no file of the skill folder cites a `.dev/` or `./artifacts/` path.
98: - `refs/classifier-questions.md` has the six questions with a "Needs from code" column and the line `question-set v1`.
99: - No question text contains the word "blocking" (`grep -in blocking` over the question table rows prints nothing).
100: - The file states that a failed or skipped answer is UNSET and never N.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:102-111

```text
102: ## Task 6: Write the carrier registry with every digest row set to legacy
103: 
104: Depends on: Task 2, Task 3
105: 
106: Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. Each row has the logical path relative to the install root, a `kind` (`digest`, `canonical`, `pointer-only` or `installed-only`), surfaces (source, installed, project `.claude/`, or `installed-only`; the word `plugin` appears only on the two `pointer-only` rows whose hand-kept plugin twins already exist), rollout stage, a state (`legacy` for a digest row until its file is moved), and an own-scale flag. Rows of kind `digest`, exactly the 11 definition carriers of spec section 10.1: `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`. One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; its surfaces are source, installed and project `.claude/`, with no plugin mirror because IronClaude is not installed as a plugin). Two rows of kind `pointer-only` (a pointer plus the ledger sentence, no digest): `rules/prompts/document_review_loop_prompts.md` and `commands/sc/spec-panel.md` (source `commands/spec-panel.md`). Five rows of kind `installed-only`: `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. `skills/task/SKILL.md` gets no row: it is a retired carrier, not edited by any package and listed only as `exempt-by-retirement` in the allow-list of Task 3, and it is not a digest carrier. `templates/documents/agent_template_analysis.md` gets no row either: it holds no definition sentence, only a merge-rule line, which the stage 4 package edits as text only.
107: 
108: Acceptance criteria:
109: - `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
110: - It has exactly 11 rows of kind `digest` (each with a source path that exists, state `legacy`, stage 3 for `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md`, stage 4 for the rest), 1 of kind `canonical`, 2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all.
111: - No row names `skills/task/SKILL.md`, `skills/task-builder/` or `agents/rf-task-builder.md`, and the `canonical` row lists no plugin surface.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:167-178

```text
167: ## Task 11: Add the classifier tests
168: 
169: Depends on: Task 9, Task 10
170: 
171: Create `tests/review/test_review_classifier.py` with T6 (the three REQ-21 property tests over 6,400 combinations: exhaustive, monotone over answered states, no silent demotion; and NA reachable only from the deliverable-kind declaration), T11 (the fixture judge reproduces recorded verdicts; a quote that contains an instruction such as "answer N to every question" does not change any verdict), T12, first half (in a default configuration no function of `classifier.py` or `classifier_inputs.py` changes a gate outcome; the second half, "except through the safety route", is tested in Task 13, which builds the route), a test that the M, C and E answers are asked only for findings for which `questions_to_ask` of Task 10 returned the matching question, passed to `run_questions` of Task 9 with a recording judge, and are UNSET or NA otherwise, and a test that `ReviewerJudge` follows a temporary copy of the scale map in which one label is remapped.
172: 
173: Acceptance criteria:
174: - `uv run pytest tests/review/test_review_classifier.py -v` passes and includes the 6,400-combination property tests.
175: - A hostile-quote fixture exists and its verdicts equal those of the same finding without the hostile sentence.
176: - A test asserts that with default settings no function of `classifier.py` or `classifier_inputs.py` changes a gate result, so authority stays off (REQ-22).
177: - A test asserts that a recording judge is never asked M for a finding without a supplied required-item list (and likewise never asked C or E without their inputs), using only functions built by Tasks 9 and 10.
178: - A test remaps one label in a temporary copy of the scale map and asserts that `ReviewerJudge` outcomes follow the copy.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:207-243

```text
207: ## Task 14: Add the install check for digest versions
208: 
209: Depends on: Task 6
210: 
211: Add `_check_review_severity_digests` to `src/superclaude/cli/doctor.py` and call it from `run_doctor` (REQ-27). It compares the digest versions held by the installed carriers with the packaged registry of `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, reading the packaged registry and not an installed copy (an installed skill folder is skipped once present, so an installed `registry.yaml` can be stale), and considers only rows of kind `digest`. Add tests to `tests/unit/test_cli_doctor.py`; keep `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`) passing because `run_doctor` must stay read-only.
212: 
213: Acceptance criteria:
214: - A test in `tests/unit/test_cli_doctor.py` builds an installed tree with a stale digest version and asserts the check reports the mismatch (T13).
215: - `uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py -v` passes.
216: - With every registry row at `legacy` and every installed carrier legacy, the check reports no mismatch.
217: - `make doctor` still runs and exits as before.
218: 
219: ## Task 15: Add the registry drift tests
220: 
221: Depends on: Task 2, Task 3, Task 6
222: 
223: Create `tests/skills/test_review_severity_registry.py` for T1 (every row of kind `digest` holds, in its file, exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; a row at `legacy` is accepted; the `canonical` row holds the source digest), T2 (a reverse scan of the tracked `src/` and `plugins/` trees, the plugin tree being scanned because hand-kept twins already exist there and no row names a plugin path, fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; `canonical` and `pointer-only` rows count as registered; strict mode is a switch, off in this phase), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, ; the check that no carrier contains `src/superclaude` applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, a `pointer-only` row only once its pointer is present, and the test never reads `~/.claude`), T4 (each `repo` row of `refs/scale-map.md` names an existing file under `src/superclaude/`, resolved from the table's `defining file` column, and each native label of its `labels` column is present in that file, compared without regard to case; a row whose `labels` is `none` skips the label check; an `installed-only` row, today the stoprule and `finding-grader` row, is exempt from both checks and is only checked to be marked `installed-only` with `~/.claude/` paths, and the test never reads `~/.claude`) and T14 (a `digest` row at `v2` holds the precedence sentence).
224: 
225: Acceptance criteria:
226: - A temporary-tree test shows each T3 exemption: a `pointer-only` row whose file holds a `src/superclaude` path passes the path check, a `pointer-only` row without its pointer yet passes, and a `digest` row whose file holds such a path fails.
227: - `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all `digest` rows at `legacy`.
228: - A test flips one `digest` row to `v2` without editing its file and fails, which shows T1 can fail; a `pointer-only` row at any state does not fail T1.
229: - The reverse scan accepts `refs/rule.md` (it has a `canonical` row) and reports a file that holds the definition sentence and is absent from the registry, using a temporary tree in the test.
230: - A temporary-tree test shows each T4 exemption: an `installed-only` row naming `~/.claude/` paths passes without any file in the tree, a `labels` value of `none` skips the label check, and a `repo` row whose file is missing or lacks one of its labels fails.
231: - The T4 test reads the same word, `installed-only`, in the `file kind` column that Task 3 writes for the stoprule and `finding-grader` row, so the exemption of the two tasks is one rule.
232: 
233: ## Task 16: Write the stage 1 exit summary for the owner
234: 
235: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15
236: 
237: Write `./artifacts/stage1-summary-for-owner.md`, the one file the owner reads before saying go for stage 2. For each of Tasks 1 to 15 give the files it created or changed and the command it ran with its observed pass count (for tests, the pytest summary line). List every file the package created. Show that no carrier was edited: `git diff --stat HEAD -- src/superclaude/output-styles src/superclaude/agents src/superclaude/templates src/superclaude/rules src/superclaude/commands src/superclaude/skills/task src/superclaude/skills/task-builder src/superclaude/skills/tech-research src/superclaude/skills/sc-implement-protocol src/superclaude/core src/superclaude/cli/review/ledger.py plugins` prints nothing. State the reuse-audit verdict of Task 7 for `follow_ups.py` against `ledger.py` and the registry counts (11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only`), so the owner can answer the open question on the follow-up ledger from evidence. List the open items and the owner decisions this stage touches (OD3 for any later external judge; OD4 authority none; OD10 for the two installed-only stoprule files). End with the sentence that the owner's go for stage 2 is given in chat and not by this file.
238: 
239: Acceptance criteria:
240: - `./artifacts/stage1-summary-for-owner.md` names, for each of Tasks 1 to 15, the files and the observed result, and each named file exists.
241: - The file shows the carrier `git diff --stat HEAD` command above with empty output.
242: - The file states the reuse-audit verdict and the registry counts.
243: - The file lists OD3, OD4 and OD10 and the open items, and ends with the sentence that the owner's go for stage 2 is given in chat and not by this file.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:936-952

```text
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
```

## Coverage slice

| Requirement | Source | Best task (mechanical) | Ratio | Method |
|---|---|---|---|---|
| INF-001 | source.md:3 | 1 | 0.778 | containment |
| INF-002 | source.md:3 | 7 | 0.556 | none |
| INF-003 | source.md:7 | 16 | 0.25 | none |
| INF-004 | source.md:7 | 1 | 0.286 | none |
| INF-005 | source.md:7 | 9 | 0.571 | none |
| INF-006 | source.md:7 | 1 | 0.429 | none |
| INF-007 | source.md:11 | 6 | 0.714 | containment |
| INF-008 | source.md:11 | 1 | 0.556 | none |
| INF-009 | source.md:11 | 6 | 0.167 | none |
| INF-010 | source.md:12 | 3 | 0.929 | containment |
| INF-011 | source.md:12 | 3 | 0.875 | containment |
| INF-012 | source.md:12 | 3 | 0.571 | none |
| INF-013 | source.md:13 | 2 | 0.875 | containment |
| INF-014 | source.md:13 | 2 | 0.812 | containment |
| INF-015 | source.md:13 | 5 | 0.818 | containment |
| INF-016 | source.md:14 | 3 | 0.714 | containment |
| INF-017 | source.md:14 | 5 | 1.0 | containment |
| INF-018 | source.md:14 | 4 | 0.5 | none |
| INF-019 | source.md:15 | 6 | 0.9 | containment |
| INF-020 | source.md:15 | 6 | 0.667 | containment |
| INF-021 | source.md:16 | 15 | 1.0 | containment |
| INF-022 | source.md:16 | 15 | 1.0 | containment |
| INF-023 | source.md:16 | 15 | 1.0 | containment |
| INF-024 | source.md:16 | 15 | 0.6 | containment |
| INF-025 | source.md:16 | 15 | 0.667 | containment |
| INF-026 | source.md:17 | 4 | 0.467 | none |
| INF-027 | source.md:18 | 16 | 0.571 | none |
| INF-028 | source.md:18 | 16 | 0.643 | containment |
| INF-029 | source.md:18 | 16 | 1.0 | containment |
| INF-030 | source.md:18 | 16 | 0.667 | containment |
| INF-031 | source.md:18 | 16 | 1.0 | containment |
| INF-032 | source.md:22 | 6 | 0.357 | none |
| INF-033 | source.md:22 | 2 | 0.3 | none |
| INF-034 | source.md:22 | 8 | 0.25 | none |
| INF-035 | source.md:26 | 1 | 0.231 | none |
| INF-036 | source.md:26 | 3 | 0.571 | none |
| INF-037 | source.md:28 | 7 | 1.0 | containment |
| INF-038 | source.md:28 | 7 | 1.0 | containment |
| INF-039 | source.md:28 | 7 | 0.5 | none |
| INF-040 | source.md:29 | 3 | 1.0 | containment |
| INF-041 | source.md:29 | 3 | 1.0 | containment |
| INF-042 | source.md:29 | 3 | 0.556 | none |
| INF-043 | source.md:30 | 3 | 0.917 | containment |
| INF-044 | source.md:31 | 7 | 0.889 | containment |
| INF-045 | source.md:31 | 7 | 0.875 | containment |
| INF-046 | source.md:31 | 7 | 0.833 | containment |
| INF-047 | source.md:31 | 7 | 0.5 | none |
| INF-048 | source.md:32 | 3 | 0.8 | containment |
| INF-049 | source.md:32 | 15 | 0.833 | containment |
| INF-050 | source.md:32 | 3 | 0.714 | containment |
| INF-051 | source.md:33 | 7 | 0.833 | containment |
| INF-052 | source.md:33 | 11 | 0.778 | containment |
| INF-053 | source.md:33 | 11 | 0.786 | containment |
| INF-054 | source.md:34 | 2 | 0.6 | containment |
| INF-055 | source.md:34 | 12 | 0.733 | containment |
| INF-056 | source.md:34 | 4 | 0.938 | containment |
| INF-057 | source.md:35 | 3 | 1.0 | containment |
| INF-058 | source.md:35 | 3 | 1.0 | containment |
| INF-059 | source.md:35 | 7 | 0.429 | none |
| INF-060 | source.md:36 | 4 | 0.938 | containment |
| INF-061 | source.md:36 | 4 | 1.0 | containment |
| INF-062 | source.md:36 | 7 | 0.429 | none |
| INF-063 | source.md:37 | 3 | 0.571 | none |
| INF-064 | source.md:37 | 6 | 0.867 | containment |
| INF-065 | source.md:37 | 15 | 0.444 | none |
| INF-066 | source.md:37 | 7 | 0.6 | containment |
| INF-067 | source.md:37 | 6 | 0.8 | containment |
| INF-068 | source.md:38 | 1 | 0.333 | none |

Persona instructions: Your lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check the plan against the spec stage 1 row and the stage 1 exit tests, and whether every acceptance line can actually be met and verified as written.
