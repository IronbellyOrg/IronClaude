---
total_diff_points: 14
shared_assumptions_count: 18
---

# Diff Analysis: Opus Architect vs Haiku Architect Roadmaps

## 1. Shared Assumptions and Agreements

1. **Spec source and complexity**: Both derive from the same TDD (AUTH-001) and PRD (AUTH-PRD-001), scoring complexity at MEDIUM (0.55)
2. **Strategic context**: Both cite ~$2.4M personalization revenue dependency and SOC2 Type II compliance gate
3. **Core architecture**: Stateless REST, `AuthService` facade with `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo` via constructor DI
4. **Token strategy**: RS256 JWT access tokens (15-min TTL) + opaque Redis refresh tokens (7-day TTL)
5. **Password hashing**: bcrypt cost factor 12 via `PasswordHasher` abstraction with future argon2id migration path
6. **Feature flags**: `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH`, both OFF by default
7. **GAP-001 resolution**: 12-month audit log retention (PRD overrides TDD's 90-day)
8. **GAP-002 resolution**: Logout endpoint added (POST `/auth/logout`)
9. **GAP-003 resolution**: Admin audit log query API added
10. **GAP-004 resolution**: GDPR consent fields added to `UserProfile` and registration flow
11. **GAP-005 resolution**: Password reset endpoint schemas to be finalized
12. **Security posture**: accessToken in memory only, HttpOnly cookie for refreshToken, rate limiting, account lockout after 5 failures
13. **Rollback triggers**: Identical thresholds (p95 >1000ms/5min, error >5%/2min, Redis failures >10/min, data corruption)
14. **Success metrics alignment**: Same NFR targets (p95 <200ms, 500 concurrent, 99.9% uptime, bcrypt cost 12, RS256 2048-bit)
15. **Business metrics**: Same targets (>60% registration conversion, >1000 DAU, >30min sessions, <5% failed logins, >80% reset completion)
16. **Team composition**: 2 backend, 1 frontend, 1 DevOps, 1 QA (core agreement)
17. **Rollout strategy**: Feature-flag-gated phased rollout (internal → beta 10% → GA 100%)
18. **Observability stack**: Prometheus metrics, OpenTelemetry traces, Grafana dashboards, structured logging

## 2. Divergence Points

### D-01: Timeline and Phase Structure

- **Opus**: 3-phase over **9 weeks** (3w + 2w + 4w) plus 2w stabilization = 11 weeks total
- **Haiku**: 3-phase over **4 weeks** (1w + 2w + 1w) with no explicit stabilization buffer

**Impact**: Opus is 2.75x longer. Opus allocates more time for implementation depth and security hardening. Haiku's timeline is aggressive — squeezing all Phase 1 implementation into 5 working days risks quality shortcuts on a security-critical service.

### D-02: Phase 1 Scope — Password Reset Placement

- **Opus**: Password reset (FR-AUTH-005) deferred to **Phase 3** (Weeks 6-9)
- **Haiku**: All 5 FR-AUTH requirements implemented in **Phase 1** (Week 1), including password reset

**Impact**: Opus's phasing reduces Phase 1 risk and focuses on core login/registration first. Haiku front-loads everything, which compresses the critical path but means SendGrid integration must be ready from Day 1.

### D-03: Phase 1 Scope — Profile and Refresh Placement

- **Opus**: Token refresh (FR-AUTH-003) and profile (FR-AUTH-004) deferred to **Phase 2** (Weeks 4-5)
- **Haiku**: Both implemented in **Phase 1** (Week 1)

**Impact**: Same trade-off as D-02. Opus creates a leaner Phase 1 MVP; Haiku aims for feature-complete before any deployment.

### D-04: Logout Endpoint Phasing

- **Opus**: Logout implemented in **Phase 2** (Section 2.3)
- **Haiku**: Logout implemented in **Phase 1** (API Endpoint Inventory shows Phase 1)

**Impact**: Minor. Both resolve GAP-002 before beta. Haiku's approach is more internally consistent (all auth operations together).

### D-05: Admin Audit Log Query Phasing

- **Opus**: Admin audit log query in **Phase 3** (Section 3.2)
- **Haiku**: Admin audit log query in **Phase 2** (API Endpoint #8)

**Impact**: Haiku's earlier delivery enables SOC2 auditor validation during beta monitoring, which is better aligned with compliance validation timing.

### D-06: Security Hardening Approach

- **Opus**: Dedicated **Phase 3 security hardening** section (3.3) with penetration testing, NIST SP 800-63B validation, security review of crypto components, HttpOnly cookie cross-browser verification
- **Haiku**: Security review at **end of Phase 1**, penetration testing engagement **scoped in Phase 1** but executed **pre-Phase 3**. No dedicated hardening phase.

**Impact**: Opus's explicit hardening phase is more thorough. Haiku spreads security across phases but lacks a consolidated gate. For a security-critical auth service, Opus's approach reduces risk of shipping with unreviewed crypto implementations.

### D-07: Wiring Documentation Style

- **Opus**: Named artifacts as **integration wiring sections** within each phase (e.g., "Named Artifact: `AuthService` Facade Dispatch") with mechanism, components, owning phase, consumers
- **Haiku**: Named artifacts as **wiring tasks** (e.g., "Wiring Task 1.1.1: Password Hashing Strategy Registry") with cross-references and implementation details. Also includes a **consolidated Integration Points & Wiring Summary** section with dispatch tables, DI config, feature flag integration, and callback chain documentation.

**Impact**: Haiku's wiring documentation is significantly more detailed and includes a cross-cutting summary table. Opus's per-phase approach is easier to follow linearly but lacks the consolidated view.

### D-08: Open Questions Handling

- **Opus**: Explicit **Open Questions table** (Section 6) with 5 items including blocking phase and recommended resolution (OQ-001 through OQ-PRD-003)
- **Haiku**: No dedicated open questions section. Some are addressed inline (e.g., async email implied by SendGrid integration) but not tracked as open items.

**Impact**: Opus's explicit tracking prevents open questions from being silently resolved with potentially wrong defaults. This is important for stakeholder alignment.

### D-09: Legacy Auth Migration Detail

- **Opus**: Legacy migration mentioned in rollout phases. Data migration risk addressed in R-003.
- **Haiku**: Explicit **legacy auth deprecation section** (3.2) with 301 redirects, public communication plan, 30-day deprecation window, and code removal steps.

**Impact**: Haiku provides a clearer operational playbook for the cutover. Opus assumes the migration is primarily a flag toggle without addressing legacy endpoint handling.

### D-10: Resource Estimation Granularity

- **Opus**: Team roles with phase coverage and allocation percentages (e.g., "QA: Part-time P1, Full-time P2-3")
- **Haiku**: More granular with **FTE counts** (e.g., "Security Engineer: 0.5"), **peak staffing analysis** (6 FTE Phase 1, 5 FTE Phase 2, 3 FTE Phase 3), and **cost estimates for third-party services** (SendGrid ~$100/mo, LaunchDarkly $200+/mo)

**Impact**: Haiku's resource section is more actionable for project planning and budgeting. Opus lacks cost visibility.

### D-11: Documentation Deliverables

- **Opus**: No explicit documentation deliverables section
- **Haiku**: Explicit **Phase 3 documentation section** (3.5) listing operations runbook, API docs (Swagger/OpenAPI), troubleshooting guide, and ADR

**Impact**: Haiku ensures knowledge transfer is planned. Opus's omission risks undocumented operations post-GA.

### D-12: Success Criteria Validation Detail

- **Opus**: Success criteria tables with metric/target/phase/method (Section 5) — concise
- **Haiku**: Extremely detailed **per-NFR validation sections** with measurement method, validation gates per phase, and explicit success definitions. Also includes **per-business-metric** phase-gated targets (e.g., "Beta: >40% conversion, GA: >60%")

**Impact**: Haiku's validation approach is more operationally rigorous with phased targets. Opus's is sufficient for tracking but less useful as a test plan.

### D-13: Critical Path Analysis

- **Opus**: Simple dependency chain (text-based, Section 6)
- **Haiku**: Detailed **per-phase task breakdown** with durations, dependencies, slack analysis, risk scenarios with time impact estimates, and conservative estimate (4w best-case, 5-6w with P1 bugs)

**Impact**: Haiku's critical path analysis is substantially more useful for project management. Opus's is illustrative but not plannable.

### D-14: Frontmatter Completeness

- **Opus**: 3 fields (spec_source, complexity_score, primary_persona)
- **Haiku**: 6 fields (spec_source, prd_source, complexity_score, complexity_class, primary_persona, roadmap_version, generated timestamp)

**Impact**: Minor. Haiku's richer metadata improves traceability and versioning.

## 3. Areas Where One Variant Is Clearly Stronger

### Opus Is Stronger

| Area | Why |
|------|-----|
| **Timeline realism** | 9-week timeline is far more realistic for a security-critical auth service than 4 weeks. Phase 1 at 3 weeks allows proper implementation, not a sprint. |
| **Security hardening** | Dedicated Phase 3 hardening section with pen testing, NIST validation, and cross-browser HttpOnly verification. Haiku's security work is scattered. |
| **Open question management** | Explicit tracking table prevents silent assumptions on unresolved decisions (e.g., sync vs async email, max roles, "remember me"). |
| **Phase decomposition logic** | Progressive delivery (core auth → tokens/profile → reset/GA) reduces blast radius per phase. Haiku's "everything in Week 1" approach is high-risk. |
| **Executive summary** | Lists critical gaps requiring pre-implementation resolution, giving stakeholders immediate visibility into blockers. |

### Haiku Is Stronger

| Area | Why |
|------|-----|
| **Wiring documentation** | Consolidated Integration Points & Wiring Summary section is a single reference for all cross-cutting concerns. Named wiring tasks with cross-references are more traceable. |
| **Critical path analysis** | Per-phase task breakdowns with durations, slack, and risk-adjusted estimates. Actually plannable. |
| **Resource and cost detail** | FTE counts, peak staffing, third-party service costs. Budget-ready. |
| **Validation rigor** | Per-NFR measurement methods, phased validation gates with relaxed beta targets, explicit success definitions. Test-plan quality. |
| **Legacy deprecation plan** | 301 redirects, 30-day window, public comms, code removal — operational playbook. |
| **Documentation deliverables** | Explicit runbook, API docs, troubleshooting guide, ADR deliverables ensure knowledge transfer. |
| **Go/No-Go criteria** | Formal exit gates with no-go triggers per phase. Opus has exit criteria but no explicit no-go triggers. |

## 4. Areas Requiring Debate to Resolve

| # | Topic | Tension | Recommendation |
|---|-------|---------|----------------|
| 1 | **Timeline: 4 weeks vs 9 weeks** | Haiku's 4-week timeline is aggressive for security-critical code. Opus's 9 weeks may be conservative for a well-bounded scope. | Debate needed. A 6-week compromise (2w build + 2w beta + 2w GA/hardening) may be optimal. |
| 2 | **Phase 1 scope: MVP vs feature-complete** | Opus defers refresh/profile/reset to later phases. Haiku builds everything in Week 1. | Opus's phasing is architecturally safer, but Haiku's approach avoids re-deployment overhead. Depends on team velocity and CI/CD maturity. |
| 3 | **Password reset in Phase 1 vs Phase 3** | Haiku treats it as a core requirement. Opus treats it as secondary to login/registration. | If FR-AUTH-005 is a launch requirement (not just nice-to-have), Haiku's front-loading is correct. If launch can proceed without reset, Opus's deferral reduces Phase 1 risk. |
| 4 | **Security review timing** | Opus: consolidated pre-GA. Haiku: end of Phase 1 review + pre-GA pentest. | Haiku's earlier review catches issues sooner. But Opus's consolidated gate ensures nothing ships without full sign-off. Consider both: early review + final gate. |
| 5 | **Admin audit query: Phase 2 vs Phase 3** | Haiku enables auditor validation during beta. Opus defers to GA phase. | Haiku's timing is better aligned with compliance validation. If SOC2 audit is in Q3, earlier validation reduces schedule risk. |
| 6 | **Merge strategy** | Both have distinct strengths. | The ideal roadmap would use Opus's timeline and phasing with Haiku's wiring documentation, critical path analysis, validation rigor, resource detail, and legacy deprecation plan. |
