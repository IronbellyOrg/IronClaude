279eeef4a0fe7a43f5fea61dff96307e813d8ebc
family: orca-readback-substring
defect form: a list read back is searched as plain text, so a name that is a prefix of another matches
command: grep -n -E "in seen\.stdout|in listed\.stdout|\.stdout\)" scripts/worktree_cleanup.py
before:
2525:    if orca is not None and (wt.path in seen.stdout or orca.worktree_id in seen.stdout):
coupled sites: _read_back git side compares parsed entries by equality (normpath) and is not affected; the Orca read back is the only plain text search; test_removal.py read back tests
after:
1200:def _first_line(text: str) -> str:
2334:def _refusal_text(text: str) -> str:
2452:                f"clearing the saved files failed: {_refusal_text(cleared.stderr)}",
2466:        why = _refusal_text(removal.stderr or removal.stdout)
2502:    return f"kept ({_refusal_text(res.stderr)})"
2527:    still = orca_lists(seen.stdout, wt.path, orca.worktree_id)
2533:def orca_lists(text: str, path: str, worktree_id: str) -> bool | None:
