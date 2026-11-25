---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-issueSummary-20261125-175321
version: "1"
priority: Medium
created_date: "2026-11-25"
---

# Make /sc:issue --create ask only about contradictions of the user's own words (issue 834)

Source: ./source.md
Goal: A `/sc:issue --create` run posts with no question when the drafter only added material (assumptions included), and asks exactly one combined question, resolved before posting, only when the draft contradicts the user's own description, instruction or flag. Every unrelated addition stays in the issue body, in `draft-notes.md` and in the final output.

## Constraints

- Base branch is `integration` (the issue text says `master`; that is stale). Edit only canonical sources under `src/superclaude/`, `docs/` and `tests/`. The generated project mirrors under `.claude/` are refreshed only by `make sync-dev`, never edited by hand.
- Keep `AskUserQuestion` in the `allowed-tools` line of `src/superclaude/skills/sc-issue-protocol/SKILL.md` (pinned by `ALLOWED_TOOLS` in `tests/skills/test_issue_protocol.py:40`).
- Keep the full issue body never shown for approval (default B1), the post-create flag pushback comment (create Wave 5, `templates/create-review-comment.md`), the three required plan sections and their one shared rule sentence (`PLAN_SECTIONS_RULE`, `tests/skills/test_issue_worker_agents.py:34-39`), claim assignment, ClickUp, Orca, watcher and launch safeguards, the stage-claim recommendation skip from pull request 833, and the launched `worktree` agent's plan-approval boundary. None of these text blocks may change in meaning.
- Lines of `src/superclaude/skills/sc-issue-protocol/refs/create.md` that `tests/skills/test_worker_contract.py` pins verbatim (the GitHub-write rule paragraph near line 9, the lookup paragraph near line 20 and step 6 of Wave 5 near line 95) must stay byte-identical. SKILL.md step 6 of create mode (line 103) is also pinned there; Task 4 updates that pinned copy together with the line.
- Do not add a new return-contract field, flag, script, agent or dependency. The classification is instruction text plus tests, as the current rule is.
- A contradiction counts only with all three parts: its category, the user's own words (a quote from `description.md` or a flag passed on the command line), and the conflicting evidence (draft text, or a verified `path:line` of code the worker read). `None` is the empty marker, never an item.
- A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag; it stays a pushback comment.

## Phase 1: Define the contradiction-only rule in the shared sources

## Task 1: Rewrite the create decision rule in the create reference

Edit `src/superclaude/skills/sc-issue-protocol/refs/create.md` (source requirement: additions never ask; one combined question only for a supported contradiction; retained additions disclosed). Change four places and nothing else:

- Wave 4 text at line 57 (the sentence that says the worker lists new material and any contradiction in `draft-notes.md`): state that new material is kept without any question, and that a contradiction is one of exactly four categories: reversed choice (the draft reverses a choice the user stated), dropped requirement (the draft omits a requirement the user stated), changed flag (the draft would not honor `--mode`, `--type` or `--depth` as given), and user-stated fact contradicted by verified code (the worker read the code and the user's stated fact is false). Say that each contradiction line carries the category, the user's own words and the conflicting evidence, and that a line without all three is recorded as new material.
- Line 69 (the "Assumption:" paragraph): keep "one line per assumption, starting with Assumption:" under "New material", and replace "so the contradiction prompt rule below applies to it" with a statement that assumptions are kept and never cause a question. Leave line 63 (the `PLAN_SECTIONS_RULE` sentence) byte-identical.
- The "Contradiction prompt rule (default D14)" section at lines 82-84: keep the heading text. Replace the body with the decision: no contradiction items (empty list or only `None`) means zero questions and Wave 5 posts; one or more supported contradiction items means exactly one `AskUserQuestion`, naming every item, asked once per run, whose choices are "keep my wording" (change the draft to honor the user's words), "keep the draft" (accept the draft's change) and "edit"; the answer is applied to `<D>/issue-body.md` before Wave 5 and changes only the contradicted items; every New material item stays in the body and in `draft-notes.md` whatever the answer; the full body is still never shown for approval (B1); worker disagreement with a supplied flag is not a contradiction when the issue is filed with the user's flag (point to the Wave 2 sentence "The issue is filed with the user's flags when the user gave them" at line 38 and to Wave 5 step 7 at line 96).
- Wave 5 step 8 at line 97 (the print step): add that the final output also lists every retained addition, one line each, in the form `kept without approval: <item>`, and states whether a contradiction question was asked and how it was answered. Keep every existing clause of that step, including "Do not stage or commit `.dev/issues/` (default D24)".

Acceptance criteria:
- `grep -n "lists new material" src/superclaude/skills/sc-issue-protocol/refs/create.md` prints nothing, and `grep -n "keep all" src/superclaude/skills/sc-issue-protocol/refs/create.md` prints nothing.
- The file names all four categories (reversed choice, dropped requirement, changed flag, user-stated fact contradicted by verified code), the words "exactly one" question, the `None` rule, the unsupported-item-becomes-new-material rule and the flag-disagreement carve-out.
- `PLAN_SECTIONS_RULE` still appears exactly once in the file (`uv run pytest tests/skills/test_issue_protocol.py -k "create_ref_defines_priority_rule_set_and_required_sections" -v` passes).
- `git diff -U0 src/superclaude/skills/sc-issue-protocol/refs/create.md` shows no change on the lines holding the GitHub-write rule paragraph, the lookup paragraph or Wave 5 step 6 (`uv run pytest tests/skills/test_worker_contract.py -k "classification" -v` passes for the create.md entries).
- Dependents that must keep working: SKILL.md create mode steps 5 and 6 (aligned in Task 4), the three worker files (Task 3), `docs/designs/sc-issue-command.md` (Task 6).

## Task 2: Rewrite the draft-notes template

Depends on: Task 1

Edit `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` (source requirement: the two lists get different consequences, the four categories, user quotation and evidence, and `None` handling). Keep the two headings `## New material` and `## Contradictions` unchanged, because the workers and `refs/create.md` refer to them by name. Replace the intro line 3 ("The orchestrator asks the user one question only when either list has an item") with the new consequence: items under New material never cause a question and are kept in the body and the final output; one or more supported items under Contradictions cause exactly one question. Under New material keep the comment about source (`path:line` or command) and add that assumptions are listed here as `Assumption: <text>`. Under Contradictions replace the comment with the required line format: category (one of the four names), the user's own words in quotes (or the flag as passed), and the conflicting evidence (draft text, or a `path:line` the worker read), and say that a line missing any of the three parts belongs under New material. Keep "None" as the empty marker under both headings and state it is not an item.

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` still has exactly the headings `## New material` and `## Contradictions`, each still holding a `- None` default line.
- The template names the four categories and states "no question" for New material and "one question" for Contradictions in plain words.
- `grep -n "either list" src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` prints nothing.
- `uv run pytest tests/skills/test_issue_protocol.py -k "template" -v` passes (heading-order, marker and no-ClickUp checks on the issue-body templates are unaffected).

## Task 3: Align the three drafting workers with the shared classification

Depends on: Task 2

Edit the Wave 4 body job in `src/superclaude/agents/issue-worker-t1.md` (Deep body), `src/superclaude/agents/issue-worker-t2.md` (Standard-depth body) and `src/superclaude/agents/issue-worker-t3.md` (Quick-depth body), each at line 24. In each, change only the last sentence that starts "Write `<D>/draft-notes.md` from the `draft-notes.md` template, listing any new material ...": it must say to list added material and assumptions under New material, and to list a contradiction only when it fits one of the four categories with the user's own words and conflicting evidence, pointing at the Contradiction prompt rule of the skill's `refs/create.md` (the installed copy under the home `skills/sc-issue-protocol/` folder, the project mirror second, exactly the lookup wording the three files already use for the Priority rule set) rather than copying the definitions. Leave `PLAN_SECTIONS_RULE` and the phrase "does not apply to the three required plan sections" byte-identical in each file.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_worker_agents.py -v` passes, including `test_worker_states_required_plan_sections_rule`, `test_plan_rule_check_fails_when_the_sentence_is_removed` and `test_plan_rule_check_fails_when_the_carve_out_is_removed` for all three workers.
- Each of the three files mentions all of: New material, Contradictions, the four-category rule by pointer to `refs/create.md`, and "Assumption:" handling, and none still says to list "any contradiction between the description and the code" without the category test.
- `tests/skills/test_worker_contract.py` still passes for these agent files (`uv run pytest tests/skills/test_worker_contract.py -v`).

## Phase 2: Align the skill, command and documents

## Task 4: Align SKILL.md and its pinned copy in the worker-contract test

Depends on: Task 3

Edit `src/superclaude/skills/sc-issue-protocol/SKILL.md` in three places. Line 76 ("The only user prompt is the create-mode contradiction question"): say the only prompt is one question for a supported contradiction of the user's own description, instruction or flag, never for added material. Line 102 (create step 5, "Ask one question only when `draft-notes.md` lists new material or a contradiction"): replace with the new decision (zero questions for additions-only or empty notes, one combined question only for a supported contradiction). Line 103 (create step 6, the post step): add that the printed output lists every retained addition and the question outcome, keeping every other clause. Leave the `allowed-tools` line 4 unchanged. Because line 103 is pinned verbatim as a key in the `WRITE_VERB_CLASSIFICATION` table of `tests/skills/test_worker_contract.py` (the entry whose key line starts `6. **Wave 5, post.** Load`), change that key string to the new line 103 text and keep its category `never-worker` and reason unchanged.

Acceptance criteria:
- `grep -n "lists new material" src/superclaude/skills/sc-issue-protocol/SKILL.md` prints nothing, and line 4 still ends with `AskUserQuestion`.
- `uv run pytest tests/skills/test_worker_contract.py -k "classification" -v` passes, including `test_classification_table_has_no_stale_entries` (the updated key matches the live SKILL.md line).
- `uv run pytest tests/skills/test_issue_protocol.py -v` passes (frontmatter, size and allowed-tools checks at lines 40 and 137-144, and `test_rule_10_line_is_carried_verbatim` for SKILL.md).

## Task 5: Align the /sc:issue command file

Depends on: Task 4

Edit `src/superclaude/commands/issue.md`. Line 19 ("Both modes post directly to GitHub; nothing is shown for approval first."): keep the promise and add that `--create` stops only for one question when the draft contradicts your own description, instruction or flag, and never for added material. In the create row of the Outputs table (line 85), keep every file name and state that added material and assumptions are kept, listed in `draft-notes.md` and printed in the final output. Leave the Activation section, the frontmatter, the Options table, the STOP rules and the rule 10 line untouched, and do not add any `src/superclaude/` path to the file.

Acceptance criteria:
- `uv run pytest tests/commands/test_issue_command.py -v` passes (frontmatter, options table, STOP-rule order, activation, `test_no_source_tree_path`, `test_rule_10_line_is_carried_verbatim`).
- `uv run pytest tests/cli/test_issue_body_templates.py -v` passes (installed Handoff/Backlog and rule-10 guards unaffected).
- The create row at line 85 still lists `description.md`, `scout.md`, `flags.md`, `issue-body.md`, `draft-notes.md` and `create-review.md`.

## Task 6: Align the design document and the user guide

Depends on: Task 5

Edit `docs/designs/sc-issue-command.md`: the paragraph at line 223-225 (the worker "lists, in `<D>/draft-notes.md`, any new material ... and any contradiction", and the next paragraph that says the orchestrator asks one question when notes list new material or a contradiction) and the D14 row at line 460 ("Create asks the user one question only when the drafter found new material or a contradiction"). Rewrite both to the new rule: no question for new material, one combined question only for a supported contradiction in one of the four categories, additions kept and printed. Keep the line-381 file-table row naming "contradiction prompt rule" valid. Edit `docs/user-guide/commands.md` at line 357 ("It posts directly to GitHub, without showing the comment or the issue body for approval first"): add one sentence that `--create` asks one question only when the drafted issue contradicts what you said, and keeps and lists everything else it added.

Acceptance criteria:
- `grep -rn "new material or a contradiction" docs/ src/` prints nothing.
- Both docs still say posting is never shown for approval, and the D14 row explains why that does not conflict with the single contradiction question.
- No other design-document decision row (D1 to D26 other than D14) changes.

## Phase 3: Cover the rule with regression tests

## Task 7: Add the four create-decision tests and their mutation cases

Depends on: Task 6

Edit `tests/skills/test_issue_protocol.py`, using its existing helpers `_text`, `REFS`, `TEMPLATES`, `SKILL` and the mutation style of `test_plan_section_check_fails_when_a_heading_is_removed` (lines 784-811). Add exactly these four tests (names from the issue): `test_create_questions_only_for_contradictions` (the create reference asks one question only for a supported contradiction, names all four categories and "exactly one", keeps the question after the user's answer applied before Wave 5, and no longer contains the old trigger text "lists new material" or "keep all"); `test_draft_notes_separates_additions_and_contradictions` (the template keeps the two headings, states "no question" for New material and "one question" for Contradictions, and keeps `None` as the empty marker); `test_create_reports_additions_without_approval` (the create reference step 8 and SKILL.md create step 6 both require the retained additions line `kept without approval:` and still say the body is never shown for approval); `test_contradiction_categories_require_user_evidence` (the reference and the template both require category, the user's own words and conflicting evidence, treat an incomplete line as new material, and say worker disagreement with a supplied flag is not a contradiction). For each, add a mutation case that edits a copy of the text under `tmp_path` (restore the old broad trigger, delete a category, delete the `None` rule) and asserts the check reports the problem, following the problems-list pattern of `plan_section_problems`. Do not change `ALLOWED_TOOLS`, `plan_section_problems` or the existing tests.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py -k "create_questions_only_for_contradictions or draft_notes_separates_additions_and_contradictions or create_reports_additions_without_approval or contradiction_categories_require_user_evidence" -v` runs all four named tests and they pass.
- Each of the four checks has at least one mutation case that fails against the old text (reinserting "lists new material or a contradiction" makes the first check report a problem).
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py tests/skills/test_worker_contract.py -v` passes with no existing test edited except the single key in Task 4.
- `test_stage_claim_skips_recommend_and_plain_claim_keeps_it` (lines 1162-1180) is untouched and passes.

## Task 8: Add command and protocol agreement checks

Depends on: Task 7

Edit `tests/commands/test_issue_command.py`, adding tests in its existing style (module helper `_text()` for the command, `SKILL` for the skill) that check the command file and SKILL.md agree: both keep the direct-posting promise, both say the only pause is one question for a contradiction of the user's own words, neither contains the old broad trigger, and the command's create Outputs row still lists the six create files and mentions retained additions. Add one mutation case on a copy that restores "nothing is shown for approval first" without the contradiction exception and asserts the agreement check fails. Do not weaken or replace the existing metadata, options, STOP-rule, activation, `test_no_source_tree_path` or rule-10 tests.

Acceptance criteria:
- `uv run pytest tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py -v` passes, with the new agreement tests listed in the output.
- The mutation case fails when the contradiction exception is removed from the command text copy.
- The five-file focused gate `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py tests/skills/test_worker_contract.py tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py -v` passes.

## Phase 4: Prove the behavior with controlled create runs and the full gates

## Task 9: Run the controlled create-decision matrix and record it

Depends on: Task 8

Static text checks cannot prove agent behavior, so run the create flow against the changed instructions with every GitHub write intercepted, and record the matrix in `./artifacts/create-decision-matrix.md` (columns: scenario, depth, expected question count, observed question count, posts observed, additions kept, result). Method: install the changed skill, agents and command into an isolated temporary `HOME` with the supported installer (`uv run superclaude install`, forcing a refresh in that temporary home only, never the real `~/.claude`), put a `gh` shim saved as `./artifacts/gh-shim.sh` first on `PATH` that logs each call to `./artifacts/gh-calls.log`, answers the read-only lookups from fixtures, and replaces `gh issue create` with a logged fake that returns a fake issue URL. Scenarios, each at depth quick, standard and deep: empty notes (0 questions); additions-only notes including an `Assumption:` line (0); one scenario for each of the four categories (1 each); two contradictions at once (still 1, naming both); a mixed list of additions and one contradiction (1, and the additions stay in the body); a `None` sentinel in both lists (0); and a user-supplied flag that a worker disagrees with (0 questions, the filed issue uses the user's flag, the pushback comment is still posted at standard and deep). For every asked question, record the answer applied before the single `gh issue create`. If no isolated runner can be set up, or a row cannot be run, write `blocked: <reason>` in that row; do not mark it passed, and do not create live issues without the owner's separate explicit authorization.

Acceptance criteria:
- `./artifacts/create-decision-matrix.md` has one row per scenario per depth (all three depths for all nine scenarios), each with an observed result or an explicit `blocked: <reason>`.
- For every row that ran, observed question count equals expected, `./artifacts/gh-calls.log` shows exactly one `gh issue create` call, and no call to a real GitHub host happened (no real issue exists after the run).
- Mixed rows show the unrelated additions present in the posted body and the final output after the answer was applied; no row shows the full body offered for approval.
- Any `blocked` row is repeated by the executor in its final report so the plan cannot be called fully verified while one exists.

## Task 10: Refresh the project mirrors and run the full gates

Depends on: Task 9

Run `make sync-dev` so the project mirrors under `.claude/` receive the canonical changes (the mirrors stay gitignored and are never staged), then run the gates and save their output: `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py tests/skills/test_worker_contract.py tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py -v` to `./artifacts/gate-focused.log`, then `make test` to `./artifacts/gate-test.log`, `make lint` to `./artifacts/gate-lint.log` and `make verify-sync` to `./artifacts/gate-verify-sync.log`. If `make test` fails on a test this change did not touch, record the test id and its failure on a clean `integration` checkout of the same test before calling it pre-existing; fix anything this change broke.

Acceptance criteria:
- `make verify-sync` exits 0 after `make sync-dev` and `git status --short` shows no path under `.claude/` as a change to stage (only `src/`, `docs/`, `tests/` and `.dev/` paths appear).
- `make lint` exits 0, the focused five-file pytest command exits 0, and `make test` exits 0 or every failure is shown to be unrelated and pre-existing with its evidence in `./artifacts/gate-test.log`.
- `grep -rn "new material or a contradiction" src/ docs/ tests/` prints nothing.
- The package `./artifacts/` holds the four gate logs plus the matrix and the shim from Task 9.
