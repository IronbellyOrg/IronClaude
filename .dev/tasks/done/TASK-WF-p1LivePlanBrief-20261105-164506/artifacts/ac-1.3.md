# AC-1.3 flagless file-creation check (spec 7.3 AC-1.3, file-creation part)

Result (file creation): **PASS**. Both print-mode runs completed (exit code 0) and `ac13-find-diff.txt` is empty: neither a plain `/sc:analyze` nor a plain `/sc:explain` created a `return-contract.yaml` in the scratch worktree.

Setup and cleanup: scratch worktree `p1-live-flagless` created by `orca worktree create ... --no-parent` (`ac13-worktree.json`, branch `ac13-branch.txt`, `make sync-dev` output `ac13-sync-dev.txt` rc 0); HEAD equalled `branch-tip.txt` at creation. Removal: `ac13-remove.json` (`removed: true`), `ac13-worktree-list-after.json` does not list `p1-live-flagless`, and the feature worktree's HEAD is unchanged (`ac13-head-after.txt` equals `branch-tip.txt`).

Evidence files:
- Status: `ac13-status-before.txt` (empty), `ac13-status-after-1.txt` (empty), `ac13-status-after-2.txt` (empty): neither run left any file in the worktree.
- Contract-file listings: `ac13-find-before.txt` (325 tracked files, the baseline), `ac13-find.txt` (325 files), `ac13-find-diff.txt` (empty).
- Runs (each `timeout 1200 claude -p "<command>" --max-budget-usd 2 --permission-mode acceptEdits`, started in the worktree): `ac13-run-1.txt` (`/sc:analyze src/superclaude/cli/install_core.py --depth quick`) and `ac13-run-2.txt` (`/sc:explain src/superclaude/cli/install_core.py --level basic`).

Tail output of run 1 (`ac13-run-1.txt`):

```text
**1. Medium: Destination setup errors escape the result contract.** At `src/superclaude/cli/install_core.py:55`, creating the destination happens outside error handling. A permission-denied directory or an existing file at that path raises an exception instead of returning the documented `(success, message)` result.

**2. Medium: Forced installation can damage an existing file before reporting failure.** At `src/superclaude/cli/install_core.py:74`, copying writes directly to the destination. A failed write, such as running out of disk space, can leave existing instructions truncated; catching the exception does not restore them.

**Recommended action:** Handle destination creation errors and copy through a temporary sibling file before replacing the destination, with regression tests for both failure paths.

Skipped runtime execution and tests because this command requests static analysis. The findings are source-backed, but their failure paths were not reproduced.
claude run 1 rc=0
```

Tail output of run 2 (`ac13-run-2.txt`):

```text
- **Copy them:** The main installation function creates the destination folder, normally `~/.claude/`, then copies each document there (`src/superclaude/cli/install_core.py:31`).
- **Protect existing files:** It skips files already present unless `force=True` allows replacement. Replacement can overwrite personal changes (`src/superclaude/cli/install_core.py:69`).
- **Report the result:** It returns a success value plus a message listing installed, skipped, and failed files. All files being skipped still counts as success (`src/superclaude/cli/install_core.py:79`).
- **Provide inventories:** Two helpers list available documents and installed documents. The installed list includes only filenames in the predefined known-files list (`src/superclaude/cli/install_core.py:129`).

**Recommended action:** None needed for this explanation.
Not checked: a live installation or tests. This explains the source behavior, not a verified installation run.
claude run 2 rc=0
```

Open owner item (the manual part of AC-1.3, not run by this plan): "run `/sc:analyze <path>` and `/sc:explain <path>` in a plain interactive Claude Code session and in the coordinator session with `WORKER-CONTRACT.md` loaded, and confirm that today's prompts and defaults appear and that no brief-guard refusal occurs".

Recording status: complete (verdict recorded, not a task failure)
