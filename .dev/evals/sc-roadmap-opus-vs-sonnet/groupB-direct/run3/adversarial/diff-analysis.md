# Diff Analysis — Variant 1 (Opus Default) vs Variant 2 (Sonnet Default)

## Metadata

- **Generated:** 2026-05-22T00:00:00Z
- **Variants compared:** 2 (opus-default, sonnet-default)
- **Variant 1:** 666 lines, 14 sections, 6 milestones
- **Variant 2:** 855 lines, 13 sections + 2 appendices, 6 milestones
- **Total differences found:** 47
- **Categories:** structural (S = 10), content (C = 12), contradictions (X = 6), unique (U = 12), shared assumptions (A = 7)
- **10% similarity check:** PASS — 47 differences across ~80 comparable items (58.75%) indicates substantial divergence; debate is warranted.

---

## Structural Differences (S-NNN)

| ID | Area | Variant 1 | Variant 2 | Severity |
|----|------|-----------|-----------|----------|
| S-001 | Milestone sequencing — Token vs Auth first | M2 = Token Lifecycle (library-only, before any endpoints). M3 = Core Auth Flows (endpoints consume token libs). | M2 = Core Authentication (login/register without JWT — session placeholder). M3 = Token Lifecycle (adds JWT retroactively to M2 endpoints). | **High** |
| S-002 | PasswordHasher placement | M3 (alongside auth endpoints) — hashing is part of the auth-flow milestone. | M1 (Data Foundation) — hashing is foundational infrastructure, built and benchmarked before any endpoint. | **Medium** |
| S-003 | Frontend component placement | M3 ships LoginPage, RegisterPage, AuthProvider alongside backend endpoints. M4 ships ProfilePage and reset UI. | M5 is a dedicated Frontend Integration milestone after all backend (M1-M4) is complete. No frontend code exists before M5. | **High** |
| S-004 | Compliance/observability milestone | M5 is a dedicated Compliance, Audit Logging & Observability milestone (1.5 sprints) with outbox emitter, Grafana dashboards, OTel, admin CLI. | Compliance is distributed: audit writer in M2 D2.4, audit query endpoint in M4 D4.5, SOC2/GDPR validation in M6. No dedicated observability milestone. | **Medium** |
| S-005 | GA rollout placement | M6 = Hardening + GA (rollout is the final milestone). | M5 = Frontend Integration + GA Rollout. M6 = Hardening + Compliance Validation (post-GA). Rollout happens *before* final hardening. | **High** |
| S-006 | Team composition | 4 BE, 2 FE, 0.5 SRE, 0.5 sec-reviewer (6.5 FTE, fixed). | 3-5 engineers (variable), plus frontend-team for M4. No dedicated SRE or security allocation. | **Medium** |
| S-007 | Section structure | 14 numbered sections including Internal Reference Index (S12), Detailed Edge-Case Catalog (S13), Notes on Variant (S14). | Unnumbered sections + Appendix A (Open Questions Resolution) + Appendix B (State-Mechanics Invariants). No edge-case catalog. | **Low** |
| S-008 | Deliverable ID scheme | D{milestone}.{sequence} with explicit "Traces To" column mapping every deliverable to FR/NFR/PRD IDs. | D{milestone}.{sequence} with "PRD/TDD Trace" and "Validation" columns per deliverable. Similar traceability, different column structure. | **Low** |
| S-009 | Dependency table granularity | Section 4 lists 13 dependency edges (From->To, Type=Hard/Soft, Rationale). Includes external deps (PRD approval, KMS, SendGrid, pen-test vendor). | "Cross-Milestone Dependencies" section with text graph + 8-row table linking specific deliverables. No Hard/Soft classification. | **Medium** |
| S-010 | Edge-case depth | Section 13 catalogs 30+ edge cases across 7 subsections (token rotation, session invalidation, password reset, rate limits, input validation, partial failures, concurrent state). | Appendix B defines 10 state invariants (INV-01 through INV-10) as P1 bugs if violated. Edge cases embedded within milestone risks rather than a dedicated catalog. | **Medium** |

---

## Content Differences (C-NNN)

| ID | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|----|-------|-------------------|-------------------|----------|
| C-001 | Token sequencing rationale | "Splitting JwtService/TokenManager out lets us security-review and benchmark the crypto-sensitive code in isolation, with property tests on rotation invariants, before HTTP concerns muddy the waters." | "Building tokens first would create unvalidated code that may need rework once login/registration requirements are fully understood during implementation." Directly opposing rationale. | **High** |
| C-002 | M2 login/register completeness | M3 endpoints are complete from the start — login returns full AuthToken pair. No retrofitting needed. | M2 login/register returns "session identifier placeholder"; M3 D3.5/D3.6 retroactively update these endpoints to return AuthToken. Retrofitting required. | **High** |
| C-003 | Shared contracts package | `@auth/contracts` npm package (v0.1.0) published to internal registry in M1, defining UserProfile, AuthToken, error envelope, and JSON-schema validators. Versioned from day one. | No shared contracts package. Interfaces are implicit in code. No explicit API contract versioning. | **Medium** |
| C-004 | API spec-first approach | OpenAPI 3.1 spec stub covering all 6 endpoints created in M1 (D1.4). Spectral lint enforced in CI. Contract tests generated from spec in M3. | No OpenAPI spec mentioned. API contracts are defined by TDD Section 8 and validated via integration tests. No spec-first workflow. | **Medium** |
| C-005 | Reset token storage medium | `password_reset_tokens` Postgres table with `used_at`, `expires_at`, `user_id`, single-use enforcement via `SELECT FOR UPDATE`. Durable, transactional. | Redis with SHA-256 hashed keys, `reset:` prefix, 1-hour TTL, atomic compare-and-delete via Lua script. Ephemeral, fast. | **High** |
| C-006 | Audit log delivery pattern | Outbox pattern: write audit event row in same DB transaction as state change, then async publisher drains to long-term store. At-least-once semantics guaranteed. | Direct synchronous write to `audit_log` table in the same request flow (M2 D2.4). No outbox pattern. No async drain. | **Medium** |
| C-007 | Email delivery architecture | BullMQ job queue for async delivery with 60-second SLA and 3 retry attempts. Separate Redis namespace (`mq:` prefix). | Retry logic within the SendGrid integration module (3 attempts, exponential backoff: 1s, 4s, 16s). No job queue. | **Medium** |
| C-008 | Redis eviction policy | `noeviction` on auth keyspace — tokens must never be silently dropped. | `allkeys-lru` — acceptable to lose tokens under memory pressure; users re-authenticate. Directly contradictory operational posture. | **High** |
| C-009 | Feature flag strategy | Single flag `auth.v1.enabled` for GA rollout + subsystem flags `auth.v1.lockout.enabled` and `auth.v1.reset.enabled` for surgical pause. | Two flags: `AUTH_NEW_LOGIN` (gates new login/register pages) and `AUTH_TOKEN_REFRESH` (gates refresh token flow). | **Low** |
| C-010 | Rollout staging | 1% -> 10% -> 50% -> 100% over 7 days, each step gated on error-rate < 0.5% and p95 < 200 ms. | Internal alpha (1 week, 0% traffic) -> Beta 10% (2 weeks) -> GA 100% (1 week). Total ~4 weeks. Rollback: p95 > 1000ms for 5 min, error > 5% for 2 min. | **Medium** |
| C-011 | Key management for JWT signing | KMS (AWS KMS or HashiCorp Vault) with ADR-002 decision record. Private key never leaves HSM. Local key cache with 5-min lifetime. | Filesystem path (Kubernetes secret mount). Quarterly manual rotation documented in runbook. No KMS/HSM. | **High** |
| C-012 | Password policy enforcement | >= 8 chars, >= 1 uppercase, >= 1 number, >= 1 special char. | >= 8 chars, >= 1 uppercase, >= 1 digit. No special-character requirement. V1 is stricter. | **Medium** |

---

## Contradictions (X-NNN)

| ID | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|----|-------------------|-------------------|-------------------|--------|
| X-001 | Should tokens be built before or after auth endpoints? | BEFORE — "Splitting them out lets us security-review and benchmark the crypto-sensitive code in isolation, before HTTP concerns muddy the waters." (Section 11) | AFTER — "tokens have no meaning without a use case. Building tokens first creates unvalidated code that may need rework." (Sequencing Rationale) | **High** — Determines whether M2 is a library milestone or an endpoint milestone. Affects security review timing, test strategy, and retrofitting risk. |
| X-002 | Should frontend be coupled with or separated from backend? | COUPLED — LoginPage, RegisterPage, AuthProvider ship in M3 alongside endpoints. No mock drift possible. | SEPARATED — Frontend is M5 after all backend is done. "Serial approach reduces coordination overhead and eliminates mock-drift risk entirely." (Sequencing Rationale) | **High** — Affects team allocation, testing strategy, and integration risk profile. V1 requires FE engineers from Sprint 5; V2 requires them only from Sprint 10. |
| X-003 | Redis eviction policy for auth tokens | `noeviction` — "eviction policy set to noeviction on the auth keyspace" (M1 Scope). Tokens must never be silently evicted. | `allkeys-lru` — "Set maxmemory-policy to allkeys-lru" (M3 Risks). Token loss is acceptable; users re-authenticate. | **High** — Directly contradictory operational posture. V1 treats token loss as unacceptable; V2 treats it as tolerable. Affects Redis sizing, monitoring, and failure-mode behavior. |
| X-004 | Reset token persistence strategy | PostgreSQL table with `password_reset_tokens` — durable, transactional, survives Redis loss. Checked via `SELECT FOR UPDATE`. | Redis with 1-hour TTL — ephemeral, fast, lost on Redis restart. Atomic via Lua compare-and-delete. | **High** — If Redis is lost (DR scenario), V2 loses all in-flight password resets. V1 retains them. V2's approach is faster but less durable. |
| X-005 | M2 endpoint completeness (V2 intra-variant) | N/A — V1 endpoints are complete when shipped. | M2 ships login/register returning "session identifier placeholder" (M2 Scope Out). M3 D3.5/D3.6 must retroactively update these to return AuthToken. This means M2 exit criteria validate endpoints that will be modified in M3. | **Medium** — M2 exit criteria (integration tests passing on login/register) are invalidated when M3 changes the response shape. Re-testing required. |
| X-006 | Audit log retention (V2 intra-variant + cross-variant) | Consistently 12-month retention with monthly partitioning throughout. | SOC2 mapping table says "90-day retention in PostgreSQL; extensible to 12 months via partitioning." M6 D6.2 exit criteria says "Confirm 12-month retention policy." These are contradictory within V2 — default is 90-day but target is 12-month. | **Medium** — SOC2 typically requires 12-month retention. V2's default 90-day may fail audit if the extension step is missed. V1 avoids this by committing to 12-month from the start. |

---

## Unique Contributions (U-NNN)

| ID | Variant | Contribution | Value |
|----|---------|-------------|-------|
| U-001 | V1 | `@auth/contracts` npm package with semantic versioning, JSON-schema validators, and internal registry publish. Enables contract-driven development across frontend and backend. | **High** |
| U-002 | V1 | OpenAPI 3.1 spec stub (D1.4) created in M1 before any implementation. Spectral lint in CI. Contract tests generated from spec. Spec-first workflow. | **High** |
| U-003 | V1 | STRIDE threat model (D1.6) produced in M1 and signed off by sec-reviewer. Security analysis before code exists. | **Medium** |
| U-004 | V1 | docker-compose dev environment with "5-minute first run" walkthrough (D1.7). Explicit developer experience goal. | **Medium** |
| U-005 | V1 | Detailed edge-case catalog (Section 13) covering 30+ scenarios across token rotation, session races, reset tokens, rate limits, malformed input, partial failures, and concurrent state. Each mapped to owner milestone and proof artifact. | **High** |
| U-006 | V1 | Pepper layer on top of bcrypt: HMAC-SHA256 with KMS-managed pepper key (M3 D3.5). Defense-in-depth beyond standard bcrypt. | **Medium** |
| U-007 | V1 | BullMQ job queue for async email delivery with dedicated Redis namespace (`mq:` prefix). Separates email delivery from request path. | **Low** |
| U-008 | V2 | Infrastructure cost estimate: ~$450/month production (3 K8s pods $150, PostgreSQL $200, Redis $100). Enables budget planning. | **Medium** |
| U-009 | V2 | State-mechanics invariants (Appendix B): INV-01 through INV-10. Each invariant declared as a P1 bug if violated, with enforcement location and validation method. Testable system properties. | **High** |
| U-010 | V2 | GDPR right-to-erasure endpoint: DELETE /auth/me in M6 D6.3. Removes all PII within 30 days. V1 has no deletion endpoint. | **High** |
| U-011 | V2 | Open questions resolution tracking (Appendix A): 6 PRD/TDD open questions resolved or deferred with owner, target date, and status. Traceable decision log. | **Medium** |
| U-012 | V2 | Admin API endpoint (GET /admin/auth-events) with pagination, role-based access, and composite indexes. V1 uses CLI tool instead. REST API is more accessible than CLI for dashboard integration. | **Medium** |

---

## Shared Assumptions (A-NNN)

| ID | Assumption | Source Agreement | Impact | Status |
|----|-----------|-----------------|--------|--------|
| A-001 | Sprint length = 2 weeks, total 12 sprints (~24 weeks / ~6 months). Team holds for full duration. | V1: explicit (Section 2, Assumption 1). V2: explicit (Roadmap Overview). Both agree on 12 sprints. | Sprint-level planning and burndown tracking depend on this. Vacations/onboarding loss: V1 bakes in 15% buffer; V2 does not account for attrition. | STATED |
| A-002 | PostgreSQL 15+ and Redis 7+ are provisioned by platform-team before development starts. | V1: Assumption 2 (with TLS, encryption-at-rest, automated backups). V2: Assumptions 2-3 (Kubernetes secrets for credentials). Both assume external provisioning. | If infra is delayed, M1 entry is blocked. V1 explicitly escalates; V2 suggests Docker Compose as local fallback. | STATED |
| A-003 | Greenfield deployment — no existing user data to migrate. | V1: implicit (no migration tasks). V2: explicit Assumption 7 ("No legacy auth migration. There is no existing user data to migrate."). | Eliminates migration complexity. Both variants would need significant rework if this is invalidated (corporate acquisition, user import requirement). | UNSTATED in V1, STATED in V2 |
| A-004 | Single-region deployment for v1.0. Cross-region/active-active is post-GA. | V1: explicit in Out of Scope (M6). V2: explicit Assumption 10. Both agree. | Capacity planning, DR strategy, and token validation all assume single-region latency. Multi-region would require token validation cache invalidation across regions. | STATED |
| A-005 | SOC2 Type II audit scheduled for Q3 2026 drives compliance timeline. Audit logging must be in place before audit window. | V1: explicit in Executive Summary and Assumption 12. V2: implicit in M6 scope and SOC2 mapping. | Compliance is a hard deadline. If the roadmap slips past Q2, audit evidence collection may be insufficient. V1 calls this out explicitly; V2 assumes it implicitly. | STATED in V1, UNSTATED in V2 |
| A-006 | NTP clock synchronization available with < 1s drift across all service instances. | V1: explicit (Assumption about clock skew, M2 risk mitigation via NTP monitoring). V2: explicit Assumption 13 ("< 1 second drift"). Both require this for JWT 5s clock-skew tolerance. | If clocks drift > 5s, JWT validation breaks. Neither variant includes a clock-drift detection mechanism beyond NTP. | STATED |
| A-007 | Penetration testing vendor is available with <= 4 weeks lead time. | V1: explicit Assumption 8. V2: implicit in M6 entry criteria ("External penetration testing firm engaged and scheduled"). Both assume vendor availability. | If pen-test vendor is unavailable or delayed, M6 exit is blocked. Neither has a fallback (e.g., internal security team scan as interim measure). | STATED in V1, UNSTATED in V2 |

---

## Summary

### Counts

| Category | Count |
|----------|-------|
| Structural (S) | 10 |
| Content (C) | 12 |
| Contradictions (X) | 6 |
| Unique (U) | 12 |
| Shared Assumptions (A) | 7 |
| **Total** | **47** |

### Highest-Severity Items (Severity = High)

- **S-001:** Token-first vs Auth-first sequencing — fundamentally different build order
- **S-003:** Frontend coupled with backend vs separated into own milestone
- **S-005:** GA rollout before hardening (V2) vs hardening before rollout (V1)
- **C-001:** Directly opposing rationale for token sequencing
- **C-002:** V2 requires retrofitting M2 endpoints in M3; V1 endpoints are complete
- **C-005:** Reset tokens in Postgres (V1, durable) vs Redis (V2, ephemeral)
- **C-008:** `noeviction` (V1) vs `allkeys-lru` (V2) Redis policy — contradictory
- **C-011:** KMS/HSM (V1) vs filesystem path/K8s secrets (V2) for signing keys
- **X-001:** Tokens before auth vs auth before tokens — opposing rationale
- **X-002:** Frontend coupling vs separation — opposing rationale
- **X-003:** Redis eviction policy — noeviction vs allkeys-lru
- **X-004:** Reset token persistence — Postgres vs Redis
- **U-005:** V1 edge-case catalog (30+ scenarios) — no equivalent in V2
- **U-009:** V2 state-mechanics invariants (10 P1-class invariants) — no equivalent in V1
- **U-010:** V2 GDPR right-to-erasure endpoint — absent from V1

### Key Judgment Axes for Debate

1. **Build order (X-001):** Is isolating crypto code for early security review (V1) more valuable than building endpoints first and validating requirements (V2)?
2. **Frontend integration timing (X-002):** Does coupled frontend/backend reduce integration risk (V1) or does separation reduce coordination overhead (V2)?
3. **Data durability posture (X-003, X-004, C-008):** Is the team optimizing for zero token loss (V1, noeviction + Postgres reset tokens) or accepting graceful degradation (V2, allkeys-lru + Redis reset tokens)?
4. **Key management maturity (C-011):** Does v1.0 warrant KMS/HSM (V1) or is filesystem path + K8s secrets sufficient for initial GA (V2)?
5. **Spec-first vs code-first (C-003, C-004):** Does the OpenAPI spec + contracts package overhead (V1) pay off in reduced integration errors, or is it premature ceremony for a 6-person team (V2)?
