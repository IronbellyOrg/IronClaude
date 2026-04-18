---
high_severity_count: 2
medium_severity_count: 8
low_severity_count: 3
total_deviations: 13
validation_complete: true
tasklist_ready: false
---

## Deviation Report

**DEV-001** | HIGH | Audit log retention period contradicts TDD.
- Source Quote (TDD §7.2): `Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days`
- Roadmap Quote: `NFR-COMP-002 | Retain audit logs 12 months ... retain:12mo`
- Impact: Storage sizing (OPS-011, infra cost), retention policy tests (TEST-014), and SOC2 evidence scope are all built against 12 months while TDD mandates 90 days. Implementation will either violate TDD or over-retain. (Roadmap acknowledges this via OQ-003 but still commits the 12-month value.)
- Recommended Correction: Resolve OQ-003 before Phase 1 begins; update TDD §7.2 to 12 months (if PRD wins) or revert NFR-COMP-002 to 90 days. Reflect result in DM-003, TEST-014, and infra cost estimate.

**DEV-002** | HIGH | TDD Open Questions OQ-001 and OQ-002 are entirely absent from the roadmap.
- Source Quote (TDD §22): `OQ-001 | Should AuthService support API key authentication for service-to-service calls? ... Target 2026-04-15` and `OQ-002 | What is the maximum allowed UserProfile roles array length? ... Target 2026-04-01`
- Roadmap Quote: [MISSING] — roadmap's 12 open questions list does not contain these two items.
- Impact: OQ-001 shapes Sam (API consumer) persona resolution and affects COMP-001/API-001 auth surface; OQ-002 constrains DM-001 roles column sizing and FR-AUTH-004 response. Dropping them removes a forcing function for scheduled resolution.
- Recommended Correction: Add OQ-001 (API-key auth scope) and OQ-002 (roles[] max length) to the roadmap Open Questions with owners (auth-team, product) and pre-Phase-1 target dates.

**DEV-003** | MEDIUM | Roadmap adds endpoint POST `/auth/logout` not present in TDD §8 API Specifications.
- Source Quote (TDD §8.1): only lists `POST /auth/login`, `POST /auth/register`, `GET /auth/me`, `POST /auth/refresh` (plus reset endpoints referenced in FR-AUTH-005). No logout endpoint.
- Roadmap Quote: `API-007 | Implement POST /auth/logout endpoint ... PRD-gap-fill:TDD-update-needed`
- Impact: Roadmap transparently flags as a TDD gap, but implementation begins without a locked TDD contract for request/response shape, revocation semantics, or audit payload. Risks schema drift between FR-AUTH-006 and TDD.
- Recommended Correction: Update TDD §8 to add POST `/auth/logout` (request body, 204/200 response, `TokenManager.revoke()` semantics, audit event `logout`) before API-007 begins coding. Close OQ-004 and OQ-011.

**DEV-004** | MEDIUM | Roadmap adds endpoint GET `/admin/auth-events` not present in TDD §8.
- Source Quote (TDD §8): no admin endpoint defined; TDD §14 only describes metrics and structured logs, no admin query API.
- Roadmap Quote: `API-008 | Implement GET /admin/auth-events ... PRD-Jordan-persona-gap-fill`
- Impact: Admin endpoint is a first-class auth surface (authZ, pagination, PII exposure) but has no TDD specification. Risk of under-specified security boundary on an admin-only route.
- Recommended Correction: Add an API spec entry in TDD §8 covering admin role check, response schema mirroring DM-003, pagination contract, and rate-limit posture. Close OQ-005 and OQ-012.

**DEV-005** | MEDIUM | Roadmap introduces schemas DM-004 `ConsentRecord`, DM-005 `PasswordResetToken`, DM-006 `AuthSecurityState` not defined in TDD §7 Data Models.
- Source Quote (TDD §7.1): only `UserProfile` and `AuthToken` interfaces are defined; §7.2 names an "Audit log" store with no schema, and reset-token/lockout state are not modeled.
- Roadmap Quote: `DM-004 Define ConsentRecord schema ... DM-005 Define PasswordResetToken schema ... DM-006 Define AuthSecurityState schema`
- Impact: These schemas are required to satisfy FR-AUTH-005 (reset token lifecycle), NFR-COMP-001 (GDPR consent policyVersion), and FR-AUTH-001 (lockout state), but TDD has no canonical field list. Implementation will create de-facto schemas without TDD review.
- Recommended Correction: Extend TDD §7 with formal schemas (fields, constraints, TTLs) for consent records, reset tokens, and auth security state before Phase 1 schema deployment.

**DEV-006** | MEDIUM | Roadmap introduces components `ConsentRecorder`, `ResetTokenStore`, `LockoutPolicy`, `AuditLogger` not listed in TDD §10 Component Inventory.
- Source Quote (TDD §10): shared components list contains only `LoginPage`, `RegisterPage`, `AuthProvider`; backend components are only `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo` (implied by §6.1 diagram).
- Roadmap Quote: `COMP-010 ConsentRecorder ... COMP-011 ResetTokenStore ... COMP-012 LockoutPolicy ... COMP-013 AuditLogger`
- Impact: Required behaviors (consent capture, lockout, audit emission) exist in TDD as prose but lack a component boundary. Implementation may collapse them into `AuthService` or fan them out inconsistently vs. roadmap.
- Recommended Correction: Update TDD §10 to declare these modules explicitly with ownership, inputs/outputs, and dependencies so roadmap COMP-010–013 match TDD contracts.

**DEV-007** | MEDIUM | Unit test coverage target inconsistent between TDD and roadmap.
- Source Quote (TDD §15.1 and §24.1): `Unit | 80% | Jest, ts-jest` and `Unit test coverage for AuthService, TokenManager, JwtService, and PasswordHasher exceeds 80%`
- Roadmap Quote (Timeline Estimates row, Phase 2): `unit+integration tests ≥85%`
- Impact: Different exit-gate thresholds may cause Phase 2 to appear failing when TDD's 80% is actually met, or allow under-testing relative to a stricter bar the team never agreed to.
- Recommended Correction: Align on one number — either hold to TDD's 80% or formally raise to 85% in TDD §15/§24.

**DEV-008** | MEDIUM | Total timeline exceeds TDD milestone schedule.
- Source Quote (TDD §23.1): milestones M1 2026-04-14 through M5 2026-06-09 — approximately 10 weeks end-to-end.
- Roadmap Quote: `total_phases: 5 ... Total estimated duration: 13 weeks sequential (default schedule)` with a "Compressed alternative (10 weeks)" noted.
- Impact: Default 13-week plan slips the GA target (M5: 2026-06-09) that TDD commits to; personalization roadmap dependency and SOC2 Q3 2026 audit may shift.
- Recommended Correction: Make the 10-week compressed plan the default, or renegotiate M5 in TDD §23.1 and update downstream personalization scheduling.

**DEV-009** | MEDIUM | Internal inconsistency: phase durations in headings disagree with Timeline Estimates table.
- Source Quote (TDD §23): implicit total ~10 weeks across 5 milestones.
- Roadmap Quote: Phase headings state `Phase 1: 2 weeks (Weeks 1–2)`, `Phase 2: 3 weeks (Weeks 3–5)`, `Phase 3: 2 weeks (Weeks 6–7)`, `Phase 4: 2 weeks (Weeks 8–9)`, `Phase 5: 4 weeks (Weeks 10–13)` — but the Timeline Estimates table lists `Phase 1 | 3 weeks | W01 | W03`, `Phase 2 | 3 weeks | W04 | W06`, `Phase 3 | 3 weeks | W07 | W09`, `Phase 4 | 2 weeks | W10 | W11`, `Phase 5 | 2 weeks | W12 | W13`.
- Impact: Two conflicting schedules in the same document; planning, resourcing, and dependency sequencing become ambiguous.
- Recommended Correction: Pick one schedule and reconcile phase headings with the Timeline Estimates table; remove the duplicate representation or sync both.

**DEV-010** | MEDIUM | Roadmap Open Questions OQ-001 (OAuth) and OQ-002 (MFA) relitigate TDD Non-Goals.
- Source Quote (TDD §3.2): `NG-001 | Social/OAuth login | Deferred to v1.1` and `NG-002 | Multi-factor authentication | Planned for v1.2 as a separate feature`
- Roadmap Quote: `OQ-001: Should social login (Google/GitHub OAuth) be in scope for v1 GA or deferred to v1.1?` and `OQ-002: MFA strategy — TOTP only, WebAuthn, or both for v1?`
- Impact: Re-opens decided scope. Creates ambiguity and risks silent scope creep (roadmap notes OQ-001 could add "2–3 weeks").
- Recommended Correction: Close OQ-001 and OQ-002 against TDD NG-001/NG-002 ("deferred to v1.1 / v1.2") or, if reconsidering, formally amend TDD §3.2 first.

**DEV-011** | LOW | Extra Prometheus metric `auth_reset_total` beyond TDD §14.
- Source Quote (TDD §14): `auth_login_total (counter), auth_login_duration_seconds (histogram), auth_token_refresh_total (counter), auth_registration_total (counter)`
- Roadmap Quote: `OPS-010 ... auth_reset_total:counter`
- Impact: Additional useful metric aligned with FR-AUTH-005 but extends TDD's explicit list. Minor.
- Recommended Correction: Add `auth_reset_total` to TDD §14 metrics list for traceability.

**DEV-012** | LOW | TDD Timeline milestone dates (M1–M5) are not carried into the roadmap.
- Source Quote (TDD §23.1): `M1: Core AuthService | 2026-04-14 ... M5: GA Release | 2026-06-09`
- Roadmap Quote: Timeline uses relative weeks `W01–W13`; no calendar anchoring.
- Impact: Harder to reconcile against TDD committed release date and Q3 2026 SOC2 audit constraint.
- Recommended Correction: Anchor roadmap week numbers to absolute dates or annotate each phase with the corresponding TDD milestone ID.

**DEV-013** | LOW | Complexity score and class computed at 0.65 MEDIUM not reflected back into TDD frontmatter.
- Source Quote (TDD frontmatter): `complexity_score: ""` and `complexity_class: ""`
- Roadmap Quote: `complexity_score: 0.65 ... complexity_class: MEDIUM`
- Impact: TDD advises these are computed by `sc:roadmap`; leaving TDD blank is allowed but roundtrip traceability is weaker.
- Recommended Correction: Optionally write the computed values back to TDD frontmatter for cross-document traceability.

## Summary

Validation complete. 13 total deviations found: 2 HIGH, 8 MEDIUM, 3 LOW. The roadmap is **not tasklist-ready**. Two blockers must be resolved before tasklist generation:

1. **Audit-retention contradiction** (DEV-001) — TDD's 90-day commitment conflicts with the roadmap's 12-month retention. OQ-003 must be closed and one source updated before DM-003, NFR-COMP-002, and TEST-14 are locked.
2. **Dropped TDD Open Questions** (DEV-002) — OQ-001 (API-key auth) and OQ-002 (roles[] max length) are omitted from the roadmap; they must be carried forward with owners and target dates.

The MEDIUM cluster centers on scope extensions (logout endpoint, admin auth-events endpoint, three extra schemas, four extra components) that the roadmap correctly adds to satisfy the PRD but that the TDD has not yet absorbed. TDD updates in §7, §8, and §10 are needed for full bidirectional consistency. Internal roadmap consistency issues (phase-duration mismatch, timeline vs TDD milestones) and relitigation of TDD non-goals (OAuth/MFA as open questions) also sit at MEDIUM and should be resolved before Phase 1 entry.
