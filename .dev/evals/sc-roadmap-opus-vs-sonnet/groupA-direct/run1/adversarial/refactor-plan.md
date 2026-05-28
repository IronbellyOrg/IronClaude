# Refactor Plan: Merging V2 Strengths into V1 Base + Resolving HIGH-Severity Invariants

## Overview

- **Base variant:** V1 (opus) — `adversarial/variant-1-opus-default.md` (403 lines)
- **Incorporating from:** V2 (sonnet) — selected strengths
- **Planned changes:** 10 (incorporate V2 strengths) + 9 (resolve HIGH-severity UNADDRESSED invariants) = **19 total**
- **Rejected V2 approaches:** 8 documented for transparency
- **Overall risk:** Medium — most changes are additive (low risk); a few modify existing V1 deliverables (medium risk); none restructure the milestone sequence (no high-risk changes)
- **Review status:** Auto-approved (non-interactive mode); `2026-05-22T16:55:00Z`

---

## Section A — Planned Changes (Incorporate V2 Strengths)

### Change #A1 — Add Avatar Upload to Profile Management

- **Diff point:** U-012
- **Source variant:** V2, section M4, D4.2
- **Target location in base:** V1's M4 § "D4.4 (FR-010): User profile endpoints"
- **Integration approach:** APPEND — extend D4.4 with an avatar-upload sub-deliverable
- **Rationale:** V1 conceded missing avatar upload in Round 1 concessions. FR-010 ("user profile management") is broader than email/password change; avatar is a standard profile field. V2's S3/R2 + signed URL design is the right pattern.
- **Risk level:** Low (additive)
- **Specific edit:** Add to D4.4 — "Avatar upload `POST /users/me/avatar` storing to S3/R2 (or compatible) with 5MB cap, MIME-type whitelist (image/png, image/jpeg, image/webp), virus scan via ClamAV sidecar; download via signed URL (15-min TTL)."

### Change #A2 — Add Explicit Reactivation Endpoint

- **Diff point:** U-013
- **Source variant:** V2, section M4, D4.6
- **Target location in base:** V1's M4 § "D4.6 (FR-012): Account deactivation workflow"
- **Integration approach:** APPEND — add reactivation sub-deliverable
- **Rationale:** V1 conceded its deactivation deliverable only described soft-delete + hard-delete; V2's explicit `/auth/reactivate` makes reactivation an active intent rather than passive grace. Better UX, clearer audit trail.
- **Risk level:** Low (additive)
- **Specific edit:** Add to D4.6 — "Reactivation endpoint `POST /auth/reactivate` during the grace window: requires email verification (re-send link), restores user row, emits `account_reactivated` audit event, regenerates a fresh `email_hash` salt to avoid collision with a future re-registration."

### Change #A3 — Add DB-Role-Level Audit Tamper Resistance

- **Diff point:** U-014
- **Source variant:** V2, section M3, D3.9 column
- **Target location in base:** V1's M1 § "D1.5 (FR-009 scaffolding): `auth_events` append-only table"
- **Integration approach:** EXTEND — add explicit DB-role-grant requirement
- **Rationale:** V1 acknowledged its append-only constraint was application-only; V2's DB-role enforcement is strictly stronger (a compromised application cannot tamper). Critical for FR-009 audit trustworthiness.
- **Risk level:** Low (configuration change)
- **Specific edit:** Add to D1.5 — "DB role separation: application connects as `auth_app` role granted only INSERT and SELECT on `auth_events`; UPDATE and DELETE grants are reserved for a separate `auth_admin` role used exclusively by retention/archive jobs. No grant of REFERENCES on this table. Verified by an integration test attempting UPDATE/DELETE from the application role and asserting permission denied."

### Change #A4 — Lengthen Soak Test to 4 Hours

- **Diff point:** C-018
- **Source variant:** V2, section M5, D5.3
- **Target location in base:** V1's M5 § "D5.1 (NFR-002)"
- **Integration approach:** REPLACE — change 1-hour soak duration to 4-hour
- **Rationale:** V1 conceded V2's longer soak surfaces slow Redis memory leaks that a 1-hour soak misses. NFR-002 (10K concurrent sessions) and NFR-005 (99.9% uptime) jointly need a longer-than-1-hour signal.
- **Risk level:** Low (test parameter change)
- **Specific edit:** Replace "sustained for 1 hour" with "sustained for 4 hours" in D5.1. Add "capture Redis memory growth slope and PostgreSQL connection-pool saturation at hour 1, hour 2, hour 4 markers; alert if slope is non-linear."

### Change #A5 — Adopt 14-Day Deactivation Grace Period

- **Diff point:** X-006 / C-008
- **Source variant:** V2, section M4, D4.5
- **Target location in base:** V1's M4 § "D4.6"
- **Integration approach:** REPLACE — change 30-day grace to 14-day
- **Rationale:** GDPR Article 17 ("right to erasure") favors shorter retention; 14 days is the common industry default and aligns with privacy-by-default. Both advocates accepted V2's window in the latter half of debate.
- **Risk level:** Low (policy parameter change)
- **Specific edit:** Replace "30-day grace period" with "14-day grace period" in D4.6. The hard-delete background job now runs daily, scanning for `deactivated_at < now - 14 days`.

### Change #A6 — Tighten Lockout Policy to 5/15min

- **Diff point:** C-007
- **Source variant:** V2, section M3, D3.8
- **Target location in base:** V1's M2 § "D2.5 (FR-002 + R-002): Account lockout"
- **Integration approach:** REPLACE — change 10/1hr to 5/15min
- **Rationale:** Closer to common industry default (Auth0, AWS Cognito both use ~5/15min). V1's 10/1hr is more permissive; V2's 5/15min is more defensive against R-002 (brute force) which the source flags as High Impact + High Probability.
- **Risk level:** Low (parameter change)
- **Specific edit:** Replace "10 failed logins in 1 hour" with "5 consecutive failed logins in 15 minutes" in D2.5. Keep the 423 Locked response semantics (distinct from 429 rate-limit per V1).

### Change #A7 — Compromise Refresh-Token TTL (7-Day Rotation, 30-Day Family Ceiling)

- **Diff point:** X-002 / C-002
- **Source variants:** Hybrid — V1's family rotation pattern + V2's shorter rotation cadence
- **Target location in base:** V1's M2 § "D2.1 (FR-002): Login refresh-token"
- **Integration approach:** MODIFY — change TTL parameters
- **Rationale:** V1's 30-day TTL with family-rotation is safe; V2's 7-day is safer-by-default. Compromise: rotate the refresh token every 7 days (per-use rotation continues), but apply an **absolute family-lifetime ceiling of 30 days** — after 30 days, the family expires and the user re-authenticates. Combines V1's reuse-detection guarantees with V2's shorter-window posture.
- **Risk level:** Medium (modifies token lifetime semantics)
- **Specific edit:** In D2.1, change refresh-token description: "Refresh token: opaque 32-byte token, stored hashed in Redis with **7-day rolling TTL** rotated on each use (family-rotation pattern per IETF OAuth 2.0 Security BCP); family has an **absolute lifetime ceiling of 30 days** after which the user must re-authenticate regardless of activity. Family revocation on reuse detection unchanged."

### Change #A8 — Static-Seeded Roles on Top of Dynamic Schema

- **Diff point:** X-004 / C-004
- **Source variants:** Hybrid — V1's schema + V2's role seeding
- **Target location in base:** V1's M4 § "D4.1 (FR-004): RBAC schema"
- **Integration approach:** MODIFY — change seeded role set; retain underlying schema
- **Rationale:** Source spec literal text is "RBAC" not "ABAC"; V2's static 4-role hierarchy matches the literal scope. But V1's underlying `roles + permissions + role_permissions + user_roles` schema is essential forward extensibility. Solution: keep V1's schema, but **seed exactly 4 roles** (`viewer`, `editor`, `admin`, `superadmin`) instead of V1's 3 (`user`, `moderator`, `admin`).
- **Risk level:** Low (data-seeding change)
- **Specific edit:** In D4.1, change "Three seeded roles: `user`, `moderator`, `admin`" to "Four seeded roles forming a static hierarchy: `viewer` (read own profile), `editor` (read+write own profile), `admin` (manage users + roles), `superadmin` (manage admins). Underlying schema (roles, permissions, role_permissions, user_roles tables) retained for v2 extensibility to fine-grained permissions, but **no permission composition exposed in v1**."

### Change #A9 — Range-Partition `audit_events` by Month

- **Diff point:** (V2 D3.9 detail not in V1)
- **Source variant:** V2 D3.9
- **Target location in base:** V1's M1 § "D1.5"
- **Integration approach:** EXTEND — add partition strategy
- **Rationale:** V1 didn't specify partitioning. V2's range-partition-by-month with cold-storage archive of partitions older than retention is the standard pattern for high-write append-only tables. Necessary for D4.7's "p95 < 500ms on 10M-event table" acceptance criterion.
- **Risk level:** Low (schema design)
- **Specific edit:** Add to D1.5 — "Table partitioning: PostgreSQL range partitioning on `occurred_at` (monthly partitions); a background job creates next-month partition 7 days before month-end; partitions older than 7 years (retention policy) are detached and archived to S3 Glacier. Partition pruning makes the M4 audit-query API (D4.7) feasible at 10M+ event scale."

### Change #A10 — Add Read Replicas for Dashboard Queries

- **Diff point:** (V2 Database Operations cross-cutting)
- **Source variant:** V2 Cross-Cutting / Database Operations
- **Target location in base:** V1's Cross-Cutting / Performance section
- **Integration approach:** EXTEND — add cross-cutting bullet
- **Rationale:** V1's PgBouncer + connection pool is good for write path; V2's read-replica routing for admin-dashboard queries avoids dashboard load impacting auth write latency. Cheap addition; high NFR-001 value.
- **Risk level:** Low (architecture addition)
- **Specific edit:** Add to Cross-Cutting / Performance bullets — "Read replica routing: admin dashboard queries (D4.5, D4.7) and audit-export queries (D4.8) routed to a PostgreSQL read replica via a separate connection-string env var; replica lag tolerated up to 5s (asserted in monitoring). Auth write path (registration, login, refresh, role change) unaffected."

---

## Section B — Resolve HIGH-Severity UNADDRESSED Invariants

Each of the 9 HIGH UNADDRESSED items from `invariant-probe.md` becomes a specific clarification deliverable inserted into the merged roadmap.

### Change #B1 — INV-001: `auth_events` Schema Migration Strategy

- **Target location in base:** V1's M1 § D1.5
- **Integration approach:** EXTEND — add migration-policy sub-bullet
- **Rationale:** Append-only DB-role-restricted tables cannot be ALTERed by the application role; need a documented schema-owner role + migration procedure that bypasses the INSERT/SELECT-only application role.
- **Risk level:** Low (policy clarification)
- **Specific edit:** Add to D1.5 — "Schema migration policy: `auth_events` schema changes (new columns, new event types) executed exclusively by the `auth_admin` DB role during a scheduled maintenance window; `ALTER TABLE` operations are blue/green where the table is large, using PostgreSQL native `ADD COLUMN ... DEFAULT NULL` (no rewrite). Every milestone that introduces new event types includes a migration plan in its acceptance criteria."

### Change #B2 — INV-002: JWKS Cache TTL + Key Rotation Overlap Window

- **Target location in base:** V1's M5 § D5.6 (key rotation drill)
- **Integration approach:** EXTEND — pin cache TTL and overlap window
- **Rationale:** Token verifiers cache RS256 public keys; cache TTL is the rotation-propagation floor. Neither variant pinned this. Without a pinned TTL, key rotation has unbounded propagation lag.
- **Risk level:** Low (parameter specification)
- **Specific edit:** Add to D5.6 — "JWKS cache TTL pinned to 10 minutes; key rotation procedure: 1) publish new `kid` in JWKS endpoint, 2) wait 11 minutes for all verifiers to refresh, 3) cut signer over to new `kid`, 4) old `kid` remains in JWKS for 24 hours to verify in-flight tokens, 5) drop old `kid` after 24 hours + access-token-TTL safety margin. Drill verifies zero auth failures during the 24-hour overlap."

### Change #B3 — INV-004: OAuth Email-Linking Canonicalization

- **Target location in base:** V1's M3 § D3.1
- **Integration approach:** EXTEND — pin canonicalization rules
- **Rationale:** Email-as-identifier is fragile without canonicalization rules. Account-takeover via case difference or Unicode normalization is a real attack vector.
- **Risk level:** Medium (security-relevant policy)
- **Specific edit:** Add to D3.1 — "Email canonicalization: all email comparisons use NFC Unicode normalization + ASCII-lowercase of the domain part + preserve case of local-part per RFC 5321 (most providers ignore local-part case in practice, but we preserve to avoid breaking edge cases). Gmail-specific normalization (dot-stripping, plus-tag removal) is NOT applied at our layer — we treat `user.test+a@gmail.com` and `usertest@gmail.com` as distinct, deferring to Google's verified-email assertion. OAuth-provided emails arrive as canonicalized strings; our stored email is canonicalized at registration. A `UNIQUE (lower(email_domain), email_local)` index enforces the boundary."

### Change #B4 — INV-008: Rate-Limit Guard at Redis Cluster Scale

- **Target location in base:** V1's M2 § D2.4
- **Integration approach:** EXTEND — pin clustering strategy
- **Rationale:** NFR-002 (10K concurrent sessions) implies Redis Cluster; sliding-window across sharded keys cannot be atomic; attackers can split-shard the budget.
- **Risk level:** Medium (rate-limit correctness at scale)
- **Specific edit:** Add to D2.4 — "Rate-limit key strategy at Redis Cluster scale: rate-limit keys use a hash tag `{user:<user_id>}` to force co-location of all per-user counters on a single shard, enabling atomic Lua-script execution of the token-bucket algorithm. IP-only rate limits (pre-auth) use `{ip:<bucket>}` where `<bucket>` is the /24 (IPv4) or /48 (IPv6) network. Clock-skew between API nodes is bounded by NTP (chrony with stratum ≤ 3); rate-limit calculations use the Redis server clock, not the API node's clock."

### Change #B5 — INV-009: Define "10K Concurrent Sessions"

- **Target location in base:** V1's Executive Summary + M5 § D5.1
- **Integration approach:** EXTEND — pin operational definition
- **Rationale:** Definition affects every NFR-002 verification step. Ambiguity propagates into Redis sizing, load-balancer config, and the soak test pattern.
- **Risk level:** Low (definition clarification)
- **Specific edit:** Add to Executive Summary glossary block (new) — "**Concurrent session** (NFR-002 measurement unit): a refresh-token family that is active (not expired, not revoked) in Redis. Equivalent operationally to: one logged-in user device. Excludes: short-lived access tokens (which may number 10K-30K simultaneously for a 10K-session user base); excludes HTTP connections (which the load balancer manages). The 10K-concurrent-session target therefore corresponds to ~10K active refresh-token families and ~10K-30K live access tokens." Mirror this definition in D5.1.

### Change #B6 — INV-013: OAuth + 2FA Interaction Policy

- **Target location in base:** V1's M3 § D3.4 (2FA verification at login)
- **Integration approach:** EXTEND — pin OAuth+2FA policy
- **Rationale:** Two valid designs exist (OAuth bypasses TOTP; OAuth still triggers TOTP). Silent default to either is wrong; consensus must pick and document.
- **Risk level:** Medium (security policy)
- **Specific edit:** Add to D3.4 — "OAuth + 2FA interaction policy: if a user has TOTP enrolled, OAuth completion DOES trigger the TOTP prompt (response: 202 with `requires: totp` even after OAuth callback). Rationale: TOTP enrollment is an explicit user opt-in for defense-in-depth; bypassing it on OAuth would reduce a user's stated security posture. Exception: trusted-device cookie (D3.6) suppresses TOTP for 30 days regardless of OAuth path. The OAuth login audit event (`oauth_login_pending_2fa`) records the 2FA-pending state for forensic clarity."

### Change #B7 — INV-014: Deactivation-vs-Access-Token Race

- **Target location in base:** V1's M4 § D4.6 (deactivation workflow)
- **Integration approach:** EXTEND — mandate denylist on deactivation
- **Rationale:** Deactivation must immediately invalidate in-flight access tokens, regardless of whether the bloom-filter denylist is in the high-security or default config. A 15-minute window of post-deactivation access is unacceptable for FR-012 and GDPR.
- **Risk level:** Medium (security-critical correctness)
- **Specific edit:** Add to D4.6 — "Deactivation invariant: when a user is deactivated (by self or admin), the deactivation transaction MUST: 1) revoke all refresh-token families in Redis, 2) add all currently-active access-token `jti` values (looked up from Redis where they were stored as a short-TTL secondary index) to the denylist, regardless of the global bloom-filter-config flag. Acceptance: a deactivation followed by an access-token usage within the TTL window returns 401 within 1s, verified by integration test."

### Change #B8 — INV-016: OWASP Compliance Gate Criteria

- **Target location in base:** V1's M5 § D5.4 (OWASP audit)
- **Integration approach:** EXTEND — pin compliance gate criteria
- **Rationale:** Sufficiency challenge: a scan + pentest is necessary but not sufficient to claim compliance without a documented gate. Need to specify severity threshold, sign-off, and which OWASP Top-10 list.
- **Risk level:** Low (compliance definition)
- **Specific edit:** Add to D5.4 — "OWASP Top 10 compliance gate criteria: (a) targeted list is **OWASP Top 10 2021** (current authoritative list at GA cut; will reassess against a 2025 list when published); (b) compliance claim requires zero Critical and zero High findings open at GA; Medium findings require documented risk acceptance signed by the security lead OR remediation; Low/Info findings are tracked but do not block GA; (c) external pentest report signed by the engagement vendor (Cobalt or equivalent) is the authoritative artifact; ZAP CI scan is a continuous regression check, not the compliance basis."

### Change #B9 — INV-017: Audit Event Taxonomy Completeness

- **Target location in base:** V1's M1 § D1.5 + per-milestone audit-event lists (D2.6, D3.7, D4.7)
- **Integration approach:** EXTEND — enumerate the full event taxonomy
- **Rationale:** Source success criterion "audit logs capture all auth events" fails sufficiency because the consensus enumerates ~10 events while source FRs imply ~20. Need explicit, complete enumeration.
- **Risk level:** Low (taxonomy completion)
- **Specific edit:** Add to D1.5 — "Audit event-type taxonomy (complete v1 enumeration): `registered`, `email_verified`, `email_verify_failed`, `login_success`, `login_failure`, `logout`, `refresh_rotated`, `refresh_reuse_detected`, `account_locked`, `account_unlocked`, `password_reset_requested`, `password_reset_completed`, `password_reset_failed`, `password_changed`, `oauth_login_success`, `oauth_login_failed`, `oauth_account_linked`, `oauth_account_unlinked`, `oauth_provider_unreachable`, `totp_enrolled`, `totp_disabled`, `totp_verified`, `totp_failed`, `recovery_codes_generated`, `recovery_codes_regenerated`, `recovery_code_used`, `trusted_device_added`, `trusted_device_removed`, `role_assigned`, `role_removed`, `permission_change_propagated`, `account_deactivated`, `account_reactivated`, `account_purged`, `admin_action` (for all admin dashboard mutations with `actor_id`, `target_id`, `action`, `before`, `after`). The acceptance test in D5.8 verifies every event type has at least one E2E test that produces it. Adding a new event type in any future milestone requires adding the event to this taxonomy AND a migration per #B1."

---

## Section C — Changes NOT Being Made (Rejected V2 Approaches)

Documenting transparency: where V2 had a position but the base (V1) approach was determined superior in debate.

| # | Rejected V2 Approach | V1 Approach Retained | Rationale (debate evidence) |
|---|----------------------|----------------------|------------------------------|
| C1 | bcrypt cost-12 password hashing | Argon2id (m=64MB, t=3, p=4) | V2 conceded Argon2 is OWASP 2025 forward choice (X-001 winner: V1 80% confidence) |
| C2 | Audit table introduced in M3 | Audit substrate in M1 (D1.5) | V1 won X-005 / S-004 unanimously — audit must precede event sources |
| C3 | No external pentest, ZAP-only | External pentest engagement (D5.4) | V2 conceded ZAP-alone insufficient for OWASP compliance claim (C-015 winner: V1 80%) |
| C4 | No chaos engineering drill | D5.2 chaos drill | V1 won C-016 unanimously — NFR-005 (99.9%) requires chaos verification |
| C5 | No DR runbook with targets | D5.5 DR runbook (RTO 1hr, RPO 5min) | V1 won C-017 unanimously |
| C6 | No IR playbook | D5.7 IR playbook with GDPR 72-hr | V1 won U-005 — GDPR Article 33 requires rehearsed notification |
| C7 | No 2FA key separation | D3.3 distinct KMS key for TOTP secrets | V1 won C-009 (85%) — V2 conceded defense-in-depth gap |
| C8 | No permission propagation mechanism | D4.3 denylist on role change | V1 won C-005 (85%) — V2 conceded "next refresh" leaves a 15-min gap |
| C9 | Sliding-window rate limiter only | Token-bucket via slowapi + Redis (kept) | C-006 was a tie at 50% — V1's token-bucket has burst-tolerance advantage; either is fine but no change to base needed |

---

## Section D — Risk Summary

| Change # | Risk | Impact | Rollback |
|----------|------|--------|----------|
| A1 (avatar) | Low | Storage cost, MIME validation gap | Disable endpoint via feature flag |
| A2 (reactivation) | Low | Audit gap if not emitting event | Feature flag + revert to passive-grace-only |
| A3 (DB-role) | Low | Migration friction | Grant UPDATE/DELETE back to `auth_app` if needed; document why |
| A4 (4-hr soak) | Low | Test execution time | Revert to 1-hr soak; risk: slow leaks missed |
| A5 (14-day grace) | Low | UX surprise if users expected 30 days | Revert to 30-day via config var (`DEACTIVATION_GRACE_DAYS`) |
| A6 (5/15min lockout) | Low | Legitimate-user lockout rate increase | Revert thresholds via config var |
| A7 (refresh TTL hybrid) | Medium | User must re-auth at 30-day ceiling | Revert to V1's 30-day rolling (no ceiling) via config var |
| A8 (4-role seed) | Low | Existing dynamic permission tests still pass | Re-seed `user/moderator/admin` via migration |
| A9 (partition by month) | Low | Migration of existing single-table to partitioned form | PostgreSQL native repartition; pre-tested in staging |
| A10 (read replicas) | Low | Replica lag visible in dashboard | Route all traffic back to primary via config var |
| B1 (schema migration policy) | Low | Adds maintenance window discipline | N/A — policy doc |
| B2 (JWKS cache TTL) | Low | Pins rotation propagation floor at 10min | Adjust TTL via config |
| B3 (email canonicalization) | Medium | Possible duplicate-account collisions during rollout | Backfill canonicalization migration in pre-prod first |
| B4 (rate-limit hash tags) | Medium | Refactor of rate-limit middleware | Tested in staging before prod; revert via feature flag |
| B5 (concurrent-session def) | Low | Documentation only | N/A |
| B6 (OAuth+2FA policy) | Medium | UX change for OAuth-with-TOTP users; security-positive | Feature flag to bypass TOTP on OAuth (not recommended) |
| B7 (deactivation denylist) | Medium | Mandates secondary jti index in Redis | Disable via feature flag (security-negative — not recommended) |
| B8 (OWASP gate criteria) | Low | Pins GA gate; may slow GA cut if findings exist | Vendor + security lead negotiate exceptions |
| B9 (audit taxonomy) | Low | Tests must cover all 35 event types | Add events incrementally; staging integration suite |

---

## Section E — Review Status

- **Mode:** Non-interactive (auto-approved)
- **Approval timestamp:** 2026-05-22T16:55:00Z
- **Approval:** Auto-approved
- **Total changes:** 19 (10 V2 incorporations + 9 invariant resolutions)
- **Hand-off to:** merge-executor agent (Step 5)
