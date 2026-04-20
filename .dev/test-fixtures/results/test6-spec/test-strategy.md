---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 5
interleave_ratio: 1:2
major_issue_policy: stop-and-fix
spec_source: test-spec-user-auth.md
generated: "2026-04-20T21:06:14.264604+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — User Authentication Service

## 1. Validation Milestones Mapped to Roadmap

**V1: Foundation & Primitives Validation** | after M2 | gates entry to M3
**V2: Service & NFR Validation** | after M4 | gates entry to M5
**V3: Release Acceptance Validation** | concurrent with M5 | gates GA flag-flip

Interleaving: V1 covers M1+M2 (2 work), V2 covers M3+M4 (2 work), V3 covers M5 (1 work). 1:2 ratio justified by MEDIUM complexity (0.6): risk profile 0.7 is elevated but testability 0.3 plus leaf-first layering mean primitives can be independently verified, so a validation gate every two work milestones catches cryptographic/persistence regressions early without stalling feature delivery. HIGH would demand per-milestone gates; LOW would tolerate one mid-point gate only.

## 2. Test Categories

| Category | Scope | Tooling | Gate |
|---|---|---|---|
| Unit | Pure functions, primitives, validators, repositories | jest/vitest + in-memory DB | V1 |
| Integration | Handler → service → repository → DB; middleware pipeline; email mock | supertest + testcontainers PG + Redis | V2 |
| E2E | Full lifecycle against staging through `/auth/*` with real secrets manager and email sandbox | playwright/k6 scripts | V3 |
| Acceptance (SC) | SC-1..SC-8 success criteria as executable checks | k6 + scripted E2E + config-snapshot diff | V3 |
| Security | Negative tests for alg=none, replay, enumeration, rate-limit bypass, JWT tampering | custom jest + pentest (SEC-003) | V2, V3 |
| Performance | Latency p95 < 200ms, bcrypt timing band 200–350ms | k6 (OPS-004), SEC-001 CI benchmark | V2 |
| Chaos / Resilience | Secrets manager outage, email vendor outage, rollback drill | fault injection + OPS-006 rehearsal | V3 |

## 3. Test-Implementation Interleaving Strategy

Tests ship in the same PR as their target code; no milestone exits with test debt. Primitives (M2) are fully covered before orchestrator (M3) composes them. Each validation milestone runs the full suite up to that point plus the new category added at that gate.

| Work | Tests Added In-PR | Validation Gate |
|---|---|---|
| M1 | TEST-M1-001/002/003 (unit + CI migration cycle) | rolled into V1 |
| M2 | TEST-M2-001..006 (unit + benchmark + replay) | **V1 runs here** |
| M3 | TEST-M3-001..006 (integration) | rolled into V2 |
| M4 | OPS-004 k6, SEC-001 benchmark, AUDIT-001 event tests | **V2 runs here** |
| M5 | SC-1..SC-8 acceptance, SEC-003 pentest, OPS-006 drill | **V3 runs here** |

## 4. Risk-Based Prioritization

Priority derived from Risk Register impact×probability:

**P0 (highest) — security & data loss:**
- R-001 key compromise → TEST-M2-002 alg whitelist; key-rotation drill
- R-002 refresh replay → TEST-M2-005 + TEST-M3-003 (SC-7)
- R-007 irreversible migration → TEST-M1-003 up/down/up CI gate
- R-009 alg=none → explicit negative in TEST-M2-002
- R-017 rollback failure → OPS-006 staging drill

**P1 — latency & availability:**
- R-014 p95 > 200ms → OPS-004 k6 pre-GA (SC-1)
- R-008 secrets cold-start → chaos test in V3
- R-015 false-green health → synthetic login probe in V3
- R-012 email outage → mocked failure + retry assertions in TEST-M3-005

**P2 — enumeration / state sharing:**
- R-011 user enumeration → TEST-M3-006
- R-013 rate-limit state sharing → multi-instance integration test

**P3 — deferred (release-notes disclosure only):** R-004, R-005, R-006

## 5. Acceptance Criteria per Milestone

**M1 exit:** migrations reversible in CI (up→down→up green); RSA keypair 2048-bit+ in secrets manager; `AUTH_SERVICE_ENABLED=false` blocks route registration; UserRepository + RefreshTokenRepository unit tests at 100% branch coverage on CRUD + revocation.

**M2 exit (== V1 gate):** bcrypt cost=12 asserted from hash string; SEC-001 p95 within 200–350ms CI band; RS256 sign/verify round-trip green; alg=none / HS256 / expired / tampered all rejected; dual-key verification passes during grace window; replay of rotated refresh token triggers `revokeAllForUser` with emitted event; VALID-001/002 truth tables pass.

**M3 exit:** all 5 `/auth/*` endpoints live behind flag; TEST-M3-001..006 green; ERR-001 uniform 401 body verified (enumeration guard); COOKIE-001 sets httpOnly+Secure+SameSite=Strict with `path=/auth/refresh`; DTO-001 introspection proves no `password_hash`/`token_hash` leak on any response; email dispatch observable via mock.

**M4 exit (== V2 gate):** k6 p95 < 200ms on staging for all 5 endpoints; `/healthz` validates DB + secrets + key-cache in <50ms p95; PagerDuty rules fire on 5xx burst, p95 regression, replay-burst; SEC-001 artifact attached to CI run; APM traces cover handler→AuthService→TokenManager→repository.

**M5 exit (== V3 gate):** SC-1..SC-8 all green with evidence links; SEC-002 architect sign-off filed; SEC-003 pentest report shows zero criticals; OPS-006 rollback drill report attached with measured MTTR; FF-001 canary→25%→100% executed; BC-001 smoke matrix green on unauthenticated routes pre/post flip.

## 6. Quality Gates Between Milestones

| Gate | Entry Check | Tests Required Green | Issue Policy |
|---|---|---|---|
| M1→M2 | OI-9, OI-10 resolved; RISK-1 policy drafted | TEST-M1-001/002/003 | CRITICAL blocks; MAJOR blocks next milestone |
| V1 (M2→M3) | M2 exit criteria met | all M1+M2 tests; alg whitelist; replay detection | **stop-and-fix** on CRITICAL/MAJOR; OI-3/4/5 must have resolution plan |
| M3→M4 | OI-3/4/5 landed; flag still off in prod | TEST-M3-001..006 + DTO-001 introspection | MAJOR blocks M4 entry |
| V2 (M4→M5) | NFR instrumentation live in staging | OPS-004 k6 p95<200ms; SEC-001 band; PagerDuty test-page acknowledged | **stop-and-fix**; R-014 regression blocks release |
| V3 (release) | SC-1..SC-8 mechanically verifiable; SEC-002 draft ready | full suite + SEC-003 pentest + OPS-006 drill | CRITICAL blocks flag-flip; MAJOR blocks 100% rollout (canary allowed); MINOR/COSMETIC tracked in v1.1 backlog |

## 7. Per-Milestone Test Focus (specific)

**M1:** schema hash equality after up/down/up; unique-email constraint violation path; FK cascade on `refresh_tokens.user_id`; `updatePasswordHash` bumps `updated_at`; `revokeAllForUser` marks every active row revoked; pruning excludes expired rows on read; secrets-manager cold fetch <500ms; flag=false means no `/auth/*` route registered (introspect route table).

**M2:** bcrypt cost extracted from `$2b$12$...` prefix; compare is constant-time on mismatch; JWT `kid` header present and matches active key id; verify rejects missing `exp`, `nbf` skew > tolerance, wrong `iss`; TokenManager issues DM-003 with exact TTLs (access=900s, refresh=604800s); SHA-256 hash comparison uses `timingSafeEqual`; replay detection emits audit event with user_id + token_id (not plaintext).

**M3:** login 200/401/403/429 matrix including identical body for invalid-email vs invalid-password (R-011); register 201/400/409 including password policy boundary (7 chars fails, 8 chars with all classes passes); refresh rotates and old token→401 on second use; `/auth/me` rejects expired token and omits `password_hash` + `token_hash` fields (DTO-001 introspection on JSON); password reset request always returns 202 (enumeration guard); confirm revokes all refresh tokens for user (query `refresh_tokens where user_id=X and revoked=false` returns 0).

**M4:** k6 scenario ramps to realistic RPS on all 5 endpoints; p95 per-endpoint panel published; health endpoint returns 503 when DB ping fails (fault-inject); PagerDuty test-page acknowledged end-to-end; SEC-001 asserts 200ms ≤ p95 ≤ 350ms on reference CI hardware with env-var override documented; AUDIT-001 events visible in observability sink with PII redacted.

**M5:** SC-8 E2E script: register→login→`/auth/me`→refresh→reset→login-with-new-password, green in staging and re-run post-flag-flip in prod; SEC-003 targets enumeration, brute force, replay, JWT confusion, cookie scope bypass; OPS-006 drill measures MTTR for flag-off + migration rollback and compares to documented SLO; BC-001 confirms unauthenticated endpoints unchanged; DOC-001 OpenAPI drift test in CI.

## 8. Issue Classification Applied

| Example Finding | Severity | Action |
|---|---|---|
| alg=none accepted by JwtService | CRITICAL | stop-and-fix immediately; block M2 exit |
| p95 = 240ms on `/auth/login` | MAJOR | stop-and-fix before M5; tune repository caching or capacity |
| Audit event missing user_id on replay | MAJOR | fix before V3 gate |
| Rate-limit counter not shared across instances in staging | MAJOR | fix before V2 gate (R-013) |
| OpenAPI example payload outdated | MINOR | next sprint |
| Grafana panel label typo | COSMETIC | backlog |
