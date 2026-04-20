---
total_diff_points: 15
shared_assumptions_count: 20
---

# Roadmap Variant Diff Analysis: Opus vs Haiku (Architect)

## Shared Assumptions and Agreements

Both variants converge on identical high-level structure and core decisions:

1. **Milestone decomposition**: 5 milestones (M1–M5), same titles, same P0 priority, same HIGH/HIGH/MEDIUM/MEDIUM/MEDIUM risk profile.
2. **Timeline**: 2w/2w/3w/2w/2w, totaling 11 weeks with identical week allocations.
3. **Critical path**: Migrations + RSA keys → primitives → AuthService + endpoints → load-test NFR-AUTH.1 → E2E SC-8.
4. **Architectural constraints**: RS256 asymmetric JWT, bcrypt cost=12, httpOnly refresh cookie, stateless JWT with rotation, single `AUTH_SERVICE_ENABLED` feature flag, reversible migrations with down scripts.
5. **Token TTLs**: access=15min, refresh=7d, reset=1h.
6. **SHA-256 hashing** of refresh tokens at rest; replay detection revokes all user tokens.
7. **Rotation cadence**: 90-day dual-key grace window bounded by refresh TTL.
8. **Success criteria**: SC-1..SC-8 with same targets (p95<200ms, 99.9% uptime, cost=12, 5/min/IP, PSS policy, replay revoke-all).
9. **Rate limiting**: 5 attempts/min/IP on login, central Redis-class store.
10. **Dependency graph**: identical M1→M2→M3→M4→M5 structure with same component wiring.
11. **Component deliverable counts per milestone**: M1=17, M2=17, M3=28, M4=10 (M5 differs — see divergence 12).
12. **Open issues register**: identical OI-1..OI-10 with same owners and blocking semantics.
13. **Risk register**: same R-001..R-017 with same severities and probabilities.
14. **Password policy**: 8+ chars, upper, lower, digit.
15. **Two-step password reset** with user-enumeration-resistant request endpoint.
16. **External dependency list**: same npm packages, secrets manager, email vendor (blocked by OI-10), Redis, APM, PagerDuty.
17. **Sequencing rationale**: primitives-first (leaf-out) over orchestrator-first, driven by risk 0.7 / testability 0.3.
18. **Rollout strategy**: canary → 25% → 100% with flag-first rollback preceding DB rollback.
19. **M5 validation gates**: SEC-002 security review + SEC-003 pentest + OPS-006 rollback rehearsal as release prerequisites.
20. **Audit scope**: AUDIT-001 ships foundational events in M4, OI-7 persistence policy deferred to v1.1.

## Divergence Points

### 1. Entity type convention (DM-001, DM-002, DM-003)
- **Opus**: SQL/persistence types (`UUID-PK`, `varchar`, `timestamptz`, `bool`).
- **Haiku**: application-layer types (`UUID-v4`, `string`, `Date`, `boolean`).
- **Impact**: Opus signals schema-first intent useful for DBAs and migration reviewers; Haiku signals code-first intent useful for backend developers. Both map to identical runtime, but artifact reviewers get different frames.

### 2. RSA key size specification (INFRA-001)
- **Opus**: explicitly mandates "2048-bit min".
- **Haiku**: unspecified beyond "RS256-compatible".
- **Impact**: Opus closes a security-review gap before M1 exits; Haiku defers the decision into implementation, risking weaker keys if a developer reads the AC literally.

### 3. JWT public key distribution format (INFRA-001, COMP-003)
- **Opus**: "public embeddable in **JWKS**".
- **Haiku**: "public embeddable in verifier set".
- **Impact**: Opus commits to a standard (RFC 7517) enabling interop with third-party verifiers; Haiku keeps format flexible but leaves a discovery-endpoint decision open.

### 4. Secrets-manager ACL scope (INFRA-002)
- **Opus**: "**kms-level** ACL restricts access".
- **Haiku**: "ACL restricts access".
- **Impact**: Opus binds the implementation to a specific access-control model (useful for compliance mapping); Haiku keeps provider-neutral phrasing.

### 5. bcrypt benchmark timing band (TEST-M2-001, SEC-001)
- **Opus**: "p95 between **200ms and 350ms** on reference hardware"; "~250ms/hash on CI hardware".
- **Haiku**: "expected hashing time" / "timing recorded".
- **Impact**: Opus gives CI a falsifiable pass/fail; Haiku requires interpretation and risks drift on CI hardware changes.

### 6. httpOnly cookie path scoping (COOKIE-001)
- **Opus**: specifies `cookie path=/auth/refresh`.
- **Haiku**: no path attribute specified.
- **Impact**: Opus narrows cookie exposure to the refresh endpoint only (defense-in-depth against CSRF-like exfiltration); Haiku leaves cookie visible on all `/auth/*` paths.

### 7. Health endpoint latency SLO (OPS-002)
- **Opus**: "<50ms p95".
- **Haiku**: no latency requirement.
- **Impact**: Opus pre-empts false-green scenarios where a slow health check still returns 200; Haiku leaves this to M5 synthetic probe work.

### 8. Rate-limit health-check bypass (RATE-001)
- **Opus**: "bypass for health checks".
- **Haiku**: not mentioned.
- **Impact**: Opus prevents the scenario where an uptime monitor exhausts rate-limit budget and self-triggers alerts; Haiku risks that failure mode.

### 9. User-enumeration guard explicitness (API-005)
- **Opus**: "always 202 regardless of existence (user enumeration guard)".
- **Haiku**: "generic success response".
- **Impact**: Opus gives implementers an unambiguous status code and security rationale; Haiku could be read as allowing differential responses.

### 10. Decision-rationale traceability
- **Opus**: cites specific constraints ("Spec §Architectural-Constraint-1") and risk IDs (RISK-1, RISK-2) per decision.
- **Haiku**: generic "Architectural constraint mandates" phrasing.
- **Impact**: Opus supports bidirectional spec traceability and audit; Haiku is more readable but weaker for compliance sign-off.

### 11. Fallback library specificity (External Dependencies)
- **Opus**: names concrete fallbacks (`node-jose`, `bcryptjs`).
- **Haiku**: generic ("Alternative JWT library only if CVE-blocked", "Pure-JS fallback").
- **Impact**: Opus shortens the incident-response path if a CVE forces vendor swap; Haiku leaves the choice to incident-time judgment.

### 12. M5 deliverable count inconsistency
- **Opus**: milestone summary row says `11` deliverables, but M5 table enumerates 16 items.
- **Haiku**: summary row says `16`, matching the 16 enumerated items.
- **Impact**: Opus has an internal count inconsistency that will cause downstream tasklist-generation mismatch; Haiku is self-consistent. Haiku is clearly stronger here.

### 13. Risk register milestone tagging (R-002, R-003)
- **Opus**: R-002 affects M2, M3; R-003 affects M2, M5.
- **Haiku**: R-002 affects M2, M3, M5; R-003 affects M2, M4, M5.
- **Impact**: Haiku's broader tagging surfaces these risks in milestone-specific risk reviews (M5 release gate sees replay risk explicitly); Opus's tighter tagging reduces noise but risks dropping the risk from later reviews.

### 14. OI-6 resolution urgency (lockout policy)
- **Opus**: "Decision before v1.1; **must be acknowledged in release notes**".
- **Haiku**: "Before v1.1 planning".
- **Impact**: Opus creates a hard release-notes gate protecting customer-visible expectations; Haiku treats it as planning-cycle work with no external disclosure requirement.

### 15. DTO field-exclusion explicitness (DM-003)
- **Opus**: AC explicitly lists `no password_hash; no token_hash`.
- **Haiku**: implicit via general DTO-001 whitelist.
- **Impact**: Opus front-loads the leak-prevention contract at the DTO definition; Haiku relies on a separate DTO-001 serializer, creating a second place a regression could slip in.

## Areas Where One Variant Is Clearly Stronger

**Opus is stronger on:**
- Specificity of cryptographic and operational parameters (key size, benchmark timing band, cookie path, health-check SLO, rate-limit bypass).
- Traceability of decisions to spec constraints and risk IDs.
- Security posture explicitness (enumeration guard 202, DTO field exclusions called out at the DTO level).
- Incident response readiness (named fallback libraries).

**Haiku is stronger on:**
- Internal consistency (M5 deliverable count matches its table; Opus has a 11-vs-16 discrepancy).
- Risk-register milestone tagging completeness (R-002 and R-003 surface in all affected milestones, including M5 release gate).
- Readability and tighter phrasing in Executive Summary and Decision Summary.

## Areas Requiring Debate to Resolve

1. **Schema-type vs application-type entity conventions (divergence 1)** — which audience is primary for persistence DTOs: DBAs or backend engineers? Affects downstream task-file generation.
2. **Cookie path scoping (divergence 6)** — broader `path=/` simplifies SPA integration; narrower `path=/auth/refresh` is safer. Security vs DX trade-off.
3. **Health-check latency SLO (divergence 7)** — <50ms bound is opinionated; some teams prefer health checks be "as fast as possible" without a hard bound.
4. **OI-6 release-notes disclosure (divergence 14)** — committing to release-notes disclosure creates product-communication work; deferring to v1.1 planning avoids that but risks customer surprise.
5. **M5 deliverable count (divergence 12)** — not a true debate: Opus has an internal error that must be fixed regardless of which variant wins. The fix direction (11 → 16 or drop 5 items) is the open question.
6. **Benchmark timing band (divergence 5)** — whether to encode a specific ms band risks CI-hardware brittleness; whether to omit it risks unfalsifiable assertions. Standard CI benchmarking trade-off.
