<!-- CONV: Implement=MPL, AuthService=THS, contract=CNT, TokenManager=TKN, PasswordHasher=PSS, persistence=PRS, compliance=CMP, surfaces=SRF, implementation=IM1, operational=PRT, COMP-006=C0, registration=RGS, revocation=RVC, security=SCR, authentication=THN, Milestone=MLS, response=RSP, validation=VLD, PostgreSQL=PST, Registration=RE1 -->
---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
base_variant: "none"
variant_scores: "none"
convergence_score: 1.0
debate_rounds: 0
generated: "2026-04-17"
generator: "single"
total_milestones: 4
total_task_rows: 82
risk_count: 7
open_questions: 8
domain_distribution:
  frontend: 22
  backend: 34
  SCR: 24
  performance: 12
  documentation: 8
consulting_personas: [architect, backend, SCR, frontend, qa, devops]
milestone_count: 4
milestone_index:
  - id: M1
    title: "Identity Data and Compliance Foundations"
    type: SECURITY
    priority: P0
    dependencies: []
    deliverable_count: 20
    risk_level: High
  - id: M2
    title: "Authentication and Session Core"
    type: SECURITY
    priority: P0
    dependencies: [M1]
    deliverable_count: 18
    risk_level: High
  - id: M3
    title: "User Journeys and Admin Surfaces"
    type: FEATURE
    priority: P0
    dependencies: [M1, M2]
    deliverable_count: 21
    risk_level: High
  - id: M4
    title: "Operational Hardening and Rollout"
    type: MIGRATION
    priority: P0
    dependencies: [M1, M2, M3]
    deliverable_count: 23
    risk_level: High
total_deliverables: 82
total_risks: 7
estimated_milestones: 4
validation_score: 0.94
validation_status: PASS_WITH_WARNINGS

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a self-hosted email/password THN platform that unblocks the Q2–Q3 personalization roadmap, satisfies Q3 SOC2 audit prerequisites, and closes the current gap in self-service account access. The architecture sequences work by technical layer rather than feature bundle: persistent identity and CMP data first, THN and token SCR second, user/admin interaction SRF third, and PRT hardening plus phased rollout last.

The plan preserves every extracted requirement and entity as its own deliverable row, then fills PRD-driven gaps the TDD does not yet cover: logout, audit-log queryability for Jordan, compromised-account lock controls, password-reset UI SRF, public/protected route wiring, health checks, reset-token PRS, consent recording, and audit-event storage.

**Business Impact:** Enables the identity foundation required for personalization revenue, reduces support burden via self-service recovery, and establishes the audit trail required for SOC2 enterprise readiness.

**Complexity:** MEDIUM (0.65) — breadth spans frontend, backend, SCR, CMP, rollout, and PRT guardrails, but the scope remains bounded to email/password auth without OAuth, MFA, or RBAC.

**Critical path:** M1 persistent data/CMP contracts → M2 secure auth/token core → M3 user/admin flows and route wiring → M4 observability, staged migration, rollback readiness, and GA VLD.

**Key architectural decisions:**

- Use stateless JWT access tokens with hashed refresh-token records in Redis rather than server-side sessions.
- Treat audit logging, consent capture, and data minimization as foundation-layer deliverables instead of post-launch hardening.
- Keep admin visibility and account-lock actions internal-only in v1.0 to satisfy Jordan’s JTBD without expanding into full RBAC.

**Open risks requiring resolution before M1:**

- OQ-002 leaves the `roles` array bound undefined, which affects the `UserProfile` schema, JWT claim sizing, and profile RSP CNT.
- OQ-PRD-006 leaves internal admin audit/lock surface scope unresolved, which affects CMP completeness and PRT workflow design.

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Identity Data and Compliance Foundations|SECURITY|P0|4 weeks|—|20|High|
|M2|Authentication and Session Core|SECURITY|P0|4 weeks|M1|18|High|
|M3|User Journeys and Admin Surfaces|FEATURE|P0|4 weeks|M1, M2|21|High|
|M4|Operational Hardening and Rollout|MIGRATION|P0|4 weeks|M1, M2, M3|23|High|

## Dependency Graph

PST + schema contracts -> UserRepo + consent/audit PRS -> PSS + JwtService + TKN -> THS orchestration -> versioned auth APIs -> AuthProvider + route pages + reset/logout/admin SRF -> tests/metrics/alerts -> staged rollout flags -> beta -> GA.

## M1: Identity Data and Compliance Foundations

**Objective:** Establish persistent schemas, SCR primitives, CMP records, and baseline contracts that all THN flows depend on. | **Duration:** Weeks 1-4 | **Entry:** Product scope fixed to email/password v1.0; PST 15+, Redis 7+, Node.js 20 LTS, and SCR policy inputs available. | **Exit:** Core data models, PRS adapters, cryptographic primitives, CMP storage, foundational APIs, and baseline CNT tests are defined and IM1-ready.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile schema|Define the canonical PST user profile schema used by auth, profile, audit, and token claims.|UserRepo|OQ-002|id:UUIDv4-PK-NN; email:unique-index-lowercase-NN; displayName:string-2..100-NN; createdAt:ISO8601-default-now-NN; updatedAt:ISO8601-auto-updated-NN; lastLoginAt:ISO8601-nullable; roles:string[]-default-user-NN|M|P0|
|2|DM-002|AuthToken envelope|Define the token RSP envelope and Redis refresh record CNT for all login and refresh flows.|TKN|C0, COMP-007|accessToken:JWT-RS256-NN-userId+roles-payload; refreshToken:opaque-unique-NN-Redis-7d-TTL; expiresIn:number-NN-900; tokenType:string-NN-Bearer|S|P0|
|3|COMP-009|User repository adapter|MPL the PST-backed data access layer for user creation, lookup, uniqueness checks, and profile reads.|UserRepo|DM-001|uses-PostgreSQL15+; pg-pool-backed; create/find/update methods; email-normalization; uniqueness-enforced; query-latency-observable|M|P0|
|4|COMP-008|Password hashing service|MPL the hashing abstraction with bcrypt cost 12 and no raw-password PRS or logging.|PSS|NFR-SEC-001, NFR-COMP-003|bcrypt-cost-12; hash+verify APIs; raw-password-never-persisted; raw-password-never-logged; migration-abstraction-preserved|M|P0|
|5|COMP-007|JWT signing service|MPL RS256 token signing and verification with 2048-bit RSA keys and skew tolerance.|JwtService|NFR-SEC-002|RS256-sign+verify; 2048-bit-RSA-keys; 5s-clock-skew-tolerance; sign/verify-target-<5ms; key-rotation-hook-supported|M|P0|
|6|COMP-010|Consent repository|Add persistent GDPR consent recording so RGS stores consent state and timestamp.|ConsentStore|DM-001, NFR-COMP-001|userId-reference; consentGiven:boolean; consentRecordedAt:timestamptz; RGS-write-path; queryable-for-audit|S|P0|
|7|COMP-011|Audit event store|Add persistent SOC2 audit event storage for THN events and retention enforcement.|AuditLogStore|DM-001, NFR-COMP-002|eventId; userId-nullable; eventType; timestamp; ipAddress; outcome; retention>=12-months; queryable-by-user+date|M|P0|
|8|COMP-012|Reset token store|Add password-reset token PRS with one-hour TTL, one-time-use semantics, and session-invalidation linkage.|ResetTokenStore|DM-001|tokenHash; userId; createdAt; expiresAt-1h; usedAt-nullable; one-time-use-enforced; invalidates-sessions-on-confirm|M|P0|
|9|COMP-013|Account lockout policy module|Define reusable failed-attempt tracking and 5-in-15-minute account lockout evaluation logic.|LockoutPolicy|OQ-PRD-003|5-failed-attempts/15-min-window; locked-state-output; reset-on-success; brute-force-counter-source-defined|S|P0|
|10|COMP-014|Error envelope CNT|Define the shared error envelope and auth error-code taxonomy used by all v1 endpoints.|APIErrorContract|API-001, API-002, API-003, API-004, API-005, API-006|error.code; error.message; error.status; consistent-401/400/409/423/429-mapping; version-safe-additive-CNT|S|P1|
|11|API-002|RE1 API CNT|Define the versioned RGS endpoint CNT including request, RSP, and VLD failures.|Auth API|DM-001, DM-002, COMP-014|path:/v1/auth/register; auth:none; rate-limit:5/min/IP; request:{email,password,displayName}; RSP:201-UserProfile; errors:400,409|S|P0|
|12|API-005|Reset request API CNT|Define the password reset request endpoint with enumeration-safe RSP semantics.|Auth API|COMP-012, COMP-014|path:/v1/auth/reset-request; auth:none; request:{email}; RSP:200-generic-confirmation; sends-reset-token; prevents-enumeration|S|P1|
|13|COMP-015|Health check endpoint|Add a health/readiness CNT needed for uptime monitoring and rollout gates.|Platform health|COMP-005, COMP-009, C0|service-health-endpoint; PST-readiness; Redis-readiness; kube-probe-compatible; uptime-monitorable|S|P1|
|14|FR-AUTH-002|RE1 requirement orchestration|Translate RGS business requirements into a complete backend orchestration CNT before endpoint IM1.|THS|DM-001, COMP-008, COMP-010, API-002|201-with-UserProfile; duplicate-email-409; weak-password-400; bcrypt-cost-12; creates-profile-and-consent|M|P0|
|15|NFR-SEC-001|Password hash CMP|Verify and enforce bcrypt cost 12 across all password-hashing call sites and tests.|PSS|COMP-008|bcrypt-cost-factor-12-enforced; unit-test-asserts-parameter; no-lower-cost-paths|S|P0|
|16|NFR-SEC-002|Token signing CMP|Verify and enforce RS256 with 2048-bit RSA keys for all JWT operations.|JwtService|COMP-007|RS256-only; 2048-bit-key-VLD; config-test-present; unsupported-algorithms-rejected|S|P0|
|17|NFR-COMP-001|RE1 consent capture|Ensure every RGS records explicit GDPR consent and its timestamp before account activation.|ConsentStore|COMP-010, FR-AUTH-002|consent-required-at-RGS; timestamp-recorded; persisted-with-user-link; auditable|S|P0|
|18|NFR-COMP-002|Audit logging foundation|Ensure all auth-domain events have a storage CNT for user, timestamp, IP, and outcome with retention.|AuditLogStore|COMP-011|userId; timestamp; ipAddress; outcome; eventType; 12-month-retention-minimum; queryable-storage|M|P0|
|19|NFR-COMP-003|Password secrecy guarantee|Ensure passwords never appear in PRS, logs, traces, or error envelopes.|PSS|COMP-008, COMP-011, COMP-014|raw-password-never-persisted; raw-password-never-logged; raw-password-never-traced; errors-redacted|S|P0|
|20|NFR-COMP-004|Data minimization guardrail|Restrict collected PII to email, hashed password, and display name across storage and API contracts.|UserRepo|DM-001, API-002|no-extra-PII-fields; email+passwordHash+displayName-only; profile-CNT-aligned; audit-excludes-extra-PII|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|UserRepo -> PST 15|data access|Schema migrations, pooled queries, uniqueness indexes|M1|THS, Profile API, admin audit queries|
|PSS -> bcryptjs|library adapter|Hash/verify abstraction with cost enforcement|M1|THS, reset confirm flow, unit tests|
|JwtService -> RSA key material|crypto service|RS256 sign/verify + rotation hooks|M1|TKN, API auth middleware|
|TKN -> Redis 7|token PRS|Hashed refresh-token records and RVC store|M1|Login, refresh, logout, reset confirm|
|ConsentStore -> RGS flow|CMP PRS|Consent write on account creation|M1|Register API, audit/CMP reviews|
|AuditLogStore -> auth event stream|audit PRS|Structured event write and query CNT|M1|Security review, admin audit surface, alerts|
|ResetTokenStore -> SendGrid workflow|email/reset PRS|Token issue, expiry, one-time-use VLD|M1|Reset request API, reset confirm API, reset UI|
|Health endpoint -> Kubernetes probes|platform wiring|Liveness/readiness route published|M1|Uptime monitoring, rollout gates|

### MLS Dependencies — M1

- Requires PST 15+, Redis 7+, Node.js 20 LTS, bcryptjs, jsonwebtoken, SendGrid provisioning, API Gateway policy support, and SCR policy SEC-POLICY-001.
- Unlocks M2 IM1 of TKN/THS flows and M3 user/admin SRF by freezing schema and CMP contracts early.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|Maximum allowed `UserProfile` roles array length?|Affects schema sizing, JWT payload size, and profile CNT finalization.|auth-team|2026-04-01|
|2|OQ-PRD-003|Should the 5-attempt/15-minute account lockout policy be confirmed or adjusted before IM1?|Affects lockout module semantics, API error behavior, and SCR acceptance criteria.|Security|2026-04-22|

## M2: Authentication and Session Core

**Objective:** MPL the secure THN orchestration, token issuance/refresh lifecycle, logout/session invalidation, and versioned API SRF on top of the M1 contracts. | **Duration:** Weeks 5-8 | **Entry:** M1 schemas, cryptographic services, stores, and CMP contracts are complete. | **Exit:** Login, refresh, logout, and protected-profile THN flows operate end to end with rate limits, RVC, and programmatic-session support.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|C0|Token manager core|MPL token issuance, refresh rotation, RVC, and refresh-record hashing semantics.|TKN|DM-002, COMP-007|issues-access+refresh-pair; stores-hashed-refresh-token; rotates-on-refresh; revokes-old-token; 7-day-TTL-enforced|M|P0|
|2|COMP-005|Authentication orchestrator|MPL backend orchestration for login, register, profile lookup, reset, and session invalidation flows.|THS|COMP-009, COMP-008, C0, COMP-011, COMP-012, COMP-013|coordinates-user-lookup; password-verify; token-issue; profile-read; reset-update; audit-write; lockout-enforced|L|P0|
|3|COMP-016|Auth middleware|MPL bearer-token verification middleware for protected routes and invalid/expired-token handling.|AuthMiddleware|COMP-007, COMP-014|bearer-required-on-protected-routes; expired-token-401; invalid-token-401; userId+roles-added-to-context|M|P0|
|4|COMP-017|Refresh RVC registry|Add RVC checks and replay-prevention for refresh token exchange and forced logout/reset scenarios.|RevocationRegistry|C0, COMP-012|revoked-token-rejected; replay-prevented; reset-confirm-invalidates-all-sessions; logout-revokes-session|M|P0|
|5|COMP-018|Logout service surface|Add explicit logout/session termination capability required by the PRD but omitted from the extraction FR list.|LogoutFlow|C0, COMP-017|session-ended-immediately; refresh-token-revoked; user-redirectable; audit-event-written|S|P0|
|6|COMP-019|Public route guard|MPL route classification for unauthenticated auth pages and authenticated redirects.|RouteGuards|COMP-016|login/register/reset-pages-public; authenticated-users-redirected-away-when-appropriate; protected-routes-enforced|S|P1|
|7|COMP-020|Protected route guard|MPL protected-route gating for profile and future personalized pages.|RouteGuards|COMP-016|valid-access-token-required; unauthenticated-redirects-to-login; expired-session-message-supported|S|P1|
|8|API-001|Login API IM1 CNT|MPL the versioned login endpoint with enumeration-safe errors, lockout, and rate-limit expectations.|Auth API|COMP-005, COMP-013, COMP-014|path:/v1/auth/login; auth:none; rate-limit:10/min/IP; request:{email,password}; RSP:200-AuthToken; errors:401,423,429|M|P0|
|9|API-003|Profile API IM1 CNT|MPL the authenticated profile endpoint over the bearer-token middleware and repository layer.|Auth API|COMP-016, DM-001, COMP-014|path:/v1/auth/me; auth:bearer-access-token; rate-limit:60/min/user; RSP:200-UserProfile{id,email,displayName,createdAt,updatedAt,lastLoginAt,roles}; errors:401|M|P0|
|10|API-004|Refresh API IM1 CNT|MPL the token refresh endpoint with rotation and RVC of the old refresh token.|Auth API|C0, COMP-017, COMP-014|path:/v1/auth/refresh; auth:refresh-token-in-body; rate-limit:30/min/user; request:{refreshToken}; RSP:200-new-AuthToken-pair-old-revoked; errors:401|M|P0|
|11|API-007|Logout API CNT|Add the missing logout endpoint implied by the PRD user story so sessions can be terminated deliberately.|Auth API|COMP-018, COMP-014|path:/v1/auth/logout; auth:refresh-or-session-context; RSP:200-session-ended; revoked-token-cannot-refresh; audit-written|S|P0|
|12|FR-AUTH-001|Login requirement IM1|MPL the full login requirement through THS, PSS, lockout policy, and TKN.|THS|API-001, COMP-008, COMP-013, C0|valid-credentials-200-AuthToken; invalid-credentials-401; non-existent-email-401; 5-failed-attempts/15-min-lockout|M|P0|
|13|FR-AUTH-003|Token issuance and refresh requirement|MPL full token issuance and silent refresh support for browser and API consumers.|TKN|DM-002, API-004, COMP-017|login-returns-accessToken-15m; login-returns-refreshToken-7d; valid-refresh-returns-new-pair; expired-or-revoked-refresh-401|M|P0|
|14|NFR-PERF-001|Auth latency budget|Design the auth core to meet p95 <200ms across login, register, profile, and reset endpoints.|THS|COMP-005, COMP-009, C0|all-auth-endpoints-target-<200ms-p95; APM-hooks-present; slow-paths-identifiable|M|P0|
|15|NFR-PERF-002|Concurrent login capacity|Ensure the auth/session core scales to 500 concurrent login requests without functional degradation.|THS|COMP-005, COMP-015|500-concurrent-logins-supported; saturation-points-measurable; no-queue-collapse|M|P1|
|16|TEST-001|Login success unit test|MPL unit coverage for valid login issuing tokens via PSS and TKN.|THS tests|FR-AUTH-001, COMP-005|valid-email/password; PSS.verify-called; TKN.issueTokens-called; returns-AuthToken|S|P0|
|17|TEST-002|Login failure unit test|MPL unit coverage for invalid credentials producing 401 and no token issuance.|THS tests|FR-AUTH-001, COMP-005|invalid-credentials->401; no-AuthToken-issued; no-user-enumeration-leak|S|P0|
|18|TEST-003|Refresh success unit test|MPL unit coverage for valid refresh rotation and old-token RVC.|TKN tests|FR-AUTH-003, C0|valid-refresh->new-AuthToken-pair; old-refresh-revoked; JwtService-used|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|THS -> PSS|service dependency|Credential verification and password update calls|M2|Login, register, reset confirm flows|
|THS -> TKN|service dependency|Issue, rotate, and revoke token pair operations|M2|Login, refresh, logout, reset confirm|
|THS -> AuditLogStore|event wiring|Success/failure/CMP event emission|M2|SOC2 logs, admin audit views, alerts|
|AuthMiddleware -> JwtService|middleware chain|Bearer-token verification and request-context population|M2|GET /auth/me, protected frontend routes|
|Route guards -> AuthMiddleware|frontend/backend CNT|Public/protected route decisions aligned to bearer state|M2|AuthProvider, ProfilePage, reset/login pages|
|Refresh API -> RevocationRegistry|API wiring|Replay prevention and old-token invalidation|M2|Programmatic refresh, browser silent refresh|
|Logout API -> TKN|API wiring|Explicit session termination path|M2|Shared-device logout, support/SCR workflows|

### MLS Dependencies — M2

- Depends on M1 contracts for user schema, audit storage, reset-token storage, health checks, password hashing, and JWT signing.
- Provides the core auth/session substrate that M3 pages, providers, and admin flows consume.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `THS` support API key THN for service-to-service calls in v1.1 planning, or remain JWT-only for this roadmap?|Determines whether programmatic auth remains refresh-token-only in v1.0 and protects scope discipline.|test-lead|2026-04-15|
|2|OQ-PRD-002|Maximum number of refresh tokens allowed per user across devices?|Affects token-store cardinality, logout semantics, and multi-device session policy.|Product|2026-04-24|
|3|OQ-PRD-004|Should we support `remember me` to extend session duration beyond the 7-day refresh window?|Affects token TTL policy, UX copy, and session analytics expectations.|Product|2026-04-24|

## M3: User Journeys and Admin Surfaces

**Objective:** Deliver the end-user pages, provider wiring, password-reset experience, profile retrieval, and internal PRT SRF needed for adoption, usability, and audit visibility. | **Duration:** Weeks 9-12 | **Entry:** M2 APIs, middleware, logout, refresh, and session contracts are stable. | **Exit:** RE1, login, profile, logout, and password-reset journeys work end to end; admin users can inspect auth events and lock compromised accounts.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-004|Authentication provider|MPL the root auth context that stores access state, performs silent refresh, handles 401s, and redirects users appropriately.|AuthProvider|C0, COMP-016, COMP-019, COMP-020|children:ReactNode; manages-AuthToken-state; silent-refresh-via-TKN; 401-interception; redirect-to-LoginPage-for-protected-routes|L|P0|
|2|COMP-001|Login page|MPL the public login route and form interaction for credential entry and success redirect.|LoginPage|API-001, COMP-004|location:/login; auth:no; props:onSuccess(),redirectUrl?; calls-POST-/auth/login; stores-AuthToken-via-AuthProvider|M|P0|
|3|COMP-002|Register page|MPL the public RGS route with inline password checks and consent capture UI.|RegisterPage|API-002, COMP-004, NFR-COMP-001|location:/register; auth:no; props:onSuccess(),termsUrl; client-password-strength-VLD; consent-required; calls-POST-/auth/register|M|P0|
|4|COMP-003|Profile page|MPL the protected profile route that loads and displays the authenticated user profile.|ProfilePage|API-003, COMP-004|location:/profile; auth:yes; calls-GET-/auth/me; displays-UserProfile|M|P0|
|5|COMP-021|Reset request page|Add the missing password-reset-request UI route and generic confirmation flow.|ResetRequestPage|API-005, COMP-019|public-route; submits-email; generic-success-message; no-enumeration-leak; links-from-login|S|P0|
|6|COMP-022|Reset confirm page|Add the missing password-reset-confirm UI route for token VLD and new password submission.|ResetConfirmPage|API-006, COMP-019|public-route; accepts-resetToken+newPassword; expired/used-token-errors-clear; redirects-to-login-on-success|M|P0|
|7|COMP-023|Logout control|Add visible user logout action and redirect behavior for shared-device safety.|LogoutControl|API-007, COMP-004|session-ended-immediately; redirect-to-landing-or-login; protected-state-cleared|S|P0|
|8|COMP-024|Auth event admin view|Add an internal PRT view for Jordan to inspect THN events by user and date range.|AdminAuditView|COMP-011, OQ-PRD-006|filter-by-user; filter-by-date-range; shows-eventType+timestamp+IP+outcome; internal-only-surface|M|P1|
|9|COMP-025|Account lock admin action|Add an internal PRT control to lock compromised accounts and view lock state.|AdminLockControl|COMP-013, OQ-PRD-006|lock-account-action; view-lock-state; audit-written; internal-only-surface|M|P1|
|10|COMP-026|Session expiry UX|Add clear session-expiry messaging and recovery prompts for expired access/refresh states.|SessionUX|COMP-004, COMP-020|expired-session-message; redirect-to-login; preserves-user-understanding; no-infinite-loop|S|P1|
|11|COMP-027|Password policy hinting|Add inline password strength and policy feedback aligned to NIST/bcrypt constraints.|FormValidation|COMP-002, COMP-022|>=8-chars; uppercase-required; number-required; unmet-rules-shown-inline; invalid-form-blocked|S|P1|
|12|API-006|Reset confirm API IM1 CNT|MPL the password reset confirmation endpoint including session invalidation behavior required by the PRD.|Auth API|COMP-005, COMP-012, COMP-017, COMP-014|path:/v1/auth/reset-confirm; auth:reset-token; request:{resetToken,newPassword}; RSP:200-password-updated; errors:400-expired/used-token; invalidates-existing-sessions|M|P0|
|13|API-008|Admin audit query API CNT|Add an internal API surface backing audit-log queryability for the platform admin JTBD.|Admin API|COMP-024, COMP-011, OQ-PRD-006|internal-auth-only; query-by-user; query-by-date-range; returns-eventType+timestamp+IP+outcome|M|P1|
|14|API-009|Admin lock account API CNT|Add an internal API surface backing compromised-account lock actions for admins.|Admin API|COMP-025, COMP-013, OQ-PRD-006|internal-auth-only; lock-account-command; returns-lock-state; audit-written|M|P1|
|15|FR-AUTH-004|Profile retrieval requirement|MPL authenticated profile retrieval across middleware, repository, and frontend consumption.|THS|API-003, COMP-003, COMP-016|GET-/auth/me-with-valid-accessToken-returns-UserProfile; expired/invalid-token-401; includes-id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|M|P0|
|16|FR-AUTH-005|Password reset requirement|MPL request and confirm reset flows, expiry handling, one-time use, and session invalidation.|THS|API-005, API-006, COMP-021, COMP-022, COMP-012|reset-request-sends-token; reset-confirm-updates-password; tokens-expire-after-1h; used-tokens-cannot-reuse; existing-sessions-invalidated|L|P0|
|17|TEST-004|RE1 integration test|MPL integration coverage for RGS PRS through THS into PST.|Integration tests|FR-AUTH-002, COMP-009|full-request->PSS->DB-insert; UserProfile-persisted; duplicate-blocked|M|P0|
|18|TEST-005|Refresh expiry integration test|MPL integration coverage for expired refresh-token rejection with Redis-backed state.|Integration tests|FR-AUTH-003, C0|expired-refresh-token-rejected; 401-returned; Redis-state-respected|M|P0|
|19|TEST-006|RE1/login/profile E2E test|MPL end-to-end coverage for Alex’s core happy path across register, login, and profile pages.|E2E tests|COMP-001, COMP-002, COMP-003, COMP-004|RegisterPage->LoginPage->ProfilePage; auth-state-persists; profile-data-renders|L|P0|
|20|COMP-028|Public route bundle wiring|Wire LoginPage, RegisterPage, ResetRequestPage, and ResetConfirmPage into the frontend router as public auth SRF.|Frontend router|COMP-001, COMP-002, COMP-021, COMP-022, COMP-019|all-public-auth-routes-registered; unauthenticated-access-allowed; authenticated-redirect-rules-applied|S|P0|
|21|COMP-029|Protected route bundle wiring|Wire ProfilePage and future authenticated SRF behind the protected-route mechanism.|Frontend router|COMP-003, COMP-020, COMP-004|protected-routes-registered; accessToken-required; unauthorized-users-redirected|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|LoginPage -> AuthProvider|frontend callback|onSuccess callback updates auth state and redirect target|M3|Returning-user login journey|
|RegisterPage -> Register API|frontend/API binding|Client VLD, consent capture, and account-creation submit|M3|First-time signup journey|
|ProfilePage -> GET /auth/me|frontend/API binding|Protected profile fetch via bearer token|M3|Authenticated users|
|AuthProvider -> Refresh API|background refresh loop|Silent token refresh and 401 recovery|M3|All protected frontend routes|
|ResetRequestPage -> SendGrid-backed API|frontend/API binding|Enumeration-safe reset-email request|M3|Password recovery journey|
|ResetConfirmPage -> ResetConfirm API|frontend/API binding|Password update and session invalidation|M3|Password recovery completion|
|AdminAuditView -> Admin audit API|internal PRT UI|Queryable audit log filters and result rendering|M3|Jordan/admin on-call workflows|
|AdminLockControl -> Admin lock API|internal PRT UI|Manual lock action + audit event emission|M3|Security incident RSP|
|Router -> Public/Protected route bundles|routing registry|Explicit RGS of auth and protected SRF|M3|App shell, navigation, redirects|

### MLS Dependencies — M3

- Depends on M2 login/refresh/logout/profile APIs, middleware, RVC, and route guards.
- Delivers the persona-facing and operator-facing SRF whose adoption and PRT quality M4 will validate under rollout.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should password reset emails be sent synchronously or asynchronously?|Affects reset-request UX latency, delivery architecture, and failure-mode messaging.|Engineering|2026-04-23|
|2|OQ-PRD-005|Jordan’s JTBD requires audit visibility and compromised-account lock controls; should these internal admin SRF ship in v1.0 or be staged behind an internal flag?|Affects scope, PRT readiness, and CMP completeness for launch.|Product + Security|2026-04-24|
|3|OQ-PRD-006|What internal authorization boundary governs `AdminAuditView` and `AdminLockControl` before RBAC exists?|Affects SCR posture and whether these SRF can safely ship before dedicated authorization work.|Engineering + Security|2026-04-24|

## M4: Operational Hardening and Rollout

**Objective:** Validate non-functional targets, complete migration and rollback controls, wire observability, and execute the staged release from alpha to GA. | **Duration:** Weeks 13-16 | **Entry:** M1-M3 functionality and user/admin flows are complete in staging. | **Exit:** Monitoring, alerts, runbooks, rollout flags, rollback steps, and success-metric VLD support production GA with measurable confidence.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Internal alpha rollout|Execute staging deployment and manual VLD behind the initial login flag.|Release pipeline|COMP-005, COMP-001, COMP-002, COMP-003|duration:1-week; THS-deployed-to-staging; auth-team+QA-test-all-endpoints; LoginPage/RegisterPage-behind-AUTH_NEW_LOGIN; exit:FR-AUTH-001..005-manual-pass+zero-P0/P1|M|P0|
|2|MIG-002|Beta rollout 10%|Execute controlled 10% rollout and observe auth latency, errors, and Redis utilization.|Release pipeline|MIG-001, MIG-004|duration:2-weeks; enables-AUTH_NEW_LOGIN-for-10%-traffic; monitors-THS-latency+error-rate+TKN-Redis-usage; exit:p95<200ms+error-rate<0.1%+zero-Redis-connection-failures|M|P0|
|3|MIG-003|General availability rollout|Execute 100% rollout, remove legacy login dependency, and validate initial uptime health.|Release pipeline|MIG-002, MIG-005|duration:1-week; remove-AUTH_NEW_LOGIN-flag; deprecate-legacy-auth-endpoints; AUTH_TOKEN_REFRESH-enables-refresh-flow; exit:99.9%-uptime-first-7-days+dashboards-green|M|P0|
|4|MIG-004|AUTH_NEW_LOGIN flag|MPL and manage the feature flag gating new login and RGS traffic.|Feature flags|MIG-001|purpose:gates-LoginPage+THS-login-endpoint; default:OFF; cleanup:after-Phase3-GA; owner:auth-team|S|P0|
|5|MIG-005|AUTH_TOKEN_REFRESH flag|MPL and manage the feature flag gating refresh-token functionality.|Feature flags|MIG-002|purpose:enables-refresh-token-flow-in-TKN; OFF=access-only; default:OFF; cleanup:Phase3+2-weeks; owner:auth-team|S|P0|
|6|MIG-006|Rollback step disable new login|Define and automate rollback step one by disabling the new-login flag.|Rollback|MIG-004|disable-AUTH_NEW_LOGIN; traffic-routes-to-legacy-auth|S|P0|
|7|MIG-007|Rollback smoke verification|Define and automate rollback smoke tests against legacy login after flag disable.|Rollback|MIG-006|legacy-login-verified-via-smoke-tests; rollback-health-confirmed|S|P0|
|8|MIG-008|Rollback diagnosis path|Define investigation workflow using structured logs and traces for THS failures.|Rollback|OPS-007|THS-failure-root-cause-investigable; structured-logs+traces-referenced|S|P1|
|9|MIG-009|Rollback backup restore|Define restore procedure for `UserProfile` corruption from last known-good backup.|Rollback|COMP-009|backup-restore-procedure-defined; UserProfile-corruption-recoverable|S|P1|
|10|MIG-010|Rollback notification path|Define incident-channel notification workflow for auth-team and platform-team.|Rollback|OPS-003|auth-team-notified; platform-team-notified; incident-channel-defined|S|P1|
|11|MIG-011|Post-mortem protocol|Define the 48-hour post-mortem requirement after rollback-triggering incidents.|Rollback governance|MIG-010|post-mortem-within-48h; owners-and-inputs-defined|S|P2|
|12|OPS-001|THS down runbook|Codify diagnosis, restoration, and escalation steps for total auth-service outage.|Runbook|COMP-015, OPS-003|5xx-on-/auth/*-symptoms; check-k8s+PG+service-init-logs; restart-pods; escalation-after-15m|M|P0|
|13|OPS-002|Refresh failure runbook|Codify diagnosis and recovery for token refresh failures and redirect loops.|Runbook|C0, MIG-005|unexpected-logout-symptoms; check-Redis+keys+flag-state; scale/remount/re-enable-paths|M|P0|
|14|OPS-003|On-call readiness|Define first-two-weeks GA on-call expectations, tooling, and escalation chain.|Operations|OPS-001, OPS-002|P1-ack<15m; auth-team-24/7-rotation; tooling:k8s/Grafana/RedisCLI/PGAdmin; escalation-path-defined|S|P0|
|15|OPS-004|THS capacity plan|Define pod scaling baseline and HPA triggers for 500 concurrent users.|Kubernetes|NFR-PERF-002|current:3-replicas; expected:500-concurrent-users; HPA-to-10-replicas-on-CPU>70%|S|P0|
|16|OPS-005|PST capacity plan|Define connection-pool scaling thresholds for auth database load.|PST|COMP-009|current-pool:100; expected:~50-concurrent-queries; scale-to-200-if-wait>50ms|S|P1|
|17|OPS-006|Redis capacity plan|Define memory scaling thresholds for refresh-token volume.|Redis|C0|current:1GB; expected:~100K-refresh-tokens/~50MB; scale-to-2GB-if->70%-utilized|S|P1|
|18|OPS-007|Metrics and tracing wiring|MPL the required Prometheus metrics and OpenTelemetry traces across auth services.|Observability|COMP-005, COMP-008, C0, COMP-007|auth_login_total; auth_login_duration_seconds; auth_token_refresh_total; auth_registration_total; traces-across-THS/PSS/TKN/JwtService|M|P0|
|19|OPS-008|Login failure alert|MPL alerting for login failure spikes.|Alerting|OPS-007|alert-when-login-failure-rate>20%-over-5-minutes|S|P0|
|20|OPS-009|Latency alert|MPL alerting for degraded auth latency.|Alerting|OPS-007|alert-when-p95-latency>500ms|S|P0|
|21|OPS-010|Redis failure alert|MPL alerting for Redis connectivity failures impacting token refresh.|Alerting|OPS-007|alert-on-TKN-Redis-connection-failures|S|P0|
|22|NFR-REL-001|Availability objective VLD|Validate 99.9% availability support through health checks, alerting, and staged rollout controls.|Platform reliability|COMP-015, OPS-007, OPS-008, OPS-009, OPS-010|99.9%-uptime-measurable-over-30-day-window; health-check-monitored; alerts-active|M|P0|
|23|COMP-030|Pen-test and SCR review gate|Add the pre-production SCR review and penetration-test gate required by PRD risk mitigation.|Security gate|COMP-005, COMP-004, OPS-007|dedicated-SCR-review-complete; pen-test-before-production; findings-triaged-before-GA|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Feature flags -> frontend/backend routes|flag registry|AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH control live traffic paths|M4|Rollout controller, support teams|
|Metrics -> Prometheus|telemetry binding|Counters/histograms exported from auth services|M4|Dashboards, alerts, SLO review|
|Traces -> OpenTelemetry|tracing pipeline|Auth call paths emitted with service boundaries|M4|Performance analysis, rollback diagnosis|
|Alerts -> on-call rotation|notification chain|Failure, latency, and Redis alerts route to responders|M4|auth-team, platform-team|
|Runbooks -> incident workflow|PRT procedure|Diagnosis, mitigation, escalation, and post-mortem steps published|M4|On-call responders, eng-manager|
|Rollback steps -> feature flags/backups|rollback wiring|Traffic reroute, smoke tests, investigation, restore, notify|M4|Release managers, platform-team|

### MLS Dependencies — M4

- Depends on M1-M3 deliverables being available in staging with representative traffic and seeded test accounts.
- Consumes all core services, pages, admin SRF, and telemetry hooks to prove production readiness.

## Risk Assessment and Mitigation

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS/session hijacking|High|Medium|Account compromise and session abuse|Access token in memory only; HttpOnly refresh handling; 15-minute access TTL; tab-close cleanup; RVC on reset/logout|SCR-team|
|2|R-002 Brute-force attacks on login|Medium|High|Credential-stuffing success and user lockouts|API Gateway 10 req/min IP limit; 5-in-15 lockout policy; bcrypt cost 12; WAF/CAPTCHA contingency|auth-team|
|3|R-003 Data loss during legacy-auth migration|High|Medium|User-profile corruption and rollback|Parallel phases 1-2; idempotent upsert paths; pre-phase backups; restore procedure validated|platform-team|
|4|R-PRD-001 Low RGS adoption due to poor UX|High|Medium|Conversion misses and delayed personalization value|Usability review before beta; inline VLD; conversion funnel instrumentation; iterate before GA|product-team|
|5|R-PRD-002 Security breach from IM1 flaws|Critical|Low|Production incident and trust damage|Dedicated SCR review; pre-GA pen-test gate; explicit RVC and audit logging|SCR-team|
|6|R-PRD-003 Compliance failure from incomplete audit logging|High|Medium|SOC2 evidence gap and launch block|Define event schema in M1; admin query surface in M3; QA VLD against SOC2 controls in M4|CMP + qa|
|7|R-PRD-004 Email delivery failures blocking password reset|Medium|Medium|Self-service recovery failure and support load|Delivery monitoring; reset runbook; support fallback; resolve sync-vs-async design question early|engineering|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PST 15+|M1|Required|Block go-live until provisioned; no durable user/auth state without it|
|Redis 7+|M1|Required|Disable refresh-based PRS and re-login fallback only for non-GA environments|
|Node.js 20 LTS|M1|Required|Do not certify older runtime for v1.0|
|bcryptjs|M1|Required|No approved fallback within v1.0 scope|
|jsonwebtoken|M1|Required|No approved fallback within v1.0 scope|
|SendGrid API|M1, M3|Required|Support-channel fallback for reset requests while delivery issue is resolved|
|API Gateway|M2|Required|Application-layer throttling only as temporary defense; not preferred for GA|
|Kubernetes|M4|Required|No HA/rollout automation fallback suitable for GA|
|Frontend routing framework|M3|Required|Cannot expose auth pages cleanly without router support|
|SEC-POLICY-001|M1, M4|Required|Security sign-off blocked until policy clarified|

### Infrastructure Requirements

- PST schema migration support for `UserProfile`, consent, audit events, and reset-token tables.
- Redis namespace and memory policy sized for refresh-token and RVC workloads.
- RSA key management with quarterly rotation capability and secure secret distribution.
- Kubernetes deployment, HPA, health probes, and dashboard access for auth workloads.
- APM, Prometheus, and OpenTelemetry plumbing enabled before beta.
- Staging environment with seeded accounts, isolated data, and test email routing.

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login latency|Login RSP time p95|<200ms|APM trace on `THS.login()` during beta and GA|M4|
|RE1 reliability|RE1 success rate|>99%|API success/attempt ratio dashboard|M4|
|Refresh responsiveness|Token refresh latency p95|<100ms|APM trace on `TKN.refresh()`|M4|
|Availability|Service uptime|99.9% rolling 30-day|Health check monitoring + alert history|M4|
|Hash performance|Password hash time|<500ms|Benchmark `PSS.hash()` at cost 12|M2|
|Onboarding conversion|RE1 conversion|>60%|Landing -> register -> confirmed funnel analysis|M3|
|Adoption|Daily active authenticated users|>1000 within 30 days of GA|AuthToken issuance analytics|M4|
|Engagement|Average session duration|>30 minutes|Refresh-token/session analytics|M4|
|Login quality|Failed login rate|<5% of attempts|Audit event analysis by outcome|M4|
|Recovery quality|Password reset completion|>80%|Reset-request -> password-updated funnel|M4|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session architecture|Stateless JWT access + Redis-backed hashed refresh tokens|Server sessions; third-party IdP|TDD mandates stateless JWT, Redis refresh storage, and rejects Auth0/Firebase; PRD requires persistent sessions and programmatic refresh.|
|Delivery sequencing|Foundations -> auth core -> user/admin SRF -> rollout|Feature-by-feature vertical slices; frontend-first sequencing|Risk inventory emphasizes CMP, migration safety, and token SCR; these are blocked unless schemas, stores, and SCR primitives ship first.|
|Token signing|RS256 with 2048-bit RSA keys|HS256 shared-secret JWT|NFR-SEC-002 explicitly requires RS256 with 2048-bit RSA keys.|
|Compliance treatment|Build consent and audit logging into M1/M3, not post-GA|Post-launch hardening sprint|PRD legal/CMP requirements and R-PRD-003 make audit completeness launch-critical.|
|Admin capabilities|Internal-only audit query + account lock SRF|No admin surface in v1.0; full RBAC console|Jordan persona/JTBD requires visibility and lock actions, but scope excludes RBAC, so minimal internal-only tooling best fits the constraints.|
|Rollout strategy|Three-phase feature-flagged rollout with rollback|Big-bang launch|Migration plan already specifies alpha, 10% beta, GA, and concrete rollback triggers/steps.|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|4 weeks|Week 1|Week 4|Schemas frozen; cryptographic primitives ready; consent/audit/reset stores in place|
|M2|4 weeks|Week 5|Week 8|Login/refresh/logout APIs live in staging; auth middleware and RVC active|
|M3|4 weeks|Week 9|Week 12|Register/login/profile/reset/logout journeys complete; admin audit/lock SRF available internally|
|M4|4 weeks|Week 13|Week 16|Observability active; alpha/beta/GA rollout executed; rollback readiness validated|

**Total estimated duration:** 16 weeks
