---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: 1.0
debate_rounds: 0
generated: "2026-04-15"
generator: "single"
total_phases: 5
total_task_rows: 64
risk_count: 10
open_questions: 10
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap translates the authentication spec, TDD, and PRD into a five-phase delivery plan that builds the security foundation first, then core auth logic, then API/frontend integration, then compliance/performance hardening, and finally controlled rollout. Priority is driven by the PRD's highest-value outcomes: unblock personalization for Alex, provide stable token refresh for Sam, and establish auditability for Jordan before SOC2 review.

**Business Impact:** Unblocks Q2 personalization revenue, closes current auth security gaps, and creates the auditable identity layer needed for Q3 SOC2 readiness.

**Complexity:** MEDIUM (0.6) — bounded endpoint count keeps scope manageable, but RS256 signing, refresh rotation, multi-store persistence, and compliance logging create a non-trivial security and rollout path.

**Critical path:** PasswordHasher/JwtService + data stores → TokenManager/UserRepo/migrations → AuthService flows → routes/middleware/API contracts → AuthProvider/pages → audit/load/E2E gates → feature-flagged alpha/beta/GA rollout.

**Key architectural decisions:**

- Keep the layered core explicit: `AuthService` orchestrates, `TokenManager` manages session lifecycle, `JwtService` signs/verifies tokens, and `PasswordHasher` owns adaptive hashing.
- Preserve stateless access tokens with RS256 and store only rotated refresh-token hashes, avoiding server-side access-token sessions while retaining revocation and replay detection.
- Deliver frontend session behavior through `AuthProvider` with access tokens in memory and refresh controls behind flags, matching the security model and Sam's programmatic-refresh needs.

**Open risks requiring resolution before Phase 1:**

- Confirm exact lockout semantics: spec says `403` for locked accounts while TDD adds `423 Locked`; pick one contract and apply consistently.
- Resolve whether password reset email dispatch is synchronous or queued; it changes reset endpoint latency and resiliency design.
- Set the maximum active refresh-token count per user/device set before repository and revocation policies are finalized.
- Confirm whether logout is in v1.0 scope; PRD includes it, but the spec/TDD roadmap inputs do not define a corresponding FR.
- Resolve refresh-token architecture drift: spec points to httpOnly-cookie + DB-backed `refresh_tokens`, while the TDD points to request-body exchange + Redis-backed storage.

## Phase 1: Foundation

**Phase 1** | milestone: Core crypto, data contracts, gateway guardrails | duration: 1.5 weeks | exit criteria: schemas, key handling, gateway controls, and foundational NFR guards are verified

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-004 | Build PasswordHasher | Sec | — | path:src/auth/password-hasher.ts; role:bcrypt-hash+compare; cost:12-config; dep:bcryptjs | M | P0 |
| 2 | COMP-003 | Build JwtService | Sec | — | path:src/auth/jwt-service.ts; role:sign+verify-JWT; alg:RS256; key:RSA-2048; dep:jsonwebtoken | M | P0 |
| 3 | COMP-013 | Build UserRepo module | DB | DM-001 | path:src/auth/user-repo.ts; role:user-fetch+create+update; ops:byEmail+byId+create+touchLogin+lock+setPassword; store:PostgreSQL | L | P0 |
| 4 | COMP-007 | Create auth DB migration | DB | — | path:src/database/migrations/003-auth-tables.ts; adds:users+refresh_tokens; down:drop-users+refresh_tokens; store:PostgreSQL | L | P0 |
| 5 | DM-001 | Model UserRecord schema | DB | COMP-007 | id:uuid-v4; email:unique+idx; display_name:string; password_hash:bcrypt; is_locked:bool; created_at:date; updated_at:date | M | P0 |
| 6 | DM-002 | Model RefreshTokenRecord | DB | COMP-007,DM-001 | id:uuid-v4; user_id:fk->UserRecord.id; token_hash:sha256; expires_at:date; revoked:bool; created_at:date | M | P0 |
| 7 | DM-003 | Model AuthTokenPair DTO | API | — | access_token:jwt-15m; refresh_token:opaque-7d | S | P1 |
| 8 | DM-006 | Model ErrorResponse DTO | API | — | error.code:string; error.message:string; error.status:number | S | P1 |
| 9 | COMP-012 | Configure API Gateway guardrails | Gate | — | path:infrastructure; role:rate-limit+CORS; place:pre-AuthService; dep:COMP-001; tls:1.3 | M | P0 |
| 10 | NFR-SEC-002 | Provision RS256 key handling | Sec | COMP-003 | alg:RS256; key:RSA-2048; verify:config-test; rotation:90d | M | P0 |
| 11 | NFR-AUTH.3 | Benchmark bcrypt cost 12 | Sec | COMP-004 | cost:12; hashTime:<500ms; unit:cost-assert; benchmark:timing-pass | S | P0 |
| 12 | NFR-COMP-004 | Enforce data minimization | Sec | DM-001 | collect:email+password_hash+display_name; pii:no-extra; logs:no-raw-password; review:schema+flow | M | P1 |
| 13 | NFR-COMP-001 | Record registration consent | API | DM-001 | consent:required; timestamp:stored; register:no-consent->400; audit:traceable | M | P1 |
| 14 | COMP-017 | Freeze refresh-token contract | Gate | DM-002,DM-003 | transport:browser-cookie-vs-api-body resolved; store:refresh_tokens+Redis policy fixed; replay:model fixed; docs:spec+TDD aligned | M | P0 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PasswordHasher injection | dependency injection | AuthService→PasswordHasher | 1 | COMP-001 |
| JwtService injection | dependency injection | TokenManager→JwtService | 1 | COMP-002 |
| UserRepo binding | repository binding | AuthService→PostgreSQL user ops | 1 | COMP-001, FR-AUTH.1, FR-AUTH.2, FR-AUTH.4 |
| API Gateway prefilters | middleware chain | CORS+rate-limit→/auth/* | 1 | COMP-001, API-001, API-003, API-006 |

## Phase 2: Core Logic

**Phase 2** | milestone: Auth orchestration and token lifecycle | duration: 2 weeks | exit criteria: login, registration, refresh, and reset core flows pass unit and service integration gates

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-014 | Build RefreshTokenRepo | DB | DM-002 | path:src/auth/refresh-token-repo.ts; ops:store+lookup+revoke+revokeAll+replayDetect; store:Redis; hash:sha256 | M | P0 |
| 2 | COMP-002 | Build TokenManager | Auth | COMP-003,COMP-014,DM-003 | path:src/auth/token-manager.ts; ops:issue+refresh+revoke+revokeAll; deps:JwtService+RefreshTokenRepo; ttl:15m+7d | L | P0 |
| 3 | COMP-001 | Build AuthService | Auth | COMP-002,COMP-004,COMP-013,DM-006 | path:src/auth/auth-service.ts; ops:login+register+refresh+me+resetRequest+resetConfirm; deps:TokenManager+PasswordHasher+UserRepo+Email | L | P0 |
| 4 | FR-AUTH.1 | Implement login flow | Auth | COMP-001,COMP-002,COMP-004,COMP-013,COMP-012 | valid→200+access15m+refresh7d; invalid→401+no-enum; locked→403/423-finalized; ip-limit:5/min; 5fail/15m→lock | L | P0 |
| 5 | FR-AUTH.2 | Implement registration flow | Auth | COMP-001,COMP-004,COMP-013,NFR-COMP-001 | valid(email,password,displayName)→201+profile+session; dup-email→409; pw:min8+upper+lower+digit; email:format-valid | L | P0 |
| 6 | FR-AUTH.3 | Implement refresh flow | Auth | COMP-001,COMP-002,COMP-014 | valid-refresh→200+new-access+rotated-refresh; expired/revoked→401; replay→revoke-all; hash-store:enabled | L | P0 |
| 7 | FR-AUTH.5 | Implement reset flow | Auth | COMP-001,COMP-002,COMP-004,COMP-014 | req-known/unknown→same-response; known→issue-reset-1h+dispatch-email; valid-token→set-new-pw+invalidate-token+revoke-sessions; expired/invalid→400; used→blocked | L | P0 |
| 8 | API-001 | Specify POST /auth/login | API | FR-AUTH.1,DM-005,DM-006 | req:email+password; 200:accessToken+refreshToken+expiresIn+tokenType; 401:no-enum; 429:rate-limit; locked:error-code | M | P0 |
| 9 | API-002 | Specify POST /auth/register | API | FR-AUTH.2,DM-004,DM-006 | req:email+password+displayName+consent; 201:id+email+displayName+createdAt+updatedAt+lastLoginAt+roles; 400:validation; 409:duplicate | M | P0 |
| 10 | API-004 | Specify POST /auth/refresh | API | FR-AUTH.3,DM-005,DM-006 | req:refreshToken; 200:new-accessToken+refreshToken+expiresIn+tokenType; 401:expired/revoked; replay→revoke-all | M | P0 |
| 11 | API-005 | Specify POST /auth/reset-request | API | FR-AUTH.5,DM-006 | req:email; resp:generic-success; known→email-dispatch; unknown→no-enum; rate-limit:defined | M | P1 |
| 12 | API-006 | Specify POST /auth/reset-confirm | API | FR-AUTH.5,DM-006 | req:token+newPassword; 200/204:password-updated; invalid/expired→400; used→400; sessions→revoked | M | P1 |
| 13 | NFR-COMP-003 | Block raw password leakage | Sec | COMP-001,COMP-004 | persist:hash-only; logs:no-raw-password; reset:no-raw-token-log; audit:security-review-pass | M | P0 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| TokenManager internals | dependency injection | TokenManager→JwtService+RefreshTokenRepo | 2 | FR-AUTH.1, FR-AUTH.3, FR-AUTH.5 |
| AuthService facade | dependency injection | AuthService→TokenManager+PasswordHasher+UserRepo | 2 | COMP-006, COMP-010 |
| Reset email dispatch | callback/service call | AuthService→SendGrid/reset transport | 2 | FR-AUTH.5 |
| Auth API handlers | route binding | POST login/register/refresh/reset*→AuthService methods | 2 | COMP-006, FE pages |

## Phase 3: Integration

**Phase 3** | milestone: HTTP surface, middleware, frontend session UX | duration: 2 weeks | exit criteria: all endpoints are wired, profile retrieval works end-to-end, and frontend auth journeys pass golden-path checks

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-005 | Wire auth middleware | API | COMP-002,DM-006 | path:src/middleware/auth-middleware.ts; bearer:extract; token:verify; invalid→401; attach:claims | M | P0 |
| 2 | COMP-006 | Register auth routes | API | COMP-001,COMP-005 | path:src/routes/index.ts; group:/auth/*; map:login+register+me+refresh+reset*; middleware:protected-on-me | M | P0 |
| 3 | API-003 | Specify GET /auth/me | API | FR-AUTH.4,DM-004,DM-006,COMP-005 | bearer:req; 200:id+email+displayName+createdAt+updatedAt+lastLoginAt+roles; 401:invalid/expired; sensitive:no-password_hash+no-refresh_token_hash | M | P0 |
| 4 | FR-AUTH.4 | Implement profile retrieval | API | COMP-001,COMP-005,COMP-013,DM-004 | valid-bearer→200+profile; invalid/expired→401; hide:password_hash+refresh_token_hash; fields:id+email+displayName+createdAt+updatedAt+lastLoginAt+roles | M | P0 |
| 5 | COMP-010 | Build AuthProvider | FE | API-001,API-003,API-004,DM-004,DM-005 | role:context-wrapper; state:AuthToken+UserProfile; refresh:silent; store:access-in-memory; expose:login+register+logout+me | L | P0 |
| 6 | COMP-008 | Build LoginPage | FE | API-001,COMP-010 | route:/login; fields:email+password; fail:generic-error; success:onSuccess+redirect; rate/lock:handled | M | P1 |
| 7 | COMP-009 | Build RegisterPage | FE | API-002,COMP-010,NFR-COMP-001 | route:/register; fields:email+password+displayName+consent; inline:pw-policy; dup-email:error; success:session-start | M | P1 |
| 8 | COMP-011 | Build ProfilePage | FE | API-003,COMP-010 | route:/profile; auth:required; render:displayName+email+createdAt; 401→redirect-login; data:matches-API | M | P1 |
| 9 | DM-004 | Model UserProfile DTO | API | API-003,FR-AUTH.4 | id:uuid; email:string; displayName:string; createdAt:iso8601; updatedAt:iso8601; lastLoginAt:iso8601-null; roles:string[] | S | P1 |
| 10 | DM-005 | Model AuthToken DTO | API | API-001,API-004 | accessToken:jwt; refreshToken:opaque; expiresIn:900; tokenType:Bearer | S | P1 |
| 11 | FR-AUTH.3.1 | Persist sessions across reloads | FE | COMP-010,API-004 | refresh-window:7d; reload→silent-refresh-or-active-session; expired→prompt-login; api-consumer:error-clear | M | P1 |
| 12 | FR-AUTH.2.1 | Auto-login after register | FE | FR-AUTH.2,COMP-010 | register-success→session-start; dashboard/profile:redirect; no-second-login; dup/invalid→stay-form | M | P1 |
| 13 | FR-AUTH.5.1 | Prevent reset email enumeration | API | API-005,FR-AUTH.5 | known-email→generic-success; unknown-email→same-success; side-effect:email-only-for-known; logs:no-enum | S | P0 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Bearer auth middleware | middleware chain | /auth/me→auth-middleware→AuthService.me | 3 | API-003, COMP-011 |
| Route registry | dispatch table | routes/index→AuthService handlers | 3 | API consumers, FE |
| AuthProvider refresh hook | callback wiring | 401/expiry→refresh endpoint→state update | 3 | COMP-008, COMP-009, COMP-011 |
| Protected route wrapper | event binding | ProfilePage render gated by AuthProvider state | 3 | Alex persona |

## Phase 4: Hardening

**Phase 4** | milestone: Compliance, observability, performance, and validation depth | duration: 1.5 weeks | exit criteria: security/compliance controls, monitoring, and test evidence satisfy pre-production review

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-AUTH.1 | Meet auth latency target | Perf | FR-AUTH.1,FR-AUTH.2,FR-AUTH.3,FR-AUTH.4,FR-AUTH.5 | p95:<200ms; method:k6+APM; scope:all-auth-endpoints; gate:pass | L | P0 |
| 2 | NFR-PERF-002 | Validate 500 concurrent logins | Perf | FR-AUTH.1,NFR-AUTH.1 | conc:500; load:k6; success:error-rate-acceptable; p95:tracked | M | P0 |
| 3 | NFR-AUTH.2 | Establish uptime guardrails | Ops | COMP-001,COMP-012 | uptime:99.9%; healthcheck:present; pagerduty:alerts; window:30d | M | P0 |
| 4 | NFR-COMP-002 | Implement audit logging | Ops | FR-AUTH.1,FR-AUTH.2,FR-AUTH.3,FR-AUTH.5,DM-001 | log:userId+timestamp+ip+outcome+eventType; retain:12mo; query:date+user; soc2:audit-pass | L | P0 |
| 5 | NFR-OPS-001 | Prepare operational readiness | Ops | NFR-AUTH.2,NFR-COMP-002 | p1-ack:<15m; oncall:24/7-2w-postGA; dashboards:auth_login_total+auth_login_duration_seconds+auth_token_refresh_total+auth_registration_total | M | P0 |
| 6 | TEST-001 | Add PasswordHasher unit tests | Test | COMP-004,NFR-AUTH.3 | hash+verify:pass; cost12:assert; invalid:reject | S | P1 |
| 7 | TEST-002 | Add JwtService unit tests | Test | COMP-003,NFR-SEC-002 | sign+verify:pass; expired→reject; alg:RS256-only | S | P1 |
| 8 | TEST-003 | Add TokenManager unit tests | Test | COMP-002,FR-AUTH.3 | issue-pair:pass; rotate:old-revoked; replay→revoke-all; expired→401 | M | P1 |
| 9 | TEST-004 | Add AuthService login tests | Test | COMP-001,FR-AUTH.1 | valid→tokens; invalid→401; no-enum; lock-path:covered | M | P1 |
| 10 | TEST-005 | Add AuthService register tests | Test | COMP-001,FR-AUTH.2 | valid→user+hash; dup→409; weak→400; consent:required | M | P1 |
| 11 | TEST-006 | Add login integration test | Test | API-001,COMP-006 | http-login→valid-jwt; creds:path-E2E; format:contract-match | M | P1 |
| 12 | TEST-007 | Add refresh integration test | Test | API-004,COMP-006 | refresh→new-pair; old-refresh→revoked; replay:path-covered | M | P1 |
| 13 | TEST-008 | Add register-login integration | Test | API-002,API-001,COMP-006 | register→persist; same-creds→login-ok; dup→409 | M | P1 |
| 14 | TEST-009 | Add full auth E2E flow | Test | COMP-008,COMP-009,COMP-010,COMP-011,FR-AUTH.5 | register→login→me→refresh→reset→login-new-pw; old-creds→reject; UI:redirects-correct | L | P1 |
| 15 | TEST-010 | Add coverage gate | Test | TEST-001,TEST-002,TEST-003,TEST-004,TEST-005 | coverage:>80%-AuthService+TokenManager+JwtService+PasswordHasher; report:CI-pass | S | P1 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Structured auth logs | event pipeline | AuthService events→log sink/query store | 4 | Jordan persona, auditors |
| Metrics registry | monitoring wiring | auth components→Prometheus/OpenTelemetry | 4 | Ops, on-call |
| Test pyramid suite | CI pipeline | unit+integration+E2E gates before rollout | 4 | Release gate |
| Alert rules | threshold registry | latency/failure/Redis alerts→PagerDuty | 4 | auth-team, platform-team |

## Phase 5: Production Readiness

**Phase 5** | milestone: Controlled rollout, rollback readiness, and GA sign-off | duration: 2 weeks | exit criteria: alpha/beta/GA completed with success metrics, rollback proof, and owner approvals

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-015 | Wire AUTH_NEW_LOGIN flag | Gate | COMP-006,COMP-008,COMP-009 | flag:AUTH_NEW_LOGIN; default:off; gates:LoginPage+RegisterPage+login-route; remove:post-GA | M | P0 |
| 2 | COMP-016 | Wire AUTH_TOKEN_REFRESH flag | Gate | COMP-002,COMP-010 | flag:AUTH_TOKEN_REFRESH; default:off; when-off:access-only; remove:GA+2w | M | P0 |
| 3 | MIG-001 | Execute internal alpha rollout | Ops | TEST-009,COMP-015,COMP-016 | env:staging; users:auth-team+QA; all-FR:manual-pass; bugs:P0/P1=0 | M | P0 |
| 4 | MIG-002 | Execute 10% beta rollout | Ops | MIG-001,NFR-AUTH.1,NFR-AUTH.2 | traffic:10%; p95:<200ms; err:<0.1%; redis-failures:0-critical | L | P0 |
| 5 | MIG-003 | Execute GA rollout | Ops | MIG-002,NFR-OPS-001 | traffic:100%; uptime:99.9%-7d; dashboards:green; legacy:deprecated | L | P0 |
| 6 | MIG-004 | Validate rollback procedure | Ops | COMP-015,MIG-001 | disable:AUTH_NEW_LOGIN; legacy-smoke:pass; restore:data-if-needed; postmortem:<48h-ready | M | P0 |
| 7 | OPS-001 | Publish auth runbook | Ops | NFR-OPS-001,MIG-001 | scenarios:AuthService-down+refresh-failures; diagnosis:defined; resolution:steps; escalation:path-set | M | P1 |
| 8 | OPS-002 | Configure dashboards and alerts | Ops | NFR-OPS-001,NFR-COMP-002 | dashboards:4-core-metrics; alerts:latency+login-fail+redis; owners:auth+platform | M | P1 |
| 9 | OPS-003 | Validate capacity plan | Ops | NFR-PERF-002,MIG-002 | pods:3→10-HPA; pg-pool:100/200-plan; redis:1GB→2GB-threshold | M | P1 |

### Integration Points — Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AUTH_NEW_LOGIN | feature flag | route/page exposure toggle | 5 | Alex persona, QA |
| AUTH_TOKEN_REFRESH | feature flag | TokenManager/AuthProvider refresh behavior toggle | 5 | Sam persona, FE |
| Rollback switch | operational control | flag disable→legacy auth path | 5 | Incident response |
| Go/no-go approvals | release gate | test-lead+eng-manager+security sign-off | 5 | Production deploy |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | RSA private key compromise | Critical | Low | Forged access tokens across services | Store keys in secrets manager; rotate every 90d; validate RS256-only config | Security |
| 2 | Refresh token replay after theft | High | Medium | Full session hijack and persistence abuse | Hash refresh tokens; rotate on use; replay→revoke-all-user-tokens | Auth team |
| 3 | Brute-force login abuse | High | Medium | Account compromise and noisy ops load | Gateway IP limits; failed-attempt lock policy; generic 401 messaging | Security |
| 4 | Contract mismatch on locked account status | Medium | Medium | Client bugs and broken monitoring classifications | Resolve 403 vs 423 pre-build; freeze API error catalog | Architect |
| 5 | Redis outage blocks refresh | High | Medium | Session drops and forced re-login | Fail closed on refresh; alert fast; scale/repair Redis; preserve login path | Platform |
| 6 | Incomplete SOC2 audit logging | High | Medium | Compliance gap before Q3 review | Define log schema early; QA audit-log completeness; 12-month retention | Backend |
| 7 | Registration friction hurts adoption | Medium | Medium | Missed >60% conversion target | Inline validation; auto-login after registration; beta funnel review | Product |
| 8 | Reset-email delivery failures | Medium | Low | Password recovery blocked; support burden rises | Monitor SendGrid; alert on failures; fallback support channel | Ops |
| 9 | Data loss during rollout/rollback | High | Low | User/account inconsistency and trust impact | Backup before phases; idempotent migrations; rollback rehearsal | Platform |
| 10 | Scope drift into OAuth/MFA/RBAC | Medium | Medium | Delayed v1.0 and diluted critical-path focus | Enforce v1.0 scope guardrails; park extras for later releases | Architect |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ | 1-5 | Required | Block release until provisioned; no durable auth without it |
| Redis 7+ | 2-5 | Required | Fail refresh closed; users re-login until restored |
| Node.js 20 LTS | 1-5 | Required | Standardize runtime before build starts |
| bcryptjs | 1-4 | Required | No fallback in v1.0; keep PasswordHasher abstraction for future swap |
| jsonwebtoken | 1-4 | Required | No fallback; JwtService depends on RS256 support |
| RSA 2048-bit key pair | 1-5 | Required | Do not launch token issuance until secrets are mounted |
| SendGrid/email service | 2-5 | Required for reset | Defer reset rollout if unavailable; keep other auth flows live |
| Frontend routing framework | 3-5 | Required | Backend can ship first; FE auth pages wait on router readiness |
| Prometheus/OpenTelemetry | 4-5 | Required | No GA without minimal observability coverage |
| PagerDuty/on-call tooling | 4-5 | Required | Use manual escalation only for alpha; not acceptable for GA |
| Kubernetes/HPA | 5 | Required | Run staged beta on fixed capacity only if load envelope is proven |
| SEC-POLICY-001 | 1-5 | Required | Freeze password/token decisions until policy is confirmed |

### Infrastructure Requirements

- Provision PostgreSQL for user records, consent records, and audit logs.
- Provision Redis for refresh-token storage, revocation, and replay detection.
- Mount RSA key material via secrets manager with rotation support.
- Expose metrics/traces and dashboards before beta traffic.
- Enable feature-flag control for login exposure and token refresh behavior.
- Support staged traffic rollout and rollback routing at gateway/platform layer.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| Fast login UX | Login response p95 | <200ms | k6 + APM on login path | 4-5 |
| Stable registration | Registration success rate | >99% | API analytics + integration tests | 4-5 |
| Silent session continuity | Refresh latency p95 | <100ms | APM on TokenManager.refresh | 4-5 |
| Reliable service | Availability | 99.9% | Health checks + alert reports | 4-5 |
| Secure hashing | Password hash time | <500ms | benchmark + unit assertion | 1,4 |
| Business adoption | Registration conversion | >60% | signup funnel review in beta/GA | 5 |
| User engagement | Avg session duration | >30 min | token refresh analytics | 5 |
| UX/security balance | Failed login rate | <5% attempts | auth event log analysis | 4-5 |
| Self-service recovery | Reset completion | >80% | reset funnel analytics | 5 |
| Technical quality | Coverage | >80% key auth modules | CI coverage gate | 4 |
| Persona support | API consumer refresh clarity | clear 401/re-auth behavior | contract tests + beta feedback | 3-5 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| 1 Foundation | 1.5 weeks | Week 1 | Mid-Week 2 | crypto services, schemas, gateway guardrails |
| 2 Core Logic | 2 weeks | Mid-Week 2 | End-Week 4 | TokenManager, AuthService, login/register/refresh/reset core |
| 3 Integration | 2 weeks | Week 5 | End-Week 6 | routes, middleware, AuthProvider, auth pages, profile flow |
| 4 Hardening | 1.5 weeks | Week 7 | Mid-Week 8 | audit logs, load validation, E2E, release gates |
| 5 Production Readiness | 2 weeks | Mid-Week 8 | End-Week 10 | alpha, 10% beta, GA, rollback proof |

**Total estimated duration:** ~10 weeks including rollout validation windows.

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | Should reset emails be synchronous or queued? | Changes reset latency and failure isolation design | 2 | Engineering |
| 2 | Max active refresh tokens per user/device? | Affects Redis storage, revocation scope, multi-device UX | 2 | Product |
| 3 | Is API-key auth needed for service-to-service use? | Could expand v1.0 scope beyond current token model | 2 | Product/Engineering |
| 4 | Max allowed roles length in UserProfile? | DTO and storage contract may change before future RBAC | 1 | Auth team |
| 5 | Final lockout response: 403 or 423? | Client/error-contract mismatch if unresolved | 2 | Security/Architect |
| 6 | Should remember-me extend beyond 7 days? | Impacts token TTLs and Sam/Alex session design | 3 | Product |
| 7 | What audit-log query surface is required for Jordan? | Determines storage/indexing depth and admin tooling scope | 4 | Backend/Admin |
| 8 | Should token revocation cascade on user deletion? | Security and data-lifecycle behavior remain underspecified | 4 | Architect |
| 9 | Is logout explicitly in scope for v1.0? | PRD expects it, but source FR set omits it | 3 | Product |
| 10 | Do we need optional email verification before full activation? | Affects registration completion semantics and compliance interpretation | 5 | Product/Security |
