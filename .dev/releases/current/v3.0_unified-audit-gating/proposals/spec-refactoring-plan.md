# Spec Refactoring Plan — unified-audit-gating-v1.2.1-release-spec.md

**Plan date**: 2026-03-17
**Target file**: `unified-audit-gating-v1.2.1-release-spec.md`
**Status**: PLAN ONLY — do not edit spec until this plan is approved

**Input sources synthesized**:
- Branch decision (B): `proposals/branch-decision/adversarial/branch-decision-merged.md` — 7 conditions C1–C7
- Adversarial delta review (A): `adversarial-delta-review/adversarial-delta-review-merged.md` — codebase-verified findings
- Delta analysis (D): `delta-analysis-post-v2.26.md` — §4.4 and §10.2 replacement language

---

## 0. Summary of Changes

| # | Section | Change Type | Trigger | Priority |
|---|---------|-------------|---------|----------|
| R1 | §1.1 Scope | Scope amendment | Branch decision C1 | BLOCKING (Phase 0) |
| R2 | §2.1 Locked decisions | Add new locked decision | Branch decision C7 | BLOCKING (Phase 0) |
| R3 | §2.3 Contradictions | Add 2 new rows | Delta review A + Branch decision C4 | Phase 1 |
| R4 | §3.1 Canonical terms | Add 6 new terms | Adversarial review A (6 undefined terms) | Phase 1 |
| R5 | §4.1 Legal transitions | Annotate task-scope deferred | Branch decision C1 | BLOCKING (Phase 0) |
| R6 | §4.4 Timeout/retry semantics | Major rewrite | Delta analysis D + adversarial review A | Phase 1 |
| R7 | §5.2 Pass/fail rules | Clarify item 4 | Adversarial review A (NR-5/NR-6) | Phase 1 |
| R8 | §6.1 GateResult | Add naming and field notes | Adversarial review A (MF-2) | Phase 1 |
| R9 | §7.2 Promotion criteria | Annotate M1/M8 recalibration | Branch decision C4 | Phase 1 |
| R10 | §8 KPI framework | Add recalibration notes | Branch decision C4 | Phase 1 |
| R11 | §9.2 Owner responsibilities | Add tasklist owner | Delta analysis D (§9.2) | Phase 1 |
| R12 | §9.3 Decision deadlines | Note branch decision as locked | Branch decision C7 | BLOCKING (Phase 0) |
| R13 | §10.1 Phase plan | Align phases with consensus | Delta analysis D + adversarial review | Phase 1 |
| R14 | §10.2 File-level change map | Major rewrite | Delta analysis D + branch decision | Phase 1 |
| R15 | §10.3 Acceptance criteria | Add deviation-analysis criterion | Adversarial review A | Phase 1 |
| R16 | §11 Checklist closure | Update D1.1 row | Delta analysis D | Phase 1 |
| R17 | §12.3 Blocker list | Add 2 new blockers | Branch decision + adversarial review | BLOCKING (Phase 0) |
| R18 | §12.4 Required decisions | Add 1 new decision | Branch decision C3 | BLOCKING (Phase 0) |
| R19 | Top 5 Immediate Actions | Add 1 item | Delta analysis D | Phase 1 |
| R20 | Top 5 Deferred | Add execute_phase_tasks item | Branch decision C6 | Any time |
| R21 | Open Decisions table | Add branch decision + C3 row | Branch decision C7 + C3 | BLOCKING (Phase 0) |

**BLOCKING changes (must complete before Phase 1 start)**: R1, R2, R5, R12, R17, R18, R21
**Phase 1 changes**: R3, R4, R6, R7, R8, R9, R10, R11, R13, R14, R15, R16, R19
**Any time**: R20

---

## 1. Detailed Change Specifications

---

### R1 — §1.1 Scope: Amendment for branch (b)

**Current text**:
> Implement a unified audit-gating capability that blocks completion/release transitions unless the corresponding gate passes at three scopes:
> 1. Task gate
> 2. Milestone gate
> 3. Release gate

**Required change**: Add a scope amendment note after the list.

**New text to append after the numbered list**:
> **v1.2.1 Scope Amendment (Branch (b), locked 2026-03-17)**: v1.2.1 implements milestone-scope (phase) and release-scope (sprint) gates only. The "Task gate" listed in item 1 above is satisfied via phase-scope gating: tasks are evaluated within phase-scope gate runs using per-task output artifacts. True task-scope gating (independent per-task state machine) is deferred to v1.3, contingent on independent validation and mainline promotion of the task-scope execution model. See §4.1 and §2.1 locked decision #6.

**Source**: Branch decision C1, C7.

---

### R2 — §2.1 Locked decisions: Add branch (b) as locked decision #6

**Current list ends at item 5**. Add:

> 6. v1.2.1 implements audit gates at phase-scope (milestone) and sprint-scope (release) only. Task-scope audit gates are deferred to v1.3. Phase-scope gates evaluate per-task output artifacts within each phase. (Branch (b) decision, 2026-03-17; see §4.1 deferral annotation.)

**Source**: Branch decision C7.

---

### R3 — §2.3 Contradictions: Add 2 new rows

**Append to the contradictions table**:

| Contradiction | Evidence | Winner in v1.2.1 | Rationale |
|---|---|---|---|
| Spec §4.1 has 12 task-scope transitions vs. sprint executor never runs at task granularity | Adversarial delta review MF-1 (CRITICAL, unanimous); `sprint/executor.py:350` zero call sites in mainline | Phase-scope gating for v1.2.1; task-scope deferred to v1.3 | Activating orphaned dead code under delivery pressure is an unacceptable compound risk. Branch (b) locked. |
| KPI M1 defined as "Task scope, ≤8s" vs no task-scope evaluations under branch (b) | Branch decision C4; `metrics-and-gates.md` KPI table | Redefine M1 as phase-scope runtime for v1.2.1 with recalibrated threshold during shadow mode | The 8s threshold was calibrated for per-task evaluations; phase-scope evaluations have different timing profiles |

**Source**: Branch decision C4; adversarial review MF-1.

---

### R4 — §3.1 Canonical terms: Add 6 new terms

**Append after existing terms**:

> **New terms added for v1.2.1 implementation (to be defined before Phase 1 GO)**:
> - **AuditLease**: A timed lock held by the audit gate evaluator while `audit_*_running`. Required fields: `lease_id` (unique identifier), `owner` (evaluator process/agent identity), `acquired_at` (ISO-8601 UTC), `expires_at` (ISO-8601 UTC), `renewed_at` (ISO-8601 UTC).
> - **audit_lease_timeout**: Per-scope configurable duration after which a missing heartbeat triggers `audit_*_failed(timeout)`. Must be independent of and no greater than the outer subprocess wall-clock timeout. Default values subject to Reliability Owner approval before Phase 2 GO.
> - **max_turns**: The sprint/roadmap runner configuration value for subprocess turn limit. Determines outer wall-clock timeout ceiling: `max_turns * 120 + 300 s` for standard subprocesses. Default: 100.
> - **Critical Path Override**: A tasklist task field (boolean). When `true`, the task is on the critical path and `audit_gate_required` defaults to `true` regardless of Tier or Risk.
> - **audit_gate_required**: A boolean field emitted per task in tasklist metadata. Derivation rule: `true` when `Tier == STRICT OR Risk == High OR Critical Path Override == true`. At phase scope, aggregated as `phase_requires_audit = any(task.audit_gate_required for task in phase.tasks)`.
> - **audit_attempts**: Per-entity retry counter, persisted in durable state, incremented on each retry attempt. Bounded by `max_attempts` per scope.

**Source**: Adversarial review A, Section 6.1 (6 undefined terms); Branch decision C2.

---

### R5 — §4.1 Legal transitions: Annotate task-scope as deferred

**Current text** has three subsections: Task scope, Milestone scope, Release scope.

**Required change**: Add a deferral block immediately before the "Task scope" subsection, and add `[v1.3 — deferred]` markers to each task-scope transition line.

**New block before "Task scope"**:
> **Branch (b) deferral**: Task-scope audit gate transitions below are retained for v1.3 reference. They are NOT implemented in v1.2.1. The v1.2.1 implementation covers Milestone scope and Release scope. Marker: `[v1.3 — deferred]`.

**Annotated task-scope transitions** (add marker suffix to each line):
```
- `in_progress -> ready_for_audit_task`  [v1.3 — deferred]
- `ready_for_audit_task -> audit_task_running`  [v1.3 — deferred]
- `audit_task_running -> audit_task_passed | audit_task_failed`  [v1.3 — deferred]
- `audit_task_passed -> completed`  [v1.3 — deferred]
- `audit_task_failed -> ready_for_audit_task` (retry path)  [v1.3 — deferred]
- `audit_task_failed -> completed` only with approved task override  [v1.3 — deferred]
```

**Source**: Branch decision C1.

---

### R6 — §4.4 Timeout/retry/recovery semantics: Major rewrite

**Current text** (5 items, terse, all TBD values) must be replaced with a version that:
1. Removes all source-file line citations (per adversarial review consensus)
2. Defines concrete behavioral contracts (not implementation pointers)
3. Reflects branch (b) scope (phase + release only)
4. Moves the reimbursement_rate governance item to §12.3 (R17)

**Replace the entire §4.4 body with**:

> 1. `audit_*_running` uses a lease model with heartbeat renewal. The lease must hold: `lease_id` (unique identifier), `owner` (evaluator identity), `acquired_at`, `expires_at`, and `renewed_at` (all ISO-8601 UTC). The audit gate evaluator must emit a heartbeat renewal event at an interval no greater than `audit_lease_timeout / 3`. The lease mechanism builds on the subprocess stall-detection pattern already present in the sprint executor's output monitoring infrastructure.
>
> 2. Missing heartbeat renewal past `audit_lease_timeout` causes `audit_*_failed(timeout)`. `audit_lease_timeout` is a per-scope configurable value; default values must be approved by the Reliability Owner (§9.2) before Phase 2 GO. The `audit_lease_timeout` must be independent of and no greater than the outer subprocess wall-clock timeout for the same scope.
>
> 3. Retry is bounded by a per-scope attempt budget. The attempt count for each audited entity (`audit_attempts`) must be persisted in durable state and incremented on each retry. `max_attempts` is configured per scope (milestone and release for v1.2.1). Default values for `max_attempts` are **provisional during shadow mode** and become normative only after calibration per §8.2. Provisional defaults: milestone=2, release=1. These values must be reviewed and approved by the Reliability Owner before Phase 2 GO.
>
> 4. Retry exhaustion remains failed and blocks completion/release.
>
> 5. Requeue allowed only while budget remains.
>
> 6. The outer wall-clock ceiling for any sprint phase execution is derived from the configured `max_turns` value (see §3.1 canonical terms). Audit gate evaluation must complete within this ceiling. The Reliability Owner must specify the audit gate sub-process time budget as a fraction of the outer ceiling before Phase 2 GO. This value must be documented as a locked decision per §9.3.

**Notes**:
- `task=3` default removed because task-scope is deferred (branch b). Only milestone=2 and release=1 remain.
- All source-file line references removed per adversarial review consensus.
- Item 7 (reimbursement_rate) moved to §12.3 blocker list (see R17).

**Source**: Adversarial review A Section 7; Delta analysis D §4.4 replacement; Branch decision C5; adversarial review consensus on line citations.

---

### R7 — §5.2 Pass/fail rules: Clarify "latest" in item 4

**Current item 4**:
> Completion/release transitions require latest gate `passed` except approved task/milestone override path.

**Replace with**:
> Completion/release transitions require the *current* gate result to reference the artifact version under evaluation. A gate result is considered stale and non-satisfying if the artifacts it audited have changed since the gate ran. Stale gate results must trigger re-evaluation. Approved task/milestone override paths are exempt from re-evaluation but must record the staleness in the `OverrideRecord`.

**Source**: Adversarial review A (NR-5/NR-6 consolidated finding; §5.2 "latest" ambiguity).

---

### R8 — §6.1 GateResult: Add implementation notes

**After the existing required fields list, append**:

> **Implementation notes for v1.2.1**:
> - The sprint codebase contains a pre-existing `GateResult` class in `cli/audit/evidence_gate.py` (2 fields: `passed`, `reason`). The v1.2.1 `GateResult` dataclass implementing this spec must use the disambiguated name `AuditGateResult` to avoid namespace collision. The existing 2-field class must not be renamed; both coexist.
> - `AuditGateResult` is a new dataclass to be added to `src/superclaude/cli/sprint/models.py`, separate from `GateDisplayState` (which remains for TUI rendering only).
> - The `artifacts` block must include artifact version hashes (SHA-256 or equivalent) to support the freshness validation required by §5.2 item 4.

**Source**: Adversarial review A (MF-2 namespace collision; §6.1 note on GateDisplayState separation).

---

### R9 — §7.2 Promotion criteria: Annotate M1/M8 recalibration

**After the promotion criteria, append**:

> **v1.2.1 branch (b) KPI adjustments**: M1 (Tier-1 runtime, originally defined as task-scope ≤8s) and M8 (false-block rate, Tier-1) are not applicable at task scope under v1.2.1. Before shadow mode launches:
> - **M1**: Redefine as phase-scope runtime for v1.2.1 with recalibrated threshold. The 8s threshold was calibrated for per-task evaluations; phase-scope will require a longer threshold. Calibrate from shadow mode data before soft-phase promotion.
> - **M8**: Apply at Tier-2 (phase scope) only. Consider tightening the false-block threshold during calibration to account for larger blast radius of phase-scope gates vs task-scope gates.
>
> These recalibrations are Phase 1 deliverables, required before shadow mode produces promotion-decision data.

**Source**: Branch decision C4.

---

### R10 — §8 KPI framework: Note on new audit events

**After §8.2 Calibration method, add**:

> **§8.5 Audit gate KPI instrumentation**
> The audit gate state machine introduces new event types that feed into existing KPIs:
> - **M1 (runtime)**: Audit lease acquisition and evaluation duration are new M1 inputs.
> - **M7 (stale-running incidents)**: Audit lease timeout events are M7 incidents.
> - **M9 (override governance)**: OverrideRecord creation and approval events are M9 inputs.
> These instrumentation points must be wired in Phase 2 before shadow mode data is collected.

**Source**: Adversarial review A Section 9 (§7.2 and §8 were missing from original update table).

---

### R11 — §9.2 Owner responsibilities: Add tasklist owner

**Append to the owner list**:
> - **Tasklist owner**: `audit_gate_required` derivation rules and `Critical Path Override` field definition. Owns per-task metadata schema compatibility between tasklist generator and sprint runner.

**Source**: Delta analysis D (§9.2 addition); adversarial review A (undefined term `Critical Path Override`).

---

### R12 — §9.3 Decision deadlines: Note branch decision as locked

**After the existing §9.3 text, append**:

> **Locked decision on record (2026-03-17)**: Branch (b) — v1.2.1 implements phase-scope and release-scope audit gates only. Task-scope deferred to v1.3. This decision is locked per §9.3 with the following record:
> - **Owner**: [to be assigned]
> - **UTC deadline**: [to be assigned]
> - **Effective rollout phase**: All phases of v1.2.1 (shadow/soft/full)
> - **Evidence basis**: `execute_phase_tasks()` confirmed dead code (MF-1, unanimous adversarial review); compound delivery risk of activating orphaned code under delivery pressure.
> - **Reversal condition**: If Phase 1 investigation shows per-task artifacts are not individually addressable within phase subprocess output (Branch decision R1), escalate to program manager.

**Source**: Branch decision C7.

---

### R13 — §10.1 Phase plan: Align with consensus ordering

**Replace current phase plan**:

> - **Phase 0**: Decision lock + code prerequisites
>   - Locked decisions closed: branch (b) record, owner/deadline assignments
>   - Code: retire `_apply_resume_after_spec_patch()` (roadmap executor)
>   - Code: wire `deviation-analysis` step into roadmap `_build_steps()` (includes updating `_get_all_step_ids()` and writing `build_deviation_analysis_prompt()`)
>   - Go/no-go gate: all Phase 0 conditions met, branch decision locked per §9.3
>
> - **Phase 1**: Deterministic contracts + evaluator
>   - Data models: `AuditWorkflowState` enum (milestone + release scopes only, v1.2.1), `AuditGateResult` dataclass (§6.1), `AuditLease` dataclass, profile enum
>   - Survey `cli/audit/` subsystem for reusable patterns and naming conflicts before finalizing model design
>   - Transition validator: legal/illegal table per §4.1 (milestone + release scopes)
>   - Deterministic evaluator in `sc-audit-gate-protocol/SKILL.md`
>   - Tasklist: `audit_gate_required` derivation + `schema_version` field + phase-level aggregation rule
>   - KPI calibration: redefine M1 and M8 for phase-scope (C4, required before shadow mode)
>   - Go/no-go gate: deterministic replay stability; fail-safe unknown handling; per-task artifacts individually addressable in phase output (C3 validation checkpoint)
>
> - **Phase 2**: Runtime controls
>   - Wire `SprintGatePolicy` into `execute_sprint()` at post-subprocess integration point (phase scope)
>   - Extend `OutputMonitor` for audit lease heartbeat events
>   - Wire `TrailingGateRunner` for phase-scope evaluation
>   - Wire `ShadowGateMetrics` for shadow mode data collection
>   - Expose `--grace-period` CLI flag
>   - Go/no-go gate: timeout/retry paths terminate deterministically (no deadlocks)
>
> - **Phase 3**: Sprint CLI integration + operator surface
>   - TUI: display `AuditWorkflowState` in phase table; release guard; operator guidance panel
>   - `sc-audit-gate/SKILL.md`: command surface, profile selection, override governance flow
>   - `_save_state()`: add `audit` block for gate result persistence
>   - Go/no-go gate: transition blocking/override rules enforced per scope (milestone + release)
>
> - **Phase 4**: Rollout execution + KPI gates
>   - Shadow → Soft → Full per §7.1 promotion criteria
>   - Rollback drills per §7.3
>   - KPI normalization from shadow data (§8.2)
>   - Go/no-go gate: phase gates pass by KPI criteria and rollback drill success

**Source**: Delta analysis D §10.2 replacement; branch decision P2b scope; adversarial review MF-9; adversarial review on phase ordering.

---

### R14 — §10.2 File-level change map: Major rewrite

**Replace current text** with a version that:
1. Uses behavioral descriptions (no source-file line number citations)
2. Reflects branch (b) scope (phase + release only)
3. Includes newly discovered integration targets from adversarial review

**Replace with**:

> #### Phase 0 prerequisites
> - `roadmap/executor.py` — remove `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()` (spec-patch auto-resume retirement)
> - `roadmap/executor.py` — add `deviation-analysis` step to `_build_steps()` after `spec-fidelity`; update `_get_all_step_ids()` to include `deviation-analysis`; write `build_deviation_analysis_prompt()` function
>
> #### Phase 1: Deterministic contracts
> - `src/superclaude/cli/sprint/models.py` — add `AuditWorkflowState` enum (milestone + release scopes only); add `AuditGateResult` dataclass (§6.1, disambiguated from existing `cli/audit/` `GateResult`); add `AuditLease` dataclass; add profile enum (`strict | standard | legacy_migration`)
> - `src/superclaude/skills/sc-audit-gate-protocol/SKILL.md` — deterministic evaluator; legal/illegal transition table for milestone + release scopes; recovery flow
> - `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — add `audit_gate_required: bool` per task (derivation: `Tier==STRICT or Risk==High or Critical Path Override==true`); add `schema_version` field; add phase-level aggregation rule
> - `src/superclaude/cli/tasklist/` — parse and emit `audit_gate_required` in generated phase files
>
> #### Phase 2: Runtime controls
> - `src/superclaude/cli/sprint/executor.py` — wire `SprintGatePolicy` into `execute_sprint()` at post-subprocess, pre-classification boundary; phase scope only
> - `src/superclaude/cli/sprint/monitor.py` — extend `OutputMonitor` to support audit lease heartbeat events as a distinct event class
> - `src/superclaude/cli/pipeline/trailing_gate.py` — wire `TrailingGateRunner` for phase-scope evaluation; `GateScope.MILESTONE` and `GateScope.RELEASE` (already defined)
> - `src/superclaude/cli/sprint/models.py` — wire `ShadowGateMetrics` for audit gate shadow mode data collection
> - `src/superclaude/cli/sprint/commands.py` — expose `--grace-period` CLI flag
>
> #### Phase 3: Sprint CLI integration
> - `src/superclaude/cli/sprint/tui.py` — extend phase table to display `AuditWorkflowState` values; add release guard (block "Sprint Complete" unless `audit_release_passed`); add operator guidance panel for `audit_*_failed` display
> - `src/superclaude/skills/sc-audit-gate/SKILL.md` — command surface, profile selection, override governance flow
> - `src/superclaude/cli/roadmap/executor.py` — add `audit` block to `_save_state()` for gate result persistence
>
> #### Phase 4: Rollout
> - `tests/sprint/test_audit_gate_state_machine.py` — legal/illegal transitions + stuck-state recovery (milestone + release scopes)
> - `tests/sprint/test_audit_gate_profiles.py` — profile determinism + severity behavior
> - `tests/sprint/test_audit_gate_overrides.py` — scope-limited override governance
> - `tests/sprint/test_audit_gate_rollout.py` — shadow/soft/full + rollback behavior

**Source**: Delta analysis D §10.2 replacement; adversarial review A (MF-2 naming, MF-3 ShadowGateMetrics, MF-8 grace_period, MF-9 _get_all_step_ids); branch decision P2b scope.

---

### R15 — §10.3 Acceptance criteria: Add Phase 1 criterion

**Append to Phase 1 acceptance criterion**:
> ; roadmap pipeline produces validated `deviation-analysis.md` artifact (prerequisite for audit gate evaluator inputs)

**Updated Phase 1 criterion becomes**:
> Phase 1: deterministic replay stability for same input; fail-safe unknown handling; roadmap pipeline produces validated `deviation-analysis.md` artifact; per-task output artifacts are individually addressable within phase subprocess output (C3 validation checkpoint)

**Source**: Adversarial review A (§10.3 was UNCHANGED but NR-3 acceptance criterion is new); branch decision C3.

---

### R16 — §11 Checklist: Update D1.1 row

**Current row** for "9. Risk/reliability controls" reads "PASS (conditional)" with closure condition about retry/backoff/timeout.

**No change to row content** — D1.1 (retry/backoff values) is now partially resolved by concrete codebase values found in v2.26 (max_turns formula). Update the evidence source column:

| Checklist section | Current status | Closure condition | Evidence source |
|---|---|---|---|
| 9. Risk/reliability controls | PASS (conditional) | Finalize retry/backoff/timeout values and budgets; lock `audit_lease_timeout` defaults via Reliability Owner | `checklist-outcome-v1.2.md`; `delta-analysis-post-v2.26.md` §D1.1 (partially resolved); `adversarial-delta-review-merged.md` §7 |

**Source**: Delta analysis D §D1.1 partial resolution.

---

### R17 — §12.3 Blocker list: Add 2 new items

**Append to existing 4 blockers**:

> 5. Branch (b) locked decision record incomplete — owner and UTC deadline not yet assigned (required per §9.3 before Phase 1 start)
> 6. `reimbursement_rate = 0.8` in `TurnLedger` (sprint/models.py) is a dead model field with no usage. Decision required: (a) wire as turn-recovery credit for audit retry paths, or (b) remove. File as cleanup item and close before Phase 2 GO. (Governance directive — not a timeout/retry semantic; see §4.4 revision.)

**Source**: Branch decision C5, C7; adversarial review A §7 (reimbursement_rate placement correction).

---

### R18 — §12.4 Required decisions: Add C3 checkpoint

**Append**:

> 6. Confirm per-task output artifacts are individually addressable within phase subprocess output (C3 validation checkpoint). If not addressable, decide: (a) restructure phase output before Phase 2, or (b) accept coarser evaluation granularity and update Branch (b) amendment accordingly.

**Source**: Branch decision C3, R1.

---

### R19 — Top 5 Immediate Actions: Add deviation-analysis prompt

**Replace existing item 2** (or add as item 6 if list expands):

The existing immediate actions are governance/decision focused. Add an implementation-readiness action:

> 6. Validate that phase subprocess output contains identifiable per-task artifacts (C3 checkpoint) — this is a Phase 1 GO/NO-GO condition for branch (b).

**Source**: Branch decision C3.

---

### R20 — Top 5 Deferred Improvements: Add execute_phase_tasks item

**Append**:

> 6. Activate `execute_phase_tasks()` as a standalone work item for v1.3 task-scope audit gates. Independent acceptance criteria required: real ClaudeProcess integration tests, stall detection, watchdog coverage, TUI task-within-phase progress, per-task state persistence schema. Not tied to v1.2.1 audit gate delivery.

**Source**: Branch decision C6.

---

### R21 — Open Decisions table: Add branch decision and C3 rows

**Append rows**:

| Decision | Owner | Deadline (UTC) | Effective phase |
|---|---|---|---|
| Branch (b) locked decision record — assign owner + deadline | [TBD] | [TBD] | All (Phase 0 blocker) |
| Confirm per-task artifact addressability within phase output (C3) | [TBD] | [TBD] | Phase 1 go/no-go |
| `audit_lease_timeout` default values per scope | Reliability Owner | [TBD] | Phase 2 GO |
| `max_attempts` defaults (milestone=2, release=1) normative approval | Reliability Owner | [TBD] | Shadow→Soft gate |
| M1/M8 recalibrated thresholds for phase-scope | Policy Owner | [TBD] | Shadow launch |
| `reimbursement_rate` fate (wire or remove) | [TBD] | [TBD] | Phase 2 GO |

**Source**: Branch decision C3, C4, C5, C7; adversarial review R6 (audit_lease_timeout); R6 (max_attempts).

---

## 2. What This Plan Does NOT Change

The following spec sections are confirmed unchanged by all three input sources:

| Section | Reason |
|---|---|
| §0 Evidence model | Methodology unchanged |
| §1.2 Primary goals | Goals remain valid under branch (b) |
| §1.3 Out-of-scope | Constraints unchanged |
| §2.2 Non-goals | Release override still forbidden |
| §3.2 Strictness vs profile | Resolution unchanged |
| §4.2 Illegal transitions | Unchanged — still applies to milestone + release |
| §4.3 Override rules | Unchanged |
| §5.1 Failure classes | Taxonomy unchanged |
| §5.3 Evidence requirements | Requirements unchanged |
| §6.2 OverrideRecord | Unchanged |
| §6.3 Transition event schema | Unchanged |
| §6.4 Versioning policy | Unchanged |
| §7.1 Rollout phases | Phases unchanged |
| §7.3 Rollback triggers | Unchanged |
| §8.1 Provisional vs normative | Unchanged |
| §8.2 Calibration method | Unchanged |
| §8.3/8.4 Warning/fail bands | Unchanged |
| §9.1 Override approval model | Unchanged |
| §12.1 GO criteria | Unchanged |
| §12.2 NO-GO criteria | Unchanged |

---

## 3. Dependency Order for Editing

When editing the spec, apply changes in this order to avoid internal inconsistencies:

```
PHASE 0 (blocking — do first):
  R2  → R5  → R1  → R12 → R17 → R18 → R21

PHASE 1 (after phase 0 changes are applied):
  R4  → R3             # Terms before contradictions
  R6                   # §4.4 — references §3.1 terms
  R7                   # §5.2 — references §4.4 freshness concept
  R8                   # §6.1 — references §3.1 AuditGateResult
  R9  → R10            # §7.2 before §8 KPI section
  R11                  # §9.2
  R13 → R14 → R15      # §10 in order
  R16                  # §11
  R19                  # Top 5 Immediate Actions

ANY TIME:
  R20                  # Top 5 Deferred
```

---

## 4. Verification Checklist (post-edit)

After editing, verify these invariants hold:

- [ ] §4.1 task-scope transitions are present but annotated `[v1.3 — deferred]`, not deleted
- [ ] §4.4 contains zero source-file line citations (e.g., no `monitor.py:255-260`)
- [ ] §3.1 defines all 6 new terms: AuditLease, audit_lease_timeout, max_turns, Critical Path Override, audit_gate_required, audit_attempts
- [ ] `AuditGateResult` is used consistently (not `GateResult`) in §6.1
- [ ] §12.3 has 6 blockers (original 4 + 2 new)
- [ ] §12.4 has 6 required decisions (original 5 + 1 new)
- [ ] Open Decisions table has 9 rows (original 5 + 4 new)
- [ ] §10.2 contains zero source-file line number citations
- [ ] §4.4 item 3 defaults are milestone=2 and release=1 only (no task=3)
- [ ] §1.1 contains the branch (b) scope amendment paragraph
- [ ] §2.1 locked decisions list ends at item 6 (branch b as new item)
