---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
debate_rounds: null
generated: "2026-04-15"
generator: "single"
total_phases: 5
total_task_rows: 72
risk_count: 9
open_questions: 11
---

# User Authentication Service — Project Roadmap

## Executive Summary

User Authentication Service is the enabling layer for Q2-Q3 personalization and the minimum viable identity boundary for SOC2-ready auditability. The roadmap front-loads contract decisions, crypto/storage foundations, and backend services before frontend adoption, then reserves hardening and rollout for compliance, SLO validation, and operational readiness.

**Business Impact:** Unblocks personalized experiences tied to roughly $2.4M projected annual revenue, removes known plaintext-password and duplicated-session risks, and establishes authenticated event trails ahead of the Q3 2026 compliance review.

**Complexity:** MEDIUM (0.6) — bounded functional scope, but high security sensitivity, cross-surface integration (backend, frontend, DB, infra), and unresolved source conflicts around rate limiting, token storage, and schema contracts.

**Critical path:** Resolve spec/TDD deltas → finalize schemas and migrations → ship `JwtService`/`PasswordHasher` → implement `TokenManager`/`AuthService` → wire middleware, routes, and `AuthProvider` → validate NFRs → stage rollout behind feature flags.

**Key architectural decisions:**

- Use RS256 JWT access tokens with 2048-bit RSA keys and explicit key-rotation operations.
- Encapsulate bcrypt cost factor 12 behind `PasswordHasher` so security posture can evolve without API churn.
- Keep access auth stateless, store access tokens only in client memory, and rotate refresh tokens with replay detection.

**Open risks requiring resolution before Phase 1:**

- Login throttling differs between sources (`5/min/IP` in spec vs `10/min/IP` in TDD), which changes gateway policy and brute-force posture.
- Refresh-token persistence differs between sources (PostgreSQL table vs Redis store), which changes migration shape, replay detection, and rollback design.
- Contract drift across `UserRecord`/`UserProfile`, missing logout definition, and missing admin audit-query scope must be normalized before API and frontend wiring.

## Phase 1: Foundation

**Phase 1** | Freeze contracts, schemas, crypto, and ingress | Duration: 1.5 weeks | Exit: schema, migration, RS256, bcrypt, and `/v1/auth/*` baseline approved

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-013 | Baseline API gateway auth chain | Infra | — | role:gateway; concerns:rate-limiting\|CORS; ingress:AuthService; policies:login-throttle+origin-allowlist | L | P0 |
| 2 | DM-001 | Finalize UserRecord/UserProfile schema | DB | — | id:UUIDv4; email:unique+idx+lower; display_name/displayName:str; password_hash:bcrypt; is_locked:bool; created_at/createdAt:ts; updated_at/updatedAt:ts; lastLoginAt:nullable-ts; roles:string[] | L | P0 |
| 3 | DM-002 | Finalize RefreshTokenRecord schema | DB | DM-001 | id:UUIDv4; user_id:fk→UserRecord.id; token_hash:sha256; expires_at:ts; revoked:bool; created_at:ts | M | P0 |
| 4 | DM-003 | Finalize AuthTokenPair/AuthToken | API | DM-001 | access_token/accessToken:jwt-15m; refresh_token/refreshToken:opaque-7d; expiresIn:900; tokenType:Bearer | S | P0 |
| 5 | COMP-012 | Build auth table migration | DB | DM-001,DM-002 | path:src/database/migrations/003-auth-tables.ts; tables:users\|refresh_tokens; up:apply; down:revert | L | P0 |
| 6 | COMP-003 | Implement JwtService | Sec | DM-003 | path:src/auth/jwt-service.ts; ops:sign\|verify; alg:RS256; keys:RSA2048; lib:jsonwebtoken | M | P0 |
| 7 | COMP-004 | Implement PasswordHasher | Sec | DM-001 | path:src/auth/password-hasher.ts; ops:hash\|compare; alg:bcrypt; cost:12; lib:bcryptjs | M | P0 |
| 8 | NFR-AUTH.3 | Enforce bcrypt security budget | Sec | COMP-004 | cost:12; hash≈250-500ms; unit+bench:pass; config:reviewable | S | P0 |
| 9 | NFR-SEC-002 | Enforce RS256 key policy | Sec | COMP-003 | alg:RS256; keylen:2048; config-test:pass; symmetric:none | S | P0 |
| 10 | NFR-003 | Block raw password persistence | Sec | COMP-004,COMP-013 | raw-password:never-store; raw-password:never-log; scan+review:pass | M | P0 |
| 11 | NFR-004 | Constrain auth data collection | DB | DM-001 | collect:email\|hashed-password\|displayName; extra-PII:none; schema-review:pass | S | P1 |
| 12 | API-008 | Freeze /v1/auth API versioning | API | COMP-013 | prefix:/v1/auth/*; breaking→new-major; additive→compatible; routes+docs aligned | S | P1 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| API Gateway policy chain | middleware chain | rate-limit+CORS→AuthService ingress | 1 | API-001,API-002,API-003,API-004,API-005,API-006 |
| AuthService DI contract | dependency injection | AuthService→TokenManager\|PasswordHasher\|UserRepo | 1 | COMP-001 |
| Token signing strategy | strategy | TokenManager→JwtService(RS256) | 1 | COMP-002,COMP-005 |
| Schema migration chain | migration chain | users+refresh_tokens→PostgreSQL | 1 | COMP-010,API-001,API-002,API-004 |

## Phase 2: Core Logic

**Phase 2** | Build repositories, token lifecycle, and auth flows | Duration: 2 weeks | Exit: login, registration, refresh, reset, logout, and audit-core logic pass service tests

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-010 | Implement UserRepo | DB | DM-001,COMP-012 | role:UserProfile-CRUD; store:PostgreSQL; ops:create\|findByEmail\|findById\|updateLastLogin\|lock; dep:PostgreSQL | L | P0 |
| 2 | COMP-002 | Implement TokenManager | Sec | COMP-003,DM-002,DM-003 | path:src/auth/token-manager.ts; role:jwt-lifecycle-mgmt; ops:issue\|refresh\|revoke; storage:Redis/PostgreSQL-decision; replay-detect:on; dep:JwtService | L | P0 |
| 3 | COMP-001 | Implement AuthService | API | COMP-002,COMP-004,COMP-010 | path:src/auth/auth-service.ts; role:auth-orchestrator; flows:login\|register\|refresh\|reset; deps:TokenManager\|PasswordHasher\|UserRepo; facade:on | XL | P0 |
| 4 | FR-AUTH.2 | Implement registration flow | API | COMP-001,COMP-010,COMP-004 | valid(email+password+displayName)→201+profile; duplicate→409; pwd:min8+upper+lower+digit; email-format:checked | L | P0 |
| 5 | FR-AUTH.1 | Implement login flow | API | COMP-001,COMP-002,COMP-004,COMP-010 | valid→200+access15m+refresh7d; invalid→401+generic; locked→403/423; throttle:per-policy; no-enum | L | P0 |
| 6 | FR-AUTH.3 | Implement refresh rotation flow | API | COMP-002,COMP-003,DM-002 | valid-refresh→200+new-pair; expired→401; revoked→401+replay-detect; store:token-hash | L | P0 |
| 7 | FR-AUTH.4 | Implement profile retrieval flow | API | COMP-001,COMP-010 | bearer-valid→200+profile; invalid/expired→401; omit:password_hash+refresh_token_hash | M | P0 |
| 8 | FR-AUTH.5 | Implement password reset flow | API | COMP-001,COMP-004,COMP-002,COMP-014 | registered-email→token1h+dispatch; valid-token→password-set; invalid/expired→400; reset→revoke-sessions | L | P0 |
| 9 | API-009 | Define logout revocation contract | API | COMP-002,COMP-001 | endpoint:/auth/logout; action:revoke-session/current-device; success:204; unauth:401; redirect-scope:landing | M | P1 |
| 10 | NFR-001 | Capture GDPR consent at signup | API | FR-AUTH.2,DM-001 | consent:required-at-register; consent_ts:stored; audit:queryable | M | P0 |
| 11 | NFR-002 | Persist SOC2 auth audit events | Ops | COMP-001,COMP-010 | events:login/register/refresh/reset/logout; fields:userId+timestamp+ip+outcome; retention:12mo | L | P0 |
| 12 | COMP-016 | Implement audit log store/query path | Ops | NFR-002,COMP-010 | role:auth-event-log; store:PostgreSQL; query:by-date+user; consumers:Jordan+auditors | M | P1 |
| 13 | NFR-AUTH.1 | Meet auth latency budget | Ops | COMP-001,COMP-002,COMP-004 | auth-p95:<200ms; APM:enabled; k6-baseline:pass | M | P0 |
| 14 | NFR-PERF-002 | Meet concurrent login capacity | Infra | COMP-001,COMP-013 | logins:500-concurrent; saturation:none-critical; k6:pass | M | P1 |
| 15 | COMP-014 | Implement reset email adapter | API | FR-AUTH.5 | role:reset-email-dispatch; provider:SendGrid; template:reset-link; SLA:<60s; dep:external-email | M | P1 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthService facade wiring | dependency injection | AuthService→UserRepo\|PasswordHasher\|TokenManager | 2 | FR-AUTH.1,FR-AUTH.2,FR-AUTH.4,FR-AUTH.5 |
| Refresh rotation registry | registry | TokenManager→token-hash store+replay rules | 2 | FR-AUTH.3,API-004,API-009 |
| Audit event pipeline | event binding | AuthService actions→audit log store | 2 | NFR-002,COMP-016,OPS-003 |
| Logout revocation hook | callback | logout endpoint→TokenManager.revoke | 2 | API-009,COMP-008 |

## Phase 3: Integration

**Phase 3** | Wire middleware, routes, endpoints, and frontend clients | Duration: 2 weeks | Exit: end-to-end auth journeys succeed through UI and HTTP layers

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-005 | Implement auth middleware | Gate | COMP-002,COMP-003 | path:src/middleware/auth-middleware.ts; extract:Bearer; verify:access-jwt; invalid→401; attach:user-claims | M | P0 |
| 2 | COMP-011 | Register auth route group | API | COMP-001,COMP-005 | path:src/routes/index.ts; routes:/auth/*; mount:middleware+handlers; version:/v1/auth/* | M | P0 |
| 3 | API-001 | Expose POST /auth/login | API | FR-AUTH.1,COMP-011 | body:email+password; 200→AuthToken; 401→generic; 423/403→locked; rate-limit:policy | M | P0 |
| 4 | API-002 | Expose POST /auth/register | API | FR-AUTH.2,COMP-011,NFR-001 | body:email+password+displayName+consent; 201→UserProfile; 400→validation; 409→duplicate | M | P0 |
| 5 | API-003 | Expose GET /auth/me | API | FR-AUTH.4,COMP-005,COMP-011 | auth:Bearer; 200→id+email+displayName+createdAt+updatedAt+lastLoginAt+roles; 401→invalid | M | P0 |
| 6 | API-004 | Expose POST /auth/refresh | API | FR-AUTH.3,COMP-011 | body:refreshToken; 200→rotated-pair; 401→expired/revoked; rate-limit:30/min/user | M | P0 |
| 7 | API-005 | Expose POST /auth/reset-request | API | FR-AUTH.5,COMP-011,COMP-014 | body:email; registered→dispatch-token; unregistered→same-confirmation; no-enum | M | P1 |
| 8 | API-006 | Expose POST /auth/reset-confirm | API | FR-AUTH.5,COMP-011 | body:token+newPassword; valid→password-updated; expired/invalid→400; used→rejected | M | P1 |
| 9 | API-007 | Standardize auth error envelope | API | API-001,API-002,API-003,API-004,API-005,API-006 | shape:error.code+message+status; codes:stable; no-sensitive-detail | S | P1 |
| 10 | COMP-008 | Implement AuthProvider | FE | API-003,API-004,API-009 | props:children; role:context-provider; state:AuthToken+UserProfile; silent-refresh:on; auth-methods:exposed; clear-on-tab-close:on | L | P0 |
| 11 | COMP-006 | Implement LoginPage | FE | API-001,COMP-008 | props:onSuccess+redirectUrl?; fields:email+password; submit→/auth/login; store:AuthToken-via-AuthProvider; success→redirect; error:generic | M | P0 |
| 12 | COMP-007 | Implement RegisterPage | FE | API-002,COMP-008,NFR-001 | props:onSuccess+termsUrl; fields:email+password+displayName+consent; inline-validation:on; submit→/auth/register; success→auto-login/login-redirect | M | P0 |
| 13 | COMP-009 | Implement ProfilePage | FE | API-003,COMP-008 | route:/profile; render:UserProfile(displayName+email+createdAt); call:GET/auth/me; auth-guard:on; 401→login-redirect | M | P1 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Bearer verification chain | middleware chain | routes→AuthMiddleware→AuthService | 3 | API-003,protected routes |
| Frontend auth context | registry | AuthProvider→LoginPage\|RegisterPage\|ProfilePage | 3 | COMP-006,COMP-007,COMP-009 |
| Silent refresh callback | callback wiring | AuthProvider 401/expiry→POST /auth/refresh | 3 | COMP-008,API consumers |
| Error envelope contract | dispatch table | endpoint handlers→shared error mapper | 3 | FE forms, API consumers |

## Phase 4: Hardening

**Phase 4** | Validate security, observability, and quality gates | Duration: 1.5 weeks | Exit: unit, integration, E2E, perf, compliance, and rollback tests pass

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | TEST-001 | Test PasswordHasher hashing path | Test | COMP-004,NFR-AUTH.3 | hash+verify:pass; cost:12; mismatch→false | S | P0 |
| 2 | TEST-002 | Test JwtService RS256 path | Test | COMP-003,NFR-SEC-002 | sign→valid-jwt; verify→claims; expired→reject | S | P0 |
| 3 | TEST-003 | Test TokenManager rotation path | Test | COMP-002,FR-AUTH.3 | issue-pair:ok; rotate:revokes-old; replay→all-user-tokens-invalid | M | P0 |
| 4 | TEST-004 | Test AuthService login path | Test | COMP-001,FR-AUTH.1 | valid→tokens; invalid→401; locked→403/423 | M | P0 |
| 5 | TEST-005 | Test AuthService registration path | Test | COMP-001,FR-AUTH.2 | create→hashed-user; duplicate→409; weak→400 | M | P0 |
| 6 | TEST-006 | Test login HTTP flow | Test | API-001,COMP-011 | POST/login→200+JWT; bad-creds→401; envelope:correct | M | P0 |
| 7 | TEST-007 | Test refresh HTTP rotation flow | Test | API-004,COMP-011 | valid→new-pair; old-token→401; replay→revoke-all | M | P0 |
| 8 | TEST-008 | Test register then login flow | Test | API-001,API-002 | register→persist; login→same-creds works; duplicate→409 | M | P0 |
| 9 | TEST-009 | Test complete user lifecycle | Test | API-001,API-002,API-003,API-004,API-005,API-006,COMP-008,COMP-006,COMP-007,COMP-009 | register→login→profile→refresh→reset→relogin; status-codes:expected; old-creds→rejected | L | P0 |
| 10 | OPS-001 | Instrument auth metrics/traces | Ops | COMP-001,COMP-002,COMP-003 | metrics:auth_login_total+duration+refresh+registration; traces:OTel-end-to-end; labels:useful | M | P0 |
| 11 | OPS-002 | Configure auth alert thresholds | Ops | OPS-001,NFR-AUTH.1,NFR-AUTH.2 | login-fail-rate>20%/5m→alert; p95>500ms→alert; Redis-failures→alert | S | P1 |
| 12 | OPS-003 | Publish auth runbook and on-call ops | Ops | NFR-002,OPS-002 | scenarios:service-down+refresh-fail; diagnosis:documented; escalation:path-defined | M | P1 |
| 13 | NFR-AUTH.2 | Validate uptime readiness | Ops | OPS-001,OPS-002 | uptime-target:99.9%; healthcheck:on; PagerDuty:routed | S | P0 |
| 14 | COMP-015 | Implement feature flag controls | Gate | API-001,API-004 | flags:AUTH_NEW_LOGIN+AUTH_TOKEN_REFRESH; default:off; env-toggle:works | M | P0 |
| 15 | NFR-002 | Validate audit retention and queryability | Ops | COMP-016 | retention:12mo; query:user+date-range; SOC2-checklist:pass | M | P0 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Test execution matrix | registry | unit+integration+e2e suites→FR/NFR coverage | 4 | release gate |
| Metrics export path | event binding | AuthService/TokenManager→Prometheus+OTel | 4 | dashboards, alerts |
| Feature flag gate | dispatch table | AUTH_NEW_LOGIN/AUTH_TOKEN_REFRESH→route+provider behavior | 4 | rollout phases |
| Runbook escalation chain | callback wiring | alerts→auth-team→platform-team | 4 | on-call operations |

## Phase 5: Production Readiness

**Phase 5** | Roll out safely, validate business outcomes, and close decisions | Duration: 2 weeks | Exit: phased rollout complete, flags removable, success metrics and rollback confidence achieved

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-001 | Prepare legacy auth parallel run | Ops | COMP-015,COMP-011 | staging:parallel-run; data-path:idempotent; backup:verified | M | P0 |
| 2 | MIG-002 | Execute internal alpha rollout | Ops | TEST-009,COMP-015 | audience:auth-team+QA; flags:AUTH_NEW_LOGIN on-staging; P0/P1-bugs:0 | M | P0 |
| 3 | MIG-003 | Execute 10% beta rollout | Ops | MIG-002,OPS-002 | traffic:10%; p95<200ms; error-rate<0.1%; Redis-failures:0-critical | L | P0 |
| 4 | MIG-004 | Execute GA rollout | Ops | MIG-003,NFR-AUTH.2 | traffic:100%; uptime:99.9%-7d; dashboards:green | L | P0 |
| 5 | MIG-005 | Validate rollback procedure | Ops | MIG-001,COMP-015,OPS-003 | disable:AUTH_NEW_LOGIN; legacy-smoke:pass; restore-playbook:tested | M | P0 |
| 6 | MIG-006 | Remove rollout flags post-stability | Gate | MIG-004 | AUTH_NEW_LOGIN:removed; AUTH_TOKEN_REFRESH:removed; config-cleanup:done | M | P1 |
| 7 | OPS-004 | Verify capacity scaling plan | Infra | MIG-003,OPS-001 | pods:3→10-HPA; pg-pool:100/200-plan; Redis-mem:<70% or scale | M | P1 |
| 8 | OPS-005 | Verify password reset delivery ops | Ops | COMP-014,MIG-002 | email-delivery:<60s; monitoring:on; fallback:support-ready | S | P1 |
| 9 | NFR-001 | Audit registration consent evidence | Ops | API-002,MIG-002 | consent_ts:present; registration-audit:pass; GDPR-evidence:stored | S | P0 |
| 10 | NFR-002 | Validate SOC2 event evidence | Ops | COMP-016,MIG-003 | login/register/refresh/reset/logout events present; fields:userId+timestamp+ip+outcome; retention:12mo | M | P0 |
| 11 | NFR-004 | Re-verify data minimization in prod | Ops | MIG-004,DM-001 | prod-schema:email+hashed-password+displayName only; extra-PII:none | S | P1 |
| 12 | NFR-003 | Re-verify password secrecy in prod | Sec | MIG-004,COMP-004 | plaintext:absent in DB+logs; scan:clean; pen-test:no-critical | M | P0 |
| 13 | API-010 | Publish admin audit query surface | API | COMP-016,NFR-002 | Jordan-query:date+user filters; access:controlled; docs:available | M | P1 |
| 14 | API-011 | Resolve refresh storage decision | Arch | COMP-002,DM-002,MIG-001 | store:Redis or PostgreSQL finalized; rationale:documented; migration-impact:closed | S | P0 |
| 15 | API-012 | Resolve login throttle decision | Arch | COMP-013,FR-AUTH.1 | rate-limit:5/min or 10/min finalized; gateway+tests aligned; risk-signoff:done | S | P0 |
| 16 | API-013 | Resolve schema naming decision | Arch | DM-001,API-002,API-003 | snake/camel mapping frozen; API docs aligned; migration+FE contracts stable | S | P0 |
| 17 | API-014 | Decide max active refresh sessions | Arch | FR-AUTH.3,COMP-002 | device-limit:defined; storage-budget:fit; UX:approved | S | P1 |

### Integration Points — Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Rollout flag controller | dispatch table | flags→alpha/beta/GA routing | 5 | ops team, frontend |
| Rollback command path | callback wiring | alert/runbook→disable flag→legacy auth | 5 | on-call team |
| Audit evidence export | registry | auth-event store→compliance queries | 5 | Jordan, auditors |
| Capacity autoscale loop | middleware/automation | metrics→HPA/DB/Redis scaling actions | 5 | platform-team |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | JWT key compromise enables forged access | High | Low | High | RS256 keys in secrets manager; 90-day rotation; config tests; emergency revoke plan | Security |
| 2 | Refresh replay bypasses session trust | High | Medium | High | Rotate refresh tokens; hash storage; replay detection; revoke all user sessions on reuse | Backend |
| 3 | bcrypt cost drifts below threat model | Medium | Low | Medium | Keep cost configurable; benchmark annually; review against OWASP/NIST guidance | Security |
| 4 | XSS exposes client auth material | High | Medium | High | Access token in memory only; refresh in httpOnly cookie; short access TTL; tab-close cleanup | Frontend |
| 5 | Brute-force traffic overwhelms login | Medium | High | Medium | Finalize throttle policy; lock after 5 failures/15m; WAF escalation; generic auth errors | Platform |
| 6 | Legacy migration corrupts auth data | High | Low | High | Parallel run; idempotent migrations; backups before each phase; tested rollback | Database |
| 7 | Registration UX underperforms business target | High | Medium | High | Inline validation; signup funnel tracking; alpha usability fixes before beta | Product |
| 8 | Missing audit logs breaks SOC2 readiness | High | Medium | High | Log all auth events with required fields; 12-month retention; query validation in hardening | Compliance |
| 9 | Email delivery outage blocks resets | Medium | Low | Medium | Monitor provider latency; fallback support path; clear user messaging; resend tooling | Ops |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ | 1 | Required | No service launch until provisioned |
| Redis 7+ | 2 | Required pending storage decision | Force re-login on expiry if refresh disabled |
| Node.js 20 LTS | 1 | Required | No fallback |
| bcryptjs | 1 | Required | Swap to bcrypt-equivalent only with security review |
| jsonwebtoken | 1 | Required | Alternate JWT lib only with RS256 parity |
| SendGrid API | 2 | Required for reset flow | Queue/reset-support fallback |
| Frontend routing framework | 3 | Required | Delay UI rollout; keep backend-only testing |
| SEC-POLICY-001 | 1 | Required | Block sign-off until policy clarified |

### Infrastructure Requirements

- RSA key material stored in a secrets manager with rotation support.
- PostgreSQL connection pooling sized for 100 base / 200 surge connections.
- Redis sized for roughly 100K refresh tokens with alerting above 70% memory.
- API Gateway or equivalent edge layer enforcing CORS, rate limits, and TLS 1.3.
- APM, Prometheus, and OpenTelemetry pipeline enabled before beta.
- Feature-flag platform supporting per-environment and percentage rollouts.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| Login latency | AuthService login p95 | <200ms | APM + k6 load test | 2-5 |
| Registration reliability | Registration success rate | >99% | Funnel + API success ratio | 3-5 |
| Refresh latency | Token refresh p95 | <100ms | APM on refresh endpoint | 3-5 |
| Availability | Service uptime | 99.9% rolling 30d | Health checks + PagerDuty records | 4-5 |
| Hash cost | Password hash time | <500ms | Benchmark test for PasswordHasher | 1-4 |
| Signup conversion | Registration conversion | >60% | Product funnel analytics | 5 |
| Adoption | Daily authenticated users | >1000 in 30d | Token issuance / active-user analytics | 5 |
| Session stickiness | Average session duration | >30m | Refresh analytics | 5 |
| Login quality | Failed login rate | <5% | Auth event log analysis | 4-5 |
| Password reset usability | Reset completion rate | >80% | Reset funnel analytics | 5 |
| Code quality | Auth module test coverage | >80% | Unit/integration coverage report | 4 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| 1 Foundation | 1.5 weeks | Week 1 | Mid-Week 2 | contracts frozen; schemas approved; JwtService/PasswordHasher ready |
| 2 Core Logic | 2 weeks | Mid-Week 2 | End Week 4 | AuthService+TokenManager complete; audit core implemented |
| 3 Integration | 2 weeks | Week 5 | End Week 6 | routes live; UI flows wired; E2E happy path working |
| 4 Hardening | 1.5 weeks | Week 7 | Mid-Week 8 | perf/compliance tests pass; alerts/runbooks/flags ready |
| 5 Production Readiness | 2 weeks | Mid-Week 8 | End Week 10 | alpha→beta→GA complete; rollback and evidence sign-off |

**Total estimated duration:** ~10 weeks end-to-end, excluding unresolved scope expansion for RBAC/MFA/OAuth.

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | Reset emails synchronous or queued? | Changes reset latency and resilience design | 2 | Engineering |
| 2 | Max active refresh tokens per user? | Changes storage sizing and multi-device semantics | 5 | Product |
| 3 | Support API keys for service auth in v1.x? | Could expand AuthMiddleware/AuthService surface | 5 | test-lead |
| 4 | Max `roles` array length? | Affects schema validation and token payload sizing | 1 | auth-team |
| 5 | Final lockout rule after repeated failures? | Changes security UX and admin handling | 1 | Security |
| 6 | Add remember-me session extension? | Changes refresh TTL and product UX | 5 | Product |
| 7 | Login rate limit 5/min or 10/min? | Directly changes gateway config and brute-force posture | 1 | Engineering |
| 8 | Canonical schema/API naming model? | Required before migration and FE integration | 1 | Engineering |
| 9 | Should logout be mandatory in v1.0 scope? | Affects user journey completeness and revocation API | 2 | Product/Engineering |
| 10 | Is admin audit-query surface in v1.0 scope? | Needed for Jordan persona and SOC2 workflows | 2 | Product/Compliance |
| 11 | Refresh tokens in Redis or PostgreSQL? | Changes revocation architecture and rollback design | 1 | Engineering |