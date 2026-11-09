# T7: l2_status rewrite, launch wiring, remaining old-state hits

File: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (uncommitted; commit B at T8).

## What changed

- `l2_status` (line 1026) is read only: `_l2_preconditions(create=False)`, then the `pre-push` entry check, then `_l2_packaged` (line 1155), then `_l2_entry_verdict`. It never writes, never creates the hooks directory, never runs the hook or the selector (FR-042). States: `owned`, `absent`, `conflict`, `unsupported`. `present-unverified` is gone from the file.
- `install_l2` (line 1335) reports through `l2_status` at S2 (entry exists) and S6 (after publish), mapped by `_l2_as_install` (line 1047): `owned` becomes `installed` (S6) or `owned` (S2), `absent` becomes `unavailable`. This closes T6 findings F1.3 (a raced `absent` at S6 is now `unavailable`) and F1.5 (one path).
- T6 F1.1: a missing packaged hook gives the FR-033 fixed text "the packaged pre-push hook is not installed (run superclaude install)" (`L2_WHY_NOT_INSTALLED`).
- T6 F1.4: the git-2.31 hint is only in `L2_WHY_GIT` (rev-parse failed); a path mismatch says only "git's pre-push hook path is not <hooks>/pre-push".
- FR-033 and OC-10: a config read failure or a git failure is `absent` in `_l2_preconditions` (what `l2_status` reports, FR-041), and `install_l2` maps it to `unsupported`, nothing written (as in T6; review r1-1 F1.1).
- `cmd_launch` (line 1675): source §3.2 steps 4-6 before `publish_pending`: `install_l2(wt)` (advisory), then `l2_status(wt)` (the reported answer), then `W-L2-ABSENT` with `L2_ABSENT_WHY + reason` when the state is not `owned`. The launch proceeds (IR-7 stays a warning; `IR7_REFUSE` itself comes in commit E, owner decision OD-3).
- `session_report(wt, l2, inode)` takes the `(state, reason)` pair and prints `L2 pre-push: owned (...)` or `L2 pre-push: <state> (<reason>; the limits are enforced by the L1 guard only)`.

## Divergences (for commit B's body and owner review)

1. A git or config failure: `l2_status` says `absent` (FR-041), `install_l2` says `unsupported` (FR-033, OC-10). A missing packaged hook, missing uv, or bad data paths: `l2_status` says `absent`, `install_l2` says `unavailable` (FR-031's install states have no `absent`).
2. An unsafe hooks directory: `unsupported` in both functions, while FR-041 lists it under `absent` (OC-9 choice kept from T6).
3. With no `pre-push` entry, `l2_status` reports `absent` "no pre-push hook" even when the packaged hook is also missing; the entry check runs first because no entry means no L2 regardless of the package.
4. An owned `pre-push` entry whose data file is missing reports `conflict` `data-file-differs` in both functions (for commit B's OC-12 note).

## Remaining old-state hits outside the file (fixed in T8)

- `src/superclaude/skills/sc-issue-protocol/refs/claim.md:120` (`present-unverified` in the launch JSON description) and `:127` (W-L2-ABSENT remedy "the L2 layer is not built yet").
- `tests/skills/test_issue_orca_worktree.py:1672`, `:1691`, `:1692` (`present-unverified` expectations), `:1728` and `:1746` ("L2 layer is not built yet"), `:1745` ("no executable pre-push hook").

## Tests (`uv run pytest tests/skills/test_issue_orca_worktree.py`): 6 failed, 157 passed

All six are the expected old-wording or old-state assertions above, rewritten in T8:

- `test_ir6_l2_status_follows_the_git_hook_path[no-file-absent]`, `[not-executable-absent]`: remedy text "L2 layer is not built yet".
- `[foreign-executable-present-unverified]`: now `absent` here (the test home has no packaged hook), expected `present-unverified`.
- `[hooks-path-present-unverified]`, `[hooks-path-elsewhere-absent]`: now `unsupported` (OC-6).
- `test_ir7_l2_absent_warns_and_the_launch_proceeds`: reason "no executable pre-push hook" and remedy wording.

## Smoke evidence (`./t7-smoke.py`, temp HOME and temp repo)

```
no-hooks-dir: status=('absent', 'no pre-push hook')
no-hooks-dir created: False
no-hook: status=('absent', 'no pre-push hook')
first: install=('installed', '') status=('owned', '')
second: install=('owned', '') status=('owned', '')
data-differs: install=('conflict', 'data-file-differs: ...') status=('conflict', 'data-file-differs: ...')
foreign: install=('conflict', 'foreign: ...') status=('conflict', 'foreign: ...')
no-packaged: install=('unavailable', 'the packaged pre-push hook is not installed (run superclaude install)') status=('absent', 'no pre-push hook')
hookspath: install=('unsupported', 'core.hooksPath is set, ...') status=('unsupported', 'core.hooksPath is set, ...')
linked: install=('installed', '') status=('owned', '')
linked in common dir: True
not-a-repo: install=('unsupported', 'git-failed: git rev-parse failed (...)') status=('absent', 'git-failed: git rev-parse failed (...)')
```
