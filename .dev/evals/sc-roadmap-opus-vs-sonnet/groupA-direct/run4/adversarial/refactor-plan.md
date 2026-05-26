# Refactoring Plan

## Overview

- **Base variant**: Variant 1 (opus default) — `variant-1-opus-default.md`
- **Incorporating from**: Variant 2 (sonnet default) — `variant-2-sonnet-default.md`
- **Total planned changes**: 14 (10 incorporations + 4 invariant-probe-derived fixes)
- **Total rejected changes**: 8 (V2 approaches the debate determined inferior)
- **Overall risk**: Medium — most changes are additive deliverables inside existing V1 milestones; INV-derived changes alter critical-path deliverables (D6.5 audit chain) but are scoped to D-level additions
- **Review status**: Auto-approved (non-interactive mode)

## Planned Changes — Incorporations from V2

### Change #1 — Add per-user concurrent session cap to M3

- **Source**: V2 D2.5 ("Configurable maximum concurrent sessions per user (default: 5). Oldest session evicted when limit exceeded.")
- **Target**: V1 M3 — Session Management & Rate Limiting (Weeks 6-7)
- **Integration approach**: Append as new deliverable D3.7
- **Rationale**: Debate evidence — V2 U-006 (0.85 confidence V2 stronger); V1 advocate conceded in R1 ("V1 lacks per-user session cap"). Limits credential-stuffing harvest size and unbounded session sprawl. Complementary to V1's family-tracking model (D3.1) — family scope = per-user identity, cap = per-user session count.
- **Risk level**: Low (additive)

### Change #2 — Add Kubernetes deployment specifics to M7 D7.6

- **Source**: V2 D7.4 (Kubernetes manifests, HPA min 3 / max 10 / CPU 70% target, PgBouncer, Redis Sentinel)
- **Target**: V1 M7 D7.6 (currently: "Multi-AZ production deploy ≥2 AZs, RDS multi-AZ, Redis replication group; chaos test killing one AZ confirms <30s RTO")
- **Integration approach**: Restructure D7.6 to combine V1's multi-AZ + chaos test with V2's K8s+HPA+PgBouncer+Sentinel — these complement rather than replace each other
- **Rationale**: V2 U-007 (0.78 confidence V2 stronger); V1 advocate conceded that K8s+PgBouncer is "materially more shippable as a runbook." V1's multi-AZ chaos test remains required for NFR-005 verification.
- **Risk level**: Medium (modifies existing critical-path deliverable; orchestrator choice has team-skill implications)

### Change #3 — Add Redis WATCH/MULTI/EXEC atomic refresh primitive to M3 D3.1

- **Source**: V2 D7.1 + R-008 ("Redis `WATCH/MULTI/EXEC` for atomic token invalidation + issuance")
- **Target**: V1 M3 D3.1 (currently: "POST /auth/refresh with token rotation (one-time-use refresh tokens, family tracking for reuse detection → invalidates entire family)")
- **Integration approach**: Modify D3.1 to specify the atomicity primitive; add explicit race-condition test to M3 exit criteria
- **Rationale**: V2 U-008 (0.82 confidence V2 stronger); V1 mentioned "idempotency token" without specifying the atomicity primitive. Concurrent refresh from the same client is a real bug class; OWASP recommends atomic invalidation.
- **Risk level**: Low (clarifies existing deliverable with concrete primitive)

### Change #4 — Add pgcrypto column-level encryption for PII to M1 D1.2

- **Source**: V2 D6.8 ("email addresses stored in encrypted column (`pgcrypto`)")
- **Target**: V1 M1 D1.2 schema migrations
- **Integration approach**: Add pgcrypto column-encryption note to D1.2; extend NFR-006 compliance verification to require column-level (not just disk-level) PII encryption
- **Rationale**: V2 U-009 (0.72 confidence V2 stronger); V1 advocate conceded V1 relies on RDS at-rest encryption only, which doesn't protect against compromised DB credentials. Defense-in-depth for NFR-006 / R-004.
- **Risk level**: Low (additive at schema layer; some query-pattern changes for indexed lookups)

### Change #5 — Add Prometheus + Grafana alert thresholds to M7

- **Source**: V2 D7.2 (Prometheus metrics for request latency p50/p95/p99, error rate, active sessions; alerts for error rate > 1%, p99 > 300ms, audit event write failures)
- **Target**: V1 M7 — currently no explicit alert-threshold deliverable; V1 D1.6 mentions OpenTelemetry baseline
- **Integration approach**: Append as new deliverable D7.9 — Monitoring & alerting thresholds
- **Rationale**: V2's specifics (error rate > 1%, p99 > 300ms, audit write failures) are concrete operational triggers V1 lacks. Adoption supports NFR-005 99.9% uptime detection.
- **Risk level**: Low (additive)

### Change #6 — Adopt V2's load-test ramp pattern in M3 D3.6 and M7 D7.6

- **Source**: V2 D6.6 ("ramp to 10,000 concurrent sessions over 10 minutes, sustain for 30 minutes")
- **Target**: V1 M3 D3.6 (currently "Load test scenario: 10,000 concurrent WebSocket-style polling clients holding sessions") and V1 M7 D7.6 production load test
- **Integration approach**: Modify D3.6 and reference in D7.6 to use V2's explicit ramp/sustain pattern; assertion criteria preserved from V1 (p95 < 200ms with V2's p99 < 200ms added as stretch)
- **Rationale**: V2's ramp+sustain is industry-standard k6/Locust pattern; V1 was less prescriptive
- **Risk level**: Low

### Change #7 — Strengthen account deactivation lifecycle in M6 D6.6 / M7 D7.3

- **Source**: V2 D5.6 (explicit `deactivated_at` timestamp, login-query filtering, 30-day grace, hard-delete with PII removal + anonymized audit retention) + V2 D5.7 (GDPR export-data + delete-account with re-auth)
- **Target**: V1 M6 D6.6 (currently: "GDPR endpoints `GET /me/export`, `DELETE /me` (soft-delete + 30-day grace, then crypto-shred)") and V1 M7 D7.3
- **Integration approach**: Modify D6.6 to specify `deactivated_at` column + login-query filtering explicitly; add re-auth requirement to `DELETE /me`; defer to V1's R-010 + D7.3 tokenization mechanism for the audit-survival design
- **Rationale**: V2 advocate's explicit lifecycle is incrementally clearer than V1's; V1's R-010 tokenization is the stronger underlying mechanism (V2 advocate conceded). Combined gives the strongest design.
- **Risk level**: Low

### Change #8 — Add edge-case validation test suite to M7 as additional gate

- **Source**: V2 D7.1 (centralized edge-case validation: empty database, single-user, max-load 10K + audit writes simultaneously, token expiry at exact boundary, refresh race, OAuth callback with malformed state, rate limit at exact threshold)
- **Target**: V1 M7 — add new deliverable D7.10 as a final-gate edge-case suite
- **Integration approach**: ADDITIVE to V1's per-milestone "Edge Cases Covered" blocks (S-002 winner V1 retained); D7.10 acts as a final integration-level regression suite
- **Rationale**: V1's distributed coverage is more debuggable per-milestone; V2's centralized suite is a useful final gate. Both win — combine.
- **Risk level**: Low

### Change #9 — Add `unverified` role to seed roles in M5 D5.1

- **Source**: V2 D4.1 (roles include `unverified` = pre-email-verification capability tier)
- **Target**: V1 M5 D5.1 (currently seeds `admin`, `user`, `auditor`, `support`)
- **Integration approach**: Add `unverified` as a 5th seed role to V1's set, scoped to "permission to verify email + nothing else"; preserves V1's operational role taxonomy (admin/auditor/support) and adds V2's verification-state tier
- **Rationale**: X-002 was tied in debate; combining both taxonomies is additive and removes a contradiction. Resolves the gap where V1's "user" role implicitly covers both verified and unverified users.
- **Risk level**: Low

### Change #10 — Document tech-stack decision deadline in Open Questions

- **Source**: V2 D1.3 (decides Python 3.12-slim upfront)
- **Target**: V1 Open Question #1 (currently: "Language/framework: Node.js/Express vs Python/FastAPI vs Go/Gin? Decision needed before M1 kickoff.")
- **Integration approach**: Modify Open Question #1 to add explicit "Default if no decision by Week 0: Python 3.12 + FastAPI (per V2 baseline); change requires Week 1 ADR refresh"
- **Rationale**: V1's defer-to-team is defensible (C-012 was tied) but V2's upfront-decide reduces decision latency. Combined: defer with a sensible default to prevent the Open Question from stalling M1.
- **Risk level**: Low

## Planned Changes — Invariant-Probe-Derived Fixes

These resolve HIGH+UNADDRESSED items from `invariant-probe.md` (Round 2.5):

### Change #11 — Specify hash-chain genesis, canonicalization, and tip-publication in D6.5

- **Source**: INV-001 (HIGH UNADDRESSED) — Hash-chain audit-log claim lacks genesis-row definition, canonicalization spec for payload JSON, and tip-publication mechanism for external verifiability
- **Target**: V1 M6 D6.5 (currently: "append-only table `audit_events` with hash-chain (each row contains SHA-256 of prior row's canonicalized payload) for tamper-evidence; daily export to S3 with object-lock")
- **Integration approach**: Expand D6.5 with three sub-deliverables: D6.5.a genesis row (deterministic content), D6.5.b canonicalization spec (JCS RFC 8785 over the row's stable fields), D6.5.c daily Merkle tip publication to S3 + optional public tip-feed
- **Rationale**: Without these the tamper-evidence claim cannot be verified
- **Risk level**: Medium (adds work to M6, possibly delaying M6 by 0.5-1 week — disclose in M6 entry/exit criteria)

### Change #12 — Resolve async audit write vs FR-009 100%-capture (outbox pattern)

- **Source**: INV-017 (HIGH UNADDRESSED) — Both variants' implicit async-after-response-commit refinement contradicts FR-009 "Audit logs capture all auth events"
- **Target**: V1 M6 D6.4 / D6.5 (currently: synchronous emit assumed; A-003 was promoted as shared assumption and rejected by V1 advocate)
- **Integration approach**: Add explicit outbox-pattern deliverable D6.4.a — auth handlers write audit event to outbox table in same DB transaction as state change; durable worker fans out from outbox to immutable store. Guarantees at-least-once delivery without blocking the response path. Latency budget for outbox write < 10ms.
- **Rationale**: Resolves the sync-vs-async tradeoff in favor of FR-009 + NFR-001 simultaneously
- **Risk level**: Medium (adds infrastructure complexity; standard pattern, well-documented)

### Change #13 — Reconcile S3 Object Lock immutability with GDPR crypto-shred (R-010)

- **Source**: INV-019 (HIGH UNADDRESSED) — Daily S3 object-lock export (D6.5) creates immutable PII copies that contradict GDPR right-to-erasure crypto-shred (D7.3, R-010)
- **Target**: V1 R-010 mitigation column
- **Integration approach**: Modify R-010 to specify: (a) S3 object-lock applies only to anonymized/tokenized audit records (post-D7.3 user-id tokenization); (b) PII never enters the immutable export — only references via the tokenized user-id; (c) PII fields remain in the live PG audit_events table where crypto-shred can act, and the immutable export contains only the hash chain over PII-free fields
- **Rationale**: Aligns the keystone compliance design with GDPR; without this fix V1 has the same regulatory exposure as V2
- **Risk level**: Medium (regulatory; requires legal sign-off, captured in D7.8)

### Change #14 — Address SameSite=Strict + OAuth callback cookie-non-send interaction

- **Source**: INV-002 (HIGH UNADDRESSED) — SameSite=Strict cookies are NOT sent on top-level navigation initiated by the third-party OAuth provider, breaking the post-callback session re-attach flow
- **Target**: V1 M4 D4.1 / D4.2 design notes
- **Integration approach**: Add D4.7 — OAuth-callback session re-attach design: callback endpoint sets a short-lived (5-min) SameSite=Lax cookie or uses a server-side state-to-session-id mapping; the SameSite=Strict refresh cookie is set ONLY after the user returns to the app's first-party page. Documents the two-cookie pattern.
- **Rationale**: Common subtle bug that breaks OAuth login on Safari + Firefox in some configurations
- **Risk level**: Low

## Changes NOT Being Made (rejected from V2)

For transparency — debate evidence determined V1's approach superior:

| # | V2 Approach | V1 Approach (retained) | Rationale |
|---|-------------|------------------------|-----------|
| R1 | V2 D2.1: refresh-token reuse → revoke all sessions for user | V1 D3.1: token-family tracking → invalidate family only | V1 is the OWASP-recommended pattern; family-scoping limits collateral damage on legitimate sessions vs full revocation |
| R2 | V2 D1.4 password policy: 12-char min + mixed case + digit + symbol | V1 D2.1: zxcvbn strength check + Argon2id + HIBP-k-anonymity + history-5 | V1 is NIST SP 800-63B aligned; composition rules are deprecated; V2 advocate partially conceded |
| R3 | V2 D1.5 email verification: generic JWT | V1 D2.2: HS256 signed token, 24h TTL, single-use, hashed in `password_resets`-style table | V1 specifies signature algorithm + storage + single-use semantics; V2 leaves these unspecified |
| R4 | V2 R-007 JWT rotation: "support multiple active signing keys" | V1 R-005 + D7.7: RS256 + JWKS `kid` header + quarterly rotation runbook | V1 specifies the asymmetric algorithm and the `kid` mechanism for zero-downtime rotation; V2 advocate conceded |
| R5 | V2 D5.6 hard-delete approach | V1 D7.3 crypto-shred + audit user-id tokenization | V1 resolves the GDPR-vs-audit conflict explicitly; V2 advocate conceded the gap (C-013, U-004) |
| R6 | V2's 18-week schedule | V1's 22-week schedule | Schedule disputed (X-003); after invariant-probe-derived changes (#11, #12, #13), V1's 22 weeks is more credible than V2's compressed 18 weeks; pen-test in V1 is non-optional per NFR-003 |
| R7 | V2 D3.3 OAuth auto-link on matching email | V1 D4.3 OAuth email-match auto-link with **explicit user confirmation** | V2's auto-link enables account-takeover via verified-email collision (V1 NE-3 un-rebutted); V1's confirmation gate is correct |
| R8 | V2 D4.4 rate-limit key = `user_id` | V1 D3.3 rate-limit key = `(IP, email)` for pre-auth | Pre-authentication, `user_id` doesn't yet exist; V1's composite key is correct (NE-4 un-rebutted) |

## Risk Summary

| Change # | Risk | Impact | Probability | Rollback |
|----------|------|--------|------------|----------|
| #2 (K8s topology) | Team unfamiliar with K8s + PgBouncer + Sentinel triad | Medium | Medium | Fall back to V1's multi-AZ + Redis cluster only |
| #11 (hash-chain specifics) | Adds 0.5-1 week to M6 schedule | Medium | High (estimate-dependent) | Cannot rollback — required for tamper-evidence claim |
| #12 (outbox pattern) | Adds infrastructure complexity | Medium | Medium | Fall back to sync writes with documented latency hit |
| #13 (S3 + GDPR reconciliation) | Requires legal sign-off | Medium | Medium | Cannot rollback — legal compliance |
| All others | Additive deliverables inside existing milestones | Low | Low | Trivial |

## Review Status

- **Approval**: Auto-approved (non-interactive mode; `--interactive` flag not set)
- **Timestamp**: 2026-05-22T20:18Z
