---
convergence_score: 0.55
rounds_completed: 2
---

# Adversarial Debate: Opus vs Haiku Roadmap Variants

## Round 1 — Opening Positions

### Variant A (Opus) — Opening Position

**Thesis:** Operational rigor and release-gate evidence are the binding constraints on shipping a production auth service. A 102-deliverable decomposition is not sprawl — it is the traceability primitive that separates "we plan to do X" from "X is owned, measured, and verified."

**Key claims:**

1. **Pentest as a scheduled gate (SEC-PENTEST-001), not a risk-register wish.** R-PRD-002 ("Security breach from implementation flaws") is rated Critical. A risk mention without a scheduled deliverable, external vendor commitment, 5-business-day triage SLA, and Critical/High-gate-before-M5 is not a mitigation — it's an aspiration. Variant B leaves this as a soft commitment.

2. **Per-trigger rollback decomposition (OPS-ROLLBACK-T1..T4) prevents slippage.** Bundling all four triggers into a single COMP-026 row means one owner, one AC, one test. Verbatim TDD thresholds (>1000ms/5min, >5%/2min, >10/min Redis, data corruption) each need their own dry-run evidence, alert wiring, and false-positive runbook. A bundle hides which trigger wasn't tested.

3. **Compliance deliverables must live in the milestone where the work happens.** NFR-COMPLIANCE-001..004 distributed across M1/M2/M4 creates milestone-local traceability — the consent field is acceptance-tested when registration is built, not months later. Haiku's M1-baseline-plus-M4-verification bundle delays evidence visibility and risks a late-cycle compliance surprise.

4. **Production key rotation dry-run (OPS-VULN-001) and GDPR export (OPS-GDPR-EXPORT) are concrete capabilities, not process gestures.** Documenting a quarterly rotation procedure is different from executing the first one under production conditions. Article 15 rights require a callable export surface, not an implicit claim in NFR-COMPLIANCE-004.

5. **Scope discipline via Non-Goals rule.** Opus explicitly states Non-Goals (OAuth, MFA, RBAC enforcement, remember-me, API-key auth) are never relitigated in milestone ACs. This prevents the logout/reset-UI scope creep that Haiku introduces.

### Variant B (Haiku) — Opening Position

**Thesis:** A roadmap that omits PRD-in-scope behavior is not a v1.0 roadmap — it is a technical subset. User-visible completeness (logout, reset UI, immediate-login UX) is a release requirement, not a nice-to-have, and explicit conflict resolution is what makes a roadmap actually executable across two source documents.

**Key claims:**

1. **Logout is PRD in-scope and Opus silently drops it.** The PRD marks logout as in-scope for shared-device safety (a real user story). TDD omits the endpoint. Opus inherits the TDD gap without acknowledgment; Haiku ships API-007 `POST /auth/logout` + COMP-015 LogoutHandler. Shipping v1.0 GA without logout is a user-visible regression.

2. **Reset UI pages are part of the recovery journey.** `/forgot-password` (COMP-016) and `/reset-password` (COMP-017) are how users actually complete reset. Opus ships the backend endpoints and assumes "some other team" owns the UI. That's a handoff to nobody at GA.

3. **Explicit conflict identification and resolution.** OQ-CFLT-002 (PRD wants immediate login post-register; TDD API-002 returns `UserProfile`) is a real contract-vs-UX tension. Haiku names it and resolves via frontend chaining — preserves TDD contract, meets PRD outcome. Opus is silent on this conflict, leaving onboarding friction unaddressed.

4. **Dual-mode refresh-token transport serves both personas.** HttpOnly cookie for Alex (browser) AND request-body refreshToken for Sam (API consumer). Opus's cookie-only approach is more XSS-restrictive but constrains non-browser clients — which is the PRD's explicit secondary persona.

5. **Propagating open questions into capacity planning.** OQ-PRD-002 (refresh-token-per-user ceiling) threads into OPS-006 Redis sizing. Opus treats it as "open, unbounded permitted" — leaves the sizing implication uncaptured. Haiku flags it as TBD-pending-OQ-PRD-002, which is honest capacity planning.

6. **Granularity consolidation aids scanability.** 77 deliverables vs 102 means reviewers can actually hold the roadmap in their head. Opus's six separate success-metric rows (SUCC-METRIC-001..006) are the same information as Haiku's four analytics components (COMP-022..025) but heavier to navigate.

## Round 2 — Rebuttals

### Variant A (Opus) — Rebuttal to Variant B

**On logout (B's Claim 1):** Concede partially. Logout is indeed PRD in-scope, and Opus's silence is a gap. However, Haiku lists API-007 at **P1, not P0**, and COMP-015 is P1. A P1 deliverable on a 2-week terminal milestone (M3) at the edge of the critical path is at material risk of being cut under schedule pressure. If logout is truly GA-blocking, it needs to be P0 — and Haiku doesn't commit to that. Opus's silence is worse, but Haiku's P1 label is a soft commitment in disguise.

**On reset UI (B's Claim 2):** The PRD's user-story-level "users complete reset" is a journey outcome; where that UI lives is an architectural decision. Opus's scope assumption (backend service provides endpoints; consuming application owns the flow) is defensible *if* the consuming app team is on the hook. However, Opus never names that assumption or that team — so this is a legitimate gap. Concede.

**On OQ-CFLT-002 (B's Claim 3):** Haiku's resolution (chain POST /register → POST /login on the frontend) introduces a two-request onboarding path with its own failure modes (register succeeds, auto-login fails → user in a weird state). That complexity needs to live *in the AC*, not just the OQ. Haiku's COMP-002 AC says "flow: POST /auth/register then POST /auth/login for immediate UX login" but doesn't specify the compensating behavior when step 2 fails. Opus's silence is scope avoidance; Haiku's resolution is under-specified.

**On dual-mode refresh transport (B's Claim 4):** This is the most substantive disagreement. Dual-mode doubles the attack surface review, doubles the E2E test matrix, and means the pentest (which Haiku doesn't schedule) must cover both. Opus's cookie-only stance is consistent with R-001 (XSS token theft) being rated Medium/High. If Sam the API-consumer is genuinely v1.0 scope, the TDD would have specified the transport — it didn't. Haiku is inferring persona requirements the TDD deferred. **Reject.**

**On granularity (B's Claim 6):** 77 vs 102 deliverables is not about reviewer cognitive load — it's about execution tracking. When Sprint 4 starts and someone asks "is OPS-ROLLBACK-T3 (Redis) dry-run complete?", Opus has a row. Haiku has a bundled COMP-026 AC with four items in one line. The consolidation B praises is the same consolidation that lets trigger T3 slip under a closed T1/T2 checkbox. **Reject.**

### Variant B (Haiku) — Rebuttal to Variant A

**On pentest scheduling (A's Claim 1):** Concede. Scheduling SEC-PENTEST-001 with a named vendor, triage SLA, and Critical/High gate is materially stronger than a risk-register bullet. Haiku should adopt this as a P0 M4 deliverable. The argument that "mention implies commitment" is not how release gates work.

**On per-trigger rollback rows (A's Claim 2):** Partial concede with caveat. Per-trigger decomposition helps execution tracking — granted. But Opus's OPS-ROLLBACK-T1..T4 rows reference the *same* automation wiring, *same* flag-disable action, *same* runbook. The decomposition is 4x rows for what is substantially one component with four threshold configurations. A middle ground — one COMP row plus four AC bullets with owner/evidence per trigger — captures the tracking benefit without inflating the deliverable count. **Partial concede.**

**On compliance distribution (A's Claim 3):** Reject. Milestone-local compliance traceability sounds good but in practice means compliance reviewers chase artifacts across four milestones. Consolidating compliance verification in M4 (after the code is built) is how SOC2 audits actually run — evidence is gathered against implemented behavior, not against in-flight code. Opus's distribution optimizes for traceability diagrams, not audit workflow.

**On GDPR export and key-rotation dry-run (A's Claim 4):** Concede on GDPR export — Article 15 is a callable capability, and Haiku's NFR-COMPLIANCE-004 bullet doesn't commit to delivering the export surface. OPS-GDPR-EXPORT as a P1 M5 deliverable should be adopted. **On production key rotation dry-run**: reject as premature. The first quarterly rotation should happen in production naturally at the quarter boundary; forcing it into M5 adds risk during GA-stabilization. Opus is correct the runbook needs validation, but dry-runs belong in staging.

**On Non-Goals scope discipline (A's Claim 5):** Reject the framing. Logout, reset UI, and immediate-login UX are **not** Non-Goals — they are PRD-in-scope items TDD failed to spec. Invoking "scope discipline" to exclude PRD scope inverts the relationship between specs and roadmap. Opus conflates "discipline against scope creep" with "discipline against PRD fidelity."

**On logout P1 (responding to A's counter):** Valid critique. If Haiku argues logout is GA-blocking, it should be P0. Concede — API-007 and COMP-015 should be promoted to P0.

**On OQ-CFLT-002 under-specification (responding to A's counter):** Valid. COMP-002 AC needs to specify failure compensation: "if auto-login step fails, user is redirected to LoginPage with email pre-filled; no duplicate account created." Concede — resolution needs tightening.

## Convergence Assessment

**Convergence score: 0.55** — moderate. Substantial agreement on 20 shared assumptions and several debate points; material disagreement on 4–5 architectural/process questions.

### Areas of Agreement Reached During Debate

1. **Pentest must be a scheduled P0 deliverable** (Haiku concedes; adopts Opus's SEC-PENTEST-001 pattern).
2. **GDPR Article 15 export needs a concrete deliverable** (Haiku concedes; adopts OPS-GDPR-EXPORT).
3. **Logout and reset UI are GA-blocking v1.0 scope** (Opus concedes the gap; Haiku concedes they must be P0, not P1).
4. **OQ-CFLT-002 resolution needs tightened AC** covering auto-login failure compensation (both concede under-specification).
5. **Opus's backend-only scope assumption needs named ownership** (Opus concedes silence is a gap).
6. **Pre-existing consensus:** 12-month audit retention, bcrypt cost-12, RS256/2048, 10-week schedule, technical-layer milestone structure, stateless JWT with Redis refresh, three-phase rollout, automated rollback (no human gate), core risk taxonomy.

### Areas of Partial Convergence

- **Rollback trigger granularity:** Middle ground acceptable — one RollbackAutomation component with four per-trigger ACs carrying owner + dry-run evidence (captures Opus's tracking without Haiku's bundling risk).
- **Deliverable count:** Neither 102 nor 77 is obviously correct; the right count is whatever maps 1:1 to sprint-level ownership. Post-debate, numbers converge closer (Haiku +2–3 for pentest/GDPR/logout P0; Opus possibly −3–4 if rollback triggers consolidate).
- **Compliance distribution:** Unresolved methodological dispute (in-flight traceability vs audit-time consolidation). Both are defensible; team preference decides.

### Remaining Material Disputes

1. **Refresh-token transport strategy.** Cookie-only (A) vs dual-mode cookie + body (B). This is a persona-scope question: is Sam the API-consumer v1.0 scope? TDD is silent; PRD implies yes. Needs product decision before M3, not roadmap assertion.

2. **Production key rotation dry-run (OPS-VULN-001).** A argues validate runbook under real conditions; B argues stabilize GA first and let the quarter boundary trigger it naturally. Risk tolerance question.

3. **Compliance deliverable distribution.** A: milestone-local. B: M4-consolidated. Methodological preference, not a correctness question.

4. **CAPTCHA as scheduled P1 (A) vs risk-register contingency (B).** A is more conservative; B accepts deferred commitment. Depends on whether brute-force likelihood estimate (R-002: High) warrants proactive scheduling.

5. **Refresh-token-per-user ceiling (OQ-PRD-002).** A leaves unbounded; B flags TBD-pending-OQ. Neither resolves it — both are honest, but Haiku's TBD propagates to capacity planning, which is the more operationally correct posture.

### Synthesis Recommendation

Neither variant is dominant. A combined roadmap would:

- **Adopt from Opus:** Pentest scheduling, GDPR export deliverable, per-trigger rollback ACs (not rows), Non-Goals rule framing, success-metric decomposition for release evidence.
- **Adopt from Haiku:** Logout endpoint + UI (promoted to P0), reset UI pages, OQ-CFLT-002 explicit resolution with tightened AC, OQ-PRD-002 propagation into Redis sizing, reset-request rate limit (OQ-RESET-RL-001).
- **Unresolved and requiring product/security decisions pre-M1:** refresh-token transport strategy, rollback trigger row vs AC granularity, compliance milestone distribution.

Convergence 0.55 reflects genuine resolution on ~6 of ~10 debate points with 4–5 remaining disputes that require external decision-makers rather than further debate.
