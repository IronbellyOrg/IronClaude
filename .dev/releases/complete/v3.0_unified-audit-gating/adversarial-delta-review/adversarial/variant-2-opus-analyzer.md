# Variant 2: Forensic Analyst Validation

**Analyst**: Opus 4.6 (1M context) -- Forensic Implementation Validator
**Date**: 2026-03-17
**Method**: Independent codebase inspection of every file and line range cited in the delta analysis, plus exhaustive search for missed integration points.
**Scope**: All deltas (2.1--2.11), new requirements (NR-1 through NR-7), severity classifications, spec replacement language, and missing coverage.

---

## 1. Finding Accuracy -- Independent Verification of Each Delta

### Delta 2.1 -- Spec-patch auto-resume cycle still present

**Original claim**: `roadmap/executor.py:1193-1322` still implements `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()`, bounded to 1 cycle at `executor.py:1216-1223`.

**Independent evidence**:
- `executor.py:1193`: `def _apply_resume_after_spec_patch(` -- CONFIRMED present.
- `executor.py:1216-1223`: Recursion guard `if cycle_count >= 1:` -- CONFIRMED, exact line range.
- `executor.py:1226`: Calls `_find_qualifying_deviation_files()` -- CONFIRMED.
- Function runs through line 1322 with the full six-step disk-reread sequence -- CONFIRMED.

**Verdict: CONFIRMED**. Line ranges are accurate. The function is live code, not dead -- it is called from the main `roadmap_run` flow.

---

### Delta 2.2 -- DEVIATION_ANALYSIS_GATE defined but not wired

**Original claim**: `DEVIATION_ANALYSIS_GATE` is fully defined at `roadmap/gates.py:712-758` with strong semantic checks, but `_build_steps()` at `roadmap/executor.py:343-440` does not include a `deviation-analysis` step. The gate exists in `ALL_GATES` at `roadmap/gates.py:760-774` but has no execution wiring.

**Independent evidence**:
- `roadmap/gates.py:712-758`: `DEVIATION_ANALYSIS_GATE = GateCriteria(...)` with 6 semantic checks (`_no_ambiguous_deviations`, `_validation_complete_true`, `_routing_ids_valid`, `_slip_count_matches_routing`, `_pre_approved_not_in_fix_roadmap`, `_total_analyzed_consistent`) -- CONFIRMED.
- `roadmap/gates.py:771`: `("deviation-analysis", DEVIATION_ANALYSIS_GATE)` in `ALL_GATES` list -- CONFIRMED.
- `roadmap/executor.py:343-440`: `_build_steps()` builds 8 sequential/parallel steps: extract, generate-A/B, diff, debate, score, merge, test-strategy, spec-fidelity. No `deviation-analysis` step -- CONFIRMED.
- `roadmap/executor.py:27-38`: Import block includes `SPEC_FIDELITY_GATE`, `TEST_STRATEGY_GATE`, etc. but does NOT import `DEVIATION_ANALYSIS_GATE` -- additional evidence of unwired state.
- `_check_annotate_deviations_freshness()` at `executor.py:588-675` references `"deviation-analysis"` as a gate_pass_state key (line 669), confirming the pipeline *expects* the step but does not build it.

**Verdict: CONFIRMED**. The gate is fully defined with 6 semantic checks but is not imported into the executor and no step references it. The freshness check function at line 669 even resets the `deviation-analysis` gate state, creating a logical inconsistency: it resets a gate that is never evaluated.

**Additional finding**: The analysis correctly identifies this as unwired but understates the inconsistency. The freshness check presumes a `deviation-analysis` gate pass state exists, but since the step is never executed, that state key is never set.

---

### Delta 2.3 -- max_turns=100 changes timeout budget arithmetic

**Original claim**: Formula is `max_turns * 120 + 300` for subprocess timeout. At default 100: 12,300 s (3h 25m). Remediation step: `max_turns * 60 = 6,000 s` (1h 40m).

**Independent evidence**:
- `sprint/process.py:115`: `timeout_seconds=config.max_turns * 120 + 300` -- CONFIRMED.
- `sprint/executor.py:479`: `timeout_seconds=config.max_turns * 120 + 300` (in `_run_task_subprocess`) -- CONFIRMED.
- `sprint/executor.py:78`: `timeout_seconds=self._config.max_turns * 60` (in `SprintGatePolicy.build_remediation_step`) -- CONFIRMED.
- `pipeline/models.py:175`: `max_turns: int = 100` in `PipelineConfig` -- CONFIRMED.
- `sprint/models.py:294`: `max_turns: int = 100` in `SprintConfig` -- CONFIRMED.
- `sprint/config.py:163`: `max_turns: int = 100` default in `load_sprint_config` -- CONFIRMED.
- Roadmap step timeouts at `roadmap/executor.py:345-439`: Per-step values are 300 (extract), 900 (generate), 300 (diff), 600 (debate), 300 (score), 600 (merge), 300 (test-strategy), 600 (spec-fidelity) -- CONFIRMED.

**Verdict: CONFIRMED**. All formulas and values are accurate. The 3h25m ceiling per subprocess is correct arithmetic.

---

### Delta 2.4 -- reimbursement_rate=0.8 is a dead model field

**Original claim**: `sprint/models.py:482-487` defines `reimbursement_rate = 0.8` in `TurnLedger` but it is unused in any formula.

**Independent evidence**:
- `sprint/models.py:485`: `reimbursement_rate: float = 0.8` -- CONFIRMED.
- Grep for `reimbursement_rate` across all of `src/superclaude/`: Only one hit, the definition itself -- CONFIRMED unused.
- `TurnLedger.credit()` exists (line 499) and accepts an arbitrary `turns` parameter, but nothing calls it with `reimbursement_rate` as a multiplier.
- `TaskResult.reimbursement_amount` (models.py:169) exists but is always initialized to 0 and only displayed in context summaries.

**Verdict: CONFIRMED**. The field is defined, the class has a `credit()` method, but nothing in the codebase computes `turns * reimbursement_rate` or uses the field in any formula.

---

### Delta 2.5 -- STRICT/STANDARD gate tier semantics differ from spec

**Original claim**: In pipeline/roadmap, STRICT/STANDARD controls validation depth (STRICT adds semantic checks), not blocking behavior. Both tiers block execution equally because `grace_period=0` by default.

**Independent evidence**:
- `pipeline/gates.py:20-69`: `gate_passed()` dispatches on `tier` string: EXEMPT always passes, LIGHT checks exists+non-empty, STANDARD adds min_lines+frontmatter, STRICT adds semantic checks. This is validation depth, not blocking behavior -- CONFIRMED.
- `pipeline/models.py:73`: `enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"]` -- CONFIRMED as validation tier.
- `pipeline/models.py:179`: `grace_period: int = 0` -- CONFIRMED, so all gates are blocking by default.
- `pipeline/trailing_gate.py:587-622`: `resolve_gate_mode()` uses `GateMode.BLOCKING` vs `GateMode.TRAILING`, which is the actual blocking/non-blocking axis -- CONFIRMED as separate from enforcement_tier.
- Tasklist protocol SKILL.md line 629: `Tier | <STRICT|STANDARD|LIGHT|EXEMPT>` -- CONFIRMED as a third distinct axis (compliance tier).

**Verdict: CONFIRMED**. Three distinct STRICT/STANDARD axes exist: (1) pipeline gate validation depth, (2) tasklist compliance tier, (3) the spec's proposed audit profile enforcement level.

---

### Delta 2.6 -- Trailing gate framework exists but is NOT wired into sprint

**Original claim**: `pipeline/trailing_gate.py` provides `TrailingGateRunner`, `DeferredRemediationLog`, `attempt_remediation()`, and `resolve_gate_mode()`. Sprint's `execute_sprint()` never calls them. `SprintGatePolicy` exists at `sprint/executor.py:47-90` as a stub but is unwired. `tui.gate_states` exists but is never populated by executor.

**Independent evidence**:
- `pipeline/trailing_gate.py`: `TrailingGateRunner` (line 88), `DeferredRemediationLog` (line 489), `attempt_remediation()` (line 358), `resolve_gate_mode()` (line 587) -- all CONFIRMED present.
- `sprint/executor.py:47-90`: `SprintGatePolicy` -- CONFIRMED present with `build_remediation_step()` and `files_changed()` methods implemented (not a pure stub -- it has real logic).
- `sprint/executor.py:36-37`: Imports `TrailingGatePolicy, TrailingGateResult` from pipeline -- CONFIRMED.
- Grep for `SprintGatePolicy` usage in executor: only the class definition. `execute_sprint()` (line 491+) never instantiates it -- CONFIRMED unwired.
- `tui.py:72`: `self.gate_states: dict[int, GateDisplayState] = {}` -- CONFIRMED initialized but never populated by executor.
- `sprint/kpi.py:14,117`: `DeferredRemediationLog` and `TrailingGateResult` are imported and used in `build_kpi_report()` -- this is a KPI aggregation function, not execution wiring.

**Verdict: PARTIALLY_CONFIRMED**. The core claim is accurate. However, the analysis describes `SprintGatePolicy` as a "stub" which understates it -- it has complete implementations of `build_remediation_step()` and `files_changed()`. The issue is not that it is a stub but that it is never instantiated or called from the execution loop. The analysis also misses that `sprint/kpi.py` already integrates `DeferredRemediationLog` for reporting, suggesting partial wiring exists in the metrics path even if the execution path is unwired.

---

### Delta 2.7 -- GateDisplayState is a UI ornament, not a GateResult model

**Original claim**: `sprint/models.py:70-149` defines `GateDisplayState` with 7 symbolic states and display metadata (color, icon, label). It has no gate_run_id, no score, no evidence, no timing.

**Independent evidence**:
- `sprint/models.py:70-150`: `GateDisplayState` enum with 7 values (NONE, CHECKING, PASS, FAIL_DEFERRED, REMEDIATING, REMEDIATED, HALT) and properties `color`, `icon`, `label` -- CONFIRMED.
- No `gate_run_id`, `score`, `evidence`, `timing`, `threshold`, `checks`, `drift_summary`, `override`, `failure_class` fields -- CONFIRMED absent.
- `TaskResult.gate_outcome` at `models.py:168`: `GateOutcome` enum with PASS/FAIL/DEFERRED/PENDING -- CONFIRMED as 4-value enum with no rich data.

**Verdict: CONFIRMED**. `GateDisplayState` is purely rendering metadata. `GateOutcome` is a simple 4-value enum. Neither approaches the 13+ field `GateResult` the spec requires.

**Additional finding**: There is already a `GateResult` class in `audit/evidence_gate.py:20` (fields: `passed: bool`, `reason: str | None`) and another in `audit/manifest_gate.py:42`. If the spec adds a new `GateResult` to `sprint/models.py`, there will be a namespace collision risk across the codebase. The delta analysis does not flag this.

---

### Delta 2.8 -- Sprint has no audit workflow states

**Original claim**: `PhaseStatus` at `sprint/models.py:206-249` has 12 states but none are audit workflow states. `TaskStatus` has 4 states. Neither contains any `audit_*` state.

**Independent evidence**:
- `sprint/models.py:206-249`: `PhaseStatus` enum with values: PENDING, RUNNING, PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED, PREFLIGHT_PASS, INCOMPLETE, HALT, TIMEOUT, ERROR, SKIPPED -- 12 values, CONFIRMED none are audit-related.
- `sprint/models.py:40-46`: `TaskStatus` with PASS, FAIL, INCOMPLETE, SKIPPED -- 4 values, CONFIRMED.
- Grep for `audit_` in sprint directory: zero hits -- CONFIRMED.

**Verdict: CONFIRMED**. The analysis correctly counts 12 PhaseStatus values (though RUNNING is not counted as a terminal state, so the count of distinct values is 12, matching the claim).

---

### Delta 2.9 -- No lease/heartbeat mechanism for audit_*_running

**Original claim**: Sprint has heartbeat-like output monitor at `sprint/monitor.py:255-260` with 120 s stall threshold, but no lease token, no lease owner, no lease expiry, no `audit_*_failed(timeout)` transition.

**Independent evidence**:
- `sprint/monitor.py:255-260`: Inside `_process_chunk`, lines update `self.state.last_event_time = now` and `self.state.events_received += 1` -- CONFIRMED as the heartbeat-like liveness tracker.
- `sprint/models.py:452-463`: `MonitorState.stall_status` property: `if since_last > 120: return "STALLED"` -- CONFIRMED 120 s threshold.
- `sprint/executor.py:620-653`: Watchdog uses `config.stall_timeout` (configurable, defaults to 0=disabled, NOT 120s) to trigger kill/warn -- PARTIALLY_CONFIRMED. The 120 s threshold is in `MonitorState.stall_status` for display, but the actual watchdog uses `config.stall_timeout` which defaults to 0 (disabled).
- No `lease`, `lease_id`, `lease_owner`, `acquired_at`, `expires_at`, `renewed_at` anywhere in sprint -- CONFIRMED absent.

**Verdict: PARTIALLY_CONFIRMED**. The 120 s threshold is for the `stall_status` property (display string), not for the actual watchdog kill. The watchdog uses `config.stall_timeout` which defaults to 0 (disabled). The analysis conflates the display threshold with the operational watchdog. The stall monitor is softer than presented -- it shows "STALLED" in the TUI but does not kill by default.

---

### Delta 2.10 -- TUI completion guard does not exist

**Original claim**: TUI has no audit-aware completion guard. Blocking is done by `executor.py:764-810`. TUI renders `SprintOutcome.SUCCESS/HALTED` but never checks audit states.

**Independent evidence**:
- `sprint/tui.py:254-273` (`_build_terminal_panel`): Renders "Sprint Complete" or "Sprint Halted" based on `sr.outcome.value == "success"` -- CONFIRMED, no audit state check.
- `sprint/executor.py:764-787`: `if status.is_failure:` triggers HALTED outcome and break -- CONFIRMED.
- `sprint/executor.py:806-809`: Final verification that all phases passed, sets ERROR if not -- CONFIRMED, no audit guard.

**Verdict: CONFIRMED**. The TUI completion path has zero audit awareness. The analysis line ranges are accurate.

---

### Delta 2.11 -- Tasklist generates no audit metadata

**Original claim**: Tasklist phase files emit rich metadata but zero audit-awareness fields. No `audit_gate_required`, `audit_scope`, or `gate_override_allowed`.

**Independent evidence**:
- `sc-tasklist-protocol/SKILL.md:622-637`: Task format shows fields: Roadmap Item IDs, Why, Effort, Risk, Risk Drivers, Tier, Confidence, Requires Confirmation, Critical Path Override, Verification Method, MCP Requirements, Fallback Allowed, Sub-Agent Delegation, Deliverable IDs -- CONFIRMED, no audit fields.
- `sprint/config.py:235-355` (`parse_tasklist`): Extracts task_id, title, dependencies, command, classifier -- CONFIRMED, no audit field parsing.
- Grep for `audit_gate_required` in tasklist directory: zero hits -- CONFIRMED.

**Verdict: CONFIRMED**. Zero audit metadata in tasklist generation or parsing.

---

## 2. Severity Classification Validation

### HIGH severity items

| Item | Claimed Severity | Forensic Assessment | Evidence |
|---|---|---|---|
| Spec-patch auto-resume still present (2.1) | HIGH -- P0 blocker | **CONFIRMED HIGH** | Live code at executor.py:1193-1322, actively called. Retirement is prerequisite per approved-immediate. |
| DEVIATION_ANALYSIS_GATE unwired (2.2) | HIGH -- audit prerequisite | **CONFIRMED HIGH** | Gate defined at gates.py:712 with 6 semantic checks, executor does not import it. Freshness check at executor.py:669 resets its state despite never being set. |
| `audit_*` states absent (2.8) | HIGH -- Phase 1 core | **CONFIRMED HIGH** | Zero audit-related enum values in PhaseStatus or TaskStatus. |
| GateResult model absent (2.7) | HIGH -- Phase 1 core | **CONFIRMED HIGH** | Only GateDisplayState (rendering) and GateOutcome (4-value enum) exist. |
| No lease model (2.9) | HIGH -- Phase 2 core | **CONFIRMED HIGH** | No lease infrastructure anywhere in sprint code. |
| SprintGatePolicy unwired (2.6) | HIGH -- Phase 2 core | **CONFIRMED HIGH** | Class exists with real implementations but is never instantiated. |
| Sprint mainline vs helper (NR-7) | HIGH -- integration target | **RECLASSIFY to CRITICAL** | `execute_phase_tasks()` is defined but **never called from `execute_sprint()`**. The mainline loop at executor.py:574-787 runs per-phase subprocesses directly; `execute_phase_tasks()` is an orphaned function. This is a larger gap than presented -- there is no task-level granularity in the mainline at all. |

### MEDIUM severity items

| Item | Claimed Severity | Forensic Assessment | Evidence |
|---|---|---|---|
| TUI completion guard absent (2.10) | MEDIUM -- Phase 3 | **CONFIRMED MEDIUM** | Display-only, no blocking logic. |
| Trailing gate not wired into sprint (2.6) | MEDIUM -- Phase 2 | **RECLASSIFY to HIGH** | The trailing gate infrastructure is complete but the sprint executor has zero integration. This blocks both audit task-scope gates and the shadow_gates feature. |
| Tasklist emits no audit metadata (2.11) | MEDIUM -- needed before sprint can declare | **CONFIRMED MEDIUM** | Correct -- downstream dependency, not blocking early phases. |
| STRICT/STANDARD axis collision (2.5) | MEDIUM -- spec clarity | **CONFIRMED MEDIUM** | Three distinct naming axes confirmed. |
| Freshness invalidation (NR-5) | MEDIUM -- correctness | **CONFIRMED MEDIUM** | Existing pattern at executor.py:588-675 is reusable. |
| `spec_hash`-style binding (NR-6) | MEDIUM -- determinism | **CONFIRMED MEDIUM** | Pattern at executor.py:792-806 is reusable. |

### LOW severity items

| Item | Claimed Severity | Forensic Assessment | Evidence |
|---|---|---|---|
| `reimbursement_rate` dead field (2.4) | LOW -- must resolve before P2 | **CONFIRMED LOW** | Single field, single definition, zero usages. |
| Tasklist schema versioning (NR-2) | LOW -- correctness risk | **CONFIRMED LOW** | No `schema_version` in tasklist models or config. |

---

## 3. Spec Update Language Verification

### SS4.4 Replacement Language

| Claim | File:Line | Verified? |
|---|---|---|
| "OutputMonitor.last_event_time mechanism" at `sprint/monitor.py:255-260` | monitor.py:256-259 updates `last_event_time` | CONFIRMED -- lines 256-259 in `_process_chunk` |
| "Bounded model mirrors roadmap/executor.py:677-723" | executor.py:677-723 `_check_remediation_budget()` | CONFIRMED -- reads `remediation_attempts` from state, enforces `max_attempts=2` |
| "Turn budget formula max_turns * 120 + 300" at `sprint/executor.py:73-79` | executor.py:78 `timeout_seconds=self._config.max_turns * 60` | **INACCURACY**: The replacement text says "the turn budget is `max_turns * 60 s` (the remediation step formula, `sprint/executor.py:73-79`)" -- the formula is at line 78, not spanning 73-79. Lines 73-79 encompass the entire `build_remediation_step` method. Minor line range imprecision. |
| "`reimbursement_rate = 0.8` in TurnLedger at `sprint/models.py:482-487`" | models.py:485 | CONFIRMED -- field at line 485, TurnLedger class starts at 474. Lines 482-487 capture the relevant fields (initial_budget through minimum_remediation_budget). |

### SS10.2 Replacement Language

| Claim | File:Line | Verified? |
|---|---|---|
| "executor.py:1193-1322 remove `_apply_resume_after_spec_patch()`" | executor.py:1193-1322 | CONFIRMED |
| "executor.py:343-440 add deviation-analysis step" | executor.py:343-440 `_build_steps()` | CONFIRMED -- line 440 is `return steps` but actual step list is 343-442 |
| "roadmap/gates.py:712-758 DEVIATION_ANALYSIS_GATE" | gates.py:712-758 | CONFIRMED |
| "sprint/executor.py:47-90 SprintGatePolicy" | executor.py:47-90 | CONFIRMED |
| "executor.py:668-717 post-subprocess, pre-classification" | executor.py:668-717 | CONFIRMED -- exit code handling through status determination |
| "executor.py:736-787 post-classification, pre-halt" | executor.py:736-787 | CONFIRMED -- PhaseResult construction through halt decision |
| "sprint/tui.py:174-203 phase table row" | tui.py:146-205 `_build_phase_table` | **MINOR INACCURACY**: The phase table method spans 146-205, not 174-203. Lines 174-203 capture the inner loop portion (starting at `for phase in self.config.active_phases:` at line 165). |
| "tui.py:254-273 release guard" | tui.py:254-273 `_build_terminal_panel` | CONFIRMED |
| "executor.py:786-847 add audit block to _save_state()" | executor.py:780-847 `_save_state` | CONFIRMED -- function starts at 780 (def line), 786 is the docstring start. State file written at 847. |
| "tasklist-protocol/SKILL.md:622-637" | SKILL.md:622-637 | CONFIRMED -- lines contain the task format table with Tier, Risk, etc. |

**Summary of SS10.2 accuracy**: File paths are all correct. Line ranges are accurate to within 5 lines in most cases, with one notable imprecision on tui.py. Function names are all correct.

---

## 4. MISSED FINDINGS

This section identifies issues the delta analysis did not flag.

### MF-1 -- `execute_phase_tasks()` is an ORPHANED function (CRITICAL)

**Finding**: `execute_phase_tasks()` at `sprint/executor.py:350-447` is defined and documented but **never called from `execute_sprint()` or anywhere else in the codebase**. The analysis (NR-7) notes that the mainline must be extended "not just execute_phase_tasks()", implying `execute_phase_tasks()` is the secondary path. In reality, it is a dead code path -- the mainline loop at executor.py:574-787 spawns per-phase (not per-task) subprocesses via `ClaudeProcess(config, phase)`.

**Impact**: The entire task-level orchestration model (TurnLedger budgeting, per-task subprocess isolation, task-level gate outcomes) exists only in the orphaned `execute_phase_tasks()`. The audit gate spec assumes task-level granularity exists in the execution path, but the actual sprint runner operates at phase granularity only. This is a fundamental architecture gap, not just an integration point.

**Severity**: CRITICAL -- this means task-scope audit gates (`audit_task_*`) have no execution surface to attach to in the current architecture.

---

### MF-2 -- Existing `GateResult` class collision in `cli/audit/`

**Finding**: Two classes named `GateResult` already exist:
- `src/superclaude/cli/audit/evidence_gate.py:20`: `GateResult(passed: bool, reason: str | None)`
- `src/superclaude/cli/audit/manifest_gate.py:42`: `GateResult` (same interface)

The delta analysis proposes adding a new `GateResult` dataclass to `sprint/models.py` implementing SS6.1 with 13+ fields. This creates a namespace collision. Imports like `from superclaude.cli.audit.evidence_gate import GateResult` and `from superclaude.cli.sprint.models import GateResult` would conflict.

**Severity**: MEDIUM -- requires naming discipline (e.g., `AuditGateResult` vs `EvidenceGateResult`) to be addressed in Phase 1 design.

---

### MF-3 -- `ShadowGateMetrics` and `shadow_gates` flag are undiscovered integration points

**Finding**: The delta analysis does not mention `ShadowGateMetrics` (`sprint/models.py:571-618`) or the `--shadow-gates` CLI flag (`sprint/commands.py:178`, `sprint/config.py:169`, `sprint/models.py:305`). This is a complete shadow-mode gate evaluation infrastructure:

- `ShadowGateMetrics`: Tracks `total_evaluated`, `passed`, `failed`, `latency_ms` with `p50_latency_ms` and `p95_latency_ms` percentile properties.
- `SprintConfig.shadow_gates: bool = False` -- flag to enable shadow mode.

This is directly relevant to the spec's SS7 rollout phases (shadow/soft/full). The audit gate rollout can leverage this existing shadow infrastructure for Phase 1 (shadow mode) instead of building from scratch.

**Severity**: HIGH (as a missed opportunity) -- this existing infrastructure directly maps to the spec's rollout plan and should be cited as an integration opportunity alongside SS3.1-3.7.

---

### MF-4 -- `cli/audit/` subsystem is a complete parallel audit infrastructure

**Finding**: The delta analysis does not mention `src/superclaude/cli/audit/` at all, despite it containing 30+ modules with directly relevant audit infrastructure:

- `audit/evidence_gate.py`: Evidence-gated classification with `GateResult`
- `audit/budget.py`: Budget management for audit operations
- `audit/checkpoint.py`: Checkpointing for long-running audit processes
- `audit/classification.py`: Classification pipeline
- `audit/escalation.py`: Escalation logic
- `audit/resume.py`: Resume/recovery for audit processes
- `audit/validation.py` and `audit/validation_output.py`: Validation infrastructure
- `audit/batch_retry.py`: Batch retry logic
- `audit/batch_decomposer.py`: Batch decomposition
- `audit/profiler.py` and `audit/profile_generator.py`: Profile management

This is a complete audit subsystem that the unified audit gating spec should either integrate with, reuse patterns from, or explicitly declare out-of-scope. The spec's evidence requirements (SS5.3), failure classes (SS5.1), and retry logic (SS4.4) have analogues here.

**Severity**: HIGH -- an entire audit subsystem exists that may contain reusable patterns, naming conflicts, or architectural constraints not accounted for in the spec.

---

### MF-5 -- `cleanup_audit/` is another gate-aware pipeline not mentioned

**Finding**: `src/superclaude/cli/cleanup_audit/` contains a full pipeline with its own gate definitions (`cleanup_audit/gates.py` with `GATE_G001` through `GATE_G006`), executor, monitor, TUI, and models -- all using the shared `pipeline.models.GateCriteria` and `pipeline.gates.gate_passed` infrastructure.

This is relevant because:
1. It demonstrates a third consumer of the pipeline gate infrastructure (alongside roadmap and sprint).
2. Its `ALL_GATES` dict pattern differs from roadmap's `ALL_GATES` list pattern -- inconsistency.
3. Any changes to `pipeline/gates.py` or `pipeline/models.py` for audit gating must not break this consumer.

**Severity**: MEDIUM -- integration risk. Changes to shared pipeline infrastructure affect three consumers, not two.

---

### MF-6 -- `sprint/kpi.py` already integrates trailing gate types for metrics

**Finding**: `sprint/kpi.py:14` imports `DeferredRemediationLog` and `TrailingGateResult`, and `build_kpi_report()` at line 115 aggregates gate pass/fail counts, latency percentiles, and remediation metrics. This is a partial wiring of the trailing gate infrastructure into sprint -- not for execution, but for reporting.

The delta analysis claims the trailing gate is "NOT wired into sprint" (Delta 2.6). This is true for execution but false for metrics. The KPI integration point should be referenced as existing Phase 2 infrastructure.

**Severity**: LOW -- but the delta analysis's absolute language ("NOT wired into sprint") is misleading.

---

### MF-7 -- `GATE_DISPLAY_TRANSITIONS` frozenset is an existing state machine

**Finding**: `sprint/models.py:107-114` defines `GATE_DISPLAY_TRANSITIONS` as a frozenset of valid `(from_state, to_state)` pairs for `GateDisplayState`, plus `is_valid_gate_transition()` at line 117. This is already a minimal state machine for gate display lifecycle:

```
NONE -> CHECKING -> PASS
NONE -> CHECKING -> FAIL_DEFERRED -> REMEDIATING -> REMEDIATED
NONE -> CHECKING -> FAIL_DEFERRED -> REMEDIATING -> HALT
```

The delta analysis proposes adding 12 audit workflow states (SS4.1) as a new `AuditWorkflowState` enum. The existing `GateDisplayState` transition model should be referenced as a design pattern to extend, not as something to be replaced.

**Severity**: LOW -- architectural awareness, not a blocker.

---

### MF-8 -- `grace_period` field exists on `PipelineConfig` but is never set by sprint CLI

**Finding**: `pipeline/models.py:179` defines `grace_period: int = 0` on `PipelineConfig`, which `SprintConfig` inherits. The `tui.py:73` checks `getattr(config, "grace_period", 0) > 0` to decide whether to show the gate column. But `sprint/config.py:load_sprint_config()` and `sprint/commands.py` never expose a `--grace-period` CLI option.

This means the trailing gate UI (gate column in phase table) can never be activated through the CLI, even though the code is ready. The audit gate spec should address this as a Phase 2 CLI surface item.

**Severity**: LOW -- but it represents dead UI code that should be activated alongside audit gate wiring.

---

### MF-9 -- `_get_all_step_ids()` omits `deviation-analysis` from the step ID list

**Finding**: `roadmap/executor.py:502-518` defines `_get_all_step_ids()` which returns a hardcoded list of step IDs: `["extract", "generate-A", "generate-B", "diff", "debate", "score", "merge", "test-strategy", "spec-fidelity", "remediate", "certify"]`. The `deviation-analysis` step is absent from this list.

This function is used for HALT diagnostics (reporting skipped steps). Even after wiring `DEVIATION_ANALYSIS_GATE` into `_build_steps()`, the `_get_all_step_ids()` function must also be updated -- otherwise the deviation-analysis step will never appear in HALT diagnostics.

**Severity**: MEDIUM -- an integration point the delta analysis missed. Should be listed as a P0 prerequisite alongside the `_build_steps()` change.

---

### MF-10 -- Preflight execution path bypasses phase-level gate evaluation entirely

**Finding**: `sprint/executor.py:491+` implements preflight execution for phases with `execution_mode in ("python", "skip")`. These phases produce `PhaseResult` with status `PREFLIGHT_PASS` but never enter the main poll loop where gate evaluation would occur (executor.py:574-787).

If audit gates are added to the main loop, preflight-executed phases will silently bypass them. The spec must decide whether preflight phases require audit gating or are exempt.

**Severity**: MEDIUM -- architectural gap. Preflight phases could contain STRICT-tier tasks that the spec assumes are audited.

---

## 5. Implementation Feasibility -- Phase Ordering Validation

### P0 Prerequisites

**Claim**: Remove `_apply_resume_after_spec_patch()` and wire `deviation-analysis` step.

**Assessment**: FEASIBLE with one hidden blocker.

- Removing the spec-patch function (executor.py:1193-1322) is straightforward deletion. However, `_apply_resume_after_spec_patch` is called from the main `roadmap_run` flow. The call site must be identified and cleaned up (not just the function definition).
- Wiring `deviation-analysis` into `_build_steps()` requires: (a) importing `DEVIATION_ANALYSIS_GATE` in executor.py, (b) adding a new `Step()` after spec-fidelity at line 439, (c) updating `_get_all_step_ids()` at line 502-518 (MF-9), (d) building a `build_deviation_analysis_prompt()` function.

**Hidden blocker**: The `deviation-analysis` step needs a prompt builder. No `build_deviation_analysis_prompt` function exists in `roadmap/prompts.py`. This is a non-trivial prerequisite -- the prompt must define what the subprocess does with spec-deviations.md. The delta analysis does not flag this as P0 work.

### P1 Prerequisites

**Claim**: Add audit workflow states, GateResult, AuditLease, profile enum to sprint/models.py.

**Assessment**: FEASIBLE, no hidden blockers. Pure data model additions. Namespace collision with `audit/evidence_gate.GateResult` must be resolved (MF-2).

### P2 Prerequisites

**Claim**: Wire SprintGatePolicy into execute_sprint(), extend OutputMonitor, integrate trailing gate.

**Assessment**: FEASIBLE but UNDERSTATED in scope due to MF-1.

The analysis assumes task-level granularity exists in the sprint mainline. It does not -- `execute_sprint()` operates at phase granularity. Wiring `SprintGatePolicy` into the mainline requires either:
(a) Activating `execute_phase_tasks()` within the mainline loop (major refactor), or
(b) Implementing audit gates at phase granularity only (scope reduction).

This is a hidden architectural decision that should be made before P2 begins.

### P3 Prerequisites

**Claim**: TUI integration, tasklist audit metadata, state persistence.

**Assessment**: FEASIBLE. These are additive changes with clear integration points.

---

## 6. Summary

| Category | Count |
|---|---|
| CONFIRMED | 9 |
| PARTIALLY_CONFIRMED | 2 |
| REFUTED | 0 |
| INSUFFICIENT_EVIDENCE | 0 |
| New findings (MISSED) | 10 |

### Confirmed findings (9)
Delta 2.1, 2.2, 2.3, 2.4, 2.5, 2.7, 2.8, 2.10, 2.11

### Partially confirmed findings (2)
- **Delta 2.6**: SprintGatePolicy is described as a "stub" -- it is actually implemented but unwired. KPI module already imports trailing gate types.
- **Delta 2.9**: The 120 s threshold is for display (stall_status property), not for the operational watchdog (which defaults to disabled). The analysis conflates the two.

### Severity reclassifications (2)
- **NR-7 (Sprint mainline vs helper)**: HIGH -> CRITICAL. `execute_phase_tasks()` is orphaned code, not merely an alternative path.
- **Delta 2.6 (Trailing gate unwired)**: MEDIUM -> HIGH. Complete infrastructure exists but has zero execution integration.

### New findings (10)
- **MF-1** (CRITICAL): `execute_phase_tasks()` is dead code -- no task-level execution granularity exists in the sprint mainline.
- **MF-2** (MEDIUM): `GateResult` class name collision between `audit/evidence_gate.py`, `audit/manifest_gate.py`, and the proposed `sprint/models.py` addition.
- **MF-3** (HIGH): `ShadowGateMetrics` and `--shadow-gates` flag are undiscovered rollout infrastructure directly relevant to spec SS7.
- **MF-4** (HIGH): `cli/audit/` subsystem (30+ modules) is a complete parallel audit infrastructure not mentioned in the analysis.
- **MF-5** (MEDIUM): `cleanup_audit/` is a third pipeline consumer of shared gate infrastructure, creating integration risk.
- **MF-6** (LOW): `sprint/kpi.py` already integrates trailing gate types for metrics reporting.
- **MF-7** (LOW): `GATE_DISPLAY_TRANSITIONS` is an existing state machine pattern to extend.
- **MF-8** (LOW): `grace_period` field exists but is never exposed via sprint CLI.
- **MF-9** (MEDIUM): `_get_all_step_ids()` omits `deviation-analysis`, must be updated alongside `_build_steps()`.
- **MF-10** (MEDIUM): Preflight execution path bypasses the phase-level loop entirely -- audit gate coverage for python/skip phases is undefined.

### Critical assessment

The delta analysis is thorough and accurate in its core findings. File paths and line ranges are correct within +/-5 lines in nearly all cases. No findings were refuted. The primary gaps are:

1. **Architectural**: The analysis assumes task-level execution granularity exists (it does not -- MF-1), which undermines the feasibility of task-scope audit gates at Phase 2.
2. **Coverage**: The `cli/audit/` and `cleanup_audit/` subsystems are completely absent from the analysis despite containing directly relevant infrastructure (gates, budgets, retries, evidence models).
3. **Shadow mode**: The existing `ShadowGateMetrics` infrastructure is a ready-made rollout vehicle that the spec's Phase 1 should leverage.
4. **P0 completeness**: Wiring `deviation-analysis` into `_build_steps()` requires a prompt builder that does not exist -- this is unaccounted-for P0 work.
