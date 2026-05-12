---
base_variant: B
variant_scores: "A:71 B:78"
---

## Scoring Criteria

Derived from the six primary debate axes plus convergence deliverables:

| # | Criterion | Weight | Rationale |
|---|-----------|--------|-----------|
| C1 | Completeness & Coverage | 20 | All FRs, NFRs, ACs, risks addressed |
| C2 | Structural Clarity | 20 | Per-phase tables, cross-cutting catalog, sequencing constraints — debate-converged structural needs |
| C3 | Risk Treatment Quality | 20 | Traceability of mitigations to phase deliverables; contingency specificity (D-09, Round 2 R2.4) |
| C4 | Implementation Specificity | 20 | Named artifacts, wiring tables, actionable checklist items vs. prose descriptions |
| C5 | Timeline Realism | 10 | Honest estimation; Haiku's circular-dependency argument on observability/rollout was not rebutted (Round 2 R2.4) |
| C6 | Convergence Alignment | 10 | Incorporation of the five converged points: cross-cutting catalog, environment gates, sequencing constraints, named security review, staged validation framework |

---

## Per-Criterion Scores

### C1 — Completeness & Coverage (max 20)

**Variant A (Opus): 16**
- All nine requirements (FR-AUTH-001–005, NFR-PERF-001–002, NFR-REL-001, NFR-SEC-001–002) traced to phases with explicit validation criteria.
- Architect-identified risks R-004/R-005/R-006 are unique to Opus (D-09 debate advantage).
- No Phase 0 means six OQs are deferred to flight with only "recommended defaults" — Haiku's rebuttal (R2 B1) correctly identified that implementation-level decisions (error codes, Redis key schema, reset token format, audit log schema) are *not* defined by the spec.

**Variant B (Haiku): 15**
- Phase 0 resolves all six OQs explicitly before implementation begins; addresses environment readiness gates and API contract freeze.
- Covers all FRs/NFRs/ACs with clear phase attribution.
- R-004/R-005/R-006 are absent — a gap conceded by Haiku's debater and accepted as a convergence point.

---

### C2 — Structural Clarity (max 20)

**Variant A (Opus): 14**
- Per-phase inline wiring tables are highly actionable (D-12 debate point confirmed by both sides in convergence).
- Per-gate validation criteria table in Section 5 is precise and measurable.
- Missing: cross-cutting integration catalog (convergence item), sequencing constraints section (convergence item).
- No environment readiness gates (convergence item).

**Variant B (Haiku): 18**
- Section 3 cross-cutting integration catalog organized into five subsections (DI/service composition, middleware pipeline, frontend callbacks, feature-flag wiring, strategy/abstraction wiring) — directly addresses the "wiring bugs are the #1 source of auth integration failures" argument (D-12).
- Section 8 sequencing constraints make implicit dependencies explicit ("Do not start frontend token orchestration before JwtService…").
- Environment readiness gates in Section 5 before Phase 2, 4, and 5.
- Named milestone markers (M0–M5C) allow unambiguous gate tracking.
- Deduction: prose-based phase descriptions are less scannable than Opus's checklist format.

---

### C3 — Risk Treatment Quality (max 20)

**Variant A (Opus): 13**
- Three spec risks (R-001/R-002/R-003) have mitigation strategies and contingencies.
- Three architect-identified risks (R-004/R-005/R-006) are listed but lack the "Roadmap controls" format — no explicit phase-mapped mitigation sequence. R-005 Redis SPOF entry reads: "Consider Redis Sentinel/Cluster for HA" with no phase assignment.
- Haiku's debater correctly identified: "A risk without a phase-mapped mitigation is a worry, not a control" (D-09).

**Variant B (Haiku): 17**
- Each risk structured with: Architectural significance, Mitigation (numbered steps), Roadmap controls (explicit phase → action mapping), Contingency.
- R-001 roadmap controls: "Phase 3 implements token handling → Phase 4 validates no leakage → Phase 5 includes revocation runbook testing."
- R-002 roadmap controls: "Phase 2 implements lockout → Phase 4 wires gateway controls → Phase 5 watches login failure rate during Beta."
- R-003 roadmap controls: "Phase 5 owns migration execution → Phase 4 validates rollback runbook → Phase 0 resolves OQ-006."
- Deduction: R-004/R-005/R-006 absent (agreed convergence gap).

---

### C4 — Implementation Specificity (max 20)

**Variant A (Opus): 18**
- Phase 1 has 14 granular checklist items including exact schema columns, constraint types, and pool sizes.
- Per-phase wiring tables include Type, Owning Phase, and Consumed By columns.
- Specific metric names (`auth_login_total`, `auth_login_duration_seconds`) with alert thresholds and rollback trigger values (p95 > 1000ms for > 5 minutes, error rate > 5% for > 2 minutes).
- Parallelization opportunities section is actionable for sprint planning.

**Variant B (Haiku): 13**
- Phase descriptions use prose scope items rather than task-level checklists.
- Cross-cutting catalog provides named artifacts with wiring details, but per-phase task granularity is lower.
- No rollback trigger thresholds specified (what Opus calls "p95 > 1000ms for > 5 min" is absent).
- No parallelization opportunities identified.

---

### C5 — Timeline Realism (max 10)

**Variant A (Opus): 6**
- 7–8 weeks. Haiku's circular-dependency argument stands unrebutted: observability is bundled with rollout in Phase 4, but alpha/beta gates *require* metric evidence (p95 < 200ms, error rate < 0.1%). This means metrics must be validated before the rollout phase they're deployed in — a logical contradiction. Opus's rebuttal (R1 A) asserted this was speculative but did not address the circular dependency.
- No Phase 0 creates mid-sprint interface churn risk for the six OQs that are not fully resolved by the spec (Haiku R2 B1 is evidenced).

**Variant B (Haiku): 8**
- 9–11 weeks. Phase 0 (3–5 days) accounts for interface locking. Observability (Phase 4, 1 week) is separated from rollout (Phase 5, 4 weeks), breaking the circular dependency. Timeline is honest about the migration/rollout window.
- Deduction: 4-week rollout phase could be tightened; Alpha and Beta durations are conservative but defensible for a production auth system.

---

### C6 — Convergence Alignment (max 10)

**Variant A (Opus): 4**
- Per-phase wiring tables: ✓ (present)
- Cross-cutting catalog: ✗ (absent — convergence item)
- Environment readiness gates: ✗ (absent — convergence item)
- Sequencing constraints: ✗ (absent — convergence item)
- Named security review: ✗ (only implicit via PR review)
- Haiku's staged validation framework (A–D): ✗ (Opus uses letter-indexed gates but not the A–D stage taxonomy)

**Variant B (Haiku): 8**
- Per-phase descriptions: partial (lacks checklist format)
- Cross-cutting catalog: ✓ (Section 3 — five subsections)
- Environment readiness gates: ✓ (Section 5, three gates)
- Sequencing constraints: ✓ (Section 8 — five explicit rules)
- Named security review: ✓ (Section 5 team roles, Phase 4 gate)
- Staged validation framework (A–D): ✓ (Section 6, stages A–D with milestone mapping)
- R-004/R-005/R-006: ✗ (absent — convergence item)

---

## Overall Scores

| Criterion | Weight | Variant A (Opus) | Variant B (Haiku) |
|-----------|--------|-----------------|------------------|
| C1 Completeness | 20 | 16 | 15 |
| C2 Structural Clarity | 20 | 14 | 18 |
| C3 Risk Treatment | 20 | 13 | 17 |
| C4 Implementation Specificity | 20 | 18 | 13 |
| C5 Timeline Realism | 10 | 6 | 8 |
| C6 Convergence Alignment | 10 | 4 | 8 |
| **Total** | **100** | **71** | **78** |

---

## Base Variant Selection Rationale

**Selected base: Variant B (Haiku)**

The 7-point gap is driven by three structural decisions that are hard to retrofit:

1. **Cross-cutting catalog vs. inline tables is not a binary choice** — the debate converged that both are needed (convergence point 2). Haiku's Section 3 provides the system-topology view that Opus lacks entirely; Opus's per-phase tables can be added to Haiku as a formatting layer. The reverse merge (adding a full catalog to Opus) requires substantially more structural work than adding Opus-style checklists to Haiku's phases.

2. **Observability separation is architecturally correct** — Haiku's unrebutted circular-dependency argument (Round 2, R2.4) is the strongest technical point in the debate: the beta gate requires p95 < 200ms and error rate < 0.1%, which require Prometheus metrics to measure, which are deployed in Phase 4. In Opus, Phase 4 bundles observability and rollout together, making the gate unmeasurable at the point it must be evaluated. This is a correctness defect, not a style preference.

3. **Convergence alignment favors Haiku on four of six items** — environment readiness gates, sequencing constraints, security review, and staged validation framework are all present in Haiku and absent in Opus. These are low-cost structural additions in Opus but are already load-bearing in Haiku's architecture.

Opus's primary strength (C4: implementation specificity, score 18 vs. 13) is the most actionable improvement path for the merge.

---

## Specific Improvements From Variant A (Opus) to Incorporate in Merge

Ordered by impact:

### 1. Convert prose scope items to checklist tasks (C4 gap: 5 points)
Opus's per-phase checklists provide task-level granularity that Haiku's prose lacks. For each Haiku phase, convert scope items to `- [ ]` checklist format with the same specificity Opus uses in Phase 1 (schema columns, constraint types, exact pool sizes) and Phase 2 (per-endpoint rate limit values, account lockout parameters).

**Evidence:** Opus Phase 1.2: "Create `UserProfile` table schema: `id` (UUID v4, PK), `email` (UNIQUE, indexed, NOT NULL)…" vs. Haiku Phase 1: "Define persistence schema: `UserProfile`, audit log store, refresh-token persistence model."

### 2. Add architect-identified risks R-004/R-005/R-006 using Haiku's risk format (converged C3)
Incorporate Opus's three additional risks using Haiku's "Architectural significance / Mitigation / Roadmap controls / Contingency" structure:
- **R-004** (RSA key compromise): Phase 1 key loading + Phase 4/5 rotation procedure → maps to OQ-004
- **R-005** (Redis SPOF): Phase 4 Redis failure alerting + Phase 5 Sentinel/Cluster decision → maps to NFR-REL-001
- **R-006** (SendGrid outage): Phase 2 retry queue + Phase 5 reset endpoint monitoring → maps to FR-AUTH-005

**Evidence:** Opus Section 3 additional risks table; convergence point 1 from debate.

### 3. Add per-phase inline wiring tables alongside the cross-cutting catalog (converged C2)
Haiku's Section 3 catalog provides topology; Opus's per-phase tables provide immediate developer context. Add a condensed per-phase wiring table to each Haiku phase showing the same four columns Opus uses (Named Artifact, Type, Wired Components, Consumed By). These are not redundant — they answer different questions at different points in the implementation.

**Evidence:** Convergence point 2: "Integration documentation should include both inline per-phase tables AND a cross-cutting catalog."

### 4. Add rollback trigger thresholds (C4 specificity gap)
Haiku's Phase 5 references rollback procedures but does not specify trigger values. Add Opus's explicit thresholds:
- p95 latency > 1000ms for > 5 minutes
- Error rate > 5% for > 2 minutes
- `TokenManager` Redis failures > 10/min
- Any `UserProfile` data loss or corruption

**Evidence:** Opus Section 4.6 rollback triggers.

### 5. Add parallelization opportunities section (C4 specificity gap)
Opus's Critical Path section identifies four parallel development opportunities that reduce calendar time without compressing the estimate. Add these to Haiku's timeline section (Section 7) to help teams execute the 9–11 week plan efficiently:
- Phase 1: `PasswordHasher` and `JwtService` in parallel
- Phase 2: Login/register endpoints vs. password reset endpoints
- Phase 3: Frontend components in parallel while Phase 4 observability setup begins
- Phase 5: Migration script development overlaps with Alpha testing

**Evidence:** Opus Section 6 Critical Path parallelization bullets.

### 6. Add external dependency provisioning lead times (C4 specificity gap)
Haiku's Section 5 lists external dependencies without provisioning timelines. Add Opus's lead time column and "Risk if Delayed" column to the dependency table. Specifically: PostgreSQL and Redis managed-cloud provisioning requires ~1 week lead time (not just npm install), and SendGrid sender identity verification requires 2–5 days — both are schedule risks if not surfaced.

**Evidence:** Opus Section 4 dependency table with "Provisioning Lead Time" and "Risk if Delayed" columns.
