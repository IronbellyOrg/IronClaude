---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
debate_rounds: 0
generated: "2026-04-16"
generator: "single"
total_phases: 5
total_task_rows: 93
risk_count: 6
open_questions: 10
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap delivers a security-first authentication platform that unblocks Q2 personalization, closes the SOC2 audit gap, and preserves headroom for future OAuth2/MFA without reworking the v1 contract. The core architectural shape is a single `AuthService` facade over password verification, token lifecycle, user persistence, consent capture, reset token handling, and audit emission.

**Business Impact:** Unblocks approximately $2.4M in personalization-dependent annual revenue, supports Q3 2026 SOC2 readiness, and reduces support load through self-service registration and password recovery.

**Complexity:** MEDIUM (0.65) — driven by security-critical auth flows, PostgreSQL + Redis coordination, compliance logging, and phased rollout controls rather than algorithmic novelty.

**Critical path:** RS256 keying and bcrypt baseline -> user/token/audit contracts -> orchestration and REST APIs -> frontend session wiring -> performance/compliance validation -> gated rollout and rollback readiness.

**Key architectural decisions:**

- Keep `AuthService` as the only orchestration facade; avoid controller- or page-level auth logic.
- Use stateless access tokens plus server-managed refresh state to support revocation, logout, and password-reset invalidation.
- Accept PRD gap fills now (`logout`, admin auth log access, consent capture) and update the TDD in parallel rather than deferring required scope.

**Open risks requiring resolution before Phase 1:**

- Audit retention, consent storage design, and logout semantics must be fixed early because they alter schema, API, and rollout behavior.

## Phased Implementation Plan with Milestones

**Phase 1** | Security and data-plane foundation approved | 2 weeks | Keys, schemas, consent, audit, reset, lockout, and edge controls validated

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-SEC-002 | Enforce RS256 token signing | Sec | — | alg:RS256; key:RSA2048; verify:strict; config:test-pass | M | P0 |
| 2 | NFR-SEC-001 | Standardize bcrypt cost 12 | Sec | — | algo:bcrypt; cost:12; verify:test-pass; downgrade:none | S | P0 |
| 3 | NFR-COMP-001 | Capture GDPR consent at signup | Sec | DM-004,API-002 | consent:req; timestamp:stored; audit:present; register:no-consent→400 | M | P0 |
| 4 | NFR-COMP-002 | Retain audit logs 12 months | Ops | DM-003,COMP-013 | fields:userId|timestamp|ip|outcome; retain:12mo; policy:validated | M | P0 |
| 5 | NFR-COMP-003 | Block raw password persistence | Sec | COMP-004,COMP-013 | rawPwd:neverStored; rawPwd:neverLogged; review:pass; sinks:all-checked | M | P0 |
| 6 | NFR-COMP-004 | Audit data minimization scope | Sec | DM-001,DM-004 | pii:email|displayName|min; roles:justified; timestamps:justified; review:pass | M | P1 |
| 7 | DM-001 | Define UserProfile schema | DB | — | id:uuidv4-pk; email:unique+lower+idx; displayName:2-100; createdAt:iso+defaultNow; updatedAt:iso+auto; lastLoginAt:iso|null; roles:str[]+default[user] | M | P0 |
| 8 | DM-002 | Define AuthToken contract | Sec | COMP-003 | accessToken:jwt-rs256; refreshToken:opaque+unique+hashed; expiresIn:900; tokenType:Bearer | S | P0 |
| 9 | DM-003 | Define AuditLog schema | DB | — | userId:uuid-refUser; eventType:str; timestamp:iso; ipAddress:str; outcome:str; retain:12mo | M | P0 |
| 10 | DM-004 | Define ConsentRecord schema | DB | — | userId:uuid-refUser; consentType:str; consentGrantedAt:iso; policyVersion:str; sourceIp:str | M | P0 |
| 11 | DM-005 | Define PasswordResetToken schema | DB | — | tokenHash:str+unique; userId:uuid-refUser; issuedAt:iso; expiresAt:iso; usedAt:iso|null | M | P0 |
| 12 | DM-006 | Define AuthSecurityState schema | DB | — | userId:uuid-pk; failedAttempts:int; firstFailedAt:iso|null; lockedUntil:iso|null; passwordChangedAt:iso|null; refreshVersion:int+default0 | M | P0 |
| 13 | COMP-003 | Build JwtService module | Sec | NFR-SEC-002,DM-002 | type:backendModule; location:withinTokenManager; desc:jwtSignVerify; alg:RS256; key:RSA2048; skew:5s; dep:quarterlyRotatedKeys; implements:NFR-SEC-002 | L | P0 |
| 14 | COMP-004 | Build PasswordHasher module | Sec | NFR-SEC-001 | type:backendModule; location:withinAuthBoundary; desc:bcryptAbstraction; alg:bcrypt; cost:12; configurable:true; dep:bcryptjs; migReady:true; implements:NFR-SEC-001 | M | P0 |
| 15 | COMP-005 | Build UserRepo layer | DB | DM-001 | type:dataAccess; location:withinAuthBoundary; desc:userProfilePersistence; store:Postgres15+; ops:userProfileCRUD; pool:pg-pool; deps:Postgres15+|pg-pool | L | P0 |
| 16 | COMP-010 | Build ConsentRecorder module | Sec | DM-004,NFR-COMP-001 | type:backendModule; location:withinAuthBoundary; fields:userId|consentType|consentGrantedAt|policyVersion|sourceIp; write:DM-004; trigger:register | M | P0 |
| 17 | COMP-011 | Build ResetTokenStore module | Sec | DM-005 | type:backendModule; location:withinAuthBoundary; fields:tokenHash|userId|issuedAt|expiresAt|usedAt; store:ttl-backed; dep:DB/Redis; reuse:none | M | P0 |
| 18 | COMP-012 | Build LockoutPolicy module | Sec | DM-006 | type:backendModule; location:withinAuthBoundary; window:15m; threshold:5; response:423; reset:on-success; dep:AuthSecurityState | M | P0 |
| 19 | COMP-013 | Build AuditLogger module | Ops | DM-003,NFR-COMP-002 | type:backendModule; location:withinAuthBoundary; fields:userId|eventType|timestamp|ipAddress|outcome; retain:12mo; sink:Postgres+otel | L | P0 |
| 20 | COMP-017 | Build rate-limit middleware | Gate | — | type:middleware; location:apiEdge; rules:login10/m/ip|register5/m/ip|refresh30/m/user|me60/m/user; action:429 | M | P0 |
| 21 | COMP-016 | Build auth health endpoint | Ops | COMP-003,COMP-005 | type:backendEndpoint; route:/health/auth; checks:postgres|redis|rsaKeys|sendgrid; slis:uptime|deps | M | P1 |

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| JwtService -> TokenManager | strategy | RS256 sign/verify + skew handling | 1 | API-001,API-004,API-007 |
| AuditLogger event sink | event binding | auth events -> Postgres + tracing | 1 | NFR-COMP-002,API-008,OPS-007 |
| ConsentRecorder register hook | callback | register success -> consent write | 1 | API-002,FR-AUTH-002 |
| LockoutPolicy login guard | middleware | pre-issue lockout check + fail counter | 1 | API-001,FR-AUTH-001 |
| HealthEndpoint probes | dependency chain | postgres/redis/keys/sendgrid checks | 1 | NFR-REL-001,OPS-001 |

**Phase 2** | Core backend auth flows feature-complete | 3 weeks | Login, registration, refresh, profile, reset, logout, and admin log APIs passing integration gates

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | FR-AUTH-001 | Implement email/password login | API | COMP-001,COMP-004,COMP-012,API-001 | valid→200+AuthToken; invalid→401; no-enum; 5fail/15m→423 | L | P0 |
| 2 | FR-AUTH-002 | Implement validated registration | API | COMP-001,COMP-004,COMP-005,COMP-010,API-002 | valid→201+UserProfile; dup→409; weakPwd→400; bcrypt:12 | L | P0 |
| 3 | FR-AUTH-003 | Implement token issue and refresh | API | COMP-002,COMP-003,API-004 | login→access15m+refresh7d; refresh→200+newPair; expired→401; revoked→401 | L | P0 |
| 4 | FR-AUTH-004 | Implement authenticated profile read | API | COMP-001,COMP-005,API-003 | validBearer→200+UserProfile; invalid→401; fields:id|email|displayName|createdAt|updatedAt|lastLoginAt|roles | M | P1 |
| 5 | FR-AUTH-005 | Implement password reset flow | API | COMP-001,COMP-004,COMP-011,API-005,API-006 | request:genericSuccess; confirm:pwdUpdated; ttl:1h; reuse:none | L | P0 |
| 6 | API-001 | Implement POST /auth/login | API | FR-AUTH-001,COMP-017 | req:email|password; 200:AuthToken; 401:invalid; 423:locked; 429:rateLimited | M | P0 |
| 7 | API-002 | Implement POST /auth/register | API | FR-AUTH-002,COMP-017,NFR-COMP-001 | req:email|password|displayName|consent; 201:UserProfile; 400:validation; 409:duplicate | M | P0 |
| 8 | API-003 | Implement GET /auth/me | API | FR-AUTH-004 | hdr:Bearer; 200:UserProfile; 401:missing|expired|invalid; limit:60/m/user | S | P1 |
| 9 | API-004 | Implement POST /auth/refresh | API | FR-AUTH-003,COMP-002 | req:refreshToken; 200:newAuthToken; oldRefresh:revoked; 401:expired|revoked | M | P0 |
| 10 | API-005 | Implement POST /auth/reset-request | API | FR-AUTH-005,COMP-011 | req:email; resp:genericSuccess; enum:none; email:queuedWithin60s | M | P1 |
| 11 | API-006 | Implement POST /auth/reset-confirm | API | FR-AUTH-005,COMP-011,COMP-004 | req:token|password; success:confirmed; expired→401/400; reused→401/400 | M | P1 |
| 12 | API-007 | Implement POST /auth/logout | API | COMP-002,COMP-001 | req:refreshToken|sessionCtx; success:204/200; refresh:revoked; redirectReady:true | M | P1 |
| 13 | API-008 | Implement GET /admin/auth-events | API | COMP-013,DM-003 | auth:adminOnly; query:userId|dateRange|eventType; resp:pageable; fields:userId|eventType|timestamp|ipAddress|outcome | M | P1 |
| 14 | COMP-001 | Build AuthService facade | API | COMP-002,COMP-004,COMP-005,COMP-010,COMP-011,COMP-012,COMP-013 | type:backendFacade; deps:TokenManager|PasswordHasher|UserRepo|SendGrid; flows:login|register|me|reset | XL | P0 |
| 15 | COMP-002 | Build TokenManager lifecycle | Sec | COMP-003,DM-002,DM-006 | type:backendModule; issue:true; validate:true; refresh:true; revoke:true; store:Redis | XL | P0 |
| 16 | TEST-001 | Verify valid login token issue | Test | FR-AUTH-001,COMP-001 | level:unit; input:validCreds; expect:AuthToken; mocks:verify+issue; result:pass | S | P0 |
| 17 | TEST-002 | Verify invalid login rejection | Test | FR-AUTH-001,COMP-001 | level:unit; input:wrongPwd; expect:401; mocks:verifyFalse; result:pass | S | P0 |
| 18 | TEST-003 | Verify refresh token rotation | Test | FR-AUTH-003,COMP-002 | level:unit; input:validRefresh; expect:newPair; old:revoked; mocks:redisValid | S | P0 |
| 19 | TEST-004 | Verify registration persistence | Test | FR-AUTH-002,COMP-001,COMP-005 | level:integration; scope:AuthService+Postgres; input:validRegister; expect:userPersisted+pwdHashed | M | P0 |
| 20 | TEST-005 | Verify expired refresh rejected | Test | FR-AUTH-003,COMP-002 | level:integration; scope:TokenManager+Redis; input:expiredRefresh; expect:401 | M | P0 |
| 21 | TEST-007 | Verify logout revokes refresh | Test | API-007,COMP-002 | level:integration; scope:logout+Redis; input:validRefresh; expect:revoked+reuse401 | M | P1 |
| 22 | TEST-008 | Verify admin event log access | Test | API-008,COMP-013 | level:integration; scope:adminAPI+Postgres; auth:adminOnly; filters:userId|dateRange; resp:pageable | M | P1 |

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthService facade dispatch | dispatch table | login/register/me/reset/logout orchestration | 2 | API-001,API-002,API-003,API-005,API-006,API-007 |
| TokenManager revocation registry | registry | refresh hash -> user/session/version mapping | 2 | API-004,API-007,FR-AUTH-003 |
| ResetTokenStore confirm callback | callback | token validate -> password update -> token consume | 2 | API-006,FR-AUTH-005 |
| Admin audit query binding | route binding | admin endpoint -> AuditLogger store filters | 2 | API-008,Jordan persona |
| Rate-limit middleware chain | middleware chain | per-route limits + lockout + auth errors | 2 | API-001,API-002,API-004 |

**Phase 3** | Frontend journey and session UX validated | 2 weeks | User flows complete across signup, login, refresh, profile, reset, logout, and route protection

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-006 | Build LoginPage route | FE | API-001,COMP-009 | type:page; route:/login; auth:none; props:onSuccess|redirectUrl?; submit:API-001; tokenStore:AuthProvider | L | P0 |
| 2 | COMP-007 | Build RegisterPage route | FE | API-002,COMP-009 | type:page; route:/register; auth:none; props:onSuccess|termsUrl; fields:email|password|displayName|consent; clientPwdCheck:true | L | P0 |
| 3 | COMP-008 | Build ProfilePage route | FE | API-003,COMP-009 | type:page; route:/profile; auth:required; source:/auth/me; fields:displayName|email|createdAt | M | P1 |
| 4 | COMP-009 | Build AuthProvider context | FE | API-004,API-007 | type:reactContext; scope:appRoot; props:children; state:AuthToken|UserProfile; 401→refresh; unauth→loginRedirect | XL | P0 |
| 5 | COMP-014 | Build LogoutControl component | FE | API-007,COMP-009 | type:frontendComponent; location:appShell; action:logout; session:endImmediate; redirect:landing | M | P1 |
| 6 | COMP-015 | Build AdminAuthEventsPage | FE | API-008,COMP-009 | type:frontendPage; route:/admin/auth-events; auth:admin; filters:userId|dateRange|eventType; table:userId|eventType|timestamp|ipAddress|outcome | L | P1 |
| 7 | FR-AUTH-006 | Implement user logout journey | FE | API-007,COMP-014,COMP-009 | clickLogout→sessionEnded; refresh:revoked; redirect:landing; sharedDevice:secure | M | P1 |
| 8 | FR-AUTH-007 | Implement admin auth log view | FE | API-008,COMP-015 | admin→viewLogs; filters:dateRange|user; data:queryable; auditorUse:true | M | P1 |
| 9 | TEST-006 | Verify register-login-profile journey | Test | COMP-006,COMP-007,COMP-008,COMP-009 | level:e2e; flow:Register→Login→Profile; expect:accountCreated+login+profileShown | L | P0 |
| 10 | TEST-009 | Verify password reset journey | Test | API-005,API-006,COMP-006 | level:e2e; flow:ForgotPwd→Email→Reset→Login; ttl:1h; reuse:none | L | P1 |
| 11 | TEST-010 | Verify silent refresh behavior | Test | COMP-009,API-004 | level:e2e; accessExpired→refresh; user:staysSignedIn; refreshExpired→loginPrompt | L | P1 |
| 12 | TEST-011 | Verify logout journey | Test | FR-AUTH-006,COMP-014 | level:e2e; action:logout; expect:landingRedirect; protectedRoute→login; refreshReuse→401 | M | P1 |
| 13 | TEST-012 | Verify admin log viewer | Test | FR-AUTH-007,COMP-015 | level:e2e; adminOnly:true; filters:work; rows:correct; nonAdmin→403/redirect | M | P1 |

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| AuthProvider refresh interceptor | middleware chain | 401 -> refresh -> retry/redirect | 3 | LoginPage,ProfilePage,AdminAuthEventsPage |
| Route protection registry | registry | public/protected/admin route guards | 3 | App router,ProfilePage,AdminAuthEventsPage |
| LogoutControl event binding | event binding | click -> API-007 -> state clear -> redirect | 3 | FR-AUTH-006 |
| RegisterPage validation bindings | callback | inline password/consent validation before submit | 3 | API-002,SC-006 |
| Admin log filter state wiring | state binding | date/user/event filters -> API query params | 3 | API-008,Jordan persona |

**Phase 4** | Performance, compliance, and operations hardened | 2 weeks | SLOs, auditability, capacity, and incident readiness proven under load

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-PERF-001 | Validate auth p95 under 200ms | Ops | API-001,API-002,API-003,API-004 | p95:<200ms; apm:enabled; scope:allAuthEndpoints; regressions:none | L | P0 |
| 2 | NFR-PERF-002 | Validate 500 concurrent logins | Ops | API-001,OPS-004,OPS-005 | conc:500; errors:acceptable; k6:test-pass; saturation:measured | L | P0 |
| 3 | NFR-REL-001 | Validate 99.9% availability path | Ops | COMP-016,OPS-001,OPS-002 | uptime:99.9%; monitor:30dRolling; health:endpoint; paging:live | M | P0 |
| 4 | MIG-004 | Gate new login with feature flag | Gate | API-001,COMP-006 | flag:AUTH_NEW_LOGIN; default:off; scope:loginPage+loginAPI; removable:true | S | P0 |
| 5 | MIG-005 | Gate refresh flow with feature flag | Gate | API-004,COMP-009 | flag:AUTH_TOKEN_REFRESH; default:off; whenOff:accessOnly; removal:phase3+2w | S | P1 |
| 6 | OPS-001 | Author AuthService down runbook | Ops | COMP-016,COMP-005,COMP-002 | symptoms:5xx; diagnosis:k8s|postgres|initLogs; resolution:restart|failover|relogin; escalate:15m | M | P1 |
| 7 | OPS-002 | Author refresh failure runbook | Ops | COMP-002,COMP-003,MIG-005 | symptoms:logoutLoop; diagnosis:redis|keys|flag; resolution:scale|remount|enableFlag; escalate:set | M | P1 |
| 8 | OPS-003 | Stand up on-call process | Ops | OPS-001,OPS-002 | p1Ack:15m; coverage:24x7+2wPostGA; path:auth→lead→mgr→platform; tools:listed | M | P1 |
| 9 | OPS-004 | Set AuthService pod scaling | Ops | NFR-PERF-002 | replicas:3; hpa:max10; trigger:cpu>70; load:500Concurrent | M | P1 |
| 10 | OPS-005 | Set PostgreSQL pool scaling | Ops | COMP-005,NFR-PERF-002 | pool:100; expectedQ:50; scaleTo:200@wait>50ms; monitor:on | M | P1 |
| 11 | OPS-006 | Set Redis memory scaling | Ops | COMP-002,NFR-PERF-002 | mem:1GB; expected:100Ktokens~50MB; scaleTo:2GB@>70% | M | P1 |
| 12 | OPS-007 | Alert on login failure spikes | Ops | COMP-013 | metric:auth_login_total; threshold:20%/5m; action:OPS-001; source:prom | S | P1 |
| 13 | OPS-008 | Alert on auth latency spikes | Ops | NFR-PERF-001 | metric:auth_login_duration_seconds; threshold:p95>500ms; source:prom; action:checkPods+db | S | P1 |
| 14 | OPS-009 | Alert on Redis failures | Ops | COMP-002 | metric:redisConnFailures; threshold:sustainedAny; source:structuredLogs; action:OPS-002 | S | P1 |
| 15 | TEST-013 | Verify consent auditability | Test | NFR-COMP-001,DM-004 | level:integration; consent:recorded; timestamp:present; policyVersion:present; noConsent→400 | M | P1 |
| 16 | TEST-014 | Verify SOC2 log retention policy | Test | NFR-COMP-002,DM-003 | level:integration; retain:12mo; fields:userId|timestamp|ip|outcome; policy:pass | M | P1 |
| 17 | TEST-015 | Verify raw password never logged | Test | NFR-COMP-003,COMP-013 | level:securityReview; sinks:app|audit|trace; rawPwd:none; review:pass | M | P0 |
| 18 | TEST-016 | Verify load and failover readiness | Test | NFR-REL-001,OPS-001,OPS-002 | level:resilience; depLoss:simulated; health:degradesCorrectly; runbooks:actionable | L | P1 |

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Feature flag gate registry | registry | AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH toggles | 4 | MIG-001,MIG-002,MIG-003 |
| Prometheus metric bindings | event binding | counters/histograms wired from auth flows | 4 | OPS-007,OPS-008,SC-001,SC-003 |
| OpenTelemetry trace chain | trace wiring | AuthService -> PasswordHasher -> TokenManager -> JwtService | 4 | NFR-PERF-001,OPS-001 |
| Alertmanager routing | callback chain | auth alerts -> on-call escalation path | 4 | OPS-003,OPS-007,OPS-008,OPS-009 |
| Health probe wiring | middleware/probe | k8s liveness/readiness -> auth health endpoint | 4 | NFR-REL-001,OPS-001 |

**Phase 5** | Controlled rollout to GA completed | 4 weeks | Alpha, beta, GA, rollback, and post-launch metrics closed with no critical regressions

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | MIG-001 | Run internal alpha rollout | Gate | MIG-004,OPS-003,TEST-006,TEST-016 | env:staging; users:auth-team+QA; flag:AUTH_NEW_LOGIN; success:allFRManualPass+0P0/P1 | L | P0 |
| 2 | MIG-002 | Run 10 percent beta rollout | Gate | MIG-001,NFR-PERF-001,NFR-PERF-002 | traffic:10%; p95:<200ms; errRate:<0.1%; redisFailures:none | XL | P0 |
| 3 | MIG-003 | Run GA rollout and cutover | Gate | MIG-002,MIG-005 | traffic:100%; dashboards:green; uptime:99.9%@7d; legacy:deprecated | XL | P0 |
| 4 | MIG-006 | Disable flag for rollback | Gate | MIG-004 | action:AUTH_NEW_LOGIN=off; route:legacy; time:immediate | S | P0 |
| 5 | MIG-007 | Verify legacy after rollback | Gate | MIG-006 | smoke:pass; login:works; userImpact:bounded | S | P0 |
| 6 | MIG-008 | Investigate rollback root cause | Ops | MIG-006,COMP-013 | inputs:logs+traces; cause:identified; evidence:captured | M | P1 |
| 7 | MIG-009 | Restore corrupted auth data | DB | MIG-006,DM-001 | backup:lastKnownGood; restore:selective; verify:userProfileIntegrity | L | P1 |
| 8 | MIG-010 | Notify response teams | Ops | MIG-006 | notify:auth+platform; channel:incident; status:shared | S | P1 |
| 9 | MIG-011 | Complete rollback postmortem | Ops | MIG-008,MIG-009,MIG-010 | deadline:48h; cause:documented; actions:assigned | M | P1 |
| 10 | SC-001 | Validate login latency success metric | Gate | NFR-PERF-001 | metric:loginP95; target:<200ms; source:APM; phase:beta+GA | S | P0 |
| 11 | SC-002 | Validate registration success rate | Gate | API-002,COMP-007 | metric:registrationSuccess; target:>99%; source:funnelRatio; phase:GA | S | P1 |
| 12 | SC-003 | Validate refresh latency metric | Gate | API-004,COMP-009 | metric:refreshP95; target:<100ms; source:APM; phase:beta+GA | S | P1 |
| 13 | SC-004 | Validate uptime success metric | Gate | NFR-REL-001 | metric:uptime; target:99.9%; source:healthMonitoring; phase:GA | S | P0 |
| 14 | SC-005 | Validate password hash timing | Gate | COMP-004 | metric:hashTime; target:<500ms; source:benchmark; phase:preGA | S | P1 |
| 15 | SC-006 | Validate registration conversion | Gate | COMP-007,TEST-006 | metric:registerConversion; target:>60%; source:funnelAnalytics; phase:GA | S | P1 |
| 16 | SC-007 | Validate authenticated DAU growth | Gate | API-001,API-004 | metric:DAU; target:>1000@30d; source:tokenIssueCounts; phase:postGA | S | P2 |
| 17 | SC-008 | Validate session duration metric | Gate | COMP-009,API-004 | metric:avgSession; target:>30m; source:refreshAnalytics; phase:GA | S | P1 |
| 18 | SC-009 | Validate failed login rate | Gate | COMP-013,API-001 | metric:failedLoginRate; target:<5%; source:authEventLogs; phase:GA | S | P1 |
| 19 | SC-010 | Validate reset completion rate | Gate | API-005,API-006 | metric:resetCompletion; target:>80%; source:resetFunnel; phase:GA | S | P1 |

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Rollout flag controller | control plane | staged traffic + auth feature toggles | 5 | MIG-001,MIG-002,MIG-003 |
| Rollback procedure chain | runbook chain | disable -> verify -> investigate -> restore -> notify -> postmortem | 5 | MIG-006..MIG-011 |
| Success metric dashboard wiring | dashboard binding | SC metrics mapped to prod telemetry | 5 | product,auth-team,platform-team |
| Incident channel notification hook | callback | rollback trigger -> team notification | 5 | MIG-010,OPS-003 |
| Legacy cutover route mapping | routing binding | new/legacy auth path selection by flag state | 5 | MIG-001,MIG-002,MIG-003,MIG-006 |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | Token theft via XSS hijacks sessions | High | Medium | Session compromise, user takeover | accessToken in memory; refresh token revocable; logout + password reset invalidate sessions; CSP review | security + frontend |
| 2 | Brute-force login attempts bypass UX | Medium | High | Account compromise, service abuse | rate limits, lockout module, WAF escalation, generic errors | security + backend |
| 3 | Migration rollback loses user data | High | Low | Auth outage, trust loss | backups before each phase, idempotent writes, selective restore path | platform + backend |
| 4 | Signup UX depresses conversion | High | Medium | Revenue delay, roadmap slip | minimize form fields, inline validation, funnel monitoring, usability test before beta | product + frontend |
| 5 | Audit trail misses required fields | High | Medium | SOC2 failure, incident blind spots | audit schema first, admin query path, retention validation, pre-GA compliance gate | compliance + backend |
| 6 | Email delivery blocks recovery | Medium | Low | Support burden, lockout frustration | async delivery, SendGrid monitoring, fallback recovery channel, reset funnel alerting | platform + support |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ | 1 | Required | stop rollout; no safe fallback |
| Redis 7+ | 1 | Required | disable refresh flag; force re-login on expiry |
| Node.js 20 LTS | 1 | Required | no fallback |
| bcryptjs | 1 | Required | approved equivalent only after security review |
| jsonwebtoken | 1 | Required | approved JOSE library only after contract revalidation |
| SendGrid API | 2 | Required | support-assisted reset path |
| Frontend routing framework | 3 | Required | hold FE rollout; API can still alpha |
| SEC-POLICY-001 | 1 | Required | freeze security-sensitive implementation |

### Infrastructure Requirements

- PostgreSQL 15+ with schema migration path for user, audit, consent, reset, and security-state tables.
- Redis 7+ with persistence and memory headroom for token revocation and session invalidation.
- Secret management for quarterly-rotated RSA key pairs and SendGrid credentials.
- Kubernetes HPA, readiness/liveness probes, Prometheus, Grafana, and OpenTelemetry.
- Staging and CI environments with testcontainers or equivalent ephemeral PostgreSQL/Redis.

### Team Requirements

1. Backend/auth team for service, API, data, and security-state implementation.
2. Frontend team for session provider, routes, logout UX, and admin log UI.
3. Platform team for infra scaling, observability, secrets, and rollout controls.
4. Compliance/security reviewers for consent, retention, and password handling sign-off.
5. QA for E2E coverage and alpha/beta validation.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| Login speed | SC-001 | < 200ms p95 | APM on login path under beta and GA traffic | 5 |
| Registration reliability | SC-002 | > 99% | registration success funnel vs attempts | 5 |
| Refresh speed | SC-003 | < 100ms p95 | APM on refresh exchange path | 5 |
| Availability | SC-004 | 99.9% | health endpoint + uptime monitoring | 4-5 |
| Hash performance | SC-005 | < 500ms | benchmark bcrypt cost 12 in prod-like env | 4-5 |
| Signup conversion | SC-006 | > 60% | landing -> register -> confirmed funnel | 5 |
| Authenticated adoption | SC-007 | > 1000 DAU in 30d | token issuance analytics | 5 |
| Session depth | SC-008 | > 30 min | refresh event analytics | 5 |
| Login failure ratio | SC-009 | < 5% | auth event log analysis | 5 |
| Reset completion | SC-010 | > 80% | reset request -> completion funnel | 5 |

## Timeline Estimates per Phase

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| 1 | 2 weeks | Week 1 | Week 2 | keys approved; schemas frozen; consent/audit/lockout/reset stores ready |
| 2 | 3 weeks | Week 3 | Week 5 | core APIs pass unit+integration; logout/admin gaps closed |
| 3 | 2 weeks | Week 6 | Week 7 | FE journeys pass E2E; session UX validated |
| 4 | 2 weeks | Week 8 | Week 9 | load, compliance, alerts, runbooks, and capacity tuned |
| 5 | 4 weeks | Week 10 | Week 13 | alpha, beta, GA, and post-launch metric verification |

**Total estimated duration:** 13 weeks

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| 1 | Should service-to-service API key auth be deferred to a separate auth surface? | Medium; affects future interface shape only | 2 | product + backend |
| 2 | What is max allowed length of `roles[]`? | Medium; affects schema bounds and JWT size | 1 | auth-team |
| 3 | Audit retention conflict resolved to 12 months in roadmap; should TDD be updated formally? | High; schema and ops policy mismatch otherwise | 1 | auth-team + compliance |
| 4 | Logout is PRD-required and added here as API-007/FR-AUTH-006; should TDD adopt server-side revocation semantics? | High; affects session invalidation and FE wiring | 2 | auth-team |
| 5 | Admin auth log access is PRD-required and added here as API-008/FR-AUTH-007; is it in v1 scope? | High; Jordan persona and SOC2 visibility depend on it | 2 | product + compliance |
| 6 | Should reset emails be synchronous or asynchronous? | Medium; impacts API latency and queue design | 2 | engineering |
| 7 | How many concurrent refresh sessions per user are allowed? | Medium; affects TokenManager registry design | 2 | product |
| 8 | Should remember-me extend beyond 7 days? | Medium; changes token TTL, UX, and compliance review | 3 | product |
| 9 | How should consent be surfaced in UI and persisted in policy-version terms? | High; legal compliance gate | 1 | compliance + frontend |
| 10 | Are `roles` and timestamps compliant under GDPR minimization, or must they be justified in policy? | High; may alter schema and audit narratives | 1 | compliance |

1. PRD gap fills included in this roadmap: `API-007`, `API-008`, `FR-AUTH-006`, `FR-AUTH-007`, `DM-004`, `DM-005`, `DM-006`, `COMP-010` through `COMP-017`, and `TEST-007` through `TEST-016`.
2. These additions are required to satisfy stated PRD scope, Jordan admin needs, consent obligations, logout semantics, and end-to-end operability.
3. TDD should be updated to absorb these additions before implementation lock.
