---
release: 2
parent-spec: ../../evals/files/fidelity-stress-gate-enforcement.md
split-proposal: ./split-proposal-final.md
scope: "Gate Evaluation Pipeline, Deferred Remediation, Rollback Contract, Audit Trail, Cross-Gate Dependencies, remaining CLI"
status: draft
predecessor_releases:
  - wiring-verification-gate-v1.0
  - anti-instincts-v1.0
validation-gate: "blocked until R1 real-world validation passes"
---

# Release 2 — Unified Gate Evaluation, Remediation, Rollback & Audit

## Objective

Build the unified evaluation pipeline, deferred remediation system, rollback contracts, audit trail, and cross-gate dependency resolution on top of Release 1's gate registry and enforcement profiles. After this release, the pipeline has a single evaluation entry point (`evaluate_checkpoint`), complete audit trail with integrity guarantees, deferred remediation with release-scope ratchet, artifact classification on failure with resume capability, and inter-gate data passing with staleness detection.

## Scope

### Included

1. **R3: Gate Evaluation Pipeline (P0)** — From: original-spec Section 2, R3

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

   **`evaluate_checkpoint()` method on `GateRegistry`** — From: original-spec Section 3.1:
   ```python
   def evaluate_checkpoint(
       self,
       scope: Literal["task", "milestone", "release"],
       profile: str,
       context: EvaluationContext,
   ) -> GateEvaluationResult:
       """Evaluate all registered gates for the given scope and profile."""
   ```

2. **R4: Deferred Remediation System (P1)** — From: original-spec Section 2, R4

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

3. **R5: Rollback Contract (P1)** — From: original-spec Section 2, R5

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

4. **R6: Remaining CLI Interface (P1)** — From: original-spec Section 2, R6
   ```
   superclaude pipeline --gate-override <gate-id> --reason "justification text"
   superclaude pipeline --resume-from <checkpoint-id>  # resume after remediation
   ```

5. **R7: Audit Trail and Compliance (P1)** — From: original-spec Section 2, R7

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

6. **R8: Cross-Gate Dependency Resolution (P2)** — From: original-spec Section 2, R8

   **Known dependency chains**:
   1. `WIRING_GATE` → `SPEC_FIDELITY_GATE`: Wiring verification findings inform whether spec fidelity is achievable
   2. `SPEC_FIDELITY_GATE` → `RELEASE_GATE`: Spec fidelity is a precondition for release approval
   3. `ANTI_INSTINCT_GATE` → `TRAILING_GATE`: Anti-instinct findings feed into trailing gate analysis

   **Data passing mechanism**: Gate outputs are written to `{checkpoint_dir}/{gate_id}/output/`. Dependent gates read from predecessor output directories. No in-memory data passing — all inter-gate communication is via filesystem artifacts.

   **Staleness detection**: When gate B depends on gate A, gate B MUST verify that gate A's output was produced during the CURRENT pipeline run by checking `run_id` in the output metadata. Stale outputs from previous runs MUST be rejected with `failure_reason = "stale_dependency_output: {gate_a_id} output from run {old_run_id}, current run {current_run_id}"`.

7. **Gate Evaluation Error Handling (remainder of Section 4.1)** — From: original-spec Section 4.1

   | Error | Classification | Behavior |
   |-------|---------------|----------|
   | Gate raises exception | `hard_fail` | Record exception traceback in audit; treat as failure |
   | Gate exceeds `timeout_seconds` | `hard_fail` | Kill evaluation; record timeout in audit |
   | Gate output directory not writable | `hard_fail` | Record I/O error; gate cannot produce output |

8. **Recovery Semantics (Section 4.2)** — From: original-spec Section 4.2

   When a gate fails in `evaluate_all` mode:
   1. Record failure in audit trail immediately
   2. Continue evaluating subsequent gates
   3. After all gates complete, aggregate results
   4. If ANY hard failures exist → checkpoint fails
   5. If ONLY soft failures exist → checkpoint passes with warnings
   6. Soft failures are recorded in `DeferredRemediationLog`

   **Critical**: In `evaluate_all` mode, a gate that depends on a failed gate is SKIPPED, not evaluated. This prevents cascading failures where gate B produces a misleading result because gate A's output is missing.

9. **Migration Phase 3: Unified Evaluation** — From: original-spec Section 5.3
   - Replace per-gate evaluation with `evaluate_checkpoint()` calls
   - Implement evaluation modes (`fail_fast`, `evaluate_all`)
   - Wire audit trail and `DeferredRemediationLog`

10. **Migration Phase 4: Rollback and Resume** — From: original-spec Section 5.4
    - Implement artifact classification on failure
    - Implement `--resume-from` mechanism
    - Implement SHA-256 artifact verification

11. **Delivery order constraint** — From: original-spec Section 5
    Delivery order is strict: Phase N depends on Phase N-1. Phases MUST NOT be parallelized. Phase 3 must be code-complete and passing all tests before Phase 4 implementation begins. This is a hard constraint because Phase 4 (rollback/resume) consumes Phase 3's evaluation pipeline, and premature parallelization in the sprint-executor-timeout release (INC-052) caused exactly this kind of integration failure.

12. **Profile Behavior Tests (full 9-case matrix)** — From: original-spec Section 6.2
    For EACH of the 3 profiles:
    - Gate failure at task scope → correct behavior per profile
    - Gate failure at milestone scope → correct behavior per profile
    - Gate failure at release scope → correct behavior per profile
    This produces 9 test cases (3 profiles × 3 scopes), each with distinct expected behavior.

13. **Incident Regression (remainder)** — From: original-spec Section 6.3
    - INC-047 (gate skipped silently): Audit trail MUST record all evaluations including skipped gates

14. **DeferredRemediationLog ratchet test** — From: original-spec Section 6.1
    - Release gate MUST fail with unresolved entries

15. **Non-Functional Requirements (remainder)** — From: original-spec Section 7
    - Checkpoint evaluation overhead: < 200ms excluding individual gate execution time
    - Audit trail write: < 5ms per record
    - Chain hash computation: < 1ms per record
    - DeferredRemediationLog query: < 50ms for 1000 entries

### Excluded (delivered in Release 1)

1. `GateRegistry`, `GateRegistryEntry`, registration API — Delivered in: Release 1, R1
2. Enforcement profiles and profile selection — Delivered in: Release 1, R2
3. `EnforcementLevel` enum — Delivered in: Release 1, Section 3.2
4. Profile × Level matrix — Delivered in: Release 1, Section 3.2
5. Override governance (10-char minimum, strict prohibition, release-scope prohibition) — Delivered in: Release 1, R2
6. CLI: `--profile`, `--gate-list`, `--gate-status` — Delivered in: Release 1, R6
7. Deprecation shims for legacy flags — Delivered in: Release 1, R6
8. Configuration errors (`GateConfigurationError`, `OverrideProhibitedError`) — Delivered in: Release 1, Section 4.1
9. Strict-profile invariant — Delivered in: Release 1, R2
10. Gate registry load time < 100ms — Delivered in: Release 1, Section 7

## Dependencies

### Prerequisites (from Release 1)

- `GateRegistry` class with `register()`, `get_gate()`, `list_gates()` methods operational
- All 7 gates registered with correct `GateRegistryEntry` data
- All 3 enforcement profiles implemented and selectable via `--profile`
- Profile × Level matrix returning correct `EnforcementLevel` for all 21 cells
- Override governance operational (10-char minimum, strict prohibition, release-scope prohibition)
- `EnforcementLevel` enum available
- Configuration error handling operational

### External Dependencies

- `wiring-verification-gate-v1.0` (predecessor release — must be complete)
- `anti-instincts-v1.0` (predecessor release — must be complete)
- Existing gate evaluation logic in `roadmap/gates.py`, `audit/wiring_gate.py`, `roadmap/generator.py:418`, `sprint/smoke.py`, `pipeline/trailing_gate.py`

## Real-World Validation Requirements

1. **Full Evaluation Pipeline**: Run `evaluate_checkpoint()` at task, milestone, and release scope with each of the 3 profiles. Verify behavior matches the 9-case matrix:
   - `strict` + task scope: hard fail, no continuation
   - `strict` + milestone scope: hard fail, no continuation
   - `strict` + release scope: hard fail, no continuation
   - `standard` + task scope: soft fail with remediation log
   - `standard` + milestone scope: soft fail with remediation log
   - `standard` + release scope: hard fail
   - `legacy_migration` + task scope: soft fail, logged to `DeferredRemediationLog`
   - `legacy_migration` + milestone scope: soft fail, logged to `DeferredRemediationLog`
   - `legacy_migration` + release scope: soft fail, logged to `DeferredRemediationLog`

2. **Fail-Fast vs Evaluate-All**: With 3 gates where gate 2 fails:
   - `fail_fast` mode: verify only gates 1 and 2 evaluated, gate 3 not evaluated
   - `evaluate_all` mode: verify all 3 gates evaluated, failure recorded, dependent gates SKIPPED (not evaluated)

3. **Deferred Remediation Ratchet**: At task scope, accumulate 3 soft failures in `DeferredRemediationLog`. Then run release-scope evaluation. Verify release gate fails with `failure_reason = "unresolved_deferred_remediations: 3"`. Resolve 2 of 3, re-run release evaluation. Verify still fails with count 1. Resolve the last one (with non-empty `remediation_evidence`). Verify release gate passes.

4. **Remediation Resolution Completeness**: Attempt to mark a remediation entry as resolved with `remediated == True` but `remediation_evidence` as None or empty string. Verify this does NOT count as resolved.

5. **Rollback Classification**: Trigger gate failure at each scope level and verify artifact classification:
   - Task-scope failure: only failing task artifacts TAINTED, other tasks VALID
   - Milestone-scope failure: all milestone artifacts TAINTED, predecessor milestones VALID
   - Release-scope failure: all artifacts TAINTED unless independently validated by a passed gate

6. **Resume from Checkpoint**: After task-scope gate failure, remediate and use `--resume-from {checkpoint_id}`. Verify:
   - Only TAINTED and INVALIDATED artifacts re-evaluated
   - VALID artifacts loaded from audit trail without re-running
   - SHA-256 comparison catches modified "valid" artifacts and reclassifies as TAINTED

7. **Audit Trail Integrity**: Run a pipeline with 5 gate evaluations. Verify:
   - `{pipeline_output_dir}/.gate-audit/audit.jsonl` exists with 5 records
   - Each record is one JSON object per line
   - Records are append-only
   - Chain hash: first record's `chain_hash` = SHA-256("genesis"), subsequent records' `chain_hash` = SHA-256(`previous_chain_hash` + `json(current_record)`)
   - Kill pipeline mid-evaluation, verify previously-flushed records survive (per-record flush, not batched)

8. **Cross-Gate Data Passing**: Trigger `WIRING_GATE` → `SPEC_FIDELITY_GATE` dependency chain. Verify:
   - Wiring gate output written to `{checkpoint_dir}/wiring-verification/output/`
   - Spec fidelity gate reads from wiring gate's output directory
   - No in-memory data passing occurs

9. **Staleness Detection**: Run pipeline producing gate A output with run_id "run-001". Start new pipeline run "run-002" that skips gate A. When gate B (depending on A) runs, verify it rejects gate A's stale output with `failure_reason = "stale_dependency_output: {gate_a_id} output from run run-001, current run run-002"`.

10. **Timeout Handling**: Register a gate with `timeout_seconds = 1` and an evaluation that takes 5 seconds. Verify evaluation is killed and result is `hard_fail` with `failure_reason = "evaluation_timeout"`.

## Success Criteria

- `evaluate_checkpoint()` operational for all 3 scopes × 3 profiles
- Both evaluation modes (`fail_fast`, `evaluate_all`) behave correctly
- `DeferredRemediationLog` records soft failures and overridden hard failures
- Remediation ratchet enforced: release gate fails with unresolved remediations
- Artifact classification (VALID/TAINTED/INVALIDATED) correct for all scope levels
- Resume mechanism re-evaluates only tainted/invalidated artifacts
- SHA-256 verification catches modified "valid" artifacts
- Audit trail is append-only, survives failures, and has valid chain hash
- Cross-gate data passing via filesystem with staleness detection
- All non-functional performance requirements met
- Full 9-case profile×scope behavioral test matrix passes
- INC-047 regression: audit trail records skipped gates

## Planning Gate

> This release's roadmap and tasklist generation may proceed only after Release 1
> has passed real-world validation and the results have been reviewed.
>
> **Validation criteria**: Release 1 must demonstrate:
> - All 7 gates registered with correct schema
> - All 3 profiles selectable and returning correct enforcement levels per the Profile × Level matrix
> - Override governance enforced (10-char minimum, strict prohibition, release-scope prohibition)
> - Deprecation shims operational for all 4 legacy flags
> - Configuration errors raised correctly
> - Gate registry load time < 100ms for 20 registered gates
>
> **Review process**: Engineering lead reviews Release 1 validation results and confirms the registry API surface is stable. Any API changes must be documented before Release 2 planning begins.
>
> **If validation fails**: Revise Release 1 to address failures. Do NOT begin Release 2 implementation on a broken foundation. If the registry API requires fundamental redesign, reconsider whether merging back to a single release is more appropriate.

## Traceability

| Release 2 Item | Original Source |
|----------------|----------------|
| evaluate_checkpoint() method | R3, Section 2 / Section 3.1 |
| Evaluation modes (fail_fast, evaluate_all) | R3, Section 2 |
| Evaluation sequence (5-step) | R3, Section 2 |
| GateEvaluationResult schema | R3, Section 2 |
| Timeout handling (failure_reason = "evaluation_timeout") | R3, Section 2 |
| DeferredRemediationLog + RemediationEntry | R4, Section 2 |
| Remediation enforcement contract (ratchet) | R4, Section 2 |
| Resolved definition (remediated + non-empty evidence) | R4, Section 2 |
| Release gate failure message ("unresolved_deferred_remediations: {count}") | R4, Section 2 |
| Artifact classification (VALID/TAINTED/INVALIDATED) | R5, Section 2 |
| Rollback rules per scope | R5, Section 2 |
| Resume contract (--resume-from, SHA-256 verification) | R5, Section 2 |
| CLI: --gate-override, --resume-from | R6, Section 2 |
| GateAuditRecord schema (15 fields) | R7, Section 2 |
| Audit trail storage (audit.jsonl, append-only, per-record flush) | R7, Section 2 |
| Chain hash formula: SHA-256(previous_chain_hash + json(current_record)), genesis = SHA-256("genesis") | R7, Section 2 |
| Known dependency chains (3 chains) | R8, Section 2 |
| Filesystem data passing ({checkpoint_dir}/{gate_id}/output/) | R8, Section 2 |
| Staleness detection (run_id verification, exact failure_reason format) | R8, Section 2 |
| Gate evaluation errors (exception → hard_fail, timeout → hard_fail, I/O → hard_fail) | Section 4.1 |
| Recovery semantics in evaluate_all mode (6-step, skipped-not-evaluated for failed dependencies) | Section 4.2 |
| Migration Phase 3 + Phase 4 | Section 5.3, 5.4 |
| Delivery order constraint (INC-052 reference) | Section 5 |
| 9-case profile×scope behavioral tests | Section 6.2 |
| INC-047 regression | Section 6.3 |
| DeferredRemediationLog ratchet test | Section 6.1 |
| Checkpoint evaluation overhead < 200ms | Section 7 |
| Audit trail write < 5ms per record | Section 7 |
| Chain hash computation < 1ms per record | Section 7 |
| DeferredRemediationLog query < 50ms for 1000 entries | Section 7 |
