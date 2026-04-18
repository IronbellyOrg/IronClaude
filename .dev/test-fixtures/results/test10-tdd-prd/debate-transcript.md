---
convergence_score: 0.62
rounds_completed: 2
---

# Adversarial Debate: Opus (7-Phase/9-Week) vs Haiku (5-Phase/13-Week)

## Round 1: Initial Positions

### Divergence 1: Phase Structure (7 vs 5) and Timeline (9 vs 13 weeks)

**Variant A (Opus):**
Seven phases with explicit overlap yields a 9-week timeline — 44% faster. Each phase is small enough to fail fast: if INFRA-001 slips, we know in week 1, not buried inside a 2-week mega-phase. The SOC2 Q3 2026 deadline is not negotiable. Thirteen weeks pushes GA dangerously close to audit prep. Phase overlap (P4 over P3, P7 over P6) is standard for any team with frontend and backend engineers — they are not blocking each other. The coordination cost of 7 exit gates is trivial compared to the cost of missing the compliance window.

**Variant B (Haiku):**
Thirteen weeks is not padding — it is honesty. Opus assumes parallel frontend/backend streams, but the spec describes a single auth-team with platform support. Phase overlap only works when distinct people own each stream. A 2-week Phase 1 that validates keys, schemas, consent stores, lockout policy, rate limiting, and health checks before any API code begins means Phase 2 developers never touch half-built infrastructure. Five phases reduce gate ceremony without losing rigor — each gate is simply higher-stakes and more meaningful. If SOC2 timing is tight, the answer is to start sooner, not to compress unrealistically.

### Divergence 2: Schema Explicitness (3 implicit vs 6 explicit)

**Variant A (Opus):**
Three first-class schemas (UserProfile, AuthToken, AuditLog) define the contract surface. ConsentRecord, PasswordResetToken, and AuthSecurityState are implementation details of their respective modules — ConsentRecorder, ResetTokenStore, LockoutPolicy. Elevating them to top-level data models creates premature rigidity. The PasswordHasher and LockoutPolicy modules own their storage shape; forcing a schema contract before the module is built inverts the dependency. We define interfaces, not tables.

**Variant B (Haiku):**
Compliance reviewers do not read module internals — they read schemas. DM-004 (ConsentRecord), DM-005 (PasswordResetToken), and DM-006 (AuthSecurityState) make consent capture, reset token lifecycle, and lockout state auditable from day one. When the SOC2 auditor asks "where is consent stored and what fields does it contain?" — Haiku answers with a schema definition, Opus answers with "check the ConsentRecorder module implementation." These are not premature — they are the exact fields the PRD and compliance requirements demand. Leaving them implicit risks three different developers implementing three different shapes.

### Divergence 3: Test Placement (Batched Phase 5 vs Distributed Inline)

**Variant A (Opus):**
A dedicated testing phase is schedulable, reportable, and auditable. TEST-001 through TEST-010 in Phase 5 form a coherent quality gate with clear entry criteria (Phases 3+4 complete) and exit criteria (80% coverage, E2E green, k6 passing, security review clean). Inline testing fragments accountability — who owns the test failure when it is discovered mid-implementation? A batched phase also enables a single security penetration test (TEST-009) across the complete attack surface rather than partial scans against incomplete endpoints.

**Variant B (Haiku):**
Discovering an integration bug in week 6 that was introduced in week 3 costs 3x more to fix than catching it immediately. Haiku places unit and integration tests (TEST-001 through TEST-005, TEST-007, TEST-008) in Phase 2 alongside the APIs they verify. E2E tests (TEST-006, TEST-009 through TEST-012) land in Phase 3 with the frontend. Compliance and load tests (TEST-013 through TEST-016) land in Phase 4 with operations. Each phase ships tested code, not code-that-will-be-tested-later. The security review (TEST-015) runs in Phase 4, still covering the complete surface before rollout. Opus's batched approach is a waterfall testing anti-pattern dressed in agile clothing.

### Divergence 4: Admin Frontend and Logout Journey Completeness

**Variant A (Opus):**
API-008 delivers the admin audit log query endpoint. The admin frontend page is a UI concern that can ship in v1.1 without blocking the Jordan persona's core need — queryable audit data. Opus includes COMP-017 LogoutButton with clear behavior (click -> clear -> redirect). The logout flow is functionally complete; wrapping it in a "journey spec" (FR-AUTH-006) and dedicated E2E test (TEST-011) adds ceremony without adding capability. The API works; the button calls it.

**Variant B (Haiku):**
The PRD defines Jordan as a persona who "views authentication event logs." An API endpoint without a UI means Jordan needs curl or Postman — that is not "viewing." COMP-015 (AdminAuthEventsPage) with filters, FR-AUTH-007 (the journey), and TEST-012 (E2E verification) close the persona gap completely. On logout: shared-device security is not ceremony. FR-AUTH-006 specifies that logout must end the session immediately, revoke refresh tokens, and redirect safely — behaviors that a simple button component does not guarantee without explicit verification. TEST-011 proves the chain works end-to-end. Opus's LogoutButton is a UI widget; Haiku's logout is a verified security control.

### Divergence 5: OpenTelemetry and Health Endpoint Scope

**Variant A (Opus):**
OpenTelemetry tracing (OPS-012) in Phase 7 is deliberate — tracing generates volume and cost. Wiring it before the service is stable adds noise to the signal. The health endpoint (NFR-REL-001) checks PostgreSQL and Redis — the two runtime dependencies. SendGrid is not a liveness dependency; email delivery failure degrades password reset, not service availability. RSA key presence is validated at startup, not at runtime health check frequency.

**Variant B (Haiku):**
OpenTelemetry must be available during alpha and beta — those are the phases where distributed tracing is most valuable for debugging rollout issues. Wiring it in Phase 7, concurrent with GA, means the team lacks tracing during the exact period they need it most. On health checks: COMP-016 checks PostgreSQL, Redis, RSA keys, and SendGrid because the SLA covers the complete auth service, not just "the parts that respond to HTTP." A degraded SendGrid means password reset is broken; a missing RSA key means no tokens can be issued. The health endpoint should reflect what users experience, not what the infrastructure team finds convenient to monitor.

## Round 2: Rebuttals

### Opus Rebuts Haiku

**On timeline:** Haiku claims 13 weeks is "honesty," but the diff analysis shows the same 88-93 tasks. The extra 4 weeks come from sequential execution, not additional work. If the team cannot parallelize frontend and backend, then neither roadmap works — Haiku's Phase 3 (frontend, 2 weeks) still assumes backend APIs from Phase 2 are complete and stable. The parallelism assumption is identical; Opus just makes it explicit. Starting sooner is not always an option — the SOC2 clock is external.

**On schemas:** Haiku's DM-004/005/006 define schemas before the modules that use them are designed. ConsentRecord's `policyVersion` field, for example, assumes a versioned consent policy system that neither roadmap specifies. This is speculative schema design. Opus's approach — let the module define its storage — produces schemas that match actual behavior. The compliance reviewer will see the schema regardless; the question is whether it was designed top-down (Haiku, risk of mismatch) or bottom-up (Opus, guaranteed consistency).

**On test placement:** Haiku claims inline tests catch bugs earlier, but Opus's Phase 3 integration points table explicitly wires all components before Phase 5 testing begins. The "3-week-old bug" scenario assumes no developer testing during implementation — unrealistic. Phase 5 is the formal validation gate, not the first time code is tested. Meanwhile, Haiku's distributed tests create ambiguity: if TEST-004 fails in Phase 2, does Phase 3 proceed? If yes, inline testing is theater. If no, every phase becomes a potential blocker for the next.

**On admin frontend:** The Jordan persona's PRD user story says "view authentication event logs." A paginated JSON API with date/user/event filters satisfies "viewing" for any technical admin — which Jordan, as a system administrator, is. Building a full React page (COMP-015) with filters, table rendering, and E2E tests adds 3-5 days of frontend work to v1 scope. If product confirms Jordan needs a GUI, it ships in v1.1 with zero API changes.

### Haiku Rebuts Opus

**On timeline:** Opus's 9-week plan has Phase 4 overlapping Phase 3 and Phase 7 overlapping Phase 6. This means frontend developers start building against APIs that are still being implemented (Phase 3 runs weeks 3-5, Phase 4 starts week 4). Any API contract change in week 4 invalidates frontend work from the same week. The "parallel streams" argument requires API contracts frozen before frontend begins — but Opus's Phase 3 includes 22 tasks across backend, API, compliance, and SendGrid integration. Contract stability during active development is an assumption, not a plan. Haiku's sequential approach ensures each phase consumes stable artifacts.

**On schemas:** "Let the module define its storage" sounds elegant until three modules independently decide how to store consent timestamps — one uses ISO strings, one uses Unix epochs, one uses database-native timestamps. DM-004 through DM-006 are not speculative; they contain exactly the fields that the PRD, TDD, and GDPR requirements specify. The `policyVersion` field in ConsentRecord is required by GDPR Article 7 — consent must reference the specific privacy policy version accepted. This is not speculation; it is a legal requirement that Opus's approach would discover late.

**On test placement:** "Does Phase 3 proceed if TEST-004 fails?" — No. That is precisely the point. A failing integration test in Phase 2 blocks Phase 3, which means the bug is fixed in week 4, not discovered in week 6. Opus's Phase 5 testing gate means a failing TEST-004 is discovered in week 5 with 4 weeks of dependent code already built on top. The "developer testing during implementation" argument concedes that testing happens inline anyway — Haiku simply makes it formal, tracked, and gate-blocking.

**On admin frontend:** "Any technical admin" is not a product requirement — the PRD specifies a user persona, not a curl command. Jordan's user story implies a UI workflow with filters and visual data. Deferring COMP-015 to v1.1 means the SOC2 auditor sees an API endpoint but no evidence that admin log viewing is operationally practiced. The 3-5 day cost is small relative to the compliance risk of presenting an unused API as evidence of log monitoring capability.

**On OpenTelemetry:** Opus concedes that tracing "generates volume and cost" but places it in Phase 7 concurrent with GA — the highest-traffic phase. If cost is the concern, tracing should be wired in Phase 4 with sampling configured before traffic hits. Opus's approach means the team either has no tracing during the most critical debugging period (alpha/beta) or rushes to wire it during GA rollout alongside runbooks, dashboards, and on-call setup. Haiku's Phase 4 placement gives 4 weeks of trace data before any production traffic.

## Convergence Assessment

### Areas of Agreement (High Convergence)

1. **Architecture is settled.** Both variants agree on AuthService facade, RS256/bcrypt, Redis refresh tokens, PostgreSQL persistence, and SendGrid. No debate needed.
2. **Rollout strategy is settled.** Alpha -> 10% beta -> GA with identical feature flags, rollback chain, and observation periods.
3. **Risk assessment is settled.** Same 6 risks, same mitigations, same owners.
4. **Success criteria are settled.** Same 10 metrics, same targets. The dispute is only about whether they are advisory (Opus) or gate-blocking (Haiku).
5. **PRD gap fills are settled.** Both include API-007 (logout) and API-008 (admin logs). The dispute is about frontend completeness, not API scope.
6. **Rate limiting and lockout are settled.** Identical thresholds and behavior.

### Areas of Partial Convergence

7. **Schema explicitness:** Haiku's GDPR Article 7 argument for `policyVersion` in ConsentRecord is strong. Opus's bottom-up concern is valid but loses on compliance grounds. **Recommendation:** Adopt Haiku's explicit schemas (DM-004/005/006) but allow module implementations to extend them.
8. **Test placement:** Both sides acknowledge testing happens during development regardless. **Recommendation:** Hybrid — unit tests inline with implementation (Haiku's approach), but consolidate E2E, load, and security tests into a dedicated gate before rollout (Opus's Phase 5 concept). This catches unit/integration bugs early while preserving a formal quality gate.
9. **Health endpoint:** Haiku's argument that RSA key absence means zero token issuance is factually correct. **Recommendation:** Adopt Haiku's 4-dependency health check but classify SendGrid as a degraded (not failed) state.

### Areas of Remaining Dispute (Low Convergence)

10. **Timeline (9 vs 13 weeks):** This is fundamentally a team-size and parallelism question that cannot be resolved without knowing the actual team composition. If parallel frontend/backend streams exist, Opus's 9 weeks is achievable. If a single team, Haiku's 13 weeks is realistic. **No convergence possible without external input.**
11. **Admin frontend in v1:** Product and compliance must decide. Haiku's SOC2 argument is stronger than Opus's deferral argument, but scope is a business decision, not a technical one. **No convergence possible without stakeholder input.**
12. **OpenTelemetry placement:** Haiku wins on merit. Tracing before rollout is objectively more useful than tracing during GA. Opus offered no strong counter beyond cost, which is a sampling configuration issue, not a placement issue. **Recommendation:** Adopt Haiku's Phase 4 placement.
13. **Phase granularity (7 vs 5):** Tightly coupled to the timeline dispute. More phases with overlap (Opus) vs fewer phases sequential (Haiku) are expressions of the same parallelism assumption. **No convergence without team data.**

### Summary

Agreement on architecture, risk, success criteria, and rollout strategy is strong (14/18 shared assumptions held). The 5 remaining disputes reduce to two root questions: (1) can the team parallelize frontend and backend work? and (2) is admin UI in v1 scope? Resolving those two questions would raise convergence from 0.62 to approximately 0.85, with the merged roadmap adopting Haiku's explicit schemas, distributed unit tests, 4-dependency health check, and pre-rollout tracing, while adopting Opus's Docker Compose task, consolidated E2E/security gate, and detailed integration point tables.
