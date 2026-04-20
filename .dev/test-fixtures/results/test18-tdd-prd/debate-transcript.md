---
convergence_score: 0.62
rounds_completed: 2
---

# Adversarial Debate: Opus vs Haiku Roadmap Variants

**Scope:** 12 divergence points across 14-week auth service roadmap. Both variants share timeline, complexity scoring, architectural decisions, and success criteria. Debate focuses on structural philosophy (vertical-slice vs horizontal-layer), risk distribution, and operational artifact scope.

## Round 1: Initial Positions

### Divergence 1 — Milestone Structure (6 vs 5 milestones)

**Variant A (Opus):** Six milestones with a dedicated M5 for Security/Compliance/Observability is the correct shape for a SOC2-adjacent system. Bundling compliance evidence into a general QA sprint (Haiku M4) risks auditors finding that compliance deliverables were treated as a subset of test coverage rather than first-class controls. Separating observability engineering (dashboards, alert rules, trace propagation, log redaction) from test instrumentation is also necessary — they're different disciplines with different review cycles.

**Variant B (Haiku):** Five milestones aligned to lifecycle phases (foundation → contracts → UX → validation → rollout) gives stakeholders a clearer mental model and reduces coordination overhead. SOC2 controls aren't a separate engineering activity — they're validated by the test suite and audit-log implementation, which naturally live in the validation milestone. Six milestones fragments ownership and creates arbitrary hand-offs; a 3-week validation sprint is the industry norm for release gating.

### Divergence 2 — M1 Scope (Scaffolds-only vs FR-complete)

**Variant A (Opus):** M1 as 2 weeks of infrastructure + primitives + scaffolds (no FR business logic) staggers risk and allows the data contract (DM-001) to be frozen against a thin slice before domain logic calcifies around a schema that may need to change after OQ-002. Writing business logic on unfrozen contracts is a well-known anti-pattern.

**Variant B (Haiku):** M1 spanning 3 weeks to include all FR-AUTH-001..005 domain logic means the backend is *done* by week 3. M2 becomes pure contract/gateway work; M3 becomes pure frontend. This enables clean team parallelization and avoids the trap of "scaffolding milestones" that produce no demonstrable user value. Contract freeze happens naturally when FR implementation completes.

### Divergence 3 — Frontend Placement (Interleaved vs Dedicated)

**Variant A (Opus):** Vertical feature slices (LoginPage in M2, AuthProvider refresh in M3, ProfilePage in M4) deliver end-to-end value per milestone. Each milestone can be demo'd. Risk is distributed.

**Variant B (Haiku):** A dedicated frontend milestone (M3) enables parallel team execution: backend team stays on compliance/validation while frontend team builds all pages + AuthProvider + guards + analytics in one coherent design language. Unified UX review happens once, not three times.

### Divergence 4 — Token Subsystem (Dedicated M3 vs Transverse)

**Variant A (Opus):** Tokens are the highest-risk subsystem (R-001 XSS, R-009 refresh replay, R-010 tail latency, AC-009 key rotation). A dedicated 2-week milestone enables focused security review, kid-overlap dry-run, atomic rotation testing, and multi-tab refresh race mitigation.

**Variant B (Haiku):** Treating token management as transverse code (implemented in M1, exposed in M2, consumed in M3) matches how production systems actually work. Token logic isn't a business feature — it's plumbing. Isolating it creates artificial boundaries.

### Divergence 5 — Logout Priority (P0 vs P1)

**Variant A (Opus):** Logout is release-critical. PRD user stories require it. Shipping auth without logout is non-viable.

**Variant B (Haiku):** Logout is P1 because it's not in the enumerated TDD API table. Flagging it as a PRD-gap-fill (with architect ownership for TDD update) is the honest scope accounting. It still ships in M2.

### Divergence 6 — Test Timing (Distributed vs Concentrated)

**Variant A (Opus):** Continuous per-milestone testing (TEST-001/002/004 in M2, TEST-003/005 in M3, TEST-006 in M4, security tests in M5, NFR-PERF in M6) means bugs are caught at the layer they're introduced. A 3-week validation sprint that collects all tests at the end is the classic waterfall trap.

**Variant B (Haiku):** Concentrating TEST-001..010 + NFR-PERF + compliance validation in M4 creates a hard QA gate that cannot be skipped. Distributed testing creates "done enough to move on" fatigue; dedicated hardening sprints produce measurable release confidence.

### Divergence 10 — Operational Artifacts (In-roadmap vs Org-standards)

**Variant A (Opus):** Backup-001, Rollback-001 game-day, Postmortem-001 template, GAExit-001 checklist, LegacyDeprec-001 sunset headers are deliverables *of this project*, not platform-wide standards we can assume exist. Explicit ownership produces audit artifacts.

**Variant B (Haiku):** These belong in platform/SRE standards, not individual service roadmaps. Duplicating them per-service bloats roadmaps and creates inconsistency. COMP-027 (rollback wiring) + OPS-001/002 (runbooks) cover the service-specific surface.

### Divergence 11 — Key Rotation (Pre-GA vs Post-Launch)

**Variant A (Opus):** Pre-GA dry-run in M3 (AC-009) catches kid-resolution bugs before they're production-critical. Rotation is high-blast-radius; validating it *after* GA is too late.

**Variant B (Haiku):** Quarterly rotation is post-launch ops (COMP-028, P1). First rotation happens 3 months after GA; there's time to build muscle memory without blocking release on a ceremony.

## Round 2: Rebuttals

### Variant A rebuts Variant B

**On milestone count:** Haiku's "lifecycle phases" framing conflates *engineering discipline* with *product phases*. SOC2 auditors ask for an evidence trail specific to compliance — not "we tested stuff in M4." Variant B's own AuditSchema-001, AuditRetention-001, and ConsentCapture-001 are real engineered deliverables that deserve their own milestone. Burying them in a validation sprint reduces the perceived investment and weakens the audit narrative.

**On M1 front-loading:** Haiku claims M1 becomes "FR-complete" in 3 weeks, but look at the deliverable list — M1 includes 17 items spanning DM-001/002, COMP-005..013, FR-AUTH-001..005, NFR-SEC-001/002, INF-001/002. That's a single milestone carrying the full data layer, all crypto primitives, the orchestrator facade, the audit writer, *and* all five FR domain flows. If OQ-002 slips or OQ-005 lockout thresholds change, the rework blast radius is the entire 3-week sprint. Opus's 2-week scaffold-then-2-week-FR structure bounds that risk.

**On frontend parallelism:** Variant B's "parallel teams" argument assumes staffing that isn't specified. If the team is small, interleaving is strictly better — no cross-team handoff friction, earlier UX feedback, fewer big-bang integration moments. Vertical slices are also easier to demo to stakeholders at milestone boundaries.

**On distributed tests:** Variant B's own M4 contains TEST-001..010 + NFR-PERF-001/002 + NFR-REL-001 + NFR-COMPLIANCE-002 + TEST-009 + TEST-010. That's 14 test-related deliverables in a 3-week sprint, plus load testing against infra that must be pre-warmed. If M1-M3 ships with weak coverage, M4 becomes a debug sprint, not a validation sprint. Opus's continuous coverage prevents the M4 traffic jam.

**On operational artifacts:** "Org standards exist" is an unverified assumption. The roadmap should produce evidence, not hope. Postmortem-001 template and Backup-001 snapshot automation are cheap to include and make the difference between a clean audit and a scrambling one.

### Variant B rebuts Variant A

**On compliance milestone:** Opus's M5 is 16 deliverables in 2 weeks — MetricsInstr-001, OTelTracing-001, AlertRules-001, StructLog-001, AuditLogger, ConsentCapture-001, PenTest-001, CORSTest-001, SecTestBrute-001, SecTestXSS-001. That's not a focused compliance milestone; it's a kitchen-sink of cross-cutting concerns. Haiku's M4 acknowledges this honestly by grouping all non-functional validation in one sprint rather than pretending "compliance" and "observability" are separable.

**On M1 risk:** Opus's 17-deliverable M1 (scaffolds only) produces *nothing demonstrable* after 2 weeks. Stakeholders see infrastructure bills and no features. Haiku's M1 produces working backend auth that can be exercised via unit tests — tangible progress. The "schema might change" risk is real but is addressed by OQ-002 gating, not by deferring domain logic.

**On token isolation:** Variant A treats tokens as a separate concern, but then AC-009 key rotation needs JwtService from M1, refresh endpoint needs TokenManager from M1, AuthProvider silent refresh needs API-004 from M2 — the dependencies cross milestones anyway. Haiku's "tokens are transverse" framing matches the actual dependency graph.

**On logout:** Calling logout "release-critical P0" when the TDD API table doesn't list it is exactly the kind of scope drift that causes roadmap-reality divergence. Variant B's explicit PRD-gap-fill framing is the correct engineering discipline — acknowledge the gap, require a TDD update, and ship it. Opus ships it without acknowledging the gap, which sets a precedent for future drift.

**On distributed testing:** Opus's "continuous testing" is a fiction — the actual test deliverables clump at milestone endings. TEST-001/002/004 at end of M2, TEST-003/005 at end of M3, etc. That's just *distributed clumping*. A single validation sprint with a dedicated owner produces cleaner release gates than six mini-validation-sprints each owned by a different milestone lead.

**On operational artifacts:** Backup-001 and Postmortem-001 are platform-team standards that should not be re-invented per service. If they don't exist at the org, the fix is to build them *once*, not add them to every roadmap. Scope discipline matters.

**On key rotation:** AC-009 is a P1 operational concern. Forcing it into M3 competes with FR-AUTH-003 (the actual critical path) for attention. Haiku correctly scopes pre-GA validation to *rotation-ready configuration* (NFR-SEC-002) and defers the actual rotation ceremony to post-launch.

## Convergence Assessment

### Areas of strong agreement (high convergence)

1. **Total duration: 14 weeks** — unchallenged in either direction.
2. **Architectural foundations** — RS256 2048-bit, bcrypt cost 12, Redis refresh, AuthService facade, feature-flag rollout. No dispute.
3. **API contract gap-fills** — both variants agree API-005/006/007 must ship; they only disagree on priority framing.
4. **Critical path** — both agree foundation → core auth → tokens → profile/reset → validation → rollout.
5. **Functional scope** — FR-AUTH-001..005 in, MFA/OAuth/RBAC out. Identical.
6. **Risk register core** — R-001..R-006 identical; Opus adds R-007..R-010 as finer-grained calls on shared risks.

### Areas of narrow, addressable disagreement

7. **M1 duration (2w vs 3w)** — resolvable by clarifying whether M1 includes FR logic or only primitives. The 1-week delta is genuine engineering philosophy, not a miscalculation.
8. **Test concentration** — both variants place most tests at M4-or-later; the real disagreement is whether earlier milestones include *any* tests. Resolvable by adding TEST-001/002/004 as M1-M2 exit criteria in Haiku's plan.
9. **Logout priority** — both ship it in M2. P0 vs P1 is a labeling disagreement, not a scope disagreement.
10. **Key rotation timing** — resolvable by adding a *dry-run* in M3 (Opus) while keeping the *operational rotation* post-GA (Haiku). Not mutually exclusive.

### Areas of genuine, unresolved disagreement

11. **Milestone count (6 vs 5)** — philosophical. Opus values audit-artifact separation; Haiku values stakeholder narrative clarity. Neither is objectively wrong; the right answer depends on the audit context and team size.
12. **Operational artifacts in-scope** — genuine disagreement on whether Backup-001, Rollback-001 game-day, Postmortem-001 belong in this roadmap. Opus: yes, for audit completeness. Haiku: no, these are platform standards. This depends on the actual maturity of the org's SRE function, which neither variant has enumerated.
13. **Frontend structure (vertical-slice vs dedicated milestone)** — depends on team composition. Small team: Opus wins. Separate frontend team: Haiku wins.
14. **Convergence metadata** — Haiku claims `convergence_score: 1.0`, Opus claims `none`. This is a meta-process disagreement about whether these variants have been reconciled. They have not — so Haiku's claim is incorrect.

### Synthesis recommendation

A merged roadmap would likely:
- Keep **14 weeks / 6 milestones** (Opus structure) for compliance-clear phasing.
- Adopt **Haiku's M1 duration (3 weeks)** but with **Opus's scope discipline** (primitives + DM freeze + minimal FR scaffolding, not full FR logic) — splitting the difference at 3 weeks of foundation-plus-minimal-domain.
- Preserve **Opus's token milestone (M3)** for focused security review of the highest-risk subsystem.
- Adopt **Haiku's dedicated frontend milestone (M3-or-M4)** if team composition supports parallel execution; otherwise **Opus's interleaving**.
- Include **Opus's operational artifacts** (Backup-001, Rollback-001, Postmortem-001, GAExit-001) as explicit deliverables — they are cheap and produce audit evidence even if redundant with org standards.
- Adopt **Haiku's PRD-gap-fill framing** for API-005/006/007 with explicit architect ownership for TDD updates.
- Schedule **Opus's key rotation dry-run in M3** while deferring **operational rotation (Haiku's COMP-028) to post-GA**.
- Distribute tests across milestones (Opus) but maintain a **final validation gate in M5-or-M6** (Haiku) for NFR-PERF, pen-test, and compliance sign-off.

**Convergence score: 0.62** — high on architecture and scope, medium on timeline structure, low on philosophical framing (vertical-slice vs horizontal-layer) and operational-artifact ownership.
