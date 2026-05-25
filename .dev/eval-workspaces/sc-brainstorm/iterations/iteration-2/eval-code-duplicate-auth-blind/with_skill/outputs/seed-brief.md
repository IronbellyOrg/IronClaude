---
topic: "consolidate three duplicate auth modules"
domain: code
strategy: systematic
depth: deep
proposal_count: 5
handoff_target: none
blind_mode: true
created: 2026-05-25T00:00:00Z
---

# Seed Brief: code-duplicate-auth-blind

> **NOTE — `--blind` mode.** Per SPEC §11.1 case 11, this run anonymizes model identifiers throughout. Proposals and the debate transcript label sources as **Agent A / Agent B / Agent C / Agent D / Agent E** rather than by model alias. The return contract's `agent_spec` field discloses the anonymization but not the per-agent mapping. Mapping (for post-hoc grader use only): `blind_mapping_path: ../blind-mapping.yaml` exists but is not loaded during scoring. This validates that the debate signal is real-disagreement, not "model X agreeing with model X" pseudo-diversity.

## Socratic Dialogue Record (code-domain DEEP tier — 12 questions, Clarify + Validate + Audit batches)

### Clarify batch

**Q1. What's the entry point — three specific files, or three logical modules?**
A: Three logical modules across three services that grew independently. (a) `services/web/src/auth/legacy_login.py` (the original, 2019, supports session-cookie + CSRF + a custom CAPTCHA hook), (b) `services/api/src/auth/api_login.py` (added 2021 when REST API split off, supports API-key + OAuth2 client_credentials), (c) `services/mobile_bff/src/auth/mobile_login.py` (added 2023, supports OAuth2 PKCE + biometric step-up). All three call into the same User table and the same Sessions table but with different abstractions and different cache strategies on top.

**Q2. What's the scope — single-module change, cross-module refactor, or new subsystem?**
A: Cross-module refactor with subsystem implications. The end state should be ONE auth core (call it `services/shared/auth_core/`) consumed by all three services as a library, with each service retaining a thin service-specific entry-point for protocol-specific concerns (session cookie vs. bearer token vs. PKCE flow). Not a microservice extraction — a shared library.

**Q3. What failure mode are we trying to prevent / behavior to add?**
A: Two failure modes. (a) Security drift: a CVE patch lands in one of the three but not the others; we've had two incidents like this in the last year. (b) Bug drift: subtle differences in CSRF handling, password-policy enforcement, and lockout logic produce inconsistent UX and audit-trail gaps that compliance is starting to flag.

**Q4. What are the non-negotiable constraints from existing code (API stability, perf, backward compat)?**
A: (i) Zero customer-visible auth disruption — no forced re-login during migration. (ii) Session and token formats must remain wire-compatible (downstream services validate sessions/tokens; changing the format breaks them). (iii) Performance: login latency budget P99 ≤ 80ms (current is ~65ms web, ~50ms api, ~95ms mobile). (iv) Audit logs from all three must be preservable as-is and the new core's audit must be a superset.

**Q5. What does "done" look like?**
A: Three services consume the shared core; the three legacy modules are deleted (not just deprecated); all current behavior preserved or explicitly delta-documented; security drift is structurally impossible because there is only one CSRF implementation, one lockout implementation, one password-policy check; full audit trail is consolidated and queryable across all three services.

### Validate batch

**Q6. Are there existing implementations this should align with or replace?**
A: Three to replace. There is also a `shared/security_utils/` module (~2K LOC) that contains some genuinely shared primitives (password hashing via Argon2id, JWT signing/verification, the rate-limit-friendly lockout logic added last year). That code stays; the new auth core consumes from it.

**Q7. Who consumes this — internal callers or external?**
A: Internal callers only at the auth-core boundary (the three services). External-facing surfaces remain the existing service endpoints (URLs, request/response shapes do not change). Internal consumers: web frontend (session-cookie flow), iOS + Android (PKCE flow), public REST API (api-key + OAuth2 client_credentials), internal microservices (signed JWT validation only — no login).

**Q8. What's the test surface?**
A: Unit + contract + integration + e2e + security. Unit: each module within auth_core. Contract: each service↔auth_core boundary has a typed contract test (Pact-style or equivalent). Integration: each service with the real auth_core hitting a test User database. E2E: real login flows from real client SDKs against staging. Security: STRIDE review, third-party pentest at end of phase, fuzzing on the public-facing parsers (OAuth2 redirect handling, PKCE code_verifier handling).

**Q9. Is there a deadline / forcing function?**
A: Yes — soft deadline next quarter. Forcing function: compliance audit cycle starts at end of Q3 and they have flagged "inconsistent auth controls across services" as a finding from the last cycle. If we are not at least mid-migration with a documented plan, the finding repeats.

**Q10. What's the rollback / safety plan?**
A: Phased rollout. Each service migrates independently. Within a service: shadow-mode (both old and new auth paths run, results compared, neither canonical) for 1 week → canary at 5% traffic for 1 week → 50% for 1 week → 100%. Per-service kill switch at every phase. Rollback to old module possible until the old module is deleted (last step of the migration for each service).

### Audit batch (deep tier additions)

**Q11. Audit log preservation — what does "preservable" actually require?**
A: Every login attempt — success or fail — is currently logged to a service-specific destination (web → CloudWatch, api → Splunk, mobile → a separate S3 stream). Compliance requires 7-year retention. The new core MUST emit a unified audit event AND continue writing to the legacy destinations during a 90-day overlap so existing investigations (which are mid-flight) continue to function. After 90 days, the unified stream becomes canonical and the legacy destinations stop receiving.

**Q12. Security drift CVE timeline — what does the post-mortem on those two incidents tell us?**
A: Incident 1 (Oct 2024): JWT-library CVE patched in `services/api` within 48h, in `services/web` after 11 days because the team didn't realize they used the same library. Incident 2 (Feb 2025): a password-policy update (length requirement bump) landed in web and api but not mobile, so mobile users could continue using newly-short-of-policy passwords for 4 months until a quarterly audit caught it. Both are structurally impossible if there is one core.

## Problem Statement

Three auth modules — `legacy_login.py` (web, 2019), `api_login.py` (api, 2021), `mobile_login.py` (mobile_bff, 2023) — grew independently and now produce security drift (two CVE-patch-asymmetry incidents in the last year), inconsistent UX behavior (CSRF, lockout, password-policy variation across surfaces), and compliance findings ("inconsistent auth controls" flagged in last audit). Consolidating into a shared `auth_core/` library consumed by thin service-specific entry points eliminates the drift structurally, but the migration must preserve zero-disruption auth UX, wire-compatible session/token formats, perf budgets, and the existing per-service audit log destinations during a 90-day overlap. Forcing function: next compliance audit cycle at end of Q3.

## Known Context

- Three services: `services/web`, `services/api`, `services/mobile_bff`.
- Three auth modules to consolidate (paths above).
- Shared lib already exists: `services/shared/security_utils/` — Argon2id, JWT, lockout. Stays; new core consumes from it.
- Persistence: User table + Sessions table, shared across all three.
- Current login latency P99: web 65ms, api 50ms, mobile 95ms. Budget: ≤80ms after consolidation.
- Two CVE-asymmetry incidents in last 12 months (Oct 2024 JWT, Feb 2025 password policy).
- Audit destinations differ (CloudWatch, Splunk, S3); 90-day overlap required; 7-year retention.
- Phased rollout supported per service (shadow → 5% → 50% → 100%).
- Compliance audit cycle at end of Q3 is the forcing function.

## Constraints

- Zero forced re-login during migration (firm).
- Session and token wire formats unchanged (firm; downstream services depend).
- Login latency P99 ≤ 80ms post-consolidation across all three services.
- Audit log: unified stream + 90-day legacy overlap + 7-year retention preserved.
- Each service migrates independently (no big-bang).
- All current behavior preserved OR delta documented with explicit security review sign-off.
- `services/shared/security_utils/` stays — consumed by new core, not replaced.

## Success Criteria

- Single source of truth for: password policy, lockout logic, CSRF handling, JWT validation, OAuth2 PKCE flow.
- Three legacy modules deleted (not deprecated) at the end of migration.
- A CVE in any auth dependency patched in ONE PR, deployed to all three services in a single release.
- Compliance audit cycle at end of Q3 finds zero auth-consistency drift.
- Login latency P99 ≤ 80ms across all three services post-migration.
- Unified audit log queryable by user, by service, by outcome; legacy streams cleanly deprecated after 90 days.
- No production auth incident attributable to the migration itself.

## Open Questions

- Per-service entry-point shape: thin facade (forwards everything to core) vs. richer per-service adapter (handles protocol-specific concerns like session-cookie vs. bearer-token)? Trade-off between core API surface size and per-service code volume.
- OAuth2 PKCE handling location: in core (centralized) or in mobile_bff entry-point (protocol-specific concern)? Affects core's surface area.
- Session-cookie CSRF token rotation policy during migration: keep current (web-only) or harmonize across all services (none of api / mobile use cookies, so this may be moot)?
- Test surface for the cutover itself: how do we prove "shadow mode results match old behavior" in CI vs. only in staging?
- Audit-log unification format: JSON event schema TBD; should we adopt CloudEvents, OpenTelemetry logs, or a custom in-house schema?
- Migration ordering: which service first? Cheapest-to-migrate (probably api — fewest behaviors) vs. highest-risk-first (mobile — largest blast radius) vs. lowest-risk-first (web — most familiar).
- Pentest scope: end of consolidation only, or after each service cuts over?

## Enrichment Context

Codebase enrichment ran in `fallback_2` (native Glob/Grep) mode. Full output at `enrichment/codebase-context.md`. Key signals folded into the brief:

- Three login modules at paths above, ~1200 / ~800 / ~950 LOC respectively (significant overlap detectable via similarity scan).
- `services/shared/security_utils/` is genuinely shared and well-tested — keep, do not refactor.
- User and Sessions tables are already shared; no schema migration required.
- Test harness: existing pytest + httpx + Pact installed per service; no new test infra needed.
- Audit pipeline: three independent destinations, no existing unifier; will need new event publisher.

Confidence on enrichment: medium. A real Auggie semantic pass would tighten cross-module similarity findings and surface any subtle behavior delta that grep cannot see (e.g., timing-sensitive auth side effects).
