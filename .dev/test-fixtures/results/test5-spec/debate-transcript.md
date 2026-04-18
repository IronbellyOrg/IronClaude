---
convergence_score: 0.62
rounds_completed: 2
---

# Structured Adversarial Debate: Opus-Architect vs Haiku-Architect Roadmaps

## Preamble

**Shared foundation**: Both variants agree on 16 foundational positions including RS256 signing, bcrypt cost 12, refresh token rotation, stateless access tokens, feature-flagged rollout, dependency injection, identical API surfaces, risk priorities, gap identification, open questions, NFRs, component decomposition, and team skill requirements. The debate focuses on the 18 divergence points where architectural judgment differs.

---

## Round 1: Initial Positions

### Divergence Cluster 1: Phase Structure and Test Timing (D-1, D-3, D-8)

**Variant A (Opus)** — 7 phases, tests co-located, monolithic SC validation:

The 7-phase structure isolates concerns cleanly: infrastructure, crypto, tokens, auth service, HTTP layer, security hardening, and release validation each get a dedicated phase with a single-purpose objective. This is not ceremony for ceremony's sake — it produces precise phase gates. When Phase 2 completes, you know crypto primitives work. When Phase 3 completes, you know token rotation works. There is no ambiguity about what "done" means at each boundary.

Co-locating tests with implementation is the stronger engineering discipline. TEST-001 through TEST-004 ship alongside PasswordHasher and JwtService in Phase 2. If the hash timing is wrong, you find out in Week 1, not Week 4. The alternative — deferring all tests to a validation phase — is a known anti-pattern that creates a late-phase testing bottleneck. Defects discovered in a concentrated test phase require changes that ripple backwards across multiple completed phases, disrupting work that was considered "done."

The monolithic SC validation (TEST-017) is defensible because it runs *after* all unit and integration tests have already validated individual criteria. It is a final coherence check, not a first-pass discovery mechanism.

**Variant B (Haiku)** — 5 phases, tests concentrated in Phase 4, distributed SC validation:

Five phases reduce coordination overhead without sacrificing rigor. Each phase is broader but self-contained: Phase 1 delivers foundations through repository abstractions, Phase 2 delivers working authentication orchestration, Phase 3 wires the request path. This means fewer milestone ceremonies, fewer handoff points, and fewer opportunities for integration gaps between narrow phases.

Concentrating tests in Phase 4 is a deliberate architectural choice, not negligence. During Phases 1-3, the team is iterating on design — interfaces are stabilizing, contracts are being defined. Writing comprehensive test suites against unstable interfaces produces test churn. Phase 4 tests are written against *settled* contracts, which means they are more stable and more meaningful as regression protection. The risk of late discovery is mitigated by the fact that Phases 1-3 include implicit developer testing — the concentrated phase formalizes and hardens what developers have already been verifying informally.

Distributed SC validation (SC-1, SC-11, SC-20, SC-21, SC-22 as individual Phase 4-5 tasks) provides traceable evidence per criterion. When a release reviewer asks "did we validate replay detection?", the answer is a specific task (SC-11) with linked evidence, not "it's somewhere inside TEST-017."

---

### Divergence Cluster 2: Component Count and Abstraction Level (D-4, D-11, D-12, D-13)

**Variant A (Opus)** — 11 components, cross-cutting concerns handled inline:

Eleven components is the right count for the actual problem size. PasswordHasher, JwtService, TokenManager, AuthService, AuthMiddleware, AuthRoutes, AuthMigration, UserRepository, RefreshTokenRepository, EmailDispatcher, and RateLimiter — each represents a genuine responsibility boundary. Error mapping, request validation, auth context propagation, and cookie transport are *implementation details* of these components, not independent responsibilities.

Creating COMP-013 (auth context attachment), COMP-014 (route-handler adapter), COMP-015 (error mapping), and COMP-016 (cookie/header transport) as named components is premature abstraction. A 3-line error mapping function inside the route handler does not need its own component identifier, test suite, and ownership entry. This inflates the task count, creates thin wrappers that add indirection without value, and makes the system harder to navigate for a team that is likely 2-3 developers.

The PasswordResetRepository (COMP-010 in Haiku) is a thin wrapper around 4 methods that could live in the AuthService. Creating a repository for every table is a pattern, not a principle — when the table has simple CRUD semantics and is only accessed by one service, the abstraction adds no testability benefit beyond what mocking the database layer already provides.

**Variant B (Haiku)** — 17 components, every concern gets a named artifact:

Seventeen components reflects the actual architectural surface area. Error mapping (COMP-015) is not a 3-line function — it is the component responsible for ensuring that domain errors never leak credentials, that 401 messages are generic, that 429 includes Retry-After, and that the response format is consistent across 6 endpoints. When this logic is "inline" in route handlers, it gets duplicated, and inconsistencies emerge. A named component makes error-response consistency a testable property.

PasswordResetRepository (COMP-010) follows the same pattern as UserRepository and RefreshTokenRepository. Consistency in abstraction patterns reduces cognitive load. When a developer sees that users and refresh tokens have repositories, they expect reset tokens to have one too. Breaking the pattern forces them to understand *why* this table is different, when it isn't meaningfully different.

The auth context model (COMP-013) prevents sensitive token material from propagating through the handler chain. Making this a named artifact means there is a test that asserts "no raw JWT appears in the request context passed to handlers." Without it, this invariant is implicit and fragile.

The route-handler adapter (COMP-014) enforces the boundary between HTTP concerns and domain logic. Without it, AuthService methods accumulate HTTP-specific logic (reading cookies, setting headers) that makes them harder to test and reuse.

---

### Divergence Cluster 3: Migration and Schema Design (D-5, D-6)

**Variant A (Opus)** — 3 separate migrations, minimal refresh token schema:

Three separate migrations (users, refresh_tokens, password_reset_tokens) provide table-level rollback granularity. If the password_reset_tokens schema needs modification after deployment, you can roll back MIG-003 without touching users or refresh_tokens. This is standard practice in production database management — you do not bundle unrelated schema changes into a single migration.

The minimal refresh token schema (id, user_id, token_hash, expires_at, revoked boolean, created_at) is sufficient for v1.0. Replay detection works by checking whether a presented token hash is marked revoked — if it is, revoke all tokens for that user. You do not need `replaced_by_token_id` to implement this. The lineage chain is a forensic analysis feature that adds schema complexity, self-referencing foreign keys, and migration maintenance burden for a capability that is not in the v1.0 requirements. YAGNI applies.

The `created_ip` and `user_agent` fields are session metadata features that belong in a v1.1 "session management" feature, not in a v1.0 authentication service. Adding them now creates columns that are populated but never queried, wasting storage and creating the false impression that per-device session management is supported.

**Variant B (Haiku)** — 2 atomic migrations, rich refresh token schema:

Two migrations (one up, one down) treat the auth schema as an atomic unit because it *is* an atomic unit. You will never deploy users without refresh_tokens, and you will never roll back refresh_tokens without also rolling back users. The auth subsystem either exists or it doesn't — feature-flag gating already provides the on/off switch. Separate migrations create the illusion of independent table lifecycle that will never be exercised in practice.

The rich refresh token schema (`replaced_by_token_id`, `revoked_at` timestamp, `created_ip`, `user_agent`) is worth the marginal complexity because:

1. `replaced_by_token_id` enables walking the rotation chain during a security incident. When replay is detected, you can trace which token replaced which, identifying the point of compromise. Without it, you can only revoke — you cannot investigate.
2. `revoked_at` as a nullable timestamp is strictly more informative than a boolean `revoked` flag at zero additional query cost. It tells you *when* revocation happened, which is essential for incident timelines.
3. `created_ip` and `user_agent` are nullable and cost nothing when unpopulated. But when a user reports "I didn't log in from that device," these fields are the difference between "we can check" and "we have no data." Adding columns to a populated table later is a production migration risk; adding them now to an empty table is free.

---

### Divergence Cluster 4: API Contracts, Integration, and Operational Readiness (D-2, D-7, D-14, D-16, D-17, D-18)

**Variant A (Opus)** — Global integration section, contracts with implementation, concentrated security phase, health check early:

The global integration section (Section 2) gives an architect or new team member a single place to understand all wiring: DI container, route registry, middleware chain, feature flag, migration registry. This is a map of the system, not a phase-specific checklist. When you are debugging a production issue at 2am, you want one section that tells you how everything connects, not integration notes scattered across 5 phases.

Defining API contracts alongside implementation (Phase 5) is pragmatic for a single team. Contract-first development assumes a consumer (frontend team) is waiting in parallel. If the same team builds both sides, or if the frontend is not yet started, defining contracts separately creates documents that immediately drift from implementation. Contracts emerging from working code are accurate by construction.

A dedicated security hardening phase (Phase 6) provides a clean review milestone for a security engineer. Security review is most effective as a focused activity, not as a distributed checkbox exercise. Phase 6 says "stop building, start validating security properties holistically." This is when you run penetration tests, verify that all RISK mitigations actually work together, and confirm that no security control was accidentally omitted during feature development.

The health check endpoint (OPS-001) in Phase 1 with concrete criteria (GET /health, <50ms) delivers observable infrastructure on Day 1. Every subsequent phase benefits from being able to verify "is the service up and connected to the database?" without manual checking.

**Variant B (Haiku)** — Per-phase integration, contract-first in Phase 2, distributed security, OQ tracking tasks:

Per-phase integration documentation is more actionable because it appears where the work happens. When a developer is implementing Phase 3 routes, the integration points for Phase 3 are right there — they do not need to cross-reference a global section written weeks earlier. Integration notes age; co-located integration notes are current.

Contract-first API definition (Phase 2, before route implementation in Phase 3) enables parallel frontend work and catches interface mismatches before code is written. Even on a single team, having API-001 through API-006 defined as contracts provides a test harness target: integration tests can be written against the contract before the implementation exists. This is strictly more valuable than discovering contract issues during implementation.

Distributed security validation catches issues earlier. AC-6 (secrets isolation) is validated in Phase 1 when the secrets manager is integrated, not in Phase 6 when it has been running unchecked for weeks. RISK-1 (key compromise mitigation) is validated in Phase 3 alongside the key rotation implementation. Waiting for a dedicated security phase means security defects found in Phase 6 require changes to Phases 1-3 code, which is the same late-discovery problem Opus criticizes about concentrated testing.

Open question tracking as explicit tasks (OQ-3 in Phase 1, OQ-1/OQ-2 in Phase 2, with resolution recording tasks OQ-1A/OQ-2A in Phase 5) makes decision debt visible. Opus mentions "resolve before Phase N" in prose, but prose directives are not tracked in sprint boards, not assignable, and not verifiable. When a project manager asks "have all blocking decisions been made?", Haiku's task-based tracking provides a definitive answer.

---

### Divergence Cluster 5: Timeline and Estimation (D-15)

**Variant A (Opus)** — 4-5 weeks (1 dev), 2.5-3.5 weeks (2 devs), critical path diagram:

The dual-track estimate (single developer and parallel developer) is more actionable for sprint planning. The critical path ASCII diagram makes scheduling concrete and reviewable:

```
DEP-4 → DM-001 → MIG-001 → COMP-007 → COMP-008 → COMP-001 → COMP-003 → COMP-004 → COMP-006 → API-001 → TEST-013 → TEST-017
```

This tells you exactly which tasks cannot be parallelized and where adding a second developer helps. The 4-5 week estimate assumes OQ decisions are made promptly, which is a reasonable assumption given that OQ resolution is called out as a Phase 1 prerequisite.

**Variant B (Haiku)** — 5.0-7.5 engineering weeks, textual description:

The wider range (5.0-7.5 weeks) reflects honest uncertainty about organizational overhead: OQ resolution delays, email provider procurement, integration debugging, and the inevitable "we need to rethink this" moments. Opus's 4-5 week estimate assumes a frictionless environment that rarely exists. A range that spans 50% is more honest than one that spans 25% — it tells stakeholders "this is genuinely uncertain" rather than creating a false sense of precision.

The textual per-phase breakdown is sufficient for planning. An ASCII critical path diagram is a snapshot that becomes outdated as soon as task dependencies shift during execution. Real critical path analysis should be done in a project management tool with live dependency tracking, not in a static markdown document.

---

### Divergence Cluster 6: Rollback and Operational Artifacts (D-9, D-10)

**Variant A (Opus)** — Rollback in regression suite, email in Phase 4:

Rollback verification within TEST-018 (end-to-end regression) is appropriate because rollback is an end-to-end operation. It exercises the full sequence: feature flag disable, down-migration execution, and verification that the system returns to pre-auth state. Isolating this into a separate task creates the impression that rollback can be validated independently of the rest of the system, when in reality it must be validated in context.

Deferring email integration to Phase 4 is pragmatic because email is a leaf dependency — nothing else depends on it. The EmailDispatcher interface can be mocked in Phases 1-3 with zero impact on other development.

**Variant B (Haiku)** — Explicit rollback rehearsal, email interface in Phase 1:

MIG-003 (rollback rehearsal) as a dedicated task with staging rehearsal criteria makes rollback readiness a first-class gate. "Run the down migration in staging and verify no orphaned objects remain" is a concrete, assignable, verifiable task. Buried inside a larger regression suite, it risks being deprioritized or perfunctorily checked. Production rollback failures are among the highest-severity incidents — the validation deserves its own task.

Defining the email service interface in Phase 1 (DEP-3) reduces integration risk. If the email provider requires procurement, API key provisioning, or domain verification, that lead time starts in Week 1 rather than Week 3. The interface is defined early; the implementation can still be mocked. This is not about building the email integration early — it is about *surfacing the dependency* early so that organizational blockers are discovered before they are on the critical path.

---

## Round 2: Rebuttals

### Rebuttal on Test Timing

**Variant A rebuts Variant B**: The claim that "interfaces are stabilizing during Phases 1-3" is an argument against Haiku's own design — if interfaces are unstable, the implementation is unstable, and concentrated testing in Phase 4 will discover fundamental design issues that require reworking Phases 1-3. Co-located tests *force* interface stability because you cannot write a passing test against a broken interface. The "test churn" concern is a symptom of poor interface design, not a reason to defer testing. Additionally, Haiku's distributed SC validation creates 12+ separate validation tasks that each require evidence linking — this is more overhead than a single comprehensive validation pass.

**Variant B rebuts Variant A**: Co-located tests are only TDD-adjacent if the team actually practices TDD. If they do not, "write tests in the same phase" becomes "write tests after the implementation is done but before the phase closes," which is functionally equivalent to concentrated testing but with more context switching. The real question is whether tests are *gate-keeping* — and Haiku's Phase 4 is an explicit gate that cannot be bypassed, while Opus's co-located tests can be deprioritized within a phase when schedule pressure mounts. The 12 SC validation tasks have higher overhead but provide auditable evidence; Opus's TEST-017 is a black box that passes or fails with no granular visibility.

### Rebuttal on Component Count

**Variant A rebuts Variant B**: The consistency argument ("UserRepository and RefreshTokenRepository exist, so PasswordResetRepository should too") prioritizes pattern uniformity over pragmatic engineering. If PasswordResetRepository has 4 methods and is called by exactly one service, the abstraction's value is near-zero — you are creating a file, an interface, and a test suite to wrap 4 database queries that will never be reused. COMP-013, COMP-014, COMP-015, and COMP-016 are even thinner — auth context attachment is 5 lines of middleware, error mapping is a switch statement, and cookie handling is a few header operations. Naming these as components inflates the task count by 35% (from ~94 to ~100) without proportional quality improvement.

**Variant B rebuts Variant A**: The "thin wrapper" dismissal underestimates the value of named, testable boundaries. Error mapping being "a switch statement" is exactly why it needs to be a named component — switch statements are where inconsistencies hide. When endpoint 4 maps a domain error to 400 instead of 401 because the developer copied from a different endpoint, the bug is invisible without a centralized mapping component and its test suite. The 35% task count increase is misleading because many of Opus's tasks contain implicit sub-tasks (error handling, validation, transport) that are simply unnamed. The total work is similar; Haiku makes it visible and trackable.

### Rebuttal on Migration and Schema

**Variant A rebuts Variant B**: The "auth is atomic" argument ignores operational reality. If a column needs to be added to refresh_tokens in a hotfix (e.g., adding an index for a query that is slow in production), you must also include users and password_reset_tokens in the rollback path of a combined migration — even though those tables are unaffected. Separate migrations provide surgical rollback. The claim that `replaced_by_token_id` "costs nothing" ignores the self-referencing foreign key constraint, which complicates INSERT operations during rotation and requires careful NULL handling. And `created_ip`/`user_agent` being "nullable and free" creates tech debt: columns that exist but are never queried mislead future developers into thinking session tracking is implemented.

**Variant B rebuts Variant A**: The hotfix scenario is contrived — adding a column to refresh_tokens would be a *new* migration (MIG-004 or equivalent), not a modification of MIG-002. The number of *initial* migrations is irrelevant to future schema evolution; each future change gets its own migration regardless. The self-referencing FK on `replaced_by_token_id` is a standard pattern (tree/linked-list in SQL) that any competent ORM handles transparently. The "misleading future developers" concern about nullable columns is addressed by schema documentation (which both variants require) — the column's existence signals "this data CAN be captured," and its NULLs signal "it is not yet captured." This is informative, not misleading.

### Rebuttal on Security Placement

**Variant A rebuts Variant B**: Distributed security validation creates a false sense of security completeness. Validating AC-6 in Phase 1 and RISK-1 in Phase 3 does not replace a holistic security review. Security vulnerabilities often emerge from the *interaction* between components, not from individual component failures. A dedicated Phase 6 forces the team to examine the security posture of the *assembled system*, including attack surfaces that only appear when all components are wired together (e.g., can a timing side-channel in the login endpoint reveal whether an email exists, despite the generic 401 response?). Haiku validates pieces; Opus validates the whole.

**Variant B rebuts Variant A**: A dedicated security phase in Phase 6 means security defects discovered there require changes to code completed in Phases 1-5. The cost of fixing a security issue grows with the amount of dependent code built on top of it. If AC-6 (private key isolation) is wrong in Phase 1 and discovered in Phase 6, every component that consumed the key in Phases 2-5 is potentially affected. Validating early bounds the blast radius. The "holistic review" argument is valid but is better served by a *review milestone* (a security engineer reviews the assembled system) rather than a *development phase* (the team builds security hardening tasks). These are different activities — one is an audit, the other is construction.

### Rebuttal on Timeline

**Variant A rebuts Variant B**: Haiku's 5.0-7.5 week range spans 50%, which is too wide to be useful for planning. A sprint commitment of "somewhere between 5 and 7.5 weeks" forces the project manager to plan for 7.5 weeks, making the lower bound meaningless. Opus's 4-5 week estimate with an explicit critical path diagram lets the team identify *which tasks* are on the critical path and optimize accordingly. The "frictionless environment" criticism applies equally to Haiku — organizational friction adds time to any estimate. The question is whether the estimate helps with planning, and a tighter range with a visible dependency chain is more plannable.

**Variant B rebuts Variant A**: Opus's 4-5 week estimate does not account for OQ resolution time. If OQ-3 (database engine) takes a week of organizational deliberation, Phase 1 cannot start on time. If OQ-1 (email dispatch) requires vendor evaluation, Phase 4 is blocked. Haiku's wider range is not imprecision — it is an honest acknowledgment that ~30% of the work depends on decisions that have not been made. A range that is "too wide to be useful" is more honest than a range that is too narrow to be accurate. Furthermore, the 2-dev parallel estimate in Opus assumes both developers can work independently through Phases 2-4, which requires the DI scaffold (AC-5) to be rock-solid on Day 1 — a big assumption for a component built in Phase 2.

### Rebuttal on Operational Artifacts

**Variant A rebuts Variant B**: Four separate operational tasks (OPS-003 deployment, OPS-004 key rotation, OPS-005 alerting, OPS-006 staged rollout) plus COMP-017 (ownership map) fragment what should be a cohesive operational handoff. A single comprehensive runbook (OPS-005 in Opus Phase 7) ensures that deployment, rollback, key rotation, and incident response are documented *in relation to each other*. Separate documents risk contradictory instructions (e.g., "disable the feature flag" in the deployment runbook but "run down-migration first" in the rollback runbook). The ownership map (COMP-017) is organizational process, not architecture — it belongs in a team wiki, not in the roadmap.

**Variant B rebuts Variant A**: A single comprehensive runbook is harder to parallelize (one person writes it), harder to review (one large document), and harder to maintain (any ops change requires editing the monolith). Separate runbooks can be assigned to different team members with relevant expertise: the DevOps engineer writes OPS-003, the security engineer writes OPS-004, the SRE writes OPS-005. Contradictions between documents are caught during the Phase 5 release readiness review — that is what the review is for. The ownership map belongs in the roadmap *because it is a deliverable* — without it, operational responsibility is implicit and contested when incidents occur.

---

## Convergence Assessment

### Areas of Agreement Reached Through Debate

1. **Hybrid test timing is optimal**: Both sides effectively concede that pure co-location and pure concentration have weaknesses. The convergent position is: unit tests co-located with implementation (catching defects early in crypto and token logic), integration and security tests concentrated in a validation phase (testing the assembled system). This captures Opus's early-defect-detection advantage and Haiku's settled-interface advantage.

2. **Security needs both distributed validation AND a review milestone**: Opus's holistic review and Haiku's early validation are complementary, not contradictory. The convergent position is: validate individual security controls when they are built (Haiku's approach), then conduct a formal security review milestone before release (Opus's Phase 6 reframed as a review, not a construction phase).

3. **API contracts should be defined before implementation**: Variant A's rebuttal did not effectively counter the contract-first advantage. Even on a single team, contracts-as-test-targets provide value. The convergent position favors Haiku's Phase 2 contract definition.

4. **Rollback rehearsal deserves its own task**: Variant A's argument that rollback is "end-to-end and belongs in regression" was weakened by Variant B's point about prioritization risk. The convergent position favors an explicit rollback rehearsal task.

5. **Email interface should be defined early**: Both sides agree the implementation can be deferred; the dispute was about when to define the interface. Haiku's argument about surfacing procurement lead time was not effectively rebutted.

### Remaining Disputes (No Convergence)

1. **Component count (11 vs 17)**: This remains genuinely unresolved. The answer depends on team size, which neither variant can determine from the spec. For a 2-person team, 17 components is over-engineered. For a 5-person team with ownership boundaries, 17 is appropriate. **Resolution requires team context.**

2. **Migration granularity (3 separate vs 2 atomic)**: Both rebuttals landed. Opus's surgical rollback benefit is real but rare. Haiku's "future changes get new migrations regardless" rebuttal is valid. **Resolution depends on operational maturity** — teams comfortable with migration management benefit from granularity; teams newer to it benefit from simplicity.

3. **Refresh token schema richness**: Opus's YAGNI argument is sound for strict v1.0 scoping. Haiku's "add columns to empty tables now vs populated tables later" argument is sound for operational pragmatism. **Resolution depends on whether security incident investigation is a stated organizational priority.** If the security team expects forensic capability, add the columns. If not, defer.

4. **Timeline precision**: Irreconcilable difference in estimation philosophy. Opus optimizes for planability; Haiku optimizes for honesty. Neither is wrong — they serve different audiences (sprint planning vs executive communication). **Both estimates should be presented** with the critical path diagram from Opus and the uncertainty acknowledgment from Haiku.

5. **Phase count (7 vs 5)**: Neither side convincingly demonstrated that their phase count is superior. The real question is milestone frequency preference, which is a team process decision, not an architectural one. **Resolution requires team input on preferred checkpoint cadence.**

6. **Integration documentation placement**: Both approaches have merit. Global integration maps aid architectural understanding; per-phase integration notes aid daily development. **The optimal approach is both** — a brief global wiring overview (Opus Section 2 style) plus per-phase integration notes (Haiku style) — but this was not conceded by either side during debate.

### Synthesis Recommendation

A merged roadmap should adopt:
- **From Opus**: 7-phase structure (finer gates), co-located unit tests, critical path diagram, health check in Phase 1, multi-developer timeline estimate
- **From Haiku**: Contract-first API definition, explicit rollback rehearsal task, PasswordResetRepository for pattern consistency, OQ tracking as tasks, early email interface definition, per-phase integration notes (supplementing a global overview), distributed SC validation with evidence linking, `revoked_at` timestamp over boolean (zero-cost improvement)
- **Deferred to team decision**: Component count (11 vs 17), migration granularity, `replaced_by_token_id` and client metadata columns, phase checkpoint cadence
