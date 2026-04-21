# Roadmap Comparison: Baseline (Spec-Only) vs Spec+PRD Enriched

**Date**: 2026-04-02
**Phase**: 6.2

## File Metrics

| Metric | Baseline (test3-spec-baseline) | Spec+PRD (test2-spec-prd) | Delta |
|--------|-------------------------------|---------------------------|-------|
| File size (bytes) | 25,773 | 27,698 | +1,925 (+7.5%) |
| Line count | 380 | 330 | -50 (-13.2%) |
| Heading count (lines starting with #) | 39 | 20 | -19 (-48.7%) |
| PRD keyword hits (persona, Alex, Jordan, Sam, compliance, SOC2, GDPR, revenue, business) | 4 | 36 | +32 (9x increase) |
| TDD keyword hits (data model, UserProfile, AuthToken, POST /auth, GET /auth, endpoint, component, frontend, LoginPage, RegisterPage) | 15 | 35 | +20 (2.3x increase) |

## Structural Comparison

### Baseline Roadmap
- **Frontmatter**: spec_source only; no prd_source
- **Phases**: 5 phases (Phase 1-5), weeks 1-6+
- **Phase naming**: Foundation, Core Auth Logic, API and Middleware, Hardening, Production Readiness
- **Section structure**: 39 headings, granular sub-sections per phase

### Spec+PRD Enriched Roadmap
- **Frontmatter**: spec_source, complexity_score, adversarial, base_variant, convergence_score, debate_rounds (no prd_source field despite PRD enrichment)
- **Phases**: 2 phases (Phase 1-2), weeks 1-7 + buffer weeks 8-10
- **Phase naming**: Authentication Core (Weeks 1-4), Recovery/Compliance/Hardening (Weeks 5-7)
- **Section structure**: 20 headings, numbered sections (1. Executive Summary, 2. Phased Implementation, 3. Risk Assessment, 4. Resource Requirements, 5. Success Criteria)
- **Additional sections not in baseline**: Risk Assessment table (7 risks with severity/mitigation), Resource Requirements (team FTE breakdown), Success Criteria table (7 measurable thresholds with IDs SC1-SC6)

## PRD Enrichment Visibility

### Present in Spec+PRD, Absent in Baseline

1. **Business context**: "Authentication unblocks the Q2-Q3 2026 personalization roadmap (~$2.4M projected annual revenue)" — baseline has zero revenue or business justification language.

2. **Compliance conflict resolution**: "The specification defers audit logging to v1.1, but the PRD requires SOC2 audit logging with a Q3 2026 deadline. This roadmap includes audit logging in Phase 2 scope." — baseline follows the spec's deferral without questioning it.

3. **Success criteria with IDs**: SC1 (registration conversion > 60%), SC2 (login p95 < 200ms), SC3 (session duration > 30 min), SC4 (failed login rate < 5%), SC5 (password reset completion > 80%), SC6 (99.9% uptime). Baseline has performance targets but no named success criteria or conversion/adoption metrics.

4. **Risk assessment table**: 7 enumerated risks (R1-R7) with severity, mitigation strategy, and success indicators. Baseline mentions some risks inline but has no dedicated risk section.

5. **Team composition table**: FTE breakdown by role and phase. Baseline mentions "2 engineers + security review" in the executive summary but provides no staffing detail.

6. **UX testing references**: "Registration UX testing at Phase 1 exit gate" with "> 60% conversion rate target validated (5+ user tests)" — baseline has no UX testing or conversion targets.

7. **GDPR/compliance tasks**: Explicit tasks for GDPR consent verification (NFR-AUTH.4), NIST password storage audit (NFR-AUTH.6), data minimization audit (NFR-AUTH.7), SOC2 control mapping. Baseline has compliance-related items but they are implicit in task descriptions rather than dedicated audit tasks.

## Verdict

**PRD enrichment is measurably visible in the Spec+PRD roadmap.** The enriched version contains business justification ($2.4M revenue), named success criteria (SC1-SC6), a formal risk register, team staffing, compliance-specific audit tasks, and UX validation gates — none of which appear in the baseline. The keyword analysis confirms a 9x increase in PRD-derived terminology.

However, the enrichment produced a structurally different roadmap (2 phases vs 5, fewer headings, more condensed), making direct section-by-section comparison difficult. The enriched roadmap consolidates implementation into fewer, larger phases with milestone sub-sections (M1-M6) rather than the baseline's granular phase breakdown.

**Assessment**: PRD enrichment is measurable and substantive. The enriched roadmap demonstrates awareness of business drivers, compliance deadlines, and user persona needs that the spec-only baseline lacks entirely.
