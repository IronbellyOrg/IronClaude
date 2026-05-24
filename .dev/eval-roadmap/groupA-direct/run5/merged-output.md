<!-- Provenance: Produced by /sc:adversarial; Base: variant-1-opus-default (opus); Merge date: 2026-05-22 -->

# User Authentication System — Implementation Roadmap

**Variant:** merged (adversarial)
**Generated:** 2026-05-22
**Source Specification:** `/config/workspace/IronClaude/tests/sc-roadmap/fixtures/sample_spec.md`
**Total Estimated Duration:** 18 weeks (5 milestones, walking-skeleton compromise in M1)
**Target Stack:** Python 3.11+ / FastAPI / SQLAlchemy / Alembic / pyotp / authlib / OpenTelemetry — PostgreSQL 15.4+, Redis 7.2+, SendGrid v3 API, Docker 24+ (pinned via week-0 ADR; see below)

---

## Executive Summary
<!-- Source: Base (original) -->

This roadmap delivers a production-grade User Authentication System that combines email/password registration, JWT-based session management with refresh tokens, third-party OAuth2 (Google, GitHub), role-based access control (RBAC), and two-factor authentication (2FA) into a single hardened service. The system is designed to satisfy OWASP Top 10 (2021) and GDPR obligations from day one, support 10,000 concurrent sessions on a horizontally scaled Redis-backed deployment, and emit a complete audit trail for compliance investigations.

The build is sequenced as 5 milestones over 18 weeks. M1 establishes the foundation (data model, crypto primitives, dev infrastructure) **and ships a walking-skeleton login endpoint to de-risk integration feedback against the encrypted schema before M2 expands the surface**. M2 ships the core identity surface (registration, login, password reset). M3 layers OAuth2 federation and the RBAC engine. M4 introduces hardening features (2FA, rate limiting, audit logging) that directly mitigate the spec's four named risks. M5 delivers the operator-facing surface (admin dashboard, profile management, account deactivation) and concludes with load testing and a security audit gate before GA.

The sequencing is deliberate: every cross-cutting concern (encryption at rest/in transit, OWASP controls, observability) is introduced in M1 and reinforced thereafter, so no milestone ships features without its security and observability tail. Risk mitigations are not deferred — R-001 (XSS/token theft) and R-002 (brute force) are addressed in M2 and M4 respectively, not punted to a post-launch hardening sprint.

---

## Week-0 Architecture Decision Record
<!-- Source: Base (modified) — Change #3: Pin stack via ADR -->

Before M1 begins, a single-page Architecture Decision Record (ADR) is committed to `docs/adr/0001-language-and-framework.md` capturing the framework choice and its rationale. This eliminates hidden estimation debt from framework-agnostic wording.

| Decision | Choice | Rationale | Alternative |
|---|---|---|---|
| Language | Python 3.11+ | Mature crypto ecosystem (cryptography, pyotp, authlib); FastAPI native async; team familiarity | Node.js 20 LTS with TypeScript (equivalent ecosystem; substitution guide included in ADR) |
| HTTP framework | FastAPI | First-class OpenAPI 3.1 generation enables Schemathesis (Change #6); native dependency-injection pattern for RBAC middleware | Express + zod for Node alternative |
| ORM / migrations | SQLAlchemy 2.x + Alembic | Type-safe ORM; deterministic migrations | Prisma for Node alternative |
| 2FA TOTP | pyotp | Vetted RFC 6238 implementation | speakeasy for Node alternative |
| OAuth client | authlib | OIDC discovery + PKCE; mature error handling | openid-client for Node alternative |
| Observability SDK | OpenTelemetry Python SDK | W3C Trace Context; OTLP exporter | OpenTelemetry Node SDK |
| Argon2id parameters | `m=64MB, t=3, p=4` (default) with `m=46MB, t=2, p=2` fallback tier | OWASP ASVS 4.0 §2.4.1 first-tier; fallback validated against target instance class per Mandatory Change #M5 | n/a |

The ADR is approved by the security reviewer named in D1.7 before M1 starts. Substitution guide in ADR section §3 documents the Node.js equivalents line-for-line.

---

## API Conventions
<!-- Source: Base (modified) — Change #1 (versioning) + Change #5 (pagination) -->

These conventions are enforced from M1 onward and validated by the Schemathesis contract gate (see Testing Strategy).

- **Versioning** (Change #1, from V2 C-018): All HTTP endpoints are prefixed `/api/v1/`. Major-version deprecation policy: a sunset header `Sunset: <RFC 7231 date>` plus a `Deprecation: true` header is emitted on legacy endpoints during a minimum 6-month parallel-version window before removal. Schemathesis is run against the current major; nightly OIDC contract tests (D3.8) remain external and unrelated to internal API versioning. This addresses INV-009 (deprecation policy gap).
- **Pagination** (Change #5, from V2 U-019): All list endpoints accept `page` (default 1) and `per_page` (default 50, max 200) query params; responses are wrapped in the envelope `{"results": [...], "total": N, "page": P, "per_page": PP}`. Empty lists return `{"results": [], "total": 0, "page": 1, "per_page": 50}` — addressing INV-007 empty-shape divergence.
- **List endpoints that adopt these defaults:** admin user list (D5.2), audit-log query (D5.2/D4.6), session-management admin view (D5.2).

---

## Milestones

### M1 — Foundation & Security Primitives + Walking-Skeleton Login (Weeks 1–3)
<!-- Source: Base (modified) — Change #2 (walking-skeleton), Change #3 (ADR), Change #9 (table format), Mandatory #M1, #M2, #M3, #M5 -->

**Goal:** Stand up the database schema, secret management, crypto primitives, containerized dev/CI environment, observability spine, AND a thin walking-skeleton login endpoint that integrates end-to-end against the encrypted schema. Every subsequent milestone depends on M1's outputs; the walking-skeleton de-risks the foundation against real traffic before M2 expands the surface.

**Source-spec coverage:**

- Dependencies: PostgreSQL 15+, Redis, Docker
- NFR-003 (OWASP baseline), NFR-004 (GDPR baseline), NFR-006 (encryption at rest and in transit)
- Risk groundwork for R-001, R-004

#### Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| D1.1 | PostgreSQL 15.4 schema with blind-index lookup | Tables: `users`, `roles`, `permissions`, `user_roles`, `refresh_tokens`, `oauth_identities`, `audit_events`, `password_reset_tokens`, `mfa_secrets`. PII columns (email, phone, name) encrypted using `pgcrypto` AES-256-GCM with per-column key references managed by AWS KMS / HashiCorp Vault. **Per Mandatory Change #M3 (INV-010 resolution):** `users` includes `email_ciphertext` (encrypted) AND `email_blind_index BYTEA NOT NULL UNIQUE` = HMAC-SHA256(lower(email), blind_index_key). Lookup queries key on `email_blind_index`; ciphertext returned for display/audit only. Blind-index key rotated separately from data-encryption key and stored in KMS. **Per Mandatory Change #M1 (INV-001 resolution):** `users` includes `pending_email` (nullable, encrypted) and `pending_email_token_hash` (nullable) columns for the email-change-keeps-old-email-valid flow. **Per Mandatory Change #M2 (INV-003):** `users.pending_2fa_enrollment` boolean (default false) flags admins promoted without 2FA. **Status separation per Change #11:** `users.status` enum (`active`, `suspended`, `deactivated`) orthogonal to role. |
| D1.2 | Redis 7.2 cluster with Sentinel-based HA (dev/test) | Redis 7.2 with TLS 1.3 in transit, AOF persistence (`appendfsync everysec` baseline; counters that must survive failover are mirrored to PostgreSQL — see D4.5), and key-namespace conventions (`session:*`, `ratelimit:*`, `lockout:*`). **Per Change #8:** dev/test docker-compose uses Sentinel-based failover (one primary + two replicas + three sentinels); production uses managed Redis (ElastiCache / Memorystore) referenced from Kubernetes Service in D5.4. |
| D1.3 | Docker Compose dev stack + production base image | Services: `postgres`, `redis`, `redis-sentinel` (x3), `mailhog` for dev SMTP, `auth-api`. Production Dockerfile uses distroless or `python:3.11-slim` base image with non-root user. |
| D1.4 | Crypto utility module | Argon2id password hashing — **default tier `m=64MB, t=3, p=4`** per OWASP ASVS 4.0 §2.4.1; **fallback tier `m=46MB, t=2, p=2`** per Mandatory Change #M5 (validated against target instance class in week-0 ADR if cold-process exceeds 200ms). JWT signing keys (RS256, 2048-bit RSA), CSRF token generator, HMAC-SHA256 utility used by D1.1 blind-index, and HMAC utility for IP/user-agent hashing (per Mandatory Change #M4). |
| D1.5 | Observability baseline | OpenTelemetry SDK wired for traces and metrics; structured JSON logs to stdout; Prometheus `/metrics` endpoint exposing `http_request_duration_seconds`, `auth_events_total`, `db_query_duration_seconds`, `concurrent_sessions`, `rate_limit_blocks_total`. |
| D1.6 | CI pipeline | GitHub Actions: lint, unit tests, SAST (Semgrep with `p/owasp-top-ten` ruleset), dependency vulnerability scan (`pip-audit` for Python; `npm audit --audit-level=high` for the Node alternative documented in the ADR), container image scan (Trivy), and the Schemathesis contract gate (Change #6) running against the current OpenAPI 3.1 spec. |
| D1.7 | Threat model document | STRIDE-style threat model covering all 12 FRs and explicit mappings to R-001..R-004. Names the designated security reviewer (role: Security Lead) responsible for per-milestone STRIDE-row revalidation sign-offs (Change #10). |
| D1.8 | Walking-skeleton login endpoint + bootstrap admin CLI | **Per Change #2:** Thin `POST /api/v1/auth/login` returning a stub RS256 JWT for a seeded user against the encrypted schema (uses blind-index lookup from D1.1; password hashed with D1.4 Argon2id). Integration test runs end-to-end against the ephemeral PostgreSQL + Sentinel-Redis stack. Acceptance criterion: happy-path login returns valid RS256 JWT for the seeded user in <200ms p95 (cold-process measured with Argon2id default tier; documents which tier the target instance class actually meets per #M5). **Bootstrap admin CLI (per Mandatory Change #M2):** `superclaude auth bootstrap-admin --email <addr>` creates the initial admin user WITH 2FA pre-provisioned via an out-of-band TOTP secret printed to the operator console; output includes the 10 recovery codes printed once and never re-emitted. This is the only path that can create an admin without prior admin authentication. |

**Dependencies:** None (start milestone).

**Acceptance criteria:**

- `docker compose up` brings the stack (including 3 Redis sentinels) to a healthy state in < 60s on a 4-core dev machine.
- All PII columns reject inserts of plaintext via a test that bypasses the application layer and asserts ciphertext; blind-index column is populated by application-layer trigger; uniqueness on `email_blind_index` enforced.
- CI run on a sample PR completes in < 8 minutes end-to-end and includes the Schemathesis gate.
- Crypto module passes 100% of test vectors (RFC 9106 Argon2 test vectors, RFC 7519 JWT round-trip tests, RFC 2104 HMAC test vectors for blind-index).
- Threat model is reviewed and signed off by the designated Security Lead (role named in D1.7).
- Walking-skeleton `POST /api/v1/auth/login` returns a valid JWT for the seeded user; integration test green; latency measurement recorded in week-0 ADR Argon2id-tier section.
- Bootstrap admin CLI produces a working admin login with 2FA in a fresh database.

**Estimated duration:** 3 weeks.

---

### M2 — Core Identity: Registration, Login, Password Reset (Weeks 4–7)
<!-- Source: Base (modified) — Change #1 (versioning), Change #9 (table format), Change #10 (STRIDE per milestone), Mandatory #M3, #M5 -->

**Goal:** Ship the primary email/password identity flows with JWT access tokens and refresh tokens, extending the M1 walking-skeleton to the full surface. This is the first milestone with full user-facing endpoints.

**Source-spec coverage:**

- FR-001 (registration with email verification)
- FR-002 (login with JWT generation)
- FR-005 (password reset via email)
- FR-006 (session management with refresh tokens)
- NFR-001 (< 200ms p95 for auth endpoints)
- NFR-003 (OWASP — token handling, password storage)
- NFR-006 (encryption in transit for all flows)
- R-001 (XSS/token theft mitigation via cookie hardening)

#### Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| D2.1 | `POST /api/v1/auth/register` | Accepts `email`, `password`, `name`; enforces password policy (≥12 chars, NIST SP 800-63B style — no composition rules, but a 10K-entry breached-password denylist via HIBP k-anonymity API or local bloom filter); Argon2id-hashes password (per the tier selected in D1.4 / week-0 ADR); writes both `email_ciphertext` and `email_blind_index` (per #M3); creates user in `pending_verification` state; emits verification token (32 bytes, base64url, 24h TTL). |
| D2.2 | `POST /api/v1/auth/verify-email` | Consumes the verification token, atomically transitions user to `users.status = 'active'`. |
| D2.3 | SendGrid integration | `@sendgrid/mail` (or Python `sendgrid` library) using dynamic templates for verification, password reset, and 2FA enrollment emails; bounce/spam webhook handler. |
| D2.4 | `POST /api/v1/auth/login` | Lookup keys on `email_blind_index` (per #M3); returns short-lived (15 min) RS256 JWT access token and a long-lived (30 day) refresh token. Refresh tokens are opaque random 32-byte strings stored hashed (SHA-256) in `refresh_tokens` with `user_id`, `family_id` (semantics: **one family per login event, per device** — multiple families per user — resolving INV-008), `issued_at`, `expires_at`, `revoked_at`. Refresh-token rotation with reuse detection per OAuth 2.0 BCP (RFC 9700 §2.2.2). |
| D2.5 | `POST /api/v1/auth/refresh` | Rotates refresh tokens; reuse of an already-rotated token revokes the entire token family (mitigates R-001 token replay). |
| D2.6 | `POST /api/v1/auth/logout` | Revokes the calling session's refresh-token family, clears cookies. |
| D2.7 | Password-reset endpoints | `POST /api/v1/auth/password-reset/request` and `POST /api/v1/auth/password-reset/confirm` — single-use reset tokens (32 bytes, 1h TTL), constant-time email-existence response to prevent enumeration. Reset-password flow keys on `email_blind_index` (NOT `pending_email`), preventing account-takeover via reset-to-pending-address per #M1. |
| D2.8 | Cookie strategy | Refresh token set as `HttpOnly`, `Secure`, `SameSite=Strict`; access token returned in response body (consumed by SPA in memory, not localStorage) — directly mitigates R-001. |
| D2.9 | Content Security Policy + headers | Default: `default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'`; HSTS `max-age=63072000; includeSubDomains; preload`. Admin SPA (D5.2) uses nonce-based `script-src` to avoid `'unsafe-inline'`. |
| D2.10 | Integration test suite | Covers all flows; ≥90% line coverage on the M2 module; includes blind-index lookup round-trip tests and the pending-email/email-change happy + sad paths even though endpoint lives in M5 (the schema and lookup logic ship in M1+M2). |

**Dependencies:** M1 (D1.1, D1.2, D1.4, D1.5, D1.8).

**Acceptance criteria:**

- p95 latency for `/api/v1/auth/login` and `/api/v1/auth/refresh` ≤ 200ms under a 100 RPS sustained load (k6 or Locust harness) — verifies NFR-001. **Per Mandatory Change #M5:** test runs with cold-Redis (cache flushed at test start) for the first 60 seconds and warm-cache for the remainder; BOTH segments must satisfy NFR-001.
- Refresh-token reuse triggers family revocation in < 1s, verified by automated test.
- ZAP baseline scan against the deployed test environment produces zero `High` or `Medium` findings against the M2 endpoints.
- Verification and password-reset emails arrive within 30s in a SendGrid sandbox test.
- Manual review confirms no auth token is ever written to localStorage or a non-`HttpOnly` cookie.
- **STRIDE re-validation (Change #10):** rows of the D1.7 threat model mapped to M2 scope (FR-001/002/005/006) are re-tested and signed off by the named Security Lead within 2 business days of milestone completion.

**Estimated duration:** 4 weeks.

---

### M3 — Federation & Authorization: OAuth2 + RBAC (Weeks 8–10)
<!-- Source: Base (modified) — Change #1, Change #9, Change #10, Change #11 (admin/user taxonomy), Mandatory #M2, #M5 -->

**Goal:** Add Google and GitHub as identity providers, implement the role/permission model, and wire authorization checks into the request pipeline.

**Source-spec coverage:**

- FR-003 (OAuth2 integration — Google, GitHub)
- FR-004 (role-based access control)
- R-003 (OAuth provider downtime → fallback to email/password)
- NFR-003 (OWASP — authorization, OAuth state handling)

#### Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| D3.1 | OAuth2 Auth Code + PKCE | RFC 7636 S256 method for Google (`accounts.google.com`) and GitHub (`github.com/login/oauth`). Use `authlib` (Python) — pinned per week-0 ADR; verified against the provider's published OIDC discovery document. |
| D3.2 | `GET /api/v1/auth/oauth/:provider/start` | Generates `state` (32-byte random, stored in short-lived Redis key) and `code_verifier`, redirects to provider. |
| D3.3 | `GET /api/v1/auth/oauth/:provider/callback` | Validates `state`, exchanges code for tokens, fetches userinfo, links to existing user by verified email (via `email_blind_index` lookup) or creates a new account; writes `oauth_identities` row. |
| D3.4 | `POST /api/v1/auth/oauth/link` | Account linking endpoint for users already authenticated via email/password. |
| D3.5 | RBAC engine (spec-aligned taxonomy per Change #11) | **Roles**: `admin`, `user` (default — assigned on registration). **Status (orthogonal)**: `users.status` enum `active`, `suspended`, `deactivated` (per Change #11). RBAC middleware checks role; lockout/suspension middleware checks status. `permissions` (e.g., `users.read`, `users.deactivate`, `audit.read`, `admin:access`), `role_permissions` join. Resolution cached in Redis for 60s per user; cache is pre-warmed on deploy (per #M5) for the top-100 active users (rolling window). Default roles seeded via migration. |
| D3.6 | Authorization middleware | `require_permission('users.deactivate')` declarative guard usable on every protected route; returns 403 with structured error code. **Admin-2FA-enrollment gate (per Mandatory Change #M2):** if `users.pending_2fa_enrollment = true`, middleware returns HTTP 403 `{"error": "admin_2fa_required", "next_step": "/api/v1/auth/2fa/enroll"}` for every route EXCEPT `/api/v1/auth/2fa/enroll` and `/api/v1/auth/logout`. On successful enrollment, the flag is cleared atomically. |
| D3.7 | Provider-outage circuit breaker | `pybreaker` on OAuth provider calls; on open-circuit, the OAuth start endpoint surfaces a user-facing banner directing to email/password login — directly mitigates R-003. A 5xx rate > 25% over a 60s window opens the circuit for 5 minutes. |
| D3.8 | Contract tests vs. external OIDC discovery | Run nightly in CI against Google's and GitHub's published OIDC/OAuth discovery endpoints to detect upstream changes. These are external contract tests; internal API conformance is owned by Schemathesis per the Testing Strategy. |
| D3.9 | Role-change protocol | **Per Mandatory Change #M2:** Promoting any user to `admin` triggers, atomically: (a) set `users.pending_2fa_enrollment = true` if user does not already have a confirmed 2FA secret; (b) revoke all refresh-token families for that user. Demoting from `admin` clears `pending_2fa_enrollment`. All role changes are audited (D4.6) with the acting `actor_id`. |

**Dependencies:** M2 (user records, JWT issuance pipeline must exist).

**Acceptance criteria:**

- End-to-end test with stubbed Google and GitHub providers (using `responses` recordings) completes the full Auth Code + PKCE flow.
- A user authenticated via Google can be promoted to `admin`; the promotion sets `pending_2fa_enrollment` and revokes their refresh-token families; their next request returns the `admin_2fa_required` response; after `/api/v1/auth/2fa/enroll` completes, full admin access is granted; a protected endpoint correctly returns 403 to a `user`-role caller and 200 to the `admin`.
- Simulated 100% Google outage (provider returns 503) does not block email/password login; the OAuth-start endpoint returns a 503 with `Retry-After` and the UI fallback path is exercised in an integration test.
- Authorization middleware adds ≤ 5ms p95 overhead per request (measured by removing the middleware in a control build); RBAC permission-cache warm-on-deploy verified by readiness probe (per #M5).
- **STRIDE re-validation (Change #10):** rows mapped to M3 scope (FR-003/004) re-tested and signed off by the Security Lead within 2 business days of milestone completion.

**Estimated duration:** 3 weeks.

---

### M4 — Hardening: 2FA, Rate Limiting, Audit Logging (Weeks 11–14)
<!-- Source: Base (modified) — Change #1, Change #9, Change #10, Mandatory #M2, #M4 -->

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

#### Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| D4.1 | TOTP-based 2FA | RFC 6238 (SHA-1, 30s step, 6 digits) via `pyotp`; QR-code enrollment using `otpauth://` URI; recovery codes (10 single-use codes, 10 chars each, hashed at rest with Argon2id). |
| D4.2 | 2FA endpoints | `POST /api/v1/auth/2fa/enroll`, `POST /api/v1/auth/2fa/verify`, `POST /api/v1/auth/2fa/disable`. 2FA is opt-in for `user` role and mandatory for `admin` role (enforced at login AND at promotion-time per #M2 / D3.9). The `enroll` endpoint clears `users.pending_2fa_enrollment` atomically on successful first verification. |
| D4.3 | Login flow upgrade for 2FA | When a 2FA-enabled user authenticates with primary factor, server returns a short-lived (5 min) `mfa_pending` token; full JWT is issued only after `/api/v1/auth/2fa/challenge` succeeds. |
| D4.4 | Rate limiting | Token-bucket algorithm in Redis using Lua script for atomicity. Per-user limits: 5 failed logins / 15 min triggers a 15-min lockout; 100 auth-endpoint requests / 1 min per user; 30 password-reset requests / 1h per IP. Per-IP global limit: 1000 requests / min. Limits returned via `X-RateLimit-*` headers; 429 response includes `Retry-After`. |
| D4.5 | Account lockout (progressive) | After 5 consecutive failed logins, lock for 15 min; after 3 such lockout cycles within a 24h decay window, require password reset (decay window closes INV-005 ambiguity: cycles are counted within a rolling 24h Redis-TTL'd window keyed on `lockout:cycles:{user_id}`). Locked-account state stored in Redis with TTL; mirrored to `users.locked_until` on lockout to survive Redis loss. |
| D4.6 | Audit logging with write-time PII redaction (per #M4) | Structured `audit_events` rows for every event in {register, verify_email, login_success, login_failure, logout, password_reset_request, password_reset_complete, 2fa_enroll, 2fa_disable, oauth_link, role_grant, role_revoke, account_deactivate, account_reactivate, admin_action}. Schema: `event_type`, `user_id` (UUID, opaque), `actor_id`, `ip_hash` (HMAC of IP, NOT raw IP), `user_agent_hash` (HMAC of UA, NOT raw UA), `request_id`, `result`, `metadata_jsonb`, `created_at`. **Per Mandatory Change #M4 (INV-011 resolution):** at write-time, the application layer redacts PII (email, name, phone, raw IP, raw user agent) from `metadata_jsonb` — only stable opaque references survive. Append-only via PostgreSQL trigger that rejects `UPDATE`/`DELETE` except by a dedicated retention role. List query endpoint returns the pagination envelope from API Conventions (Change #5). |
| D4.7 | Audit-log retention | 13 months hot in PostgreSQL, then archived to S3 (or equivalent) with object-lock for 7-year retention per common SOC2/GDPR practice. **Per #M4:** because PII is redacted at write-time (D4.6), the immutable archive contains no PII. GDPR Art. 17(3)(b) legal-basis-for-retention rationale ("audit records retained for the establishment, exercise, or defense of legal claims") is documented in the GDPR runbook (D5.8) for legal review. |
| D4.8 | GDPR data-subject endpoints | `GET /api/v1/me/export` (returns JSON of all user-owned rows) and `POST /api/v1/me/erase` (soft-deletes user, redacts PII columns including `email_ciphertext` and `pending_email` to `<redacted>`, recomputes `email_blind_index` to a tombstone marker, retains audit rows by `user_id` reference). Per #M4, audit `user_id` references survive without dragging PII into the immutable archive. |

**Dependencies:** M2 (login flow to extend), M3 (RBAC roles for admin-mandatory 2FA).

**Acceptance criteria:**

- A scripted brute-force attack (1000 attempts/min from 1 IP, 50 attempts/min per user) is fully blocked: zero successful logins, account locked within 5 attempts, IP rate-limited within 1 minute. Verifies R-002 mitigation.
- TOTP enrollment and verification work against Google Authenticator and Authy reference apps.
- Audit log captures all 15 event types in an end-to-end test that exercises each flow; spot-checks confirm zero PII present in `metadata_jsonb` (asserted by automated test that searches for email/IP literals in audit rows after exercising every flow).
- `POST /api/v1/me/erase` removes PII from `users` row while leaving `audit_events.user_id` intact for legal hold (verified by SQL inspection).
- Rate-limiter load test: 10,000 concurrent users at steady-state with rate limiting enabled shows < 1% rate-limiter overhead in tail latency.
- **STRIDE re-validation (Change #10):** rows mapped to M4 scope (FR-007/008/009) re-tested and signed off by the Security Lead within 2 business days of milestone completion.

**Estimated duration:** 4 weeks.

---

### M5 — Admin Surface, Profile Management, Deactivation, GA Hardening (Weeks 15–18)
<!-- Source: Base (modified) — Change #1, Change #4 (admin perf gate + EXPLAIN ANALYZE), Change #5 (pagination), Change #8 (managed Redis prod), Change #9, Change #10, Mandatory #M1, #M5, #M6 -->

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

#### Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| D5.1 | Profile endpoints with email-change-keeps-old-valid (per #M1) | `GET /api/v1/me`, `PATCH /api/v1/me` (name, locale, timezone, avatar URL), `POST /api/v1/me/email/change`, `POST /api/v1/me/password/change` (current-password required; HIBP breached-password denylist re-applied per INV-004 mitigation). **Email change flow (per Mandatory Change #M1):** stores new address in `pending_email` and emits a verification token (hash stored in `pending_email_token_hash`). The old email remains the login key (`email_blind_index` unchanged) until verification. On confirmation: transactionally update `email_ciphertext = encrypt(pending_email)`, recompute `email_blind_index = HMAC(lower(pending_email), key)`, clear `pending_email` and `pending_email_token_hash`, and revoke all refresh-token families to force re-login under the new email. Reset-password requests during the pending window key on the OLD address only (preventing reset-to-pending-address account takeover). |
| D5.2 | Admin dashboard with perf gate (per Change #4) | Server-rendered or SPA (React 18 SPA documented in week-0 ADR). Features: user search, filter by role/status/last-login, view audit trail per user, grant/revoke roles, force password reset, force logout (revoke all refresh-token families for that user — semantics resolved by D2.4: revokes every family across all devices), enable/disable 2FA enforcement for a user (admin-side break-glass). All admin actions are themselves audited (`actor_id` ≠ `user_id` case). **Pagination per Change #5:** all list views accept `page`/`per_page` (50 default, 200 max) and return the standard envelope. **Performance acceptance (per Change #4 / V2 U-018):** admin user list loads in <500ms p95 with 50,000 seeded user records. Empty admin lists return `{"results": [], "total": 0, ...}` per INV-007 resolution. |
| D5.3 | Account deactivation | `POST /api/v1/me/deactivate` (self-service, requires password + 2FA if enabled) and admin equivalent. Deactivation sets `users.status = 'deactivated'`, revokes all sessions, blocks login with a clear `account_deactivated` error, sends confirmation email. A 30-day grace period during which the user can reactivate via password reset; after 30 days an automated job runs the GDPR erasure (D4.8) workflow unless legal hold is set. |
| D5.4 | Production deployment manifests | Kubernetes Helm chart with: horizontal pod autoscaler keyed on CPU + custom `concurrent_sessions` metric, PodDisruptionBudget min-available=2, readiness/liveness probes hitting `/health/ready` and `/health/live`. **Per Change #8:** production references managed Redis (ElastiCache / Memorystore) via Kubernetes Service — NOT Sentinel-in-cluster. **Per Mandatory Change #M5:** the `/health/ready` probe ONLY returns 200 after the RBAC permission cache is pre-warmed for the top-100 active users (rolling window) — preventing cold-cache 5xx during rolling deploys. |
| D5.5 | SLO instrumentation + scoped SLO definition (per Mandatory Change #M6) | 99.9% availability burn-rate alerts (fast 2% / 1h, slow 5% / 6h windows), p95 latency alerts, error-budget dashboard. **SLO scope definition (`docs/slo/auth-slo.md`, per #M6, resolves INV-015):** <br/>**In-scope endpoints (count toward SLO):** `/api/v1/auth/login`, `/api/v1/auth/refresh`, `/api/v1/auth/oauth/:provider/callback`, RBAC-protected reads on `/api/v1/me/*`. <br/>**Excluded endpoints (graceful degradation documented):** `/api/v1/auth/register` and `/api/v1/auth/password-reset/request` (depend on SendGrid — no fallback for transactional email; degraded mode shows user-facing "email delivery temporarily delayed" banner); `/api/v1/auth/oauth/:provider/start` (depends on OAuth providers; circuit-breaker fallback per D3.7). <br/>**Dependency exclusion policy:** when an excluded dependency is degraded, affected endpoints continue to be observed (latency, error rate) but are excluded from SLO burn-rate alerts until restored. <br/>**Documented dependency SLAs:** SendGrid 99.95% / MTTR 30min, Google OIDC 99.95% / MTTR 60min, GitHub OAuth 99.9% / MTTR 90min, managed PostgreSQL 99.99% / MTTR 30s, managed Redis 99.99% / MTTR 30s. <br/>**Composite availability check:** product of in-scope dependencies (managed PG × managed Redis × HPA-mitigated own service) = 99.99% × 99.99% × ~99.95% ≈ 99.93%, exceeding the 99.9% target with headroom. |
| D5.6 | Load test | k6 scenario ramping to 10,000 concurrent active sessions (mix of login, refresh, profile read, RBAC-protected calls) sustained for 30 minutes, asserting p95 < 200ms and zero 5xx — verifies NFR-001 and NFR-002. **Per #M5:** test exercises both cold-Redis and warm-Redis segments; cold-Argon2id and warm-Argon2id segments; cold-RBAC-cache and warm-RBAC-cache segments. All segments must satisfy NFR-001. |
| D5.7 | External penetration test / security audit | OWASP Top 10 (2021) — A01..A10 — with findings triaged and all `High`/`Critical` remediated before GA. Scope explicitly includes audit-log tamper-evidence (probes the append-only trigger AND the retention-role separation) per INV-014 awareness. |
| D5.8 | Incident response runbook | Token-compromise revocation procedure, mass password-reset procedure, OAuth-provider-outage procedure, PII-breach notification procedure (GDPR Art. 33 — 72h notification), GDPR Art. 17(3)(b) audit-retention legal-basis rationale (per #M4), and a **sole-admin / lost-2FA-device break-glass procedure** (INV-012 awareness): a documented two-operator manual DB intervention to clear `pending_2fa_enrollment` and re-trigger TOTP re-enrollment, gated by signed change-control. |
| D5.9 | GA readiness review sign-off | Security, SRE, product, legal/privacy. SLO definition document (D5.5) is signed off by SRE; audit-retention legal basis (D4.7, D5.8) is signed off by legal/privacy. |
| D5.10 | Query-plan CI gate (per Change #4) | CI step runs `EXPLAIN ANALYZE` on all frequently-used queries (login lookup via `email_blind_index`, refresh-token lookup, audit-log paginated query, admin user list with role+status filters); PR fails if any query plan contains a sequential scan on a table with >10K rows. Prevents missing-index regressions at PR time. |

**Dependencies:** M2, M3, M4.

**Acceptance criteria:**

- Load test sustains 10,000 concurrent sessions for 30 minutes with p95 < 200ms on `/api/v1/auth/login`, `/api/v1/auth/refresh`, `/api/v1/me`, and RBAC-guarded endpoints — across cold and warm cache phases (per #M5).
- Admin user list loads in <500ms p95 with 50,000 seeded user records (per Change #4).
- External pen-test report shows zero unresolved `High` or `Critical` OWASP Top 10 findings; audit-log tamper-evidence probe path documented.
- Admin can deactivate a user via the dashboard; the user's next login attempt returns the documented `account_deactivated` error; an `account_deactivate` audit event is recorded with the admin's `actor_id`.
- Email-change happy path and sad path (verification failure) both leave the old email functional and login uninterrupted (per #M1).
- 30-day deactivation-to-erasure job runs in staging against a fast-forwarded clock and produces the same outcome as the manual `POST /api/v1/me/erase` flow; `email_blind_index` tombstone verified.
- 99.9% availability SLO dashboard is live, scoped per D5.5, and burn-rate alerts fire correctly in a staged failure injection that targets in-scope dependencies.
- D5.10 CI gate rejects a PR that adds a sequential scan on `users`, `audit_events`, or `refresh_tokens`.
- **STRIDE re-validation (Change #10):** all remaining threat-model rows re-tested and signed off by the Security Lead within 2 business days of milestone completion (final pass).

**Estimated duration:** 4 weeks.

---

## Cross-Cutting Concerns

### Security
<!-- Source: Base (modified) — Mandatory #M3, #M4, #M5; Change #1 deprecation policy -->

- **Encryption in transit (NFR-006):** TLS 1.3 minimum on all ingress; mTLS between auth-api and PostgreSQL/Redis where the deployment topology supports it. HSTS enforced from M2 onward.
- **Encryption at rest (NFR-006):** PII columns encrypted at the column level with `pgcrypto` AES-256-GCM (M1) using non-deterministic IV per row; lookup queries key on the `email_blind_index` HMAC-SHA256 column (Mandatory Change #M3) — the combination eliminates the deterministic-encryption antipattern while preserving login lookup performance. Database volumes encrypted at the disk level (cloud-provider KMS or LUKS). Backup encryption verified quarterly.
- **OWASP Top 10 2021 mapping (NFR-003):** A01 Broken Access Control → RBAC middleware (M3) + admin-2FA-gate (M3 D3.6); A02 Cryptographic Failures → Argon2id (parameter tier documented in week-0 ADR per #M5), RS256, AES-256-GCM, HMAC-SHA256 blind-index (M1); A03 Injection → parameterized queries enforced by ORM, zero raw SQL; A04 Insecure Design → threat model (M1) + per-milestone STRIDE re-validation (Change #10); A05 Security Misconfiguration → CIS-benchmarked base images, security headers (M2); A06 Vulnerable Components → Trivy + dependency scan in CI (M1); A07 Identification & Auth Failures → all of M2/M3/M4; A08 Software & Data Integrity → signed container images, SBOM generation, append-only audit trigger (M4 D4.6); A09 Logging & Monitoring Failures → audit log with PII-redaction-at-write (M4) + observability (M1); A10 SSRF → URL allowlist on any outbound calls.
- **API versioning + deprecation:** `/api/v1/` is the current major. Future deprecations emit `Sunset` + `Deprecation: true` headers for a minimum 6-month parallel-version window per INV-009 resolution.
- **Secret management:** No secrets in code or env files committed to git; all secrets from Vault / AWS Secrets Manager / Kubernetes Secrets with at-rest encryption. The blind-index key (#M3) is rotated independently from the data-encryption key.
- **Static & dynamic scanning:** Semgrep (SAST) + Trivy (containers) + `pip-audit` (deps) in CI from M1; Schemathesis (own-API contract) on every PR (Change #6); OWASP ZAP baseline against staging nightly from M2; external pen-test in M5 with explicit audit-log tamper-evidence probe (INV-014 awareness).

### Observability
<!-- Source: Base (modified) — Mandatory #M4, #M5, #M6 -->

- **Tracing:** OpenTelemetry, W3C Trace Context propagated through every request; spans on every DB query, Redis call, OAuth provider call.
- **Metrics:** Prometheus — RED (rate/errors/duration) on every endpoint, USE (utilization/saturation/errors) on DB and Redis pools, custom `auth_events_total{event_type,result}`, `concurrent_sessions`, `rate_limit_blocks_total`, `rbac_cache_hit_ratio`, `argon2_hash_duration_seconds`.
- **Logging:** Structured JSON, one event per line, with `request_id`, `user_id` (where authenticated), `actor_id`, `ip_hash` (HMAC, not raw IP — per #M4), `route`, `status`, `duration_ms`. PII redacted before serialization (email → SHA-256 prefix, password fields → `[REDACTED]`).
- **Dashboards & alerts:** Grafana dashboards for auth-funnel (registration → verify → login), error rate, latency percentiles, rate-limit hits, audit-event volume. Alerts scoped to D5.5 SLO endpoints only (per #M6): error rate > 1% / 5m on in-scope endpoints, p95 > 200ms / 5m on in-scope endpoints (NFR-001), failed-login rate spike > 3 sigma (potential attack), audit-event-volume drop > 50% (potential logging failure).

### Testing Strategy
<!-- Source: Base (modified) — Change #6 (Schemathesis), Change #9 (table format) -->

| Layer | Tool | Coverage Target | Frequency |
|-------|------|-----------------|-----------|
| Unit | pytest + pytest-cov | ≥80% project-wide; ≥90% on crypto and auth-flow modules. Required to merge. | Every commit (CI) |
| Integration | pytest + httpx TestClient | All API endpoints — happy path + error cases — running against ephemeral PostgreSQL + Sentinel-Redis containers. Includes negative cases (token replay, CSRF, parameter tampering, blind-index collision). | Every commit (CI) |
| Contract (own API) | Schemathesis v3+ | API conformance vs OpenAPI 3.1 spec (Change #6, from V2 U-013) | Every PR (CI) |
| Contract (external) | Provider OIDC discovery harness | Google + GitHub OIDC/OAuth discovery endpoint stability (D3.8) | Nightly (CI) |
| Load | k6 | 10K concurrent sessions, p95 < 200ms; weekly cadence from M2 small-scale; full 30-min 10K-session test in M5 (D5.6). | Weekly small / pre-release full |
| Security (SAST/DAST) | Semgrep + OWASP ZAP | Zero High/Medium findings on M2+ endpoints; manual pen-test in M5 (D5.7). | Every commit (SAST) / nightly (DAST) |
| E2E | Playwright | OAuth2 login (Google, GitHub), 2FA enrollment, admin dashboard | Nightly |
| Chaos | Custom harness | OAuth-provider-outage simulation (M3 acceptance), Redis failover test (M4 acceptance), database failover test (M5 acceptance) | Per-milestone |

---

## Risk Register
<!-- Source: Base (modified) — Change #1 (versioned endpoint paths in mitigation column) -->

| ID | Risk (from spec) | Impact | Probability | Roadmap Mitigation | Milestone |
|----|------------------|--------|-------------|--------------------|-----------|
| R-001 | Token theft via XSS | High | Medium | Refresh tokens in `HttpOnly`/`Secure`/`SameSite=Strict` cookies; access tokens never in localStorage; strict CSP `default-src 'self'; script-src 'self'; style-src 'self'` with nonce-based admin SPA; refresh-token rotation with reuse-detection family revocation (D2.4, D2.5, D2.8, D2.9). 2FA as defense-in-depth (D4.1–D4.3). | M2 (primary), M4 (2FA reinforcement) |
| R-002 | Brute force attacks | High | High | Per-user + per-IP token-bucket rate limiting in Redis with Lua atomicity (D4.4); progressive account lockout with 24h decay window (D4.5); Argon2id slow-by-design hashing (D1.4) imposes attacker cost; audit-log alerting on failed-login spikes. | M4 (primary), M1 (hashing foundation) |
| R-003 | OAuth provider downtime | Medium | Low | Circuit breaker around provider calls (D3.7); UI fallback banner directing to email/password; email/password path remains independently functional. Nightly contract tests detect upstream API drift (D3.8). | M3 |
| R-004 | Data breach of PII | Critical | Low | Column-level AES-256-GCM with KMS-managed keys + HMAC-SHA256 blind-index for lookup (D1.1, per #M3); append-only audit trail with PII redaction at write-time (D4.6, per #M4); GDPR erasure endpoint (D4.8); access controls enforced via RBAC + admin-2FA-enrollment gate (D3.5–D3.6 + D3.9, per #M2); external pen-test gates GA (D5.7); 72h breach notification runbook (D5.8). | M1, M3, M4, M5 (defense-in-depth across the system) |

---

## Success Criteria — Verification Matrix
<!-- Source: Base (modified) — Change #1 (versioned paths in verification) -->

Every functional and non-functional requirement is mapped to a concrete verification approach. The original spec's "Success Criteria" checklist is restated in the final block.

### Functional Requirements

| ID | Requirement | Milestone | Verification |
|----|-------------|-----------|--------------|
| FR-001 | User registration with email verification | M2 | Integration test covers register → verify-email → login happy path; verifies email-token TTL and single-use semantics. |
| FR-002 | Login with JWT generation | M1 (skeleton), M2 (full) | Integration test asserts RS256 JWT structure, claims (`sub`, `iat`, `exp`, `roles`), and signature verification; load test asserts NFR-001 with cold + warm cache segments. |
| FR-003 | OAuth2 integration (Google, GitHub) | M3 | End-to-end test with stubbed providers using PKCE; nightly contract test against real provider discovery endpoints. |
| FR-004 | Role-based access control | M3 | Authorization-middleware unit tests + integration tests asserting 403/200 for role/permission combinations; admin-2FA-enrollment gate exercised (per #M2). |
| FR-005 | Password reset via email | M2 | Integration test for request → email-receipt → confirm; verifies single-use token, constant-time email-existence response, and reset-keys-on-old-email (per #M1). HIBP breach denylist re-applied (INV-004 closure). |
| FR-006 | Session management with refresh tokens | M2 | Integration test for refresh rotation; reuse-detection test asserts family revocation; family semantics (device-scoped) verified per D2.4. |
| FR-007 | Two-factor authentication | M4 | Integration test against TOTP reference library (`pyotp.totp.verify`); manual test with Google Authenticator + Authy; admin-promotion-triggers-enrollment-gate verified. |
| FR-008 | API rate limiting per user | M4 | Automated test fires N+1 requests in window, asserts 429 with `Retry-After`; load test asserts no false positives at 10K-session baseline. |
| FR-009 | Audit logging for auth events | M4 | End-to-end test exercises all 15 event types and asserts corresponding `audit_events` rows with append-only enforcement AND zero-PII assertion on `metadata_jsonb` (per #M4). |
| FR-010 | User profile management | M5 | Integration tests for GET/PATCH `/api/v1/me`, email-change keeps-old-email-valid flow (per #M1), password-change current-password requirement + HIBP re-check. |
| FR-011 | Admin dashboard for user management | M5 | Playwright E2E covering search, role grant/revoke, force-logout (all families), view-audit; admin actions audited assertion; <500ms p95 with 50K users (Change #4). |
| FR-012 | Account deactivation workflow | M5 | Integration test: self-deactivate → session revoked → login blocked → 30-day grace → automatic erasure job. |

### Non-Functional Requirements

| ID | Requirement | Milestone(s) | Verification |
|----|-------------|--------------|--------------|
| NFR-001 | < 200ms p95 for auth endpoints | M2 (initial), M5 (sustained) | k6 load test reporting p95 from histogram across cold/warm cache segments and cold/warm Argon2id (per #M5); alert on `http_request_duration_seconds{route=~"/api/v1/auth/.*"}` p95 > 200ms / 5m for in-scope endpoints (per #M6). |
| NFR-002 | Support 10,000 concurrent sessions | M5 | 30-minute k6 scenario at 10K concurrent sessions with mixed workload; SLO dashboard confirms zero 5xx and stable p95. |
| NFR-003 | OWASP Top 10 (2021) compliance | M1–M5 | SAST in CI from M1; Schemathesis on every PR (Change #6); DAST nightly from M2; external pen-test in M5 with zero unresolved High/Critical and audit-log tamper-evidence probe. Compliance matrix maintained in `docs/security/owasp-mapping.md`. STRIDE rows re-validated per milestone (Change #10). |
| NFR-004 | GDPR compliance for user data | M1, M4, M5 | Data-subject export and erasure endpoints (D4.8); 72h breach-notification runbook (D5.8); audit-retention legal-basis (Art. 17(3)(b)) documented per #M4; legal/privacy sign-off in D5.9. |
| NFR-005 | 99.9% uptime for auth services | M1, M5 | SLO instrumentation with explicit endpoint scope (D5.5, per #M6) + burn-rate alerts; HPA + PDB (D5.4) ensures rolling deploys do not breach SLO; readiness probe gated on RBAC cache warm-up (per #M5); quarterly availability review post-GA. |
| NFR-006 | Encrypt PII at rest and in transit | M1, M2 | Column-level encryption + blind-index lookup tested in M1 (D1.1, per #M3); TLS 1.3 enforced via Nginx/ALB policy and verified in M2 acceptance; backup encryption verified quarterly. |

### Spec's Original Success Criteria Checklist

- [ ] All FR-001..FR-012 requirements implemented and tested → verified by the FR matrix above; final sign-off at end of M5.
- [ ] OWASP compliance verified via security scan → SAST + Schemathesis + DAST in CI continuously; external pen-test gate in D5.7.
- [ ] Load testing confirms 10K concurrent sessions → D5.6 (k6 30-minute scenario across cold/warm cache phases).
- [ ] OAuth2 flow works for Google and GitHub → M3 acceptance criteria; ongoing nightly contract tests (D3.8).
- [ ] Audit logs capture all auth events → D4.6 + M4 end-to-end audit test covering 15 event types with zero-PII assertion.

---

## Known Limitations

All 6 HIGH-severity invariant probe findings (INV-001, INV-003, INV-010, INV-011, INV-013, INV-015) have been concretely resolved via Mandatory Changes #M1–#M6 in the body of this roadmap; no HIGH items are deferred. The following MEDIUM/LOW items remain as documented awareness rather than blocking work — each is acknowledged in the roadmap text but not separately ticketed:

- **INV-002** (Redis AOF fsync mode for lockout counter survival): D1.2 specifies `appendfsync everysec` baseline; counters requiring guaranteed survival are mirrored to PostgreSQL `users.locked_until` (D4.5).
- **INV-004** (HIBP scope beyond registration): D5.1 password-change endpoint re-applies the HIBP denylist; reset endpoint references the same strength + denylist pipeline.
- **INV-005** (progressive-lockout cycle decay window): D4.5 specifies a rolling 24h Redis-TTL'd decay window keyed on `lockout:cycles:{user_id}`.
- **INV-008** (refresh-token family semantics): D2.4 codifies one family per login event per device; force-logout (D5.2) revokes all families across all devices.
- **INV-012** (sole-admin lost-2FA break-glass): D5.8 runbook documents the two-operator manual DB intervention.
- **INV-014** (audit log tamper-evidence beyond append-only): D5.7 pen-test scope explicitly includes audit-log tamper-evidence probing; ASVS §10.5 signed-log-entry adoption is a candidate post-GA hardening item but not blocking M5 GA.
- **INV-016** (CSP nonce for React 18 admin SPA): D2.9 + D5.2 specify nonce-based `script-src` for the admin SPA; `'unsafe-inline'` is not used.
- **INV-006**, **INV-007**, **INV-009** are addressed inline (RBAC cache sizing in D3.5, empty-shape envelope in API Conventions, deprecation policy in API Conventions + Cross-Cutting Security).

---

## Provenance Footnote

This document is an **adversarially-merged artifact** produced by `/sc:adversarial` from two independent roadmap variants and an invariant probe. Full audit trail:

- Base variant: [`./adversarial/variant-1-opus-default.md`](./adversarial/variant-1-opus-default.md) (opus, default)
- Cross-referenced variant: [`./adversarial/variant-2-sonnet-default.md`](./adversarial/variant-2-sonnet-default.md) (sonnet, default)
- Diff analysis: [`./adversarial/diff-analysis.md`](./adversarial/diff-analysis.md)
- Debate transcript: [`./adversarial/debate-transcript.md`](./adversarial/debate-transcript.md)
- Invariant probe: [`./adversarial/invariant-probe.md`](./adversarial/invariant-probe.md)
- Refactor plan: [`./adversarial/refactor-plan.md`](./adversarial/refactor-plan.md)
- Merge log: [`./adversarial/merge-log.md`](./adversarial/merge-log.md)

Per-section provenance is annotated inline via HTML comments. All 17 planned changes (Changes #1–#11 + Mandatory #M1–#M6) were applied; all 6 HIGH-severity invariant findings are concretely resolved in the body of this document.
