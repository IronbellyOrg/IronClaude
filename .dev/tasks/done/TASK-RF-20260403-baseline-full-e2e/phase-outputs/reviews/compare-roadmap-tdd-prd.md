# Roadmap Comparison: Baseline (Spec-Only) vs TDD+PRD Enriched

**Date**: 2026-04-02
**Phase**: 6.3

## File Metrics

| Metric | Baseline (test3-spec-baseline) | TDD+PRD (test1-tdd-prd) | Delta |
|--------|-------------------------------|-------------------------|-------|
| File size (bytes) | 25,773 | 32,640 | +6,867 (+26.6%) |
| Line count | 380 | 523 | +143 (+37.6%) |
| Heading count (lines starting with #) | 39 | 37 | -2 (-5.1%) |
| PRD keyword hits | 4 | 40 | +36 (10x increase) |
| TDD keyword hits | 15 | 50 | +35 (3.3x increase) |
| Extraction size (bytes) | 14,648 | 28,864 | +14,216 (2x — TDD+PRD extracts more source material) |

## Structural Comparison

### Baseline Roadmap
- **Frontmatter**: `spec_source` only
- **Phases**: 5 phases (Phase 1-5), Week 1 through 5-6+
- **Input**: Single spec document
- **No Phase 0**: Jumps directly to implementation

### TDD+PRD Enriched Roadmap
- **Frontmatter**: `spec_source`, `prd_source`, `complexity_score`, `adversarial`, `base_variant`, `variant_scores`, `convergence_score`, `debate_rounds`
- **Phases**: 4 phases (Phase 0-3), Week 1 through 12.5
- **Input**: TDD + PRD documents (dual enrichment)
- **Phase 0 (Design and Foundation)**: Dedicated 2-week pre-coding phase for architecture review, OQ resolution, infrastructure provisioning, and compliance alignment

## TDD+PRD Enrichment Visibility — 3 Specific Content Examples

### Example 1: Frontend Component Architecture (TDD-sourced)

**Present in TDD+PRD (lines 176-201), absent in baseline:**

The TDD+PRD roadmap includes a full "Frontend Development" track running in parallel with backend, specifying:
- `AuthProvider` context component with state shape `{ authToken, user, isLoading, error }` and methods (`login`, `register`, `logout`, `refreshToken`)
- `LoginPage` component with form fields and client-side validation
- `RegisterPage` component with GDPR consent checkbox and inline password strength feedback
- `ProfilePage` component with logout button
- `ProtectedRoute` wrapper with token check and redirect logic
- Token storage strategy: "accessToken in memory only (XSS mitigation per R-001); refreshToken in HttpOnly cookie"

The baseline roadmap has zero frontend component references. It treats the system as backend-only, with no mention of LoginPage, RegisterPage, ProfilePage, or AuthProvider.

### Example 2: Persona-Driven Validation Gates (PRD-sourced)

**Present in TDD+PRD (lines 294-298), absent in baseline:**

The TDD+PRD roadmap includes a "Persona-Driven Validation" section at Phase 2 exit:
- "Alex (end user): Registration completes in under 60 seconds; session persists across page refreshes; password reset email arrives within 60 seconds; logout works cleanly"
- "Sam (API consumer): Programmatic token refresh works without user interaction; clear error codes returned; expired tokens produce actionable 401 responses"
- "Jordan (admin): Account unlock endpoint operational; audit logs queryable by date range and user; failed login visibility confirmed"

The baseline roadmap contains zero persona references. Validation is expressed purely in technical terms (unit tests pass, benchmark timings met) without mapping back to user needs.

### Example 3: Business Drivers and Revenue Justification (PRD-sourced)

**Present in TDD+PRD (lines 18-21), absent in baseline:**

The TDD+PRD executive summary includes explicit business drivers:
1. "Personalization roadmap — Enables ~$2.4M in projected annual revenue from identity-dependent personalization features planned for Q2-Q3 2026"
2. "Compliance deadline — Required for SOC2 Type II audit in Q3 2026 (user-level event logging, 12-month audit retention)"
3. "Competitive positioning — 25% of churned users cite missing user accounts as reason for leaving"

The baseline executive summary describes only technical architecture ("JWT-based authentication service with five core capabilities") with no business context, revenue figures, or competitive analysis.

## Additional Enrichment Features Unique to TDD+PRD

| Feature | TDD+PRD | Baseline |
|---------|---------|----------|
| Phase 0 (pre-coding design) | YES — 2 weeks for threat model, OQ resolution, infra setup | NO — jumps to implementation |
| Open Questions with persona rationale | YES — OQ-001 through OQ-008 with persona-specific rationale (e.g., "JWT refresh pattern sufficient for Sam persona") | YES — OQ-1 through OQ-5 but with technical rationale only |
| Infrastructure provisioning (K8s, Redis, PostgreSQL) | YES — explicit provisioning tasks with connection pooling, HPA config | NO — assumes infrastructure exists |
| Feature flags | YES — `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` with rollback criteria | NO — mentions single `AUTH_SERVICE_ENABLED` flag without rollback detail |
| Extended beta period rationale | YES — "7-day refresh token TTL means the first forced re-authentication occurs at the beta boundary. To capture at least one full refresh lifecycle before GA" | NO — no beta period |
| Compliance gate per phase | YES — Phase 1 Compliance Gate with 4 NFR-COMP checkpoints | NO — compliance items embedded in tasks without formal gates |
| Observability (Prometheus metrics, OpenTelemetry) | YES — specific metric names (`auth_login_total`, `auth_login_duration_seconds`) and alert thresholds | NO — mentions "performance test suite" generically |
| Team composition table | YES — FTE breakdown (5 roles across 3 phases) | Minimal — "2 engineers + security review" |

## Verdict

**TDD+PRD enrichment produces the most measurably different output of all three runs.** The enriched roadmap is 26.6% larger, has 37.6% more lines, and contains 10x more PRD keywords and 3.3x more TDD keywords than the baseline.

The enrichment is visible across three distinct dimensions:
1. **TDD-sourced**: Frontend component architecture, data model field-level detail, API endpoint specifications with rate limits, infrastructure provisioning detail
2. **PRD-sourced**: Business drivers ($2.4M revenue), persona-driven validation gates, competitive positioning, success metrics with named IDs
3. **Combined TDD+PRD**: Phase 0 design phase (neither spec-only nor either enrichment alone would motivate this), compliance conflict resolution (spec says v1.1, PRD says Q3 2026), extended beta period with token lifecycle rationale

The TDD+PRD enrichment is unambiguously measurable and produces a qualitatively different roadmap.
