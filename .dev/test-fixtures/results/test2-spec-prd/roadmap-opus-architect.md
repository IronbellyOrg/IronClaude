---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
generated: "2026-04-02T00:00:00Z"
generator: "roadmap-architect-agent"
total_phases: 4
total_milestones: 8
estimated_duration_weeks: 12
risk_count: 7
open_questions_count: 9
---

# User Authentication Service — Project Roadmap

## 1. Executive Summary

This roadmap defines a four-phase implementation plan for the User Authentication Service, delivering secure registration, login, token management, password reset, profile retrieval, and compliance controls. The system uses JWT (RS256) with refresh token rotation, bcrypt password hashing, and PostgreSQL-backed persistence.

**Complexity**: MEDIUM (0.6) — well-understood authentication patterns but security-critical with compliance obligations (GDPR, SOC2 Type II by Q3 2026).

**Strategic context**: Authentication unblocks the entire Q2–Q3 2026 personalization roadmap (~$2.4M projected annual revenue) and is prerequisite for the Q3 SOC2 audit. The phasing below front-loads critical-path items (login, registration, token management) while deferring password reset until the email delivery dependency (D5) is confirmed.

**Key architectural decisions**:
- Stateless JWT with RS256 asymmetric signing — no server-side session store
- Refresh token rotation with replay detection — stored as hashed values in PostgreSQL
- Layered module dependency: auth-middleware → auth-service → token-manager/password-hasher → jwt-service
- Compliance controls (audit logging, GDPR consent) integrated into Phase 3 rather than retrofitted

---

## 2. Phased Implementation Plan

### Phase 1: Foundation & Data Layer (Weeks 1–2)

**Objective**: Establish database schema, cryptographic infrastructure, and core service modules that all functional requirements depend on.

**Milestone M1**: Database migration and core services operational (end of Week 2)

| Task | Requirement | Details |
|------|------------|---------|
| 1.1 Provision PostgreSQL 15+ environment | D4 | Dev, staging, production environments |
| 1.2 Create migration 003: `users` table | D6 | Columns: id (UUID PK), email (unique index), password_hash, display_name, created_at, updated_at, locked_at (nullable) |
| 1.3 Create migration 003: `refresh_tokens` table | D7 | Columns: id (UUID PK), user_id (FK → users), token_hash, expires_at, revoked_at, created_at; index on user_id |
| 1.4 Generate RS256 key pair | D3 | Store private key in secrets manager; public key available to token verification layer |
| 1.5 Implement `PasswordHasher` module | D2, NFR-AUTH.3 | bcrypt cost factor 12; configurable; unit test verifying cost factor and ~250ms hash timing |
| 1.6 Implement `JwtService` module | D1 | RS256 signing/verification; access token 15min TTL; configurable expiry |
| 1.7 Implement `TokenManager` module | — | Orchestrates JwtService + refresh token DB operations; refresh token 7d TTL; rotation logic |
| 1.8 GDPR schema compliance audit | NFR-AUTH.7 | Verify users table collects only email, hashed password, display name — no extraneous PII |

**Integration points created in this phase**:

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---------------|------|-------------------|-------------|-------------|
| `PasswordHasher` | Service module | bcrypt library (D2) | Phase 1 | Phase 2 (FR-AUTH.1, FR-AUTH.2), Phase 3 (FR-AUTH.5) |
| `JwtService` | Service module | jsonwebtoken library (D1), RS256 key pair (D3) | Phase 1 | Phase 1 (TokenManager), Phase 2 (auth-middleware) |
| `TokenManager` | Orchestrator module | JwtService, RefreshToken table (D7) | Phase 1 | Phase 2 (FR-AUTH.1, FR-AUTH.3), Phase 3 (FR-AUTH.5) |
| Migration 003 | Database schema | users table (D6), refresh_tokens table (D7) | Phase 1 | All subsequent phases |

**Exit criteria**: All three service modules pass unit tests. Migration 003 applies cleanly. RS256 key pair provisioned in secrets manager.

---

### Phase 2: Core Authentication (Weeks 3–6)

**Objective**: Deliver login, registration, token refresh, and profile retrieval — the critical path that unblocks authenticated functionality.

**Milestone M2**: Registration and login functional (end of Week 4)
**Milestone M3**: Token refresh and profile retrieval functional (end of Week 6)

| Task | Requirement | Details |
|------|------------|---------|
| 2.1 Implement `auth-service` — registration | FR-AUTH.2 | Validates email format (FR-AUTH.2d), enforces password policy (FR-AUTH.2c), checks duplicate email (FR-AUTH.2b), hashes password via PasswordHasher, creates user record, returns 201 with profile (FR-AUTH.2a) |
| 2.2 Add GDPR consent capture to registration | NFR-AUTH.4 | Consent checkbox in registration payload; consent timestamp stored in users table; blocks registration if not provided |
| 2.3 Implement `auth-service` — login | FR-AUTH.1 | Validates credentials via PasswordHasher.verify; issues access + refresh tokens via TokenManager (FR-AUTH.1a); generic 401 on failure (FR-AUTH.1b); 403 on locked account (FR-AUTH.1c) |
| 2.4 Implement rate limiting on login endpoint | FR-AUTH.1d | 5 attempts per minute per IP address; return 429 on exceeded |
| 2.5 Implement `auth-service` — token refresh | FR-AUTH.3 | Accepts refresh token; validates against DB hash (FR-AUTH.3d); issues new access + rotated refresh token (FR-AUTH.3a); returns 401 on expired (FR-AUTH.3b); replay detection revokes all user tokens (FR-AUTH.3c) |
| 2.6 Implement `auth-middleware` — Bearer token extraction | — | Extracts JWT from Authorization header; validates via JwtService; attaches user context to request; returns 401 on invalid/expired token |
| 2.7 Register `/auth/*` route group | — | POST `/auth/register`, POST `/auth/login`, POST `/auth/refresh`; add to existing route index |
| 2.8 Implement profile retrieval endpoint | FR-AUTH.4 | GET `/auth/profile`; requires auth-middleware; returns id, email, display_name, created_at (FR-AUTH.4a); 401 on invalid token (FR-AUTH.4b); excludes sensitive fields (FR-AUTH.4c) |
| 2.9 Refresh token cookie configuration | Architectural Constraint #3 | Set refresh token in httpOnly, Secure, SameSite=Strict cookie; access token returned in response body only |
| 2.10 Integration tests — auth flows | — | Happy path + error cases for login, registration, token refresh, profile retrieval |

**Integration points created in this phase**:

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---------------|------|-------------------|-------------|-------------|
| `auth-service` | Service layer | TokenManager, PasswordHasher, User table | Phase 2 | Phase 2 (route handlers), Phase 3 (password reset) |
| `auth-middleware` | Middleware (request pipeline) | JwtService | Phase 2 | Phase 2 (profile route), Phase 3+ (all authenticated routes) |
| `/auth/*` route group | Route registration (route index) | auth-service handlers | Phase 2 | Phase 3 (adds `/auth/password-reset/*`) |
| Rate limiter | Middleware | IP-based counter (in-memory or Redis) | Phase 2 | Phase 2 (login endpoint) |

**Dependency gate**: Frontend routing framework (D8) must be available by Week 4 for login/registration UI. If delayed, API-only testing proceeds; UI integration shifts to Phase 3.

**Exit criteria**: All FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4 acceptance criteria pass in integration tests. Rate limiting verified. Refresh token rotation and replay detection demonstrated.

---

### Phase 3: Password Reset & Compliance (Weeks 7–9)

**Objective**: Deliver password reset (blocked until email service is confirmed) and compliance controls (audit logging, GDPR). Resolves OQ6 conflict by including audit logging in v1.0 scope per PRD SOC2 timeline.

**Milestone M4**: Password reset flow operational (end of Week 8)
**Milestone M5**: Audit logging and compliance controls verified (end of Week 9)

| Task | Requirement | Details |
|------|------------|---------|
| 3.1 Confirm email delivery service (SendGrid) availability | D5 | **BLOCKING**: FR-AUTH.5 cannot proceed without this. Escalate if unavailable by Week 6. |
| 3.2 Implement password reset — request endpoint | FR-AUTH.5a | POST `/auth/password-reset/request`; generates 1-hour TTL reset token; dispatches email; same response regardless of email registration status (prevents enumeration) |
| 3.3 Implement password reset — confirm endpoint | FR-AUTH.5b, FR-AUTH.5c | POST `/auth/password-reset/confirm`; validates reset token; hashes new password; invalidates reset token; invalidates all refresh tokens (FR-AUTH.5d) |
| 3.4 Email delivery monitoring | R7 | Alert on delivery failures; log send attempts; document manual reset fallback via support channel |
| 3.5 Implement audit logging infrastructure | NFR-AUTH.5 | Log schema: user_id, event_type, timestamp, IP address, outcome; structured JSON logging; 12-month retention policy |
| 3.6 Wire audit logging into all auth endpoints | NFR-AUTH.5 | Events: registration, login (success/failure), token refresh, password reset (request/confirm), profile access |
| 3.7 Verify GDPR consent records | NFR-AUTH.4 | Consent timestamp queryable; consent present on all user records; audit confirms no registration bypasses consent |
| 3.8 NIST password storage audit | NFR-AUTH.6 | Code review confirming no plaintext password storage or logging anywhere in the codebase |
| 3.9 Integration tests — password reset + audit logging | — | Full reset flow; audit log completeness for all event types |

**Integration points created in this phase**:

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---------------|------|-------------------|-------------|-------------|
| Audit logger | Cross-cutting service | All auth endpoints (login, register, refresh, reset, profile) | Phase 3 | Phase 4 (admin queries), ongoing operations |
| Password reset routes | Route registration (added to `/auth/*` group) | auth-service, TokenManager, email service (D5) | Phase 3 | Frontend password reset UI |

**Exit criteria**: All FR-AUTH.5 acceptance criteria pass. Audit logs present for every auth event type. GDPR consent verified. NIST compliance confirmed via code audit.

---

### Phase 4: Hardening, Performance & Launch (Weeks 10–12)

**Objective**: Performance validation, security review, UX testing, and production deployment.

**Milestone M6**: Performance targets met (end of Week 10)
**Milestone M7**: Security review and penetration test complete (end of Week 11)
**Milestone M8**: Production launch (end of Week 12)

| Task | Requirement | Details |
|------|------------|---------|
| 4.1 Load testing — login endpoint | NFR-AUTH.1, SC2 | k6 tests: < 200ms p95 under 500 concurrent requests |
| 4.2 Load testing — registration, refresh, profile endpoints | NFR-AUTH.1 | Verify all auth endpoints meet < 200ms p95 |
| 4.3 Availability testing | NFR-AUTH.2, SC6 | Health check endpoint; verify monitoring and PagerDuty alerting configured for 99.9% target |
| 4.4 Security review | R5 | Dedicated security review of: JWT implementation, bcrypt configuration, token rotation, replay detection, error messages (no user enumeration), httpOnly cookie settings |
| 4.5 Penetration testing | R5 | External penetration test covering OWASP Top 10 for authentication; remediate findings before launch |
| 4.6 Key rotation procedure | R1 | Document and test RS256 key rotation; verify 90-day rotation schedule; confirm old tokens gracefully expire |
| 4.7 UX testing — registration funnel | R4, SC1 | Usability testing targeting > 60% registration conversion rate; iterate on friction points |
| 4.8 UX testing — password reset funnel | SC5 | Verify > 80% reset completion rate; email delivery within 60 seconds |
| 4.9 Session duration validation | SC3 | Verify silent token refresh enables > 30 minute average session duration |
| 4.10 Failed login rate baseline | SC4 | Measure failed login rate; target < 5% of total attempts |
| 4.11 Production deployment | — | Deploy to production; smoke test all endpoints; confirm monitoring active |
| 4.12 Post-launch monitoring (72-hour) | — | Watch error rates, latency p95, audit log completeness; rollback plan documented |

**Exit criteria**: All success criteria (SC1–SC6) validated. Security review and penetration test passed. Production deployment successful with 72-hour stability confirmed.

---

## 3. Risk Assessment and Mitigation

| # | Risk | Severity | Phase Impact | Mitigation Strategy | Residual Risk |
|---|------|----------|-------------|---------------------|---------------|
| R1 | JWT private key compromise | **High** | Phase 1, 4 | RS256 asymmetric keys in secrets manager; 90-day rotation (Task 4.6); monitoring for anomalous token patterns | Low after rotation procedure verified |
| R2 | Refresh token replay attack | **High** | Phase 2 | Rotation with replay detection (FR-AUTH.3c); revoke all user tokens on reuse; implemented in Task 2.5 | Low — standard mitigation pattern |
| R3 | bcrypt cost factor obsolescence | **Medium** | Phase 1 | Configurable cost factor (Task 1.5); annual OWASP review; documented migration path to Argon2id | Low — long time horizon |
| R4 | Low registration adoption | **High** | Phase 4 | UX testing before launch (Task 4.7); iterate based on SC1 funnel data; PRD targets > 60% conversion | Medium — depends on UX iteration speed |
| R5 | Security breach from implementation flaws | **High** | Phase 4 | Dedicated security review (Task 4.4); penetration testing (Task 4.5); remediation before launch | Low after testing |
| R6 | Incomplete audit logging → SOC2 failure | **High** | Phase 3 | Log schema defined early (Task 3.5); wired into all endpoints (Task 3.6); validated in QA; 12-month retention | Low — tested before launch |
| R7 | Email delivery failures blocking password reset | **Medium** | Phase 3 | Delivery monitoring (Task 3.4); fallback support channel documented; SendGrid availability confirmed as gate (Task 3.1) | Low — standard operational concern |

**Additional architectural risk**: OQ6 identifies a conflict between the spec (audit logging deferred to v1.1) and the PRD (SOC2 audit by Q3 2026). This roadmap resolves the conflict by **including audit logging in Phase 3** to meet the compliance deadline. If stakeholders override this decision, the SOC2 timeline is at risk.

---

## 4. Resource Requirements and Dependencies

### Infrastructure Prerequisites (must be available before Phase 1 starts)

| Dependency | ID | Required By | Provisioning Owner |
|------------|-----|------------|-------------------|
| PostgreSQL 15+ (dev/staging/prod) | D4 | Phase 1, Task 1.1 | DevOps/Infrastructure |
| RS256 key pair in secrets manager | D3 | Phase 1, Task 1.4 | Security/Infrastructure |
| NPM packages: jsonwebtoken, bcrypt | D1, D2 | Phase 1, Tasks 1.5–1.6 | Engineering (package install) |

### Gated Dependencies (must be available before specific phases)

| Dependency | ID | Required By | Gate |
|------------|-----|------------|------|
| Frontend routing framework | D8 | Phase 2 (UI integration) | Week 4 — API-only testing proceeds if delayed |
| Email delivery service (SendGrid) | D5 | Phase 3, Task 3.1 | **Week 6 hard gate** — FR-AUTH.5 blocked without this |
| Security Policy (SEC-POLICY-001) | D9 | Phase 1 (password/token policy) | Week 1 — defaults to NIST SP 800-63B if unavailable |

### Team Composition

| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| Backend engineer | 1–2 | 2 | 1–2 | 1 |
| Frontend engineer | 0 | 1 | 1 | 0.5 |
| Security engineer | 0.25 (review) | 0 | 0.25 (audit) | 1 (pen test) |
| QA engineer | 0.5 | 1 | 1 | 1 |
| DevOps | 0.5 (infra) | 0 | 0 | 0.5 (deploy) |

---

## 5. Success Criteria and Validation Approach

| Criterion | ID | Target | Validation Phase | Method |
|-----------|-----|--------|-----------------|--------|
| Registration conversion rate | SC1 | > 60% | Phase 4 (Task 4.7) | Funnel instrumentation: landing → register → confirmed account |
| Login response time (p95) | SC2 | < 200ms | Phase 4 (Task 4.1) | k6 load testing + production APM on `/auth/login` |
| Average session duration | SC3 | > 30 minutes | Phase 4 (Task 4.9) | Token refresh event analytics — measure time between first access token and last refresh |
| Failed login rate | SC4 | < 5% of attempts | Phase 4 (Task 4.10) | Auth event log analysis — failed logins / total login attempts |
| Password reset completion | SC5 | > 80% | Phase 4 (Task 4.8) | Funnel: reset requested → new password set (from audit logs) |
| Service availability | SC6 | 99.9% uptime | Phase 4 ongoing (Task 4.3) | Health check endpoint monitoring; rolling 30-day windows |

**Validation strategy**: SC1–SC5 are measured during Phase 4 hardening. SC6 is an ongoing operational metric established at launch. All metrics require audit logging (Phase 3) to be operational before measurement can begin.

---

## 6. Timeline Summary

```
Week  1–2   ████████  Phase 1: Foundation & Data Layer
                      M1: DB migration + core services operational

Week  3–4   ████████  Phase 2a: Registration + Login
                      M2: Registration and login functional

Week  5–6   ████████  Phase 2b: Token Refresh + Profile
                      M3: Token refresh and profile functional

Week  7–8   ████████  Phase 3a: Password Reset
                      M4: Password reset flow operational

Week    9   ████      Phase 3b: Compliance Controls
                      M5: Audit logging + GDPR verified

Week   10   ████      Phase 4a: Performance Validation
                      M6: Performance targets met

Week   11   ████      Phase 4b: Security Review
                      M7: Security review + pen test complete

Week   12   ████      Phase 4c: Launch
                      M8: Production launch
```

**Critical path**: Phase 1 → Phase 2 (login/registration) → Phase 3 (password reset, audit logging) → Phase 4 (hardening, launch)

**Parallel opportunities**: Frontend UI development can proceed in parallel with backend API work in Phase 2. Security review preparation (Task 4.4 scoping) can begin during Phase 3.

---

## 7. Open Questions — Resolution Schedule

These open questions must be resolved by the indicated phase to avoid blocking work. Architect recommendation included for each.

| # | Question | Must Resolve By | Architect Recommendation |
|---|----------|----------------|------------------------|
| OQ1 | Sync vs async password reset emails? | Phase 3 start (Week 7) | **Async via message queue** — decouples reset endpoint latency from email delivery; adds resilience; queue infrastructure cost is justified |
| OQ2 | Max active refresh tokens per user? | Phase 2 start (Week 3) | **5 tokens max** — supports multi-device (phone, laptop, tablet, work, home) without unbounded storage; oldest revoked on overflow |
| OQ3 | Account lockout policy after N failures? | Phase 2, Task 2.3 (Week 3) | **Progressive lockout**: 5 failures → 15-min lock; 10 failures → 1-hour lock; 20 failures → admin unlock required. Supplements per-IP rate limiting. |
| OQ4 | "Remember me" extending session beyond 7 days? | Phase 2, Task 2.9 (Week 5) | **Defer to v1.1** — 7-day refresh window is adequate for launch; "remember me" introduces security tradeoffs that need separate analysis |
| OQ5 | Token revocation on user deletion? | Phase 3 (Week 9) | **Cascade delete** — delete user record cascades to refresh_tokens; access tokens expire naturally within 15 minutes |
| OQ6 | Audit logging in v1.0 or v1.1? | **Already resolved in this roadmap** | **v1.0** — SOC2 Q3 2026 deadline forces this. Phase 3 includes audit logging. |
| OQ7 | GDPR consent mechanism? | Phase 2, Task 2.2 (Week 3) | **Explicit checkbox** — "I agree to [Terms] and [Privacy Policy]" with timestamp; simplest compliant implementation |
| OQ8 | Logout endpoint (in PRD, not in spec)? | Phase 2 (Week 5) | **Include in Phase 2** — add POST `/auth/logout` that revokes the user's current refresh token; low implementation cost, high UX value |
| OQ9 | JTBD #2 state persistence beyond sessions? | Pre-Phase 1 | **Out of scope for auth service** — JTBD #2 implies application-level state persistence (saved preferences, activity history), not session persistence. Confirm with Product and track separately. |

---

## 8. Scope Guardrails (from PRD Scope Definition)

The following are explicitly **out of scope** per the PRD. Any roadmap change request touching these areas requires a scope change approval:

| Capability | Status | Rationale |
|-----------|--------|-----------|
| OAuth/OIDC | Out of scope | Planned for v2.0 |
| Multi-factor authentication | Out of scope | Planned for v1.1; requires SMS/TOTP infrastructure |
| Role-based access control | Out of scope | Separate concern with dedicated PRD |
| Social login (Google, GitHub) | Out of scope | Depends on OAuth/OIDC not yet available |
| Application state persistence (JTBD #2) | Confirm out of scope (OQ9) | Auth service provides session identity, not application state |
