# /sc:analyze report: src/superclaude/cli/issue_watch (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:47:23Z; degraded: none

Target: `src/superclaude/cli/issue_watch` (15 Python files, 6,892 lines), the watcher half of the chain issue 777 asks to map. The coordinator half lives in `src/superclaude/cli/issue_pipeline/` (read for context only).

## Layout (codegraph_files, confirmed by `wc -l`)

| File | Lines | Role |
|---|---|---|
| cycle.py | 1544 | one watcher pass: reads candidates, applies predicates, claims |
| github.py | 1158 | GitHub reads and writes for the watcher |
| record.py | 865 | claim store (`dispatch.json`) read/write |
| cli.py | 518 | CLI entry points |
| dispatch.py | 504 | dispatcher across repositories (`run-all`) |
| launch.py | 416 | claim launch prompt, pipeline level, ship gate |
| predicates.py | 360 | trigger and approval predicates |
| audit.py, generate.py, first_run.py, defaults.py, repos.py, repo_init.py, runner.py | 130-406 | support |

## Findings

1. **INFO, architecture: the ship gate is a code constant.** `src/superclaude/cli/issue_watch/launch.py:48` sets `GOVERNED_LEVELS_ALLOWED = False`; the docstring at lines 49-53 says only Pipeline None launches while it is False and that no config key or environment variable flips it. This is one of the pieces issue 777 lists ("the ship gate").
2. **INFO, architecture: the pipeline value maps to a `--pipeline` argument** at `launch.py:55-61` (`None`/`None` to `none`, `Worktree`, `Full`, `Full Submit` to `full --submit`).
3. **INFO, architecture: the coordinator side has separate verbs** in `src/superclaude/cli/issue_pipeline/cli.py`: `plan-hash` (62), `check-approval` (77), `adopt-create` (109), `adopt-mark` (118), `record-create` (135), `record-mark` (180), `complete` (226), `stage-status` (409). Together with the watcher's `dispatch.json` store these are the "two stores" the issue names.
4. **MEDIUM, quality: three files hold 3,567 of 6,892 lines** (cycle.py, github.py, record.py). Not a defect for issue 777; it is why a written map is useful. Lead only.

No source file was modified. This quick run found nothing that changes the issue's scope.
