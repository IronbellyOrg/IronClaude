# Opus:Architect Variant — Roadmap Proposal

> Captured verbatim from the opus:architect sub-agent during multi-roadmap adversarial generation. Preserved for traceability.

## Architectural Stance

The dominant risk surface here is **cryptographic and audit correctness, not feature throughput**. RISK-005 (Critical) and RISK-006 (High) compound silently — a flaw shipped in M1 propagates into every subsequent milestone's audit trail. Therefore this roadmap front-loads **trust primitives** (key management, audit sink, hashing contract) as a dedicated foundation milestone *before* any user-visible endpoint. The sonnet variant will likely fold these into M1-Login; that is the principal architectural disagreement.

A second deliberate divergence: **TokenManager is split from AuthService at M1**, not refactored out later. The 15-min/7-day asymmetric TTL, quarterly RS256 key rotation, and refresh-token rotation-on-use are sufficiently distinct concerns that coupling them to AuthService creates a god-object that resists the NFR-005 key rotation requirement.

## Milestones

### M1 — Cryptographic & Audit Foundation

- Type: SECURITY | Priority: P0 | Effort: M | Risk: High
- Dependencies: none
- Deliverables: RSA 2048-bit keypair + rotation harness + JWKS stub; PasswordHasher (bcrypt cost=12) with pluggable interface; AuditLogger append-only Postgres sink with 12-month retention; secrets management with key-id versioning
- Objective: Establish the three trust primitives every later milestone consumes. Audit as dependency, not afterthought.

### M2 — Identity Core & Registration

- Type: FEATURE | Priority: P0 | Effort: L | Risk: Med
- Dependencies: M1
- Deliverables: UserRepo with GDPR consent + soft-delete; POST /auth/register; TokenManager service with refresh-token rotation-on-use; audit hooks REGISTER_*
- Objective: Build identity substrate. TokenManager lands here, not M3, because registration must issue tokens for the auto-login UX path.

### M3 — Authentication Endpoints & Brute-Force Defense

- Type: FEATURE | Priority: P0 | Effort: L | Risk: High
- Dependencies: M2
- Deliverables: POST /auth/login with timing-safe compare + Redis lockout 5×/15min; POST /auth/refresh with reuse-detection (revoke family on replay); GET /auth/me + POST /auth/logout; audit hooks LOGIN_*, REFRESH_*, LOGOUT
- Objective: Complete synchronous auth surface. Lockout in isolated Redis namespace from sessions.

### M4 — Password Reset Flow

- Type: FEATURE | Priority: P1 | Effort: M | Risk: Med
- Dependencies: M3
- Deliverables: POST /auth/reset-request (1hr TTL token, SendGrid); POST /auth/reset-confirm (invalidate ALL sessions); audit hooks RESET_*; SendGrid retry queue + DLQ
- Objective: Reset is its own milestone — distinct token TTL, external dependency, highest blast-radius operation.

### M5 — Frontend Integration & AuthProvider

- Type: FEATURE | Priority: P1 | Effort: M | Risk: Med
- Dependencies: M3
- Deliverables: AuthProvider context (httpOnly cookies for RISK-001); LoginPage + RegisterPage + ProfilePage feature-flag-gated; silent refresh + 401 interceptor; reset UI flows
- Objective: Frontend after M3 stabilizes, not parallel — AuthProvider's storage decision must follow backend refresh contract.

### M6 — Performance, Compliance Hardening & Migration Gate

- Type: TEST + MIGRATION | Priority: P0 | Effort: L | Risk: High
- Dependencies: M5
- Deliverables: Load tests 500 concurrent p95<200ms; SOC2 audit-log completeness matrix; quarterly key-rotation drill with JWKS key-id; migration runbook with rollback gates
- Objective: This is the promotion gate, not a polish phase. Key-rotation drill pre-GA so the muscle exists when needed.

## Critical Path

M1 → M2 → M3 → M5 → M6 (5 hops). M4 parallelizes with M5 once M3 ships.

## Decision Rationale (key points)

- M1 is a dedicated foundation, not part of login — eliminates retrofit risk on RISK-005 (Critical)
- TokenManager splits at M2 — NFR-005 quarterly RS256 rotation requires this isolation
- Audit logging is a M1 deliverable — FR-007/NFR-006/RISK-006 form a compliance triad where retrofit is catastrophic
- Password reset is M4 standalone — distinct token TTL + external dep + highest blast radius
- Frontend M5 not parallel with M3 — AuthProvider storage is a RISK-001 architecture decision
- M6 is a gate, not polish — NFRs are promotion criteria
