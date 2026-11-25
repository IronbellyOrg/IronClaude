<!-- /sc:issue feature template (simple). Filled by issue-worker-t3, 2026-11-22. -->

## Feature Summary

Add a way for the person watching the `superclaude observe` dashboard to mark, per coordinator question shown on the questions screen / Decision Desk, whether their intervention was the right call. When it was not, keep a stored record of what was asked and what the decision was, so later work can train when and how the agent should have handled that case autonomously to reach the same result.

## Problem Statement

The observer shows the coordinator's open questions (questions panel and Decision Desk under `src/superclaude/cli/observe/questions.py` and `view.py`), but the person's judgement about their own intervention is lost: there is no place to record "this interruption was necessary" or "the agent should have handled this itself", nor the question and decision text to go with it. Without that record, nothing can later be mined for when the agent should have been left autonomous.

## User Story

As a person supervising a coordinator through the observer dashboard, I want to record, for each question I answered, whether my intervention was the right call and (when it was not) what was asked and decided, so that later work can learn when and how the agent should have handled it autonomously.

## Proposed Solution

Not known yet (no scoring scheme, storage format or training method is given by the description; the storage location and the read-only tension below are the only code-informed parts).

The dashboard already retains each question under a stable key `(Run id, message id)` in `QuestionRecord` (`src/superclaude/cli/observe/questions.py`), so a vote can be attached to that key. A natural place for the stored record is the observer's state directory `$XDG_STATE_HOME/superclaude/observe` (`state_dir()` in `src/superclaude/cli/observe/export.py`), which already writes files atomically via `write_atomic()`.

Tension the owner must decide: the observer is read-only by design. `commands.py` opens with "Read-only. The only Orca calls are the ones `adapter.py` makes", and `Effect` in `view.py` says "no effect ever reaches Orca"; issue #409's dashboard text says the view shows no approval, dispatch, retry or merge actions. A vote does not have to reach Orca (it can stay a local file), but it is the first write-from-input the dashboard would perform, so the owner must confirm that this is acceptable and where it does not violate the read-only contract (local state file: yes; any Orca call: no).

## Acceptance Criteria

- [ ] From the questions screen / Decision Desk, the person can record a yes/no judgement ("was my intervention the right call") for the selected question, keyed by `(Run id, message id)`.
- [ ] When the judgement is "not the right call", the record keeps what was asked and what the decision was.
- [ ] The stored record survives restarts (written under the observer state directory) and later work can read it back.
- [ ] No approval, dispatch, retry or merge action is added to the dashboard; the vote is recorded locally only.

## Out of Scope

- Any scoring scheme, weighting or aggregation of votes.
- Any training method or model change that consumes the records.
- Sending the vote to Orca or making the dashboard issue any write to Orca.
- Changing how questions are collected or retained.

## Components Affected (from `/sc:analyze`)

- `src/superclaude/cli/observe/view.py` — questions panel, Decision Desk (`DeskView`, `DESK_TITLE`), `Effect` enum and `apply_key` key handling (currently only NONE/EXPORT/QUIT, docstring "no effect ever reaches Orca").
- `src/superclaude/cli/observe/questions.py` — `QuestionRecord` keyed by `(Run id, message id)`; the retention store the vote attaches to.
- `src/superclaude/cli/observe/commands.py` — interaction loop; module docstring states "Read-only".
- `src/superclaude/cli/observe/export.py` — `state_dir()` (`$XDG_STATE_HOME/superclaude/observe`), `write_atomic()`: the existing local-write pattern a record file can reuse.
- `src/superclaude/cli/observe/keys.py` — POSIX key reader the new key would come through.
- `tests/observe/` — `test_questions.py`, `test_view.py`, `test_export.py`, `test_commands.py` are the neighbouring test homes.

## Related Issues/PRs

- #409 (TUI dashboard, open) — this feature extends its Decision Desk; #409 also states the view shows no approval, dispatch, retry or merge actions.
- #706 (observer follow-up, open)
- #604 (observer remote fleet, open)
- #718 (dashboard items from the 655 split, open)
- #716 (coordinator next release, open)

## Priority

Medium: a planned feature, not a defect blocking work — the rule set puts a planned feature at Medium.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: master.

Commands, in order: /sc:workflow, then /sc:implement, then /sc:pr-submit --monitor 3.

Steps, in order:

- Step 1: Owner decision first (gate): confirm the vote is a local state-file write only and that this is an accepted exception to the observer's read-only stance; no Orca write is in scope. Record the ruling in the issue before implementation.
- Step 2: Extend `view.py` (`apply_key`, `Effect`, the questions/Decision Desk view) with a key that records the judgement for `session.selected_question`, storing `(run id, message id, judgement, question text, decision note)`; add a record store beside `questions.py` (pure, no I/O in the store itself).
- Step 3: Persist via `export.py`'s `state_dir()` + `write_atomic()` pattern into a new record file under `$XDG_STATE_HOME/superclaude/observe`; keep the existing exports unchanged.
- Step 4: Wire the loop in `commands.py`; update the keys line literal in `view.py` (`QUESTIONS_KEYS_LINE` / `QUESTIONS_LINK_KEYS_LINE`) to name the new key.

## Test plan

- Tests to add or change: new tests in `tests/observe/test_view.py` (key handling produces the record for the selected `(Run, message id)`; no effect reaches Orca — `Effect` stays free of Orca), `tests/observe/test_export.py` or a new `test_votes.py` (record written under a temp `state_dir`, atomic, readable back after "restart"), `tests/observe/test_commands.py` (loop wiring, `--once` path unaffected).
- Regression gate: `uv run pytest tests/observe/ -v`, then `uv run pytest`, `make lint`, `make verify-sync`.
- How a reviewer verifies: run the new observe tests and the full suite green; optionally run `superclaude observe --questions --run <id>` against a fixture (`tests/observe/` fixtures), press the new key on a selected question, and inspect the record file under a temp `XDG_STATE_HOME`.

<!-- sc:issue:create template=issue-feature-simple -->
