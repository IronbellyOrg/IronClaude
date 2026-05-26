# Round 1 — Advocate for V1 (opus)

## Position Summary

V1 is the stronger base roadmap because it (a) treats the audit log as a cryptographic invariant (hash-chained rows + S3 object-lock) rather than a write-amplified database table, (b) explicitly models the GDPR-erasure-vs-audit-retention conflict that V2 leaves under-specified, and (c) reserves M1 as pure scaffolding so M2 ships user-facing auth on a hardened, observable base. V1's risk register is materially deeper (12 entries vs 8), surfacing JWT signing-key compromise, SendGrid failover, RBAC misconfiguration, recovery-code abuse, and TOCTOU on role revocation — risks that map directly to OWASP A01/A02/A07 and are absent or hand-waved in V2.

## Steelman of V2

**V2-S1 — "p99 < 200ms is a stricter, more honest commitment than p95."**

V2's strongest framing: tail latency is what users actually feel. A p95 SLA can hide a 1-in-20 hot-path stall that, at 10K concurrent sessions, materializes as ~500 affected sessions at any moment. By writing the goal as p99 (Goals row 9, D6.6 exit), V2 is committing the team to the metric production support actually pages on.

**Response.** The criticism is real but the spec text is "< 200ms," and V1's p95 commitment is *honest about what a 22-week single-team build can verify*. V1 still bounds tail latency via M3 D3.6's 10K soak (<1% error) and via Argon2id memory-cost tuning (D2.1). V2's p99 commitment is also asserted only on three endpoints (`/auth/login`, `/auth/refresh`, `/auth/profile`); V1's p95 applies to `/login`, `/register`, `/refresh`, and `/oauth/*` — strictly broader endpoint coverage even if looser per-endpoint. The right resolution at merge time is to make this an explicit pick; V1's broader endpoint scope is the better default since silent omission of `/register` or `/oauth/*` from the SLA is the more dangerous gap. See A-003 shared assumption: V2's stricter p99 + synchronous audit writes have not been jointly load-tested anywhere in the doc.

**V2-S2 — "Per-user session cap (D2.5) is a real control V1 lacks."**

Strongest form: an attacker who compromises one credential can fan out into unbounded session sprawl, and at 10K aggregate concurrency limit a single attacker could plausibly consume hundreds of slots. A default cap of 5 sessions with oldest-eviction (D2.5) bounds credential-stuffing harvest size and gives the user a visible signal when their account is being abused. This is a security control V1 simply does not have.

**Response.** Conceded as a gap (see Concessions). V1 should adopt the per-user cap. However, V2's implementation is under-specified at the security boundary: oldest-eviction is *user-hostile* when the legitimate user is the attacker-on-rotation (rotating tokens evict the legitimate session). V1's family-tracking refresh model (D3.1, U-011 risk) achieves the deeper goal — credential-theft *detection* — by triggering family invalidation + user alert on reuse, which is a stronger signal than "you've been silently evicted." The merge plan should integrate V2's session cap as a hard ceiling and keep V1's family-tracking as the detection layer.

**V2-S3 — "K8s + HPA + PgBouncer + Redis Sentinel (D7.4) is a more shippable deployment runbook."**

Strongest form: V1 says "multi-AZ" but never names the orchestrator, the autoscaler signal, the connection pool, or the Redis HA mechanism. V2 names all four (HPA min 3/max 10, CPU 70%, PgBouncer, Sentinel). For a team starting from zero, V2's spec is materially closer to a runnable manifest.

**Response.** Conceded as concrete-deployment-detail strength (see Concessions). However, V1's choice is more *architecturally honest*: it commits to multi-AZ + RDS multi-AZ + Redis replication group + chaos test (<30s RTO) — i.e., the **failure-mode contract**, not the toolchain. V2's K8s assumption locks the team into one orchestrator before language/framework is even chosen (V2 hard-codes Python 3.12-slim in D1.3 — see C-012). V1's deferral of tech-stack to Open Q #1 is the correct sequencing: you cannot pick the orchestrator before the ADR exists. The merge should adopt V2's K8s runbook *conditional on* the ADR landing on Python; on Node, the same runbook structure ports cleanly but the base image and PgBouncer config change.

**V2-S4 — "Refresh-token race-condition handling with Redis WATCH/MULTI/EXEC (D7.1, R-008) is more rigorous than V1's mention of 'idempotency token'."**

Strongest form: concurrent refresh from the same client is a real bug class (mobile retry, double-click, network jitter). V2 names the atomicity primitive (WATCH/MULTI/EXEC) and writes the explicit race-condition test. V1 mentions "concurrent refresh from same client (idempotency token)" in M3 edge cases but doesn't specify the atomicity primitive or include a dedicated test.

**Response.** Conceded as testing-discipline strength. V1's family-tracking model (D3.1) *already* converts the race-condition failure mode into a detectable security event — if two concurrent refreshes both invalidate the parent token, the family is killed and the user is alerted. That's defense-in-depth: V2's WATCH/MULTI/EXEC prevents the race; V1's family-tracking *also* catches the race when prevention fails. The right merge keeps both: WATCH/MULTI/EXEC as primary, family invalidation as secondary detection.

## Strengths Claimed (V1)

1. **Hash-chained audit log + S3 object-lock (D6.5, U-001).** Each audit row contains the SHA-256 of the prior row's canonicalized payload; daily export to S3 with object-lock. Advantages V1 on **C-006** (tamper-evidence) and **R-009** (insider tampering). V2's append-only PG table is defeated by a privileged DBA or compromised app credentials — there is no cryptographic chain to detect splice attacks.

2. **R-005 JWT signing-key compromise with JWKS `kid` + 15-min access TTL bounding blast radius (U-002).** Quarterly rotation runbook (D7.7), zero-downtime rotation via `kid` header. Advantages V1 on **C-008** (RS256 + JWKS endpoint `/.well-known/jwks.json`). V2's R-007 mentions "multiple active signing keys" but never names the publication mechanism (JWKS) or the rotation cadence.

3. **R-010 GDPR erasure ↔ audit retention conflict explicitly resolved (U-004, C-013).** Tokenize `user_id` in audit table; crypto-shred PII at erasure; audit references survive. Legal sign-off gated in D7.8. Advantages V1 on **C-013** and **A-002** (canonical identifier). V2's hard delete "removes PII, retains anonymized audit records" but `actor_user_id` is indexed and de-anonymizable via timing correlation — V2 has the conflict and doesn't address it.

4. **R-006 SendGrid failover via SES (U-003).** Secondary SMTP configured; degraded-mode SLA documented. Advantages V1 on resilience: V2's R-006 mitigation is single-provider queue + retry (3 attempts over 24h) — a full SendGrid outage extends registration latency to hours.

5. **R-007 RBAC misconfiguration with deny-by-default + peer-reviewed permission matrix + negative-path integration tests + audited admin assignments.** Advantages V1 on **C-003 / X-002**: V1's `admin / user / auditor / support` taxonomy maps to *duties* (auditor for SOC 2 evidence collection, support for desk-side troubleshooting), matching real org structure better than V2's CRUD-tiered `editor / viewer / unverified`.

6. **R-008 2FA recovery-code abuse (U-002 adjacent).** Argon2id-hashed, single-use, force re-enroll after any use, alert email. Advantages V1 on M5 D5.5 vs V2 D5.4 ("backup codes ... stored hashed" — no re-enroll-on-use, no alert).

7. **R-011 offline refresh-token theft + R-012 TOCTOU on role revocation.** Two L3 state-mechanics risks V2 does not register. R-012 in particular addresses C-011 (refresh family invalidation) and gives the admin force-logout path (D7.1) — V2's `PUT /admin/users/{id}/role` (D4.3) does not invalidate live sessions.

8. **Bootstrap admin path (D2.7, U-005).** First-user/empty-DB cold start has a shipped script. Advantages V1 on **A-006** (migration state) and addresses the real operational gap V2 covers only as a *test case* in D7.1, not as a deliverable.

9. **HIBP k-anonymity check at registration + reset (D2.1, D6.2, C-007).** Breached-password rejection before hash. V2's password policy (12-char + complexity) is *exactly the policy NIST SP 800-63B deprecated*; V1's zxcvbn + HIBP is the modern equivalent.

10. **M1 as pure scaffolding (X-004).** Foundation milestone ships zero auth code; observability + CI/CD + container scan (Trivy) + Vault land before any user-facing endpoint. V2 ships register/login/verify in M1 (D1.4–D1.6), which means OWASP ZAP doesn't run against the stack until M6 — five months after the first auth endpoint goes live in staging.

11. **22-week schedule with 4-week M5 (RBAC + 2FA) and 5-week M7 (admin + hardening + pen-test) (X-003).** V2 compresses pen-test, runbooks, multi-AZ, and rollback rehearsal into a 2-week M7. Pen-test alone typically needs 2–3 weeks of vendor engagement + remediation; V2's M7 is not credible.

12. **Open Question #1 (tech-stack ADR) gates M1 entry (C-012).** V1 defers Node/Python/Go to a documented decision; V2 silently commits to Python 3.12-slim in D1.3 without an ADR. This is a process-discipline strength.

## Weaknesses Identified in V2

1. **V2 D6.2 (synchronous audit write within 500ms on hot path)** combined with **V2 D2.5 (per-user session cap)** and **V2 NFR p99 < 200ms** are jointly unverified. A login emits ≥1 audit event; a refresh emits ≥1 audit event; account lockout emits ≥1. Write amplification at 10K concurrent sessions has no load-test scenario. Diff point: **A-003**, **C-004**.

2. **V2 D6.1 audit table is not tamper-evident.** "Append-only" is an application-level convention; a DBA with `DELETE` privilege defeats it. Diff point: **C-006**, **U-001**.

3. **V2 R-007 (JWT secret rotation)** mitigates with "multiple active signing keys" but never names JWKS or `kid`. Without a publication endpoint, downstream services can't validate new-key tokens without redeploy. Diff point: **C-008**, **U-002**.

4. **V2 D5.6 hard delete "removes PII, retains anonymized audit records"** but D6.1 indexes `actor_user_id` and joins on it. Anonymization claim is not substantiated by schema. Diff point: **C-013**, **U-004**, **A-002**.

5. **V2 D1.4 password policy (12-char, mixed case, digit, symbol) is the NIST-deprecated composition-rule pattern.** NIST SP 800-63B §5.1.1.2 explicitly recommends against composition rules in favor of breach-list checks. Diff point: **C-007**.

6. **V2 D1.3 hard-codes Python 3.12-slim** without an ADR. Tech-stack choice is a multi-year architectural commitment; making it implicitly in a deliverable is process debt. Diff point: **C-012**.

7. **V2 M7 (2 weeks) is implausible for production hardening.** It must contain: edge-case suite, Prometheus + Grafana, incident runbooks (4 scenarios), K8s manifests + HPA + PgBouncer + Sentinel, launch readiness checklist, rollback rehearsal. Diff point: **C-001**, **X-003**.

8. **V2 R-005 (Redis SPoF) mitigation includes "accept login with direct PostgreSQL token validation (slower, but functional"** — but D4.4 (rate limiting) and D4.5 (lockout) both rely on Redis. Graceful Redis degradation cannot exist without redesigning rate-limit/lockout to use PG. Diff point: V2 internal inconsistency in R-005.

9. **V2 D4.4 rate-limit key is `ratelimit:{user_id}:{endpoint_group}`** — keyed on `user_id`, which doesn't exist for `/auth/login` (the request that needs rate-limiting most). V1 D3.3 uses `(IP, email)` composite, which is the correct pre-auth scope. Diff point: **C-005**, R-002 quality.

10. **V2 D3.3 OAuth account linking auto-links on email match without re-verification.** Spec text: "if OAuth email matches existing account, link provider to that account." V1 requires "explicit user confirmation" (D4.3). Account-takeover vector: attacker registers Google account with victim's email, gets verified Google account, then auto-link gifts them the existing account. Diff point: V2 security regression in M3 D3.3.

11. **V2 M5 lumps 2FA, password reset, profile, GDPR, account deactivation into 3 weeks.** Eight deliverables (D5.1–D5.8) with cross-cutting concerns (token invalidation on reset, audit emission on every change, GDPR re-auth). V1 splits into M5 (4w) and M6 (3w). Diff point: **C-002**.

12. **V2 only 8 risks vs V1's 12.** Missing: signing-key rotation as L3 risk, SendGrid failover, RBAC misconfig, recovery-code abuse, audit insider tampering, GDPR-audit conflict, offline refresh-token theft, TOCTOU role revocation. Diff point: risk-coverage breadth.

## Concessions

V1 is honestly weaker than V2 on these points:

- **C-005 / U-006:** V1 has no per-user session cap. This is a real gap; V2's default-5 with eviction is a sensible control. V1 should adopt it at merge time.
- **U-008 / C-008:** V1 mentions "idempotency token" for concurrent refresh but does not name `WATCH/MULTI/EXEC` or include a dedicated race-condition test. V2's D7.1 + R-008 specificity is better engineering hygiene.
- **U-009:** V1 relies on RDS at-rest encryption only; V2's pgcrypto column-level encryption on the email column is defense-in-depth V1 lacks. Should be merged in.
- **U-007:** V2's K8s + HPA + PgBouncer + Sentinel specifics are materially more shippable than V1's "multi-AZ" abstraction. V1's deployment topology section needs more concreteness.
- **C-004:** V2's p99 framing is more honest about tail latency than V1's p95, *for the endpoints V2 covers*. Best resolution is p99 on critical-path endpoints, p95 on the broader auth surface — but V1 should not claim p99 was the equivalent commitment.
- **Word count:** V2 is 3669 words vs V1's 2785 — V2 packs more deliverable-level detail per milestone (D5.1–D5.8 are highly specific). V1 is denser per-line but covers less surface area in deliverable enumeration. This is a stylistic concession, not a correctness one.

## Shared Assumption Responses

| ID | Position | Rationale |
|----|----------|-----------|
| A-001 | QUALIFY | ACCEPT for browser-on-shared-domain (V1's primary client model). Native mobile / cross-origin SPA must use Authorization header + opaque refresh in encrypted storage — needs explicit deliverable in merged plan, not silent assumption. |
| A-002 | ACCEPT | Email as canonical identifier is consistent with both variants and with FR-001..FR-012. Username login is in V1's "Out of Scope (deferred): SCIM provisioning" implicitly and V2's Out of Scope explicitly excludes nothing here — both can ship without username. |
| A-003 | REJECT | Synchronous audit writes at 10K concurrent + V2's p99 < 200ms + write amplification (login + refresh + logout = 3 audit writes per session lifecycle) has no joint load test in either variant. V1's M3 D3.6 covers session soak but not audit write amplification. Must be modeled as a deliverable in merged plan — likely with async audit fan-out to a queue + sync write to PG within a bounded retry window. |
| A-004 | ACCEPT | OAuth callback URI under team's control is standard; V1 D4.5 explicitly mentions "redirect_uri allowlist." Cert lifecycle is implicit in TLS 1.3 commitment (NFR-006) but a runbook in D7.7 should name it. |
| A-005 | QUALIFY | 99.9% (43min/month) tolerates a regional outage *statistically* but not in expectation. V1's multi-AZ (D7.6) + chaos test (<30s RTO) bounds AZ failure; cross-region failover is genuinely out of scope for 99.9% and should be deferred to a 99.95+ SLO conversation. Both variants implicitly assume single-region; merge plan should make this explicit. |
| A-006 | QUALIFY | Both variants use forward-only migrations but neither addresses the schema-compatibility window for rolling deploys (e.g., add column → backfill → switch reads → drop). V1's D1.2 lists Flyway/Alembic but the *compatibility discipline* is unstated. Add to D7.7 runbook. |
| A-007 | REJECT | Token-binding race is an unaddressed L3 invariant. Both variants describe single-use tokens but neither specifies the ordering (mark-then-verify vs verify-then-mark). V1 should add explicit guard: `UPDATE password_resets SET used_at = NOW() WHERE token_hash = $1 AND used_at IS NULL RETURNING id` — a single atomic claim. Merged plan must specify. |
| A-008 | QUALIFY | V1's 22 weeks and V2's 18 weeks both omit team-composition modeling. V1's longer schedule is *more credible* for a single team (≤6 engineers) given pen-test + multi-AZ + 2FA + audit-chain scope; V2's 18 weeks implies either parallel teams or scope shaving. Merged plan should state team size assumption. |

## Per-Point Verdicts

| Diff Point ID | V1 Position | V2 Position | Where V1 is stronger / weaker / tied | Confidence |
|---------------|-------------|-------------|---------------------------------------|------------|
| S-001 | `---` separators between milestones | `###` heading only | V1 stronger on readability of long docs | 0.55 |
| S-002 | Edge cases distributed per-milestone (M2, M3, M5) | Centralized in M7 D7.1 | V1 stronger — edge cases discovered at design time, not deferred to validation phase | 0.78 |
| S-003 | Goals grouped by G1..G7 axes | Goals grouped by scope-area | V1 stronger — semantic axes survive scope churn; scope-area rows churn with milestone reshuffle | 0.65 |
| C-001 | 22 weeks | 18 weeks | V1 stronger — V2's 2-week M7 is not credible for pen-test + multi-AZ + rollback rehearsal | 0.85 |
| C-002 | Sessions before OAuth before RBAC | OAuth before RBAC before Reset | V1 stronger — session/rate-limit foundation must precede OAuth (OAuth-issued sessions need rate-limit + revocation); V2's ordering bolts OAuth on before the session model is hardened | 0.78 |
| C-003 | Duty-based roles (admin/user/auditor/support) | CRUD-tiered (admin/editor/viewer/unverified) | Tied — both are valid; product decision. V1's `auditor` directly maps to SOC 2 evidence collection which V2 lacks | 0.55 |
| C-004 | p95 < 200ms across broader endpoints | p99 < 200ms on 3 endpoints | Mixed — V2 stricter percentile, V1 broader endpoint coverage. Best outcome is both | 0.65 |
| C-005 | 10K aggregate, no per-user cap | 10K aggregate + 5/user cap | V2 stronger — concede | 0.80 |
| C-006 | Hash-chained audit + S3 object-lock | Append-only PG table | V1 stronger — cryptographic invariant beats application convention | 0.92 |
| C-007 | zxcvbn + HIBP + Argon2id (params named) | 12-char composition rules + Argon2id (params unnamed) | V1 stronger — V2's policy is NIST-deprecated; Argon2id params unspecified | 0.88 |
| C-008 | RS256 + JWKS endpoint + kid | Algorithm unspecified | V1 stronger — concrete crypto + rotation mechanism | 0.85 |
| C-009 | HS256 24h verification token | JWT 24h (no algorithm) | V1 stronger — specificity | 0.70 |
| C-010 | Multi-AZ + chaos test + <30s RTO contract | K8s HPA + PgBouncer + Sentinel | Mixed — V2 stronger on toolchain specificity, V1 stronger on failure-mode contract. Concede V2 advantage on shippability | 0.55 |
| C-011 | Family-tracking refresh; reuse kills family + alerts user | Single-token reuse → revoke all user sessions | V1 stronger — family-tracking is finer-grained detection; V2's revoke-all is hostile to legitimate users on shared accounts | 0.80 |
| C-012 | Tech-stack deferred to ADR (Open Q #1) | Python 3.12-slim committed in D1.3 | V1 stronger — ADR discipline; V2 makes architectural commit implicitly | 0.80 |
| C-013 | Tokenized user_id + crypto-shred PII + legal sign-off | "Removes PII, retains anonymized" — vector unaddressed | V1 stronger — V2 has the conflict, doesn't model the resolution | 0.90 |
| X-001 | p95 commitment | p99 commitment | Mixed (see C-004) | 0.60 |
| X-002 | Duty-based roles | CRUD-tiered roles | Tied — product decision | 0.55 |
| X-003 | 22 weeks | 18 weeks | V1 stronger — V2 schedule omits pen-test realistic window | 0.85 |
| X-004 | M1 = scaffolding only | M1 = scaffolding + core auth | V1 stronger — security posture: V2 ships auth endpoints before observability + ZAP baseline | 0.82 |
| X-005 | Rate-limit in M3 (with sessions) | Rate-limit in M4 (with security) | V1 stronger — rate-limit + session both Redis-keyed; coupling reduces context-switch | 0.65 |
| U-001 | Hash-chain audit + S3 object-lock | (absent) | V1 strictly stronger | 0.92 |
| U-002 | JWT signing-key risk + JWKS + kid + 15-min TTL | (R-007 partial) | V1 stronger | 0.85 |
| U-003 | SES failover for SendGrid | Queue + retry only | V1 stronger | 0.75 |
| U-004 | Tokenized user_id + crypto-shred | (absent) | V1 strictly stronger | 0.88 |
| U-005 | Bootstrap admin script (D2.7) | Empty-DB as test case only | V1 stronger — operational deliverable vs test | 0.72 |
| U-006 | (absent) | Per-user session cap (5, oldest-evict) | V2 strictly stronger — concede | 0.80 |
| U-007 | "multi-AZ" abstract | K8s HPA + PgBouncer + Sentinel | V2 stronger — concede shippability | 0.72 |
| U-008 | "idempotency token" mention | WATCH/MULTI/EXEC + dedicated test | V2 stronger — concede testing discipline | 0.70 |
| U-009 | RDS at-rest encryption | pgcrypto column-level on email | V2 stronger — defense-in-depth, concede | 0.72 |
| A-001 | Cookie-only (browser implicit) | Cookie-only (browser implicit) | Tied — both unstated; QUALIFY | 0.60 |
| A-002 | Email as canonical | Email as canonical | Tied — ACCEPT | 0.70 |
| A-003 | Sync audit on hot path | Sync audit on hot path | Tied weakness — REJECT, must model | 0.85 |
| A-004 | Implicit | Implicit | Tied — ACCEPT | 0.65 |
| A-005 | Multi-AZ explicit, region implicit | K8s + Sentinel, region implicit | Tied — QUALIFY | 0.65 |
| A-006 | Migration tool named, compat discipline implicit | Migration directory only | V1 slightly stronger; both QUALIFY | 0.60 |
| A-007 | Single-use mentioned, ordering unspecified | Single-use mentioned, ordering unspecified | Tied weakness — REJECT, must specify | 0.78 |
| A-008 | 22 weeks, team comp implicit | 18 weeks, team comp implicit | V1 stronger because schedule is *more achievable* with implicit single-team assumption | 0.68 |

**Aggregate (weighted by confidence × severity):** V1 is stronger on 22 diff points, V2 is stronger on 5 (U-006, U-007, U-008, U-009, partial C-004), tied on 8. V1's strengths concentrate in L3 state-mechanics invariants (audit chain, GDPR resolution, JWT rotation, family-tracking) — exactly the high-severity category. V2's strengths are deployment-runbook concreteness — important and mergeable, but downstream of the architectural commitments where V1 leads.
