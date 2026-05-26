---
id: ROADMAP-AUTH-V1-VARIANT1
title: "User Authentication Service v1.0 — Delivery Roadmap (Opus Default Variant)"
source-spec: .dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md
generated-at: 2026-05-22
variant-tag: opus-default
target-release: v1.0 (Q2 2026)
owner: auth-team
status: Draft
---

# User Authentication Service v1.0 — Delivery Roadmap

## 1. Executive Summary

This roadmap operationalizes the merged PRD (AUTH-PRD-001) and TDD (AUTH-001) for the User Authentication Service v1.0 across six sequenced milestones spanning approximately 12 sprints (6 calendar months). The service is the foundational identity layer that unblocks Q2–Q3 2026 personalization features (projected $2.4M ARR contribution) and SOC2 Type II audit readiness scheduled for Q3 2026. Scope is deliberately constrained to email/password authentication, JWT-based stateless sessions with refresh-token rotation, self-service password reset, and structured audit logging — explicitly excluding OAuth/OIDC (v2.0), MFA (v1.1), and RBAC enforcement (separate PRD).

The sequencing strategy front-loads platform and data-model foundations (M1) so subsequent milestones can land independently behind feature flags. Token lifecycle (M2) and core authentication flows (M3) follow because they are prerequisites for both the profile (M4) and password-reset (M4) epics, while compliance instrumentation (M5) and production hardening (M6) close out the release. Every functional requirement (FR-AUTH.1 through FR-AUTH-005) and non-functional requirement (NFR-PERF-001/002, NFR-REL-001, NFR-SEC-001/002) traces to a numbered deliverable, and every milestone exits on measurable criteria rather than narrative checkpoints.

## 2. Roadmap Overview

- **Milestone count:** 6 (M1 Foundations, M2 Token Lifecycle, M3 Core Auth Flows, M4 Profile + Reset, M5 Compliance + Audit, M6 Hardening + GA)
- **Sequencing strategy:** Foundation-first with feature-flagged increments. Wave-1 (M1) establishes infra and contracts; Waves 2–4 (M2–M4) deliver vertical user-facing slices; Waves 5–6 (M5–M6) deliver non-functional / compliance posture required for GA and SOC2 audit.
- **Target completion:** Sprint 12 (end of Q2 2026) for GA-ready cut. SOC2 evidence collection runs in parallel through Sprint 13 (Q3 2026 audit window).
- **Sprint length assumption:** 2 calendar weeks. 12 sprints = 24 weeks ≈ 6 months. Team size assumption: 4 backend engineers, 2 frontend engineers, 0.5 SRE, 0.5 security reviewer.
- **Release vehicle:** Single GA cut at end of M6 behind feature flag `auth.v1.enabled`, with staged rollout (1% → 10% → 50% → 100%) over 7 days.

---

## 3. Milestones

### M1 — Foundations & Contracts

**ID:** M1
**Name:** Foundations & Contracts
**Goal:** Stand up the persistence layer, shared contracts, project skeleton, and CI/CD scaffolding so that subsequent milestones can land vertical slices without paying foundational tax.

**Scope (In):**

- PostgreSQL 15 schema for `UserProfile`, `auth_audit_log`, and `password_reset_tokens` tables with migrations under Flyway (or equivalent).
- Redis 7 namespace allocation for refresh tokens and rate-limit counters; eviction policy set to `noeviction` on the auth keyspace.
- TypeScript shared `@auth/contracts` package defining `UserProfile`, `AuthToken`, error envelope, and JSON-schema validators.
- `AuthService` Node.js 20 LTS project skeleton: ESLint, Prettier, Jest, ts-jest, Supertest, testcontainers, OpenAPI 3.1 spec stub.
- CI pipeline (GitHub Actions) with build, lint, unit-test, integration-test, container build, SBOM, and Trivy scan stages.
- Local dev environment via docker-compose: Postgres, Redis, SMTP sink (mailhog).

**Scope (Out):**

- Any user-facing endpoint logic (deferred to M3).
- JWT signing keys (deferred to M2, requires HSM/KMS decision).
- Production infrastructure (deferred to M6).

**Deliverables:**

| ID | Deliverable | Traces To |
|----|-------------|-----------|
| D1.1 | Postgres schema + migrations for `users`, `auth_audit_log`, `password_reset_tokens` | TDD §7, NFR-AUTH.3, Compliance audit logging |
| D1.2 | Redis keyspace design doc + `redis-cli` provisioning script (TLS, `requirepass`) | TDD §6.3, NFR-SEC-001 |
| D1.3 | `@auth/contracts` npm package v0.1.0 published to internal registry | TDD §7.1, §8.3 |
| D1.4 | OpenAPI 3.1 spec stub covering all 6 v1 endpoints (no impl yet) | TDD §8 |
| D1.5 | CI pipeline green on empty service skeleton, with branch protection on `main` | NFR-REL-001 evidence |
| D1.6 | Threat-model v0 (STRIDE) documented; signed off by security-reviewer | Risk R-SEC-1 |
| D1.7 | docker-compose dev environment + README "5-minute first run" | Engineering enablement |

**Dependencies:** None (entry milestone). Requires PostgreSQL 15 and Redis 7 access tokens from platform-team.

**Entry Criteria:**

- PRD AUTH-PRD-001 approved (currently Draft → must be Approved before M1 sprint 1 ends).
- TDD AUTH-001 reviewed by sys-architect and sec-reviewer.
- Engineering team allocated (4 BE, 2 FE confirmed in capacity plan).

**Exit Criteria (all measurable):**

- `make ci` exits 0 with ≥80% coverage on stub code (baseline guard).
- Postgres migration roll-forward and roll-back tested in CI (`flyway migrate` + `flyway undo` both succeed).
- OpenAPI spec passes `spectral lint` with zero errors.
- Threat model approved (signed PR comment from sec-reviewer).
- Dev environment from clean clone to first request in ≤5 minutes (timed walkthrough recorded).

**Effort estimate:** 2 sprints (Sprint 1–2).

**Milestone-specific risks:**

- *Schema premature lock-in:* Mitigated by tagging migrations as reversible and gating production application behind feature flag.
- *Contract churn:* Mitigated by versioning `@auth/contracts` from v0.1.0 and tagging breaking changes.

**Validation approach:** Architecture review with sys-architect; security review with sec-reviewer; smoke test of CI pipeline against a no-op endpoint; spectral lint on OpenAPI spec.

---

### M2 — Token Lifecycle

**ID:** M2
**Name:** Token Lifecycle (`JwtService` + `TokenManager`)
**Goal:** Deliver the JWT signing, verification, refresh, and revocation infrastructure that all authenticated flows in M3/M4 depend on.

**Scope (In):**

- `JwtService` with RS256 signing using 2048-bit RSA keys stored in KMS (AWS KMS or HashiCorp Vault — decision recorded in ADR-002).
- Key rotation playbook with overlapping `kid` header support so old tokens validate during the 15-minute rotation window.
- `TokenManager` issuing 15-minute access tokens and 7-day refresh tokens; refresh tokens are opaque (32 bytes from `crypto.randomBytes`), stored as SHA-256 hashes in Redis with TTL = 604800 s.
- Refresh-token rotation: every successful `/auth/refresh` revokes the previous refresh token and issues a new one (one-time-use semantics).
- Revocation list keyed on `jti` in Redis for emergency invalidation (e.g., compromised user).
- Clock-skew tolerance of 5 seconds in JWT verification (matches TDD §12).

**Scope (Out):**

- HTTP endpoints exposing these flows (M3 wires `/auth/refresh`; M2 ships only the library).
- MFA-related claim shape (out of v1.0 entirely per NG-002).

**Deliverables:**

| ID | Deliverable | Traces To |
|----|-------------|-----------|
| D2.1 | `JwtService` library with sign(), verify(), and key-rotation hooks | FR-AUTH-003, NFR-SEC-002 |
| D2.2 | `TokenManager` library: `issuePair()`, `refreshPair()`, `revoke(jti)`, `revokeAllForUser(userId)` | FR-AUTH-003, FR-AUTH.3 |
| D2.3 | KMS integration + ADR-002 (KMS vs Vault decision recorded) | NFR-SEC-002 |
| D2.4 | Key-rotation runbook with rehearsal evidence (rotation drill in staging) | Operational readiness |
| D2.5 | Redis token storage: hashed refresh tokens, `auth:rt:<sha256>` keys, TTL 604800 | TDD §6.3, §13 |
| D2.6 | Unit + integration tests covering issuance, refresh, rotation, revocation, expiry, clock-skew, and Redis-down failure modes | NFR-REL-001 |
| D2.7 | Performance benchmark: `TokenManager.refresh()` p95 < 100 ms with Redis local SLA | TDD §4.1 |

**Dependencies:** M1 (`@auth/contracts`, Redis keyspace, project skeleton).

**Entry Criteria:**

- M1 exit criteria met.
- KMS access provisioned (or Vault namespace allocated) with role permissions audited.
- Crypto library choice (`jose` v5+ or `node-jsonwebtoken`) approved by sec-reviewer.

**Exit Criteria (all measurable):**

- 100% of M2 unit tests pass; integration tests pass against ephemeral Redis container.
- Token refresh benchmark: p95 ≤ 100 ms at 200 RPS sustained for 60 s (k6 report attached).
- Key-rotation drill executed in staging: old `kid` tokens valid for 15 min after rotation; new tokens validate immediately.
- Redis-down test: refresh requests return 503 with retry-after header (no stale-token serving — TDD §12).
- Coverage ≥85% for `JwtService` and `TokenManager` modules.

**Effort estimate:** 2 sprints (Sprint 3–4).

**Milestone-specific risks:**

- *Token-rotation race:* Two concurrent refreshes with the same refresh token must not both succeed. Mitigation: Lua script for atomic GET+DEL in Redis; integration test asserting only one of N parallel requests returns 200.
- *Clock skew between issuer and verifier:* Mitigated by 5 s tolerance in `verify()` and NTP discipline on hosts (monitored via node_exporter).
- *Key compromise:* Mitigated by KMS-backed private key (never leaves HSM) and `revokeAllForUser` administrative tool.

**Validation approach:** k6 load test, key-rotation drill, security review with sec-reviewer focused on JWT pitfalls (alg confusion, none-alg), property-based tests on rotation invariants using fast-check.

---

### M3 — Core Authentication Flows

**ID:** M3
**Name:** Core Authentication Flows (Login / Register / Refresh / Logout)
**Goal:** Ship the primary HTTP endpoints and frontend pages that fulfill FR-AUTH.1, FR-AUTH.2, FR-AUTH-003, and the logout user story.

**Scope (In):**

- `POST /auth/login`, `POST /auth/register`, `POST /auth/refresh`, `POST /auth/logout` endpoints.
- `PasswordHasher` library wrapping bcrypt cost factor 12 with constant-time comparison and pepper (HMAC-SHA256 with KMS-managed pepper key).
- Password policy enforcement: ≥8 chars, ≥1 uppercase, ≥1 number, ≥1 special char (server-side authoritative; client mirrors for UX).
- Email normalization: lowercase + Unicode NFC + trim; uniqueness enforced by Postgres UNIQUE constraint with explicit conflict handling for race conditions.
- Account-lockout policy: 5 failed login attempts within 15 minutes locks for 30 minutes; counter keyed `auth:lockout:<userId>` in Redis.
- Rate limits per TDD §8.1: 10 req/min/IP on login, 5 req/min/IP on register, 30 req/min/user on refresh. Implemented as sliding-window in Redis.
- Frontend: `LoginPage`, `RegisterPage`, `AuthProvider` React components with silent-refresh logic on 401 + retry once.

**Scope (Out):**

- Profile endpoint (M4).
- Password reset (M4).
- Audit log persistence (M5 — but log events are emitted in M3, just not yet stored in long-term table).

**Deliverables:**

| ID | Deliverable | Traces To |
|----|-------------|-----------|
| D3.1 | `POST /auth/login` endpoint with bcrypt verification, lockout, audit-event emission | FR-AUTH.1, FR-AUTH-001 |
| D3.2 | `POST /auth/register` endpoint with email uniqueness, password policy, profile creation | FR-AUTH.2, FR-AUTH-002 |
| D3.3 | `POST /auth/refresh` endpoint wiring `TokenManager.refreshPair()` to HTTP | FR-AUTH-003, FR-AUTH.3 |
| D3.4 | `POST /auth/logout` endpoint revoking active refresh token and adding `jti` to revocation list | User story AUTH-E1.logout |
| D3.5 | `PasswordHasher` library (bcrypt cost 12 + pepper) with benchmark < 500 ms per hash | NFR-SEC-001 |
| D3.6 | Sliding-window rate limiter with per-IP and per-user buckets | TDD §8.1 |
| D3.7 | Account-lockout module with 5-attempts-in-15min trigger and 30-minute cooldown | TDD §13, Error matrix row 3 |
| D3.8 | `LoginPage`, `RegisterPage`, `AuthProvider` React components | TDD §10 |
| D3.9 | E2E happy-path + 12 negative-path Playwright tests (wrong password, locked account, duplicate email, weak password, expired token, revoked token, refresh-token reuse, malformed body, oversized payload, SQL injection probe, XSS probe, CSRF probe) | TDD §15 |

**Dependencies:** M1 (schema, contracts), M2 (`JwtService`, `TokenManager`).

**Entry Criteria:**

- M2 exit criteria met.
- API Gateway available in staging with CORS allowlist configured for known frontend origins.
- Pepper key provisioned in KMS (separate `kid` from JWT signing key).

**Exit Criteria (all measurable):**

- All 4 endpoints respond to spec-compliant requests with documented status codes (verified by contract tests generated from OpenAPI).
- Login p95 ≤ 200 ms at 500 concurrent requests in staging (NFR-PERF-001, NFR-PERF-002 — k6 report).
- bcrypt hash p95 ≤ 500 ms with cost factor 12 (microbenchmark).
- Account lockout proven: 5 consecutive failures returns 423 on the 6th attempt; counter resets 30 minutes later.
- Rate-limit boundary test: exactly 10 login req/min/IP succeed; the 11th returns 429 (sliding-window correctness asserted).
- Refresh-token reuse test: replaying a rotated refresh token returns 401 and triggers `revokeAllForUser` (defense against token theft).
- Zero password-related strings in application logs (regex scan of stdout/stderr during E2E run).
- E2E coverage ≥ 90% for the four happy paths plus all 12 negative paths.

**Effort estimate:** 3 sprints (Sprint 5–7).

**Milestone-specific risks:**

- *User-enumeration leakage* via timing or differential error messages (registration confirm path, login error path). Mitigated by constant-time bcrypt compare on a dummy hash when user not found, and identical error envelopes for "unknown email" and "wrong password".
- *bcrypt CPU bottleneck* under load. Mitigated by horizontal scaling and cost-12 budget validated in benchmark; if p95 exceeds 500 ms, reduce to cost 11 only with sec-reviewer approval (recorded in ADR-003).
- *Refresh-token reuse race* (concurrent refresh from two tabs). Atomic Lua script in M2 D2.6 + integration test in M3 D3.9.
- *Empty/oversized payloads:* request body limit set to 4 KB on auth endpoints; payloads > 4 KB return 413; empty body returns 400 with schema-validation error.

**Validation approach:** k6 load test, OWASP ZAP active scan, security review focused on authn flaws (OWASP ASVS V2), contract tests via `dredd` against OpenAPI spec, Playwright E2E suite.

---

### M4 — Profile Retrieval & Password Reset

**ID:** M4
**Name:** Profile Retrieval & Self-Service Password Reset
**Goal:** Deliver FR-AUTH.4 (`/auth/me`) and FR-AUTH.5 (two-step password reset) and the corresponding frontend ProfilePage and reset UI.

**Scope (In):**

- `GET /auth/me` returning `UserProfile` JSON for the bearer-authenticated user.
- `POST /auth/reset-request` with email parameter; always returns 202 Accepted regardless of registration status (anti-enumeration).
- `POST /auth/reset-confirm` with `token` + `newPassword`; validates token, updates hash, invalidates ALL active refresh tokens for that user via `TokenManager.revokeAllForUser(userId)`.
- Reset token: 32-byte random, stored hashed (SHA-256) in `password_reset_tokens` table with `user_id`, `expires_at` (NOW() + 1 hour), `used_at` (nullable), single-use semantics.
- Email integration with SendGrid (or equivalent) using templated reset email; queued via BullMQ for async delivery with 60-second SLA and 3 retry attempts on transient failures.
- ProfilePage React component rendering `UserProfile`.
- Reset request and reset confirmation pages.

**Scope (Out):**

- Profile editing (update name/email) — deferred to v1.1.
- Email verification at registration — deferred to v1.1 (registration in M3 marks user `email_verified = false`; downstream features can enforce verification later).

**Deliverables:**

| ID | Deliverable | Traces To |
|----|-------------|-----------|
| D4.1 | `GET /auth/me` endpoint returning `UserProfile` from JWT subject | FR-AUTH.4, FR-AUTH-004 |
| D4.2 | `POST /auth/reset-request` with anti-enumeration 202 response and email enqueue | FR-AUTH.5 part 1, Error matrix row 4 |
| D4.3 | `POST /auth/reset-confirm` with token validation, password update, session invalidation | FR-AUTH.5 part 2, Error matrix row 5 |
| D4.4 | `password_reset_tokens` table with single-use enforcement (`used_at` updated in same transaction as password hash) | TDD §7.2 |
| D4.5 | SendGrid integration + BullMQ job queue with 60-second delivery SLA and 3 retries | TDD §6.3, PRD JTBD reset |
| D4.6 | ProfilePage React component + reset-request and reset-confirm pages | TDD §10 |
| D4.7 | E2E tests: profile load, reset happy path, expired token, used token, unregistered email | TDD §15 |
| D4.8 | Email-template review (legal + design) and approval log | GDPR consent, brand |

**Dependencies:** M3 (endpoints, `PasswordHasher`, `AuthProvider`).

**Entry Criteria:**

- M3 exit criteria met.
- SendGrid account provisioned with sandbox + production templates approved.
- BullMQ Redis namespace allocated separately from auth keys (`mq:` prefix).

**Exit Criteria (all measurable):**

- `GET /auth/me` p95 ≤ 50 ms (cached `UserProfile` row lookup; well under the 200 ms aggregate budget).
- Reset email delivery 95th percentile ≤ 60 s in staging (SendGrid event webhook timing).
- Reset-token reuse rejected: confirm endpoint called twice with the same token returns 410 Gone on second call.
- Expired reset token (force `expires_at` < NOW()) returns 410 Gone.
- After successful reset, all existing refresh tokens for that user are invalid (verified by attempting refresh with a pre-reset refresh token — expect 401).
- Anti-enumeration verified: identical timing and response for registered vs unregistered emails (± 25 ms variance over 100 trials).
- E2E coverage ≥ 90% for the new flows.

**Effort estimate:** 2 sprints (Sprint 8–9).

**Milestone-specific risks:**

- *Reset-token reuse:* Mitigated by `used_at` column + SELECT FOR UPDATE in confirm transaction; integration test asserts only one of N parallel confirms succeeds.
- *Email enumeration via timing:* Mitigated by always enqueuing a dummy job (no email actually sent for unregistered addresses) so the response path is identical.
- *Email-delivery failure blocking reset:* SendGrid retries + dead-letter queue + Jordan-the-admin dashboard for manual reissue. Open question PRD-OQ-1 resolved here (async).
- *Reset token leakage via referrer:* Reset URL fragments use `#token=...` not query string; documented in email template.
- *Partial failures:* If hash update succeeds but session-revoke fails, transaction rolled back; both happen in the same DB transaction with token-revoke deferred to commit hook (saga compensation if Redis call fails — recorded in ADR-004).

**Validation approach:** Playwright E2E, timing-attack measurement script (100 trials), SendGrid webhook integration test, ZAP scan of reset flow.

---

### M5 — Compliance, Audit Logging & Observability

**ID:** M5
**Name:** Compliance, Audit Logging & Observability
**Goal:** Deliver the SOC2 audit-logging surface, GDPR consent capture, Prometheus metrics, OpenTelemetry traces, and Jordan-the-admin facing log query tool.

**Scope (In):**

- `auth_audit_log` table population for every login (success/failure), registration, refresh, logout, reset-request, reset-confirm, lockout, and admin action. Fields: `event_id` (UUID), `user_id` (nullable for unregistered email events), `event_type`, `timestamp`, `ip_address`, `user_agent`, `outcome`, `metadata` (jsonb).
- 12-month retention with monthly partitioning; archive job to S3 (or equivalent object storage) after partition rolls off.
- GDPR consent recording at registration: explicit checkbox state captured with timestamp into `users.consent_accepted_at` + `users.consent_version`.
- Prometheus metrics: `auth_login_total{outcome}`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`, `auth_password_reset_total{stage}`, `auth_lockout_total`, `auth_audit_log_writes_total`.
- OpenTelemetry tracing across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` → DB.
- Alert rules: login failure rate > 20% over 5 min (warning), p95 latency > 500 ms over 5 min (warning), p95 latency > 1 s (page), Redis connection failures (page), audit-log write failures (page — compliance critical).
- Admin log-query CLI / lightweight UI: query by user_id, date range, event type with pagination.
- Log scrubbing: explicit allowlist of fields persisted to audit log; deny-list test asserts no password/token strings ever appear.

**Scope (Out):**

- Admin self-service account lock/unlock UI (deferred to v1.1).
- Real-time SIEM integration (export hooks shipped; downstream platform-team owns ingestion).

**Deliverables:**

| ID | Deliverable | Traces To |
|----|-------------|-----------|
| D5.1 | `auth_audit_log` table with monthly partitions and 12-month retention policy | GDPR/SOC2, Compliance §audit logging |
| D5.2 | Audit-event emitter wired into M3/M4 endpoints with at-least-once semantics (outbox pattern) | SOC2 Type II controls |
| D5.3 | GDPR consent capture + `consent_version` migration | GDPR/PRD §Legal |
| D5.4 | Prometheus metrics + Grafana dashboard `auth-overview` | TDD §14 |
| D5.5 | OpenTelemetry spans across the full request lifecycle | TDD §14 |
| D5.6 | Alert rule definitions in alertmanager + runbook stubs for each alert | Operational readiness |
| D5.7 | Admin log query CLI (`auth-admin log query --user X --since Y --until Z --type login_failed`) | Jordan JTBD, PRD AUTH-E3 story |
| D5.8 | Log-scrub deny-list automated test (CI gate) | NFR-SEC-001 |
| D5.9 | SOC2 control mapping document (CC6.1, CC7.2, CC7.3, A1.2 mapped to deliverables) | Compliance §SOC2 |

**Dependencies:** M3 (endpoints emit events), M4 (reset events).

**Entry Criteria:**

- M4 exit criteria met.
- Prometheus + Grafana stack available in staging.
- S3 archive bucket provisioned with lifecycle policy.

**Exit Criteria (all measurable):**

- 100% of state-changing auth endpoints emit at least one audit event (verified by CI test that diffs endpoint inventory vs emitter coverage).
- Audit-event write latency adds ≤ 10 ms p95 to the request path (outbox + async flush).
- Grafana `auth-overview` dashboard renders all 7 metrics with non-zero data from staging traffic.
- All 5 alert rules fire correctly in synthetic-failure tests (chaos drills).
- Log-scrub CI test passes (zero password/token strings in any audit log row generated by E2E suite).
- 12-month retention proven by simulating partition rollover (test fixture advances `current_date` 13 months).
- SOC2 control mapping signed off by compliance contact.

**Effort estimate:** 1.5 sprints (Sprint 10 + half of Sprint 11).

**Milestone-specific risks:**

- *Audit-log write failure during transaction:* Mitigated by outbox pattern — write event row in same DB transaction as state change, then async publisher drains to long-term audit store. Failure to drain pages on-call but never blocks user flow.
- *PII over-collection:* Mitigated by allowlist + deny-list tests; only email and display name persisted, IP and UA logged for audit only with documented retention.
- *Metric cardinality explosion:* `outcome` label has only 4 values; user_id is NOT a metric label (it goes to traces).

**Validation approach:** Chaos drill (kill audit-log writer, observe outbox catch-up), CI scrub test, compliance review with sec-reviewer + legal.

---

### M6 — Hardening & GA

**ID:** M6
**Name:** Production Hardening & GA Rollout
**Goal:** Take the feature-flagged service to GA via load testing, penetration testing, staged rollout, on-call readiness, and final acceptance.

**Scope (In):**

- Full load test at 500 concurrent + 2,000 RPS sustained for 1 hour against staging that mirrors prod.
- Third-party penetration test focused on authentication (engagement scope: OWASP Top 10, OWASP ASVS V2/V3, auth-specific flaws).
- DAST + SAST sweeps in CI: ZAP baseline, Snyk, Semgrep auth rules.
- Production deploy with blue/green strategy + feature-flag `auth.v1.enabled` defaulted false.
- Staged rollout: 1% → 10% → 50% → 100% over 7 days, each step gated on error-rate < 0.5% and p95 < 200 ms.
- On-call runbooks for every alert from M5; PagerDuty schedule populated.
- Disaster-recovery drill: simulated full Redis loss (no refresh-token continuity) and full Postgres failover.
- Acceptance test pass against all PRD success metrics (registration conversion measurable in funnel, login p95 < 200 ms, failed-login < 5%).
- Documentation freeze: API docs published, internal SDK shipped, support team trained.

**Scope (Out):**

- Anything in NG-001/002/003 (OAuth, MFA, RBAC).
- Multi-region active-active deployment (single-region with cross-AZ HA at GA).

**Deliverables:**

| ID | Deliverable | Traces To |
|----|-------------|-----------|
| D6.1 | Load-test report at 500 concurrent / 2k RPS / 1 h with p95 < 200 ms, p99 < 400 ms, error rate < 0.1% | NFR-PERF-001, NFR-PERF-002, NFR-REL-001 |
| D6.2 | Pen-test report with all High/Critical findings remediated; Medium findings either fixed or accepted with sec-reviewer sign-off | Risk R-SEC-1, R-SEC-2 |
| D6.3 | DAST/SAST CI gates passing on `main` (no new High findings) | NFR-SEC-001 |
| D6.4 | Blue/green deploy infra + feature flag wired through Unleash (or equivalent) | Rollout safety |
| D6.5 | Staged rollout dashboard with auto-rollback trigger on SLO violation | Operational readiness |
| D6.6 | 12 on-call runbooks (one per alert + 7 scenario runbooks for common incidents) | Operational readiness |
| D6.7 | DR drill report (Redis loss + Postgres failover) | NFR-REL-001 |
| D6.8 | PRD success-metric acceptance: registration funnel instrumented, login p95 dashboard live, failed-login < 5% in 7-day rolling window | PRD §Success Metrics |
| D6.9 | Public API documentation + internal client SDK v1.0.0 | Sam-the-API-consumer JTBD |
| D6.10 | Support-team training + escalation matrix | Jordan JTBD |

**Dependencies:** M5 (observability ready before load test; runbooks reference M5 metrics).

**Entry Criteria:**

- M5 exit criteria met.
- Production environment provisioned (Postgres, Redis, KMS, SendGrid, observability stack).
- Pen-test vendor engaged with statement of work signed.

**Exit Criteria (all measurable):**

- Load test passes targets above; report attached to release.
- Pen-test High/Critical = 0 unresolved; Medium ≤ 3 with documented acceptance.
- Staged rollout reaches 100% without auto-rollback.
- 30-day post-GA observation: availability ≥ 99.9%, login p95 ≤ 200 ms, registration conversion > 60% (or root-cause analysis filed if not).
- All PRD success metrics have a live dashboard and a named metric owner.
- Sign-off from PM, EM, Architect, Security, Compliance.

**Effort estimate:** 1.5 sprints (second half of Sprint 11 + Sprint 12).

**Milestone-specific risks:**

- *Pen-test finds a structural flaw late:* Mitigated by booking the engagement at start of M6, not end; budget 1 sprint of fix-time buffer.
- *Rollout regression:* Mitigated by feature flag + auto-rollback on SLO violation + 7-day staged ramp.
- *Capacity surprise at 100%:* Mitigated by load test at 4× projected peak (2k RPS vs 500 concurrent baseline).

**Validation approach:** k6 load test, vendor pen-test, chaos drills, staged-rollout dashboard with automated SLO gates.

---

## 4. Cross-Milestone Dependency Table

| From → To | Type | Rationale |
|----------|------|-----------|
| M1 → M2 | Hard | M2 needs `@auth/contracts`, Redis namespace, project skeleton |
| M1 → M3 | Hard | Schema, contracts, CI pipeline |
| M2 → M3 | Hard | `JwtService` + `TokenManager` libraries are direct dependencies |
| M2 → M4 | Hard | Reset confirmation calls `revokeAllForUser` from `TokenManager` |
| M3 → M4 | Hard | `PasswordHasher` reused by reset-confirm; `AuthProvider` reused by ProfilePage |
| M3 → M5 | Soft | M5 instruments M3 endpoints; M3 emits provisional events to a stub sink while M5 is in flight |
| M4 → M5 | Soft | Reset events need audit instrumentation |
| M5 → M6 | Hard | Load test and SLO gating depend on metrics + alerts in place |
| M4 → M6 | Hard | All functional scope must be done before GA |
| External: PRD approval → M1 | Hard | PRD is currently Draft; must be Approved before M1 exits |
| External: KMS access → M2 | Hard | Signing keys live in KMS |
| External: SendGrid → M4 | Hard | Reset email delivery |
| External: Pen-test vendor → M6 | Hard | Engagement scheduled at M6 start |

Critical path: PRD approval → M1 → M2 → M3 → M4 → M5 → M6. M5 partial-overlap with M6 is permitted (observability and load test prep can run concurrently with admin-CLI polish in M5).

---

## 5. Risk Register

| ID | Risk | Probability | Impact | Mitigation | Owner |
|----|------|------------|--------|-----------|-------|
| R-SEC-1 | Implementation flaw enables credential theft or account takeover | Low | Critical | Threat model in M1; security reviews at M2/M3/M4 gates; third-party pen-test in M6; OWASP ASVS V2 checklist gated in CI | sec-reviewer |
| R-SEC-2 | Token reuse / refresh-token rotation race allows session hijack | Medium | High | Atomic Lua GET+DEL in Redis (M2); reuse-detection triggers `revokeAllForUser` (M3 D3.9 test); pen-test scope (M6) | tech-lead |
| R-COMP-1 | SOC2 audit fails because audit-log coverage is incomplete | Medium | High | Endpoint-to-emitter coverage CI test (M5 D5.2); compliance sign-off gate in M5 exit | compliance |
| R-EMAIL-1 | SendGrid outage blocks password reset | Low | Medium | Retry + DLQ (M4 D4.5); admin manual-reissue path; multi-provider abstraction documented as future option in ADR-005 | platform-team |
| R-PERF-1 | bcrypt cost 12 misses 500 ms target under realistic CPU | Medium | Medium | Microbenchmark in M2; ADR-003 contingency to cost 11 with sec sign-off; horizontal scaling baked into deploy plan | tech-lead |
| R-UX-1 | Registration conversion < 60% due to friction | Medium | High | Usability test of M3 forms before M6; inline validation; minimal field count; A/B flag-driven copy tests post-GA | product |
| R-DATA-1 | Postgres schema change later in v1.x breaks active sessions | Low | Medium | Migrations reversible; backwards-compatible field additions only; ADR-001 enforces this | tech-lead |
| R-RATE-1 | Rate-limit boundary error allows brute-force | Medium | High | Sliding-window with strict per-IP and per-user buckets (M3 D3.6); boundary test asserting 11th request fails; lockout reinforces (M3 D3.7) | tech-lead |
| R-DEP-1 | KMS or Vault unavailable at signing time | Low | Critical | Local key cache with 5-minute lifetime; circuit breaker; pager alert; readiness probe excludes node if KMS unhealthy (M2 D2.3) | sre |
| R-SCOPE-1 | Scope creep (MFA, social login) jeopardizes Q2 GA | Medium | High | Roadmap explicitly excludes via NG-001/002/003; product steering committee gates any change; v1.1 roadmap stubbed for parking lot | product |

---

## 6. Success Metrics

Metrics traced directly to PRD §Success Metrics and TDD §4:

| Metric | Target | Methodology | Owner | First-measurement milestone |
|--------|--------|-------------|-------|----------------------------|
| Registration conversion rate | > 60% | Funnel: `landing_view` → `register_submit` → `register_success` events in product analytics; numerator/denominator computed on a 7-day rolling window | product | M6 (live), with instrumentation in M5 |
| Login response time (p95) | < 200 ms | APM histogram `auth_login_duration_seconds` aggregated p95 over 5-minute rolling windows | sre | M3 (staging), M6 (production SLO) |
| Average session duration | > 30 minutes | Computed as time between login event and explicit logout OR expiry of refresh chain; emitted in audit log | product | M6 |
| Failed login rate | < 5% | `auth_login_total{outcome="failure"}` / `auth_login_total` over 7-day rolling | sre | M5 |
| Password reset completion | > 80% | `auth_password_reset_total{stage="confirm_success"}` / `auth_password_reset_total{stage="request"}` over 7-day window | product | M5 |
| Service availability | 99.9% | Health-check uptime over 30-day rolling | sre | M6 (post-GA SLO) |
| Token refresh latency p95 | < 100 ms | `auth_token_refresh_total` histogram p95 | sre | M2 (microbenchmark), M6 (production) |
| Password hash time | < 500 ms | bcrypt benchmark in CI + APM histogram on hash call | tech-lead | M2 (benchmark), M3 (production) |

Each metric has a Grafana dashboard panel (M5 D5.4) and a named accountable owner. PRD targets exceed only when the entire 7-day window meets the bar; otherwise the on-call rotation files an RCA.

---

## 7. Out of Scope / Deferred

The following items are explicitly excluded from v1.0 and tracked in the v1.1+ parking lot:

| Item | Rationale | Tentative target |
|------|-----------|-----------------|
| OAuth/OIDC (Google, GitHub, etc.) | Requires third-party app registrations and richer identity merging logic; v1.0 ships email/password only | v2.0 |
| Multi-factor authentication (TOTP, SMS, WebAuthn) | Requires SMS or authenticator-app delivery infrastructure; tracked separately as MFA-PRD | v1.1 |
| Role-based access control enforcement | Authorization is a separate concern; `roles` field is captured but not enforced by `AuthService` | Separate PRD |
| Social login | Depends on OAuth/OIDC layer above | v2.0 |
| Profile editing (update name/email/password while logged in) | Reset flow covers password; broader profile editing planned alongside settings page | v1.1 |
| Email verification at registration (mandatory) | `email_verified` flag captured in v1.0 (default false); enforcement deferred | v1.1 |
| Multi-device session management UI | Refresh-token list per user exists in Redis; user-facing "active sessions" page deferred | v1.1 |
| Admin self-service lock/unlock UI | Admin CLI ships in v1.0 (M5 D5.7); GUI deferred | v1.1 |
| "Remember me" extended sessions | Open question PRD-OQ-4 resolved as "no" for v1.0 (single 7-day refresh window) | v1.1 |
| Multi-region active-active | v1.0 is single-region with cross-AZ HA | v2.0 |
| Real-time SIEM integration | Audit logs export hooks shipped; downstream ingestion not in scope | Platform-team owned |

---

## 8. Assumptions

Explicit assumptions — surfaced so they can be challenged in adversarial debate:

1. **Sprint length = 2 weeks** and team composition holds (4 BE, 2 FE, 0.5 SRE, 0.5 sec) for the full 12 sprints; vacation/onboarding loss baked in at 15%.
2. **PostgreSQL 15 and Redis 7** are provisioned by platform-team with TLS, encryption-at-rest, and automated backups before Sprint 1.
3. **KMS (AWS KMS or Vault) access** is approved and provisioned before Sprint 3; failure to confirm by end of M1 escalates to a P1 dependency block.
4. **SendGrid (or equivalent) account** with production sending reputation is provisioned by Sprint 7 (M4 entry).
5. **PRD AUTH-PRD-001 is approved** by all stakeholders (Product, Eng Lead, Design Lead, Exec Sponsor) before the end of M1 sprint 2; otherwise M2 entry slips.
6. **Frontend framework supports client-side routing and token-based auth** (PRD §Assumptions); React + React Router v6 confirmed.
7. **Bcrypt cost factor 12 fits within the 500 ms hashing budget** on production CPU class (validated in M2 benchmark; fallback to 11 documented in ADR-003).
8. **Pen-test vendor capacity** is bookable with ≤ 4 weeks lead time (engagement signed by start of M6).
9. **No regulatory changes** between now and Q2 GA that would expand v1.0 scope (e.g., new mandatory MFA requirement).
10. **Email deliverability** to common providers (Gmail, Outlook, corporate ESPs) is acceptable; SPF/DKIM/DMARC configured by platform-team.
11. **Internal client SDK** consumers (Sam-the-API-consumer) are willing to migrate from ad-hoc API keys to JWT bearer auth on the v1.0 timeline; communication plan owned by product.
12. **Audit-log retention of 12 months** satisfies SOC2 requirements; legal has confirmed this is adequate for v1.0.
13. **Anti-enumeration latency variance** of ± 25 ms is achievable via constant-time dummy hashing; if hardware variance prevents this, M3/M4 acceptance criteria adjust to ± 50 ms with sec sign-off.
14. **No requirement for password history / disallow-last-N-passwords** in v1.0; deferred to v1.1.

If any assumption is invalidated, the affected milestone enters a re-planning gate before exit.

---

## 9. Compliance & Security

### 9.1 SOC2 Control Mapping

| Control | Description | Roadmap deliverable |
|---------|-------------|---------------------|
| CC6.1 | Logical and physical access controls | D5.1 audit log, D5.2 emitter, D3.7 lockout |
| CC6.6 | Transmission of information | TLS 1.3 enforcement (M3), KMS-backed signing (M2 D2.3) |
| CC6.7 | Restriction of unauthorized access | D2.1 JWT verify, D3.1 endpoint authn, D3.6 rate limit |
| CC7.2 | Detection of vulnerabilities | D6.3 DAST/SAST, D5.6 alerting |
| CC7.3 | Incident response | D6.6 runbooks, M5 alert rules |
| A1.2 | Availability monitoring | D5.4 metrics, D6.5 staged rollout, D6.7 DR drill |
| GDPR Art. 7 | Consent capture | D5.3 consent record |
| GDPR Art. 5(1)(c) | Data minimization | Only email + display name + hashed password persisted (TDD §7) |
| NIST SP 800-63B | Password strength | D3.5 PasswordHasher + policy enforcement |

### 9.2 Threat Model Summary (STRIDE)

| Threat | Vector | Mitigation milestone |
|--------|--------|---------------------|
| Spoofing | Stolen credential | bcrypt + lockout (M3); future MFA (v1.1) |
| Tampering | JWT modification | RS256 + key rotation (M2) |
| Repudiation | User denies action | Audit log with IP/UA/timestamp (M5) |
| Information disclosure | Password/token in logs | Log allowlist + CI scrub test (M3, M5 D5.8) |
| Denial of service | Auth-endpoint flood | Rate limits + per-IP/user buckets (M3 D3.6); upstream WAF assumed |
| Elevation of privilege | Refresh-token theft | Rotation + reuse detection (M2 D2.7, M3 D3.9); revokeAllForUser on misuse |
| Enumeration | Login/reset reveals user existence | Generic error envelope + constant-time path + always-202 reset (M3, M4) |
| Token replay | Captured access token reused | Short 15-min TTL; revocation list keyed by `jti` (M2) |

---

## 10. Operational Readiness

- **Observability:** Prometheus + Grafana dashboard `auth-overview` (D5.4); OTel traces (D5.5); structured JSON logs at INFO with redaction (D5.8).
- **Alerting:** 5 baseline alerts (D5.6) routed to PagerDuty; severity matrix documented (warning vs page).
- **Runbooks:** 12 runbooks (D6.6) — login latency, error spike, Redis down, Postgres failover, KMS unavailable, SendGrid outage, audit-log lag, refresh-token reuse alert, key-rotation failure, lockout flood, rate-limit misconfig, GA rollback.
- **On-call:** Auth-team rotation populated with 4-engineer pool; secondary backstop from platform-team for infra concerns. PagerDuty schedule active from Sprint 11.
- **DR:** Postgres point-in-time recovery (RPO ≤ 5 min); Redis replicas in two AZs (refresh-token loss is acceptable — users re-authenticate); KMS cross-region replication; full DR drill in M6 D6.7.
- **Capacity:** k6 load test at 500 concurrent + 2k RPS validates 4× current projection; auto-scaling group with min 3 / max 12 nodes.
- **Feature flag:** `auth.v1.enabled` controls rollout; `auth.v1.lockout.enabled` and `auth.v1.reset.enabled` allow surgical pause of subsystems without full rollback.
- **Documentation:** API docs (D6.9), internal SDK v1.0.0, support training (D6.10), `KNOWLEDGE.md` updates per ADR.
- **Change management:** All schema changes via reversible migrations; ADR-001 mandates backwards-compatible additions during v1.x.

---

## 11. Sequencing Rationale

**Why M1 first?** Schema, contracts, and CI are the unavoidable foundation. Skipping them invites rework. Two sprints is short because the scope is genuinely small.

**Why M2 before M3?** `JwtService` and `TokenManager` are libraries that M3 endpoints consume. Splitting them out lets us security-review and benchmark the crypto-sensitive code in isolation, with property tests on rotation invariants, before HTTP concerns muddy the waters.

**Why M3 before M4?** `/auth/me` and reset both depend on `PasswordHasher`, `AuthProvider`, and the existence of authenticated users. M4 reuses the M3 surface; doing M4 first would have forced stubbing the very flows M4 verifies.

**Why M5 partially overlaps M3?** Audit-event emission is wired into M3 endpoints from day one (events go to a stub sink). M5 lights up the durable audit table, dashboards, and alerts. This split prevents a "compliance bolt-on at the end" anti-pattern that would otherwise miss events.

**Why M6 last and feature-flag-gated?** Load testing, pen testing, and staged rollout only make sense once the functional surface is frozen. The feature flag allows production deploy in M6's first sprint with zero user impact, decoupling deploy from release.

**Why six milestones rather than fewer or more?** Fewer would force vertical slices to span more concerns (security + persistence + UI + telemetry in one go), increasing review surface and merge conflicts. More would over-segment the work given a team of 6 engineers — coordination overhead would exceed parallelism gains. Six aligns to one milestone per ~2 sprints with one milestone (M5) running slightly compressed because its dependencies (M3, M4) provide ready integration points.

**What about regressions?** Each milestone exits on measurable thresholds that include backwards-compat checks: M1's reversible migrations, M2's overlapping `kid` validity during rotation, M3's contract tests against frozen OpenAPI spec, M4's session-revoke transactionality, M5's metric stability over a 7-day window, and M6's staged rollout with auto-rollback on SLO violation.

**Edge cases consciously sequenced for early discovery:**

- Token rotation race → covered by M2 D2.6 (atomic Lua) before any user touches it.
- Session invalidation race on reset → covered by M4 D4.3 single-transaction semantics.
- Reset-token reuse → M4 D4.4 single-use enforcement asserted in tests.
- Rate-limit boundary precision → M3 D3.6 sliding-window with exact-N-allowed boundary test.
- Empty / oversized inputs → M3 D3.9 negative-path Playwright matrix.
- Partial failures (DB ok, Redis down on logout / refresh / reset) → M2 D2.6 503 + retry-after; M4 ADR-004 saga compensation.
- Clock skew → M2 §verify with 5 s tolerance + NTP monitoring (M5 D5.6 alert).

---

## 12. Internal Reference Index

- D1.1 — `auth_audit_log` is created here but populated in M5.
- D2.6 — Atomic refresh test underpins R-SEC-2 mitigation.
- D3.7 — Account lockout sized to match PRD error matrix row 3.
- D4.3 — Reset confirm transaction underpins R-SEC-2 and R-DATA-1 mitigations.
- D5.2 — Outbox emitter ensures audit completeness (R-COMP-1 mitigation).
- D6.5 — Staged rollout with auto-rollback closes the loop on rollout safety (R-SCOPE-1, R-PERF-1).
- ADR-001 — Backwards-compatible schema rule.
- ADR-002 — KMS vs Vault decision.
- ADR-003 — bcrypt cost-factor contingency.
- ADR-004 — Reset transaction + Redis compensation.
- ADR-005 — Email-provider abstraction parking lot.

All FR / NFR identifiers in this roadmap resolve to PRD AUTH-PRD-001 §Technical Requirements or TDD AUTH-001 §5. All TDD section references resolve to `merged-prd-tdd-user-auth.md`.

---

## 13. Detailed Edge-Case Catalog

This section enumerates the edge cases that are easy to miss but expensive to find post-GA. Each entry names the milestone that owns the mitigation and the test artifact that proves it.

### 13.1 Token Rotation Edge Cases

| Case | Behavior | Owner | Proof |
|------|----------|-------|-------|
| Concurrent refresh from two browser tabs sharing the same refresh token | Exactly one returns 200 with a new pair; the other returns 401 and triggers `revokeAllForUser` (reuse detection) | M2 | D2.6 integration test with N=8 parallel requests; asserts unique winner |
| Refresh token replayed after rotation | 401 + `revokeAllForUser`; user must re-authenticate; security event audited | M2 / M3 | D3.9 Playwright + D2.6 integration |
| Refresh token present but signing key rotated | New tokens use new `kid`; old tokens valid for 15-minute overlap window; verify resolves correct key via JWKS endpoint | M2 | D2.4 rotation drill in staging |
| Access token issued by old key after rotation completes | Validates until expiry (≤15 min) via overlap window; revocation list still honored | M2 | D2.4 drill timeline |
| `alg: none` token submitted | Rejected by JwtService allowlist of acceptable algorithms (RS256 only) | M2 | Unit test asserting alg confusion guard |
| Token with manipulated `aud` claim | Rejected | M2 | Unit test |

### 13.2 Session-Invalidation Races

| Case | Behavior | Owner | Proof |
|------|----------|-------|-------|
| User changes password while a separate session is mid-request | Mid-flight request completes with old access token (≤15 min) but next refresh fails; all refresh tokens for user are revoked atomically with the password update | M4 | D4.3 single-transaction test |
| Admin emergency-revokes user while user is refreshing | Refresh returns 401; user re-authenticates; audit event recorded | M2 / M5 | D2.6 + D5.2 |
| Logout from device A while device B is refreshing | Device A's refresh token revoked; device B's untouched (multi-device per PRD error matrix row 6) | M3 | D3.4 + D3.9 |
| Reset confirm fires while old refresh token is being used | Both succeed or both fail (transactional); never half-state | M4 | D4.3 |

### 13.3 Password Reset Token Edge Cases

| Case | Behavior | Owner | Proof |
|------|----------|-------|-------|
| Reset token used twice (e.g., user clicks link twice quickly) | First call returns 200 + invalidates sessions; second call returns 410 Gone | M4 | D4.7 |
| Reset token expired (>1 h since issuance) | 410 Gone with option to request new link | M4 | D4.7 |
| Reset token for an unregistered email | No token issued; no email sent; 202 returned to caller (anti-enumeration) | M4 | D4.2 |
| User requests N reset emails in quick succession | Rate-limited at 3 per email per hour; counter keyed `auth:reset:<emailhash>:<hour>` | M4 | D4.5 rate-limit test |
| Reset link copied with token in browser history | Token still single-use; once consumed, link is dead | M4 | D4.4 |
| Reset email delivered to spam | Out of scope for engineering; mitigated by SPF/DKIM/DMARC + delivery monitoring | platform-team | D5.4 metric |

### 13.4 Rate-Limit Boundaries

| Case | Behavior | Owner | Proof |
|------|----------|-------|-------|
| Exactly 10 login requests in 60 seconds from one IP | All 10 succeed (assuming valid creds); 11th returns 429 | M3 | D3.6 boundary test |
| 11th request arrives at second 61 (window slide) | Succeeds because oldest entry rolled off | M3 | D3.6 sliding-window unit test |
| Rate limit hit during legitimate burst (e.g., load test, CI smoke) | 429 with `Retry-After` header in seconds | M3 | D3.6 + D6.1 |
| Rate-limit counter Redis key evicted unexpectedly | Counter resets to 0 (fail-open); compensating control = WAF rate limit upstream | M3 / M6 | D2.1 noeviction policy + WAF check in D6.4 |
| Per-IP limit defeated by NAT | Mitigated by per-user limit on authenticated endpoints; for login (pre-auth), lockout per email is the secondary control | M3 | D3.6 + D3.7 |

### 13.5 Empty / Malformed / Oversized Inputs

| Case | Behavior | Owner | Proof |
|------|----------|-------|-------|
| Empty request body on `/auth/login` | 400 with schema-validation error | M3 | D3.9 |
| Body > 4 KB on any auth endpoint | 413 Payload Too Large | M3 | D3.9 |
| Email with whitespace, unicode confusables, or mixed case | Normalized (NFC + lowercase + trim); uniqueness compared on normalized form | M3 | D3.2 unit test with i18n fixtures |
| Password containing null bytes | Accepted (bcrypt handles up to 72 bytes; we truncate explicitly at 64 chars input and document the limit) | M3 | D3.5 unit test |
| Display name with HTML / script content | Stored as-is (server is not the XSS guard for rendering); frontend escapes on render | M3 | D3.2 + frontend unit test |
| JSON with extra unexpected fields | Accepted (lenient parse) but extra fields are dropped, not echoed back | M3 | D1.4 OpenAPI `additionalProperties: false` mode discussed in ADR |
| Malformed JSON | 400 with parse-error code | M3 | D3.9 |

### 13.6 Partial Failures

| Case | Behavior | Owner | Proof |
|------|----------|-------|-------|
| Postgres up, Redis down at login time | Login still succeeds; refresh token issuance returns 503 with retry-after (or, alternative path: synchronous access token only, no refresh — decision in ADR-006 TBD before M3 exit) | M3 | ADR-006 decision + D2.6 |
| Postgres up, Redis down at refresh time | 503 with retry-after; user keeps using access token until expiry | M2 / M3 | D2.6 |
| Postgres down at login | 503 with retry-after; lockout counters in Redis preserved for resumption | M3 | D2.6 |
| Audit-log write fails | Outbox row written in same transaction; async drain catches up; alert fires if backlog > 1000 events for 5 min | M5 | D5.2 |
| SendGrid 5xx on reset request | Job retries 3× with exponential backoff; on terminal failure, alert fires and admin can manual-reissue | M4 | D4.5 |
| KMS unavailable at token-sign time | Local key cache (5-min lifetime) serves until refresh; if cache also empty, 503 + alert; readiness probe drops node from LB | M2 | D2.3 + R-DEP-1 mitigation |

### 13.7 Concurrent State Edge Cases

| Case | Behavior | Owner | Proof |
|------|----------|-------|-------|
| Two registrations submitting the same email simultaneously | Postgres UNIQUE constraint causes one to 409 Conflict; the other 201 Created | M3 | D3.2 integration test |
| User locks out themselves mid-reset (5 failed logins, then completes reset) | Reset completion clears lockout counter for that user (documented behavior) | M3 / M4 | D3.7 + D4.3 |
| User updates password to current password | Accepted in v1.0 (no history check); v1.1 introduces history check (parking lot) | M4 | Assumption #14 |

---

## 14. Notes on the Variant

This variant uses a six-milestone, foundation-first sequencing. Alternatives considered and rejected:

- **Four-milestone "verticals"** (each milestone = full vertical slice from API to UI): rejected because it forces the JWT crypto surface (high security risk) to be reviewed inside whichever first vertical needs auth, mixing concerns.
- **Eight-milestone "atomic" plan** (one milestone per endpoint plus one per supporting library): rejected as over-segmented for a team of 6; coordination cost exceeds parallelism gain.
- **Compressed five-sprint MVP** (skip M5 audit + M6 hardening): rejected because SOC2 audit in Q3 makes M5 deliverables blocking, and skipping M6 forfeits both the load test and pen test which are necessary for GA-grade authentication.

The chosen plan accepts the cost of one extra milestone (M2 as a separate library milestone) in exchange for isolating cryptographic concerns for review and benchmarking. This is judged the correct trade for an authentication service.
