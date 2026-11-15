# Dispatch: 1.1-prep reconciliation producer

## Governing source and purpose

Source: item `1.1-prep reconciliation producer` in repository-root `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/TASK-RESEARCH-model-effort-router-20261109-023552.md`. Executor: person-opened /task session (Run run_c974cafd0eb6). Produce-only. Both page checks are independently PASS (page-1-check.md line 70, page-2-check.md line 58).

TASK_DIR: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`

## Worker contract

Verified Tier1b (claude-gw-tier1b; live slots claude-sonnet-5-5, gpt-6.1-sol, muse-wonder-full-1.0). Stub-first incremental writing: immediately Write the full header/section skeleton with explicit placeholders at the output path BEFORE content gathering, then populate one section at a time with Edit. Every Read under 100 lines, every tool output under 40 lines. No edits outside your output; no tests, requests, UV/Python/package commands, installs, cleanup, commits/pushes, publication, SuperClaude-Org interaction, nested workers.

## Assigned inputs (complete, package-relative; measured)

1. Procedure passage first (after metadata pinning): TASK file lines 140-161 (22 lines).
2. `qa/prep-pages/page-1-scope-boundary.md` (194 lines) — accepted.
3. `qa/prep-pages/page-2-construction-gates.md` (127 lines) — accepted.
4. `qa/prep-pages/page-1-check.md` (72 lines) — PASS.
5. `qa/prep-pages/page-2-check.md` (58 lines) — PASS.

Total 451 + 22 = 473 lines; within the 1000-line lifetime budget.

## Deliverable

`qa/prep-pages/reconciliation.md`: a lossless merge of the two accepted digests preserving every distinct scope-boundary and construction-gate element exactly once; deduplicate repeated wording only, never unique meaning. Include:

- an exhaustive input-element-to-output-location map (each element of both digests mapped to its section in the reconciliation)
- any cross-page contradictions retained verbatim under a `CONTRADICTION:` marker citing both sources (do not resolve them)

Source-cite lineage to the page digests. Return ONLY the output path plus a one-line completion statement; the executor Reads it from disk before acceptance.
