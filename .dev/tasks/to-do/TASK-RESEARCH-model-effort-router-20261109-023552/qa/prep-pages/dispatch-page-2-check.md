# Dispatch: 1.1-prep-page-2 independent check (rf-qa verifier)

## Governing source and purpose

Source: item `1.1-prep-page-2 independent check` in repository-root `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/TASK-RESEARCH-model-effort-router-20261109-023552.md`. Executor: person-opened /task session (Run run_c974cafd0eb6). Report-only, fix_authorization false.

TASK_DIR: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`

## Worker contract

Verified Tier1b (claude-gw-tier1b; live slots claude-sonnet-5-5, gpt-6.1-sol, muse-wonder-full-1.0). Resolve role text project `.claude/agents/rf-qa.md` first, then installed `/home/coder/.claude/agents/rf-qa.md`. Stub-first incremental writing: Read the role's registered Output Format, immediately Write the full QA Report skeleton with placeholders at the output path, then populate one section at a time. Every Read under 100 lines, every tool output under 40 lines. No edits outside your report; no tests, requests, UV/Python/package commands, installs, cleanup, commits/pushes, publication, SuperClaude-Org interaction, nested workers.

## Assigned inputs (complete, package-relative)

1. Procedure passage: TASK file lines 140-161 (22 lines), read first after metadata pinning.
2. The six page-2 originals completely: `qa/analyst-completeness-report.md` (115), `qa/analyst-cross-validation-report.md` (56), `qa/qa-research-evidence-report.md` (61), `qa/qa-research-gap-report.md` (56), `qa/qa-research-depth-report.md` (75), `qa/qa-builder-research-gate-consolidated.md` (62). Total 425 lines.
3. The produced digest `qa/prep-pages/page-2-construction-gates.md` (127 lines).

Lifetime input at most 1000 lines.

## Deliverable

`qa/prep-pages/page-2-check.md` — adversarial zero-trust QA report verifying every gate verdict/scope/deferral boundary/minor note/unresolved conflict in each original is preserved in the digest with resolvable file:line citations; nothing invented; no construction review inflated into execution acceptance. The producer flagged one classification mismatch (evidence report counts 0 minor versus the consolidated report carrying its process note as minor) — verify how the digest records it (it must be recorded, not silently resolved). Findings graded blocking versus minor; binary `VERDICT: PASS` or `VERDICT: FAIL`; zero-finding verdict requires an active Self-Audit stating what was checked. Return ONLY your report path and verdict; the executor Reads the report from disk before acceptance.
