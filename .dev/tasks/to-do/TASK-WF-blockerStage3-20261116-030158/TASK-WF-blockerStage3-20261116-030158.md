---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-blockerStage3-20261116-030158
version: "1"
priority: Medium
created_date: "2026-11-16"
---

# Stage 3 plan: pilot the new rule for the blocker classification work (issue #552)

Source: ./source.md
Goal: Run the seeded-defect recall test under the old and the new rule text, then move `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md` and the task skill's consolidation text to the new rule, re-pin the tests that guard them, and give the owner the audit-window numbers before the stage 4 go.

## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 3 of five packages (one plan per stage). It changes the live review rule. It runs only when all of these hold, each checked by reading files and not by memory (Task 1 checks them): the owner's go for stage 3 is recorded in the stage ledger; the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and states at least 5 observed shadow runs with zero safety misses (by the definition the stage 0 spec edit drafted) and no capture failure; the stage 0 package's `stage0b-escape-test.md` and `stage0c-regrade.md` exist. `/sc:implement` runs this whole package in order, so the rule switch cannot start unless Task 1's checks and the seeded-recall result pass. Stage 4 starts only after one audit window with no revert trigger tripped (spec section 13.2) and the owner's go in chat.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.

## Phase 1: Produce the evidence before the switch

## Task 1: Run the seeded-defect recall set under the old and the new rule text

Run the seeded-defect set built by the stage 0 package (its `./artifacts/seeded-recall-set.md` and the planted deliverable under its `./artifacts/seeded/`, read by package id) as spec section 8.3 says. Spawn three reviewer agents for each pass (old rule text, new rule text) as freshly spawned agents, never agents continued from an earlier pass, and alternate the pass order across the three reviewers on the planted deliverable, once with today's rule text (the definition bullets and the Medium bullet of `src/superclaude/output-styles/pragmatic.md`) and once with the digest of spec section 4.1, never showing them the answer key. Score each planted defect as found or missed and as blocking or not, per class. Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts, the share of cosmetic defects that block under each, the Wilson 95 percent intervals, and a pass or fail line for each of the three requirements named in the stage 0 package's `seeded-recall-set.md` (safety recall equals the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the cosmetic block share falls). This task reports the result; the owner decides whether stage 3 may proceed.

Acceptance criteria:
- The stage ledger `stage-requests/README.md` in PF has an owner go for stage 3 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
- The stage 2 package's `./artifacts/stage2-summary-for-owner.md` (read by package id) states at least 5 observed shadow runs with zero safety misses and no capture failure.
- The stage 0 package's `./artifacts/stage0b-escape-test.md` and `./artifacts/stage0c-regrade.md` exist.
- `./artifacts/seeded-recall-result.md` holds per-class recall under both rule texts with intervals, the cosmetic block share under both, and a pass or fail line for each of the three requirements.
- The reviewer agent ids are recorded and the answer key is not among the files they were given.
- The file states that the result is evidence for the owner's go and does not itself grant it.

## Task 2: Build the post-fix mechanical-check helper

Create `src/superclaude/cli/review/fixcheck.py` for L2: over the lines a fix pass edited it runs every mechanical check that exists (table pipe count per row, byte-present quotes, recomputed counts, link existence) and returns results for the fix log; a defect that a verifier finds that the fix introduced carries `origin: fix-induced`. Add `tests/review/test_review_fixcheck.py` with the run-2 case (an unescaped pipe in a backticked command gives 8 pipes in a 7-cell row).

Acceptance criteria:
- `uv run pytest tests/review/test_review_fixcheck.py -v` passes and the run-2 pipe case is detected.
- The helper reports a result for every check it ran, including passes, so the fix log is complete.
- It edits no file (read-only over its inputs).


## Phase 2: Move the three QA carriers and rf-analyst

## Task 3: Move pragmatic.md to digest v2

Depends on: Task 1, Task 2

Edit `src/superclaude/output-styles/pragmatic.md`: replace the three definition bullets (the one that begins "Grade every review finding as blocking or minor", the one that begins "Minor findings never fail a review", and the one that begins "On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking", today lines 225, 226 and 229) with the digest of REQ-01 inside its fence plus the pointer line naming `~/.claude/skills/sc-review-severity/refs/rule.md` first and `.claude/skills/sc-review-severity/refs/rule.md` second. The cap bullet and the own-model bullet ("A protocol that defines its own severity model, such as `/sc:implement`") stay word for word (the cap sentence is also the last sentence of the digest). Move the Medium and spec-panel bullets into the full rule and scale map, and change the reviewer brief bullet ("Every review agent MUST review as an independent reader") so reviewers hunt for defects and name their consequence instead of hunting for "false claims" (REQ-04). Set the registry row of `output-styles/pragmatic.md` to `v2`. Run `make sync-dev` and then the existing tests that Task 8 re-pins.

Acceptance criteria:
- `./artifacts/seeded-recall-result.md` exists and shows pass on all three requirements (safety recall equal to the old rule's; recall of decision-bearing and missing items within 5 points of the old rule's; the cosmetic block share falls); when a line shows fail, this check fails and the run halts for the owner's Ruling. This task does not rely on `Depends on` for the gate.
- `src/superclaude/output-styles/pragmatic.md` holds exactly one fenced digest equal to the digest section of the skill's `refs/rule.md` and its registry row says `v2`.
- The cap sentence ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings") and the own-model bullet still appear word for word (`grep -c` of each sentence prints 1 or more).
- The hook `pragmatic-subagent.js` still finds and injects the file: `grep -n "pragmatic" src/superclaude/hooks/hooks.json` still matches and `src/superclaude/output-styles/pragmatic.md` exists.
- The new pointer line names `~/.claude/skills/sc-review-severity/refs/rule.md` before the `.claude/` copy and contains no `src/superclaude` path.
- `uv run pytest tests/skills/test_review_brief_rests_on.py -v` passes (its legacy assertion is skipped now that the row is `v2`).

## Task 4: Move rf-qa.md to digest v2 and rewrite its fixed FAIL triggers

Depends on: Task 3

Edit `src/superclaude/agents/rf-qa.md`: replace S1, S2 and S5 (the definition bullet and the bullets beside it, today around line 108) with the digest and pointer; replace the merge rule ("take the more severe rating for shared items", today line 83) with the L1 text (the consolidator grades by the rule, keeps every reviewer's grade visible, and sends a blocking grade that names no consumer back once); add the L2 pre-handback checks to the Fix Cycle section; at each of its two cap sentences ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", today in the Fix Cycle bullet near line 402 and in numbered rule 10 "Maximum 2 fix cycles" near line 549) add the L3 three choices (fix by hand, accept and file as an `accepted-blocker` follow-up, or stop) and the one-offer sentence naming the task skill's end-of-run offer; and for each fixed FAIL trigger listed in `./artifacts/stage0-inventory-freeze.md` for this file (spec section 10.4: "Any incomplete file = FAIL", "Any untagged doc claim = FAIL", the "Will this gap reduce report quality? -> IMPORTANT" and "Any CRITICAL or IMPORTANT gap = overall FAIL" bullets, the PASS and FAIL bullets by label near lines 182 to 183, "Flag exact duplicates as IMPORTANT", and the count-CRITICAL-and-IMPORTANT-as-blocking lines) either rewrite it to "grade by the three conditions; the label is information" or keep it as a named mechanical gate mapped to condition 2 (Missing) and record the keep in `refs/scale-map.md`; "Flag exact duplicates as IMPORTANT" becomes Note unless a condition holds. Set the registry row to `v2`.

Acceptance criteria:
- `grep -n "more severe rating" src/superclaude/agents/rf-qa.md` prints nothing.
- Every FAIL-trigger line in the frozen inventory for `rf-qa.md` is either changed or listed as a kept mechanical gate in `refs/scale-map.md` with a reason.
- The PASS and FAIL bullets are reworded to "any blocking gap" and the file holds exactly one digest.
- The L2 fix-cycle checks are present in the Fix Cycle section, and the L3 three choices with the one-offer sentence sit beside each of the two places the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" appears (`grep -c` of that sentence still prints 2).

## Task 5: Move rf-qa-qualitative.md to digest v2, rewrite its eight FAIL-by-label pairs and apply OD16

Depends on: Task 3

Edit `src/superclaude/agents/rf-qa-qualitative.md`: replace S1, S2 and S5 (today around line 108) with the digest and pointer; replace the merge rule (today line 84); rewrite or keep as named mechanical gates, recorded in `refs/scale-map.md`, the eight verdict pairs that fail a review on "Any CRITICAL or IMPORTANT issue exists" (the FAIL bullet today at lines 240, 291, 362, 429, 500, 567, 746 and 784, each with its PASS bullet one line above; the list is in `./artifacts/stage0-inventory-freeze.md`); and rewrite Rule 6 ("Contradictions are always IMPORTANT or CRITICAL ... that's never minor", today line 990) per OD16 option (b), so a contradiction nothing rests on is a follow-up, and keep contradictions that touch a decision basis, a quoted number or a required deliverable as Blocking under condition 1. Update the registry row to `v2`.

Acceptance criteria:
- `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/agents/rf-qa-qualitative.md` prints 0, or each remaining line is listed in `refs/scale-map.md` with its reason.
- `grep -n "that's never minor" src/superclaude/agents/rf-qa-qualitative.md` prints nothing, and the new Rule 6 text names the decision-basis exception.
- The file holds exactly one digest and no `more severe rating` text.
- `tests/audit/test_severity_floor_unweakened.py` is updated in Task 9 in the same change set; the file's `## Critical Rules` block hash is re-pinned there.

## Task 6: Replace the merge rule in rf-analyst.md

Depends on: Task 3

Edit `src/superclaude/agents/rf-analyst.md`, the line that reads "union of findings, take the more severe rating for shared items, merge gap compila...", to the L1 text: union the findings, keep each reviewer's own grade visible, and let the consolidator grade by the rule; keep the rest of the line (the gap compilation) unchanged.

Acceptance criteria:
- `grep -n "more severe rating" src/superclaude/agents/rf-analyst.md` prints nothing.
- The gap-compilation words that followed on the line are still present.


## Phase 3: Switch the task skill, re-pin the tests and add the scan test

## Task 7: Switch the task skill's consolidation, fix and escalation text and turn the sweep on

Depends on: Task 2, Task 3

Edit `src/superclaude/skills/task/SKILL.md`: the Findings Consolidation step and the Follow-Up Items consolidation sentence replace "Preserve the highest severity rating when duplicates disagree" with the L1 text and keep the ledger writing of the stage 2 package; the Fix Agent step requires the L2 mechanical checks before handing back and the `origin: fix-induced` tag; the Conditional Proceed step counts Blocking findings only and, at each cap sentence ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", today at the Conditional Proceed step, the Escalation item and the Fidelity Verification step), offers three choices (fix by hand, accept and file as an `accepted-blocker` follow-up, or stop) without changing the cap of 2 fix cycles (L3); and the sweep call of the stage 2 package is switched to `promote` on, so a swept Medium row becomes Blocking at the last gate. The skill gets no registry row (it is not a digest carrier).

Acceptance criteria:
- `grep -n "highest severity" src/superclaude/skills/task/SKILL.md` prints nothing.
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" is still present at each place it appears today, each with the three choices and the statement that the cap is unchanged.
- The sweep call in "Post-Completion Validation (Final Phase Only)" states `promote` on.
- `grep -n "sc-review-severity" src/superclaude/skills/sc-review-severity/refs/registry.yaml` shows no row for `skills/task/SKILL.md`.

## Task 8: Re-pin the severity tests in tests/skills

Depends on: Task 3, Task 4, Task 5, Task 7

Update `tests/skills/test_review_severity_rule.py` (`canonical_rule_bullets()` reads the digest from `refs/rule.md`; `S1_S3_FILES` and its `[:6]` slice `S5_FILES` become registry rows of kind `digest`; the cap-text and banned-phrase checks stay, and the cap text constant `CANONICAL_CAP_TEXT` stays asserted against the output style only, as today), `tests/skills/test_review_severity_mapping.py` (the Medium and cadence pins move from "once per loop" to the once-per-run wording and to assertions on `refs/rule.md` and `refs/scale-map.md`), `tests/skills/test_implement_severity_static.py` (S4 kept word for word; the S2 assertion moves to the digest; the `qa.md` pins stay), the fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` (update only the approved changed strings) and the two plan tables the fixtures must be byte copies of, `.dev/review-severity-rule/cap-edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml` (the test `test_ej_fixtures_are_byte_copies_of_the_plan_tables` in `tests/skills/test_review_severity_rule.py` compares them; edit each pair in the same change, or record which relaxation of that test is chosen and why). `tests/skills/test_review_loop_extension.py`, `test_review_prompt_overrides.py` and `test_spec_panel_review_loop.py` must still pass unchanged. Also add `tests/skills/test_review_brief_rests_on.py` of the stage 2 package to the list of tests re-run, because its legacy assertion is skipped once the pragmatic row is `v2`.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_implement_severity_static.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_brief_rests_on.py -v` passes, including `test_ej_fixtures_are_byte_copies_of_the_plan_tables`.
- The two fixtures change only rows whose new text is the digest or the once-per-run cadence; the diff of each fixture and of each plan table is listed in `./artifacts/t38-fixture-diff.md`.
- No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text.

## Task 9: Re-pin the audit tests for the QA agents

Depends on: Task 4, Task 5

Update `tests/audit/test_nfr_conv_9_zero_trust.py` (byte-exact PASS and FAIL bullets of `src/superclaude/agents/rf-qa.md` and its `.claude/` mirror) to the reworded "any blocking gap" bullets on both surfaces; update `tests/audit/test_invariant_preservation_NFR_6_through_10.py` (it imports `FAIL_BULLET` and `PASS_BULLET` from the first module) in the same change; re-pin `tests/audit/test_severity_floor_unweakened.py` (the SHA-256 of the `## Critical Rules` block of `rf-qa-qualitative.md` and its mirror, and Rule 6 verbatim) to the Task 5 text, including the rewritten verdict pairs; leave `tests/audit/test_dnsp_all_agents_fail_bypass.py` unchanged unless the cap text moved.

Acceptance criteria:
- `uv run pytest tests/audit -v` passes.
- The re-pinned hash in `test_severity_floor_unweakened.py` matches the new `## Critical Rules` block on both the source and the mirror surface after `make sync-dev`.
- `test_dnsp_all_agents_fail_bypass.py` passes without an edit.

## Task 10: Add the merge-rule reverse-scan test

Depends on: Task 4, Task 5, Task 6, Task 7

Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude`, matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`: `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, `src/superclaude/skills/sc-review-severity/refs/rule.md`, and, until the stage 4 package, the six stage 4 files (`src/superclaude/skills/tech-reference/SKILL.md`, `src/superclaude/skills/readme/SKILL.md`, `src/superclaude/skills/tdd/refs/build-request-template.md`, `src/superclaude/skills/operational-guide/SKILL.md`, `src/superclaude/templates/documents/agent_template_qa.md` and `src/superclaude/templates/documents/agent_template_analysis.md`). The stage 4 package removes each of those files from the allow-list in the same change that edits it, and adds the plugin mirror of `refs/rule.md` to the allow-list and the registry before it copies the skill folder; the plugin mirror is NOT in the allow-list here.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 34 to 37, with no hit in `src/superclaude/cli/` counted.
- A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
- The allow-list is read from `refs/scale-map.md` and a test fails when a file named there does not exist.


## Phase 4: Write the audit summary for the owner

## Task 11: Write the stage 3 audit summary for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10

Write `./artifacts/stage3-summary-for-owner.md`: the seeded-recall result headline from Task 1, the re-pinned test results, and the audit-window measures the spec's section 13 defines for stage 3 (read the metric list in section 13.1 including M12, the rf-qa FAIL count per pilot gate, and the revert triggers RT1 and RT2 in section 13.2 with their current state; quote their text from the spec and do not restate it from memory). State that the audit window runs after this package and is observed by the owner or operator, name which runs and gates it covers, and end with the sentence that the owner's go for stage 4 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/stage3-summary-for-owner.md` names the seeded-recall headline and the file that holds it, lists the tests re-pinned with their observed pass counts, and quotes RT1, RT2 and M12 from the spec.
- The summary states the revert command per carrier row (the spec's three-step revert) and that no revert trigger can be judged until the audit window has run.
- The summary ends with the sentence that the owner's go for stage 4 is given in chat and not by this file.
