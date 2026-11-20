6773b49565ded7b521ed636b04a56ef4a2314ce0
# T18 review 1

Reviewed the live files whole:
- /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/repos.py
- /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/tests/issue_watch/test_repos.py
- the "repos" row of /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/tests/issue_watch/test_module_boundaries.py (line 75: `"repos": Rule(siblings=frozenset({"runner", "launch"}))`)

Run: `uv run pytest tests/issue_watch/test_repos.py tests/issue_watch/test_no_shell.py tests/issue_watch/test_module_boundaries.py -q` gave 143 passed.

## Earlier blocking findings

None were passed in (first review).

## Acceptance criteria

- T18.AC1 met. T18.AC1@tests/issue_watch/test_repos.py:49 (six repos, one in /tmp, with the other two skips reported); :71 (non-GitHub origin skipped); :80 (foreign owner skipped, allowed owner matched in any case); :98-113 (failed list raises: returncode 1, 127 and spawn error, and the timed-out case at :104 raises `list_timeout`); :133-137 (empty but successful list returns no repos and no skips). Failure is raised at src/superclaude/cli/issue_watch/repos.py:121-124; output that cannot be read raises at repos.py:84-88.
- T18.AC2 met. T18.AC2@src/superclaude/cli/issue_watch/repos.py:20-28 (imports only re, collections.abc, dataclasses, pathlib, and the siblings `launch` and `runner`; no subprocess); every command goes through `runner.run` with an argv list (repos.py:99-100, 120). The boundary row at tests/issue_watch/test_module_boundaries.py:75 allows exactly those two siblings. The tests in test_no_shell.py and test_module_boundaries.py pass. The module also has its own no-shell test at tests/issue_watch/test_repos.py:208.

## Other checks against the task text

- Record fields (Orca id, name, path, owner/name from origin): repos.py:46-53.
- Skip reasons: /tmp at repos.py:72-74 and 132-134 (the part check keeps /tmpfoo, /var/tmp and /home/u/tmp, which are tested at test_repos.py:176-185); non-GitHub origin at :138-139 via `launch.parse_origin` (launch.py:256); foreign owner at :140-141, case-insensitive. The allowed owners are passed in by the caller (default tuple at defaults.py:30), so the "allowed owners of Task 17" link holds.
- Format parsed as `<id>  <name>  <path>` with maxsplit 2, so a path with spaces is kept (test_repos.py:152 area, `test_a_path_with_spaces...`).

## Findings

None blocking.

F1.1 ac=scope at=src/superclaude/cli/issue_watch/repos.py:83 anchor=`_FIELDS.split(line, maxsplit=2)` chk=n,n,n,n family=minor-parse fix=none needed now; a repo name that itself holds two or more spaces would split wrongly and the line would then fail the path check and raise `unreadable_list` (a loud failure, not a silent skip) [covers=none]: observation only, not blocking.
