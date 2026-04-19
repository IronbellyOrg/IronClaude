---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-19T00:00:00Z
generator: requirements-design-extractor
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.72
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, compliance]
risks_identified: 7
dependencies_identified: 9
success_criteria_count: 11
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 8
test_artifacts_identified: 6
migration_items_identified: 7
operational_items_identified: 10
pipeline_diagnostics: {elapsed_seconds: 165.0, started_at: "2026-04-19T14:46:56.337246+00:00", finished_at: "2026-04-19T14:49:41.359573+00:00"}
---

## Functional Requirements

### FR-AUTH-001
**Login with email and password.** `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
**Acceptance Criteria:**
1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
2. Invalid credentials return 401 with error message.
3. Non-existent email returns 401 (no user enumeration).
4. Account locked after 5 failed attempts within 15 minutes.
**Source:** TDD §5.1; PRD FR-AUTH.1.

### FR-AUTH-002
**User registration with validation.** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
**Acceptance Criteria:**
1. Valid registration returns 201 with `UserProfile` data.
2. Duplicate email returns 409 Conflict.
3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
4. `PasswordHasher` stores bcrypt hash with cost factor 12.
**Source:** TDD §5.1; PRD FR-AUTH.2.

### FR-AUTH-003
**JWT token issuance and refresh.** `TokenManager` must issue JWT access tokens (15-min expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
**Acceptance Criteria:**
1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
3. Expired refreshToken returns 401.
4. Revoked refreshToken returns 401.
**Source:** TDD §5.1; PRD FR-AUTH.3.

### FR-AUTH-004
**User profile retrieval.** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
**Acceptance Criteria:**
1. GET `/auth/me` with valid accessToken returns `UserProfile`.
2. Expired or invalid token returns 401.
3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
**Source:** TDD §5.1; PRD FR-AUTH.4.

### FR-AUTH-005
**Password reset flow.** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
**Acceptance Criteria:**
1. POST `/auth/reset-request` with valid email sends reset token via email.
2. POST `/auth/reset-confirm` with valid token updates the password hash.
3. Reset tokens expire after 1 hour.
4. Used reset tokens cannot be reused.
**Source:** TDD §5.1; PRD FR-AUTH.5.

## Non-Functional Requirements

### NFR-PERF-001
**API response time.** All auth endpoints must respond in < 200ms at p95. Measured via APM tracing on `AuthService` methods. Source: TDD §5.2; PRD NFR-AUTH.1.

### NFR-PERF-002
**Concurrent authentication.** Support 500 concurrent login requests. Measured via k6 load testing. Source: TDD §5.2; PRD NFR-AUTH.1.

### NFR-REL-001
**Service availability.** 99.9% uptime measured over 30-day rolling windows. Uptime monitoring via health check endpoint. Source: TDD §5.2; PRD NFR-AUTH.2.

### NFR-SEC-001
**Password hashing.** `PasswordHasher` must use bcrypt with cost factor 12. Unit test asserts bcrypt cost parameter. Source: TDD §5.2.

### NFR-SEC-002
**Token signing.** `JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Configuration validation test. Source: TDD §5.2.

### NFR-COMP-001
**GDPR consent at registration.** Users must consent to data collection at registration; consent recorded with timestamp. Source: PRD Legal & Compliance.

### NFR-COMP-002
**SOC2 Type II audit logging.** All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention. Source: PRD Legal & Compliance; TDD §7.2 (audit log retention 90 days conflicts with PRD 12-month — flagged in Open Questions).

### NFR-COMP-003
**NIST SP 800-63B password storage.** One-way adaptive hashing; raw passwords never persisted or logged. Implemented via `PasswordHasher`. Source: PRD Legal & Compliance.

### NFR-COMP-004
**GDPR data minimization.** Only email, hashed password, and display name collected. No additional PII required. Source: PRD Legal & Compliance.

## Complexity Assessment
**complexity_score:** 0.72
**complexity_class:** HIGH
**Rationale:** Multi-component backend service (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`) plus three frontend surfaces (`LoginPage`, `RegisterPage`, `AuthProvider`). Cross-team coordination (auth-team, platform-team, frontend-team). Security-critical domain with bcrypt, RS256 JWT, rate limiting, account lockout. Phased rollout with two feature flags, rollback procedure, and data-migration concerns. Compliance-bound (SOC2, GDPR, NIST). 5 FRs, 9 NFRs, 6 API endpoints, 2 data entities, 7 risks, 3-phase migration. Score elevated by security-critical nature and compliance deadline pressure but moderated by well-defined stateless architecture and mature library choices.

## Architectural Constraints
- **Runtime/stack mandates:** Node.js 20 LTS, PostgreSQL 15+, Redis 7+.
- **Cryptographic mandates:** bcrypt cost factor 12 (`PasswordHasher`); RS256 with 2048-bit RSA keys, rotated quarterly (`JwtService`).
- **Session model:** Stateless JWT with refresh tokens; no server-side session state beyond Redis refresh-token records.
- **Access token TTL:** 15 minutes. **Refresh token TTL:** 7 days. **Password reset token TTL:** 1 hour, single-use.
- **Transport:** TLS 1.3 on all endpoints; CORS restricted to known frontend origins.
- **API versioning:** URL prefix `/v1/auth/*`; breaking changes require new major version.
- **Rate limiting:** Enforced at API Gateway before reaching `AuthService` (per endpoint in §8.1).
- **Error semantics:** Generic 401 on login failure (no user enumeration); password-reset success response identical for registered/unregistered emails.
- **Integration boundaries:** API Gateway → `AuthService` (HTTP/REST JSON); `AuthService` → PostgreSQL (pg-pool); `TokenManager` → Redis (RESP); `AuthService` → SendGrid (SMTP/API).
- **Deferred scope:** No OAuth/social login, no MFA, no RBAC enforcement in v1.0 (roles field present but not enforced).
- **Persona-driven design (PRD):** Must serve Alex (end user — fast self-service), Jordan (admin — visibility/audit), Sam (API consumer — programmatic refresh, stable contracts).
- **Compliance windows:** Q3 2026 SOC2 Type II audit deadline drives audit-logging design.

## Risk Inventory
1. **R-001 (High severity).** Token theft via XSS allows session hijacking. Mitigation: accessToken in memory only; refreshToken in HttpOnly cookie; 15-min access TTL; `AuthProvider` clears tokens on tab close. Contingency: `TokenManager` revocation + forced password reset.
2. **R-002 (Medium severity).** Brute-force attacks on login endpoint. Mitigation: API Gateway rate limit 10 req/min/IP; account lockout after 5 failures; bcrypt cost 12. Contingency: WAF IP blocks; CAPTCHA on `LoginPage` after 3 failures.
3. **R-003 (High severity).** Data loss during migration from legacy auth. Mitigation: parallel-run through Phase 1-2; idempotent upserts; full DB backup before each phase. Contingency: rollback + restore from pre-migration backup.
4. **R-004 (Medium severity, PRD business).** Low registration adoption due to poor UX. Mitigation: usability testing pre-launch; iterate on funnel data.
5. **R-005 (Medium severity, PRD operational).** Compliance failure from incomplete audit logging. Mitigation: define log requirements early; validate against SOC2 controls in QA.
6. **R-006 (Low severity, PRD operational).** Email delivery failures blocking password reset. Mitigation: SendGrid delivery monitoring and alerting; fallback support channel.
7. **R-007 (Low severity).** Redis unavailability impairing `TokenManager`. Mitigation: fail-closed on refresh (reject rather than serve stale tokens); users re-login via `LoginPage`.

## Dependency Inventory
1. **PostgreSQL 15+** — `UserProfile` persistence and audit log storage.
2. **Redis 7+** — `TokenManager` refresh-token storage with 7-day TTL.
3. **Node.js 20 LTS** — service runtime.
4. **bcryptjs** — used by `PasswordHasher`.
5. **jsonwebtoken** — used by `JwtService`.
6. **SendGrid** (external SMTP/API) — password reset emails.
7. **API Gateway** — rate limiting and CORS enforcement in front of `AuthService`.
8. **SEC-POLICY-001** — password/token policy authority.
9. **INFRA-DB-001** — database provisioning dependency (from TDD frontmatter `depends_on`).

## Success Criteria
- Login response p95 < 200ms (APM on `AuthService.login()`).
- Registration success rate > 99% (successful vs. attempted).
- Token refresh p95 < 100ms (APM on `TokenManager.refresh()`).
- Service availability 99.9% over 30-day rolling windows.
- `PasswordHasher.hash()` < 500ms at bcrypt cost 12.
- Registration conversion > 60% (funnel `RegisterPage` → confirmed account).
- DAU > 1000 within 30 days of GA (`AuthToken` issuance counts).
- Average session duration > 30 minutes (refresh-event analytics) — PRD.
- Failed login rate < 5% of attempts — PRD.
- Password reset completion > 80% (funnel reset-requested → new-password-set) — PRD.
- Unit coverage for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher` > 80% (Release Criteria §24).

## Open Questions
- **OQ-001.** Should `AuthService` support API key authentication for service-to-service calls? (Owner: test-lead; target 2026-04-15.)
- **OQ-002.** Maximum allowed `UserProfile.roles` array length? (Owner: auth-team; target 2026-04-01.)
- **OQ-003 (PRD).** Password-reset emails sent synchronously or asynchronously? (Owner: Engineering.)
- **OQ-004 (PRD).** Maximum refresh tokens per user across devices? (Owner: Product.) Relates to `TokenManager` Redis capacity planning.
- **OQ-005 (PRD).** Account-lockout policy after N consecutive failures — aligned with TDD's 5/15-min rule, but needs Security sign-off. (Owner: Security.)
- **OQ-006 (PRD).** Should "remember me" be supported to extend session duration? (Owner: Product.)
- **OQ-007 (conflict).** Audit-log retention: TDD §7.2 states 90 days; PRD Legal & Compliance states 12 months for SOC2. PRD wins on business intent — retention target should be 12 months. Requires TDD update.
- **OQ-008 (JTBD coverage).** PRD JTBD "log out to secure session on shared device" is implicit in `AuthProvider` but no explicit FR in TDD for logout/token revocation endpoint. Consider adding FR-AUTH-006 (logout / refresh-token revocation).
- **OQ-009 (JTBD coverage).** PRD Jordan persona JTBD "view auth event logs to investigate incidents" has no corresponding FR in TDD; audit-log query capability is unspecified.

## Data Models and Interfaces

### DM-001 — `UserProfile`
**Storage:** PostgreSQL 15 (indefinite retention).
**Interface:**
```ts
interface UserProfile {
  id: string; email: string; displayName: string;
  createdAt: string; updatedAt: string;
  lastLoginAt: string; roles: string[];
}
```
**Fields:**
|Field|Type|Constraints|Description|
|---|---|---|---|
|id|UUID v4|PK, NOT NULL|Generated by `AuthService`|
|email|string|UNIQUE, NOT NULL, indexed, lowercase-normalized|Login identifier|
|displayName|string|NOT NULL, 2-100 chars|UI display via `LoginPage`/`RegisterPage`|
|createdAt|ISO 8601|NOT NULL, DEFAULT now()|Account creation|
|updatedAt|ISO 8601|NOT NULL, auto-updated|Last profile modification|
|lastLoginAt|ISO 8601|NULLABLE|Updated on successful login|
|roles|string[]|NOT NULL, DEFAULT ["user"]|Authorization roles; not enforced by `AuthService`|
**Relationships:** 1:N with refresh-token records (Redis), 1:N with audit-log entries (PostgreSQL).

### DM-002 — `AuthToken`
**Storage:** accessToken is stateless (JWT); refreshToken stored in Redis with 7-day TTL.
**Interface:**
```ts
interface AuthToken {
  accessToken: string; refreshToken: string;
  expiresIn: number; tokenType: string;
}
```
**Fields:**
|Field|Type|Constraints|Description|
|---|---|---|---|
|accessToken|JWT string|NOT NULL|RS256 via `JwtService`; carries user id + roles|
|refreshToken|string|NOT NULL, unique|Opaque; Redis-backed by `TokenManager`; 7-day TTL|
|expiresIn|number|NOT NULL|Seconds until access expiry; always 900|
|tokenType|string|NOT NULL|Always "Bearer" (OAuth2 compat)|
**Relationships:** refreshToken record maps to `UserProfile.id`; issued/revoked by `TokenManager`.

**Additional storage (audit log):** PostgreSQL 15, 90-day retention per TDD §7.2 (conflicts with PRD 12-month requirement — see OQ-007).

## API Specifications

### API-001 — POST `/auth/login`
Auth required: No. Rate limit: 10 req/min/IP. Authenticates via `AuthService` → `PasswordHasher.verify()` → `TokenManager.issueTokens()`.
**Request:** `{ email, password }`. **Response 200:** `AuthToken` (`accessToken`, `refreshToken`, `expiresIn`, `tokenType`).
**Errors:** 401 invalid credentials; 423 locked (after 5 failures in 15 min); 429 rate-limited.

### API-002 — POST `/auth/register`
Auth required: No. Rate limit: 5 req/min/IP. Creates `UserProfile` via `AuthService`; bcrypt via `PasswordHasher`.
**Request:** `{ email, password, displayName }`. **Response 201:** `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt=null, roles=["user"]).
**Errors:** 400 validation (weak password, invalid email); 409 email conflict.

### API-003 — GET `/auth/me`
Auth required: Yes (Bearer accessToken). Rate limit: 60 req/min/user. Returns caller's `UserProfile`.
**Headers:** `Authorization: Bearer <jwt>`. **Response 200:** full `UserProfile`.
**Errors:** 401 missing/expired/invalid accessToken.

### API-004 — POST `/auth/refresh`
Auth required: No (refresh token in body). Rate limit: 30 req/min/user. Exchanges refresh token via `TokenManager`; revokes old, issues new `AuthToken`.
**Request:** `{ refreshToken }`. **Response 200:** new `AuthToken` pair.
**Errors:** 401 expired or revoked refresh token.

### API-005 — POST `/auth/reset-request`
Auth required: No. Rate limit: not specified (recommend align with register). Generates 1-hour single-use reset token; sends email via SendGrid. Returns identical response regardless of whether email is registered (no enumeration).
**Request:** `{ email }`. **Response:** 200/202 success message.
**Errors:** 400 malformed email; 429 rate-limited.
**Source:** FR-AUTH-005.

### API-006 — POST `/auth/reset-confirm`
Auth required: No (token in body). Validates reset token; updates password via `PasswordHasher`; invalidates all existing sessions.
**Request:** `{ token, newPassword }`. **Response:** 200 success.
**Errors:** 400 weak password; 401 invalid/expired/used token.
**Source:** FR-AUTH-005.

**Error envelope (all endpoints):** `{ "error": { "code": "AUTH_*", "message": "...", "status": <int> } }`.
**Governance:** URL-prefix versioning `/v1/auth/*`; additive non-breaking changes permitted within a major version; breaking changes require new major.

## Component Inventory

### COMP-001 — `LoginPage`
Type: Frontend route component. Location: `/login`. Auth: No. Props: `onSuccess: () => void`, `redirectUrl?: string`. Calls API-001. Stores `AuthToken` via `AuthProvider`.

### COMP-002 — `RegisterPage`
Type: Frontend route component. Location: `/register`. Auth: No. Props: `onSuccess: () => void`, `termsUrl: string`. Client-side password-strength validation before API-002.

### COMP-003 — `ProfilePage`
Type: Frontend route component. Location: `/profile`. Auth: Yes (via `AuthProvider`). Calls API-003 to render `UserProfile`.

### COMP-004 — `AuthProvider`
Type: React context provider. Props: `children: ReactNode`. Wraps all routes; manages `AuthToken` state; intercepts 401 and triggers `TokenManager` silent refresh via API-004; redirects unauthenticated users to `LoginPage`.

### COMP-005 — `AuthService`
Type: Backend orchestrator (facade). Delegates to `PasswordHasher`, `TokenManager`, `UserRepo`. Hosts API-001..006. Dependencies: PostgreSQL (via pg-pool), Redis (via `TokenManager`), SendGrid.

### COMP-006 — `TokenManager`
Type: Backend token-lifecycle component. Responsibilities: issue/revoke/rotate refresh tokens; store hashed refresh tokens in Redis with 7-day TTL. Delegates signing/verification to `JwtService`.

### COMP-007 — `JwtService`
Type: Backend JWT signer/verifier. Uses RS256 with 2048-bit RSA keys, rotated quarterly. Sign/verify latency target < 5ms. 5-second clock-skew tolerance.

### COMP-008 — `PasswordHasher`
Type: Backend password-hashing component. Uses bcrypt with configurable cost factor (default 12). Exposes `hash(plain)` and `verify(plain, hash)`. Benchmarked ~300ms per hash.

**Hierarchy:** `App → AuthProvider → { PublicRoutes → { LoginPage, RegisterPage }, ProtectedRoutes → ProfilePage }`.

## Testing Strategy

### TEST-001 — Unit: Login with valid credentials returns `AuthToken`
Component: `AuthService`. Validates FR-AUTH-001. Input: valid email/password. Mocks: `PasswordHasher.verify()→true`, `TokenManager.issueTokens()`. Expected: returned `AuthToken` has non-empty accessToken + refreshToken. Tooling: Jest + ts-jest.

### TEST-002 — Unit: Login with invalid credentials returns 401
Component: `AuthService`. Validates FR-AUTH-001. Input: valid-format email, wrong password. Mocks: `PasswordHasher.verify()→false`. Expected: 401; no `AuthToken` issued; no `TokenManager` call. Tooling: Jest.

### TEST-003 — Unit: Token refresh with valid refresh token
Component: `TokenManager`. Validates FR-AUTH-003. Input: valid refreshToken. Mocks: Redis returns active record; `JwtService.sign()`. Expected: old token revoked; new `AuthToken` pair issued. Tooling: Jest.

### TEST-004 — Integration: Registration persists `UserProfile` to database
Scope: `AuthService` + PostgreSQL. Validates FR-AUTH-002. Input: new email/password/displayName via API-002. Expected: `UserProfile` row with bcrypt hash; returned payload matches persisted row. Tooling: Supertest + testcontainers.

### TEST-005 — Integration: Expired refresh token rejected by `TokenManager`
Scope: `TokenManager` + Redis. Validates FR-AUTH-003. Input: refresh token past 7-day TTL. Expected: 401; no new pair issued. Tooling: Supertest + testcontainers (Redis with accelerated TTL).

### TEST-006 — E2E: User registers and logs in
Flow: `RegisterPage` → `LoginPage` → `ProfilePage`. Validates FR-AUTH-001, FR-AUTH-002. Expected: full journey under `AuthProvider`; profile page shows correct `UserProfile`. Tooling: Playwright.

**Pyramid targets:** Unit 80%, Integration 15%, E2E 5%.
**Environments:** Local (Docker Compose PG+Redis), CI (testcontainers), Staging (seeded accounts, prod-isolated).

## Migration and Rollout Plan

### MIG-001 — Phase 1: Internal Alpha
Duration: 1 week. Audience: auth-team + QA (staging). Tasks: deploy `AuthService`; manual-test all endpoints; `LoginPage`/`RegisterPage` behind `AUTH_NEW_LOGIN`=OFF except for internal users. Exit: FR-AUTH-001..005 pass manual testing; zero P0/P1 bugs. Rollback: disable `AUTH_NEW_LOGIN`.

### MIG-002 — Phase 2: Beta (10%)
Duration: 2 weeks. Audience: 10% of traffic. Monitoring: `AuthService` latency, error rate, `TokenManager` Redis usage; `AuthProvider` refresh under real load. Exit: p95 < 200ms; error rate < 0.1%; zero Redis connection failures. Rollback: lower `AUTH_NEW_LOGIN` % to 0.

### MIG-003 — Phase 3: General Availability (100%)
Duration: 1 week. Remove `AUTH_NEW_LOGIN`; all users on new `AuthService`; legacy endpoints deprecated; `AUTH_TOKEN_REFRESH` enables refresh flow. Exit: 99.9% uptime over first 7 days; all dashboards green.

### MIG-004 — Feature Flag `AUTH_NEW_LOGIN`
Purpose: Gate access to new `LoginPage` and login endpoint. Default OFF. Cleanup: remove after Phase 3 GA. Owner: auth-team.

### MIG-005 — Feature Flag `AUTH_TOKEN_REFRESH`
Purpose: Enable refresh-token flow in `TokenManager`; when OFF, only access tokens issued. Default OFF. Cleanup: remove 2 weeks after Phase 3. Owner: auth-team.

### MIG-006 — Rollback Procedure
Sequential steps: (1) disable `AUTH_NEW_LOGIN`; (2) smoke-test legacy login; (3) investigate `AuthService` RCA via logs/traces; (4) if `UserProfile` corruption detected, restore from last-known-good backup; (5) notify auth-team + platform-team via incident channel; (6) post-mortem within 48 hours.

### MIG-007 — Rollback Triggers
Any one triggers rollback: p95 > 1000ms for > 5 min; error rate > 5% for > 2 min; `TokenManager` Redis failures > 10/min; any `UserProfile` data loss or corruption.

## Operational Readiness

### OPS-001 — Runbook: `AuthService` down
Symptoms: 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` show error state. Diagnosis: pod health in K8s; PostgreSQL connectivity; init logs for `PasswordHasher`/`TokenManager`. Resolution: restart pods; failover PostgreSQL read replica; on Redis outage `TokenManager` rejects refresh — users must re-login. Escalation: auth-team on-call → platform-team if > 15 min. Prevention: HPA + DB replica readiness.

### OPS-002 — Runbook: Token refresh failures
Symptoms: users logged out unexpectedly; `AuthProvider` loops to `LoginPage`; `auth_token_refresh_total` error spike. Diagnosis: Redis connectivity from `TokenManager`; `JwtService` signing-key availability; `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis if degraded; re-mount `JwtService` secrets volume; enable `AUTH_TOKEN_REFRESH` if OFF. Escalation: auth-team on-call; platform-team on Redis cluster issue.

### OPS-003 — On-call expectations
P1 ack within 15 minutes. Coverage: auth-team 24/7 rotation during first 2 weeks post-GA. Tooling: K8s dashboards, Grafana, Redis CLI, PostgreSQL admin. Escalation path: auth-team on-call → test-lead → eng-manager → platform-team.

### OPS-004 — Capacity: `AuthService` pods
Current 3 replicas. Expected 500 concurrent users. Scaling: HPA to 10 replicas on CPU > 70%.

### OPS-005 — Capacity: PostgreSQL connections
Current pool size 100; avg 50 concurrent queries. Trigger: increase to 200 if connection wait time > 50ms.

### OPS-006 — Capacity: Redis memory
Current 1 GB; expected ~100K refresh tokens (~50 MB). Trigger: scale to 2 GB at > 70% utilization.

### OPS-007 — Observability: Structured logs
`AuthService` emits structured logs for login success/failure, registration, token refresh, password reset. Sensitive fields (password, tokens) excluded. Retention for audit log: TDD 90 days; PRD SOC2 requires 12 months (see OQ-007).

### OPS-008 — Observability: Prometheus metrics
Exposed: `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter).

### OPS-009 — Observability: Alerts
Thresholds: login failure rate > 20% over 5 min; p95 latency > 500ms; `TokenManager` Redis connection failures. Routed to auth-team on-call.

### OPS-010 — Observability: Distributed tracing
OpenTelemetry spans cover full request lifecycle through `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`. Enables latency attribution and failure root-cause.
