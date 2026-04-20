---
base_variant: A
variant_scores: "A:86 B:81"
---

# Variant Scoring & Base Selection

## 1. Scoring Criteria (derived from debate + TDD/PRD context)

| # | Criterion | Weight | Source |
|---|---|---|---|
| C1 | Completeness / coverage breadth | 15 | Debate: granularity dispute |
| C2 | Operational hardening depth | 15 | Debate: TOKEN-STUB, OBS-ROLLBACK, RSA rotation |
| C3 | Risk management fidelity | 10 | Debate: 20 vs 10 risk entries |
| C4 | TDD technical completeness (§7/§8/§10) | 15 | TDD supplement |
| C5 | Testing strategy alignment (§15) | 10 | TDD supplement |
| C6 | Migration & rollout feasibility (§19) | 10 | TDD supplement |
| C7 | Compliance alignment (SOC2/GDPR/NIST) | 10 | PRD + TDD §13 |
| C8 | Persona coverage (Alex/Jordan/Sam) | 5 | PRD S7 |
| C9 | Explicit conflict resolution | 5 | Debate: CONFLICT-2 dispute |
| C10 | Readability/consumability | 5 | Debate: compactness |

## 2. Per-Criterion Scores

| # | Criterion | A (Opus) | B (Haiku) | Evidence |
|---|---|---|---|---|
| C1 | Completeness | 95 | 82 | A:122 items, 5 MLS, 24 M1 tasks; B:83 items, 17 M1 tasks — A decomposes observability, key rotation, async queue as explicit deliverables |
| C2 | Operational hardening | 93 | 75 | A has OBS-001..009, OBS-ROLLBACK-TRIGGERS, RSA-KEY-ROTATION, DATA-MIG-SCRIPT, RELIABILITY-READINESS chaos test, ASYNC-QUEUE, FE-CLOCK-SKEW; B lacks chaos testing, RSA rotation script, explicit clock-skew mitigation |
| C3 | Risk management | 90 | 72 | A:20 risks including R-010 clock skew, R-017 admin PII, R-020 flag sprawl; B:10 risks — Haiku concedes brevity but Opus catches frontend-specific modes |
| C4 | TDD technical completeness | 85 | 88 | B wins: DM-001..004 explicit (adds AuthAuditLog + PasswordResetToken schemas), API-001..011 (includes admin lock/unlock + health endpoint); A has implicit A0 + ADMIN-001 query-only |
| C5 | Testing alignment | 88 | 85 | A:TEST-001..006+E2E+coverage gate+LOAD-TEST-FULL; B:TEST-001..013 adequate but less granular around flakiness/burn-in |
| C6 | Migration feasibility | 90 | 82 | A: DATA-MIG-SCRIPT deliverable + idempotent upsert + automated rollback triggers + 3-day buffer; B: phased rollout present but no migration script, no automated triggers |
| C7 | Compliance | 90 | 88 | Both resolve CONFLICT-1 (12-mo RTN); A adds NFR-COMP-003 NIST conformance explicit, DSAR-export stub; B has clean NFR-COMP-001/002 but defers NIST framing |
| C8 | Persona coverage | 80 | 92 | B wins: API-008/009/010 covers Jordan's full incident response; A only ships ADMIN-001 query (Opus concedes this gap in Round 2) |
| C9 | Explicit conflict resolution | 75 | 95 | B explicitly resolves CONFLICT-2 (register→LoginPage per TDD contract); A leaves it implicit (Opus concedes) |
| C10 | Readability | 78 | 88 | B: 6-row Decision Summary table, 10-row risk register — executive-consumable; A: narrative ADRs, denser |

## 3. Weighted Overall Scores

**Variant A (Opus):** (95·15 + 93·15 + 90·10 + 85·15 + 88·10 + 90·10 + 90·10 + 80·5 + 75·5 + 78·5) / 100 = **86.4**

**Variant B (Haiku):** (82·15 + 75·15 + 72·10 + 88·15 + 85·10 + 82·10 + 88·10 + 92·5 + 95·5 + 88·5) / 100 = **81.4**

## 4. Base Variant Selection: A (Opus)

**Rationale:**
- A dominates on C1/C2/C3/C6 — the dimensions where merging *down* is painful (building observability decomposition, chaos tests, risk coverage, and migration scripts into B requires structural rewrites).
- B's advantages (C4/C8/C9) are **localized additions**: admin lock/unlock endpoints, explicit CONFLICT-2 note, refresh-token cap — each is a discrete graft onto A's existing scaffolding.
- Debate convergence assessment itself recommends adopting Opus's operational scaffolding (OBS-ROLLBACK-TRIGGERS, RSA-KEY-ROTATION, DATA-MIG-SCRIPT, FE-CLOCK-SKEW, ASYNC-QUEUE, expanded risk register) and layering Haiku's specific gap-fills on top.
- A's 3-day post-GA buffer is low-cost insurance on a fixed 2026-06-09 GA with external pen-test dependency (Opus rebuttal accepted).

## 5. Specific Improvements to Incorporate from B (Haiku)

| # | Incorporate | Source in B | Rationale |
|---|---|---|---|
| I1 | Add **API-009 POST /admin/users/{id}/lock** + **API-010 POST /admin/users/{id}/unlock** + **COMP-019 AccountLockManager** | B M4 rows 19-20, 23 | Jordan persona incident response — Opus concedes ADMIN-001 query-only is half a feature |
| I2 | Add **API-011 GET /health** as distinct deliverable | B M4 row 21 | A has NFR-REL-001 but no explicit endpoint row — raise to first-class |
| I3 | Add explicit **CONFLICT-2 resolution note** to M3 (RegisterPage redirects to LoginPage per TDD §8.2 contract; flag for v1.1 product review) | B CONFLICT-2 row | Opus concedes implicit resolution is a gap |
| I4 | Add **refresh-token cap=5 with oldest-eviction** as reversible default (not unlimited) | B OQ-PRD-2 resolution | Bounds Redis sizing deterministically; Opus's "unlimited+metric" leaves sizing open-ended |
| I5 | Add **DM-003 AuthAuditLog** and **DM-004 PasswordResetToken** as explicit data-model rows in M1 (A has A0 in M4; promote to M1 schema with forward reference) | B DM-003, DM-004 | TDD §7 coverage strengthened; resolves storage sizing earlier |
| I6 | Adopt B's **OQ-GOV-001 API deprecation policy** (90-day notice, one active major) | B M4 OQ row 2 | A has API-VER-001 but no deprecation window commitment |
| I7 | Pull **COMP-018 AdminAuthEventService** as service-layer abstraction behind ADMIN-001 | B COMP-018 | Enables I1 lock/unlock without duplicating admin auth wiring |

## 6. Merge Constraints (per debate)

- **TOKEN-STUB**: keep A's M2 stub as documented fallback; primary plan = real TokenManager in M2 contingent on M1 Redis provisioning — do NOT remove TOKEN-STUB row entirely per Haiku's concern, retain as contingency artifact
- **Automated rollback**: keep A's OBS-ROLLBACK-TRIGGERS but annotate "human-confirmed for first 30 days post-GA" per B's operational-maturity point
- **3-day post-GA buffer**: retain (A); costs nothing if unused
- **Risk register**: retain A's 20 entries (reject B's compaction argument — frontend/admin/flag-sprawl risks are launch-relevant)
