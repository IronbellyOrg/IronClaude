---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 2
work_milestones: 4
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: test-spec-user-auth.md
generated: "2026-04-15T19:12:56.105717+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — User Authentication Service

## Issue Classification

| Severity | Action | Gate Impact |
|---|---|---|
| CRITICAL | stop-and-fix immediately | Blocks current phase |
| MAJOR | stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

## 1. Validation Milestones Mapped to Roadmap Phases

The 1:2 interleave ratio (MEDIUM complexity) places **two validation milestones** across four work phases. Tests are written alongside implementation but validation gates consolidate at V1 and V2.

| Validation Milestone | After Phase | Gate Scope | Key Tests | Exit Criteria |
|---|---|---|---|---|
| **V1** | Phase 2 | Crypto primitives + domain logic | TEST-001 (crypto), TEST-002 (auth service unit) | RS256 sign/verify pass; bcrypt cost-12 verified; all auth service branches covered; replay detection unit-tested |
| **V2** | Phase 4 | Integration + E2E + NFRs | TEST-003..008, TEST-010, TEST-004, TEST-005 | Route integration pass; E2E lifecycle pass; p95 < 200ms; migration rollback verified; SC-1..22 evidenced |

**Phase-level test activity (continuous, not gated):**

| Phase | Tests Written/Run | Purpose |
|---|---|---|
| 1 | TEST-001 (crypto primitives) | Verify RS256 and bcrypt before building on them |
| 2 | TEST-002 drafts (auth service unit stubs) | Validate domain logic as each flow lands |
| 3 | TEST-002 complete, TEST-003, TEST-006..008 | Full unit + integration suites; **V1 gate evaluated here** |
| 4 | TEST-004, TEST-005, TEST-010, NFR-AUTH.1..3 | E2E, load, migration drills; **V2 gate evaluated here** |

## 2. Test Categories

### 2.1 Unit Tests

| Test ID | Scope | What to Assert | Phase |
|---|---|---|---|
| TEST-001 | JwtService, PasswordHasher | RS256 sign→verify round-trip; tampered token rejected; bcrypt hash prefix `$2b$12$`; compare correct/incorrect; timing 200-400ms | 1 |
| TEST-002 | AuthService, TokenManager, AuthRateLimiter, ResetEmailAdapter | Login: valid→tokens, invalid→401 (no enum), locked→403; Register: valid→201, dup→409, weak-pw→rejected; Refresh: valid→rotated pair, replay→global revoke; Reset: token generated, consumed once, expired→400, all sessions revoked; Rate limiter: 6th attempt→429; >90% branch coverage; all dependencies mocked | 3 |

### 2.2 Integration Tests

| Test ID | Scope | What to Assert | Phase |
|---|---|---|---|
| TEST-003 | AuthRoutes end-to-end (DB + HTTP) | Status codes match contracts; cookie flow (httpOnly refresh); Bearer flow (access token); feature flag off → routes disabled; sensitive fields excluded; middleware attaches userId | 3 |
| TEST-006 | Login route | valid→200+tokens; invalid→401 no enumeration; locked→403; 5th+→429; tokens are valid RS256 JWT | 3 |
| TEST-007 | Registration route | valid→201+profile; dup-email→409; weak-pw→400; bad-email→400; user persisted in DB | 3 |
| TEST-008 | Token refresh route | valid-refresh→new pair; expired→401; replay→all tokens revoked; old refresh invalidated | 3 |

### 2.3 End-to-End Tests

| Test ID | Scope | What to Assert | Phase |
|---|---|---|---|
| TEST-004 | Full auth lifecycle | register→login→GET /auth/me→refresh→password reset: all in single test; cookie transport; replay defense; real DB; no mocks | 4 |
| TEST-005 | Migration and recovery | backup-restore pass; down+up migration; rollback under flag-off; reapply clean; no orphan schema | 4 |

### 2.4 Performance / NFR Tests

| Test ID | Scope | What to Assert | Phase |
|---|---|---|---|
| TEST-010 | k6 load tests | login p95 < 200ms; register p95 < 200ms; refresh p95 < 200ms; profile p95 < 200ms; 100 concurrent users baseline | 4 |
| NFR-AUTH.1 | Latency budget | p95 < 200ms in prod-like env; no regressions | 4 |
| NFR-AUTH.2 | Availability | Health check returns 200; PagerDuty alerting configured; SLO published | 4 |
| NFR-AUTH.3 | Hashing benchmark | bcrypt cost factor = 12; hash time ~250ms; unit test + benchmark pass | 4 |

### 2.5 Acceptance Tests (Success Criteria Verification)

SC-1 through SC-22 map directly to the success criteria table in the roadmap. Each SC is verified by specific test IDs already defined. No separate acceptance test suite needed — the existing test matrix covers all 22 criteria.

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

**MEDIUM complexity → 1:2 ratio.** Security sensitivity (0.8) argues for tighter validation, but the bounded component set and well-constrained dependency chain mean two consolidated validation gates suffice. Crypto primitives get immediate test coverage in Phase 1 (TEST-001) as a risk-mitigation exception — a failing RS256 or bcrypt implementation invalidates everything downstream.

### Interleaving Schedule

```
Phase 1 [WORK]     ████████████████  Build crypto + data foundation
  └─ TEST-001       ▓▓▓▓              Crypto primitive tests (immediate, not gated)
Phase 2 [WORK]     ████████████████████  Build auth flows + freeze contracts
  └─ TEST-002 stubs  ▓▓▓▓▓▓            Unit test drafts alongside implementation
─── V1 GATE ─── (evaluated at Phase 3 entry) ───
Phase 3 [WORK+VAL] ████████████████  Routes + middleware + complete test suites
  └─ TEST-002..008   ▓▓▓▓▓▓▓▓▓▓▓▓    Full unit + integration execution
Phase 4 [WORK+VAL] ████████████████  Hardening + NFR + rollout
  └─ TEST-004..010   ▓▓▓▓▓▓▓▓▓▓      E2E + load + migration drills
─── V2 GATE ─── (evaluated before production rollout) ───
```

**Key rule:** Test code is written in the same phase as the implementation it covers. Validation gates consolidate pass/fail decisions at V1 and V2.

## 4. Risk-Based Test Prioritization

Ordered by risk severity × likelihood, mapped to specific test responses:

| Priority | Risk | Test Response | Tests |
|---|---|---|---|
| 1 | R-2: Refresh token replay (High sev, Medium likelihood) | Dedicated replay detection tests in unit AND integration; E2E verifies global revoke | TEST-002 (replay branch), TEST-008, TEST-004 |
| 2 | R-1: Private key exposure (High sev, Low likelihood) | Verify SecretsProvider loads from secrets manager not env; key never in logs; rotation works | TEST-001 (key loading), TEST-005 (rotation drill) |
| 3 | R-6: Feature flag rollback untested (High sev, Low likelihood) | Flag-off disables all routes; rollback drill under load; schema retained | TEST-003 (flag-off), TEST-005 (rollback) |
| 4 | R-4: Email provider latency (Medium sev, Medium likelihood) | Timeout behavior in ResetEmailAdapter; stub provider in integration tests | TEST-002 (adapter timeout), TEST-003 (reset flow) |
| 5 | R-5: Unbounded refresh tokens (Medium sev, Medium likelihood) | Verify eviction policy after OQ-2 resolution; monitor table growth | TEST-008 (rotation creates bounded set) |
| 6 | R-3: bcrypt cost factor degradation (Medium sev, Low likelihood) | Benchmark hash timing; verify cost factor in output | TEST-001, NFR-AUTH.3 |

## 5. Acceptance Criteria per Milestone

### V1 Gate (after Phase 2, evaluated at Phase 3 start)

| # | Criterion | Evidence Required |
|---|---|---|
| 1 | RS256 sign/verify round-trip passes | TEST-001 green |
| 2 | Tampered JWT rejected | TEST-001 green |
| 3 | bcrypt cost factor 12, hash prefix `$2b$12$` | TEST-001 green |
| 4 | bcrypt compare timing 200-400ms | TEST-001 benchmark output |
| 5 | Migration up idempotent, rollback clean | MIG-001, MIG-002, MIG-003 execution logs |
| 6 | All auth service unit test branches pass (>90%) | TEST-002 coverage report |
| 7 | Replay detection triggers global revoke (unit) | TEST-002 replay test case |
| 8 | Rate limiter blocks 6th attempt (unit) | TEST-002 rate limiter case |
| 9 | API contracts frozen (6 endpoints) | API-001..006 contract documents committed |

**V1 blocker policy:** Any CRITICAL or MAJOR failure in items 1-4 (crypto) or 7 (replay) blocks Phase 3 entry.

### V2 Gate (before production rollout OPS-009)

| # | Criterion | Evidence Required |
|---|---|---|
| 1 | All integration tests pass (TEST-003, 006-008) | CI green, report archived |
| 2 | E2E lifecycle test passes (TEST-004) | Full register→login→me→refresh→reset in single run |
| 3 | Migration rollback drill passes (TEST-005) | Down/up/reapply clean |
| 4 | p95 latency < 200ms all endpoints (TEST-010) | k6 report with 100 concurrent users |
| 5 | Health check returns 200 (OPS-002) | HTTP probe evidence |
| 6 | Feature flag off disables routes (TEST-003) | Integration test case |
| 7 | Sensitive fields never in response (TEST-003) | Assertion on profile/login/register responses |
| 8 | SC-1 through SC-22 individually verified | Checklist with test ID mapping |
| 9 | Deployment runbook reviewed (OPS-008) | Sign-off documented |
| 10 | Canary error rate < 0.1% for 4h (OPS-009) | Monitoring dashboard screenshot |

**V2 blocker policy:** Any CRITICAL or MAJOR failure blocks OPS-011 (full rollout). Canary failure triggers immediate rollback per runbook.

## 6. Quality Gates Between Phases

### Phase 1 → Phase 2

| Gate Check | Pass Condition | Severity if Failed |
|---|---|---|
| RSA keys provisioned in secrets manager | SecretsProvider loads without error | CRITICAL |
| Migration up/down verified | MIG-001 + MIG-002 + MIG-003 pass | CRITICAL |
| TEST-001 crypto primitives | All assertions green | CRITICAL |
| Repositories implement CRUD contracts | COMP-008, COMP-009 compile + type-check | MAJOR |
| OQ-6 resolved (REST paths) | Endpoint paths documented | MAJOR |

### Phase 2 → Phase 3 (includes V1 gate)

| Gate Check | Pass Condition | Severity if Failed |
|---|---|---|
| OQ-1 resolved (email sync/queue) | Decision documented, ResetEmailAdapter aligned | MAJOR |
| OQ-2 resolved (max refresh tokens) | Eviction policy in RefreshTokenRepository | MAJOR |
| All 6 API contracts frozen | API-001..006 committed | CRITICAL |
| AuthService + TokenManager unit tests pass | TEST-002 >90% branch coverage | CRITICAL |
| Replay detection verified (unit) | TEST-002 replay case green | CRITICAL |
| Rate limiter verified (unit) | TEST-002 rate limiter case green | MAJOR |

### Phase 3 → Phase 4

| Gate Check | Pass Condition | Severity if Failed |
|---|---|---|
| Integration test suite passes | TEST-003, TEST-006, TEST-007, TEST-008 green | CRITICAL |
| AuthMiddleware extracts + verifies Bearer | TEST-003 middleware cases | CRITICAL |
| Feature flag gate works both directions | TEST-003 flag-off case | MAJOR |
| Cookie policy correct (httpOnly, Secure, SameSite) | TEST-003 cookie assertions | MAJOR |
| AuthConfig fails fast on missing key/invalid TTL | Boot-time validation test | MAJOR |

### Phase 4 → Production (V2 gate)

| Gate Check | Pass Condition | Severity if Failed |
|---|---|---|
| E2E lifecycle passes | TEST-004 green | CRITICAL |
| k6 load test within budget | TEST-010: all endpoints p95 < 200ms | CRITICAL |
| Migration rollback drill passes | TEST-005 clean | CRITICAL |
| Deployment runbook complete + reviewed | OPS-008 sign-off | CRITICAL |
| Canary 10% stable 4h | Error rate < 0.1%, latency within NFR | CRITICAL |
| SC-1..22 verified | Evidence checklist complete | CRITICAL |
| Health check and alerting live | OPS-002 probe + PagerDuty test alert | MAJOR |
| Key rotation procedure documented | OPS-004 runbook exists | MAJOR |

### Gate Failure Protocol

1. **CRITICAL failure:** Phase entry blocked. stop-and-fix immediately. No work on next-phase tasks until resolved.
2. **MAJOR failure:** Current phase may continue. stop-and-fix before next phase transition. Track in defect backlog with phase-gate tag.
3. **MINOR/COSMETIC:** Log in backlog. No gate impact. Address in next sprint or as capacity permits.
