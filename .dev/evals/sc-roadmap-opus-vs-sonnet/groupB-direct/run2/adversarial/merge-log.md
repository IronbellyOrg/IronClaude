# Merge Log

## Metadata

- **Base variant**: `variant-2-sonnet-architect.md` (450 lines, 6-milestone scaffold)
- **Source variants for merged content**: `variant-1-opus-architect.md` (484 lines, 5 milestones)
- **Invariant probe source**: `invariant-probe.md` (16 findings, 8 HIGH UNADDRESSED at gate)
- **Refactor plan**: `refactor-plan.md` (18 planned changes)
- **Merged output**: `/config/workspace/IronClaude/.dev/eval-roadmap/groupB-direct/run2/merged-output.md`
- **Changes planned**: 18
- **Changes applied**: 18
- **Changes failed**: 0
- **Changes skipped**: 0
- **Status**: APPLIED
- **Timestamp**: 2026-05-22T18:30:00Z
- **Reviewer**: merge-executor agent (non-interactive auto-approve)

---

## Per-Change Execution Log

### Change #1 — Sequencing Rationale section

- **Status**: APPLIED
- **Source**: V1 L476-484
- **Target**: New final H2 section in merged output (before close)
- **Before**: V2 base had no sequencing rationale section
- **After**: New "## Sequencing Rationale (architect's note)" section added with 6 numbered points; V1→V2 milestone numbers translated (V1 M1-Redis-lockout → V2 M2-atomic-lockout; V1 M2-contract-freeze → V2 M3 D3.9; V1 M4-pen-test → V2 M4-backend-pen-test + M5-frontend-pen-test; V1 M5-rollout → V2 M6)
- **Provenance tag**: `<!-- Source: V1 Opus, L476-484 — merged per Change #1 -->`
- **Risk realized**: None

### Change #2 — Constant-time login defense (mechanism)

- **Status**: APPLIED
- **Source**: V1 L66, V1 L87
- **Target**: V2 M2 D2.1, new D2.2, M2 AC list
- **Before**: V2 D2.1 said "returns generic 401 for wrong password, unknown email, and locked accounts (no enumeration)" — outcome only, no mechanism
- **After**: New D2.2 "Constant-time defense module" with explicit dummy-hash verify on unknown-email AND lockout-rejected paths; M2 AC #2 requires identical p95 latency (±20ms) across all 401 paths; D2.8 timing-parity test added
- **Provenance tag**: `<!-- Changes #2, #12, #13: constant-time + dummy-hash + boundary parity (INV-001, INV-005, INV-014) -->`
- **Risk realized**: None (additive)

### Change #3 — Constant-time reset defense (mechanism)

- **Status**: APPLIED
- **Source**: V1 L218 + INV-007
- **Target**: V2 M4 D4.1, D4.5
- **Before**: V2 D4.1 returned "identical success response... no email sent" creating timing oracle
- **After**: D4.1 now "always enqueues email job in `redis-queue` BullMQ regardless of registration status"; worker silently drops unregistered-email send step but ALWAYS emits audit row; identical 200 response p95 ≤ 200ms regardless of registration status
- **Provenance tag**: `<!-- Change #3 + Change #10: always-enqueue + audit-row parity (INV-007) -->`
- **Risk realized**: None

### Change #4 — OQ-7 PRD-vs-TDD retention conflict + schema flag

- **Status**: APPLIED
- **Source**: V1 L462 (OQ-7), invariant-probe INV-002
- **Target**: V2 Open Questions table, V2 M1 D1.2 schema
- **Before**: V2 D1.2 had "12-month retention policy" with no flag column; OQ table did not mention TDD §7.2 90-day conflict
- **After**: D1.2 adds `soc2_relevant BOOLEAN DEFAULT TRUE` column; partitioned by month; 12-month default with 90-day operational subset as derived view; new OQ row `OQ-PRD-TDD-1` documents resolution
- **Provenance tag**: `<!-- Change #4: OQ-7 retention conflict resolution + schema flag (INV-002) -->`
- **Risk realized**: None (resolution documented, no destructive migration required)

### Change #5 — Lockout counter atomicity

- **Status**: APPLIED
- **Source**: V1 R-008 + V2 R2 concession
- **Target**: V2 M2 D2.1, M2 AC list, D2.9 integration test
- **Before**: V2 D2.1 said "increments failed_login_count; at >=5 failures within 15 min sets locked_until" with no atomicity guarantee
- **After**: D2.1 now specifies single-statement atomic UPDATE SQL with CASE for locked_until; AC #4 mandates concurrent-pod lockout proof; D2.9 integration test enforces 10-parallel-pod CI check
- **Provenance tag**: `<!-- Change #5: atomic-UPDATE lockout (INV-009, INV-013) -->`
- **Risk realized**: None

### Change #6 — Quarterly RS256 key-rotation runbook + drill

- **Status**: APPLIED
- **Source**: V1 D2.7, D5.7
- **Target**: V2 M3 new D3.8, V2 M6 D6.2 + D6.6
- **Before**: V2 D2.6 said "key rotation documented for quarterly cadence" but no runbook deliverable or drill
- **After**: New D3.8 "RS256 key-rotation runbook with quarterly cadence; key-access audit log; in-memory tmpfs"; D6.2 includes "first RS256 key-rotation drill executed and audit-logged"; D6.6 includes key rotation procedure with first drill in Phase 1 Alpha
- **Provenance tag**: `<!-- Change #6 -->`
- **Risk realized**: None

### Change #7 — Pen-test split (backend M4 + frontend M5)

- **Status**: APPLIED
- **Source**: V1 R-010 + V2 R2 compromise
- **Target**: V2 M4 new D4.10, V2 M5 D5.7 scope narrowed
- **Before**: V2 D5.7 was single penetration test covering all surface in M5; V2 had no M4 pen-test
- **After**: New D4.10 "Backend penetration test report" as M4 completion gate (RS256, lockout, timing oracles, atomic-UPDATE, admin RBAC, password storage, rate limit); D5.7 narrowed to frontend (XSS, CSRF, AuthProvider redirect loop, token storage); 1-week buffer reserved in M5
- **Provenance tag**: `<!-- Change #7: pen-test split -->`
- **Risk realized**: M4 capacity flagged in risk table; mitigation = pen-test in final 3 days with 1-week M5 buffer

### Change #8 — Per-email rate limit explicit

- **Status**: APPLIED
- **Source**: V1 R-002 + A-004 resolution
- **Target**: V2 M2 D2.5
- **Before**: V2 D2.5 said "rate limited at 10 req/min per IP at API Gateway"
- **After**: D2.5 now "rate limited at 10 req/min per IP AND 5 req/min per email at API Gateway (per-email is primary; per-IP guards against credential-stuffing across accounts; per-email lockout is the primary defense and acknowledges A-004 NAT false-positive concern)"; AC #11 added
- **Provenance tag**: `<!-- Change #8 -->`
- **Risk realized**: None

### Change #9 — Admin endpoint RBAC v1.0 minimal enforcement (INV-004)

- **Status**: APPLIED
- **Source**: invariant-probe INV-004
- **Target**: V2 M1 D1.1 (schema), new D1.10 (seed), V2 M3 D3.1/D3.5 (JWT claim), V2 M4 D4.7 (guard)
- **Before**: V2 D1.1 had no isAdmin column; V2 D4.7 said "requires admin role" but RBAC was v1.1+ — privilege-escalation surface
- **After**: D1.1 adds `isAdmin BOOLEAN DEFAULT FALSE`; new D1.10 "Admin bootstrap seed" via migration; D3.1 issueTokens includes isAdmin; D3.5 /me returns isAdmin; D4.7 guard enforces `isAdmin=true` claim or 403; D4.8 integration test verifies
- **Provenance tag**: `<!-- Change #9: minimal admin enforcement (INV-004) -->`
- **Risk realized**: None; full RBAC framework remains v1.1+

### Change #10 — Worker emits audit row for dropped reset requests (INV-007)

- **Status**: APPLIED
- **Source**: invariant-probe INV-007
- **Target**: V2 M4 D4.5
- **Before**: V2 D4.5 SendGrid module had no audit-emission requirement for dropped jobs
- **After**: D4.5 now "worker emits `password_reset_requested` audit row for ALL incoming requests (including unregistered-email drops) with non-user-correlatable `request_id` payload"; AC #2 enforces audit row written for unregistered emails; D4.8 integration test verifies
- **Provenance tag**: `<!-- Change #3 + Change #10: always-enqueue + audit-row parity (INV-007) -->`
- **Risk realized**: RR-11 added (audit row could become oracle if request_id is correlatable — mitigated by opaque UUID requirement)

### Change #11 — Redis isolation for BullMQ queue (INV-012)

- **Status**: APPLIED
- **Source**: invariant-probe INV-012
- **Target**: V2 M1 D1.5
- **Before**: V2 D1.5 was "Redis 7+ cluster provisioned with TLS, 1 GB initial allocation" — single Redis for all use cases
- **After**: D1.5 now "two logically-isolated namespaces: `redis-session` (refresh tokens + lockout counters) and `redis-queue` (BullMQ reset-email queue). Implementation may be two Redis instances OR single instance with explicit maxmemory-policy per key-prefix + monitoring alert when queue keys exceed 30% of allocation. Memory-budget documented per namespace."
- **Provenance tag**: `<!-- Change #11: Redis isolation (INV-012); Change #15: multi-AZ -->`
- **Risk realized**: None

### Change #12 — Dummy hash provisioned at build time (INV-001)

- **Status**: APPLIED
- **Source**: invariant-probe INV-001
- **Target**: V2 M1 new D1.9, V2 M2 D2.2
- **Before**: No mention of dummy hash provenance in V2
- **After**: New D1.9 "Dummy-hash constant provisioned at build/deploy time as stable cross-pod config artifact (NOT per-pod boot-time hash); stored in secret store alongside RSA keys; rotated only deliberately"; M1 AC #6 verifies identical hash across pods; D2.2 references DUMMY_HASH_CONSTANT from D1.9
- **Provenance tag**: `<!-- Change #12: dummy hash provisioning (INV-001) -->`
- **Risk realized**: None

### Change #13 — Sliding-window lockout OR window-boundary timing parity (INV-005)

- **Status**: APPLIED (Option B chosen per refactor plan recommendation)
- **Source**: invariant-probe INV-005, diff A-003
- **Target**: V2 M2 D2.2
- **Before**: No mention of window-boundary timing in V2
- **After**: D2.2 includes "(e) Option B for v1.0: fixed-window lockout with explicit AC that lockout-rejected response time MUST match dummy-verify duration regardless of window state (sliding-window upgrade deferred to v1.1)"; M2 AC #2 enforces ±20ms p95 across all 401 paths including lockout
- **Provenance tag**: `<!-- Changes #2, #12, #13: constant-time + dummy-hash + boundary parity (INV-001, INV-005, INV-014) -->`
- **Risk realized**: None

### Change #14 — Legacy-vs-greenfield rollback branching (A-007)

- **Status**: APPLIED
- **Source**: V1 A-007 REJECT + V2 R2 compromise
- **Target**: V2 M6 D6.5
- **Before**: V2 D6.5 was "Rollback procedure tested in staging: disable AUTH_NEW_LOGIN -> verify legacy flow operational"
- **After**: D6.5 now branched — (a) Legacy-present branch: disable flag → verify legacy → smoke test → time elapsed; (b) Greenfield branch (no legacy): flag-off blast-radius test → confirm 503 for all `/auth/*` cleanly; topology declared at Phase 1 kickoff (D6.2 added); RR-8 mitigation updated
- **Provenance tag**: `<!-- Change #14 (A-007) -->`
- **Risk realized**: None

### Change #15 — Multi-AZ explicit for Postgres + Redis (A-001 resolution)

- **Status**: APPLIED
- **Source**: A-001 resolution
- **Target**: V2 M1 D1.5 (Redis), new D1.8 (Postgres multi-AZ)
- **Before**: V2 D1.5 didn't specify Redis multi-AZ; no Postgres multi-AZ deliverable
- **After**: D1.5 amended "Redis 7+ provisioning (multi-AZ)"; new D1.8 "PostgreSQL multi-AZ deployment with synchronous standby for SOC2 fault-tolerance evidence"; M1 AC #7 verifies multi-AZ failover within 60s; M1 risk table notes cost concern
- **Provenance tag**: `<!-- Change #15: Multi-AZ Postgres -->` and inline in D1.5
- **Risk realized**: Infra cost noted in M1 risks; SOC2-defensible

### Change #16 — NTP/clock-drift monitoring (A-002 resolution)

- **Status**: APPLIED
- **Source**: A-002 resolution
- **Target**: V2 cross-cutting Observability section
- **Before**: V2 had no clock-drift alerting
- **After**: Observability bullet added: "pod-clock-drift alert: warn when pod-to-pod drift exceeds 2 seconds (early warning before JWT 5s skew tolerance is breached)"; Assumption #11 added
- **Provenance tag**: `<!-- Source: Base (V2 Sonnet) + Change #16: NTP/clock-drift monitoring -->`
- **Risk realized**: None

### Change #17 — V2-only contributions retained as-is

- **Status**: APPLIED (preserved verbatim with provenance comment)
- **Source**: V2 base
- **Target**: D4.7 admin audit query endpoint (modified by Change #9/#18 not removed); D2.3 register concurrent-registration AC; D2.3 auto-login on registration; D4.5 SendGrid SPF/DKIM/DMARC
- **Before / After**: Preserved structure; transparency-only entry
- **Provenance tag**: `<!-- Source: Base (V2 Sonnet) -->` on retained sections
- **Risk realized**: None

### Change #18 — Pagination ordering invariant for admin endpoint (INV-011 MEDIUM)

- **Status**: APPLIED
- **Source**: invariant-probe INV-011
- **Target**: V2 M4 D4.7
- **Before**: V2 D4.7 said "paginated results" with no page-size cap or ordering invariant
- **After**: D4.7 now "keyset cursor pagination on `(timestamp DESC, id DESC)` with explicit LIMIT default 100, max 500; no OFFSET pagination on large tables"; D4.8 integration test verifies deterministic ordering under concurrent inserts
- **Provenance tag**: `<!-- Change #18: keyset pagination (INV-011) -->`
- **Risk realized**: None

---

## Post-Merge Validation Results

### 1. Structural Integrity

- **Status**: PASS
- **Heading hierarchy**: Consistent (H1 title → H2 sections → H3 milestones M1-M6 → H4 N/A); no orphans
- **Milestone numbering**: Sequential M1-M6, no gaps
- **Section ordering**: Executive Summary → Milestones → Cross-Cutting Concerns → Risk Register → Definition of Done → Open Questions → Sequencing Rationale (V1 contribution appended last per Change #1)
- **YAML frontmatter**: Updated with merged ID, title, source, generated_by, generated_at, version, target_release, soc2_audit_deadline

### 2. Internal Reference Resolution

- **Status**: PASS
- **Milestone references**: M1-M6 all resolve (no orphan M0 or M7)
- **Deliverable references**: D1.1-D1.10, D2.1-D2.9, D3.1-D3.12, D4.1-D4.10, D5.1-D5.7, D6.1-D6.9 all defined in their respective milestones; cross-milestone references (e.g., D4.7 → D1.10, D3.5) resolve
- **Risk register references**: RR-1 through RR-13 defined; RR-9 through RR-13 newly introduced for merge changes
- **Open Questions references**: OQ-PRD-1 through OQ-PRD-4, OQ-TDD-1 through OQ-TDD-2, and new OQ-PRD-TDD-1 all present
- **Invariant references**: INV-001, INV-002, INV-004, INV-005, INV-007, INV-009, INV-011, INV-012, INV-013, INV-014 referenced in provenance comments and AC text; INV-010 promoted to D3.11 / M3 AC #12

### 3. Contradiction Re-Scan

- **Status**: PASS (no new contradictions introduced)
- **Verified**:
  - Lockout storage: V2's PG-column approach retained; atomic-UPDATE pattern resolves V1's "Redis-from-M1" concern (Change #5). No dual-store contradiction.
  - Retention: Single source of truth (12-month default + `soc2_relevant` flag for derived view); resolves PRD-vs-TDD §7.2 conflict (Change #4).
  - Admin endpoint: D4.7 RBAC enforcement now consistent with v1.0 scope via minimal isAdmin column (Change #9); no longer self-contradictory.
  - Timing parity: Single dummy-verify policy applies to unknown-email AND lockout-rejected paths (Change #2/#13); no faster-locked-vs-unknown oracle.
  - Pen-test: Backend (M4) and frontend (M5) clearly delineated; no overlap or gap (Change #7).

### 4. Invariant Probe Coverage

| ID | Severity | Status post-merge | Mechanism |
|----|----------|-------------------|-----------|
| INV-001 | HIGH | RESOLVED | Change #12 — D1.9 build-time dummy hash + M1 AC #6 |
| INV-002 | HIGH | RESOLVED | Change #4 — D1.2 `soc2_relevant` flag + OQ-PRD-TDD-1 |
| INV-003 | MEDIUM | PARTIAL | D2.3 emits race-loser registration_attempt audit row |
| INV-004 | HIGH | RESOLVED | Change #9 — D1.1 isAdmin + D1.10 seed + D3.1/D3.5 JWT claim + D4.7 guard |
| INV-005 | HIGH | RESOLVED (Option B) | Change #13 — D2.2 timing-parity AC across window state |
| INV-006 | MEDIUM | UNADDRESSED | DKIM rotation coordination — flagged for v1.1 |
| INV-007 | HIGH | RESOLVED | Change #3 + #10 — D4.1/D4.5 always-enqueue + audit-row for drops |
| INV-008 | MEDIUM | PARTIAL | Read as "≥90 days" per Change #4's soc2_relevant flag + month-partition |
| INV-009 | HIGH | RESOLVED | Change #5 — D2.1 atomic-UPDATE SQL pattern |
| INV-010 | LOW | PROMOTED TO AC | M3 D3.11 + AC #12 |
| INV-011 | MEDIUM | RESOLVED | Change #18 — D4.7 keyset pagination |
| INV-012 | HIGH | RESOLVED | Change #11 — D1.5 Redis namespace isolation |
| INV-013 | HIGH | RESOLVED | Change #5 — atomic UPDATE keyed by email (D2.1) + D2.2 lockout-key clarification |
| INV-014 | HIGH | RESOLVED | Change #2 — D2.2 dummy-verify on lockout-rejected path + AC #3 |
| INV-015 | MEDIUM | UNADDRESSED | Queue-saturation timing — flagged for v1.1 monitoring |
| INV-016 | MEDIUM | MITIGATED | Change #4's view-based split avoids destructive table-split retrofit |

**HIGH severity post-merge**: 0 UNADDRESSED (all 8 resolved)
**MEDIUM severity post-merge**: 2 UNADDRESSED (INV-006, INV-015), 2 PARTIAL (INV-003, INV-008), 1 MITIGATED (INV-016), 1 RESOLVED (INV-011)
**Convergence gate**: WOULD-PASS post-merge (HIGH UNADDRESSED == 0)

---

## Summary

- **Planned**: 18
- **Applied**: 18
- **Failed**: 0
- **Skipped**: 0
- **HIGH invariants resolved**: 8 of 8
- **Structural integrity**: PASS
- **Internal references**: PASS
- **Contradiction re-scan**: PASS (no new contradictions)
- **Status**: SUCCESS

### Warnings / Items for User Attention

1. **MEDIUM-severity invariants remain unaddressed** (INV-006 DKIM rotation, INV-015 queue-saturation timing) — flagged for v1.1.
2. **Multi-AZ infra cost** (Change #15) flagged in M1 risk register; SOC2-defensible but cost-impact should be confirmed with platform team.
3. **M4 capacity** (Change #7 — backend pen-test added to M4) flagged in risk register; mitigation = pen-test in final 3 days + 1-week M5 buffer.
4. **Atomic-UPDATE SQL pattern** (Change #5) requires DB lead review; integration test enforced as CI gate (D2.9).
5. **Greenfield-vs-legacy deployment topology** must be declared at M6 Phase 1 kickoff (Change #14 / D6.2); user/PM should confirm which branch applies.
