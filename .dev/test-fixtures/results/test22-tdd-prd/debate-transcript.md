---
convergence_score: 0.62
rounds_completed: 2
---

# Adversarial Debate: Opus vs Haiku Roadmap Variants

## Round 1 — Initial Positions

### Variant A (Opus) — Opening Position

**On Registration (M2):** Registration belongs in M2, not M1. M1 must be pure infrastructure — schemas, keys, feature flags, RS256 provisioning. Putting a user-facing endpoint in Foundation couples M1 to API surface, GDPR UX, and validation logic before the token lifecycle exists. Blast radius matters; M1 failures should not touch customer-facing endpoints.

**On Logout as P1:** The PRD user story is satisfied by a P1 logout shipping in M3. Marking it P0 inflates the GA-blocking surface unnecessarily. If the refresh token expires in 7 days and access tokens in 15 minutes, a missing logout endpoint is a UX inconvenience, not a compliance breach. P1 preserves delivery buffer.

**On Audit Query Endpoint:** Not required in v1.0. Jordan's admin persona can be served by direct DB query tooling during initial GA. Adding `GET /v1/auth/audit-events` expands API surface, introduces RBAC enforcement questions (which v1.0 explicitly defers), and creates a new attack surface requiring its own pen-test coverage.

**On OQ-PRD-002:** Must be resolved before M1 exit. DM-002 Redis key schema cannot be frozen with `TBD-pending-OQ-PRD-002` placeholders — that's a commitment to schema churn post-M2. Discipline on schema finalization is non-negotiable for a data store that ships to production.

**On Timeline Margin:** 3-week M5 is the correct buffer. Phase 2 beta regressions, pen-test P1 remediation, and runbook drift discovered during drills all consume M5 capacity. 16 days leaves no room for a second rollback drill or unexpected SLO regression.

**On Security Gate Separation:** SEC-REVIEW and SEC-PENTEST must be distinct deliverables with independent sign-off. Bundling them into "validation pack" conflates design-review findings (fixable in code) with pen-test findings (which may require architectural changes and have longer remediation cycles).

**On GDPR Consent (M4):** Adding `consent_given_at` via migration in M4 is standard hardening practice. Deferring consent capture to hardening phase avoids bundling privacy UX into foundation work; reversible migration handles the schema add safely.

### Variant B (Haiku) — Opening Position

**On Registration (M1):** Registration is the foundational user-facing contract. Front-loading it exposes GDPR consent capture and validation pipelines early, giving QA a testable end-to-end path from week 2. Without registration in M1, there is no meaningful E2E coverage until M3.

**On Logout as P0:** PRD AUTH-E1 explicitly includes logout as a user story. Shipping GA without logout violates the committed PRD user narrative. Logout is also a security control — refresh token revocation is not optional when a user explicitly requests session termination. P0 is the only defensible priority.

**On Audit Query Endpoint:** The PRD admin persona (Jordan) requires queryable audit access. SOC2 Type II audit workflows need repeatable query paths, not DB-admin ad-hoc access. `GET /v1/auth/audit-events` with internal-admin-only auth closes OQ-GAP-002 at minimal cost and improves audit defensibility.

**On OQ-PRD-002:** A configurable per-user token cap with `TBD-pending-OQ-PRD-002` placeholder is safer than blocking M1. The Redis key schema does not change based on cap policy — only the eviction logic does. Forcing a blocker creates artificial timeline pressure.

**On Timeline Margin:** 10 weeks + 2 days with a 16-day M5 is sufficient if M4 load tests pass cleanly. Excess M5 buffer means less time in earlier phases where most defects originate. Tighter schedule reflects confidence in M4 SLO proof.

**On Security Gate Separation:** TEST-013 "Security and reliability validation pack" captures both review and pen test outputs under a single release gate. Bundling simplifies the release review and avoids the coordination overhead of two independent sign-offs.

**On GDPR Consent (M1):** Consent must be captured from schema inception. Adding a `consent_given_at` column in M4 after registration has been live since M2 creates a data-quality gap — early users either have no consent record or require backfill. Schema-first consent eliminates this class of migration risk.

## Round 2 — Rebuttals

### Variant A (Opus) — Rebuttal

**On Registration placement — Haiku's E2E argument is weak:** E2E coverage of registration before login and token issuance exist is unrepresentative. The full user journey requires M2 tokens to be meaningful; M1-only registration tests only validate schema-level insert, which unit tests already cover. The coupling cost exceeds the testability benefit.

**On Logout P0 — partial concession:** PRD AUTH-E1 does make logout GA-blocking; the priority should be P0. However, Opus delivers logout in M3 alongside other API endpoints, which is functionally equivalent to Haiku's treatment. The disagreement is labeling, not delivery timing. Conceded on priority label.

**On Audit Query Endpoint — Haiku undersells the RBAC problem:** "Internal-admin-only auth" is not free. It implies an admin role check, which requires role enforcement semantics the PRD explicitly defers to v1.1. Haiku smuggles RBAC enforcement into v1.0 via API-009. The cleaner path is v1.1 when RBAC is designed holistically.

**On OQ-PRD-002 — Haiku misreads the schema risk:** The Redis key pattern `authtok:refresh:{hash}` is not the issue — the eviction strategy changes key-lifecycle semantics (LRU vs FIFO vs unlimited). This affects memory budgeting (OPS-006), monitoring, and multi-device UX. Shipping with "TBD" means shipping with an unvalidated memory projection.

**On Timeline Margin — rollback drills require real time:** Haiku's confidence in M4 is unjustified optimism. Pen-test P0/P1 findings, which R-PRD-002 explicitly flags as probable, need remediation + re-test windows. 16 days does not accommodate one remediation cycle plus phased rollout plus retrospective.

**On Security Gate — bundling hides findings:** TEST-013 as a single gate means a pen-test P1 finding can block the same release review as a dashboards-not-yet-deployed finding. Separate gates enable parallel remediation tracks. Haiku's bundling optimizes for process simplicity at the cost of finding-resolution clarity.

**On GDPR Consent — concession with qualification:** Haiku is correct that schema-from-inception is lower-risk than late migration. Conceded on principle. However, this requires M1 to include consent UX in the registration endpoint, which reinforces the registration-in-M1 coupling that Opus argued against. Haiku's GDPR position strengthens its registration-in-M1 position, but also confirms the coupling concern.

### Variant B (Haiku) — Rebuttal

**On Registration — Opus overweights "pure infrastructure":** Pure-infrastructure M1 is an aesthetic preference, not a risk-mitigation requirement. M1 already includes feature flag infrastructure, API gateway, and rate limits — it is not pure infra. Adding registration is incremental, not categorical.

**On Logout — Opus concedes the point:** Accepted. Priority label resolved.

**On Audit Query — Opus conflates authorization with RBAC enforcement:** Internal-admin-only access can be enforced via network-level controls (service mesh, internal-only route) without user-facing role enforcement. The RBAC deferral applies to end-user role semantics, not internal service authorization. Opus's concern is overreach.

**On OQ-PRD-002 — configurable caps are standard practice:** Redis memory monitoring already handles variable per-user counts via OPS-006 scaling to 2GB. The eviction strategy is a runtime config change, not a schema change. Opus's "schema churn" risk is mischaracterized — no migration occurs.

**On Timeline — Opus conflates risk with duration:** A 3-week M5 does not reduce pen-test P0 risk; only M4 scheduling does. The correct mitigation is pen-test execution in M4 week 7 (which both variants do). Extra M5 days do not buy risk reduction proportional to lost M3/M4 iteration time.

**On Security Gate — separation creates artificial process:** Opus's "parallel remediation tracks" argument assumes finding types are cleanly separable. In practice, pen-test findings often require design-review re-validation, making the gates sequential anyway. Bundling acknowledges this reality.

**On GDPR Consent — Opus's concession validates Haiku's broader position:** Opus now agrees schema-first consent is correct. This implies registration logic must exist where the schema is applied, which further supports Haiku's M1 registration placement. The two positions are coupled; Opus cannot accept one without the other.

## Convergence Assessment

### Areas of Agreement (High Convergence)

- **Shared foundation:** 15 of 16 structural assumptions converge (complexity, token architecture, bcrypt cost, RS256, audit retention 12mo, lockout 5/15min, GA date 2026-06-09, 3-phase rollout, HPA/pool/Redis capacity, risk taxonomy).
- **Logout priority:** After Opus's rebuttal, both agree logout is GA-blocking; disagreement was labeling, not substance. **Resolved to P0.**
- **GDPR consent timing:** Opus conceded schema-first is lower risk. **Resolved to M1 schema inclusion.**
- **OQ-PRD-004 (remember me):** Both arrive at "not supported v1.0"; stylistic difference only.
- **OQ-PRD-003 (lockout):** Both adopt TDD §13 values (5/15min).

### Partial Convergence

- **Registration placement:** GDPR concession pulls Opus toward M1 registration, but Opus maintains coupling concern. Likely resolution: M1 with explicit scope of "registration endpoint + consent capture only; login integration deferred to M2."
- **Timeline margin:** Both agree pen-test execution timing (M4 week 7) matters more than M5 duration. Remaining disagreement is margin preference, not mitigation substance.

### Unresolved Disputes

- **Audit query endpoint (API-009):** Fundamental disagreement on whether internal-admin authorization counts as RBAC enforcement. Requires product + security arbitration on what "v1.1 RBAC deferral" actually prohibits.
- **OQ-PRD-002 treatment:** Opus treats unresolved cap as schema-churn risk; Haiku treats it as runtime-config risk. Resolution depends on whether eviction strategy requires key-schema changes — a technical fact question, not a debate question.
- **Security gate separation:** Process-design disagreement with reasonable arguments on both sides. Either approach can succeed with disciplined execution.

### Recommended Synthesis

A merged roadmap should:
1. Place registration in M1 with GDPR consent from schema inception (Haiku position, validated by Opus concession).
2. Mark logout P0 (agreed).
3. Include `GET /v1/auth/audit-events` with explicit internal-admin-only documentation clarifying it is not RBAC enforcement (Haiku with Opus caveat).
4. Resolve OQ-PRD-002 before M1 exit per Opus discipline; if unresolvable, ship with documented memory-projection range, not open placeholder.
5. Keep SEC-REVIEW and SEC-PENTEST as separate tracked deliverables within a single release gate — hybrid approach.
6. Adopt timeline closer to Opus's 3-week M5 to preserve pen-test remediation buffer.
7. Use Opus's complexity derivation breakdown, TDD calendar mapping table, and dependency graph visualization for auditability.
8. Use Haiku's explicit component rows (AuthGuard, LoginAttemptTracker, FeatureFlagController, rollout dashboard) for inventory completeness.

Convergence score **0.62** reflects strong shared foundation with 2 unresolved technical questions (API-009 scope, OQ-PRD-002 schema impact) and 1 unresolved process question (security gate bundling).
