# TASKLIST INDEX -- User Authentication Service

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | User Authentication Service |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-04-20 |
| TASKLIST_ROOT | .dev/releases/current/v1.1/ |
| Total Phases | 6 |
| Total Tasks | 108 |
| Total Deliverables | 108 |
| Complexity Class | HIGH |
| Primary Persona | architect |
| Consulting Personas | backend, security, frontend, devops, qa |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | TASKLIST_ROOT/tasklist-index.md |
| Phase 1 Tasklist | TASKLIST_ROOT/phase-1-tasklist.md |
| Phase 2 Tasklist | TASKLIST_ROOT/phase-2-tasklist.md |
| Phase 3 Tasklist | TASKLIST_ROOT/phase-3-tasklist.md |
| Phase 4 Tasklist | TASKLIST_ROOT/phase-4-tasklist.md |
| Phase 5 Tasklist | TASKLIST_ROOT/phase-5-tasklist.md |
| Phase 6 Tasklist | TASKLIST_ROOT/phase-6-tasklist.md |
| Execution Log | TASKLIST_ROOT/execution-log.md |
| Checkpoint Reports | TASKLIST_ROOT/checkpoints/ |
| Evidence Directory | TASKLIST_ROOT/evidence/ |
| Artifacts Directory | TASKLIST_ROOT/artifacts/ |
| Validation Reports | TASKLIST_ROOT/validation/ |
| Feedback Log | TASKLIST_ROOT/feedback-log.md |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Foundation -- Data + Auth + Consent | T01.01-T01.24 | STRICT: 11, STANDARD: 13, LIGHT: 0, EXEMPT: 0 |
| 2 | phase-2-tasklist.md | Token Management | T02.01-T02.19 | STRICT: 10, STANDARD: 8, LIGHT: 0, EXEMPT: 1 |
| 3 | phase-3-tasklist.md | Profile and Password Management | T03.01-T03.13 | STRICT: 7, STANDARD: 6, LIGHT: 0, EXEMPT: 0 |
| 4 | phase-4-tasklist.md | Frontend and Logout | T04.01-T04.18 | STRICT: 12, STANDARD: 6, LIGHT: 0, EXEMPT: 0 |
| 5 | phase-5-tasklist.md | Admin APIs and Observability | T05.01-T05.13 | STRICT: 5, STANDARD: 8, LIGHT: 0, EXEMPT: 0 |
| 6 | phase-6-tasklist.md | Production Readiness and Rollout | T06.01-T06.21 | STRICT: 11, STANDARD: 10, LIGHT: 0, EXEMPT: 0 |

## Source Snapshot

- Five-milestone delivery (M1 Foundation, M2 Token Management, M3 Password & Profile, M4 Frontend + Admin + Observability, M5 Production Readiness) ending GA 2026-06-09.
- Stateless JWT RS256 (2048-bit RSA, quarterly rotation, 15-min access), opaque refresh tokens (Redis, 7-day TTL, hashed SHA-256, 5-per-user cap with oldest-eviction).
- PostgreSQL 15 persistence for UserProfile (DM-001), auth audit log (DM-AUDIT), password-reset tokens (DM-RESET); Redis 7 for refresh tokens, lockout counter, email queue.
- bcrypt cost 12 via PasswordHasher abstraction; TLS 1.3 at gateway; CONFLICT-2 contract: /auth/register returns 201 UserProfile without auto-login.
- CONFLICT-1 compliance precedence: 12-month audit retention (OPS-004) overrides TDD §7.2 90-day default.
- GDPR consent captured at M1 registration (not M3) to satisfy data minimization per R-PRD-001.
- Phased rollout via AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH flags (0->1->5->25->50->100%); 4 automated rollback triggers (LATENCY/ERR/REDIS/DATA); OPS-011 GA go/no-go gate.

## Deterministic Rules Applied

- Roadmap items parsed in appearance order; R-### IDs assigned 1:1 for 107 roadmap deliverables.
- Phases derived from explicit milestone headings M1..M5; M4 split into Phase 4 and Phase 5 because roadmap M4 contains 31 deliverables (exceeds 25-task phase cap per Structural Quality Gate #13).
- Phase renumbering: sequential 1..6 with no gaps; M5 becomes Phase 6.
- Task IDs zero-padded T<PP>.<TT>; within-phase order preserves roadmap top-to-bottom.
- One Clarification Task inserted at Phase 2 start (T02.01) for OQ-M1-003 (RSA key custody) -- only unresolved blocker without committed default.
- Checkpoint cadence: every 5 tasks within a phase plus end-of-phase checkpoint.
- Deliverable Registry: 1 deliverable per task, IDs D-0001..D-0108 in task appearance order.
- Effort/Risk mappings computed per keyword matches in roadmap item text per Section 5.2.
- Compliance tier classification uses STRICT>EXEMPT>LIGHT>STANDARD priority; auth/security/token paths trigger +0.4 STRICT boost.
- Verification routing: STRICT -> sub-agent (quality-engineer, 60s); STANDARD -> direct test (30s); EXEMPT -> skip.
- MCP requirements: STRICT tier requires Sequential+Serena.
- Traceability Matrix links R-### -> T<PP>.<TT> -> D-#### -> artifact paths -> Tier -> Confidence.
- Multi-file output: one tasklist-index.md + six phase-N-tasklist.md files.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<=20 words) |
|---|---|---|
| R-001 | Phase 1 | DM-001 UserProfile PostgreSQL schema -- Create user_profiles table with all source fields and indexes per TDD §7.1 |
| R-002 | Phase 1 | DM-AUDIT Audit log PostgreSQL schema -- Create auth_audit_log table for SOC2 Type II event trail |
| R-003 | Phase 1 | COMP-AUTHSVC AuthService orchestrator class -- facade delegating to PasswordHasher/TokenManager/UserRepo/ConsentRecorder |
| R-004 | Phase 1 | COMP-PWDHASH PasswordHasher component -- Bcrypt abstraction with cost factor 12 per NFR-SEC-001 |
| R-005 | Phase 1 | COMP-USERREPO UserRepo data-access component -- PostgreSQL data access layer for UserProfile |
| R-006 | Phase 1 | COMP-CONSENT-REC ConsentRecorder component records consent evidence during registration (pulled forward from M3) |
| R-007 | Phase 1 | FR-AUTH-001 Login authentication logic -- AuthService.login() validates credentials via PasswordHasher |
| R-008 | Phase 1 | FR-AUTH-002 Registration with validation -- AuthService.register() creates UserProfile with email uniqueness policy |
| R-009 | Phase 1 | API-001 POST /auth/login endpoint -- REST endpoint binding per TDD §8.2 |
| R-010 | Phase 1 | API-002 POST /auth/register endpoint -- REST endpoint binding per TDD §8.2 (CONFLICT-2: 201 redirect-to-login) |
| R-011 | Phase 1 | FEAT-LOCK Account lockout enforcement -- Lockout after 5 failed attempts within 15 minutes |
| R-012 | Phase 1 | API-ERR Unified error envelope middleware -- {error:{code,message,status}} across all /auth/* endpoints |
| R-013 | Phase 1 | API-RATE Rate limiting configuration -- 10/min login per IP, 5/min register per IP |
| R-014 | Phase 1 | NFR-SEC-001 bcrypt cost 12 validation test -- Unit test enforcing PasswordHasher uses cost factor 12 |
| R-015 | Phase 1 | NFR-SEC-003 Transport and log redaction baseline -- TLS 1.3 at gateway and redact sensitive fields |
| R-016 | Phase 1 | NFR-GDPR-CONSENT GDPR consent capture at registration -- Consent flag + timestamp persisted at /auth/register |
| R-017 | Phase 1 | NFR-PERF-001 Login endpoint latency instrumentation p95 <200ms -- Histogram + p95 alert rule |
| R-018 | Phase 1 | NFR-PERF-002 Concurrent 500-user load profile k6 -- Validates 500 concurrent logins sustain <200ms p95 |
| R-019 | Phase 1 | TEST-001 Unit -- login with valid credentials returns AuthToken per TDD §15.2 |
| R-020 | Phase 1 | TEST-002 Unit -- login with invalid credentials returns 401 per TDD §15.2 |
| R-021 | Phase 1 | TEST-004 Integration -- registration persists UserProfile to database per TDD §15.2 |
| R-022 | Phase 1 | OPS-LOG-M1 Structured login/registration logging -- stdout JSON logs for login_success/failure and register |
| R-023 | Phase 1 | METRIC-REG Registration counter metric -- auth_registration_total counter per OPS-004 |
| R-024 | Phase 1 | METRIC-LOGIN Login counter metric -- auth_login_total counter per OPS-004 |
| R-025 | Phase 2 | DM-002 RefreshToken data model -- Entity persisted in Redis hash set keyed by user_id |
| R-026 | Phase 2 | COMP-JWTSVC JwtService -- RS256 signer/verifier using 2048-bit RSA keys with rotation |
| R-027 | Phase 2 | COMP-TOKMGR TokenManager service -- Issues, rotates, and revokes refresh tokens via Redis |
| R-028 | Phase 2 | NFR-SEC-002 Token security requirements -- Access tokens RS256 only, refresh tokens SHA-256 hashed |
| R-029 | Phase 2 | FR-AUTH-003 User Login token issuance path -- Endpoint validates credentials then issues access+refresh pair |
| R-030 | Phase 2 | FR-AUTH-004 Token Refresh -- POST /auth/refresh with rotation and replay detection |
| R-031 | Phase 2 | API-003 POST /auth/login endpoint -- HTTP contract 200 tokens, 401 invalid, 423 locked |
| R-032 | Phase 2 | API-004 POST /auth/refresh endpoint -- HTTP contract 200 new pair, 401 invalid/replay, 429 rate |
| R-033 | Phase 2 | COMP-AUTHMW AuthMiddleware -- Express middleware extracting bearer token and attaching req.user |
| R-034 | Phase 2 | FEAT-REFRESH-FLAG Feature flag AUTH_TOKEN_REFRESH -- LaunchDarkly flag gating new refresh flow |
| R-035 | Phase 2 | NFR-PERF-003 Token issuance performance -- p95 <100ms at 100 RPS sustained 5 minutes |
| R-036 | Phase 2 | METRIC-REFRESH Metrics for refresh flow -- Prometheus counters and histogram for refresh |
| R-037 | Phase 2 | TEST-003 JWT validation test suite -- Unit tests for JwtService coverage >=90% |
| R-038 | Phase 2 | TEST-005 Refresh rotation integration test -- login + refresh + replay returns 401 family revocation |
| R-039 | Phase 2 | TEST-ME GET /profile protected route fixture -- standing integration test for middleware behaviour |
| R-040 | Phase 2 | OPS-LOG-M2 Token-lifecycle audit logs -- Extend DM-AUDIT event_type enum with token events |
| R-041 | Phase 2 | SEC-RT-HASH Refresh token hashing at rest -- SHA-256 stored in Redis plaintext never persisted |
| R-042 | Phase 2 | SEC-CLOCK-SKEW Clock-skew tolerance +/-30s -- JwtService configured with 30-second leeway |
| R-043 | Phase 3 | FR-PROF-001 Profile Retrieval -- GET /profile returns authenticated caller profile |
| R-044 | Phase 3 | FR-PROF-002 Profile Update -- PUT /profile accepts display_name only (v1.0 scope) |
| R-045 | Phase 3 | FR-AUTH-005 Password Change authenticated -- POST /auth/password/change revokes all refresh tokens |
| R-046 | Phase 3 | FR-AUTH-006 Password Reset Request -- POST /auth/password/reset-request always returns 200 enumeration-resistant |
| R-047 | Phase 3 | FR-AUTH-007 Password Reset Confirm -- POST /auth/password/reset-confirm rotates password invalidates sessions |
| R-048 | Phase 3 | DM-RESET PasswordResetToken data model -- Entity persisted in PostgreSQL token_hash SHA-256 indexed |
| R-049 | Phase 3 | COMP-EMAILQ EmailDispatcher async queue -- Queue-backed email dispatcher BullMQ on Redis 7 |
| R-050 | Phase 3 | API-005 GET/PUT /profile endpoints -- Protected by authMiddleware contract tests green |
| R-051 | Phase 3 | API-006 POST /auth/password/change -- Protected 200 ok 401 wrong current 400 weak |
| R-052 | Phase 3 | API-RESET-REQ POST /auth/password/reset-request -- Public always 200 rate-limit 3/hour/email |
| R-053 | Phase 3 | API-RESET-CONF POST /auth/password/reset-confirm -- Public token-bearer 200 ok 400 invalid-expired |
| R-054 | Phase 3 | TEST-PROFILE Profile integration tests -- E2E login then GET PUT profile negative unauth invalid |
| R-055 | Phase 3 | TEST-RESET Password reset integration test -- E2E register reset-request reset-confirm login new password |
| R-056 | Phase 4 | COMP-001 LoginPage component -- React component at /login posts to /auth/login memory-only token |
| R-057 | Phase 4 | COMP-002 RegisterPage component -- React component at /register with consent checkbox redirects /login |
| R-058 | Phase 4 | COMP-003 ProfilePage component -- React component at /profile with editable display_name |
| R-059 | Phase 4 | COMP-004 PasswordChangeForm -- Embedded ProfilePage form calling POST /auth/password/change |
| R-060 | Phase 4 | COMP-005 PasswordResetForm -- Two-step flow request email then confirm new password |
| R-061 | Phase 4 | COMP-006 AuthGuard router component -- React Router guard with silent refresh before redirect |
| R-062 | Phase 4 | SEC-HTTPONLY HttpOnly refresh-token cookie -- Backend sets HttpOnly Secure SameSite=Strict cookie |
| R-063 | Phase 4 | SEC-MEMSTORE Access token in memory only -- Frontend stores access token in module-scoped variable |
| R-064 | Phase 4 | FEAT-SILENTREF Silent refresh on expiry -- Interceptor fires POST /auth/refresh on 401 or preemptively |
| R-065 | Phase 4 | FEAT-401INT 401 response interceptor -- Axios interceptor triggers silent refresh retries original |
| R-066 | Phase 4 | UI-ERR Error boundaries + toast system -- React ErrorBoundary wraps each page network errors via toast |
| R-067 | Phase 4 | UI-A11Y Accessibility audit pass -- WCAG 2.1 AA compliance across auth screens keyboard ARIA contrast |
| R-068 | Phase 4 | TEST-006 Frontend component test suite -- React Testing Library Jest coverage >=80% auth module |
| R-069 | Phase 4 | E2E-REFRESH Playwright E2E silent refresh -- login wait expiry protected request seamless refresh |
| R-070 | Phase 4 | E2E-LOGOUT Playwright E2E logout -- login click LogoutControl assert cookie cleared 401 /login |
| R-071 | Phase 4 | FUNNEL-REG Registration funnel instrumentation -- Frontend events feed PRD NFR-001 conversion KPIs |
| R-072 | Phase 4 | API-007 POST /auth/logout -- Server endpoint revokes refresh token clears httpOnly cookie 204 |
| R-073 | Phase 4 | COMP-016 LogoutControl component -- React component button in header calling POST /auth/logout |
| R-074 | Phase 5 | API-008 GET /admin/auth/users -- Admin-only paginated list of UserProfile rows redacted |
| R-075 | Phase 5 | API-009 POST /admin/auth/users/:id/revoke-sessions -- Admin endpoint calling revokeAllForUser audit event |
| R-076 | Phase 5 | API-010 POST /admin/auth/users/:id/unlock -- Admin endpoint clearing lockout counter audit event |
| R-077 | Phase 5 | COMP-018 AdminAuthEventService -- Server-side service encapsulating admin-originated mutations |
| R-078 | Phase 5 | COMP-019 AccountLockManager -- Server-side service centralising lockout logic from M1 FEAT-LOCK |
| R-079 | Phase 5 | API-011 GET /health -- Liveness readiness endpoint returns status db redis version uptime |
| R-080 | Phase 5 | OBS-001 Prometheus metrics endpoint -- GET /metrics exposes scrape format counters histogram |
| R-081 | Phase 5 | OBS-002 Structured JSON logging -- Logger pino emits JSON timestamp level service trace_id fields |
| R-082 | Phase 5 | OBS-003 Distributed trace IDs -- OpenTelemetry SDK integrated traces propagate to OTLP Tempo |
| R-083 | Phase 5 | OBS-004 Audit-log dashboard -- Grafana dashboard reading from DM-AUDIT logins failed-login lockouts |
| R-084 | Phase 5 | OBS-005 SLI/SLO definitions -- login-success >=99.5% refresh >=99.9% p95 login <200ms refresh <100ms |
| R-085 | Phase 5 | OBS-006 Synthetic monitors -- Checkly probe suite /health every 1min full flow every 5min |
| R-086 | Phase 5 | OBS-007 Alerting runbook -- docs/runbooks/auth.md symptom diagnosis mitigation escalation |
| R-087 | Phase 6 | MIG-001 Legacy user data migration script -- One-time job upserting legacy_users into new UserProfile |
| R-088 | Phase 6 | MIG-002 Parallel-run reconciliation -- Every login hits legacy AND new systems discrepancies logged |
| R-089 | Phase 6 | MIG-003 Legacy auth retirement -- After 100% stable 48h legacy routes return 410 archived |
| R-090 | Phase 6 | FEAT-FLAG-NEWLOGIN Rollout AUTH_NEW_LOGIN -- Phased 0-1-5-25-50-100% SLO-gated advancement |
| R-091 | Phase 6 | FEAT-FLAG-REFRESH Rollout AUTH_TOKEN_REFRESH -- Same phased approach dependent NEWLOGIN >=25% |
| R-092 | Phase 6 | OPS-001 Production Prometheus Grafana provisioned -- Prod instances separate staging SSO auth |
| R-093 | Phase 6 | OPS-002 Production Tempo Jaeger trace backend -- Prod retention 7-day sampling 10% 100% 5xx |
| R-094 | Phase 6 | OPS-003 Production Loki log aggregation -- Prod cluster ingesting structured JSON retention 14d+90d |
| R-095 | Phase 6 | OPS-004 Audit-log retention 12 months -- DM-AUDIT rows older than 12 months archived S3 Glacier |
| R-096 | Phase 6 | OPS-005 SMTP email provider prod rollout -- Prod credentials DKIM SPF DMARC bounce complaint monitoring |
| R-097 | Phase 6 | ALERT-LOGIN-FAIL Login failure spike alert -- Prometheus rate >0.30 sustained 10min pages oncall |
| R-098 | Phase 6 | ALERT-LATENCY Login p95 latency alert -- histogram_quantile >300ms sustained 10min |
| R-099 | Phase 6 | ALERT-REDIS Redis unavailable alert -- redis_up==0 >1min pages oncall immediately |
| R-100 | Phase 6 | ROLLBACK-AUTO-LATENCY Automated rollback latency breach -- login p95 >500ms 15min auto-reverts |
| R-101 | Phase 6 | ROLLBACK-AUTO-ERR Automated rollback error rate -- 5xx-rate >1% 10min auto-reverts |
| R-102 | Phase 6 | ROLLBACK-AUTO-REDIS Automated rollback Redis unavailability -- Redis >3min read-only mode flag flip |
| R-103 | Phase 6 | ROLLBACK-AUTO-DATA Automated rollback DB write-failure spike -- DM-001 write error >5% 5min halt |
| R-104 | Phase 6 | ROLLBACK-STEPS Manual rollback runbook -- docs/runbooks/auth-rollback.md step-by-step full stack revert |
| R-105 | Phase 6 | NFR-REL-001 Reliability 99.9% availability -- Prod service meets 99.9% monthly SLO post-rollout |
| R-106 | Phase 6 | SUCC-SLO-BOARD Production SLO dashboard -- Grafana board login-success refresh-success p95 latencies |
| R-107 | Phase 6 | OPS-011 GA go/no-go gate -- Formal signed-off gate checklist ROLLBACK-AUTO chaos SUCC-SLO-BOARD ALERT |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---|---|---|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | user_profiles migration + schema file | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0001/spec.md, notes.md, evidence.md | M | High |
| D-0002 | T01.02 | R-002 | auth_audit_log migration + schema file | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0002/spec.md, notes.md, evidence.md | S | High |
| D-0003 | T01.03 | R-003 | AuthService facade class src/services/auth-service.ts | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0003/spec.md, notes.md, evidence.md | M | Medium |
| D-0004 | T01.04 | R-004 | PasswordHasher class with bcrypt cost 12 | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0004/spec.md, notes.md, evidence.md | S | Medium |
| D-0005 | T01.05 | R-005 | UserRepo data-access class with pg-pool | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0005/spec.md, notes.md, evidence.md | M | Medium |
| D-0006 | T01.06 | R-006 | ConsentRecorder class with audit emission | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0006/spec.md, notes.md, evidence.md | S | Medium |
| D-0007 | T01.07 | R-007 | AuthService.login() implementation | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0007/spec.md, notes.md, evidence.md | M | Medium |
| D-0008 | T01.08 | R-008 | AuthService.register() implementation | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0008/spec.md, notes.md, evidence.md | M | Medium |
| D-0009 | T01.09 | R-009 | POST /v1/auth/login route binding | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0009/spec.md, notes.md, evidence.md | S | Medium |
| D-0010 | T01.10 | R-010 | POST /v1/auth/register route binding | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0010/spec.md, notes.md, evidence.md | S | Medium |
| D-0011 | T01.11 | R-011 | Lockout enforcement Redis-backed 5/15min | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0011/spec.md, notes.md, evidence.md | M | High |
| D-0012 | T01.12 | R-012 | Unified error envelope middleware | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0012/spec.md, notes.md, evidence.md | S | Low |
| D-0013 | T01.13 | R-013 | API Gateway rate-limit config | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0013/spec.md, notes.md, evidence.md | S | Low |
| D-0014 | T01.14 | R-014 | bcrypt cost 12 unit test | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0014/spec.md, notes.md, evidence.md | XS | Low |
| D-0015 | T01.15 | R-015 | TLS 1.3 ingress + log redaction middleware | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0015/spec.md, notes.md, evidence.md | S | Medium |
| D-0016 | T01.16 | R-016 | GDPR consent capture wiring at registration | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0016/spec.md, notes.md, evidence.md | S | Medium |
| D-0017 | T01.17 | R-017 | Prometheus histogram + p95 alert rule | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0017/spec.md, notes.md, evidence.md | S | Low |
| D-0018 | T01.18 | R-018 | k6 load script tests/load/login.js | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0018/spec.md, notes.md, evidence.md | S | Low |
| D-0019 | T01.19 | R-019 | Unit test TEST-001 login valid credentials | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0019/spec.md, notes.md, evidence.md | XS | Low |
| D-0020 | T01.20 | R-020 | Unit test TEST-002 login invalid credentials | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0020/spec.md, notes.md, evidence.md | XS | Low |
| D-0021 | T01.21 | R-021 | Integration test TEST-004 register persistence | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0021/spec.md, notes.md, evidence.md | S | Low |
| D-0022 | T01.22 | R-022 | Structured JSON logger pino/winston wiring | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0022/spec.md, notes.md, evidence.md | S | Low |
| D-0023 | T01.23 | R-023 | Prometheus counter auth_registration_total | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0023/spec.md, notes.md, evidence.md | XS | Low |
| D-0024 | T01.24 | R-024 | Prometheus counter auth_login_total | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0024/spec.md, notes.md, evidence.md | XS | Low |
| D-0025 | T02.01 | -- | Clarification: OQ-M1-003 JWT key custody approval artifact | EXEMPT | Skip verification | TASKLIST_ROOT/artifacts/D-0025/spec.md, notes.md, evidence.md | XS | Low |
| D-0026 | T02.02 | R-025 | RefreshToken Redis hash schema + cap eviction | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0026/spec.md, notes.md, evidence.md | M | High |
| D-0027 | T02.03 | R-026 | JwtService RS256 signer/verifier + rotateKeys | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0027/spec.md, notes.md, evidence.md | L | High |
| D-0028 | T02.04 | R-027 | TokenManager service with family revocation | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0028/spec.md, notes.md, evidence.md | L | High |
| D-0029 | T02.05 | R-028 | NFR-SEC-002 token security config enforcement | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0029/spec.md, notes.md, evidence.md | M | Medium |
| D-0030 | T02.06 | R-029 | FR-AUTH-003 login-with-token-issuance path | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0030/spec.md, notes.md, evidence.md | L | High |
| D-0031 | T02.07 | R-030 | FR-AUTH-004 refresh endpoint with rotation/replay | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0031/spec.md, notes.md, evidence.md | M | High |
| D-0032 | T02.08 | R-031 | POST /auth/login HTTP contract implementation | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0032/spec.md, notes.md, evidence.md | M | Medium |
| D-0033 | T02.09 | R-032 | POST /auth/refresh HTTP contract implementation | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0033/spec.md, notes.md, evidence.md | M | High |
| D-0034 | T02.10 | R-033 | AuthMiddleware Express bearer-token validator | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0034/spec.md, notes.md, evidence.md | M | Medium |
| D-0035 | T02.11 | R-034 | AUTH_TOKEN_REFRESH LaunchDarkly feature flag | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0035/spec.md, notes.md, evidence.md | S | Low |
| D-0036 | T02.12 | R-035 | NFR-PERF-003 k6 harness token issuance p95 | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0036/spec.md, notes.md, evidence.md | M | Low |
| D-0037 | T02.13 | R-036 | METRIC-REFRESH Prometheus counters + histogram | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0037/spec.md, notes.md, evidence.md | S | Low |
| D-0038 | T02.14 | R-037 | TEST-003 JwtService unit test suite >=90% | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0038/spec.md, notes.md, evidence.md | M | Low |
| D-0039 | T02.15 | R-038 | TEST-005 refresh rotation integration test | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0039/spec.md, notes.md, evidence.md | M | Low |
| D-0040 | T02.16 | R-039 | TEST-ME GET /profile middleware fixture | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0040/spec.md, notes.md, evidence.md | S | Low |
| D-0041 | T02.17 | R-040 | OPS-LOG-M2 token-lifecycle audit events | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0041/spec.md, notes.md, evidence.md | S | Low |
| D-0042 | T02.18 | R-041 | SEC-RT-HASH refresh-token SHA-256 hashing | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0042/spec.md, notes.md, evidence.md | S | Medium |
| D-0043 | T02.19 | R-042 | SEC-CLOCK-SKEW 30-second leeway config | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0043/spec.md, notes.md, evidence.md | S | Low |
| D-0044 | T03.01 | R-043 | GET /profile endpoint + handler | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0044/spec.md, notes.md, evidence.md | M | Low |
| D-0045 | T03.02 | R-044 | PUT /profile handler display_name only | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0045/spec.md, notes.md, evidence.md | S | Low |
| D-0046 | T03.03 | R-045 | FR-AUTH-005 password change + revoke-all | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0046/spec.md, notes.md, evidence.md | M | High |
| D-0047 | T03.04 | R-046 | FR-AUTH-006 reset-request enumeration-safe | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0047/spec.md, notes.md, evidence.md | M | High |
| D-0048 | T03.05 | R-047 | FR-AUTH-007 reset-confirm + session revoke | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0048/spec.md, notes.md, evidence.md | M | High |
| D-0049 | T03.06 | R-048 | DM-RESET PostgreSQL schema + cleanup job | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0049/spec.md, notes.md, evidence.md | S | Medium |
| D-0050 | T03.07 | R-049 | COMP-EMAILQ BullMQ async email dispatcher | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0050/spec.md, notes.md, evidence.md | M | Low |
| D-0051 | T03.08 | R-050 | API-005 GET/PUT /profile OpenAPI contract | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0051/spec.md, notes.md, evidence.md | S | Low |
| D-0052 | T03.09 | R-051 | API-006 POST /auth/password/change contract | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0052/spec.md, notes.md, evidence.md | S | Medium |
| D-0053 | T03.10 | R-052 | API-RESET-REQ POST /auth/password/reset-request | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0053/spec.md, notes.md, evidence.md | S | Medium |
| D-0054 | T03.11 | R-053 | API-RESET-CONF POST /auth/password/reset-confirm | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0054/spec.md, notes.md, evidence.md | S | Medium |
| D-0055 | T03.12 | R-054 | TEST-PROFILE profile integration E2E | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0055/spec.md, notes.md, evidence.md | S | Low |
| D-0056 | T03.13 | R-055 | TEST-RESET password reset integration E2E | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0056/spec.md, notes.md, evidence.md | M | Low |
| D-0057 | T04.01 | R-056 | COMP-001 LoginPage React component | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0057/spec.md, notes.md, evidence.md | M | Medium |
| D-0058 | T04.02 | R-057 | COMP-002 RegisterPage React component | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0058/spec.md, notes.md, evidence.md | M | Medium |
| D-0059 | T04.03 | R-058 | COMP-003 ProfilePage React component | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0059/spec.md, notes.md, evidence.md | M | Low |
| D-0060 | T04.04 | R-059 | COMP-004 PasswordChangeForm component | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0060/spec.md, notes.md, evidence.md | S | Medium |
| D-0061 | T04.05 | R-060 | COMP-005 PasswordResetForm two-step flow | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0061/spec.md, notes.md, evidence.md | M | Medium |
| D-0062 | T04.06 | R-061 | COMP-006 AuthGuard router component | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0062/spec.md, notes.md, evidence.md | M | Medium |
| D-0063 | T04.07 | R-062 | SEC-HTTPONLY HttpOnly SameSite refresh cookie | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0063/spec.md, notes.md, evidence.md | S | Medium |
| D-0064 | T04.08 | R-063 | SEC-MEMSTORE in-memory access token pattern | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0064/spec.md, notes.md, evidence.md | S | Medium |
| D-0065 | T04.09 | R-064 | FEAT-SILENTREF silent refresh interceptor | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0065/spec.md, notes.md, evidence.md | M | Medium |
| D-0066 | T04.10 | R-065 | FEAT-401INT axios 401 response interceptor | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0066/spec.md, notes.md, evidence.md | S | Medium |
| D-0067 | T04.11 | R-066 | UI-ERR ErrorBoundary + toast system | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0067/spec.md, notes.md, evidence.md | S | Low |
| D-0068 | T04.12 | R-067 | UI-A11Y WCAG 2.1 AA audit pass auth screens | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0068/spec.md, notes.md, evidence.md | M | Low |
| D-0069 | T04.13 | R-068 | TEST-006 frontend component test suite | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0069/spec.md, notes.md, evidence.md | M | Low |
| D-0070 | T04.14 | R-069 | E2E-REFRESH Playwright silent refresh scenario | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0070/spec.md, notes.md, evidence.md | M | Low |
| D-0071 | T04.15 | R-070 | E2E-LOGOUT Playwright logout scenario | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0071/spec.md, notes.md, evidence.md | S | Low |
| D-0072 | T04.16 | R-071 | FUNNEL-REG registration funnel analytics events | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0072/spec.md, notes.md, evidence.md | S | Low |
| D-0073 | T04.17 | R-072 | API-007 POST /auth/logout endpoint | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0073/spec.md, notes.md, evidence.md | S | Medium |
| D-0074 | T04.18 | R-073 | COMP-016 LogoutControl React component | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0074/spec.md, notes.md, evidence.md | S | Medium |
| D-0075 | T05.01 | R-074 | API-008 GET /admin/auth/users endpoint | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0075/spec.md, notes.md, evidence.md | M | Medium |
| D-0076 | T05.02 | R-075 | API-009 POST /admin/.../revoke-sessions | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0076/spec.md, notes.md, evidence.md | S | Medium |
| D-0077 | T05.03 | R-076 | API-010 POST /admin/.../unlock endpoint | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0077/spec.md, notes.md, evidence.md | S | Medium |
| D-0078 | T05.04 | R-077 | COMP-018 AdminAuthEventService | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0078/spec.md, notes.md, evidence.md | M | Medium |
| D-0079 | T05.05 | R-078 | COMP-019 AccountLockManager | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0079/spec.md, notes.md, evidence.md | M | Medium |
| D-0080 | T05.06 | R-079 | API-011 GET /health liveness readiness | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0080/spec.md, notes.md, evidence.md | S | Low |
| D-0081 | T05.07 | R-080 | OBS-001 GET /metrics Prometheus exposition | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0081/spec.md, notes.md, evidence.md | M | Low |
| D-0082 | T05.08 | R-081 | OBS-002 pino structured JSON logger config | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0082/spec.md, notes.md, evidence.md | S | Low |
| D-0083 | T05.09 | R-082 | OBS-003 OpenTelemetry SDK + OTLP exporter | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0083/spec.md, notes.md, evidence.md | M | Low |
| D-0084 | T05.10 | R-083 | OBS-004 Grafana audit-log dashboard | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0084/spec.md, notes.md, evidence.md | M | Low |
| D-0085 | T05.11 | R-084 | OBS-005 SLI/SLO Prometheus recording rules | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0085/spec.md, notes.md, evidence.md | M | Low |
| D-0086 | T05.12 | R-085 | OBS-006 Checkly synthetic monitor suite | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0086/spec.md, notes.md, evidence.md | S | Low |
| D-0087 | T05.13 | R-086 | OBS-007 docs/runbooks/auth.md alerting runbook | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0087/spec.md, notes.md, evidence.md | S | Low |
| D-0088 | T06.01 | R-087 | MIG-001 legacy_users -> UserProfile migration script | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0088/spec.md, notes.md, evidence.md | L | High |
| D-0089 | T06.02 | R-088 | MIG-002 parallel-run reconciliation + mismatch table | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0089/spec.md, notes.md, evidence.md | M | High |
| D-0090 | T06.03 | R-089 | MIG-003 legacy auth retirement 410 Gone | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0090/spec.md, notes.md, evidence.md | S | Medium |
| D-0091 | T06.04 | R-090 | FEAT-FLAG-NEWLOGIN phased rollout segment | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0091/spec.md, notes.md, evidence.md | M | High |
| D-0092 | T06.05 | R-091 | FEAT-FLAG-REFRESH phased rollout segment | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0092/spec.md, notes.md, evidence.md | M | Medium |
| D-0093 | T06.06 | R-092 | OPS-001 production Prometheus + Grafana stack | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0093/spec.md, notes.md, evidence.md | M | Low |
| D-0094 | T06.07 | R-093 | OPS-002 production Tempo trace backend | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0094/spec.md, notes.md, evidence.md | S | Low |
| D-0095 | T06.08 | R-094 | OPS-003 production Loki log aggregation | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0095/spec.md, notes.md, evidence.md | M | Low |
| D-0096 | T06.09 | R-095 | OPS-004 12-month audit archival job + manifest | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0096/spec.md, notes.md, evidence.md | M | Medium |
| D-0097 | T06.10 | R-096 | OPS-005 prod SMTP + DKIM/SPF/DMARC | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0097/spec.md, notes.md, evidence.md | S | Low |
| D-0098 | T06.11 | R-097 | ALERT-LOGIN-FAIL Prometheus alert rule | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0098/spec.md, notes.md, evidence.md | S | Low |
| D-0099 | T06.12 | R-098 | ALERT-LATENCY login p95 latency alert rule | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0099/spec.md, notes.md, evidence.md | S | Low |
| D-0100 | T06.13 | R-099 | ALERT-REDIS Redis unavailable alert rule | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0100/spec.md, notes.md, evidence.md | S | Low |
| D-0101 | T06.14 | R-100 | ROLLBACK-AUTO-LATENCY rule + chaos drill | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0101/spec.md, notes.md, evidence.md | M | High |
| D-0102 | T06.15 | R-101 | ROLLBACK-AUTO-ERR rule + chaos drill | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0102/spec.md, notes.md, evidence.md | M | High |
| D-0103 | T06.16 | R-102 | ROLLBACK-AUTO-REDIS rule + read-only mode | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0103/spec.md, notes.md, evidence.md | M | High |
| D-0104 | T06.17 | R-103 | ROLLBACK-AUTO-DATA DB write-error rollback | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0104/spec.md, notes.md, evidence.md | M | High |
| D-0105 | T06.18 | R-104 | ROLLBACK-STEPS manual rollback runbook | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0105/spec.md, notes.md, evidence.md | S | Medium |
| D-0106 | T06.19 | R-105 | NFR-REL-001 99.9% availability SLO | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0106/spec.md, notes.md, evidence.md | M | Low |
| D-0107 | T06.20 | R-106 | SUCC-SLO-BOARD prod Grafana SLO dashboard | STANDARD | Direct test execution | TASKLIST_ROOT/artifacts/D-0107/spec.md, notes.md, evidence.md | S | Low |
| D-0108 | T06.21 | R-107 | OPS-011 GA go/no-go gate signed checklist | STRICT | Sub-agent (quality-engineer) | TASKLIST_ROOT/artifacts/D-0108/spec.md, notes.md, evidence.md | M | High |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---|---|---|---|---|---|
| R-001 | T01.01 | D-0001 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0001/ |
| R-002 | T01.02 | D-0002 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0002/ |
| R-003 | T01.03 | D-0003 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0003/ |
| R-004 | T01.04 | D-0004 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0004/ |
| R-005 | T01.05 | D-0005 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0005/ |
| R-006 | T01.06 | D-0006 | STRICT | 80% | TASKLIST_ROOT/artifacts/D-0006/ |
| R-007 | T01.07 | D-0007 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0007/ |
| R-008 | T01.08 | D-0008 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0008/ |
| R-009 | T01.09 | D-0009 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0009/ |
| R-010 | T01.10 | D-0010 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0010/ |
| R-011 | T01.11 | D-0011 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0011/ |
| R-012 | T01.12 | D-0012 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0012/ |
| R-013 | T01.13 | D-0013 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0013/ |
| R-014 | T01.14 | D-0014 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0014/ |
| R-015 | T01.15 | D-0015 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0015/ |
| R-016 | T01.16 | D-0016 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0016/ |
| R-017 | T01.17 | D-0017 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0017/ |
| R-018 | T01.18 | D-0018 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0018/ |
| R-019 | T01.19 | D-0019 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0019/ |
| R-020 | T01.20 | D-0020 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0020/ |
| R-021 | T01.21 | D-0021 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0021/ |
| R-022 | T01.22 | D-0022 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0022/ |
| R-023 | T01.23 | D-0023 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0023/ |
| R-024 | T01.24 | D-0024 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0024/ |
| -- | T02.01 | D-0025 | EXEMPT | 95% | TASKLIST_ROOT/artifacts/D-0025/ |
| R-025 | T02.02 | D-0026 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0026/ |
| R-026 | T02.03 | D-0027 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0027/ |
| R-027 | T02.04 | D-0028 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0028/ |
| R-028 | T02.05 | D-0029 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0029/ |
| R-029 | T02.06 | D-0030 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0030/ |
| R-030 | T02.07 | D-0031 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0031/ |
| R-031 | T02.08 | D-0032 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0032/ |
| R-032 | T02.09 | D-0033 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0033/ |
| R-033 | T02.10 | D-0034 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0034/ |
| R-034 | T02.11 | D-0035 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0035/ |
| R-035 | T02.12 | D-0036 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0036/ |
| R-036 | T02.13 | D-0037 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0037/ |
| R-037 | T02.14 | D-0038 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0038/ |
| R-038 | T02.15 | D-0039 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0039/ |
| R-039 | T02.16 | D-0040 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0040/ |
| R-040 | T02.17 | D-0041 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0041/ |
| R-041 | T02.18 | D-0042 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0042/ |
| R-042 | T02.19 | D-0043 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0043/ |
| R-043 | T03.01 | D-0044 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0044/ |
| R-044 | T03.02 | D-0045 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0045/ |
| R-045 | T03.03 | D-0046 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0046/ |
| R-046 | T03.04 | D-0047 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0047/ |
| R-047 | T03.05 | D-0048 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0048/ |
| R-048 | T03.06 | D-0049 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0049/ |
| R-049 | T03.07 | D-0050 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0050/ |
| R-050 | T03.08 | D-0051 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0051/ |
| R-051 | T03.09 | D-0052 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0052/ |
| R-052 | T03.10 | D-0053 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0053/ |
| R-053 | T03.11 | D-0054 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0054/ |
| R-054 | T03.12 | D-0055 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0055/ |
| R-055 | T03.13 | D-0056 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0056/ |
| R-056 | T04.01 | D-0057 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0057/ |
| R-057 | T04.02 | D-0058 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0058/ |
| R-058 | T04.03 | D-0059 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0059/ |
| R-059 | T04.04 | D-0060 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0060/ |
| R-060 | T04.05 | D-0061 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0061/ |
| R-061 | T04.06 | D-0062 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0062/ |
| R-062 | T04.07 | D-0063 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0063/ |
| R-063 | T04.08 | D-0064 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0064/ |
| R-064 | T04.09 | D-0065 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0065/ |
| R-065 | T04.10 | D-0066 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0066/ |
| R-066 | T04.11 | D-0067 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0067/ |
| R-067 | T04.12 | D-0068 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0068/ |
| R-068 | T04.13 | D-0069 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0069/ |
| R-069 | T04.14 | D-0070 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0070/ |
| R-070 | T04.15 | D-0071 | STANDARD | 80% | TASKLIST_ROOT/artifacts/D-0071/ |
| R-071 | T04.16 | D-0072 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0072/ |
| R-072 | T04.17 | D-0073 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0073/ |
| R-073 | T04.18 | D-0074 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0074/ |
| R-074 | T05.01 | D-0075 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0075/ |
| R-075 | T05.02 | D-0076 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0076/ |
| R-076 | T05.03 | D-0077 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0077/ |
| R-077 | T05.04 | D-0078 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0078/ |
| R-078 | T05.05 | D-0079 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0079/ |
| R-079 | T05.06 | D-0080 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0080/ |
| R-080 | T05.07 | D-0081 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0081/ |
| R-081 | T05.08 | D-0082 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0082/ |
| R-082 | T05.09 | D-0083 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0083/ |
| R-083 | T05.10 | D-0084 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0084/ |
| R-084 | T05.11 | D-0085 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0085/ |
| R-085 | T05.12 | D-0086 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0086/ |
| R-086 | T05.13 | D-0087 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0087/ |
| R-087 | T06.01 | D-0088 | STRICT | 95% | TASKLIST_ROOT/artifacts/D-0088/ |
| R-088 | T06.02 | D-0089 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0089/ |
| R-089 | T06.03 | D-0090 | STRICT | 85% | TASKLIST_ROOT/artifacts/D-0090/ |
| R-090 | T06.04 | D-0091 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0091/ |
| R-091 | T06.05 | D-0092 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0092/ |
| R-092 | T06.06 | D-0093 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0093/ |
| R-093 | T06.07 | D-0094 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0094/ |
| R-094 | T06.08 | D-0095 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0095/ |
| R-095 | T06.09 | D-0096 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0096/ |
| R-096 | T06.10 | D-0097 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0097/ |
| R-097 | T06.11 | D-0098 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0098/ |
| R-098 | T06.12 | D-0099 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0099/ |
| R-099 | T06.13 | D-0100 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0100/ |
| R-100 | T06.14 | D-0101 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0101/ |
| R-101 | T06.15 | D-0102 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0102/ |
| R-102 | T06.16 | D-0103 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0103/ |
| R-103 | T06.17 | D-0104 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0104/ |
| R-104 | T06.18 | D-0105 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0105/ |
| R-105 | T06.19 | D-0106 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0106/ |
| R-106 | T06.20 | D-0107 | STANDARD | 75% | TASKLIST_ROOT/artifacts/D-0107/ |
| R-107 | T06.21 | D-0108 | STRICT | 90% | TASKLIST_ROOT/artifacts/D-0108/ |

## Execution Log Template

**Intended Path:** TASKLIST_ROOT/execution-log.md

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<=12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---|---|---|---|---|---|---|
| (pending execution) | T01.01 | STRICT | D-0001 | -- | Manual | TBD | TASKLIST_ROOT/evidence/T01.01/ |

## Checkpoint Report Template

**Template:**
- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status`
  - `Overall: Pass | Fail | TBD`
- `## Verification Results` (exactly 3 bullets; align to checkpoint Verification bullets)
- `## Exit Criteria Assessment` (exactly 3 bullets; align to checkpoint Exit Criteria bullets)
- `## Issues & Follow-ups`
  - List blocking issues; reference T<PP>.<TT> and D-####
- `## Evidence`
  - Bullet list of intended evidence paths under TASKLIST_ROOT/evidence/

## Feedback Collection Template

**Intended Path:** TASKLIST_ROOT/feedback-log.md

| Task ID | Original Tier | Override Tier | Override Reason (<=15 words) | Completion Status | Quality Signal | Time Variance |
|---|---|---|---|---|---|---|
| T01.01 | STRICT | -- | -- | pending | pending | pending |

## Generation Notes

- M4 from the roadmap contained 31 deliverables, exceeding the Structural Quality Gate #13 cap of 25 tasks per phase. M4 was deterministically split into Phase 4 (Frontend + Logout, 18 tasks) and Phase 5 (Admin APIs + Observability, 13 tasks). M5 then became Phase 6.
- One Clarification Task (T02.01) was inserted at the start of Phase 2 for OQ-M1-003 (JWT RSA key custody) because it is the only open question without a "Committed default" resolution and it blocks M2 token issuance.
- All other open questions with "Committed default: ..." wording were treated as resolved and did not trigger Clarification Tasks.
- TASKLIST_ROOT version token derived from the first `v<digits>(.<digits>)+` match in roadmap text ("v1.1" on line 31 -- "ship at GA, not v1.1").
