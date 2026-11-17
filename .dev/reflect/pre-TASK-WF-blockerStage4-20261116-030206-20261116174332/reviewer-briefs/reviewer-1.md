# Reviewer brief 1 (persona: analyzer; model class: sonnet)

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


Persona instructions (analyzer): you own question (a) for the findings G1 to G8 and the live-test simulation. For each of G1 to G8, say fixed, partly fixed or not fixed in the live plan, with the plan line. Then simulate the tests: take the exact text Task 4 and Task 2 will write (spec-panel Grading, Verdict, FR-8, dimensional-mismatch and Unattended lines; the rules prompt and its plugin byte copy) and walk every assertion of tests/skills/test_review_severity_mapping.py, tests/skills/test_spec_panel_review_loop.py, tests/skills/test_review_loop_extension.py, tests/skills/test_review_brief_placement.py, tests/review/test_review_rules_text.py and tests/skills/test_worker_contract.py that reads those files; name any assertion that would fail or any test the plan does not run. Also check Task 5's final run list against every test file that reads a file the package edits (use Grep over tests/ for each edited path or a distinctive phrase). Then look for new defects in Tasks 1 to 4.


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

### src/superclaude/commands/spec-panel.md:215-222

`````markdown
|---------------|------|---------------|-----------|-----------------|------------------|
| `<var_name>` | `<type>` | `<initial>` | `<constraint that must always hold>` | `<operations that read this variable>` | `<operations that modify this variable>` |

## Tool Coordination

- **Read**: Specification content analysis and parsing; `src/superclaude/examples/release-spec-template.md` — read when generating scoped release spec output from TDD input (Step 6b / `--downstream roadmap` mode)
- **Native reasoning**: Expert panel coordination and iterative analysis
- **Context7**: Specification patterns and industry best practices
`````

### src/superclaude/commands/spec-panel.md:250-264

`````markdown
**Iteration 3**: Polish and optimization

- Documentation quality and clarity
- Example and scenario enhancement
- Final validation and consistency checks

## Review Loop

1. **Mode**: `--re-review` applies to `--mode critique` only; without both `--re-review` and `--baseline` the run is a first review of the full document, with `baseline: missing` noted if only one was given; if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review; the report header also records the SHA-256 of the candidate and, when a baseline was given, of the baseline, and the reviewer model actually used, and an input whose hash cannot be taken stops the run like an unreadable file.
2. **Grading**: grade by consequence, not by label; CRITICAL is blocking; a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk, otherwise it is Medium (a warning listed under `follow-up candidates`); MINOR is a note; Medium and minor findings never trigger a revision, never fail a review and never appear in the Reviser brief.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes and Medium warnings allowed) or `verdict: FAIL` (a blocking finding is open); the report lists Medium and minor findings under `follow-up candidates`, the session that ran the review asks the user once per loop whether to open an issue for them and creates none without the user's answer, and an `--unattended` run only records the list; a coordinator treats a re-review report with no prior-findings table, any report whose final `verdict:` line is missing or ambiguous, and any report that cites a finding id absent from its table as `verdict: FAIL`, never as PASS and never as zero findings.
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the prior report's N plus 1 (1 for a first review); a prior-findings file at `review: 3` (a higher value counts as 3) with `verdict: FAIL` means do not review (this check runs before the first-review default of bullet 1), HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--re-review` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review; after the second fix cycle only the third review runs, and a severity or necessity audit before it only reports and edits nothing.
5. **Re-review output**: first a table of prior blocking findings `resolved|open|regressed` (`regressed` = a finding the prior report marked resolved that fails again; each keeps its id from the prior report, and a finding the reviser deferred or withdrew, or one the reviewer cannot match to a prior id with certainty, counts as open); then findings on lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`; an `origin=unchanged` finding is a minor note unless it quotes the changed line that depends on it; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on changed lines only; an empty diff leaves every prior blocking finding open and still counts as a review; a re-review with no open blocking finding ends `verdict: PASS` with the coverage line `scoped PASS: changed lines + prior blockers`, and whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line, listing only blocking finding ids and restating this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser prefers deleting or narrowing to adding and reports the byte size before and after, with the bytes added and deleted per finding id.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking. A brief also cannot make a minor or Medium finding fail the review or authorize editing one, including through "apply all findings", and the report names any brief clause it overrode.
`````

### src/superclaude/commands/spec-panel.md:326-336

`````markdown
| `<guard_name>` | `<section/requirement>` | Legitimate Edge Case | `<edge value>` | `<true/false>` | `<what spec says happens>` | OK/GAP |

#### Completion Criteria (Hard Gates)

These rules are **hard gates**, not advisory recommendations. They block synthesis output unconditionally.

1. **FR-8: GAP Status Rule**: Any cell in the Status column containing "GAP" generates a finding. It is blocking when it names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk; otherwise it is Medium (a warning listed under `follow-up candidates`).
2. **FR-9: Blank Behavior Rule**: Any blank or "unspecified" entry in the Specified Behavior column generates a finding, graded like FR-8.
3. **FR-10: Synthesis-Blocking Gate**: The Guard Condition Boundary Table MUST be complete (all cells populated, all guards enumerated, and every input class either given a row or left out with its one-line reason) before synthesis output is generated. An incomplete table blocks synthesis output. This is a hard gate, not advisory.

#### Downstream Propagation
`````

### src/superclaude/commands/spec-panel.md:366-376

`````markdown
3. **Downstream Tracing** (Fowler + Whittaker): For each stage where N != M, trace which downstream consumers use the output. Verify that each consumer's specification accounts for the count difference. Flag consumers that assume input count == original count.

4. **Consistency Check** (Whittaker leads): For every identified count mismatch, verify that the specification explicitly handles the divergence. Flag any mismatch where the specification assumes count conservation (e.g., "process all N items" after a filter that may reduce count to M < N).

#### Severity Classification (FR-19)

Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity. The finding MUST include a concrete scenario demonstrating the mismatch with specific count values (e.g., "10 items enter filter, 7 pass, but downstream batch processor assumes 10").

#### Quantity Flow Diagram (FR-21)

When Pipeline Dimensional Analysis triggers, the panel MUST produce a Quantity Flow Diagram as an output artifact. The diagram:
`````

### src/superclaude/commands/spec-panel.md:452-468

`````markdown
- **Dev Workflow Integration**: CI/CD spec validation, VCS spec evolution tracking, IDE inline quality feedback, automated quality-gate enforcement
- **Learning and Mentoring**: progressive skill tracking, spec-writing pattern teaching, best-practice library sharing, educational/mentoring mode

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:spec-panel` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (quoted specification content is a quoted argument); otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/spec-panel-report.md`. `artifacts` lists `<report-dir>/improved-spec.md` when the Improve step ran; paths git ignores are left out (WC-4), and it is `[]` otherwise. The run is succeeded when the report is written, blocked at the gate below, and failed otherwise.
- **Person-mode flags.** None is refused. `--mode socratic` only writes its questions into the report and does not wait for answers.
- **Gates.** Under `--unattended` a TDD input without `--target-release` resolves as blocked, with the `target_release` question in `blocked_question`; PRD inputs are unchanged, because they need no `target_release`. The Improve step (step 6) runs only when `--improve` is passed, and then writes `<report-dir>/improved-spec.md`; the input specification is never modified. There is no other gate.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

`````

### plugins/superclaude/commands/spec-panel.md:213-220

`````markdown
|---------------|------|---------------|-----------|-----------------|------------------|
| `<var_name>` | `<type>` | `<initial>` | `<constraint that must always hold>` | `<operations that read this variable>` | `<operations that modify this variable>` |

## Tool Coordination

- **Read**: Specification content analysis and parsing; `src/superclaude/examples/release-spec-template.md` — read when generating scoped release spec output from TDD input (Step 6b / `--downstream roadmap` mode)
- **Sequential**: Expert panel coordination and iterative analysis
- **Context7**: Specification patterns and industry best practices
`````

### plugins/superclaude/commands/spec-panel.md:248-262

`````markdown
**Iteration 3**: Polish and optimization

- Documentation quality and clarity
- Example and scenario enhancement
- Final validation and consistency checks

## Review Loop

1. **Mode**: `--re-review` applies to `--mode critique` only; without both `--re-review` and `--baseline` the run is a first review of the full document, with `baseline: missing` noted if only one was given; if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review; the report header also records the SHA-256 of the candidate and, when a baseline was given, of the baseline, and the reviewer model actually used, and an input whose hash cannot be taken stops the run like an unreadable file.
2. **Grading**: grade by consequence, not by label; CRITICAL is blocking; a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk, otherwise it is Medium (a warning listed under `follow-up candidates`); MINOR is a note; Medium and minor findings never trigger a revision, never fail a review and never appear in the Reviser brief.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes and Medium warnings allowed) or `verdict: FAIL` (a blocking finding is open); the report lists Medium and minor findings under `follow-up candidates`, the session that ran the review asks the user once per loop whether to open an issue for them and creates none without the user's answer, and an `--unattended` run only records the list; a coordinator treats a re-review report with no prior-findings table, any report whose final `verdict:` line is missing or ambiguous, and any report that cites a finding id absent from its table as `verdict: FAIL`, never as PASS and never as zero findings.
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the prior report's N plus 1 (1 for a first review); a prior-findings file at `review: 3` (a higher value counts as 3) with `verdict: FAIL` means do not review (this check runs before the first-review default of bullet 1), HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--re-review` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review; after the second fix cycle only the third review runs, and a severity or necessity audit before it only reports and edits nothing.
5. **Re-review output**: first a table of prior blocking findings `resolved|open|regressed` (`regressed` = a finding the prior report marked resolved that fails again; each keeps its id from the prior report, and a finding the reviser deferred or withdrew, or one the reviewer cannot match to a prior id with certainty, counts as open); then findings on lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`; an `origin=unchanged` finding is a minor note unless it quotes the changed line that depends on it; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on changed lines only; an empty diff leaves every prior blocking finding open and still counts as a review; a re-review with no open blocking finding ends `verdict: PASS` with the coverage line `scoped PASS: changed lines + prior blockers`, and whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line, listing only blocking finding ids and restating this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser prefers deleting or narrowing to adding and reports the byte size before and after, with the bytes added and deleted per finding id.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking. A brief also cannot make a minor or Medium finding fail the review or authorize editing one, including through "apply all findings", and the report names any brief clause it overrode.
`````

### plugins/superclaude/commands/spec-panel.md:326-334

`````markdown
#### Completion Criteria (Hard Gates)

These rules are **hard gates**, not advisory recommendations. They block synthesis output unconditionally.

1. **FR-8: GAP Status Rule**: Any cell in the Status column containing "GAP" generates a finding. It is blocking when it names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk; otherwise it is Medium (a warning listed under `follow-up candidates`).
2. **FR-9: Blank Behavior Rule**: Any blank or "unspecified" entry in the Specified Behavior column generates a finding, graded like FR-8.
3. **FR-10: Synthesis-Blocking Gate**: The Guard Condition Boundary Table MUST be complete (all cells populated, all guards enumerated, and every input class either given a row or left out with its one-line reason) before synthesis output is generated. An incomplete table blocks synthesis output. This is a hard gate, not advisory.

#### Downstream Propagation
`````

### plugins/superclaude/commands/spec-panel.md:364-376

`````markdown
3. **Downstream Tracing** (Fowler + Whittaker): For each stage where N != M, trace which downstream consumers use the output. Verify that each consumer's specification accounts for the count difference. Flag consumers that assume input count == original count.

4. **Consistency Check** (Whittaker leads): For every identified count mismatch, verify that the specification explicitly handles the divergence. Flag any mismatch where the specification assumes count conservation (e.g., "process all N items" after a filter that may reduce count to M < N).

#### Severity Classification (FR-19)

Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity. The finding MUST include a concrete scenario demonstrating the mismatch with specific count values (e.g., "10 items enter filter, 7 pass, but downstream batch processor assumes 10").

#### Quantity Flow Diagram (FR-21)

When Pipeline Dimensional Analysis triggers, the panel MUST produce a Quantity Flow Diagram as an output artifact. The diagram:

- Shows counts at each pipeline stage (N in -> M out)
`````

### tests/skills/test_review_severity_mapping.py:1-145

`````python
"""Pins for the consequence-based severity mapping and Medium tier (#346, phase P2).

Findings are graded by consequence, not label. On ``/sc:spec-panel``'s scale
CRITICAL is blocking; MAJOR and FR-8/FR-9 are blocking only when they name a
concrete wrong outcome or a security, data-loss or safety-boundary risk,
otherwise they are Medium warnings listed under ``follow-up candidates``; MINOR
is a note. The boundary table asks for one row per applicable input class, not a
six-row quota. The S1-S5 bullets of ``pragmatic.md`` stay byte-identical (ten
files copy them verbatim); the Medium tier is added after S5.

Enforcement type: STATIC - assertions over tracked primitive text.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.skills.test_review_severity_rule import canonical_rule_bullets

_REPO = Path(__file__).resolve().parents[2]
STYLE = _REPO / "src/superclaude/output-styles/pragmatic.md"
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)

spec_panel = pytest.mark.parametrize("rel", SPEC_PANELS)


def _flat(text: str) -> str:
    return " ".join(text.split())


def _text(rel: str) -> str:
    return _flat((_REPO / rel).read_text(encoding="utf-8"))


def _bullet(rel: str, number: int) -> str:
    lines = (_REPO / rel).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Review Loop") + 1
    prefix = f"{number}. **"
    return next(line for line in lines[start:] if line.startswith(prefix))


# --- spec-panel Review Loop ---------------------------------------------------


@spec_panel
def test_grading_bullet_grades_by_consequence(rel):
    grading = _flat(_bullet(rel, 2))
    for literal in (
        "grade by consequence, not by label",
        "CRITICAL is blocking",
        "a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome",
        "security, data-loss or safety-boundary risk",
        "otherwise it is Medium (a warning listed under `follow-up candidates`)",
        "MINOR is a note",
        "never appear in the Reviser brief",
    ):
        assert literal in grading, literal
    assert "CRITICAL and FR-8/FR-9 findings are blocking" not in grading


@spec_panel
def test_verdict_bullet_routes_follow_up_candidates(rel):
    verdict = _flat(_bullet(rel, 3))
    for literal in (
        "minor notes and Medium warnings allowed",
        "`follow-up candidates`",
        "asks the user once per loop",
        "creates none without the user's answer",
        "an `--unattended` run only records the list",
    ):
        assert literal in verdict, literal


@spec_panel
def test_reviser_brief_still_lists_only_blocking_ids(rel):
    assert "listing only blocking finding ids" in _flat(_bullet(rel, 6))


# --- boundary table -------------------------------------------------------------


@spec_panel
def test_boundary_table_is_one_row_per_applicable_class(rel):
    text = _text(rel)
    assert "one row per input class that applies to the guard" in text
    assert "the six classes below are the menu, not a quota" in text
    assert "minimum 6 input condition rows per guard" not in text


@spec_panel
def test_fr8_fr9_grade_by_outcome_not_by_status_cell(rel):
    text = _text(rel)
    assert "**MAJOR** severity minimum" not in text
    fr8 = text[text.index("**FR-8: GAP Status Rule**") :]
    fr8 = fr8[: fr8.index("**FR-10")]
    assert "It is blocking when it names a concrete wrong outcome" in fr8
    assert "otherwise it is Medium" in fr8
    assert "graded like FR-8" in fr8


@spec_panel
def test_fr10_gate_survives_with_applicable_rows(rel):
    text = _text(rel)
    assert "**FR-10: Synthesis-Blocking Gate**" in text
    assert "This is a hard gate, not advisory." in text
    assert "left out with its one-line reason" in text


# --- pragmatic.md ----------------------------------------------------------------


def test_medium_tier_follows_the_untouched_s1_s5_bullets():
    lines = STYLE.read_text(encoding="utf-8").splitlines()
    s5 = canonical_rule_bullets()[4]
    i = lines.index(s5)
    medium, scale = lines[i + 1], lines[i + 2]
    flat = _flat(medium)
    assert flat.startswith(
        "- Among minor findings, one that describes a real but non-blocking weakness"
    )
    assert "is Medium" in flat and "never fails a review" in flat
    assert "never appears in a reviser brief" in flat
    assert "asks the user once per loop whether to open an issue" in flat
    assert "no issue is created without the user's answer" in flat
    assert "only records the list" in flat
    flat = _flat(scale)
    assert flat.startswith("- On `/sc:spec-panel`'s CRITICAL / MAJOR / MINOR scale")
    assert "MAJOR is blocking only when it names a concrete wrong outcome" in flat
    assert (
        "a reviewer never suppresses such a finding because its label says Medium or minor"
        in flat
    )


def test_security_and_data_loss_risk_is_never_downgraded_by_label():
    flat = _flat(STYLE.read_text(encoding="utf-8"))
    assert (
        "a finding of any label whose consequence is a security, data-loss or safety-boundary risk is blocking"
        in flat
    )
`````

### tests/skills/test_spec_panel_review_loop.py:1-174

`````python
"""Static pins for the /sc:spec-panel ``## Review Loop`` section (issue 346).

Enforcement type: STATIC - assertions over the text of the two spec-panel
copies, the two routing-guide copies and the two release guides. They prove the
text is present and in the right order, not that a reviewer obeys it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.skills.test_review_severity_rule import AT_CAP_CLAUSES, CANONICAL_CAP_TEXT

_REPO = Path(__file__).resolve().parents[2]

SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
HOW_WE_WORK = (
    "src/superclaude/core/HOW-WE-WORK.md",
    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
)
RELEASE_GUIDES = (
    "docs/guides/prd-skill-release-guide.md",
    "docs/guides/tdd-skill-release-guide.md",
)
HEADING = "## Review Loop"
BULLET_NAMES = (
    "Mode",
    "Grading",
    "Verdict",
    "Cap",
    "Re-review output",
    "Reviser contract",
    "Precedence",
)
OLD_SENTENCE = "until no critical findings remain"


def _flat(text: str) -> str:
    return " ".join(text.split())


def _lines(rel: str) -> list[str]:
    return (_REPO / rel).read_text(encoding="utf-8").splitlines()


def _section_lines(rel: str) -> list[str]:
    """Raw lines between the Review Loop heading and the next ``## `` heading."""
    lines = _lines(rel)
    start = lines.index(HEADING) + 1
    end = next(
        (i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines)
    )
    return lines[start:end]


def _section(rel: str) -> str:
    return _flat("\n".join(_section_lines(rel)))


spec_panel = pytest.mark.parametrize("rel", SPEC_PANELS)


@spec_panel
def test_t1_usage_line_names_the_re_review_flags(rel):
    usage = next(line for line in _lines(rel) if line.startswith("/sc:spec-panel "))
    assert "[--re-review <prior-findings-file> --baseline <saved-copy>]" in _flat(usage)


@spec_panel
def test_t2_section_exists_once_before_output_formats(rel):
    lines = _lines(rel)
    assert lines.count(HEADING) == 1
    assert lines.index(HEADING) < lines.index("## Output Formats")


@spec_panel
def test_t3_seven_single_line_bullets_in_order(rel):
    body = [line for line in _section_lines(rel) if line.strip()]
    bullets = [line for line in body if re.match(r"^[1-7]\. \*\*", line)]
    assert body == bullets, (
        "every non-blank line of the section must be one of the seven bullets"
    )
    assert [re.match(r"^(\d)\. \*\*([^*]+)\*\*", b).groups() for b in bullets] == [
        (str(i), name) for i, name in enumerate(BULLET_NAMES, start=1)
    ]


CAP_LITERALS = (CANONICAL_CAP_TEXT, AT_CAP_CLAUSES[1])
VOCABULARY = (
    "resolved|open|regressed",
    "origin=changed|unchanged",
    "verdict: PASS",
    "verdict: FAIL",
    "review: N of 3",
    "Reviser brief",
    "byte size before and after",
)
LOOKUP_ORDER = (
    "the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`"
)
SPEC_REVIEW_FIXES = (
    "ignores `--iterations`",
    "`regressed` = a finding the prior report marked resolved that fails again",
    "never fall back to a first review",
)
PRECEDENCE = (
    "a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, "
    "and may not grade a minor finding as blocking"
)


@spec_panel
@pytest.mark.parametrize("literal", CAP_LITERALS, ids=["t4-cap-text", "t4-at-cap-halt"])
def test_t4_cap(rel, literal):
    assert literal in _section(rel)


@spec_panel
@pytest.mark.parametrize(
    "literal", VOCABULARY, ids=[f"t5-{i}" for i in range(len(VOCABULARY))]
)
def test_t5_vocabulary(rel, literal):
    assert literal in _section(rel)


@spec_panel
def test_t6_project_rf_qa_lookup_comes_first(rel):
    section = _section(rel)
    assert LOOKUP_ORDER in section
    assert section.index(".claude/agents/rf-qa.md") < section.index(
        "~/.claude/agents/rf-qa.md"
    )


@spec_panel
@pytest.mark.parametrize(
    "literal",
    SPEC_REVIEW_FIXES,
    ids=["t7-iterations", "t7-regressed", "t7-no-first-review"],
)
def test_t7_spec_review_fixes(rel, literal):
    assert literal in _section(rel)


@spec_panel
def test_t8_precedence_sentence(rel):
    assert PRECEDENCE in _section(rel)


@spec_panel
def test_t9_section_names_no_source_path(rel):
    # Scoped to the section: the whole file names one such path elsewhere and must not be asserted.
    assert "src/superclaude" not in _section(rel)


@pytest.mark.parametrize("rel", HOW_WE_WORK)
@pytest.mark.parametrize(
    "literal", ("--re-review", "--baseline", "save a copy of the PRD")
)
def test_t10_routing_guide_sentence_carries_the_new_flags(rel, literal):
    reporting = [line for line in _lines(rel) if "It only reports." in line]
    assert reporting, "routing guide lost the 'It only reports.' sentence"
    assert all(literal in _flat(line) for line in reporting)


@pytest.mark.parametrize("rel", HOW_WE_WORK + RELEASE_GUIDES)
def test_t10_old_sentence_is_gone(rel):
    assert OLD_SENTENCE not in _flat("\n".join(_lines(rel)))
`````

### tests/skills/test_review_loop_extension.py:1-127

`````python
"""Pins for the Review Loop extension of ``/sc:spec-panel`` (#346, phase P4).

Each clause answers a failure seen in the #346 experiments and is prose only: no
parser, script or state machine. The seven Review Loop bullets stay single lines
in their existing order (``test_spec_panel_review_loop.py``).

Enforcement type: STATIC - assertions over the text of both spec-panel copies.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
spec_panel = pytest.mark.parametrize("rel", SPEC_PANELS)


def _flat(text: str) -> str:
    return " ".join(text.split())


def _bullet(rel: str, number: int) -> str:
    lines = (_REPO / rel).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Review Loop") + 1
    return _flat(
        next(line for line in lines[start:] if line.startswith(f"{number}. **"))
    )


@spec_panel
def test_provenance_in_the_report_header(rel):
    mode = _bullet(rel, 1)
    assert (
        "records the SHA-256 of the candidate and, when a baseline was given, of the baseline"
        in mode
    )
    assert "the reviewer model actually used" in mode
    assert "cannot be taken stops the run like an unreadable file" in mode
    assert "never fall back to a first review" in mode  # existing pin kept


@spec_panel
def test_fail_closed_on_a_missing_or_ambiguous_report(rel):
    verdict = _bullet(rel, 3)
    assert "a re-review report with no prior-findings table" in verdict
    assert "any report whose final `verdict:` line is missing or ambiguous" in verdict
    assert "any report that cites a finding id absent from its table" in verdict
    assert "as `verdict: FAIL`, never as PASS and never as zero findings" in verdict


@spec_panel
def test_first_review_path_is_not_made_to_fail_by_the_new_clauses(rel):
    """A first review has no prior-findings table and may have no baseline."""
    mode, verdict = _bullet(rel, 1), _bullet(rel, 3)
    # the missing-table condition is scoped to re-review reports only
    assert "a report whose prior-findings table" not in verdict
    # the baseline hash is only required when a baseline was given
    assert "when a baseline was given" in mode
    assert "SHA-256 of the baseline and of the candidate" not in mode


@spec_panel
def test_no_edits_between_the_second_fix_and_the_third_review(rel):
    cap = _bullet(rel, 4)
    assert "after the second fix cycle only the third review runs" in cap
    assert (
        "a severity or necessity audit before it only reports and edits nothing" in cap
    )
    assert "at most 2 fix cycles (3 reviews)" in cap  # cap unchanged


@spec_panel
def test_identity_and_open_counting_of_prior_findings(rel):
    out = _bullet(rel, 5)
    assert "each keeps its id from the prior report" in out
    assert "deferred or withdrew" in out
    assert "cannot match to a prior id with certainty, counts as open" in out
    assert "`resolved|open|regressed`" in out  # existing vocabulary kept


@spec_panel
def test_scoped_pass_names_its_coverage(rel):
    out = _bullet(rel, 5)
    assert "`scoped PASS: changed lines + prior blockers`" in out
    assert "whole-document assurance needs a separate, labelled first review" in out
    assert "never start a fourth review" in out


@spec_panel
def test_reviser_prefers_deleting_and_reports_gross_bytes(rel):
    reviser = _bullet(rel, 6)
    assert "prefers deleting or narrowing to adding" in reviser
    assert "byte size before and after" in reviser  # existing pin kept
    assert "bytes added and deleted per finding id" in reviser
    assert not re.search(r"\b\d+ ?(bytes|words)\b", reviser), "no numeric budget"


@spec_panel
def test_brief_cannot_regrade_or_authorize_minor_edits(rel):
    prec = _bullet(rel, 7)
    assert (
        "may not widen it past the changed lines and the prior blocking findings"
        in prec
    )
    assert (
        "cannot make a minor or Medium finding fail the review or authorize editing one"
        in prec
    )
    assert 'including through "apply all findings"' in prec
    assert "the report names any brief clause it overrode" in prec


@spec_panel
def test_section_adds_no_script_or_parser_requirement(rel):
    lines = (_REPO / rel).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Review Loop") + 1
    end = next(i for i in range(start, len(lines)) if lines[i].startswith("## "))
    section = _flat("\n".join(lines[start:end])).lower()
    for word in ("parser", "script", "state machine", "transcript", "asynchronous"):
        assert word not in section, word
`````

### tests/skills/test_review_brief_placement.py:1-140

`````python
"""Placement pins for the coordinator review/revise prompts (#346, P7 refactor 1: single home plus mechanical evidence).

All prompt text lives only in the rules file. The command carries a one-sentence hard gate that restates no role,
procedure or prompt text, and the routing guide points at that gate, not at the file. Static text assertions only.
"""

from __future__ import annotations

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
GUIDES = (
    "src/superclaude/core/HOW-WE-WORK.md",
    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
)
RULES_FILE = _REPO / "src/superclaude/rules/prompts/document_review_loop_prompts.md"
REF = "~/.claude/rules/prompts/document_review_loop_prompts.md"
LABELS = ("First-review brief", "Re-review brief", "Revise brief")


def _text(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


def _gate_paragraph(rel: str) -> str:
    text = _text(rel)
    head = "\n## Review-loop prompts (hard gate)\n\n"
    assert head in text, rel
    after = text.split(head, 1)[1]
    return after.split("\n\n", 1)[0]


def test_rules_file_holds_all_prompt_text():
    text = RULES_FILE.read_text(encoding="utf-8")
    for label in LABELS:
        assert f'- {label}: "' in text, label
    for token in (
        "FIRST-REVIEW prompt",
        "RE-REVIEW prompt",
        "REVISE prompt",
        "## When to use which prompt",
        "## Values to fill",
        "## Never",
        "| ROLE | FILE VALUE | MEANING |",
        "| CANDIDATE | the `@file` of the command | the revised text under review |",
        "| BASELINE | the `--baseline` file | the text as it was before the revision |",
        "| PRIOR | the `--re-review` file | the previous review report |",
        "never infer a role from reading order or from memory",
        "Step 1, the evidence block",
        "`diff -w BASELINE CANDIDATE`",
        "`BEFORE (baseline)`",
        "`AFTER (candidate)`",
        "If the diff is empty, every prior blocking finding stays open",
        "N is the number in PRIOR's `review: N of 3` header plus 1",
        "Example: a prior `review: 2 of 3` gives `review: 3 of 3`",
        "Use no other header variant",
        "`grep -nF`",
        "you swapped roles: redo Step 1",
    ):
        assert token in text, token
    for ph in ("{{CANDIDATE}}", "{{BASELINE}}", "{{PRIOR}}", "{{N}}", "{{IDS}}"):
        assert ph in text, ph
    assert "src/superclaude" not in text
    assert not re.search(r"Prompt (R\d|V\d)", text), "old prompt names must be gone"
    assert "<!-- core:" not in text, "refactor 1 has no mirrored core block"


def test_spec_panel_gate_is_one_sentence_that_restates_nothing():
    for rel in SPEC_PANELS:
        para = _gate_paragraph(rel)
        assert para.count("\n") == 0, rel
        assert (
            f"read `{REF}` in full and follow its prompt for your task step by step"
            in para
        )
        assert "return `incomplete` and review nothing" in para
        assert para.count(". ") == 0 and para.endswith("."), "one sentence"
        for forbidden in (
            "CANDIDATE",
            "BASELINE",
            "PRIOR",
            "{{",
            "Step 1",
            "diff -w",
            "FIRST-REVIEW",
            "RE-REVIEW",
            "REVISE",
            "evidence",
        ):
            assert forbidden not in para, (rel, forbidden)
        text = _text(rel)
        for label in LABELS:
            assert f'- {label}: "' not in text, (rel, label)
        lines = text.splitlines()
        start = lines.index("## Review Loop") + 1
        end = next(i for i in range(start, len(lines)) if lines[i].startswith("## "))
        assert lines[end] == "## Review-loop prompts (hard gate)"
        assert "src/superclaude" not in "\n".join(lines[end : end + 8])


def test_guide_points_at_the_gate_not_the_file_and_holds_no_prompt_text():
    for rel in GUIDES:
        text = _text(rel)
        assert (
            'follow the "Review-loop prompts (hard gate)" section of `/sc:spec-panel`'
            in text
        )
        assert "do not write the brief yourself" in text
        assert "document_review_loop_prompts" not in text, rel
        for label in LABELS:
            assert f'- {label}: "' not in text, (rel, label)


def test_installer_ships_the_rules_file(tmp_path):
    from superclaude.cli import install_user_setup as setup

    ok, message = setup.install_rules(home=tmp_path)
    assert ok, message
    assert (
        tmp_path / ".claude/rules/prompts/document_review_loop_prompts.md"
    ).is_file()


def test_plugin_bundles_the_rules_file_and_the_gate_falls_back_to_it():
    # Plugin-only installs get no ~/.claude/rules; the plugin carries a byte copy.
    bundled = (
        _REPO / "plugins/superclaude/rules/prompts/document_review_loop_prompts.md"
    )
    assert bundled.read_bytes() == RULES_FILE.read_bytes()
    para = _gate_paragraph("plugins/superclaude/commands/spec-panel.md")
    assert (
        "`${CLAUDE_PLUGIN_ROOT}/rules/prompts/document_review_loop_prompts.md`" in para
    )
    build = (_REPO / "scripts/build_superclaude_plugin.py").read_text(encoding="utf-8")
    assert '"rules"' in build
`````

### tests/review/test_review_rules_text.py:1-92

`````python
"""The review-loop rules file carries the findings-block, fix-map and panel text exactly once (PN1, C4.3 and section E)."""

from __future__ import annotations

from pathlib import Path

RULES = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/rules/prompts/document_review_loop_prompts.md"
)
TEXT = RULES.read_text(encoding="utf-8")

INS_A = '- **Findings block**: end the report with the findings block described under "Findings block" below, one line per finding, blocking or not.'
INS_B = '- **Findings block**: end the report with the findings block described under "Findings block" below: one line per finding you report and one prior line per prior blocking finding.'
INS_C = (
    '- **Fix map**: end your output with the fix map described under "Fix map" below.'
)
HEAD_D = "### Findings block"
HEAD_FIX = "### Fix map"
HEAD_E = "### Review panel"
E_FIRST = "Run each review with the reviewers that `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>` prints"


def lines():
    return TEXT.splitlines()


def test_each_insertion_is_present_exactly_once():
    for needle in (INS_A, INS_B, INS_C, HEAD_D, HEAD_FIX, HEAD_E):
        assert TEXT.count(needle) == 1, needle
    assert TEXT.count(E_FIRST) == 1


def test_insertions_a_b_c_follow_their_brief_lines():
    ls = lines()
    for prefix, ins in (
        ('- First-review brief: "', INS_A),
        ('- Re-review brief: "', INS_B),
        ('- Revise brief: "', INS_C),
    ):
        i = next(n for n, line in enumerate(ls) if line.startswith(prefix))
        assert ls[i + 1] == ins, prefix


def test_d_then_fix_map_then_e_come_before_never():
    ls = lines()
    never = ls.index("## Never")
    d = ls.index(HEAD_D)
    fix = ls.index(HEAD_FIX)
    e = ls.index(HEAD_E)
    assert d < fix < e < never
    assert ls[d - 1] == "" and ls[never - 1] == ""
    assert ls[e - 1] == ""
    assert "Only these scripts change a finding's status" in "\n".join(ls[e:never])
    assert "superclaude review ledger revise --ledger" in "\n".join(ls[e:never])
    assert (
        "If the `superclaude` command is not installed, run one reviewer and say so in the loop summary."
        in TEXT
    )
    fix_para = ls[fix + 2]
    assert fix_para.startswith("The reviser ends its output with `## Fix map`")
    assert ls[fix + 3] == ""


def test_d_text_is_the_contract_text():
    for token in (
        "The last section of every review report is `## Findings block`: one fenced code block whose info string is `findings-v1`",
        '{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "<text copied exactly from the candidate>", "anchor2": "<optional second exact quote>", "refs": ["AC-0.4"], "claim": "<one sentence naming the wrong outcome>"}',
        '{"prior": "L3", "status": "resolved"}',
        "The block restates the findings discussed above it and adds none. The verdict line stays the reviewer's verdict.",
        '{"id": "L3", "action": "applied", "reason": "<one sentence>"}',
    ):
        assert token in TEXT, token


def test_older_pins_still_hold_and_no_source_path():
    for token in (
        "FIRST-REVIEW prompt",
        "RE-REVIEW prompt",
        "REVISE prompt",
        "## When to use which prompt",
        "## Values to fill",
        "## Never",
        "| ROLE | FILE VALUE | MEANING |",
        "Step 1, the evidence block",
        "`diff -w BASELINE CANDIDATE`",
        "you swapped roles: redo Step 1",
    ):
        assert token in TEXT, token
    for label in ("First-review brief", "Re-review brief", "Revise brief"):
        assert f'- {label}: "' in TEXT
    assert "src/superclaude" not in TEXT
`````

### src/superclaude/rules/prompts/document_review_loop_prompts.md:1-74

`````markdown
# Document Review Loop Prompts

Prompts for a coordinator that briefs a reviewer or a reviser in a document review loop (`/sc:spec-panel --mode critique`). This file is read on demand and never auto-loaded. `/sc:spec-panel` makes reading it a hard gate before a re-review and before any review or revise brief is written or accepted.

## When to use which prompt

| Situation | Prompt |
|---|---|
| First review of a document | FIRST-REVIEW prompt |
| Any re-review (review 2 or 3) | RE-REVIEW prompt |
| After a review report with open blocking findings, to revise | REVISE prompt |

At `review: 3` with an open blocking finding the loop escalates to the user; no REVISE prompt and no fourth review.

## Values to fill

- `{{CANDIDATE}}`: the revised file under review, the `@file` of the command.
- `{{BASELINE}}`: the `--baseline` file.
- `{{PRIOR}}`: the `--re-review` file.
- `{{N}}`: the number in the prior report's `review: N of 3` header plus 1.
- `{{IDS}}`: the blocking finding ids listed in the report's `Reviser brief`, and only those.

A brief that names the roles differently, or does not name them, does not change them: the table in the re-review core below decides.

## Prompts

### FIRST-REVIEW prompt

Write `review: 1 of 3` once, as the first line of the report.

- **Grading check**, for each finding before you mark it blocking. Write the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass. Grade it Medium when the sentence needs a guess that the implementer picks the worse of two readings the text allows, or when the finding is a requirement the document never states (a missing restriction, an undefined state, an unspecified edge case) rather than a stated text that does harm. A Medium finding goes under follow-up candidates even when its label is MAJOR.
- First-review brief: "Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."
- **Findings block**: end the report with the findings block described under "Findings block" below, one line per finding, blocking or not.

### RE-REVIEW prompt

Follow the re-review core below in order (roles, Step 1, review number, self-check), then use this brief.

| ROLE | FILE VALUE | MEANING |
|---|---|---|
| CANDIDATE | the `@file` of the command | the revised text under review |
| BASELINE | the `--baseline` file | the text as it was before the revision |
| PRIOR | the `--re-review` file | the previous review report |
- **Step 1, the evidence block**, before any finding. Roles are fixed: never infer a role from reading order or from memory. Run `diff -w BASELINE CANDIDATE` and copy the changed lines verbatim under `BEFORE (baseline)` (lines starting `<`) and `AFTER (candidate)` (lines starting `>`). Decide each prior blocking finding marked resolved as resolved or regressed by comparing its defect with the AFTER text only. If the diff is empty, every prior blocking finding stays open.
- **Review number**: N is the number in PRIOR's `review: N of 3` header plus 1. Write `review: N of 3` once, as the first line of the report. Example: a prior `review: 2 of 3` gives `review: 3 of 3`. Use no other header variant.
- **Self-check before the verdict**, when commands can be run: `grep -nF` each quoted AFTER line (without its `>`) in CANDIDATE and each quoted BEFORE line (without its `<`) in BASELINE. If any quote is not found, you swapped roles: redo Step 1. A PASS requires the AFTER text to be consistent with every requirement that depends on it.

- Re-review brief: "Review the revised candidate {{CANDIDATE}} (sha256 of the file) against {{BASELINE}}, the spec as it was before the revision (sha256 of the file), using prior report {{PRIOR}} (sha256 of the file), review {{N}} of 3, where N is the prior report's review number plus 1. Do Step 1, the evidence block, before any finding. Re-check each prior blocking finding as resolved, open or regressed against the revised candidate. Inspect changed behavior and the dependencies it touches; for inherited text, cite the changed line it depends on. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. Record a severe defect you newly discover even if it is older, and say where it came from. If an input is missing or unreadable, return incomplete. Run the self-check before the verdict. Do not edit the candidate and do not start another review. State what you covered."
- **Findings block**: end the report with the findings block described under "Findings block" below: one line per finding you report and one prior line per prior blocking finding.

### REVISE prompt

- Revise brief: "Repair only the blocking findings {{IDS}} in the revised candidate {{CANDIDATE}}. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS."
- **Fix map**: end your output with the fix map described under "Fix map" below.

### Findings block

The last section of every review report is `## Findings block`: one fenced code block whose info string is `findings-v1`, holding one JSON object per line and nothing else. A report with no finding has an empty block.

- Finding line: `{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "<text copied exactly from the candidate>", "anchor2": "<optional second exact quote>", "refs": ["AC-0.4"], "claim": "<one sentence naming the wrong outcome>"}`. `severity` is CRITICAL, MAJOR or MINOR. `blocking` is true only for a finding that passes the grading check. `category` is one of contradiction, unpassable-check, data-loss, safety, missing-requirement, other. `anchor` is 12 to 200 characters copied exactly from the candidate: the text that is wrong; for a contradiction `anchor2` is the other side. `refs` lists the requirement ids and section numbers the finding rests on.
- Prior line, re-reviews only: `{"prior": "L3", "status": "resolved"}`, with status resolved, open or regressed, one line per prior blocking finding id.
- The block restates the findings discussed above it and adds none. The verdict line stays the reviewer's verdict.

### Fix map

The reviser ends its output with `## Fix map`: one fenced code block whose info string is `fixmap-v1`, one JSON object per line, `{"id": "L3", "action": "applied", "reason": "<one sentence>"}`, with action applied or rejected, one line per blocking id in the brief.

### Review panel

Run each review with the reviewers that `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>` prints (a panel for a first review, one reviewer for a re-review by default): each in a fresh context with the same brief, none seeing another's report or transcript. Merge the reports with `superclaude review merge`, also for a single reviewer; its merged report and the ledger it keeps give the verdict and the Reviser brief ids. After the reviser finishes, record its work before the next merge with `superclaude review ledger revise --ledger <ledger> --old <candidate before the revision> --new <candidate after it> --fixmap <the reviser's output>`: it moves the rows the reviser applied to `resolved_check`, the only state a clean re-review clears, so without it corrected findings stay open and the next review still fails. A merge refuses a round in which no reviewer produced a valid findings block; run that review again. Only these scripts change a finding's status. If the `superclaude` command is not installed, run one reviewer and say so in the loop summary.

## Never

Never put "any finding of any severity is FAIL", "assume defects remain", a required number of findings, or "apply all findings" in a brief: a brief may narrow the command's scope but may not widen it or regrade a minor finding as blocking.
`````

### tests/skills/test_worker_contract.py:456-472

`````python
P2_COMMANDS = (
    "auggie-review",
    "cleanup",
    "improve",
    "cli-eval",
    "cli-portify",
    "recommend",
    "research",
    "review-translation",
    "spec-panel",
    "task",
    "tasklist",
    "reflect",
    "release-split",
    "tdd",
    "troubleshoot",
)
`````

### tests/skills/test_worker_contract.py:612-626

`````python
            "an explicit `--strategy intent` or `--strategy unified` is refused",
        ],
        "nested": [],
    },
    "spec-panel": {
        "flags": ["--target-release", "--improve", "--output"],
        "phrases": [
            "target_release",
            "blocked_question",
            "improved-spec.md",
            "spec-panel-report.md",
            "never modified",
            "a TDD input without `--target-release` resolves as blocked",
        ],
        "nested": [],
`````

### tests/skills/test_worker_contract.py:893-927

`````python
def _unattended_section(name: str) -> str:
    """The text of `## Unattended mode` up to the next `## ` heading."""
    lines = (
        (Path(_THIS.COMMANDS_DIR) / f"{name}.md").read_text(encoding="utf-8")
    ).splitlines()
    start = next(
        (i for i, ln in enumerate(lines) if ln.rstrip() == "## Unattended mode"), None
    )
    assert start is not None, f"{name}: no `## Unattended mode` section"
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    return "\n".join(lines[start:end])


def _check_unattended_section(text: str, expect: dict) -> None:
    for need in (
        "return-contract.yaml",
        "~/.claude/WORKER-CONTRACT.md",
        "--report-dir",
    ):
        assert need in text, f"section lacks {need!r}"
    for tok in expect.get("flags", []):
        assert _token_re(tok).search(text), f"section lacks flag {tok!r}"
    for phrase in expect.get("phrases", []):
        assert phrase in text, f"section lacks {phrase!r}"
    nested = expect.get("nested", [])
    for name in nested:
        assert f"nested/{name}-" in text, f"section lacks nested/{name}-"
    if not nested:
        assert "nested/" not in text, "section names a nested directory"
    assert "src/superclaude/" not in text, "section names a src/superclaude/ path"
    assert not _ORCA_NAME_RE.search(text), "section names an Orca command"

`````

### tests/skills/test_worker_contract.py:1296-1304

`````python


def _artifacts_clause(text: str) -> str:
    """The rest of the line after the first `artifacts` key (backticked or YAML)."""
    line = next(
        ln for ln in text.splitlines() if re.search(r"`artifacts`|^artifacts:", ln)
    )
    return re.split(r"`artifacts`|^artifacts:", line, maxsplit=1)[1]

`````

### tests/skills/test_worker_contract.py:1917-1928

`````python
@pytest.mark.parametrize("cmd", P2_COMMANDS)
def test_p2_artifacts_clause_follows_f1(cmd):
    clause = _artifacts_clause(_unattended_section(cmd))
    _check_f1_clause(clause)
    for broken in (
        clause.replace(F1_PHRASE, ""),
        clause + " git refuses it",
        clause + " git add it",
    ):
        with pytest.raises(AssertionError):
            _check_f1_clause(broken)

`````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:17-31

`````markdown
## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17), metrics (M1 to M13), revert triggers (RT1 to RT8) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder. The stage 0 package is `TASK-WF-blockerStage0-20261116-021044`, the stage 1 package `TASK-WF-blockerStage1-20261116-030154` and the stage 2 package `TASK-WF-blockerStage2-20261116-030156`.
- One package, one stage. This is stage 3 of five packages (one plan per stage). It changes the live review rule. It runs only when all of these hold, each checked by reading files and not by memory, and all of them checked in Task 1 before any agent is spawned and before any file under `src/` or `tests/` changes: the owner's go for stage 3 is recorded in the stage ledger together with the list of shadow-run folders the owner counted; a recount of those folders with the stage 2 package's `./artifacts/shadow_summary.py` shows at least 5 observed shadow runs, zero safety misses (by the definition the stage 0 spec edit drafted) and no capture failure; the stage 0 package's `stage0b-escape-test.md` and `stage0c-regrade.md` exist. The stage 2 package's `./artifacts/stage2-summary-for-owner.md` is written when stage 2 finishes and states the runs observed up to then (zero is allowed), so this package does not use its run count. `/sc:implement` runs this whole package in order, so no later task starts unless Task 1 and the seeded-recall gate of Task 5 pass. Stage 4 starts only after one audit window with no revert trigger tripped (spec section 13.2) and the owner's go in chat.
- Gates are read, never edited. No task and no fix pass edits the stage ledger row, a stage 0 or stage 2 file, the seeded-recall result or its answer key to turn a failing line into a pass. A failing gate halts the run for the owner's Ruling. An owner ruling counts only as Task 3 defines it.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Retired carriers are not edited. The owner is retiring `/sc:task` and the task-builder: no task here edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`. `src/superclaude/skills/task/SKILL.md` still holds two merge-rule lines; the stage 1 allow-list in `refs/scale-map.md` lists that path as `exempt-by-retirement` (by path only), and the exemption ends when the retirement removes the file. Tests that exist only to pin the retired files are not re-pinned here; where one test pins both a retired and an active carrier, only the active carrier's part is re-pinned.
- Follow-up carrier. The sweep call and the printed follow-up list sit in `/sc:implement`'s final review step: the stage 2 package put them in `src/superclaude/skills/sc-implement-protocol/SKILL.md` (final summary instructions) and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (archive gate, run before the package moves). This stage only adds `--promote` to that call (Task 9). The carrier records and prints and asks nothing, because `refs/qa.md` keeps its own scale and its closed list of interrupts; the once-per-run offer question stays with the top-level session through the output style (the Medium rule of `pragmatic.md`, changed from per loop to per run in Task 5) and with the consent-bound filing path (OD15), so `/sc:implement` gains no question.
- Plugin surface. IronClaude is installed from the Coder template or from a clone plus `superclaude install`, not as a plugin, so this package creates no plugin surface (no plugin mirror of the skill folder, no plugin parity test, no plugin registry row). Nothing under `plugins/` is edited except the byte-equal twins of the two implement-protocol files that Task 9 edits, which the existing test `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` pins. `src/superclaude/commands/spec-panel.md` and its plugin twin keep their text in this stage: their "once per loop" wording, pinned by `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_review_loop_extension.py` and `tests/skills/test_spec_panel_review_loop.py`, moves with the spec-panel narrowing in stage 4. The registry keeps exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only` and 5 `installed-only`. Whether plugin parity is dropped for good is the owner's decision and is not made here.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), any mapping of `follow-ups.md` to `review-ledger/1` rows or edit of `src/superclaude/cli/review/ledger.py` (version 1 keeps the follow-up ledger as its own file), the 35 percent score target, any change to the cap of 2 fix cycles, and any template, rule-prompt, builder, researcher or spec-panel edit (those are stage 4).
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev` (it copies skills, agents, commands, hooks and templates; it does not copy `output-styles/`, `core/` or `rules/`); staging anything under the project `.claude/` folder is forbidden (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is left out of staging. Staging is not committing.
`````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:186-198

`````markdown
## Phase 4: Re-pin the tests and add the scan test

## Task 10: Re-pin the severity tests in tests/skills

Depends on: Task 5, Task 6, Task 7, Task 9

Update `tests/skills/test_review_severity_rule.py` (`canonical_rule_bullets()` reads the digest from `refs/rule.md`; `S1_S3_FILES` and its `[:6]` slice `S5_FILES` become registry rows of kind `digest`, dispatched by registry state: rows at `v2` (`pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`) are checked against the digest, and rows still at `legacy` (the eight template and rule-prompt files, until stage 4) stay pinned to a frozen copy of the old three bullets held as literal constants in the test; the cap-text and banned-phrase checks stay, and `CANONICAL_CAP_TEXT` stays asserted against the output style only, as today), `tests/skills/test_review_severity_mapping.py` (the pragmatic Medium pin moves from "once per loop" to the once-per-run wording and its position check reads the Medium bullet after the digest and pointer instead of after the old S5 bullet, with new assertions on `refs/rule.md` and `refs/scale-map.md`; the spec-panel pins on "once per loop" stay unchanged because the spec-panel carrier is not edited in this stage), `tests/skills/test_implement_severity_static.py` (S4 kept word for word; the S2 assertion moves to the digest; the `qa.md` pins stay), the fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` (update only the approved changed strings; rows for the retired task skill stay as they are) and the two plan tables the fixtures must be byte copies of, `.dev/review-severity-rule/cap-edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml` (the test `test_ej_fixtures_are_byte_copies_of_the_plan_tables` in `tests/skills/test_review_severity_rule.py` compares them; edit each pair in the same change, or record which relaxation of that test is chosen and why). `tests/skills/test_review_loop_extension.py`, `test_review_prompt_overrides.py` and `test_spec_panel_review_loop.py` must still pass unchanged. Also re-run `tests/skills/test_review_brief_rests_on.py` and `tests/skills/test_review_severity_registry.py` of the earlier stages (the first skips its legacy assertion once the pragmatic row is `v2`), `tests/skills/test_task_builder_merge.py` (it pins the Retry Monotonicity tokens of `rf-qa.md`; its parts that pin only retired carriers are not re-pinned) and `tests/review/test_review_rules_text.py`.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_implement_severity_static.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_brief_rests_on.py tests/skills/test_review_severity_registry.py tests/skills/test_implement_follow_up_sweep.py tests/skills/test_task_builder_merge.py tests/review/test_review_rules_text.py -v` passes, including `test_ej_fixtures_are_byte_copies_of_the_plan_tables` and `test_h_implement_protocol_plugin_twins_byte_equal`.
- The two fixtures change only rows whose new text is the digest or the once-per-run cadence; the diff of each fixture and of each plan table is listed in `./artifacts/fixture-diff.md`.
- No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text, and the rows of `legacy` digest carriers still assert the old text.

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


## Coverage slice

| Requirement | Card ID | Status | Grounding |
|-------------|---------|--------|-----------|
| INF-001: Generate it only after the stage 3 package is done, one audit window has passed with no revert trigger tripped | T1 card | covered (containment 0.821 -> Task 1) | source.md:3 |
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
