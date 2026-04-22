# Unified Checkpoint Enforcement Proposal

**Date**: 2026-03-23
**Author**: Claude Opus 4.6 (Adversarial Compare + Merge)
**Inputs**: `design-proposals-A.md` (Solutions 1-2), `design-proposals-B.md` (Solutions 3-4)
**Root Cause**: `troubleshoot-missing-p03-checkpoint.md`

---

## Part 1: Adversarial Comparison

### Solution Summary

| # | Name | Source | Core Mechanism | Root Causes Addressed |
|---|------|--------|----------------|----------------------|
| 1 | Prompt-Level Checkpoint Enforcement | proposals-A | Add checkpoint instructions to `build_prompt()` | Cause 1 (primary) |
| 2 | Tasklist-Level Checkpoint Normalization | proposals-A | Convert `### Checkpoint:` to `### T<NN>.<NN>` task entries | Cause 2 (structural) |
| 3 | Post-Phase Checkpoint Enforcement Gate | proposals-B | Executor verifies checkpoint files exist after phase PASS | Cause 3 (pipeline) |
| 4 | Checkpoint Observability & Auto-Recovery | proposals-B | Manifest tracking + CLI verify + auto-recovery from evidence | Cause 3 (pipeline) + operational gap |

### Criterion 1: Effectiveness

| Solution | Rating | Analysis |
|----------|--------|----------|
| **1 (Prompt)** | **HIGH** | Directly addresses Cause 1 — the agent will be explicitly instructed to write checkpoints. However, relies on agent compliance; a context-pressured agent (like P3's 744KB output) could still skip instructions. Estimated failure rate drops from ~14% (1/7 phases) to ~5%. |
| **2 (Tasklist)** | **VERY HIGH** | Eliminates Cause 2 entirely. Checkpoints become structurally indistinguishable from tasks. The agent's task scanner processes them unconditionally — no discretion, no interpretation. Estimated failure rate drops to <1% (only if the agent crashes mid-task). |
| **3 (Gate)** | **MEDIUM** | Does not prevent the failure — detects it after the fact. In `full` mode, halts the sprint so a human can intervene, but the checkpoint is still missing. In `shadow`/`soft` mode, merely logs. Value is as a safety net, not a fix. |
| **4 (Recovery)** | **MEDIUM** | Does not prevent the failure. Provides automated remediation, but recovered checkpoints are synthesized from evidence files and may miss agent-observed nuances. Value is operational efficiency (30-minute manual recovery -> 1 CLI command). |

**Verdict**: Solutions 1+2 are *preventive* (fix the root causes). Solutions 3+4 are *detective/corrective* (catch and remediate failures that slip through). Maximum effectiveness requires at least one from each category.

### Criterion 2: Implementation Complexity

| Solution | LOC (est.) | Files Modified | Files Created | Risk of Introducing Bugs |
|----------|-----------|----------------|---------------|-------------------------|
| **1 (Prompt)** | ~60 | 2 (`process.py`, `executor.py`) | 0 | **Very Low** — string additions to prompt template + new helper function with no side effects |
| **2 (Tasklist)** | ~200 | 1 (`SKILL.md`) | 0 | **Low-Medium** — changes tasklist generation rules; numbering cascade logic must be correct; self-check rule catches errors |
| **3 (Gate)** | ~80 | 3 (`executor.py`, `models.py`, `logging_.py`) | 0 | **Low** — new enum value + new function + call site insertion; well-isolated |
| **4 (Recovery)** | ~290 | 3 (`executor.py`, `commands.py`, `logging_.py`) | 1 (`checkpoints.py`) | **Medium** — new module with path resolution, evidence scanning, and template generation; most complex of the four |

**Verdict**: Solutions 1 and 3 are the lightest-weight. Solution 2 is moderate. Solution 4 is the heaviest but provides the most operational value per line of code.

### Criterion 3: Backward Compatibility

| Solution | Compatible? | Impact on Existing Artifacts |
|----------|-------------|------------------------------|
| **1 (Prompt)** | **Fully** | No changes to tasklist format, result file contract, or executor behavior. Phases without `### Checkpoint:` sections are unaffected (prompt instructions are a no-op). |
| **2 (Tasklist)** | **Not compatible** | Existing tasklists with `### Checkpoint:` headings will NOT be processed as tasks. Requires regeneration or manual patching. The current OntRAG R0+R1 tasklists would need rework. |
| **3 (Gate)** | **Fully** (in `shadow` default) | New JSONL event type is additive. New `PhaseStatus` enum value requires downstream consumers that exhaustively match on status to add a case — but the `shadow` default means no behavioral change. |
| **4 (Recovery)** | **Fully** | New module, new CLI command, new `manifest.json` file. All additive. Works retroactively on sprints run before this feature existed. |

**Verdict**: Solutions 1, 3, and 4 are deploy-and-forget. Solution 2 is a breaking change for in-flight work and requires a migration path.

### Criterion 4: Defense in Depth

The root cause is a triple failure chain. Each solution addresses different links:

| Solution | Cause 1 (No prompt) | Cause 2 (Structural mismatch) | Cause 3 (No enforcement) |
|----------|---------------------|-------------------------------|--------------------------|
| **1 (Prompt)** | **FIXES** | Mitigates (agent told to look for `### Checkpoint:`) | Partially (adds executor warning) |
| **2 (Tasklist)** | Not needed (structural fix) | **ELIMINATES** | Not addressed |
| **3 (Gate)** | Not addressed | Not addressed | **FIXES** (detection) |
| **4 (Recovery)** | Not addressed | Not addressed | **FIXES** (detection + remediation) |

**Verdict**: No single solution addresses all three causes. The minimum set for full coverage is Solution 1 + Solution 3 (or 4). Adding Solution 2 provides structural elimination of Cause 2, making Cause 1's fix redundant for new tasklists but still valuable for old ones.

### Criterion 5: Time to Value

| Solution | Estimated Implementation Time | Can Ship Independently? |
|----------|------------------------------|------------------------|
| **1 (Prompt)** | 1-2 hours | **Yes** — zero dependencies on other solutions |
| **2 (Tasklist)** | 4-6 hours (incl. testing numbering cascade) | **Yes** — but requires tasklist regeneration |
| **3 (Gate)** | 2-3 hours | **Yes** — zero dependencies |
| **4 (Recovery)** | 4-6 hours (incl. CLI tests) | **Yes** — zero dependencies |

**Verdict**: Solution 1 is the fastest win. Solution 3 is second. Solutions 2 and 4 are roughly equivalent in effort but Solution 4 provides immediate retroactive value.

### Criterion 6: Operational Overhead

| Solution | Added Burden on Users/Operators |
|----------|--------------------------------|
| **1 (Prompt)** | **None** — invisible to users. Prompt changes are internal to the sprint runner. |
| **2 (Tasklist)** | **Low** — task count increases (e.g., P3 goes from 6 to 8 tasks). Checkpoint tasks consume agent tokens. Users see more tasks in tasklists but no action required. |
| **3 (Gate)** | **Low** — `shadow`/`soft` mode adds log lines only. `full` mode adds sprint halts that require investigation. Operators must understand `PASS_MISSING_CHECKPOINT` status. |
| **4 (Recovery)** | **Low** — `manifest.json` is auto-generated. `verify-checkpoints` CLI is opt-in. No mandatory new steps in the workflow. |

**Verdict**: All solutions have minimal operational overhead. Solution 3 in `full` mode is the only one that changes operator workflows (sprint halts).

### Complementary vs. Alternative Analysis

| Pair | Relationship | Rationale |
|------|-------------|-----------|
| 1 + 2 | **Complementary (belt + suspenders)** | Solution 1 teaches the agent about checkpoints via prompt. Solution 2 makes checkpoints structurally identical to tasks. Together: even if the prompt instructions fail, the task structure catches it; even if task normalization is not applied (old tasklists), the prompt catches it. |
| 1 + 3 | **Complementary (prevent + detect)** | Solution 1 prevents the failure. Solution 3 detects if prevention failed. Different layers, no overlap. |
| 1 + 4 | **Complementary (prevent + remediate)** | Solution 1 prevents. Solution 4 remediates if prevention + detection missed it. Different lifecycle phases. |
| 2 + 3 | **Complementary (structural + runtime)** | Solution 2 eliminates the structural cause. Solution 3 provides runtime verification. Useful together because Solution 2 only applies to new tasklists. |
| 3 + 4 | **Complementary (detect + remediate)** | Solution 3 detects during sprint. Solution 4 provides post-sprint audit + recovery. The `_extract_checkpoint_paths()` logic in both can be shared/unified to avoid duplication. |
| 2 vs. 1 | **Partially alternative** | If Solution 2 is fully deployed, Solution 1's checkpoint instructions become redundant for new tasklists. However, Solution 1 remains necessary for backward compatibility with old-format tasklists. |

**Key finding**: All four solutions are complementary. None is a strict alternative to another. The redundancy between Solutions 1 and 2 is desirable (defense in depth), not wasteful.

### Redundancy to Eliminate

Both Solution 3 (`_extract_checkpoint_paths()` in executor.py) and Solution 4 (`build_manifest()` in checkpoints.py) independently parse phase tasklists for `Checkpoint Report Path:` entries. This is the primary code duplication.

**Resolution**: Solution 4's `build_manifest()` is a superset of Solution 3's path extraction. The unified proposal should have Solution 3 call into Solution 4's module rather than maintaining separate parsing logic:
- `checkpoints.py` provides `extract_checkpoint_paths()` as a public function
- `_verify_checkpoints()` in executor.py imports and calls it
- Both the per-phase gate (Solution 3) and post-sprint verification (Solution 4) use the same parsing code

---

## Part 2: Unified Merged Proposal

### Architecture: Three-Layer Checkpoint Enforcement

The unified design implements checkpoint enforcement as three concentric layers, each independent and each sufficient to catch the failure on its own:

```
Layer 1 — PREVENTION (Agent-Side)
  Solution 1: Prompt instructions tell the agent to write checkpoints
  Solution 2: Tasklist structure makes checkpoints indistinguishable from tasks
  -> Agent writes checkpoints as part of normal task execution

Layer 2 — DETECTION (Executor-Side, Real-Time)
  Solution 3: Post-phase gate verifies checkpoint files exist on disk
  -> Sprint halts (or warns) if agent failed to write them

Layer 3 — REMEDIATION (Post-Sprint, On-Demand)
  Solution 4: CLI verify + auto-recovery from evidence artifacts
  -> Missing checkpoints are detected, audited, and optionally regenerated
```

Any single layer failing is caught by the next. All three must fail simultaneously for a checkpoint to go permanently unwritten — and even then, the manifest provides observability.

### Implementation Sequence

#### Wave 1: Immediate (ship within 1 day)

**Solution 1 — Prompt-Level Checkpoint Enforcement**

- Modify `build_prompt()` in `process.py` to add `## Checkpoints` section
- Amend `## Scope Boundary` to include "AND writing all checkpoint reports"
- Amend `## Result File` to include "after all checkpoints"
- Add `_warn_missing_checkpoints()` helper to `executor.py` (warning-only, no status change)
- **Files**: `process.py`, `executor.py`
- **LOC**: ~60
- **Risk**: Very Low
- **Backward compatible**: Yes

This is the highest-value, lowest-risk change. It transforms checkpoint writing from emergent to instructed behavior for ALL existing and future tasklists without any format changes.

#### Wave 2: Near-term (ship within 1 week)

**Solution 3 (merged with Solution 4 path extraction) — Post-Phase Checkpoint Gate**

- Create `checkpoints.py` with `extract_checkpoint_paths()` function (shared by both Solutions 3 and 4)
- Add `_verify_checkpoints()` to `executor.py`, importing from `checkpoints.py`
- Add `PASS_MISSING_CHECKPOINT` to `PhaseStatus` enum in `models.py`
- Add `checkpoint_gate_mode` config field (default: `shadow`)
- Add `write_checkpoint_verification()` to `logging_.py`
- **Files**: `checkpoints.py` (new), `executor.py`, `models.py`, `logging_.py`
- **LOC**: ~120
- **Risk**: Low
- **Backward compatible**: Yes (shadow default)

Deploy in `shadow` mode. This gathers data on checkpoint completeness without affecting sprint behavior. Promote to `soft` after 2 sprint cycles, then `full` after confirming zero false positives.

#### Wave 3: Near-term (ship within 1-2 weeks, after Wave 2)

**Solution 4 (remainder) — Checkpoint Manifest + CLI + Auto-Recovery**

- Extend `checkpoints.py` with `build_manifest()`, `verify_checkpoints()`, `recover_missing_checkpoints()`, `write_manifest()`
- Add `verify-checkpoints` CLI subcommand to `commands.py`
- Add manifest build at sprint start and verify at sprint end in `executor.py`
- Add `CheckpointEntry` dataclass to `models.py`
- **Files**: `checkpoints.py` (extend), `commands.py`, `executor.py`, `models.py`
- **LOC**: ~200 incremental
- **Risk**: Medium (path resolution, evidence scanning)
- **Backward compatible**: Yes

This extends Wave 2's `checkpoints.py` module. The `verify-checkpoints` CLI is immediately useful retroactively on past sprints.

#### Wave 4: Next release cycle (ship with next tasklist generation)

**Solution 2 — Tasklist-Level Checkpoint Normalization**

- Modify `sc-tasklist-protocol/SKILL.md` to emit checkpoints as `### T<PP>.<TT> -- Checkpoint:` entries
- Add validation rule to Sprint Compatibility Self-Check
- Update deliverable registry guidance for checkpoint deliverables
- **Files**: `SKILL.md` (1 file, ~200 lines of changes)
- **LOC**: ~200
- **Risk**: Low-Medium (numbering cascade)
- **Backward compatible**: No (new tasklists only)

This is deferred because: (a) it is a breaking change for existing tasklists, (b) Waves 1-3 already provide full prevention + detection + remediation coverage, and (c) it requires a full tasklist generation cycle to validate. Solution 2 becomes the *structural hardening* that eliminates Cause 2 for all future sprints.

### Rollout Strategy

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

### Configuration

Add to `SprintConfig` in `models.py`:

```python
checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```

- **off**: No checkpoint verification (backward-compatible escape hatch)
- **shadow**: Verify + log to JSONL only (data collection)
- **soft**: Verify + log + on-screen warning (operator awareness)
- **full**: Verify + log + downgrade PASS to PASS_MISSING_CHECKPOINT (hard gate)

### Risk Mitigation

| Risk | Wave | Mitigation |
|------|------|------------|
| Agent ignores prompt instructions despite Wave 1 | 1 | Waves 2+3 detect and remediate |
| Path resolution bugs cause false positives in Wave 2 | 2 | Shadow mode means no behavioral impact; fix before promoting to soft/full |
| Numbering cascade errors in Wave 4 | 4 | Self-check validation rule catches errors before tasklist write; Wave 1 prompt instructions still work as fallback |
| Auto-recovery produces low-quality checkpoints | 3 | "Auto-Recovered" header + `recovered: true` manifest flag distinguishes them from agent-written checkpoints |
| Existing OntRAG tasklists incompatible with Wave 4 | 4 | Waves 1-3 already provide full coverage for existing tasklists; Wave 4 only applies to new tasklist generation |

### Success Criteria

| Metric | Target | Measured By |
|--------|--------|-------------|
| Checkpoint write rate | 100% (currently 86% = 6/7) | JSONL `checkpoint_verification` events from Wave 2 |
| False positive rate in gate | 0% over 2 sprint cycles | Wave 2 shadow mode data |
| Time to detect missing checkpoint | <1 second (currently: manual inspection) | Wave 2 gate runs at phase completion |
| Time to recover missing checkpoint | <5 seconds (currently: ~30 minutes manual) | Wave 3 `--recover` CLI |
| All three root causes addressed | Yes | Wave 1 (Cause 1) + Wave 4 (Cause 2) + Waves 2+3 (Cause 3) |

### Files Changed (Complete Inventory)

| File | Wave | Action | Purpose |
|------|------|--------|---------|
| `src/superclaude/cli/sprint/process.py` | 1 | MODIFY | Add checkpoint instructions to `build_prompt()` |
| `src/superclaude/cli/sprint/executor.py` | 1,2,3 | MODIFY | Wave 1: warning helper; Wave 2: gate call site; Wave 3: manifest build+verify |
| `src/superclaude/cli/sprint/checkpoints.py` | 2,3 | CREATE | Shared path extraction (Wave 2), manifest + verify + recovery (Wave 3) |
| `src/superclaude/cli/sprint/models.py` | 2,3 | MODIFY | Wave 2: `PASS_MISSING_CHECKPOINT` enum; Wave 3: `CheckpointEntry` dataclass, `checkpoint_gate_mode` config |
| `src/superclaude/cli/sprint/logging_.py` | 2 | MODIFY | `write_checkpoint_verification()` method |
| `src/superclaude/cli/sprint/commands.py` | 3 | MODIFY | `verify-checkpoints` subcommand |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 4 | MODIFY | Checkpoint normalization rules |

**Total estimated LOC**: ~580 across all 4 waves
**Total files**: 7 (1 new, 6 modified)

---

## Part 3: Decision Record

### Selected Elements Per Solution

| Solution | What We Take | What We Skip | Rationale for Skip |
|----------|-------------|-------------|-------------------|
| **1** | Full prompt changes + scope boundary amendment + result file amendment + executor warning helper | Nothing skipped | Fully adopted as Wave 1 |
| **2** | Full tasklist normalization + self-check rule + deliverable registry guidance | Nothing skipped; deferred to Wave 4 | Breaking change; needs migration path; Waves 1-3 provide interim coverage |
| **3** | `_verify_checkpoints()` gate + `PASS_MISSING_CHECKPOINT` enum + `checkpoint_gate_mode` config + shadow/soft/full rollout | Separate `_extract_checkpoint_paths()` in executor.py | Replaced by shared `extract_checkpoint_paths()` in `checkpoints.py` (eliminates duplication with Solution 4) |
| **4** | Full manifest system + CLI + auto-recovery + executor integration | Nothing skipped | Fully adopted as Wave 3 |

### Key Design Decisions

1. **Shared path extraction module**: Solutions 3 and 4 both need to parse `Checkpoint Report Path:` from tasklists. Rather than duplicate this logic, `checkpoints.py` provides it once. Solution 3's per-phase gate imports from it.

2. **Shadow-first rollout for the gate**: The gate (Solution 3) defaults to `shadow` because path resolution bugs could cause false positives. Shadow mode lets us validate the extraction logic against real sprints before it can affect behavior.

3. **Wave 4 deferred, not dropped**: Solution 2's tasklist normalization is the strongest structural fix (eliminates Cause 2 entirely). But it is a breaking change that requires tasklist regeneration. Waves 1-3 provide equivalent coverage for existing tasklists, so Wave 4 can wait for the next release cycle.

4. **Warning-only in Wave 1**: The executor warning added in Wave 1 (`_warn_missing_checkpoints()`) is deliberately warning-only, not a gate. This is because Wave 1 ships immediately and we want zero risk of breaking existing sprints. The proper gate comes in Wave 2 with configurable severity.

5. **Auto-recovery is opt-in**: Wave 3's `--recover` flag is never invoked automatically. Recovery requires explicit user intent because auto-generated checkpoints are lower fidelity than agent-written ones.
