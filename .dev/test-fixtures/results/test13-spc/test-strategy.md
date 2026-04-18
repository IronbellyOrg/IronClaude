---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 6
interleave_ratio: 1:2
major_issue_policy: stop-and-fix
spec_source: test-spec-user-auth.md
generated: "2026-04-17T13:59:50.567852+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — User Authentication Service

## 1. Validation Milestones Mapped to Roadmap

**V1: Foundation & Crypto Validation** | duration: 0.5w (end W4) | exit: V1 covers M1+M2 — DB migration round-trip green, repository CRUD verified, JWT sign/verify exhaustive matrix passes, bcrypt cost=12 + timing band asserted, TokenManager rotation/replay/race scenarios proven.

**V2: Auth Flows & Lifecycle Validation** | duration: 0.5w (end W8) | exit: V2 covers M3+M4 — login/register/refresh/profile end-to-end against real DB, AuthMiddleware route-protection contract enforced, replay-detection triggers revokeAllForUser, ProfileDTO no-leak regression green, refresh httpOnly+Secure+SameSite Set-Cookie attributes asserted, account-lock check covers both login (403) and refresh (401).

**V3: Reset & Production Readiness Validation** | duration: 0.5w (end W12) | exit: V3 covers M5+M6 — full E2E user lifecycle test green, reset flow timing parity (no enumeration) verified, reset invalidates all refresh tokens, NFR-AUTH.1 k6 p95<200ms confirmed, NFR-AUTH.2 staging soak ≥99.9%, feature-flag rollback rehearsal recorded, GAP-1/2/3 plans owned with ADRs filed.

## 2. Test Categories

| Category | Scope | Where | Tools |
|---|---|---|---|
| Unit | Single component in isolation; pure logic, no I/O | Each COMP-xxx + SEC-xxx + validator | jest/vitest, mocks |
| Integration | Cross-component or component+DB; real Postgres container | Repos, TokenManager, AuthService flows | testcontainers, supertest |
| Contract | API request/response schema, Set-Cookie attrs, DTO allowlist | API-001…API-006, SEC-007 | json-schema, header lint |
| E2E | Full lifecycle through HTTP stack | TEST-M6-001 register→login→me→refresh→reset→relogin | supertest/playwright |
| Acceptance | NFR validation under load, dependency health, rollback | NFR-AUTH.1/2/3, OPS-009, OPS-002 | k6, synthetic probes |
| Security | Replay, enumeration, leakage, cookie policy, log redaction | SEC-001..SEC-007, R6/R7/R9 | targeted fuzz, header lint, response diff |

## 3. Test-Implementation Interleaving — 1:2 Ratio Justification

**Rationale (MEDIUM=0.6):** Bounded scope (5 FRs, 6 endpoints) with cryptographic rigor warrants validation every two work milestones. Validating after M2 catches crypto contract drift before flow code consumes TokenManager; validating after M4 catches replay/cookie regressions before reset reuses revokeAllForUser; validating after M6 gates production cutover. Per-milestone unit tests run continuously inside each M (TEST-M{N}-xxx), but cross-milestone validation sweeps occur at the three V points. Continuous-parallel: unit/integration tests are written alongside each deliverable in M1–M6 (already enumerated TEST-Mx-xxx); the V milestones are explicit gate checkpoints, not the only place tests exist.

## 4. Risk-Based Test Prioritization

| Priority | Risk | Test Focus | Milestone |
|---|---|---|---|
| P0-CRIT | R1 JWT key compromise | RS256-only verify, kid-rotation, HS256 rejection (TEST-M2-001) | V1 |
| P0-CRIT | R2 Refresh replay | Rotation + replay→revokeAll + race-safety (TEST-M4-002) | V2 |
| P0-CRIT | R7 httpOnly misconfig | Set-Cookie attribute contract per response | V2 |
| P0-CRIT | R8 Migration irreversible | down→up idempotence in CI (TEST-M1-001) | V1 |
| P0-CRIT | R9 Reset token in logs | Log-redaction middleware test; no querystring delivery | V3 |
| P0-HIGH | R6 Enumeration | Identical 401 body + ±10% latency band (TEST-M3-002), 202 reset parity (TEST-M5-001) | V2/V3 |
| P0-HIGH | Race on refresh | Concurrent refresh → at most one live pair (TEST-M2-003 + M4) | V1/V2 |
| P1-MED | R10 Latency under load | k6 50rps 10m p95<200ms (NFR-AUTH.1) | V3 |
| P1-MED | R11 Email outage | Async dispatch path; provider-mock failure does not 5xx API-005 | V3 |
| P1-MED | R3 bcrypt cost | Cost prefix + 200–300ms benchmark (TEST-M2-002) | V1 |
| P2-LOW | R12 Audit gap | GAP-2 ADR existence check | V3 |

## 5. Acceptance Criteria per Milestone

**M1: Foundation** | exit: migration up/down idempotent in CI | Postgres container starts, schema matches DM-001/DM-002, FK cascade verified, repo CRUD passes, RSA keys fetchable from secrets manager dry-run, libs pinned + SCA clean.

**M2: Crypto & Token** | exit: token contracts locked | TEST-M2-001/002/003 green; JWT rejects HS256/expired/tampered/wrong-key; bcrypt embeds cost=12; TokenManager.refresh rotates atomically; replay of revoked hash invokes revokeAllForUser; concurrent refresh yields ≤1 live pair.

**M3: Login/Register/Middleware** | exit: public auth surface live | TEST-M3-001…005 green; identical 401 body + latency band on bad creds; 403 on locked; 409 on duplicate email; rate limiter 6th call→429 with Retry-After; AuthMiddleware blocks protected routes without Bearer; account-lock hook centralized.

**M4: Refresh/Profile** | exit: lifecycle + cookie policy locked | TEST-M4-001/002/003 green; refresh rotates and revokes prior; replay→revokeAllForUser + audit event; row-lock prevents double-issue race; ProfileDTO returns allowlist only (password_hash/token_hash/is_locked never serialized); Set-Cookie has HttpOnly+Secure+SameSite=Strict+Path=/auth+Max-Age=7d; refresh on locked user→401.

**M5: Password Reset** | exit: reset flow safe and async-correct | OI-1-DEC ADR filed; TEST-M5-001/002/003 green; 202 timing parity for known/unknown email; token expires at 1h boundary (59m accept, 61m reject); single-use enforced; successful reset revokes all refresh tokens in same transaction; provider mock failure does not leak recipient existence.

**M6: Wiring/Rollout/Validation** | exit: production cutover signed | TEST-M6-001 E2E green; TEST-M6-002 flag-toggle rollback green (in-flight requests complete, new return 404 when off); k6 p95<200ms at 50rps for 10m on /login + /refresh; staging soak ≥99.9% over 30 days; /health/auth reports per-dependency status correctly under induced failures; PagerDuty drill alert routes verified; GAP-1/2/3 plans have named owners + ADRs.

## 6. Quality Gates Between Milestones

| Gate | Position | Pass Conditions | Block Action |
|---|---|---|---|
| G1 | M1→M2 | Migration round-trip + repo CRUD green; secrets fetch dry-run OK | CRITICAL: stop-and-fix; foundation drift contaminates all crypto |
| G2 | M2→M3 (V1 sweep) | All TEST-M2-xxx green; bcrypt benchmark in band; replay-detection unit-proven; HS256 rejection asserted | MAJOR: stop-and-fix before M3; THS will inherit defects |
| G3 | M3→M4 | Login/register/middleware integration green; rate-limit enforced; account-lock centralized; no enumeration in 401 body or latency | MAJOR: stop-and-fix; refresh path reuses lock check |
| G4 | M4→M5 (V2 sweep) | Refresh replay→revokeAll green; ProfileDTO no-leak regression green; Set-Cookie contract green; race test green | MAJOR: stop-and-fix before M5; reset depends on revokeAll path |
| G5 | M5→M6 | OI-1-DEC ADR filed; reset TTL/single-use/invalidate-all green; timing parity asserted; log-redaction verified | MAJOR: stop-and-fix; production cutover requires reset-flow safety |
| G6 | M6→Release (V3 sweep) | E2E green; k6 NFR-AUTH.1 pass; staging soak NFR-AUTH.2 pass; flag rollback rehearsed; GAP-1/2/3 owned + ADRs | CRITICAL: stop-and-fix; do not flip phase-1→phase-2 cutover |

**Issue handling at every gate:** CRITICAL halts current milestone immediately. MAJOR halts the next milestone until resolved. MINOR is logged to next sprint backlog without gate impact. COSMETIC goes to general backlog.
