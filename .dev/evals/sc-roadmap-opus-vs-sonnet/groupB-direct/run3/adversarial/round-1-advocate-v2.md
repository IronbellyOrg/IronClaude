# Round 1 Advocate — Variant 2 (Sonnet Default)

**Author:** V2 Advocate
**Round:** 1
**Date:** 2026-05-22

---

## Position Summary

V2 delivers a pragmatic, production-viable auth service roadmap that prioritizes user-visible value at every milestone, accepts principled trade-offs in durability and ceremony to accelerate time-to-GA, and provides concrete operational artifacts (state invariants, GDPR erasure, admin API) that V1 omits. Where V1 optimizes for audit-reviewer confidence, V2 optimizes for engineering execution velocity on a small team with a hard Q2 deadline.

---

## Steelman of V1 (REQUIRED before any critique)

### Build Order (X-001): Token-First

V1's strongest argument is real and deserves acknowledgment: isolating `JwtService` and `TokenManager` into M2 (before any HTTP endpoints) allows dedicated security review of the cryptographic surface without HTTP concerns muddying the waters. V1 Section 11 states: "Splitting them out lets us security-review and benchmark the crypto-sensitive code in isolation, with property tests on rotation invariants, before HTTP concerns muddy the waters." This is sound engineering for a security-critical subsystem. The property-based tests on rotation invariants (using fast-check, per V1 M2 Validation) are a genuine strength -- rotation races are the single most dangerous class of bug in a JWT system, and testing them in isolation is cleaner than testing them entangled with HTTP routing.

### Data Durability (X-003, X-004, C-008): Zero-Loss Posture

V1's `noeviction` Redis policy plus Postgres-backed `password_reset_tokens` table represents a defensible zero-data-loss posture. The reasoning is clear: tokens are security credentials, and silently evicting them is semantically equivalent to revoking user sessions without consent or notification. V1 M1 Scope explicitly states "eviction policy set to noeviction on the auth keyspace." The `password_reset_tokens` table with `SELECT FOR UPDATE` (V1 M4 D4.4) gives transactional single-use enforcement that survives any Redis failure. If a DR scenario destroys Redis, V1's users retain their in-flight password resets. That is a genuinely stronger durability guarantee.

### Key Management (C-011): KMS/HSM

V1's KMS-backed signing keys (AWS KMS or HashiCorp Vault, per M2 D2.3) ensure the private key never leaves an HSM. This is the textbook correct answer for production JWT signing. The ADR-002 decision record (V1 M2 D2.3) and the local key cache with 5-minute lifetime (V1 Risk R-DEP-1) represent a mature key-management posture that would satisfy any security auditor immediately, without explanation or defense.

### Spec-First (C-003, C-004): OpenAPI + Contracts Package

V1's `@auth/contracts` npm package (M1 D1.3) and OpenAPI 3.1 spec stub (M1 D1.4) with Spectral linting provide contract stability from day one. For a team building both frontend and backend, shared typed contracts prevent the integration surprises that inevitably arise when frontend and backend teams work against implicit assumptions. The JSON-schema validators in the contracts package mean that any API shape change is caught at compile time, not at integration time.

### Frontend Coupling (X-002): Ship Together

V1's decision to ship `LoginPage`, `RegisterPage`, and `AuthProvider` in M3 alongside the backend endpoints they consume eliminates the mock-drift problem entirely. There is no gap between "backend says it returns X" and "frontend expects X" because they are tested together from the moment either exists. V1 M3 D3.9's 12 negative-path Playwright tests cover the full stack, not just one layer.

### What V1 Gets RIGHT (summary)

V1 gets the following things genuinely right: (1) property-based testing of rotation invariants in isolation; (2) zero token loss as an operational posture; (3) KMS-backed signing keys as the textbook production standard; (4) contract-driven development via OpenAPI + shared npm package; (5) a 30+ edge-case catalog (Section 13) that is genuinely comprehensive; (6) 15% buffer for vacation/onboarding attrition baked into sprint planning. These are real engineering strengths, not ceremonial additions.

---

## Strengths Claimed

1. **Auth-first delivers user-visible value at M2, not M3.** V2 M2 (Core Authentication) ships `POST /auth/register` and `POST /auth/login` in Sprints 3-4. V1 ships these in M3 (Sprints 5-7). This means V2 delivers the two most important user-facing endpoints -- registration and login -- two sprints earlier than V1. By Sprint 4, stakeholders can register and log in against a real backend. V1 delivers only a token library by that point, which is invisible to users and to most integration testers. (Ref: V2 M2 Scope, "POST /auth/register endpoint" and "POST /auth/login endpoint"; V1 M3 Scope, same endpoints deferred to Sprints 5-7; diff S-001.)

2. **State-mechanics invariants (INV-01 through INV-10) provide testable system properties.** V2 Appendix B defines 10 invariants, each declared as a P1 bug if violated, with explicit enforcement location and validation method. For example, INV-02 ("Each refresh token is used exactly once") is enforced via "TokenManager.refresh() atomically deletes old token and creates new one via Redis Lua script" and validated by "Integration test: second use of same token returns 401." This gives QA an unambiguous checklist. V1 has no equivalent -- its edge cases are cataloged descriptively in Section 13 but lack the P1-severity binding and enforcement-location traceability. (Ref: V2 Appendix B; diff U-009.)

3. **GDPR right-to-erasure endpoint (DELETE /auth/me) exists in V2 but not V1.** V2 M6 D6.3 delivers a `DELETE /auth/me` endpoint that "removes all PII (nullifies email, deletes password hash, anonymizes display_name) within 30 days." V1 has no deletion endpoint. GDPR Article 17 requires the ability to erase personal data. V1's GDPR mapping (Section 9.1) covers consent and data minimization but omits the right to erasure entirely. This is a compliance gap. (Ref: V2 M6 D6.3; V2 GDPR Mapping table; diff U-010.)

4. **Infrastructure cost estimate enables budget planning.** V2 Roadmap Overview table includes "$450/month production (3 K8s pods $150, PostgreSQL $200, Redis $100)." V1 provides no cost estimate. For a team shipping to production, this is actionable financial data that enables conversations with finance and capacity planning. (Ref: V2 Roadmap Overview table, line 29; diff U-008.)

5. **Admin API endpoint (GET /admin/auth-events) is more useful than a CLI tool.** V2 M4 D4.5 delivers a REST endpoint with pagination, role-based access, and composite indexes. V1 M5 D5.7 delivers a CLI tool (`auth-admin log query --user X --since Y`). A REST API is composable -- it can power dashboards, be called from automation, and does not require SSH access to production. The CLI tool requires shell access to a production-adjacent environment, which is a security and operational barrier. (Ref: V2 M4 D4.5; V1 M5 D5.7; diff U-012.)

6. **PasswordHasher placement in M1 enables early benchmarking and avoids downstream surprise.** V2 places PasswordHasher in M1 (Data Foundation, D1.3) with explicit benchmark testing against cost factor 12. V1 defers it to M3 (D3.5). If cost factor 12 proves too slow on production CPU, V2 discovers this in Sprint 2; V1 discovers it in Sprint 5-7 when it is entangled with endpoint logic and frontend components. Early discovery is strictly better for a schedule-constrained project. (Ref: V2 M1 D1.3, "hash operation benchmarks < 500ms"; V1 M3 D3.5; diff S-002.)

7. **Open questions are tracked with owner, status, and resolution.** V2 Appendix A tracks 6 open questions (PRD OQ1-OQ4, TDD OQ1-OQ2) with explicit status (Resolved or Deferred), target milestone, and resolution description. V1 has no equivalent. This creates traceability for decisions that would otherwise live only in Slack threads. (Ref: V2 Appendix A; diff U-011.)

8. **Team sizing is realistic for a startup/growth-stage team.** V2 specifies "3-5 engineers, plus frontend-team for M4." V1 requires "4 BE, 2 FE, 0.5 SRE, 0.5 sec-reviewer" -- 6.5 FTE fixed. For a company shipping its first auth service, requiring 6.5 dedicated FTEs may be infeasible. V2's variable sizing allows the team to scale with availability. (Ref: V2 Roadmap Overview, "3-5 engineers"; V1 Section 2, "4 backend engineers, 2 frontend engineers, 0.5 SRE, 0.5 security reviewer"; diff S-006.)

9. **Sequencing rationale addresses the token-first alternative explicitly.** V2's Sequencing Rationale section contains a subsection "Alternative considered -- Token-first (M3 before M2)" that argues: "tokens have no meaning without a use case. Building tokens first creates unvalidated code that may need rework once login/registration requirements are fully understood during implementation." This is a pragmatic position: build the thing that validates your requirements (login/register endpoints) before building the optimization layer (JWT tokens). (Ref: V2 Sequencing Rationale, "Alternative considered -- Token-first"; diff C-001.)

10. **GA rollout happens in M5, with hardening in M6 -- enabling earlier value delivery.** V2's M5 is "Frontend Integration and GA Rollout." Users are on the new system by the end of M5 (Sprint 11). M6 is dedicated hardening and compliance validation. V1 does GA rollout in M6, meaning users cannot use the system until Sprint 12. For a project unblocking $2.4M ARR in personalization features, one sprint of earlier availability matters. (Ref: V2 M5/M6 naming and sequencing; V1 M6 = Hardening + GA; diff S-005.)

---

## Weaknesses in V1

1. **Token-first sequencing delays user-visible value by two sprints.** V1 M2 (Token Lifecycle) delivers only library code -- `JwtService` and `TokenManager` with no HTTP endpoints. No user can register or log in until M3 (Sprints 5-7). V2 ships registration and login in M2 (Sprints 3-4). For a service that "unblocks Q2-Q3 2026 personalization features (projected $2.4M ARR contribution)" (V1 Executive Summary, line 16), two extra sprints of invisible library work is a significant delay to time-to-value. (Ref: V1 M2 Scope, "M2 ships only the library"; V1 M3 Scope; diff X-001.)

2. **V1's 6.5 FTE fixed team size is unrealistic for most organizations.** V1 Section 2 requires "4 backend engineers, 2 frontend engineers, 0.5 SRE, 0.5 security reviewer" for the full 12 sprints. This assumes zero attrition, zero reassignment, and a dedicated SRE/security allocation that most growth-stage teams cannot afford. V2's variable "3-5 engineers" (V2 Roadmap Overview) is more honest about the uncertainty of headcount. (Ref: V1 Section 2; diff S-006.)

3. **V1 omits GDPR right-to-erasure.** V1's GDPR mapping (Section 9.1, line 503) covers consent capture and data minimization but has no deletion endpoint. GDPR Article 17 is not optional -- it is a legal requirement for any service processing EU user data. V2 M6 D6.3 explicitly delivers `DELETE /auth/me`. (Ref: V1 Section 9.1; V2 M6 D6.3; diff U-010.)

4. **V1's dedicated M5 (Compliance, Audit Logging & Observability) creates a compliance bolt-on risk despite claiming to avoid it.** V1 Section 11 states: "This split prevents a 'compliance bolt-on at the end' anti-pattern." However, V1 defers all audit-log persistence to M5 -- M3 and M4 emit events "to a stub sink." This means M3 and M4 run in production (behind feature flags) with no durable audit trail until M5 completes. If M5 slips, the system operates for an extended period without compliant audit logging, which is the exact compliance bolt-on risk V1 claims to avoid. V2 embeds audit writing directly into M2 (D2.4) and M4 (D4.6), so every endpoint produces audit rows from its first sprint. (Ref: V1 M3 Scope Out, "Audit log persistence (M5 -- but log events are emitted in M3, just not yet stored in long-term table)"; V2 M2 D2.4; diff S-004.)

5. **V1's KMS dependency on M2 creates a blocking external dependency.** V1 M2 Entry Criteria (line 121) requires "KMS access provisioned (or Vault namespace allocated) with role permissions audited." V1 Risk R-DEP-1 acknowledges this risk (probability Low, impact Critical). If the KMS provisioning slips -- which is common in organizations where KMS requires security-team approval -- M2 is entirely blocked with no fallback. V2 uses Kubernetes secret mounts (V2 M3 D3.7), which require no external approval and are provisioned by the same team deploying the service. (Ref: V1 M2 Entry Criteria line 121; V1 Risk R-DEP-1; V2 M3 D3.7; diff C-011.)

6. **V1's edge-case catalog is descriptive but not testable at the invariant level.** V1 Section 13 catalogs 30+ edge cases across 7 subsections, each with an owner milestone and proof artifact. However, the catalog does not declare severity -- is a violated edge case a P1, P2, or P3? V2's Appendix B invariants are all declared P1 by construction ("Violation of any invariant is a P1 bug"). This means V2's test failures are automatically severity-classified, while V1's require triage. (Ref: V1 Section 13; V2 Appendix B preamble; diff U-005 vs U-009.)

---

## Concessions

1. **V2 requires retrofitting M2 endpoints in M3 (D3.5, D3.6).** This is a genuine weakness. V2 M2 ships login/register returning a "session identifier placeholder" (V2 M2 Scope Out), and M3 D3.5/D3.6 must retroactively update these endpoints to return `AuthToken`. This means M2 exit criteria validate endpoints that will be modified in M3, requiring re-testing. V1 avoids this entirely by building tokens first and shipping complete endpoints from the start. (Ref: V2 M2 Scope Out, "returns session identifier placeholder; M3 adds JWT"; V2 M3 D3.5, D3.6; diff X-005.)

2. **V2's `allkeys-lru` Redis policy means tokens can be silently evicted under memory pressure.** This is a real operational risk. If Redis memory fills (e.g., due to a token leak creating millions of refresh tokens), valid users will be forced to re-authenticate without warning. V2 acknowledges this in M3 Risks: "Set maxmemory-policy to allkeys-lru" with monitoring at 70%. However, the monitoring does not prevent eviction -- it only alerts after it starts. V1's `noeviction` policy is strictly stronger for session continuity. (Ref: V2 M3 Risks, line 304; V1 M1 Scope, "noeviction"; diff X-003.)

3. **V2's SOC2 retention mapping contains an internal contradiction.** V2's SOC2 mapping table states "90-day retention in PostgreSQL; extensible to 12 months via partitioning" (line 729), but M6 D6.2 exit criteria says "Confirm 12-month retention policy." If the team misses the extension step, the default 90-day retention may fail SOC2 audit. V1 commits to 12-month retention from the start and avoids this inconsistency. (Ref: V2 SOC2 Mapping table, line 729; V2 M6 D6.2; diff X-006.)

4. **V2 has no OpenAPI spec or shared contracts package.** This means API shape changes are caught only at integration test time, not at compile time. For a 3-5 person team working in a single repository, this is acceptable, but it becomes a liability if the team grows or if external consumers (Sam-the-API-consumer) need typed bindings. V1's `@auth/contracts` package and OpenAPI stub would scale better. (Ref: V2 has no equivalent to V1 D1.3 or D1.4; diff C-003, C-004.)

---

## Shared Assumption Responses

- **A-001: ACCEPT.** Both variants assume 2-week sprints, 12 sprints total, team holds for duration. This is a standard agile assumption. V1's 15% buffer for attrition is a good practice, but V2's smaller team size (3-5 vs 6.5) means the absolute impact of losing one person is proportionally smaller.

- **A-002: ACCEPT.** Both assume PostgreSQL 15+ and Redis 7+ are externally provisioned. V2's fallback to Docker Compose for local development (V2 M1 Risks) is a practical hedge that does not change the production dependency.

- **A-003: ACCEPT.** Greenfield deployment eliminates migration complexity. Both variants benefit equally from this assumption.

- **A-004: ACCEPT.** Single-region for v1.0 is a pragmatic scoping decision. Cross-region complexity would dwarf the current roadmap in either variant.

- **A-005: QUALIFY.** The SOC2 Q3 2026 audit deadline is real and binding. V1 calls it out explicitly (Assumption 12); V2 embeds it implicitly in M6 scope. V2's approach is adequate IF the team treats M6 as non-negotiable. The risk is that without an explicit stated assumption, schedule pressure could compress M6. Mitigation: V2 M6 entry criteria require "at least 7 days of production traffic data," which creates a natural deadline forcing function.

- **A-006: ACCEPT.** NTP with < 1s drift is standard infrastructure. Both variants need this for JWT clock-skew tolerance.

- **A-007: QUALIFY.** Pen-test vendor availability with <= 4 weeks lead time is a common assumption but has no fallback in either variant. V2 makes this implicit (M6 Entry Criteria, "External penetration testing firm engaged and scheduled"). The qualification: if the vendor is unavailable, V2 can substitute an internal security team scan using OWASP ZAP as an interim measure, accepting higher risk for a delayed vendor engagement. Neither variant plans for this fallback, but V2's simpler security posture (no KMS, no HSM) means the attack surface for an internal scan is easier to validate.

---

## Focused Defense of V2 Positions

### 1. Build Order: Auth-First Delivers Value Sooner

V1 builds tokens first (M2), then auth endpoints (M3). V2 builds auth endpoints first (M2), then tokens (M3). The key question is: what can stakeholders validate at the M2 exit gate?

With V1's M2: A security reviewer can inspect `JwtService` and `TokenManager` library code, run property-based tests on rotation invariants, and benchmark signing performance. No user can register or log in. No integration tester can exercise the HTTP path. The value is purely internal and review-oriented.

With V2's M2: Stakeholders can register users, log in, observe audit log entries, trigger account lockout, and verify anti-enumeration behavior. The system is testable end-to-end (minus JWT tokens, which return a placeholder). Integration testers can exercise every login/register edge case. The security reviewer can review the same flows that users will experience.

V2's Sequencing Rationale (Section: "M2 before M3") argues: "AuthService registration and login must exist before token issuance can be integrated into them. The account lockout logic and anti-enumeration measures in M2 are security-critical and must be validated independently, before token logic adds complexity." This is the core argument: validate your security-critical auth logic in its simplest form, then layer token complexity on top. V1 does the reverse -- it adds token complexity first, then validates auth logic while also debugging token integration.

The retrofitting cost (V2 M3 D3.5/D3.6) is real but bounded: two deliverables, each estimated at ~1 day of work (V2 M3 Effort, "D3.5-D3.6 login/register updates (2 days)" out of a 4-week milestone). This is a small, well-defined integration task, not an architectural rework.

### 2. Data Durability: Graceful Degradation over Zero Loss

V1's `noeviction` + Postgres reset tokens posture is stronger in the absolute. But the question is whether the strength is needed for v1.0.

V2 M3 Risks (line 304) provides the sizing math: "100K tokens at ~500 bytes each = 50MB, well within 1GB allocation." Redis eviction under memory pressure requires memory pressure to exist. At 50MB used out of 1GB, the system must grow 20x before eviction becomes a possibility. V2's monitoring at 70% (70MB alert threshold) provides ample warning. The `allkeys-lru` policy is a safety valve for runaway growth, not an expected operational state.

For reset tokens specifically, V2 uses Redis with 1-hour TTL (V2 M4 D4.4). The worst case is: Redis is lost, and users who requested a reset in the last hour must request again. This is a minor inconvenience, not a security incident. V1's Postgres-backed reset tokens survive Redis loss, but at the cost of adding a database table, a migration, and `SELECT FOR UPDATE` transactional complexity for what is an inherently ephemeral operation (a 1-hour window).

V2's operational posture is explicit in its Redis risk (RR-05): "Redis cluster with replication; fallback: reject refresh (users re-login); alert at connection failures > 10/min." The fallback is user-visible (re-login required) but safe (no data corruption, no security gap). For v1.0 of a greenfield service with no existing users, this is the correct trade-off: optimize for operational simplicity and accept minor user inconvenience under failure.

### 3. Key Management: Ops Simplicity over Textbook Perfection

V1's KMS/HSM approach is the textbook answer for production JWT signing. No argument. But textbook answers have textbook costs:

- KMS provisioning requires security-team approval (V1 M2 Entry Criteria). This is a blocking external dependency.
- KMS integration code must be written, tested, and maintained. V1 M2 D2.3 ("KMS integration + ADR-002") is a deliverable.
- Local development must either mock KMS or use a local proxy. V1 does not specify how developers sign tokens locally.
- The KMS dependency creates a failure mode (R-DEP-1, probability Low, impact Critical) that requires a circuit breaker, local key cache, and readiness-probe exclusion logic.

V2's approach: "RSA key pair loaded from filesystem path (Kubernetes secret mount)" (V2 M3 D3.7). This is:

- Zero external dependencies. Kubernetes secrets are provisioned by the same team deploying the service.
- Trivial to develop locally (put a key file on disk).
- Adequately secure for v1.0: Kubernetes secrets are encrypted at rest in modern K8s, access-controlled by RBAC, and auditable via Kubernetes audit logs.
- Upgradeable to KMS post-GA without architectural change (load key from KMS instead of filesystem -- same interface).

V2's quarterly manual rotation (V2 M3 D3.7, "Documentation for quarterly rotation procedure") is less automated than V1's KMS-managed rotation, but for a greenfield service with no existing key-rotation infrastructure, manual rotation with a documented runbook is the right starting point. Automation can be added post-GA when the team has operational experience with the rotation procedure.

### 4. Spec-First vs Code-First: Agility for a Small Team

V1's OpenAPI 3.1 spec (M1 D1.4) and `@auth/contracts` package (M1 D1.3) represent approximately 2-3 days of upfront work (spec writing + JSON-schema authoring + npm package scaffolding + internal registry publish). For a team of 6.5 FTE building 6 endpoints, this investment pays for itself if the API shape changes frequently and those changes would otherwise cause integration bugs.

But V1's team is building a greenfield service with 6 endpoints (login, register, refresh, logout, me, reset-request, reset-confirm). The API shape is defined by the PRD and TDD. The probability of frequent API shape changes on a greenfield service with a detailed TDD is low. The PRD already specifies request/response shapes for every endpoint.

V2's code-first approach (define API contracts via TDD Section 8, validate via integration tests) is faster to start and avoids the maintenance burden of keeping an OpenAPI spec in sync with implementation. For a 3-5 person team, the coordination overhead of spec maintenance exceeds the integration-error savings.

Post-GA, when external consumers (Sam-the-API-consumer) need typed bindings, V2 can generate an OpenAPI spec from the existing implementation (a common practice using tools like `tsoa` or `nestjs/swagger`). This is additive work, not rework.

### 5. Frontend Coupling: Deferred Separation Reduces Risk for Small Teams

V1 couples frontend with backend (LoginPage, RegisterPage, AuthProvider ship in M3 alongside endpoints). This requires 2 FE engineers from Sprint 5 (V1 Section 2). The argument: no mock drift.

V2 separates frontend into M5 (Frontend Integration, Sprints 10-11). The argument (V2 Sequencing Rationale, "Alternative considered -- Frontend-first with mocked backend"): "Given the small team size (3-5 engineers), the serial approach reduces coordination overhead and eliminates mock-drift risk entirely."

Both approaches eliminate mock drift -- V1 by shipping together, V2 by not starting frontend until the backend is stable. The difference is team allocation:

- V1 requires FE engineers from Sprint 5 (7 sprints of engagement for 2 FE engineers).
- V2 requires FE engineers only for M5 (Sprints 10-11, 2 sprints of engagement for the frontend team).

For a startup/growth-stage company, dedicating 2 FE engineers for 14 weeks to an auth service may conflict with other product priorities. V2's 4-week FE engagement is a significantly smaller ask. The risk of frontend-to-backend mismatch is mitigated by V2's detailed TDD (which specifies exact endpoint contracts) and V2's integration tests (which validate the actual API shape). The frontend team in V2 builds against a frozen, tested API rather than a co-evolving one.

---

## Summary

V2 trades textbook perfection for pragmatic execution. It ships user-visible endpoints two sprints earlier, requires fewer dedicated headcount, embeds compliance instrumentation from M2 (not M5), includes GDPR erasure (which V1 omits), and provides state invariants that are automatically severity-classified. The concessions are real: endpoint retrofitting in M3, potential token eviction under memory pressure, no OpenAPI spec, and a retention-policy inconsistency. But each concession has a bounded, explicit mitigation documented within V2 itself. For a team with a hard Q2 deadline, a small headcount, and a greenfield codebase, V2 is the executable plan.
