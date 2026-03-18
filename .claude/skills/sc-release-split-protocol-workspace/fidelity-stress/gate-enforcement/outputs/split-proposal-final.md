---
adversarial:
  agents: [opus:architect, haiku:analyzer]
  convergence_score: 0.82
  base_variant: opus:architect
  artifacts_dir: ./adversarial/
  unresolved_conflicts: 0
  fallback_mode: true
---

# Adversarial Review — Release Split Proposal

> **Warning**: Adversarial result produced via fallback path (Mode A inline analysis, not Mode B Skill invocation). Quality may be reduced compared to multi-agent variant generation. Review conclusions carefully.

## Original Proposal Summary

The Part 1 discovery analysis recommends splitting Unified Gate Enforcement v3.0 along the Phase 1-2 / Phase 3-4 boundary defined in the spec's own migration path. Release 1 would deliver the Gate Registry (R1), Enforcement Profiles (R2), and partial CLI (R6). Release 2 would deliver the Evaluation Pipeline (R3), Deferred Remediation (R4), Rollback Contract (R5), Audit Trail (R7), Cross-Gate Dependencies (R8), and remaining CLI. Confidence: 0.85.

## Advocate Position

**For splitting at the Phase 1-2 / Phase 3-4 boundary:**

1. **The spec demands it.** Section 5 explicitly states "Phases MUST NOT be parallelized" and cites INC-052 as evidence that premature parallelization caused integration failure. A split enforces this constraint at the release level, not just the implementation level.

2. **The registry API is the single largest design risk.** R3-R8 all consume the `GateRegistry` API surface. If `GateRegistryEntry`, `evaluate_checkpoint()`, or the dependency resolution semantics are wrong, everything downstream breaks. Real-world validation of R1+R2 before building R3-R8 is exactly the kind of feedback loop the release-split protocol is designed to enable.

3. **Release 1 delivers real behavioral change.** It is not scaffolding. After Release 1:
   - 7 inconsistent gate implementations are registered under a uniform schema
   - Profile selection changes pipeline behavior (strict/standard/legacy_migration)
   - The override governance gap (Section 1.2) is closed
   - Legacy flags are shimmed with deprecation warnings

4. **The cost of splitting is low.** The spec already defines 4 sequential phases. Splitting between Phase 2 and Phase 3 adds zero implementation overhead — it adds only a release boundary at a point where one naturally exists.

## Skeptic Position

**Against splitting:**

1. **Release 1 delivers a registry without an evaluation engine.** Users can register gates and select profiles, but gates still evaluate through the old per-gate mechanisms. This is an awkward intermediate state: the configuration system is unified but the execution system is not. Real-world testing of the registry without the evaluation pipeline tests only the data model, not the behavioral contract.

2. **The Profile × Level matrix is defined but not consumed.** R2 defines the 7×3 matrix (7 gates × 3 profiles), but the matrix only matters when `evaluate_checkpoint()` (R3) uses it to determine enforcement behavior. Testing the matrix in isolation tests a lookup table, not gate enforcement.

3. **R6 CLI fragmentation.** Splitting R6 across two releases creates a partial CLI in Release 1 (`--gate-list`, `--gate-status`, `--profile`) and a complete CLI in Release 2 (`--gate-override`, `--resume-from`). Users encounter an incomplete interface.

4. **The real risk is in R3-R5, not R1-R2.** The evaluation pipeline, deferred remediation ratchet, and rollback contracts are the hard engineering problems. The registry is a data structure. Splitting validates the easy part first and defers all the hard parts to Release 2.

## Pragmatist Assessment

1. **Does Release 1 enable real-world tests that couldn't happen otherwise?** Partially. Registration, circular dependency detection, profile selection, and override rejection are all independently testable and meaningful. However, the most valuable test — "does the unified evaluation pipeline correctly enforce gates across profiles and scopes?" — is deferred to Release 2. **Verdict: Marginal benefit, but non-zero.**

2. **Is the overhead of two releases justified?** Yes, because the overhead is minimal. The spec already defines 4 sequential phases with explicit ordering. A release boundary at Phase 2/3 adds only release-management cost (tagging, notes, communication), not engineering rework.

3. **Hidden coupling risks?** Low. Release 1 establishes APIs that Release 2 consumes. If Release 1's API changes after real-world feedback, Release 2 adapts before building on the wrong surface. This is the intended benefit.

4. **Blast radius if the split decision is wrong?** Low. Merging back into a single release requires only removing the release boundary — no architectural changes are needed because the phases are already sequential.

## Key Contested Points

| Point | Advocate | Skeptic | Pragmatist | Resolution |
|-------|----------|---------|------------|------------|
| Registry without evaluation = valuable? | Yes — validates API surface, closes override governance gap | Validates data model, not behavior | Marginal but non-zero; overhead is low enough to justify | SPLIT — incremental validation of foundation is worth the minimal overhead |
| Profile × Level matrix testable in isolation? | Yes — verify lookup returns correct enforcement levels per the exact matrix in Section 3.2 | Testing a lookup table, not enforcement behavior | The matrix IS the specification; validating it before building evaluation logic is sound | SPLIT — testing the specification before building its consumers is standard engineering |
| CLI fragmentation risk | Manageable with clear documentation | Creates incomplete user experience | Users are developers; partial CLI with clear docs is acceptable for a dev tool | SPLIT — acceptable for development tooling |
| Where is the real risk? | In the API design that everything depends on | In the behavioral logic (R3-R5) | Both — but sequencing them reduces compound risk | SPLIT — sequential risk reduction is the argument |

## Verdict: SPLIT

### Decision Rationale

The split aligns with the spec's own delivery sequencing, adds minimal overhead, and provides an opportunity to validate the foundation (registry + profiles) before building the complex behavioral systems (evaluation, remediation, rollback, audit) on top. The skeptic's strongest point — that Release 1 validates the data model but not behavior — is valid but does not outweigh the benefits because: (a) the registry API IS the most consequential design decision, (b) the spec itself prohibits parallelization for exactly this reason, and (c) the cost of the split is near zero.

### Strongest Argument For

The spec's own Section 5 states "Phase 2 consumes Phase 1's registry API, and premature parallelization in the sprint-executor-timeout release (INC-052) caused exactly this kind of integration failure." Splitting the release enforces this constraint structurally rather than relying on process discipline.

### Strongest Argument Against

Release 1 delivers a unified configuration system without a unified execution system. The most valuable validation — does the evaluation pipeline correctly enforce the Profile × Level matrix across all 3 profiles × 3 scopes × 7 gates? — happens only in Release 2. Release 1's real-world testing is limited to data model and configuration validation.

### Remaining Risks

1. If the registry API needs significant changes after Release 1 feedback, Release 2 implementation work done in parallel (if any) is wasted. **Mitigation**: Release 2 planning is gated on Release 1 validation.
2. Users may be confused by the partial CLI in Release 1. **Mitigation**: Document available vs. upcoming commands clearly.

### Confidence-Increasing Evidence

- If real-world testing of Release 1 reveals a registry API design flaw, this validates the split decision retroactively.
- If Release 1 deploys cleanly with no API changes needed, Release 2 can proceed with high confidence.

### Modifications

None. The original proposal's boundary at Phase 1-2 / Phase 3-4 is well-justified and aligns with the spec's own sequencing.
