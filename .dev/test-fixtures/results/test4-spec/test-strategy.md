---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 2
work_milestones: 5
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: test-spec-user-auth.md
generated: "2026-04-15T00:53:18.127366+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy: User Authentication Service

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

**Classification examples specific to this project**:
- CRITICAL: JWT signing produces invalid tokens; refresh token stored in plaintext; replay detection fails to revoke sessions; password_hash leaked in API response
- MAJOR: Rate limiter off by one (6 instead of 5); bcrypt cost factor not configurable; enumeration timing variance > 10ms; migration down script leaves orphaned indexes
- MINOR: Error message wording inconsistent across endpoints; display_name trim behavior undefined; health check response schema not documented
- COSMETIC: Log message formatting; variable naming inconsistency in test fixtures

---

## 1. Validation Milestones Mapped to Roadmap Phases

The roadmap defines 6 implementation phases (0–5) plus one advisory checkpoint (B). Two existing milestones are validation-oriented:

| Validation Milestone | Roadmap Location | Type | Covers |
|---------------------|------------------|------|--------|
| **VM-1: Checkpoint B** | After Phase 2 | Advisory review | Phases 0–2 integration integrity |
| **VM-2: Phase 5** | Final phase | Formal validation + release gate | All phases; SC-1 through SC-14 |

### Recommended Additional Validation Gates (to achieve 1:2 ratio)

The MEDIUM complexity class prescribes a 1:2 interleave ratio. The existing roadmap places validation too late (primarily Phase 5). The strategy inserts validation gates to catch issues earlier:

| Inserted Gate | After Phase | Validates |
|---------------|-------------|-----------|
| **VG-0/1** | Phase 1 | Phase 0 contracts + infrastructure; Phase 1 registration/login acceptance criteria |
| **VG-2/3** (= Checkpoint B, upgraded from advisory to gating) | Phase 3 | Phase 2 token lifecycle + Phase 3 password reset; full 6-endpoint integration |
| **VG-4/5** (= Phase 5, existing) | Phase 5 | Phase 4 NFR hardening; final E2E + release gate |

This yields 3 validation gates across 5 work phases — a ratio of approximately 1:1.7, satisfying the 1:2 minimum.

---

## 2. Test Categories

### 2.1 Unit Tests (~25 cases)

Isolated component verification. No database, no network.

| Component | Test Focus | Roadmap ID | Phase |
|-----------|-----------|------------|-------|
| PasswordHasher | Hash roundtrip, wrong-password rejection, cost factor assertion, configurable cost | TEST-001 | 1 |
| JwtService | RS256 sign/verify roundtrip, expired token rejection, malformed token, kid header presence, TTL configuration | TEST-002 | 1 |
| TokenManager | Access token generation (15min TTL), refresh token generation (7d TTL), SHA-256 hashing of refresh tokens, reset token generation (1h TTL) | Implicit in TEST-005 | 1–2 |
| Auth middleware | Bearer extraction, missing header (401), malformed token (401), expired token (401), valid token context attachment | Implicit in COMP-004 | 0–1 |
| Password policy | 7-char rejection, missing uppercase, missing lowercase, missing digit, 8-char valid boundary | FR-AUTH.2c | 1 |
| Email validation | Malformed email formats, RFC 5322 basic validation | FR-AUTH.2d | 1 |
| Response DTO | Allowlisted fields only; password_hash and token_hash excluded | FR-AUTH.4c | 2 |

### 2.2 Integration Tests (~25 cases)

Endpoint-to-database verification with real database.

| Flow | Cases | Roadmap ID | Phase |
|------|-------|------------|-------|
| Registration (FR-AUTH.2) | Valid 201, duplicate 409, bad password 400, bad email 400 | TEST-003 | 1 |
| Login (FR-AUTH.1) | Valid 200 + tokens, invalid creds 401, locked 403, rate limit 429 | TEST-004 | 1 |
| Token refresh (FR-AUTH.3) | Rotation (new pair), expired 401, replay → full revocation, hash storage | TEST-005 | 2 |
| Profile (FR-AUTH.4) | Valid fetch 200, expired token 401, no sensitive fields | TEST-006 | 2 |
| Password reset (FR-AUTH.5) | Token generation + email dispatch, reset confirmation + invalidation, expired token 400, session revocation | TEST-008 | 3 |
| Response schema | Zero occurrences of password_hash/token_hash across all endpoints | TEST-007 | 2 |

### 2.3 Security Tests (~8 cases)

Adversarial verification targeting identified risks.

| Test | Target Risk | Roadmap ID | Phase |
|------|------------|------------|-------|
| Enumeration resistance (login) | R-6 | TEST-009 | 4 |
| Timing analysis (valid vs invalid email) | R-6 | TEST-009 | 4 |
| Replay detection chain (rotate → reuse old → verify full revocation) | R-2 | TEST-005 / R-2 task | 2, 4 |
| Sensitive field leakage scan (all endpoints) | Data exposure | TEST-007 | 2, 5 |
| Reset token single-use enforcement | FR-AUTH.5b | TEST-008 | 3 |
| Rate limiter boundary (5th passes, 6th blocked, reset works) | FR-AUTH.1d | TEST-010 | 4 |
| Progressive lockout (cross-IP failures) | R-6 | R-6 task | 4 |
| Feature flag gate (503 when disabled) | OPS-009 | SC-13 | 5 |

### 2.4 Performance / Load Tests (~5 cases)

NFR verification under load.

| Test | Target | Tool | Roadmap ID | Phase |
|------|--------|------|------------|-------|
| p95 latency (all auth endpoints) | < 200ms | k6 | OPS-004, SC-8 | 4–5 |
| Rate limiter under concurrent load | 429 at boundary | k6 | TEST-010 | 4 |
| bcrypt benchmark (100 iterations) | ~250ms ± 20% | Custom benchmark | TEST-011 | 4 |
| Refresh token rotation under concurrency | No lost rotations | k6 | OPS-004 | 4 |
| Login endpoint sustained throughput | Stable p95 | k6 | NFR-AUTH.1 | 4 |

### 2.5 E2E Tests (~3 cases)

Full lifecycle traversal through all endpoints.

| Scenario | Steps | Roadmap ID | Phase |
|----------|-------|------------|-------|
| Happy-path lifecycle | register(201) → login(200) → profile(200) → refresh(200) → reset-request(200) → re-login(200) | TEST-012, SC-6 | 5 |
| Replay attack lifecycle | register → login → refresh → reuse-old-refresh(401) → verify-all-revoked → re-login | TEST-005 extension | 5 |
| Feature flag lifecycle | flag-on: all endpoints work → flag-off: all return 503 → flag-on: all recover | SC-13 | 5 |

### 2.6 Infrastructure / Deployment Tests (~4 cases)

| Test | Validates | Roadmap ID | Phase |
|------|-----------|------------|-------|
| Migration up (create tables) | DM-001, DM-002 columns, types, indexes, FKs | MIG-001 | 0 |
| Migration down (drop tables) | Clean rollback, no orphans, idempotent | MIG-002, SC-14 | 0, 5 |
| Health check endpoint | 200 with auth dependency status | NFR-AUTH.2 | 4 |
| PagerDuty alert on failure | Alert fires within 60s | OPS-003 | 4 |

---

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

MEDIUM complexity (0.6) prescribes **1:2** — one validation milestone for every two work milestones. This is appropriate because:

1. **Security sensitivity is high (0.8)** — cryptographic and token-lifecycle errors are silent and high-impact. Catching them early is disproportionately valuable.
2. **Architectural footprint is modest (0.5)** — the bounded scope means validation gates can be thorough without being expensive.
3. **State management is complex (0.7)** — refresh token rotation with replay detection introduces multi-step state transitions that only surface bugs through integration testing.

A 1:1 ratio (HIGH) would over-invest in formal gates for a well-bounded module. A 1:3 ratio (LOW) would defer security validation dangerously late.

### Interleaving Schedule

```
Phase 0 (1.5 wk)  ─── Work: Foundation, contracts, infra
  └─ Inline: Migration up/down test, contract review
Phase 1 (1.5 wk)  ─── Work: Registration & Login
  └─ Inline: TEST-001..004 (unit + integration for Phase 0-1 components)
 ┌──────────────────────────────────────────────────────┐
 │ VG-0/1: Validation Gate (0.5 day)                    │
 │  - All Phase 0 contracts approved                    │
 │  - Migration tested (up + down)                      │
 │  - PasswordHasher, JwtService, TokenManager pass     │
 │  - Registration 4/4 criteria green                   │
 │  - Login 4/4 criteria green                          │
 │  - Feature flag toggle verified                      │
 └──────────────────────────────────────────────────────┘
Phase 2 (1 wk)     ─── Work: Token Lifecycle & Profile
  └─ Inline: TEST-005..007
Phase 3 (1 wk)     ─── Work: Password Reset
  └─ Inline: TEST-008
 ┌──────────────────────────────────────────────────────┐
 │ VG-2/3: Validation Gate (0.5 day) [= Checkpoint B    │
 │         upgraded to gating]                          │
 │  - Token refresh 4/4 criteria green                  │
 │  - Profile 3/3 criteria green                        │
 │  - Password reset 4/4 criteria green                 │
 │  - Replay detection end-to-end verified              │
 │  - Response schema scan: zero leakage                │
 │  - 6-endpoint integration lifecycle smoke test       │
 └──────────────────────────────────────────────────────┘
Phase 4 (1.5 wk)   ─── Work: NFR Hardening
  └─ Inline: TEST-009..011, OPS-004
Phase 5 (1 wk)     ─── Validation: Final gate
 ┌──────────────────────────────────────────────────────┐
 │ VG-4/5: Release Gate (1 wk)                          │
 │  - SC-1 through SC-14 green                          │
 │  - E2E lifecycle (TEST-012) green                    │
 │  - OQ-1/3/7/8 closed with evidence                   │
 │  - Load test p95 < 200ms                             │
 │  - Feature flag rollback proven                      │
 │  - Migration rollback proven                         │
 │  - Regression suite: zero breaks                     │
 └──────────────────────────────────────────────────────┘
```

### Continuous-Parallel Execution Model

Tests are not batch-deferred. Each phase co-locates test implementation with feature implementation:

- **Same-phase unit tests**: Written alongside the component (e.g., TEST-001/002 written during Phase 1 as COMP-001/002 are built)
- **Same-phase integration tests**: Written after the endpoint is functional (e.g., TEST-003 written after FR-AUTH.2a–d are complete)
- **Validation gates run accumulated tests**: Gates re-run all tests from prior phases plus gate-specific checks
- **Security and load tests are Phase 4 deliverables**: Created and first-executed in Phase 4; re-executed in Phase 5 gate

---

## 4. Risk-Based Test Prioritization

### Priority Tier 1: Test First, Block on Failure (CRITICAL/MAJOR)

These tests address the highest-severity risks and are mandatory before proceeding past their owning phase.

| Risk | Test | Why First | Consequence of Deferral |
|------|------|-----------|------------------------|
| **R-2: Refresh token replay** | TEST-005 (FR-AUTH.3c replay detection) | Highest residual risk after mitigation; race condition between legitimate and attacker refresh | Stolen tokens grant persistent access; full session revocation logic is foundational to security model |
| **R-1: JWT key compromise surface** | TEST-002 (kid header, key versioning) | Key rotation without versioning invalidates all tokens simultaneously | Mass forced re-auth on key rotation; operational incident |
| **R-4: Latency conflict** | TEST-011 (bcrypt benchmark) + OPS-004 (k6) | OQ-3 decision must be architecturally validated, not assumed correct | Ship with NFR-AUTH.1 violated; p95 > 200ms in production |
| **Data leakage** | TEST-007 (schema scan) | Sensitive fields in API responses are a compliance/security incident | password_hash or token_hash exposed to clients |
| **Enumeration resistance** | TEST-009 (timing analysis) | Timing side-channel leaks user existence | Account enumeration enables targeted attacks |

### Priority Tier 2: Test in Phase, Gate-Blocking (MAJOR)

| Risk | Test | Phase |
|------|------|-------|
| Rate limiter correctness | TEST-010 | 4 |
| Progressive lockout (R-6) | R-6 integration test | 4 |
| Email graceful degradation (R-5) | R-5 integration test | 4 |
| Migration rollback | SC-14 | 5 |
| Feature flag rollback | SC-13 | 5 |

### Priority Tier 3: Validate Before Release, Non-Blocking (MINOR)

| Area | Test | Phase |
|------|------|-------|
| Health check response schema | NFR-AUTH.2 | 4 |
| PagerDuty alert timing | OPS-003 | 4 |
| bcrypt cost factor configurability | R-3 unit test | 4 |
| Argon2id migration documentation | R-3 review | 4 |

---

## 5. Acceptance Criteria Per Milestone

### VG-0/1: Post-Phase 1 Gate

| # | Criterion | Evidence | Severity if Failed |
|---|-----------|----------|-------------------|
| 1 | Security contracts CONT-001, CONT-002 reviewed and approved by security engineer | Sign-off artifact | CRITICAL — blocks all implementation |
| 2 | Migration 003 up executes cleanly; tables have correct columns, types, indexes, FKs | MIG-001 test green | CRITICAL — blocks all data-dependent work |
| 3 | Migration 003 down drops tables cleanly, idempotent | MIG-002 test green | MAJOR — blocks release confidence |
| 4 | PasswordHasher: hash roundtrip, wrong-password rejection, cost == 12 | TEST-001 green | CRITICAL — blocks login |
| 5 | JwtService: RS256 sign/verify, expiry, malformed rejection, kid header | TEST-002 green | CRITICAL — blocks all token operations |
| 6 | Registration: 4/4 acceptance criteria (201, 409, 400×2) | TEST-003 green | CRITICAL — blocks Phase 2 |
| 7 | Login: 4/4 acceptance criteria (200, 401, 403, 429) | TEST-004 green | CRITICAL — blocks Phase 2 |
| 8 | Feature flag OPS-009 toggles /auth/* routes on/off | Manual verification | MAJOR — blocks regression confidence |
| 9 | OQ-3 decision documented with stakeholder sign-off | Decision artifact | MAJOR — blocks NFR-AUTH.1 work in Phase 4 |

**Gate rule**: All CRITICAL criteria must pass. MAJOR criteria follow stop-and-fix — work on Phase 2 may begin while MAJOR fixes are in progress, but VG-2/3 cannot pass until all MAJOR issues from VG-0/1 are resolved.

### VG-2/3: Post-Phase 3 Gate (Upgraded Checkpoint B)

| # | Criterion | Evidence | Severity if Failed |
|---|-----------|----------|-------------------|
| 1 | Token refresh: 4/4 criteria (rotation, expired, replay, hash storage) | TEST-005 green | CRITICAL |
| 2 | Replay detection triggers full user token revocation end-to-end | TEST-005 specific case | CRITICAL |
| 3 | Profile: 3/3 criteria (200, 401, no sensitive fields) | TEST-006 green | CRITICAL |
| 4 | Password reset: 4/4 criteria (generation, confirmation, expired, session revocation) | TEST-008 green | CRITICAL |
| 5 | Response schema scan: 0 occurrences of password_hash/token_hash in any /auth/* response | TEST-007 green | CRITICAL |
| 6 | Register → Login → Profile → Refresh → Reset → Re-login smoke test passes | Manual or scripted | MAJOR |
| 7 | AuthMiddlewareChain correctly distinguishes public vs protected routes | Manual or integration test | MAJOR |
| 8 | SecurityServiceContainer resolves all wired services at runtime | Integration verification | MAJOR |
| 9 | Email service adapter (COMP-007) registered and functional (or stubbed with documented plan) | Integration test or stub verification | MAJOR |
| 10 | All VG-0/1 MAJOR issues resolved | Issue tracker | MAJOR |

**Gate rule**: All CRITICAL criteria must pass before Phase 4 begins. Phase 4 hardening work is wasted if the functional foundation is broken.

### VG-4/5: Release Gate (Phase 5)

| # | Criterion | Evidence | Severity if Failed |
|---|-----------|----------|-------------------|
| 1 | SC-1 through SC-5: All FR acceptance criteria green in CI | TEST-003..008 | CRITICAL |
| 2 | SC-6: E2E lifecycle (6-step scenario) green | TEST-012 | CRITICAL |
| 3 | SC-7: Zero sensitive field leakage | TEST-007 | CRITICAL |
| 4 | SC-8: p95 < 200ms under normal load | k6 report (OPS-004) | CRITICAL |
| 5 | SC-9: Health check operational, PagerDuty alert fires within 60s | OPS-003 test | MAJOR |
| 6 | SC-10: bcrypt cost factor == 12 asserted | TEST-011 | MAJOR |
| 7 | SC-11: bcrypt ~250ms ± 20% benchmark | TEST-011 | MAJOR |
| 8 | SC-12: Zero regressions in pre-existing test suite | CI regression run | CRITICAL |
| 9 | SC-13: Feature flag rollback verified in staging | Manual staging test | CRITICAL |
| 10 | SC-14: Migration rollback clean and idempotent | MIG-002 re-verification | MAJOR |
| 11 | OQ-1-VAL: Email dispatch mode validated with implementation evidence | Integration test | MAJOR |
| 12 | OQ-3-VAL: Latency resolution validated with k6 evidence | k6 report | CRITICAL |
| 13 | OQ-7-VAL: Email service interface matches contract | Contract comparison | MAJOR |
| 14 | OQ-8-VAL: Key rotation procedure executed in staging | Staging evidence | MAJOR |
| 15 | All VG-2/3 MAJOR issues resolved | Issue tracker | CRITICAL |

**Gate rule**: This is a binary go/no-go release gate. ALL CRITICAL criteria must pass. ALL MAJOR criteria must pass or carry formal exemptions with documented rationale and stakeholder sign-off. No MAJOR exemptions permitted for security-related criteria (SC-7, TEST-007, TEST-009).

---

## 6. Quality Gates Between Phases

### Gate Structure

Each gate is a named checkpoint with explicit pass/fail criteria. Gates enforce the stop-and-fix policy for MAJOR and CRITICAL issues.

```
Phase 0 ──→ Phase 1
         │
         └── Gate G0: "Foundation Verified"
             Pass: Migration green, OQ-3 decision documented,
                   contracts CONT-001/002 approved
             Fail-CRITICAL: No implementation begins
             Fail-MAJOR: Phase 1 starts; fix in parallel

Phase 1 ──→ Phase 2
         │
         └── Gate VG-0/1: "Core Auth Validated"
             (See §5 VG-0/1 criteria above)
             Fail-CRITICAL: Phase 2 blocked
             Fail-MAJOR: Phase 2 starts; fix in parallel,
                         must resolve before VG-2/3

Phase 2 ──→ Phase 3
         │
         └── Gate G2: "Token Lifecycle Sound"
             Pass: TEST-005, TEST-006, TEST-007 green;
                   replay detection confirmed
             Fail-CRITICAL: Phase 3 blocked
             Fail-MAJOR: Phase 3 may start if OQ-7
                         was resolved (email interface ready)

Phase 3 ──→ Phase 4
         │
         └── Gate VG-2/3: "Functional Complete"
             (See §5 VG-2/3 criteria above)
             Fail-CRITICAL: Phase 4 blocked — hardening
                            a broken foundation is waste
             Fail-MAJOR: Phase 4 starts; all MAJOR resolved
                         before VG-4/5

Phase 4 ──→ Phase 5
         │
         └── Gate G4: "Hardening Complete"
             Pass: TEST-009, TEST-010, TEST-011 green;
                   OPS-004 k6 suite runnable; OPS-003 PagerDuty live
             Fail-CRITICAL: Phase 5 blocked
             Fail-MAJOR: Phase 5 starts; fix in parallel

Phase 5 ──→ Release
         │
         └── Gate VG-4/5: "Release Gate"
             (See §5 VG-4/5 criteria above)
             Binary go/no-go. No partial releases.
```

### Gate Escalation Protocol

1. **CRITICAL failure at any gate**: Work stops on downstream phases. The owning engineer and security engineer triage within 4 hours. Fix is the sole priority until the criterion passes.
2. **MAJOR failure at a gate**: Logged as a tracked issue with owner and deadline. Next phase may begin if the MAJOR issue is independent of downstream work. Must be resolved before the subsequent validation gate.
3. **MINOR/COSMETIC at a gate**: Logged. No gate impact. Addressed in next sprint or backlog.
4. **Regression in a previously-green test**: Treated as CRITICAL regardless of the test's original severity classification. A regression means the system's behavior changed unexpectedly.

### Test Environment Requirements

| Gate | Environment | Database | External Services |
|------|-------------|----------|-------------------|
| G0, VG-0/1 | CI + local dev | Real database (test instance) | Secrets manager (local fallback OK) |
| G2, VG-2/3 | CI + integration env | Real database (shared test instance) | Email service (stub acceptable with documented plan) |
| G4 | CI + staging | Real database (staging) | All services real (email, secrets manager, PagerDuty) |
| VG-4/5 | Staging → Production | Production database (canary) | All services production |

### Shared Test Fixtures (TEST-ARCH-002)

All gates rely on a common fixture set defined in Phase 0:

| Fixture | Contents | Used By |
|---------|----------|---------|
| `validUser` | Registered user with known email/password/display_name | TEST-003..008, TEST-012 |
| `lockedUser` | User with non-null `locked_at` | TEST-004 (FR-AUTH.1c) |
| `expiredRefreshToken` | Refresh token with `expires_at` in the past | TEST-005 (FR-AUTH.3b) |
| `revokedRefreshToken` | Refresh token with non-null `revoked_at` (for replay tests) | TEST-005 (FR-AUTH.3c) |
| `activeRefreshTokenSet` | N refresh tokens for one user (tests OQ-2 limit) | TEST-005, R-6 |
| `expiredResetToken` | Reset token with `expires_at` in the past | TEST-008 (FR-AUTH.5c) |
| `usedResetToken` | Reset token already consumed | TEST-008 (FR-AUTH.5b) |
| `rsaKeyPair` | Test RSA key pair for JWT operations | TEST-002, all integration tests |
