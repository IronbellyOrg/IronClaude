# Gates (Task 10)

Run on 2026-11-26 from the repository root `/home/coder/workspaces/worktrees/IronClaude/issue-834-rest`, branch `clayphi/issue-834-rest`, HEAD `ad306da5c52ea3725b45448ae5576e950d4f620f` (the branch was fast-forwarded to `origin/integration` before the gates; nothing is committed yet; this work's files are untracked). Raw output of each gate: `./gates/*.txt` (`full-suite-reduced.txt` is the full-suite output with most per-test PASSED lines removed; the summary line and the failure blocks are intact; the original is in the scratch directory); `./gates/ruff-checks.txt` holds the ruff version, format checks and the standalone rerun of a failing test.

| Gate | Command | Exit code | Summary line as printed | Result |
|---|---|---|---|---|
| Focused tests | `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_create_question_scenarios.py tests/commands/test_issue_command.py -q` | 0 | `296 passed in 1.77s` | pass |
| Lint | `make lint` | 0 | `All checks passed!` (architecture policy: `PASS, 4 warning(s)`) | pass |
| Sync check, first run | `make verify-sync` | 2 | `Drift detected! Run 'make sync-dev' to fix` (the gitignored `.claude/` copy of this fresh worktree held no skills, agents or commands: every line was `MISSING in .claude/...`) | fail, environmental |
| Sync, after `make sync-dev` | `make sync-dev` (exit 0), then `make verify-sync` | 0 | `All components in sync.` | pass |
| Full suite | `make test` | 2 | `2 failed, 25535 passed, 64 skipped, 9 warnings in 1569.30s (0:26:09)` | 2 failures, not connected to this work (below) |

## The sync check

`make verify-sync` failed once, before `make sync-dev` had been run in this worktree. `.claude/` is gitignored and is created by `make sync-dev`; the failure listed missing copies only, not a difference between `src/` and a changed file. After `make sync-dev` the check passes. `make sync-dev` writes only the gitignored `.claude/` folder; `git status` shows nothing staged and no file changed under `src/` (below).

## The two failing tests of the full suite

- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`

Connected to the files this work changed? No. This work adds only `tests/skills/test_issue_create_question_scenarios.py` and files under `.dev/`; the failing tests concern the `cli/eval` adapter module and run `.venv/bin/python -m ruff`. Rerun alone, the first test fails with `.venv/bin/python: No module named ruff` (the test's ruff subprocess prints it on stderr; stdout is empty, so the `TID251` assertion fails). `ruff` is not installed as a module in this worktree's `.venv` (the project's `uv run ruff` finds it elsewhere: `ruff 0.17.3`). The cause is the worktree's environment, not a file of this work. No test was skipped, relaxed or changed, and nothing under `src/` was changed to pass a gate.

## Format check (not one of the four gates)

The CI format gate covers `src/` and `tests/` (`.pre-commit-config.yaml:129-134`). `uv run ruff format --check tests/skills/test_issue_create_question_scenarios.py` prints `1 file already formatted`. `uv run ruff format --check src tests` reports 6 files that would be reformatted; none is a file of this work (the local ruff is 0.17.3, the repository pins 0.15.20, and the formatter output is version-sensitive). The harness files under `.dev/` are outside that gate. Note that `make lint` (`uv run ruff check .`) therefore also ran with ruff 0.17.3, not the pinned 0.15.20; the raw output is in `./gates/ruff-checks.txt`.

## After the gates

- `git status --short` shows only untracked paths: `.dev/issues/834/`, `.dev/reflect/pre-createQuestionEv-20261126142850/`, `.dev/reflect/pre-issueSummary-20261126132809/`, `.dev/tasks/archive/TASK-WF-createQuestionEv-20261126-142533/`, `.dev/tasks/archive/TASK-WF-createQuestionEv-20261126-170236/`, `.dev/tasks/archive/TASK-WF-issueSummary-20261126-132314/`, `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/`, `tests/skills/test_issue_create_question_scenarios.py`.
- No file under `src/` is modified (`git status --short src` prints nothing), nothing is staged, and nothing under `.claude/` or `.dev/issues/` is staged.
