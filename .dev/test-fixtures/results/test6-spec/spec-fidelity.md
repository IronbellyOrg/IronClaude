---
high_severity_count: 0
medium_severity_count: 6
low_severity_count: 2
total_deviations: 8
validation_complete: true
tasklist_ready: true
---

## Deviation Report

**DEV-001** | **MEDIUM**
- **Deviation**: Implementation order diverges — spec puts database migrations at step 5 (last); roadmap moves them to Phase 1 (first)
- **Source Quote**: `"5. routes + migrations -- depends on 3, 4"` (Section 4.6)
- **Roadmap Quote**: `"COMP-007 | Build auth table migration | DB | OPS-001"` (Phase 1, row 5)
- **Impact**: Timeline and dependency sequencing differs from spec guidance. Roadmap's order is arguably more pragmatic (repos need schema), but deviates from the stated plan. Could cause confusion if spec is used as implementation reference alongside roadmap.
- **Recommended Correction**: Add a note in the roadmap acknowledging the reordering with rationale: "Migrations moved to Phase 1 to unblock repository implementation; departs from Section 4.6 ordering."

**DEV-002** | **MEDIUM**
- **Deviation**: Spec allows TokenManager to be built in parallel with JwtService; roadmap makes TokenManager sequentially dependent on JwtService
- **Source Quote**: `"token-manager.ts -- [parallel with jwt-service once interface defined]"` (Section 4.6, step 2)
- **Roadmap Quote**: `"COMP-002 | Implement token manager | Auth | COMP-003,COMP-009,DM-003"` (Phase 2, depending on Phase 1 COMP-003)
- **Impact**: Extends critical path by removing a parallelization opportunity. Phase 2 cannot start TokenManager until Phase 1 JwtService completes. Could add 1-2 days to schedule if JwtService encounters issues.
- **Recommended Correction**: Split COMP-002 dependency — allow TokenManager implementation to begin once JwtService interface is defined (not fully implemented). Alternatively, document why full implementation dependency was chosen.

**DEV-003** | **MEDIUM**
- **Deviation**: E2E test (TEST-004) omits step 6 "Login with new password" and the verification that "old credentials rejected after reset"
- **Source Quote**: `"1. Register new user 2. Login with credentials 3. Access profile with token 4. Refresh token 5. Reset password 6. Login with new password"` and `"old credentials rejected after reset"` (Section 8.3)
- **Roadmap Quote**: `"register→login→me→refresh→reset:pass; cookie flow:pass; replay defense:pass; full lifecycle in single test; real DB"` (TEST-004)
- **Impact**: Missing post-reset login verification means the E2E test could pass even if password reset doesn't actually update credentials. A critical user journey step goes untested.
- **Recommended Correction**: Extend TEST-004 AC to: `"register→login→me→refresh→reset→login-new-pw:pass; old-creds-rejected; cookie flow:pass; replay defense:pass"`

**DEV-004** | **MEDIUM**
- **Deviation**: Spec integration test #3 "Registration followed by login succeeds with same credentials" is not a dedicated integration test in the roadmap
- **Source Quote**: `"Registration followed by login succeeds with same credentials | FR-AUTH.1, FR-AUTH.2: Data persistence between registration and authentication"` (Section 8.2)
- **Roadmap Quote**: TEST-007 covers `"valid→201+profile; dup-email→409; weak-pw→400; bad-email→400; user persisted in DB"` — registration only, no subsequent login
- **Impact**: Cross-flow data persistence (password hash stored during registration is usable for login) has no Phase 3 integration test. TEST-004 (E2E, Phase 4) covers it, but the gap delays detection of persistence bugs.
- **Recommended Correction**: Add AC to TEST-007 or create TEST-009: `"register→login-same-creds→200+tokens; validates FR-AUTH.1+FR-AUTH.2 data persistence"`

**DEV-005** | **MEDIUM**
- **Deviation**: Spec's two-phase rollout plan (opt-in → required) has no explicit transition task in the roadmap
- **Source Quote**: `"Authentication will be opt-in during phase 1, required for protected endpoints in phase 2."` (Section 9)
- **Roadmap Quote**: `"AUTH_SERVICE_ENABLED:true globally; monitoring stable 24h; no rollback triggered"` (OPS-011) — enables the service but doesn't make it required
- **Impact**: The feature flag controls whether auth routes exist, not whether other endpoints require authentication. No task addresses transitioning existing endpoints from unauthenticated to auth-required. Could result in auth being deployed but never enforced.
- **Recommended Correction**: Add OPS-013: "Enable auth-required mode on protected endpoints" with AC specifying which endpoints transition and the enforcement mechanism.

**DEV-006** | **MEDIUM**
- **Deviation**: Spec directs roadmap to use a two-milestone structure; roadmap uses four phases
- **Source Quote**: `"The authentication service introduces a single theme ('Secure User Authentication') spanning two milestones: (1) Core Auth Infrastructure (password hashing, JWT signing, token management) and (2) Auth API Endpoints (login, register, refresh, profile, reset)."` (Section 10)
- **Roadmap Quote**: `"total_phases: 4"` with phases: Security Foundation, Core Flows, API Exposure, Hardening
- **Impact**: Downstream consumers expecting two milestones (per spec directive) will encounter four phases. Milestone tracking and sprint planning must adapt. The four-phase structure is arguably better decomposed but misaligns with the spec's stated structure.
- **Recommended Correction**: Either restructure to two phases matching the spec, or add a mapping note: "Spec milestones → roadmap phases: Milestone 1 = Phase 1+2; Milestone 2 = Phase 3+4."

**DEV-007** | **LOW**
- **Deviation**: Spec names specific test file paths; roadmap uses task IDs without file paths
- **Source Quote**: `"tests/auth/password-hasher.test.ts"`, `"tests/auth/jwt-service.test.ts"`, `"tests/auth/token-manager.test.ts"`, `"tests/auth/auth-service.test.ts"` (Section 8.1)
- **Roadmap Quote**: `"TEST-001 | Add crypto primitive tests"`, `"TEST-002 | Add auth service unit tests"` — no file paths specified
- **Impact**: Minor — implementers may place test files inconsistently without path guidance, but task descriptions provide sufficient information for correct placement.
- **Recommended Correction**: Add file path to test task AC (e.g., TEST-001 AC: `"path:tests/auth/password-hasher.test.ts+jwt-service.test.ts"`).

**DEV-008** | **LOW**
- **Deviation**: Roadmap introduces 8 additional source files beyond the spec's 4 new files
- **Source Quote**: Section 4.1 lists 4 new files: `auth-service.ts`, `token-manager.ts`, `jwt-service.ts`, `password-hasher.ts`
- **Roadmap Quote**: Additional files: `secrets-provider.ts` (COMP-012), `user-repository.ts` (COMP-008), `refresh-token-repository.ts` (COMP-009), `auth-rate-limiter.ts` (COMP-010), `reset-email-adapter.ts` (COMP-011), `auth-config.ts` (COMP-013), `auth-feature-gate.ts` (COMP-014), `auth-cookie-policy.ts` (COMP-015)
- **Impact**: Scope expansion is additive, not contradictory. Additional components improve separation of concerns and testability. However, effort estimates based on the spec's 4-file scope will undercount actual work.
- **Recommended Correction**: Acceptable as architectural elaboration. No correction needed, but effort estimates should account for the expanded file count.

## Summary

**Distribution**: 0 HIGH | 6 MEDIUM | 2 LOW | 8 total

The roadmap demonstrates strong fidelity to the source specification. All 5 functional requirements (FR-AUTH.1–5), all 3 non-functional requirements (NFR-AUTH.1–3), all 3 data models, all API endpoints, all 3 risks, and both open items are faithfully represented. Integration wiring is complete — every dependency injection point, strategy pattern, and middleware chain in the spec has a corresponding creation task, wiring task, and test in the roadmap.

The 6 MEDIUM deviations fall into two categories: **structural** (implementation ordering and milestone structure differ from spec directives) and **test coverage gaps** (E2E post-reset login verification and cross-flow integration test missing as dedicated items). None represent missing requirements or contradicted constraints.

**Tasklist readiness**: With zero HIGH deviations, the roadmap is suitable for tasklist generation. The MEDIUM deviations should be addressed as refinements but do not block decomposition into actionable tasks.
