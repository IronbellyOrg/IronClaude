---
convergence_score: 0.62
rounds_completed: 2
---

# Structured Adversarial Debate: Opus-Architect vs Haiku-Architect Roadmaps

## Debate Scope

Eight divergence points from the diff analysis were selected for debate, corresponding to the "Areas Requiring Debate to Resolve" (Section 4 of the diff analysis) plus two additional high-impact structural divergences.

**Debated divergence points**: D-2 (contract-first vs implementation-first), D-3 (task decomposition), D-5 (OQ resolution timing), D-6 (testing distribution), D-8 (feature flag timing), D-1 (phase granularity), D-13 (deployment scope), D-10 (timeline estimates).

---

## Round 1: Initial Positions

### Topic 1: Contract-First vs Implementation-First (D-2)

**Variant A (Opus):**
Phase 0 delivers working services — `COMP-001` is "Implement PasswordHasher," not "Define PasswordHasher contract." This is deliberate. For a medium-complexity auth module with 1 backend FTE as the primary implementer, the fastest path to validated behavior is writing the code. Contracts are useful when multiple engineers need to code against an interface simultaneously. With a single backend engineer owning Phases 0–3, the interface *is* the implementation. Defining a contract first and then implementing it doubles the task surface without reducing risk. The 92-task plan already covers the full scope; inflating it to ~130 tasks with define/implement/wire/bind splits adds tracking overhead that a small team will resent, not value.

**Variant B (Haiku):**
Contract-first is not about team size — it is about *architectural legibility*. Phase 1 defines `COMP-005` (JWT signing contract), `COMP-006` (password hasher contract), `COMP-007` (token manager contract), and `COMP-008` (middleware contract) before any implementation. This forces the architect to make interface decisions explicit and reviewable *before* sinking time into implementation details. Even with 1 FTE, the contract review is the cheapest possible moment to catch a misaligned abstraction boundary. If `TokenManager`'s contract doesn't account for reset-token lifecycle, that surfaces in review of a 20-line interface spec — not after 200 lines of implementation. The 0.5 FTE security engineer reviews contracts in Phase 1, implementations in Phase 2. Without contracts, the security review must read implementation code, which is slower and less focused.

---

### Topic 2: Task Decomposition and Wiring Visibility (D-3, D-4)

**Variant A (Opus):**
92 tasks with one task per working deliverable. Route wiring is `API-001` through `API-006` — six tasks, each registering a route. Middleware wiring is `COMP-005` ("Wire auth-middleware into Express middleware pipeline"). Service creation tasks implicitly include making services available to consumers. This is how production teams actually work: you build a service, you make it available, you move on. Splitting "implement service" from "bind service into container" from "wire service into handler" creates three tasks where one suffices. The 12 extra wiring/DI tasks in Haiku (5 DI-* tasks, 7 API-*.W1 tasks, 2 MW-* tasks) are pure tracking overhead. They don't change what gets built — they change how many checkboxes you tick.

**Variant B (Haiku):**
Integration debt is the most common source of late-project surprises. Wiring tasks (`API-001.W1` through `API-007.W1`, `MW-001`, `MW-002`, `DI-001` through `DI-005`) make integration work *visible and trackable*. When a task says "Implement JwtService," does completion mean the service exists as a file, or that it's actually resolvable at runtime? With Opus, you don't know until you read the acceptance criteria. With Haiku, `DI-001` ("Bind JwtService implementation into SecurityServiceContainer") has an unambiguous acceptance criterion: "Runtime container resolves production JwtService successfully." The `SecurityServiceContainer` artifact is named and tracked. If someone asks "is JwtService wired up?" — you check `DI-001`, not grep through `COMP-002`'s acceptance criteria. The 12 extra tasks cost ~20 minutes of tracking overhead across the entire project. Integration bugs cost days.

---

### Topic 3: Open Question Resolution Timing (D-5)

**Variant A (Opus):**
All 8 open questions are resolved in Phase 0 before any implementation begins. This is the correct sequencing because every OQ in this spec has downstream architectural consequences. OQ-3 (bcrypt vs latency) affects NFR-AUTH.1 implementation. OQ-1 (sync vs async email) affects COMP-007 design. OQ-2 (refresh token cap) affects DM-002 schema. Resolving these after implementation starts means rework. The Phase 0 resolution approach assumes stakeholders are available — and they should be, because this is a P0 security-sensitive project. If stakeholders aren't available to resolve 8 questions in 1.5 weeks, the project has a resourcing problem, not a process problem.

**Variant B (Haiku):**
Decisions (`DEC-001` through `DEC-004`) are made in Phase 1, but formal closure with implementation evidence happens in Phase 3 (`OQ-1` through `OQ-8`). This is progressive closure: decide early, validate late. The difference from Opus is not *when* the decision is made — both make decisions early. The difference is *what constitutes closure*. Opus closes OQ-3 with "Decision documented; stakeholder sign-off obtained." Haiku closes OQ-3 with "Signed-off resolution exists for bcrypt vs p95 contradiction" backed by `TEST-018` measured evidence. A decision made on a whiteboard and a decision validated by a load test are not the same confidence level. Progressive closure costs one extra validation task per OQ — 8 tasks at S effort — and provides auditable evidence that decisions actually worked.

---

### Topic 4: Testing Distribution (D-6)

**Variant A (Opus):**
Tests are co-located with implementation: `TEST-001` through `TEST-004` in Phase 1 alongside registration/login, `TEST-005` through `TEST-007` in Phase 2 alongside token refresh/profile, `TEST-008` in Phase 3 alongside password reset. This shortens the feedback loop between writing code and validating it. A bug in `PasswordHasher` surfaces in Phase 1 when `TEST-001` runs, not in Phase 3 when someone finally gets around to writing the unit test. Co-location is also better for developer flow — you implement a feature, you test it, you move on with confidence. Consolidated testing creates a "wall of tests" at the end that nobody wants to write and everyone wants to rush through.

**Variant B (Haiku):**
Phase 3 consolidates all 22 test tasks plus 14 SC validations plus 6 risk reviews. This is not "deferred testing" — it's *structured validation*. The distinction matters. Phase 2 developers write code against contracts defined in Phase 1. They run ad-hoc tests during development (any competent developer does). Phase 3 is the formal validation pass where test architecture (`TEST-ARCH-001`, `TEST-ARCH-002`) ensures comprehensive coverage. The test strategy matrix maps every FR/NFR to a verification type *before* individual tests are written. This prevents the common failure mode of co-located testing: each phase writes tests for its own features but nobody writes the cross-cutting tests (security schema validation, regression suite, E2E lifecycle) until forced to. The 22-test Phase 3 includes all cross-cutting concerns that co-located testing naturally misses.

---

### Topic 5: Feature Flag Introduction Timing (D-8)

**Variant A (Opus):**
`OPS-006` (feature flag) is in Phase 5 because the feature flag is a deployment concern, not a development concern. During Phases 1–4, the auth service is under active development — toggling it off serves no purpose because there's nothing to "roll back to." The flag becomes meaningful only when you're deploying to staging/production and need the ability to disable the new auth service if issues arise. Introducing it in Phase 1 means maintaining flag-awareness in every task across Phases 2–4, which adds conditional logic to implementation and testing without providing rollback value during development.

**Variant B (Haiku):**
`OPS-003` introduces `AUTH_SERVICE_ENABLED` in Phase 1 because the flag is a *development safety net*, not just a deployment mechanism. With the flag available from Phase 1, every integration test in Phase 3 (`TEST-021`: "Existing endpoints remain green with auth feature enabled and disabled") can validate rollback behavior throughout the test suite. Without the flag until Phase 5, the regression test in Opus (`SC-12`: "All pre-existing integration tests pass alongside new auth test suite") can only verify that auth doesn't break existing endpoints — it cannot verify that *disabling* auth restores previous behavior. That's the difference between "it works when on" and "it works when on AND off." The flag also enables incremental integration testing during Phase 2: run the system with auth off, confirm nothing breaks, then run with auth on.

---

### Topic 6: Phase Granularity (D-1)

**Variant A (Opus):**
Six phases (0–5) provide natural review gates between functional areas. Phase 1 (registration + login) is reviewed before Phase 2 (token refresh + profile) begins. This catches design issues early — if the token issuance in Phase 1 has a flaw, it's caught before Phase 2 builds token refresh on top of it. Each phase has a clear milestone with specific pass/fail criteria. The overhead of 6 phase reviews (each taking ~1 hour with stakeholders) is 6 hours across 7.5 weeks — negligible compared to the rework cost of discovering integration issues late.

**Variant B (Haiku):**
Three phases (Architecture → Implementation → Validation) reflect the actual decision cadence of the project. Phase boundaries should correspond to *qualitative shifts in work type*, not arbitrary functional groupings. Moving from "defining contracts" to "writing implementations" to "validating everything works" are genuine phase transitions. Splitting implementation into 4 sub-phases (Opus Phases 1–4) creates artificial gates where the same engineer pauses to get review on login before starting token refresh — but the reviewer needs to see both to assess the token lifecycle holistically. Fewer phases, more meaningful checkpoints: Haiku adds Checkpoint B at mid-Phase 2 to catch the integration issues Opus is worried about, without requiring a full phase boundary.

---

### Topic 7: Deployment Scope (D-13)

**Variant A (Opus):**
Phase 5 includes 18 tasks covering staging deployment (`OPS-007`), production deployment (`OPS-008`), feature flag configuration (`OPS-006`), and all 14 SC validations. The roadmap's job is to deliver a working feature to production, not to hand off a validated codebase and hope someone else deploys it. If the team owns deployment — and with 0.25 FTE DevOps allocated, they clearly do — then deployment is in scope. Omitting deployment from the roadmap creates an implicit handoff that often falls through the cracks, especially for security-sensitive features where the deployment sequence matters (enable monitoring → deploy canary → validate → expand).

**Variant B (Haiku):**
Deployment is implied after Phase 3 validation, not absent. The `OperationalReadinessChecklist` artifact in Phase 3 covers monitoring, alerts, feature-flag rollback, migration rollback, and key-rotation readiness. What Haiku doesn't do is prescribe the deployment playbook (canary percentages, staging smoke test scripts, PagerDuty escalation policies) — because those are operational procedures that belong in a runbook, not a development roadmap. Mixing development tasks and operational procedures in the same phase creates a document that serves two audiences poorly. The roadmap audience is engineers building the feature. The deployment audience is the DevOps team executing the rollout. Haiku's approach: the roadmap proves the feature is ready; a separate deployment plan handles the rollout.

---

### Topic 8: Timeline Estimates (D-10)

**Variant A (Opus):**
7.5 weeks is a single-point estimate with explicit parallelization opportunity (Phase 2 + Phase 3 concurrent → 6.5 weeks). This is more actionable for project planning than a range. The parallelization note gives the project manager a concrete lever: "If we can resolve OQ-7 in Phase 0, we save a week." Single-point estimates with identified compression opportunities are how experienced project managers actually plan — they take the number, add their own buffer based on team velocity, and schedule accordingly.

**Variant B (Haiku):**
5.5–7 weeks as a range acknowledges the inherent uncertainty in a medium-complexity security project with 8 unresolved open questions. The lower bound (5.5 weeks) assumes smooth OQ resolution and no rework. The upper bound (7 weeks) accounts for decision churn and integration surprises. Giving a single number (7.5 weeks) implies false precision — it suggests the estimator knows something they don't. The range is also tighter than Opus's estimate, reflecting the efficiency of contract-first development: when interfaces are stable before implementation, there's less rework in later phases. Opus's 7.5-week estimate implicitly includes rework time that contract-first development avoids.

---

## Round 2: Rebuttals

### Topic 1 Rebuttal: Contract-First vs Implementation-First

**Variant A (Opus) rebuts Variant B:**
The security review argument is plausible but overstated. The 0.5 FTE security engineer is allocated to Phases 0 and 4 in Opus — they review the *architecture decisions* in Phase 0 (which are contracts in all but name) and the *hardened implementation* in Phase 4. Reviewing a formal interface spec vs reviewing the implementation's public API is a marginal difference when the reviewer is a security engineer focused on cryptographic correctness, not API design. Furthermore, Haiku's contract tasks don't actually prevent implementation misalignment — they prevent *interface* misalignment. The real risk in auth code isn't "does the interface have the right methods?" — it's "does the implementation handle timing attacks, token reuse, and hash comparison correctly?" Those risks exist only in implementation code, which contracts don't touch.

**Variant B (Haiku) rebuts Variant A:**
Opus conflates "contracts are unnecessary for 1 FTE" with "contracts have no value for 1 FTE." Even a solo developer benefits from reviewing their own interface design before committing to implementation. But the real argument isn't about the solo developer — it's about the *fractional team*. The 0.5 FTE security engineer and 0.5 FTE QA engineer both need to understand the system's surface area. Contracts give them a reviewable artifact that's 10x smaller than the implementation. The security engineer reviews 8 contracts in Phase 1 (~200 lines total), then focuses on implementation correctness in Phase 2 (~2000 lines). Without contracts, the security review in Phase 4 covers everything at once — a much larger review surface with less time to request changes.

---

### Topic 2 Rebuttal: Wiring Visibility

**Variant A (Opus) rebuts Variant B:**
"Integration bugs cost days" is an appeal to fear without evidence specific to this project. This is a greenfield auth module, not an integration of legacy systems. The integration surface is: 6 routes registered, 1 middleware wired, 3 services consumed by handlers. Opus tracks all of these — `API-001` through `API-006` for routes, `COMP-005` for middleware, and each FR-AUTH.* task's acceptance criteria includes "delegates to [service]." The claim that you need `DI-001` through `DI-005` to know whether services are wired assumes a project-tracking tool that can't search acceptance criteria. If the team uses any modern issue tracker, "is JwtService wired?" is answered by checking `COMP-002`'s acceptance criteria. The 12 extra tasks don't provide information that isn't already in Opus — they just duplicate it into separate tracking items.

**Variant B (Haiku) rebuts Variant A:**
Opus's argument that "the integration surface is small" proves the point — if the surface is small, the overhead of tracking it explicitly is also small. Five DI-binding tasks at S effort each = ~2.5 hours total. Seven route-wiring tasks at S effort each = ~3.5 hours total. Total overhead: ~6 hours across the entire project. The value: every integration point has a single task with a binary pass/fail status. The `SecurityServiceContainer` isn't just a tracking mechanism — it's a named architectural artifact that appears in documentation, test fixtures, and operational runbooks. When someone asks "what services does the auth module depend on?" in six months, `SecurityServiceContainer` answers that question. Opus's distributed integration has no single artifact to point to.

---

### Topic 3 Rebuttal: OQ Resolution Timing

**Variant A (Opus) rebuts Variant B:**
Progressive closure sounds rigorous but introduces a subtle risk: decisions that are "made" in Phase 1 but not "closed" until Phase 3 can be reopened. If OQ-3 (bcrypt vs latency) is decided in Phase 1 but the Phase 3 load test shows the decision didn't work, you've built 2+ weeks of implementation on a faulty premise. Opus's approach: resolve in Phase 0, implement the resolution in Phase 4, validate in Phase 5. If the Phase 5 validation fails, the rework is confined to Phase 4 (NFR hardening) — not the entire implementation. Furthermore, 8 OQs at S effort in Phase 0 = ~1 week of focused decision-making. That's a worthwhile investment to eliminate ambiguity before writing a single line of feature code.

**Variant B (Haiku) rebuts Variant A:**
Opus mischaracterizes progressive closure as "decisions that can be reopened." The decisions are made in Phase 1 and are binding — `DEC-001` through `DEC-004` have explicit acceptance criteria. What Phase 3 adds is *evidence that the decision worked*. If the Phase 3 load test shows the OQ-3 decision didn't work, that's not "reopening" — that's *discovering the decision was wrong*, which happens in both approaches. The difference is when you discover it. Opus discovers it in Phase 5 validation. Haiku discovers it in Phase 3 — with 2+ weeks of buffer before a hypothetical Phase 4 deployment. Both approaches build on the decision from Phase 0/1. Haiku just validates sooner.

---

### Topic 4 Rebuttal: Testing Distribution

**Variant A (Opus) rebuts Variant B:**
Haiku claims Phase 3 prevents the "common failure mode of co-located testing: missing cross-cutting tests." But Opus *does* include cross-cutting tests: `TEST-007` (security schema validation across all endpoints) in Phase 2, `TEST-012` (E2E lifecycle) in Phase 5, and `TEST-009`/`TEST-010` (enumeration resistance, rate limiting) in Phase 4. The difference is that Opus writes these when the relevant features are complete, not in a batch at the end. `TEST-007` runs in Phase 2 because that's when all response schemas exist — writing it earlier would be impossible, writing it later would be wasteful. Haiku's `TEST-ARCH-001` (test strategy matrix) is valuable but doesn't require consolidated testing — Opus could add it to Phase 0 without changing the test distribution.

**Variant B (Haiku) rebuts Variant A:**
Opus's cross-cutting tests exist but are scattered. `TEST-007` in Phase 2, `TEST-009`/`TEST-010` in Phase 4, `TEST-012` in Phase 5. A developer finishing Phase 2 doesn't know whether all cross-cutting tests relevant to their work have been written — they'd need to scan Phases 3–5 to find out. Haiku's consolidated Phase 3 makes the test inventory *complete and auditable at a single point*. The `AuthTestMatrix` artifact maps every FR/NFR to its verification type. When the QA engineer asks "are we done testing?" — the answer is a single Phase 3 status check, not a cross-phase audit. The cost of consolidated testing (slightly longer feedback loops for individual features) is offset by the benefit of comprehensive coverage visibility.

---

### Topic 5 Rebuttal: Feature Flag Timing

**Variant A (Opus) rebuts Variant B:**
Haiku's argument assumes the regression test (`TEST-021`) needs the feature flag to validate rollback. But the regression test's job is to verify "existing endpoints remain green with auth feature enabled." The flag-disabled case is a deployment concern, not a development concern. During development, the auth routes either exist or they don't — there's no intermediate state where you need a flag. Introducing the flag in Phase 1 means every developer must reason about two code paths (flag on, flag off) from day one. That's cognitive overhead that slows development without providing value until deployment. The flag takes ~2 hours to implement — doing it in Phase 5 vs Phase 1 doesn't change the total effort, just when the complexity is introduced.

**Variant B (Haiku) rebuts Variant A:**
"Two hours to implement" is exactly why it should be in Phase 1, not Phase 5. If the flag is trivial to add, add it early and get the testing benefit across all phases. The cognitive overhead argument is backwards: a feature flag is a single `if` check at the route-group level (`API-001`), not per-endpoint conditional logic. Developers don't "reason about two code paths" — they develop with the flag on and ignore it. But the *test suite* benefits enormously: `TEST-021` validates that existing endpoints work with auth both enabled and disabled, providing regression confidence that Opus can only get in Phase 5. If a Phase 2 implementation accidentally breaks an existing endpoint *only when auth is disabled* (e.g., middleware ordering issue), Haiku catches it in Phase 3; Opus catches it after production deployment.

---

### Topic 6 Rebuttal: Phase Granularity

**Variant A (Opus) rebuts Variant B:**
Haiku's Checkpoint B (mid-Phase 2: "registration/login/refresh functional") is essentially Opus's Phase 2 milestone without the phase boundary. The question is whether a "checkpoint" provides the same governance value as a "phase boundary." In practice, checkpoints are advisory — someone looks at the work and says "looks good." Phase boundaries are gates — the phase doesn't proceed until the milestone is validated. For a security-sensitive auth module, the gate model is safer. If the login token issuance in Opus Phase 1 has a subtle flaw (e.g., timing leak in enumeration resistance), the Phase 1 → Phase 2 gate catches it. Haiku's Checkpoint B might catch it, or the checkpoint might be treated as a formality because Phase 2 is "already in progress."

**Variant B (Haiku) rebuts Variant A:**
The gate model assumes that "review at phase boundary" is more rigorous than "review at checkpoint." That's an organizational culture question, not an architectural one. A disciplined team treats checkpoints as seriously as phase gates. An undisciplined team rubber-stamps phase gates. The real cost of 6 phases is calendar time: each phase boundary requires scheduling a review, collecting stakeholders, presenting progress, and obtaining sign-off. With fractional resources (0.5 FTE security, 0.5 FTE QA, 0.25 FTE DevOps), scheduling 6 reviews across 7.5 weeks means a review almost every week — which for part-time contributors means constant context-switching. Three phases with 4 checkpoints provides the same visibility with fewer synchronization points.

---

### Topic 7 Rebuttal: Deployment Scope

**Variant A (Opus) rebuts Variant B:**
"A separate deployment plan handles the rollout" is exactly the handoff gap that causes production incidents. The deployment plan needs to reference the roadmap's success criteria, the feature flag, the migration rollback procedure, and the monitoring thresholds — all of which are defined in the roadmap. Separating them means the deployment plan author must read the roadmap, extract the relevant details, and create a second document. With Opus, Phase 5 *is* the deployment plan: `OPS-007` (staging smoke test) → `OPS-008` (production cutover with canary percentage). One document, one workflow, one tracking system. The `OperationalReadinessChecklist` artifact in Haiku is a checklist without tasks — it's a reminder to do things, not a plan for doing them.

**Variant B (Haiku) rebuts Variant A:**
Opus's Phase 5 conflates validation tasks (SC-1 through SC-14) with deployment tasks (OPS-006 through OPS-008) in a single phase. These have different owners, different timelines, and different failure modes. Validation is done by the engineering team. Deployment is done by DevOps. Mixing them in one phase means either the deployment waits for validation (blocking DevOps resources) or they run concurrently (making it unclear whether deployment depends on all validation passing). Haiku's separation is cleaner: Phase 3 produces a validated, release-ready artifact. The deployment team takes the artifact and executes the rollout per their standard procedures. The `OperationalReadinessChecklist` is the interface contract between the development team and the operations team — it says "here's what we've proven; here's what you need to verify operationally."

---

### Topic 8 Rebuttal: Timeline Estimates

**Variant A (Opus) rebuts Variant B:**
Haiku claims the range is tighter (5.5–7 weeks) than Opus's single point (7.5 weeks), implying Haiku is faster. But the comparison is misleading. Haiku's 5.5-week lower bound excludes deployment, which Opus's 7.5 weeks includes. If you add deployment to Haiku's estimate (~0.5–1 week), the range becomes 6–8 weeks — wider than Opus, not tighter. The "efficiency of contract-first development" claim is unsubstantiated — there's no evidence that defining contracts first reduces total effort for a 1-FTE backend team. Contract-first can *increase* total effort by adding a round of interface design that the solo developer would otherwise skip. The parallelization note in Opus (6.5 weeks with Phase 2+3 concurrent) is a concrete, actionable optimization that Haiku doesn't identify.

**Variant B (Haiku) rebuts Variant A:**
The deployment comparison is fair: Haiku treats deployment as out of scope for the roadmap because it's an operational procedure. Adding it doesn't extend the *development* timeline. Opus's 7.5-week estimate includes 1 week of Phase 5 that's mostly validation + deployment — activities that Haiku distributes across Phase 3 (validation) and the ops team (deployment). The real timeline difference is in development effort: Haiku's 130 tasks include explicit wiring and contract work that *replaces* implicit rework, not adds to it. The range estimate reflects honest uncertainty about 8 open questions. Opus's 7.5-week single point assumes all OQs resolve cleanly in Phase 0 — but if they don't (and some almost certainly won't), the schedule has no acknowledged flexibility.

---

## Convergence Assessment

### Areas of Agreement Reached Through Debate

1. **OQ resolution must happen early** — both approaches make decisions in Phase 0/1. The disagreement is about closure evidence, not timing. *Convergence*: early decision + later validation is the strongest combined approach.

2. **Feature flag value is real** — Opus acknowledged the flag takes ~2 hours. Haiku acknowledged it's a single `if` check, not per-endpoint complexity. *Convergence*: introducing the flag early has low cost and moderate testing benefit; this is net positive.

3. **Cross-cutting tests must be planned** — Opus conceded `TEST-ARCH-001` (test strategy matrix) would add value to Phase 0. Haiku conceded that some tests (like `TEST-007` schema validation) can only be written once features exist. *Convergence*: a test strategy matrix should be defined early; individual tests should be written when their prerequisites are complete.

4. **Mid-phase checkpoints add value** — Opus's rebuttal argued checkpoints are weaker than phase gates, but didn't argue they're valueless. *Convergence*: some form of mid-implementation checkpoint (whether gate or advisory) is warranted for the largest implementation block.

### Remaining Disputes (No Convergence)

1. **Contract-first vs implementation-first** — fundamental philosophical disagreement about whether interface stability or implementation velocity matters more for a 1-FTE team. Neither side conceded the core claim. Opus: contracts are overhead for solo developers. Haiku: contracts are cheap insurance regardless of team size.

2. **Testing distribution** — co-located (Opus) vs consolidated (Haiku) reflects genuine tradeoffs that neither rebuttal resolved. Co-location catches bugs earlier. Consolidation ensures completeness. The optimal choice depends on team discipline and historical defect patterns, which neither variant can know from the spec.

3. **Deployment in scope or out** — unresolvable without knowing the team's operational model. If the development team owns deployment (common in smaller orgs), Opus is right. If a separate ops team handles deployment (common in larger orgs), Haiku is right.

4. **Phase granularity** — 6 phases vs 3 phases remains a governance question. Opus's gate model is safer for teams with review discipline. Haiku's checkpoint model is more efficient for teams with fractional resources. The spec doesn't specify which organizational context applies.

5. **Wiring task granularity** — Haiku's explicit DI/wiring tasks vs Opus's implicit integration. Both sides acknowledged the overhead is small (~6 hours), but disagreed on whether the tracking value justifies it. This is a team preference, not an architectural decision.

### Synthesis Recommendation

A merged roadmap would take:
- **From Opus**: deployment phase, FTE allocations, frontmatter traceability, parallelization analysis, co-located unit/integration tests for individual features
- **From Haiku**: early feature flag (Phase 1), contract definitions for security-sensitive interfaces only (JWT, token manager), test strategy matrix in foundation phase, explicit release gate criteria, mid-phase checkpoint, evidence-based OQ closure
- **From neither (new)**: a hybrid test distribution where unit and integration tests are co-located with implementation, but security, regression, E2E, and load tests are consolidated in a validation phase
