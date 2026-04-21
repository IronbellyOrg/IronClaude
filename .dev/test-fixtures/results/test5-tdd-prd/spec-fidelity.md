---
high_severity_count: 0
medium_severity_count: 4
low_severity_count: 3
total_deviations: 7
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **Severity**: MEDIUM
- **Deviation**: Audit log retention period conflicts between TDD (90 days) and roadmap (12 months), resolved in favor of PRD requirement.
- **Source Quote** (TDD §7.2): "Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days"
- **Roadmap Quote**: "Audit log RTN set to 12 months (PRD NC0 / SOC2) overriding TDD §7.2's 90-day default — CMP precedence DCM in OQ-CONFLICT-1."
- **Impact**: The roadmap intentionally overrides the TDD to comply with PRD's 12-month requirement for SOC2. This is a documented conflict resolution, but the TDD itself specifies 90 days. Resolution is appropriate given PRD/compliance precedence.
- **Recommended Correction**: Update TDD §7.2 to reflect 12-month retention to eliminate the documented conflict; alternatively, accept as resolved via OQ-CONFLICT-1.

### DEV-002
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds admin lock/unlock endpoints (API-009, API-010) and admin audit query endpoint (ADMIN-001) that are not specified in the TDD.
- **Source Quote** (TDD §8.1): Lists only POST `/auth/login`, POST `/auth/register`, GET `/auth/me`, POST `/auth/refresh` — no admin endpoints.
- **Roadmap Quote**: "API-009 | POST /v1/admin/users/{id}/lock | Wire admin lock EN1 with role-gated auth (Jordan persona incident response, JTBD-gap resolved)"
- **Impact**: Roadmap adds scope beyond TDD to address PRD Jordan persona JTBD gap. This is justified by PRD persona coverage requirement but extends TDD scope.
- **Recommended Correction**: Update TDD to include admin endpoints, or document this as an approved scope augmentation driven by PRD persona requirements.

### DEV-003
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds logout endpoint (POST /v1/auth/logout) not present in TDD §8.
- **Source Quote** (TDD §8.1): Does not include `/auth/logout` endpoint.
- **Roadmap Quote**: "PRD-GAP-LOGOUT | POST /v1/auth/logout EN1 | IM1 dedicated logout EN1 revoking current refresh token + clearing THP state (PRD AUTH-E1 logout story, absent in TDD)."
- **Impact**: Required by PRD user story ("As Alex, I want to log out so that I can secure my session on a shared device"), but missing from TDD. Roadmap correctly identifies and addresses this gap.
- **Recommended Correction**: Update TDD §8 to include POST /auth/logout endpoint contract to align with PRD.

### DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds PasswordResetToken data model (DM-004) not explicitly defined in TDD §7.
- **Source Quote** (TDD §7.1): Defines only `UserProfile` and `AuthToken` interfaces; no PasswordResetToken schema.
- **Roadmap Quote**: "DM-004 | PA2 schema | Define `PA2` PST DDL + TypeScript interface for reset-token persistence (single-use with 1h TTL)."
- **Impact**: Required for FR-AUTH-005 password reset persistence; TDD mentions 1-hour expiry but omits schema definition. Roadmap appropriately fills schema gap.
- **Recommended Correction**: Add PasswordResetToken data model to TDD §7.1 with fields matching DM-004.

### DEV-005
- **Severity**: LOW
- **Deviation**: Roadmap specifies API versioning (`/v1/auth/*`) as a committed deliverable; TDD §8.4 mentions versioning is via URL prefix "in production" without explicit M1 commitment.
- **Source Quote** (TDD §8.4): "The authentication API is versioned via URL prefix (`/v1/auth/*` in production)."
- **Roadmap Quote**: "API-VER-001 | API URL versioning | Establish `/v1/auth/*` URL-prefix versioning convention with DCM breaking-change policy."
- **Impact**: Roadmap clarifies ambiguous TDD language into concrete deliverable. No functional deviation.
- **Recommended Correction**: None required; roadmap appropriately concretizes TDD intent.

### DEV-006
- **Severity**: LOW
- **Deviation**: Roadmap adds /v1/health endpoint (API-011) as first-class deliverable; TDD §25 mentions health check monitoring but does not specify dedicated /health endpoint contract.
- **Source Quote** (TDD §4.1): "Service availability | 99.9% uptime | Health check monitoring over 30-day windows"
- **Roadmap Quote**: "API-011 | GET /v1/health | Expose /v1/health as distinct first-class deliverable (separate from internal /health) for external uptime monitors and load-balancer probes."
- **Impact**: Roadmap concretizes monitoring requirement into explicit endpoint. Aligned with NFR-REL-001 intent.
- **Recommended Correction**: Add /v1/health endpoint to TDD §8 with response contract.

### DEV-007
- **Severity**: LOW
- **Deviation**: Roadmap enforces per-user refresh token cap (5 tokens with oldest-eviction); TDD does not specify a cap.
- **Source Quote** (TDD §7.1 AuthToken, §8.2 /auth/refresh): No mention of per-user refresh token limit.
- **Roadmap Quote**: "Refresh-token cap=5 per user with OE policy (per OQ-PRD-2 RSL) — deterministic Redis sizing, reversible via feature flag if user friction observed."
- **Impact**: Resolves PRD Open Question #2 (Maximum refresh tokens per user). Reversible default; affects capacity sizing positively.
- **Recommended Correction**: Document decision in TDD §7 or §13 (Security); track as OQ-PRD-2 resolution.

## Summary

- **Total deviations**: 7 (0 HIGH, 4 MEDIUM, 3 LOW)
- **Validation complete**: true
- **Tasklist ready**: true

All TDD functional requirements (FR-AUTH-001 through FR-AUTH-005), NFRs (performance, reliability, security), data models, API endpoints, migration phases, observability commitments, and testing strategy are traced with explicit roadmap tasks. MEDIUM findings are augmentations driven by PRD persona coverage (Jordan admin needs, Alex logout story) and PRD compliance requirements (12-month audit retention), not omissions. The roadmap correctly identifies PRD-TDD gaps and addresses them through explicit tasks (PRD-GAP-LOGOUT, ADMIN-001, API-009/010, DM-004). Observability implementation tasks (OBS-001 through OBS-009) are separate from validation ACs, satisfying the anti-pattern check. Integration wiring (feature flags, middleware chains, DI points, dispatch tables) is fully tabled per milestone. No HIGH severity deviations found — roadmap is ready for tasklist generation.
