<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (opus, default persona) -->
<!-- Non-base source for grafted strengths: Variant 2 (sonnet, default persona) -->
<!-- Merge date: 2026-05-22 -->
<!-- Refactor plan: adversarial/refactor-plan.md (16 RCs across Tier 1/2/3) -->

# Roadmap: User Authentication System (Merged — sc:adversarial Mode B opus+sonnet, 2026-05-22)

<!-- Source: Base (original, modified) — RC-006: rewrite philosophy to remove "2FA precedes OAuth" claim and align with M1-M5 sequencing -->

## Architectural Philosophy

This roadmap is constructed on three load-bearing principles:

1. **Security as a first-class layer, not a cross-cutting afterthought.** Cryptographic primitives, secrets management, and threat models are established in M0/M1 — before a single user record is written. OWASP/GDPR posture is "shifted left" into the schema and middleware, not retrofitted.
2. **Strict layering with thin contracts at each boundary.** Database (PostgreSQL 15) → Domain services (Python/Node) → HTTP API (REST + OpenAPI 3.1) → UI (admin dashboard). Each layer has its own test pyramid; no layer reaches across a boundary.
3. **Observability and operability are non-negotiable for the NFR-005 99.9% target.** SLOs, dashboards, runbooks, and incident drills are M7 deliverables — not "nice-to-haves" deferred to after launch.

**Critical sequencing decision:** **Primary credential hardening (M1–M4: Argon2id, RS256, lockout, RBAC) precedes federation (M5: OAuth); 2FA at M6 layers step-up assurance on top of the hardened primary path.** OAuth2 (FR-003) is intentionally deferred to M5, after RBAC (M4), because OAuth claim → role mapping is otherwise undefined and creates an authorization vacuum. 2FA (FR-007) lands at M6 once the primary credential path is fully hardened — it is an additive control on top of M1–M4, not a prerequisite for OAuth federation.

---

<!-- Source: Variant 2 (sonnet, default), "Technology Decisions & Rationale" section (lines ~692-706) — merged per RC-011, adapted to V1 choices with RC-005 (tuned Argon2id) and RC-008 (per-user DEK) -->

## Technology Decisions & Rationale

This table captures the load-bearing technology choices and their explicit rationale. Where parameters differ from V2's source table, V1 architecture and the tuned values from invariant remediations (RC-005 Argon2id, RC-008 per-user DEK) take precedence.

| Decision | Choice | Rationale | Alternative Considered |
|----------|--------|-----------|------------------------|
| Password hashing | **Argon2id (m=32768, t=2, p=4)** — tuned per RC-005 / INV-006 to ~80ms p95 on target hardware | OWASP 2023 recommendation; resistant to GPU-based attacks; tuned to fit inside NFR-001 200ms p95 budget (hash 80ms + DB 60ms + JWT 20ms + network 40ms) | bcrypt (rejected — aging, no memory-hardness); scrypt (rejected — less ecosystem support); higher Argon2id parameters m=65536/t=3 (rejected — 250ms hash blows NFR-001 budget) |
| Password hashing pepper | HMAC pepper from Vault, applied pre-hash | Adds a secret layer beyond per-user salt; pepper rotation does not require re-hashing all users (HMAC layer can be rolled separately) | Pepper in DB or env var (rejected — defeats the purpose; same compromise surface as the hashes) |
| JWT algorithm | RS256 (RSA 2048-bit) | Asymmetric: auth service holds private key, all services verify with public key; enables key rotation via JWKS without redistributing secrets | HS256 (rejected — symmetric key shared with every verifier expands compromise blast radius); EdDSA (acceptable alternative; deferred to v2) |
| Refresh token storage | PostgreSQL (SHA-256 hashed) + Redis (fast lookup); per-device families per RC-004 | Hashed in DB for durability and reuse-detection; per-device family (`device_id`) eliminates the false-positive logout caused by legitimate concurrent device refresh | Single-family tokens (rejected — INV-005 false-positive); plaintext storage (rejected — DB compromise = total auth compromise) |
| Refresh token TTL | 30 days with reuse detection + per-device families | Reuse detection collapses effective theft window; per-device families (RC-004) eliminate false positives; UX trade-off accepted (less frequent re-auth) | 7 days (V2 default — kept as configurable downward; 30-day default favored for UX once RC-004 closes false-positive risk) |
| Session store | Redis 7 with AOF (`appendfsync everysec`) + RDB snapshots | Sub-millisecond reads for session validation; AOF ensures sessions survive Redis restart; canonical refresh-token state lives in DB so Redis loss degrades to "no new logins" not "auth down" | DB-only sessions (rejected — 10K concurrent NFR-002 latency overhead); memcached (rejected — no persistence) |
| PII encryption | **AES-256-GCM with KMS envelope encryption; per-user DEK** per RC-008 / INV-008 | Per-user DEK enables true per-user cryptographic erasure for GDPR Article 17 without destroying other users' PII; authenticated encryption prevents tampering | Column-level single DEK (rejected — INV-008: erasing one user destroys all PII); plaintext + disk encryption only (rejected — defense-in-depth requirement) |
| Rate limiting | Token-bucket in Redis (atomic Lua script); burst 2x for 10s | Atomic Lua script ensures consistency across N replicas; token-bucket allows controlled burst absorption; tiered limits per endpoint sensitivity | Sliding window sorted sets (V2 alternative; comparable correctness, slightly higher Redis memory) |
| 2FA | TOTP (RFC 6238); WebAuthn deferred to v2 | No SMS dependency (SIM swap, cost); works with all authenticator apps; offline-capable; recovery codes for account-loss scenarios | SMS OTP (rejected — SIM swap, deliverability); WebAuthn (deferred — adds enrollment complexity; planned post-launch) |
| Audit log storage | PostgreSQL append-only with monthly RANGE partitioning + Merkle hash chain (RC-009) + WORM S3 fan-out | Native SQL for compliance reporting; partition drops for retention with 90-day soft-delete grace (RC-009); Merkle root provides cryptographic tamper proof independent of DB ACLs | Append-only Kafka (rejected — adds operational surface); DB ACL-only (rejected — INV-014: detects nothing) |
| Audit retention | 7 years default (configurable downward) with 90-day soft-delete-before-drop grace | Covers SOX, HIPAA, PCI-DSS, FINRA; configurable downward for less-regulated tenants; soft-delete grace prevents irreversible loss on retention-policy mistakes | 2 years (V2 default — rejected as default; retroactive extension impossible after partition drop; available as configured value) |
| Email delivery | SendGrid with circuit breaker + Redis-backed retry queue (BullMQ/Celery) | Reliable transactional delivery; circuit breaker prevents cascade failures; retry queue absorbs short outages without user-visible failure | Provider-agnostic SMTP (rejected — operational overhead for deliverability, DKIM/SPF/DMARC); SES (acceptable alternative; SendGrid chosen for template management UX) |
| Deployment | Canary (1% → 10% → 50% → 100%) with automated rollback on error-budget burn | Lower blast radius than blue-green for auth-critical service; tied to SLO burn-rate alerts; canary failures auto-rollback before user impact | Blue-green (V2 alternative — instant cutover but no progressive validation; canary preferred for auth criticality) |
| Database migrations | Alembic (Python) or Prisma Migrate (Node) per ADR-004; forward-only with compensating migrations | Versioned, reversible-via-compensation migrations; CI integration; supports PostgreSQL partitions and UUID v7 | golang-migrate / Flyway (acceptable alternatives; framework choice per ADR-004) |

---

<!-- Source: Variant 2 (sonnet, default), "Blast Radius Analysis" section (lines ~710-720) — merged per RC-012, augmented with V1's per-user DEK as 7th invariant -->

## Blast Radius Analysis

Design choices that limit the impact of individual failures. These complement the M0 STRIDE threat model by documenting runtime failure containment. Each invariant has a tested failure mode that confirms the isolation property.

1. **Token storage isolation.** Refresh tokens live in a separate table (`refresh_tokens`) from user data (`users`). A SQL injection or compromise scoped to the token table cannot exfiltrate user PII; conversely a `users`-scoped breach does not yield refresh secrets.
2. **Redis as session cache, not session authority.** Sessions are validated against PostgreSQL on sensitive operations (password change, role change, deactivation). Redis failure degrades to slower DB lookups, not auth failure. Canonical refresh-token state lives in DB.
3. **OAuth identity linking is additive, never replacement.** Linking a Google or GitHub account does not replace email/password. If an OAuth provider is down, email/password still works (D-M5.5 circuit breaker + visible fallback banner).
4. **Audit log is append-only with cryptographic tamper-evidence.** The application user has no UPDATE/DELETE on `audit_events`. In addition, Merkle hash-chain anchoring (D-M6.4 with RC-009 scope) provides cryptographic proof of integrity that survives DBA-level tampering and backup-restore swaps — not just app-layer integrity.
5. **Rate limiter isolation.** If rate limiting fails open (Redis down), auth still works (degraded protection logged + paged). If it fails closed, users get 429s but the auth service stays up. Rate-limit logic does not share state with auth decision logic.
6. **KMS key separation.** Encryption keys live in KMS, never in the database. Full database access does not yield encryption keys. Key rotation does not require re-encrypting all data (envelope encryption pattern).
7. **Per-user DEK isolation** (added per RC-008 / INV-008). Each user's PII is encrypted with a unique DEK wrapped by the master KEK. GDPR Article 17 erasure destroys only the requesting user's wrapped DEK, rendering only that user's PII undecryptable. No cross-user blast radius from individual erasure requests.

---

<!-- Source: Base (original, modified) — RC-007: add "Effort" column for person-week estimates; RC-001/RC-002: add CSRF and password history deliverables surfaced in column; RC-008: per-user DEK reflected in M1 deliverable summary; RC-004: per-device refresh families reflected in M3 deliverable summary -->

## Milestone Summary Table

| ID | Milestone | Duration | Effort (person-weeks) | Depends On | Primary Deliverables | Risks Addressed |
|----|-----------|----------|------------------------|------------|----------------------|-----------------|
| M0 | Foundations & Threat Model | 2 weeks | 3 pw | — | Docker stack, secrets layer (Vault), ADRs, STRIDE threat model | R-001, R-004 (prep) |
| M1 | Data Layer & Crypto Primitives | 2 weeks | 4 pw | M0 | PostgreSQL schema, **per-user DEK** encryption-at-rest, Argon2id (m=32768/t=2/p=4) hashing | R-004 |
| M2 | Core Auth: Register + Login + JWT | 3 weeks | 6 pw | M1 | FR-001, FR-002, email verification, JWT issuer, **password history (last 5)** | R-001, R-002 |
| M3 | Sessions, Refresh Tokens & Password Reset | 2 weeks | 4 pw | M2 | FR-005, FR-006, Redis session store, **per-device refresh families with 30s grace** | R-001 |
| M4 | RBAC & Authorization | 2 weeks | 4 pw | M2 | FR-004, FR-010, FR-012, permission middleware | R-004 |
| M5 | OAuth2 (Google + GitHub) | 2 weeks | 3 pw | M4 | FR-003, **null-email handling** (synthetic placeholder), provider fallback | R-003 |
| M6 | 2FA, Rate Limiting, CSRF & Audit Logging | 3 weeks | 6 pw | M3, M4 | FR-007, FR-008, FR-009, **CSRF double-submit**, append-only Merkle-anchored audit | R-002, R-004 |
| M7 | Admin Dashboard & Operational Readiness | 3 weeks | 5 pw | M4, M6 | FR-011, dashboards, runbooks, SLOs | — |
| M8 | Verification: Load, Security, Compliance | 2 weeks | 4 pw | M7 | NFR-001 through NFR-006 verification | All |
| M9 | Production Cutover & Hardening | 1 week | 2 pw | M8 | Canary rollout, on-call rotation, post-launch review | — |

**Total estimated duration:** 22 weeks (with 2 weeks built-in slack); critical path = M0→M1→M2→M3→M6→M8→M9 (~17 weeks). Total effort: **~41 person-weeks** (illustrative — adjust to actual team composition; see "Week-by-Week Parallelization Schedule" below).

---

<!-- Source: Base (original) — M0 unchanged structurally; RC-016 deliverable table format applied; RC-015 (M0 definition-of-done checklist) per refactor-plan -->

## M0 — Foundations & Threat Model

**Duration:** 2 weeks
**Effort:** 3 person-weeks
**Goal:** Establish infrastructure, secrets, and security baseline *before* any auth code is written. This milestone exists because retrofitting secrets management and threat models after launch is an order of magnitude more expensive than doing it first.

### Deliverables

<!-- Source: Base (original, reformatted per RC-016 to deliverable-table format adopted from V2) -->

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M0.1 | Containerized development stack | `docker-compose.yml` brings up PostgreSQL 15.5, Redis 7.2, MailHog, and the auth service; multi-stage Dockerfiles with distroless `gcr.io/distroless/python3-debian12` base; non-root UID 10001; read-only root FS where possible; `docker compose up` healthy within 30s |
| D-M0.2 | Secrets management layer (Vault) | HashiCorp Vault dev mode locally; AWS Secrets Manager (or equivalent) reference architecture for staging/prod; zero secrets in env vars in production; sidecar injection pattern documented; JWT signing keys RS256 with rotation hooks stubbed (full rotation in M9) |
| D-M0.3 | Threat model document (STRIDE) | Per-asset analysis for credentials, tokens, sessions, PII; explicit mapping to R-001 (XSS/token theft), R-002 (brute force), R-004 (PII breach); counter-control catalog including HTTP-only + Secure + SameSite=Strict cookies, CSP `default-src 'self'`, HSTS `max-age=63072000`; reviewed by ≥2 engineers |
| D-M0.4 | ADRs (Architecture Decision Records) | ADR-001: Token strategy (short-lived JWT access + opaque refresh in HTTP-only cookie). ADR-002: Password hashing (Argon2id **m=32768, t=2, p=4** per RC-005 tuning). ADR-003: Schema-per-bounded-context vs shared (decision: shared schema, separate migrations namespace). ADR-004: Framework choice (FastAPI 0.115+ OR NestJS 10+) — pick one, document why |
| D-M0.5 | CI/CD skeleton | GitHub Actions: lint (ruff/eslint), type check (mypy strict / tsc strict), unit tests, SAST (Semgrep), dependency scan (Trivy); pre-commit hooks: detect-secrets, no-debugger, no-print-statements; green pipeline on empty `auth-service` skeleton |

### Exit Criteria

- `docker compose up` produces a healthy stack passing readiness probes within 30s
- Threat model reviewed by ≥2 engineers; STRIDE coverage matrix at 100%
- All four ADRs merged with rationale and alternatives-considered sections
- CI pipeline green on an empty `auth-service` skeleton

### M0 Definition of Done (Scope-Creep Guard)

<!-- Source: Refactor plan RC-015 — added to mitigate V1's M0 scope-creep meta-risk -->

M0 is complete when **all five** items below pass. No additional items may be added to M0 without an explicit scope-change request documented in a new ADR. If a candidate item is parallelizable with M1+, it belongs in M1+, not M0.

1. STRIDE threat model document reviewed and signed off by security lead.
2. ADR-001 through ADR-004 approved and merged.
3. Vault dev-mode operational with HMAC pepper stored and retrievable.
4. CI/CD pipeline passes smoke test (lint + type check + empty unit test run).
5. No auth-related code (registration, login, token issuance) merged.

### Implicit Prerequisites Surfaced

- Time-source synchronization (NTP) — required for TOTP and JWT `exp`/`nbf`
- TLS termination strategy (decision: terminate at ALB/ingress, mTLS internally optional for M9)
- Service discovery for Redis (decision: direct DNS in M0–M7, ElastiCache cluster mode in M9)

---

<!-- Source: Base (original, modified) — RC-008 (per-user DEK replaces global DEK); RC-005 (Argon2id parameters tuned to m=32768/t=2/p=4); RC-016 deliverable table format -->

## M1 — Data Layer & Crypto Primitives

**Duration:** 2 weeks
**Effort:** 4 person-weeks
**Goal:** Lock down the database schema and cryptographic primitives. The schema is the longest-lived artifact in the system; getting it right now prevents painful migrations later. (Dependency: PostgreSQL 15+)

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M1.1 | PostgreSQL 15 schema (initial migration) | `users` (id UUID v7, email CITEXT **nullable** per RC-003, password_hash TEXT, email_verified_at, status ENUM, timestamps); `roles`, `permissions`, `role_permissions`, `user_roles` — pure relational RBAC; `oauth_identities` (provider, provider_user_id, linked_at); `audit_events` partitioned monthly by RANGE on `occurred_at`; `email_verification_tokens`, `password_reset_tokens`, `refresh_tokens` (all hashed); indexes on `users(email)`, partial index `users(status) WHERE status='active'`, `refresh_tokens(user_id, device_id, revoked_at)` per RC-004 |
| D-M1.2 | **Per-user DEK** envelope encryption (RC-008 / INV-008 remediation) | New table `user_encryption_keys (user_id, wrapped_dek BYTEA, kek_id, created_at, destroyed_at)`. At registration: generate per-user DEK; wrap with master KEK from KMS; store wrapped DEK. PII columns (phone, name) encrypted with that user's DEK. Disk-level encryption (LUKS in dev, AWS EBS gp3 with KMS in cloud) for defense-in-depth. Erasure path: destroy the user's wrapped DEK, rendering that user's PII undecryptable without affecting other users. Verified by raw-page inspection: ciphertext only |
| D-M1.3 | Argon2id password hashing module (tuned per RC-005 / INV-006) | Library: `argon2-cffi` (Python) or `node-argon2`. **Parameters: m=32768, t=2, p=4 targeting ~80ms p95 hash** on target hardware; benchmarked and recorded. Pepper stored in Vault (not DB), applied as HMAC pre-hash. **NFR-001 budget breakdown documented: hash 80ms + DB lookup 60ms + JWT sign 20ms + network 40ms = 200ms p95 total** |
| D-M1.4 | Migration tooling | Alembic (Python) or Prisma Migrate (Node) per ADR-004; forward-only migrations; rollbacks via compensating migrations only (policy documented) |
| D-M1.5 | Repository pattern with parameterized queries only | Zero string-concatenated SQL; static analysis (Semgrep rule `python.sqlalchemy.security.sqlalchemy-execute-raw-query`) enforced in CI |

### Exit Criteria

- Schema migrated successfully forward and the chain replayed from empty on a fresh DB
- 100 sample users seeded with hashed passwords; **Argon2id hash verification <100ms p95 on target hardware (m=32768/t=2/p=4)** per RC-005
- All PII columns encrypted at rest with **per-user DEK**; verified by raw page contents via `pg_read_binary_file` and confirming ciphertext; per-user DEK destruction test confirms only the target user's PII becomes undecryptable
- Repository unit tests achieve ≥90% line coverage with parameterized-query assertions

### Risks Addressed

- **R-004 (PII breach):** Per-user DEK + KMS-wrapped envelope + disk encryption = three layers of defense, with per-user erasure granularity (RC-008)

---

<!-- Source: Base (original, modified) — RC-002 adds D-M2.7 password history (last 5); RC-016 table format -->

## M2 — Core Auth: Registration + Login + JWT (FR-001, FR-002)

**Duration:** 3 weeks
**Effort:** 6 person-weeks
**Goal:** The minimum viable authentication surface. Email-verified registration and JWT-issuing login. (Dependency: SendGrid)

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M2.1 | User registration endpoint (FR-001) | `POST /api/v1/auth/register` accepts email + password; zxcvbn score ≥3, min length 12, HIBP k-anonymity top-1M breach check; rate-limited 5 req/min/IP (full FR-008 in M6); CSPRNG-32-byte verification token, SHA-256 hashed in DB, raw in email; status flow `pending` → verified → `active` |
| D-M2.2 | Email verification flow | `GET /api/v1/auth/verify-email?token=...` constant-time comparison; 24h expiry; single-use; revoked on consumption |
| D-M2.3 | SendGrid integration | Wrapper service with circuit breaker (resilience4j-style); fallback to queued retry via Redis-backed BullMQ/Celery; templates: verification, password-reset, security-alert; DKIM/SPF/DMARC documented for production sender domain |
| D-M2.4 | Login endpoint (FR-002) | `POST /api/v1/auth/login` accepts email + password; constant-time Argon2id verify; issues short-lived RS256 JWT access (15min) + opaque refresh (30d) as HTTP-only Secure SameSite=Strict cookies (R-001 mitigation); JWT claims `sub, iat, exp, jti, aud, iss`; failed-login counter per email AND per IP; preliminary lockout 10 failures/15min (tuned in M6) |
| D-M2.5 | JWT issuer/verifier middleware | RS256 signature verification; `kid` in header for rotation; `GET /.well-known/jwks.json` (public key only); `jti` checked against Redis denylist on refresh (M3 expansion) |
| D-M2.6 | Security headers middleware | CSP, X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy: strict-origin-when-cross-origin; HSTS preload-ready `max-age=63072000; includeSubDomains; preload` |
| D-M2.7 | **Password history enforcement** (RC-002 / OWASP ASVS L2 V2.1.10) | New table `password_history (user_id, password_hash, created_at)` storing last 5 Argon2id hashes per user; registration rejects passwords matching any historical hash; password-change endpoint (D-M4.3) checks against history before acceptance; oldest entry evicted when exceeding 5 |

### Exit Criteria

- Happy-path: register → email → click link → login → token chain in 100% of test runs
- Login p95 latency <150ms (within NFR-001 200ms budget per RC-005 breakdown)
- Argon2id hash verification <100ms p95 (acceptable login UX per RC-005)
- SAST scan reports zero high/critical findings
- Integration tests cover ≥95% of register/login state machine transitions
- **Password history check rejects reuse of last 5 passwords** (RC-002 acceptance)

### Risks Addressed

- **R-001 (token theft via XSS):** HTTP-only cookies prevent JS access; CSP blocks inline scripts
- **R-002 (brute force):** preliminary rate limit + lockout (full in M6); password history prevents trivial credential-stuffing reuse

---

<!-- Source: Base (original, modified) — RC-004 restructures D-M3.1 to per-device refresh families with grace window per INV-005; RC-016 table format -->

## M3 — Sessions, Refresh Tokens & Password Reset (FR-005, FR-006)

**Duration:** 2 weeks
**Effort:** 4 person-weeks
**Goal:** Production-grade session lifecycle and self-service password recovery. (Dependency: Redis)

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M3.1 | **Refresh token rotation with per-device families** (FR-006, RC-004 / INV-005 remediation) | `POST /api/v1/auth/refresh` verifies opaque refresh token, issues new access + new refresh, revokes old refresh. **Per-device family**: each device assigned a `device_id` on first refresh; refresh-token row stores `(user_id, device_id, family_id, parent_token_hash)`. When device A refreshes, only device A's family rotates. **Concurrent-refresh grace**: if a revoked refresh from the same family is presented within a **30-second grace window** of the rotation, both old and new are accepted (handles legitimate race). Outside the grace window OR mismatched device family → full family revocation triggers (genuine theft, per RFC 6819 §5.2.2.3). Tokens stored as SHA-256 hashes |
| D-M3.2 | Redis session store | Key schema `session:{user_id}:{session_id}` → JSON (device, IP, UA, last_seen); TTL = refresh token lifetime (30d); sliding expiration on activity; Redis `maxmemory-policy allkeys-lru`, AOF `appendfsync everysec` |
| D-M3.3 | Logout endpoints | `POST /api/v1/auth/logout` (current session only — revokes refresh, denylists `jti` until natural expiry); `POST /api/v1/auth/logout-all` (revokes all sessions; security events trigger this; see D-M6.5) |
| D-M3.4 | Password reset flow (FR-005) | `POST /api/v1/auth/forgot-password` always returns 200 regardless of email existence (prevents enumeration); email contains time-limited (1h) single-use token (CSPRNG + hashed-storage); `POST /api/v1/auth/reset-password` revokes ALL sessions on success, sends security-alert email; **password history check applies (D-M2.7)** |
| D-M3.5 | Session enumeration API (FR-010 groundwork) | `GET /api/v1/auth/sessions` returns current user's active sessions (last-seen, IP, UA, device_id); `DELETE /api/v1/auth/sessions/:id` revokes specific session |

### Exit Criteria

- Refresh-token rotation cycle works for 100 consecutive refreshes without drift
- **Per-device grace window test** (RC-004): two devices simulating concurrent legitimate refresh within 30s — neither device is logged out, both receive new tokens. **Theft test**: revoked refresh from same family presented after 30s grace expiry → full family revocation triggers. **Cross-device theft test**: token from device A's family presented as device B → full revocation triggers
- Password reset E2E: request → email → click → set new password → all sessions revoked → security email sent
- Redis failure injected via chaos test — auth degrades to "no new logins" but existing JWTs still validate until expiry
- Email enumeration via `/forgot-password` confirmed prevented (timing variance <5ms across known/unknown emails)

### Risks Addressed

- **R-001:** Per-device reuse detection means stolen refresh tokens self-destruct on second use without false-positive logout of legitimate concurrent devices

---

<!-- Source: Base (original, modified) — RC-010 (combined erasure: per-user DEK destruction from RC-008 + audit pseudonymization scrub); RC-016 table format -->

## M4 — RBAC & Authorization (FR-004, FR-010, FR-012)

**Duration:** 2 weeks
**Effort:** 4 person-weeks
**Goal:** Permission system that scales beyond two roles. This *must* land before OAuth (M5) because OAuth identity → role mapping has nowhere to land otherwise.

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M4.1 | Role and permission model | Default roles: `user`, `admin`, `support`, `auditor` (read-only audit log access for compliance separation-of-duties); permission format `resource:action` (e.g., `user:read`, `user:write`, `audit:read`, `admin:impersonate`); all assignments in DB tables from M1; no hardcoded roles in code |
| D-M4.2 | Authorization middleware | Declarative `@require_permission("user:write")` decorator / NestJS guard; permissions loaded with JWT at issue time and cached in Redis (TTL = 15min access-token lifetime); permission changes invalidate cache immediately via Redis pub/sub |
| D-M4.3 | Profile management endpoints (FR-010) | `GET /api/v1/users/me` (own profile); `PATCH /api/v1/users/me` (name, phone, prefs — encrypted with per-user DEK per M1.2); `POST /api/v1/users/me/change-password` requires current password, **checks password history (D-M2.7)**, revokes all other sessions; email change is separate two-step flow (verification to new address → confirm) |
| D-M4.4 | **Combined GDPR erasure workflow** (RC-008 + RC-010 / INV-008 + INV-015 remediation; FR-012) | `POST /api/v1/users/me/deactivate` initiates soft-delete: status → `deactivated`, immediate session revocation. 30-day grace period before hard-delete. **Combined hard-delete erasure**: (1) destroy that user's wrapped DEK (cryptographic erasure of PII columns — only this user affected, per RC-008); (2) pseudonymize `audit_events.actor_user_id` for this user to `anonymized_<uuid>`; (3) scrub user-identifiable fragments from `audit_events.metadata` JSONB via field-allowlist filter; (4) destroy `oauth_identities.provider_user_id` mapping for this user. This combined approach targets "effective erasure" per GDPR Recital 26 (data no longer identifiable by any means reasonably likely to be used) while preserving audit chain integrity. Admin reactivation endpoint within grace period: `POST /api/v1/admin/users/:id/reactivate` |
| D-M4.5 | Authorization audit hooks | Every authorization decision (allow OR deny on protected endpoints) logged to in-process buffer; flushed to audit store in M6 |

### Exit Criteria

- 100% of API endpoints covered by either `@public` or `@require_permission(...)` — verified by automated route inspector
- Role assignment changes propagate within 5 seconds (cache invalidation test)
- **Combined erasure test** (RC-010): deactivate user → 30-day timer (time-travel fixture) → hard-delete triggers → that user's DEK destroyed, audit `actor_user_id` pseudonymized, `metadata` scrubbed, OAuth mapping deleted; other users' PII remains decryptable; audit chain integrity verified
- Authorization bypass attempts (privilege escalation, IDOR) tested in security suite; zero successful bypasses

### Risks Addressed

- **R-004:** Per-user DEK destruction + audit pseudonymization + metadata scrub = GDPR-effective erasure without breaking other users' PII or audit chain (RC-008 + RC-010)

---

<!-- Source: Base (original, modified) — RC-003 (null-email handling for INV-002) restructures D-M5.4; RC-016 table format -->

## M5 — OAuth2 (Google + GitHub) (FR-003)

**Duration:** 2 weeks
**Effort:** 3 person-weeks
**Goal:** Third-party identity federation with safe fallback.

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M5.1 | OAuth2 authorization code + PKCE flow | `GET /api/v1/auth/oauth/:provider/start` generates state (CSRF) + PKCE verifier, stores in Redis 10min TTL; `GET /api/v1/auth/oauth/:provider/callback` validates state, exchanges code, fetches user info; PKCE mandatory even for confidential clients |
| D-M5.2 | Google OAuth2 provider adapter | Endpoints from `https://accounts.google.com/.well-known/openid-configuration` (auto-discovery); scopes `openid email profile` only (data minimization) |
| D-M5.3 | GitHub OAuth2 provider adapter | GitHub does not implement OIDC discovery; endpoints hardcoded with periodic verification; scopes `read:user user:email` |
| D-M5.4 | Identity linking + **null-email handling** (RC-003 / INV-002 remediation) | First sign-in with OAuth auto-creates user with `email_verified_at=now()` (provider already verified) and default role `user`. **Null-email handling (RC-003)**: if provider returns null/missing email (GitHub users without public email), generate synthetic placeholder `{provider}_{provider_user_id}@oauth.placeholder.invalid`, mark `email_verified_at=NULL`, store `email_status='synthetic_pending'`. On next login the user is prompted to supply and verify a real email before access to non-self endpoints. **Existing email collision**: require existing-account login to link OAuth identity (prevents account takeover). `oauth_identities` table holds (provider, provider_user_id) → user_id mapping |
| D-M5.5 | Provider downtime fallback (R-003) | Health check on OAuth providers' `.well-known` endpoints every 60s; degraded → login page shows banner emphasizing email/password option; circuit breaker: 5 consecutive provider errors → 60s open circuit |
| D-M5.6 | OAuth-specific audit events | `oauth.initiated`, `oauth.callback_success`, `oauth.callback_failure`, `oauth.identity_linked`, `oauth.identity_unlinked`, **`oauth.synthetic_email_assigned`** (RC-003), **`oauth.real_email_upgraded`** (RC-003) |

### Exit Criteria

- Google E2E: button click → consent → callback → JWT issued (Playwright)
- GitHub E2E: same as above
- **GitHub null-email E2E** (RC-003): account with no public email completes OAuth callback without crash; synthetic placeholder assigned; subsequent login prompts for real email; supplying + verifying real email upgrades `email_status` to `verified`
- State-CSRF attack: tampered `state` parameter rejected with 400
- Account-collision test: OAuth callback for existing email *without* existing session → linking flow triggered (not silent takeover)
- Provider downtime simulated (block egress to `accounts.google.com`); fallback banner appears within 60s

### Risks Addressed

- **R-003 (OAuth provider downtime):** Circuit breaker + visible fallback to email/password

---

<!-- Source: Base (original, modified) — RC-001 adds D-M6.6 CSRF double-submit cookie; RC-009 adds Merkle scope subsection + soft-delete grace; RC-016 table format -->

## M6 — 2FA, Rate Limiting, CSRF & Audit Logging (FR-007, FR-008, FR-009)

**Duration:** 3 weeks
**Effort:** 6 person-weeks
**Goal:** Defense-in-depth controls and compliance-grade audit trail. Largest milestone — multiple substantial features bundled because they share the "intercept all auth events" plumbing.

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M6.1 | TOTP-based 2FA (FR-007) | `POST /api/v1/auth/2fa/enroll` generates RFC 6238 secret, returns QR provisioning URI; `POST /api/v1/auth/2fa/verify-enrollment` activates only on success; login modification: if 2FA enabled, login returns `mfa_required` instead of tokens; second call to `POST /api/v1/auth/2fa/login` with code completes auth; TOTP secret encrypted with per-user DEK (M1.2); time-window ±1 step (90s); 10 single-use recovery codes hashed in DB, shown once; rate limit 5 TOTP attempts per 15min per user → 15min lockout |
| D-M6.2 | API rate limiting (FR-008) | Token-bucket in Redis (atomic Lua); tiered limits: `/login,/register,/forgot-password` 10/min/IP + 5/min/email; `/refresh` 60/min/user; general authenticated 1000/min/user; `Retry-After` + `X-RateLimit-*` headers per IETF draft; burst 2x for 10s; Redis-backed distributed across N replicas |
| D-M6.3 | Account lockout (M2 hardening) | **Lockout triggers ON the Nth attempt** (the Nth attempt itself is rejected, per RC-009 / INV-007 disambiguation); 10 failed logins/email in 15min → 15min lockout; 50 failed/IP in 1h → 1h IP block (separate from per-email); lockouts logged as security events; admin unlock via M7 dashboard |
| D-M6.4 | Audit logging with Merkle tamper-evidence (FR-009) | Append-only `audit_events` table (M1 monthly RANGE partitions); event schema `event_id` (UUID v7), `occurred_at`, `actor_user_id`, `actor_ip`, `actor_ua`, `event_type`, `resource_type`, `resource_id`, `outcome`, `metadata` (JSONB); event types `user.registered, user.email_verified, user.login_*, user.logout, user.password_*, user.2fa_*, user.account_*, user.deactivated, user.reactivated, oauth.*, admin.user_modified, authz.permission_denied`; synchronous DB insert for security-critical events; async fan-out to S3 with Object Lock (WORM) for retention; **Merkle hash chain** — each event includes hash of previous event_id+payload; daily Merkle root anchored to immutable log. **Retention: 7 years default with 90-day soft-delete-before-drop grace per RC-009 / INV-009** |
| D-M6.5 | Security alert emails | Triggered on: new-device login, password change, 2FA disabled, multiple failed logins, password reset completed; includes IP geolocation, device/UA, timestamp, "wasn't me" link → triggers logout-all + password-reset prompt |
| D-M6.6 | **CSRF double-submit cookie protection** (RC-001 / U-011 incorporation) | `__Host-csrf-token` cookie issued on first authenticated request (random 32-byte CSPRNG, SameSite=Strict, Secure, no HttpOnly so JS can read for header echo); `X-CSRF-Token` header required on all state-changing requests (POST/PUT/PATCH/DELETE); middleware validates header value matches cookie value with constant-time comparison; GET/HEAD/OPTIONS exempt; integrates with M2.6 security headers middleware. Layered with SameSite=Strict per defense-in-depth |

### Tamper Detection Scope (RC-009 / INV-014)

<!-- Source: Refactor plan RC-009 / invariant remediation INV-014 — explicit Merkle chain scope documentation -->

The Merkle hash chain in D-M6.4 **detects** the following tampering classes:

- DBA-level direct SQL modifications to `audit_events` rows (chain hash mismatch on verification job).
- Backup restoration substituting tampered data (Merkle root mismatch against anchor log).
- Row insertion/deletion within the audit history (chain link gap).

The Merkle chain **does NOT detect** the following — these require separate detective controls documented in M7 (operational readiness):

- **Replication bypass**: a DBA writing directly to a read replica that is later promoted. Mitigation: replication monitoring + read-replica write-permission audits (M7 runbook).
- **OS-level file tampering** of PostgreSQL data files. Mitigation: file integrity monitoring (AIDE/OSSEC) on database hosts (M7 runbook).
- **Application-layer log suppression** before write. Mitigation: write-path code review + synchronous-write tests in D-M6.4 acceptance.

### Audit Retention Soft-Delete Grace (RC-009 / INV-009)

<!-- Source: Refactor plan RC-009 / invariant remediation INV-009 — soft-delete-before-drop grace window -->

Default retention is 7 years. When a partition exceeds the retention threshold, the partition enters a "detached but preserved" state for **90 days** before actual `DROP PARTITION`. This provides a 90-day recovery window if a regulated tenant requires retroactive retention extension. After 90 days, the partition is hard-dropped (irreversible). The grace window is configurable but defaults to 90 days as an operational safeguard.

### Exit Criteria

- 2FA E2E: enroll → scan QR with Google Authenticator → verify → log out → log in → prompted for code → success
- TOTP replay attack blocked (same code rejected within validity window)
- Rate limit verified under 10k req/s synthetic load: limits enforced, no false positives at legitimate use rates
- Audit hash-chain integrity: tampering with any historical row detected by chain-verification job
- Audit-event count after a synthetic 100-user, 1000-action workload matches expected count (zero loss)
- **CSRF test** (RC-001): missing `X-CSRF-Token` header on POST → 403; mismatched value → 403; valid value → request processed
- **Lockout semantics test** (RC-009 / INV-007): 10th failed login attempt itself is rejected with lockout response (not the 11th)
- **Retention soft-delete test** (RC-009 / INV-009): partition exceeding retention enters detached-preserved state for 90 days; can be re-attached within grace window; hard-dropped after 90 days

### Risks Addressed

- **R-002 (brute force):** Multi-layer rate limiting + account lockout (clarified semantics) + 2FA
- **R-004 (PII breach):** Tamper-evident audit chain (Merkle, with explicit scope) enables forensics and breach-notification compliance

---

<!-- Source: Base (original) — RC-016 table format applied -->

## M7 — Admin Dashboard & Operational Readiness (FR-011)

**Duration:** 3 weeks
**Effort:** 5 person-weeks
**Goal:** UI for human operators + the operability infrastructure NFR-005 (99.9% uptime) actually requires. This is where "we built it" becomes "we can run it."

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M7.1 | Admin dashboard (FR-011) — React + TypeScript SPA | User list with filters (status, role, signup date, last login), cursor-paginated; user detail (profile, roles, sessions, recent audit events); actions: force-logout-all, reset-password, lock/unlock, role assignment, deactivate, reactivate, impersonate (with full audit trail and time-limited 1h impersonation tokens); audit log viewer with structured filters (event_type, actor, time range, outcome); strict CSP (no `unsafe-inline`, no `unsafe-eval`); nonce-based script loading |
| D-M7.2 | Observability stack | Prometheus golden signals per endpoint + custom auth metrics (`auth_logins_total{outcome}`, `auth_active_sessions`, `auth_token_refreshes_total`, `auth_rate_limit_hits_total`); structured JSON logs with correlation IDs, no PII in logs (enforced via lint rule on log field names); OpenTelemetry with W3C Trace Context (auth → DB → Redis → SendGrid spans) |
| D-M7.3 | Dashboards & alerting | Grafana dashboards: SLI overview, latency percentiles, error rate, 2FA adoption, OAuth provider health, audit-log write rate. Alertmanager: `AuthErrorRateHigh` (5xx >1% for 5min → page), `LoginLatencyP95High` (p95 >180ms for 10min → ticket; NFR-001 buffer), `RefreshTokenReuseDetected` (>0 in 5min → page), `OAuthProviderDown` (error >50% for 2min → ticket), `AuditLogWriteFailure` (any failure → page) |
| D-M7.4 | SLOs & error budgets | Auth API availability SLO 99.9% (NFR-005) → 43.8min/month error budget; login latency SLO 99% <200ms (NFR-001); error-budget burn-rate alerts (Google SRE multi-window multi-burn-rate pattern) |
| D-M7.5 | Runbooks | Incident response for: Redis outage, PostgreSQL primary failure, SendGrid outage, OAuth provider outage, suspected credential leak, rate-limit storm, audit-log lag, **emergency JWT signing key compromise (distinct from planned rotation: immediate revocation of ALL tokens with no overlap period — per refactor plan INV-012 documentation)**, **replication-bypass audit-tamper response and OS-level file-tamper response (per RC-009 / INV-014 scope)**; on-call escalation tree; RTO 15min, RPO 1min (DB), RPO 0 (audit events — synchronous write) |
| D-M7.6 | Backup & restore | PostgreSQL pgBackRest with WAL archiving (RPO 1min, point-in-time recovery); Redis AOF + periodic RDB snapshots; **quarterly restore drill** scripted and required |

### Exit Criteria

- Dashboard usability test passes with two real operators completing 5 representative tasks unaided
- Alert fired in staging by injecting a fault → on-call receives page within 2min
- Restore drill: backup from previous day restored to scratch DB in <30min; data integrity verified
- All runbooks reviewed by an engineer not involved in their authoring
- Grafana dashboards show <60s data lag end-to-end

---

<!-- Source: Base (original) — RC-016 table format applied -->

## M8 — Verification: Load, Security, Compliance (NFR-001 through NFR-006)

**Duration:** 2 weeks
**Effort:** 4 person-weeks
**Goal:** Prove the NFRs with evidence, not assertions.

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M8.1 | Load testing (NFR-001, NFR-002) | k6 or Locust scenarios version-controlled. Scenario A: 10,000 concurrent sessions (NFR-002) — steady-state, validates connection pools, Redis memory, DB connections. Scenario B: Login spike — 1,000 logins/sec for 10min, p95 <200ms (NFR-001 per RC-005 budget). Scenario C: Token refresh storm — 5,000 refreshes/sec including per-device family grace-window stress. PgBouncer transaction pooling sized (CPU cores × 2) + effective_io_concurrency |
| D-M8.2 | Security scanning (NFR-003, OWASP Top 10) | DAST: OWASP ZAP baseline + active scan; SAST: Semgrep with OWASP Top 10 ruleset (CI from M0); Trivy + `npm audit` / `pip-audit` (zero high/critical); external pen-test engagement + remediation. Coverage matrix: A01→IDOR tests, A02→M1 encryption + JWT algorithm-confusion (`alg: none`) test, A03→SAST + parameterized-query lint, A04→threat model review (M0), A05→ZAP + headers + **CSRF tests (D-M6.6)**, A06→Trivy, A07→2FA + rate limit + lockout, A08→SBOM + signed builds (cosign), A09→M6 audit suite, A10→outbound allowlist for SendGrid + OAuth providers only |
| D-M8.3 | GDPR compliance verification (NFR-004) | Right-to-access endpoint `GET /api/v1/users/me/data-export` returns all PII as JSON; right-to-erasure tested end-to-end via M4 D-M4.4 combined erasure flow; Data Processing Agreement template for SendGrid and OAuth providers; privacy notice and consent capture on registration; DPIA (Data Protection Impact Assessment) document completed |
| D-M8.4 | OAuth E2E re-verification | Playwright suite covering full Google + GitHub flows, including consent, error, cancel paths, **and null-email synthetic-placeholder path (RC-003)** |
| D-M8.5 | Chaos / resilience testing | Kill PostgreSQL replica during sustained load → confirm failover within SLO; kill 1 of 3 Redis nodes → confirm sessions preserved; SendGrid 503 injection → verify queued retry + alert fires; **per-user DEK rotation drill (RC-008)**: simulate single-user erasure under load and confirm zero impact on other users' decryption paths |

### Exit Criteria

- All NFRs have measured evidence attached to a verification report
- Load test: 10K concurrent sessions sustained for 1h with p95 <200ms and error rate <0.1%
- Security scan: zero high/critical; medium findings either fixed or have written acceptance from security lead
- GDPR data export returns complete, correct user data in <30s for a user with 1k audit events
- Penetration test report received; all high/critical findings remediated

---

<!-- Source: Base (original, modified) — RC-013 (pre-launch verification checklist) and RC-014 (post-launch ongoing cadence) merged here; RC-016 table format -->

## M9 — Production Cutover & Hardening

**Duration:** 1 week
**Effort:** 2 person-weeks
**Goal:** Land in production with low blast radius and a smooth rollback path.

### Deliverables

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M9.1 | Production infrastructure | Multi-AZ PostgreSQL with synchronous replica, Multi-AZ Redis cluster, multi-replica auth service behind ALB; auto-scaling on CPU 70% + custom `auth_active_sessions` |
| D-M9.2 | JWT signing key rotation | Operationalize stubbed rotation from M0: dual-key serving (old `kid` still validates), 90-day rotation cadence; first production rotation drilled and documented before going live. **Note (per refactor-plan INV-012 documentation)**: emergency key-compromise scenario uses a distinct runbook (D-M7.5) — immediate revocation of ALL tokens with no overlap period; planned rotation procedure does NOT apply to compromise |
| D-M9.3 | Canary rollout | Initial 1% via header-based routing, observe 24h; then 10% for 48h, then 50% for 48h, then 100%; automated rollback if error budget consumed >25% in any window |
| D-M9.4 | On-call rotation | PagerDuty schedules with primary + secondary; each on-call engineer completed at least one runbook walkthrough; first 2 weeks post-launch senior engineer shadow on-call |
| D-M9.5 | Post-launch review (after 2 weeks of production) | Metric review against SLOs; lessons-learned document; backlog of M10+ improvements |

### Launch Readiness Gate (RC-013 / Pre-Launch Verification Checklist)

<!-- Source: Variant 2 (sonnet, default), "Pre-Launch Verification Checklist" (lines ~664-680) — merged per RC-013, adapted to V1 deliverables -->

Before flipping the canary to 100%, **all** of the following must pass. Owners are illustrative (assign to actual engineers/teams). The gate is binary: any unchecked item blocks 100% cutover.

- [ ] **Auth flow smoke test** (D-M9 production smoke): registration → email verification → login → token refresh → 2FA challenge → profile update → all pass within 5 minutes of canary deploy.
- [ ] **OAuth2 E2E**: Google and GitHub authorization code flows complete successfully in production (with production OAuth apps), including the GitHub null-email synthetic-placeholder path (RC-003).
- [ ] **Load test baseline** (D-M8.1): 10,000 concurrent sessions with p95 latency <200ms and error rate <0.1%.
- [ ] **OWASP ZAP scan** (D-M8.2): zero critical or high findings against production URL.
- [ ] **GDPR data export** (D-M8.3): test user can request and receive complete data within 30s.
- [ ] **GDPR erasure** (D-M4.4 combined flow): test user erasure destroys that user's DEK, pseudonymizes audit `actor_user_id`, scrubs metadata; verified other users' PII remains decryptable.
- [ ] **Monitoring dashboards**: all Grafana dashboards populated with real data; no gaps; <60s data lag verified.
- [ ] **Alerting**: at least one alert (synthetic) triggered and delivered to on-call during staging dress-rehearsal within 2 min.
- [ ] **Backup restore** (D-M7.6): database restore from previous-day backup completes successfully on staging; RTO <30 min and RPO <1 min verified.
- [ ] **Rollback** (D-M9.3): canary rollback tested on staging; completes within configured window; error-budget-burn auto-rollback path exercised.
- [ ] **Rate limiting** (D-M6.2): verified that exceeding configured rate limits returns 429 with correct `Retry-After` header.
- [ ] **Account lockout** (D-M6.3): verified that the 10th failed login attempt itself is rejected with lockout response (per RC-009 / INV-007 disambiguation).
- [ ] **Token theft detection** (D-M3.1): verified that out-of-grace-window refresh-token reuse from same family triggers full family revocation; concurrent legitimate refresh within 30s grace does NOT trigger false positive (per RC-004).
- [ ] **CSRF protection** (D-M6.6): verified state-changing request without `X-CSRF-Token` header returns 403; mismatched value returns 403.
- [ ] **CSP headers**: verified on production that CSP blocks inline script execution.
- [ ] **PII encryption** (D-M1.2 per-user DEK): verified that raw database dump contains no plaintext emails, phone numbers, names, or 2FA secrets.

### Post-Launch Operations (RC-014 / Ongoing Verification Cadence)

<!-- Source: Variant 2 (sonnet, default), "Ongoing Verification (Post-Launch)" (lines ~683-688) — merged per RC-014 -->

Once at 100% production traffic, the following cadence applies. Failures or regressions feed back into the M9.5 post-launch review backlog.

| Cadence | Activity | Owner | Failure Action |
|---------|----------|-------|----------------|
| **Daily** | Automated smoke test against production (D-M9 production smoke extended). | On-call | Page on-call; rollback if SLO breach |
| **Weekly** | OWASP ZAP baseline scan against staging; results compared to previous week. | Security lead | File ticket for any new finding; high/critical → immediate remediation |
| **Monthly** | Load test at 1.5× current peak to verify headroom; update capacity forecast. | SRE | Capacity-plan ticket if headroom <50% |
| **Monthly** | Per-user DEK rotation drill — random user erasure under synthetic load (RC-008). | Security lead | Investigate any other-user impact |
| **Quarterly** | Full penetration test by external firm; findings tracked to remediation. | Security lead | High/critical → 30-day remediation SLA |
| **Quarterly** | Backup restore drill (D-M7.6) on staging from production snapshot. | SRE | Investigate any RTO/RPO drift |
| **Quarterly** | Merkle audit-chain integrity verification job (D-M6.4 + RC-009 scope). | Security lead | Forensics if integrity gap detected |
| **Annually** | Full GDPR compliance audit; retention policy effectiveness review; combined-erasure (RC-010) effectiveness review against current GDPR guidance. | DPO + security lead | Update D-M4.4 erasure flow if guidance evolves |
| **Annually** | JWT signing key planned rotation drill (D-M9.2). | Security lead | Verify dual-key window and JWKS propagation |

### Exit Criteria

- 14 days at 100% traffic with zero SLO breaches
- One unforced rotation of JWT signing keys completed without user impact
- Two incident drills (simulated outages) successfully executed by on-call
- All Launch Readiness Gate items checked at the moment of 100% cutover

---

<!-- Source: Base (original, modified) — augmented with RC-001/RC-002 deliverable mappings, RC-008 per-user DEK, RC-004 per-device families, RC-005 Argon2id budget -->

## Traceability Matrix

### Functional Requirements

| Req | Milestone | Deliverable(s) |
|-----|-----------|----------------|
| FR-001 (Registration + email verification) | M2 | D-M2.1, D-M2.2, D-M2.3, D-M2.7 (password history per RC-002) |
| FR-002 (Login + JWT) | M2 | D-M2.4, D-M2.5 |
| FR-003 (OAuth2 Google + GitHub) | M5 | D-M5.1–D-M5.6 (incl. D-M5.4 null-email handling per RC-003) |
| FR-004 (RBAC) | M4 | D-M4.1, D-M4.2 |
| FR-005 (Password reset via email) | M3 | D-M3.4 |
| FR-006 (Sessions + refresh tokens) | M3 | D-M3.1 (per-device families per RC-004), D-M3.2, D-M3.3 |
| FR-007 (2FA) | M6 | D-M6.1 |
| FR-008 (Rate limiting per user) | M6 | D-M6.2, D-M6.3 |
| FR-009 (Audit logging) | M6 | D-M6.4 (Merkle + RC-009 scope), D-M6.5 |
| FR-010 (Profile management) | M4 | D-M4.3 |
| FR-011 (Admin dashboard) | M7 | D-M7.1 |
| FR-012 (Account deactivation + erasure) | M4 | D-M4.4 (combined erasure per RC-008 + RC-010) |
| (Cross-cutting) CSRF protection | M6 | D-M6.6 (per RC-001, OWASP A05) |
| (Cross-cutting) Password history | M2 | D-M2.7 (per RC-002, OWASP ASVS L2 V2.1.10) |

### Non-Functional Requirements

| Req | Milestone | Deliverable(s) | Verification | Budget Breakdown |
|-----|-----------|----------------|--------------|------------------|
| NFR-001 (<200ms auth latency) | M1, M2, M7, M8 | D-M1.3 (tuned Argon2id), D-M2.4 (impl), D-M7.4 (SLO), D-M8.1 (load test) | k6 Scenario B | **Per RC-005: hash 80ms + DB 60ms + JWT sign 20ms + network 40ms = 200ms p95** |
| NFR-002 (10K concurrent sessions) | M3, M8 | D-M3.2 (Redis sizing), D-M8.1 | k6 Scenario A | — |
| NFR-003 (OWASP Top 10) | M0, M1, M6, M8 | D-M0.3 (threat model), D-M6.6 (CSRF per RC-001), D-M8.2 | OWASP ZAP + Semgrep + pen-test | — |
| NFR-004 (GDPR) | M4, M8 | D-M4.4 (combined erasure per RC-008+RC-010), D-M8.3 | DPIA + export endpoint + erasure isolation test | — |
| NFR-005 (99.9% uptime) | M7, M9 | D-M7.4 (SLOs), D-M9.1 (multi-AZ), D-M9.3 (canary), Launch Readiness Gate | SLO measurement post-launch | — |
| NFR-006 (PII encryption) | M1 | D-M1.2 (per-user DEK per RC-008) | Raw page inspection + per-user erasure isolation test | — |

### Risks

| Risk | Milestone(s) | Mitigation Deliverable(s) |
|------|--------------|---------------------------|
| R-001 (Token theft via XSS) | M0, M2, M3, M6 | D-M0.3 (CSP), D-M2.4 (HTTP-only cookies), D-M2.6 (headers), D-M3.1 (per-device reuse detection per RC-004), D-M6.6 (CSRF per RC-001) |
| R-002 (Brute force) | M2, M6 | D-M2.4 (prelim lockout), D-M2.7 (password history per RC-002), D-M6.2 (rate limit), D-M6.3 (lockout w/ clarified semantics per RC-009), D-M6.1 (2FA) |
| R-003 (OAuth provider downtime) | M5 | D-M5.5 (circuit breaker + fallback) |
| R-004 (PII breach) | M1, M4, M6 | D-M1.2 (per-user DEK encryption per RC-008), D-M4.4 (combined GDPR erasure per RC-010), D-M6.4 (Merkle-anchored tamper-evident audit + RC-009 scope) |

### Dependencies

| Dependency | First Used | Milestone Establishing It |
|------------|------------|---------------------------|
| PostgreSQL 15+ | M1 | D-M0.1, D-M1.1 |
| Redis 7.2 | M3 | D-M0.1, D-M3.2 |
| SendGrid | M2 | D-M2.3 |
| Docker | M0 | D-M0.1 |
| HashiCorp Vault (dev) / AWS Secrets Manager (staging+prod) | M0 | D-M0.2 |
| KMS (AWS KMS or equivalent) | M1 | D-M1.2 (per-user DEK envelope encryption) |

### Success Criteria

| Criterion | Verified By |
|-----------|-------------|
| All FRs implemented and tested | Traceability matrix + per-milestone exit criteria + Launch Readiness Gate |
| OWASP compliance via security scan | D-M8.2 (incl. CSRF coverage per RC-001) |
| Load test 10K concurrent sessions | D-M8.1 Scenario A |
| OAuth2 works for Google + GitHub (incl. null-email path) | D-M5.1–D-M5.4, D-M8.4 |
| Audit logs capture all auth events with Merkle integrity | D-M6.4 + integration suite + RC-009 scope verification |
| GDPR erasure is per-user (no cross-user blast radius) | D-M4.4 combined erasure test + D-M8.5 chaos drill |

### Invariant Remediation Cross-Reference

<!-- Source: Refactor plan "Invariant Remediation Cross-Reference" table — copied for traceability -->

| Invariant | Severity | Change(s) | Status After Merge |
|-----------|----------|-----------|--------------------|
| INV-001 (V2-specific) | HIGH | N/A — V1 RBAC-before-OAuth sequencing kept (RA-002) | N/A (no authorization vacuum) |
| INV-002 (both) | HIGH | RC-003 → D-M5.4 | REMEDIATED (nullable email + synthetic placeholder + later upgrade) |
| INV-003 (both) | MEDIUM | Not in scope — 15-min JWT TTL is a known design trade-off | DOCUMENTED (JWT self-validation window accepted; denylist checked on refresh) |
| INV-004 (V2-specific) | HIGH | N/A — V1 sequencing kept | N/A |
| INV-005 (both) | HIGH | RC-004 → D-M3.1 | REMEDIATED (per-device families with 30s grace) |
| INV-006 (both) | HIGH | RC-005 → D-M1.3 + NFR-001 budget | REMEDIATED (Argon2id m=32768/t=2/p=4 ~80ms + explicit budget breakdown) |
| INV-007 (both) | MEDIUM | RC-009 → D-M6.3 acceptance criteria | DOCUMENTED (lockout triggers ON the Nth attempt) |
| INV-008 (V1) | HIGH | RC-008 → D-M1.2 + D-M4.4 | REMEDIATED (per-user DEK with envelope encryption) |
| INV-009 (V2) | HIGH | RC-009 → D-M6.4 retention subsection | MITIGATED (90-day soft-delete grace) |
| INV-010 (V2-specific) | HIGH | N/A — V1 sequencing kept | N/A |
| INV-011 (both) | MEDIUM | Not in scope — V1 retry queue kept | PARTIALLY ADDRESSED |
| INV-012 (both) | MEDIUM | Documented in D-M7.5 + D-M9.2 note | DOCUMENTED (emergency runbook distinct from planned rotation) |
| INV-013 (both) | LOW | Already ADDRESSED in V1 | ADDRESSED |
| INV-014 (both) | HIGH | RC-009 → D-M6.4 Tamper Detection Scope subsection | REMEDIATED (Merkle scope documented; out-of-scope routed to M7 runbooks) |
| INV-015 (V1) | HIGH | RC-010 → D-M4.4 combined erasure | REMEDIATED (per-user DEK destruction + audit pseudonymization + metadata scrub) |

---

<!-- Source: Base (original, modified) — RC-015 adds week-by-week parallelization schedule subsection; X-001 fix per RC-006 removes "soft sequencing 2FA vs OAuth" contradictory note -->

## Sequencing & Critical Path

```
M0 ──► M1 ──► M2 ──► M3 ──► M6 ──► M8 ──► M9
                │      │      ▲      ▲
                │      └──────┤      │
                └──► M4 ──► M5┤      │
                       │      │      │
                       └──► M7┴──────┘
```

**Critical path:** M0 → M1 → M2 → M3 → M6 → M8 → M9 (≈17 weeks)

**Parallelizable opportunities:**

- M4 (RBAC) can begin midway through M3 once M2 contracts are stable
- M5 (OAuth) waits on M4, but the provider-adapter scaffolding can be prototyped in parallel
- M7 (dashboard + ops) can start at end of M4; backend prerequisites for the admin endpoints come from M4 & M6
- M8 verification can begin partial runs after M6 lands; full pass requires M7

**Hard sequencing constraints (do not violate):**

1. **M0 before any code** — secrets and threat model must precede implementation
2. **M1 before M2** — no auth logic without schema and crypto primitives
3. **M4 before M5** — OAuth identity → role mapping requires RBAC to exist (RA-002 rejection rationale)
4. **M6 before M8** — security verification cannot meaningfully run without rate limiting, 2FA, CSRF, and audit logs in place
5. **M7 before M9** — observability and runbooks are launch prerequisites for the 99.9% NFR

### Week-by-Week Parallelization Schedule (Illustrative 3-Person Team)

<!-- Source: Variant 2 (sonnet, default), "Parallelization Opportunities" week-by-week table (lines ~634-647) — merged per RC-015, adapted to V1 milestone structure (M0-M9) -->

**Assignments are illustrative.** Real teams should adjust to actual headcount and skill mix. The total of ~41 person-weeks (sum of "Effort" column in Milestone Summary) supports either a 3-person team across ~14 calendar weeks or larger teams across compressed windows. Critical-path tasks must be sequential; non-critical tasks parallelize.

| Week | Backend A | Backend B | Frontend/DevOps |
|------|-----------|-----------|-----------------|
| 1 | M0 Vault + ADRs (pair) | M0 STRIDE threat model + ADRs (pair) | M0 Docker stack + CI/CD skeleton |
| 2 | M0 finalize + M1 schema | M0 finalize + M1 per-user DEK (RC-008) | M0 CI hardening + M1 migration tooling |
| 3 | M1 Argon2id tuning (RC-005) + repository pattern | M1 schema finalization | M1 disk encryption + KMS integration |
| 4 | M2 registration + email verification | M2 password hashing module + password history (RC-002) | M2 SendGrid integration + email templates |
| 5 | M2 login + JWT + JWKS | M2 security headers + tests | M2 integration tests + finalize |
| 6 | M3 per-device refresh families (RC-004) | M3 session store + logout | M4 RBAC seed + middleware (start) |
| 7 | M3 password reset + session API | M4 RBAC continuation | M4 profile endpoints + combined-erasure workflow (RC-008+RC-010) |
| 8 | M5 OAuth flow + Google adapter | M5 GitHub adapter + null-email handling (RC-003) | M5 provider health + audit events |
| 9 | M6 2FA enrollment + verify | M6 rate limiting + lockout (RC-009 semantics) | M6 CSRF middleware (RC-001) |
| 10 | M6 audit logging + Merkle chain | M6 security alerts + retention soft-delete (RC-009) | M7 admin SPA scaffolding |
| 11 | M6 finalize + verify | M7 observability stack | M7 admin SPA features |
| 12 | M7 SLOs + runbooks (incl. INV-012, INV-014 scope) | M7 backup/restore | M7 admin E2E + dashboard polish |
| 13 | M8 load testing (Scenario A+B) | M8 security scanning + pen-test prep | M8 GDPR verification + OAuth E2E (incl. null-email path) |
| 14 | M8 chaos + per-user DEK rotation drill | M9 production infra + canary | M9 Launch Readiness Gate runthrough + smoke |

**Wall-clock estimate**: ~14 weeks for the parallelized 3-person model (vs ~22 weeks fully sequential). Critical-path constraint M0→M1→M2→M3→M6→M8→M9 means the schedule cannot compress below ~14 weeks regardless of team size without restructuring milestones.

---

<!-- Source: Base (original) — unchanged -->

## Verification & Success Criteria Summary

### Per-Milestone Gates

Each milestone has explicit exit criteria above. No milestone is "complete" until those gates are met.

### Cross-Cutting Verification Suites (continuous from M2 onward)

- **Unit tests:** ≥90% coverage on auth-critical modules (hashing, token issuance, authorization)
- **Integration tests:** Full state-machine coverage per flow (registration, login, refresh, reset, OAuth, 2FA, CSRF)
- **Contract tests:** OpenAPI schema validated on every PR; breaking changes blocked
- **Security regression:** Each disclosed CVE / lesson-learned becomes a permanent test case
- **Performance regression:** k6 smoke test on every PR catches >20% p95 regression

### Compliance Sign-Offs (M8 deliverables)

- OWASP Top 10 coverage matrix signed by security lead (incl. A05 CSRF per RC-001)
- GDPR DPIA signed by data-protection officer (or designated equivalent), with explicit per-user erasure isolation evidence (RC-008+RC-010)
- Penetration test report with all high/critical findings remediated

### Launch Gate (M9)

- 14 days of canary at progressive traffic levels with zero SLO breaches
- One full incident drill executed by on-call rotation
- Backup restore drill within last 30 days
- **Launch Readiness Gate checklist (above) fully checked** at the moment of 100% cutover

---

<!-- Source: Base (original) — unchanged -->

## Implicit Prerequisites Surfaced

These were not in the source spec but are required for a credible launch:

1. **NTP-synchronized clocks** — TOTP, JWT `exp`/`nbf`, audit timestamps
2. **TLS termination strategy** — ALB or equivalent; HSTS preload
3. **Sender domain DKIM/SPF/DMARC** — without these, SendGrid emails will land in spam
4. **CORS policy** — explicit allowlist, no wildcard for credentialed requests
5. **Frontend domain decisions** — same-site cookie behavior depends on domain structure
6. **Mobile/native client strategy** — refresh-token-in-cookie pattern needs an alternative (PKCE + secure storage) for native; not in scope for v1 but should be documented
7. **Localization plan** — email templates and error messages need i18n hooks even if only English ships
8. **DPO and security-lead engagement** — sign-off authorities for NFR-003 and NFR-004
9. **Cost model for SendGrid** — at 10k concurrent sessions, transactional email volume must be priced
10. **KMS request-quota plan** (added per RC-008) — per-user DEK adds one KMS unwrap call per first PII read per user-session; capacity plan must account for KMS throttling and cost at 10K concurrent sessions

---

<!-- Source: Base (original, modified) — augmented with notes on RC-015 M0 DoD mitigation -->

## Risks Created by This Roadmap (Meta-Risks)

| Risk | Mitigation |
|------|-----------|
| M0 scope creep — "while we're here, let's also..." | Strict ADR review + **M0 Definition-of-Done checklist** per RC-015 (5-item gate; no additions without ADR-documented scope change) |
| M6 bundle is too large (2FA + rate limit + CSRF + audit) | Allow internal split into M6a/M6b/M6c if velocity demands; CSRF (D-M6.6) is the smallest unit and can ship first |
| M8 verification surfaces blockers late | Run partial verification continuously from M2; M8 is the *final* pass, not the *first*; Launch Readiness Gate forces explicit re-check at M9 |
| OAuth provider API changes mid-build | M5.2/M5.3 isolate provider logic behind adapter interface; contract tests guard against silent drift; null-email path (RC-003) tested explicitly |
| Per-user DEK adds KMS request volume (RC-008) | Cache unwrapped DEK in-process per session (TTL bounded by access token lifetime); KMS request quota included in implicit prerequisites |
| Combined erasure workflow complexity (RC-010) | Annual GDPR audit (post-launch cadence) reviews against current guidance; D-M4.4 acceptance test verifies audit-chain integrity post-pseudonymization |

---

*End of merged roadmap.*
