<!-- CONV: AuthService=THS, TokenManager=TKN, PasswordHasher=PSS, Integration=NTG, ERROR-ENVELOPE=EE, register=RGS, Implement=MPL, JwtService=JWT, password=PA1, UserProfile=SRP, FR-AUTH-001=FA0, SendGrid=SND, AuthProvider=THP, COMP-006=C0, NFR-COMPLIANCE-001=NC0, PostgreSQL=PST, rate-limit=RL, retention=RTN, FR-AUTH-005=FRT, rotation=RTT -->
---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "A"
variant_scores: "A:86 B:75"
convergence_score: 0.65
debate_rounds: 2
generated: "2026-04-16"
generator: "adversarial_merge"
total_phases: 8
total_task_rows: 119
risk_count: 9
open_questions: 11

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service establishes the platform's identity layer, unblocking $2.4M of personalization-dependent revenue and satisfying the Q3 2026 SOC2 Type II audit. The v1.0 scope — registration, login, token refresh, profile retrieval, PA1 reset, logout — is explicitly bounded (no OAuth, MFA, or RBAC) so the critical path is short, auditable, and compliance-ready.

**Business Impact:** Unblocks Q2-Q3 2026 personalization roadmap (projected $2.4M ARR); enables SOC2 Type II audit trail with 12-month RTN; reduces 30% QoQ access-related support volume via self-service PA1 reset; captures GDPR consent at registration; resolves 25% churned-user feedback citing missing accounts.

**Complexity:** HIGH (0.72) — cross-cutting security (bcrypt-12, RS256/2048, refresh RTT, lockout), dual datastores (PST + Redis), external SND integration, phased rollout with feature flags, SOC2/GDPR/NIST SP 800-63B compliance burden, and backend/frontend coordination across `THP` silent refresh.

**Critical path:** Infra provisioning → `SRP` + `PSS` + `JWT` + baseline telemetry → `THS` (login/RGS) + uniform error envelope → `TKN` + refresh + logout → PA1 reset + email → Frontend (`THP` + pages + reset UI in parallel) → audit/observability maturation + admin → phased GA (Alpha → Beta 10% → 100%).

**Key architectural decisions:**

- Stateless JWT access tokens (15 min, RS256/2048) + opaque refresh tokens in Redis (7-day TTL, hashed-at-rest) — no server session store beyond Redis refresh records.
- `TKN` fails closed on Redis outage to prevent auth-bypass; users forced to re-login rather than silently extending expired sessions.
- bcrypt cost 12 isolated behind `PSS` abstraction to enable future migration (e.g., argon2id) without touching `THS`.
- Rate limiting enforced at API Gateway (not in-service) to protect `THS` from resource exhaustion before application-layer lockout kicks in.
- Uniform error envelope `{error:{code,message,status}}` across all `/v1/auth/*` endpoints to stabilize API consumer integrations (Sam persona).
- Audit log RTN set to 12 months (PRD/SOC2 authoritative) overriding TDD's 90-day figure; persisted in PST alongside `SRP` with formal reconciliation row.
- Baseline observability emission in Phase 1 (telemetry shapes against real traffic) + dedicated Phase 6 dashboard/alert maturation (partial convergence with velocity variant).

**Open risks requiring resolution before Phase 1:**

- OQ-005 (lockout policy confirmation — TDD 5/15min vs Security-team sign-off) must be resolved before `THS` lockout logic is coded.
- OQ-008 (audit RTN — PRD 12 months vs TDD 90 days) must be formally reconciled; PRD-over-TDD ruling logged in Phase 1 decision row.
- OQ-003 (reset email sync vs async) must be resolved before Phase 4 `THS.resetRequest` contract freezes.
- SND account provisioning + DKIM/SPF setup must complete before Phase 4 or PA1-reset flow is blocked (R-006).
- Quarterly RSA key RTT procedure must be documented and signed off by platform-team before `JWT` enters Phase 2; retrofitting RTT into a running deployment is high risk (R-008).

## Phase 0: Foundation & Infrastructure

**Phase 0** | M0 Infrastructure Baseline | Weeks 1-2 | Entry: TDD + PRD signed off; SEC-POLICY-001 available; cloud accounts provisioned | Exit: PST+Redis reachable from service mesh; CI green on empty repo; RSA keys + secrets in vault

|#|ID|Task|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|INFRA-PG|Provision PST 15 with HA replica|Infra|—|2-node primary+replica; pool-capacity:100; failover<30s; backup-daily|M|P0|
|2|INFRA-REDIS|Provision Redis 7 cluster with persistence|Infra|—|3-node; 1GB-initial; AOF-on; TTL-support; failover-tested|M|P0|
|3|INFRA-K8S|Configure K8s namespace+HPA for auth-service|Infra|—|min:3; max:10; cpu-trigger:70%; liveness+readiness-probes|M|P0|
|4|INFRA-NODE|Pin Node.js 20 LTS in Dockerfile+CI|Infra|—|node-version:20.x; multi-stage-build; non-root-user; image-scanned|S|P0|
|5|INFRA-TLS|Terminate TLS 1.3 at API Gateway|Sec|—|tls:1.3-only; hsts-on; cert-auto-renew; weak-ciphers-blocked|M|P0|
|6|INFRA-CORS|Configure CORS allowlist at gateway|Sec|INFRA-TLS|known-origins-only; credentials:true; wildcard-blocked|S|P0|
|7|INFRA-GW|Configure API Gateway RL rules|Sec|INFRA-TLS|login:10/min/ip; RGS:5/min/ip; me:60/min/user; refresh:30/min/user|M|P0|
|8|INFRA-RSA|Generate+rotate RS256 keypair in KMS|Sec|—|rsa-2048; kms-stored; quarterly-RTT-scheduled; public-key-jwks|M|P0|
|9|INFRA-SG|Provision SND account + DKIM/SPF|Infra|—|api-key-vaulted; dkim-verified; spf-verified; sender-domain-authenticated|M|P0|
|10|INFRA-CI|Bootstrap CI pipeline with testcontainers|Ops|INFRA-PG,INFRA-REDIS|lint+unit+integration-jobs; testcontainers-pg+redis; coverage-report|M|P0|
|11|INFRA-VAULT|Mount secrets (DB, Redis, RSA, SG) in K8s|Sec|INFRA-K8S,INFRA-RSA,INFRA-SG|sealed-secrets; no-env-plaintext; RTT-documented|M|P0|
|12|INFRA-OBS|Deploy Prometheus+Grafana+OTel collector|Ops|INFRA-K8S|prom-scrape-live; grafana-datasource-ok; otel-otlp-endpoint|M|P0|
|13|SEC-POLICY|Ratify SEC-POLICY-001 hashing+signing rules|Sec|—|bcrypt-cost:12-mandated; rs256-2048-mandated; cleartext-ban-in-logs|S|P0|

### NTG Points — Phase 0

|Artifact|Type|Wired|Phase|Consumed By|
|---|---|---|---|---|
|RSA keypair (kid)|Key RTT registry|INFRA-RSA|Phase 0|`JWT` (Phase 2)|
|Rate-limit policies|Gateway config map|INFRA-GW|Phase 0|`THS` endpoints (Phase 2-3)|
|Secret mounts|K8s sealed-secrets binding|INFRA-VAULT|Phase 0|`THS`, `TKN`, `EmailService` (all downstream)|
|OTel collector endpoint|Env var injection|INFRA-OBS|Phase 0|All backend components|

## Phase 1: Data Models, Core Security Primitives & Baseline Telemetry

**Phase 1** | M1a Data Layer + Primitives | Weeks 3-4 | Entry: Phase 0 exit met; PG+Redis reachable; RSA keys in KMS | Exit: `SRP`/`AuditLog`/`ResetToken` schemas live; `PSS`+`JWT`+`UserRepo` unit-tested; baseline telemetry emitting; PRD-vs-TDD decision log ratified

|#|ID|Task|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|DM-001|Create SRP table + constraints|DB|INFRA-PG|id:UUID-PK; email:unique-idx-lowercase-NOT-NULL; displayName:varchar-2-100-NOT-NULL; createdAt:timestamptz-default-now-NOT-NULL; updatedAt:timestamptz-auto-NOT-NULL; lastLoginAt:timestamptz-nullable; roles:text[]-default-[user]-NOT-NULL|M|P0|
|2|DM-001.idx|Add indexes on email + lastLoginAt|DB|DM-001|email-unique-btree; last-login-btree; explain-plan-verified|S|P0|
|3|DM-003|Create AuditLog table (PRD SOC2)|DB|INFRA-PG|id:UUID-PK; user_id:FK-nullable; event_type:enum; ip:inet; outcome:enum; created_at:timestamptz-index; RTN:12mo|M|P0|
|4|DM-004|Create ResetToken table|DB|INFRA-PG|id:UUID-PK; user_id:FK-NOT-NULL; token_hash:varchar-unique; expires_at:timestamptz; used_at:timestamptz-nullable; created_at:timestamptz|M|P0|
|5|MIG-DB-BASE|Author initial Knex/Prisma migration set|DB|DM-001,DM-003,DM-004|idempotent; up+down-reversible; checksum-locked; applied-via-CI|M|P0|
|6|COMP-008|MPL PSS (bcrypt cost 12)|Sec|SEC-POLICY,INFRA-NODE|deps:bcryptjs; methods:hash+verify; cost:12-enforced; pluggable-interface; hash<500ms|M|P0|
|7|NFR-SEC-001|Assert bcrypt cost factor 12 in unit test|Test|COMP-008|inspect-hash-prefix:$2b$12$; wrong-cost→test-fails; round-trip-verify-ok|S|P0|
|8|COMP-007|MPL JWT (RS256 sign/verify)|Sec|INFRA-RSA,SEC-POLICY|deps:jsonwebtoken+kms; algo:RS256; keysize:2048; clock-skew:5s; kid-in-header|M|P0|
|9|NFR-SEC-002|Assert RS256+2048 in config test|Test|COMP-007|algo-assert:RS256; keysize-assert:2048; hs256-rejected; unsigned-rejected|S|P0|
|10|COMP-009|MPL UserRepo (PG access layer)|DB|DM-001|methods:findByEmail+findById+insert+updateLastLogin+incrementFailedAttempts+lockAccount; pool-bounded; query-timeout:1s|L|P0|
|11|COMP-011|MPL AuditLogger component|Ops|DM-003|methods:record(userId,event,ip,outcome); async-batched; passwords-tokens-scrubbed; fire-and-forget|M|P0|
|12|COMP-012|MPL RateLimiter middleware hook|Sec|INFRA-GW|gateway-primary; in-service-fallback; 429-envelope; retry-after-header|M|P1|
|13|COMP-010|MPL EmailService (SND adapter)|API|INFRA-SG|methods:sendResetEmail; template-id-config; retry-on-5xx; delivery-id-logged|M|P1|
|14|COMP-005-skel|Scaffold THS class with DI|API|COMP-008,COMP-007,COMP-009,COMP-011|deps:PSS+TKN+JWT+UserRepo+AuditLogger; methods:login+RGS+getProfile+resetRequest+resetConfirm; email-lowercase-normalized|M|P0|
|15|OPS-005.baseline|Emit baseline telemetry shapes with real traffic|Ops|COMP-011,INFRA-OBS|json-logs-emitted; counters-registered:auth_login_total+auth_registration_total+auth_token_refresh_total; OTel-spans-bootstrapped; no-paging-yet|M|P0|
|16|PRE-OQ-005|Resolve lockout policy (OQ-005)|Gate|—|security-team-signoff-recorded; 5-attempts/15min-confirmed-or-revised; documented-in-TDD|S|P0|
|17|OQ-RECON-RET|Ratify PRD-over-TDD RTN ruling (OQ-008)|Docs|DM-003|RTN:12mo-confirmed-PRD-authoritative; TDD-90d-superseded; decision-log-entry-signed:compliance+product; audit-schema-reflects-12mo|S|P0|
|18|OQ-RECON-LOGOUT|Ratify logout as v1.0 scope (OQ-011)|Docs|—|logout:in-v1.0-scope-confirmed; TDD-update-logged; API-005-authorized; decision-log-signed:product+engineering|S|P0|

### NTG Points — Phase 1

|Artifact|Type|Wired|Phase|Consumed By|
|---|---|---|---|---|
|`PSS` interface|DI binding in container|COMP-008|Phase 1|`THS.login`, `THS.RGS`, `THS.resetConfirm`|
|`JWT` key loader|KMS → process secret provider|COMP-007|Phase 1|`TKN` (Phase 3), `/auth/me` verifier middleware|
|`UserRepo`|DI binding in container|COMP-009|Phase 1|`THS` (all methods)|
|`AuditLogger`|Async event emitter subscribed per auth event|COMP-011|Phase 1|`THS`, `TKN`, reset flow|
|`EmailService`|DI binding behind feature flag|COMP-010|Phase 1|`THS.resetRequest` (Phase 4)|
|`RateLimiter`|Middleware chain registration|COMP-012|Phase 1|`/auth/*` endpoints (Phase 2-3)|
|Baseline telemetry registry|Prom-client counters + OTel tracer provider|OPS-005.baseline|Phase 1|Phase 6 dashboard/alert maturation (OPS-005.dash/alert/trace)|
|PRD-vs-TDD decision log|Compliance/product signoff artifact|OQ-RECON-RET,OQ-RECON-LOGOUT|Phase 1|SOC2 dry-run evidence pack (SOC2-VALIDATION Phase 6)|

## Phase 2: Login & Registration Endpoints

**Phase 2** | M1 Core THS (2026-04-14) | Weeks 5-6 | Entry: Phase 1 primitives unit-tested; OQ-005 resolved; decision log ratified | Exit: FA0 + FR-AUTH-002 pass unit+integration tests; lockout enforced; RL wired; uniform error envelope on all auth endpoints

|#|ID|Task|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|FA0|MPL THS.login flow|API|COMP-005-skel,COMP-008,COMP-009|valid-creds→200+AuthToken; invalid→401; non-existent-email→401-no-enum; 5fail/15min→423-locked; lastLoginAt-updated|L|P0|
|2|FR-AUTH-002|MPL THS.RGS flow|API|COMP-005-skel,COMP-008,COMP-009|valid→201+SRP; duplicate-email→409; weak-pw→400; bcrypt-cost:12-persisted|L|P0|
|3|EE|MPL uniform error envelope|API|COMP-005-skel|shape:{error:{code,message,status}}; applied-all-/v1/auth/*; stable-codes:AUTH_INVALID_CREDENTIALS+AUTH_LOCKED+AUTH_RATE_LIMITED+AUTH_WEAK_PASSWORD+AUTH_EMAIL_CONFLICT+AUTH_UNAUTHORIZED; no-stack-traces; documented-in-OpenAPI|M|P0|
|4|API-001|Expose POST /v1/auth/login endpoint|API|FA0,COMP-012,EE|path:/v1/auth/login; body:{email,PA1}; 200:AuthToken; 401:invalid; 423:locked; 429:rate; RL:10/min/ip|M|P0|
|5|API-002|Expose POST /v1/auth/RGS endpoint|API|FR-AUTH-002,COMP-012,EE|path:/v1/auth/RGS; body:{email,PA1,displayName}; 201:SRP; 400:validation; 409:conflict; RL:5/min/ip|M|P0|
|6|COMP-005|Finalize THS (login+RGS paths)|API|FA0,FR-AUTH-002|deps-wired:PSS+UserRepo+AuditLogger; email-lowercased; lockout-counter-in-UserRepo; exceptions-mapped-to-status|L|P0|
|7|LOCKOUT|MPL 5-fail/15-min lockout window|Sec|FA0,COMP-009|sliding-window:15min; threshold:5; 423-after-lock; auto-unlock-after-window; admin-unlock-hook-stub|M|P0|
|8|PW-STRENGTH|Enforce NIST SP 800-63B PA1 policy|Sec|FR-AUTH-002|min-length:8; uppercase+digit-required; common-PA1-blocklist; inline-error-per-rule|M|P0|
|9|EMAIL-UNIQ|Enforce case-insensitive email uniqueness|DB|FR-AUTH-002,DM-001|lowercased-at-persist; citext-or-lowercase-index; race-safe-insert|S|P0|
|10|NO-ENUM|Suppress user enumeration in error envelope|Sec|FA0,EE|wrong-email+wrong-pw→identical-401-message; timing-normalized; dummy-hash-compare-on-miss|M|P0|
|11|GDPR-CONSENT|Record GDPR consent at registration|Data|FR-AUTH-002,DM-003|consent-timestamp-stored; consent-version-tracked; audit-event-logged|M|P0|
|12|TEST-001|Unit test login valid credentials|Test|FA0|PSS.verify-called; TKN.issue-called; AuthToken-returned|S|P0|
|13|TEST-002|Unit test login invalid credentials|Test|FA0|verify→false; 401-returned; no-token-issued; lockout-counter-incremented|S|P0|
|14|TEST-004|NTG test registration persists|Test|API-002,COMP-009|testcontainer-pg; POST→201; row-in-SRP; bcrypt-hash-stored; audit-row-written|M|P0|
|15|AUDIT-LOGIN|Wire audit events for login+RGS|Ops|FA0,FR-AUTH-002,COMP-011|events:login_success+login_fail+RGS; fields:user_id+ip+ts+outcome; no-plaintext-PA1|M|P0|

### NTG Points — Phase 2

|Artifact|Type|Wired|Phase|Consumed By|
|---|---|---|---|---|
|`THS.login`|Route handler binding `POST /v1/auth/login`|API-001|Phase 2|API Gateway → `LoginPage` (Phase 5)|
|`THS.RGS`|Route handler binding `POST /v1/auth/RGS`|API-002|Phase 2|API Gateway → `RegisterPage` (Phase 5)|
|Error envelope formatter|Middleware chain registered before route handlers|EE|Phase 2|All `/v1/auth/*` endpoints, Sam persona (API consumer)|
|Lockout counter|Redis + UserRepo column wiring|LOCKOUT|Phase 2|`THS.login`, admin unlock (Phase 6 ADMIN-UNLOCK)|
|Password policy validator|Strategy plugin registered in `THS`|PW-STRENGTH|Phase 2|`THS.RGS`, `THS.resetConfirm`|
|Audit event bus|Async subscription `THS → AuditLogger`|AUDIT-LOGIN|Phase 2|SOC2 audit log|

## Phase 3: Token Lifecycle & Profile Retrieval

**Phase 3** | M2 Token Management (2026-04-28) | Weeks 7-8 | Entry: Phase 2 login+RGS green in staging | Exit: FR-AUTH-003 + FR-AUTH-004 pass; refresh RTT on; logout invalidates; /auth/me returns profile; multi-device policy ratified

|#|ID|Task|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|DM-002|Define AuthToken DTO contract|API|COMP-007|accessToken:JWT-RS256-signed-NOT-NULL; refreshToken:opaque-unique-NOT-NULL; expiresIn:number-NOT-NULL-eq-900; tokenType:string-eq-Bearer|S|P0|
|2|C0|MPL TKN lifecycle|API|COMP-007,INFRA-REDIS|deps:JWT+Redis; methods:issueTokens+refresh+revoke+verifyRefresh; refresh-hashed-at-rest; ttl:7d; RTT-on-refresh; fail-closed-on-redis-down|L|P0|
|3|FR-AUTH-003|MPL JWT issue + refresh flow|API|C0,FA0|login→AuthToken-pair; access-ttl:15min; refresh-ttl:7d; POST-refresh→new-pair+old-revoked; expired→401; revoked→401|L|P0|
|4|FR-AUTH-004|MPL /auth/me profile retrieval|API|COMP-005,COMP-007|valid-token→200+SRP; expired→401; invalid→401; response:id+email+displayName+createdAt+updatedAt+lastLoginAt+roles|M|P0|
|5|API-003|Expose GET /v1/auth/me endpoint|API|FR-AUTH-004,EE|path:/v1/auth/me; header:Authorization-Bearer; 200:SRP; 401:missing-expired-invalid; RL:60/min/user|M|P0|
|6|API-004|Expose POST /v1/auth/refresh endpoint|API|FR-AUTH-003,EE|path:/v1/auth/refresh; body:{refreshToken}; 200:AuthToken; 401:expired-or-revoked; RL:30/min/user; old-token-revoked-atomically|M|P0|
|7|API-005|Expose POST /v1/auth/logout (PRD gap)|API|C0,EE,OQ-RECON-LOGOUT|path:/v1/auth/logout; body:{refreshToken}; 204:success; refresh-revoked-in-redis; audit-event:logout; RL:30/min/user|M|P0|
|8|REDIS-REFRESH|Persist hashed refresh tokens in Redis|DB|INFRA-REDIS,C0|key:refresh:{sha256(token)}; value:{user_id,issued_at,kid}; ttl:604800s; keyspace-notify-on-expire|M|P0|
|9|CLOCK-SKEW|Apply 5s clock skew tolerance|Sec|COMP-007|iat/exp-tolerance:5s; library-option-asserted; test-covers-bounds|S|P1|
|10|REVOKE-ON-PW|Revoke all refresh tokens on PA1 change|Sec|C0,FR-AUTH-003|PRD:new-pw-invalidates-all-sessions; delete-all-user-refresh-keys; audit-event:bulk_revoke|M|P0|
|11|KID-ROTATION|Support key-id header for RSA RTT|Sec|COMP-007,INFRA-RSA|kid-in-jwt-header; jwks-endpoint-exposes-all-active-kids; old-kid-accepted-until-expiry|M|P1|
|12|OQ-RECON-MULTIDEV|Ratify multi-device session policy (OQ-009)|Docs|C0|policy-decided:unlimited|bounded-N|user-managed; Redis-keying-aligned; logout-scope-defined:single-device|all-devices; decision-log-signed:product+security|S|P0|
|13|TEST-003|Unit test TKN refresh|Test|C0|valid-refresh→new-pair; old-revoked-in-redis; JWT.sign-called-with-new-iat|S|P0|
|14|TEST-005|NTG test expired refresh rejected|Test|C0,INFRA-REDIS|testcontainer-redis; ttl-elapsed→401; revoked-key-removed-from-redis|M|P0|
|15|AUDIT-TOKEN|Wire audit events for refresh+logout|Ops|C0,COMP-011|events:token_refresh+logout+bulk_revoke; outcome+user_id+ip; no-token-in-log|S|P0|

### NTG Points — Phase 3

|Artifact|Type|Wired|Phase|Consumed By|
|---|---|---|---|---|
|`TKN`|DI binding; injected into `THS`|C0|Phase 3|`THS.login`, `/auth/refresh`, `/auth/logout`, `THP` silent refresh|
|JWT verifier middleware|Express/Nest middleware registered for protected routes|API-003|Phase 3|`GET /auth/me` and future protected endpoints|
|Redis refresh keyspace|Keyspace-notifications subscription|REDIS-REFRESH|Phase 3|`TKN` revocation, observability metrics|
|JWKS endpoint|Public discovery route `/v1/auth/.well-known/jwks.json`|KID-ROTATION|Phase 3|External verifiers, Sam (API consumer persona)|
|Multi-device policy ruling|Decision log → TKN key scheme|OQ-RECON-MULTIDEV|Phase 3|`TKN`, logout flow, future device-management UX|

## Phase 4: Password Reset & Email NTG

**Phase 4** | M3 Password Reset (2026-05-12) | Weeks 9-10 | Entry: Phase 3 tokens stable; SND DKIM/SPF verified; OQ-003 resolved | Exit: FRT end-to-end; reset tokens one-time + 1h TTL; PA1 change revokes all sessions; frontend reset screens begin in parallel (see Phase 5 RESET-UI)

|#|ID|Task|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|FRT|MPL two-step PA1 reset|API|COMP-005,COMP-010,DM-004|reset-request→email-sent+token-persisted; reset-confirm→PA1-updated+hash-rotated; ttl:1h; one-time-use|L|P0|
|2|API-006|Expose POST /v1/auth/reset-request|API|FRT,COMP-010,EE|path:/v1/auth/reset-request; body:{email}; 200-generic-regardless-of-account; RL:3/min/ip; email-sent<60s|M|P0|
|3|API-007|Expose POST /v1/auth/reset-confirm|API|FRT,EE|path:/v1/auth/reset-confirm; body:{token,newPassword}; 200:success; 400:invalid-or-expired; 400:weak-PA1; used-token→400|M|P0|
|4|RESET-TOKEN-GEN|Generate cryptographically-secure reset tokens|Sec|DM-004|csprng:32-bytes-base64url; sha256-at-rest; unguessable; entropy>=256bit|S|P0|
|5|RESET-TTL|Enforce 1-hour reset token expiry|Sec|DM-004,FRT|expires_at:now+1h; expired→400; cleanup-job-purges-expired-daily|M|P0|
|6|RESET-ONETIME|Mark used reset tokens non-reusable|Sec|DM-004|used_at-set-atomically; replay→400; concurrent-use-serializable|M|P0|
|7|RESET-REVOKE|Invalidate all sessions on PA1 change|Sec|REVOKE-ON-PW,FRT|PRD:new-pw-invalidates-all-existing-sessions; bulk-refresh-revoke; audit-event-emitted|M|P0|
|8|EMAIL-TEMPLATE|Build reset email template + content|Docs|COMP-010|link-contains-token-only; brand-header; expiry-stated; support-contact; dkim-signed|M|P1|
|9|EMAIL-DELIVERY|Monitor SND delivery + bounces|Ops|COMP-010|delivery-webhook-ingested; bounce-alert-on-spike; fallback-channel-documented-for-R-006|M|P1|
|10|NO-ENUM-RESET|Generic response on reset-request|Sec|API-006|registered+unregistered→same-200; no-timing-side-channel; audit-records-both-cases|S|P0|
|11|AUDIT-RESET|Wire audit events for reset flow|Ops|FRT,COMP-011|events:reset_request+reset_confirm+reset_token_used; outcome+user_id+ip+ts|S|P0|

### NTG Points — Phase 4

|Artifact|Type|Wired|Phase|Consumed By|
|---|---|---|---|---|
|`EmailService.sendResetEmail`|Invoked from `THS.resetRequest`|FRT|Phase 4|Reset request API, EMAIL-DELIVERY monitoring|
|Reset-token cleanup job|Scheduled worker (cron)|RESET-TTL|Phase 4|PST `ResetToken` table|
|Bulk-revoke hook|Event listener on PA1-changed event|RESET-REVOKE|Phase 4|`TKN` refresh store|
|Webhook ingest|SND events → internal queue|EMAIL-DELIVERY|Phase 4|Observability dashboards, on-call alerting|

## Phase 5: Frontend NTG

**Phase 5** | M4 Frontend NTG (2026-05-26) | Weeks 11-12 | Entry: Phase 4 backend APIs stable in staging; RESET-UI may start in parallel mid-Phase 4 against mocked endpoints | Exit: `LoginPage` + `RegisterPage` + `ProfilePage` + reset screens ship behind `AUTH_NEW_LOGIN`; silent refresh works across tabs

|#|ID|Task|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|COMP-004|MPL THP context + silent refresh|FE|API-003,API-004|props:children:ReactNode; state:AuthToken+SRP; methods:login+logout+refresh+getMe; intercepts-401→refresh-or-redirect; exposes-useAuth-hook|L|P0|
|2|COMP-001|Build LoginPage (/login)|FE|API-001,COMP-004|props:onSuccess+redirectUrl; form:email+PA1; inline-validation; submit→POST-login; stores-AuthToken-via-THP; loading+error-states|L|P0|
|3|COMP-002|Build RegisterPage (/RGS)|FE|API-002,COMP-004|props:onSuccess+termsUrl; form:email+PA1+displayName; client-strength-validation; POST-RGS; duplicate-email-error|L|P0|
|4|COMP-003|Build ProfilePage (/profile)|FE|API-003,COMP-004|auth-required; fetches-GET-me; displays:displayName+email+createdAt; loading+error-states|M|P0|
|5|PUB-ROUTES|Configure PublicRoutes wrapping login+RGS|FE|COMP-001,COMP-002|redirects-authenticated-users-to-/profile; loads-without-token; bundle-code-split|M|P1|
|6|PROT-ROUTES|Configure ProtectedRoutes wrapping profile|FE|COMP-003,COMP-004|unauthenticated→redirect-/login-with-returnTo; checks-via-THP|M|P0|
|7|REFRESH-COOKIE|Store refresh token in HttpOnly SameSite cookie|Sec|COMP-004,API-001|HttpOnly:true; Secure:true; SameSite:Strict; path:/v1/auth; cleared-on-logout; R-001-mitigation|M|P0|
|8|ACCESS-MEMORY|Keep access token in memory only|Sec|COMP-004|not-in-localStorage; not-in-cookie; cleared-on-tab-close; R-001-mitigation|M|P0|
|9|FE-401-INTERCEPT|Intercept 401 and trigger silent refresh|FE|COMP-004,API-004|axios/fetch-interceptor; single-inflight-refresh; queue-requests-during-refresh; redirect-on-refresh-fail|L|P0|
|10|RESET-UI|Build forgot-PA1 + set-new-PA1 screens|FE|API-006,API-007|/forgot-PA1:email-form→confirmation-screen; /reset-confirm:token-from-query+newPassword; generic-success-message; dev-mocked-APIs-allowed-mid-Phase-4|M|P0|
|11|LOGOUT-UI|Wire logout button to /auth/logout|FE|API-005,COMP-004|calls-logout-API; clears-THP-state; redirects-/login; refresh-cookie-cleared|S|P0|
|12|TEST-006|E2E test full user journey (Playwright)|Test|COMP-001,COMP-002,COMP-003,COMP-004,RESET-UI|RGS→login→profile→reset-request→reset-confirm→login→refresh→logout; runs-against-staging; <45s-runtime|L|P0|
|13|FE-A11Y|Accessibility pass on auth pages|FE|COMP-001,COMP-002,COMP-003|wcag-aa; keyboard-nav; screen-reader-labels; error-announcements|M|P1|

### NTG Points — Phase 5

|Artifact|Type|Wired|Phase|Consumed By|
|---|---|---|---|---|
|`useAuth` hook|React Context consumer exported from `THP`|COMP-004|Phase 5|All protected pages, logout button, navbar|
|HTTP 401 interceptor|Axios/fetch middleware registered by `THP`|FE-401-INTERCEPT|Phase 5|Every authenticated API call|
|Route guards|`PublicRoutes` / `ProtectedRoutes` wrapper components|PUB-ROUTES,PROT-ROUTES|Phase 5|Router tree `App → THP → Routes`|
|Refresh cookie|Browser cookie jar on `/v1/auth` path|REFRESH-COOKIE|Phase 5|`/auth/refresh`, `/auth/logout`|
|Reset screens|Parallel dev track against Phase 4 mocked endpoints|RESET-UI|Phase 4-5|Alex persona (end user) PA1 recovery|

## Phase 6: Compliance, Observability & Admin Tooling

**Phase 6** | M4b Audit + Admin | Weeks 13-14 | Entry: Phase 5 frontend in staging; all auth events emitted; OQ-010 gate resolved | Exit: SOC2 audit queryable; Jordan persona JTBD closed; dashboards + alerts green in staging; TEST-010 audit-completeness passes

|#|ID|Task|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|NC0|Ship SOC2/GDPR/NIST audit-log schema|Ops|DM-003,COMP-011|fields:user_id+event+ip+ts+outcome; RTN:12mo; immutable-partitioned-monthly; scrubs-secrets|L|P0|
|2|PRE-OQ-010|Gate admin unlock scope (OQ-010)|Gate|—|product+security-signoff-recorded; decision:commit-ADMIN-UNLOCK-v1.0-or-defer-v1.1; if-defer→ADMIN-UNLOCK-removed-from-phase; decision-log-signed|S|P0|
|3|API-008|Admin audit-log query endpoint (PRD JTBD)|API|DM-003,NC0,EE|path:/v1/admin/audit-logs; auth:admin-role; query:date-range+user_id; paginated; rate-limited; audit-of-audit-access|L|P0|
|4|ADMIN-UNLOCK|Admin account unlock endpoint|API|LOCKOUT,PRE-OQ-010|path:/v1/admin/users/{id}/unlock; auth:admin-role; clears-lock-counter; emits-audit-event; rate-limited; conditional-on-PRE-OQ-010=commit|M|P1|
|5|DATA-MIN|Enforce GDPR data-minimization audit|Sec|DM-001|only-email+hash+displayName+roles-persisted; pii-scanner-in-ci; schema-change-requires-compliance-review|M|P0|
|6|NIST-PW|Validate NIST SP 800-63B compliance in tests|Sec|PW-STRENGTH,COMP-008|breach-corpus-check; min-8-enforced; no-hints; one-way-hash-verified|M|P0|
|7|OPS-005|Structured logging + no-secrets scrubber|Ops|COMP-011,OPS-005.baseline|json-logs; PA1-token-scrubbed-via-regex; pii-redacted; correlation-id-propagated|M|P0|
|8|OPS-005.metrics|Mature Prometheus counters + histograms|Ops|INFRA-OBS,OPS-005.baseline|auth_login_total-per-outcome; auth_login_duration_seconds-histogram; auth_token_refresh_total-per-outcome; auth_registration_total|M|P0|
|9|OPS-005.trace|Instrument OTel spans across THS|Ops|INFRA-OBS,OPS-005.baseline|spans:THS→PSS+TKN+JWT; sampled:10%; trace-id-in-logs|M|P0|
|10|OPS-005.dash|Build Grafana dashboards|Ops|OPS-005.metrics|panels:login-rate+latency+refresh-rate+reg-rate; per-endpoint-p95; error-rate|M|P0|
|11|OPS-005.alert|Configure Prometheus alert rules|Ops|OPS-005.dash|login-fail>20%/5m; p95>500ms; redis-fail>10/min; pager-ok|M|P0|
|12|NFR-REL-001|Wire uptime SLO + synthetic checks|Ops|OPS-005.alert|99.9%/30d-rolling-window; synthetic-login-every-60s; slo-error-budget-tracked|M|P0|
|13|NFR-PERF-001|APM tracing asserts p95<200ms|Ops|OPS-005.trace|per-endpoint-p95-recorded; sli-dashboard-published; breach-alerts-configured|M|P0|
|14|OPS-004|Document capacity plan + HPA triggers|Docs|INFRA-K8S,INFRA-REDIS|3→10-replicas; pg-pool:100→200-if-wait>50ms; redis:1→2GB-if>70%util; runbook-linked|M|P1|
|15|TEST-010|Verify audit log completeness vs SOC2 fields|Test|NC0,API-008,AUDIT-LOGIN,AUDIT-TOKEN,AUDIT-RESET|events:login+RGS+refresh+reset+logout+unlock; fields:user_id+event_type+ip+ts+outcome; RTN-partition:12mo; assert-query-by-user+date; regression-test-in-CI|M|P0|
|16|SOC2-VALIDATION|Compliance dry-run against SOC2 controls|Gate|NC0,API-008,TEST-010,OQ-RECON-RET|controls-cc6.1+cc6.6+cc7.2-evidence-collected; 12mo-RTN-verified; PRD-over-TDD-decision-log-included; signoff:compliance-team|M|P0|

### NTG Points — Phase 6

|Artifact|Type|Wired|Phase|Consumed By|
|---|---|---|---|---|
|Admin audit API|Route registered `/v1/admin/audit-logs` with RBAC middleware|API-008|Phase 6|Jordan persona (admin UI, future work)|
|Admin unlock endpoint|Route registered `/v1/admin/users/{id}/unlock` conditional on PRE-OQ-010|ADMIN-UNLOCK|Phase 6|Jordan persona, support on-call|
|Prometheus metric registry|`prom-client` registry export on `/metrics` (matures from OPS-005.baseline)|OPS-005.metrics|Phase 6|Grafana, alertmanager|
|OTel span processor|OTel SDK tracer provider registered at service bootstrap (matures from OPS-005.baseline)|OPS-005.trace|Phase 6|Observability backend (Tempo/Jaeger)|
|Alertmanager routes|Prom alert rules → on-call PagerDuty|OPS-005.alert|Phase 6|Auth-team on-call RTT|
|SOC2 evidence pack|Compliance artifact pipeline|SOC2-VALIDATION|Phase 6|Q3 2026 SOC2 Type II audit|

## Phase 7: Hardening, Migration & GA Rollout

**Phase 7** | M5 GA Release (2026-06-09) | Weeks 15-16 | Entry: Phase 6 observability green in staging; compliance signed off | Exit: 99.9% uptime first 7 days; feature flags cleaned; legacy auth deprecated; post-mortem playbook validated

|#|ID|Task|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|NFR-PERF-002|Run k6 load test 500 concurrent|Test|NFR-PERF-001|k6-ramp:0→500-users; p95<200ms; error-rate<0.1%; sustained-5min|L|P0|
|2|PENTEST|Security review + penetration test|Sec|COMP-005,C0,COMP-007|owasp-top10-coverage; jwt-none-alg-rejected; replay-attacks-blocked; report-filed; criticals-zero|L|P0|
|3|CAPTCHA|CAPTCHA after 3 failed login attempts|Sec|FA0|trigger:3-fails-per-session; captcha-challenge-required; bypass-rate<1%; R-002-mitigation|M|P1|
|4|WAF-RULES|Deploy WAF IP-block rules|Sec|INFRA-GW|known-bad-ips-blocked; bot-sig-rules-on; log-only-first-48h; R-002-mitigation|M|P1|
|5|FLAG-NEW-LOGIN|Provision AUTH_NEW_LOGIN feature flag|Ops|COMP-001,COMP-002,COMP-005|default:OFF; percentage-rollout-controls; audit-on-toggle; cleanup:after-phase-3-GA|S|P0|
|6|FLAG-REFRESH|Provision AUTH_TOKEN_REFRESH feature flag|Ops|C0|default:OFF; when-off:access-only; cleanup:GA+2weeks; audit-on-toggle|S|P0|
|7|MIG-001|Phase 1 Internal Alpha on staging|Infra|FLAG-NEW-LOGIN|1-week; zero-P0/P1-bugs; manual-qa-auth-team; exit→feature-flag-togglable; rollback:disable-flag|M|P0|
|8|MIG-002|Phase 2 Beta at 10% traffic|Infra|MIG-001|2-weeks; p95<200ms; error-rate<0.1%; zero-redis-failures; monitor-THP-under-load; rollback:flag-to-0%|L|P0|
|9|MIG-003|Phase 3 GA at 100% + legacy deprecation|Infra|MIG-002|1-week; uptime:99.9%/7d-first-week; dashboards-green; AUTH_NEW_LOGIN-removed; legacy-endpoints-deprecated|L|P0|
|10|OPS-001|Publish runbook — THS down|Docs|OPS-005.alert|symptoms+diagnosis+resolution-documented; owner:auth-team; escalation:platform-team-after-15min; drill-completed|M|P0|
|11|OPS-002|Publish runbook — token refresh failures|Docs|OPS-005.alert|symptoms:logouts+401-loops; diagnosis:redis+jwks+flag; resolution:scale+remount+toggle; drill-completed|M|P0|
|12|OPS-003|Activate 24/7 on-call RTT (first 2 weeks)|Ops|OPS-001,OPS-002|p1-ack<15min; auth-team-RTT-scheduled; mttr-target:<60min; tooling:k8s+grafana+redis+pg|M|P0|
|13|ROLLBACK-PROC|Document + drill rollback procedure|Docs|MIG-003|6-step-sequence; smoke-test-legacy; log-investigation; pg-restore-if-needed; incident-channel-notify; post-mortem<48h|M|P0|
|14|ROLLBACK-TRIG|Encode rollback triggers as alerts|Ops|OPS-005.alert,ROLLBACK-PROC|p95>1000ms/5min; err-rate>5%/2min; redis-fail>10/min; data-loss→auto-page|M|P0|
|15|BACKUP-PRE|Pre-phase PST backup + restore drill|Ops|INFRA-PG|snapshot-before-each-phase; pitr-window:7d; restore-drill-passes; R-003-mitigation|M|P0|
|16|LEGACY-DEPRECATE|Publish deprecation notice for legacy auth|Docs|MIG-003|90-day-sunset-announced; api-consumers-notified; stats-tracked-per-week|M|P1|
|17|POST-GA-VERIFY|7-day post-GA SLO verification|Gate|MIG-003|uptime:99.9%; p95<200ms-sustained; reg-conv>60%; fail-login<5%; retrospective-held|M|P0|
|18|FLAG-CLEANUP|Remove AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH|Ops|POST-GA-VERIFY|dead-code-removed; flag-config-pruned; audit-logged; rollback-path-deprecated|M|P1|

### NTG Points — Phase 7

|Artifact|Type|Wired|Phase|Consumed By|
|---|---|---|---|---|
|`AUTH_NEW_LOGIN` flag|LaunchDarkly/Unleash/internal flag dispatch|FLAG-NEW-LOGIN|Phase 7|`THS` login path, `LoginPage` route|
|`AUTH_TOKEN_REFRESH` flag|Flag dispatch table|FLAG-REFRESH|Phase 7|`TKN.refresh`, `THP` silent-refresh|
|Rollback trigger hooks|Alertmanager → runbook automation webhook|ROLLBACK-TRIG|Phase 7|Auth-team on-call, automated flag-flip|
|Legacy deprecation banner|API Gateway response-header injector|LEGACY-DEPRECATE|Phase 7|Sam persona (API consumer integrations)|

## Risk Assessment and Mitigation

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-001|Token theft via XSS allows session hijacking|HIGH|Medium|High|Access token in memory only (ACCESS-MEMORY); HttpOnly+SameSite cookie for refresh (REFRESH-COOKIE); 15-min access TTL; `TKN` revoke-on-suspect; force PA1 reset for affected accounts|security|
|R-002|Brute-force attacks on /auth/login|MEDIUM|High|Medium|Gateway RL 10/min/ip (INFRA-GW); account lockout 5/15min (LOCKOUT); bcrypt cost 12; CAPTCHA after 3 fails (CAPTCHA); WAF IP block (WAF-RULES)|security|
|R-003|Data loss during legacy auth migration|HIGH|Low|High|Parallel operation Phase 1-2 (MIG-001/MIG-002); idempotent upserts; pre-phase PG snapshot (BACKUP-PRE); restore drill rehearsed|platform|
|R-004|Redis unavailability disables refresh flow|MEDIUM|Medium|Medium|`TKN` fails closed → forced re-login (C0); redis cluster + monitoring (INFRA-REDIS, OPS-005.alert); HPA scale-out runbook (OPS-002)|platform|
|R-005|Clock skew breaks JWT validation|LOW|Low|Low|`JWT` 5s tolerance (CLOCK-SKEW); ntp on all nodes; bound-test in CI|auth-team|
|R-006|Email delivery failure blocks PA1 reset|MEDIUM|Medium|High|SND delivery webhook + bounce alerting (EMAIL-DELIVERY); fallback support channel documented; multi-region SND pool|auth-team|
|R-007|Compliance failure from incomplete audit logging|HIGH|Medium|High|Audit schema defined Phase 1 (DM-003); event coverage Phase 2-4 (AUDIT-LOGIN/TOKEN/RESET); TEST-010 SOC2 field coverage; SOC2 dry-run gate (SOC2-VALIDATION); 12-month RTN enforced; PRD-vs-TDD decision log (OQ-RECON-RET)|compliance|
|R-008|RSA key compromise|HIGH|Low|Critical|Quarterly RTT (INFRA-RSA, KID-ROTATION); KMS-stored private key; JWKS publishes `kid`; revocation playbook signed off pre-Phase-2|security|
|R-009|Refresh-token-RTT race causes user lockout|MEDIUM|Medium|Medium|Atomic Redis swap (REDIS-REFRESH); single-inflight-refresh on FE (FE-401-INTERCEPT); grace window for in-flight requests|auth-team|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Phase|Status|Fallback|
|---|---|---|---|
|PST 15+ (HA + replica)|Phase 0|Provisioning (INFRA-PG)|Read-replica failover (OPS-001); restore from PITR snapshot (BACKUP-PRE)|
|Redis 7+ cluster|Phase 0|Provisioning (INFRA-REDIS)|`TKN` fails closed; users re-login until cluster restored|
|Node.js 20 LTS runtime|Phase 0|Pinned in Dockerfile|Pin previous LTS image; revert deployment via K8s rollback|
|bcryptjs library|Phase 1|Available in npm|Vendored snapshot in lockfile; replaceable behind `PSS`|
|jsonwebtoken library|Phase 1|Available in npm|Vendored snapshot; replaceable behind `JWT`|
|SND API + verified sender domain|Phase 4|Provisioning (INFRA-SG)|SES or Postmark adapter behind `EmailService`; manual support escalation|
|API Gateway (RL + CORS + TLS)|Phase 0|In place|Service-side fallback rate limiter (COMP-012); manual block rules|
|SEC-POLICY-001 (security policy doc)|Phase 1|Ratification pending (SEC-POLICY)|Block Phase 1 start until ratified — non-bypassable|
|KMS for RSA key custody|Phase 0|Provisioning (INFRA-RSA)|Encrypted-at-rest secrets file with stricter access controls; manual RTT|
|Compliance team review capacity|Phase 6|Scheduled SOC2 dry-run|Slip GA by ≤1 week if signoff delayed|
|Product + Security decision capacity (OQ-010)|Phase 6|Scheduled PRE-OQ-010 gate|Defer ADMIN-UNLOCK to v1.1 with scope note|

### Infrastructure Requirements

- Kubernetes cluster with HPA enabled (3→10 auth-service replicas, CPU>70% trigger).
- PST 15+ primary + replica with daily backup, 7-day PITR window.
- Redis 7+ cluster with AOF persistence, ≥1 GB initial capacity, scale to 2 GB at >70% utilization.
- API Gateway terminating TLS 1.3, enforcing CORS allowlist, and applying per-endpoint rate limits.
- KMS-backed RSA-2048 keypair with quarterly RTT.
- Prometheus + Grafana + OpenTelemetry collector for metrics, dashboards, traces (baseline in Phase 1, maturation in Phase 6).
- SND account with DKIM/SPF on the sender domain.
- Sealed-secrets controller in K8s for DB, Redis, RSA, SND credentials.
- CI pipeline with testcontainers for ephemeral PST + Redis on every PR.
- Staging cluster mirrored from production for MIG-001 internal alpha gating.

### Team & Skills

- Backend engineers (2): Node.js 20, PST, Redis, JWT, bcrypt; own `THS`, `TKN`, `PSS`, `JWT`.
- Frontend engineers (1-2): React, Context API, route guards; own `THP`, pages, silent refresh, reset UI parallel track.
- Platform/SRE engineer (1): K8s, HPA, Prometheus, Grafana, OTel, SND; own baseline telemetry + observability maturation + runbooks.
- Security engineer (≥0.5 FTE): policy ratification, pentest coordination, audit evidence; own R-001/R-002/R-008.
- Compliance lead: SOC2 dry-run, GDPR consent review, RTN enforcement, PRD-vs-TDD decision log custody; owns R-007.
- QA engineer (1): unit/integration coverage, k6 load test, Playwright E2E across RGS→login→reset→logout, accessibility.
- Auth-team on-call RTT (≥4 engineers) for first 2 weeks post-GA.

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Phase|
|---|---|---|---|---|
|Login latency (NFR-PERF-001)|p95 `THS.login()`|< 200ms|APM histogram `auth_login_duration_seconds`|Phase 6-7|
|Concurrent auth throughput (NFR-PERF-002)|k6 sustained users|≥ 500 with p95 < 200ms|k6 load test (NFR-PERF-002 row)|Phase 7|
|Service availability (NFR-REL-001)|Uptime over 30-day rolling window|≥ 99.9%|Synthetic login probe + SLO dashboard (NFR-REL-001 row)|Phase 6-7|
|Password hashing cost (NFR-SEC-001)|bcrypt cost factor|= 12|Unit test + hash prefix inspection|Phase 1|
|Token signing algorithm (NFR-SEC-002)|JWT header `alg` + key size|RS256 + 2048-bit|Config assertion test|Phase 1|
|Audit logging completeness (NC0)|% of auth events with full fields|100%|TEST-010 regression + SOC2 dry-run (SOC2-VALIDATION)|Phase 6|
|Audit log RTN (NC0)|Retention window|12 months (PRD authoritative)|PG partition + lifecycle policy audit + OQ-RECON-RET decision log|Phase 6|
|Test coverage|Unit coverage across core components|> 80%|Jest coverage report in CI|Phase 1-4|
|Token refresh latency|p95 `TKN.refresh()`|< 100ms|APM histogram `auth_token_refresh_total`|Phase 3-7|
|Password hash operation (NFR-SEC-001)|`PSS.hash()` duration|< 500ms|Benchmark in unit test|Phase 1|
|Registration conversion (PRD S19)|Landing→RGS→confirmed funnel|> 60%|Product analytics funnel|Post-GA (Phase 7)|
|Daily active authenticated users (PRD)|DAU with valid session|> 1000 within 30d of GA|Refresh-event analytics rollup|Post-GA (Phase 7)|
|Average session duration (PRD S19)|Refresh-event-derived session length|> 30 minutes|`auth_token_refresh_total` analytics|Post-GA (Phase 7)|
|Failed login rate (PRD S19)|fail / total logins|< 5%|`auth_login_total{outcome=fail}`|Post-GA (Phase 7)|
|Password reset completion (PRD)|reset requested → new PA1 set|> 80%|Reset-event funnel|Post-GA (Phase 7)|
|No user enumeration|Identical 401 for wrong-email vs wrong-PA1|timing delta < 10ms|Pentest case (PENTEST)|Phase 7|
|GDPR consent capture|Consent recorded at registration|100% of new accounts|Row-level audit check on `SRP`|Phase 2 + SOC2|
|Error envelope stability (Sam persona)|Uniform `{error:{code,message,status}}` shape|100% of /v1/auth/* responses|Contract test in CI|Phase 2|

## Timeline Estimates

|Phase|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|Phase 0|2 weeks|Week 1|Week 2|M0 Infrastructure Baseline — PG+Redis+K8s+TLS+RSA+SND provisioned|
|Phase 1|2 weeks|Week 3|Week 4|M1a Data Layer + Primitives + Baseline Telemetry + Decision-Log Ratification|
|Phase 2|2 weeks|Week 5|Week 6|M1 Core THS (2026-04-14) — login + RGS + uniform error envelope|
|Phase 3|2 weeks|Week 7|Week 8|M2 Token Management (2026-04-28) — refresh + /auth/me + logout + multi-device policy|
|Phase 4|2 weeks|Week 9|Week 10|M3 Password Reset (2026-05-12) — end-to-end reset via SND; RESET-UI parallel-start|
|Phase 5|2 weeks|Week 11|Week 12|M4 Frontend NTG (2026-05-26) — `LoginPage`+`RegisterPage`+`ProfilePage`+`THP`+RESET-UI|
|Phase 6|2 weeks|Week 13|Week 14|M4b Audit + Admin — SOC2 dry-run + TEST-010 + admin audit endpoint + dashboards green|
|Phase 7|2 weeks|Week 15|Week 16|M5 GA Release (2026-06-09) — Alpha → Beta (10%) → GA (100%) + legacy deprecated|

**Total estimated duration:** 16 weeks (4 months), aligned to the v1.0 Q2 2026 target (ends 2026-06-09, within Q2) with the SOC2 Q3 2026 deadline comfortably preceded.

## Open Questions

|#|Question|Impact|Blocking Phase|Resolution Owner|
|---|---|---|---|---|
|OQ-001|Should `THS` support API key authentication for service-to-service calls?|Scope expansion; may add API-009 for key issuance|v1.1 (not blocking v1.0)|test-lead (deferred to v1.1 discussion)|
|OQ-002|Maximum allowed `SRP.roles` array length?|Column constraint + validation; small impact|Phase 1 (before DM-001 constraint finalized)|auth-team (target 2026-04-01)|
|OQ-003|Password reset emails: synchronous or asynchronous delivery?|Changes `THS.resetRequest` contract + SLA|Phase 4 (before FRT implementation)|Engineering|
|OQ-004|Maximum refresh tokens allowed per user across devices?|Redis keyspace design + device-limit policy|Phase 3 (before C0 freeze)|Product|
|OQ-005|Account lockout policy confirmation (TDD: 5/15min — Security signoff?)|Phase 2 lockout implementation depends on this|Phase 1 gate (PRE-OQ-005)|Security|
|OQ-006|Should we support "remember me" to extend session duration?|Extra refresh-ttl tier; potential compliance impact|v1.1 or late v1.0 if prioritized|Product|
|OQ-007|Jordan (admin) JTBD RBAC model — single admin role vs graded permissions?|API-008 + ADMIN-UNLOCK authorization surface|Phase 6 (before API-008 goes live)|Product + Security|
|OQ-008|Audit log RTN — PRD 12mo vs TDD 90d authoritative?|Compliance evidence + storage sizing; RESOLVED via OQ-RECON-RET (PRD wins)|Phase 1 (ratified in decision log)|Compliance (resolved)|
|OQ-009|Multi-device session policy — unlimited, bounded, or user-managed?|Refresh keying + logout scope; RESOLVED via OQ-RECON-MULTIDEV|Phase 3 (ratified in decision log)|Product + Security (resolved)|
|OQ-010|Admin unlock in v1.0 scope or deferred to v1.1?|ADMIN-UNLOCK effort lock; gated by PRE-OQ-010|Phase 6 (gate before ADMIN-UNLOCK build)|Product + Security|
|OQ-011|Logout as explicit v1.0 scope despite TDD omission?|API-005 + LOGOUT-UI authorization; RESOLVED via OQ-RECON-LOGOUT (in scope)|Phase 1 (ratified in decision log)|Product + Engineering (resolved)|

