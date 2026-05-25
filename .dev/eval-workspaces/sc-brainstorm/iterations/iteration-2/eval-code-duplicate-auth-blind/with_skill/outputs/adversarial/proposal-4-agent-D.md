---
proposal_id: 4
agent_label: Agent D
persona: qa
blind_mode: true
lens: test surface, regression risk, acceptance criteria, contract validation
---

# Proposal 4 — Agent D: The Test Surface Is The Hard Part — And Nobody Has Sized It

## Position

I read four of the planned five proposals before drafting this one. Three (Agent A, B, C — well, C indirectly) have made implementation/architecture claims with no explicit answer to: **what is the test suite that proves the new code is wire-compatible with the old, behaviorally?** Auth has a higher behavioral surface than any of the proposals have engaged with — login success / failure, lockout interactions, session/token lifetime, CSRF token rotation, password-policy enforcement at register vs login vs change vs reset, OAuth2 PKCE error paths, biometric step-up downgrade paths, audit-event timing relative to lockout-counter increment, idempotency under network retry. Each is a place a regression silently lands.

## Test plan (concrete, non-negotiable)

### Unit (≥120 cases across the new core)

- Password policy: ≥15 cases — boundary length, allowed-character classes, history check if implemented, register vs login enforcement parity, the Feb-2025 length-update regression case.
- Lockout policy: ≥20 cases — threshold parity across three services, time-window behavior at boundary, concurrent-request increment-correctness, lockout-state interaction during shadow mode (Agent C's C1 concern, tested explicitly).
- JWT validation: ≥15 cases — the Oct-2024 CVE patched, signature mismatch, expired token, missing claims, malformed payload.
- OAuth2 PKCE: ≥20 cases — S256 verification, code_verifier length / character class, redirect URI mismatch, state parameter, expired authorization codes.
- Session-cookie flow: ≥15 cases — CSRF token rotation, secure/httponly/samesite attributes, cookie-jar interaction across subdomains.
- API key: ≥10 cases — HMAC verification, per-customer key rotation behavior.
- Biometric step-up: ≥15 cases — WebAuthn attestation, downgrade to password fallback, lost-device path.
- Audit emit: ≥10 cases — event-shape validation against schema, dual-write success/failure isolation.

### Contract (≥50 cases per service boundary)

Each service ↔ auth_core boundary documented as a Pact (or equivalent) contract. Contracts are versioned and breaking changes block migration. ~150 contract cases total.

### Integration (≥30 cases per service)

Each service in test mode against the real auth_core, real Redis (Testcontainer), real test User database. End-to-end through the service's HTTP surface so the session-cookie / bearer-token / PKCE flow is exercised. ~90 integration cases total.

### Shadow-mode delta detection (the hard one)

Concrete test scaffolding: a runner that pumps a corpus of recorded production-shape requests (anonymized) through both old and new paths and asserts:

- Identical outcome (success/fail). Delta = bug.
- Identical lockout-counter side effects. Delta = exploitable (Agent C's C1).
- Identical audit-event content (modulo timestamp / event-ID). Delta = compliance gap.
- Latency within ±10% per request, ±5% on P99 aggregate. Delta = perf regression.

Corpus: ~50K requests sampled across all three services, all flows, all outcomes, including known-edge-cases (Incident 1 and 2 input patterns reconstructed). Must pass with zero deltas before any service exits shadow mode for that service.

### E2E (per service, ≥10 scenarios)

Real client SDKs (iOS, Android, JS browser, Python API client) against staging, full login flows including failure paths. ≥30 scenarios total.

### Security / pentest (Agent C's territory; agreed)

≥4 external pentest engagements — pre-migration, post-api-cutover, post-web-cutover, post-mobile-cutover. Findings block promotion to the next phase if they are MEDIUM or higher.

## Acceptance criteria (specific, measurable)

- **AC-T1**: All ≥120 unit cases green; coverage on new core ≥95% line + branch.
- **AC-T2**: All ≥150 contract cases green; no version-bump pending against a consumer.
- **AC-T3**: All ≥90 integration cases green; Redis-unavailable scenario exercises documented behavior.
- **AC-T4**: Shadow-mode runner shows zero deltas on the 50K-request corpus for each service before that service exits shadow.
- **AC-T5**: All ≥30 E2E scenarios green per service.
- **AC-T6**: All pre-migration and per-cutover pentest findings ≤ LOW before promotion.
- **AC-T7**: Latency P99 ≤ 80ms across all three services post-migration; verified in staging-shape load test before each canary phase.

## What I'd push back on

Both Agent A and Agent B underestimated the test surface. Agent A's "~4 engineer-weeks for core + tests" and Agent B's "~2 engineer-weeks for core" almost certainly do not include the contract-test layer, the shadow-mode delta-detection runner, or the corpus collection. **The test plan above adds ~8 engineer-weeks of test development on top of either architectural plan.** It is a non-negotiable cost; auth is the surface where untested code becomes incident response.

## What I'd concede

I have no strong preference between Agent A's plugin architecture and Agent B's policy-only consolidation on test cost — the unit/contract/integration/E2E shape is roughly the same either way. The shadow-mode delta-detection runner is slightly smaller against Agent B (less core code) but the difference is ~10%, not architectural.

## Cost

~8 engineer-weeks of test development. Sustaining cost: ~10% of post-migration auth engineer time on test maintenance.

## Confidence

High on the test counts (these are the right orders of magnitude for an auth surface). Lower on whether the shadow-mode corpus can be collected at sufficient diversity from production traffic alone — may need synthetic augmentation for the rare-error paths.
