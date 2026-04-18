---
spec_source: test-tdd-user-auth.md
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
generated: "2026-04-16"
generator: "single"
total_phases: 5
total_task_rows: 67
risk_count: 7
open_questions: 11
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap sequences the authentication platform as a security-first foundation, then core auth contracts, then frontend/session UX, then admin/compliance controls, and finally controlled rollout. That ordering minimizes rework across JWT signing, Redis token lifecycle, audit retention, and frontend silent refresh while delivering the fastest path to measurable business value: user registration, persistent sessions, and self-service recovery.

**Business Impact:** Authentication unblocks the Q2-Q3 personalization roadmap, supports the Q3 2026 SOC2 deadline, reduces support burden for access recovery, and protects the projected $2.4M annual value tied to identity-dependent features.

**Complexity:** HIGH (0.72) — Security-critical flows span PostgreSQL, Redis, JWT key management, SendGrid delivery, React session handling, audit retention, and phased rollout/rollback requirements.

**Critical path:** security baselines and schemas → AuthService/TokenManager contracts → login/register/refresh/profile APIs → AuthProvider/page integration → audit/admin controls → alpha/beta/GA rollout.

**Key architectural decisions:**

- Use PostgreSQL for durable user and audit records, with Redis reserved for hashed refresh-token lifecycle only.
- Keep access tokens short-lived and memory-resident, rotate opaque refresh tokens on every refresh, and fail closed when Redis is unavailable.
- Treat auditability and rollout gates as first-class workstreams rather than post-build hardening.

**Open risks requiring resolution before Phase 1:**

- Confirm the PRD-over-TDD retention rule as authoritative: audit logs retain for 12 months, not 90 days.
- Confirm refresh-token concurrency policy across devices before finalizing Redis keying and revocation semantics.
- Decide whether reset emails are synchronous or asynchronous before password-reset implementation begins.
- Confirm whether Jordan’s admin workflow requires read-only visibility or active account unlock in v1.0.

**Phase 1** | milestone: M1 Security and data baseline | duration: Weeks 1-2 | exit criteria: schemas, cryptography, observability, and SLO controls ready for backend feature work

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DM-001 | Persist UserProfile schema | DB | — | id:UUIDv4-PK; email:unique+idx+lowercase+notNull; displayName:2-100+notNull; createdAt:ISO8601+defaultNow; updatedAt:ISO8601+autoUpdate; lastLoginAt:ISO8601+nullable; roles:string[]+default[user]; rel:refreshTokensByUserId+auditRefs | L | P0 |
| 2 | COMP-009 | Build UserRepo adapter | DB | DM-001 | store:PostgreSQL15; entity:UserProfile; ops:findByEmail+findById+create+updateLastLogin+updatePassword+setLockState+recordConsent; refs:auditLog | L | P0 |
| 3 | COMP-008 | Build PasswordHasher abstraction | Sec | — | algo:bcrypt; cost:12; abstraction:true; ops:hash+verify; futureMigration:enabled; rawLog:none | M | P0 |
| 4 | COMP-007 | Build JwtService signer/verifier | Sec | — | alg:RS256; key:rsa2048; ops:sign+verify; rotate:quarterly; skew:5s | M | P0 |
| 5 | NFR-SEC-001 | Enforce bcrypt cost 12 | Sec | COMP-008 | bcrypt:12; unit:assertCost; hash<500ms; rawPassword:none | S | P0 |
| 6 | NFR-SEC-002 | Enforce RS256 RSA signing | Sec | COMP-007 | alg:RS256; key:2048-bit; cfgTest:pass; rotation:qtr | S | P0 |
| 7 | NFR-COMPLIANCE-001 | Implement audit and consent controls | Sec | DM-001, COMP-009 | audit:userId+timestamp+ip+outcome; retain:12mo; consent:timestamp@register; pii:email+hashedPassword+displayNameOnly; rawSecrets:none; nist800-63B:pass | L | P0 |
| 8 | OPS-005 | Provision auth observability | Ops | NFR-COMPLIANCE-001 | logs:login+register+refresh+reset; metrics:auth_login_total+auth_login_duration_seconds+auth_token_refresh_total+auth_registration_total; traces:AuthService>PasswordHasher|TokenManager|JwtService; alerts:failRate>20%/5m+p95>500ms+redisFailures | L | P1 |
| 9 | OPS-004 | Size auth capacity baseline | Infra | OPS-005 | replicas:3-10@cpu>70%; pgPool:100>200@ifWait>50ms; redis:1GB>2GB@ifUtil>70%; target:500concurrent+100kRefresh | M | P1 |
| 10 | NFR-REL-001 | Define uptime health gates | Gate | OPS-005 | availability:99.9%/30d; healthEndpoint:monitored; slo:published; alerting:on | M | P1 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| PasswordHasher → AuthService | dependency | bcrypt hash/verify abstraction | Phase 1 | COMP-005 |
| JwtService → TokenManager | dependency | RS256 sign/verify with 5s skew | Phase 1 | COMP-006 |
| UserRepo → PostgreSQL | adapter | user persistence and lock state | Phase 1 | COMP-005 |
| Auth telemetry pipeline | middleware | logs, metrics, traces, alerts | Phase 1 | OPS-001, OPS-002, OPS-003, MIG-001 |

**Phase 2** | milestone: M2 Core backend auth contracts | duration: Weeks 3-5 | exit criteria: backend APIs and token lifecycle satisfy login, register, refresh, and profile requirements

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DM-002 | Define AuthToken contract | API | COMP-007, COMP-006 | accessToken:JWT+RS256+userId+roles+ttl15m; refreshToken:opaque+unique+hashedInRedis+ttl7d; expiresIn:number=900; tokenType:string=Bearer | M | P0 |
| 2 | COMP-006 | Implement TokenManager lifecycle | API | COMP-007, DM-002 | deps:JwtService+Redis; issue:access+refresh; store:hashedRefresh+ttl7d; rotate:revokeOldOnRefresh; reject:expired+revoked; failClosed:redisDown | L | P0 |
| 3 | COMP-005 | Implement AuthService orchestration | API | COMP-008, COMP-006, COMP-007, COMP-009 | deps:PasswordHasher+TokenManager+JwtService+UserRepo; ops:login+register+me+resetRequest+resetConfirm; lockout:enforced; normalizeEmail:true | XL | P0 |
| 4 | FR-AUTH-001 | Deliver login credential flow | API | COMP-005, DM-002 | valid→200+AuthToken; invalid→401; missingUser→401; 5fail/15min→423; no-enum | L | P0 |
| 5 | API-001 | Expose POST /v1/auth/login | API | FR-AUTH-001, DM-002 | auth:none; rate:10/min/IP; req:email+password; 200:AuthToken; 401:invalid; 423:locked; 429:limited; envelope:error.code+message+status | M | P0 |
| 6 | FR-AUTH-002 | Deliver registration flow | API | COMP-005, DM-001, COMP-008 | valid→201+UserProfile; dupEmail→409; weakPwd→400; bcryptCost12; consentRecorded | L | P0 |
| 7 | API-002 | Expose POST /v1/auth/register | API | FR-AUTH-002, DM-001 | auth:none; rate:5/min/IP; req:email+password+displayName; 201:UserProfile; 400:weakPwd|invalidEmail; 409:emailConflict; envelope:error.code+message+status | M | P0 |
| 8 | FR-AUTH-003 | Deliver token issue and refresh | API | COMP-006, DM-002 | login→access15m+refresh7d; refreshValid→200+newPair; refreshExpired→401; refreshRevoked→401; revokeOld:true | L | P0 |
| 9 | API-004 | Expose POST /v1/auth/refresh | API | FR-AUTH-003, DM-002 | auth:body.refreshToken; rate:30/min/user; req:refreshToken; 200:newAuthToken+oldRevoked; 401:expired|revoked; envelope:error.code+message+status | M | P0 |
| 10 | FR-AUTH-004 | Deliver authenticated profile read | API | COMP-005, DM-001 | validJWT→200+UserProfile; invalid|expired→401; fields:id+email+displayName+createdAt+updatedAt+lastLoginAt+roles | M | P0 |
| 11 | API-003 | Expose GET /v1/auth/me | API | FR-AUTH-004, DM-001 | auth:BearerJWT; rate:60/min/user; hdr:Authorization; 200:UserProfile; 401:missing|expired|invalid; envelope:error.code+message+status | M | P0 |
| 12 | NFR-PERF-001 | Meet auth endpoint latency SLO | Gate | API-001, API-002, API-003, API-004, OPS-005 | allAuth:p95<200ms; apm:AuthServiceMethods; regressions:none | M | P1 |
| 13 | NFR-PERF-002 | Meet concurrent login target | Gate | API-001, OPS-004 | login:500concurrent; load:k6; p95<200ms; saturation:acceptable | M | P1 |
| 14 | TEST-001 | Verify valid login token issue | Test | FR-AUTH-001, COMP-005, COMP-006 | input:validEmail+password; verify:PasswordHasher.verifyCalled; issue:TokenManager.issueTokensCalled; out:AuthToken | S | P1 |
| 15 | TEST-002 | Verify invalid login rejection | Test | FR-AUTH-001, COMP-005 | input:badPassword; out:401; issueTokens:notCalled | S | P1 |
| 16 | TEST-003 | Verify refresh token rotation | Test | FR-AUTH-003, COMP-006 | input:validRefresh; validate:Redis+JwtService; revoke:old; issue:newPair | S | P1 |
| 17 | TEST-004 | Verify registration DB persist | Test | FR-AUTH-002, API-002, DM-001 | path:api>hasher>dbInsert; bcrypt:true; out:201; store:UserProfile | M | P1 |
| 18 | TEST-005 | Verify expired refresh rejection | Test | FR-AUTH-003, API-004 | input:expiredRefresh; redisTTL:expired; out:401 | M | P1 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Route registry /v1/auth/* | dispatch table | login/register/me/refresh handlers bound | Phase 2 | API Gateway, frontend |
| TokenManager → Redis | token store | hashed refresh records with 7d TTL | Phase 2 | AuthProvider, API-004 |
| JwtService → middleware verifier | middleware | Bearer verification for /auth/me | Phase 2 | API-003 |
| Error envelope formatter | callback chain | uniform {error:{code,message,status}} | Phase 2 | all auth endpoints |

**Phase 3** | milestone: M3 Password reset and frontend session UX | duration: Weeks 6-8 | exit criteria: end-user flows work across register, login, refresh, profile, reset, and logout journeys

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-001 | Build LoginPage route | FE | API-001, COMP-004 | route:/login; public:true; props:onSuccess()+redirectUrl?; form:email+password; call:POST/auth/login; store:AuthTokenViaAuthProvider | L | P0 |
| 2 | COMP-002 | Build RegisterPage route | FE | API-002, COMP-004 | route:/register; public:true; props:onSuccess()+termsUrl; form:email+password+displayName; validate:pwdStrengthClient; call:POST/auth/register | L | P0 |
| 3 | COMP-003 | Build ProfilePage route | FE | API-003, COMP-004 | route:/profile; auth:required; show:UserProfileViaGET/auth/me | M | P0 |
| 4 | COMP-004 | Build AuthProvider context | FE | API-001, API-003, API-004, DM-002 | props:children:ReactNode; wraps:PublicRoutes+ProtectedRoutes; state:AuthToken; silentRefresh:viaTokenManager; on401:refreshOrRedirectLoginPage; expose:UserProfile+authMethods | XL | P0 |
| 5 | FR-AUTH-005 | Deliver password reset flow | API | COMP-005, COMP-008 | resetRequestValidEmail→sendToken; resetConfirmValidToken→updateHash; tokenTTL:1h; usedToken→reject; reset→invalidateAllSessions | L | P0 |
| 6 | API-005 | Expose POST /v1/auth/reset-request | API | FR-AUTH-005 | auth:none; req:email; resp:genericSuccess; enum:none; email<60s; rate:bounded | M | P0 |
| 7 | API-006 | Expose POST /v1/auth/reset-confirm | API | FR-AUTH-005 | auth:none; req:token+newPassword; valid→200; expired|used→401|400; passwordUpdated:true; sessionsInvalidated:true | M | P0 |
| 8 | API-007 | Expose POST /v1/auth/logout | API | COMP-006, COMP-004 | auth:sessionContext; req:refreshToken|session; out:204; revoke:currentRefresh; redirect:landing; clearsClientState:true | M | P1 |
| 9 | COMP-010 | Build ResetRequestPage route | FE | API-005 | route:/forgot-password; form:email; resp:genericSuccess; enum:none | M | P1 |
| 10 | COMP-011 | Build ResetConfirmPage route | FE | API-006 | route:/reset-password; form:token+newPassword; valid→loginRedirect; expired→newRequestPrompt | M | P1 |
| 11 | COMP-012 | Build Logout action control | FE | API-007, COMP-004 | action:LogOut; revoke:session; redirect:landing; clear:authState | S | P1 |
| 12 | TEST-006 | Verify register-login-profile journey | Test | COMP-001, COMP-002, COMP-003, COMP-004 | flow:RegisterPage>LoginPage>ProfilePage; out:endToEndSuccess; authProvider:true | L | P1 |
| 13 | TEST-007 | Verify logout ends session | Test | API-007, COMP-012 | logout→204; authState:cleared; protectedRoute→loginRedirect | M | P1 |
| 14 | TEST-008 | Verify reset request privacy | Test | API-005, COMP-010 | registered|unknown→sameResponse; emailSent:registeredOnly; enum:none | M | P1 |
| 15 | TEST-009 | Verify reset confirm invalidates sessions | Test | API-006, COMP-006 | resetConfirm→passwordUpdated; allRefreshRevoked:true; oldSessions→401 | M | P1 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthProvider → route guards | context/provider | PublicRoutes and ProtectedRoutes wrapped | Phase 3 | LoginPage, RegisterPage, ProfilePage |
| 401 interceptor → refresh callback | middleware chain | refresh or redirect on unauthorized responses | Phase 3 | AuthProvider children |
| Logout control → revoke endpoint | event binding | click handler posts logout and clears state | Phase 3 | end users |
| Reset email template → SendGrid | dispatch | request generates time-limited reset delivery | Phase 3 | API-005 |

**Phase 4** | milestone: M4 Admin, compliance, and operational hardening | duration: Weeks 9-10 | exit criteria: audit/admin gaps, runbooks, and production-readiness controls are complete

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-013 | Build AuditLog query service | Sec | NFR-COMPLIANCE-001, COMP-009 | queryBy:user+dateRange; fields:userId+eventType+timestamp+ip+outcome; retention:12mo | L | P0 |
| 2 | API-008 | Expose GET /v1/auth/audit | API | COMP-013 | auth:admin; filters:userId+dateFrom+dateTo+outcome; out:queryableAuditRows; pii:minimized | M | P1 |
| 3 | COMP-014 | Build AccountLock admin service | Sec | COMP-009, FR-AUTH-001 | ops:viewLock+unlockAccount; reason:capture; audit:onUnlock | M | P1 |
| 4 | API-009 | Expose POST /v1/auth/unlock | API | COMP-014 | auth:admin; req:userId+reason; locked→200+unlocked; audit:written; unauthorized→403 | M | P1 |
| 5 | OPS-001 | Author AuthService down runbook | Ops | OPS-005, COMP-005 | symptoms:5xx/allAuth+pageErrors; diagnose:k8s+pg+initLogs; resolve:restart+pgFailover; escalate:authOncall>platform@15m | M | P1 |
| 6 | OPS-002 | Author refresh failure runbook | Ops | OPS-005, COMP-006 | symptoms:logouts+redirectLoop+refreshErrors; diagnose:redis+jwtKeys+flagState; resolve:scaleRedis+remountSecrets+toggleFlag | M | P1 |
| 7 | OPS-003 | Define on-call auth rotation | Ops | OPS-001, OPS-002 | p1Ack<15m; rotation:24/7first2wPostGA; tools:k8s+grafana+redisCli+pgAdmin; mttr<60m | M | P1 |
| 8 | TEST-010 | Verify audit log completeness | Test | COMP-013, API-008, NFR-COMPLIANCE-001 | events:login+register+refresh+reset+unlock; fields:userId+timestamp+ip+outcome; retention:12mo | M | P1 |
| 9 | TEST-011 | Verify account unlock flow | Test | API-009, COMP-014 | lockedUser→unlock200; subsequentLoginAllowed:true; audit:onUnlock | M | P2 |
| 10 | TEST-012 | Verify load and fail-closed ops | Test | NFR-PERF-002, COMP-006, OPS-004 | 500concurrent:pass; redisDown→refresh401+relogin; noPartialSession | M | P1 |
| 11 | OQ-007 | Resolve admin audit gap from PRD | Docs | COMP-013, API-008, API-009 | resolution:PRDRequires; tddUpdate:needed; scope:v1.0AdminVisibility+unlockDecision | S | P0 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuditLog query service → admin API | service registry | date/user filters wired to audit store | Phase 4 | Jordan admin workflows |
| AccountLock service → unlock endpoint | command handler | admin unlock operation with audit write | Phase 4 | Security, support |
| Alert rules → on-call escalation | monitoring binding | failure thresholds route incidents | Phase 4 | OPS-003 |
| Compliance evidence pack | reporting pipeline | test outputs and retention evidence assembled | Phase 4 | SOC2 review |

**Phase 5** | milestone: M5 Controlled rollout and GA | duration: Weeks 11-12 | exit criteria: alpha, beta, and GA gates pass; flags retired; legacy paths deprecated with rollback safety

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-001 | Execute internal alpha rollout | Gate | API-001, API-002, API-003, API-004, API-005, API-006, COMP-001, COMP-002 | stageDeploy:true; manualQA:FR-AUTH-001..005; bugs:P0=0+P1=0; flag:AUTH_NEW_LOGIN=ONforAlpha; rollback:disableFlag | L | P0 |
| 2 | MIG-002 | Execute beta 10% rollout | Gate | MIG-001, NFR-PERF-001, COMP-004 | traffic:10%; p95<200ms; errorRate<0.1%; redisFailures:0TokenManager; refreshRealLoad:observed; rollback:flagPct=0 | L | P0 |
| 3 | MIG-003 | Execute GA 100% rollout | Gate | MIG-002, NFR-REL-001, OPS-003 | traffic:100%; uptime:99.9%first7d; dashboards:green; remove:AUTH_NEW_LOGIN; deprecate:legacyEndpoints; enable:AUTH_TOKEN_REFRESH; rollback:legacyFlag | L | P0 |
| 4 | OQ-001 | Defer API key auth to v1.1 | Docs | MIG-003 | outOfScope:v1.0; revisit:v1.1; decisionLogged:true | S | P2 |
| 5 | OQ-002 | Resolve roles array max length | Docs | DM-001 | rolesMax:defined; downstreamRBAC:documented; decisionLogged:true | S | P2 |
| 6 | OQ-003 | Resolve reset email delivery mode | Docs | API-005 | mode:sync|async; rationale:captured; tddUpdate:required | S | P1 |
| 7 | OQ-004 | Resolve refresh token device cap | Docs | COMP-006 | maxTokensPerUser:defined; redisKeying:aligned; revokePolicy:aligned | S | P1 |
| 8 | OQ-005 | Confirm lockout policy parameters | Docs | FR-AUTH-001 | threshold:5/15min|updated; securityApproval:true; docsAligned:true | S | P1 |
| 9 | OQ-006 | Resolve remember-me scope | Docs | COMP-004 | scope:v1.0|defer; sessionDurationImpact:documented; noHiddenExtension:true | S | P2 |
| 10 | OQ-008 | Reconcile audit retention conflict | Docs | NFR-COMPLIANCE-001 | retention:12mo; prdWins:true; tddCorrected:true | S | P0 |
| 11 | OQ-009 | Decide multi-device session policy | Docs | COMP-006, API-007 | concurrentDevices:allowed|bounded; logoutSemantics:single|all; docsAligned:true | S | P1 |
| 12 | OQ-010 | Clarify admin unlock in v1.0 | Docs | API-009 | unlock:v1.0|v1.1; stakeholderApproval:true; roadmapAligned:true | S | P1 |
| 13 | OQ-011 | Reconcile logout requirement gap | Docs | API-007, COMP-012 | resolution:PRDRequires; tddUpdate:needed; userStoryCovered:true | S | P0 |

### Integration Points — Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Feature flag AUTH_NEW_LOGIN | flag | frontend login/register traffic gate | Phase 5 | MIG-001, MIG-002, MIG-003 |
| Feature flag AUTH_TOKEN_REFRESH | flag | refresh flow enablement and cleanup | Phase 5 | COMP-004, MIG-003 |
| Rollback playbook → legacy route switch | operational switch | disable new flow and smoke-test legacy | Phase 5 | auth-team, platform-team |
| Release dashboards → go/no-go gate | gate | p95, error, redis, uptime checks | Phase 5 | release managers |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | R-001 Token theft via XSS | HIGH | Medium | Session hijack | accessToken:memoryOnly; refresh:HttpOnly; ttl:15m; revoke:onRefresh/reset; clearOnTabClose | security-team |
| 2 | R-002 Brute-force login abuse | MEDIUM | High | Account compromise | gateway:10/min/IP; lockout:5/15m; bcrypt:12; waf:block; captchaAfter3Fails | auth-team |
| 3 | R-003 Legacy migration data loss | HIGH | Low | User/account corruption | parallelRun:Phase1-2; idempotentUpserts; preBackup:true; restoreRollback:true | platform-team |
| 4 | R-004 Redis refresh outage | MEDIUM | Medium | Forced re-login | failClosed:true; monitor+alert; scaleOut:ready; noPartialRefresh | auth-team |
| 5 | R-005 JWT clock skew errors | LOW | Medium | False 401s | skewTolerance:5s; clockSync:required; configTest:pass | platform-team |
| 6 | R-006 Reset email delivery failure | MEDIUM | Medium | Recovery blocked | sendgridMonitoring:true; alerting:on; supportFallback:documented | auth-team |
| 7 | R-007 Incomplete audit logging | HIGH | Medium | SOC2 failure | defineFieldsEarly; qaAgainstSOC2; retain:12mo; adminQueryPath:implemented | compliance-team |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ | Phase 1 | Required | block release until provisioned |
| Redis 7+ | Phase 2 | Required | refresh disabled; force re-login |
| Node.js 20 LTS | Phase 1 | Required | none |
| bcryptjs | Phase 1 | Required | swap to equivalent bcrypt binding via abstraction |
| jsonwebtoken | Phase 1 | Required | swap JOSE-compatible signer behind JwtService |
| SendGrid API | Phase 3 | Required | support fallback channel; queue retries |
| API Gateway | Phase 2 | Required | app-level temporary throttles only |
| SEC-POLICY-001 | Phase 1 | Required | security sign-off blocks go-live |
| Frontend routing framework | Phase 3 | Required | delay FE launch; backend can proceed |
| Kubernetes + HPA | Phase 4 | Required | static replicas for pre-GA only |

### Infrastructure Requirements

- Provision PostgreSQL with backup/restore validated before migration and rollout.
- Provision Redis with monitoring, alerting, and capacity for ~100K refresh tokens.
- Mount RSA signing keys securely and support quarterly rotation without downtime.
- Enforce TLS 1.3 and CORS allowlists at API Gateway.
- Stand up staging with seeded accounts plus isolated SendGrid, PostgreSQL, and Redis dependencies.
- Configure APM, Prometheus, OpenTelemetry, dashboards, and release gates before beta.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| Login latency | p95 login response | <200ms | APM on AuthService.login + API-001 | Phase 2 |
| Registration reliability | registration success rate | >99% | endpoint analytics + TEST-004 | Phase 2 |
| Refresh latency | p95 refresh latency | <100ms | APM on TokenManager.refresh + API-004 | Phase 2 |
| Service uptime | rolling availability | 99.9% | health checks + SLO dashboards | Phase 5 |
| Hash performance | PasswordHasher.hash | <500ms | unit/perf tests with cost 12 | Phase 1 |
| Unit coverage | core auth modules | >80% | CI coverage across AuthService/TokenManager/JwtService/PasswordHasher | Phase 4 |
| Integration fidelity | auth endpoints against real stores | 4+ endpoints pass | integration tests with PostgreSQL + Redis | Phase 2 |
| Concurrency | login load | 500 concurrent | k6 load test with p95<200ms | Phase 4 |
| Registration funnel | conversion rate | >60% | product funnel analytics | Phase 5 |
| Active usage | authenticated DAU | >1000 in 30d | product telemetry post-GA | Phase 5 |
| Session quality | average session duration | >30 min | refresh event analytics | Phase 5 |
| Recovery quality | reset completion; failed login rate | >80%; <5% | auth event analysis + reset funnel | Phase 5 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| Phase 1 | 2 weeks | Week 1 | Week 2 | M1 Security/data baseline |
| Phase 2 | 3 weeks | Week 3 | Week 5 | M2 Core backend auth contracts |
| Phase 3 | 3 weeks | Week 6 | Week 8 | M3 Password reset and frontend UX |
| Phase 4 | 2 weeks | Week 9 | Week 10 | M4 Admin/compliance hardening |
| Phase 5 | 2 weeks | Week 11 | Week 12 | M5 Alpha, beta, and GA rollout |

**Total estimated duration:** 12 weeks

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | Should API key auth be added for service-to-service calls? | scope expansion and contract divergence | Phase 5 | test-lead |
| 2 | What is the maximum allowed UserProfile.roles length? | schema and token-size assumptions | Phase 5 | auth-team |
| 3 | Should reset emails send synchronously or asynchronously? | reset UX latency and queue design | Phase 3 | engineering |
| 4 | How many refresh tokens are allowed per user across devices? | Redis keying and revocation semantics | Phase 1 | product |
| 5 | Is 5 failed attempts in 15 minutes the final lockout policy? | security UX and support burden | Phase 2 | security |
| 6 | Should remember-me extend session duration in v1.0? | AuthProvider/session policy | Phase 5 | product |
| 7 | Does v1.0 require admin audit search and unlock, or only visibility? | Jordan persona completeness | Phase 4 | product + security |
| 8 | Confirm PRD retention supersedes TDD retention. | compliance evidence and storage sizing | Phase 1 | compliance |
| 9 | Are multi-device sessions unlimited, bounded, or user-managed? | refresh token cap and logout semantics | Phase 1 | product |
| 10 | Must password reset invalidate all sessions or only current device? | session revocation breadth | Phase 3 | security |
| 11 | Should logout be treated as explicit v1.0 scope despite TDD omission? | PRD/TDD fidelity and UX completeness | Phase 3 | product + engineering |
