# Reviewer brief 3 (persona: refactorer; model class: opus)

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


Persona instructions (refactorer): you own question (b) and the cross-stage structure. (1) Contradictions with the brief and the owner answers (hunks: the revision 2 brief, OPEN-QUESTIONS sections 2.2, 2.3 and 3.4): for EVERY file the plan edits, decide whether it is a retired carrier or 'exists only for' the retired `/sc:task` and task-builder (the two MDTM templates are the case to settle: the plan keeps them as digest carriers) and whether the plan's choice is consistent and forced by the registry and strict T2; check that no plugin surface (mirror folder, parity test, plugin registry row, plugin reverse scan) is created, and that the plugin twins are edited only where an existing test pins them. (2) Cross-stage assumptions: read the stage 1 and stage 3 plan text in your hunks and decide whether Tasks 1, 2, 3, 5 and 6 get what they assume: the registry rows and states, the 'Merge-rule allow-list' section and its entries, how strict mode of T2 is switched (S1 says it is a switch, off in this phase: does stage 1 name the mechanism, and does Task 5's acceptance line prove the switch is on?), the digest text and fence lines, the summary file names, the heading stage 3 gives Rule 6. (3) Task 1's entry gate: check the archive-blocked semantics against the managed-workspace reference in your hunks. (4) Paths that do not exist: Glob or Grep every path and command a task names that no earlier stage creates. (5) Anything in Task 5 or Task 6 that cannot run as written (make targets, commands, artifacts).


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

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/OPEN-QUESTIONS.md:1-88

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
- **Checkout-local `.claude` mirror:** keep the CI check; refresh a live checkout only on explicit request, never automatically from an installed release.
- **Installed-instruction path checks (G10):** keep the checks that stop installed instructions referencing repository-only paths.
- **Combined review-loop, severity and plugin-routing coverage:** earlier answer was to keep it and merge it into a single check. The later installation correction (below) must be read together with it.
- **Installation context correction:** IronClaude is not installed as a plugin. Assume the Coder template, or a git clone followed by SuperClaude installation. Reassess whether plugin-parity coverage is relevant; keep review-loop and severity checks. This is not a decision to remove plugin parity.
- **Static QA coverage:** keep static QA checks for active workflows; remove task-builder-specific checks as part of the task-builder retirement.
- **G16 safeguard:** remove it. Its architecture lint is duplicated under G9, which stays. The PR reminder's value is unverified, and the lost prompt is a recorded trade-off.
- **Salvage from malformed reviewer reports:** remove the proposed salvage of individual blocking findings. No separate handling or verdict policy for malformed reports is approved.
- **Q68 run log and integrity checks:** keep the existing run log, durability and partial-write handling checks and commit-identity checks. Not shown to have run or passed.

### 2.4 Session handling
Acknowledge an answer once, briefly, without repeating it; then move to the next applicable question. Do not invent questions or give duplicate receipts.

## 3. Still open

### 3.1 Follow-up ledger (owner asked the developing agent for evidence, not a choice)
Owner questions: is `follow-ups/1` a replacement or an augmentation of `review-ledger/1`; what each does and how old the existing one is; whether the refactor is implemented and tested; what shows improved performance. Conditional owner direction: if it is a tested refactor that outperforms the existing ledger, it replaces it. That condition is not established.

Evidence so far (checked 2026-11-16):
- `review-ledger/1` (`src/superclaude/cli/review/ledger.py`, tests `tests/review/test_review_ledger.py`) first appears in master in the #346 merge of 2026-11-11, about 5 days old. Unmerged branches were not checked. It stores review rounds, blocker states and PASS, REVISE or ESCALATE.
- `follow-ups/1` is a per-run Markdown queue for non-blocking findings, user choices, consent, filing and dispositions (spec lines 338 and 404). `src/superclaude/cli/review/follow_ups.py` does not exist. No reuse audit or comparative test exists. The five-run experiment is not a ledger comparison.
- The spec leaves the mapping from follow-up rows to `review-ledger/1` rows to the plan (line 404), and the reuse-auditor must run first (line 879). The stage 1 plan has that task.

Remaining question: after the reuse audit, do follow-up rows map into `review-ledger/1`, or stay a separate file? Answer it from the stage 1 reuse-audit result.

### 3.2 Blocker programme owner decisions not yet decided
OD3 (finding text to an external judge, key and budget; privacy first), OD5, OD6, OD7, OD8, OD10, OD14 (decide after stage 3 data), OD17. Plans assume the spec's recommendations for the rest (OD1, OD2, OD4, OD9, OD11 to OD13, OD15, OD16). OD4 (no classifier authority in version 1) stays. Per 2.1, Jev investigation does not decide OD3.

### 3.3 Plan packages and their reviews

| Stage | Package | First review | State on 2026-11-16 |
|---|---|---|---|
| 0 | `TASK-WF-blockerStage0-20261116-021044` | NEEDS-REVISION (2 blocking, 9 non-blocking) | revised in place; not re-reviewed |
| 1 | `TASK-WF-blockerStage1-20261116-030154` | NEEDS-REVISION (2 blocking, 7 non-blocking) | revision 2 applied (16 tasks); re-review pending |
| 2 | `TASK-WF-blockerStage2-20261116-030156` | run never finished (no verdict) | revision 2 applied (8 tasks); first review pending |
| 3 | `TASK-WF-blockerStage3-20261116-030158` | NEEDS-REVISION (7 blocking, 8 non-blocking); no `REPORT.md` | revision 2 applied (13 tasks, 5 phases); re-review pending |
| 4 | `TASK-WF-blockerStage4-20261116-030206` | NEEDS-REVISION (2 blocking, 12 non-blocking); no `REPORT.md` | revision 2 applied (6 tasks); re-review pending |

Every first-review blocking finding was applied in revision 2 (details in each package's `artifacts/codegraph-grounding.md`, section "Revision 2", and in `stage-requests/stageN-request.md`). Whether the revisions hold is not known until the re-reviews run. The first-review reports and cards are under `.dev/reflect/pre-TASK-WF-blockerStage<N>-*/`.

### 3.4 Decisions the plan author made for the 2026-11-16 answers (owner has not confirmed these)
- Follow-up carrier: approved as `/sc:implement`'s final review step. Built as record and print only, because `refs/qa.md` line 225 says the final summary never asks the user anything and `qa.md` is on the do-not-edit list. The once-per-run offer stays with the output style (stage 3 changes the Medium rule from per loop to per run). Consequence: under `/sc:implement`, a promoted follow-up adds no stop path, so the "blocking at the final gate" effect of OD14 shows only as a printed list. OD14 deferral stays off by default.
- `/sc:task`, task-builder and `rf-task-builder` are not edited; the scan allow-list lists them `exempt-by-retirement`. Tests that pin only them are not re-pinned.
- Plugin: no new mirror folder, parity test or plugin registry row. Existing plugin twins (`spec-panel.md`, the rules prompt, and the `sc-implement-protocol` copy, which two existing tests pin byte for byte) are edited only where a test pins them. The owner's answer said to reassess plugin parity, not to remove it: confirm.
- The two MDTM templates (01 and 02) and the `automated_qa_workflow` prompt stay as digest rows, because the roadmap, readme and tdd skills also use them. If the owner treats them as retired with task-builder, the registry drops to 9 digest rows.
- The new command `follow_ups_cmd.py` (subcommands `write`, `safety`, `sweep`, `summary`) is built by stage 2; `classify_cmd` stays with stage 1. Shadow ledgers can come only from tech-research runs, because `/sc:implement` has no unattended section, so the stage 3 entry (5 observed runs) depends on tech-research runs.

### 3.5 Not yet written
Stage 3 and 4 `REPORT.md` for the first reviews (the cards exist); the return contracts for stages 1 to 4 (written after the re-reviews); owner go rows.
`````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:17-30

`````markdown
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

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:205-231

`````markdown
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

Create `tests/skills/test_review_severity_registry.py` for T1 (every row of kind `digest` holds, in its file, exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; a row at `legacy` is accepted; the `canonical` row holds the source digest), T2 (a reverse scan of the tracked `src/` and `plugins/` trees, the plugin tree being scanned because hand-kept twins already exist there and no row names a plugin path, fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; `canonical` and `pointer-only` rows count as registered; strict mode is a switch, off in this phase), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, ; the check that no carrier contains `src/superclaude` applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, a `pointer-only` row only once its pointer is present, and the test never reads `~/.claude`), T4 (each `repo` row of `refs/scale-map.md` names an existing file under `src/superclaude/`, resolved from the table's `defining file` column, and each native label of its `labels` column is present in that file, compared without regard to case; a row whose `labels` is `none` skips the label check; an `installed-only` row, today the stoprule and `finding-grader` row, is exempt from both checks and is only checked to be marked `installed-only` with `~/.claude/` paths, and the test never reads `~/.claude`) and T14 (a `digest` row at `v2` holds the precedence sentence).

Acceptance criteria:
- A temporary-tree test shows each T3 exemption: a `pointer-only` row whose file holds a `src/superclaude` path passes the path check, a `pointer-only` row without its pointer yet passes, and a `digest` row whose file holds such a path fails.
- `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all `digest` rows at `legacy`.
- A test flips one `digest` row to `v2` without editing its file and fails, which shows T1 can fail; a `pointer-only` row at any state does not fail T1.
- The reverse scan accepts `refs/rule.md` (it has a `canonical` row) and reports a file that holds the definition sentence and is absent from the registry, using a temporary tree in the test.
- A temporary-tree test shows each T4 exemption: an `installed-only` row naming `~/.claude/` paths passes without any file in the tree, a `labels` value of `none` skips the label check, and a `repo` row whose file is missing or lacks one of its labels fails.
- The T4 test reads the same word, `installed-only`, in the `file kind` column that Task 3 writes for the stoprule and `finding-grader` row, so the exemption of the two tasks is one rule.
`````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:15-31

`````markdown
Goal: Check the entry conditions, count the stage 2 baselines and run the seeded-defect recall test under the old and the new rule text; then move `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md` and `rf-analyst.md` to the new rule, turn the final-gate sweep's `promote` switch on in the implement protocol, re-pin the tests that guard them, and give the owner the audit-window numbers, the switch steps and the revert path before the stage 4 go.

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

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:121-135

`````markdown
## Task 5: Move pragmatic.md to digest v2 and change the Medium offer to once per run

Depends on: Task 2, Task 3, Task 4

Edit `src/superclaude/output-styles/pragmatic.md`: replace the three definition bullets (the one that begins "Grade every review finding as blocking or minor", the one that begins "Minor findings never fail a review", and the one that begins "On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking", today lines 225, 226 and 229) with the digest of REQ-01 inside its fence plus the pointer line naming `~/.claude/skills/sc-review-severity/refs/rule.md` first and `.claude/skills/sc-review-severity/refs/rule.md` second. The cap bullet and the own-model bullet ("A protocol that defines its own severity model, such as `/sc:implement`") stay word for word (the cap sentence is also the last sentence of the digest). Change the reviewer brief bullet ("Every review agent MUST review as an independent reader") so reviewers hunt for defects and name their consequence instead of hunting for "false claims" (REQ-04). This task owns the cadence change: in the Medium bullet ("Among minor findings, one that describes a real but non-blocking weakness") replace "asks the user once per loop whether to open an issue for the list" with "asks the user once per run, and again at any escalation halt, whether to open an issue for the list", and keep the rest of that bullet and the spec-panel scale bullet word for word (OD2; the spec-panel carrier keeps its own scale until stage 4). Set the registry row of `output-styles/pragmatic.md` in `src/superclaude/skills/sc-review-severity/refs/registry.yaml` to `v2`. `make sync-dev` does not copy output styles: the installed `~/.claude/output-styles/pragmatic.md` changes only at the refresh that Task 13 describes. The existing pins on the old text (the tests Task 10 re-pins) are red from here until Task 10 and are not run in this task.

Acceptance criteria:
- `./artifacts/seeded-recall-result.md` exists and each of R1, R1b, R2a, R2b and R3 reads PASS, or each line that does not read PASS is covered by an owner ruling in the stage ledger row of PF that names the line, is dated on or after the date the result file was written and cites the file's current SHA-256; a FAIL line without a valid ruling, or a ruling whose hash differs from the file's current SHA-256, fails this check and the run halts for the owner's Ruling. This task does not rely on `Depends on` for the gate.
- `src/superclaude/output-styles/pragmatic.md` holds exactly one fenced digest equal to the digest section of the skill's `refs/rule.md` (its SHA-256 equals the one in `./artifacts/seeded-recall-result.md`), and the registry row for `output-styles/pragmatic.md` reads `v2` (`grep -n -A6 "output-styles/pragmatic.md" src/superclaude/skills/sc-review-severity/refs/registry.yaml` shows state `v2`).
- The cap sentence ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings") and the own-model bullet still appear word for word (`grep -c` of each sentence prints 1 or more).
- `grep -c "asks the user once per loop" src/superclaude/output-styles/pragmatic.md` prints 0, `grep -c "asks the user once per run, and again at any escalation halt" src/superclaude/output-styles/pragmatic.md` prints 1, and the sentences "no issue is created without the user's answer" and "only records the list" and the spec-panel scale bullet ("MAJOR is blocking only when it names a concrete wrong outcome") are still present.
- The hook `pragmatic-subagent.js` still finds and injects the file: `grep -n "pragmatic" src/superclaude/hooks/hooks.json` still matches and `src/superclaude/output-styles/pragmatic.md` exists.
- The new pointer line names `~/.claude/skills/sc-review-severity/refs/rule.md` before the `.claude/` copy and contains no `src/superclaude` path.
- `uv run pytest tests/skills/test_review_severity_registry.py tests/skills/test_review_brief_rests_on.py -v` passes (the stage 2 test's legacy assertion is skipped now that the row is `v2`).

`````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:150-172

`````markdown
## Task 7: Move rf-qa-qualitative.md to digest v2, rewrite its eight FAIL-by-label pairs and apply OD16

Depends on: Task 4, Task 5

Edit `src/superclaude/agents/rf-qa-qualitative.md`: replace S1, S2 and S5 (today around line 108) with the digest and pointer; replace the merge rule (today line 84) with the L1 text; add the L2 pre-handback step to its fix-cycle text and the L3 three choices with the one-offer sentence beside each cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" (today at lines 809 and 994; line 994 is rule 10 inside the `## Critical Rules` block whose hash Task 11 re-pins; the cap sentence itself stays word for word); rewrite or keep as named mechanical gates, recorded in `refs/scale-map.md`, the eight verdict pairs that fail a review on "Any CRITICAL or IMPORTANT issue exists" (the FAIL bullet today at lines 240, 291, 362, 429, 500, 567, 746 and 784, each with its PASS bullet one line above; the list is in the stage 0 package's `./artifacts/stage0-inventory-freeze.md`, read by package id); and rewrite Rule 6 ("Contradictions are always IMPORTANT or CRITICAL ... that's never minor", today line 990) per OD16 option (b), so a contradiction nothing rests on is a follow-up, and keep contradictions that touch a decision basis, a quoted number or a required deliverable as Blocking under condition 1. Set the registry row of `agents/rf-qa-qualitative.md` to `v2`. Run `make sync-dev` afterwards.

Acceptance criteria:
- `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/agents/rf-qa-qualitative.md` prints 0, or each remaining line is listed in `refs/scale-map.md` with its reason.
- `grep -n "that's never minor" src/superclaude/agents/rf-qa-qualitative.md` prints nothing, and the new Rule 6 text names the decision-basis exception.
- The file holds exactly one digest, no `more severe rating` text, and its registry row reads `v2` (`grep -n -A6 "agents/rf-qa-qualitative.md" src/superclaude/skills/sc-review-severity/refs/registry.yaml` shows state `v2`).
- The cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still prints a `grep -c` of 2, each with the three choices and the one-offer sentence, and the L2 step naming `superclaude review fixcheck` is present.
- `uv run pytest tests/skills/test_review_severity_registry.py -v` passes. `tests/audit/test_severity_floor_unweakened.py` is red from this task until Task 11 re-pins the `## Critical Rules` block hash in the same change set.

## Task 8: Replace the merge rule in rf-analyst.md

Depends on: Task 5

Edit `src/superclaude/agents/rf-analyst.md`, the line that reads "union of findings, take the more severe rating for shared items, merge gap compila...", to the L1 text: union the findings, keep each reviewer's own grade visible, and let the consolidator grade by the rule; keep the rest of the line (the gap compilation) unchanged. This agent is not a digest carrier and gets no registry row. Run `make sync-dev` afterwards.

Acceptance criteria:
- `grep -n "more severe rating" src/superclaude/agents/rf-analyst.md` prints nothing.
- The gap-compilation words that followed on the line are still present.

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

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:210-241

`````markdown
## Task 12: Add the merge-rule reverse-scan test

Depends on: Task 6, Task 7, Task 8

Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude` (read only; nothing there is edited), matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`, one bullet per path (relative to `src/superclaude/`) with the status `allowed` or `exempt-by-retirement`: as stage 1 wrote it, `skills/sc-auggie-review-protocol/SKILL.md`, `skills/sc-review-severity/refs/rule.md`, the two code files `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` and, until the stage 4 package, the six stage 4 files (`skills/tech-reference/SKILL.md`, `skills/readme/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/operational-guide/SKILL.md`, `templates/documents/agent_template_qa.md` and `templates/documents/agent_template_analysis.md`) are `allowed`; the retired carriers `skills/task/SKILL.md`, `skills/task-builder/` (every file in the folder) and `agents/rf-task-builder.md` are `exempt-by-retirement`. A row marked `exempt-by-retirement` allows hits while its file exists and is not an error once the retirement has removed the file; every `allowed` row names a file that must exist. The stage 4 package removes each of its six files from the allow-list in the same change that edits it, and adds the plugin mirror of `refs/rule.md` to the allow-list and the registry before it copies the skill folder; the plugin mirror is NOT in the allow-list here.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 6 to 8, with no hit in `src/superclaude/cli/` counted and the two hits in `src/superclaude/skills/task/SKILL.md` accepted only through its `exempt-by-retirement` row.
- A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
- The allow-list is read from `refs/scale-map.md`: a test fails when an `allowed` row names a file that does not exist, and a test shows an `exempt-by-retirement` row whose file or folder is missing does not fail.

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

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:15-22

`````markdown
Goal: Build the `follow-ups` commands (write, safety, sweep, summary) and the record-only sweep; make tech-research write the follow-up ledger; give the final review step of `/sc:implement` one read-only sweep call and a printed follow-up list that asks nothing; add the three worker-contract keys with a named producer; evaluate the classifier on the stage 0 populations; and give the owner the stage 2 numbers before the stage 3 go. The old definition still decides every gate outcome.

## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the scored table in `04-historical/master-table.md`, the panel consensus in `05-scoring/consensus.md`, `OPEN-QUESTIONS.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 2 of five packages (one plan per stage). The old definition still decides every gate outcome. The only exception the spec allows is the GR12 safety route, which asks a reachable person about a possible safety finding that was graded non-blocking and, with nobody reachable, records and does not wait. The sweep only records (`promote` off), the classifier has no authority, and the one sweep call sits in the final review step of `/sc:implement`. tech-research gets no sweep call and no offer. The package runs only after the stage 1 package is done (its modules `follow_ups.py`, `safety_route.py`, `classifier_inputs.py` and the `classify` command exist; Task 1 checks that) and the owner has said go in chat. Stage 3 starts only after the owner reads this package's summary and says go; its entry also needs at least 5 observed shadow runs, which the owner or operator produces over time and no task here can produce.
- Carrier decision (owner, 2026-11-16, recorded in `OPEN-QUESTIONS.md`): the follow-up carrier is the final review step of `/sc:implement`, record and print only. That step prints a list and asks nothing, because `refs/qa.md` of the `/sc:implement` protocol says its final summary "is informational and never asks the user anything" and closes the list of interrupts, so the edit goes into that protocol's `SKILL.md` and `refs/managed-workspace.md` only; the once-per-run offer question stays with the top-level session through the output style (the `pragmatic.md` Medium rule, changed from per loop to per run by the stage 3 package) and with the consent-bound filing path (OD15), and stage 2 adds no question to `/sc:implement`.
- Retired carriers are not edited. `/sc:task` and task-builder are being retired (owner, 2026-11-16). No task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for those; they keep today's text until the retirement removes them. Tests that exist only to pin them are not re-pinned here, and when a test pins both a retired and an active carrier this plan re-pins the active carrier's part only. The stage 1 scale map lists them as exempt-by-retirement by path.
`````

### tests/skills/test_review_severity_rule.py:100-135

`````python
    return _flat(bullet[2:] if bullet.startswith("- ") else bullet)


def test_b_canonical_bullets_follow_binary_verdict_bullet():
    bullets = canonical_rule_bullets()
    assert all(b.startswith("- ") for b in bullets)
    assert not any(re.search(r"\(S[1-5]\)", b) for b in bullets)
    assert not any("contains the canonical cap text" in b for b in bullets)


# --- (a) any-severity wording ----------------------------------------------

BANNED_SEVERITY_PHRASES = (
    "any issue of any severity",
    "issues of any severity",
    "gaps of any severity",
    "at any severity",
    "regardless of severity",
    "no severity level is exempt",
    "minor issues still pass",
    "must still be fixed",
    "still must be fixed",
    "must be perfect to pass",
    "ALL findings must be resolved",
    "CRITICAL, IMPORTANT, and MINOR issues",
)


def _phrase_hits(text: str, phrases) -> list[str]:
    low = text.lower()
    return [p for p in phrases if p.lower() in low]


def _scan_phrases(files: dict[str, str], phrases) -> list[str]:
    hits = []
    for path, text in sorted(files.items()):
`````

### tests/skills/test_review_severity_rule.py:176-285

`````python
    assert not hits, "any-severity wording survives:\n" + "\n".join(hits)


# --- (c) S1-S3 / S5 copies in the ten-file set -----------------------------

S1_S3_FILES = (
    "src/superclaude/agents/rf-qa.md",
    "src/superclaude/agents/rf-qa-qualitative.md",
    "src/superclaude/templates/documents/agent_template_qa.md",
    "src/superclaude/templates/documents/skill_template.md",
    "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md",
    "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md",
    "src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md",
    "src/superclaude/rules/prompts/doc_code_analyst_qa_prompt.md",
    "src/superclaude/rules/prompts/documentation_expert_qa_prompt.md",
    "src/superclaude/rules/prompts/recruiting_expert_qa_prompt.md",
)
S5_FILES = S1_S3_FILES[:6]


@pytest.mark.parametrize("rel", S1_S3_FILES)
def test_c_s1_s3_copied_verbatim(rel):
    flat = _flat(_read(rel))
    s1, s2, s3, _s4, s5 = canonical_rule_bullets()
    for n, bullet in ((1, s1), (2, s2), (3, s3)):
        assert _rule_body(bullet) in flat, f"S{n} missing from {rel}"
    if rel in S5_FILES:
        assert _rule_body(s5) in flat, f"S5 missing from {rel}"


@pytest.mark.parametrize("rel", S1_S3_FILES)
def test_c_no_inventory_labels_or_annotation(rel):
    text = _read(rel)
    assert not re.search(r"\(S[1-5]\)", text), rel
    assert "contains the canonical cap text" not in text, rel


# --- (d) canonical cap text and at-cap clause -------------------------------

CANONICAL_CAP_TEXT = "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"
AT_CAP_CLAUSES = (
    "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings",
    "HALT and escalate to the user with the open blocking findings",
)


@functools.lru_cache(maxsize=None)
def _rows(fixture: str) -> tuple[dict, ...]:
    data = yaml.safe_load((_FIXTURES / fixture).read_text(encoding="utf-8"))
    return tuple(data["rows"])


def test_d_canonical_cap_text_in_style():
    assert CANONICAL_CAP_TEXT in _flat(STYLE.read_text(encoding="utf-8"))
    assert CANONICAL_CAP_TEXT in canonical_rule_bullets()[2]


def test_d_at_cap_clause_present_where_cap_rows_add_it():
    expected: dict[str, set[str]] = {}
    for row in _rows("review_severity_cap_edits.yaml"):
        for clause in AT_CAP_CLAUSES:
            if clause in row["new"]:
                expected.setdefault(row["file"], set()).add(clause)
    assert expected, "no cap-edits row carries the at-cap clause"
    missing = [
        f"{rel}: {clause!r}"
        for rel, clauses in sorted(expected.items())
        for clause in sorted(clauses)
        if clause not in _read(rel)
    ]
    assert not missing, "at-cap clause missing:\n" + "\n".join(missing)


# --- (e) / (j) edit-table rows hold ----------------------------------------


def _failing_rows(fixture: str) -> list[str]:
    bad = []
    for row in _rows(fixture):
        text = _read(row["file"])
        if row["old"] in text or row["new"] not in text:
            bad.append(f"{row['id']} {row['file']}")
    return bad


def test_e_every_cap_edits_row_holds():
    rows = _rows("review_severity_cap_edits.yaml")
    assert len(rows) == 161
    bad = _failing_rows("review_severity_cap_edits.yaml")
    assert not bad, "cap-edits rows not applied:\n" + "\n".join(bad)


def test_j_every_sweep_edits_row_holds():
    rows = _rows("review_severity_sweep_edits.yaml")
    assert len(rows) == 139
    bad = _failing_rows("review_severity_sweep_edits.yaml")
    assert not bad, "sweep-edits rows not applied:\n" + "\n".join(bad)


def test_ej_fixtures_are_byte_copies_of_the_plan_tables():
    for fixture, source in (
        ("review_severity_cap_edits.yaml", "cap-edits.yaml"),
        ("review_severity_sweep_edits.yaml", "sweep-edits.yaml"),
    ):
        plan_copy = _REPO / ".dev/review-severity-rule" / source
        if not plan_copy.exists():
            pytest.skip(f"{plan_copy} not present in this checkout")
        assert (_FIXTURES / fixture).read_bytes() == plan_copy.read_bytes(), fixture


`````

### src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:44-64

`````markdown
  hashes are lowercase hex SHA-256 of the bytes of `<slug>.md` and `source.md`. Every invocation recomputes them. **Before the first `T<id>: start` line** a differing hash is re-pinned by appending a new `PLAN:` line (append-only; never edit). The first `T<id>: start` line is the immutability boundary: afterwards any plan/source hash differing from the latest `PLAN:` line → STOP `E-PLAN-CHANGED`; no repair, no new pin.

## Completion: fresh FINAL, then archive

Dispatch (replaces the legacy "already complete" stop for managed packages): when every task is `complete` and the package is still in `to-do/`, you are **active all-complete** → run the archive gate below. Report `archive-blocked: <reason>` if it cannot finish. Never print `already complete` for an unarchived package.

Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never counts):

1. Join every delegated writer / background task. Nothing may still be writing the package or delivery files.
2. `--skip-final-review` → no FINAL and no archive: STOP `E-ARCHIVE-BLOCKED` (`--skip-final-review` prevents archiving a managed package).
3. State: `uv run --no-project python "<skill base>/scripts/archive_workspace.py" --root "<checkout>" --package "<checkout>/.dev/tasks/to-do/<slug>" --print-state` → JSON `{"status": "state", "state": "<sha256>", "files": [...]}` (the plan/source/delivery-file digest; `files` = every repo-relative path named in a ledger `files=` field, so list every delivery file there). Failure → STOP `E-ARCHIVE-BLOCKED` with the helper's code.
4. One independent reviewer (always a Task subagent, even N=1; `refs/qa.md` isolation rules) gets the current full plan, the full ledger, and the current contents of each listed delivery file. Pass absolute paths (include the package root so `./artifacts/` tokens resolve) or inline contents; the reviewer must read the real current files. It verifies every task's AC against the real files and returns `pass` or `issues` with `path:line` evidence. Missing or unverifiable evidence → `issues`, as `refs/qa.md` (Managed FINAL review) defines it. For a user-accepted gap, verify the current outcome still matches the recorded scoped acceptance and cite the unmet AC honestly; any new or changed unaccepted gap → `issues`. Do not mark unmet AC as met or change the non-compliant task verdict. The reviewer applies the FINAL derived test of `refs/qa.md`: a notes entry whose answers are all `no` is never `issues`, and a notes entry with a confirmed `yes` is `issues`.
5. Re-run step 3. If `state` changed during the review, discard the result and repeat from step 1. Otherwise append (after all task lines and the latest `PLAN:` pin):

```
FINAL: <pass|issues> evidence=<ev-list> state=<sha256>
```

6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says, except the recovery's own re-review of a saved-prompt task. Before that stop, when every `issues` item of the FINAL concerns a saved prompt (a template difference, a superseded prompt with no later passing saved prompt, or a missing README), the executor runs "Defective saved prompt (recovery)" from `refs/qa.md` in the same invocation and then repeats the archive gate from step 1; the recovery is idempotent (it finishes a half-done move, writes a missing README and runs a missing re-review), and the stop applies only if the recovery cannot finish or the new FINAL still returns `issues`.

`<skill base>` is the base directory the loaded skill announces (the directory holding this skill's `SKILL.md`); never hardcode a repository `src/` path. A FINAL pass is not a commit, PR, merge, release or human approval.
`````

### src/superclaude/templates/documents/agent_template_qa.md:80-95

`````markdown

The orchestrator (skill session or team lead) is responsible for:
- Deciding when to partition (based on file count — typically >6 files warrants partitioning)
- Dividing files into balanced subsets
- Spawning multiple [agent-name] instances in parallel, each with its `assigned_files` list
- Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items)

---

<!-- CLASSIFICATION: SUBSTITUTE — 3 shared principles (BOILERPLATE) + domain-specific principles (GENERATE) -->
## Verification Principles

0. **Independent stance**: Review as a reader who did not write this work. Look for concrete defects and report each one with evidence; there is no minimum count. A review that finds none is valid when it states what was checked; do not invent findings to avoid a zero.

<!-- SPECIALIZATION: DOMAIN_PRINCIPLES — Domain-specific verification principles. Number sequentially starting from 1. Examples from existing QA agents:
  - rf-qa (10 principles total): Zero tolerance for blocking defects, Evidence-based, Clear documentation, Actionable feedback, Consistent standards, Source truth is king, Complete means complete, NO LENIENCY, Self-audit
`````

### src/superclaude/templates/documents/agent_template_qa.md:150-165

`````markdown
### Stakeholder Personas
Read through these lenses simultaneously:
- **[Persona 1]:** [What this persona cares about — e.g., "Product Manager: Does this solve the stated problem?"]
- **[Persona 2]:** [What this persona cares about — e.g., "Engineering Lead: Is this implementable as described?"]
- **[Persona 3]:** [What this persona cares about — e.g., "QA Engineer: Can I write test cases from these requirements?"]

### Verdict
- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.

Review severity rule (applies to every verdict):
- Grade every review finding as blocking or minor. Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk. Minor is cosmetic, wording, formatting, citation format, a nit, style, or a moved line number on a true claim.
- Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. Minor findings are not rechecked in later rounds and never trigger a fix pass on their own. Only blocking findings produce FAIL.
- A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings.

---
`````

### src/superclaude/templates/documents/agent_template_qa.md:186-192

`````markdown
4. Updated verdict: PASS / FAIL

### Rules

- Maximum 2 fix cycles. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. Do NOT convert unfixed findings to Open Questions.
- Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.

`````

### src/superclaude/templates/documents/agent_template_qa.md:326-341

`````markdown
<!-- CLASSIFICATION: SUBSTITUTE — Shared boilerplate rules at template positions (1, N+1, N+2, N+3) copied verbatim from rf-qa.md. Mapping: template position 1 = rf-qa.md rule 1 (incremental writing), template position N+1 = rf-qa.md rule 4 (fix then verify), template position N+2 = rf-qa.md rule 9 (report honestly), template position N+3 = rf-qa.md rule 10 (max 2 fix cycles). Domain-specific rules (2 through N) are placeholders for per-agent customization. -->
## Critical Rules

1. **NEVER one-shot your output file** — Create the file immediately with a header (Write), then append findings incrementally section by section (Edit). Never accumulate the entire report in context and write it in one shot. One-shotting hits max token output limits and freezes the process. This is the #1 failure mode for all agents.

<!-- SPECIALIZATION: DOMAIN_RULES — Domain-specific critical rules. Number sequentially from 2. Examples from existing QA agents:
  - rf-qa: "Assume everything is wrong", "Evidence for every verdict", "Zero tolerance for fabrication", "Contradictions are critical", "Be specific about fixes", "Read EVERY file in scope", "You are the last line of defense"
  - rf-qa-qualitative: "Read the ENTIRE document", "Think like a stakeholder", "Evidence for every verdict", "Contradictions are always IMPORTANT or CRITICAL", "Be specific about fixes", "Scope is the #1 issue", "You complement rf-qa, not replace it"
  Add 5-8 domain-specific rules appropriate for this agent's verification focus. -->
[2-N. Domain-specific critical rules appropriate for this agent's QA focus]

N+1. **Fix then verify** — If authorized to fix, always verify the fix worked. A fix that doesn't verify = still failed.

N+2. **Report honestly** — A false PASS is worse than a false FAIL. When in doubt, fail it and explain why.

N+3. **Maximum 2 fix cycles** — After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. All blocking findings must be resolved; minor findings are recorded as notes.
`````

### src/superclaude/templates/documents/skill_template.md:820-834

`````markdown

<!-- VERBATIM — Research QA Verdict pattern -->
VERDICTS:
- PASS: Green light for synthesis
- FAIL: any blocking (Critical or Important) finding; every blocking finding must be resolved. Minor findings are notes: they never fail the gate and are not rechecked. Only PASS or FAIL — no conditional pass.
<!-- END VERBATIM — repo-cleanup uses "assembly" instead of "synthesis" in the PASS line -->

REVIEW SEVERITY RULE:
- Grade every review finding as blocking or minor. Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk. Minor is cosmetic, wording, formatting, citation format, a nit, style, or a moved line number on a true claim.
- Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. Minor findings are not rechecked in later rounds and never trigger a fix pass on their own. Only blocking findings produce FAIL.
- A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings.
- On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking and MINOR findings are minor; grade by the definition above, not by the label, so a finding labelled IMPORTANT that is only wording is minor.

Use the full QA report output format from your agent definition.
Zero tolerance — if you can't verify it, it fails.
`````

### src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:640-660

`````markdown
   See M3 for the complete 8-step lens-based QA sequence, I19 for minimum agent counts, and I20 for serialized fix authorization protocol.

I16. QA GATE VERDICT AND FIX CYCLES
   QA agents produce binary verdicts: PASS or FAIL.
   - Grade every review finding as blocking or minor. Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk. Minor is cosmetic, wording, formatting, citation format, a nit, style, or a moved line number on a true claim.
   - Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. Minor findings are not rechecked in later rounds and never trigger a fix pass on their own. Only blocking findings produce FAIL.
   - A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings.
   - On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking and MINOR findings are minor; grade by the definition above, not by the label, so a finding labelled IMPORTANT that is only wording is minor.

   Fix cycle rules per gate type:

   | Gate Type | Max Fix Cycles | After Max Reached |
   |-----------|---------------|-------------------|
   | research-gate | 2 | HALT and escalate to user |
   | synthesis-gate | 2 | HALT and escalate to the user with the open blocking findings; minor findings stay as notes |
   | report-validation | 2 | HALT and escalate to user |
   | task-integrity | 2 | HALT and escalate to the user with the open blocking findings; minor findings stay as notes |
   | Any qualitative gate | 2 | HALT and escalate to user |

   Each fix cycle MUST re-verify every previously failed blocking item plus check for new blocking issues introduced by fixes; minor findings are not rechecked. If the number of issues increases across cycles, flag this as a systemic problem.

`````

### src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:650-672

`````markdown

   Every QA gate step — each lens agent spawn, the consolidation, the fix agent, each verification agent — MUST be encoded as individual `- [ ]` checklist items in the task file. No QA is implicit. No QA lives only in prose.

I16. QA GATE VERDICT AND FIX CYCLES
   QA agents produce binary verdicts: PASS or FAIL.
   - Grade every review finding as blocking or minor. Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk. Minor is cosmetic, wording, formatting, citation format, a nit, style, or a moved line number on a true claim.
   - Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. Minor findings are not rechecked in later rounds and never trigger a fix pass on their own. Only blocking findings produce FAIL.
   - A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings.
   - On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking and MINOR findings are minor; grade by the definition above, not by the label, so a finding labelled IMPORTANT that is only wording is minor.

   **Multi-Agent Verdict Consolidation:** When multiple lens agents evaluate the same document (see M3), their individual reports are consolidated into a single findings list. The consolidated verdict is FAIL if any individual agent's report contains a blocking issue; minor issues from every agent are carried into the consolidated file as notes. The consolidated findings file lists all issues from all agents, deduplicated, with the originating lens agent identified for each issue.

   Fix cycle rules per gate type:

   | Gate Type | Max Fix Cycles | After Max Reached |
   |-----------|---------------|-------------------|
   | research-gate | 2 | HALT and escalate to user |
   | synthesis-gate | 2 | HALT and escalate to the user with the open blocking findings; minor findings stay as notes |
   | report-validation | 2 | HALT and escalate to user |
   | task-integrity | 2 | HALT and escalate to the user with the open blocking findings; minor findings stay as notes |
   | Any qualitative gate | 2 | HALT and escalate to user |
   | source-fidelity | 2 | HALT and escalate to user |

`````

### src/superclaude/agents/rf-qa-qualitative.md:984-996

`````markdown

1. **NEVER one-shot your output file** — Create the file immediately with a header (Write), then append findings incrementally section by section (Edit). Never accumulate the entire report in context and write it in one shot. One-shotting hits max token output limits and freezes the process. This is the #1 failure mode for all agents.
2. **Read the ENTIRE document** — Do not skim. Qualitative issues hide in the details. Read every section, every table row, every acceptance criterion.
3. **Think like a stakeholder** — Would a PM approve this? Would an engineer be able to build from this? Would a VP present this to investors? If any answer is "no," that's a finding.
4. **Evidence for every verdict** — Never say "this seems fine" without explaining what you checked. Never say "this is wrong" without explaining what it should be.
5. **Fix then verify** — If authorized to fix, always verify the fix worked. A fix that doesn't verify = still failed.
6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.
7. **Be specific about fixes** — "This section needs work" is useless. "S5.1 contains a KPI table with 11 metrics that duplicates S19 — replace with business justification prose and a forward reference to S19" is useful.
8. **Scope is the #1 issue** — The most common qualitative failure is content at the wrong scope level (platform content in feature PRDs, feature content in platform PRDs). Check this first and thoroughly.
9. **Report honestly** — A false PASS that lets a bad PRD reach stakeholders is worse than a false FAIL that triggers one more review cycle. When in doubt, fail it and explain why.
10. **Maximum 2 fix cycles** — After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. All blocking findings must be resolved; minor findings are recorded as notes.
11. **You complement rf-qa, not replace it** — rf-qa checks structural correctness (section
    numbers, cross-references, evidence citations, template conformance, the TB-Add-*
`````

### tests/audit/test_severity_floor_unweakened.py:1-75

`````python
"""TEST-014 — Severity-floor / Critical Rules block preservation (R-087 / FR-CONV.4 PR-07).

Phase-4 / T04.14 deliverable (D-0052). Asserts that the severity-floor /
Critical Rules block at rf-qa-qualitative.md is byte-identical to the
pre-M4 baseline at commit ``3a57a0d`` (the last commit on this branch
before PR-07 axis-overlay landed). Two equality proofs are checked:

1. The strict ``:786-795`` spec range (pre-M4) maps to ``:831-840``
   (post-M4) with SHA-256
   ``770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7``.
2. The entire Critical Rules block (``## Critical Rules`` header + Rules
   #1..#11) has SHA-256
   ``be18e2cf2194b3232c83c77ee6d08c30ad707d10304ff592e5d7e78872e46b1b``
   (re-pinned 2026-05-24 after markdownlint MD013 reflow in
   TASK-RF-20260523-234320-markdownlint-remediation, and 2026-11-02 after
   the review severity rule rewrote Rule #10).

Rule #6 — "Contradictions are always IMPORTANT or CRITICAL" — must
appear verbatim with no softening verbs.

Acceptance reference (phase-4-tasklist.md T04.14 AC):
- ``uv run pytest tests/audit/test_severity_floor_unweakened.py -v`` exits 0.
- TEST-014 asserts byte-diff of Critical Rules block is zero.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0052/evidence.md``.

Run: ``uv run pytest tests/audit/test_severity_floor_unweakened.py -v``
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

AGENT_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
AGENT_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa-qualitative.md"

# Baselines captured in D-0049 evidence (pre-M4 commit 3a57a0d).
BASELINE_SLICE_SHA = "770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7"
# Updated 2026-05-24: re-pinned to post-reflow content following the
# authorized markdownlint MD013 remediation in
# TASK-RF-20260523-234320-markdownlint-remediation. The Critical Rules
# block was reflowed (no semantic content change); recompute reflects
# the new byte sequence of the same logical block.
# Re-pinned 2026-11-02 (review severity rule, fix/review-severity-rule):
# rule 10 now reads "Maximum 2 fix cycles ... with the open blocking
# findings. All blocking findings must be resolved; minor findings are
# recorded as notes." (cap-edits.yaml row C-003). Rules 1-9 and 11,
# including Rule 6, are unchanged.
BASELINE_BLOCK_SHA = "be18e2cf2194b3232c83c77ee6d08c30ad707d10304ff592e5d7e78872e46b1b"  # pragma: allowlist secret

# Rule #6 verbatim text (the explicit severity floor).
RULE_6_TEXT = (
    "**Contradictions are always IMPORTANT or CRITICAL** — If two sections "
    "say different things about the same topic, that's never minor. Always "
    "surface contradictions."
)

CRITICAL_RULES_HEADER = "## Critical Rules"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _slice_lines(path: Path, start: int, end_inclusive: int) -> str:
    """Return the substring of ``path`` covering 1-based lines [start, end_inclusive].

    Preserves the trailing newline of the last line if present in source, matching
    the byte semantics of ``sed -n 'A,Bp'``.
    """
`````

### Makefile:105-125

`````text
	@echo "✅ Translation complete!"
	@echo "📝 Files updated: README-zh.md, README-ja.md"

# Sync src/superclaude/{skills,agents} → .claude/{skills,agents} for local dev
sync-dev:
	@echo "🔄 Syncing src/superclaude/ → .claude/ for local development..."
	@mkdir -p .claude/skills .claude/agents
	@for skill_dir in src/superclaude/skills/*/; do \
		skill_name=$$(basename "$$skill_dir"); \
		case "$$skill_name" in __*) continue;; esac; \
		if [ -f "$$skill_dir/SKILL.md" ] || [ -f "$$skill_dir/skill.md" ]; then \
			mkdir -p ".claude/skills/$$skill_name"; \
			find "$$skill_dir" -type f ! -name '__init__.py' ! -path '*/__pycache__/*' -exec sh -c ' \
				src="$$1"; skill_dir="$$2"; target_base="$$3"; \
				rel=$${src#$$skill_dir}; \
				target_dir="$$target_base/$$(dirname "$$rel")"; \
				mkdir -p "$$target_dir"; \
				cp "$$src" "$$target_dir/" \
			' _ {} "$$skill_dir" ".claude/skills/$$skill_name" \; ; \
		fi; \
	done
`````

### Makefile:160-185

`````text
	@echo "   Agents:    $$(ls .claude/agents/*.md 2>/dev/null | wc -l | tr -d ' ') files"
	@echo "   Commands:  $$(ls .claude/commands/sc/*.md 2>/dev/null | wc -l | tr -d ' ') files"
	@echo "   Hooks:     $$(ls .claude/hooks/*.sh 2>/dev/null | wc -l | tr -d ' ') files"
	@echo "   Templates: $$(find .claude/templates -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ') files"

# Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)
verify-sync:
	@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."
	@drift=0; \
	echo ""; \
	echo "=== Skills ==="; \
	for skill_dir in src/superclaude/skills/*/; do \
		name=$$(basename "$$skill_dir"); \
		case "$$name" in __*) continue;; esac; \
		if [ ! -d ".claude/skills/$$name" ]; then \
			echo "  ❌ MISSING in .claude/skills/: $$name"; \
			drift=1; \
		else \
			changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
			if [ -n "$$changes" ]; then \
				echo "  ⚠️  DIFFERS: $$name"; \
				echo "$$changes" | sed 's/^/      /'; \
				drift=1; \
			else \
				echo "  ✅ $$name"; \
			fi; \
`````

### tests/skills/test_review_prompt_overrides.py:255-283

`````python

@pytest.mark.parametrize(
    "rel",
    [
        "src/superclaude/agents/rf-qa.md",
        "src/superclaude/agents/rf-qa-qualitative.md",
        "src/superclaude/templates/documents/agent_template_qa.md",
    ],
)
def test_qa_agents_use_the_independent_stance(rel):
    flat = _flat((_REPO / rel).read_text(encoding="utf-8"))
    assert "**Independent stance**" in flat, rel
    assert "there is no minimum count" in flat, rel
    assert "do not invent findings to avoid a zero" in flat, rel


@pytest.mark.parametrize(
    "rel",
    [
        "src/superclaude/skills/task/SKILL.md",
        "src/superclaude/skills/tech-reference/SKILL.md",
        "src/superclaude/skills/tech-research/SKILL.md",
        "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md",
        "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md",
    ],
)
def test_lens_prompts_state_no_minimum_count(rel):
    flat = _flat((_REPO / rel).read_text(encoding="utf-8"))
    assert "no minimum count" in flat, rel
`````


## Coverage slice

| Requirement | Card ID | Status | Grounding |
|-------------|---------|--------|-----------|
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
| INF-025: The old Task 4 (consumer line in `task-builder/SKILL.md` and the two MDTM templates) is dropped, and `rf-task- | T1 card | covered (containment 0.640 -> Task 1) | source.md:40 |
| INF-027: No mirror folder, parity test, plugin registry row or plugin reverse scan. Plugin twins are edited only where  | T1 card | covered (containment 0.615 -> Task 4) | source.md:42 |
