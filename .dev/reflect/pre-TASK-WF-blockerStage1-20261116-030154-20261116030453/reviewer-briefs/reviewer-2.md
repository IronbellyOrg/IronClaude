# Reviewer brief 2 (persona: qa; model class: haiku)

## T1 card excerpt

**T1 reflection card (UC-1, pre-execution)**

Spec: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md` (22 lines: the stage 1 plan request; a byte copy of `stage-requests/stage1-request.md` in the program folder)
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (4 phases, 16 tasks, schema workflow-plan/1.2, 226 lines). Cited below as PLAN:<line>.
Author of this card: the reflect orchestrator, a self-review. It did not write the plan; the plan came from a `/sc:workflow` run in another session (executor class unknown). The T2 reviewers exist to break the self-review bias.
Program spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`, cited as SPEC:<line>. Base plan report: `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md` (8 blocking findings; F3, F4, F5, F6, F9, F12, F13, F15 touch stage 1).

#### Coverage and acceptance

Pass 1 found 0 labelled ids in source.md, so every requirement is an inferred row (Pass 2: 24 rows from the requirements-analyst agent, `artifacts/pass2-requirements-analyst.yaml`; the script confirmed every quote is a verbatim substring of its cited source.md line). The deterministic containment rule matched 16 of 24 (`coverage_pct_union` 0.6667, `S_dev_density` 0.3333); it is noisy on prose. It put INF-018 (T2 non-strict) on Task 3 and INF-022 (no carrier edit) on Task 6, both wrong. A manual read maps the 8 unmatched rows to the plan: INF-002, 004, 005, 023 and 024 to the Constraints block (PLAN:20-23), INF-003 to the task numbering (15 tasks plus the exit task), INF-008 to the absence of any gate prose after Phase 4, INF-020 to PLAN:24.

Source request items and where the plan answers them:
- Constraints (new files only, digest rows stay legacy, stage 2 only after owner go): PLAN:20.
- Task 13 allow-list without the phrases, listing the auggie file, `refs/rule.md` and six stage 4 files, plugin mirror deferred: Task 3, PLAN:59 and PLAN:65-66.
- Task 12 `rule.md` with GR5 and the grep acceptance for the old sentence: Task 2, PLAN:49 (the line carves out "outside the one fenced digest's own text"; source.md:13 asks for "prints nothing").
- Task 15/all refs, no `.dev/` or `artifacts/` path: Task 5, PLAN:87. Registry 11/1/2/5: Task 6, PLAN:96-100. T3/T2 scope and temporary-tree tests: Task 15, PLAN:209-215. Exit summary: Task 16, PLAN:217-226.
- "Acceptance lines that a later task makes false get an end point": stated at PLAN:24; applied once (PLAN:65 "until the stage 4 package"); not applied to PLAN:115 (see O1).

#### Checked and found sound

- 11 `digest` carriers exist under `src/superclaude/`, the old definition sentence is in exactly those 11 files (`grep -rln` over `src` and `plugins`), none contains `src/superclaude` (T3 can pass at `legacy`), and the cap sentence is at `pragmatic.md:227`. The 2 `pointer-only` source files exist; the 5 spec-panel variants are installed-only (`src/superclaude/commands` holds only `spec-panel.md`).
- SPEC:195-207 is the digest (REQ-01 with the REQ-02 and REQ-03 sentences and the cap sentence); SPEC:289-304 has 14 worked cases; SPEC:350-367 has the 16 Items columns of Task 4; SPEC:735-748 has the 12 families; 7 tasklist lines (1439, 1450, 1531, 1567, 1571, 1610, 1614) hold "High or Medium" or "Medium (blocking)".
- `classify` is a free subcommand name; modules export `command` and are listed in a tuple (`cli/review/__init__.py:1-36`); `tests/unit/test_cli_install.py` checks baseline members for presence only, so a new skill folder breaks no inventory; `lint-architecture` only pairs `sc-*-protocol` skills with commands (Makefile:362+); PyYAML is a declared dependency (`pyproject.toml:38`); `origin_repo.py`, `ledger.py`, `findings_v2.py`, `card_convert.py`, `doctor.py::run_doctor` and the named doctor tests exist.
- Findings of the base report: F4 (analysis template is no carrier row, PLAN:96), F5 and F12 (T3 exemptions, PLAN:209-215), F13 (scale map without the phrases, PLAN:66), F15 (no `.dev/` path, PLAN:87) are resolved in this plan; F6 only in part (O1); F3 only in part (O3).

Persona instructions (qa): audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Check that each source.md request item has a task whose acceptance line can fail when the requirement is not met (read the acceptance line itself before calling it unassertive), and check the stage 1 exit conditions of the program spec (SPEC:945) against the tasks.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:11:43Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Every hunk line is shown as `<real file line>: <text>`. The number before the colon is the line number in the real file, not a line of this brief. Cite those numbers; leave the `N: ` prefix out of any quote.

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:1-22
```markdown
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
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:12-27
```markdown
12: # Stage 1 plan: offline scaffold for the blocker classification work (issue #552)
13: 
14: Source: ./source.md
15: Goal: Create the new skill folder, its references, the registry, the ledger and classifier modules, the classify command, the safety route, the install check and their tests, all offline; no review-loop carrier is edited and every registry `digest` row stays `legacy`. The owner reads `./artifacts/stage1-summary-for-owner.md` and decides whether to say go for stage 2.
16: 
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
20: - One package, one stage. This is stage 1 of five packages (one plan per stage, the owner's decision of 2026-11-16). It creates new files only (the skill folder, new CLI modules, new tests, one doctor check) and edits no review-loop carrier (`pragmatic.md`, agents, templates, rule prompts, the task skill, tech-research, `WORKER-CONTRACT.md`); every registry `digest` row stays `legacy`. It runs only after the stage 0 package is done, the owner has read the stage 0 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Stage 2 starts only after the owner reads this package's summary and says go.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
24: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
25: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
26: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
27: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:31-53
```markdown
31: ## Task 1: Create the skill folder entry file
32: 
33: Create `src/superclaude/skills/sc-review-severity/SKILL.md` (the folder does not exist today, confirmed). It states the purpose, which ref is read by whom (the table of spec section 9.1), the rule version `v2`, and "Delegate-only, no slash command", in the style of the existing `sc-bare-review` skill. Do not name any `src/superclaude/` path inside it.
34: 
35: Acceptance criteria:
36: - The stage ledger `stage-requests/README.md` in PF has an owner go for stage 1 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
37: - The stage 0 package's `./artifacts/stage0-summary-for-owner.md` (read by package id) exists.
38: - `src/superclaude/skills/sc-review-severity/SKILL.md` exists with frontmatter, the five refs named in spec section 9.1 (`refs/rule.md`, `refs/scale-map.md`, `refs/follow-up-ledger.md`, `refs/classifier-questions.md`, `refs/registry.yaml`) and the line "Delegate-only, no slash command".
39: - `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/SKILL.md` prints nothing.
40: - After `make sync-dev`, `make verify-sync` reports the new folder in sync.
41: 
42: ## Task 2: Write the full rule with the pinned digest
43: 
44: Depends on: Task 1
45: 
46: Create `src/superclaude/skills/sc-review-severity/refs/rule.md`. It holds the full rule: the three blocking conditions, the Medium and Note classes, the counterfactual test and the table of spec section 4.2, the decision basis of section 4.3, the worked cases of section 5, the table-shape rule, the guardrails GR1 to GR12 of section 8.1 (GR5 names "highest severity wins" as the thing it does not re-create, so the file contains that phrase and the merge-rule scan allow-lists it), and the digest. The digest is the block of REQ-01 word for word, including REQ-02 (the unknown-consumer sentence), REQ-03 (the precedence sentence) and the cap sentence that today's `src/superclaude/output-styles/pragmatic.md` holds in its cap bullet ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings."), placed between the HTML-comment fence lines `review-severity:digest v2 begin` and `review-severity:digest v2 end`.
47: 
48: Acceptance criteria:
49: - `grep -rn "Grade every review finding as blocking or minor" src/superclaude/skills/sc-review-severity` prints nothing outside the one fenced digest's own text (the digest does not quote the old sentence either).
50: - `refs/rule.md` contains exactly one fenced digest whose last sentence equals the cap sentence of `src/superclaude/output-styles/pragmatic.md` word for word.
51: - The digest contains the sentences of REQ-02 and REQ-03.
52: - Every one of the 14 worked cases of spec section 5 appears with its verdict.
53: - `grep -n "src/superclaude" refs/rule.md` prints nothing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:80-102
```markdown
80: ## Task 5: Write the classifier question reference
81: 
82: Depends on: Task 1
83: 
84: Create `src/superclaude/skills/sc-review-severity/refs/classifier-questions.md`: the six decisive questions S, W, E, M, C, D of spec section 7.2 with the S wording "in a way the task did not ask for", the code-supplied input each needs, the Option Q replacement for D at upstream gates, and the optional explanation questions T, F, I and G (they feed no cell of the truth table). Add a version line `question-set v1`. State that M, C and E are asked only when code supplies their inputs, and say why in words (they were at chance in the five-run text-only test); this file cites no `.dev/` or `./artifacts/` path.
85: 
86: Acceptance criteria:
87: - `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing: no file of the skill folder cites a `.dev/` or `./artifacts/` path.
88: - `refs/classifier-questions.md` has the six questions with a "Needs from code" column and the line `question-set v1`.
89: - No question text contains the word "blocking" (`grep -in blocking` over the question table rows prints nothing).
90: - The file states that a failed or skipped answer is UNSET and never N.
91: 
92: ## Task 6: Write the carrier registry with every digest row set to legacy
93: 
94: Depends on: Task 2, Task 3
95: 
96: Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. Each row has the logical path relative to the install root, a `kind` (`digest`, `canonical`, `pointer-only` or `installed-only`), surfaces (source, installed, project `.claude/`, plugin, or `installed-only`), rollout stage, a state (`legacy` for a digest row until its file is moved), and an own-scale flag. Rows of kind `digest`, exactly the 11 definition carriers of spec section 10.1: `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`. One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; the stage 4 package adds its plugin mirror). Two rows of kind `pointer-only` (a pointer plus the ledger sentence, no digest): `rules/prompts/document_review_loop_prompts.md` and `commands/sc/spec-panel.md` (source `commands/spec-panel.md`). Five rows of kind `installed-only`: `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. `skills/task/SKILL.md` gets no row: it is not a digest carrier. `templates/documents/agent_template_analysis.md` gets no row either: it holds no definition sentence, only a merge-rule line, which the stage 4 package edits as text only.
97: 
98: Acceptance criteria:
99: - `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
100: - It has exactly 11 rows of kind `digest` (each with a source path that exists, state `legacy`, stage 3 for `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md`, stage 4 for the rest), 1 of kind `canonical`, 2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all.
101: - No row names `skills/task/SKILL.md`.
102: 
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:193-203
```markdown
193: ## Task 14: Add the install check for digest versions
194: 
195: Depends on: Task 6
196: 
197: Add `_check_review_severity_digests` to `src/superclaude/cli/doctor.py` and call it from `run_doctor` (REQ-27). It compares the digest versions held by the installed carriers with the packaged registry of `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, reading the packaged registry and not an installed copy (an installed skill folder is skipped once present, so an installed `registry.yaml` can be stale), and considers only rows of kind `digest`. Add tests to `tests/unit/test_cli_doctor.py`; keep `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`) passing because `run_doctor` must stay read-only.
198: 
199: Acceptance criteria:
200: - A test in `tests/unit/test_cli_doctor.py` builds an installed tree with a stale digest version and asserts the check reports the mismatch (T13).
201: - `uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py -v` passes.
202: - With every registry row at `legacy` and every installed carrier legacy, the check reports no mismatch.
203: - `make doctor` still runs and exits as before.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:217-226
```markdown
217: ## Task 16: Write the stage 1 exit summary for the owner
218: 
219: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15
220: 
221: Write `./artifacts/stage1-summary-for-owner.md`, the one file the owner reads before saying go for stage 2. For each of Tasks 1 to 15 give the files it created or changed and the command it ran with its observed pass count (for tests, the pytest summary line). List every file the package created. Show that no carrier was edited: `git diff --stat HEAD -- src/superclaude/output-styles src/superclaude/agents src/superclaude/templates src/superclaude/rules src/superclaude/commands src/superclaude/skills/task src/superclaude/skills/tech-research src/superclaude/core` prints nothing. List the open items and the owner decisions this stage touches (OD3 for any later external judge; OD4 authority none). End with the sentence that the owner's go for stage 2 is given in chat and not by this file.
222: 
223: Acceptance criteria:
224: - `./artifacts/stage1-summary-for-owner.md` names, for each of Tasks 1 to 15, the files and the observed result, and each named file exists.
225: - The file shows the carrier `git diff --stat HEAD` command above with empty output.
226: - The file lists OD3 and OD4 and the open items, and ends with the sentence that the owner's go for stage 2 is given in chat and not by this file.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:912-933
```markdown
912: ### 11.2 New tests the plan must add
913: 
914: | # | Test | Fails when |
915: |---|---|---|
916: | T1 | digest equality over the registry | a registry row's file does not hold exactly one digest equal to the digest section of `refs/rule.md` for its version |
917: | T2 | reverse scan of tracked `src/` and `plugins/` | a file holds the old definition sentence or a fence opener and is not a registry row; from stage 4, any legacy definition sentence remains |
918: | T3 | pointer line | a pointer does not name `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, or a carrier contains `src/superclaude` |
919: | T4 | scale map | a scale-map row names a missing file or a label that is not in it |
920: | T5 | merge-rule reverse scan | `highest severity`, `more severe rating` or `higher severity` appears in `src/` or `plugins/` outside the scale-map allow-list (staged with section 10.3) |
921: | T6 | truth-table properties | any of the three property tests of REQ-21 fails, or NA is reachable from a failed or skipped call (REQ-19) |
922: | T7 | ledger contract | a required column is missing; a Medium row lacks `why_not_blocking`; identity merges on digest alone; a codec round-trip fails (pipes, backticks, a triple-backtick line, literal entities, Unicode, multiline); a stale writer overwrites a newer revision; a malformed ledger is reset instead of preserved |
923: | T8 | crash, reconcile and consent | a resume asks again; a changed set is filed without new consent; a timeout after a successful post creates a second issue; a body whose read-back digest differs is marked `filed`; a repository other than the verified `<R>` is targeted |
924: | T9 | reviewer brief | `rests_on` or `why not blocking` is missing from a reviewer brief |
925: | T10 | unattended contract | an unattended run asks a question or makes a GitHub call; the three keys are missing; `follow_up_capture_state: incomplete` does not give `worker_status: partial` |
926: | T11 | classifier fixture replay | the fixture judge does not reproduce verdicts, or hostile instructions inside a quote change a verdict |
927: | T12 | no authority by default | a classifier verdict changes a gate outcome other than through the safety route |
928: | T13 | install check | a stale installed digest version is not reported (REQ-27) |
929: | T14 | precedence sentence | a v2 carrier lacks the precedence sentence (REQ-03) |
930: | T15 | plugin parity (stage 4) | the plugin mirror of the skill folder differs from `src` |
931: | T16 | final-gate sweep | a seeded Medium row whose flawed text reaches the final decision basis uncorrected is not made Blocking (GR7; precondition of OD14) |
932: | T17 | safety route | a GR1 vocabulary hit, or a judge answer S = Y or S = U, on a non-blocking row is written as a plain follow-up instead of `protected-risk-dispute` (GR12) |
933: 
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:944-949
```markdown
944: | 0. Measure (this program, offline) | this spec reviewed | 0a: the scored table and five runs with a fixture or approved judge, only if the table exists. 0b: the retrospective escape test on run 2 (section 8.4). 0c: three blind agents that did not write the rule re-grade the table under the old and the new text, paired, only if the table exists. Inventory freeze: every Grep of section 10 re-run, including the frozen FAIL-trigger Grep (REQ-30), with results stored | a written result: escape estimate with its interval; when the table exists, how many old-blocking rows become non-blocking and the confusion matrix | nothing changed |
945: | 1. Offline scaffold | stage 0 result written; owner go | the skill folder with registry rows all `legacy` (T1 and T2 accept the legacy text in registered rows); the ledger reader and writer with the codec; ledger adapters; the fixture judge; property tests; crash, reconcile and consent tests; the install check. No carrier is edited | T1 to T4, T6 to T8, T11 to T13 and T17 green offline | delete the new files |
946: | 2. Shadow beside the old rule | stage 1 exit | the task skill and tech-research gates write the ledger and make the per-run offer (it replaces the output style's "once per loop" ask for that run); reviewers emit `rests_on` while the old definition still decides; the classifier runs in shadow; the safety route GR12 is live; the final-gate sweep GR7 is built; `core/WORKER-CONTRACT.md` gains the three keys (REQ-12) | at least 5 shadow runs observed; ledger volume and `consumer-unknown` share known; offers answered; shadow agreement reported; zero safety misses and no capture failure | stop writing the ledger; restore the old carrier text by the three-step revert (section 9.4) |
947: | 3. Pilot | 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (section 8.3) met; 0c as well when the table exists; owner go | `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` move to digest v2 together; the stage 3 merge-rule lines of section 10.3 (task skill, rf-qa, rf-qa-qualitative, rf-analyst; L1); L2 fix-pass checks; L6 for rf-qa, and Rule 6 if OD16 chooses (b), with its test re-pinned in the same change; the cadence pins move | one audit window (section 8.2) with no revert trigger tripped; M12 reported | the three-step revert of the pilot rows to `legacy` |
948: | 4. Propagate | stage 3 exit; owner go | templates, rule prompts, builders and researchers to v2; the stage 4 lines of section 10.3; the spec-panel narrowing; the plugin mirror and parity test; T2 becomes strict (no legacy definition sentence in `src/` or `plugins/`) | drift tests green and strict; a second audit window clear | per-row three-step revert |
949: 
```

## Coverage slice

| Requirement | Card ID (task) | Status | Grounding |
|---|---|---|---|
| INF-001: Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summary-for-owner.md` and said go in chat, and after the stage ... (source.md:3) | Task 1 | covered | PLAN:36-37; mechanical rule: containment (task 1, ratio 0.882) |
| INF-002: This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-loop carrier. (source.md:3) | Constraints | covered | PLAN:20; mechanical rule: none (task 14, ratio 0.556) |
| INF-003: Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 2, stage 1; found by that folder name under `.de... (source.md:7) | task numbering | covered | PLAN:31-226 (15 tasks plus the exit task); mechanical rule: none (task 1, ratio 0.25) |
| INF-004: Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-built list, the classifier f... (source.md:7) | Constraints | covered | PLAN:19-27; mechanical rule: none (task 10, ratio 0.45) |
| INF-005: The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation) is read by package id. (source.md:7) | Constraints, Task 1 | covered | PLAN:19, PLAN:37; mechanical rule: none (task 1, ratio 0.455) |
| INF-006: State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. (source.md:11) | Constraints, Task 6 | covered | PLAN:20, PLAN:100; mechanical rule: containment (task 6, ratio 0.733) |
| INF-007: The next package (stage 2) starts only after the owner's go in chat. (source.md:11) | Constraints | covered | PLAN:20; mechanical rule: containment (task 1, ratio 0.778) |
| INF-008: Drop the base plan's Phase 3 to 5 gate prose. (source.md:11) | no Phase 3-5 gate prose | covered | PLAN:29-226 has Phases 1-4 only; mechanical rule: none (task 4, ratio 0.167) |
| INF-009: The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definition sentence. (source.md:12) | Task 3 | covered | PLAN:59, PLAN:66; mechanical rule: containment (task 3, ratio 1.0) |
| INF-010: At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. (source.md:12) | Task 3 | covered (see O3) | PLAN:59, PLAN:65; mechanical rule: containment (task 3, ratio 1.0) |
| INF-011: Say in the task that the plugin mirror is added in stage 4, not here. (source.md:12) | Task 3 | covered | PLAN:59; mechanical rule: containment (task 3, ratio 0.857) |
| INF-012: `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) but never quotes the old definition sentence "Grade every r... (source.md:13) | Task 2 | partial (see O4) | PLAN:46, PLAN:49; mechanical rule: containment (task 2, ratio 0.765) |
| INF-013: No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path (acceptance: `grep -rn "\.dev/\/artifacts/" src/s... (source.md:14) | Task 5 | covered | PLAN:87; mechanical rule: containment (task 5, ratio 1.0) |
| INF-014: State the M, C and E input rule in words. (source.md:14) | Task 5 | covered | PLAN:84; mechanical rule: containment (task 5, ratio 0.75) |
| INF-015: Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). (source.md:15) | Task 6 | covered | PLAN:96-100; mechanical rule: containment (task 6, ratio 0.9) |
| INF-016: Say the analysis template is not a carrier row (merge-rule text only in stage 4). (source.md:15) | Task 6 | covered | PLAN:96; mechanical rule: containment (task 6, ratio 0.727) |
| INF-017: T3's `src/superclaude` check applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order ... (source.md:16) | Task 15 | covered | PLAN:209; mechanical rule: containment (task 15, ratio 1.0) |
| INF-018: T2 is non-strict (strict only in stage 4). (source.md:16) | Task 15 | covered | PLAN:209; mechanical rule: containment (task 3, ratio 0.6) |
| INF-019: Acceptance includes a temporary-tree test of each exemption. (source.md:16) | Task 15 | covered | PLAN:212; mechanical rule: containment (task 15, ratio 0.857) |
| INF-020: **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N"). (source.md:17) | Constraints | partial (see O1) | PLAN:24, PLAN:65; mechanical rule: none (task 3, ratio 0.385) |
| INF-021: Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the commands run and their pass c... (source.md:18) | Task 16 | covered | PLAN:221-226; mechanical rule: containment (task 16, ratio 0.838) |
| INF-022: No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and no stage 2 to 4 task. (source.md:22) | Constraints | covered | PLAN:20, PLAN:22; mechanical rule: containment (task 6, ratio 0.647) |
| INF-023: Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. (source.md:22) | Constraints | covered | PLAN:22; mechanical rule: none (task 3, ratio 0.529) |
| INF-024: No Jev call, key or account. (source.md:22) | Constraints | covered | PLAN:22; mechanical rule: none (task 8, ratio 0.4) |
