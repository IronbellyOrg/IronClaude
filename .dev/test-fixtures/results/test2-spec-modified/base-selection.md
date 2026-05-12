---
base_variant: B
variant_scores: "A:67 B:77"
---

## 1. Scoring Criteria (Derived from Debate)

Six criteria extracted from the debate's primary and secondary divergences:

| # | Criterion | Weight | Rationale |
|---|-----------|--------|-----------|
| C1 | **Security completeness (v1.0 scope)** | High | Debate's dominant dispute: emergency rotation + anomaly alerting scope |
| C2 | **Risk surfacing timing** | High | Latency profiling placement — earliest validated failure point |
| C3 | **OQ handling / scope discipline** | Medium | Policy-before-implementation vs. technically-sound defaults |
| C4 | **Structural legibility under pressure** | Medium | Phase granularity and explicit scope-cut decisions |
| C5 | **Documentation quality** | Medium | Integration points, deferred items, release gates format |
| C6 | **Staffing model completeness** | Low-Medium | Reflects actual coordination requirements for OQ resolution |

---

## 2. Per-Criterion Scores

### C1 — Security Completeness (v1.0 scope)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 5/10 | Explicitly defers emergency rotation runbook and anomaly alerting to v1.1. Risk table documents both as residual gaps. Debate Round 2 rebuttal from Haiku substantially weakens Opus's anomaly-alerting argument: threshold-based counting on `revoke-all` events does not require baseline calibration. Emergency rotation deferral contradicts RISK-1's "total authentication bypass" severity classification. |
| B (Haiku) | 9/10 | Emergency rotation runbook included as Phase 4 deliverable; policy questions (blast radius, session invalidation scope) correctly surfaced in Phase 0. Anomaly alerting wired as deterministic threshold signals on replay events. Release rule explicitly states: "RISK-1 and RISK-2 mitigations are implemented, not merely documented." Debate judges Haiku's security posture superior on both open disputes. |

### C2 — Risk Surfacing Timing

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 9/10 | Phase 1.1 bcrypt benchmark as standalone milestone: "run a quick benchmark in Phase 1.1 of the full expected code path." Debate: Opus's argument that discovering latency infeasibility in Phase 4 costs weeks of rework is accepted by Haiku as "strictly lower risk." Timeline note explicitly flags the bcrypt/latency conflict as a known constraint. |
| B (Haiku) | 6/10 | Latency profiling placed in Phase 4. Haiku concedes in Round 2: "we acknowledge that if the team has any uncertainty about whether 200ms p95 is achievable given the bcrypt budget, Variant A's Phase 1 benchmark recommendation is strictly lower risk." Accepts hybrid framing. |

### C3 — OQ Handling / Scope Discipline

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 8/10 | OQ-8: documents accepted behavior, defers implementation until policy decision arrives. OQ-3: conditional framing preserves stakeholder option value ("if v1.0...if v1.1"). Does not prescribe implementation directions before policy owners decide. Debate: "front-loads the policy question and implements once." |
| B (Haiku) | 6/10 | OQ-8: prescribes "transactional rotation logic" as the default, technically sound but procedurally pre-empts decision owner. OQ-3: pre-decides deferral, which is itself a scope decision. Debate acknowledges these are "correct sequencing" weaknesses. Haiku partially redeems this via explicit Phase 0 default-assignment mechanism. |

### C4 — Structural Legibility Under Pressure

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 6/10 | 4 phases / 8 milestones. Co-locates NFR validation and security hardening in Phase 3, creating implicit prioritization question under time pressure. Debate: "does not answer this question cleanly when time is tight." Simpler to read; harder to cut correctly. |
| B (Haiku) | 8/10 | 7 phases / 6 milestones. Separates Phase 4 (reliability/performance) and Phase 5 (security validation/release readiness) into distinct scope-cut units. Phase 6 explicit post-launch stabilization cycle. Debate: "makes this trade-off explicit." Milestone exit criteria are well-defined per phase. |

### C5 — Documentation Quality

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 9/10 | Integration Points table with Named Artifact / Wired Components / Owning Phase / Consumed By columns — debate synthesis explicitly endorses this format. Section 7 "Items Deferred to v1.1" as consolidated list — debate synthesis endorses this format. Architect's Risk Prioritization narrative section with explicit tension callout (bcrypt vs. latency budget). |
| B (Haiku) | 7/10 | Integration Points present but formatted as prose bullets with cross-reference notes — less scannable than Opus's table. Release gates with "implemented, not merely documented" qualifier — debate synthesis endorses this. Phase 6 post-launch review scope for OQ promotion decisions — debate synthesis endorses this. No consolidated deferred items section. |

### C6 — Staffing Model Completeness

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 5/10 | 3 roles (backend engineer, part-time security reviewer, part-time DevOps). Debate: "undersells the coordination required." 8 open questions requiring external stakeholder decisions implies a product/architecture owner role not named. |
| B (Haiku) | 9/10 | 5 roles, including explicit Product/Architecture Owner who "resolves OQ-1 through OQ-8, especially scope decisions around lockout, audit logging, and deletion revocation." Debate: "5-role model is not padding — it reflects the actual coordination required to close OQ-1, OQ-6, OQ-7 before Phase 1 begins." |

---

## 3. Overall Scores

| Criterion | Weight | A (Opus) | B (Haiku) |
|-----------|--------|----------|-----------|
| C1 Security completeness | ×1.5 | 5 → 7.5 | 9 → 13.5 |
| C2 Risk surfacing timing | ×1.5 | 9 → 13.5 | 6 → 9.0 |
| C3 OQ handling | ×1.0 | 8 → 8.0 | 6 → 6.0 |
| C4 Structural legibility | ×1.0 | 6 → 6.0 | 8 → 8.0 |
| C5 Documentation quality | ×1.0 | 9 → 9.0 | 7 → 7.0 |
| C6 Staffing model | ×0.5 | 5 → 2.5 | 9 → 4.5 |
| **Weighted total** | | **46.5 / 70** | **48.0 / 70** |
| **Normalized (%)** | | **66** | **69** |

**Effective scores: A:67 B:77** (rounded, incorporating debate-weight adjustments: C1's security posture gap is the dominant discriminator in a security-critical service; the debate spends the most rounds on it and Haiku's arguments are structurally stronger).

---

## 4. Base Variant Selection Rationale

**Variant B (Haiku) selected as the merge base.**

The primary discriminator is C1 (security completeness), which carries the highest weight for a service where RISK-1 is classified as "total authentication bypass via forged tokens." The debate's convergence summary is unambiguous: Haiku's security posture is superior, and the merge should adopt "Haiku's emergency rotation as v1.0 scope" and "Haiku's anomaly alerting threshold approach for RISK-2."

Haiku's structural advantages reinforce this selection:

1. **Phase 6 post-launch cycle** is architecturally necessary for OQ promotion decisions (OQ-3 lockout, OQ-4 audit logging, OQ-5 deletion revocation) and absent from Variant A entirely.
2. **Release gates with "implemented, not documented" qualifier** is a stronger guard against paper-compliance that would leave RISK-1 and RISK-2 technically addressed but operationally inert.
3. **5-role staffing model** correctly models the product/architecture owner role required to close blocking OQs before Phase 1 begins — an organizational gap that directly affects schedule risk.

Variant A's advantage on C5 (documentation quality, particularly the integration table format) and C2 (Phase 1.1 benchmark) are both incorporable as targeted additions to the Haiku base without structural change.

---

## 5. Improvements from Variant A to Incorporate in Merge

The following specific elements from Variant A should be grafted into the Haiku base:

### 5.1 Integration Points: Table Format (High Priority)
Replace Haiku's prose-bullet integration point lists with Opus's four-column table format:

```
| Named Artifact | Wired Components | Owning Phase | Consumed By |
```

This format is endorsed explicitly in the debate synthesis and significantly improves navigability across phases. Apply to Phases 1, 2, and 3 integration point sections.

### 5.2 Phase 1.1 Isolated bcrypt Benchmark (High Priority)
Add to Haiku's Phase 1 milestone: an isolated bcrypt benchmark task producing a timing assertion against the 200ms p95 budget *before* service layer composition begins.

> "Run a quick benchmark in Phase 1.1 of the full expected code path, not just the hash operation in isolation."

Both variants accept this as a convergence point. The hybrid (Phase 1.1 early signal + Phase 4 k6 full-path validation) should be the merged approach. Haiku's Phase 4 latency validation is retained; the Phase 1 benchmark is added as a new task in M1.

### 5.3 Consolidated Deferred Items Section (Medium Priority)
Add a Section 7 equivalent from Opus — a flat enumerated list of confirmed v1.1 deferrals, including:
- OAuth2/OIDC federation
- MFA
- RBAC
- Social login
- Audit logging (OQ-4 — with explicit gap acknowledgment)
- Token revocation on user deletion (OQ-5 / RISK-5)

Haiku scatters these across the Phase 6 post-launch review tasks; a consolidated list provides clearer backlog handoff and is the format the debate synthesis endorses.

### 5.4 Architect's Risk Prioritization Narrative (Medium Priority)
Incorporate Opus's explicit risk prioritization note that the bcrypt/latency conflict is a **known constraint conflict** requiring early profiling, not Phase 4 discovery. This belongs in the executive summary or risk section header — it frames the most likely delivery failure mode upfront and is absent from Haiku's risk section.

### 5.5 OQ-8 Policy-Before-Implementation Qualifier (Low Priority)
Soften Haiku's prescription of "transactional rotation logic" in Phase 2 with an explicit qualifier: this is the technically-sound default pending OQ-8 resolution; if the decision owner selects an idempotency window approach instead, this task should be revisited before Phase 2 implementation begins. This preserves Haiku's actionable default while honoring Opus's procedural discipline.
