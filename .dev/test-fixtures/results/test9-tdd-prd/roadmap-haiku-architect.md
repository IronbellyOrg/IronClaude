---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: 0.65
debate_rounds: 0
generated: "2026-04-15"
generator: "single"
total_phases: 4
total_task_rows: 83
risk_count: 7
open_questions: 8
---
# User Authentication Service — Project Roadmap
## Executive Summary
The authentication service is a P0 platform foundation: it unblocks the Q2–Q3 2026 personalization roadmap, closes a SOC2 audit gap before Q3 2026, and supports roughly $2.4M in projected annual revenue tied to identity-dependent features. The architecture should be delivered in technical layers: establish security and data contracts first, implement backend auth flows second, wire user-facing and admin-facing surfaces third, and only then expand traffic under explicit rollout gates.

**Business Impact:** Enables user identity for personalization, compliance auditability, self-service recovery, and stable API authentication without expanding v1.0 scope into OAuth, MFA, or RBAC.

**Complexity:** MEDIUM (0.65) — single-service scope with clear boundaries, but materially elevated by RS256 key management, brute-force defenses, Redis-backed refresh revocation, GDPR/SOC2/NIST constraints, and cross-layer FE/BE integration.

**Critical path:** RS256+bcrypt baseline → canonical auth data contracts → AuthService/TokenManager/UserRepo → login/register/refresh flows → AuthProvider and route guards → observability, rollout gates, and rollback readiness.

**Key architectural decisions:**
- Use stateless REST with 15-minute access JWTs and 7-day hashed refresh tokens in Redis; no server-side session store.
- Make compliance first-class in v1.0: consent capture at registration, 12-month audit retention, strict data minimization, and zero raw-password persistence/logging.
- Use contract-first rollout with API Gateway rate limits, feature flags, staged activation, and hard rollback triggers.

**Open risks requiring resolution before Phase 1:**
- OQ-008 must be resolved in favor of 12-month audit retention before schema, storage, and cost baselines are locked.
- OQ-001 and OQ-004 affect TokenManager shape, refresh-token cardinality, and future service-auth boundaries.
- Logout and admin audit viewing are PRD-scope gaps; their components must be designed before FE route structure hardens.

## Phased Implementation Plan with Milestones
**Phase 1** | Security, contracts, and persistence baseline | 2 weeks | Exit: dependencies provisioned, schemas frozen, key security/compliance constraints ratified

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DEP-001 | Provision PostgreSQL 15+ primary | Infra | — | version:15+; pool:100-ready; backup:pre-phase; user+audit-store:reachable | L | P0 |
| 2 | DEP-002 | Provision Redis 7+ refresh store | Infra | — | version:7+; ttl:7d-ready; hash-store:on; failover:documented | M | P0 |
| 3 | DEP-003 | Pin Node.js 20 LTS runtime | Infra | — | runtime:20LTS; build:green; start:ok; drift:blocked | S | P0 |
| 4 | DEP-004 | Lock bcryptjs dependency | Sec | DEP-003 | lib:bcryptjs; hash+verify:ok; cost12:supported; vuln:0-critical | S | P0 |
| 5 | DEP-005 | Lock jsonwebtoken dependency | Sec | DEP-003 | lib:jsonwebtoken; RS256:ok; verify:ok; vuln:0-critical | S | P0 |
| 6 | DEP-006 | Baseline SendGrid integration | Ops | — | api-key:provisioned; sandbox:ok; template-path:defined; fallback:support | M | P1 |
| 7 | DEP-007 | Confirm frontend routing base | FE | — | routes:/login+/register+/profile; guards:supported; redirects:ok | S | P0 |
| 8 | OQ-008 | Resolve 12-month log retention | Gate | DEP-001 | retention:12mo; TDD-conflict:closed; storage-cost:accepted; schema:unblocked | S | P0 |
| 9 | OQ-001 | Decide service auth boundary | Gate | — | api-key-scope:decided; v1-impact:documented; defer/accept:recorded | S | P1 |
| 10 | OQ-004 | Set refresh token device limit | Gate | DEP-002 | per-user-limit:decided; eviction-policy:defined; UX-impact:documented | S | P0 |
| 11 | NFR-SEC-001 | Enforce bcrypt cost 12 | Sec | DEP-004 | algo:bcrypt; cost:12; unit-test:pass; raw-pass:never | M | P0 |
| 12 | NFR-SEC-002 | Enforce RS256 2048-bit keys | Sec | DEP-005 | alg:RS256; key:2048b; verify:pass; clock-skew:5s | M | P0 |
| 13 | NFR-COMP-001 | Capture GDPR consent record | Sec | DM-001 | consent:req-on-register; ts:stored; no-consent→400; proof:queryable | M | P0 |
| 14 | NFR-COMP-003 | Ban raw password persistence | Sec | NFR-SEC-001 | adaptive-hash:on; raw-store:none; raw-log:none; review:pass | M | P0 |
| 15 | NFR-COMP-004 | Minimize collected PII | Sec | DM-001 | allow:email+hash+displayName; extra-PII:none; forms:trimmed | M | P0 |
| 16 | DM-001 | Model UserProfile schema | DB | DEP-001,OQ-008 | id:UUIDv4-PK; email:unique+idx+lowercase+notnull; displayName:2-100+notnull; createdAt:iso+defaultnow+notnull; updatedAt:iso+autoupdate+notnull; lastLoginAt:iso+nullable; roles:string[]+default[user]+notnull | L | P0 |
| 17 | DM-002 | Model AuthToken contract | API | DEP-002,NFR-SEC-002 | accessToken:JWT+notnull; refreshToken:unique+notnull; expiresIn:900+notnull; tokenType:Bearer+notnull | M | P0 |
| 18 | DM-003 | Model AuditLog schema | DB | DEP-001,OQ-008 | userId:notnull; eventType:notnull; timestamp:iso+notnull; ipAddress:notnull; outcome:notnull | M | P0 |
| 19 | COMP-003 | Build JwtService module | Sec | NFR-SEC-002,DM-002 | type:backend-module; loc:backend; sign:RS256; verify:on; skew:5s; dep:DEP-005 | L | P0 |
| 20 | COMP-004 | Build PasswordHasher module | Sec | NFR-SEC-001 | type:backend-module; loc:backend; algo:bcrypt; cost:12-default; future-migrate:hooked; dep:DEP-004 | M | P0 |
| 21 | COMP-005 | Build UserRepo data layer | DB | DM-001,DEP-001 | type:data-access; loc:backend; store:UserProfile; pool:pg-pool; dep:DEP-001 | L | P0 |
| 22 | COMP-001 | Skeleton AuthService orchestrator | API | COMP-003,COMP-004,COMP-005 | type:backend-svc; loc:backend; deps:COMP-002+COMP-004+COMP-005; delegate:auth-flows | M | P0 |
| 23 | COMP-002 | Skeleton TokenManager module | API | COMP-003,DEP-002,OQ-004 | type:backend-module; loc:backend; issue:JWT+refresh; store:Redis-hash; revoke:on; deps:COMP-003+DEP-002 | M | P0 |
| 24 | COMP-010 | Design logout coordination | API | COMP-001,COMP-002 | type:session-component; loc:cross-layer; action:end-session; revoke:refresh; redirect:landing | S | P1 |
| 25 | COMP-011 | Design audit log viewer | Ops | DM-003,NFR-COMP-002 | type:admin-component; loc:ops/admin; query:user+date; fields:userId+eventType+timestamp+ipAddress+outcome | M | P1 |
| 26 | OQ-002 | Bound roles array length | Gate | DM-001 | roles-max:decided; token-size:reviewed; validation:defined | S | P1 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| API Gateway → AuthService | DI/edge routing | Route map, rate-limit stubs, TLS1.3, CORS allowlist | 1 | API-001, API-002, API-003, API-004, API-005, API-006 |
| AuthService → PasswordHasher | Service delegation | verify/hash call contract | 1 | FR-AUTH-001, FR-AUTH-002, FR-AUTH-005 |
| AuthService → UserRepo | Repository binding | CRUD/query adapter with pg-pool | 1 | FR-AUTH-001, FR-AUTH-002, FR-AUTH-004 |
| TokenManager → JwtService | Service delegation | sign/verify interface and clock-skew policy | 1 | FR-AUTH-003, API-004 |
| TokenManager → Redis | Cache/store binding | hashed refresh token keying + TTL | 1 | DM-002, FR-AUTH-003 |
| Auth events → AuditLog | Event persistence | structured event schema to PostgreSQL | 1 | NFR-COMP-002, DM-003 |

**Phase 2** | Core auth flows and public API | 3 weeks | Exit: login, registration, profile, refresh, and reset contracts pass unit+integration gates

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | FR-AUTH-001 | Implement email/password login | API | COMP-001,COMP-004,COMP-005,API-001 | valid→200+AuthToken; invalid→401+generic; unknown-email→401+no-enum; 5fail/15m→423 | L | P0 |
| 2 | FR-AUTH-002 | Implement validated registration | API | COMP-001,COMP-004,COMP-005,API-002,NFR-COMP-001,NFR-COMP-004 | valid→201+UserProfile; dup-email→409; weak(<8|noUpper|noNum)→400; hash:bcrypt12 | L | P0 |
| 3 | FR-AUTH-003 | Implement JWT issue and refresh | API | COMP-002,COMP-003,DEP-002,API-004 | login→access15m+refresh7d; valid-refresh→200+newpair; expired→401; revoked→401 | L | P0 |
| 4 | FR-AUTH-004 | Implement authenticated profile fetch | API | COMP-001,COMP-005,API-003 | valid-bearer→200+UserProfile; invalid/expired→401; fields:id+email+displayName+createdAt+updatedAt+lastLoginAt+roles | M | P0 |
| 5 | FR-AUTH-005 | Implement password reset flow | API | COMP-001,COMP-004,DEP-006,API-005,API-006 | request(valid-email)→email-sent; confirm(valid-token)→hash-updated; token-ttl:1h; used-token→reject | L | P0 |
| 6 | NFR-PERF-001 | Tune p95 auth latency | Gate | FR-AUTH-001,FR-AUTH-002,FR-AUTH-003,FR-AUTH-004,FR-AUTH-005 | auth-p95:<200ms; apm:on; hotpaths:measured; regressions:blocked | L | P0 |
| 7 | NFR-PERF-002 | Prove 500 concurrent logins | Gate | FR-AUTH-001,NFR-PERF-001 | login-concurrency:500; k6:pass; saturation:within-limit; failures:within-SLO | M | P0 |
| 8 | NFR-REL-001 | Establish 99.9% uptime gate | Ops | API-001,API-003,API-004 | uptime:99.9/30d; healthcheck:on; monitors:live; alert-route:set | M | P0 |
| 9 | NFR-COMP-002 | Persist SOC2 audit events | Ops | DM-003,COMP-001,OQ-008 | events:login+register+refresh+reset; fields:userId+timestamp+ip+outcome; retention:12mo; storage:queryable | L | P0 |
| 10 | API-001 | Contract POST /auth/login | API | FR-AUTH-001 | auth:none; rate:10/min/ip; req:email+password; 200:AuthToken; err:401+423+429 | M | P0 |
| 11 | API-002 | Contract POST /auth/register | API | FR-AUTH-002 | auth:none; rate:5/min/ip; req:email+password+displayName; 201:UserProfile; err:400+409 | M | P0 |
| 12 | API-003 | Contract GET /auth/me | API | FR-AUTH-004 | auth:Bearer; rate:60/min/user; hdr:Authorization; 200:UserProfile; err:401 | M | P0 |
| 13 | API-004 | Contract POST /auth/refresh | API | FR-AUTH-003 | auth:none; rate:30/min/user; req:refreshToken; 200:AuthToken; err:401; old-refresh→revoked | M | P0 |
| 14 | API-005 | Contract POST /auth/reset-request | API | FR-AUTH-005 | auth:none; rate:defined; req:email; resp:generic-success; no-enum:on | M | P1 |
| 15 | API-006 | Contract POST /auth/reset-confirm | API | FR-AUTH-005 | auth:none; rate:defined; req:token+password; resp:success; token:1h+single-use | M | P1 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| /v1/auth router → handlers | Dispatch table | login/register/me/refresh/reset routes mapped to AuthService/TokenManager | 2 | API-001, API-002, API-003, API-004, API-005, API-006 |
| Rate-limit middleware → endpoints | Middleware chain | 10/min, 5/min, 60/min, 30/min, reset caps | 2 | API-001, API-002, API-003, API-004, API-005, API-006 |
| Error formatter → HTTP responses | Callback/serializer | canonical error.code/message/status payload | 2 | Sam persona, all APIs |
| Password reset request → SendGrid | Service callback | token generation, email template, delivery dispatch | 2 | FR-AUTH-005, API-005 |
| AuthService/TokenManager → audit writer | Event binding | success/failure outcomes persisted with IP | 2 | NFR-COMP-002, Jordan persona |

**Phase 3** | Frontend surfaces, admin gaps, and QA | 2 weeks | Exit: user journeys, admin observability gaps, and test pyramid all pass against integrated services

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | OQ-003 | Choose reset email dispatch | Gate | DEP-006,API-005 | mode:sync/async-decided; email-SLA:<60s; retry:defined; failure-UX:set | S | P1 |
| 2 | OQ-005 | Decide remember-me scope | Gate | FR-AUTH-003,COMP-009 | support:yes/no; session-impact:documented; v1/v1.1:assigned | S | P1 |
| 3 | OQ-006 | Specify logout v1 scope | Gate | COMP-010,COMP-009 | logout-story:covered; revoke-path:defined; redirect:landing; shared-device-risk:reduced | S | P0 |
| 4 | OQ-007 | Specify audit viewer scope | Gate | COMP-011,DM-003 | filters:user+date; access:admin-only; retention-view:12mo; incident-use:covered | S | P0 |
| 5 | COMP-009 | Build AuthProvider context | FE | API-004,API-003,OQ-005 | type:context-provider; loc:app-root; props:children:ReactNode; state:AuthToken; silent-refresh:API-004; intercept:401; redirect:on-auth-fail; expose:UserProfile+auth-methods; deps:API-004+API-003 | L | P0 |
| 6 | COMP-006 | Build LoginPage route | FE | COMP-009,API-001,R-002 | type:page; loc:/login; auth:none; props:onSuccess()+redirectUrl?; form:email+password; submit:API-001; token-store:via-COMP-009 | M | P0 |
| 7 | COMP-007 | Build RegisterPage route | FE | COMP-009,API-002,NFR-COMP-001 | type:page; loc:/register; auth:none; props:onSuccess()+termsUrl; form:email+password+displayName; pw-strength:client-validate; submit:API-002 | M | P0 |
| 8 | COMP-008 | Build ProfilePage route | FE | COMP-009,API-003 | type:page; loc:/profile; auth:required; render:UserProfile; source:API-003; deps:COMP-009+API-003 | M | P1 |
| 9 | TEST-001 | Unit test valid login | Test | FR-AUTH-001,COMP-001 | input:valid email+password; verify:hasher-called; issue:tokens-called; return:AuthToken | M | P0 |
| 10 | TEST-002 | Unit test invalid login | Test | FR-AUTH-001,COMP-001 | input:valid email+wrong-pass; verify:false; status:401; token-issue:not-called | M | P0 |
| 11 | TEST-003 | Unit test token refresh | Test | FR-AUTH-003,COMP-002 | input:valid refresh; revoke:old-token; issue:newpair; mocks:Redis+JwtService | M | P0 |
| 12 | TEST-004 | Integration test registration DB | Test | FR-AUTH-002,DEP-001 | scope:AuthService+PostgreSQL; req:email+password+displayName; insert:UserProfile; retrieve:ok | L | P0 |
| 13 | TEST-005 | Integration test refresh TTL | Test | FR-AUTH-003,DEP-002 | scope:TokenManager+Redis; expired-TTL→401; reissue:none; expiry:effective | L | P0 |
| 14 | TEST-006 | E2E register login profile | Test | COMP-006,COMP-007,COMP-008,COMP-009 | flow:Register→Login→Profile; auth-provider:on; profile:visible; playwright:pass | L | P0 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| App root → AuthProvider | Context provider | global auth state and user exposure | 3 | COMP-006, COMP-007, COMP-008 |
| AuthProvider → route guards | Registry/guard chain | public routes and protected routes split | 3 | LoginPage, RegisterPage, ProfilePage |
| AuthProvider → 401 interceptor | Callback/middleware | silent refresh then redirect on failure | 3 | API-003, API-004 |
| Login/Register pages → submit handlers | Event binding | form submit to API contracts with inline validation | 3 | API-001, API-002 |
| Logout action → token revoker | Event binding | user-initiated session end path | 3 | OQ-006, COMP-010 |
| Admin audit viewer → log query API | Query binding | user/date filters to AuditLog store | 3 | OQ-007, COMP-011 |

**Phase 4** | Rollout, operations, and production validation | 4 weeks | Exit: staged rollout complete, rollback tested, SLOs met, success metrics observable in GA

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-001 | Run internal alpha rollout | Gate | FR-AUTH-001,FR-AUTH-002,FR-AUTH-003,FR-AUTH-004,FR-AUTH-005 | env:staging; users:auth-team+QA; flag:AUTH_NEW_LOGIN-on; P0/P1:0 | M | P0 |
| 2 | MIG-002 | Run 10% beta rollout | Gate | MIG-001,NFR-PERF-001,NFR-PERF-002 | traffic:10%; p95:<200ms; err-rate:<0.1%; Redis-fail:0 | L | P0 |
| 3 | MIG-003 | Execute GA cutover | Gate | MIG-002,SC-004 | traffic:100%; dashboards:green; flag-removal:AUTH_NEW_LOGIN; legacy:deprecated | L | P0 |
| 4 | MIG-004 | Operate AUTH_NEW_LOGIN flag | Gate | MIG-001 | purpose:new-login-gate; default:OFF; target-remove:post-GA; rollback:ready | S | P0 |
| 5 | MIG-005 | Operate AUTH_TOKEN_REFRESH flag | Gate | FR-AUTH-003,MIG-003 | purpose:refresh-gate; default:OFF; target-remove:GA+2w; only-access-when-off:on | S | P1 |
| 6 | MIG-006 | Drill rollback procedure | Ops | MIG-001,MIG-002,MIG-004 | step1:disable-AUTH_NEW_LOGIN; smoke:legacy-ok; root-cause:logged; backup-restore:ready; notify:auth+platform; postmortem:<48h | M | P0 |
| 7 | MIG-007 | Enforce rollback criteria | Gate | MIG-006,NFR-PERF-001,NFR-REL-001 | p95>1000ms/5m→rollback; err>5%/2m→rollback; Redis-fail>10/min→rollback; data-corrupt→rollback | M | P0 |
| 8 | OPS-001 | Publish AuthService down runbook | Ops | COMP-001,DEP-001,DEP-002 | symptoms:5xx+/auth/*; diag:k8s+PG+initlogs; resolve:restart/failover/relogin; escalate:15m | M | P0 |
| 9 | OPS-002 | Publish refresh failure runbook | Ops | COMP-002,COMP-003,MIG-005 | symptoms:logout-loop+counter-spike; diag:Redis+key+flag; resolve:scale/remount/enable-flag; page:on-call | M | P0 |
| 10 | OPS-003 | Staff 24/7 launch on-call | Ops | MIG-003 | ack:P1<15m; coverage:24/7+2w; path:auth→test-lead→eng-manager→platform; tools:k8s+Grafana+RedisCLI+PGadmin | M | P1 |
| 11 | OPS-004 | Validate capacity scaling plan | Infra | NFR-PERF-002,DEP-001,DEP-002 | pods:3→10@CPU>70%; pg-pool:100→200@wait>50ms; Redis:1GB→2GB@mem>70% | M | P0 |
| 12 | R-001 | Mitigate token theft via XSS | Sec | FR-AUTH-003,COMP-009 | accessToken:memory-only; refresh:HttpOnly-cookie; access-ttl:15m; revoke-path:ready | L | P0 |
| 13 | R-002 | Mitigate brute-force login abuse | Sec | API-001,FR-AUTH-001 | gw-rate:10/min/ip; lockout:5fail/15m; bcrypt:12; WAF-block:ready; captcha>3fail:planned | L | P0 |
| 14 | R-003 | Protect migration data integrity | DB | MIG-001,MIG-002,MIG-006 | parallel-op:on; upsert:idempotent; backup:each-phase; restore:test-pass | M | P0 |
| 15 | R-004 | Improve registration adoption | FE | COMP-007,SC-006 | usability-test:prelaunch; funnel:tracked; iterate:on-dropoff; conversion-target:owned | M | P1 |
| 16 | R-005 | Run security breach prevention gate | Sec | TEST-001,TEST-002,TEST-003,MIG-002 | sec-review:done; pentest:done; critical-findings:0; prod-gate:blocked-until-pass | L | P0 |
| 17 | R-006 | Validate audit completeness | Ops | NFR-COMP-002,COMP-011 | SOC2-controls:mapped; missing-events:0; retention:12mo; query-check:pass | M | P0 |
| 18 | R-007 | Monitor email delivery health | Ops | DEP-006,API-005,API-006 | reset-email-SLA:<60s; delivery-alert:on; fallback:support; failures:triaged | M | P1 |
| 19 | SC-001 | Validate login p95 target | Gate | NFR-PERF-001,API-001 | metric:login-p95; target:<200ms; measure:APM login(); phase:beta+GA | M | P0 |
| 20 | SC-002 | Validate registration success rate | Gate | FR-AUTH-002,API-002 | metric:reg-success; target:>99%; measure:success/attempts; alert:on-drop | M | P1 |
| 21 | SC-003 | Validate refresh p95 latency | Gate | FR-AUTH-003,API-004 | metric:refresh-p95; target:<100ms; measure:APM refresh(); regressions:blocked | M | P0 |
| 22 | SC-004 | Validate service availability | Gate | NFR-REL-001 | metric:uptime; target:99.9%; measure:30d healthchecks; breach:page | M | P0 |
| 23 | SC-005 | Validate bcrypt hash time | Gate | NFR-SEC-001,COMP-004 | metric:hash-time; target:<500ms; measure:benchmark cost12; drift:blocked | S | P0 |
| 24 | SC-006 | Validate registration conversion | Gate | COMP-007,R-004 | metric:funnel-conversion; target:>60%; measure:landing→confirmed; phase:GA | M | P1 |
| 25 | SC-007 | Validate authenticated DAU growth | Gate | MIG-003,COMP-009 | metric:auth-DAU; target:>1000/30d; measure:token-issuance-counts; trend:reported | M | P1 |
| 26 | SC-008 | Validate average session duration | Gate | COMP-009,API-004 | metric:session-duration; target:>30m; measure:refresh-analytics; expiry-UX:reviewed | M | P1 |
| 27 | SC-009 | Validate failed login rate | Gate | API-001,NFR-COMP-002 | metric:failed-login-rate; target:<5%; measure:audit-log-analysis; spikes:alerted | M | P1 |
| 28 | SC-010 | Validate reset completion rate | Gate | API-005,API-006,R-007 | metric:reset-completion; target:>80%; measure:req→reset funnel; blockers:triaged | M | P1 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Feature flag service → login routes | Registry/gating | AUTH_NEW_LOGIN percentage rollout and rollback | 4 | MIG-001, MIG-002, MIG-003, MIG-004 |
| Feature flag service → refresh flow | Registry/gating | AUTH_TOKEN_REFRESH enablement path | 4 | MIG-003, MIG-005, OPS-002 |
| Alert rules → on-call rota | Event binding | latency, error, Redis, delivery, uptime alerts | 4 | OPS-001, OPS-002, OPS-003, SC-004 |
| Dashboards → rollback controller | Decision gate | SLO breach thresholds trigger rollback | 4 | MIG-006, MIG-007 |
| Analytics funnel → product reviews | Reporting pipeline | registration, session, reset, failed-login metrics | 4 | SC-002, SC-006, SC-008, SC-009, SC-010 |

## Risk Assessment and Mitigation
1. Prioritize security and compliance gates before broad traffic exposure.
2. Treat Redis, PostgreSQL, and email delivery as independent failure domains with rehearsed fallbacks.
3. Do not remove feature flags until GA telemetry is stable and rollback drills have passed.

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | R-001 Token theft via XSS | High | Medium | Session hijack, forced resets, trust loss | accessToken memory-only; refresh HttpOnly; 15m TTL; revoke workflow | security + FE |
| 2 | R-002 Brute-force login abuse | Medium | High | Account lockouts, attack traffic, support load | gateway rate limits; 5fail/15m lockout; WAF blocks; CAPTCHA contingency | security + platform |
| 3 | R-003 Data loss during migration | High | Low | Account corruption, rollback, launch delay | idempotent upserts; backups each phase; restore rehearsal; legacy parallel path | platform + DB |
| 4 | R-004 Low registration adoption | High | Medium | Revenue delay, poor funnel performance | usability testing; funnel instrumentation; iterate RegisterPage copy/validation | product + FE |
| 5 | R-005 Security breach from flaws | Critical | Low | Incident response, audit failure, reputational damage | dedicated security review; penetration test; prod gate on zero critical findings | security |
| 6 | R-006 Incomplete audit logging | High | Medium | SOC2 failure, incident blind spots | early schema freeze; event coverage tests; admin query validation; 12mo retention | compliance + ops |
| 7 | R-007 Email delivery failures | Medium | Low | Password reset blockage, support tickets | delivery alerts; retry policy; fallback support path; SendGrid sandbox/prod checks | ops |

## Resource Requirements and Dependencies
### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ (DEP-001) | 1 | Must provision before schema freeze | Block rollout; fail to legacy auth if unavailable |
| Redis 7+ (DEP-002) | 1 | Must provision before refresh design closes | Disable refresh; force re-login |
| Node.js 20 LTS (DEP-003) | 1 | Standardize in CI and runtime images | No fallback; service cannot start |
| bcryptjs (DEP-004) | 1 | Pin and security-scan before implementation | No fallback in v1.0 |
| jsonwebtoken (DEP-005) | 1 | Pin and validate RS256 support | No fallback in v1.0 |
| SendGrid API (DEP-006) | 2 | Sandbox early, prod before reset launch | Support-assisted reset process |
| Frontend routing framework (DEP-007) | 1 | Confirm guard and redirect support | Delay FE rollout; keep API-only validation |
| SEC-POLICY-001 | 1 | Product/security signoff required | Freeze security-sensitive scope until clarified |

### Infrastructure Requirements
- Kubernetes deployment with HPA from 3 to 10 `AuthService` replicas.
- PostgreSQL pool baseline 100, expansion path to 200 when wait time exceeds 50ms.
- Redis memory baseline 1 GB, expansion path to 2 GB at 70% utilization.
- TLS 1.3 termination, restricted CORS allowlist, and URL versioning on `/v1/auth/*`.
- APM, OpenTelemetry traces, Prometheus metrics, structured logs, and alert routing before beta.

### Teaming and ownership
- **auth-team:** backend service, token lifecycle, test ownership.
- **frontend team:** `AuthProvider`, `LoginPage`, `RegisterPage`, `ProfilePage`, funnel UX.
- **security/compliance:** RS256, NIST/GDPR/SOC2 validation, pen test, audit coverage.
- **platform/ops:** infra provisioning, feature flags, monitoring, on-call, rollback rehearsals.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| SC-001 | Login response time (p95) | < 200ms | APM on `AuthService.login()` during beta+GA | 4 |
| SC-002 | Registration success rate | > 99% | Registration attempt/success ratio on API-002 | 4 |
| SC-003 | Token refresh latency (p95) | < 100ms | APM on `TokenManager.refresh()` | 4 |
| SC-004 | Service availability | 99.9% uptime | 30-day health-check monitoring and alert audit | 4 |
| SC-005 | Password hash time | < 500ms | bcrypt cost-12 benchmark in CI and pre-GA | 4 |
| SC-006 | Registration conversion | > 60% | landing→register→confirmed funnel analytics | 4 |
| SC-007 | Daily active authenticated users | > 1000 in 30 days | token issuance and active-user analytics | 4 |
| SC-008 | Average session duration | > 30 minutes | refresh event analytics and cohort review | 4 |
| SC-009 | Failed login rate | < 5% of attempts | audit-log analysis with alert thresholds | 4 |
| SC-010 | Password reset completion | > 80% | reset requested→password updated funnel | 4 |

Validation sequence:
- Phase 1: contract and schema validation, security baseline checks, dependency readiness.
- Phase 2: unit/integration/API contract tests plus performance/load baselines.
- Phase 3: Playwright E2E journeys, UX checks against Alex/Jordan/Sam personas, admin-gap closure.
- Phase 4: staged rollout telemetry, rollback rehearsal, security/compliance signoff, GA metric review.

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| 1 | 2 weeks | 2026-04-15 | 2026-04-28 | Infra ready; retention conflict closed; schemas frozen; core modules scaffolded |
| 2 | 3 weeks | 2026-04-29 | 2026-05-19 | Auth APIs live; audit logging wired; perf and concurrency baselines pass |
| 3 | 2 weeks | 2026-05-20 | 2026-06-02 | FE routes live; AuthProvider stable; E2E flows green; admin gaps specified |
| 4 | 4 weeks | 2026-06-03 | 2026-06-30 | Alpha→beta→GA; rollback drill passed; SLOs and success metrics validated |

**Total estimated duration:** 11 weeks

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | OQ-001 Should `AuthService` support API key auth? | Changes future service-auth boundary and TokenManager extensibility | 1 | test-lead |
| 2 | OQ-002 Max allowed `UserProfile.roles` length? | Affects schema validation, JWT size, downstream auth payloads | 1 | auth-team |
| 3 | OQ-003 Send reset emails synchronously or asynchronously? | Changes UX latency, queueing design, and delivery retry model | 3 | Engineering |
| 4 | OQ-004 Max refresh tokens per user across devices? | Changes Redis cardinality, revocation logic, and device UX | 1 | Product |
| 5 | OQ-005 Support remember-me session extension? | Changes FE session UX and token lifetime expectations | 3 | Product |
| 6 | OQ-006 Add logout functionality missing from TDD? | PRD scope gap; affects session revocation and shared-device safety | 3 | Product + Engineering |
| 7 | OQ-007 Add admin audit log viewing capability? | PRD scope gap; affects Jordan persona and incident workflows | 3 | Product + Engineering |
| 8 | OQ-008 Confirm PRD 12-month audit retention override? | Blocks storage sizing, compliance signoff, and audit design | 1 | Product + Compliance |
