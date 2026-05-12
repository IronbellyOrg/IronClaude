---
base_variant: "B (Haiku Architect)"
variant_scores: "A:71 B:79"
---

# Base Selection: Opus Architect (A) vs Haiku Architect (B)

## Scoring Criteria

Derived from the 10 debate topics and PRD business context:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Timeline realism | 15% | Debate Topics 1, rebuttals |
| C2 | Phase scope coherence | 12% | Debate Topics 2, 3 |
| C3 | Security review strategy | 10% | Debate Topic 4 |
| C4 | Compliance alignment | 10% | Debate Topic 5, PRD S17 |
| C5 | Wiring & operational detail | 12% | Debate Topic 6 |
| C6 | Validation rigor (NFR measurement) | 10% | Debate convergence assessment |
| C7 | Resource & cost transparency | 8% | Debate Topic 6 rebuttal |
| C8 | Business value delivery speed | 10% | PRD: $2.4M personalization, S19 metrics |
| C9 | Persona coverage | 7% | PRD S7: Alex, Jordan, Sam |
| C10 | Risk management depth | 6% | Debate convergence, PRD S20 |

## Per-Criterion Scores

| Criterion | A (Opus) | B (Haiku) | Justification |
|-----------|----------|-----------|---------------|
| **C1: Timeline realism** | 6/10 | 7/10 | Opus's 9 weeks includes "unstructured padding" (debate rebuttal B acknowledged). Haiku's 4 weeks is tight but includes explicit slack analysis and conservative estimate (4-6 weeks). Neither is ideal — the debate converged on 6 weeks. Haiku's granular task durations and critical path analysis with slack values make its timeline more auditable. |
| **C2: Phase scope coherence** | 8/10 | 7/10 | Opus's progressive delivery (login/register in P1, refresh/profile in P2, reset in P3) has smaller blast radius per phase. Haiku puts all FR-AUTH in Phase 1 with feature flags — implementationally complete but validation-light. Opus wins on risk isolation; debate Topic 2 was unresolved but Opus's argument about untested-but-built code being "worst of both worlds" is strong. |
| **C3: Security review** | 6/10 | 8/10 | Debate converged: early checkpoint + final gate is strictly better. Haiku schedules security review at end of Phase 1 AND penetration testing pre-Phase 3. Opus defers entirely to Phase 3 — the debate's own rebuttal acknowledged the cost asymmetry of late discovery for crypto code. |
| **C4: Compliance alignment** | 6/10 | 9/10 | Haiku places admin audit query API in Phase 2, giving compliance teams weeks for pre-audit validation. Opus defers to Phase 3. Debate rebuttal A ("SOC2 audit is Q3, months to validate") was weakened by B's point about pre-audit preparation queues. Haiku also includes explicit compliance validation tasks in Phase 2. |
| **C5: Wiring & operational detail** | 7/10 | 9/10 | Opus has named artifacts per phase — readable but no consolidated reference. Haiku has both per-phase wiring tasks WITH cross-references (e.g., "Cross-Reference: FR-AUTH-003") AND a consolidated Integration Points & Wiring Summary with dispatch tables, DI configuration, feature flag matrix, and callback chains. Debate convergence acknowledged both approaches should be merged, but Haiku's baseline is richer. |
| **C6: Validation rigor** | 6/10 | 9/10 | Haiku provides per-NFR measurement methods with phased targets (Alpha/Beta/GA), specific tools (k6, APM), and success definitions. Opus lists metrics and targets but lacks measurement methodology detail. Example: Haiku specifies "k6 load test: 500 concurrent, sustained for 10 min" vs Opus's "500 concurrent login load test with k6." |
| **C7: Resource & cost transparency** | 6/10 | 9/10 | Haiku includes FTE counts per phase (6→5→3), third-party cost estimates (SendGrid ~$100/mo, LaunchDarkly $200+/mo), peak staffing notes, and procurement timelines. Opus lists roles and allocations but no cost data or staffing curves. |
| **C8: Business value delivery** | 6/10 | 8/10 | PRD identifies $2.4M personalization roadmap blocked by auth. Haiku delivers GA in 4 weeks (conservative: 5-6), unblocking personalization 3-5 weeks sooner than Opus's 9-week plan. Both reference the business context, but Haiku's faster delivery has a concrete revenue impact. The debate rebuttal noted "2+ extra months" of blocking. |
| **C9: Persona coverage** | 7/10 | 8/10 | Both cover Alex (end user) and Sam (API consumer). Haiku explicitly addresses Jordan (admin) earlier via Phase 2 audit query API (GAP-003). Opus defers Jordan's primary need to Phase 3. Haiku's Phase 2 compliance validation tasks also address Jordan's audit trail needs. |
| **C10: Risk management** | 8/10 | 8/10 | Both have substantially identical risk registers (debate convergence point). Opus includes an Open Questions table (OQ-001 through OQ-PRD-003) that Haiku lacks — useful for preventing silent assumptions. Haiku includes a Risk Mitigation Roadmap with temporal phases (Immediate → Pre-Beta → Pre-GA). Wash. |

## Overall Scores

| Variant | Weighted Score | Strengths | Weaknesses |
|---------|---------------|-----------|------------|
| **A (Opus)** | **71** | Progressive delivery reduces blast radius; open questions table prevents assumption drift; clean per-phase narrative; conservative risk posture | Unstructured timeline padding; deferred security review; no cost data; weak measurement methodology; late compliance delivery |
| **B (Haiku)** | **79** | Operational completeness (wiring, costs, FTE, critical path); validation rigor; faster business value; compliance-forward phasing; security checkpoint strategy | Aggressive Phase 1 scope risks quality; zero timeline slack in Phases 2-3; password reset in Phase 1 may be premature given complexity |

## Base Variant Selection Rationale

**Haiku (B) selected as base** because:

1. **Structural completeness.** Haiku's consolidated wiring summary, DI configuration table, feature flag integration matrix, callback chain documentation, critical path analysis with slack, FTE counts, and cost estimates provide a project-management-ready document. Opus would require substantial additions to reach this level.

2. **Validation depth.** Haiku's per-NFR measurement methods with phased targets are production-grade. Adding these to Opus would require rewriting the entire success criteria section.

3. **Compliance timing.** Haiku's Phase 2 admin audit query and compliance validation tasks align better with SOC2 pre-audit preparation — a point the debate converged on.

4. **Business value.** Faster GA delivery directly serves the PRD's $2.4M personalization dependency.

Adding Opus's phasing logic and open questions to Haiku's structure is less work than adding Haiku's operational detail to Opus's structure.

## Improvements to Incorporate from Variant A (Opus)

| # | Element from Opus | How to Incorporate | Priority |
|---|-------------------|--------------------|----------|
| 1 | **Timeline: 6-week compromise** | Adjust Haiku's 4-week plan to 6 weeks: 2w implementation + 2w beta + 2w GA/hardening. This was the debate's convergence point. Adds buffer without Opus's padding. | Critical |
| 2 | **Phase 1 scope: Progressive delivery** | Move password reset (FR-AUTH-005) from Phase 1 to Phase 2. Move token refresh validation to Phase 2 (keep implementation in Phase 1 but gate production exercise). This reduces Phase 1 blast radius per Opus's argument. | Critical |
| 3 | **Open Questions table** | Add Opus's OQ-001 through OQ-PRD-003 as a dedicated section. Haiku lacks explicit tracking of unresolved decisions. | High |
| 4 | **Named artifact format** | Retain Haiku's wiring tasks but add Opus's "Named Artifact" headers for readability. The per-phase narrative style improves scanning. | Medium |
| 5 | **Post-GA stabilization phase** | Add Opus's explicit 2-week post-GA stabilization period (on-call rotation, metric validation, flag removal). Haiku's Phase 3 Week 4 compresses this. | High |
| 6 | **Security: Dual-gate approach** | Add both Haiku's end-of-Phase-1 security checkpoint AND Opus's consolidated Phase 3 pre-GA security gate. The debate converged on this as optimal. | High |
| 7 | **Dependency table format** | Use Opus's cleaner dependency table format (Type, Required By, Status columns) alongside Haiku's procurement timeline data. | Low |
