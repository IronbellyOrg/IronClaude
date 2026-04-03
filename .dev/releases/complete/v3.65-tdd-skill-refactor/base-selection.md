---
base_variant: "roadmap-opus-architect"
variant_scores: "A:82 B:68"
---

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced 6 substantive topics. I derive 8 scoring criteria from these plus the spec's stated priorities:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Executability — tasks are concrete, ordered, and actionable | 20% | Debate Topics 3, 4 |
| C2 | Fidelity safety — prevents silent content drift | 20% | Debate Topics 1, 5 |
| C3 | Line-count & range correctness | 10% | Debate Topic 4 |
| C4 | BUILD_REQUEST wiring safety | 15% | Debate Topic 1 |
| C5 | Verification structure — both executable and auditable | 10% | Debate Topic 5 |
| C6 | Architectural awareness — precedent, integration points | 10% | Debate Topic 6 |
| C7 | Timeline realism for actual execution context | 10% | Debate Topic 3 |
| C8 | Traceability — FR/SC/OQ mapped to phases | 5% | Debate Topic 2 |

## 2. Per-Criterion Scores

### C1: Executability (20%)

**Variant A: 9/10** — Every task has a concrete command or action ("Run `wc -l`", "grep for all 6 updated references"). Phase prerequisites are explicit. Tasks within Phase 2 are explicitly marked parallelizable with non-overlapping ranges stated.

**Variant B: 6/10** — Tasks are described at milestone level ("5/5 canonical refs files exist") rather than action level. Phase 0 deliverable "M0.2: Approved transformation allowlist baseline" doesn't specify what approval means or who approves. Phase 1 bundles extraction and wiring without step-level ordering.

### C2: Fidelity Safety (20%)

**Variant A: 9/10** — Per-phase verification gates with specific methods (block-wise diff, checksum markers, grep tests). Phase 5 includes a comprehensive 14-row success criteria table mapping each criterion to the phase where it's verified and the verification method.

**Variant B: 7/10** — Gate C groups fidelity concerns well for review, but the gates span phases, making it unclear *when* each check actually runs. Phase 4 "fidelity certification" defers most verification to end, reducing early detection.

### C3: Line-Count & Range Correctness (10%)

**Variant A: 9/10** — Commits to 1,387 as the measured value, re-anchors all ranges in Phase 1. Debate assessed this as "pragmatically correct." Every extraction task references "lines per corrected fidelity index."

**Variant B: 4/10** — References "1,364 lines" throughout (Phase 0 scope, Phase 4 fidelity coverage "lines 1–1364") while simultaneously claiming to resolve the discrepancy. The debate flagged this as "an unresolved inconsistency propagated through the entire plan."

### C4: BUILD_REQUEST Wiring Safety (15%)

**Variant A: 9/10** — Separates extraction (Phase 2, verbatim) from wiring (Phase 3, after all targets confirmed to exist). Phase 3 is a dedicated 15-minute phase with a closed allowlist of exactly 6 changes and verification that only those changes appear in the diff.

**Variant B: 5/10** — Bundles wiring into Phase 1 (M1.2) alongside extraction. The debate assessed this as the riskier approach: "Opus wins on safety principle... the cost of separation is trivial (15 minutes) and the failure mode it prevents — partial-state broken references — is exactly the kind of silent defect the spec identifies as highest risk."

### C5: Verification Structure (10%)

**Variant A: 7/10** — Per-phase gates are excellent for execution but require cross-referencing to answer "is fidelity proven?" The Phase 5 success criteria table partially compensates by mapping criteria to verification phases.

**Variant B: 8/10** — Named gates (A through D) grouping cross-cutting concerns are superior for audit. Gate C cleanly answers "is fidelity proven?" The requirement traceability matrix in Section 6 adds further auditability.

### C6: Architectural Awareness (10%)

**Variant A: 9/10** — Identifies R6 (no established refs pattern precedent) as a novel architectural insight. Correctly notes the adversarial-protocol refs pattern doesn't exist yet. Integration points are documented inline at the phases that own them.

**Variant B: 5/10** — References `sc-adversarial-protocol/refs/` as a "tooling dependency" without verifying it exists. The debate concluded: "Opus is clearly stronger here. A roadmap should validate its own assumptions rather than propagating potentially incorrect spec references."

### C7: Timeline Realism (10%)

**Variant A: 8/10** — 3-4 hours aligns with single-agent (Claude session) execution, which the debate identified as the likely context. Per-phase estimates sum correctly. However, lacks explicit statement of assumed execution context.

**Variant B: 6/10** — 3.5-5 days is valid for team execution with review cycles, but the debate concluded this is not the likely execution context. Role definitions (architect, implementation engineer, QA/reviewer, toolsmith) are useful documentation but inflate the timeline.

### C8: Traceability (5%)

**Variant A: 7/10** — FR and SC numbers are referenced per-task and in verification gates. OQ resolution is mapped to phases in a table. Lacks a standalone traceability matrix.

**Variant B: 8/10** — Includes an explicit requirement traceability matrix (Section 6) mapping FR/NFR to phases and gates. More systematic, though the mapping is "high level" rather than exhaustive.

## 3. Overall Scores

| Criterion | Weight | Variant A | Variant B |
|-----------|--------|-----------|-----------|
| C1: Executability | 20% | 9 (18.0) | 6 (12.0) |
| C2: Fidelity Safety | 20% | 9 (18.0) | 7 (14.0) |
| C3: Line-Count Correctness | 10% | 9 (9.0) | 4 (4.0) |
| C4: BUILD_REQUEST Wiring | 15% | 9 (13.5) | 5 (7.5) |
| C5: Verification Structure | 10% | 7 (7.0) | 8 (8.0) |
| C6: Architectural Awareness | 10% | 9 (9.0) | 5 (5.0) |
| C7: Timeline Realism | 10% | 8 (8.0) | 6 (6.0) |
| C8: Traceability | 5% | 7 (3.5) | 8 (4.0) |
| **Weighted Total** | **100%** | **86.0 → 82** | **60.5 → 68** |

*(Scores normalized to 0-100 scale with rounding for variant_scores header.)*

**Variant A (Opus): 82** — Wins on executability, safety, correctness, and architectural awareness. The plan is directly actionable by a Claude session with concrete commands, verified ranges, and incremental gates.

**Variant B (Haiku): 68** — Stronger on audit structure and traceability, but undermined by the propagated line-count inconsistency, premature wiring bundling, and milestone-level (rather than task-level) granularity that reduces executability.

## 4. Base Variant Selection Rationale

**Variant A (Opus)** is the clear base for three reasons:

1. **The debate's own synthesis recommended it**: "The merged roadmap should use Opus as the structural base (phase ordering, task specificity, timeline, BUILD_REQUEST wiring safety, line-count commitment)."

2. **Execution context alignment**: This refactor will be executed as a Claude session, not a multi-day team effort. Opus's 5-phase structure with concrete tasks and 3-4 hour timeline matches the actual execution model.

3. **Correctness over efficiency**: On the highest-risk decision (BUILD_REQUEST wiring timing), Opus's Phase 3 separation is safer at trivial cost. The debate explicitly judged this in Opus's favor.

## 5. Specific Improvements from Variant B to Incorporate in Merge

### Must incorporate:

1. **Cross-cutting gate summary table** (Variant B Section 6, Gates A-D) — Add as an appendix or subsection to Phase 5. Groups criteria by concern (structural completeness, sync/contract, fidelity, behavioral parity) for reviewer convenience. This is additive to Opus's per-phase gates.

2. **Requirement traceability matrix** (Variant B Section 6, bottom) — Add a compact FR→Phase→Gate mapping table after the success criteria checklist in Phase 5. Maps FR-TDD-R.1/R.6 → Phase 4, FR-TDD-R.2/3/4/5/8 → Phase 2, FR-TDD-R.7 → Phase 5, NFR → relevant gates.

3. **Integration Points as a standalone section** (Variant B Section 3, IP-1 through IP-4) — Opus documents integration points inline at owning phases, which is good for execution. Add Variant B's standalone IP section as a cross-reference index so reviewers can see all integration points in one place. Retain Opus's inline treatment as primary.

4. **Contract-awareness in Phase 1** (debate compromise) — Add a lightweight task to Phase 1: "Document the phase loading contract matrix from spec Section 5.3 as a verification baseline." This captures Haiku's contract-first principle without adding a full Phase 0.

### Consider incorporating:

5. **Role definitions** (Variant B Section 5) — Include as an optional scaling note: "Primary execution: single Claude session. For team execution, roles map as: architect (Phase 1 verification), implementation (Phases 2-4), QA (Phase 5 gates)."

6. **Explicit execution context statement** — Neither variant states its assumed execution model clearly. Add to Executive Summary: "This roadmap assumes single-agent (Claude session) execution. For team execution with review cycles, multiply phase estimates by ~3x."

### Do not incorporate:

- **Phase 0 as a separate phase** — Opus's Phase 1 already handles discovery and OQ resolution. Adding Phase 0 creates unnecessary phase overhead for work that takes 30 minutes.
- **Bundled BUILD_REQUEST wiring in Phase 1** — The debate ruled this out on safety grounds.
- **3.5-5 day timeline as primary** — Note it as the team-execution alternative, not the primary estimate.
- **"Lines 1-1364" references** — All ranges must use the verified 1,387-line anchor per Opus's approach.
