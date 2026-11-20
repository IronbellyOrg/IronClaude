# Fixtures for the worktree cleanup tests

Every file here is a small made-up reply, written by hand from the spec and the tool help.
None is a literal capture of a real workspace: the paths, ids, titles and numbers are
examples (the same stance as `tests/merged_pr_log/test_merged_pr_log.py`).

One recorded shape for each of the seven replies the script reads:

- `gh_pr_list.json`: `gh pr list --repo <owner>/<repo> --head <branch> --state all --json ...`
- `gh_pr_view.json`: `gh pr view <N> --repo <owner>/<repo> --json state,mergedAt`
- `gh_issue_view.json`: `gh issue view <N> --repo <owner>/<repo> --json state`
- `orca_repo_list.json`: `orca repo list --json`
- `orca_worktree_ps.json`: `orca worktree ps --json` (a reply envelope with `ok` and
  `result.worktrees`). The field names are the ones seen in a real reply during the survey
  for issue 687 (`worktreeId`, `path`, `lastActivityAt`, `isPinned`, `liveTerminalCount`,
  `linkedPR`, `comment`); the values are not.
- `orca_reference_list.json`: `orca reference list --worktree <selector> --json`
- `orca_terminal_list.json`: `orca terminal list --worktree <selector> --json`

The three Orca shapes other than `worktree ps` are UNVERIFIED against a real reply (no
real one was captured), so the parsers read them tolerantly and report "Orca unavailable"
for anything else.

Do not put a real path, name or token in these files.
