# Adversarial Debate Transcript: pass_no_report Solution Selection

## Participants

- **Advocate-A**: Argues for Option A (Prompt Injection)
- **Advocate-D**: Argues for Option D (Reorder Executor Write)
- **Advocate-C**: Argues for Option C (Accept Status Quo)
- **Orchestrator**: Process coordination, scoring, convergence tracking

Option B was excluded from active debate after diff-analysis revealed `execute_phase_tasks()` is not wired into `execute_sprint()`, making it infeasible as a targeted fix.

---

## Round 1: Opening Arguments

### Advocate-D (Opening)

Option D is the most architecturally aligned solution. The executor already writes a result file with `EXIT_RECOMMENDATION: CONTINUE/HALT` via `_write_executor_result_file()`. The only problem is timing: it runs AFTER `_determine_phase_status()`.

However, I must acknowledge a complication discovered in the diff analysis: `_write_executor_result_file()` takes `status: PhaseStatus` as a parameter (L928). It cannot run before status determination because it needs the status to decide what to write. This creates a genuine circularity -- exactly the concern documented in the L707 comment.

**Revised Option D proposal**: Instead of moving the existing function, create a new lightweight pre-write that uses exit_code alone:

```python
# Before _determine_phase_status:
if exit_code == 0:
    _pre_recommendation = "CONTINUE"
    _write_preliminary_result(config, phase, exit_code, _pre_recommendation)
# Then _determine_phase_status reads the file and classifies as PASS
```

This preserves the existing `_write_executor_result_file()` as an authoritative post-hoc overwrite while ensuring a result file exists for `_determine_phase_status()` to read when exit_code is 0.

### Advocate-A (Opening)

Option A is the simplest change: append 3-4 lines to the agent prompt at L461-466 instructing it to write EXIT_RECOMMENDATION. The agent would write `config.result_file(phase)` with CONTINUE/HALT, and `_determine_phase_status()` would find it.

Agent compliance is the primary risk. However, in practice, Claude Code agents follow explicit file-write instructions with high reliability (>95%). The instruction is simple, unambiguous, and the path is deterministic.

Furthermore, Option A provides a richer signal than Option D: the agent can report actual task outcomes (which tasks passed, which failed) rather than just "exit code was 0 therefore CONTINUE." The agent has context that the executor lacks.

### Advocate-C (Opening)

Both A and D introduce unnecessary complexity and risk to solve a problem that is not a problem. `PASS_NO_REPORT` is already `is_success = True`. The sprint succeeds. Every consumer of `PhaseStatus` checks `is_success`, not `== PhaseStatus.PASS`.

The only cost of `pass_no_report` vs `pass` is telemetry granularity. That cost is addressed by adding a single paragraph to the sprint CLI guide. Zero risk, zero code change, zero regression surface.

---

## Round 1: Cross-Examination

### Advocate-D challenges Advocate-A

**D to A**: Your solution depends on the agent writing to `config.result_file(phase)`. But the agent runs inside an isolation directory (L560-562). The agent's working directory is set to this isolation dir via `CLAUDE_WORK_DIR`. If the agent writes a relative path, it writes inside isolation, not to `config.results_dir`. You need to inject the absolute path.

**A responds**: Correct. The prompt must include the absolute path: `str(config.result_file(phase))`. This is straightforward.

**D to A**: Even with the absolute path, the agent may not comply. What is your fallback?

**A responds**: The fallback is the existing behavior: `PASS_NO_REPORT`. Option A improves the situation when the agent complies and does not worsen it when the agent does not. It is a strict improvement.

### Advocate-C challenges Advocate-D

**C to D**: Your revised Option D writes a "preliminary result" before status determination. Trace the behavior for non-zero exit codes.

If exit_code != 0 and you wrote a preliminary file with HALT:
1. `_determine_phase_status()` enters the non-zero path
2. `detect_prompt_too_long()` check -- if True, calls `_classify_from_result_file()` which reads your preliminary file, finds HALT, returns `PhaseStatus.HALT`
3. This short-circuits the context exhaustion logic that should return `INCOMPLETE`

**Your preliminary write would corrupt the non-zero exit path.**

**D responds**: This is a valid concern. The preliminary write MUST be guarded to only fire when exit_code == 0. For non-zero exits, the existing classification handles context exhaustion, checkpoint recovery, and error detection correctly. No preliminary file should exist for those paths.

**C follows up**: And for exit_code == 0 with a stale result file from a previous run?

**D responds**: `_classify_from_result_file()` already has staleness checking (L850: `if started_at > 0 and mtime < started_at`). But this function is only called in the non-zero exit path. In the zero-exit path, `_determine_phase_status()` directly reads `result_file.read_text()` at L1019 without staleness checking. However, this is not a problem for Option D because the preliminary file is freshly written seconds before reading -- it will never be stale.

### Advocate-A challenges Advocate-C

**A to C**: You say "every consumer checks `is_success`." But the debug log at L737 writes `status=status.value`. The execution-log.md records the exact status. When diagnosing sprint issues across multiple runs, `pass_no_report` for every phase means you cannot tell whether the agent successfully self-reported or simply ran and exited. This matters for debugging production sprint failures.

**C responds**: How often do you need to distinguish "agent passed and reported" from "agent passed and didn't report" in a system where agents NEVER report (because the prompt never asks them to)? The answer is: never. `pass_no_report` IS the correct classification for the current design. If you change the design, then the distinction matters -- but that is circular reasoning for justifying the change.

**A responds**: The value is forward-looking. As the sprint system matures, we will want to know whether agents can reliably self-report. Option A establishes that capability. If all phases show `pass` after implementing A, we know agents comply. If some show `pass_no_report`, we know which agents failed to report. This telemetry has diagnostic value beyond the immediate fix.

---

## Round 2: Focused Debate on Key Differentiators

### Point 1: Regression Risk

| Variant | Risk Level | Explanation |
|---------|-----------|-------------|
| A | Low | Prompt change only; worst case is status quo behavior |
| C | None | No code change |
| D (revised) | Low | Guarded to exit_code==0 only; isolated code path |

All advocates agree: C has zero risk, A and D have low risk. **Agreement: 95%.**

### Point 2: Signal Fidelity

| Variant | Status Produced | Telemetry Value |
|---------|----------------|-----------------|
| A (agent complies) | PASS | High -- agent-reported with task detail |
| A (agent does not comply) | PASS_NO_REPORT | Same as current |
| C | PASS_NO_REPORT | Low -- no distinction possible |
| D (revised) | PASS | Medium -- executor-determined, no task detail |

Advocate-A argues agent-reported detail is more valuable. Advocate-D argues determinism is more valuable than richness. **Agreement: 85%.**

### Point 3: Architectural Alignment

The executor.py comment at L706-708 states: "Overwrites any agent-written file -- executor is authoritative."

| Variant | Alignment |
|---------|-----------|
| A | Weak -- makes agent the primary authority for the result file read by `_determine_phase_status()` |
| C | Neutral -- no result file produced before status determination |
| D | Strong -- executor writes the authoritative result before its own classifier reads it |

**Agreement: 95%.**

### Point 4: Implementation Complexity

| Variant | Lines Changed | New Functions | Test Changes |
|---------|--------------|--------------|-------------|
| A | ~5 (prompt string) | 0 | Minimal -- test prompt content |
| C | 0 | 0 | None |
| D (revised) | ~12 | 1 (`_write_preliminary_result`) | Test exit_code==0 guard, test non-zero paths unaffected |

**Agreement: 95%.**

### Point 5: False Positive Risk

Critical concern raised by Advocate-C: if the agent actually fails tasks but exit_code is 0, what happens?

- **Option A**: Agent writes EXIT_RECOMMENDATION: HALT (if it detects failures). Status = HALT. Correct.
- **Option C**: Status = PASS_NO_REPORT (is_success=True). False positive.
- **Option D**: Executor writes CONTINUE (exit_code==0). Status = PASS. False positive.

**Advocate-A scores here**: Only Option A can detect "exit 0 but tasks actually failed" because the agent has semantic understanding of task outcomes. The executor only sees exit codes.

**Advocate-D rebuts**: This is theoretical. Claude Code's exit code reliably indicates success/failure. Exit 0 with failed tasks is an edge case.

**Agreement: 75%.** This is the highest-contention point.

---

## Round 3: Convergence Assessment

### Per-Point Scoring Matrix

| Point | A | C | D | Convergence |
|-------|---|---|---|-------------|
| Regression risk | LOW | NONE | LOW | 95% |
| Signal fidelity | HIGH (conditional) | LOW | MEDIUM (guaranteed) | 85% |
| Architectural alignment | WEAK | NEUTRAL | STRONG | 95% |
| Implementation complexity | LOW | ZERO | LOW | 95% |
| False positive detection | YES | NO | NO | 75% |
| Determinism | NO | YES (trivially) | YES | 90% |
| Option B feasibility | N/A | N/A | N/A | 100% (excluded) |

### Overall Convergence: 91%

### Remaining Disagreements

1. **Advocate-C** (7%): Maintains any code change is unnecessary risk for a cosmetic improvement
2. **Advocate-A** (2%): Maintains agent-reported task detail and false-positive detection outweigh determinism concerns

### Consensus Position

**Option D (revised)** is the recommended base solution:
- Write a preliminary result file with EXIT_RECOMMENDATION: CONTINUE when exit_code == 0, before `_determine_phase_status()` runs
- Guard: do NOT write for non-zero exit codes
- Preserve existing `_write_executor_result_file()` as authoritative post-hoc overwrite

**Option A** is recommended as a layered follow-up:
- Add result-file write instruction to agent prompt for defense-in-depth
- Provides richer telemetry when agent complies
- Does not interfere with Option D (executor file overwrites agent file post-hoc)
