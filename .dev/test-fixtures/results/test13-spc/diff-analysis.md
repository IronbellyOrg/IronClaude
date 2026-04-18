---
total_diff_points: 12
shared_assumptions_count: 10
---

## Shared Assumptions and Agreements

Both variants converge on the following foundational decisions:

1. **Complexity classification**: MEDIUM (0.6) with architect persona as primary driver.
2. **Token strategy**: RS256 JWT (stateless), with private key in secrets manager and 90-day rotation policy.
3. **Password hashing**: bcrypt cost factor 12, targeting ~250ms hash time (NFR-AUTH.3).
4. **Refresh token model**: Opaque token, SHA-256 hashed in DB, rotated on every refresh, with replay detection triggering revoke-all-for-user.
5. **Storage policy**: Refresh tokens delivered via httpOnly cookie; no localStorage/sessionStorage path.
6. **Rollout gate**: `AUTH_SERVICE_ENABLED` feature flag with phase-1 backward compatibility and phase-2 mandatory auth cutover.
7. **Layered architecture**: AuthService → TokenManager → JwtService, with PasswordHasher as peer utility.
8. **Scope exclusions**: OAuth, MFA, and RBAC deferred to v2.0.
9. **Data model shape**: UserRecord, RefreshTokenRecord, AuthTokenPair with identical field contracts.
10. **Critical blocking open issues**: OI-1 (reset email sync vs queue), OI-2 (refresh token cap), OI-7/email provider selection must resolve before downstream milestones.

## Divergence Points

**1. Milestone count and timeline granularity**
- Opus: 6 milestones, 12 weeks total, one milestone per capability cluster.
- Haiku: 4 milestones, 8 weeks total, broader milestone scope with multiple capabilities per milestone.
- Impact: Opus provides finer-grained gating and handoff checkpoints at higher planning overhead; Haiku yields faster nominal delivery but larger batch sizes per milestone reduce rollback precision.

**2. Foundation milestone scope (M1)**
- Opus: Dedicated M1 to data layer, repositories, RSA keys, secrets manager, library pinning only — no cryptographic services.
- Haiku: M1 bundles foundation + JwtService + PasswordHasher + route flag gating + NFR-AUTH.3 validation.
- Impact: Opus permits clean "foundation-only" gate before any crypto code; Haiku front-loads M1 risk with cryptographic primitives but eliminates a milestone boundary.

**3. Cryptographic services as standalone milestone**
- Opus: M2 dedicated to JwtService, PasswordHasher, TokenManager, and RSA key rotation runbook (OPS-006).
- Haiku: Distributes these across M1 (primitives) and M2 (TokenManager only).
- Impact: Opus isolates crypto contract lock before flow work begins; Haiku couples TokenManager to the issuance endpoints.

**4. Password reset flow positioning**
- Opus: Dedicated M5 (Password Reset Flow) — fully isolated from refresh lifecycle.
- Haiku: Bundled into M3 alongside refresh rotation and replay detection.
- Impact: Opus treats reset as P1 and can defer it independently; Haiku ships refresh + reset atomically but raises M3 risk profile (rated HIGH).

**5. Wiring, rollout, and validation as dedicated milestone**
- Opus: Dedicated M6 with APM, PagerDuty, k6 load tests, E2E lifecycle, feature-flag rollback rehearsal, rollout runbook.
- Haiku: Folded into M4 (Integration hardening and rollout readiness) alongside deferred gap resolution (GAP-1/2/3) and OI-2 decisions.
- Impact: Opus cleanly separates build-complete from ship-ready; Haiku conflates backlog/deferred-gap triage with go-live readiness.

**6. Open issue resolution timing**
- Opus: Flags OI-1, OI-7, and endpoint paths (OI-6) as pre-M5 blockers, with endpoint paths resolved in M2 contract lock.
- Haiku: Schedules OI-1 within M3 as a deliverable (decision made during implementation) and OI-2 within M4.
- Impact: Opus treats OI resolution as gate; Haiku treats it as in-flight deliverable, accepting schedule compression risk.

**7. Security-specific deliverable tracking**
- Opus: Explicit SEC-xxx IDs (SEC-001 through SEC-006) for password policy, email validator, refresh rotation, profile sanitization, reset TTL, invalidate-all.
- Haiku: Rolls these into COMP-011 through COMP-018 and general FR implementations; no SEC-prefixed tracking.
- Impact: Opus supplies stronger traceability for security-review and audit purposes; Haiku simpler but less explicitly auditable.

**8. Test coverage enumeration**
- Opus: 20+ individually-numbered TEST-M*-xxx deliverables per milestone, each with acceptance criteria.
- Haiku: 3 consolidated test suites (TEST-001/002/003) scoped per milestone.
- Impact: Opus makes test gaps visible at standup granularity; Haiku reduces bookkeeping at risk of hidden coverage gaps.

**9. Risk severity weighting per milestone**
- Opus: M2 and M4 flagged HIGH risk (crypto correctness, refresh replay race).
- Haiku: M2, M3, M4 flagged HIGH risk (broader scope per milestone).
- Impact: Opus pinpoints two highest-attention milestones; Haiku signals sustained elevated risk across three consecutive milestones.

**10. Rate limiter and password policy positioning**
- Opus: Password policy (SEC-001), email validator (SEC-002), rate limiter (OPS-003) are distinct M3 deliverables.
- Haiku: Bundled as COMP-011 (rate limiter), COMP-012 (registration validator) within M2.
- Impact: Both cover the same ground; Opus permits separate ownership assignment; Haiku aligns with a single-team-per-milestone model.

**11. Deferred gap handling (GAP-1, GAP-2, GAP-3)**
- Opus: Treats as risk-register entries (R4, R5, R12) with mitigations in the risk table; no milestone deliverable.
- Haiku: Creates explicit M4 planning deliverables (GAP-1, GAP-2, GAP-3) producing owned v1.1 plans.
- Impact: Haiku forces explicit ownership/handoff documentation; Opus relies on risk-register discipline, lower ceremony but higher forget-risk.

**12. Email service integration timing**
- Opus: EmailService (COMP-010) and email provider selection (DEP-003) live entirely in M5 with OI-7 as pre-M5 blocker.
- Haiku: EmailService integration in M3 alongside refresh rotation, with sync/queue decision (OI-1) in-flight.
- Impact: Opus enforces provider selection up front, reducing M5 scope uncertainty; Haiku accepts concurrent decision-and-implementation at higher rework risk.

## Areas Where One Variant is Clearly Stronger

**Opus is stronger in:**
- **Gating discipline**: Six milestones with explicit entry/exit create cleaner stop-the-line points, reducing blast radius on rollback.
- **Security auditability**: Dedicated SEC-xxx IDs, explicit replay race-condition tests (TEST-M4-002 includes concurrent refresh), Set-Cookie attribute contract tests.
- **Production readiness ceremony**: M6 includes feature-flag rollback rehearsal (TEST-M6-002), canary 5% deploy with APM watch, explicit rollout runbook (OPS-007).
- **Test granularity**: Per-test acceptance criteria allow precise PR-level coverage gating.

**Haiku is stronger in:**
- **Calendar velocity**: 8-week plan vs. 12 weeks; significantly faster nominal time-to-production if scope holds.
- **Deferred-gap ownership**: Explicit GAP-1/2/3 deliverables force assigned owners for v1.1 handoff rather than relying on risk-register follow-through.
- **Milestone economy**: Fewer handoffs reduce coordination tax between teams.
- **Convergence tracking**: Includes `convergence_score: 0.84` metadata, signaling awareness of variant fidelity as a first-class concern.

## Areas Requiring Debate to Resolve

1. **Delivery cadence vs. gating density** (Divergence #1, #3, #5): 12-week six-milestone plan vs. 8-week four-milestone plan — trade-off between rollback precision and time-to-value. Requires stakeholder decision on risk tolerance.
2. **Refresh + Reset coupling** (Divergence #4): Should reset flow share a milestone with refresh rotation, or be isolated? Depends on whether reset is P0 or P1 for launch.
3. **Crypto services milestone isolation** (Divergence #2, #3): Whether cryptographic primitives warrant their own gated milestone or are sufficiently bounded as foundation work.
4. **OI resolution timing** (Divergence #6, #12): Pre-milestone blockers (Opus) vs. concurrent in-flight decisions (Haiku) — depends on maturity of product/ops decision cadence.
5. **Deferred gap formalization** (Divergence #11): Risk-register entries vs. explicit v1.1 planning deliverables — affects how strongly v1.1 handoff is enforced.
6. **Test enumeration style** (Divergence #8): Fine-grained TEST-M*-xxx tracking vs. consolidated suites — process overhead vs. coverage visibility.
