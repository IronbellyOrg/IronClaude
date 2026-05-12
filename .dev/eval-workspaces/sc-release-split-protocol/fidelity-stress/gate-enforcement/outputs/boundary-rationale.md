# Split Boundary Rationale

## Split Point

The boundary falls between the spec's own Migration Phase 2 and Phase 3:
- **Release 1**: Phase 1 (Registry) + Phase 2 (Profiles) = R1, R2, partial R6, relevant error handling and testing
- **Release 2**: Phase 3 (Unified Evaluation) + Phase 4 (Rollback and Resume) = R3, R4, R5, remainder of R6, R7, R8, relevant error handling and testing

## Why This Boundary

1. **The spec prescribes it.** Section 5 defines 4 sequential phases with an explicit prohibition on parallelization: "Phases MUST NOT be parallelized." The boundary between Phase 2 and Phase 3 is the natural seam because Phase 3 is the first phase that CONSUMES Phase 2's output (profile-aware evaluation).

2. **Historical precedent justifies caution.** The spec cites INC-052 (sprint-executor-timeout release) as evidence that premature parallelization of dependent phases caused integration failure. A release boundary enforces this structurally.

3. **The registry API is the highest-risk design surface.** All of R3-R8 depend on the `GateRegistry` API, `GateRegistryEntry` schema, `EnforcementLevel` enum, and profile system. Validating these in production before building on top reduces compound risk.

4. **Release 1 delivers independently valuable behavioral change.** It is not scaffolding:
   - Closes the override governance gap (Section 1.2)
   - Unifies 7 inconsistent gate configurations under a single schema
   - Enforces the strict-profile invariant
   - Provides deprecation path for legacy flags

## Release 1 Delivers

**Independently testable components**:
- Central gate registry with uniform `GateRegistryEntry` schema for all 7 gates
- Deterministic evaluation ordering (by `evaluation_order`, then lexicographic `gate_id`)
- Circular dependency detection at load time
- 3 enforcement profiles with distinct override policies
- Override governance: 10-character minimum reason, strict prohibition (no bypass), release-scope prohibition in strict + standard
- Profile × Level matrix: 21 cells (7 gates × 3 profiles) with exact enforcement levels
- Strict-profile invariant enforced at registry load time
- CLI: `--profile`, `--gate-list`, `--gate-status`
- Deprecation shims for 4 legacy flags with correct warning messages and mappings
- Configuration error handling (`GateConfigurationError`, `OverrideProhibitedError`)

**Value**: After Release 1, the pipeline has a single source of truth for gate configuration, profile-based governance, and a migration path from legacy flags. This is real behavioral change, not just data model scaffolding.

## Release 2 Builds On

**Consumes from Release 1**:
- `GateRegistry` API (`register`, `get_gate`, `list_gates`) — extended with `evaluate_checkpoint()`
- `GateRegistryEntry` schema — consumed by the evaluation pipeline to determine gate ordering, dependencies, timeouts, and retry policies
- `EnforcementLevel` enum — used by the evaluation pipeline to route gate results
- Profile system — determines evaluation mode (`fail_fast` for strict, `evaluate_all` for standard/legacy_migration)
- Override governance — consumed by the CLI `--gate-override` command

**Adds**:
- Unified evaluation pipeline replacing 7 per-gate evaluation paths
- Deferred remediation with release-scope ratchet
- Artifact classification and rollback contracts
- Resume-from-checkpoint capability with SHA-256 verification
- Append-only audit trail with chain hash integrity
- Cross-gate data passing via filesystem with staleness detection

**Why it depends on Release 1 being validated first**: The evaluation pipeline's correctness depends entirely on the registry returning correct gates in correct order with correct enforcement levels. If the Profile × Level matrix has an error, or the dependency resolution has a bug, or the override governance has a bypass, every evaluation result in Release 2 would be wrong.

## Cross-Release Dependencies

| Release 2 Item | Depends On (Release 1) | Type | Risk if R1 Changes |
|----------------|----------------------|------|---------------------|
| `evaluate_checkpoint()` | `GateRegistry`, `GateRegistryEntry`, `list_gates()` | hard | Must re-verify evaluation ordering and dependency resolution |
| Evaluation mode selection | Profile system, Profile × Level matrix | hard | Wrong evaluation mode could cause false passes or false blocks |
| `DeferredRemediationLog` recording | `EnforcementLevel` (SOFT triggers deferred logging) | hard | Wrong enforcement level classification breaks remediation tracking |
| Rollback artifact classification | Checkpoint scope from registry | hard | Wrong scope assignment taints wrong artifacts |
| `--gate-override` CLI | Override governance (10-char min, profile restrictions) | hard | Must respect all override rules from Release 1 |
| `--resume-from` CLI | Audit trail (loads VALID gate results) | soft | Resume path must be compatible with audit record format |
| Cross-gate data passing | `dependencies` field in `GateRegistryEntry` | hard | Wrong dependency declarations break data flow |
| Staleness detection | `run_id` in gate output metadata | hard | Format of run_id must be consistent between releases |
| Audit trail chain hash | Gate evaluation results schema | soft | Schema changes require chain hash recalculation |
| Deprecation shim audit records | `actor = "deprecation_shim"` convention from Release 1 | soft | Actor naming must be consistent |

## Integration Points

1. **GateRegistry.evaluate_checkpoint()**: Release 2 adds this method to the Release 1 class. It must be API-compatible with existing `register()`, `get_gate()`, `list_gates()` methods.

2. **Profile-to-evaluation-mode mapping**: Release 1 defines profiles; Release 2 maps them to evaluation modes:
   - `strict` → `fail_fast`
   - `standard` → `evaluate_all`
   - `legacy_migration` → `evaluate_all`

3. **Override governance → gate-override CLI**: Release 2's `--gate-override` command must respect all Release 1 override rules (10-character minimum, strict prohibition, release-scope prohibition in strict + standard).

4. **Audit trail → resume mechanism**: Release 2's `--resume-from` loads VALID gate results from the audit trail produced during evaluation. The audit record format must be stable between Release 1 deprecation shim records and Release 2 evaluation records.

5. **GateRegistryEntry.dependencies → cross-gate data passing**: Release 2's inter-gate data passing uses the `dependencies` field defined in Release 1's `GateRegistryEntry` to determine which gate outputs to read.

## Handoff Criteria

Before Release 2 planning begins, Release 1 must demonstrate:

1. All 7 gates registered and retrievable via `get_gate()` and `list_gates()`
2. Evaluation ordering is deterministic across 100 randomized runs
3. Circular dependency detection raises `GateConfigurationError` at load time
4. All 21 cells of the Profile × Level matrix return correct enforcement levels
5. Strict-profile invariant enforced: no gate in strict has OFF, SHADOW, or SOFT
6. Override reason < 10 characters rejected with exact error message format
7. Strict profile rejects overrides via all paths (flag, env, config) at the registry level
8. Release-scope overrides rejected in strict and standard profiles
9. All 4 deprecation shims produce correct warnings and mappings
10. Gate registry loads in < 100ms for 20 gates
11. No regressions in existing pipeline behavior (registry is additive)

## Reversal Cost

If the split decision needs to be reversed (merge back to single release):

**Cost: Low.** The phases are already sequential and the boundary adds no architectural divergence. Merging requires:
1. Combining Release 1 and Release 2 specs into a single document
2. Removing the release boundary (no code changes needed)
3. Adjusting the testing strategy to run all tests in one release cycle

No code rework, no API redesign, no architectural changes. The split is purely a delivery boundary, not a technical fork.
