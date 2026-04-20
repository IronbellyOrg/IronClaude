---
convergence_score: 0.62
rounds_completed: 2
---

# Adversarial Debate: Opus vs Haiku Roadmap Variants

## Round 1 — Initial Positions

### Variant A (Opus) — Opening Statement

**1. Schedule realism is non-negotiable.** Today is 2026-04-20. M1's TDD target was 2026-04-14. Haiku's calendar (M1: 2026-03-31 → 2026-04-14) is already impossible. Shipping a plan that is internally inconsistent with the current date on page one undermines executive trust and hides the real compression risk from M4/M5.

**2. Technical-layer decomposition parallelizes better.** Foundation → Token → Compliance → Frontend → Production keeps each milestone narrow. Haiku's M4 carries 26 deliverables spanning performance, observability, admin ops, and security review — a single hardening chokepoint before rollout.

**3. Automated rollback honors the TDD contract.** TDD §19.4 uses the phrase "automatic conditions." `ROLLBACK-AUTO-LATENCY/ERR/REDIS/DATA` implements that literally. Haiku's human-gated drill accepts MTTR latency measured in minutes per incident — exactly when users are churning.

**4. Defer admin UI to v1.1.** PRD persona Jordan can be served by raw SQL query access at GA (documented in OPS-003 runbook). Adding `API-008/009/010` plus `COMP-018/019` to pre-GA scope is feature creep against a compressed schedule.

**5. Preserve optionality via open questions.** 8 tracked OQs are not failures — they are legitimate stakeholder alignment items (refresh token cap, remember-me, sync/async email). Committing a default without product review is velocity theater.

**6. Load test early.** `NFR-PERF-002` at M1 catches capacity issues before M2/M3 dependencies compound fix cost. Haiku pushes load testing to M4 against a more complete system but much later and more expensive to correct.

### Variant B (Haiku) — Opening Statement

**1. Preserve the TDD calendar as the published commitment.** The GA date 2026-06-09 is the stakeholder contract. Opus's "compressed" schedule front-loads risk into M1 (2 weeks vs original 2) and creates M4/M5 overlap that itself becomes a slip multiplier. If M1 has already slipped, that's a status update — not grounds to rewrite five milestone anchors.

**2. Thematic layering produces cleaner sign-off gates.** Foundation/Contracts → Core Logic → User Journeys → Hardening/Compliance → Rollout maps to how auditors, security reviewers, and operators actually consume the work. Hardening concentrated in M4 gives SOC2 a single review surface.

**3. PRD capability completeness is a release requirement, not a v1.1 aspiration.** Logout (`API-007`) closes stolen-refresh-token TTL exposure. Admin APIs (`API-008/009/010`) satisfy Jordan persona and give SOC2 operational readiness. Shipping without these means GA is functionally incomplete against the PRD user stories.

**4. Close open questions with committed defaults.** Resolving 11 of 13 OQs (5-token refresh cap, async email, register → login redirect, API-key deferral) removes decision debt from the execution path. Opus's 8 open items risk blocking downstream work while waiting for product review.

**5. Surface conflicts explicitly.** `CONFLICT-2` (PRD auto-login vs TDD 201-redirect) is a real product decision with measurable impact on the >60% conversion target. Opus silently implements the TDD contract without documenting the gap — that's how roadmaps lose product trust.

**6. Early compliance wiring prevents schema churn.** Consent capture at M1 (`NFR-COMP-001`, `COMP-013`, wired via `COMP-020` in M2) avoids a late schema migration window. Opus's M3 consent placement leaves registration operating without consent capture during M1-M2.

## Round 2 — Rebuttals

### Variant A (Opus) — Rebuttal

**On calendar:** Haiku's "preserve GA 2026-06-09" is rhetorical — Opus also preserves 2026-06-09 via M4/M5 overlap. The difference is honesty: Opus documents the compression in `OQ-M1-001` and `R-M1-SCHED`; Haiku hides it by printing impossible start dates. Both plans land on the same GA date; only one is falsifiable.

**On admin APIs:** Jordan's PRD story is "view authentication event logs" and "lock compromised accounts." Raw SQL access to `auth_audit_log` satisfies the first. Lockout is already automatic (`FEAT-LOCK` 5/15min). Manual admin lock/unlock is a convenience, not a SOC2 blocker — the auditor cares about the audit trail, which Opus delivers identically in M1 (`DM-AUDIT`).

**On conflict surfacing:** Opus's decision table explicitly records "Audit-log retention: 12 months (PRD overrides TDD §7.2)." That's exactly the pattern Haiku claims is missing. The auto-login conflict is worth noting — fair point — but resolving it to the TDD contract (Haiku's own choice) makes it a footnote, not a blocker.

**On closing OQs:** Committing "5 refresh tokens per user, evict oldest on sixth" without product-manager review is the same velocity theater Haiku accuses Opus of avoiding. Where's the UX research on multi-device behavior? A tracked OQ with a target date beats an arbitrary number baked into Redis sizing.

**On M4 chokepoint:** Haiku's M4 at 26 deliverables spanning performance validation, 6 observability tasks, 4 runbooks, 3 admin APIs, and a security review is the definition of single-point-of-failure scheduling. If any of those 26 items slips, GA slips. Opus's distributed hardening lands each concern alongside the feature that introduces it.

### Variant B (Haiku) — Rebuttal

**On schedule realism:** "Honesty in documentation" and "calendar preservation" are not mutually exclusive. Haiku treats M1's slip as execution status to manage in standup, not roadmap text to rewrite. The M4/M5 overlap Opus proposes is itself a schedule risk — staged rollout over a frontend integration that is still converging is exactly where defects slip into production.

**On rollback automation:** TDD §19.4's "automatic conditions" language describes *triggers*, not *actuators*. Building four dedicated automation deliverables (`ROLLBACK-AUTO-*`) adds infrastructure with its own failure modes — watchers that mis-fire, integrity checks that false-positive. A drilled runbook (`TEST-012`) with alert routing is well-understood technology. Opus is gold-plating MTTR when the incident rate at 1000 DAU is empirically near zero.

**On admin scope:** "Raw SQL access for GA" assumes the admin team has DB credentials, query guidance, and incident response muscle memory. None of those are free. `API-008/009/010` is three M-sized deliverables — 1-1.5 weeks of work — that converts an undocumented escalation path into a supported one. That's not scope creep; that's shipping what the PRD promised.

**On open questions:** The 5-token refresh cap is derived from the extraction — it's not arbitrary. The alternative (unbounded per-user tokens) has a concrete Redis sizing risk. Every OQ Opus leaves open is a decision someone will make under schedule pressure in week 4 without product review. Closing them upfront with documented defaults invites review *before* execution starts.

**On observability distribution vs concentration:** Opus's metric tasks exist (`METRIC-REG`, `METRIC-LOGIN`, etc.) but they're P1, individually small, and spread across milestones — which is exactly how instrumentation gaps ship. Haiku's M4 OBS-001..007 treats observability as a first-class deliverable with acceptance criteria and a named owner.

## Convergence Assessment

**Strong agreement (shared foundation, 15 assumptions):** Both variants converge on stateless JWT + Redis refresh architecture, bcrypt cost 12, RS256 2048-bit, self-hosted AuthService, 12-month audit retention (PRD overrides TDD §7.2), 5-milestone structure, GA 2026-06-09, HttpOnly refresh cookie + in-memory access token, Kubernetes HPA 3→10, SLO targets (p95 login <200ms, refresh <100ms, 99.9% availability), and staged rollout gated by `AUTH_NEW_LOGIN` + `AUTH_TOKEN_REFRESH` flags.

**Narrow disputes (resolvable with clarification):** Health endpoint shape (both deliver it, Haiku makes it explicit via `API-011`), refresh token quota (both need a number, Haiku committed, Opus deferred), registration auto-login conflict (both resolve to TDD contract, only Haiku documents it). These would converge trivially in a joint review.

**Genuine strategic disputes (require stakeholder decision):**
- **Admin APIs pre-GA vs v1.1:** Depends on whether SOC2 Type II audit and Jordan persona support are GA-blocking. Executive/compliance decision.
- **Automated rollback vs drilled runbook:** Engineering cost vs MTTR tradeoff. SRE/platform decision.
- **OQ closure policy:** Organizational preference for decision velocity vs stakeholder alignment.
- **Milestone layering:** Technical (Opus) parallelizes better; thematic (Haiku) sign-offs cleaner. Program management decision.
- **Schedule documentation style:** Whether to print the slip (Opus) or manage it operationally (Haiku).

**Areas where one variant is clearly stronger:**
- Opus wins on: schedule realism, rollback automation fidelity to TDD §19.4, success-criteria traceability (`SUCC-SLO-BOARD`), early load testing, risk register depth (13 vs 10 risks with explicit schedule + key rotation entries).
- Haiku wins on: PRD capability completeness (logout + admin APIs), open-question closure rate, explicit conflict surfacing, earlier compliance wiring, clearer operator runbooks per component.

**Unresolved after debate:** 5 of 18 divergence points. The two plans represent genuinely different execution philosophies — Opus optimizes for engineering rigor and schedule honesty; Haiku optimizes for product completeness and decision velocity. Neither dominates; the right choice depends on which class of risk (execution slip vs capability gap) the organization finds more expensive.
