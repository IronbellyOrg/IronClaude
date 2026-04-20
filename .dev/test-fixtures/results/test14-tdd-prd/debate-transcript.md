---
convergence_score: 0.62
rounds_completed: 2
---

# Structured Adversarial Debate: Opus 16-Week vs Haiku 8-Week Roadmap

## Round 1: Initial Positions

### Variant A (Opus — 16 weeks, 8 milestones)

**Position on timeline:** An 8-week compression is unrealistic for HIGH complexity (0.72) work spanning six cross-cutting domains. The 16-week plan isolates risk: M5 (NFR/compliance) cannot begin until M3/M4 are stable; M6 (testing pyramid) requires a hardened code surface before 80/15/5 targets can be validated. Collapsing these into Haiku's M3/M4 forces parallel execution of penetration testing, load testing, compliance dry-runs, and rollout — any slippage in one cascades into GA.

**Position on scope:** The 4-endpoint API surface (login/register/me/refresh + reset) is a deliberate architectural boundary. Adding API-007/008/009/010 (logout, admin audit, lock/unlock) inflates the attack surface and RBAC requirements before the core is stable. OQ-008 should be resolved *explicitly* — either add FR-AUTH-006 with proper design, or defer to v1.1 with BI-tool-based audit queries. Haiku's approach smuggles admin work in without a real FR spec.

**Position on testing:** Dedicated M6 (2 weeks) for 12 test deliverables including TEST-SEC-ENUMERATION (timing parity ±10ms) and TEST-IMPLICIT-LOAD (k6 nightly, p95<200ms) automates NFR drift detection. Haiku's 6 embedded tests in M3 rely on post-hoc validation metrics (SC-001..012), which detects failures only after user exposure.

**Position on pen-test:** COMP-PENTEST must be vendor-booked by Week 6 with a reserved 1-week remediation buffer. Treating pen-test as a release gate (R-PRD-004) without timeline allocation is how critical findings slip schedules.

### Variant B (Haiku — 8 weeks, 4 milestones)

**Position on timeline:** 16 weeks front-loads calendar cost without proportional risk reduction. Layered architecture (contracts → APIs → clients → rollout) naturally parallelizes: security module work (M1) and API handlers (M2) don't need separate milestones when the dependency graph is linear. The organization bleeds $2.4M in personalization revenue and a SOC2 Type II dependency every month the auth foundation is missing — doubling duration to isolate risk has a real opportunity cost.

**Position on scope:** The Jordan persona (admin audit view, lock/unlock) is a PRD requirement, not a "nice to have." Opus flags OQ-008 as an open question with "descope to v1.1" as an option — that is a visible PRD/TDD gap that Haiku closes with bounded deliverables (API-008/009/010, COMP-011). This is *scope discipline*, not scope expansion: Haiku explicitly excludes OAuth, MFA, and RBAC.

**Position on testing:** Success criteria SC-001..012 are better as actionable deliverables with owners and methods than as a measurement table. Haiku's M4 SC deliverables each have an ID, metric, target, and validation method — clearer ownership than Opus treating them as a summary artifact.

**Position on pen-test:** R-PRD-004 is a *release gate*, not a schedule filler. Hard-booking vendors at Week 6 assumes findings arrive before code stabilizes. Haiku treats pen-test as a blocking condition in M4 with "rollout blocked on critical findings resolved" — which is the actual compliance requirement.

## Round 2: Rebuttals

### Variant A Rebuttal (Opus)

**On Haiku's timeline defense:** The "layered architecture naturally parallelizes" argument assumes adequate staffing. Haiku's M4 contains 26 deliverables (migration + operations + 12 success criteria + 7 risk mitigations + 4 security reviews) across 4 weeks. That's 6.5 deliverables per week on a release phase — historically the *least* forgiving phase. Opus's M7 (3 weeks for rollout) + M8 (1 week for ops) separates these concerns with dedicated exit criteria per phase. The opportunity-cost argument is valid but cuts both ways: a botched rollout that triggers R-003 data corruption costs more than 8 weeks of additional calendar.

**On Haiku's scope defense:** Haiku claims scope discipline while adding 4 new endpoints (API-007/008/009/010) and a new page component (COMP-011) as P1 deliverables. The "admin-only" constraint on API-008/009/010 requires an RBAC mechanism — which Haiku simultaneously declares out-of-scope. That's a contradiction: you cannot enforce "admin-only" without role checks, and role checks beyond the default `roles:["user"]` array aren't specified. Opus's deferral to v1.1 is honest about the dependency.

**On Haiku's testing defense:** Success criteria as deliverables is not equivalent to a test pyramid. SC-001 ("login p95 < 200ms via APM") is a *measurement* — it doesn't prevent regressions; it only detects them after the fact. Opus's TEST-IMPLICIT-LOAD runs nightly in CI, blocking merges. Haiku has no equivalent pre-merge NFR gate.

**On pen-test scheduling:** "Release gate" without booking is aspirational. Security vendors typically have 4–8 week booking lead times; if Haiku discovers this at M4 week 1, the release slips to accommodate vendor availability, not the other way around.

### Variant B Rebuttal (Haiku)

**On Opus's risk-isolation defense:** Opus's 8-milestone structure introduces its own coordination overhead. Multi-branch dependency graph (M1→M2→M3→M4 parallel to M1→M5; M3/M4/M5 converge into M6) requires synchronization points that in practice become status-meeting tax. Haiku's linear M1→M4 graph matches how the work actually flows: you cannot do NFR validation (M5) before the code exists (M3), and the "parallelism" Opus claims is largely illusory because most teams cannot staff frontend, backend, ops, and testing streams simultaneously at full fidelity.

**On the admin scope contradiction:** Fair point on RBAC dependency. However, the `users` schema already includes `roles:text[]-NN-DEFAULT'{"user"}'` — a boolean admin check against `'admin' = ANY(roles)` is ~3 lines of middleware, not an RBAC system. Haiku can enforce "admin-only" without designing a role hierarchy, permission matrix, or delegation model. Opus's deferral ignores that Jordan's JTBD is directly tied to SOC2 evidence (PRD S17) — deferring to v1.1 means the SOC2 auditor at M5 dry-run sees an incomplete story.

**On testing rigor:** Conceded that success criteria ≠ pre-merge gates. However, the 80/15/5 pyramid is achievable inside M3 if framed as a coverage threshold gate (which Haiku's CI can enforce identically). The real divergence is whether load + security tests *need* their own milestone or can run nightly during rollout. For a 4-endpoint surface, nightly k6 against staging during MIG-001 alpha is sufficient — dedicated M6 is over-engineered for this surface area.

**On pen-test booking:** Accepted. Haiku should amend M4 to include an explicit "pen-test vendor booked by W4" entry — this is a process gap, not a strategic difference. The release-gate framing remains correct; the booking mechanics are a planning fix.

## Convergence Assessment

### Areas of Strong Agreement (already shared)
All 10 shared assumptions hold: stateless JWT + Redis, bcrypt cost 12, RS256/2048-bit, 12-month audit retention, phased rollout with feature flags, `/v1/auth/*` versioning, 5/15-min lockout, parallel-run migration, Prometheus+OTel stack, and HIGH complexity classification.

### Areas of Emerging Convergence (moved during debate)
- **Pen-test booking:** Variant B conceded that explicit vendor-booking timeline is required; this was a planning gap, not a strategic split. Both now agree on booking-by-W4 (Haiku) / booking-by-W6 (Opus).
- **Testing gates:** Variant B conceded that SC measurements are not pre-merge gates; both now agree coverage thresholds (80/15/5) and nightly k6 should be enforced — disagreement reduces to whether this needs a dedicated milestone.
- **Admin scope RBAC dependency:** Variant B acknowledged the `roles` array needs an enforcement path; Variant A can accept a minimal `'admin' = ANY(roles)` check if staffing allows adding API-008/009/010 without compromising core stability.

### Remaining Disputes (unresolved)
1. **Timeline (8 vs 16 weeks):** Core disagreement on staffing model and risk tolerance. Requires team velocity data — neither variant's argument is purely correct without it.
2. **Dedicated M6 testing phase vs embedded testing:** Variant A sees milestone separation as risk isolation; Variant B sees it as over-engineering for 4–6 endpoints. This is a philosophical split on whether testing deserves its own phase or should be continuous.
3. **Admin v1.0 inclusion vs deferral:** Variant A prefers clean 4-endpoint surface with v1.1 deferral; Variant B prefers closing the SOC2 Jordan gap immediately. The SOC2 audit timing (Q3 2026) tips toward Variant B if admin audit is required evidence; toward Variant A if BI-tool queries satisfy the auditor.
4. **Operational handover (dedicated M8 week vs in-flight in M4):** Variant A's separation enables peer review of runbooks; Variant B accepts runbook validation under rollout pressure. Genuine tradeoff between review depth and calendar cost.
5. **Remember-me (OQ-007) and progressive CAPTCHA:** Both variants have different positions on v1.0 inclusion. Unresolved and needs product decision before M3/M4 frontend freeze.

### Recommended Resolution Path
A hybrid approach would: (a) adopt Haiku's linear dependency graph and admin inclusion (API-007/008/009/010), (b) adopt Opus's dedicated pen-test booking, testing rigor (TEST-SEC-ENUMERATION, TEST-IMPLICIT-LOAD), and operational handover phase, (c) target a 10–12 week timeline as the realistic middle ground, (d) resolve OQ-007 and OQ-008 as hard gates before M2 code freeze. Convergence score of 0.62 reflects substantial agreement on architecture and security fundamentals but genuine disagreement on timeline, testing structure, and admin scope that requires organizational judgment rather than further debate.
