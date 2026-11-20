e3bf3867225640604102a3659be325fa6aaa2858
# Review 1 of Task 21 (first-run check)

Evidence: read /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/first_run.py and tests/issue_watch/test_first_run.py; ran `uv run pytest tests/issue_watch/test_first_run.py tests/issue_watch/test_module_boundaries.py -q` (93 passed). Both new files are untracked on disk; they were read directly.

## Earlier blocking findings
None (first review).

## AC marks
- T21.AC1: met. T21.AC1@tests/issue_watch/test_first_run.py:148 (all pass gives enabled true, steps all ok, mode 600), :174 (missing worktree: enabled false, `worktree_invalid` and "first-run: failed config" in report, line 180), :185 (dry-run failure keeps false), :213 and :220 (held lock detected; a cycle that ends 0 under the lock fails with `lock_not_detected`), :239 (corrupt dispatch.json fails restart with `state_not_reloadable`), :256 (store changed by second dry run fails restart), :274 (second run changes nothing: `already_enabled`, config and store bytes equal, no further calls), :299 (closed gate line and `approver_is_launch_account` warning in the report). Implementation: src/superclaude/cli/issue_watch/first_run.py:125-252 (order config, label, init_state, dry_run, lock, restart; `_enable` at :98 sets `enabled: true` only from `done(None)` at :149-153).
- T21.AC2: met. T21.AC2@tests/issue_watch/test_first_run.py:75-97 and :100-139 (Router and Harness take every external call through the fake runner or GhWorld; FakeLauncher records launches), :142-145 (asserts no launches, no home dir under tmp, no orca argv), autouse HOME/XDG redirect into tmp_path. Source runs no process of its own (first_run.py takes `runner` and `deps_factory`).

## Spec details checked
- Lock test uses the store lock of record.py: first_run.py:226-228 holds `store.lock()` and expects exit 75 (`LOCK_HELD_EXIT`).
- Failure leaves `enabled: false` and writes a one-line reason: first_run.py:158-170, report file name `first-run.txt` (first_run.py:41) in the state dir.
- Report states the ship gate from `launch.GOVERNED_LEVELS_ALLOWED` (first_run.py:163-169) and the launch-account warning (first_run.py:187-190); the warning respects `approval_excluded_ids`, consistent with Task 9.
- Idempotent: already enabled returns before any check (first_run.py:136-137); an existing store is kept via `StateExists` (first_run.py:209-210).
- No harmful write found: writes are the config's own atomic rewrite, the report file and `init_state` of the repo's own state dir; `.claude/` untouched.

## Findings
F1.1 ac=scope at=tests/issue_watch/test_first_run.py:142 anchor=assert not (tmp_path / "home").exists() chk=n,n,n,n family=test-strength fix=also snapshot the real home (or assert the real HOME env was never read) if a stronger proof of "nothing written under the real home" is wanted: non-blocking, observation only because HOME is redirected and nothing can write there in these tests.

No blocking findings.
