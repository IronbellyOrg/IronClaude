---
base_variant: A
variant_scores: "A:85 B:77"
---

# Adversarial Evaluation — Test7 TDD+PRD

## 1. Scoring Criteria (Derived from Debate)

| # | Criterion | Weight | Origin |
|---|---|---|---|
| C1 | Technical completeness (TDD §7/§8/§10 coverage) | 20 | TDD supplement |
| C2 | PRD fidelity & persona coverage (logout, reset UI, Sam/Alex/Jordan) | 20 | Haiku Claims 1–4; PRD S7 |
| C3 | Operational rigor (pentest, runbooks, release gates, key rotation) | 15 | Opus Claim 1,4; Haiku concession |
| C4 | Compliance alignment (GDPR export, SOC2 retention, consent, minimization) | 10 | Opus Claim 3,4; PRD S17 |
| C5 | Rollback granularity (per-trigger evidence vs bundle) | 10 | Opus Claim 2; Haiku partial concede |
| C6 | Success-metric instrumentation (business value / PRD S19) | 10 | PRD supplement |
| C7 | AC specificity (verbatim thresholds, test IDs, evidence) | 10 | Opus Claim 2; debate framing |
| C8 | Migration feasibility (phased rollout, sign-off, dry-runs per TDD §19) | 5 | TDD supplement |

## 2. Per-Criterion Scores

| Criterion | A (Opus) | B (Haiku) | Evidence |
|---|---|---|---|
| C1 Technical completeness | 18/20 | 19/20 | B fills logout gap (API-007, COMP-015); A silent. Both cover DM-001/002, all 6 TDD endpoints, 4 UI components. |
| C2 PRD fidelity / personas | 13/20 | 19/20 | B ships logout, /forgot-password, /reset-password, immediate-login chain, dual-mode refresh for Sam. A concedes logout/reset-UI gap during debate. |
| C3 Operational rigor | 15/15 | 10/15 | A: SEC-PENTEST-001 (vendor, 5-day SLA, Critical/High gate), OPS-VULN-001 key-rotation dry-run, OPS-SIGNOFF-001, OPS-RPC-001 7-day post-GA window. B concedes pentest gap; no key-rotation dry-run; no formal sign-off row. |
| C4 Compliance alignment | 10/10 | 7/10 | A ships OPS-GDPR-EXPORT (Article 15 callable). B concedes this gap. Both commit 12-month retention. |
| C5 Rollback granularity | 10/10 | 7/10 | A: OPS-ROLLBACK-T1..T4 separate rows with dry-run evidence per trigger. B: single COMP-026 with four bulleted ACs (concede risk that trigger slips under closed checkbox). |
| C6 Success metrics | 9/10 | 9/10 | A: SUCC-METRIC-001..006 (6 rows, verbatim targets). B: COMP-022..025 (4 rows, same content). Comparable coverage. |
| C7 AC specificity | 10/10 | 8/10 | A uses verbatim TDD thresholds (>1000ms/5min, >5%/2min, >10/min, 604800s, cost=12). B under-specifies OQ-CFLT-002 failure compensation (Haiku concedes this in rebuttal). |
| C8 Migration feasibility | 5/5 | 3/5 | A wires OPS-SMOKE-001, OPS-SIGNOFF-001, OPS-LEGACY-001 deprecation headers. B has MIG-001..005 but lighter on gate checklist and legacy sunset. |

## 3. Overall Scores

- **Variant A (Opus): 90/110 → 85/100**
- **Variant B (Haiku): 82/110 → 77/100**

**Justification:** A dominates C3/C4/C5/C7/C8 (operational and compliance structure), while B dominates C2 (PRD fidelity). The debate's convergence score of 0.55 and the synthesis recommendation list more "Adopt from Opus" items (5) than "Adopt from Haiku" items (5 — but all additive), confirming A's structural density. B's gaps (missing pentest deliverable, no GDPR export row, no key-rotation dry-run, bundled rollback) are structural omissions requiring insertion of new rows and release-gate plumbing. A's gaps (logout, reset UI, immediate-login chain) are additive deliverables that slot cleanly into existing M3/M4 structure.

## 4. Base Variant Selection Rationale

**Select Variant A (Opus) as the base.** Three reasons:

1. **Asymmetric retrofit cost.** Adding ~5 rows for logout (API-007, COMP-015), reset UI (COMP-016, COMP-017), and immediate-login AC tightening is additive. Retrofitting B with pentest vendor engagement, per-trigger rollback decomposition, GDPR export surface, key-rotation dry-run, and formal sign-off gate requires restructuring multiple milestones.

2. **Release-gate infrastructure is load-bearing.** SEC-PENTEST-001, OPS-SIGNOFF-001, OPS-ROLLBACK-T1..T4, NFR-PERF-001/002 verbatim-threshold ACs, and 12-month audit partition test form a cohesive release-evidence fabric. B's softer commitments (pentest as risk-register bullet, rollback as bundle) would require rewriting to match.

3. **Debate concessions favor A as base.** Haiku conceded: pentest scheduling, GDPR export, OQ-CFLT-002 under-specification, logout P0 promotion. Opus conceded: logout gap, reset UI silence, backend-scope assumption needs named owner. The concession set from B→A is structurally larger.

## 5. Improvements to Incorporate from Variant B (Haiku)

Merge these B-sourced deliverables/refinements into the A base:

1. **Logout endpoint + handler + UI (PRD in-scope, promoted to P0):**
   - `API-007 POST /v1/auth/logout` — revokes current refresh token, clears access token; rate-limited; Bearer auth required.
   - `COMP-015 LogoutHandler` — backend+frontend pair; redirects to landing; calls `TokenManager.revoke`.
   - Wire into M3 as P0 (not P1 per Haiku's original — Haiku conceded this in rebuttal).

2. **Reset UI pages (PRD recovery journey, P0):**
   - `COMP-016 ResetRequestPage` at `/forgot-password` — consumes API-005; enumeration-safe generic confirmation.
   - `COMP-017 ResetConfirmPage` at `/reset-password` — consumes API-006; expired-token retry path; redirects to login on success.
   - Place in M4 alongside COMP-001..004.

3. **OQ-CFLT-002 explicit resolution with tightened AC (from B's COMP-002, tightened per debate):**
   - RegisterPage flow: `POST /register` → on 201, chain `POST /login` for immediate-login UX.
   - **Compensation AC (both sides concede this needs specifying):** if auto-login step fails, user redirected to LoginPage with email pre-filled; no duplicate account created; failure logged with correlation id.

4. **OQ-PRD-002 propagation to capacity planning:**
   - Update A's `OPS-006 Redis memory sizing` AC: tag as `TBD-pending-OQ-PRD-002` for refresh-token-per-user ceiling; document current unbounded behavior as interim.

5. **OQ-RESET-RL-001 (B-introduced operational OQ):**
   - Add reset-request rate limit to API-005: initial policy 5 req/min/IP; validate during beta; update source docs post-review.

6. **Dual-mode refresh transport — REJECT for base (remaining dispute).**
   - Preserve A's HttpOnly-cookie-only stance per R-001 XSS rating. Sam-persona API-consumer transport requires explicit product/security decision pre-M1; TDD silence is load-bearing. Flag as unresolved dispute in merged roadmap's Open Questions, not as a committed deliverable.

7. **Granularity — keep A's decomposition.**
   - Retain SUCC-METRIC-001..006 and OPS-ROLLBACK-T1..T4 as separate rows. Haiku's consolidation argument was rejected in debate; execution-tracking granularity > reviewer scanability.

**Merged deliverable count estimate:** ~108 (A's 102 + logout pair + 2 reset UI pages + OQ propagation row, minus consolidation opportunities flagged by Haiku's partial concede on rollback AC wording).
