---
high_severity_count: 0
medium_severity_count: 3
low_severity_count: 4
total_deviations: 7
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **Severity**: MEDIUM
- **Deviation**: Roadmap milestone structure diverges from spec's downstream guidance of two milestones.
- **Source Quote**: "The authentication service introduces a single theme ('Secure User Authentication') spanning two milestones: (1) Core Auth Infrastructure (password hashing, JWT signing, token management) and (2) Auth API Endpoints (login, register, refresh, profile, reset). Each milestone maps directly to the implementation order in Section 4.6."
- **Roadmap Quote**: "M1 Foundation, Data Layer, Key Management | M2 Core Auth Primitives | M3 Auth Service and Endpoints | M4 Non-Functional Requirements and Observability | M5 Hardening, Validation, and Release"
- **Impact**: Spec guidance for sc:roadmap was a two-milestone structure mapping to Section 4.6; roadmap expands to five, separating infrastructure, NFRs, and release gates into their own milestones. Does not alter functional correctness but reorganizes milestone boundaries.
- **Recommended Correction**: Either consolidate M1/M2 and M4/M5 into the two-milestone structure per spec guidance, or document in roadmap rationale why a five-milestone expansion was preferred (risk front-loading, NFR/release gating).

### DEV-002
- **Severity**: MEDIUM
- **Deviation**: Spec's two-phase rollout (opt-in then mandatory) is not mapped to roadmap tasks.
- **Source Quote**: "Authentication will be opt-in during phase 1, required for protected endpoints in phase 2."
- **Roadmap Quote**: "Staged rollout (canary→25%→100%) with kill-switch verified"
- **Impact**: Roadmap replaces the spec's semantic phase model (opt-in vs. required) with a percentage canary model. The transition from phase 1 (opt-in) to phase 2 (required for protected endpoints) is not tracked as a discrete milestone deliverable.
- **Recommended Correction**: Add explicit tasks (or split FF-001) for Phase 1 opt-in enablement and Phase 2 enforcement of authentication on protected endpoints, with acceptance criteria keyed to those two states.

### DEV-003
- **Severity**: MEDIUM
- **Deviation**: bcrypt cost factor verification timing band widened beyond spec's stated target.
- **Source Quote**: "bcrypt cost factor 12 (approx. 250ms per hash) | Unit test verifying cost factor; benchmark test for hash timing"
- **Roadmap Quote**: "p95 between 200ms and 350ms on reference hardware (CI env-var override); failure prints actual ms"
- **Impact**: Spec benchmark target is "approx. 250ms"; roadmap admits a ±100ms band (200-350ms). Accepting hash times as low as 200ms may silently admit regressions below spec's approximate target.
- **Recommended Correction**: Tighten SEC-001 acceptance criterion to center on ~250ms (e.g., 225-275ms) or document the rationale for the wider band and explicitly gate on NFR-AUTH.3 compliance.

### DEV-004
- **Severity**: LOW
- **Deviation**: Module dependency graph in spec places `auth-middleware` above `auth-service`, implying middleware consumes service directly; roadmap places middleware consuming only TokenManager.
- **Source Quote**: "auth-middleware.ts | v | auth-service.ts | / \\ | token-manager.ts   password-hasher.ts"
- **Roadmap Quote**: "COMP-002 → COMP-005 AuthMiddleware → FR-AUTH.4 (API-004)"
- **Impact**: Spec diagram shows middleware → auth-service → token-manager; roadmap wires middleware directly to TokenManager (COMP-002), bypassing AuthService. Functionally equivalent for verification, but architecturally different from spec diagram.
- **Recommended Correction**: Either update COMP-005 to depend on COMP-001 (AuthService) per spec diagram, or amend roadmap rationale documenting that middleware consumes TokenManager directly for token verification (a reasonable optimization).

### DEV-005
- **Severity**: LOW
- **Deviation**: Spec explicitly states no CLI surface; roadmap does not restate this constraint.
- **Source Quote**: "The authentication service does not expose a CLI interface. All interactions occur through the REST API endpoints defined in the functional requirements."
- **Roadmap Quote**: [MISSING]
- **Impact**: Roadmap does not contradict the spec but omits the explicit no-CLI commitment. Low risk of downstream task generators inferring CLI scaffolding.
- **Recommended Correction**: Add a one-line note in Decision Summary or M3 scope clarifying that no CLI surface is produced; all interfaces are REST.

### DEV-006
- **Severity**: LOW
- **Deviation**: Spec data flow diagram shows TokenManager invoking JwtService for both access and refresh token signing; roadmap's CRYPTO-002 stores refresh tokens as SHA-256 hashes (opaque), not JWT-signed.
- **Source Quote**: "TokenManager | -- sign JWT --> | <--- access_token --- | -- sign refresh ----> | <--- refresh_token ---"
- **Roadmap Quote**: "Refresh tokens stored only as SHA-256 hashes, never in plaintext | DB insert uses sha256(token)"
- **Impact**: Spec's sequence diagram implies both tokens are JWT-signed; spec Section 4.5 describes refresh_token as "Opaque token, 7-day TTL" which aligns with roadmap. Internal spec inconsistency; roadmap follows the data-model definition. No correctness impact but spec diagram is inconsistent with DM.
- **Recommended Correction**: No roadmap change required; flag the spec diagram inconsistency for spec-level correction in a future revision (refresh is opaque, not JWT).

### DEV-007
- **Severity**: LOW
- **Deviation**: Spec RISK-3 mitigation lists three specific items; roadmap risk register condenses them.
- **Source Quote**: "Make cost factor configurable; review annually against OWASP recommendations; migration path to Argon2id if needed"
- **Roadmap Quote**: "Cost read from config (CRYPTO-003); SEC-001 benchmark; annual OWASP review; Argon2id migration path documented"
- **Impact**: Roadmap preserves all three mitigations plus SEC-001 evidence; ordering and phrasing differ but content is equivalent. No functional deviation.
- **Recommended Correction**: None required; content matches.

## Summary

Analysis complete. Found 7 deviations: 0 HIGH, 3 MEDIUM, 4 LOW. All functional requirements (FR-AUTH.1 through FR-AUTH.5), non-functional requirements (NFR-AUTH.1 through NFR-AUTH.3), data models (UserRecord, RefreshTokenRecord, AuthTokenPair), architecture files, test plan items, gap-analysis items (GAP-1/2/3 → OI-6/7/8), and the open items (OI-1, OI-2) are traceable in the roadmap with explicit wiring tasks. MEDIUM findings concern milestone granularity divergence from downstream guidance, phased rollout semantics, and benchmark tolerance band — all correctable without structural rework. Tasklist readiness: true (no HIGH severity blockers).
