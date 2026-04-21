---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
base_variant: "none"
variant_scores: "none"
convergence_score: "none"
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a production-grade user authentication platform in five technical-layer milestones: security and data foundations, core account flows, token lifecycle and recovery, observability and operational hardening, and controlled rollout. The plan preserves every extracted requirement/entity ID, resolves document conflicts explicitly, and adds only the PRD-required gap fills needed to ship a complete v1.0 authentication experience.

**Business Impact:** Unblocks Q2-Q3 personalization work, closes the SOC2 audit-trail gap ahead of Q3, reduces access-related support burden, and creates a stable contract for both end-user and API-consumer authentication.

**Complexity:** MEDIUM (0.65) — multi-surface delivery across backend, frontend, crypto, data, observability, rollout controls, and compliance with several source conflicts that must be resolved consistently.

**Critical path:** PostgreSQL/Redis/SendGrid readiness -> security baseline (`PasswordHasher`, `JwtService`, audit retention decision) -> `AuthService`/`UserRepo` implementation -> core APIs/pages -> `TokenManager`/reset flow/session revocation -> observability and rollback automation -> phased rollout via `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH`.

**Key architectural decisions:**

- Keep stateless auth with 15-minute RS256 access tokens and 7-day refresh tokens backed by Redis revocation state.
- Enforce browser refresh tokens through HttpOnly cookies while allowing request-body refresh for API-consumer use cases.
- Apply PRD precedence for user/compliance outcomes where TDD and PRD conflict, while retaining TDD API shapes when UX goals can be met without contract breakage.

**Open risks requiring resolution before M1:**

- Audit retention conflict must stay fixed at 12 months across schema, storage, validation, and runbooks.
- Lockout policy and role-array bounds must be frozen early because they shape API behavior, JWT size, and test baselines.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation and Security Baseline|Foundation|P0|L|Node.js 20, PostgreSQL 15+, Redis 7+, SEC-POLICY-001|22|High|
|M2|Core Account Flows and UI Integration|Core|P0|L|M1, frontend routing, API gateway policies|13|High|
|M3|Session Lifecycle, Recovery, and Gap Fills|Integration|P0|L|M1-M2, SendGrid, rollout flags|15|High|
|M4|Observability, Reliability, and Operational Hardening|Hardening|P0|XL|M2-M3, monitoring stack, k6, staging|22|High|
|M5|Migration, Rollout, and GA Cutover|Release|P0|L|M3, M4 critical controls, production flags, backup/restore readiness|5|High|

## Dependency Graph

API Gateway(TLS1.3,CORS,rate limits) -> `/v1/auth/*` -> `AuthService` -> {`PasswordHasher`,`UserRepo`,`AuditLogWriter`,`TokenManager`}
`TokenManager` -> {`JwtService`,Redis7,`SessionRevoker`}
`AuthService` -> PostgreSQL15
`ResetEmailDispatcher` -> SendGrid
React App -> `AuthProvider` -> {`LoginPage`,`RegisterPage`,`ProfilePage`} -> Auth APIs
MIG-004(`AUTH_NEW_LOGIN`) -> MIG-001 -> MIG-002 -> MIG-003
MIG-005(`AUTH_TOKEN_REFRESH`) -> `TokenManager`/`AuthProvider` -> GA session persistence

## M1: Foundation and Security Baseline

**Objective:** Establish the secure data, crypto, consent, and persistence baseline that all externally reachable auth features depend on. | **Duration:** Weeks 1-2 (2026-03-30 to 2026-04-14) | **Entry:** PostgreSQL 15+, Redis 7+, Node.js 20 LTS, SEC-POLICY-001, gateway TLS/CORS configuration available. | **Exit:** Core schemas, crypto services, consent/audit foundations, and non-negotiable compliance/security controls are implemented and testable without exposing partial end-user flows.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-SEC-001|Bcrypt cost-12 enforcement|Lock password hashing to bcrypt cost factor 12 through configuration and tests.|PasswordHasher|COMP-007|algo:bcrypt; cost:12; unit-test asserts cost=12; no lower-cost override in prod config|S|P0|
|2|NFR-SEC-002|RS256 signing baseline|Provision RSA signing and verification with quarterly rotation support.|JwtService|COMP-011|alg:RS256; key_size:2048-bit; verify path enabled; rotation:quarterly documented and testable|M|P0|
|3|NFR-COMPLIANCE-002|Registration consent capture|Add GDPR consent capture contract at registration and persist timestamp evidence.|AuthService, UserRepo|COMP-005, COMP-012|consent_required:true; recorded_at:timestamptz; registration blocked without consent; audit event emitted|M|P0|
|4|NFR-COMPLIANCE-003|Password secrecy hygiene|Prevent raw passwords from being stored or logged anywhere in the stack.|AuthService, PasswordHasher|COMP-005, COMP-007|raw_password:persisted=false; raw_password:logged=false; hashing:one-way adaptive; log-redaction verified|S|P0|
|5|NFR-COMPLIANCE-004|Data minimization guardrail|Constrain collected profile data to minimum GDPR set for v1.0.|UserRepo|COMP-012, DM-001|collects:email,hashed_password,display_name only; excludes:extra_PII; schema review approved|S|P0|
|6|COMP-007|PasswordHasher implementation|Implement the bcrypt abstraction used by AuthService and reset flows.|PasswordHasher|NFR-SEC-001, NFR-COMPLIANCE-003|type:backend abstraction; methods:hash(password), verify(password,hash); algo:bcrypt; cost:12; future_migration:preserved|M|P0|
|7|COMP-011|JwtService implementation|Implement JWT signing and verification service called by TokenManager.|JwtService|NFR-SEC-002|type:backend service; methods:sign(payload), verify(token); alg:RS256; key_bits:2048; skew_tolerance:5s; rotation:quarterly|M|P0|
|8|COMP-012|UserRepo implementation|Create PostgreSQL repository for user persistence and lookup operations.|UserRepo|DM-001|type:backend repository; store:PostgreSQL15; methods:create, findByEmail, findById, updateLastLogin, recordConsent; entity:UserProfile|M|P0|
|9|COMP-013|AuditLogWriter implementation|Create structured audit persistence for SOC2 and admin investigations.|AuditLogWriter|NFR-COMPLIANCE-001, OQ-CFLT-001|type:backend service; store:PostgreSQL15; records:user_id,event_type,timestamp,ip,outcome; retention:12 months; queryable:date range+user|M|P0|
|10|DM-001|UserProfile schema|Implement the canonical user profile interface and backing table contract.|UserProfile|COMP-012|id:UUID-PK-NOTNULL; email:unique-indexed-lowercase-NOTNULL; displayName:string-2..100-NOTNULL; createdAt:ISO8601-default-now-NOTNULL; updatedAt:ISO8601-auto-updated-NOTNULL; lastLoginAt:ISO8601-nullable; roles:string[]-default[user]-NOTNULL|M|P0|
|11|DM-001-F01|UserProfile.id field|Create UUID primary-key generation and persistence for user identifiers.|UserProfile|DM-001|field:id; type:UUIDv4 string; constraints:PK,NOTNULL; generation:service-side|S|P0|
|12|DM-001-F02|UserProfile.email field|Implement normalized unique email storage and lookup index.|UserProfile|DM-001|field:email; type:string; constraints:UNIQUE,NOTNULL,indexed; normalization:lowercase|S|P0|
|13|DM-001-F03|UserProfile.displayName field|Persist validated display names for UI presentation.|UserProfile|DM-001|field:displayName; type:string; constraints:NOTNULL,2..100 chars|S|P1|
|14|DM-001-F04|UserProfile.createdAt field|Persist immutable account creation timestamp.|UserProfile|DM-001|field:createdAt; type:ISO8601 string; constraints:NOTNULL,default now()|S|P1|
|15|DM-001-F05|UserProfile.updatedAt field|Persist auto-updated modification timestamp.|UserProfile|DM-001|field:updatedAt; type:ISO8601 string; constraints:NOTNULL,auto-updated on change|S|P1|
|16|DM-001-F06|UserProfile.lastLoginAt field|Persist nullable successful-login timestamp.|UserProfile|DM-001|field:lastLoginAt; type:ISO8601 string; constraints:nullable; updated:on successful login only|S|P1|
|17|DM-001-F07|UserProfile.roles field|Persist downstream authorization roles array with bounded size.|UserProfile|DM-001, OQ-002|field:roles; type:string[]; constraints:NOTNULL,default[user]; max_length:TBD-pending-OQ-002|S|P1|
|18|DM-002|AuthToken contract|Implement the canonical token response contract shared by login and refresh.|AuthToken|COMP-011, COMP-006|accessToken:JWT-NOTNULL-15m-userId+roles; refreshToken:opaque-NOTNULL-unique-7d; expiresIn:number-NOTNULL-900; tokenType:string-NOTNULL-Bearer|M|P0|
|19|DM-002-F01|AuthToken.accessToken field|Define the access token claim and expiry contract.|AuthToken|DM-002|field:accessToken; type:JWT string; constraints:NOTNULL; alg:RS256; payload:user_id,roles; ttl:15 min|S|P0|
|20|DM-002-F02|AuthToken.refreshToken field|Define the opaque refresh token contract and uniqueness semantics.|AuthToken|DM-002|field:refreshToken; type:string; constraints:NOTNULL,unique; storage:hashed in Redis; ttl:7 days|S|P0|
|21|DM-002-F03|AuthToken.expiresIn field|Define constant bearer expiry value exposed to clients.|AuthToken|DM-002|field:expiresIn; type:number; constraints:NOTNULL; value:900|S|P1|
|22|DM-002-F04|AuthToken.tokenType field|Define token type for API consumers and browser clients.|AuthToken|DM-002|field:tokenType; type:string; constraints:NOTNULL; value:Bearer|S|P1|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthService` -> `PasswordHasher`|service dependency|Constructor injection and interface contract|M1|FR-AUTH-001, FR-AUTH-002, FR-AUTH-005|
|`TokenManager` -> `JwtService`|service dependency|Signing/verification adapter contract|M1|FR-AUTH-003, API-004, COMP-004|
|`UserRepo` -> PostgreSQL 15|persistence|Schema migrations and repository methods|M1|API-001, API-002, API-003, audit queries|
|`AuditLogWriter` -> PostgreSQL 15|audit persistence|Append-only auth-event table and retention policy|M1|NFR-COMPLIANCE-001, OPS-007, COMP-010|
|API Gateway -> `/v1/auth/*`|middleware chain|TLS 1.3, rate limits, CORS allowlist|M1|All external auth endpoints|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Cryptographic misconfiguration weakens tokens or hashes|Critical|Medium|Account compromise and failed security review|Pin bcrypt cost 12 and RS256/2048 in code plus configuration tests before any endpoint exposure|auth-team|
|2|Audit-retention mismatch creates compliance failure at launch|High|Medium|SOC2 evidence gap and rework across schema/runbooks|Resolve retention to 12 months in M1 and carry the value verbatim through storage, dashboards, and procedures|auth-team + compliance|
|3|Role-array size ambiguity leaks into JWT payload design|Medium|Medium|Schema churn and oversized tokens later|Keep bounded field definition blocked on OQ-002 before GA-facing authorization data is finalized|auth-team|

### Milestone Dependencies — M1

- PostgreSQL 15+ provisioning with migration permissions.
- Redis 7+ provisioning for later token lifecycle work.
- RSA key material generation and secure secret distribution path.
- API gateway ownership for TLS 1.3, CORS allowlist, and per-route rate limits.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-CFLT-001|Conflict: audit-log retention is 90 days in TDD S7.2/S7.3 and 12 months in PRD Legal & Compliance. Resolution: choose 12 months under PRD precedence for compliance commitments; all roadmap references use 12 months.|Drives schema partitioning, storage sizing, retention jobs, SOC2 evidence scope, OPS-007, and release criteria.|auth-team + compliance|2026-03-31|
|2|OQ-002|What is the maximum allowed `UserProfile` roles array length? Source: TDD S22. Status: open; unresolved bound blocks final JWT payload sizing.|Affects DM-001-F07, token size assumptions, validation rules, and downstream admin-role seeding.|auth-team|2026-04-01|
|3|OQ-PRD-003|Account lockout policy exact threshold (TDD says 5 attempts / 15 min; PRD does not confirm)? Source: extraction/PRD open questions. Resolution: use 5 attempts in 15 minutes for v1.0 because TDD provides the only concrete implementation value and PRD is silent.|Unblocks API-001, FR-AUTH-001, TEST-002, WAF guidance, and user messaging; any later product change becomes a post-v1.0 tuning task.|security|2026-03-31|
|4|OQ-001|Should `AuthService` support API key authentication for service-to-service calls? Source: TDD S22. Resolution: closed for v1.0 as out of scope; defer to v1.1 without creating roadmap deliverables.|Prevents accidental scope creep into non-goal territory while keeping interface abstractions future-compatible.|test-lead|2026-04-15|

## M2: Core Account Flows and UI Integration

**Objective:** Deliver externally consumable registration, login, and profile retrieval flows across backend APIs and primary React pages without exposing incomplete session-management features. | **Duration:** Weeks 3-4 (2026-04-15 to 2026-04-28) | **Entry:** M1 complete; frontend routing scaffold available; gateway policies active; staging environment reachable. | **Exit:** Users can register, log in, and view profile data through the shipped pages and APIs; all core-path unit/integration tests pass; partial features remain protected behind flags where needed.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-001|Login capability|Implement credential login through AuthService and the public login route.|AuthService, LoginPage|COMP-005, API-001, COMP-001, TEST-001, TEST-002|valid creds:200+AuthToken; invalid creds:401 generic; unknown email:401 generic; lockout:5 attempts/15 min->423; no user enumeration|M|P0|
|2|FR-AUTH-002|Registration capability|Implement validated account creation with consent, hashing, and profile persistence.|AuthService, RegisterPage|COMP-005, API-002, COMP-002, TEST-004, NFR-COMPLIANCE-002|valid registration:201+UserProfile; duplicate email:409; weak password:<8/no uppercase/no number->400; bcrypt cost:12; consent timestamp recorded|M|P0|
|3|FR-AUTH-004|Profile retrieval capability|Implement authenticated profile retrieval for signed-in users.|AuthService, ProfilePage|COMP-005, API-003, COMP-003|valid accessToken returns id,email,displayName,createdAt,updatedAt,lastLoginAt,roles; expired/invalid token:401|M|P0|
|4|API-001|POST /auth/login|Expose login endpoint with gateway protections and consistent error envelope.|Auth API|FR-AUTH-001, DM-002|method:POST; path:/v1/auth/login; auth:none; rate_limit:10 req/min/IP; request:{email,password}; 200:AuthToken; 401:generic invalid credentials; 423:account locked; 429:rate limited|M|P0|
|5|API-002|POST /auth/register|Expose registration endpoint with validation, uniqueness, and consent capture.|Auth API|FR-AUTH-002, DM-001, NFR-COMPLIANCE-002|method:POST; path:/v1/auth/register; auth:none; rate_limit:5 req/min/IP; request:{email,password,displayName,consent}; 201:UserProfile; 400:validation; 409:duplicate email|M|P0|
|6|API-003|GET /auth/me|Expose current-user profile endpoint secured by bearer tokens.|Auth API|FR-AUTH-004, DM-001|method:GET; path:/v1/auth/me; auth:Bearer; rate_limit:60 req/min/user; header:Authorization Bearer <jwt>; 200:UserProfile; 401:missing/expired/invalid token|S|P0|
|7|COMP-001|LoginPage|Build the login route and form integration for email/password sign-in.|LoginPage|API-001, COMP-004|type:React page; route:/login; auth:none; props:onSuccess():required, redirectUrl?:string; fields:email,password; calls:POST /auth/login; stores:AuthToken via AuthProvider|M|P0|
|8|COMP-002|RegisterPage|Build the registration route and post-success UX for new users.|RegisterPage|API-002, API-001, COMP-004|type:React page; route:/register; auth:none; props:onSuccess():required, termsUrl:string; fields:email,password,displayName,consent; client_validation:password strength; flow:POST /auth/register then POST /auth/login for immediate UX login|M|P0|
|9|COMP-003|ProfilePage|Build the protected profile page bound to current-user data.|ProfilePage|API-003, COMP-004|type:React page; route:/profile; auth:required; props:none explicit; calls:GET /auth/me; displays:id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|M|P1|
|10|COMP-005|AuthService|Implement the backend facade for registration, login, profile, refresh, and reset orchestration.|AuthService|COMP-007, COMP-011, COMP-012, COMP-013|type:backend facade; methods:login,register,me,refresh,resetRequest,resetConfirm; delegates:PasswordHasher,TokenManager,UserRepo; receives:gateway requests|L|P0|
|11|TEST-001|Valid login unit test|Verify successful login issues tokens after password verification.|AuthService test|FR-AUTH-001, API-001|component:AuthService; verify():called; issueTokens():called; returns:valid AuthToken; status:success path covered|S|P0|
|12|TEST-002|Invalid login unit test|Verify bad credentials fail generically and do not issue tokens.|AuthService test|FR-AUTH-001, API-001|component:AuthService; verify():false path; response:401 generic; tokens:not issued; lockout counter increments|S|P0|
|13|TEST-004|Registration integration test|Verify registration writes through hashing and persistence layers.|Integration test|FR-AUTH-002, API-002, COMP-012|scope:AuthService+PostgreSQL; flow:API->PasswordHasher->DB insert; result:UserProfile persisted; duplicate email rejected|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`RegisterPage` -> `API-002` -> `API-001`|frontend orchestration|Sequential submit then immediate-login chain|M2|Alex first-time signup journey|
|`LoginPage` -> `AuthProvider`|context wiring|Token state setter and redirect callback|M2|Public routes and protected-route bootstrap|
|`ProfilePage` -> `API-003`|protected API binding|Bearer token injection and 401 handling|M2|Authenticated users|
|`AuthService` -> `UserRepo`|repository dependency|Email uniqueness, profile persistence, profile lookup|M2|Login, register, me|
|Gateway rate limits -> auth endpoints|middleware registry|Per-route policies for login/register/me|M2|API-001, API-002, API-003|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Poor registration UX suppresses adoption|High|Medium|Missed >60% conversion target and increased support friction|Use inline validation, immediate-login UX chaining, and generic but actionable duplicate-email handling on RegisterPage|frontend-team + auth-team|
|2|Login responses leak identity details|High|Medium|Enumeration risk and security findings|Keep 401 messaging generic for wrong password and unknown email; review UI copy and error envelope together|auth-team|
|3|Profile route exposes stale or partial data|Medium|Low|User trust erosion and downstream personalization issues|Bind ProfilePage only after API-003 contract is stable and always fetch from current token-backed identity|frontend-team|

### Milestone Dependencies — M2

- M1 schema and service contracts completed and reviewed.
- Frontend router and application shell ready for AuthProvider wrapping.
- Staging environment accessible for API and UI integration.
- Gateway route mapping for `/v1/auth/login`, `/v1/auth/register`, and `/v1/auth/me` deployed.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-CFLT-002|Potential source conflict: PRD user story says successful registration logs the user in immediately, while TDD API-002 returns `UserProfile`. Resolution: keep API-002 body as `UserProfile` and satisfy immediate-login UX by chaining LoginPage/AuthProvider login after successful registration.|Preserves TDD endpoint contract while meeting the PRD journey outcome; affects COMP-002, conversion analytics, and onboarding flow tests.|product-team + auth-team|2026-04-16|

## M3: Session Lifecycle, Recovery, and Gap Fills

**Objective:** Complete the session lifecycle, password-reset recovery, logout/session revocation, and missing PRD/TDD end-to-end behaviors required for a coherent v1.0 auth product. | **Duration:** Weeks 5-6 (2026-04-29 to 2026-05-12) | **Entry:** M2 complete; Redis connectivity stable; SendGrid credentials available; feature flags created in non-prod. | **Exit:** Refresh, reset, logout, and session invalidation flows operate end-to-end; PRD user-story gaps are covered without violating v1.0 non-goals.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-AUTH-003|Token issuance and refresh capability|Implement access/refresh token lifecycle with silent refresh semantics and revocation.|TokenManager, AuthProvider|COMP-006, API-004, COMP-004, TEST-003, TEST-005|login returns access:15 min + refresh:7 day; POST /auth/refresh valid token->new pair; expired/revoked refresh:401; old refresh revoked on use|L|P0|
|2|FR-AUTH-005|Password reset capability|Implement request and confirmation flow with single-use reset tokens and session invalidation.|AuthService, ResetEmailDispatcher|API-005, API-006, COMP-005|reset-request sends email for valid address; reset-confirm validates token and updates hash; token ttl:1 hour; used token:not reusable|L|P0|
|3|API-004|POST /auth/refresh|Expose refresh endpoint for browser and API-consumer session continuation.|Auth API|FR-AUTH-003, DM-002|method:POST; path:/v1/auth/refresh; auth:none; rate_limit:30 req/min/user; request:{refreshToken}; 200:new AuthToken pair; 401:expired/revoked token|M|P0|
|4|API-005|POST /auth/reset-request|Expose enumeration-safe password reset initiation endpoint.|Auth API|FR-AUTH-005, OQ-PRD-001|method:POST; path:/v1/auth/reset-request; auth:none; rate_limit:TBD-pending-policy; request:{email}; response:generic confirmation; behavior:SendGrid email with 1-hour TTL token|M|P0|
|5|API-006|POST /auth/reset-confirm|Expose reset confirmation endpoint with password-policy enforcement and session invalidation.|Auth API|FR-AUTH-005, API-005|method:POST; path:/v1/auth/reset-confirm; auth:none; request:{resetToken,newPassword}; 200:password updated+all sessions invalidated; 401:expired/used token; 400:password policy failed|M|P0|
|6|COMP-004|AuthProvider|Implement client auth context, token state, silent refresh, and redirect handling.|AuthProvider|API-001, API-003, API-004, MIG-005|type:React context provider; props:children:ReactNode; stores:accessToken in-memory,current UserProfile; refresh:HttpOnly cookie/browser + request-body/API consumer; intercepts:401; redirects:unauthenticated to LoginPage|L|P0|
|7|COMP-006|TokenManager|Implement token issue/refresh/revoke logic on top of JwtService and Redis.|TokenManager|COMP-011, DM-002, API-004|type:backend service; methods:issueTokens, refresh, revoke, revokeAllForUser; wraps:JwtService; stores:hashed refresh tokens in Redis 7-day TTL; distinguishes:expired vs revoked|L|P0|
|8|COMP-014|ResetEmailDispatcher|Implement SendGrid-backed password reset delivery path.|ResetEmailDispatcher|API-005|type:backend email component; provider:SendGrid; payload:reset link/token; delivery target:<60 seconds; enumeration-safe response decoupled from mail status|M|P0|
|9|COMP-015|LogoutHandler|Add explicit logout/session termination behavior required by PRD scope.|LogoutHandler|COMP-006, COMP-004|type:backend/frontend pair; action:log out; effect:end session immediately; revokes current refresh token; clears in-memory access token; redirects:landing page|M|P1|
|10|TEST-003|Refresh unit test|Verify valid refresh exchanges and revokes old token pair.|TokenManager test|FR-AUTH-003, API-004|component:TokenManager; valid refresh accepted; old token revoked; new AuthToken pair issued via JwtService|S|P0|
|11|TEST-005|Expired refresh integration test|Verify Redis TTL expiry rejects stale refresh tokens.|Integration test|FR-AUTH-003, API-004, COMP-006|scope:TokenManager+Redis; expired token path returns 401; no new token pair issued|S|P0|
|12|TEST-006|Register-login-profile E2E test|Verify end-user golden path from registration through authenticated profile.|E2E test|FR-AUTH-001, FR-AUTH-002, FR-AUTH-004, COMP-001, COMP-002, COMP-003, COMP-004|flow:RegisterPage->LoginPage/Profile bootstrap->ProfilePage; AuthProvider holds session; displayed profile matches registration data|M|P0|
|13|COMP-016|ResetRequestPage|Add the forgot-password initiation UI implied by the PRD journey.|ResetRequestPage|API-005|type:React page; route:/forgot-password; auth:none; fields:email; response:generic confirmation for registered/unregistered email|M|P1|
|14|COMP-017|ResetConfirmPage|Add the reset-confirmation UI implied by the PRD journey.|ResetConfirmPage|API-006|type:React page; route:/reset-password; auth:none; fields:resetToken,newPassword; expired token shows retry path; success redirects:login|M|P1|
|15|API-007|POST /auth/logout|Add logout endpoint required by PRD in-scope scope definition and user story coverage.|Auth API|COMP-015|method:POST; path:/v1/auth/logout; auth:Bearer or refresh-context; request:current session token context; 200:session ended; effect:refresh token revoked, client instructed to clear access token|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthProvider` -> `API-004`|silent-refresh binding|401 interceptor and refresh retry path|M3|ProfilePage, protected routes, Alex returning-user journey|
|`TokenManager` -> Redis 7|cache/revocation|Hashed refresh token storage with 7-day TTL and rotation-on-refresh|M3|FR-AUTH-003, API-007|
|`ResetEmailDispatcher` -> SendGrid|external SaaS integration|Password reset token email dispatch|M3|API-005, password-reset journey|
|`ResetConfirmPage` -> `API-006`|frontend binding|Token + new-password submission|M3|Alex password recovery journey|
|`LogoutHandler` -> `AuthProvider` + `API-007`|session-termination wiring|Client clear-state plus server revocation|M3|Shared-device logout user story|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Refresh-token theft extends compromised sessions|Critical|Medium|Session hijack across devices|Store browser refresh token in HttpOnly cookie, hash at rest in Redis, rotate on every refresh, and revoke all sessions on password reset|auth-team|
|2|Email delivery failures block account recovery|High|Medium|Users locked out and support burden spikes|Instrument SendGrid delivery, keep reset-request response generic, and publish fallback support path in runbook|auth-team + platform-team|
|3|Missing logout semantics undermine shared-device safety|Medium|Medium|Users remain authenticated after intended sign-out|Add explicit logout handler and endpoint even though TDD omitted it, because PRD marks logout in scope|auth-team|

### Milestone Dependencies — M3

- Redis 7+ availability with production-like TTL behavior.
- SendGrid credentials and tested sender configuration.
- Feature flags `AUTH_TOKEN_REFRESH` and `AUTH_NEW_LOGIN` available in lower environments.
- Frontend route support for reset and logout flows.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should password reset emails be sent synchronously or asynchronously? Source: PRD/TDD open questions. Resolution: choose asynchronous dispatch with durable job acknowledgement while preserving immediate generic API response.|Affects API-005 latency, queueing design, supportability, and reset-email SLO tracking.|Engineering|2026-04-30|
|2|OQ-PRD-002|Maximum number of refresh tokens per user across devices? Source: PRD open questions. Status: open; roadmap keeps multi-device support but caps enforcement as TBD-pending-OQ-PRD-002.|Affects Redis memory sizing, TokenManager eviction policy, logout-all semantics, and OPS-006 calculations.|Product|2026-05-02|
|3|OQ-PRD-004|Support "remember me" to extend session duration? Source: PRD open questions. Resolution: closed for v1.0 as out of scope because session duration is fixed by TDD/PRD 7-day refresh window and no source commits a separate remember-me feature.|Prevents silent scope expansion into alternate session policies while preserving current success metrics.|Product|2026-05-02|
|4|OQ-JTBD-001|PRD Jordan-admin JTBD requires viewing auth event logs and locking compromised accounts; this roadmap covers queryable logs via COMP-013/COMP-010 but lock/unlock UI is not in TDD and is out of scope for v1.0. Resolution: logs ship in v1.0; admin lock/unlock capability deferred and PRD/TDD must be updated before implementation.|Clarifies that incident investigation is supported, but admin account-lock controls are not delivered in this roadmap.|product-team + auth-team|2026-05-05|

## M4: Observability, Reliability, and Operational Hardening

**Objective:** Add measurable instrumentation, testing, capacity controls, runbooks, and compliance-grade operational behaviors so the service can safely enter phased rollout. | **Duration:** Weeks 7-8 (2026-05-13 to 2026-05-26) | **Entry:** M3 complete; staging traffic available; monitoring stack and load-test environment accessible. | **Exit:** Numeric targets are instrumented and alertable, operational procedures are executable, and release-readiness evidence exists for performance, reliability, security, and compliance.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-PERF-001|Auth endpoint latency budget|Instrument and enforce p95 latency budgets across auth endpoints.|Observability stack|OPS-007, COMP-018|all auth endpoints traced; p95 target:<200ms recorded; alert threshold configured; dashboards per endpoint available|M|P0|
|2|NFR-PERF-002|500-concurrent login support|Validate and tune service for 500 concurrent login requests.|Performance test stack|API-001, OPS-004, OPS-005, OPS-006|k6 scenario:500 concurrent login requests; result within target; bottlenecks documented and remediated|L|P0|
|3|NFR-REL-001|Availability objective instrumentation|Implement uptime measurement and health signaling for 99.9% target.|Health and monitoring|COMP-018|health check endpoint present; 30-day rolling uptime tracked; alerting wired for availability regression|M|P0|
|4|NFR-COMPLIANCE-001|SOC2 audit logging compliance|Complete queryable audit logging with retention and validation evidence.|AuditLogWriter, Admin query layer|COMP-013, COMP-010|events:user id,timestamp,IP,outcome logged; retention:12 months; queryable by date range+user; QA validation against SOC2 controls|L|P0|
|5|COMP-010|AuthEventQuery service|Provide query path for admins/compliance to inspect auth events without adding RBAC enforcement scope.|Audit query service|COMP-013, OQ-JTBD-001|type:backend query service; filters:user,date range,event type,outcome; source:audit log; no RBAC enforcement beyond existing admin boundary|M|P1|
|6|COMP-018|MetricsEmitter|Implement Prometheus counters/histograms for auth events and latency budgets.|Metrics|COMP-005, COMP-006|metrics:auth_login_total,auth_login_duration_seconds,auth_token_refresh_total,auth_registration_total; labels:outcome where appropriate; scrape-ready|M|P0|
|7|COMP-019|TraceInstrumentation|Implement OpenTelemetry spans across auth call chains.|Tracing|COMP-005, COMP-006, COMP-011, COMP-007|spans:AuthService->PasswordHasher/TokenManager->JwtService; context propagation works; sampling configured|M|P0|
|8|COMP-020|StructuredLogPolicy|Implement structured application logging with token/password redaction.|Logging|COMP-005, COMP-006|events:login success/failure,registration,refresh,password reset; excludes:passwords,tokens; output:structured JSON/stdout|M|P0|
|9|COMP-021|HealthCheckEndpoint|Expose readiness/liveness endpoint for availability monitoring.|Auth API|NFR-REL-001|endpoint:/health or equivalent; checks:app readiness and dependencies policy; consumed by uptime monitor and K8s|S|P0|
|10|OPS-001|AuthService-down runbook|Document and validate incident procedure for total auth outage.|Runbook|COMP-021, COMP-020, COMP-019|scenario:5xx all /auth/*; diagnosis:pods,PostgreSQL,init logs; resolution:restart/failover/re-login guidance; escalation:15 min to platform-team|M|P0|
|11|OPS-002|Token-refresh-failure runbook|Document and validate incident procedure for refresh degradation.|Runbook|COMP-018, COMP-019, MIG-005|scenario:unexpected logouts/redirect loop; diagnosis:Redis,signing keys,flag state; resolution:scale Redis/remount secrets/enable flag|M|P0|
|12|OPS-003|On-call readiness|Stand up post-GA on-call expectations and escalation chain.|Operations|OPS-001, OPS-002|P1 ack<=15 min; auth-team 24/7 first 2 weeks post-GA; tooling:K8s dashboards,Grafana,Redis CLI,PostgreSQL admin; escalation chain documented|S|P0|
|13|OPS-004|AuthService pod capacity plan|Define and test horizontal scaling thresholds for service pods.|Capacity|NFR-PERF-002|current:3 replicas; expected:500 concurrent users; HPA target:scale to 10 at CPU>70%|M|P0|
|14|OPS-005|PostgreSQL connection capacity plan|Define DB connection pool scaling criteria.|Capacity|NFR-PERF-002|current pool:100; avg concurrent:50; scale to:200 if wait time>50ms|S|P1|
|15|OPS-006|Redis memory capacity plan|Define refresh-token cache sizing and scaling criteria.|Capacity|COMP-006, OQ-PRD-002|current:1GB; expected:~100K refresh tokens (~50MB); scale to:2GB if >70% utilized|S|P1|
|16|OPS-007|Observability package|Assemble the required logs, metrics, traces, alerts, and audit-query behavior into one operational capability.|Observability stack|COMP-018, COMP-019, COMP-020, COMP-013, COMP-010|logs:login success/failure,registration,refresh,password reset; metrics:auth_login_total,auth_login_duration_seconds,auth_token_refresh_total,auth_registration_total; traces:end-to-end spans; alerts:login failure >20%/5m,p95 latency >500ms,Redis failures; audit query:user+date range|L|P0|
|17|COMP-022|Registration funnel analytics|Instrument registration conversion target from register start to confirmed account.|Product analytics|COMP-002|metric:registration conversion; target:>60%; funnel:RegisterPage view->submit->confirmed account; dashboard available|M|P1|
|18|COMP-023|Session-duration analytics|Instrument average session duration and DAAU targets from token activity.|Product analytics|COMP-004, API-004|metrics:average session duration >30 minutes; daily active authenticated users >1000 within 30 days GA; source:token issuance/refresh analytics|M|P1|
|19|COMP-024|Failed-login-rate analytics|Instrument failed-login ratio target for UX/security monitoring.|Product analytics|API-001, COMP-018|metric:failed login rate; target:<5% of attempts; source:auth event log analysis; alert/report available|S|P1|
|20|COMP-025|Password-reset funnel analytics|Instrument reset completion target and email-delivery timing.|Product analytics|API-005, API-006, COMP-014|metric:password reset completion >80%; delivery target:<60s email send; funnel:requested->email sent->password changed|M|P1|
|21|COMP-026|RollbackAutomation|Implement automated rollback triggers from rollout criteria without human approval gates.|Release operations|MIG-001, MIG-002, MIG-003|triggers:auto on p95>1000ms for >5 min; auto on error rate>5% for >2 min; auto on Redis failures>10/min; auto on any UserProfile data loss/corruption signal; action:disable AUTH_NEW_LOGIN and start checklist|L|P0|
|22|TEST-007|Performance and resilience test suite|Add k6 and staging validation suite for latency, concurrency, and rollback thresholds.|Quality suite|NFR-PERF-001, NFR-PERF-002, COMP-026|covers:<200ms p95, 500 concurrent login, rollback triggers, dashboard verification; evidence captured for release review|L|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthService`/`TokenManager` -> Prometheus|metrics pipeline|Counters and histograms exported for scraping|M4|SRE dashboards, alerts, release review|
|`AuthService` -> OpenTelemetry collector|tracing pipeline|Span emission and context propagation|M4|Performance diagnosis, incident response|
|Structured logs -> incident channel/runbooks|logging pipeline|JSON logs with redaction and searchable fields|M4|OPS-001, OPS-002, security review|
|Audit log store -> `AuthEventQuery`|query service|Date-range and user filters|M4|Jordan admin investigations, compliance evidence|
|RollbackAutomation -> feature flag system|automation hook|Disable `AUTH_NEW_LOGIN` on trigger breach|M4|MIG-001, MIG-002, MIG-003|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Numeric targets exist on paper but not in instrumentation|High|Medium|No objective release gate and blind production rollout|Create dedicated emitter rows plus alerts for each named latency, failure, adoption, and reset metric|auth-team + platform-team|
|2|Rollback remains manual despite automatic source contract|Critical|Low|Slow incident response during rollout breach|Ship automated trigger wiring in M4 and rehearse it in staging before traffic exposure|platform-team|
|3|Audit logging is complete but not queryable|High|Medium|Jordan/admin JTBD and SOC2 evidence not actually satisfied|Add AuthEventQuery and validation paths rather than only raw append logs|auth-team|

### Milestone Dependencies — M4

- Monitoring stack with Prometheus, tracing backend, and alerting channels.
- k6 or equivalent load-testing infrastructure.
- Staging environment seeded with realistic traffic and test users.
- Feature-flag platform APIs accessible for rollback automation.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-RESET-RL-001|Reset-request rate limit is not explicitly specified in the TDD/extraction. Resolution: set an initial gateway policy of 5 req/min/IP, matching registration, and validate during beta; update source docs post-review.|Affects API-005 abuse resistance, UX for repeated reset requests, and WAF alignment.|security + auth-team|2026-05-06|

## M5: Migration, Rollout, and GA Cutover

**Objective:** Execute the phased migration plan, validate automated rollback readiness, and complete the GA cutover without exceeding the TDD’s committed schedule. | **Duration:** Weeks 9-10 (2026-05-27 to 2026-06-09) | **Entry:** M4 release evidence approved; rollback automation tested; runbooks published; production dependencies healthy. | **Exit:** Internal alpha, beta, and GA phases complete; legacy auth is deprecated; required flags cleaned up on schedule or assigned post-GA cleanup ownership.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-001|Phase 1 internal alpha|Deploy new auth stack to staging/internal alpha with manual validation gate.|Release plan|M2, M3, M4, MIG-004|duration:1 week; env:staging; actors:auth-team+QA; flags:AUTH_NEW_LOGIN on for internal only; exit:FR-AUTH-001..005 manual pass; zero P0/P1 bugs|M|P0|
|2|MIG-002|Phase 2 beta rollout|Expose auth flows to 10% traffic with heightened monitoring and rollback automation.|Release plan|MIG-001, COMP-026, MIG-004, MIG-005|duration:2 weeks; traffic:10%; monitor:latency,error,Redis usage; exit:p95<200ms; error rate<0.1%; no Redis connection failures|M|P0|
|3|MIG-003|Phase 3 GA rollout|Cut over 100% of users to the new service and deprecate legacy auth.|Release plan|MIG-002, COMP-026|duration:1 week; traffic:100%; AUTH_NEW_LOGIN removed; AUTH_TOKEN_REFRESH enabled; exit:99.9% uptime over 7 days; dashboards green|M|P0|
|4|MIG-004|Feature flag AUTH_NEW_LOGIN|Use the main rollout gate for new login page and login endpoint exposure.|Feature flags|M2, COMP-026|purpose:gates LoginPage+AuthService login; default:OFF; used in phases 1-2; cleanup:after Phase 3 GA|S|P0|
|5|MIG-005|Feature flag AUTH_TOKEN_REFRESH|Use the session-persistence gate for refresh-token flow rollout and cleanup.|Feature flags|M3, COMP-026|purpose:gates TokenManager refresh flow; default:OFF; enabled by GA; cleanup:Phase 3 + 2 weeks owner auth-team|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AUTH_NEW_LOGIN` -> gateway/app routing|feature flag|Traffic exposure gate for new auth entrypoints|M5|MIG-001, MIG-002, MIG-003|
|`AUTH_TOKEN_REFRESH` -> `AuthProvider`/`TokenManager`|feature flag|Refresh-flow activation and cleanup scheduling|M5|Returning-user sessions at GA|
|RollbackAutomation -> alpha/beta rollout|automation|Terminal-condition rollback execution|M5|Release managers, on-call|
|Backup/restore -> `UserProfile` data|data procedure|Pre-phase backups and corruption recovery path|M5|Migration safety and incident response|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Legacy cutover causes user-visible auth outage|Critical|Medium|Failed launch and trust damage|Use staged flags, objective exits, and automated rollback criteria before each traffic increase|auth-team + platform-team|
|2|Data corruption during rollout persists unnoticed|High|Low|User lockouts and permanent account damage|Take full backups before each phase and auto-trigger rollback on corruption signals|platform-team|
|3|Flag cleanup is forgotten post-GA|Medium|Medium|Long-lived complexity and hidden routing paths|Assign explicit cleanup owner/date and include cleanup in GA checklist|auth-team|

### Milestone Dependencies — M5

- Production-grade flag management and change windows.
- Backup/restore validation completed against production-like data.
- On-call staffing active for first two weeks post-GA.
- Go/no-go sign-off from test-lead and eng-manager.

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1-M5|Required|Block rollout; no safe fallback for persistent identity storage|
|Redis 7+|M3-M5|Required|Disable refresh flow and force re-login; do not serve stale refresh state|
|Node.js 20 LTS|M1-M5|Required|Upgrade target runtime before implementation starts|
|bcryptjs|M1-M4|Required|No alternate library in v1.0; PasswordHasher abstraction keeps future migration path|
|jsonwebtoken|M1-M4|Required|No alternate library in v1.0; hold release if signing/verification is unstable|
|SendGrid API|M3-M5|Required|Fallback support channel only; password-reset self-service remains degraded until restored|
|Frontend routing framework|M2-M3|Required|Temporary backend-only validation possible, but user journeys cannot ship|
|SEC-POLICY-001|M1-M4|Required|Security review cannot close without policy alignment|

### Infrastructure Requirements

- Kubernetes deployment target with HPA support for 3 -> 10 `AuthService` replicas.
- Secret-management path for RSA private/public keys and SendGrid credentials.
- Monitoring stack with Prometheus, tracing backend, and alert delivery.
- Staging environment with PostgreSQL, Redis, seeded accounts, and production-like network controls.
- Load-test environment capable of 500 concurrent login attempts.
- Feature-flag service supporting automated disable operations.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-001|Token theft via XSS or stolen client state enables session hijacking|M3,M4,M5|Medium|High|Access token in memory only; HttpOnly cookie for browser refresh token; rotate refresh tokens; revoke on reset/logout|auth-team|
|R-002|Brute-force attacks on login endpoint|M2,M4,M5|High|Medium|Gateway rate limiting 10 req/min/IP; lockout after 5 failures/15 min; WAF/CAPTCHA escalation path|auth-team + platform-team|
|R-003|Data loss or corruption during migration|M5|Low|High|Parallel phases, pre-phase backups, idempotent data handling, automated rollback triggers|platform-team|
|R-PRD-001|Low registration adoption due to poor UX|M2,M4|Medium|High|Inline validation, immediate-login onboarding, funnel analytics, usability iteration before GA|frontend-team + product-team|
|R-PRD-002|Security breach from implementation flaws|M1,M3,M4,M5|Low|Critical|Dedicated security review, crypto tests, penetration testing, rollback readiness|security + auth-team|
|R-PRD-003|Compliance failure from incomplete SOC2 audit logging|M1,M4,M5|Medium|High|Implement queryable audit logs early, validate controls in QA, enforce 12-month retention|auth-team + compliance|
|R-PRD-004|Email delivery failures block password reset|M3,M4,M5|Low|Medium|SendGrid monitoring, async dispatch, delivery metrics, fallback support path|auth-team|
|R-M1-001|Cryptographic misconfiguration weakens tokens or hashes|M1|Medium|Critical|Pin bcrypt cost 12 and RS256/2048 in code plus configuration tests before any endpoint exposure|auth-team|
|R-M1-002|Audit-retention mismatch creates compliance failure at launch|M1|Medium|High|Resolve retention to 12 months in M1 and carry the value verbatim through storage, dashboards, and procedures|auth-team + compliance|
|R-M1-003|Role-array size ambiguity leaks into JWT payload design|M1|Medium|Medium|Keep bounded field definition blocked on OQ-002 before GA-facing authorization data is finalized|auth-team|
|R-M2-001|Poor registration UX suppresses adoption|M2|Medium|High|Use inline validation, immediate-login UX chaining, and generic but actionable duplicate-email handling on RegisterPage|frontend-team + auth-team|
|R-M2-002|Login responses leak identity details|M2|Medium|High|Keep 401 messaging generic for wrong password and unknown email; review UI copy and error envelope together|auth-team|
|R-M2-003|Profile route exposes stale or partial data|M2|Low|Medium|Bind ProfilePage only after API-003 contract is stable and always fetch from current token-backed identity|frontend-team|
|R-M3-001|Refresh-token theft extends compromised sessions|M3|Medium|Critical|Store browser refresh token in HttpOnly cookie, hash at rest in Redis, rotate on every refresh, and revoke all sessions on password reset|auth-team|
|R-M3-002|Email delivery failures block account recovery|M3|Medium|High|Instrument SendGrid delivery, keep reset-request response generic, and publish fallback support path in runbook|auth-team + platform-team|
|R-M3-003|Missing logout semantics undermine shared-device safety|M3|Medium|Medium|Add explicit logout handler and endpoint even though TDD omitted it, because PRD marks logout in scope|auth-team|
|R-M4-001|Numeric targets exist on paper but not in instrumentation|M4|Medium|High|Create dedicated emitter rows plus alerts for each named latency, failure, adoption, and reset metric|auth-team + platform-team|
|R-M4-002|Rollback remains manual despite automatic source contract|M4|Low|Critical|Ship automated trigger wiring in M4 and rehearse it in staging before traffic exposure|platform-team|
|R-M4-003|Audit logging is complete but not queryable|M4|Medium|High|Add AuthEventQuery and validation paths rather than only raw append logs|auth-team|
|R-M5-001|Legacy cutover causes user-visible auth outage|M5|Medium|Critical|Use staged flags, objective exits, and automated rollback criteria before each traffic increase|auth-team + platform-team|
|R-M5-002|Data corruption during rollout persists unnoticed|M5|Low|High|Take full backups before each phase and auto-trigger rollback on corruption signals|platform-team|
|R-M5-003|Flag cleanup is forgotten post-GA|M5|Medium|Medium|Assign explicit cleanup owner/date and include cleanup in GA checklist|auth-team|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Fast login|Login response time (p95)|< 200ms|APM + histogram from `auth_login_duration_seconds`; k6 and staging validation|M4-M5|
|Concurrent authentication|Concurrent login capacity|500 concurrent login requests|k6 load test with release evidence pack|M4|
|Reliable service|Availability|99.9% uptime over 30-day windows|Health-check uptime monitor and post-GA SLO report|M4-M5|
|Secure hashing|Password hash time|< 500ms|Benchmark `PasswordHasher.hash()` at cost 12 under staging load|M4|
|Fast refresh|Token refresh latency (p95)|< 100ms|APM trace on `TokenManager.refresh()` plus endpoint histogram|M4|
|Frictionless onboarding|Registration success rate|> 99%|Registration funnel analytics and integration-test pass rate|M4-M5|
|Conversion target|User registration conversion|> 60%|Register funnel from page view to confirmed account|M4-M5|
|Adoption target|Daily active authenticated users|> 1000 within 30 days of GA|Token issuance analytics report|M4-M5|
|Session quality|Average session duration|> 30 minutes|Token refresh event analytics after beta/GA|M4-M5|
|Authentication quality|Failed login rate|< 5% of attempts|Auth event log analysis and dashboarding|M4-M5|
|Recovery quality|Password reset completion|> 80%|Reset funnel from request to successful password change|M4-M5|
|Compliance evidence|Audit retention and fields|12-month retention; user ID, timestamp, IP, outcome present|Query validation against audit log and retention-policy checks|M4-M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Session mechanism|JWT access tokens + Redis-backed refresh revocation|Server-side sessions; access-token-only|Matches stateless scaling constraint while preserving revocation and silent refresh support.|
|Password hashing|bcrypt cost factor 12 behind `PasswordHasher`|argon2id; scrypt|Source mandates bcrypt 12; abstraction preserves future migration path without violating v1.0.|
|Token signing|RS256 with 2048-bit RSA and quarterly rotation|HS256 shared secret|Asymmetric signing aligns with security policy and safer verification distribution.|
|Audit retention conflict|12 months (OQ-CFLT-001)|90 days from TDD|PRD compliance commitment takes precedence; all downstream roadmap references use 12 months consistently.|
|Registration success behavior|Immediate-login UX via chained login after `UserProfile` response (OQ-CFLT-002)|Change API-002 to return tokens directly|Meets PRD onboarding goal without breaking TDD API contract.|
|Password reset dispatch|Asynchronous email send with immediate generic API response|Synchronous request/response mail send|Protects API latency and resiliency while preserving enumeration-safe UX and delivery observability.|
|Logout scope|Ship explicit logout endpoint/UI in v1.0|Omit logout because TDD omitted endpoint|PRD marks logout in scope; adding the missing endpoint closes the user-story gap without violating non-goals.|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|2026-03-30 (Week 1)|2026-04-14 (Week 2)|Maps to TDD M1 Core `AuthService`; security baseline, schemas, crypto services, consent/audit foundation|
|M2|2 weeks|2026-04-15 (Week 3)|2026-04-28 (Week 4)|Maps to TDD M1/M2 overlap; login/register/me APIs and pages, AuthService core, initial tests|
|M3|2 weeks|2026-04-29 (Week 5)|2026-05-12 (Week 6)|Maps to TDD M2/M3 overlap; refresh, reset, logout, reset pages, end-to-end session lifecycle|
|M4|2 weeks|2026-05-13 (Week 7)|2026-05-26 (Week 8)|Maps to TDD M4 Frontend Integration and hardening; observability, runbooks, capacity plans, automated rollback, release evidence|
|M5|2 weeks|2026-05-27 (Week 9)|2026-06-09 (Week 10)|Maps to TDD M5 GA Release; alpha, beta, GA cutover, flag cleanup commitments, launch sign-off|

**Total estimated duration:** 10 weeks (2026-03-30 to 2026-06-09)

