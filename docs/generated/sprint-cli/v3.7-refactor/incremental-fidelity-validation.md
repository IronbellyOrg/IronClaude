# Incremental Fidelity Validation: Path A Partition

## Metadata

| Field | Value |
|---|---|
| **Date** | 2026-04-04 |
| **Input** | path-a-partition-document.md |
| **Baseline** | r1-fidelity-index.md (mean 0.77), r2-fidelity-index.md (mean 0.83) |
| **Scope** | Validate that all 8 R1-assigned + 1 R2-assigned + 2 deferred new tasks, plus 15 modified tasks, have homes in the release specs |

---

## R1 Incremental Fidelity

### New Tasks Assigned to R1

| Task ID | R1 Spec Section | Status | Gap Description |
|---------|----------------|--------|-----------------|
| PA-01 | Phase 0 (new section needed) | **NEEDS ADDITION** | R1 spec currently starts at Phase 1 (Naming + W1). A new "Phase 0: Path A Foundation" section must be added before Phase 1, containing PA-01/02/03/04/05/06. R1 rollout strategy (Day 1: naming + W1) must prepend "Day 0: Path A foundation (parallel with naming)." |
| PA-02 | Phase 0 (new section) | **NEEDS ADDITION** | Same as PA-01. Listed as dependent on PA-01 within Phase 0. |
| PA-03 | Phase 0 (new section) | **NEEDS ADDITION** | Same. Also needs note about `process.py` shared builder refactor (file already in R1 file inventory). |
| PA-04 | Phase 0 (new section) | **NEEDS ADDITION** | Bug fix in `executor.py:1091`. R1 file inventory already includes executor.py (checkpoint modifications). Add "Path A bug fix (line 1091)" to executor.py entry's change description. |
| PA-05 | Phase 0 (new section) | **NEEDS ADDITION** | Bug fix in `executor.py:1017-1025`. Same file inventory note as PA-04. Add "TaskResult.output_path wiring (line 1017)" to executor.py entry. |
| PA-06 | Phase 1 (alongside existing tasks) | **NEEDS ADDITION** | `models.py:329` default change. R1 file inventory already includes models.py. Add entry: "gate_rollout_mode default: off -> shadow". Depends on PA-04+PA-05 so it slots into Phase 1. |
| NEW-DM-04 | Phase 1 (new entry) | **NEEDS ADDITION** | New function in `monitor.py`. R1 file inventory does NOT currently include monitor.py — must be added. Add: "monitor.py | MODIFY | Add extract_token_usage() function | Phase 1". |
| NEW-DM-05 | Phase 1 (new entry) | **NEEDS ADDITION** | New fields on `TaskResult` in `models.py`. R1 file inventory has models.py. Add: "Add tokens_in/tokens_out to TaskResult". |

### Modified Tasks With R1 Spec Notes

| Task ID | R1 Spec Section | Status | Gap Description |
|---------|----------------|--------|-----------------|
| T02.04 | Checkpoint W2 (existing) | **NEEDS MODIFICATION** | Add note: "T02.04 is Path A's PRIMARY defense. Consider changing default checkpoint_gate_mode from 'shadow' to 'soft'." Currently T02.04 description doesn't mention Path A primacy. |
| T02.05 | Checkpoint W2 (existing) | **NEEDS MODIFICATION** | Add note: "Extend tests to explicitly cover Path A's per-task TaskResult accumulation flow." |
| T04.01 | Checkpoint W4 section | **NOT APPLICABLE** | T04.01 is Wave 4, which is deferred. The modification note about "checkpoint becomes regular task in Path A" should be added to R1's "Excluded (deferred)" section as future context. |
| Sec 5 (R1 portion) | Cross-Domain Dependencies | **NEEDS ADDITION** | Add sections 5.6 (Path A <-> Checkpoint) and 5.7 (Path A <-> TurnLedger). The baseline fidelity index flagged Sec 5.5 as PARTIAL (0.50) — this addition partially addresses that gap. |
| Sec 6.2 | Implementation Order | **NEEDS MODIFICATION** | Insert "Path A Prompt Enrichment" and "TurnLedger Bug Fixes" into the 7-step order, making it 9 steps. Currently R1 rollout strategy at lines 210-221 doesn't mention Path A tasks. |
| Sec 6.4 (R1 portion) | Post-Phase Hook Ordering | **NEEDS MODIFICATION** | Add that `_verify_checkpoints()` must also be inserted in Path A block (executor.py:1222-1233), not just Path B. Baseline flagged this as PARTIAL (0.30) — this directly addresses the gap. |
| Sec 14 (R1 portion) | Open Questions | **NEEDS MODIFICATION** | Resolve CE-Q3, CE-Q4, CE-Q6. Reframe CE-Q2. Add cross-reference to Path A analysis documents. |

### R1 Verification Checklist

- [x] **a) Every PA task assigned to R1 has a home**: PA-01/02/03/04/05/06 need a new Phase 0 section. DM-04/DM-05 need Phase 1 entries. All 8 tasks have identified homes (NEEDS ADDITION, not MISSING PREREQUISITE).
- [x] **b) No R1 task creates undocumented R2 dependency**: PA-04 (turns), PA-05 (output_path), DM-05 (tokens) create data contracts R2 consumes. These are now documented in the partition document's "R1 Provides -> R2 Consumes" table. R1 spec must add a "Cross-Release Contracts" section listing these.
- [x] **c) R1's existing tasks are not broken**: PA-04 modifies executor.py:1091 (different line range from checkpoint W1-W3). PA-05 modifies executor.py:1017-1025 (different line range). DM-04 modifies monitor.py (not currently in R1). PA-06 modifies models.py:329 (different field from checkpoint_gate_mode). No conflicts with existing R1 tasks.
- [x] **d) R1 file inventory needs updating**:
  - ADD: `monitor.py | MODIFY | extract_token_usage() | Phase 1` (for NEW-DM-04)
  - UPDATE: `executor.py` entry to note Path A bug fixes (lines 1017, 1064-1068, 1091)
  - UPDATE: `models.py` entry to note gate_rollout_mode default change + tokens_in/out fields
- [x] **e) R1 rollout strategy accommodates Wave 0**: Must prepend Phase 0 to rollout: "Day 0 (parallel with naming): PA-04, PA-05, PA-01 (all independent, can parallelize)." Day 1 becomes "naming + W1 + PA-02/PA-03/PA-06/DM-04/DM-05."

---

## R2 Incremental Fidelity

### New Tasks Assigned to R2

| Task ID | R2 Spec Section | Status | Gap Description |
|---------|----------------|--------|-----------------|
| NEW-DM-06 | Wave 1 (Data Model + Monitor) | **NEEDS ADDITION** | R2 Wave 1 currently lists 6 items (MonitorState fields, PhaseResult fields, SprintResult properties, SprintConfig.total_tasks, SprintTUI.latest_summary_notification, monitor extraction). Add item 7: "Path A aggregation: TaskResult list -> PhaseResult.turns/tokens_in/tokens_out". This is the bridge logic. |

### Modified Tasks With R2 Spec Notes

| Task ID | R2 Spec Section | Status | Gap Description |
|---------|----------------|--------|-----------------|
| F1 | Wave 2 feature list | **NEEDS MODIFICATION** | Add: "Path A adaptation: use synthetic activity entries (task_id, status, duration) per completed task. OutputMonitor not started for Path A." |
| F2 | Wave 2 feature list | **NEEDS MODIFICATION** | Add: "Path A adaptation: wire turns/output columns from accumulated TaskResult data, not MonitorState." |
| F3 | Wave 2 feature list | **NEEDS MODIFICATION** | Add: "Path A adaptation: set exact task counts (total_tasks=len(tasks), completed=i+1). 2-line change." |
| F4 | Wave 2 feature list | **NEEDS MODIFICATION** | Add: "Path A adaptation: use task-level errors (task_id, 'subprocess', exit_code) from TaskResult, not NDJSON." |
| F6 | Wave 2 feature list | **NEEDS MODIFICATION** | Add: "Path A adaptation: aggregate PhaseResult.turns/tokens/output_bytes from TaskResult list post-phase." |
| F8 | Wave 3 feature list | **NEEDS MODIFICATION** | Add: "Path A adaptation: PhaseSummarizer must accept list[TaskResult] as alternative to NDJSON file path." |
| 7.1 | Wave 1 MonitorState | **NEEDS MODIFICATION** | Add: "Path A population: fields populated by PhaseAccumulator.to_monitor_state() adapter (synthetic, not live monitoring). Fields last_tool_used, files_changed, growth_rate_bps remain at defaults under Path A v3.7. Document as Path B only." |
| 7.2 | Wave 1 PhaseResult | **NEEDS MODIFICATION** | Add: "Path A data flow: TaskResult -> PhaseResult aggregation (via NEW-DM-06), not MonitorState -> PhaseResult." |
| Sec 5 (R2 portion) | Dependencies | **NEEDS ADDITION** | Add Path A <-> TUI data flow documentation. Baseline flagged Sec 5.1 as PARTIAL (0.70). |
| Sec 6.4 (R2 portion) | Hook ordering | **COVERED** | R2 already documents hook ordering at item 21: _verify_checkpoints() -> summary_worker.submit(). No additional change needed. |
| Sec 14 (R2 portion) | Open Questions | **NEEDS MODIFICATION** | Resolve TUI-Q8, reframe TUI-Q1 and TUI-Q2 per Path A analysis findings. |

### R2 Verification Checklist

- [x] **a) Every R2 prerequisite from R1 is documented**: R2 Dependencies section (lines 109-117) has hard deps on PhaseStatus.PASS_MISSING_CHECKPOINT and executor hook site. **Must add**: PA-04 (turns), PA-05 (output_path), NEW-DM-05 (tokens) as new hard prerequisites. PA-01/PA-06 as soft prerequisites.
- [x] **b) Modified features have dual-path acceptance criteria**: Currently R2 feature specs assume Path B only. Each modified feature (F1/F2/F3/F4/F6/F8) needs acceptance criteria for BOTH paths. Example: "F2 acceptance: phase table shows correct turns for BOTH per-task Path A execution AND single-process Path B execution."
- [x] **c) MonitorState field population accounts for Path A synthetic mode**: R2 Wave 1 item 1 lists 8 new MonitorState fields but doesn't mention synthetic population. **Must add**: "Path A: fields populated by PhaseAccumulator.to_monitor_state(). Fields without synthetic source (last_tool_used, files_changed, growth_rate_bps) show defaults. stall_status adapter sets last_event_time to suppress false STALLED alarms."
- [x] **d) TurnLedger bug fixes listed as R2 prerequisites**: Not currently in R2 Dependencies table. **Must add** PA-04 and PA-05 as hard prerequisites with note: "Required for F2/F6 turns display and F8 output path access."

---

## Fidelity Summary

| Metric | R1 | R2 |
|--------|----|----|
| Tasks added | 8 (PA-01/02/03/04/05/06, DM-04/05) | 1 (DM-06) |
| Tasks modified | 4 (T02.04, T02.05, Sec 5, Sec 6.4) | 8 (F1/F2/F3/F4/F6/F8, 7.1, 7.2) |
| Spec modifications to both | 3 (Sec 5, Sec 6.4, Sec 14) | — |
| New prerequisites identified | 0 (R1 has no external prereqs) | 6 (3 hard: PA-04, PA-05, DM-04+DM-05; 3 soft: PA-01/02/03, PA-06, append-mode) |
| Boundary tensions found | 0 hard | 0 hard |
| Documentation-only tensions | 2 (Sec 5, Sec 6.4) | — |
| Spec sections needing update | 7 | 12 |
| New cross-release integration points | 6 (points 5-10 in partition doc) | — |

### Baseline Fidelity Improvements

The Path A additions directly address several gaps identified in the baseline fidelity indices:

| Baseline Gap | Fidelity Before | Addressed By | Expected After |
|---|---|---|---|
| R1: Sec 6.4 Post-Phase Hook Ordering | 0.30 | Sec 6.4 modification (hook in Path A block) | 0.70+ |
| R1: Sec 5.5 Shared File Conflict Analysis | 0.50 | Sec 5 addition (Path A as 4th domain) | 0.70+ |
| R1: Sec 6.1 Shared File Modifications | 0.40 | File inventory update (monitor.py, executor.py notes) | 0.60+ |
| R2: Sec 5.1 Checkpoint <-> TUI | 0.70 | Sec 5 addition (Path A <-> TUI data flow) | 0.85+ |
| R2: Sec 5.3 Naming <-> TUI | 0.50 | (Not directly addressed by this partition) | 0.50 |

### Tasks Deferred to v3.8 (Validation)

| Task | Reason for Deferral | Would Be Assigned To | Risk of Deferral |
|---|---|---|---|
| PA-07 (build_task_context) | 75% confidence, optional, behind config flag, depends on shadow-mode data | R1 | **Low** — default off, no consumer depends on it |
| PA-08 (deliverable existence check) | Observability only, ~40 LOC, low urgency | R1 | **Negligible** — logging-only, no enforcement |

Both deferred tasks are self-contained and can be added to any future release without architectural impact.

---

## Boundary Tension Resolutions

### Tension 1: Sec 5 (Cross-Domain Dependencies) — Documentation in Both Specs

**Resolution**: SPLIT THE DOCUMENTATION.
- R1 spec adds: Section 5.6 "Path A <-> Checkpoint Enforcement" (how PA-01/02/03 enriched prompts interact with checkpoint instructions) and Section 5.7 "Path A <-> TurnLedger" (how PA-04/05/06 fix the gate evaluation chain).
- R2 spec adds: Updated Section 5.1 "Path A <-> TUI Data Flow" (how TaskResult fields from R1 feed into MonitorState adapter and TUI rendering).
- No code split needed. Documentation-only. **No escalation required.**

### Tension 2: Sec 6.4 (Post-Phase Hook Ordering) — Insertion in Both Specs

**Resolution**: R1 ESTABLISHES, R2 EXTENDS.
- R1 spec defines the hook insertion site in Path A block (executor.py:1222-1233) and inserts `_verify_checkpoints()` as the first hook.
- R2 spec appends `summary_worker.submit()` after `_verify_checkpoints()` at the same site.
- The ordering contract (checkpoint before summary before manifest) is documented in BOTH specs.
- This is identical to existing integration point #1 from boundary-rationale.md. **No escalation required.**

---

## Recommendations

### Immediate Actions (before implementation begins)

1. **Add Phase 0 to R1 spec**: Create a new section "Phase 0: Path A Foundation" with PA-01/02/03/04/05/06, DM-04/DM-05. All can parallelize with naming.

2. **Update R1 file inventory**: Add monitor.py. Update executor.py and models.py change descriptions.

3. **Update R1 rollout strategy**: Prepend Day 0 for Path A foundation tasks.

4. **Add R2 prerequisites**: PA-04, PA-05, NEW-DM-05 as hard prerequisites. PA-01, PA-06 as soft.

5. **Add Path A adaptation notes to R2 features**: F1/F2/F3/F4/F6/F8 each need a "Path A:" note in their spec.

6. **Add MonitorState synthetic population note to R2 Wave 1**: Document PhaseAccumulator adapter and which fields remain at defaults.

7. **Add cross-release contracts section to R1**: Document what R2 depends on from R1's Path A tasks.

### No Escalation Required

All boundary tensions resolved by documentation splitting. No tasks require reassignment or adversarial micro-debate. The partition is clean.

---

*End of incremental fidelity validation.*
