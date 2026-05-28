# Refactor Plan

## Overview

- **Base variant**: V2 (sonnet-architect, 450 lines, 6 milestones)
- **Incorporating from**: V1 (opus-architect, 484 lines, 5 milestones)
- **Total planned changes**: 18 (8 V1-strength incorporations + 8 invariant-probe fixes + 2 contested-assumption resolutions)
- **Total rejected (V1 approaches not adopted)**: 4
- **Overall risk**: Medium (adds security-mechanism specificity + invariant fixes; structural scaffold preserved)
- **Review status**: Auto-approved (non-interactive mode)

---

## Planned Changes

### From V1 Strengths

#### Change #1 — Sequencing Rationale section

- **Source**: V1 L476–484
- **Target**: Append as final H2 section in merged roadmap before YAML close
- **Approach**: insert (verbatim from V1, with milestone number translations: V1's M2-contract-freeze becomes M3-contract-freeze in V2 numbering; V1's M1-lockout-on-Redis becomes M2-lockout-atomicity; M4-pen-test becomes M4-backend-pen-test + M5-frontend-pen-test)
- **Rationale**: Both advocates unanimously concede (S-003, 95% confidence). Future maintainers need the *why* behind milestone ordering.
- **Risk**: Low (additive section, no conflict with existing structure)

#### Change #2 — Constant-time login defense (mechanism)

- **Source**: V1 L66 ("6th attempt is rejected without invoking `PasswordHasher.verify`"), V1 L87 ("run `PasswordHasher.verify` against a constant dummy hash on miss")
- **Target**: Insert into V2's M2 deliverable D2.1 + add to M2 AC list
- **Approach**: replace V2 AC #2 boilerplate with V1's explicit mechanism; add new D2.x deliverable "Constant-time defense: `PasswordHasher.verify` against constant dummy hash on unknown-email branch; lockout-rejected path ALSO executes dummy verify before returning (fixes INV-014)"
- **Rationale**: Both advocates concede V1's mechanism is more actionable (C-005, 90% confidence). Adds critical implementation detail V2 lacked.
- **Risk**: Low (additive within existing M2)

#### Change #3 — Constant-time reset defense (mechanism)

- **Source**: V1 L218 ("always enqueue email job (drop in worker if unregistered)")
- **Target**: Replace V2 M4 D4.1 fragment "no email sent" with V1's always-enqueue mechanism
- **Approach**: modify D4.1 to "always enqueue email job; worker silently drops unregistered-email jobs; worker ALSO emits `password_reset_requested` audit row for dropped jobs so audit-log absence ≠ unregistered (fixes INV-007)"
- **Rationale**: V2's "no email sent" creates exactly the timing oracle the PRD anti-enumeration requirement prohibits (C-006, 90% confidence).
- **Risk**: Low (mechanism swap inside existing deliverable)

#### Change #4 — OQ-7 PRD-vs-TDD retention conflict

- **Source**: V1 L462 (OQ-7)
- **Target**: V2 Open Questions table (add new row)
- **Approach**: insert as OQ-PRD-TDD-1 with proposed resolution: "split tables — 90-day operational `auth_audit_log` + 12-month SOC2-relevant subset". Also amends V2 D1.2 to include optional `soc2_relevant BOOLEAN` column so M5 can derive split-tables-view without destructive migration (fixes INV-002).
- **Rationale**: V2 unilaterally picked 12-month without flagging TDD §7.2's 90-day conflict (C-004, 90% confidence; INV-002 HIGH).
- **Risk**: Medium (touches D1.2 schema which is M1 — must land before any prod audit data)

#### Change #5 — Lockout counter atomicity

- **Source**: V1 R-008 + V2 R2 concession
- **Target**: V2 M2 D2.1
- **Approach**: modify D2.1 to require atomic counter semantics: "single-statement atomic `UPDATE users SET failed_login_count = failed_login_count + 1, locked_until = CASE WHEN failed_login_count + 1 >= 5 THEN NOW() + INTERVAL '15 minutes' ELSE locked_until END WHERE email = $1 RETURNING failed_login_count, locked_until` — no SELECT FOR UPDATE needed". Add AC: "Concurrent failed logins for same email correctly trigger lockout at 5th attempt across multiple pods (integration test with 10 parallel POST /auth/login from 3 pods)".
- **Rationale**: V2's original D1.1 didn't specify atomicity (INV-009, INV-013 HIGH). Fix addresses C-001 hybrid resolution.
- **Risk**: Medium (SQL pattern change but well-understood)

#### Change #6 — Quarterly RS256 key-rotation runbook + drill

- **Source**: V1 D2.7, D5.7
- **Target**: V2 M3 (token lifecycle) — add new D3.x; V2 M6 (rollout) — add to D6.6 runbook
- **Approach**: append D3.x "RS256 key-rotation runbook with quarterly cadence; key-access audit log; in-memory tmpfs mount for private key" + amend V2 D6.6 to include "first key-rotation drill executed during M6 Phase 1 Alpha"
- **Rationale**: V2 says "rotate once before GA as dry run" without scheduled cadence (V1 contribution; high audit/SOC2 value).
- **Risk**: Low (additive deliverables)

#### Change #7 — Pen-test split (backend M4 + frontend M5)

- **Source**: V1 R-010 + V2 R2 compromise
- **Target**: V2 M5 D5.7 → split into M4-backend pen-test (new D4.x) + M5 D5.7 frontend pen-test
- **Approach**: insert into M4 new deliverable "D4.x Backend security review + penetration test (focused on backend surface: RS256 verification, refresh rotation, lockout bypass, timing oracles, password storage, rate limit) — completion gate for M4"; modify V2 D5.7 scope to frontend-specific concerns (XSS, CSRF, AuthProvider redirect loop, token storage in memory) + extend buffer to 1 week
- **Rationale**: Hybrid resolution (C-003/X-003, 78% confidence). V1's R-010 schedule-risk reasoning combined with V2's frontend-coverage concern.
- **Risk**: Medium (changes M4 scope; verify M4 capacity)

#### Change #8 — Per-email rate limit explicit

- **Source**: V1 R-002 + A-004 resolution
- **Target**: V2 M2 (auth core) — extend D2.4, D2.5 rate-limit specification
- **Approach**: modify "rate limited at 10 req/min per IP" to "rate limited at 10 req/min per IP AND 5 req/min per email (per-email is authoritative anti-brute-force control; per-IP secondary). Per-email lockout is the primary defense; per-IP guards against credential-stuffing across accounts."
- **Rationale**: A-004 resolution acknowledges per-IP false-positive risk on shared-NAT populations.
- **Risk**: Low (rate-limit config tweak)

### Invariant Probe Fixes (HIGH-severity UNADDRESSED items not already covered above)

#### Change #9 — Admin endpoint RBAC v1.0 minimal enforcement (INV-004)

- **Source**: invariant-probe.md INV-004
- **Target**: V2 M4 D4.7 admin endpoint + V2 M1 D1.1 schema + V2 OQ table
- **Approach**: modify D4.7 to require minimal admin-role enforcement: "Add `isAdmin BOOLEAN DEFAULT FALSE` column to `users` table (D1.1); seed `users.isAdmin=TRUE` for explicit admin emails at M1 deploy; JWT payload includes `isAdmin` claim from this column; admin endpoint requires `isAdmin=true` claim. Full RBAC remains v1.1+, but minimal admin-gating is v1.0 to make D4.7 implementable."
- **Rationale**: INV-004 HIGH — V2 contradicts itself by requiring admin gating while declaring RBAC enforcement out of scope.
- **Risk**: Medium (schema change to M1; small JWT payload addition to M3)

#### Change #10 — Worker emits audit row for dropped reset requests (INV-007)

- **Source**: invariant-probe.md INV-007 (also folded into Change #3)
- **Target**: V2 M4 D4.5 SendGrid integration / worker
- **Approach**: amend D4.5 worker to emit `password_reset_requested` audit event for ALL incoming requests including drops; payload distinguishes outcome via a non-user-correlatable `request_id` not by registration status; admin endpoint receives audit row for every request so absence-of-row ≠ unregistered
- **Rationale**: INV-007 HIGH — without this, admin audit query becomes enumeration oracle.
- **Risk**: Medium (audit semantics change; ensure no leakage in admin query response)

#### Change #11 — Redis isolation for BullMQ queue (INV-012)

- **Source**: invariant-probe.md INV-012
- **Target**: V2 M1 D1.5 Redis provisioning
- **Approach**: modify D1.5 to provision TWO Redis instances: `redis-session` (refresh tokens + lockout counters) and `redis-queue` (BullMQ reset-email queue). Document memory-budget per namespace. OR (lighter) single Redis with explicit `maxmemory-policy` per key-prefix + monitoring alert when queue keys exceed 30% of allocation.
- **Rationale**: INV-012 HIGH — reset-spam OOM could collapse lockout counters if colocated.
- **Risk**: Medium (infra change but standard pattern)

#### Change #12 — Dummy hash provisioned at build time (INV-001)

- **Source**: invariant-probe.md INV-001
- **Target**: V2 M2 D2.1 (constant-time defense — also see Change #2)
- **Approach**: add to D2.1 spec: "Dummy hash is a config constant, seeded at build/deploy time (NOT per-pod boot-time hash); identical across pods to maintain constant-time invariant cross-replica"
- **Rationale**: INV-001 HIGH — per-pod boot-time hash gives different verify durations cross-pod.
- **Risk**: Low (config detail)

#### Change #13 — Sliding-window lockout OR window-boundary timing parity (INV-005)

- **Source**: invariant-probe.md INV-005, diff A-003
- **Target**: V2 M2 D2.1
- **Approach**: add to D2.1 either (option A): "Lockout counter uses sliding-window via Redis sorted-set of failure timestamps; bucket evaluates last 15 minutes on each attempt", OR (option B, simpler): "Fixed-window with explicit AC: lockout-rejected response time MUST match `PasswordHasher.verify` (dummy-hash) duration regardless of window state". Recommend option B for v1.0 (simpler); option A as v1.1 upgrade.
- **Rationale**: INV-005 HIGH — boundary cliff at T+15min creates timing oracle.
- **Risk**: Low (option B is an AC addition; option A requires Redis sorted-set design)

### Contested-Assumption Resolutions

#### Change #14 — Legacy-vs-greenfield rollback branching (A-007)

- **Source**: V1 A-007 REJECT + V2 R2 compromise
- **Target**: V2 M6 D6.5 rollback procedure
- **Approach**: modify D6.5 to include explicit branch: "If legacy auth system exists at GA: rollback drill targets feature-flag-off + legacy auth handles traffic. If greenfield (no legacy): rollback drill is replaced with feature-flag-off blast-radius test — confirm auth-disabled state returns 503 for all `/auth/*` endpoints cleanly. Verify deployment topology (legacy-present vs greenfield) explicitly in M6 Phase 1 Alpha kickoff."
- **Rationale**: Both A-007 positions agreed in R2 compromise; resolves SPLIT verdict.
- **Risk**: Low (procedure clarification)

#### Change #15 — Multi-AZ explicit for Postgres + Redis (A-001 resolution)

- **Source**: A-001 resolution (multi-AZ added)
- **Target**: V2 M1 D1.5 (Redis) + new D1.x (PG multi-AZ)
- **Approach**: amend D1.5 to specify Redis multi-AZ deployment; add new D1.x "PostgreSQL multi-AZ deployment with synchronous standby for SOC2 fault-tolerance evidence"
- **Rationale**: Both advocates accept multi-AZ as v1.0 requirement.
- **Risk**: Medium (infra cost increase but SOC2-defensible)

#### Change #16 — NTP/clock-drift monitoring (A-002 resolution)

- **Source**: A-002 resolution
- **Target**: V2 cross-cutting Observability section
- **Approach**: add alert spec: "Pod-clock-drift alert: warn when pod-to-pod drift exceeds 2s (early warning before JWT 5s skew tolerance is breached)"
- **Rationale**: Both advocates QUALIFY; add monitoring deliverable.
- **Risk**: Low (observability addition)

### V2-only contributions retained as-is

#### Change #17 — Confirm V2's admin endpoint, concurrent-registration AC, auto-login, SendGrid hardening

- These are preserved from V2 base. Listed here for transparency:
  - D4.7 admin audit query endpoint
  - M2 AC #9 concurrent-registration race handling
  - D2.2 auto-login on registration
  - D4.5 SendGrid SPF/DKIM/DMARC + Gmail/Outlook deliverability hardening
- **Risk**: None (existing in base)

#### Change #18 — Pagination ordering invariant for admin endpoint (INV-011 MEDIUM)

- **Source**: invariant-probe.md INV-011
- **Target**: V2 M4 D4.7
- **Approach**: add to D4.7: "Pagination uses keyset cursor on `(timestamp DESC, id DESC)` with explicit `LIMIT 100` cap (max 500). No OFFSET pagination on large tables."
- **Rationale**: INV-011 MEDIUM — deep pagination on 100M+ row table needs ordering invariant.
- **Risk**: Low (API design detail)

---

## Changes NOT Being Made (transparency — V1 approaches considered and rejected)

### Rejected #1 — V1's reset-token PostgreSQL table

- **V1 approach**: D3.1 `reset_tokens` table with `user_id FK, expires_at, used_at nullable`
- **Why rejected**: V2's Redis-with-TTL is more elegant for a 1-hour ephemeral artifact. Audit chain lives in `audit_log` not in operational reset-token store (see C-002 R2 V1 concession). V1's concern about durability is moot — losing a reset token forces user to request again, which is acceptable.
- **Confidence**: 80% (V1 R2 conceded)

### Rejected #2 — V1's 5-milestone scaffold (merge M1 + M2)

- **V1 approach**: M1 ships schema + audit + register/login + lockout in one 3-week milestone
- **Why rejected**: V1's M1 has 8 deliverables and 7 ACs in 3 weeks — highest schedule-slip risk. V2's split (M1 infra 2w + M2 auth-core 2w) gates infra readiness before service logic. V1 R2 conceded this point.
- **Confidence**: 75%

### Rejected #3 — V1's Redis-from-M1 lockout backend choice

- **V1 approach**: Lockout counter in Redis from M1 ("Counter accuracy is a SOC2 control")
- **Why rejected**: V2's PG-column approach is equally valid IF atomic-UPDATE is specified (Change #5 handles this). Avoids M1 Redis dependency. Lighter M1.
- **Confidence**: 70% (close — could go either way; V2 R2 conceded atomicity gap which removed V1's primary objection)

### Rejected #4 — V1's pen-test as single M4-parallel milestone

- **V1 approach**: Full pen-test in M4 with 1-week cure time
- **Why rejected**: Pen-testing against incomplete frontend undermines coverage (V2 R1 critique). Change #7 adopts hybrid split instead.
- **Confidence**: 78%

---

## Risk Summary

| Change | Risk | Impact if Wrong | Rollback Path |
|---|---|---|---|
| #1 Sequencing Rationale | Low | Minor (cosmetic section) | Delete section |
| #2/#3/#12/#13 Constant-time mechanisms + dummy hash | Low | Re-introduces timing oracle | Revert to V2's outcome-only ACs |
| #4 OQ-7 + schema flag | Medium | M1 schema migration cost if reverted | Roll forward with view-based split |
| #5 Atomic lockout | Medium | Wrong SQL pattern would break lockout | Revert to SELECT FOR UPDATE pattern |
| #6 Key-rotation runbook | Low | Process doc only | Defer drill to v1.1 |
| #7 Pen-test split | Medium | M4 capacity overrun | Combine back into M5 |
| #8 Per-email rate limit | Low | Config change | Revert to per-IP only |
| #9 Admin RBAC minimal | Medium | Admin endpoint privilege-escalation surface | Drop admin endpoint to v1.1 |
| #10 Audit-row for drops | Medium | Information leak if implemented wrong | Drop admin endpoint, revert to V1's "DB-direct" |
| #11 Redis isolation | Medium | Operational complexity | Single Redis with memory caps |
| #14 Legacy/greenfield branch | Low | Procedure clarification | Revert to "rollback to legacy" without branch |
| #15 Multi-AZ | Medium | Infra cost | Single-AZ with documented SOC2 risk acceptance |
| #16 NTP monitoring | Low | Observability gap | Defer to v1.1 |
| #17 V2 retained | None | (preserved as-is) | N/A |
| #18 Pagination ordering | Low | API design detail | Default ordering |

---

## Review Status

- **Mode**: Non-interactive (no `--interactive` flag)
- **Auto-approved**: Yes
- **Timestamp**: 2026-05-22T18:11:00Z

**Note on convergence-blocked status**: Per `invariant-probe.md` gate, 8 HIGH UNADDRESSED items existed before this refactor plan. Changes #2, #5, #9, #10, #11, #12, #13 collectively address INV-001, INV-004, INV-005, INV-007, INV-009, INV-012, INV-013, INV-014. INV-002 addressed by Change #4. The remaining HIGH item (none) — all 8 HIGH-severity items now have planned fixes. MEDIUM items (INV-003, INV-006, INV-008, INV-011, INV-015, INV-016) partially addressed (INV-011 via Change #18). The merged output should still flag unresolved items in its Open Questions section and the return contract's `unaddressed_invariants` field will reflect the post-merge state.
