---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 5
interleave_ratio: 1:2
major_issue_policy: stop-and-fix
spec_source: test-tdd-user-auth.md
generated: "2026-04-20T22:44:30.720802+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — User Authentication Service

## 1. Validation Milestone Mapping

**V# milestones run in parallel to work milestones (continuous-parallel)**; each V milestone is a hard gate that must complete before the paired work milestone's exit.

|V#|Paired Work|Runs During|Focus|Exit Criteria|
|---|---|---|---|---|
|V1|M1 + M2|Weeks 1–4 (2026-03-31 → 2026-04-28)|Foundation + Core Auth validation: schema correctness, bcrypt/NIST compliance, login/register contracts, enumeration safety, lockout, audit emission|All unit + integration tests for TEST-001/002/004 pass; NFR-SEC-001 (cost=12) + NFR-COMPLIANCE-003 (NIST SP 800-63B) + NFR-COMPLIANCE-002 (GDPR consent) + NFR-COMPLIANCE-004 (minimization) signed off; enumeration parity byte-equal; account lockout integration test passes; audit rows emitted for every FR-AUTH-001/002 path|
|V2|M3 + M4|Weeks 5–8 (2026-04-29 → 2026-05-26)|Token lifecycle + session + reset + logout + frontend + observability + compliance + pentest|TEST-003/005/006 pass; NFR-SEC-002 (RS256 2048-bit) verified; reset single-use + 1h TTL verified; logout revocation verified; NFR-PERF-001 (p95<200ms) + NFR-PERF-002 (500 concurrent) pass; SEC-PENTEST-001 Critical/High remediated; SOC2 12-month partition probe passes; funnel telemetry (SUCC-METRIC-001..006) green|
|V3|M5|Weeks 9–10 (2026-05-27 → 2026-06-09)|Phased rollout validation, automated rollback triggers, capacity, on-call, legacy deprecation|Smoke suite green after MIG-001/002/003; OPS-ROLLBACK-T1..T4 dry-runs verified in staging with no false-positive storm; OPS-AUDIT-QA sign-off; 99.9% uptime sustained 7 days post-GA (OPS-RPC-001); flag removals (MIG-004-CLEANUP) non-regressing|

## 2. Test Categories

|Category|Coverage Target|Tools|Scope|
|---|---|---|---|
|Unit|80% (TDD §15.1)|Jest + ts-jest|`AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, policy/consent validators, envelope shape, clock-skew, reset TTL|
|Integration|15%|Supertest + testcontainers (real PostgreSQL 15 + Redis 7)|API request/response cycles for all 7 endpoints, DB persistence, Redis TTL, SendGrid stubbed via interface|
|E2E|5%|Playwright (staging)|Full user journeys incl. register→auto-login chain, reset-request→email→reset-confirm, shared-device logout, silent refresh|
|Contract|All 4xx/5xx paths|Supertest-based envelope matcher|COMP-ENVELOPE-001 asserts `{error:{code,message,status}}` across API-001..007|
|Security|Per-release|Pentest vendor (SEC-PENTEST-001) + in-CI static checks + COMP-LOGHYG-001/002|XSS surface on `AuthProvider`, alg=none bypass, RS256 key length, enumeration, reset replay|
|Performance|Per-release|k6 + APM histograms|NFR-PERF-001 (all 7 endpoints p95<200ms), NFR-PERF-002 (500 concurrent 10 min), hash-time benchmark|
|Compliance|Per-milestone|OPS-AUDIT-QA harness + partition probe + GDPR export test|SOC2 audit coverage (every FR path + logout emits exactly 1 row); 12-month retention; consent recording; GDPR Article 15 export (OPS-GDPR-EXPORT)|
|Operational|V3|Smoke suite (OPS-SMOKE-001) + chaos drills|Rollback triggers T1..T4 dry-runs; runbook OPS-001/002 walkthroughs; on-call paging|

## 3. Test-Implementation Interleaving Strategy

**Ratio: 1:2 (MEDIUM complexity → TDD §1 / roadmap complexity_score=0.65).** Justification: cryptographic correctness (bcrypt cost, RS256 key length, enumeration timing) and SOC2/GDPR/NIST compliance require validation cadence tighter than LOW (1:3), but bounded functional scope (5 FR, 7 endpoints, 2 data models) does not warrant HIGH (1:1). Paired cadence V1↔(M1+M2), V2↔(M3+M4), V3↔M5 keeps a validation gate between every pair of work milestones, catching regressions before the next pair layers on dependent code (token lifecycle on top of password storage; rollout on top of observability).

**Continuous-parallel mechanics:**
- Each work milestone enters its TEST-### rows (TEST-001..006 from TDD §15.2) in the same sprint they implement the target FR, not retroactively.
- V# milestones run continuously in parallel with their paired work milestone(s). The gate closes only when both the work milestone's exit criteria **and** the V# exit criteria are met.
- CI benchmark (SUCC-METRIC-006, NFR-SEC-001, NFR-SEC-002 config probes) blocks merge on regression — not deferred to V#.

## 4. Risk-Based Test Prioritization

|Rank|Risk|Severity|Priority Tests|Milestone|
|---|---|---|---|---|
|1|R-PRD-002 Security breach from implementation flaws|Critical|SEC-PENTEST-001, NFR-SEC-001, NFR-SEC-002, COMP-LOGHYG-001/002, alg=none rejection unit, RS256 key length probe|V1 (crypto readiness), V2 (full pentest)|
|2|R-001 Token theft via XSS|High|HttpOnly+Secure+SameSite=Strict cookie assertion; accessToken-not-in-localStorage inspection; CSP header test; pentest XSS surface|V2|
|3|R-003 Data loss during migration|High|MIG-DB-001 idempotency test (apply twice); backup-restore drill; OPS-ROLLBACK-T4 data-integrity probe dry-run|V3|
|4|R-PRD-003 SOC2 audit logging gaps|High|OPS-AUDIT-QA (1 row per FR path + logout); 12-month partition-expiry probe; admin CLI query test (JTBD-GAP-001)|V1 (emission), V2 (query + retention)|
|5|R-002 Brute-force|Medium-High|COMP-LOCKOUT-001 threshold/reset/expiry integration test; API-001-RATE k6 burst; NFR-ENUM-001 byte-equality|V1|
|6|R-PENTEST-001 Findings block GA|High|Vendor weekly interim reports; Critical/High SLA <5 business days; buffer in M4|V2|
|7|R-PRD-004 Email delivery failure|Medium|SendGrid delivery mock + 3-retry test; >5% failure-rate alert dry-run; fallback channel runbook walkthrough|V2|
|8|R-RESET-ENUM Reset UI enumeration|Medium|NFR-ENUM-002 byte-equality extended to COMP-016 rendered content; pentest reset surface|V2|
|9|R-OBS-001 Instrumentation regresses p95|Medium|Before/after NFR-PERF-001 benchmark; trace sampling audit|V2|
|10|R-ROLLBACK-FP False-positive rollback|Medium|T1..T4 staged dry-runs; debounce-window assertion tests|V3|
|11|R-REFRESH-TRANSPORT Ambiguous contract|Medium|Assert cookie-only in COMP-HTTPONLY-001 contract test; fail build if request-body path re-appears without sign-off|V1 (pre-M3 gate)|
|12|R-OQ-PRD-002 Redis sizing|Medium|OPS-006 headroom assertion 2× baseline until OQ closed; memory-utilization alert dry-run|V3|
|13|R-LEGACY-DEP Consumer breakage|Medium|Deprecation/Sunset header contract test; consumer notification audit|V3|
|14|R-PRD-001 Low registration adoption|High (business)|SUCC-METRIC-001 funnel dashboard live pre-GA; usability test on RegisterPage|V2|

## 5. Acceptance Criteria per Milestone

**M1: Foundation** | Exit: DM-001 + DM-002 schemas applied; MIG-DB-001 idempotent (re-apply clean); COMP-AUDIT-001 partitioned monthly, indexed, retention=12mo; INFRA-001/002/003 reachable from staging; INFRA-006 buckets registered for all 7 endpoints incl. reset-request=5/min/IP (OQ-RESET-RL-001) and logout=30/min/user; feature flags `AUTH_NEW_LOGIN` + `AUTH_TOKEN_REFRESH` registered default-OFF; COMP-POLICY-001 unit test asserts each NIST rule; COMP-CONSENT-001 unit test covers accept + reject paths; COMP-LOGHYG-001 scrubs password/accessToken/refreshToken/resetToken.

**M2: Core Authentication** | Exit: TEST-001, TEST-002, TEST-004 pass; NFR-SEC-001 (cost=12) parses $2b$ hash and fails build on mismatch; COMP-LOCKOUT-001 integration test covers threshold (5 fails), window reset on success, 15-min expiry, 423 Locked; NFR-ENUM-001 byte-equality between unknown-email and wrong-password responses; API-001-RATE + API-002-RATE k6 bursts return 429 at 11th/6th request; OPS-AUDIT-LOGIN + OPS-AUDIT-REG emit exactly 1 row per attempt with correct outcome enum; NFR-COMPLIANCE-003/004 compliance-lead sign-off recorded; `AUTH_NEW_LOGIN` remains gated to internal tenants.

**M3: Token Management & Session** | Exit: TEST-003, TEST-005 pass; NFR-SEC-002 config probe asserts RS256 + 2048-bit modulus; COMP-JWT-001 rejects alg=none and alg≠RS256; COMP-CLOCKSKEW-001 unit (exp=now-3s verifies, exp=now-10s fails); COMP-006a Redis stores SHA-256 hash (never plain) with TTL=604800; COMP-006b revokes old + issues new on refresh; COMP-RESET-001 atomic compare-and-delete prevents replay (second use returns 401); COMP-RESET-INVALIDATE integration test (3 tokens → all revoked on reset); API-007 + COMP-015 round-trip test (logout revokes refresh, clears HttpOnly cookie, emits AUTH_LOGOUT audit row); COMP-HTTPONLY-001 contract test asserts HttpOnly+Secure+SameSite=Strict+Path=/v1/auth; COMP-ENVELOPE-001 contract test sweeps all 7 endpoints.

**M4: Integration & Hardening** | Exit: TEST-006 E2E (including auto-login failure compensation path landing on LoginPage with email pre-filled and no duplicate account); COMP-SILENT-REFRESH fires at exp-60s via jest fake timers; COMP-401-INT retries once then logs out (infinite-loop guard asserted); all 4 Prometheus metric names emitted verbatim (`auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`); OPS-007-TRACE spans parent→PasswordHasher/TokenManager→JwtService visible in staging APM; OPS-007-A1/A2/A3 alerts dry-run fire correctly and route to auth-team on-call; NFR-PERF-001 histograms confirm p95<200ms on all 7 endpoints; NFR-PERF-002 k6 10-min 500-concurrent scenario error rate <0.1%; NFR-COMPLIANCE-001 SOC2 query interface signed off; NFR-COMPLIANCE-002 E2E (registration-without-consent rejected; consent export returned); SEC-PENTEST-001 Critical + High remediated; COMP-LOGHYG-002 scans 1000 log + 1000 trace samples → zero secret fields; SUCC-METRIC-001..006 dashboards live; JTBD-GAP-001 admin CLI query works end-to-end.

**M5: Production Readiness & GA** | Exit: OPS-SMOKE-001 passes after MIG-001 / MIG-002 / MIG-003 transitions (covers all 7 endpoints incl. logout); OPS-ROLLBACK-001 all 6 ordered steps executable in staging with named owner + evidence; OPS-ROLLBACK-T1..T4 dry-runs trigger flag toggle with verbatim thresholds (>1000ms/5min, >5%/2min, >10/min, data-corruption probe); OPS-003 24/7 rotation live; OPS-004/005/006 capacity validated against M4 load-test numbers (OPS-006 `TBD-pending-OQ-PRD-002` closed before MIG-001); OPS-LEGACY-001 Deprecation + Sunset headers emit at GA; OPS-VULN-001 first quarterly RS256 rotation dry-run verifies dual-key verification during grace; OPS-AUDIT-QA walks every happy + error path for 7 endpoints and asserts exactly 1 audit row each; OPS-RPC-001 99.9% over 7 consecutive days post-GA; MIG-004-CLEANUP removes `AUTH_NEW_LOGIN` with all conditional paths simplified; MIG-005-CLEANUP scheduled 2026-06-23; OPS-GDPR-EXPORT validated against Article 15.

## 6. Quality Gates

|Gate|Position|Condition|On Failure|
|---|---|---|---|
|G1|End of V1 (blocks M3 entry)|All V1 exit criteria met; OQ-REFRESH-TRANSPORT-001 closed; security-review lead onboarded|**stop-and-fix** — hold M3 kickoff until resolved|
|G2|End of V2 (blocks M5 entry / OPS-SIGNOFF-001)|All V2 exit criteria met; SEC-PENTEST-001 Critical+High=0; NFR-PERF-001/002 pass; NFR-COMPLIANCE-001/002 sign-off; JTBD-GAP-001 CLI live|**stop-and-fix** — hold OPS-SIGNOFF-001 / MIG-001|
|G3|Between MIG-001 → MIG-002|Alpha smoke clean; zero P0/P1; test-lead sign-off|Roll back to M4 staging; fix before Beta|
|G4|Between MIG-002 → MIG-003|Beta p95<200ms, error rate<0.1%, zero T1..T4 auto-triggers fired unprompted; eng-manager sign-off|Extend Beta or trigger OPS-ROLLBACK-001|
|G5|GA+7 days|99.9% uptime sustained; OPS-RPC-001 green; no Critical findings open|If breached, post-mortem within 48h + triage|
|G6|GA+14 days|`AUTH_TOKEN_REFRESH` removal canary + contract test (flag ON and OFF unconditional)|Block MIG-005-CLEANUP if regression; reintroduce flag ON|

**Issue severity enforcement across all gates:** CRITICAL blocks current milestone immediately; MAJOR blocks next milestone (paired V# cannot close); MINOR tracked in next sprint; COSMETIC backlog. Policy: **stop-and-fix** for CRITICAL and MAJOR with no exceptions — no "proceed with known issue" waiver path defined for this release.
