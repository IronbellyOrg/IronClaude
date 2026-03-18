# Split Proposal — Unified Gate Enforcement v3.0

## Analysis Summary

The Unified Gate Enforcement v3.0 spec defines 8 requirements (R1-R8) across 4 explicitly sequenced delivery phases. The spec itself articulates a strict dependency chain: "Phase N depends on Phase N-1. Phases MUST NOT be parallelized."

## Dependency Chain Analysis

```
R1 (Gate Registry)          ← Foundation; all others depend on this
  ├── R2 (Enforcement Profiles) ← Consumes registry API; defines profile×level matrix
  │     ├── R3 (Evaluation Pipeline) ← Consumes registry + profiles; core evaluation
  │     │     ├── R4 (Deferred Remediation) ← Consumes evaluation results
  │     │     ├── R5 (Rollback Contract) ← Consumes evaluation results + checkpoint state
  │     │     ├── R7 (Audit Trail) ← Records evaluation events
  │     │     └── R8 (Cross-Gate Dependencies) ← Extends evaluation with inter-gate data passing
  │     └── R6 (CLI Interface) ← Exposes profiles + overrides to users
  └── R6 (CLI Interface) ← Also consumes registry directly for --gate-list, --gate-status
```

## Standalone Value Assessment

**Potential Release 1 (Registry + Profiles — Phases 1-2)**:
- R1: `GateRegistry`, `GateRegistryEntry`, registration, dependency validation, circular dependency detection
- R2: 3 enforcement profiles (`strict`, `standard`, `legacy_migration`), `EnforcementLevel` enum, Profile × Level matrix, override governance
- R6 (partial): `--gate-list`, `--gate-status`, `--profile` selection, deprecation shim for legacy flags
- Section 3.1: `GateRegistry` API (`register`, `get_gate`, `list_gates`)
- Section 3.2: `EnforcementLevel` enum
- Section 4.1 (partial): `GateConfigurationError` cases (duplicate gate_id, circular dependency, unrecognized profile)

This delivers independently testable value: all 7 existing gates registered with uniform schema, profile selection wired, legacy flags shimmed, and strict-profile invariant enforced.

**Potential Release 2 (Evaluation + Rollback — Phases 3-4)**:
- R3: Full evaluation pipeline (`evaluate_checkpoint`), evaluation modes (`fail_fast`, `evaluate_all`), `GateEvaluationResult`
- R4: `DeferredRemediationLog`, `RemediationEntry`, remediation ratchet at release scope
- R5: Artifact classification (`VALID`, `TAINTED`, `INVALIDATED`), rollback rules per scope, resume contract with SHA-256 verification
- R6 (remainder): `--gate-override`, `--resume-from`
- R7: `GateAuditRecord`, append-only audit trail, SHA-256 chain hash, per-record disk flush
- R8: Known dependency chains, filesystem-based data passing, staleness detection with `run_id` verification
- Section 4.2: Recovery semantics in `evaluate_all` mode

## Cost-Benefit Analysis

**Cost of splitting**:
- Two release cycles instead of one
- R6 (CLI) must be partially delivered in each release
- Integration testing of Phase 2 profile wiring must be validated before Phase 3 can begin

**Cost of NOT splitting**:
- The spec explicitly warns against parallelization (citing INC-052 as evidence of past failure)
- A single release of 900-1200 lines with 4 phases creates big-bang risk
- If the registry API is wrong, all downstream phases are built on a broken foundation
- No opportunity for real-world feedback on registry design before building evaluation logic on top

**The seam**:
The spec's own Phase 1-2 / Phase 3-4 boundary is a natural foundation-vs-application seam. Phase 1-2 establishes the registry and profile system that Phase 3-4 consumes. The spec itself says "Phase 2 consumes Phase 1's registry API" — the same applies at the release level: Release 2 consumes Release 1's registry + profiles.

## Recommendation: SPLIT

**Confidence**: 0.85

**Rationale**: The spec itself identifies a strict 4-phase sequential dependency chain and explicitly prohibits parallelization. This is a strong signal that the author intended incremental delivery. The Phase 1-2 / Phase 3-4 boundary is a natural seam where:
1. Release 1 delivers a complete, testable registry + profile system
2. Release 2 builds the evaluation, remediation, rollback, and audit systems on top
3. Real-world validation of the registry API prevents the exact integration failure (INC-052) the spec warns about

**Release 1 scope**: R1 (Gate Registry) + R2 (Enforcement Profiles) + partial R6 (CLI: profile selection, gate listing, deprecation shim) + relevant error handling + relevant testing
**Release 2 scope**: R3 (Evaluation Pipeline) + R4 (Deferred Remediation) + R5 (Rollback Contract) + remainder of R6 (CLI: override, resume) + R7 (Audit Trail) + R8 (Cross-Gate Dependencies)

## Real-World Test Plan for Release 1

1. Register all 7 existing gates with their `GateRegistryEntry` data — verify deterministic evaluation ordering across multiple runs
2. Attempt circular dependency registration — verify `GateConfigurationError` at load time
3. Select each profile and verify the Profile × Level matrix returns correct enforcement levels for all 7 gates
4. Attempt override on `strict` profile via all paths (flag, env var, config file) — verify rejection with no bypass
5. Attempt release-scope override on `standard` profile — verify prohibition
6. Use deprecated `--skip-gate`, `--skip-wiring-gate`, `--no-smoke` flags — verify deprecation warnings and correct mapping
7. Verify override reason minimum 10 characters with exact error message

## Risks of the Split

1. R6 (CLI) spans both releases — partial delivery creates intermediate state where some CLI features exist but others don't
2. Release 1 delivers registry without evaluation — users can register and inspect gates but can't run them through the new unified pipeline yet
3. The Profile × Level matrix is defined in Release 1 but only consumed by the evaluation pipeline in Release 2

**Mitigations**:
1. Document clearly which CLI features are available in Release 1 vs Release 2
2. Existing per-gate evaluation continues to work — registry is explicitly additive (Section 5.1)
3. Matrix is testable in isolation by verifying enforcement level lookups

## Justification: Release 1 Is Not Just "The Easy Work"

Release 1 is not just "register some gates." It establishes:
- The uniform interface that eliminates 7 inconsistent enforcement implementations (Section 1.1)
- Override governance that closes the audit gap (Section 1.2)
- The strict-profile invariant that is foundational to production-grade enforcement
- Profile selection that changes pipeline behavior — this is meaningful behavioral change
- Deprecation shims that allow gradual migration of existing users

Without real-world validation of these foundations, Release 2 would be building evaluation, remediation, and rollback logic on an unverified API surface.
