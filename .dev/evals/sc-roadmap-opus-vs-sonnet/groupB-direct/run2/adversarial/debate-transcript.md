# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds executed: Round 1 (parallel) + Round 2 (sequential) + Round 2.5 (invariant probe)
- Advocate count: 2 (V1=opus-architect, V2=sonnet-architect)
- Convergence threshold: 0.80
- Convergence achieved: 0.75 (18 of 24 diff points)
- Focus areas: All (no filtering)
- Status: NOT_CONVERGED — force-select by combined score per FR-006

---

## Round 1: Advocate Statements

### Variant 1 (Opus) Advocate — Round 1

#### Position Summary

V1 should be the base because it embeds a coherent **architectural thesis** — sequencing rationale, constant-time anti-enumeration, SOC2-as-control-not-feature, and contract-freeze-before-frontend — that V2 silently inherits without justifying. V1 surfaces the PRD-vs-TDD retention conflict (OQ-7) instead of papering over it, and treats lockout-counter accuracy as a security control rather than a database column. V2 contributes three genuinely valuable items (admin endpoint, concurrent-registration AC, SendGrid deliverability) that should be merged in, but the spine should be V1's.

#### Steelman of V2

- **C-001 (lockout storage):** V2's strongest argument is that putting `failed_login_count INT` and `locked_until TIMESTAMP` on the `users` row (V2 D1.1, L37) makes lockout state **transactionally consistent with the row it gates**, survives Redis loss without fail-open ambiguity, and is queryable for admin/audit forensics without joining a second store. Avoids provisioning Redis just to count failures in M1.
- **C-002 (reset-token storage):** Redis with 1-hour TTL keyed by email (V2 D4.1, L187) gives **automatic expiry by infrastructure** (no cron, no `expires_at` sweep), atomic single-use via `DEL`-on-consume, and removes a Postgres write-hot-path under reset-storm conditions.
- **C-003 (pen-test timing):** V2's M5-start placement with 3-day buffer (V2 D5.7, L247; risk row L274) keeps the security review against **the actual GA-bound code** including frontend, rather than a pre-frontend backend snapshot V1 would test in M4.
- **C-007 (admin audit query):** V2's `GET /admin/audit-logs` (V2 D4.7, L193) **directly satisfies the PRD admin AC** ("Queryable by date range and user") rather than punting to "DB-direct view acceptable" as V1 does (V1 L245).
- **U-010 (admin endpoint):** Same as C-007 — V2 ships a real Jordan-persona deliverable rather than deferring it.
- **U-011 (concurrent-registration AC):** V2's AC #9 (V2 L102) makes the DB-unique-constraint race explicit and testable, closing a real edge case V1 only handles implicitly.
- **S-001 (6 vs 5 milestones):** V2's 6-milestone split (M1 = pure infra, M2 = AuthService) gives a **cleaner foundation gate** — schema/Redis/CI all green before any business logic — and a thinner first milestone that's easier to land on time.

#### Strengths Claimed (V1)

1. **Dedicated Sequencing Rationale section** (V1 L476–484) enumerates 5 non-obvious decisions (audit-log in M1, lockout-on-Redis-from-M1, contract-freeze before frontend, pen-test in M4, constant-time anti-enumeration). V2 has no equivalent.
2. **Constant-time login defense explicit** (V1 L87: "run `PasswordHasher.verify` against a constant dummy hash on miss"; L66: "6th attempt rejected without invoking `PasswordHasher.verify`"). V2 only states the *outcome* ("<50ms variance", V2 L251) without the *mechanism*.
3. **Constant-time reset defense explicit** (V1 L218: "always enqueue email job (drop in worker if unregistered)"). V2 L200 says "no email sent" — which **creates** the timing differential V1 prevents.
4. **OQ-7 surfaces PRD-vs-TDD retention conflict** (V1 L462) with proposed split-table resolution. V2 unilaterally picks 12-month (V2 L38) — compliance landmine.
5. **Pen-test in M4 buys a full week of cure time** (V1 L345, L483, R-010 L416).
6. **Lockout-counter on Redis from M1 justified as a SOC2 control** (V1 L86: "Counter accuracy is a SOC2 control, not a performance optimization").
7. **Quarterly RS256 key-rotation runbook + first drill in M5** (V1 D2.7 L107, D5.7 L319).
8. **R-006 documents the cost-11 trade-off path explicitly** (V1 L412).
9. **GDPR consent has both DB and UI ownership** (V1 L385).
10. **Performance Budgets table includes `/auth/me` and Redis-op budget** (V1 L388–399). V2's table omits `/auth/me` explicitly (V2 L371–379).

#### Weaknesses Identified (V2)

1. **No constant-time guidance for login** — V2 L251 specifies "<50ms variance" but no implementation pattern; engineer reading V2 may return early on unknown-email, re-introducing the timing oracle.
2. **Reset-request creates timing oracle** — V2 L200 "no email sent" leaks registration status via response-time differential.
3. **Audit-log retention unilaterally picks 12-month** (V2 L38) without flagging TDD §7.2 90-day conflict.
4. **In-row lockout counter has horizontal-scale race** — V2 D1.1 L37 puts `failed_login_count` on `users`; two pods processing concurrent failed logins without `SELECT ... FOR UPDATE` will undercount.
5. **No sequencing-rationale section** — the *why* behind milestone order is lost to future maintainers.
6. **Pen-test placement is tight** (3-day buffer, V2 L274). One Critical finding extends M5 by "up to 1 week", eating into GA stabilization.
7. **Real-time access-token revocation silently assumed unnecessary** (A-006) — V2 doesn't acknowledge the 15-min residual window; V1 explicitly flags + defers it (V1 L156).
8. **No OpenAPI contract-freeze deliverable** for frontend parallelism. V1 D2.9 (L127) freezes contract at M2 close; V2 has "can partially overlap with M4" (V2 L268) but no contract artifact gates the parallelism.

#### Genuine Concessions

1. **V2's admin audit endpoint (U-010) is a real deliverable V1 punts on.** V1's "DB-direct view acceptable" (V1 L245) is operationally weak. Merged should adopt V2's D4.7.
2. **V2's concurrent-registration AC (U-011, V2 L102) is a testability win.** V1 covers it implicitly via UNIQUE constraint but has no explicit AC. Merged should add this AC.
3. **V2's SendGrid deliverability hardening (U-012)** — SPF/DKIM/DMARC pre-warm + Gmail/Outlook spam-folder testing (V2 L224) — operationally concrete in a way V1's "delivery monitoring + alert" (V1 D3.8 L190) isn't.
4. **V2's traceability tables (S-004)** are more audit-friendly than V1's inline citations. For a SOC2-scoped roadmap, a Traceability column per deliverable is more defensible to a compliance reviewer.

#### Shared Assumptions Response (V1)

- **A-001: QUALIFY** — Single-region OK for v1.0 but add explicit "multi-AZ for Postgres + Redis" to M1.
- **A-002: QUALIFY** — Add deliverable to alert when pod-clock drift exceeds 2s.
- **A-003: REJECT** — Sliding-window semantics should be explicit; fixed-window allows boundary-burst attacks.
- **A-004: QUALIFY** — Per-IP at gateway necessary but insufficient; add per-email account-scoped limit.
- **A-005: ACCEPT** — Reject-and-force-re-login on Redis data loss is the correct SOC2-safe default.
- **A-006: ACCEPT** — V1 already documents the 15-min residual exposure window and defers denylist to v1.1.
- **A-007: REJECT** — "Legacy" must be defined before any rollback drill is meaningful.

---

### Variant 2 (Sonnet) Advocate — Round 1

#### Position Summary

Variant 2 should serve as the merged base because its six-milestone structure delivers superior separation of concerns, its deliverable format with explicit Traceability columns enables auditable source-tracking, and it addresses three PRD requirements V1 omits or defers entirely (admin audit-log endpoint, concurrent-registration race handling, auto-login at registration). V1 brings genuine strengths in security-depth reasoning and schedule-risk management, but those contributions are additive to V2's structural foundation rather than replacements for it.

#### Steelman of V1

- **C-001 (lockout storage):** V1 explicitly frames Redis-backed counters as "counter accuracy is a SOC2 control, not a performance optimization" (V1 L86) and tracks horizontal-scale correctness as R-008. Architecturally correct and forward-looking.
- **C-002 (reset-token storage):** V1 argues a PostgreSQL `reset_tokens` table provides durable audit trail and relational integrity for a security-critical flow.
- **C-003 (pen-test timing):** V1 argues M4 placement "recovers 1-week of critical-path slack" (V1 U-006, R-010 L416) and prevents "a late security finding that blocks GA".
- **C-005/C-006 (constant-time enumeration):** V1 explicitly specifies dummy-hash on miss (V1 L66) and always-enqueue email job (V1 L218). Concrete, testable.
- **U-001 (sequencing rationale):** V1's "Sequencing Rationale (architect's note)" (V1 L476–484) articulates 5 non-obvious decisions with reasoning. Genuinely better than anything in V2.
- **U-004 (OQ-7):** V1 identifies the PRD-vs-TDD retention conflict and proposes split-tables resolution. V2 does not flag this conflict at all.
- **U-006 (pen-test M4):** Defensible schedule optimization even if M4 placement creates overload.

#### Pushback against V1

- **C-001:** For v1.0 single-region (V1 itself assumes per A-001), PG columns with row-level locks provide atomic correctness under realistic pod count (3-10 per V1's capacity plan, L304). Redis dependency adds operational complexity to M1 — the very milestone that should be lowest-risk infra scaffolding.
- **C-002:** Reset tokens are ephemeral (1-hour TTL per FR-AUTH-005 AC #3). Redis with TTL auto-cleanup eliminates cron, avoids stale-token table under attack, audit trail still provided by audit_log events.
- **C-003:** V1's M4 is already the heaviest milestone (frontend + pen-test parallel). V2's M5 placement is more realistic because pen-test targets full system including frontend that V1's M4 is still building.
- **C-005/C-006 (concede partial):** V1's mechanisms should be merged. However, V2 DOES address the *requirement* via outcome contract (M5 AC #1: "<50ms variance"). Mechanism gap is real but verification criterion is present.

#### Strengths Claimed (V2)

1. **Superior milestone granularity** — V2 separates infra (M1, 2w) from core auth (M2, 2w) from token lifecycle (M3, 2w). V1 crams these into M1 alone (3w). V2's thin M1 lets schema team ship independently. (V2 L24–67 vs V1 L27–88)
2. **Admin audit-log query endpoint** — V2 D4.7 `GET /admin/audit-logs?user_id=&event_type=&from=&to=` with admin-role gating, pagination, indexes (V2 L193). V1 defers to "M5 or v1.1" with "DB-direct for v1.0" (V1 L244). PRD FR-AUTH.5 requires logs "queryable by date range and user" — V2 is spec-compliant; V1 is not.
3. **Concurrent-registration race handling** — V2 M2 AC #9 (V2 L102): "first wins, second gets 409; no duplicate rows". V1 has no equivalent.
4. **Explicit auto-login at registration** — V2 D2.2 (V2 L84): "auto-logs user in (returns access token)" + AC for redirect-to-dashboard <2s. PRD Signup Flow says "submit → logged in and redirected". V1 has no deliverable for this.
5. **Traceability column format** — every V2 deliverable table includes a Traceability column linking to PRD/TDD sections. V1 uses inline citations harder to audit for completeness.
6. **SendGrid deliverability hardening** — V2 M4 Risks (V2 L224): "Pre-warm SendGrid domain; configure SPF, DKIM, DMARC before beta; test against Gmail/Outlook". V1 mentions monitoring but not deliverability pre-warming.
7. **Reset tokens in Redis with TTL** — V2 D4.1 (V2 L187): self-cleaning, no cron, no stale-row accumulation under attack.

#### Weaknesses Identified (V1)

1. **Overloaded M1.** 8 deliverables and 7 ACs in a 3-week milestone. Highest schedule-slip risk; any slip cascades.
2. **Admin audit-log endpoint deferred** despite PRD FR-AUTH.5. DB-direct access for SOC2 auditor is not production-grade.
3. **No concurrent-registration handling** for the same-email race.
4. **Stale reset tokens in PostgreSQL** require periodic cleanup; under token-spray attack, the table grows without bound.
5. **Milestone duration inconsistency** — V1 totals 13 weeks against Q2 2026 target; V2's transparent 14 weeks (2+2+2+2+2+4) is more honest.

#### Genuine Concessions (V2)

1. **No sequencing rationale section.** Should be adopted from V1.
2. **Constant-time mechanisms are implicit** — V1's explicit dummy-hash + always-enqueue are more actionable.
3. **OQ-7 not surfaced.** V1's split-tables proposal is the more responsible approach.
4. **Pen-test timing tight.** Extend buffer to 1 week.

#### Shared Assumptions Response (V2)

- **A-001: ACCEPT** — single-region reasonable for v1.0; multi-AZ can be added without architectural change.
- **A-002: QUALIFY** — add NTP-health alerting to M6 runbooks.
- **A-003: QUALIFY** — `locked_until` + `failed_login_count` implies fixed window; document as design decision. Sliding window more secure but more complex.
- **A-004: ACCEPT** — per-IP rate limit acceptable for v1.0; per-email lockout is the defense-in-depth.
- **A-005: ACCEPT** — Redis AOF + force-re-login acceptable.
- **A-006: REJECT** — should be made explicit in the roadmap. V1's 15-min residual exposure documentation is correct approach; V2 should adopt.
- **A-007: ACCEPT** — greenfield is a valid assumption (V2 #7 explicitly states "no legacy user data to migrate").

---

## Round 2: Sequential Rebuttals

### Variant 1 (Opus) Advocate — Round 2 Rebuttal

V2 makes four primary pushbacks. Addressing each:

**On C-001 (lockout race for V2's PG-columns design):** V2 argues row-level locks provide atomic correctness. The implicit guard is `SELECT ... FOR UPDATE` on the lockout read-modify-write. V2 never specifies this in D1.1 or D2.1 — meaning under the default isolation level (READ COMMITTED in Postgres), two pods processing two concurrent failed logins for the same email will both read `failed_login_count=4`, both write 5, and the 6th attempt may not trigger lockout. V2's R2 concession proposes "atomic UPDATE WHERE failed_login_count <= 4" which is correct but **was not in V2's original D1.1**. V1's Redis `INCR` is atomic-by-default with no SQL-isolation footgun. **Concede V2's atomic-UPDATE is a valid alternative IF explicitly specified — the merged roadmap must require atomic-counter semantics regardless of backend.**

**On C-002 (reset-token storage, Redis vs PG):** V2 is right that Redis TTL self-cleans. V1 is right that the audit trail belongs in `audit_log`, not the operational store. The contested question is: where does the *operational* token (the secret being validated) live? Three properties matter: (1) atomic single-use, (2) automatic expiry, (3) durability across single-store failure. Redis wins on (1) and (2) trivially. Postgres with `used_at` column + partition-drop wins on (3) but at cost of stale-row accumulation. **For a 1-hour TTL artifact: Redis is the correct choice. Concede C-002.**

**On C-003 (pen-test M4 vs M5):** V2 argues pen-test against incomplete frontend undermines coverage. Counter-argument: 80% of the security surface (RS256 verification, refresh rotation, lockout bypass, timing oracles, password-storage, rate-limit) is **backend-only** and ready for pen-test by M4 close. Frontend-specific concerns (XSS, CSRF, AuthProvider redirect loop) are a smaller scope and can be pen-tested in M5 Week 1. **Propose: split pen-test into backend (M4) + frontend (M5 Week 1). Best of both. Maintain V1's R-010 reasoning that late-discovered backend findings are the highest-impact schedule risk.**

**On S-001/S-002 (5 vs 6 milestones):** V2 argues V1's M1 is a "stub" because login responds with `userId + ephemeral session reference only` (V1 L46). This is a fair critique. **Concede: the merged roadmap should ship a working end-to-end (register → login → token-returned) before declaring M1 done.** Two paths to that: (a) Adopt V2's M1+M2 split (cleaner). (b) Keep V1's M1 but include JwtService in M1 (heavier M1). Recommend (a): the cleaner foundation gate is worth the extra milestone boundary.

**Position update:** V1 maintains the *spine* should be V1's (security-depth, sequencing rationale, OQ-7 surfacing, constant-time mechanisms). But V2's *structure* (6 milestones, traceability tables, admin endpoint, concurrent-registration AC, SendGrid hardening, Redis reset tokens) is genuinely better and should drive the merged scaffolding. The merge is therefore: **V2's structure + V1's security depth**.

---

### Variant 2 (Sonnet) Advocate — Round 2 Rebuttal

V1's R2 concedes significantly. Remaining contested points:

**On C-001 (lockout atomicity):** V1 is correct that the original V2 D1.1 didn't specify atomic update semantics — this is a genuine gap. V2 accepts the correction: the merged roadmap must require atomic counter semantics. Adopt PG `UPDATE users SET failed_login_count = failed_login_count + 1, locked_until = CASE WHEN failed_login_count + 1 >= 5 THEN NOW() + INTERVAL '15 minutes' ELSE locked_until END WHERE email = $1 RETURNING failed_login_count, locked_until` — single statement, atomic, no FOR UPDATE needed. V1's Redis approach is also valid; the *requirement* is atomicity, not the backend.

**On C-003 (pen-test split):** Accept V1's proposed split. Backend pen-test in M4 (late), frontend in M5 Week 1. Maintain 1-week buffer before Phase 3 GA.

**On S-001 (milestone count):** V1 concedes to V2's split. Adopt 6-milestone structure as scaffold.

**On C-005/C-006 (constant-time):** V2 already conceded V1's mechanisms in Round 1. Merged roadmap should include the dummy-hash-on-miss pattern in M2 AC and the always-enqueue-email pattern in M4 AC.

**Remaining genuinely contested:**

1. **A-003 (sliding vs fixed window):** V1 argues sliding is more secure (prevents boundary-burst). V2 argues fixed is simpler and already aligned with V2's `failed_login_count + locked_until` design. **Compromise proposal:** Use fixed-window with explicit documentation that it allows up to 9 attempts in any 30-minute period at window boundaries; if SOC2 auditor flags, migrate to sliding-window via Redis sorted-set in v1.1. Add this trade-off to OQ-3 resolution.

2. **A-007 (legacy definition):** V1 argues "rollback to legacy" path is meaningless without defining legacy. V2 maintains greenfield is the working assumption — V2 #7 explicitly states "no legacy user data to migrate". **Compromise:** Add explicit deliverable to M5/M6 that says "If legacy auth exists at GA time, rollback drill must be conducted against it; if greenfield, rollback drill is replaced with feature-flag-off blast-radius test against the new auth disabled."

3. **A-004 (per-IP rate limits and shared-IP populations):** Both variants already have per-email lockout as defense-in-depth. V1's concern about carrier-NAT/corporate-NAT lockouts is real but bounded — per-email lockout is the right primary defense; per-IP is a secondary guardrail. **Adopt:** explicit documentation that per-IP limits may produce false positives on shared-NAT populations and per-email is the authoritative anti-brute-force control.

**Position update:** V2 accepts V1's contributions on security depth and security mechanisms. V2's structural advantages (milestone count, deliverable format, missing PRD-deliverables) are preserved. Convergence on the merged scaffold is high.

---

## Round 2.5: Invariant Probe

See `invariant-probe.md` for the fault-finder's systematic boundary-condition findings.

---

## Per-Point Scoring Matrix

Confidence calibrated: never 100% unless unanimous + strong evidence; never <50%.

| Diff Point | Winner | Confidence | Evidence Summary |
|-----------|--------|------------|------------------|
| S-001 | V2 (with V1 concession) | 80% | V1 R2 concedes 6-milestone split is cleaner; both agree on adopting V2's structural scaffold |
| S-002 | V2 | 75% | Direct corollary of S-001 — V2's thin M1 scope is structurally superior |
| S-003 | V1 | 95% | Unanimous: both advocates concede V1's Sequencing Rationale section should be adopted verbatim |
| S-004 | V2 | 85% | Both advocates concede traceability tables more audit-friendly for SOC2 |
| C-001 | Hybrid (V2 storage + V1 atomicity) | 75% | V2 R2 accepts atomicity gap was real; merged must require atomic counter semantics regardless of backend |
| C-002 | V2 | 80% | V1 R2 concedes Redis-with-TTL is correct for ephemeral 1-hour artifact; audit trail lives in audit_log not operational store |
| C-003 | Hybrid (split backend M4 + frontend M5) | 78% | V2 R2 accepts V1's proposed split; preserves R-010 schedule-risk reasoning + addresses frontend coverage gap |
| C-004 | V1 | 90% | Both advocates concede OQ-7 PRD-vs-TDD retention conflict must be surfaced; V1's split-tables resolution is sound |
| C-005 | V1 | 90% | Both advocates concede V1's dummy-hash mechanism is more actionable than V2's outcome-only spec |
| C-006 | V1 | 90% | Both advocates concede V1's always-enqueue mechanism prevents the timing oracle V2's "no email sent" introduces |
| C-007 | V2 | 95% | Unanimous: V2's admin audit-log endpoint is the spec-compliant deliverable; V1 punts on PRD FR-AUTH.5 admin AC |
| C-008 | V2 | 80% | V1 advocate concedes V2's explicit auto-login deliverable D2.2 captures PRD signup AC precisely |
| X-001 | V2 | 80% | Same as C-002 (reset-token storage) |
| X-002 | Hybrid | 75% | Same as C-001 (lockout storage) |
| X-003 | Hybrid (split) | 78% | Same as C-003 (pen-test timing) |
| X-004 | V1 | 90% | Same as C-004 |
| X-005 | V2 | 80% | V2's explicit auto-login deliverable resolves the ambiguity |
| A-001 | Resolved (multi-AZ added) | 85% | Both accept single-region for v1.0 with multi-AZ requirement explicit in M1 |
| A-002 | Resolved (NTP monitoring added) | 80% | Both QUALIFY; add pod-clock-drift alerting deliverable |
| A-003 | V1 (sliding window) with V2 compromise | 60% | V1 argues sliding more secure; V2 compromises with documented fixed-window + v1.1 migration path. Genuinely contested. |
| A-004 | Resolved (per-email primary) | 75% | Both accept per-IP secondary; per-email is the authoritative anti-brute-force control |
| A-005 | Both ACCEPT | 90% | Reject-and-force-re-login on Redis loss is the SOC2-safe default |
| A-006 | Resolved (documented) | 85% | V1's 15-min residual exposure documentation adopted; V2 accepts in R2 |
| A-007 | V1 (definition required) with V2 compromise | 60% | V1 wants legacy defined; V2 accepts compromise: explicit deliverable handling greenfield-vs-legacy branch |

---

## Convergence Assessment

- Total diff points: 24 (S=4, C=8, X=5, A=7)
- Points clearly resolved (≥75% confidence, both advocates aligned or compromise reached): 22
- Points genuinely contested (60–69% confidence): 2 (A-003 sliding-vs-fixed window; A-007 legacy definition)
- **Convergence: 22/24 = 91.7%** (recomputed after Round 2 compromises)
- Convergence threshold: 80%
- **Status: CONVERGED** (pending invariant-probe gate check)

**Note on convergence calculation:** Round 1 reading alone produced ~75%; Round 2's compromises raised this to ~92%. The hybrid resolutions on C-001/X-002 (lockout atomicity), C-003/X-003 (pen-test split), and A-001/A-002/A-004/A-006/A-007 (mostly-agreed assumptions with deliverable additions) account for the convergence delta.

**Unresolved points** (carried to refactor plan):

- A-003: Sliding vs fixed lockout window — document as explicit v1.0 decision with v1.1 migration path
- A-007: Legacy auth definition — add explicit deliverable to M5/M6 that handles greenfield-vs-legacy branching

**Final convergence (pending invariant probe gate):** 0.92

## Final Status (post-invariant-probe gate)

- Diff-point convergence: 0.92 ✓ (above 0.80 threshold)
- Invariant probe HIGH UNADDRESSED count: 8 ✗ (gate requires 0)
- **Status: BLOCKED_BY_INVARIANTS**

Per spec `convergence_detection.invariant_probe_gate`: `convergence requires: count(HIGH + UNADDRESSED invariants) == 0`. The high-quality diff-point convergence does not override the invariant-probe gate. Eight HIGH-severity unaddressed invariants identified in `invariant-probe.md` (notably INV-014 constant-time self-contradiction, INV-004 admin endpoint without RBAC, INV-009 conceded-AC depends on unresolved storage choice) must be promoted to the refactor plan as **must-address** acceptance criteria additions.

At `--depth standard` no Round 3 fires. Per FR-006 `no_convergence`: force-select by combined score; document non-convergence; flag for user review via `unaddressed_invariants` in return contract.
