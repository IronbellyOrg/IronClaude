# Option C: two commands (impact with tests, graph) and the core guide as the seam

Read `context.md` first.

## Commands

1. `/sc:impact <symbol>... | --diff [<base>]` `[--depth 1-3, default 2] [--limit N, default 20] [--tests] [--output-dir <dir>] [--caller <name>]`: for symbols or a diff, list definitions, production and test dependents (callers + impact), call sites confirmed by Grep inside the caller and Read, and with `--tests` the test files from `codegraph affected` plus the path heuristic. Writes `impact.md` + `return-contract.yaml`. With no codegraph or no index it returns `status: partial` with Grep-based results and `degraded: [codegraph]`, never stops the caller.
2. `/sc:graph [status|init] [--output-dir <dir>]`: readiness (state, version, counts, next action) and the only place `codegraph init --yes` runs, only when the user typed `init`. Callers use `/sc:graph status --output-dir <dir>` (or simply read the guide's one-call readiness check) as their probe.

No new skill for shared semantics: readiness labels, read-before-cite, fail-open and the call-site rule are written once in `~/.claude/CODEGRAPH.md` (core guide); each command's protocol cites it.

## Callers

- `/sc:impact`: sc-implement-protocol Q1 and Q6, sc-task-protocol STRICT step 7, sc-troubleshoot-protocol `--fix`, sc-pr-submit-protocol Wave 4 and VG-1 (advisory tests), sc-auggie-review-protocol Wave 1, sc-reflect-protocol 1B.3 and UC-2, sc-workflow-protocol (informational).
- `/sc:graph status`: users; referenced by `/sc:load` and by the guide's "not initialized" message.

## Strengths

- Smallest new surface that covers impact, test selection and index ownership; two command files and two test files.
- One contract for all dependent and test questions; callers learn one interface.
- No per-run skill invocation and no shell parser; the guide is already planned (spec §4).

## Weaknesses

- `/sc:impact` is larger (two jobs: dependents and tests).
- No dedicated resolver script: call-site confirmation is a written procedure (Grep inside the caller's span, then Read), less mechanical than a script.
- A caller that only wants tests still calls `/sc:impact --tests`.
