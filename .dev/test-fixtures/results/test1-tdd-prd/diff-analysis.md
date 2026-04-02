---
total_diff_points: 14
shared_assumptions_count: 18
---

## 1. Shared Assumptions and Agreements

Both variants agree on the following foundational elements:

1. **Complexity classification**: MEDIUM (0.55) with architect persona
2. **Core tech stack**: PostgreSQL 15+, Redis 7+, Node.js 20 LTS, bcryptjs, jsonwebtoken, SendGrid, React
3. **JWT architecture**: RS256 with 2048-bit RSA keys, 15-minute access token expiry, 7-day refresh token TTL in Redis, 5-second clock skew tolerance
4. **Password hashing**: bcrypt cost factor 12 behind a `PasswordHasher` abstraction
5. **Token storage security**: accessToken in memory only (not localStorage), refreshToken in HttpOnly cookie (R-001 mitigation)
6. **Account lockout**: 5 failed attempts within 15 minutes
7. **Rate limiting**: 10 req/min login, 5 req/min register at API gateway
8. **Feature flags**: `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` for progressive rollout
9. **Three-phase rollout**: Alpha → Beta 10% → GA 100%
10. **Risk identification**: Both identify R-001 (token theft/XSS), R-002 (brute-force), R-003 (migration data loss)
11. **OQ-EXT-001 conflict**: Both flag the 90-day vs 12-month audit log retention discrepancy
12. **GDPR/SOC2 requirements**: Both acknowledge NFR-COMP-001 (consent), NFR-COMP-002 (audit logging), NFR-COMP-003 (data minimization)
13. **Success criteria alignment**: p95 < 200ms login, 99.9% uptime, >1000 DAU, >60% registration conversion
14. **Scope guardrails**: OAuth/OIDC, MFA, RBAC, social login all out of scope
15. **Test coverage target**: 80% unit test coverage
16. **Rollback triggers**: Both define latency and error rate thresholds for rollback
17. **Infrastructure dependencies**: Same provisioning requirements (PostgreSQL, Redis, SendGrid, RSA keys)
18. **API versioning**: Both use `/v1/auth/*` URL-prefix versioning

---

## 2. Divergence Points

### D-01: Timeline — 10 weeks vs 20 weeks

- **Opus**: 10–11 weeks across 5 phases (Foundation through GA)
- **Haiku**: 20 weeks across 6 phases (Phase 0 through Phase 5d)
- **Impact**: Opus assumes roughly half the calendar time. This is the single largest divergence. Opus's timeline is aggressive and assumes high parallelism and experienced team velocity. Haiku's timeline is conservative and includes explicit buffer for security review, runbook testing, and stability monitoring. A 10-week timeline risks underestimating integration complexity; a 20-week timeline risks scope creep and stakeholder fatigue.

### D-02: Phase structure — 5 phases vs 6 phases (Phase 0 separation)

- **Opus**: Infrastructure provisioning is Phase 1 (weeks 1–2), combined with project skeleton setup
- **Haiku**: Dedicates a standalone Phase 0 (weeks -2 to 0) for infrastructure and policy finalization before any code begins
- **Impact**: Haiku's Phase 0 forces explicit resolution of security policies (SEC-POLICY-001) and infrastructure readiness before development starts. Opus folds this into Phase 1 which could create blocking dependencies mid-sprint if provisioning slips.

### D-03: Compliance timing — Early vs Late

- **Opus**: GDPR consent recording built into Phase 2 (registration flow); SOC2 audit logging foundation also in Phase 2
- **Haiku**: Defers both GDPR consent (NFR-COMP-001) and SOC2 audit logging (NFR-COMP-002) to Phase 3 (weeks 9–12)
- **Impact**: Opus's approach reduces rework risk — consent is baked into the registration schema from the start. Haiku's deferral means the registration flow must be retrofitted with consent logic later, potentially requiring migration of existing test data and schema changes. However, Haiku explicitly calls out this deferral and gates Phase 3→4 on compliance readiness.

### D-04: Frontend timing — Parallel vs Sequential

- **Opus**: Frontend components (`LoginPage`, `RegisterPage`, `ProfilePage`) are deferred to Phase 4 (weeks 5–7), after all backend components including token management are complete
- **Haiku**: Frontend `LoginPage` and `RegisterPage` are built in Phase 1 (weeks 1–4) alongside core backend, with `ProfilePage` in Phase 3
- **Impact**: Opus's approach ensures the backend API contract is stable before frontend work begins, reducing frontend rework. Haiku's approach enables earlier E2E testing and faster user-facing demos, but risks frontend changes if the token API evolves in Phase 2.

### D-05: Admin audit log query API — Deferred vs In-scope

- **Opus**: Explicitly defers admin log query endpoint to post-GA (OQ-EXT-002)
- **Haiku**: Includes admin audit log query API (GET `/auth/admin/logs`) as a Phase 3 deliverable with authorization middleware
- **Impact**: Haiku adds ~18h of implementation work plus admin authorization middleware. This satisfies the Jordan (admin) persona needs from the PRD. Opus's deferral reduces v1.0 scope but leaves the admin persona underserved at launch.

### D-06: Logout endpoint — Different deferral strategies

- **Opus**: Identifies logout as OQ-EXT-003, recommends implementing as `POST /auth/logout` (low effort, PRD requires it) — suggests inclusion
- **Haiku**: Explicitly defers logout to Phase 5 / v1.1
- **Impact**: The PRD's AUTH-E1 epic mentions logout. Opus's recommendation to include it is more PRD-faithful. Haiku's deferral is a scope reduction that may cause PRD coverage gaps.

### D-07: Team sizing — Implicit vs Explicit

- **Opus**: Lists team roles (auth-team, platform-team, frontend-team, QA, security) without headcount
- **Haiku**: Specifies exact headcount: 5 backend, 2 frontend, 1 QA, 1 DevOps, 1 security (0.5 FTE), 1 product lead = ~11 FTE
- **Impact**: Haiku's explicit resourcing enables realistic capacity planning and directly explains why the timeline is 20 weeks. Opus's omission makes it unclear whether the 10-week timeline is achievable with a realistic team.

### D-08: Task-level estimation granularity

- **Opus**: Provides task lists without hour estimates or sprint assignments
- **Haiku**: Provides detailed task tables with owner, sprint week, hour estimates, blocking dependencies, and test references for every task
- **Impact**: Haiku's granularity is immediately actionable for sprint planning. Opus requires a separate task breakdown pass before work can begin.

### D-09: Account lockout implementation — Database vs In-process

- **Opus**: Implies database-backed lockout (references `locked_until` implicitly through account lockout behavior)
- **Haiku**: Explicitly specifies in-process hash map for lockout registry, acknowledges the persistence gap (users unlocked on restart), and plans Redis migration as future enhancement
- **Impact**: Haiku is more architecturally honest about the trade-off. Opus doesn't address what happens to lockout state on service restart.

### D-10: Wiring mechanism documentation depth

- **Opus**: Provides integration point tables per phase showing named artifacts, wired components, owning phase, and consumers
- **Haiku**: Provides the same plus a comprehensive appendix checklist enumerating every registry and dispatch mechanism across all phases with status tracking
- **Impact**: Haiku's appendix serves as a cross-cutting verification artifact that prevents "forgot to wire X" failures. Opus's per-phase tables are useful but require mental assembly to get the full picture.

### D-11: Password reset email — Async default vs Unresolved

- **Opus**: Decides async (Redis queue-based) as the safer default for OQ-PRD-001
- **Haiku**: Leaves async vs sync as an open question to resolve at Phase 3 start
- **Impact**: Opus's decision-forward approach reduces ambiguity. Haiku's deferral could delay Phase 3 implementation if the decision isn't made promptly.

### D-12: Approval gates between phases

- **Opus**: Defines exit criteria per phase but no formal approval gate process
- **Haiku**: Defines explicit approval gates with named approvers and success criteria at every phase boundary
- **Impact**: Haiku's gates provide governance checkpoints suitable for SOC2 audit evidence. Opus's approach is leaner but may lack the formal accountability trail needed for compliance.

### D-13: Rollback trigger specificity

- **Opus**: Defines 4 specific rollback triggers with numeric thresholds (p95 > 1000ms for 5 min, error rate > 5% for 2 min, Redis failures > 10/min, any data corruption)
- **Haiku**: Describes rollback capability but rollback triggers are less precisely defined (refers to metrics being "within normal ranges")
- **Impact**: Opus's specific thresholds are operationally superior — on-call engineers can make instant rollback decisions without judgment calls.

### D-14: Audit log retention default

- **Opus**: Implements 12-month as the conservative default pending resolution
- **Haiku**: Leaves the decision explicitly unresolved, marking it as "MUST RESOLVE by Phase 3 M3.4"
- **Impact**: Opus's approach is pragmatically safer — building for the longer retention is backwards-compatible. Haiku's approach forces an explicit decision but risks Phase 3 delays if stakeholders don't resolve promptly.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:

- **Decision-forward defaults**: Resolves open questions with conservative defaults rather than leaving them open (audit retention, async email, consent field, logout endpoint)
- **Rollback trigger precision**: Specific numeric thresholds make rollback operationally executable
- **Compliance timing**: Building GDPR consent and audit logging into Phase 2 avoids retrofit costs
- **Conciseness**: ~40% shorter while covering the same functional requirements — easier to maintain and reference
- **Business context**: Includes revenue impact ($2.4M) and SOC2 deadline (Q3 2026) that anchor priority decisions

### Haiku is stronger in:

- **Implementation actionability**: Hour estimates, sprint assignments, and owner fields make it immediately sprint-plannable
- **Team resourcing**: Explicit headcount and FTE allocation enables realistic capacity planning
- **Wiring completeness**: Appendix checklist is a powerful cross-cutting verification artifact
- **Governance formality**: Named approval gates at every phase boundary satisfy compliance audit requirements
- **Risk analysis depth**: More risks identified (8 vs 5) with per-phase mitigation tables and specific trigger conditions
- **Phase 0 separation**: Forces infrastructure and policy readiness before development starts

---

## 4. Areas Requiring Debate to Resolve

1. **Timeline realism (D-01)**: Is 10 weeks achievable? Opus doesn't specify team size. If the team is the ~11 FTE Haiku assumes, 10 weeks may be feasible with aggressive parallelism. If the team is smaller, 10 weeks is unrealistic. This needs to be resolved against actual team capacity.

2. **Frontend sequencing (D-04)**: Should frontend start in Phase 1 (Haiku) or wait until Phase 4 (Opus)? This depends on whether the frontend team would otherwise be idle and whether early E2E validation outweighs potential rework from API changes.

3. **Admin audit API scope (D-05)**: Is the Jordan persona's needs a v1.0 requirement or v1.1? This is ultimately a product decision. If SOC2 audit requires admin log access by Q3 2026, it must be in v1.0.

4. **Compliance timing trade-off (D-03)**: Opus's early integration is technically cleaner. Haiku's deferral groups compliance work into a focused phase. The right answer depends on whether the team can handle compliance work interleaved with core feature development or whether dedicated focus is needed.

5. **Governance overhead (D-12)**: Opus's lightweight exit criteria vs Haiku's formal approval gates. For a SOC2-bound project, formal gates may be non-negotiable. For a startup moving fast, they may slow delivery unnecessarily.

6. **Granularity vs maintainability**: Haiku's task-level detail is immediately useful but expensive to maintain as plans change. Opus's higher-level structure is more resilient to plan evolution but requires additional planning work before execution. The right level depends on team maturity and PM tooling.
