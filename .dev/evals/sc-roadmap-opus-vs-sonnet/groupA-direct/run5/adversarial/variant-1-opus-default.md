# User Authentication System — Implementation Roadmap

**Variant:** variant-1-opus-default
**Generated:** 2026-05-22
**Source Specification:** `/config/workspace/IronClaude/tests/sc-roadmap/fixtures/sample_spec.md`
**Total Estimated Duration:** 18 weeks (5 milestones, sequential with limited parallelism)
**Target Stack:** PostgreSQL 15.4+, Redis 7.2+, SendGrid v3 API, Docker 24+, Node.js 20 LTS (reference; the spec does not pin a language — substitute equivalents if implementing in Python/Go)

---

## Executive Summary

This roadmap delivers a production-grade User Authentication System that combines email/password registration, JWT-based session management with refresh tokens, third-party OAuth2 (Google, GitHub), role-based access control (RBAC), and two-factor authentication (2FA) into a single hardened service. The system is designed to satisfy OWASP Top 10 (2021) and GDPR obligations from day one, support 10,000 concurrent sessions on a horizontally scaled Redis-backed deployment, and emit a complete audit trail for compliance investigations.

The build is sequenced as 5 milestones over 18 weeks. M1 establishes the foundation (data model, crypto primitives, dev infrastructure). M2 ships the core identity surface (registration, login, password reset). M3 layers OAuth2 federation and the RBAC engine. M4 introduces hardening features (2FA, rate limiting, audit logging) that directly mitigate the spec's four named risks. M5 delivers the operator-facing surface (admin dashboard, profile management, account deactivation) and concludes with load testing and a security audit gate before GA.

The sequencing is deliberate: every cross-cutting concern (encryption at rest/in transit, OWASP controls, observability) is introduced in M1 and reinforced thereafter, so no milestone ships features without its security and observability tail. Risk mitigations are not deferred — R-001 (XSS/token theft) and R-002 (brute force) are addressed in M2 and M4 respectively, not punted to a post-launch hardening sprint.

---

## Milestones

### M1 — Foundation & Security Primitives (Weeks 1–3)

**Goal:** Stand up the database schema, secret management, crypto primitives, containerized dev/CI environment, and observability spine. Nothing ships to end users in this milestone, but every subsequent milestone depends on its outputs.

**Source-spec coverage:**

- Dependencies: PostgreSQL 15+, Redis, Docker
- NFR-003 (OWASP baseline), NFR-004 (GDPR baseline), NFR-006 (encryption at rest and in transit)
- Risk groundwork for R-001, R-004

**Deliverables:**

- **D1.1** PostgreSQL 15.4 schema (`users`, `roles`, `permissions`, `user_roles`, `refresh_tokens`, `oauth_identities`, `audit_events`, `password_reset_tokens`, `mfa_secrets`) with PII columns (email, phone, name) encrypted using `pgcrypto` AES-256-GCM and per-column key references managed by AWS KMS / HashiCorp Vault.
- **D1.2** Redis 7.2 cluster configuration with TLS 1.3 in transit, AOF persistence enabled, and key-namespace conventions (`session:*`, `ratelimit:*`, `lockout:*`).
- **D1.3** Docker Compose stack (`postgres`, `redis`, `mailhog` for dev SMTP, `auth-api`) + production Dockerfile using a distroless or `node:20-alpine` base image with non-root user.
- **D1.4** Crypto utility module: Argon2id password hashing (m=64MB, t=3, p=4 per OWASP ASVS 4.0 §2.4), JWT signing keys (RS256, 2048-bit RSA), CSRF token generator.
- **D1.5** Observability baseline: OpenTelemetry SDK wired for traces and metrics; structured JSON logs to stdout; Prometheus `/metrics` endpoint exposing `http_request_duration_seconds`, `auth_events_total`, `db_query_duration_seconds`.
- **D1.6** CI pipeline (GitHub Actions): lint, unit tests, SAST (Semgrep with `p/owasp-top-ten` ruleset), dependency vulnerability scan (`npm audit --audit-level=high` or `pip-audit`), container image scan (Trivy).
- **D1.7** Threat model document (STRIDE-style) covering all 12 FRs and explicit mappings to R-001..R-004.

**Dependencies:** None (start milestone).

**Acceptance criteria:**

- `docker compose up` brings the stack to a healthy state in < 60s on a 4-core dev machine.
- All PII columns reject inserts of plaintext via a test that bypasses the application layer and asserts ciphertext.
- CI run on a sample PR completes in < 8 minutes end-to-end.
- Crypto module passes 100% of test vectors (RFC 9106 Argon2 test vectors, RFC 7519 JWT round-trip tests).
- Threat model is reviewed and signed off by at least one security reviewer.

**Estimated duration:** 3 weeks.

---

### M2 — Core Identity: Registration, Login, Password Reset (Weeks 4–7)

**Goal:** Ship the primary email/password identity flows with JWT access tokens and refresh tokens. This is the first milestone with user-facing endpoints.

**Source-spec coverage:**

- FR-001 (registration with email verification)
- FR-002 (login with JWT generation)
- FR-005 (password reset via email)
- FR-006 (session management with refresh tokens)
- NFR-001 (< 200ms p95 for auth endpoints)
- NFR-003 (OWASP — token handling, password storage)
- NFR-006 (encryption in transit for all flows)
- R-001 (XSS/token theft mitigation via cookie hardening)

**Deliverables:**

- **D2.1** `POST /auth/register` — accepts `email`, `password`, `name`; enforces password policy (≥12 chars, NIST SP 800-63B style — no composition rules, but a 10K-entry breached-password denylist via HIBP k-anonymity API or local bloom filter); Argon2id-hashes password; creates user in `pending_verification` state; emits verification token (32 bytes, base64url, 24h TTL).
- **D2.2** `POST /auth/verify-email` — consumes the verification token, atomically transitions user to `active`.
- **D2.3** SendGrid integration via `@sendgrid/mail` (or equivalent) using dynamic templates for verification, password reset, and 2FA enrollment emails; bounce/spam webhook handler.
- **D2.4** `POST /auth/login` — returns short-lived (15 min) RS256 JWT access token and a long-lived (30 day) refresh token. Refresh tokens are opaque random 32-byte strings stored hashed (SHA-256) in `refresh_tokens` with `user_id`, `family_id`, `issued_at`, `expires_at`, `revoked_at`. Refresh-token rotation with reuse detection per OAuth 2.0 BCP (RFC 9700 §2.2.2).
- **D2.5** `POST /auth/refresh` — rotates refresh tokens; reuse of an already-rotated token revokes the entire token family (mitigates R-001 token replay).
- **D2.6** `POST /auth/logout` — revokes refresh-token family, clears cookies.
- **D2.7** `POST /auth/password-reset/request` and `POST /auth/password-reset/confirm` — single-use reset tokens (32 bytes, 1h TTL), constant-time email-existence response to prevent enumeration.
- **D2.8** Cookie strategy: refresh token set as `HttpOnly`, `Secure`, `SameSite=Strict`; access token returned in response body (consumed by SPA in memory, not localStorage) — directly mitigates R-001.
- **D2.9** Content Security Policy header default: `default-src 'self'; frame-ancestors 'none'; object-src 'none'`; HSTS `max-age=63072000; includeSubDomains; preload`.
- **D2.10** Integration test suite covering all flows, achieving ≥90% line coverage on the M2 module.

**Dependencies:** M1 (D1.1, D1.2, D1.4, D1.5).

**Acceptance criteria:**

- p95 latency for `/auth/login` and `/auth/refresh` ≤ 200ms under a 100 RPS sustained load (k6 or Locust harness) — verifies NFR-001.
- Refresh-token reuse triggers family revocation in < 1s, verified by automated test.
- ZAP baseline scan against the deployed test environment produces zero `High` or `Medium` findings against the M2 endpoints.
- Verification and password-reset emails arrive within 30s in a SendGrid sandbox test.
- Manual review confirms no auth token is ever written to localStorage or a non-`HttpOnly` cookie.

**Estimated duration:** 4 weeks.

---

### M3 — Federation & Authorization: OAuth2 + RBAC (Weeks 8–10)

**Goal:** Add Google and GitHub as identity providers, implement the role/permission model, and wire authorization checks into the request pipeline.

**Source-spec coverage:**

- FR-003 (OAuth2 integration — Google, GitHub)
- FR-004 (role-based access control)
- R-003 (OAuth provider downtime → fallback to email/password)
- NFR-003 (OWASP — authorization, OAuth state handling)

**Deliverables:**

- **D3.1** OAuth2 Authorization Code flow with PKCE (RFC 7636, S256 method) for Google (`accounts.google.com`) and GitHub (`github.com/login/oauth`). Use `openid-client` (Node) or `authlib` (Python) — pinned to a current major version verified against the provider's published OIDC discovery document.
- **D3.2** `GET /auth/oauth/:provider/start` — generates `state` (32-byte random, stored in short-lived Redis key) and `code_verifier`, redirects to provider.
- **D3.3** `GET /auth/oauth/:provider/callback` — validates `state`, exchanges code for tokens, fetches userinfo, links to existing user by verified email or creates a new account; writes `oauth_identities` row.
- **D3.4** Account linking endpoint `POST /auth/oauth/link` for users already authenticated via email/password.
- **D3.5** RBAC engine: `roles` (e.g., `admin`, `user`, `support`), `permissions` (e.g., `users.read`, `users.deactivate`, `audit.read`), `role_permissions` join. Resolution cached in Redis for 60s per user. Default roles seeded via migration.
- **D3.6** Authorization middleware: `requirePermission('users.deactivate')` declarative guard usable on every protected route; returns 403 with a structured error code.
- **D3.7** Provider-outage fallback: circuit breaker (e.g., `opossum` or `pybreaker`) on OAuth provider calls; on open-circuit, the OAuth start endpoint surfaces a user-facing banner directing to email/password login — directly mitigates R-003. A 5xx rate > 25% over a 60s window opens the circuit for 5 minutes.
- **D3.8** Contract tests against Google's and GitHub's published OIDC/OAuth discovery endpoints, run nightly in CI to detect upstream changes.

**Dependencies:** M2 (user records, JWT issuance pipeline must exist).

**Acceptance criteria:**

- End-to-end test with stubbed Google and GitHub providers (using `nock` / `responses` recordings) completes the full Auth Code + PKCE flow.
- A user authenticated via Google can be promoted to `admin`, and a protected endpoint correctly returns 403 to a `user`-role caller and 200 to the `admin`.
- Simulated 100% Google outage (provider returns 503) does not block email/password login; the OAuth-start endpoint returns a 503 with `Retry-After` and the UI fallback path is exercised in an integration test.
- Authorization middleware adds ≤ 5ms p95 overhead per request (measured by removing the middleware in a control build).

**Estimated duration:** 3 weeks.

---

### M4 — Hardening: 2FA, Rate Limiting, Audit Logging (Weeks 11–14)

**Goal:** Add the controls that directly mitigate the spec's two highest-probability risks (R-002 brute force, R-001 token theft) and close the GDPR/compliance audit trail.

**Source-spec coverage:**

- FR-007 (two-factor authentication)
- FR-008 (API rate limiting per user)
- FR-009 (audit logging for auth events)
- NFR-002 (10K concurrent sessions — rate-limit infrastructure must scale)
- NFR-003 (OWASP — authentication, logging & monitoring)
- NFR-004 (GDPR — audit trail, data subject access)
- NFR-005 (99.9% uptime — rate limiting prevents resource exhaustion)
- R-001 (XSS — 2FA defense-in-depth)
- R-002 (brute force — rate limiting + lockout)
- R-004 (PII breach — audit trail enables forensics)

**Deliverables:**

- **D4.1** TOTP-based 2FA per RFC 6238 (SHA-1, 30s step, 6 digits) via a vetted library (`speakeasy`, `pyotp`); QR-code enrollment using `otpauth://` URI; recovery codes (10 single-use codes, 10 chars each, hashed at rest with Argon2id).
- **D4.2** `POST /auth/2fa/enroll`, `POST /auth/2fa/verify`, `POST /auth/2fa/disable`. 2FA is opt-in for `user` role and mandatory for `admin` role (enforced at login).
- **D4.3** Login flow upgrade: when a 2FA-enabled user authenticates with primary factor, server returns a short-lived (5 min) `mfa_pending` token; full JWT is issued only after `/auth/2fa/challenge` succeeds.
- **D4.4** Rate limiting: token-bucket algorithm in Redis using Lua script for atomicity. Per-user limits: 5 failed logins / 15 min triggers a 15-min lockout; 100 auth-endpoint requests / 1 min per user; 30 password-reset requests / 1h per IP. Per-IP global limit: 1000 requests / min. Limits returned via `X-RateLimit-*` headers; 429 response includes `Retry-After`.
- **D4.5** Account lockout: after 5 consecutive failed logins, lock for 15 min; after 3 such lockout cycles, require password reset. Locked-account state stored in Redis with TTL; mirrored to `users.locked_until` on lockout to survive Redis loss.
- **D4.6** Audit logging: structured `audit_events` rows for every event in {register, verify_email, login_success, login_failure, logout, password_reset_request, password_reset_complete, 2fa_enroll, 2fa_disable, oauth_link, role_grant, role_revoke, account_deactivate, account_reactivate, admin_action}. Each row: `event_type`, `user_id`, `actor_id`, `ip`, `user_agent`, `request_id`, `result`, `metadata_jsonb`, `created_at`. Append-only via PostgreSQL trigger that rejects `UPDATE`/`DELETE` except by a dedicated retention role.
- **D4.7** Audit-log retention: 13 months hot in PostgreSQL, then archived to S3 (or equivalent) with object-lock for 7-year retention per common SOC2/GDPR practice.
- **D4.8** GDPR data-subject endpoints: `GET /me/export` (returns JSON of all user-owned rows), `POST /me/erase` (soft-deletes user, redacts PII columns to `<redacted>`, retains audit rows by user-id reference).

**Dependencies:** M2 (login flow to extend), M3 (RBAC roles for admin-mandatory 2FA).

**Acceptance criteria:**

- A scripted brute-force attack (1000 attempts/min from 1 IP, 50 attempts/min per user) is fully blocked: zero successful logins, account locked within 5 attempts, IP rate-limited within 1 minute. Verifies R-002 mitigation.
- TOTP enrollment and verification work against Google Authenticator and Authy reference apps.
- Audit log captures all 15 event types in an end-to-end test that exercises each flow.
- `POST /me/erase` removes PII from `users` row while leaving `audit_events.user_id` intact for legal hold (verified by SQL inspection).
- Rate-limiter load test: 10,000 concurrent users at steady-state with rate limiting enabled shows < 1% rate-limiter overhead in tail latency.

**Estimated duration:** 4 weeks.

---

### M5 — Admin Surface, Profile Management, Deactivation, GA Hardening (Weeks 15–18)

**Goal:** Deliver the remaining user-facing and operator-facing surfaces, then complete load testing, security audit, and production readiness review for general availability.

**Source-spec coverage:**

- FR-010 (user profile management)
- FR-011 (admin dashboard for user management)
- FR-012 (account deactivation workflow)
- NFR-001 (sustained < 200ms p95 at target load)
- NFR-002 (10K concurrent sessions verified under load)
- NFR-003 (OWASP audit complete)
- NFR-004 (GDPR sign-off)
- NFR-005 (99.9% uptime — SLO instrumentation + runbook)
- R-004 (PII breach — final access-control + encryption review)

**Deliverables:**

- **D5.1** Profile endpoints: `GET /me`, `PATCH /me` (name, locale, timezone, avatar URL), `POST /me/email/change` (re-verification required), `POST /me/password/change` (current-password required).
- **D5.2** Admin dashboard (server-rendered or SPA — implementation choice): user search, filter by role/status/last-login, view audit trail per user, grant/revoke roles, force password reset, force logout (revoke all refresh-token families), enable/disable 2FA enforcement for a user. All admin actions are themselves audited (`actor_id` ≠ `user_id` case).
- **D5.3** Account deactivation: `POST /me/deactivate` (self-service, requires password + 2FA if enabled) and admin equivalent. Deactivation revokes all sessions, blocks login with a clear error, sends confirmation email. A 30-day grace period during which the user can reactivate via password reset; after 30 days an automated job runs the GDPR erasure (D4.8) workflow unless legal hold is set.
- **D5.4** Production deployment manifests (Kubernetes Helm chart or equivalent) with: horizontal pod autoscaler keyed on CPU + custom `concurrent_sessions` metric, PodDisruptionBudget min-available=2, readiness/liveness probes hitting `/health/ready` and `/health/live`.
- **D5.5** SLO instrumentation: 99.9% availability burn-rate alerts (fast 2% / 1h, slow 5% / 6h windows), p95 latency alerts, error-budget dashboard.
- **D5.6** Load test: k6 scenario ramping to 10,000 concurrent active sessions (mix of login, refresh, profile read, RBAC-protected calls) sustained for 30 minutes, asserting p95 < 200ms and zero 5xx — verifies NFR-001 and NFR-002.
- **D5.7** External penetration test or security audit covering OWASP Top 10 (2021) — A01..A10 — with findings triaged and all `High`/`Critical` remediated before GA.
- **D5.8** Incident response runbook: token-compromise revocation procedure, mass password-reset procedure, OAuth-provider-outage procedure, PII-breach notification procedure (GDPR Art. 33 — 72h notification).
- **D5.9** GA readiness review sign-off (security, SRE, product, legal/privacy).

**Dependencies:** M2, M3, M4.

**Acceptance criteria:**

- Load test sustains 10,000 concurrent sessions for 30 minutes with p95 < 200ms on `/auth/login`, `/auth/refresh`, `/me`, and RBAC-guarded endpoints.
- External pen-test report shows zero unresolved `High` or `Critical` OWASP Top 10 findings.
- Admin can deactivate a user via the dashboard; the user's next login attempt returns the documented `account_deactivated` error; an `account_deactivate` audit event is recorded with the admin's `actor_id`.
- 30-day deactivation-to-erasure job runs in staging against a fast-forwarded clock and produces the same outcome as the manual `POST /me/erase` flow.
- 99.9% availability SLO dashboard is live and burn-rate alerts fire correctly in a staged failure injection.

**Estimated duration:** 4 weeks.

---

## Cross-Cutting Concerns

### Security

- **Encryption in transit (NFR-006):** TLS 1.3 minimum on all ingress; mTLS between auth-api and PostgreSQL/Redis where the deployment topology supports it. HSTS enforced from M2 onward.
- **Encryption at rest (NFR-006):** PII columns encrypted at the column level (M1); database volumes encrypted at the disk level (cloud-provider KMS or LUKS). Backup encryption verified quarterly.
- **OWASP Top 10 2021 mapping (NFR-003):** A01 Broken Access Control → RBAC middleware (M3); A02 Cryptographic Failures → Argon2id, RS256, AES-256-GCM (M1); A03 Injection → parameterized queries enforced by ORM, zero raw SQL; A04 Insecure Design → threat model (M1); A05 Security Misconfiguration → CIS-benchmarked base images, security headers (M2); A06 Vulnerable Components → Trivy + dependency scan in CI (M1); A07 Identification & Auth Failures → all of M2/M3/M4; A08 Software & Data Integrity → signed container images, SBOM generation; A09 Logging & Monitoring Failures → audit log (M4) + observability (M1); A10 SSRF → URL allowlist on any outbound calls.
- **Secret management:** No secrets in code or env files committed to git; all secrets from Vault / AWS Secrets Manager / Kubernetes Secrets with at-rest encryption.
- **Static & dynamic scanning:** Semgrep (SAST) + Trivy (containers) + `npm audit`/`pip-audit` (deps) in CI from M1; OWASP ZAP baseline against staging nightly from M2; external pen-test in M5.

### Observability

- **Tracing:** OpenTelemetry, W3C Trace Context propagated through every request; spans on every DB query, Redis call, OAuth provider call.
- **Metrics:** Prometheus — RED (rate/errors/duration) on every endpoint, USE (utilization/saturation/errors) on DB and Redis pools, custom `auth_events_total{event_type,result}`, `concurrent_sessions`, `rate_limit_blocks_total`.
- **Logging:** Structured JSON, one event per line, with `request_id`, `user_id` (where authenticated), `actor_id`, `ip`, `route`, `status`, `duration_ms`. PII redacted before serialization (email → SHA-256 prefix, password fields → `[REDACTED]`).
- **Dashboards & alerts:** Grafana dashboards for auth-funnel (registration → verify → login), error rate, latency percentiles, rate-limit hits, audit-event volume. Alerts: error rate > 1% / 5m, p95 > 200ms / 5m (NFR-001), failed-login rate spike > 3 sigma (potential attack), audit-event-volume drop > 50% (potential logging failure).

### Testing Strategy

- **Unit:** ≥80% line coverage project-wide, ≥90% on crypto and auth-flow modules. Required to merge.
- **Integration:** Per-milestone integration suites running against ephemeral PostgreSQL + Redis containers. Includes negative cases (token replay, CSRF, parameter tampering).
- **Contract:** Nightly contract tests against Google and GitHub OIDC discovery endpoints (M3).
- **Load:** k6 scenarios in CI on a weekly cadence from M2 (small scale) and a full 10K-session test in M5.
- **Security:** SAST + DAST in CI; manual pen-test in M5.
- **Chaos:** OAuth-provider-outage simulation (M3 acceptance), Redis failover test (M4 acceptance), database failover test (M5 acceptance).

---

## Risk Register

| ID | Risk (from spec) | Impact | Probability | Roadmap Mitigation | Milestone |
|----|------------------|--------|-------------|--------------------|-----------|
| R-001 | Token theft via XSS | High | Medium | Refresh tokens in `HttpOnly`/`Secure`/`SameSite=Strict` cookies; access tokens never in localStorage; strict CSP `default-src 'self'`; refresh-token rotation with reuse-detection family revocation (D2.4, D2.5, D2.8, D2.9). 2FA as defense-in-depth (D4.1–D4.3). | M2 (primary), M4 (2FA reinforcement) |
| R-002 | Brute force attacks | High | High | Per-user + per-IP token-bucket rate limiting in Redis (D4.4); progressive account lockout (D4.5); Argon2id slow-by-design hashing (D1.4) imposes attacker cost; audit-log alerting on failed-login spikes. | M4 (primary), M1 (hashing foundation) |
| R-003 | OAuth provider downtime | Medium | Low | Circuit breaker around provider calls (D3.7); UI fallback banner directing to email/password; email/password path remains independently functional. Nightly contract tests detect upstream API drift (D3.8). | M3 |
| R-004 | Data breach of PII | Critical | Low | Column-level encryption of PII with KMS-managed keys (D1.1); append-only audit trail (D4.6); GDPR erasure endpoint (D4.8); access controls enforced via RBAC (D3.5–D3.6); external pen-test gates GA (D5.7); 72h breach notification runbook (D5.8). | M1, M3, M4, M5 (defense-in-depth across the system) |

---

## Success Criteria — Verification Matrix

Every functional and non-functional requirement is mapped to a concrete verification approach. The original spec's "Success Criteria" checklist is restated in the final block.

### Functional Requirements

| ID | Requirement | Milestone | Verification |
|----|-------------|-----------|--------------|
| FR-001 | User registration with email verification | M2 | Integration test covers register → verify-email → login happy path; verifies email-token TTL and single-use semantics. |
| FR-002 | Login with JWT generation | M2 | Integration test asserts RS256 JWT structure, claims (`sub`, `iat`, `exp`, `roles`), and signature verification; load test asserts NFR-001. |
| FR-003 | OAuth2 integration (Google, GitHub) | M3 | End-to-end test with stubbed providers using PKCE; nightly contract test against real provider discovery endpoints. |
| FR-004 | Role-based access control | M3 | Authorization-middleware unit tests + integration tests asserting 403/200 for role/permission combinations. |
| FR-005 | Password reset via email | M2 | Integration test for request → email-receipt → confirm; verifies single-use token and constant-time email-existence response. |
| FR-006 | Session management with refresh tokens | M2 | Integration test for refresh rotation; reuse-detection test asserts family revocation. |
| FR-007 | Two-factor authentication | M4 | Integration test against TOTP reference library (`speakeasy.totp.verify`); manual test with Google Authenticator + Authy. |
| FR-008 | API rate limiting per user | M4 | Automated test fires N+1 requests in window, asserts 429 with `Retry-After`; load test asserts no false positives at 10K-session baseline. |
| FR-009 | Audit logging for auth events | M4 | End-to-end test exercises all 15 event types and asserts corresponding `audit_events` rows with append-only enforcement. |
| FR-010 | User profile management | M5 | Integration tests for GET/PATCH `/me`, email-change re-verification, password-change current-password requirement. |
| FR-011 | Admin dashboard for user management | M5 | UI E2E test (Playwright/Cypress) covering search, role grant/revoke, force-logout, view-audit; admin actions audited assertion. |
| FR-012 | Account deactivation workflow | M5 | Integration test: self-deactivate → session revoked → login blocked → 30-day grace → automatic erasure job. |

### Non-Functional Requirements

| ID | Requirement | Milestone(s) | Verification |
|----|-------------|--------------|--------------|
| NFR-001 | < 200ms p95 for auth endpoints | M2 (initial), M5 (sustained) | k6 load test reporting p95 from histogram; alert on `http_request_duration_seconds{route=~"/auth/.*"}` p95 > 200ms / 5m. |
| NFR-002 | Support 10,000 concurrent sessions | M5 | 30-minute k6 scenario at 10K concurrent sessions with mixed workload; SLO dashboard confirms zero 5xx and stable p95. |
| NFR-003 | OWASP Top 10 (2021) compliance | M1–M5 | SAST in CI from M1; DAST nightly from M2; external pen-test in M5 with zero unresolved High/Critical. Compliance matrix maintained in `docs/security/owasp-mapping.md`. |
| NFR-004 | GDPR compliance for user data | M1, M4, M5 | Data-subject export and erasure endpoints (D4.8); 72h breach-notification runbook (D5.8); legal/privacy sign-off in D5.9. |
| NFR-005 | 99.9% uptime for auth services | M1, M5 | SLO instrumentation (D5.5) with burn-rate alerts; HPA + PDB (D5.4) ensures rolling deploys do not breach SLO; quarterly availability review post-GA. |
| NFR-006 | Encrypt PII at rest and in transit | M1, M2 | Column-level encryption tested in M1 (D1.1); TLS 1.3 enforced via Nginx/ALB policy and verified in M2 acceptance; backup encryption verified quarterly. |

### Spec's Original Success Criteria Checklist

- [ ] All FR-001..FR-012 requirements implemented and tested → verified by the FR matrix above; final sign-off at end of M5.
- [ ] OWASP compliance verified via security scan → SAST + DAST in CI continuously; external pen-test gate in D5.7.
- [ ] Load testing confirms 10K concurrent sessions → D5.6 (k6 30-minute scenario).
- [ ] OAuth2 flow works for Google and GitHub → M3 acceptance criteria; ongoing nightly contract tests (D3.8).
- [ ] Audit logs capture all auth events → D4.6 + M4 end-to-end audit test covering 15 event types.
