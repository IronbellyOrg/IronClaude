---
base_variant: "Haiku (Variant B)"
variant_scores: "A:71 B:81"
---

# Base Selection: Opus vs. Haiku Roadmap Evaluation

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced 10 dimensions. I weight them by impact on successful delivery:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Phase structure & design front-loading | 12% | Debate Topics 3, 4 |
| C2 | OQ resolution strategy | 10% | Debate Topic 5 |
| C3 | Parallel development efficiency | 10% | Debate Topic 1 |
| C4 | Risk table depth & ownership | 10% | Debate convergence table |
| C5 | Implementation specificity | 10% | Debate convergence table |
| C6 | Integration point documentation | 10% | Debate convergence table |
| C7 | Rollback criteria precision | 8% | Debate Topic 6 |
| C8 | Rollout safety & duration | 8% | Debate Topic 6 |
| C9 | Compliance gate clarity | 10% | PRD S17, debate convergence |
| C10 | Business value delivery speed | 12% | PRD S19, debate Topic 4 |

**PRD-derived dimensions** (weighted into existing criteria):
- Business value delivery → folded into C10
- Persona coverage → evaluated across C2, C5, C6
- Compliance alignment → folded into C9

## 2. Per-Criterion Scores

### C1: Phase Structure & Design Front-Loading (12%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 60 | No Phase 0. Infrastructure provisioning mixed into Phase 1 coding weeks. Debate Round 2: Opus did not adequately defend implicit design-during-coding. |
| Haiku (B) | 88 | Explicit Phase 0 (Weeks 1-2) separates infrastructure, OQ resolution, threat modeling, and team alignment from coding. Debate convergence: "Haiku's position is stronger here." |

Opus treats design as emergent from implementation. For a security-critical service with 8 open questions, this is risky. Haiku's Phase 0 parallelizes infra provisioning with OQ resolution — neither blocks the other, and both complete before coding starts.

### C2: OQ Resolution Strategy (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 55 | OQs listed in Section 8 with "resolve before Phase X" dates but no decisions made. OQ-008 (logout) deferred to "before Phase 4" — Week 7. Debate: Opus argued stakeholder resolution, but the debate showed most OQs are technical. |
| Haiku (B) | 90 | All 8 OQs resolved in Phase 0 with explicit decisions and rationales. OQ-005 correctly deferred to v1.1. OQ-007 (admin unlock) resolved with endpoint for Jordan persona. Decision log as deliverable. |

Haiku's approach directly addresses the PRD's Jordan persona (admin needs account unlock — OQ-007) and Alex persona (logout — OQ-008). Opus leaves these unresolved for 7+ weeks.

### C3: Parallel Development Efficiency (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 65 | Frontend starts Week 7 (Phase 4) after backend stable. Some Phase 3/4 overlap noted in timeline. Sequential approach is safe but slow. |
| Haiku (B) | 82 | Frontend starts Week 3 in parallel with backend. OpenAPI spec from Phase 0 enables contract-first development. Debate: Opus raised valid token lifecycle edge case concerns, but Haiku's contract-first position is industry-standard. |

The debate did not fully resolve this — Opus's point about token lifecycle timing is legitimate. However, Haiku's approach saves 2-3 weeks on critical path, and integration testing in Week 7 catches contract mismatches. The risk is manageable with a mature team.

### C4: Risk Table Depth & Ownership (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 68 | 7 risks with severity, phase addressed, and mitigation. No probability, no owner, no monitoring strategy. R-005 (security breach) labeled CRITICAL but mitigation is generic ("dedicated security review"). |
| Haiku (B) | 90 | 7 risks with severity, probability, impact, mitigation, contingency, owner, and monitoring columns. Each risk has a named owner (security-engineer, platform-team, backend-lead). Monitoring is specific (e.g., "Failed login counter; IP blocklist length"). |

Haiku's risk table is operationally actionable. Opus's is a summary.

### C5: Implementation Specificity (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 72 | Good component-level detail (PasswordHasher, TokenManager, etc.). Method signatures implied but not shown. Weekly breakdown absent — phases are 2-3 week blocks. |
| Haiku (B) | 85 | Week-by-week breakdown within each phase. Explicit wiring tables showing which component connects to which, with owning phase and consumers. Method-level detail (e.g., `AuthService.login(email, password)` → `PasswordHasher.verify()` → `TokenManager.issueTokens()`). |

Haiku provides enough detail for a developer to start coding on Day 1 of Phase 1. Opus requires additional decomposition.

### C6: Integration Point Documentation (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 88 | Dedicated Section 3 with 5 named integration points. Each has: named artifact, wired components, owning phase, cross-reference. Feature flag registry documented with cleanup targets. Rate limiting configuration per endpoint. |
| Haiku (B) | 72 | Integration points documented inline within phase tables (Named Artifact columns in Phase 1 and Phase 2). Less consolidated — reader must scan multiple phases to build the full picture. |

Opus's Section 3 is a standout. A developer or architect can read it independently to understand all system wiring without reading the full roadmap. Haiku distributes this information across phases, which is contextually useful but harder to reference.

### C7: Rollback Criteria Precision (8%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 90 | Section 6.5: explicit numeric thresholds (p95 > 1000ms for > 5 min, error rate > 5% for > 2 min, Redis failures > 10/min, any data loss). Actionable by on-call without interpretation. |
| Haiku (B) | 70 | Rollback mentioned in Phase 3 ("rollback criteria are not triggered") but specific thresholds not consolidated. Alerts section has thresholds (p95 > 500ms, Redis > 10/min) but these are alerting, not rollback triggers. |

Opus's rollback criteria are copy-pasteable into a runbook. Haiku's require synthesis from multiple sections.

### C8: Rollout Safety & Duration (8%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 82 | 4-week rollout (alpha → 2-week beta at 10% → 1-week GA). Captures full 7-day refresh token lifecycle during beta. Debate Round 2: Opus correctly identified that 7-day beta may miss the first forced re-auth. |
| Haiku (B) | 72 | 2-week rollout (Week 11 GA, Week 12 stabilization). Beta starts Week 10 — only 7 days before GA. Haiku conceded in debate that 7-day beta is insufficient for 7-day refresh TTL. |

Opus wins here. The debate produced a convergence point: minimum 10-day beta. Haiku's 7-day beta is insufficient for the refresh token lifecycle. Opus's 14-day beta is appropriately conservative.

### C9: Compliance Gate Clarity (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 78 | Phase 1 has a compliance gate (Section 1.6) checking GDPR consent, audit schema, no plaintext passwords, data minimization. Phase 5 has final compliance validation. Two-gate approach is solid. |
| Haiku (B) | 82 | Phase 0 maps NFR-COMP-001 through NFR-COMP-004 to audit log schema fields. Phase 2 dedicates Week 9 to SOC2 compliance with specific validation steps. AuditLogger service is a named artifact with explicit wiring. |

Both handle compliance well. Haiku edges ahead because the AuditLogger is a first-class component with explicit wiring, and compliance mapping happens in Phase 0 — meaning any schema issues are caught before coding starts.

### C10: Business Value Delivery Speed (12%)

| Variant | Score | Evidence |
|---------|-------|----------|
| Opus (A) | 60 | 15-week timeline (13 weeks development + some overlap, 4-week rollout). GA at Week 15. PRD states personalization features need auth; 15 weeks pushes to mid-July. Debate: "If personalization features need auth by June, 15 weeks pushes delivery to mid-July." |
| Haiku (B) | 85 | 12-week timeline. GA at Week 12. All 5 FRs delivered by Week 10. PRD Success Metrics (S19) measurable by Week 12. Enables Q2 2026 personalization roadmap on schedule. |

PRD S19 defines DAU > 1000 within 30 days of GA. Starting that clock 3 weeks earlier (Week 12 vs. Week 15) matters for the $2.4M revenue pipeline and Q3 SOC2 audit timing.

## 3. Overall Scores

| Criterion | Weight | Opus (A) | Haiku (B) | A Weighted | B Weighted |
|-----------|--------|----------|-----------|------------|------------|
| C1: Phase structure | 12% | 60 | 88 | 7.2 | 10.6 |
| C2: OQ resolution | 10% | 55 | 90 | 5.5 | 9.0 |
| C3: Parallel efficiency | 10% | 65 | 82 | 6.5 | 8.2 |
| C4: Risk depth | 10% | 68 | 90 | 6.8 | 9.0 |
| C5: Implementation detail | 10% | 72 | 85 | 7.2 | 8.5 |
| C6: Integration docs | 10% | 88 | 72 | 8.8 | 7.2 |
| C7: Rollback precision | 8% | 90 | 70 | 7.2 | 5.6 |
| C8: Rollout safety | 8% | 82 | 72 | 6.6 | 5.8 |
| C9: Compliance gates | 10% | 78 | 82 | 7.8 | 8.2 |
| C10: Business value speed | 12% | 60 | 85 | 7.2 | 10.2 |
| **Total** | **100%** | | | **70.8** | **82.3** |

**Final Scores: Opus 71 / Haiku 82**

## 4. Base Variant Selection Rationale

**Selected base: Haiku (Variant B)**

Haiku wins on 7 of 10 criteria. Its structural advantages are:

1. **Phase 0 eliminates ambiguity before coding starts** — the debate converged on this being the stronger position. Opus did not defend implicit design-during-coding.
2. **OQ resolution prevents mid-sprint blocking** — all 8 OQs decided with rationale, enabling parallel frontend development.
3. **12-week timeline delivers business value faster** — 3 weeks earlier to GA, critical for the $2.4M personalization pipeline and Q3 SOC2 audit.
4. **Risk table is operationally actionable** — named owners, monitoring strategies, and contingencies per risk.
5. **Week-by-week granularity** enables sprint planning without additional decomposition.

Opus's advantages (integration documentation, rollback criteria, rollout duration) are important but additive — they can be merged into Haiku's structure without restructuring.

## 5. Improvements from Opus to Incorporate in Merge

The following Opus elements should be merged into the Haiku base:

### Must Incorporate

1. **Integration Points Section (Opus Section 3)** — Lift Opus's consolidated integration point documentation as a new section in the merged roadmap. Haiku's inline tables are useful but insufficient for cross-phase reference. Include all 5 integration points: AuthService Facade, TokenManager→JwtService, AuthProvider→API, Feature Flag Registry, Rate Limiting Configuration.

2. **Rollback Criteria (Opus Section 6.5)** — Replace Haiku's implicit rollback references with Opus's explicit thresholds: p95 > 1000ms for > 5 min, error rate > 5% for > 2 min, Redis failures > 10/min, any data loss. These belong in Phase 3's GA section.

3. **Extended Beta Duration** — Per debate convergence, extend Haiku's beta from 7 days to minimum 10-14 days. Opus correctly identified that a 7-day refresh TTL means the first forced re-auth happens at the beta boundary. Adjust Phase 3 timeline: beta starts Week 9.5 (3 days earlier) or GA shifts to mid-Week 12.

4. **Phase 1 Compliance Gate (Opus Section 1.6)** — Haiku validates compliance in Phase 2 (Week 9), but Opus adds an early compliance gate after Phase 1 that catches GDPR consent, audit schema, and password logging issues before 6 weeks of development. Add this as a Phase 1 exit gate.

### Should Incorporate

5. **Operational Readiness Detail (Opus Section 6.6)** — Opus specifies HPA scaling (10 pods at CPU > 70%), on-call rotation, and runbook deployment. Haiku has similar content but less specific. Merge Opus's HPA and runbook specifics into Haiku's Phase 3.

6. **Phase 3/4 Overlap Note (Opus Timeline)** — Opus notes that frontend LoginPage/RegisterPage can begin while password reset backend develops. Haiku already parallelizes, but this specific overlap optimization should be explicit.

7. **Library Dependencies List (Opus Section 5)** — Opus lists specific libraries (bcryptjs, jsonwebtoken, Jest, Supertest, testcontainers, Playwright, k6). Haiku mentions some inline but lacks a consolidated list. Add to Phase 0 deliverables.

### Nice to Have

8. **Success Criteria Validation Phase Column (Opus Section 6)** — Opus maps each metric to its validation phase. Haiku has a similar table but with more columns (Source, Measurement Method, Owner). Merge Opus's "Validation Phase" column into Haiku's table for completeness.
