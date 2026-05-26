---
spec_source: /config/workspace/IronClaude/.dev/eval-roadmap/inputs/merged-prd-tdd-user-auth.md
generated: 2026-05-22T16:31:30Z
generator: sc:roadmap
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 6
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
complexity_class: MEDIUM
---

# Test Strategy: Continuous Parallel Validation

## Validation Philosophy

This test strategy implements **continuous parallel validation** — the assumption that work has deviated from the plan, is incomplete, or contains errors until validation proves otherwise.

**Core Principles**:

1. A validation agent runs in parallel behind the work agent, checking completed work against requirements
2. Major issues trigger a stop — work pauses for refactor/fix before continuing
3. Validation milestones are interleaved between work milestones (not batched at the end)
4. Minor issues are logged and addressed in the next validation pass
5. The interleave ratio is **1:2** (one validation per two work milestones), derived from MEDIUM complexity class (score 0.48)

For an authentication service with Critical-severity security risks (RISK-005) and High-severity compliance risk (RISK-006), validation cannot wait for a single gate at the end. Each validation milestone validates the previous two work milestones against the deliverable acceptance criteria, the success criteria, and the security regression baseline.

## Validation Milestones

| ID | After Work Milestone | Validates | Stop Criteria |
|----|---------------------|-----------|---------------|
| V1 | M2 (Identity Core + Session Lifecycle) | M1 trust primitives + M2 identity substrate — schema correctness, bcrypt cost=12 enforcement, JWT RS256 signature verification, audit event capture across REGISTER/LOGIN/REFRESH/LOGOUT, refresh-token family reuse detection | Any of: bcrypt cost ≠ 12 in shipped code; missing audit emit on any M2 endpoint; reuse detection fails to revoke family; JWT verification accepts wrong-`kid` token |
| V2 | M4 (Password Reset + Audit Compliance) | M3 brute-force defenses + M4 reset flow + audit compliance — lockout fires at attempt #5 in isolated namespace, rate limits enforced, reset token single-use + 1hr TTL, session invalidation on reset confirm, SOC2 audit query API returns correct results, retention archiver moves >12mo events | Any of: lockout doesn't fire or fires outside isolated namespace; reset token replayable; reset doesn't invalidate sessions; audit query returns events outside retention window; SendGrid DLQ silently drops failures |
| V3 | M6 (Production Hardening + Phased Rollout) | M5 perf NFRs + M6 rollout readiness — login p95 < 200ms at 500 concurrent verified, refresh p95 < 100ms verified, hash time < 500ms verified, feature flags toggle without deploy, key rotation completes zero-downtime in staging, migration script idempotent + reversible | Any of: any perf SC red; feature flag requires deploy to change; key rotation causes downtime in drill; migration is not idempotent; rollback procedure fails in staging exercise |

**Placement rule**: Validation milestones are placed after every 2 work milestones per the 1:2 MEDIUM interleave ratio. V1 after M2, V2 after M4, V3 after M6.

## Issue Classification

| Severity | Action | Threshold | Example |
|----------|--------|-----------|---------|
| Critical | Stop work immediately; fix before any further progress | Any occurrence | Cryptographic flaw (wrong bcrypt cost, wrong JWT algo); audit emit missing on a security-relevant event; secrets logged in plaintext; reset doesn't invalidate sessions |
| Major | Stop work; refactor/fix before next milestone | >1 occurrence OR blocking | Lockout fires but in wrong Redis namespace; rate limit headers missing; integration test coverage <90% on auth modules; refresh-token family not revoked on replay |
| Minor | Log; address in next validation pass | Accumulated count > 5 triggers review | Inconsistent error code naming; missing JSDoc on internal helpers; minor inline-validation copy issues |
| Info | Log only; no action required | N/A | Optimization opportunity in PasswordHasher pool; alternative SendGrid client noted |

## Acceptance Gates

Per-milestone acceptance criteria derived from deliverable ACs and success criteria, mapped to validation milestones.

| Milestone | Gate Criteria | Pass Condition |
|-----------|--------------|----------------|
| M1 | All 5 deliverable ACs met; schema migration applies cleanly; bcrypt benchmark passes; JWKS endpoint serves valid JSON; AuditLogger writes to insert-only table | D1.1–D1.5 ACs ✓; no Critical/Major issues |
| M2 | All 6 deliverable ACs met; all 6 endpoints reachable; auto-login post-register works; refresh-token family revocation on replay verified; audit events emitted on all paths | D2.1–D2.6 ACs ✓; SC-001 funnel measurable; SC-003 token TTL correct; V1 validation passes |
| M3 | All 4 deliverable ACs met; integration test coverage ≥90% on auth modules; lockout fires at #5 in isolated Redis namespace; rate limit returns 429; security regression suite green in CI | D3.1–D3.4 ACs ✓; SC-004 measurable (failed login rate query works); no Critical/Major issues |
| M4 | All 4 deliverable ACs met; reset token single-use + 1hr TTL enforced; session invalidation on reset confirm verified; audit query API + retention archiver functional; SendGrid retry queue + DLQ alerting wired | D4.1–D4.4 ACs ✓; SC-005 funnel measurable; V2 validation passes; SOC2 compliance matrix complete |
| M5 | All 5 deliverable ACs met; httpOnly cookie storage verified (no JS access); silent refresh works; all 4 perf SCs green; load test report archived | D5.1–D5.5 ACs ✓; SC-002 + SC-006 + SC-007 green; SC-001 funnel measurable in UI |
| M6 | All 4 deliverable ACs met; feature flags toggle without deploy; key rotation drill completes zero-downtime in staging; migration idempotent + reversible; runbook signed off | D6.1–D6.4 ACs ✓; SC-008 measurement infrastructure ready; V3 validation passes; go/no-go sign-off |

## Validation Coverage Matrix

| Requirement | Validated By | Milestone | Method |
|-------------|-------------|-----------|--------|
| FR-001 Login | V1, V3 | M2, M5 | Integration test (V1); load test 500 concurrent (V3); brute-force lockout test (V1) |
| FR-002 Registration | V1 | M2 | Integration test happy path + email-collision case; bcrypt cost assertion |
| FR-003 JWT issuance + refresh | V1, V3 | M2, M5 | Integration test refresh + reuse detection (V1); refresh latency load test (V3) |
| FR-004 Profile retrieval | V1 | M2 | Integration test GET /auth/me with valid + expired tokens |
| FR-005 Password reset | V2 | M4 | Integration test: token TTL, single-use, session invalidation; SendGrid retry queue tested |
| FR-006 Logout | V1 | M2 | Integration test logout revokes refresh family |
| FR-007 Audit event logging | V1, V2 | M2, M4 | V1: every M2 endpoint emits structured event; V2: query API + retention archiver |
| NFR-001 p95 < 200ms | V3 | M5 | k6 load test report; baseline locked in CI |
| NFR-002 500 concurrent | V3 | M5 | k6 load test with 500 VUs sustained |
| NFR-003 99.9% uptime | V3 | M6 | Phase 3 GA observation window; uptime monitor over 30 days |
| NFR-004 bcrypt cost=12 | V1 | M1 | Unit test asserts cost; security regression suite re-asserts |
| NFR-005 JWT RS256 + 2048-bit | V1, V3 | M1, M6 | Configuration validation test (V1); quarterly rotation drill (V3) |
| NFR-006 SOC2 audit retention | V2 | M4 | Audit query API + cron archiver verified; 12-month retention enforced |
| NFR-007 GDPR consent + minimization | V1 | M2 | Schema review (consent_at populated); data minimization audit (only email/hash/displayName) |
| SC-001 Reg conversion > 60% | V3 | M5 | Funnel analytics infrastructure ready in M2; baseline measurement in Phase 1 alpha |
| SC-002 Login p95 < 200ms | V3 | M5 | k6 load test (D5.5) |
| SC-003 Avg session > 30min | V3 | M6 | TokenManager refresh event analytics in production |
| SC-004 Failed login < 5% | V2 | M3 | audit_events query LOGIN_FAILED / LOGIN_TOTAL |
| SC-005 Reset completion > 80% | V2 | M4 | Funnel: RESET_REQUESTED → RESET_COMPLETED |
| SC-006 Token refresh p95 < 100ms | V3 | M5 | k6 load test (D5.5) |
| SC-007 Hash time < 500ms | V1, V3 | M1, M5 | bcrypt benchmark in M1 unit test (V1); verified under load in M5 (V3) |
| SC-008 DAU > 1000 within 30d GA | V3 | M6 | AuthToken issuance counts post-Phase 3 |
