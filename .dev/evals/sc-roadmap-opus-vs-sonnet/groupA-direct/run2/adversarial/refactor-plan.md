# Refactoring Plan: Merge Variant 1 (base) with Variant 2 additions and Invariant Patches

## Overview

- **Base variant**: Variant 1 (opus / default persona)
- **Variants contributing additions**: Variant 2 (sonnet / default persona)
- **Planned change count**: 24 changes (15 V2-additive incorporations + 9 invariant patches)
- **Rejected changes**: 6 (documented under "Changes NOT Being Made")
- **Overall risk**: Medium — most changes are additive; 5 changes (P-1, P-2, P-6, P-7, P-9) modify substantive structure or invariants and require careful application

---

## Planned Changes

### Section A — V2-Additive Incorporations (Low/Medium Risk)

#### Change A1: Add FR Coverage Matrix table

- **Source variant**: V2, "## FR Coverage Matrix" section (lines 342–358)
- **Target location**: V1 base, between "## Success Criteria → Milestone Mapping" and the GA cutover paragraph (after line 357)
- **Integration approach**: Insert as a new "## FR Coverage Matrix" section. Adjust milestone/deliverable references to match the merged document's D{M}.{N} numbering (mostly unchanged since merge keeps V1 ordering).
- **Rationale**: Debate evidence — V1 advocate full concession in Round 2 ("There is no architectural defense for V1's omission. The merge adopts V2's FR Coverage Matrix verbatim and back-populates V1's milestones."). U-025 winner V2 confidence 92%.
- **Risk level**: Low (additive)

#### Change A2: Add per-milestone duration + critical-path callout (corrected for V1 ordering)

- **Source variant**: V2 "Milestone Overview" table + "Critical path" comment (lines 12–22, 36)
- **Target location**: V1 base, augment the existing "## Milestone Map" table by adding a "Duration" column and a "Critical Path" annotation
- **Integration approach**: Add `Duration` column to V1's Milestone Map. Compute corrected durations: M1=3w (foundation expanded vs V2's M1=3w core auth — same duration since V1 M1 includes secrets+TLS+schema), M2=2w (core auth — register/login/reset), M3=2w (OAuth+sessions), M4=2w (RBAC+perm cache), M5=2w (2FA/rate-limit/audit), M6=2w (admin+lifecycle), M7=2w (NFR gates). Critical path: M1 → M2 → M3 → M5 → M6 → M7 (or M1 → M2 → M4 → M5 → M6 → M7); M3 and M4 can parallelize after M2.
- **Rationale**: U-012, U-013 winner V2 confidence 80%. INV-010 mandates correcting the 13-week figure post-topology-swap.
- **Risk level**: Low (additive metadata)
- **Total weeks (sequential)**: 15w; with M3 // M4 parallel branch after M2: ~13w

#### Change A3: Email-change re-verification pattern in D6.1

- **Source variant**: V2 D3.2, "PATCH /auth/profile accepts { display_name } (email change requires re-verification: send verification to new email, keep old email until confirmed)" (line 135)
- **Target location**: V1 D6.1 (User profile management)
- **Integration approach**: Add to V1 D6.1 artifact bullets: "`PATCH /v1/users/me/email` accepts new email; sends verification to new address via D2.1 path; original email remains the active account identifier until verification completes. New email is stored in `pending_email_changes` table (encrypted per Invariant Patch P-3 below) until consumed."
- **Rationale**: V1 advocate full concession in Round 2; U-020/C-024 winner V2 confidence 92%; patches V1 silence on account-takeover via email change
- **Risk level**: Low (additive endpoint)

#### Change A4: Add `user_consents` table to M4 alongside audit substrate

- **Source variant**: V2 D5.3 "user_consents table records { user_id, consent_type, granted_at, revoked_at }" (line 211)
- **Target location**: New deliverable D4.3 in M4 (alongside RBAC + cache invalidation), since M4 is where audit substrate work begins
- **Integration approach**: Add D4.3 "Consent ledger": table `user_consents` with `{user_id, consent_type, policy_version, granted_at, revoked_at}`. Registration writes consent row for privacy policy + ToS. Consent revocation visible in audit log via D5.3. (See Invariant Patch P-3 — table must be in PII Encryption Inventory.)
- **Rationale**: U-022 winner V2 confidence 88%; V1 advocate concede gap; GDPR Article 7 requires demonstrable consent
- **Risk level**: Low (additive table + deliverable)

#### Change A5: `erased_<uuid>@erased.local` anonymization in D6.3

- **Source variant**: V2 D5.3 erasure pattern + actor_user_id retention (lines 209–211)
- **Target location**: V1 D6.3 (Account deactivation workflow)
- **Integration approach**: Update V1 D6.3 GDPR right-to-erasure acceptance criterion. Replace "overwrites encrypted columns with NULL" with "replaces email with `erased_<uuid>@erased.local`, replaces display_name/phone/address with NULL, retains `actor_user_id = ERASED_<uuid>` in `audit_events` for compliance-mandated event-actor traceability. Idempotency: a `users.deactivated_at` non-NULL value gates re-running the erasure path (Invariant Patch P-9)."
- **Rationale**: U-023 winner V2 confidence 85%; preserves audit chain integrity better than NULL pattern
- **Risk level**: Medium (changes V1's erasure semantics; INV-016 idempotency must be patched simultaneously — see P-9)

#### Change A6: Burst-detection auto-block in D5.2

- **Source variant**: V2 D4.2 "single IP exceeds 1000 requests/minute across all rate-limit buckets, auto-block IP for 1 hour and alert via POST /internal/alerts webhook" (line 171)
- **Target location**: V1 D5.2 (API rate limiting)
- **Integration approach**: Add to V1 D5.2 acceptance criteria: "Burst-detection: IP exceeding 1000 req/min across all rate-limit buckets is auto-blocked for 1 hour and alert fired via PagerDuty webhook within 5 seconds. Allowlist mechanism via `RATE_LIMIT_IP_ALLOWLIST` env var for known enterprise NAT egress IPs (Invariant Patch P-8 below)."
- **Rationale**: U-024 winner V2 confidence 80%
- **Risk level**: Low (additive control)

#### Change A7: DB GRANT INSERT-only on `audit_events` in D5.3

- **Source variant**: V2 D5.1 "audit_logs table is INSERT-only: no GRANT for UPDATE or DELETE to application role; only DBA can modify" (line 195)
- **Target location**: V1 D5.3 (audit logging)
- **Integration approach**: Add to V1 D5.3 acceptance criteria: "DB role `auth_app` has only `INSERT` and `SELECT` privileges on `audit_events`; `UPDATE` and `DELETE` are revoked. Schema migration includes `REVOKE UPDATE, DELETE ON audit_events FROM auth_app`. Repair path (when hash-chain cron flags corruption from INV-004 race) requires DBA role with documented runbook (see Invariant Patch P-6)."
- **Rationale**: U-030 winner V2 confidence 88%; defence-in-depth complementing V1's hash chain
- **Risk level**: Medium (introduces operational dependency on DBA for chain repair; runbook required)

#### Change A8: `/health/oauth` endpoint in D3.1

- **Source variant**: V2 D2.1 "Health check endpoint /health/oauth checks provider reachability every 60 seconds and exposes { google: 'up|down', github: 'up|down' }" (line 95)
- **Target location**: V1 D3.1 (OAuth2 integration)
- **Integration approach**: Add to V1 D3.1 artifact bullets: "`GET /health/oauth` — polls Google OIDC discovery + GitHub `/zen` endpoints every 60s; exposes `{google: up|down, github: up|down, last_check: ISO-8601}`. Discrepancy with live-request fallback (V1 D3.1's >3s timeout path) is tolerated; live-request fallback is authoritative for routing decisions per INV-020."
- **Rationale**: U-018 winner V2 confidence 75%
- **Risk level**: Low (additive read endpoint)

#### Change A9: Disposable-email-domain rejection in D2.1

- **Source variant**: V2 D1.1 "Reject disposable-email domains via disposable-email-domains npm list" (line 46)
- **Target location**: V1 D2.1 (user registration)
- **Integration approach**: Add to V1 D2.1 acceptance criteria: "Registration rejects emails whose domain appears in `disposable-email-domains` npm list (locked to version 1.0.x; refreshed by quarterly dependabot PR with regression-test sample)."
- **Rationale**: U-014 winner V2 confidence 60% (Low value but easy to incorporate)
- **Risk level**: Low

#### Change A10: Unverified-account 72-hour pruning cron in D2.1

- **Source variant**: V2 D1.1 "Unverified accounts auto-pruned after 72 hours via cron job" (line 46)
- **Target location**: V1 D2.1 (user registration)
- **Integration approach**: Add to V1 D2.1 artifact bullets: "Cron `prune-unverified-users` runs daily at 03:00 UTC; deletes user rows where `email_verified_at IS NULL AND created_at < now() - INTERVAL '72 hours' AND verification_token_expires_at < now() - INTERVAL '1 minute'` — the +1 min buffer respects V1's 24h ± 1 min verification token tolerance, preventing race per INV-012."
- **Rationale**: U-015 winner V2 confidence 75%
- **Risk level**: Low

#### Change A11: 50-session cap + concurrent-login detection in D3.2

- **Source variant**: V2 D1.3 + D1.2 "max 50 active sessions per user; oldest sessions auto-evicted on new login" (line 78); "Concurrent login detection: invalidate older refresh token if same user logs in from new device within 60 seconds" (line 62)
- **Target location**: V1 D3.2 (session management)
- **Integration approach**: Add to V1 D3.2 acceptance criteria: "Session cap: 50 active refresh tokens per user; on creation of 51st, oldest is revoked AND its associated access-token `jti` is published to the denylist (binds eviction to revocation invariant — patches INV-003). Concurrent-login detection: if a login from a new device IP occurs within 60s of a prior login, the older refresh token is invalidated and the user is notified via SendGrid."
- **Rationale**: U-016, U-017 winners V2 confidence 65–70%
- **Risk level**: Medium (eviction-binding requires denylist coordination — see Invariant Patch P-1)

#### Change A12: Avatar upload constraints in D6.1

- **Source variant**: V2 D3.2 "POST /auth/profile/avatar accepts multipart upload (max 2 MiB, JPEG/PNG/WebP only), stored in S3-compatible storage, resized to 128x128 and 256x256 via Sharp" (line 135)
- **Target location**: V1 D6.1 (profile management)
- **Integration approach**: Add to V1 D6.1 artifact bullets: "Avatar upload `POST /v1/users/me/avatar`: multipart, ≤2 MiB, content-type allowlist {image/jpeg, image/png, image/webp}, server-side magic-byte verification, Sharp v0.33 resize to 128×128 and 256×256, stored in S3 with `Cache-Control: max-age=31536000, immutable`."
- **Rationale**: U-019 winner V2 confidence 60%
- **Risk level**: Low

#### Change A13: Technology & Version Pinning table

- **Source variant**: V2 "## Technology & Version Pinning" section (lines 362–375)
- **Target location**: Append as a new section after FR Coverage Matrix (after Change A1)
- **Integration approach**: Add the V2 Technology & Version Pinning table verbatim, augmented with V1-specific entries: Patroni 3.x, Keycloak-free (V1 D1.1), `simple-oauth2` 5.x (V1 D3.1), `otplib` 12.x (V1 D5.1 — prefer this over `otpauth` since V1 is base), `pgcrypto` (built-in PG 15.4), HashiCorp Vault 1.15 (V1 D1.3), `node-pg-migrate` 7.x (V1 D1.2), Semgrep `p/owasp-top-ten` (V1 D7.2), Sharp v0.33 (added by Change A12).
- **Rationale**: U-026 winner V2 confidence 75%
- **Risk level**: Low

#### Change A14: TLS 1.3 nmap acceptance test in D1.3

- **Source variant**: V2 D5.3 "nmap --script ssl-enum-ciphers -p 443 <host> shows only TLS 1.3 ciphers" (line 219)
- **Target location**: V1 D1.3 (secrets management + TLS)
- **Integration approach**: Add to V1 D1.3 acceptance criteria: "`nmap --script ssl-enum-ciphers -p 443 $HOST` enumerates ONLY TLS 1.3 cipher suites (no TLS 1.0/1.1/1.2 entries); test scripted into the staging pre-deploy smoke suite. Complementary to existing `testssl.sh` grade A+ check."
- **Rationale**: U-027 winner V2 confidence 70%; complements V1's testssl.sh
- **Risk level**: Low

#### Change A15: Prometheus alerting rules in D7.4

- **Source variant**: V2 D7.3 "Prometheus metrics endpoint at /metrics... Alerting rules: auth_error_rate > 0.01 for 5 minutes → PagerDuty. auth_p99_latency > 1000 for 3 minutes → PagerDuty" (lines 284–285)
- **Target location**: V1 D7.4 (reliability gate)
- **Integration approach**: Add to V1 D7.4 acceptance criteria: "Prometheus `/metrics` endpoint exposes `auth_login_total`, `auth_login_failures_total`, `auth_token_refresh_total`, `auth_active_sessions`, `auth_request_duration_seconds`. Alertmanager rules: `auth_error_rate > 0.01` sustained 5 min → PagerDuty P2; `auth_p99_latency > 1.0s` sustained 3 min → PagerDuty P2; `auth_denylist_publish_lag_seconds > 30` sustained 1 min → PagerDuty P1 (binds to ≤60s revocation invariant — Invariant Patch P-1)."
- **Rationale**: U-028 winner V2 confidence 75%
- **Risk level**: Low

---

### Section B — Invariant Patches (REQUIRED — High Risk)

These patches address the 9 HIGH UNADDRESSED items from the Round 2.5 invariant probe. Convergence remains BLOCKED until all are merged.

#### Invariant Patch P-1: TTL-bounded denylist + budget breakdown + Sentinel chaos test (resolves INV-001 + INV-009 + INV-022)

- **Target location**: V1 D3.2 (session management) + V1 D7.4 (reliability gate)
- **Integration approach**:
  - Replace "Redis pub/sub denylist consulted on every request" with: "Redis-backed denylist keyed `denylist:<jti>` with TTL = access-token-TTL + 60s grace; checked synchronously on every authenticated request (≤5ms per check via Redis pipelining). Per-pod in-memory cache of denylist entries with TTL ≤30s + clock-skew tolerance ≤5s + Sentinel-failover reconnect ≤10s. **Budget**: 5 + 30 + 5 + 10 = ≤50s ≤ 60s claim (margin 10s)."
  - Replace pub/sub fan-out with direct key writes (`SETEX denylist:<jti> <ttl> "1"`); subscribers no longer required; Sentinel failover preserves keys via AOF persistence (`appendonly yes; appendfsync everysec`).
  - Add to D7.4 chaos test: "Sequence includes killing Redis primary mid-revocation; verify that no in-flight `SETEX` is lost (AOF + Sentinel promotion preserves the write) and that the denylist key is visible from the new primary within ≤10s."
- **Severity**: HIGH — addresses INV-001, INV-009, INV-022
- **Risk level**: High (changes core revocation mechanism from pub/sub to TTL-keyed)
- **Migration note**: This deletes V1's pub/sub-based denylist; pub/sub is *not* re-introduced. The merged document must remove any "pub/sub" prose from D3.2.

#### Invariant Patch P-2: pgcrypto key-residency clarification + per-request KMS unwrap (resolves INV-023)

- **Target location**: V1 D1.2 (PostgreSQL schema with PII encryption) + V1 D1.3 (Secrets management)
- **Integration approach**:
  - Clarify in D1.2: "PII columns are encrypted via `pgp_sym_encrypt(plaintext, dek)`. The DEK is unwrapped from KMS *per request* by the application (`kms:GenerateDataKey` returns ciphertext-DEK + plaintext-DEK; ciphertext is stored as `dek_ciphertext` on the row; plaintext-DEK is held only in request-scoped memory and zeroed in a `try/finally` after the SQL transaction commits). The KMS *master key* never enters app memory; only ephemeral DEKs do."
  - Acceptance criteria update: "Memory probe (`valgrind` or eBPF) on a soak-test pod shows no DEK plaintext bytes outside request lifetimes. `pg_log_statement = off` in production (verified via `SHOW log_statement`); query payloads containing keys are not logged."
  - Alternative path documented in D1.1 tech-stack lock-in: "Future migration to `pg_tde` or Vault Transit for true server-side / HSM-resident decryption is tracked as a v2 follow-up; M1 ships the per-request KMS unwrap pattern."
- **Severity**: HIGH — addresses INV-023
- **Risk level**: Medium (clarifies an existing claim; no architectural inversion)

#### Invariant Patch P-3: PII Encryption Inventory + plaintext-email grep CI test (resolves INV-002 + INV-005 + INV-024)

- **Target location**: V1 D1.2 (PostgreSQL schema) + new acceptance test in V1 D7.2 (security gate)
- **Integration approach**:
  - Add to D1.2 a "PII Encryption Inventory" artifact (markdown table) enumerating every column across every table that stores PII, including V2-added tables:

    | Table | Column | PII type | Encryption | Lookup hash sidecar |
    |-------|--------|----------|------------|----------------------|
    | users | email | direct | pgcrypto AEAD | email_lookup_hash (Invariant Patch P-7) |
    | users | phone | direct | pgcrypto AEAD | — |
    | users | full_name | direct | pgcrypto AEAD | — |
    | users | address | direct | pgcrypto AEAD | — |
    | user_profiles | display_name | direct | pgcrypto AEAD | — |
    | mfa_secrets | secret | secret | pgcrypto AEAD | — |
    | password_reset_tokens | (no PII; token only) | — | — | — |
    | email_verification_tokens | token, email_ref | indirect | pgcrypto AEAD | — |
    | pending_email_changes (new from A3) | new_email | direct | pgcrypto AEAD | new_email_lookup_hash |
    | user_consents (new from A4) | user_id, consent_type, policy_version | non-PII | — | — |
    | user_oauth_identities | provider_uid, email_from_provider | indirect | pgcrypto AEAD | — |
    | audit_events | actor_id, target_id, ip, user_agent | indirect | retained but ip + user_agent stored as hashed values; user_id columns become `ERASED_<uuid>` after erasure | — |

  - Add to D7.2 a CI test: "post-integration-test-suite, run `pg_dump --column-inserts --data-only` and grep the dump for any line matching `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$` outside the `audit_events.target_id` column (which legitimately contains `erased_<uuid>@erased.local` strings). Any match fails the build with the offending table/column."
- **Severity**: HIGH — addresses INV-002, INV-005, INV-024
- **Risk level**: Medium (test addition; inventory is documentation)

#### Invariant Patch P-4: Audit hash-chain single-writer queue + DBA repair runbook (resolves INV-004 + INV-019)

- **Target location**: V1 D5.3 (audit logging)
- **Integration approach**:
  - Add to D5.3 artifact: "Hash-chain append serialization: a per-cluster Postgres advisory lock (`pg_advisory_xact_lock('audit_events'::regclass::oid)`) is acquired at the start of each `INSERT INTO audit_events` transaction. Concurrent writers serialize on the lock; throughput ≥1000 inserts/sec sustained per the D7.1 perf gate. Alternative: dedicated audit-writer worker consuming from a Redis stream — documented as v2 path."
  - Add operational runbook entry: "When the hourly `audit-verify` cron flags chain corruption (suspected race or tamper), DBA executes `audit-repair --from-checkpoint <last-good-row>` which (a) requires DBA role since `auth_app` lacks UPDATE per Change A7, (b) replays event log from the previous hourly checkpoint, (c) recomputes `prev_hash` chain forward, (d) re-runs `audit-verify` to confirm green. SLA: investigation begins within 15 min of PagerDuty alert; chain restored within 60 min."
- **Severity**: HIGH — addresses INV-004 (and INV-019 dead-end from Change A7 GRANT)
- **Risk level**: Medium (introduces serialization point; perf test validates throughput)

#### Invariant Patch P-5: Corrected schedule (resolves INV-010)

- **Target location**: V1 Milestone Map (top of document) + new "## Schedule" subsection
- **Integration approach**:
  - Replace V2's "~13 weeks (M2 // M3 parallel)" with: "**Sequential total**: 15 weeks (M1 3w + M2 2w + M3 2w + M4 2w + M5 2w + M6 2w + M7 2w). **With M3 and M4 parallelized after M2**: ~13 weeks. Critical path: M1 → M2 → M3 → M5 → M6 → M7 (or M1 → M2 → M4 → M5 → M6 → M7 depending on which parallel branch completes first). M3 and M4 each need M2's auth foundation but do not need each other's outputs."
- **Severity**: HIGH — addresses INV-010
- **Risk level**: Low (text correction)

#### Invariant Patch P-6: DBA repair runbook for hash-chain corruption (resolves operational dead-end from INV-019)

- **Target location**: D5.3 acceptance criteria + ops runbook reference
- **Integration approach**: Covered by Patch P-4's runbook section (same edit; logically distinct concern but same target location).
- **Severity**: HIGH (operationally) — covered jointly with P-4
- **Risk level**: see P-4

#### Invariant Patch P-7: `email_lookup_hash` deterministic sidecar (resolves INV-021)

- **Target location**: V1 D1.2 (schema) + V1 D2.1 (registration) + V1 D2.2 (login)
- **Integration approach**:
  - D1.2 schema additions: `users.email_lookup_hash BYTEA NOT NULL`, computed as `HMAC-SHA256(lookup_key, lower(email))` where `lookup_key` is a separate KMS-managed key (NOT the encryption DEK; lookup_key has its own rotation cadence — quarterly with re-hash migration). Unique index `users_email_lookup_hash_uidx` on `(email_lookup_hash)`. The plaintext email is encrypted in `users.email` per P-3.
  - D2.1 (registration): "Insert path computes `email_lookup_hash` before INSERT; pre-insert query `SELECT 1 FROM users WHERE email_lookup_hash = $1` enforces uniqueness without decrypting any row."
  - D2.2 (login): "Login flow looks up user by `WHERE email_lookup_hash = $1`; loads encrypted `email` only for the candidate row; decrypts in app memory via P-2 path; compares post-decrypt against submitted email to reject hash collisions (HMAC collision = ~2^-256, effectively impossible but checked defensively)."
  - `disposable_email_check` (Change A9) and `pending_email_changes.new_email_lookup_hash` (Change A3) reuse this pattern.
  - Acceptance criterion: "Login path `EXPLAIN ANALYZE` shows an index scan on `users_email_lookup_hash_uidx` with cost <1ms at 10K users; p95 login latency ≤200ms under k6 NFR-001 load with email_lookup_hash in the query plan (NFR-001 met)."
- **Severity**: HIGH — addresses INV-021
- **Risk level**: High (introduces deterministic hash sidecar with its own key — separate KMS key, separate rotation cadence; lookup_key rotation requires re-hashing all rows in a backfill migration documented in D1.2)

#### Invariant Patch P-8: Burst-block tenant allowlist (resolves INV-008)

- **Target location**: V1 D5.2 (rate limiting) — paired with Change A6
- **Integration approach**: "Burst-block exempts IPs listed in `RATE_LIMIT_IP_ALLOWLIST` (env var, CIDR-supporting; enterprise NAT egress IPs registered via support ticket). Allowlisted IPs are still subject to per-account lockout and per-route rate limits — only the IP-wide auto-block is bypassed. Allowlist is loaded at boot and reloaded on SIGHUP; audit log captures every allowlist change."
- **Severity**: MEDIUM (INV-008) — bundled with HIGH patches since it's a same-deliverable edit
- **Risk level**: Low

#### Invariant Patch P-9: Idempotency guard on erasure (resolves INV-016)

- **Target location**: V1 D6.3 (account deactivation workflow) — paired with Change A5
- **Integration approach**: "Erasure path is gated by `WHERE users.deactivated_at IS NOT NULL AND users.deactivated_at < now() - INTERVAL '30 days' AND users.erased_at IS NULL` and atomically sets `users.erased_at = now()` in the same transaction as the anonymization writes. Repeated invocation of `erase-expired-deactivated` cron observes `users.erased_at IS NOT NULL` and skips the row; chain references to `actor_user_id = ERASED_<uuid>` remain stable."
- **Severity**: LOW (INV-016) — bundled with Change A5 for atomicity
- **Risk level**: Low

---

## Changes NOT Being Made

Document differences where V1's approach was retained over V2's after deliberation.

### NotApplied-1: V2's M1 = working auth surface (S-002, S-003)

- **V2 approach**: Ship register/login/sessions in M1 itself
- **Rationale for rejection**: V1's foundation-first M1 ordering is the highest-value architectural property of the base. NIST SP 800-63B §5.1.1.2, OWASP ASVS V2.1, CIS Controls v8 §6 all require encryption + KMS + audit substrate to be operational before authentication endpoints expose user data to network traffic. V2 advocate's "early E2E testability" benefit is real but secondary; can be partially captured by lightweight harness tests against M1 substrate before M2 ships endpoints. Debate evidence: V1 advocate Round 2 cited Verizon DBIR; V2 advocate Round 2 conceded "Merge handling: Adopt V1's M1 scope (D1.2 schema + encryption baseline) as M1, shift V2's register/login to M2. The four-milestone plaintext window collapses to zero."

### NotApplied-2: V2's Docker Compose deployment topology (X-009, C-015)

- **V2 approach**: Docker Compose with `restart: unless-stopped` for HA
- **Rationale for rejection**: Mathematically infeasible against NFR-005 99.9% over 30-day rolling window. Single-host failure = total outage. V2 advocate full concession in Round 2: "Single-host Docker Compose with restart: unless-stopped cannot achieve 99.9% availability over 30 days. ... V1's three-AZ Kubernetes + Patroni + Redis Sentinel topology is the correct architecture for the stated SLO."

### NotApplied-3: V2's app-layer AES-256-GCM with env-var key (X-005, C-010)

- **V2 approach**: `PII_ENCRYPTION_KEY` env var, 32 bytes, rotated quarterly
- **Rationale for rejection**: Env-var keys appear in `docker inspect` / `/proc/<pid>/environ` / CI logs / Kubernetes Secrets dumps; V1's pgcrypto + KMS DEK keeps the key out of process listings (with Patch P-2 clarifying the per-request unwrap pattern). V2 advocate full concession in Round 2.

### NotApplied-4: V2's monthly merkle-tree audit checkpoint (X-006, C-009)

- **V2 approach**: Per-month merkle-tree with signed root verified via on-demand API
- **Rationale for rejection**: 720× longer detection latency than V1's hourly hash-chain cron. V1's pattern catches tampering within 1 hour; V2's within 1 month. For R-004 (data breach of PII with audit-log tampering as a sub-vector), 1-month detection is unacceptable. Note: V2's DB GRANT enforcement (U-030) is ADOPTED via Change A7 as a complementary defence-in-depth control alongside V1's hash-chain.

### NotApplied-5: V2's SameSite=Strict cookies + style-src 'unsafe-inline' (X-007, X-012)

- **V2 approach**: SameSite=Strict on cookies; CSP `style-src 'self' 'unsafe-inline'`
- **Rationale for rejection**: SameSite=Lax with `__Host-` prefix (V1 D3.3) is the recommended setting per OWASP Cheat Sheet Series — Strict can break cross-origin OAuth callback flows. `unsafe-inline` in `style-src` allows injected style attacks; V1's strict CSP (no unsafe-inline) is the right baseline. INV-007 (admin-subdomain guard) is patched separately in P-additional-1 below.

### NotApplied-6: V2's 3-role default RBAC (X-008)

- **V2 approach**: `admin/editor/viewer` baseline + custom roles via `POST /admin/roles`
- **Rationale for rejection**: V1's 5-role default (user/moderator/admin/support/billing_read) ships better separation-of-duty out of the box. V2's custom-role endpoint IS adopted (allows runtime creation of additional roles) — but the *default* taxonomy is V1's. Debate: V1 advocate concession Round 2 acknowledged "Custom roles via `POST /admin/roles` provides extensibility"; V2 advocate Round 2 "Adopt V1's 5-role default taxonomy. Retain V2's `POST /admin/roles` for extensibility."

---

## Additional Patches Captured but Below HIGH Severity

### Patch-additional-1: `__Host-` cookie + admin subdomain guard (INV-007 MEDIUM)

- Add to V1 D3.3: "`__Host-` prefix REQUIRES Secure + Path=/ + no Domain attribute. Admin SPA (D6.2) MUST be served on the SAME registrable domain (e.g., `example.com/admin/`), NOT a subdomain (`admin.example.com`), else `__Host-` cookies are not sent. Deployment runbook validates the constraint pre-cutover."

### Patch-additional-2: Lockout × burst-block composition (INV-011 MEDIUM)

- Add to V1 D5.2: "Account lockout (15 min from D2.2) and IP burst-block (1 hour from Change A6 + Patch P-8) are evaluated independently. The user-visible block time is `max(account_lockout_remaining, ip_burst_block_remaining)`. Both controls fire `audit.lockout` / `audit.ip_burst_block` events."

### Patch-additional-3: Empty-role default for unverified users (INV-013 MEDIUM)

- Add to V1 D4.1: "Newly-created users in the 72-hour verification window receive the `unverified_user` role with permissions = {`user.profile.read.own`, `user.profile.complete-verification`}. Full `user` role granted on `email_verified_at` set."

### Patch-additional-4: Genesis row for audit hash chain (INV-015 LOW)

- Add to V1 D5.3: "First row (`row_id = 1`) has `prev_hash = '0000000000000000000000000000000000000000000000000000000000000000'` (32 zero bytes hex-encoded). `audit-verify` cron treats genesis row as valid by definition; for fresh deployments with empty `audit_events`, cron emits `audit.fresh-deployment` and returns success."

### Patch-additional-5: Health-vs-live OAuth state divergence (INV-020 LOW)

- Add to V1 D3.1: "`/health/oauth` (Change A8) is a lagging indicator (60s cadence). Live-request fallback (V1's >3s timeout) is the authoritative source for routing decisions. Discrepancy is by design; on-call documentation explains the contract."

### Patch-additional-6: Eviction-binding to denylist (INV-003 MEDIUM)

- Covered by Change A11's integration approach (eviction publishes denylist entry for the evicted refresh-token's last access-token `jti`).

### Patch-additional-7: Verification-token tolerance vs prune (INV-012 LOW)

- Covered by Change A10's integration approach (`+1 min` buffer in prune query).

### Patch-additional-8: Disposable-email list freshness (INV-006 LOW)

- Covered by Change A9's "quarterly dependabot PR with regression-test sample".

---

## Risk Summary

| Patch / Change | Severity | Risk | Impact if not applied | Rollback path |
|----------------|----------|------|------------------------|----------------|
| A1 FR Coverage Matrix | — | Low | Auditability gap | Remove section |
| A2 Duration + critical path | — | Low | Schedule unclear | Remove column |
| A3 Email-change re-verification | — | Low | Account takeover via email change | Revert to V1 silent path |
| A4 user_consents table | — | Low | GDPR Art 7 unprovable | Drop table |
| A5 erased_<uuid> anonymization | — | Medium | Audit-chain breaks on NULL | Revert to NULL pattern |
| A6 Burst-detection auto-block | — | Low | Credential stuffing not detected | Remove rule |
| A7 DB GRANT INSERT-only | — | Medium | App-process tamper undetected | Re-grant UPDATE/DELETE |
| A8–A15 (additive) | — | Low | Each is a per-FR enhancement | Remove section |
| **P-1 TTL denylist + budget + Sentinel chaos** | HIGH | High | INV-001/INV-009/INV-022 unfixed — ≤60s claim false | Revert to V1 pub/sub (but claim breaks) |
| **P-2 pgcrypto per-request KMS unwrap** | HIGH | Medium | INV-023 unfixed — "key out of memory" claim false | Revert to original D1.2 prose (claim weakens) |
| **P-3 PII Encryption Inventory + grep CI** | HIGH | Medium | INV-002/INV-005/INV-024 unfixed — plaintext PII leaks possible | Remove inventory + CI test |
| **P-4 Audit single-writer + DBA runbook** | HIGH | Medium | INV-004/INV-019 unfixed — chain corrupts under load | Revert advisory lock (race re-emerges) |
| **P-5 Corrected schedule** | HIGH | Low | INV-010 unfixed — 13-week claim ungrounded | Restate as ~15 weeks |
| **P-7 email_lookup_hash sidecar** | HIGH | High | INV-021 unfixed — NFR-001 violated on email queries | Drop sidecar (NFR-001 fails) |
| P-8 Burst-block allowlist | MEDIUM | Low | INV-008 unfixed — enterprise NAT lockout | Remove allowlist |
| P-9 Erasure idempotency guard | LOW | Low | INV-016 unfixed — repeated erasure breaks chain | Remove gate |

---

## Review Status

- **Approval**: Auto-approved (non-interactive mode; per skill, --interactive flag not set)
- **Pre-execution validation**: All 9 HIGH UNADDRESSED invariant items have at least one corresponding patch (P-1, P-2, P-3, P-4, P-5, P-7 cover INV-001, INV-002, INV-005, INV-009, INV-010, INV-021, INV-022, INV-023, INV-024 — note P-2 covers INV-023, P-7 covers INV-021, P-3 covers INV-002+INV-005+INV-024, P-1 covers INV-001+INV-009+INV-022, P-4 covers INV-004+INV-019 [adjacent], P-5 covers INV-010).
- **Post-merge expected invariant state**: HIGH UNADDRESSED count drops from 9 to 0 (all patched); MEDIUM count drops from 9 to ~3 (INV-007/INV-013/INV-017 partial); LOW count from 6 to ~2 (INV-012/INV-014 noted but not patched explicitly).
- **Merge-executor instruction**: Apply changes in order A1–A15, then P-1–P-9, then Patch-additional-1–8. Validate post-merge per Step 5 consistency checks.
