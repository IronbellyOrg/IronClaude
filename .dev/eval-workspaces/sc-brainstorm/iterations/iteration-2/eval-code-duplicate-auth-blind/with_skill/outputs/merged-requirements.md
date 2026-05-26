---
spec_type: requirements
domain: code
strategy: systematic
adversarial_status: pass
convergence_score: 0.71
proposal_count: 5
source_proposals: [proposal-1-agent-A, proposal-2-agent-B, proposal-3-agent-C, proposal-4-agent-D, proposal-5-agent-E]
debate_transcript: ./adversarial/debate-transcript.md
source_seed: ../seed-brief.md
blind_mode: true
---

# Merged Requirements: Consolidate Three Duplicate Auth Modules

## Problem Statement

Three independently-evolved auth modules (`services/web/src/auth/legacy_login.py`, `services/api/src/auth/api_login.py`, `services/mobile_bff/src/auth/mobile_login.py`) have produced two CVE-asymmetry security incidents in the last year and a compliance finding ("inconsistent auth controls across services") in the last audit cycle. Forcing function: next compliance audit cycle at end of Q3. The remediation is a shared `services/shared/auth_core/` module that owns the *primitive-level* policies and audit emission (eliminating the documented drift sources) while leaving protocol-specific flow code in each service's repo (CSRF in web, OAuth2 PKCE in mobile, api-key HMAC in api). Migration runs per-service with shadow → 5% → 50% → 100% phases gated by an explicit promotion checklist; lockout state is unified from Phase 0; audit emission dual-writes to legacy and unified streams for 90 days. Migration of auth IS an auth change: pre-migration and per-cutover pentests are blocking checklist items, not advisory. Test surface is the load-bearing engineering investment alongside the architecture itself.

## Constraints

- **C1** — Zero forced re-login during migration. *(seed Q4)*
- **C2** — Session and token wire formats unchanged. *(seed Q4)*
- **C3** — Login latency P99 ≤ 80ms post-consolidation across all three services. *(seed Q4)*
- **C4** — Audit log: unified stream + 90-day legacy-destination overlap + 7-year retention preserved. *(seed Q11)*
- **C5** — Each service migrates independently; no big-bang. *(seed Q10)*
- **C6** — All current behavior preserved OR delta documented with explicit security review sign-off. *(seed Q5)*
- **C7** — `services/shared/security_utils/` stays as-is — consumed by new core, not replaced. *(seed Q6 + enrichment)*
- **C8** — Forcing function: at least mid-migration with documented plan before end-of-Q3 compliance cycle. *(seed Q9)*

## Functional Requirements

- **FR1** — **Single source of truth for policies**: `services/shared/auth_core/policy.py` owns password_policy, lockout_policy, jwt_validation, audit_event_schema. All three services import. *(Agent B core, Agent A concession-1 override-registry attached)*
- **FR2** — **Override registry**: any per-service deviation from a core policy requires a named entry in `services/shared/auth_core/overrides.yaml` with a security-review-sign-off field. Config load fails on unregistered override. Quarterly review auto-expires unsigned overrides. *(Agent A concession-1, Agent E O8)*
- **FR3** — **Unified audit emitter** at `services/shared/auth_core/audit_emitter.py`. CloudEvents-shaped events to one Kafka topic. Three legacy-shim consumers (CloudWatch / Splunk / S3) consume from Kafka and re-emit during the 90-day overlap. *(Agent A concession-2, Agent B compatible)*
- **FR4** — **Lockout store unification from Phase 0**: new core writes to and reads from the existing `security_utils/lockout.py` Redis store. No new lockout store is introduced; web's custom-Redis lockout implementation is deleted in favor of the canonical one. *(Agent C C1, Agent D test coverage)*
- **FR5** — **Audit dual-write with idempotency UUIDs** during 90-day overlap. Each event carries a UUID; reconciliation across legacy and unified streams must show zero gap before legacy decommission. *(Agent C C2, Agent E O7)*
- **FR6** — **Shadow-mode runner with delta detection**. Pumps recorded production-shape requests (~50K corpus per service, anonymized, including Incident 1 and Incident 2 input patterns) through both old and new paths; asserts identical outcome, identical lockout-counter side effects, identical audit-event content (modulo timestamps/IDs), latency delta within ±10%. Sensitive data redacted at the runner before any logging. *(Agent D test plan, Agent C C3)*
- **FR7** — **Per-service feature flags with sub-flag granularity**: `auth_core_enabled`, `auth_core_canary_percent` (0-100), `audit_dual_write`, `shadow_mode_active`, `lockout_store_unified`. Default values reviewed by EM before each phase promotion. *(Agent E O1)*
- **FR8** — **Promotion checklist as code artifact**: `services/shared/auth_core/promotion-checklists/<phase>.yaml`. Each phase has pre-promotion, in-flight, and post-promotion checks. Promotion gated by checklist execution. *(Agent E O2)*
- **FR9** — **Dashboards exist BEFORE Phase 0 builds begin**: login-success-rate, login-latency P50/P99, lockout-counter-divergence, audit-stream-divergence, per-flow error rate, per-service vs. unified comparison views. All panels have named owners. *(Agent E O3)*
- **FR10** — **Per-phase runbook entries** for each promotion event: rollback procedure, kill-switch path, expected dashboard signature. Reviewed at PR time. *(Agent E O4)*
- **FR11** — **Pre-migration + per-cutover pentest** (≥4 engagements total). Findings ≥ MEDIUM block phase promotion. *(Agent C C4, Agent D AC-T6)*
- **FR12** — **Compliance attestation mapping table**: per-policy before/after table (web before / api before / mobile before → unified) signed off by compliance. Becomes part of the Q3 audit packet. *(Agent C C5)*
- **FR13** — **Migration ordering: api → web → mobile**. Unanimous across all five proposals. *(debate Tension 5)*

## Non-Functional Requirements

- **NFR1** — **Performance**: login latency P99 ≤ 80ms across all three services post-migration; verified in staging-shape load test before each canary phase. *(C3 + Agent D AC-T7)*
- **NFR2** — **Test coverage**: new core ≥95% line + branch. ≥120 unit cases, ≥150 contract cases across service↔core boundaries, ≥90 integration cases, ≥30 E2E scenarios per service. *(Agent D)*
- **NFR3** — **Audit reconciliation**: zero gap between legacy stream and unified stream at the 90-day reconciliation gate. *(C4 + Agent E O7)*
- **NFR4** — **Drift prevention is structural**: a CVE in any auth dependency must be patchable in one PR and deployed to all three services in a single release. *(seed success criteria)*
- **NFR5** — **No new login-latency outliers above the P99 budget** during any canary phase. *(Agent C C4 sub-criterion)*
- **NFR6** — **Shadow-mode delta**: zero delta on the 50K corpus before any service exits shadow mode. *(Agent D AC-T4)*
- **NFR7** — **Sensitive-data redaction in shadow-mode runner**: no raw passwords, tokens, or session IDs in logs. *(Agent C C3)*

## Acceptance Criteria

- **AC1** — All ≥120 unit cases green; coverage on new core ≥95% line + branch. *(Agent D AC-T1)*
- **AC2** — All ≥150 contract cases green; no version-bump pending against a consumer. *(Agent D AC-T2)*
- **AC3** — All ≥90 integration cases green; Redis-unavailable scenario exercises documented behavior. *(Agent D AC-T3)*
- **AC4** — Shadow-mode runner shows zero deltas on 50K-request corpus for each service before that service exits shadow. Lockout-counter side-effect deltas explicitly checked. *(Agent D AC-T4 + Agent C C1)*
- **AC5** — All ≥30 E2E scenarios green per service against real client SDKs in staging. *(Agent D AC-T5)*
- **AC6** — Pre-migration pentest + per-cutover pentest findings ≤ LOW before each promotion. *(Agent D AC-T6 + Agent C C4)*
- **AC7** — Login latency P99 ≤ 80ms across all three services post-migration. *(NFR1)*
- **AC8** — Audit dual-write reconciliation: zero gap between legacy and unified streams at the 90-day gate. Legacy decommission blocked until this is verified. *(NFR3 + Agent E O7)*
- **AC9** — Compliance attestation mapping table signed by compliance team before the Q3 audit cycle. *(FR12)*
- **AC10** — Three legacy auth modules **deleted** (not just deprecated) by end of migration. *(seed success criteria)*
- **AC11** — All operational scaffolding (FR7-FR10) in place before Phase 1 service-migration begins. *(Agent E)*

## Risks

- **R1** (severity: HIGH) — **Migration introduces a subtle auth weakness during shadow/canary.** Two code paths in parallel = a new class of risk that doesn't exist in either end state alone. *Mitigation*: FR4 (unified lockout store from Phase 0), FR5 (audit dual-write with UUIDs), FR11 (pre-migration + per-cutover pentest), FR6 (shadow-mode delta detection with explicit lockout-counter side-effect checking).
- **R2** (severity: HIGH) — **90-day audit overlap finds reconciliation gaps.** S3 eventual-consistency reads may produce phantom missing events during reconciliation. *Mitigation*: FR5 idempotency UUIDs + retries + Agent E O7 hard timer reset if reconciliation fails; budget for overlap extension if needed.
- **R3** (severity: MEDIUM) — **Override registry becomes a rubber-stamp.** Risk that security-review sign-off becomes pro-forma and drift returns. *Mitigation*: FR2 quarterly auto-expiry of unsigned overrides; EM review of registry before each quarter.
- **R4** (severity: MEDIUM) — **Test development underestimated.** ~8 engineer-weeks of test development is the median estimate; corpus collection for shadow mode may be longer if rare-error paths require synthetic augmentation. *Mitigation*: Phase 0 includes corpus collection and surface explicitly; do not start Phase 1 if corpus shows < 90% production-shape coverage.
- **R5** (severity: MEDIUM) — **Promotion checklist becomes ceremonial.** Risk that checks become "click through" rather than meaningful gates. *Mitigation*: each phase's post-promotion check requires 24h of clean signal before next phase; on-call (not the migrator) signs off.
- **R6** (severity: LOW) — **Plugin-framework deferred decision becomes never.** If SAML/OIDC need emerges later, the per-service flow code we kept here is harder to refactor into a plugin shape. *Mitigation*: deferred-decision documented; revisit in 12 months post-migration completion.
- **R7** (severity: LOW) — **Mobile S3 audit stream durability semantics differ from CloudWatch and Splunk.** Eventual-consistency may produce reconciliation noise that is not actually a gap. *Mitigation*: per-stream reconciliation tolerance windows documented in FR5 implementation.

## Open Questions

- **OQ1** — **"Security review" definition for override-registry sign-off**: which team or role specifically? Operationalize in Phase 0. *(debate Tension carry-over)*
- **OQ2** — **Shadow corpus augmentation strategy**: if production traffic alone covers < 90% of rare-error paths, what's the synthetic-augmentation approach? *(Agent D confidence note)*
- **OQ3** — **Per-service flow code future extraction**: if SAML/OIDC need emerges within 12 months of migration completion, do we extract a plugin framework then (Agent A's path), or extend per-service code (Agent B's path)? *(deferred decision)*
- **OQ4** — **Pentest cadence beyond 4 engagements**: is annual pentest of the unified core sufficient post-migration, or does each major dependency upgrade trigger a fresh pentest? *(Agent C carried forward)*

## Out of Scope (explicit)

- Replacing `services/shared/security_utils/` (Argon2id, JWT, lockout) — stays as-is.
- Net-new auth flows (SAML, OIDC, hardware-key WebAuthn beyond current biometric step-up) — out of scope; deferred to future product decisions.
- Refactoring of downstream services that validate sessions/tokens — wire-format compatibility means no changes needed there.
- Multi-tenant per-tenant policy customization — out of scope; current single-tenant policy structure preserved.

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (single source of truth for policies) | Agent B core proposal; debate Tension 1 resolution |
| FR2 (override registry) | Agent A concession-1; Agent E O8 quarterly review |
| FR3 (unified audit emitter via Kafka) | Agent A concession-2; Agent B compatible |
| FR4 (unified lockout store from Phase 0) | Agent C C1; Agent D test coverage |
| FR5 (audit dual-write with UUIDs) | Agent C C2; Agent E O7 |
| FR6 (shadow-mode runner with delta detection) | Agent D test plan; Agent C C3 redaction |
| FR7 (sub-flag feature flags) | Agent E O1 |
| FR8 (promotion checklist as code) | Agent E O2 |
| FR9 (dashboards before code) | Agent E O3; billing_core post-mortem lesson |
| FR10 (per-phase runbook entries) | Agent E O4 |
| FR11 (pre + per-cutover pentest) | Agent C C4; Agent D AC-T6 |
| FR12 (compliance attestation mapping) | Agent C C5 |
| FR13 (api → web → mobile ordering) | Unanimous; debate Tension 5 |
| NFR1-NFR7 | Cross-cutting from seed constraints + agents' acceptance criteria |
| AC1-AC11 | Mapped above |
| R1 (migration-as-auth-change risk) | Agent C central thesis |
| R2 (90-day reconciliation gaps) | Agent E O7 + enrichment S3 eventual-consistency |
| R3 (override registry rubber-stamping) | Agent A concession-1 own risk |
| R4 (test development underestimate) | Agent D confidence note |
| R5 (checklist becomes ceremonial) | Agent E O2 risk |
| R6 (plugin-framework deferred) | Agent A→B concession risk |
| R7 (S3 durability semantics) | Enrichment + Agent E O7 |
| OQ1-OQ4 | Debate tensions remaining + agents' open notes |
