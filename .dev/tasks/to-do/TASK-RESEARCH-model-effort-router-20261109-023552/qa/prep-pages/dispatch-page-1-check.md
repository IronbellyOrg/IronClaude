# Dispatch: 1.1-prep-page-1 independent check (rf-qa verifier)

## Governing source and purpose

Source: item `1.1-prep-page-1 independent check` in repository-root `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/TASK-RESEARCH-model-effort-router-20261109-023552.md`. Executor: person-opened /task session (Run run_c974cafd0eb6). Report-only, fix_authorization false.

TASK_DIR: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`

## Worker contract

Verified Tier1b (claude-gw-tier1b, backend membership in live Tier1b slots: claude-sonnet-5-5, gpt-6.1-sol, muse-wonder-full-1.0). Resolve role text project `.claude/agents/rf-qa.md` first, then installed `/home/coder/.claude/agents/rf-qa.md`; do not edit role definitions. Stub-first incremental writing: Read the role's registered Output Format (All Phases), immediately Write the full QA Report skeleton with explicit placeholders at the output path, then populate one section at a time with Edit. Every Read under 100 lines, every tool output under 40 lines. No source/test/config edits, tests, requests, UV/Python/package commands, installs, cleanup, commits/pushes, publication, SuperClaude-Org interaction, nested workers. You own ONLY your report file.

## Assigned inputs (complete, package-relative)

1. Procedure passage: TASK file lines 140-161 (22 lines), read first after metadata pinning.
2. The six page-1 originals completely: `BUILD-REQUEST.md` (76), `research/research-notes.md` (112), `research/scope-01-launcher-init.md` (138), `research/scope-02-launcher-selection.md` (142), `research/scope-03-proxy.md` (92), `research/scope-04-contracts-tests.md` (107). Total 667 lines.
3. The produced digest `qa/prep-pages/page-1-scope-boundary.md` (194 lines).

Lifetime input at most 1000 lines.

## Deliverable

`qa/prep-pages/page-1-check.md` — adversarial zero-trust QA report:

- Verify every scope-boundary element in each assigned original (owner goal and why, output ownership and canonical output names, every explicit constraint including research-only/preserve-explicit-selections/Coder-role default/Tier1b-policy-not-default/no-SuperClaude-Org/no-private-data/no-forbidden-actions/incident disclosure, seven-phase structure, five local topics with concrete file scope, three external obligations, every distinct MUST/NEVER statement) is preserved in the digest with resolvable file:line citations.
- No dropped constraint, no invented or inflated content, no construction-review acceptance inflated into execution acceptance, no source-inspected claim presented as executed proof.
- Production context note (not your finding to re-litigate): two concurrent producer passes wrote interleaved sections of the digest (duplicate dispatch, both cross-checked each other, logged in the task Execution Log). Verify the merged content on its own merits.
- Findings graded blocking versus minor; binary `VERDICT: PASS` or `VERDICT: FAIL` anchored case-sensitively. A zero-finding verdict requires an active Self-Audit stating exactly what was checked.

Return ONLY your report path and verdict as final output; the executor Reads the report from disk before acceptance.
