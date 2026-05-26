# Merge Log — Adversarial Pipeline Step 5

## Metadata

- **Base variant:** Variant 1 (opus/default) — `variant-1-opus-default.md` (403 lines)
- **Source-of-merges:** Variant 2 (sonnet/default) + invariant-probe.md HIGH-severity items
- **Executor:** merge-executor agent
- **Refactor plan:** `adversarial/refactor-plan.md` (19 planned changes)
- **Changes applied:** 19 / 19
- **Status:** SUCCESS — all planned changes applied, no escalations
- **Timestamp:** 2026-05-22T17:10:00Z
- **Output artifact:** `merged-output.md`

---

## Changes Applied

### Section A — V2 Strength Incorporations (10 changes)

#### A1 — Avatar upload added to D4.4 (FR-010)

- **Status:** APPLIED
- **Before:** D4.4 covered `GET/PATCH /users/me` for email and password only
- **After:** D4.4 now includes `POST /users/me/avatar` with S3/R2 store, 5MB cap, MIME whitelist (png/jpeg/webp), ClamAV scan, 15-min signed-URL download
- **Provenance tag:** `<!-- Source: Variant 2 (sonnet/default) D4.2 — merged per refactor-plan #A1 -->`

#### A2 — Reactivation endpoint added to D4.6 (FR-012)

- **Status:** APPLIED
- **Before:** D4.6 specified soft-delete + hard-delete only; no explicit reactivation path
- **After:** D4.6 includes `POST /auth/reactivate` requiring email verification, fresh email_hash salt, `account_reactivated` audit event
- **Provenance tag:** `<!-- Source: Variant 2 (sonnet/default) D4.6 — merged per refactor-plan #A2 -->`

#### A3 — DB-role-level audit tamper resistance added to D1.5

- **Status:** APPLIED
- **Before:** D1.5 specified application-level append-only constraint
- **After:** D1.5 now mandates `auth_app` role (INSERT/SELECT only) vs `auth_admin` role (UPDATE/DELETE), with integration-test verification
- **Provenance tag:** `<!-- Source: Variant 2 (sonnet/default) D3.9 — merged per refactor-plan #A3 -->`

#### A4 — Soak test lengthened from 1 hour to 4 hours in D5.1

- **Status:** APPLIED
- **Before:** "sustained for 1 hour"
- **After:** "sustained for 4 hours" with hour 1/2/4 marker capture for Redis memory slope + PG pool saturation
- **Provenance tag:** `<!-- Source: Base (modified per refactor-plan #A4) — adopt V2's 4-hour soak duration -->`

#### A5 — Deactivation grace period reduced from 30 days to 14 days in D4.6

- **Status:** APPLIED
- **Before:** "Hard delete after 30-day grace period"
- **After:** "Hard delete after 14-day grace period (background job runs daily, scanning for `deactivated_at < now - 14 days`)"
- **Provenance tag:** `<!-- Source: Base (modified per refactor-plan #A5) — adopt V2's 14-day grace -->`
- **Side effect:** Compliance / Retention policies bullet updated to match (14-day grace)

#### A6 — Lockout policy tightened from 10/1hr to 5/15min in D2.5

- **Status:** APPLIED
- **Before:** "Account lockout after 10 failed logins in 1 hour"
- **After:** "5 consecutive failed logins in 15 minutes", lockout duration 15 min, IP+email composite scope, 423 distinct from 429 preserved
- **Provenance tag:** `<!-- Source: Base (modified per refactor-plan #A6) — adopt V2's tighter 5/15min lockout -->`

#### A7 — Hybrid refresh-token TTL (7-day rotation + 30-day family ceiling) in D2.1

- **Status:** APPLIED
- **Before:** "Opaque 32-byte token, stored hashed in Redis with 30-day TTL, family-rotation pattern"
- **After:** "7-day rolling TTL rotated on each use ... family has an absolute lifetime ceiling of 30 days"
- **Provenance tag:** `<!-- Source: Base (modified per refactor-plan #A7) — hybrid: 7-day rotation + 30-day family ceiling -->`
- **Acceptance criterion added:** family-ceiling enforcement test

#### A8 — 4-role static hierarchy seeded on V1's dynamic schema in D4.1

- **Status:** APPLIED
- **Before:** "Three seeded roles: `user`, `moderator`, `admin`"
- **After:** "Four seeded roles forming a static hierarchy: `viewer`, `editor`, `admin`, `superadmin`"; schema retained for v2 extensibility; viewer assigned at registration with `role_assigned` audit event
- **Provenance tag:** `<!-- Source: Base (modified per refactor-plan #A8) — V2's 4-role static hierarchy seeded on V1's dynamic schema -->`
- **Side effect:** Out-of-Scope clarification added ("No fine-grained permission composition exposed in v1")

#### A9 — Monthly range partitioning added to D1.5

- **Status:** APPLIED
- **Before:** No partition strategy specified
- **After:** Monthly range partitioning on `occurred_at`, next-month partition created 7 days early, partitions > 7 years archived to S3 Glacier
- **Provenance tag:** `<!-- Source: Variant 2 (sonnet/default) D3.9 — merged per refactor-plan #A9 -->`
- **Acceptance criterion added:** monthly partition auto-creation verified in staging

#### A10 — Read-replica routing added to Cross-Cutting / Performance

- **Status:** APPLIED
- **Before:** PgBouncer + connection pooling, no replica routing
- **After:** Admin dashboard (D4.5/D4.7) and audit-export (D4.8) routed to PG read replica via separate env var; 5s lag tolerance; auth write path unaffected
- **Provenance tag:** `<!-- Source: Variant 2 (sonnet/default) Cross-Cutting / Database Operations — merged per refactor-plan #A10 -->`

### Section B — HIGH-Severity Invariant Resolutions (9 changes)

#### B1 — INV-001: `auth_events` schema migration policy added to D1.5

- **Status:** APPLIED
- **Resolution:** Migration policy: `auth_admin` DB role executes ALTER during maintenance windows; blue/green for large tables; native `ADD COLUMN ... DEFAULT NULL` (no rewrite)
- **Provenance tag:** `<!-- Source: invariant-probe INV-001 resolution per refactor-plan #B1 -->`

#### B2 — INV-002: JWKS cache TTL + key-rotation overlap window pinned in D5.6

- **Status:** APPLIED
- **Resolution:** JWKS cache TTL = 10 min; rotation procedure: publish kid → wait 11 min → cut over → 24-hour overlap → drop old kid
- **Provenance tag:** `<!-- Source: invariant-probe INV-002 resolution per refactor-plan #B2 -->`

#### B3 — INV-004: OAuth email canonicalization rules added to D3.1

- **Status:** APPLIED
- **Resolution:** NFC normalization + ASCII-lowercase domain + preserve local-part case; no Gmail dot-stripping; UNIQUE (lower(email_domain), email_local) index
- **Provenance tag:** `<!-- Source: invariant-probe INV-004 resolution per refactor-plan #B3 -->`
- **Acceptance criterion added:** canonicalization test (Gmail rule deference verified)

#### B4 — INV-008: Rate-limit hash-tag strategy at Redis Cluster scale added to D2.4

- **Status:** APPLIED
- **Resolution:** `{user:<user_id>}` hash tags for per-user co-location; `{ip:<bucket>}` for IP-only limits; atomic Lua execution; NTP-bound clock skew; Redis server clock authoritative
- **Provenance tag:** `<!-- Source: invariant-probe INV-008 resolution per refactor-plan #B4 -->`
- **Acceptance criterion added:** hash-tag co-location test

#### B5 — INV-009: "10K concurrent sessions" operational definition pinned

- **Status:** APPLIED (2 locations: Executive Summary glossary + D5.1 mirror)
- **Resolution:** Concurrent session = 1 active refresh-token family in Redis; excludes access tokens and HTTP connections; 10K target = ~10K families + ~10K–30K live access tokens
- **Provenance tags:** `<!-- Source: invariant-probe INV-009 resolution per refactor-plan #B5 -->` (glossary), `<!-- Source: invariant-probe INV-009 resolution per refactor-plan #B5 (mirror) -->` (D5.1)

#### B6 — INV-013: OAuth + 2FA interaction policy added to D3.4

- **Status:** APPLIED
- **Resolution:** OAuth-completed login DOES trigger TOTP prompt if TOTP enrolled; trusted-device cookie (D3.6) is the only exception; `oauth_login_pending_2fa` audit event registered in D1.5 taxonomy
- **Provenance tag:** `<!-- Source: invariant-probe INV-013 resolution per refactor-plan #B6 -->`
- **Acceptance criterion added:** OAuth+TOTP interaction test

#### B7 — INV-014: Deactivation-vs-access-token race resolved in D4.6

- **Status:** APPLIED
- **Resolution:** Deactivation transaction MUST revoke refresh families AND add all active access-token `jti` to denylist (regardless of bloom-filter config flag); 401 within 1s verified by integration test
- **Provenance tag:** `<!-- Source: invariant-probe INV-014 resolution per refactor-plan #B7 -->`
- **Acceptance criterion added:** deactivation race test

#### B8 — INV-016: OWASP compliance gate criteria pinned in D5.4

- **Status:** APPLIED
- **Resolution:** OWASP Top 10 2021 list; zero Critical/High at GA; Medium requires sign-off or remediation; pentest vendor report is authoritative; ZAP is regression gate not compliance basis
- **Provenance tag:** `<!-- Source: invariant-probe INV-016 resolution per refactor-plan #B8 -->`

#### B9 — INV-017: Complete audit-event taxonomy enumerated in D1.5

- **Status:** APPLIED
- **Resolution:** 35 event types explicitly enumerated (registered, email_verified, login_*, refresh_*, account_*, password_*, oauth_*, totp_*, recovery_*, trusted_device_*, role_*, permission_change_propagated, admin_action); D5.8 asserts every event has a producing E2E test
- **Provenance tag:** `<!-- Source: invariant-probe INV-017 resolution per refactor-plan #B9 -->`
- **Side effect:** D3.7 event list expanded to match taxonomy; D2.6 added `account_unlocked`

---

## Post-Merge Validation

### Structural Integrity

- **H1 count:** 1 (document title) — correct
- **H2 sections:** 13 (Executive Summary, Milestone Overview, M1–M5, Cross-Cutting Concerns, Risk Register, Success Criteria Mapping, FR/NFR Coverage Matrix, Out of Scope, Appendix: Sprint Layout) — all retained from V1
- **H3 subsections:** All under a parent H2; no orphans detected
- **H4 subsections:** None present; no H2→H4 gaps
- **Heading hierarchy:** PASS
- **Section ordering:** Preserved V1's order (Executive Summary → Milestone Overview → M1...M5 → Cross-Cutting → Risk Register → Success Criteria → Coverage Matrix → Out of Scope → Sprint Layout)

### Internal References

- **Total cross-references checked:** 24
  - "see D1.5" / "D1.5 taxonomy" / "M1 `AuditLogger`" — 6 references → all resolve to D1.5 in M1
  - "D2.x" denylist / bloom-filter / rate-limit references from M3/M4 — 5 references → all resolve to M2 deliverables
  - "D3.x" 2FA / OAuth references from M4/M5 — 3 references → all resolve to M3 deliverables
  - "D4.x" admin / audit / GDPR references from M5 — 4 references → all resolve to M4 deliverables
  - "D5.x" internal references (D5.1 → D5.3, D5.2 → D5.1, etc.) — 3 references → all resolve
  - "Cross-Cutting / Performance" / "Executive Summary glossary" — 3 references → all resolve
- **Resolved:** 24
- **Broken:** 0
- **Result:** PASS

### Contradiction Re-Scan

Scanned for the following potential contradictions introduced by the merge:

- **Lockout policy (D2.5):** verified single canonical statement — "5 consecutive failed logins in 15 minutes" appears in D2.5 and Risk Register R-002; no surviving reference to V1's original "10/1hr"
- **Deactivation grace (D4.6):** verified single canonical statement — "14-day grace" in D4.6, Compliance / Retention policies, and Success Criteria; no surviving reference to V1's original "30-day"
- **Refresh-token TTL (D2.1):** verified single canonical statement — "7-day rolling TTL ... 30-day absolute family ceiling" in D2.1 and Risk Register R-001; no surviving conflict
- **RBAC role count (D4.1):** verified single canonical statement — four roles (viewer/editor/admin/superadmin); D4.5 references "admin (or higher)" consistently; no surviving "user/moderator/admin" set
- **Soak duration (D5.1):** verified single canonical statement — "4 hours" in D5.1 and M5 acceptance criteria; no surviving "1 hour"
- **Audit event taxonomy (D1.5):** D2.6 / D3.7 event lists are subsets of the master D1.5 enumeration; no event mentioned outside D1.5; D5.8 enforces taxonomy coverage
- **OAuth+TOTP interaction (D3.4):** single pinned policy (OAuth triggers TOTP if enrolled; trusted-device exception); no surviving silent bypass

**New contradictions introduced:** 0
**Result:** PASS

### Coverage Matrix Verification

- **FR coverage:** 12/12 (FR-001 → FR-012) — all retained from V1; D4.4 now includes avatar (A1), D4.6 now includes reactivation (A2) and deactivation-denylist (B7); D1.5 expanded for FR-009 with taxonomy + DB-role + partition + migration policy
- **NFR coverage:** 6/6 (NFR-001 → NFR-006) — all retained; NFR-001 now includes D5.2 chaos-paired verification; NFR-002 references operational definition; NFR-003 references documented gate criteria; NFR-004 references 14-day grace; NFR-005 references JWKS TTL
- **Risk coverage:** 4/4 (R-001 → R-004) — all retained; mitigation columns updated to reflect merged deliverables (TTL ceiling, 5/15min lockout, hash-tag rate limit, DB-role audit, deactivation-denylist invariant, etc.)
- **Coverage statement:** "12/12 FRs, 6/6 NFRs, 4/4 risks — 100%." — preserved verbatim
- **Result:** PASS — no regressions

---

## Summary

| Metric | Count |
|--------|-------|
| Planned changes | 19 |
| Applied | 19 |
| Failed | 0 |
| Skipped | 0 |
| Escalations to orchestrator | 0 |
| Structural integrity | PASS |
| Cross-references resolved | 24 / 24 |
| New contradictions | 0 |
| Coverage regressions | 0 |

**Outcome:** All 19 planned changes from `refactor-plan.md` were applied to the V1 base with provenance annotations. The merged roadmap retains all 13 V1 H2 sections, preserves the cross-cutting tracks, risk register, coverage matrix, out-of-scope, and sprint layout. Coverage of 12/12 FR + 6/6 NFR + 4/4 R is maintained. The merge is ready for downstream comparator review.

---

*End of merge log.*
