# Round 2 Rebuttal — Advocate for Variant 2 (Sonnet Default)

**Author:** V2 Advocate
**Round:** 2 (Rebuttal)
**Date:** 2026-05-22

---

## Response to Criticisms

I extract every specific criticism V1 raised against V2 in Round 1 (round-1-advocate-v1.md) and Round 2 (round-2-rebuttal-v1.md), and respond to each.

### Criticism 1 — "V2's M2 ships endpoints that M3 retroactively modifies" (Round 1, Weaknesses-in-V2 #1)

**V1's claim:** V2 M2 login returns "session identifier placeholder"; M3 D3.5/D3.6 must retroactively update these to return AuthToken. M2 exit criteria validate a response shape that M3 changes, requiring re-testing. V1 calls this "rework V2 imposes on itself."

**Response: Genuine weakness, but V1 overstates the cost and understates the benefit.**

I already conceded this in Round 1. The retrofit is real: two deliverables (D3.5, D3.6) that update login and register to return AuthToken pairs. V2 M3 Effort estimates this at 2 days out of a 4-week milestone.

What V1 does not acknowledge is that the retrofit is *structurally simple*: it changes the return value of two endpoints from a session-string to an AuthToken object, while keeping the endpoint signatures, validation logic, error paths, rate limiting, lockout mechanics, and audit logging untouched. The M2 integration tests that validate login/register behavior test the *inputs and error paths* (401, 423, 409, 400, rate limiting), none of which change in M3. Only the 200/201 response-body assertions need updating. V1 frames this as "invalidates the integration tests, contract tests, audit-event shapes, and frontend assumptions" -- but V2 has no frontend until M5, no contract tests (by V2's design), and audit-event shapes do not change (the audit writer logs event types, not response shapes).

The benefit V1 dismisses is real: stakeholders can exercise real HTTP endpoints in Sprint 4, validate error behavior, and confirm anti-enumeration mechanics against a running service. V1's proposed Sprint-4 "Postman collection driving the token library through staged scenarios" (V1 Round 2 UC-1) is a library demo, not a service demo. Libraries do not expose rate-limiting, account lockout, or error-envelopment behavior -- endpoints do.

**Concession maintained.** But the cost is 2 days of bounded work, not an architectural rework.

### Criticism 2 — "allkeys-lru is a security posture downgrade" (Round 1, Weaknesses-in-V2 #2; Round 2 NE-2)

**V1's claim:** Under `allkeys-lru`, evicted lockout counters reset locked-out attackers to zero failed attempts. V2 does not address this cross-keyspace contamination. V1 NE-2 further argues that INV-05 ("Account lockout is atomic") holds only for non-evicted counters under `allkeys-lru`.

**Response: Partial concession on the contamination point; V1's NE-2 is directionally correct but overstates the practical risk.**

I concede that V2's `allkeys-lru` policy applies globally to the Redis instance and that, under memory pressure, lockout counters (`auth:lockout:<userId>`) and rate-limit sliding windows could be evicted alongside refresh tokens. This is a real contamination risk that V2 should address explicitly.

However, the practical severity is lower than V1 presents:

1. V2's Redis sizing (Appendix B, Operational Readiness, Capacity Planning) allocates 1 GB, with expected usage of ~50 MB for 100K tokens. Lockout counters and rate-limit windows add perhaps 5-10 MB. The system must grow 15-20x before eviction is even possible. V2's 70% monitoring alert triggers at 700 MB, providing weeks of lead time.

2. V2 INV-05 enforces lockout via *PostgreSQL* atomic UPDATE (not Redis). The variant-2-sonnet-default.md M2 D2.3 and the INV-05 enforcement location both specify: "PostgreSQL atomic UPDATE with WHERE clause: `UPDATE users SET failed_login_attempts = failed_login_attempts + 1 WHERE id = $1 RETURNING failed_login_attempts`." The `locked_until` column is in the `users` table in Postgres, not in Redis. V1's NE-2 assertion that "the lockout state itself lives in Redis" misreads V2's architecture. V2 stores lockout state durably in Postgres; Redis is used only for rate-limit counters (which are inherently tolerant of reset -- a rate-limit counter reset just allows slightly more requests until the counter rebuilds).

3. That said, V2 *does* use Redis for rate-limit sliding windows, and eviction of those counters is a nuisance. The correct mitigation -- which V2 should document -- is a separate Redis database or key-prefix with `volatile-lru` (evict only keys with TTL) rather than the broader `allkeys-lru`. This narrows the eviction candidate pool to TTL-bearing tokens while protecting the sliding-window counters, which also have TTLs but are cheaper to rebuild.

**Concession upgraded:** V2 should specify `volatile-lru` instead of `allkeys-lru` and should segregate rate-limit counters into a separate Redis database (db 1) from refresh/reset tokens (db 0). This is a documentation fix, not an architectural change.

### Criticism 3 — "Reset tokens in Redis lose all in-flight resets on Redis restart" (Round 1, Weaknesses-in-V2 #3)

**V1's claim:** Redis restart atomically invalidates every reset email in flight. Users who clicked "Forgot Password" 30 minutes ago receive a dead link with "Invalid or expired token" and no diagnostic.

**Response: Genuine trade-off, correctly identified, but overstated in severity.**

The worst case V1 describes is: Redis restarts, N users who received reset emails in the last hour must request a new reset email. The recovery path is: click "Forgot Password" again, receive a new email. This is a known UX pattern (Gmail, GitHub, AWS all handle it the same way). The user sees "This link has expired. Please request a new one." with a clickable "request a new link" button.

V1's Postgres-backed reset tokens survive Redis loss, which is genuinely stronger. But the cost of that strength is a full database table (`password_reset_tokens`) with a migration, a `SELECT FOR UPDATE` transactional pattern, and a periodic cleanup job for expired rows. For a token with a 1-hour lifespan and a cheap retry path, this is over-engineering.

For v1.0 of a greenfield service, the Redis approach is the correct trade-off: simpler code, faster performance, acceptable UX under failure. Post-GA, if Redis reliability proves problematic, the migration to Postgres is a single deliverable.

**No concession change from Round 1.** The trade-off is intentional and defensible.

### Criticism 4 — "GA before pen test" (Round 1, Weaknesses-in-V2 #4; Round 2 NE-4)

**V1's claim:** V2 M5 D5.7 ships GA 100% before M6 pen test. If the pen test finds a Critical, the blast radius is 100% of users. V1 NE-4 calls this "Low-probability/Catastrophic-impact" vs V1's "Low-probability/Critical-impact" at 1% staging.

**Response: This is V1's strongest structural argument. Partial concession with qualification.**

V1 is correct that shipping 100% GA before pen testing exposes the full user base. The sequence difference is real: V1 pen-tests at 1% rollout, V2 pen-tests after 100% rollout.

However, V1's framing omits three mitigating factors:

1. **V2's M5 beta is 10% for 2 full weeks.** During this period, the auth service handles real traffic at 10% with full monitoring. The pen test in V2's M6 runs against the same codebase that has been live for 2+ weeks. V1's pen test runs against code that has seen 1% traffic for days, not weeks. V2 actually accumulates more production-evidence time before the pen test than V1's timeline suggests.

2. **V2's M5 rollback triggers are explicit.** V2 D5.7 defines rollback criteria (p95 > 1000ms for 5 min, error > 5% for 2 min, Redis failures > 10/min, data corruption). If any Critical-pen-test-equivalent issue surfaces during the 2-week beta, V2's monitoring catches it and triggers rollback. The pen test is not the *only* security gate -- it is the *formal* security gate.

3. **V2's M6 entry criteria require 7 days of production traffic data.** This means V2 has at least 3 weeks of production exposure (1 week alpha + 2 weeks beta) before M6 starts. If a Critical vulnerability exists in the GA code, the probability of discovering it via monitoring during those 3 weeks is non-trivial.

**Concession:** V2 should add an explicit "security review checkpoint" at the end of M5 beta (before GA 100%) where the sec-reviewer reviews production logs, error patterns, and monitoring data for security anomalies. This creates a manual security gate before the 100% flip, reducing the "no security gate before GA" gap. Additionally, V2 should move the pen-test engagement to start *during* the M5 beta window (parallel with the 10% traffic period) rather than deferring it entirely to M6. This way, pen-test findings start landing while traffic is still at 10%.

### Criticism 5 — "V2 audit log retention is internally contradictory" (Round 1, Weaknesses-in-V2 #5)

**V1's claim:** V2 SOC2 mapping says "90-day retention" but M6 D6.2 exit criteria says "Confirm 12-month retention policy." If the extension step is missed, V2 fails SOC2.

**Response: Full concession. V2 has an inconsistency that V1 avoids.**

Already conceded in Round 1. The default should be 12-month from M2 D2.4 onward, not 90-day "extensible." V1 commits to 12-month from the start, which is the correct posture. V2 should align M2 D2.4 to create the audit_log table with 12-month partitioning from day one, eliminating the extension step entirely.

### Criticism 6 — "No spec-first artifact" (Round 1, Weaknesses-in-V2 #6; Round 2 NE-3)

**V1's claim:** No OpenAPI spec, no `@auth/contracts` package. Integration tests catch drift only after both sides are written. V1 NE-3 argues that `@auth/contracts` makes camelCase/snake_case field-name mismatches a compile-time error rather than a runtime failure.

**Response: Partial concession for team-growth scenarios; not a material concern at v1.0 team size.**

V1 NE-3's specific example -- frontend reads `display_name` while backend returns `displayName` -- is a real class of bug. I concede that a shared contracts package would catch this at compile time. However:

1. V2's TDD Section 7.1 specifies exact field names for UserProfile (`id`, `email`, `password_hash`, `display_name`, `created_at`, `updated_at`, `last_login_at`, `roles`, `consent_at`, `locked_until`, `failed_login_attempts`). The API response shape in V2 D3.4 uses camelCase conversion (`displayName`, `createdAt`) as is standard for JSON APIs. This is a single, well-documented mapping that a developer makes once. The probability of getting it wrong in a 3-5 person team working in one repository with shared code review is low.

2. V2's M5 integration tests explicitly validate the response shapes from D5.1 through D5.5. If the frontend reads a field the backend does not provide, the Playwright E2E test fails. This is a runtime catch, not a compile-time catch, but it catches the bug in Sprint 10, not in production.

3. V1's `@auth/contracts` package requires an internal npm registry (V1 D1.3 "published to internal registry"). If the organization does not have an internal npm registry, this is a hidden infrastructure dependency. V2 avoids this dependency entirely.

**Concession:** V2 should add a shared TypeScript interface file (not a published npm package) defining the API response shapes, checked into the monorepo. This gives 80% of the compile-time safety at 10% of the infrastructure cost. If the team grows post-GA, this file becomes the `@auth/contracts` package.

### Criticism 7 — "No threat model deliverable" (Round 1, Weaknesses-in-V2 #8)

**V1's claim:** V2 has no standalone STRIDE threat-model artifact. Security analysis is implicit until M6 pen testing.

**Response: V2 has a threat model, but it is formatted as a table rather than a standalone deliverable.**

V2 Section "Threat Model Summary" contains a 9-row threat table covering: credential brute-force, user enumeration, token theft (XSS), token theft (network), refresh token replay, password reset token reuse, privilege escalation, SQL injection, and timing attack. Each row maps to a control location (milestone + deliverable). This is a threat model in table format, not the absence of one.

I concede that V1's D1.6 format (a standalone STRIDE document, signed off by sec-reviewer in M1) is a better audit artifact. V2's threat model should be extracted into a standalone document and reviewed at M1 exit. But the *analysis content* is present; it is the *packaging and timing* that V1 improves on.

### Criticism 8 — "No anti-enumeration acceptance test until late" (Round 1, Weaknesses-in-V2 #9)

**V1's claim:** V2 M2 exit criteria uses 50ms variance (generous); V1 M3 D3.9 commits to +/- 25ms with explicit dummy-bcrypt mitigation in the deliverable text.

**Response: Partial concession on the variance window.**

V2's 50ms variance is generous given bcrypt's inherent latency variability under load. V1's +/- 25ms over 100 trials is a tighter standard. V2 should tighten to +/- 30ms over 100 trials, which is achievable with dummy-bcrypt normalization and provides a meaningful security margin without being fragile under CI hardware variability.

Regarding "dummy-hash mitigation not in the deliverable text" -- V2 D2.3 (login route description) explicitly states: "5th failure returns 423" and "generic 401 for all auth failures," and V2's risk RR-004 specifies "Dummy bcrypt verify for non-existent users." The mitigation is present in the risk register, which is the natural home for this detail. V1 places it in the deliverable spec. Both are valid locations; V1's is more prominent.

---

## Response to V1's New Evidence (Round 2)

### NE-1 — "V2's INV-08 is inconsistent with V2's audit-write semantics"

**V1's claim:** V2's synchronous audit writes have no transactional guarantee with the state-change row. If auth INSERT commits and audit INSERT fails, INV-08 is silently violated. V1's outbox pattern makes this structurally impossible.

**Response: Partial concession. V2 should add transactional wrapping. But the outbox pattern is not the only solution.**

V1 correctly identifies that V2's D2.4 audit writer inserts into `audit_log` without explicit transactional coupling to the auth state change. This is a real gap.

However, the fix is not necessarily the outbox pattern (which V1 adopts in M5 D5.2, meaning V1 itself does not have transactional audit logging until M5 -- the same milestone where V2 could add it). V2 can fix this in M2 D2.4 by wrapping the auth INSERT and audit INSERT in the same PostgreSQL transaction. This is a simpler pattern than the outbox and achieves the same atomicity for a single-service deployment:

```
BEGIN;
INSERT INTO users (...) VALUES (...);
INSERT INTO audit_log (...) VALUES (...);
COMMIT;
```

If either INSERT fails, the transaction rolls back and neither row persists. INV-08 holds. No outbox, no async publisher, no at-least-once drain complexity.

V1's outbox pattern is *more robust* for multi-service architectures where the audit consumer is a separate service. For v1.0 (single AuthService, single database), the same-transaction approach is sufficient and simpler.

**Concession:** V2 D2.4 should specify that audit writes are performed within the same database transaction as the state change. This closes the INV-08 gap without introducing the outbox pattern's complexity.

### NE-2 — "V2's INV-05 contradicts allkeys-lru"

**V1's claim:** Lockout counters stored in Redis can be evicted under `allkeys-lru`, making INV-05 conditional.

**Response: Factually incorrect. V2 stores lockout state in PostgreSQL, not Redis.**

V2 M2 D2.3 (login route) specifies: "increments failed_attempts on failure, locks account after 5 failures in 15 min window." The enforcement is via PostgreSQL: `UPDATE users SET failed_login_attempts = failed_login_attempts + 1 WHERE id = $1 RETURNING failed_login_attempts` (V2 M2 Risks table). The `locked_until` column is in the `users` table (V2 D1.1 schema). INV-05's enforcement location is "PostgreSQL atomic UPDATE + RETURNING pattern."

V2 does not store lockout counters in Redis. V1 appears to have conflated V2's architecture with V1's own `auth:lockout:<userId>` Redis key (V1 M3 Scope, line 153). This is a V1 convention, not a V2 convention. V2's lockout is durable by construction because it lives in Postgres.

V2 uses Redis for: (1) refresh tokens, (2) reset tokens, (3) rate-limit sliding windows. Only the rate-limit counters are affected by eviction, and rate-limit counter eviction is a nuisance, not a security incident (the counter resets, allowing slightly more requests until it rebuilds). The hard security control is the Postgres-backed account lockout, which is eviction-proof.

**No concession needed.** V1's NE-2 is based on a misreading of V2's lockout architecture.

### NE-3 — "@auth/contracts prevents field-name mismatches"

**V1's claim:** A shared contracts package makes camelCase/snake_case mismatches a compile-time error. V2 catches this only at integration-test time or potentially in production.

**Response: Addressed in Criticism 6 above.** The risk is real but bounded for a 3-5 person team in a monorepo. V2's mitigation: shared TypeScript interface file checked into the monorepo, enforced by code review. This is the 80/20 solution.

### NE-4 — "V2's GA-before-pen-test means 100% blast radius for Critical findings"

**V1's claim:** V2 ships 100% GA before pen testing, creating Low-probability/Catastrophic-impact vs V1's Low/Critical at 1%.

**Response: Addressed in Criticism 4 above.** V2 should move pen-test engagement to start during M5 beta, creating a security gate while traffic is at 10%. This reduces the blast radius from 100% to 10% during the pen-test finding window.

### NE-5 — "V1's rollout is mechanically gated, V2's requires human decisions"

**V1's claim:** V1 has auto-rollback on SLO violation (D6.5). V2 has go/no-go meetings with humans, which is less safe for an auth service.

**Response: V1 overstates V2's reliance on human gates.**

V2 D5.7 explicitly defines rollback triggers: "p95 > 1000ms for 5 min, error rate > 5% for 2 min, Redis failures > 10/min, data corruption." These are quantitative thresholds that trigger rollback, not subjective human judgment. The "go/no-go meeting" is a confirmation step on top of automated monitoring, not a substitute for it.

However, I concede that V2 does not have a dedicated auto-rollback *infrastructure* deliverable equivalent to V1's D6.5 ("Staged rollout dashboard with auto-rollback trigger on SLO violation"). V2's rollback is a human-operated procedure triggered by alerts. For a single-service deployment, this is adequate -- the engineer on call sees the alert, runs `kubectl rollout undo`, and confirms in the monitoring dashboard. V1's auto-rollback is a more mature operational posture, but it is also more engineering effort for a feature that may never fire.

**Concession:** V2 should add an explicit "automated rollback trigger" to D5.7: "If any rollback criterion is met for the specified duration, the on-call engineer is paged immediately, and a rollback script (`scripts/rollback-auth.sh`) is pre-validated and documented in the runbook." This is not auto-rollback (which requires Unleash/feature-flag infrastructure V2 does not explicitly call for), but it is a documented, tested procedure rather than an ad-hoc decision.

---

## Updated Assessment of V1

After V1's Round 1 and Round 2, my assessment of V1 has shifted on several axes.

### V1's strongest arguments (where V1 has strengthened its position)

1. **Pen-test-before-GA ordering (NE-4).** V1's Round 2 amplifies this beyond what Round 1 achieved. The blast-radius argument (1% vs 100%) is compelling. V2 should adopt V1's ordering or, at minimum, start the pen test during beta. This is V1's single strongest structural point.

2. **KMS audit posture (Round 2 Criticism 5 response).** V1's counter to V2's "K8s secrets require no approval" is effective: in any organization with real access control, `kubectl get secret` permissions are broader than KMS service-principal access. The SOC2 CC6.1 argument is real. V1 concedes the need for a fallback (Vault), which is the right addition.

3. **Edge-case catalog + invariant table combination.** V1's Round 2 response to Criticism 6 is balanced: "the catalog tells you how it can fail; the invariant table tells you what must hold." This is the correct synthesis. V1's catalog provides authoring guidance that V2's INV table alone does not.

### V1's weakest arguments (where V1 has conceded ground)

1. **GDPR erasure (V1 Round 2 Criticism 3).** V1 fully concedes and goes further: "erasure should ship in M4, which is stronger than V2's own placement in M6." This is a genuine upgrade that V2 should consider adopting. If V1's M4 placement is correct (and it is -- the revoke-all-sessions plumbing exists there), then V2's M6 placement is a real gap.

2. **Team sizing (V1 Round 2 Criticism 2).** V1 concedes that "capacity-equivalent" is better phrasing than "engineers-allocated." V2's point about headcount flexibility stands.

3. **Compliance bolt-on critique (V1 Round 2 Criticism 4).** V1's defense is technically correct (M5 finishes before production exposure), but the defense requires reading V1's timeline carefully. V1's M3/M4 emit events to a stub sink, and the durable audit table only lights up in M5. V1's argument is: "staging does not need durable audit." That is true, but it also means V1's M3/M4 integration tests run against a stub that accepts everything, while V2's M2 integration tests run against the real `audit_log` table from Sprint 3. V2's early-durable-audit posture catches audit-schema bugs (missing columns, wrong types, constraint violations) in M2, not M5.

### Points where I have moved closer to V1

- **Pen-test ordering:** V2 should start pen testing during M5 beta, not after GA. Partial move.
- **Transactional audit writes:** V2 should wrap auth + audit in the same database transaction. Full move.
- **Retention default:** V2 should default to 12-month, not 90-day. Full move (already conceded).
- **Redis policy:** V2 should narrow from `allkeys-lru` to `volatile-lru` with database segregation. Partial move.
- **KMS for post-GA:** V2 should plan KMS adoption for the Q3 SOC2 audit window. The Q3 audit timeline does make KMS a stronger position than I credited in Round 1. Partial move -- V2 can adopt KMS in M6 as part of compliance validation, which gives the auditor the right answer without blocking M3 development.

---

## New Evidence (V2 NE-1 through NE-4)

### NE-1 — V1's outbox pattern introduces M5-dependent audit latency, contradicting V1's "no compliance bolt-on" claim

V1 Section 11 Sequencing Rationale (variant-1-opus-default.md line 543): "Audit-event emission is wired into M3 endpoints from day one (events go to a stub sink). M5 lights up the durable audit table, dashboards, and alerts."

V1 M5 D5.2 (line 291): "Audit-event emitter wired into M3/M4 endpoints with at-least-once semantics (outbox pattern)."

V1's outbox pattern writes audit events to a transactional outbox table in the same DB transaction as the state change, then an async publisher drains to the long-term audit store. This is architecturally sound but introduces a timing gap: between the state-change commit and the async-drain completion, the audit event exists only in the outbox table, not in the queryable `auth_audit_log`. If Jordan-the-admin queries the audit log during this window, the event is missing.

V2's synchronous write (when wrapped in the same transaction, per my NE-1 response above) has zero drain latency: the event is in the audit table the instant the transaction commits. For SOC2 evidence collection, synchronous writes produce immediately queryable records. V1's outbox introduces a configurable-but-nonzero replication lag.

This is not a reason to reject the outbox pattern -- it is the correct pattern for multi-service architectures. But for v1.0 single-service, the simpler synchronous-write-in-same-transaction approach produces stronger audit-immediacy guarantees.

### NE-2 — V1's STRIDE threat model in M1 (D1.6) predates the implementation that satisfies its mitigations

V1 D1.6 requires a STRIDE threat model signed off by sec-reviewer in M1 (Sprints 1-2). This is before any code exists -- the threat model is informed by the PRD and TDD, not by implementation. V1 presents this as a strength: "security analysis before code exists."

But threat modeling an implementation you have not built risks identifying threats that the eventual implementation does not have, and missing threats that the implementation introduces. The STRIDE model will contain rows like "JWT alg confusion" (a threat that `JwtService` handles in M2) and "refresh-token rotation race" (handled by atomic Lua in M2 D2.6). These are *correct* threats to identify, but the mitigation column will say "handled in M2" -- meaning the threat model is speculative until M2 ships and proves the mitigation works.

V2's approach (threat model table derived from the PRD, validated against implementation during sec-reviewer sign-offs at each milestone exit) produces a threat model that is incrementally grounded in real code. By M6, V2's threat model is fully validated against implementation. By M6, V1's threat model is also validated -- but V1's M1 artifact was speculative for 5 milestones.

The practical difference: V1's D1.6 is a better *process artifact* for auditors (it shows security thinking from day 1). V2's approach is a better *technical artifact* (every threat row is backed by running code). The merged variant should have both: an early STRIDE analysis in M1 and an implementation-validated update at each milestone exit.

### NE-3 — V1's frontend coupling in M3 creates a brittle dependency graph

V1 M3 ships LoginPage, RegisterPage, and AuthProvider (D3.8) alongside backend endpoints. V1 argues this eliminates mock drift. But it introduces a different risk: the frontend components in M3 are written against backend endpoints that have not yet been hardened by M4 (password reset) or M5 (compliance). When M4 changes the backend (adding reset-confirm's session-revocation behavior, which affects AuthProvider's token state), the M3 frontend must be re-visited.

V2's separated frontend (M5) builds against a *frozen* backend API. M4's changes to session invalidation, reset flows, and audit logging are all complete before the frontend team starts. The frontend team in V2 writes code once; the frontend team in V1 writes code that may need updates as M4 and M5 modify backend behavior.

This is not a fatal flaw in V1 -- the `@auth/contracts` package absorbs the shape changes -- but it is a coordination cost V1 does not account for: the frontend team must be available for M3 *and* re-engaged for M4/M5 backend changes that affect frontend behavior. V2's 4-week FE engagement (M5 only) avoids this multi-engagement overhead.

### NE-4 — V2's PasswordHasher in M1 enables a security decision that V1 defers

V2 M1 D1.3 places PasswordHasher with benchmark testing in Sprint 1-2. V1 defers PasswordHasher to M3 D3.5 (Sprint 5-7). The benchmark result (bcrypt cost 12 under 500ms on production CPU) is a security-architecture decision: if cost 12 is too slow, the team must decide between (a) reducing to cost 11, (b) adding horizontal replicas, or (c) accepting higher latency.

V2 makes this decision in Sprint 2, before any endpoint code exists. If cost 12 is too slow, the fix is a one-line config change in M1. V1 makes this decision in Sprint 6-7, when login endpoints, frontend components, and rate limiters are already built against the cost-12 assumption. If cost 12 proves too slow in V1, the fix touches load-test results, frontend timeout configurations, rate-limit budgets, and the M3 exit criteria.

Early discovery of a constraint that affects performance budgets, capacity planning, and security posture is strictly better than late discovery. V2's M1 placement of PasswordHasher is the correct sequencing for this specific component.

---

## Updated Concessions

Beyond my Round 1 concessions (retrofitting M2 endpoints, `allkeys-lru` risk, SOC2 retention inconsistency, no OpenAPI spec), Round 2 surfaces four additional concessions.

### UC-1 — V2's audit writes need transactional wrapping

V1's NE-1 correctly identifies that V2's D2.4 synchronous audit writes are not transactionally coupled to the state change. V2 should specify that the auth-row INSERT and audit-row INSERT occur within the same database transaction. This is a one-sentence addition to D2.4, not an architectural change.

### UC-2 — V2's Redis policy should be narrowed

V1's Criticism 2 and NE-2 (where NE-2 misidentifies the lockout storage but correctly flags rate-limit counter vulnerability) convince me that `allkeys-lru` is too broad. V2 should specify `volatile-lru` (evict only TTL-bearing keys) with separate Redis databases for tokens (db 0) and rate-limit counters (db 1). This preserves V2's graceful-degradation philosophy for tokens while protecting operational counters.

### UC-3 — V2 should start pen testing during M5 beta

V1's NE-4 is the strongest argument V1 advances. V2's GA-before-pen-test ordering exposes 100% of users to untested attack surface. V2 should move pen-test engagement to start during M5 Phase 2 (beta 10%), with findings landing while traffic is still capped. This does not change V2's milestone structure (pen-test coordination remains in M6), but it advances the engagement start date to reduce blast radius.

### UC-4 — V2's GDPR erasure should move to M4

V1's Round 2 Criticism 3 response argues that erasure should ship in M4, not M6, because the technical primitives (nullify PII, revoke all sessions) are the same as password reset. This is correct. V2 should add a DELETE /auth/me deliverable to M4 alongside the reset-confirm endpoint, using the same TokenManager.revokeAllForUser() primitive. This ensures erasure is available before any production exposure in M5.

---

## Closing Posture

After two rounds of debate, my assessment is:

**V1's structural spine (token-first, `noeviction`, KMS, OpenAPI, outbox, hardening-before-rollout) is optimized for a problem profile where SOC2 audit readiness is the binding constraint and the team can absorb heavier ceremony. V2's structural spine (auth-first, separated frontend, `volatile-lru`, K8s secrets, code-first, GA-before-pen) is optimized for a problem profile where team size is small, time-to-demo matters politically, and ceremony overhead delays real engineering work.**

The debate has moved both positions closer to the center:

- V2 should adopt: transactional audit writes, `volatile-lru` Redis policy, pen-test engagement during beta, GDPR erasure in M4, 12-month retention default, and a shared TypeScript interface file.
- V1 should adopt: GDPR erasure endpoint (in M4), invariant table format, infrastructure cost estimate, open-questions resolution log, capacity-equivalent team language, Sprint-4 demo artifact, and KMS fallback documentation.

The highest-impact unresolved disagreement is **pen-test ordering**. V1's position (pen-test before staged rollout) is the safer default for an authentication service. V2's mitigation (start pen test during beta at 10%, not after GA at 100%) narrows but does not eliminate the gap. For a final merged variant, V1's ordering should prevail, with V2's earlier-stakeholder-demo practice grafted on as a process addition.

The second highest-impact disagreement is **build order**. V2's auth-first order delivers running endpoints two sprints earlier with a bounded 2-day retrofit cost. V1's token-first order delivers property-tested crypto isolation with no retrofit. For a team that values early integration testing and stakeholder confidence, V2's order is the pragmatic choice. For a team that values security-surface isolation above all else, V1's order is correct. The merged variant should follow V2's order but include V1's Sprint-4 token-library demo artifact as a parallel track.

The third highest-impact disagreement is **key management**. V2's K8s-secrets posture is defensible for development and staging. V1's KMS posture is required for the Q3 SOC2 audit window. The merged variant should use K8s secrets for M1-M3 development, then adopt KMS in M6 as a compliance-validation deliverable, giving the auditor the answer they need without blocking M3 development on KMS provisioning.

**Final position:** V2 is the more executable plan for a 3-5 person team shipping v1.0. V1 is the more auditable plan for a SOC2-bound service. A merged variant should take V2's execution spine and graft V1's compliance posture onto M6, while adopting each variant's concessions as documented above.
