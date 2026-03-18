<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (opus:analyzer — Forensic Analyst Validation) -->
<!-- Incorporated: Variant 1 (opus:architect), Variant 3 (sonnet:scribe) -->
<!-- Merge date: 2026-03-17 -->
<!-- Convergence: 89% after 3 rounds + invariant probe -->

# Adversarial Review: v1.2.1 Spec Delta Analysis — Post-v2.26

**Produced by**: 3-agent adversarial debate (opus:architect, opus:analyzer, sonnet:scribe)
**Base variant**: Forensic Analyst Validation (opus:analyzer)
**Date**: 2026-03-17
**Convergence**: 89% (threshold: 85%) after 3 debate rounds + invariant probe
**Method**: Independent codebase inspection + adversarial debate across finding accuracy, severity classification, spec update language, missing coverage, and implementation feasibility

---

## 1. Finding Accuracy — Independent Verification of Each Delta

<!-- Source: Base (Variant 2, Forensic Analyst) -->

### Delta 2.1 — Spec-patch auto-resume cycle still present

**Original claim**: `roadmap/executor.py:1193-1322` still implements `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()`, bounded to 1 cycle at `executor.py:1216-1223`.

**Independent evidence**:
- `executor.py:1193`: `def _apply_resume_after_spec_patch(` — CONFIRMED present.
- `executor.py:1216-1223`: Recursion guard `if cycle_count >= 1:` — CONFIRMED, exact line range.
- `executor.py:1226`: Calls `_find_qualifying_deviation_files()` — CONFIRMED.
- Function runs through line 1322 with the full six-step disk-reread sequence — CONFIRMED.

**Verdict: CONFIRMED**. Line ranges are accurate. The function is live code, not dead — it is called from the main `roadmap_run` flow.

---

### Delta 2.2 — DEVIATION_ANALYSIS_GATE defined but not wired

**Original claim**: `DEVIATION_ANALYSIS_GATE` is fully defined at `roadmap/gates.py:712-758` with strong semantic checks, but `_build_steps()` at `roadmap/executor.py:343-440` does not include a `deviation-analysis` step.

**Independent evidence**:
- `roadmap/gates.py:712-758`: `DEVIATION_ANALYSIS_GATE = GateCriteria(...)` with 6 semantic checks — CONFIRMED.
- `roadmap/gates.py:771`: Listed in `ALL_GATES` — CONFIRMED.
- `roadmap/executor.py:343-440`: `_build_steps()` builds 8 steps; no `deviation-analysis` step — CONFIRMED.
- `roadmap/executor.py:27-38`: Import block does NOT import `DEVIATION_ANALYSIS_GATE` — additional evidence.
- `_check_annotate_deviations_freshness()` at `executor.py:588-675` references `"deviation-analysis"` as a gate_pass_state key (line 669), confirming the pipeline *expects* the step but does not build it.

**Verdict: CONFIRMED**. The gate is fully defined with 6 semantic checks but is not imported into the executor and no step references it. The freshness check at line 669 resets a gate state that is never set — a logical inconsistency the delta analysis understates.

---

### Delta 2.3 — max_turns=100 changes timeout budget arithmetic

**Original claim**: Formula is `max_turns * 120 + 300` for subprocess timeout. At default 100: 12,300 s (3h 25m). Remediation step: `max_turns * 60 = 6,000 s` (1h 40m).

**Independent evidence**:
- `sprint/process.py:115`, `sprint/executor.py:479`: `timeout_seconds=config.max_turns * 120 + 300` — CONFIRMED.
- `sprint/executor.py:78`: `timeout_seconds=self._config.max_turns * 60` — CONFIRMED.
- `pipeline/models.py:175`, `sprint/models.py:294`, `sprint/config.py:163`: `max_turns: int = 100` — CONFIRMED.
- Roadmap step timeouts at `roadmap/executor.py:345-439`: Per-step values 300–900 s — CONFIRMED.

**Verdict: CONFIRMED**. All formulas and values are accurate.

---

### Delta 2.4 — reimbursement_rate=0.8 is a dead model field

**Original claim**: `sprint/models.py:482-487` defines `reimbursement_rate = 0.8` in `TurnLedger` but it is unused.

**Independent evidence**:
- `sprint/models.py:485`: `reimbursement_rate: float = 0.8` — CONFIRMED.
- Grep across all of `src/superclaude/`: Only one hit, the definition — CONFIRMED unused.
- `TurnLedger.credit()` exists (line 499) but nothing calls it with `reimbursement_rate` as multiplier.

**Verdict: CONFIRMED**. The field is defined but unused in any formula.

<!-- Source: Variant 1 (Architect), Delta 2.4 — merged per Change #7 -->
**Note**: The delta's §4.4 item 7 treats this as a normative timeout/retry semantic. Per adversarial consensus, this is a **governance directive** (decide: wire or remove) that belongs in §12.3/§12.4, not in the normative §4.4 section. The risk is maintainability/confusion, not correctness — dead fields cannot produce incorrect results.

---

### Delta 2.5 — STRICT/STANDARD gate tier semantics differ from spec

**Original claim**: STRICT/STANDARD controls validation depth, not blocking behavior. Both tiers block equally because `grace_period=0`.

**Independent evidence**:
- `pipeline/gates.py:20-69`: Tiered validation dispatch (EXEMPT → LIGHT → STANDARD → STRICT) — CONFIRMED.
- `pipeline/models.py:73`: `enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"]` — CONFIRMED.
- `pipeline/models.py:179`: `grace_period: int = 0` — CONFIRMED, all gates blocking by default.
- `pipeline/trailing_gate.py:587-622`: `resolve_gate_mode()` uses `GateMode.BLOCKING` vs `GateMode.TRAILING` — CONFIRMED as separate axis.
- Tasklist SKILL.md line 629: `Tier | <STRICT|STANDARD|LIGHT|EXEMPT>` — CONFIRMED as a third axis.

**Verdict: CONFIRMED**. Three distinct STRICT/STANDARD axes exist. The spec already uses distinct lowercase terms (`strict | standard | legacy_migration`); the collision risk is real but the spec's naming is already differentiated.

---

### Delta 2.6 — Trailing gate framework exists but NOT wired into sprint

**Original claim**: `pipeline/trailing_gate.py` provides full infrastructure but sprint's `execute_sprint()` never calls it. `SprintGatePolicy` is described as a "stub."

**Independent evidence**:
- All four trailing gate components confirmed present in `pipeline/trailing_gate.py`.
- `sprint/executor.py:47-90`: `SprintGatePolicy` — CONFIRMED present with **complete implementations** of `build_remediation_step()` and `files_changed()` (not a stub — it has real logic).
- `execute_sprint()` (line 491+) never instantiates `SprintGatePolicy` — CONFIRMED unwired.
- `tui.py:72`: `gate_states` initialized empty, never populated — CONFIRMED.
- `sprint/kpi.py:14,117`: `DeferredRemediationLog` and `TrailingGateResult` imported and used in `build_kpi_report()` — partial wiring exists in the metrics path.

<!-- Source: Base (modified) — characterization corrected per debate consensus -->
**Verdict: PARTIALLY_CONFIRMED**. The core claim is accurate but the "stub" characterization is wrong — `SprintGatePolicy` is implemented but unwired. The delta also misses that `sprint/kpi.py` already integrates trailing gate types for reporting, so the absolute statement "NOT wired into sprint" is misleading (true for execution, false for metrics).

---

### Delta 2.7 — GateDisplayState is not merely a UI ornament

**Original claim**: `sprint/models.py:70-149` defines `GateDisplayState` with 7 symbolic states and display metadata. No gate_run_id, no score, no evidence, no timing.

**Independent evidence**:
- `sprint/models.py:70-150`: `GateDisplayState` enum with 7 values and `color`, `icon`, `label` properties — CONFIRMED.
- No rich data fields (gate_run_id, score, evidence, timing, etc.) — CONFIRMED absent.
- `TaskResult.gate_outcome` at `models.py:168`: `GateOutcome` enum with PASS/FAIL/DEFERRED/PENDING — CONFIRMED.

<!-- Source: Base (modified) — characterization updated per Change #12 -->
**Verdict: CONFIRMED** on the data gap. However, `GateDisplayState` is **formally a state machine, not merely a UI ornament**: `GATE_DISPLAY_TRANSITIONS` (lines 107-114) defines valid transition pairs and `is_valid_gate_transition()` (line 117) enforces them. The delta's characterization as "UI ornament" understates the design intent. The existing transition model should be referenced as a pattern to extend when building the new `AuditWorkflowState`.

**Additional finding**: `GateResult` classes already exist in `audit/evidence_gate.py:20` (2 fields: `passed`, `reason`) and `audit/manifest_gate.py:42`. Adding a 13-field `GateResult` to `sprint/models.py` creates a namespace collision (MF-2).

---

### Delta 2.8 — Sprint has no audit workflow states

**Original claim**: `PhaseStatus` has 12 states, `TaskStatus` has 4 states. Neither contains any `audit_*` state.

**Independent evidence**:
- `sprint/models.py:206-249`: 12 `PhaseStatus` values (PENDING through SKIPPED) — CONFIRMED, none audit-related.
- `sprint/models.py:40-46`: 4 `TaskStatus` values — CONFIRMED.
- Grep for `audit_` in sprint: zero hits — CONFIRMED.

**Verdict: CONFIRMED**. Zero audit states exist. The 12 audit states from §4.1 are entirely new additions.

---

### Delta 2.9 — No lease/heartbeat mechanism for audit_*_running

**Original claim**: Sprint has heartbeat-like output monitor with 120 s stall threshold but no lease infrastructure.

**Independent evidence**:
- `sprint/monitor.py:255-260`: Updates `last_event_time` and `events_received` — CONFIRMED as liveness tracker.
- `sprint/models.py:452-463`: `stall_status` property with 120 s threshold — CONFIRMED for display.
- `sprint/executor.py:620-653`: Watchdog uses `config.stall_timeout` (defaults to 0=**disabled**) — CONFIRMED.
- No lease infrastructure anywhere in sprint — CONFIRMED.

**Verdict: PARTIALLY_CONFIRMED**. The 120 s threshold is for the `stall_status` display property, not the operational watchdog (which defaults to disabled). The delta conflates the display threshold with the operational mechanism. The stall monitor is softer than presented — it shows "STALLED" in the TUI but does not kill by default. Building the audit lease heartbeat on this substrate means inheriting a disabled-by-default guard condition.

---

### Delta 2.10 — TUI completion guard does not exist

**Original claim**: TUI has no audit-aware completion guard.

**Independent evidence**:
- `sprint/tui.py:254-273`: Renders based on `outcome.value == "success"` — CONFIRMED, no audit check.
- `sprint/executor.py:764-787`: Halts on `status.is_failure` — CONFIRMED, no audit guard.

**Verdict: CONFIRMED**. Zero audit awareness in TUI completion path.

---

### Delta 2.11 — Tasklist generates no audit metadata

**Original claim**: Tasklist phase files have zero audit-awareness fields.

**Independent evidence**:
- Tasklist SKILL.md:622-637: Rich metadata but no audit fields — CONFIRMED.
- `sprint/config.py:235-355`: No audit field parsing — CONFIRMED.
- Grep for `audit_gate_required`: zero hits — CONFIRMED.

**Verdict: CONFIRMED**. Zero audit metadata in tasklist generation or parsing.

<!-- Source: Variant 1 (Architect), NR-1 analysis — merged per Change #8 -->
**Note on NR-1 determinism claim**: The delta states that without `audit_gate_required`, the runner must infer at runtime, "which breaks determinism." This is incorrect — a deterministic derivation function produces the same output regardless of when it executes. The real argument for push-model tasklist metadata is **auditability and transparency** (you can inspect the tasklist to see which tasks will be gated), not determinism.

---

## 2. Severity Classification Validation

<!-- Source: Base (Variant 2, Forensic Analyst) -->

### HIGH severity items

| Item | Claimed Severity | Forensic Assessment | Evidence |
|---|---|---|---|
| Spec-patch auto-resume (2.1) | HIGH — P0 blocker | **CONFIRMED HIGH** | Live code at executor.py:1193-1322, actively called from roadmap_run flow |
| DEVIATION_ANALYSIS_GATE unwired (2.2) | HIGH — audit prerequisite | **CONFIRMED HIGH** | Gate defined with 6 semantic checks; freshness check resets state that is never set |
| `audit_*` states absent (2.8) | HIGH — Phase 1 core | **CONFIRMED HIGH** | Zero audit-related enum values in any sprint model |
| GateResult model absent (2.7) | HIGH — Phase 1 core | **CONFIRMED HIGH** | Only GateDisplayState (rendering) and GateOutcome (4-value enum) exist |
| No lease model (2.9) | HIGH — Phase 2 core | **CONFIRMED HIGH** | No lease infrastructure anywhere in sprint |
| SprintGatePolicy unwired (2.6) | HIGH — Phase 2 core | **CONFIRMED HIGH** | Class exists with real implementations but never instantiated |
| Sprint mainline vs helper (NR-7) | HIGH — integration target | **RECLASSIFY to CRITICAL** | `execute_phase_tasks()` is orphaned dead code (see MF-1) |

### MEDIUM severity items

| Item | Claimed Severity | Forensic Assessment | Evidence |
|---|---|---|---|
| TUI completion guard absent (2.10) | MEDIUM — Phase 3 | **CONFIRMED MEDIUM** | Display-only, no blocking logic |
| Trailing gate unwired in sprint (2.6) | MEDIUM — Phase 2 | **RECLASSIFY to HIGH** | Complete infrastructure with zero execution integration |
| Tasklist no audit metadata (2.11) | MEDIUM | **CONFIRMED MEDIUM** | Downstream dependency, not blocking early phases |
| STRICT/STANDARD axis collision (2.5) | MEDIUM — spec clarity | **CONFIRMED MEDIUM** | Three distinct naming axes confirmed |
| Freshness invalidation (NR-5) | MEDIUM — correctness | **CONFIRMED MEDIUM** | Existing pattern reusable |
| `spec_hash`-style binding (NR-6) | MEDIUM — determinism | **CONFIRMED MEDIUM** | Existing pattern reusable |

<!-- Source: Variant 3 (Scribe), Section 2.1 — merged per Change #2 -->
**Note**: NR-5 and NR-6 describe the same requirement from different angles (reactive invalidation vs proactive binding). Per adversarial consensus, these should be **consolidated into a single finding** with two implementation facets. See Appendix B.

### LOW severity items

| Item | Claimed Severity | Forensic Assessment | Evidence |
|---|---|---|---|
| `reimbursement_rate` dead field (2.4) | LOW | **CONFIRMED LOW** | Single field, single definition, zero usages |

<!-- Source: Variant 3 (Scribe), Section 2.1 — merged per Change #11 -->
| Tasklist schema versioning (NR-2) | LOW | **RECLASSIFY to MEDIUM** | Per §5.2 "Unknown/missing deterministic inputs => failed" — silently accepting stale bundles missing `audit_gate_required` is a correctness risk |

---

## 3. Spec Update Language Verification

<!-- Source: Base (Variant 2, Forensic Analyst) -->

### §4.4 Replacement Language — File:Line Accuracy

| Claim | Verified? |
|---|---|
| `OutputMonitor.last_event_time` mechanism | CONFIRMED (monitor.py:256-259) |
| Bounded model mirrors remediation pattern | CONFIRMED (executor.py:677-723) |
| Turn budget formula `max_turns * 60` | CONFIRMED at executor.py:78 (minor line range imprecision: 73-79 is the full method) |
| `reimbursement_rate = 0.8` in TurnLedger | CONFIRMED at models.py:485 |

### §10.2 Replacement Language — File:Line Accuracy

| Claim | Verified? |
|---|---|
| executor.py:1193-1322 (`_apply_resume_after_spec_patch`) | CONFIRMED |
| executor.py:343-440 (`_build_steps`) | CONFIRMED |
| gates.py:712-758 (`DEVIATION_ANALYSIS_GATE`) | CONFIRMED |
| executor.py:47-90 (`SprintGatePolicy`) | CONFIRMED |
| executor.py:668-717 (post-subprocess integration point) | CONFIRMED |
| executor.py:736-787 (post-classification integration point) | CONFIRMED |
| tui.py:174-203 (phase table) | MINOR INACCURACY — method spans 146-205 |
| tui.py:254-273 (terminal panel) | CONFIRMED |
| executor.py:786-847 (`_save_state`) | CONFIRMED |
| SKILL.md:622-637 (task format) | CONFIRMED |

**Summary**: File paths are all correct. Line ranges accurate within ±5 lines. Function names all correct.

<!-- Source: Variant 3 (Scribe), Section 3.1 — merged per Change #7 -->
**Critical systemic issue**: All source-file line citations must be **removed from normative spec text**. Per adversarial consensus (96% confidence, all three advocates concurred), line numbers in normative spec language become wrong on first refactor. They belong in traceability appendices, not in the spec body. Replace with behavioral descriptions.

---

## 4. Missed Findings

<!-- Source: Base (Variant 2, Forensic Analyst) — unique strength -->

### MF-1 — `execute_phase_tasks()` is ORPHANED dead code (CRITICAL)

**Finding**: `execute_phase_tasks()` at `sprint/executor.py:350-447` is defined and documented but **never called from `execute_sprint()` or anywhere else in the codebase**. The mainline loop at executor.py:574-787 spawns per-phase (not per-task) subprocesses via `ClaudeProcess(config, phase)`.

**Impact**: The entire task-level orchestration model (TurnLedger budgeting, per-task subprocess isolation, task-level gate outcomes) exists only in the orphaned function. The audit gate spec assumes task-level granularity exists in the execution path, but the sprint runner operates at phase granularity only.

**Severity**: **CRITICAL** — task-scope audit gates (`audit_task_*`) have no execution surface in the current architecture. This was confirmed by all three adversarial advocates as the single most consequential finding. See Section 10 for the branch decision framework.

---

### MF-2 — Existing `GateResult` class collision in `cli/audit/`

**Finding**: Two classes named `GateResult` already exist:
- `src/superclaude/cli/audit/evidence_gate.py:20`: `GateResult(passed: bool, reason: str | None)` — 2 fields
- `src/superclaude/cli/audit/manifest_gate.py:42`: `GateResult` (same interface)

The spec proposes a 13-field `GateResult` for `sprint/models.py`. This creates a namespace collision. The 2-field existing struct is structurally incompatible with the spec's 13-field target — this is net-new development, not wiring up existing code.

**Severity**: MEDIUM — requires naming discipline (e.g., `AuditGateResult` vs `EvidenceGateResult`).

---

### MF-3 — `ShadowGateMetrics` and `--shadow-gates` are undiscovered rollout infrastructure

**Finding**: The delta analysis does not mention:
- `ShadowGateMetrics` (`sprint/models.py:571-618`): Tracks `total_evaluated`, `passed`, `failed`, `latency_ms` with percentile properties.
- `SprintConfig.shadow_gates: bool = False` (sprint/config.py:169, sprint/commands.py:178).

This maps directly to the spec's §7 rollout phases (shadow/soft/full). The audit gate rollout can leverage this existing infrastructure.

**Severity**: HIGH (missed integration opportunity). Note: ShadowGateMetrics covers M1 (latency) but not M4/M5/M7/M9 KPI dimensions — reusability is real but limited to one of five required KPI axes (per INV-012).

---

### MF-4 — `cli/audit/` subsystem is a complete parallel audit infrastructure

**Finding**: `src/superclaude/cli/audit/` contains 30+ modules including evidence gates, budget management, checkpointing, classification, escalation, resume/recovery, validation, batch retry, and profile management. The delta analysis does not mention this subsystem.

**Severity**: HIGH — but per INV-010, domain semantics may not align. The existing `GateResult` has only 2 fields vs the spec's 13; the "30+ modules" count should be qualified by actual domain applicability. A targeted survey is needed before assuming reusability.

---

### MF-5 — `cleanup_audit/` is a third gate-aware pipeline

**Finding**: `src/superclaude/cli/cleanup_audit/` contains a full pipeline with its own gate definitions (`GATE_G001` through `GATE_G006`), using shared `pipeline.models.GateCriteria`. Changes to shared pipeline infrastructure for audit gating must not break this third consumer.

**Severity**: MEDIUM — integration risk.

---

### MF-6 — `sprint/kpi.py` already integrates trailing gate types for metrics

**Finding**: `sprint/kpi.py:14` imports `DeferredRemediationLog` and `TrailingGateResult` for `build_kpi_report()`. The delta's absolute claim "NOT wired into sprint" is true for execution but false for metrics.

**Severity**: LOW.

---

### MF-7 — `GATE_DISPLAY_TRANSITIONS` is an existing state machine pattern

**Finding**: `sprint/models.py:107-114` defines a formal transition frozenset for `GateDisplayState`. This is a design pattern to extend when building `AuditWorkflowState`, not something to replace.

**Severity**: LOW — architectural awareness.

---

### MF-8 — `grace_period` field exists but is never exposed via sprint CLI

**Finding**: `pipeline/models.py:179` defines `grace_period: int = 0` (inherited by `SprintConfig`). The TUI gate column activates when `grace_period > 0`, but no CLI flag exposes it.

**Severity**: LOW — dead UI code to activate alongside audit gate wiring.

---

### MF-9 — `_get_all_step_ids()` omits `deviation-analysis`

**Finding**: `roadmap/executor.py:502-518` returns a hardcoded step ID list without `deviation-analysis`. Must be updated alongside `_build_steps()` when wiring the gate — otherwise HALT diagnostics are incomplete.

**Severity**: MEDIUM — P0 prerequisite alongside `_build_steps()` change.

---

### MF-10 — Preflight execution path bypasses phase-level gate evaluation

**Finding**: Phases with `execution_mode in ("python", "skip")` produce `PREFLIGHT_PASS` without entering the main poll loop. If audit gates are added to the main loop, preflight phases silently bypass them. The spec must decide whether preflight phases require audit gating or are exempt.

**Severity**: MEDIUM.

---

## 5. Implementation Feasibility — Revised Phase Ordering

<!-- Source: Base (modified) — replaced per Change #9, incorporating Round 3 consensus -->

### Consensus Phase Plan (post-adversarial review)

The original delta's P0→P3 plan has dependency errors identified by all three advocates. The revised ordering resolves the P2/P3 chicken-and-egg problem and incorporates MF-1 as a prerequisite.

**⚠ BLOCKING DECISION**: The phase plan below assumes **branch (a)** — activating task-scope execution. See Section 10 for the branch decision framework. Under branch (b) (phase-only scope), items marked with ‡ become no-ops.

#### P0: Prerequisites (code cleanup + architectural decision)

- Retire `_apply_resume_after_spec_patch()` (executor.py:1193-1322) and clean up call site
- Wire `deviation-analysis` step into `_build_steps()` (executor.py:343-440)
  - Requires: import `DEVIATION_ANALYSIS_GATE`, add Step, update `_get_all_step_ids()` (MF-9)
  - **Hidden blocker**: `build_deviation_analysis_prompt()` does not exist in `roadmap/prompts.py`
- **Branch decision**: Spec owner must decide task-scope (a) vs phase-only (b) before P1 starts

#### P1: Data models + profile decision

- Add `AuditWorkflowState` enum (12 states under branch (a), 8 under branch (b)‡) alongside `PhaseStatus`/`TaskStatus`
- Add `AuditGateResult` dataclass implementing §6.1 (13 fields) — using disambiguated name per MF-2
- Add `AuditLease` dataclass
- Add profile enum (`strict | standard | legacy_migration`) — **requires D1.2 governance decision first**
- Resolve `reimbursement_rate` fate (wire into audit retry budget or remove)
- Survey `cli/audit/` subsystem for reusable patterns and naming conflicts (MF-4)

#### P2a: Tasklist audit metadata emission

- ‡ Add `audit_gate_required: bool` derivation rules to tasklist generator
- ‡ Add `schema_version` to generated `tasklist-index.md` (NR-2)
- Emit field in generated phase files

#### P2b: Sprint executor integration

- ‡ Activate `execute_phase_tasks()` within `execute_sprint()` mainline (MF-1 resolution, branch (a))
- Complete `SprintGatePolicy` wiring into `execute_sprint()`
- Extend `OutputMonitor` for audit lease heartbeat events
- Integrate `TrailingGateRunner` for task-scope audit gates via `SprintGatePolicy`
- Expose `--grace-period` CLI flag (MF-8)
- Wire `ShadowGateMetrics` for audit gate shadow mode (MF-3)

#### P3: TUI + release guards + rollout

- Extend phase table to display `AuditWorkflowState` values
- Add release guard (block "Sprint Complete" unless `audit_release_passed`)
- Add operator guidance panel for `audit_*_failed` states
- Add `audit` block to `_save_state()` for persistence
- Define rollback/safe-disable triggers (D1.3 — currently STILL OPEN)
- Phase 4 test files: state machine, profiles, overrides, rollout

---

## 6. Undefined Terms and Spec Gaps

<!-- Source: Variant 3 (Scribe), Sections 5.1 and 8.2 — merged per Change #5 -->

### 6.1 Undefined Terms Requiring §3.1 Canonical Definitions

The delta's replacement text introduces 6 terms in normative language without defining them in §3.1 Canonical Terms:

| Term | First Appearance | Definition Needed |
|---|---|---|
| `AuditLease` | §4.4 item 1 | Model with `lease_id`, `owner`, `acquired_at`, `expires_at`, `renewed_at` |
| `audit_lease_timeout` | §4.4 item 2 | Per-scope configurable timeout for lease heartbeat |
| `max_turns` | §4.4 item 6 | Runner configuration for subprocess turn limit (undefined in spec) |
| `Critical Path Override` | §10.2 Phase 3 derivation rule | Tasklist field — values and semantics undefined |
| `audit_gate_required` | §10.2 Phase 3 | Boolean field derived from Tier/Risk/Critical Path Override |
| `audit_attempts` | §4.4 item 3 | Per-entity retry counter persisted in durable state |

These must be defined in §3.1 before appearing in normative text.

---

## 7. Corrected Spec Language Recommendations

<!-- Source: Variant 3 (Scribe), Section 3.1 — merged per Change #3 -->

The delta's §4.4 replacement text embeds mutable source-file line citations in normative language and leaves critical values undefined. Below are corrected versions with line citations removed and behavioral constraints specified.

### §4.4 Item 1 (Lease + Heartbeat) — Corrected

> `audit_*_running` uses a lease model with heartbeat renewal. The lease must have: a unique `lease_id`, an `owner` identifier, `acquired_at` (ISO-8601 UTC), `expires_at` (ISO-8601 UTC), and `renewed_at` (ISO-8601 UTC). The audit gate evaluator must emit a heartbeat renewal event at an interval no greater than `audit_lease_timeout / 3`. The lease mechanism builds on the subprocess stall-detection pattern already present in the runner infrastructure.

### §4.4 Item 2 (Timeout) — Corrected

> Missing heartbeat renewal past `audit_lease_timeout` causes `audit_*_failed(timeout)`. `audit_lease_timeout` is a per-scope configurable value; default values must be approved by the Reliability Owner (§9.2) before Phase 2 GO. The `audit_lease_timeout` must be independent of and no greater than the outer subprocess wall-clock timeout for the same scope.

### §4.4 Item 3 (Retry budget) — Corrected

> Retry is bounded by a per-scope attempt budget. The attempt count for each audited entity (`audit_attempts`) must be persisted in durable state and incremented on each retry. `max_attempts` is configured per scope: task, milestone, and release. Default values for `max_attempts` per scope are **provisional during shadow mode** and become normative only after calibration per §8.2. Provisional defaults: task=3, milestone=2, release=1. These values must be reviewed and approved by the Reliability Owner (§9.2) before Phase 2 GO.

### §4.4 Item 6 (Turn budget ceiling) — Corrected

> The outer wall-clock ceiling for any sprint phase execution is derived from the configured `max_turns` value. Audit gate evaluation must complete within this ceiling. The Reliability Owner (§9.2) must specify the audit gate sub-process time budget as a fraction of the outer ceiling before Phase 2 GO. This value must be documented as a locked decision per §9.3.

### §4.4 Item 7 — Placement Correction

> **This item should be moved to §12.3 (blocker list) or §12.4 (required decisions).** It is a governance directive, not a timeout/retry/recovery semantic. The decision: either wire `reimbursement_rate` into turn-recovery credit for audit retry paths, or remove it from the model to avoid confusion.

---

## 8. Missing Acceptance Criteria

<!-- Source: Variant 3 (Scribe), Section 7 — merged per Change #4 -->

The following items proposed by the delta lack testable acceptance criteria:

| Item | Proposed Change | Missing Criterion |
|---|---|---|
| `AuditLease` model | Introduce new model with 5 fields | What constitutes a valid lease? What is the validation protocol? |
| Heartbeat emission | Evaluator must emit periodic heartbeat | At what frequency? What constitutes a valid heartbeat event? |
| `audit_lease_timeout` | Deferred to Reliability Owner | What is the deadline for this decision? |
| Retry defaults (task=3, milestone=2, release=1) | Suggested defaults | At what shadow-mode measurement threshold do these become normative? |
| `audit_gate_required` derivation | Add derivation rule to SKILL.md | What test verifies the derivation rule produces correct output? |
| Tasklist schema versioning (NR-2) | Require `schema_version` in frontmatter | What is the rejection behavior when version is incompatible? What error class? |
| `reimbursement_rate` fate (NR-4) | Must be resolved before Phase 2 GO | What does "resolved" mean as a deliverable? |
| Stale audit invalidation (NR-5) | Freshness invalidation semantics | What event triggers invalidation? What is the grace period? |
| Artifact binding (NR-6) | Bind gate result to artifact version | Which hash algorithm? What fields are in the hash input? |
| DEVIATION_ANALYSIS_GATE wiring | Add step to `_build_steps()` | What output does the step produce? When does the gate pass? |

---

## 9. Additional Spec Sections Requiring Updates

<!-- Source: Variant 3 (Scribe), Section 6 — merged per Change #6 -->

The delta's Section 4 update table misses these spec sections:

| Section | Required Update | Rationale |
|---|---|---|
| §5.2 (Pass/fail rules) | Clarify "latest" in item 4 to mean "gate result bound to current artifact version" | NR-5/NR-6 resolution requires operational definition of "latest" |
| §7.2 (Promotion criteria) | M7 now includes audit lease staleness incidents | Adding audit lease changes M7's operational meaning |
| §8 (KPI framework) | New audit events feed into M1, M4, M7, M9 metrics | Audit lease heartbeat, attempt budget, and `audit_gate_required` all generate KPI-relevant events |
| §10.3 (Acceptance criteria) | Phase 1 criterion must include "deviation-analysis.md artifact is produced by roadmap pipeline" | Without this, Phase 1 GO can be declared without the prerequisite artifact |
| §3.1 (Canonical Terms) | Add 6 new canonical terms (see Section 6.1) | Understated as MINOR_UPDATE; scope is significant |

---

## 10. MF-1 Resolution — Branch Decision Framework

<!-- Source: Round 3 consensus — merged per Change #10 -->

MF-1 (`execute_phase_tasks()` is orphaned dead code) is the single most consequential finding from this adversarial review. Its resolution is a **binary fork** that changes the meaning of downstream findings.

### Branch (a): Activate Task-Scope Execution

- Wire `execute_phase_tasks()` into the `execute_sprint()` mainline loop
- All 12 audit states from §4.1 are required
- NR-1 (`audit_gate_required` per task) is required
- Task-scope audit gates (`audit_task_*`) become implementable
- TurnLedger integration becomes operative
- Risk: Activating dead code that has never run in production

### Branch (b): Phase-Only Scope

- Audit gates operate at phase granularity only
- 4 of 12 audit states (`audit_task_*`) become unnecessary → 8-state machine
- NR-1 (`audit_gate_required` per task) loses its consumer → no-op or phase-level aggregation
- Simpler implementation, lower risk
- Risk: Spec deviation — the spec mandates task-scope in §4.1, §4.3, §5.2

### Items Conditional on Branch (a)

| Item | Under Branch (a) | Under Branch (b) |
|---|---|---|
| NR-1 (audit_gate_required per task) | Required | No-op or aggregated to phase level |
| §4.1 audit_task_* states (4 of 12) | Required | Unnecessary |
| P2a (tasklist metadata emission) | Required | Scope-reduced |
| P2b (execute_phase_tasks activation) | Required | Not needed |
| TurnLedger integration | Required | Not needed |

### Resolution Protocol

**This is a blocking spec-owner decision.** The remediation plan assumes branch (a) as the default (spec-aligned per §4.1, §4.3, §5.2). If branch (b) is selected, all items marked with ‡ in Section 5 become no-ops.

The spec owner must decide before Phase 1 implementation begins. The decision must be documented as a locked decision per §9.3.

---

## 11. Summary

<!-- Source: Base (modified) — updated with merged counts -->

### Finding Verification

| Category | Count |
|---|---|
| CONFIRMED | 9 |
| PARTIALLY_CONFIRMED | 2 |
| REFUTED | 0 |
| New findings (MISSED) | 10 |

### Severity Reclassifications

| Item | Original | Reclassified | Evidence |
|---|---|---|---|
| NR-7 (Sprint mainline) | HIGH | **CRITICAL** | `execute_phase_tasks()` is orphaned dead code |
| Delta 2.6 (Trailing gate) | MEDIUM | **HIGH** | Complete infrastructure with zero execution integration |
| NR-2 (Schema versioning) | LOW | **MEDIUM** | Correctness risk per §5.2 deterministic input rule |

### Adversarial Debate Outcomes

| Outcome | Detail |
|---|---|
| Convergence | 89% (threshold: 85%) |
| Rounds | 3 + invariant probe (16 invariants, 4 HIGH resolved) |
| Consensus items | MF-1 CRITICAL, Delta 2.1 HIGH, line citations removal, NR-5/NR-6 merge, phase reordering, §4.4 defaults unjustified |
| Overridden positions | NR-3 downgraded from "real finding" to "recommended spec amendment" (INV-005) |
| Blocking decisions | MF-1 branch (a)/(b) — spec-owner decision required |

### Critical Gaps in Original Delta Analysis

1. **Architectural**: Assumes task-level execution granularity exists (MF-1 shows it does not)
2. **Coverage**: `cli/audit/` (30+ modules) and `cleanup_audit/` entirely absent
3. **Rollout infrastructure**: `ShadowGateMetrics` is a ready-made rollout vehicle not mentioned
4. **Spec language quality**: Line citations in normative text, 6 undefined terms, 10 missing acceptance criteria
5. **P0 completeness**: Deviation-analysis step requires a prompt builder that does not exist

---

## Appendix A: Recommended Spec Amendments

<!-- Source: Variant 1 (Architect) + Round 3 INV-005 resolution — merged per Change #1 -->

The following items are recommendations for spec improvement, not implementation findings. They were reclassified during the adversarial debate.

### NR-3 — deviation-analysis step as audit prerequisite (Reclassified)

**Original classification**: Independent real finding (P0 prerequisite)
**Reclassified to**: Recommended spec amendment

**Rationale**: The invariant probe (INV-005) identified that NR-3's validity was resolved by majority vote rather than by checking whether any §5.1-§5.3 evaluation rule actually references the `deviation-analysis.md` artifact. The Architect's position — that the deviation-analysis gate is a roadmap pipeline completeness issue independent of sprint audit gates — prevailed (92% confidence). The spec *should* reference this artifact, but no existing normative text requires it.

**Recommendation**: Add `deviation-analysis.md` as a referenced artifact in §10.3 Phase 1 acceptance criteria.

---

## Appendix B: Finding Consolidations

<!-- Source: Variant 1 (Architect) + Round 2 consensus — merged per Change #2 -->

### NR-5 + NR-6 → Consolidated Finding: Audit Gate Result Freshness

**NR-5** (stale audit gate results need freshness invalidation) and **NR-6** (`spec_hash`-style audit result binding) describe the same requirement from different angles:
- NR-5 is the **reactive** facet: when an upstream artifact changes, the gate result must be invalidated
- NR-6 is the **proactive** facet: gate results must be bound to specific artifact versions via hash

These should be consolidated into a single finding: "Audit gate results must be bound to artifact versions and invalidated when those artifacts change." The implementation requires both facets — binding without invalidation cannot detect staleness; invalidation without binding cannot determine what to invalidate.
