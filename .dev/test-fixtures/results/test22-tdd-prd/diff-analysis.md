---
total_diff_points: 16
shared_assumptions_count: 15
---

## Shared Assumptions and Agreements

Both variants converge on core architecture and governance:

1. Complexity score 0.75 HIGH, architect persona, same spec source
2. Stateless JWT access token (15-min) + Redis-backed refresh token (7-day)
3. RS256 2048-bit signing with quarterly rotation
4. bcrypt cost 12 via `PasswordHasher` abstraction
5. **12-month audit retention** — both resolve OQ-CONF-001 in favor of PRD/SOC2 over TDD §7.2 90-day note
6. **5 attempts / 15-min lockout** — both adopt TDD §13 values for OQ-PRD-003
7. Committed GA date 2026-06-09 anchored to TDD §23
8. Five-milestone technical phasing: Foundation → Core → Integration/UX → Hardening → Production Readiness
9. Logout endpoint added to close PRD AUTH-E1 gap beyond TDD
10. OAuth/social, MFA, RBAC enforcement, API keys explicitly deferred to v1.1
11. Async SendGrid reset email dispatch
12. "Remember me" deferred beyond v1.0
13. Three-phase rollout (internal alpha → 10% beta → 100% GA) with feature flags AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH
14. Kubernetes HPA 3→10 pods at CPU>70%; pg-pool 100→200; Redis 1GB→2GB
15. Same risk taxonomy (R-001 XSS, R-002 brute force, R-003 migration, R-PRD-001..004)

## Divergence Points

**1. FR-AUTH-002 Registration placement**
- Opus: M2 (alongside login/core logic, row 24)
- Haiku: M1 (as row 1, treated as Foundation deliverable)
- Impact: Haiku front-loads a user-facing endpoint before token lifecycle exists, coupling M1 to API + GDPR consent UX; Opus keeps M1 pure infrastructure, reducing M1 blast radius but delaying registration E2E testability.

**2. Audit admin query endpoint (API-009)**
- Opus: Not included — audit logging emits but admin query interface absent
- Haiku: Explicit `GET /v1/auth/audit-events` added in M3 via OQ-GAP-002 closure
- Impact: Haiku closes Jordan admin-persona gap from PRD; Opus leaves internal audit access implicit/manual, risking SOC2 audit workflow friction.

**3. Forgot/Reset password page components**
- Opus: Single row FE-RESET (M3 row 49) covering both routes
- Haiku: Two explicit rows COMP-016 ForgotPasswordPage + COMP-017 ResetPasswordPage plus OQ-GAP-003 rationale
- Impact: Haiku produces cleaner traceability for PRD-implied UI; Opus is terser but leaves per-page acceptance criteria undistinguished.

**4. Logout endpoint priority**
- Opus: API-LOGOUT marked P1, FE-LOGOUT also P1
- Haiku: API-007 logout marked P0 with dedicated TEST-009 flow test
- Impact: Haiku treats logout as GA-blocking per PRD AUTH-E1; Opus allows logout to ship as fast-follow, which would violate PRD user story if deferred.

**5. Timeline duration and start date**
- Opus: 11 weeks, 2026-03-26 → 2026-06-09, M5=3 weeks
- Haiku: 10 weeks + 2 days, 2026-03-30 → 2026-06-09, M5=16 days
- Impact: Opus has larger M5 buffer for rollout incidents; Haiku runs tighter, less margin for beta-phase SLO regressions.

**6. OQ-PRD-001 (sync vs async reset email)**
- Opus: Listed as open in M3 with default async + upgrade trigger
- Haiku: Closed in M3 open-questions with async commit
- Impact: Haiku removes a late-stage decision point; Opus preserves explicit escalation threshold (loss rate >0.1%) that Haiku omits.

**7. OQ-PRD-004 (remember me)**
- Opus: Open with default "not supported v1.0"
- Haiku: Closed deferred
- Impact: Mostly stylistic — both arrive at same v1.0 behavior.

**8. OQ-PRD-002 (max refresh tokens per user)**
- Opus: Hard blocker before M1 exit — DM-002 Redis schema cannot freeze
- Haiku: Remains open through M2, with TKN keeping configurable cap as `TBD-pending-OQ-PRD-002`
- Impact: Opus is stricter about schema finalization; Haiku ships with placeholder that could cause Redis key-schema churn if cap policy changes post-M2.

**9. Complexity score derivation transparency**
- Opus: Shows explicit additive breakdown (+0.20 security, +0.15 orchestration, etc.)
- Haiku: Asserts 0.75 without itemization
- Impact: Opus enables audit of complexity-class assumption; Haiku is less defensible if class is challenged.

**10. TDD milestone mapping**
- Opus: Dedicated mapping table (roadmap M1..M5 → TDD §23 M1..M5 with target dates and alignment note)
- Haiku: Inline prose in Timeline row
- Impact: Opus makes calendar-anchor compliance verifiable at a glance.

**11. Security review/pen test as separate rows**
- Opus: SEC-REVIEW (row 66) + SEC-PENTEST (row 67) as distinct M4 deliverables with own AC
- Haiku: Bundled into TEST-013 "Security and reliability validation pack"
- Impact: Opus enables separate ownership (Security team) and independent sign-off gates; Haiku conflates the two and risks missing pen-test findings remediation window.

**12. AuthGuard / LoginAttemptTracker as explicit components**
- Opus: Implicit in SEC-LOCKOUT and API handlers
- Haiku: Explicit COMP-012 AuthGuard + COMP-013 LoginAttemptTracker rows
- Impact: Haiku improves component inventory clarity for traceability; Opus treats them as internal implementation detail.

**13. Risk register depth**
- Opus: 10 rows including R-PERF-001 (bcrypt latency breach), R-AUDIT-RET (retention conflict), R-RACE-REFRESH (multi-tab race)
- Haiku: 7 rows, omits performance-specific and multi-tab race entries
- Impact: Opus surfaces quantifiable risks earlier; Haiku under-documents known mitigations (e.g., BroadcastChannel tab-leader election).

**14. Feature flag + rollout dashboard as explicit components**
- Opus: Rollout tooling implicit; ROLL-TRIG row for automation
- Haiku: COMP-020 FeatureFlagController + COMP-021 Rollout dashboard as explicit rows
- Impact: Haiku improves operational handoff artifacts; Opus delivers equivalent function but less visible in component inventory.

**15. Data minimization + GDPR consent treatment**
- Opus: NFR-COMP-001 adds `consent_given_at` column via migration + RegisterPage checkbox in M4
- Haiku: NFR-COMP-001 in M1 alongside DM-001, with consent captured at registration from day one
- Impact: Haiku enforces GDPR from schema inception, reducing rework risk; Opus defers to hardening phase, risking late schema migration.

**16. Dependency graph visualization**
- Opus: ASCII diagram with wiring arrows, intra-component details
- Haiku: Linear arrow-list notation
- Impact: Opus enables faster dependency audit; Haiku is compact but less visual.

## Areas Where One Variant Is Clearly Stronger

**Opus stronger:**
- Complexity derivation auditability (#9)
- TDD calendar-anchor mapping (#10)
- Risk register depth and quantification (#13)
- Security gate separation (SEC-REVIEW vs SEC-PENTEST, #11)
- Open-question blocker discipline on OQ-PRD-002 (#8)

**Haiku stronger:**
- PRD gap closure — explicit audit query endpoint and forgot/reset pages (#2, #3)
- Logout GA-priority alignment with PRD (#4)
- Component inventory explicitness (#12, #14)
- GDPR-from-schema (#15)
- Fewer unresolved OQs carrying into rollout (#6, #7)

## Areas Requiring Debate to Resolve

1. **Registration placement (M1 vs M2)** — affects M1 surface area and E2E testability cadence.
2. **Logout as P0 vs P1** — genuine PRD-vs-pragmatism tension; PRD text favors Haiku, delivery buffer favors Opus.
3. **Audit admin query endpoint inclusion** — scope expansion vs SOC2/Jordan persona completeness.
4. **OQ-PRD-002 treatment** — freeze schema now (Opus) or ship with configurable placeholder (Haiku).
5. **Timeline margin** — 3-week M5 (Opus buffer) vs 16-day M5 (Haiku tighter); depends on confidence in M4 SLO proof.
6. **Security review separation** — two gates (Opus) vs bundled validation pack (Haiku); tradeoff between process overhead and finding-remediation clarity.
7. **GDPR consent timing** — M1 schema inclusion (Haiku) vs M4 hardening-phase addition (Opus); depends on migration tolerance.
