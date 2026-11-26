# pre-commit spike (Task 2, FR-118)

Question: does the hook emulator in `tests/vcs/conftest.py` behave like the real pre-commit framework?

## Run

- Date: 2026-11-26. Network was available.
- Command: `uv run --with pre-commit pytest tests/vcs/test_precommit_spike.py -q -p no:cacheprovider -rs -v` (uv puts the `pre-commit` script on PATH for that run only).
- Framework: pre-commit 4.6.2 from PyPI (`importlib.metadata.version("pre-commit")`), Python 3.10.20, git 2.47.3.
- Source copied by the emulator: `pre_commit/staged_files_only.py` of that release (functions `_unstaged_changes_cleared`, `_git_apply`, constant `_CHECKOUT_CMD`). The package has no git revision; the release number is the revision name.
- The real framework ran a `repo: local` hook with `language: system` (no network needed) that calls the same action script as the emulator.

## Outcome: it ran

Result: `7 passed in 3.94s`. Six scenarios gave identical results from the emulator and the real framework (exit status, whether HEAD moved, contents of a.txt, b.txt and c.txt, number of saved patch files):

- success with an unstaged edit outside the commit set (one patch saved, edit restored)
- hook exits 1
- hook rewrites a file in the commit set and exits 1
- hook rewrites the file and stages it
- assume-unchanged edit together with another unstaged edit (the hidden edit is overwritten, nothing saved for it)
- assume-unchanged edit alone (left alone, because the framework only checks out when its diff is not empty)

A seventh test sends SIGKILL to the process group while the hook is blocked: on both sides HEAD is unchanged, the work tree file is back to its committed content, and the person's edit exists only in the saved patch.

Without `pre-commit` on PATH the module is skipped (`SKIPPED [1] ... pre-commit is not on PATH`), and `uv run pytest tests/vcs -q --strict-markers` reports no unregistered marker.

## Finding that differs from the task text

The task says an edit to an assume-unchanged file is overwritten "even without a kill". That is true only when another unstaged change exists, so the framework's diff is not empty and its `git checkout -- .` runs. With only the assume-unchanged edit, nothing happens to it (git 2.47.3). The tests cover both cases.

## Not covered (UNVERIFIED)

Other pre-commit versions, other git versions, SIGTERM variants, timeouts, stale locks, skip-worktree edits, mode changes and the intent-to-add step (not replayed by the emulator). These belong to later tasks (T-20).
