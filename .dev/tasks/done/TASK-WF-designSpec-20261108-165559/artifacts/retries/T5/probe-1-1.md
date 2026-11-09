fb76413587f3c0bc91b8e0f5ae9c3009038ffef1

## family=commit-a-missing (F1.1)

- defect form: Task 5 ends with local commit A, but the review ran before the commit, so `git show --stat HEAD` still shows the start commit 5dc29d23.
- command: `git log -1 --format=%H HEAD` and `git status --porcelain -- <rows 1-9>`
- before:
  - HEAD = 5dc29d23b15eb7db4ead50623bb409f696a0d7d3 (the T5 q0-head)
  - rows 1-9: the two launch-level-pre-push.sh copies and the records test are untracked; the other six rows are modified and unstaged.
- coupled sites: none outside rows 1-9 and `.dev/tasks`; `.claude/` mirrors from `make sync-dev` are gitignored and must stay unstaged.

## family=format (F1.2, minor)

- defect form: `ruff format --check` reported the records test file would be reformatted (parametrize at :133).
- command: `uv run ruff format tests/hooks/test_launch_level_pre_push_records.py`
- after: 1 file reformatted (fixed before commit A).
