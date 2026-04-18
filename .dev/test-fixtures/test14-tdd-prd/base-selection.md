---
base_variant: B
variant_scores: "A:78 B:82"
---

## 1. Scoring Criteria (Derived from Debate)

Criteria surfaced across rebuttals and PRD requirements:
1. **Timeline realism & risk isolation** (debate R1-R2 core dispute)
2. **Scope discipline & completeness** (admin/Jordan dispute)
3. **Testing rigor** (dedicated M6 vs embedded dispute)
4. **Security & pen-test scheduling** (R-PRD-004 dispute)
5. **Operational readiness** (M8 vs M4 handover dispute)
6. **Business value delivery** (PRD S19 — $2.4M personalization unblock)
7. **Persona coverage** (PRD S7 — Alex/Jordan/Sam)
8. **Compliance alignment** (PRD S17 — SOC2 Type II, GDPR)

## 2. Per-Criterion Scores

| Criterion | Weight | Variant A (Opus) | Variant B (Haiku) |
|---|---|---|---|
| Timeline realism | 12 | 9 (risk-isolated; 16w credible for HIGH 0.72) | 6 (M4 carries 26 DLVs in 4w — overloaded per A's rebuttal) |
| Scope discipline | 12 | 7 (clean 4-endpoint boundary; OQ-008 deferred) | 9 (adds API-007/008/009/010 + COMP-011 bounded; excludes OAuth/MFA/RBAC) |
| Testing rigor | 14 | 10 (M6 dedicated; TEST-SEC-ENUMERATION ±10ms timing, TEST-IMPLICIT-LOAD nightly k6, pre-merge coverage gate) | 6 (SC-001..012 as measurements; B conceded these ≠ pre-merge gates) |
| Security/pen-test | 12 | 9 (COMP-PENTEST booked W6 + 1w remediation buffer) | 6 (release-gate framing right, but B conceded booking mechanics gap) |
| Operational readiness | 10 | 9 (dedicated M8; OPS-RSA-ROTATION automated; postmortem template) | 6 (runbooks written under MIG-002/003 rollout pressure — A's point) |
| Business value (PRD S19) | 14 | 5 (16w delays $2.4M personalization + SOC2 by 8w) | 10 (8w delivery; B's opportunity-cost argument direct) |
| Persona coverage (PRD S7) | 14 | 5 (Jordan JTBD deferred to v1.1; PRD explicitly lists admin audit/lock-unlock) | 10 (API-008 events query, API-009/010 lock/unlock, COMP-011 AdminAuditPage close Jordan gap) |
| Compliance (PRD S17) | 12 | 8 (12mo retention + full audit wiring + SOC2 dry-run) | 9 (same compliance baseline + admin audit visibility provides SOC2 Type II evidence directly) |

## 3. Overall Scores

**Variant A (Opus):** weighted 78/100 — technically superior in rigor, risk-isolation, and ops maturity, but structurally penalized on PRD alignment (Jordan deferral, business-value delay).

**Variant B (Haiku):** weighted 82/100 — faster time-to-value, complete PRD persona coverage, closes SOC2 evidence gap for Jordan, but conceded gaps in pen-test mechanics, pre-merge testing gates, and ops separation.

## 4. Base Variant Selection

**Base: Variant B (Haiku).**

Rationale:
- **PRD fidelity is the tiebreaker.** PRD S7 explicitly names Jordan with JTBD for audit/lock; Variant A's v1.1 deferral leaves a visible SOC2 Type II evidence gap before the Q3 2026 audit (PRD S17). Haiku's API-008/009/010 + COMP-011 directly satisfy Jordan's story.
- **Business-value delivery (PRD S19).** 8-week GA protects the $2.4M personalization revenue unlock cited in the PRD; 16 weeks pushes this past the Q2 2026 target.
- **Debate convergence recommendation explicitly names Haiku's linear graph + admin inclusion as the hybrid base,** with Opus layered on top for rigor — consistent with using B as the scaffold.
- **B's conceded gaps are localized fixes** (pen-test booking date, pre-merge test gates, ops phase) rather than structural rework.

## 5. Improvements to Incorporate from Variant A

Merge these Opus contributions into the Haiku-based scaffold:

1. **Testing rigor (A's M6 content, not the milestone):**
   - `TEST-SEC-ENUMERATION` — timing parity ±10ms across registered/unregistered emails on login + reset-request (A Item 71)
   - `TEST-IMPLICIT-LOAD` — k6 500-VU nightly in CI against staging with p95<200ms / err<0.1% gates (A Item 69)
   - `TEST-IMPLICIT-BCRYPT` / `TEST-IMPLICIT-RS256` — boot-time config validation fails-fast on weak config (A Items 67-68)
   - **Coverage threshold gate** — PR blocked if coverage drops below 80/15/5 (A's M6 NTG table)

2. **Pen-test booking mechanics (B conceded):**
   - Add explicit "pen-test vendor booked by W4" line item to M2 (adapt A's Week-6 booking rule to B's 8w timeline)
   - Reserve 1w remediation buffer before GA (A's M5 mitigation)

3. **Operational handover improvements:**
   - `OPS-RSA-ROTATION` quarterly key rotation automation (A Item 89)
   - `OPS-RETENTION-JOB` monthly partition-drop for 12mo audit retention (A Item 90)
   - `OPS-POSTMORTEM-TEMPLATE` blameless review webhook (A Item 91)

4. **Migration safety mechanics:**
   - `MIG-DATAMIG-BACKUP` pre-phase pg_basebackup + WAL (A Item 75)
   - `MIG-DUAL-RUN` idempotent upsert with divergence monitor alerting on >0.1% drift (A Item 76)
   - `MIG-002-ROLLBACK` explicit named trigger thresholds: p95>1000ms/5min, err>5%/2min, Redis conn fail>10/min (A Item 79)

5. **M1 scaffolding hardening:**
   - `COMP-INFRA-TLS` testssl.sh A+ gate (A Item 14)
   - `COMP-XSS-HARDEN` CSP strict-default + HSTS (A Item 57)
   - `COMP-DLP` secret-scrubbing middleware with allowlist (A Item 60)

6. **Timeline adjustment (debate consensus):**
   - Expand B's 8-week plan toward **10–12 weeks** to absorb M6 testing content and M8 ops separation without overloading M4. Concrete split: M4 (rollout, 3w) + M5 (ops handover, 1w), keeping B's linear graph.

7. **OQ resolution gates before freezes:**
   - Resolve OQ-007 (remember-me) and OQ-008 (admin scope confirmation) as hard gates before M2 code freeze (debate unresolved dispute #5).
