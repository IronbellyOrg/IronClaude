---
spec_source: "spec-refactor-plan-merged.md"
generated: "2026-03-18T00:00:00Z"
generator: "claude-opus-4-6-requirements-extractor"
functional_requirements: 47
nonfunctional_requirements: 18
total_requirements: 65
complexity_score: 0.92
complexity_class: HIGH
domains_detected: [backend, security, cli, testing, devops, observability]
risks_identified: 12
dependencies_identified: 14
success_criteria_count: 16
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 174.0, started_at: "2026-03-18T03:11:52.656480+00:00", finished_at: "2026-03-18T03:14:46.682266+00:00"}
---

## Functional Requirements

**FR-001** — Implement unified audit-gating at three scopes: task gate, milestone gate, and release gate, blocking completion/release transitions unless the corresponding gate passes.

**FR-002** — Implement Silent Success Detection (`SilentSuccessDetector`) as a mandatory post-execution hook inside `executor.run()` before `_emit_return_contract()`, detecting pipeline runs where no real work was performed despite `outcome: SUCCESS`.

**FR-003** — Implement Smoke Test Gate G-012 as a release-tier blocking gate that invokes the CLI against a minimal test fixture and validates real artifacts with substantive content are produced (Gate ID: G-012, tier: STRICT, scope: RELEASE).

**FR-004** — Implement Spec Fidelity Deterministic Checks D-03 and D-04 as two new semantic check functions in `SPEC_FIDELITY_GATE` that verify named dispatch tables and pseudocode dispatch function names are preserved from spec to roadmap.

**FR-005** — v1.2.1 implements milestone-scope (phase) and release-scope (sprint) gates only; task-scope gating is deferred to v1.3 with tasks evaluated within phase-scope gate runs using per-task output artifacts.

**FR-006** — Add locked decision #6 to SS2.1: v1.2.1 implements audit gates at phase-scope and sprint-scope only; task-scope deferred to v1.3.

**FR-007** — `SilentSuccessDetector` MUST treat a pipeline with zero non-EXEMPT, non-SKIPPED steps as a `policy` failure (not a pass) unless `--dry-run` was explicitly invoked and all steps are legitimately dry-run-excluded (C-1 resolution).

**FR-008** — Define 6 new canonical terms before Phase 1 GO: `AuditLease`, `audit_lease_timeout`, `max_turns`, `Critical Path Override`, `audit_gate_required`, `audit_attempts`.

**FR-009** — Annotate all task-scope transitions in SS4.1 with `[v1.3 -- deferred]` markers without deleting them; add a deferral block before the "Task scope" subsection.

**FR-010** — Implement lease model with heartbeat renewal for `audit_*_running` states: lease holds `lease_id`, `owner`, `acquired_at`, `expires_at`, `renewed_at` (all ISO-8601 UTC); heartbeat renewal at interval ≤ `audit_lease_timeout / 3`.

**FR-011** — Missing heartbeat renewal past `audit_lease_timeout` causes `audit_*_failed(timeout)` with per-scope configurable timeout values approved by Reliability Owner before Phase 2 GO.

**FR-012** — Implement per-scope retry attempt budget with durable `audit_attempts` counter; provisional defaults: milestone=2, release=1; normative only after calibration per SS8.2.

**FR-013** — Derive outer wall-clock ceiling from `max_turns` value: `max_turns * 120 + 300 s` for standard subprocesses; audit gate evaluation must complete within this ceiling.

**FR-014** — Extend `policy` failure class with three named sub-types: `policy.silent_success`, `policy.smoke_failure` (with sub-types `.timing`, `.artifact_absence`, `.content_evidence`), and `policy.fidelity_deterministic`.

**FR-015** — Route smoke test gate failures: API unavailability/network errors/HTTP 4xx-5xx → `transient` (retryable); timing/artifact/content evidence → `policy.smoke_failure.*` (not retryable).

**FR-016** — Replace SS5.2 item 4: completion/release transitions require the *current* gate result to reference the artifact version under evaluation; stale gate results trigger re-evaluation; override paths record staleness in `OverrideRecord`.

**FR-017** — Add SS5.2 rule 5: EXEMPT aggregate bypass prohibition — all-EXEMPT/SKIPPED evaluation produces `failed(policy.silent_success)` unless `--dry-run` was explicitly passed or pipeline has zero registered steps.

**FR-018** — Extend `GateResult` with `silent_success_audit` block (required when `SilentSuccessDetector` ran): `suspicion_score`, per-signal scores (S1-S3), `band`, `diagnostics`, `gate_decision`, `thresholds`. Block MUST be written even when `suspicion_score = 0.0`.

**FR-019** — Extend `GateResult` with `smoke_test_result` block (required when G-012 ran): `gate_id`, `fixture_path`, `elapsed_s`, `artifacts_found`, `checks_passed`, `checks_failed`, `failure_class`, `tmpdir_cleaned`.

**FR-020** — Extend `GateResult` with `fidelity_deterministic` block (required when D-03/D-04 ran): dispatch tables/functions found/preserved booleans, checks run/excluded lists.

**FR-021** — A fidelity report with `dispatch_tables_preserved: false` OR `dispatch_functions_preserved: false` MUST produce `gate failed` even when `high_severity_count: 0`; deterministic checks are not overridable by LLM output.

**FR-022** — Use disambiguated name `AuditGateResult` for v1.2.1 dataclass to avoid namespace collision with existing 2-field `GateResult` in `cli/audit/evidence_gate.py`.

**FR-023** — `AuditGateResult` `artifacts` block must include artifact version hashes (SHA-256 or equivalent) to support freshness validation per SS5.2 item 4.

**FR-024** — Implement `SilentSuccessDetector` signal suite: S1 (Artifact Content, weight 0.35), S2 (Execution Trace, weight 0.35), S3 (Output Freshness, weight 0.30) with composite formula `suspicion_score = ((1-S1) × 0.35) + ((1-S2) × 0.35) + ((1-S3) × 0.30)`.

**FR-025** — Implement suspicion score bands: 0.0-0.29 pass, 0.30-0.49 warn, 0.50-0.74 soft-fail, 0.75-1.00 hard-fail.

**FR-026** — Soft-fail (0.50-0.74) is overridable at task/milestone scope; hard-fail (≥0.75) is never overridable at release tier (LD-3 compliance).

**FR-027** — Implement G-012 smoke test check hierarchy: timing check (elapsed < 5s) as WARN only (non-blocking); intermediate artifact absence as ERROR (blocking); content evidence (fixture proper nouns) as ERROR (blocking).

**FR-028** — Implement `--mock-llm` mode for G-012 enabling CI integration without API access.

**FR-029** — Implement D-03 check: `_DISPATCH_TABLE_PATTERN` regex finds `UPPER_CASE_NAME = {` or `dict(` in spec; verify each found name appears in roadmap text.

**FR-030** — Implement D-04 check: `_STEP_DISPATCH_CALL` regex finds `_run_*()` or `step_result =` patterns in spec code fences; verify at least one found function name appears in roadmap.

**FR-031** — Fix Defect 1 (P0-A): `run_portify()` must pass `step_runner` to `PortifyExecutor`; create `STEP_DISPATCH` mapping from step IDs to imported step functions.

**FR-032** — Fix Defect 2 (P0-A): `commands.py` must call `validate_portify_config()` before `run_portify()`; exit non-zero on validation errors.

**FR-033** — Implement `silent_success.py` module (~300 lines): `FileSnapshot`, `StepTrace`, `SilentSuccessConfig`, `SilentSuccessDetector`, `SilentSuccessResult`, `SilentSuccessError` dataclasses and detector.

**FR-034** — Instrument executor with `_step_traces`, `time.monotonic()` wrapping of `_step_runner` calls, post-loop detector invocation, and `snapshot_pre_run()` call.

**FR-035** — Add `PortifyOutcome.SILENT_SUCCESS_SUSPECTED` and `PortifyOutcome.SUSPICIOUS_SUCCESS` enum values to models.

**FR-036** — Implement `fidelity_inventory.py` (~150 lines): `SpecInventory` dataclass, `build_spec_inventory()`, `_DISPATCH_TABLE_PATTERN`, `_STEP_DISPATCH_CALL`, `_DEP_ARROW_PATTERN` regexes.

**FR-037** — Implement `smoke_gate.py` (~400 lines): `SmokeTestConfig`, `SmokeTestResult` dataclasses; `run_smoke_test()`; timing/artifact/content check functions; `SMOKE_TEST_GATE: GateCriteria`; constants `SMOKE_NOOP_CEILING_S=5`, `SMOKE_MIN_REAL_EXECUTION_S=10`, `SMOKE_TIMEOUT_S=600`.

**FR-038** — Wire `SprintGatePolicy` into `execute_sprint()` at post-subprocess integration point (phase scope).

**FR-039** — Extend `OutputMonitor` for audit lease heartbeat events as a distinct event class.

**FR-040** — Wire `TrailingGateRunner` for phase-scope evaluation with `GateScope.MILESTONE` and `GateScope.RELEASE`.

**FR-041** — Wire `ShadowGateMetrics` for shadow mode data collection.

**FR-042** — Expose `--grace-period` CLI flag in sprint commands.

**FR-043** — Implement `audit_gate_required` per-task derivation: `true` when `Tier == STRICT OR Risk == High OR Critical Path Override == true`; phase-level aggregation: `phase_requires_audit = any(task.audit_gate_required for task in phase.tasks)`.

**FR-044** — Extend TUI phase table to display `AuditWorkflowState` values; add release guard blocking "Sprint Complete" unless `audit_release_passed`; add operator guidance panel for `audit_*_failed`.

**FR-045** — Add `audit` block to `_save_state()` for gate result persistence.

**FR-046** — Retire `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()` from roadmap executor (Phase 0).

**FR-047** — Wire `deviation-analysis` step into roadmap `_build_steps()` after `spec-fidelity`; update `_get_all_step_ids()`; write `build_deviation_analysis_prompt()`.

## Non-Functional Requirements

**NFR-001** — Audit lease timeout must be independent of and no greater than the outer subprocess wall-clock timeout for the same scope.

**NFR-002** — `SilentSuccessConfig(enabled=False)` must be available for test harnesses to disable detection.

**NFR-003** — Smoke test fixture stability: `sc-smoke-skill/SKILL.md` must retain component names `InputValidator`, `DataProcessor`, `OutputFormatter` as content evidence anchors.

**NFR-004** — Absence of `silent_success_audit` block in GateResult is itself a `failed` condition at STRICT tier (audit trail completeness).

**NFR-005** — All timeout/retry paths must terminate deterministically with no deadlocks (Phase 2 go/no-go).

**NFR-006** — Deterministic replay stability: same input must produce same gate result (Phase 1 go/no-go).

**NFR-007** — Fail-safe unknown handling: unknown/missing deterministic inputs produce `failed` (SS5.2 rule 2).

**NFR-008** — Smoke test warning band: elapsed > 300s (5 min); fail band: elapsed > 600s (hard timeout). Runs completing under 5s are failures, not acceptable fast results.

**NFR-009** — Silent success suspicion rate: warning > 5% of runs in warn range (0.30-0.49); fail > 1% of runs produce soft/hard-fail.

**NFR-010** — Rollout follows Shadow → Soft → Full promotion with KPI gate criteria at each transition.

**NFR-011** — Shadow → Soft promotion requires passing M1, M4, M5, M7, M9; Soft → Full requires M1-M12 for two consecutive windows plus rollback drill (M10).

**NFR-012** — M1 (runtime) must be recalibrated for phase-scope before shadow mode launch; original 8s task-scope threshold is not applicable.

**NFR-013** — S2 timing thresholds (50ms suspicious, 10ms near-certain no-op) are provisional; calibration methodology must be documented before soft-phase M14 activation.

**NFR-014** — D-03/D-04 should be gated behind a feature flag or made conditional if Anti-Instincts ships first (overlap with fingerprint and integration-contract modules).

**NFR-015** — `tmpdir_cleaned: bool` field in smoke test result for AC-006 compliance evidence (cleanup).

**NFR-016** — No source-file line citations in SS4.4 or SS10.2 (adversarial review consensus).

**NFR-017** — Audit gate KPI instrumentation: lease acquisition/duration feed M1; lease timeouts feed M7; OverrideRecord events feed M9 — all wired before shadow mode.

**NFR-018** — Provisional KPI defaults (M13, M14) become normative only after shadow-mode data collection and Reliability Owner approval.

## Complexity Assessment

**complexity_score**: 0.92
**complexity_class**: HIGH

**Rationale**:
- **Architectural breadth (0.95)**: Changes span 25+ files across 6 subsystems (sprint executor, cli-portify, roadmap, audit, tasklist, TUI) with deep cross-cutting concerns.
- **State machine complexity (0.90)**: Multi-scope audit workflow state machine with lease/heartbeat, retry budgets, timeout recovery, and deferral annotations for an entire scope tier.
- **Integration density (0.93)**: Three independently-deployable behavioral gate extensions must integrate with the core audit state machine in Phase 2, creating a two-wave delivery with cross-wave dependencies.
- **Governance overhead (0.88)**: 9 blockers, 9 required user decisions, 11 open decision rows, 5 owner roles, and a 4-phase rollout with go/no-go gates at each transition.
- **Contradiction resolution (0.85)**: 3 synthesized conflict resolutions, 2 locked decision tensions (C-1, C-2), and a branch decision constraining scope mid-spec.
- **Testing surface (0.90)**: 7+ new test files, regression tests against real v2.25 artifacts, smoke fixtures with stability contracts, and shadow/soft/full rollout behavioral tests.

## Architectural Constraints

1. **Single primary interface (LD-4)**: All audit gate commands flow through `/sc:audit-gate`. Developer utility subcommands (e.g., `cli-portify smoke-test`) are convenience wrappers, not audit gate commands.

2. **Override scope restriction (LD-3)**: Overrides allowed only at task/milestone scope, never at release scope. Hard-fail silent success (≥0.75) is never overridable at release tier.

3. **Configurable strictness/profile model (LD-1)**: Canonical model is `--profile` with values `strict | standard | legacy_migration`. `SilentSuccessConfig` is an additional configuration, not a profile replacement.

4. **Tier-1 gate required (LD-2)**: Even LIGHT/EXEMPT flows require Tier-1 gate; aggregate EXEMPT bypass is prohibited by C-1 rule.

5. **Explicit `audit_*` states (LD-5)**: All audit workflow states must use explicit `audit_*` state names; pre-integration phases (P0-B standalone emission) are acceptable but must integrate by Phase 2.

6. **Naming disambiguation**: v1.2.1 `GateResult` dataclass must be named `AuditGateResult` to avoid collision with existing 2-field `GateResult` in `cli/audit/evidence_gate.py`.

7. **Phase-scope only for v1.2.1**: No task-scope audit gate implementation; task-scope transitions retained with `[v1.3 -- deferred]` markers.

8. **Deterministic checks override LLM**: D-03/D-04 deterministic findings MUST produce gate failure even when LLM reports `high_severity_count: 0`.

9. **No source-file line citations**: SS4.4 and SS10.2 must contain zero source-file line number citations per adversarial review consensus.

10. **Behavioral gate extensions location**: New SS13 section consolidates all behavioral gate extension specifications; cross-references from other sections point here.

## Risk Inventory

1. **[HIGH] S2 calibration methodology gap** — Silent success timing thresholds (50ms/10ms) lack empirical derivation methodology. Mitigation: Blocker 7 requires Reliability Owner to document calibration protocol before soft-phase M14 activation.

2. **[HIGH] EXEMPT aggregate bypass** — All-EXEMPT step registries produce false pass with zero denominator. Mitigation: C-1 normative rule in SS5.2 rule 5 treats this as `policy` failure.

3. **[HIGH] P0-A defect fix scheduling** — G-012 smoke gate cannot pass legitimate runs until Defect 1 (step_runner) and Defect 2 (validation call) are fixed. Mitigation: Blocker 9 requires scheduling with owner/deadline before Phase 2.

4. **[HIGH] Compound delivery risk from orphaned code** — Task-scope `execute_phase_tasks()` is confirmed dead code (MF-1, unanimous adversarial review). Mitigation: Branch (b) defers to v1.3; no activation under delivery pressure.

5. **[MEDIUM] Smoke test CI false positives** — Timing check as BLOCKING creates systematic CI false positives from infrastructure overhead. Mitigation: Timing check is WARN only (non-blocking); artifact-absence is the primary blocking mechanism.

6. **[MEDIUM] Fixture drift** — Smoke fixture component name changes break content evidence checks. Mitigation: Stability contract in `smoke/README.md`; `test_fixture_content_matches_gate_patterns` unit test ships with gate.

7. **[MEDIUM] D-05 stub sentinel false positives** — Stub sentinel detection produces high false positives in TDD workflows. Mitigation: D-05 explicitly deferred until section-scope filtering is implemented.

8. **[MEDIUM] `--mock-llm` scope undefined** — G-012 cannot integrate into CI without mock mode specification. Mitigation: Blocker 8 and user decision 8 require scope definition before Phase 2 CI integration.

9. **[MEDIUM] `reimbursement_rate` dead field** — `TurnLedger` contains unused `reimbursement_rate = 0.8` field. Mitigation: Blocker 6 requires wire-or-remove decision before Phase 2 GO.

10. **[MEDIUM] Per-task artifact addressability uncertainty** — Phase subprocess output may not contain individually addressable per-task artifacts. Mitigation: C3 validation checkpoint is Phase 1 go/no-go condition; user decision 6 escalation path defined.

11. **[LOW] Anti-Instincts overlap with D-03/D-04** — Fingerprint and integration-contract modules materially overlap. Mitigation: Feature flag or conditional activation if Anti-Instincts ships first.

12. **[LOW] M1/M8 KPI threshold miscalibration** — 8s task-scope threshold not applicable to phase-scope. Mitigation: Recalibration from shadow mode data required before soft-phase promotion.

## Dependency Inventory

1. **Existing `GateResult` class** — `cli/audit/evidence_gate.py` (2-field class); must coexist with new `AuditGateResult`.

2. **`cli/audit/` subsystem** — Must be surveyed for reusable patterns and naming conflicts before Phase 1 model design.

3. **Sprint executor** (`cli/sprint/executor.py`) — Integration point for `SprintGatePolicy` at post-subprocess boundary.

4. **`OutputMonitor`** (`cli/sprint/monitor.py`) — Extended for audit lease heartbeat events.

5. **`TrailingGateRunner`** (`cli/pipeline/trailing_gate.py`) — Wired for phase-scope evaluation.

6. **`GateScope.MILESTONE` and `GateScope.RELEASE`** — Already defined; used by `TrailingGateRunner`.

7. **`GATE_REGISTRY`** (`cli_portify/gates.py`) — G-012 registered as `smoke-test` in existing G-000-G-011 sequence.

8. **`SPEC_FIDELITY_GATE`** (`roadmap/gates.py`) — Extended with D-03/D-04 check functions.

9. **`return-contract.yaml`** — Target for `SilentSuccessResult` standalone emission in Phase 1 (P0-B).

10. **v2.25 spec and roadmap artifacts** — `.dev/releases/complete/v2.25-cli-portify-cli/` used as regression test fixtures for D-03/D-04.

11. **`sc-audit-gate-protocol/SKILL.md`** — Deterministic evaluator and transition table definition target.

12. **`sc-tasklist-protocol/SKILL.md`** — `audit_gate_required` derivation and `schema_version` field.

13. **Tasklist generator** (`cli/tasklist/`) — Must parse and emit `audit_gate_required` in generated phase files.

14. **LLM API** — Required for non-mock smoke gate runs; unavailability routed as `transient` failure class.

## Success Criteria

1. **SC-001** — `test_no_op_pipeline_scores_1_0` passes: current broken executor (no step_runner) produces `suspicion_score = 1.0`, outcome `SILENT_SUCCESS_SUSPECTED`, `return-contract.yaml` includes `silent_success_audit` block, CLI exits non-zero.

2. **SC-002** — `test_run_deterministic_inventory_cli_portify_case` passes: v2.25 spec/roadmap pair produces `dispatch_tables_preserved: false` and `dispatch_functions_preserved: false`; gate rejects roadmap even with `high_severity_count: 0`.

3. **SC-003** — P0-A Fix 1 verified: `run_portify()` with test fixture produces at least one intermediate artifact beyond `return-contract.yaml`.

4. **SC-004** — P0-A Fix 2 verified: `commands.py` exits non-zero when `validate_portify_config()` returns errors.

5. **SC-005** — G-012 against known-bad executor: fails with `policy.smoke_failure.timing` AND `policy.smoke_failure.artifact_absence`.

6. **SC-006** — G-012 after P0-A fixes: real run against smoke fixture passes all checks.

7. **SC-007** — S2 calibration protocol documented and approved by Reliability Owner before soft-phase M14 activation.

8. **SC-008** — `SilentSuccessResult` appears in unified audit trail with `failure_class: policy.silent_success`; override at release scope blocked; task/milestone override requires valid `OverrideRecord`.

9. **SC-009** — All-EXEMPT step registry (without `--dry-run`) produces `failed(policy.silent_success)`, not pass.

10. **SC-010** — Deterministic replay stability: same input produces same gate result (Phase 1).

11. **SC-011** — Timeout/retry paths terminate deterministically with no deadlocks (Phase 2).

12. **SC-012** — Roadmap pipeline produces validated `deviation-analysis.md` artifact (Phase 1).

13. **SC-013** — Per-task output artifacts individually addressable within phase subprocess output (C3 validation, Phase 1 go/no-go).

14. **SC-014** — Transition blocking/override rules enforced per scope for milestone + release (Phase 3).

15. **SC-015** — Phase gates pass by KPI criteria and rollback drill success (Phase 4).

16. **SC-016** — All 9 blockers (SS12.3) closed with owner/deadline before their respective phase go/no-go gates.

## Open Questions

1. **Owner assignments**: Blockers 5, 6, 7, 8, 9 and multiple open decision rows have `[TBD]` owners and deadlines. Who are the Reliability Owner, Policy Owner, Tasklist Owner, and Program Manager for this release?

2. **`audit_lease_timeout` default values**: What are the per-scope default values for milestone and release lease timeouts? The spec mandates Reliability Owner approval but provides no provisional values.

3. **`reimbursement_rate` disposition**: Should the dead `reimbursement_rate = 0.8` field in `TurnLedger` be wired as a turn-recovery credit for audit retry paths, or removed entirely?

4. **Per-task artifact addressability (C3)**: Can phase subprocess output currently provide individually addressable per-task artifacts? If not, is option (a) restructuring or option (b) coarser granularity preferred?

5. **`--mock-llm` check matrix**: Exactly which G-012 checks remain active vs. skipped in mock mode? The spec suggests timing stays active and content evidence may be relaxed — what about artifact-absence checks?

6. **D-03/D-04 regex generality**: Are the `_DISPATCH_TABLE_PATTERN` (`UPPER_CASE_NAME = {` or `dict(`) and `_STEP_DISPATCH_CALL` (`_run_*()` or `step_result =`) patterns sufficiently general for all spec authoring conventions in this project?

7. **Anti-Instincts timeline**: When is Anti-Instincts expected to ship relative to D-03/D-04 deployment? This determines whether a feature flag is needed.

8. **Shadow mode data collection duration**: How long must shadow mode run before M13/M14 provisional metrics can be calibrated to normative status? No minimum observation window is specified.

9. **M1 phase-scope threshold**: What is the recalibrated M1 runtime threshold for phase-scope evaluations? The original 8s is explicitly invalidated but no provisional replacement is given.

10. **Audit gate sub-process time budget**: What fraction of the outer wall-clock ceiling (`max_turns * 120 + 300 s`) is allocated to audit gate evaluation? SS4.4 item 6 requires Reliability Owner specification but provides no provisional value.

11. **`SilentSuccessConfig` defaults maintenance**: Who owns ongoing maintenance of `SilentSuccessConfig` default values after initial calibration? The spec identifies this as a required decision but assigns no owner.

12. **Branch (b) reversal conditions**: If C3 validation fails (per-task artifacts not addressable), what is the escalation timeline and decision authority beyond "escalate to program manager"?
