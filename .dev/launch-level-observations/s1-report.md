# S1 report: OB-CTX coverage checker

- Date: 2026-11-25. Worktree: /home/coder/workspaces/worktrees/IronClaude/obsctx-plan. Task task_9b771ae0df66.
- Nothing staged, committed or pushed. No /sc: command, no paid session, no GitHub write.

## Built
- /home/coder/workspaces/worktrees/IronClaude/obsctx-plan/tests/hooks/fixtures/launch_level/ob_ctx_check.py
  Pure functions: `check(records, sessions, store_column, verdict_text, human_text, complete)`, `jsonl_records`, `tsv_records`, `verdicts`, `render`. Standard library only.
  CLI: `--jsonl FILE | --tsv FILE`, `--governed-store-column`, `--session SID` (repeatable), `--human-file`, `--stream`, `--complete`. Prints the R1 to R10 table (plus an `other` row), `VIOLATION` lines, and a last line `OB-CTX-CHECK violations=<n>`. Exit 0 only at 0.
- /home/coder/workspaces/worktrees/IronClaude/obsctx-plan/tests/hooks/test_ob_ctx_check.py (16 tests).

## Predicate mapping (how the plan's P1 to P8 were cut)
- P4 = `session_id` absent. P1 = present but not a valid id (integer, space, bad pattern). Together they are the plan's P1 and P4, with no double count.
- P2 = event name, `tool_name`, `tool_input`, `tool_use_id`, `prompt` shape. P3 = `agent_id`/`agent_type` not strings, or a session id outside the governed set (a subagent line with another session id).
- P5 (with `--stream`): no verdicts, any `unknown`, a `governed` verdict with a foreign id, or more than 2 `ordinary` (LIM-1 and LIM-2) are violations.
- P6 (with `--human-file`): the `human shell` line must read `ordinary`; the `governed job child` line must read `governed` with a run session id.
- P8 (only with `--complete`, off by default so the existing evidence is not failed for rows it never had): a PreToolUse line (UserPromptSubmit for R1) for R1, R2 (main, sub), R3, R4, R5 (main, sub), R6 (main, sub), R7 (main, sub).
- Void run: no governed line in scope gives a `VOID` violation, so an empty file prints `violations=1` and exits 1; it cannot read as a pass.

## Not done, on purpose
- P7 is not a separate predicate. Resume = run P1 to P4 with Run A's `--session`; fork = run it with the fork's own id. Whether a fork's verdict is `ordinary` is covered by P5 only loosely (it allows up to 2 ordinary).
- "Nested" subagent cannot be told from the payload alone, so the table has only main and sub columns, and P8 does not require a nested line. R8 (needs the stream's init tool list) is not checked by P8. Both would need extra input; the plan can add them in S7 if the owner wants.
- `--stream` counts each verdict it finds once, so feed it verdict lines (for example the `jq` output of S7 step 2), not a raw stream where the same verdict appears twice.

## Test and lint
- `uv run pytest tests/hooks/test_ob_ctx_check.py -q`: 16 passed.
- `uv run ruff check` on both files: All checks passed. `ruff format` was also applied to both new files.
- Cases covered: missing `session_id`, integer `session_id`, id with a space, integer `agent_id`, subagent line with another session id, missing `tool_use_id`, `tool_input` not an object, unknown event, prompt missing, good run with counts, empty file (void), store column "absent" lines skipped, P5, P6, P8, CLI exit code.

## Coverage over the existing governed evidence
Output file: /home/coder/workspaces/worktrees/IronClaude/obsctx-plan/.dev/launch-level-observations/evidence/ob-ctx-existing-coverage.tsv (three runs, one section each, each with its own `OB-CTX-CHECK` line). Evidence read from /home/coder/workspaces/worktrees/IronClaude/obs-plan/.dev/launch-level-observations/evidence/.

| File | Governed lines | R1 | R2 Pre main/sub | R5 Agent Pre | R6 Pre | R10 Pre main/sub | Violations |
|---|---|---|---|---|---|---|---|
| ob-h3-F-issue-841-probe.tsv (sessions 3852709b and dc89127a) | 158 of 158 | 5 | 16 / 2 | 3 | 26 | 17 / 13 | 0 |
| ob-h3-W-issue-829-probe.tsv (session dc89127a; the 5 Coordinator lines are `absent`, skipped) | 39 of 44 | 7 | 5 / 0 | 0 | 7 | 6 / 0 | 0 |
| ob-h2-real-claim-827-probe.tsv (no store column; `--session 2af36456`) | 13 of 13 | 1 | 2 / 0 | 0 | 2 | 3 / 0 | 0 |

- Rows R3, R4, R7, R8, R9 have zero governed lines in all three files (as the plan said: no background Bash, Monitor, SendMessage, NotebookEdit/Cron*, push-class MCP). Row "other" (a plain MCP tool) has 1 Pre and 1 Post in the 841 file.
- Zero violations of P1 to P4: every governed line has a valid string `session_id`, valid `tool_use_id`, string `agent_id`/`agent_type` where present, and a known event name.
- Two things to know, neither a violation: (1) the 841 file holds 2 subagent lines of session dc89127a (issue 829's agent), so it only passes with both session ids given; with `--session 3852709b` alone they are reported as P3 (this matches the plan's hygiene note 2). (2) In the 841 file subagent Bash has 2 Pre and 3 Post lines; the 827 file has 2 Bash Pre and 0 Post. Pre and Post counts need not match (blocked or still-running calls, the plan's own note), so the checker does not compare them.
- The live issue 842 log (/tmp/ll-obs-h23.qJA6WFwb/logs/ob-h3.tsv) was not run: the task named only the three evidence files.
