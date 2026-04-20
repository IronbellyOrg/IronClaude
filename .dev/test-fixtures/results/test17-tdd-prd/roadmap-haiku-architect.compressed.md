<!-- CONV: AuthService=THS, AuthController=THC, TokenManager=TKN, registration=RGS, Implement=MPL, validation=VLD, password=PSS, implementation=IM1, PasswordHasher=PA1, Registration=RE1, FR-AUTH-005=FA0, integration=NTG, contract=CNT, AuthProvider=THP, compliance=CMP, PostgreSQL=PST, endpoint=NDP, retention=RTN, sessions=SSS, NFR-COMPLIANCE-002=NC0 -->
---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.65
complexity_class: MEDIUM
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: 0.0
debate_rounds: 0
generated: "2026-04-18"
generator: "single"
total_milestones: 5
total_task_rows: 95
risk_count: 7
open_questions: 8
domain_distribution:
  frontend: 18
  backend: 36
  security: 20
  performance: 10
  documentation: 16
consulting_personas: [architect, backend, security, frontend, qa, devops]
milestone_count: 5
milestone_index:
  - id: M1
    title: "Core Security and Data Foundations"
    type: SECURITY
    priority: P0
    dependencies: []
    deliverable_count: 24
    risk_level: High
  - id: M2
    title: "RE1 and Login Experience"
    type: FEATURE
    priority: P0
    dependencies: [M1]
    deliverable_count: 15
    risk_level: High
  - id: M3
    title: "Session Lifecycle and Protected Access"
    type: FEATURE
    priority: P0
    dependencies: [M1, M2]
    deliverable_count: 20
    risk_level: High
  - id: M4
    title: "Password Reset, Audit, and Admin Visibility"
    type: FEATURE
    priority: P0
    dependencies: [M1, M3]
    deliverable_count: 19
    risk_level: High
  - id: M5
    title: "Rollout, Reliability, and GA Operations"
    type: MIGRATION
    priority: P1
    dependencies: [M2, M3, M4]
    deliverable_count: 17
    risk_level: Medium
total_deliverables: 95
total_risks: 7
estimated_milestones: 5
validation_score: 0.94
validation_status: PASS_WITH_WARNINGS
---

# User Authentication Service — Project Roadmap

## Executive Summary

This roadmap sequences the authentication program as a technical-layer rollout: establish cryptographic and data foundations first, ship RGS/login next to unlock business value early, then harden session management, PSS recovery, auditability, and staged production rollout. The plan preserves every extracted requirement and entity as an explicit deliverable while adding PRD-driven gap fills for logout and admin audit-log investigation so v1.0 satisfies both user and CMP outcomes.

**Business Impact:** Unlocks the Q2 2026 personalization roadmap, protects the projected $2.4M annual revenue tied to authenticated experiences, and closes the largest SOC2 audit blocker before Q3 2026.

**Complexity:** MEDIUM (0.65) — moderate functional surface, but elevated by RS256 key management, Redis-backed refresh-token revocation, staged rollout, GDPR/SOC2 obligations, and anti-abuse controls.

**Critical path:** M1 crypto/data/runtime baseline → M2 RGS/login → M3 token refresh/profile/logout → M4 PSS reset/audit/admin visibility → M5 staged rollout and SLO VLD.

**Key architectural decisions:**

- Use RS256 access tokens with opaque Redis-backed refresh tokens so revocation, rotation, and Sam’s programmatic refresh use case can coexist.
- Keep access tokens in memory and refresh tokens in HttpOnly transport to reduce XSS exposure while preserving silent refresh.
- Add an explicit admin audit-log query surface and UI because Jordan’s JTBD and SOC2 evidence requirements are not fully covered by the extracted FR set alone.

**Open risks requiring resolution before M1:**

- Lock in RSA key provisioning and quarterly rotation ownership before IM1 begins.
- Confirm whether API-key auth stays out of v1.0 so the auth boundary does not widen mid-foundation.

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Core Security and Data Foundations|SECURITY|P0|XL|—|24|High|
|M2|RE1 and Login Experience|FEATURE|P0|L|M1|15|High|
|M3|Session Lifecycle and Protected Access|FEATURE|P0|XL|M1,M2|20|High|
|M4|Password Reset, Audit, and Admin Visibility|FEATURE|P0|XL|M1,M3|19|High|
|M5|Rollout, Reliability, and GA Operations|MIGRATION|P1|L|M2,M3,M4|17|Medium|

## Dependency Graph

M1(core schemas, crypto, controllers, health) -> M2(RGS, login, consent)
M1(core schemas, crypto, controllers, health) -> M3(refresh, profile, logout, protected access)
M1(core schemas, crypto, controllers, health) -> M4(reset, audit, admin visibility)
M2(RGS, login, consent) -> M3(refresh, profile, logout, protected access)
M3(refresh, profile, logout, protected access) -> M4(reset, audit, admin visibility)
M2,M3,M4 -> M5(alpha, beta, GA, rollback, reliability)

## M1: Core Security and Data Foundations

**Objective:** Establish the runtime, schema, cryptographic, API-shell, and policy baseline that every auth flow depends on. | **Duration:** 3 weeks | **Entry:** PRD scope fixed to email/PSS v1.0; PST, Redis, and Node.js 20 environments available. | **Exit:** Core data contracts, token/signing services, audit schema, controller skeletons, and observability baseline are deployable in staging with policy conformance verified.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|UserProfile schema|Define PST schema and TypeScript CNT for the canonical user record used by RGS, login, and profile retrieval.|THS,PST|INFRA-DB-001|id:uuid-pk-notnull; email:unique-indexed-lowercase-notnull; displayName:2-100-notnull; createdAt:iso8601-default-now-notnull; updatedAt:iso8601-auto-updated-notnull; lastLoginAt:iso8601-nullable; roles:string[]-default-user-notnull|M|P0|
|2|DM-002|AuthToken CNT|Define token response CNT returned by login and refresh and align it with frontend and API consumers.|TKN,JwtService|NFR-SEC-002|accessToken:jwt-rs256-notnull; refreshToken:opaque-unique-notnull; expiresIn:number-900-notnull; tokenType:Bearer-notnull|S|P0|
|3|COMP-007|THS core module|Create the orchestration service that owns RGS, login, profile, and reset use cases and delegates hashing, tokening, and persistence.|THS|DM-001,DM-002|service boundaries documented; methods for register/login/me/reset flows defined; persistence/token/hash dependencies injected; no caller bypasses service boundary|M|P0|
|4|COMP-008|PA1 module|MPL dedicated PSS hashing and verification component using bcrypt cost 12 and no raw-PSS persistence.|PA1|NFR-SEC-001,SEC-POLICY-001|hash uses bcrypt-cost12; verify compares bcrypt hashes; raw passwords never persisted; raw passwords never logged|S|P0|
|5|COMP-009|JwtService module|MPL RS256 signing and verification component with 2048-bit RSA keys, 15-minute access-token TTL, and ±5-second clock skew tolerance.|JwtService|NFR-SEC-002,SEC-POLICY-001|signs-rs256; rsa-keysize-2048; access-ttl-900s; verify honors-5s-skew; key identifiers supported for rotation|M|P0|
|6|COMP-010|TKN module|MPL refresh-token issuance, hashing, storage, revocation, and rotation orchestration against Redis 7+.|TKN,Redis|DM-002,COMP-009|issues access+refresh pair; stores hashed refresh token in redis; ttl-7d; supports revoke+rotate; lookup by user/session metadata|M|P0|
|7|COMP-011|AuditLog repository|Create audit-log persistence component for CMP evidence and incident investigation support.|AuditLog,PST|NC0,INFRA-DB-001|stores userId; eventType; timestamp; ipAddress; outcome; RTN-configurable-to-12m; query paths support date+user filters|M|P0|
|8|COMP-012|ResetToken store|Create reset-token persistence and VLD component with one-hour TTL and single-use semantics.|ResetTokenStore,PST|FA0|token persisted hashed; ttl-1h; used flag enforced; lookup invalid after consume; user linkage preserved|M|P0|
|9|COMP-013|Consent recorder|Create RGS-consent component to capture GDPR consent state and timestamp at account creation.|ConsentRecorder,PST|NFR-COMPLIANCE-001,DM-001|consent-required-at-RGS; consentTimestamp-recorded; linked-to-userId; no extra-PII captured|S|P0|
|10|COMP-014|THC shell|Create REST controller shell for `/v1/auth/*` endpoints with unified error envelope and versioned routing.|THC|COMP-007|routes mounted under-v1-auth; errors use error.code+message+status; JSON-only responses; additive-field policy documented|M|P0|
|11|API-001|Login NDP CNT|Define and scaffold POST `/auth/login` request, response, and error semantics before business logic wiring.|THC|COMP-014,DM-002|method POST; path /v1/auth/login; auth none; request email+PSS; 200 returns AuthToken; 401 generic-invalid; 423 locked; 429 rate-limited|S|P0|
|12|API-002|Register NDP CNT|Define and scaffold POST `/auth/register` CNT for validated account creation.|THC|COMP-014,DM-001|method POST; path /v1/auth/register; auth none; request email+PSS+displayName; 201 returns UserProfile; 400 VLD; 409 duplicate|S|P0|
|13|API-003|Profile NDP CNT|Define and scaffold GET `/auth/me` CNT for authenticated profile retrieval.|THC|COMP-014,DM-001|method GET; path /v1/auth/me; auth bearer-accessToken; header Authorization:Bearer<JWT>; 200 returns id+email+displayName+createdAt+updatedAt+lastLoginAt+roles; 401 invalid-expired-missing|S|P0|
|14|API-004|Refresh NDP CNT|Define and scaffold POST `/auth/refresh` CNT for silent and programmatic refresh.|THC|COMP-014,DM-002|method POST; path /v1/auth/refresh; auth refreshToken-in-body; request refreshToken; 200 returns new AuthToken pair; old refresh revoked; 401 expired-or-revoked|S|P0|
|15|API-005|Reset-request NDP CNT|Define and scaffold POST `/auth/reset-request` anti-enumeration CNT.|THC|COMP-014|method POST; path /v1/auth/reset-request; auth none; request email; 200 regardless-of-RGS; side-effect reset email token with-1h-ttl|S|P0|
|16|API-006|Reset-confirm NDP CNT|Define and scaffold POST `/auth/reset-confirm` CNT with session invalidation behavior.|THC|COMP-014,COMP-012|method POST; path /v1/auth/reset-confirm; auth none; request token+newPassword; updates PSS hash; invalidates all SSS; 400 expired-used-token; 400 weak-PSS|S|P0|
|17|API-007|Logout NDP gap fill|Add explicit logout NDP required by the PRD user story so shared-device session termination is first-class.|THC,TKN|COMP-014,OQ-PRD-002|method POST; path /v1/auth/logout; auth bearer-or-refresh context; revokes current session immediately; returns clear success code; redirects supported by frontend flow|S|P0|
|18|API-008|Admin audit query NDP gap fill|Add admin audit-log query API to satisfy Jordan’s PRD JTBD and SOC2 investigation workflow.|AuditController,AuditLog|COMP-011|method GET; path /v1/auth/audit-events; auth admin-only; filters userId+dateRange+outcome; paginated JSON; auditable access to audit logs|M|P1|
|19|NFR-SEC-001|Password hashing policy enforcement|Validate bcrypt cost-factor and hashing policy as a release-blocking platform capability.|PA1|COMP-008|bcrypt cost factor 12 enforced; unit assertion covers configured cost; no plain-text persistence; no plain-text logging|S|P0|
|20|NFR-SEC-002|Token signing policy enforcement|Validate JWT signing configuration meets RS256 and RSA key-size requirements with rotation support.|JwtService|COMP-009|rs256-only; rsa2048-minimum; config VLD test exists; quarterly rotation path defined; invalid config fails fast|S|P0|
|21|NC0|Audit logging foundation|Define compliant audit-event schema, RTN policy, and event taxonomy before feature flows emit logs.|AuditLog|COMP-011|captures userId+timestamp+ipAddress+outcome; auth event taxonomy defined; RTN configurable to-12-months; SOC2 evidence queries supported|M|P0|
|22|NFR-COMPLIANCE-003|Password-storage CMP|Map NIST SP 800-63B storage requirements directly into IM1 and VLD controls.|PA1|NFR-SEC-001|adaptive one-way hashing only; raw passwords never persisted; raw passwords never logged; CMP mapping documented in tests|S|P0|
|23|NFR-COMPLIANCE-004|Data-minimization boundary|Enforce collection boundary so auth data stores only email, hashed PSS, display name, and required operational metadata.|THS,PST|DM-001,NFR-COMPLIANCE-001|collects email+hashedPassword+displayName only; no additional PII fields added; audit data separate from profile; schema review completed|S|P0|
|24|OPS-010|Tracing baseline|Establish OpenTelemetry trace propagation across auth components before business flows are load-tested.|THS,PA1,TKN,JwtService|COMP-007,COMP-008,COMP-009,COMP-010|traces span THS->PA1->TKN->JwtService; correlation ids propagate; staging export works; missing sampling policy flagged|M|P1|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|THS -> PA1|dependency injection|Constructor injection with verify/hash interface|M1|FR-AUTH-001,FR-AUTH-002,FA0|
|THS -> TKN|dependency injection|Constructor injection with issue/refresh/revoke interface|M1|FR-AUTH-001,FR-AUTH-003,API-007|
|TKN -> JwtService|service call|issueTokens/refreshTokens invoke sign+verify|M1|API-001,API-004|
|THC route registry|dispatch table|`/v1/auth/*` mapped to handlers in versioned router|M1|API-001,API-002,API-003,API-004,API-005,API-006,API-007|
|Audit event emitter -> AuditLog repository|event binding|auth events emit structured records to repository|M1|NC0,API-008|
|Auth middleware -> trace context|middleware chain|request context injects trace/span ids before handler execution|M1|NFR-PERF-001,OPS-010|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS|High|Medium|Session compromise and unauthorized access|Keep access tokens in memory, use HttpOnly refresh transport, limit access TTL to 15 minutes, and support fast revocation.|security|
|2|R-002 Brute-force on login|High|Medium|Credential stuffing, account lockouts, and operational noise|Define gateway rate limits, enforce lockout state, and validate bcrypt cost and anti-enumeration behavior in M1.|security|
|3|R-PRD-003 Compliance failure from incomplete audit logging|High|Medium|SOC2 evidence gap and release delay|Lock schema, required fields, and RTN direction in M1 before downstream feature work proceeds.|CMP|

### Milestone Dependencies — M1

- PST 15+, Redis 7+, Node.js 20 LTS, SEC-POLICY-001, and SendGrid NTG design must be available before exiting M1.
- API-key authentication is explicitly deferred unless OQ-001 is reopened and approved for v1.0.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-001|Should `THS` support API key authentication for service-to-service calls?|Changes the auth boundary, route contracts, and token model; defer keeps v1.0 scope stable.|test-lead|2026-04-15|
|2|OQ-002|Maximum allowed `UserProfile` roles array length?|Affects DM-001 VLD, storage sizing, and admin-query assumptions.|auth-team|2026-04-01|
|3|OQ-PRD-003|Should the 5-failures-in-15-min lockout policy remain fixed or be adjusted?|Changing threshold affects brute-force mitigation, UX, and alert tuning.|Security|2026-04-22|
|4|OQ-RET-001|Who owns the audit RTN decision between 90 days and 12 months?|Blocks final schema/index sizing and CMP evidence design; PRD intent currently wins.|Compliance + Engineering|2026-04-22|

## M2: RE1 and Login Experience

**Objective:** Deliver the first-user journey end to end so Alex can register and log in in under 60 seconds with strong VLD, anti-enumeration, and immediate business value. | **Duration:** 2 weeks | **Entry:** M1 controller, hashing, token, consent, and user schema foundations complete in staging. | **Exit:** RE1 and login flows work across API and frontend, consent is captured, duplicate/weak-PSS/lockout cases are enforced, and RGS funnel instrumentation is active.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|25|FR-AUTH-002|RE1 workflow|MPL validated user-RGS flow with email uniqueness, PSS strength, consent capture, and profile creation.|THS,THC|DM-001,COMP-008,COMP-013,API-002|201 returns UserProfile; duplicate email->409; weak PSS<8/no-uppercase/no-number->400; bcrypt hash cost12 stored; consent required|M|P0|
|26|FR-AUTH-001|Login workflow|MPL credential authentication with anti-enumeration behavior and lockout tracking.|THS,THC|COMP-008,COMP-010,API-001|valid credentials->200+AuthToken; invalid credentials->401; nonexistent email->401 generic; account locked after5failures/15min|M|P0|
|27|NFR-COMPLIANCE-001|RE1 consent capture|Wire GDPR consent collection into RGS UI, API VLD, and persistence path.|RegisterPage,THS|FR-AUTH-002,COMP-013|consent checkbox required; consent timestamp recorded; RGS blocked without consent; audit event emitted|S|P0|
|28|COMP-001|LoginPage|Build `/login` page for email/PSS login, generic error messaging, and success redirect into the authenticated app.|LoginPage|API-001,COMP-004,COMP-005|route /login; props onSuccess+redirectUrl supported; calls API-001; generic invalid message; success stores AuthToken via THP|M|P0|
|29|COMP-002|RegisterPage|Build `/register` page with inline VLD, terms link, consent, and happy-path auto-login/redirect behavior.|RegisterPage|API-002,COMP-004,COMP-005,NFR-COMPLIANCE-001|route /register; props onSuccess+termsUrl supported; client-side PSS VLD; consent presented; success redirects within signup journey|M|P0|
|30|COMP-005|PublicRoutes|Wire unauthenticated route group to host RGS and login pages without auth enforcement.|PublicRoutes|COMP-001,COMP-002|includes LoginPage+RegisterPage; no auth required; route guards do not block access; unknown public auth paths handled cleanly|S|P1|
|31|COMP-015|RE1 validator|Create VLD module for email normalization, PSS policy, display-name constraints, and duplicate checks.|THS,RegisterPage|DM-001,FR-AUTH-002|email lowercased; displayName 2-100 chars; PSS policy enforced client+server; duplicate email checked before create|S|P0|
|32|COMP-016|Login lockout tracker|MPL failed-login counting and 15-minute lockout state management tied to account and abuse controls.|THS,Redis|FR-AUTH-001,R-002|tracks failed attempts; lockout after 5 in 15 min; successful login resets counter; 423 surfaced consistently|M|P0|
|33|COMP-017|Auth event emitter|Emit structured events for RGS and login outcomes into audit logs and metrics streams.|THS,AuditLog|COMP-011,OPS-007|RGS success/failure logged; login success/failure logged; includes userId-or-anonymous key, ip, timestamp, outcome|S|P0|
|34|COMP-018|RE1 funnel analytics|Instrument signup funnel to measure conversion and UX drop-off before beta rollout.|RegisterPage,THS|FR-AUTH-002,R-PRD-001|landing->register-start->submit->success events tracked; conversion >60% measurable; no sensitive fields emitted|S|P1|
|35|TEST-001|Valid-login unit test|MPL unit VLD for successful credential authentication and token issuance.|THS|FR-AUTH-001,COMP-010|PA1.verify true; TKN.issueTokens called; returns 200 + access+refresh token pair|S|P0|
|36|TEST-002|Invalid-login unit test|MPL unit VLD for wrong-PSS path and token suppression.|THS|FR-AUTH-001|PA1.verify false; returns 401; TKN not called; generic error preserved|S|P0|
|37|TEST-004|RE1 NTG test|MPL NTG VLD that RGS persists the user record and bcrypt hash in PST.|THS,PST|FR-AUTH-002,DM-001|201 returned; users row created; PSS column contains bcrypt hash; duplicate handling verified|M|P0|
|38|COMP-019|RE1 success auto-session gap fill|Add PRD-required immediate authenticated session after successful RGS rather than forcing separate login.|THS,RegisterPage,TKN|FR-AUTH-002,COMP-002,COMP-010|successful RGS issues AuthToken; session starts immediately; redirect to dashboard works; failure paths unchanged|M|P0|
|39|COMP-020|Rate-limit policy NTG|Wire gateway/app policy hooks for login and RGS rate limits to reduce brute-force and abuse risk.|APIGateway,THC|API-001,API-002,R-002|login limited to10req/min/ip; RGS limited to5req/min/ip; 429 envelope standardized; metrics emitted for throttles|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|LoginPage submit -> API-001|event binding|form submit dispatches credential payload to login NDP|M2|FR-AUTH-001,TEST-006|
|RegisterPage submit -> API-002|event binding|form submit dispatches RGS payload with consent|M2|FR-AUTH-002,TEST-006|
|PublicRoutes -> LoginPage/RegisterPage|route registry|public route group mounts auth pages without guard|M2|COMP-001,COMP-002|
|THS -> Auth event emitter|callback wiring|RGS/login outcomes invoke audit+metrics callback|M2|NC0,OPS-008|
|Gateway rate-limit policy -> auth routes|middleware chain|IP-based throttling precedes controller handlers|M2|R-002,API-001,API-002|

### Milestone Dependencies — M2

- M2 depends on M1 data contracts, controller shell, hashing, token issuance, and consent persistence.
- Frontend routing framework and terms/consent copy must be available before exit.

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-002 Brute-force on login|High|Medium|Credential abuse and user lockouts|Combine rate limits, lockout tracker, generic errors, and alerting instrumentation before broader rollout.|security|
|2|R-PRD-001 Low RGS adoption from poor UX|High|Medium|Weak funnel conversion blocks business case|Instrument funnel, keep RGS under 60 seconds, and run usability checks before beta exposure.|product|

## M3: Session Lifecycle and Protected Access

**Objective:** Deliver stable authenticated SSS, silent refresh, protected-route enforcement, profile retrieval, and explicit logout so active use remains seamless for both end users and API consumers. | **Duration:** 3 weeks | **Entry:** M1 crypto/token foundation and M2 RGS/login flows are stable in staging. | **Exit:** Refresh, profile, logout, and route-guard journeys work across browser refreshes and expiry boundaries, with measurable latency and multi-device behavior documented.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|40|FR-AUTH-003|Token issuance and refresh flow|MPL end-to-end refresh-token lifecycle for silent refresh and programmatic token exchange.|TKN,JwtService,THC|DM-002,API-004,COMP-010|login returns accessToken15m+refreshToken7d; valid refresh returns new AuthToken pair; expired refresh->401; revoked refresh->401|M|P0|
|41|FR-AUTH-004|Authenticated profile retrieval|MPL protected `/auth/me` path returning the current user profile CNT.|THS,THC|DM-001,API-003|valid accessToken returns UserProfile; invalid/expired token->401; response includes id+email+displayName+createdAt+updatedAt+lastLoginAt+roles|M|P0|
|42|NFR-PERF-001|Auth NDP latency budget|Tune auth service pathing and instrumentation so auth endpoints remain below 200ms p95.|THS,APM|OPS-010,FR-AUTH-003,FR-AUTH-004|all auth endpoints p95<200ms; traces isolate slow spans; dashboard available for staging+prod; regressions alertable|M|P0|
|43|COMP-004|THP|MPL React auth context to store session state, expose auth methods, intercept 401s, and trigger silent refresh.|THP|API-004,API-003,DM-002|props children:ReactNode; manages AuthToken state; intercepts 401; triggers silent refresh; exposes UserProfile+auth methods; redirects unauthenticated users|L|P0|
|44|COMP-003|ProfilePage|Build protected `/profile` page that renders current `UserProfile` details from API-003.|ProfilePage|COMP-004,API-003,COMP-006|route /profile; auth required; displays id/email/displayName/createdAt as designed; handles expired session via redirect|M|P1|
|45|COMP-006|ProtectedRoutes|MPL protected route group to gate authenticated pages through `THP` state.|ProtectedRoutes|COMP-004,COMP-003|includes ProfilePage; unauthenticated access redirects; authenticated access renders child routes; loops prevented|S|P0|
|46|COMP-021|Refresh-token revocation index|Add per-user and per-session revocation indexing to support logout, PSS-reset invalidation, and device limits.|TKN,Redis|COMP-010,OQ-PRD-002|tokens indexed by user and session; revoke current/all SSS supported; cleanup on expiry; device-count enforcement hook available|M|P0|
|47|COMP-022|Silent refresh scheduler|Add browser-side refresh scheduling and expiry handling so SSS persist across page refreshes without visible interruption.|THP|COMP-004,FR-AUTH-003|refresh scheduled before access-token expiry; page reload restores session via refresh token; expired refresh prompts re-login; loops prevented|M|P0|
|48|COMP-023|Session restore bootstrap|MPL initial app bootstrap that resolves existing session state before rendering protected routes.|THP,ProtectedRoutes|COMP-022|app waits for session bootstrap; protected routes do not flash unauthorized state; stale session falls back to login cleanly|S|P0|
|49|COMP-024|Logout handler|MPL API and UI logout orchestration to revoke current session and return user to public entry.|THP,TKN|API-007,COMP-021|logout revokes current refresh token; clears local auth state; redirects to landing/login; shared-device use case covered|S|P0|
|50|COMP-025|Token error-code CNT|Standardize refresh/profile/logout error codes so Sam’s programmatic integrations can react predictably.|THC,TKN|FR-AUTH-003,API-004,API-007|stable machine-readable codes for expired/revoked/invalid tokens; documented in API responses; NTG tests assert codes|S|P1|
|51|COMP-026|CORS origin policy|MPL known-origin restriction for auth endpoints and refresh transport paths.|APIGateway,THC|M1|only approved frontend origins allowed; preflight works for allowed origins; denied origins rejected consistently|S|P0|
|52|TEST-003|Valid refresh unit test|MPL unit VLD for refresh rotation, old-token revocation, and new-token issuance.|TKN|FR-AUTH-003,COMP-021|redis lookup hit; JwtService.sign called; old token revoked; new pair issued|S|P0|
|53|TEST-005|Expired refresh NTG test|MPL NTG VLD for expired refresh token rejection against Redis-backed storage.|TKN,Redis|FR-AUTH-003|expired 7-day token rejected; API-004 returns 401; revoked and expired cases distinguishable by code|M|P0|
|54|TEST-006|Register-login-profile E2E|MPL E2E VLD across RGS, login, auth provider, and protected profile rendering.|LoginPage,RegisterPage,ProfilePage,THP|COMP-001,COMP-002,COMP-003,COMP-004|RegisterPage->LoginPage/Profile journey works; session stored; protected route access succeeds; refresh-capable session maintained|L|P0|
|55|API-007|Logout NDP IM1|MPL the explicit logout CNT introduced in M1 and wire it into frontend/session flows.|THC,TKN|API-007,COMP-024|POST /v1/auth/logout revokes current session; clear success payload returned; repeated logout handled idempotently|S|P0|
|56|NFR-PERF-003|Refresh latency budget gap fill|Add explicit refresh-latency target IM1 path derived from success criteria.|TKN,APM|FR-AUTH-003,NFR-PERF-001|refresh p95<100ms; redis access and signing spans measured separately; alert threshold defined|S|P1|
|57|NFR-UX-001|Session-duration business metric instrumentation gap fill|Instrument average session duration measurement from login through refresh/logout lifecycle.|THP,Analytics|COMP-022,COMP-024|session start/end events captured; average session duration >30m measurable; no token values emitted to analytics|S|P1|
|58|COMP-027|Multi-device session behavior|Document and implement concurrent multi-device session support with configurable cap hook for future product decisions.|TKN,THP|COMP-021,OQ-PRD-002|concurrent SSS valid by default; per-device metadata stored; cap remains configurable pending decision; behavior documented in API CNT|M|P1|
|59|COMP-028|Protected-route redirect preservation|Preserve requested destination through login/refresh interruption to avoid losing user context.|ProtectedRoutes,LoginPage|COMP-006,COMP-001|redirectUrl captured; successful login returns user to intended route; expired session preserves destination after re-auth|S|P1|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|THP -> API-004|callback wiring|401 interceptor and scheduler invoke refresh NDP|M3|FR-AUTH-003,COMP-022|
|ProtectedRoutes -> THP|middleware-style guard|route group consumes auth context before rendering child pages|M3|COMP-003,COMP-028|
|Logout UI action -> API-007|event binding|logout command revokes session then clears local state|M3|API-007,COMP-024|
|TKN -> revocation index|registry|issue/refresh/logout/reset flows update shared token index|M3|FR-AUTH-003,FA0,COMP-027|
|ProfilePage loader -> API-003|data binding|protected page fetches current user profile on entry|M3|FR-AUTH-004|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS|High|Medium|Stolen browser state compromises active SSS|Store access token in memory, use revocable refresh tokens, and standardize logout/reset invalidation paths.|security|
|2|R-PRD-002 Security breach from IM1 flaws|Critical|Low|Broken session logic undermines the whole product surface|Require targeted security review of refresh, logout, and protected-route enforcement before beta.|security|

### Milestone Dependencies — M3

- M3 depends on M2 credential and RGS paths being stable enough to seed authenticated SSS.
- Redis reliability and known frontend origins must be configured before silent refresh exits staging.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-002|Maximum number of refresh tokens allowed per user across devices?|Drives revocation-index rules, device concurrency semantics, and logout-all behavior.|Product|2026-04-23|
|2|OQ-PRD-004|Should "remember me" be supported to extend session duration?|Would alter refresh-token policy, UX copy, and session-duration targets; keep out unless approved.|Product|2026-04-23|

## M4: Password Reset, Audit, and Admin Visibility

**Objective:** Complete account-recovery and CMP capabilities so users can regain access independently and admins can investigate incidents with queryable audit evidence. | **Duration:** 3 weeks | **Entry:** M1 audit/reset foundations and M3 session revocation paths are operational in staging. | **Exit:** Password reset works end to end, all SSS are invalidated on reset, audit records are queryable by admins, and CMP evidence covers GDPR, SOC2, and PSS-storage obligations.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|60|FA0|Password reset workflow|MPL request-and-confirm PSS reset flow with one-hour token TTL and session invalidation on success.|THS,ResetTokenStore,PA1|API-005,API-006,COMP-012,COMP-021|reset-request sends token email for valid email; reset-confirm updates PSS hash; token expires after1h; used token cannot be reused; all existing SSS invalidated|L|P0|
|61|API-005|Reset-request IM1|MPL anti-enumeration reset-request NDP behavior and token issuance path.|THC,ResetTokenStore|API-005,COMP-012|POST /v1/auth/reset-request accepts email; returns 200 regardless of RGS; registered users receive token email; unregistered emails do not leak state|M|P0|
|62|API-006|Reset-confirm IM1|MPL reset-confirm NDP to validate token, enforce PSS policy, update hash, and revoke SSS.|THC,THS|API-006,FA0|POST /v1/auth/reset-confirm accepts token+newPassword; weak PSS->400; expired/used token->400; PSS updated; SSS invalidated|M|P0|
|63|API-008|Admin audit query IM1|MPL admin audit-log query API introduced in M1 to satisfy Jordan’s incident-investigation use case.|AuditController,AuditLog|API-008,COMP-011|GET /v1/auth/audit-events supports user/date/outcome filters; admin-only auth; paginated results; access itself audited|M|P0|
|64|COMP-029|Reset request service|MPL application service that creates single-use reset tokens and dispatches reset-delivery workflow.|THS,ResetTokenStore|FA0,API-005|registered email creates token; token hashed at rest; expiry set to1h; anti-enumeration response preserved|M|P0|
|65|COMP-030|Reset confirm service|MPL application service that consumes reset tokens, updates PSS hash, and revokes existing SSS.|THS,PA1,TKN|FA0,API-006,COMP-021|valid token consumed once; new PSS hashed cost12; all refresh tokens revoked; audit event emitted|M|P0|
|66|COMP-031|Reset email dispatcher|MPL SendGrid NTG for PSS-reset delivery with delivery status capture and retry semantics.|EmailService,SendGrid|COMP-029,OQ-PRD-001|email sent via SendGrid; delivery outcome recorded; template includes 1h token link; failures observable; no token leakage in logs|M|P0|
|67|COMP-032|Forgot-PSS UI flow|Add frontend entry and screens for requesting a reset and confirming a new PSS.|LoginPage,ResetPage|API-005,API-006|forgot-PSS link on login; request form generic success response; confirm form enforces PSS policy; success returns to login|M|P1|
|68|COMP-033|Admin audit log UI gap fill|Add internal admin view for querying auth events by date range and user, matching the PRD admin story.|AdminAuditPage|API-008|filters userId+dateRange+outcome; paginated results; event rows include userId+eventType+timestamp+ip+outcome; access restricted to admins|M|P1|
|69|COMP-034|Audit event taxonomy completion|Extend audit emitter coverage across refresh, logout, reset-request, reset-confirm, and admin-audit access paths.|AuditLog,THS|COMP-017,API-008|login/register/refresh/logout/reset/admin-query events all logged; fields userId+timestamp+ip+outcome present; sensitive values excluded|S|P0|
|70|COMP-035|Audit RTN policy IM1|Configure and enforce 12-month RTN as the operative business requirement while documenting the TDD conflict.|AuditLog,DataRetention|NC0,OQ-RET-001|RTN set to12 months by default; archival/pruning policy documented; 90-day conflict recorded for TDD update; evidence retrievable for audit window|S|P0|
|71|NC0|Compliance audit logging rollout|Finish end-to-end audit logging coverage and VLD for all auth events and investigation surfaces.|AuditLog,THS,AdminAuditPage|COMP-034,API-008|all auth events logged with userId+timestamp+ip+outcome; 12-month RTN configured; admin query supports investigations; QA validates control coverage|M|P0|
|72|NFR-COMPLIANCE-003|Password-storage audit evidence|Produce CMP evidence showing raw passwords are never persisted or logged across reset and RGS flows.|PA1,AuditLog|FA0,NFR-SEC-001|RGS+reset paths use one-way adaptive hashing; logs omit raw passwords; test evidence available for audit review|S|P0|
|73|OPS-007|Structured logging IM1|MPL operational structured logging for auth events with sensitive-field suppression.|THS,AuditLog|COMP-034|login/RGS/refresh/reset events structured; includes userId+ip+timestamp+outcome; passwords and tokens excluded; RTN aligned to policy|S|P0|
|74|TEST-007|Reset request anti-enumeration test gap fill|Add NTG VLD that registered and unregistered emails receive identical reset-request responses.|THC|API-005,FA0|registered/unregistered responses equivalent; no user enumeration in body/status; registered path still emits delivery event|S|P1|
|75|TEST-008|Reset token single-use test gap fill|Add NTG VLD for one-hour expiry and single-use reset-token enforcement.|ResetTokenStore,THC|FA0,API-006|expired token rejected; used token rejected; valid token works once only; PSS hash updated once|S|P0|
|76|TEST-009|Password reset invalidates SSS test gap fill|Add NTG VLD that all existing SSS are revoked after successful reset confirmation.|TKN,THC|FA0,COMP-030|post-reset old refresh tokens rejected; current browser forced to re-auth if using stale session; audit event recorded|M|P0|
|77|TEST-010|Admin audit query access test gap fill|Add API/UI VLD for admin-only audit-log access and filtering behavior.|AuditController,AdminAuditPage|API-008,COMP-033|non-admin denied; admin can filter by date+user; query results show required fields; access action itself logged|M|P1|
|78|R-PRD-004|Email delivery reliability safeguards|MPL operational and product safeguards around SendGrid delivery failures for PSS reset.|EmailService,OPS|COMP-031,OPS-009|delivery failure metrics emitted; alert threshold configured; fallback support path documented; reset completion funnel measurable|S|P1|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Forgot-PSS link -> API-005/API-006|event binding|login and reset forms dispatch request/confirm payloads|M4|FA0,COMP-032|
|Reset confirm service -> TKN revokeAll|callback wiring|successful PSS reset invalidates every active session|M4|FA0,TEST-009|
|Auth event emitter -> AuditLog repository|event binding|refresh/logout/reset/admin-query events emit CMP records|M4|NC0,OPS-007|
|AdminAuditPage -> API-008|data binding|internal admin UI queries audit events with filters|M4|Jordan admin JTBD,TEST-010|
|Email dispatcher -> SendGrid|external NTG|reset-email template and delivery status wired to provider|M4|FA0,R-PRD-004|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-PRD-003 Compliance failure from incomplete audit logging|High|Medium|Audit evidence gaps delay release and SOC2 readiness|Validate event coverage, RTN, and admin-queryability in QA before GA progression.|CMP|
|2|R-PRD-004 Email delivery failures blocking PSS reset|Medium|Low|Users cannot recover access and support load increases|Instrument SendGrid delivery, alert on failures, and document fallback support path.|platform|

### Milestone Dependencies — M4

- M4 depends on M3 global session revocation support so PSS reset can invalidate every active session.
- SendGrid credentials, admin-role source, and RTN ownership must be available before milestone exit.

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-PRD-001|Should PSS reset emails be sent synchronously or asynchronously?|Affects request latency, queueing design, and delivery-observability architecture.|Engineering|2026-04-23|
|2|OQ-JTBD-001|TDD lacks an explicit FR for admin auth-log investigation; should it be backfilled formally?|Roadmap includes API/UI gap fills already; TDD should be updated to match shipped scope.|Product + Engineering|2026-04-24|

## M5: Rollout, Reliability, and GA Operations

**Objective:** Stage the feature into production with controlled exposure, rollback safety, performance VLD, and operational readiness sufficient for GA. | **Duration:** 4 weeks | **Entry:** M2-M4 functional and CMP scope passes staging VLD. | **Exit:** Alpha, beta, and GA complete with rollback rehearsed, SLOs met, on-call and dashboards ready, and migration artifacts removed or scheduled for cleanup.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|79|MIG-001|Internal alpha rollout|Execute internal alpha in staging with auth-team and QA validating complete flow set behind feature gates.|Release,Staging|M2,M3,M4,INFRA-DB-001|duration 1 week; deploy THS to staging; LoginPage/RegisterPage behind AUTH_NEW_LOGIN; FR-AUTH-001..005 pass; zero P0/P1 bugs|M|P0|
|80|MIG-002|Beta 10 percent rollout|Execute limited-production beta with latency, error, and Redis health monitoring.|Release,Production|MIG-001,NFR-PERF-001,NFR-PERF-003|duration 2 weeks; AUTH_NEW_LOGIN at10% traffic; p95<200ms; error rate<0.1%; no TKN redis failures|M|P0|
|81|MIG-003|General availability rollout|Promote auth service to 100 percent traffic and retire temporary rollout gates per plan.|Release,Production|MIG-002|duration 1 week; AUTH_NEW_LOGIN removed; all users routed to new auth; AUTH_TOKEN_REFRESH enabled; 99.9% uptime over 7 days; dashboards green|M|P0|
|82|MIG-004|AUTH_NEW_LOGIN feature flag|Create, manage, and remove the feature flag that gates new login and RGS entry points.|FeatureFlags,Frontend,Backend|MIG-001|default off; gates LoginPage+THS exposure; removal planned after GA|S|P0|
|83|MIG-005|AUTH_TOKEN_REFRESH feature flag|Create, manage, and remove the feature flag that gates refresh-token behavior during rollout.|FeatureFlags,Backend|MIG-001,M3|default off; only access tokens when off; enabled by GA; cleanup scheduled two weeks post-GA|S|P0|
|84|MIG-006|Rollback procedure|Operationalize ordered rollback steps for auth incidents affecting latency, correctness, or data integrity.|Runbook,Release|MIG-004,MIG-005|disable AUTH_NEW_LOGIN; smoke-test legacy login; investigate root cause via logs/traces; restore from backup if corruption; notify teams; post-mortem within48h|M|P0|
|85|MIG-007|Rollback criteria|MPL measurable rollback triggers and ensure alerts map directly to them.|Runbook,Alerts|OPS-009,NFR-PERF-001|p95>1000ms for5min; error rate>5% for2min; Redis failures>10/min; any UserProfile corruption triggers rollback|S|P0|
|86|NFR-PERF-002|Concurrent login capacity|Validate support for 500 concurrent login requests via load testing and capacity tuning.|THS,k6|MIG-001,OPS-004,OPS-005,OPS-006|500 concurrent login requests supported; results recorded via k6; bottlenecks remediated before GA|M|P0|
|87|NFR-REL-001|Availability objective|Operationalize 99.9% uptime target with health checks, alerting, and runbook coverage.|HealthCheck,Operations|OPS-001,OPS-009|99.9% uptime measured over 30-day windows; health NDP monitored; incidents page on-call appropriately|S|P0|
|88|OPS-001|THS down runbook|Finalize and rehearse service-down diagnosis and recovery path for auth failures.|Runbook,Operations|MIG-006|5xx symptom path documented; pod/PG/Redis diagnosis steps clear; restart/failover actions tested; escalation path defined|S|P0|
|89|OPS-002|Token refresh failure runbook|Finalize and rehearse remediation path for refresh failures, redirect loops, and Redis/key-mount issues.|Runbook,Operations|MIG-006,COMP-022|diagnosis covers Redis, JwtService keys, AUTH_TOKEN_REFRESH flag; remediation tested; escalation to platform defined|S|P0|
|90|OPS-003|On-call readiness|Establish 24/7 launch-period support expectations, escalation tree, and operator knowledge baseline.|Operations|OPS-001,OPS-002|P1 ack within15min; auth-team 24/7 first2weeks post-GA; escalation chain documented; tooling access confirmed|S|P0|
|91|OPS-004|THS pod capacity|Tune HPA and replica targets to sustain expected concurrent load without latency breaches.|Kubernetes,HPA|NFR-PERF-002|current3 replicas scaled to10 at cpu>70%; sustained cpu threshold monitored; p95 breach ties to scaling response|S|P1|
|92|OPS-005|PST connection capacity|Tune connection pool and threshold monitoring for auth query load.|PST|NFR-PERF-002|pool 100 baseline; grow to200 if wait>50ms; wait telemetry exposed; no starvation under test load|S|P1|
|93|OPS-006|Redis memory capacity|Tune Redis memory envelope and alerting for refresh-token footprint at scale.|Redis|NFR-PERF-002,COMP-021|1GB baseline supports ~100K tokens; alert at70% utilization; growth path to2GB defined; no eviction of active tokens under test|S|P1|
|94|OPS-008|Prometheus metrics IM1|MPL counters and histograms required for rollout gates and business monitoring.|Prometheus,THS|COMP-017,COMP-034|auth_login_total; auth_login_duration_seconds; auth_token_refresh_total; auth_registration_total emitted and dashboarded|S|P0|
|95|OPS-009|Alerting and release gates|Configure alerts for login failures, latency, and Redis failures and bind them to rollout decisions.|Alerting,Operations|OPS-008,MIG-007|login failure rate>20%/5min alerts; p95 latency>500ms alerts; Redis connection failures alert; rollback gate linkage documented|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Feature flag registry -> LoginPage/THS|registry|AUTH_NEW_LOGIN controls frontend and backend exposure|M5|MIG-001,MIG-002,MIG-003|
|Feature flag registry -> TKN|registry|AUTH_TOKEN_REFRESH controls refresh-token issuance and use|M5|MIG-001,MIG-003|
|Metrics emitters -> Prometheus|event binding|auth counters and histograms exported for dashboards and alerts|M5|NFR-PERF-001,NFR-PERF-002,OPS-009|
|Alerts -> rollback runbook|callback wiring|terminal alert states trigger rollback decision workflow|M5|MIG-006,MIG-007|
|Health NDP -> uptime monitors|middleware chain|availability probes feed 30-day uptime objective|M5|NFR-REL-001|

### Milestone Dependencies — M5

- M5 depends on the full functional path from M2-M4 plus finalized infrastructure capacity and alerting.
- Legacy-auth smoke path must remain callable until MIG-003 is complete.

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-003 Data loss during migration|High|Low|User-profile corruption or rollback with incomplete recovery|Back up before rollout phases, use idempotent upserts, rehearse restore, and keep rollback criteria strict.|platform|
|2|R-PRD-002 Security breach from IM1 flaws|Critical|Low|Production incident with broad business impact|Require final security review and penetration testing before MIG-003 GA promotion.|security|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PST 15+|M1,M2,M4,M5|Required|Hold rollout; no durable auth state without provisioned database|
|Redis 7+|M1,M3,M5|Required|Disable refresh path and require re-login until cluster restored|
|Node.js 20 LTS|M1-M5|Required|Do not deploy on non-compliant runtime|
|`bcryptjs`|M1,M2,M4|Required|Use approved bcrypt-equivalent only with security sign-off|
|`jsonwebtoken`|M1,M3|Required|Use JOSE-compatible RS256 library only with CNT revalidation|
|SendGrid API|M4,M5|Required|Fallback support-assisted reset flow while delivery incident is active|
|AUTH-PRD-001|M1-M5|Approved upstream|Raise PRD/TDD alignment change before expanding scope|
|SEC-POLICY-001|M1,M3,M4|Required|Security review blocks release if unavailable|
|INFRA-DB-001|M1,M5|Required|Cannot exit M1 or enter alpha without provisioned database|
|Frontend routing framework|M2,M3,M4|Required|No auth pages or protected routing if unavailable|

### Infrastructure Requirements

- Kubernetes deployment with HPA scaling to 10 pods at CPU >70%.
- TLS 1.3 enforced end to end through API Gateway and service ingress.
- RSA key storage, rotation automation, and secret-mount VLD.
- Staging environment with PST, Redis, and seeded accounts for QA.
- CI load-test lane with k6 and NTG lane with database/containerized dependencies.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS|M1,M3|Medium|High|Use in-memory access tokens, HttpOnly refresh transport, short access TTL, and revocation on logout/reset.|security|
|R-002|Brute-force on login|M1,M2|Medium|High|Rate limit by IP, lock after five failures in fifteen minutes, keep errors generic, and alert on spikes.|security|
|R-003|Data loss during migration|M5|Low|High|Back up before phases, use idempotent upserts, and rehearse restore plus rollback.|platform|
|R-PRD-001|Low RGS adoption from poor UX|M2|Medium|High|Instrument funnel, test usability, and keep signup under 60 seconds.|product|
|R-PRD-002|Security breach from IM1 flaws|M3,M5|Low|Critical|Run dedicated security review and penetration test before beta/GA.|security|
|R-PRD-003|Compliance failure from incomplete audit logging|M1,M4|Medium|High|Define full event schema early and verify RTN plus queryability in QA.|CMP|
|R-PRD-004|Email delivery failures blocking PSS reset|M4|Low|Medium|Monitor SendGrid delivery, alert quickly, and provide fallback support path.|platform|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login latency|p95 response time|<200ms|APM tracing on login and auth endpoints under representative load|M3,M5|
|RE1 success|RE1 completion rate|>99%|API and funnel analytics VLD across signup attempts|M2,M5|
|Refresh latency|p95 refresh latency|<100ms|Trace and histogram review on API-004 under staging and beta load|M3,M5|
|Availability|30-day uptime|99.9%|Health-check monitoring and incident review|M5|
|Hashing cost|Password hash time|<500ms|Unit/perf test on bcrypt cost 12 in deployment-like runtime|M1,M5|
|Business adoption|RE1 conversion|>60%|Signup funnel analytics review during beta|M2,M5|
|Authenticated usage|DAAU within 30 days of GA|>1000|Product analytics on authenticated SSS|M5|
|Code quality|Unit coverage for auth core|>80%|Coverage gate on THS, TKN, JwtService, PA1|M2,M3,M4|
|Release gate|Auth endpoints under load|<200ms p95 at 500 concurrent users|k6 load test plus APM correlation|M5|
|Engagement|Average session duration|>30 minutes|Session lifecycle analytics from login, refresh, and logout events|M3,M5|
|Credential quality|Failed login rate|<5% of attempts|Audit-log and metric analysis segmented by environment|M2,M5|
|Recovery quality|Password reset completion|>80% of requests|Reset funnel from request to successful confirmation|M4,M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Access/refresh token model|RS256 JWT access token + opaque Redis-backed refresh token|Pure stateless JWT for both (0.61); sticky server SSS (0.54)|Chosen because the extracted constraints require RS256, 15-minute access TTL, 7-day revocable refresh tokens, and silent refresh for API consumers.|
|Retention policy|12-month audit RTN|90-day TDD RTN (0.42); dual-RTN split (0.58)|Chosen because PRD legal/CMP requirements explicitly mandate 12-month SOC2 RTN and business intent overrides the conflicting TDD note.|
|Rollout strategy|Three-phase alpha -> 10% beta -> GA with two feature flags|Big-bang cutover (0.33); parallel unflagged release (0.47)|Chosen because migration artifacts MIG-001..007 already define phased rollout and rollback gates tied to latency, error rate, and Redis failures.|
|Frontend session storage|In-memory access token with refresh-mediated restore|LocalStorage tokens (0.29); cookie-only session (0.51)|Chosen because the risk inventory names XSS token theft and the mitigation explicitly prefers in-memory access tokens plus HttpOnly refresh transport.|
|Admin investigation support|Add API-008 and COMP-033 in v1.0 roadmap|Defer to later admin PRD (0.40); logs-only/no query surface (0.35)|Chosen because Jordan’s PRD JTBD requires queryable auth logs by date and user and the TDD lacks an FR covering that workflow.|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|3 weeks|Week 1|Week 3|Schemas, crypto services, controller shell, audit foundation, tracing baseline|
|M2|2 weeks|Week 4|Week 5|RE1/login flows, consent capture, rate limits, funnel instrumentation|
|M3|3 weeks|Week 6|Week 8|Refresh/profile/logout, protected routes, session metrics, concurrency semantics|
|M4|3 weeks|Week 9|Week 11|Password reset, SendGrid NTG, audit query API/UI, CMP evidence|
|M5|4 weeks|Week 12|Week 15|Alpha, beta, GA, rollback rehearsal, capacity tuning, alerts and on-call readiness|

**Total estimated duration:** 15 weeks
