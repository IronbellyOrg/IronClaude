---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
adversarial: true
base_variant: "B (Haiku Architect)"
convergence_score: 0.72
debate_rounds: 2
---

# User Authentication Service — Final Merged Roadmap

## 1. Executive Summary

The User Authentication Service is a **medium-complexity, security-critical feature** that delivers secure registration, login, token management, password reset, profile retrieval, and compliance controls. The system uses JWT (RS256) with refresh token rotation, bcrypt password hashing (cost factor 12), and PostgreSQL-backed persistence.

**Strategic Priority**: Highest. Authentication unblocks the Q2–Q3 2026 personalization roadmap (~$2.4M projected annual revenue) and is prerequisite for the Q3 SOC2 Type II audit. Every downstream personalization feature depends on user identity shipping in Q2.

**Complexity**: MEDIUM (0.6) — well-understood authentication patterns but security-critical with compliance obligations (GDPR, SOC2 Type II by Q3 2026).

**Timeline**: 7–10 weeks across 2 phases (4 weeks Phase 1, 3 weeks Phase 2) plus 2–3 weeks contingency buffer. Development complete by late May, leaving 4+ weeks for hardening and production validation before the June 30 Q2 deadline.

**Key Architectural Decisions**:
- Stateless JWT with RS256 asymmetric signing — no server-side session store
- Refresh token rotation with replay detection — stored as hashed values in PostgreSQL
- Progressive account lockout (5→15min, 10→1hr, 20→admin unlock) — near-zero marginal cost over single-threshold
- Audit logging included in v1.0 (Phase 2) — SOC2 Q3 2026 deadline overrides spec's v1.1 deferral
- Differentiated performance targets — 200ms p95 for login/register/refresh, 500ms p95 for password reset
- Quarterly key rotation with 30-day overlap window for zero-downtime deprecation

**Compliance Conflict Resolution**: The specification defers audit logging to v1.1, but the PRD requires SOC2 audit logging with a Q3 2026 deadline. This roadmap includes audit logging in Phase 2 scope. Product and engineering must confirm this decision at discovery kickoff.

---

## 2. Phased Implementation Plan

### Phase 1: Authentication Core (Weeks 1–4)

**Objective**: Deliver login, registration, token management, profile retrieval, and logout — the minimum viable authentication layer that unblocks personalization development.

**Business Value**: Establishes identity foundation; unblocks downstream personalization feature work; delivers measurable registration conversion data by Week 4.

#### Phase 1 Milestones

**M1: Infrastructure and Schema (Week 1)**

| Task | Requirement | Details |
|------|------------|---------|
| 1.1 Provision PostgreSQL 15+ environment | D4 | Dev, staging, production environments |
| 1.2 Create migration 003: `users` table | D6 | Columns: id (UUID PK), email (unique index), password_hash, display_name, consent_timestamp, created_at, updated_at, locked_at (nullable), lock_count (integer default 0) |
| 1.3 Create migration 003: `refresh_tokens` table | D7 | Columns: id (UUID PK), user_id (FK → users), token_hash, device_id (UUID), expires_at, revoked_at, created_at; index on (user_id, expires_at) |
| 1.4 Generate RS256 key pair | D3 | 4096-bit RSA; store private key in secrets manager (AWS Secrets Manager or HashiCorp Vault); public key available to token verification layer |
| 1.5 GDPR schema compliance audit | NFR-AUTH.7 | Verify users table collects only email, hashed password, display name, consent timestamp — no extraneous PII |
| 1.6 Security and compliance architecture review | R1, R2, R5, R6 | Secrets manager integration, key rotation strategy, refresh token state machine design, OWASP checklist, SOC2 control mapping |

**M2: Core Service Implementation (Week 2)**

| Task | Requirement | Details |
|------|------------|---------|
| 2.1 Implement `PasswordHasher` module | D2, NFR-AUTH.3 | bcrypt cost factor 12; configurable via environment variable; unit test verifying cost factor and ~250ms hash timing |
| 2.2 Implement `JwtService` module | D1 | RS256 signing/verification; access token 15min TTL; configurable expiry; dual-key verification support for rotation overlap |
| 2.3 Implement `TokenManager` module | — | Orchestrates JwtService + refresh token DB operations; refresh token 7d TTL; rotation logic with replay detection; hashed token storage |
| 2.4 Implement `UserRepository` | — | Database access layer with prepared statements to prevent SQL injection |
| 2.5 Implement `AuthService` | — | Orchestrates login, registration, token refresh, logout logic; dependency injection for EmailService (no-op in Phase 1) |

**M3: API, Middleware, and Security Hardening (Weeks 3–4)**

| Task | Requirement | Details |
|------|------------|---------|
| 3.1 Implement `auth-middleware` | — | Bearer token extraction from Authorization header; JWT validation via JwtService; user context injection into request; 401 on invalid/expired token |
| 3.2 Implement registration endpoint | FR-AUTH.2 | POST `/auth/register`; validates email format (FR-AUTH.2d), enforces password policy (FR-AUTH.2c), checks duplicate email (FR-AUTH.2b), captures GDPR consent with timestamp (NFR-AUTH.4), hashes password, creates user record, returns 201 with profile (FR-AUTH.2a) |
| 3.3 Implement login endpoint | FR-AUTH.1 | POST `/auth/login`; validates credentials via PasswordHasher.verify; issues access + refresh tokens via TokenManager (FR-AUTH.1a); generic 401 on failure (FR-AUTH.1b); 403 on locked account (FR-AUTH.1c) |
| 3.4 Implement rate limiting on login | FR-AUTH.1d | 5 attempts per minute per IP; return 429 on exceeded |
| 3.5 Implement progressive account lockout | OQ3 | 5 failures → 15min lock; 10 failures → 1hr lock; 20 failures → admin unlock required. Log lock events. |
| 3.6 Implement token refresh endpoint | FR-AUTH.3 | POST `/auth/refresh`; validates refresh token hash against DB (FR-AUTH.3d); issues new access + rotated refresh token (FR-AUTH.3a); 401 on expired (FR-AUTH.3b); replay detection revokes all user tokens (FR-AUTH.3c) |
| 3.7 Implement profile retrieval endpoint | FR-AUTH.4 | GET `/auth/profile`; requires auth-middleware; returns id, email, display_name, created_at (FR-AUTH.4a); 401 on invalid token (FR-AUTH.4b); excludes sensitive fields (FR-AUTH.4c) |
| 3.8 Implement logout endpoint | OQ8 | POST `/auth/logout`; revokes current refresh token; clears httpOnly cookie |
| 3.9 Configure refresh token cookie | Constraint #3 | httpOnly, Secure, SameSite=Strict cookie for refresh token; access token returned in response body only |
| 3.10 Register `/auth/*` route group | — | All endpoints registered in main route index |
| 3.11 Unit tests | — | Password hashing, JWT signing/verification, token rotation, progressive lockout thresholds |
| 3.12 Integration tests | — | Full login/register/refresh/logout flows; happy path + error cases |
| 3.13 Security tests | — | Credential error messages reveal nothing (no enumeration); expired tokens return 401 without token state; locked accounts return 403 |
| 3.14 Performance testing | NFR-AUTH.1 | k6: login endpoint < 200ms p95 under 500 concurrent requests |
| 3.15 Security code review | R5 | Focused on JWT signing, bcrypt config, token rotation, replay detection, SQL injection vectors |
| 3.16 Registration UX testing | SC1, R4 | 5+ users per persona (Alex, Sam); target > 60% conversion rate; iterate on friction points before Phase 2 |

#### Phase 1 Integration Points

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---------------|------|-------------------|-------------|-------------|
| `PasswordHasher` | Service module | bcrypt library (D2) | Phase 1 (M2) | Phase 1 (AuthService), Phase 2 (password reset) |
| `JwtService` | Service module | jsonwebtoken library (D1), RS256 key pair (D3) | Phase 1 (M2) | Phase 1 (TokenManager, auth-middleware) |
| `TokenManager` | Orchestrator module | JwtService, RefreshToken table (D7) | Phase 1 (M2) | Phase 1 (login, refresh), Phase 2 (password reset) |
| `AuthService` | Service layer | TokenManager, PasswordHasher, UserRepository | Phase 1 (M2) | Phase 1 (route handlers), Phase 2 (password reset, audit) |
| `auth-middleware` | Middleware (request pipeline) | JwtService | Phase 1 (M3) | All authenticated endpoints (Phase 1–2) |
| `/auth/*` route group | Route registration | AuthService handlers | Phase 1 (M3) | Phase 2 (adds password reset routes) |
| Rate limiter | Middleware | IP-based counter (in-memory or Redis) | Phase 1 (M3) | Login endpoint, Phase 2 (password reset) |
| Migration 003 | Database schema | users table (D6), refresh_tokens table (D7) | Phase 1 (M1) | All subsequent phases |

**Dependency Gate**: Frontend routing framework (D8) must be available by Week 3 for login/registration UI. If delayed, API-only testing proceeds; UI integration shifts to Phase 2.

**Phase 1 Exit Gate**:
- All FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4 acceptance criteria pass in integration tests
- NFR-AUTH.1 verified: login endpoint < 200ms p95 under 500 concurrent load (k6)
- NFR-AUTH.3 verified: bcrypt cost factor 12 confirmed in unit tests (~250ms hash time)
- NFR-AUTH.6 verified: code audit confirms no plaintext password storage or logging
- Security review clearance: no critical/high findings
- Registration UX testing: > 60% conversion rate target validated (5+ user tests)
- All open questions (OQ1–OQ8) resolved; scope confirmed with product

---

### Phase 2: Recovery, Compliance, and Hardening (Weeks 5–7)

**Objective**: Deliver password reset, compliance baselines (GDPR verification, audit logging), monitoring, and production readiness.

**Business Value**: Enables self-service account recovery (reduces support burden), establishes SOC2 compliance foundation, and hardens token security for production.

#### Phase 2 Milestones

**M4: Password Reset and Email Integration (Week 5)**

| Task | Requirement | Details |
|------|------------|---------|
| 4.1 Confirm email delivery service (SendGrid) availability | D5 | **BLOCKING**: FR-AUTH.5 cannot proceed without this. Escalate if unavailable. |
| 4.2 Implement password reset request endpoint | FR-AUTH.5a | POST `/auth/password-reset/request`; generates 1-hour TTL reset token (one-time use); dispatches email via async message queue; same response regardless of email registration status (prevents enumeration) |
| 4.3 Implement password reset confirm endpoint | FR-AUTH.5b, FR-AUTH.5c | POST `/auth/password-reset/confirm`; validates reset token; hashes new password; invalidates reset token; revokes all refresh tokens (FR-AUTH.5d) |
| 4.4 Implement password reset rate limiting | D6 (debate) | 10 requests per hour per email address; prevents email bombing |
| 4.5 Email delivery monitoring | R7 | SendGrid delivery status tracking; alert on bounce/delay rates > 5%; retry logic for transient failures; delivery SLA target: > 95% within 60 seconds |
| 4.6 Integration tests — password reset | — | Full reset flow; expired link handling; rate limiting verification |

**M5: Compliance and Audit Logging (Week 6)**

| Task | Requirement | Details |
|------|------------|---------|
| 5.1 Design audit logging schema | NFR-AUTH.5 | `auth_events` table: id, user_id, event_type, timestamp, ip_address, user_agent, outcome (success/failure), error_code; 12-month retention via TTL or archival job; index on (user_id, timestamp) for SOC2 audit queries |
| 5.2 Wire audit logging into all auth endpoints | NFR-AUTH.5 | Events: registration, login (success/failure), logout, token refresh, password reset (request/confirm), account lock/unlock |
| 5.3 SOC2 control mapping validation | R6 | Map audit events to SOC2 controls (CC6.1 login audit, CC7.2 logout events); compliance team review |
| 5.4 Verify GDPR consent records | NFR-AUTH.4 | Consent timestamp queryable; consent present on all user records; audit confirms no registration bypasses consent |
| 5.5 NIST password storage audit | NFR-AUTH.6 | Code review confirming no plaintext password storage or logging anywhere in the codebase |
| 5.6 Data minimization audit | NFR-AUTH.7 | Verify users table contains only: id, email, password_hash, display_name, consent_timestamp, created_at, updated_at — no extraneous PII |

**M6: Security Hardening, Monitoring, and Launch Readiness (Week 7)**

| Task | Requirement | Details |
|------|------------|---------|
| 6.1 Refresh token replay detection hardening | FR-AUTH.3c | Verify: rotated token reuse triggers revocation of all user tokens; add rotation history for forensics |
| 6.2 Key rotation procedure | R1 | Document and test RS256 key rotation; quarterly schedule; 30-day overlap window with dual-key verification; production keys in HSM/KMS |
| 6.3 Monitoring and alerting | NFR-AUTH.2 | Alert on > 20 failed logins/min; alert on unusual refresh token reuse patterns (potential breach); APM dashboard for auth endpoint latency and error rates |
| 6.4 Health check endpoint | NFR-AUTH.2 | Availability monitoring configured for 99.9% target; PagerDuty integration |
| 6.5 Load testing — all endpoints | NFR-AUTH.1, SC2 | k6: login/register/refresh < 200ms p95; password reset < 500ms p95; 500 concurrent users |
| 6.6 Penetration testing | R5 | External penetration test covering OWASP Top 10 for authentication; remediate critical/high findings before launch |
| 6.7 Session duration validation | SC3 | Verify silent token refresh enables > 30 minute average session duration |
| 6.8 Failed login rate baseline | SC4 | Measure failed login rate; target < 5% of total attempts |
| 6.9 Password reset completion validation | SC5 | Funnel measurement: reset requested → new password set; target > 80% |
| 6.10 Complete-flow UX testing | SC1, SC5 | End-to-end user journey: registration through password reset; validates full experience |
| 6.11 Production deployment | — | Deploy to production; smoke test all endpoints; confirm monitoring active |
| 6.12 Post-launch monitoring (72-hour) | — | Watch error rates, latency p95, audit log completeness; rollback plan documented |

#### Phase 2 Integration Points

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---------------|------|-------------------|-------------|-------------|
| Audit logger | Cross-cutting service | All auth endpoints | Phase 2 (M5) | Ongoing operations, SOC2 audit queries |
| Password reset routes | Route registration (added to `/auth/*` group) | AuthService, TokenManager, email service (D5) | Phase 2 (M4) | Frontend password reset UI |
| Email event dispatcher | Event emitter | SendGrid, message queue (Redis) | Phase 2 (M4) | Password reset flow |
| Account lock registry | State machine | Failed login counter, lock expiration, progressive thresholds | Phase 1 (M3), hardened Phase 2 (M6) | Login endpoint |

**Phase 2 Exit Gate**:
- All FR-AUTH.5 acceptance criteria pass
- NFR-AUTH.2 infrastructure in place: health check configured, 99.9% monitoring active
- NFR-AUTH.4 verified: GDPR consent recorded at registration with timestamp
- NFR-AUTH.5 complete: audit log schema approved; 12-month retention configured; SOC2 control mappings verified
- NFR-AUTH.7 verified: schema audit confirms data minimization
- Security review clearance: penetration testing zero critical findings on password reset, token replay detection
- Email delivery monitoring active: > 95% of reset emails delivered within 60 seconds
- Password reset endpoint < 500ms p95; all other auth endpoints < 200ms p95
- Compliance validation: audit log requirements signed off against SOC2 control objectives (CC6.1, CC7.2)

---

## 3. Risk Assessment and Mitigation

| # | Risk | Severity | Phase | Mitigation Strategy | Success Indicator |
|---|------|----------|-------|---------------------|-------------------|
| R1 | JWT private key compromise allows forged tokens | **High** | All | (1) RS256 private key in secrets manager — never in code, logs, or CI/CD. (2) Quarterly rotation with 30-day overlap window for zero-downtime deprecation. (3) Production: dedicated HSM or KMS. (4) Anomaly detection on token issue rate. | Private key never appears in code/logs. Key rotation tested quarterly. |
| R2 | Refresh token replay attack after theft | **High** | Phase 1–2 | (1) Token rotation on every use (FR-AUTH.3c). (2) Refresh tokens hashed before storage. (3) Replay detection: rotated token reuse revokes all user tokens immediately. (4) Phase 2: rotation history table for forensics. | Replay detection test passes. Audit log shows token revocation on reuse. |
| R3 | bcrypt cost factor insufficient for future hardware | **Medium** | Phase 1 | (1) Cost factor configurable via environment variable (12 minimum). (2) Annual OWASP review. (3) Argon2id migration path documented for v1.1. (4) Alert if hash time < 100ms (indicates weak config). | Cost factor verified in unit tests. Migration path documented. |
| R4 | Low registration adoption due to poor UX | **High** | Phase 1–2 | (1) Registration UX testing at Phase 1 exit gate — catches funnel problems before Phase 2 investment. (2) Inline validation with real-time error feedback. (3) Complete-flow UX testing at Phase 2 exit. (4) Target > 60% conversion (PRD SC1). (5) If < 50% at Week 3, iterate form design before proceeding. | Conversion funnel > 60%. A/B test results analyzed. |
| R5 | Security breach from implementation flaws | **High** | Phase 1–2 | (1) Phase 1 security review: JWT signing, password hashing, token storage, SQL injection vectors. (2) Phase 2 penetration testing: OWASP Top 10 for authentication. (3) Threat modeling at Phase 1 kickoff. (4) Remediate all critical/high findings before launch. | Security review clearance. Pen test zero critical findings. |
| R6 | Compliance failure from incomplete audit logging | **High** | Phase 2 | (1) SOC2 control mappings defined early (CC6.1, CC7.2). (2) Audit schema review by compliance team before Phase 2 dev. (3) Validation at Phase 2 exit gate. (4) 12-month retention enforced via TTL or archival. (5) Queryability test: logs queryable by date/user/event type. | Audit log schema approved by compliance. Phase 2 QA validates completeness. |
| R7 | Email delivery failures blocking password reset | **Medium** | Phase 2 | (1) SendGrid delivery monitoring: alert on bounce/delay > 5%. (2) Async delivery via message queue (decouples endpoint latency). (3) Support runbook for manual reset process. (4) Delivery SLA target: > 95% within 60 seconds. | Email delivery > 95%. Reset email within 60 seconds. Support runbook documented. |

**Architectural Risk Note**: OQ6 conflict between spec (audit logging deferred to v1.1) and PRD (SOC2 Q3 2026 deadline) is resolved by including audit logging in Phase 2. If stakeholders override this decision, the SOC2 timeline is at risk.

---

## 4. Resource Requirements and Dependencies

### Team Composition

| Role | Phase 1 (Wk 1–4) | Phase 2 (Wk 5–7) | Buffer (Wk 8–10) |
|------|-------------------|-------------------|-------------------|
| Backend Engineer | 1.5 FTE | 1.5 FTE | 1 FTE |
| Frontend Engineer | 1 FTE (from Wk 3) | 1 FTE | 0.5 FTE |
| Security Engineer | 0.5 FTE (review, threat model) | 0.5 FTE (audit, pen test) | As needed |
| QA Engineer | 0.5 FTE (Wk 1–2), 1 FTE (Wk 3–4) | 1 FTE | 1 FTE |
| DevOps | 0.5 FTE (infra) | 0.25 FTE | 0.5 FTE (deploy) |
| Product Manager | 0.5 FTE (OQ resolution, UX) | 0.25 FTE | As needed |

**Total Effort**: ~4.5 FTE for 7–10 weeks ≈ 180–200 engineer-days.

### Infrastructure Prerequisites (before Phase 1)

| Dependency | ID | Required By | Provisioning Owner |
|------------|-----|------------|-------------------|
| PostgreSQL 15+ (dev/staging/prod) | D4 | Phase 1, Task 1.1 | DevOps/Infrastructure |
| RS256 key pair in secrets manager | D3 | Phase 1, Task 1.4 | Security/Infrastructure |
| NPM packages: jsonwebtoken, bcrypt | D1, D2 | Phase 1, Tasks 2.1–2.2 | Engineering |
| Security Policy (SEC-POLICY-001) | D9 | Phase 1, Task 1.6 | Security — defaults to NIST SP 800-63B if unavailable |

### Gated Dependencies

| Dependency | ID | Required By | Gate |
|------------|-----|------------|------|
| Frontend routing framework | D8 | Phase 1 (UI integration) | Week 3 — API-only testing proceeds if delayed |
| Email delivery service (SendGrid) | D5 | Phase 2, Task 4.1 | **Week 5 hard gate** — FR-AUTH.5 blocked without this; provision in Week 3, allow 2 weeks for integration |
| Message queue (Redis) | — | Phase 2 (async email) | Week 5 — provision if OQ1 resolves to async (recommended) |
| APM/monitoring tool | — | Phase 2 (monitoring) | Week 6 — confirm existing tool (Datadog, New Relic); integrate auth endpoints |

---

## 5. Success Criteria and Validation Approach

### Measurable Success Thresholds

| Criterion | ID | Target | Validation Phase | Method |
|-----------|-----|--------|-----------------|--------|
| Registration conversion rate | SC1 | > 60% | Phase 1 exit (early), Phase 2 exit (complete flow) | Funnel: landing → register form → confirmed account |
| Login response time (p95) | SC2 | < 200ms | Phase 1 (k6), Phase 2 (production APM) | k6 load test (500 concurrent); APM on `/auth/login` |
| Average session duration | SC3 | > 30 minutes | Phase 2 (Task 6.7) | Token refresh event analytics — time between first access token and last refresh |
| Failed login rate | SC4 | < 5% of attempts | Phase 2 (Task 6.8), post-launch | Auth event log analysis — failed logins / total login attempts |
| Password reset completion | SC5 | > 80% | Phase 2 (Task 6.9), post-launch | Funnel: reset requested → new password set (from audit logs) |
| Service availability | SC6 | 99.9% uptime (< 8.76 hrs/year) | Phase 2 ongoing (Task 6.4) | Health check endpoint monitoring; rolling 30-day windows |
| Password reset response time (p95) | — | < 500ms | Phase 2 (Task 6.5) | k6 load test on `/auth/password-reset/*` |

**Validation strategy**: SC1 is tested at both Phase 1 exit (registration-only) and Phase 2 exit (complete flow). SC2 is validated at Phase 1 exit and re-validated under production load in Phase 2. SC3–SC5 require audit logging (Phase 2) to be operational before measurement. SC6 is an ongoing operational metric established at launch.

---

## 6. Timeline Summary

```
Week  1      ████      M1: Infrastructure & Schema
                       DB migration, RS256 keys, GDPR schema audit,
                       security architecture review

Week  2      ████      M2: Core Service Implementation
                       PasswordHasher, JwtService, TokenManager,
                       UserRepository, AuthService

Week  3-4    ████████  M3: API, Middleware & Security Hardening
                       All endpoints, rate limiting, progressive lockout,
                       integration tests, security review, UX testing
                       ── Phase 1 Exit Gate ──

Week  5      ████      M4: Password Reset & Email Integration
                       Reset endpoints, rate limiting (10/hr/email),
                       SendGrid integration, async email queue

Week  6      ████      M5: Compliance & Audit Logging
                       Audit schema, SOC2 control mapping, GDPR
                       verification, NIST audit, data minimization

Week  7      ████      M6: Hardening, Monitoring & Launch
                       Replay detection hardening, key rotation procedure,
                       alerting, pen testing, load testing, UX validation,
                       production deployment
                       ── Phase 2 Exit Gate ──

Week  8-10   ████████  Buffer: Risk Absorption
                       Pen test remediation, UX iteration, regression
                       testing, production stabilization (72-hour watch)
```

**Critical path**: M1 → M2 → M3 (login/registration) → M4 (password reset) → M5 (audit logging) → M6 (hardening/launch)

**Parallel opportunities**: Frontend UI development proceeds alongside backend API work in Weeks 3–4. Security architecture review (M1) informs threat model used throughout. Penetration test scoping can begin during Week 6.

**Go-Live Target**: End of Q2 2026 (by June 30). If 10-week estimate holds, development complete by late May, leaving 4+ weeks buffer against the deadline.

---

## 7. Open Questions — Resolution Schedule

| # | Question | Must Resolve By | Resolution |
|---|----------|----------------|------------|
| OQ1 | Sync vs async password reset emails? | Phase 2 start (Week 5) | **Async via message queue** — decouples endpoint latency from email delivery; adds resilience |
| OQ2 | Max active refresh tokens per user? | Phase 1 start (Week 1) | **10 tokens max with device-based rotation** — compromise between bounded storage (A) and multi-device UX (B); covers realistic scenarios; revisit cap in v1.1 based on usage data |
| OQ3 | Account lockout policy after N failures? | Phase 1, Task 3.5 (Week 3) | **Progressive lockout**: 5→15min, 10→1hr, 20→admin unlock. Near-zero marginal cost; supplements per-IP rate limiting |
| OQ4 | "Remember me" extending session beyond 7 days? | Phase 1 (Week 3) | **Defer to v1.1** — 7-day refresh window is adequate for launch |
| OQ5 | Token revocation on user deletion? | Phase 1 schema design (Week 1) | **Cascade delete** — delete user record cascades to refresh_tokens; access tokens expire naturally (15min) |
| OQ6 | Audit logging in v1.0 or v1.1? | **Resolved** | **v1.0 (Phase 2)** — SOC2 Q3 2026 deadline forces inclusion |
| OQ7 | GDPR consent mechanism? | Phase 1, Task 3.2 (Week 3) | **Explicit checkbox** — "I agree to [Terms] and [Privacy Policy]" with timestamp |
| OQ8 | Logout endpoint? | Phase 1 (Week 3) | **Phase 1 scope** — POST `/auth/logout`; revokes current refresh token |
| OQ9 | JTBD #2 state persistence beyond sessions? | Pre-Phase 1 | **Out of scope for auth service** — JTBD #2 implies application-level state persistence (saved preferences, activity history), not session persistence. Confirm with Product and track separately. |

---

## 8. Scope Guardrails

The following are explicitly **out of scope** per the PRD. Any roadmap change request touching these areas requires scope change approval:

| Capability | Status | Rationale |
|-----------|--------|-----------|
| OAuth/OIDC | Out of scope | Planned for v2.0; adds complexity without addressing core v1.0 needs |
| Multi-factor authentication | Out of scope | Planned for v1.1; requires SMS/TOTP infrastructure |
| Role-based access control | Out of scope | Authorization is a separate concern with dedicated PRD |
| Social login (Google, GitHub) | Out of scope | Depends on OAuth/OIDC not yet available |
| Application state persistence (JTBD #2) | Confirm out of scope (OQ9) | Auth service provides session identity, not application state |
| "Remember me" extended sessions | Deferred to v1.1 (OQ4) | 7-day refresh window adequate for launch; increased token management complexity |

---

## 9. Persona Coverage

| Persona | Addressed By | Phase |
|---------|-------------|-------|
| **Alex (End User)** | Registration (FR-AUTH.2), login (FR-AUTH.1), logout (OQ8), session persistence (FR-AUTH.3), profile (FR-AUTH.4), password reset (FR-AUTH.5) | Phase 1 (core), Phase 2 (reset) |
| **Jordan (Platform Admin)** | Audit logging (NFR-AUTH.5), account lockout visibility (OQ3 progressive model), SOC2 control mappings | Phase 2 (M5) |
| **Sam (API Consumer)** | Token refresh endpoint (FR-AUTH.3), clear error codes (401/403/429), programmatic token management via device-based rotation | Phase 1 (M3) |
