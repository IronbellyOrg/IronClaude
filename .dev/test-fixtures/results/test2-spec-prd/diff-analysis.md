---
total_diff_points: 14
shared_assumptions_count: 12
---

## 1. Shared Assumptions and Agreements

Both variants agree on the following foundational elements:

1. **Complexity rating**: Both score 0.6 (MEDIUM) with architect persona
2. **Technology stack**: TypeScript, PostgreSQL 15+, bcrypt (cost 12), RS256 JWT, SendGrid
3. **Token architecture**: Stateless JWT access tokens (15min TTL), refresh tokens (7d TTL) with rotation and replay detection
4. **Layered DI architecture**: AuthService → TokenManager → JwtService with PasswordHasher as parallel utility
5. **Critical path**: TokenManager is the central blocking dependency for login, refresh, and password reset
6. **Risk inventory**: Identical 7 risks with matching severity/probability assessments
7. **NFR targets**: <200ms p95, 99.9% availability, 500 concurrent requests, bcrypt ~250ms
8. **Success metrics**: Same 8 criteria with identical targets (>60% registration conversion, <200ms p95, etc.)
9. **Scope exclusions**: OAuth/OIDC, MFA, RBAC, social login, admin UI, account deletion all deferred
10. **Open questions**: Both flag #5 (audit fields), #7 (GDPR consent), and #10 (logout endpoint) as requiring immediate resolution
11. **Refresh token storage**: Both mandate httpOnly cookie with Secure + SameSite; access token in memory
12. **Password policy**: Both enforce 8-char min, 1 uppercase, 1 lowercase, 1 digit

---

## 2. Divergence Points

### D1: Phase Structure — 4 phases vs 2 phases
- **Opus**: 4 phases across 6 sprints (~14 weeks). Foundation → Core Auth → Session/Recovery → Compliance/Launch
- **Haiku**: 2 phases across 6 weeks. Foundation+Core Auth combined → Session/Profile/Reset/Compliance combined
- **Impact**: Opus's 4-phase model provides more granular go/no-go gates but implies a longer calendar timeline. Haiku's 2-phase model is more compressed and aggressive, with less intermediate validation.

### D2: Total Timeline Estimate
- **Opus**: ~14 weeks (6 two-week sprints with overlap)
- **Haiku**: ~6 weeks (36 engineer-days at ~2.8 FTE)
- **Impact**: **Major divergence.** Opus is 2.3x longer. This may reflect Opus accounting for single-threaded delivery while Haiku assumes parallel FTE allocation. Neither is wrong per se, but the gap needs reconciliation against actual team capacity.

### D3: Audit Log Table Provisioning Timing
- **Opus**: Defers audit_logs table creation to Phase 4 (compliance phase); audit logging is a late-stage concern
- **Haiku**: Pre-provisions audit_logs table in Phase 1 Week 1 (Milestone 1.1.1) and wires event dispatch incrementally
- **Impact**: Haiku's approach is architecturally stronger — capturing audit events from day one prevents a "retrofit" problem where Phase 2-3 handlers must be retroactively instrumented. Opus explicitly notes this retroactive wiring in Phase 4.

### D4: Security Review Checkpoint Placement
- **Opus**: Single security review + penetration test in Phase 4.3 (final phase, pre-launch)
- **Haiku**: Mid-stream security review at Phase 1 Week 3 (Milestone 1.5.2) as a gate before Phase 2, plus pre-production pen test
- **Impact**: Haiku's earlier checkpoint reduces the risk of discovering fundamental security flaws late. Opus defers all security validation to the end, which could force costly rework.

### D5: Logout Endpoint Placement
- **Opus**: Lists logout as Open Question #10, recommends inclusion but doesn't assign it to a specific milestone
- **Haiku**: Explicitly implements logout as Milestone 1.4.4 in Phase 1 with full acceptance criteria
- **Impact**: Haiku is more decisive here. Opus leaves it ambiguous, which could cause scope creep later.

### D6: DI Container as Explicit Deliverable
- **Opus**: Mentions injectable architecture but does not dedicate a milestone to DI container setup
- **Haiku**: Dedicates Milestone 1.1.3 to DI container implementation with explicit acceptance criteria (no circular deps, mockable services)
- **Impact**: Haiku's explicit treatment prevents the common failure mode where DI is assumed but never formally wired, causing integration issues later.

### D7: Password Policy Enforcement Location
- **Opus**: Enforces password policy at the registration endpoint level (Milestone 2.1)
- **Haiku**: Enforces password policy inside PasswordHasher itself (Milestone 1.2.1) — policy checked at hash time
- **Impact**: Haiku's approach is more defensive (policy can't be bypassed by any caller), but couples validation logic to the hashing utility. Opus's approach keeps concerns separated but requires discipline at every call site.

### D8: Password Reset Token Storage
- **Opus**: Reuses refresh_tokens infrastructure or generates tokens inline; no dedicated table mentioned
- **Haiku**: Creates a dedicated `password_reset_tokens` table (Milestone 2.3.1) with separate TTL, hash, and consumption tracking
- **Impact**: Haiku's dedicated table is cleaner and avoids conflating reset tokens with refresh tokens. Opus's approach is underspecified and could lead to schema ambiguity.

### D9: Resource/FTE Estimation Granularity
- **Opus**: Lists role categories (backend, frontend, DevOps, security, QA) without FTE numbers
- **Haiku**: Provides specific FTE allocations per role (1.0 backend lead, 0.5 support, 0.3 security, etc.) totaling ~2.8 FTE
- **Impact**: Haiku is more actionable for project planning. Opus requires a separate capacity planning exercise.

### D10: Integration Point Documentation Style
- **Opus**: Uses per-phase tables listing artifact name, type, wired components, owning phase, and consumed-by
- **Haiku**: Uses inline "INTEGRATION POINT" callout blocks with the same fields, plus a summary appendix
- **Impact**: Both are thorough. Haiku's appendix collecting all 5 registries in one place is useful for cross-cutting review. Opus's per-phase tables are easier to consume during sprint execution.

### D11: Account Lockout Handling
- **Opus**: Proposes progressive lockout (5→15min, 10→1hr, 20→admin unlock) as recommended resolution for Open Question #3
- **Haiku**: Defers account-level lockout entirely to v1.1; v1.0 only does IP-level rate limiting
- **Impact**: Opus is more opinionated but adds implementation scope. Haiku's deferral is pragmatic for v1.0 but leaves a security gap if credential stuffing targets specific accounts.

### D12: Email Dispatch Recommendation
- **Opus**: Recommends async via message queue but notes sync is acceptable for v1.0 given low volume
- **Haiku**: Recommends async (Celery/Bull/SQS) without the synchronous fallback option
- **Impact**: Minor. Opus is more pragmatic; Haiku is more architecturally pure. Both are reasonable.

### D13: Post-Launch Monitoring Plan
- **Opus**: Brief mention of post-launch monitoring for success criteria #1, #3, #4, #5
- **Haiku**: Detailed post-launch timeline (Week 1-2 monitoring, Week 4 retro, Month 2-3 SOC2, Month 6 key rotation)
- **Impact**: Haiku provides more operational continuity planning, which is valuable for handoff to an ops team.

### D14: GDPR Consent Table Design
- **Opus**: Suggests consent field in users table OR dedicated consents table (leaves decision open)
- **Haiku**: Specifies dedicated `consents` table with user_id, consent_type, timestamp, version
- **Impact**: Haiku's versioned consent table is more compliance-friendly (supports consent revocation and audit). Opus's ambiguity here could result in an inadequate schema.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Open questions analysis**: More thorough treatment with decision owners, blocking phases, and architect recommendations. The table in Section 7 is excellent.
- **Scope guardrails**: Dedicated Section 8 with explicit out-of-scope table prevents scope creep.
- **Risk notes**: Architect's commentary on Race conditions in replay detection (database-level atomicity) and the GAP-2 blocker are insightful.
- **Feature flag strategy**: Explicit `AUTH_SERVICE_ENABLED` flag with gradual rollout plan.

### Haiku is stronger in:
- **Audit logging architecture**: Pre-provisioning + incremental wiring is architecturally superior to Opus's late-stage retrofit.
- **Security review cadence**: Mid-stream checkpoint prevents late-stage rework.
- **Operational detail**: FTE allocations, post-launch timeline, external service SLAs, pre-Phase-1 checklist.
- **Implementation specificity**: Dedicated milestones for DI container, password reset token table, logout endpoint, and each middleware component.
- **Integration point documentation**: The appendix summarizing all 5 registries is a strong cross-cutting reference.
- **Acceptance criteria**: Every milestone has explicit, testable acceptance criteria — Opus is less consistent here.

---

## 4. Areas Requiring Debate to Resolve

1. **Timeline (D2)**: The 14-week vs 6-week gap is the most consequential divergence. Need to align on team size, parallelization assumptions, and whether Opus's sprint overlap already accounts for parallel work. Likely truth is somewhere in between.

2. **Audit log timing (D3)**: Should audit logging be provisioned in Phase 1 (Haiku) or deferred to Phase 4 (Opus)? Haiku's approach is safer for compliance but adds Phase 1 scope. If SOC2 deadline is firm, early provisioning is clearly better.

3. **Security review timing (D4)**: One checkpoint at end (Opus) vs mid-stream gate (Haiku). If security engineer availability is limited, Haiku's earlier engagement is more efficient. Debate whether the Phase 1 review is worth the potential Phase 2 delay.

4. **Phase granularity (D1)**: 4 phases vs 2. More gates (Opus) gives stakeholders more control but adds coordination overhead. Fewer gates (Haiku) moves faster but reduces visibility. This is a team/org culture decision.

5. **Password policy location (D7)**: In PasswordHasher (Haiku) vs at endpoint (Opus). This is a genuine design debate — coupling vs defense-in-depth. Consider: will password policy ever be checked without hashing? If yes, decouple. If no, Haiku's approach is fine.
