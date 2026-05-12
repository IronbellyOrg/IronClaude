---
high_severity_count: 1
medium_severity_count: 4
low_severity_count: 2
total_deviations: 7
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **Severity**: HIGH
- **Deviation**: No database table or storage mechanism for password reset tokens. FR-AUTH.5 requires generating, storing, validating, and invalidating reset tokens, but the roadmap's migration tasks (Phase 1.1) only create `users` and `refresh_tokens` tables. No `password_reset_tokens` table is defined, and no alternative storage strategy (e.g., JWT-based stateless tokens) is specified.
- **Spec Quote**: "Given a registered email, the system shall generate a password reset token (1-hour TTL) and dispatch a reset email" (FR-AUTH.5a); "Given a valid reset token, the system shall allow setting a new password and **invalidate the reset token**" (FR-AUTH.5b)
- **Roadmap Quote**: Phase 1.1 migrations: "Create `users` table migration" and "Create `refresh_tokens` table migration" — no password reset token table. Phase 2.2: "Generate reset token (1hr TTL), dispatch email synchronously" and "Validate token → update password → invalidate token → revoke all refresh tokens" — storage mechanism unspecified.
- **Impact**: FR-AUTH.5b requires single-use token invalidation, which demands stateful storage. Without a table or explicit JWT-based approach with invalidation tracking, the password reset flow cannot be implemented as specified. Implementers will be forced to make an unguided architectural decision.
- **Recommended Correction**: Add a `password_reset_tokens` table migration to Phase 1.1 with columns: `id` (UUID v4 PK), `user_id` (FK → users), `token_hash` (SHA-256, unique), `expires_at`, `used_at` (nullable), `created_at`. Alternatively, explicitly document a signed JWT approach with a `used` flag tracked in the database.

### DEV-002
- **Severity**: MEDIUM
- **Deviation**: RefreshTokenRecord schema changed from `revoked: boolean` to `revoked_at` (timestamp), altering the data model contract without acknowledging the change.
- **Spec Quote**: `revoked: boolean;  // Account suspension flag` (Section 4.5 Data Models, RefreshTokenRecord interface)
- **Roadmap Quote**: Phase 1.1: "Columns: ... `revoked_at`, `created_at`"
- **Impact**: Changes the query semantics (check `revoked_at IS NOT NULL` vs `revoked = true`) and the interface contract. While `revoked_at` is arguably superior (provides audit timestamp), this is an undocumented deviation from the spec's defined data model. Implementers referencing the spec's TypeScript interface will encounter a mismatch.
- **Recommended Correction**: Acknowledge the schema change in the Open Questions section with rationale. Update the spec's `RefreshTokenRecord` interface to use `revoked_at: Date | null` if the timestamp approach is preferred.

### DEV-003
- **Severity**: MEDIUM
- **Deviation**: Implementation order diverges from spec's Section 4.6. The spec places "routes + migrations" at step 5 (last); the roadmap places migrations at Phase 1.1 (first).
- **Spec Quote**: "1. password-hasher.ts ... 2. jwt-service.ts ... 3. auth-service.ts ... 4. auth-middleware.ts ... 5. routes + migrations -- depends on 3, 4" (Section 4.6)
- **Roadmap Quote**: "The roadmap follows a **database-first** approach" (Executive Summary); Phase 1.1 is "Database Schema and Migrations" before any service code.
- **Impact**: The roadmap's database-first approach is arguably superior (services can integrate against real tables immediately), but it explicitly contradicts the spec's stated order. The spec's ordering implies migrations are bundled with routes as a final integration step. This affects sprint planning and task sequencing.
- **Recommended Correction**: The roadmap's approach is sound but should explicitly note the deviation from Section 4.6 and provide justification (which it partially does). The spec should be updated to reflect the database-first order if accepted.

### DEV-004
- **Severity**: MEDIUM
- **Deviation**: TokenManager sequenced strictly after JwtService instead of in parallel as the spec recommends. The spec explicitly marks TokenManager as parallelizable with JwtService.
- **Spec Quote**: "2. jwt-service.ts -- No dependencies; pure crypto / token-manager.ts -- [parallel with jwt-service once interface defined]" (Section 4.6)
- **Roadmap Quote**: JwtService is in Phase 1.3 (Week 1–2); TokenManager is in Phase 2.1 (Week 2–3) — separated by a phase boundary and crypto review gate.
- **Impact**: Adds approximately 1 week to the critical path compared to the spec's parallel suggestion. The crypto review gate (Phase 1.5) between them is a reasonable justification but is not acknowledged as a deviation from the spec's parallelism recommendation.
- **Recommended Correction**: Either explicitly justify the sequential ordering (crypto review gate must complete before TokenManager builds on JwtService) or restructure so TokenManager interface definition and implementation begin during Phase 1, with integration testing deferred to Phase 2.

### DEV-005
- **Severity**: MEDIUM
- **Deviation**: Logout functionality is declared in-scope by the spec but has no corresponding functional requirement, route, or roadmap task.
- **Spec Quote**: "**In scope**: User registration, **login/logout**, JWT token issuance and refresh, password hashing, authenticated profile retrieval, password reset flow." (Section 1.2)
- **Roadmap Quote**: [MISSING] — No logout endpoint, no `AuthService.logout()` method, no route for `POST /auth/logout`.
- **Impact**: Users have no explicit way to terminate their session. While refresh token expiration provides eventual logout, the spec's scope statement explicitly includes logout. The roadmap should either implement it (revoke all refresh tokens for the user) or explicitly defer it with justification.
- **Recommended Correction**: Add a `POST /auth/logout` route that calls `TokenManager.revokeAllForUser(userId)`, or explicitly note that logout is deferred despite the scope statement, with rationale (e.g., "stateless JWT access tokens cannot be revoked; logout is effective upon refresh token revocation, which is covered by `revokeAllForUser`").

### DEV-006
- **Severity**: LOW
- **Deviation**: Spec's test plan (Section 8.1) specifies exact test file paths; roadmap describes test content without referencing these paths.
- **Spec Quote**: "`tests/auth/password-hasher.test.ts`", "`tests/auth/jwt-service.test.ts`", "`tests/auth/token-manager.test.ts`", "`tests/auth/auth-service.test.ts`" (Section 8.1)
- **Roadmap Quote**: "Unit tests: hash timing ~250ms, verify round-trip, policy validation" (Phase 1.2) — no file path references.
- **Impact**: Minor organizational gap. Implementers may create tests with different file paths or structures than the spec intends. Does not affect correctness.
- **Recommended Correction**: Add the spec's test file paths to the roadmap's test tasks for consistency, or note that test organization follows the spec's Section 8.1 convention.

### DEV-007
- **Severity**: LOW
- **Deviation**: Spec references a specific migration file path `src/database/migrations/003-auth-tables.ts`; roadmap does not reference this file by name.
- **Spec Quote**: "`src/database/migrations/003-auth-tables.ts` | Add users and refresh_tokens tables" (Section 4.2, Modified Files)
- **Roadmap Quote**: "Create `users` table migration" and "Create `refresh_tokens` table migration" (Phase 1.1) — no file path specified; implies separate migration files rather than a single combined one.
- **Impact**: Minor. The roadmap implies two separate migration files (one per table) rather than the spec's single `003-auth-tables.ts`. This is a reasonable structural choice but differs from the spec's file listing.
- **Recommended Correction**: Either reference the spec's migration file path or note that the roadmap splits into two migration files for better reversibility granularity.

---

## Summary

The roadmap is a thorough and well-structured implementation plan that covers the vast majority of the specification's requirements. Of the 7 deviations identified:

| Severity | Count | Key Concern |
|----------|-------|-------------|
| HIGH | 1 | Missing password reset token storage mechanism (DEV-001) |
| MEDIUM | 4 | Schema change (DEV-002), implementation order (DEV-003), parallelism (DEV-004), missing logout (DEV-005) |
| LOW | 2 | File path references (DEV-006, DEV-007) |

**The single HIGH severity deviation (DEV-001) blocks tasklist readiness.** FR-AUTH.5 cannot be implemented without a defined storage mechanism for password reset tokens. This is likely an oversight, as the roadmap's Phase 2.2 describes the reset flow in detail but never addresses where reset tokens are persisted.

The MEDIUM deviations are defensible design choices (database-first ordering, `revoked_at` timestamp) but should be explicitly acknowledged as spec deviations with rationale. The missing logout endpoint (DEV-005) is a genuine gap between the spec's scope declaration and both documents' functional requirements.
