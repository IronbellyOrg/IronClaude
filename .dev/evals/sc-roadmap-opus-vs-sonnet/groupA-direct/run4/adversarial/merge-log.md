# Merge Log

## Metadata

- **Base variant**: `variant-1-opus-default.md` (V1, opus default)
- **Incorporating from**: `variant-2-sonnet-default.md` (V2, sonnet default)
- **Invariant probe**: `invariant-probe.md` (Round 2.5)
- **Refactoring plan**: `refactor-plan.md` (14 planned changes)
- **Executor model**: opus (merge-executor)
- **Merge timestamp**: 2026-05-22T20:30Z
- **Merged output**: `/config/workspace/IronClaude/.dev/eval-roadmap/groupA-direct/run4/merged-roadmap.md`
- **Status**: SUCCESS — 14 of 14 changes applied; post-merge validation PASS

## Changes Applied

### Change #1 — Per-user concurrent session cap (V2 D2.5 → new D3.7)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D2.5 — merged per Change #1 -->` (inline at D3.7)
- **Before**: V1 M3 had D3.1-D3.6; no per-user session cap
- **After**: Added D3.7 — configurable cap default=5, oldest-eviction on N+1, emits `auth.session.evicted` audit event (links to D6.4 taxonomy); eviction kills only the leaf refresh token (resolves INV-013 interaction with V1 family-tracking)
- **Validation**: Internal references resolve (D6.4, D3.1); edge-case block updated; exit criteria mentions N=5→N=6 verification

### Change #2 — Kubernetes deployment specifics (V2 D7.4 → V1 D7.6 restructured)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D7.4 — combined with V1 multi-AZ baseline per Change #2 -->`
- **Before**: V1 D7.6 = "Multi-AZ production deploy ≥2 AZs, RDS multi-AZ, Redis replication group; chaos test killing one AZ confirms <30s RTO"
- **After**: D7.6 expanded to combine V1's multi-AZ + chaos test (NFR-005 verification) with V2's K8s manifests + HPA (min 3 / max 10 / CPU 70%) + PgBouncer + Redis Sentinel. Both layers preserved (additive, not replacement)
- **Validation**: NFR-005 chaos test retained; D3.6 ramp pattern re-run in prod-like topology preserved

### Change #3 — Redis WATCH/MULTI/EXEC atomicity (V2 D7.1 + R-008 → V1 D3.1)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D7.1/R-008 — merged per Change #3 -->`
- **Before**: V1 D3.1 = "POST /auth/refresh with token rotation (one-time-use refresh tokens, family tracking for reuse detection → invalidates entire family)" — no atomicity primitive
- **After**: D3.1 now specifies Redis `WATCH/MULTI/EXEC` wraps invalidate-old + issue-new atomically; family-tracking remains the defense-in-depth detection layer. Exit criteria adds explicit concurrent-refresh race test
- **Validation**: D3.1 still resolves all back-references (D6.2 password reset invalidation); R-011 mitigation updated to reference WATCH/MULTI/EXEC

### Change #4 — pgcrypto column-level encryption (V2 D6.8 → V1 D1.2)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D6.8 — merged into D1.2 per Change #4 -->`
- **Before**: V1 D1.2 schema migrations referenced only RDS at-rest encryption
- **After**: D1.2 explicitly adds pgcrypto column-encryption on `users.email` plus deterministic-encryption search-hash column for indexed lookup (addresses INV-016 scan-on-login concern); NFR-006 verification extended; D1.2 exit criteria adds pgcrypto extension installed
- **Validation**: R-004 mitigation column updated to cite pgcrypto on `users.email` (D1.2)

### Change #5 — Prometheus + Grafana alerts (V2 D7.2 → new D7.9)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D7.2 — merged per Change #5 as new D7.9 -->`
- **Before**: V1 M7 had no explicit alert-threshold deliverable (D1.6 mentioned OpenTelemetry only)
- **After**: D7.9 adds Prometheus metrics (p50/p95/p99 latency, error rate, sessions, rate-limit rejections, failed logins, outbox lag, hash-chain lag) and Grafana dashboards. Alert thresholds: error rate > 1%, p99 > 300ms, audit-write failures (any), outbox lag > 60s, JWKS 5xx > 0.1%
- **Validation**: NFR-005 (99.9% uptime detection) referenced; D7.8 launch gate adds D7.9 fault-injection verification

### Change #6 — Load-test ramp pattern (V2 D6.6 → V1 D3.6 + D7.6)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D6.6 — merged per Change #6 -->`
- **Before**: V1 D3.6 = "10,000 concurrent WebSocket-style polling clients holding sessions" — less prescriptive
- **After**: D3.6 specifies "ramp to 10,000 over 10 minutes, sustain for 30 minutes" (k6/Locust); V1's p95<200ms preserved, V2's p99<200ms added as stretch; D7.6 re-uses pattern in prod-like topology
- **Validation**: NFR-002 verification path retained

### Change #7 — Account deactivation lifecycle (V2 D5.6 + D5.7 → V1 D6.6 / D7.3)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D5.6/D5.7 — merged per Change #7 -->`
- **Before**: V1 D6.6 = "soft-delete + 30-day grace, then crypto-shred" — `deactivated_at` and login-query filter not explicit; no re-auth on DELETE
- **After**: D6.6 explicitly sets `users.deactivated_at = NOW()` immediately filtering account from login queries; 30-day grace + cancel-link email; hard-delete via crypto-shred per D7.3; `DELETE /me` requires re-authentication (current password OR active 2FA); audit-survival via D7.3 user-id tokenization preserved (V1's stronger mechanism per refactor-plan rationale)
- **Validation**: D6.6 exit criteria verifies `deactivated_at` filter blocks login within 1s; re-auth verified

### Change #8 — Edge-case validation suite (V2 D7.1 → new D7.10)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D7.1 — merged per Change #8 as new D7.10 -->`
- **Before**: V1 had per-milestone "Edge Cases Covered" blocks (S-002 winner) but no centralized final-gate suite
- **After**: D7.10 added as final integration-level regression suite (additive, not replacement); covers empty DB, single-user, max-load + audit writes simultaneously, token boundary, refresh race, OAuth malformed state, rate-limit boundary, session-cap eviction race, hash-chain genesis + Merkle verify. Per-milestone blocks retained as authoritative per-milestone exit gates
- **Validation**: D7.8 launch gate references D7.10 100% pass requirement

### Change #9 — `unverified` role added (V2 D4.1 → V1 D5.1)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D4.1 — merged per Change #9 -->`
- **Before**: V1 D5.1 seeded 4 roles (`admin`, `user`, `auditor`, `support`)
- **After**: D5.1 seeds 5 roles, adding `unverified` (default at registration; permission to verify email + nothing else). Upgrade to `user` on email verification. Operational taxonomy preserved
- **Validation**: M5 exit criteria updated to cover all 5 roles; M5 edge cases mention `unverified` privileged-action denial; R-007 mitigation references the gate

### Change #10 — Tech-stack default in Open Questions (V2 D1.3 → V1 Open Q #1)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet), D1.3 — merged per Change #10 -->`
- **Before**: V1 Open Q #1 = pure defer-to-team
- **After**: Open Q #1 retains the deferral but adds explicit default — "Python 3.12 + FastAPI" if no decision by Week 0; change requires Week 1 ADR refresh + 2-3 day slip warning. Prevents Open Question from stalling M1
- **Validation**: D1.1 still references "team choice ratified in Open Questions"; consistent

### Change #11 — Hash-chain specifics (INV-001 → V1 D6.5 expanded with a/b/c)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Base (modified) — Change #11 from invariant probe INV-001 -->`
- **Before**: V1 D6.5 = "append-only table audit_events with hash-chain (each row contains SHA-256 of prior row's canonicalized payload); daily export to S3 with object-lock" — genesis, canonicalization, and tip-publication unspecified
- **After**: D6.5 expanded with three sub-deliverables:
  - D6.5.a: deterministic genesis row (fixed payload, `prev_hash = SHA-256("")`, committed to source control + first daily export)
  - D6.5.b: JCS RFC 8785 canonicalization spec over stable fields; `pg_advisory_xact_lock` serializes hash-chain writes across multi-pod (resolves INV-007)
  - D6.5.c: daily Merkle tip publication to separate S3 bucket with Object Lock + optional public tip-feed for external verifiability
- **Validation**: M6 exit criteria adds tamper-detection test (payload-modify-after-fact fails Merkle verify); D7.7 runbook adds canonicalization spec + tip-publication procedure; M6 duration adjusted to "3-4 weeks (3.5 if Change #11 tracks to plan)" per schedule disclosure

### Change #12 — Audit outbox pattern (INV-017 → new D6.4.a)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Base (modified) — Change #12 from invariant probe INV-017 -->`
- **Before**: V1 D6.4/D6.5 assumed synchronous emit; INV-017 identified that async-after-commit violates FR-009 100%-capture
- **After**: D6.4.a added — auth handlers INSERT into `audit_outbox` inside the SAME transaction as the state change (at-least-once for FR-009); a durable worker drains outbox to immutable `audit_events` and feeds hash-chain writer. Latency budget: outbox INSERT < 10ms p99 inside request transaction; hash-chain materialization async without blocking response. Resolves FR-009 vs NFR-001 tradeoff
- **Validation**: M6 exit criteria adds outbox at-least-once injection test (process-crash between commit and worker drain); Success Criteria audit row references D6.4.a outbox

### Change #13 — S3 Object Lock + GDPR reconciliation (INV-019 → R-010 mitigation)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Base (modified) — Change #13 from invariant probe INV-019 -->`
- **Before**: R-010 mitigation = "Tokenize `user_id` in audit table; PII fields crypto-shredded at erasure while audit references survive; legal sign-off in D7.8" — did not address S3 Object Lock immutability vs GDPR
- **After**: R-010 mitigation column rewritten to specify: (a) S3 Object Lock applies ONLY to anonymized/tokenized audit records (post-D7.3 tokenization); (b) PII never enters immutable export — only tokenized user_id references; (c) PII fields remain in live PG `audit_events` table + live `users` row where crypto-shred can act; (d) immutable S3 export contains only hash chain + canonicalized payload over PII-free / tokenized fields; (e) metadata JSONB whitelisted at write time (no raw IP/UA/email in immutable export); legal sign-off captured in D7.8. All other R-010 columns (ID, Risk, Impact, Probability, Milestones) preserved unchanged
- **Validation**: Open Q #5 (audit retention) updated to cross-reference R-010 alignment

### Change #14 — OAuth callback two-cookie pattern (INV-002 → new D4.7)

- **Status**: APPLIED
- **Provenance tag**: `<!-- Source: Base (modified) — Change #14 from invariant probe INV-002 -->`
- **Before**: V1 M4 (D4.1-D4.6) did not address SameSite=Strict refresh cookie not being sent on top-level callback navigation from third-party OAuth provider
- **After**: D4.7 added — callback endpoint uses short-lived (5-min) SameSite=Lax `oauth_continuation` cookie OR server-side state→session-id Redis mapping to identify originating session; SameSite=Strict refresh cookie set only after first-party page return. Two-cookie pattern documented in OAuth runbook; explicit Safari + Firefox test
- **Validation**: M4 exit criteria adds two-cookie verification on Safari + Firefox; D4.7 dependency on D4.3 captured in Dependency Graph Explicit Blockers

## Post-Merge Validation

### Structural Integrity — PASS

- Heading hierarchy: H1 (1) → H2 (12) → H3 (7); no gaps, no orphan headings
- Section ordering preserved: Executive Summary → Goals → Milestones (M1-M7) → Dependency Graph → Risk Register → Open Questions → Out of Scope → Success Criteria
- V1's `---` separators between milestones preserved (7 separators between 7 milestones + closing one before Dependency Graph)
- All V1 milestone identifiers (M1-M7) preserved; no renumbering
- All V1 deliverable identifiers (D1.1-D7.8) preserved; new IDs added (D3.7, D4.7, D6.4.a, D6.5.a/b/c, D7.9, D7.10) without disturbing existing numbering

### Internal Reference Validation — PASS

Verified every D{M}.{N} cross-reference resolves to a defined deliverable:

- D6.4 (taxonomy) — referenced from D3.7 eviction event, D7.10 edge-case suite — RESOLVES
- D3.1 (refresh + WATCH/MULTI/EXEC) — referenced from D6.2, D7.10, R-011 — RESOLVES
- D6.4.a (outbox) — referenced from D6.5 dependency, M6 exit, Success Criteria, D7.10 — RESOLVES
- D6.5.a/b/c (hash-chain sub-deliverables) — referenced from D7.7 runbook, R-009 mitigation — RESOLVES
- D3.7 (session cap) — referenced from M3 exit, edge cases, R-002 mitigation — RESOLVES
- D4.7 (OAuth two-cookie) — referenced from M4 exit criteria, Dependency Graph — RESOLVES
- D7.9 (alerts) — referenced from D7.8 launch gate — RESOLVES
- D7.10 (edge-case suite) — referenced from D7.8 launch gate, Success Criteria implication — RESOLVES
- D7.3 (user_id tokenization) — referenced from R-010, D6.6, D6.5.b — RESOLVES

### Contradiction Re-Scan — PASS (no new contradictions introduced)

V1's clean baseline preserved + the following invariant-probe contradictions RESOLVED:

- INV-001 (hash-chain genesis/canonicalization/tip-publication) — RESOLVED by D6.5.a/b/c
- INV-002 (SameSite=Strict vs OAuth callback) — RESOLVED by D4.7 two-cookie pattern
- INV-017 (async audit write vs FR-009) — RESOLVED by D6.4.a outbox pattern
- INV-019 (S3 Object Lock vs GDPR crypto-shred) — RESOLVED by R-010 reconciliation
- INV-007 (hash-chain serialization under multi-pod K8s) — RESOLVED in D6.5.b via `pg_advisory_xact_lock`
- INV-013 (session-cap eviction × family-tracking interaction) — RESOLVED in D3.7 (eviction kills only the leaf)
- INV-016 (pgcrypto email → SCAN) — PARTIALLY RESOLVED in D1.2 via deterministic-encryption search-hash column (full validation deferred to D3.6 load test)
- INV-012 (tokenization timing) — RESOLVED in D7.3 ("user_id tokenization happens AT deactivation (t=0)")
- INV-008 (cookie hardening sufficiency) — PARTIALLY RESOLVED in D7.4 (no `unsafe-eval` + restrictive `Domain` attribute)

Remaining UNADDRESSED INV findings (out of refactor-plan scope; not introduced by merge):

- INV-003, INV-004, INV-005, INV-009, INV-010, INV-011, INV-015, INV-018, INV-020 — these were not selected by the refactor plan and are documented for follow-up backlog. They do not constitute NEW contradictions introduced by the merge.

### Schedule Disclosure — APPLIED

- M6 duration changed from "3 weeks" → "3-4 weeks (3.5 if Change #11 hash-chain sub-deliverables track to plan)"
- Dependency Graph Critical Path changed from "M1 → M2 → M3 → M5 → M6 → M7 (20 weeks)" → "20-21 weeks baseline; 22-23 weeks with merged scope"
- Executive Summary updated to reference 20-21 baseline / 22-23 with merged scope
- M7 envelope unchanged (Change #2 K8s scope absorbed within existing 5-week M7 duration per refactor-plan)

### Provenance Coverage — PASS

- Document header `<!-- Provenance: ... -->` block present at top with base/incorporating/invariant-probe/changes-applied/timestamp/executor
- Per-section provenance HTML comments present on every modified section (M1, M3, M4, M5, M6, M7, Dependency Graph, Risk Register, Open Questions)
- Unchanged sections explicitly tagged `<!-- Source: Base (original) -->` (Executive Summary, Goals & Success Metrics, M2, Out of Scope, Success Criteria)
- Inline per-change tags `<!-- Change #N: ... -->` at the point of each modification

## Summary

| Metric | Value |
|--------|-------|
| Planned changes | 14 |
| Applied | 14 |
| Failed | 0 |
| Skipped | 0 |
| Structural validation | PASS |
| Internal reference validation | PASS |
| Contradiction re-scan | PASS (no new contradictions; 6 INV findings RESOLVED, 2 PARTIALLY RESOLVED, remainder out-of-scope) |
| Provenance coverage | Complete (header + per-section tags + per-change inline tags) |
| File size | 298 lines / 4,673 words |
| Status | SUCCESS |
