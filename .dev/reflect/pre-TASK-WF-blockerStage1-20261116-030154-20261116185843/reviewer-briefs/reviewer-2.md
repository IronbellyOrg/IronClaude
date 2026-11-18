# Reviewer 2 brief (persona: qa; model class: haiku)

## T1 card excerpt
#### Coverage (Step 1B)

Pass 1 found 9 parsed rows: R-001 to R-008 are recommendation labels of the first two reviews (false positives of the ID regex, source.md lines 26 to 50) and REQ-09 is a real spec requirement (Task 7 names it, PLAN:124). Pass 2 (requirements-analyst) gave 84 quote-pinned rows; 35 lie inside a parsed span (parsed wins) and 49 were kept; containment matched 38 of 49; the 11 misses are mapped by hand in `artifacts/inferred-table.md` (every one is a Constraints line or a provenance line). `coverage_pct` (parsed only) 0.1111, `coverage_pct_union` 0.6724, `S_dev_density` 0.3276; the parse-density guard fires (49 inferred > 9 parsed).

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

#### Reviewer instructions (apply to every persona)

You are one of three independent reviewers of a PRE-EXECUTION plan. You are read-only: use Read, Grep, Glob and the codegraph tools only when the run-state line below says index_state=fresh; run no shell and edit nothing. Return your card as your final message (the orchestrator saves it).

Plan under review: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (254 lines, 16 tasks, 4 phases). Request it came from: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md`. The driving spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (1224 lines). Cross-stage files you may read: the stage 2 plan `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md`, the stage 3 plan `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md`, the shared brief `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/revision2-brief.md`, the first and second review reports `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116030453/REPORT.md` and `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/REPORT.md`.

This is the THIRD and final review. Check, in this order: (1) the earlier findings (first review F1 to F9, second review M-F1 to M-F10) are really fixed in the live plan text; (2) the revisions added no defect: task numbering, `Depends on:` lines, acceptance lines that a later task of the same package makes false (they must carry an end point), missing or wrong paths, contradictions with the shared brief or with the stage 2 plan (which reads this stage's outputs); (3) the plan against the spec: does it build every stage 1 deliverable and exit test the spec asks for (SPEC:945), and can each acceptance check be met on the current repository?

Grade every finding by consequence: BLOCKING means a requirement or check in the plan cannot be met, a wrong or missing result would follow, or data would be lost; NON-BLOCKING (minor) means wording, format or a real but harmless weakness. A blocking finding must name the task, quote the sentence, say what an executor following the plan would do wrong or fail to do, and give a repair. Verify every claim with a Read or Grep before you report it; never report from memory. Do not invent a finding to meet a quota, and a zero-finding result is valid only if you say what you checked.

Return format (under 7500 characters): `## Findings` with one block per finding: `id` (R<n>-F<k>), `blocking: yes|no`, `claim` (one or two sentences), `evidence` (file:line citations you re-read), `repair`; then `## Earlier findings check` (one line per earlier finding group: fixed or not, with the live line); then `## Verdict` (PASS or NEEDS-REVISION) with `confidence` (0 to 1) and the list of blocking ids; then one line `reviewer_model_self_report: <the model you are>`.

Persona lens: qa. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check that every stage 1 exit test and every stage 1 deliverable of the spec has a task whose acceptance line can pass.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T19:09Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:1-55

````markdown
# Stage 1 plan request: offline scaffold for the blocker classification work (issue #552)

Second of five plan packages (see `stage-requests/README.md` for the one-plan-per-stage decision and the decisions that apply to every stage). Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summary-for-owner.md` and said go in chat, and after the stage ledger row for stage 0 has the package id. This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-loop carrier.

## Base text

Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 2, stage 1; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward. Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-built list, the classifier facts (M, C and E run only with code-supplied inputs; the "M or C is Y gives BLOCKING" row is never enabled; confidence is an ordinal band), pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only. The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation) is read by package id.

## Changes to apply

- **Constraints.** State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. The next package (stage 2) starts only after the owner's go in chat. Drop the base plan's Phase 3 to 5 gate prose.
- **Task 13 (scale map).** The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definition sentence. At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. Say in the task that the plugin mirror is added in stage 4, not here.
- **Task 12 (rule).** `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) but never quotes the old definition sentence "Grade every review finding as blocking or minor" outside the digest's own fence history; state this as an acceptance line (`grep` of the old sentence over the skill folder prints nothing).
- **Task 15 (classifier questions) and all refs.** No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path (acceptance: `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing). State the M, C and E input rule in words.
- **Task 16 (registry).** Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). Say the analysis template is not a carrier row (merge-rule text only in stage 4).
- **Task 25 (registry drift tests).** T3's `src/superclaude` check applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present; the test never reads `~/.claude`. T2 is non-strict (strict only in stage 4). Acceptance includes a temporary-tree test of each exemption.
- **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N").
- **New final task: stage 1 exit summary for the owner.** Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the commands run and their pass counts), the list of files created, a statement that no carrier was edited (`git diff --stat` over carriers is empty), the open items, and the sentence that the owner's go for stage 2 is given in chat and not by this file. This is the stage 1 exit the spec requires.

## Not to be done by the plan

No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and no stage 2 to 4 task. Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.

## Revision 2 (2026-11-16)

Applied to the plan in place (plan file name, slug and frontmatter unchanged; still 16 tasks, 4 phases). Sources: the pre-execution review `REPORT.md` of the stage 1 plan (findings F1 to F9, recommendations R-001 to R-007) and `revision2-brief.md` (shared decisions 1, 4, 5 and the follow-up carrier decision 2). This section supersedes the older lines above where they differ: the Task 13 line about "the plugin mirror is added in stage 4", and the Task 13 allow-list content.

- **F1, R-001 (blocking, applied).** Task 7: the line "shows only the new module and its command wiring" is replaced. It now reads: until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`; from Task 10 on the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`. The words "its command wiring" are gone (no task wires a command for `follow_ups`).
- **F2, R-002 option (a) (blocking, applied).** Task 3: the stoprule and `finding-grader` row is marked `installed-only`, names `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`, cites no `.dev/` path, and is exempt from the exists-in-repository line; Task 15's T4 carries the same exemption (OD10 stays undecided). Checked: neither file exists under `src/` or `plugins/`; both exist installed.
- **F3, R-003 (applied).** Task 3's allow-list section also lists `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed` (they hold the phrases and are not changed). `stage3-request.md` line 14 repeated the old list and would have contradicted the plan, so it was edited the same way.
- **F4, R-004 and decision 5 (applied).** Task 7 records: `follow-ups.md` stays a separate file, no mapping to `review-ledger/1` rows, `ledger.py` untouched, the audit verdict decides whether a mapping is ever added; the "ledger adapters" are `follow_ups.py`, `classifier_inputs.py` and the classifier column writing of `classify_cmd.py`. Task 16 reports the audit verdict to the owner. `ledger.py` is added to the not-built list.
- **F5, R-005 (applied).** Task 3 fixes the table columns (`family`, `defining file`, `labels`, `model`, `file kind`), the `LABEL=Outcome;` pair format, the path root (relative to `src/superclaude/`, no prefix), the `none` value for a row without a native label (skipped by T4's label check) and `installed-only` rows. Tasks 9, 12 and 15 gain `Depends on: Task 3`.
- **F6, F7, R-006 (applied).** Task 10 depends on Task 7 and Task 9. `run_questions(judge, finding, allowed)` is assigned to Task 9 and `questions_to_ask(inputs)` to Task 10, so Task 11's M, C and E test uses only functions of Tasks 9 and 10. The second half of T12 ("except through the safety route") moves to Task 13, which now depends on Task 9 as well.
- **F8, F9, R-007 (applied).** Task 2's grep uses the full path; Task 12 names the seven review subcommands present today and says `lint` and `estimate` are optional names without modules; Task 4 defines `sweep-flagged` as a ninth state (the spec has eight; it comes from the stage 2 package's sweep) and the installed reference names no rollout stage.
- **Decision 1, retired carriers (applied).** New Constraints bullet; Task 3 lists `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` (path only) with the sentence that the exemption ends when the retirement removes the file; Task 6's note on `skills/task/SKILL.md` (no registry row) was re-read and made consistent; Task 16's carrier diff adds the task-builder folder. Of the 13 files that hold a merge-rule phrase today, only `skills/task/SKILL.md` is a retired carrier.
- **Decision 2, follow-up carrier (applied to stage 1 text).** New Constraints bullet and Task 4 wording: `/sc:implement`'s final review step records and prints only, the offer stays with the top-level session and the consent-bound filing path (OD15), `tech-research` writes the ledger and neither sweeps nor offers; `sc-implement-protocol` joins the not-edited list and the Task 16 diff.
- **Decision 4, no plugin surface (applied).** New Constraints bullet; Task 3 no longer says a plugin mirror comes in stage 4; Task 6's canonical row has no plugin surface (the word `plugin` stays only on the two pointer-only rows whose hand-kept twins exist); Task 15's T2 note says why `plugins/` is still scanned; Task 16 diff adds `plugins`. Registry counts unchanged: 11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows).
- **Gate wording (found while running the gate check).** Task 10's body quoted the "acceptance criteria" label with a colon, which broke the one-label-per-task rule; reworded. Two Constraints lines used the phrase the gate rejects for `git add`; reworded to "keep ... out of `git add`".

## Revision 3 (2026-11-16)

Fix cycle 2, applied to the plan in place (file name, slug and frontmatter unchanged; still 16 tasks, 4 phases). Source: the second pre-execution review `REPORT.md` (M-F1 to M-F10, R-001 to R-008). The first review's F1 to F9 are not reopened. Each finding was checked against the live files before the change.

- **M-F1, R-001 (blocking, applied).** Task 7: the line is now `grep -rln --include='*.py' --exclude-dir=__pycache__ "follow_ups" src/superclaude/cli/review` and says "lists no file other than" in both sentences, so compiled `.pyc` files (pytest writes them) and an empty result both pass.
- **M-F2, R-003 (applied).** Task 3 fixes three grammar rules: a lowercase `family` key (12 keys named), a `Conditional` outcome token (spec-panel MAJOR), and ` + ` between several `defining file` paths. Task 9 names the lookup key (the ledger row's `origin`, else the finding's `source`) and gives UNSET for an unknown family, an unlisted label or a `Conditional` label (test in Task 11). Task 15's T4 splits ` + ` cells and checks each label against at least one file, with temporary-tree tests for a two-file row and a conditional label.
- **M-F3, R-004 (applied).** REQ-09 now has an owner: Task 7 adds `earlier_decisions(rows, identity)` with a test. The offer step that calls it belongs to the stage 2 package (cross-stage fact for its plan).
- **M-F4, R-002 (applied, option: supply the inputs).** Task 10 adds the M absence-by-name precheck and the decision-basis excerpts (spec section 4.3, with Option Q at upstream gates); `questions_to_ask` returns S and W always, and M, C, E and D only with their inputs. Tasks 10, 11 and 12 follow (four count lines, D in the recording-judge test).
- **M-F5, R-005 (applied).** Task 12 writes the verdict for every finding to `classifier-results.json` and to the ledger row's `classifier` column only when a row exists; Task 7 adds `update_field(row_id, field, value, expected_revision)`.
- **M-F6, R-006 (applied).** Task 8: the resolver is an injected function like `gh`; the default loads `origin_repo.py` by file path and calls `read_origin()`; the T8 test passes a fake and one test shows the by-path load.
- **M-F7, R-007 (applied).** Task 4 writes the pr-submit exception without the gitignored-folder path and names no `src/superclaude/` file; its acceptance and Task 5's acceptance gain `src/superclaude` greps; Task 6 repeats both folder greps once `registry.yaml` exists.
- **M-F8 (applied).** Task 1 runs its go and stage 0 summary checks before it creates `SKILL.md` (first sentence of the body).
- **M-F9 (applied).** `verify` is now `verify-citations` in Task 12; the stray ", ;" and the T3 wording for `installed-only` rows (not checked by T3) are fixed in Task 15; Task 2's self-cancelling grep line says "prints nothing"; the tasklist Medium line count is 9 on 2026-11-16 (the spec says 7; the live count wins and is re-counted when the task runs).
- **M-F10 (applied).** Task 7's importer list has the end point "until the stage 2 package adds its own importer"; Task 9 keeps its constant off the names `THRESHOLDS` and `CONVERGENCE_THRESHOLDS`, and Tasks 9, 10, 12 and 13 gain a `make lint` acceptance line.
- **Added after the stage 2 fix cycle.** Task 7 gains an acceptance line: a later `write` or `update_field` never clears a ledger's capture state or a row's tags (the stage 2 package tests it).
- **Added after the stage 4 fix cycle.** Task 15 names the strict switch of T2 as the constant `STRICT_T2` (default `False`); the stage 4 package sets it `True`.
````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:17-30

````markdown
## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 1 of five packages (one plan per stage, the owner's decision of 2026-11-16). It creates new files only (the skill folder, new CLI modules, new tests, one doctor check) and edits no review-loop carrier (`pragmatic.md`, agents, templates, rule prompts, the task skill, tech-research, `sc-implement-protocol`, `WORKER-CONTRACT.md`); every registry `digest` row stays `legacy`. It runs only after the stage 0 package is done, the owner has read the stage 0 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Stage 2 starts only after the owner reads this package's summary and says go.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, any change to the cap of 2 fix cycles, and any edit or replacement of `src/superclaude/cli/review/ledger.py`.
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
- Retired carriers (owner decision of 2026-11-16: `/sc:task` and task-builder are being retired). No task of this program edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for those; they keep today's text until the retirement removes them. Task 3 lists them in the "Merge-rule allow-list" section as `exempt-by-retirement` (by path only), and that exemption ends when the retirement removes the file. Tests that exist only to pin those files are not re-pinned here; a test that pins both a retired and an active carrier is re-pinned for the active carrier's part only.
- Follow-up carrier. The end-of-run follow-up list is carried by the final review step of `/sc:implement`, which records and prints only. `refs/qa.md` of that skill is not edited (it keeps its own scale and its final summary "never asks the user anything"), and the once-per-run offer question stays with the top-level session through the output style and with the consent-bound filing path (OD15), so this program adds no question to `/sc:implement`. `tech-research` is an active workflow that writes the ledger and neither sweeps nor offers. Stage 1 edits none of these files.
- Plugin surface. IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin, so this program creates no plugin surface: no `plugins/superclaude/skills/sc-review-severity/` mirror, no plugin parity test and no `canonical` registry row for a plugin path. The two existing hand-kept plugin twins (`plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`) are touched only where an existing test pins them and the active source carrier changes; this package touches neither. The owner has not confirmed removing plugin parity (the program's open-questions file, section 3.4); this is the plan author's reassessment.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; keep everything under the project `.claude/` folder out of `git add` (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes tells a reader to keep `.dev/tasks/` out of `git add`. Staging is not committing.
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:936-952

````markdown
## 12. Rollout stages

<!-- Source: Base (original, modified) - restructured per Change #PC-28 from Variant 2 section 12, Variant 3 section 10 stages 0 and 1 and Variant 1 section 11; stage 2 duties per RM-8 and RM-9; L6 and Rule 6 per Change #PC-24 and RB-2; inventory per RM-14; revert per RB-1 -->

No stage starts before its entry condition is met and the owner has seen the numbers. Own-scale adapters (OD6, OD7, OD8, OD10) and classifier authority (OD4) are owner decisions, not stages, and no stage implies them.

| Stage | Entry condition | What happens | Exit condition | Rollback |
|---|---|---|---|---|
| 0. Measure (this program, offline) | this spec reviewed | 0a: the scored table and five runs with a fixture or approved judge, only if the table exists. 0b: the retrospective escape test on run 2 (section 8.4). 0c: three blind agents that did not write the rule re-grade the table under the old and the new text, paired, only if the table exists. Inventory freeze: every Grep of section 10 re-run, including the frozen FAIL-trigger Grep (REQ-30), with results stored | a written result: escape estimate with its interval; when the table exists, how many old-blocking rows become non-blocking and the confusion matrix | nothing changed |
| 1. Offline scaffold | stage 0 result written; owner go | the skill folder with registry rows all `legacy` (T1 and T2 accept the legacy text in registered rows); the ledger reader and writer with the codec; ledger adapters; the fixture judge; property tests; crash, reconcile and consent tests; the install check. No carrier is edited | T1 to T4, T6 to T8, T11 to T13 and T17 green offline | delete the new files |
| 2. Shadow beside the old rule | stage 1 exit | the task skill and tech-research gates write the ledger and make the per-run offer (it replaces the output style's "once per loop" ask for that run); reviewers emit `rests_on` while the old definition still decides; the classifier runs in shadow; the safety route GR12 is live; the final-gate sweep GR7 is built; `core/WORKER-CONTRACT.md` gains the three keys (REQ-12) | at least 5 shadow runs observed; ledger volume and `consumer-unknown` share known; offers answered; shadow agreement reported; zero safety misses and no capture failure | stop writing the ledger; restore the old carrier text by the three-step revert (section 9.4) |
| 3. Pilot | 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (section 8.3) met; 0c as well when the table exists; owner go | `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` move to digest v2 together; the stage 3 merge-rule lines of section 10.3 (task skill, rf-qa, rf-qa-qualitative, rf-analyst; L1); L2 fix-pass checks; L6 for rf-qa, and Rule 6 if OD16 chooses (b), with its test re-pinned in the same change; the cadence pins move | one audit window (section 8.2) with no revert trigger tripped; M12 reported | the three-step revert of the pilot rows to `legacy` |
| 4. Propagate | stage 3 exit; owner go | templates, rule prompts, builders and researchers to v2; the stage 4 lines of section 10.3; the spec-panel narrowing; the plugin mirror and parity test; T2 becomes strict (no legacy definition sentence in `src/` or `plugins/`) | drift tests green and strict; a second audit window clear | per-row three-step revert |

Why shadow comes before the pilot: the whole design rests on reviewers being able to name a consumer honestly. Stage 2 measures that while the old definition still decides, so a failure costs nothing.

Templates note: task files already generated from the old MDTM templates keep the old text. The reverse scan covers `src/` and `plugins/` only; old task folders under `.dev/tasks/` are not migrated.
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:912-934

````markdown
### 11.2 New tests the plan must add

| # | Test | Fails when |
|---|---|---|
| T1 | digest equality over the registry | a registry row's file does not hold exactly one digest equal to the digest section of `refs/rule.md` for its version |
| T2 | reverse scan of tracked `src/` and `plugins/` | a file holds the old definition sentence or a fence opener and is not a registry row; from stage 4, any legacy definition sentence remains |
| T3 | pointer line | a pointer does not name `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, or a carrier contains `src/superclaude` |
| T4 | scale map | a scale-map row names a missing file or a label that is not in it |
| T5 | merge-rule reverse scan | `highest severity`, `more severe rating` or `higher severity` appears in `src/` or `plugins/` outside the scale-map allow-list (staged with section 10.3) |
| T6 | truth-table properties | any of the three property tests of REQ-21 fails, or NA is reachable from a failed or skipped call (REQ-19) |
| T7 | ledger contract | a required column is missing; a Medium row lacks `why_not_blocking`; identity merges on digest alone; a codec round-trip fails (pipes, backticks, a triple-backtick line, literal entities, Unicode, multiline); a stale writer overwrites a newer revision; a malformed ledger is reset instead of preserved |
| T8 | crash, reconcile and consent | a resume asks again; a changed set is filed without new consent; a timeout after a successful post creates a second issue; a body whose read-back digest differs is marked `filed`; a repository other than the verified `<R>` is targeted |
| T9 | reviewer brief | `rests_on` or `why not blocking` is missing from a reviewer brief |
| T10 | unattended contract | an unattended run asks a question or makes a GitHub call; the three keys are missing; `follow_up_capture_state: incomplete` does not give `worker_status: partial` |
| T11 | classifier fixture replay | the fixture judge does not reproduce verdicts, or hostile instructions inside a quote change a verdict |
| T12 | no authority by default | a classifier verdict changes a gate outcome other than through the safety route |
| T13 | install check | a stale installed digest version is not reported (REQ-27) |
| T14 | precedence sentence | a v2 carrier lacks the precedence sentence (REQ-03) |
| T15 | plugin parity (stage 4) | the plugin mirror of the skill folder differs from `src` |
| T16 | final-gate sweep | a seeded Medium row whose flawed text reaches the final decision basis uncorrected is not made Blocking (GR7; precondition of OD14) |
| T17 | safety route | a GR1 vocabulary hit, or a judge answer S = Y or S = U, on a non-blocking row is written as a plain follow-up instead of `protected-risk-dispute` (GR12) |

Static string pins are delivery checks, not evidence that agents follow the flow. The plan also runs behavioural fixture replays and the held-out evaluation.
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:396-396

````markdown
**[REQ-09] Across runs.** A new run on the same deliverable matches earlier `declined`, `filed` and `resolved` rows by the identity tuple without the run namespace, and does not offer or file them again.
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:525-562

````markdown

**From probability to state.** Each question's probability becomes Y, N or U by bands; a failed or skipped call is UNSET. The starting bands are placeholders from `jev-uses.md`, to be set from the scored table and not fitted to it: Y at p of 0.70 or more, N at 0.30 or less, U between; the safety question S uses a lower band (Y at 0.30 or more, N at 0.10 or less), because a missed safety finding is the costly error.

**[REQ-19] The NA state.** NA (read as N) exists only for M and C, and only when the deliverable kind is declared to have no required-item list or no constraint list. It is never used when an extractor failed or is missing; that is UNSET. A test pins that NA is reachable only from the deliverable-kind declaration, never from a failed or skipped call (in the sketch, `tri(q, None)` gives UNSET [V]).

**Precedence.**

1. S = Y gives BLOCKING.
2. Otherwise M = Y or C = Y gives BLOCKING.
3. Otherwise "wrong" combines W and E. **[REQ-17]** Wrong is Y if either is Y; N only if both are N; UNSET only if both are UNSET; otherwise U. A missing or unsettled partner never reads as "not wrong".
4. If wrong is UNSET, the base verdict is SHOW_USER. Otherwise look up (wrong, D):

| wrong \ D | Y | U | N | UNSET |
|---|---|---|---|---|
| Y | BLOCKING | SHOW_USER | FOLLOW_UP | SHOW_USER |
| U | SHOW_USER | SHOW_USER | FOLLOW_UP | SHOW_USER |
| N | NOTE | NOTE | NOTE | NOTE |

5. **[REQ-18]** If any of S, M or C is U or UNSET, a verdict below SHOW_USER is lifted to SHOW_USER. A BLOCKING verdict is never lowered.

The cell (wrong N, D Y) gives NOTE although the text feeds a decision; it is a possible mis-answer, counted per run and not tuned.

**Verdict meanings.** BLOCKING; FOLLOW_UP (Medium); NOTE; SHOW_USER (the classifier will not decide; the reviewer's label stands and the row is tagged `unsettled`, section 6.1). **[REQ-20]** UNDETERMINED is not a verdict of the table: it is a typed failure of the judge chain (no judge gave a usable answer) that moves the finding to the next judge (section 7.5).

**[REQ-21] Property tests.** The table carries three property tests, and the sketch version 2 passes all three [V: run during this merge with `uv run --no-project python -B`]:

1. Every one of the 6,400 combinations returns exactly one verdict (S, W, E, D each in Y, N, U, UNSET; M and C each in Y, N, U, UNSET, NA).
2. Monotone over answered states: raising an answered input from N to U to Y (NA counts as N) never lowers the verdict, on the order NOTE, FOLLOW_UP, SHOW_USER, BLOCKING. 0 violations.
3. No silent demotion: a verdict below SHOW_USER means that no way of filling the UNSET answers could produce BLOCKING. 0 violations.

The table is monotone over answered states only. It is not "monotone in every input", and the spec must never claim that: moving an input from UNSET to an answer can lower the verdict, by design. The remaining lowering moves, all intended [V: this merge]:

- Of 26,880 moves from UNSET to an answer, 256 lower the verdict. 240 are moves to N: a real "no" may lower a verdict. The other 16 move SHOW_USER to FOLLOW_UP when W and E were both unset, one of them becomes Y or U, and D is N: D = N rules out BLOCKING, so FOLLOW_UP is correct.
- Of 2,560 moves from UNSET to NA on M or C, 72 lower the verdict: a declared absence of a list is a real "no".
- No state with S, M or C at U or UNSET lands below SHOW_USER. `verdict(N,N,N,N,UNSET,Y)` (E missing, a decision depends) gives SHOW_USER, and `verdict(UNSET,N,N,Y,N,N)` (safety answer missing) gives SHOW_USER; both were wrong in version 1.
- Verdict counts over the 6,400 combinations: BLOCKING 3,664, SHOW_USER 2,664, FOLLOW_UP 56, NOTE 16.

History: a first draft of the sketch let S = U return SHOW_USER ahead of an M = Y blocking verdict (511 violations); version 1 counted 4,096 combinations, let a missing answer lower a verdict (432 of 18,432 moves) and let a missing S, M, C or E answer file a finding as a note [E: `jev-uses.md` section 4]. The lesson is the three property tests, not only example rows.
````

## Coverage slice

Exit-test to task map built by the orchestrator (verify each row):

| Spec stage 1 exit test (SPEC:945) | Plan task that builds it (orchestrator's reading; verify) |
|---|---|
| T1 digest equality over the registry | Task 15 |
| T2 reverse scan (non-strict) | Task 15 |
| T3 pointer line | Task 15 |
| T4 scale map | Task 15 (reads the table of Task 3) |
| T6 truth-table properties | Task 11 (module in Task 9) |
| T7 ledger contract | Task 7 |
| T8 crash, reconcile and consent | Task 8 |
| T11 classifier fixture replay | Task 11 |
| T12 no authority by default | Task 11 (first half), Task 13 (second half) |
| T13 install check | Task 14 |
| T17 safety route | Task 13 |
| T14 precedence sentence (not a stage 1 exit test) | Task 15 |

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| R-001 (parsed; a review-recommendation label, not a requirement) | T1 | unmatched by ID | source.md:26,28,42,44 |
| R-002 (parsed; a review-recommendation label, not a requirement) | T1 | unmatched by ID | source.md:29,47 |
| R-003 (parsed; a review-recommendation label, not a requirement) | T1 | unmatched by ID | source.md:30,45 |
| R-004 (parsed; a review-recommendation label, not a requirement) | T1 | unmatched by ID | source.md:31,46 |
| R-005 (parsed; a review-recommendation label, not a requirement) | T1 | unmatched by ID | source.md:32,48 |
| R-006 (parsed; a review-recommendation label, not a requirement) | T1 | unmatched by ID | source.md:33,49 |
| R-007 (parsed; a review-recommendation label, not a requirement) | T1 | unmatched by ID | source.md:26,34,50 |
| R-008 (parsed; a review-recommendation label, not a requirement) | T1 | unmatched by ID | source.md:42 |
| REQ-09 (parsed; spec requirement) | T1 | covered, task [7] | source.md:46 |
| INF-001: This stage creates new files only (the skill folder, new CLI modules, new tests, one docto | T1 | unmatched mechanically (best task 7, 0.562); orchestrator mapped by hand to the Constraints or provenance lines | source.md:3 |
| INF-004: Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254 | T1 | unmatched mechanically (best task 9, 0.368); orchestrator mapped by hand to the Constraints or provenance lines | source.md:7 |
| INF-005: Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owne | T1 | unmatched mechanically (best task 1, 0.357); orchestrator mapped by hand to the Constraints or provenance lines | source.md:7 |
| INF-007: pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only | T1 | unmatched mechanically (best task 9, 0.5); orchestrator mapped by hand to the Constraints or provenance lines | source.md:7 |
| INF-008: The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation | T1 | unmatched mechanically (best task 1, 0.5); orchestrator mapped by hand to the Constraints or provenance lines | source.md:7 |
| INF-011: Drop the base plan's Phase 3 to 5 gate prose. | T1 | unmatched mechanically (best task 2, 0.333); orchestrator mapped by hand to the Constraints or provenance lines | source.md:11 |
| INF-027: that a later task of the same package makes false get an end point ("until Task N"). | T1 | unmatched mechanically (best task 7, 0.5); orchestrator mapped by hand to the Constraints or provenance lines | source.md:17 |
| INF-033: No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech- | T1 | unmatched mechanically (best task 4, 0.4); orchestrator mapped by hand to the Constraints or provenance lines | source.md:22 |
| INF-034: Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 f | T1 | unmatched mechanically (best task 2, 0.364); orchestrator mapped by hand to the Constraints or provenance lines | source.md:22 |
| INF-035: No Jev call, key or account. | T1 | unmatched mechanically (best task 9, 0.5); orchestrator mapped by hand to the Constraints or provenance lines | source.md:22 |
| INF-065: `sc-implement-protocol` joins the not-edited list and the Task 16 diff. | T1 | unmatched mechanically (best task 7, 0.429); orchestrator mapped by hand to the Constraints or provenance lines | source.md:36 |
