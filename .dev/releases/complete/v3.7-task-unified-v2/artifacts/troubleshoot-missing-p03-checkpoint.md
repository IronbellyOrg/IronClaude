# Root Cause Analysis: Missing Phase 3 Checkpoints (CP-P03-T01-T05, CP-P03-END)

**Date**: 2026-03-23
**Analyst**: Claude Opus 4.6
**Sprint**: OntRAG R0+R1 (7 phases, executed 2026-03-22)
**Affected Phase**: Phase 3 — Configuration & Utilities

---

## 1. Executive Summary

Phase 3 completed all 6 tasks (T03.01-T03.06) and produced all 6 deliverables (D-0013 through D-0018) but failed to write either checkpoint file. The root cause is a **structural anomaly in phase-3-tasklist.md** combined with **missing checkpoint enforcement in the sprint pipeline** and **no explicit checkpoint instructions in the agent prompt**.

Phase 3 is the ONLY phase with TWO checkpoint sections (mid-phase + end-of-phase). All other phases have exactly ONE (end-of-phase only). The agent interpreted the `### Checkpoint:` sections as passive documentation rather than actionable work items, because:
- The prompt from the sprint runner says nothing about checkpoints
- The `### Checkpoint:` heading pattern does not match `### T<NN>.<NN>` task pattern
- The task-unified skill processes `### T<NN>.<NN>` headings as actionable items and treats everything else as context

---

## 2. Root Cause: Triple Failure Chain

### Cause 1 (Primary): Agent prompt contains no checkpoint instructions

**File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py`, lines 169-203

The `build_prompt()` method constructs the prompt given to the claude subprocess for each phase. The prompt instructs the agent to:
- Execute tasks in order (T03.01, T03.02, etc.)
- Handle tiers (STRICT, STANDARD, LIGHT, EXEMPT)
- Write a result file with `EXIT_RECOMMENDATION: CONTINUE`
- Stop after completing all tasks

**Crucially absent**: Any mention of checkpoint sections, checkpoint file writing, or checkpoint report paths. The prompt says "After completing all tasks, STOP immediately" — which the agent correctly interpreted as "stop after T03.06."

The relevant prompt excerpt (lines 186-191):
```
## Scope Boundary
- After completing all tasks, STOP immediately.
- Do not read, open, or act on any subsequent phase file.
```

### Cause 2 (Structural): Phase 3 uniquely has two checkpoint sections

**File**: `.dev/releases/current/feature-Ont-RAG/feature-OntRAG_r0-r1/phase-3-tasklist.md`, lines 285-314

Heading inventory across all 7 phase tasklists:

| Phase | Task Headings | Checkpoint Headings | Total `###` Headings |
|-------|--------------|--------------------|--------------------|
| 1 | T01.01-T01.05 (5) | 1 (End of Phase 1) | 6 |
| 2 | T02.01-T02.06 (6) | 1 (End of Phase 2) | 7 |
| **3** | **T03.01-T03.06 (6)** | **2 (Mid-Phase + End)** | **8** |
| 4 | T04.01-T04.04 (4) | 1 (End of Phase 4) | 5 |
| 5 | T05.01-T05.05 (5) | 1 (End of Phase 5) | 6 |
| 6 | T06.01-T06.05 (5) | 1 (End of Phase 6) | 6 |
| 7 | T07.01-T07.04 (4) | 1 (End of Phase 7) | 5 |

Phase 3 is the only phase with a mid-phase checkpoint (`### Checkpoint: Phase 3 / Tasks T03.01-T03.05`). This created two checkpoint sections for the agent to process — but neither was processed.

The `### Checkpoint:` heading pattern is structurally distinct from the `### T<NN>.<NN> --` pattern that all task items use. The agent's task scanner (whether built into sc:task-unified or inferred from the prompt's "execute tasks in order T03.01, T03.02..." instruction) recognizes `T<NN>.<NN>` as actionable and treats `### Checkpoint:` as descriptive context.

### Cause 3 (Pipeline): No checkpoint enforcement or detection in sprint executor

**File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`, lines 1592-1603

The `_check_checkpoint_pass()` function EXISTS in the executor, but it is only called as a **crash recovery heuristic** (line 1799-1802) — it reads checkpoint files to infer whether a phase succeeded despite a non-zero exit code. It is NEVER called as a **post-phase enforcement gate**.

The phase completion flow:
1. Agent subprocess exits with code 0
2. Executor reads `results/phase-3-result.md` for `EXIT_RECOMMENDATION: CONTINUE`
3. Executor classifies phase as PASS
4. Executor moves to Phase 4

At no point does the executor check whether `checkpoints/CP-P03-END.md` exists or was written. The checkpoint existence check is purely a recovery mechanism, not a quality gate.

---

## 3. Why Other Phases Succeeded

**Answer**: The agents for phases 1, 2, 4, 5, 6, and 7 chose to write checkpoints voluntarily.

Evidence from Phase 4 output (lines 146-152 of `phase-4-output.txt`):
```
"All tests pass. Now write the checkpoint report and result file."
[creates mkdir for checkpoints directory]
[writes CP-P04-END.md]
[writes phase-4-result.md]
```

The Phase 4 agent independently decided to write the checkpoint before the result file. This was not prompted — the same `build_prompt()` was used. It was an emergent behavior: the agent read the tasklist, noticed the `### Checkpoint: End of Phase 4` section with a `Checkpoint Report Path:`, and inferred it should write that file.

**Why Phase 3 differed**: The Phase 3 agent processed all tasks correctly but after T03.06, it proceeded directly to running tests and writing the result file (lines 285-302 of `phase-3-output.txt`). Its thinking at line 12 shows it planned only the 6 T-numbered tasks:

```
T03.01: UE_MANAGER_URL default — already correct
T03.02: Need to add CHECKPOINT_POSTGRES_DSN
T03.03: Need to add Redis namespace constants
T03.04: Need to create validate_v01_data.py script
T03.05: Dead code import trace (read-only analysis)
T03.06: Need to create validate_gemini_key.py script
```

No mention of checkpoint sections. The agent's task plan enumerated only `T<NN>.<NN>` items.

**Contributing factor — Phase 3 context pressure**: Phase 3 output was 744KB (the largest of all phases). The agent may have been under higher context pressure by the time it finished T03.06, making it more likely to rush to the result file rather than re-scan the tasklist for additional items beyond the T-numbered tasks.

---

## 4. Failure Path Trace

```
Sprint Runner
  |
  +-- build_prompt() [process.py:169-203]
  |     Constructs: "/sc:task-unified Execute all tasks in @phase-3-tasklist.md"
  |     Contains: "Execute tasks in order (T03.01, T03.02, etc.)"
  |     Contains: "After completing all tasks, STOP immediately"
  |     MISSING: Any checkpoint instruction
  |
  +-- Claude subprocess spawned
  |     |
  |     +-- Agent reads phase-3-tasklist.md
  |     +-- Agent plans: T03.01 through T03.06 (6 tasks)
  |     +-- Agent does NOT plan checkpoints
  |     |     (### Checkpoint: heading != ### T03.xx heading pattern)
  |     |
  |     +-- Executes T03.01 through T03.06 (all succeed)
  |     +-- Runs regression tests
  |     +-- Writes results/phase-3-result.md with "EXIT_RECOMMENDATION: CONTINUE"
  |     +-- Agent exits (end_turn at line 302 of output)
  |
  +-- determine_phase_status() [executor.py:1775]
  |     Reads phase-3-result.md -> finds "EXIT_RECOMMENDATION: CONTINUE"
  |     Returns PhaseStatus.PASS
  |     DOES NOT check for checkpoint file existence
  |
  +-- Logs phase_complete with status=pass
  +-- Proceeds to Phase 4
```

---

## 5. Sprint Runner Pipeline — Enforcement Gap Locations

### Location 1: build_prompt() — Missing checkpoint instructions
**File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py`, lines 169-203

**Fix**: Add a checkpoint section to the prompt template:
```python
f"## Checkpoints\n"
f"- After completing all tasks, check the phase file for `### Checkpoint:` sections\n"
f"- For each checkpoint section, write the checkpoint report to the path specified in `Checkpoint Report Path:`\n"
f"- Checkpoint reports must include verification results per the checkpoint's criteria\n"
f"- Write checkpoint files BEFORE the result file\n"
```

### Location 2: determine_phase_status() — No post-phase checkpoint validation
**File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`, line ~1811+

**Fix**: After the phase returns PASS, check whether expected checkpoint files exist:
```python
# After classifying as PASS, verify checkpoint files exist
if status == PhaseStatus.PASS and config and phase:
    expected_checkpoint = config.release_dir / "checkpoints" / f"CP-P{phase.number:02d}-END.md"
    if not expected_checkpoint.exists():
        # Log warning, optionally downgrade to INCOMPLETE or trigger remediation
        logger.warning(f"Phase {phase.number} PASS but checkpoint missing: {expected_checkpoint}")
```

### Location 3: _check_checkpoint_pass() — Only used for crash recovery
**File**: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`, lines 1592-1603, called at 1802

**Fix**: Promote this from crash-recovery-only to a standard post-phase verification step.

### Location 4: Tasklist generator — Checkpoint sections lack actionable markers
**Observation**: The `### Checkpoint:` sections contain structured data (Checkpoint Report Path, Verification, Exit Criteria) but do not follow the `### T<NN>.<NN>` naming convention that signals "this is a task to execute."

**Fix**: Either:
(a) Convert checkpoints to proper task entries (e.g., `### T03.07 -- Write CP-P03-T01-T05 checkpoint report`) so the agent's task scanner picks them up, OR
(b) Add explicit `- [ ] Write checkpoint report to <path>` checklist items within checkpoint sections

---

## 6. Contributing Factors (Non-Root-Cause)

| Factor | Impact | Evidence |
|--------|--------|----------|
| Two checkpoint sections (unique to P3) | Doubled the likelihood of missing checkpoints | P3 has 2 vs. 1 for all other phases |
| 744KB output (largest phase) | Higher context pressure may have caused agent to rush | `execution-log.jsonl` line 7: `output_bytes: 744332` |
| No TodoWrite checkpoint item | P4 agent used TodoWrite to track "Write checkpoint" as a todo; P3 agent did not | P4 output line 147 vs. P3 output (no TodoWrite for checkpoints) |
| Nondeterministic agent behavior | Whether an agent writes checkpoints is emergent, not enforced | 6/7 phases wrote checkpoints voluntarily |

---

## 7. Recommendations (Priority Order)

1. **[HIGH] Add checkpoint instructions to build_prompt()** — Deterministic fix. Every agent will be explicitly told to write checkpoint files. Eliminates reliance on emergent behavior.

2. **[HIGH] Add post-phase checkpoint validation** — Defense in depth. Even if an agent skips checkpoints, the executor detects the gap and can trigger remediation or warn.

3. **[MEDIUM] Convert checkpoint sections to task entries** — Makes the tasklist generator produce checkpoint items that the agent's task scanner will unconditionally process (e.g., `### T03.07 -- Write mid-phase checkpoint CP-P03-T01-T05`).

4. **[LOW] Add checkpoint file list to execution-log.jsonl** — After each phase, log which checkpoint files exist. Provides observability for future debugging.

---

## 8. Files Examined

| File | Purpose in analysis |
|------|-------------------|
| `feature-OntRAG_r0-r1/phase-3-tasklist.md:285-314` | Checkpoint sections that were skipped |
| `feature-OntRAG_r0-r1/phase-{1,2,4,5,6,7}-tasklist.md` | Comparison: all have 1 checkpoint vs. P3's 2 |
| `feature-OntRAG_r0-r1/results/phase-3-output.txt:12,285-302` | Agent thinking (no checkpoints planned) and end-of-phase (no checkpoint written) |
| `feature-OntRAG_r0-r1/results/phase-4-output.txt:146-154` | Comparison: P4 agent voluntarily wrote checkpoint |
| `feature-OntRAG_r0-r1/execution-log.jsonl:6-7` | P3 phase_complete event (status=pass, no checkpoint validation) |
| `feature-OntRAG_r0-r1/checkpoints/CP-P03-*.md` | Retroactively created on 2026-03-23 |
| `IronClaude/.../sprint/process.py:169-203` | `build_prompt()` — no checkpoint instructions |
| `IronClaude/.../sprint/executor.py:1592-1603` | `_check_checkpoint_pass()` — crash recovery only |
| `IronClaude/.../sprint/executor.py:1775-1830` | `determine_phase_status()` — no checkpoint enforcement |
| `IronClaude/.../commands/task-unified.md` | Task command — no checkpoint awareness |
| `.claude/skills/task/SKILL.md` | Task skill — processes `- [ ]` items, no checkpoint awareness |
