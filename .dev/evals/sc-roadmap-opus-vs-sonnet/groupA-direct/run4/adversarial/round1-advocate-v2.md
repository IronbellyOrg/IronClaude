# Round 1 Advocate: Variant 2 (sonnet-default)

**Role**: Advocate for V2
**Round**: 1 of 2
**Date**: 2026-05-22

---

## Position Summary

V2 delivers the same functional scope in 18 weeks versus V1's 22, a 4-week (18%) reduction achieved by tighter milestone bundling and front-loading core auth into M1. It provides materially more shippable operational artifacts (Kubernetes manifests, PgBouncer config, Redis Sentinel topology) and addresses two real-world bug classes that V1 leaves under-specified: concurrent refresh-token race conditions (Redis WATCH/MULTI/EXEC, U-008) and unbounded per-user session sprawl (configurable cap, U-006). Where V2 is weaker -- audit tamper-evidence and GDPR erasure precision -- those gaps are narrow and remediable within V2's existing milestone structure without schedule impact.

---

## Steelman of V1

### Steelman 1: Hash-Chain Audit Log (U-001, C-006)

**V1's strongest argument**: V1's D6.5 introduces a cryptographic hash-chain (each audit row contains SHA-256 of the prior row's canonicalized payload) plus daily S3 export with object-lock. This provides forensic-grade tamper-evidence against privileged insiders, which directly supports R-004 (data breach of PII, Critical impact) and satisfies compliance auditors who require proof that audit records have not been altered. V2's append-only table with async fan-out to a read replica offers no cryptographic integrity guarantee; a privileged DBA could silently alter rows.

**Response**: The hash-chain is a genuinely valuable compliance control, and I concede V2 does not match it. However, V2's append-only model with a separate read replica already raises the bar above a plain table: the write path is synchronous (D6.2), and the read replica provides an independent forensic copy that diverges if the primary is tampered with. For most compliance frameworks (SOC 2, ISO 27001), append-only + replica + access logging satisfies the control objective. Where a customer requires cryptographic chain proof, it can be added to D6.1 as an enhancement in a single sprint -- the schema change is additive (add a `prev_hash` column) and does not alter the existing write path semantics. The risk is real but the remediation cost is bounded.

### Steelman 2: Explicit GDPR Erasure + Audit Survival (U-004, C-013)

**V1's strongest argument**: V1 models the GDPR erasure-versus-audit-retention conflict explicitly via R-010, with a concrete resolution: tokenize `user_id` in the audit table, crypto-shred PII fields at erasure, while audit references survive. Legal sign-off is gated in D7.8. V2's D5.6 says "hard delete removes PII, retains anonymized audit records" but does not address the de-anonymization vector: the audit table has an indexed `actor_user_id` column (D6.1), and if PII is removed from the `users` table but `actor_user_id` still points to a deleted row, any correlation with the `metadata` JSONB field could re-identify the user.

**Response**: V1's tokenization approach is the correct long-term design. V2's current wording is imprecise and this is a genuine gap. However, V2 already has the building blocks to close it: the `metadata` JSONB field in D6.1 can be extended to carry a tokenized reference at write time, and the hard-delete path in D5.6 can be updated to null out `actor_user_id` while preserving the event record. This is a wording-and-schema fix, not an architectural change. The key question is whether this should disqualify V2 as a base: I argue no, because the 4-week schedule savings and superior operational artifacts outweigh a gap that requires ~2 days of schema work to close.

### Steelman 3: Higher Risk Coverage (R-005 through R-012 vs V2's R-005 through R-008)

**V1's strongest argument**: V1 identifies 12 risks to V2's 8. V1 explicitly models JWT signing-key compromise (R-005), SendGrid outage with failover SMTP (R-006), RBAC misconfiguration escalation (R-007), 2FA recovery-code abuse (R-008), audit-log tampering by insider (R-009), GDPR erasure conflict (R-010), refresh-token theft offline (R-011), and TOCTOU on role revocation (R-012). V2 covers only Redis SPOF, SendGrid failures, JWT rotation, and race conditions -- missing explicit modeling of insider tampering, TOCTOU, and recovery-code abuse.

**Response**: V1's risk register is more thorough, and I concede V2 should adopt R-008 (2FA recovery-code abuse) and R-012 (TOCTOU on role revocation) as explicit entries. However, several of V1's "additional" risks are already implicitly mitigated in V2's deliverables: V2's D4.2 middleware with deny-by-default semantics addresses RBAC misconfiguration; V2's D5.3 stores 2FA secrets encrypted (AES-256-GCM); V2's 15-min access-token TTL bounds TOCTOU damage. The difference is V1 documents these as explicit risks while V2 embeds the mitigations in deliverables. Both approaches are valid; V1's is more auditor-friendly, V2's is more implementer-friendly. A merge should adopt V1's explicit risk entries alongside V2's deliverable language.

### Steelman 4: Edge Cases Distributed Per Milestone (S-002)

**V1's strongest argument**: V1 places `**Edge Cases Covered**` blocks inside each milestone (M2, M3, M5), ensuring developers encounter edge-case requirements at the point of implementation rather than deferring them to a final validation pass. V2 centralizes all edge cases into M7's D7.1 test suite, creating a risk that edge-case behavior is not designed for during M1-M6 implementation -- only tested after the fact.

**Response**: This is a legitimate structural advantage for V1. Per-milestone edge-case documentation is superior for implementation guidance. However, V2's approach has a complementary strength: D7.1 serves as a comprehensive regression gate that validates edge-case behavior holistically, including cross-milestone interactions that per-milestone lists cannot capture (e.g., refresh-token reuse during an OAuth-linked session). The ideal is both: per-milestone edge-case guidance (from V1) plus a centralized validation suite (from V2). The merge should adopt V1's inline blocks into V2's milestone structure while retaining D7.1 as the regression gate.

---

## Strengths Claimed (V2)

1. **18-week delivery (C-001, X-003)**: V2 achieves the full FR scope in 18 weeks versus V1's 22, a 4-week reduction. This is accomplished by bundling core auth into M1 (X-004) and collapsing the admin dashboard + compliance validation into M6 rather than spreading them across M6 and M7. The schedule advantage is material: 4 weeks of engineering time, earlier revenue, and faster feedback cycles. Diff points: C-001, X-003, X-004.

2. **Decided tech stack (C-012)**: V2 specifies Python 3.12-slim (D1.3), removing the language/framework open question entirely. V1 defers this decision, leaving a blocker on M1 start. Making the call early unblocks library selection (pyotp, Authlib, argon2-cffi) and allows the team to write code in Week 1. Diff points: C-012.

3. **Kubernetes deployment specifics with PgBouncer (U-007, C-010)**: V2's D7.4 specifies Deployment, Service, ConfigMap, Secret manifests, HPA (min 3, max 10, CPU 70%), PgBouncer for connection pooling, and Redis Sentinel for HA. V1 says "multi-AZ" but does not specify the orchestrator or connection-pooling strategy. At 10K concurrent sessions, PostgreSQL without PgBouncer will exhaust connections. Diff points: U-007, C-010.

4. **Per-user concurrent session cap (U-006, C-005)**: V2's D2.5 enforces a configurable maximum of 5 concurrent sessions per user with oldest-eviction on overflow. This limits credential-stuffing harvest size, prevents unbounded session sprawl, and provides a concrete operational lever. V1 has no per-user cap. Diff points: U-006, C-005.

5. **Refresh-token race condition via Redis WATCH/MULTI/EXEC (U-008, C-011)**: V2's D2.1 and D7.1 specify Redis atomic transactions for concurrent refresh requests and an explicit race-condition test. V1 mentions "idempotency token" in M3 edge cases but does not specify the atomicity primitive. This is a real bug class: two concurrent refresh requests from the same client on a slow network can both validate the same token and issue two new tokens. Diff points: U-008, C-011.

6. **Email-column encryption via pgcrypto (U-009, C-007)**: V2's D6.8 specifies column-level encryption for email addresses using pgcrypto, in addition to RDS at-rest encryption. V1 relies on RDS at-rest encryption only, which does not protect against compromised DB credentials (a legitimate threat vector per R-004). Diff points: U-009, C-007.

7. **Stricter latency percentile: p99 vs p95 (C-004, X-001)**: V2 commits to p99 < 200ms (Goals row 9, D6.6 exit), which is a stricter SLO than V1's p95 < 200ms. A system that satisfies p99 automatically satisfies p95; the reverse is not true. This provides a stronger availability contract to consumers. Diff points: C-004, X-001.

8. **Front-loading user-facing value in M1 (X-004)**: V2 ships registration, login, and email verification in M1 (Weeks 1-3), enabling an early demo and stakeholder feedback at the 3-week mark. V1 delivers no user-facing functionality until M2 (Week 5). Early demos reduce project risk by validating UX assumptions sooner. Diff points: X-004.

---

## Weaknesses Identified in V1

1. **Vague deployment topology (C-010)**: V1's D7.6 says "multi-AZ" without specifying the container orchestrator, connection pooling, or Redis HA strategy. At the stated 10K concurrent session target, PostgreSQL without connection pooling will fail. The lack of PgBouncer or equivalent is an operational gap that will surface during load testing (D3.6) and require an unplanned fix. Diff points: C-010, U-007.

2. **No per-user session cap (C-005, U-006)**: V1's 10K aggregate target has no per-user bound. A single compromised account could hold thousands of active sessions, and credential-stuffing tools exploit exactly this gap. V2's D2.5 cap of 5 sessions per user with oldest-eviction is a standard security control that V1 omits. Diff points: C-005, U-006.

3. **Deferred tech-stack decision creates M1 blocker (C-012)**: V1's Open Q #1 defers the language/framework choice, but D1.1 (service skeleton) cannot begin without it. This creates a "decision before action" dependency that delays M1 start. The question will be resolved in a meeting, but the roadmap should not encode a blocker into the first milestone's entry criteria. Diff points: C-012.

4. **Underspecified concurrent-refresh atomicity (C-011, U-008)**: V1's M3 edge cases mention "concurrent refresh from same client (idempotency token)" but do not specify the atomicity primitive. An idempotency token without a server-side atomic compare-and-swap is insufficient: two requests arriving simultaneously can both read the token as valid before either writes the invalidation. V2's Redis WATCH/MULTI/EXEC provides a correct solution. Diff points: C-011, U-008.

5. **Weaker latency SLO (C-004, X-001)**: V1's p95 < 200ms permits 5% of requests to exceed the threshold without consequence. At 10K concurrent sessions, 5% is 500 requests per measurement window. V2's p99 < 200ms limits this to 100 requests, a 5x tighter guarantee. Diff points: C-004, X-001.

6. **No column-level PII encryption (U-009)**: V1 relies solely on RDS at-rest encryption for PII protection. If an attacker obtains database credentials (SQL injection, credential leak), they have plaintext access to all email addresses and PII. V2's pgcrypto column encryption adds a defense-in-depth layer. Diff points: U-009, C-007.

7. **Four extra weeks with no additional FR coverage (C-001, X-003)**: V1 takes 22 weeks to deliver the same FR scope (FR-001 through FR-012). The additional 4 weeks are spent on a longer M7 (5 weeks vs V2's 2 weeks) and more granular milestone separation. This is schedule inflation without corresponding functional value. Diff points: C-001, X-003.

---

## Concessions

1. **Audit tamper-evidence (C-006, U-001)**: V2's append-only table with read-replica fan-out does not provide cryptographic tamper-evidence. V1's hash-chain + S3 object-lock is superior for compliance-sensitive environments. V2 should adopt V1's hash-chain mechanism in D6.1.

2. **GDPR erasure precision (C-013, U-004)**: V2's D5.6 hand-waves the erasure-audit conflict. The `actor_user_id` index in D6.1 creates a de-anonymization vector that V2 does not address. V2 should adopt V1's tokenized `user_id` approach.

3. **Risk register completeness**: V2 identifies 8 risks to V1's 12. V2 is missing explicit entries for audit-log tampering (V1 R-009), GDPR erasure conflict (V1 R-010), refresh-token theft offline (V1 R-011), and 2FA recovery-code abuse (V1 R-008). These should be merged in.

4. **Per-milestone edge-case documentation (S-002)**: V1's inline `**Edge Cases Covered**` blocks are superior implementation guidance. V2's centralized D7.1 approach risks edge-case blindness during M1-M6 implementation. The merge should incorporate V1's inline blocks.

5. **Bootstrap admin script (U-005)**: V1 explicitly includes a bootstrap admin script for empty-database cold start (D2.7). V2 covers "empty database" in D7.1 tests but does not ship a creation path. This is a real operational gap for first deployment.

---

## Shared Assumption Responses

| ID | Position | Rationale |
|----|----------|-----------|
| A-001 | **ACCEPT** | V2's D1.6 specifies SameSite=Strict cookies, confirming browser-as-primary-client. Mobile SDKs are explicitly out of scope (V2 Out of Scope). This is a valid constraint for the stated FR scope. |
| A-002 | **ACCEPT** | Email as canonical identifier is appropriate for the auth system's scope. Both variants converge on this. Adding a username field would be scope creep beyond the FR requirements. |
| A-003 | **QUALIFY** | Synchronous audit writes on the hot path are acceptable at 10K sessions *if* the write completes within the latency budget. V2's D6.2 specifies "within 500ms" for audit writes, which exceeds the 200ms API latency target. The audit write should be async after response commit, not blocking the client response. This is a design refinement, not a fundamental rejection. |
| A-004 | **ACCEPT** | OAuth callback URIs are standard endpoints under the team's control. Both variants implement Authorization Code + PKCE/state. No additional mitigation needed beyond V2's D3.5 state parameter with server-side session storage. |
| A-005 | **QUALIFY** | Single-region with multi-AZ (V1) or k8s + Sentinel (V2) can achieve 99.9% (43.2 min/month). However, neither variant models regional failure. If single-region SLA requirements increase post-launch, cross-region failover will need a separate roadmap. Accept for launch, flag for v2. |
| A-006 | **ACCEPT** | Forward-only, zero-downtime migrations are standard practice. V2's `/migrations/` directory and V1's Flyway/Alembic both support this. The rolling-deploy compatibility window is an operational concern, not a roadmap design concern. |
| A-007 | **REJECT** | V2's D7.1 edge-case suite includes "refresh token reuse race condition (two simultaneous refresh requests)" which directly tests this scenario, but V2 does not specify the validation ordering (one-time-use check before or after signature verification). The correct order is: (1) mark token used in Redis/DB atomically, (2) validate signature/expiry, (3) issue new token. V2 should specify this ordering in D2.1 to prevent the token-binding race. |
| A-008 | **QUALIFY** | V2's 18-week schedule is more achievable with a single team than V1's 22 weeks, but neither variant models team composition. V2's tighter bundling (e.g., M1 includes both infra and core auth) implies full-stack engineers or a 3+ person team. This should be stated in M1 entry criteria. |

---

## Per-Point Verdicts

| Diff Point | V2 Position | V1 Position | Where V2 is stronger / weaker / tied | Confidence |
|------------|-------------|-------------|--------------------------------------|------------|
| S-001 | No separators | `---` between milestones | Tied (cosmetic) | 0.95 |
| S-002 | Centralized edge cases in D7.1 | Per-milestone edge-case blocks | V1 stronger (implementation guidance) | 0.85 |
| S-003 | Goals table by scope area | Goals table by semantic axis (G1..G7) | Tied (both valid) | 0.90 |
| C-001 | 18 weeks | 22 weeks | V2 stronger (same FR scope, 18% shorter) | 0.92 |
| C-002 | M1 Foundation+CoreAuth, tighter bundling | M1 Foundation only, more granular | V2 stronger (faster value delivery) | 0.80 |
| C-003 | admin/editor/viewer/unverified | admin/user/auditor/support | Tied (product decision, both valid RBAC) | 0.70 |
| C-004 | p99 < 200ms | p95 < 200ms | V2 stronger (5x tighter SLO) | 0.90 |
| C-005 | Per-user cap of 5, oldest-eviction | No per-user cap | V2 stronger (security control) | 0.92 |
| C-006 | Append-only + read replica | Hash-chain + S3 object-lock | V1 stronger (cryptographic tamper-evidence) | 0.88 |
| C-007 | 12-char policy + Argon2id + pgcrypto | zxcvbn + Argon2id (64MB, par 2) + HIBP + history | V1 stronger (HIBP + history check superior to static policy) | 0.78 |
| C-008 | Algorithm unspecified, multi-key mentioned | RS256 + JWKS + rotation runbook | V1 stronger (explicit crypto specification) | 0.85 |
| C-009 | JWT 24h TTL (algo unspecified) | HS256 24h TTL | Tied (both functional, V1 more explicit) | 0.75 |
| C-010 | Kubernetes + PgBouncer + Redis Sentinel | Multi-AZ (orchestrator unspecified) | V2 stronger (shippable runbook) | 0.90 |
| C-011 | Single-token reuse detection, revoke all user sessions | Family-tracking, invalidate family | Tied (different tradeoffs: V2 more aggressive, V1 more precise) | 0.65 |
| C-012 | Decided: Python 3.12 | Deferred to Open Q #1 | V2 stronger (unblocks M1) | 0.88 |
| C-013 | Implicit, de-anonymization gap | Explicit tokenization + crypto-shred | V1 stronger (correct long-term design) | 0.85 |
| X-001 | p99 < 200ms | p95 < 200ms | V2 stronger (stricter contract) | 0.90 |
| X-002 | CRUD-capability roles | Duty-based roles | Tied (product decision) | 0.60 |
| X-003 | 18 weeks | 22 weeks | V2 stronger (4-week savings) | 0.92 |
| X-004 | Core auth in M1 | Pure scaffolding in M1 | V2 stronger (early value delivery) | 0.82 |
| X-005 | Rate-limit in M4 with RBAC | Rate-limit in M3 with sessions | Tied (both defensible) | 0.65 |
| U-001 | N/A (V1 unique) | Hash-chain audit + S3 export | V1 stronger | 0.88 |
| U-002 | Multi-key mentioned (R-007) | Explicit R-005 with JWKS + kid + blast-radius analysis | V1 stronger | 0.85 |
| U-003 | Queue + retry on single provider | SES failover + degraded-mode SLA | V1 stronger | 0.80 |
| U-004 | Implicit handling | Crypto-shred + tokenized user_id | V1 stronger | 0.85 |
| U-005 | Empty DB in D7.1 tests only | Bootstrap admin script (D2.7) | V1 stronger | 0.82 |
| U-006 | Per-user session cap (D2.5) | N/A (V2 unique) | V2 stronger | 0.90 |
| U-007 | K8s + PgBouncer + Sentinel (D7.4) | Multi-AZ unspecified | V2 stronger | 0.92 |
| U-008 | Redis WATCH/MULTI/EXEC + race test (D7.1, R-008) | Idempotency token (unspecified) | V2 stronger | 0.88 |
| U-009 | pgcrypto column encryption (D6.8) | RDS at-rest only | V2 stronger | 0.85 |
| A-001 | ACCEPT | ACCEPT | Tied | 0.95 |
| A-002 | ACCEPT | ACCEPT | Tied | 0.95 |
| A-003 | QUALIFY | QUALIFY | Tied (both need audit-write refinement) | 0.80 |
| A-004 | ACCEPT | ACCEPT | Tied | 0.90 |
| A-005 | QUALIFY | QUALIFY | Tied | 0.75 |
| A-006 | ACCEPT | ACCEPT | Tied | 0.90 |
| A-007 | REJECT | REJECT | Tied (both need fix) | 0.85 |
| A-008 | QUALIFY | QUALIFY | Tied | 0.80 |

**Summary**: V2 is stronger on 11 diff points, weaker on 8, and tied on 15. V2's advantages cluster in operational shippability (C-010, U-007, U-008, U-009), schedule efficiency (C-001, X-003, X-004), and SLO precision (C-004, X-001). V1's advantages cluster in compliance depth (C-006, C-013, U-001, U-004) and risk documentation. The merge should use V2 as the structural base and graft V1's compliance controls and risk entries on top.
