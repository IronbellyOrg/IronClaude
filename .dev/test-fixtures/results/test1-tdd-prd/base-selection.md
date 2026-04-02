---
base_variant: "Opus (Variant A)"
variant_scores: "A:79 B:73"
---

# Adversarial Debate Scoring — Opus vs Haiku Roadmaps

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced 13 divergence points. I distill these into 10 weighted scoring criteria:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| 1 | Timeline realism | 12% | D-01 |
| 2 | Compliance timing & completeness | 12% | D-03, D-12 |
| 3 | Architectural precision (wiring, integration points) | 10% | Both variants emphasized this |
| 4 | Rollback & operational safety | 10% | D-13 |
| 5 | Risk mitigation specificity | 8% | R-001 through R-005 |
| 6 | Business value delivery speed (PRD S19) | 10% | PRD Success Metrics |
| 7 | Persona coverage (PRD S7) | 8% | D-05, PRD personas |
| 8 | Scope discipline & guardrails | 8% | Both variants |
| 9 | Actionability (task granularity, resourcing) | 10% | D-07, D-08 |
| 10 | Frontend timing pragmatism | 7% | D-04 |
| 11 | Open question resolution strategy | 5% | OQ handling |

## 2. Per-Criterion Scores

### C1: Timeline Realism (12%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 6/10 | 10-11 weeks with no team sizing. Debate convergence agreed this is too aggressive. Opus never specifies headcount, making the timeline unfalsifiable (Haiku's rebuttal, Round 2). |
| **Haiku** | 5/10 | 20 weeks with ~11 FTE is over-padded. Phase 0 at 2 weeks and Phase 4 at 4 weeks include excessive serial assumptions. Debate convergence landed at 14-16 weeks. |

**Verdict:** Both miss the mark. Opus is closer to the converged 14-16 week target but lacks resourcing justification. Haiku provides resourcing but inflates duration.

### C2: Compliance Timing & Completeness (12%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 8/10 | Integrates GDPR consent field into Phase 2 registration (zero-cost schema decision). Builds audit logging foundation in Phase 2. Compliance validation gate in Phase 5a. Debate convergence supported early schema integration. |
| **Haiku** | 7/10 | Dedicates Phase 3 entirely to compliance. Stronger organizational grouping (single compliance review gate). But defers consent_timestamp to Phase 3, creating the data quality gap Opus identified. |

**Verdict:** Opus's early integration is architecturally cleaner. The debate convergence (point 10) recommended Opus's schema approach + Haiku's grouped validation — favoring Opus as base.

### C3: Architectural Precision (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 8/10 | Named integration point tables per phase. Clear DI wiring (`AuthService` → `PasswordHasher` → `UserRepo`). Dispatch tables show which phase owns each artifact. |
| **Haiku** | 9/10 | More detailed wiring checklist (13-entry appendix table). Explicit registry naming (Account Lockout Registry, Error Code Registry, Rate Limit Registry, Token Signing Key Registry, etc.). Each mechanism has owning phase, cross-references, artifact path, and risk. |

**Verdict:** Haiku's wiring appendix is superior. The explicit artifact paths and per-mechanism risk notes are operationally valuable.

### C4: Rollback & Operational Safety (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 9/10 | Specific rollback triggers: p95 > 1000ms for 5 min, error rate > 5% for 2 min, Redis failures > 10/min, any data corruption. Automatable thresholds. Haiku partially conceded this point (D-13). |
| **Haiku** | 7/10 | "Metrics within normal ranges" is vague. But stronger on rollback *procedures*: step-by-step runbook testing, team drills, simulated outage exercises. |

**Verdict:** Opus wins on trigger precision. Haiku wins on procedural thoroughness. Merge should combine both.

### C5: Risk Mitigation Specificity (8%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 7/10 | 5 risks identified with mitigation strategies. R-004 (open questions delay) and R-005 (Redis unavailability) are novel additions. Contingencies defined per risk. |
| **Haiku** | 8/10 | Same core risks plus additional architectural risks (PostgreSQL pool exhaustion, password hash timing attacks, JWT clock skew, compliance audit failure, feature flag service failure). Per-phase risk tables with triggers. More comprehensive. |

**Verdict:** Haiku's per-phase risk tables with specific triggers are more operationally useful.

### C6: Business Value Delivery Speed — PRD S19 (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 9/10 | GA in 10-11 weeks. Registration conversion (>60%) and DAU (>1000) metrics tracked from Phase 5d. Revenue unlock ($2.4M) explicitly cited. SOC2 deadline met with months of margin. |
| **Haiku** | 5/10 | GA in 20 weeks. Lands GA in mid-August at best, leaving zero SOC2 buffer. The debate established this as a significant business risk. Haiku's slower delivery directly delays the personalization roadmap the PRD identifies as blocked. |

**Verdict:** Opus delivers business value significantly faster. Even accounting for the converged 14-16 week timeline, Opus's structure is closer to achieving it.

### C7: Persona Coverage — PRD S7 (8%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 6/10 | Alex (end user) fully covered. Sam (API consumer) partially covered via token refresh. Jordan (admin) explicitly deferred — admin audit API out of v1.0 scope. |
| **Haiku** | 9/10 | Alex fully covered. Sam covered. Jordan addressed with dedicated admin audit log query API (Phase 3 M3.5) with authorization middleware. All three PRD personas have explicit deliverables. |

**Verdict:** Haiku clearly wins. The PRD defines Jordan as a key persona with a user story (AUTH-E3). Opus's deferral creates a persona coverage gap. The debate (D-05) left this unresolved but Haiku's inclusion is more PRD-faithful.

### C8: Scope Discipline & Guardrails (8%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 9/10 | Explicit Section 8 on scope guardrails referencing PRD S12. Clear out-of-scope list (OAuth, MFA, RBAC, social login). No scope creep beyond TDD. |
| **Haiku** | 7/10 | Includes admin audit API and extensive per-phase task breakdowns that risk scope creep. The admin API adds ~18h but is PRD-justified. Some Phase 4 items (chaos engineering, extensive runbook suites) feel like nice-to-haves. |

**Verdict:** Opus is more disciplined. Haiku's additions are mostly justified but create more surface area.

### C9: Actionability (Task Granularity, Resourcing) (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 5/10 | No team sizing. No hour estimates. Tasks listed but not assigned to sprints or individuals. The debate established this makes the timeline unverifiable. |
| **Haiku** | 9/10 | ~11 FTE explicitly defined. Hour estimates per task. Sprint assignments (W1, W2-W3, etc.). Owner column per task. Capacity constraints visible (security engineer at 0.5 FTE). |

**Verdict:** Haiku is dramatically more actionable. Sprint planning can begin immediately from Haiku's roadmap.

### C10: Frontend Timing Pragmatism (7%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 6/10 | Frontend deferred to Phase 4 (Week 5-7). Avoids stub API risk but leaves frontend team idle. Debate convergence suggested Phase 2 start as compromise. |
| **Haiku** | 7/10 | Frontend starts Phase 1 (LoginPage, RegisterPage). Validates UX early. Risk of building against incomplete APIs, but login/register are stable surfaces. |

**Verdict:** Haiku is slightly more pragmatic given the debate's convergence toward Phase 2 frontend start. Neither variant perfectly matches the converged recommendation.

### C11: Open Question Resolution Strategy (5%)

| Variant | Score | Evidence |
|---------|-------|----------|
| **Opus** | 8/10 | Splits OQs into blocking vs non-blocking. Applies conservative defaults where safe (12-month retention, async email). Decision-forward approach reduces delivery risk. |
| **Haiku** | 7/10 | Tracks OQs with owner and target date. But leaves more decisions open (OQ-EXT-001 "MUST RESOLVE by Phase 3 M3.4" rather than defaulting). |

**Verdict:** Opus's default-forward approach is operationally safer.

## 3. Overall Scores

| Criterion | Weight | Opus | Haiku |
|-----------|--------|------|-------|
| Timeline realism | 12% | 6 | 5 |
| Compliance timing | 12% | 8 | 7 |
| Architectural precision | 10% | 8 | 9 |
| Rollback & ops safety | 10% | 9 | 7 |
| Risk mitigation | 8% | 7 | 8 |
| Business value speed | 10% | 9 | 5 |
| Persona coverage | 8% | 6 | 9 |
| Scope discipline | 8% | 9 | 7 |
| Actionability | 10% | 5 | 9 |
| Frontend timing | 7% | 6 | 7 |
| OQ resolution | 5% | 8 | 7 |
| **Weighted Total** | **100%** | **7.27 → 79** | **7.05 → 73** |

**Opus: 79/100 | Haiku: 73/100**

## 4. Base Variant Selection Rationale

**Selected base: Opus (Variant A)**

Opus wins as the base for three reinforcing reasons:

1. **Faster business value delivery.** The PRD is unambiguous: authentication blocks $2.4M in revenue and the SOC2 deadline is Q3 2026. Opus's compressed timeline (even when extended to the debate-converged 14-16 weeks) delivers GA sooner with more SOC2 margin.

2. **Structurally cleaner for merge.** Opus's 5-phase structure is simpler to extend than Haiku's 6-phase structure. Adding Haiku's improvements (resourcing, wiring appendix, admin API) to Opus is additive. Removing Haiku's padding to reach the converged timeline would be subtractive — harder and riskier.

3. **Compliance timing aligns with debate convergence.** The debate's consensus (point 10) recommended Opus's early schema integration + Haiku's grouped validation. Opus is already the base for this hybrid.

Opus's two weaknesses (no resourcing, no admin API) are straightforward to patch from Haiku.

## 5. Specific Improvements from Haiku to Incorporate in Merge

| # | Haiku Element | Target Location in Merged Roadmap | Rationale |
|---|---------------|-----------------------------------|-----------|
| 1 | **Team composition table** (~11 FTE breakdown with roles, timeline, and 0.5 FTE security) | New Section 4 subsection "Team Composition" | Makes timeline verifiable. Debate convergence point 9. |
| 2 | **Wiring checklist appendix** (13-entry table with mechanism, type, owning phase, cross-deps, status) | New Section 8 "Component Wiring Checklist" | Haiku's strongest architectural contribution. Prevents "forgot to wire X" failures. |
| 3 | **Admin audit log query API** (Phase 3 M3.5 in Haiku) | Add to Opus Phase 4 as optional deliverable with decision gate at Week 0 | PRD defines Jordan persona with explicit user story. Debate point 8 recommends escalating to product owner. Include as conditional scope. |
| 4 | **Per-phase risk tables with triggers** | Extend Opus Section 3 with Haiku's per-phase risk/trigger format | More operationally useful than Opus's single summary table. |
| 5 | **Runbook drill process** (team executes each runbook scenario) | Add to Opus Phase 5a hardening | Debate convergence point 2: combine Opus's thresholds with Haiku's drill process. |
| 6 | **Approval gates at 3 critical junctures** (pre-dev, pre-hardening, pre-GA) | Add lightweight gates per debate convergence point 7 | Not at every phase boundary (Haiku's overhead), but at the 3 points the debate identified as SOC2-necessary. |
| 7 | **Phase-level effort estimates** (hours per phase, not per task) | Add to Opus Section 6 timeline summary | Debate point 9: phase-level estimates without hour-level task breakdown. |
| 8 | **Frontend start in Phase 2** (LoginPage, RegisterPage after API contract defined) | Move Opus's frontend from Phase 4 to Phase 3 (after core auth) | Debate convergence point 6. Build pages after API contract is defined but before full token management. |
| 9 | **Explicit Phase 0** (compressed to 1 week) | Add 1-week Phase 0 before Opus's Phase 1 | Debate convergence point 5. Infrastructure provisioning deserves explicit tracking even if compressed. |
| 10 | **Consent timestamp hybrid** | Keep Opus's Phase 2 schema addition; add Haiku's Phase 3 compliance validation gate | Debate convergence point 10. Schema field early, full validation grouped later. |
