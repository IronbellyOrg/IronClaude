---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
base_variant: "none"
variant_scores: "none"
convergence_score: 0.94
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers the User Authentication Service as a technically phased program: foundation contracts first, then core auth logic, then user journeys, then hardening/compliance, then controlled rollout. The plan keeps the TDD as the primary engineering source, pulls PRD-driven value and compliance requirements forward where the TDD is incomplete, and resolves cross-document conflicts before they can create downstream rework.

The roadmap preserves all extracted work items and adds missing implementation artifacts required by the TDD and PRD: audit-log storage/query surfaces, logout, password-reset UX, consent capture, observability wiring, and staged rollout controls. Architecturally, the critical design guardrails are stateless JWT access tokens, Redis-backed hashed refresh tokens, PostgreSQL-backed user and audit records, TLS 1.3 transport, and compliance-grade auditability.

**Business Impact:** Unblocks Q2/Q3 personalization, supports Q3 SOC2 readiness, reduces support burden via self-service password reset, and establishes a reusable identity layer for future authenticated features.

**Complexity:** HIGH (0.72) — security-critical auth domain, multi-store persistence, cross-component orchestration, frontend integration, phased rollout, and compliance constraints increase coordination and verification cost.

**Critical path:** security/data contracts → crypto and persistence baseline → `AuthService`/`TokenManager` orchestration → public auth APIs → frontend flows and reset journey → observability/compliance controls → staged rollout and rollback readiness.

**Key architectural decisions:**

- Use stateless JWT access tokens plus hashed Redis refresh tokens rather than server-side sessions to satisfy scaling and silent-refresh requirements.
- Resolve the audit-retention conflict in favor of the PRD legal requirement: 12-month retention for auth audit events.
- Fill PRD/TDD gaps explicitly with roadmap deliverables for logout, admin auth-event visibility, account lock/unlock management, consent capture, and password-reset UX.

**Open risks requiring resolution before M1:**

- Audit-log retention conflict (`CONFLICT-1`) must be resolved before schema and storage policies are frozen.
- `UserProfile.roles` bound (`OQ-002`) must be recorded even if enforcement is deferred, to avoid contract ambiguity in tokens and profile responses.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation & Contracts|Foundation|P0|2 weeks|PostgreSQL, Redis, SEC-POLICY-001, COMPLIANCE-001|17|High|
|M2|Core Logic & Auth APIs|Core Logic|P0|2 weeks|M1, Node.js 20, bcryptjs, jsonwebtoken|16|High|
|M3|User Journeys & Frontend Integration|Integration|P0|2 weeks|M2, SendGrid, frontend routing framework|15|Medium-High|
|M4|Hardening, Compliance & Admin Operations|Hardening|P0|2 weeks|M1, M2, M3, staging env, Grafana/APM|26|High|
|M5|Production Readiness & Rollout|Production Readiness|P0|2 weeks|M4, feature flags, on-call staffing, rollout approvals|10|High|

## Dependency Graph

`PostgreSQL 15+` + `Redis 7+` + `SEC-POLICY-001` + `COMPLIANCE-001` → M1
M1 → M2
M2 + `frontend routing framework` + `SendGrid` → M3
M1 + M2 + M3 + `Grafana/APM` → M4
M4 + `AUTH_NEW_LOGIN` + `AUTH_TOKEN_REFRESH` + on-call readiness → M5
Cross-cutting: `Node.js 20` → M2/M3/M4/M5; `AUTH-PRD-001` → M1/M3/M4; `INFRA-DB-001` → M1/M5

## M1: Foundation & Contracts

**M1: Foundation & Contracts** | Weeks 1-2 (2026-03-31 to 2026-04-14) | exit criteria: security/storage contracts frozen; schema and crypto baselines implemented; compliance conflicts resolved and reflected in persistence policy

**Objective:** Establish the data, crypto, controller, and compliance contracts that every later flow depends on. | **Duration:** Weeks 1-2 (2026-03-31 to 2026-04-14) | **Entry:** AUTH-PRD-001 approved for design input; PostgreSQL 15+, Redis 7+, SEC-POLICY-001, COMPLIANCE-001 available | **Exit:** DM-001..DM-004, COMP-007..COMP-013, and NFR-SEC/NFR-COMP baseline controls implemented; audit retention fixed at 12 months; TLS/log-redaction policy codified

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile schema contract|Define and persist the canonical user profile model in PostgreSQL with normalization and timestamps.|PostgreSQL/UserRepo|PostgreSQL 15+|id:uuidv4-pk-notnull; email:unique-idx-lowercase-notnull; displayName:string-2..100-notnull; createdAt:iso8601-default-now; updatedAt:iso8601-auto-update; lastLoginAt:iso8601-nullable; roles:string[]-default["user"]-no-rbac-enforcement; relations:auditLogs1:N,refreshTokens1:N; retention:indefinite|M|P0|
|2|DM-002|AuthToken contract|Define the token-pair response contract used by login and refresh flows.|TokenManager/JwtService|DM-001|accessToken:jwt-rs256-userId+roles-15m-notnull; refreshToken:opaque-unique-hashed-redis-7d-notnull; expiresIn:number=900; tokenType:"Bearer"; relation:userId-ref-DM-001.id|S|P0|
|3|DM-003|AuthAuditLog schema|Create a compliance-grade audit event model for login, registration, refresh, reset, logout, and admin actions.|PostgreSQL/AuditLogRepo|PostgreSQL 15+, CONFLICT-1|fields:id:uuid-pk; userId:uuid-nullable-idx; eventType:string-idx; timestamp:iso8601-idx; ip:string; outcome:string; actorType:string; metadata:jsonb-minimized; retention:12-months-per-CONFLICT-1|M|P0|
|4|DM-004|PasswordResetToken schema|Create a single-use reset token model with expiry and consumption tracking.|PostgreSQL/ResetTokenStore|PostgreSQL 15+|fields:id:uuid-pk; userId:uuid-fk; tokenHash:string-notnull; expiresAt:iso8601-notnull; usedAt:iso8601-nullable; createdAt:iso8601-default-now; ttl:1-hour; singleUse:true|M|P0|
|5|NFR-SEC-001|bcrypt cost baseline|Set password hashing policy to bcrypt cost factor 12 and lock it with testable configuration.|PasswordHasher|SEC-POLICY-001|algorithm:bcrypt; costFactor:12; unit-assertion:required; plaintext-storage:false; hash-time-target:<500ms|S|P0|
|6|NFR-SEC-002|RS256 key baseline|Set JWT signing policy to RS256 with 2048-bit RSA keys and validation hooks.|JwtService|SEC-POLICY-001|alg:RS256; rsaKeySize:2048-bit; signingKeys:configured; verification:enabled; config-validation-test:required; rotation:quarterly|M|P0|
|7|NFR-SEC-003|Transport and log redaction baseline|Enforce TLS 1.3 and remove passwords/tokens from logs at the contract layer.|AuthHttpController/Logging|SEC-POLICY-001|tls:1.3-required-all-endpoints; sensitiveFields:password,accessToken,refreshToken,resetToken-excluded; controller-policy:applied; logging-schema:redacted|M|P0|
|8|NFR-COMP-001|Registration consent capture|Record GDPR consent with timestamp during registration without expanding PII scope.|ConsentRecorder/AuditLogRepo|DM-003, COMPLIANCE-001|consent:required-at-registration; timestamp:recorded; evidence:stored-as-audit-event-or-consent-record; pii-minimization:preserved|M|P0|
|9|NFR-COMP-002|SOC2 audit retention policy|Implement audit logging contract with 12-month retention and mandatory event fields.|AuditLogRepo|DM-003, CONFLICT-1|events:all-auth-events; fields:userId,timestamp,ip,outcome; retention:12-months; queryability:date-range+user; SOC2-alignment:documented|M|P0|
|10|NFR-COMP-003|Data minimization policy|Constrain persisted account data to the approved minimal set and keep passwords one-way hashed.|UserRepo/PasswordHasher|DM-001, NFR-SEC-001|collectedFields:email,hashedPassword,displayName; rawPassword:persisted-never; extraPII:none-required; NIST-SP-800-63B-aligned|S|P0|
|11|COMP-007|JwtService and PasswordHasher primitives|Implement the crypto primitives used by all auth flows.|JwtService/PasswordHasher|NFR-SEC-001, NFR-SEC-002|JwtService:sign,verify-RS256-2048bit-clockSkew5s; PasswordHasher:bcrypt-cost12-hash,verify; abstraction:future-migration-ready|M|P0|
|12|COMP-008|UserRepo persistence adapter|Implement the repository boundary for `UserProfile` reads/writes and uniqueness checks.|UserRepo|DM-001|methods:createUser,getByEmail,getById,updateLastLogin; constraints:email-unique-normalized; store:PostgreSQL15+|M|P0|
|13|COMP-009|AuditLogRepo persistence adapter|Implement the repository boundary for audit writes and admin queries.|AuditLogRepo|DM-003|methods:appendEvent,listEventsByUser,listEventsByDateRange; store:PostgreSQL15+; retention:12-months|M|P0|
|14|COMP-010|ResetTokenStore|Implement storage and consumption semantics for reset tokens.|ResetTokenStore|DM-004|methods:createToken,getValidToken,consumeToken,revokeUserTokens; ttl:1-hour; singleUse:enforced; store:PostgreSQL|M|P0|
|15|COMP-011|Auth HTTP controller shell|Create the versioned `/v1/auth/*` controller shell and standard error envelope contract.|AuthHttpController|DM-001, DM-002|prefix:/v1/auth/*; errorEnvelope:error.code,message,status; versioning:url-prefix; breakingChanges:new-major|M|P0|
|16|COMP-012|Bearer auth middleware|Create middleware for Bearer extraction, JWT validation, and protected-route context injection.|AuthMiddleware|COMP-007, DM-001|input:Authorization-Bearer; verify:JwtService.verify; skewTolerance:5s; output:userId,roles,authContext; invalidOrExpired:401|M|P0|
|17|COMP-013|Consent recorder component|Implement the component that records consent evidence during registration and links it to the user/audit trail.|ConsentRecorder|NFR-COMP-001, DM-003, DM-001|inputs:userId,consentTimestamp,ip; writes:consent-event; linkage:DM-001.id; pii-minimized:true|S|P1|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`UserRepo` ↔ PostgreSQL users table|Repository|DM-001 persisted with unique email + timestamp defaults|M1|`AuthService`, admin surfaces, `/auth/me`|
|`AuditLogRepo` ↔ PostgreSQL audit table|Repository|12-month retention, user/date-range indexes, redacted metadata|M1|observability, admin event query APIs, compliance review|
|`ResetTokenStore` ↔ PostgreSQL reset table|Repository|single-use token hash + expiry + consumption tracking|M1|password reset request/confirm flow|
|`AuthMiddleware` ↔ `JwtService`|Middleware chain|Bearer parsing + RS256 verification + auth context injection|M1|protected APIs, admin APIs, profile flow|
|`ConsentRecorder` ↔ `AuditLogRepo`|Callback/event write|consent timestamp recorded during registration|M1|GDPR evidence, compliance checks|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Audit retention frozen incorrectly before schema creation|High|Medium|High|Resolve `CONFLICT-1` in M1 and apply 12-month retention consistently in DM-003, repo policies, and success criteria.|architect|
|2|Weak crypto defaults leak into later milestones|High|Low|Critical|Lock bcrypt cost 12 and RS256/2048-bit requirements in COMP-007 and validation tests before API work starts.|security|
|3|Over-collection of user data violates GDPR/NIST constraints|High|Medium|High|Limit persisted user fields to email, hashed password, displayName; route consent evidence to audit records instead of profile expansion.|architect|
|4|Brute-force behavior is underspecified at the contract layer|Medium|Medium|High|Resolve `OQ-PRD-3` in M1 and encode 5 failures/15 minutes into controller/service contracts.|backend|

### Milestone Dependencies — M1

- PostgreSQL 15+ provisioned with migration capability.
- Redis 7+ reachable for later token lifecycle work, even though M1 only defines the contract.
- `SEC-POLICY-001` available for cryptographic and transport defaults.
- `COMPLIANCE-001` and PRD legal/compliance requirements available for retention and consent policy.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `AuthService` support API key authentication for service-to-service calls? (Source: TDD §22; status: closed; resolution: deferred to v1.1 because PRD scope locks v1.0 to email/password only.)|No v1.0 API-key path is planned; M2/M3 implement token-based user auth only.|test-lead|2026-04-15|
|2|OQ-002|Maximum allowed `UserProfile` roles array length? (Source: TDD §22; status: closed; resolution: no v1.0 service-level cap; `roles:string[]` remains contract-only until RBAC design review.)|Keeps DM-001 stable without inventing RBAC enforcement in v1.0.|auth-team|2026-04-01|
|3|CONFLICT-1|Audit log retention — PRD mandates 12 months for SOC2 (`NFR-COMP-002`) but TDD §7.2 specifies 90 days. (Source: extraction + TDD §7.2 + PRD Legal & Compliance; status: closed; chosen: 12 months; precedence: PRD legal/compliance requirement overrides TDD default.)|DM-003, COMP-009, admin log APIs, ops storage sizing, and success criteria all use 12-month retention.|architect|2026-03-31|
|4|OQ-PRD-3|Account lockout policy (N consecutive failures)? TDD states 5/15min; PRD still open — reconcile. (Source: extraction; status: closed; chosen: 5 failed attempts within 15 minutes because TDD FR-AUTH-001 and R-002 provide the only numeric contract.)|M2 login logic, API-001 responses, and TEST-009 all implement 5/15min.|security|2026-03-31|

## M2: Core Logic & Auth APIs

**M2: Core Logic & Auth APIs** | Weeks 3-4 (2026-04-15 to 2026-04-28) | exit criteria: login, registration, refresh, and profile retrieval operate against real stores with stable `/v1/auth/*` contracts and core tests passing

**Objective:** Implement the backend auth orchestration and public API surfaces on top of the foundation contracts. | **Duration:** Weeks 3-4 (2026-04-15 to 2026-04-28) | **Entry:** M1 complete; Node.js 20 LTS runtime available; bcryptjs and jsonwebtoken dependencies approved | **Exit:** FR-AUTH-001..004, API-001..004, COMP-020..022, and TEST-001..005 pass against real PostgreSQL/Redis where applicable

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-001|Login flow|Implement email/password authentication with uniform failure handling and lockout support.|AuthService|COMP-021, COMP-007, COMP-008|200-on-valid-credentials-with-DM-002; 401-on-invalid-password; 401-on-unknown-email-no-enumeration; 423-on-locked-account-after-5-failures/15min|L|P0|
|2|FR-AUTH-002|Registration flow|Implement validated registration with unique email enforcement and profile creation.|AuthService|COMP-021, COMP-008, COMP-013, COMP-020|201-on-valid-registration-with-DM-001; 409-on-duplicate-email; 400-on-password<8-or-missing-uppercase-or-missing-number; bcrypt-cost12-stored|L|P0|
|3|FR-AUTH-003|Token issuance and refresh|Implement access/refresh issuance and silent refresh semantics with old-token revocation.|TokenManager|COMP-022, COMP-007, Redis 7+|login-returns-access15m+refresh7d; POST-/auth/refresh-valid→new-DM-002; expired-refresh→401; revoked-refresh→401|L|P0|
|4|FR-AUTH-004|Authenticated profile retrieval|Implement current-user retrieval from validated access token context.|AuthService/AuthMiddleware|COMP-021, COMP-012, DM-001|GET-/auth/me-valid-token→DM-001; expired-or-invalid-token→401; response-includes-id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|M|P0|
|5|API-001|POST `/auth/login`|Expose the login endpoint with lockout and rate-limit aware behavior.|AuthHttpController|FR-AUTH-001|method:POST; path:/v1/auth/login; auth:no; rateLimit:10/min/IP; request:email,password; response200:DM-002; errors:401,423,429|M|P0|
|6|API-002|POST `/auth/register`|Expose the registration endpoint with profile response semantics.|AuthHttpController|FR-AUTH-002|method:POST; path:/v1/auth/register; auth:no; rateLimit:5/min/IP; request:email,password,displayName; response201:DM-001; errors:400,409|M|P0|
|7|API-003|GET `/auth/me`|Expose the authenticated profile endpoint.|AuthHttpController/AuthMiddleware|FR-AUTH-004|method:GET; path:/v1/auth/me; auth:Bearer-required; rateLimit:60/min/user; request:Authorization-Bearer<accessToken>; response200:DM-001; errors:401|M|P0|
|8|API-004|POST `/auth/refresh`|Expose the refresh endpoint that rotates refresh tokens.|AuthHttpController/TokenManager|FR-AUTH-003|method:POST; path:/v1/auth/refresh; auth:no-body-token; rateLimit:30/min/user; request:refreshToken; response200:DM-002; errors:401|M|P0|
|9|COMP-021|AuthService orchestrator|Implement the backend façade for auth flows and persistence/crypto delegation.|AuthService|COMP-007, COMP-008, COMP-010|methods:login,register,getProfile,resetRequest,resetConfirm; delegates:PasswordHasher,TokenManager,UserRepo; location:src/auth/auth-service|L|P0|
|10|COMP-022|TokenManager lifecycle service|Implement issue/refresh/revoke lifecycle management with Redis-backed refresh tokens.|TokenManager|COMP-007, Redis 7+|methods:issueTokens,refresh,revoke; access:JWT-via-JwtService; refresh:hashed-in-Redis-7d; oldRefresh:revoked-on-rotate|L|P0|
|11|COMP-020|Registration consent wiring|Wire consent recording into the registration path so legal evidence is created with the account.|AuthService/ConsentRecorder|FR-AUTH-002, NFR-COMP-001|registration-calls-consent-recorder; consentTimestamp-captured; user-linkage-preserved; failure-handling-auditable|S|P1|
|12|TEST-001|Unit login success test|Verify successful login issues token pairs through the correct collaborators.|Jest/AuthService|FR-AUTH-001|component:AuthService; input:valid-email-password; expects:PasswordHasher.verify-called; expects:TokenManager.issueTokens-called; result:DM-002|S|P0|
|13|TEST-002|Unit login failure test|Verify invalid credentials return 401 and do not issue tokens.|Jest/AuthService|FR-AUTH-001|component:AuthService; input:invalid-password; PasswordHasher.verify:false; result:401; token-issuance:none|S|P0|
|14|TEST-003|Unit refresh success test|Verify refresh rotates tokens and revokes the old refresh token.|Jest/TokenManager|FR-AUTH-003|component:TokenManager; input:valid-refreshToken; old-refresh:revoked; new-pair:issued-via-JwtService|S|P0|
|15|TEST-004|Integration registration persistence test|Verify registration persists `UserProfile` and password hash in PostgreSQL.|Supertest/testcontainers|FR-AUTH-002|scope:AuthService+PostgreSQL; validates:PasswordHasher.hash; validates:DB-insert; result:DM-001-persisted|M|P0|
|16|TEST-005|Integration expired refresh rejection test|Verify Redis TTL expiry blocks refresh reuse.|Supertest/testcontainers|FR-AUTH-003|scope:TokenManager+Redis; expired-refreshToken→401; ttl-expiry-observed; revoked-state-honored|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthService` → `PasswordHasher.verify/hash`|Service delegation|login/register paths call bcrypt abstraction instead of raw library usage|M2|API-001, API-002, reset-confirm|
|`AuthService` → `TokenManager.issueTokens/refresh`|Service delegation|login and refresh issue `AuthToken` pairs with rotation|M2|API-001, API-004, frontend silent refresh|
|`AuthMiddleware` → request context|Middleware chain|JWT verification injects `userId` and `roles` for `/auth/me`|M2|API-003, later admin endpoints|
|`ConsentRecorder` → registration flow|Callback/event|registration writes consent evidence after successful user creation|M2|compliance audit, legal review|
|Redis refresh-token store|Cache/store|hashed refresh tokens persisted with 7-day TTL and revoke-on-rotate semantics|M2|API-004, logout, password reset invalidation|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Credential failures leak user enumeration signals|High|Medium|High|Keep unknown-email and wrong-password responses identical and verify error-envelope consistency in API tests.|backend|
|2|Refresh rotation is implemented without revoking old tokens|High|Medium|High|Make revoke-on-rotate part of FR-AUTH-003, API-004, and TEST-003/005 acceptance criteria.|security|
|3|Consent evidence is omitted from successful registrations|Medium|Medium|High|Wire COMP-013 and COMP-020 directly into the registration transaction boundary and audit on failure paths.|compliance|
|4|Core APIs drift from versioned contract|Medium|Low|High|Enforce `/v1/auth/*` prefix and schema/error-envelope checks in controller tests before frontend integration starts.|architect|

### Milestone Dependencies — M2

- M1 schema, middleware, and crypto contracts complete.
- Redis 7+ available for refresh-token storage and revocation.
- Node.js 20 LTS runtime and core crypto libraries (`bcryptjs`, `jsonwebtoken`) available.
- Testcontainers or equivalent ephemeral PostgreSQL/Redis infrastructure available for integration tests.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|JTBD-gap-1|PRD JTBD #4 (Sam the API consumer programmatic auth) has no explicit FR — refresh is covered (FR-AUTH-003) but no dedicated API-key/service-account path. (Source: extraction; status: closed; resolution: v1.0 programmatic auth is satisfied by API login + refresh contracts, while API-key/service-account auth remains deferred by OQ-001.)|Avoids unauthorized scope expansion while still delivering stable programmatic refresh behavior for user-scoped integrations.|architect|2026-04-15|
|2|OQ-PRD-2|Maximum refresh tokens allowed per user across devices? (Source: PRD Open Questions; status: closed; chosen: cap active refresh tokens at 5 per user, evict oldest on sixth issuance to preserve multi-device use without unbounded token growth.)|TokenManager and logout/reset invalidation logic use a bounded per-user refresh-token set.|product-manager|2026-04-15|

## M3: User Journeys & Frontend Integration

**M3: User Journeys & Frontend Integration** | Weeks 5-6 (2026-04-29 to 2026-05-12) | exit criteria: end-user registration, login, profile, password-reset, and logout journeys work through the frontend with stable redirects and silent-refresh behavior

**Objective:** Deliver the user-facing journeys on top of the stable backend contracts and close PRD capability gaps for logout and password-reset UX. | **Duration:** Weeks 5-6 (2026-04-29 to 2026-05-12) | **Entry:** M2 APIs stable in staging; SendGrid and frontend routing framework available | **Exit:** FR-AUTH-005, API-005..007, COMP-001..004, COMP-014..017, and TEST-006..008 pass in staging; password reset emails delivered within 60 seconds; logout ends session immediately

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-005|Password reset flow|Implement request/confirm reset flow with token issuance, expiry, single use, and session invalidation.|AuthService/ResetTokenStore|COMP-021, COMP-010, COMP-022|POST-/auth/reset-request-sends-reset-token; POST-/auth/reset-confirm-valid-token-updates-password-hash; reset-token-expires-1h; used-token-cannot-reuse; new-password-invalidates-all-sessions|L|P0|
|2|API-005|POST `/auth/reset-request`|Expose the password reset request endpoint with no-enumeration behavior.|AuthHttpController|FR-AUTH-005|method:POST; path:/v1/auth/reset-request; auth:no; rateLimit:5/min/IP; request:email; response:generic-confirmation-regardless-of-registration; errors:standard-error-envelope|M|P0|
|3|API-006|POST `/auth/reset-confirm`|Expose the password reset confirm endpoint with password policy enforcement.|AuthHttpController|FR-AUTH-005|method:POST; path:/v1/auth/reset-confirm; auth:no; rateLimit:10/min/IP; request:token,newPassword; errors:400-invalid-or-expired-token,400-weak-password; sessions:invalidated-on-success|M|P0|
|4|API-007|POST `/auth/logout`|Add the missing logout endpoint required by the PRD user story and scope definition.|AuthHttpController/TokenManager|COMP-022, OQ-GAP-001|method:POST; path:/v1/auth/logout; auth:Bearer-or-refresh-context; request:current-refreshToken-or-session-context; response:204-or-200; effect:session-ends-immediately-and-refresh-token-revoked|M|P0|
|5|COMP-001|LoginPage|Implement the `/login` route and login form with generic failure handling and optional redirect support.|Frontend/LoginPage|API-001|route:/login; authRequired:false; props:onSuccess:()=>void,redirectUrl?:string; fields:email,password; calls:POST-/auth/login; storesTokens:via-AuthProvider; captcha-after-3-failed-attempts|M|P0|
|6|COMP-002|RegisterPage|Implement the `/register` route and registration form with inline validation and terms linkage.|Frontend/RegisterPage|API-002, NFR-COMP-001|route:/register; authRequired:false; props:onSuccess:()=>void,termsUrl:string; fields:email,password,displayName,consent; validation:password-strength-client-side; calls:POST-/auth/register|M|P0|
|7|COMP-003|ProfilePage|Implement the protected `/profile` route that renders current account details.|Frontend/ProfilePage|API-003, COMP-017|route:/profile; authRequired:true; props:none; data:id,email,displayName,createdAt,lastLoginAt,roles; calls:GET-/auth/me|M|P0|
|8|COMP-004|AuthProvider|Implement the React auth context wrapper, token storage strategy, 401 interception, and silent refresh behavior.|Frontend/AuthProvider|API-001, API-003, API-004|props:children:ReactNode; accessToken:in-memory; refreshToken:HttpOnly-cookie; intercept401:true; silentRefresh:via-TokenManager/API-004; redirects:unauthenticated-users-to-LoginPage|L|P0|
|9|COMP-014|ForgotPasswordPage|Implement the reset-request UI and generic confirmation message flow.|Frontend/ForgotPasswordPage|API-005|route:/forgot-password; authRequired:false; props:onSubmitted?:()=>void; field:email; calls:POST-/auth/reset-request; confirmation:no-enumeration|M|P1|
|10|COMP-015|ResetPasswordPage|Implement the reset-confirm UI for token + new password submission.|Frontend/ResetPasswordPage|API-006|route:/reset-password; authRequired:false; props:token:string; fields:newPassword,confirmPassword; calls:POST-/auth/reset-confirm; handles:expired-link-and-weak-password-errors|M|P1|
|11|COMP-016|LogoutControl|Implement the logout action in the authenticated UI and clear local auth state.|Frontend/LogoutControl|API-007, COMP-004|trigger:button-or-menu-action; calls:POST-/auth/logout; clears:in-memory-accessToken; redirects:landing-or-login; shared-device-session-end-immediate|S|P1|
|12|COMP-017|Protected/Public route wrappers|Implement the route wrappers shown in the component hierarchy so guarded navigation is explicit.|Frontend/RouteGuards|COMP-004|components:PublicRoutes,ProtectedRoutes; consumes:AuthProvider-context; redirects:protected→/login-if-unauthenticated; preserves:redirectUrl|M|P1|
|13|TEST-006|E2E registration and login journey|Verify end-to-end registration, login, and profile access through the frontend stack.|Playwright|COMP-001, COMP-002, COMP-003, COMP-004|flow:RegisterPage→LoginPage→ProfilePage; tool:Playwright; validates:FR-AUTH-001+FR-AUTH-002; tokens:stored-and-used-correctly|M|P0|
|14|TEST-007|E2E password reset journey|Verify self-service password reset from request to relogin.|Playwright|COMP-014, COMP-015, API-005, API-006|flow:ForgotPasswordPage→email-link→ResetPasswordPage→LoginPage; reset-email-delivered≤60s; old-sessions-invalidated; relogin-with-new-password-succeeds|M|P0|
|15|TEST-008|E2E logout journey|Verify logout immediately ends the current session and redirects correctly.|Playwright|API-007, COMP-016|flow:authenticated-user→logout→redirect; current-session-invalid; protected-route-access-redirects-to-login|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`LoginPage` → `AuthProvider`|Component/context|successful login stores access token in memory and refresh token via cookie-backed flow|M3|protected navigation, silent refresh|
|`RegisterPage` → consent + register API|Form/API binding|inline validation + consent capture + POST `/auth/register`|M3|new user onboarding, funnel analytics|
|`AuthProvider` → API-004|Interceptor/refresh loop|401 interception triggers silent refresh before redirecting to login|M3|`ProfilePage`, future protected routes|
|`ForgotPasswordPage`/`ResetPasswordPage` → SendGrid-backed reset flow|Page/API/email binding|generic reset request, email link handoff, token confirmation|M3|self-service recovery journey|
|`LogoutControl` → API-007|Action binding|logout revokes refresh context and clears local auth state|M3|shared-device safety, session end|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Registration UX diverges from product expectations and hurts conversion|High|Medium|High|Keep forms minimal, inline-validate only necessary fields, and track funnel metrics from landing to success.|frontend|
|2|Password reset emails fail or arrive too slowly|Medium|Low|Medium|Use asynchronous email dispatch with delivery monitoring, generic confirmation UX, and alerting on send failures.|backend|
|3|Access token storage is implemented insecurely in the browser|High|Medium|High|Keep access token in memory only and store refresh token in HttpOnly cookies as specified in R-001 mitigation.|security|
|4|Logout or reset flows leave refresh tokens valid|High|Medium|High|Revoke refresh-token sets on logout and password reset, and verify with E2E coverage.|backend|

### Milestone Dependencies — M3

- Stable staging deployment of M2 APIs.
- SendGrid or equivalent email delivery dependency available.
- Frontend routing framework available for `/login`, `/register`, `/profile`, `/forgot-password`, `/reset-password`.
- Browser storage and cookie policy reviewed for HttpOnly refresh-token handling.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-1|Should password reset emails be sent synchronously or asynchronously? (Source: PRD Open Questions; status: closed; chosen: asynchronous dispatch with immediate generic UI confirmation and delivery monitoring.)|Allows API-005 to stay fast and non-enumerating while supporting the PRD delivery target of reset email within 60 seconds.|engineering|2026-04-29|
|2|OQ-PRD-4|Should we support "remember me" to extend session duration? (Source: PRD Open Questions; status: closed; resolution: deferred to v1.1 because TDD/PRD already define 15-minute access and 7-day refresh windows for v1.0.)|Keeps token policy stable and avoids introducing alternate session semantics in M3.|product-manager|2026-04-29|
|3|CONFLICT-2|Registration success behavior conflicts: PRD user story says successful registration logs the user in immediately, while TDD/API-002 and extraction require `201 UserProfile` without token issuance. (Source: PRD Implementation Plan + TDD §8.2; status: closed; chosen: TDD endpoint contract prevails for v1.0; RegisterPage redirects to LoginPage after success.)|Preserves API stability and avoids expanding API-002 beyond the current contract; conversion impact is tracked in M4 metrics and may drive a v1.1 change.|architect|2026-04-29|
|4|OQ-GAP-001|PRD in-scope scope/story includes logout but the TDD omits a dedicated endpoint. (Source: PRD Scope Definition + User Stories; status: closed; resolution: add API-007 and COMP-016 as gap-fill deliverables; TDD should be updated.)|Closes a user-story completeness gap and gives M3 a complete authenticated session lifecycle.|architect|2026-04-29|

## M4: Hardening, Compliance & Admin Operations

**M4: Hardening, Compliance & Admin Operations** | Weeks 7-8 (2026-05-13 to 2026-05-26) | exit criteria: performance, reliability, observability, auditability, and admin operational controls validated in staging with measurable gates

**Objective:** Add the operational, compliance, and admin control surfaces required for secure production use and SOC2 readiness. | **Duration:** Weeks 7-8 (2026-05-13 to 2026-05-26) | **Entry:** M1-M3 complete in staging; Grafana/APM and load-test tooling available | **Exit:** NFR-PERF-001/002, NFR-REL-001, OPS-001..005, OPS-007..010, OBS-001..006, API-008..011, COMP-018..019, and TEST-009..010 pass review; Jordan admin use cases have backend support

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-PERF-001|Auth endpoint latency budget|Validate and tune all auth endpoints to meet the p95 latency budget.|AuthService/APM|M2, OBS-002, OBS-005|all-auth-endpoints-p95<200ms; measurement:APM-tracing-on-AuthService-methods; regression-budget:tracked|M|P0|
|2|NFR-PERF-002|Concurrent login capacity|Validate 500 concurrent login requests with load testing and scaling guidance.|AuthService/k6|NFR-PERF-001, OPS-005, OPS-010|500-concurrent-login-requests-supported; tool:k6; p95<200ms-under-load; bottlenecks-documented|M|P0|
|3|NFR-REL-001|Availability and health checks|Implement health monitoring and release gating for 99.9% availability targets.|HealthCheck/Monitoring|API-011, OPS-008|availability:99.9%-30-day-windows; monitor:health-check-endpoint; release-gate:configured|M|P0|
|4|OPS-001|Runbook: `AuthService` down|Publish and validate the primary service outage runbook.|Runbook/OnCall|OBS-006|scenario:AuthService-down; symptoms:5xx-on-/auth/*+LoginPage/RegisterPage-errors; diagnosis:pod-health,PostgreSQL,init-logs; resolution:restart-pods+failover-Postgres-to-read-replica+reject-refresh-if-Redis-down; escalation:auth-team→platform-team-after-15min|S|P1|
|5|OPS-002|Runbook: token refresh failures|Publish and validate the refresh-failure runbook.|Runbook/OnCall|OBS-003, OBS-006|scenario:token-refresh-failures; symptoms:unexpected-logouts,AuthProvider-loop,auth_token_refresh_total-error-spike; diagnosis:Redis,JwtService-keys,AUTH_TOKEN_REFRESH; resolution:scale-Redis+remount-secrets+enable-flag-if-off; escalation:auth-team→platform-team-if-Redis-cluster-issue|S|P1|
|6|OPS-003|On-call readiness|Define post-GA response expectations, escalation chain, and tooling.|OnCallProgram|OPS-001, OPS-002|P1-ack≤15min; coverage:24/7-first-2-weeks-post-GA; tooling:K8s,Grafana,RedisCLI,PostgreSQL-admin; path:auth-team→test-lead→eng-manager→platform-team|S|P1|
|7|OPS-004|Observability implementation baseline|Implement the extracted observability contract for logs, metrics, tracing, and alerts.|Observability/AuthService|OBS-001..006|logs:login-success/failure,registration,refresh,password-reset-excluding-passwords/tokens; metrics:auth_login_total,auth_login_duration_seconds,auth_token_refresh_total,auth_registration_total; tracing:AuthService→PasswordHasher→TokenManager→JwtService; alerts:login-failure-rate>20%/5m,p95>500ms,Redis-connection-failures|M|P0|
|8|OPS-005|Capacity planning baseline|Implement the extracted capacity plan for service, PostgreSQL, and Redis.|Kubernetes/PostgreSQL/Redis|NFR-PERF-002|AuthService:3-replicas-baseline-HPA10-at-CPU>70%; PostgreSQL:100-pool-raise200-if-wait>50ms; Redis:1GB-baseline-scale2GB-at->70%-utilization|M|P1|
|9|OPS-007|AuthService pod scaling runbook|Codify pod scaling actions and thresholds for expected concurrency.|Kubernetes/HPA|OPS-005|current:3-replicas; expected:500-concurrent-users; HPA:max10-pods-on-CPU>70%; operator-actions:documented|S|P1|
|10|OPS-008|Alerting and dashboards|Implement alert thresholds and Grafana dashboards for degraded auth behavior.|Grafana/Alertmanager|OBS-006|alerts:login-failure-rate>20%/5m,p95>500ms,Redis-connection-failures; dashboards:login/refresh/registration-counters+duration-histograms|M|P0|
|11|OPS-009|PostgreSQL scaling runbook|Codify database pool scaling targets and operator actions.|PostgreSQL|OPS-005|currentPool:100; expectedQueries:50-avg-concurrent; scaleTo:200-if-wait>50ms; operator-actions:documented|S|P1|
|12|OPS-010|Redis scaling runbook|Codify Redis memory scaling thresholds and operator actions for refresh tokens.|Redis|OPS-005|currentMemory:1GB; expectedTokens:~100K/~50MB; scaleTo:2GB-at->70%-utilization; operator-actions:documented|S|P1|
|13|OBS-001|Structured auth logging implementation|Wire structured application logs into all auth service methods and controller outcomes.|Logging/AuthService|M2, NFR-SEC-003|events:login-success,login-failure,registration,refresh,password-reset,logout,admin-actions; fields:timestamp,userId?,ip,outcome,eventType; sensitiveFields:redacted|M|P0|
|14|OBS-002|Latency histogram instrumentation|Instrument login and endpoint latency histograms for p95 monitoring.|Metrics/AuthService|OBS-001|metric:auth_login_duration_seconds-histogram; coverage:all-auth-endpoints; labels:outcome,endpoint; export:Prometheus|S|P0|
|15|OBS-003|Token refresh counter instrumentation|Instrument token refresh success/failure counters.|Metrics/TokenManager|OBS-001|metric:auth_token_refresh_total-counter; labels:outcome; errors:counted; export:Prometheus|S|P0|
|16|OBS-004|Registration counter instrumentation|Instrument registration attempt/success/failure counters.|Metrics/AuthService|OBS-001|metric:auth_registration_total-counter; labels:outcome; export:Prometheus; funnel-input:available|S|P0|
|17|OBS-005|Distributed tracing implementation|Implement OpenTelemetry spans across the auth call graph.|Tracing/AuthService|M2|spanChain:AuthService→PasswordHasher→TokenManager→JwtService; contextPropagation:true; endpoint-coverage:login,register,me,refresh,reset|M|P0|
|18|OBS-006|Alert rule and dashboard configuration|Configure alert rules and dashboard panels that consume the auth telemetry.|Grafana/Alertmanager|OBS-002, OBS-003, OBS-004, OBS-005|rules:login-failure-rate,p95-latency,Redis-failures; dashboards:auth-counters,histograms,traces; owners:on-call-team|M|P0|
|19|API-008|GET `/admin/auth-events`|Add the missing admin query API for authentication event logs required by Jordan's PRD story.|AdminAuthApi|COMP-018, DM-003|method:GET; path:/v1/admin/auth-events; auth:admin; filters:userId,dateRange,eventType; response:queryable-auth-events-with-userId,timestamp,ip,outcome|M|P0|
|20|API-009|POST `/admin/users/{id}/lock`|Add the missing admin account lock API implied by the PRD incident-management story.|AdminAuthApi|COMP-019, DM-001|method:POST; path:/v1/admin/users/{id}/lock; auth:admin; effect:account-locked; audit:event-recorded|M|P1|
|21|API-010|POST `/admin/users/{id}/unlock`|Add the missing admin account unlock API for incident recovery.|AdminAuthApi|COMP-019, DM-001|method:POST; path:/v1/admin/users/{id}/unlock; auth:admin; effect:account-unlocked; audit:event-recorded|M|P1|
|22|API-011|GET `/health`|Expose a health endpoint used for availability monitoring and rollout gates.|MonitoringApi|NFR-REL-001|method:GET; path:/health; auth:no; checks:service,PostgreSQL,Redis,signing-keys; status:healthy-or-degraded|S|P1|
|23|COMP-018|Admin auth event query service|Implement the backend service that powers auth-event queries and filtering for admin tools.|AdminAuthEventService|COMP-009, API-008|methods:listEventsByUser,listEventsByDateRange,listEventsByType; source:DM-003; filters:user,dateRange,eventType,outcome|M|P0|
|24|COMP-019|Account lock manager|Implement the backend service that performs lock/unlock operations and writes audit records.|AccountLockManager|DM-001, DM-003, API-009, API-010|methods:lockUser,unlockUser,isLocked; effects:audit-event-written; login-enforcement:compatible-with-FR-AUTH-001|M|P1|
|25|TEST-009|Load test suite|Run and retain evidence for the 500-concurrent-user load target and latency budget.|k6/APM|NFR-PERF-001, NFR-PERF-002|tool:k6; scenario:500-concurrent-logins; evidence:p95<200ms; bottlenecks:documented|M|P0|
|26|TEST-010|Security and compliance verification suite|Run the dedicated security review and audit-log validation expected by the PRD risks and release criteria.|SecurityReview/QA|OBS-001, API-008..010|checks:bcrypt-cost-verified,JwtService-key-rotation-documented,log-redaction-verified,audit-fields-complete,admin-query-surface-functional|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthService` telemetry hooks|Instrumentation|logs, counters, histograms, and traces emitted on all auth paths|M4|Grafana, Alertmanager, on-call, release gates|
|`AdminAuthEventService` → `AuditLogRepo`|Service/repository|query filters wired to audit-log persistence indexes|M4|API-008, admin tooling, compliance review|
|`AccountLockManager` → login lockout checks|Service/policy|manual lock/unlock and automatic lockout share account-state semantics|M4|API-001, API-009, API-010|
|`/health` → release gate monitors|Endpoint/monitor|service + dependency status exposed for uptime and rollout criteria|M4|NFR-REL-001, M5 canary gating|
|Capacity runbooks → platform scaling actions|Runbook/ops wiring|pod, PostgreSQL, and Redis thresholds mapped to operator actions|M4|NFR-PERF-002, M5 rollout safety|
|Alert rules → on-call rotation|Monitoring chain|threshold breaches page the configured auth/platform escalation path|M4|OPS-003, MIG-002, MIG-003|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Compliance failure from incomplete audit logging|High|Medium|High|Implement OPS-007, API-008, and TEST-010 so event completeness is measurable and queryable.|compliance|
|2|Security flaws escape into rollout because observability is validation-only|High|Low|Critical|Create explicit OBS implementation tasks before validation tasks and require security review evidence for release.|security|
|3|Jordan admin persona remains unsupported despite audit logging being emitted|Medium|Medium|High|Add API-008..010 and backend admin services as gap fills; flag TDD update requirement in the open questions subsection.|architect|
|4|Availability target cannot be proven because no health endpoint or alerts exist|High|Medium|High|Add API-011 and OPS-008 before M5 canary starts, and use them for rollout gates.|devops|

### Milestone Dependencies — M4

- Staging environment with APM/Grafana/Alertmanager access.
- Load-testing toolchain (`k6`) and representative staging data.
- Admin authentication/authorization context available for `/v1/admin/*` APIs.
- Storage sizing visibility for PostgreSQL and Redis.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|JTBD-gap-2|Jordan the Admin persona ("view authentication event logs", "lock compromised accounts") has no FR in the TDD. (Source: extraction + PRD personas/user stories; status: closed; resolution: add API-008..010 and COMP-018..019 as gap-fill deliverables; TDD should be updated.)|Closes a major persona coverage gap before production readiness and gives operations a supported incident response path.|architect|2026-05-13|
|2|OQ-GOV-001|Deprecation policy for auth API versions is not explicitly defined in the TDD governance section. (Source: extraction API Governance note; status: closed; chosen: support one active major version plus 90-day deprecation notice for superseded auth majors.)|Prevents future versioning ambiguity for `/v1/auth/*` without blocking v1.0 launch.|architect|2026-05-13|

## M5: Production Readiness & Rollout

**M5: Production Readiness & Rollout** | Weeks 9-10 (2026-05-27 to 2026-06-09) | exit criteria: rollout phases complete, rollback tested, release criteria satisfied, and default schedule lands on or before the TDD committed end date

**Objective:** Execute the staged migration, validate release criteria under live traffic, and leave the service operationally supportable. | **Duration:** Weeks 9-10 (2026-05-27 to 2026-06-09) | **Entry:** M4 complete with alerts, health checks, admin ops, and hardening evidence in place | **Exit:** MIG-001..005, OPS-011, and TEST-011..013 complete; staged traffic ramp succeeds; 99.9% uptime preserved during GA window; go/no-go sign-off recorded by owners

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1 internal alpha|Deploy to staging/internal alpha behind `AUTH_NEW_LOGIN` and validate full auth scope manually.|Release/Rollout|M4, MIG-004|duration:1-week; environment:staging; audience:auth-team+QA; flag:AUTH_NEW_LOGIN; exit:all-FR-AUTH-001..005-pass-manual-tests-and-zero-P0/P1|M|P0|
|2|MIG-002|Phase 2 beta (10%)|Enable the new login flow for 10% of traffic and monitor live metrics.|Release/Rollout|MIG-001, OPS-008|duration:2-weeks; traffic:10%; monitors:latency,error-rates,Redis; exit:p95<200ms,error<0.1%,no-Redis-failures|M|P0|
|3|MIG-003|Phase 3 general availability|Promote to 100% traffic, enable refresh flow, and deprecate legacy endpoints.|Release/Rollout|MIG-002, MIG-005|duration:1-week; traffic:100%; AUTH_NEW_LOGIN:removed; AUTH_TOKEN_REFRESH:enabled; exit:99.9%-uptime-over-first-7-days|M|P0|
|4|MIG-004|Feature flag `AUTH_NEW_LOGIN`|Manage the login rollout gate and removal timing.|FeatureFlags|MIG-001|flag:AUTH_NEW_LOGIN; purpose:gates-LoginPage/AuthService-login; default:OFF; removalTarget:post-Phase3; owner:auth-team|S|P0|
|5|MIG-005|Feature flag `AUTH_TOKEN_REFRESH`|Manage the refresh-flow rollout gate and delayed cleanup.|FeatureFlags|MIG-002|flag:AUTH_TOKEN_REFRESH; purpose:enables-TokenManager-refresh-flow; default:OFF; removalTarget:Phase3+2-weeks; owner:auth-team|S|P0|
|6|TEST-011|Staging smoke and release checklist|Execute the release checklist and smoke tests before each rollout phase advance.|QA/Release|MIG-001, MIG-002, MIG-003|checks:staging-smoke,LoginPage/RegisterPage/AuthProvider,feature-flags,runbooks,dashboards,migration-script,sign-offs|M|P0|
|7|TEST-012|Rollback drill|Exercise the rollback procedure in staging and verify each rollback trigger path is actionable.|QA/Platform|MIG-001, OPS-001, OPS-002|steps:disable-AUTH_NEW_LOGIN; smoke-test-legacy; inspect-logs/traces; restore-backup-on-corruption; notify-auth+platform; postmortem≤48h|M|P0|
|8|TEST-013|Canary and GA validation pack|Collect the production-readiness evidence used for go/no-go and GA continuation.|Release/Monitoring|MIG-002, MIG-003|evidence:p95<200ms,500-concurrent-user-validation,security-review-complete,integration-tests-pass-against-real-PostgreSQL/Redis|M|P0|
|9|OPS-011|Go/no-go gate|Create the explicit release gate aggregating technical, compliance, and operational approvals.|ReleaseGovernance|TEST-011, TEST-013|approvals:test-lead,eng-manager,security,platform; inputs:dashboards,runbooks,security-review,rollback-drill; outcome:go-or-no-go-recorded|S|P0|
|10|OBS-007|Rollout SLO dashboard|Create a rollout-focused dashboard that overlays flag state, traffic percentage, latency, errors, and Redis health.|Grafana/Release|OBS-006, MIG-002, MIG-003|panels:flag-state,traffic-share,p95,error-rate,Redis-failures,health-status; consumers:on-call+release-managers|S|P1|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AUTH_NEW_LOGIN` flag → login routes and backend path|Feature flag|traffic progressively switched from legacy auth to new auth|M5|MIG-001, MIG-002, MIG-003|
|`AUTH_TOKEN_REFRESH` flag → refresh flow|Feature flag|silent refresh enabled only after beta confidence is reached|M5|MIG-003, AuthProvider|
|Rollback drill → runbooks + dashboards|Release process|trigger thresholds mapped to concrete operational actions|M5|on-call, release managers|
|Go/no-go gate → sign-off workflow|Governance|technical and compliance evidence consolidated before promotion|M5|test-lead, eng-manager, security, platform|
|Rollout SLO dashboard → canary decisions|Dashboard|flag/traffic overlays bound to live latency, error, and Redis signals|M5|release managers, on-call|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Migration causes user-impacting regressions or data loss|High|Low|High|Use staged traffic, idempotent migration behavior, backups, and a tested rollback drill before GA.|platform|
|2|Canary thresholds are exceeded without a fast operational response|High|Medium|High|Bind rollout advancement to OBS-007, OPS-008 alerts, and OPS-011 go/no-go gate ownership.|release-manager|
|3|Feature flags remain permanently and create operational sprawl|Medium|Medium|Medium|Assign owners and explicit removal targets to MIG-004 and MIG-005 and review cleanup after GA stabilization.|architect|
|4|Release evidence is incomplete at decision time|High|Medium|High|Require TEST-011..013 and OPS-011 completion before promotion beyond each phase.|qa|

### Milestone Dependencies — M5

- All M4 observability, admin, and hardening work complete.
- Feature flag platform available in production.
- On-call staffing active for the first two post-GA weeks.
- Release managers and approvers available for staged sign-off.

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1-M5|Required|Do not proceed beyond M1 without production-like DB provisioning|
|Redis 7+|M2-M5|Required|Disable refresh flow and force re-login if Redis is degraded|
|Node.js 20 LTS|M2-M5|Required|No supported fallback; runtime standardization required|
|bcryptjs|M2-M4|Required|Swap only through `PasswordHasher` abstraction after explicit security review|
|jsonwebtoken|M2-M4|Required|No supported fallback in v1.0|
|SendGrid or equivalent|M3-M5|Required|Fallback support channel for reset failures; block password-reset GA if absent|
|Frontend routing framework|M3|Required|No full user-journey launch without route support|
|SEC-POLICY-001|M1-M5|Required|Escalate to security before shipping any crypto or transport changes|
|COMPLIANCE-001|M1-M5|Required|Hold audit-log and consent implementation until clarified|
|INFRA-DB-001|M1,M5|Required|Use staging-equivalent schema rehearsal while infra dependency is resolved|

### Infrastructure Requirements

- Kubernetes deployment capacity for `AuthService` with HPA up to 10 replicas.
- Secret management for RS256 key material with quarterly rotation support.
- APM, Prometheus, Grafana, and Alertmanager wired before beta traffic.
- Testcontainers or equivalent ephemeral PostgreSQL/Redis support in CI.
- Backup/restore path for `UserProfile` and audit-log storage verified before GA.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS or unsafe browser token storage|M3,M4,M5|Medium|High|Keep access tokens in memory, refresh tokens in HttpOnly cookies, short access TTL, revoke on logout/reset.|security|
|R-002|Brute-force attacks or weak lockout enforcement|M1,M2,M4,M5|High|Medium|Encode 5 failures/15 minutes, API gateway rate limits, account lock state, and monitoring on login failures.|backend|
|R-003|Data loss during migration or rollback|M5|Low|High|Use staged rollout, idempotent migration behavior, backups, rollback drill, and production gates.|platform|
|R-PRD-001|Low registration adoption due to poor UX|M3,M5|Medium|High|Use minimal forms, inline validation, registration funnel metrics, and post-launch UX iteration.|frontend|
|R-PRD-002|Security breach from implementation flaws|M2,M4,M5|Low|Critical|Dedicated security review, crypto validation, log redaction checks, and penetration-style validation before GA.|security|
|R-PRD-003|Compliance failure from incomplete audit logging|M1,M4,M5|Medium|High|Resolve retention conflict early, implement admin query surfaces, and verify required event fields in TEST-010.|compliance|
|R-PRD-004|Email delivery failures block password reset|M3,M4,M5|Low|Medium|Use asynchronous dispatch, delivery monitoring, alerting, and fallback support path.|backend|
|R-004|Contract drift between PRD expectations and TDD/API behavior|M3|Medium|Medium|Document and resolve conflicts explicitly (e.g., registration auto-login) and keep roadmap values consistent.|architect|
|R-005|Admin persona remains unsupported despite emitted audit logs|M4|Medium|High|Add API-008..010 and supporting services as explicit roadmap gap fills.|architect|
|R-006|Rollout thresholds are exceeded without clear stop conditions|M5|Medium|High|Bind canary advancement to dashboards, alerts, and go/no-go approvals.|release-manager|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Technical-1|Login response time p95|<200ms|APM + OBS-002 + TEST-009 evidence|M4|
|Technical-2|Registration success rate|>99%|Funnel and API outcome metrics from OBS-004|M4|
|Technical-3|Token refresh latency p95|<100ms|APM traces on refresh path + rollout dashboard|M4|
|Technical-4|Service availability|99.9% uptime over 30-day windows|API-011 health monitoring + OPS-008 alerts|M4-M5|
|Technical-5|Password hash time|<500ms|bcrypt benchmark and config validation in TEST-010|M4|
|Business-6|Registration conversion|>60%|Landing→register→confirmed funnel instrumentation|M5|
|Business-7|Daily active authenticated users|>1000 within 30 days of GA|Auth token issuance analytics after GA|M5|
|Business-8|Average session duration|>30 minutes|Token refresh event analytics and session tracking|M5|
|Business-9|Failed login rate|<5% of attempts|Auth event log analysis on login failures|M4-M5|
|Business-10|Password reset completion|>80%|Reset-request→reset-confirm funnel from TEST-007 + telemetry|M5|
|Goal-11|G-001 secure registration/login|Implemented and verified|FR-AUTH-001/002 + TEST-001/002/004/006|M2-M3|
|Goal-12|G-002 stateless token sessions|Implemented and verified|FR-AUTH-003 + API-004 + TEST-003/005|M2|
|Goal-13|G-003 self-service password reset|Implemented and verified|FR-AUTH-005 + API-005/006 + TEST-007|M3|
|Goal-14|G-004 UserProfile via `/auth/me`|Implemented and verified|FR-AUTH-004 + API-003 + ProfilePage validation|M2-M3|
|Goal-15|G-005 frontend integration|Implemented and verified|COMP-001..004 + TEST-006/008|M3|
|Release-16|Functional + test readiness|All FR-AUTH-001 through FR-AUTH-005 implemented and test-verified; unit coverage >80%; integration tests pass against real PostgreSQL/Redis|Release checklist + TEST-001..005 + TEST-006..008|M5|
|Release-17|Security + scale readiness|Security review complete; bcrypt cost verified; JwtService key rotation documented; 500-concurrent-user p95 <200ms validated|TEST-009 + TEST-010 + release gate evidence|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session architecture|JWT access tokens + hashed Redis refresh tokens|Server-side sessions; API keys for v1.0; long-lived JWTs only|TDD architecture specifies stateless JWT + refresh, PRD requires persistent sessions and programmatic refresh, and this path keeps horizontal scaling simple while preserving revocation control.|
|Audit retention policy|12-month auth event retention|90-day TDD default|PRD legal/compliance requirement is the higher-precedence source for regulatory retention; roadmap applies 12 months consistently to DM-003, COMP-009, API-008, OPS sizing, and success criteria.|
|Password reset email dispatch|Asynchronous send with immediate generic confirmation|Synchronous send in request path|PRD asks for delivery within 60 seconds, while NFR-PERF-001 requires fast auth endpoints; asynchronous send satisfies both without exposing enumeration behavior.|
|Registration success behavior for v1.0|Return `201 UserProfile` and redirect to login|Immediate auto-login after registration|TDD/API extraction defines the concrete endpoint contract; changing it in the roadmap would silently fork the API. PRD expectation is preserved as a tracked product gap for follow-up.|
|Programmatic auth scope|User-scoped login + refresh only in v1.0|Dedicated API-key/service-account flow in v1.0|PRD JTBD for Sam is partially satisfied by refresh contracts; PRD and TDD scope constraints explicitly defer API-key style auth beyond v1.0.|
|Admin operational support|Add query and lock/unlock APIs in M4|Leave admin workflows undocumented/manual|PRD persona Jordan requires queryable auth events and account lock management; without these, audit logging alone does not satisfy the user story or incident-response need.|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|2026-03-31|2026-04-14|Roadmap M1 ↔ TDD M1 Core `AuthService` foundation/contracts|
|M2|2 weeks|2026-04-15|2026-04-28|Roadmap M2 ↔ TDD M2 Token Management + core auth APIs|
|M3|2 weeks|2026-04-29|2026-05-12|Roadmap M3 ↔ TDD M3 Password Reset + TDD M4 Frontend Integration|
|M4|2 weeks|2026-05-13|2026-05-26|Roadmap M4 ↔ TDD hardening work preceding GA; adds PRD compliance/admin gaps|
|M5|2 weeks|2026-05-27|2026-06-09|Roadmap M5 ↔ TDD M5 GA Release and rollout phases 1-3|

**Total estimated duration:** 10 weeks (2026-03-31 to 2026-06-09)
