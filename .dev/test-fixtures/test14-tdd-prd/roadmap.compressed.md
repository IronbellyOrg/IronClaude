<!-- CONV: AuthService=THS, TokenManager=TKN, AuthProvider=THP, Implement=MPL, PasswordHasher=PSS, registration=RGS, FR-AUTH-001=FA0, UserProfile=SRP, contract=CNT, PostgreSQL=PST, NFR-COMP-002=NC0, AUTH_NEW_LOGIN=ANL, AuditLogWriter=DTL, JwtService=JWT, documented=DCM, Validate=VLD, Validation=VA1, Milestone=MLS, AuthToken=THT, validation=VA2 -->
---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "B"
variant_scores: "A:78 B:82"
convergence_score: 0.62

# User Authentication Service — Project Roadmap

## Executive Summary

The roadmap delivers the platform's first secure, self-service identity layer — RGS, login, JWT-based session persistence, profile retrieval, self-service password reset, logout, and minimal admin audit — using a layered linear delivery (contracts → APIs → client → rollout → ops handover) that unblocks Q2 2026 personalization revenue while satisfying the Q3 2026 SOC2 Type II audit dependency on authenticated event logging. The plan is organized as 5 milestones over ~10 weeks, absorbing Opus-grade testing rigor, pen-test booking mechanics, migration safety, and a dedicated ops handover phase on top of the Haiku linear scaffold.

**Business Impact:** Unblocks ~$2.4M projected 2026 personalization revenue (PRD S19); enables SOC2 Type II audit trail (PRD S17 + NC0) including Jordan admin visibility; reduces access-ticket support volume (30% QoQ growth per PRD S4); targets RGS conversion >60%, login p95 <200ms, failed-login <5%, password-reset completion >80% (PRD S19 + TDD §4.1–4.2).

**Complexity:** HIGH (0.72) — driven by six cross-cutting domains (backend/security/frontend/testing/devops/compliance), authentication-level security criticality (bcrypt cost 12, RS256, refresh-token revocation, account lockout, XSS hardening), five external integrations (PST 15, Redis 7, SendGrid, API Gateway, frontend THP), and a three-phase rollout parallel-run against legacy auth. Mitigating factors: bounded endpoint surface, no OAuth/MFA/RBAC in v1.0, single greenfield service rather than cross-system refactor.

**Critical path:** SEC-POLICY-001 sign-off + OQ-003/005/007/008 resolution → infrastructure provisioning (PST 15, Redis 7, SendGrid) → canonical data and token contracts → core crypto primitives (PSS, JWT, TKN) → THS orchestrator → `/v1/auth/*` REST surface (user + admin) → frontend THP + pages → test pyramid with pre-merge NFR gates → pen-test booked W4 with 1w remediation buffer → MIG-001 internal alpha → MIG-002 10% beta → MIG-003 100% GA → dedicated ops handover with RSA rotation + retention jobs automated.

**Key architectural decisions:**

- **Stateless THS + Redis-backed hashed refresh tokens** with 15-minute access JWTs and 7-day refresh TTL — enables horizontal scale (HPA 3→10 pods) and immediate revocation without sticky sessions.
- **Bcrypt cost 12 behind PSS abstraction and RS256 2048-bit RSA** with quarterly rotation — satisfies NIST SP 800-63B (PRD S17) and TDD constraints while preserving algorithm upgrade path.
- **Three-phase rollout with two feature flags (ANL + AUTH_TOKEN_REFRESH)** and named rollback triggers (p95>1000ms/5min, err>5%/2min, Redis conn failures>10/min) — chosen over big-bang cutover given R-003 data-loss severity.
- **Close SOC2 Jordan gap in v1.0** via minimal admin surface (API-007 logout, API-008 events query, API-009 lock, API-010 unlock, COMP-011 AdminAuditPage) — PRD S7 persona coverage tips over clean-boundary deferral because SOC2 Type II audit evidence is required Q3 2026.
- **12-month audit retention over 90-day TDD default** — OQ-003 conflict resolved in favor of PRD S17 SOC2 Type II evidence requirement.
- **API versioned under `/v1/auth/*`** with additive evolution — supports future MFA/OAuth without destabilizing THP.

**Open risks requiring resolution before M1:**

- OQ-003 audit retention conflict (90-day TDD vs 12-month PRD/SOC2) — blocks NC0 scope, storage sizing, and partition strategy. Owner: compliance + auth-team. Target: M1 Day 3.
- OQ-005 refresh-token-per-user cap — affects Redis capacity planning (OPS-004) and TKN key schema. Owner: product. Target: before M1 COMP-007 design freeze.
- OQ-007 remember-me (session duration extension) — affects frontend state CNT and refresh TTL behavior; resolve as hard gate before M2 code freeze per debate convergence.
- OQ-008 admin scope confirmation (Jordan JTBD — API-008/009/010 + COMP-011) — closes PRD/TDD gap and SOC2 evidence; resolve as hard gate before M2 code freeze.
- R-PRD-004 security breach risk (critical) — pen-test vendor booked by W4 with 1-week remediation buffer reserved before GA.

## MLS Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Security, contracts, persistence baseline + M1 scaffolding hardening|Foundation|P0|2w|SEC-POLICY-001; OQ-003/005/007/008; PST 15; Redis 7; Node.js 20|27|High|
|M2|Core auth APIs and compliance flows|Backend|P0|2w|M1; SendGrid; API Gateway|29|High|
|M3|Client integration, admin gaps, and QA with pre-merge test gates|Application/Quality|P0|2w|M2; routing framework; k6; Playwright|23|Medium|
|M4|Rollout, migration safety, and observability|Release|P0|3w|M3; LaunchDarkly; Prometheus/OTel; pen-test vendor|35|High|
|M5|Operational readiness and runbook handover|Ops|P1|1w|M4|8|Low|

## Dependency Graph

```
SEC-POLICY-001, PostgreSQL 15, Redis 7, Node.js 20 LTS, SendGrid → M1
M1 → {DM-001, DM-002, DM-003, COMP-005..009, COMP-012/013, DEP-*, COMP-INFRA-TLS, COMP-XSS-HARDEN, COMP-DLP}
M1 → M2 → {API-001..010, FR-AUTH-001..005, NFR-PERF-001/002, NFR-REL-001, NFR-COMP-002, COMP-EMAILCLIENT, COMP-LOCKOUT, COMP-RESETTOKEN, COMP-VALIDATOR, COMP-AUTHMW, COMP-ERRORENV, COMP-OPENAPI, COMP-PENTEST-BOOK}
M2 → M3 → {COMP-001..004, COMP-010/011, COMP-FE-RESET-*, PRD-JOURNEY-*, TEST-001..006, TEST-IMPLICIT-*, TEST-SEC-*, TEST-COVERAGE-GATE}
M2, M3 → M4 → {MIG-001..003, MIG-FLAG-*, MIG-DATAMIG-BACKUP, MIG-DUAL-RUN, MIG-002-ROLLBACK, MIG-ROLLBACK-RUNBOOK, MIG-LEGACY-DEPRECATE, MIG-FLAG-REMOVE, COMP-METRICS, COMP-TRACING, COMP-ALERTS, COMP-CORS, COMP-PENTEST, R-001..003, R-PRD-001..004, SC-001..012}
M4 → M5 → {OPS-001..005, OPS-RSA-ROTATION, OPS-RETENTION-JOB, OPS-POSTMORTEM-TEMPLATE}
```

## M1: Security, contracts, persistence baseline

**Objective:** Freeze security, compliance, token, and persistence contracts; provision infrastructure; harden M1 scaffolding (TLS 1.3, CSP/HSTS, secret scrubbing) before feature implementation. | **Duration:** 2w (Week 1–2) | **Entry:** SEC-POLICY-001 signed off; PST 15 and Redis 7 procurement confirmed | **Exit:** schemas/module boundaries/policy decisions implementation-ready; OQ-003/005/007/008 closed as hard gates before M2 code freeze; TLS 1.3 A+ verified

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|OQ-003|Resolve audit-retention conflict (90d TDD vs 12mo PRD)|Compliance|SEC-POLICY-001|decision:12mo signed by compliance+auth-team; TDD §7.2 updated; storage sizing recomputed; partition-drop plan drafted|S|P0|
|2|OQ-002|Bound roles cardinality|SRP|DM-001|roles max decided; token payload bounded; validator rule DCM; schema impact closed|S|P1|
|3|OQ-005|Cap concurrent refresh tokens per user|TKN|DM-002|per-user token cap decided; multi-device policy DCM; eviction rule defined; Redis sizing updated|S|P0|
|4|OQ-006|Confirm account lockout policy|THS|FA0|threshold:5/15m confirmed or revised; 423 behavior approved; admin visibility captured; gateway policy aligned|S|P0|
|5|OQ-007|Decide remember-me scope as hard gate before M2 freeze|Product/session UX|API-004, COMP-004|remember-me yes/no decided; session-duration impact DCM; token TTL CNT frozen; frontend state CNT aligned|S|P0|
|6|OQ-008|Resolve admin audit and lock scope as hard gate before M2 freeze|Admin surface|API-008, API-009, API-010|admin event view and lock/unlock confirmed in v1.0 scope or formally deferred; owner assigned; SOC2 evidence story DCM; roadmap variance closed|S|P0|
|7|DM-001|Define SRP schema|PST|OQ-002|id:UUIDv4-PK-NN; email:varchar-UNIQUE-NN-idx-lowercase; displayName:varchar-NN-2to100; passwordHash:varchar-NN; createdAt:timestamptz-NN-DEFAULTnow; updatedAt:timestamptz-NN-auto; lastLoginAt:timestamptz-nullable; roles:text[]-NN-DEFAULT'{"user"}'|M|P0|
|8|DM-002|Define THT CNT|TKN|FR-AUTH-003|accessToken:JWT-RS256-NN-payload{uid,roles}; refreshToken:opaque-NN-unique-Redis-7dTTL-hashedAtRest; expiresIn:number-NN-900; tokenType:string-NN-"Bearer"|M|P0|
|9|DM-003|Define AuditLog schema (append-only, monthly partitioned)|PST|OQ-003, DM-001|userId:UUID-FK-nullable; eventType:enum-NN{login_success,login_failure,RGS,token_refresh,password_reset,logout,lock,unlock}; timestamp:timestamptz-NN-idx; ipAddress:inet-NN; userAgent:text; outcome:enum-NN; monthly-partitioned; retention=12mo|M|P0|
|10|DEP-POSTGRES|Provision PST 15 cluster with read replica|Infrastructure|—|version≥15; connection pool=100; multi-AZ replica; nightly backup + WAL archive; PITR tested|M|P0|
|11|DEP-REDIS|Provision Redis 7 cluster (HA + sentinel)|Infrastructure|—|version≥7; cluster mode; 1GB baseline; HA+failover; TLS at rest|M|P0|
|12|DEP-NODE|Standardize Node.js 20 LTS build image|Infrastructure|—|Dockerfile base=node:20-LTS; SBOM generated; CVE scan=0 high; pinned bcryptjs + jsonwebtoken|S|P0|
|13|DEP-SENDGRID|Procure SendGrid account + sender domain|Infrastructure|—|API key in HashiCorp Vault; SPF/DKIM/DMARC records set; delivery domain warmed; webhook configured|M|P0|
|14|NFR-SEC-001|Standardize bcrypt cost 12 policy|PSS|DEP-NODE|algorithm:bcrypt; cost:12; raw-password never logged; config abstraction for future algorithm migration; unit-check defined|M|P0|
|15|NFR-SEC-002|Standardize RS256 key policy + rotation runbook|JWT|DEP-NODE|alg:RS256; key:2048-bit RSA; rotation:quarterly DCM; private key in HashiCorp Vault; dual-kid cutover window specified|M|P0|
|16|NFR-COMP-001|Capture GDPR consent at RGS|Registration|DM-001|consent_accepted_at:timestamptz-NN; consent_version:varchar; RGS rejected if unchecked; consent event audited; DPO sign-off|M|P0|
|17|NFR-COMP-003|Enforce data minimization at RGS boundary|Data boundary|DM-001|collect only:email+password_hash+displayName+consent; extra PII fields rejected 400; forms aligned; API schema whitelisted|M|P0|
|18|COMP-005|Establish THS facade (orchestrator)|THS|DM-001, DM-002, DM-003|type:backend-service; loc:Node.js20 service; deps-injected:PSS+TKN+JWT+UserRepo+AuditRepo+EmailClient; flows:login+register+profile+refresh+resetRequest+resetConfirm+logout; typed error codes|L|P0|
|19|COMP-006|Baseline backend security module package|Security modules|DM-002, NFR-SEC-001, NFR-SEC-002|type:backend-internal-modules; TKN:issue+refresh+revoke THT pairs+Redis hashed refresh TTL7d; JWT:sign+verify JWT RS256 2048-bit RSA skew5s; PSS:bcrypt cost12+migration abstraction|L|P0|
|20|COMP-007|Isolate TKN subcomponent|TKN|COMP-006, DM-002|type:backend-module; actions:issue+refresh+revoke; store:Redis hashed refreshToken TTL7d; rotation:on-use; multi-device policy applied; revoke O(1)|M|P0|
|21|COMP-008|Isolate JWT subcomponent|JWT|COMP-006, NFR-SEC-002|type:backend-module; actions:sign+verify accessToken; alg:RS256; key:2048-bit RSA; skew:5s; kid-based key lookup|M|P0|
|22|COMP-009|Isolate PSS subcomponent|PSS|COMP-006, NFR-SEC-001|type:backend-module; actions:hash+verify; alg:bcrypt; cost:12; future algorithm migration abstraction preserved|M|P0|
|23|COMP-012|MPL UserRepo adapter|UserRepo|DM-001|type:repository; store:PostgreSQL15+; ops:create+findByEmail+findById+updatePassword+updateLastLogin; uniqueness:email enforced; idempotent upsert for migration safety; parameterized queries only|M|P0|
|24|COMP-013|MPL DTL adapter|DTL|DM-003, OQ-003|type:repository; store:PostgreSQL15+; writes:userId+eventType+timestamp+ipAddress+userAgent+outcome; non-blocking with retry queue; secret fields scrubbed; retention:12mo; query support:date+user|M|P0|
|25|COMP-INFRA-TLS|Enforce TLS 1.3 on all `/v1/auth/*` endpoints|API Gateway|—|TLS config=1.3-only; HSTS header set; cipher suites restricted; testssl.sh score A+ verified in CI|S|P0|
|26|COMP-XSS-HARDEN|XSS hardening headers (CSP strict-default + HSTS)|API Gateway|—|CSP strict-default; no inline scripts; Report-Only pre-launch; X-Frame=DENY; X-Content=nosniff; upgrade-insecure-requests|S|P0|
|27|COMP-DLP|Secret-scrubbing middleware on logs with allowlist|THS|COMP-013|unit test against known secrets; log processor allowlist; no passwords/tokens/reset-tokens in structured logs; incident runbook if breach detected|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|PST connection pool|DI registry|pg-pool singleton wired into repo layer at app bootstrap|M1|UserRepo, DTL (M2+)|
|Redis client|DI registry|ioredis client singleton with sentinel config loaded at bootstrap|M1|TKN (M2)|
|Config module (bcrypt cost, JWT keys, SendGrid)|Strategy/config registry|env-driven config loader; boot-time VA2 fails-fast on weak config|M1|PSS, JWT, EmailClient (M2)|
|API Gateway → THS|Edge routing|TLS1.3 (COMP-INFRA-TLS), CSP/HSTS (COMP-XSS-HARDEN), CORS allowlist, `/v1/auth/*` route prefix, upstream rate-limit hooks|M1|API-001..010 (M2)|
|AuditEvent enum dispatcher|Dispatch table|`AuthEventType` enum mapped to DTL; phase-tagged for later migration events|M1|DTL, all auth flows (M2)|
|Log scrubbing middleware|Middleware chain|log processor redacts by field-name regex; allowlist centralized|M1|All log writers (M2+)|
|JWT kid resolver|Registry|kid→public-key map loaded at boot; rotation-safe|M1|JWT.verify consumers (M2, gateway)|

### Deliverables — M1

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|OQ-003|Audit retention conflict resolved|12-month retention accepted; TDD updated; sizing recomputed|
|OQ-007 / OQ-008|Hard-gate resolution before M2 freeze|Remember-me and admin scope decisions DCM; downstream contracts frozen|
|DM-001|`users` table migrated with full schema|Migration reversible; all 8 columns present with constraints|
|DM-002|THT CNT DCM|OpenAPI schema reviewed; 4 fields defined; TTLs fixed|
|DM-003|`auth_events` table migrated|Monthly-partitioned; 12mo retention; required fields present|
|DEP-POSTGRES / DEP-REDIS / DEP-NODE / DEP-SENDGRID|Core infra provisioned|Health probes green; secrets in Vault; SBOMs clean|
|NFR-SEC-001 / NFR-SEC-002|Crypto policy frozen|Config tests pass; rotation runbook shipped|
|NFR-COMP-001 / NFR-COMP-003|GDPR gates wired into schema|Consent captured; PII minimized; DPO sign-off|
|COMP-005..009 / COMP-012 / COMP-013|Backend service + module decomposition|Each module independently testable; DI wired|
|COMP-INFRA-TLS / COMP-XSS-HARDEN / COMP-DLP|M1 scaffolding hardening|testssl.sh A+; CSP Report-Only; secret-leak test passes|

### MLS Dependencies — M1

- SEC-POLICY-001 sign-off required before any persistence/crypto decisions.
- PST 15 / Redis 7 / SendGrid / Node.js 20 procurement completed by platform team.
- OQ-003 must be resolved before NC0 sizing and DM-003 finalization.
- OQ-005 must be resolved before COMP-007 Redis key schema is locked.
- OQ-007 and OQ-008 must be closed as hard gates before M2 code freeze (debate convergence).

### MLS Risk Assessment — M1

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|OQ-003 resolution slips past Week 1|Medium|High|Escalate to compliance lead by Day 3; parallel-start audit schema with worst-case 12mo|
|SendGrid sender-domain warming delay|Low|Medium|Begin domain warm-up Week 0 pre-kickoff; AWS SES as degraded fallback|
|Retention/roles/refresh-cap open questions remain ambiguous|Medium|Medium|Hard-gate OQ-002/005/007/008 resolution before M2 freeze; time-box each to ≤3 days|
|RSA key-rotation automation scope creep|Medium|Medium|Ship manual quarterly rotation runbook in M1; automate in M5 (OPS-RSA-ROTATION)|

## M2: Core auth APIs and compliance flows

**Objective:** MPL server-side contracts for login, RGS, profile, refresh, two-step password reset, logout, and admin audit/lock/unlock; wire SOC2 audit logging on all flows; book pen-test vendor. | **Duration:** 2w (Week 3–4) | **Entry:** M1 exit; OQ-007/008 resolved; THS facade signed off; key vault access granted | **Exit:** all 10 `/v1/auth/*` endpoints live with unified error envelope and OpenAPI 3.1 spec; FA0..005 + admin flows pass acceptance tests; pen-test vendor booked with date confirmed

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|OQ-001|Decide API-key auth deferment|Auth boundary|COMP-005|service-to-service auth yes/no decided; v1.0 deferment DCM; non-user path excluded from current APIs; backlog owner assigned|S|P1|
|2|OQ-004|Decide synchronous vs asynchronous reset email delivery|Password reset|FR-AUTH-005|delivery mode decided; <60s delivery target preserved; retry semantics defined; SendGrid integration shape fixed|S|P1|
|3|FA0|MPL login with email/password returning THT|THS|COMP-005, COMP-009, COMP-007, COMP-012, COMP-LOCKOUT|valid creds→200+THT; invalid→401 no enumeration; unknown email→401 constant-time response; 5 failed attempts/15m→423 lockout; audit logged|L|P0|
|4|FR-AUTH-002|MPL validated RGS creating SRP|THS|COMP-005, COMP-009, COMP-012, COMP-VALIDATOR, NFR-COMP-001, NFR-COMP-003|valid→201+SRP; duplicate email→409; weak password(<8,no uppercase,no number)→400; bcrypt cost12 hash stored; consent captured; audit logged|L|P0|
|5|FR-AUTH-003|MPL JWT issuance and refresh-token rotation|TKN|COMP-007, COMP-008, DM-002|login→access(15m)+refresh(7d); POST refresh valid→new THT pair+old revoked atomically; expired→401; revoked→401; audit logged|L|P0|
|6|FR-AUTH-004|MPL authenticated profile retrieval|THS|COMP-005, COMP-012, DM-001|GET /auth/me valid bearer→200+full SRP; expired/invalid token→401; response includes id+email+displayName+createdAt+updatedAt+lastLoginAt+roles|M|P0|
|7|FR-AUTH-005|MPL two-step password reset via email|THS|COMP-005, COMP-RESETTOKEN, COMP-EMAILCLIENT, OQ-004|reset-request→email sent within 60s; reset-confirm→new hash stored + all sessions revoked; token 1h TTL+single-use; unknown email returns 200 no enumeration; audit logged|L|P0|
|8|NFR-PERF-001|Meet p95 latency target across all auth endpoints|THS|FA0, FR-AUTH-002, FR-AUTH-003, FR-AUTH-004, FR-AUTH-005|all auth endpoints p95<200ms; OpenTelemetry tracing on THS methods; hot paths measured; regressions blocked|M|P0|
|9|NFR-PERF-002|Support 500 concurrent logins|THS|FA0, NFR-PERF-001|500 concurrent login requests sustained; k6 scenario defined; p95<200ms; err<0.1%; DB pool saturation<70%|M|P0|
|10|NFR-REL-001|Establish availability controls and SLO|Health/ops|COMP-005|uptime target 99.9%/30d instrumented; health check endpoint live; burn-rate alerts at 2x+5x; synthetic monitor every 1min|M|P0|
|11|NC0|MPL SOC2 audit logging wired into all auth flows|DTL|COMP-013, DM-003|log every login/register/refresh/reset/logout/lock/unlock event; fields userId+timestamp+ipAddress+userAgent+outcome; retention=12mo; queryable by date range and user; SOC2 dry-run evidence export passes|L|P0|
|12|API-001|Deliver POST /auth/login CNT|Login API|FA0|auth:none; rate-limit:10 req/min/IP; request email+password; 200:THT(accessToken+refreshToken+expiresIn900+tokenTypeBearer); errors 401+423+429; unified error envelope|M|P0|
|13|API-002|Deliver POST /auth/register CNT|Register API|FR-AUTH-002, NFR-COMP-001|auth:none; rate-limit:5 req/min/IP; request email+password+displayName+consent; 201:SRP(id+email+displayName+createdAt+updatedAt+lastLoginAt:null+roles[user]); errors 400+409|M|P0|
|14|API-003|Deliver GET /auth/me CNT|Profile API|FR-AUTH-004, COMP-AUTHMW|auth:Bearer accessToken; rate-limit:60 req/min/user; request header Authorization:Bearer; 200:full SRP; errors 401|M|P0|
|15|API-004|Deliver POST /auth/refresh CNT|Refresh API|FR-AUTH-003|auth:none at HTTP layer; rate-limit:30 req/min/user; request refreshToken; 200:new THT pair; expired/revoked refresh→401; old token invalidated atomically|M|P0|
|16|API-005|Deliver POST /auth/reset-request CNT|Reset request API|FR-AUTH-005, OQ-004|auth:none; request email; always 200 generic success no enumeration; email dispatch path fixed via SendGrid; rate-limit 3/hr/IP|M|P1|
|17|API-006|Deliver POST /auth/reset-confirm CNT|Reset confirm API|FR-AUTH-005|auth:none; request token+newPassword; valid token updates bcrypt hash and revokes all sessions; expired/used token 400; validator applied; audit logged|M|P1|
|18|API-007|Deliver POST /auth/logout CNT|Logout API|FR-AUTH-003|auth:Bearer or refresh-bound session identity; session ends immediately; refresh token revoked via TKN; client instructed to clear state; audit logged|M|P1|
|19|API-008|Deliver GET /auth/events admin audit CNT|Admin audit API|NC0, OQ-008|admin-only (role check `admin = ANY(roles)`); filters user+dateRange; response fields userId+eventType+timestamp+ipAddress+outcome; pagination; auth errors defined|M|P1|
|20|API-009|Deliver POST /auth/users/{id}/lock admin lock CNT|Admin lock API|OQ-008, FA0|admin-only; target account lock persisted; lock reason captured; subsequent login blocked with 423; audit logged|M|P1|
|21|API-010|Deliver POST /auth/users/{id}/unlock admin unlock CNT|Admin unlock API|OQ-008, API-009|admin-only; lock cleared; unlock visible in audit log; subsequent valid login allowed|M|P1|
|22|COMP-EMAILCLIENT|MPL SendGrid EmailClient with templated reset emails|EmailClient|DEP-SENDGRID|sendPasswordReset(email,token,locale); retry with exponential backoff (3 attempts); delivery tracking webhook; 60s SLA|M|P0|
|23|COMP-LOCKOUT|MPL account-lockout policy (5 attempts / 15min per email+IP)|THS|COMP-013, DEP-REDIS|failed-attempt counter in Redis keyed on email+window; lock flag after 5/15min; returns 423; auto-unlock after 15min; audit logged|M|P0|
|24|COMP-RESETTOKEN|MPL reset-token issuance (1h TTL, single-use)|TKN|DEP-REDIS, COMP-EMAILCLIENT|issueResetToken(uid)→opaque; 1h TTL in Redis; consumed on first use; subsequent attempts 400; hashed-at-rest|M|P0|
|25|COMP-VALIDATOR|MPL password-strength + email-format validators|THS|—|password: ≥8chr + uppercase + digit per NIST; email: RFC5322 + lowercase normalization; returns typed errors|S|P0|
|26|COMP-AUTHMW|MPL bearer authentication middleware for protected routes|THS|COMP-008|Authorization header parsed; JWT.verify; uid + roles attached to req.ctx; 401 on missing/invalid; admin guard composable|S|P0|
|27|COMP-ERRORENV|MPL unified error envelope `{error:{code:AUTH_*,message,status}}`|THS|—|all 4xx/5xx return envelope; `code` taxonomy DCM; no stack traces to client; error-code registry published|S|P0|
|28|COMP-OPENAPI|Publish OpenAPI 3.1 spec for `/v1/auth/*`|THS|API-001..010|spec validates against OAS 3.1; includes all 10 endpoints, error schemas, examples; served at `/v1/auth/openapi.json`; CI asserts handler-spec parity|S|P1|
|29|COMP-PENTEST-BOOK|Book pen-test vendor by Week 4 with 1w remediation buffer reserved|Security review|R-PRD-004|vendor CNT signed; scope=all 10 endpoints + THP; SOC2-aligned report expected; remediation buffer reserved before GA; booking confirmation on file|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|`/v1/auth/*` router|Dispatch table|login/register/me/refresh/reset-request/reset-confirm/logout/events/lock/unlock handlers mapped to THS + admin services|M2|API-001..010|
|Rate-limit middleware chain|Middleware|per-route limits applied in order: CORS→authMW→rateLimit→handler|M2|All 10 endpoints|
|Bearer auth middleware + admin guard|Middleware|COMP-AUTHMW mounted on protected routes; admin guard on API-008/009/010 via `admin = ANY(roles)` check|M2|API-003, API-007, API-008, API-009, API-010|
|Error envelope handler|Strategy|typed-error→HTTP mapping strategy keyed by error code|M2|All endpoints|
|THS DI container|Dependency injection|THS constructor wires PSS, TKN, UserRepo, DTL, EmailClient, Validator via container|M2|All API handlers|
|THS → TKN → JWT chain|Service chain|verify password, issue pair, rotate refresh, sign/verify JWT|M2|FA0, FR-AUTH-003, API-001, API-004, API-007|
|THS → SendGrid via BullMQ|Callback wiring|reset token generation, template render, delivery dispatch, failure surfacing|M2|FR-AUTH-005, API-005|
|THS/admin handlers → DTL|Event binding|success/failure/logout/lock/unlock events persisted with IP + outcome|M2|NC0, API-007, API-008, API-009, API-010|
|Lockout counter key schema|Registry|Redis key template `lockout:{email}:{window}` registered centrally|M2|FA0, COMP-LOCKOUT|

### Deliverables — M2

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|FA0|Login flow implementation|Generic on failure; enumeration-safe; canonical token pair on success|
|FR-AUTH-005|Two-step reset flow|Privacy-preserving; TTL and session-invalidation semantics correct|
|API-001..010|10 REST endpoints live|All status codes correct; rate limits enforced; unified error envelope|
|API-008|Admin event-query API|Jordan can query audit records by user + date range with stable response fields|
|API-009 / API-010|Administrative lock/unlock|Admin-triggered lockout prevents future logins; audit trail created|
|NC0|SOC2-grade event logging on all flows|12-month retention; required fields; SOC2 dry-run export passes|
|COMP-EMAILCLIENT / COMP-LOCKOUT / COMP-RESETTOKEN / COMP-VALIDATOR|Domain services complete|Unit + integration test green; enumeration-safe; hashed-at-rest|
|COMP-AUTHMW / COMP-ERRORENV|Auth middleware + error envelope|Admin guard composable; no stack traces to client|
|COMP-OPENAPI|OpenAPI 3.1 spec|Linter passes; CI asserts handler-spec parity|
|COMP-PENTEST-BOOK|Pen-test booked by W4|Vendor CNT signed; remediation buffer reserved|

### MLS Dependencies — M2

- M1 complete (contracts frozen; OQ-007/008 closed; crypto modules ready).
- SendGrid provisioned + templates approved by product + legal.
- API Gateway team pre-booked for rate-limit + CORS rule deployment.
- Pen-test vendor shortlist qualified during M1 to enable W4 booking.

### MLS Risk Assessment — M2

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Reset delivery mode (sync/async) chosen too late|Medium|Medium|Freeze OQ-004 before email integration and API error CNT stabilize|
|Admin-control scope expands uncontrolled|Medium|High|Limit v1.0 admin surface to audit + lock + unlock only; exclude RBAC and broader user management|
|Performance target missed after compliance logging added|Medium|High|Instrument audit path early; async + retry queue; benchmark p95 before M3 handoff|
|Pen-test vendor booking slips past W4|Medium|High|Qualify shortlist during M1; book earliest available slot; keep internal security review as degraded fallback|
|Password-reset email enumeration leak via timing or response|Medium|High|Constant-time response path; always 200; timing tests deferred to M3 TEST-SEC-ENUMERATION|

## M3: Client integration, admin gaps, and QA with pre-merge test gates

**Objective:** Wire THP, deliver core user journeys (Alex/Sam) + admin journey (Jordan), and prove correctness across unit/integration/E2E/load/security layers with pre-merge coverage gate and pre-merge NFR gates. | **Duration:** 2w (Week 5–6) | **Entry:** M2 APIs stable and testable in staging | **Exit:** golden-path + admin journeys verified end-to-end; CI 80/15/5 coverage gate green; TEST-IMPLICIT-LOAD nightly k6 passes; TEST-SEC-ENUMERATION/LOCKOUT green; pre-merge bcrypt + RS256 config VA2 tests fail-fast on weak config

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|COMP-001|MPL LoginPage at `/login`|LoginPage|API-001, COMP-004|type:frontend page route; auth:none; props:onSuccess()+redirectUrl?; form email+password; inline VA2; generic error on 401; CAPTCHA after 3 fails (R-002); stores THT via THP|M|P0|
|2|COMP-002|MPL RegisterPage at `/register`|RegisterPage|API-002, COMP-004, NFR-COMP-001|type:frontend page route; auth:none; props:onSuccess()+termsUrl; form email+password+displayName+consent; password strength meter; consent checkbox required; duplicate→inline 409 hint; submit→logged in+redirect dashboard|M|P0|
|3|COMP-003|MPL ProfilePage at `/profile`|ProfilePage|API-003, COMP-004|type:frontend page route; auth:required; pulls full SRP; renders id+email+displayName+createdAt+updatedAt+lastLoginAt+roles; loading state <1s; 401 triggers silent refresh then re-fetch|M|P1|
|4|COMP-004|MPL THP React context|THP|API-001, API-003, API-004, API-007, OQ-007|type:React context provider; accessToken in memory only (R-001); refreshToken in HttpOnly cookie; 401 triggers silent refresh via API-004; unauth users redirected to `/login`; clears state on logout/tab-close policy; remember-me behavior aligned with OQ-007 resolution|L|P0|
|5|COMP-010|MPL LogoutControl|Logout UX|API-007, COMP-004|visible logout action in header; triggers immediate session termination; clears client auth state; calls API-007 to revoke refresh token; redirects to landing/login|M|P1|
|6|COMP-011|MPL AdminAuditPage|Admin audit UI|API-008, OQ-008|admin view lists auth events; filters by user/date range; shows userId+eventType+timestamp+ipAddress+outcome; access restricted to admins (role gate); Jordan JTBD validated|M|P1|
|7|COMP-FE-RESET-REQ|MPL forgot-password page (calls API-005)|LoginPage|API-005|always shows confirmation no enumeration; email input validated; 60s client-side throttle|S|P0|
|8|COMP-FE-RESET-CONF|MPL reset-confirmation page (token from URL, calls API-006)|LoginPage|API-006|token parsed from URL query; new-password form with strength meter; success→redirect to `/login` with toast; expired→clear message + link to request new|M|P0|
|9|PRD-JOURNEY-FIRSTSIGNUP|VLD PRD S22 first-time-signup journey end-to-end|THP + COMP-002|COMP-002, COMP-004|land→signup→dashboard ≤2s; inline VA2 during entry; usability test with 5 users (R-PRD-001 mitigation); funnel analytics wired from Day 1|S|P0|
|10|PRD-JOURNEY-SESSIONPERSIST|VLD PRD S22 returning-user session persistence|THP|COMP-004|silent refresh triggers without re-login; >7d idle→clear re-login prompt; cross-device login confirmed|S|P0|
|11|TEST-001|Unit: login with valid creds returns THT|THS test|FA0|THS.login calls PSS.verify then TKN.issueTokens; returns THT with both tokens; success path audited; Jest + ts-jest|S|P0|
|12|TEST-002|Unit: login with invalid creds returns 401|THS test|FA0|returns 401 when verify()=false; no THT issued; no enumeration; mocks assert single call to verify|S|P0|
|13|TEST-003|Unit: token refresh with valid refresh token|TKN test|FR-AUTH-003|refresh() validates→revokes old→issues new pair; old key absent in Redis after call; audit logged|S|P0|
|14|TEST-004|Integration: RGS persists SRP to PST|THS + PST test|FR-AUTH-002, DM-001|Supertest + testcontainers; POST /register→201; DB row with correct hash (bcrypt cost=12); consent_accepted_at not null; duplicate email blocked|M|P0|
|15|TEST-005|Integration: expired refresh token rejected by TKN + Redis|Token + Redis test|FR-AUTH-003, DM-002|insert refresh token with 1s TTL; wait 2s; refresh()→401; audit event logged; no replacement pair issued|S|P0|
|16|TEST-006|E2E: user registers, logs in, sees profile (Playwright)|RegisterPage + LoginPage + ProfilePage|FA0, FR-AUTH-002, COMP-004|full journey landing→register→profile; silent token refresh works; feature-flag-enabled path; Chromium/Firefox/WebKit matrix|M|P0|
|17|TEST-IMPLICIT-BCRYPT|Pre-merge: assert bcrypt cost parameter (NFR-SEC-001)|PSS|NFR-SEC-001|parse produced hash header; assert cost==12; negative test with cost=10 fails; boot-time config VA2 fails-fast|S|P0|
|18|TEST-IMPLICIT-RS256|Pre-merge: config VA2 RS256 + 2048-bit RSA (NFR-SEC-002)|JWT|NFR-SEC-002|JWT boot asserts alg==RS256 and key modulus≥2048; fails-fast if weak config|S|P0|
|19|TEST-IMPLICIT-LOAD|Nightly k6 load scenario at 500 concurrent (NFR-PERF-002)|THS|NFR-PERF-002|scripted scenario committed in repo; CI runs against staging nightly; p95<200ms; error<0.1%; fails pipeline on regression|M|P0|
|20|TEST-IMPLICIT-AUDIT|Integration: audit event emitted for every auth flow (NC0)|DTL|NC0|10 flows × 2 outcomes each = 20 scenarios; assert event row with required fields exists in 12mo partition|M|P0|
|21|TEST-SEC-ENUMERATION|Security: no user enumeration on login/reset-request|THS|API-001, API-005|timing-parity test (±10ms) across registered/unregistered email; response body identical; response headers identical|S|P0|
|22|TEST-SEC-LOCKOUT|Integration: account locks after 5 attempts/15min|THS|COMP-LOCKOUT|5 failed attempts→423; 6th→423; after 15min→200 with correct creds; audit rows present|S|P0|
|23|TEST-COVERAGE-GATE|Pre-merge CI coverage gate 80/15/5|CI pipeline|TEST-001..006, TEST-IMPLICIT-*, TEST-SEC-*|PR blocked if coverage drops below 80% unit / 15% integration / 5% E2E; enforced by GitHub Actions; testcontainers parallelized <15min|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|App root → THP|Context/provider wiring|global auth state, refresh lifecycle, protected-route redirect behavior|M3|COMP-001, COMP-002, COMP-003, COMP-010, COMP-011|
|Public/Protected route registry|Route binding|`/login`, `/register`, `/forgot-password`, `/reset-confirm` public; `/profile`, admin routes protected|M3|COMP-001, COMP-002, COMP-003, COMP-011|
|React router guard `<ProtectedRoute>`|Middleware|wraps routes behind THP.isAuthenticated; admin guard on AdminAuditPage|M3|COMP-003, COMP-011|
|Axios/fetch interceptor|Event binding|401 → silent refresh via TKN → retry original; single-flight promise prevents races|M3|All authenticated API calls|
|ANL flag consumer|Feature flag registry|LaunchDarkly/config reader checked at route mount|M3|LoginPage, RegisterPage|
|Token storage strategy|Strategy pattern|access=in-memory / refresh=HttpOnly cookie; swappable for future session mode|M3|THP|
|CAPTCHA provider adapter|Strategy|Recaptcha v3 wrapper with feature-flag fallback|M3|LoginPage|
|CI test-tier matrix|Dispatch table|GitHub Actions job map: unit/integration/e2e/load/security|M3|PR gating|
|Testcontainers registry|Registry|ephemeral PST + Redis per integration run|M3|TEST-004, TEST-005, TEST-IMPLICIT-AUDIT|
|k6 nightly runner|Strategy|nightly load run against staging; dedicated tenancy; synthetic accounts only|M3|TEST-IMPLICIT-LOAD, NFR monitoring|
|Playwright test projects|Strategy|Chromium/Firefox/WebKit matrix|M3|TEST-006, PRD-JOURNEY-*|
|Coverage threshold gate|Middleware|fails PR if coverage drops below 80/15/5|M3|PR gating|

### Deliverables — M3

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|COMP-004|Shared authentication provider|Client state, refresh, redirect, logout behavior centralized and deterministic|
|COMP-001 / COMP-002 / COMP-003|Login/Register/Profile pages|Visual QA pass; a11y WCAG 2.1 AA|
|COMP-FE-RESET-REQ / COMP-FE-RESET-CONF|Reset flow UI|Token round-trip works; enumeration-safe|
|COMP-010|Logout control|Token cleared + revocation called via API-007|
|COMP-011|Admin incident visibility UI|Jordan can inspect audit activity without direct DB access|
|PRD-JOURNEY-FIRSTSIGNUP / PRD-JOURNEY-SESSIONPERSIST|Journey map VA2|≤2s signup; seamless cross-device refresh|
|TEST-001..006|Core TDD-specified test cases|Covers FA0..005 + end-to-end|
|TEST-IMPLICIT-BCRYPT / TEST-IMPLICIT-RS256|Pre-merge NFR-SEC gates|Boot fails-fast on weak config; PR blocked|
|TEST-IMPLICIT-LOAD|Nightly k6 load suite|p95<200ms; CI regression gate|
|TEST-IMPLICIT-AUDIT|Audit coverage integration|20 scenarios green|
|TEST-SEC-ENUMERATION / TEST-SEC-LOCKOUT|Security hardening tests|Timing parity ±10ms; lockout enforced|
|TEST-COVERAGE-GATE|Pre-merge coverage gate|80/15/5 enforced by CI|

### MLS Dependencies — M3

- Frontend routing framework supports protected-route redirects and shared context providers.
- Browser E2E coverage depends on stable reset, login, and profile APIs from M2.
- Remember-me behavior constrained to product/security decision from OQ-007.
- k6 runner or Grafana Cloud k6 account configured before TEST-IMPLICIT-LOAD.
- CAPTCHA keys procured (R-002 mitigation).

### MLS Risk Assessment — M3

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|THP race condition during concurrent silent refresh|Medium|High|Single-flight refresh promise; property-based tests; replay harness|
|AccessToken inadvertently persisted to localStorage (XSS, R-001)|Medium|High|ESLint rule forbidding localStorage.setItem for auth; code review gate|
|Admin views leak excessive auth data|Low|High|Limit fields to userId + eventType + timestamp + IP + outcome; admin-only access enforced at middleware + UI|
|Flaky E2E tests block CI|Medium|Medium|Quarantine lane for flaky tests; mandatory 48h triage SLA|
|k6 environment not isolated from real users|Low|High|Dedicated staging tenancy; rate-limit k6 IPs; synthetic test accounts only|
|Poor RGS UX tanks conversion (R-PRD-001)|Medium|High|Pre-launch usability testing with 5 users; funnel analytics wired Day 1|

## M4: Rollout, migration safety, and observability

**Objective:** Execute three-phase rollout with feature flags, parallel-run against legacy auth, pre-phase backups, named rollback triggers, observability stack, pen-test completion, and success-criteria VA2. | **Duration:** 3w (Week 7–9) | **Entry:** M3 exit (tests green, coverage gate active); pen-test booked per COMP-PENTEST-BOOK; 7-day clean burn in staging | **Exit:** 100% GA; 99.9% uptime first 7 days; flags removed; legacy decommissioned; pen-test critical/high = 0 open

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|MIG-001|Execute internal alpha rollout|Rollout|M2, M3|duration:1w; staging deploy complete; auth-team+QA enabled via ANL; FA0..005 + admin flows manual pass; zero P0/P1 bugs; audit logs flowing|M|P0|
|2|MIG-002|Execute 10% beta rollout|Rollout|MIG-001, NFR-PERF-001, NFR-PERF-002|duration:2w; ANL enabled for 10% traffic; p95<200ms; error rate<0.1%; zero TKN Redis connection failures; rollback triggers armed|L|P0|
|3|MIG-003|Execute 100% GA rollout|Rollout|MIG-002|duration:1w overlapping W9; all users routed to new THS; ANL removed; AUTH_TOKEN_REFRESH enabled then removed +2w stability; 99.9% uptime first 7d|L|P0|
|4|MIG-FLAG-LOGIN|Provision ANL feature flag (default OFF)|THP, THS|LaunchDarkly|flag registered in LD; targeting rules (internal/beta/all); flag referenced in gateway, THS, frontend; removal backlog item created|S|P0|
|5|MIG-FLAG-REFRESH|Provision AUTH_TOKEN_REFRESH feature flag (default OFF → ON in MIG-003)|TKN|LaunchDarkly|when OFF only access tokens issued; when ON refresh pair issued; remove flag M5 after 2w stability|S|P0|
|6|MIG-DATAMIG-BACKUP|Full PST backup immediately before each phase|PST|DEP-POSTGRES|pg_basebackup + WAL archive per phase; restore tested in staging; backup retained ≥30 days|S|P0|
|7|MIG-DUAL-RUN|Parallel-run with legacy auth during Phases 1–2 with divergence monitor|THS|MIG-FLAG-LOGIN|legacy + new both live; idempotent upsert on SRP prevents dup rows; nightly divergence metric alerts on >0.1% drift; block MIG-003 if drift present|L|P0|
|8|MIG-002-ROLLBACK|Rollback triggers + automation for MIG-002|THS|MIG-002|trigger: p95>1000ms/5min OR err>5%/2min OR Redis conn failures>10/min OR SRP corruption; auto-disable flag via LD API; PagerDuty page; require 2 consecutive windows before auto-disable|M|P0|
|9|MIG-ROLLBACK-RUNBOOK|Documented 6-step rollback procedure (TDD §19.3) tabletop-exercised|THS|MIG-002|steps: disable flag→smoke test legacy→root-cause THS→restore SRP if corrupted→notify teams→post-mortem ≤48h; tabletop exercised before MIG-002|S|P0|
|10|MIG-LEGACY-DEPRECATE|Decommission legacy auth endpoints after MIG-003|Legacy auth svc|MIG-003|2-week deprecation window; monitoring shows <1% traffic; shutdown coordinated with platform-team; DB rows archived; legacy endpoints return 410 Gone with migration instructions|M|P1|
|11|MIG-FLAG-REMOVE|Remove both feature flags after stability proven|THS|MIG-003|ANL removed immediately post MIG-003; AUTH_TOKEN_REFRESH removed MIG-003+2w; CI asserts flag absence|S|P1|
|12|COMP-METRICS|Prometheus metrics emitter (counters + histograms)|THS|OPS-005|`auth_login_total{outcome}`, `auth_login_duration_seconds`, `auth_token_refresh_total{outcome}`, `auth_registration_total`; Grafana dashboard template as-code|M|P0|
|13|COMP-TRACING|OpenTelemetry distributed tracing across THS→PSS→TKN→JWT|THS|COMP-METRICS|spans linked; trace ids propagated from gateway; sampling 10% default, 100% on error; Tempo/Jaeger target|M|P0|
|14|COMP-ALERTS|Alert rules in Alertmanager|THS|COMP-METRICS|login failure >20%/5min; p95 >500ms; Redis conn failures >10/min; oncall paged P1; alert runbook linked; burn-rate alerts at 2x+5x|M|P0|
|15|COMP-CORS|CORS allowlist at API Gateway restricted to known frontend origins|API Gateway|—|allowlist=[staging,prod frontend FQDNs]; credentials=true only for allowlisted; preflight cached 24h|S|P0|
|16|COMP-PENTEST|External penetration test and findings remediation (R-PRD-004)|THS|COMP-PENTEST-BOOK, M3 complete|vendor engaged; scope=all 10 endpoints + THP; SOC2-aligned report; all Critical/High remediated pre-GA; 1w remediation buffer reserved|L|P0|
|17|R-001|Mitigate token theft via XSS|Security|COMP-004, FR-AUTH-003|accessToken stored in memory only; refreshToken HttpOnly cookie; THP clears tokens on tab close per policy; immediate revocation path available; CSP strict-default from COMP-XSS-HARDEN|L|P0|
|18|R-002|Mitigate brute-force attacks|Security|API-001, FA0|gateway rate limit 10 req/min/IP; account lockout after 5 failed attempts/15m; bcrypt cost12 active; CAPTCHA after 3 fails in COMP-001; WAF block contingency DCM|L|P0|
|19|R-003|Protect legacy-auth migration data|Migration safety|MIG-001, MIG-002|parallel run in phases 1–2; idempotent SRP upserts; full DB backup before each phase; restore procedure tested; divergence monitor armed|M|P0|
|20|R-PRD-001|Counter poor RGS UX adoption|Product risk|COMP-002, MIG-002|usability testing pre-launch complete (PRD-JOURNEY-FIRSTSIGNUP); funnel instrumentation enabled; iterate on drop-off findings; conversion target ownership assigned|M|P1|
|21|R-PRD-002|Prevent compliance failure from incomplete logs|Compliance risk|NC0, OPS-005|log field set mapped to SOC2 controls; QA VA2 complete; 12-month retention confirmed; missing-event audit passes SOC2 dry-run|M|P0|
|22|R-PRD-003|Detect email delivery failures|Operational risk|API-005, OPS-005|SendGrid delivery monitoring and alerts live; reset email SLA tracked; fallback support channel DCM in OPS-002|M|P1|
|23|R-PRD-004|Run dedicated security review gate|Security review|COMP-PENTEST|dedicated security review complete; pen-test before production complete; critical findings resolved or rollout blocked; SOC2 auditor preview passes|L|P0|
|24|SC-001|VLD login latency target|VA1|API-001, OPS-005|metric:login p95; target<200ms; method:APM tracing; milestone admission:beta+GA|M|P0|
|25|SC-002|VLD RGS success rate|VA1|API-002, OPS-005|metric:RGS success; target>99%; method:API analytics; failures triaged|M|P1|
|26|SC-003|VLD refresh latency target|VA1|API-004, OPS-005|metric:refresh p95; target<100ms; method:APM tracing on refresh path; regressions blocked|M|P0|
|27|SC-004|VLD availability target|VA1|NFR-REL-001, OPS-005|metric:uptime; target≥99.9% over 30d; method:health-check monitoring; alert route tested|M|P0|
|28|SC-005|VLD hash-time target|VA1|NFR-SEC-001|metric:PSS.hash(); target<500ms at cost12; method:benchmark test; drift blocked|S|P0|
|29|SC-006|VLD RGS conversion|VA1|R-PRD-001|metric:funnel conversion; target>60%; method:landing→register→confirmed funnel; review cadence defined|M|P1|
|30|SC-007|VLD authenticated DAU growth|VA1|MIG-003|metric:daily active authenticated users; target>1000 within 30d GA; method:THT issuance analytics; trend review scheduled|M|P1|
|31|SC-008|VLD average session duration|VA1|API-004, COMP-004|metric:avg session duration; target>30m; method:token-refresh analytics; UX regressions investigated|M|P1|
|32|SC-009|VLD failed-login rate|VA1|API-001, NC0|metric:failed login rate; target<5% attempts; method:auth event log analysis; spikes alert|M|P1|
|33|SC-010|VLD password-reset completion|VA1|API-005, API-006, R-PRD-003|metric:reset completion; target>80%; method:reset funnel analysis; delivery failures correlated|M|P1|
|34|SC-011|VLD phase-2 beta exit gate|VA1|MIG-002|metric:p95<200ms + err<0.1% + zero Redis failures over 2 weeks at 10% traffic; method:staged rollout telemetry; exit signoff recorded|M|P0|
|35|SC-012|VLD 500 concurrent login throughput|VA1|NFR-PERF-002, TEST-IMPLICIT-LOAD|metric:500 sustained concurrent requests; p95<200ms; err<0.1%; method:k6 load test against login path|M|P0|

### Integration Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|LaunchDarkly SDK|Registry|initialized in both frontend and backend at bootstrap; flag cache 30s|M4|THP, THS, MIG-001..003|
|Feature flag registry|Registry|ANL and AUTH_TOKEN_REFRESH staged enablement, disablement, and removal|M4|MIG-001, MIG-002, MIG-003, OPS-002|
|Legacy/new dispatcher at gateway|Dispatch table|flag-based routing: ANL on→/v1/auth/*, off→/legacy/auth/*|M4|API Gateway|
|Rollback automation|Event binding|alert payload → LD API (disable flag) → PagerDuty → incident channel|M4|MIG-002-ROLLBACK, on-call, SRE|
|Data-parity divergence monitor|Event binding|nightly job compares SRP rows between legacy+new stores; alert on >0.1% drift|M4|MIG-DUAL-RUN, SRE, compliance|
|Prometheus scrape target|Registry|`/metrics` endpoint exposed; ServiceMonitor CR|M4|COMP-METRICS, Grafana dashboards|
|OTLP exporter|Event binding|traces→collector→Tempo/Jaeger|M4|COMP-TRACING, SRE/on-call|
|Alertmanager routes|Dispatch table|severity→team-specific on-call routing|M4|COMP-ALERTS, PagerDuty/Opsgenie|
|Audit event taxonomy (migration_phase)|Dispatch table|eventType extended with phase tag for rollout analysis|M4|Post-mortem analysis, SC-011|
|Monitoring stack → alert routes|Event binding|latency, failure-rate, Redis, uptime, and delivery alerts routed to on-call|M4|COMP-ALERTS, SC-001, SC-004, SC-011|
|Analytics pipeline|Reporting pipeline|RGS, session, failed-login, and reset funnels recorded for business VA2|M4|SC-002, SC-006..010|
|Backup/restore automation|Operational wiring|pre-phase backup, restore rehearsal, corruption contingency path|M4|MIG-DATAMIG-BACKUP, R-003|

### Deliverables — M4

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|MIG-001 / MIG-002 / MIG-003|Three-phase rollout executed|Exit criteria met at each phase; 99.9% uptime first 7d GA|
|MIG-FLAG-LOGIN / MIG-FLAG-REFRESH|Feature flags provisioned|Targeting rules defined; DCM removal dates|
|MIG-DATAMIG-BACKUP|Pre-phase backups + restore tested|Backups retained ≥30d|
|MIG-DUAL-RUN|Parallel run with legacy|Idempotent; divergence alert armed; drift blocks MIG-003|
|MIG-002-ROLLBACK / MIG-ROLLBACK-RUNBOOK|Rollback automation + runbook|Tabletop exercised; triggers armed|
|MIG-LEGACY-DEPRECATE / MIG-FLAG-REMOVE|Cleanup complete|Legacy 410 Gone; flags removed|
|COMP-METRICS / COMP-TRACING / COMP-ALERTS|Observability stack live|Dashboards + pager routes in production|
|COMP-CORS|Gateway CORS allowlist|Only known origins accepted|
|COMP-PENTEST|Pen-test complete|Critical/High = 0 open; SOC2-aligned report on file|
|R-001..003, R-PRD-001..004|Release-gate risk mitigations|Each risk ownership + verification evidence recorded|
|SC-001..012|Success-criteria VA2|Targets met or explicit variance signed off|

### MLS Dependencies — M4

- R-003 data-loss mitigation implemented (idempotent upserts, per-phase backup, divergence monitor).
- LaunchDarkly account + SDK quotas sufficient for frontend + backend.
- Pen-test vendor executing per COMP-PENTEST-BOOK timeline; 1w remediation buffer reserved.
- Incident channel + PagerDuty rotation staffed 24/7 for first 2 weeks of GA.
- SOC2 auditor preview booked for MIG-002 exit signoff.

### MLS Risk Assessment — M4

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|R-003 data loss during legacy→new migration|Medium|High|Parallel run + idempotent upserts + pre-phase backups + tabletop rollback + divergence monitor|
|Silent data divergence between legacy and new stores|Medium|High|Nightly divergence monitor; alert on >0.1% drift; block MIG-003 if drift present|
|Rollback trigger fires false-positive at 3AM|Medium|Medium|Burn-rate windows tuned with M3 baseline; require 2 consecutive windows before auto-disable|
|Pen-test surfaces critical finding late|Medium|Critical|Pre-M4 "light" review; 1w remediation buffer reserved; block GA on unresolved Critical/High|
|Observability misses compliance-critical events|Medium|High|VLD event coverage against SOC2-required fields before MIG-002 signoff|
|Alert fatigue from false positives|Medium|Low|Tune thresholds with 2w dry-run in staging before PagerDuty wiring|
