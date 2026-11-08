# Git baseline (Step 1.3), recorded 2026-11-07

| Command | Output |
|---|---|
| `git rev-parse --abbrev-ref HEAD` | `ironbelly/issue-331-github-issue-watcher` |
| `git rev-parse HEAD` | `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b` |
| `git rev-parse --verify origin/master` | `2b3ae7e7516917c981cf1134528cf92b3de65e01` |
| `git merge-base HEAD origin/master` | `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b` |
| `git diff --cached --name-only` | 161 staged paths (all under `.dev/tasks/`) |

- The branch name is not `master` or `main`.
- 161 paths are staged and none of them starts with `.claude/`.
- Difference from R-003: R-003 recorded origin/master as `0b8a5801d75f159bcbca7087b99507c2a50d8dba`; today it is `2b3ae7e7516917c981cf1134528cf92b3de65e01` (the fork master has moved ahead of the merge-base `e8db2fe6`; a rebase onto origin/master is a later PR-step concern, not part of this task). The merge-base equals the R-003 value.
- This baseline is not BASE; BASE is captured in Step 10.2.
