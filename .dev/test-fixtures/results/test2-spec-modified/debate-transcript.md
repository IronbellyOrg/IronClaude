---
convergence_score: 0.64
rounds_completed: 2
---

# Structured Adversarial Debate: Roadmap Variant A (Opus) vs. Variant B (Haiku)

**Debate Scope**: 6 primary divergence points selected for dispute — those rated as requiring debate to resolve in the diff analysis: (1) emergency rotation procedure scope, (2) anomaly alerting scope, (3) latency profiling timing, (4) phase structure trade-off, (5) OQ-8 implementation prescription, and (6) account lockout default. Four secondary divergences (staffing model, release gates format, deferred items tracking, Phase 0 duration) are addressed as subordinate claims.

---

## Round 1: Initial Positions

---

### Variant A (Opus) — Opening Statement

**On emergency key rotation procedure (Divergence 4)**

We explicitly defer the emergency key rotation runbook to v1.1, and we believe this is the correct risk-acceptance posture for a v1.0 delivery. RISK-1 is addressed through its two primary mitigations: private key isolation in a secrets manager and 90-day automated rotation. An emergency rotation procedure is an operational capability — it requires coordination with incident response process owners, communication runbooks, and decisions about blast radius (e.g., does emergency rotation invalidate all active sessions?). These are organizational decisions, not engineering decisions. Shipping v1.0 without a documented emergency runbook that no one has reviewed or rehearsed is no safer than deferring it cleanly with an explicit gap acknowledgment. The residual gap is real; we document it as such. Haiku's Phase 4 task "add emergency rotation runbook" is a checkbox, not a procedure.

**On anomaly alerting for rapid token rotation (Divergence 5)**

We agree that observability into refresh replay events is valuable. We disagree that it belongs in v1.0. The reason is infrastructure dependency: anomaly alerting requires a functioning APM stack, defined baselines, and alert routing before signals are actionable. On day 1 of a new auth service, no baseline exists for "normal" refresh rotation frequency. An alert without a baseline is noise. Haiku's Phase 4 inclusion of "anomaly signals for rapid repeated refresh attempts" presupposes an observability infrastructure and baseline that v1.0 does not yet establish. We prefer to ship the replay detection logic (SC-8) — which is the blocking mitigation — and let v1.1 add alerting once production baseline data exists.

**On latency profiling timing (Divergence 8)**

This is the divergence where we are most confident we are correct. We recommend a full-path bcrypt benchmark in Phase 1.1, not Phase 4. The reasoning is simple: if the 200ms p95 target (SC-1) is structurally infeasible given bcrypt cost factor 12 (~250ms for the hash alone), discovering this in Phase 4 means 3–4 weeks of implementation work may need to be partially undone — cost factor adjustment, architecture changes, or SLO renegotiation. All of these are cheaper before service layer composition begins. Haiku's Phase 4 placement "keeps Phase 1 focused on correctness," but correctness of what? If the latency constraint is violated, the implementation direction is wrong. Surfacing this risk at Phase 1.1 costs one benchmark run. Deferring it to Phase 4 costs potentially weeks of rework.

**On phase structure (Divergence 1)**

Four phases with 8 milestones is not simpler for the sake of simplicity — it reflects the realistic team context for a medium-complexity service (complexity score 0.62). Seven phases may benefit a team with dedicated QA and security engineers who need structural separation to avoid competing for attention. But our staffing model (1 backend engineer, part-time security and DevOps) does not produce enough concurrent work streams to justify 7 distinct phase boundaries. Each phase boundary is a coordination cost. Haiku's 7-phase structure imposes overhead that exceeds its benefit for the team size the spec implies. The NFR and security validation co-location in our Phase 3 is not a risk — it is a reflection of the fact that on a small team, one engineer does both.

**On OQ-8 concurrency prescription (Divergence 9)**

Haiku prescribes "transactional rotation logic" as the default implementation for concurrent refresh rotation. We believe this is correct technically but wrong procedurally. OQ-8 is an open question precisely because the policy decision — idempotency window vs. accepted false-positive invalidation — has not been made by its decision owner. Transactional rotation is one implementation approach that follows from one policy choice. If the OQ-8 decision owner chooses an idempotency window instead, Haiku's prescribed implementation approach is incorrect. We document accepted behavior, defer to the decision owner, and implement after the policy is confirmed. This is not indecisiveness; it is correct sequencing.

**On account lockout default (Divergence 7)**

We leave OQ-3 open by design. The spec does not resolve account lockout scope, and the implementation implications differ meaningfully: if v1.0, progressive lockout adds work to Phase 2.1; if v1.1, we document the gap. Haiku pre-decides deferral. Pre-deciding a deferral is itself a scope decision — one that should be made by the team, not baked into the roadmap. Our conditional framing gives stakeholders the option to include it without requiring a roadmap revision.

---

### Variant B (Haiku) — Opening Statement

**On emergency key rotation procedure (Divergence 4)**

Variant A's argument that the emergency runbook is an "organizational decision" rather than an engineering one is a category error. The runbook's operational questions — does rotation invalidate sessions? what is the blast radius? — are exactly the questions that must be answered by Phase 4, because they directly affect the token lifecycle architecture we are building. If the answer is "session invalidation on emergency rotation," that is a `TokenManager` capability we must build. If the answer is "no session invalidation," that is a separate implementation choice. Deferring the runbook to v1.1 means deferring these architectural decisions, which means v1.0 may ship with an incomplete implementation of RISK-1 mitigation. RISK-1's severity is "total authentication bypass via forged tokens." Accepting an explicit gap in the primary mitigation chain is not a clean risk posture — it is a gap with consequences that may surface before v1.1 ships.

**On anomaly alerting (Divergence 5)**

Variant A argues that anomaly alerting requires a baseline before it is actionable. We agree that baselines develop over time. We disagree that this means alerting should not be wired in v1.0. A threshold-based alert ("more than N refresh rotation failures in M seconds per user") does not require a production baseline — it requires a policy decision about what constitutes anomalous behavior. That policy decision is available in Phase 0 (when we resolve OQ-8 and replay behavior). Shipping SC-8 without any observability path means that replay attacks may succeed silently: the revocation logic triggers, but no one is alerted, no one investigates, and the attack surface is only discovered in post-mortem. The operational gap is not "noise vs. signal" — it is "visibility vs. blindness."

**On latency profiling timing (Divergence 8)**

We partially concede Variant A's point here. A bcrypt benchmark in Phase 1.1 is not harmful and does provide earlier signal. Our Phase 4 placement reflects a preference for keeping Phase 1 focused on cryptographic correctness without introducing performance concerns that may distract from the unit test suite. However, we acknowledge that if the team has any uncertainty about whether 200ms p95 is achievable given the bcrypt budget, Variant A's Phase 1 benchmark recommendation is strictly lower risk. We would accept a hybrid: run an isolated benchmark in Phase 1.1 as a fast signal, then validate the full code path in Phase 4 under load.

**On phase structure (Divergence 1)**

Variant A argues that 7 phases impose coordination overhead beyond the team size. This misreads what phase boundaries provide. Phase boundaries are not just coordination points — they are scope control mechanisms. When NFR validation and security hardening share a phase (Variant A's Phase 3), the team faces an implicit prioritization question: if time is tight, do we cut performance validation or security review? Separating them into Phase 4 (NFR) and Phase 5 (security validation and release readiness) makes the scope cut explicit and deliberate. The benefit is not team coordination — it is scope legibility under pressure. A roadmap that is easier to cut correctly is more valuable than one that is easier to read on paper.

Furthermore, Variant A's staffing model (3 roles) undersells the coordination required. The spec identifies 8 open questions, 3 of which block implementation and require external stakeholder decisions. Managing those decisions requires a product/architecture owner role that Variant A does not name. Our 5-role model is not padding — it reflects the actual coordination required to close OQ-1, OQ-6, OQ-7 before Phase 1 begins.

**On OQ-8 concurrency prescription (Divergence 9)**

Variant A is correct that transactional rotation is one of two policy outcomes from OQ-8. But Variant A's "document accepted behavior" framing is passive — it produces a roadmap that cannot begin Phase 2 implementation until the OQ-8 decision arrives, with no fallback. We prescribe transactional rotation as the default with explicit acknowledgment that the idempotency window alternative exists. This is not circumventing the decision owner — it is providing a technically sound starting point that can be adjusted when the policy decision is received. Shipping without transactional rotation exposes legitimate users to false-positive session invalidation on concurrent refresh operations, which is a user-facing correctness bug, not just a policy question.

**On account lockout default (Divergence 7)**

Variant A leaves OQ-3 open "to give stakeholders the option." But an open OQ with no default assumption creates ambiguity that propagates into Phase 2 planning. If the team begins Phase 2 implementation without knowing whether progressive lockout is in scope, they may build login flow logic that is difficult to extend later, or they may delay Phase 2 start waiting for OQ-3 resolution. Our explicit deferral is not a scope decision we are making unilaterally — it is documentation of the most likely outcome given the spec's framing of OQ-3, allowing Phase 2 to begin with a clear, minimal-scope assumption.

---

## Round 2: Rebuttals

---

### Variant A (Opus) — Rebuttal

**On emergency key rotation (counter to Haiku's Round 1)**

Haiku argues that the runbook's policy questions — "does rotation invalidate sessions?" — are architectural decisions that affect `TokenManager`. This is partially correct. But Haiku then includes "add emergency rotation runbook" as a Phase 4 task, *after* `TokenManager` is already implemented in Phase 1.3. If the runbook's policy questions genuinely drive `TokenManager` design, Haiku's own phase placement is wrong — the runbook should precede Phase 1, not follow it. Haiku cannot simultaneously argue that the runbook is architecturally necessary and schedule it in Phase 4. This internal inconsistency reveals that Haiku's Phase 4 runbook task is documentation, not architecture — which is precisely our characterization of it.

**On anomaly alerting (counter to Haiku's Round 1)**

Haiku proposes threshold-based alerting ("N failures in M seconds per user") without acknowledging where N and M come from. For a new service with no traffic history, setting N and M is a policy guess. Too tight and the alert fires on legitimate concurrent mobile clients. Too loose and it misses real attacks. Haiku's response assumes a policy decision about anomalous behavior is available in Phase 0. The spec does not surface this decision anywhere in the 8 open questions. We are not arguing against alerting — we are arguing that shipping alerting without calibrated thresholds in v1.0 creates operational noise that degrades confidence in the alert channel. Ship SC-8. Collect baselines. Alert in v1.1.

**On OQ-8 prescription (counter to Haiku's Round 1)**

Haiku argues that transactional rotation is a technically sound default that can be adjusted when the policy decision arrives. We agree it is technically sound. Our objection is not to the implementation — it is to prescribing it without the policy decision. If the OQ-8 decision owner chooses an idempotency window with grace period, the transactional rotation implementation may need to be unwound. "Adjust when the policy arrives" is the same risk we are trying to avoid by flagging the OQ as blocking. Haiku's approach front-loads implementation that may be partially wrong, whereas our approach front-loads the policy question and implements once. For a medium-complexity service, we prefer one implementation cycle over two.

**On Haiku's partial concession on latency profiling**

We accept Haiku's hybrid framing as a reasonable convergence: isolated benchmark in Phase 1.1 for early signal, full k6 code-path validation in Phase 4. This resolves the divergence practically.

**On phase structure and staffing (counter to Haiku's Round 1)**

Haiku argues that our 3-role model undersells coordination requirements. We acknowledge that a product/architecture owner role is implicit in OQ resolution — but that role is an organizational reality, not a staffing addition the roadmap creates. Naming it explicitly (Haiku's 5-role model) is useful documentation; it does not change the implementation work. The coordination cost of phase boundaries, however, is real engineering overhead: each phase boundary implies a milestone review, gate criteria evaluation, and transition decision. Seven gates on a 21–36 day project means a gate every 3–5 days. At that frequency, milestone reviews become the work, not the implementation. Haiku's scope legibility argument is valid in theory; it is expensive in practice for a small team.

**On OQ-3 account lockout default (counter to Haiku's Round 1)**

Haiku argues that our open framing delays Phase 2 start. This is a false dilemma. We explicitly state that OQ-3 is resolved in Phase 0 — the phase whose entire purpose is decision closure. If OQ-3 resolves to deferral (most likely, per spec framing), Phase 2 begins with IP rate limiting in scope and lockout out of scope. If it resolves to v1.0 inclusion, Phase 2 scope expands accordingly. Both outcomes are handled. Haiku's pre-decision removes stakeholder optionality without offering a faster Phase 2 start, because Phase 2 does not begin until Phase 0 closes regardless.

---

### Variant B (Haiku) — Rebuttal

**On emergency key rotation (counter to Opus's Round 2)**

Variant A's observation that Haiku schedules the runbook in Phase 4 after `TokenManager` is implemented in Phase 1 is a legitimate internal consistency challenge. We accept it partially. The correction is not to remove the runbook — it is to clarify that the runbook's *policy questions* (session invalidation scope, blast radius) should be surfaced in Phase 0, with the runbook document itself produced in Phase 4 after operational capabilities are proven. This does not invalidate the argument for v1.0 inclusion; it refines the placement. The substantive claim stands: RISK-1 severity warrants a complete mitigation chain in v1.0, not a partial one.

**On anomaly alerting (counter to Opus's Round 2)**

Variant A argues that threshold calibration requires production baseline data and that miscalibrated thresholds produce noise. This is accurate for sophisticated statistical anomaly detection. We are not proposing statistical anomaly detection. A hard threshold — "revoke-all-for-user triggered more than 3 times in 60 seconds for the same user ID" — is a deterministic signal that does not require baseline calibration. It is a direct proxy for the replay attack scenario the system is designed to detect. The question of whether N=3 or N=5 is a policy question that can be decided in Phase 0 alongside OQ-8. Variant A's "collect baselines first" argument applies to percentile-based anomaly detection, not to threshold-based event counting on a system where the triggering event (revoke-all) is itself a security response.

**On Variant A's acceptance of latency profiling hybrid**

We confirm acceptance of the hybrid framing as convergence on this point.

**On phase structure (counter to Opus's Round 2)**

Variant A argues that 7 milestone gates every 3–5 days creates overhead. This mischaracterizes what milestone gates require in practice. Milestones are not necessarily formal reviews — they are defined exit criteria that indicate when the next phase can begin. A small team can evaluate "has M1 been achieved?" in a 15-minute standup. The value is not the ceremony; it is the explicit answer to "are we ready to proceed?" under time pressure. A 4-phase roadmap where Phase 3 co-locates performance and security validation does not answer this question cleanly when time is tight. It produces a judgment call: ship with SC-1 unproven, or delay security review. Haiku's structure makes this trade-off explicit. Variant A's structure leaves it implicit.

**On OQ-3 account lockout (counter to Opus's Round 2)**

Variant A argues that OQ-3 resolution in Phase 0 handles both outcomes. We agree this is correct as stated. Our objection to Variant A's framing is not that it fails to handle both outcomes — it is that leaving OQ-3 open without a default assumption in the roadmap document communicates ambiguity to readers who use the roadmap for Phase 2 planning. If a team member picks up the roadmap to estimate Phase 2 scope, Variant A's conditional ("if OQ-3 resolves as v1.0, add progressive lockout") requires them to know the OQ-3 resolution before they can size Phase 2. Haiku's explicit deferral communicates a clear planning assumption. This is a documentation quality difference, not an architectural one — but documentation quality matters for team coordination.

---

## Convergence Assessment

### Areas of Agreement Reached

1. **Latency profiling timing**: Both variants converge on a hybrid approach — isolated bcrypt benchmark in Phase 1.1 for early signal, full-path k6 validation in Phase 4 under load. This resolves Divergence 8.

2. **Core security architecture**: Fully shared. RS256, bcrypt cost factor 12, secrets manager integration, refresh token hashing, replay detection, and httpOnly cookie delivery are not in dispute.

3. **Implementation dependency order**: Fully shared. The component build sequence is identical in both variants.

4. **Emergency rotation policy questions belong in Phase 0**: Haiku concedes that the runbook's policy questions (blast radius, session invalidation scope) should be surfaced in Phase 0, not deferred entirely to Phase 4. Variant A acknowledges the runbook is a legitimate gap even if its scope of inclusion is disputed.

5. **OQ-8 requires a policy decision before implementation**: Variant A's framing is accepted as procedurally correct. Haiku's transactional rotation is acknowledged as technically sound. Both agree implementation should follow policy; dispute is about whether to start with a technically-sound default or hold until the decision arrives.

---

### Remaining Disputes

**Dispute 1: Emergency rotation procedure — v1.0 vs. v1.1 scope**

Haiku's position (v1.0 deliverable) is more defensible from a security posture standpoint, given RISK-1's total-auth-bypass severity. Variant A's internal consistency critique — that the runbook cannot be architecturally necessary and scheduled post-implementation — is valid and forces Haiku to refine its framing (policy in Phase 0, runbook document in Phase 4). The resolution the diff analysis suggests (this is a legitimate security posture difference requiring stakeholder alignment) remains accurate. Neither variant is wrong; the decision depends on whether the delivery team treats "tested and rehearsed rotation capability" as a launch requirement or a v1.1 operational hardening item.

**Dispute 2: Anomaly alerting — threshold calibration argument**

Haiku's Round 2 rebuttal (deterministic threshold counting does not require baseline calibration) substantially weakens Variant A's argument. A hard-coded event count threshold on the revoke-all event is technically implementable without production baselines. Variant A does not successfully refute this. Haiku's position is stronger on the technical merits; Variant A's position is stronger on the scope discipline merits (v1.0 should ship SC-8; alerting is an operational enhancement).

**Dispute 3: Phase structure — 4 phases vs. 7 phases**

Neither variant prevails definitively. Variant A's coordination overhead argument is valid for a single backend engineer context. Haiku's scope legibility argument is valid for any team facing time pressure in Phase 3. The correct structure depends on actual team composition and organizational gate-review culture, neither of which is determinable from the spec. Unresolved.

**Dispute 4: OQ-3 documentation framing**

Haiku correctly identifies this as a documentation quality difference, not an architectural one. Both approaches handle both outcomes correctly. Haiku's explicit deferral is better for readers using the roadmap for Phase 2 planning; Variant A's conditional is better for preserving stakeholder option value. Unresolved but low stakes.

---

### Summary Judgment

The two variants share architectural DNA — identical security model, identical component order, identical acceptance criteria. The disputes are concentrated in three areas: **v1.0 security completeness** (emergency rotation, anomaly alerting), **risk surfacing timing** (latency profiling — substantially resolved), and **structural philosophy** (phase granularity, OQ prescription vs. deferral).

Haiku is operationally stronger on security completeness and post-launch governance. Variant A is stronger on scope discipline, early risk surfacing, and documentation structure for backlog handoff. A synthesized roadmap would adopt:
- Haiku's emergency rotation as v1.0 scope (with policy questions in Phase 0)
- Haiku's anomaly alerting threshold approach for RISK-2
- Variant A's Phase 1.1 benchmark (retained in Haiku's hybrid)
- Variant A's consolidated deferred items list format
- Variant A's integration point table format
- Haiku's release gates consolidation and "implemented, not documented" qualifier
- Haiku's explicit post-launch review cycle (Phase 6)
- Team-size-appropriate phase count (4 for small teams, 7 for larger ones with dedicated QA/security)

**Convergence score: 0.64** — strong agreement on fundamentals and architecture; meaningful unresolved dispute on v1.0 security completeness scope and phase structure philosophy.
