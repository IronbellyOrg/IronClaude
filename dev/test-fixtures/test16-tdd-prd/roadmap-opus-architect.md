---
spec_source: "test-tdd-user-auth.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
debate_rounds: none
generated: "2026-04-19"
generator: "single"
total_milestones: 6
total_task_rows: 96
risk_count: 7
open_questions: 9
domain_distribution:
  frontend: 12
  backend: 38
  security: 22
  performance: 8
  documentation: 5
consulting_personas: [architect, security, backend, frontend, qa, devops]
milestone_count: 6
milestone_index:
  - id: M1
    title: "Foundation and Infrastructure"
    type: FEATURE
    priority: P0
    dependencies: []
    deliverable_count: 14
    risk_level: Medium
  - id: M2
    title: "Data Models and Cryptographic Primitives"
    type: SECURITY
    priority: P0
    dependencies: [M1]
    deliverable_count: 14
    risk_level: High
  - id: M3
    title: "Authentication Backend Services and APIs"
    type: FEATURE
    priority: P0
    dependencies: [M2]
    deliverable_count: 26
    risk_level: High
  - id: M4
    title: "Frontend Authentication Surfaces"
    type: FEATURE
    priority: P0
    dependencies: [M3]
    deliverable_count: 11
    risk_level: Medium
  - id: M5
    title: "Testing, Observability and Compliance"
    type: TEST
    priority: P0
    dependencies: [M3, M4]
    deliverable_count: 21
    risk_level: Medium
  - id: M6
    title: "Migration, Rollout and GA"
    type: MIGRATION
    priority: P0
    dependencies: [M5]
    deliverable_count: 10
    risk_level: High
total_deliverables: 96
total_risks: 7
estimated_milestones: 6
validation_score: 0.88
validation_status: PASS
---

# User Authentication Service — Project Roadmap

## Executive Summary

Deliver a production-grade, SOC2-aligned User Authentication Service (registration, login, logout, token lifecycle, profile, self-service reset) that unblocks the Q2–Q3 2026 personalization roadmap and meets the Q3 2026 SOC2 Type II audit deadline. Stateless JWT (RS256, 15-min access / 7-day refresh) + bcrypt (cost 12) + Redis-backed refresh records on Node.js 20 LTS / PostgreSQL 15 / Redis 7, fronted by an API Gateway enforcing rate limits and CORS. Architecture is phased across six milestones: foundation, cryptographic primitives, backend services, frontend surfaces, test/observability/compliance, and a feature-flag-gated migration to GA.

**Business Impact:** Unblocks ~$2.4M projected annual revenue tied to personalized features; satisfies Q3 2026 SOC2 Type II audit; reduces 30% QoQ growth in access-related support tickets; enables Jordan-persona audit workflows and Sam-persona programmatic integrations.

**Complexity:** HIGH (0.72) — multi-component backend (AuthService, TokenManager, JwtService, PasswordHasher) + three frontend surfaces + compliance-bound (SOC2, GDPR, NIST SP 800-63B) + phased rollout with two feature flags and parallel-run migration.

**Critical path:** M1 Foundation → M2 Data + Crypto (DM-001, DM-002, PasswordHasher, JwtService) → M3 AuthService + TokenManager + API-001..006 → M4 Frontend surfaces → M5 Test/Observability/Compliance gate → M6 Phased rollout (Phase 1 alpha → Phase 2 10% beta → Phase 3 GA).

**Key architectural decisions:**

- Stateless JWT (RS256, 2048-bit RSA, quarterly rotation) for access tokens; Redis-backed opaque refresh tokens for server-side revocation — chosen over sticky sessions for horizontal scale and over HS256 for key-rotation safety.
- bcrypt cost factor 12 via PasswordHasher — aligns with NIST SP 800-63B adaptive-hashing requirement; benchmarked ~300ms/hash balances attacker cost against NFR-PERF-001 200ms p95 login target.
- API Gateway enforces rate limiting (10/min/IP login, 5/min/IP register) and CORS BEFORE requests reach AuthService — keeps brute-force (R-002) mitigation out of application code path.
- AuthProvider holds accessToken in memory only; refreshToken in HttpOnly cookie — mitigates R-001 (XSS token theft) without requiring server-side session.
- Two-flag rollout (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) with parallel-run legacy auth for idempotent rollback — bounded blast radius for R-003 (migration data loss).

**Open risks requiring resolution before M1:**

- OQ-007 audit-log retention conflict (TDD 90 days vs PRD SOC2 12 months) must be resolved with Security before schema work begins in M1 — drives storage sizing and archival design.
- OQ-005 account-lockout policy (5/15-min) must be ratified by Security before M3 API-001 implementation; premature lock of legitimate users is a P1 UX risk.
- OQ-008 logout / refresh-token revocation endpoint scope — if added to v1.0, requires API-007 row in M3; decision needed before M3 sprint planning.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation and Infrastructure|FEATURE|P0|2w|none|14|Medium|
|M2|Data Models and Cryptographic Primitives|SECURITY|P0|2w|M1|14|High|
|M3|Authentication Backend Services and APIs|FEATURE|P0|3w|M2|26|High|
|M4|Frontend Authentication Surfaces|FEATURE|P0|2w|M3|11|Medium|
|M5|Testing, Observability and Compliance|TEST|P0|2w|M3,M4|21|Medium|
|M6|Migration, Rollout and GA|MIGRATION|P0|3w|M5|10|High|

## Dependency Graph

```
M1 (Foundation) → M2 (Data + Crypto) → M3 (Backend + APIs) → M4 (Frontend) → M5 (Test + Ops + Compliance) → M6 (Migration + GA)

Detailed intra-milestone dependencies:
  M1: [INFRA-NODE → INFRA-PG → INFRA-REDIS → INFRA-GW] ∥ [CI, SECRETS, OBS-BOOTSTRAP]
  M2: [DM-001, DM-002] ← schema-migrations ; [COMP-008 PasswordHasher, COMP-007 JwtService] ← [NFR-SEC-001, NFR-SEC-002, key-rotation]
  M3: [COMP-006 TokenManager] → [COMP-005 AuthService] → [API-001..006] ; FR-AUTH-001..005 track API rows ; NFR-COMP-001/003/004 gate registration
  M4: [COMP-004 AuthProvider] → [COMP-001 LoginPage, COMP-002 RegisterPage, COMP-003 ProfilePage]
  M5: [TEST-001..003 Unit] → [TEST-004..005 Integration] → [TEST-006 E2E] ; [OPS-007..010 Observability] ← NFR-PERF-001/002, NFR-REL-001, NFR-COMP-002
  M6: [MIG-004, MIG-005 flags] → [MIG-001 Alpha] → [MIG-002 10% Beta] → [MIG-003 GA] ; [MIG-006, MIG-007 rollback] parallel gates

External dependency injection:
  SEC-POLICY-001 → M2 crypto config ; INFRA-DB-001 → M1 PG provisioning ; SendGrid → M3 FR-AUTH-005
```

## M1: Foundation and Infrastructure

**Objective:** Provision runtime, database, cache, gateway, CI/CD, observability bootstrap, and project scaffolding required by all downstream milestones. | **Duration:** Weeks 1–2 (2 weeks) | **Entry:** PRD + TDD signed off; SEC-POLICY-001 retention conflict (OQ-007) resolved; INFRA-DB-001 PG cluster provisioned. | **Exit:** Health endpoint returns 200 in CI and staging; Node 20 service skeleton, PG 15 pool, Redis 7 client, API Gateway, structured logger, metrics scaffolding, secret manager all wired and integration-tested.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|INFRA-NODE-001|Node.js 20 LTS service skeleton|Bootstrap TypeScript service repo with Node 20 LTS, ts-jest, ESLint, Prettier, structured logger placeholder.|build-system|—|node>=20.x; tsc compiles; lint clean; test runner green on empty suite|S|P0|
|2|INFRA-PG-001|PostgreSQL 15 cluster integration|Provision PG 15 (INFRA-DB-001) connection pool (pg-pool, size 100) with migrations runner; verify schema namespace owned by service role.|persistence|INFRA-NODE-001, INFRA-DB-001|pg-pool size=100; reconnection handles transient drops; migration tool idempotent; CI testcontainer healthy|M|P0|
|3|INFRA-REDIS-001|Redis 7 client integration|Standalone Redis 7 client (RESP) with TLS, connection pool, fail-closed semantics for refresh-token reads.|cache|INFRA-NODE-001|client connects; PING<5ms; TLS verified; connection pool=20; fail-closed on outage|S|P0|
|4|INFRA-GW-001|API Gateway provisioning|Stand up API Gateway in front of AuthService; path prefix `/v1/auth/*`; CORS allowlist for known frontend origins; TLS 1.3 termination.|gateway|INFRA-NODE-001|TLS 1.3 only; CORS restricted; routes /v1/auth/* forwarded; latency overhead<10ms p95|M|P0|
|5|INFRA-RATE-001|Gateway rate-limit policy framework|Configure per-endpoint rate-limit primitives at the gateway (sliding window) for use by API-001 (10/min/IP), API-002 (5/min/IP), API-003 (60/min/user), API-004 (30/min/user).|gateway|INFRA-GW-001|policy engine deployed; per-route limits configurable via IaC; 429 returned on excess; metrics exported|M|P0|
|6|INFRA-CI-001|CI/CD pipeline|Build, test, lint, typecheck, security-scan jobs; container image build; staging deploy on green main.|ci|INFRA-NODE-001|PR gate: lint+test+type pass; image SBOM generated; auto-deploy staging on main|M|P0|
|7|INFRA-SECRETS-001|Secret manager wiring|Mount RSA private key, DB credentials, Redis credentials, SendGrid API key from secret manager; deny plaintext env vars for sensitive material.|security|INFRA-NODE-001|secrets loaded at boot; missing secret = startup fail; rotation reload verified|S|P0|
|8|INFRA-LOG-001|Structured logging bootstrap|Pino-based JSON logger; mandatory request_id correlation; field denylist (password, accessToken, refreshToken, resetToken).|observability|INFRA-NODE-001|log fields JSON; sensitive fields redacted at sink; request_id propagated through OTel context|S|P0|
|9|INFRA-METRICS-001|Prometheus metrics scaffolding|Expose `/metrics` endpoint; register histograms/counters that OPS-008 will populate.|observability|INFRA-NODE-001|/metrics 200; default process metrics present; counter registry idempotent|S|P1|
|10|INFRA-TRACE-001|OpenTelemetry tracing bootstrap|OTel SDK + OTLP exporter; auto-instrument http/pg/ioredis; span attributes redacted.|observability|INFRA-NODE-001, INFRA-PG-001, INFRA-REDIS-001|spans emitted to collector; no PII in attributes; sampling 10% staging, 1% prod|M|P1|
|11|INFRA-HEALTH-001|Health and readiness endpoints|Implement `/healthz` (process liveness) and `/readyz` (PG + Redis reachability) for HPA + uptime monitoring (NFR-REL-001 baseline).|observability|INFRA-PG-001, INFRA-REDIS-001|/healthz<10ms; /readyz fails when PG or Redis unreachable; K8s probes wired|S|P0|
|12|INFRA-SCHEMA-001|Schema migration runner|Pin migration tool (e.g., node-pg-migrate); enforce forward-only with rollback scripts; CI gate prevents drift.|persistence|INFRA-PG-001|up/down templates; migration registered in CI; drift detection job green|S|P0|
|13|INFRA-ENV-001|Environment configuration matrix|Local (Docker Compose PG+Redis+gateway), CI (testcontainers), Staging, Prod env profiles with strict schema validation at boot.|build-system|INFRA-NODE-001, INFRA-SECRETS-001|invalid config = boot fail; env matrix documented; staging≠prod isolation enforced|S|P0|
|14|INFRA-DOC-001|Architecture decision record (ADR) seed|Capture stack/runtime choices (Node 20 LTS, PG 15, Redis 7, RS256, bcrypt 12) as ADR-0001..0005 in repo `/docs/adr/`.|documentation|—|five ADRs committed; each cites TDD section; PR template links ADRs|S|P2|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|API Gateway route table|Dispatch table|IaC at INFRA-GW-001|M1|All M3 API-001..006 endpoints|
|Per-endpoint rate-limit registry|Registry|IaC at INFRA-RATE-001|M1|API-001 (10/min/IP), API-002 (5/min/IP), API-003 (60/min/user), API-004 (30/min/user)|
|Secret manager mount map|DI binding|INFRA-SECRETS-001|M1|JwtService key, PG creds, Redis creds, SendGrid key|
|OTel instrumentation chain|Middleware chain|INFRA-TRACE-001|M1|All HTTP handlers in M3, PG queries, Redis ops|
|Logger field denylist|Strategy|INFRA-LOG-001|M1|All log call-sites in M3/M4|

### Milestone Dependencies — M1

- INFRA-DB-001 (PostgreSQL provisioning, external) — required before INFRA-PG-001.
- SEC-POLICY-001 (password/token policy authority) — required as input for INFRA-SECRETS-001 secret class definitions.
- OQ-007 audit-log retention decision — must precede INFRA-SCHEMA-001 (informs partition strategy).

### Open Questions — M1

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-007|Audit-log retention: TDD says 90 days, PRD SOC2 says 12 months. Adopt 12 months?|Drives PG storage sizing, partitioning, archival tier; gate on SOC2 audit pass|Security + Product|2026-04-26|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|INFRA-DB-001 provisioning slip blocks INFRA-PG-001|Medium|Medium|2-day shift on M1; cascades to M2|Pre-engage platform-team week 0; provisional dev DB for INFRA-PG-001 hardening in parallel|platform-team|
|2|Gateway rate-limit policy mis-scoped delays brute-force defense|Medium|Low|R-002 mitigation incomplete at M3 entry|Define rate-limit IaC contract in M1 INFRA-RATE-001; integration test in CI|auth-team|
|3|Secret manager outage at boot blocks all environments|High|Low|Service refuses to start|INFRA-SECRETS-001 caches last-good secret bundle locally with TTL; documented runbook|platform-team|

## M2: Data Models and Cryptographic Primitives

**Objective:** Implement persistent data models (DM-001 UserProfile, DM-002 AuthToken), cryptographic components (PasswordHasher, JwtService), and security policies (bcrypt cost 12, RS256 2048-bit, key rotation, GDPR minimization) that AuthService + TokenManager will compose in M3. | **Duration:** Weeks 3–4 (2 weeks) | **Entry:** M1 exit criteria met; RSA keypair generated in secret manager; Redis + PG reachable from CI. | **Exit:** DM-001/DM-002 migrations applied; PasswordHasher + JwtService unit-tested; NFR-SEC-001/NFR-SEC-002 invariants asserted by tests; key rotation runbook verified.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|DM-001|`UserProfile` persistent model|Define PG table `user_profile` and TypeScript interface backing FR-AUTH-002/004.|persistence|INFRA-PG-001, INFRA-SCHEMA-001|id:UUIDv4-PK-NOTNULL; email:string-UNIQUE-NOTNULL-indexed-lowercase; displayName:string-NOTNULL-2-100chars; createdAt:ISO8601-NOTNULL-DEFAULTnow(); updatedAt:ISO8601-NOTNULL-auto-update; lastLoginAt:ISO8601-NULLABLE; roles:string[]-NOTNULL-DEFAULT-["user"]|M|P0|
|2|DM-002|`AuthToken` data model|Define TS interface + Redis record layout for refresh tokens; accessToken remains stateless JWT.|persistence|INFRA-REDIS-001|accessToken:JWT-string-NOTNULL-RS256; refreshToken:string-NOTNULL-unique-opaque-Redis-backed-7dayTTL; expiresIn:number-NOTNULL-always=900; tokenType:string-NOTNULL-always="Bearer"-OAuth2-compat|M|P0|
|3|DM-001-MIG|UserProfile migration script|Forward migration creating `user_profile` table with constraints + indexes; matching down script.|persistence|DM-001|unique index on lower(email); btree index on createdAt; check constraint on displayName length; migration idempotent|S|P0|
|4|DM-AUDIT-001|Audit log table schema|PG table for SOC2 audit events (user_id, timestamp, ip, event_type, outcome); partitioned by month for retention tiering.|persistence|DM-001, OQ-007|event_id:UUID-PK; user_id:FK-UserProfile; timestamp:timestamptz-indexed; ip:inet; event_type:enum; outcome:enum; retention policy = 12 months (pending OQ-007)|M|P0|
|5|COMP-008|`PasswordHasher` component|Backend bcrypt wrapper exposing `hash(plain)` and `verify(plain, hash)`; cost factor 12; benchmarked ~300ms/hash.|security|INFRA-NODE-001|hash() uses bcryptjs cost=12; verify() returns boolean without timing-leak; hash output ~60 chars; benchmark<500ms per NFR target|M|P0|
|6|COMP-007|`JwtService` component|RS256 sign/verify with 2048-bit RSA keys; 5-second clock-skew tolerance; sign/verify latency <5ms.|security|INFRA-NODE-001, INFRA-SECRETS-001|sign() uses RS256 + private key from secret mgr; verify() rejects HS*; clockTolerance=5s; latency<5ms p95|M|P0|
|7|NFR-SEC-001|Bcrypt cost-factor policy test|Unit test asserts PasswordHasher always calls bcrypt with cost=12.|security|COMP-008|test inspects hash prefix `$2b$12$`; fails if cost drifts; gating CI check|S|P0|
|8|NFR-SEC-002|Token signing policy test|Configuration validation test asserts JwtService rejects non-RS256 algorithms and keys <2048 bits.|security|COMP-007|test loads 2048-bit key OK; 1024-bit rejected; HS256 header rejected on verify|S|P0|
|9|CRYPTO-KEY-ROT|Quarterly RSA key rotation procedure|Dual-key verify window; generate new key, publish JWKS-like mechanism, retire old key after 15 min max-TTL window.|security|COMP-007, INFRA-SECRETS-001|rotate playbook documented; verify works for both keys during overlap; rotation event emits audit log|M|P0|
|10|SEC-POLICY-PWD|Password strength policy module|Enforce NIST SP 800-63B checks (min 8 chars, mix rules compliant with TDD FR-AUTH-002 ACs) invoked before PasswordHasher.hash().|security|COMP-008|reject <8 chars; require uppercase + number; API-002 returns 400 on fail; unit tests cover edge cases|S|P0|
|11|SEC-EMAIL-NORM|Email normalization helper|Lowercase + trim email before persistence/lookup; prevents UNIQUE collisions and enumeration through casing tricks.|persistence|DM-001|input "Alice@Example.COM" stored as "alice@example.com"; lookup normalizes identically|S|P0|
|12|NFR-COMP-003|NIST SP 800-63B adaptive hashing compliance|Control verifying plaintext password never persists or logs; enforced via PasswordHasher boundary + logger denylist.|compliance|COMP-008, INFRA-LOG-001|static grep gate rejects log("password"); runtime assert at boundary; CI check|S|P0|
|13|NFR-COMP-004|GDPR data minimization inventory|Verify UserProfile only collects email, password hash, displayName; document as data-inventory artifact for compliance.|compliance|DM-001|data inventory committed; any new PII column blocked by schema-lint CI; signed off by DPO|S|P0|
|14|COMP-REPO-USER|`UserRepo` data-access module|Typed repository wrapping `user_profile` CRUD used by AuthService; encapsulates normalization + transactions.|persistence|DM-001, DM-001-MIG, SEC-EMAIL-NORM|findByEmail normalizes; insert handles UNIQUE violation as domain error; update returns new updatedAt; >95% unit coverage|M|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Bcrypt cost constant|Config injection|COMP-008|M2|AuthService register/login flows in M3|
|JWKS-style key map|Registry|CRYPTO-KEY-ROT|M2|JwtService verify() during overlap window|
|Password policy validator|Strategy|SEC-POLICY-PWD|M2|API-002 (register), API-006 (reset-confirm) in M3|
|Email normalizer|Strategy|SEC-EMAIL-NORM|M2|UserRepo lookups, API-001 login, API-002 register, API-005 reset-request|

### Milestone Dependencies — M2

- SEC-POLICY-001 governance — crypto choices (bcrypt 12, RS256 2048) must be ratified; ADR-0002 links here.
- OQ-007 retention decision — blocks DM-AUDIT-001 partitioning strategy.

### Open Questions — M2

|#|ID|Question|Impact|Owner|Target|
|---|---|---|---|---|---|
|1|OQ-002|Maximum allowed `UserProfile.roles` array length?|Sets validation cap; avoids unbounded JSON and Redis key growth in M3|auth-team|2026-05-03|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Bcrypt cost-12 exceeds NFR-PERF-001 200ms p95 login budget|High|Medium|Miss performance SLO at M5 validation|Budget ~300ms for hash, reserve <100ms for remaining login path; tune PG pool + JwtService to compensate; load test in M5|backend-team|
|2|RSA key leak via secret manager misconfig|Critical|Low|Global token compromise|Least-privilege IAM on secret; audit on read; enable KMS-backed envelope encryption|security|
|3|Migration drift between local/CI/staging schemas|Medium|Medium|Integration test false positives in M3|INFRA-SCHEMA-001 drift-detection job gates PR; testcontainers mirror migrations exactly|backend-team|



