---
convergence_score: 0.72
rounds_completed: 2
---

# Adversarial Debate: Opus Roadmap vs. Haiku Roadmap

## Round 1: Initial Positions

### D-01 / D-02 / D-03: Phase 0 and Timeline

**Variant A (Opus):**
Phase 0 is ceremony. The six open questions (OQ-001 through OQ-006) are answerable in flight — OQ-001 is explicitly deferred, OQ-002 and OQ-005 have obvious defaults (20 roles, 5 req/min), and OQ-003/OQ-006 don't block until Weeks 3 and 6 respectively. Adding 3–5 days of ADR writing before a single line of code ships is a planning trap. Our 7–9 week timeline reflects that a competent auth-team can resolve interface questions while building the infrastructure they inform. Architecture freezes are valuable for distributed teams with unclear ownership — not for a focused auth squad.

**Variant B (Haiku):**
Phase 0 is insurance, not ceremony. OQ-004 (RSA key rotation) and OQ-006 (migration schema mapping) have downstream consequences that compound if resolved ad hoc. An ADR takes hours, not days, but the *contract freeze* — locking the API shape, error catalog, and rate-limit policy before implementation — prevents the integration churn that turns a 2-week phase into a 3-week phase. The 9–11 week estimate is honest; Opus's 7–9 weeks will quietly become 9–10 when Phase 2 slips because the error format changed mid-sprint. We pay the 3–5 days upfront or pay them scattered across every phase as rework.

---

### D-04: `UserRepo` Phase Assignment

**Variant A (Opus):**
`UserRepo` belongs in Phase 1 because it is infrastructure, not domain logic. It is a thin CRUD layer over pg-pool. Placing it in Phase 1 means we can write integration tests against real PostgreSQL for `UserProfile` persistence *before* `AuthService` exists. This validates the data model early. Deferring it to Phase 2 means Phase 1 delivers security primitives that can only be unit-tested in isolation — you cannot verify that `PasswordHasher` output actually persists correctly until Phase 2.

**Variant B (Haiku):**
`UserRepo` is a domain service that expresses business rules — email uniqueness, lowercase normalization, last-login tracking, audit logging. It belongs with `AuthService` in Phase 2 because its interface is shaped by the auth flows that consume it, not by the database schema alone. Implementing it in Phase 1 risks building a generic CRUD layer that needs reshaping once `AuthService` integration reveals the actual access patterns. Phase 1 should validate primitives in isolation; Phase 2 validates them in composition.

---

### D-05: Rate Limiting Phase Assignment

**Variant A (Opus):**
Rate limiting is a security control, and security controls belong as close to implementation as possible. Implementing rate-limit middleware in Phase 2 alongside the endpoints means every integration test exercises the full request pipeline — including throttling. Deferring gateway-level rate limiting to Phase 4 means two full phases of testing occur without realistic abuse protection, and any rate-limit integration bugs surface late.

**Variant B (Haiku):**
There are two distinct layers: application-level lockout (5 attempts / 15 minutes) and API Gateway rate limiting (10 req/min per IP). Application lockout is Phase 2 — it's business logic. Gateway rate limiting is operational infrastructure that depends on the deployment topology, which isn't finalized until Phase 4. Mixing them conflates concerns. Phase 2 integration tests should validate auth behavior, not gateway configuration.

---

### D-07 / D-08: Security Review Role and Environment Gates

**Variant A (Opus):**
A dedicated security review role for a 4-phase auth project with 2–3 backend engineers is organizational overhead. The backend engineers *are* the security engineers for this scope — they implement bcrypt, JWT, and token revocation. Security review happens through code review and the test suite, not a separate role. Similarly, environment readiness is implicit: if PostgreSQL isn't up, tests fail. The failing test *is* the gate.

**Variant B (Haiku):**
Auth is the one domain where "the backend engineers handle security" is insufficient. RS256 key lifecycle, token storage model, and XSS mitigation require adversarial review by someone not implementing the feature. The spec itself identifies three high/medium risks. A named security reviewer costs zero engineering time — it's a review assignment, not a headcount. Environment readiness gates are equally cheap: a checklist item "DB schema deployed, Redis available, key material loading tested" catches the 2-day delay where a developer is blocked waiting for Redis provisioning and doesn't flag it because it's "not their task."

---

### D-09: Risk Treatment Scope

**Variant A (Opus):**
We identified R-004 (RSA key compromise), R-005 (Redis SPOF), and R-006 (SendGrid outage) because they are real operational risks the spec doesn't cover. A roadmap that only parrots spec risks is a transcription, not architecture. R-005 alone — Redis as a single point of failure for all refresh tokens — could take down every authenticated session. Flagging it now means the team can plan Sentinel/Cluster evaluation during Phase 1 infrastructure work.

**Variant B (Haiku):**
Breadth without depth is noise. We cover R-001, R-002, and R-003 with explicit "Roadmap controls" mapping each risk to specific phase deliverables and contingency actions. Opus lists R-004/R-005/R-006 but doesn't integrate them into the phase plan with the same rigor. A risk without a phase-mapped mitigation is a worry, not a control. We'd rather have three risks with full traceability than six risks with partial coverage.

---

### D-10 / D-06 / D-11 / D-12: Structural Differences

**Variant A (Opus):**
Bundling observability with rollout in Phase 4 is efficient — the same engineers configure Prometheus, deploy to staging, and monitor alpha. Splitting them adds a week and a handoff. Inline wiring tables per phase are actionable: a developer opening Phase 2 sees exactly what to wire. A cross-cutting catalog is an architect's artifact that no one reads during implementation. Explicit sequencing constraints are unnecessary when phases are well-ordered — Phase 3 obviously can't start frontend token work before `JwtService` exists.

**Variant B (Haiku):**
Bundling observability with rollout means observability is validated *during* rollout, not *before*. If your Prometheus config is wrong, you discover it when alpha traffic is already flowing — and you're flying blind. One week of separated observability validation is cheap insurance. The cross-cutting integration catalog (Section 3) exists because wiring bugs are the #1 source of auth integration failures — developers need both the per-phase view *and* the system-topology view. Sequencing constraints (Section 8) exist because "obvious" dependencies are the ones teams skip. "Do not start frontend token orchestration before `JwtService` is stable" is obvious in retrospect and violated in practice.

---

## Round 2: Rebuttals

### Variant A rebuts Variant B:

1. **Phase 0 rework claim is speculative.** Haiku asserts Opus's timeline will slip due to mid-sprint interface changes, but provides no evidence. The API contract (`/v1/auth/*` with six endpoints) is defined in the spec. Error format (`AC-009`) is defined in the spec. Rate limits are defined or have obvious defaults. There is nothing to "freeze" that isn't already frozen by the spec itself. Phase 0 re-freezes what's already frozen.

2. **`UserRepo` reshaping risk is overstated.** `UserRepo` is CRUD. Its interface is `create(profile)`, `findByEmail(email)`, `update(id, fields)`. These methods don't change based on auth flow design. The access patterns are table stakes for any user store. Haiku's concern applies to complex domain repositories, not a user table wrapper.

3. **Security review role is a process artifact.** Haiku says "zero engineering time" but ignores coordination cost. A security reviewer who isn't writing the code needs context transfer, review cycles, and scheduling. For a team of 2–3, the backend engineers reviewing each other's PRs with a security checklist achieves the same outcome with less overhead.

4. **Haiku's risk traceability advantage is real but narrow.** We concede the "Roadmap controls" mapping is superior for the three spec risks. But ignoring R-004/R-005/R-006 entirely is a gap. The merged roadmap should adopt Haiku's traceability format *and* include our additional risks.

### Variant B rebuts Variant A:

1. **"The spec defines the contract" is wishful.** The spec defines *what* — six endpoints, JWT, bcrypt. It does not define *how* — error codes, pagination of roles arrays, reset token format, audit log schema, or the exact Redis key structure. These are the decisions that cause mid-phase churn if not locked. Phase 0 isn't re-freezing the spec; it's resolving the implementation-level decisions the spec deliberately leaves open.

2. **`UserRepo` as "just CRUD" ignores the business rules.** Email uniqueness enforcement, lowercase normalization, audit log co-writes, last-login timestamp updates — these are all shaped by the auth flows. Building `UserRepo` before `AuthService` means building it speculatively. Yes, `create` and `findByEmail` exist in any version, but the *transactional boundaries* (does registration write both `UserProfile` and audit log atomically?) depend on `AuthService` design.

3. **Opus's inline wiring tables are good for developers; our catalog is good for reviewers.** These aren't competing — they're complementary. We concede the inline format is more actionable per-phase. The merged roadmap should include both. But the cross-cutting view is not optional for an auth system — it's how you verify that `TokenManager` wiring is consistent across the three phases that touch it.

4. **Opus's observability bundling is the highest-risk structural decision in the debate.** If alpha begins with incomplete metrics, the team cannot evaluate whether alpha *passed*. The gate between alpha and beta requires "p95 < 200ms" and "error rate < 0.1%" — these numbers come from observability. Bundling observability with rollout creates a circular dependency: you need metrics to evaluate rollout, but metrics are deployed as part of rollout.

---

## Convergence Assessment

### Areas of Agreement Reached

1. **Both variants should include proactive risk identification (R-004/R-005/R-006) with Haiku's traceability format.** Opus's risk breadth + Haiku's roadmap-controls structure = stronger risk section. *(Converged)*

2. **Integration documentation should include both inline per-phase tables AND a cross-cutting catalog.** Developers get context; architects get topology. *(Converged)*

3. **Environment readiness gates are low-cost and should be included.** A checklist line before each phase is not process overhead. *(Converged)*

4. **Sequencing constraints section should be included.** Explicit > implicit for cross-team coordination. *(Converged)*

5. **Security review as a named responsibility (not necessarily a separate role) should be included.** Compromise: assign security review checkpoints to specific phase gates rather than a permanent role. *(Converged)*

6. **Validation should use Haiku's staged framework (A–D) combined with Opus's per-gate criteria table.** *(Converged)*

### Remaining Disputes (Requiring Human Decision)

1. **Phase 0: Include or skip?** — Opus argues the spec already defines the contract; Haiku argues implementation-level decisions need locking. Resolution depends on team maturity and whether OQs are truly blocking. *Score: 40% convergence.*

2. **`UserRepo` timing (Phase 1 vs Phase 2)** — Genuine architectural tradeoff between early integration testing and cleaner layering. Neither side conceded. *Score: 30% convergence.*

3. **Observability/rollout separation** — Haiku's circular-dependency argument (metrics needed to evaluate rollout gates) was not effectively rebutted by Opus. This leans toward Haiku but Opus did not concede. *Score: 50% convergence — Haiku's argument is stronger but the timeline cost is real.*

4. **Rate limiting phase** — Clean separation of concerns (Haiku) vs. early integration coverage (Opus). Legitimate tradeoff with no clear winner. *Score: 35% convergence.*

5. **Timeline** — Directly follows from the above four decisions. If Phase 0 and observability separation are adopted, timeline is ~9–10 weeks. If skipped, ~7–8 weeks. *Score: 20% convergence — fundamentally dependent on unresolved disputes.*
