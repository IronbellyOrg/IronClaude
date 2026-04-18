---
base_variant: A
variant_scores: "A:86 B:75"
---

## Scoring Criteria (derived from debate)

Technical criteria from debate divergences #1-#12:
1. Timeline appropriateness (risk buffer vs velocity)
2. Phase structure coherence
3. Task decomposition clarity
4. Risk catalog completeness (R-008, R-009)
5. Rollback formalism
6. Compliance/SOC2 alignment (gate task)
7. Observability maturity
8. Admin/Jordan persona commitment
9. Frontend security hardening granularity
10. Open-questions governance

PRD-derived criteria:
11. Business value delivery (PRD S19 — Q2 2026 / $2.4M)
12. Persona coverage (PRD S7 — Alex, Jordan, Sam)
13. Compliance alignment (PRD S17 — SOC2, GDPR, NIST)

## Per-Criterion Scores (0-10)

| # | Criterion | A (Opus) | B (Haiku) | Evidence |
|---|---|---|---|---|
| 1 | Timeline | 7 | 8 | A: 16wk safer for SOC2 Q3; B: 12wk delivers $2.4M faster, still meets Q2 |
| 2 | Phase structure | 8 | 7 | A Phase 0/1 split isolates gating; B bundling creates coupling per R2 |
| 3 | Decomposition | 9 | 7 | A: 112 reviewable ACs; B: OPS-005 bundle loses implementation boundary |
| 4 | Risk catalog | 9 | 7 | A tracks R-008 (RSA)/R-009 (refresh race); B asserts subsumption |
| 5 | Rollback | 9 | 7 | A: ROLLBACK-PROC/TRIG/BACKUP-PRE drills; B: flag-flip only (MIG-003) |
| 6 | Compliance gate | 10 | 8 | A: SOC2-VALIDATION + DATA-MIN + NIST-PW explicit; B: TEST-010 implicit |
| 7 | Observability | 9 | 7 | A Phase 6 dashboards+alerts+SLO; B Phase 1 emission without paging |
| 8 | Admin persona | 9 | 6 | A commits API-008 + ADMIN-UNLOCK P1; B defers to OQ-010 |
| 9 | FE hardening | 9 | 7 | A discrete ACCESS-MEMORY/REFRESH-COOKIE/FE-401; B embedded in COMP-004 |
| 10 | OQ governance | 7 | 9 | B surfaces 11 (OQ-008/009/011); A silently resolved some |
| 11 | Business value (S19) | 7 | 9 | B ships 4wk earlier against $2.4M; A meets Q2 but later |
| 12 | Personas (S7) | 9 | 7 | A covers Alex+Jordan(committed)+Sam(JWKS); B defers Jordan |
| 13 | Compliance (S17) | 10 | 8 | A: SOC2 dry-run gate + GDPR consent row + 12mo retention; B partial |

## Overall Scores

**Variant A (Opus): 86/100** (subtotal 112/130 scaled)
Justification: Superior on compliance rigor (gate tasks), risk completeness (R-008/R-009), rollback formalism, admin persona commitment, and frontend hardening granularity. These align with PRD Section 17 (SOC2/GDPR/NIST), Section 7 (all three personas), and the HIGH complexity class (0.72). Cost is +4 weeks and governance transparency.

**Variant B (Haiku): 75/100** (subtotal 97/130 scaled)
Justification: Stronger on velocity, governance transparency (11 OQs), and business-value timing against the $2.4M personalization revenue. Weaker on SOC2 evidence rigor, admin scope commitment, and explicit failure-mode coverage. Defensible for velocity-focused teams with mature CI/CD but weaker for compliance-heavy context.

## Base Variant Selection: A (Opus)

Rationale:
- PRD Section 17 (Legal/Compliance) mandates SOC2 Type II audit trail, 12-month retention, NIST SP 800-63B compliance — Variant A's SOC2-VALIDATION gate + DATA-MIN + NIST-PW rows directly satisfy this; Variant B relies on implicit coverage via TEST-010.
- PRD Section 7 defines Jordan (admin) as a persona with JTBD "see who attempted access and lock compromised accounts" — Variant A commits ADMIN-UNLOCK + API-008 in Phase 6; Variant B leaves this as OQ-010 (deferral risk).
- Complexity class HIGH (0.72) with cryptographic, concurrency, and dual-datastore concerns — debate established (Opus R2) that rework on live deployment is catastrophic. The extra 4 weeks are risk-buffer, not ceremony.
- PRD Risk Analysis row "Compliance failure from incomplete audit logging" (Medium/High) is better mitigated by explicit gate (A) than test coverage alone (B).

## Improvements from Variant B to Incorporate in Merge

1. **Adopt Haiku OQ-008, OQ-009, OQ-011 as explicit decision-log rows** (not just open questions): even if Opus silently resolved retention/logout, the audit trail requires surfaced reconciliation per debate Round 2. Add `OQ-RECONCILE` rows in Phase 1 documenting PRD-over-TDD retention ruling.
2. **Add Haiku TEST-010 (audit log completeness with SOC2 field assertions)** into Phase 6 alongside SOC2-VALIDATION — test evidence complements the gate.
3. **Adopt Haiku's Phase 3 bundling of password-reset with frontend** partially: move `RESET-UI` (Phase 5 in Opus) earlier to enable Haiku's earlier E2E exercise without losing Phase 4 backend isolation. Run parallel.
4. **Incorporate Haiku OQ-010 as an explicit gate before ADMIN-UNLOCK effort lock** (PRE-OQ-010 in Phase 5 or early Phase 6) so product scope-down to v1.1 doesn't leave unpriced deletion per Haiku R2.
5. **Compress Phase 6 tuning into Phase 1 baseline + Phase 6 alerting split** per Haiku observability critique — `OPS-005` baseline emission in Phase 1 (telemetry shapes with real traffic), then `OPS-005.dash/alert/trace` maturation in Phase 6 (tuning with signal). Aligns with debate partial-convergence on 14-week middle ground.
6. **Adopt Haiku's uniform error envelope `{error:{code,message,status}}`** (explicit in Haiku API rows) as a cross-cutting contract row in Phase 2.
7. **Preserve Haiku's multi-device session row (OQ-009)** — it is a genuine PRD gap ("Concurrent login from multiple devices" Error Handling table) that Opus's OQ-004 understates.

Merge base remains A's 8-phase skeleton; these are additive refinements, not restructuring.
