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
Goal: Move the remaining templates, rule prompts, builder and researcher skills and the spec-panel to the new rule, mirror the skill folder into the plugin, switch the drift scan to strict, and give the owner the final summary.

## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 4 of five packages and the last (one plan per stage). It runs only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (spec section 13.2), the owner has read the stage 3 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Strict T2 is switched on here.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.

## Phase 1: Move the templates

## Task 1: Move the templates to digest v2

Edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (the definition bullet near line 161, the merge rule near line 85, the Rule 6 text near line 333 per OD16, and the FAIL-by-label bullet "Any CRITICAL or IMPORTANT issue exists" near line 158, rewritten or kept as a named mechanical gate recorded in `refs/scale-map.md`), `documents/agent_template_analysis.md` (the merge rule near line 466), `documents/skill_template.md` (the definition near line 828), `workflow/01_mdtm_template_generic_task.md` (near line 644) and `workflow/02_mdtm_template_complex_task.md` (near line 655). Each of the four digest templates (`agent_template_qa.md`, `skill_template.md` and the two MDTM templates) gets the digest and pointer in place of the definition bullets and the L1 merge text and its registry row is set to `v2`; `agent_template_analysis.md` gets the L1 merge text only (no digest, no fence, no registry row); remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of the stage 3 scan test. Task files already generated from the old templates keep the old text and are not migrated.

Acceptance criteria:
- The stage ledger `stage-requests/README.md` in PF has an owner go for stage 4 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
- The stage 3 package's `./artifacts/stage3-summary-for-owner.md` (read by package id) exists and states that one audit window has passed with no revert trigger tripped.
- Each of the four digest template files holds exactly one digest; `agent_template_analysis.md` holds no digest and no `more severe rating` text.
- The registry rows of the four digest templates say `v2`, T1 passes for them and the registry still has exactly 11 `digest` rows.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude/templates` prints nothing, and `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/templates/documents/agent_template_qa.md` prints 0 or the remaining line is listed in `refs/scale-map.md`.
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the two templates removed from its allow-list.


## Phase 2: Move the rule prompts, builders, researchers and the consumer line

## Task 2: Move the rule prompts to digest v2 and set the two pointer-only rows

Depends on: Task 1

Edit the digest carriers in `src/superclaude/rules/prompts/`: `automated_qa_workflow_qa_prompt.md` (near line 11), `doc_code_analyst_qa_prompt.md` (near line 27), `documentation_expert_qa_prompt.md` (near line 28) and `recruiting_expert_qa_prompt.md` (near line 27); update those four registry rows to `v2`. Edit `document_review_loop_prompts.md` (the Medium wording near lines 31, 32 and 48 becomes the pointer and the ledger sentence inside an existing section; its structure and the `"src/superclaude" not in TEXT` assertion of `tests/review/test_review_rules_text.py` must still hold): its registry row is of kind `pointer-only` and stays so; it is checked by T3 and never by T1.

Acceptance criteria:
- Each of the four rule prompts holds exactly one digest and its registry row says `v2`.
- `document_review_loop_prompts.md` holds the pointer and the ledger sentence and no digest, and its registry row stays `pointer-only`.
- `uv run pytest tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_registry.py -v` passes and the zero-finding and "no minimum count" sentences still exist.

## Task 3: Replace the merge rule in the builder and researcher skills

Edit the stage 4 merge-rule lines of spec section 10.3: `src/superclaude/skills/tech-reference/SKILL.md` (two lines near 510 and 513), `src/superclaude/skills/readme/SKILL.md` (two lines near 542 and 547), `src/superclaude/skills/tdd/refs/build-request-template.md` (near line 122) and `src/superclaude/skills/operational-guide/SKILL.md` (near line 511), each to the L1 text; and remove those four files from the allow-list of the stage 3 scan test in the same change.

Acceptance criteria:
- `grep -rniE "highest severity|more severe rating|higher severity" src/superclaude/skills/tech-reference src/superclaude/skills/readme src/superclaude/skills/tdd src/superclaude/skills/operational-guide` prints nothing.
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the four skills removed from its allow-list.
- The cap text in each of the four files is unchanged (each file still contains its "After 2 fix cycles" sentence).

## Task 4: Add the consumer line to the task builder and MDTM templates

Depends on: Task 1

Edit `src/superclaude/skills/task-builder/SKILL.md` and the MDTM templates `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` so the task builder writes a consumer line for each phase output ("feeds item X, reads column Y"), which gives upstream gates a declared consumer list (L4, spec section 4.3 option A for upstream outputs only). Keep the cap sentence in `src/superclaude/skills/task-builder/SKILL.md` ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", one occurrence today) unchanged; `src/superclaude/agents/rf-task-builder.md` holds no such sentence and is not edited.

Acceptance criteria:
- Both MDTM templates and the task-builder skill contain the consumer-line instruction.
- `uv run pytest tests/skills/test_task_builder_merge.py -v` passes.
- The cap sentence is still present in `src/superclaude/skills/task-builder/SKILL.md` (`grep -c` prints 1), and `git diff --stat` shows no edit to `src/superclaude/agents/rf-task-builder.md`.


## Phase 3: Narrow spec-panel and update its twins

## Task 5: Narrow spec-panel and update the plugin twins

Depends on: Task 2

Edit `src/superclaude/commands/spec-panel.md`: the Review Loop bullets (the Grading and Cap bullets near lines 259 to 261) and the always-CRITICAL dimensional-mismatch sentence ("Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity", near line 372) are narrowed to the three conditions (CRITICAL stays blocking, a MAJOR stays blocking only when it names a concrete wrong outcome), its `follow-up candidates` list becomes the follow-up ledger, and the Unattended mode section gains one line for the ledger and the three contract keys. Apply the same edits to the hand-kept twins `plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`; the `spec-panel` source and plugin copies differ today, so edit each file in place and do not copy one over the other. The `commands/sc/spec-panel.md` registry row stays `pointer-only`.

Acceptance criteria:
- The existing `src/superclaude/examples/...` mention in `src/superclaude/commands/spec-panel.md` and its twins is left as it is (T3 does not check `pointer-only` rows for that path).
- `uv run pytest tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py -v` passes and the cap sentence `at most 2 fix cycles (3 reviews)` is still in `src/superclaude/commands/spec-panel.md`.
- `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` prints nothing and the ledger is named instead.
- The plugin twins carry the same pointer and ledger sentence as their source twins, and a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`.


## Phase 4: Mirror the skill folder into the plugin and write the summary

## Task 6: Mirror the skill folder into the plugin and make the drift scan strict

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5

Work in this order, because the registry and the allow-list must be correct before the copy. First add the plugin mirror of `refs/rule.md` (`plugins/superclaude/skills/sc-review-severity/refs/rule.md`) as a `canonical` row in `src/superclaude/skills/sc-review-severity/refs/registry.yaml` and as a path in the "Merge-rule allow-list" section of `refs/scale-map.md` (by path only; no merge-rule phrase is written there). Then copy `src/superclaude/skills/sc-review-severity/` to `plugins/superclaude/skills/sc-review-severity/` by hand (the plugin's `skills/` is hand-kept and holds 4 entries today). Then add `tests/skills/test_review_severity_plugin_parity.py` for T15 (the mirror equals the source), set every `digest` row to `v2` where its file now holds the digest (and repeat the copy if the registry changed), and switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode so any legacy definition sentence left in `src/` or `plugins/` fails. Run `make sync-dev` and `make verify-sync`, then the three tests together.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passes with strict T2, and the plugin mirror of `refs/rule.md` is accepted by the reverse scan through its `canonical` row and by the merge-rule scan through the allow-list.
- `make verify-sync` passes.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` prints nothing; the five installed-only spec-panel variants are outside the scan and stay listed `installed-only`.
- No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`.

## Task 7: Write the stage 4 summary for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final results of the merge-rule scan, the plugin parity test and the strict registry test with their observed pass counts, and the revert command per row (the spec's three-step revert). State that a second audit window is observed by the owner or operator and is not a task of this package, and list the open items.

Acceptance criteria:
- `./artifacts/stage4-summary-for-owner.md` lists every carrier row with its state (`v2` or the stated exception) and the test that pins it, and each named test file exists.
- The summary shows the observed pass counts of the scan, parity and strict registry tests and the `make verify-sync` result.
- The summary states the revert command per row and that the second audit window is not a task of this package.
