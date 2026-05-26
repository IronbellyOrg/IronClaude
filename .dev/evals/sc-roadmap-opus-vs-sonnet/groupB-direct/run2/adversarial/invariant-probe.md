# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder probed the emerging consensus across 5 categories (state_variables, guard_conditions, count_divergence, collection_boundaries, interaction_effects) for hidden assumptions and boundary-condition failures.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | C5 mandates `PasswordHasher.verify` against a constant dummy hash on miss, but the dummy hash itself must persist as a stable cross-pod constant. Neither variant specifies where it lives, how it's seeded, or whether a per-pod fresh-hash on boot violates the constant-time invariant | UNADDRESSED | HIGH | V1 L87 R-002 mitigation specifies technique but not storage; V2 has no mention; consensus C5 inherits V1's gap |
| INV-002 | guard_conditions | C6/OQ-7 retention conflict resolution defers to M5 evidence pack, but M1 ships an audit-log schema on Day 1. If M5 chooses "split tables", the M1 schema must already partition SOC2-relevant subset vs operational, otherwise M5 requires destructive schema migration on production audit data | UNADDRESSED | HIGH | V1 OQ-7 L462 says "needed by M5" but D1.1 L53 already specifies single-table partition-by-month; reconciliation cost not budgeted |
| INV-003 | state_variables | C3 (DB-unique-constraint race) AC #9 says "first wins, second gets 409". The 409 path must also emit an audit event for the *losing* registration_attempt — otherwise enumeration via deliberate race becomes invisible to SOC2 logs | UNADDRESSED | MEDIUM | V2 D2.2 L84 emits on success path; V2 AC #7 L100 lists outcomes but doesn't tie losing-race rows to a specific outcome code |
| INV-004 | interaction_effects | C2 admin audit-log endpoint (`GET /admin/audit-logs`) lands in V2's M4, which is **before** the M5/M6 admin-role enforcement scope. The endpoint requires "admin role" gating (V2 D4.7) but RBAC enforcement is explicitly out of scope (V2 L308: "RBAC enforcement... v1.1+"). Admin endpoint without admin-role enforcement = privilege-escalation surface | UNADDRESSED | HIGH | V2 D4.7 L193 requires "admin role"; V2 L308 RBAC v1.1+; gating cannot be implemented if RBAC deferred |
| INV-005 | collection_boundaries | A-003 sliding-vs-fixed lockout window is UNSTATED but C5 requires constant-time defense across window boundary. At T+15min, fixed window resets counter; 6th attempt at T+14:59 hits lockout but at T+15:01 hits `PasswordHasher.verify`. The latency cliff at the boundary IS an enumeration timing oracle | UNADDRESSED | HIGH | Diff A-003 flags UNSTATED in both variants; C1 unresolved makes it unimplementable |
| INV-006 | guard_conditions | C4 SendGrid SPF/DKIM/DMARC hardening scoped before beta, but reset-token TTL is 1 hour. If DKIM key rotation occurs during a reset session's 1-hour window, in-flight reset emails fail validation at receiver — token still valid in Redis, but user can't retrieve link. No coordination between DKIM rotation and reset-token TTL specified | UNADDRESSED | MEDIUM | V2 L224 mentions DKIM pre-warming but not rotation cadence; V1 doesn't mention DKIM |
| INV-007 | state_variables | C5 always-enqueue email job for reset means unregistered-email requests enqueue jobs that the worker must silently drop. The drop must NOT emit `password_reset_requested` to audit log (would create registered-email oracle via audit query) — but request-side audit log IS emitted on every request. Either the worker correlates back to suppress the audit row, or admin audit query (U-010) becomes an enumeration oracle | UNADDRESSED | HIGH | V1 L174 emits reset-requested on every request; V2 D4.7 admin query exposes by user_id — admins querying "no audit row" vs "audit row" infers registration |
| INV-008 | count_divergence | M1 partitions audit log by month with 90-day drop (V1). If partition drop runs at month boundary and SOC2 requires "minimum 90 days", actual retention is 90-120 days, never exactly 90 — read as "≥90 days" the policy holds; read as "exactly 90 days" it doesn't | UNADDRESSED | MEDIUM | V1 D1.1 L53 says "90-day retention policy (partitioned by month)"; V1 L84 drops "older than 90 days" — month-granularity makes actual retention 90-120 days |
| INV-009 | interaction_effects | C3 + C1 interaction: if lockout counter lives in Redis (V1) but `users.failed_login_count` is also written (V2), Redis-down means lockout counter is lost on next login. C-001 still UNRESOLVED but C3 race-handling AC was conceded — the conceded AC depends on the unresolved storage choice | UNADDRESSED | HIGH | Diff X-002 L44 notes the storage backend conflict; C1 unresolved but C3 conceded |
| INV-010 | guard_conditions | Both variants set `/auth/refresh` rotation-on-refresh (M2/M3). C3 race-handling was scoped to registration only. Same race exists for refresh: two tabs refresh simultaneously, V2 RR-1 acknowledges with WATCH/MULTI, V1 R-007 with MULTI/EXEC — but neither was promoted to consensus item | ADDRESSED | LOW | V1 L152 R-007 + V2 RR-6 L392 — both variants address it in risk registers; flagged for promotion to acceptance criteria |
| INV-011 | collection_boundaries | C2 admin audit-log query returns paginated results, but neither variant specifies max page size or default ordering. With 12-month retention × high-traffic = potentially 100M+ rows. Without explicit LIMIT cap and tie-breaker on `(timestamp, id)`, deep pagination causes inconsistent results when audit events arrive during paging | UNADDRESSED | MEDIUM | V2 D4.7 L193 says "paginated" but no page-size cap; V2 RR-3 L222 mentions 5-second timeout but not ordering invariants |
| INV-012 | state_variables | C5 "always enqueue email job" requires the job queue to outlive process restart. V1 D3.4 uses BullMQ on Redis. If Redis is same instance as lockout/refresh-token store, a Redis OOM caused by reset-spam fills memory used by lockout counters — DoS on reset endpoint cascades into lockout bypass | UNADDRESSED | HIGH | V1 L186 D3.4 colocates BullMQ on Redis; V1 lockout on Redis per OQ-3; V1 D1.5 has 1GB allocation with no key-namespace isolation |
| INV-013 | interaction_effects | C5 dummy-hash defense for unknown email skips DB user lookup, but lockout counter increment requires keying by something. If keyed by submitted email → attacker can lock out arbitrary accounts by knowing the email. If keyed by IP → NAT'd users share lockout state (A-004). Consensus doesn't pick a key strategy | UNADDRESSED | HIGH | V1 L86-87 doesn't specify lockout key; V2 D1.1 L37 implies email; A-004 flags NAT issue |
| INV-014 | guard_conditions | C5 specifies "6th attempt is rejected without invoking `PasswordHasher.verify`" (V1 L66). But constant-time invariant requires response timing to match the unknown-email-with-verify path. Skipping verify on 6th attempt is FASTER than the unknown-email-with-dummy-verify path → newly distinguishable timing oracle: locked accounts respond faster than unknown emails | UNADDRESSED | HIGH | V1 L66 acceptance criterion creates the contradiction: "rejected without invoking `PasswordHasher.verify` (defense against timing oracle)" — but the defense creates a new oracle |
| INV-015 | count_divergence | C5 reset request "always enqueue email job" + V2 D4.3 "rate limited at 3 req/min per IP". A queue backlog from real reset traffic creates different request-side latency for queued-vs-immediate enqueue. The "constant time" is constant only when queue is unsaturated | UNADDRESSED | MEDIUM | V2 D4.3 L189 + V1 L218 — neither addresses queue-depth-induced timing variance |
| INV-016 | state_variables | C2 admin audit endpoint reads from `auth_audit_log`, but C6/OQ-7 may split tables. If split happens after admin endpoint is built (V2 M4), endpoint must be retrofitted to query union-of-tables, or admin users see only one slice post-split. No consensus on ordering between OQ-7 resolution and admin endpoint | UNADDRESSED | MEDIUM | V2 D4.7 in M4 L193; V1 OQ-7 resolution in M5 L462; admin endpoint built before retention resolution = guaranteed rework |

---

## Summary

- **Total findings**: 16
- **ADDRESSED**: 1 (INV-010 at LOW, flagged for promotion)
- **UNADDRESSED**: 15
  - **HIGH**: 8 (INV-001, INV-002, INV-004, INV-005, INV-007, INV-009, INV-012, INV-013, INV-014)
  - **MEDIUM**: 6 (INV-003, INV-006, INV-008, INV-011, INV-015, INV-016)
  - **LOW**: 0

## Convergence Gate Decision

Per `invariant_probe_gate`: convergence requires `count(HIGH + UNADDRESSED) == 0`. **Currently 8 HIGH UNADDRESSED items.**

**Status: BLOCKED_BY_INVARIANTS**

At `--depth standard`, max rounds reached. No Round 3 will execute. Per FR-006 `no_convergence`:

- Force-select by combined score (Step 3)
- Document non-convergence
- Flag for user review via `unaddressed_invariants` in return contract
- Promote HIGH UNADDRESSED items to refactor-plan as **must-address** acceptance criteria additions

## Top-Priority Items for Refactor Plan

1. **INV-014** (constant-time defense self-contradicts) — locked-account response faster than unknown-email-with-dummy-verify creates a new oracle. **Fix:** lockout-rejected response path must execute the dummy-hash verify before returning to maintain timing parity.
2. **INV-004** (admin endpoint without RBAC) — `GET /admin/audit-logs` requires admin role but RBAC is v1.1+. **Fix:** either drop admin endpoint to v1.1, OR pull minimal admin-role enforcement (single `isAdmin` claim in JWT, hardcoded admin emails seeded at M1) into v1.0.
3. **INV-009** (C3 conceded but depends on C-001 unresolved) — race-handling AC pre-supposes storage choice not resolved. **Fix:** decide C-001 first (atomic-UPDATE on Postgres OR Redis INCR); race-handling AC inherits the choice.
4. **INV-007** (admin endpoint = enumeration oracle via audit-log absence) — combining always-enqueue with admin audit query exposes registration status via audit-row presence/absence. **Fix:** worker must also emit a `password_reset_requested` audit row for dropped (unregistered-email) requests so audit-log absence ≠ unregistered.
5. **INV-012** (single-Redis cascade) — reset-spam OOM on Redis can collapse lockout counters. **Fix:** isolate BullMQ on separate Redis instance OR explicit memory-budget per key namespace with hard caps.
6. **INV-001** (dummy-hash provisioning unspecified) — per-pod boot-time hash creation violates constant-time invariant cross-pod. **Fix:** dummy hash is a config constant seeded at build/deploy time, identical across pods.
7. **INV-002** (audit-log schema choice before OQ-7 resolution) — M1 schema commits before M5 SOC2 evidence review. **Fix:** ship M1 schema with optional `soc2_relevant BOOLEAN` flag so M5 can derive split-tables-view without destructive migration.
8. **INV-005** (window-boundary timing oracle) — fixed-window reset creates latency cliff at T+15min. **Fix:** sliding-window via Redis sorted-set of failure timestamps, OR explicit AC that lockout-rejected response time matches `PasswordHasher.verify` regardless of window state.
