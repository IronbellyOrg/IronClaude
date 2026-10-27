# Checkpoint Enforcement — Unified Release Spec Summary

**Date**: 2026-04-02
**Source Documents**:
1. `troubleshoot-missing-p03-checkpoint.md` — Root cause analysis
2. `unified-checkpoint-enforcement-proposal.md` — Merged 4-solution proposal
3. `tasklist-checkpoint-enforcement.md` — Implementation task list (4 phases, 15 tasks)

---

## A. Problem Statement

### What Happened
During the OntRAG R0+R1 sprint (2026-03-22, 7 phases), Phase 3 (Configuration & Utilities) completed all 6 tasks (T03.01–T03.06) and produced all 6 deliverables (D-0013 through D-0018) but **failed to write either checkpoint file** (CP-P03-T01-T05 mid-phase and CP-P03-END). All other phases (1, 2, 4–7) wrote their checkpoints successfully.

### Impact
- Checkpoint completion rate degraded to 86% (6/7 phases)
- Missing checkpoint files required ~30 minutes of manual retroactive recovery
- Phase 3's quality gate was never formally evaluated, creating an audit gap
- Reliability of the sprint pipeline is undermined: checkpoint writing was revealed to be **emergent, not enforced**

### Root Causes — Triple Failure Chain

| # | Cause | Category | Severity | Location |
|---|-------|----------|----------|----------|
| **1** | Agent prompt contains **no checkpoint instructions** — `build_prompt()` tells the agent to execute T-numbered tasks and STOP; checkpoints are never mentioned | Primary | HIGH | `process.py:169-203` |
| **2** | Phase 3 uniquely has **two checkpoint sections** using `### Checkpoint:` headings that are structurally distinct from the `### T<NN>.<NN>` pattern the agent's task scanner recognizes | Structural | MEDIUM | `phase-3-tasklist.md:285-314` |
| **3** | Sprint executor has **no post-phase checkpoint enforcement** — `_check_checkpoint_pass()` exists but is only used for crash recovery, never as a quality gate | Pipeline | HIGH | `executor.py:1592-1603, 1775-1830` |

### Contributing Factors (Non-Root-Cause)
- Phase 3 output was 744KB (largest phase), increasing context pressure
- Phase 3 agent did not use TodoWrite to track checkpoint writing (Phase 4's agent did)
- Whether agents write checkpoints is nondeterministic — 6/7 did so voluntarily

---

## B. Architecture Overview — Three-Layer Enforcement Model

The unified design implements checkpoint enforcement as three concentric layers, each independent and each sufficient to catch the failure on its own:

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 1 — PREVENTION (Agent-Side)                           │
│    Solution 1: Prompt instructions → agent told to write CPs │
│    Solution 2: Tasklist normalization → CPs = tasks           │
│    Result: Agent writes checkpoints as part of normal work    │
├──────────────────────────────────────────────────────────────┤
│  Layer 2 — DETECTION (Executor-Side, Real-Time)              │
│    Solution 3: Post-phase gate verifies CP files exist        │
│    Result: Sprint halts/warns if agent missed them            │
├──────────────────────────────────────────────────────────────┤
│  Layer 3 — REMEDIATION (Post-Sprint, On-Demand)              │
│    Solution 4: Manifest + CLI verify + auto-recovery          │
│    Result: Missing CPs detected, audited, optionally rebuilt  │
└──────────────────────────────────────────────────────────────┘
```

### Solution-to-Root-Cause Mapping

| Solution | Cause 1 (No prompt) | Cause 2 (Structural) | Cause 3 (No enforcement) |
|----------|:-------------------:|:--------------------:|:------------------------:|
| 1 — Prompt Enforcement | **FIXES** | Mitigates | Partially |
| 2 — Tasklist Normalization | N/A (structural fix) | **ELIMINATES** | — |
| 3 — Post-Phase Gate | — | — | **FIXES** (detection) |
| 4 — Manifest + Recovery | — | — | **FIXES** (detection + remediation) |

All four solutions are **complementary**, not alternatives. The only overlap is between Solutions 1 and 2 (both address agent-side prevention), which is desirable for defense in depth.

---

## C. Implementation Waves

### Wave 1 — Prompt-Level Checkpoint Enforcement

| Attribute | Value |
|-----------|-------|
| **Scope** | Add checkpoint instructions to agent prompt; add warning-only post-phase check |
| **Goal** | Transform checkpoint writing from emergent to instructed behavior |
| **Risk** | Very Low — string additions to prompt template + new helper function |
| **Estimated LOC** | ~60 |
| **Files** | `process.py` (modify), `executor.py` (modify) |
| **Ship Timeline** | Day 1 |
| **Dependencies** | None |

**Tasks:**

| Task ID | Target File | What It Does | Effort |
|---------|-------------|--------------|--------|
| **T01.01** | `process.py` | Add `## Checkpoints` section to `build_prompt()`; amend `## Scope Boundary` and `## Result File` to reference checkpoints | S |
| **T01.02** | `executor.py` | Add `_warn_missing_checkpoints()` helper — parses `Checkpoint Report Path:` from tasklist, checks file existence, logs warnings (no status change) | S |

---

### Wave 2 — Post-Phase Checkpoint Enforcement Gate

| Attribute | Value |
|-----------|-------|
| **Scope** | Executor-level verification after each phase; shared checkpoint path extraction module |
| **Goal** | Detect checkpoint failures at runtime; deploy in shadow mode for data collection |
| **Risk** | Low — new function + enum value + call site; shadow default = no behavioral change |
| **Estimated LOC** | ~120 |
| **Files** | `checkpoints.py` (new), `executor.py` (modify), `models.py` (modify), `logging_.py` (modify) |
| **Ship Timeline** | Day 2–5 |
| **Dependencies** | Wave 1 complete (T01.02 establishes call site pattern) |

**Tasks:**

| Task ID | Target File | What It Does | Effort |
|---------|-------------|--------------|--------|
| **T02.01** | `checkpoints.py` (NEW) | Create shared module with `extract_checkpoint_paths()` and `verify_checkpoint_files()` — parses `Checkpoint Report Path:` from tasklists, resolves paths, checks existence | S |
| **T02.02** | `models.py` | Add `PASS_MISSING_CHECKPOINT` to `PhaseStatus` enum (non-failure); add `checkpoint_gate_mode` config field (default: `"shadow"`) | XS |
| **T02.03** | `logging_.py` | Add `write_checkpoint_verification()` — emits structured `checkpoint_verification` JSONL event | XS |
| **T02.04** | `executor.py` | Wire `_verify_checkpoints()` into phase completion flow — replaces Wave 1's `_warn_missing_checkpoints()` with full gate respecting `checkpoint_gate_mode` (off/shadow/soft/full) | M |

**Dependency chain**: T02.04 depends on T02.01, T02.02, T02.03.

---

### Wave 3 — Checkpoint Manifest, CLI Verify & Auto-Recovery

| Attribute | Value |
|-----------|-------|
| **Scope** | Manifest tracking across entire sprint; CLI verification command; auto-recovery from evidence artifacts |
| **Goal** | Provide post-sprint audit capability and automated remediation |
| **Risk** | Medium — path resolution, evidence scanning, template generation |
| **Estimated LOC** | ~200 incremental |
| **Files** | `checkpoints.py` (extend), `commands.py` (modify), `executor.py` (modify), `models.py` (modify) |
| **Ship Timeline** | Day 5–10 (1–2 weeks after Wave 2) |
| **Dependencies** | Wave 2 complete (`checkpoints.py` exists) |

**Tasks:**

| Task ID | Target File | What It Does | Effort |
|---------|-------------|--------------|--------|
| **T03.01** | `models.py` | Add `CheckpointEntry` dataclass (phase, name, expected_path, exists, recovered, recovery_source) | XS |
| **T03.02** | `checkpoints.py` | Add `build_manifest()` — scans all phase tasklists, returns `CheckpointEntry` list; add `write_manifest()` — writes `manifest.json` | M |
| **T03.03** | `checkpoints.py` | Add `recover_missing_checkpoints()` — generates retroactive checkpoints from deliverable evidence files, marked `Auto-Recovered` | M |
| **T03.04** | `commands.py` | Add `verify-checkpoints` CLI subcommand with `--recover` and `--json` flags; works retroactively on past sprints | S |
| **T03.05** | `executor.py` | Wire manifest build at sprint start + finalize/write at sprint end; emit `checkpoint_manifest` JSONL event | S |

**Dependency chain**: T03.05 depends on T03.02.

---

### Wave 4 — Tasklist-Level Checkpoint Normalization (Deferred)

| Attribute | Value |
|-----------|-------|
| **Scope** | Change tasklist generation to emit checkpoints as T-numbered task entries |
| **Goal** | Structurally eliminate the heading pattern mismatch (Cause 2) for all future tasklists |
| **Risk** | Low-Medium — numbering cascade must be correct; **breaking change** for existing tasklists |
| **Estimated LOC** | ~200 |
| **Files** | `SKILL.md` (sc-tasklist-protocol) |
| **Ship Timeline** | Next release cycle |
| **Dependencies** | Waves 1–3 complete (provide interim coverage for existing tasklists) |

**Tasks:**

| Task ID | Target File | What It Does | Effort |
|---------|-------------|--------------|--------|
| **T04.01** | `SKILL.md` | Update checkpoint generation rules: emit `### T<PP>.<NN> -- Checkpoint:` entries with metadata tables, steps, acceptance criteria | M |
| **T04.02** | `SKILL.md` | Add 3 validation rules to Sprint Compatibility Self-Check for checkpoint task entries | S |
| **T04.03** | `SKILL.md` | Add checkpoint deliverable type (D-CP*) to deliverable registry guidance | XS |

**Dependency chain**: T04.02 depends on T04.01.

---

## D. File Change Inventory

| File Path | Action | Wave(s) | Purpose |
|-----------|--------|---------|---------|
| `src/superclaude/cli/sprint/process.py` | MODIFY | 1 | Checkpoint instructions in `build_prompt()` |
| `src/superclaude/cli/sprint/executor.py` | MODIFY | 1, 2, 3 | W1: warning helper; W2: gate call site; W3: manifest build/verify |
| `src/superclaude/cli/sprint/checkpoints.py` | **CREATE** | 2, 3 | W2: shared path extraction; W3: manifest + verify + recovery |
| `src/superclaude/cli/sprint/models.py` | MODIFY | 2, 3 | W2: `PASS_MISSING_CHECKPOINT` enum + gate config; W3: `CheckpointEntry` dataclass |
| `src/superclaude/cli/sprint/logging_.py` | MODIFY | 2 | `write_checkpoint_verification()` JSONL event |
| `src/superclaude/cli/sprint/commands.py` | MODIFY | 3 | `verify-checkpoints` CLI subcommand |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | MODIFY | 4 | Checkpoint normalization rules, self-check rules, deliverable registry |

**Totals**: 7 files (1 new, 6 modified) · ~580 LOC across all 4 waves

---

## E. Configuration & Rollout

### Gate Modes

Added to `SprintConfig` in `models.py`:

```python
checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```

| Mode | Behavior | Use Case |
|------|----------|----------|
| `off` | No checkpoint verification | Backward-compatible escape hatch |
| `shadow` | Verify + log to JSONL only | **Default** — data collection, zero behavioral change |
| `soft` | Verify + log + on-screen warning | Operator awareness without sprint interruption |
| `full` | Verify + log + downgrade PASS → `PASS_MISSING_CHECKPOINT` | Hard enforcement gate |

### Rollout Timeline

| Day | Action | Gate Mode |
|-----|--------|-----------|
| **Day 1** | Wave 1 deployed — prompt fix + executor warning | N/A (prompt-only) |
| **Day 2–5** | Wave 2 deployed — checkpoint gate active | `shadow` |
| **Day 5–10** | Wave 3 deployed — manifest + CLI + auto-recovery | `shadow` |
| **Day 10** | Promote gate | `shadow` → `soft` |
| **Sprint +2** | Promote gate (after confirming 0 false positives) | `soft` → `full` |
| **Next release** | Wave 4 deployed — tasklist normalization | `full` |

### Success Criteria

| Metric | Current | Target | Measured By |
|--------|---------|--------|-------------|
| Checkpoint write rate | 86% (6/7) | **100%** | JSONL `checkpoint_verification` events (Wave 2) |
| False positive rate in gate | N/A | **0%** over 2 sprint cycles | Wave 2 shadow mode data |
| Time to detect missing CP | Manual inspection | **<1 second** | Wave 2 gate at phase completion |
| Time to recover missing CP | ~30 minutes | **<5 seconds** | Wave 3 `--recover` CLI |
| All 3 root causes addressed | 0/3 | **3/3** | W1 (Cause 1) + W4 (Cause 2) + W2+W3 (Cause 3) |

---

## F. Key Design Decisions

### 1. Shared Path Extraction Module (`checkpoints.py`)
Both Solution 3 (per-phase gate) and Solution 4 (post-sprint manifest) need to parse `Checkpoint Report Path:` from tasklists. Rather than duplicate this logic in two places, a shared `checkpoints.py` module provides `extract_checkpoint_paths()` once. This is the primary code deduplication in the unified proposal.

### 2. Shadow-First Rollout for the Gate
The gate defaults to `shadow` because path resolution bugs could cause false positives. Shadow mode logs JSONL events without any visible output or behavioral change, allowing validation against real sprints before promotion to `soft`/`full`. This ensures zero risk of breaking existing sprint flows on deployment.

### 3. Wave 4 Deferred, Not Dropped
Solution 2 (tasklist normalization) is the strongest structural fix — it eliminates Cause 2 entirely by making checkpoints structurally indistinguishable from tasks. However, it is a **breaking change** that requires tasklist regeneration and does not benefit existing tasklists. Waves 1–3 already provide full prevention + detection + remediation coverage, so Wave 4 can safely wait for the next release cycle.

### 4. Warning-Only in Wave 1
The `_warn_missing_checkpoints()` helper added in Wave 1 is deliberately warning-only (no status change). Wave 1 ships on Day 1 with zero risk tolerance — the proper configurable gate comes in Wave 2 with shadow/soft/full modes.

### 5. Auto-Recovery Is Opt-In
Wave 3's `--recover` flag is never invoked automatically. Recovery requires explicit user intent via CLI because auto-generated checkpoints are lower fidelity than agent-written ones. Recovered files are clearly marked with `## Note: Auto-Recovered` headers and `recovered: true` frontmatter.

### 6. `PASS_MISSING_CHECKPOINT` Is Non-Failure
The new `PhaseStatus` enum value has `is_failure = False` because the phase's tasks did pass — only checkpoints are missing. This prevents downstream pipeline logic from treating it as a hard failure while still distinguishing it from a clean PASS.

---

## G. Risk Mitigation Matrix

| Risk | Wave | Likelihood | Impact | Mitigation |
|------|------|------------|--------|------------|
| Agent ignores prompt instructions despite Wave 1 (context pressure, long phases) | 1 | Low–Medium | Medium | Waves 2+3 detect and remediate; Wave 1 reduces incidence from ~14% to ~5% |
| Path resolution bugs cause false positives in Wave 2 gate | 2 | Low | High (if in `full` mode) | Shadow mode default means zero behavioral impact; fix before promoting to soft/full |
| Numbering cascade errors in Wave 4 tasklist normalization | 4 | Low–Medium | Medium | Self-check validation rules (T04.02) catch errors before tasklist write; Waves 1–3 remain as fallback |
| Auto-recovery produces low-quality checkpoints | 3 | Medium | Low | `Auto-Recovered` header + `recovered: true` flag distinguishes from agent-written CPs; recovery is opt-in |
| Existing OntRAG tasklists incompatible with Wave 4 | 4 | Certain | Low | Waves 1–3 already provide full coverage for old-format tasklists; Wave 4 applies only to new generation |
| Downstream consumers don't handle `PASS_MISSING_CHECKPOINT` enum | 2 | Low | Low | `is_failure = False` means existing failure-path logic is unaffected; only explicit enum matches need updating |
| Manifest generation slows sprint start/end | 3 | Very Low | Low | Manifest build is lightweight file scanning; no network or subprocess calls |

---

## H. Open Questions / Gaps

### Ambiguities

1. **Wave 2 → Wave 1 replacement timing**: T02.04 states it "replaces `_warn_missing_checkpoints()` (from T01.02) with `_verify_checkpoints()`". The transition mechanism is unclear — is T01.02's function deleted when T02.04 ships, or does T02.04 extend it? If the two waves ship to different branches, the merge strategy needs definition.

2. **Config persistence**: `checkpoint_gate_mode` is added to `SprintConfig` in `models.py`, but none of the documents specify how users set it. Is it a CLI flag (`--checkpoint-gate=full`), an environment variable, a config file entry, or all three? The rollout timeline assumes operators can change it, but the mechanism is unspecified.

3. **Mid-phase checkpoint handling in Wave 2 gate**: The gate verifies checkpoint files exist after a phase completes. Phase 3 has a mid-phase checkpoint (CP-P03-T01-T05) that should theoretically be verified partway through the phase. The documents don't address whether the gate checks only end-of-phase CPs or also mid-phase CPs. If end-only, mid-phase CPs remain unverified by Layer 2.

### Contradictions

4. **LOC estimates**: The proposal says "~580 across all 4 waves" (60 + 120 + 200 + 200), but the tasklist's Phase 3 alone has 5 tasks including two marked M (medium) effort. The 200 LOC estimate for Wave 3 may be conservative given the evidence scanning and template generation complexity in T03.03.

### Incomplete Items

5. **Test coverage**: The tasklist references unit and integration tests as verification methods for individual tasks but does not include dedicated test-writing tasks. No `tests/` file targets appear in the file inventory. Test strategy is implied but not formalized.

6. **Backward compatibility for `PASS_MISSING_CHECKPOINT`**: T02.02 mentions "Grep for exhaustive PhaseStatus matches and verify new variant is handled" but does not enumerate which files contain such matches. A gap exists if any match/switch statement is missed.

7. **Evidence file format for auto-recovery (T03.03)**: The task references "deliverable evidence files (D-*/evidence.md)" but the expected format/location of these files is not specified. If evidence files vary in structure across sprints, the recovery template quality will be inconsistent.

8. **Tasklist index format (T03.02)**: `build_manifest()` takes a `tasklist_index: Path` parameter, but the format of this index file is not documented. It's unclear if this is an existing artifact or one that needs to be created.

9. **Wave 4 migration path**: The proposal notes Wave 4 is a breaking change for existing tasklists but does not specify a migration utility or documentation for converting old-format `### Checkpoint:` sections to `### T<PP>.<NN> -- Checkpoint:` format. Projects with in-flight sprints using old-format tasklists would need guidance.

10. **Interaction with `_check_checkpoint_pass()` crash recovery**: The existing crash-recovery function at `executor.py:1592-1603` is mentioned in the root cause analysis but never appears in any task's modification scope. It should either be deprecated in favor of the new gate or explicitly documented as retained for its original crash-recovery purpose.
