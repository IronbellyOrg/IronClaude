---
convergence_score: 0.72
rounds_completed: 2
---

# Adversarial Debate: Opus (6-MLS/12w) vs Haiku (4-MLS/8w) Roadmap Variants

## Round 1: Initial Positions

### Variant A (Opus) — Opening Statement

**Position:** Six-milestone, 12-week gated delivery is the correct posture for a security-critical authentication service.

**Key arguments:**

1. **Gating discipline (Divergence #1, #3, #5):** Six milestones create stop-the-line checkpoints at each capability cluster. Rollback blast radius is bounded to one milestone's deliverables. For a service handling credentials, tokens, and reset flows, the cost of a bad merge propagating downstream is catastrophic — an extra four weeks buys precisely-scoped rollback boundaries.

2. **Foundation isolation (M1 pure foundation):** Shipping data-layer + secrets + library pinning without any cryptographic code lets security review sign off on the persistence contract independently. When JWT/bcrypt land in M2, the schema is already frozen — no feedback loops.

3. **Crypto milestone isolation (M2):** Locking `TokenManager.issue/refresh/revoke*` contracts before any endpoint consumes them means every downstream flow codes against a stable interface. Haiku's approach couples TokenManager to M2's endpoint work, creating contract churn under endpoint pressure.

4. **Security auditability:** Explicit SEC-001 through SEC-006 IDs map 1:1 to audit/compliance review items. Haiku's COMP-011/012 conflation makes security traceability harder.

5. **Reset isolation (M5):** P1 reset flow should not ship atomically with P0 refresh rotation. If reset slips, refresh ships on time. Haiku's M3 bundle has no such escape hatch.

6. **OI resolution as gate:** OI-1 (reset email mode) and OI-7 (provider) are hard pre-requisites, not in-flight decisions. Making them blockers forces product/ops decisions before code commits.

### Variant B (Haiku) — Opening Statement

**Position:** Four-milestone, 8-week delivery with broader milestone scope is the correct posture — gating density past a threshold is ceremony, not safety.

**Key arguments:**

1. **Calendar velocity matters (Divergence #1):** 8 weeks vs 12 weeks is not a rounding error — it's a 33% faster time-to-production. The business impact of unblocking authenticated surfaces compounds weekly. Opus pays a real cost in delayed product value for marginal gating benefit.

2. **Foundation + primitives together (M1):** JWT and bcrypt are self-contained libraries with stable contracts — `jsonwebtoken` and `bcrypt` don't need an isolated milestone. Bundling them with schema+repositories lets M1 exit with a genuinely complete crypto foundation, not a half-delivered persistence layer.

3. **TokenManager with endpoints (M2):** Coupling TokenManager to issuance endpoints is a feature, not a bug — it validates the interface against real consumption immediately. Isolated contracts without consumers often ship with latent mis-design that only surfaces at integration.

4. **Refresh + Reset atomic (M3):** Both flows share the revoke-all-for-user primitive (SEC-006 depends on SEC-003). Shipping them together ensures the revocation contract is exercised by two consumers before freeze, catching design issues Opus's serial approach would only discover in M5.

5. **Explicit GAP ownership (Divergence #11):** Opus's "risk-register entry" for GAP-1/2/3 is exactly how handoffs get lost. Creating M4 deliverables with owners and v1.1 targets is accountability, not ceremony.

6. **OI as in-flight decision:** Product/ops decisions rarely land cleanly before sprint kickoff in practice. Haiku accepts the realistic cadence — decisions made inside M3/M4 with documented rework tolerance.

## Round 2: Rebuttals

### Variant A (Opus) — Rebuttal to Haiku

**On calendar velocity:** "33% faster" assumes the 8-week plan ships. Haiku flags three consecutive HIGH-risk milestones (M2, M3, M4). When one slips — and refresh replay detection under concurrent load is a genuine race-condition risk — the recovery is harder because more scope is entangled per milestone. Opus's 12 weeks is a *reliable* 12, not an optimistic 8 that degrades to 10.

**On primitives+foundation bundling:** JWT is self-contained *only if* RSA key rotation, secrets manager wiring, and kid-based verification work on the first try. OPS-006 (90-day rotation runbook) sitting in M2 is not incidental — it belongs with the service that consumes it. Haiku putting JwtService in M1 forces either (a) writing crypto without the rotation policy, or (b) pulling the rotation policy forward into foundation work, blurring the "no business logic in M1" principle.

**On refresh+reset coupling:** The shared revoke-all primitive is exactly why they should NOT ship together. If the revocation contract has a defect, Haiku's M3 ships two broken flows atomically. Opus's approach exercises revoke-all once in M4 (refresh replay), validates it, then consumes it in M5 (reset) with proven semantics.

**On GAP ownership:** Creating M4 "planning deliverables" that produce v1.1 plans is bureaucratic theater — the plan itself has no functional output in v1. Opus's risk-register entries (R4, R5, R12) are equally visible and don't consume sprint capacity producing documents for future milestones.

**On OI timing:** "Decisions rarely land cleanly" is a process failure to fix, not accept. Haiku's "accept rework risk" stance is exactly how auth services ship with email-provider-specific assumptions baked into EmailService that then require refactoring.

### Variant B (Haiku) — Rebuttal to Opus

**On reliable 12 vs optimistic 8:** Opus's 12 weeks is optimistic *too* — 6 handoff boundaries means 6 chances for coordination friction, standup overhead, and review-cycle delay. The "rollback precision" advantage only matters if rollbacks are frequent. For a greenfield auth service where every milestone is gated by tests + integration review anyway, rollback-per-milestone vs rollback-per-capability-cluster is mostly theoretical.

**On crypto isolation:** OPS-006 (key rotation runbook) is a P1 document, explicitly marked as such in Opus's own plan. It doesn't block M2 exit. Haiku's approach — primitives in M1, TokenManager in M2 — is the standard dependency ordering: low-level libs → orchestrators. Opus's "isolate crypto in its own milestone" is the anomaly requiring justification.

**On refresh+reset decoupling:** Opus claims M4 validates revoke-all "once" before M5 consumes it — but M4 validates revoke-all from the *replay detection* path, which is a different trigger than the *post-reset* path. Both paths need validation regardless. Haiku's M3 forces both consumers to validate the same primitive in the same milestone, eliminating the gap between "works for replay" and "works for reset."

**On GAP documentation theater:** A risk-register entry that says "mitigation: handoff to v1.1" with no owner and no deadline is *exactly* the theater Opus accuses Haiku of. Haiku assigns owners (Security, Architect, Backend) to specific deliverables. The "bureaucratic cost" of writing a one-page plan is negligible compared to the cost of v1.1 launching without clear scope.

**On OI timing rigidity:** Opus gates M5 on OI-7 resolution. If email provider selection slips by one week, the entire M5 milestone (10 deliverables, 2 weeks) sits idle waiting. Haiku's approach — provider adapter abstracted, decision in-flight — allows M3 to proceed with a temporary SMTP bridge while the provider contract finalizes. That's resilience, not sloppiness.

**On security auditability:** SEC-xxx vs COMP-xxx IDs are cosmetic. Both variants trace deliverables to spec requirements. Auditors care about the requirement→test→artifact chain, which both plans provide. The claim that Opus is "more auditable" is unsupported.

## Convergence Assessment

**Convergence score: 0.72**

### Areas of Strong Agreement (10 shared assumptions hold)

Both variants agree on every *technical* decision: RS256 JWT, bcrypt cost 12, SHA-256-hashed rotated refresh tokens, httpOnly cookies, feature-flag rollout, layered architecture, v2 exclusions (OAuth/MFA/RBAC), data model contracts, and the criticality of OI-1/OI-2/OI-7 as blocking issues. The *what to build* is converged.

### Areas of Partial Agreement

- **Test coverage importance:** Both agree coverage matters; disagree on enumeration granularity (TEST-M*-xxx per deliverable vs consolidated suites). Resolvable by team preference — neither is objectively wrong.
- **Risk severity weighting:** Both flag M2+ as HIGH risk; Opus pinpoints two milestones, Haiku flags three. Same underlying risk surface, different attention distribution.
- **Rate limiter + password policy:** Both ship the same controls; disagree only on milestone placement and ID scheme.

### Remaining Disputes (weighted by impact)

1. **Timeline (12w vs 8w) — UNRESOLVED.** This is a genuine stakeholder decision. Business context required: is time-to-production or rollback precision the binding constraint? Neither variant's arguments definitively win without business input.

2. **Refresh + Reset coupling — LEANS OPUS.** The argument that P1 reset should not block P0 refresh is structurally strong. Haiku's "shared primitive" rebuttal has merit but doesn't overcome priority-based isolation.

3. **Crypto milestone isolation — LEANS HAIKU.** Opus's case for M2-only-crypto is weaker than it appears; primitives-in-foundation is the conventional dependency pattern. OPS-006 can be P1-documented without gating M1 exit.

4. **GAP formalization — LEANS HAIKU.** Explicit owned deliverables with v1.1 handoff targets are more robust than risk-register discipline. The "ceremony" cost is low; the forget-risk cost of risk-register-only is high.

5. **OI resolution timing — LEANS OPUS for OI-7, LEANS HAIKU for OI-2.** Email provider (OI-7) genuinely blocks concrete integration work; refresh cap (OI-2) is a policy decision that tolerates in-flight resolution.

6. **Security ID scheme — NOT A REAL DISPUTE.** SEC-xxx vs COMP-xxx is cosmetic.

### Recommended Synthesis

A hybrid plan would likely outperform either variant: **5 milestones, 10 weeks**, using Opus's reset isolation (separate M5) and OI-7 gating, but Haiku's foundation+primitives bundling (merged M1) and explicit GAP ownership deliverables. Neither variant is wholly correct; the debate exposes genuine trade-offs requiring stakeholder arbitration on the 8w-vs-12w axis.
