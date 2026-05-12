---
title: Sprint CLI - Critique Validation Report
generated: 2026-04-03
scope: Validation of 6 specific claims against codebase evidence
---

# Critique Validation Report

Six claims about the Sprint CLI pipeline were investigated by independent agents comparing each assertion against source code evidence. Results below.

## Summary Table

| # | Claim | Verdict | Key Nuance |
|---|-------|---------|------------|
| 1 | Tasklist held only in memory, never serialized | **PARTIALLY VALID** | Task list itself is in-memory; task-derived data (IDs) persisted via remediation log |
| 2 | Worker prompt is minimal 3 lines, lacks acceptance criteria | **VALID (with context)** | Per-task prompt is indeed 3 lines, but full spec is on disk at a known path; model routinely reads it |
| 3 | Resume is phase-level only, no mid-phase checkpointing | **PARTIALLY VALID** | No task-level resume exists; but "no record of progress" overstated — phase events are persisted |
| 4 | No scope enforcement, worker can exceed task boundary | **PARTIALLY VALID** | Per-task prompts lack scope limits; but phase-level prompts include explicit scope boundary language |
| 5 | No semantic QA, only exit code + structural checks | **PARTIALLY VALID** | Broadly correct, but anti-instinct gate includes semantic checks (not just YAML); however, effectively bypassed due to missing `output_path` |
| 6 | `build_task_context()` is dead code with no callers | **PARTIALLY VALID** | Dead in production runtime, but called extensively from test files |

---

## Claim 1: Tasklist Held in Memory Only

> "_parse_phase_tasks returns a list[TaskEntry]. That list is a local variable... never written to disk, never serialized."

### Verdict: PARTIALLY VALID

**What's correct:**
- `_parse_phase_tasks` at `executor.py:1203` returns `list[TaskEntry] | None`
- Passed directly to `execute_phase_tasks(tasks=tasks)` at `executor.py:1208`
- The raw `tasks` list object itself is not serialized to disk
- Execution logs (`logging_.py:91-105`) record phase-level events, not full `TaskEntry` lists

**What's overstated:**
- Task-derived data IS persisted indirectly:
  - `DeferredRemediationLog` entries include `step_id=task.task_id` (`executor.py:639-645`)
  - Serialized to `results/remediation.json` (`trailing_gate.py:548-570`)
- `_parse_phase_tasks` can return `None` (not always a list) — returns `None` if file missing (`executor.py:1104-1105`) or no tasks parsed (`executor.py:1109`)

---

## Claim 2: Worker Prompt Lacks Sufficient Context

> "The description is just the Deliverables text — one line. The worker does NOT get acceptance criteria, steps, tier... The prompt gives the worker a file path, but does not instruct it to read it."

### Verdict: VALID (with important context)

**What's correct:**
- Per-task prompt at `executor.py:1064-1068` is exactly 3 lines:
  ```
  Execute task {task.task_id}: {task.title}
  From phase file: {phase.file}
  Description: {task.description}
  ```
- `description` is derived from `**Deliverables:**` block only (`config.py:362-380`)
- Omitted from prompt: `dependencies`, `command`, `classifier`, acceptance criteria, steps, validation rules
- No `@{path}` syntax (which would force-load the file)
- No `/sc:task-unified` invocation (unlike the phase-level `build_prompt()`)
- No explicit "read this file" instruction

**Critical context the claim ignores:**
- The full phase file (e.g., `phase-1-tasklist.md`) contains extremely detailed task specs: metadata tables, numbered steps, acceptance criteria, validation commands, rollback instructions
- The file path IS in the prompt (`From phase file: {path}`)
- Claude workers with filesystem access routinely read referenced files
- The phase-level freeform path (`process.py:170`) DOES use `@{phase_file}` and `/sc:task-unified`

**Assessment:** The per-task prompt is technically minimal, but the claim frames this as a design flaw while ignoring that the specification is a single file read away. The real gap is that file loading is inference-dependent rather than contractually guaranteed.

---

## Claim 3: No Mid-Phase Resume Mechanism

> "If the process crashes mid-loop mid-phase, there's no resume mechanism... that's phase-level granularity only."

### Verdict: PARTIALLY VALID

**What's correct:**
- No task-level checkpointing during `execute_phase_tasks` loop (`executor.py:956`)
- `TaskResult` objects accumulate in memory only (`executor.py:964-971, 1017-1025`)
- No per-task JSONL events in sprint logger
- `--start` flag provides phase-level skip only (`commands.py:73-86`, `models.py:404-407`)
- Resume command generated is phase-level: `--start {halt_phase}` (`models.py:490-497`)
- Phase-end checkpoint (`CP-Pxx-END.md`) is phase-level, not task-level (`executor.py:1594-1596`)
- No mechanism to skip completed tasks within a restarted phase

**What's overstated:**
- "No record of progress" is too absolute:
  - `execution-log.jsonl` records phase-level events (`logging_.py:91-106`)
  - Phase result files persist to disk (`executor.py:1718-1760`)
  - Completed tasks' side effects (file changes, git commits) persist
  - The claim acknowledges this but then overstates by saying "no record"

---

## Claim 4: No Scope Enforcement

> "Nothing stops the worker from completing more than the item sent to it... no scope enforcement mechanism in the programmatic layer. The only scope boundary is the prompt text, which is 3 lines and doesn't say 'do only this task and nothing else.'"

### Verdict: PARTIALLY VALID

**What's correct:**
- Per-task subprocess prompt (`executor.py:1064-1068`) contains NO scope-limiting language
- No programmatic before/after diff gate per task
- No file-change allowlist per task
- No verification that only expected files were modified
- Worker runs with `--dangerously-skip-permissions` by default
- Monitor tracks telemetry (`monitor.py`) but doesn't enforce scope

**What's overstated:**
- Phase-level prompt (`process.py:build_prompt()`) DOES include explicit scope boundaries:
  - "**Scope Boundary** ... After completing all tasks, STOP immediately."
  - "Do not read, open, or act on any subsequent phase file."
  - "Focus only on the tasks defined in the phase file."
- `sc-task-unified-protocol` SKILL includes MUST/VIOLATION process rules (TFEP)
- "Orchestrator has no way to know" is too absolute — monitor tracks last task ID and file-change counts

**Key distinction:** The claim conflates two execution paths:
- **Phase-level freeform** (uses `build_prompt()` with scope language + `/sc:task-unified`)
- **Per-task subprocess** (uses minimal 3-line prompt without scope language)

The critique is valid for per-task mode but not for phase-level mode.

---

## Claim 5: No Semantic QA

> "No semantic QA. Per-task checks are: (1) exit code, (2) wiring hook, (3) anti-instinct YAML frontmatter check... No check that worker output matches acceptance criteria."

### Verdict: PARTIALLY VALID

**What's correct:**
- Per-task hooks are limited to (`executor.py:1027-1036`):
  1. Exit code classification (`executor.py:999-1005`)
  2. Wiring hook — structural code analysis, not task-specific (`executor.py:450-611`)
  3. Anti-instinct hook (`executor.py:787-909`)
- No acceptance-criteria matching
- No deliverable-file existence verification
- No automatic test execution after tasks
- No before/after state comparison
- `empirical_gate_v1` is exit-code only (`classifiers.py:19-24`)

**What's inaccurate:**
- Anti-instinct is NOT merely "YAML frontmatter check":
  - `ANTI_INSTINCT_GATE` is STRICT tier (`roadmap/gates.py:1063`)
  - Includes semantic checks: `undischarged_obligations == 0`, `uncovered_contracts == 0`, `fingerprint_coverage >= 0.7` (`roadmap/gates.py:1071-1087`)
- **However**, in Sprint per-task flow, anti-instinct is effectively bypassed:
  - `TaskResult.output_path` defaults to `""` (`models.py:176`)
  - Not set during `execute_phase_tasks` (`executor.py:1017-1025`)
  - When `output_path` is empty, anti-instinct vacuously passes (`executor.py:829-831`)

**Net effect:** The claim's conclusion is correct (no semantic QA in practice), but its characterization of what anti-instinct does is incomplete.

---

## Claim 6: `build_task_context()` is Dead Code

> "build_task_context() exists in process.py... it's defined but dead code. No caller anywhere in the codebase."

### Verdict: PARTIALLY VALID

**What's correct:**
- `build_task_context()` defined at `process.py:245-307`
- **No runtime caller** in any `src/superclaude/cli/` code
- Not called from `execute_phase_tasks()` or `_run_task_subprocess()`
- Dead in production execution flow

**What's incorrect:**
- "No caller anywhere" is false — tests call it extensively:
  - `tests/sprint/test_process.py:314, 326, 339, 361, 378, 386, 397, 410`
  - `tests/sprint/test_context_injection.py:78, 92, 100, 108, 115, ...`

**What it would do if wired:**
- Build `## Prior Task Context` section with per-task summaries
- Include `### Gate Outcomes` list
- Include `### Remediation History` for reimbursed tasks
- Include `### Git Changes Since Sprint Start` via `git diff --stat`
- Support context compression for older tasks (`compress_context_summary()` at `process.py:335-374`)

This is infrastructure for context injection between sequential tasks — built, tested, but not connected to the execution loop.

---

## Overall Assessment

The critique identifies **real architectural gaps** in the Sprint CLI's per-task execution path. The core observations are sound:

1. Per-task prompts are minimal (valid)
2. No task-level resume (valid)
3. No semantic QA of task outcomes (valid in practice)
4. `build_task_context()` is production-dead (valid)

However, the critique consistently **overstates** findings by:
- Ignoring the phase-level execution path which has stronger guarantees
- Characterizing inference-layer controls (skills, protocols) as nonexistent
- Using absolutes ("never", "no caller anywhere", "no record") where partial mechanisms exist
- Not acknowledging that rich task specs on disk compensate for minimal prompts
- Mischaracterizing anti-instinct as "just YAML" when it has semantic checks (even if bypassed)

The most actionable gaps identified:
1. **Wire `build_task_context()`** — tested but unused; would significantly improve per-task context
2. **Set `TaskResult.output_path`** — would enable anti-instinct semantic checks per-task
3. **Add `@` file reference** to per-task prompt — would guarantee phase file loading
4. **Add per-task JSONL events** — would enable task-level resume
