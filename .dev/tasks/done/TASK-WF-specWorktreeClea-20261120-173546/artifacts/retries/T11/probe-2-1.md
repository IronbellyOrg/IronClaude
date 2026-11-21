279eeef4a0fe7a43f5fea61dff96307e813d8ebc
family: orca-readback-unlisted-skip
defect form: the read back runs a list command and then ignores its reply for a worktree that had no row before the removal
command: grep -n -E "orca_lists|orca is None|orca is not None" scripts/worktree_cleanup.py
before: _read_back returns None when orca is None right after running the Orca list (scripts/worktree_cleanup.py around line 2525); orca_lists takes the id as a plain argument
coupled sites: _read_back, orca_lists, the read back tests in tests/worktree_cleanup/test_removal.py (they all use a worktree Orca listed or default replies)
after (attempt 3):
2524:    still = orca_lists(
2532:def orca_lists(text: str, path: str, worktree_id: str) -> bool | None:
