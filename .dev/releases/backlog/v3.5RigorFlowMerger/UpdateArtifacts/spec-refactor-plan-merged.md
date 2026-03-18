# Merged Spec Refactoring Plan — Unified Audit Gating 

**Date**: 2026-03-17
**Target document**: `unified-audit-gating-release-spec.md`
**Plan type**: Document refactoring plan only — no files modified here
**Status**: PLAN ONLY — do not edit spec until this plan is approved

**Source authority (Plan A)**: Proposals P05, P04, P02 (D-03/D-04) + their adversarial debate transcripts
**Source authority (Plan B)**: Branch decision (B), Adversarial delta review (A), Delta analysis (D)

---

## Merge Summary

- **Total changes in Plan A**: 16 (SS1.1, SS1.3, SS2.2, SS2.3, SS5.1, SS5.2, SS6.1, SS8.3, SS10.1, SS10.2, SS10.3, SS11, SS12.3, SS12.4, New SS13, Top 5 Actions)
- **Total changes in Plan B**: 21 (R1-R21)
- **Unique to A**: 6 (SS1.3, SS2.2, SS5.1, SS8.3, New SS13, Implementation Order Summary)
- **Unique to B**: 11 (R2/SS2.1, R4/SS3.1, R5/SS4.1, R6/SS4.4, R8/SS6.1-impl-notes, R9/SS7.2, R10/SS8.5, R11/SS9.2, R12/SS9.3, R20/Top 5 Deferred, R21/Open Decisions)
- **Compatible overlaps merged**: 8 (SS1.1, SS2.3, SS5.2, SS6.1, SS10.3, SS11, SS12.4, Top 5 Immediate)
- **Conflicting overlaps resolved by debate**: 3 (SS10.1, SS10.2, SS12.3)
- **Synthesized resolutions**: 3

**Merge classification legend**:
- `UNIQUE-A` = Change exists only in Plan A; included verbatim
- `UNIQUE-B` = Change exists only in Plan B; included verbatim
- `A+B-merged` = Both plans modify the same section with compatible, non-conflicting additions; both included
- `synthesized` = Both plans modify the same section with conflicting content; resolved by adversarial debate

---

## Contradiction Check Against SS2.1 Locked Decisions

[Source: A]

Before section-by-section changes, all three Plan A improvements (P05, P04, P02) are checked against the five locked decisions. **No contradiction proceeds silently.**

| Locked Decision | P05 | P04 | P02 (D-03/D-04) | Verdict |
|----------------|-----|-----|-----------------|---------|
| LD-1: Configurable strictness/profile behavior | No conflict -- `SilentSuccessConfig` is an additional config, not a profile replacement | No conflict | No conflict | CLEAR |
| LD-2: Tier-1 gate required even for LIGHT/EXEMPT flows | TENSION: P05 proposes EXEMPT-tier exemptions for individual steps. If all steps are EXEMPT, the detector's denominator is zero and it passes trivially. | No conflict -- G-012 is a STRICT/RELEASE gate, not a replacement for Tier-1 | No conflict | **RESOLVE BELOW (C-1)** |
| LD-3: Overrides allowed only task/milestone, never release | P05 SS4.2: hard-fail at release scope has no override -- compliant. Soft-fail follows governance. | P04: no override path at release tier -- compliant | No conflict | CLEAR |
| LD-4: Single primary command interface (`/sc:audit-gate`) | P04 proposes a `superclaude cli-portify smoke-test` standalone command -- potential interface proliferation | Same | No conflict | **RESOLVE BELOW (C-2)** |
| LD-5: Explicit `audit_*` states are required | P05 integrates as a `GateResult` in Phase 2 -- compliant when wired. Phase 1 (executor hook only) precedes `audit_*` state integration -- not a violation, just pre-integration. | P04 occupies `audit_release_running` state -- compliant | No conflict | CLEAR |

### C-1 Resolution: EXEMPT Step Denominator Edge Case

**Problem**: If a pipeline's `STEP_REGISTRY` marks all steps as EXEMPT, `SilentSuccessDetector`
evaluates against a zero denominator and produces `suspicion_score = 0` (false pass).

**Resolution for spec**: Add to SS5.2 (pass/fail rules) a new normative invariant:
> "SilentSuccessDetector MUST treat a pipeline with zero non-EXEMPT, non-SKIPPED steps as a
> `policy` failure -- not a pass -- unless `--dry-run` was explicitly invoked and all steps are
> legitimately dry-run-excluded."

This closes the gap without modifying LD-2. EXEMPT classification still applies per-step; the
system-level guard prevents EXEMPT from being used to bypass detection at aggregate level.

### C-2 Resolution: Interface Proliferation

**Problem**: P04's `superclaude cli-portify smoke-test` is a new top-level command that conflicts
with LD-4's single primary interface.

**Resolution for spec**: The standalone `smoke-test` subcommand is scoped under `cli-portify`, not
under the audit gate namespace -- it is a developer utility, not an audit gate command. Spec SS2.2
(non-goals) should note:
> "Developer utility subcommands (`cli-portify smoke-test`) are not audit gate commands and do not
> replace or extend `/sc:audit-gate`."

The release-tier gate invocation still flows through the sprint executor's `audit_release_running`
state, which calls the smoke gate internally. The standalone command is a convenience wrapper.

---

## Section-by-Section Changes

Changes are presented in dependency order (see Dependency Order section at end of document).

---

### SS1.1 -- Scope

[Source: A+B-merged]

**Current text** (excerpt):
> Implement a unified audit-gating capability that blocks completion/release transitions unless
> the corresponding gate passes at three scopes:
> 1. Task gate
> 2. Milestone gate
> 3. Release gate

**Change type**: EXTEND (two independent additions)

**Proposed addition from Plan A** (append after the three-scope list):

> Additionally, this release incorporates three validated behavioral gate extensions from the
> forensic analysis of the cli-portify no-op incident (2026-03-17):
>
> 4. **Silent Success Detection** -- A mandatory post-execution hook (`SilentSuccessDetector`)
>    that runs inside `executor.run()` before `_emit_return_contract()`, detecting pipeline
>    runs where no real work was performed despite `outcome: SUCCESS` being reported.
>
> 5. **Smoke Test Gate (G-012)** -- A release-tier blocking gate that invokes the CLI against a
>    minimal test fixture and validates that real artifacts with substantive content are produced.
>    Gate ID: G-012, enforcement tier: STRICT, scope: RELEASE.
>
> 6. **Spec Fidelity Deterministic Checks (D-03, D-04)** -- Two new semantic check functions
>    added to `SPEC_FIDELITY_GATE` that deterministically verify named dispatch tables and
>    pseudocode dispatch function names are preserved from spec to roadmap. These supplement
>    (do not replace) the existing LLM-generated fidelity report.

**Proposed addition from Plan B** (append after Plan A additions):

> **v1.2.1 Scope Amendment (Branch (b), locked 2026-03-17)**: v1.2.1 implements milestone-scope (phase) and release-scope (sprint) gates only. The "Task gate" listed in item 1 above is satisfied via phase-scope gating: tasks are evaluated within phase-scope gate runs using per-task output artifacts. True task-scope gating (independent per-task state machine) is deferred to v1.3, contingent on independent validation and mainline promotion of the task-scope execution model. See SS4.1 and SS2.1 locked decision #6.

**Rationale**: Plan A adds three behavioral gate extensions to scope. Plan B adds the branch (b) scope amendment constraining task-scope gating. Both additions are independent and additive.

**Dependencies**: None -- this is a scope declaration.

---

### SS1.3 -- Out-of-Scope for v1.2.1

[Source: UNIQUE-A]

**Current text** (excerpt):
> - New non-gating product features unrelated to transition control
> - Security hardening expansions not required for correctness of gate transitions
> - Full auto-tuning of profiles during rollout (deferred)

**Change type**: ADD

**Proposed addition** (append to the out-of-scope list):

> - **Developer utility subcommands** (`superclaude cli-portify smoke-test`) -- these are
>   convenience wrappers over release-tier gate logic, not audit gate commands. They do not
>   extend or replace `/sc:audit-gate` and are not subject to the single-interface constraint
>   of LD-4.
> - **D-01 (FR-NNN identifier coverage)** and **D-05 (stub sentinel detection)** from the
>   spec fidelity hardening proposal -- D-01 is non-load-bearing for specs using prose/pseudocode
>   rather than formal identifier notation; D-05 requires section-scope filtering before it is
>   safe to ship (high false positive risk in TDD workflows). Both are deferred post release.

**Rationale**: C-2 resolution requires an explicit scope boundary for the standalone command.
Explicit exclusion of D-01 and D-05 from scope prevents scope creep during implementation.

**Dependencies**: None.

---

### SS2.1 -- Locked Decisions

[Source: UNIQUE-B (R2)]

**Current list ends at item 5**. Add:

> 6. v1.2.1 implements audit gates at phase-scope (milestone) and sprint-scope (release) only. Task-scope audit gates are deferred to v1.3. Phase-scope gates evaluate per-task output artifacts within each phase. (Branch (b) decision, 2026-03-17; see SS4.1 deferral annotation.)

**Rationale**: Branch decision C7.

**Dependencies**: None -- locked decisions are foundational.

---

### SS2.2 -- Non-Goals

[Source: UNIQUE-A]

**Current text**:
> - Release-level override capability
> - LLM/agent heuristics as source of truth for pass/fail

**Change type**: ADD

**Proposed addition** (append to non-goals):

> - **EXEMPT-tier classification as aggregate bypass** -- individual steps may be classified as
>   EXEMPT (excluded from SilentSuccessDetector signal denominators) per SS5.2 normative rule
>   C-1, but a pipeline where all steps are EXEMPT does not thereby achieve a pass; it produces
>   a `policy` failure unless `--dry-run` was explicitly invoked.
> - **Smoke test as bug fix substitute** -- G-012 is a regression guard, not a replacement for
>   the wiring fix (Defect 1: `run_portify()` missing `step_runner`) or the validation fix
>   (Defect 2: `validate_portify_config()` not called). Both fixes are prerequisites for G-012
>   to pass a legitimate run.

**Rationale**: C-1 resolution; P04 Appendix B explicitly requires this distinction.

**Dependencies**: SS5.2 addition (C-1 rule must be consistent with this non-goal).

---

### SS2.3 -- Contradictions and Winning Decisions

[Source: A+B-merged]

**Current text** (table excerpt):
> | Contradiction | Evidence | Winner in v1.2.1 | Rationale |
> |---|---|---|---|
> | `--strictness standard|strict` vs profile set... | ... | Canonical model is `--profile`... | ... |
> | ... | ... | ... | ... |

**Change type**: ADD (append 4 new rows total: 2 from Plan A, 2 from Plan B)

**Proposed additions from Plan A** (append to contradictions table):

> | EXEMPT step denominator vs. Tier-1 gate requirement | `SilentSuccessDetector` EXEMPT classification (P05 SS3.1) vs. LD-2 (Tier-1 gate required even for LIGHT/EXEMPT flows) | **C-1 resolution**: individual step EXEMPT exemptions are permitted; aggregate pipeline EXEMPT bypass is forbidden. A pipeline with zero non-EXEMPT, non-SKIPPED steps fails with `policy` failure class unless `--dry-run` was explicitly invoked. | Ensures EXEMPT classification cannot be used as an aggregate bypass of behavioral detection (SS5.2 normative rule) |
> | Standalone `cli-portify smoke-test` command vs. single primary interface (LD-4) | P04 SS6.3 proposes `superclaude cli-portify smoke-test` as standalone CLI; LD-4 mandates single primary interface `/sc:audit-gate` | **C-2 resolution**: `smoke-test` is scoped as a `cli-portify` utility subcommand, not an audit gate command. Release-tier gate invocation remains through sprint executor's `audit_release_running` state. | Preserves LD-4 intent; the utility command wraps gate logic rather than replacing the interface |

**Proposed additions from Plan B** (append to contradictions table):

> | Spec SS4.1 has 12 task-scope transitions vs. sprint executor never runs at task granularity | Adversarial delta review MF-1 (CRITICAL, unanimous); `sprint/executor.py:350` zero call sites in mainline | Phase-scope gating for v1.2.1; task-scope deferred to v1.3 | Activating orphaned dead code under delivery pressure is an unacceptable compound risk. Branch (b) locked. |
> | KPI M1 defined as "Task scope, <=8s" vs no task-scope evaluations under branch (b) | Branch decision C4; `metrics-and-gates.md` KPI table | Redefine M1 as phase-scope runtime for v1.2.1 with recalibrated threshold during shadow mode | The 8s threshold was calibrated for per-task evaluations; phase-scope evaluations have different timing profiles |

**Rationale**: Plan A adds C-1 and C-2 contradiction resolutions. Plan B adds branch (b) scope and M1 recalibration contradictions. All four rows are independent.

**Dependencies**: SS2.2 non-goal additions; SS5.2 normative rule; Branch decision C4.

---

### SS3.1 -- Canonical Terms

[Source: UNIQUE-B (R4)]

**Current text** (excerpt):
> - **Scope**: `task | milestone | release`
> - **Tier**: `Tier-1(task), Tier-2(milestone), Tier-3(release)`
> - **Profile**: `strict | standard | legacy_migration`
> - **Gate status**: `passed | failed`
> - **Failure class**: `policy | transient | system | timeout | unknown`

**Change type**: ADD (append after existing terms)

**Proposed addition**:

> **New terms added for v1.2.1 implementation (to be defined before Phase 1 GO)**:
> - **AuditLease**: A timed lock held by the audit gate evaluator while `audit_*_running`. Required fields: `lease_id` (unique identifier), `owner` (evaluator process/agent identity), `acquired_at` (ISO-8601 UTC), `expires_at` (ISO-8601 UTC), `renewed_at` (ISO-8601 UTC).
> - **audit_lease_timeout**: Per-scope configurable duration after which a missing heartbeat triggers `audit_*_failed(timeout)`. Must be independent of and no greater than the outer subprocess wall-clock timeout. Default values subject to Reliability Owner approval before Phase 2 GO.
> - **max_turns**: The sprint/roadmap runner configuration value for subprocess turn limit. Determines outer wall-clock timeout ceiling: `max_turns * 120 + 300 s` for standard subprocesses. Default: 100.
> - **Critical Path Override**: A tasklist task field (boolean). When `true`, the task is on the critical path and `audit_gate_required` defaults to `true` regardless of Tier or Risk.
> - **audit_gate_required**: A boolean field emitted per task in tasklist metadata. Derivation rule: `true` when `Tier == STRICT OR Risk == High OR Critical Path Override == true`. At phase scope, aggregated as `phase_requires_audit = any(task.audit_gate_required for task in phase.tasks)`.
> - **audit_attempts**: Per-entity retry counter, persisted in durable state, incremented on each retry attempt. Bounded by `max_attempts` per scope.

**Rationale**: Adversarial review A, Section 6.1 (6 undefined terms); Branch decision C2.

**Dependencies**: None -- terms must be defined before other sections reference them.

---

### SS4.1 -- Legal Transitions

[Source: UNIQUE-B (R5)]

**Current text** has three subsections: Task scope, Milestone scope, Release scope.

**Change type**: ANNOTATE (add deferral markers, do not delete)

**Required change**: Add a deferral block immediately before the "Task scope" subsection, and add `[v1.3 -- deferred]` markers to each task-scope transition line.

**New block before "Task scope"**:
> **Branch (b) deferral**: Task-scope audit gate transitions below are retained for v1.3 reference. They are NOT implemented in v1.2.1. The v1.2.1 implementation covers Milestone scope and Release scope. Marker: `[v1.3 -- deferred]`.

**Annotated task-scope transitions** (add marker suffix to each line):
```
- `in_progress -> ready_for_audit_task`  [v1.3 -- deferred]
- `ready_for_audit_task -> audit_task_running`  [v1.3 -- deferred]
- `audit_task_running -> audit_task_passed | audit_task_failed`  [v1.3 -- deferred]
- `audit_task_passed -> completed`  [v1.3 -- deferred]
- `audit_task_failed -> ready_for_audit_task` (retry path)  [v1.3 -- deferred]
- `audit_task_failed -> completed` only with approved task override  [v1.3 -- deferred]
```

**Rationale**: Branch decision C1.

**Dependencies**: SS2.1 locked decision #6 (must exist before this annotation references it).

---

### SS4.4 -- Timeout/Retry/Recovery Semantics

[Source: UNIQUE-B (R6)]

**Current text** (5 items, terse, all TBD values):
> 1. `audit_*_running` uses lease + heartbeat.
> 2. Missing heartbeat past timeout causes `audit_*_failed(timeout)`.
> 3. Retry is bounded by per-scope attempt budget.
> 4. Retry exhaustion remains failed and blocks completion/release.
> 5. Requeue allowed only while budget remains.

**Change type**: REPLACE (major rewrite)

**Replace the entire SS4.4 body with**:

> 1. `audit_*_running` uses a lease model with heartbeat renewal. The lease must hold: `lease_id` (unique identifier), `owner` (evaluator identity), `acquired_at`, `expires_at`, and `renewed_at` (all ISO-8601 UTC). The audit gate evaluator must emit a heartbeat renewal event at an interval no greater than `audit_lease_timeout / 3`. The lease mechanism builds on the subprocess stall-detection pattern already present in the sprint executor's output monitoring infrastructure.
>
> 2. Missing heartbeat renewal past `audit_lease_timeout` causes `audit_*_failed(timeout)`. `audit_lease_timeout` is a per-scope configurable value; default values must be approved by the Reliability Owner (SS9.2) before Phase 2 GO. The `audit_lease_timeout` must be independent of and no greater than the outer subprocess wall-clock timeout for the same scope.
>
> 3. Retry is bounded by a per-scope attempt budget. The attempt count for each audited entity (`audit_attempts`) must be persisted in durable state and incremented on each retry. `max_attempts` is configured per scope (milestone and release for v1.2.1). Default values for `max_attempts` are **provisional during shadow mode** and become normative only after calibration per SS8.2. Provisional defaults: milestone=2, release=1. These values must be reviewed and approved by the Reliability Owner before Phase 2 GO.
>
> 4. Retry exhaustion remains failed and blocks completion/release.
>
> 5. Requeue allowed only while budget remains.
>
> 6. The outer wall-clock ceiling for any sprint phase execution is derived from the configured `max_turns` value (see SS3.1 canonical terms). Audit gate evaluation must complete within this ceiling. The Reliability Owner must specify the audit gate sub-process time budget as a fraction of the outer ceiling before Phase 2 GO. This value must be documented as a locked decision per SS9.3.

**Notes**:
- `task=3` default removed because task-scope is deferred (branch b). Only milestone=2 and release=1 remain.
- All source-file line references removed per adversarial review consensus.
- Item 7 (reimbursement_rate) moved to SS12.3 blocker list (see R17 in SS12.3 below).

**Rationale**: Adversarial review A Section 7; Delta analysis D SS4.4 replacement; Branch decision C5; adversarial review consensus on line citations.

**Dependencies**: SS3.1 canonical terms (references AuditLease, audit_lease_timeout, max_turns, audit_attempts).

---

### SS5.1 -- Failure Classes

[Source: UNIQUE-A]

**Current text**:
> - `policy`: rule/threshold violation
> - `transient`: recoverable execution issue
> - `system`: non-recoverable runner/system error
> - `timeout`: stale/expired running state
> - `unknown`: unmapped condition (fail-safe)

**Change type**: EXTEND

**Proposed addition** (append sub-classifications to `policy`):

> The `policy` failure class has three named sub-types for behavioral gate failures:
>
> - `policy.silent_success` -- `SilentSuccessDetector` composite suspicion score >= soft-fail
>   threshold (0.50). Signals that the pipeline completed with `outcome: SUCCESS` but produced
>   no observable evidence of real work (no artifacts, near-zero timing, no fresh output files).
>
> - `policy.smoke_failure` -- G-012 smoke gate blocked the release. Sub-types:
>   - `policy.smoke_failure.timing` -- execution completed under `SMOKE_NOOP_CEILING_S` (5s)
>   - `policy.smoke_failure.artifact_absence` -- fewer than minimum intermediate artifacts present
>   - `policy.smoke_failure.content_evidence` -- artifact lacks fixture-specific content anchors
>
> - `policy.fidelity_deterministic` -- `SPEC_FIDELITY_GATE` blocked by a deterministic check
>   (D-03 or D-04) independent of the LLM-generated severity counts.
>
> For the smoke test gate specifically, `transient` is used (not `policy`) when the gate cannot
> complete due to API unavailability, network failure, or HTTP 4xx/5xx from the LLM API. This
> enables retry without constituting a release block.

**Rationale**: P05 SS4.2, P04 SS5.2 and AC-005, P02 debate synthesis. Sub-type taxonomy enables
precise incident triage.

**Dependencies**: SS6.1 GateResult extension (the `failure_class` field carries these sub-types).

---

### SS5.2 -- Pass/Fail Rules

[Source: A+B-merged]

**Current text**:
> 1. Any blocking check failure => gate `failed`.
> 2. Unknown/missing deterministic inputs => `failed`.
> 3. Missing evidence for failed check => `failed` and non-completable.
> 4. Completion/release transitions require latest gate `passed` except approved task/milestone
>    override path.

**Change type**: MODIFY item 4 (Plan B) + ADD rule 5 (Plan A)

**Proposed replacement of item 4 from Plan B**:

> 4. Completion/release transitions require the *current* gate result to reference the artifact version under evaluation. A gate result is considered stale and non-satisfying if the artifacts it audited have changed since the gate ran. Stale gate results must trigger re-evaluation. Approved task/milestone override paths are exempt from re-evaluation but must record the staleness in the `OverrideRecord`.

**Proposed addition of item 5 from Plan A**:

> 5. **EXEMPT aggregate bypass prohibition (C-1 normative rule)**: A `SilentSuccessDetector`
>    evaluation where all evaluated steps have been classified as EXEMPT or SKIPPED produces a
>    `failed(policy.silent_success)` result -- not a pass -- unless:
>    (a) `--dry-run` was explicitly passed to the CLI invocation, OR
>    (b) the pipeline has zero registered steps (empty `STEP_REGISTRY`).
>    This rule prevents EXEMPT classification from being used as an aggregate gate bypass.
>    Individual step EXEMPT classification remains valid per-step for signal denominator exclusion.

**Rationale**: Plan B clarifies "latest" ambiguity in item 4 (NR-5/NR-6 consolidated finding). Plan A adds C-1 enforcement rule. Both changes are compatible.

**Dependencies**: SS2.2 non-goal and SS2.3 contradiction row (must be consistent).

---

### SS6.1 -- GateResult

[Source: A+B-merged]

**Current text** (required fields list):
> Required fields:
> - `version`
> - `gate_run_id`
> - `scope`, `entity_id`, `profile`
> - `status`, `score`, `threshold`
> - `checks[]` (includes severity + evidence)
> - `drift_summary` (`edited`, `non_edited`)
> - `override` block
> - `timing` block
> - `artifacts` block
> - `failure_class` (v1.2 addition)

**Change type**: EXTEND (Plan A behavioral gate blocks) + ADD (Plan B implementation notes)

**Proposed addition from Plan A** (append after the required fields list):

> #### v1.2.1 Behavioral Gate Extensions to GateResult
>
> **Silent success audit block** (required when `SilentSuccessDetector` ran):
> ```yaml
> silent_success_audit:
>   suspicion_score: float          # 0.0-1.0; higher = more suspicious
>   s1_artifact_coverage: float     # S1 score (before inversion)
>   s2_execution_activity: float    # S2 score (before inversion)
>   s3_output_freshness: float      # S3 score (before inversion)
>   band: pass|warn|soft_fail|hard_fail
>   diagnostics: list[str]          # per-signal failure messages with evidence
>   gate_decision: str              # PASS | SUSPICIOUS_SUCCESS | SILENT_SUCCESS_SUSPECTED
>   thresholds:                     # all thresholds that were applied (no magic numbers)
>     soft_fail: float
>     hard_fail: float
>     s2_suspicious_ms: float
>     s2_noop_ms: float
> ```
> This block MUST be written even when `suspicion_score = 0.0` (pass case), so that audit trails
> can confirm the detector ran and found no issues. Absence of the block is itself a `failed`
> condition at STRICT tier.
>
> **Smoke test result block** (required when G-012 ran):
> ```yaml
> smoke_test_result:
>   gate_id: G-012
>   fixture_path: str
>   elapsed_s: float
>   artifacts_found: list[str]      # relative paths of artifacts discovered
>   checks_passed: list[str]
>   checks_failed: list[GateFailure]
>   failure_class: transient|policy.smoke_failure.timing|policy.smoke_failure.artifact_absence|policy.smoke_failure.content_evidence
>   tmpdir_cleaned: bool            # AC-006 compliance evidence
> ```
>
> **Fidelity deterministic check block** (required when D-03/D-04 ran):
> ```yaml
> fidelity_deterministic:
>   dispatch_tables_found: list[str]     # named constants matching _DISPATCH_TABLE_PATTERN
>   dispatch_tables_preserved: bool      # false => gate blocked regardless of LLM severity counts
>   dispatch_functions_found: list[str]  # function name patterns matching _STEP_DISPATCH_CALL
>   dispatch_functions_preserved: bool   # false => gate blocked regardless of LLM severity counts
>   checks_run: [D-03, D-04]
>   checks_excluded: [D-01, D-05]        # explicitly deferred per SS1.3
> ```
> **Critical invariant**: A fidelity report with `dispatch_tables_preserved: false` OR
> `dispatch_functions_preserved: false` MUST produce `gate failed` even when the LLM report
> has `high_severity_count: 0`. The deterministic checks are not overridable by LLM output.

**Proposed addition from Plan B** (append after Plan A additions):

> **Implementation notes for v1.2.1**:
> - The sprint codebase contains a pre-existing `GateResult` class in `cli/audit/evidence_gate.py` (2 fields: `passed`, `reason`). The v1.2.1 `GateResult` dataclass implementing this spec must use the disambiguated name `AuditGateResult` to avoid namespace collision. The existing 2-field class must not be renamed; both coexist.
> - `AuditGateResult` is a new dataclass to be added to `src/superclaude/cli/sprint/models.py`, separate from `GateDisplayState` (which remains for TUI rendering only).
> - The `artifacts` block must include artifact version hashes (SHA-256 or equivalent) to support the freshness validation required by SS5.2 item 4.

**Rationale**: Plan A extends GateResult with three behavioral gate blocks. Plan B adds implementation notes for naming disambiguation and artifact hashing. Both are additive and compatible.

**Dependencies**: SS5.1 failure class taxonomy (sub-types referenced here must be defined there); SS3.1 AuditGateResult naming.

---

### SS7.2 -- Promotion Criteria

[Source: UNIQUE-B (R9)]

**Current text**:
> - Shadow -> Soft: pass M1, M4, M5, M7, M9
> - Soft -> Full: pass M1-M12 for two consecutive windows + pass rollback drill (M10)

**Change type**: ADD (append annotation)

**Proposed addition** (append after the promotion criteria):

> **v1.2.1 branch (b) KPI adjustments**: M1 (Tier-1 runtime, originally defined as task-scope <=8s) and M8 (false-block rate, Tier-1) are not applicable at task scope under v1.2.1. Before shadow mode launches:
> - **M1**: Redefine as phase-scope runtime for v1.2.1 with recalibrated threshold. The 8s threshold was calibrated for per-task evaluations; phase-scope will require a longer threshold. Calibrate from shadow mode data before soft-phase promotion.
> - **M8**: Apply at Tier-2 (phase scope) only. Consider tightening the false-block threshold during calibration to account for larger blast radius of phase-scope gates vs task-scope gates.
>
> These recalibrations are Phase 1 deliverables, required before shadow mode produces promotion-decision data.
>
> **Consumer note**: The Wiring Verification Gate should consume this rollout framework rather than defining independent thresholds. Ensure the profile system (`strict | standard | legacy_migration`) can accommodate Wiring Verification gate parameters.

**Rationale**: Branch decision C4.

**Dependencies**: None.

---

### SS8.3 -- KPI/SLO: Warning/Fail Bands

[Source: UNIQUE-A]

**Current text**:
> - Runtime bands M1-M3 as defined in KPI table
> - Determinism floor M4 strict by tier
> - Evidence completeness M5 has no warning band (any miss is fail)

**Change type**: ADD

**Proposed addition** (append as new bullets):

> - **Smoke test gate duration M13** (provisional in shadow mode):
>   - Warning band: elapsed > 300s (5 minutes) for a minimal fixture run
>   - Fail band: elapsed > 600s (`SMOKE_TIMEOUT_S` ceiling; hard timeout)
>   - Note: the SMOKE_NOOP_CEILING_S (5s) is a *minimum* threshold, not a KPI target -- runs
>     completing under 5s are failures, not acceptable fast results.
>   - Calibration owner: Reliability Owner (SS9.2) must establish baseline from shadow-mode smoke
>     runs before M13 is normative.
>
> - **Silent success suspicion rate M14** (provisional):
>   - Warning band: > 5% of production runs produce `suspicion_score` in warn range (0.30-0.49)
>   - Fail band: > 1% of production runs produce soft-fail or hard-fail
>   - Indicates either threshold miscalibration (see C-1) or recurring no-op patterns
>   - Calibration owner: Reliability Owner; S2 thresholds require documented recalibration
>     protocol before M14 is normative (debate finding: timing thresholds lack methodology).

**Rationale**: P04 SS5.2 (timeout budgets), debate-05 Round 2 (S2 calibration methodology gap).
Both metrics are provisional; they require shadow-mode data collection per SS8.1/SS8.2 before
becoming normative.

**Dependencies**: SS8.1 (provisional vs. normative threshold rule applies here too).

---

### SS8.5 -- Audit Gate KPI Instrumentation (NEW SUBSECTION)

[Source: UNIQUE-B (R10)]

**Change type**: ADD (new subsection after SS8.4)

**Proposed addition**:

> **SS8.5 Audit gate KPI instrumentation**
> The audit gate state machine introduces new event types that feed into existing KPIs:
> - **M1 (runtime)**: Audit lease acquisition and evaluation duration are new M1 inputs.
> - **M7 (stale-running incidents)**: Audit lease timeout events are M7 incidents.
> - **M9 (override governance)**: OverrideRecord creation and approval events are M9 inputs.
> These instrumentation points must be wired in Phase 2 before shadow mode data is collected.

**Rationale**: Adversarial review A Section 9 (SS7.2 and SS8 were missing from original update table).

**Dependencies**: SS7.2 M1/M8 recalibration annotation.

---

### SS9.2 -- Owner Responsibilities

[Source: UNIQUE-B (R11)]

**Current text** (excerpt):
> - **Policy owner**: profile thresholds + severity mapping
> - **State-machine owner**: legal/illegal transition validator correctness
> - **Reliability owner**: timeout/retry/backoff + stale recovery
> - **Migration owner**: rollout/rollback readiness and drills
> - **Program manager**: open-decision closure with owner+deadline tracking

**Change type**: ADD (append to the owner list)

**Proposed addition**:

> - **Tasklist owner**: `audit_gate_required` derivation rules and `Critical Path Override` field definition. Owns per-task metadata schema compatibility between tasklist generator and sprint runner.

**Rationale**: Delta analysis D (SS9.2 addition); adversarial review A (undefined term `Critical Path Override`).

**Dependencies**: SS3.1 canonical terms (defines audit_gate_required and Critical Path Override).

---

### SS9.3 -- Decision Deadlines

[Source: UNIQUE-B (R12)]

**Current text** (excerpt):
> All open blocking decisions must have:
> - Owner
> - UTC decision deadline
> - Effective rollout phase
>
> No GO decision without all three assigned.

**Change type**: ADD (append locked decision record)

**Proposed addition** (append after the existing SS9.3 text):

> **Locked decision on record (2026-03-17)**: Branch (b) -- v1.2.1 implements phase-scope and release-scope audit gates only. Task-scope deferred to v1.3. This decision is locked per SS9.3 with the following record:
> - **Owner**: [to be assigned]
> - **UTC deadline**: [to be assigned]
> - **Effective rollout phase**: All phases of v1.2.1 (shadow/soft/full)
> - **Evidence basis**: `execute_phase_tasks()` confirmed dead code (MF-1, unanimous adversarial review); compound delivery risk of activating orphaned code under delivery pressure.
> - **Reversal condition**: If Phase 1 investigation shows per-task artifacts are not individually addressable within phase subprocess output (Branch decision R1), escalate to program manager.

**Rationale**: Branch decision C7.

**Dependencies**: SS2.1 locked decision #6 (must exist).

---

### SS10.1 -- Phase Plan

[Source: synthesized]

**Resolution**: Plan B provides the detailed phase plan for core v1.2.1 work. Plan A's behavioral gate prerequisites (P0-A, P0-B, P0-C) are merged INTO Plan B's Phase 0 and Phase 2 structures.

**Current text**:
> - **Phase 0**: design/policy lock and owner/date assignments
> - **Phase 1**: deterministic contracts + evaluator + transition validator
> - **Phase 2**: runtime controls (lease/heartbeat/retry/recovery)
> - **Phase 3**: sprint CLI integration + override governance flow + report persistence
> - **Phase 4**: rollout execution + KPI gates + rollback drills

**Change type**: REPLACE

**Proposed replacement**:

> - **Phase 0**: Decision lock + code prerequisites
>   - Locked decisions closed: branch (b) record, owner/deadline assignments
>   - Code: retire `_apply_resume_after_spec_patch()` (roadmap executor)
>   - Code: wire `deviation-analysis` step into roadmap `_build_steps()` (includes updating `_get_all_step_ids()` and writing `build_deviation_analysis_prompt()`)
>   - **P0-A (Defect fixes, prerequisite for G-012)**: Fix Defect 1 (`run_portify()` must pass `step_runner` to `PortifyExecutor`) and Fix Defect 2 (`commands.py` must call `validate_portify_config()` before `run_portify()`). These are independent of v1.2.1 spec infrastructure and must be in production before G-012 can pass a legitimate run.
>   - **P0-B (SilentSuccessDetector Phase 1 deployment)**: `silent_success.py` module, executor instrumentation, and `test_no_op_pipeline_scores_1_0` test. This is deployable in parallel with the v1.2.1 Phase 1 spec work and has no dependency on `AuditWorkflowState` or `GateResult` -- in Phase 1, `SilentSuccessResult` emits to the `return-contract.yaml` `silent_success_audit` block as a standalone artifact.
>   - **P0-C (D-03 + D-04 deployment)**: `fidelity_inventory.py` helper, two new semantic check functions in `SPEC_FIDELITY_GATE`, and test `test_run_deterministic_inventory_cli_portify_case`. Independently deployable in ~6 hours; no dependency on Phase 1 spec infrastructure.
>   - Go/no-go gate: all Phase 0 conditions met, branch decision locked per SS9.3
>
> - **Phase 1**: Deterministic contracts + evaluator
>   - Data models: `AuditWorkflowState` enum (milestone + release scopes only, v1.2.1), `AuditGateResult` dataclass (SS6.1), `AuditLease` dataclass, profile enum
>   - Survey `cli/audit/` subsystem for reusable patterns and naming conflicts before finalizing model design
>   - Transition validator: legal/illegal table per SS4.1 (milestone + release scopes)
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
>   - **G-012 smoke test gate** (`smoke_gate.py`) -- operational after P0-A fixes are in production
>   - **SilentSuccessDetector promoted from executor hook to GateResult entry** -- integrates with the `AuditWorkflowState` and `SprintGatePolicy` wiring completed in Phase 2
>   - **S2 calibration protocol** must be documented and approved by Reliability Owner before G-012 and M14 metrics are activated at Soft enforcement phase
>   - Go/no-go gate: timeout/retry paths terminate deterministically (no deadlocks)
>
> - **Phase 3**: Sprint CLI integration + operator surface
>   - TUI: display `AuditWorkflowState` in phase table; release guard; operator guidance panel
>   - `sc-audit-gate/SKILL.md`: command surface, profile selection, override governance flow
>   - `_save_state()`: add `audit` block for gate result persistence
>   - Go/no-go gate: transition blocking/override rules enforced per scope (milestone + release)
>
> - **Phase 4**: Rollout execution + KPI gates
>   - Shadow -> Soft -> Full per SS7.1 promotion criteria
>   - Rollback drills per SS7.3
>   - KPI normalization from shadow data (SS8.2)
>   - Go/no-go gate: phase gates pass by KPI criteria and rollback drill success

**Rationale**: Plan B provides the implementation-ready phase structure derived from branch decisions C1-C7 and adversarial delta review. Plan A's behavioral gate prerequisites (P0-A, P0-B, P0-C) are independently deployable additions merged into Phase 0. Plan A's Phase 2 behavioral gate integration items (G-012, SilentSuccessDetector promotion, S2 calibration) are merged into Phase 2. Both streams coexist without conflict.

**Dependencies**: SS10.2 file-level change map entries must align with these phase assignments.

---

### SS10.2 -- File-Level Change Map

[Source: synthesized]

**Resolution**: Plan B provides the structural rewrite removing line citations. Plan A's behavioral gate extension files are added as clearly-labeled subsections within Plan B's phase structure.

**Current text** (9 numbered entries with line citations):
> 1. `src/superclaude/cli/sprint/models.py` -- states/enums/constraints/profile fields
> 2. `src/superclaude/cli/sprint/tui.py` -- completion/release guards and operator guidance
> ...
> 9. `tests/sprint/test_audit_gate_rollout.py` -- shadow/soft/full + rollback behavior

**Change type**: REPLACE

**Proposed replacement**:

> #### Phase 0 prerequisites
>
> **Core spec prerequisites (Plan B)**:
> - `roadmap/executor.py` -- remove `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()` (spec-patch auto-resume retirement)
> - `roadmap/executor.py` -- add `deviation-analysis` step to `_build_steps()` after `spec-fidelity`; update `_get_all_step_ids()` to include `deviation-analysis`; write `build_deviation_analysis_prompt()` function
>
> **P0-A: Defect fixes (prerequisite for G-012; independent of spec infrastructure)**:
> - `src/superclaude/cli/cli_portify/executor.py` -- pass `step_runner` to `PortifyExecutor` in `run_portify()`. Create `STEP_DISPATCH` mapping from step IDs to imported step functions from `steps/*.py`.
> - `src/superclaude/cli/cli_portify/commands.py` -- add `validate_portify_config()` call between `load_portify_config()` and `run_portify()`. Exit non-zero on validation errors.
>
> **P0-B: Silent Success Detection (deployable immediately; no Phase 1 dependency)**:
> - `src/superclaude/cli/cli_portify/silent_success.py` [NEW, ~300 lines] -- `FileSnapshot`, `StepTrace`, `SilentSuccessConfig`, `SilentSuccessDetector`, `SilentSuccessResult`, `SilentSuccessError` dataclasses and detector implementation.
> - `src/superclaude/cli/cli_portify/executor.py` [ADDITIVE, ~20 lines] -- Change A: `_step_traces: list[StepTrace]` field + initialization. Change B: `time.monotonic()` wrap around `_step_runner` call; append `StepTrace`. Change C: Post-loop detector invocation before `_emit_return_contract()`. Change D: `pipeline_start_time = time.time()` + `snapshot_pre_run()` call before step loop.
> - `src/superclaude/cli/cli_portify/models.py` [ADDITIVE, ~10 lines] -- Add `PortifyOutcome.SILENT_SUCCESS_SUSPECTED` and `PortifyOutcome.SUSPICIOUS_SUCCESS` enums. Add `silent_success_config: SilentSuccessConfig` field to `PortifyExecutor` (default instance). Add `_pipeline_start_time: float` field.
> - `tests/cli_portify/test_silent_success.py` [NEW, ~200 lines] -- 7 tests including `test_no_op_pipeline_scores_1_0` (AC-10: must pass against current broken executor) and `test_override_blocked_at_release_scope`.
>
> **P0-C: Spec Fidelity Deterministic Checks D-03 + D-04 (deployable in ~6h; no dependency)**:
> - `src/superclaude/cli/roadmap/fidelity_inventory.py` [NEW, ~150 lines] -- `SpecInventory` dataclass; `build_spec_inventory(spec_text: str) -> SpecInventory`; `_DISPATCH_TABLE_PATTERN` regex; `_STEP_DISPATCH_CALL` regex; `_DEP_ARROW_PATTERN` regex. **Scope note**: D-01 (FR-NNN) and D-05 (stub sentinels) are explicitly excluded from this module per SS1.3. Only D-03 and D-04 are implemented.
> - `src/superclaude/cli/roadmap/gates.py` [EXTEND, ~80 lines] -- Add `_check_dispatch_tables_preserved(content: str, inventory: SpecInventory) -> bool`. Add `_check_dispatch_functions_preserved(content: str, inventory: SpecInventory) -> bool`. Extend `SPEC_FIDELITY_GATE.semantic_checks` to include both new check functions. Add enforcement: if `dispatch_tables_preserved: false` OR `dispatch_functions_preserved: false` in frontmatter, gate fails regardless of `high_severity_count`.
> - `tests/roadmap/test_fidelity_inventory.py` [NEW, ~200 lines] -- 10 tests including `test_run_deterministic_inventory_cli_portify_case` which uses the actual v2.25 spec and roadmap artifacts from `.dev/releases/complete/v2.25-cli-portify-cli/`.
>
> #### Phase 1: Deterministic contracts
> - `src/superclaude/cli/sprint/models.py` -- add `AuditWorkflowState` enum (milestone + release scopes only); add `AuditGateResult` dataclass (SS6.1, disambiguated from existing `cli/audit/` `GateResult`); add `AuditLease` dataclass; add profile enum (`strict | standard | legacy_migration`)
> - `src/superclaude/skills/sc-audit-gate-protocol/SKILL.md` -- deterministic evaluator; legal/illegal transition table for milestone + release scopes; recovery flow
> - `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` -- add `audit_gate_required: bool` per task (derivation: `Tier==STRICT or Risk==High or Critical Path Override==true`); add `schema_version` field; add phase-level aggregation rule
> - `src/superclaude/cli/tasklist/` -- parse and emit `audit_gate_required` in generated phase files
>
> #### Phase 2: Runtime controls
> - `src/superclaude/cli/sprint/executor.py` -- wire `SprintGatePolicy` into `execute_sprint()` at post-subprocess, pre-classification boundary; phase scope only
> - `src/superclaude/cli/sprint/monitor.py` -- extend `OutputMonitor` to support audit lease heartbeat events as a distinct event class
> - `src/superclaude/cli/pipeline/trailing_gate.py` -- wire `TrailingGateRunner` for phase-scope evaluation; `GateScope.MILESTONE` and `GateScope.RELEASE` (already defined)
> - `src/superclaude/cli/sprint/models.py` -- wire `ShadowGateMetrics` for audit gate shadow mode data collection
> - `src/superclaude/cli/sprint/commands.py` -- expose `--grace-period` CLI flag
>
> **Phase 2 additions -- Behavioral Gate Integration**:
> - `src/superclaude/cli/cli_portify/smoke_gate.py` [NEW, ~400 lines] -- `SmokeTestConfig`, `SmokeTestResult` dataclasses; `run_smoke_test(config) -> SmokeTestResult`; `_check_execution_time()`, `_check_intermediate_artifacts()`, `_check_artifact_content()`. `SMOKE_TEST_GATE: GateCriteria` (tier=STRICT, scope=RELEASE). Constants: `SMOKE_NOOP_CEILING_S=5`, `SMOKE_MIN_REAL_EXECUTION_S=10`, `SMOKE_TIMEOUT_S=600`. **Timing check severity**: `WARN` only (not BLOCKING) per debate-04 critical finding. Primary BLOCKING check: `intermediate-artifact-absence`. `--mock-llm` mode required for CI environments without API access.
> - `src/superclaude/cli/cli_portify/gates.py` [EXTEND, ~5 lines] -- Add `GATE_REGISTRY["smoke-test"] = SMOKE_TEST_GATE` (G-012 in the existing G-000-G-011 sequence).
> - `src/superclaude/cli/cli_portify/commands.py` [EXTEND, ~10 lines] -- Add smoke gate invocation to release check path (runs once at pipeline completion, not per-step).
> - `tests/fixtures/cli_portify/smoke/sc-smoke-skill/SKILL.md` [NEW] -- Minimal smoke fixture with component names `InputValidator`, `DataProcessor`, `OutputFormatter`. Must retain these names -- they are content evidence anchors in `smoke_gate.py`.
> - `tests/fixtures/cli_portify/smoke/sc-smoke-skill/refs/minimal-protocol.md` [NEW] -- Minimal ref document (~10-20 lines) for component description.
> - `tests/fixtures/cli_portify/smoke/README.md` [NEW] -- Stability contract: component names, maintenance rules, CI configuration notes.
> - `tests/cli_portify/test_smoke_gate.py` [NEW, ~200 lines] -- 5 unit tests covering AC-001 through AC-008. Includes `test_transient_failure_on_api_error` and `test_fixture_content_matches_gate_patterns` (prevents fixture drift).
> - `src/superclaude/cli/cli_portify/silent_success.py` (Phase 2 update) -- Integrate `SilentSuccessResult` into `GateResult` schema (SS6.1 `silent_success_audit` block). Gate failure class updated from standalone emission to `failed(policy.silent_success)`.
>
> #### Phase 3: Sprint CLI integration
> - `src/superclaude/cli/sprint/tui.py` -- extend phase table to display `AuditWorkflowState` values; add release guard (block "Sprint Complete" unless `audit_release_passed`); add operator guidance panel for `audit_*_failed` display
> - `src/superclaude/skills/sc-audit-gate/SKILL.md` -- command surface, profile selection, override governance flow
> - `src/superclaude/cli/roadmap/executor.py` -- add `audit` block to `_save_state()` for gate result persistence
>
> #### Phase 4: Rollout + tests
> - `tests/sprint/test_audit_gate_state_machine.py` -- legal/illegal transitions + stuck-state recovery (milestone + release scopes)
> - `tests/sprint/test_audit_gate_profiles.py` -- profile determinism + severity behavior
> - `tests/sprint/test_audit_gate_overrides.py` -- scope-limited override governance
> - `tests/sprint/test_audit_gate_rollout.py` -- shadow/soft/full + rollback behavior

**Rationale**: Plan B provides the structural rewrite aligned with the adversarial review consensus to remove line citations. Plan A's behavioral gate extension files are added as subsections: P0-A/P0-B/P0-C in Phase 0, smoke gate and SilentSuccessDetector integration in Phase 2.

**Dependencies**: SS10.1 phase plan (phase assignments must be consistent).

---

### SS10.3 -- Acceptance Criteria Per Phase

[Source: A+B-merged]

**Current text**:
> - Phase 0: all blocking decisions closed with owner/date
> - Phase 1: deterministic replay stability for same input; fail-safe unknown handling
> - Phase 2: timeout/retry paths terminate deterministically (no deadlocks)
> - Phase 3: transition blocking/override rules enforced per scope
> - Phase 4: phase gates pass by KPI criteria and rollback drill success

**Change type**: EXTEND (Plan A adds Phase 0 and Phase 2 criteria; Plan B extends Phase 1 criterion)

**Proposed replacement**:

> - **Phase 0**: all blocking decisions closed with owner/date. ADDITIONALLY:
>   - **P0-A (Defect fixes)**: `run_portify()` with a test fixture produces at least one
>     intermediate artifact beyond `return-contract.yaml` (Fix 1 verified). `commands.py`
>     exits non-zero when `validate_portify_config()` returns errors (Fix 2 verified).
>   - **P0-B (SilentSuccessDetector)**: `test_no_op_pipeline_scores_1_0` passes against the
>     executor in its current state (no `step_runner` provided) -- `suspicion_score = 1.0`,
>     outcome `SILENT_SUCCESS_SUSPECTED`. `return-contract.yaml` includes `silent_success_audit`
>     block. CLI exits non-zero.
>   - **P0-C (D-03/D-04)**: `test_run_deterministic_inventory_cli_portify_case` passes -- the
>     actual v2.25 spec/roadmap pair produces `dispatch_tables_preserved: false` and
>     `dispatch_functions_preserved: false`. Gate rejects the roadmap even with
>     `high_severity_count: 0`.
>
> - **Phase 1**: deterministic replay stability for same input; fail-safe unknown handling; roadmap pipeline produces validated `deviation-analysis.md` artifact; per-task output artifacts are individually addressable within phase subprocess output (C3 validation checkpoint)
>
> - **Phase 2**: timeout/retry paths terminate deterministically (no deadlocks). ADDITIONALLY:
>   - **G-012 smoke gate**: against the known-bad executor (step_runner not wired), smoke gate
>     fails with `policy.smoke_failure.timing` AND `policy.smoke_failure.artifact_absence`.
>     After P0-A fixes are applied, a real run against the smoke fixture passes all G-012 checks.
>   - **S2 calibration protocol**: documented and approved by Reliability Owner before soft-phase
>     activation of M14 metric.
>   - **SilentSuccessDetector GateResult integration**: `SilentSuccessResult` appears in the
>     unified audit trail with `failure_class: policy.silent_success`; override at release scope
>     is blocked; override at task/milestone scope requires valid `OverrideRecord`.
>   - **EXEMPT aggregate bypass guard (C-1)**: a pipeline with all-EXEMPT step registry
>     (without `--dry-run`) produces `failed(policy.silent_success)`, not pass.
>
> - **Phase 3**: transition blocking/override rules enforced per scope (milestone + release)
>
> - **Phase 4**: phase gates pass by KPI criteria and rollback drill success

**Rationale**: Plan A adds P0-A/P0-B/P0-C acceptance criteria for Phase 0 and behavioral gate criteria for Phase 2. Plan B extends Phase 1 criterion with deviation-analysis and C3 validation. All additions target different phases and are compatible.

**Dependencies**: Phase 0 criteria must be verified before Phase 2 G-012 and GateResult integration can be tested against real execution.

---

### SS11 -- Checklist Closure Matrix

[Source: A+B-merged]

**Current text** (excerpt):
> | 9. Risk/reliability controls | PASS (conditional) | Finalize retry/backoff/timeout values and budgets | `checklist-outcome-v1.2.md`, `risk-register-v1.2.md` |
> | 10. Implementation readiness | NO-GO (current) | Close all 4 blockers with owner/date and reflect in artifacts | `checklist-outcome-v1.2.md`, `executive-summary.md` |

**Change type**: MODIFY (Plan B updates row 9 evidence; Plan A updates row 10, adds rows 11-12)

**Proposed changes from Plan B** (update row 9 evidence source):

| Checklist section | Current status | Closure condition | Evidence source |
|---|---|---|---|
| 9. Risk/reliability controls | PASS (conditional) | Finalize retry/backoff/timeout values and budgets; lock `audit_lease_timeout` defaults via Reliability Owner | `checklist-outcome-v1.2.md`; `delta-analysis-post-v2.26.md` SS D1.1 (partially resolved); `adversarial-delta-review-merged.md` SS7 |

**Proposed changes from Plan A** (update row 10, add rows 11-12):

> | 10. Implementation readiness | **PARTIAL-GO** | Original 4 blockers remain (see SS12.3). P0-B and P0-C are GO-eligible independently (no blocked dependencies). P0-A defect fixes must be scheduled. G-012 Phase 2 integration is conditional on Phase 1 completion. | `checklist-outcome-v1.2.md` + behavioral gate analysis |
> | **11. Behavioral gate extensions** | **PASS (conditional)** | P0-B and P0-C independently deployable with no spec infrastructure dependency; verify P0-A defect fixes are scheduled before G-012 integration | `proposal-05-silent-success-detection.md`, `proposal-04-smoke-test-gate.md`, `proposal-02-spec-fidelity-hardening.md` |
> | **12. Smoke gate CI prerequisites** | **NO-GO (current)** | `--mock-llm` mode must be specified before CI integration; API key configuration documented in `smoke/README.md`; `test_fixture_content_matches_gate_patterns` unit test must ship with gate on day one | `proposal-04-smoke-test-gate.md` SS8.2, `debate-04` Round 2 synthesis |

**Rationale**: Plan B updates row 9 evidence to reflect partial resolution from v2.26 codebase. Plan A upgrades row 10 from NO-GO to PARTIAL-GO and adds rows 11-12 for behavioral gate extensions.

**Dependencies**: SS10.1 phase plan (P0-B, P0-C independence established there).

---

### SS12.3 -- Current Blocker List

[Source: synthesized]

**Resolution**: Both Plan A and Plan B add new blockers. Plan B's note about partial resolution of blocker 2 is preserved. All new blockers are non-overlapping and merged sequentially.

**Current text**:
> 1. Profile thresholds and task-tier major-severity behavior not finalized
> 2. Retry/backoff/timeout values not finalized
> 3. Rollback/safe-disable triggers not finalized
> 4. Open blocking decisions not yet assigned owner+deadline in final artifact set

**Change type**: MODIFY + ADD

**Proposed replacement**:

> **Original blockers (still open for core v1.2.1 spec)**:
> 1. Profile thresholds and task-tier major-severity behavior not finalized
> 2. Retry/backoff/timeout values not finalized (partially resolved by v2.26 -- see `delta-analysis-post-v2.26.md` SS1 for concrete formula; audit-specific lease budget remains TBD)
> 3. Rollback/safe-disable triggers not finalized
> 4. Open blocking decisions not yet assigned owner+deadline in final artifact set
>
> **New blockers from branch decision and adversarial review (Plan B)**:
> 5. Branch (b) locked decision record incomplete -- owner and UTC deadline not yet assigned (required per SS9.3 before Phase 1 start)
> 6. `reimbursement_rate = 0.8` in `TurnLedger` (sprint/models.py) is a dead model field with no usage. Decision required: (a) wire as turn-recovery credit for audit retry paths, or (b) remove. File as cleanup item and close before Phase 2 GO. (Governance directive -- not a timeout/retry semantic; see SS4.4 revision.)
>
> **New blockers introduced by behavioral gate extensions (Plan A)**:
> 7. **S2 calibration methodology** -- Silent success detection timing thresholds (50ms suspicious, 10ms near-certain no-op) are not derived from benchmarks. Reliability Owner must document calibration methodology and recalibration protocol before M14 metric is normative at soft phase. (Source: `debate-05` Round 2, Devil's Advocate unchallenged finding)
> 8. **`--mock-llm` mode specification** -- G-012 smoke gate cannot be safely integrated into CI without a `--mock-llm` mode that validates all non-LLM checks without API calls. Mode must be specified before Phase 2 CI integration. (Source: `debate-04` Round 2 synthesis)
> 9. **P0-A defect fix scheduling** -- Defect 1 (`step_runner` wiring) and Defect 2 (`validate_portify_config()` call) must be scheduled as separate work items with owner and deadline before G-012 smoke gate integration can begin. (Source: `proposal-04-smoke-test-gate.md` SS8.5)

**Rationale**: All 9 blockers are legitimate, actionable, and non-overlapping. Plan B contributes branch decision and codebase-verified findings (5-6). Plan A contributes behavioral gate extension blockers (7-9). Blocker 2 note about partial resolution from Plan B is preserved.

**Dependencies**: SS12.4 required user decisions must be extended to cover new blockers.

---

### SS12.4 -- Required User Decisions

[Source: A+B-merged]

**Current text**:
> 1. Approve canonical profile model and numeric thresholds
> 2. Approve major-severity behavior at task tier under `standard`
> 3. Approve retry/backoff/timeout values and max attempts
> 4. Approve rollback/safe-disable objective triggers
> 5. Approve override governance model (single vs dual approver) and review cadence

**Change type**: EXTEND (Plan B adds decision 6; Plan A adds decisions 7-9)

**Proposed additions from Plan B**:

> 6. **Confirm per-task output artifacts are individually addressable** within phase subprocess output (C3 validation checkpoint). If not addressable, decide: (a) restructure phase output before Phase 2, or (b) accept coarser evaluation granularity and update Branch (b) amendment accordingly.

**Proposed additions from Plan A**:

> 7. **Approve S2 calibration methodology** -- The Reliability Owner must specify: (a) the
>    measurement protocol for establishing `SUSPICIOUS_MS` and `NOOP_MS` thresholds from observed
>    production run data, (b) the recalibration trigger (e.g., "after major hardware change or
>    infrastructure migration"), and (c) who owns ongoing maintenance of `SilentSuccessConfig`
>    defaults. This decision blocks soft-phase activation of M14.
>
> 8. **Approve smoke gate `--mock-llm` scope** -- Define what `--mock-llm` mode validates vs.
>    skips. At minimum: timing check remains active (mock mode must not skip the no-op ceiling
>    check); artifact-absence check must use real subprocess invocation with a stubbed LLM
>    response. Content evidence checks may be relaxed in mock mode. Decision must specify the
>    exact check matrix for `--mock-llm` vs. real mode.
>
> 9. **Approve D-03/D-04 pattern scope** -- Confirm that D-03 (`_DISPATCH_TABLE_PATTERN`) and
>    D-04 (`_STEP_DISPATCH_CALL`) regex patterns are sufficiently general for the project's
>    spec authoring conventions, or specify required pattern extensions. This decision gates
>    `test_run_deterministic_inventory_cli_portify_case` becoming a normative regression test.

**Rationale**: Plan B adds C3 artifact addressability decision. Plan A adds S2 calibration, mock-llm scope, and D-03/D-04 pattern scope decisions. All are independent.

**Dependencies**: SS12.3 blockers 5-9 are unblocked by these decisions.

---

### New SS13 -- Behavioral Gate Extensions

[Source: UNIQUE-A]

**Change type**: NEW_SECTION

**Insert after SS12, before "Top 5 Immediate Actions"**:

> ## 13. Behavioral Gate Extensions (v1.2.1 Additions)
>
> ### 13.1 Motivation
>
> Sections 1-12 of this spec address the audit workflow state machine, gate result schemas, and
> rollout mechanics -- all operating on the transition layer between task/milestone/release states.
> Three validated improvements from the cli-portify no-op forensic analysis address a distinct
> gap: **the existing gate system validates documents; these extensions validate behavior**.
>
> The behavioral gate extensions are specified here as a unified section because they share a
> common motivation (the no-op anti-pattern), share an implementation wave (Phase 0 prerequisites),
> and have interdependencies (SilentSuccessDetector Phase 2 integration with GateResult).
>
> ### 13.2 Silent Success Detection (P05)
>
> **Gate type**: Post-execution executor hook (Phase 1); GateResult entry (Phase 2)
> **Scope**: Applies to cli-portify executor; generalizes to any executor using the
> `(exit_code, stdout, timed_out)` return pattern
> **Blocking**: soft-fail (0.50-0.74) = overridable at task/milestone; hard-fail (>=0.75) =
> never overridable at release tier (LD-3 compliance)
>
> **Signal suite**:
> | Signal | Measurement | Weight |
> |--------|-------------|--------|
> | S1 -- Artifact Content | Per-step output file existence + min lines + section count + non-header ratio | 0.35 |
> | S2 -- Execution Trace | `wall_clock_ms` and `stdout_bytes` per step via `time.monotonic()` wrap | 0.35 |
> | S3 -- Output Freshness | mtime >= pipeline_start_time; content hash change from pre-run snapshot | 0.30 |
>
> **Composite formula**:
> ```
> suspicion_score = ((1-S1) x 0.35) + ((1-S2) x 0.35) + ((1-S3) x 0.30)
> ```
> Bands: 0.0-0.29 pass | 0.30-0.49 warn | 0.50-0.74 soft-fail | 0.75-1.00 hard-fail
>
> **Key constraints**:
> - S2 thresholds (50ms / 10ms) are provisional; Reliability Owner must approve calibration
>   methodology before soft-phase M14 activation (blocker 7, SS12.3)
> - EXEMPT step classification excludes individual steps from signal denominators
> - EXEMPT aggregate bypass prohibition: see SS5.2 rule 5 and C-1 resolution
> - `SilentSuccessConfig(enabled=False)` must be available for test harnesses
>
> ### 13.3 Smoke Test Gate G-012 (P04)
>
> **Gate ID**: G-012 (follows existing G-000 through G-011 in `cli_portify/gates.py`)
> **Enforcement tier**: STRICT | **Scope**: RELEASE | **Override**: forbidden (LD-3)
> **Prerequisites**: Defect 1 and Defect 2 fixes must be in production (blocker 9, SS12.3)
>
> **Check hierarchy**:
> | Check | Severity | Blocks? | No-op failure mode |
> |-------|----------|---------|-------------------|
> | Timing: elapsed < SMOKE_NOOP_CEILING_S (5s) | WARN | No -- advisory only | ~0.12s elapsed |
> | Intermediate artifact absence | ERROR | Yes | 0 artifacts beyond return-contract.yaml |
> | Content evidence (fixture proper nouns) | ERROR | Yes | No artifacts to check |
>
> **Critical debate finding**: Timing check is WARN only (not BLOCKING). The artifact-absence
> check is the primary BLOCKING mechanism. Timing as BLOCKING creates systematic CI false positives
> in environments where infrastructure overhead inflates startup time. (Source: debate-04 synthesis)
>
> **Fixture stability contract**: `tests/fixtures/cli_portify/smoke/sc-smoke-skill/SKILL.md`
> must retain component names `InputValidator`, `DataProcessor`, `OutputFormatter`. These are
> content evidence anchors -- modifying them without updating `smoke_gate.py` breaks the gate.
>
> **Failure class routing**:
> - API unavailability, network errors, HTTP 4xx/5xx -> `transient` (retryable)
> - Timing / artifact absence / content evidence -> `policy.smoke_failure.*` (not retryable)
>
> ### 13.4 Spec Fidelity Deterministic Checks D-03 + D-04 (P02 subset)
>
> **Gate**: Extension to existing `SPEC_FIDELITY_GATE` in `roadmap/gates.py`
> **Deployment**: P0-C, independently deployable (~6h), no Phase 1 dependency
>
> **Check D-03 -- Named dispatch table preservation**:
> Input: spec text (post-extraction), roadmap body text
> Detection: `_DISPATCH_TABLE_PATTERN` regex finds `UPPER_CASE_NAME = {` or `dict(` in spec;
> verifies each found name appears anywhere in roadmap text.
> Failure output: `dispatch_tables_preserved: false` in fidelity report frontmatter.
> Incident replay: `PROGRAMMATIC_RUNNERS = {` found in v2.25 spec; absent from roadmap ->
> would have produced `dispatch_tables_preserved: false` and blocked the gate.
>
> **Check D-04 -- Pseudocode dispatch function name preservation**:
> Input: spec text (code fences only), roadmap body text
> Detection: `_STEP_DISPATCH_CALL` regex finds `_run_*()` or `step_result = ` patterns in spec
> code fences; verifies at least one found function name appears in roadmap.
> Failure output: `dispatch_functions_preserved: false` in fidelity report frontmatter.
> Incident replay: `_run_programmatic_step`, `_run_claude_step` found in v2.25 spec pseudocode;
> absent from roadmap -> would have produced `dispatch_functions_preserved: false`.
>
> **Critical invariant** (repeated from SS6.1 for emphasis):
> A fidelity report with `dispatch_tables_preserved: false` OR `dispatch_functions_preserved: false`
> MUST produce `gate failed` even when `high_severity_count: 0`. The LLM cannot override these
> deterministic findings.
>
> **Overlap note**: D-03/D-04 materially overlap with Anti-Instincts' fingerprint and integration-contract modules. If Anti-Instincts ships first, D-03/D-04 should be gated behind a feature flag or made conditional. D-03/D-04's value proposition is rapid independent deployment (~6h) as interim protection.
>
> **Explicitly excluded**:
> - D-01 (FR-NNN coverage): non-load-bearing for informal/prose specs; deferred
> - D-05 (stub sentinel detection): high TDD false positive risk without section-scope filtering;
>   deferred until filtering is implemented

**Rationale**: A single authoritative section documenting all three behavioral gate extensions
with their constraints, failure modes, and interdependencies prevents these from being scattered
across the spec with inconsistent cross-references.

**Dependencies**: SS5.1 (failure class sub-types defined there); SS6.1 (GateResult blocks defined
there); SS10.2 (files defined there); SS12.3 (blockers referenced here).

---

### Top 5 Immediate Actions

[Source: A+B-merged]

**Current text**:
> 1. Finalize and sign off profile thresholds + major-severity behavior.
> 2. Finalize retry/backoff/timeout and stale-state budgets.
> 3. Ratify explicit legal/illegal transition table as implementation authority.
> 4. Approve rollback/safe-disable triggers and phase regression policy.
> 5. Assign owner + UTC deadline + effective phase to each blocking decision.

**Change type**: EXTEND (Plan A prepends 0a-0c; Plan B appends item 6)

**Proposed replacement**:

> **Behavioral gate extension actions (can proceed immediately, no spec blocker dependency)**:
>
> 0a. **Deploy P0-B (SilentSuccessDetector)**: Implement `silent_success.py` + executor
>     instrumentation + `test_no_op_pipeline_scores_1_0`. This alone would have blocked the
>     no-op pipeline across all three v2.24-v2.25 releases. Estimated effort: 2.5 days.
>     Owner: [TBD]. Start: immediately (no dependency).
>
> 0b. **Deploy P0-C (D-03 + D-04)**: Implement `fidelity_inventory.py` + two semantic checks
>     in `SPEC_FIDELITY_GATE` + regression test using v2.25 artifacts. Estimated effort: ~6h.
>     Owner: [TBD]. Start: immediately (no dependency). D-01 and D-05 explicitly excluded.
>
> 0c. **Schedule P0-A defect fixes**: Wire `run_portify()` to step dispatch (Fix 1) and add
>     `validate_portify_config()` call in `commands.py` (Fix 2). These are prerequisites for
>     G-012 smoke gate; they are not v1.2.1 spec items but must be scheduled with owner + deadline
>     before Phase 2 begins. Estimated effort: ~1.5 days total.
>
> **Original actions (renumbered)**:
>
> 1. Finalize and sign off profile thresholds + major-severity behavior.
> 2. Finalize retry/backoff/timeout and stale-state budgets.
> 3. Ratify explicit legal/illegal transition table as implementation authority.
> 4. Approve rollback/safe-disable triggers and phase regression policy.
> 5. Assign owner + UTC deadline + effective phase to each blocking decision (now includes
>    blockers 5-9 from SS12.3 and user decisions 6-9 from SS12.4).
> 6. Validate that phase subprocess output contains identifiable per-task artifacts (C3 checkpoint) -- this is a Phase 1 GO/NO-GO condition for branch (b).

**Rationale**: Plan A's actions 0a-0c can be executed today without waiting for the four original blockers. Plan B's item 6 adds C3 validation as a Phase 1 gate condition. All additions are compatible.

**Dependencies**: 0a has no dependencies. 0b has no dependencies. 0c must precede Phase 2 G-012 integration. Item 6 is a Phase 1 gate condition.

---

### Top 5 Deferred Improvements

[Source: UNIQUE-B (R20)]

**Current text**:
> 1. Add readiness preview mode pre-gate.
> 2. Improve human-readable remediation hints in gate failures.
> 3. Add trend dashboards for drift/override quality.
> 4. Add profile auto-tuning recommendations from shadow telemetry.
> 5. Optimize long-horizon artifact retention policy.

**Change type**: ADD (append item 6)

**Proposed addition**:

> 6. Activate `execute_phase_tasks()` as a standalone work item for v1.3 task-scope audit gates. Independent acceptance criteria required: real ClaudeProcess integration tests, stall detection, watchdog coverage, TUI task-within-phase progress, per-task state persistence schema. Not tied to v1.2.1 audit gate delivery.

**Rationale**: Branch decision C6.

**Dependencies**: None.

---

### Open Decisions Needed from User

[Source: UNIQUE-B (R21)]

**Current text** (5 rows):
> | Decision | Owner | Deadline (UTC) | Effective phase |
> |---|---|---|---|
> | Profile thresholds + major-severity behavior | [TBD] | [TBD] | Soft |
> | Retry/backoff/timeout policy | [TBD] | [TBD] | Soft |
> | Rollback/safe-disable triggers | [TBD] | [TBD] | Full |
> | Override approver model + review cadence | [TBD] | [TBD] | Soft |
> | `--strictness` alias deprecation date | [TBD] | [TBD] | Full |

**Change type**: ADD (append 6 new rows)

**Proposed additions**:

| Decision | Owner | Deadline (UTC) | Effective phase |
|---|---|---|---|
| Branch (b) locked decision record -- assign owner + deadline | [TBD] | [TBD] | All (Phase 0 blocker) |
| Confirm per-task artifact addressability within phase output (C3) | [TBD] | [TBD] | Phase 1 go/no-go |
| `audit_lease_timeout` default values per scope | Reliability Owner | [TBD] | Phase 2 GO |
| `max_attempts` defaults (milestone=2, release=1) normative approval | Reliability Owner | [TBD] | Shadow->Soft gate |
| M1/M8 recalibrated thresholds for phase-scope | Policy Owner | [TBD] | Shadow launch |
| `reimbursement_rate` fate (wire or remove) | [TBD] | [TBD] | Phase 2 GO |

**Rationale**: Branch decision C3, C4, C5, C7; adversarial review R6 (audit_lease_timeout); R6 (max_attempts).

**Dependencies**: None.

---

## Implementation Order Summary

[Source: A (extended to include Plan B items)]

```
TODAY (no dependencies — Plan A behavioral gate extensions):
  +-- 0a: silent_success.py + test_no_op_pipeline_scores_1_0    [2.5 days]
  +-- 0b: fidelity_inventory.py + D-03/D-04 + regression test  [6 hours]

PARALLEL (separate work items, prerequisite for G-012):
  +-- 0c: Fix 1 (step_runner wiring) + Fix 2 (validation call) [1.5 days]

PHASE 0 (Plan B core spec prerequisites):
  +-- Locked decisions closed: branch (b) record, owner/deadline assignments
  +-- Code: retire _apply_resume_after_spec_patch() (roadmap executor)
  +-- Code: wire deviation-analysis step into _build_steps()

PHASE 1 (existing v1.2.1 Phase 1 work):
  +-- AuditWorkflowState, AuditGateResult dataclass, AuditLease
  +-- Survey cli/audit/ subsystem
  +-- Transition validator, deterministic evaluator
  +-- Tasklist: audit_gate_required derivation
  +-- KPI calibration: M1/M8 for phase-scope (C4)
  +-- C3 validation checkpoint (Phase 1 go/no-go)

PHASE 2 (requires Phase 1 + 0c):
  +-- SprintGatePolicy, OutputMonitor, TrailingGateRunner, ShadowGateMetrics
  +-- --grace-period CLI flag
  +-- G-012 smoke_gate.py + smoke fixture + test_smoke_gate.py  [3 days]
  +-- SilentSuccessDetector -> GateResult integration            [1 day]
  +-- S2 calibration protocol approval

PHASE 3 (requires Phase 2):
  +-- TUI display, sc-audit-gate SKILL, _save_state() audit block

PHASE 4 (requires Phase 3):
  +-- Shadow -> Soft -> Full rollout
  +-- Rollback drills, KPI normalization
```

Total behavioral gate extension effort: ~8 days across two waves.
Core v1.2.1 spec work proceeds on its own timeline in parallel.

---

## What This Plan Does NOT Change

[Source: B (updated for accuracy given Plan A additions)]

The following spec sections are confirmed unchanged by all input sources:

| Section | Reason |
|---|---|
| SS0 Evidence model | Methodology unchanged |
| SS1.2 Primary goals | Goals remain valid under branch (b) and behavioral gate additions |
| SS3.2 Strictness vs profile | Resolution unchanged |
| SS4.2 Illegal transitions | Unchanged -- still applies to milestone + release |
| SS4.3 Override rules | Unchanged |
| SS5.3 Evidence requirements | Requirements unchanged |
| SS6.2 OverrideRecord | Unchanged |
| SS6.3 Transition event schema | Unchanged |
| SS6.4 Versioning policy | Unchanged |
| SS7.1 Rollout phases | Phases unchanged |
| SS7.3 Rollback triggers | Unchanged |
| SS8.1 Provisional vs normative | Unchanged |
| SS8.2 Calibration method | Unchanged |
| SS8.4 Heuristic operational guidance | Unchanged |
| SS9.1 Override approval model | Unchanged |
| SS12.1 GO criteria | Unchanged |
| SS12.2 NO-GO criteria | Unchanged |

**Note**: The following sections were listed as unchanged in Plan B but ARE changed by Plan A:
- SS1.3 Out-of-scope -- Plan A adds developer utility subcommand and D-01/D-05 exclusions
- SS2.2 Non-goals -- Plan A adds EXEMPT aggregate bypass and smoke test non-goals
- SS5.1 Failure classes -- Plan A adds policy sub-type taxonomy
- SS8.3 Warning/fail bands -- Plan A adds M13 and M14 provisional metrics

---

## Dependency Order for Editing

[Source: B (extended to cover Plan A items)]

When editing the spec, apply changes in this order to avoid internal inconsistencies:

```
PHASE 0 (blocking — do first):
  R2/SS2.1  -> R5/SS4.1  -> R1+A/SS1.1  -> R12/SS9.3  -> R17+A/SS12.3  -> R18+A/SS12.4  -> R21/Open Decisions

PHASE 1 (after phase 0 changes are applied):
  R4/SS3.1                  # Terms before contradictions
  A/SS1.3                   # Out-of-scope (no dependency, but logically near SS1.1)
  A/SS2.2                   # Non-goals (references SS5.2 C-1 rule)
  R3+A/SS2.3                # Contradictions (references SS2.2 and branch decision)
  R6/SS4.4                  # SS4.4 — references SS3.1 terms
  A/SS5.1                   # Failure class taxonomy (before SS5.2 and SS6.1)
  R7+A/SS5.2                # SS5.2 — references SS4.4 freshness concept + C-1 rule
  R8+A/SS6.1                # SS6.1 — references SS3.1 AuditGateResult + SS5.1 sub-types
  R9/SS7.2  -> R10/SS8.5    # SS7.2 before SS8 KPI section
  A/SS8.3                   # Warning/fail bands (M13, M14)
  R11/SS9.2                 # SS9.2 — owner responsibilities
  R13+A/SS10.1  -> R14+A/SS10.2  -> R15+A/SS10.3    # SS10 in order (synthesized)
  R16+A/SS11                # SS11 — checklist closure
  A/New SS13                # Behavioral gate extensions (references SS5.1, SS6.1, SS10.2, SS12.3)
  R19+A/Top 5 Immediate     # Top 5 Immediate Actions

ANY TIME:
  R20/Top 5 Deferred        # Top 5 Deferred
```

---

## Verification Checklist (post-edit)

[Source: B (extended to cover Plan A items)]

After editing the spec, verify these invariants hold:

**Plan B invariants**:
- [ ] SS4.1 task-scope transitions are present but annotated `[v1.3 -- deferred]`, not deleted
- [ ] SS4.4 contains zero source-file line citations (e.g., no `monitor.py:255-260`)
- [ ] SS3.1 defines all 6 new terms: AuditLease, audit_lease_timeout, max_turns, Critical Path Override, audit_gate_required, audit_attempts
- [ ] `AuditGateResult` is used consistently (not `GateResult`) in SS6.1
- [ ] SS12.3 has 9 blockers (original 4 + 2 Plan B + 3 Plan A)
- [ ] SS12.4 has 9 required decisions (original 5 + 1 Plan B + 3 Plan A)
- [ ] Open Decisions table has 11 rows (original 5 + 6 new)
- [ ] SS10.2 contains zero source-file line number citations
- [ ] SS4.4 item 3 defaults are milestone=2 and release=1 only (no task=3)
- [ ] SS1.1 contains the branch (b) scope amendment paragraph
- [ ] SS2.1 locked decisions list ends at item 6 (branch b as new item)

**Plan A invariants**:
- [ ] SS1.1 contains items 4-6 (Silent Success Detection, Smoke Test Gate G-012, Spec Fidelity D-03/D-04)
- [ ] SS1.3 contains developer utility subcommand exclusion and D-01/D-05 deferral
- [ ] SS2.2 contains EXEMPT aggregate bypass non-goal and smoke test non-goal
- [ ] SS2.3 contains 4 new contradiction rows total (2 from Plan A + 2 from Plan B)
- [ ] SS5.1 contains three `policy.*` sub-type definitions (silent_success, smoke_failure, fidelity_deterministic)
- [ ] SS5.2 contains rule 5 (EXEMPT aggregate bypass prohibition C-1)
- [ ] SS6.1 contains all three behavioral gate extension blocks (silent_success_audit, smoke_test_result, fidelity_deterministic)
- [ ] SS8.3 contains M13 (smoke test duration) and M14 (silent success suspicion rate) provisional metrics
- [ ] SS10.1 Phase 0 contains P0-A, P0-B, P0-C prerequisites
- [ ] SS10.1 Phase 2 contains G-012 and SilentSuccessDetector GateResult integration
- [ ] SS10.3 Phase 0 contains P0-A, P0-B, P0-C acceptance criteria
- [ ] SS10.3 Phase 2 contains G-012, S2 calibration, GateResult integration, and C-1 guard criteria
- [ ] SS11 contains rows 11 and 12 (behavioral gate extensions and smoke gate CI)
- [ ] SS11 row 10 reads PARTIAL-GO (not NO-GO)
- [ ] New SS13 exists with subsections 13.1-13.4
- [ ] Top 5 Immediate Actions contain items 0a, 0b, 0c before the original 5

**Cross-plan consistency invariants**:
- [ ] SS12.3 blocker numbering is sequential 1-9 with no gaps
- [ ] SS12.4 decision numbering is sequential 1-9 with no gaps
- [ ] SS10.1 phase assignments match SS10.2 file assignments match SS10.3 acceptance criteria
- [ ] All SS cross-references resolve (no dangling section references)
- [ ] No contradictions between Plan A behavioral gate additions and Plan B branch (b) scope constraints

---

## Files Referenced but Not Changed by This Plan

[Source: A]

The following files are referenced in the proposals but require NO changes to the spec document:
- `src/superclaude/cli/pipeline/trailing_gate.py` -- smoke gate does not use TrailingGateRunner
- `src/superclaude/cli/roadmap/prompts.py` -- D-03/D-04 are semantic checks, not prompt changes
- `src/superclaude/cli/cli_portify/gates.py` -- `GATE_REGISTRY` update is a code change, not a spec change
- Any existing test files -- behavioral gate tests are new files only

These are implementation targets, not spec targets. They appear in SS10.2 but do not require
additional spec language beyond what is already in this plan.
