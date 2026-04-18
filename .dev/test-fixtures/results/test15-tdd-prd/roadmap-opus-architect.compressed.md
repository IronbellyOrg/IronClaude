<!-- CONV: AuthService=THS, TokenManager=TKN, PasswordHasher=PSS, AuthProvider=THP, password=PA1, UserProfile=SRP, endpoint=NDP, Integration=NTG, SendGrid=SND, FR-AUTH-001=FA0, PostgreSQL=PST, deliverable_count=DC, auth-team=AT, integration=IN1, Dependencies=DPN, rotation=RTT, dependencies=DE1, JwtService=JWT, validation=VLD, registration=RGS -->
---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
generated: "2026-04-17"
generator: "single"
total_milestones: 8
total_task_rows: 89
risk_count: 7
open_questions: 7
domain_distribution:
  frontend: 12
  backend: 38
  security: 18
  performance: 10
  documentation: 8
  devops: 14
consulting_personas: [architect, security, backend, frontend, qa, devops]
milestone_count: 8
milestone_index:
  - id: M1
    title: "Infrastructure Foundation"
    type: FEATURE
    priority: P0
    DE1: []
    DC: 12
    risk_level: Medium
  - id: M2
    title: "Core Domain Services"
    type: FEATURE
    priority: P0
    DE1: [M1]
    DC: 12
    risk_level: High
  - id: M3
    title: "API Layer and Contracts"
    type: FEATURE
    priority: P0
    DE1: [M2]
    DC: 11
    risk_level: Medium
  - id: M4
    title: "Frontend NTG"
    type: FEATURE
    priority: P1
    DE1: [M3]
    DC: 9
    risk_level: Medium
  - id: M5
    title: "Security Hardening and Compliance"
    type: SECURITY
    priority: P0
    DE1: [M2, M3]
    DC: 10
    risk_level: High
  - id: M6
    title: "Quality Assurance and Performance Validation"
    type: TEST
    priority: P0
    DE1: [M4, M5]
    DC: 13
    risk_level: Medium
  - id: M7
    title: "Migration and Phased Rollout"
    type: MIGRATION
    priority: P0
    DE1: [M6]
    DC: 11
    risk_level: High
  - id: M8
    title: "Operational Readiness"
    type: IMPROVEMENT
    priority: P0
    DE1: [M7]
    DC: 11
    risk_level: Medium
total_deliverables: 89
total_risks: 7
estimated_milestones: 8
validation_score: 0.92
validation_status: PASS

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service delivers the foundational identity layer that unblocks the Q2-Q3 2026 personalization roadmap, SOC2 Type II audit readiness, and self-service account recovery. This roadmap sequences 89 deliverables across 8 technical-layer milestones (18 weeks) — proceeding bottom-up from infrastructure (PST 15, Redis 7, RS256 key material) through domain services (`THS`, `TKN`, `PSS`, `JWT`), API surface (`/v1/auth/*`), frontend IN1 (`LoginPage`, `RegisterPage`, `THP`), security/compliance hardening, QA VLD, feature-flagged phased migration, and operational readiness.

**Business Impact:** Unblocks ~$2.4M in projected annual revenue dependent on personalization; satisfies Q3 2026 SOC2 audit requirements; reduces access-issue support ticket volume (up 30% QoQ). Targets RGS conversion >60%, login p95 <200ms, 99.9% availability, and PA1 reset completion >80%.

**Complexity:** MEDIUM (0.65) — 5 FRs and 9 NFRs spanning 6 domains (backend/security/frontend/testing/devops/compliance); security sensitivity is the dominant driver (blast radius of auth flaws) alongside three-phase feature-flagged rollout and cross-stack IN1 (PST, Redis, SND, API Gateway, Kubernetes).

**Critical path:** M1 (DM-001/DM-002 + PG/Redis infra) → M2 (COMP-005 `THS` + COMP-006 `TKN` dispatch) → M3 (API-001/API-002/API-004) → M5 (NFR-SEC-001/002 + NFR-COMP-002 audit logging) → M6 (TEST-001..006 + NFR-PERF load VLD) → M7 (MIG-001..003 phased rollout) → GA.

**Key architectural decisions:**

- Stateless JWT with RS256 (2048-bit keys, quarterly RTT) + opaque refresh tokens hashed in Redis, over server-side sessions — supports horizontal scaling, satisfies Sam's JTBD for programmatic auth, limits token-theft blast radius.
- Self-hosted `THS` orchestrator with pluggable `PSS` abstraction (bcrypt cost 12 today) — rejects Auth0/Firebase third-party IdP; permits future algorithm migration without FR changes.
- Feature-flagged phased rollout (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) with parallel-run migration from legacy auth — mitigates R-003 data loss risk.

**Open risks requiring resolution before M1:**

- OQ-002 `SRP.roles` array maximum length (blocks DM-001 schema finalization).
- OQ-PRD-003 account lockout policy confirmation (TDD sets 5/15min; PRD requests confirmation before encoding into FA0 AC).
- SND account provisioning and API-key secrets RTT process (blocks M2 PA1-reset email path).

## Milestone Summary

|ID|Title|Type|Priority|Effort|DPN|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Infrastructure Foundation|FEATURE|P0|2w|—|12|Medium|
|M2|Core Domain Services|FEATURE|P0|2w|M1|12|High|
|M3|API Layer and Contracts|FEATURE|P0|2w|M2|11|Medium|
|M4|Frontend NTG|FEATURE|P1|2w|M3|9|Medium|
|M5|Security Hardening and Compliance|SECURITY|P0|2w|M2, M3|10|High|
|M6|Quality Assurance and Performance Validation|TEST|P0|2w|M4, M5|13|Medium|
|M7|Migration and Phased Rollout|MIGRATION|P0|4w|M6|11|High|
|M8|Operational Readiness|IMPROVEMENT|P0|2w|M7|11|Medium|

## Dependency Graph

```
M1 (Infra Foundation)
 └─> M2 (Core Domain Services)
      └─> M3 (API Layer)
           ├─> M4 (Frontend Integration) ──┐
           └─> M5 (Security + Compliance) ─┤
                                           └─> M6 (QA + Perf Validation)
                                                └─> M7 (Migration + Rollout)
                                                     └─> M8 (Operational Readiness)
```

Parallel opportunities: M4 and M5 can proceed concurrently once M3 contracts are frozen. Within M7, MIG-004/005 (flag scaffolding) can precede MIG-001 (Alpha) to avoid serialization.

## M1: Infrastructure Foundation

**Objective:** Provision data stores, runtime, libraries, and gateway infrastructure required by all downstream services; finalize `SRP` and `AuthToken` schemas. | **Duration:** Weeks 1-2 | **Entry:** Architecture approved; OQ-002 resolved for DM-001 roles length | **Exit:** DM-001 migrated to staging PG15; Redis 7 reachable from K8s; RS256 key pair generated and mounted; bcryptjs + jsonwebtoken pinned; SND account provisioned.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|SRP PST schema|Create `SRP` table with all required fields and constraints for persistent user identity.|PST 15|—|id:UUIDv4-PK-NOT-NULL; email:string-UNIQUE-NOT-NULL-idx-lowercase-normalized; displayName:string-NOT-NULL-2to100chars; createdAt:timestamptz-NOT-NULL-DEFAULT-now; updatedAt:timestamptz-NOT-NULL-auto-updated; lastLoginAt:timestamptz-NULLABLE; roles:string[]-NOT-NULL-DEFAULT-["user"]; audit-log FK references id|M|P0|
|2|DM-002|AuthToken envelope + Redis refresh record|Define response DTO and Redis-backed refresh record for token lifecycle management.|TKN, Redis 7|DM-001|accessToken:JWT-RS256-NOT-NULL-payload-includes-user-id-and-roles; refreshToken:opaque-string-NOT-NULL-unique-hashed-in-Redis-7day-TTL; expiresIn:number-NOT-NULL-always-900s; tokenType:string-NOT-NULL-always-"Bearer"; revocation-surface-managed-by-TKN|M|P0|
|3|INF-001|PST 15+ cluster provisioning|Provision PG15 primary + read replica with pg-pool for `THS` and audit log storage.|PST 15|—|PG15 primary + 1 replica deployed; pool size=100 tuned; connectivity verified from K8s THS pods; backup schedule daily; PITR enabled|M|P0|
|4|INF-002|Redis 7+ cluster for refresh tokens|Provision Redis 7 cluster with 1GB memory, connection pooling, and failover for `TKN` refresh-token storage.|Redis 7|—|Redis 7 deployed with persistence AOF; 1GB initial memory; connectivity verified; failover tested; eviction policy=noeviction for token keys|S|P0|
|5|INF-003|Node.js 20 LTS runtime baseline|Standardize Node 20 LTS across `THS` base image and CI runners.|THS|—|Base image uses node:20-lts-alpine; CI pins 20.x; security patches auto-applied within 72h|S|P0|
|6|INF-004|bcryptjs library IN1|Pin bcryptjs at latest stable; configure cost factor 12 constant for `PSS`.|PSS|INF-003|bcryptjs pinned; cost=12 defined as env-overrideable constant; SBOM entry created|S|P0|
|7|INF-005|jsonwebtoken library IN1|Pin jsonwebtoken; configure RS256 + 5s clock-skew for `JWT`.|JWT|INF-003|jsonwebtoken pinned; RS256 algorithm enforced; clockTolerance=5s; SBOM entry created|S|P0|
|8|INF-006|SND account + API key provisioning|Provision SND tenant, sending domain with SPF/DKIM/DMARC, and rotating API keys for PA1-reset email delivery.|SND|—|Tenant active; SPF/DKIM/DMARC passing on auth-mailer domain; primary+backup API keys in secrets manager; delivery webhook NDP registered|M|P0|
|9|INF-007|API Gateway configuration baseline|Configure gateway routes, CORS allow-list, TLS 1.3, and slot for per-NDP rate limits.|API Gateway|—|/v1/auth/* routed; CORS allow-list=known-frontend-origins; TLS1.3 enforced; rate-limit plugin enabled (values per API)|M|P0|
|10|INF-008|Kubernetes base deployment + HPA skeleton|Create K8s Deployment, Service, HPA, and secrets for `THS` with 3-replica baseline.|Kubernetes|INF-003|Deployment 3 replicas; Service ClusterIP; HPA placeholder CPU>70% scale-to-10; secrets mounted via K8s Secret|M|P0|
|11|INF-009|RS256 2048-bit RSA key material + RTT schedule|Generate initial RS256 keypair; store in secrets manager; schedule quarterly RTT with overlap window.|JWT, Secrets Manager|—|Keypair=2048-bit RSA; private key in secrets manager ACL-restricted to auth-service; public key JWKS exposed; quarterly RTT runbook authored; overlap=1 week|M|P0|
|12|INF-010|pg-pool configuration for UserRepo|Configure pg-pool with pool size 100, connection timeout, and idle eviction for `UserRepo`.|UserRepo, PST 15|INF-001|pool min=10 max=100; idle-timeout=30s; connection-timeout=5s; wait-timeout<50ms alerting threshold|S|P0|

### NTG Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|RS256 JWKS NDP|Dependency Injection|INF-009|M1|JWT (M2), API Gateway verifier|
|pg-pool factory|Dependency Injection|INF-010|M1|UserRepo (M2), audit-log writer (M5)|
|Redis client factory|Dependency Injection|INF-002|M1|TKN (M2), rate-limit store (M5)|
|SND client|Dependency Injection|INF-006|M1|THS reset flow (M2)|

### Milestone DPN — M1

- No upstream milestone DE1.
- External: SOC2 auditor sign-off on audit-log storage plan; security team key-custody approval for INF-009.

### Open Questions — M1

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|Maximum allowed `SRP.roles` array length?|Blocks DM-001 schema finalization (column type choice, VLD rules).|AT|2026-04-01|

## M2: Core Domain Services

**Objective:** Build backend domain services (`PSS`, `JWT`, `UserRepo`, `TKN`, `THS`) and implement all 5 functional requirements behind pluggable abstractions. | **Duration:** Weeks 3-4 | **Entry:** M1 infrastructure green; DM-001/DM-002 finalized | **Exit:** All FA0..005 pass unit+IN1 tests against real PG/Redis; `THS` orchestrator wired with DI container.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|13|COMP-008|`PSS` backend service|Implement bcrypt-based hasher with cost 12 and pluggable algorithm interface for future migration.|PSS|INF-004|hash()+verify() methods; cost=12; interface permits algorithm swap; hash time <500ms on baseline hardware; raw passwords never logged|M|P0|
|14|COMP-007|`JWT` backend service|Implement RS256 signing/verification with 5s clock skew; expose sign/verify primitives for `TKN`.|JWT|INF-005, INF-009|sign()+verify() for RS256; 2048-bit RSA; clockTolerance=5s; sign<5ms p95; verify<5ms p95; unit test asserts RS256 only|M|P0|
|15|COMP-009|`UserRepo` data-access layer|Implement PST-backed repository for `SRP` CRUD with email uniqueness enforcement.|UserRepo|DM-001, INF-010|findByEmail() case-insensitive; create() enforces UNIQUE email; updateLastLoginAt(); updatePasswordHash(); all calls via pg-pool; parameterized queries only (no string interpolation)|M|P0|
|16|COMP-006|`TKN` backend service|Issue access+refresh token pairs; store hashed refresh tokens in Redis 7-day TTL; support silent refresh and revocation.|TKN|COMP-007, INF-002, DM-002|issueTokens()→AuthToken; refresh()→new pair, revoke old; revoke() deletes Redis record; stored refresh=SHA-256 hash (not plaintext); TTL=604800s|M|P0|
|17|COMP-005|`THS` orchestrator|Orchestrate authentication flows by composing `PSS`, `TKN`, `UserRepo`; expose login/register/me/reset methods.|THS|COMP-006, COMP-008, COMP-009|DI-wired DE1; login+register+me+reset-request+reset-confirm methods; no direct DB access; all IO routed through injected deps; unit-testable with mocks|L|P0|
|18|FA0|Login with email + PA1|Authenticate users by validating email/PA1 credentials against stored bcrypt hashes.|THS|COMP-005, COMP-008|valid credentials→200+AuthToken; invalid→401 generic error; non-existent email→401 (no enumeration); account locked after 5 failed attempts/15min window|M|P0|
|19|FR-AUTH-002|User RGS with VLD|Create new accounts with email uniqueness, PA1 strength enforcement, and `SRP` creation.|THS|COMP-005, COMP-009|valid→201+SRP; duplicate email→409; weak PA1 (<8 chars, no uppercase, no number)→400; bcrypt cost 12 persisted|M|P0|
|20|FR-AUTH-003|JWT token issuance and refresh|Issue JWT access (15min) + opaque refresh (7day) tokens; POST /auth/refresh returns new pair and revokes old.|TKN|COMP-006, COMP-007|login returns both tokens with specified TTLs; /auth/refresh valid→new pair; expired refresh→401; revoked refresh→401; old refresh revoked on RTT|M|P0|
|21|FR-AUTH-004|User profile retrieval|Return authenticated user's `SRP` via `THS.me()`.|THS|COMP-005|GET /auth/me with valid access token→SRP; expired/invalid→401; response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles|S|P0|
|22|FR-AUTH-005|Password reset flow|Two-step reset: request (sends email with 1h token) and confirmation (validates token, updates hash, invalidates sessions).|THS|COMP-005, INF-006|/auth/reset-request sends email with token; /auth/reset-confirm with valid token updates hash; tokens expire 1h; used tokens rejected on reuse; all refresh tokens for user invalidated on confirm|L|P0|
|23|COMP-010|Password reset token store|Generate, persist, and expire single-use reset tokens in Redis; validate on confirm.|TKN, Redis 7|INF-002|reset tokens 32-byte URL-safe; TTL=3600s; stored as SHA-256 hash; single-use (deleted on consume); throughput=100/s|S|P0|
|24|COMP-011|Logout NDP handler|Handler to terminate current session by revoking refresh token (PRD AUTH-E1 gap fill).|THS, TKN|COMP-006|POST /auth/logout with valid access token→204; refresh token revoked in Redis; subsequent refresh attempts→401; PRD user story AUTH-E1 "Log Out" AC satisfied|S|P1|

### NTG Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`THS` DI container|Dependency Injection|COMP-005|M2|API handlers (M3), test harness (M6)|
|`TKN` issue/refresh/revoke dispatch|Dispatch Table|COMP-006|M2|login/refresh/logout handlers (M3), reset-confirm (M2)|
|SND mailer strategy|Strategy Pattern|FR-AUTH-005|M2|Password reset email send (M2), operational alerts (M8)|
|`PSS` algorithm interface|Strategy Pattern|COMP-008|M2|THS login/register/reset (M2), future algorithm migration|

### Milestone DPN — M2

- Depends on M1 (all INF-* provisioning complete).

### Open Questions — M2

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should PA1 reset emails be sent synchronously or asynchronously?|Determines FR-AUTH-005 request-path latency; affects SND failure-mode handling.|Engineering|2026-04-20|
|2|OQ-PRD-002|Maximum number of refresh tokens allowed per user across devices?|Affects `TKN` storage bounds and Sam's programmatic IN1 scenarios; drives Redis capacity planning.|Product|2026-04-20|
|3|GAP-001|Logout NDP COMP-011 added to satisfy PRD AUTH-E1 user story "Log Out"; TDD FR set does not explicitly cover it.|PRD requires; TDD should be updated to include FR-AUTH-006 logout.|AT|2026-04-25|

## M3: API Layer and Contracts

**Objective:** Expose all auth capabilities via versioned REST endpoints under `/v1/auth/*` with consistent error envelope, per-NDP rate limits, CORS policy, and TLS enforcement. | **Duration:** Weeks 5-6 | **Entry:** M2 services complete and covered by unit tests | **Exit:** All 6 APIs respond to contract tests; error envelope, rate-limits, and TLS all enforced at gateway.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|25|API-001|POST /auth/login|Login NDP: validate credentials via `THS`, return `AuthToken` pair.|THS, API Gateway|FA0, INF-007|Request: {email, PA1}; 200→AuthToken{accessToken, refreshToken, expiresIn, tokenType}; 401 invalid creds; 423 account locked; 429 rate limited; rate limit=10 req/min per IP; no auth required|M|P0|
|26|API-002|POST /auth/register|Registration NDP with email uniqueness + PA1 policy VLD.|THS, API Gateway|FR-AUTH-002, INF-007|Request: {email, PA1, displayName}; 201→SRP; 400 VLD (weak PA1/invalid email); 409 email conflict; rate limit=5 req/min per IP; no auth required|M|P0|
|27|API-003|GET /auth/me|Profile retrieval NDP; requires valid Bearer access token.|THS, API Gateway|FR-AUTH-004, INF-007|Bearer access token required; 200→SRP with id,email,displayName,createdAt,updatedAt,lastLoginAt,roles; 401 missing/expired/invalid; rate limit=60 req/min per user|S|P0|
|28|API-004|POST /auth/refresh|Token refresh NDP; rotates refresh token on success.|TKN, API Gateway|FR-AUTH-003, INF-007|Request: {refreshToken}; 200→new AuthToken pair (old revoked); 401 expired/revoked; rate limit=30 req/min per user; no access-token required|M|P0|
|29|API-005|POST /auth/reset-request|Password reset request NDP; always returns generic response.|THS, SND|FR-AUTH-005, INF-006|Request: {email}; 200 with generic confirmation regardless of email existence (prevents enumeration); 1h reset token issued when email matches; SND delivery triggered; rate limit=3 req/min per IP|S|P0|
|30|API-006|POST /auth/reset-confirm|Password reset confirmation NDP; validates reset token and updates hash.|THS, TKN|FR-AUTH-005|Request: {resetToken, newPassword}; 200 on PA1 update; 400 expired/used/invalid token; existing refresh tokens invalidated on success; new PA1 enforced by same policy as RGS|M|P0|
|31|API-007|Logout NDP POST /auth/logout|Expose COMP-011 logout handler via gateway with auth required.|THS, API Gateway|COMP-011|Bearer access token required; 204 on success; current refresh token revoked; subsequent refresh→401; PRD AUTH-E1 logout story satisfied|S|P1|
|32|CONTRACT-001|Error envelope standard|Define `{error: {code, message, status}}` envelope enforced across all auth endpoints.|API Gateway|—|all 4xx/5xx responses conform; `code` is stable machine-readable string; `message` is human-readable; `status` mirrors HTTP status; documented in OpenAPI|S|P0|
|33|CONTRACT-002|URL versioning `/v1/auth/*`|Prefix all endpoints with /v1; governance for non-breaking additive changes within v1.|API Gateway|—|all endpoints routed under /v1/auth/*; non-breaking additions permitted within v1; breaking changes require /v2; versioning documented in API README|S|P0|
|34|CONTRACT-003|Per-NDP rate limits at gateway|Configure rate-limit plugin values per API row above to mitigate R-002 brute force.|API Gateway|INF-002, INF-007|login=10/min/IP; register=5/min/IP; refresh=30/min/user; me=60/min/user; reset-request=3/min/IP; counters stored in Redis; 429 response on breach|M|P0|
|35|CONTRACT-004|TLS 1.3 + CORS allow-list enforcement|Enforce TLS 1.3 on all endpoints; CORS restricted to known frontend origins.|API Gateway|INF-007|TLS<1.3 rejected; HSTS max-age=63072000; CORS origin allow-list from config; Access-Control-Allow-Credentials=true for cookie-bound refresh path|S|P0|

### NTG Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Auth handler registry|Dispatch Table|API-001..007|M3|API Gateway routing layer|
|Rate-limit policy map|Registry|CONTRACT-003|M3|Gateway rate-limiter plugin|
|Error-envelope formatter middleware|Middleware Chain|CONTRACT-001|M3|All auth endpoints|
|Request VLD middleware|Middleware Chain|API-001..006|M3|All inbound request bodies|

### Milestone DPN — M3

- Depends on M2 (COMP-005..011 implemented and unit-tested).

### Open Questions — M3

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `THS` support API key authentication for service-to-service calls?|If yes, adds new API row (e.g. /auth/apikey) and new FR; currently deferred to v1.1. Confirms Sam's programmatic JTBD is satisfied by refresh-token path alone.|test-lead|2026-04-15|
|2|GAP-002|API deprecation policy not explicitly defined in TDD; needs governance doc.|Affects long-term API lifecycle and consumer migration; PRD expects stable contracts for Sam persona.|platform-team|2026-05-01|

## M4: Frontend NTG

**Objective:** Ship user-facing pages (`LoginPage`, `RegisterPage`, `ProfilePage`) and the `THP` context that orchestrates token storage, silent refresh, and 401 interception. | **Duration:** Weeks 7-8 | **Entry:** M3 API contracts frozen; OpenAPI spec published | **Exit:** All 4 frontend components integrated against staging API; E2E happy-path works; R-001 token-theft mitigations in place on client side.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|36|COMP-001|`LoginPage` frontend route|Render login form at /login; integrate with `THP` on submit.|LoginPage|API-001|props: onSuccess+redirectUrl; POSTs /auth/login; on 401 shows generic "Invalid email or PA1"; on 423 shows account-locked state; AuthToken stored via THP; Alex JTBD frictionless login satisfied|M|P1|
|37|COMP-002|`RegisterPage` frontend route|Render RGS form at /register with inline PA1 strength VLD.|RegisterPage|API-002|props: onSuccess+termsUrl; inline VLD (length, uppercase, digit) before submit; POST /auth/register; on 409 shows "email taken" with login/reset CTA; on 201 logs user in via THP; RGS <60s target (Alex JTBD)|M|P1|
|38|COMP-003|`ProfilePage` frontend route|Render authenticated profile page at /profile.|ProfilePage|API-003|auth-gated via THP; GET /auth/me on mount; displays id, email, displayName, createdAt, lastLoginAt, roles; redirects to LoginPage when 401 received|S|P1|
|39|COMP-004|`THP` React context|Manage AuthToken state, silent refresh timer, 401 axios interceptor, protected-route redirects.|THP|API-004, COMP-001..003|provides useAuth() hook; silent refresh 60s before expiry; 401 interceptor triggers refresh once, else redirect /login; clears state on tab close (sessionStorage); protected-route HOC wraps profile page|L|P1|
|40|FE-001|Client-side PA1 strength VLD|Implement NIST-aligned PA1 meter on `RegisterPage` before submit.|RegisterPage|COMP-002|meter updates on keystroke; blocks submit until min criteria met (≥8 chars, uppercase, number); messaging matches server policy to avoid double-rejection UX|S|P2|
|41|FE-002|Access token in-memory only (R-001 mitigation)|Store accessToken in JS memory only; never in localStorage/cookies.|THP|COMP-004|accessToken lives in THP state only; cleared on window.beforeunload; not readable by other tabs; R-001 mitigation verified via browser XSS test|S|P0|
|42|FE-003|HttpOnly SameSite=Strict cookie for refresh token (R-001 mitigation)|Refresh token transported as HttpOnly, SameSite=Strict, Secure cookie.|API Gateway, THP|INF-007, COMP-004|cookie attributes HttpOnly+Secure+SameSite=Strict; Path=/v1/auth/refresh; JS cannot read cookie; refresh NDP reads cookie not body for frontend path; R-001 mitigation verified|M|P0|
|43|FE-004|Password reset UI flows|Render reset-request and reset-confirm pages; integrate with APIs 005/006.|LoginPage, RegisterPage|API-005, API-006|/forgot-PA1 page POSTs reset-request and shows generic confirmation; /reset-PA1/:token page POSTs reset-confirm; success redirects to /login with toast; expired token shows resend CTA|M|P1|
|44|FE-005|Logout UI wire|Wire logout CTA in app header to COMP-011 handler and clear THP state.|THP|COMP-011, API-007|POST /auth/logout on click; clears THP state; redirects to landing; PRD AUTH-E1 logout story satisfied on shared-device scenario|S|P1|

### NTG Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|axios 401 interceptor|Middleware Chain|COMP-004|M4|All authenticated API calls in SPA|
|`THP` context|Dependency Injection|COMP-004|M4|ProfilePage, protected routes, logout CTA|
|Silent-refresh scheduler|Event Binding|COMP-004|M4|Token lifecycle (auto-refresh before 15min expiry)|
|Protected-route HOC|Strategy Pattern|COMP-004|M4|ProfilePage and future personalized pages|

### Milestone DPN — M4

- Depends on M3 (API contracts published and rate-limits configured).

### Open Questions — M4

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-004|Should we support "remember me" to extend session duration?|Changes refresh-token TTL or introduces secondary long-lived token; affects `THP` session semantics and Alex's multi-device UX.|Product|2026-05-10|

## M5: Security Hardening and Compliance

**Objective:** Enforce NFR-SEC and NFR-COMP controls end-to-end; deliver SOC2/GDPR/NIST evidence, account lockout, audit-log stream, admin query surface, and R-001/R-002 mitigations. | **Duration:** Weeks 9-10 | **Entry:** M2 services + M3 APIs functional; OQ-PRD-003 lockout policy confirmed | **Exit:** Security review sign-off (R-PRD-002); audit log queryable by admin (Jordan JTBD); pen-test scheduled; compliance evidence archived.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|45|NFR-SEC-001|bcrypt cost 12 enforcement|Enforce and verify `PSS` uses bcrypt cost 12 across all environments.|PSS|COMP-008|unit test asserts cost=12 from stored hash prefix; config override disallowed in prod; hash time >300ms on baseline hardware confirms cost; NIST SP 800-63B alignment documented|S|P0|
|46|NFR-SEC-002|RS256 + 2048-bit RSA + quarterly RTT|Enforce RS256 signing, 2048-bit keys, quarterly RTT with 1-week overlap.|JWT|COMP-007, INF-009|config test asserts RS256 and 2048-bit; RTT runbook tested in staging; overlap window=1 week prior+after; JWKS publishes current+next keys; old tokens accepted until TTL|M|P0|
|47|NFR-COMP-001|GDPR consent at RGS|Capture explicit consent checkbox at RGS; persist consent record with timestamp.|THS, UserRepo|FR-AUTH-002|consent column added to SRP or consent_log table; consent_given=true+consent_timestamp persisted; RGS rejected without consent; evidence exported for audit|M|P0|
|48|NFR-COMP-002|SOC2 Type II audit logging|Emit structured audit events for all auth flows with user ID, timestamp, IP, outcome; retain 12 months.|THS, API Gateway|DM-001|events: login_success/login_failure/register/logout/refresh/reset_request/reset_confirm/lock; fields=user_id,timestamp,ip,outcome,reason; 12-month PST retention; immutable append-only|L|P0|
|49|NFR-COMP-003|NIST SP 800-63B PA1 storage alignment|Validate one-way adaptive hashing, no plaintext persistence, no PA1 field in logs.|PSS, Logger|NFR-SEC-001, NFR-COMP-002|static analysis confirms no log statement references PA1 field; audit log sanitizer redacts PA1/token keys; NIST SP 800-63B checklist attached to release evidence|M|P0|
|50|NFR-COMP-004|GDPR data minimization|Limit collected PII to email, hashed PA1, display name; documented data-flow diagram.|UserRepo, THS|DM-001|DM-001 columns audited: no additional PII; data-flow diagram published in /docs; DPO sign-off attached; PRD data-minimization requirement verified|S|P0|
|51|SEC-001|Account lockout after 5/15min (FA0 AC4)|Track failed login attempts per email; lock account after 5 failures within 15-minute window.|THS, Redis 7|FA0, INF-002, OQ-PRD-003|sliding window in Redis; 5th failure→lock; lockout TTL=configurable (default 15min); 423 returned during lockout; unlock on successful reset; audit event lock_triggered emitted|M|P0|
|52|SEC-002|Refresh token hashed in Redis (R-001 mitigation)|Store SHA-256 hash of refresh token in Redis, not plaintext; compare hashes on refresh.|TKN|COMP-006, DM-002|Redis stores hex(sha256(token)); plaintext never persisted server-side; unit test asserts no plaintext in any persistent store; R-001 blast radius reduced (read-only DB dump does not yield usable tokens)|S|P0|
|53|SEC-003|Generic error messages + timing equalization|All auth errors return generic messages; equalize timing across valid/invalid email paths to prevent enumeration.|THS|FA0, FR-AUTH-005|timing variance <10ms between valid and invalid email on login and reset-request; error envelope always returns same code for 401; security review approves anti-enumeration posture|M|P0|
|54|COMP-012|Admin audit log query NDP (Jordan JTBD gap fill)|Build admin-only NDP to query audit log by date range and user — addresses Jordan Platform Admin JTBD gap.|THS, API Gateway|NFR-COMP-002|GET /v1/admin/auth-events with admin role required; filters: user_id, date_range, event_type; paginated; 403 for non-admin; audit trail for admin queries themselves; PRD user story "Jordan admin audit view" satisfied|L|P1|

### NTG Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Audit event bus|Event Binding|NFR-COMP-002|M5|Login/register/refresh/reset/logout handlers; admin query NDP|
|Rate-limit + lockout counter store|Registry|SEC-001|M5|THS login handler; lockout-unlock on reset|
|Log sanitizer middleware|Middleware Chain|NFR-COMP-003|M5|All application log emitters|
|Consent capture validator|Middleware Chain|NFR-COMP-001|M5|Register handler pre-persistence|

### Milestone DPN — M5

- Depends on M2 (services) and M3 (API surface and gateway policies).

### Open Questions — M5

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-003|Account lockout policy after N consecutive failed attempts?|TDD FA0 specifies 5/15min; PRD requests confirmation. Determines SEC-001 parameters.|Security|2026-04-25|
|2|GAP-003|Admin audit query NDP COMP-012 added to cover Jordan JTBD "see who attempted access and lock compromised accounts"; TDD has no corresponding FR.|PRD requires; TDD should be updated with FR-AUTH-ADMIN for admin surface.|security-team|2026-05-05|

## M6: Quality Assurance and Performance Validation

**Objective:** Stand up the 80/15/5 test pyramid, validate NFR-PERF/REL, benchmark hashing, and certify the release candidate against all success criteria before rollout. | **Duration:** Weeks 11-12 | **Entry:** M4 frontend and M5 security complete; staging environment populated | **Exit:** Unit coverage ≥80%; p95 login <200ms; 500-concurrent load test passes; all TEST-001..006 green; NFR-REL health check active.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|55|TEST-001|Unit: login valid creds returns AuthToken|Jest unit test mocks PSS+TKN; asserts THS.login() returns AuthToken.|THS|COMP-005|valid email+PA1→PSS.verify() then TKN.issueTokens(); returns AuthToken; mocks verified called once; FA0 validated|S|P0|
|56|TEST-002|Unit: login invalid creds returns error|Jest unit test asserts 401 and no token issued on invalid creds.|THS|COMP-005|invalid creds→401 error; TKN.issueTokens() never called; FA0 negative path validated|S|P0|
|57|TEST-003|Unit: token refresh with valid refresh token|Jest unit test covers TKN.refresh() happy path with RTT.|TKN|COMP-006|valid refresh→old revoked, new pair issued via JWT.sign(); Redis record rotated; FR-AUTH-003 validated|S|P0|
|58|TEST-004|NTG: RGS persists SRP to DB|Supertest+testcontainers IN1: full POST /auth/register→PSS→PG insert.|THS, PST 15|COMP-005, COMP-009|testcontainer PG spun up; real bcrypt hash persisted; UNIQUE constraint verified; FR-AUTH-002 end-to-end validated|M|P0|
|59|TEST-005|NTG: expired refresh token rejected|Supertest+testcontainers IN1: assert Redis-stored refresh token expiration path.|TKN, Redis 7|COMP-006|Redis TTL advanced; refresh attempt→401 with expired-token code; audit event emitted; FR-AUTH-003 negative path validated|M|P0|
|60|TEST-006|E2E: user registers and logs in|Playwright E2E flow exercises RegisterPage→LoginPage→ProfilePage through THP.|Playwright|COMP-001..004|new email registers, session persists, profile displays; re-login after logout succeeds; FA0+002 and PRD AUTH-E1 Alex journey validated|M|P0|
|61|NFR-PERF-001|APM VLD: login p95 <200ms|Instrument THS.login() with OpenTelemetry; validate p95 against target on staging.|THS, APM|OPS-007|OpenTelemetry span per login call; Grafana dashboard shows p95; 7-day window <200ms; regression gate in CI on staging load|M|P0|
|62|NFR-PERF-002|Load test: 500 concurrent logins (k6)|Run k6 load test scenario sustaining 500 concurrent logins; verify error rate + latency.|k6|INF-008, NFR-PERF-001|k6 scenario 500 VUs × 10min; error rate <0.1%; p95 <200ms; HPA scales pods appropriately; results archived|M|P0|
|63|NFR-REL-001|Health check NDP + uptime monitoring|Expose /healthz for K8s readiness/liveness; wire external uptime monitor with 30-day rolling window.|THS, Kubernetes|INF-008|/healthz returns 200 when PG+Redis reachable; K8s readiness probe wired; external uptime monitor (Pingdom/StatusCake) probes every 60s; 99.9% availability dashboard|M|P0|
|64|TEST-007|Password hash time benchmark <500ms|Micro-benchmark asserts bcrypt cost 12 hash completes <500ms on target hardware profile.|PSS|COMP-008|benchmark harness; p95 hash time <500ms on baseline; CI gate fails if regression >20%; NIST SP 800-63B success criterion validated|S|P0|
|65|TEST-008|Jest unit harness + coverage gate|Stand up Jest+ts-jest harness; configure coverage gate ≥80% statements on backend modules.|Jest|COMP-005..009|jest config with ts-jest; coverage collects from src/**; gate at 80% statements/75% branches; CI fails below threshold|S|P0|
|66|TEST-009|Playwright E2E harness|Configure Playwright with multi-browser runners and CI IN1.|Playwright|—|chromium+firefox+webkit runners; CI step runs against staging; screenshots+videos retained on failure; flake rate <1%|S|P1|
|67|TEST-010|testcontainers IN1 harness|Wire testcontainers to spin up PG15 + Redis7 per IN1-test run.|testcontainers|INF-001, INF-002|PG+Redis containers started per test suite; isolated networks; teardown on suite complete; CI parallelism=4|M|P0|

### NTG Points — M6

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Jest test harness|Registry|TEST-008|M6|All unit test files; CI coverage gate|
|testcontainers factory|Dependency Injection|TEST-010|M6|NTG tests for PG and Redis flows|
|Playwright config|Registry|TEST-009|M6|E2E flows and future UI regression tests|
|k6 load-test registry|Registry|NFR-PERF-002|M6|CI performance gate; pre-rollout VLD|

### Milestone DPN — M6

- Depends on M4 (frontend available for E2E) and M5 (security controls testable).

## M7: Migration and Phased Rollout

**Objective:** Execute three-phase feature-flagged rollout from legacy auth to the new service with documented rollback playbook and data-migration safeguards. | **Duration:** Weeks 13-16 | **Entry:** M6 quality gate passed; security sign-off; legacy data backup verified | **Exit:** MIG-003 GA at 100% traffic; legacy endpoints deprecated; `AUTH_NEW_LOGIN` flag cleaned up; 7-day post-GA dashboards green (99.9% uptime).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|68|MIG-004|Feature flag `AUTH_NEW_LOGIN` scaffolding|Create flag and routing logic to gate new LoginPage + THS login NDP; default OFF.|Feature-flag service|COMP-005, COMP-001|flag registered with default=OFF; routing splits traffic at API Gateway; AT owns; cleanup tagged for post-Phase-3|S|P0|
|69|MIG-005|Feature flag `AUTH_TOKEN_REFRESH` scaffolding|Create flag to enable refresh-token flow in TKN; default OFF (access-only until enabled).|Feature-flag service|COMP-006|flag registered default=OFF; when OFF TKN issues access-only response; when ON full refresh flow enabled; cleanup tagged Phase-3 + 2 weeks|S|P0|
|70|MIG-001|Phase 1: Internal Alpha (1 week)|Deploy to staging; AT+QA validate all endpoints; LoginPage+RegisterPage behind flag for internal accounts only.|THS, Kubernetes|MIG-004, MIG-005, TEST-*|all FA0..005 pass manual QA; zero P0/P1 bugs; flag ON for internal email domain allow-list; exit criteria archived|M|P0|
|71|MIG-002|Phase 2: Beta at 10% traffic (2 weeks)|Enable `AUTH_NEW_LOGIN` for 10% of production traffic; monitor latency, errors, Redis usage.|Feature-flag service, APM|MIG-001, NFR-PERF-001|10% traffic on new path; p95 <200ms sustained; error rate <0.1%; zero Redis connection failures; rollback rehearsal performed; exit criteria archived|L|P0|
|72|MIG-003|Phase 3: GA at 100% traffic (1 week)|Enable `AUTH_NEW_LOGIN` for 100%; deprecate legacy endpoints; enable `AUTH_TOKEN_REFRESH`.|Feature-flag service, API Gateway|MIG-002|100% traffic on new path; legacy endpoints return deprecation header and 410 after cutover; all dashboards green first 7 days; 99.9% uptime confirmed|M|P0|
|73|MIG-006|Rollback step 1: disable `AUTH_NEW_LOGIN`|Runbook step 1 — flip flag OFF to immediately route traffic back to legacy auth.|Feature-flag service|MIG-004|one-click flag flip; propagation <60s; no pod restart required; runbook validated in staging rehearsal|S|P0|
|74|MIG-007|Rollback step 2: smoke test legacy login|Runbook step 2 — execute smoke-test suite against legacy auth to verify it remains healthy.|Legacy auth|MIG-006|smoke suite ≤5 min; covers login, logout, profile; pass/fail captured in incident ticket|S|P0|
|75|MIG-008|Rollback step 3: root-cause `THS` failure|Runbook step 3 — triage logs, traces, and metrics to identify root cause.|APM, Logger|MIG-007|structured-log query bundle prepared; on-call consults OPS-001/002 runbooks; root cause captured within 4h|M|P0|
|76|MIG-009|Rollback step 4: restore `SRP` from backup|Runbook step 4 — if corruption detected, restore from last known-good PG backup.|PST 15|INF-001|PITR target chosen; restore verified against checksum; downtime window communicated; integrity verified before re-enabling traffic|M|P0|
|77|MIG-010|Rollback step 5: notify AT + platform-team|Runbook step 5 — open incident channel and page both teams per escalation policy.|Incident comms|—|incident channel created; both teams paged; status page updated; comms cadence 30min during incident|S|P0|
|78|MIG-011|Rollback step 6: post-mortem within 48h|Runbook step 6 — schedule blameless post-mortem; document corrective actions.|—|MIG-010|post-mortem scheduled ≤48h from resolution; corrective actions tracked in backlog; linked to R-003/R-PRD-002 mitigation evidence|S|P0|

### NTG Points — M7

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Feature flag registry|Registry|MIG-004, MIG-005|M7|API Gateway routing; TKN refresh path|
|Rollback playbook runbook|Registry|MIG-006..011|M7|On-call operators; incident response|
|Legacy-to-new parallel-run adapter|Middleware Chain|MIG-001..003|M7|Data migration safety net during Phases 1-2|
|Deprecation-header middleware|Middleware Chain|MIG-003|M7|Legacy endpoints post-GA|

### Milestone DPN — M7

- Depends on M6 (quality gate) and security review completion in M5.

## M8: Operational Readiness

**Objective:** Finalize runbooks, capacity plans, metrics, alerts, and structured logging for 24/7 AT ownership post-GA. | **Duration:** Weeks 17-18 | **Entry:** M7 GA complete | **Exit:** Grafana dashboards and alerts live; on-call RTT handed over; runbooks rehearsed; SOC2 evidence package archived.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|79|OPS-001|Runbook — `THS` down|Author and rehearse runbook for total `THS` outage scenario.|Runbook|MIG-003|symptoms documented (5xx on /auth/*); diagnosis steps: K8s pod health, PG connectivity, init logs; resolution: restart pods / PG failover / Redis-down fallback forces re-login; escalation: AT on-call → platform-team at 15min|M|P0|
|80|OPS-002|Runbook — token refresh failures|Author and rehearse runbook for refresh-token failure surge scenario.|Runbook|MIG-003|symptoms documented (unexpected logouts, 401 spike); diagnosis: Redis from TKN, JWT signing-key availability, AUTH_TOKEN_REFRESH state; resolution: scale Redis/re-mount secrets/re-enable flag; escalation chain documented|M|P0|
|81|OPS-003|On-call RTT + tooling|Set up 24/7 AT RTT with PagerDuty; pre-provision Kubernetes/Grafana/Redis-CLI/PG-admin access.|PagerDuty|—|P1 ack <15 min; 24/7 AT RTT for first 2 weeks post-GA; tooling access verified for all RTT members; escalation path: on-call→test-lead→eng-manager→platform-team|M|P0|
|82|OPS-004|Capacity plan — `THS` pods (HPA)|Finalize HPA policy: 3 replica baseline, scale to 10 on CPU >70% for 500 concurrent users.|Kubernetes|INF-008, NFR-PERF-002|HPA configured min=3 max=10; target CPU=70%; scale-up cooldown 60s; scale-down cooldown 300s; capacity validated in k6 load test|S|P0|
|83|OPS-005|Capacity plan — PST connections|Monitor pool utilization; scale trigger to 200 when wait time >50ms.|PST 15|INF-001, INF-010|alert rule: pool-wait-p95 >50ms over 10min → scale pool to 200; runbook documents scaling steps; 50 avg concurrent queries baseline established|S|P0|
|84|OPS-006|Capacity plan — Redis memory|Provision 1GB baseline for ~100K refresh tokens (~50MB); scale to 2GB when >70% utilized.|Redis 7|INF-002|alert rule: redis-memory-used >70% over 10min → manual scale to 2GB; eviction policy=noeviction to protect token keys; monitor documented|S|P0|
|85|OPS-007|Metrics + tracing stack (Prometheus + OpenTelemetry)|Instrument `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`; OpenTelemetry spans across THS, PSS, TKN, JWT.|Prometheus, OpenTelemetry|COMP-005..009|all 4 metrics emitted; histogram buckets aligned for p50/p95/p99; OpenTelemetry traces propagate from API Gateway through THS into PG/Redis; Grafana dashboards published|M|P0|
|86|OPS-008|Alert — login failure rate >20%|Configure Prometheus alert firing when login failure rate exceeds 20% over 5 minutes.|Prometheus|OPS-007|alert expr=rate(auth_login_failed_total[5m])/rate(auth_login_total[5m])>0.2; severity=P1; routes to AT on-call; annotation links to OPS-001 runbook|S|P0|
|87|OPS-009|Alert — p95 latency >500ms|Configure alert for sustained login latency regression.|Prometheus|OPS-007|alert expr=histogram_quantile(0.95, auth_login_duration_seconds)>0.5 for 5m; severity=P2; routes to AT on-call; links to OPS-001 runbook|S|P0|
|88|OPS-010|Alert — `TKN` Redis connection failures|Configure alert on TKN Redis connection errors surpassing threshold.|Prometheus|OPS-007|alert expr=rate(tokenmanager_redis_errors_total[5m])>0; severity=P1; routes to AT on-call; links to OPS-002 runbook|S|P0|
|89|LOG-001|Structured logging + sensitive-field redaction|Emit structured (JSON) logs for login/register/refresh/reset events; redact PA1/token fields; 12-month retention per NFR-COMP-002.|Logger|NFR-COMP-002, NFR-COMP-003|all event logs JSON; redact list covers PA1, accessToken, refreshToken, resetToken; 12-month retention in centralized log store; static-analysis gate fails build if new log statements reference redact-listed fields|M|P0|

### NTG Points — M8

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Alert routing rules|Registry|OPS-008..010|M8|PagerDuty AT service|
|Runbook registry|Registry|OPS-001..002|M8|On-call operators; incident response|
|Log redact-list|Registry|LOG-001|M8|All application log emitters; CI static-analysis gate|
|Metric registry|Registry|OPS-007|M8|Grafana dashboards; SLO tooling; capacity planning|

### Milestone DPN — M8

- Depends on M7 (GA complete) so that production signal informs capacity tuning.

## Risk Assessment and Mitigation

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS enabling session hijacking|High|Medium|Session hijacking; unauthorized access to user data; PII exposure; compliance breach|accessToken memory-only (FE-002); HttpOnly+SameSite=Strict cookie for refresh (FE-003); 15-min access TTL; refresh hashed in Redis (SEC-002); THP clears state on tab close. Contingency: TKN mass-revocation + forced PA1 reset|security-team|
|2|R-002 Brute-force attacks on login|Medium|High|Account compromise; service degradation from auth volume; reputational harm|API Gateway 10 req/min/IP limit (CONTRACT-003); 5-attempt lockout in 15-min window (SEC-001); bcrypt cost 12 raises attack cost (NFR-SEC-001). Contingency: WAF IP blocking + CAPTCHA on LoginPage|security-team|
|3|R-003 Data loss during migration from legacy auth|High|Low|User data corruption; inability to restore credentials; GDPR incident|Parallel-run in Phases 1-2 (MIG-001/002); idempotent upsert semantics; pre-phase PG backups + PITR (INF-001); rollback step MIG-009 restores from backup. Contingency: full rollback to legacy via MIG-006|AT|
|4|R-PRD-001 Low RGS adoption due to poor UX|High|Medium|Misses >60% conversion target; delays personalization rollout ROI|Usability testing pre-Phase-1 on LoginPage/RegisterPage; RGS-funnel instrumentation (OPS-007); iterate between Phase 1 and Phase 2|product-team|
|5|R-PRD-002 Security breach from implementation flaws|Critical|Low|Breach of all user credentials; SOC2 audit failure; loss of enterprise deals|Dedicated security review gate in M5; third-party penetration test before MIG-003 GA; static analysis + dependency scanning in CI; secrets management for all key material|security-team|
|6|R-PRD-003 Compliance failure from incomplete audit logging|High|Medium|SOC2 Type II audit failure in Q3 2026; enterprise customer churn|NFR-COMP-002 defines events and retention early; QA validates against SOC2 controls in M6; 12-month retention enforced in LOG-001; admin query surface (COMP-012) enables auditor access|compliance-team|
|7|R-PRD-004 Email delivery failures blocking PA1 reset|Medium|Medium|Users cannot recover access; support ticket volume rises; missed >80% reset completion target|SND delivery webhook monitored (OPS-007); alert on bounce/defer rate; support-channel fallback documented; OQ-PRD-001 resolution drives sync vs async architecture|AT|

## Resource Requirements and DPN

### External DPN

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PST 15+ cluster|M1|Available|Use existing platform PG cluster with dedicated `auth` schema if new cluster delayed|
|Redis 7+ cluster|M1|Available|Use existing platform Redis with dedicated keyspace if new cluster delayed|
|SND API (email delivery)|M2|Available|Ses/Mailgun backup provider; if both fail, degrade PA1-reset to support-ticket flow|
|bcryptjs library|M1|Available|No practical fallback — bcrypt is the mandated algorithm|
|jsonwebtoken library|M1|Available|node-jose as alternative RS256 implementation|
|API Gateway|M1|Available|Kubernetes Ingress + per-service rate-limit middleware as minimal fallback|
|Kubernetes cluster|M1|Available|Existing platform K8s; no alternative orchestrator approved|
|Node.js 20 LTS runtime|M1|Available|Node 18 LTS acceptable only for emergency rollback|
|Frontend routing framework (React)|M4|Available|Blocks COMP-001..004 if unavailable; no fallback|

### Infrastructure Requirements

- PST 15+ primary with 1 read replica, pg-pool 100 connections, daily backups + PITR, dedicated `auth` schema; 12-month audit-log retention capacity.
- Redis 7+ cluster with 1GB baseline memory, AOF persistence, failover enabled, eviction policy=`noeviction` for token keys.
- Kubernetes cluster with HPA enabled (3-10 replica range for `THS`), secrets mount for RS256 private key + SND API key.
- API Gateway capable of per-NDP rate limits, CORS allow-list, TLS 1.3 termination, HSTS, and deprecation-header middleware.
- Prometheus + Grafana + OpenTelemetry collector + PagerDuty IN1 for observability and alerting.
- Centralized log store with 12-month retention and field-level redaction for SOC2 Type II (NFR-COMP-002).
- SND tenant with sending domain configured (SPF/DKIM/DMARC) and webhook NDP for delivery status.

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login latency|`auth_login_duration_seconds` p95|<200ms|APM histogram on staging and production; CI gate on staging load test|M6|
|Registration success rate|successful / attempted registrations|>99%|Funnel analysis via `auth_registration_total` + error counters|M6|
|Token refresh latency|TKN.refresh() p95|<100ms|APM on TKN spans|M6|
|Service availability|Uptime over 30-day rolling window|99.9%|External uptime monitor probing /healthz every 60s|M8|
|Password hash time|bcrypt cost-12 hash duration p95|<500ms|Micro-benchmark TEST-007; CI regression gate|M6|
|Registration conversion|landing → confirmed account|>60%|PRD funnel analytics; Alex persona target|M7|
|Daily active authenticated users|count of unique users issued AuthToken per day|>1000 within 30 days of GA|`auth_login_total` distinct-user aggregation|M8|
|Average session duration|time between login and refresh-expiry events|>30 minutes|Token-refresh analytics|M8|
|Failed login rate|failed / total login attempts|<5%|Audit-event log analysis; alert at >20% (OPS-008)|M8|
|Password reset completion|reset-requested → new-PA1-set|>80%|Funnel via audit events reset_request + reset_confirm|M8|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Authentication paradigm|Stateless JWT (RS256) + opaque refresh|Server-side sessions; Auth0/Firebase third-party IdP|TDD architectural constraints mandate JWT; Sam's JTBD for programmatic auth (PRD) requires token-based flow; self-hosted avoids third-party dependency rejected in constraints|
|Password hashing|bcrypt cost 12 via `PSS` abstraction|argon2id; pbkdf2|NFR-SEC-001 mandates bcrypt cost 12; NIST SP 800-63B compliant; cost=12 yields hash time <500ms target (TEST-007) on baseline hardware|
|Refresh-token storage|Hashed in Redis, 7-day TTL|Plaintext in Redis; DB-only storage|DM-002 mandates Redis TTL; SEC-002 hashing reduces R-001 blast radius; 7-day TTL from FR-AUTH-003|
|Rollout strategy|Three-phase feature-flagged (Alpha/Beta/GA)|Big-bang cutover; canary on single pod|R-003 severity=High justifies parallel-run; MIG-001..003 provides rollback points; matches TDD migration plan explicitly|
|Admin audit surface|Dedicated `/v1/admin/auth-events` NDP (COMP-012)|Direct DB access for admins; external log UI only|Jordan JTBD requires queryable audit trail; SOC2 auditor needs self-service query; direct DB access rejected on security grounds|
|Password reset delivery|Email via SND with 1h token|SMS; in-app only|PRD constraint (email/PA1 only) + TDD FR-AUTH-005; SND already provisioned as external dep; 1h TTL balances security and UX|
|API versioning|URL prefix `/v1/auth/*`|Header-based versioning; query-param version|TDD architectural constraint mandates URL-versioned; simplest consumer IN1 for Sam persona; non-breaking additive changes supported within v1|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|DM-001/DM-002 finalized; PG15 + Redis 7 provisioned; RS256 keys generated; SND tenant active|
|M2|2 weeks|Week 3|Week 4|COMP-005..009 unit-tested; FA0..005 green in unit tests; COMP-011 logout handler delivered|
|M3|2 weeks|Week 5|Week 6|API-001..006 + API-007 contract-tested; error envelope + rate limits + TLS enforced|
|M4|2 weeks|Week 7|Week 8|LoginPage/RegisterPage/ProfilePage/THP integrated; R-001 client mitigations in place|
|M5|2 weeks|Week 9|Week 10|NFR-SEC + NFR-COMP controls enforced; admin audit surface (COMP-012) delivered; security review sign-off|
|M6|2 weeks|Week 11|Week 12|TEST-001..010 pass; k6 500-concurrent validated; p95 <200ms confirmed; health-check wired|
|M7|4 weeks|Week 13|Week 16|MIG-001 Alpha (Week 13); MIG-002 Beta 10% (Weeks 14-15); MIG-003 GA 100% (Week 16)|
|M8|2 weeks|Week 17|Week 18|Runbooks rehearsed; PagerDuty RTT live; Grafana dashboards published; SOC2 evidence archived|

**Total estimated duration:** 18 weeks (Q2 2026 start aligns with PRD target release v1.0).
