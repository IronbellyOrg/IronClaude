---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
base_variant: "none"
variant_scores: "none"
convergence_score: 0.94
debate_rounds: 0
generated: "2026-04-19"
generator: "single"
total_milestones: 4
total_task_rows: 89
risk_count: 7
open_questions: 9
domain_distribution:
  frontend: 22
  backend: 34
  security: 20
  performance: 12
  documentation: 12
consulting_personas: [architect, backend, security, frontend, qa, devops]
milestone_count: 4
milestone_index:
  - id: M1
    title: "Security, data, and platform foundation"
    type: SECURITY
    priority: P0
    dependencies: []
    deliverable_count: 21
    risk_level: High
  - id: M2
    title: "Core authentication and session experience"
    type: FEATURE
    priority: P0
    dependencies: [M1]
    deliverable_count: 23
    risk_level: High
  - id: M3
    title: "Profile, recovery, and admin visibility"
    type: FEATURE
    priority: P0
    dependencies: [M1, M2]
    deliverable_count: 20
    risk_level: Medium
  - id: M4
    title: "Validation, rollout, and operational readiness"
    type: MIGRATION
    priority: P0
    dependencies: [M1, M2, M3]
    deliverable_count: 25
    risk_level: High
total_deliverables: 89
total_risks: 7
estimated_milestones: 4
validation_score: 0.94
validation_status: PASS_WITH_WARNINGS
---
# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers the authentication platform as a security-first foundation for Q2 2026 personalization while meeting the Q3 2026 SOC2 audit window. The sequence front-loads schema, cryptography, compliance, and gateway controls before user-facing flows so later rollout decisions are constrained by security and data integrity rather than retrofitted after launch.

The plan preserves every extracted requirement, model, API, component, test artifact, migration item, and operational item as its own deliverable row, then adds PRD-required gap fills for logout, password-reset UI surfaces, and admin audit-log query capabilities. From an architect perspective, the critical path is policy and storage correctness first, then auth/session flows, then recovery and observability, and finally performance validation with staged rollout under reversible flags.

**Business Impact:** Unblocks the personalization roadmap tied to approximately $2.4M annual revenue, replaces manual access recovery with self-service flows, and establishes authenticated audit trails needed for enterprise compliance.

**Complexity:** HIGH (0.72) — the solution spans backend services, React surfaces, Redis token state, PostgreSQL identity and audit storage, email delivery, compliance controls, rate limiting, and multi-phase rollout under failure-sensitive conditions.

**Critical path:** SEC-POLICY-001 + INFRA-DB-001 + M1 security/data foundation → M2 login/register/refresh/logout session flows → M3 profile/reset/admin visibility and auditability → M4 performance proof, phased migration, rollback readiness, and on-call cutover.

**Key architectural decisions:**

- Use stateless RS256 access tokens with Redis-backed refresh-token records so session continuity scales horizontally while preserving revocation and device-level control.
- Treat PRD-mandated 12-month audit retention as the active target now, because deferring the TDD/PRD conflict would invalidate schema, storage, and compliance evidence later.
- Fill PRD coverage gaps explicitly with logout and admin audit-event query deliverables instead of assuming those capabilities are implied by existing auth components.

**Open risks requiring resolution before M1:**

- OQ-007 audit-log retention conflict changes storage shape, retention jobs, and compliance evidence.
- OQ-004 maximum refresh tokens per user changes Redis cardinality and revocation strategy.
- OQ-005 lockout policy sign-off affects login semantics, gateway behavior, and UX messaging.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Security, data, and platform foundation|SECURITY|P0|2w|—|21|High|
|M2|Core authentication and session experience|FEATURE|P0|3w|M1|23|High|
|M3|Profile, recovery, and admin visibility|FEATURE|P0|2w|M1, M2|20|Medium|
|M4|Validation, rollout, and operational readiness|MIGRATION|P0|4w|M1, M2, M3|25|High|

## Dependency Graph

`SEC-POLICY-001 + INFRA-DB-001 + PostgreSQL + Redis + Node.js 20 + gateway + SendGrid -> M1 -> M2 -> M3 -> M4`
`MIG-004 + MIG-005 -> MIG-001 -> MIG-002 -> MIG-003`
`COMP-014 -> MIG-004/MIG-005; COMP-019 -> COMP-004 -> API-001/API-002/API-003/API-004/API-007; COMP-025 -> API-008`

## M1: Security, data, and platform foundation

**Objective:** Freeze the security model, persistence model, and cross-cutting wiring needed by every downstream milestone. | **Duration:** 2 weeks (W1-W2) | **Entry:** Extraction accepted; SEC-POLICY-001 available; PostgreSQL 15+, Redis 7+, gateway, and SendGrid environments allocated. | **Exit:** Identity and token storage are defined, security policies are encoded, cross-cutting modules are wired, and feature-flag foundations exist for reversible rollout.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile model and table|Define the canonical user identity model and PostgreSQL schema, including security and consent support needed by registration and lockout workflows.|PostgreSQL, UserRepo|SEC-POLICY-001, INFRA-DB-001|id:UUIDv4-PK-NOT-NULL; email:string-UNIQUE-NOT-NULL-indexed-lowercase-normalized; displayName:string-NOT-NULL-2-100; createdAt:ISO8601-NOT-NULL-default-now; updatedAt:ISO8601-NOT-NULL-auto-updated; lastLoginAt:ISO8601-nullable; roles:string[]-NOT-NULL-default-[user]; extension-columns:password_hash,failed_login_count,locked_until,consent_recorded_at|L|P0|
|2|DM-002|AuthToken contract and token record design|Define the access/refresh token contract and Redis-backed refresh-token record structure used by issuance, rotation, and revocation.|TokenManager, Redis, JwtService|SEC-POLICY-001, OQ-004|accessToken:JWT-string-NOT-NULL-RS256; refreshToken:string-NOT-NULL-unique-opaque; expiresIn:number-NOT-NULL-900; tokenType:string-NOT-NULL-Bearer; redis-record:userId,tokenHash,issuedAt,expiresAt,revokedAt?,deviceId?|M|P0|
|3|COMP-009|User repository|Implement the database access layer for user create/read/update flows, uniqueness checks, lockout counters, and profile projection.|UserRepo|DM-001, INFRA-DB-001|operations:createUser,findByEmail,findById,updateLastLogin,incrementFailedLogins,lockAccount,clearFailedLogins,listRoles; queries-parameterized; transactions-used-for-multi-write|M|P0|
|4|COMP-010|Audit log store|Define PostgreSQL storage for auth-event audit records and retention-safe indexing.|PostgreSQL|INFRA-DB-001, OQ-007|fields:event_id,user_id?,email_hash?,event_type,timestamp,ip,outcome,correlation_id,metadata_json; indexes:user_id,timestamp,event_type; retention-job-compatible|M|P0|
|5|COMP-011|Reset token store|Create the dedicated token store for password-reset issuance, expiration, and single-use enforcement.|Redis|DM-001|fields:tokenHash,userId,issuedAt,expiresAt,usedAt?; TTL:3600s; namespaces-separated-from-refresh-tokens; single-use-check-supported|M|P0|
|6|COMP-012|Lockout policy module|Centralize failed-login counting and lockout-window computation so AuthService and gateway rules use one policy source.|AuthService, UserRepo|DM-001, OQ-005|inputs:userId,attemptTimestamp,outcome; policy:5-failures/15-min-window-default; outputs:isLocked,lockedUntil,remainingAttempts; reset-on-success-supported|M|P0|
|7|COMP-014|Feature-flag adapter|Provide application-side access to rollout flags and cohort checks for new login and refresh behavior.|Runtime, rollout control|—|flags:AUTH_NEW_LOGIN,AUTH_TOKEN_REFRESH; operations:isEnabled,isCohortMember,getPercentage,setDefault; environment-aware-loading|S|P0|
|8|COMP-015|Gateway policy bundle|Define gateway-side reusable policies for rate limiting, CORS, TLS, and auth middleware attachment.|API Gateway|SEC-POLICY-001|policies:login-rate-limit,register-rate-limit,me-rate-limit,refresh-rate-limit,CORS-allowlist,TLS1.3,error-mapping; attachable-per-route|M|P0|
|9|COMP-017|Health check endpoint|Add a dedicated service health endpoint used by uptime probes and rollout gating.|Runtime, gateway|—|route:/healthz; checks:app-ready,db-connectivity,redis-connectivity,key-material-loaded; returns:200/503-with-machine-readable-status|S|P0|
|10|COMP-018|Metrics registry|Create a shared metrics registration module for counters, histograms, and gauges consumed by auth flows and ops alerts.|Telemetry|—|registers:counters,histograms,gauges; exports:Prometheus-format; labels-standardized:route,outcome,component|S|P0|
|11|COMP-026|Secrets and key-rotation adapter|Encapsulate RSA key loading, key version lookup, and rotation-safe secret access for JwtService and mail credentials.|Secrets manager, JwtService|SEC-POLICY-001|secrets:jwt_private_key,jwt_public_key,current_kid,sendgrid_api_key,db_credentials,redis_credentials; supports:versioned-read,rotation-reload|M|P0|
|12|COMP-028|Consent capture flow|Define the end-to-end consent capture shape so registration, storage, and audit logs use the same consent semantics.|RegisterPage, AuthService, AuditLogStore|NFR-COMP-001|fields:consentGiven,consentTimestamp,policyVersion,sourceChannel; recorded-at-registration-only; auditable|S|P0|
|13|COMP-029|Error envelope module|Standardize auth error codes and JSON response envelopes across service and gateway handlers.|Runtime, gateway|—|shape:error.code,error.message,error.status; codes:AUTH_INVALID_CREDENTIALS,AUTH_LOCKED,AUTH_RATE_LIMITED,AUTH_TOKEN_EXPIRED,AUTH_TOKEN_REVOKED,AUTH_VALIDATION_FAILED|S|P0|
|14|COMP-030|CORS and TLS policy|Encode frontend-origin allowlists and TLS 1.3-only transport constraints as shared configuration.|Gateway, frontend integration|SEC-POLICY-001|origins:known-frontend-origins-only; credentials:restricted; tls:min-1.3; HSTS:enabled; no-wildcard-CORS|S|P0|
|15|NFR-SEC-001|Password hashing policy enforcement|Establish bcrypt cost-factor requirements and validation gates before PasswordHasher implementation begins.|PasswordHasher|SEC-POLICY-001|algorithm:bcrypt; cost-factor:12; verification-tests-required; downgrade-blocked-in-CI|S|P0|
|16|NFR-SEC-002|JWT signing policy enforcement|Establish RS256 and 2048-bit RSA key requirements, including rotation and validation expectations.|JwtService|SEC-POLICY-001|algorithm:RS256; key-size:2048-bit-RSA; rotation:quarterly; unsupported-algorithms:rejected; config-validation-required|S|P0|
|17|NFR-COMP-001|GDPR consent requirement design|Bind registration and persistence design to GDPR consent recording with timestamp before API contracts are finalized.|RegisterPage, AuthService, UserRepo|COMP-028|consent-required-at-registration; consentTimestamp-stored; policyVersion-tracked; registration-without-consent-rejected|S|P0|
|18|NFR-COMP-003|NIST password-storage requirement design|Constrain storage and logging design so raw passwords are never persisted, echoed, or emitted to telemetry.|PasswordHasher, logging|NFR-SEC-001|raw-password-never-persisted; raw-password-never-logged; only-adaptive-one-way-hashes-stored|S|P0|
|19|NFR-COMP-004|GDPR data-minimization boundary|Freeze the allowed identity surface so no additional PII enters schemas or APIs during later milestones.|Architecture|DM-001|collected-fields:email,password_hash,displayName,consent-record; excluded-fields:phone,address,DOB,government-id; API-and-logs-reviewed|S|P0|
|20|MIG-004|Feature flag AUTH_NEW_LOGIN|Define the rollout flag that gates the new login route and backend endpoint behavior.|Feature flags|COMP-014|flag:AUTH_NEW_LOGIN; default:OFF; supports:internal-users,percentage-rollout,global-disable; cleanup-planned-post-GA|S|P0|
|21|MIG-005|Feature flag AUTH_TOKEN_REFRESH|Define the rollout flag that gates refresh-token behavior independently from the login rollout.|Feature flags|COMP-014|flag:AUTH_TOKEN_REFRESH; default:OFF; supports:independent-enablement,global-disable; cleanup-planned-post-GA+2-weeks|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-014 feature-flag adapter|Registry/adapter|Yes|M1|MIG-004, MIG-005, rollout controller|
|COMP-015 gateway policy bundle|Middleware registry|Yes|M1|API-001 through API-008|
|COMP-026 secrets adapter|DI/service locator|Yes|M1|COMP-006, COMP-007, COMP-004|
|COMP-029 error envelope module|Shared contract|Yes|M1|Gateway handlers, frontend client|
|COMP-030 CORS/TLS policy|Gateway config|Yes|M1|All auth routes|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-005 Incomplete audit-log design causes compliance gaps later|Medium|Medium|SOC2 evidence becomes non-recoverable if event fields or retention are wrong at schema time|Define COMP-010 and NFR-COMP-001/003/004 before API implementation; resolve OQ-007 in M1|security, compliance|
|2|R-003 Early schema mistakes create migration or rollback risk|High|Low|Identity data or retention jobs may require destructive rework during rollout|Keep DM-001/DM-002 versioned, migration-safe, and reviewed before M2 starts|backend, platform|

### Milestone Dependencies — M1

- PostgreSQL 15+, Redis 7+, Node.js 20 LTS, gateway access, and SendGrid credentials must exist before implementation starts.
- SEC-POLICY-001 must remain the authoritative source for hashing, token, and transport rules.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-004|Maximum refresh tokens per user across devices?|Changes DM-002 Redis cardinality, revocation fan-out cost, and session UX across devices.|Product|2026-04-19|
|2|OQ-007|Audit-log retention conflict: TDD says 90 days, PRD says 12 months.|Blocks COMP-010 sizing, retention-pruner logic, and compliance evidence. Working assumption is 12 months.|Security, Compliance|2026-04-19|

## M2: Core authentication and session experience

**Objective:** Implement the backend auth services, primary APIs, and user-facing session surfaces that deliver registration, login, refresh, logout, and profile continuity. | **Duration:** 3 weeks (W3-W5) | **Entry:** M1 storage, policies, and cross-cutting modules are complete; feature flags exist; key material is available. | **Exit:** End users and API consumers can register, log in, refresh tokens, log out, and maintain active sessions through the defined frontend and backend contracts.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|22|COMP-005|AuthService facade|Implement the backend orchestrator that owns auth use cases and delegates to specialized collaborators.|AuthService|COMP-009, COMP-011, COMP-012, COMP-026, COMP-029|type:backend-orchestrator/facade; delegates:PasswordHasher,TokenManager,UserRepo; hosts:API-001,API-002,API-003,API-004,API-005,API-006,API-007,API-008; dependencies:PostgreSQL-via-pg-pool,Redis-via-TokenManager,SendGrid; operations:login,register,getMe,refresh,logout,requestPasswordReset,confirmPasswordReset,listAuthEvents|L|P0|
|23|COMP-006|TokenManager|Implement token issuance, rotation, validation, and revocation over Redis-backed refresh-token state.|TokenManager|DM-002, COMP-026|type:backend-token-lifecycle; responsibilities:issue,revoke,rotate-refresh-tokens,store-hashed-refresh-tokens; storage:Redis; refresh-token-TTL:7-days; delegates-signing/verification-to:JwtService; operations:issuePair,refreshPair,revokeToken,revokeUserTokens,validateRefreshToken|L|P0|
|24|COMP-007|JwtService|Implement the JWT signer/verifier with required keying, rotation, and skew constraints.|JwtService|NFR-SEC-002, COMP-026|type:backend-JWT-signer/verifier; algorithm:RS256; key-size:2048-bit-RSA; rotation:quarterly; latency-target:<5ms-sign/verify; clock-skew-tolerance:5s; operations:sign,verify,decode|M|P0|
|25|COMP-008|PasswordHasher|Implement the bcrypt password component with configurable cost and benchmarked runtime.|PasswordHasher|NFR-SEC-001|type:backend-password-hashing; algorithm:bcrypt; configurable-cost-factor:default-12; operations:hash(plain),verify(plain,hash); benchmark:~300ms-per-hash-target; plaintext-never-persisted-or-logged|M|P0|
|26|FR-AUTH-001|Email/password login flow|Deliver credential authentication with generic 401 handling, lockout enforcement, and token issuance on success.|AuthService, PasswordHasher, TokenManager|COMP-005, COMP-006, COMP-008, COMP-012|valid-credentials:return-200-AuthToken-with-accessToken-and-refreshToken; invalid-credentials:return-401-generic; non-existent-email:return-401-no-enumeration; locked-account-after-5-failures-in-15-minutes|L|P0|
|27|FR-AUTH-002|Registration flow|Deliver validated user registration with uniqueness checks, password policy enforcement, consent capture, and immediate token-capable account creation.|AuthService, UserRepo, PasswordHasher|COMP-005, COMP-008, COMP-028, NFR-COMP-001|valid-registration:return-201-UserProfile; duplicate-email:return-409; weak-password(<8,no-uppercase,no-number):return-400; bcrypt-cost-factor-12-stored; consent-captured-and-timestamped|L|P0|
|28|FR-AUTH-003|JWT issuance and silent refresh flow|Deliver access/refresh token issuance and refresh-token rotation through backend and client-consumable APIs.|TokenManager, JwtService, AuthProvider|COMP-006, COMP-007, DM-002|login-returns-accessToken(15m)-and-refreshToken(7d); POST-/auth/refresh-valid-refreshToken-returns-new-AuthToken-pair; expired-refreshToken-returns-401; revoked-refreshToken-returns-401|L|P0|
|29|FR-AUTH-004|Authenticated profile retrieval|Deliver the authenticated profile read flow for current-user identity and session validation.|AuthService, UserRepo|COMP-005, COMP-009, COMP-007|GET-/auth/me-valid-accessToken-returns-UserProfile; expired-or-invalid-token-returns-401; response-includes-id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|M|P0|
|30|COMP-001|LoginPage|Implement the public login route and form surface for credential sign-in.|Frontend, AuthProvider|FR-AUTH-001, API-001|type:frontend-route-component; location:/login; auth:no; props:onSuccess,redirectUrl?; calls:API-001; stores:AuthToken-via-AuthProvider; fields:email,password|M|P0|
|31|COMP-002|RegisterPage|Implement the public registration route and form surface with client-side password checks and consent capture.|Frontend, AuthProvider|FR-AUTH-002, API-002, COMP-028|type:frontend-route-component; location:/register; auth:no; props:onSuccess,termsUrl; client-side-password-strength-validation:enabled; calls:API-002; fields:email,password,displayName,consent|M|P0|
|32|COMP-003|ProfilePage|Implement the authenticated profile route that renders current-user account data.|Frontend, AuthProvider|FR-AUTH-004, API-003|type:frontend-route-component; location:/profile; auth:yes-via-AuthProvider; calls:API-003; renders:id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|S|P1|
|33|COMP-004|AuthProvider|Implement the React auth context provider that owns session state and refresh behavior across routes.|Frontend|FR-AUTH-003, FR-AUTH-004|type:React-context-provider; props:children:ReactNode; wraps:all-routes; manages:AuthToken-state; intercepts:401; triggers:silent-refresh-via-API-004; redirects:unauthenticated-users-to-LoginPage; clears-tokens-on-tab-close|L|P0|
|34|COMP-019|Frontend auth HTTP client|Implement the frontend client abstraction with interceptor hooks for 401 handling and token-aware calls.|Frontend, AuthProvider|COMP-004, COMP-029|operations:login,register,getMe,refresh,logout,requestReset,confirmReset; 401-interceptor-wired; error-envelope-decoded|M|P0|
|35|API-001|POST /v1/auth/login|Implement the login endpoint behind gateway rate limits and generic credential-error semantics.|Gateway, AuthService|FR-AUTH-001, COMP-015, COMP-029|request:email,password; response200:accessToken,refreshToken,expiresIn,tokenType; errors:401,423,429; rate-limit:10/min/IP|M|P0|
|36|API-002|POST /v1/auth/register|Implement the registration endpoint including validation, duplicate handling, and consent enforcement.|Gateway, AuthService|FR-AUTH-002, NFR-COMP-001, COMP-015|request:email,password,displayName,consent; response201:UserProfile; errors:400,409,429; rate-limit:5/min/IP|M|P0|
|37|API-003|GET /v1/auth/me|Implement the authenticated profile endpoint with bearer-token validation and per-user throttling.|Gateway, AuthService|FR-AUTH-004, COMP-015|header:Authorization-Bearer<jwt>; response200:UserProfile; errors:401; rate-limit:60/min/user|S|P0|
|38|API-004|POST /v1/auth/refresh|Implement the refresh endpoint that exchanges a valid refresh token for a rotated auth-token pair.|Gateway, TokenManager|FR-AUTH-003, COMP-015|request:refreshToken; response200:new-AuthToken-pair; errors:401; rate-limit:30/min/user; old-refresh-token-revoked|M|P0|
|39|API-007|POST /v1/auth/logout|Add the PRD-required logout endpoint to revoke refresh-token state and clear client session context.|Gateway, AuthService, TokenManager|COMP-006, COMP-004|request:refreshToken-or-session-context; response200:idempotent-success; revokes-active-refresh-token(s); clears-client-session; redirects-to-landing-supported|M|P0|
|40|COMP-020|Logout session handler|Implement backend/session logic for logout so refresh tokens are revoked and audit logs can capture explicit sign-out events.|AuthService, TokenManager|API-007|operations:logoutSingleSession,logoutAllSessions?; revocation-atomic; audit-event-emitted|M|P0|
|41|NFR-PERF-001|Auth endpoint latency budget integration|Wire tracing and instrumentation points into every auth endpoint so p95 latency is measurable against the <200ms target.|Telemetry, AuthService|COMP-018, API-001, API-002, API-003, API-004|all-auth-endpoints-instrumented; spans-on-AuthService-methods; p95-queryable-per-endpoint; target:<200ms|S|P0|
|42|NFR-COMP-002|Audit-event emission contract|Define the mandatory event payload emitted by login, register, refresh, and logout actions for SOC2 evidence.|AuthService, AuditLogStore|COMP-010, COMP-005, API-007|fields:userId,timestamp,ip,outcome,eventType,correlationId; emitted-on-login,register,refresh,logout; retention-target:12-month-working-assumption|S|P0|
|43|COMP-021|Session refresh scheduler|Implement the frontend timing logic that performs silent refresh before access-token expiry and falls back to login if renewal fails.|AuthProvider|FR-AUTH-003, API-004|refresh-triggered-before-15-min-expiry; failed-refresh-clears-session-and-redirects; active-session-persists-across-page-refresh|M|P0|
|44|COMP-022|Route guard and redirect policy|Implement protected-route enforcement and post-auth redirect behavior across login, profile, and logout boundaries.|Frontend, AuthProvider|COMP-001, COMP-003, COMP-004|unauthenticated-users-redirected-to-/login; redirectUrl-respected; authenticated-users-blocked-from-protected-route-loss|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-004 AuthProvider|Context/provider|Yes|M2|COMP-001, COMP-002, COMP-003, COMP-019, COMP-021, COMP-022|
|COMP-019 auth HTTP client|Callback/interceptor wiring|Yes|M2|Frontend route components|
|COMP-021 refresh scheduler|Timer/callback|Yes|M2|COMP-004 AuthProvider|
|COMP-012 lockout module|Policy callback|Yes|M2|COMP-005, API-001|
|COMP-020 logout handler|Strategy/service|Yes|M2|API-007, COMP-004|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS enables session hijack|High|Medium|Compromised browser state can expose session continuity controls|Keep access tokens in memory, clear on tab close, use refresh-token revocation, and keep logout explicit|frontend, security|
|2|R-002 Brute-force attacks on login endpoint|Medium|High|Credential stuffing degrades security and user availability|Enforce gateway rate limits plus COMP-012 lockout and CAPTCHA contingency in later UI polish|security, backend|
|3|R-004 Low registration adoption due to poor UX|Medium|Medium|Core auth may ship but business value lags if onboarding friction stays high|Implement inline validation, minimal form fields, clear feedback, and redirect continuity in M2|product, frontend|

### Milestone Dependencies — M2

- M1 security, schema, secrets, and gateway bundles must be complete.
- API-007 logout remains a PRD gap fill and should be reflected back into the TDD.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should AuthService support API key authentication for service-to-service calls?|Could introduce an additional auth strategy, contract surface, and policy branch in COMP-005/API design.|test-lead|2026-04-15|
|2|OQ-002|Maximum allowed UserProfile.roles array length?|Changes DM-001 validation constraints, profile serialization, and future authorization compatibility.|auth-team|2026-04-01|
|3|OQ-005|Should the 5-failures/15-min lockout rule receive any additional security exceptions or recovery path changes?|Affects COMP-012, FR-AUTH-001 semantics, and customer-facing error flows.|Security|2026-04-19|
|4|OQ-006|Should "remember me" be supported to extend session duration?|Changes COMP-004/COMP-021 client behavior, DM-002 token lifetime variants, and product expectations.|Product|2026-04-19|
|5|OQ-008|PRD JTBD requires logout on shared devices; TDD lacks explicit logout FR. Keep API-007 as scope for v1.0?|Impacts whether logout is mandatory release scope. Current roadmap treats it as required.|Product, Engineering|2026-04-19|

## M3: Profile, recovery, and admin visibility

**Objective:** Deliver password-reset completion, richer profile/account visibility, compliance-grade audit access, and the missing PRD user-facing surfaces around recovery and investigation. | **Duration:** 2 weeks (W6-W7) | **Entry:** M2 auth/session flows and primary APIs are running in staging. | **Exit:** Password reset is self-service end-to-end, admin audit visibility exists, profile retrieval is stable, and compliance-meaningful logging can be queried and validated.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|45|FR-AUTH-005|Password reset flow|Deliver the two-step password reset flow with token issuance, email delivery, validation, hash update, and single-use enforcement.|AuthService, PasswordHasher, ResetTokenStore|COMP-005, COMP-008, COMP-011|POST-/auth/reset-request-valid-email-sends-reset-token-via-email; POST-/auth/reset-confirm-valid-token-updates-password-hash; reset-token-expires-after-1-hour; used-reset-tokens-cannot-be-reused|L|P0|
|46|API-005|POST /v1/auth/reset-request|Implement the password-reset request endpoint with enumeration-safe response semantics and delivery initiation.|Gateway, AuthService, SendGrid|FR-AUTH-005|request:email; response:200/202-generic-success; errors:400,429; registered-and-unregistered-emails-return-same-success-shape|M|P0|
|47|API-006|POST /v1/auth/reset-confirm|Implement the password-reset confirm endpoint with token validation, password update, and session invalidation.|Gateway, AuthService, TokenManager|FR-AUTH-005|request:token,newPassword; response200:success; errors:400,401; invalidates-all-existing-sessions-after-password-change|M|P0|
|48|COMP-023|ForgotPasswordPage|Add the frontend request-reset surface linked from LoginPage for enumeration-safe password recovery start.|Frontend|API-005, COMP-019|route:/forgot-password; field:email; generic-confirmation-message; login-page-link-present|M|P1|
|49|COMP-024|ResetPasswordPage|Add the frontend reset-confirm surface for new password entry, token submission, and redirect-to-login on success.|Frontend|API-006, COMP-019|route:/reset-password; fields:token,newPassword; validates-password-policy; success-redirects-to-/login|M|P1|
|50|COMP-025|Admin audit-event query service|Implement the minimal admin-facing backend capability that lets Jordan investigate auth events by date/user filters.|AuthService, AuditLogStore|COMP-010, NFR-COMP-002, OQ-009|operations:listAuthEventsByUser,listAuthEventsByDateRange; filters:userId,dateRange,outcome,eventType; pagination-supported; admin-only|M|P0|
|51|API-008|GET /v1/auth/events|Expose the admin audit-event query API required by the PRD Jordan persona investigation flow.|Gateway, AuthService|COMP-025|auth:admin-only; query:userId?,from?,to?,outcome?,eventType?; response:paginated-events; errors:401,403|M|P0|
|52|COMP-027|Auth-event admin page|Provide a minimal internal page or operational view that consumes API-008 for incident investigation and audit preparation.|Internal frontend/admin tooling|API-008|filters:userId,date-range,outcome,eventType; table:timestamp,userId,ip,outcome,eventType; read-only|M|P1|
|53|OPS-007|Structured auth logs|Implement structured logging for login, registration, refresh, logout, password reset, and admin audit access events with sensitive-field exclusion.|Logging, AuthService|NFR-COMP-002, NFR-COMP-003|events:login_success,login_failure,register,refresh,logout,reset_request,reset_confirm,audit_query; excludes:password,raw-token; includes:userId?,timestamp,ip,outcome|M|P0|
|54|OPS-008|Prometheus auth metrics|Expose counters and histograms for auth login, registration, refresh, and reset flows.|Telemetry|COMP-018, NFR-PERF-001|metrics:auth_login_total,auth_login_duration_seconds,auth_token_refresh_total,auth_registration_total,auth_reset_total; labels:outcome|S|P0|
|55|OPS-009|Auth alert definitions|Define and wire alerts for login failure spikes, p95 latency breaches, and Redis/token-manager failures.|Telemetry, on-call|OPS-008|alerts:login-failure-rate>20%/5m,p95>500ms,redis-connection-failures; routes:auth-team-on-call|S|P0|
|56|OPS-010|Distributed tracing across auth stack|Implement trace propagation across gateway, AuthService, PasswordHasher, TokenManager, JwtService, and reset flows.|Telemetry|COMP-018, COMP-005, COMP-006, COMP-007, COMP-008|spans:gateway->AuthService->PasswordHasher->TokenManager->JwtService->SendGrid; correlation-id-propagated; failures-attributable|M|P0|
|57|NFR-COMP-002A|12-month audit retention execution|Implement the operational retention and storage controls that realize the 12-month audit-log decision in production systems.|AuditLogStore, ops|COMP-010, OQ-007|retention:12-months; archival-or-pruning-job-defined; compliance-review-signed; TDD-update-required-recorded|M|P0|
|58|TEST-OBS-001|Audit-event completeness validation|Add tests proving every auth event path emits the required audit fields and remains queryable through API-008.|Testing, AuditLogStore|COMP-025, API-008, NFR-COMP-002|login/register/refresh/logout/reset-request/reset-confirm-events-recorded; fields:userId,timestamp,ip,outcome-present; query-filters-work|M|P0|
|59|TEST-UX-001|Password reset usability validation|Validate that the recovery flow is understandable, non-enumerating, and completes within the PRD journey expectations.|Frontend, product research|COMP-023, COMP-024|request-flow-clear; reset-email-under-60s-target; expired-link-behavior-clear; completion-rate-measured|M|P1|
|60|COMP-031|Session invalidation on password reset|Implement the PRD-required behavior that all existing sessions are revoked when password reset completes.|TokenManager, AuthService|API-006, OQ-008|all-refresh-token-records-for-user-revoked; active-client-session-forced-relogin; audit-event-emitted|M|P0|
|61|COMP-032|Profile projection formatter|Create the backend/frontend mapping layer that keeps UserProfile API responses and UI rendering fields aligned.|AuthService, frontend|FR-AUTH-004, COMP-003|fields:id,email,displayName,createdAt,updatedAt,lastLoginAt,roles-only; no-extra-PII; formatting-consistent|S|P1|
|62|NFR-REL-001A|Health-check monitoring bootstrap|Activate uptime monitoring against the health endpoint so the 99.9% availability target can be measured before rollout begins.|Telemetry, ops|COMP-017|monitor:/healthz; cadence:continuous; 30-day-rolling-window-enabled; outage-alert-hooked|S|P0|
|63|COMP-033|Reset email template and delivery adapter|Implement the reset email payload builder and SendGrid delivery wrapper with safe content and correlation IDs.|SendGrid, AuthService|API-005|template:reset-link,expiry,help-copy; no-account-enumeration-content; correlation-id-propagated; delivery-errors-observable|M|P1|
|64|COMP-034|Account investigation query filters|Add reusable filtering and pagination logic shared by admin audit-event APIs and views.|Audit query service|COMP-025|filters:userId,dateRange,outcome,eventType,ip?; pagination:cursor-or-page; deterministic-sort:timestamp-desc|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-033 reset email adapter|Callback/adapter|Yes|M3|API-005, FR-AUTH-005|
|COMP-031 password-reset invalidation|Service callback|Yes|M3|API-006, TokenManager|
|COMP-025 audit query service|Registry/service|Yes|M3|API-008, COMP-027|
|COMP-034 investigation filters|Shared query module|Yes|M3|COMP-025, API-008|
|OPS-010 tracing pipeline|Middleware/event binding|Yes|M3|All recovery and audit flows|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-006 Email delivery failures block password reset|Low|Medium|Users cannot recover access without support intervention|Use COMP-033 delivery adapter, observable failures, and support fallback path in operations|platform, product|
|2|R-005 Incomplete audit visibility fails compliance or incident response|Medium|Medium|Jordan persona and SOC2 expectations remain unmet|Implement COMP-025/API-008/TEST-OBS-001 and keep retention aligned to 12 months|security, backend|

### Milestone Dependencies — M3

- M2 core auth/session APIs and frontend plumbing must be working.
- Admin audit access is a PRD gap fill and should be reflected into the TDD after roadmap generation.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-003|Should password-reset emails be sent synchronously or asynchronously?|Changes API-005 latency budget, delivery architecture, and failure handling behavior.|Engineering|2026-04-19|
|2|OQ-009|Jordan persona needs auth-event investigation; should API-008 remain in v1.0 scope?|Impacts whether admin visibility is considered release-blocking. Current roadmap treats it as required gap fill.|Product, Security|2026-04-19|

## M4: Validation, rollout, and operational readiness

**Objective:** Prove the system against performance, reliability, rollout, rollback, migration, and on-call readiness requirements, then cut traffic in controlled phases. | **Duration:** 4 weeks (W8-W11) | **Entry:** M3 delivery complete; audit logging and reset flows are operational in staging; metrics and traces are live. | **Exit:** Test pyramid passes, performance and availability goals are measurable, rollout phases complete, rollback is rehearsed, and production support ownership is explicit.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|65|TEST-001|Unit test: valid login returns AuthToken|Validate successful login orchestration through AuthService with non-empty access and refresh tokens.|Testing, AuthService|FR-AUTH-001|input:valid-email,password; mocks:PasswordHasher.verify=true,TokenManager.issueTokens; expected:non-empty-accessToken-and-refreshToken|S|P0|
|66|TEST-002|Unit test: invalid login returns 401|Validate generic credential failure handling with no token issuance on wrong password.|Testing, AuthService|FR-AUTH-001|input:valid-email,wrong-password; mocks:PasswordHasher.verify=false; expected:401; TokenManager-not-called|S|P0|
|67|TEST-003|Unit test: refresh with valid token|Validate TokenManager rotation behavior for a valid refresh token and new token-pair issuance.|Testing, TokenManager|FR-AUTH-003|input:valid-refreshToken; mocks:redis-active-record,JwtService.sign; expected:old-token-revoked,new-AuthToken-pair-issued|S|P0|
|68|TEST-004|Integration test: registration persists UserProfile|Validate end-to-end registration persistence against PostgreSQL with stored bcrypt hash and profile payload consistency.|Testing, PostgreSQL, AuthService|FR-AUTH-002, DM-001|input:new-email,password,displayName,consent; expected:UserProfile-row-created,password-hash-persisted,payload-matches-row|M|P0|
|69|TEST-005|Integration test: expired refresh token rejected|Validate refresh-token expiry enforcement against Redis-backed token state.|Testing, Redis, TokenManager|FR-AUTH-003, DM-002|input:expired-refreshToken; expected:401; no-new-token-pair-issued|M|P0|
|70|TEST-006|E2E test: register then log in|Validate the primary user journey across RegisterPage, LoginPage, AuthProvider, and ProfilePage.|Frontend, backend, Playwright|COMP-002, COMP-001, COMP-004, COMP-003|flow:RegisterPage->LoginPage->ProfilePage; expected:session-established,profile-shows-correct-UserProfile|M|P0|
|71|NFR-PERF-002|Concurrent login load validation|Prove support for 500 concurrent login requests under load using k6 and backend telemetry.|Performance testing|API-001, NFR-PERF-001|load:500-concurrent-login-requests; measurement:k6; errors-below-threshold; capacity-observed|M|P0|
|72|NFR-REL-001|Availability validation and health SLO|Operationalize the 99.9% uptime requirement with health-check monitoring and alerting windows.|Ops, telemetry|COMP-017, NFR-REL-001A|availability-target:99.9%-rolling-30-day; health-check-monitoring-enabled; alert-thresholds-documented|S|P0|
|73|MIG-001|Phase 1 internal alpha rollout|Deploy to staging/internal users with manual validation of all auth capabilities before external exposure.|Rollout, auth-team, QA|MIG-004, MIG-005, TEST-001, TEST-006|duration:1-week; audience:auth-team+QA; FR-AUTH-001..005-pass-manual-testing; zero-P0/P1-bugs|M|P0|
|74|MIG-002|Phase 2 beta 10% rollout|Expose the new auth system to 10% of traffic under live telemetry and rollback guardrails.|Rollout, gateway|MIG-001, NFR-PERF-002, OPS-009|duration:2-weeks; audience:10%-of-traffic; p95<200ms; error-rate<0.1%; zero-Redis-connection-failures|L|P0|
|75|MIG-003|Phase 3 general availability|Move all traffic to the new auth service, deprecate legacy endpoints, and enable full refresh behavior.|Rollout, gateway, auth-team|MIG-002|duration:1-week; audience:100%-traffic; AUTH_NEW_LOGIN-removed; AUTH_TOKEN_REFRESH-enabled; dashboards-green|M|P0|
|76|MIG-006|Rollback procedure|Codify and rehearse the rollback sequence for disabling rollout flags, restoring service, and notifying stakeholders.|Rollout, ops|MIG-004, MIG-005|steps:disable-AUTH_NEW_LOGIN; smoke-test-legacy-login; investigate-RCA; restore-backup-if-needed; notify-auth+platform; post-mortem-within-48h|M|P0|
|77|MIG-007|Rollback triggers|Define explicit thresholds that force rollback without manual interpretation drift.|Rollout, ops|MIG-006, OPS-009|triggers:p95>1000ms-for>5m,error-rate>5%-for>2m,Redis-failures>10/min,UserProfile-data-loss-or-corruption|S|P0|
|78|OPS-001|Runbook: AuthService down|Create and validate the outage runbook for full auth-service disruption.|Ops, auth-team|MIG-006|symptoms:5xx-on-/auth/*; diagnosis:pods,db,logs,redis; resolution:restart,failover,re-login-guidance; escalation:auth-team->platform-team|S|P0|
|79|OPS-002|Runbook: token refresh failures|Create and validate the runbook for refresh-specific degradation and forced re-login scenarios.|Ops, auth-team|MIG-006, COMP-021|symptoms:unexpected-logouts,redirect-loops,refresh-errors; diagnosis:Redis,JwtService,secrets,flag-state; resolution:scale-redis,remount-secrets,enable-flag-if-off|S|P0|
|80|OPS-003|On-call expectations|Define response-time, ownership, and command responsibilities for auth incidents.|Ops, auth-team|OPS-001, OPS-002|P1-ack-within-15-minutes; 24/7-rotation-first-2-weeks-post-GA; escalation-path-documented|S|P1|
|81|OPS-004|Capacity plan: AuthService pods|Define baseline and scale-out behavior for service replicas under expected traffic.|Ops, platform|NFR-PERF-002|current:3-replicas; scaling:HPA-to-10-on-CPU>70%; expected:500-concurrent-users|S|P1|
|82|OPS-005|Capacity plan: PostgreSQL connections|Define pool sizing and scaling triggers for database connectivity under auth load.|Ops, platform, DB|NFR-PERF-002|pool-size:100; average:50-concurrent-queries; scale-to-200-if-wait>50ms|S|P1|
|83|OPS-006|Capacity plan: Redis memory|Define baseline and trigger-based scaling for refresh-token and reset-token memory usage.|Ops, platform, Redis|DM-002, COMP-011|current:1GB; expected:~100K-refresh-tokens(~50MB); scale-to-2GB-at>70%-utilization|S|P1|
|84|TEST-SEC-001|Security review and penetration test gate|Run dedicated security validation before GA to reduce implementation-flaw exposure.|Security review, QA|MIG-001, OPS-001|security-review-complete; pen-test-findings-tracked; no-unresolved-critical-issues-before-MIG-003|M|P0|
|85|TEST-PERF-001|Latency and refresh benchmark suite|Measure login, refresh, and hash timing against roadmap success thresholds under realistic load.|Performance testing|NFR-PERF-001, NFR-PERF-002, NFR-SEC-001|login-p95<200ms; refresh-p95<100ms; PasswordHasher.hash<500ms; benchmark-results-archived|M|P0|
|86|TEST-REL-001|Uptime and failover drill|Exercise health checks, alerting, and failover procedures before GA cutover.|Ops, QA|NFR-REL-001, OPS-001, OPS-002|synthetic-health-checks-fire; alerts-route-correctly; drill-completed-with-postmortem|M|P0|
|87|TEST-COV-001|Core auth coverage gate|Enforce >80% unit coverage for AuthService, TokenManager, JwtService, and PasswordHasher.|Testing, CI|TEST-001, TEST-002, TEST-003|coverage>80%-for-AuthService,TokenManager,JwtService,PasswordHasher; CI-blocks-below-threshold|S|P0|
|88|COMP-035|Rollout dashboard and decision panel|Provide an operational dashboard aggregating latency, error rate, Redis health, registration funnel, and rollback trigger status.|Telemetry, ops|OPS-008, OPS-009, NFR-PERF-002|panels:latency,error-rate,redis-health,registration-conversion,rollback-triggers; used-in-MIG-002-and-MIG-003-go/no-go|M|P1|
|89|COMP-036|Legacy auth coexistence bridge|Implement any temporary compatibility routing or smoke-test shim needed while legacy and new auth coexist during migration.|Gateway, rollout|MIG-001, MIG-006|legacy-login-smoke-supported; new-and-legacy-routing-switchable; removed-post-GA|M|P1|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-035 rollout dashboard|Dashboard/data binding|Yes|M4|MIG-002, MIG-003, incident review|
|MIG-006 rollback procedure|Operational workflow|Yes|M4|MIG-001, MIG-002, MIG-003, OPS-001, OPS-002|
|COMP-036 legacy coexistence bridge|Routing strategy|Yes|M4|MIG-001, MIG-006|
|TEST-COV-001 CI gate|Pipeline enforcement|Yes|M4|Release decision|
|TEST-REL-001 failover drill|Operational exercise|Yes|M4|OPS-001, OPS-002|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 Data loss during migration from legacy auth|High|Low|Corrupted accounts or rollback complexity during phased launch|Use MIG-006, MIG-007, backups, coexistence bridge, and explicit rollback triggers before GA|platform, backend|
|2|R-007 Redis unavailability impairs TokenManager|Low|Medium|Refresh flow fails and users are forced to re-login|Fail closed on refresh, alert quickly, scale Redis, and document recovery in OPS-002|platform, backend|
|3|R-005 Compliance failure from incomplete audit logging|Medium|Low|Launch may pass traffic but fail audit obligations|Keep audit validation and retention execution release-blocking before MIG-003|security, compliance|

### Milestone Dependencies — M4

- M3 tracing, audit visibility, and recovery flows must already be operational.
- Rollout decisions depend on TEST-SEC-001, TEST-PERF-001, TEST-REL-001, and TEST-COV-001 being green.

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1|Required|Delay M2-M4 until INFRA-DB-001 is satisfied; no safe local substitute for production roadmap work|
|Redis 7+|M1|Required|Fail closed on refresh and re-login temporarily; still blocks full FR-AUTH-003 and FR-AUTH-005 readiness|
|Node.js 20 LTS|M1|Required|No fallback; runtime mandate|
|bcryptjs|M1|Required|Alternate bcrypt library only with policy review and benchmark parity|
|jsonwebtoken|M1|Required|Alternate JOSE/JWT implementation only if RS256 + kid behavior remains equivalent|
|SendGrid|M1, M3|Required|Fallback SMTP/API provider with identical reset-email semantics|
|API Gateway|M1, M2, M4|Required|In-app temporary throttling for non-production only; production requires gateway enforcement|
|SEC-POLICY-001|M1|Required|No fallback; authoritative policy dependency|
|INFRA-DB-001|M1|Required|No fallback; storage provisioning dependency|

### Infrastructure Requirements

- PostgreSQL 15+ with migration support, audit-log retention jobs, backups, and connection-pool observability.
- Redis 7+ with namespaced keyspaces for refresh tokens and reset tokens, TTL observability, and capacity alarms.
- Node.js 20 runtime with secret-loading support for RSA keys and SendGrid credentials.
- API gateway with route-level rate limits, TLS 1.3 enforcement, CORS allowlists, and auth middleware attachment.
- Telemetry stack for logs, Prometheus metrics, distributed tracing, dashboards, and alert routing.
- CI/CD support for unit, integration, E2E, performance, security, and coverage gates.
- Feature-flag infrastructure supporting internal-only, percentage-based, and global disable modes.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS allows session hijacking|M2|Medium|High|Access token in memory only; refresh-token revocation; explicit logout; clear on tab close; later security review gate|security, frontend|
|R-002|Brute-force attacks on login endpoint|M2, M4|High|Medium|Gateway rate limits, lockout policy, CAPTCHA contingency, and alerting during rollout|security, backend|
|R-003|Data loss during migration from legacy auth|M1, M4|Low|High|Versioned schema, backups, coexistence bridge, explicit rollback procedure and triggers|platform, backend|
|R-004|Low registration adoption due to poor UX|M2|Medium|Medium|Inline validation, minimal UX friction, usability validation, and funnel observability|product, frontend|
|R-005|Compliance failure from incomplete audit logging|M1, M3, M4|Medium|High|Audit store, 12-month retention execution, completeness validation, and admin query visibility|security, compliance|
|R-006|Email delivery failures blocking password reset|M3|Medium|Low|Observable delivery adapter, support fallback, and explicit reset usability/testing gates|platform, product|
|R-007|Redis unavailability impairs TokenManager|M4|Medium|Low|Fail-closed refresh behavior, alerts, scaling plan, and documented refresh-failure recovery|platform, backend|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Fast login responses|Login response p95|<200ms|TEST-PERF-001 with APM/tracing from NFR-PERF-001 instrumentation|M4|
|Concurrent auth capacity|Concurrent login support|500 requests|k6-based NFR-PERF-002 load validation|M4|
|Reliable service availability|Rolling uptime|99.9%|NFR-REL-001 health monitoring plus TEST-REL-001 failover drill|M4|
|Secure password hashing|PasswordHasher.hash runtime|<500ms at cost 12|TEST-PERF-001 and NFR-SEC-001 policy checks|M4|
|High registration success|Registration success rate|>99%|API telemetry and rollout dashboard monitoring|M4|
|Good onboarding conversion|Registration conversion|>60%|COMP-035 dashboard plus UX validation and production funnel review|M4|
|Healthy engagement|DAU after GA|>1000 within 30 days|Rollout dashboard and auth issuance analytics|M4|
|Sustained sessions|Average session duration|>30 minutes|Refresh analytics from AuthProvider and TokenManager traces|M4|
|Low failed-login rate|Failed login ratio|<5% of attempts|Prometheus metrics and auth-event logs|M4|
|Recoverable accounts|Password reset completion|>80%|TEST-UX-001 and production reset funnel metrics|M3, M4|
|Core code quality|Unit coverage for core auth components|>80%|TEST-COV-001 CI gate|M4|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Session architecture|RS256 access tokens + Redis-backed refresh tokens|Server-side sessions; JWT-only without refresh state|Supports Sam’s programmatic refresh JTBD, horizontal scale, and explicit revocation requirements from FR-AUTH-003|
|Audit retention target|12 months|90 days|PRD legal/compliance intent and SOC2 requirement outweigh the conflicting older TDD note|
|Logout scope|Include API-007 + explicit logout handling in v1.0|Defer logout as implicit client-only behavior|PRD user story explicitly requires secure logout on shared devices; implicit behavior is insufficient|
|Admin visibility scope|Minimal audit-event query API and view|No admin visibility in v1.0; full admin suite|Jordan persona and PRD acceptance criteria require queryable auth logs, but a minimal scope avoids overshooting v1.0|
|Security enforcement order|Policy/storage first, flows second|Build user flows first and retrofit controls later|Architecturally safer because lockout, retention, token, and consent choices shape persistent contracts and rollout risk|
|Rollout strategy|4-week phased rollout with flags and rehearsed rollback|Immediate GA cutover|Risk inventory and migration items require reversible exposure with measurable stop conditions|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|W1|W2|Security and data model foundation complete; feature flags and gateway policies wired|
|M2|3 weeks|W3|W5|Core auth services, login/register/refresh/logout, and session UX operational|
|M3|2 weeks|W6|W7|Password reset, audit visibility, admin query path, and observability complete|
|M4|4 weeks|W8|W11|Testing, phased rollout, rollback readiness, and on-call handoff complete|

**Total estimated duration:** 11 weeks
