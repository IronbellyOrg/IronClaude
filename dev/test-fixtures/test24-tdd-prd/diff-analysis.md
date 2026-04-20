---
total_diff_points: 15
shared_assumptions_count: 18
---

## Shared Assumptions and Agreements

1. **Complexity class**: Both classify as HIGH (0.78); primary_persona = architect.
2. **Milestone count**: Both use 5 P0 milestones over ~10–11 calendar weeks.
3. **GA date**: Both target 2026-06-09.
4. **Audit retention**: Both resolve OQ-CONFLICT-1 in favor of PRD (12 months, overriding TDD's 90-day default).
5. **Lockout policy**: Both resolve OQ-PRD-3 → 5 failures / 15 minutes.
6. **Remember-me (OQ-PRD-4/REMEMBER-ME)**: Both defer to v1.1.
7. **API-key auth (OQ-001)**: Both defer to v1.1.
8. **Password reset (OQ-PRD-1)**: Both resolve async.
9. **Crypto**: bcrypt cost 12, RS256 2048-bit RSA, 15-min access / 7-day refresh.
10. **Stores**: PostgreSQL 15 (user + audit), Redis 7 (hashed refresh tokens).
11. **Transport**: TLS 1.3, CORS allow-list, log redaction.
12. **Email**: SendGrid with async delivery pattern.
13. **Rollout**: `AUTH_NEW_LOGIN` + `AUTH_TOKEN_REFRESH` flags; 10% beta → 100% GA.
14. **Logout gap-fill**: Both add missing `/auth/logout` endpoint (OQ-GAP-001).
15. **Admin gap-fill (JTBD-gap-2)**: Both add admin auth-event query surface.
16. **Coverage gate**: Both require ≥80% unit coverage.
17. **Stack**: Node 20 LTS, bcryptjs, jsonwebtoken, React.
18. **NFR targets**: p95 <200ms, 99.9% uptime, 500 concurrent logins, zero PII in logs.

## Divergence Points

1. **Deliverable granularity** — Opus: 122 items; Haiku: 83 items. *Impact*: Opus provides finer traceability (skeleton vs full tasks, per-metric entries); Haiku reduces tracking overhead but bundles concerns.

2. **Timeline length** — Opus: 11 weeks (2026-03-30 → 2026-06-12, 3-day post-GA buffer); Haiku: 10 weeks (2026-03-31 → 2026-06-09, exact TDD alignment). *Impact*: Opus carries explicit rollout buffer; Haiku is tighter with no global slack.

3. **M3 duration & scope** — Opus: 3 weeks combining tokens + frontend + reset (34 items); Haiku: 2 weeks with tokens moved to M2 and M3 focused on user journeys (15 items). *Impact*: Opus consolidates the token-heavy integration risk in one milestone; Haiku parallelizes earlier but loads M2.

4. **TOKEN-STUB pattern (M2)** — Opus: introduces TOKEN-STUB so login is testable before real JWT lands in M3; Haiku: implements real `TokenManager`/`JwtService` in M2 directly. *Impact*: Opus reduces M2 dependency surface but incurs temporary code; Haiku avoids throwaway code but couples M2 to Redis/JWT readiness.

5. **Refresh-token cap (OQ-PRD-2)** — Opus: unlimited tentative, observe metric for v1.1; Haiku: cap 5 per user, evict oldest. *Impact*: Haiku bounds Redis memory and improves revocation semantics; Opus preserves multi-device UX without churn.

6. **CONFLICT-2 (register auto-login)** — Opus: not explicitly addressed; Haiku: explicitly resolves in favor of TDD (201 UserProfile, redirect to LoginPage). *Impact*: Haiku preempts a PRD/TDD contract collision that Opus leaves implicit.

7. **Rollback triggers** — Opus: dedicated OBS-ROLLBACK-TRIGGERS task with automated flag flips; Haiku: TEST-012 rollback drill + OPS-009 go/no-go gate. *Impact*: Opus automates rollback decisions; Haiku relies on human-gated workflow.

8. **Risk register depth** — Opus: 20 risks with numbered mitigations and owners; Haiku: 10 risks with tabular mitigations. *Impact*: Opus surfaces more edge cases (R-008 CAPTCHA, R-010 clock skew, R-017 admin PII, R-020 flag sprawl); Haiku is more digestible.

9. **ADR format** — Opus: 6 narrative ADRs with alternatives considered and landing slots; Haiku: 6-row Decision Summary table. *Impact*: Opus is more auditable; Haiku is more compact.

10. **CAPTCHA integration** — Opus: explicit CAPTCHA-INTEG task in M3 with spike + feature-flag fallback; Haiku: mentioned only as login-after-3-failures requirement on COMP-001. *Impact*: Opus treats CAPTCHA as a procurement/integration risk; Haiku treats it as a UX detail.

11. **Frontend clock-skew/silent-refresh** — Opus: FE-CLOCK-SKEW (refresh at exp-60s), FE-ERROR-HANDLING task; Haiku: implicit in AuthProvider AC. *Impact*: Opus prevents a specific production pain point (R-010); Haiku relies on implementation judgment.

12. **RSA key rotation** — Opus: RSA-KEY-ROTATION documented task in M3 with overlap script and drill; Haiku: quarterly rotation stated in NFR-SEC-002 but no dedicated deliverable. *Impact*: Opus reduces R-006 (unplanned rotation incident); Haiku keeps the requirement but defers operationalization.

13. **Async email infrastructure** — Opus: ASYNC-QUEUE task (BullMQ) with DLQ and retries; Haiku: asynchronous dispatch as a decision only. *Impact*: Opus sizes queue infra explicitly; Haiku leaves implementation discretion to engineering.

14. **Admin surfaces placement** — Opus: ADMIN-001 audit query in M3 (alongside tokens); Haiku: API-008/009/010 (query + lock + unlock) in M4 as CMP hardening. *Impact*: Opus ships admin visibility earlier; Haiku bundles admin with SOC2 evidence generation and adds lock/unlock endpoints Opus omits.

15. **Data migration script** — Opus: DATA-MIG-SCRIPT (M4) with idempotent upsert + rehash-on-login hook; Haiku: referenced only in rollback drill. *Impact*: Opus plans for legacy users; Haiku assumes greenfield migration.

## Areas Where One Variant Is Clearly Stronger

**Opus stronger on:**
- Operational readiness (rollback automation, key rotation, async queue, migration script)
- Risk identification (20 vs 10 entries; covers frontend-specific risks)
- ADR transparency (alternatives + trade-offs documented per decision)
- Per-metric observability decomposition (OBS-001..009 separate tasks)
- Frontend production quality (clock skew, error UX, CSP)

**Haiku stronger on:**
- Contract conflict resolution (explicit CONFLICT-2 call-out)
- Admin operational completeness (lock + unlock APIs, not just query)
- Deliverable density (fewer items, less tracking overhead)
- Timeline precision (exact TDD alignment, simpler dependency graph)
- Refresh-token memory bound (concrete cap vs deferred decision)

## Areas Requiring Debate to Resolve

1. **OQ-PRD-2 (refresh-token cap)**: unlimited-observe vs cap-5-evict — affects Redis sizing and multi-device UX.
2. **CONFLICT-2 (register behavior)**: whether to update TDD API-002 for auto-login or hold the line for API stability.
3. **M3 scope width**: 3-week token+frontend block vs 2-week tokens-in-M2 split — affects integration risk concentration.
4. **TOKEN-STUB use**: throwaway stub in M2 vs complete TokenManager in M2.
5. **Rollback posture**: automated flag flips (Opus OBS-ROLLBACK-TRIGGERS) vs human-gated drill (Haiku OPS-009).
6. **Admin scope**: query-only (Opus) vs query + lock + unlock (Haiku).
7. **Timeline buffer**: 3-day post-GA buffer (Opus) vs zero-slack GA-exact (Haiku).
8. **Migration path**: explicit legacy-data script (Opus) vs greenfield assumption (Haiku).
