---
convergence_score: 0.62
rounds_completed: 2
---

# Structured Adversarial Debate: Opus (7-phase/14-week) vs Haiku (4-phase/11-week)

## Round 1: Initial Positions

### Divergence Cluster A: Structure and Granularity (Phases, Rows, Duration)

**Variant A (Opus):**
Seven phases with 52 task rows over 14 weeks is the correct structure for a security-critical service. Each phase has an unambiguous entry/exit gate — when the team finishes Phase 3, there is zero ambiguity about whether API hardening is done. The 14-week timeline is honest: it sequences compliance after functional completeness because compliance validation requires a working system to validate against. Fewer task rows means less tracking noise — the 52 rows are *all implementation work*, not process artifacts masquerading as deliverables. A team managing 83 rows in a tracker will spend measurable hours grooming gate tasks that could be checklist items in a phase exit review.

**Variant B (Haiku):**
Four phases with 83 rows over 11 weeks reflects how a single auth-team actually ships. The 7-phase structure forces artificial handoff ceremonies between phases that share the same team and the same codebase. Phase 2 (Core Backend) and Phase 3 (API Layer) in Opus are one continuous implementation effort — splitting them creates a checkpoint that exists for reporting, not for engineering. The 83 rows are higher because every open question, risk, dependency, and success criterion is a tracked task with an ID, acceptance criteria, and effort estimate. This is not inflation — it is the difference between "we acknowledged the risk" and "we scheduled the mitigation." The 3-week compression comes from parallelizing compliance with implementation (because compliance *constraints* can be validated on schemas and contracts, not just running systems) and co-locating tests with the code they validate.

### Divergence Cluster B: Compliance Timing

**Variant A (Opus):**
Compliance belongs in Phase 5, after functional completeness, for three reasons. First, GDPR consent capture and SOC2 audit logging are *instrumentation on top of working flows* — you cannot validate that audit events fire correctly if the auth flows don't exist yet. Second, front-loading compliance effort in Phase 1 risks building against compliance requirements that may shift during implementation (OQ-008 was already a retention conflict). Third, a dedicated compliance phase ensures focused security review without competing for attention with feature development. The risk of late-stage rework is mitigated by defining compliance *requirements* early (DM-003 schema in Phase 1) while deferring *validation* to Phase 5.

**Variant B (Haiku):**
Compliance-first is non-negotiable for a SOC2-auditable service. Opus's Phase 5 placement is the number one cause of late-stage rework in enterprise auth projects: you build the schema without the consent field, wire the frontend without the consent checkbox, then discover in "compliance phase" that you need a schema migration, a new form field, and a re-test of registration. Haiku resolves this by ratifying NFR-COMP-001 (GDPR consent), NFR-COMP-003 (no raw password persistence), and NFR-COMP-004 (data minimization) in Phase 1 *as constraints on the schema and contracts*, not as instrumentation on running code. The audit persistence (NFR-COMP-002) is wired in Phase 2 alongside the auth flows that emit audit events. This is not premature — it is constraint-driven design. OQ-008 (retention conflict) is resolved as a Phase 1 gate task precisely because it affects schema sizing.

### Divergence Cluster C: Actionability — OQs, Risks, Success Criteria, Dependencies

**Variant A (Opus):**
Open questions, risks, and success criteria are *governance artifacts*, not implementation tasks. Embedding them as rows in the task tracker conflates two concerns: "what we build" and "what we monitor." Opus's approach — standalone tables with blocking-phase annotations — keeps the task list focused on deliverables while providing a clear reference for program managers. A team that needs to check whether OQ-004 is resolved looks at the OQ table; they don't scroll through 83 rows hunting for a gate task. This separation of concerns is standard in mature project management: the risk register is not the sprint backlog.

**Variant B (Haiku):**
The "separation of concerns" argument is exactly why OQs and risks fall through the cracks. Opus's OQ table says OQ-004 blocks Phase 2, but there is no task in Phase 1 or Phase 2 that says "resolve OQ-004." The resolution depends on someone reading a reference table and creating a task ad hoc. Haiku makes this explicit: OQ-004 is a Phase 1 gate task with acceptance criteria ("per-user-limit:decided; eviction-policy:defined; UX-impact:documented"), effort (S), and priority (P0). It blocks COMP-002 (TokenManager) by dependency. This is not conflation — it is the difference between documenting a risk and scheduling its mitigation. The same applies to R-001 through R-007: Opus describes mitigations in prose; Haiku assigns them IDs, effort, dependencies, and acceptance criteria in Phase 4. The question is not whether governance and implementation should be separated — it is whether a task that says "mitigate token theft via XSS" with clear AC is a governance artifact or a deliverable. It is a deliverable.

### Divergence Cluster D: Scaffolding, Testing, Timeline, and Ownership

**Variant A (Opus):**
Full component implementation in Phase 2 is preferable to skeleton-first for a 9-component system where 5 of the components are backend modules with clear interfaces. Scaffolding AuthService and TokenManager as skeletons in Phase 1 when their dependencies (PasswordHasher, UserRepo) don't exist yet produces stubs that test nothing meaningful. Dedicated testing in Phase 6 guarantees uncompressed QA time — co-locating tests with frontend development in Phase 3 means QA gets squeezed when the frontend runs long (which it always does). Relative-week timelines are deliberately flexible: a team can anchor Week 1 to any start date without rewriting the roadmap. The risk/owner column in the risk table is sufficient for a single-team project; a dedicated ownership section is overhead for a project with one primary owner (auth-team).

**Variant B (Haiku):**
Skeleton-first scaffolding in Phase 1 validates interface contracts before full implementation. When COMP-001 (AuthService) and COMP-002 (TokenManager) exist as skeletons with typed interfaces, Phase 2 implementers code against a contract, not against assumptions. This catches integration mismatches 3 weeks earlier. Co-located testing is modern engineering practice — writing TEST-004 (integration test registration persists) in the same phase as COMP-007 (RegisterPage) means defects surface immediately, not 4 weeks later in a dedicated QA phase where context has evaporated. Absolute dates (2026-04-15 through 2026-06-30) are mandatory for stakeholder communication — the SOC2 Q3 deadline is a calendar date, not "Week 14." A dedicated teaming section mapping auth-team, frontend team, security/compliance, and platform/ops to specific domains prevents the "who owns this?" ambiguity that Opus's fragmented owner column creates.

## Round 2: Rebuttals

### Variant A (Opus) Rebuts Variant B (Haiku):

**On compliance timing:** Haiku claims compliance-first prevents rework, but the consent field example is a strawman. Opus defines DM-001 (UserProfile schema) in Phase 1 — the schema *already includes* all fields needed for compliance. The Phase 5 compliance work is *validation and instrumentation*, not schema changes. Haiku's Phase 1 includes 26 tasks — nearly a third of its total roadmap — creating a front-loaded bottleneck that delays all implementation by 2 weeks. If any Phase 1 gate task (OQ-001, OQ-004, OQ-008) slips, the entire roadmap shifts right. Opus's approach lets implementation begin while governance questions are resolved in parallel.

**On actionability:** Haiku's 83 rows include 10 success-criteria validation tasks (SC-001 through SC-010) in Phase 4, each with "M" effort. These are not deliverables — they are metric checks that take 15 minutes each. Assigning them M effort and tracking them as tasks is theater. The same applies to dependency provisioning: DEP-003 ("Pin Node.js 20 LTS runtime," effort S) is `nvm use 20` — it does not need an ID, acceptance criteria, and a row in the tracker. Haiku's actionability comes at the cost of signal-to-noise ratio. When everything is a tracked task, nothing stands out.

**On 11-week compression:** Haiku claims 3 weeks of compression through parallelism, but its Phase 2 is 3 weeks (vs Opus's combined Phase 2+3 at 3.5 weeks) while covering the same scope *plus* API contracts, performance tuning, uptime establishment, and SOC2 audit persistence. This is not compression through parallelism — it is compression through underestimation. The 11-week timeline assumes zero slip on any Phase 1 gate task, zero frontend scope creep in Phase 3, and perfect parallelism between compliance and implementation. Opus's 14 weeks includes realistic buffer for the security-critical nature of authentication work.

**On skeleton scaffolding:** Skeleton AuthService and TokenManager with no implemented dependencies are type-checked interfaces, not validated contracts. You cannot integration-test a skeleton against a PasswordHasher that doesn't exist. The scaffolds will be rewritten when the real implementations surface edge cases (error handling, retry logic, audit event emission) that the skeleton didn't anticipate. This is premature abstraction — the exact anti-pattern the project principles warn against.

### Variant B (Haiku) Rebuts Variant A (Opus):

**On compliance timing:** Opus's rebuttal that "the schema already includes all fields" proves Haiku's point — if compliance shapes the schema, then compliance constraints must be ratified *before* the schema is frozen. Opus freezes the schema in Phase 1 but validates compliance in Phase 5. What happens when Phase 5 compliance validation discovers that the AuditLog schema needs an additional field for SOC2 control mapping? A schema migration in Week 8 that propagates through the audit persistence layer, the admin viewer, and the test suite. Haiku prevents this by making NFR-COMP-001/003/004 Phase 1 tasks with explicit AC that constrain DM-001/DM-003. The 26-task Phase 1 is not a bottleneck — it is 2 weeks of foundation work that includes provisioning (7 tasks), gate resolution (4 tasks), security config (4 tasks), compliance constraints (3 tasks), schemas (3 tasks), module scaffolds (4 tasks), and PRD gap designs (2 tasks). These parallelize naturally across infra, security, and backend roles.

**On signal-to-noise:** Opus argues that SC-001 through SC-010 as tasks is "theater." But Opus's own SC table says "Validation Method: APM tracing + k6 load test" and "Phase: Phase 3 (NFR-PERF-001)" — who runs the k6 test? When? With what acceptance criteria? Opus leaves this implicit; Haiku makes it explicit. The "Pin Node.js 20 LTS" task (DEP-003) is trivial in isolation, but its AC includes "drift:blocked" — ensuring CI prevents version drift. That is not `nvm use 20`; it is a CI configuration change with a verification step. Small tasks with clear AC are how teams avoid the "we assumed someone handled that" failure mode. The overhead of tracking 83 rows in modern project tooling (Linear, Jira, GitHub Projects) is negligible; the overhead of discovering untracked work in Week 10 is not.

**On timeline:** Opus claims Haiku underestimates, but Opus's own Phase 6 (dedicated QA, 1.5 weeks) is the underestimation. Every modern engineering team runs tests alongside implementation. Opus's Phase 6 will discover defects introduced in Phase 2 that have propagated through Phases 3-5 — defects that co-located testing would have caught in the same sprint. The 14-week timeline is not "realistic buffer" — it is the cost of sequential compliance and deferred testing. Haiku's 11 weeks assumes a standard 4-person auth team with infra support, which is exactly the team size implied by both roadmaps' infrastructure requirements.

**On scaffolding:** The skeletons are not premature abstraction — they are interface contracts. COMP-001 (AuthService) skeleton defines `login(email, password): AuthToken`, `register(email, password, displayName): UserProfile`, and `refresh(refreshToken): AuthToken`. These signatures are stable — they come directly from the TDD's FR definitions. Phase 2 implementers code PasswordHasher.verify() knowing that AuthService.login() will call it with a specific contract. The skeleton *is* the contract. If the implementation surfaces edge cases that change the interface, that is a contract change that should be tracked, not silently absorbed.

## Convergence Assessment

### Areas of Agreement (Reached Through Debate)

| Point | Consensus |
|---|---|
| Schema design must account for compliance fields from Day 1 | Both agree DM-001/DM-003 include compliance-relevant fields in Phase 1; dispute is about when validation occurs |
| Gate tasks for blocking OQs add value | Opus concedes that OQ-004 and OQ-008 benefit from explicit resolution tasks; disputes extending this to all risks and SCs |
| Absolute dates are needed for stakeholder communication | Opus's relative weeks require a supplementary schedule; Haiku's dates are directly usable |
| Co-located testing for unit/integration is modern practice | Opus concedes unit/integration tests should run alongside implementation; maintains E2E needs dedicated time |
| Dependency provisioning tasks prevent "assumed ready" failures | DEP-001 and DEP-002 as explicit tasks with AC is reasonable; dispute is whether DEP-003 (Node.js pinning) warrants a tracked task |

### Areas of Persistent Disagreement

| Point | Opus Position | Haiku Position | Resolution Depends On |
|---|---|---|---|
| Phase count | 7 phases provide checkpoint clarity for reporting and progress measurement | 4 phases reflect actual workflow boundaries; 7 creates artificial handoffs | Team size and management reporting cadence |
| Compliance validation timing | Phase 5 (post-functional) avoids front-loading effort on potentially shifting requirements | Phase 1 constraints prevent late-stage schema rework; constraints are stable because they come from regulations | Whether compliance requirements are truly stable (regulations suggest yes) |
| Success criteria as tasks | Metric checks are not deliverables; tracking them as M-effort tasks inflates the roadmap | Untracked validation is unscheduled validation; explicit tasks prevent "we forgot to check" | Project management tooling maturity and team discipline |
| 11 vs 14 weeks | 14 weeks is honest for security-critical work with compliance gates | 11 weeks is achievable with parallel compliance and co-located testing | Team size, cross-functional availability, and whether compliance-first actually eliminates sequential dependencies |
| Risk mitigation as tasks vs prose | Prose mitigations provide context without tracker noise | Scheduled mitigations with IDs and AC ensure execution, not just acknowledgment | Historical team behavior — does this team act on risk register entries without task assignments? |
| Skeleton scaffolding | Stubs without implementations test nothing; premature abstraction risk | Interface contracts from stable TDD signatures enable early integration validation | Interface stability — if FR signatures are locked, scaffolds have value; if they shift, scaffolds are waste |

### Synthesis Recommendation

The strongest roadmap would combine:
- **Haiku's compliance-first sequencing** (regulations are stable; late-stage schema changes are expensive)
- **Haiku's gate tasks for OQs and blocking dependencies** (OQ-004, OQ-008, DEP-001, DEP-002 as tracked work)
- **Haiku's absolute dates** (SOC2 Q3 deadline demands calendar anchoring)
- **Opus's phase granularity** (5-6 phases as a compromise — merge Opus Phases 2+3, keep compliance early, keep dedicated E2E testing time)
- **Opus's separation of SC validation from task rows** (success criteria as a phase exit checklist, not individual M-effort tasks)
- **Opus's risk table format** (risks as governance with mitigation owners, not as 28 Phase 4 rows)
- **Haiku's team ownership section** (clear RACI for a multi-team effort)

The 0.62 convergence score reflects strong agreement on fundamentals (architecture, components, success targets) but genuine, unresolved disagreement on project structure that depends on team-specific context neither variant can assume.
