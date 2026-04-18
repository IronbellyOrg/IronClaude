---
base_variant: "B (Haiku 5-Phase/13-Week)"
variant_scores: "A:68 B:81"
---

## 1. Scoring Criteria

Twelve criteria derived from debate divergences and PRD requirements, weighted by impact on delivery and compliance.

| # | Criterion | Weight | Source |
|---|---|---|---|
| 1 | Schema completeness & compliance readiness | 12 | Debate D2; PRD S17 GDPR/SOC2 |
| 2 | Test strategy effectiveness | 10 | Debate D3 |
| 3 | Persona coverage | 10 | PRD S7 (Alex, Jordan, Sam) |
| 4 | PRD gap-fill completeness | 10 | Debate D4; PRD scope |
| 5 | Compliance alignment | 10 | PRD S17; debate D2 convergence |
| 6 | Business value delivery speed | 10 | PRD S19 success metrics |
| 7 | Observability placement | 8 | Debate D5 |
| 8 | Integration documentation quality | 8 | Structural comparison |
| 9 | Timeline realism | 7 | Debate D1 |
| 10 | Health endpoint completeness | 5 | Debate D5 sub-point |
| 11 | Phase granularity & exit gates | 5 | Debate D1 |
| 12 | Risk management | 5 | Convergence area (agreed) |

## 2. Per-Criterion Scores

| # | Criterion | Wt | A (Opus) | B (Haiku) | Justification |
|---|---|---|---|---|---|
| 1 | Schema & compliance | 12 | 6 | 9 | Haiku's DM-004/005/006 address GDPR Art. 7 `policyVersion` requirement. Debate convergence endorsed explicit schemas. Opus leaves ConsentRecord shape to module internals — auditor-hostile. |
| 2 | Test strategy | 10 | 6 | 8 | Haiku places unit/integration tests inline (Phase 2) catching bugs at introduction. Opus batches all testing in Phase 5 — debate identified this as "waterfall testing dressed in agile clothing." Haiku still consolidates E2E/load in Phase 4. |
| 3 | Persona coverage | 10 | 6 | 9 | Haiku delivers COMP-015 (AdminAuthEventsPage), FR-AUTH-007, TEST-012 for Jordan. Opus defers admin UI to v1.1 — PRD user story says Jordan "views authentication event logs," not "runs curl commands." Haiku's FR-AUTH-006 logout journey with TEST-011 closes shared-device security gap. |
| 4 | PRD gap-fills | 10 | 7 | 9 | Both include API-007/008. Haiku adds FR-AUTH-006, FR-AUTH-007, DM-004-006, COMP-010-017, TEST-007-016 — 16 additional gap-fill items explicitly tracked. Opus acknowledges gaps but defers several. |
| 5 | Compliance alignment | 10 | 6 | 9 | Haiku defines consent schema in Phase 1, tests auditability (TEST-013), retention (TEST-014), and password handling (TEST-015) in Phase 4 before any rollout. Opus validates compliance in Phase 5 alongside E2E — no dedicated compliance test gate. |
| 6 | Business value speed | 10 | 8 | 6 | Opus reaches GA at week 9 vs Haiku's week 13. Four-week advantage for $2.4M personalization revenue. Opus scores here despite assumptions because earlier delivery is real if parallelism holds. |
| 7 | Observability | 8 | 5 | 9 | Debate convergence: "Haiku wins on merit." Opus places OTel in Phase 7 concurrent with GA — no tracing during alpha/beta debugging. Haiku wires OTel in Phase 4, providing 4 weeks of trace data before production traffic. Opus's cost argument is a sampling config issue, not a placement issue. |
| 8 | Integration docs | 8 | 9 | 7 | Opus provides detailed per-phase integration point tables with artifact type, wiring phase, and consumer columns. Haiku has tables but less granular — fewer explicit wiring details. Opus's format is significantly more useful for handoffs. |
| 9 | Timeline realism | 7 | 7 | 7 | Tie. Both assume roughly 88-93 tasks. Opus's 9 weeks requires proven parallel streams; Haiku's 13 weeks assumes sequential. Debate correctly identified this as unresolvable without team composition data. Neither is wrong — they target different team shapes. |
| 10 | Health endpoint | 5 | 6 | 8 | Haiku checks PostgreSQL + Redis + RSA keys + SendGrid. Debate established: missing RSA key = zero token issuance, broken SendGrid = broken password reset. Opus checks only PostgreSQL + Redis. Convergence recommended Haiku's 4-dep check with SendGrid as degraded state. |
| 11 | Phase granularity | 5 | 7 | 7 | Tie. Opus's 7 phases offer more checkpoints; Haiku's 5 phases reduce gate ceremony. Both are valid expressions of parallelism vs sequential assumptions. |
| 12 | Risk management | 5 | 8 | 8 | Tie. Same 6 risks, same mitigations, same owners. Debate confirmed convergence here. Both include identical rollback chains (MIG-006 through MIG-011). |

## 3. Overall Scores

**Weighted calculation:** Sum(score × weight) / 100

| Variant | Calculation | Score |
|---|---|---|
| A (Opus) | (6×12)+(6×10)+(6×10)+(7×10)+(6×10)+(8×10)+(5×8)+(9×8)+(7×7)+(6×5)+(7×5)+(8×5) | **68** |
| B (Haiku) | (9×12)+(8×10)+(9×10)+(9×10)+(9×10)+(6×10)+(9×8)+(7×8)+(7×7)+(8×5)+(7×5)+(8×5) | **81** |

**Opus (68):** Strong integration documentation and faster delivery timeline. Loses on compliance readiness (implicit schemas), persona completeness (no admin UI), and observability timing. The 9-week timeline is its main competitive advantage but carries parallelism risk.

**Haiku (81):** Wins decisively on compliance, persona coverage, test distribution, and observability. The 13-week timeline is the primary cost — 4 extra weeks against a SOC2 Q3 2026 deadline. However, the thoroughness reduces rework risk and audit failure probability.

## 4. Base Variant Selection Rationale

**Selected: B (Haiku)** as merge base.

Three reasons:

1. **Compliance is non-negotiable.** The SOC2 Q3 2026 deadline means audit failure costs more than 4 weeks of delay. Haiku's explicit schemas (DM-004/005/006), distributed compliance testing (TEST-013-015), and Phase 1 consent/audit infrastructure are structurally safer. Retrofitting these into Opus would require restructuring Phases 2-3.

2. **Persona coverage is a PRD requirement.** Jordan's admin UI (COMP-015) and the logout journey (FR-AUTH-006 + TEST-011) are scope items in the PRD, not nice-to-haves. Adding them to Opus would change Phase 4 scope and ripple into Phase 5 testing — easier to start from Haiku which already includes them.

3. **Observability placement was debate-settled.** The convergence assessment explicitly recommended Haiku's Phase 4 OTel placement. Moving Opus's Phase 7 OTel earlier would require restructuring its phase dependencies.

Haiku's weaknesses (slower timeline, less detailed integration tables) are additive fixes — they can be patched into the base without structural changes. Opus's weaknesses (missing schemas, deferred persona items, late observability) require structural surgery.

## 5. Specific Improvements from Opus to Incorporate

| # | Opus Element | Merge Action | Rationale |
|---|---|---|---|
| 1 | **Integration point tables** (per-phase artifact/type/wired/consumer format) | Adopt Opus's table format across all 5 Haiku phases. Add wiring phase and consumed-by columns where Haiku's tables are sparse. | Debate did not contest these; Opus's format is objectively better for developer handoffs and onboarding. |
| 2 | **INFRA-009: Docker Compose dev environment** | Add to Haiku Phase 1 as new task. AC: `pg+redis-in-compose; health-checks-pass; dev-startup<30s; testcontainers-compatible` | Haiku has no local dev environment task. Opus's inclusion is practical and uncontested. Effort: M, Priority: P1. |
| 3 | **Consolidated E2E/security gate** | Add a formal quality gate checkpoint between Haiku Phase 4 and Phase 5. Aggregate E2E (TEST-006/009-012), security pen test, and load results into a single pass/fail gate with explicit entry/exit criteria. | Debate convergence recommended hybrid: distributed unit tests (Haiku) + formal quality gate (Opus Phase 5 concept). Haiku distributes tests well but lacks a single sign-off moment before rollout. |
| 4 | **Critical path definition** | Add Opus's explicit critical path chain to Haiku's executive summary. | Haiku describes the critical path narratively; Opus's `INFRA-001 -> DM-001 -> COMP-005 -> ...` chain format is more actionable. |
| 5 | **Phase overlap notation** | Add a note in Haiku's timeline section indicating which phases can overlap if the team supports parallel frontend/backend streams, with a compressed 10-week alternative schedule. | Addresses the unresolved timeline dispute. Haiku's 13-week default is the safe baseline; the overlay shows teams with parallelism capacity how to compress without changing task order. |
| 6 | **SendGrid health as degraded state** | Modify Haiku's COMP-016 health endpoint AC to classify SendGrid failure as `degraded` rather than `unhealthy`. | Debate convergence recommendation. RSA key absence and PostgreSQL/Redis failures are hard failures; SendGrid loss degrades password reset but does not block login/register. |
