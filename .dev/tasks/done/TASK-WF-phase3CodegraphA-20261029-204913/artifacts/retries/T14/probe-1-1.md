afc00365c1d9af67f58ee0273d6b841fc0156dd0
family=group-comment-rows
defect form: a group comment that omits decision-log rows of its group
command: grep -n -F -e "| T13 |" -e "| T14 |" -- .dev/codegraph-migration/decisions/P3X-execution-log.md
before:
82:| 2026-10-31 | T13 | Run the `sync-dev` and `verify-sync` recipes with a small runner (`artifacts/t13-mkrun.py`) beca
83:| 2026-10-31 | T13 | Live smoke fix: `Edit` added to the `allowed-tools` of `sc-impact-protocol` and `sc-graph-protoc
84:| 2026-10-31 | T13 | The troubleshoot smoke's evidence comes from a fresh session told to follow this branch's dev sk
85:| 2026-10-31 | T13 | The Task 13 commit also holds `CHANGELOG.md` and `docs/user-guide/mcp-installation.md` (and `.de
86:| 2026-10-31 | T13 | `tests/commands/test_graph_command.py` keeps its existing `ruff format` difference (from Task 8;
87:| 2026-10-31 | T14 | Pre-PR check: `origin` and `gh repo view` both name `IronbellyOrg/IronClaude`; `origin/master` i
88:| 2026-10-31 | T14 | The two smoke `/sc:troubleshoot` run directories and the counter files they created (`.dev/troub
89:| 2026-10-31 | T14 | `/sc:pr-submit --monitor 3` round 1: the Augment review on `4dc5cd9b` raised 4 Medium findings i
90:| 2026-10-31 | T14 | The fix commit also runs `ruff format` on six Phase 3 test files (`test_codegraph_rosters.py`, `
91:| 2026-10-31 | T14 | Monitor VAL gate VG-2 ("cross-cutting change → `make test`", triggered by the guide edit) ran 
92:| 2026-10-31 | T14 | The troubleshoot dispatch ran the installed (pre-Phase-3) skill: its closed analyst roster rejec
93:| 2026-10-31 | T14 | Monitor run 1 ended `terminal_clean` (CI on `b356399c`: 6 checks passed); the Step 6 record comm
coupled sites: .dev/codegraph-migration/progress/P3-G.md Decisions list; posted comment 6546090554
after:
82:| 2026-10-31 | T13 | Run the `sync-dev` and `verify-sync` recipes with a small runner (`artifacts/t13-mkrun.py`) beca
83:| 2026-10-31 | T13 | Live smoke fix: `Edit` added to the `allowed-tools` of `sc-impact-protocol` and `sc-graph-protoc
84:| 2026-10-31 | T13 | The troubleshoot smoke's evidence comes from a fresh session told to follow this branch's dev sk
85:| 2026-10-31 | T13 | The Task 13 commit also holds `CHANGELOG.md` and `docs/user-guide/mcp-installation.md` (and `.de
86:| 2026-10-31 | T13 | `tests/commands/test_graph_command.py` keeps its existing `ruff format` difference (from Task 8;
87:| 2026-10-31 | T14 | Pre-PR check: `origin` and `gh repo view` both name `IronbellyOrg/IronClaude`; `origin/master` i
88:| 2026-10-31 | T14 | The two smoke `/sc:troubleshoot` run directories and the counter files they created (`.dev/troub
89:| 2026-10-31 | T14 | `/sc:pr-submit --monitor 3` round 1: the Augment review on `4dc5cd9b` raised 4 Medium findings i
90:| 2026-10-31 | T14 | The fix commit also runs `ruff format` on six Phase 3 test files (`test_codegraph_rosters.py`, `
91:| 2026-10-31 | T14 | Monitor VAL gate VG-2 ("cross-cutting change → `make test`", triggered by the guide edit) ran 
92:| 2026-10-31 | T14 | The troubleshoot dispatch ran the installed (pre-Phase-3) skill: its closed analyst roster rejec
93:| 2026-10-31 | T14 | Monitor run 1 ended `terminal_clean` (CI on `b356399c`: 6 checks passed); the Step 6 record comm
