---
release: unified-gate-enforcement-v3.0
version: 3.0.0
status: draft
date: 2026-03-18
priority: P0
estimated_scope: 900-1200 lines production code
predecessor_releases:
  - wiring-verification-gate-v1.0
  - anti-instincts-v1.0
enforcement_model: "3-profile system: strict | standard | legacy_migration"
---

# Unified Gate Enforcement v3.0 — Release Specification

## 1. Problem Statement

The pipeline currently has 7 independent gates, each with its own enforcement logic, configuration mechanism, and failure handling. This creates three categories of problems:

### 1.1 Inconsistent Enforcement Semantics

| Gate | Enforcement Implementation | Override Mechanism | Failure Mode |
|------|---------------------------|-------------------|--------------|
| SPEC_FIDELITY_GATE | `gate_passed()` in `roadmap/gates.py` | `--skip-gate spec-fidelity` | Hard fail — blocks pipeline |
| DEVIATION_ANALYSIS_GATE | Defined but never wired (see INC-041) | N/A (dead code) | Silent pass — gate is no-op |
| WIRING_GATE | `gate_passed()` via `audit/wiring_gate.py` | `--skip-wiring-gate` | 3-mode: shadow/soft/full |
| ANTI_INSTINCT_GATE | Inline check in `roadmap/generator.py:418` | None | Soft fail — warning only |
| SMOKE_TEST_GATE | `run_smoke_tests()` in `sprint/smoke.py` | `--no-smoke` | Hard fail |
| TRAILING_GATE | `TrailingGateRunner` in `pipeline/trailing_gate.py` | `resolve_gate_mode()` scope-aware | Configurable per scope |
| RELEASE_GATE | Not yet implemented | N/A | N/A |

### 1.2 Override Governance Gap

Gate overrides are currently flag-based with no audit trail:
- `--skip-gate` accepts any gate name string with no validation
- `--skip-wiring-gate` is a boolean that leaves no trace in artifacts
- `--no-smoke` is undocumented and inconsistent with other flag naming
- No mechanism to distinguish "override because gate is known-flaky" from "override because deadline pressure"

### 1.3 Missing Rollback Contract

When a gate fails during full enforcement, the pipeline stops but does not define:
- What artifacts are safe to keep vs. what must be invalidated
- Whether subsequent gates should still evaluate (for diagnostic completeness)
- How to resume after remediation without re-running the entire pipeline

## 2. Requirements

### R1: Unified Gate Registry (P0)

All gates MUST be registered in a central `GateRegistry` with a uniform interface.

**Registry entry schema**:
```python
@dataclass
class GateRegistryEntry:
    gate_id: str                    # unique, e.g., "spec-fidelity"
    gate_criteria: GateCriteria     # existing model
    scope: Literal["task", "milestone", "release"]
    enforcement_profile_overrides: dict[str, EnforcementLevel]  # profile → level
    default_enforcement: EnforcementLevel  # used when profile doesn't specify
    evaluation_order: int           # lower = earlier; ties broken by gate_id
    dependencies: list[str]         # gate_ids that must pass before this gate runs
    timeout_seconds: int            # max time for gate evaluation; default 60
    retry_policy: RetryPolicy | None  # None = no retry
```

**Evaluation order contract**: Gates evaluate in `evaluation_order` ascending. When two gates have the same `evaluation_order`, they are disambiguated by lexicographic sort of `gate_id`. This ordering is deterministic and MUST NOT vary between runs.

**Dependency contract**: If gate A lists gate B in `dependencies`, then:
- Gate B MUST complete evaluation before gate A starts
- If gate B fails with `hard_fail`, gate A is SKIPPED (not failed) with `skip_reason = "dependency_failed: {gate_b_id}"`
- If gate B fails with `soft_fail`, gate A still evaluates (soft failures are advisory)
- Circular dependencies MUST be detected at registry load time and MUST raise `GateConfigurationError` — the pipeline MUST NOT start

### R2: Enforcement Profiles (P0)

Three enforcement profiles govern gate behavior. Profile selection is per-pipeline-run, NOT per-gate.

**Profile definitions**:

| Profile | Description | Override Policy | Gate Failure Behavior |
|---------|-------------|----------------|----------------------|
| `strict` | Production-grade enforcement | No overrides permitted for any gate at any scope | Hard fail on any gate failure; no continuation |
| `standard` | Normal development enforcement | Override permitted for task and milestone scope ONLY; release scope overrides prohibited | Hard fail at release scope; soft fail with remediation log at task/milestone |
| `legacy_migration` | Transitional profile for v1.0→v2.0 migration | Override permitted at all scopes with mandatory `override_reason` | Soft fail everywhere; all failures logged to `DeferredRemediationLog` |

**Override governance**:
- Every override MUST record: `gate_id`, `scope`, `override_reason` (free text, minimum 10 characters), `overridden_by` (user identity), `timestamp_utc`
- Overrides with `override_reason` shorter than 10 characters MUST be rejected with error: `"Override reason must be at least 10 characters (got {len}). Provide a meaningful justification."`
- The `strict` profile MUST NOT accept overrides under ANY circumstances, including `--force` flags, environment variables, or configuration file entries. The strict profile's no-override policy is enforced at the registry level, not the CLI level — there is no code path that can bypass it.
- Release-scope overrides are PROHIBITED in both `strict` and `standard` profiles. ONLY `legacy_migration` permits release-scope overrides.

### R3: Gate Evaluation Pipeline (P0)

Gates evaluate in a defined sequence with short-circuit and continuation semantics.

**Evaluation modes**:
- `fail_fast`: Stop on first hard failure. Remaining gates are not evaluated. Used in `strict` profile by default.
- `evaluate_all`: Continue evaluating all gates even after failures. Used in `standard` and `legacy_migration` profiles. Produces a complete diagnostic report.

**Evaluation sequence for a single scope checkpoint**:
1. Load enforcement profile for current run
2. Sort gates by `evaluation_order` (ties → lexicographic `gate_id`)
3. Check dependency graph for satisfied preconditions
4. For each gate in order:
   a. If dependencies unsatisfied → SKIP gate
   b. Evaluate gate with `timeout_seconds` limit
   c. On timeout → treat as `hard_fail` with `failure_reason = "evaluation_timeout"`
   d. On pass → record in audit trail, continue
   e. On soft_fail → record in `DeferredRemediationLog`, continue
   f. On hard_fail:
      - If `fail_fast` mode → stop evaluation, return aggregate result
      - If `evaluate_all` mode → record failure, continue to next gate
5. Return `GateEvaluationResult` with per-gate outcomes

**GateEvaluationResult schema**:
```python
@dataclass
class GateEvaluationResult:
    scope: Literal["task", "milestone", "release"]
    profile: str
    evaluation_mode: str
    gates_evaluated: int
    gates_passed: int
    gates_failed: int
    gates_skipped: int
    overall_passed: bool  # True iff gates_failed == 0
    gate_results: list[IndividualGateResult]
    evaluation_duration_ms: int
    timestamp_utc: datetime
```

### R4: Deferred Remediation System (P1)

When gates fail in `standard` or `legacy_migration` profiles at task/milestone scope, failures are recorded for later resolution rather than blocking immediately.

**DeferredRemediationLog schema**:
```python
@dataclass
class RemediationEntry:
    gate_id: str
    scope: Literal["task", "milestone"]
    entity_id: str          # task or milestone ID
    failure_type: Literal["soft_fail", "hard_fail_overridden"]
    failure_evidence: str    # gate output content
    override_reason: str | None  # populated only for overridden hard failures
    overridden_by: str | None
    created_utc: datetime
    remediated: bool = False
    remediated_utc: datetime | None = None
    remediation_evidence: str | None = None
```

**Remediation enforcement contract**:
- At release scope, ALL entries in the `DeferredRemediationLog` for the current pipeline run MUST be resolved (`remediated == True`) before the release gate passes
- "Resolved" means: `remediated == True` AND `remediation_evidence is not None` AND `remediation_evidence` is non-empty
- A release gate MUST fail with `failure_reason = "unresolved_deferred_remediations: {count}"` if any entries remain unresolved
- This creates a ratchet: you can defer at task scope, but you CANNOT ship without resolving all deferrals

### R5: Rollback Contract (P1)

When a gate fails during full enforcement, the system must define artifact validity.

**Artifact classification on gate failure**:
- `VALID`: Artifacts produced BEFORE the failing gate's scope checkpoint. These are safe to keep.
- `TAINTED`: Artifacts produced during the same scope checkpoint as the failing gate. These must be re-evaluated after remediation.
- `INVALIDATED`: Artifacts produced AFTER the failing gate's scope checkpoint that depend on tainted artifacts. These must be regenerated.

**Rollback rules**:
- On task-scope gate failure: ONLY the failing task's artifacts are tainted. Other tasks in the phase are unaffected.
- On milestone-scope gate failure: ALL artifacts in the failing milestone are tainted. Predecessor milestones remain valid.
- On release-scope gate failure: ALL artifacts in the release are tainted UNLESS they were independently validated by a passed gate.

**Resume contract**:
- After remediation, the pipeline can resume from the failed scope checkpoint by providing `--resume-from {checkpoint_id}`
- On resume, ONLY tainted and invalidated artifacts are re-evaluated
- VALID artifacts are NOT re-run — their gate results are loaded from the audit trail
- The resume mechanism MUST verify that no VALID artifact has been modified since the original run (SHA-256 comparison). Modified "valid" artifacts are reclassified as TAINTED.

### R6: Unified CLI Interface (P1)

Replace the current per-gate flag system with a unified interface.

**New interface**:
```
superclaude pipeline --profile strict|standard|legacy_migration
superclaude pipeline --gate-override <gate-id> --reason "justification text"
superclaude pipeline --gate-list                    # show registered gates
superclaude pipeline --gate-status <gate-id>        # show gate config and history
superclaude pipeline --resume-from <checkpoint-id>  # resume after remediation
```

**Deprecated flags** (emit deprecation warning for 2 releases, then remove):
- `--skip-gate` → `--gate-override`
- `--skip-wiring-gate` → `--gate-override wiring-verification`
- `--no-smoke` → `--gate-override smoke-test`
- `--strictness` → `--profile`

**Deprecation behavior**: When a deprecated flag is used:
1. Emit `DEPRECATION WARNING: --skip-gate is deprecated. Use --gate-override <gate-id> --reason "..." instead. This flag will be removed in v5.0.`
2. Map to the new interface internally: `--skip-gate spec-fidelity` → `--gate-override spec-fidelity --reason "legacy flag migration"`
3. The override reason "legacy flag migration" is auto-generated and DOES satisfy the 10-character minimum
4. Record the mapping in the audit trail with `actor = "deprecation_shim"`

### R7: Audit Trail and Compliance (P1)

Every gate evaluation produces an auditable record.

**Audit record schema**:
```python
@dataclass
class GateAuditRecord:
    run_id: str                     # pipeline run identifier
    checkpoint_id: str              # unique per scope evaluation
    gate_id: str
    scope: Literal["task", "milestone", "release"]
    profile: str
    enforcement_level: EnforcementLevel
    evaluation_started_utc: datetime
    evaluation_completed_utc: datetime
    result: Literal["passed", "soft_failed", "hard_failed", "skipped", "timed_out"]
    failure_reason: str | None
    override_applied: bool
    override_reason: str | None
    override_actor: str | None
    artifact_sha256: str | None     # hash of the artifact evaluated
    gate_output_sha256: str | None  # hash of the gate's output
```

**Audit trail guarantees**:
- Audit records are append-only — records MUST NOT be modified or deleted after creation
- Audit trail is stored in `{pipeline_output_dir}/.gate-audit/audit.jsonl` (one JSON object per line)
- The audit trail MUST survive pipeline failures — records are flushed to disk after each gate evaluation, not batched
- Audit trail integrity: the file includes a running SHA-256 chain hash. Each record's `chain_hash` field = SHA-256(`previous_chain_hash` + `json(current_record)`). First record uses `chain_hash = SHA-256("genesis")`.

### R8: Cross-Gate Dependency Resolution (P2)

Some gates produce outputs that other gates consume.

**Known dependency chains**:
1. `WIRING_GATE` → `SPEC_FIDELITY_GATE`: Wiring verification findings inform whether spec fidelity is achievable
2. `SPEC_FIDELITY_GATE` → `RELEASE_GATE`: Spec fidelity is a precondition for release approval
3. `ANTI_INSTINCT_GATE` → `TRAILING_GATE`: Anti-instinct findings feed into trailing gate analysis

**Data passing mechanism**: Gate outputs are written to `{checkpoint_dir}/{gate_id}/output/`. Dependent gates read from predecessor output directories. No in-memory data passing — all inter-gate communication is via filesystem artifacts.

**Staleness detection**: When gate B depends on gate A, gate B MUST verify that gate A's output was produced during the CURRENT pipeline run by checking `run_id` in the output metadata. Stale outputs from previous runs MUST be rejected with `failure_reason = "stale_dependency_output: {gate_a_id} output from run {old_run_id}, current run {current_run_id}"`.

## 3. Interface Contracts

### 3.1 GateRegistry API

```python
class GateRegistry:
    def register(self, entry: GateRegistryEntry) -> None:
        """Register a gate. Raises GateConfigurationError on duplicate gate_id
        or circular dependency."""

    def evaluate_checkpoint(
        self,
        scope: Literal["task", "milestone", "release"],
        profile: str,
        context: EvaluationContext,
    ) -> GateEvaluationResult:
        """Evaluate all registered gates for the given scope and profile."""

    def get_gate(self, gate_id: str) -> GateRegistryEntry | None:
        """Return gate entry or None if not registered."""

    def list_gates(
        self,
        scope: Literal["task", "milestone", "release"] | None = None,
    ) -> list[GateRegistryEntry]:
        """List gates, optionally filtered by scope. Returns in evaluation order."""
```

### 3.2 Enforcement Level Enum

```python
class EnforcementLevel(Enum):
    OFF = "off"           # gate is not evaluated
    SHADOW = "shadow"     # evaluate and log, no effect on pipeline
    SOFT = "soft"         # evaluate, warn on failure, record in DeferredRemediationLog
    HARD = "hard"         # evaluate, block on failure
```

**Profile × Level matrix** (defines the enforcement level for each gate in each profile):

| Gate | strict | standard | legacy_migration |
|------|--------|----------|-----------------|
| spec-fidelity | HARD | HARD | SOFT |
| deviation-analysis | HARD | HARD | SHADOW |
| wiring-verification | HARD | SOFT | SHADOW |
| anti-instinct | HARD | SOFT | OFF |
| smoke-test | HARD | HARD | SOFT |
| trailing-gate | HARD | SOFT | SHADOW |
| release-gate | HARD | HARD | SOFT |

**Invariant**: The `strict` profile MUST have ALL gates set to `HARD`. No gate in the `strict` profile may have enforcement level `OFF`, `SHADOW`, or `SOFT`. This invariant is checked at registry load time.

## 4. Error Handling

### 4.1 Gate Evaluation Errors

| Error | Classification | Behavior |
|-------|---------------|----------|
| Gate raises exception | `hard_fail` | Record exception traceback in audit; treat as failure |
| Gate exceeds `timeout_seconds` | `hard_fail` | Kill evaluation; record timeout in audit |
| Gate dependency not registered | `GateConfigurationError` | Pipeline refuses to start |
| Gate output directory not writable | `hard_fail` | Record I/O error; gate cannot produce output |
| Circular gate dependency detected | `GateConfigurationError` | Pipeline refuses to start |
| Profile name not recognized | `GateConfigurationError` | Pipeline refuses to start |
| Override attempted on `strict` profile | `OverrideProhibitedError` | Override rejected; pipeline continues WITHOUT the override |

### 4.2 Recovery Semantics

When a gate fails in `evaluate_all` mode:
1. Record failure in audit trail immediately
2. Continue evaluating subsequent gates
3. After all gates complete, aggregate results
4. If ANY hard failures exist → checkpoint fails
5. If ONLY soft failures exist → checkpoint passes with warnings
6. Soft failures are recorded in `DeferredRemediationLog`

**Critical**: In `evaluate_all` mode, a gate that depends on a failed gate is SKIPPED, not evaluated. This prevents cascading failures where gate B produces a misleading result because gate A's output is missing.

## 5. Migration Path

### 5.1 Phase 1: Registry (this release, first deliverable)
- Implement `GateRegistry` and `GateRegistryEntry`
- Register all 7 existing gates
- Existing gate evaluation logic continues to work — registry is additive
- No behavioral changes to pipeline

### 5.2 Phase 2: Profiles (this release, second deliverable)
- Implement enforcement profiles
- Wire profile selection into pipeline configuration
- Default profile: `standard`
- Existing `--skip-*` flags continue to work via deprecation shim

### 5.3 Phase 3: Unified Evaluation (this release, third deliverable)
- Replace per-gate evaluation with `evaluate_checkpoint()` calls
- Implement evaluation modes (`fail_fast`, `evaluate_all`)
- Wire audit trail and `DeferredRemediationLog`

### 5.4 Phase 4: Rollback and Resume (this release, fourth deliverable)
- Implement artifact classification on failure
- Implement `--resume-from` mechanism
- Implement SHA-256 artifact verification

**Delivery order is strict**: Phase N depends on Phase N-1. Phases MUST NOT be parallelized. Phase 1 must be code-complete and passing all tests before Phase 2 implementation begins. This is a hard constraint because Phase 2 consumes Phase 1's registry API, and premature parallelization in the sprint-executor-timeout release (INC-052) caused exactly this kind of integration failure.

## 6. Testing Strategy

### 6.1 Invariant Tests

- Strict profile invariant: all gates HARD
- Override prohibition in strict: programmatic attempts to override must fail
- Release scope override prohibition in standard: attempts must fail
- Circular dependency detection at load time
- Evaluation order determinism across 100 randomized runs
- DeferredRemediationLog ratchet: release gate MUST fail with unresolved entries

### 6.2 Profile Behavior Tests

For EACH of the 3 profiles:
- Gate failure at task scope → correct behavior per profile
- Gate failure at milestone scope → correct behavior per profile
- Gate failure at release scope → correct behavior per profile

This produces 9 test cases (3 profiles × 3 scopes), each with distinct expected behavior.

### 6.3 Incident Regression

- INC-041 (DEVIATION_ANALYSIS_GATE never wired): Registry MUST reject a registered gate with no evaluation path
- INC-047 (gate skipped silently): Audit trail MUST record all evaluations including skipped gates
- Override without reason: MUST be rejected with specific error message

## 7. Non-Functional Requirements

- Gate registry load time: < 100ms for 20 registered gates
- Checkpoint evaluation overhead: < 200ms excluding individual gate execution time
- Audit trail write: < 5ms per record
- Chain hash computation: < 1ms per record
- DeferredRemediationLog query: < 50ms for 1000 entries
