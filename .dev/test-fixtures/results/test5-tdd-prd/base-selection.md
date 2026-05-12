---
base_variant: A
variant_scores: "A:78 B:72"
---

# Base Selection Rationale

## Scoring Criteria (from debate + TDD + PRD)

**Debate-derived (weight 50%):**
1. Schedule realism (today = 2026-04-20; M1 TDD target = 2026-04-14)
2. Milestone decomposition / parallelization risk
3. Rollback automation fidelity to TDD §19.4
4. Open-question closure rate
5. Conflict surfacing
6. Compliance wiring timing
7. Observability first-class vs distributed

**TDD-supplementary (weight 30%):**
8. Technical completeness vs §7/§8/§10 (data models, APIs, components)
9. Testing strategy alignment (§15 pyramid + load targets)
10. Migration feasibility (§19 phases + rollback)

**PRD-supplementary (weight 20%):**
11. Business-value delivery (S19 success metrics)
12. Persona coverage (Alex/Jordan/Sam from S7)
13. Compliance alignment (S17 legal: SOC2, GDPR, NIST)

## Per-Criterion Scores (0-10)

| # | Criterion | Variant A (Opus) | Variant B (Haiku) | Evidence |
|---|---|---|---|---|
| 1 | Schedule realism | 9 | 3 | A compresses M1 to 2026-04-20→05-04 honestly via `OQ-M1-001` + `R-M1-SCHED`; B prints impossible 2026-03-31→04-14 window |
| 2 | Decomposition / parallelization | 8 | 6 | A distributes hardening; B concentrates 26 deliverables in M4 (single-point chokepoint per Opus rebuttal) |
| 3 | Rollback automation fidelity | 10 | 5 | A's `ROLLBACK-AUTO-LATENCY/ERR/REDIS/DATA` literally implements TDD §19.4 "automatic conditions"; B uses drilled runbook `TEST-012` |
| 4 | OQ closure rate | 5 | 9 | B closes 11/13 OQs with committed defaults; A leaves 8 open (including 5-token cap, async email, logout) |
| 5 | Conflict surfacing | 7 | 9 | B explicitly documents `CONFLICT-2` (PRD auto-login vs TDD 201 redirect); A silently implements TDD contract |
| 6 | Compliance wiring timing | 7 | 9 | B wires consent at M1 (`NFR-COMP-001`, `COMP-013`); A places consent in M3 |
| 7 | Observability | 7 | 9 | B dedicates `OBS-001..007` with owners; A spreads `METRIC-*` tasks across milestones |
| 8 | Technical completeness (TDD) | 7 | 9 | B includes `API-007` logout + `API-008/009/010` admin per PRD; A defers admin APIs to v1.1 |
| 9 | Testing strategy | 8 | 7 | A puts `NFR-PERF-002` k6 load test in M1 (earlier bug-catching); B defers to M4 (`TEST-009`) |
| 10 | Migration feasibility | 9 | 7 | A's automated triggers reduce MTTR; B relies on human-gated drills |
| 11 | Business-value delivery | 7 | 8 | Both track conversion funnel; B's earlier logout + admin APIs deliver PRD S19 capability at GA |
| 12 | Persona coverage | 6 | 10 | Jordan persona: B ships admin APIs at GA; A ships raw-SQL access only (`OPS-003` runbook) |
| 13 | Compliance alignment | 8 | 9 | Both honor 12-month retention; B's M1 consent capture + admin audit query surface satisfies SOC2 Type II more completely |

## Weighted Overall Scores

- **Variant A (Opus): 78** — Debate criteria 40/50, TDD 24/30, PRD 14/20
- **Variant B (Haiku): 72** — Debate criteria 40/50, TDD 22/30, PRD 10/20 (dragged by schedule realism)

Note: B's scores on criteria 1 and 3 alone cost ~11 points; B leads on 7 criteria but loses critical ones that anchor the plan to the TDD contract and the current calendar.

## Base Variant Selection Rationale

Variant A is selected as base because:

1. **Schedule honesty is load-bearing for the rest of the plan.** Today is 2026-04-20; B's M1 window (2026-03-31→04-14) is already in the past. Opus's rebuttal is correct: both plans preserve GA 2026-06-09, but only A's is falsifiable against the current date. Merging from B as base would require rewriting every milestone date.

2. **Rollback automation is a TDD contract.** TDD §19.4 uses "automatic conditions" language. A's four `ROLLBACK-AUTO-*` deliverables literally implement it; B's human-gated runbook is a contract weakening disguised as simplification.

3. **Distributed hardening is safer under compression.** With the M1 slip already consumed, B's 26-item M4 is the exact single-point-of-failure Opus's rebuttal identifies.

4. **Risk register depth** (13 risks including schedule + key rotation vs B's 10) and **success-criteria traceability** (`SUCC-SLO-BOARD` binding every numeric target to a Grafana panel) give A more surface for execution review.

## Improvements to Incorporate from Variant B

Merge these deltas into the A base during the final merge phase:

1. **Add logout endpoint** — Adopt B's `API-007` (POST `/auth/logout`) + `COMP-016` LogoutControl. Closes PRD AUTH-E1 user story gap that A's `OQ-M4-001` flags. Targets M4.

2. **Add admin APIs as GA deliverables, not v1.1** — Merge B's `API-008` (GET `/admin/auth-events`), `API-009` (lock), `API-010` (unlock), plus supporting `COMP-018` AdminAuthEventService and `COMP-019` AccountLockManager. Jordan persona (PRD S7) and SOC2 operational readiness (PRD S17) are GA-blocking per Haiku rebuttal; A's "raw SQL access" stance is a capability regression against the PRD contract. Target M4.

3. **Close OQs with committed defaults** — Adopt B's resolutions for:
   - `OQ-PRD-1` (async email dispatch with generic UX confirmation) → apply to A's M3
   - `OQ-PRD-2` (cap refresh tokens at 5/user, evict oldest) → apply to A's M2 TokenManager
   - `OQ-PRD-4` (defer "remember-me" to v1.1) → close A's `OQ-M2-002`/`OQ-M4-002`
   - `CONFLICT-2` (register returns 201 + redirect to login, not auto-login) → add to A's decision table

4. **Pull compliance wiring forward** — Move A's GDPR consent capture (`NFR-GDPR-CONSENT`) from M3 into M1 alongside `DM-AUDIT`, mirroring B's `NFR-COMP-001` + `COMP-013` placement. Avoids late schema migration.

5. **Explicit observability block with owners** — Replace A's scattered `METRIC-*` tasks with a dedicated `OBS-001..007` group (structured logging, latency histogram, refresh counter, registration counter, OTEL spans, alert rules, rollout SLO dashboard) assigned to a single owner, per B's M4 structure. Keep A's early load test (`NFR-PERF-002` in M1) — do NOT move it to M4.

6. **Surface CONFLICT-2 explicitly in the decision table** — Follow B's pattern of documenting PRD/TDD contract conflicts with chosen resolution + precedence rule, not silent TDD adoption.

7. **Add `/health` endpoint deliverable** — Adopt B's `API-011` GET `/health` explicitly (A implies it via `NFR-REL-001` but never wires a deliverable). Required by B's release gate.

8. **Health/release-gate aggregation** — Adopt B's `OPS-011` go/no-go gate as a formal deliverable aggregating test-lead + eng-manager + security + platform approvals before each rollout phase advance. A has implicit sign-offs; making them explicit reduces rollout risk.

Keep from A (do NOT take from B): compressed M1 schedule with `R-M1-SCHED` risk entry, all four `ROLLBACK-AUTO-*` deliverables, early M1 load testing, `SUCC-SLO-BOARD` binding, distributed hardening layout, 13-item risk register, technical-layer milestone decomposition.
