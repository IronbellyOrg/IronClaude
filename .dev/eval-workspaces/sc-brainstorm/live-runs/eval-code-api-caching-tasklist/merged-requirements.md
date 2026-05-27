---
schema_version: "1.0"
source_seed_brief_path: ".dev/eval-workspaces/sc-brainstorm/live-runs/eval-code-api-caching-tasklist/seed-brief.md"
contract_version: "1.0"
status: success
case_id: 8
case_name: code-api-caching-tasklist
topic: "adding caching to the API layer"
domain: code
strategy: systematic
depth: standard
proposal_count: 3
adversarial_status: converged
convergence_score: 0.82
fit_to_intent: pass
unresolved_conflicts: []
handoff_action: tasklist
blind_mode: false
created: "2026-05-27"
base_variant: 2
incorporated_variants: [1, 3]
---

# Merged Requirements — Adding Caching to the API Layer

## Functional Requirements

### FR1 — Endpoint Cache-Policy Registry

A central registry / control plane is the source of truth for which endpoints are cached and how. Each cached endpoint declares: identifier or route pattern, eligibility classification, TTL + max-stale window, key-builder dimensions, invalidation source (or rationale for TTL-only), stale-if-error eligibility, rollout flag + policy version, owner + reviewer.

### FR2 — Deny-by-Default Eligibility

Caching is disabled by default. Candidate endpoints must be classified before enablement as one of: **public/global**, **tenant-scoped**, **user-scoped**, **confidential/regulated**, **non-cacheable**. Public/reference endpoints follow a lightweight approval path; tenant / user / confidential responses require explicit policy + security approval.

### FR3 — Read-Endpoint Scope

Initial scope is safe, idempotent GET endpoints (list, detail, reference, summaries, public metadata). Mutations, auth/session, and secret-bearing endpoints remain non-cacheable unless separately approved.

### FR4 — Cache Key Correctness

Keys must include every dimension that can change the response. Minimum dimensions: route + normalised path params; normalised query params; API version; tenant id; user / role / permission / authorisation when output-shaping; content-negotiation headers; locale / region when applicable; feature-flag / experiment state when output-affecting.

### FR5 — Expiration & Invalidation

All cached endpoints require TTL. Endpoints whose data can change via mutations require event-driven or mutation-hook invalidation. If reliable invalidation is unavailable, the endpoint uses a short bounded TTL or remains uncached.

### FR6 — Manual Purge Controls

Operators must be able to purge by global scope, endpoint, resource, tenant/cohort, and policy version where feasible. Purges propagate across all cache replicas or emit explicit failure signals.

### FR7 — Resilience & Fallback

Cache-backend failures must degrade safely. Approved behaviour: origin read-through fallback with alerting unless origin itself is unavailable. Cache failures must not bypass authorisation, return another tenant's data, or alter contract semantics.

### FR8 — Stampede Protection

Prevent stampedes for hot keys via request coalescing, per-key locking, TTL jitter, early refresh, or another documented mechanism.

### FR9 — Bounded Stale-if-Error

Stale-if-error may be enabled only when the endpoint's policy explicitly marks bounded-stale responses as safe. Forbidden for revocation-sensitive, secret-bearing, confidential, or regulated responses unless explicitly approved by security + product owners.

### FR10 — Rollout Controls

Caching is controllable globally, per endpoint, per tenant/cohort, per policy version. Supported states: disabled, shadow/observe, read-through enabled, rollback.

### FR11 — Observability & Auditability

Expose metrics + logs for: hit ratio, miss ratio, cache latency, origin latency, fallback count, stale-served count, invalidation count, purge count, backend errors, policy version, endpoint/cohort dimensions. Policy changes, security overrides, manual purges, and stale-if-error use are auditable with actor / time / scope / reason.

### FR12 — Compatibility Preservation

Preserve existing API response bodies, status codes, client-required headers, authorisation behaviour, and error semantics unless an explicit contract change is separately approved.

## Non-Functional Requirements

- **NFR1.** Pilot cached endpoints achieve ≥ 30% p95 latency improvement vs baseline.
- **NFR2.** Pilot cached endpoints reduce origin dependency load by ≥ 20% in steady state.
- **NFR3.** Cache hit path adds ≤ 10 ms p95 beyond cache-backend latency.
- **NFR4.** Cache miss path adds ≤ 15 ms p95 over current origin behaviour.
- **NFR5.** Cache-backend outage must not take down the API layer.
- **NFR6.** Zero cross-tenant / cross-user cache leakage is acceptable.
- **NFR7.** Cache storage + logs obey existing encryption, retention, privacy, and data-residency policies.
- **NFR8.** Operators can disable caching for any endpoint without code deployment.
- **NFR9.** Cache hit ratio for pilot endpoints ≥ 60% in steady state.
- **NFR10.** Policy / registry changes are reviewable and auditable (security + product sign-off captured).

## Acceptance Criteria

- **AC1.** ≥ 3 endpoint classes have documented cache policies (eligibility, TTL, key dimensions, invalidation, rollout state, owner, reviewer).
- **AC2.** Tests prove keys vary by tenant, auth/role, API version, normalised query, and content-negotiation when output-affecting.
- **AC3.** Mutation-driven invalidation is implemented or explicitly waived with short-TTL / no-cache rationale per affected resource.
- **AC4.** Operators can disable caching globally, per endpoint, and per tenant/cohort without deployment.
- **AC5.** Manual purges emit audit events with actor / time / scope / reason.
- **AC6.** Cache-backend outage testing proves safe origin fallback without data leakage.
- **AC7.** Load tests demonstrate pilot latency + origin-load targets (NFR1, NFR2).
- **AC8.** Stampede protection is tested for hot keys + simultaneous expiry.
- **AC9.** Stale-if-error disabled for revocation-sensitive + sensitive endpoints unless explicitly approved.
- **AC10.** Dashboards show hit ratio, miss ratio, latency split, invalidation count, purge count, fallback count, stale-served count, backend errors by endpoint + cohort.
- **AC11.** Pilot rollout completes a documented shadow → enabled → measured cycle with explicit go/no-go review.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Key omits tenant / auth dimension | Cross-tenant or cross-user data leak | Deny-by-default; mandatory key-dimension tests; security review of policy registry entries |
| Stale reads after mutation | Incorrect user-visible data | Event-driven invalidation; short-TTL / no-cache fallback when invalidation unavailable |
| Cache backend outage | Latency / error spike on API layer | Origin read-through fallback; circuit breaker; alerts; per-endpoint bypass switch |
| Hot-key stampede | Origin overload during expiry storms | Single-flight / per-key locking; TTL jitter; early refresh |
| Sensitive / regulated data retained | Privacy / compliance incident | Classification step; encryption + retention policy parity; non-cacheable defaults for confidential routes |
| Debug logs expose key material | Information disclosure | Key redaction in logs; logging review; policy audit; restricted access |
| Stale-if-error returns revoked content | Authorisation drift | Stale-if-error gated by policy + security approval; forbidden for revocation-sensitive endpoints |
| Cache layer masks origin degradation | Hidden regressions | Track origin latency separately; alert on origin-latency drift independent of hit ratio |
| Rollout overshoots safe cohort | Production incident | Shadow mode → cohort rollout → global; explicit go/no-go; kill switch |

## Open Questions

- Which API framework and cache backend does the target system use?
- Is there an existing domain event stream that can drive event-based invalidation?
- Which endpoints are public/global vs tenant-scoped vs user-scoped today (sensitivity inventory)?
- What is the maximum acceptable stale-data window per endpoint class?
- Are cache keys or response bodies subject to special regulatory / data-residency rules?
- Should clients receive cache-related response headers (Age, X-Cache, ETag policy), or remain server-internal?
- Which team owns endpoint cache policy review + long-term operation?
- What production-like load-test environment is available for AC7 validation?
- Are there existing rate-limit / circuit-breaker layers whose interaction with caching must be specified?

## Provenance

This merged-requirements artifact was produced by `/sc:brainstorm` Case 8 (`code-api-caching-tasklist`) under the `sc-brainstorm-protocol` Wave-3 adversarial sub-pipeline.

- **Topic (verbatim from prompt):** `Brainstorm adding caching to the API layer. Use --depth standard. Handoff tasklist.`
- **Source seed brief:** `seed-brief.md` (Phase-2 schema: Intent Summary, Context Anchors, Must Preserve, Out of Scope).
- **Source-of-truth protocol:** `sc-brainstorm-protocol` (Waves 0-4) + `sc-adversarial-protocol` (Wave-3 merge).
- **Schema version:** `1.0` (Phase-2 merged-requirements schema).
- **Contract version:** `1.0`.
- **Convergence:** 0.82 (threshold 0.75 — CONVERGED in 2 rounds).
- **Fit-to-intent:** pass.
- **Unresolved conflicts:** none after Round 2; see `adversarial/debate-transcript.md` for the conflict timeline.
- **Base variant:** Variant 2 (backend / sonnet) — selected for the densest operational coverage (invalidation, stampede, observability, fallback).
- **Incorporated from Variant 1 (architect / opus):** the explicit cache-policy registry / control plane spine (FR1, FR10, FR12, AC1, AC11, NFR10).
- **Incorporated from Variant 3 (security / haiku):** deny-by-default eligibility, classification taxonomy, key-dimension correctness, audit logging, stale-if-error security gates (FR2, FR4, FR9, FR11, NFR6, NFR7).
- **Enrichment inputs:** `enrichment/codebase-context.md` (codebase=ON, research=LIGHT per depth=standard defaults).
- **Adversarial artifacts:** `adversarial/variant-1-architect-opus.md`, `variant-2-backend-sonnet.md`, `variant-3-security-haiku.md`, `debate-transcript.md`, `diff-analysis.md`, `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `merged-output.md`, `return-contract.yaml`.
- **Handoff:** `handoff/tasklist-index.md` + per-phase tasklists (Wave 4).
- **Generated:** 2026-05-27 (Phase-2 schema rerun).
