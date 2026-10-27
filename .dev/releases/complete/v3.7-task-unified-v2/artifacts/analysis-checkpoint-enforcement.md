# Domain Analysis: Checkpoint Enforcement

**Date**: 2026-04-02
**Analyst**: Claude Opus 4.6 (rf-analyst)
**Source Documents**: 3 files in `v3.7-task-unified-v2/`
**Analysis Type**: Comprehensive Domain Analysis — Cross-validation, completeness, gap identification

---

## 1. Executive Summary

### Problem

During the OntRAG R0+R1 sprint (2026-03-22, 7 phases), Phase 3 (Configuration & Utilities) completed all 6 tasks and produced all 6 deliverables but **failed to write either checkpoint file** (CP-P03-T01-T05, CP-P03-END). This is the only phase out of 7 that missed its checkpoints. The failure went undetected until post-sprint manual inspection because the sprint pipeline has no checkpoint enforcement.

**Source**: `troubleshoot-missing-p03-checkpoint.md`, Section 1 (lines 10-17)

### Why It Matters

Checkpoints are the sprint pipeline's quality gate — they record verification results, exit criteria, and evidence of task completion. A missing checkpoint means:
- No structured record that Phase 3's deliverables were verified
- No automated detection of the gap (discovered manually ~24 hours later)
- The 86% voluntary checkpoint write rate (6/7 phases) is unacceptable for a pipeline that aspires to deterministic execution

The root cause is a **triple failure chain**: (1) the agent prompt contains no checkpoint instructions, (2) Phase 3's checkpoint sections use a heading format invisible to the task scanner, and (3) the executor has no post-phase checkpoint validation. All three must be addressed.

**Source**: `troubleshoot-missing-p03-checkpoint.md`, Section 2 (lines 22-103); `unified-checkpoint-enforcement-proposal.md`, Section "Criterion 1: Effectiveness" (lines 22-30)

### Solution

A **three-layer defense architecture** (Prevention, Detection, Remediation) implemented across 4 waves:

| Wave | Layer | Solution | Ship Target |
|------|-------|----------|-------------|
| 1 | Prevention | Prompt-level checkpoint instructions in `build_prompt()` | Day 1 |
| 2 | Detection | Post-phase checkpoint enforcement gate (shadow -> soft -> full) | Day 2-5 |
| 3 | Remediation | Manifest tracking + CLI verify + auto-recovery | Day 5-10 |
| 4 | Prevention | Tasklist-level checkpoint normalization (breaking change, new tasklists only) | Next release |

**Total estimated LOC**: ~580 across 7 files (1 new, 6 modified), 15 tasks in 4 phases.

**Source**: `unified-checkpoint-enforcement-proposal.md`, Part 2 (lines 115-134); `tasklist-checkpoint-enforcement.md`, full document

---

## 2. Root Cause Analysis Summary

### The Triple Failure Chain

The Phase 3 checkpoint failure was not a single-point failure. Three independent safeguards were all absent simultaneously.

#### Cause 1 (Primary): Agent prompt contains no checkpoint instructions

**File**: `src/superclaude/cli/sprint/process.py`, lines 169-203
**Evidence**: The `build_prompt()` method constructs the prompt given to the Claude subprocess. It instructs the agent to execute T-numbered tasks, handle tiers, write a result file, and stop. It contains **zero mention** of checkpoints, checkpoint file writing, or checkpoint report paths.

Key prompt excerpt (lines 186-191 of process.py, quoted in RCA lines 36-40):
```
## Scope Boundary
- After completing all tasks, STOP immediately.
- Do not read, open, or act on any subsequent phase file.
```

The agent correctly interpreted "all tasks" as T03.01 through T03.06 and stopped after writing the result file.

**Source**: `troubleshoot-missing-p03-checkpoint.md`, Section 2, Cause 1 (lines 24-40)

#### Cause 2 (Structural): Phase 3 uniquely has two checkpoint sections with non-task heading pattern

**File**: `phase-3-tasklist.md`, lines 285-314
**Evidence**: Phase 3 is the ONLY phase with TWO checkpoint sections (mid-phase + end-of-phase). All other phases have exactly ONE. More importantly, the `### Checkpoint:` heading pattern is structurally distinct from the `### T<NN>.<NN>` pattern that the agent's task scanner recognizes as actionable.

| Phase | Task Headings | Checkpoint Headings | Total `###` Headings |
|-------|--------------|--------------------|--------------------|
| 1 | 5 | 1 | 6 |
| 2 | 6 | 1 | 7 |
| **3** | **6** | **2** | **8** |
| 4 | 4 | 1 | 5 |
| 5 | 5 | 1 | 6 |
| 6 | 5 | 1 | 6 |
| 7 | 4 | 1 | 5 |

The Phase 3 agent's thinking (output line 12) enumerated only T-numbered tasks — no checkpoints appeared in its plan.

**Source**: `troubleshoot-missing-p03-checkpoint.md`, Section 2, Cause 2 (lines 42-61)

#### Cause 3 (Pipeline): No checkpoint enforcement or detection in sprint executor

**File**: `src/superclaude/cli/sprint/executor.py`, lines 1592-1603 (function), 1799-1802 (call site)
**Evidence**: The `_check_checkpoint_pass()` function EXISTS but is only called as a **crash recovery heuristic** — it reads checkpoint files to infer whether a phase succeeded despite a non-zero exit code. It is NEVER called as a post-phase enforcement gate.

Phase completion flow:
1. Agent subprocess exits code 0
2. Executor reads result file for `EXIT_RECOMMENDATION: CONTINUE`
3. Executor classifies phase as PASS
4. Executor moves to next phase — **no checkpoint existence check**

**Source**: `troubleshoot-missing-p03-checkpoint.md`, Section 2, Cause 3 (lines 63-74)

### Why Other Phases Succeeded

The agents for phases 1, 2, 4, 5, 6, and 7 wrote checkpoints **voluntarily** — they read the `### Checkpoint:` sections with `Checkpoint Report Path:` entries and inferred they should write files. This was emergent behavior, not instructed. Phase 4's output (lines 146-152) explicitly shows the agent deciding on its own: "All tests pass. Now write the checkpoint report and result file."

Phase 3 differed due to a combination of: (a) the agent planning only T-numbered tasks, and (b) a 744KB output (largest of all phases) creating context pressure that may have caused the agent to rush to the result file.

**Source**: `troubleshoot-missing-p03-checkpoint.md`, Section 3 (lines 78-106)

### Contributing Factors (Non-Root-Cause)

| Factor | Impact | Evidence |
|--------|--------|----------|
| Two checkpoint sections (unique to P3) | Doubled likelihood of missing checkpoints | P3 has 2 vs. 1 for all other phases |
| 744KB output (largest phase) | Higher context pressure | `execution-log.jsonl` line 7: `output_bytes: 744332` |
| No TodoWrite checkpoint item | P4 agent used TodoWrite to track checkpoint; P3 did not | P4 output line 147 vs. P3 output |
| Nondeterministic agent behavior | Checkpoint writing is emergent, not enforced | 6/7 phases wrote voluntarily |

**Source**: `troubleshoot-missing-p03-checkpoint.md`, Section 6 (lines 184-192)

### Failure Path Trace

```
Sprint Runner
  |
  +-- build_prompt() [process.py:169-203]
  |     Contains: "Execute tasks in order (T03.01, T03.02, etc.)"
  |     Contains: "After completing all tasks, STOP immediately"
  |     MISSING: Any checkpoint instruction
  |
  +-- Claude subprocess spawned
  |     +-- Agent reads phase-3-tasklist.md
  |     +-- Agent plans: T03.01 through T03.06 (6 tasks) — NO checkpoints
  |     +-- Executes T03.01 through T03.06 (all succeed)
  |     +-- Writes results/phase-3-result.md with "EXIT_RECOMMENDATION: CONTINUE"
  |     +-- Agent exits
  |
  +-- determine_phase_status() [executor.py:1775]
  |     Reads phase-3-result.md -> "EXIT_RECOMMENDATION: CONTINUE"
  |     Returns PhaseStatus.PASS
  |     DOES NOT check for checkpoint file existence
  |
  +-- Proceeds to Phase 4 (gap undetected)
```

**Source**: `troubleshoot-missing-p03-checkpoint.md`, Section 4 (lines 109-139)

---

## 3. Solution Architecture

### Three-Layer Defense Model

The unified proposal implements checkpoint enforcement as three concentric, independent layers. Each layer is sufficient to catch the failure on its own; all three must fail simultaneously for a checkpoint to go permanently unwritten.

```
Layer 1 -- PREVENTION (Agent-Side)
  Solution 1: Prompt instructions tell the agent to write checkpoints
  Solution 2: Tasklist structure makes checkpoints indistinguishable from tasks
  -> Agent writes checkpoints as part of normal task execution

Layer 2 -- DETECTION (Executor-Side, Real-Time)
  Solution 3: Post-phase gate verifies checkpoint files exist on disk
  -> Sprint halts (or warns) if agent failed to write them

Layer 3 -- REMEDIATION (Post-Sprint, On-Demand)
  Solution 4: CLI verify + auto-recovery from evidence artifacts
  -> Missing checkpoints are detected, audited, and optionally regenerated
```

**Source**: `unified-checkpoint-enforcement-proposal.md`, Part 2, "Architecture" (lines 115-134)

### Solution-to-Layer Mapping

| # | Solution Name | Layer | Root Cause Addressed | Mechanism |
|---|--------------|-------|---------------------|-----------|
| 1 | Prompt-Level Checkpoint Enforcement | Prevention | Cause 1 (primary) | Add `## Checkpoints` section to `build_prompt()` output |
| 2 | Tasklist-Level Checkpoint Normalization | Prevention | Cause 2 (structural) | Convert `### Checkpoint:` to `### T<PP>.<NN>` task entries |
| 3 | Post-Phase Checkpoint Enforcement Gate | Detection | Cause 3 (pipeline) | Executor verifies checkpoint files exist after phase PASS |
| 4 | Checkpoint Observability & Auto-Recovery | Remediation | Cause 3 + operational gap | Manifest tracking + CLI verify + auto-recovery from evidence |

**Source**: `unified-checkpoint-enforcement-proposal.md`, Part 1, "Solution Summary" (lines 14-19)

### Solution-to-Root-Cause Coverage Matrix

| Solution | Cause 1 (No prompt) | Cause 2 (Structural mismatch) | Cause 3 (No enforcement) |
|----------|---------------------|-------------------------------|--------------------------|
| 1 (Prompt) | **FIXES** | Mitigates | Partially |
| 2 (Tasklist) | Not needed | **ELIMINATES** | Not addressed |
| 3 (Gate) | Not addressed | Not addressed | **FIXES** (detection) |
| 4 (Recovery) | Not addressed | Not addressed | **FIXES** (detection + remediation) |

**Minimum viable set**: Solution 1 + Solution 3 (or 4). This covers all three causes with prevention + detection.

**Full set**: All four solutions provide defense in depth where no single failure can result in a permanently missing checkpoint.

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Criterion 4: Defense in Depth" (lines 56-65)

### Key Architectural Decision: Shared Path Extraction Module

Both Solution 3 (per-phase gate) and Solution 4 (manifest/CLI) need to parse `Checkpoint Report Path:` from tasklists. Rather than duplicating this logic:

- `checkpoints.py` provides `extract_checkpoint_paths()` as a public function
- Solution 3's `_verify_checkpoints()` in executor.py imports from it
- Solution 4's `build_manifest()` imports from it

This eliminates the primary code duplication identified in the adversarial analysis.

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Redundancy to Eliminate" (lines 102-109) and "Key Design Decisions" item 1 (lines 288-289)

---

## 4. Adversarial Analysis Highlights

The unified proposal includes a 6-criterion adversarial comparison of all 4 solutions. Key findings:

### Criterion 1: Effectiveness

| Solution | Rating | Key Finding |
|----------|--------|-------------|
| 1 (Prompt) | HIGH | Drops failure rate from ~14% (1/7) to ~5%. Still relies on agent compliance. |
| 2 (Tasklist) | VERY HIGH | Drops failure rate to <1%. Checkpoints become structurally indistinguishable from tasks. |
| 3 (Gate) | MEDIUM | Detective, not preventive. Catches failures after they happen. |
| 4 (Recovery) | MEDIUM | Corrective, not preventive. Reduces 30-min manual recovery to 1 CLI command. |

**Verdict**: Solutions 1+2 are preventive (fix root causes). Solutions 3+4 are detective/corrective (catch and remediate). Maximum effectiveness requires at least one from each category.

**Source**: `unified-checkpoint-enforcement-proposal.md`, Criterion 1 (lines 22-30)

### Criterion 2: Implementation Complexity

| Solution | LOC (est.) | Files Modified | Files Created | Bug Risk |
|----------|-----------|----------------|---------------|----------|
| 1 (Prompt) | ~60 | 2 | 0 | Very Low |
| 2 (Tasklist) | ~200 | 1 | 0 | Low-Medium |
| 3 (Gate) | ~80 | 3 | 0 | Low |
| 4 (Recovery) | ~290 | 3 | 1 | Medium |

**Source**: `unified-checkpoint-enforcement-proposal.md`, Criterion 2 (lines 34-41)

### Criterion 3: Backward Compatibility

| Solution | Compatible? | Key Concern |
|----------|-------------|-------------|
| 1 (Prompt) | Fully | No format changes needed |
| 2 (Tasklist) | **Not compatible** | Existing tasklists with `### Checkpoint:` headings need regeneration |
| 3 (Gate) | Fully (shadow default) | New enum value is additive |
| 4 (Recovery) | Fully | All additive; works retroactively |

**Critical finding**: Solution 2 is a breaking change. This is the primary reason it is deferred to Wave 4 (next release cycle) rather than shipped immediately.

**Source**: `unified-checkpoint-enforcement-proposal.md`, Criterion 3 (lines 44-52)

### Criterion 5: Time to Value

| Solution | Est. Time | Ships Independently? |
|----------|-----------|---------------------|
| 1 (Prompt) | 1-2 hours | Yes |
| 2 (Tasklist) | 4-6 hours | Yes (but requires tasklist regen) |
| 3 (Gate) | 2-3 hours | Yes |
| 4 (Recovery) | 4-6 hours | Yes |

**Source**: `unified-checkpoint-enforcement-proposal.md`, Criterion 5 (lines 68-76)

### Complementary vs. Alternative Analysis

All four solutions are **complementary, not alternative**. No solution is a strict replacement for another. The only partial overlap is between Solutions 1 and 2: if Solution 2 is fully deployed, Solution 1's prompt instructions become redundant for new tasklists — but remain necessary for backward compatibility with old-format tasklists.

**Key finding** (line 100): "The redundancy between Solutions 1 and 2 is desirable (defense in depth), not wasteful."

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Complementary vs. Alternative Analysis" (lines 89-100)

---

## 5. Implementation Plan

### Overview

4 phases (waves), 15 tasks total (T01.01-T01.02, T02.01-T02.04, T03.01-T03.05, T04.01-T04.03), each with full MDTM metadata.

### Phase 1 -- Prompt-Level Checkpoint Enforcement (Wave 1)

**Goal**: Transform checkpoint writing from emergent to instructed behavior.
**Ship target**: Within 1 day
**Risk**: Very Low
**Files**: `process.py`, `executor.py`
**LOC**: ~60

| Task ID | Description | Effort | Risk | Tier | Confidence | Dependencies |
|---------|-------------|--------|------|------|------------|-------------|
| T01.01 | Add checkpoint instructions to `build_prompt()` in process.py | S | Very Low | STANDARD | 95% | None |
| T01.02 | Add `_warn_missing_checkpoints()` helper to executor.py | S | Very Low | STANDARD | 90% | None |

**T01.01 Details**:
- Target: `process.py` `build_prompt()` (lines ~169-203)
- Add `## Checkpoints` section with 5 instruction lines between task execution and scope boundary
- Amend `## Scope Boundary` to include "AND writing all checkpoint reports"
- Amend `## Result File` to include "after all checkpoints"
- Acceptance: prompt output contains checkpoint section; module imports clean; no other sections modified
- **Source**: `tasklist-checkpoint-enforcement.md`, T01.01 (lines 18-62)

**T01.02 Details**:
- Target: `executor.py`, after `determine_phase_status()` (~line 1775)
- New function `_warn_missing_checkpoints(phase_file, checkpoints_dir, phase_number) -> list[str]`
- Parses `Checkpoint Report Path:` from phase file, checks existence, logs warnings
- Warning-only — does NOT modify phase status
- Acceptance: function exists, parses paths, logs warnings, called after PASS, no status change
- **Source**: `tasklist-checkpoint-enforcement.md`, T01.02 (lines 65-106)

**Checkpoint**: End of Phase 1 verifies both `build_prompt()` changes and `_warn_missing_checkpoints()` are functional.
**Source**: `tasklist-checkpoint-enforcement.md`, lines 109-121

### Phase 2 -- Post-Phase Checkpoint Enforcement Gate (Wave 2)

**Goal**: Add executor-level checkpoint verification after each phase, deployed in shadow mode.
**Ship target**: Within 1 week
**Risk**: Low
**Files**: `checkpoints.py` (NEW), `executor.py`, `models.py`, `logging_.py`
**LOC**: ~120
**Dependencies**: Phase 1 complete (T01.02 establishes call site pattern)

| Task ID | Description | Effort | Risk | Tier | Confidence | Dependencies |
|---------|-------------|--------|------|------|------------|-------------|
| T02.01 | Create `checkpoints.py` with `extract_checkpoint_paths()` | S | Low | STANDARD | 85% | None |
| T02.02 | Add `PASS_MISSING_CHECKPOINT` to `PhaseStatus` enum | XS | Low | LIGHT | 90% | None |
| T02.03 | Add `write_checkpoint_verification()` to `logging_.py` | XS | Very Low | LIGHT | 95% | None |
| T02.04 | Wire `_verify_checkpoints()` into executor.py phase completion | M | Low | STANDARD | 85% | T02.01, T02.02, T02.03 |

**T02.01 Details**:
- Creates new file `src/superclaude/cli/sprint/checkpoints.py`
- `extract_checkpoint_paths(phase_file, release_dir) -> list[tuple[str, Path]]`
- `verify_checkpoint_files(paths) -> list[tuple[str, Path, bool]]`
- Handles edge cases: no checkpoint sections, relative paths, missing release_dir
- **Source**: `tasklist-checkpoint-enforcement.md`, T02.01 (lines 132-171)

**T02.02 Details**:
- Add `PASS_MISSING_CHECKPOINT = "pass_missing_checkpoint"` to `PhaseStatus` enum
- `is_failure` returns `False` for this status
- Add `checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` to config
- **Source**: `tasklist-checkpoint-enforcement.md`, T02.02 (lines 174-209)

**T02.03 Details**:
- Add structured JSONL event method to sprint logger
- Event type: `checkpoint_verification` with expected/found/missing lists
- **Source**: `tasklist-checkpoint-enforcement.md`, T02.03 (lines 212-247)

**T02.04 Details**:
- **Replaces** T01.02's `_warn_missing_checkpoints()` with full `_verify_checkpoints()`
- Imports from `checkpoints.py` (shared module)
- Respects `checkpoint_gate_mode`: off/shadow/soft/full
- Shadow mode = JSONL event only, no visible output, no status change
- Full mode = downgrade PASS to `PASS_MISSING_CHECKPOINT`
- **Source**: `tasklist-checkpoint-enforcement.md`, T02.04 (lines 250-295)

**Checkpoint**: End of Phase 2 verifies shadow mode is operational with zero behavioral change.
**Source**: `tasklist-checkpoint-enforcement.md`, lines 298-312

### Phase 3 -- Checkpoint Manifest, CLI Verify & Auto-Recovery (Wave 3)

**Goal**: Manifest tracking, CLI verification command, and auto-recovery from evidence artifacts.
**Ship target**: 1-2 weeks after Wave 2
**Risk**: Medium
**Files**: `checkpoints.py` (extend), `commands.py`, `executor.py`, `models.py`
**LOC**: ~200 incremental
**Dependencies**: Phase 2 complete (`checkpoints.py` exists)

| Task ID | Description | Effort | Risk | Tier | Confidence | Dependencies |
|---------|-------------|--------|------|------|------------|-------------|
| T03.01 | Add `CheckpointEntry` dataclass to `models.py` | XS | Very Low | LIGHT | 95% | None |
| T03.02 | Extend `checkpoints.py` with `build_manifest()` and `write_manifest()` | M | Low-Med | STANDARD | 80% | None |
| T03.03 | Add `recover_missing_checkpoints()` to `checkpoints.py` | M | Medium | STANDARD | 75% | None |
| T03.04 | Add `verify-checkpoints` CLI subcommand to `commands.py` | S | Low | STANDARD | 85% | None |
| T03.05 | Wire manifest build/verify into executor.py sprint lifecycle | S | Low | STANDARD | 85% | T03.02 |

**T03.01 Details**:
- `CheckpointEntry` dataclass: phase, name, expected_path, exists, recovered, recovery_source
- **Source**: `tasklist-checkpoint-enforcement.md`, T03.01 (lines 323-359)

**T03.02 Details**:
- `build_manifest(tasklist_index, release_dir) -> list[CheckpointEntry]`
- `write_manifest(entries, output_path)` writes `manifest.json` with summary + entries
- Must identify all 8 expected checkpoints in OntRAG (7 end-of-phase + 1 mid-phase P3)
- **Source**: `tasklist-checkpoint-enforcement.md`, T03.02 (lines 362-401)

**T03.03 Details**:
- `recover_missing_checkpoints(manifest, artifacts_dir, phase_tasklists) -> list[CheckpointEntry]`
- Generates checkpoint files from deliverable evidence with `## Note: Auto-Recovered` header
- Idempotent; does not overwrite existing files
- Lowest confidence task at 75% — highest risk in entire implementation
- **Source**: `tasklist-checkpoint-enforcement.md`, T03.03 (lines 404-449)

**T03.04 Details**:
- `superclaude sprint verify-checkpoints <dir>` subcommand
- Flags: `--recover` (trigger auto-recovery), `--json` (machine-readable output)
- Works retroactively on sprints run before this feature existed
- **Source**: `tasklist-checkpoint-enforcement.md`, T03.04 (lines 452-495)

**T03.05 Details**:
- Build manifest at sprint start (expectation tracking)
- Finalize and write manifest at sprint end
- Emit `checkpoint_manifest` JSONL event
- **Source**: `tasklist-checkpoint-enforcement.md`, T03.05 (lines 498-533)

**Checkpoint**: End of Phase 3 verifies Waves 1-3 are all operational (prevention + detection + remediation).
**Source**: `tasklist-checkpoint-enforcement.md`, lines 536-548

### Phase 4 -- Tasklist-Level Checkpoint Normalization (Wave 4)

**Goal**: Eliminate the structural root cause for all future tasklists.
**Ship target**: Next release cycle
**Risk**: Low-Medium (breaking change for existing tasklists)
**Files**: `SKILL.md` (sc-tasklist-protocol)
**LOC**: ~200
**Dependencies**: Phases 1-3 complete (provide interim coverage)
**Note**: Breaking change — existing tasklists retain `### Checkpoint:` headings; Waves 1-3 handle them.

| Task ID | Description | Effort | Risk | Tier | Confidence | Dependencies |
|---------|-------------|--------|------|------|------------|-------------|
| T04.01 | Update SKILL.md checkpoint generation rules | M | Low-Med | STANDARD | 80% | None |
| T04.02 | Add checkpoint task validation to Sprint Compatibility Self-Check | S | Low | STANDARD | 85% | T04.01 |
| T04.03 | Update deliverable registry guidance for checkpoint deliverables | XS | Very Low | LIGHT | 90% | None |

**T04.01 Details**:
- Convert `### Checkpoint:` sections to `### T<PP>.<NN> -- Checkpoint:` task entries
- Checkpoint tasks get full MDTM metadata (Effort=XS, Risk=Low, Tier=LIGHT)
- End-of-phase checkpoint always last task; mid-phase at specified boundary
- Example for Phase 3: T03.01-T03.05 (tasks), T03.06 (mid-checkpoint), T03.07 (task), T03.08 (end-checkpoint)
- **Source**: `tasklist-checkpoint-enforcement.md`, T04.01 (lines 560-604)

**T04.02 Details**:
- Three new validation rules in Sprint Compatibility Self-Check
- Catches: missing checkpoint task entries, misplaced checkpoint tasks, missing report path references
- **Source**: `tasklist-checkpoint-enforcement.md`, T04.02 (lines 608-642)

**T04.03 Details**:
- Add checkpoint deliverable type: `D-CP<PP>[-MID]`
- Default paths: `checkpoints/CP-P<PP>-END.md` or `checkpoints/CP-P<PP>-<NAME>.md`
- **Source**: `tasklist-checkpoint-enforcement.md`, T04.03 (lines 645-678)

**Checkpoint**: End of Phase 4 verifies all 4 waves are operational and all 3 root causes are addressed.
**Source**: `tasklist-checkpoint-enforcement.md`, lines 681-699

---

## 6. Rollout Strategy

### Timeline: Shadow -> Soft -> Full Progression

```
Day 1:     Wave 1 deployed (prompt fix + executor warning)
           -> All future sprints benefit immediately
           -> Existing tasklists benefit without regeneration

Day 2-5:   Wave 2 deployed (checkpoint gate in shadow mode)
           -> Per-phase verification logging begins
           -> No behavioral change; data collection only

Day 5-10:  Wave 3 deployed (manifest + CLI + auto-recovery)
           -> verify-checkpoints CLI available
           -> Run retroactively on OntRAG R0+R1 sprint output

Day 10:    Promote Wave 2 gate from shadow -> soft
           -> Operators see on-screen warnings for missing checkpoints
           -> Sprint still continues (no halt)

Sprint +2: Promote Wave 2 gate from soft -> full
           -> Missing checkpoints halt the sprint
           -> Wave 3 auto-recovery available as remediation path

Next release: Wave 4 deployed (tasklist normalization)
              -> All new tasklists use T-numbered checkpoint tasks
              -> Prompt instructions (Wave 1) remain as belt-and-suspenders
```

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Rollout Strategy" (lines 199-224)

### Configuration

Added to `SprintConfig` in `models.py`:

```python
checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```

| Mode | Behavior |
|------|----------|
| `off` | No checkpoint verification (backward-compatible escape hatch) |
| `shadow` | Verify + log to JSONL only (data collection) |
| `soft` | Verify + log + on-screen warning (operator awareness) |
| `full` | Verify + log + downgrade PASS to `PASS_MISSING_CHECKPOINT` (hard gate) |

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Configuration" (lines 226-237)

### Key Design Decisions

1. **Shadow-first rollout**: Gate defaults to shadow because path resolution bugs could cause false positives. Shadow mode validates extraction logic against real sprints before affecting behavior.
2. **Warning-only in Wave 1**: The `_warn_missing_checkpoints()` helper is deliberately warning-only, not a gate. Zero risk of breaking existing sprints. Proper gate comes in Wave 2.
3. **Wave 4 deferred, not dropped**: Solution 2 is the strongest structural fix but is a breaking change. Waves 1-3 provide equivalent coverage for existing tasklists.
4. **Auto-recovery is opt-in**: `--recover` flag is never invoked automatically. Recovery requires explicit user intent because auto-generated checkpoints are lower fidelity.

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Key Design Decisions" (lines 287-297)

---

## 7. Risk Register

| # | Risk | Wave | Severity | Mitigation |
|---|------|------|----------|------------|
| 1 | Agent ignores prompt instructions despite Wave 1 | 1 | Medium | Waves 2+3 detect and remediate |
| 2 | Path resolution bugs cause false positives in Wave 2 | 2 | Medium | Shadow mode means no behavioral impact; fix before promoting to soft/full |
| 3 | Numbering cascade errors in Wave 4 | 4 | Low-Med | Self-check validation rule catches errors before tasklist write; Wave 1 prompt still works as fallback |
| 4 | Auto-recovery produces low-quality checkpoints | 3 | Low | "Auto-Recovered" header + `recovered: true` manifest flag distinguishes them |
| 5 | Existing OntRAG tasklists incompatible with Wave 4 | 4 | Low | Waves 1-3 already provide full coverage for existing tasklists; Wave 4 applies to new generation only |
| 6 | Context pressure (large phases) causes agent to skip prompt instructions | 1 | Medium | Wave 2 gate catches this; contributing factor documented in RCA (744KB output) |
| 7 | Downstream consumers exhaustively matching PhaseStatus break on new enum value | 2 | Low | T02.02 includes grep for exhaustive matches as verification step |

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Risk Mitigation" (lines 239-248); `troubleshoot-missing-p03-checkpoint.md`, Section 6 (lines 184-192)

---

## 8. Success Metrics

| Metric | Current | Target | Measured By |
|--------|---------|--------|-------------|
| Checkpoint write rate | 86% (6/7 phases) | 100% | JSONL `checkpoint_verification` events from Wave 2 |
| False positive rate in gate | N/A | 0% over 2 sprint cycles | Wave 2 shadow mode data |
| Time to detect missing checkpoint | Manual inspection (~24h) | <1 second | Wave 2 gate runs at phase completion |
| Time to recover missing checkpoint | ~30 minutes (manual) | <5 seconds | Wave 3 `--recover` CLI |
| All three root causes addressed | 0/3 | 3/3 | Wave 1 (Cause 1) + Wave 4 (Cause 2) + Waves 2+3 (Cause 3) |

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Success Criteria" (lines 249-257)

---

## 9. File Inventory

### Complete List of Files Created/Modified

| File | Wave(s) | Action | Purpose |
|------|---------|--------|---------|
| `src/superclaude/cli/sprint/process.py` | 1 | MODIFY | Add checkpoint instructions to `build_prompt()` |
| `src/superclaude/cli/sprint/executor.py` | 1, 2, 3 | MODIFY | Wave 1: warning helper; Wave 2: gate call site; Wave 3: manifest build+verify |
| `src/superclaude/cli/sprint/checkpoints.py` | 2, 3 | CREATE | Shared path extraction (Wave 2), manifest + verify + recovery (Wave 3) |
| `src/superclaude/cli/sprint/models.py` | 2, 3 | MODIFY | Wave 2: `PASS_MISSING_CHECKPOINT` enum, `checkpoint_gate_mode` config; Wave 3: `CheckpointEntry` dataclass |
| `src/superclaude/cli/sprint/logging_.py` | 2 | MODIFY | `write_checkpoint_verification()` method |
| `src/superclaude/cli/sprint/commands.py` | 3 | MODIFY | `verify-checkpoints` subcommand |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 4 | MODIFY | Checkpoint normalization rules, self-check rules, deliverable registry |

**Totals**: 7 files (1 new, 6 modified), ~580 LOC across all 4 waves.

**Source**: `unified-checkpoint-enforcement-proposal.md`, "Files Changed (Complete Inventory)" (lines 259-272)

---

## 10. Cross-References

### Connection to Sprint TUI v2 Work

The checkpoint enforcement feature is being planned under the `v3.7-task-unified-v2` release backlog. The tasklist (`tasklist-checkpoint-enforcement.md`) is explicitly marked as `sc:task-unified compatible` (line 7), meaning it follows the MDTM task format and can be executed by the Sprint CLI's task-unified pipeline.

The implementation directly modifies Sprint CLI core files (`process.py`, `executor.py`, `models.py`, `logging_.py`, `commands.py`), which are the same files that the Sprint TUI v2 work targets. **Coordination required** to avoid merge conflicts, particularly in `executor.py` which is modified across Waves 1, 2, and 3.

### Connection to Naming Consolidation Work

[LOW CONFIDENCE] The source documents do not explicitly reference naming consolidation work. However, Wave 4 (tasklist normalization) introduces a new naming convention for checkpoint tasks (`### T<PP>.<NN> -- Checkpoint:`) and checkpoint deliverables (`D-CP<PP>[-MID]`). If there is parallel naming consolidation work, these conventions should be aligned.

### Connection to v3.6-Cli-portify-fix

This analysis is placed in the `v3.6-Cli-portify-fix` current release directory. The sprint-runner-bugfix-workflow.md already present in this directory may relate to the same sprint executor fixes. [LOW CONFIDENCE] The relationship between the CLI portify fix and checkpoint enforcement is not explicitly stated in the source documents.

---

## 11. Open Questions / Gaps

### Questions Not Fully Addressed in Source Documents

1. **Test strategy**: The tasklist specifies verification methods per task (unit test, integration test, manual inspection) but does not include dedicated test tasks. There is no `tests/` file in the file inventory. **How will the ~580 LOC of new code be tested?** The tasklist assumes tests are written inline within each task's verification step, but there is no explicit test file creation task or test coverage target.

2. **Rollback granularity**: Each task specifies a rollback command (`git checkout -- <file>`), but Wave 2's T02.04 replaces Wave 1's `_warn_missing_checkpoints()` with `_verify_checkpoints()`. Rolling back Wave 2 without re-applying Wave 1 would leave the executor without any checkpoint awareness. **The rollback strategy is per-task but does not address cross-wave rollback dependencies.**

3. **Phase 3 context pressure mitigation**: The RCA identifies 744KB output as a contributing factor (RCA Section 6). None of the 4 solutions directly addresses context pressure. Solutions 1 and 2 make checkpoint writing more likely under pressure, but a very large phase could still cause an agent to truncate or skip late instructions. **Is there a token budget or context window guard that should be considered?**

4. **Mid-phase checkpoint handling in the gate**: Wave 2's checkpoint gate verifies checkpoints after phase completion. Phase 3 has a mid-phase checkpoint (CP-P03-T01-T05) that should be written mid-execution. **The post-phase gate can only detect the absence of the mid-phase checkpoint after the fact, not enforce it at the correct execution point.** This is partially addressed by Wave 4 (converting mid-phase checkpoints to tasks), but for existing tasklists, mid-phase checkpoint enforcement is weaker than end-of-phase enforcement.

5. **Concurrent sprint execution**: The source documents do not discuss what happens when multiple sprints run concurrently and share the same checkpoint directory structure. [LOW CONFIDENCE] This may not be a real concern if sprints use isolated output directories.

6. **`_check_checkpoint_pass()` refactoring**: The RCA identifies that `_check_checkpoint_pass()` (executor.py:1592-1603) exists but is only used for crash recovery. The implementation plan creates `_verify_checkpoints()` (T02.04) but does not explicitly refactor or remove `_check_checkpoint_pass()`. **Are there two overlapping checkpoint-checking functions in executor.py after Wave 2?** The tasklist is silent on whether the old function should be consolidated.

7. **Manifest schema stability**: Wave 3 introduces `manifest.json` but does not specify a schema version field. If the manifest format evolves, consumers of `manifest.json` need a way to distinguish versions.

8. **Wave 4 migration path for in-flight tasklists**: The proposal notes Solution 2 is a breaking change (line 48: "Existing tasklists with `### Checkpoint:` headings will NOT be processed as tasks. Requires regeneration or manual patching.") but does not provide a migration script or guide for converting existing tasklists. Waves 1-3 handle them, but there is no documented path for operators who want to opt in to the new format early.

### Confidence Assessment by Task

| Task | Stated Confidence | Analyst Assessment | Notes |
|------|------------------|-------------------|-------|
| T01.01 | 95% | Reasonable | String additions, very low risk |
| T01.02 | 90% | Reasonable | New function, no side effects |
| T02.01 | 85% | Reasonable | Path resolution edge cases noted |
| T02.02 | 90% | Reasonable | Additive enum change |
| T02.03 | 95% | Reasonable | Follows existing patterns |
| T02.04 | 85% | Reasonable | Integration point, but well-scoped |
| T03.01 | 95% | Reasonable | Simple dataclass |
| T03.02 | 80% | Reasonable | Multi-phase scanning, JSON serialization |
| T03.03 | 75% | **Slightly optimistic** | Evidence scanning + template generation is underspecified; recovery quality depends on evidence file format consistency |
| T03.04 | 85% | Reasonable | Standard CLI subcommand |
| T03.05 | 85% | Reasonable | Well-defined integration points |
| T04.01 | 80% | Reasonable | Numbering cascade is the real risk |
| T04.02 | 85% | Reasonable | Rule-based validation |
| T04.03 | 90% | Reasonable | Documentation change only |

**Highest-risk task**: T03.03 (auto-recovery) at 75% confidence. The recovery template generation depends on evidence file format consistency, which is not formally specified. If evidence files vary in structure across phases, the recovery function may produce inconsistent output.

---

## Appendix: Source Document Index

| Document | Path | Purpose | Lines |
|----------|------|---------|-------|
| Root Cause Analysis | `.dev/releases/backlog/v3.7-task-unified-v2/troubleshoot-missing-p03-checkpoint.md` | Triple failure chain analysis, failure path trace, enforcement gap locations | 222 |
| Unified Proposal | `.dev/releases/backlog/v3.7-task-unified-v2/unified-checkpoint-enforcement-proposal.md` | Adversarial 6-criterion comparison + merged 4-wave architecture | 298 |
| Implementation Tasklist | `.dev/releases/backlog/v3.7-task-unified-v2/tasklist-checkpoint-enforcement.md` | 15 tasks across 4 phases with full MDTM metadata | 700 |
