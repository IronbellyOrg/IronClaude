# Codebase context: naming report directories

Source tier: fallback_1 (the auggie retrieval tool is not available in this session; codegraph search, Grep and Read were used instead). Graph rows are leads; the lines below were read from files or grep output.

## Rules the worker contract already fixes (`~/.claude/WORKER-CONTRACT.md`)

- WC-4: exactly one report directory per run, known before dispatch; a command refuses one that already holds a `return-contract.yaml`.
- WC-6: every retry is a new Task with its own report directory, recording the old Task ID.
- WC-11: two workers in one worktree never write the same file; "the coordinator gives every Task its own report directory"; default paths carry "a timestamp or the slug the coordinator passes".
- Section 4, child worktrees: a Task placed in a child gets an absolute report directory inside that child; concurrent `/sc:implement` runs in different worktrees use distinct plan slugs.
- Worked example: `.dev/tdd/auth-1/`, then the retry `.dev/tdd/auth-2/`.
- Nested commands: `<report-dir>/nested/<command>-<n>/`, `<n>` from 1, never reused.

## Naming schemes already in use

| Where | Pattern | Evidence |
|---|---|---|
| brainstorm default | `.dev/brainstorms/<ts>-<slug>/`, `-N` suffix on collision | `src/superclaude/commands/brainstorm.md:62` |
| workflow package | `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` (UTC, camelCase subject, at most 16 characters, `-2` to `-9` on collision) | `.dev/README.md:47` |
| reflect | `.dev/reflect/...` | `src/superclaude/commands/reflect.md:101` |
| P1 live plan | one fixed directory per check: `.dev/p1-live/<command-name>/` (also `watch`, `guard1`, `commit-grant`) | `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md` lines 73 to 565 |
| Python helpers | timestamp-stamped names, for example `%Y%m%dT%H%M%S` | `src/superclaude/cli/sprint/rerun_tasks.py:247` |
| pr_submit run log | `default_output_dir(pr_number, timestamp, base_dir)` | `src/superclaude/pr_submit/run_log.py:386` |
| eval | `_default_output_dir(started_at, suite_name)` | `src/superclaude/cli/eval/commands.py:1331` |

## Observations

- Every generated scheme in the repository combines a readable subject with a timestamp or a counter. Only the hand-written P1 live plan uses a bare subject, and it works there because each check runs once.
- Nothing in the repository derives a report directory from the Orca Task ID. The Task ID exists only after the Task is created, and the brief is the Task's spec, so a name built from it cannot be written into the same brief without a second step (UNVERIFIED: whether `task-create` can return the ID before the spec is stored).
- A timestamp chosen by the coordinator when it writes the brief is known before dispatch, so it satisfies the "known before dispatch" rule. A timestamp chosen by the worker does not.
