---
total_diff_points: 14
shared_assumptions_count: 18
---

# Diff Analysis: Opus Architect vs Haiku Architect Roadmaps

## 1. Shared Assumptions and Agreements

Both variants agree on the following 18 points:

1. **Complexity**: MEDIUM (0.6) — well-understood auth patterns, security-critical
2. **Strategic priority**: Authentication unblocks Q2–Q3 2026 personalization ($2.4M projected revenue)
3. **SOC2 deadline**: Q3 2026 audit forces audit logging into v1.0 scope (OQ6 resolution)
4. **JWT approach**: RS256 asymmetric signing with keys in secrets manager
5. **Password hashing**: bcrypt cost factor 12 (~250ms), configurable
6. **Refresh token rotation**: With replay detection, revoke-all-on-reuse
7. **Database**: PostgreSQL 15+ with `users` and `refresh_tokens` tables
8. **Token TTLs**: 15-minute access tokens, 7-day refresh tokens
9. **Rate limiting**: 5 login attempts per minute per IP
10. **Performance target**: < 200ms p95 on login endpoint
11. **Availability target**: 99.9% uptime
12. **GDPR consent**: Explicit checkbox at registration with timestamp
13. **Email service**: SendGrid for password reset delivery
14. **OQ1 recommendation**: Async email via message queue
15. **OQ4 recommendation**: Defer "remember me" to v1.1
16. **OQ5 recommendation**: Cascade delete tokens on user deletion
17. **OQ7 recommendation**: Explicit consent checkbox
18. **OQ8 recommendation**: Include logout endpoint in scope

---

## 2. Divergence Points

### D1: Phase Structure and Timeline

- **Opus**: 4 phases over 12 weeks (Foundation → Core Auth → Password Reset & Compliance → Hardening & Launch)
- **Haiku**: 2 phases over 7–10 weeks with 2–3 week buffer (Auth Core → Recovery, Compliance & Hardening)
- **Impact**: Opus provides finer granularity for tracking and gating but extends duration 20–70%. Haiku is more aggressive, compressing foundation + core auth into a single 4-week phase and bundling hardening into Phase 2 rather than a dedicated phase.

### D2: Separation of Foundation from Core Auth

- **Opus**: Dedicates Weeks 1–2 entirely to schema, key provisioning, and service modules (PasswordHasher, JwtService, TokenManager) before any endpoint work
- **Haiku**: Interleaves infrastructure (Week 1), service implementation (Week 2), and API endpoints (Week 3) within a single phase
- **Impact**: Opus's separation creates a cleaner dependency chain and explicit exit criteria for the foundation layer. Haiku's approach is faster to first working endpoint but has less isolation between layers.

### D3: Dedicated Launch/Hardening Phase

- **Opus**: Full 3-week Phase 4 for load testing, security review, penetration testing, UX testing, and production deployment
- **Haiku**: Hardening compressed into Week 7 of Phase 2; penetration testing is a Phase 2 exit gate rather than a dedicated phase
- **Impact**: Opus allocates significantly more calendar time for security validation and UX iteration. Haiku relies on the 2–3 week buffer to absorb any hardening overruns.

### D4: Max Refresh Tokens Per User (OQ2)

- **Opus**: Recommends **5 tokens max** — supports multi-device without unbounded storage; oldest revoked on overflow
- **Haiku**: Recommends **unlimited** with per-device rotation — simplifies UX, enables multi-device persistence
- **Impact**: Opus's bounded approach is more predictable for storage and security auditing. Haiku's unlimited approach avoids user-facing friction when adding devices but requires per-device tracking infrastructure and has unbounded storage implications.

### D5: Account Lockout Policy (OQ3)

- **Opus**: **Progressive lockout** — 5 failures → 15 min, 10 failures → 1 hour, 20 failures → admin unlock
- **Haiku**: **Single threshold** — 5 failures → 15-minute lock, admin unlock capability
- **Impact**: Opus's progressive approach provides better defense against sustained brute-force while being less punitive for legitimate typos. Haiku's simpler model is easier to implement and explain to users.

### D6: Logout Endpoint Placement

- **Opus**: Recommends including logout in **Phase 2** (Week 5) with low implementation cost noted
- **Haiku**: Recommends including logout in **Phase 1** (Week 3), citing PRD user story AUTH-E1
- **Impact**: Minor scheduling difference. Haiku's placement is more defensible since logout is core UX, not an edge case.

### D7: Performance Testing Scope

- **Opus**: Tests all auth endpoints for < 200ms p95 (Tasks 4.1, 4.2)
- **Haiku**: Tests login at < 200ms p95, password reset at < 500ms p95 (different target)
- **Impact**: Haiku's differentiated targets are more realistic — password reset involves email dispatch and more DB operations. Opus applies a uniform target that may be unnecessarily strict for non-login endpoints.

### D8: Key Rotation Schedule

- **Opus**: **90-day** rotation schedule with documented procedure (Task 4.6)
- **Haiku**: **Quarterly** rotation with 30-day overlap window for graceful deprecation
- **Impact**: Similar cadence but Haiku's overlap window detail is architecturally important — Opus doesn't address how old tokens are handled during rotation.

### D9: Total Effort Estimation

- **Opus**: ~4.75 FTE across 12 weeks (team composition table with fractional allocations per phase)
- **Haiku**: 4.5 FTE across 7–10 weeks = ~180–200 engineer-days explicitly stated
- **Impact**: Opus allocates more calendar time but similar headcount. Haiku's explicit engineer-day estimate is more useful for resource planning.

### D10: Milestone Granularity

- **Opus**: 8 milestones (M1–M8) with clear week boundaries
- **Haiku**: Phase-level exit gates with weekly internal milestones (not numbered)
- **Impact**: Opus's numbered milestones are better for stakeholder reporting and go/no-go decisions. Haiku's approach is adequate but less formal.

### D11: Migration Numbering

- **Opus**: Creates migration 003 for **both** `users` and `refresh_tokens` tables (single migration)
- **Haiku**: References migration 003 without specifying whether it's one or two migrations
- **Impact**: Minor — Opus is more explicit about migration strategy.

### D12: UX Testing Placement

- **Opus**: UX testing (registration funnel, password reset funnel) in **Phase 4** as dedicated tasks
- **Haiku**: Registration UX testing in **Phase 1 exit gate** (> 60% conversion required before Phase 2)
- **Impact**: Haiku's earlier UX validation catches conversion issues before building password reset. Opus risks building the complete system before discovering UX problems.

### D13: Password Reset Rate Limiting

- **Opus**: No explicit rate limit on password reset requests
- **Haiku**: **10 password reset requests per hour per email** to prevent email bombing
- **Impact**: Haiku addresses a real abuse vector that Opus overlooks.

### D14: Monitoring and Alerting Detail

- **Opus**: General monitoring mentioned in Phase 4 (PagerDuty, health checks)
- **Haiku**: Specific alert thresholds defined — > 20 failed logins/minute, unusual token reuse patterns, email bounce rates > 5%
- **Impact**: Haiku's specificity is more actionable for DevOps and reduces ambiguity in implementation.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus Is Stronger

| Area | Why |
|------|-----|
| **Integration point documentation** | Every phase has an explicit wiring table showing named artifacts, types, owning phase, and consumers — far superior traceability |
| **Milestone structure** | 8 numbered milestones with week-level precision; better for stakeholder communication and sprint planning |
| **Scope guardrails** | Explicit out-of-scope table with rationale (OAuth, MFA, RBAC, social login); prevents scope creep |
| **Timeline visualization** | ASCII Gantt chart provides at-a-glance schedule understanding |
| **OQ resolution detail** | Each open question has a concrete architect recommendation with reasoning |

### Haiku Is Stronger

| Area | Why |
|------|-----|
| **UX testing timing** | Phase 1 exit gate requires conversion validation before proceeding — catches problems early |
| **Password reset rate limiting** | Addresses email bombing abuse vector that Opus misses entirely |
| **Alert specificity** | Concrete thresholds for operational monitoring instead of vague "configure alerting" |
| **Differentiated performance targets** | < 500ms for password reset vs < 200ms for login reflects realistic operational differences |
| **Key rotation overlap** | 30-day overlap window is an essential detail for zero-downtime rotation |
| **Effort estimation** | Explicit engineer-day count (180–200) is more useful for budgeting than fractional FTE tables |
| **SOC2 control mapping** | References specific SAC 2 control objectives (CC6.1, CC7.2) rather than generic "compliance" |
| **Component architecture** | Explicitly names patterns (Strategy, DI container, State machine) for implementability |

---

## 4. Areas Requiring Debate to Resolve

| Topic | Opus Position | Haiku Position | Resolution Criteria |
|-------|--------------|----------------|-------------------|
| **Phase count / timeline** | 4 phases, 12 weeks — more gates, longer | 2 phases, 7–10 weeks + buffer — faster, fewer gates | Depends on team cadence and stakeholder reporting needs. If Q2 deadline is hard (June 30), Haiku's timeline is more realistic. |
| **Max refresh tokens (OQ2)** | 5 per user, oldest revoked | Unlimited with per-device rotation | Security team should weigh in — bounded is safer; product should weigh in — unlimited is simpler UX. Compromise: bounded at 10 with explicit device management UI in v1.1. |
| **Lockout progression (OQ3)** | Progressive (5/10/20 thresholds) | Single threshold (5 → lock) | Progressive is better security but more complex. If Phase 1 timeline is tight, ship single threshold and upgrade to progressive in hardening. |
| **Hardening as separate phase** | Yes — dedicated 3 weeks | No — embedded in Phase 2 + buffer | If the team has done auth implementations before, embedded is fine. If this is the team's first security-critical system, a dedicated hardening phase reduces risk. |
| **UX testing timing** | Phase 4 (post-build) | Phase 1 exit gate (pre-Phase 2) | Haiku's approach is objectively lower-risk. The only argument for Opus is if UX testing resources aren't available until later. |
