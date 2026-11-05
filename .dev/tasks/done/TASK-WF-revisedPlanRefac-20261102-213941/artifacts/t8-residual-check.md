# Task 8 residual-hit check

Sources: `./artifacts/t8-residual-a.txt` (Search A), `./artifacts/t8-residual-b.txt` (Search B); classes from `./artifacts/worktree-hit-classification.md`.

## Search A: 94 lines in 11 files (was 108 in 17)

| File | Hits | Class (Task 1) | Why it remains |
|---|---|---|---|
| POST-REFLECT-TASK.md | 79 | Historical record | Owner decision: unchanged. |
| CLAUDE.md | 3 | Project worktree (rewritten in Task 3) | Lines 312, 315, 316: forbid the retired location and raw `git worktree add`, state the internal-checkout exception, and describe existing retired-location checkouts. |
| .gitignore | 1 | Project worktree (comment rewritten in Task 5) | Line 242: the `.dev/worktrees/` entry kept as a retired-path guard. |
| scripts/eval_runner.py | 1 | Internal temporary checkout | Line 165: the error message `git worktree add exited with code ...` of the new temporary checkout (new hit after the Task 2 rewrite; same file and class). |
| src/superclaude/cli/reflect/config.py | 1 | Internal temporary checkout | Unchanged. |
| src/superclaude/skills/sc-post-release-protocol/SKILL.md | 1 | Internal temporary checkout | Line 91: optional tag checkout, now made in a temporary directory and removed after the scan (Task 6). |
| src/superclaude/skills/sc-reflect-protocol/SKILL.md | 2 | Internal temporary checkout | Unchanged. |
| tests/cli/reflect/test_isolate_reviewers_cli.py | 2 | Internal temporary checkout | Unchanged. |
| tests/skills/test_implement_retry_revert.py | 2 | Internal temporary checkout | Unchanged (pytest `tmp_path` fixture). |
| tests/troubleshoot/backtest/git_replay.py | 1 | Internal temporary checkout | Unchanged. |
| tests/troubleshoot/backtest/test_git_replay_integration.py | 1 | Internal temporary checkout | Unchanged. |

Gone from Search A: the three `src/superclaude/` sc-recommend files and their three `plugins/superclaude/` copies (Tasks 6-7), and `tests/docs/test_tavily_doc_alignment.py` (Task 8 comment).

## Search B: 9 lines in 7 files (unchanged count)

Every file is classified "Internal temporary checkout" in Task 1: `scripts/eval_runner.py` (line 154, now `git worktree add --detach <temporary directory> master`), `src/superclaude/cli/reflect/config.py`, `tests/cli/reflect/test_isolate_reviewers_cli.py`, `tests/skills/test_implement_retry_revert.py`, `tests/troubleshoot/backtest/git_replay.py`, `tests/troubleshoot/backtest/test_git_replay_unit.py`, `tests/unit/test_ccsession_tag.py`.

`scripts/eval_runner.py` no longer creates a checkout outside a temporary directory: `master_checkout()` uses `tempfile.mkdtemp(prefix="ironclaude-eval-master-")` and removes the checkout with `git worktree remove --force` (scripts/eval_runner.py:144-182).

The new test file `tests/unit/test_eval_runner_master_checkout.py` is untracked, so neither `git grep` search sees it. It contains no `.dev/worktrees` text and no `git worktree add` or `"worktree", "add"` text; if it is tracked later it adds no hit.
