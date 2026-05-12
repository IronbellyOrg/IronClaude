---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 5
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: test-spec-user-auth.md
generated: "2026-04-03T14:39:38.026995+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy: User Authentication Service

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

**Examples specific to this project**:
- CRITICAL: Plaintext password stored in DB, JWT signed with wrong algorithm, replay detection fails to revoke tokens
- MAJOR: Rate limiter allows 6th request, sensitive field leaked in profile response, cookie missing `HttpOnly` flag
- MINOR: Error message wording inconsistent across endpoints, bcrypt timing 310ms instead of ~250ms
- COSMETIC: OpenAPI description typos, log message formatting

---

## 1. Validation Milestones Mapped to Roadmap Phases

### VM-1: Foundation + Core Logic Validation (after Phase 2)

**Covers**: Phase 1 (Foundation Layer) + Phase 2 (Core Auth Logic)

| What to Validate | Method | Success Criteria |
|------------------|--------|-----------------|
| Crypto correctness: bcrypt hash/verify round-trip | Unit test | 100% pass; timing 200–400ms |
| Crypto correctness: JWT RS256 sign/verify, reject tampered/expired | Unit test | All 4 failure modes covered |
| Migration reversibility: up then down yields clean state | Automated migration test | Zero residual schema objects |
| DI wiring: all singletons resolve, mocks injectable | Integration test | Container resolves all 4 services |
| TokenManager: issue, rotate, replay-detect, expiry, cap at 5 | Unit test against real DB | 6+ test cases pass |
| AuthService: all 5 flows (login, register, profile, reset-request, reset-confirm) | Unit test | 15+ test cases pass (happy + error paths) |
| Feature flag: `AUTH_SERVICE_ENABLED=false` returns expected status | Integration test | Routes not registered |
| Crypto review gate: security engineer sign-off | Manual code review | Written sign-off on PasswordHasher + JwtService |
| SC-5 partial: all unit tests pass for 4 services | Test suite run | Green across PasswordHasher, JwtService, TokenManager, AuthService |

**Gate decision**: All unit tests green + crypto review signed off. Any MAJOR+ crypto issue (wrong algorithm, key leakage, broken replay detection) is stop-and-fix.

### VM-2: Integration + Hardening Validation (after Phase 4)

**Covers**: Phase 3 (Integration Layer) + Phase 4 (Hardening and Validation)

| What to Validate | Method | Success Criteria |
|------------------|--------|-----------------|
| E2E lifecycle: register → login → profile → refresh → reset → re-login | E2E test against real DB | Completes without error (SC-7) |
| Token refresh rotation: old token rejected after refresh | Integration test | 401 on old token |
| Replay detection E2E: reuse revoked token → all tokens revoked | Integration test | Verified via DB query |
| Sensitive field filtering: no `password_hash` or `refresh_token_hash` in any response | Automated response schema scan | Zero leaks across all 6 endpoints (SC-8) |
| Rate limiting: 6th login attempt within 1 min returns 429 | Integration test | 429 on attempt 6 |
| Performance: p95 < 200ms at defined load for login and refresh | k6 load test | SC-2 passes |
| Coverage: ≥90% line, ≥85% branch | Coverage report | Thresholds met |
| Security suite: cookie attributes, JWT validation, information leakage, password policy boundary values | Dedicated security test suite | All pass |
| Rollback: flag=false + down-migrations | Integration test | Pre-auth behavior restored (SC-9) |

**Gate decision**: SC-1 through SC-9 validated (except SC-3 which is post-deploy). Any security test failure is CRITICAL. Coverage shortfall is MAJOR.

### VM-3: Production Readiness Validation (after Phase 5)

**Covers**: Phase 5 (Production Readiness)

| What to Validate | Method | Success Criteria |
|------------------|--------|-----------------|
| Secrets manager integration: keys load from vault | Integration test in staging | Service starts and signs JWTs |
| Key rotation: old key still verifies during grace period | Integration test | Tokens signed with old key accepted |
| Monitoring: alerts fire on simulated conditions (error rate, latency, replay) | Staged alert test | All 5 alert rules trigger |
| CI pipeline: full suite runs, fails on coverage < 90% | Pipeline execution | End-to-end green |
| Gradual rollout: flag off → on at 10% → 100% | Staging deployment | Traffic routing correct at each step |
| Rollback < 5 minutes | Timed drill | Clock stops under 5 min |
| Documentation: OpenAPI spec matches implementation | Schema diff tool | Zero undocumented endpoints/fields |

**Gate decision**: Production deployment approved only when all items pass. Missing monitoring is MAJOR. Missing runbook is MINOR.

---

## 2. Test Categories

### Unit Tests (~60 tests)

| Component | Test Count | Key Scenarios |
|-----------|-----------|---------------|
| PasswordHasher | 6 | hash round-trip, timing benchmark, cost factor 12, empty input, unicode handling, verify with wrong hash |
| Password policy validator | 8 | min length, uppercase, lowercase, digit, all-valid, boundary (exactly 8 chars), unicode, empty |
| JwtService | 8 | sign/verify round-trip, expired rejection, tampered payload, tampered signature, wrong algorithm, missing claims, key mismatch, null input |
| TokenManager | 10 | issue pair, rotate, replay detection, expiry, cap enforcement (6th token revokes oldest), revoke all, hash storage verification, concurrent rotation, atomic transaction |
| AuthService.login | 6 | valid credentials, wrong password, wrong email, locked account, generic 401 message, rate limit boundary |
| AuthService.register | 6 | valid registration, duplicate email (409), invalid email format, weak password, missing fields, SQL injection attempt |
| AuthService.getProfile | 4 | valid token, expired token, sensitive field exclusion, non-existent user |
| AuthService.requestPasswordReset | 4 | registered email, unregistered email (still 200), token TTL = 1hr, email dispatch called |
| AuthService.resetPassword | 6 | valid reset, expired token, invalid token, password updated, old tokens revoked, reset token single-use |
| Feature flag | 2 | enabled vs disabled behavior |

### Integration Tests (~15 tests)

| Flow | Test Count | Scope |
|------|-----------|-------|
| Login flow (register → login → verify token) | 2 | DB + services + JWT |
| Token refresh with rotation | 3 | DB + TokenManager + cookie handling |
| Password reset lifecycle | 3 | DB + email service mock + token invalidation |
| Sensitive field filtering (all endpoints) | 1 | Response body scan across 6 routes |
| Rate limiting | 2 | Timing-sensitive, 5 req/min boundary |
| Auth middleware (valid/invalid/missing token) | 3 | Middleware + JwtService |
| Feature flag toggle | 1 | Route registration conditional |

### E2E Tests (~3 tests)

| Scenario | Description |
|----------|-------------|
| Full user lifecycle | register → login → profile → refresh → reset → re-login |
| Multi-device simulation | Login from 2 devices, refresh one, verify other still valid |
| Replay attack scenario | Steal token → legitimate refresh → attacker reuses old token → all sessions revoked |

### Security Tests (~12 tests)

| Category | Tests |
|----------|-------|
| Cookie attributes | httpOnly, Secure, SameSite=Strict on refresh token |
| Information leakage | Generic 401 messages, no email enumeration on reset |
| JWT attack surface | Tampered JWT, expired JWT, `alg:none` attack, wrong key |
| Sensitive data | No password_hash in any response, no plaintext in DB |
| Injection | SQL injection in email/password fields, XSS in display_name |
| Crypto verification | RS256 4096-bit key size, bcrypt cost factor 12 |

### Performance Tests (~4 tests)

| Endpoint | Load Profile | Target |
|----------|-------------|--------|
| POST /auth/login | 100 concurrent, 50 req/s | p95 < 200ms |
| POST /auth/refresh | 100 concurrent, 50 req/s | p95 < 200ms |
| POST /auth/register | 50 concurrent, 25 req/s | Document baseline (bcrypt-bound) |
| Bcrypt benchmark | Single-threaded | ~250ms per hash |

---

## 3. Test-Implementation Interleaving Strategy

**Ratio**: 1:2 (one validation milestone per two work phases)

**Justification**: MEDIUM complexity (0.6) warrants validation after paired phases rather than after every phase. The primary complexity drivers — cryptographic correctness and replay detection — are concentrated in Phases 1–2. Validating after each individual phase would add overhead without proportional risk reduction, since Phase 1 components can't be meaningfully integration-tested until Phase 2 services consume them.

**Interleave schedule**:

```
Phase 1 (Foundation)     ─── build ───┐
Phase 2 (Core Auth)      ─── build ───┤
                                      └── VM-1: Foundation + Core Logic Validation
Phase 3 (Integration)    ─── build ───┐
Phase 4 (Hardening)      ─── build ───┤
                                      └── VM-2: Integration + Hardening Validation
Phase 5 (Prod Readiness) ─── build ───┐
                                      └── VM-3: Production Readiness Validation
```

**Continuous testing within phases** (not gated, but executed during development):
- Unit tests run on every commit during Phases 1–2
- Integration tests run on every PR merge during Phases 3–4
- Security and performance tests run nightly from Phase 3 onward

---

## 4. Risk-Based Test Prioritization

Tests ordered by risk severity and probability:

| Priority | Risk | Tests to Run First | Rationale |
|----------|------|--------------------|-----------|
| P0 | RISK-2: Refresh token replay | Replay detection unit test, E2E replay scenario | HIGH severity, MEDIUM probability; failure = persistent unauthorized access |
| P0 | RISK-1: JWT key compromise | RS256 key size verification, no-key-in-logs test, secrets manager integration | HIGH severity; failure = forged tokens |
| P1 | Sensitive data leakage (SC-8) | Response schema scan, no-plaintext-in-DB audit | Compliance-critical; easy to miss during development |
| P1 | Cookie security | httpOnly/Secure/SameSite attribute verification | XSS vector if wrong; one-line fix but high impact |
| P2 | RISK-5: Brute force | Rate limiter boundary test (5th vs 6th attempt) | MEDIUM severity; off-by-one errors common |
| P2 | Password policy | Boundary value tests for FR-AUTH.2c | MEDIUM severity; incorrect enforcement is a regulatory risk |
| P3 | RISK-3: bcrypt obsolescence | Cost factor verification, timing benchmark | LOW probability; configurable mitigates |
| P3 | RISK-4: Email service | Email dispatch called (mock), always-200 on reset request | MEDIUM probability but limited blast radius |

---

## 5. Acceptance Criteria Per Milestone

### VM-1 Acceptance Criteria

- [ ] All 60 unit tests pass (zero failures)
- [ ] Crypto review gate: written sign-off from security engineer
- [ ] bcrypt timing within 200–400ms range at cost factor 12
- [ ] JWT sign/verify < 50ms
- [ ] Migrations run up and down cleanly (automated test)
- [ ] DI container resolves all 4 services without runtime errors
- [ ] Replay detection works against real database (not mocks)
- [ ] Feature flag disables route registration
- [ ] No CRITICAL or MAJOR issues open

### VM-2 Acceptance Criteria

- [ ] SC-1: All FR-AUTH.1–5 acceptance criteria pass
- [ ] SC-2: p95 < 200ms at 100 concurrent / 50 req/s
- [ ] SC-4: bcrypt cost 12 confirmed under load
- [ ] SC-5: All unit tests pass
- [ ] SC-6: All integration tests pass
- [ ] SC-7: E2E lifecycle completes
- [ ] SC-8: No sensitive fields in any response (automated scan)
- [ ] SC-9: Feature flag rollback verified
- [ ] Line coverage ≥ 90%, branch coverage ≥ 85%
- [ ] All 12 security tests pass
- [ ] No CRITICAL or MAJOR issues open

### VM-3 Acceptance Criteria

- [ ] Secrets load from vault; service starts and operates
- [ ] Key rotation with grace period works
- [ ] All 5 monitoring alerts fire on simulated conditions
- [ ] CI pipeline runs full suite and enforces coverage gate
- [ ] Gradual rollout executes without errors
- [ ] Rollback completes in < 5 minutes
- [ ] OpenAPI spec matches implementation (zero drift)
- [ ] Runbooks reviewed and approved
- [ ] SC-3 monitoring configured (30-day measurement begins post-deploy)
- [ ] No CRITICAL or MAJOR issues open

---

## 6. Quality Gates Between Phases

### Gate 1→2: Foundation Complete

| Check | Pass Condition | Blocking? |
|-------|---------------|-----------|
| Unit tests (PasswordHasher, JwtService) | All green | Yes |
| Crypto review | Signed off | Yes — CRITICAL if not |
| Migration reversibility | Automated test passes | Yes |
| DI wiring | Container resolves | Yes |
| Bcrypt timing | 200–400ms | Yes (MAJOR if out of range) |

### Gate 2→3: Core Logic Complete

| Check | Pass Condition | Blocking? |
|-------|---------------|-----------|
| All Phase 2 unit tests | Green (15+ AuthService, 6+ TokenManager) | Yes |
| Replay detection | Works against real DB | Yes — CRITICAL |
| Token cap enforcement | 6th token revokes oldest | Yes |
| Feature flag | Disables auth routes | Yes |

### Gate 3→4: Integration Complete

| Check | Pass Condition | Blocking? |
|-------|---------------|-----------|
| E2E lifecycle | Completes | Yes |
| Sensitive field scan | Zero leaks | Yes — CRITICAL |
| Rate limiter | 429 on 6th attempt | Yes — MAJOR |
| All integration tests | Green | Yes |

### Gate 4→5: Hardening Complete

| Check | Pass Condition | Blocking? |
|-------|---------------|-----------|
| Security test suite | All 12 pass | Yes — any failure is CRITICAL |
| Performance targets | p95 < 200ms | Yes — MAJOR |
| Coverage | ≥90% line, ≥85% branch | Yes — MAJOR |
| Rollback | Flag=false works | Yes |

### Gate 5→Deploy: Production Ready

| Check | Pass Condition | Blocking? |
|-------|---------------|-----------|
| Secrets manager | Keys load, rotation works | Yes — CRITICAL |
| Monitoring | All alerts configured and tested | Yes — MAJOR |
| CI pipeline | End-to-end green | Yes |
| Documentation | OpenAPI + runbooks reviewed | Yes — MAJOR |
| Rollback drill | < 5 minutes | Yes |
