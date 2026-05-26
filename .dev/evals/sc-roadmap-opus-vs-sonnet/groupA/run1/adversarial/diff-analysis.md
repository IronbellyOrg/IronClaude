# Diff Analysis: User Authentication Roadmap (Variant A vs Variant B)

## Metadata

- Generated: 2026-05-22T16:27:38+00:00
- Variants compared: 2 (V-A = opus:security, V-B = sonnet:security)
- Total differences found: 27 (S: 6, C: 5, X: 3, U: 6, A: 7)
- Pipeline: sc:adversarial Mode B, --depth standard
- Source: /config/workspace/IronClaude/tests/sc-roadmap/fixtures/sample_spec.md

## Structural Differences

| # | Area | Variant A (opus:security) | Variant B (sonnet:security) | Severity |
|---|------|---------------------------|------------------------------|----------|
| S-001 | Milestone count | 9 total (7 work + 2 validation) | 7 total (5 work + 2 validation) | Medium |
| S-002 | M1 scope | Threat-model-first (STRIDE + infra + secrets + CI + encryption baseline) | Infrastructure-first (containers + schema + observability + API skeleton) | Medium |
| S-003 | OAuth + 2FA placement | OAuth in M4; 2FA in M6 (Defense Layer with rate limiting) | OAuth + 2FA combined in M3 (Federated/Strong Auth) | High |
| S-004 | Policy decomposition | RBAC+Audit in M5; Rate-Limit+2FA in M6 (two milestones) | RBAC+Audit+Rate-Limit combined in M4 (one milestone) | High |
| S-005 | GDPR coverage | Scattered: M2 primitives + M5 misc | Concentrated: M5 has dedicated data-export + right-to-erasure deliverables | Medium |
| S-006 | M2 effort/scope | Narrow (5 deliverables: identity primitives only — no login yet) | Broad (7 deliverables: full shippable email/password auth) | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Threat modeling | Dedicated milestone deliverable (STRIDE map at M1) | Ongoing activity owned by security persona, not a discrete milestone | Medium |
| C-002 | CSP headers timing | Deferred to M6 (defense-in-depth layer) | Landed in M2 alongside HTTP-only cookies | Medium |
| C-003 | 2FA framing | "Defense" — pairs with rate limiting to mitigate brute force | "Strong auth" — pairs with OAuth to reduce password reliance | High |
| C-004 | Audit log integrity | Hash-chain, append-only, tamper-evident | Hash-chain, append-only, tamper-evident | Low (agreement) |
| C-005 | Effort estimation philosophy | Many smaller (S/M) milestones, smaller blast radius per release | Fewer larger (L) milestones, stronger end-to-end coherence per release | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | When CSP headers ship | M6 — defense layer (D6.5) | M2 — same milestone as cookies (D2.5) | High — affects when RISK-001 is fully mitigated |
| X-002 | Need for dedicated threat-model milestone | YES — M1 is foundation (D1.1 STRIDE deliverable) | NO — threat-model is continuous security-persona activity | Medium — strategic delivery philosophy |
| X-003 | 2FA belongs with… | …rate limiting (attack-surface reduction) | …OAuth (alternate auth methods) | High — drives milestone composition |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | A | Explicit STRIDE threat model deliverable (D1.1) before any auth code | High — catches design-stage threats and provides reference for downstream milestones |
| U-002 | A | "JWT shape lock before federated identity" rationale (M3 → V1 → M4 sequencing) | High — mitigates a known real-world bug class (federated/local token-shape drift) |
| U-003 | A | Explicit secret & JWT key rotation policy at foundation (D1.3, 90-day cycle) | Medium — often deferred and then forgotten |
| U-004 | B | Observability baseline (D1.5) — structured logs, metrics, tracing for auth endpoints | High — supports NFR-005 (99.9% uptime) measurement and incident response |
| U-005 | B | GDPR right-to-erasure as a first-class deliverable (D5.5) | High — NFR-004 compliance often left implicit; this makes it auditable |
| U-006 | B | Schema-rewrite risk explicitly called out in M1 with "keep schema minimal" mitigation | Medium — pragmatic flag for a common pitfall |

## Shared Assumptions

Implicit preconditions both variants depend on. UNSTATED items are promoted to [SHARED-ASSUMPTION] diff points (A-NNN) and surface for debate scrutiny.

| # | Assumption | Source Agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | Single-tenant deployment | Neither variant addresses multi-tenancy in RBAC, audit, or rate-limit deliverables | High — multi-tenant SaaS rework would invalidate RBAC + rate-limit designs | UNSTATED → promoted |
| A-002 | Monolithic deployment | Both use docker-compose / single Docker service; no service decomposition | Medium — affects horizontal-scaling story for NFR-002 (10K concurrent) | UNSTATED → promoted |
| A-003 | PostgreSQL 15+ for both user data AND audit log | Stated in both as DEP-001 | Low — explicit | STATED (not promoted) |
| A-004 | Redis session-store is reliable enough; no DB fallback | No DB-backed session fallback in either variant | Medium — Redis outage = full auth outage (NFR-005 risk) | UNSTATED → promoted |
| A-005 | English-only auth flows | No i18n deliverable in either variant for email templates, error messages | Low — but may surface as compliance/UX issue | UNSTATED → promoted |
| A-006 | FR-011 admin dashboard is web-based | Neither specifies CLI/API-only admin path | Low — UX assumption | UNSTATED → promoted |
| A-007 | SendGrid is the sole email provider (no DSN switching) | Stated as DEP-003; no fallback in either | Medium — single point of failure for FR-001, FR-005 verification | UNSTATED → promoted |
| A-008 | Rate limit applies uniformly across endpoints (no per-endpoint tiering) | Both describe sliding-window per-user + per-IP, no endpoint-level policy | Medium — auth endpoints likely need different limits than profile endpoints | UNSTATED → promoted |

**Promoted [SHARED-ASSUMPTION] diff points**: A-001, A-002, A-004, A-005, A-006, A-007, A-008 (7 of 8; A-003 stated and not promoted).

## Summary

- Total structural differences: 6 (2 High, 3 Medium, 1 Low-equiv)
- Total content differences: 5 (1 High, 3 Medium, 1 Low/agreement)
- Total contradictions: 3 (2 High, 1 Medium)
- Total unique contributions: 6 (4 High value, 2 Medium value)
- Total shared assumptions: 8 surfaced (1 STATED, 7 UNSTATED → promoted to A-001..A-007+A-008)
- **Total diff points for convergence denominator**: 6 + 5 + 3 + 7 = 21 (U-NNN not in denominator per protocol)
- **Highest-severity items**: S-003, S-004, X-001, X-003, C-003, A-001 (all High)

## Variant Similarity Check

Total comparable items: ~30 (deliverables, milestones, risks). Differences: 27. Difference ratio: ~90%. **Not substantially identical** — proceed with debate.
