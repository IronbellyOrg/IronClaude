---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-d3ContractEditBr-20261126-023139
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Let a dashboard response count as the person's confirmation (D3, option 1)

Source: ./source.md
Goal: The written rules name exactly two valid channels for a person's confirmation (their own chat message, or a dashboard response once the dashboard answer path is released) and nothing else, in every file that states the rule, with the tests that pin the text updated and a new test pinning both channels, the nothing-else list and the timing safeguard.

## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.

## Phase 1: Define the rule once

## Task 1: Rewrite the confirmation rule in the worker contract

Edit src/superclaude/core/WORKER-CONTRACT.md, the WC-3 bullet that begins "A Ruling halt is never asked" (line 57). Make it the single governing definition of a valid confirmation. State: a person's confirmation counts only as (a) their own chat message in the current conversation naming the exact scope, or (b) a dashboard response, meaning an answer row created through the dashboard under that person's authenticated login for the question id whose text names the exact scope, recorded with the channel (dashboard), the person id, the question id and the time. List what never counts: another agent's message, a coordinator's reply or relay of a message, any file, silence, a generic go-ahead, an answer to a different question or scope, a row written by an agent's login, a row the person's own login did not create. State the timing safeguard (clause b applies only when the dashboard answer path is released; until then only clause a). State the recording rule: the agent records the Ruling line, grant row or pass record from the confirmation, naming the exact scope, the person's quoted words (chat) or the answer row id (dashboard), and the date; the person is never asked to write a file. Keep the decision D2 amendment note and the existing sentence that a Ruling halt is never asked and is reported blocked. Rewrite the final sentence so "executor-invented approval" names a Ruling line, grant row or pass record recorded without one of the two channels for that exact scope.

Acceptance criteria:
- WORKER-CONTRACT.md line 57 area contains both channels, the nothing-else list including "a coordinator's reply or relay", the timing safeguard and the recording rule, and still contains the phrases "another agent's message" and "executor-invented approval".
- No sentence in WORKER-CONTRACT.md says or implies that a coordinator's reply or relay is acceptance (Grep for "relay" and "coordinator's reply" in the file and Read each hit).
- Dependents updated by later tasks: tests/skills/test_worker_contract.py (Task 7) and the executor rules (Tasks 3 to 5).

## Task 2: Align the rest of the worker contract with the single definition

Depends on: Task 1

Read and, where they conflict with Task 1, edit these places in src/superclaude/core/WORKER-CONTRACT.md: WC-17 (line 59, plan approval is the reply to the worker's own ask), line 190 (a coordinator never "writes or drafts a Ruling"), the resume section (lines 256-278, including check 3 item (4) that points to the Ruling eligibility rule), and the issue-pipeline bullets (lines 296-303, "Plan approval", "Completion", "Never", and the grant-row wording). Add a short pointer to the WC-3 definition where a place restates who may confirm; do not restate the full rule a second time. Leave any place that is about timing or mechanics, not about who confirms, unchanged.

Acceptance criteria:
- Each place named above has been read, and the final report of this task lists which were edited and which were left unchanged with the reason.
- Where a place says approval or confirmation is given in chat, it now either points to the WC-3 definition or names both channels; none contradicts the single definition.
- WC-17 and the plan-approval flow keep their mechanics (plan hash, check-approval, ack) unchanged.

## Phase 2: Align the executor rules

## Task 3: Update the implement QA rules to name both channels

Depends on: Task 1

Edit src/superclaude/skills/sc-implement-protocol/refs/qa.md: the accepted-minor versus Ruling table rows "Who decides" and "Writes a Ruling: line" (lines 215-220), the Halt table rows for a clear user confirmation and for `E-NO-RULING` (lines 248-249), and the paragraph beginning "A Ruling counts only when it is eligible" (line 254) and the following paragraph (line 256-259). Replace "clear user confirmation in the current conversation is sufficient" with wording that names both channels by pointing to the definition in core/WORKER-CONTRACT.md (installed path ~/.claude/WORKER-CONTRACT.md, as other primitives already cite it) and repeating only the two channel names; keep "another agent's message" and "executor-invented approval" in the text. State that the provenance in the Ruling's `<what>` field is either the person's quoted chat words or the dashboard answer row id.

Acceptance criteria:
- qa.md names the chat channel and the dashboard channel (with the timing safeguard) and keeps the E-NO-RULING row for missing or ambiguous confirmation, `--force` and executor-invented approval.
- The phrases "another agent's message" and "executor-invented approval" remain in qa.md.
- qa.md contains no src/superclaude/ path (installed primitives never cite that path).
- Dependents updated by Task 7: tests/skills/test_task_workspace_lifecycle.py and tests/skills/test_implement_severity_static.py.

## Task 4: Update the ledger Ruling line rules and examples

Depends on: Task 3

Edit src/superclaude/skills/sc-implement-protocol/refs/ledger.md: the heading and prose of "Ruling line (user-authorized, executor-recorded)" (lines 62-72), the post-ruling complete line prose (lines 74-82) only where it says who confirms, and the examples at lines 193-199. Keep the three-field grammar `T<id>: Ruling: <what> — <why> — <cost-if-wrong>` and the regular expression unchanged. Say the `<what>` field carries the provenance: the person's quoted chat words, or the dashboard answer row id. Add one example of a dashboard-provenance Ruling line that matches the regular expression.

Acceptance criteria:
- The regular expression in ledger.md is byte-identical to before.
- The new dashboard example line matches that regular expression (check by running the regular expression over the example with uv run python -c in a throwaway command; record the result in the final report).
- ledger.md names both channels and does not let a coordinator relay count.

## Task 5: Check the remaining rule files for conflicts and edit only where they conflict

Depends on: Task 4

Read each of these and edit only a sentence that states who may confirm a Ruling or approval and is now incomplete: src/superclaude/skills/sc-implement-protocol/refs/retry.md (Ruling eligibility rule, lines 498-500; it is about timing, expected unchanged), src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md (line 76 and the table rows at 92-93), src/superclaude/skills/sc-implement-protocol/SKILL.md (the E-NO-RULING row at line 41, lines 58, 149-150, 193), src/superclaude/commands/implement.md (line 107), src/superclaude/core/HOW-WE-WORK.md (line 114 and any other place that says approval comes only in chat) and src/superclaude/core/CLAUDE.md. If HOW-WE-WORK.md changes, copy it byte for byte to plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md as the project rules require, and re-run the level-table copy into src/superclaude/core/CLAUDE.md.

Acceptance criteria:
- The final report lists each file as edited or unchanged, with one line of reason.
- The `E-NO-RULING` row in SKILL.md still stops for `--force`, missing or ambiguous confirmation and executor-invented approval.
- If HOW-WE-WORK.md was edited, plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md is byte-identical to it (cmp exits 0).

## Phase 3: Tests and follow-ups

## Task 6: Mirror the edited skill rules into the plugin copy

Depends on: Task 5

The plugin copy under plugins/superclaude/skills/sc-implement-protocol/ is tracked and was byte-identical to src/superclaude/skills/sc-implement-protocol/ for refs/qa.md before this plan. Copy each edited file byte for byte from src/superclaude/skills/sc-implement-protocol/ to plugins/superclaude/skills/sc-implement-protocol/: refs/qa.md, refs/ledger.md, and refs/managed-workspace.md, refs/retry.md or SKILL.md only if Task 3, 4 or 5 edited them. Do not edit anything else under plugins/. There is no plugin copy of WORKER-CONTRACT.md.

Acceptance criteria:
- For every file copied, cmp of the src file and the plugins file exits 0.
- git diff --stat under plugins/ shows only the files listed above.

## Task 7: Update the tests that pin the old text

Depends on: Task 6

Edit the existing assertions that quote the old wording so they match the new text: tests/skills/test_worker_contract.py (test_owner_records_are_given_in_chat_and_recorded_by_the_agent and any neighbour that quotes WC-3 or WC-17 text), tests/skills/test_task_workspace_lifecycle.py (lines 338-349, 485, 878), tests/skills/test_implement_severity_static.py (line 410), tests/skills/test_workflow_archive.py (line 350) and tests/sweep/test_classify.py (line 744). Change only assertions made false by Tasks 1 to 6; keep each test's intent.

Acceptance criteria:
- uv run pytest tests/skills/test_worker_contract.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_severity_static.py tests/skills/test_workflow_archive.py tests/sweep/test_classify.py passes.
- Any test that fails for a reason other than the changed wording is reported, not edited around.

## Task 8: Add a regression test for the two channels, the nothing-else list and the timing safeguard

Depends on: Task 7

Create tests/skills/test_confirmation_channels.py. It reads src/superclaude/core/WORKER-CONTRACT.md and src/superclaude/skills/sc-implement-protocol/refs/qa.md and asserts: both channel names are present; each item of the nothing-else list is present (another agent's message, coordinator's reply or relay, any file, silence, generic go-ahead, different question or scope, agent-login row, row not created by the person's login); the timing safeguard sentence is present; "executor-invented approval" and "another agent's message" are present; no line in WORKER-CONTRACT.md or qa.md says a relay or a coordinator's reply counts as acceptance; and the ledger Ruling regular expression still matches the chat example and the dashboard example in refs/ledger.md. Follow the helper style already used in tests/skills/test_worker_contract.py.

Acceptance criteria:
- uv run pytest tests/skills/test_confirmation_channels.py passes.
- The test fails when the timing safeguard sentence or any nothing-else item is removed from WORKER-CONTRACT.md (check once by editing a throwaway copy of the text inside the test run, not the repository file).

## Task 9: Write the follow-up list of code that checks approvals

Depends on: Task 8

Write ./artifacts/follow-ups.md in this package. List docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md (lines 717, 722 and 2204 restate the old rule and cite WORKER-CONTRACT.md:57 and qa.md:249 by line number) as a document that needs its own update, not edited here. For each of src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py and src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py, name the function or line range that checks an approval or Ruling, say what it checks today, and say what would have to change for it to accept a dashboard answer row. State plainly that none of these files was edited. Also list docs/designs/ files that restate the old rule, found by Grep for "executor-invented" and "another agent's message" under docs/designs/.

Acceptance criteria:
- ./artifacts/follow-ups.md exists and names all four code files with a read line range each.
- git diff --stat shows no change to those four files or to docs/designs/.
