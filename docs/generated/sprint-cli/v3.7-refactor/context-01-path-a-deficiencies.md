---
title: "Context Document 1: Path A Deficiencies & Validated Critiques"
generated: 2026-04-03
purpose: Synthesis of all validated issues with the per-task execution path (Path A)
source: Sprint CLI deep analysis conversation, 8 research agents + 6 validation agents
---

# Path A Deficiencies & Validated Critiques

## The Two Execution Paths

The sprint executor at `src/superclaude/cli/sprint/executor.py:1201-1254` has a branching decision:

```python
tasks = _parse_phase_tasks(phase, config)
if tasks:
    # PATH A: per-task subprocess loop (executor.py:1064-1068)
    execute_phase_tasks(tasks, config, phase, ...)
else:
    # PATH B: freeform single-subprocess (process.py:build_prompt())
    ClaudeProcess(config, phase)
```

**Path A** fires for every properly structured tasklist (the production path).
**Path B** fires only when phase files lack `### T<PP>.<TT>` headings (fallback for malformed/legacy files).

All production sprints using `sc-tasklist-protocol`-generated tasklists execute via Path A.

## Validated Deficiency 1: Minimal Per-Task Prompt

**Severity: HIGH** | **Evidence: executor.py:1064-1068**

Path A sends a 3-line prompt per task:
```
Execute task {task.task_id}: {task.title}
From phase file: {phase.file}
Description: {task.description}
```

Missing from prompt (compared to Path B's `build_prompt()`):
- No `@{phase_file}` syntax (file not force-loaded into context)
- No `/sc:task-unified` invocation (skill protocol not activated)
- No scope boundary ("Execute ONLY this task, STOP when complete")
- No sprint context (release name, phase number, artifact root, prior-phase paths)
- No result file contract
- No checkpoint instructions

The `description` field is derived only from the `**Deliverables:**` block (`config.py:362-380`), omitting acceptance criteria, steps, validation commands, tier, dependencies, and rollback instructions — all of which are in the phase file.

**Mitigating factor**: The full task spec IS on disk at the referenced path. Claude workers routinely read referenced files. But this is inference-dependent, not guaranteed.

## Validated Deficiency 2: TurnLedger Reimbursement System Functionally Inert

**Severity: HIGH** | **Evidence: Three compounding bugs**

The TurnLedger economic model (designed as intra-task QA) is architecturally wired but mathematically zeroed out:

### Bug 1: `turns_consumed` always returns 0
- `executor.py:1091-1092`: `return (exit_code, 0, output_bytes)`
- Comment: `# Turn counting is wired separately in T02.06`
- T02.06 does not exist in any current or backlog release spec
- **Effect**: `int(0 * 0.8) = 0` reimbursement for every task

### Bug 2: `TaskResult.output_path` never set
- `executor.py:1017-1025`: `TaskResult(...)` constructed without `output_path`
- `models.py:176`: defaults to `""`
- **Effect**: Anti-instinct gate at `executor.py:826-831` checks `if output_path is not None and output_path.exists()` — always False, vacuously passes

### Bug 3: `gate_rollout_mode` defaults to "off"
- Unless `--shadow-gates` is explicitly passed, mode is "off"
- `executor.py:814-816`: returns immediately without evaluating
- **Effect**: Even if bugs 1-2 were fixed, gate doesn't run by default

### Combined Effect
- Anti-instinct semantic checks (undischarged obligations, uncovered contracts, fingerprint coverage >= 0.7) never execute
- Reimbursement credits are always 0
- Budget exhaustion halts never trigger from quality signals
- The 50 tests from v3.7-TurnLedger-Validation validate correct math on zero inputs

## Validated Deficiency 3: No Evidence Artifact Verification

**Severity: MEDIUM** | **Evidence: executor.py:1017-1036**

Tasklist specs define `**Artifacts (Intended Paths):**` per task (e.g., `TASKLIST_ROOT/artifacts/D-0001/evidence.md`). These are written by the worker (inference layer) during task execution.

The orchestrator never verifies:
- Whether the evidence file was actually written
- Whether deliverable files listed in `**Deliverables:**` exist
- Whether validation commands in `**Validation:**` were run

Post-task hooks check structural code integrity (wiring) and output format (anti-instinct), not task-specific deliverables.

## Validated Deficiency 4: `build_task_context()` Dead in Production

**Severity: MEDIUM** | **Evidence: process.py:245-307, grep across src/**

`build_task_context()` would inject prior task results, gate outcomes, remediation history, and git diff context into subsequent task prompts. It is:
- Fully implemented (process.py:245-307)
- Extensively tested (test_process.py:314+, test_context_injection.py:78+)
- Never called from any runtime code path

## Validated Deficiency 5: Task Dependencies Parsed but Not Enforced

**Severity: LOW** | **Evidence: config.py:342-349, executor.py:956**

`parse_tasklist` extracts `TaskEntry.dependencies` (config.py:342-349, 389-394). `execute_phase_tasks` iterates in document order (executor.py:956: `for i, task in enumerate(tasks)`). No topological sort or dependency check.

## Validated Deficiency 6: No Task-Level Resume

**Severity: LOW** | **Evidence: executor.py:956, models.py:490-497**

`TaskResult` objects accumulate in memory only. No per-task JSONL events. Resume is phase-level only (`--start` flag). No mechanism to skip completed tasks within a restarted phase.

## Validated Deficiency 7: No Per-Task Scope Enforcement

**Severity: LOW** | **Evidence: executor.py:1064-1068**

Per-task prompt contains no scope-limiting language. Worker could read phase file and execute sibling tasks. Subprocess isolation partially mitigates (orchestrator spawns next task regardless), but wasted turns and potential conflicts remain.
