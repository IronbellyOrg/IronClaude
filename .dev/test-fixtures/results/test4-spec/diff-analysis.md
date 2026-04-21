---
total_diff_points: 18
shared_assumptions_count: 16
---

# Comparative Diff Analysis: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Shared Assumptions and Agreements

Both variants agree on the following foundational elements:

1. **Spec source and complexity**: Both derive from `test-spec-user-auth.md` with complexity score 0.6 (MEDIUM), architect persona
2. **Functional scope**: Five FR requirements (FR-AUTH.1–5) covering login, registration, token refresh, profile retrieval, and password reset
3. **NFR scope**: Three NFRs — p95 latency < 200ms, 99.9% uptime, bcrypt cost factor 12
4. **Database model**: Two new tables (`users`, `refresh_tokens`) with the same column semantics (UUID PKs, hashed tokens, nullable revocation timestamps)
5. **Cryptographic choices**: RS256 for JWT signing, bcrypt for password hashing, SHA-256 for refresh token storage
6. **Open questions identified**: Both surface the same 8 OQs (sync/async email, refresh token cap, latency conflict, lockout policy, deletion revocation, audit logging, email interface, key rotation)
7. **Risk register**: Identical 6 risks (R-1 through R-6) with substantially similar severity assessments
8. **Success criteria**: Both validate against the same 14 SC gates (SC-1 through SC-14)
9. **v1 scope boundary**: Both explicitly exclude OAuth, MFA, RBAC, and social login
10. **Bcrypt/latency conflict**: Both flag this as the single most critical architectural decision and require resolution before NFR signoff
11. **Token rotation model**: Both specify rotation-on-every-refresh with replay detection triggering full user session revocation
12. **Middleware pattern**: Both wire auth middleware for Bearer extraction, JWT verification, user context attachment
13. **Email dependency risk**: Both identify undefined email service as a blocker for FR-AUTH.5
14. **Library dependencies**: Both name `jsonwebtoken` and `bcrypt` as the two library dependencies
15. **Feature flag rollback**: Both require `AUTH_SERVICE_ENABLED` toggle for gradual rollout and instant rollback
16. **Migration reversibility**: Both require tested up/down migrations with idempotent rollback

---

## 2. Divergence Points

### D-1: Phase Structure

| Aspect | Opus | Haiku |
|--------|------|-------|
| Phase count | 6 phases (0–5) | 3 phases (1–3), Phase 4 implied |
| Granularity | Each functional area gets its own phase (Registration+Login, Token+Profile, Password Reset) | Features consolidated into a single "Core Implementation" phase |

**Impact**: Opus's finer phases create natural review gates between functional areas, making it easier to course-correct mid-stream. Haiku's coarser phases reduce ceremony but risk late discovery of integration issues between features.

---

### D-2: Contract-First vs Implementation-First

| Aspect | Opus | Haiku |
|--------|------|-------|
| Approach | Implements services directly in Phase 0 (COMP-001 = "Implement PasswordHasher") | Defines contracts/interfaces first (COMP-006 = "Define password hasher service contract"), implements later in Phase 2 |
| Task naming | "Implement X" | "Define X contract" → "Implement X" |

**Impact**: Haiku's contract-first approach enforces interface stability before coding begins, reducing rework when multiple engineers work in parallel. Opus's approach gets to working code faster but may require interface changes once integration reveals mismatches.

---

### D-3: Task Count and Decomposition Style

| Aspect | Opus | Haiku |
|--------|------|-------|
| Total tasks | 92 | ~130 (40 + 40 + 50) |
| Decomposition | Implementation-oriented (one task = one working piece) | Separation of design, implement, wire, and bind steps |
| Explicit wiring tasks | Route registration only (API-001 through API-006) | Route wiring (API-001.W1–007.W1), middleware wiring (MW-001, MW-002), DI binding (DI-001–005) |

**Impact**: Haiku's explicit wiring/binding tasks make integration debt visible and trackable. Opus assumes wiring happens implicitly within implementation tasks, which is simpler but can hide integration gaps.

---

### D-4: Dependency Injection Visibility

| Aspect | Opus | Haiku |
|--------|------|-------|
| DI tasks | None — services are created and consumed inline | 5 explicit DI binding tasks (DI-001 through DI-005) |
| Container concept | Implicit — services exist as imports | Named `SecurityServiceContainer` with explicit bindings |

**Impact**: Haiku's approach is more rigorous for teams using IoC containers. Opus's approach is more practical for smaller codebases where direct imports suffice.

---

### D-5: Open Question Resolution Timing

| Aspect | Opus | Haiku |
|--------|------|-------|
| Resolution phase | All 8 OQs resolved in Phase 0 before any implementation | OQs addressed as decisions (DEC-001–004) in Phase 1, formally closed with evidence in Phase 3 |
| Closure evidence | Decision documented with stakeholder sign-off | Decision + implementation evidence + validation evidence required |

**Impact**: Opus front-loads all ambiguity resolution, which is faster if stakeholders are available. Haiku's evidence-based closure is more rigorous but may delay formal closure of questions that have clear answers early.

---

### D-6: Testing Distribution

| Aspect | Opus | Haiku |
|--------|------|-------|
| Strategy | Tests co-located with implementation phases (TEST-001–004 in Phase 1, TEST-005–007 in Phase 2, etc.) | All testing consolidated in Phase 3 (TEST-001 through TEST-022) |
| Test count | ~15 test tasks distributed across phases | 22 test tasks + 14 SC validations + 6 risk reviews in one phase |

**Impact**: Opus's co-located testing catches bugs earlier and keeps test-to-implementation feedback loops short. Haiku's consolidated testing risks a large "test writing sprint" that could bottleneck release if defects surface late.

---

### D-7: Named Integration Artifacts

| Aspect | Opus | Haiku |
|--------|------|-------|
| Integration naming | File-path based (`src/middleware/index.ts`, `src/routes/index.ts`) | Architectural abstractions (`AuthRouteRegistry`, `SecurityServiceContainer`, `AuthMiddlewareChain`, `AuthTestMatrix`, `OperationalReadinessChecklist`) |

**Impact**: Opus's file-path naming is immediately actionable — a developer knows exactly where to look. Haiku's abstraction-level naming is better for architectural documentation but requires mapping to actual files during implementation.

---

### D-8: Feature Flag Introduction Timing

| Aspect | Opus | Haiku |
|--------|------|-------|
| Introduced in | Phase 5, task OPS-006 | Phase 1, task OPS-003 |

**Impact**: Haiku's early introduction means the flag is available throughout development for testing rollback behavior. Opus's late introduction means rollback testing can only happen in the final phase, and earlier phases run without the safety net.

---

### D-9: Route Naming Convention

| Aspect | Opus | Haiku |
|--------|------|-------|
| Password reset routes | `POST /auth/reset-request`, `POST /auth/reset-confirm` | `POST /auth/password-reset/request`, `POST /auth/password-reset/confirm` |
| Endpoint count | 6 endpoints (API-001 through API-006) | 7 route skeletons (API-001 through API-007) — separate group registration |

**Impact**: Haiku's nested `/password-reset/` prefix is more RESTful and self-documenting. Opus's flatter naming is more concise. Minor difference — but affects API documentation and client SDKs.

---

### D-10: Timeline Estimates

| Aspect | Opus | Haiku |
|--------|------|-------|
| Total estimate | ~7.5 weeks (fixed) | ~5.5–7 weeks (range) |
| Parallelization opportunity | Explicitly noted: Phase 2+3 concurrent → 6.5 weeks | Not explicitly identified |
| Confidence in estimate | Single point | Range with lower/upper bounds |

**Impact**: Haiku's range estimate is more honest about uncertainty. Opus's single point with explicit parallelization opportunity is more actionable for project planning.

---

### D-11: Resource Allocation Specificity

| Aspect | Opus | Haiku |
|--------|------|-------|
| FTE allocation | Specific: 1 BE, 0.5 Security, 0.5 QA, 0.25 DevOps | Role list without FTE numbers |
| Phase coverage mapping | Explicit per-role phase coverage | Roles described by responsibility only |

**Impact**: Opus's FTE allocation is directly usable for staffing decisions. Haiku's approach is more flexible but leaves resourcing ambiguous.

---

### D-12: Frontmatter Richness

| Aspect | Opus | Haiku |
|--------|------|-------|
| Fields | 8 fields (spec_source, complexity, persona, date, generator, phases, tasks, IDs) | 3 fields (spec_source, complexity, persona) |
| Traceability | `extraction_ids_preserved: 55`, `derived_entity_ids: 37` | No ID traceability metadata |

**Impact**: Opus's frontmatter enables automated validation pipelines to verify spec-to-roadmap traceability. Haiku's minimal frontmatter requires manual verification.

---

### D-13: Deployment Phase Existence

| Aspect | Opus | Haiku |
|--------|------|-------|
| Dedicated deployment phase | Yes — Phase 5 with 18 tasks covering staging, production, feature flag, monitoring | No — deployment implied after Phase 3 validation |
| Staging smoke tests | Explicit task (OPS-007) | Not present |
| Production cutover | Explicit task (OPS-008) with canary percentage | Not present |

**Impact**: Opus provides a complete delivery playbook. Haiku assumes deployment operations are handled outside the roadmap scope.

---

### D-14: Milestone Checkpoint Model

| Aspect | Opus | Haiku |
|--------|------|-------|
| Checkpoints | Phase-level milestones with prose descriptions | 4 named checkpoints (A–D) at specific points including mid-phase |
| Mid-phase check | None | Checkpoint B at mid-Phase 2 (registration/login/refresh functional) |

**Impact**: Haiku's mid-phase checkpoint catches problems earlier within the largest phase. Opus relies on per-phase boundaries only.

---

### D-15: Executive Summary Framing

| Aspect | Opus | Haiku |
|--------|------|-------|
| Style | Action-oriented: critical path, key risks, quantified metrics | Principle-oriented: 5 architectural priorities, recommended delivery stance |
| Release gate | Implicit via SC criteria | Explicit "Release gate recommendation" section with 5 boolean conditions |

**Impact**: Opus's summary is more useful for project managers tracking progress. Haiku's summary is more useful for architects ensuring quality posture.

---

### D-16: Test Strategy Architecture

| Aspect | Opus | Haiku |
|--------|------|-------|
| Strategy definition | Implicit — 3 tiers described in Section 6 | Explicit tasks: TEST-ARCH-001 (test strategy matrix), TEST-ARCH-002 (test fixtures) |
| Test fixtures | Not explicit | Dedicated task for fixture design covering users, sessions, revoked/expired tokens, locked accounts |

**Impact**: Haiku treats test architecture as a first-class deliverable. Opus assumes test structure emerges from implementation.

---

### D-17: Cookie Security Handling

| Aspect | Opus | Haiku |
|--------|------|-------|
| Cookie configuration | Mentioned in passing (FR-AUTH.1a: "refresh_token set as httpOnly cookie") | Dedicated task OPS-005: "Implement secure cookie configuration for refresh tokens" |

**Impact**: Haiku explicitly tracks cookie security as a deliverable, reducing risk of misconfigured security attributes. Opus subsumes it within token issuance.

---

### D-18: Architect Recommendations Section

| Aspect | Opus | Haiku |
|--------|------|-------|
| Present | No — recommendations embedded in risk/executive sections | Yes — 5 explicit numbered recommendations at document end |
| Content | Distributed across sections | Consolidated, scannable, and actionable |

**Impact**: Haiku's standalone recommendations section is easier for decision-makers to find and act on. Opus requires reading the full document to extract architectural guidance.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:

- **Deployment completeness**: Full staging → production → monitoring pipeline with explicit tasks. Haiku stops at validation.
- **Resource planning**: FTE allocations and external dependency tables with delay-risk assessment are directly usable for project planning.
- **Frontmatter traceability**: ID preservation counts enable automated spec-to-roadmap validation.
- **Parallelization analysis**: Explicit identification of Phase 2/3 overlap opportunity with quantified schedule compression (7.5 → 6.5 weeks).
- **Test co-location**: Tests alongside implementation reduces feedback latency and catches issues earlier.
- **Spec ID preservation**: 55 extracted + 37 derived IDs maintain clear lineage to the source spec.

### Haiku is stronger in:

- **Architectural rigor**: Contract-first approach, named integration artifacts, explicit DI bindings, and wiring tasks make the architecture more visible and auditable.
- **Early safety nets**: Feature flag in Phase 1 (not Phase 5) provides rollback capability throughout development.
- **Risk/decision formalization**: Separate DEC-001–004 tasks with evidence-based closure in Phase 3 create a decision audit trail.
- **Test architecture**: Dedicated test strategy and fixture design tasks treat testing as a first-class architectural concern.
- **Release gate clarity**: Explicit 5-condition release gate recommendation is unambiguous.
- **Cookie security visibility**: Dedicated task prevents security-critical configuration from being buried in implementation.
- **Milestone granularity**: Mid-phase checkpoint (B) catches integration problems earlier within the largest phase.

---

## 4. Areas Requiring Debate to Resolve

1. **Test timing**: Should tests be co-located with implementation (Opus) or consolidated in a validation phase (Haiku)? The answer depends on team size — small teams benefit from co-location; larger teams with dedicated QA may prefer consolidated testing.

2. **Contract-first vs implementation-first**: Is the overhead of defining interfaces before implementing justified for a team of 1–2 backend engineers? Contract-first pays off at 3+ engineers; for smaller teams it may be ceremony without benefit.

3. **Phase granularity**: 6 phases vs 3 phases is a governance question. More phases = more review gates = more calendar time but less rework. The right answer depends on organizational review cadence.

4. **Deployment in scope or out**: Should the roadmap cover deployment operations (Opus) or treat them as a separate operational concern (Haiku)? If the team owns deployment, it should be in the roadmap.

5. **Named abstractions vs file paths**: `SecurityServiceContainer` vs `src/middleware/index.ts` — which naming convention better serves the team? Depends on whether the audience is architects or implementers.

6. **Timeline precision**: Fixed 7.5-week estimate (Opus) vs 5.5–7-week range (Haiku). Stakeholders typically want a number; engineers typically want a range. The right framing depends on the audience.

7. **OQ resolution timing**: All-upfront (Opus) vs progressive-with-evidence (Haiku). Front-loading is faster when stakeholders are engaged. Progressive closure is safer when decisions benefit from implementation learning.

8. **Wiring task visibility**: Are explicit DI/wiring tasks (Haiku's 12 extra tasks) valuable tracking overhead or unnecessary granularity? This depends on whether integration bugs have historically been a problem for the team.
