<!-- CONV: AuthService=THS, TokenManager=TKN, AuthProvider=THP, Milestone=MLS, PasswordHasher=PSS, retention=RTN, JwtService=JWT, endpoints=NDP, PostgreSQL=PST, UserProfile=SRP, auth-team=AT, rotation=RTT, Integration=NTG, FR-AUTH-001=FA0, compliance=CMP, Dependencies=DPN, AUTH_NEW_LOGIN=ANL, registration=RGS, AUTH_TOKEN_REFRESH=ATR, Deliverables=DLV -->
---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service delivers the platform's first secure, self-service identity layer: RGS, login, JWT-based session persistence, profile retrieval, and self-service password reset. The capability unblocks ~$2.4M of projected 2026 personalization revenue (PRD S5), satisfies the Q3 2026 SOC2 Type II audit dependency on authenticated event logging, and replaces a support path that is consuming 30% QoQ more access tickets. The roadmap is organized as 8 architectural milestones (16 weeks total) sequenced to front-load security-critical foundations (bcrypt, RS256, audit logging) before the phased 10%→100% rollout governed by `ANL` and `ATR` feature flags.

**Business Impact:** Unblocks personalization roadmap for Q2–Q3 2026 (PRD S5); enables SOC2 Type II audit trail (PRD S17 + COMPLIANCE-001); reduces access-issue support volume (30% QoQ growth cited in PRD S4); targets RGS conversion >60%, login p95 <200ms, failed-login <5%, password-reset completion >80% (PRD S19 + TDD §4.1–4.2).

**Complexity:** HIGH (0.72) — driven by six cross-cutting domains (backend/security/frontend/testing/devops/CMP), authentication-level security criticality (bcrypt cost 12, RS256, refresh-token revocation, account lockout, XSS hardening), five external integrations (PST 15, Redis 7, SendGrid, API Gateway, frontend `THP`), and a three-phase rollout with parallel-run against legacy auth. Mitigating factors: bounded 4-endpoint API surface, no MFA/OAuth/RBAC in v1.0, single greenfield service rather than cross-system refactor.

**Critical path:** Security policy reconciliation (OQ-003 12-month audit RTN) → infrastructure (PST 15, Redis 7, SendGrid) → core crypto primitives (`PSS`, `JWT`, `TKN`) → `THS` orchestrator → REST API surface → frontend `THP` + pages → audit/CMP wiring → test pyramid → MIG-001 internal alpha → MIG-002 10% beta → MIG-003 100% GA → operational handover. A stop-the-line blocker exists at OQ-003 (RTN conflict) which must resolve before NFR-COMP-002 can be implemented.

**Key architectural decisions:**

- **Stateless `THS` + Redis-backed refresh tokens:** Access tokens are stateless JWTs (RS256, 15-min TTL); refresh tokens are hashed opaque values in Redis with 7-day TTL. Enables horizontal scale (HPA 3→10 pods) and immediate refresh revocation (Decision Summary row 1).
- **Bcrypt cost factor 12 behind `PSS` abstraction:** Meets NIST SP 800-63B (PRD S17) and enables future algorithm migration (Argon2) without rewriting call sites (Decision Summary row 2).
- **Three-phase rollout with two feature flags:** `ANL` (login/register gate) and `ATR` (refresh-token gate) enable 10% canary at MIG-002 with named rollback triggers (p95>1000ms, error>5%, Redis failures>10/min) — chosen over big-bang cutover given R-003 data-loss severity.
- **Audit logging written on all auth events with 12-month RTN:** Reconciles TDD §7.2 (90-day) with PRD S17 SOC2 (12-month) in favor of PRD per OQ-003; implemented as an append-only partitioned table with monthly RTT.
- **API surface versioned under `/v1/auth/*`:** Supports additive non-breaking evolution (MFA in v1.1, OAuth in v2.0) without destabilizing the `THP` client.

**Open risks requiring resolution before M1:**

- OQ-003 audit RTN conflict (90-day TDD vs 12-month PRD/SOC2) — blocks NFR-COMP-002 scope, storage sizing, and partitioning strategy. Owner: CMP + AT. Target: before M1 exit.
- OQ-005 refresh-token-per-user cap — affects Redis capacity planning (OPS-004) and `TKN` data model. Owner: Product. Target: before M2 TKN design.
- PRD S21 admin story (Jordan view event logs / lock-unlock) lacks TDD functional requirement coverage (OQ-008) — either descope or add FR-AUTH-006 admin API surface before M3.
- R-PRD-004 security breach risk (critical) — pen-test scheduling and SEC-POLICY-001 sign-off must be booked before M2.

## MLS Summary

|ID|Title|Type|Priority|Effort|DPN|DLV|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation, Data Models & Compliance Policy|Foundation|P0|2w|SEC-POLICY-001; OQ-003 resolved|14|High|
|M2|Core Auth Primitives (THS + Crypto)|Backend|P0|2w|M1|10|High|
|M3|REST API Surface & Functional Flows|Backend/API|P0|2w|M2|14|Medium|
|M4|Frontend Components & THP Wiring|Frontend|P0|2w|M3|9|Medium|
|M5|Non-Functional, Compliance & Observability|Cross-cutting|P0|2w|M3, M4|13|High|
|M6|Testing Pyramid (Unit/NTG/E2E/Load)|Quality|P0|2w|M4, M5|12|Medium|
|M7|Migration, Feature Flags & Phased Rollout|Release|P0|3w|M5, M6|11|High|
|M8|Operational Readiness & Runbook Handover|Ops|P1|1w|M7|8|Low|

## Dependency Graph

```
M1 (Foundation) → M2 (Core Primitives) → M3 (API) → M4 (Frontend)
                                       ↘
M1 ─────────────────────────────────→ M5 (NFR/Compliance/Observability)
                                                         ↘
M3, M4, M5 ──────────────────────────────────────────→ M6 (Testing)
                                                                  ↘
M5, M6 ─────────────────────────────────────────────────────→ M7 (Rollout)
                                                                         ↘
                                                                      M8 (Ops Handover)

External inputs: PostgreSQL 15 → M1; Redis 7 → M2; SendGrid → M3;
                 API Gateway → M5; SEC-POLICY-001 → M1; OQ-003 resolution → M1.
```

## M1: Foundation, Data Models & Compliance Policy

**Objective:** Stand up persistence, caching, and CMP substrate. Finalize DM-001/DM-002 schema and resolve OQ-003 RTN conflict. | **Duration:** 2w (Week 1–2) | **Entry:** SEC-POLICY-001 signed off; PST 15 and Redis 7 provisioned | **Exit:** DM-001/DM-002 migrated; audit log partition strategy approved; OQ-003 resolved in favor of 12-month RTN

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|OQ-003|Resolve audit RTN conflict (90d vs 12mo) in favor of PRD 12-month SOC2|THS|SEC-POLICY-001|decision doc signed by CMP+AT; TDD §7.2 updated; RTN=12mo; storage sizing recomputed|S|P0|
|2|DM-001|Provision `users` table for SRP with full field schema|PST|OQ-003|id:UUID-PK-NN; email:varchar-UNIQUE-NN-idx-lowercase; display_name:varchar-NN-2to100; password_hash:varchar-NN; created_at:timestamptz-NN-DEFAULTnow(); updated_at:timestamptz-NN-auto; last_login_at:timestamptz-nullable; roles:text[]-NN-DEFAULT'{"user"}'|M|P0|
|3|DM-002|Design AuthToken contract (accessToken JWT + refreshToken Redis)|TKN|DM-001|accessToken:JWT-RS256-NN-payload{uid,roles}; refreshToken:opaque-NN-unique-Redis-7dTTL-hashedAtRest; expiresIn:number-NN-900; tokenType:string-NN-"Bearer"|M|P0|
|4|COMP-DM-AUDIT|Create `auth_events` append-only audit log table (12-month RTN)|PST|OQ-003, DM-001|user_id:UUID-FK-nullable; event_type:enum-NN; ip:inet-NN; user_agent:text; outcome:enum-NN; created_at:timestamptz-NN-idx; monthly-partitioned; RTN=12mo|M|P0|
|5|DEP-POSTGRES|Install and configure PST 15 cluster with read replica|Infrastructure|—|version≥15; connection pool=100; multi-AZ replica; backup schedule=nightly+WAL|M|P0|
|6|DEP-REDIS|Install and configure Redis 7 cluster (HA)|Infrastructure|—|version≥7; cluster mode; 1GB baseline; HA+failover; TLS at rest|M|P0|
|7|DEP-NODE|Standardize Node.js 20 LTS build image|Infrastructure|—|Dockerfile base=node:20-LTS; SBOM generated; CVE scan=0 high|S|P0|
|8|DEP-SENDGRID|Procure and configure SendGrid account + sender domain|Infrastructure|—|API key in vault; SPF/DKIM/DMARC records set; delivery domain warmed|M|P0|
|9|NFR-SEC-001-SCAFFOLD|Define bcrypt config abstraction (cost=12)|PSS|DEP-NODE|config module exposes cost parameter; unit test asserts cost==12; dependency=bcryptjs pinned|S|P0|
|10|NFR-SEC-002-SCAFFOLD|Define RS256 key management + RTT policy|JWT|DEP-NODE|2048-bit RSA keypair generated; kid header set; RTT=quarterly documented; private key in HashiCorp Vault|M|P0|
|11|NFR-COMP-001|GDPR consent-at-RGS storage column + policy|DM-001|DM-001|consent_accepted_at:timestamptz-NN; consent_version:varchar; RGS rejected if unchecked; log consent event|S|P0|
|12|NFR-COMP-002|SOC2 audit-log schema and RTN enforcement|COMP-DM-AUDIT|COMP-DM-AUDIT|all auth events logged; fields=user_id+timestamp+ip+outcome; RTN=12mo; partition drop job scheduled|M|P0|
|13|NFR-COMP-003|Data minimization contract — reject extra PII fields at RGS|THS|DM-001|RGS schema whitelist={email,password,displayName,consent}; extra fields rejected 400; DPO sign-off|S|P0|
|14|COMP-INFRA-TLS|Enforce TLS 1.3 on all `/v1/auth/*` NDP|API Gateway|—|TLS config=1.3-only; HSTS header set; cipher suites restricted; scan via testssl.sh passes|S|P0|

### NTG Points — M1

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|PST connection pool|DI registry|pg-pool singleton wired into repo layer at app bootstrap|M1|UserRepo, AuditRepo (M2+)|
|Redis client|DI registry|ioredis client singleton with sentinel config|M1|TKN (M2)|
|Config module (bcrypt cost, JWT keys)|Strategy/config registry|env-driven config loader at bootstrap|M1|PSS, JWT (M2)|
|Audit event enum|Dispatch table|`AuthEventType` enum mapped to handler writers|M1|AuditRepo, all auth flows (M3)|

### DLV — M1

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|OQ-003|Audit RTN conflict resolved|12-month RTN accepted; TDD updated|
|DM-001|`users` table migrated with full schema|Migration reversible; all 7 columns present|
|DM-002|AuthToken contract documented|OpenAPI schema reviewed; 4 fields defined|
|COMP-DM-AUDIT|`auth_events` table migrated|Partitioned monthly; 12mo RTN job live|
|DEP-POSTGRES/REDIS/NODE/SENDGRID|Core infra provisioned|Health probes green; secrets in vault|
|NFR-SEC-001/002-SCAFFOLD|Crypto abstractions defined|Config tests pass; keys rotatable|
|NFR-COMP-001/002/003|Compliance gates wired into schema|Consent captured; audit log active; PII minimized|
|COMP-INFRA-TLS|TLS 1.3 enforced|testssl.sh score A+|

### MLS DPN — M1

- SEC-POLICY-001 sign-off required before any persistence decisions.
- PST 15 / Redis 7 / SendGrid procurement completed by platform team.
- OQ-003 must be resolved before NFR-COMP-002 RTN sizing.

### MLS Risk Assessment — M1

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|OQ-003 resolution slips past Week 1|Medium|High|Escalate to CMP lead by Day 3; parallel-start audit schema with worst-case 12mo|
|SendGrid sender domain warming delay|Low|Medium|Begin domain warm-up Week 0 pre-kickoff; keep SES as fallback|
|RSA key-RTT automation scope creep|Medium|Medium|Ship manual quarterly RTT runbook in M1; automate in M8|

## M2: Core Auth Primitives (THS + Crypto)

**Objective:** Build crypto primitives (`PSS`, `JWT`), stateful `TKN`, and `THS` orchestrator with full unit coverage. | **Duration:** 2w (Week 3–4) | **Entry:** M1 exit; DM-001/DM-002 migrated; key-vault access granted | **Exit:** `THS.login/register/refresh/me/resetRequest/resetConfirm` implemented with green unit tests; SEC review booked

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|15|COMP-006-PH|Implement `PSS` (bcrypt cost=12) with hash/verify API|PSS|NFR-SEC-001-SCAFFOLD|hash(plaintext)→hash; verify(plaintext,hash)→bool; cost=12 asserted; < 500ms per NFR|S|P0|
|16|COMP-006-JWT|Implement `JWT` (sign/verify RS256) with kid-based key lookup|JWT|NFR-SEC-002-SCAFFOLD|sign(payload)→JWT with kid; verify(token)→payload or error; 5s clock skew; 2048-bit keys; unit test on expired/mutated tokens|M|P0|
|17|COMP-006-TM|Implement `TKN` (issue/refresh/revoke) with Redis persistence|TKN|DEP-REDIS, DM-002, COMP-006-JWT|issueTokens(uid,roles)→AuthToken; refresh(token)→new pair + revoke old; revoke(token); Redis hashed storage; 7d TTL; unit + integ test|L|P0|
|18|COMP-005|Implement `THS` orchestrator (login/register/me/refresh/reset)|THS|COMP-006-PH, COMP-006-JWT, COMP-006-TM|depends injected PSS+TKN+UserRepo+EmailClient; 6 methods exposed; async; typed error codes|L|P0|
|19|COMP-USERREPO|Implement `UserRepo` (CRUD + email lookup + idempotent upsert)|UserRepo|DM-001|create/findByEmail/findById/updatePassword/updateLastLogin; parameterized queries only; upsert idempotent (MIG data safety)|M|P0|
|20|COMP-AUDITREPO|Implement `AuditRepo` writer for auth events|AuditRepo|COMP-DM-AUDIT|log(event_type,user_id,ip,ua,outcome); non-blocking with retry queue; secret fields scrubbed; 12mo RTN honored|M|P0|
|21|COMP-EMAILCLIENT|Implement `EmailClient` (SendGrid) with templated password-reset emails|EmailClient|DEP-SENDGRID|sendPasswordReset(email,token,locale); retry with exponential backoff (3 attempts); delivery tracking webhook; 60s SLA|M|P0|
|22|COMP-LOCKOUT|Implement account-lockout policy (5 attempts/15min per email+IP)|THS|COMP-AUDITREPO, DEP-REDIS|failed attempt counter in Redis keyed on email; lock flag set after 5/15min; returns 423; auto-unlock after 15min; audit logged|M|P0|
|23|COMP-RESETTOKEN|Implement reset-token issuance (1h TTL, single-use)|TKN|DEP-REDIS, COMP-EMAILCLIENT|issueResetToken(uid)→opaque; 1h TTL in Redis; consumed on first use; subsequent attempts 400|M|P0|
|24|COMP-VALIDATOR|Implement password-strength + email-format validators|THS|—|password: ≥8chr + uppercase + digit per NIST; email: RFC5322 + lowercase normalization; returns typed errors|S|P0|

### NTG Points — M2

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|DI container (`THS` deps)|Dependency injection|THS constructor wires PSS, TKN, UserRepo, AuditRepo, EmailClient via container|M2|All API NDP (M3)|
|AuthEvent → AuditRepo dispatch|Dispatch table|enum-keyed handler map emits writes per event|M2|M3 endpoint handlers|
|Password-strength validator|Strategy pattern|Strategy registered by policy version id|M2|THS.register, THS.resetConfirm|
|Lockout counter key schema|Registry|Redis key template `lockout:{email}:{window}` registered centrally|M2|THS.login (M3)|
|JWT kid resolver|Registry|kid→public-key map loaded at boot; RTT-safe|M2|JWT.verify consumers (M3, gateway)|

### DLV — M2

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|COMP-005|THS orchestrator with 6 flows|All methods covered by unit tests; error paths typed|
|COMP-006-PH/JWT/TM|Crypto + token primitives|bcrypt cost=12; RS256 signed; Redis TTL honored|
|COMP-USERREPO/AUDITREPO/EMAILCLIENT|Persistence + email client|Idempotent; retry wired; PII scrubbed|
|COMP-LOCKOUT|Lockout policy enforced|5/15-min counters tested; 423 returned|
|COMP-RESETTOKEN|Password reset tokens|1-hour TTL; single-use; cannot be replayed|
|COMP-VALIDATOR|Validators|Weak passwords rejected; duplicate emails rejected via UserRepo|

### MLS DPN — M2

- M1 complete (DM-001/DM-002 migrated, key vault ready).
- Security review booked for M2 exit (R-PRD-004 mitigation).

### MLS Risk Assessment — M2

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Bcrypt cost=12 exceeds 500ms on target infra|Low|Medium|Benchmark on target pod specs Week 3; if >500ms, tune to cost=11 with security team sign-off|
|Redis latency inflates TKN.refresh beyond 100ms p95|Medium|Medium|Pipeline Redis ops; co-locate Redis in same AZ; measure in M5 load test|
|RSA key material mishandled (committed to repo, leaked)|Low|Critical|CI secret-scanning; pre-commit hooks; keys only in Vault; rotate immediately on leak|

## M3: REST API Surface & Functional Flows

**Objective:** Expose 6 REST NDP (login/register/me/refresh + reset-request/reset-confirm) under `/v1/auth/*` wiring FA0..005 end to end. | **Duration:** 2w (Week 5–6) | **Entry:** M2 exit; `THS` facade signed off | **Exit:** all NDP return correct status codes and error envelope; FA0..005 acceptance tests green; OpenAPI spec published

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|25|FA0|Functional: login with email/password returns AuthToken|THS|COMP-005, COMP-LOCKOUT|valid→200+AuthToken; invalid→401 (no enumeration); unknown→401; lockout→423 after 5/15min; audit logged|M|P0|
|26|API-001|POST `/v1/auth/login` handler + rate-limit (10/min/IP)|THS|FA0, API Gateway|body={email,password}; 200→AuthToken(expiresIn=900,tokenType=Bearer); 401/423/429; error envelope `{error:{code,message,status}}`|M|P0|
|27|FR-AUTH-002|Functional: RGS with validation creates SRP|THS|COMP-005, COMP-VALIDATOR, NFR-COMP-001|valid→201+SRP; duplicate→409; weak pw→400; bcrypt cost=12 stored; consent captured; audit logged|M|P0|
|28|API-002|POST `/v1/auth/register` handler + rate-limit (5/min/IP)|THS|FR-AUTH-002|body={email,password,displayName,consent}; 201→SRP(id,email,displayName,createdAt,updatedAt,lastLoginAt:null,roles:["user"]); 400/409|M|P0|
|29|FR-AUTH-003|Functional: JWT issuance + refresh-token RTT|TKN|COMP-006-TM, COMP-006-JWT|login→access(15m)+refresh(7d); refresh→new pair+old revoked; expired→401; revoked→401; audit logged|M|P0|
|30|API-004|POST `/v1/auth/refresh` handler + rate-limit (30/min/user)|TKN|FR-AUTH-003|body={refreshToken}; 200→new AuthToken; 401 on expired/revoked; old token invalidated atomically|M|P0|
|31|FR-AUTH-004|Functional: user profile retrieval for authenticated user|THS|COMP-005, COMP-USERREPO|valid bearer→200+SRP; expired/invalid→401; response includes id,email,displayName,createdAt,updatedAt,lastLoginAt,roles|S|P0|
|32|API-003|GET `/v1/auth/me` handler + bearer auth middleware + rate-limit (60/min/user)|THS|FR-AUTH-004|requires `Authorization: Bearer`; JWT.verify; 200→SRP; 401 on invalid/expired|S|P0|
|33|FR-AUTH-005|Functional: two-step password reset via email|THS|COMP-RESETTOKEN, COMP-EMAILCLIENT|request→email sent within 60s; confirm→new hash stored + all sessions revoked; token 1h TTL; single-use; unknown email returns 200 (no enumeration)|M|P0|
|34|API-005|POST `/v1/auth/reset-request` handler (implied, FR-AUTH-005)|THS|FR-AUTH-005|body={email}; always 200 (no enumeration); async email send via SendGrid; rate-limit 3/hr/IP|S|P0|
|35|API-006|POST `/v1/auth/reset-confirm` handler (implied, FR-AUTH-005)|THS|FR-AUTH-005|body={token,newPassword}; 200 on success + revoke all user sessions; 400 invalid token; validator applied; audit logged|M|P0|
|36|COMP-AUTHMW|Bearer authentication middleware for protected routes|THS|COMP-006-JWT|Authorization header parsed; JWT.verify; uid attached to req.ctx; 401 on missing/invalid|S|P0|
|37|COMP-ERRORENV|Unified error envelope `{error:{code:AUTH_*,message,status}}`|THS|—|all 4xx/5xx return envelope; `code` taxonomy documented; no stack traces to client|S|P0|
|38|COMP-OPENAPI|Publish OpenAPI 3.1 spec for `/v1/auth/*`|THS|API-001..006|spec validates against OAS 3.1; includes all 6 NDP, error schemas, examples; served at `/v1/auth/openapi.json`|S|P1|

### NTG Points — M3

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Express/Fastify route registry|Dispatch table|routes registered via `/v1/auth/*` prefix with handler map|M3|API Gateway (M5), frontend pages (M4)|
|Rate-limit middleware chain|Middleware|per-route limits applied in order: CORS→authMW→rateLimit→handler|M3|All 6 NDP|
|Error envelope handler|Strategy|typed-error→HTTP mapping strategy keyed by error code|M3|All NDP|
|Bearer auth middleware|Middleware|`COMP-AUTHMW` mounted on `GET /me` (+ any future protected route)|M3|API-003, future protected NDP|
|SendGrid retry queue binding|Event binding|`EmailClient.sendPasswordReset` → BullMQ/worker|M3|API-005|

### DLV — M3

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|API-001..006|6 REST NDP operational|All status codes correct; rate limits enforced; error envelope uniform|
|FA0..005|5 functional flows end-to-end|Acceptance tests from TDD pass|
|COMP-AUTHMW|Bearer middleware|Unit + integration test green|
|COMP-ERRORENV|Error envelope|Documented code taxonomy AUTH_*|
|COMP-OPENAPI|OpenAPI 3.1 spec|Linter passes; published behind `/openapi.json`|

### MLS DPN — M3

- M2 complete (THS orchestrator + token primitives ready).
- API Gateway team pre-booked for rate-limit + CORS rule deployment.
- SendGrid email templates approved by product + legal.

### MLS Risk Assessment — M3

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Rate-limit tuning too strict, blocks legitimate users|Medium|Medium|Start with PRD-specified limits; measure 99th percentile real traffic in M5; allow runtime override via config|
|Password-reset email enumeration leak via timing or response|Medium|High|Constant-time response path; always 200; timing tests in M6 security suite|
|OpenAPI spec drift from handlers|Low|Low|Schema-first: generate types from OpenAPI; CI asserts handler types match|

## M4: Frontend Components & THP Wiring

**Objective:** Ship `THP` context, protected routing, and `LoginPage` / `RegisterPage` / `ProfilePage` behind `ANL` flag. Reset flow UI included. | **Duration:** 2w (Week 7–8) | **Entry:** M3 exit; API-001..006 live in staging | **Exit:** UI journey from landing→register→login→profile→reset functional behind feature flag; PRD journey maps validated

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|39|COMP-004|`THP` React context (token mgmt, silent refresh, route guard)|THP|API-001, API-003, API-004|accessToken in memory only (R-001); refreshToken in HttpOnly cookie; 401 triggers silent refresh via API-004; unauth users redirected to `/login`; clears on tab close|L|P0|
|40|COMP-001|`LoginPage` at `/login` (email/password form + CAPTCHA after 3 fails)|LoginPage|COMP-004, API-001|props{onSuccess,redirectUrl?}; inline validation; generic error on 401; CAPTCHA after 3 fails (R-002); stores token via THP|M|P0|
|41|COMP-002|`RegisterPage` at `/register` (form + client-side password strength + consent)|RegisterPage|COMP-004, API-002, NFR-COMP-001|props{onSuccess,termsUrl}; password strength meter; consent checkbox NN (NFR-COMP-001); duplicate→inline 409 hint; submit→logged in+redirect dashboard|M|P0|
|42|COMP-003|`ProfilePage` at `/profile` (displays SRP)|ProfilePage|COMP-004, API-003|protected route; renders id,email,displayName,createdAt; loading state <1s; error state on 401 triggers refresh then re-fetch|S|P0|
|43|COMP-FE-RESET-REQ|Forgot-password page (calls API-005)|LoginPage|API-005|always shows confirmation (no enumeration); email input validated; 60s client-side throttle|S|P0|
|44|COMP-FE-RESET-CONF|Reset-confirmation page (token from URL, calls API-006)|LoginPage|API-006|token parsed from URL query; new-password form with strength meter; success→redirect to `/login` with toast; expired→clear message + link to request new|M|P0|
|45|COMP-FE-LOGOUT|Logout UI control + session termination|THP|COMP-004|button in header for authenticated users; clears access token; revokes refresh token via API-004 revoke path; redirects to `/`|S|P0|
|46|PRD-JOURNEY-FIRSTSIGNUP|Validate PRD S22 first-time-signup journey end-to-end|THP+COMP-002|COMP-002, COMP-004|land→signup→dashboard ≤2s; inline validation during entry; usability test with 5 users (R-PRD-001 mitigation)|S|P0|
|47|PRD-JOURNEY-SESSIONPERSIST|Validate PRD S22 returning-user session persistence|THP|COMP-004|silent refresh triggers without re-login; >7d idle→clear re-login prompt; cross-device login confirmed|S|P0|

### NTG Points — M4

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|React router guard|Middleware|`<ProtectedRoute>` wraps routes behind `THP.isAuthenticated`|M4|ProfilePage and future protected routes|
|Axios/fetch interceptor|Event binding|401 → silent refresh via `TKN` → retry original|M4|All authenticated API calls|
|`ANL` flag consumer|Feature flag registry|LaunchDarkly/config reader checked at route mount|M4|LoginPage, RegisterPage|
|Token storage strategy|Strategy pattern|access=in-memory / refresh=HttpOnly cookie, swappable for future session mode|M4|THP|
|CAPTCHA provider adapter|Strategy|Recaptcha v3 wrapper with feature-flag fallback|M4|LoginPage|

### DLV — M4

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|COMP-004|THP context|Silent refresh tested; 401 interception validated|
|COMP-001/002/003|Login/Register/Profile pages|Visual QA pass; a11y WCAG 2.1 AA|
|COMP-FE-RESET-REQ/CONF|Reset flow UI|Token round-trip works; enumeration-safe|
|COMP-FE-LOGOUT|Logout control|Token cleared + revocation called|
|PRD-JOURNEY-*|Journey map validation|≤2s signup; seamless cross-device refresh|

### MLS DPN — M4

- M3 NDP live in staging with observable response times.
- CAPTCHA keys procured (R-002 mitigation).
- Design assets approved by design lead (PRD S27).

### MLS Risk Assessment — M4

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|`THP` race condition during concurrent silent refresh|Medium|High|Single-flight refresh promise; property-based tests; replay harness|
|AccessToken inadvertently persisted to localStorage (XSS risk, R-001)|Medium|High|ESLint rule forbidding localStorage.setItem for auth; code review gate|
|Poor RGS UX tanks conversion (R-PRD-001)|Medium|High|Pre-launch usability testing with 5 users; funnel analytics wired from Day 1|

## M5: Non-Functional, Compliance & Observability

**Objective:** Validate performance, reliability, and security NFRs; finalize SOC2/GDPR CMP wiring; stand up metrics, traces, and alerts. | **Duration:** 2w (Week 9–10) | **Entry:** M3 + M4 exit; staging environment stable | **Exit:** p95 <200ms at 500 concurrent; 99.9% synthetic uptime 7-day; SOC2 audit dry-run passes; all alerts firing in staging

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|48|NFR-PERF-001|Validate auth NDP p95 <200ms via APM instrumentation|THS|COMP-005|OpenTelemetry tracing on all 6 NDP; p95 <200ms sustained over 1h test; span attributes include endpoint,uid_hash,outcome|M|P0|
|49|NFR-PERF-002|Validate 500 concurrent login throughput via k6|THS|NFR-PERF-001|k6 scenario: 500 VU ramp, 10-min steady; p95 <200ms; error <0.1%; DB pool saturation <70%|M|P0|
|50|NFR-REL-001|Validate 99.9% availability over 30-day rolling window|THS|OPS-005|SLO defined as `availability = success_requests/total`; budget=43.8 min/mo; burn-rate alert at 2x+5x; synthetic monitor every 1min|M|P0|
|51|NFR-SEC-001|Validate bcrypt cost=12 enforced in PSS|PSS|COMP-006-PH|unit test asserts cost=12 in produced hash; hash verification roundtrip; benchmark <500ms|S|P0|
|52|NFR-SEC-002|Validate RS256 with 2048-bit RSA keys; RTT runbook|JWT|COMP-006-JWT|config validation test asserts alg=RS256 and modulus≥2048; RTT runbook with kid cutover; dual-kid window documented|M|P0|
|53|NFR-COMP-002-WIRING|Wire audit logging into all auth flows (SOC2)|AuditRepo|COMP-AUDITREPO, API-001..006|every login/register/refresh/reset/logout writes event; fields=user_id+ts+ip+ua+outcome; 12mo RTN enforced; sample export passes SOC2 evidence|L|P0|
|54|COMP-METRICS|Prometheus metrics emitter (counters + histograms)|THS|OPS-005|`auth_login_total{outcome}`, `auth_login_duration_seconds`, `auth_token_refresh_total{outcome}`, `auth_registration_total`; Grafana dashboard template|M|P0|
|55|COMP-TRACING|OpenTelemetry distributed tracing across THS→PSS→TKN→JWT|THS|COMP-METRICS|spans linked; trace ids propagated from gateway; sampling 10% default, 100% on error|M|P0|
|56|COMP-ALERTS|Alert rules in Alertmanager|THS|COMP-METRICS|login failure >20%/5min; p95 >500ms; Redis conn failures >10/min; oncall paged P1; alert runbook linked|M|P0|
|57|COMP-XSS-HARDEN|XSS hardening headers (CSP, X-Frame-Options, X-Content-Type)|API Gateway|R-001|CSP strict-default; no inline scripts; Report-Only pre-launch; X-Frame=DENY; X-Content=nosniff|S|P0|
|58|COMP-CORS|CORS allowlist at API Gateway restricted to known frontend origins|API Gateway|—|allowlist=[staging,prod frontend FQDNs]; credentials=true only for allowlisted; preflight cached 24h|S|P0|
|59|COMP-PENTEST|External penetration test and findings remediation (R-PRD-004)|THS|M4 complete|vendor engaged; scope=all 6 NDP + THP; SOC2-aligned report; all Critical/High remediated pre-GA|L|P0|
|60|COMP-DLP|Secret-scrubbing on logs (no passwords, no tokens, no reset tokens)|THS|COMP-AUDITREPO|unit test against known secrets; log processor allowlist; incident runbook if breach detected|S|P0|

### NTG Points — M5

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|Prometheus scrape target|Registry|`/metrics` endpoint exposed; ServiceMonitor CR|M5|Grafana dashboards|
|OTLP exporter|Event binding|traces→collector→Tempo/Jaeger|M5|SRE/oncall|
|Alertmanager routes|Dispatch table|severity→team-specific on-call RTT|M5|PagerDuty/Opsgenie|
|Audit event taxonomy|Dispatch table|event_type enum → JSON schema version|M5|SOC2 auditors, BI team|
|Secret scrubbing middleware|Middleware chain|log processor pipeline redacts by field-name regex|M5|All log writers|

### DLV — M5

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|NFR-PERF-001/002|Performance targets met|p95<200ms @ 500 concurrent|
|NFR-REL-001|Availability SLO defined|Burn-rate alerts armed|
|NFR-SEC-001/002|Crypto config validated|Tests + runbook shipped|
|NFR-COMP-002-WIRING|Audit logging live on all events|SOC2 dry-run passes|
|COMP-METRICS/TRACING/ALERTS|Observability stack|Dashboards + pager routes live|
|COMP-XSS-HARDEN/CORS|Defensive headers|Scanner scores A+|
|COMP-PENTEST|Pen-test complete|Critical/High=0 open|
|COMP-DLP|Log scrubbing|Secret-leak test passes|

### MLS DPN — M5

- Staging environment provisioned identically to production (same pod sizing, DB sizing).
- Pen-test vendor booked by Week 6 to avoid scheduling slip.
- SOC2 auditor preview booked for M5 exit.

### MLS Risk Assessment — M5

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Pen-test surfaces critical finding late|Medium|Critical|Book pre-M5 "light" review; reserve 1w buffer in M5 for remediation|
|Audit log volume exceeds storage sizing|Low|Medium|Estimate 1KB/event × 1000 DAU × 365d = ~400MB; size with 3x headroom; compress partitions|
|Alert fatigue (false positives)|Medium|Low|Tune thresholds with 2w dry-run in staging before PagerDuty wiring|

## M6: Testing Pyramid (Unit/NTG/E2E/Load)

**Objective:** Achieve 80% unit / 15% integration / 5% E2E coverage per TDD §15.1; add security + load + CMP test suites. | **Duration:** 2w (Week 11–12) | **Entry:** M5 exit; all code paths ready for test | **Exit:** CI pipeline green on all tiers; load test sustains 500 concurrent; all mandatory NFR assertions automated

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|61|TEST-001|Unit: login with valid creds returns AuthToken|THS|FA0|THS.login calls PSS.verify then TKN.issueTokens; returns AuthToken with both tokens; Jest + ts-jest|S|P0|
|62|TEST-002|Unit: login with invalid creds returns 401|THS|FA0|Returns 401 when verify()=false; no AuthToken issued; no enumeration; mocks assert single call to verify|S|P0|
|63|TEST-003|Unit: token refresh with valid refresh token|TKN|FR-AUTH-003|refresh() validates→revokes old→issues new pair; old key absent in Redis after call|S|P0|
|64|TEST-004|NTG: RGS persists SRP to PST|THS|FR-AUTH-002|Supertest+testcontainers; POST /register→201; DB row with correct hash (bcrypt cost=12); consent_accepted_at not null|M|P0|
|65|TEST-005|NTG: expired refresh token rejected by TKN + Redis|TKN|FR-AUTH-003|Insert refresh token with 1s TTL; wait 2s; refresh()→401; audit event logged|S|P0|
|66|TEST-006|E2E: user registers, logs in, sees profile (Playwright)|RegisterPage+LoginPage+ProfilePage|FA0, FR-AUTH-002, COMP-004|full journey: landing→register→profile; token refresh silent; feature-flag-enabled path|M|P0|
|67|TEST-IMPLICIT-BCRYPT|Unit: assert bcrypt cost parameter (NFR-SEC-001)|PSS|NFR-SEC-001|parse produced hash header; assert cost==12; negative test with cost=10|S|P0|
|68|TEST-IMPLICIT-RS256|Config validation: RS256 + 2048-bit RSA (NFR-SEC-002)|JWT|NFR-SEC-002|JWT boot asserts alg==RS256 and key modulus≥2048; fails-fast if weak|S|P0|
|69|TEST-IMPLICIT-LOAD|k6 load scenario at 500 concurrent (NFR-PERF-002)|THS|NFR-PERF-002|scripted scenario committed in repo; CI runs against staging nightly; p95<200ms; error<0.1%|M|P0|
|70|TEST-IMPLICIT-AUDIT|NTG: audit event emitted for every auth flow (NFR-COMP-002)|AuditRepo|NFR-COMP-002-WIRING|6 flows × 2 outcomes each=12 scenarios; assert event row with required fields exists in 12mo partition|M|P0|
|71|TEST-SEC-ENUMERATION|Security: no user enumeration on login/reset-request|THS|API-001, API-005|timing-parity test (±10ms) across registered/unregistered email; response body identical|S|P0|
|72|TEST-SEC-LOCKOUT|NTG: account locks after 5 attempts/15min|THS|COMP-LOCKOUT|5 failed attempts→423; 6th→423; after 15min→200 with correct creds; audit rows present|S|P0|

### NTG Points — M6

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|CI test-tier matrix|Dispatch table|GitHub Actions job map: unit/integration/e2e/load|M6|PR gating|
|Testcontainers registry|Registry|ephemeral PST + Redis per integration run|M6|NTG tests|
|k6 runner|Strategy|nightly load run against staging|M6|NFR monitoring|
|Playwright test projects|Strategy|Chromium/Firefox/WebKit matrix|M6|E2E coverage|
|Coverage threshold gate|Middleware|fails PR if coverage drops below 80% unit / 15% integ / 5% e2e|M6|PR gating|

### DLV — M6

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|TEST-001..006|Core TDD-specified test cases|Covers FA0..005|
|TEST-IMPLICIT-BCRYPT/RS256|NFR-SEC assertions automated|Boot fails-fast on misconfig|
|TEST-IMPLICIT-LOAD|k6 load suite|Nightly run in CI; p95<200ms|
|TEST-IMPLICIT-AUDIT|Audit coverage integration|12 scenarios green|
|TEST-SEC-ENUMERATION/LOCKOUT|Security hardening tests|Timing + lockout enforced|

### MLS DPN — M6

- Staging identical to production (M5 pre-req).
- k6 runner or Grafana Cloud k6 account configured.
- Playwright CI infrastructure provisioned.

### MLS Risk Assessment — M6

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Flaky E2E tests block CI|Medium|Medium|Quarantine lane for flaky tests; mandatory triage SLA of 48h|
|testcontainers slow down CI >15min|Medium|Low|Parallelize by test group; cache container images|
|k6 environment not isolated from real users|Low|High|Dedicated staging tenancy; rate-limit k6 IPs; synthetic test accounts only|

## M7: Migration, Feature Flags & Phased Rollout

**Objective:** Execute MIG-001/002/003 three-phase rollout with `ANL` + `ATR` feature flags and documented rollback. | **Duration:** 3w (Week 13–15) | **Entry:** M5 + M6 green; pen-test clean; staging 7-day clean burn | **Exit:** 100% GA; 99.9% uptime first 7 days; legacy auth decommissioned

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|73|MIG-FLAG-LOGIN|Provision `ANL` feature flag (default OFF)|THP, THS|LaunchDarkly|flag registered in LD; targeting rules (internal/beta/all); flag referenced in gateway, THS, frontend; removal backlog item created|S|P0|
|74|MIG-FLAG-REFRESH|Provision `ATR` feature flag (default OFF → ON in MIG-003)|TKN|LaunchDarkly|when OFF only access tokens issued; when ON refresh pair issued; remove flag M8 after 2w stability|S|P0|
|75|MIG-DATAMIG-BACKUP|Full PST backup immediately before each phase|PST|DEP-POSTGRES|pg_basebackup + WAL archive; restore tested in staging; backup retained ≥30 days|S|P0|
|76|MIG-DUAL-RUN|Parallel-run with legacy auth during Phases 1–2|THS|MIG-FLAG-LOGIN|legacy + new both live; idempotent upsert on SRP prevents dup rows; divergence metric alerts on mismatch|L|P0|
|77|MIG-001|Phase 1: Internal Alpha — staging enable for AT + QA|THS|M5, M6|1w duration; all FA0..005 manual pass; zero P0/P1 bugs; audit logs flowing; flag ON for internal users only|M|P0|
|78|MIG-002|Phase 2: Beta at 10% — enable for 10% traffic|THP, THS|MIG-001|2w duration; LD targeting 10% users; p95<200ms; error<0.1%; zero Redis conn failures; rollback triggers armed|L|P0|
|79|MIG-002-ROLLBACK|Rollback triggers + automation for MIG-002|THS|MIG-002|trigger: p95>1000ms/5min OR error>5%/2min OR Redis conn failures>10/min OR SRP corruption; auto-disable flag; PagerDuty page|M|P0|
|80|MIG-003|Phase 3: GA at 100% — remove flag; deprecate legacy|THS|MIG-002|1w duration; flag removed; legacy NDP return 410 Gone with migration instructions; 99.9% uptime first 7d|M|P0|
|81|MIG-ROLLBACK-RUNBOOK|Documented 6-step rollback procedure (TDD §19.3)|THS|MIG-002|steps: disable flag→smoke test legacy→root-cause THS→restore SRP if corrupted→notify teams→post-mortem ≤48h; tabletop exercised|S|P0|
|82|MIG-LEGACY-DEPRECATE|Decommission legacy auth NDP after MIG-003|Legacy auth svc|MIG-003|2-week deprecation window; monitoring shows <1% traffic; shutdown coordinated with platform-team; DB rows archived|M|P1|
|83|MIG-FLAG-REMOVE|Remove both feature flags after stability proven|THS|MIG-003|ANL removed immediately post MIG-003; ATR removed MIG-003+2w; CI asserts flag absence|S|P1|

### NTG Points — M7

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|LaunchDarkly SDK|Registry|initialized in both frontend and backend at bootstrap; flag cache 30s|M7|THP, THS|
|Rollback automation|Event binding|alert payload → LD API (disable flag) → PagerDuty → incident channel|M7|On-call, SRE|
|Legacy/new dispatcher at gateway|Dispatch table|flag-based routing: ANL on→/v1/auth/*, off→/legacy/auth/*|M7|API Gateway|
|Data-parity monitor|Event binding|nightly job compares SRP rows between legacy+new stores|M7|SRE, CMP|
|Audit event taxonomy (migration_phase)|Dispatch table|event_type extended with phase tag for rollout analysis|M7|Post-mortem analysis|

### DLV — M7

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|MIG-001/002/003|Three-phase rollout executed|Exit criteria met at each phase|
|MIG-FLAG-LOGIN/REFRESH|Feature flags provisioned|Documented removal dates|
|MIG-DATAMIG-BACKUP|Pre-phase backups|Restore tested before GA|
|MIG-DUAL-RUN|Parallel run with legacy|Idempotent; divergence alert armed|
|MIG-002-ROLLBACK / MIG-ROLLBACK-RUNBOOK|Rollback automation + runbook|Tabletop exercised|
|MIG-LEGACY-DEPRECATE / MIG-FLAG-REMOVE|Cleanup complete|Legacy 410 Gone; flags removed|

### MLS DPN — M7

- R-003 data-loss mitigation implemented (idempotent upserts, backup).
- LaunchDarkly account + SDK quotas sufficient.
- Incident channel + PagerDuty RTT staffed 24/7 for first 2 weeks of GA.

### MLS Risk Assessment — M7

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|R-003 data loss during legacy→new migration|Medium|High|Parallel run + idempotent upserts + pre-phase backups + tabletop rollback|
|Silent data divergence between legacy and new stores|Medium|High|Nightly divergence monitor; alert on >0.1% drift; block MIG-003 if drift present|
|Rollback trigger fires false-positive at 3AM|Medium|Medium|Burn-rate windows tuned with M5 baseline; require 2 consecutive windows before auto-disable|

## M8: Operational Readiness & Runbook Handover

**Objective:** Complete runbooks, capacity planning, on-call RTT, and observability handover; automate RSA key RTT. | **Duration:** 1w (Week 16) | **Entry:** MIG-003 complete; 7-day clean burn | **Exit:** AT on-call schedule live; all OPS runbooks signed off; capacity plan peer-reviewed; key-RTT automation deployed

|#|ID|Deliverable|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|84|OPS-001|Runbook: THS down|THS|COMP-METRICS, COMP-ALERTS|documented symptoms, diagnosis (pod health, PST, PSS/TKN init), resolution (restart, failover), escalation path (AT→platform-team 15min), prevention (HPA, multi-AZ Redis, DB pool tuning)|M|P0|
|85|OPS-002|Runbook: Token refresh failures|TKN|COMP-METRICS|symptoms (THP redirect loop, auth_token_refresh_total spike), diagnosis (Redis conn, JWT key mount, flag state), resolution (scale Redis, remount secrets, enable flag), prevention (Redis HA, secret monitoring)|M|P0|
|86|OPS-003|On-call RTT + response expectations|AT|OPS-001, OPS-002|24/7 for 2w post-GA; P1 ACK ≤15min; tooling=K8s/Grafana/Redis CLI/PG admin; escalation AT→test-lead→eng-mgr→platform-team; schedule in PagerDuty|S|P0|
|87|OPS-004|Capacity planning document|THS|NFR-PERF-002|THS 3-10 pods HPA@70% CPU; PG pool 100 (→200 if wait>50ms); Redis 1GB (→2GB@>70% util); review cadence quarterly|M|P1|
|88|OPS-005|Observability bundle: logs, metrics, traces, alerts|THS|COMP-METRICS, COMP-TRACING, COMP-ALERTS|structured logs (sensitive fields scrubbed); 4 Prom metrics published; OTel spans linked; 3 Alertmanager rules armed; Grafana dashboards as-code|M|P0|
|89|OPS-RSA-ROTATION|Automate quarterly RSA key RTT|JWT|NFR-SEC-002|scheduled job generates new keypair→updates kid map→dual-verify window 1h→old key archived; automated test verifies cutover; manual runbook retained as fallback|M|P1|
|90|OPS-RETENTION-JOB|Monthly partition-drop job for `auth_events` (12mo RTN)|PST|NFR-COMP-002|cron job drops partitions >12mo; dry-run first; audit-trail of drops; rollback via PITR|S|P0|
|91|OPS-POSTMORTEM-TEMPLATE|Post-mortem template + blameless review process|AT|OPS-003|template covers: timeline, root cause, impact, corrective actions, prevention; review within 48h of any P1; published to shared drive|S|P1|

### NTG Points — M8

|Artifact|Type|Wired|MLS|Consumed By|
|---|---|---|---|---|
|PagerDuty RTT|Registry|on-call schedule imported into PD; escalation policy linked|M8|Alertmanager|
|Runbook links in alerts|Dispatch table|alert→runbook URL map|M8|On-call responders|
|Key-RTT scheduler|Event binding|cron 0 0 1 */3 * → RTT workflow|M8|JWT|
|Retention job scheduler|Event binding|cron 0 3 * * 0 → partition-drop dry-run then apply|M8|AuditRepo|
|Post-mortem webhook|Event binding|incident close → template issue created|M8|AT|

### DLV — M8

|ID|Description|Acceptance Criteria|
|----|-------------|---------------------|
|OPS-001/002|Core runbooks|Signed off by SRE + AT|
|OPS-003|On-call RTT|24/7 coverage confirmed 2w post-GA|
|OPS-004|Capacity plan|Peer-reviewed; next review booked|
|OPS-005|Observability bundle|Logs/metrics/traces/alerts in production|
|OPS-RSA-ROTATION|Key RTT automated|Dry-run successful in staging|
|OPS-RETENTION-JOB|Audit log RTN enforced|Monthly drop job green|
|OPS-POSTMORTEM-TEMPLATE|Post-mortem process|Template approved; webhook wired|

### MLS DPN — M8

- MIG-003 complete and stable for 7 days.
- AT staffing confirmed for 24/7 RTT.
- Grafana-as-code repo provisioned.

### MLS Risk Assessment — M8

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|Key-RTT automation introduces regression|Medium|High|Dry-run in staging for 2w before production; manual fallback retained|
|Retention-drop job accidentally drops recent partition|Low|Critical|Dry-run + audit trail + PITR test before enabling; require human approval for first 3 runs|
|On-call fatigue beyond 2w post-GA|Medium|Medium|Rotate AT with platform-team starting week 3; tune alerts to reduce noise|

## Risk Assessment and Mitigation

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-001 Token theft via XSS enables session hijack|High|Medium|Session takeover; account compromise|accessToken in memory only; HttpOnly cookie for refresh; 15min TTL; ESLint rule forbidding localStorage; CSP strict (M5 COMP-XSS-HARDEN)|security-lead|
|2|R-002 Brute-force attacks on login|Medium|High|Credential stuffing; account compromise|10 req/min/IP gateway rate limit; 5/15min account lockout; bcrypt cost 12; CAPTCHA after 3 fails in COMP-001|security-lead|
|3|R-003 Data loss during legacy→new migration|High|Medium|SRP corruption; user lockout|Parallel-run during MIG-001..002; idempotent upsert; per-phase backup; tabletop rollback in M7|AT|
|4|R-PRD-001 Low RGS adoption from poor UX|High|Medium|Missed 60% conversion target; revenue delay|Pre-launch usability test with 5 users (M4); funnel analytics from Day 1; iterate in MIG-002|product|
|5|R-PRD-002 Compliance failure from incomplete audit logging|High|Medium|SOC2 audit fail; legal exposure|OQ-003 resolved to 12-month; audit wiring on all 6 flows (M5 NFR-COMP-002-WIRING); SOC2 dry-run M5 exit|CMP|
|6|R-PRD-003 Email delivery failures block password reset|Medium|Low|Support ticket spike; user frustration|SendGrid delivery webhook + alerting; retry with backoff; support-channel fallback documented in OPS-002|platform-team|
|7|R-PRD-004 Security breach from implementation flaws|Critical|Low|User credentials leaked; regulatory + reputational|Dedicated security review at M2 exit; external pen-test M5 (COMP-PENTEST); all Critical/High remediated before MIG-001|security-lead|
|8|OQ-003 RTN conflict unresolved blocks M1|High|Medium|M1 slips; downstream milestones slip|Escalate to CMP lead Day 1; decision required before Week 1 Day 3|CMP + AT|
|9|OQ-005 refresh-token cap undefined inflates Redis|Medium|Medium|Redis memory exhaustion; token storage DoS|Impose soft cap=10 devices/user in M2; revisit with Product before MIG-002|product|
|10|OQ-008 Admin story (Jordan) missing FR coverage|Medium|Medium|PRD/TDD gap; CMP evidence missing|Decide scope before M3: either add FR-AUTH-006 admin NDP or descope to v1.1 with audit log query via BI tool|product + CMP|

## Resource Requirements and DPN

### External DPN

|Dependency|Required By MLS|Status|Fallback|
|---|---|---|---|
|PST 15+ cluster|M1|Confirmed; provisioning scheduled|None — hard dependency|
|Redis 7+ cluster (HA)|M1/M2|Confirmed|None — hard dependency|
|SendGrid account + warm sender domain|M1 → M3|Procurement in progress|AWS SES (requires domain re-warm)|
|Node.js 20 LTS runtime image|M1|Confirmed|N/A|
|bcryptjs (npm)|M2|Pinned|argon2 (requires PSS swap)|
|jsonwebtoken (npm)|M2|Pinned|jose (equivalent RS256 support)|
|API Gateway (rate-limit + CORS)|M3 / M5|Owned by platform-team|Service-mesh-level limits as degraded fallback|
|HashiCorp Vault (RSA keys)|M1 / M2|Owned by platform-team|AWS KMS (requires JWT adapter change)|
|SEC-POLICY-001 sign-off|M1|Pending|Block M1 start until signed|
|LaunchDarkly SDK + account|M4 / M7|Procurement confirmed|OpenFeature + in-house flag service|
|External pen-test vendor|M5|Booking required by Week 6|Internal security review (degraded confidence)|
|SOC2 auditor preview|M5|Booking required|Compliance lead internal review|

### Infrastructure Requirements

- 3× Node.js 20 `THS` pods baseline; HPA to 10 at 70% CPU (OPS-004).
- PST 15 primary + read replica; pool size 100; multi-AZ.
- Redis 7 cluster with sentinel; 1GB baseline, 2GB on >70% utilization; TLS at rest.
- SendGrid with SPF/DKIM/DMARC; minimum 1k emails/day warmed capacity.
- Prometheus + Grafana stack with SSO.
- Tempo or Jaeger for OTLP traces.
- LaunchDarkly workspace with separate prod/staging environments.
- GitHub Actions CI with testcontainers + k6 + Playwright runners.
- HashiCorp Vault namespace for RSA keypair and SendGrid/DB secrets.

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|MLS|
|---|---|---|---|---|
|Login p95 latency (TDD §4.1)|p95 response time on POST /auth/login|< 200ms|APM percentile over 1h sustained|M5|
|Registration success rate|successful_registrations / total_attempts|> 99%|Prometheus `auth_registration_total{outcome}`|M5|
|Token refresh p95 latency|p95 on POST /auth/refresh|< 100ms|APM|M5|
|Service availability|(successes/total) over 30d|≥ 99.9%|SLO burn-rate monitor|M5 → M8|
|`PSS.hash()` duration|p95 hash time|< 500ms at cost=12|Bench + unit test|M2 / M6|
|Concurrent login throughput|k6 VU=500 for 10min|p95<200ms, err<0.1%|k6 load run|M6|
|Registration conversion (PRD)|landing→register→confirmed|> 60%|Funnel analytics on `RegisterPage`|MIG-002 → MIG-003|
|DAU of authenticated users (PRD)|unique uid / day|> 1,000 within 30d of GA|`AuthToken` issuance analytics|MIG-003 + 30d|
|Average session duration (PRD)|avg time between first login and last activity|> 30 minutes|Token-refresh event analytics|MIG-003|
|Failed login rate (PRD)|failed/total attempts|< 5%|Audit event log analysis|MIG-003|
|Password reset completion (PRD)|completed/requested resets|> 80%|Reset funnel analytics|MIG-003|
|MIG-002 beta exit (TDD §24)|p95, error, Redis conn over 2w at 10%|p95<200ms, err<0.1%, 0 Redis failures|SLO dashboards|MIG-002|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Token architecture|Stateless JWT access + Redis refresh|(a) Stateless only (no revocation); (b) Server sessions|JWT+Redis enables both horizontal scale and immediate revocation; pure stateless fails R-001 revocation; pure sessions fails NFR-PERF-002 (500 concurrent) on single-instance stickiness|
|Password hashing|bcrypt cost 12|Argon2id; scrypt; PBKDF2|bcrypt cost 12 satisfies NIST SP 800-63B (PRD S17) and TDD NFR-SEC-001 with <500ms hash time; Argon2 superior but new operational burden; `PSS` abstraction preserves upgrade path|
|JWT algorithm|RS256 with 2048-bit RSA|HS256; ES256; EdDSA|RS256 enables public key distribution to API Gateway without shared secret; 2048-bit matches NIST floor; per TDD constraint; rotated quarterly via OPS-RSA-ROTATION|
|Rollout strategy|Three-phase w/ 2 flags (ANL, ATR)|Big-bang cutover; single flag|3-phase + named rollback triggers from TDD §19 mitigates R-003 high-severity data loss; enables 10% canary per MIG-002 success criteria|
|Audit RTN|12 months|TDD original 90 days|PRD S17 SOC2 Type II requires 12-month RTN; OQ-003 conflict resolved in favor of PRD (legal/business intent outweighs TDD default)|
|Refresh token storage|Hashed opaque in Redis, 7-day TTL|Plain refresh; DB-backed|Hashed-at-rest mitigates read-through compromise; Redis TTL gives automatic expiry; TKN revoke is O(1); DB-backed alternative fails NFR latency at concurrent load|
|Account lockout|5 attempts / 15-minute window|3/10min (tighter); 10/1hr (looser)|TDD FA0 specifies 5/15min; balances R-002 brute-force risk against PRD UX concern (PRD OQ "remember me" discussion)|
|CAPTCHA introduction|After 3 failed login attempts|Always on; never|Progressive friction: CAPTCHA only after abuse signal preserves NFR latency on happy path while mitigating R-002 brute force|
|Versioning scheme|URL prefix `/v1/auth/*`|Header-based; domain-based|URL prefix is simplest for the 4-endpoint surface; breaking changes require `/v2/*` per TDD constraint; supports future MFA/OAuth additions as additive fields|
|Migration safety|Idempotent upsert + pre-phase backup + parallel run|Cut-over with snapshot; blue-green DB|R-003 severity=High + TDD §19 prescription; parallel run on dual read/write resolves dup rows via idempotent key (email normalized lowercase)|
|Observability stack|Prometheus + OTel + Alertmanager|Datadog; New Relic|Matches TDD §20 tooling; already in house; SOC2 evidence easier from owned stack|

## Timeline Estimates

|MLS|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|DM-001/002 migrated; OQ-003 resolved; audit schema approved|
|M2|2 weeks|Week 3|Week 4|PSS/JWT/TKN implemented; THS unit-tested|
|M3|2 weeks|Week 5|Week 6|6 REST NDP live; OpenAPI 3.1 published; FA0..005 passing|
|M4|2 weeks|Week 7|Week 8|THP + LoginPage/RegisterPage/ProfilePage behind feature flag|
|M5|2 weeks|Week 9|Week 10|Performance SLOs validated; SOC2 dry-run passes; pen-test clean|
|M6|2 weeks|Week 11|Week 12|Test pyramid green (80/15/5); load + security suites in CI|
|M7|3 weeks|Week 13|Week 15|MIG-001 alpha (1w) → MIG-002 10% beta (2w) → MIG-003 GA (1w overlaps Week 15)|
|M8|1 week|Week 16|Week 16|Runbooks + on-call + key RTT + RTN jobs live|

**Total estimated duration:** 16 weeks (~4 months) from SEC-POLICY-001 sign-off to GA handover.

## Open Questions

|#|Question|Impact|Blocking MLS|Resolution Owner|
|---|---|---|---|---|
|1|OQ-001 (TDD): Should THS support API key auth for service-to-service calls?|Scope expansion; affects THS surface|Not blocking (deferred to v1.1)|test-lead|
|2|OQ-002 (TDD): Maximum `SRP.roles` array length?|DM-001 validator + storage; minor|M1 (DM-001 schema)|AT|
|3|OQ-003 (cross-doc): TDD 90-day vs PRD 12-month audit RTN — PRD wins; confirm before sizing|Storage sizing; NFR-COMP-002 scope; SOC2 evidence|M1 — MUST resolve before DEP-POSTGRES capacity and COMP-DM-AUDIT schema finalized|CMP + AT|
|4|OQ-004 (PRD): Sync vs async password reset email delivery?|OPS-002 runbook + EmailClient design|M2 (COMP-EMAILCLIENT)|engineering|
|5|OQ-005 (PRD): Max refresh tokens per user across devices?|Redis capacity (OPS-004); TKN data model|M2 (COMP-006-TM)|product|
|6|OQ-006 (PRD): Account lockout policy — partially answered (5/15min) — confirm with Security|COMP-LOCKOUT finalization|M2 (COMP-LOCKOUT)|security-lead|
|7|OQ-007 (PRD): Support "remember me" to extend session duration?|Token TTL design; THP storage strategy|Not blocking v1.0 (deferred to v1.1)|product|
|8|OQ-008 (JTBD coverage): PRD Jordan admin story — view event logs, lock/unlock accounts — not covered by TDD FA0..005. PRD requires; TDD should be updated|Scope decision for admin NDP (FR-AUTH-006 candidate)|M3 — decide before API surface frozen|product + CMP|
|9|Pen-test vendor booking slot|Delays M5 exit and MIG-001 start|M5 — vendor must be booked by Week 6|security-lead|
|10|Dual-store divergence threshold for MIG-002|Go/no-go gate between MIG-002 and MIG-003|M7 — tolerance agreed before 10% enablement|AT + SRE|

