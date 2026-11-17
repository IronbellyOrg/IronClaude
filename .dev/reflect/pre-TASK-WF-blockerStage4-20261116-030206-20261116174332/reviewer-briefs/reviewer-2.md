# Reviewer brief 2 (persona: qa; model class: haiku)

## T1 card excerpt

# T1 reflection card (UC-1, pre-execution), second review of the revised plan

Spec: `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md` (45 lines; byte-identical to `stage-requests/stage4-request.md`, checked with `cmp`: SOURCE_BYTE_EQUAL). Lines 1 to 20 are the original request; lines 22 to 45 are "Revision 2 (2026-11-16)".
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md` (4 phases, 6 tasks, schema workflow-plan/1.2, 128 lines, edited in place on 2026-11-16). In this card `P4:n` is line n of that plan, `SRC4:n` is line n of `source.md`, `S1:n` and `S3:n` are lines of the stage 1 plan `TASK-WF-blockerStage1-20261116-030154` and the stage 3 plan `TASK-WF-blockerStage3-20261116-030158`, `SPEC:n` is line n of `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`, `MAP:n` is line n of `tests/skills/test_review_severity_mapping.py`.
Author: the orchestrator (self-review; the T2 reviewers exist to break that bias). Executor class (plan author) unknown.
Codegraph run state: index_state=fresh, checked_at 2026-11-16T17:44:17Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel, projectPath same. Codegraph does not index Markdown, so every claim below was checked with Grep and Read. Stages 1 to 3 have not run: `src/superclaude/skills/sc-review-severity/` does not exist, so every cross-stage fact is read from the stage 1 and stage 3 plan text, not from files.

## Coverage and acceptance

The source has no labelled requirement ids (parsed_count 0). Step 1B.0 Pass 2 emitted 28 quote-pinned inferred rows (`artifacts/coverage-matrix.yaml`). The containment rule matched 22 of 28, `coverage_pct_union` 0.7857, so `coverage_degraded: parsed-sparse` (inferred 28 greater than parsed 0) and the Tier-1 stop is forbidden. The six mechanical misses read by hand all map: INF-002 (reuse of base Tasks 41 to 46) is the structure of Tasks 1 to 6 and P4:19; INF-012 (stage 4 is the last package, strict T2 here, end points) is P4:20 and P4:28; INF-014 (not to be done) is P4:26; INF-018 (dimensional-mismatch sentence) is Task 4 line P4:97; INF-026 (once per run) is P4:86 and P4:24; INF-010 (plugin mirror order) is superseded on purpose by INF-027 (decision 4), see observation 5.

## Check of the first-review fixes (G1 and G2 blocking, G3 to G14 non-blocking) against the live plan

- G1 fixed: Task 1 acceptance P4:40 to P4:42 now reads the go cell (date plus the window statement) and the stage 3 package, and only requires the stage 3 summary to exist and quote RT1, RT2 and M12. The stage 3 plan's own summary acceptance S3:238 quotes M12, M10b, M1 and RT1 to RT3, so the three tokens will exist. The column name `Owner go (date, where)` exists in the ledger README.
- G2 fixed in the plan text: Task 4 P4:93 names the re-pins in `MAP` (Grading literal at MAP:58, Verdict literals at MAP:71 and MAP:72, both parametrized over `SPEC_PANELS` at MAP:24), leaves the output-style pin at MAP:128 to stage 3, adds one source-only test, runs the mapping test (P4:100), and names the FR-8 line near 332 (P4:87). S3:25 and S3:192 confirm stage 3 leaves the spec-panel pins alone.
- G3 fixed: Task 5 P4:113 runs 12 test files, including `test_review_severity_rule.py`, `test_review_brief_placement.py`, `test_review_prompt_overrides.py`, `test_worker_contract.py`, `test_implement_severity_static.py` and `test_review_brief_rests_on.py`; the plugin byte copy moved to Task 2 (P4:57).
- G5 fixed: P4:88 and P4:97. G6 fixed: P4:37 "First do the first three acceptance checks, before any edit". G7 fixed: Tasks 1 and 3 name the "Merge-rule allow-list" section. G8 fixed: P4:70 and P4:75 give the case-insensitive counts 5, 6, 1, 2; I re-counted them today (5, 6, 1, 2). G9 fixed: the L1 text is defined once at P4:25. G10 fixed: P4:60 and P4:61. G13 fixed: P4:108 and P4:111. G14 (a) to (d): see observations 3 and 2.
- G4, G11 and G12 are removed by the plugin decision (P4:23). I confirmed `git grep -n "review-severity:digest" -- src plugins` prints nothing today and that no plugin file holds the old definition sentence or a merge-rule phrase.

## Live facts re-read today (anchors the plan relies on)

`agent_template_qa.md`: merge rule line 85, PASS line 157, FAIL line 158, S1 line 161, S2 line 162, cap line 190 and 341, label list line 333. `agent_template_analysis.md:466`, `skill_template.md:828` to 830, MDTM templates `01:644` and `02:655`. Rule prompts `:11, :27, :28, :27`. `document_review_loop_prompts.md:31, :32, :48`. Skills merge lines: tech-reference 510 and 513, readme 542 and 547, tdd 122, operational-guide 511. Spec-panel source 259, 260, 332, 372, 455; plugin twin 257, 258, 330. The only 11 files holding "Grade every review finding as blocking or minor" under `src` are the 11 digest carriers (stage 3 owns pragmatic, rf-qa, rf-qa-qualitative). `cmp` of the source and plugin rules prompt prints nothing today. HALT counts 2, 5, 6 match P4:43.

## Deviation and risk observations (new in this revision)

1. **Task 5 does not prove strict mode.** P4:112 requires "a temporary-tree case ... that holds the old definition sentence and has no registry row failing". The stage 1 T2 test already fails on exactly that case before the switch (S1:223: "fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; strict mode is a switch, off in this phase"). Strict mode differs by also failing a registered file that still holds the old sentence (SPEC:917 "from stage 4, any legacy definition sentence remains"). The acceptance line passes with the switch left off, and the 12-test run (P4:113) is green either way once all rows are `v2`. The switch has no name or mechanism in the stage 1 text, so the executor must guess it.
2. **Task 1 acceptance P4:41 contradicts itself.** "it is in the done subfolder ... or its `progress.md` has a `complete` line for every task (a package stopped at archive-blocked ... fails this check and the run halts)". A package whose tasks are all complete but whose archive is blocked keeps every `complete` line and stays in `to-do/` (managed-workspace.md line 48 and 62), so it passes the second branch and fails the parenthesis.
3. **Task 1 Rule 6 pointer is ambiguous.** P4:37 says read the heading with `grep -n "^6\. \*\*" src/superclaude/agents/rf-qa-qualitative.md`. Today that grep returns about ten lines (97, 182, 265, 322, 393, 460, 531, 687, 768, 990); only line 990 is Critical Rule 6. Stage 3 rewrites it (S3:154, S3:158). The executor must pick the right hit by hand.
4. **Spec section 10.5 rows are unaddressed.** SPEC:867 lists `skills/tech-research/SKILL.md` (488 to 490, 517 to 519, 555, 562) and `skills/roadmap` cap lines under "Builders and researchers ... point at the shared rule". No stage 4 task touches them and the plan does not record an exclusion (the base plan did not either). The lines are marked [E] (not verified) in the spec. `skills/roadmap/SKILL.md` today holds several "Max 2 fix cycles" lines (434 to 448, 563).
5. **The snapshot `source.md` still carries the old plugin-mirror instruction.** SRC4:14 orders the plugin mirror, T15 parity and a plugin canonical row; SRC4:42 and P4:23 override it. The plan follows the override and names it a plan-author reassessment, not an owner decision (P4:23); the owner has not confirmed it (OPEN-QUESTIONS section 3.4). The spec's stage 4 row (SPEC:948) still lists the plugin mirror and parity test.
6. **Allow-list and registry ordering holds.** Tasks 1 and 3 remove six files from the allow-list; stage 1 Task 3 lists exactly those six as `allowed` (S1:66, S1:73), so no row is left or missing. The MDTM templates have registry rows but no allow-list entries and hold no merge-rule phrase.
7. **No fixture row breaks.** The edit-table fixtures `review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` hold rows for the stage 4 files only on cap lines, the Fix Cycle block, the PASS/FAIL pair of `skill_template.md` and the zero-tolerance intros (checked row by row); none holds the definition bullets, the merge-rule lines or the lines Task 1 rewrites, so `test_e_every_cap_edits_row_holds` and `test_j_every_sweep_edits_row_holds` stay green.

## Recommendations (for the reviewers, not for the plan)

- Test observation 1 against the stage 1 T2 definition and the spec; decide whether the missing discriminating check is a wrong result or only a weak check.
- Test whether the 12-test run (P4:113) misses a pin: `tests/unit/test_cli_install.py`, `tests/audit/*`, the stage 1 doctor test, and any test reading the plugin spec-panel.
- Read stage 1, stage 2 and stage 3 for anything Tasks 1 to 6 assume and the earlier plans do not provide (registry states, scale-map section name, strict switch, summary file names).
- Check the revision for new defects: task numbers and `Depends on:` lines, acceptance lines a later task falsifies without an end point, paths that do not exist, and contradictions with the brief (no plugin mirror or parity test, retired task-builder files not edited).


This is the SECOND pre-execution review of the stage 4 plan (stage 4 of 5, the last, of the blocker-classification work, GitHub issue #552). The plan was revised in place on 2026-11-16 after a first review (card in your hunks: blocking G1 and G2, non-blocking G3 to G14). The lead asks three things: (a) does each first-review finding the plan says it fixed really get fixed in the LIVE plan (the audit-window summary check, the re-pin of tests/skills/test_review_severity_mapping.py, the final pinning run), (b) did the revision introduce a new defect (task numbering and dependencies, acceptance lines that a later task of this package makes false without an end point, paths that do not exist, contradictions with the brief's decisions: no plugin mirror or parity test, the retired task-builder files not edited), and (c) does the plan meet the spec `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`. Grade by consequence. In the plan, `P4:n` is line n of the plan file; use full repo-relative paths with line numbers in your citations.


Persona instructions (qa): audit the coverage matrix AGAINST the spec body in your grounding hunks (the stage 4 request `source.md` in full, and the merged spec sections for stage 4); surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check: (1) every change the request and its Revision 2 list has a task with an acceptance line that tests it, and no task contradicts it; (2) every acceptance line of Tasks 1 to 6: can it be met, does it name a command that exists and prints what the line says (re-run the grep logic mentally against the live files in your hunks or with Grep), and does a LATER task of this package make it false without an end point ('until Task N'); (3) task numbering, phase count and every `Depends on:` line (contiguous numbers, only lower numbers, no missing dependency: e.g. does a task read or edit something another task creates or changes); (4) findings G9 to G14 of the first review: fixed or not; (5) the plan against the spec's stage 4 row and section 10.3 to 10.5 (merge-rule lines, spec-panel narrowing, cap text, strict T2), noting any spec requirement for stage 4 that the plan neither does nor excludes on purpose.


Severity rule (use exactly this): grade every finding by consequence as blocking or minor. Blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss. Minor = wording or format. A finding that needs a guess about which of two readings an executor picks is minor unless the worse reading is the only one the text allows. A zero-finding result is valid if you state what you checked; never invent a finding to avoid a zero; there is no minimum count. You are read-only: do not edit, write, move or delete anything, run no shell or git command. Audit the supplied hunks and what you can Read, Grep and Glob from the repository root (the current working directory). Use the codegraph tools only when the run-state line says index_state=fresh, passing the projectPath given; codegraph indexes .py and .yaml, not Markdown. Stages 1 to 3 have not run, so `src/superclaude/skills/sc-review-severity/` does not exist yet: read cross-stage facts from the stage 1 and stage 3 plan text in your hunks, never assume a file exists that no hunk or Glob shows.


Return your card as one message, at most about 7000 characters, in this shape (no tables, no markdown table rows): start with `## Verdict` (one sentence), then `## Findings` with one line per finding: `F<n> | MAJOR or MINOR | blocking true or false | category (contradiction, data-loss, missing-requirement, unpassable-check, safety, other) | Who: <the executor or reader affected>. Wrong result: <the concrete wrong outcome>. | citations: <path:line "quote"> (1 to 6 real file:line citations, quotes verbatim, re-Read each before citing)`; then `## Checked` (bullets: what you verified and found fine, with citations), then `## Self-report` with `confidence: <0.00-1.00>` and `reviewer_model_self_report: <the model you are running as, in one line>`. Number the findings F1, F2, ... and write them in the F-line format only. Do not add a findings-v2 block (legacy engine).


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T17:44:17Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md:1-128

`````markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-blockerStage4-20261116-030206
version: "1"
priority: Medium
created_date: "2026-11-16"
---

# Stage 4 plan: propagate the new rule to the remaining carriers (issue #552)

Source: ./source.md
Goal: Move the remaining templates, rule prompts, builder and researcher skills and the spec-panel to the new rule, switch the drift scan to strict, run every pinning test once at the end, and give the owner the final summary.

## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the owner answers of 2026-11-16 in `OPEN-QUESTIONS.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 4 of five packages and the last (one plan per stage). It runs only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (spec section 13.2), the owner has read the stage 3 summary and said go in chat, and the go is recorded in the stage ledger. The window result is recorded in the owner's entry in the stage 4 go cell of the ledger (column `Owner go (date, where)`), because the stage 3 summary is written before the window and cannot state its result. Task 1 checks the cell, the stage 3 package and the summary before its first edit. Strict T2 is switched on here (Task 5).
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Retired carriers are not edited (owner answer of 2026-11-16, PF `OPEN-QUESTIONS.md` section 2.2: `/sc:task` and task-builder are to be retired). No task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for them; they keep today's text until the retirement removes them. The base plan's consumer-line task (L4, which edited the builder skill and the two MDTM templates) is dropped for that reason: its only writer is the retired builder. The merge-rule text of the retired carriers is listed `exempt-by-retirement`, by path only, in the "Merge-rule allow-list" section of `refs/scale-map.md` (stage 1), and the exemption ends when the retirement removes the file. Tests that exist only to pin the retired carriers (for example `tests/skills/test_task_builder_merge.py`) are neither run nor re-pinned here. The two MDTM templates stay in scope only as digest carriers: they hold the old definition sentence and have registry rows.
- No plugin surface is added (owner answer of 2026-11-16, PF `OPEN-QUESTIONS.md` sections 2.3 and 3.4: IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin). This package builds no `plugins/superclaude/skills/sc-review-severity/` folder, no plugin parity test (T15), no registry row for a plugin path and no reverse scan of a plugin tree; this is the plan author's reassessment, not an owner decision to remove plugin parity. The two hand-kept plugin twins `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` and `plugins/superclaude/commands/spec-panel.md` are edited only where an existing test pins them and the source carrier changes: `tests/skills/test_review_brief_placement.py` pins the rules prompt as a byte copy, and `tests/skills/test_review_severity_mapping.py`, `test_spec_panel_review_loop.py` and `test_review_loop_extension.py` pin the spec-panel copy. A plugin-only install, which has neither `~/.claude` nor a project `.claude/`, cannot resolve the pointers and is not covered. The registry ends with exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only` and 5 `installed-only`.
- The once-per-run offer stays with the top-level session through the output style (moved from once per loop to once per run by the stage 3 package). This package adds no question to any command; the spec-panel text only names the ledger and the cadence.
- L1 merge text, used by Tasks 1 and 3: the clause "the consolidator grades each finding by the rule, keeps every reviewer's own grade visible, and sends a blocking grade that names no consumer back to the reviewer once" (spec L1). It is pinned by the phrase `keeps every reviewer's own grade visible`, and each edited file names the rule once as `~/.claude/skills/sc-review-severity/refs/rule.md`, else `.claude/skills/sc-review-severity/refs/rule.md`.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), any replacement of `src/superclaude/cli/review/ledger.py`, the 35 percent score target, and any change to the cap of 2 fix cycles.
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability. This package builds no classifier task.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; do not stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says that `.dev/tasks/` is excluded from staging. Staging is not committing.

## Phase 1: Move the templates

## Task 1: Check the entry gate and move the templates to digest v2

First do the first three acceptance checks, before any edit; when one fails, stop and leave every file unchanged. Then edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (the definition bullets near line 161, the merge rule near line 85, the label list near line 333 per OD16, and the PASS and FAIL bullets near lines 157 and 158, rewritten to "No blocking issues" and "Any blocking issue exists" or kept as a named mechanical gate recorded in `refs/scale-map.md`), `documents/agent_template_analysis.md` (the merge rule near line 466), `documents/skill_template.md` (the definition near line 828), `workflow/01_mdtm_template_generic_task.md` (near line 644) and `workflow/02_mdtm_template_complex_task.md` (near line 655). Each of the four digest templates (`agent_template_qa.md`, `skill_template.md` and the two MDTM templates) gets the digest and pointer in place of the definition bullets and the L1 merge text, and its registry row is set to `v2`; `agent_template_analysis.md` gets the L1 merge text only (no digest, no fence, no registry row). The label list near line 333 of `agent_template_qa.md` is an example comment that names the rf-qa-qualitative rule labels; replace its label "Contradictions are always IMPORTANT or CRITICAL" with the heading the stage 3 package gave Rule 6 in `src/superclaude/agents/rf-qa-qualitative.md` (read it there with `grep -n "^6\. \*\*" src/superclaude/agents/rf-qa-qualitative.md`). Remove `agent_template_qa.md` and `agent_template_analysis.md` from the "Merge-rule allow-list" section of `src/superclaude/skills/sc-review-severity/refs/scale-map.md` (the stage 3 scan test reads its allow-list from that section and only checks that each listed file exists, so a forgotten removal turns nothing red; the grep below catches it). Task files already generated from the old templates keep the old text and are not migrated.

Acceptance criteria:
- The stage ledger `stage-requests/README.md` in PF has, in the Owner go cell of the stage 4 row, a date and the owner's statement that one audit window has passed with no revert trigger (RT1 or RT2) tripped; when the cell lacks either, this check fails and the run halts for the owner's Ruling.
- The stage 3 package is complete: it is in the done subfolder of the repository task folder, or its `progress.md` has a `complete` line for every task (a package stopped at archive-blocked or at an open blocking finding fails this check and the run halts).
- The stage 3 package's `./artifacts/stage3-summary-for-owner.md` (read by package id) exists and quotes RT1, RT2 and M12 (`grep -c` of each token prints 1 or more); it is not required to state that the window passed, because the window runs after that package and its result is the one read from the go cell in the first check.
- Each of the four digest template files holds exactly one fenced digest (`grep -c "review-severity:digest v2 begin"` prints 1 in each) and its digest ends with the sentence "A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings" (`grep -c "runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"` prints 1 in each); the at-cap sentences outside the digest are unchanged (`grep -c "HALT and escalate to the user with the open blocking findings"` still prints 2 for `agent_template_qa.md`, 5 for `01_mdtm_template_generic_task.md` and 6 for `02_mdtm_template_complex_task.md`, re-counted before the edit).
- `agent_template_analysis.md` holds no digest (`grep -c "review-severity:digest"` prints 0) and no `more severe rating` text, and its merge line contains `keeps every reviewer's own grade visible`; the merge line of `agent_template_qa.md` contains the same phrase.
- The registry rows of the four digest templates say `v2` and the registry still has exactly 11 rows of kind `digest` (read from `refs/registry.yaml`); `uv run pytest tests/skills/test_review_severity_registry.py -v` passes, so T1 holds for the four rows.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude/templates` prints nothing, and `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/templates/documents/agent_template_qa.md` prints 0 or the remaining line is listed in `refs/scale-map.md` with its reason.
- `grep -n "Contradictions are always IMPORTANT or CRITICAL" src/superclaude/templates/documents/agent_template_qa.md` prints nothing, and the rf-qa-qualitative example label there equals the Rule 6 heading words found in `src/superclaude/agents/rf-qa-qualitative.md`.
- The "Merge-rule allow-list" section of `refs/scale-map.md` no longer names `agent_template_qa.md` or `agent_template_analysis.md` and still names every entry that is not one of the six stage 4 files (the auggie file, `refs/rule.md` and the entries marked `exempt-by-retirement`).
- `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_prompt_overrides.py -v` passes with the two templates removed from the allow-list (the Independent stance, "there is no minimum count" and "do not invent findings to avoid a zero" sentences are still in `agent_template_qa.md`, and "no minimum count" is still in both MDTM templates).

## Phase 2: Move the rule prompts, builders and researchers

## Task 2: Move the rule prompts to digest v2 and set the two pointer-only rows

Depends on: Task 1

Edit the digest carriers in `src/superclaude/rules/prompts/`: `automated_qa_workflow_qa_prompt.md` (near line 11), `doc_code_analyst_qa_prompt.md` (near line 27), `documentation_expert_qa_prompt.md` (near line 28) and `recruiting_expert_qa_prompt.md` (near line 27); update those four registry rows to `v2`. Edit `document_review_loop_prompts.md`: the Medium wording near lines 31, 32 and 48 (the Grading check bullet and the first-review and re-review briefs, which say "follow-up candidates") becomes the follow-up ledger wording, with one pointer sentence naming `~/.claude/skills/sc-review-severity/refs/follow-up-ledger.md` first and `.claude/skills/sc-review-severity/refs/follow-up-ledger.md` second, inside the existing Grading check bullet (no new section; the structure and the `"src/superclaude" not in TEXT` assertion of `tests/review/test_review_rules_text.py` must still hold). Its registry row is of kind `pointer-only` and stays so; it is checked by T3 and never by T1. Then make `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` a byte copy of the edited source file with `cp`, in this task and not later, because `tests/skills/test_review_brief_placement.py` pins the two files as byte-equal and the two are byte-identical today. The plugin copy therefore carries the installed-path pointer like every other carrier, and no plugin-root path.

Acceptance criteria:
- Each of the four rule prompts holds exactly one fenced digest, its registry row says `v2`, and its digest ends with the sentence "A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings" (`grep -c "runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"` prints 1 in each).
- `grep -c "follow-up candidates" src/superclaude/rules/prompts/document_review_loop_prompts.md` prints 0 (the Medium wording left the file) and `grep -c "follow-up ledger"` prints 3 or more (the Grading check bullet and the two briefs); the pointer names `~/.claude/skills/sc-review-severity/refs/follow-up-ledger.md` before `.claude/skills/sc-review-severity/refs/follow-up-ledger.md`.
- `document_review_loop_prompts.md` holds no fenced digest (`grep -c "review-severity:digest"` prints 0), its registry row stays `pointer-only`, and the zero-finding sentence "If an input is missing or unreadable, return incomplete" and the sentence "not a minimum number of findings" are still in it.
- `cmp src/superclaude/rules/prompts/document_review_loop_prompts.md plugins/superclaude/rules/prompts/document_review_loop_prompts.md` prints nothing.
- `uv run pytest tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_registry.py tests/skills/test_review_brief_placement.py -v` passes.

## Task 3: Replace the merge rule in the builder and researcher skills

Depends on: Task 1

Edit the stage 4 merge-rule lines of spec section 10.3 to the L1 merge text (see Constraints): `src/superclaude/skills/tech-reference/SKILL.md` (two lines near 510 and 513; the one near 513 reads "Preserve the highest severity rating when duplicates disagree"), `src/superclaude/skills/readme/SKILL.md` (two lines near 542 and 547), `src/superclaude/skills/tdd/refs/build-request-template.md` (near line 122) and `src/superclaude/skills/operational-guide/SKILL.md` (near line 511). Remove those four files from the "Merge-rule allow-list" section of `src/superclaude/skills/sc-review-severity/refs/scale-map.md` in the same change (the section is where the stage 3 scan test reads its allow-list). Do not touch any cap sentence. The cap sentence is lower-case "after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" in one place of the tdd file and "After 2 fix cycles ..." elsewhere, so the checks below are case-insensitive.

Acceptance criteria:
- `grep -rniE "highest severity|more severe rating|higher severity|more severe" src/superclaude/skills/tech-reference src/superclaude/skills/readme src/superclaude/skills/tdd src/superclaude/skills/operational-guide` prints nothing.
- `grep -c "keeps every reviewer's own grade visible"` prints 2 for `tech-reference/SKILL.md`, 2 for `readme/SKILL.md`, 1 for `tdd/refs/build-request-template.md` and 1 for `operational-guide/SKILL.md`, and each of the four files names `sc-review-severity/refs/rule.md` with the `~/.claude/` form first.
- The cap text in each of the four files is unchanged: `grep -ci "after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings"` prints the same count as before the edit (today 5 for `tech-reference/SKILL.md`, 6 for `readme/SKILL.md`, 1 for `tdd/refs/build-request-template.md` and 2 for `operational-guide/SKILL.md`; re-count before editing).
- The "Merge-rule allow-list" section of `refs/scale-map.md` names none of the four files, and `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with them removed from it.

## Phase 3: Narrow spec-panel

## Task 4: Narrow spec-panel, name the ledger and re-pin the spec-panel pins

Depends on: Task 2

Edit `src/superclaude/commands/spec-panel.md` (re-read each line first; the lines are near 259, 260, 332, 372 and the `## Unattended mode` section near 455):
- Grading bullet (Review Loop bullet 2): change only the parenthesis "(a warning listed under `follow-up candidates`)" to "(a warning recorded in the follow-up ledger)". "CRITICAL is blocking" and "a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome" stay word for word, because the mapping test pins them.
- Verdict bullet (Review Loop bullet 3): "the report lists Medium and minor findings under `follow-up candidates`" becomes "the report lists Medium and minor findings in the follow-up ledger (rules: `~/.claude/skills/sc-review-severity/refs/follow-up-ledger.md`, else `.claude/skills/sc-review-severity/refs/follow-up-ledger.md`)", and "asks the user once per loop" becomes "asks the user once per run". "creates none without the user's answer" and "an `--unattended` run only records the list" stay. The Cap bullet stays word for word.
- FR-8 line (near line 332, "otherwise it is Medium (a warning listed under `follow-up candidates`)", reached by the same grep as the two bullets): the parenthesis becomes "(a warning recorded in the follow-up ledger)"; "It is blocking when it names a concrete wrong outcome", "otherwise it is Medium" and the FR-9 words "graded like FR-8" stay.
- The always-CRITICAL sentence near line 372 ("Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity") becomes "A dimensional mismatch identified by the Consistency Check is graded by the three blocking conditions of the shared rule (`~/.claude/skills/sc-review-severity/refs/rule.md`, else `.claude/skills/sc-review-severity/refs/rule.md`) and not by its label: it is blocking when its concrete scenario meets one of them and Medium otherwise." The next sentence, "The finding MUST include a concrete scenario demonstrating the mismatch", stays.
- `## Unattended mode` section: add one line, "**Follow-up ledger.**", saying that Medium and minor findings are recorded in `<report-dir>/follow-ups.md` (rules in `~/.claude/skills/sc-review-severity/refs/follow-up-ledger.md`, else the `.claude/` copy) and that the return contract carries `follow_up_ledger`, `follow_up_counts` and `follow_up_capture_state` as `~/.claude/WORKER-CONTRACT.md` states them (stage 2). The line names no `src/superclaude/` path and no `nested/` path, which `tests/skills/test_worker_contract.py` forbids in the section.

Edit `plugins/superclaude/commands/spec-panel.md` in place (the source and the plugin copy differ today, so do not copy one over the other) for the first three items only, the Grading bullet, the Verdict bullet and the FR-8 line near lines 257, 258 and 330, because the mapping test pins them on both files. The plugin copy has no `## Unattended mode` section and is not given one, and its dimensional-mismatch sentence stays (no existing test pins either on the plugin copy).

Then re-pin `tests/skills/test_review_severity_mapping.py`. First run `grep -n "follow-up candidates\|once per loop" tests/skills/test_review_severity_mapping.py`. The hits inside `test_grading_bullet_grades_by_consequence` and `test_verdict_bullet_routes_follow_up_candidates` (both parametrized over the source and the plugin spec-panel) are re-pinned here: the Grading literal becomes "otherwise it is Medium (a warning recorded in the follow-up ledger)", and in the Verdict literals "`follow-up candidates`" becomes "the follow-up ledger" and "asks the user once per loop" becomes "asks the user once per run". Every other literal in those two tests, including "CRITICAL is blocking", stays, and `test_fr8_fr9_grade_by_outcome_not_by_status_cell` needs no change. A hit inside `test_medium_tier_follows_the_untouched_s1_s5_bullets` is the output-style pin that the stage 3 package owns; leave it. If stage 3 already moved one of the spec-panel literals to other wording, take the spec-panel text from that pin and do not re-pin it again. Add one test to the same file for the source spec-panel only: it contains "A dimensional mismatch identified by the Consistency Check is graded by the three blocking conditions" and does not contain "is classified as **CRITICAL** severity".

Acceptance criteria:
- `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md plugins/superclaude/commands/spec-panel.md` prints nothing (this reaches the Grading bullet, the Verdict bullet and the FR-8 line in each file), and `grep -c "follow-up ledger"` prints 3 or more in each file.
- The narrowing is checked by content: `grep -c "is classified as \*\*CRITICAL\*\* severity" src/superclaude/commands/spec-panel.md` prints 0, the sentence "A dimensional mismatch identified by the Consistency Check is graded by the three blocking conditions" is present, and the Grading bullet still contains "CRITICAL is blocking".
- The `## Unattended mode` section of `src/superclaude/commands/spec-panel.md` contains `follow-ups.md`, `follow_up_ledger`, `follow_up_counts` and `follow_up_capture_state`, and `plugins/superclaude/commands/spec-panel.md` still has no such section.
- The existing `src/superclaude/examples/...` mention in `src/superclaude/commands/spec-panel.md` and in the plugin copy is left as it is (T3 does not check `pointer-only` rows for that path), and the registry row `commands/sc/spec-panel.md` stays `pointer-only` with the pointer text naming `~/.claude/skills/sc-review-severity/` before `.claude/skills/sc-review-severity/`.
- `uv run pytest tests/skills/test_review_severity_mapping.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py tests/skills/test_review_brief_placement.py tests/skills/test_worker_contract.py tests/skills/test_review_severity_registry.py -v` passes, and the cap sentence `at most 2 fix cycles (3 reviews)` is still in `src/superclaude/commands/spec-panel.md` and in the plugin copy.

## Phase 4: Make the drift scan strict and write the summary

## Task 5: Switch the drift scan to strict and run every pinning test once

Depends on: Task 1, Task 2, Task 3, Task 4

Before the switch, settle which files the strict scan can reach: run `git grep -n "review-severity:digest" -- src plugins` and `git grep -ln "Grade every review finding as blocking or minor" -- src plugins`, and write both outputs to `./artifacts/strict-t2-hits.md`. Every hit must be in a file that has a `digest` or `canonical` row. For any other tracked file under `src/` that holds the fence opener or the old sentence as a literal (for example a string in `src/superclaude/cli/doctor.py`, which stage 1 extends to read digest versions), reword it so the literal is built from parts, or record a named exemption in T2 and list it in that artifact. Then check that the registry ends in its final states: all 11 `digest` rows at `v2`, with the 1 `canonical`, 2 `pointer-only` and 5 `installed-only` rows unchanged; set any `digest` row still at `legacy` whose file now holds the digest. Then switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode, so a legacy definition sentence left in a tracked file under `src/` fails; if stage 1 left T2 also scanning `plugins/`, that scan passes today because no tracked plugin file holds the sentence or a fence, and no row or scan for a plugin path is added here. Run `make sync-dev` and `make verify-sync`, then run the pinning tests once, after the last edit of the package, so that no red test ships unseen.

Acceptance criteria:
- `./artifacts/strict-t2-hits.md` holds the output of both `git grep` commands and states, for every hit outside a `digest` or `canonical` file, the reword or the named exemption; when there is no such hit it says so.
- T2 of `tests/skills/test_review_severity_registry.py` is in strict mode, a temporary-tree case in that test shows a file under `src/` that holds the old definition sentence and has no registry row failing, and the registry has exactly 11 `digest` rows all at `v2`, 1 `canonical`, 2 `pointer-only` and 5 `installed-only`.
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_review_severity_registry.py tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_brief_placement.py tests/skills/test_review_loop_extension.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_worker_contract.py tests/skills/test_implement_severity_static.py tests/skills/test_review_brief_rests_on.py tests/review/test_review_rules_text.py -v` passes with strict T2, and its pass counts are noted for Task 6.
- `make verify-sync` passes.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` prints nothing; the five installed-only spec-panel variants are outside the repository scan and stay listed `installed-only`.
- No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`, and the files this package edited (listed in the Task 6 summary) include none of the retired carriers named in Constraints.

## Task 6: Write the stage 4 summary for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5

Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final results of the merge-rule scan, the registry tests with strict T2 and the full pinning run of Task 5 with their observed pass counts, the `make verify-sync` result, the files this package edited, and the revert command per row (the spec's three-step revert). Name the retired carriers left untouched by path (`exempt-by-retirement`), say that no plugin mirror, plugin parity test or plugin registry row was built and why (the owner's installation answer; the plan author's reassessment, not an owner decision), and list the open items. The last sentence of the file states that a second audit window is observed by the owner or operator and is not a task of this package.

Acceptance criteria:
- `./artifacts/stage4-summary-for-owner.md` lists every carrier row with its state (`v2` or the stated exception) and the test that pins it, and each named test file exists.
- The summary shows the observed pass counts of the full pinning run and of the scan and strict registry tests, and the `make verify-sync` result.
- The summary names the retired carriers left untouched, states that no plugin mirror was built and why, and states the revert command per row.
- The last sentence of the summary says that a second audit window is observed by the owner or operator and is not a task of this package.
`````

### .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md:1-45

`````markdown
# Stage 4 plan request: propagate the new rule to the remaining carriers (issue #552)

Last of five plan packages (see `stage-requests/README.md`). Generate it only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (the spec's section 13.2), the owner has read `./artifacts/stage3-summary-for-owner.md`, and the owner's go in chat is recorded in the stage ledger.

## Base text

Reuse Tasks 41 to 46 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 5, stage 4; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 4 parts). Earlier stages' evidence is read by package id.

## Changes to apply

- **Templates (the old Task 41).** The digest goes into four templates: `agent_template_qa.md`, `skill_template.md`, `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md`. `agent_template_analysis.md` gets the merge-rule text only (no digest, no registry row, no fence). The registry keeps exactly 11 `digest` rows. Acceptance: "four template files hold exactly one digest", the analysis template holds none and no `more severe rating` text, and `agent_template_qa.md` holds none of the "Any CRITICAL or IMPORTANT issue exists" FAIL bullet unless it is listed as a kept mechanical gate in `refs/scale-map.md`. Remove `agent_template_qa.md` and `agent_template_analysis.md` from the scan allow-list in the same change.
- **Rule prompts, builders and researchers, consumer line (the old Tasks 42 to 44).** As the base text, with the two `pointer-only` rows left at `pointer-only` and the cap sentences kept by content.
- **Spec-panel (the old Task 45).** As the base text; the existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` and its twins stays, since T3 does not check `pointer-only` rows for that path.
- **Plugin mirror (the old Task 46).** Order the work so the registry and the allow-list are correct BEFORE the copy: first add the plugin mirror of `refs/rule.md` to the `canonical` registry rows and to the allow-list in `refs/scale-map.md` (path only, no merge-rule phrases), then copy the skill folder to `plugins/superclaude/skills/sc-review-severity/`, then run T15 parity, strict T2 and the merge-rule scan. Acceptance includes `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passing, `make verify-sync` passing, and no `.claude/` path other than `.claude/settings.json` staged.
- **Constraints.** State this is stage 4 and the last package; strict T2 is switched on here. Acceptance lines that a later task of this package makes false get an end point.
- **New final task: stage 4 summary for the owner.** Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final scan and parity results, and the revert command per row (the spec's three-step revert), ending with the sentence that a second audit window is observed by the owner or operator and is not a task of this package.

## Not to be done by the plan

No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.

## Revision 2 (2026-11-16)

Plan edited in place after the pre-execution review (merged card, verdict NEEDS-REVISION, 2 blocking G1 and G2, 12 non-blocking G3 to G14) and the owner answers of 2026-11-16 (`OPEN-QUESTIONS.md` section 2). The plan file name, slug and frontmatter are unchanged. Shape: 7 tasks in 4 phases before, 6 tasks in 4 phases after.

Changes by finding or decision:

- **G1 (blocking), applied.** Task 1's check that the stage 3 summary "states that one audit window has passed" is removed (the summary is written before the window). The summary check is now: exists and quotes RT1, RT2 and M12. The window result is recorded in the owner's entry in the stage 4 `Owner go (date, where)` cell of the stage ledger, which the first check reads (date plus the statement that one audit window passed with no RT1 or RT2 tripped). The Constraints say so. G6: Task 1 now runs its first three checks before any edit.
- **G2 (blocking), applied.** Task 4 (was Task 5) names the pins it re-pins in `tests/skills/test_review_severity_mapping.py` (the Grading literal with `follow-up candidates`, the Verdict literals `follow-up candidates` and `once per loop`, both parametrized over the source and the plugin spec-panel), leaves the output-style pin to stage 3, adds the test to its run line, and names the FR-8 line (near line 332 of `spec-panel.md`, which the same grep reaches). A settling grep over the mapping test comes first, and if stage 3 already moved a pin the spec-panel text follows that pin.
- **G3 (MEDIUM), applied.** The last code task (Task 5) runs the whole pinning set once after the last edit, including `test_review_severity_rule.py`, `test_review_brief_placement.py`, `test_review_prompt_overrides.py`, `test_worker_contract.py`, `test_implement_severity_static.py` and `test_review_brief_rests_on.py`. The plugin rules-prompt byte copy moved into Task 2 so `test_review_brief_placement.py` is never red between tasks.
- **G4 (MEDIUM), removed by decision 4.** No plugin mirror to name. The plugin spec-panel is not given an Unattended section (it has none and no test pins one); the source line is the only Unattended edit.
- **G5 (MEDIUM), applied.** Task 4 quotes the new dimensional-mismatch sentence by content, requires the always-CRITICAL sentence to be gone, and keeps "CRITICAL is blocking" (pinned). One new source-only test pins the sentence.
- **G7, applied.** Tasks 1 and 3 name the "Merge-rule allow-list" section of `refs/scale-map.md` and add a grep check, because the scan test only checks that listed files exist.
- **G8, applied.** The cap checks in Task 3 are case-insensitive and give today's counts (5, 6, 1, 2).
- **G9, applied.** The L1 merge text is defined once in the Constraints and pinned by the phrase `keeps every reviewer's own grade visible`; the registry check names its pytest command; the consumer-line acceptance is gone with the task.
- **G10, applied.** Tasks 1 and 2 pin the digest's closing cap sentence by content in every digest carrier, and Task 2 checks that `follow-up candidates` left `document_review_loop_prompts.md` and `follow-up ledger` replaced it.
- **G11 and G12, removed by decision 4.** No plugin mirror, no T15 parity test, no plugin `canonical` row, no strict-T2 reverse scan of a plugin tree.
- **G13, applied.** Task 5 runs `git grep -n "review-severity:digest" -- src plugins` and the old-sentence grep before the strict switch, records the output in `./artifacts/strict-t2-hits.md`, and rewords or exempts any hit outside a `digest` or `canonical` file.
- **G14, applied.** (a) The label list near line 333 of `agent_template_qa.md` is checked against the Rule 6 heading that stage 3 gives `rf-qa-qualitative.md`. (b) The scale-map plugin copy no longer exists. (c) Task 1 checks that the stage 3 package is complete (done subfolder, or a `complete` ledger line per task). (d) Task 6 ends with the audit-window sentence as its last sentence.
- **Decision 1 (retired carriers), applied.** The old Task 4 (consumer line in `task-builder/SKILL.md` and the two MDTM templates) is dropped, and `rf-task-builder.md` is not edited. The MDTM templates stay only as digest carriers (they hold the old definition sentence and have registry rows). `tests/skills/test_task_builder_merge.py` is neither run nor re-pinned. The Constraints name the retired paths and the `exempt-by-retirement` allow-list entries (stage 1).
- **Decision 2, noted.** The spec-panel Verdict text moves from once per loop to once per run to match the output style; no question is added to any command.
- **Decision 4 (plugin surface), applied.** No mirror folder, parity test, plugin registry row or plugin reverse scan. Plugin twins are edited only where an existing test pins them: the rules prompt (byte copy) and the spec-panel Grading, Verdict and FR-8 lines. The registry keeps 11 `digest`, 1 `canonical`, 2 `pointer-only` and 5 `installed-only` rows. OPEN-QUESTIONS.md section 3.4: this is the plan author's reassessment and the owner has not confirmed removing plugin parity.
- **Decision 5, noted.** No task touches `src/superclaude/cli/review/ledger.py`.

Cross-stage facts: stage 1's T2 reverse scan is described as `src/` and `plugins/`; this package needs only `src/` strict, and the `plugins/` scan passes today because no tracked plugin file holds the old sentence. Stage 1's allow-list section must carry the `exempt-by-retirement` entries by path, and its registry must keep the 4 digest-bearing templates among the 11 `digest` rows. Stage 3's Task 8 must leave the spec-panel literals to this package or say it moved them.
`````

### .dev/reflect/pre-TASK-WF-blockerStage4-20261116-030206-20261116030426/adversarial/merged-review-card.md:21-67

`````markdown
## Verdict

NEEDS-REVISION: the stage 4 plan has 2 blocking findings (G1, G2) and 12 non-blocking findings (4 MEDIUM warnings G3 to G6 and 8 minor G7 to G14).

## Findings

G1 | blocking true | blocking | unpassable-check | Who: the `/sc:implement` executor and the QA reader of Task 1, and the owner who reads the ledger. Wrong result: Task 1 acceptance line P4:37 requires the stage 3 owner summary to state that one audit window has passed. The stage 3 plan writes that file before the window and says the window runs after the package, and no package edits it afterwards, so the check cannot be met: the run halts at Task 1, or QA passes it on a guess. The ledger has no column for window evidence, so even after P4:37 is re-pointed no file anywhere states that the window passed. Fix: keep the go-row check at P4:36 as the gate; change P4:37 to require that the summary exists and quotes RT1 and RT2 (stage 3 already requires that) and drop the clause that the window has passed; and say in the plan where the window result is recorded, either in the owner's go entry in the ledger cell `Owner go (date, where)` or in a new ledger column. | citations: P4:37 "exists and states that one audit window has passed with no revert trigger tripped"; S3:158 "State that the audit window runs after this package"; S3:162 "that no revert trigger can be judged until the audit window has run"; P4:36 "when the row has none, this check fails and the run halts"; S3:161 "quotes RT1, RT2 and M12 from the spec"; README:15 "Owner go (date, where)"
<!-- Source: V1 F1, V2 D2, V3 F1, INV-010, INV-018 -->

G2 | blocking true | blocking | contradiction | Who: the executor of Task 5 and the owner who reads a green run. Wrong result: Task 5 acceptance line P4:89 requires `follow-up candidates` to be gone from `spec-panel.md`, but `tests/skills/test_review_severity_mapping.py` pins that phrase, and the cadence phrase `once per loop`, in the Grading and Verdict bullets of both the source and the plugin spec-panel (lines 55, 58, 71 and 72). Task 5 runs two other tests (P4:88), Task 6 runs three others, and no stage 4 task re-pins or runs the mapping test, so it stays red or is silently relaxed. This is conditional on stage 3 Task 8 as written: S3:122 names no spec-panel text, S3:125 needs the mapping test green with spec-panel unchanged, and the stage 3 request forbids a spec-panel edit. The same grep also reaches the FR-8 line PANEL:332, which is outside Task 5's edit list; the FR-8 assertions at MAP:101-103 pin other wording ("graded like FR-8"), so a fix must not break them, but removing only the parenthetical does not fail them. Fix: state the condition and settle it with one grep after stage 3, `grep -n "follow-up candidates\|once per loop" tests/skills/test_review_severity_mapping.py`. A hit on a `SPEC_PANELS` test means Task 5 must say which MAP pins it re-pins (58 and 71 on both files, and 72 if still present) and must add the mapping test to the P4:88 and P4:102 runs; no hit means stage 3 moved the pins and the gap shrinks to "Task 5 does not run the mapping test". | citations: MAP:55 "CRITICAL is blocking"; MAP:58 "otherwise it is Medium (a warning listed under `follow-up candidates`)"; MAP:71 "`follow-up candidates`"; MAP:72 "asks the user once per loop"; MAP:101-103 "graded like FR-8"; PANEL:259 "otherwise it is Medium (a warning listed under `follow-up candidates`)"; PANEL:332 "otherwise it is Medium (a warning listed under `follow-up candidates`)"; P4:89 "prints nothing and the ledger is named instead"; P4:88 "tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py -v"; S3:122 "the Medium and cadence pins move from \"once per loop\" to the once-per-run wording"; S3:125 "tests/skills/test_review_severity_mapping.py"; S3REQ:20 "No template, rule-prompt, builder, researcher or spec-panel edit (stage 4)"; ADV/debate/round2-advocate-2.md:39 "They do not themselves require the follow-up-list parenthetical"; ADV/debate/round2-advocate-3.md:63 "A hit on a `SPEC_PANELS` test means the 4 parametrized cases fail after Task 5 (blocking holds)."
<!-- Source: V1 F2, V1 F5, INV-019, Round 2 evidence (round2-advocate-2 section 1, round2-advocate-3 sections 2 to 4) -->

G3 | blocking false | MEDIUM | missing-requirement | Who: the executor of Tasks 1, 2, 4 and 5, and the owner who reads a closing run. Wrong result: none is demonstrated, but pinning tests that read stage 4 files are never run after the last edit to those files, so a red test can ship unseen. The named gaps: `test_review_severity_rule.py` (its file list holds all 8 stage 4 digest carriers and is never re-run after the rows move to `v2`); `test_review_brief_placement.py:134` (the plugin rules prompt must stay a byte copy of `document_review_loop_prompts.md`, while Task 2 edits the source and Task 5 edits the plugin twin in place); `test_review_prompt_overrides.py` (run in Task 2 only, though Tasks 3 to 5 touch files it pins); `tests/skills/test_worker_contract.py` (it reads the `## Unattended mode` section that Task 5 edits); and Task 4, which runs only the task-builder test after Task 1 has put the digest in the MDTM templates. Fix: one final run in Task 6 of `uv run pytest tests/skills tests/review`, or of the named list above. The probe raised this from minor to MEDIUM. | citations: INV-008 ADV/invariant-probe.md:17 "No P4 line runs a suite; the only pytest lines are P4:41,55,63,74,88,102."; tests/skills/test_review_brief_placement.py:134 "assert bundled.read_bytes() == RULES_FILE.read_bytes()"; P4:84 "edit each file in place and do not copy one over the other"; tests/skills/test_review_severity_rule.py:181-187 "S1_S3_FILES"; S3:122 "`S1_S3_FILES` and its `[:6]` slice `S5_FILES` become registry rows of kind `digest`"; tests/skills/test_review_prompt_overrides.py:283 "assert \"no minimum count\" in flat, rel"; P4:55 "tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_registry.py -v"; P4:74 "`uv run pytest tests/skills/test_task_builder_merge.py -v` passes."; tests/skills/test_worker_contract.py:893 "def _unattended_section(name: str) -> str:"; P4:102 "passes with strict T2"
<!-- Source: V1 F6, V3 F4, INV-008, INV-016, INV-020 -->

G4 | blocking false | MEDIUM | missing-requirement | Who: the executor of Task 5 and the plugin-only user. Wrong result: none is demonstrated, but Task 5 cannot be applied to the plugin twin as worded. P4:84 orders that the Unattended mode section gains one line and that the same edits go to `plugins/superclaude/commands/spec-panel.md`, yet that file has no `## Unattended mode` section (the source has it at PANEL:455), so the executor must invent a section or skip the clause. P4:84 also never orders the pointer that P4:90 expects (the source `spec-panel.md` has no reference to `sc-review-severity` today). And no plugin carrier can name the plugin mirror that Task 6 adds: the pointer names installed paths first and project `.claude/` second (P4:25), and the plugin prompts twin must stay a byte copy (test_review_brief_placement.py:134), so it cannot carry a plugin-root path; the precedent is the `${CLAUDE_PLUGIN_ROOT}` fallback pinned at test_review_brief_placement.py:129-138. A plugin-only run whose ledger or offer step cannot read the pointer records `capture_state: incomplete`. Fix: Task 5 states where the plugin twin carries the Unattended line (it has no such section) and orders the pointer text that P4:90 expects; the plan states how a plugin carrier names the plugin mirror under the byte-copy rule, using the `${CLAUDE_PLUGIN_ROOT}` fallback as the precedent. | citations: P4:84 "the Unattended mode section gains one line for the ledger and the three contract keys"; P4:84 "Apply the same edits to the hand-kept twins `plugins/superclaude/commands/spec-panel.md`"; PANEL:455 "## Unattended mode"; ADV/invariant-probe.md:15 "a diff of `^## ` headings shows PPANEL has no such section"; P4:90 "The plugin twins carry the same pointer and ledger sentence as their source twins"; S1:209 "a `pointer-only` row only once its pointer is present"; P4:25 "Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path."; tests/skills/test_review_brief_placement.py:134 "assert bundled.read_bytes() == RULES_FILE.read_bytes()"; tests/skills/test_review_brief_placement.py:137 "`${CLAUDE_PLUGIN_ROOT}/rules/prompts/document_review_loop_prompts.md`"; ADV/invariant-probe.md:16 "a plugin-only run whose ledger or offer step cannot read the pointer records `capture_state: incomplete`"; ADV/variant-1-original.md:21 "which has zero references to `sc-review-severity` today"
<!-- Source: V1 F7, INV-006, INV-007 -->

G5 | blocking false | MEDIUM | missing-requirement | Who: the executor of Task 5 and the owner. Wrong result: none is demonstrated, but Task 5's narrowing is not checked. The parenthesis in P4:84 restates today's Grading bullet (PANEL:259 already says CRITICAL is blocking and a MAJOR is blocking only if it names a concrete wrong outcome), so for that bullet the narrowing is a no-op, and no acceptance line (P4:87 to P4:90) checks that the always-CRITICAL sentence at PANEL:372 changed. Task 5 can pass with only the `follow-up candidates` rename, while stage 4 of the spec requires the narrowing. Fix: add an acceptance line to Task 5 that quotes the new dimensional-mismatch sentence by content and shows the always-CRITICAL wording is gone, and keep the `CRITICAL is blocking` wording that the mapping test pins on both surfaces (this folds into G2). | citations: SPEC:739 "narrow \"CRITICAL is blocking\" and the always-CRITICAL dimensional mismatch (`spec-panel.md:372` [E]) to the three conditions"; P4:84 "CRITICAL stays blocking, a MAJOR stays blocking only when it names a concrete wrong outcome"; PANEL:259 "CRITICAL is blocking; a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome"; PANEL:372 "Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity"; MAP:55 "CRITICAL is blocking"
<!-- Source: INV-012 -->

G6 | blocking false | MEDIUM | safety | Who: the owner. Wrong result: none is demonstrated, but the two gate checks sit in Task 1's acceptance lines (P4:36 and P4:37), which QA reads after the five template edits and the allow-list change (P4:33) are already on disk. With G1 unfixed, P4:37 halts the run after those edits exist, and the plan cannot then be corrected and resumed in place because `/sc:implement` fails on a plan changed after its first task; the package would have to be regenerated with the edits already applied. Fix: correct the plan (G1 and G2) before the first task runs, and read the go row and the summary before the first template edit. The probe raised this from minor to MEDIUM in combination with G1. | citations: P4:33 "remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of the stage 3 scan test"; P4:36 "when the row has none, this check fails and the run halts"; P4:37 "exists and states that one audit window has passed with no revert trigger tripped"; README:3 "fails on a plan changed after its first task"
<!-- Source: V1 F8, INV-017 -->

G7 | blocking false | minor | other | Who: the executor of Tasks 1 and 3. Wrong result: both tasks name "the allow-list of the stage 3 scan test", but that test holds no list. It reads the "Merge-rule allow-list" section of `refs/scale-map.md`, and it only checks that each listed file exists, so a forgotten removal never turns a check red and an executor may hunt for a list in the test file or add one there. Fix: name that section of `refs/scale-map.md` in both tasks. | citations: P4:33 "remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of the stage 3 scan test"; P4:59 "remove those four files from the allow-list of the stage 3 scan test"; S3:144 "The allow-list is read from the \"Merge-rule allow-list\" section of `refs/scale-map.md`"; S3:149 "a test fails when a file named there does not exist"; S1:59 "so the stage 3 scan test reads its allow-list from one place"
<!-- Source: V1 F3, V3 F5 -->

G8 | blocking false | minor | unpassable-check | Who: a literal-minded QA reader of Task 3. Wrong result: P4:64 says each of the four files still contains its "After 2 fix cycles" sentence, which fails a case-sensitive grep for the tdd file because it holds only the lowercase "after 2 fix cycles" at line 125. Fix: quote the cap sentence per file as it stands today, or say the match is case-insensitive. | citations: P4:64 "each file still contains its \"After 2 fix cycles\" sentence"; src/superclaude/skills/tdd/refs/build-request-template.md:125 "after 2 fix cycles (3 reviews), HALT and escalate"; src/superclaude/skills/tech-reference/SKILL.md:538 "After 2 fix cycles"
<!-- Source: V1 F4 -->

G9 | blocking false | minor | other | Who: the QA reader. Wrong result: several acceptance lines pin no content or command, which conflicts with the by-content pin rule at P4:24. "T1 passes for them" (P4:39) names no pytest command; "the L1 merge text" (P4:33) is a spec change description, not a sentence; Task 4's "contain the consumer-line instruction" (P4:73) has no quoted form. Fix: name the pytest command in P4:39, and quote the sentence or the expected text for the L1 merge line and the consumer-line instruction. | citations: P4:24 "Pins are by content."; P4:39 "T1 passes for them"; P4:33 "the L1 merge text"; P4:73 "contain the consumer-line instruction"; SPEC:270 "L1 | **[REQ-05]** The consolidator grades by the rule"
<!-- Source: V1 F9, V3 F4 (first half) -->

G10 | blocking false | minor | missing-requirement | Who: the Task 2 executor and reviewer. Wrong result: Task 2's acceptance lines (P4:53 to P4:55) check the digests, the registry states, the pointer-only row, the named tests and the zero-finding wording, but none pins the cap sentences by content as the request asks (SRC4:12), while sibling Tasks 3 and 4 spell it out (P4:64, P4:70). No line checks that `document_review_loop_prompts.md` lost the Medium wording either: RLP:32 still holds `follow-up candidates`, and only Task 5 has a removal check (P4:89, for spec-panel). This is incomplete checking, not an unprotected cap, because digest equality already ties the cap content to the canonical digest. Fix: add a cap-sentence line to Task 2 and a check that the Medium wording left `document_review_loop_prompts.md`. | citations: SRC4:12 "the cap sentences kept by content"; P4:55 "the zero-finding and \"no minimum count\" sentences still exist"; P4:50 "the Medium wording near lines 31, 32 and 48 becomes the pointer and the ledger sentence inside an existing section"; RLP:32 "list Medium and minor findings under follow-up candidates"; P4:89 "prints nothing and the ledger is named instead"; P4:64 "The cap text in each of the four files is unchanged"; P4:70 "Keep the cap sentence in `src/superclaude/skills/task-builder/SKILL.md`"; ADV/debate/round2-advocate-2.md:61 "S1:46 and :50 require the canonical digest to end with the cap"
<!-- Source: V2 D3, INV-016 -->

G11 | blocking false | minor | other | Who: the Task 6 executor and its QA. Wrong result: strict T2 scans only git-tracked files, and Task 6 copies the new plugin folder by hand and never stages it, so the reverse-scan half of the P4:102 claim ("accepted by the reverse scan through its `canonical` row") passes without reading the plugin mirror. The merge-rule scan half is a real check, because that scan selects files by directory. No wrong result follows, because the T15 parity test ties the mirror to the scanned source. Fix: stage `plugins/superclaude/skills/sc-review-severity/` before the three-test run, or make T2 read the filesystem. | citations: S1:209 "a reverse scan of the tracked `src/` and `plugins/` trees"; tests/skills/test_review_severity_rule.py:39 "[\"git\", \"ls-files\", \"-z\", \"--\", *_SCAN_TREES],"; P4:102 "the plugin mirror of `refs/rule.md` is accepted by the reverse scan through its `canonical` row"; P4:99 "copy `src/superclaude/skills/sc-review-severity/` to `plugins/superclaude/skills/sc-review-severity/` by hand"; S3:144 "reads Markdown files only (`*.md`)"; ADV/variant-3-original.md:11 "T15 parity ties the mirror to the source"
<!-- Source: V3 F2 -->

G12 | blocking false | minor | contradiction | Who: the Task 6 executor editing `registry.yaml` (conditional on the stage 1 registry test and resolver). Wrong result: a registry row holds a path relative to the install root plus a list of surfaces, and `plugin` is already a surface value; Task 6 instead adds a second `canonical` row with a repo path. That row would repeat the logical path of the existing `rule.md` row, T1 and T3 may resolve the wrong file, and the executor must guess between adding `plugin` to the existing row and adding a new row. Stage 1 also pins one `canonical` row and 19 rows in all, and T1 reads the `canonical` row in the singular; if stage 1 codifies those counts in its test, P4:102 fails and Task 6 names only the strict-T2 switch as an edit to that test. The ambiguity starts in S1:96. Fix: Task 6 says whether the mirror is a `plugin` surface on the existing row or a second row, and if a second row, updates the stage 1 count pins. | citations: S1:96 "Each row has the logical path relative to the install root, a `kind`"; S1:96 "One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; the stage 4 package adds its plugin mirror)"; P4:99 "(`plugins/superclaude/skills/sc-review-severity/refs/rule.md`) as a `canonical` row"; S1:100 "1 of kind `canonical`"; S1:100 "19 rows in all"; S1:209 "the `canonical` row holds the source digest"
<!-- Source: V3 F3, INV-005 -->

G13 | blocking false | minor | missing-requirement | Who: the Task 6 executor (conditional; promote to blocking if the settling grep below hits). Wrong result: strict T2 fails on any tracked file under `src/` or `plugins/` that holds the old definition sentence or a fence opener and has no registry row, Python files included. Stage 1 adds a doctor check that reads the digest versions of installed carriers, so it has to recognise the fence line, and if `doctor.py` or another unregistered tracked file holds the opener literal or the old sentence, P4:102 and the grep at P4:104 cannot pass and no task names the edit that would fix it (register, exempt or reword the file). Nothing prints today because stage 1 has not run; a matcher built from parts would not trip it, a literal string would. Fix: before the strict switch in Task 6, run `git grep -n "review-severity:digest" -- src plugins` (and the same for the old sentence) and, for every hit outside a `digest` or `canonical` row, register the file or record a named exemption in T2. | citations: S1:209 "on any file that holds the old definition sentence or a fence opener and has no registry row of any kind"; S1:209 "strict mode is a switch, off in this phase"; S1:197 "compares the digest versions held by the installed carriers"; P4:99 "switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode so any legacy definition sentence left in `src/` or `plugins/` fails"; P4:104 "prints nothing; the five installed-only spec-panel variants are outside the scan"; ADV/debate/round2-advocate-3.md:79 "A regex built from parts would not trip it; a literal string would."
<!-- Source: Round 2 N-1 (round2-advocate-3 section 5), INV-014 -->

G14 | blocking false | minor | missing-requirement | Who: the executors of Tasks 1, 6 and 7, and the owner. Wrong result: four small gaps, none a wrong result by itself. (a) Task 1's edit "per OD16" near `agent_template_qa.md:333` has no check: that line is one list line of rule labels, not the text the spec calls "the same Rule 6 text", and the grep at P4:40 covers only the FAIL bullet, so the line can stay unchanged while every acceptance line passes. (b) `refs/scale-map.md` carries repo paths (`src/superclaude/...`) in its allow-list section and Task 6 copies it into the plugin, against P4:25; the T3 path check covers only `digest` and `canonical` rows, so nothing checks that file. (c) No Task 1 line reads that the stage 3 package is done (P4:20 requires it): the summary exists even when stage 3 ends failed, and a package can be generated yet marked NEEDS-REVISION; the owner's go is the backstop. (d) Task 7 does not say the audit-window sentence ends the summary, as the request specifies. Fix: (a) add an acceptance line quoting the new Rule 6 text; (b) check the plugin copy of `refs/scale-map.md` for repo paths or label them as maintainer notes; (c) add a line that reads the stage 3 `progress.md` or its location in `done/`; (d) say in Task 7 that the audit-window sentence is the last sentence of the summary. | citations: P4:33 "the Rule 6 text near line 333 per OD16"; P4:40 "grep -c \"Any CRITICAL or IMPORTANT issue exists\""; SPEC:855 "the same Rule 6 text"; S3:144 "`src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, `src/superclaude/skills/sc-review-severity/refs/rule.md`"; P4:25 "never a `src/superclaude/` path"; ADV/invariant-probe.md:24 "T3's path check covers only `digest` and `canonical` rows (S1:209), so nothing checks `scale-map.md`."; P4:20 "It runs only after the stage 3 package is done"; README:17 "its pre-execution review says NEEDS-REVISION"; P4:111 "State that a second audit window is observed by the owner or operator and is not a task of this package, and list the open items."; SRC4:16 "ending with the sentence that a second audit window is observed by the owner or operator and is not a task of this package"; ADV/variant-2-original.md:48 "Its wording does not require the audit-window sentence to be the final sentence, as the request specifies"
<!-- Source: INV-013, INV-015, INV-011, V2 note (Task 7 ordering) -->
`````

### .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/artifacts/codegraph-grounding.md:1-59

`````markdown
# Codegraph grounding for TASK-WF-blockerStage4-20261116-030206

## Run state

- index_state: fresh
- checked_at: 2026-11-16T03:03:44Z (`codegraph_status`: 3570 files, "Changes since index: 0 added, 0 modified, 0 removed")
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- access: mcp
- degraded tokens: none
- note: the index covers Python, YAML, JavaScript and TypeScript, not Markdown. The skill, agent, template, rule-prompt and command files this plan edits were resolved with Grep and Read from the base grounding of `TASK-WF-loosenBlockerRev-20261115-210254` (read 2026-11-15) plus a `test -e` check today; no symbol lookup beyond that was repeated for this package.

## Resolved symbols

- Four digest templates under `src/superclaude/templates/` (`documents/agent_template_qa.md` merge rule near 85, `skill_template.md` near 828, two MDTM templates near 644 and 655) and `agent_template_analysis.md` (merge-rule text only); four rule prompts near lines 11, 27, 28, 27; the builder and researcher skills (`tech-reference`, `readme`, `tdd/refs/build-request-template.md`, `operational-guide`); `commands/spec-panel.md` and its plugin twin. Line numbers are from the base grounding and Task 1 of the base plan; every task re-reads before editing.
- `plugins/superclaude/skills/` holds 4 entries today (`confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`); the mirror folder is new.
- Existing paths named in the plan (`test -e` today): 16. Paths named that do not exist yet: 6: `plugins/superclaude/skills/sc-review-severity/`, `plugins/superclaude/skills/sc-review-severity/refs/rule.md`, `src/superclaude/skills/sc-review-severity/`, `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, `tests/skills/test_review_severity_plugin_parity.py`, `tests/skills/test_review_severity_registry.py`.

## Dependents

- Plugin twins (hand-kept, differ from source): `plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`.
- Installed-only spec-panel variants in `~/.claude/commands/sc/` (`spec-panel-armb.md`, `-diffgate.md`, `-ledger.md`, `-ponytail.md`, `-stoprule.md`) are outside the scan and stay `installed-only`.
- `make verify-sync` covers `src/` to `.claude/`; the plugin mirror is checked by the new parity test.

## Pre-check

Checked 2026-11-16 with `test -e` over the 22 distinct `src/`, `tests/`, `plugins/` paths the plan names in backticks: 16 exist and 6 do not. Every absent path is a file or folder this package creates or one an earlier package creates (the stage 1 modules and tests, the skill folder `sc-review-severity`, the stage 2 `test_review_brief_rests_on.py`); the first task of each of stages 2, 3 and 4 checks the earlier package's evidence by package id before anything else runs. No named existing path is missing.
Plan edits made during this pre-check. The protocol says the pre-check never edits the plan; this run did edit it after the generator wrote it and before the gate and the reflect call, to remove wording the gate rules reject: the literal task-folder prefix in the Constraints line for the spec, and leftover cross-package task numbers (a Phase or Task number of the old 46-task plan, replaced by the stage 3 package's name). No reflect finding drove these edits.
Not checked: the quoted line numbers in task bodies (they come from the 2026-11-15 grounding and each task re-reads before editing); that the old 46-task plan's task text is unchanged since extraction (it is the base text, extracted once on 2026-11-16).

## Revision 2 (2026-11-16)

Re-checked against the live files in the worktree on 2026-11-16 (Markdown carriers are not in the codegraph index, so Grep, `git grep` and Read were used; `codegraph_status` was not repeated because no symbol lookup was needed).

Existence (`test -e` over 38 paths named in the revised plan): 29 exist (all 5 templates, the 5 rule prompts, the 4 builder and researcher skill files, `src/superclaude/commands/spec-panel.md` and the two plugin twins, `rf-qa-qualitative.md`, `doctor.py`, 9 existing test files, `OPEN-QUESTIONS.md`, `~/.claude/WORKER-CONTRACT.md`); 9 do not exist yet and are created by earlier stages: `src/superclaude/skills/sc-review-severity/` with `refs/rule.md`, `refs/registry.yaml`, `refs/scale-map.md`, `refs/follow-up-ledger.md` (stage 1), `tests/skills/test_review_severity_registry.py` and `tests/skills/test_review_merge_rule_scan.py` (stages 1 and 3), `tests/skills/test_review_brief_rests_on.py` (stage 2). The plugin paths of the old plan (`plugins/superclaude/skills/sc-review-severity/...`, `tests/skills/test_review_severity_plugin_parity.py`) are no longer named.

Facts re-read (commands):
- `git grep -l "Grade every review finding as blocking or minor" -- src plugins` prints exactly the 11 digest carriers (none under `plugins/`); `git grep -n "review-severity:digest" -- src plugins` prints nothing today.
- `git grep -n "follow-up candidates" -- src plugins` hits 3 in `src/superclaude/commands/spec-panel.md`, 3 in the plugin twin, 3 in each `document_review_loop_prompts.md` and 1 in `pragmatic.md` (stage 3). `git grep -n "follow-up candidates\|once per loop" -- tests` hits `tests/skills/test_review_severity_mapping.py` (Grading literal, Verdict literals, the output-style cadence pin) and one unrelated fixture.
- `cmp` of the two `document_review_loop_prompts.md` copies prints nothing (byte-identical); `tests/skills/test_review_brief_placement.py` asserts the byte copy.
- The plugin `commands/spec-panel.md` has no `## Unattended mode` heading (`grep -n "^## "`); the source has it near line 455. `tests/skills/test_worker_contract.py` forbids `src/superclaude/` and `nested/` in that section.
- Cap sentence counts (`grep -ci`): tech-reference 5, readme 6, tdd 1 (lower-case "after"), operational-guide 2. HALT-line counts: `agent_template_qa.md` 2, 01 template 5, 02 template 6. Each of the 8 digest carriers holds the cap phrase once today.
- Merge-rule lines match the plan: 6 lines in the four skills (tech-reference 510 and 513, readme 542 and 547, tdd 122, operational-guide 511), plus `agent_template_qa.md:85` and `agent_template_analysis.md:466`.
- Label list near `agent_template_qa.md:333` holds "Contradictions are always IMPORTANT or CRITICAL" in an example comment; `rf-qa-qualitative.md:990` holds Rule 6 today (stage 3 rewrites it).
- `git diff --name-only HEAD -- src/superclaude/skills/task src/superclaude/skills/task-builder src/superclaude/agents/rf-task-builder.md` prints nothing.

Findings:
- G1 applied (summary check reduced; window result read from the stage ledger go cell; checks run before the first edit).
- G2 applied (pins named, mapping test added to the run lines, FR-8 line named; conditional on stage 3 settled by a grep first).
- G3 applied (final pinning run in Task 5; plugin byte copy moved into Task 2).
- G4 not needed (decision 4: no plugin mirror; plugin spec-panel gets no Unattended section).
- G5 applied (acceptance by content plus one source-only test).
- G6 applied (checks before the first edit).
- G7 applied. G8 applied (case-insensitive counts verified above). G9 applied. G10 applied.
- G11 and G12 not applied: the plugin mirror, parity test and plugin `canonical` row are removed by decision 4.
- G13 applied (settling `git grep` before the strict switch; both print nothing or only registered files today).
- G14 applied for (a), (c), (d); (b) is moot (no plugin copy of `scale-map.md`).
- Decision 1 applied (old Task 4 dropped; `rf-task-builder.md` and `task-builder/SKILL.md` not edited; `test_task_builder_merge.py` not run).
- Not verified: whether stage 3's Task 8 moves the spec-panel literals in the mapping test (its text names none), so Task 4 settles that with a grep at run time; the exact wording of Rule 6 after stage 3 (Task 1 reads it then).
`````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:758-770

`````markdown
**[REQ-26]** Delivery rules:

1. **First install.** The new skill folder reaches an existing `~/.claude` without `--force`, because the folder does not exist there yet.
2. **Every later change** to that folder, to `pragmatic.md` or to a rule prompt stays stale on an installed machine until `superclaude update` or an install with `--force`.
3. **A stage switch or a revert is three steps, never "a registry edit":** (a) in the repository, edit the affected carriers' digests and registry rows and re-run the drift tests; (b) ship a release whose note names the refresh command; (c) refresh each machine (`superclaude update` or install with `--force`), confirmed by the install check.
4. **There is no immediate brake.** The three-step revert is the only brake. The safety revert trigger RT1 acts through it. Machines that are not refreshed keep the new rule until they are; this is residual risk RK14, mitigated by the release note and the install check. A brake that needs no reinstall would be a new design: a named file that every carrier digest reads, with its format, writer and precedence stated (OD17).
5. **[REQ-27] Install check.** A `make doctor` check, backed by a pytest test, compares the digest versions held by the installed carriers with the packaged (source) registry and reports mismatches. It reads the packaged registry, not an installed `registry.yaml`, because the installed skill folder is skipped once present (`install_skills.py:102`) [V]. A `doctor` target already exists (`Makefile:23`) [V, this merge]. Each ledger header records the digest versions its carriers held (section 6.2).

### 9.5 Plugin surface

<!-- Source: Variant 1 (opus:architect), decision D9 - merged per Change #PC-05 -->

The plugin tree has no output-style hook: a Grep for `pragmatic` under `plugins/superclaude` finds no file [V: LC-09]. Its carriers of blocking text are `commands/spec-panel.md`, `rules/prompts/document_review_loop_prompts.md` and `skills/sc-implement-protocol/refs/qa.md` [V: invariant probe]. These hold the inline digest. At stage 4 a hand mirror of the skill folder goes into `plugins/superclaude/skills/` with a parity test (T15); the plugin's `skills/` is hand-kept and holds 4 skills today [V: LC-20]. Until then the release note says plugin-only users keep today's text.
`````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:786-885

`````markdown
- `Grade every review finding as blocking or minor` (the definition sentence, S1): 11 files, 11 matching lines [V].
- `Blocking is a real defect` (both cases): 11 files, 11 occurrences [V: invariant probe]. The seed brief's "12 occurrences" is not reproduced.
- `Minor findings never fail a review` (S2): 11 files [V: Variant 1 check].
- `at most 2 fix cycles \(3 reviews\)` (the cap, S3): 12 files, the 11 plus `commands/spec-panel.md` [V].
- `CRITICAL and IMPORTANT findings are blocking` (S5): 7 files [V].
- `follow-up candidates`: 3 files, 7 matching lines [V].
- `2 fix cycles`: 22 files, 120 matching lines, 139 occurrences (a line can hold more than one) [V]. Most of these carry the cap, not the definition.
- Merge rule, case-insensitive: `highest severity|more severe`, then `higher severity|max(imum)? severity|worst (severity|rating)|highest (rating|grade)` [V: LC-04]. Results in section 10.3.
- Fixed FAIL triggers: the frozen Grep of section 10.4.
- Tasklist: "High or Medium" or "Medium (blocking)" in `skills/sc-tasklist-protocol/SKILL.md`: 7 lines [V].
- Plugin tree: the definition sentence 0 files; merge-rule patterns 0 matches [V].
- Method caveat: the Grep tool skips gitignored folders, so it reports 0 copies under the project `.claude/`; a plain `grep -rlF` finds 6 copies of S1 there (rf-qa, rf-qa-qualitative, 2 document templates, 2 MDTM templates) [V: diff analysis]. Any plan step that counts `.claude/` copies must not use the Grep tool.

### 10.1 The 11 files that carry the definition

| File | Line | Group |
|---|---|---|
| `output-styles/pragmatic.md` | 225 | output style; reaches every subagent. Also lines 221 (reviewer brief) to 231 [V: Read] |
| `agents/rf-qa.md` | 108 | QA agent |
| `agents/rf-qa-qualitative.md` | 108 | QA agent |
| `templates/documents/agent_template_qa.md` | 161 | template |
| `templates/documents/skill_template.md` | 828 | template |
| `templates/workflow/01_mdtm_template_generic_task.md` | 644 | template |
| `templates/workflow/02_mdtm_template_complex_task.md` | 655 | template |
| `rules/prompts/automated_qa_workflow_qa_prompt.md` | 11 | QA prompt |
| `rules/prompts/doc_code_analyst_qa_prompt.md` | 27 | QA prompt |
| `rules/prompts/documentation_expert_qa_prompt.md` | 28 | QA prompt |
| `rules/prompts/recruiting_expert_qa_prompt.md` | 27 | QA prompt |

Each is a carrier: at its stage it replaces S1, S2 and S5 (where present) with the digest and pointer line; the cap text stays word for word.

### 10.2 Variants and carriers of the Medium mechanism

| File | What it carries | Pattern and count |
|---|---|---|
| `commands/spec-panel.md` | own scale; Review Loop bullets at lines 259 to 261 [V]; FR-8 at 332 [E] | `follow-up candidates`: 3 matches |
| `rules/prompts/document_review_loop_prompts.md` | reviewer briefs; Medium wording at 31, 32, 48 [E] | `follow-up candidates`: 3 matches |
| `output-styles/pragmatic.md` | Medium and the spec-panel scale at 230 to 231 [V] | `follow-up candidates`: 1 match |
| `cli/review/card_convert.py` | word translator, lines 71 to 83 [V] | no change |

The plugin copies of the first two files exist; `spec-panel.md` differs between `src` and the plugin, and the review-loop prompts are identical [V: diff analysis, `cmp`].

### 10.3 "Highest severity wins": 13 lines in 10 files

**[REQ-05, location]** Label-max merging is replaced at all of these lines, in two stages [V: LC-04]:

| File | Lines | Stage |
|---|---|---|
| `skills/task/SKILL.md` | 252, 361 | 3 |
| `agents/rf-qa.md` | 83 | 3 |
| `agents/rf-qa-qualitative.md` | 84 | 3 |
| `agents/rf-analyst.md` | 75 | 3 |
| `skills/tech-reference/SKILL.md` | 510, 513 | 4 |
| `skills/readme/SKILL.md` | 542, 547 | 4 |
| `skills/tdd/refs/build-request-template.md` | 122 | 4 |
| `skills/operational-guide/SKILL.md` | 511 | 4 |
| `templates/documents/agent_template_qa.md` | 85 | 4 |
| `templates/documents/agent_template_analysis.md` | 466 | 4 |

Not changed: `skills/sc-auggie-review-protocol/SKILL.md:228` ("keep the higher severity") is a code-review de-duplication on its own scale, a scale-map row unchanged in version 1. `cli/roadmap/remediate_parser.py` (lines 55, 301, 365) assigns severity in code and is out of scope with the roadmap checkers. `cli/pipeline/fmea_classifier.py` and `pr_submit/severity_router.py` rank unrelated things [V: LC-04]. An earlier draft said the rule also sits in task-builder and tech-research; the Grep does not show that, and the claim is withdrawn. The reverse-scan test T5 searches `src/` and `plugins/` for `highest severity`, `more severe rating` and `higher severity`, with the scale-map rows as its allow-list.

### 10.4 Fixed FAIL triggers in the QA agents

**[REQ-30]** The stage 0 inventory of fixed FAIL lines is a frozen Grep, not a remembered list. Patterns: `= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT`, run over `src/superclaude/{agents,skills,templates,rules}` at stage 0 and stored with the stage 0 results. Lines known today:

| File | Lines | Stage | Treatment (L6) |
|---|---|---|---|
| `agents/rf-qa.md` | 152 ("Any incomplete file = FAIL"), 162 ("Any untagged doc claim = FAIL"), 168 to 170 ("Will this gap reduce report quality? -> IMPORTANT"; "Any CRITICAL or IMPORTANT gap = overall FAIL"), 182 to 183 (PASS or FAIL by label), 327 ("Flag exact duplicates as IMPORTANT"), 389 and 476 (count CRITICAL and IMPORTANT as blocking) [V: LC-13]; also 221, 316, 333, 334 [V, this merge] and 494, 548 [E: plan review] | 3 | each rewritten to "grade by the three conditions; the label is information", or kept as a named mechanical gate mapped to condition 2 (Missing) when a template requires the item (likely for 152 and 162), with the keep recorded in the scale map; 327 becomes Note unless a condition holds |
| `agents/rf-qa-qualitative.md` | 990, Rule 6: "Contradictions are always IMPORTANT or CRITICAL ... that's never minor" [V, this merge] | 3, if OD16 says so | OD16: keep as a named mechanical gate mapped to condition 1, or rewrite so a contradiction nothing rests on is a follow-up. Until decided, Rule 6 stays and metric M12 notes it as a known counter-example |
| `templates/documents/agent_template_qa.md` | 333 (the same Rule 6 text) [V, this merge] | 4 | follows OD16 |

`tests/audit/test_severity_floor_unweakened.py` pins Rule 6 verbatim and hashes the whole `## Critical Rules` block of rf-qa-qualitative and its `.claude/` mirror (lines 53 to 61 and 166 to 189) [V, this merge]. `tests/audit/test_nfr_conv_9_zero_trust.py` pins rf-qa's PASS and FAIL bullets, and `tests/audit/test_invariant_preservation_NFR_6_through_10.py` imports them [V]. Each changes in the same step as the lines it pins.

### 10.5 Loop and cap text

Those cap-family files that need an edit because they say who counts, merges or escalates:

| Group | Files and lines | Edit |
|---|---|---|
| Task skill | `skills/task/SKILL.md`: 252 (merge) [V], 254 (fix agent) [V], 258 (halt at the cap) [V], 361 (Follow-Up Items) [V], 372 [E] | L1, L2, L3, ledger |
| QA agents | `agents/rf-qa.md` 398, 402 to 415, 549 [E]; `agents/rf-qa-qualitative.md` 110, 809, 994 [E]; `agents/rf-task-builder.md` 383 to 389, 415 to 421 [E] | the cap counts Blocking only; fix-step checks (L2) |
| Builders and researchers | `skills/task-builder/SKILL.md` 875 [E]; `skills/tech-research/SKILL.md` 488 to 490, 517 to 519, 555, 562 [E]; `skills/roadmap`, `readme`, `tech-reference`, `operational-guide` cap lines [E] | point at the shared rule; the consumer line (L4) in the task builder |
| Tasklist | `skills/sc-tasklist-protocol/SKILL.md` 1439, 1450, 1531, 1567, 1571, 1610, 1614 [V] | only if OD7 says so |
| Reflect | `skills/sc-reflect-protocol/SKILL.md` 1540 [V] | only if OD6 says so |
| Worker contract | `core/WORKER-CONTRACT.md` 33 (key list), WC-4 status mapping, 39 (coordinator duties) [V] | the three keys of REQ-12 (stage 2) |
| Routing doc | `core/HOW-WE-WORK.md` 65 [E] | the level text names the cap; check wording |

### 10.6 New files and mirrors

| Item | Note |
|---|---|
| `skills/sc-review-severity/` (6 files) | the shared rule package (section 9.1) |
| classifier code: question module, thresholds config, truth table, judge interface | reached only through a `superclaude review` subcommand whose name does not clash with existing `review` commands (REQ-24); module layout is a plan decision |
| follow-up ledger reader and writer | one reader and one writer for `follow-ups.md` only (REQ-10); the `reuse-auditor` agent runs first, and a mapping to `review-ledger/1` is a plan decision (section 6.2) |
| the `finding-grader` agent in `agents/` | today installed only [V]; needed only if the LLM judge builds on it (OD10) |
| a post-fix mechanical-check helper (L2) | the checks used in run 2 were ad hoc [E]; the helper is new |
| the final-gate sweep (GR7) | new code; stage 2 |
| the install check | a `make doctor` check backed by a pytest test (REQ-27) |
| `plugins/superclaude/` twins of `spec-panel.md` and the review-loop prompts, and from stage 4 the skill-folder mirror | hand-maintained; the plugin tree holds none of the other 11 carriers [V] |
| project `.claude/` copies | made by `make sync-dev` for skills, agents, commands, hooks and templates, never staged; `core/`, `rules/` and `output-styles/` are not synced [V: LC-15] |
`````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:905-934

`````markdown
| `tests/audit/test_nfr_conv_9_zero_trust.py` | byte-exact PASS and FAIL bullets in `rf-qa.md` and its `.claude/` mirror | those bullets are reworded | reword the FAIL bullet to "any blocking gap" with L6 at stage 3 and re-pin both surfaces |
| `tests/audit/test_invariant_preservation_NFR_6_through_10.py` | imports `FAIL_BULLET` and `PASS_BULLET` from the module above (lines 95 to 101) [V] | the imported bullets change | changes in the same step as its source module |
| `tests/audit/test_severity_floor_unweakened.py` | a SHA-256 of rf-qa-qualitative's `## Critical Rules` block in source and mirror; Rule 6 verbatim ("... that's never minor") [V, this merge] | any line in that block changes | re-pin only with OD16: under option (b), Rule 6 and the hash are re-pinned in the same change at stage 3 |
| `tests/audit/test_dnsp_all_agents_fail_bypass.py` | a hash of the `rf-team-lead` fix-cycle line | that line changes | no change unless the cap text moves |
| `tests/review/test_review_rules_text.py` | structure of the review-loop prompts file and `"src/superclaude" not in TEXT` (line 92) [V] | structural moves | keep; the ledger sentence goes inside an existing section |
| Fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` | the old and new strings of past rule edits [V: files exist] | an old or new row no longer holds | update only approved changed strings; do not bypass historical protections wholesale |

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
`````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:936-952

`````markdown
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
`````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:979-994

`````markdown
### 13.2 Revert triggers

A revert means: restore the previous digest for the stage in force through the three-step revert of section 9.4 (repository edit and drift tests, a release naming the refresh command, a refresh on each machine) and go back to the stage before. There is no faster brake in version 1 (section 9.4, OD17). Each trigger is stated with what it can actually detect.

| # | Trigger | Detects | Note on power |
|---|---|---|---|
| RT1 | Any safety-class escape in the audit or the seeded set, or any confirmed safety finding that ended as a plain follow-up | a Safety finding graded Medium or Note | a single event; needs no sample size; acts through the three-step revert |
| RT2 | In an audit window, the 95 percent Wilson lower bound on the escape rate of the simple random sample exceeds 2 percent | a rate that is confidently above 2 percent | at n = 60 this is 4 or more escapes (3 of 60 gives a lower bound of about 1.7 percent; 4 of 60 about 2.6 percent) [computed]. Oversampled strata never feed this trigger. Two escapes in a window is a yellow flag: the owner reviews each one |
| RT3 | Seeded recall of decision-bearing or missing items falls more than 5 points below the old rule, or safety recall falls below it | a rule that is simply too loose | the planted set must be large enough to see 5 points; size it in the plan |
| RT4 | The owner reports a decision-bearing defect that shipped from the ledger | escape type (c) | counts as an escape in M4 |
| RT5 | After 5 runs under stage 3, M1 is not at least 25 percent lower than stage 2 | no benefit | a stop-and-investigate trigger, not an automatic revert, and not tied to the 35 percent target |
| RT6 | M9 is not lower than baseline | L2 is not working | fix L2; the rule can stay |
| RT7 | M6 exceeds 40 percent of non-blocking rows | the decision basis is not being supplied | redesign L4 and the consumer line; the 40 percent is a placeholder to set from stage 2 |
| RT8 | The offer is ignored in 3 consecutive runs | ledger rot | redesign the offer; not a rule revert |

RT2's wording matters. A rule such as "revert if the escape rate exceeds 2 percent" cannot be tested at n = 60, because 0 escapes in 60 only supports "under 5 percent". Triggers are therefore stated as interval bounds, and windows pool runs until the sample supports the claim.
`````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:1-41

`````markdown
# Stage requests for the blocker-classification work (issue #552): one plan per stage

Decision (owner, 2026-11-16): one managed plan package per stage, each generated with `/sc:workflow` and run with `/sc:implement`. `/sc:implement` cannot pause for an owner go, ignores `Depends on:` lines between packages and fails on a plan changed after its first task, so each owner gate sits between two packages and is a chat message from the owner, not a task.

This replaces the single 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (its pre-execution review, `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md`, found 8 blocking defects). That plan stays on disk as the base text for the task bodies; each stage request below names the base tasks it reuses and the changes the review required.

## How to use

1. Generate a stage's package only after the owner's go for it: `/sc:workflow @<request file> --depth standard --handoff none`.
2. Read the plan and its reflect report; run `/sc:implement <printed plan path>` only when execution is wanted.
3. When the package is done, the owner reads its owner summary file and says go for the next stage in chat. Record the go and the package id in the table below (the owner or the session that receives the go writes the row).

## Stage ledger

| Stage | Request file | Base tasks (revised plan) | Package id | Owner go (date, where) |
|---|---|---|---|---|
| 0 Measurement | `stage0-request.md` | 1 to 10 | `TASK-WF-blockerStage0-20261116-021044` (generated 2026-11-16; its review said NEEDS-REVISION, 2 blocking findings; revised in place 2026-11-16, not re-reviewed) | not needed (no change under `src/`) |
| 1 Offline scaffold | `stage1-request.md` | 11 to 25 | `TASK-WF-blockerStage1-20261116-030154` (revision 2 applied 2026-11-16; re-review pending) | |
| 2 Shadow | `stage2-request.md` | 26 to 30 | `TASK-WF-blockerStage2-20261116-030156` (revision 2 applied 2026-11-16; first review never finished; re-review pending) | |
| 3 Pilot | `stage3-request.md` | 31 to 40 | `TASK-WF-blockerStage3-20261116-030158` (revision 2 applied 2026-11-16; re-review pending) | |
| 4 Propagation | `stage4-request.md` | 41 to 46 | `TASK-WF-blockerStage4-20261116-030206` (revision 2 applied 2026-11-16; re-review pending) | |

## Decisions applied to every stage (from the review findings F1 to F15)

- **Gates (F1, F8).** No gate task. The owner's go is a chat message recorded in the ledger above. Each package ends with an owner summary file under its `./artifacts/` that holds the numbers the owner needs for the next go.
- **Cross-package evidence.** A later package reads an earlier package's evidence by package id, found by that folder name under `.dev/tasks/to-do/` or `.dev/tasks/done/` (the package moves when archived). A task never embeds either prefix in an operational link.
- **Merge-rule allow-list staging (F3, F9, F13).** The allow-list in `refs/scale-map.md` lists files by path only and never writes the three merge-rule phrases (`highest severity`, `more severe rating`, `higher severity`) or the old definition sentence. Stage 3's scan test allow-lists only files that exist then. Revision 2 (2026-11-16): there is no plugin mirror folder and no plugin parity test (IronClaude is not installed as a plugin); stage 4 narrows the allow-list and runs the scan strict for `src/` only. The retired `/sc:task` and task-builder files are listed `exempt-by-retirement` and are not edited.
- **Analysis template (F4).** `agent_template_analysis.md` gets the merge-rule text only. It is not a digest carrier: the registry keeps exactly 11 `digest` rows, and the template count in stage 4 is four digest templates plus the analysis template's merge-rule edit.
- **T3 scope (F5, F12).** The `src/superclaude` path check of T3 applies to `digest` and `canonical` rows only. `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present. The existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` (and its plugin twin and the installed variants) is left as it is; it is a read-path note outside this work.
- **Installed files (F15).** No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path; the M, C and E input rule is stated in words.
- **Seeded recall (F2, F10, F11).** Stage 0 defines and sizes the set (with a stated minimum n per gating class, or the set's pass line is called advisory and the interval shown). Stage 3 runs it with fresh agent spawns per pass and alternated order, and Task 33's acceptance line requires the result file to show pass on all three requirements.
- **Classifier evaluation (F7).** Stage 2 evaluates the classifier on the fresh-findings set, the held-out half and the reviewer-called-minor set (all from the stage 0 package) and writes the result for the owner.
- **Superseded acceptance lines (F6).** Resolved by the split: a package's final review covers only its own tasks. Inside a package, a line that a later task of the same package makes false is written with its end point ("until Task N").
- **Unchanged from the revision request.** Three owner gates stay (stage 0 results read before stage 1; stage 1 exit before stage 2; owner go for stages 3 and 4), plus the existing not-built list, the no-authority classifier rule (OD4) and the owner-decision defaults of the first plan.

## Revision 2 decisions (2026-11-16, see `revision2-brief.md` and `../OPEN-QUESTIONS.md`)

- `/sc:task` and task-builder are being retired: no stage edits them; the scan allow-list lists them `exempt-by-retirement`.
- The follow-up carrier is `/sc:implement`'s final review step (owner approved 2026-11-16): record and print only, `refs/qa.md` unedited; the once-per-run offer question stays with the top-level session through the output style.
- No plugin mirror, parity test or plugin registry row; existing plugin twins are edited only where an existing test pins them.
- `follow-ups.md` stays a separate file; no mapping to `review-ledger/1` in these plans.
`````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/revision2-brief.md:1-38

`````markdown
# Revision 2 brief for the stage 1 to 4 plan packages (2026-11-16)

Shared instructions for the four agents that revise the stage 1, 2, 3 and 4 plan packages in place. Read this file first, then `OPEN-QUESTIONS.md` (sections 2 and 3) in the same program folder.

## Why

The pre-execution reviews of stages 1, 3 and 4 said NEEDS-REVISION (stage 2's review did not finish). The owner then answered open questions on 2026-11-16 (recorded in `OPEN-QUESTIONS.md` section 2): `/sc:task` and task-builder are being retired; IronClaude is not installed as a plugin; static QA checks for active workflows stay; the follow-up carrier is `/sc:implement`'s final review step (approved).

No package has been run with `/sc:implement`, so each plan can be edited in place now. The plan file name, slug and frontmatter stay the same.

## Shared design decisions (apply in every stage; do not reopen them)

1. **Retired carriers are not edited.** No task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for those. They keep today's text until the owner's retirement removes them. The stage 1 "Merge-rule allow-list" section in `refs/scale-map.md` lists them as `exempt-by-retirement` (by path only, no merge-rule phrase and no old definition sentence written in it), with the sentence that the exemption ends when the retirement removes the file. Tests that exist only to pin those files are not re-pinned by these plans; the retirement owns them. When a test pins both a retired and an active carrier, the plan re-pins the active carrier's part only.
2. **The follow-up carrier is `/sc:implement`'s final review step, record and print only.** Verified facts the plan must respect: `src/superclaude/skills/sc-implement-protocol/refs/qa.md` keeps its own scale and is NOT edited (it is on the not-built list); `qa.md` line 225 says the final summary "is informational and never asks the user anything"; `qa.md` lines 276 to 288 close the list of interrupts ("No other path may stop automation or prompt the user"). So the edit goes into `src/superclaude/skills/sc-implement-protocol/SKILL.md` (final summary instructions) and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (archive gate, run before the package moves in step 6): one read-only call of the sweep command over the follow-up ledgers the package's review loops wrote, and a printed list in the final summary with the plain-English line naming how the owner can file them. It asks nothing and prompts nothing. The once-per-run offer question stays with the top-level session through the output style (the `pragmatic.md` Medium rule, changed from per loop to per run in stage 3) and with the consent-bound filing path (OD15); stage 2 adds no question to `/sc:implement`. Say this in the plan in one sentence so a reviewer sees the choice.
3. **tech-research** (`src/superclaude/skills/tech-research/SKILL.md`) is an active workflow and keeps its ledger-writing edit as already planned (no sweep, no offer there).
4. **Plugin surface.** IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin. Do not create any new plugin surface: no `plugins/superclaude/skills/sc-review-severity/` mirror, no plugin parity test (T15), no `canonical` registry row for a plugin path. Existing hand-kept plugin twins (`plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`) are touched only where an existing test pins them and the active source carrier changes; say so in the plan. The registry keeps exactly 11 `digest` rows, 1 canonical, 2 pointer-only and 5 installed-only unless the review findings below require a different count; if you change a count, change it everywhere and say why. OPEN-QUESTIONS.md section 3.4 records that this reassessment is the plan author's and the owner has not confirmed removing plugin parity.
5. **Ledger decision (owner question 5).** Version 1 keeps `follow-ups.md` as a separate file; no mapping to `review-ledger/1` rows is built in these plans. The stage 1 reuse-audit result decides whether a mapping is ever added. No plan task replaces or edits `src/superclaude/cli/review/ledger.py`.
6. **Do not use `/sc:implement`, commit or push.** Stage with `git add .dev/tasks` only. Never stage under `.claude/`.

## Rules for the plan files (from `~/.claude/skills/sc-workflow-protocol/refs/quality-gates.md`)

- Keep frontmatter keys as they are. Phases: 4 to 8. Task numbers contiguous from 1. `Depends on: Task K` only to a lower K. Every task has `Acceptance criteria:` with at least one bullet. No checkbox lines and no numbered lines (`1.`, `1)`) anywhere. No absolute paths and no `.dev/tasks/to-do/` prefix in operational links (name a package by id and say "found in the to-do or done subfolder of the repository task folder").
- No document written by a task may say `.dev/tasks/` is never staged.
- An acceptance line that a later task of the same package makes false carries its end point ("until Task N").
- Acceptance checks are pinned by content (quote the sentence protected); never by a line number alone.
- Python is `uv run python ...` only.

## What to do (each agent, for its stage)

1. Read the plan, its `source.md`, its stage request in `stage-requests/`, its `artifacts/codegraph-grounding.md`, and the review output named below. Verify each finding against the live files before you change the plan (a finding the live files do not support is recorded as not applied, with the reason).
2. Edit the plan in place with the Edit tool: fix every BLOCKING finding; fix the non-blocking findings that are cheap and clear; apply the shared design decisions above; renumber tasks and fix every `Task N` reference if you add, remove or merge tasks. Keep the phase count within 4 to 8.
3. Append a `## Revision 2 (2026-11-16)` section to the stage request file in `stage-requests/` listing what changed and why (finding id or decision), then copy it byte for byte to the package's `source.md` (`cp`). The plan's `source:` stays `./source.md`.
4. Append a `## Revision 2` section to the package's `artifacts/codegraph-grounding.md`: what you re-checked (file existence with `test -e`, symbols, dependents, with the commands), and a line for each finding applied or not applied.
5. Run the gate check from the task folder: `cd .dev/tasks/to-do && uv run python /tmp/gate_check.py` (it checks all four stage packages; yours must print PASS; the "never stage" wording check must not fire on your plan). Fix and re-run until your package passes.
6. Run `git add .dev/tasks` from the repository root. Do not commit.
7. Final message to the main session (plain text, under 2000 characters, no file bodies): the plan path, the task count before and after, one line per finding id with applied, partly applied or not applied and why, every cross-stage fact another stage's plan must match (file names, command names, artifact names, task counts), and anything you could not do. If a Write or Edit is refused, say which file and return the exact text you intended.

Work only on your stage's files plus the shared files named in step 3. Do not edit another stage's plan; report cross-stage needs in your final message.
`````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/OPEN-QUESTIONS.md:1-40

`````markdown
# Open questions and decisions: blocker classification (#552) and Review Panel unification

Single index of where decisions live, what the owner has answered, and what is still open. Documentation only: nothing here authorizes code changes, tests, issue filing, merges or implementation. Last updated 2026-11-16.

## 1. Where the sources are

| Topic | Source of truth |
|---|---|
| Blocker programme owner decisions OD1 to OD17 (options and recommendations) | `02-brainstorm/merged-requirements.md` section 15 (line 1023) in this folder; repeated in `09-plan-input.md` line 30 |
| Owner go for each stage | `stage-requests/README.md` (stage ledger) |
| Review Panel open items | `.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/MERGED-review-panel-unification.md` section 9.12 (line 9350); reviewed blob `5620c5d4be813fc3967d667fc76e0539ced86a9b` |
| Plan review findings per stage | `.dev/reflect/pre-TASK-WF-blockerStage<N>-*/` (`REPORT.md` where written, else `adversarial/merged-review-card.md`) |

Owner answers of 2026-11-16 are recorded in section 2 below as the owner gave them. Section 15 of the spec still shows the earlier recommendations and has not been edited.

## 2. Owner answers (2026-11-16)

### 2.1 Jev and blocker classification (#552)
- Investigate Jev for blocker classification. Data access and sharing stays a separate decision (OD3). No credentials, external transmission, paid evaluation or implementation are implied.
- The five-run experiment used Claude as a stand-in, not Jev. It does not prove Jev quality or ledger performance.
- Real blocking findings keep their established refactor and review process. The model-usage warning-only rule does not make all blocker handling informational.

### 2.2 Current workflow and legacy commands
- The active workflow is `/sc:workflow` and `/sc:implement`.
- `sprint run` in its current form is obsolete and is not tested as the current workflow.
- `/sc:task` and task-builder commands are to be retired, without evaluating them. This is a decision, not a claim that removal has happened.
- Only Sprint run and its CLI suite are evaluated, for measurable benefit versus retirement. Any return must be refactored around workflow and implement and properly evaluated. No outcome is assumed.
- Obsolete-command testing is not revived as if it represented the current workflow.

### 2.3 Review Panel unification
- **PR sequence:** merge one PR before opening the next. Sequencing guidance only.
- **Distinct models:** if the panel cannot fill every seat with a different model it may continue and may pass, while clearly disclosing reduced diversity. Duplicate models are never presented as independent. Other verdict criteria and real blocking findings are not waived.
- **Post-gate issues:** the identified issues should be fixed (desired outcome only).
- **Finding claim length:** 2,000 characters maximum. Supersedes the 300-character truncation and the intermediate open cap. Unlimited is not approved. No code claimed. Over-cap behaviour beyond the no-arbitrary-truncation concern is not decided and must not be invented.
- **Missing roster:** a review may complete with a warning when at least two valid reviewer reports exist and there are no obvious signs of failure.
- **Per-seat configuration:** deferred; no design inferred.
- **Exit outcomes:** must be distinguishable. Numeric assignments are not decided.
- **Review-ledger format version:** keep the existing one; backwards compatibility is not a concern. This does not settle whether `follow-ups/1` replaces or augments `review-ledger/1` (see 3.1).
- **Finding-grouping engines:** fix only the newer one for now.
- **Restricted reviewer launcher:** reuse the existing one, subject to verifying it meets the needs. If a second launcher is needed, extract the security policies into a shared module. Design decision only; suitability not verified.
`````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:221-241

`````markdown
## Phase 5: Write the audit summary for the owner

## Task 13: Write the stage 3 audit summary for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12

Write `./artifacts/stage3-summary-for-owner.md`. First re-run the commands of Tasks 4, 10, 11 and 12 and record each pytest summary line. Then write these parts.

- The seeded-recall headline of Task 3 (the outcome of R1, R1b, R2a, R2b and R3, and any owner ruling used), the entry check of Task 1 and the baselines of Task 2 with the RT5 threshold.
- The audit-window measures: read the metric list in spec section 13.1 and quote the rows for M1, M4, M5, M6, M9, M10b, M11 and M12 (M12 is the rf-qa FAIL count per pilot gate), each with its baseline from Task 2 or the statement that none exists; quote RT1 to RT8 from spec section 13.2 and do not restate them from memory.
- The revert triggers that can be judged now. RT1 (seeded part) and RT3 are judged from the Task 3 result: state tripped or not tripped for each, noting that R1b is stricter than R1 (it passes only when every planted safety defect is found-and-blocking under the new text). Mark as pending until the audit window has run only the window-dependent parts: RT1's audit part, RT2, RT4, RT5, RT6, RT7 and RT8.
- The switch steps before the audit window (spec REQ-26). The repository edit and the drift tests are done by this package. Still to do by the owner or operator: ship a release whose note names the refresh command (`superclaude update`, or an install with `--force`), then refresh each machine that will run the audit window and confirm it with the install check (`make doctor`, the `_check_review_severity_digests` check, which reads the packaged registry). The installed style carries the digest once `grep -c "review-severity:digest v2 begin" ~/.claude/output-styles/pragmatic.md` prints 1. Run both commands now, read-only, record what they print on this machine, and say plainly that the audit window is not started on a machine until both show the refreshed state. Until then QA runs under the new carriers plus the old injected style (RK15, counted by M10b).
- The revert path. The per-row three-step revert (spec REQ-26) covers the three digest rows (`output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`): restore the file from the commit before this package's change, set the row to `legacy`, re-run the drift tests, release and refresh. The edits with no registry row are reverted by restoring each listed file from the same commit: the merge text and L2 and L3 text in the two QA agents, `rf-analyst.md`, the once-per-run Medium wording in `pragmatic.md`, the `--promote` flag on the sweep call in `sc-implement-protocol/SKILL.md` and `refs/managed-workspace.md` with their plugin twins and `tests/skills/test_implement_follow_up_sweep.py`, and the re-pinned tests, followed by `make sync-dev` and the same release and refresh. List those files by path.
- State that the audit window runs after this package and is observed by the owner or operator, and name what it covers: every run on a refreshed machine that passes an rf-qa or rf-qa-qualitative gate, from the first run after the refresh until the rate sample of spec section 8.2 reaches 5 runs or 60 non-blocking rows, whichever is later.
- End with the sentence that the owner's go for stage 4 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/stage3-summary-for-owner.md` names the seeded-recall headline and the file that holds it, lists the tests re-pinned with their observed pytest summary lines, and quotes M12, M10b, M1 and RT1 to RT3 from the spec with the baselines of `./artifacts/stage3-baselines.md`.
- The summary states whether RT1 (seeded part) and RT3 are tripped, from the Task 3 result, and lists only the window-dependent triggers as pending; it does not say that no trigger can be judged.
- The summary names the release, the refresh command and the install check as steps that come before the audit window, records the observed output of the install check and of the `grep -c` on the installed style, and states the revert path for the digest rows and for the edits without a registry row.
- The summary ends with the sentence that the owner's go for stage 4 is given in chat and not by this file.
`````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:58-75

`````markdown
## Task 3: Write the scale map

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3, in a single Markdown table whose columns are `family`, `defining file`, `labels`, `model` and `file kind`, because Tasks 9 and 12 read the table in code and the T4 test of Task 15 parses it. `labels` holds each native label with its shared outcome as `LABEL=Outcome` pairs separated by semicolons (outcomes: Blocking, Medium, Note), or the word `none` for a family with no native label. `model` is either "graded by the three conditions" or "keeps its own model because <reason>". `file kind` is `repo` or `installed-only`. For a `repo` row the `defining file` cell holds the path relative to the `src/superclaude/` folder, written without that prefix (for example `agents/rf-qa.md`), so the installed file never names a `src/superclaude/` path; for an `installed-only` row it holds the `~/.claude/...` path of a file that exists only in an installed copy. The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale (defining file `agents/rf-qa.md`, not the retired task skill); the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family (`labels` is `none`; its defining files are `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py`).

The stoprule and `finding-grader` row has no defining file in the repository: the spec files both as installed-only (they exist under `~/.claude/` and not under `src/superclaude/`, and whether they ever move into `src/` is owner decision OD10, not decided here). That row is therefore marked `installed-only`, names `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`, and is exempt from the exists-in-repository line below and from T4 (Task 15 repeats the exemption). It cites no `.dev/` path.

Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" with one bullet per file: the path relative to `src/superclaude/` in backticks, then `allowed` or `exempt-by-retirement`. It lists by path only the files allowed to contain the three merge-rule phrases of spec section 10.3, and never writes those phrases or the old definition sentence, so the stage 3 scan test reads its allow-list from one place. The `allowed` entries are the auggie file (`skills/sc-auggie-review-protocol/SKILL.md`), `skills/sc-review-severity/refs/rule.md`, the six stage 4 files (`skills/tech-reference/SKILL.md`, `skills/readme/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/operational-guide/SKILL.md`, `templates/documents/agent_template_qa.md`, `templates/documents/agent_template_analysis.md`) and the two code files that hold the phrases and are not changed because they assign severity in code (`cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py`, out of scope by spec section 10.3). The `exempt-by-retirement` entries are the retired carriers `skills/task/SKILL.md`, `skills/task-builder/` (every file in the folder) and `agents/rf-task-builder.md`, with the sentence that the exemption ends when the retirement removes the file. No plugin path is listed: no plugin mirror of this skill folder is made by any package.

Acceptance criteria:
- `refs/scale-map.md` has a row for each of the 12 families with the five columns above, and each `repo` row names a defining file that exists in the repository under `src/superclaude/`.
- The stoprule and `finding-grader` row is marked `installed-only`, names the two `~/.claude/` paths, and is exempt from the exists-in-repository line above and from T4; the code-assigned row has `labels` equal to `none`.
- The tasklist row states that Medium is blocking today on 7 lines of `skills/sc-tasklist-protocol/SKILL.md` and that no stage 1 to 4 task changes it.
- The `card_convert.py` row states that its word translator maps `important` and `medium` to non-blocking while `agents/rf-qa.md` treats IMPORTANT as blocking.
- The "Merge-rule allow-list" section exists and lists the auggie file, `refs/rule.md`, the six stage 4 files, `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed`, and `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` with the sentence that the exemption ends when the retirement removes the file; the plugin mirror is not listed.
- `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing.
- `grep -n -i "highest severity\|more severe rating\|higher severity" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing.
`````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:102-111

`````markdown
## Task 6: Write the carrier registry with every digest row set to legacy

Depends on: Task 2, Task 3

Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. Each row has the logical path relative to the install root, a `kind` (`digest`, `canonical`, `pointer-only` or `installed-only`), surfaces (source, installed, project `.claude/`, or `installed-only`; the word `plugin` appears only on the two `pointer-only` rows whose hand-kept plugin twins already exist), rollout stage, a state (`legacy` for a digest row until its file is moved), and an own-scale flag. Rows of kind `digest`, exactly the 11 definition carriers of spec section 10.1: `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`. One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; its surfaces are source, installed and project `.claude/`, with no plugin mirror because IronClaude is not installed as a plugin). Two rows of kind `pointer-only` (a pointer plus the ledger sentence, no digest): `rules/prompts/document_review_loop_prompts.md` and `commands/sc/spec-panel.md` (source `commands/spec-panel.md`). Five rows of kind `installed-only`: `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. `skills/task/SKILL.md` gets no row: it is a retired carrier, not edited by any package and listed only as `exempt-by-retirement` in the allow-list of Task 3, and it is not a digest carrier. `templates/documents/agent_template_analysis.md` gets no row either: it holds no definition sentence, only a merge-rule line, which the stage 4 package edits as text only.

Acceptance criteria:
- `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
- It has exactly 11 rows of kind `digest` (each with a source path that exists, state `legacy`, stage 3 for `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md`, stage 4 for the rest), 1 of kind `canonical`, 2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all.
- No row names `skills/task/SKILL.md`, `skills/task-builder/` or `agents/rf-task-builder.md`, and the `canonical` row lists no plugin surface.
`````

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:486-552

`````markdown
## Task 41: Move the templates to digest v2

Depends on: Task 40

Edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (the definition bullet near line 161, the merge rule near line 85, the Rule 6 text near line 333 per OD16, and the FAIL-by-label bullet "Any CRITICAL or IMPORTANT issue exists" near line 158, rewritten or kept as a named mechanical gate recorded in `refs/scale-map.md`), `documents/agent_template_analysis.md` (the merge rule near line 466), `documents/skill_template.md` (the definition near line 828), `workflow/01_mdtm_template_generic_task.md` (near line 644) and `workflow/02_mdtm_template_complex_task.md` (near line 655). Each gets the digest and pointer in place of the definition bullets and the L1 merge text; update their registry rows to `v2`; remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of Task 40. Task files already generated from the old templates keep the old text and are not migrated.

Acceptance criteria:
- Each of the five template files holds exactly one digest and no `more severe rating` text.
- Their registry rows say `v2` and T1 passes for them.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude/templates` prints nothing, and `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/templates/documents/agent_template_qa.md` prints 0 or the remaining line is listed in `refs/scale-map.md`.
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the two templates removed from its allow-list.

## Task 42: Move the rule prompts to digest v2 and set the two pointer-only rows

Depends on: Task 41

Edit the digest carriers in `src/superclaude/rules/prompts/`: `automated_qa_workflow_qa_prompt.md` (near line 11), `doc_code_analyst_qa_prompt.md` (near line 27), `documentation_expert_qa_prompt.md` (near line 28) and `recruiting_expert_qa_prompt.md` (near line 27); update those four registry rows to `v2`. Edit `document_review_loop_prompts.md` (the Medium wording near lines 31, 32 and 48 becomes the pointer and the ledger sentence inside an existing section; its structure and the `"src/superclaude" not in TEXT` assertion of `tests/review/test_review_rules_text.py` must still hold): its registry row is of kind `pointer-only` and stays so; it is checked by T3 and never by T1.

Acceptance criteria:
- Each of the four rule prompts holds exactly one digest and its registry row says `v2`.
- `document_review_loop_prompts.md` holds the pointer and the ledger sentence and no digest, and its registry row stays `pointer-only`.
- `uv run pytest tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_registry.py -v` passes and the zero-finding and "no minimum count" sentences still exist.

## Task 43: Replace the merge rule in the builder and researcher skills

Depends on: Task 40

Edit the stage 4 merge-rule lines of spec section 10.3: `src/superclaude/skills/tech-reference/SKILL.md` (two lines near 510 and 513), `src/superclaude/skills/readme/SKILL.md` (two lines near 542 and 547), `src/superclaude/skills/tdd/refs/build-request-template.md` (near line 122) and `src/superclaude/skills/operational-guide/SKILL.md` (near line 511), each to the L1 text; and remove those four files from the allow-list of Task 40 in the same change.

Acceptance criteria:
- `grep -rniE "highest severity|more severe rating|higher severity" src/superclaude/skills/tech-reference src/superclaude/skills/readme src/superclaude/skills/tdd src/superclaude/skills/operational-guide` prints nothing.
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the four skills removed from its allow-list.
- The cap text in each of the four files is unchanged (each file still contains its "After 2 fix cycles" sentence).

## Task 44: Add the consumer line to the task builder and MDTM templates

Depends on: Task 41

Edit `src/superclaude/skills/task-builder/SKILL.md` and the MDTM templates `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` so the task builder writes a consumer line for each phase output ("feeds item X, reads column Y"), which gives upstream gates a declared consumer list (L4, spec section 4.3 option A for upstream outputs only). Keep the cap sentence in `src/superclaude/skills/task-builder/SKILL.md` ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", one occurrence today) unchanged; `src/superclaude/agents/rf-task-builder.md` holds no such sentence and is not edited.

Acceptance criteria:
- Both MDTM templates and the task-builder skill contain the consumer-line instruction.
- `uv run pytest tests/skills/test_task_builder_merge.py -v` passes.
- The cap sentence is still present in `src/superclaude/skills/task-builder/SKILL.md` (`grep -c` prints 1), and `git diff --stat` shows no edit to `src/superclaude/agents/rf-task-builder.md`.

## Task 45: Narrow spec-panel and update the plugin twins

Depends on: Task 42

Edit `src/superclaude/commands/spec-panel.md`: the Review Loop bullets (the Grading and Cap bullets near lines 259 to 261) and the always-CRITICAL dimensional-mismatch sentence ("Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity", near line 372) are narrowed to the three conditions (CRITICAL stays blocking, a MAJOR stays blocking only when it names a concrete wrong outcome), its `follow-up candidates` list becomes the follow-up ledger, and the Unattended mode section gains one line for the ledger and the three contract keys. Apply the same edits to the hand-kept twins `plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`; the `spec-panel` source and plugin copies differ today, so edit each file in place and do not copy one over the other. The `commands/sc/spec-panel.md` registry row stays `pointer-only`.

Acceptance criteria:
- `uv run pytest tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py -v` passes and the cap sentence `at most 2 fix cycles (3 reviews)` is still in `src/superclaude/commands/spec-panel.md`.
- `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` prints nothing and the ledger is named instead.
- The plugin twins carry the same pointer and ledger sentence as their source twins, and a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`.

## Task 46: Mirror the skill folder into the plugin and make the drift scan strict

Depends on: Task 41, Task 42, Task 43, Task 44, Task 45

Copy `src/superclaude/skills/sc-review-severity/` to `plugins/superclaude/skills/sc-review-severity/` by hand (the plugin's `skills/` is hand-kept and holds 4 entries today), add a `canonical` registry row for the plugin mirror of `refs/rule.md`, add `tests/skills/test_review_severity_plugin_parity.py` for T15 (the mirror equals the source), set every `digest` row to `v2` where its file now holds the digest, and switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode so any legacy definition sentence left in `src/` or `plugins/` fails. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passes with strict T2, and the plugin mirror of `refs/rule.md` is accepted by the reverse scan through its `canonical` row.
- `make verify-sync` passes.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` prints nothing; the five installed-only spec-panel variants are outside the scan and stay listed `installed-only`.
- No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`.
`````

### .dev/reflect/pre-TASK-WF-blockerStage4-20261116-030206-20261116174332/artifacts/coverage-matrix.yaml:1-175

`````yaml
parsed_ids: []
parsed_count: 0
inferred_count: 28
rows:
  - id: INF-001
    citation: source.md:3
    quote: "Generate it only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (the spec's section 13.2), the owner has read `./artifacts/stage3-summary-for-owner.md`, and the owner's go in chat is recorded in the stage ledger."
    containment_match: Task 1
    containment_ratio: 0.821
    best_task: Task 1
  - id: INF-002
    citation: source.md:7
    quote: "Reuse Tasks 41 to 46 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 5, stage 4; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 4 parts)."
    containment_match: none
    containment_ratio: 0.346
    best_task: Task 5
  - id: INF-003
    citation: source.md:11
    quote: "The digest goes into four templates: `agent_template_qa.md`, `skill_template.md`, `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md`."
    containment_match: Task 1
    containment_ratio: 0.875
    best_task: Task 1
  - id: INF-004
    citation: source.md:11
    quote: "`agent_template_analysis.md` gets the merge-rule text only (no digest, no registry row, no fence)."
    containment_match: Task 1
    containment_ratio: 1.000
    best_task: Task 1
  - id: INF-005
    citation: source.md:11
    quote: "The registry keeps exactly 11 `digest` rows."
    containment_match: Task 1
    containment_ratio: 1.000
    best_task: Task 1
  - id: INF-006
    citation: source.md:11
    quote: "Acceptance: \"four template files hold exactly one digest\", the analysis template holds none and no `more severe rating` text, and `agent_template_qa.md` holds none of the \"Any CRITICAL or IMPORTANT issue exists\" FAIL bullet unless it is listed as a kept mechanical gate in `refs/scale-map.md`."
    containment_match: Task 1
    containment_ratio: 0.812
    best_task: Task 1
  - id: INF-007
    citation: source.md:11
    quote: "Remove `agent_template_qa.md` and `agent_template_analysis.md` from the scan allow-list in the same change."
    containment_match: Task 1
    containment_ratio: 0.857
    best_task: Task 1
  - id: INF-008
    citation: source.md:12
    quote: "As the base text, with the two `pointer-only` rows left at `pointer-only` and the cap sentences kept by content."
    containment_match: Task 4
    containment_ratio: 0.636
    best_task: Task 4
  - id: INF-009
    citation: source.md:13
    quote: "As the base text; the existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` and its twins stays, since T3 does not check `pointer-only` rows for that path."
    containment_match: Task 4
    containment_ratio: 0.765
    best_task: Task 4
  - id: INF-010
    citation: source.md:14
    quote: "Order the work so the registry and the allow-list are correct BEFORE the copy: first add the plugin mirror of `refs/rule.md` to the `canonical` registry rows and to the allow-list in `refs/scale-map.md` (path only, no merge-rule phrases), then copy the skill folder to `plugins/superclaude/skills/sc-review-severity/`, then run T15 parity, strict T2 and the merge-rule scan."
    containment_match: none
    containment_ratio: 0.500
    best_task: Task 1
  - id: INF-011
    citation: source.md:14
    quote: "Acceptance includes `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passing, `make verify-sync` passing, and no `.claude/` path other than `.claude/settings.json` staged."
    containment_match: Task 5
    containment_ratio: 0.800
    best_task: Task 5
  - id: INF-012
    citation: source.md:15
    quote: "State this is stage 4 and the last package; strict T2 is switched on here. Acceptance lines that a later task of this package makes false get an end point."
    containment_match: none
    containment_ratio: 0.526
    best_task: Task 5
  - id: INF-013
    citation: source.md:16
    quote: "Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final scan and parity results, and the revert command per row (the spec's three-step revert), ending with the sentence that a second audit window is observed by the owner or operator and is not a task of this package."
    containment_match: Task 6
    containment_ratio: 0.966
    best_task: Task 6
  - id: INF-014
    citation: source.md:20
    quote: "No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account."
    containment_match: none
    containment_ratio: 0.417
    best_task: Task 4
  - id: INF-015
    citation: source.md:28
    quote: "The summary check is now: exists and quotes RT1, RT2 and M12. The window result is recorded in the owner's entry in the stage 4 `Owner go (date, where)` cell of the stage ledger, which the first check reads (date plus the statement that one audit window passed with no RT1 or RT2 tripped)."
    containment_match: Task 1
    containment_ratio: 0.886
    best_task: Task 1
  - id: INF-016
    citation: source.md:29
    quote: "A settling grep over the mapping test comes first, and if stage 3 already moved a pin the spec-panel text follows that pin."
    containment_match: Task 4
    containment_ratio: 0.750
    best_task: Task 4
  - id: INF-017
    citation: source.md:30
    quote: "The last code task (Task 5) runs the whole pinning set once after the last edit, including `test_review_severity_rule.py`, `test_review_brief_placement.py`, `test_review_prompt_overrides.py`, `test_worker_contract.py`, `test_implement_severity_static.py` and `test_review_brief_rests_on.py`. The plugin rules-prompt byte copy moved into Task 2 so `test_review_brief_placement.py` is never red between tasks."
    containment_match: Task 5
    containment_ratio: 0.656
    best_task: Task 5
  - id: INF-018
    citation: source.md:32
    quote: "Task 4 quotes the new dimensional-mismatch sentence by content, requires the always-CRITICAL sentence to be gone, and keeps \"CRITICAL is blocking\" (pinned). One new source-only test pins the sentence."
    containment_match: none
    containment_ratio: 0.571
    best_task: Task 4
  - id: INF-019
    citation: source.md:33
    quote: "Tasks 1 and 3 name the \"Merge-rule allow-list\" section of `refs/scale-map.md` and add a grep check, because the scan test only checks that listed files exist."
    containment_match: Task 1
    containment_ratio: 0.789
    best_task: Task 1
  - id: INF-020
    citation: source.md:34
    quote: "The cap checks in Task 3 are case-insensitive and give today's counts (5, 6, 1, 2)."
    containment_match: Task 3
    containment_ratio: 0.769
    best_task: Task 3
  - id: INF-021
    citation: source.md:35
    quote: "The L1 merge text is defined once in the Constraints and pinned by the phrase `keeps every reviewer's own grade visible`; the registry check names its pytest command; the consumer-line acceptance is gone with the task."
    containment_match: Task 1
    containment_ratio: 0.609
    best_task: Task 1
  - id: INF-022
    citation: source.md:36
    quote: "Tasks 1 and 2 pin the digest's closing cap sentence by content in every digest carrier, and Task 2 checks that `follow-up candidates` left `document_review_loop_prompts.md` and `follow-up ledger` replaced it."
    containment_match: Task 2
    containment_ratio: 0.652
    best_task: Task 2
  - id: INF-023
    citation: source.md:38
    quote: "Task 5 runs `git grep -n \"review-severity:digest\" -- src plugins` and the old-sentence grep before the strict switch, records the output in `./artifacts/strict-t2-hits.md`, and rewords or exempts any hit outside a `digest` or `canonical` file."
    containment_match: Task 5
    containment_ratio: 0.769
    best_task: Task 5
  - id: INF-024
    citation: source.md:39
    quote: "(a) The label list near line 333 of `agent_template_qa.md` is checked against the Rule 6 heading that stage 3 gives `rf-qa-qualitative.md`. (b) The scale-map plugin copy no longer exists."
    containment_match: Task 1
    containment_ratio: 0.619
    best_task: Task 1
  - id: INF-025
    citation: source.md:40
    quote: "The old Task 4 (consumer line in `task-builder/SKILL.md` and the two MDTM templates) is dropped, and `rf-task-builder.md` is not edited. The MDTM templates stay only as digest carriers (they hold the old definition sentence and have registry rows)."
    containment_match: Task 1
    containment_ratio: 0.640
    best_task: Task 1
  - id: INF-026
    citation: source.md:41
    quote: "The spec-panel Verdict text moves from once per loop to once per run to match the output style; no question is added to any command."
    containment_match: none
    containment_ratio: 0.500
    best_task: Task 4
  - id: INF-027
    citation: source.md:42
    quote: "No mirror folder, parity test, plugin registry row or plugin reverse scan. Plugin twins are edited only where an existing test pins them: the rules prompt (byte copy) and the spec-panel Grading, Verdict and FR-8 lines."
    containment_match: Task 4
    containment_ratio: 0.615
    best_task: Task 4
  - id: INF-028
    citation: source.md:43
    quote: "No task touches `src/superclaude/cli/review/ledger.py`."
    containment_match: Task 5
    containment_ratio: 0.714
    best_task: Task 5
matched: 22
total: 28
coverage_pct_union: 0.7857
`````


## Coverage slice

| Requirement | Card ID | Status | Grounding |
|-------------|---------|--------|-----------|
| INF-001: Generate it only after the stage 3 package is done, one audit window has passed with no revert trigger tripped | T1 card | covered (containment 0.821 -> Task 1) | source.md:3 |
| INF-002: Reuse Tasks 41 to 46 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 5, stage 4; | T1 card | not matched mechanically (0.346 best Task 5) | source.md:7 |
| INF-003: The digest goes into four templates: `agent_template_qa.md`, `skill_template.md`, `01_mdtm_template_generic_ta | T1 card | covered (containment 0.875 -> Task 1) | source.md:11 |
| INF-004: `agent_template_analysis.md` gets the merge-rule text only (no digest, no registry row, no fence). | T1 card | covered (containment 1.000 -> Task 1) | source.md:11 |
| INF-005: The registry keeps exactly 11 `digest` rows. | T1 card | covered (containment 1.000 -> Task 1) | source.md:11 |
| INF-006: Acceptance: "four template files hold exactly one digest", the analysis template holds none and no `more sever | T1 card | covered (containment 0.812 -> Task 1) | source.md:11 |
| INF-007: Remove `agent_template_qa.md` and `agent_template_analysis.md` from the scan allow-list in the same change. | T1 card | covered (containment 0.857 -> Task 1) | source.md:11 |
| INF-008: As the base text, with the two `pointer-only` rows left at `pointer-only` and the cap sentences kept by conten | T1 card | covered (containment 0.636 -> Task 4) | source.md:12 |
| INF-009: As the base text; the existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` and its twin | T1 card | covered (containment 0.765 -> Task 4) | source.md:13 |
| INF-010: Order the work so the registry and the allow-list are correct BEFORE the copy: first add the plugin mirror of  | T1 card | not matched mechanically (0.500 best Task 1) | source.md:14 |
| INF-011: Acceptance includes `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severi | T1 card | covered (containment 0.800 -> Task 5) | source.md:14 |
| INF-012: State this is stage 4 and the last package; strict T2 is switched on here. Acceptance lines that a later task  | T1 card | not matched mechanically (0.526 best Task 5) | source.md:15 |
| INF-013: Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the f | T1 card | covered (containment 0.966 -> Task 6) | source.md:16 |
| INF-014: No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superc | T1 card | not matched mechanically (0.417 best Task 4) | source.md:20 |
| INF-015: The summary check is now: exists and quotes RT1, RT2 and M12. The window result is recorded in the owner's ent | T1 card | covered (containment 0.886 -> Task 1) | source.md:28 |
| INF-016: A settling grep over the mapping test comes first, and if stage 3 already moved a pin the spec-panel text foll | T1 card | covered (containment 0.750 -> Task 4) | source.md:29 |
| INF-017: The last code task (Task 5) runs the whole pinning set once after the last edit, including `test_review_severi | T1 card | covered (containment 0.656 -> Task 5) | source.md:30 |
| INF-018: Task 4 quotes the new dimensional-mismatch sentence by content, requires the always-CRITICAL sentence to be go | T1 card | not matched mechanically (0.571 best Task 4) | source.md:32 |
| INF-019: Tasks 1 and 3 name the "Merge-rule allow-list" section of `refs/scale-map.md` and add a grep check, because th | T1 card | covered (containment 0.789 -> Task 1) | source.md:33 |
| INF-020: The cap checks in Task 3 are case-insensitive and give today's counts (5, 6, 1, 2). | T1 card | covered (containment 0.769 -> Task 3) | source.md:34 |
| INF-021: The L1 merge text is defined once in the Constraints and pinned by the phrase `keeps every reviewer's own grad | T1 card | covered (containment 0.609 -> Task 1) | source.md:35 |
| INF-022: Tasks 1 and 2 pin the digest's closing cap sentence by content in every digest carrier, and Task 2 checks that | T1 card | covered (containment 0.652 -> Task 2) | source.md:36 |
| INF-023: Task 5 runs `git grep -n "review-severity:digest" -- src plugins` and the old-sentence grep before the strict  | T1 card | covered (containment 0.769 -> Task 5) | source.md:38 |
| INF-024: (a) The label list near line 333 of `agent_template_qa.md` is checked against the Rule 6 heading that stage 3  | T1 card | covered (containment 0.619 -> Task 1) | source.md:39 |
| INF-025: The old Task 4 (consumer line in `task-builder/SKILL.md` and the two MDTM templates) is dropped, and `rf-task- | T1 card | covered (containment 0.640 -> Task 1) | source.md:40 |
| INF-026: The spec-panel Verdict text moves from once per loop to once per run to match the output style; no question is | T1 card | not matched mechanically (0.500 best Task 4) | source.md:41 |
| INF-027: No mirror folder, parity test, plugin registry row or plugin reverse scan. Plugin twins are edited only where  | T1 card | covered (containment 0.615 -> Task 4) | source.md:42 |
| INF-028: No task touches `src/superclaude/cli/review/ledger.py`. | T1 card | covered (containment 0.714 -> Task 5) | source.md:43 |
