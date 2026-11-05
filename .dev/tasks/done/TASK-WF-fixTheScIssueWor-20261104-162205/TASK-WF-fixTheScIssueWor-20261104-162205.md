---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-fixTheScIssueWor-20261104-162205
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Make the /sc:issue worker agents always write their files

Source: ./source.md
Goal: Each of the three `/sc:issue` worker agents states early, in identical words, that the exact files it writes under `.dev/issues/` are tool inputs it must write with the Write tool (not report files), repeats that in its Rules section, and the skill's spawn rule tells the orchestrator to restate it in every spawn prompt; regression tests pin all of it and fail on the old text.

## Constraints

- Background (verified defect): Claude Code injects into every subagent's system prompt the line "Do NOT Write report/summary/findings/analysis .md files. Return findings directly as your final assistant message ... (Files written as input to another tool are fine; this note is about report files.)". On a live claim of issue #365, `issue-worker-t2` obeyed it, wrote neither `accuracy-check.md` nor `summary.md`, and returned text. Coordinator follow-up (message "Retry still skipped summary.md: name the files explicitly"): the protocol's one retry, with a spawn prompt stating the exemption in general terms, wrote `accuracy-check.md` but still skipped `summary.md`, because the harness line names "summary" files directly. So the rule must name the exact files, say writing them with the Write tool is mandatory and that returning their content as text is a failure, and sit early in each agent file, not only in Rules.
- Files in scope: `src/superclaude/agents/issue-worker-t1.md`, `src/superclaude/agents/issue-worker-t2.md`, `src/superclaude/agents/issue-worker-t3.md`, `tests/skills/test_issue_worker_agents.py`, and one added line in the "Workers and the spawn rule" section of `src/superclaude/skills/sc-issue-protocol/SKILL.md` (judged needed: the spawn prompt is the instruction nearest the worker's action, and the retry evidence shows a general statement there is not enough, so it must name the exact paths). No other file is edited.
- `flags-user.md` is not in the worker file list: the orchestrator writes it (`src/superclaude/skills/sc-issue-protocol/refs/create.md`, deep row of the flag table), and `issue-worker-t1` is told never to read it.
- Exact early section (byte-identical in all three agent files, inserted directly after the opening "Spawned only by ..." paragraph and before `## Jobs for this tier`):

  `## Your files are tool inputs, not reports`

  `The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, `summary.md`, the reports under `analysis/`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md`) are input files for the orchestrator's next tool calls (`gh --body-file` posts and `/sc:recommend`), not report files, so a general instruction against writing report or summary `.md` files does not apply to them. Writing every file your job names with the Write tool is mandatory; returning its content as text instead is a failure (`E-WORKER-NO-OUTPUT`).`
- Exact Rules bullet (byte-identical in all three agent files, inserted in `## Rules` directly after the `**Writing only under `.dev/issues/`.**` bullet):

  `- **Write your files.** Every file your job names is a tool input, not a report (see "Your files are tool inputs, not reports" above): write it with the Write tool and never return its content as text.`
- Exact SKILL.md line (a new paragraph directly after the paragraph that starts "Workers make read-only GitHub and git calls" in "Workers and the spawn rule"):

  `Every spawn prompt names each exact path the job must write under `.dev/issues/` and states that these are input files for the orchestrator's next tool calls, not report files: the worker writes them with the Write tool, and returning their content as text counts as no output (`E-WORKER-NO-OUTPUT`).`
- The new text must keep every existing test green: it names no `gh issue`, `gh pr` or `gh label` command (the fork-safety scan `gh_lines_missing_repo`), no `~/.claude/skills/` path (the dual-surface scan) and no `src/superclaude/` path in an agent file; SKILL.md stays under 500 lines.
- Do not touch any other wording in these files (the earlier minor review notes m1 to m7 and N1 to N3 stay as they are). Do not edit `.claude/` copies by hand; `make sync-dev` regenerates them and they are never staged.
- Negative proofs use `tmp_path` copies; the real files are never reverted.
- UV only (`uv run pytest`). No commits, pushes or GitHub writes. `.dev/tasks/` is staged with `git add .dev/tasks`.

## Phase 1: Regression tests that fail on the old text

## Task 1: Add the tool-input rule tests to tests/skills/test_issue_worker_agents.py

Add to `tests/skills/test_issue_worker_agents.py`:

- module constants holding the exact early-section heading, the early-section paragraph, the Rules bullet and the SKILL.md line from the Constraints (byte-identical), plus a `SKILL` path constant for `src/superclaude/skills/sc-issue-protocol/SKILL.md`;
- a helper `tool_input_rule_problems(text)` that returns a list of problems for an agent file text: the heading missing, the heading not before `## Jobs for this tier`, the paragraph not appearing exactly once directly under that heading, any of the files `scout.md`, `accuracy-check.md`, `summary.md`, `analysis/`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md` missing from the paragraph, or the Rules bullet not appearing exactly once inside the `## Rules` section;
- a test parametrized over `sorted(WORKERS)` asserting `tool_input_rule_problems` returns `[]` for each agent file;
- a negative test parametrized over `sorted(WORKERS)` that writes a `tmp_path` copy of the agent file with the early section and the Rules bullet removed (the pre-fix text) and asserts the helper reports problems for it;
- a test asserting the "Workers and the spawn rule" section of SKILL.md (from its heading to the next `## ` heading) contains the SKILL.md line exactly once, and a negative test that a `tmp_path` copy of SKILL.md with that line removed fails the same check.

Before Tasks 2 and 3, run the new positive tests against the current, unedited files and save the output with its exit code to `./artifacts/t1-red.log`.

Acceptance criteria:
- The constants, the helper and the four new tests exist in `tests/skills/test_issue_worker_agents.py`; no existing test is changed.
- `./artifacts/t1-red.log` shows the agent positive test failing for all three agent files and the SKILL.md positive test failing, with a non-zero exit code recorded: proof the tests fail on the old text.

## Phase 2: The rule in every worker agent and in the spawn rule

## Task 2: Add the early section and the Rules bullet to the three issue-worker agent files

Depends on: Task 1

Insert the exact early section from the Constraints into `src/superclaude/agents/issue-worker-t1.md`, `src/superclaude/agents/issue-worker-t2.md` and `src/superclaude/agents/issue-worker-t3.md`, directly after the opening "Spawned only by ..." paragraph, and insert the exact Rules bullet directly after the `**Writing only under `.dev/issues/`.**` bullet in each file's `## Rules`.

Acceptance criteria:
- Each agent file carries the early section and the Rules bullet exactly once, byte-identical across the three files; `git diff` on each file shows only those additions.
- The Task 1 agent tests (positive and negative) and every pre-existing test in `tests/skills/test_issue_worker_agents.py` pass.

## Task 3: Add the spawn-prompt line to SKILL.md and sync

Depends on: Task 2

Add the exact SKILL.md line from the Constraints to `src/superclaude/skills/sc-issue-protocol/SKILL.md` as a new paragraph directly after the paragraph starting "Workers make read-only GitHub and git calls" in "Workers and the spawn rule". Then run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- SKILL.md gains exactly that one line (plus its blank separator line) and no other change.
- `uv run pytest tests/skills/test_issue_worker_agents.py tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py -v` passes; output and exit code saved to `./artifacts/t3-green.log`.
- `make verify-sync` exits 0 after `make sync-dev`; output and exit code saved to `./artifacts/t3-verify-sync.log`.
