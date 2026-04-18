---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: "none"
debate_rounds: "none"
generated: "2026-04-16"
generator: "single"
total_phases: 8
total_task_rows: 112
risk_count: 7
open_questions: 7
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service establishes the platform's identity layer, unblocking $2.4M of personalization-dependent revenue and satisfying the Q3 2026 SOC2 Type II audit. The v1.0 scope — registration, login, token refresh, profile retrieval, password reset — is explicitly bounded (no OAuth, MFA, or RBAC) so that the architect's critical path is short and auditable.

**Business Impact:** Unblocks Q2-Q3 2026 personalization roadmap; enables SOC2 audit trail (12-month retention); reduces 30% QoQ access-related support volume via self-service password reset; captures GDPR consent at registration.

**Complexity:** HIGH (0.72) — cross-cutting security (bcrypt-12, RS256, refresh rotation, lockout), dual datastores (PostgreSQL + Redis), external SendGrid integration, phased rollout with feature flags, SOC2/GDPR/NIST SP 800-63B compliance burden, and backend/frontend coordination across `AuthProvider` silent refresh.

**Critical path:** Infra provisioning → `UserProfile` + `PasswordHasher` + `JwtService` → `AuthService` (login/register) → `TokenManager` + refresh → Password reset + email → Frontend (`AuthProvider` + pages) → Audit/observability → Phased GA (Alpha 10% → Beta → 100%).

**Key architectural decisions:**

- Stateless JWT access tokens (15 min, RS256/2048) + opaque refresh tokens in Redis (7-day TTL, hashed-at-rest) — no server session store beyond Redis refresh records.
- `TokenManager` fails closed on Redis outage to prevent auth-bypass; users forced to re-login rather than silently extending expired sessions.
- bcrypt cost 12 isolated behind `PasswordHasher` abstraction to enable future algorithm migration (e.g., argon2id) without touching `AuthService`.
- Rate limiting enforced at API Gateway (not in-service) to protect `AuthService` from resource exhaustion before application-layer lockout kicks in.
- Audit log retention set to 12 months (PRD/SOC2 authoritative) overriding TDD's 90-day figure; persisted in PostgreSQL alongside `UserProfile`.

**Open risks requiring resolution before Phase 1:**

- OQ-005 (lockout policy confirmation — TDD 5/15min vs Security-team sign-off) must be resolved before `AuthService` lockout logic is coded; otherwise rework of lockout storage is likely.
- SendGrid account provisioning and sender domain DKIM/SPF setup must complete before Phase 4 or password-reset flow is blocked (R-006).
- Quarterly RSA key rotation procedure must be documented and signed off by platform-team before `JwtService` enters Phase 2; retrofitting rotation into a running deployment is high risk.

## Phase 0: Foundation & Infrastructure (Weeks 1-2)

**Phase 0** | M0 Infrastructure Baseline | 2 weeks | Entry: TDD + PRD signed off; SEC-POLICY-001 available; cloud accounts provisioned | Exit: PostgreSQL+Redis reachable from service mesh; CI green on empty repo; RSA keys + secrets in vault

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | INFRA-PG | Provision PostgreSQL 15 with HA replica | Infra | — | 2-node primary+replica; pool-capacity:100; failover<30s; backup-daily | M | P0 |
| 2 | INFRA-REDIS | Provision Redis 7 cluster with persistence | Infra | — | 3-node; 1GB-initial; AOF-on; TTL-support; failover-tested | M | P0 |
| 3 | INFRA-K8S | Configure K8s namespace+HPA for auth-service | Infra | — | min:3; max:10; cpu-trigger:70%; liveness+readiness-probes | M | P0 |
| 4 | INFRA-NODE | Pin Node.js 20 LTS in Dockerfile+CI | Infra | — | node-version:20.x; multi-stage-build; non-root-user; image-scanned | S | P0 |
| 5 | INFRA-TLS | Terminate TLS 1.3 at API Gateway | Sec | — | tls:1.3-only; hsts-on; cert-auto-renew; weak-ciphers-blocked | M | P0 |
| 6 | INFRA-CORS | Configure CORS allowlist at gateway | Sec | INFRA-TLS | known-origins-only; credentials:true; wildcard-blocked | S | P0 |
| 7 | INFRA-GW | Configure API Gateway rate-limit rules | Sec | INFRA-TLS | login:10/min/ip; register:5/min/ip; me:60/min/user; refresh:30/min/user | M | P0 |
| 8 | INFRA-RSA | Generate+rotate RS256 keypair in KMS | Sec | — | rsa-2048; kms-stored; quarterly-rotation-scheduled; public-key-jwks | M | P0 |
| 9 | INFRA-SG | Provision SendGrid account + DKIM/SPF | Infra | — | api-key-vaulted; dkim-verified; spf-verified; sender-domain-authenticated | M | P0 |
| 10 | INFRA-CI | Bootstrap CI pipeline with testcontainers | Ops | INFRA-PG,INFRA-REDIS | lint+unit+integration-jobs; testcontainers-pg+redis; coverage-report | M | P0 |
| 11 | INFRA-VAULT | Mount secrets (DB, Redis, RSA, SG) in K8s | Sec | INFRA-K8S,INFRA-RSA,INFRA-SG | sealed-secrets; no-env-plaintext; rotation-documented | M | P0 |
| 12 | INFRA-OBS | Deploy Prometheus+Grafana+OTel collector | Ops | INFRA-K8S | prom-scrape-live; grafana-datasource-ok; otel-otlp-endpoint | M | P0 |
| 13 | SEC-POLICY | Ratify SEC-POLICY-001 hashing+signing rules | Sec | — | bcrypt-cost:12-mandated; rs256-2048-mandated; cleartext-ban-in-logs | S | P0 |

### Integration Points — Phase 0

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| RSA keypair (kid) | Key rotation registry | INFRA-RSA | Phase 0 | `JwtService` (Phase 2) |
| Rate-limit policies | Gateway config map | INFRA-GW | Phase 0 | `AuthService` endpoints (Phase 2-3) |
| Secret mounts | K8s sealed-secrets binding | INFRA-VAULT | Phase 0 | `AuthService`, `TokenManager`, `EmailService` (all downstream) |
| OTel collector endpoint | Env var injection | INFRA-OBS | Phase 0 | All backend components |

## Phase 1: Data Models & Core Security Primitives (Weeks 3-4)

**Phase 1** | M1a Data Layer + Primitives | 2 weeks | Entry: Phase 0 exit met; PG+Redis reachable; RSA keys in KMS | Exit: `UserProfile`/`AuditLog`/`ResetToken` schemas live; `PasswordHasher` + `JwtService` + `UserRepo` unit-tested

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DM-001 | Create UserProfile table + constraints | DB | INFRA-PG | id:UUID-PK; email:unique-idx-lowercase-NOT-NULL; displayName:varchar-2-100-NOT-NULL; createdAt:timestamptz-default-now-NOT-NULL; updatedAt:timestamptz-auto-NOT-NULL; lastLoginAt:timestamptz-nullable; roles:text[]-default-[user]-NOT-NULL | M | P0 |
| 2 | DM-001.idx | Add indexes on email + lastLoginAt | DB | DM-001 | email-unique-btree; last-login-btree; explain-plan-verified | S | P0 |
| 3 | DM-003 | Create AuditLog table (PRD SOC2) | DB | INFRA-PG | id:UUID-PK; user_id:FK-nullable; event_type:enum; ip:inet; outcome:enum; created_at:timestamptz-index; retention:12mo | M | P0 |
| 4 | DM-004 | Create ResetToken table | DB | INFRA-PG | id:UUID-PK; user_id:FK-NOT-NULL; token_hash:varchar-unique; expires_at:timestamptz; used_at:timestamptz-nullable; created_at:timestamptz | M | P0 |
| 5 | MIG-DB-BASE | Author initial Knex/Prisma migration set | DB | DM-001,DM-003,DM-004 | idempotent; up+down-reversible; checksum-locked; applied-via-CI | M | P0 |
| 6 | COMP-008 | Implement PasswordHasher (bcrypt cost 12) | Sec | SEC-POLICY,INFRA-NODE | deps:bcryptjs; methods:hash+verify; cost:12-enforced; pluggable-interface; hash<500ms | M | P0 |
| 7 | NFR-SEC-001 | Assert bcrypt cost factor 12 in unit test | Test | COMP-008 | inspect-hash-prefix:$2b$12$; wrong-cost→test-fails; round-trip-verify-ok | S | P0 |
| 8 | COMP-007 | Implement JwtService (RS256 sign/verify) | Sec | INFRA-RSA,SEC-POLICY | deps:jsonwebtoken+kms; algo:RS256; keysize:2048; clock-skew:5s; kid-in-header | M | P0 |
| 9 | NFR-SEC-002 | Assert RS256+2048 in config test | Test | COMP-007 | algo-assert:RS256; keysize-assert:2048; hs256-rejected; unsigned-rejected | S | P0 |
| 10 | COMP-009 | Implement UserRepo (PG access layer) | DB | DM-001 | methods:findByEmail+findById+insert+updateLastLogin+incrementFailedAttempts+lockAccount; pool-bounded; query-timeout:1s | L | P0 |
| 11 | COMP-011 | Implement AuditLogger component | Ops | DM-003 | methods:record(userId,event,ip,outcome); async-batched; passwords-tokens-scrubbed; fire-and-forget | M | P0 |
| 12 | COMP-012 | Implement RateLimiter middleware hook | Sec | INFRA-GW | gateway-primary; in-service-fallback; 429-envelope; retry-after-header | M | P1 |
| 13 | COMP-010 | Implement EmailService (SendGrid adapter) | API | INFRA-SG | methods:sendResetEmail; template-id-config; retry-on-5xx; delivery-id-logged | M | P1 |
| 14 | COMP-005-skel | Scaffold AuthService class with DI | API | COMP-008,COMP-007,COMP-009,COMP-011 | deps:PasswordHasher+TokenManager+JwtService+UserRepo+AuditLogger; methods:login+register+getProfile+resetRequest+resetConfirm; email-lowercase-normalized | M | P0 |
| 15 | PRE-OQ-005 | Resolve lockout policy (OQ-005) | Gate | — | security-team-signoff-recorded; 5-attempts/15min-confirmed-or-revised; documented-in-TDD | S | P0 |

### Integration Points — Phase 1

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| `PasswordHasher` interface | DI binding in container | COMP-008 | Phase 1 | `AuthService.login`, `AuthService.register`, `AuthService.resetConfirm` |
| `JwtService` key loader | KMS → process secret provider | COMP-007 | Phase 1 | `TokenManager` (Phase 3), `/auth/me` verifier middleware |
| `UserRepo` | DI binding in container | COMP-009 | Phase 1 | `AuthService` (all methods) |
| `AuditLogger` | Async event emitter subscribed per auth event | COMP-011 | Phase 1 | `AuthService`, `TokenManager`, reset flow |
| `EmailService` | DI binding behind feature flag | COMP-010 | Phase 1 | `AuthService.resetRequest` (Phase 4) |
| `RateLimiter` | Middleware chain registration | COMP-012 | Phase 1 | `/auth/*` endpoints (Phase 2-3) |

## Phase 2: Login & Registration Endpoints (Weeks 5-6)

**Phase 2** | M1 Core AuthService (2026-04-14) | 2 weeks | Entry: Phase 1 primitives unit-tested; OQ-005 resolved | Exit: FR-AUTH-001 + FR-AUTH-002 pass unit+integration tests; lockout enforced; rate-limit wired

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | FR-AUTH-001 | Implement AuthService.login flow | API | COMP-005-skel,COMP-008,COMP-009 | valid-creds→200+AuthToken; invalid→401; non-existent-email→401-no-enum; 5fail/15min→423-locked; lastLoginAt-updated | L | P0 |
| 2 | FR-AUTH-002 | Implement AuthService.register flow | API | COMP-005-skel,COMP-008,COMP-009 | valid→201+UserProfile; duplicate-email→409; weak-pw→400; bcrypt-cost:12-persisted | L | P0 |
| 3 | API-001 | Expose POST /v1/auth/login endpoint | API | FR-AUTH-001,COMP-012 | path:/v1/auth/login; body:{email,password}; 200:AuthToken; 401:invalid; 423:locked; 429:rate; rate-limit:10/min/ip | M | P0 |
| 4 | API-002 | Expose POST /v1/auth/register endpoint | API | FR-AUTH-002,COMP-012 | path:/v1/auth/register; body:{email,password,displayName}; 201:UserProfile; 400:validation; 409:conflict; rate-limit:5/min/ip | M | P0 |
| 5 | COMP-005 | Finalize AuthService (login+register paths) | API | FR-AUTH-001,FR-AUTH-002 | deps-wired:PasswordHasher+UserRepo+AuditLogger; email-lowercased; lockout-counter-in-UserRepo; exceptions-mapped-to-status | L | P0 |
| 6 | LOCKOUT | Implement 5-fail/15-min lockout window | Sec | FR-AUTH-001,COMP-009 | sliding-window:15min; threshold:5; 423-after-lock; auto-unlock-after-window; admin-unlock-hook-stub | M | P0 |
| 7 | PW-STRENGTH | Enforce NIST SP 800-63B password policy | Sec | FR-AUTH-002 | min-length:8; uppercase+digit-required; common-password-blocklist; inline-error-per-rule | M | P0 |
| 8 | EMAIL-UNIQ | Enforce case-insensitive email uniqueness | DB | FR-AUTH-002,DM-001 | lowercased-at-persist; citext-or-lowercase-index; race-safe-insert | S | P0 |
| 9 | NO-ENUM | Suppress user enumeration in error envelope | Sec | FR-AUTH-001 | wrong-email+wrong-pw→identical-401-message; timing-normalized; dummy-hash-compare-on-miss | M | P0 |
| 10 | GDPR-CONSENT | Record GDPR consent at registration | Data | FR-AUTH-002,DM-003 | consent-timestamp-stored; consent-version-tracked; audit-event-logged | M | P0 |
| 11 | TEST-001 | Unit test login valid credentials | Test | FR-AUTH-001 | PasswordHasher.verify-called; TokenManager.issue-called; AuthToken-returned | S | P0 |
| 12 | TEST-002 | Unit test login invalid credentials | Test | FR-AUTH-001 | verify→false; 401-returned; no-token-issued; lockout-counter-incremented | S | P0 |
| 13 | TEST-004 | Integration test registration persists | Test | API-002,COMP-009 | testcontainer-pg; POST→201; row-in-UserProfile; bcrypt-hash-stored; audit-row-written | M | P0 |
| 14 | AUDIT-LOGIN | Wire audit events for login+register | Ops | FR-AUTH-001,FR-AUTH-002,COMP-011 | events:login_success+login_fail+register; fields:user_id+ip+ts+outcome; no-plaintext-password | M | P0 |

### Integration Points — Phase 2

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| `AuthService.login` | Route handler binding `POST /v1/auth/login` | API-001 | Phase 2 | API Gateway → `LoginPage` (Phase 5) |
| `AuthService.register` | Route handler binding `POST /v1/auth/register` | API-002 | Phase 2 | API Gateway → `RegisterPage` (Phase 5) |
| Lockout counter | Redis + UserRepo column wiring | LOCKOUT | Phase 2 | `AuthService.login`, admin unlock (future) |
| Password policy validator | Strategy plugin registered in `AuthService` | PW-STRENGTH | Phase 2 | `AuthService.register`, `AuthService.resetConfirm` |
| Audit event bus | Async subscription `AuthService → AuditLogger` | AUDIT-LOGIN | Phase 2 | SOC2 audit log |

## Phase 3: Token Lifecycle & Profile Retrieval (Weeks 7-8)

**Phase 3** | M2 Token Management (2026-04-28) | 2 weeks | Entry: Phase 2 login+register green in staging | Exit: FR-AUTH-003 + FR-AUTH-004 pass; refresh rotation on; logout invalidates; /auth/me returns profile

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | DM-002 | Define AuthToken DTO contract | API | COMP-007 | accessToken:JWT-RS256-signed-NOT-NULL; refreshToken:opaque-unique-NOT-NULL; expiresIn:number-NOT-NULL-eq-900; tokenType:string-eq-Bearer | S | P0 |
| 2 | COMP-006 | Implement TokenManager lifecycle | API | COMP-007,INFRA-REDIS | deps:JwtService+Redis; methods:issueTokens+refresh+revoke+verifyRefresh; refresh-hashed-at-rest; ttl:7d; rotation-on-refresh; fail-closed-on-redis-down | L | P0 |
| 3 | FR-AUTH-003 | Implement JWT issue + refresh flow | API | COMP-006,FR-AUTH-001 | login→AuthToken-pair; access-ttl:15min; refresh-ttl:7d; POST-refresh→new-pair+old-revoked; expired→401; revoked→401 | L | P0 |
| 4 | FR-AUTH-004 | Implement /auth/me profile retrieval | API | COMP-005,COMP-007 | valid-token→200+UserProfile; expired→401; invalid→401; response:id+email+displayName+createdAt+updatedAt+lastLoginAt+roles | M | P0 |
| 5 | API-003 | Expose GET /v1/auth/me endpoint | API | FR-AUTH-004 | path:/v1/auth/me; header:Authorization-Bearer; 200:UserProfile; 401:missing-expired-invalid; rate-limit:60/min/user | M | P0 |
| 6 | API-004 | Expose POST /v1/auth/refresh endpoint | API | FR-AUTH-003 | path:/v1/auth/refresh; body:{refreshToken}; 200:AuthToken; 401:expired-or-revoked; rate-limit:30/min/user; old-token-revoked-atomically | M | P0 |
| 7 | API-005 | Expose POST /v1/auth/logout (PRD gap) | API | COMP-006 | path:/v1/auth/logout; body:{refreshToken}; 204:success; refresh-revoked-in-redis; audit-event:logout; rate-limit:30/min/user | M | P0 |
| 8 | REDIS-REFRESH | Persist hashed refresh tokens in Redis | DB | INFRA-REDIS,COMP-006 | key:refresh:{sha256(token)}; value:{user_id,issued_at,kid}; ttl:604800s; keyspace-notify-on-expire | M | P0 |
| 9 | CLOCK-SKEW | Apply 5s clock skew tolerance | Sec | COMP-007 | iat/exp-tolerance:5s; library-option-asserted; test-covers-bounds | S | P1 |
| 10 | REVOKE-ON-PW | Revoke all refresh tokens on password change | Sec | COMP-006,FR-AUTH-003 | PRD:new-pw-invalidates-all-sessions; delete-all-user-refresh-keys; audit-event:bulk_revoke | M | P0 |
| 11 | KID-ROTATION | Support key-id header for RSA rotation | Sec | COMP-007,INFRA-RSA | kid-in-jwt-header; jwks-endpoint-exposes-all-active-kids; old-kid-accepted-until-expiry | M | P1 |
| 12 | TEST-003 | Unit test TokenManager refresh | Test | COMP-006 | valid-refresh→new-pair; old-revoked-in-redis; JwtService.sign-called-with-new-iat | S | P0 |
| 13 | TEST-005 | Integration test expired refresh rejected | Test | COMP-006,INFRA-REDIS | testcontainer-redis; ttl-elapsed→401; revoked-key-removed-from-redis | M | P0 |
| 14 | AUDIT-TOKEN | Wire audit events for refresh+logout | Ops | COMP-006,COMP-011 | events:token_refresh+logout+bulk_revoke; outcome+user_id+ip; no-token-in-log | S | P0 |

### Integration Points — Phase 3

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| `TokenManager` | DI binding; injected into `AuthService` | COMP-006 | Phase 3 | `AuthService.login`, `/auth/refresh`, `/auth/logout`, `AuthProvider` silent refresh |
| JWT verifier middleware | Express/Nest middleware registered for protected routes | API-003 | Phase 3 | `GET /auth/me` and future protected endpoints |
| Redis refresh keyspace | Keyspace-notifications subscription | REDIS-REFRESH | Phase 3 | `TokenManager` revocation, observability metrics |
| JWKS endpoint | Public discovery route `/v1/auth/.well-known/jwks.json` | KID-ROTATION | Phase 3 | External verifiers, Sam (API consumer persona) |

## Phase 4: Password Reset & Email Integration (Weeks 9-10)

**Phase 4** | M3 Password Reset (2026-05-12) | 2 weeks | Entry: Phase 3 tokens stable; SendGrid DKIM/SPF verified | Exit: FR-AUTH-005 end-to-end; reset tokens one-time + 1h TTL; password change revokes all sessions

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | FR-AUTH-005 | Implement two-step password reset | API | COMP-005,COMP-010,DM-004 | reset-request→email-sent+token-persisted; reset-confirm→password-updated+hash-rotated; ttl:1h; one-time-use | L | P0 |
| 2 | API-006 | Expose POST /v1/auth/reset-request | API | FR-AUTH-005,COMP-010 | path:/v1/auth/reset-request; body:{email}; 200-generic-regardless-of-account; rate-limit:3/min/ip; email-sent<60s | M | P0 |
| 3 | API-007 | Expose POST /v1/auth/reset-confirm | API | FR-AUTH-005 | path:/v1/auth/reset-confirm; body:{token,newPassword}; 200:success; 400:invalid-or-expired; 400:weak-password; used-token→400 | M | P0 |
| 4 | RESET-TOKEN-GEN | Generate cryptographically-secure reset tokens | Sec | DM-004 | csprng:32-bytes-base64url; sha256-at-rest; unguessable; entropy>=256bit | S | P0 |
| 5 | RESET-TTL | Enforce 1-hour reset token expiry | Sec | DM-004,FR-AUTH-005 | expires_at:now+1h; expired→400; cleanup-job-purges-expired-daily | M | P0 |
| 6 | RESET-ONETIME | Mark used reset tokens non-reusable | Sec | DM-004 | used_at-set-atomically; replay→400; concurrent-use-serializable | M | P0 |
| 7 | RESET-REVOKE | Invalidate all sessions on password change | Sec | REVOKE-ON-PW,FR-AUTH-005 | PRD:new-pw-invalidates-all-existing-sessions; bulk-refresh-revoke; audit-event-emitted | M | P0 |
| 8 | EMAIL-TEMPLATE | Build reset email template + content | Docs | COMP-010 | link-contains-token-only; brand-header; expiry-stated; support-contact; dkim-signed | M | P1 |
| 9 | EMAIL-DELIVERY | Monitor SendGrid delivery + bounces | Ops | COMP-010 | delivery-webhook-ingested; bounce-alert-on-spike; fallback-channel-documented-for-R-006 | M | P1 |
| 10 | NO-ENUM-RESET | Generic response on reset-request | Sec | API-006 | registered+unregistered→same-200; no-timing-side-channel; audit-records-both-cases | S | P0 |
| 11 | AUDIT-RESET | Wire audit events for reset flow | Ops | FR-AUTH-005,COMP-011 | events:reset_request+reset_confirm+reset_token_used; outcome+user_id+ip+ts | S | P0 |

### Integration Points — Phase 4

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| `EmailService.sendResetEmail` | Invoked from `AuthService.resetRequest` | FR-AUTH-005 | Phase 4 | Reset request API, OPS-006 delivery monitoring |
| Reset-token cleanup job | Scheduled worker (cron) | RESET-TTL | Phase 4 | PostgreSQL `ResetToken` table |
| Bulk-revoke hook | Event listener on password-changed event | RESET-REVOKE | Phase 4 | `TokenManager` refresh store |
| Webhook ingest | SendGrid events → internal queue | EMAIL-DELIVERY | Phase 4 | Observability dashboards, on-call alerting |

## Phase 5: Frontend Integration (Weeks 11-12)

**Phase 5** | M4 Frontend Integration (2026-05-26) | 2 weeks | Entry: Phase 4 backend APIs stable in staging | Exit: `LoginPage` + `RegisterPage` + `ProfilePage` ship behind `AUTH_NEW_LOGIN`; silent refresh works across tabs

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | COMP-004 | Implement AuthProvider context + silent refresh | FE | API-003,API-004 | props:children:ReactNode; state:AuthToken+UserProfile; methods:login+logout+refresh+getMe; intercepts-401→refresh-or-redirect; exposes-useAuth-hook | L | P0 |
| 2 | COMP-001 | Build LoginPage (/login) | FE | API-001,COMP-004 | props:onSuccess+redirectUrl; form:email+password; inline-validation; submit→POST-login; stores-AuthToken-via-AuthProvider; loading+error-states | L | P0 |
| 3 | COMP-002 | Build RegisterPage (/register) | FE | API-002,COMP-004 | props:onSuccess+termsUrl; form:email+password+displayName; client-strength-validation; POST-register; duplicate-email-error | L | P0 |
| 4 | COMP-003 | Build ProfilePage (/profile) | FE | API-003,COMP-004 | auth-required; fetches-GET-me; displays:displayName+email+createdAt; loading+error-states | M | P0 |
| 5 | PUB-ROUTES | Configure PublicRoutes wrapping login+register | FE | COMP-001,COMP-002 | redirects-authenticated-users-to-/profile; loads-without-token; bundle-code-split | M | P1 |
| 6 | PROT-ROUTES | Configure ProtectedRoutes wrapping profile | FE | COMP-003,COMP-004 | unauthenticated→redirect-/login-with-returnTo; checks-via-AuthProvider | M | P0 |
| 7 | REFRESH-COOKIE | Store refresh token in HttpOnly SameSite cookie | Sec | COMP-004,API-001 | HttpOnly:true; Secure:true; SameSite:Strict; path:/v1/auth; cleared-on-logout; R-001-mitigation | M | P0 |
| 8 | ACCESS-MEMORY | Keep access token in memory only | Sec | COMP-004 | not-in-localStorage; not-in-cookie; cleared-on-tab-close; R-001-mitigation | M | P0 |
| 9 | FE-401-INTERCEPT | Intercept 401 and trigger silent refresh | FE | COMP-004,API-004 | axios/fetch-interceptor; single-inflight-refresh; queue-requests-during-refresh; redirect-on-refresh-fail | L | P0 |
| 10 | RESET-UI | Build forgot-password + set-new-password screens | FE | API-006,API-007 | /forgot-password:email-form→confirmation-screen; /reset-confirm:token-from-query+newPassword; generic-success-message | M | P0 |
| 11 | LOGOUT-UI | Wire logout button to /auth/logout | FE | API-005,COMP-004 | calls-logout-API; clears-AuthProvider-state; redirects-/login; refresh-cookie-cleared | S | P0 |
| 12 | TEST-006 | E2E test full user journey (Playwright) | Test | COMP-001,COMP-002,COMP-003,COMP-004 | register→login→profile→refresh→logout; runs-against-staging; <30s-runtime | L | P0 |
| 13 | FE-A11Y | Accessibility pass on auth pages | FE | COMP-001,COMP-002,COMP-003 | wcag-aa; keyboard-nav; screen-reader-labels; error-announcements | M | P1 |

### Integration Points — Phase 5

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| `useAuth` hook | React Context consumer exported from `AuthProvider` | COMP-004 | Phase 5 | All protected pages, logout button, navbar |
| HTTP 401 interceptor | Axios/fetch middleware registered by `AuthProvider` | FE-401-INTERCEPT | Phase 5 | Every authenticated API call |
| Route guards | `PublicRoutes` / `ProtectedRoutes` wrapper components | PUB-ROUTES,PROT-ROUTES | Phase 5 | Router tree `App → AuthProvider → Routes` |
| Refresh cookie | Browser cookie jar on `/v1/auth` path | REFRESH-COOKIE | Phase 5 | `/auth/refresh`, `/auth/logout` |

## Phase 6: Compliance, Observability & Admin Tooling (Weeks 13-14)

**Phase 6** | M4b Audit + Admin | 2 weeks | Entry: Phase 5 frontend in staging; all auth events emitted | Exit: SOC2 audit queryable; Jordan persona JTBD closed; dashboards + alerts green in staging

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-COMPLIANCE-001 | Ship SOC2/GDPR/NIST audit-log schema | Ops | DM-003,COMP-011 | fields:user_id+event+ip+ts+outcome; retention:12mo; immutable-partitioned-monthly; scrubs-secrets | L | P0 |
| 2 | API-008 | Admin audit-log query endpoint (PRD JTBD) | API | DM-003,NFR-COMPLIANCE-001 | path:/v1/admin/audit-logs; auth:admin-role; query:date-range+user_id; paginated; rate-limited; audit-of-audit-access | L | P0 |
| 3 | ADMIN-UNLOCK | Admin account unlock endpoint | API | LOCKOUT | path:/v1/admin/users/{id}/unlock; auth:admin-role; clears-lock-counter; emits-audit-event; rate-limited | M | P1 |
| 4 | DATA-MIN | Enforce GDPR data-minimization audit | Sec | DM-001 | only-email+hash+displayName+roles-persisted; pii-scanner-in-ci; schema-change-requires-compliance-review | M | P0 |
| 5 | NIST-PW | Validate NIST SP 800-63B compliance in tests | Sec | PW-STRENGTH,COMP-008 | breach-corpus-check; min-8-enforced; no-hints; one-way-hash-verified | M | P0 |
| 6 | OPS-005 | Structured logging + no-secrets scrubber | Ops | COMP-011 | json-logs; password-token-scrubbed-via-regex; pii-redacted; correlation-id-propagated | M | P0 |
| 7 | OPS-005.metrics | Emit Prometheus counters + histograms | Ops | INFRA-OBS | auth_login_total; auth_login_duration_seconds; auth_token_refresh_total; auth_registration_total | M | P0 |
| 8 | OPS-005.trace | Instrument OTel spans across AuthService | Ops | INFRA-OBS | spans:AuthService→PasswordHasher+TokenManager+JwtService; sampled:10%; trace-id-in-logs | M | P0 |
| 9 | OPS-005.dash | Build Grafana dashboards | Ops | OPS-005.metrics | panels:login-rate+latency+refresh-rate+reg-rate; per-endpoint-p95; error-rate | M | P0 |
| 10 | OPS-005.alert | Configure Prometheus alert rules | Ops | OPS-005.dash | login-fail>20%/5m; p95>500ms; redis-fail>10/min; pager-ok | M | P0 |
| 11 | NFR-REL-001 | Wire uptime SLO + synthetic checks | Ops | OPS-005.alert | 99.9%/30d-rolling-window; synthetic-login-every-60s; slo-error-budget-tracked | M | P0 |
| 12 | NFR-PERF-001 | APM tracing asserts p95<200ms | Ops | OPS-005.trace | per-endpoint-p95-recorded; sli-dashboard-published; breach-alerts-configured | M | P0 |
| 13 | OPS-004 | Document capacity plan + HPA triggers | Docs | INFRA-K8S,INFRA-REDIS | 3→10-replicas; pg-pool:100→200-if-wait>50ms; redis:1→2GB-if>70%util; runbook-linked | M | P1 |
| 14 | SOC2-VALIDATION | Compliance dry-run against SOC2 controls | Gate | NFR-COMPLIANCE-001,API-008 | controls-cc6.1+cc6.6+cc7.2-evidence-collected; 12mo-retention-verified; signoff:compliance-team | M | P0 |

### Integration Points — Phase 6

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| Admin audit API | Route registered `/v1/admin/audit-logs` with RBAC middleware | API-008 | Phase 6 | Jordan persona (admin UI, future work) |
| Prometheus metric registry | `prom-client` registry export on `/metrics` | OPS-005.metrics | Phase 6 | Grafana, alertmanager |
| OTel span processor | OTel SDK tracer provider registered at service bootstrap | OPS-005.trace | Phase 6 | Observability backend (Tempo/Jaeger) |
| Alertmanager routes | Prom alert rules → on-call PagerDuty | OPS-005.alert | Phase 6 | Auth-team on-call rotation |

## Phase 7: Hardening, Migration & GA Rollout (Weeks 15-16)

**Phase 7** | M5 GA Release (2026-06-09) | 2 weeks | Entry: Phase 6 observability green in staging; compliance signed off | Exit: 99.9% uptime first 7 days; feature flags cleaned; legacy auth deprecated; post-mortem playbook validated

| # | ID | Task | Comp | Deps | AC | Eff | Pri |
|---|---|---|---|---|---|---|---|
| 1 | NFR-PERF-002 | Run k6 load test 500 concurrent | Test | NFR-PERF-001 | k6-ramp:0→500-users; p95<200ms; error-rate<0.1%; sustained-5min | L | P0 |
| 2 | PENTEST | Security review + penetration test | Sec | COMP-005,COMP-006,COMP-007 | owasp-top10-coverage; jwt-none-alg-rejected; replay-attacks-blocked; report-filed; criticals-zero | L | P0 |
| 3 | CAPTCHA | CAPTCHA after 3 failed login attempts | Sec | FR-AUTH-001 | trigger:3-fails-per-session; captcha-challenge-required; bypass-rate<1%; R-002-mitigation | M | P1 |
| 4 | WAF-RULES | Deploy WAF IP-block rules | Sec | INFRA-GW | known-bad-ips-blocked; bot-sig-rules-on; log-only-first-48h; R-002-mitigation | M | P1 |
| 5 | FLAG-NEW-LOGIN | Provision AUTH_NEW_LOGIN feature flag | Ops | COMP-001,COMP-002,COMP-005 | default:OFF; percentage-rollout-controls; audit-on-toggle; cleanup:after-phase-3-GA | S | P0 |
| 6 | FLAG-REFRESH | Provision AUTH_TOKEN_REFRESH feature flag | Ops | COMP-006 | default:OFF; when-off:access-only; cleanup:GA+2weeks; audit-on-toggle | S | P0 |
| 7 | MIG-001 | Phase 1 Internal Alpha on staging | Infra | FLAG-NEW-LOGIN | 1-week; zero-P0/P1-bugs; manual-qa-auth-team; exit→feature-flag-togglable; rollback:disable-flag | M | P0 |
| 8 | MIG-002 | Phase 2 Beta at 10% traffic | Infra | MIG-001 | 2-weeks; p95<200ms; error-rate<0.1%; zero-redis-failures; monitor-AuthProvider-under-load; rollback:flag-to-0% | L | P0 |
| 9 | MIG-003 | Phase 3 GA at 100% + legacy deprecation | Infra | MIG-002 | 1-week; uptime:99.9%/7d-first-week; dashboards-green; AUTH_NEW_LOGIN-removed; legacy-endpoints-deprecated | L | P0 |
| 10 | OPS-001 | Publish runbook — AuthService down | Docs | OPS-005.alert | symptoms+diagnosis+resolution-documented; owner:auth-team; escalation:platform-team-after-15min; drill-completed | M | P0 |
| 11 | OPS-002 | Publish runbook — token refresh failures | Docs | OPS-005.alert | symptoms:logouts+401-loops; diagnosis:redis+jwks+flag; resolution:scale+remount+toggle; drill-completed | M | P0 |
| 12 | OPS-003 | Activate 24/7 on-call rotation (first 2 weeks) | Ops | OPS-001,OPS-002 | p1-ack<15min; auth-team-rotation-scheduled; mttr-target:<60min; tooling:k8s+grafana+redis+pg | M | P0 |
| 13 | ROLLBACK-PROC | Document + drill rollback procedure | Docs | MIG-003 | 6-step-sequence; smoke-test-legacy; log-investigation; pg-restore-if-needed; incident-channel-notify; post-mortem<48h | M | P0 |
| 14 | ROLLBACK-TRIG | Encode rollback triggers as alerts | Ops | OPS-005.alert,ROLLBACK-PROC | p95>1000ms/5min; err-rate>5%/2min; redis-fail>10/min; data-loss→auto-page | M | P0 |
| 15 | BACKUP-PRE | Pre-phase PostgreSQL backup + restore drill | Ops | INFRA-PG | snapshot-before-each-phase; pitr-window:7d; restore-drill-passes; R-003-mitigation | M | P0 |
| 16 | LEGACY-DEPRECATE | Publish deprecation notice for legacy auth | Docs | MIG-003 | 90-day-sunset-announced; api-consumers-notified; stats-tracked-per-week | M | P1 |
| 17 | POST-GA-VERIFY | 7-day post-GA SLO verification | Gate | MIG-003 | uptime:99.9%; p95<200ms-sustained; reg-conv>60%; fail-login<5%; retrospective-held | M | P0 |
| 18 | FLAG-CLEANUP | Remove AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH | Ops | POST-GA-VERIFY | dead-code-removed; flag-config-pruned; audit-logged; rollback-path-deprecated | M | P1 |

### Integration Points — Phase 7

| Artifact | Type | Wired | Phase | Consumed By |
|---|---|---|---|---|
| `AUTH_NEW_LOGIN` flag | LaunchDarkly/Unleash/internal flag dispatch | FLAG-NEW-LOGIN | Phase 7 | `AuthService` login path, `LoginPage` route |
| `AUTH_TOKEN_REFRESH` flag | Flag dispatch table | FLAG-REFRESH | Phase 7 | `TokenManager.refresh`, `AuthProvider` silent-refresh |
| Rollback trigger hooks | Alertmanager → runbook automation webhook | ROLLBACK-TRIG | Phase 7 | Auth-team on-call, automated flag-flip |
| Legacy deprecation banner | API Gateway response-header injector | LEGACY-DEPRECATE | Phase 7 | Sam persona (API consumer integrations) |

## Risk Assessment and Mitigation

| # | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R-001 | Token theft via XSS allows session hijacking | HIGH | Medium | High | Access token in memory only (ACCESS-MEMORY); HttpOnly+SameSite cookie for refresh (REFRESH-COOKIE); 15-min access TTL; `TokenManager` revoke-on-suspect; force password reset for affected accounts | security |
| R-002 | Brute-force attacks on /auth/login | MEDIUM | High | Medium | Gateway rate-limit 10/min/ip (INFRA-GW); account lockout 5/15min (LOCKOUT); bcrypt cost 12; CAPTCHA after 3 fails (CAPTCHA); WAF IP block (WAF-RULES) | security |
| R-003 | Data loss during legacy auth migration | HIGH | Low | High | Parallel operation Phase 1-2 (MIG-001/MIG-002); idempotent upserts; pre-phase PG snapshot (BACKUP-PRE); restore drill rehearsed | platform |
| R-004 | Redis unavailability disables refresh flow | MEDIUM | Medium | Medium | `TokenManager` fails closed → forced re-login (COMP-006); redis cluster + monitoring (INFRA-REDIS, OPS-005.alert); HPA scale-out runbook (OPS-002) | platform |
| R-005 | Clock skew breaks JWT validation | LOW | Low | Low | `JwtService` 5s tolerance (CLOCK-SKEW); ntp on all nodes; bound-test in CI | auth-team |
| R-006 | Email delivery failure blocks password reset | MEDIUM | Medium | High | SendGrid delivery webhook + bounce alerting (EMAIL-DELIVERY); fallback support channel documented; multi-region SendGrid pool | auth-team |
| R-007 | Compliance failure from incomplete audit logging | HIGH | Medium | High | Audit schema defined Phase 1 (DM-003); event coverage Phase 2-4 (AUDIT-LOGIN/TOKEN/RESET); SOC2 dry-run gate (SOC2-VALIDATION); 12-month retention enforced | compliance |
| R-008 | RSA key compromise (architect-added) | HIGH | Low | Critical | Quarterly rotation (INFRA-RSA, KID-ROTATION); KMS-stored private key; JWKS publishes `kid`; revocation playbook | security |
| R-009 | Refresh-token-rotation race causes user lockout (architect-added) | MEDIUM | Medium | Medium | Atomic Redis swap (REDIS-REFRESH); single-inflight-refresh on FE (FE-401-INTERCEPT); grace window for in-flight requests | auth-team |

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Required By Phase | Status | Fallback |
|---|---|---|---|
| PostgreSQL 15+ (HA + replica) | Phase 0 | Provisioning (INFRA-PG) | Read-replica failover (OPS-001); restore from PITR snapshot (BACKUP-PRE) |
| Redis 7+ cluster | Phase 0 | Provisioning (INFRA-REDIS) | `TokenManager` fails closed; users re-login until cluster restored |
| Node.js 20 LTS runtime | Phase 0 | Pinned in Dockerfile | Pin previous LTS image; revert deployment via K8s rollback |
| bcryptjs library | Phase 1 | Available in npm | Vendored snapshot in lockfile; replaceable behind `PasswordHasher` |
| jsonwebtoken library | Phase 1 | Available in npm | Vendored snapshot; replaceable behind `JwtService` |
| SendGrid API + verified sender domain | Phase 4 | Provisioning (INFRA-SG) | SES or Postmark adapter behind `EmailService`; manual support escalation |
| API Gateway (rate-limit + CORS + TLS) | Phase 0 | In place | Service-side fallback rate limiter (COMP-012); manual block rules |
| SEC-POLICY-001 (security policy doc) | Phase 1 | Ratification pending (SEC-POLICY) | Block Phase 1 start until ratified — non-bypassable |
| KMS for RSA key custody | Phase 0 | Provisioning (INFRA-RSA) | Encrypted-at-rest secrets file with stricter access controls; manual rotation |
| Compliance team review capacity | Phase 6 | Scheduled SOC2 dry-run | Slip GA by ≤1 week if signoff delayed |

### Infrastructure Requirements

- Kubernetes cluster with HPA enabled (3→10 auth-service replicas, CPU>70% trigger).
- PostgreSQL 15+ primary + replica with daily backup, 7-day PITR window.
- Redis 7+ cluster with AOF persistence, ≥1 GB initial capacity, scale to 2 GB at >70% utilization.
- API Gateway terminating TLS 1.3, enforcing CORS allowlist, and applying per-endpoint rate limits.
- KMS-backed RSA-2048 keypair with quarterly rotation.
- Prometheus + Grafana + OpenTelemetry collector for metrics, dashboards, traces.
- SendGrid account with DKIM/SPF on the sender domain.
- Sealed-secrets controller in K8s for DB, Redis, RSA, SendGrid credentials.
- CI pipeline with testcontainers for ephemeral PostgreSQL + Redis on every PR.
- Staging cluster mirrored from production for MIG-001 internal alpha gating.

### Team & Skills

- Backend engineers (2): Node.js 20, PostgreSQL, Redis, JWT, bcrypt; own `AuthService`, `TokenManager`, `PasswordHasher`, `JwtService`.
- Frontend engineers (1-2): React, Context API, route guards; own `AuthProvider`, pages, silent refresh.
- Platform/SRE engineer (1): K8s, HPA, Prometheus, Grafana, OTel, SendGrid; own observability + runbooks.
- Security engineer (≥0.5 FTE): policy ratification, pentest coordination, audit evidence; own R-001/R-002/R-008.
- Compliance lead: SOC2 dry-run, GDPR consent review, retention enforcement; owns R-007.
- QA engineer (1): unit/integration coverage, k6 load test, Playwright E2E, accessibility.
- Auth-team on-call rotation (≥4 engineers) for first 2 weeks post-GA.

## Success Criteria and Validation Approach

| Criterion | Metric | Target | Validation Method | Phase |
|---|---|---|---|---|
| Login latency (NFR-PERF-001) | p95 `AuthService.login()` | < 200ms | APM histogram `auth_login_duration_seconds` | Phase 6-7 |
| Concurrent auth throughput (NFR-PERF-002) | k6 sustained users | ≥ 500 with p95 < 200ms | k6 load test (NFR-PERF-002 row) | Phase 7 |
| Service availability (NFR-REL-001) | Uptime over 30-day rolling window | ≥ 99.9% | Synthetic login probe + SLO dashboard (NFR-REL-001 row) | Phase 6-7 |
| Password hashing cost (NFR-SEC-001) | bcrypt cost factor | = 12 | Unit test + hash prefix inspection | Phase 1 |
| Token signing algorithm (NFR-SEC-002) | JWT header `alg` + key size | RS256 + 2048-bit | Config assertion test | Phase 1 |
| Audit logging completeness (NFR-COMPLIANCE-001) | % of auth events with full fields | 100% | Log schema validator + SOC2 dry-run | Phase 6 |
| Audit log retention (NFR-COMPLIANCE-001) | Retention window | 12 months | PG partition + lifecycle policy audit | Phase 6 |
| Test coverage | Unit coverage across core components | > 80% | Jest coverage report in CI | Phase 1-4 |
| Token refresh latency | p95 `TokenManager.refresh()` | < 100ms | APM histogram `auth_token_refresh_total` | Phase 3-7 |
| Password hash operation (NFR-SEC-001) | `PasswordHasher.hash()` duration | < 500ms | Benchmark in unit test | Phase 1 |
| Registration conversion (PRD) | Landing→register→confirmed funnel | > 60% | Product analytics funnel | Post-GA (Phase 7) |
| Daily active authenticated users (PRD) | DAU with valid session | > 1000 within 30d of GA | Refresh-event analytics rollup | Post-GA (Phase 7) |
| Average session duration (PRD) | Refresh-event-derived session length | > 30 minutes | `auth_token_refresh_total` analytics | Post-GA (Phase 7) |
| Failed login rate (PRD) | fail / total logins | < 5% | `auth_login_total{outcome=fail}` | Post-GA (Phase 7) |
| Password reset completion (PRD) | reset requested → new password set | > 80% | Reset-event funnel | Post-GA (Phase 7) |
| No user enumeration | Identical 401 for wrong-email vs wrong-password | timing delta < 10ms | Pentest case (PENTEST) | Phase 7 |
| GDPR consent capture | Consent recorded at registration | 100% of new accounts | Row-level audit check on `UserProfile` | Phase 2 + SOC2 |

## Timeline Estimates

| Phase | Duration | Start | End | Key Milestones |
|---|---|---|---|---|
| Phase 0 | 2 weeks | Week 1 | Week 2 | M0 Infrastructure Baseline — PG+Redis+K8s+TLS+RSA+SendGrid provisioned |
| Phase 1 | 2 weeks | Week 3 | Week 4 | M1a Data Layer + Primitives — DM-001/DM-003/DM-004 + `PasswordHasher` + `JwtService` + `UserRepo` |
| Phase 2 | 2 weeks | Week 5 | Week 6 | M1 Core AuthService (2026-04-14) — login + register live on staging |
| Phase 3 | 2 weeks | Week 7 | Week 8 | M2 Token Management (2026-04-28) — refresh + /auth/me + logout |
| Phase 4 | 2 weeks | Week 9 | Week 10 | M3 Password Reset (2026-05-12) — end-to-end reset via SendGrid |
| Phase 5 | 2 weeks | Week 11 | Week 12 | M4 Frontend Integration (2026-05-26) — `LoginPage`+`RegisterPage`+`ProfilePage`+`AuthProvider` |
| Phase 6 | 2 weeks | Week 13 | Week 14 | M4b Audit + Admin — SOC2 dry-run + admin audit endpoint + dashboards green |
| Phase 7 | 2 weeks | Week 15 | Week 16 | M5 GA Release (2026-06-09) — Alpha → Beta (10%) → GA (100%) + legacy deprecated |

**Total estimated duration:** 16 weeks (4 months), aligned to the v1.0 Q2 2026 target with the SOC2 Q3 2026 deadline comfortably preceded.

## Open Questions

| # | Question | Impact | Blocking Phase | Resolution Owner |
|---|---|---|---|---|
| OQ-001 | Should `AuthService` support API key authentication for service-to-service calls? | Scope expansion; may add API-009 for key issuance | v1.1 (not blocking v1.0) | test-lead (deferred to v1.1 discussion) |
| OQ-002 | Maximum allowed `UserProfile.roles` array length? | Column constraint + validation; small impact | Phase 1 (before DM-001 constraint finalized) | auth-team (target 2026-04-01) |
| OQ-003 | Password reset emails: synchronous or asynchronous delivery? | Changes `AuthService.resetRequest` contract + SLA | Phase 4 (before FR-AUTH-005 implementation) | Engineering |
| OQ-004 | Maximum refresh tokens allowed per user across devices? | Redis keyspace design + device-limit policy | Phase 3 (before COMP-006 freeze) | Product |
| OQ-005 | Account lockout policy confirmation (TDD: 5/15min — Security signoff?) | Phase 2 lockout implementation depends on this | Phase 1 gate (PRE-OQ-005) | Security |
| OQ-006 | Should we support "remember me" to extend session duration? | Extra refresh-ttl tier; potential compliance impact | v1.1 or late v1.0 if prioritized | Product |
| OQ-007 | Jordan (admin) JTBD gap — admin unlock + audit query surface (PRD requires; TDD omits) | Added API-008 + ADMIN-UNLOCK rows as gap fills in Phase 6 — confirm RBAC model | Phase 6 (before API-008 goes live) | Product + Security (PRD requires; TDD should be updated) |










