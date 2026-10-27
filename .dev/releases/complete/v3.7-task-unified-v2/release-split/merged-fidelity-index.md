# Merged Fidelity Index — v3.7 Release Split Verification

**Date**: 2026-04-02
**Method**: Parallel independent audits (R1 agent + R2 agent), merged with cross-validation

---

## Consolidated Section Coverage

Every section of the original spec must be covered by exactly one of: R1, R2, or DEFERRED. Sections may be PARTIAL in both R1 and R2 if they contain cross-domain content.

| Section | Subsection | R1 Status | R1 Fid | R2 Status | R2 Fid | Combined | Gap? |
|---------|-----------|-----------|--------|-----------|--------|----------|------|
| **1** | Executive Summary | PRESENT | 0.85 | PARTIAL | 0.80 | COVERED | No |
| 1 | Scope Boundaries (In) | PRESENT | 0.90 | PRESENT | 0.90 | COVERED | No |
| 1 | Scope Boundaries (Deferred) | PRESENT | 0.95 | PRESENT | 0.95 | COVERED | No |
| **2.1** | Checkpoint Failure | ABSENT | -- | N/A | -- | **GAP** | **Yes** |
| **2.2** | TUI Information Gap | N/A | -- | PARTIAL | 0.60 | **WEAK** | **Yes** |
| **2.3** | Naming Confusion | ABSENT | -- | N/A | -- | **GAP** | **Yes** |
| **3.1** | Checkpoint Architecture | PARTIAL | 0.60 | N/A | -- | **WEAK** | **Yes** |
| 3.2 | TUI v2 Architecture | N/A | -- | PRESENT | 0.90 | COVERED | No |
| 3.2 | Critical Invariants | N/A | -- | PRESENT | 1.00 | COVERED | No |
| 3.2 | Haiku Pipeline | N/A | -- | PRESENT | 0.95 | COVERED | No |
| 3.3 | Naming Architecture | PARTIAL | 0.75 | N/A | -- | COVERED | No |
| **4.1** | Phase 1 (W1) | PRESENT | 0.70 | N/A | -- | COVERED | No |
| 4.1 | Phase 2 (W2) | PRESENT | 0.70 | N/A | -- | COVERED | No |
| 4.1 | Phase 3 (W3) | PRESENT | 0.70 | N/A | -- | COVERED | No |
| 4.1 | Phase 4 (W4) | N/A | -- | N/A | -- | DEFERRED | No |
| **4.1** | End-of-Phase Checkpoints | ABSENT | -- | N/A | -- | **GAP** | **Yes** |
| 4.2 | TUI Waves Overview | N/A | -- | PRESENT | 0.85 | COVERED | No |
| 4.2 | Wave 1 (Data+Monitor) | N/A | -- | PRESENT | 0.90 | COVERED | No |
| 4.2 | Wave 2 (Rendering) | N/A | -- | PRESENT | 0.90 | COVERED | No |
| 4.2 | Wave 3 (Summary) | N/A | -- | PRESENT | 0.90 | COVERED | No |
| 4.2 | Wave 4 (Tmux) | N/A | -- | PRESENT | 0.90 | COVERED | No |
| 4.2 | Per-Feature Specs (F1-F10) | N/A | -- | PARTIAL | 0.75 | COVERED | No |
| 4.3 | Naming Tasks (N1-N12) | PRESENT | 0.90 | N/A | -- | COVERED | No |
| **5.1** | Checkpoint <-> TUI | N/A | -- | PARTIAL | 0.70 | COVERED | No |
| 5.2 | Naming <-> Checkpoint | PRESENT | 0.80 | N/A | -- | COVERED | No |
| 5.3 | Naming <-> TUI | N/A | -- | PARTIAL | 0.50 | **WEAK** | **Yes** |
| 5.4 | PASS_MISSING_CHECKPOINT Display | N/A | -- | PRESENT | 0.85 | COVERED | No |
| 5.5 | Shared File Conflict Map | PARTIAL | 0.50 | PARTIAL | 0.50 | **WEAK** | **Yes** |
| **6.1** | Shared File Modifications | PARTIAL | 0.40 | ABSENT | -- | **GAP** | **Yes** |
| 6.2 | Implementation Order | PRESENT | 0.75 | PARTIAL | 0.60 | COVERED | No |
| 6.3 | Haiku Conventions | N/A | -- | PRESENT | 0.90 | COVERED | No |
| **6.4** | Post-Phase Hook Ordering | PARTIAL | 0.30 | PRESENT | 0.90 | COVERED | No |
| 6.5 | Token Display Helper | N/A | -- | PRESENT | 0.85 | COVERED | No |
| 7.1 | MonitorState Fields | N/A | -- | PRESENT | 0.95 | COVERED | No |
| 7.2 | PhaseResult Fields | N/A | -- | PRESENT | 0.95 | COVERED | No |
| 7.3 | SprintResult Properties | N/A | -- | PRESENT | 0.95 | COVERED | No |
| 7.4 | SprintConfig Fields | PARTIAL | 0.80 | PARTIAL | 0.80 | COVERED | No |
| 7.5 | PhaseStatus Enum | PRESENT | 0.85 | N/A | -- | COVERED | No |
| 7.6 | New Dataclasses | PARTIAL | 0.75 | PARTIAL | 0.70 | COVERED | No |
| 7.7 | SprintTUI Field | N/A | -- | PRESENT | 0.95 | COVERED | No |
| 8.1 | Checkpoint Files | PRESENT | 0.95 | N/A | -- | COVERED | No |
| 8.2 | TUI Files | N/A | -- | PRESENT | 0.95 | COVERED | No |
| 8.3 | Naming Files | PRESENT | 0.90 | N/A | -- | COVERED | No |
| **8.4** | Cross-Domain Conflict Map | ABSENT | -- | ABSENT | -- | **GAP** | **Yes** |
| 8.5 | Output Artifacts | PARTIAL | 0.50 | PRESENT | 0.90 | COVERED | No |
| 8 | Test Files | PRESENT | 0.85 | PRESENT | 0.85 | COVERED | No |
| **9.1** | Combined Timeline | PRESENT | 0.85 | ABSENT | -- | **PARTIAL** | **Yes** |
| 9.2 | Gate Progression | PRESENT | 0.80 | N/A | -- | COVERED | No |
| 9.3 | Backward Compatibility | PRESENT | 0.90 | PARTIAL | 0.50 | COVERED | No |
| 10.1 | Checkpoint Risks | PRESENT | 0.85 | N/A | -- | COVERED | No |
| 10.2 | TUI Risks | N/A | -- | PRESENT | 0.90 | COVERED | No |
| 10.3 | Naming Risks | PRESENT | 0.90 | N/A | -- | COVERED | No |
| 11.1 | Checkpoint Metrics | PRESENT | 0.90 | N/A | -- | COVERED | No |
| 11.2 | TUI Metrics | N/A | -- | PRESENT | 0.90 | COVERED | No |
| 11.3 | Naming Metrics | PRESENT | 0.90 | N/A | -- | COVERED | No |
| **12.1** | Existing Tests Updates | ABSENT | -- | PRESENT | 0.85 | COVERED | No |
| 12.2 | New Tests Required | PARTIAL | 0.60 | PRESENT | 0.90 | COVERED | No |
| **12.3** | Tests Unchanged | ABSENT | -- | ABSENT | -- | **GAP** | **Yes** |
| **12.4** | Test Coverage Targets | ABSENT | -- | ABSENT | -- | **GAP** | **Yes** |
| 12.5 | Verification Methods | ABSENT | -- | N/A | -- | **GAP** | **Yes** |
| 12.6 | Test Tasks Added | PRESENT | 0.80 | N/A | -- | COVERED | No |
| 13.1 | SprintConfig Additions | PARTIAL | 0.70 | PARTIAL | 0.70 | COVERED | No |
| **13.2** | Gate Mode Behavior | PARTIAL | 0.65 | N/A | -- | **WEAK** | **Yes** |
| 13.3 | CLI Additions | PRESENT | 0.85 | N/A | -- | COVERED | No |
| 13.4 | No TUI CLI Flags | N/A | -- | ABSENT | -- | **MINOR** | Yes |
| **14.1** | Checkpoint Open Questions | PRESENT | 0.85 | N/A | -- | COVERED | No |
| 14.2 | TUI Open Questions | N/A | -- | PRESENT | 0.85 | COVERED | No |
| 14.3 | Naming Open Questions | PRESENT | 0.90 | N/A | -- | COVERED | No |
| **14.4** | Confidence Assessment | ABSENT | -- | ABSENT | -- | **GAP** | **Yes** |
| 15-A | Adversarial Analysis | ABSENT | -- | N/A | -- | **GAP** | **Yes** |
| **15-B** | UI Layout Mockups | N/A | -- | ABSENT | -- | **GAP** | **Yes** |
| 15-C | Integration Map | ABSENT | -- | N/A | -- | **GAP** | **Yes** |
| 15-D | Source Document Index | ABSENT | -- | ABSENT | -- | **GAP** | **Yes** |

---

## Gap Summary

### Sections Missing from BOTH Specs (true gaps)

| # | Section | Should Be In | Severity | Impact |
|---|---------|-------------|----------|--------|
| 1 | **8.4 Cross-Domain Conflict Map** | Both (R1 portion + R2 portion) | Medium | Implementers of both releases modify executor.py. Without the conflict map, they lack guidance on which wave/feature modifies which code location. |
| 2 | **12.3 Tests Confirmed Unchanged** | Both | Low | Useful for implementer confidence but not blocking. |
| 3 | **12.4 Test Coverage Targets** | Both (R1: >90% checkpoints.py; R2: >80% summarizer/retrospective, >90% MonitorState) | Medium | Quality bar not established in either spec. |
| 4 | **14.4 Confidence Assessment** | R1 (primary), R2 (summary) | Medium | T03.03 (auto-recovery) at 75% is the highest-risk task. This risk signal is lost. |
| 5 | **15-D Source Document Index** | Both | Low | 9 source documents not referenced. Parent-spec backlinks partially compensate. |

### Sections Missing from R1 Only (R1 gaps)

| # | Section | Severity | Impact |
|---|---------|----------|--------|
| 6 | **2.1 Problem Statement (Checkpoint)** | Medium | Root cause analysis and triple failure chain context absent. Implementers lack motivation framing. |
| 7 | **2.3 Problem Statement (Naming)** | Low-Medium | Naming collision table and occurrence counts absent. |
| 8 | **4.1 End-of-Phase Checkpoints** | Medium | Checkpoint report paths and verification criteria for each phase absent. |
| 9 | **3.1 Architecture detail** (fidelity 0.60) | Medium | Solution-to-root-cause matrix, shared module design decision missing. |
| 10 | **12.5 Verification Methods** | Low-Medium | Per-task verification method table (16 rows) absent. |
| 11 | **15-A Adversarial Analysis** | Low | Architectural justification for complementary solutions. |
| 12 | **15-C Integration Map** | Low-Medium | Failure path trace and integration point map. |
| 13 | **6.1 Shared File Modifications** (fidelity 0.40) | Low | Multi-wave executor.py coordination guidance. |

### Sections Missing from R2 Only (R2 gaps)

| # | Section | Severity | Impact |
|---|---------|----------|--------|
| 14 | **15-B UI Layout Mockups** | **HIGH** | The ASCII mockups (active sprint, sprint complete, sprint halted, tmux 3-pane) are the PRIMARY visual reference for TUI implementation. Most critical gap in either spec. |
| 15 | **9.1 Timeline** (for R2 portion) | Medium | No wave-by-wave delivery estimate for TUI work. |
| 16 | **2.2 Problem Statement (TUI)** (fidelity 0.60) | Medium | Current-vs-target 7-dimension table absent. |
| 17 | **9.3 Backward Compatibility** (fidelity 0.50) | Medium | Missing explicit "all changes additive" guarantee. |

### Sections With Low Fidelity (below 0.70) in Their Assigned Spec

| # | Section | Spec | Fidelity | Issue |
|---|---------|------|----------|-------|
| 18 | 6.4 Post-Phase Hook Ordering | R1 | 0.30 | No hook ordering or 5s timeout in R1 (covered well in R2) |
| 19 | 6.1 Shared File Modifications | R1 | 0.40 | No multi-wave coordination guidance |
| 20 | 5.5 Shared File Conflict Analysis | R1 | 0.50 | Partial conflict awareness only |
| 21 | 5.5 Shared File Conflict Analysis | R2 | 0.50 | No file-level conflict table |
| 22 | 5.3 Naming <-> TUI | R2 | 0.50 | Prompt string contract dependency underexplained |
| 23 | 9.3 Backward Compatibility | R2 | 0.50 | Missing "all changes additive" statement |
| 24 | 8.5 Output Artifacts | R1 | 0.50 | manifest.json not listed as output artifact |
| 25 | 12.2 New Tests Required | R1 | 0.60 | Test scope descriptions absent |
| 26 | 2.2 TUI Information Gap | R2 | 0.60 | No dedicated problem statement |
| 27 | 3.1 Checkpoint Architecture | R1 | 0.60 | Solution matrices and shared module design absent |

---

## Aggregate Statistics

| Metric | R1 | R2 | Combined |
|--------|----|----|----------|
| Sections assessed | 56 | 55 | 68 unique |
| PRESENT | 24 | 22 | -- |
| PARTIAL | 11 | 11 | -- |
| ABSENT (should be present) | 11 | 8 | -- |
| NOT-APPLICABLE | 10 | 14 | -- |
| Mean fidelity (scored items) | 0.77 | 0.83 | 0.80 |
| Items below 0.70 | 6 | 5 | 10 |
| True gaps (missing from both) | -- | -- | 5 |
| R1-only gaps | -- | -- | 8 |
| R2-only gaps | -- | -- | 4 |

---

## Verdict

### Overall Split Integrity: GOOD with identified gaps

The split correctly partitions all 78 discrete requirements (tasks, features, data model changes, config, tests, metrics) between R1 and R2 with zero orphaned scope and zero scope creep. The fidelity audit (Part 4) score of 1.00 for discrete requirements is validated by this section-level analysis.

However, this deeper section-level review reveals that **contextual and reference material** (problem statements, architecture rationale, appendices, mockups) was not fully propagated into the split specs. The specs function as **scope boundary documents with parent-spec backlinks** rather than **standalone implementation specs**.

### Critical Finding

**R2 missing UI layout mockups (15-B) is the single most impactful gap.** The ASCII mockups are the primary visual reference for implementing the TUI v2 layout. Without them, the R2 implementer must constantly reference the parent spec.

### Recommendation

The split specs are suitable for use as-is IF implementers are expected to reference the parent spec for implementation detail. To make them standalone, address these priority items:

**Priority 1 (should fix)**:
- Add UI layout mockups to R2 (from Appendix B)
- Add per-task confidence assessment to R1 (from Section 14.4, especially T03.03 at 75%)
- Add test coverage targets to both specs (from Section 12.4)

**Priority 2 (nice to have)**:
- Add problem statement sections to both specs (from Sections 2.1, 2.2, 2.3)
- Add solution architecture detail to R1 (solution-to-cause matrix from Section 3.1)
- Add backward compatibility guarantee to R2 (from Section 9.3)
- Add timeline estimate to R2 (from Section 9.1)

**Priority 3 (optional)**:
- Add cross-domain conflict map to both specs (from Section 8.4)
- Add verification methods table to R1 (from Section 12.5)
- Add source document index to both specs (from Appendix D)
