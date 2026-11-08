# Wave 1 shared context (UC-2 post-execution reflect run)

Written by the reflect orchestrator at Wave 0/1. Read-only context for helper agents. Every helper writes ONLY under `OUT/artifacts/` (or returns text); nothing else in the repo may be edited, staged, committed or moved. No `git` mutation, no tests/builds (the orchestrator already ran them), no network.

## Paths (absolute)

- REPO = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher
- OUT = REPO/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post
- Tasklist (executed task file, 1091 lines) = REPO/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- Driving design/spec (935 lines) = REPO/docs/designs/issue-watcher.md  (design sections: 4 command interface, 5 components, 6 cycle, 7 dispatch record, 8 call contracts, 9+ security, 12 tests, 13 gates, 14 PROPOSAL values, 17 acceptance criteria AC-1..AC-25 at lines ~868-898, 18 FR/NFR table at ~902-935)
- Finalized spec (FR-001..FR-029, NFR-001..NFR-014, closed reason table lines 330-358, runbook steps 384-395) = REPO/.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md (untracked, read-only context)
- Decision register (wins over the design where they disagree; DF-01..DF-60; 29 are "DEVIATION = yes" authorized departures) = REPO/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md
- Open Questions (authorized departures OQ-1..OQ-29, readings OQ-36..OQ-51, PRE reflect findings PRE-1..13) = tasklist lines 916-1003
- Executor's own claims (NOT evidence; verify independently): REPO/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/{ac-trace,deviation-register,final-gate-record,final-change-set,post-completion-validation}.md and phase-outputs/test-results/*

## Diff under audit

- BASE = e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b ; HEAD = 26f551f41edece1f05c07a3c02d78325e365f6d1 (ONE commit "feat(cli): add issue-watch poller for issue #331", 379 files, 87301 insertions, all additions)
- Source (6333 lines in 12 non-test, non-.dev files): src/superclaude/cli/issue_watch/{__init__(0),audit(404),cli(348),cycle(1369),github(960),launch(355),predicates(312),record(865),runner(130)}.py ; src/superclaude/cli/main.py (+4 lines) ; docs/designs/issue-watcher.md (935) ; docs/designs/issue-watcher-setup.md (651)
- Tests: tests/issue_watch/ (40 files incl. conftest.py, 19 `_assumed_shape` JSON fixtures under tests/issue_watch/fixtures/_assumed_shape/)
- .dev: 327 files (task package, research, qa gates, phase-outputs, reflect/pre) -- the process artifacts of the task
- Use `git show 26f551f4:<path>` or read the working tree (the tree equals HEAD for these paths; git status is dirty only for the tasklist file and untracked .dev/ files)

## Verification run results already obtained by the orchestrator (Step 5 / 5.5)

- `uv run ruff check src/superclaude/cli/issue_watch tests/issue_watch src/superclaude/cli/main.py` -> "All checks passed!" ; `uv run ruff format --check ...` -> "31 files already formatted"
- pytest on tests/issue_watch: running; result will be in OUT/verify-logs/invocations.yaml when done

## Codegraph run state (Wave 0 readiness check)

index_state=fresh checked_at=2026-11-08T04:12:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher  (use projectPath on every codegraph call; a codegraph row is a lead you Read before citing; Grep/Read floor is always allowed)

## Rules for every helper

- Every claim you report needs a real `file:line` you Read; no citation = tag the claim [INFERRED].
- Do not trust the executor's reports as evidence; use them only as leads.
- Report only what you verified. If you could not verify something, say so.
