---
total_diff_points: 14
shared_assumptions_count: 16
---

## Shared Assumptions and Agreements

Both variants agree on these 16 foundational decisions:

1. **Architecture**: Stateless REST with RS256-signed JWTs (15min access, 7d refresh), Redis-backed refresh revocation, no server-side sessions
2. **Data stores**: PostgreSQL 15+ (users, audit), Redis 7+ (refresh tokens), SendGrid (email)
3. **Password security**: bcrypt cost-12, <500ms hash time, no raw password persistence/logging
4. **API surface**: Same 6 endpoints (login, register, me, refresh, reset-request, reset-confirm) with identical rate limits
5. **Compliance**: GDPR consent at registration, SOC2 12-month audit logging, NIST SP 800-63B password storage, data minimization
6. **Components**: Same 9+ components (AuthService, TokenManager, JwtService, PasswordHasher, UserRepo, AuthProvider, LoginPage, RegisterPage, ProfilePage, PasswordResetPage, EmailService)
7. **Rollout strategy**: Feature-flagged 3-stage (alpha → 10% beta → 100% GA) with AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH flags
8. **Infrastructure sizing**: 3→10 pods at CPU>70%, pg-pool 100→200, Redis 1GB→2GB
9. **Success criteria**: Same 10 metrics with identical targets (login p95 <200ms, uptime 99.9%, registration >99%, conversion >60%, etc.)
10. **Risks**: Same 7 risks with identical severity ratings
11. **Open questions**: Same 8 OQs, same blocking assessments
12. **External dependencies**: Same 7 (PostgreSQL, Redis, Node 20, bcryptjs, jsonwebtoken, SendGrid, frontend routing)
13. **Business impact**: $2.4M revenue, SOC2 Q3 deadline, personalization roadmap dependency
14. **Personas**: Alex (end user), Jordan (admin), Sam (API consumer)
15. **Rollback triggers**: p95>1000ms/5min, error>5%/2min, Redis failures>10/min, data corruption
16. **Test pyramid**: Same 6 test cases (TEST-001 through TEST-006) with same scope and tooling (testcontainers, Playwright, Jest mocks)

## Divergence Points

### 1. Phase granularity — 7 phases vs 4 phases
- **Opus**: 7 fine-grained phases (Infrastructure → Backend → API → Frontend → Compliance/Ops → Testing → Migration)
- **Haiku**: 4 consolidated phases (Security+Contracts+Persistence → Core Flows+API → Frontend+Admin+QA → Rollout+Ops+Validation)
- **Impact**: Opus provides clearer checkpoint boundaries and easier progress tracking. Haiku reduces coordination overhead and allows tighter coupling of related work (e.g., tests alongside the code they validate).

### 2. Total duration — 14 weeks vs 11 weeks
- **Opus**: 14 weeks (1.5+2+1.5+1.5+1.5+1.5+4)
- **Haiku**: 11 weeks (2+3+2+4)
- **Impact**: 3-week delta. Haiku achieves compression by parallelizing work that Opus sequences (compliance alongside frontend, testing alongside implementation). Whether achievable depends on team size and cross-skill availability.

### 3. Task row count — 52 vs 83
- **Opus**: 52 task rows across 7 phases
- **Haiku**: 83 task rows across 4 phases
- **Impact**: Haiku embeds open questions, risks, success criteria, and dependency provisioning as explicit tracked tasks. Opus keeps these as separate reference sections. Haiku's approach makes work visible in the task tracker but inflates the row count with gates and validation items.

### 4. Compliance timing — Phase 5 (post-frontend) vs Phase 1 (pre-implementation)
- **Opus**: Compliance in dedicated Phase 5 after all functional work is complete
- **Haiku**: Security and compliance constraints ratified in Phase 1, audit persistence wired in Phase 2
- **Impact**: Haiku's approach prevents late-stage compliance surprises (e.g., discovering the consent field requires schema changes after frontend is built). Opus risks rework if compliance requirements affect schema or component contracts.

### 5. Open question resolution — reference table vs gate tasks
- **Opus**: OQs listed in a standalone table at the end; blocking phase noted but no explicit resolution task
- **Haiku**: OQs embedded as explicit gate tasks (OQ-001 through OQ-008) with acceptance criteria, effort, and priority within the phase they block
- **Impact**: Haiku makes OQ resolution trackable and blocks dependent work explicitly. Opus relies on process discipline to ensure OQs are resolved before their blocking phase begins.

### 6. Risk mitigation — separate section vs inline tasks
- **Opus**: Risks in a standalone assessment table with mitigation descriptions
- **Haiku**: Risks as Phase 4 tasks (R-001 through R-007) with IDs, acceptance criteria, effort, and dependencies
- **Impact**: Haiku makes risk mitigation visible as scheduled work with clear ownership. Opus treats risks as contextual guidance rather than deliverables, risking "acknowledge but don't act" patterns.

### 7. Success criteria validation — narrative vs explicit gates
- **Opus**: SC-001 through SC-010 in a reference table; validation method and phase noted
- **Haiku**: SC-001 through SC-010 as explicit gate tasks in Phase 4 with dependencies, effort, and AC
- **Impact**: Same tradeoff as risks — Haiku ensures validation is scheduled work; Opus relies on someone remembering to check.

### 8. Component scaffolding strategy — full build vs skeleton-first
- **Opus**: Full component implementation in Phase 2 (COMP-001 through COMP-005 built to completion)
- **Haiku**: Skeleton AuthService and TokenManager in Phase 1 (COMP-001, COMP-002 as scaffolds), full implementation in Phase 2
- **Impact**: Haiku's skeleton approach enables earlier integration point validation and interface contract testing. Opus's approach is simpler but delays integration discovery.

### 9. Logout and admin audit viewer — open questions vs design tasks
- **Opus**: Logout (OQ-006) and admin viewer (OQ-007) noted as open questions only
- **Haiku**: Explicit design tasks — COMP-010 (logout coordination) and COMP-011 (audit log viewer) — scaffolded in Phase 1 with AC
- **Impact**: Haiku proactively addresses PRD-scope gaps, ensuring route structure accounts for these features even if implementation is deferred. Opus defers entirely, risking architectural rework when these are eventually added.

### 10. Testing placement — dedicated phase vs co-located
- **Opus**: Dedicated Phase 6 (1.5 weeks) after all compliance/observability work
- **Haiku**: Tests (TEST-001 through TEST-006) co-located in Phase 3 alongside frontend development
- **Impact**: Opus's dedicated phase ensures comprehensive coverage but delays feedback. Haiku's co-location enables faster defect discovery but may compress QA if frontend work runs long.

### 11. Timeline specificity — relative weeks vs absolute dates
- **Opus**: "Week 1" through "Week 14" with no calendar dates
- **Haiku**: Absolute dates (2026-04-15 through 2026-06-30)
- **Impact**: Haiku's dates enable concrete resource planning and stakeholder communication. Opus's relative timeline requires a separate scheduling exercise.

### 12. Dependency provisioning — implicit vs explicit tasks
- **Opus**: Dependencies listed in a reference table; provisioning assumed as prerequisites
- **Haiku**: DEP-001 through DEP-007 as explicit Phase 1 tasks with AC and effort estimates
- **Impact**: Haiku prevents the common failure mode where "assumed provisioned" dependencies aren't actually ready. Adds tracking overhead but reduces risk of Phase 1 blockers.

### 13. Team ownership model — risk-table owners vs dedicated section
- **Opus**: Owner column in risk table only (auth-team, platform-team, etc.)
- **Haiku**: Dedicated "Teaming and ownership" section mapping teams to domains
- **Impact**: Haiku provides clearer RACI-style accountability. Opus's ownership is fragmented across tables.

### 14. Effort sizing scale — S/M/L/XL vs S/M/L
- **Opus**: Uses XL for AuthService orchestrator (COMP-001) and E2E test (TEST-006)
- **Haiku**: Caps at L; no XL designations
- **Impact**: Opus's XL flag signals tasks that may need decomposition. Haiku either disagrees on complexity or absorbs it into the broader phase structure.

## Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Phase checkpoint clarity**: 7 discrete milestones with explicit entry/exit criteria make progress measurement unambiguous
- **Integration point documentation**: Per-phase integration tables with "Wired" vs "Consumed By" columns trace exactly when artifacts are created vs consumed
- **Executive summary depth**: Explicit critical path notation (DM-001 → COMP-005 → ...), cost estimates ($450/mo), and persona-driven sequencing rationale

### Haiku is stronger in:
- **Actionability**: Every open question, risk, success criterion, and dependency is a tracked task with ID, AC, effort, and priority — nothing falls through the cracks
- **Compliance-first sequencing**: Security and compliance constraints resolved in Phase 1 before any implementation begins, eliminating late-stage rework risk
- **Concrete scheduling**: Absolute dates enable stakeholder commitments and resource blocking
- **PRD gap coverage**: Proactively designs logout and admin viewer components rather than deferring them as questions
- **Compression efficiency**: Achieves 3 fewer weeks by parallelizing work that Opus unnecessarily sequences

## Areas Requiring Debate to Resolve

1. **4-phase vs 7-phase structure**: Is the coordination overhead of 7 phases justified by clearer checkpoints, or does Haiku's 4-phase consolidation better reflect how a single team actually works? Depends on team size and management cadence.

2. **Compliance timing**: Should compliance controls be validated before implementation (Haiku) or after functional completeness (Opus)? Haiku's approach is safer but front-loads effort on constraints that may shift. Opus assumes stable compliance requirements.

3. **Testing co-location vs dedicated phase**: Should tests run alongside the code they validate (Haiku) or in a dedicated QA phase (Opus)? Co-location is modern practice but risks scope compression. Dedicated phase guarantees time but delays feedback loops.

4. **11 weeks vs 14 weeks**: Is Haiku's 3-week compression realistic or does it assume parallelism that a single auth-team cannot achieve? The answer depends on team size, cross-functional availability, and whether the compliance-first approach actually eliminates Opus's sequential dependencies.

5. **Task granularity**: Haiku's 83 rows vs Opus's 52 — does embedding gates as tasks improve execution rigor, or does it create tracking noise that obscures the actual implementation work? Teams with strong project management tooling benefit from Haiku; teams relying on the roadmap as a narrative guide benefit from Opus.

6. **Skeleton-first components**: Does scaffolding AuthService and TokenManager in Phase 1 yield meaningful early integration validation, or is it premature when the dependent services (PasswordHasher, UserRepo) aren't yet implemented? The answer depends on whether interface contracts are stable enough to scaffold against.
