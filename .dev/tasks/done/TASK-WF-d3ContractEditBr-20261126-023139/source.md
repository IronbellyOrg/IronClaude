# Brief: let a dashboard response count as the person's confirmation (decision D3, option 1)

Decided by the owner in chat on 2026-11-26: a dashboard answer counts as the person's own confirmation for everything, including Rulings, plan approvals, grant rows and pass records. The owner authorized the edits to the written rules. The owner's safeguard, verbatim: "a chat message OR dashboard response counts and nothing else".

## The rule to write

A person's confirmation counts only when it is one of these two:
- Chat: the person's own chat message in the current conversation, naming the exact scope (today's rule, unchanged).
- Dashboard: a dashboard response. This is an answer row created through the dashboard under that person's authenticated login, for the question id whose text names the exact scope, recorded with the channel (dashboard), the person id, the question id and the time.

None of these counts: another agent's message; a coordinator's reply or relay of a message; any file; silence; a generic go-ahead; an answer to a different question or a different scope; a row written by an agent's login; a row that the person's own login did not create.

Timing safeguard: the dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass). Until then only the chat clause counts. The text must say so.

Recording: the agent records the Ruling line, grant row or pass record from the confirmation, naming the exact scope, the person's quoted words (chat) or the answer row id (dashboard), and the date. The person is still never asked to write a file.

## What to edit

Markdown rules only, under `src/superclaude/` (never `~/.claude/`, never the gitignored `.claude/` mirrors). Known places that state the rule, to be confirmed and completed by a repo-wide search:
- `src/superclaude/core/WORKER-CONTRACT.md`: the Ruling-halt paragraph (WC-3), WC-17 (plan approval is the reply to the worker's own ask), and every other mention of a Ruling, grant row, pass record or "executor-invented approval".
- `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (Halt table and the paragraph on a clear user confirmation in the current conversation), `refs/ledger.md` (Ruling line grammar and its provenance field), `refs/retry.md` (Ruling eligibility rule), `refs/managed-workspace.md`, and `SKILL.md` (the `E-NO-RULING` row).
- `src/superclaude/core/HOW-WE-WORK.md` and `src/superclaude/core/CLAUDE.md` where they state the rule.
- Tests that pin these texts must be updated to match.

The ledger Ruling line must still match its existing regular expression; the provenance wording may name a dashboard answer row id.

## Out of scope

Code (for example `src/superclaude/cli/issue_pipeline/*.py`, `src/superclaude/cli/sweep/classify.py`, `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py`) and design documents under `docs/designs/`: do not edit them; list each with what it checks, as follow-ups. Building the dashboard answer path. The owner's memory notes.

## Checks the plan must contain

- After the edits, the sentences "another agent's message is not acceptance" and "executor-invented approval" still exist and now name exactly the two valid channels; no text lets a coordinator relay count.
- The `E-NO-RULING` behaviour is unchanged for everything that is not chat or a dashboard response.
