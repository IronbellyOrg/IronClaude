# Diff Analysis: Roadmap Comparison

## Metadata

- Generated: 2026-05-22T17:58Z
- Source spec: `tests/sc-roadmap/fixtures/sample_spec.md`
- Variants compared: 2
  - Variant 1: `variant-1-opus-default.md` (369 lines, opus / default persona)
  - Variant 2: `variant-2-sonnet-default.md` (378 lines, sonnet / default persona)
- Generation type: roadmap
- Depth: standard
- Categories surveyed: structural (S), content (C), contradictions (X), unique contributions (U), shared assumptions (A)

---

## Structural Differences

| # | Area | Variant 1 (opus) | Variant 2 (sonnet) | Severity |
|---|------|-------------------|---------------------|----------|
| S-001 | Total milestones | 7 (M1..M7) | 7 (M1..M7) | Low |
| S-002 | M1 scope | Foundation & Data Layer (scaffold/DB schema/secrets/TLS) — auth surface NOT exposed | Core Auth Foundation (register + login + sessions) — auth surface exposed in M1 | High |
| S-003 | M1 deliverable count | 3 (D1.1 scaffold, D1.2 schema, D1.3 secrets/TLS) | 3 (D1.1 register, D1.2 login, D1.3 sessions) | High |
| S-004 | Sessions placement | M3.D3.2 (after RBAC dependencies resolved) | M1.D1.3 (with login foundation) | Medium |
| S-005 | OAuth placement | M3.D3.1 (after core register/login in M2) | M2.D2.1 (immediately after M1 auth foundation) | Medium |
| S-006 | RBAC placement | M4 (full dedicated milestone with D4.1+D4.2) | M3 (shared with profile mgmt in same milestone) | Medium |
| S-007 | Profile management | M6.D6.1 (with admin & lifecycle) | M3.D3.2 (with RBAC) | Medium |
| S-008 | 2FA placement | M5.D5.1 (security hardening cluster) | M4.D4.1 (with rate limiting) | Low |
| S-009 | Audit logging placement | M5.D5.3 (in hardening cluster) | M5.D5.1 (with OWASP + GDPR compliance) | Low |
| S-010 | OWASP gating | M7.D7.2 (NFR gate phase) | M5.D5.2 (folded into M5 compliance work) | High |
| S-011 | GDPR/PII placement | M6.D6.1 + M6.D6.3 + M7.D7.3 (split across export, erasure, DPIA gate) | M5.D5.3 (single deliverable bundling export + erasure + consent + PII encryption) | High |
| S-012 | M7 sub-gate count | 4 sub-gates (perf, security, compliance, reliability) | 3 sub-gates (perf, scale, reliability) — security & compliance live in M5 | Medium |
| S-013 | Cookie hardening | M3.D3.3 dedicated deliverable | Embedded in M5.D5.2 OWASP work | Medium |
| S-014 | Top-of-document tables | Milestone Map (id/title/blocks/blocked-by) | Milestone Overview (id/theme/FRs/depends-on/duration) | Low |
| S-015 | Duration estimates | Not provided | Provided per milestone (~13 weeks total, M2//M3 parallel) | Medium |
| S-016 | Dependency graph rendering | ASCII text + bullet list explaining graph | ASCII text with explicit critical-path callout | Low |
| S-017 | FR coverage table | Implicit — FRs cited per-deliverable in bullets | Explicit FR Coverage Matrix table at end | Medium |
| S-018 | Technology version pinning | Embedded in narrative (per deliverable) | Dedicated Technology & Version Pinning table at end | Low |
| S-019 | Risk mitigation table | Yes — Risk / Primary mitigation / Milestone(s) | Yes — Risk / Mitigation / Milestone / Deliverable | Low |
| S-020 | NFR enforcement section | Bullet list with per-NFR mechanism | Tabular form with column for specific threshold | Low |
| S-021 | Out-of-scope reaffirmation | Present (narrative form with re-planning warning) | Present (bulleted with explicit "spec revision required" callout) | Low |
| S-022 | Success criteria → milestone mapping | Tabular at end | Tabular at end + extra "Evidence" column | Low |

**Structural verdict**: Both variants ship 7 milestones with comparable depth. The fundamental disagreement is *milestone topology*: Variant 1 treats M1 as a non-exposed foundation milestone (data + secrets only) and pushes authentication endpoints to M2; Variant 2 ships register/login/sessions inside M1 itself and pushes compliance work earlier (M5 instead of M7).

---

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|---|-------|---------------------|---------------------|----------|
| C-001 | Registration email-verification (FR-001) | SendGrid template id, zxcvbn ≥3 OR length <12, token SHA-256-hashed at rest, 24h ± 1 min TTL, resend 3/24h, audit row written | Disposable-email rejection, hex token in `email_verification_tokens`, 24h TTL, resend 3/hour, unverified pruned after 72h | Medium |
| C-002 | Login + JWT (FR-002) | RS256 with rotating 4096-bit keys, claims include iss/aud/sub/jti/iat/exp, lockout 15 min after 5 fails | RS256 via node-jose, claims sub/roles/iat/exp, lockout 30 min after 5 fails | Medium |
| C-003 | OAuth integration (FR-003) | `simple-oauth2` 5.x, fallback on >3s timeout or 5xx, alert via PagerDuty webhook | `googleapis` + GitHub REST, fallback on 10s connect / 30s total, dedicated `/health/oauth` endpoint polled every 60s | Medium |
| C-004 | Session storage (FR-006) | Redis-backed `sessions:<sid>` keys + Redis pub/sub denylist for access-token invalidation within 60s | PostgreSQL `refresh_tokens` table with `token_family` column + family-revoke-on-reuse + 50-session cap | High |
| C-005 | RBAC roles (FR-004) | 5 default roles (user/moderator/admin/support/billing_read); permission dotted strings; CI check fails if any route lacks `requiredPermission` metadata | 3 default roles (admin/editor/viewer); permission `resource:action`; custom roles via `POST /admin/roles` | Medium |
| C-006 | Permission cache | Redis TTL 10 min, invalidation via DEL + `perms:invalidated` pub/sub; cache hit ≥90% as load gate criterion | Redis TTL 5 min, fan-out via `SMEMBERS role_users:<role_id>` on role-permission change | Low |
| C-007 | 2FA (FR-007) | TOTP via `otplib` 12.x, 10 recovery codes 128-bit each argon2id-hashed at rest, sudo-mode 5-min window for enrolment, audit `mfa.bypass_attempt` | TOTP via `otpauth`, secret AES-256-GCM encrypted at rest, 10 recovery codes 8-char alphanumeric SHA-256-hashed, ±1 time step window, 3 wrong → 5-min lockout | High |
| C-008 | Rate limiting (FR-008) | Sliding-window log via Lua; 10/min login, 5/min password-reset-request, 300/min authenticated; collapses X-Forwarded-For to `user_id` bucket | INCR+EXPIRE or EVALSHA Lua; 20/min auth endpoints, 100/min user API, 200/min admin; rate-limit headers on every response; 1000+/min IP → auto-block 1h + webhook | Medium |
| C-009 | Audit logging (FR-009) | Append-only `audit_events` with `prev_hash` linear hash chain, audit-verify cron hourly, 12 enumerated event types | UUIDv7 row IDs, INSERT-only enforced by DB GRANT (no UPDATE/DELETE), monthly merkle-tree checkpoint signed with server private key, 15 enumerated event types | High |
| C-010 | PII encryption (NFR-006) | DB-layer pgcrypto AEAD (`pgp_sym_encrypt`) with KMS-managed DEK rotated every 90 days; PII columns named explicitly | App-layer AES-256-GCM with `PII_ENCRYPTION_KEY` env var (32 bytes, rotated quarterly); `email`, `display_name`, `two_fa_secret` cited | High |
| C-011 | GDPR right-to-erasure (NFR-004) | Soft delete + 30-day grace; worker hard-deletes PII (NULLs encrypted columns) while retaining audit metadata for compliance | Soft-deletes user, anonymizes email to `erased_<uuid>@erased.local`, retains audit logs with `actor_user_id = ERASED_<uuid>` | Medium |
| C-012 | GDPR export | Article 20 export via signed S3 URL valid 24h | Encrypted file in S3 + emailed link, downloadable 7 days then auto-deleted | Low |
| C-013 | Cookie hardening (R-001) | HttpOnly, Secure, SameSite=Lax, __Host- prefix; CSP `default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'` | HttpOnly, Secure, SameSite=Strict; CSP `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'`; Playwright assertion that `document.cookie` does not contain refresh | Medium |
| C-014 | Admin dashboard tech (FR-011) | Next.js 14 SPA; enforces sudo mode for destructive ops; all admin actions audited within 5s | React 18 + TanStack Table; user list <500ms with 10K users (Playwright timing); audit search <2s for 90-day window | Medium |
| C-015 | Reliability/uptime (NFR-005) | K8s 1.29 with Patroni streaming-replication + Redis Sentinel + PodDisruptionBudgets `minAvailable: 2`; chaos test killing pod/Redis-replica/Postgres-replica in sequence; SLO dashboard 99.9% over 30-day rolling window | Docker Compose with `HEALTHCHECK` + `restart: unless-stopped`; Prometheus `/metrics` endpoint + alerting rules; rolling deploy (kill one of two containers) with zero 5xx | High |
| C-016 | Performance gate (NFR-001) | k6 0.49 against 3-node staging cluster; p95 ≤200ms across login/refresh/verify-token at 10K VUs sustained 15 min; error rate <0.1% | k6 thresholds in CI: `p(95) < 200` for `endpoint:auth` tag; `p(99) < 500` for login specifically; 0 threshold failures across 3 consecutive CI runs | Medium |
| C-017 | Concurrent sessions gate (NFR-002) | Folded into D7.1 perf gate (same 10K VU scenario); Redis sized at 4 GiB with `noeviction` to surface capacity issues | Separate D7.2 stress test ramping 0→10K VUs over 10 min holding active sessions; <1% error rate; Redis <2 GiB; pg pool `max: 50` | Low |
| C-018 | Token-revocation propagation | Redis pub/sub denylist consulted on every request → access tokens invalidated within ≤60s of refresh-token revoke | Family-revoke + email notification on theft detection; no per-request denylist mentioned | High |
| C-019 | Tech-stack lock-in | Explicit D1.1 deliverable choosing Fastify 4.x vs FastAPI 0.110 at M1 (decision artifact) | Implicit in metadata header + final Technology table | Medium |
| C-020 | Account-lockout policy | 15-min lock after 5 fails; reset always returns 202 to prevent enumeration | 30-min lock after 5 fails; reset endpoint always returns 200 | Low |
| C-021 | Audit verification cadence | Hourly cron job runs `audit-verify` against the hash chain | On-demand API endpoint `GET /admin/audit/verify/:month` recomputes monthly merkle root | Medium |
| C-022 | Adversarial security tests | Custom adversarial suite for rate-limit bypass + token-theft scenarios is a named D7.2 artifact | SQL-injection + cookie-exfil acceptance tests inline in D5.2; bypass detection delegated to runtime (X-Forwarded-For monitoring) | Medium |
| C-023 | Compliance evidence handling | Formal D7.3 deliverable: DPIA signed by DPO, Data Processing Register, encryption inventory in compliance evidence repository | Implicit in D5.3: consent tracking table + erasure pipeline; no DPIA / DPO sign-off artifact named | High |
| C-024 | Email change re-verification (FR-010) | Not explicitly addressed (subsumed under D6.1 generic profile update path) | Explicit pattern: verification sent to new address; old email remains active until verification completes | Medium |
| C-025 | Avatar upload (FR-010) | Not explicitly addressed | Multipart upload, 2 MiB cap, JPEG/PNG/WebP only, Sharp resize to 128×128 and 256×256 | Low |

**Content verdict**: The variants share the same target architecture (OAuth2 + JWT + RBAC + 2FA + audit) but make materially different *implementation* choices on three high-impact axes: session storage layer (Redis vs PostgreSQL), encryption layer (DB-side pgcrypto vs app-side AES), and deployment topology (Kubernetes/Patroni vs Docker Compose).

---

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|--------------------|---------------------|---------------------|--------|
| X-001 | Session/refresh-token persistence layer | "Redis-backed `sessions:<sid>` keys" (D3.2) | "PostgreSQL `refresh_tokens` table with `token_family` column" (D1.3) | **High** — fundamental architectural divergence. Cannot pick "both" — must select one for the merged base. |
| X-002 | Account lockout duration | 15 min after 5 consecutive failures (D2.2) | 30 min after 5 failures (D1.2) | Medium — affects R-002 mitigation aggression. |
| X-003 | OAuth-provider downtime detection threshold | Fallback on >3s timeout or 5xx (D3.1) | Fallback on 10s connect / 30s total timeout (D2.1) | Medium — V1 ~10× more aggressive on slow-OAuth scenarios. |
| X-004 | Login rate-limit threshold | 10 req/min on `/auth/login` (D5.2) | 20 req/min on auth endpoints incl. `/auth/login` (D4.2) | Medium — V1 stricter; V2 more permissive. |
| X-005 | PII-at-rest encryption layer | DB-layer (pgcrypto AEAD with KMS DEK rotated 90d) (D1.2) | App-layer (AES-256-GCM with env var key rotated quarterly) (D5.3) | **High** — affects key management, query path, performance, NFR-006 implementation. |
| X-006 | Audit tamper-evidence cryptographic scheme | Linear hash chain (`prev_hash`); hourly `audit-verify` cron (D5.3) | Monthly merkle-tree checkpoint signed with server private key (D5.1) | Medium — both work; verification cadence differs by 720×. |
| X-007 | Cookie `SameSite` policy | `SameSite=Lax` with `__Host-` prefix (D3.3) | `SameSite=Strict` (D5.2 + D1.2 implicit) | Low — both prevent CSRF; Strict can break cross-origin login flows. |
| X-008 | Default RBAC role taxonomy | 5 roles (user/moderator/admin/support/billing_read) (D4.1) | 3 roles (admin/editor/viewer) (D3.1) | Medium — different separation-of-duty granularity baseline. |
| X-009 | Reliability/HA deployment topology | Kubernetes 1.29 + Patroni + Redis Sentinel + PodDisruptionBudgets + 3-AZ + chaos test (D7.4) | Docker Compose with restart policy + Prometheus alerting + rolling deploy (D7.3) | **High** — Docker Compose alone cannot achieve "99.9% uptime over a 30-day rolling window" with single-host failure isolation. |
| X-010 | Permission cache TTL | 10 min (D4.2) | 5 min (D3.1) | Low — both invalidate on change; TTL is the staleness ceiling. |
| X-011 | 2FA recovery code format & hash | 10 codes × 128-bit each, argon2id-hashed at rest (D5.1) | 10 codes × 8-char alphanumeric, SHA-256-hashed (D4.1) | Medium — V1 cryptographically stronger but harder to transcribe; V2 user-friendly but lower entropy and weaker hash. |
| X-012 | CSP `style-src` policy | `'self'` only (D3.3) | `'self' 'unsafe-inline'` (D5.2) | Low — `unsafe-inline` allows injected style attacks; V1 stricter. |
| X-013 | Refresh-token access-token revocation propagation | Per-request Redis denylist check ≤60s | Family-revoke + email; no per-request denylist | High — V2 cannot guarantee bounded latency between refresh-token revoke and access-token invalidation while the 15-min access TTL is still alive. |
| X-014 | Compliance artifact requirement | DPIA + DPO sign-off + Data Processing Register named in D7.3 | Consent table + erasure pipeline; no DPIA artifact | High — GDPR DPIA is mandatory for high-risk processing under Article 35; V2 omits it. |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|---------------|-------|
| U-001 | V1 | Dedicated D3.3 Cookie hardening deliverable separated from auth flow work — forces explicit security review of cookie envelope | High |
| U-002 | V1 | 5-role RBAC default model (user/moderator/admin/support/billing_read) capturing separation-of-duty between admin and support/billing personas | Medium |
| U-003 | V1 | CI check that fails the build if any HTTP route lacks `requiredPermission` metadata — prevents authorization-by-default-allow drift | High |
| U-004 | V1 | D7.4 Reliability gate with K8s + Patroni + chaos test killing pod / Redis replica / Postgres replica in sequence | High |
| U-005 | V1 | D7.3 Compliance gate with DPIA + DPO sign-off + Data Processing Register + encryption inventory | High |
| U-006 | V1 | Explicit Fastify vs FastAPI tech-stack decision artifact at D1.1 | Medium |
| U-007 | V1 | Adversarial rate-limit-bypass and token-theft test suite in D7.2 (named, scheduled) | High |
| U-008 | V1 | Per-request Redis pub/sub denylist enabling ≤60s access-token revocation latency bound | High |
| U-009 | V1 | Audit hash-chain (`prev_hash`) verified hourly via cron with PagerDuty alert | Medium |
| U-010 | V1 | Defence-in-depth statement: account lockout enforced *in addition to* rate limiting, not as substitute | Medium |
| U-011 | V1 | Reset endpoint returns HTTP 202 (not 200) for enumeration prevention | Low |
| U-012 | V2 | Per-milestone duration estimates totalling ~13 weeks with M2//M3 parallel branch acknowledged | Medium |
| U-013 | V2 | Critical-path callout (M1 → M3 → M4 → M7) for scheduling | High |
| U-014 | V2 | Disposable-email-domain rejection list (`disposable-email-domains` npm) | Low |
| U-015 | V2 | 72-hour pruning job for unverified accounts | Medium |
| U-016 | V2 | Concurrent-login detection: invalidate older refresh token if same user logs in from new device within 60s | Medium |
| U-017 | V2 | 50-session-per-user cap with oldest-evicted policy on new login | Low |
| U-018 | V2 | `/health/oauth` provider reachability endpoint polled every 60s exposing `{google: up\|down, github: up\|down}` | Medium |
| U-019 | V2 | Avatar upload spec: multipart, 2 MiB cap, MIME allowlist, Sharp resize to 128 and 256 | Low |
| U-020 | V2 | Email change re-verification pattern: send to new address, keep old email active until confirmation | High |
| U-021 | V2 | Per-month merkle-tree audit checkpoint with signed root | Medium |
| U-022 | V2 | Consent tracking table `user_consents` with version-tracked privacy policy acceptance | High |
| U-023 | V2 | Anonymization pattern `erased_<uuid>@erased.local` retaining `actor_user_id = ERASED_<uuid>` for audit compliance | High |
| U-024 | V2 | Burst-detection auto-block: 1000+ req/min IP → 1-hour block + webhook alert | Medium |
| U-025 | V2 | Explicit FR Coverage Matrix table with per-FR Milestone/Deliverable/Key Acceptance Test triple | High |
| U-026 | V2 | Dedicated Technology & Version Pinning table at end with rationale per component | Medium |
| U-027 | V2 | TLS 1.3 acceptance test via `nmap --script ssl-enum-ciphers` | Medium |
| U-028 | V2 | Prometheus `/metrics` + alerting rules `auth_error_rate > 0.01` 5min → PagerDuty; `auth_p99_latency > 1000` 3min → PagerDuty | Medium |
| U-029 | V2 | SQL-injection acceptance test in D5.2: `POST /auth/login` with `email: "' OR 1=1 --"` returns 401 | Low |
| U-030 | V2 | Database GRANT enforcement: no UPDATE/DELETE on `audit_logs` for app role | High |

---

## Shared Assumptions

The following preconditions are implicit in both variants. Per AD-2, UNSTATED preconditions are promoted to synthetic [SHARED-ASSUMPTION] diff points that the debate must address.

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-------------|-------------------|--------|--------|
| A-001 | JWT signing algorithm is RS256 (with rotating asymmetric keys), not HS256/EdDSA/PS256 | C-002 — both variants converge on RS256 | High — affects key management, library support, signature size, performance | UNSTATED (promoted) |
| A-002 | Argon2id parameters `m=64 MiB, t=3, p=4` are appropriate for the spec's 200ms NFR-001 budget | C-001/C-002 — both converge on identical Argon2id params | High — Argon2id at m=64MiB is ~50–100ms on commodity hardware; tight against the NFR-001 200ms p95 budget | UNSTATED (promoted) |
| A-003 | Access-token TTL = 15 minutes, refresh-token TTL = 30 days | C-002, both variants | Medium — short access TTL drives refresh frequency; 30-day refresh implies long-lived theft window unless rotation+detection works | UNSTATED (promoted) |
| A-004 | 256-bit random for one-time tokens (verification, password reset, OAuth state) is sufficient | C-001, C-003, both variants | Low — 256 bits is well above any plausible threat threshold | STATED (in V1 D2.1, D2.3) |
| A-005 | PKCE with `S256` is mandatory (not optional) for OAuth authorization-code flow | C-003 — both converge on PKCE; spec only says "OAuth2" | Medium — without PKCE, OAuth2 on public clients is vulnerable to code interception | UNSTATED (promoted) |
| A-006 | Node.js / Fastify is the implementation stack (vs Python/FastAPI, Go, etc.) | Both variants converge on Node 20 LTS + Fastify 4.x; V1 mentions FastAPI as alternative at D1.1 but selects Fastify | Medium — locks in JavaScript ecosystem dependencies (jsonwebtoken, otplib, otpauth) | UNSTATED (promoted) |
| A-007 | SendGrid is the *only* email delivery path (no SES/Mailgun fallback) | Spec lists SendGrid as dependency; neither variant proposes alternative provider | Medium — registration/verification/reset/notification all hard-depend on SendGrid availability; outage = full registration outage | STATED (spec dependency) |
| A-008 | RBAC model is role-permission (RBAC1) — not attribute-based (ABAC) or relationship-based (ReBAC) | C-005 — both variants implement role-permission tables | Medium — adequate for stated 5/3 role taxonomies but constrains future delegation/sharing flows | UNSTATED (promoted) |
| A-009 | Refresh-token reuse triggers family-revocation (RFC 6819 §5.2.2 / RFC 6749 errata) | C-018 — both variants implement family revocation | Low — well-established pattern; both correctly apply it | STATED (V1 D3.2, V2 D1.3) |
| A-010 | The "10,000 concurrent sessions" NFR-002 figure is bounded by Redis (V1) or PostgreSQL row count (V2) — i.e., a single-region single-cluster sizing | C-017 — both variants size for single-cluster Redis/Postgres; neither addresses multi-region replication | High — at 10K sessions with refresh-token rotation, write throughput on the chosen session store matters; V2's PG-backed sessions hit row contention earlier than V1's Redis-keyed sessions | UNSTATED (promoted) |
| A-011 | NFR-001 (≤200ms p95) is measured against authenticated endpoints under steady-state load — not under cold-start, post-cache-invalidation, or post-deploy traffic | Both D7.1 deliverables assume k6 steady-state scenario | Medium — Argon2id at m=64MiB on login means *first-request* login latency can exceed 200ms on cold workers regardless of cache | UNSTATED (promoted) |
| A-012 | "All PII at rest" (NFR-006) is interpreted as application-managed encryption for email, display_name, profile, and 2FA secret — *not* full-disk encryption or transparent DB encryption (TDE) | C-010 — both variants implement column-level encryption | Medium — column-level encryption blocks BTREE search on the encrypted column; both variants must address `WHERE email = ?` lookup pattern (V1 silent, V2 silent) | UNSTATED (promoted) |
| A-013 | Audit log retention period meets compliance need (no explicit retention policy stated by either variant beyond "INSERT-only" or "append-only") | C-009 — both variants design append-only audit storage | Medium — GDPR Article 17 right-to-erasure tension with audit retention is unaddressed; both rely on "actor_id retained, PII anonymized" pattern | UNSTATED (promoted) |
| A-014 | Operator alerting infrastructure (PagerDuty) is available and on-call rotation exists | V1 D3.1, D5.3, D7.4 cite PagerDuty; V2 D7.3 cites PagerDuty | Low — typical SaaS assumption | STATED (both variants) |
| A-015 | The two OAuth providers (Google, GitHub) provide ID-token claims sufficient for first-party user creation; no separate identity-proofing required | C-003 — both variants create users on first OAuth without additional verification (V2 explicitly: `email_verified_at = now()` for Google) | Medium — trusting Google's `email_verified` claim is conventional but allows account takeover via OAuth-merge if local user has the same email and OAuth-merge path is not gated | UNSTATED (promoted) |

**Shared assumption verdict**: Twelve UNSTATED preconditions surfaced, three already STATED. The taxonomy-level distribution skews toward L3 (state-mechanics) — A-010 (session-store capacity), A-011 (cold-start latency budget), A-012 (encrypted-column query pattern), and A-013 (audit retention vs GDPR erasure tension) all touch state-machine boundaries that neither advocate addressed in variant prose.

---

## Summary

- Total structural differences: 22
- Total content differences: 25
- Total contradictions: 14
- Total unique contributions: 30 (V1: 11, V2: 19)
- Total shared assumptions: 15 (UNSTATED promoted: 12, STATED: 3)
- Total comparable diff points: **S(22) + C(25) + X(14) + A(15) = 76**
- Highest-severity items (High):
  - S-002, S-003, S-010, S-011 (milestone topology disagreements)
  - C-004, C-007, C-009, C-010, C-015, C-018, C-023 (architecture/security)
  - X-001, X-005, X-009, X-013, X-014 (foundational contradictions)
  - U-003, U-004, U-005, U-007, U-008, U-020, U-022, U-023, U-025, U-030 (high-value unique contributions)
  - A-001, A-002, A-010 (load-bearing unstated assumptions)

Similarity check: 76 substantive differences across two ~370-line roadmaps — variants are NOT substantially identical (>10% diff threshold easily exceeded). Full debate proceeds.
