# Option A: three focused commands (impact, test-scope, graph)

Read `context.md` first. Candidates come from the brainstorm's K-2, K-3, K-4 (`.dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/merged-requirements.md` §6).

## Commands

1. `/sc:impact <symbol> | --file <path> | --diff [<base>]` `[--depth 1-3] [--limit N] [--tests] [--output-dir <dir>] [--caller <name>]`: dependents of a symbol, file or diff, split into production and test callers; each cited row re-Read. Writes `<output-dir>/impact.md` (human) and `<output-dir>/return-contract.yaml` (machine).
2. `/sc:test-scope --files <list> | --diff [<base>]` `[--depth N] [--output-dir <dir>] [--caller <name>]`: changed files → tests: today's path heuristic plus `codegraph affected`, as an advisory superset with the source of each test recorded. Writes `test-scope.md` + `return-contract.yaml`.
3. `/sc:graph [status|init]`: index readiness for this worktree (state, version, counts, next action) and the only place `codegraph init --yes` runs, and only when the user typed `init`. Writes `return-contract.yaml` when `--output-dir` is given.

Shared rules (readiness labels, read-before-cite, fail-open) live in the core guide `~/.claude/CODEGRAPH.md`, not in a skill.

## Callers

- `/sc:impact`: sc-implement-protocol Q1 (rename/delete/signature tasks), sc-task-protocol STRICT step 7, sc-troubleshoot-protocol `--fix` handoff, sc-pr-submit-protocol Wave 4, sc-auggie-review-protocol Wave 1 (blast radius context), sc-reflect-protocol 1B.3, sc-workflow-protocol (informational).
- `/sc:test-scope`: sc-implement-protocol Q6 extras, sc-pr-submit-protocol VG-1 (advisory), sc-reflect-protocol UC-2, `/sc:impact --tests`, `/sc:test`.
- `/sc:graph status`: every caller above as its readiness probe; users.

## Strengths

- Each command has one job and one contract; easy to test and to call.
- `test-scope` is reusable by callers that do not need dependents.
- Readiness and init have a single owner.

## Weaknesses

- Three command files, three protocol skills (or three self-contained commands), three test files, three sets of docs and `tests/unit/test_cli_install.py` entries.
- `/sc:impact --tests` duplicates `/sc:test-scope` unless it calls it.
- `affected` was never run in EVAL; `test-scope` value is unmeasured.
