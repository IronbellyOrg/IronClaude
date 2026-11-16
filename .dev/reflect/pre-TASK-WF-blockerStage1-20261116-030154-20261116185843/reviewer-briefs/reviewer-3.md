# Reviewer 3 brief (persona: refactorer; model class: opus)

## T1 card excerpt
#### Earlier findings (first review F1 to F9, second review M-F1 to M-F10): all fixed in the live text

| Finding | Where it is fixed now |
|---|---|
| F1, M-F1 (Task 7 grep lists `.pyc`) | PLAN:129: `grep -rln --include='*.py' --exclude-dir=__pycache__ "follow_ups" src/superclaude/cli/review`, "lists no file other than" in both sentences, with the end point "until the stage 2 package adds its own importer" |
| F2, F3 (stoprule row, allow-list) | PLAN:64, 66, 70 (`installed-only` row, 12 keys, allow-list holds `remediate_parser.py` and `fmea_classifier.py`) |
| F4 (ledger decision) | PLAN:124, 248, 22 |
| F5, M-F2 (scale-map grammar) | PLAN:62 (family key, `LABEL=Outcome` pairs, `Conditional` token, ` + ` separator, `none`), PLAN:151 (lookup key, UNSET for unknown family, unlisted label, `Conditional`), PLAN:234 (T4 splits ` + `) |
| F6, F7 (dependencies, `run_questions`, `questions_to_ask`) | PLAN:164 (Depends on 7, 9), PLAN:151, PLAN:166, PLAN:204 (Depends on 7, 9) |
| F8, F9 | PLAN:52 (full path), PLAN:192 (seven subcommands named, `lint` and `estimate` have no module: confirmed), PLAN:82 (`sweep-flagged` as a ninth state) |
| M-F3 (REQ-09) | PLAN:124 (`earlier_decisions`) |
| M-F4 (M and D inputs) | PLAN:166 (`absent-by-name` precheck, decision-basis excerpts, Option Q) |
| M-F5 (verdict store) | PLAN:192 (`classifier-results.json`, `update_field`), PLAN:124 |
| M-F6 (resolver) | PLAN:137, 141 (injected resolver, by-path load; `read_origin` confirmed) |
| M-F7 (paths in new refs) | PLAN:82, 90, 99-100, 115 (greps) |
| M-F8 (Task 1 order) | PLAN:36 |
| M-F9, M-F10 | PLAN:192 (`verify-citations`), PLAN:52, 72 (count 9, matches the live grep), PLAN:151 (name off `THRESHOLDS`), PLAN:131, 160, 173, 200, 213 (`make lint`) |

#### Findings of this review (provisional, T1)

- **T1-F1 (non-blocking).** PLAN:124 asks for a test that `earlier_decisions` "does not return a `pending` row", but `pending` is not an item state: the item states are `recorded`, `offered`, `resolving`, `resolved`, `filed`, `declined`, `duplicate`, `superseded` (SPEC:381-390) plus `sweep-flagged` (PLAN:82); `pending` is a state of the Offers table (SPEC:375). The executor must guess which row to use (likely `recorded` or `offered`).
- **T1-F2 (non-blocking).** The consent binding of REQ-11 (SPEC:421-428; Offers table with `set_digest`, `answer`, `state`, SPEC:375) has no code owner. Task 7 (PLAN:124) lists no Offers table logic and Task 8 (PLAN:137) builds only the Filings table, yet Task 8 must test "a resume asks again" and "a changed set is filed without new consent" (T8, SPEC:923). The tests have no function to call unless the executor invents an offer object.
- **T1-F3 (non-blocking).** Task 10 (PLAN:166) supplies the NA marker for M only. REQ-19 (SPEC:528) lets NA stand for M and for C, but no task supplies the "kind declared to have no constraint list" marker, so C is UNSET for every finding without constraint lines, and REQ-18 (SPEC:543) then lifts every such verdict to SHOW_USER; the classifier will say SHOW_USER for most non-spec deliverables in stage 2.
- **T1-F4 (non-blocking).** Task 3 (PLAN:62) names the lens-scale row but gives no outcome values for CRITICAL, IMPORTANT and MINOR, and the spec says only that the label is information (SPEC:737). Stage 2 Task 2 (STAGE2:57) sets the tier of every imported row from that row, and `ReviewerJudge` (PLAN:151) returns UNSET for a `Conditional` label. If the executor writes `Conditional` for all three, stage 2 gets no tier for any row.
- **T1-F5 (minor).** STAGE2:27 still quotes the old stage 1 wording ("only the new module and its command wiring mention `follow_ups`"); PLAN:129 now says something different with an end point. The stage 2 sentence is harmless (it says the line describes the end of stage 1) but quotes text that no longer exists.

No finding rises to blocking: every task is reachable in order, every dependency points to a lower number, every acceptance check I ran can pass on the current repository, and no cross-stage name differs.

#### Reviewer instructions (apply to every persona)

You are one of three independent reviewers of a PRE-EXECUTION plan. You are read-only: use Read, Grep, Glob and the codegraph tools only when the run-state line below says index_state=fresh; run no shell and edit nothing. Return your card as your final message (the orchestrator saves it).

Plan under review: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (254 lines, 16 tasks, 4 phases). Request it came from: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md`. The driving spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (1224 lines). Cross-stage files you may read: the stage 2 plan `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md`, the stage 3 plan `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md`, the shared brief `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/revision2-brief.md`, the first and second review reports `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116030453/REPORT.md` and `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/REPORT.md`.

This is the THIRD and final review. Check, in this order: (1) the earlier findings (first review F1 to F9, second review M-F1 to M-F10) are really fixed in the live plan text; (2) the revisions added no defect: task numbering, `Depends on:` lines, acceptance lines that a later task of the same package makes false (they must carry an end point), missing or wrong paths, contradictions with the shared brief or with the stage 2 plan (which reads this stage's outputs); (3) the plan against the spec: does it build every stage 1 deliverable and exit test the spec asks for (SPEC:945), and can each acceptance check be met on the current repository?

Grade every finding by consequence: BLOCKING means a requirement or check in the plan cannot be met, a wrong or missing result would follow, or data would be lost; NON-BLOCKING (minor) means wording, format or a real but harmless weakness. A blocking finding must name the task, quote the sentence, say what an executor following the plan would do wrong or fail to do, and give a repair. Verify every claim with a Read or Grep before you report it; never report from memory. Do not invent a finding to meet a quota, and a zero-finding result is valid only if you say what you checked.

Return format (under 7500 characters): `## Findings` with one block per finding: `id` (R<n>-F<k>), `blocking: yes|no`, `claim` (one or two sentences), `evidence` (file:line citations you re-read), `repair`; then `## Earlier findings check` (one line per earlier finding group: fixed or not, with the live line); then `## Verdict` (PASS or NEEDS-REVISION) with `confidence` (0 to 1) and the list of blocking ids; then one line `reviewer_model_self_report: <the model you are>`.

Persona lens: refactorer. Look for structural and cross-package defects: task numbering and dependency order, shared names (file names, command names, registry and scale-map grammar) that the stage 2, 3 and 4 plans read, acceptance lines a later task of this package makes false, and contradictions with the shared brief's decisions 1, 2, 4 and 5.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T19:09Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:32-116

````markdown
## Phase 1: Create the skill folder and its references

## Task 1: Create the skill folder entry file

Before creating any file, run the entry gate: the stage ledger `stage-requests/README.md` in PF must show an owner go for stage 1 with a date, and the stage 0 package's `./artifacts/stage0-summary-for-owner.md` (read by package id) must exist; when either is missing, create nothing and halt for the owner's Ruling. Then create `src/superclaude/skills/sc-review-severity/SKILL.md` (the folder does not exist today, confirmed). It states the purpose, which ref is read by whom (the table of spec section 9.1), the rule version `v2`, and "Delegate-only, no slash command", in the style of the existing `sc-bare-review` skill. Do not name any `src/superclaude/` path inside it.

Acceptance criteria:
- The stage ledger `stage-requests/README.md` in PF has an owner go for stage 1 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
- The stage 0 package's `./artifacts/stage0-summary-for-owner.md` (read by package id) exists.
- `src/superclaude/skills/sc-review-severity/SKILL.md` exists with frontmatter, the five refs named in spec section 9.1 (`refs/rule.md`, `refs/scale-map.md`, `refs/follow-up-ledger.md`, `refs/classifier-questions.md`, `refs/registry.yaml`) and the line "Delegate-only, no slash command".
- `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/SKILL.md` prints nothing.
- After `make sync-dev`, `make verify-sync` reports the new folder in sync.

## Task 2: Write the full rule with the pinned digest

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/rule.md`. It holds the full rule: the three blocking conditions, the Medium and Note classes, the counterfactual test and the table of spec section 4.2, the decision basis of section 4.3, the worked cases of section 5, the table-shape rule, the guardrails GR1 to GR12 of section 8.1 (GR5 names "highest severity wins" as the thing it does not re-create, so the file contains that phrase and the merge-rule scan allow-lists it), and the digest. The digest is the block of REQ-01 word for word, including REQ-02 (the unknown-consumer sentence), REQ-03 (the precedence sentence) and the cap sentence that today's `src/superclaude/output-styles/pragmatic.md` holds in its cap bullet ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings."), placed between the HTML-comment fence lines `review-severity:digest v2 begin` and `review-severity:digest v2 end`.

Acceptance criteria:
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude/skills/sc-review-severity` prints nothing (neither the digest nor any other text of the skill folder quotes the old sentence).
- `refs/rule.md` contains exactly one fenced digest whose last sentence equals the cap sentence of `src/superclaude/output-styles/pragmatic.md` word for word.
- The digest contains the sentences of REQ-02 and REQ-03.
- Every one of the 14 worked cases of spec section 5 appears with its verdict.
- `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/refs/rule.md` prints nothing.

## Task 3: Write the scale map

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3, in a single Markdown table whose columns are `family`, `defining file`, `labels`, `model` and `file kind`, because Tasks 9 and 12 read the table in code and the T4 test of Task 15 parses it. Three grammar rules fix what the code reads. First, `family` holds a short lowercase key that code looks a row up by: `lens-scale`, `implement-qa`, `spec-panel`, `stoprule`, `reflect`, `tasklist`, `roadmap-validate`, `card-convert`, `findings`, `auggie-review`, `pr-router` and `code-assigned` (one per family below). Second, `labels` holds each native label with its shared outcome as `LABEL=Outcome` pairs separated by semicolons (outcomes: Blocking, Medium, Note, or `Conditional` for a label whose outcome depends on a condition the table cannot test, for example spec-panel MAJOR, which is Blocking only when it names a concrete wrong outcome; the `model` cell states the condition in words), or the word `none` for a family with no native label. Third, `defining file` holds one path, or several paths separated by ` + ` when a family is defined in more than one file (the code-assigned row). `model` is either "graded by the three conditions" or "keeps its own model because <reason>". `file kind` is `repo` or `installed-only`. For a `repo` row the `defining file` cell holds the path relative to the `src/superclaude/` folder, written without that prefix (for example `agents/rf-qa.md`), so the installed file never names a `src/superclaude/` path; for an `installed-only` row it holds the `~/.claude/...` path of a file that exists only in an installed copy. The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale (defining file `agents/rf-qa.md`, not the retired task skill); the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family (`labels` is `none`; its defining files are `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py`).

The stoprule and `finding-grader` row has no defining file in the repository: the spec files both as installed-only (they exist under `~/.claude/` and not under `src/superclaude/`, and whether they ever move into `src/` is owner decision OD10, not decided here). That row is therefore marked `installed-only`, names `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`, and is exempt from the exists-in-repository line below and from T4 (Task 15 repeats the exemption). It cites no `.dev/` path.

Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" with one bullet per file: the path relative to `src/superclaude/` in backticks, then `allowed` or `exempt-by-retirement`. It lists by path only the files allowed to contain the three merge-rule phrases of spec section 10.3, and never writes those phrases or the old definition sentence, so the stage 3 scan test reads its allow-list from one place. The `allowed` entries are the auggie file (`skills/sc-auggie-review-protocol/SKILL.md`), `skills/sc-review-severity/refs/rule.md`, the six stage 4 files (`skills/tech-reference/SKILL.md`, `skills/readme/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/operational-guide/SKILL.md`, `templates/documents/agent_template_qa.md`, `templates/documents/agent_template_analysis.md`) and the two code files that hold the phrases and are not changed because they assign severity in code (`cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py`, out of scope by spec section 10.3). The `exempt-by-retirement` entries are the retired carriers `skills/task/SKILL.md`, `skills/task-builder/` (every file in the folder) and `agents/rf-task-builder.md`, with the sentence that the exemption ends when the retirement removes the file. No plugin path is listed: no plugin mirror of this skill folder is made by any package.

Acceptance criteria:
- `refs/scale-map.md` has a row for each of the 12 families with the five columns above, and each `repo` row names a defining file that exists in the repository under `src/superclaude/`.
- The stoprule and `finding-grader` row is marked `installed-only`, names the two `~/.claude/` paths, and is exempt from the exists-in-repository line above and from T4; the code-assigned row has `labels` equal to `none`.
- The `family` cells are the 12 keys above, the `labels` and `defining file` cells follow the second and third grammar rules, and the spec-panel row marks MAJOR as `Conditional`.
- The tasklist row states that Medium is blocking today on 9 lines of `skills/sc-tasklist-protocol/SKILL.md` (a re-count on 2026-11-16 by `grep -c -i "High or Medium\|High and Medium\|Medium (blocking)\|High/Medium"`; the spec lists 7 and the live count wins, re-counted when the task runs) and that no stage 1 to 4 task changes it.
- The `card_convert.py` row states that its word translator maps `important` and `medium` to non-blocking while `agents/rf-qa.md` treats IMPORTANT as blocking.
- The "Merge-rule allow-list" section exists and lists the auggie file, `refs/rule.md`, the six stage 4 files, `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed`, and `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` with the sentence that the exemption ends when the retirement removes the file; the plugin mirror is not listed.
- `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing.
- `grep -n -i "highest severity\|more severe rating\|higher severity" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing.

## Task 4: Write the follow-up ledger reference

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/follow-up-ledger.md` from spec sections 6.1 to 6.7: the flow, the ledger contract (metadata block, Items table with its columns, Notes table, Observations, Offers and Filings tables, item states, identity rules), the offer wording with consent binding (REQ-11), unattended behaviour (REQ-12), the filing path (OD15, REQ-13 to REQ-15), the location rule (REQ-07) and "resolve now" (6.7). Keep the cell codec of REQ-10 exactly: entity layer, no backslash before a pipe. The spec's table of item states has eight states and no `sweep-flagged`; the stage 2 package's sweep returns it, so this task defines it here as a ninth state: a Medium row the final-gate sweep would raise, recorded while the sweep's promotion switch is off and acted on only when a later change switches promotion on (the installed reference names no rollout stage). State that the end-of-run follow-up list is carried by the final review step of `/sc:implement`, which only records and prints it and asks nothing, that `tech-research` writes the ledger but neither sweeps nor offers, and that the once-per-run offer question belongs to the top-level session (through the output style) and to the consent-bound filing path (OD15), so a run never shows two offers. The file names no `.dev/` path, no `./artifacts/` path and no `src/superclaude/` path: the pr-submit exception of the location rule is written as "keeps its own report-only list" without the spec's gitignored-folder path, and the relation to the existing typed ledger names the `review ledger` command and the schema `review-ledger/1`, not their files.

Acceptance criteria:
- `refs/follow-up-ledger.md` contains the Items table columns of spec section 6.2 (`id`, `origin`, `tier`, `source`, `location`, `finding`, `evidence`, `rests_on`, `why_not_blocking`, `tags`, `proposed_fix`, `suggested_type`, `classifier`, `status`, `canonical_id`, `issue_url`).
- The offer wording of spec section 6.3 and the sentence "Nothing is filed until you answer." appear.
- The file states the three tags `consumer-unknown`, `unsettled` and `protected-risk-dispute` and that all three feed the single `show_user` count.
- The file lists the eight item states of spec section 6.2 and defines `sweep-flagged` as a ninth, and its `sweep-flagged` passage names no rollout stage.
- The file states that the `/sc:implement` final review step only records and prints the follow-up list, that the top-level session is the one owner of the offer, and that `tech-research` neither sweeps nor offers.
- `grep -n "\.dev/\|artifacts/\|src/superclaude" src/superclaude/skills/sc-review-severity/refs/follow-up-ledger.md` prints nothing.

## Task 5: Write the classifier question reference

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/classifier-questions.md`: the six decisive questions S, W, E, M, C, D of spec section 7.2 with the S wording "in a way the task did not ask for", the code-supplied input each needs, the Option Q replacement for D at upstream gates, and the optional explanation questions T, F, I and G (they feed no cell of the truth table). Add a version line `question-set v1`. State that M, C and E are asked only when code supplies their inputs, and say why in words (they were at chance in the five-run text-only test); this file cites no `.dev/` or `./artifacts/` path.

Acceptance criteria:
- `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing: no file of the skill folder cites a `.dev/` or `./artifacts/` path.
- `grep -rn "src/superclaude" src/superclaude/skills/sc-review-severity` prints nothing: no file of the skill folder names a `src/superclaude/` path.
- `refs/classifier-questions.md` has the six questions with a "Needs from code" column and the line `question-set v1`.
- No question text contains the word "blocking" (`grep -in blocking` over the question table rows prints nothing).
- The file states that a failed or skipped answer is UNSET and never N.

## Task 6: Write the carrier registry with every digest row set to legacy

Depends on: Task 2, Task 3

Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. Each row has the logical path relative to the install root, a `kind` (`digest`, `canonical`, `pointer-only` or `installed-only`), surfaces (source, installed, project `.claude/`, or `installed-only`; the word `plugin` appears only on the two `pointer-only` rows whose hand-kept plugin twins already exist), rollout stage, a state (`legacy` for a digest row until its file is moved), and an own-scale flag. Rows of kind `digest`, exactly the 11 definition carriers of spec section 10.1: `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`. One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; its surfaces are source, installed and project `.claude/`, with no plugin mirror because IronClaude is not installed as a plugin). Two rows of kind `pointer-only` (a pointer plus the ledger sentence, no digest): `rules/prompts/document_review_loop_prompts.md` and `commands/sc/spec-panel.md` (source `commands/spec-panel.md`). Five rows of kind `installed-only`: `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. `skills/task/SKILL.md` gets no row: it is a retired carrier, not edited by any package and listed only as `exempt-by-retirement` in the allow-list of Task 3, and it is not a digest carrier. `templates/documents/agent_template_analysis.md` gets no row either: it holds no definition sentence, only a merge-rule line, which the stage 4 package edits as text only.

Acceptance criteria:
- `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
- It has exactly 11 rows of kind `digest` (each with a source path that exists, state `legacy`, stage 3 for `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md`, stage 4 for the rest), 1 of kind `canonical`, 2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all.
- No row names `skills/task/SKILL.md`, `skills/task-builder/` or `agents/rf-task-builder.md`, and the `canonical` row lists no plugin surface.
- With `registry.yaml` in place, the two folder greps of Task 5 (`\.dev/\|artifacts/` and `src/superclaude` over `src/superclaude/skills/sc-review-severity`) still print nothing.

````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:216-254

````markdown
## Phase 4: Add the install check, the drift tests and the exit summary

## Task 14: Add the install check for digest versions

Depends on: Task 6

Add `_check_review_severity_digests` to `src/superclaude/cli/doctor.py` and call it from `run_doctor` (REQ-27). It compares the digest versions held by the installed carriers with the packaged registry of `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, reading the packaged registry and not an installed copy (an installed skill folder is skipped once present, so an installed `registry.yaml` can be stale), and considers only rows of kind `digest`. Add tests to `tests/unit/test_cli_doctor.py`; keep `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`) passing because `run_doctor` must stay read-only.

Acceptance criteria:
- A test in `tests/unit/test_cli_doctor.py` builds an installed tree with a stale digest version and asserts the check reports the mismatch (T13).
- `uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py -v` passes.
- With every registry row at `legacy` and every installed carrier legacy, the check reports no mismatch.
- `make doctor` still runs and exits as before.

## Task 15: Add the registry drift tests

Depends on: Task 2, Task 3, Task 6

Create `tests/skills/test_review_severity_registry.py` for T1 (every row of kind `digest` holds, in its file, exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; a row at `legacy` is accepted; the `canonical` row holds the source digest), T2 (a reverse scan of the tracked `src/` and `plugins/` trees, the plugin tree being scanned because hand-kept twins already exist there and no row names a plugin path, fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; `canonical` and `pointer-only` rows count as registered; strict mode is the module constant `STRICT_T2` in `tests/skills/test_review_severity_registry.py`, `False` in this phase, which the stage 4 package sets to `True`), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`; the check that no carrier contains `src/superclaude` applies to `digest` and `canonical` rows only; a `pointer-only` row is checked for pointer order only, and only once its pointer is present; an `installed-only` row is not checked by T3; and the test never reads `~/.claude`), T4 (each `repo` row of `refs/scale-map.md` names its existing files under `src/superclaude/`, resolved from the table's `defining file` column, where a cell with several paths joined by ` + ` is split and every path must exist, and each native label of its `labels` column is present in at least one of those files, compared without regard to case, with a label whose outcome is `Conditional` checked the same way; a row whose `labels` is `none` skips the label check; an `installed-only` row, today the stoprule and `finding-grader` row, is exempt from both checks and is only checked to be marked `installed-only` with `~/.claude/` paths, and the test never reads `~/.claude`) and T14 (a `digest` row at `v2` holds the precedence sentence).

Acceptance criteria:
- A temporary-tree test shows each T3 exemption: a `pointer-only` row whose file holds a `src/superclaude` path passes the path check, a `pointer-only` row without its pointer yet passes, and a `digest` row whose file holds such a path fails.
- `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all `digest` rows at `legacy`.
- A test flips one `digest` row to `v2` without editing its file and fails, which shows T1 can fail; a `pointer-only` row at any state does not fail T1.
- The reverse scan accepts `refs/rule.md` (it has a `canonical` row) and reports a file that holds the definition sentence and is absent from the registry, using a temporary tree in the test.
- A temporary-tree test shows each T4 exemption: an `installed-only` row naming `~/.claude/` paths passes without any file in the tree, a `labels` value of `none` skips the label check, and a `repo` row whose file is missing or lacks one of its labels fails; a row with two files joined by ` + ` passes when each file exists and each label is in at least one of them, and fails when one of the two files is missing; a `Conditional` label is checked like any other label.
- The T4 test reads the same word, `installed-only`, in the `file kind` column that Task 3 writes for the stoprule and `finding-grader` row, so the exemption of the two tasks is one rule.

## Task 16: Write the stage 1 exit summary for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15

Write `./artifacts/stage1-summary-for-owner.md`, the one file the owner reads before saying go for stage 2. For each of Tasks 1 to 15 give the files it created or changed and the command it ran with its observed pass count (for tests, the pytest summary line). List every file the package created. Show that no carrier was edited: `git diff --stat HEAD -- src/superclaude/output-styles src/superclaude/agents src/superclaude/templates src/superclaude/rules src/superclaude/commands src/superclaude/skills/task src/superclaude/skills/task-builder src/superclaude/skills/tech-research src/superclaude/skills/sc-implement-protocol src/superclaude/core src/superclaude/cli/review/ledger.py plugins` prints nothing. State the reuse-audit verdict of Task 7 for `follow_ups.py` against `ledger.py` and the registry counts (11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only`), so the owner can answer the open question on the follow-up ledger from evidence. List the open items and the owner decisions this stage touches (OD3 for any later external judge; OD4 authority none; OD10 for the two installed-only stoprule files). End with the sentence that the owner's go for stage 2 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/stage1-summary-for-owner.md` names, for each of Tasks 1 to 15, the files and the observed result, and each named file exists.
- The file shows the carrier `git diff --stat HEAD` command above with empty output.
- The file states the reuse-audit verdict and the registry counts.
- The file lists OD3, OD4 and OD10 and the open items, and ends with the sentence that the owner's go for stage 2 is given in chat and not by this file.
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/revision2-brief.md:11-18

````markdown
## Shared design decisions (apply in every stage; do not reopen them)

1. **Retired carriers are not edited.** No task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for those. They keep today's text until the owner's retirement removes them. The stage 1 "Merge-rule allow-list" section in `refs/scale-map.md` lists them as `exempt-by-retirement` (by path only, no merge-rule phrase and no old definition sentence written in it), with the sentence that the exemption ends when the retirement removes the file. Tests that exist only to pin those files are not re-pinned by these plans; the retirement owns them. When a test pins both a retired and an active carrier, the plan re-pins the active carrier's part only.
2. **The follow-up carrier is `/sc:implement`'s final review step, record and print only.** Verified facts the plan must respect: `src/superclaude/skills/sc-implement-protocol/refs/qa.md` keeps its own scale and is NOT edited (it is on the not-built list); `qa.md` line 225 says the final summary "is informational and never asks the user anything"; `qa.md` lines 276 to 288 close the list of interrupts ("No other path may stop automation or prompt the user"). So the edit goes into `src/superclaude/skills/sc-implement-protocol/SKILL.md` (final summary instructions) and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (archive gate, run before the package moves in step 6): one read-only call of the sweep command over the follow-up ledgers the package's review loops wrote, and a printed list in the final summary with the plain-English line naming how the owner can file them. It asks nothing and prompts nothing. The once-per-run offer question stays with the top-level session through the output style (the `pragmatic.md` Medium rule, changed from per loop to per run in stage 3) and with the consent-bound filing path (OD15); stage 2 adds no question to `/sc:implement`. Say this in the plan in one sentence so a reviewer sees the choice.
3. **tech-research** (`src/superclaude/skills/tech-research/SKILL.md`) is an active workflow and keeps its ledger-writing edit as already planned (no sweep, no offer there).
4. **Plugin surface.** IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin. Do not create any new plugin surface: no `plugins/superclaude/skills/sc-review-severity/` mirror, no plugin parity test (T15), no `canonical` registry row for a plugin path. Existing hand-kept plugin twins (`plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`) are touched only where an existing test pins them and the active source carrier changes; say so in the plan. The registry keeps exactly 11 `digest` rows, 1 canonical, 2 pointer-only and 5 installed-only unless the review findings below require a different count; if you change a count, change it everywhere and say why. OPEN-QUESTIONS.md section 3.4 records that this reassessment is the plan author's and the owner has not confirmed removing plugin parity.
5. **Ledger decision (owner question 5).** Version 1 keeps `follow-ups.md` as a separate file; no mapping to `review-ledger/1` rows is built in these plans. The stage 1 reuse-audit result decides whether a mapping is ever added. No plan task replaces or edits `src/superclaude/cli/review/ledger.py`.
6. **Do not use `/sc:implement`, commit or push.** Stage with `git add .dev/tasks` only. Never stage under `.claude/`.
````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:162-162

````markdown
Record every kept mechanical gate in a section titled `Kept mechanical gates` at the end of `refs/scale-map.md` (create it on the first keep; do not touch the `Merge-rule allow-list` section that Task 13 reads), one bullet per gate in the form: path relative to `src/superclaude/`, the gate's quoted words, the condition it maps to, the reason. The bullets never write a `src/superclaude` path or the three merge-rule phrases (stage 1 acceptance lines scan the file for them). Set the registry row of `agents/rf-qa.md` to `v2`. Run `make sync-dev` afterwards.
````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:240-245

````markdown
Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude` (read only; nothing there is edited), matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`, one bullet per path (relative to `src/superclaude/`) with the status `allowed` or `exempt-by-retirement`: as stage 1 wrote it, `skills/sc-auggie-review-protocol/SKILL.md`, `skills/sc-review-severity/refs/rule.md`, the two code files `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` and, until the stage 4 package, the six stage 4 files (`skills/tech-reference/SKILL.md`, `skills/readme/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/operational-guide/SKILL.md`, `templates/documents/agent_template_qa.md` and `templates/documents/agent_template_analysis.md`) are `allowed`; the retired carriers `skills/task/SKILL.md`, `skills/task-builder/` (every file in the folder) and `agents/rf-task-builder.md` are `exempt-by-retirement`. A row marked `exempt-by-retirement` allows hits while its file exists and is not an error once the retirement has removed the file; every `allowed` row names a file that must exist. The stage 4 package removes each of its six files from the allow-list in the same change that edits it. No stage builds a plugin mirror of the skill folder, so the allow-list names no plugin path. The `Kept mechanical gates` section that Tasks 7 and 8 add to `refs/scale-map.md` is a different section and the scan does not read it.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 7 to 9, with no hit in `src/superclaude/cli/` counted and the two hits in `src/superclaude/skills/task/SKILL.md` accepted only through its `exempt-by-retirement` row.
- A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
- The allow-list is read from `refs/scale-map.md`: a test fails when an `allowed` row names a file that does not exist, and a test shows an `exempt-by-retirement` row whose file or folder is missing does not fail.
````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:57-57

````markdown
Read `src/superclaude/cli/review/__init__.py` (it registers nine subcommand modules today and none for follow-ups, the safety route or the sweep, so a skill can name no working command until this task adds one) and the stage 1 modules `follow_ups.py` and `safety_route.py`, and write `./artifacts/follow-ups-cmd-wiring.md` naming each stage 1 function the commands call and stating whether the stage 1 safety route saves the `protected-risk-dispute` tag itself or only returns the rows. If a test of this task shows that the stage 1 writer itself clears a tag or resets `capture_state` on a later write, that is a stage 1 defect: record it in the wiring file and stop for the owner's Ruling (stage 1 owns `follow_ups.py`; this package does not edit it). Create `src/superclaude/cli/review/follow_ups_cmd.py` exporting `command` (a click group named `follow-ups`), add `"follow_ups_cmd"` to the tuple in `__init__.py`, and give it four subcommands. `write --ledger <path> --report <reviewer report> (repeatable) --run-id <id> --gate-id <id> [--expected-revision <n>]` imports the non-blocking rows of reviewer report tables through the stage 1 writer (the run owner is the only writer). Table layout: the command finds a table whose header row holds a `Severity` column (the native label) and the two columns `rests_on` and `why not blocking`, and reads the location from the `Section` or `Location` column and the finding text from the `Finding` or `Issue` column, all by header name, so both reviewer layouts (`# | Severity | Section | Finding | Proposed Fix` and `# | Severity | Location | Issue | Required Fix`, each with the two fields as last columns) and the analyst section that Task 4 adds parse the same way. The tier of a row is the shared outcome that the lens-scale row of `refs/scale-map.md` gives its native label, read at run time with no second copy in the command; Blocking rows are never written; a Medium row without `why not blocking` is refused by the writer and reported. A report that cannot be read, or holds no table with those columns, sets `capture_state: incomplete` with the reason, and `incomplete` stays after any later successful `write` to the same ledger (a later write never resets it to `complete`; a new run starts a new ledger). `safety --ledger <path> [--judge-answers <file>] [--unattended]` runs the stage 1 safety route over the ledger and saves the `protected-risk-dispute` tag on each row it flags through the stage 1 writer (the command calls the writer itself when the route only returns rows), so the tag is in the ledger after the call and after any later `write`; attended output names the rows for the person prompt, and in both modes its last line is `worker_status_signal: partial` when the ledger holds one or more rows tagged `protected-risk-dispute` and `worker_status_signal: none` otherwise; this line is the signal that Task 5 maps to `worker_status: partial`. `--judge-answers` reads recorded answers only, through the stage 1 `FixtureJudge`. `sweep --root <dir> | --ledger <path> (repeatable) [--deliverable <path> (repeatable)] --kind auto|report|spec|tasklist|code|other [--promote] [--write] [--output <file>]` first prints the line `ledgers found: N` (with `--root`, every `follow-ups.md` under that folder; zero is valid and the command stops after that line and exits 0), then for each ledger its path relative to `--root`, its counts (`follow_up`, `note`, `show_user`) and its `show_user` rows (id, tier, location, finding) first, then calls Task 1's sweep and prints the flagged rows (id, deliverable, section) and the skipped count; it writes the same text to `--output` when given, exits 0 whenever it ran (flagged rows are information) and non-zero only when it cannot run. This single output is the producer of the printed follow-up list of Task 3, so Task 3 needs no second command. `summary --ledger <path>` prints exactly the three worker-contract keys as YAML (`follow_up_ledger`, `follow_up_counts` with `follow_up`, `note` and `show_user`, `follow_up_capture_state`); this is the named producer of those keys for Task 5. No subcommand calls `gh`, a network or a live judge. Create `tests/review/test_review_follow_ups_cmd.py`.
````

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-002: Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summar | T1 | covered, task 1 (0.818) | source.md:3 |
| INF-003: and after the stage ledger row for stage 0 has the package id | T1 | covered, task 1 (1.0) | source.md:3 |
| INF-009: State this package is stage 1: new files only, no carrier edited, every registry `digest`  | T1 | covered, task 6 (0.769) | source.md:11 |
| INF-010: The next package (stage 2) starts only after the owner's go in chat. | T1 | covered, task 16 (0.667) | source.md:11 |
| INF-012: The "Merge-rule allow-list" section lists files by path and never writes the three merge-r | T1 | covered, task 3 (0.929) | source.md:12 |
| INF-013: At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. | T1 | covered, task 3 (0.9) | source.md:12 |
| INF-014: Say in the task that the plugin mirror is added in stage 4, not here. | T1 | covered, task 3 (0.625) | source.md:12 |
| INF-015: `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) | T1 | covered, task 2 (0.875) | source.md:13 |
| INF-016: never quotes the old definition sentence "Grade every review finding as blocking or minor" | T1 | covered, task 2 (0.8) | source.md:13 |
| INF-017: state this as an acceptance line (`grep` of the old sentence over the skill folder prints  | T1 | covered, task 2 (0.8) | source.md:13 |
| INF-018: No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts | T1 | covered, task 5 (0.857) | source.md:14 |
| INF-019: State the M, C and E input rule in words. | T1 | covered, task 5 (0.714) | source.md:14 |
| INF-020: Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 row | T1 | covered, task 6 (0.923) | source.md:15 |
| INF-021: Say the analysis template is not a carrier row (merge-rule text only in stage 4). | T1 | covered, task 6 (0.667) | source.md:15 |
| INF-022: T3's `src/superclaude` check applies to `digest` and `canonical` rows only | T1 | covered, task 15 (1.0) | source.md:16 |
| INF-023: `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointe | T1 | covered, task 15 (1.0) | source.md:16 |
| INF-024: the test never reads `~/.claude` | T1 | covered, task 15 (1.0) | source.md:16 |
| INF-025: T2 is non-strict (strict only in stage 4). | T1 | covered, task 15 (0.8) | source.md:16 |
| INF-028: New final task: stage 1 exit summary for the owner. | T1 | covered, task 16 (0.625) | source.md:18 |
| INF-029: Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and it | T1 | covered, task 16 (0.667) | source.md:18 |
| INF-030: the list of files created | T1 | covered, task 16 (1.0) | source.md:18 |
| INF-031: a statement that no carrier was edited (`git diff --stat` over carriers is empty) | T1 | covered, task 16 (0.75) | source.md:18 |
| INF-032: the open items, and the sentence that the owner's go for stage 2 is given in chat and not  | T1 | covered, task 16 (1.0) | source.md:18 |
| INF-060: Task 3 lists `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md | T1 | covered, task 3 (1.0) | source.md:35 |
| INF-061: the exemption ends when the retirement removes the file | T1 | covered, task 3 (1.0) | source.md:35 |
| INF-062: Task 16's carrier diff adds the task-builder folder. | T1 | covered, task 16 (0.625) | source.md:35 |
| INF-063: `/sc:implement`'s final review step records and prints only, the offer stays with the top- | T1 | covered, task 4 (0.938) | source.md:36 |
| INF-064: `tech-research` writes the ledger and neither sweeps nor offers | T1 | covered, task 4 (1.0) | source.md:36 |
| INF-066: Task 3 no longer says a plugin mirror comes in stage 4 | T1 | covered, task 3 (0.667) | source.md:37 |
| INF-067: Task 6's canonical row has no plugin surface | T1 | covered, task 15 (0.857) | source.md:37 |
| INF-068: Task 16 diff adds `plugins`. | T1 | covered, task 16 (0.8) | source.md:37 |
| INF-069: Registry counts unchanged: 11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only | T1 | covered, task 6 (0.846) | source.md:37 |
| INF-084: Task 15 names the strict switch of T2 as the constant `STRICT_T2` (default `False`); the s | T1 | covered, task 15 (0.867) | source.md:55 |
