<!--
Provenance:
  Base variant:   variant-1-opus-default.md (V1, opus default)
  Incorporating: variant-2-sonnet-default.md (V2, sonnet default), Section refs noted per-change
  Invariant probe: invariant-probe.md (Round 2.5) — INV-001, INV-002, INV-017, INV-019 resolved
  Changes applied: 14 of 14 per refactor-plan.md
  Merge timestamp: 2026-05-22T20:30Z
  Executor: merge-executor (opus)
-->

# Roadmap: User Authentication System

<!-- Source: Base (original) — Executive Summary -->
## Executive Summary

This roadmap delivers a production-grade user authentication system featuring OAuth2 (Google, GitHub), JWT-based session management with refresh tokens, role-based access control (RBAC), two-factor authentication, and comprehensive audit logging. The system is engineered to support 10,000 concurrent sessions at sub-200ms p95 latency while meeting OWASP Top 10 and GDPR compliance standards. Delivery spans 7 milestones over 22 weeks (20-21 weeks on the critical path; 22-23 weeks with merged scope from Changes #11/#12), sequenced to land core auth primitives first and layer advanced features (OAuth, 2FA, admin tooling) on a hardened foundation.

<!-- Source: Base (original) — Goals & Success Metrics -->
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

<!-- Source: Base (modified) — Change #4 from V2 D6.8 adds pgcrypto column-encryption to D1.2 -->
### M1 — Foundation & Infrastructure (Weeks 1-2)

**Goal**: Stand up the runtime, data layer, and CI/CD scaffolding the auth service will run on.

**Deliverables**:

- D1.1: Dockerized service skeleton (Node.js 20 LTS or Python 3.12, team choice ratified in Open Questions) with multi-stage build, health endpoint `/healthz`
- D1.2: PostgreSQL 15 schema migrations (Flyway/Alembic) for `users`, `roles`, `permissions`, `user_roles`, `audit_events`, `refresh_tokens`, `oauth_identities`, `password_resets`, `mfa_secrets`. **PII column-level encryption via `pgcrypto`**: `users.email` stored in encrypted column (defense-in-depth beyond RDS at-rest encryption); a deterministic-encryption search-hash column is added to preserve indexed lookups for login. NFR-006 compliance verification extended to require column-level (not just disk-level) PII encryption. <!-- Change #4: V2 D6.8 pgcrypto incorporated into D1.2 -->
- D1.3: Redis 7 cluster provisioned with TLS, AUTH enabled; namespaces `sess:`, `rl:`, `lock:`, `verify:` documented
- D1.4: CI/CD pipeline (GitHub Actions) running lint, unit tests, container scan (Trivy), and ephemeral preview deploys
- D1.5: Secrets management via Vault/AWS Secrets Manager; no secrets in env files committed
- D1.6: Observability baseline: structured JSON logs, OpenTelemetry traces, Prometheus metrics endpoint

**Mapped IDs**: NFR-005, NFR-006 (encryption at rest config + pgcrypto column-level), Dependencies (PostgreSQL 15+, Redis, Docker)

**Entry Criteria**: Cloud accounts provisioned, repo access granted, architecture decision record (ADR) for language/framework merged.

**Exit Criteria**: `docker compose up` brings the stack up locally; preview deploy passes smoke test; migrations apply cleanly on empty DB; pgcrypto extension installed and column-encryption verified on `users.email`.

**Estimated Duration**: 2 weeks

---

<!-- Source: Base (original) — M2 unchanged -->
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

<!-- Source: Base (modified) — Change #1 adds D3.7 per-user session cap (V2 D2.5); Change #3 modifies D3.1 with Redis WATCH/MULTI/EXEC (V2 D7.1/R-008); Change #6 modifies D3.6 load-test pattern (V2 D6.6) -->
### M3 — Session Management & Rate Limiting (Weeks 6-7)

**Goal**: Make sessions resilient, revocable, and protected against brute-force and credential-stuffing attacks.

**Deliverables**:

- D3.1: `POST /auth/refresh` with token rotation (one-time-use refresh tokens, family tracking for reuse detection → invalidates entire family). **Atomicity primitive**: Redis `WATCH/MULTI/EXEC` transaction wraps the invalidate-old + issue-new pair so concurrent refresh from the same client cannot produce two valid descendants of the same parent token. Family-tracking remains the defense-in-depth layer that detects reuse across the WATCH boundary. <!-- Change #3: V2 D7.1 + R-008 atomicity primitive incorporated -->
- D3.2: `POST /auth/logout` (single session) and `POST /auth/logout-all` (revoke all refresh tokens for user)
- D3.3: Per-user + per-IP rate limiting via Redis sliding window: 5 login attempts / 15 min per (IP, email), 100 req/min per authenticated user on sensitive endpoints
- D3.4: Account lockout: 10 failed attempts → 30-min lockout, exponential backoff on subsequent rounds; unlock via email link
- D3.5: Session store keyed by `jti`; `GET /auth/sessions` lists active sessions with device/IP metadata; `DELETE /auth/sessions/:id` revokes
- D3.6: Load test scenario: **ramp to 10,000 concurrent sessions over 10 minutes, sustain for 30 minutes** (k6 / Locust); assertions retained from V1 (p95 < 200ms) with V2's p99 < 200ms added as stretch criterion; verifies NFR-002. <!-- Change #6: V2 D6.6 ramp+sustain pattern incorporated -->
- D3.7: **Per-user concurrent session cap** (configurable, default = 5). Sixth login triggers oldest-session eviction; eviction emits an `auth.session.evicted` audit event (links into D6.4 taxonomy). Eviction kills only the leaf refresh token, NOT the family — family-tracking still detects reuse on the evicted token if replayed. <!-- Change #1: V2 D2.5 per-user session cap added as new deliverable -->

**Mapped IDs**: FR-006, FR-008, NFR-002, R-002

**Entry Criteria**: M2 exit; Redis cluster benchmarked at ≥50K ops/sec.

**Exit Criteria**: 10K concurrent session soak test passes (<1% error, p95 < 200ms); refresh-token reuse triggers family invalidation in pen-test scenario; **explicit concurrent-refresh race test passes** (two simultaneous refresh requests for the same parent produce exactly one valid descendant via WATCH/MULTI/EXEC); session-cap eviction verified at N=5→N=6 boundary.

**Estimated Duration**: 2 weeks

**Edge Cases Covered**: Clock-skew between API nodes for rate-limit windows (Redis as authoritative clock); legitimate refresh after near-expiry; concurrent refresh from same client (now resolved atomically via D3.1 WATCH/MULTI/EXEC); session-cap N=0 first-login (eviction skipped) and N=5→N=6 boundary (oldest evicted).

---

<!-- Source: Base (modified) — Change #14 adds D4.7 OAuth callback two-cookie pattern (INV-002 fix) -->
### M4 — OAuth2 Providers & Account Linking (Weeks 8-10)

**Goal**: Enable Google and GitHub sign-in with safe account linking and an email/password fallback.

**Deliverables**:

- D4.1: OAuth2 Authorization Code + PKCE flow for Google (`openid email profile` scopes) at `GET /auth/oauth/google/start` and `/callback`
- D4.2: Same flow for GitHub (`read:user user:email` scopes)
- D4.3: `oauth_identities` table linking `(provider, provider_user_id)` → `users.id`; email-match auto-link with explicit user confirmation
- D4.4: Provider-down fallback: circuit breaker (Resilience4j/opossum) opens after 5 consecutive failures → UI surfaces email/password option with clear messaging
- D4.5: State parameter (CSRF) and nonce (replay protection) validated server-side; redirect_uri allowlist
- D4.6: `POST /auth/oauth/unlink` requiring password verification if it's the only identity, blocks otherwise
- D4.7: **OAuth-callback session re-attach design (two-cookie pattern)** — SameSite=Strict refresh cookies are NOT sent on top-level navigation initiated by a third-party OAuth provider, which would break the post-callback "link to existing logged-in account" flow. Resolution: the callback endpoint reads a short-lived (5-min) **SameSite=Lax `oauth_continuation` cookie** OR a server-side state-to-session-id mapping (Redis, 10-min TTL) to identify the originating session; the SameSite=Strict refresh cookie is set ONLY after the user returns to the app's first-party page. Documents the two-cookie pattern in the OAuth runbook and includes an explicit Safari + Firefox cross-browser test in the M4 exit criteria. <!-- Change #14: INV-002 resolved — SameSite=Strict + OAuth callback interaction -->

**Mapped IDs**: FR-003, R-003, NFR-003 (OAuth state/nonce mitigates OWASP A01/A07)

**Entry Criteria**: M2 exit; Google + GitHub OAuth apps registered, client secrets in Vault.

**Exit Criteria**: End-to-end test passes for both providers in staging; chaos test simulating provider 503 confirms fallback path; OWASP ASVS L2 OAuth checklist signed off; **two-cookie pattern verified on Safari + Firefox** (logged-in user can link Google account without losing session attribution at callback).

**Estimated Duration**: 3 weeks

---

<!-- Source: Base (modified) — Change #9 adds `unverified` as 5th seed role (V2 D4.1) -->
### M5 — RBAC & Two-Factor Authentication (Weeks 11-14)

**Goal**: Add authorization (roles/permissions) and step-up authentication (TOTP-based 2FA).

**Deliverables**:

- D5.1: Role model: `roles` (id, name, description), `permissions` (id, resource, action), `role_permissions`, `user_roles`; seed roles **`admin`, `user`, `auditor`, `support`, `unverified`** (5 total). The `unverified` role is the default capability tier assigned at registration before email verification completes; it carries permission to verify email and nothing else, removing the implicit verified-vs-unverified ambiguity in the prior `user` role. On successful email verification, the user is upgraded from `unverified` → `user`. <!-- Change #9: V2 D4.1 `unverified` role added as 5th seed role -->
- D5.2: Authorization middleware `requirePermission('users:write')` enforced on protected endpoints; permissions claim in JWT (scoped, ≤2KB to avoid header bloat — overflow falls back to server-side lookup with 30s cache)
- D5.3: `POST /auth/2fa/setup` issues TOTP secret + QR (RFC 6238, SHA-1, 30s window, 6 digits); `POST /auth/2fa/verify` confirms enrollment
- D5.4: Login flow extended: when 2FA enabled, `/auth/login` returns `mfa_required: true` + short-lived (5-min) MFA challenge token; `POST /auth/2fa/challenge` exchanges challenge + TOTP for full JWT
- D5.5: 10 single-use recovery codes generated at enrollment, hashed (Argon2id) and stored; `POST /auth/2fa/recovery` accepts a code, consumes it, prompts re-enrollment
- D5.6: Admin role-assignment APIs `POST /admin/users/:id/roles` (audited)

**Mapped IDs**: FR-004, FR-007, NFR-003 (broken access control mitigation)

**Entry Criteria**: M3 exit; design review of permission taxonomy approved by product + security.

**Exit Criteria**: Authorization integration tests cover positive + negative paths for every seeded role (5 roles, including `unverified`); 2FA enrollment, login challenge, and recovery flows pass; recovery codes single-use enforced.

**Estimated Duration**: 4 weeks

**Edge Cases Covered**: User with no roles (deny-by-default); `unverified` user attempts privileged action (denied with 403 + verification prompt); revoking a role mid-session (server-side check, JWT short TTL bounds staleness ≤15 min); 2FA secret leaked → recovery + force re-enroll runbook; clock-drift on TOTP (±1 window tolerance).

---

<!-- Source: Base (modified) — Change #7 modifies D6.6 deactivation lifecycle (V2 D5.6/D5.7); Change #11 expands D6.5 with hash-chain genesis/canonicalization/tip-publication (INV-001 fix); Change #12 adds D6.4.a outbox pattern (INV-017 fix) -->
### M6 — Password Reset, Profile, Audit Logging (Weeks 15-17)

**Goal**: Round out user-facing flows and stand up the immutable audit trail required for compliance.

**Deliverables**:

- D6.1: `POST /auth/password/forgot` issues signed reset token (HS256, 1h TTL, single-use, hashed in `password_resets`) and emails via SendGrid; constant-time response regardless of email existence
- D6.2: `POST /auth/password/reset` verifies token, applies new password (zxcvbn + history check, last 5), invalidates all refresh tokens
- D6.3: Profile endpoints: `GET /me`, `PATCH /me` (name, avatar URL, locale, timezone), `POST /me/email/change` (re-verification required)
- D6.4: Audit event taxonomy: `auth.login.success|failure`, `auth.logout`, `auth.password.reset.requested|completed`, `auth.2fa.enabled|disabled`, `auth.oauth.linked|unlinked`, `rbac.role.assigned|revoked`, `account.deactivated|reactivated`, `auth.session.evicted` (from D3.7 cap-eviction)
- **D6.4.a: Audit outbox pattern (resolves FR-009 100%-capture vs NFR-001 p99-latency conflict)** — Auth handlers write the audit event to an `audit_outbox` table inside the SAME database transaction as the state change (atomic with the auth action; satisfies FR-009 at-least-once). A durable worker (Postgres LISTEN/NOTIFY or scheduled poller) drains the outbox to the immutable `audit_events` table and the hash-chain writer (D6.5). Latency budget: outbox INSERT < 10ms p99 inside the request transaction; hash-chain materialization happens asynchronously without blocking the response. This satisfies FR-009's "100% capture" without paying the synchronous hash-chain serialization cost on the request path. <!-- Change #12: INV-017 resolved — outbox pattern for at-least-once audit write -->
- D6.5: Audit sink: append-only table `audit_events` with hash-chain (each row contains SHA-256 of prior row's canonicalized payload) for tamper-evidence; daily export to S3 with object-lock. Expanded into three sub-deliverables to make the tamper-evidence claim externally verifiable:
  - **D6.5.a: Genesis row** — the first row of the chain is a deterministic, well-known genesis record with a fixed payload (e.g., `{"type":"genesis","schema_version":"1","epoch":"2026-01-01T00:00:00Z"}`) and `prev_hash` = `SHA-256("")` (the empty string hash). Genesis is inserted by a one-time migration at M6 deploy time; subsequent rows cannot be re-forged top-to-bottom because the genesis hash is committed to source control AND to the first daily S3 export. <!-- Change #11.a: INV-001 genesis anchoring -->
  - **D6.5.b: Canonicalization spec** — payload canonicalization uses **JSON Canonicalization Scheme (JCS, RFC 8785)** over the row's stable fields (`event_type`, `actor_user_id` (tokenized — see D7.3), `target_user_id` (tokenized), `created_at` (ISO-8601 UTC), `metadata` (JCS-canonicalized JSONB), `prev_hash`). Postgres JSONB does not preserve key order, so the canonicalization layer sorts keys lexicographically before hashing. Specification published in the runbook (D7.7). A single-writer advisory lock (`pg_advisory_xact_lock`) serializes hash-chain materialization to guarantee total ordering across multi-pod writers. <!-- Change #11.b: INV-001 canonicalization + INV-007 serialization -->
  - **D6.5.c: Daily Merkle tip publication** — at end-of-day, a worker computes the Merkle root over all rows appended that day, publishes (i) the day's tip hash + Merkle root to a separate S3 bucket with Object Lock, and (ii) optionally pushes the tip to a public tip-feed (e.g., a notarization service or a public Git repo of daily tips) for external verifiability. Verifiers can independently confirm the chain has not been retroactively rewritten by checking the published tip against the recomputed Merkle root. <!-- Change #11.c: INV-001 tip publication for external verifiability -->
- D6.6: GDPR endpoints: `GET /me/export` (JSON dump within 30 days, async job), `DELETE /me` (soft-delete + 30-day grace, then crypto-shred). **Explicit `deactivated_at` lifecycle**: setting `users.deactivated_at = NOW()` immediately filters the account out of login queries (login lookup `WHERE deactivated_at IS NULL`); during the 30-day grace, a cancel-link email allows reactivation. At t=+30 days, hard-delete removes PII from `users` row (crypto-shred per D7.3) while anonymized audit records survive via tokenized user_id (R-010). `DELETE /me` requires **re-authentication (current password OR active 2FA)** as a confirmation step; export is async (large datasets) but deletion request is synchronous-confirmed. <!-- Change #7: V2 D5.6 + D5.7 explicit lifecycle + re-auth requirement -->

**Mapped IDs**: FR-005, FR-009, FR-010, FR-012, NFR-004, NFR-006, R-004

**Entry Criteria**: M5 exit; DPO/legal review of audit retention and GDPR endpoints scheduled.

**Exit Criteria**: All audit event types verified emitted in integration tests; hash-chain tamper test passes (modifying any row's payload after the fact fails verification against the daily Merkle tip); outbox at-least-once verified by process-crash injection between transaction commit and worker drain (event still materializes); export job completes for synthetic user with 10K events in <60s; `deactivated_at` filter prevents login within 1 second of deactivation; re-auth required on `DELETE /me` verified.

**Estimated Duration**: 3-4 weeks (3.5 if Change #11 hash-chain sub-deliverables track to plan)

---

<!-- Source: Base (modified) — Change #2 restructures D7.6 K8s/HPA/PgBouncer/Sentinel + multi-AZ chaos test (V2 D7.4); Change #5 adds D7.9 Prometheus/Grafana alerts (V2 D7.2); Change #8 adds D7.10 edge-case validation suite (V2 D7.1) -->
### M7 — Admin Dashboard, Hardening, Launch Readiness (Weeks 18-22)

**Goal**: Operational tooling, security hardening, and production launch gate.

**Deliverables**:

- D7.1: Admin dashboard (React + Vite) with user list, search, view profile, force-logout, reset-password, assign/revoke roles, view audit trail per user, deactivate/reactivate
- D7.2: Admin dashboard authz: `admin` role required, all actions audited with actor + target + before/after diff
- D7.3: Account deactivation workflow: user-initiated (D6.6) and admin-initiated (D7.1); 30-day grace with cancel-link email; crypto-shred PII at grace expiry while preserving audit references via tokenized user_id. **User_id tokenization happens AT deactivation (t=0)** on audit `actor_user_id` / `target_user_id` columns, NOT at crypto-shred time, so the audit table cannot be queried by the deleted user's original UUID at any point after deactivation (per INV-012 boundary fix).
- D7.4: Security hardening pass: CSP (no `unsafe-inline`, no `unsafe-eval`), HSTS (`max-age=31536000; preload`), X-Frame-Options DENY, secure cookies with restrictive `Domain` attribute (no subdomain leakage), dependency audit (Snyk), OWASP ZAP baseline scan → zero High/Critical
- D7.5: Third-party penetration test engagement; findings remediated to Medium-or-lower before launch
- D7.6: **Production deploy: multi-AZ + Kubernetes topology (combined)** — RDS multi-AZ + Redis replication group (V1 multi-AZ baseline required for NFR-005). **Kubernetes manifests** (Deployment, Service, ConfigMap, Secret); **horizontal pod autoscaler** (min 3 replicas, max 10, CPU 70% target — pre-warmed on schedule to absorb top-of-hour bursts per INV-018 mitigation); **PgBouncer** transaction-pool with documented connection cap aligned to PG `max_connections`; **Redis Sentinel** for HA. Production load test re-runs D3.6's ramp+sustain pattern in prod-like topology. Chaos test killing one AZ confirms <30s RTO; the K8s+PgBouncer+Sentinel triad provides the orchestration substrate but the multi-AZ chaos test remains the authoritative NFR-005 verification. <!-- Change #2: V2 D7.4 K8s+HPA+PgBouncer+Sentinel combined with V1's multi-AZ+chaos baseline -->
- D7.7: Runbooks: key rotation, OAuth client rotation, incident response (suspected breach), 2FA recovery override, GDPR request handling, **hash-chain canonicalization spec (D6.5.b)** + **daily tip-publication and external-verification procedure (D6.5.c)**
- D7.8: Launch readiness review: capacity plan signed off, SLO dashboards live, on-call rota staffed, GDPR DPIA signed (including legal sign-off on the S3-Object-Lock + GDPR-erasure reconciliation per R-010 mitigation)
- **D7.9: Monitoring & alerting thresholds** — Prometheus metrics for request latency (p50/p95/p99), error rate, active sessions, rate-limit rejections, failed-login attempts, audit-outbox lag, hash-chain materialization lag. Grafana dashboards for auth service health. Alerts fire on: **error rate > 1%, p99 latency > 300ms, audit-event-write failures (any), audit-outbox lag > 60s, active sessions approaching Redis capacity, JWKS endpoint 5xx > 0.1%**. Supports NFR-005 99.9% uptime detection. <!-- Change #5: V2 D7.2 Prometheus/Grafana thresholds added -->
- **D7.10: Edge-case validation test suite (final integration gate)** — centralized regression suite that exercises cross-cutting boundary conditions: empty database (first user registration), single-user system (admin creates own account), max-load (10K sessions + audit writes simultaneously per outbox D6.4.a), token expiry at exact boundary, refresh-token reuse race (two simultaneous refresh requests against D3.1 WATCH/MULTI/EXEC), OAuth callback with malformed `state` parameter, rate-limit at exact threshold boundary (5th vs 6th attempt), session-cap N=5→N=6 eviction race, hash-chain genesis row presence and Merkle-tip recomputation. ADDITIVE to V1's per-milestone "Edge Cases Covered" blocks (those remain authoritative for per-milestone exit criteria); D7.10 is the final integration-level gate. <!-- Change #8: V2 D7.1 centralized edge-case suite added as final gate -->

**Mapped IDs**: FR-011, FR-012, NFR-003, NFR-004, NFR-005, R-001, R-002, R-004

**Entry Criteria**: M6 exit; pen-test vendor engaged; SRE on-call rota proposed.

**Exit Criteria**: All NFRs verified in staging matching production topology; go/no-go meeting approves launch; rollback plan rehearsed; D7.10 edge-case suite passes 100%; alert thresholds D7.9 verified by fault-injection (each alert fires within 60s of trigger condition).

**Estimated Duration**: 5 weeks

---

<!-- Source: Base (modified) — Critical Path updated to reflect merged scope per refactor-plan Schedule Disclosure -->
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

**Critical Path**: M1 → M2 → M3 → M5 → M6 → M7 — **20-21 weeks baseline; 22-23 weeks with merged scope** (Change #11 hash-chain sub-deliverables D6.5.a/b/c add 0.5-1 week to M6; Change #2 K8s topology adds operational complexity within the existing M7 envelope). M4 runs parallel to M3 starting Week 8 but must complete before M5 finishes since OAuth-issued sessions need RBAC.

**Explicit Blockers**:

- D5.2 (authz middleware) blocks D7.1 (admin dashboard) — admin role enforcement
- D3.1 (refresh rotation) blocks D6.2 (password reset invalidating tokens)
- D6.4 (audit taxonomy) blocks D7.1 (admin actions must emit audit events)
- D6.4.a (outbox pattern) blocks D6.5 hash-chain materialization
- D6.5.b (canonicalization spec) blocks D6.5.c (Merkle tip publication)
- D4.1/D4.2 (OAuth flows) block D5.4 (2FA challenge must integrate with OAuth-initiated sessions)
- D4.7 (two-cookie pattern) blocks D4.3 (account linking requires session attribution at callback)
- D1.2 (schema, including pgcrypto + search-hash) blocks every later DB-touching deliverable
- D3.7 (session cap) depends on D3.1 (family-tracking semantics) for eviction-leaf interaction

<!-- Source: Base (modified) — Change #13 modifies R-010 Mitigation column (INV-019 fix) -->
## Risk Register

| ID | Risk | Impact | Probability | Mitigation | Milestone(s) |
|----|------|--------|------------|------------|--------------|
| R-001 | Token theft via XSS | High | Medium | HTTP-only + Secure + SameSite=Strict cookies for refresh token (D2.5); CSP header without `unsafe-inline` and without `unsafe-eval` (D7.4); restrictive cookie `Domain` attribute (D7.4); access token kept in memory (not localStorage) per frontend integration guide | M2, M7 |
| R-002 | Brute force / credential stuffing | High | High | Sliding-window rate limiting (D3.3); progressive account lockout (D3.4); CAPTCHA on Nth attempt (D3.4 stretch); breached-password check against HIBP k-anonymity API at registration + reset (D2.1, D6.2); per-user session cap (D3.7) bounds harvest size | M3, M6 |
| R-003 | OAuth provider downtime | Medium | Low | Circuit breaker with email/password fallback path (D4.4); status-page monitor; provider health surfaced in UI | M4 |
| R-004 | Data breach of PII | Critical | Low | AES-256 at rest (RDS encryption, D1.2); pgcrypto column-level encryption for `users.email` (D1.2); TLS 1.3 in transit; least-privilege IAM; audit-trail on PII access; crypto-shred on deletion (D7.3); pen-test (D7.5) | M1, M6, M7 |
| R-005 (new) | JWT signing key compromise | Critical | Low | RS256 with key in Vault; quarterly rotation runbook (D7.7); JWKS `kid` header allows zero-downtime rotation; short access-token TTL (15min) bounds blast radius | M2, M7 |
| R-006 (new) | SendGrid outage blocks verification + reset | Medium | Medium | Secondary SMTP provider (SES) configured as failover; verification token reissue endpoint; document degraded-mode SLA in runbook | M2, M6 |
| R-007 (new) | RBAC misconfiguration → privilege escalation | High | Medium | Deny-by-default middleware; permission matrix peer-reviewed (D5.1); negative-path integration tests (D5.6 exit); admin role assignments audited (D5.6); explicit `unverified` role gates privileged actions pre-verification | M5 |
| R-008 (new) | 2FA recovery-code abuse | High | Low | Argon2id-hashed codes, single-use, count surfaced to user, force re-enroll after any use; alert email on recovery use | M5 |
| R-009 (new) | Audit-log tampering by privileged insider | High | Low | Hash-chained rows with deterministic genesis (D6.5.a), JCS canonicalization (D6.5.b), and daily Merkle tip publication for external verifiability (D6.5.c); daily S3 export with object-lock; advisory-lock serialized writer; separation of duties — admins cannot delete audit rows via app | M6 |
| R-010 (new) | GDPR erasure conflicts with audit retention | Medium | Medium | **S3 Object Lock applies ONLY to anonymized/tokenized audit records (post-D7.3 user-id tokenization); PII never enters the immutable export — only references via tokenized user_id; PII fields remain in the live PG `audit_events` table (and the live `users` row) where crypto-shred at t=+30 days can act; the immutable S3 export contains only the hash chain + canonicalized payload over PII-free / tokenized fields. The metadata JSONB field is whitelisted-only at write time (no raw IP/UA/email in immutable export — those stay in live PG). Legal sign-off captured in D7.8.** | M6, M7 |
| R-011 (new) | Refresh-token theft (offline) | High | Low | Refresh tokens stored hashed (SHA-256), one-time-use with family-reuse detection (D3.1) auto-invalidates family + alerts user; WATCH/MULTI/EXEC atomicity prevents concurrent-refresh race | M3 |
| R-012 (new) | Time-of-check/time-of-use on role revocation | Medium | Medium | Access-token TTL ≤15min bounds staleness; admin force-logout (D7.1) invalidates refresh-token family immediately | M5, M7 |

<!-- Source: Base (modified) — Change #10 modifies Open Question #1 with default-if-no-decision (V2 D1.3) -->
## Open Questions

1. **Language/framework**: Node.js/Express vs Python/FastAPI vs Go/Gin? Affects D1.1, library choices for Argon2/JWT/OAuth. Decision needed before M1 kickoff. **Default if no decision by Week 0: Python 3.12 + FastAPI (per V2 baseline tech stack); change requires a Week 1 ADR refresh and may slip M1 entry by 2-3 days for environment retooling.**
2. **Tenancy model**: Single-tenant or multi-tenant from day one? Schema in D1.2 needs `organization_id` if multi-tenant — retrofitting is expensive.
3. **JWT claims contract**: Final list of claims (`sub`, `email`, `roles[]`, `permissions[]` or `scope`, `mfa_verified`, `tenant_id`?) — needed by Week 3 (D2.3).
4. **Password policy**: Min length, max length, special-char requirement, zxcvbn score threshold? NIST SP 800-63B suggests min 8, no composition rules — confirm with security.
5. **Audit retention**: How long are audit events retained (12mo? 7yr for SOX-adjacent?) — affects D6.5 storage sizing and GDPR balancing. Must align with R-010 mitigation (S3 Object Lock retention period must be coherent with crypto-shred timing for non-tokenized references; see R-010).
6. **OAuth account linking policy**: Auto-link on matching verified email, or always require explicit user action? Affects D4.3 UX and security posture.
7. **2FA enforcement**: Optional for all users, required for `admin` role, required for all users? Affects D5.3 and admin onboarding flow.
8. **Email deliverability**: Dedicated IP on SendGrid vs shared? SPF/DKIM/DMARC owner? Affects verification + reset reliability (R-006).
9. **Rate-limit tuning**: Are the proposed thresholds (5 logins / 15min) acceptable for legitimate shared-IP users (corporate NATs, mobile carriers)? May need per-account + per-IP composite scoring.
10. **Admin dashboard hosting**: Same domain as API (cookie sharing) or separate subdomain (CORS + cookie scope decisions)? Affects D7.1 and security review.
11. **GDPR data-residency**: EU-only data residency required? Affects RDS region and possibly architecture.
12. **Out-of-band password reset throttling**: Max reset requests per email per day to limit email bombing — needs threshold (suggest 3/day).

<!-- Source: Base (original) — Out of Scope unchanged -->
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

<!-- Source: Base (original) — Success Criteria unchanged -->
## Success Criteria

| Spec Criterion | Satisfying Milestone(s) | Evidence |
|----------------|-------------------------|----------|
| All FR requirements implemented and tested | M2 (FR-001, FR-002), M3 (FR-006, FR-008), M4 (FR-003), M5 (FR-004, FR-007), M6 (FR-005, FR-009, FR-010, FR-012), M7 (FR-011, FR-012) | Test report aggregated at D7.8 gate |
| OWASP compliance verified via security scan | M7 (D7.4 ZAP + Snyk, D7.5 pen-test) | Scan reports + remediation tracker |
| Load testing confirms 10K concurrent sessions | M3 (D3.6) re-verified at M7 (D7.6) in prod-like topology | k6 report archived |
| OAuth2 flow works for Google and GitHub | M4 (D4.1, D4.2) | E2E test recordings + staging demo |
| Audit logs capture all auth events | M6 (D6.4, D6.4.a outbox, D6.5 hash-chain) verified by M7 admin dashboard cross-check | Audit-event coverage matrix + outbox at-least-once injection test |

**Launch Gate (D7.8)**: All five rows above show green; pen-test residual risks ≤ Medium; SLO dashboards green for 7 consecutive days in staging soak; D7.10 edge-case suite passes 100%; D7.9 alert thresholds verified by fault-injection.
