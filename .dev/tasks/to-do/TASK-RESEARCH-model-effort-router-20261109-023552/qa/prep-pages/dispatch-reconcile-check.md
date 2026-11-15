# Dispatch: 1.1-prep reconciliation independent check (rf-qa verifier)

## Governing source and purpose

Source: item `1.1-prep reconciliation independent check` in repository-root `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/TASK-RESEARCH-model-effort-router-20261109-023552.md`. Executor: person-opened /task session (Run run_c974cafd0eb6). Report-only, fix_authorization false.

TASK_DIR: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`

## Worker contract

Verified Tier1b (claude-gw-tier1b; live slots claude-sonnet-5-5, gpt-6.1-sol, muse-wonder-full-1.0). Resolve role text project `.claude/agents/rf-qa.md` first, then installed `/home/coder/.claude/agents/rf-qa.md`. Stub-first incremental writing: Read the role's registered Output Format, immediately Write the full QA Report skeleton with placeholders, then populate one section at a time. Every Read under 100 lines, every tool output under 40 lines (the producer disclosed exceeding the 40-line output cap on some reads; you must not). No edits outside your report; no tests, requests, UV/Python/package commands, installs, cleanup, commits/pushes, publication, nested workers.

## Assigned inputs (complete, package-relative; measured)

1. Procedure passage: TASK file lines 140-161 (22 lines), read first.
2. `qa/prep-pages/page-1-scope-boundary.md` (194)
3. `qa/prep-pages/page-2-construction-gates.md` (127)
4. `qa/prep-pages/page-1-check.md` (72)
5. `qa/prep-pages/page-2-check.md` (58)
6. `qa/prep-pages/reconciliation.md` (481)

Total 954 lines including procedure passage; within the 1000-line lifetime budget.

## Deliverable

`qa/prep-pages/reconcile-check.md` — adversarial zero-trust verification that the reconciliation is lossless: every distinct element of both accepted digests survives in it with correct lineage, no false dedup (two elements merged that differ in meaning), no dropped CONTRADICTION marker, and every element-map entry resolves to real reconciliation content. Binary `VERDICT: PASS` or `VERDICT: FAIL`; zero-finding verdict requires an active Self-Audit stating what was checked. Return ONLY your report path and verdict; the executor Reads the report from disk before acceptance.
