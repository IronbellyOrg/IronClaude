---
total_diff_points: 16
shared_assumptions_count: 15
---

## Shared Assumptions and Agreements

Both variants agree on:

1. RS256 asymmetric JWT signing with secrets-manager-stored private key
2. bcrypt password hashing at cost factor 12 (~250ms target)
3. Refresh token rotation with replay-triggered global session invalidation
4. Stateless 15min access tokens; 7d opaque refresh tokens stored as SHA-256 hashes
5. `AUTH_SERVICE_ENABLED` feature flag for dark-launch gating
6. Same core component dependency chain: JwtService + PasswordHasher → TokenManager → AuthService → Middleware → Routes
7. Same 6 functional requirements (FR-AUTH.1–5 plus profile retrieval)
8. Same 3 non-functional requirements (p95 <200ms, 99.9% uptime, bcrypt cost 12)
9. Same 22 success criteria (SC-1 through SC-22)
10. Same 6 open questions (email dispatch, max tokens, lockout policy, audit format, deletion revocation, REST paths)
11. Same 6 risks with identical severity/likelihood assessments
12. Same external dependency set (jsonwebtoken, bcrypt, email, PostgreSQL, secrets manager, k6, PagerDuty)
13. httpOnly cookie transport for refresh tokens
14. Login rate limiting at 5 requests/min/IP
15. Medium complexity classification (0.6)

## Divergence Points

### 1. Phase Count and Boundaries
- **Opus**: 5 phases (0–4). Phase 0 = infrastructure/schema. Phase 1 = crypto primitives. Phase 2 = service + API. Phase 3 = testing/hardening. Phase 4 = deployment.
- **Haiku**: 4 phases (1–4). Phase 1 = infrastructure + schema + crypto + repositories merged. Phase 2 = domain flows. Phase 3 = API exposure + initial tests. Phase 4 = hardening + release.
- **Impact**: Opus's Phase 0/1 split creates a cleaner gate between "can we access keys/DB" and "are crypto primitives working." Haiku's merge reduces handoff overhead but creates a larger first phase with mixed concerns.

### 2. Component Granularity
- **Opus**: 7 named components (COMP-001 through COMP-007). Repositories, config, and adapters are implicit within service implementations.
- **Haiku**: 15 named components (COMP-001 through COMP-015). Explicitly defines SecretsProvider, UserRepository, RefreshTokenRepository, AuthRateLimiter, ResetEmailAdapter, AuthConfig, AuthFeatureGate, AuthCookiePolicy.
- **Impact**: Haiku's approach creates clearer DI boundaries and independently testable units. Opus's approach reduces task count but leaves internal decomposition to implementer discretion.

### 3. Task Count and Row Density
- **Opus**: 52 task rows with globally sequential numbering (1–52).
- **Haiku**: 45 task rows with per-phase numbering (restarting at 1 each phase).
- **Impact**: Opus's global numbering simplifies cross-phase references. Haiku's per-phase numbering is more readable within each phase but requires phase prefix for unambiguous reference.

### 4. Testing Placement Strategy
- **Opus**: Dedicated Phase 3 for all testing (unit, integration, E2E, load). Tests are separate from implementation phases.
- **Haiku**: Tests distributed across Phase 3 (crypto + service unit, route integration) and Phase 4 (E2E, migration drills). No standalone testing phase.
- **Impact**: Opus's dedicated phase risks delayed defect discovery — bugs found in Phase 3 require rework of Phase 1–2 code. Haiku's distributed approach catches issues closer to implementation but makes test coverage harder to audit as a batch.

### 5. "Route Contract Freezing" vs Handler Implementation
- **Opus**: Defines API handler tasks (API-001 through API-006) as implementation tasks, then separate FR-wiring tasks to validate end-to-end.
- **Haiku**: Separates flow delivery (FR-AUTH.x) from contract freezing (API-00x), treating route contracts as explicit review gates.
- **Impact**: Haiku's contract-freeze pattern forces explicit API design review before implementation proceeds. Opus assumes endpoint design is embedded in the handler task itself.

### 6. Password Reset Priority
- **Opus**: Marks reset endpoints API-005/API-006 as **P1**, and FR-AUTH.5 as **P1**.
- **Haiku**: Marks FR-AUTH.5 as **P0**, treating reset flow as a launch-blocking requirement.
- **Impact**: If reset is truly P1, Opus can ship auth without it. Haiku blocks launch on full reset flow, which is more conservative but delays initial availability.

### 7. Account Lockout Handling
- **Opus**: Includes explicit OPS-007 task for account lockout in Phase 3 (P2 priority, 10 failed attempts, 30min unlock).
- **Haiku**: Defers lockout entirely to open question resolution (OQ-3); no implementation task defined.
- **Impact**: Opus ships a basic lockout even if policy details aren't finalized. Haiku avoids building the wrong policy but leaves a security gap if OQ-3 isn't resolved before launch.

### 8. Timeline Estimates
- **Opus**: 14–19 working days (3–4 weeks).
- **Haiku**: 17–21 working days (~4 weeks).
- **Impact**: 3-day difference in lower bound. Haiku's longer Phase 1 (4–5d vs 2–3d) and longer Phase 4 (4–5d vs 2–3d) account for the gap. Haiku's estimate may be more realistic given the explicit component count.

### 9. Cookie/CORS Policy
- **Opus**: Cookie configuration is implicit in handler tasks (API-001, API-003). No dedicated CORS task.
- **Haiku**: Explicit COMP-015 (AuthCookiePolicy) for httpOnly cookie attributes and CORS headers.
- **Impact**: Cookie misconfiguration is a common security defect. Haiku's explicit component reduces risk of inconsistent cookie handling across endpoints.

### 10. Secrets/Config Validation
- **Opus**: RSA key loading is embedded in JwtService. No explicit config validation component.
- **Haiku**: Explicit COMP-012 (SecretsProvider) and COMP-013 (AuthConfig validator) that checks TTLs, cookie flags, and key presence at boot.
- **Impact**: Haiku catches misconfigurations at startup rather than at first request. Reduces debugging time in multi-environment deployments.

### 11. Migration Recovery
- **Opus**: Down-migration tested as part of MIG-003 in Phase 0. No production recovery drill.
- **Haiku**: Adds TEST-005 migration and recovery drills in Phase 4 (backup-restore, down+up cycle, rollback under flag-off).
- **Impact**: Haiku validates recovery under production-like conditions. Opus validates schema rollback only in isolation.

### 12. Open Question Blocking Phases
- **Opus**: OQ-6 (REST paths) blocks Phase 0. OQ-1 (email dispatch) blocks Phase 2.
- **Haiku**: OQ-6 blocks Phase 2. OQ-2 (max refresh tokens) also blocks Phase 2. OQ-1 blocks Phase 2.
- **Impact**: Opus is stricter — won't start any work until paths are finalized. Haiku allows infrastructure/crypto work to proceed while paths are debated, but must resolve more questions before Phase 2.

### 13. Deployment Specificity
- **Opus**: Explicit deployment runbook (OPS-008), canary at 10% traffic (OPS-009), production validation (OPS-010), full rollout (OPS-011), RSA rotation schedule (OPS-012) — 5 dedicated deployment tasks.
- **Haiku**: Single OPS-005 "Execute feature-flag rollout plan" plus OPS-004 key rotation procedure — 2 tasks covering similar ground at higher abstraction.
- **Impact**: Opus provides a more actionable deployment checklist. Haiku's rollout plan task assumes deployment details will be elaborated in the runbook (DOC-001).

### 14. Documentation
- **Opus**: No explicit documentation task.
- **Haiku**: DOC-001 "Publish auth architecture notes" in Phase 4 (P2).
- **Impact**: Minor. Opus assumes docs emerge from the deployment runbook. Haiku makes it an explicit (if low-priority) deliverable.

### 15. Critical Path Articulation
- **Opus**: Linear critical path: RSA keys → JwtService → TokenManager → AuthService → Middleware → Routes → Integration tests → Feature flag.
- **Haiku**: More granular: includes config/secrets providers and repositories in the chain, plus explicit SLO validation and rollout drill as path nodes.
- **Impact**: Haiku's critical path better reflects actual blocking dependencies. Opus's is simpler to communicate but omits implicit blockers.

### 16. Effort Sizing Consistency
- **Opus**: AuthService is XL. TokenManager is L. Most tasks are M or S.
- **Haiku**: AuthService is L. FR-AUTH.5 (password reset flow) is XL. TokenManager is L.
- **Impact**: Disagreement on where the largest effort concentration lies — Opus sees it in the AuthService orchestrator, Haiku sees it in the reset flow (which includes email integration and multi-step token lifecycle).

## Areas Where One Variant Is Clearly Stronger

**Opus is stronger in:**
- Deployment specificity — 5 granular deployment tasks vs 2
- Global task numbering — unambiguous cross-phase references
- Account lockout — ships a basic policy even at P2, rather than deferring entirely
- Success criteria validation mapping — each SC mapped to a specific test and phase

**Haiku is stronger in:**
- Component decomposition — 15 named, injectable components with explicit file paths create a clearer implementation blueprint
- Config validation at boot — SecretsProvider + AuthConfig catch misconfigurations early
- Cookie/CORS as first-class concern — dedicated component reduces security surface area
- Migration recovery drills — validates rollback under production-like conditions
- Critical path completeness — includes all actual blocking dependencies

## Areas Requiring Debate to Resolve

1. **Testing phase vs distributed testing**: Should tests have their own phase (Opus) or be co-located with implementation (Haiku)? Depends on team structure — a separate QA function favors Opus; integrated devs favor Haiku.

2. **Password reset as P0 vs P1**: Is reset flow launch-blocking? Product owner must decide if auth can ship without password recovery.

3. **Component granularity threshold**: Haiku's 15 components are more precise but create more integration surface. Is the tradeoff worth it for a MEDIUM-complexity project?

4. **Phase 0 separation**: Does splitting infrastructure setup into its own phase (Opus) provide meaningful gating value, or does it just add a handoff for work that takes 2–3 days?

5. **Lockout policy**: Build a basic lockout now (Opus, P2) or wait for product/security alignment (Haiku)? Risk of shipping the wrong policy vs risk of shipping no policy.

6. **Timeline realism**: Opus's 14–19d lower bound assumes infrastructure and crypto can complete in 5–7 combined days. Haiku's 17–21d may better account for secrets manager integration and key provisioning delays. Which estimate should drive planning?
