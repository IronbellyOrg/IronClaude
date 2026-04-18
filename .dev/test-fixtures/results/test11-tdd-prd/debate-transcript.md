---
convergence_score: 0.65
rounds_completed: 2
---

# Structured Adversarial Debate: Opus vs. Haiku Roadmap Variants

## Round 1 — Initial Positions

### Variant A (Opus — 16 weeks, 8 phases, 112 rows)

**Position on timeline (Divergence #1):** The 16-week plan is the correct risk posture for a HIGH-complexity (0.72) security-critical system with SOC2 Q3 2026 deadline. Compressing to 12 weeks assumes primitives work first-try; cryptographic and concurrency rework on a live deployment is catastrophically expensive.

**Position on phase granularity (#2, #3):** Isolating Phase 0 (Infrastructure) as a gating concern lets SRE, security, and backend work in parallel without coupling. 112 task rows is not bureaucratic overhead — each row is a discrete acceptance criterion that reviewers and estimators can sign against. Coarse bundling (Haiku's `OPS-005` as one row covering logs+metrics+traces+alerts) produces ambiguity at the implementation boundary.

**Position on risk coverage (#5, #8):** R-008 (RSA key compromise) and R-009 (refresh-rotation race) are material operational failure modes. The PRD mandates quarterly rotation; a race condition on Redis swap causes user lockouts that are indistinguishable from attack. Leaving these implicit is how production incidents happen.

**Position on compliance and rollback (#8, #10):** `SOC2-VALIDATION` as a formal gate task and explicit `ROLLBACK-PROC`/`ROLLBACK-TRIG`/`BACKUP-PRE`/`POST-GA-VERIFY` rows convert "we should be ready" into verifiable artifacts. Flag-flip alone is rollback *configuration*, not rollback *procedure*.

**Position on admin scope (#12):** Jordan's JTBD is PRD-required, not optional. Committing to `API-008` + `ADMIN-UNLOCK` in Phase 6 prevents late descoping that would break the compliance story.

**Position on frontend hardening (#11):** `ACCESS-MEMORY`, `REFRESH-COOKIE`, `FE-401-INTERCEPT` as discrete rows make R-001 (XSS) mitigations individually reviewable. Embedding them inside `AuthProvider`'s contract (Haiku) means a reviewer cannot audit XSS posture without reading the implementation.

### Variant B (Haiku — 12 weeks, 5 phases, 67 rows)

**Position on timeline (#1):** 12 weeks aligns to the PRD's Q2 2026 target with genuine slack against Q3 SOC2. Opus's extra 4 weeks are spent on ceremony (dedicated observability phase, rollback drill rows) that mature teams fold into ongoing work. Every additional week is business value deferred against the $2.4M personalization-dependent revenue.

**Position on phase structure (#2):** 5 phases with Phase 1 bundling infra+security+data primitives reflects how this work actually gets done — the same security engineer ratifying SEC-POLICY-001 is the one who provisions RSA keys. Opus's Phase 0/Phase 1 split creates artificial handoff cost.

**Position on open questions (#4):** 11 open questions vs 7 is not a weakness — it's honesty. OQ-008 (retention conflict), OQ-009 (multi-device policy), OQ-010 (admin unlock scoping), OQ-011 (logout gap) are genuine PRD/TDD conflicts that Opus silently resolved without stakeholder sign-off. Surfacing ambiguity for product+security is correct governance.

**Position on password reset sequencing (#7):** Shipping reset alongside frontend (Phase 3) enables end-to-end user journey testing earlier. Opus's Phase 4 isolation means reset backend sits un-exercised by real UI for two weeks.

**Position on observability (#9):** Baseline instrumentation in Phase 1 (`OPS-005` covering logs/metrics/traces/alerts) lets telemetry mature across Phases 2-5 with real traffic shaping the dashboards. Opus's dedicated Phase 6 tunes dashboards after the fact — backward.

**Position on rollback (#10):** Rollback-as-flag-flip is the *modern* pattern. Drill tasks and backup pre-stages are pre-CI/CD-era rituals; the real rollback safety comes from feature flags, idempotent migrations, and PITR — all of which Haiku already specifies.

**Position on risk coverage (#5):** R-008 and R-009 are subsumed by existing mitigations (quarterly rotation in COMP-007; fail-closed in COMP-006). Adding rows for every conceivable failure mode inflates the risk register without adding mitigation rigor.

## Round 2 — Rebuttals

### Variant A rebuts Variant B

**On "12 weeks aligns to Q2 target":** The PRD target is "v1.0 Q2 2026" — Opus ships Week 16 = 2026-06-09, still Q2. Haiku's 4-week acceleration buys zero calendar value against Q2 but costs the SOC2 dry-run gate. If SOC2 evidence assembly slips (OPS-002 runbook in Haiku Phase 4 isn't a gate), Q3 audit is at risk, which is the more expensive miss.

**On "11 open questions is honesty":** Surfacing OQ-011 (logout requirement) *in Phase 5* is not honesty — it's deferral. Logout is a PRD-required user story. Treating it as an open question at rollout means `COMP-012` (logout control) could be descoped during GA prep. Opus resolved it by making `API-005` a Phase 3 deliverable. Haiku's 11-question list conflates "need stakeholder input" (OQ-005) with "we haven't decided yet" (OQ-011) — the latter is roadmap incompleteness, not governance.

**On "rollback-as-flag-flip is modern":** Flag flip doesn't help when Redis refresh state is corrupted mid-rotation (R-009 scenario) or when the bcrypt migration lands with wrong cost. `BACKUP-PRE` exists because flag-flip presumes data-layer integrity. Haiku's MIG-003 says "rollback:legacyFlag" without specifying *how* to reconcile user records created on the new system — that's an incident waiting to happen.

**On "R-008/R-009 are subsumed":** "Quarterly rotation" as a config item is not the same as a documented revocation playbook with `kid`-based JWKS rollback. Haiku has no row that forces the team to rehearse rotation before GA.

**On observability maturity:** Haiku's `OPS-005` produces *telemetry emission*, not *actionable dashboards and paged alerts*. Phase 6 in Opus isn't "tuning after the fact" — it's the difference between `auth_login_total` being exported and someone actually getting paged when it drops.

### Variant B rebuts Variant A

**On "112 rows = reviewable contracts":** 112 rows is also 112 things that drift out of sync with the implementation. Opus's fine-grained decomposition (`OPS-005.metrics`, `.trace`, `.dash`, `.alert`) is four PRs where one will do. Granularity is optimizing for estimator precision at the cost of coordination cost — and estimators can decompose during sprint planning when they have real signal.

**On "SOC2-VALIDATION gate is auditable signoff":** Haiku's Phase 4 includes `TEST-010` (audit log completeness with SOC2 field assertions) and `COMP-013`/`API-008` admin query. The signoff happens at GA gate (MIG-003 exit). A named "gate task" adds a checkbox; it doesn't change whether controls CC6.1/CC6.6/CC7.2 are met. Auditors care about evidence, which both variants produce.

**On "OQ-011 is deferral":** OQ-011's *placement* in Phase 5 reflects that API-007 and COMP-012 *are* in Phase 3 already — the open question is whether to treat it as explicit PRD-required v1.0 scope or update the TDD. Opus simply asserts one answer without a decision log. When the TDD is the source of truth for compliance, silent resolution is worse than surfaced conflict.

**On rollback rigor:** `ROLLBACK-PROC` and `ROLLBACK-TRIG` as rows don't rehearse anything — they document. Haiku's MIG-002 gate ("rollback:flagPct=0") is executable; Opus's drill task is a deliverable that produces a document. Both end up with the same artifact.

**On frontend hardening rows:** Embedding HttpOnly+SameSite inside `COMP-004` (AuthProvider contract) is the *correct abstraction boundary*. Opus's separate `REFRESH-COOKIE` row implies the AuthProvider could ship without it — which is impossible, because it's a single line in the cookie config. Row separation implies implementation separation that doesn't exist.

**On admin commit vs defer:** Opus commits `ADMIN-UNLOCK` to P1 priority in Phase 6 with effort M. If product decides unlock is v1.1 (a reasonable scope call), Opus now has an unpriced deletion. Haiku's OQ-010 forces the scope decision *before* estimation freezes, which is cheaper.

## Convergence Assessment

### Areas of Strong Agreement (fully converged)

- Both variants agree on all 10 shared assumptions from the diff: complexity class, PG+Redis architecture, bcrypt-12/RS256/2048, TTLs, fail-closed Redis posture, 12-month retention (PRD wins), rollout model, success criteria, external dependencies, and critical-path ordering.
- Both agree R-001 through R-007 are material and need mitigation exactly as specified.
- Both agree the admin audit/unlock gap must be addressed; they disagree on whether to commit or defer.
- Both agree feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` gate the rollout.

### Areas of Partial Convergence

- **Timeline:** Both ship in Q2 2026. The 4-week delta is about risk buffer shape, not calendar target. A reasonable middle would be 14 weeks (6 phases) — accept Haiku's phase bundling but keep Opus's Phase 6 observability/compliance separation.
- **Open questions:** Agreement that OQ-005 (lockout), OQ-003 (reset email sync/async), OQ-008 (retention) must be resolved pre-Phase-1. Disagreement on whether OQ-009/010/011 are roadmap incompleteness (Opus view) or genuine stakeholder questions (Haiku view).
- **Observability:** Agreement that Prometheus+OTel+Grafana+alerts are required. Disagreement on whether Phase 1 baseline (Haiku) suffices or a Phase 6 dedicated tuning phase (Opus) is required.

### Areas of Genuine Persistent Dispute

1. **Row granularity philosophy:** 112 vs 67 rows reflects incompatible views on where decomposition belongs (roadmap vs sprint planning). Neither concedes.
2. **Rollback formalism:** Drill tasks as rows vs rollback as flag-flip configuration — philosophical disagreement about whether rehearsal artifacts belong in the roadmap.
3. **Risk catalog scope:** Whether R-008 (RSA compromise) and R-009 (refresh race) warrant tracked rows or are adequately covered by existing mitigations.
4. **Admin unlock v1.0 commitment:** Scope decision that neither variant can resolve without product input — Opus commits, Haiku defers; both are defensible but they cannot both be right.
5. **Password reset phase positioning:** Phase 4 isolation (backend stability) vs Phase 3 bundling (earlier E2E) — genuine sequencing trade-off.

### Convergence Score Rationale

**0.65** — The variants agree on ~70% of substantive decisions (architecture, primitives, risks R-001-R-007, rollout model, success metrics) but diverge persistently on ~30% (timeline shape, row granularity, rollback formalism, admin commitment, observability phasing). The disagreements are not resolvable by debate alone — they require product/security/compliance stakeholder input on OQ-010, OQ-011, and the risk-buffer-vs-velocity trade-off. Both variants would be defensible roadmaps in different organizational contexts: Opus for compliance-heavy enterprises with mature SRE, Haiku for velocity-focused teams with strong CI/CD hygiene.
