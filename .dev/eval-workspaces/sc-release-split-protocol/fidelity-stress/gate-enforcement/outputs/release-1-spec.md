---
release: 1
parent-spec: ../../evals/files/fidelity-stress-gate-enforcement.md
split-proposal: ./split-proposal-final.md
scope: "Gate Registry, Enforcement Profiles, partial CLI, configuration error handling"
status: draft
predecessor_releases:
  - wiring-verification-gate-v1.0
  - anti-instincts-v1.0
validation-gate: "N/A — this is Release 1"
---

# Release 1 — Unified Gate Registry & Enforcement Profiles

## Objective

Establish a central gate registry with uniform interface for all 7 existing pipeline gates, implement the 3-profile enforcement system (`strict`, `standard`, `legacy_migration`), wire profile selection into the pipeline, and provide deprecation shims for legacy per-gate flags. After this release, all gates are registered under a uniform schema, profiles govern enforcement levels, and override governance closes the audit gap identified in Section 1.2 of the original spec.

## Scope

### Included

1. **R1: Unified Gate Registry (P0)** — From: original-spec Section 2, R1
   - `GateRegistryEntry` dataclass with all 9 fields:
     - `gate_id: str` (unique, e.g., "spec-fidelity")
     - `gate_criteria: GateCriteria` (existing model)
     - `scope: Literal["task", "milestone", "release"]`
     - `enforcement_profile_overrides: dict[str, EnforcementLevel]` (profile → level)
     - `default_enforcement: EnforcementLevel` (used when profile doesn't specify)
     - `evaluation_order: int` (lower = earlier; ties broken by `gate_id`)
     - `dependencies: list[str]` (gate_ids that must pass before this gate runs)
     - `timeout_seconds: int` (max time for gate evaluation; default 60)
     - `retry_policy: RetryPolicy | None` (None = no retry)
   - **Evaluation order contract**: Gates evaluate in `evaluation_order` ascending. When two gates have the same `evaluation_order`, they are disambiguated by lexicographic sort of `gate_id`. This ordering is deterministic and MUST NOT vary between runs.
   - **Dependency contract**:
     - If gate A lists gate B in `dependencies`, gate B MUST complete evaluation before gate A starts
     - If gate B fails with `hard_fail`, gate A is SKIPPED (not failed) with `skip_reason = "dependency_failed: {gate_b_id}"`
     - If gate B fails with `soft_fail`, gate A still evaluates (soft failures are advisory)
     - Circular dependencies MUST be detected at registry load time and MUST raise `GateConfigurationError` — the pipeline MUST NOT start

2. **R2: Enforcement Profiles (P0)** — From: original-spec Section 2, R2
   - Three enforcement profiles: `strict`, `standard`, `legacy_migration`. Profile selection is per-pipeline-run, NOT per-gate.
   - **Profile definitions**:

     | Profile | Description | Override Policy | Gate Failure Behavior |
     |---------|-------------|----------------|----------------------|
     | `strict` | Production-grade enforcement | No overrides permitted for any gate at any scope | Hard fail on any gate failure; no continuation |
     | `standard` | Normal development enforcement | Override permitted for task and milestone scope ONLY; release scope overrides prohibited | Hard fail at release scope; soft fail with remediation log at task/milestone |
     | `legacy_migration` | Transitional profile for v1.0→v2.0 migration | Override permitted at all scopes with mandatory `override_reason` | Soft fail everywhere; all failures logged to `DeferredRemediationLog` |

   - **Override governance**:
     - Every override MUST record: `gate_id`, `scope`, `override_reason` (free text, minimum 10 characters), `overridden_by` (user identity), `timestamp_utc`
     - Overrides with `override_reason` shorter than 10 characters MUST be rejected with error: `"Override reason must be at least 10 characters (got {len}). Provide a meaningful justification."`
     - The `strict` profile MUST NOT accept overrides under ANY circumstances, including `--force` flags, environment variables, or configuration file entries. The strict profile's no-override policy is enforced at the registry level, not the CLI level — there is no code path that can bypass it.
     - Release-scope overrides are PROHIBITED in both `strict` and `standard` profiles. ONLY `legacy_migration` permits release-scope overrides.

3. **EnforcementLevel Enum** — From: original-spec Section 3.2
   ```python
   class EnforcementLevel(Enum):
       OFF = "off"           # gate is not evaluated
       SHADOW = "shadow"     # evaluate and log, no effect on pipeline
       SOFT = "soft"         # evaluate, warn on failure, record in DeferredRemediationLog
       HARD = "hard"         # evaluate, block on failure
   ```

4. **Profile × Level Matrix** — From: original-spec Section 3.2

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

5. **GateRegistry API (partial)** — From: original-spec Section 3.1
   ```python
   class GateRegistry:
       def register(self, entry: GateRegistryEntry) -> None:
           """Register a gate. Raises GateConfigurationError on duplicate gate_id
           or circular dependency."""

       def get_gate(self, gate_id: str) -> GateRegistryEntry | None:
           """Return gate entry or None if not registered."""

       def list_gates(
           self,
           scope: Literal["task", "milestone", "release"] | None = None,
       ) -> list[GateRegistryEntry]:
           """List gates, optionally filtered by scope. Returns in evaluation order."""
   ```
   Note: `evaluate_checkpoint()` is deferred to Release 2.

6. **Partial CLI Interface (R6)** — From: original-spec Section 2, R6
   ```
   superclaude pipeline --profile strict|standard|legacy_migration
   superclaude pipeline --gate-list                    # show registered gates
   superclaude pipeline --gate-status <gate-id>        # show gate config and history
   ```
   - **Deprecated flags** (emit deprecation warning for 2 releases, then remove):
     - `--skip-gate` → `--gate-override`
     - `--skip-wiring-gate` → `--gate-override wiring-verification`
     - `--no-smoke` → `--gate-override smoke-test`
     - `--strictness` → `--profile`
   - **Deprecation behavior**: When a deprecated flag is used:
     1. Emit `DEPRECATION WARNING: --skip-gate is deprecated. Use --gate-override <gate-id> --reason "..." instead. This flag will be removed in v5.0.`
     2. Map to the new interface internally: `--skip-gate spec-fidelity` → `--gate-override spec-fidelity --reason "legacy flag migration"`
     3. The override reason "legacy flag migration" is auto-generated and DOES satisfy the 10-character minimum
     4. Record the mapping in the audit trail with `actor = "deprecation_shim"`

7. **Configuration Error Handling (partial R4.1)** — From: original-spec Section 4.1

   | Error | Classification | Behavior |
   |-------|---------------|----------|
   | Gate dependency not registered | `GateConfigurationError` | Pipeline refuses to start |
   | Circular gate dependency detected | `GateConfigurationError` | Pipeline refuses to start |
   | Profile name not recognized | `GateConfigurationError` | Pipeline refuses to start |
   | Override attempted on `strict` profile | `OverrideProhibitedError` | Override rejected; pipeline continues WITHOUT the override |

8. **Migration Phase 1: Registry** — From: original-spec Section 5.1
   - Implement `GateRegistry` and `GateRegistryEntry`
   - Register all 7 existing gates
   - Existing gate evaluation logic continues to work — registry is additive
   - No behavioral changes to pipeline

9. **Migration Phase 2: Profiles** — From: original-spec Section 5.2
   - Implement enforcement profiles
   - Wire profile selection into pipeline configuration
   - Default profile: `standard`
   - Existing `--skip-*` flags continue to work via deprecation shim

10. **Invariant Tests** — From: original-spec Section 6.1
    - Strict profile invariant: all gates HARD
    - Override prohibition in strict: programmatic attempts to override must fail
    - Release scope override prohibition in standard: attempts must fail
    - Circular dependency detection at load time
    - Evaluation order determinism across 100 randomized runs

11. **Profile Behavior Tests (configuration only)** — From: original-spec Section 6.2
    - Verify profile selection returns correct enforcement levels per the matrix
    - Full 9-case profile×scope behavioral testing deferred to Release 2 (requires evaluation pipeline)

12. **Incident Regression (partial)** — From: original-spec Section 6.3
    - INC-041 (DEVIATION_ANALYSIS_GATE never wired): Registry MUST reject a registered gate with no evaluation path
    - Override without reason: MUST be rejected with specific error message: `"Override reason must be at least 10 characters (got {len}). Provide a meaningful justification."`

13. **Non-Functional Requirements (partial)** — From: original-spec Section 7
    - Gate registry load time: < 100ms for 20 registered gates
    - Note: Checkpoint evaluation overhead, audit trail write, chain hash computation, and DeferredRemediationLog query requirements are deferred to Release 2

### Excluded (assigned to Release 2)

1. `evaluate_checkpoint()` method on `GateRegistry` — Deferred to: Release 2, R3
2. R3: Gate Evaluation Pipeline — evaluation modes, `GateEvaluationResult`, evaluation sequence — Deferred to: Release 2, R3
3. R4: Deferred Remediation System — `DeferredRemediationLog`, `RemediationEntry`, remediation ratchet — Deferred to: Release 2, R4
4. R5: Rollback Contract — artifact classification, rollback rules, resume contract, SHA-256 verification — Deferred to: Release 2, R5
5. R6 remainder: `--gate-override <gate-id> --reason "..."` and `--resume-from <checkpoint-id>` CLI commands — Deferred to: Release 2, R6
6. R7: Audit Trail — `GateAuditRecord`, append-only audit trail, SHA-256 chain hash formula, per-record disk flush — Deferred to: Release 2, R7
7. R8: Cross-Gate Dependency Resolution — known dependency chains, filesystem data passing, staleness detection — Deferred to: Release 2, R8
8. Migration Phase 3: Unified Evaluation — Deferred to: Release 2
9. Migration Phase 4: Rollback and Resume — Deferred to: Release 2
10. Gate evaluation error handling (`hard_fail` on exception, timeout, I/O error) — Deferred to: Release 2, Section 4.1
11. Recovery semantics in `evaluate_all` mode — Deferred to: Release 2, Section 4.2
12. Full 9-case profile×scope behavioral tests (3 profiles × 3 scopes) — Deferred to: Release 2, Section 6.2
13. INC-047 regression (gate skipped silently → audit trail must record) — Deferred to: Release 2 (requires audit trail)
14. Checkpoint evaluation overhead: < 200ms — Deferred to: Release 2
15. Audit trail write: < 5ms per record — Deferred to: Release 2
16. Chain hash computation: < 1ms per record — Deferred to: Release 2
17. DeferredRemediationLog query: < 50ms for 1000 entries — Deferred to: Release 2

## Dependencies

### External Dependencies
- `wiring-verification-gate-v1.0` (predecessor release — must be complete)
- `anti-instincts-v1.0` (predecessor release — must be complete)
- Existing `GateCriteria` model (consumed by `GateRegistryEntry`)
- Existing per-gate evaluation logic in `roadmap/gates.py`, `audit/wiring_gate.py`, `roadmap/generator.py:418`, `sprint/smoke.py`, `pipeline/trailing_gate.py`

## Real-World Validation Requirements

1. **Gate Registration**: Register all 7 existing gates (`spec-fidelity`, `deviation-analysis`, `wiring-verification`, `anti-instinct`, `smoke-test`, `trailing-gate`, `release-gate`) with production `GateRegistryEntry` data. Verify each gate's `evaluation_order` is respected. Run 100 randomized registration orders and verify evaluation ordering is deterministic.

2. **Circular Dependency Detection**: Register gates with circular dependencies (A→B→C→A). Verify `GateConfigurationError` is raised at load time and the pipeline does not start.

3. **Profile Selection**: Run pipeline with `--profile strict`, `--profile standard`, `--profile legacy_migration`. For each profile, query each gate's enforcement level and verify against the Profile × Level matrix exactly as specified.

4. **Strict Override Prohibition**: With `--profile strict`, attempt override via:
   - CLI flag: `--gate-override spec-fidelity --reason "testing"`
   - Environment variable
   - Configuration file entry
   - Verify ALL attempts are rejected with `OverrideProhibitedError`. Verify no code path bypasses the registry-level enforcement.

5. **Override Reason Validation**: Attempt override with reason "too short" (9 characters). Verify rejection with exact error: `"Override reason must be at least 10 characters (got 9). Provide a meaningful justification."` Then attempt with "short but ok" (12 characters). Verify acceptance.

6. **Release-Scope Override Prohibition**: With `--profile standard`, attempt release-scope override. Verify rejection. With `--profile legacy_migration`, attempt release-scope override with valid reason. Verify acceptance.

7. **Deprecation Shim**: Use `--skip-gate spec-fidelity`. Verify:
   - Deprecation warning emitted: `DEPRECATION WARNING: --skip-gate is deprecated. Use --gate-override <gate-id> --reason "..." instead. This flag will be removed in v5.0.`
   - Internal mapping to `--gate-override spec-fidelity --reason "legacy flag migration"`
   - Override reason "legacy flag migration" satisfies 10-character minimum
   - Audit trail records mapping with `actor = "deprecation_shim"`
   - Repeat for `--skip-wiring-gate` → `--gate-override wiring-verification` and `--no-smoke` → `--gate-override smoke-test` and `--strictness` → `--profile`

8. **Dependency Contract Verification**: Register gate A depending on gate B. Verify gate B completes before gate A starts. (Note: full evaluation pipeline testing in Release 2; this validates the dependency metadata is stored and retrievable.)

## Success Criteria

- All 7 existing gates registered under `GateRegistryEntry` with correct schema
- `GateRegistry.register()`, `get_gate()`, `list_gates()` API operational
- All 3 enforcement profiles selectable via `--profile`
- Profile × Level matrix returns correct `EnforcementLevel` for all 21 cells (7 gates × 3 profiles)
- Strict-profile invariant checked and enforced at registry load time
- Override governance: 10-character minimum enforced, strict override prohibition enforced at registry level, release-scope prohibition enforced in strict and standard
- Deprecation shims operational for all 4 legacy flags with correct warnings and mappings
- Configuration errors (`GateConfigurationError`, `OverrideProhibitedError`) raised correctly
- Gate registry load time < 100ms for 20 registered gates
- Existing pipeline behavior unaffected (registry is additive)

## Traceability

| Release 1 Item | Original Source |
|----------------|----------------|
| GateRegistryEntry dataclass | R1, Section 2 |
| Evaluation order contract | R1, Section 2 |
| Dependency contract | R1, Section 2 |
| Circular dependency detection | R1, Section 2 |
| 3 enforcement profiles | R2, Section 2 |
| Override governance (10-char min, strict prohibition, release-scope prohibition) | R2, Section 2 |
| EnforcementLevel enum | Section 3.2 |
| Profile × Level matrix (7×3) | Section 3.2 |
| Strict-profile invariant | Section 3.2 |
| GateRegistry API (register, get_gate, list_gates) | Section 3.1 |
| CLI: --profile, --gate-list, --gate-status | R6, Section 2 |
| Deprecation shims (4 flags) | R6, Section 2 |
| Configuration errors | Section 4.1 (partial) |
| Migration Phase 1 + Phase 2 | Section 5.1, 5.2 |
| Invariant tests | Section 6.1 |
| INC-041 regression, override-without-reason regression | Section 6.3 (partial) |
| Registry load time < 100ms | Section 7 (partial) |
