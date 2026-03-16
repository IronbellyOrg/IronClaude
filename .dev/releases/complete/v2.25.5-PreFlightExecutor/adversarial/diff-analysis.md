# Diff Analysis: pass_no_report Solution Variants

## 1. Variant Inventory

| Variant | Label | Core Mechanism |
|---------|-------|----------------|
| A | Prompt Injection | Append result-file write instruction to agent prompt |
| B | AggregatedPhaseReport Pre-Write | Use per-task aggregation to write result file before status determination |
| C | Accept Status Quo | Document `pass_no_report` as expected; no code change |
| D | Reorder Executor Write | Move `_write_executor_result_file()` to run BEFORE `_determine_phase_status()` |

---

## 2. Structural Differences

### Control Flow Impact

**Option A** modifies `_run_task_subprocess()` (L461-466) only. Does not touch the main `execute_sprint()` loop.

**Option B** requires wiring `execute_phase_tasks()` (L350-447) into `execute_sprint()` (L491-831). Currently `execute_phase_tasks()` is **defined but never called** from the main loop. The main loop spawns one `ClaudeProcess` per phase at L578, not per task. This is a significant architectural gap.

**Option C** modifies zero source files. Documentation-only change.

**Option D** reorders two existing function calls in `execute_sprint()` at L696-717. Moves `_write_executor_result_file()` before `_determine_phase_status()`, then passes the written file to status determination.

### Files Touched

| Variant | executor.py | models.py | docs | New code |
|---------|------------|-----------|------|----------|
| A | L461-466 (prompt string) | None | None | ~4 lines |
| B | L536+ (main loop refactor) | None | None | ~30-50 lines |
| C | None | None | Yes | 0 lines |
| D | L696-717 (reorder) | None | None | ~5 lines |

---

## 3. Content Differences

### Source of Truth for Phase Outcome

- **A**: Agent self-reports via result file (non-deterministic)
- **B**: Runner aggregates per-task results (deterministic, but infrastructure not wired)
- **C**: No result file; status inferred from output existence (heuristic)
- **D**: Executor writes result file with its own assessment, then reads it back (deterministic)

### Alignment with "Executor is Authoritative" (L706-708)

The code comment at L706-708 explicitly states: "Overwrites any agent-written file -- executor is authoritative."

- **A**: Contradicts this -- makes agent the authority for result file content
- **B**: Aligns -- runner constructs report from observed outcomes
- **C**: N/A -- no result file at all
- **D**: Aligns perfectly -- executor writes its own authoritative result before reading it

---

## 4. Contradictions

### Option B's Premise vs. Reality

Option B assumes `execute_phase_tasks()` feeds into `execute_sprint()`. It does not. The main loop runs one subprocess per phase (L578: `ClaudeProcess(config, phase, ...)`), not per task. `execute_phase_tasks()` exists for future per-task orchestration but is currently dead code in the main loop path.

To implement Option B, you would need to:
1. Parse tasks from phase file inside `execute_sprint()`
2. Replace `ClaudeProcess(config, phase)` with `execute_phase_tasks(tasks, config, phase)`
3. Thread `task_results` through to `aggregate_task_results()`
4. Write the aggregated report before `_determine_phase_status()`

This is a major refactor of the main loop, not a targeted fix.

### Option A's Self-Contradiction

Option A appends instructions to the prompt to write EXIT_RECOMMENDATION. But `_write_executor_result_file()` at L708 already "overwrites any agent-written file." So even if the agent writes the file, the executor overwrites it AFTER status determination. The agent's file would be read by `_determine_phase_status()` at L696, then immediately overwritten. This actually works for status determination -- but the agent compliance risk means it may not write the file at all, falling through to `PASS_NO_REPORT` anyway.

### Option D's Circularity Concern

The existing comment at L707 says: "Written AFTER status determination to avoid circularity." Option D proposes the opposite. The circularity concern was: the executor would write PASS/FAIL based on status, then read it to determine status. Option D resolves this by having the executor compute its status assessment from exit_code and monitor_state FIRST, write it, then let `_determine_phase_status()` read the file. The "circularity" was about the function needing its own output as input -- but `_write_executor_result_file` takes `status` as a parameter and `_determine_phase_status` produces it. In Option D, we compute a preliminary status from exit_code alone, write it, then let the full classifier run.

---

## 5. Unique Contributions

### Option D (Emergent)

Option D is the only variant that:
- Requires no new infrastructure
- Has zero agent-compliance risk
- Perfectly aligns with "executor is authoritative"
- Achieves `PASS` status deterministically
- Changes approximately 5-10 lines of code

The key insight: `_write_executor_result_file()` already produces a result file with `EXIT_RECOMMENDATION: CONTINUE/HALT`. It just runs too late. Moving it before `_determine_phase_status()` solves the problem completely.

### Option B (Future Value)

Option B's per-task orchestration would provide richer telemetry (per-task pass/fail in the result file). While not feasible as a targeted fix, the infrastructure exists and could be wired in during a larger refactor.

### Option A (Defense in Depth)

Even after implementing D, adding result-file instructions to the prompt provides a secondary signal. If the agent writes a result file AND the executor writes one, the executor's file would take precedence.
