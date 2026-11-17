# Reviewer brief 3 (refactorer)

## T1 card excerpt

## Check (b): new defects introduced by the revision

Mechanical structure (batch d01 to d05): 16 "Acceptance criteria:" labels for 16 tasks; `Depends on` targets are all lower task numbers; no checkbox or numbered-list lines; no absolute paths or `.dev/tasks/to-do/` prefixes; no "never staged" wording.

N1 (candidate, blocking). PLAN:125 acceptance line "lists only `follow_ups.py`" cannot be met as written. `grep -rln` also lists binary files, and `src/superclaude/cli/review/__pycache__/` holds `*.cpython-311.pyc` and `*-pytest-9.2.0.pyc` for every module (batch c01 and d20: the same grep for "ledger" lists 10 `.pyc` files besides the 5 `.py` files). Task 7's first acceptance line runs pytest, which writes `follow_ups.cpython-311*.pyc`, and from Task 10 on the importers' `.pyc` files also contain the name. The check lists extra paths whatever the code does. (`.gitignore:2` ignores `__pycache__/`, so the fix is to restrict the grep to `*.py`.)

N2 (candidate, non-blocking). Task 9 (PLAN:146) makes `ReviewerJudge` read the reviewer's label "through the scale map" from the `labels` column of `refs/scale-map.md`, but the same word has different outcomes in different rows (tasklist Medium is Blocking, `card_convert.py` medium is Note, rf-qa MINOR, auggie Medium). The plan never says which family row a finding's label is read against (the ledger `source`/`origin` columns could key it); Task 12's disagreement matrix (PLAN:184) has the same gap. An implementer must invent the key.

N3 (candidate, non-blocking). Task 3 fixes one outcome per label (PLAN:62: Blocking, Medium, Note), but SPEC:739 gives spec-panel MAJOR as "Blocking only when it names a concrete wrong outcome, else Medium" and SPEC:738 maps `false-claim` more broadly than the rule; a single `LABEL=Outcome` pair cannot hold a conditional mapping.

N4 (candidate, non-blocking). REQ-09 (SPEC:396, cross-run matching of declined, filed and resolved rows) is not named in Task 7 (PLAN:120) or in any T7 failure condition, although the identity tuple is.

N5 (candidate, minor). Task 8 (PLAN:132) takes the repository from `origin_repo.py`, which is a script, not an importable package (`tests/issue_watch/test_origin_parity.py:3`; `cli/issue_watch/launch.py:206` copies its rules), and says nothing about how code calls it or how the tests fake it.

N6 (candidate, minor). Task 4 copies spec sections 6.1 to 6.7; SPEC:485 mentions `.dev/pr-monitor/`, which Task 5's folder-wide grep (PLAN:97) forbids; Task 4 comes first, so the executor must drop it from the copy. The first review dropped this as an executor-avoidable point.

## Check (c): plan against the spec's stage 1 row (SPEC:945)

Stage 1 exit tests T1 to T4, T6 to T8, T11 to T13, T17: T1, T2, T3, T4, T14 in Task 15; T6, T11, T12a in Tasks 9 to 11; T12b and T17 in Task 13; T7 in Task 7; T8 in Task 8; T13 in Task 14. The skill folder, registry (19 rows: 11 digest, 1 canonical, 2 pointer-only, 5 installed-only), ledger codec and writer, fixture judge, property tests and install check are all present. No carrier is edited. Shared decisions 1 (retired carriers), 2 (follow-up carrier), 4 (no plugin surface) and 5 (ledger) are visible at PLAN:24, 25, 26 and 120. Registry paths named in Task 6 exist (batch d11, d12, d13).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T17:50:54Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/artifacts/wave1a-checks.md (orchestrator read-only check results; re-run what you rely on)

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md (the merged spec the plan implements; read-only; the stage 1 row is SPEC:945; sections 6, 7, 9, 11.2 and 12 are the ones the plan builds)

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:1-32

```text
1: ---
2: schema: workflow-plan/1.2
3: source: ./source.md
4: strategy: systematic
5: depth: standard
6: slug: TASK-WF-blockerStage1-20261116-030154
7: version: "1"
8: priority: Medium
9: created_date: "2026-11-16"
10: ---
11: 
12: # Stage 1 plan: offline scaffold for the blocker classification work (issue #552)
13: 
14: Source: ./source.md
15: Goal: Create the new skill folder, its references, the registry, the ledger and classifier modules, the classify command, the safety route, the install check and their tests, all offline; no review-loop carrier is edited and every registry `digest` row stays `legacy`. The owner reads `./artifacts/stage1-summary-for-owner.md` and decides whether to say go for stage 2.
16: 
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
20: - One package, one stage. This is stage 1 of five packages (one plan per stage, the owner's decision of 2026-11-16). It creates new files only (the skill folder, new CLI modules, new tests, one doctor check) and edits no review-loop carrier (`pragmatic.md`, agents, templates, rule prompts, the task skill, tech-research, `sc-implement-protocol`, `WORKER-CONTRACT.md`); every registry `digest` row stays `legacy`. It runs only after the stage 0 package is done, the owner has read the stage 0 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Stage 2 starts only after the owner reads this package's summary and says go.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, any change to the cap of 2 fix cycles, and any edit or replacement of `src/superclaude/cli/review/ledger.py`.
23: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
24: - Retired carriers (owner decision of 2026-11-16: `/sc:task` and task-builder are being retired). No task of this program edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for those; they keep today's text until the retirement removes them. Task 3 lists them in the "Merge-rule allow-list" section as `exempt-by-retirement` (by path only), and that exemption ends when the retirement removes the file. Tests that exist only to pin those files are not re-pinned here; a test that pins both a retired and an active carrier is re-pinned for the active carrier's part only.
25: - Follow-up carrier. The end-of-run follow-up list is carried by the final review step of `/sc:implement`, which records and prints only. `refs/qa.md` of that skill is not edited (it keeps its own scale and its final summary "never asks the user anything"), and the once-per-run offer question stays with the top-level session through the output style and with the consent-bound filing path (OD15), so this program adds no question to `/sc:implement`. `tech-research` is an active workflow that writes the ledger and neither sweeps nor offers. Stage 1 edits none of these files.
26: - Plugin surface. IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin, so this program creates no plugin surface: no `plugins/superclaude/skills/sc-review-severity/` mirror, no plugin parity test and no `canonical` registry row for a plugin path. The two existing hand-kept plugin twins (`plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`) are touched only where an existing test pins them and the active source carrier changes; this package touches neither. The owner has not confirmed removing plugin parity (the program's open-questions file, section 3.4); this is the plan author's reassessment.
27: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
28: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; keep everything under the project `.claude/` folder out of `git add` (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
29: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
30: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes tells a reader to keep `.dev/tasks/` out of `git add`. Staging is not committing.
31: 
32: ## Phase 1: Create the skill folder and its references
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:44-56

```text
44: 
45: ## Task 2: Write the full rule with the pinned digest
46: 
47: Depends on: Task 1
48: 
49: Create `src/superclaude/skills/sc-review-severity/refs/rule.md`. It holds the full rule: the three blocking conditions, the Medium and Note classes, the counterfactual test and the table of spec section 4.2, the decision basis of section 4.3, the worked cases of section 5, the table-shape rule, the guardrails GR1 to GR12 of section 8.1 (GR5 names "highest severity wins" as the thing it does not re-create, so the file contains that phrase and the merge-rule scan allow-lists it), and the digest. The digest is the block of REQ-01 word for word, including REQ-02 (the unknown-consumer sentence), REQ-03 (the precedence sentence) and the cap sentence that today's `src/superclaude/output-styles/pragmatic.md` holds in its cap bullet ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings."), placed between the HTML-comment fence lines `review-severity:digest v2 begin` and `review-severity:digest v2 end`.
50: 
51: Acceptance criteria:
52: - `grep -rn "Grade every review finding as blocking or minor" src/superclaude/skills/sc-review-severity` prints nothing outside the one fenced digest's own text (the digest does not quote the old sentence either).
53: - `refs/rule.md` contains exactly one fenced digest whose last sentence equals the cap sentence of `src/superclaude/output-styles/pragmatic.md` word for word.
54: - The digest contains the sentences of REQ-02 and REQ-03.
55: - Every one of the 14 worked cases of spec section 5 appears with its verdict.
56: - `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/refs/rule.md` prints nothing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:90-111

```text
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
101: 
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

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:207-231

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
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/artifacts/codegraph-grounding.md:34-47

```text
34: ## Revision 2
35: 
36: Re-checked 2026-11-16 (no code symbol changed; the index does not cover Markdown, so existence and phrase checks used `test -e`, `grep` and `git ls-files`, run from the repository root in one read-only batch):
37: 
38: - `test -e` over 11 paths named by the revision: all exist (`src/superclaude/cli/roadmap/remediate_parser.py`, `src/superclaude/cli/pipeline/fmea_classifier.py`, `src/superclaude/skills/task/SKILL.md`, `src/superclaude/skills/task-builder`, `src/superclaude/agents/rf-task-builder.md`, `src/superclaude/cli/review/ledger.py`, `plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`, `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, and the installed `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`).
39: - `test -e` over 5 paths that must be absent: all absent (`src/superclaude/cli/review/lint_cmd.py`, `src/superclaude/cli/review/estimate_cmd.py`, `src/superclaude/skills/sc-spec-panel-stoprule-protocol`, `src/superclaude/agents/finding-grader.md`, `plugins/superclaude/skills/sc-review-severity`).
40: - `git ls-files src plugins | grep -i -E "stoprule|finding-grader"` prints nothing: the stoprule rubric and `finding-grader` have no tracked copy under `src/` or `plugins/` (the tracked copies sit under `.dev/experiments/`), which is why their scale-map row is `installed-only`.
41: - `grep -rl -i "highest severity\|more severe rating\|higher severity" src --include=*.md --include=*.py` lists 13 files: `agents/rf-analyst.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `cli/pipeline/fmea_classifier.py`, `cli/roadmap/remediate_parser.py`, `skills/operational-guide/SKILL.md`, `skills/readme/SKILL.md`, `skills/sc-auggie-review-protocol/SKILL.md`, `skills/task/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/tech-reference/SKILL.md`, `templates/documents/agent_template_analysis.md` and `templates/documents/agent_template_qa.md` (paths relative to `src/superclaude/`). The allow-list of Task 3 now covers the auggie file, the six stage 4 files and the two code files; `skills/task/SKILL.md` is the one retired carrier among them.
42: - `src/superclaude/cli/review/__init__.py` lists nine module names in the subcommand tuple; seven modules exist (`panel_cmd`, `merge_cmd`, `ledger_cmd`, `telemetry_cmd`, `cluster_cmd`, `verify_cmd`, `manifest_cmd`).
43: - `git diff --stat HEAD` over the carrier paths of Task 16 (plus `plugins` and `ledger.py`) prints no line today.
44: - `plugins/superclaude/skills/` holds four skills (`confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`), so no existing plugin test requires a mirror of a new skill folder.
45: - `uv run python /tmp/gate_check.py` from the repository task folder: the stage 1 package prints PASS (16 tasks, 4 phases).
46: 
47: Findings: F1 applied (Task 7 end point and allowed importers); F2 applied, option (a) (Task 3 and Task 15 T4 `installed-only` exemption); F3 applied (allow-list lists `remediate_parser.py` and `fmea_classifier.py`; `stage3-request.md` line 14 edited to match); F4 applied (decision sentence in Task 7, audit verdict in Task 16); F5 applied (columns, path root, `none` labels, Task 3 dependencies in Tasks 9, 12 and 15); F6 and F7 applied (Task 10 depends on Task 7; `run_questions` in Task 9 and `questions_to_ask` in Task 10; the safety-route half of T12 moved to Task 13); F8 applied (full grep path; seven review subcommands named); F9 applied (`sweep-flagged` defined as a ninth state, no rollout stage named). Decisions 1, 2, 4 and 5 applied as listed in the Revision 2 section of the stage request. Not applied: none.
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

Persona instructions: Your lens: structure and tech debt of the plan: task numbering and dependency order, whether an executor following the tasks in order can meet every acceptance line (check each grep, count and 'exists' line against later tasks), paths that do not exist, duplicated or contradictory instructions, and the plan against the spec.
