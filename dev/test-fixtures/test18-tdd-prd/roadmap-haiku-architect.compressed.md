---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
base_variant: "none"
variant_scores: "none"
convergence_score: 1.0
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers the platform’s foundational authentication layer in five technical milestones over 14 weeks, sequencing schema and service foundations before external contracts, user-facing flows, validation, and phased rollout. The plan prioritizes the critical path to unlock Q2 2026 personalization work, satisfy Q3 2026 SOC2 audit readiness, and deliver self-service account recovery without introducing out-of-scope OAuth, MFA, or RBAC work.

**Business Impact:** Unblocks the personalization roadmap tied to approximately $2.4M projected annual revenue, reduces access-related support burden, and establishes the audit trail required for enterprise compliance.

**Complexity:** HIGH (0.72) — complexity is driven by cross-stack orchestration across PostgreSQL, Redis, SendGrid, API Gateway, Kubernetes, frontend auth state, RS256 key management, and phased migration under security and compliance constraints.

**Critical path:** M1 data and crypto foundations → M2 auth domain services and core auth APIs → M3 frontend/session/profile/reset experience → M4 compliance, performance, and test validation → M5 phased rollout and operational readiness.

**Key architectural decisions:**

- Use stateless RS256-signed access tokens with Redis-backed refresh-token revocation to satisfy concurrency, horizontal scaling, and programmatic refresh requirements.
- Keep `AuthService` as the orchestration facade over `UserRepo`, `PasswordHasher`, `JwtService`, and `TokenManager` so validation, audit logging, and policy enforcement stay centralized.
- Use phased rollout behind `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` feature flags with legacy fallback to reduce migration and availability risk.

**Open risks requiring resolution before M1:**

- `OQ-002` must be resolved before finalizing the `UserProfile.roles` schema and validation limits.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation and Core Services|FEATURE|P0|3w|—|17|High|
|M2|External Contracts and Backend Flows|FEATURE|P0|2w|M1|14|High|
|M3|Frontend Experience and Session UX|FEATURE|P1|2w|M2|12|Medium|
|M4|Validation, Compliance, and Non-Functional Assurance|SECURITY|P0|3w|M2, M3|14|High|
|M5|Rollout, Migration, and Operations|MIGRATION|P0|4w|M4|10|High|

## Dependency Graph

M1 → M2 → M3 → M4 → M5

Parallel paths after M2: frontend UX hardening in M3 can proceed alongside portions of M4 test harness and observability preparation once contracts are frozen.

## M1: Foundation and Core Services

**Objective:** Establish persistent identity data, token primitives, backend orchestration components, and the minimum infrastructure required for secure auth flows. | **Duration:** Weeks 1-3 | **Entry:** PRD/TDD scope frozen; infrastructure owners assigned; `OQ-002` accepted for initial schema bound | **Exit:** Core services issue and validate tokens, persist users, enforce password policy, and support login/registration/profile/reset through internal service interfaces.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile persistence model|Define and persist the canonical authenticated-user model in PostgreSQL for all downstream auth flows.|UserRepo, PostgreSQL|OQ-002|id:UUID-PK; email:unique-idx-lowercase-not-null; displayName:varchar-2..100-not-null; createdAt:timestamptz-default-now; updatedAt:timestamptz-auto-updated; lastLoginAt:timestamptz-nullable; roles:text[]-default-user; schema deployed to PG15|M|P0|
|2|DM-002|AuthToken contract model|Define the canonical token pair returned by login and refresh operations.|TokenManager, JwtService|COMP-006|accessToken:jwt-rs256-not-null; refreshToken:opaque-unique-not-null; expiresIn:number-900; tokenType:string-Bearer; contract shared by login and refresh paths|S|P0|
|3|COMP-005|AuthService facade|Implement the central backend orchestrator for login, registration, profile retrieval, and password reset workflows.|AuthService|DM-001, DM-002|login/register/getProfile/requestReset/confirmReset methods exposed; delegates hashing/signing/storage to collaborators; emits audit events on auth state changes|L|P0|
|4|COMP-006|TokenManager and JwtService module|Implement token issuance, verification, refresh rotation, and revocation using Redis-backed refresh state and RS256 JWT signing.|TokenManager, JwtService|DM-002, NFR-SEC-002|issues access TTL=15m and refresh TTL=7d; refresh rotates old token; revoked refresh rejected; RS256 only; 2048-bit key support|L|P0|
|5|COMP-007|UserRepo data access component|Create the Postgres-backed repository responsible for persisting and retrieving user records and related auth metadata.|UserRepo|DM-001|create/findByEmail/findById/updateLastLogin/updatePasswordHash methods available; uniqueness violations mapped cleanly; parameterized SQL only|M|P0|
|6|COMP-008|PasswordHasher component|Implement the password hashing abstraction used across registration, login, and reset confirmation.|PasswordHasher|NFR-SEC-001|bcrypt cost=12 enforced; verify and hash methods available; plaintext never logged or persisted; benchmark target suitable for <500ms hash time|M|P0|
|7|COMP-012|ResetTokenStore component|Create the single-use password reset token store with expiration and replay prevention semantics.|ResetTokenStore, Redis|FR-AUTH-005|token hashed before storage; TTL=1h; consume-once semantics; reused token rejected; user binding enforced|M|P0|
|8|COMP-013|AuditLogWriter component|Create the backend writer that records structured auth events for compliance and operational visibility.|AuditLogWriter, PostgreSQL|NFR-COMPLIANCE-002|event includes userId-or-anonymous, timestamp, IP, outcome, eventType; write path available to AuthService; retention policy configurable|M|P0|
|9|FR-AUTH-001|Login domain flow|Implement credential authentication against stored bcrypt hashes with lockout-aware failure handling.|AuthService, PasswordHasher|COMP-005, COMP-008|valid credentials return AuthToken; invalid returns 401; non-existent email returns generic 401; lockout after 5 failed attempts in 15m|M|P0|
|10|FR-AUTH-002|Registration domain flow|Implement validated account creation with unique-email enforcement and immediate user-profile creation.|AuthService, UserRepo|COMP-005, COMP-007, NFR-COMPLIANCE-001|valid registration returns UserProfile; duplicate email returns 409; weak password returns 400; consent recorded with timestamp|M|P0|
|11|FR-AUTH-003|Token issuance and refresh domain flow|Implement access/refresh token lifecycle for authenticated and silent-refresh scenarios.|TokenManager|COMP-006, DM-002|login issues 15m/7d pair; valid refresh returns new pair; expired refresh returns 401; revoked refresh returns 401|M|P0|
|12|FR-AUTH-004|Profile retrieval domain flow|Implement authenticated user profile retrieval with complete required fields.|AuthService, UserRepo|COMP-005, DM-001|returns id,email,displayName,createdAt,updatedAt,lastLoginAt,roles; invalid/expired token returns 401|S|P0|
|13|FR-AUTH-005|Password reset domain flow|Implement reset-request and reset-confirm business logic including token generation, validation, and session invalidation.|AuthService, ResetTokenStore|COMP-005, COMP-012, OQ-003|reset-request triggers token creation and email dispatch; confirm updates password hash; token expires in 1h; used token cannot be reused; existing sessions invalidated|L|P0|
|14|NFR-SEC-001|Password hashing policy|Enforce bcrypt cost factor 12 consistently through the hashing abstraction and tests.|PasswordHasher|COMP-008|bcrypt cost fixed at 12; unit test asserts cost parameter; no weaker fallback allowed|S|P0|
|15|NFR-SEC-002|JWT signing policy|Enforce RS256 token signing and verification using 2048-bit RSA keys and rotation-ready configuration.|JwtService|COMP-006|RS256 enforced; 2048-bit key material loaded from secure config; verification rejects other algs; rotation hooks present|M|P0|
|16|INF-001|PostgreSQL auth storage baseline|Provision and configure PostgreSQL 15+ for user profiles and audit-log storage paths.|PostgreSQL|—|PG15 reachable from auth service; migrations runnable in CI/staging; backups enabled; connection pool sized for auth workload|M|P0|
|17|INF-002|Redis token-state baseline|Provision and configure Redis 7+ for refresh-token revocation and reset-token expiry workflows.|Redis|—|Redis7 reachable from auth service; TTL semantics verified; persistence/HA posture documented; key namespaces defined|M|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`AuthService` dependency graph|Dependency injection|`AuthService` wired to `UserRepo`, `PasswordHasher`, `TokenManager`, `ResetTokenStore`, `AuditLogWriter`|M1|All backend auth flows|
|`TokenManager` refresh rotation pipeline|Dispatch table|issue→verify→revoke→reissue path registered|M1|Login, refresh, logout, password-reset session invalidation|
|`PasswordHasher` strategy|Strategy pattern|bcrypt cost-12 implementation registered behind abstraction|M1|Registration, login, reset confirmation|
|`AuditLogWriter` event binding|Callback/event binding|auth success/failure/reset events bound to writer|M1|Compliance logs, operational metrics, admin visibility|

### Milestone Dependencies — M1

- External dependencies: PostgreSQL 15+, Redis 7+, Node.js 20 LTS, bcryptjs, jsonwebtoken, SendGrid tenant setup, organizational security policy `SEC-POLICY-001`.
- Architectural constraints enforced here: AC-001, AC-002, AC-003, AC-004, AC-005, AC-012.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|Maximum allowed `UserProfile.roles` array length?|Schema and validator finalization for `DM-001` depends on explicit upper bound for `roles`.|auth-team|2026-04-01|
|2|OQ-005|Account lockout policy thresholds (N attempts)?|Current implementation can ship with 5 failures / 15 minutes, but policy confirmation is required before hardening and runbook publication.|Security|—|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Token signing misconfiguration exposes invalid or forgeable JWTs.|High|Medium|Authentication compromise across all protected endpoints.|Enforce RS256-only validation, 2048-bit keys, secure secret distribution, and configuration tests before API exposure.|security-team|
|2|Early schema mistakes in `UserProfile` cause migration churn and downstream contract instability.|High|Medium|Rework across repo, APIs, and frontend profile flows.|Resolve `OQ-002` before schema freeze; review AC field fidelity against source model; run migration rehearsal in staging.|auth-team|
|3|Reset-token replay or storage mistakes permit password-reset abuse.|High|Medium|Account takeover and support burden.|Hash reset tokens at rest, enforce one-time consume, bind token to user, and test expiry and replay paths before endpoint exposure.|security-team|

## M2: External Contracts and Backend Flows

**Objective:** Expose the backend auth capabilities through stable versioned APIs, complete missing contract gaps implied by the PRD, and wire gateway-level protections and compatibility guarantees. | **Duration:** Weeks 4-5 | **Entry:** M1 services and stores available in staging | **Exit:** All backend auth endpoints are contract-complete, versioned under `/v1/auth/*`, protected by gateway policy, and aligned with PRD user stories.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|18|API-001|Login endpoint contract|Expose login over `POST /v1/auth/login` with generic credential errors and lockout/rate-limit handling.|API Gateway, AuthService|FR-AUTH-001, AC-006|method:POST; path:/v1/auth/login; auth:none; request:{email,password}; response:AuthToken; errors:401-invalid-creds-generic,423-locked,429-rate-limited; delegates PasswordHasher→TokenManager→JwtService|M|P0|
|19|API-002|Registration endpoint contract|Expose account creation over `POST /v1/auth/register` with validation and duplicate-email handling.|API Gateway, AuthService|FR-AUTH-002, NFR-COMPLIANCE-001|method:POST; path:/v1/auth/register; auth:none; request:{email,password,displayName,consent}; response:UserProfile; errors:400-validation,409-duplicate; consent timestamp persisted|M|P0|
|20|API-003|Profile endpoint contract|Expose authenticated profile retrieval over `GET /v1/auth/me` with Bearer access-token validation.|API Gateway, AuthService|FR-AUTH-004|method:GET; path:/v1/auth/me; auth:Bearer-accessToken; response:UserProfile; headers:Authorization; errors:401-missing-expired-invalid|S|P0|
|21|API-004|Refresh endpoint contract|Expose token refresh over `POST /v1/auth/refresh` with rotation and revoked/expired handling.|API Gateway, TokenManager|FR-AUTH-003, AC-P-003|method:POST; path:/v1/auth/refresh; auth:refreshToken-in-body; request:{refreshToken}; response:AuthToken; errors:401-expired-revoked; old refresh revoked on success|M|P0|
|22|API-005|Reset-request endpoint gap fill|Add the PRD-required password-reset request endpoint omitted from the enumerated TDD API table.|API Gateway, AuthService|FR-AUTH-005, OQ-003|method:POST; path:/v1/auth/reset-request; auth:none; request:{email}; response:202-or-200-generic-confirmation; enumeration-safe for registered/unregistered emails; email dispatched within 60s target|M|P0|
|23|API-006|Reset-confirm endpoint gap fill|Add the PRD-required password-reset confirmation endpoint omitted from the enumerated TDD API table.|API Gateway, AuthService|FR-AUTH-005|method:POST; path:/v1/auth/reset-confirm; auth:none; request:{token,password}; response:204-or-200-success; errors:400-invalid-token,401-expired,409-used-token; password update invalidates sessions|M|P0|
|24|API-007|Logout endpoint gap fill|Add the PRD user-story endpoint for ending an authenticated session immediately.|API Gateway, AuthService|COMP-011|method:POST; path:/v1/auth/logout; auth:Bearer-accessToken-plus-refresh-context; response:204; revoked current refresh token; redirect-safe for frontend logout UX|S|P1|
|25|COMP-001|LoginPage route contract integration|Bind the login page to `API-001` and the shared error envelope expected by the frontend.|LoginPage|API-001|onSuccess:() => void; redirectUrl?:string; renders email/password inputs; submits to API-001; generic invalid-credential error; handles 423/429; success stores AuthToken via provider|M|P1|
|26|COMP-002|RegisterPage route contract integration|Bind the register page to `API-002` with inline validation and consent capture.|RegisterPage|API-002, NFR-COMPLIANCE-001|onSuccess:() => void; termsUrl:string; renders email/password/displayName/consent; inline password-strength validation; duplicate email surfaced clearly; success redirects/logs in user|M|P1|
|27|COMP-014|PasswordResetRequestPage component|Provide the frontend form for requesting password-reset emails with enumeration-safe confirmation UX.|PasswordResetRequestPage|API-005|renders email input; submit always shows same confirmation state; completion within 60s UX expectation; no user enumeration leakage|M|P1|
|28|COMP-015|PasswordResetConfirmPage component|Provide the frontend form for confirming password reset and entering a new compliant password.|PasswordResetConfirmPage|API-006|accepts token and new password; inline password policy hints; expired/used token states handled; success redirects to login|M|P1|
|29|COMP-016|ErrorEnvelope and auth-code registry|Centralize stable auth error codes and messages for frontend/backend alignment and Sam’s API-consumer requirements.|API Layer, Frontend|API-001, API-002, API-003, API-004|error envelope={error:{code,message,status}}; stable codes documented for invalid creds, locked, rate-limited, duplicate email, expired token, revoked token; tokenType always Bearer|S|P0|
|30|COMP-017|Gateway rate-limit and CORS policy wiring|Apply API-Gateway controls for rate limits, known-origin CORS, and TLS 1.3 across auth routes.|API Gateway|API-001, API-002, API-003, API-004, API-005, API-006, AC-007, AC-008|login=10/min/IP; register=5/min/IP; me=60/min/user; refresh=30/min/user; CORS allow-list only known origins; TLS1.3 enforced on all endpoints|M|P0|
|31|COMP-018|API versioning and contract-governance policy|Codify `/v1/auth/*` routing, additive-change policy, and breaking-change governance for future revisions.|API Layer|AC-006|all endpoints served under /v1/auth/*; additive optional fields allowed in-version; breaking changes require new major path; contract document published|S|P1|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Auth route registry|Registry|`/v1/auth/login`,`/register`,`/me`,`/refresh`,`/reset-request`,`/reset-confirm`,`/logout` registered|M2|API Gateway, frontend router, test suites|
|Error-code map|Registry|Stable `AUTH_*` error codes mapped to status and message contracts|M2|Frontend views, API consumers, integration tests|
|Gateway middleware chain|Middleware chain|TLS, CORS, rate limit, auth verification, handler dispatch ordered and bound|M2|All auth endpoints|
|Password-reset route wiring|Event binding|request and confirm routes bound to reset-token store and email dispatch path|M2|Frontend reset pages, email delivery pipeline|

### Milestone Dependencies — M2

- Depends on M1 foundation services and data stores.
- External dependencies: API Gateway, SendGrid, security policy `SEC-POLICY-001`, product PRD `AUTH-PRD-001`.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-003|Should password reset emails be sent sync or async?|Affects `API-005` latency budget, retry semantics, and failure handling architecture.|Engineering|—|
|2|OQ-004|Max refresh tokens per user across devices?|Affects `API-004` behavior, Redis bounds, and session-revocation policy for multi-device users.|Product|—|
|3|OQ-007|PRD JTBD for Jordan (admin audit log UI) has no corresponding FR in TDD — is admin tooling in scope v1.0?|Determines whether API-only audit logging is sufficient for release or if admin-facing retrieval contracts are required in this roadmap.|product-team|—|
|4|OQ-001|Should `AuthService` support API key auth for service-to-service calls?|Affects whether a non-user auth mode must be reserved in the v1 contract or explicitly deferred as out of scope.|test-lead|2026-04-15|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|API contract gaps leave PRD user stories only partially implementable.|High|High|Reset and logout flows would be incomplete at release.|Add `API-005`, `API-006`, and `API-007` as explicit deliverables and flag TDD update requirement in decision tracking.|architect|
|2|Gateway misconfiguration exposes auth endpoints to cross-origin abuse or ineffective rate limiting.|High|Medium|Brute-force and token abuse risk increases materially.|Apply route-specific quotas, strict origin allow-list, TLS 1.3, and contract tests at the gateway layer before beta.|platform-team|
|3|Unstable error codes break Sam’s programmatic integration scenario.|Medium|Medium|Client integrations become brittle and retry logic unreliable.|Define and freeze `AUTH_*` registry with contract tests and additive-only versioning policy.|backend-team|

## M3: Frontend Experience and Session UX

**Objective:** Deliver the end-user and API-consumer-facing experience through route components, auth context orchestration, silent refresh, logout UX, and secure token handling. | **Duration:** Weeks 6-7 | **Entry:** M2 API contracts frozen in staging | **Exit:** Users can register, log in, persist sessions, view profile, reset passwords, and log out through coherent browser flows that satisfy persona expectations.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|32|COMP-003|ProfilePage implementation|Build the authenticated profile page that renders the required `UserProfile` fields from `API-003`.|ProfilePage|API-003, DM-001|auth:required; renders id,email,displayName,createdAt,updatedAt,lastLoginAt,roles from API-003; invalid or expired session redirects through AuthProvider|M|P1|
|33|COMP-004|AuthProvider implementation|Implement the React auth context that stores auth state, performs silent refresh, handles 401 recovery, and clears tokens on tab close.|AuthProvider|API-001, API-003, API-004, API-007, DM-002|children:ReactNode; state:accessToken,refreshToken,expiresIn,tokenType; silent refresh via TokenManager contract; intercept 401→refresh or redirect LoginPage; clears tokens on tab close|L|P0|
|34|COMP-019|ProtectedRoutes guard|Create route-guard wiring for protected navigation to profile and future authenticated surfaces.|ProtectedRoutes|COMP-004|unauthenticated users redirected to LoginPage; expired sessions attempt silent refresh first; preserves redirect target|S|P1|
|35|COMP-020|PublicRoutes guard|Create public-route wiring so login/register/reset routes remain accessible without auth while respecting active sessions.|PublicRoutes|COMP-004|authenticated users may be redirected away from login/register appropriately; reset routes remain accessible with token links; route state preserved|S|P2|
|36|COMP-021|Session bootstrap and hydration logic|Hydrate browser auth state on app load using refresh semantics without persisting access tokens insecurely.|AuthProvider|COMP-004, API-004|page refresh attempts session restoration via refresh token path; no access token persisted to localStorage; expired refresh leads to clear login prompt|M|P0|
|37|COMP-022|Remembered redirect and post-auth navigation|Provide consistent redirect behavior after login, registration, logout, and reset completion.|AuthProvider, Router|COMP-001, COMP-002, COMP-014, COMP-015, API-007|login/register success redirect to requested path or dashboard; logout redirects to landing/login; reset confirmation redirects to login|S|P1|
|38|COMP-023|Client-side password-strength and consent UX|Unify password and consent validation behavior across register and reset-confirm screens.|RegisterPage, PasswordResetConfirmPage|COMP-002, COMP-015, NFR-COMPLIANCE-001|shows unmet password rules inline; consent required on registration only; validation prevents premature submit; messages match backend rules|S|P1|
|39|COMP-024|Lockout, rate-limit, and session-expiry messaging|Create explicit UI states for 423 locked, 429 rate-limited, and expired-session recovery paths.|LoginPage, AuthProvider|API-001, API-004|423 displays retry/reset guidance; 429 displays throttling guidance; expired session explains re-login requirement after refresh window|S|P1|
|40|COMP-025|Password reset email-link entry flow|Support token-bearing navigation from email link into reset confirmation UX.|PasswordResetConfirmPage, Router|COMP-015, API-006|token read from URL safely; invalid/missing token states rendered; no token echoed in logs/analytics|S|P1|
|41|COMP-026|Client auth analytics hooks|Emit client-side funnel events for registration, login, refresh, reset-request, reset-confirm, and logout to support PRD business metrics.|Frontend Analytics|COMP-001, COMP-002, COMP-014, COMP-015, API-007|events emitted for start/success/failure where appropriate; no secrets captured; supports SC-006, SC-008, SC-010 measurement|M|P1|
|42|NFR-COMPLIANCE-001|Registration consent capture UX|Ensure GDPR consent is visibly collected and timestamped during registration without expanding collected PII.|RegisterPage, AuthService|COMP-002, API-002, NFR-COMPLIANCE-003|consent checkbox/text shown at registration; submit blocked until consent; timestamp propagated to backend; no extra PII beyond allowed fields|S|P0|
|43|NFR-COMPLIANCE-003|Data-minimization enforcement|Ensure frontend and backend only collect permitted identity fields in registration and profile flows.|RegisterPage, API Layer|COMP-002, API-002, DM-001|collection limited to email,password,displayName,consent; no extra PII fields in UI or API payloads; profile rendering does not imply extra storage|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|App auth-provider wrapper|Dependency injection|`AuthProvider` wraps app root and router|M3|Login/Register/Profile/Reset routes|
|Route guard registry|Registry|Public and protected route groups bound to router|M3|All auth-related navigation|
|401 interceptor chain|Middleware chain|API client intercepts 401 → refresh attempt → redirect fallback|M3|Profile fetches, protected mutations, session bootstrap|
|Client analytics event bindings|Event binding|auth funnel events bound to UI transitions and API outcomes|M3|Product metrics dashboards, experiment analysis|

### Milestone Dependencies — M3

- Depends on M2 contracts and gateway protections.
- Architectural constraints enforced here: AC-P-001, AC-P-003, AC-010, AC-011.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-006|Support "remember me" for extended sessions?|Affects session UX, refresh-token policy, and whether current 7-day refresh window is sufficient for Alex’s expectations.|Product|—|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Frontend token handling introduces XSS-exposure or insecure persistence.|High|Medium|Access-token theft and account compromise.|Keep access token memory-only, avoid localStorage/sessionStorage persistence, and use secure refresh path wiring with code review focused on XSS sinks.|frontend-team|
|2|Poor lockout or reset UX suppresses registration and recovery conversion.|Medium|Medium|Business targets SC-006 and SC-010 miss despite working backend.|Design clear inline validation, generic errors, explicit recovery messaging, and measure funnel drop-off with analytics hooks.|product-design|
|3|Silent-refresh loops cause redirect churn and broken protected navigation.|Medium|Medium|Users experience forced logout or unusable sessions.|Implement bounded retry logic, explicit expired-session state, and E2E coverage for refresh-expiry scenarios.|frontend-team|

## M4: Validation, Compliance, and Non-Functional Assurance

**Objective:** Validate the implementation against functional, performance, reliability, security, and compliance targets using unit, integration, E2E, observability, and audit-readiness deliverables. | **Duration:** Weeks 8-10 | **Entry:** M2 and M3 flows working end-to-end in staging | **Exit:** Test pyramid complete, non-functional targets measured, compliance controls evidenced, and release criteria satisfied.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|44|TEST-001|Unit test: valid login returns AuthToken|Validate that `AuthService.login()` verifies password and issues the expected token pair.|AuthService tests|FR-AUTH-001, COMP-005|valid email+password invokes PasswordHasher.verify then TokenManager.issueTokens; returns AuthToken with accessToken and refreshToken|S|P0|
|45|TEST-002|Unit test: invalid login returns error|Validate rejection path for invalid credentials with no token issuance.|AuthService tests|FR-AUTH-001|PasswordHasher.verify=false yields 401-compatible error; TokenManager.issueTokens not called; no enumeration difference between unknown email and wrong password|S|P0|
|46|TEST-003|Unit test: refresh succeeds and rotates token|Validate token refresh lifecycle and old-token revocation.|TokenManager tests|FR-AUTH-003|valid refresh validates, revokes old token, issues new pair through JwtService; old refresh no longer accepted|S|P0|
|47|TEST-004|Integration test: registration persists UserProfile|Validate registration end-to-end against real PostgreSQL persistence.|AuthService + PostgreSQL tests|FR-AUTH-002, DM-001|registration inserts id,email,displayName,createdAt,updatedAt,lastLoginAt,roles correctly; duplicate email rejected; password stored hashed only|M|P0|
|48|TEST-005|Integration test: expired refresh token rejected|Validate Redis TTL behavior for refresh-token expiration.|TokenManager + Redis tests|FR-AUTH-003|expired refresh token returns 401; Redis TTL expiration enforces invalidation without manual cleanup|M|P0|
|49|TEST-006|E2E test: register → login → profile|Validate the core browser journey across frontend and backend surfaces.|Playwright E2E|COMP-001, COMP-002, COMP-003, COMP-004|user can register, log in, land on profile, and see expected account details; auth state handled through AuthProvider|M|P0|
|50|TEST-007|E2E test: forgot-password recovery journey|Validate the self-service recovery flow from reset request to successful re-login.|Playwright E2E|API-005, API-006, COMP-014, COMP-015|request shows generic confirmation; email-link flow reaches confirm form; reset succeeds; old password fails; new password succeeds|M|P0|
|51|TEST-008|E2E test: logout and session-expiry behavior|Validate logout and expired-session handling implied by the PRD journeys.|Playwright E2E|API-007, COMP-021, COMP-024|logout ends session immediately; protected route requires re-auth; expired refresh window results in clear login prompt and preserved redirect semantics|M|P1|
|52|NFR-PERF-001|API response-time validation|Measure all auth endpoints against the <200ms p95 target using tracing and load probes.|APM, AuthService|API-001, API-002, API-003, API-004, API-005, API-006|all auth endpoints p95 <200ms in staging benchmark; tracing spans available on AuthService methods; bottlenecks identified and addressed|M|P0|
|53|NFR-PERF-002|Concurrent authentication validation|Prove support for 500 concurrent login requests using load testing with realistic infra settings.|k6, Kubernetes|API-001, INF-001, INF-002|500 concurrent logins sustained; error rate within release tolerance; no saturation-induced auth failures; resource scaling profile captured|M|P0|
|54|NFR-REL-001|Availability and health validation|Implement health monitoring and release gating for 99.9% availability objective.|Health checks, Monitoring|COMP-005|health endpoint available; uptime monitoring configured; SLO dashboard tracks 30-day rolling availability; release checklist references 99.9% target|M|P0|
|55|NFR-COMPLIANCE-002|SOC2 audit-logging validation|Validate that all auth events are logged with required fields and retention semantics.|Audit logging, Compliance QA|COMP-013, AC-P-002|login success/failure, registration, refresh, reset-request, reset-confirm, logout all log userId/timestamp/IP/outcome/eventType; 12-month retention policy configured; logs queryable|L|P0|
|56|TEST-009|Security validation: algorithm, key, and token misuse checks|Validate bcrypt cost, RS256 enforcement, revoked-token behavior, and reset-token replay resistance.|Security tests|NFR-SEC-001, NFR-SEC-002, COMP-012|bcrypt cost=12 asserted; non-RS256 JWTs rejected; revoked refresh rejected; used reset token rejected; raw secrets absent from logs|M|P0|
|57|TEST-010|Coverage and release-gate verification|Prove release criteria for unit coverage and FR integration completeness are met before rollout.|CI, QA|TEST-001, TEST-002, TEST-003, TEST-004, TEST-005, TEST-006|unit coverage ≥80% for AuthService/TokenManager/JwtService/PasswordHasher; all 5 FRs verified with real PG+Redis integration evidence|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Test suite registry|Registry|unit, integration, and E2E suites bound to CI stages|M4|Release pipeline, QA sign-off|
|Tracing pipeline|Middleware chain|OpenTelemetry spans wired through AuthService→PasswordHasher→TokenManager→JwtService|M4|Performance dashboards, debugging, audits|
|Metrics emitter bindings|Event binding|login/refresh/registration counters and latency histograms bound to Prometheus|M4|SLO dashboards, rollout gates|
|Compliance evidence package|Callback/workflow|audit-log validation, retention config, and test evidence assembled for review|M4|Compliance, security, release approvers|

### Milestone Dependencies — M4

- Depends on M2 backend contracts and M3 frontend/session UX.
- External dependencies: Prometheus, OpenTelemetry, k6/load-test environment, compliance reviewers.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Incomplete audit logging causes SOC2 control failure despite feature completeness.|High|Medium|Release blocked or compliance exposure persists.|Define log schema early, validate every auth event path, and include retention configuration in release evidence.|compliance-team|
|2|Performance regressions under concurrency break login UX during rollout.|High|Medium|Missed p95 target, rollout rollback, and user dissatisfaction.|Run k6 before beta, trace slow paths, scale infra baseline, and gate rollout on measured thresholds.|platform-team|
|3|Test coverage appears adequate but misses cross-stack edge cases like reset replay or session expiry.|Medium|Medium|Production defects escape into rollout.|Use mixed pyramid coverage with real PG/Redis integration, E2E journeys, and explicit security regression tests.|qa-team|

## M5: Rollout, Migration, and Operations

**Objective:** Execute the phased feature-flag rollout, operationalize observability and incident response, and validate production readiness for general availability. | **Duration:** Weeks 11-14 | **Entry:** M4 release gates passed and stakeholders approved rollout plan | **Exit:** Feature flags rolled through alpha/beta/GA, rollback path proven, operational ownership accepted, and success metrics are measurable in production.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|58|MIG-001|Phase 1 internal alpha rollout|Deploy auth stack to staging/internal audiences behind `AUTH_NEW_LOGIN` with manual validation of all core flows.|Release pipeline|TEST-010, AC-010|staging deploy complete; auth-team+QA validate FR-AUTH-001..005 manually; `AUTH_NEW_LOGIN` default OFF outside alpha; zero P0/P1 defects at exit|M|P0|
|59|MIG-002|Phase 2 beta 10% rollout|Enable the new login flow for 10% of traffic and monitor latency, errors, and Redis stability.|Feature flags, Platform|MIG-001, NFR-PERF-001, NFR-PERF-002|10% traffic exposed; p95 <200ms maintained; error rate <0.1%; no Redis instability; rollback criteria monitored live|M|P0|
|60|MIG-003|Phase 3 general availability rollout|Promote the auth system to GA, remove the new-login flag, and complete the refresh-flow enablement path.|Feature flags, Platform|MIG-002, NFR-REL-001|`AUTH_NEW_LOGIN` removed after GA; `AUTH_TOKEN_REFRESH` enabled then scheduled for removal; 99.9% uptime observed across acceptance window; dashboards green|M|P0|
|61|OPS-001|Runbook for AuthService outage|Operationalize diagnosis and recovery steps for auth-service outages across pods, database, and Redis dependencies.|Runbook, On-call|MIG-001|symptoms, diagnosis, resolution, escalation documented; restart/failover steps tested; on-call ack path defined|S|P0|
|62|OPS-002|Runbook for token-refresh failures|Operationalize diagnosis and recovery for refresh failures, redirect loops, and key-access issues.|Runbook, On-call|MIG-001, API-004, COMP-004|diagnoses Redis connectivity, key access, and feature-flag state; resolution path documented; user re-login fallback explicit|S|P0|
|63|OPS-003|On-call ownership and escalation model|Establish first-two-weeks post-GA coverage, access, and escalation responsibilities.|Operations|MIG-002|P1 ack within 15 min; 24/7 auth-team rotation for first 2 weeks post-GA; tooling access documented; escalation chain approved|S|P0|
|64|OPS-004|Capacity-planning baseline|Set production scaling policies for AuthService, Postgres, and Redis against the 500-concurrent-user target.|Kubernetes, PostgreSQL, Redis|NFR-PERF-002, INF-001, INF-002|AuthService 3 replicas/HPA to 10 at CPU>70%; Postgres pool baseline 100 with growth path to 200; Redis 1GB baseline with scale trigger >70% utilization|M|P0|
|65|OPS-005|Observability and alerting package|Deploy structured logs, metrics, traces, dashboards, and alerts for auth reliability and rollout gating.|Prometheus, OpenTelemetry, Logging|NFR-PERF-001, NFR-REL-001, NFR-COMPLIANCE-002|logs for login/registration/refresh/reset/logout with sensitive fields excluded; metrics include auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total; tracing spans end-to-end; alerts configured|L|P0|
|66|COMP-027|Legacy-auth fallback and rollback wiring|Implement and verify the ordered rollback path from new auth to legacy auth under trigger conditions.|Release controls|MIG-001, MIG-002, MIG-003|disable `AUTH_NEW_LOGIN` routes to legacy; smoke-test legacy login after rollback; root-cause workflow documented; backup restore trigger included for data corruption|M|P0|
|67|COMP-028|Quarterly key-rotation operations path|Operationalize JWT key rotation with overlap, rollout, and validation procedure after launch.|Security operations|NFR-SEC-002, OPS-005|quarterly rotation schedule defined; overlap window prevents token outage; validation checks public/private key pair distribution; runbook approved|S|P1|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Feature-flag registry|Registry|`AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` bound to rollout stages|M5|Frontend routes, backend handlers, release controls|
|Rollback workflow|Callback/workflow|disable flag → smoke-test legacy → diagnose → restore if needed|M5|On-call, platform-team, incident response|
|Observability sink chain|Middleware chain|logs, metrics, traces, and alerts wired into production monitoring stack|M5|On-call, product metrics, compliance review|
|Escalation path binding|Event binding|auth-team → test-lead → eng-manager → platform-team on incident triggers|M5|Operations and incident management|

### Milestone Dependencies — M5

- Depends on M4 validation and compliance evidence.
- External dependencies: Kubernetes, Prometheus, OpenTelemetry, incident channel, legacy-auth fallback path, stakeholder release approval.

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Migration rollout causes latency/error spikes or Redis instability in production.|High|Medium|Rollback, user-facing auth failures, and release delay.|Use staged flag rollout, real-time dashboards, strict rollback triggers, and legacy fallback smoke tests at each stage.|platform-team|
|2|Incomplete operational readiness leaves incidents unresolved during the first GA window.|High|Medium|Extended outages and user trust loss.|Publish runbooks, staff 24/7 rotation, test escalation path, and ensure tooling access before GA.|operations-team|
|3|Email delivery failures block password reset recovery after launch.|Medium|Low|Support volume rises and recovery KPI misses.|Monitor SendGrid delivery, alert on failures, and provide fallback support channel while preserving enumeration-safe UX.|support-ops|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|PostgreSQL 15+|M1|Required|Block release until provisioned; no acceptable functional fallback|
|Redis 7+|M1|Required|Disable refresh/reset features and keep legacy auth only during incident windows|
|Node.js 20 LTS|M1|Required|Pin runtime image; no alternate runtime supported|
|bcryptjs|M1|Required|No weaker hashing fallback permitted|
|jsonwebtoken|M1|Required|No alternate algorithm library without new security review|
|SendGrid|M1, M2, M5|Required|Fallback support-assisted recovery channel if delivery degraded|
|API Gateway|M2|Required|Service must not bypass gateway protections in production|
|Prometheus|M4, M5|Required|Temporary cloud metrics acceptable only for pre-GA debugging, not release evidence|
|OpenTelemetry|M4, M5|Required|Structured logs only as short-term troubleshooting fallback|
|Kubernetes|M1, M5|Required|Staging-only single-instance run acceptable before GA, not for production|
|AUTH-PRD-001|M1, M2, M3|Required|Roadmap assumptions must be re-approved if PRD changes materially|
|SEC-POLICY-001|M1, M2, M4|Required|Security sign-off blocks release if unavailable|
|INFRA-DB-001|M1|Required|No fallback beyond delaying schema rollout|

### Infrastructure Requirements

- PostgreSQL 15+ with backups, migration pipeline support, and auth-appropriate connection pooling.
- Redis 7+ with TTL reliability, high availability posture, and key namespace isolation for refresh/reset tokens.
- Node.js 20 LTS runtime image and CI parity.
- Kubernetes deployment with 3-replica baseline and HPA to 10 replicas at CPU > 70%.
- Secure RSA key storage and quarterly rotation mechanism.
- API Gateway enforcement of TLS 1.3, CORS allow-list, versioned routing, and per-endpoint rate limits.
- Observability stack with structured logs, Prometheus metrics, OpenTelemetry traces, and alert routing.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-001|Token theft via XSS or insecure frontend token handling.|M3, M5|Medium|High|Keep access tokens memory-only, review XSS sinks, use short access-token TTL, and preserve secure refresh path semantics.|security-team|
|R-002|Brute-force login abuse or ineffective gateway quotas.|M1, M2, M5|High|Medium|Enforce lockout policy, per-route rate limits, monitoring, and escalation to WAF/IP blocking when thresholds exceed norms.|security-team|
|R-003|Data loss or auth instability during migration and rollback.|M1, M5|Low|High|Run staged rollout, rehearse rollback, backup before rollout phases, and preserve legacy-auth fallback until GA confidence is established.|platform-team|
|R-004|Low registration adoption due to poor UX or excessive friction.|M3, M5|Medium|High|Instrument funnel events, run usability checks, refine inline validation and post-auth navigation, and monitor conversion metrics.|product-team|
|R-005|Compliance failure from incomplete audit logging.|M1, M4, M5|Medium|High|Define audit schema early, validate all auth events in tests, and retain evidence package for review.|compliance-team|
|R-006|Email delivery failures block password reset completion.|M2, M3, M5|Low|Medium|Provision SendGrid correctly, monitor delivery, alert on failures, and offer support fallback.|operations-team|
|R-007|Contract or PRD/TDD scope gaps leave user stories partially delivered.|M2, M3|Medium|High|Add explicit gap-fill deliverables (`API-005`/`006`/`007`, reset pages, logout flow) and track required TDD updates.|architect|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC-001|Login response time p95|< 200ms|APM tracing on login endpoint and staged load runs|M4|
|SC-002|Registration success rate|> 99%|Registration integration tests and production funnel analytics|M4|
|SC-003|Token refresh response time p95|< 100ms|Refresh endpoint tracing and focused refresh load tests|M4|
|SC-004|Service availability|99.9% over 30-day rolling window|Health checks, uptime monitoring, and SLO dashboard|M4, M5|
|SC-005|`PasswordHasher.hash()` latency|< 500ms|Unit benchmark and staging performance profiling at cost 12|M1, M4|
|SC-006|Registration conversion|> 60%|Client analytics funnel from landing/signup to confirmed account|M3, M5|
|SC-007|Authenticated DAU|≥ 1000 within 30 days of GA|Production analytics and auth-event aggregation|M5|
|SC-008|Average session duration|> 30 minutes|Refresh-event analytics and session telemetry|M3, M5|
|SC-009|Failed login rate|< 5% of attempts|Auth event log analysis and dashboard review|M4, M5|
|SC-010|Password reset completion|> 80%|Reset-request to reset-confirm funnel tracking|M3, M5|
|SC-011|Unit coverage|≥ 80% for AuthService, TokenManager, JwtService, PasswordHasher|CI coverage gate and test report review|M4|
|SC-012|Functional verification|All 5 FRs pass against real Postgres + Redis|Integration test suite plus manual alpha validation|M4, M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Session architecture|Stateless RS256 access tokens + Redis-backed refresh state|Server-side sessions; opaque-only tokens; third-party IdP|Chosen because AC-001, AC-012, FR-AUTH-003, and Sam’s programmatic refresh JTBD require scalable stateless access with revocable refresh flow.|
|Password hashing approach|`PasswordHasher` abstraction over bcrypt cost 12|Direct bcrypt calls; lower bcrypt cost; argon2 in v1|Chosen because AC-002 and NFR-SEC-001 explicitly require bcrypt cost 12 while abstraction preserves future migration optionality without changing callers.|
|Release strategy|Three-phase feature-flag rollout with legacy fallback|Big-bang cutover; shadow-only launch; dual-write migration|Chosen because MIG-001..003 and R-003 define staged rollout as the lowest-risk path under availability and rollback constraints.|
|API surface completeness|Add explicit logout and reset endpoints missing from enumerated API list|Ship only four listed APIs; defer logout/reset to later phase|Chosen because PRD in-scope stories require logout and self-service password reset end-to-end; omitting them would fail JTBD and scope commitments.|
|Frontend token storage|Memory-only access token with refresh-driven restoration|localStorage; sessionStorage; cookie-stored access token|Chosen because R-001 mitigation and component guidance for `AuthProvider` call for minimizing XSS exposure while preserving silent refresh.|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|3 weeks|Week 1|Week 3|Data models finalized; core services implemented; Postgres/Redis baselines ready|
|M2|2 weeks|Week 4|Week 5|Versioned APIs exposed; gateway protections wired; contract gaps filled|
|M3|2 weeks|Week 6|Week 7|Frontend auth flows complete; session UX stabilized; analytics hooks added|
|M4|3 weeks|Week 8|Week 10|Test pyramid green; performance/compliance targets evidenced; release gates passed|
|M5|4 weeks|Week 11|Week 14|Alpha→beta→GA rollout executed; runbooks accepted; production monitoring live|

**Total estimated duration:** 14 weeks
