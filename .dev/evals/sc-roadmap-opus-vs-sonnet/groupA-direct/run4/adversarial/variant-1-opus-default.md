# Roadmap: User Authentication System

## Executive Summary

This roadmap delivers a production-grade user authentication system featuring OAuth2 (Google, GitHub), JWT-based session management with refresh tokens, role-based access control (RBAC), two-factor authentication, and comprehensive audit logging. The system is engineered to support 10,000 concurrent sessions at sub-200ms p95 latency while meeting OWASP Top 10 and GDPR compliance standards. Delivery spans 7 milestones over 22 weeks, sequenced to land core auth primitives first and layer advanced features (OAuth, 2FA, admin tooling) on a hardened foundation.

## Goals & Success Metrics

| Goal | Measurable Outcome | Source |
|------|--------------------|--------|
| G1: Performant auth APIs | p95 latency < 200ms across `/login`, `/register`, `/refresh`, `/oauth/*` measured via k6 load test | NFR-001 |
| G2: Scale to peak load | Sustain 10,000 concurrent active sessions with <1% error rate during 30-min soak test | NFR-002 |
| G3: Security posture | Zero High/Critical findings in OWASP ZAP + Snyk + manual pen-test; CSP, HSTS, secure cookies verified | NFR-003, R-001, R-002 |
| G4: Regulatory compliance | GDPR DPIA signed off; data export + erasure endpoints functional; PII encrypted (AES-256 at rest, TLS 1.3 in transit) | NFR-004, NFR-006, R-004 |
| G5: Service availability | 99.9% uptime SLO over rolling 30-day window; multi-AZ deployment with health-checked failover | NFR-005 |
| G6: Functional completeness | 100% of FR-001 through FR-012 acceptance criteria pass in staging | All FRs |
| G7: Auditability | 100% of auth events (login, logout, password reset, role change, OAuth link/unlink, 2FA enable/disable, lockout) logged to immutable store | FR-009 |

## Milestones

### M1 — Foundation & Infrastructure (Weeks 1-2)

**Goal**: Stand up the runtime, data layer, and CI/CD scaffolding the auth service will run on.

**Deliverables**:

- D1.1: Dockerized service skeleton (Node.js 20 LTS or Python 3.12, team choice ratified in Open Questions) with multi-stage build, health endpoint `/healthz`
- D1.2: PostgreSQL 15 schema migrations (Flyway/Alembic) for `users`, `roles`, `permissions`, `user_roles`, `audit_events`, `refresh_tokens`, `oauth_identities`, `password_resets`, `mfa_secrets`
- D1.3: Redis 7 cluster provisioned with TLS, AUTH enabled; namespaces `sess:`, `rl:`, `lock:`, `verify:` documented
- D1.4: CI/CD pipeline (GitHub Actions) running lint, unit tests, container scan (Trivy), and ephemeral preview deploys
- D1.5: Secrets management via Vault/AWS Secrets Manager; no secrets in env files committed
- D1.6: Observability baseline: structured JSON logs, OpenTelemetry traces, Prometheus metrics endpoint

**Mapped IDs**: NFR-005, NFR-006 (encryption at rest config), Dependencies (PostgreSQL 15+, Redis, Docker)

**Entry Criteria**: Cloud accounts provisioned, repo access granted, architecture decision record (ADR) for language/framework merged.

**Exit Criteria**: `docker compose up` brings the stack up locally; preview deploy passes smoke test; migrations apply cleanly on empty DB.

**Estimated Duration**: 2 weeks

---

### M2 — Core Identity: Registration, Login, JWT (Weeks 3-5)

**Goal**: Deliver password-based auth with email verification and JWT issuance — the backbone every later milestone depends on.

**Deliverables**:

- D2.1: `POST /auth/register` with Argon2id password hashing (memoryCost 64MB, parallelism 2), zxcvbn strength check, duplicate-email check
- D2.2: Email verification flow via SendGrid: signed token (HS256, 24h TTL), `GET /auth/verify?token=...`, resend endpoint with rate limit
- D2.3: `POST /auth/login` returning access JWT (RS256, 15-min TTL) + refresh token (opaque, 7-day TTL, stored hashed in `refresh_tokens`)
- D2.4: JWT validation middleware with JWKS endpoint `/.well-known/jwks.json` and key rotation runbook
- D2.5: HTTP-only, Secure, SameSite=Strict cookie for refresh token; access token in Authorization header
- D2.6: Unit + integration test coverage ≥85% on auth handlers; contract tests for token shape

**Mapped IDs**: FR-001, FR-002, NFR-001 (latency budget enforced via test), NFR-006 (TLS, hashed tokens), R-001 (HTTP-only cookies)

**Entry Criteria**: M1 exit criteria met; SendGrid API key provisioned; RS256 keypair generated and stored in Vault.

**Exit Criteria**: Postman collection demonstrates register → verify email → login → access protected endpoint; load test confirms `/login` p95 < 200ms at 500 RPS.

**Estimated Duration**: 3 weeks

**Edge Cases Covered**: Empty-state (first user in DB, no admin yet → bootstrap admin script in D2.7); duplicate registration; expired verification token; clock skew on JWT `iat`/`exp`; refresh-token replay (rotated on use, old hash invalidated).

---

### M3 — Session Management & Rate Limiting (Weeks 6-7)

**Goal**: Make sessions resilient, revocable, and protected against brute-force and credential-stuffing attacks.

**Deliverables**:

- D3.1: `POST /auth/refresh` with token rotation (one-time-use refresh tokens, family tracking for reuse detection → invalidates entire family)
- D3.2: `POST /auth/logout` (single session) and `POST /auth/logout-all` (revoke all refresh tokens for user)
- D3.3: Per-user + per-IP rate limiting via Redis sliding window: 5 login attempts / 15 min per (IP, email), 100 req/min per authenticated user on sensitive endpoints
- D3.4: Account lockout: 10 failed attempts → 30-min lockout, exponential backoff on subsequent rounds; unlock via email link
- D3.5: Session store keyed by `jti`; `GET /auth/sessions` lists active sessions with device/IP metadata; `DELETE /auth/sessions/:id` revokes
- D3.6: Load test scenario: 10,000 concurrent WebSocket-style polling clients holding sessions, verifying NFR-002

**Mapped IDs**: FR-006, FR-008, NFR-002, R-002

**Entry Criteria**: M2 exit; Redis cluster benchmarked at ≥50K ops/sec.

**Exit Criteria**: 10K concurrent session soak test passes (<1% error, p95 < 200ms); refresh-token reuse triggers family invalidation in pen-test scenario.

**Estimated Duration**: 2 weeks

**Edge Cases Covered**: Clock-skew between API nodes for rate-limit windows (Redis as authoritative clock); legitimate refresh after near-expiry; concurrent refresh from same client (idempotency token).

---

### M4 — OAuth2 Providers & Account Linking (Weeks 8-10)

**Goal**: Enable Google and GitHub sign-in with safe account linking and an email/password fallback.

**Deliverables**:

- D4.1: OAuth2 Authorization Code + PKCE flow for Google (`openid email profile` scopes) at `GET /auth/oauth/google/start` and `/callback`
- D4.2: Same flow for GitHub (`read:user user:email` scopes)
- D4.3: `oauth_identities` table linking `(provider, provider_user_id)` → `users.id`; email-match auto-link with explicit user confirmation
- D4.4: Provider-down fallback: circuit breaker (Resilience4j/opossum) opens after 5 consecutive failures → UI surfaces email/password option with clear messaging
- D4.5: State parameter (CSRF) and nonce (replay protection) validated server-side; redirect_uri allowlist
- D4.6: `POST /auth/oauth/unlink` requiring password verification if it's the only identity, blocks otherwise

**Mapped IDs**: FR-003, R-003, NFR-003 (OAuth state/nonce mitigates OWASP A01/A07)

**Entry Criteria**: M2 exit; Google + GitHub OAuth apps registered, client secrets in Vault.

**Exit Criteria**: End-to-end test passes for both providers in staging; chaos test simulating provider 503 confirms fallback path; OWASP ASVS L2 OAuth checklist signed off.

**Estimated Duration**: 3 weeks

---

### M5 — RBAC & Two-Factor Authentication (Weeks 11-14)

**Goal**: Add authorization (roles/permissions) and step-up authentication (TOTP-based 2FA).

**Deliverables**:

- D5.1: Role model: `roles` (id, name, description), `permissions` (id, resource, action), `role_permissions`, `user_roles`; seed roles `admin`, `user`, `auditor`, `support`
- D5.2: Authorization middleware `requirePermission('users:write')` enforced on protected endpoints; permissions claim in JWT (scoped, ≤2KB to avoid header bloat — overflow falls back to server-side lookup with 30s cache)
- D5.3: `POST /auth/2fa/setup` issues TOTP secret + QR (RFC 6238, SHA-1, 30s window, 6 digits); `POST /auth/2fa/verify` confirms enrollment
- D5.4: Login flow extended: when 2FA enabled, `/auth/login` returns `mfa_required: true` + short-lived (5-min) MFA challenge token; `POST /auth/2fa/challenge` exchanges challenge + TOTP for full JWT
- D5.5: 10 single-use recovery codes generated at enrollment, hashed (Argon2id) and stored; `POST /auth/2fa/recovery` accepts a code, consumes it, prompts re-enrollment
- D5.6: Admin role-assignment APIs `POST /admin/users/:id/roles` (audited)

**Mapped IDs**: FR-004, FR-007, NFR-003 (broken access control mitigation)

**Entry Criteria**: M3 exit; design review of permission taxonomy approved by product + security.

**Exit Criteria**: Authorization integration tests cover positive + negative paths for every seeded role; 2FA enrollment, login challenge, and recovery flows pass; recovery codes single-use enforced.

**Estimated Duration**: 4 weeks

**Edge Cases Covered**: User with no roles (deny-by-default); revoking a role mid-session (server-side check, JWT short TTL bounds staleness ≤15 min); 2FA secret leaked → recovery + force re-enroll runbook; clock-drift on TOTP (±1 window tolerance).

---

### M6 — Password Reset, Profile, Audit Logging (Weeks 15-17)

**Goal**: Round out user-facing flows and stand up the immutable audit trail required for compliance.

**Deliverables**:

- D6.1: `POST /auth/password/forgot` issues signed reset token (HS256, 1h TTL, single-use, hashed in `password_resets`) and emails via SendGrid; constant-time response regardless of email existence
- D6.2: `POST /auth/password/reset` verifies token, applies new password (zxcvbn + history check, last 5), invalidates all refresh tokens
- D6.3: Profile endpoints: `GET /me`, `PATCH /me` (name, avatar URL, locale, timezone), `POST /me/email/change` (re-verification required)
- D6.4: Audit event taxonomy: `auth.login.success|failure`, `auth.logout`, `auth.password.reset.requested|completed`, `auth.2fa.enabled|disabled`, `auth.oauth.linked|unlinked`, `rbac.role.assigned|revoked`, `account.deactivated|reactivated`
- D6.5: Audit sink: append-only table `audit_events` with hash-chain (each row contains SHA-256 of prior row's canonicalized payload) for tamper-evidence; daily export to S3 with object-lock
- D6.6: GDPR endpoints: `GET /me/export` (JSON dump within 30 days, async job), `DELETE /me` (soft-delete + 30-day grace, then crypto-shred)

**Mapped IDs**: FR-005, FR-009, FR-010, FR-012, NFR-004, NFR-006, R-004

**Entry Criteria**: M5 exit; DPO/legal review of audit retention and GDPR endpoints scheduled.

**Exit Criteria**: All audit event types verified emitted in integration tests; hash-chain tamper test passes; export job completes for synthetic user with 10K events in <60s.

**Estimated Duration**: 3 weeks

---

### M7 — Admin Dashboard, Hardening, Launch Readiness (Weeks 18-22)

**Goal**: Operational tooling, security hardening, and production launch gate.

**Deliverables**:

- D7.1: Admin dashboard (React + Vite) with user list, search, view profile, force-logout, reset-password, assign/revoke roles, view audit trail per user, deactivate/reactivate
- D7.2: Admin dashboard authz: `admin` role required, all actions audited with actor + target + before/after diff
- D7.3: Account deactivation workflow: user-initiated (D6.6) and admin-initiated (D7.1); 30-day grace with cancel-link email; crypto-shred PII at grace expiry while preserving audit references via tokenized user_id
- D7.4: Security hardening pass: CSP (no `unsafe-inline`), HSTS (`max-age=31536000; preload`), X-Frame-Options DENY, secure cookies, dependency audit (Snyk), OWASP ZAP baseline scan → zero High/Critical
- D7.5: Third-party penetration test engagement; findings remediated to Medium-or-lower before launch
- D7.6: Multi-AZ production deploy (≥2 AZs, RDS multi-AZ, Redis replication group); chaos test killing one AZ confirms <30s RTO
- D7.7: Runbooks: key rotation, OAuth client rotation, incident response (suspected breach), 2FA recovery override, GDPR request handling
- D7.8: Launch readiness review: capacity plan signed off, SLO dashboards live, on-call rota staffed, GDPR DPIA signed

**Mapped IDs**: FR-011, FR-012, NFR-003, NFR-004, NFR-005, R-001, R-002, R-004

**Entry Criteria**: M6 exit; pen-test vendor engaged; SRE on-call rota proposed.

**Exit Criteria**: All NFRs verified in staging matching production topology; go/no-go meeting approves launch; rollback plan rehearsed.

**Estimated Duration**: 5 weeks

---

## Dependency Graph

```
M1 (Foundation)
 └─> M2 (Core Identity)
      ├─> M3 (Sessions + Rate Limiting)
      │    └─> M5 (RBAC + 2FA)
      │         └─> M6 (Reset + Profile + Audit)
      │              └─> M7 (Admin + Hardening + Launch)
      └─> M4 (OAuth)  ──> M5  (M5 RBAC also gates OAuth-issued tokens)
```

**Critical Path**: M1 → M2 → M3 → M5 → M6 → M7 (20 weeks). M4 runs parallel to M3 starting Week 8 but must complete before M5 finishes since OAuth-issued sessions need RBAC.

**Explicit Blockers**:

- D5.2 (authz middleware) blocks D7.1 (admin dashboard) — admin role enforcement
- D3.1 (refresh rotation) blocks D6.2 (password reset invalidating tokens)
- D6.4 (audit taxonomy) blocks D7.1 (admin actions must emit audit events)
- D4.1/D4.2 (OAuth flows) block D5.4 (2FA challenge must integrate with OAuth-initiated sessions)
- D1.2 (schema) blocks every later DB-touching deliverable

## Risk Register

| ID | Risk | Impact | Probability | Mitigation | Milestone(s) |
|----|------|--------|------------|------------|--------------|
| R-001 | Token theft via XSS | High | Medium | HTTP-only + Secure + SameSite=Strict cookies for refresh token (D2.5); CSP header without `unsafe-inline` (D7.4); access token kept in memory (not localStorage) per frontend integration guide | M2, M7 |
| R-002 | Brute force / credential stuffing | High | High | Sliding-window rate limiting (D3.3); progressive account lockout (D3.4); CAPTCHA on Nth attempt (D3.4 stretch); breached-password check against HIBP k-anonymity API at registration + reset (D2.1, D6.2) | M3, M6 |
| R-003 | OAuth provider downtime | Medium | Low | Circuit breaker with email/password fallback path (D4.4); status-page monitor; provider health surfaced in UI | M4 |
| R-004 | Data breach of PII | Critical | Low | AES-256 at rest (RDS encryption, D1.2); TLS 1.3 in transit; least-privilege IAM; audit-trail on PII access; crypto-shred on deletion (D7.3); pen-test (D7.5) | M1, M6, M7 |
| R-005 (new) | JWT signing key compromise | Critical | Low | RS256 with key in Vault; quarterly rotation runbook (D7.7); JWKS `kid` header allows zero-downtime rotation; short access-token TTL (15min) bounds blast radius | M2, M7 |
| R-006 (new) | SendGrid outage blocks verification + reset | Medium | Medium | Secondary SMTP provider (SES) configured as failover; verification token reissue endpoint; document degraded-mode SLA in runbook | M2, M6 |
| R-007 (new) | RBAC misconfiguration → privilege escalation | High | Medium | Deny-by-default middleware; permission matrix peer-reviewed (D5.1); negative-path integration tests (D5.6 exit); admin role assignments audited (D5.6) | M5 |
| R-008 (new) | 2FA recovery-code abuse | High | Low | Argon2id-hashed codes, single-use, count surfaced to user, force re-enroll after any use; alert email on recovery use | M5 |
| R-009 (new) | Audit-log tampering by privileged insider | High | Low | Hash-chained rows (D6.5); daily S3 export with object-lock; separation of duties — admins cannot delete audit rows via app | M6 |
| R-010 (new) | GDPR erasure conflicts with audit retention | Medium | Medium | Tokenize `user_id` in audit table; PII fields crypto-shredded at erasure while audit references survive; legal sign-off in D7.8 | M6, M7 |
| R-011 (new) | Refresh-token theft (offline) | High | Low | Refresh tokens stored hashed (SHA-256), one-time-use with family-reuse detection (D3.1) auto-invalidates family + alerts user | M3 |
| R-012 (new) | Time-of-check/time-of-use on role revocation | Medium | Medium | Access-token TTL ≤15min bounds staleness; admin force-logout (D7.1) invalidates refresh-token family immediately | M5, M7 |

## Open Questions

1. **Language/framework**: Node.js/Express vs Python/FastAPI vs Go/Gin? Affects D1.1, library choices for Argon2/JWT/OAuth. Decision needed before M1 kickoff.
2. **Tenancy model**: Single-tenant or multi-tenant from day one? Schema in D1.2 needs `organization_id` if multi-tenant — retrofitting is expensive.
3. **JWT claims contract**: Final list of claims (`sub`, `email`, `roles[]`, `permissions[]` or `scope`, `mfa_verified`, `tenant_id`?) — needed by Week 3 (D2.3).
4. **Password policy**: Min length, max length, special-char requirement, zxcvbn score threshold? NIST SP 800-63B suggests min 8, no composition rules — confirm with security.
5. **Audit retention**: How long are audit events retained (12mo? 7yr for SOX-adjacent?) — affects D6.5 storage sizing and GDPR balancing.
6. **OAuth account linking policy**: Auto-link on matching verified email, or always require explicit user action? Affects D4.3 UX and security posture.
7. **2FA enforcement**: Optional for all users, required for `admin` role, required for all users? Affects D5.3 and admin onboarding flow.
8. **Email deliverability**: Dedicated IP on SendGrid vs shared? SPF/DKIM/DMARC owner? Affects verification + reset reliability (R-006).
9. **Rate-limit tuning**: Are the proposed thresholds (5 logins / 15min) acceptable for legitimate shared-IP users (corporate NATs, mobile carriers)? May need per-account + per-IP composite scoring.
10. **Admin dashboard hosting**: Same domain as API (cookie sharing) or separate subdomain (CORS + cookie scope decisions)? Affects D7.1 and security review.
11. **GDPR data-residency**: EU-only data residency required? Affects RDS region and possibly architecture.
12. **Out-of-band password reset throttling**: Max reset requests per email per day to limit email bombing — needs threshold (suggest 3/day).

## Out of Scope

Mirrored from source spec:

- Biometric authentication (fingerprint, face ID)
- Hardware security keys (WebAuthn / FIDO2 / YubiKey support)
- Custom SSO protocol implementation (SAML, custom OIDC server)

Deferred by this roadmap (revisit post-launch):

- SCIM provisioning for enterprise customers
- Passwordless / magic-link login
- Push-notification-based 2FA (vs current TOTP-only)
- Federated identity beyond Google/GitHub (Microsoft, Apple, Facebook)
- Anomaly-based adaptive authentication (geo/device risk scoring)
- Self-service consent / app-authorization screens (full OAuth2 *server* role)
- Mobile SDKs (web-only at launch; mobile uses same REST API)

## Success Criteria

| Spec Criterion | Satisfying Milestone(s) | Evidence |
|----------------|-------------------------|----------|
| All FR requirements implemented and tested | M2 (FR-001, FR-002), M3 (FR-006, FR-008), M4 (FR-003), M5 (FR-004, FR-007), M6 (FR-005, FR-009, FR-010, FR-012), M7 (FR-011, FR-012) | Test report aggregated at D7.8 gate |
| OWASP compliance verified via security scan | M7 (D7.4 ZAP + Snyk, D7.5 pen-test) | Scan reports + remediation tracker |
| Load testing confirms 10K concurrent sessions | M3 (D3.6) re-verified at M7 (D7.6) in prod-like topology | k6 report archived |
| OAuth2 flow works for Google and GitHub | M4 (D4.1, D4.2) | E2E test recordings + staging demo |
| Audit logs capture all auth events | M6 (D6.4, D6.5) verified by M7 admin dashboard cross-check | Audit-event coverage matrix |

**Launch Gate (D7.8)**: All five rows above show green; pen-test residual risks ≤ Medium; SLO dashboards green for 7 consecutive days in staging soak.
