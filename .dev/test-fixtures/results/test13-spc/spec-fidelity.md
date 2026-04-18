---
high_severity_count: 0
medium_severity_count: 3
low_severity_count: 7
total_deviations: 10
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **Severity**: MEDIUM
- **Deviation**: Implementation order of database migrations reversed relative to spec's stated sequence.
- **Source Quote**: "1. password-hasher.ts -- No dependencies... 2. jwt-service.ts... 3. auth-service.ts... 4. auth-middleware.ts... 5. routes + migrations -- depends on 3, 4"
- **Roadmap Quote**: "M1: Foundation, Data Layer & Secrets... COMP-007 Implement `003-auth-tables.ts` migration" (migration placed in M1, first milestone, before PasswordHasher/JwtService in M2 and AuthService in M3).
- **Impact**: Roadmap front-loads schema work contrary to spec's explicit ordering; pragmatic but sequencing assumption may propagate into task generation where spec's ordering is authoritative.
- **Recommended Correction**: Either update the TDD to reflect that migrations must precede utility classes for test-against-DB reasons, or re-sequence the roadmap so migration work is deferred to match spec's step 5; document the decision explicitly.

### DEV-002
- **Severity**: MEDIUM
- **Deviation**: PasswordHasher hash-generation-and-comparison correctness unit test not explicitly included; only cost-factor inspection and timing benchmark are scheduled.
- **Source Quote**: "`PasswordHasher` hashes and verifies passwords correctly | `tests/auth/password-hasher.test.ts` | FR-AUTH.1, FR-AUTH.2: bcrypt hash generation and comparison"
- **Roadmap Quote**: "TEST-M2-002 | bcrypt timing benchmark... median 200–300ms" and "NFR-AUTH.3 | unit test asserts cost=12 embedded in hash prefix" ([MISSING] explicit hash/compare correctness test).
- **Impact**: Functional correctness of `hash()` and `compare()` is not directly validated; cost-factor and timing tests do not cover constant-time verification or round-trip correctness.
- **Recommended Correction**: Add an explicit PasswordHasher unit-test deliverable in M2 asserting `compare(password, hash(password)) === true` and `compare(wrong, hash(password)) === false`.

### DEV-003
- **Severity**: MEDIUM
- **Deviation**: Integration test "Registration followed by login" not represented as a standalone integration test.
- **Source Quote**: "Registration followed by login succeeds with same credentials | FR-AUTH.1, FR-AUTH.2: Data persistence between registration and authentication"
- **Roadmap Quote**: "TEST-M6-001 | E2E user lifecycle test... register→login→GET /me→refresh→password-reset→login-with-new-password" ([MISSING] as a distinct integration test).
- **Impact**: The focused register-then-login integration scenario is only validated within a broad E2E flow, making failure localization harder.
- **Recommended Correction**: Add a dedicated integration test deliverable in M3 for register→login persistence continuity, separate from the M6 lifecycle E2E.

### DEV-004
- **Severity**: LOW
- **Deviation**: Access token client-side storage strategy ("in memory") not explicitly enforced in roadmap.
- **Source Quote**: "Token storage | Access token in memory, refresh token in httpOnly cookie"
- **Roadmap Quote**: "SEC-007 Refresh token httpOnly cookie policy... refresh token returned only in Set-Cookie... no localStorage/sessionStorage emission path" ([MISSING] access-token-in-memory contract/lint).
- **Impact**: Refresh-token storage is explicitly constrained, but access-token delivery/storage guidance is implicit; consumers could store access tokens insecurely.
- **Recommended Correction**: Add a short deliverable or contract note in M3/M4 documenting that access tokens must not be set as cookies or written to browser storage; include client-side integration guidance.

### DEV-005
- **Severity**: LOW
- **Deviation**: OI-2 (max concurrent refresh tokens per user) is deferred rather than resolved.
- **Source Quote**: "OI-2 | What is the maximum number of active refresh tokens per user?... Resolution Target | Architecture review meeting"
- **Roadmap Quote**: "OI-2... Not blocking v1 (accepted as in-flight decision at M4 kickoff per Haiku improvement); enforceable change in v1.1 if deferred"
- **Impact**: Spec assigned resolution to an architecture review; roadmap accepts it as in-flight with potential v1.1 enforcement, softening the resolution commitment.
- **Recommended Correction**: Schedule an explicit architecture-review milestone or deliverable to resolve OI-2 before M4 kickoff, matching the spec's resolution target.

### DEV-006
- **Severity**: LOW
- **Deviation**: Roadmap introduces OI-6 (endpoint paths) and OI-7 (email provider) as new open items not present in the source spec.
- **Source Quote**: "OI-1... OI-2..." (only two open items in spec §11)
- **Roadmap Quote**: "OI-6 | Endpoint paths for register/refresh/password-reset... OI-7 | Email provider selection"
- **Impact**: Transparent extension surfacing gaps the spec left implicit; requires downstream TDD update rather than causing incorrect implementation. Marker tied to spec traceability ("only /auth/login and /auth/me verbatim in spec") — qualifies as traceable source-extension.
- **Recommended Correction**: Record as `PRD-gap-fill:TDD-update-needed` items; feed decisions back into the spec's §11 Open Items.

### DEV-007
- **Severity**: LOW
- **Deviation**: Roadmap introduces a 90-day RSA key rotation policy (OPS-006) not specified in source.
- **Source Quote**: "implement key rotation every 90 days" (appears only in Risk Assessment R1 mitigation, not as a deliverable)
- **Roadmap Quote**: "OPS-006 Document RSA key rotation policy (90-day)... runbook covers kid advertising; grace window for overlapping keys; rollback procedure; audit-log requirement"
- **Impact**: Roadmap promotes a risk-mitigation note to an explicit runbook deliverable — reasonable hardening; traceable to spec Risk §7.
- **Recommended Correction**: None required; record as traceable extension.

### DEV-008
- **Severity**: LOW
- **Deviation**: Roadmap introduces a dedicated `reset_tokens` table for password-reset tokens rather than reusing the `refresh_tokens` table implied by FR-AUTH.5 dependencies.
- **Source Quote**: "FR-AUTH.5... Dependencies | TokenManager, PasswordHasher, Email service (external)" — no reset_tokens table enumerated; spec §4.5 shows only UserRecord and RefreshTokenRecord.
- **Roadmap Quote**: "Reset token store | Repository extension | Dedicated `reset_tokens` table (chosen to separate single-use semantics from refresh rotation)"
- **Impact**: Adds a data structure not present in the spec's §4.5 data models. Decision is justified (different revocation semantics) but should be reflected in the data-model section of the TDD.
- **Recommended Correction**: Update source spec §4.5 to include a `ResetTokenRecord` schema, or note the extension as `PRD-gap-fill:TDD-update-needed`.

### DEV-009
- **Severity**: LOW
- **Deviation**: Roadmap introduces a COMP-017 account-suspension hook and forward-compatibility with progressive lockout beyond spec's minimal `is_locked` flag.
- **Source Quote**: "is_locked: boolean;  // Account suspension flag" (only a field; no lockout policy deliverable)
- **Roadmap Quote**: "COMP-017 Implement account suspension hook... centralized check invoked from login + refresh paths... forward-compatible with progressive lockout extension (GAP-1)"
- **Impact**: Transparent extension tying GAP-1 to a concrete surface; improves testability without changing requirements.
- **Recommended Correction**: None required; retain as traceable extension tied to GAP-1.

### DEV-010
- **Severity**: LOW
- **Deviation**: Roadmap strengthens password-reset endpoint to always return 202 regardless of whether email is registered (enumeration protection) — beyond spec's acceptance criteria.
- **Source Quote**: "Given a registered email, the system shall generate a password reset token (1-hour TTL) and dispatch a reset email"
- **Roadmap Quote**: "API-005... always 202 whether email known or not (no enumeration); rate-limited per IP"
- **Impact**: Security hardening; does not contradict spec but extends acceptance behavior. Traceable to spec's general "not reveal whether email or password was incorrect" philosophy in FR-AUTH.1.
- **Recommended Correction**: None required; record as security hardening and reflect in TDD acceptance criteria for FR-AUTH.5.

## Summary

Validation is complete with 0 HIGH, 3 MEDIUM, and 7 LOW severity deviations. All five functional requirements (FR-AUTH.1–FR-AUTH.5), three non-functional requirements (NFR-AUTH.1–NFR-AUTH.3), four new files, three modified files, three data models, feature-flag rollout, and all three gap items (GAP-1/2/3) are present in the roadmap. MEDIUM deviations concern implementation-order reversal of database migrations, a missing explicit PasswordHasher correctness unit test, and an absent standalone registration→login integration test. LOW deviations are largely transparent, security-hardening extensions (cookie policy, key rotation runbook, reset-token table, enumeration protection) and two added open items that should flow back into the TDD as `PRD-gap-fill:TDD-update-needed`. Roadmap is tasklist-ready (no HIGH severity blockers).
