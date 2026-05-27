# Diff Analysis: spec Comparison (3 variants)

## Metadata

- Generated: 2026-05-25T20:05:00Z
- Variants compared: 3
- Variant 1: opus:architect (4337 words) — Federation-readiness-as-monolith-discipline + named governance roles
- Variant 2: sonnet:analyzer (4390 words) — Rejection-condition-first + premortem-per-decision
- Variant 3: haiku:backend (3416 words) — Operations-first + idempotency/error/consistency contracts
- Categories: structural (5), content (9), contradictions (3), unique (8), shared assumptions (5)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Top-level sections | 14 (incl. §0 scope declaration) | 12 (open-questions table at §10) | 17 (most granular) | Low |
| S-002 | Decision framing | Decision → Rationale → Rejected alternatives | Decision → Evidence → Failure-Mode Analysis → Premortem | Decision → Justification → Tables of defaults | Medium |
| S-003 | Where rejection criteria live | §10 (late) | §1 (executive) + §9 (deep) | §16 (late) | Medium — V2 leads with rejection; V1/V3 treat it as conclusion |
| S-004 | Use of numerical defaults | Sparse (alert thresholds only) | Sparse (rate/depth defaults only) | Dense (entire §6 + §7 + §12 are tables of numbers) | Medium |
| S-005 | Hierarchy depth | 4 levels (H1→H4) | 3 levels (H1→H3 + tables) | 3 levels (H1→H3 + dense tables) | Low |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Variant 3 approach | Severity |
|---|-------|--------------------|--------------------|--------------------|----------|
| C-001 | Topology (monolith vs federation) | Federation-ready-by-construction monolith with `@owner` directive + per-domain folders | Plain monolith; federation only on demonstrated coordination pain | Plain monolith; federation on team-topology + traffic triggers | Medium — V1 advocates explicit scaffolding now; V2/V3 advocate wait-and-see |
| C-002 | Federation migration triggers | 2 of 3 signals (schema ownership %, deploy coupling, resolver fan-out) | 2 of 2 conditions (multi-team AND PR latency >48h) | 3+ of 5 conditions (teams, schema size, internal subgraphs, release delay, RPS) | Medium |
| C-003 | Schema evolution windows | Additive free / 6mo deprecation / 12mo breaking partner | Additive free / 6mo public / 12mo partner | Additive free / 12mo field / 18mo mutations & enums | High — V3's 12/18mo conflicts with V1/V2's 6/12mo |
| C-004 | Schema governance roles | 3 named roles (Steward, Breaking-Change Reviewer, Deprecation Gatekeeper) | 1 schema-review process, 24h SLA, no named roles | "API platform team" + on-call, no named roles | Medium — V1 is uniquely structured |
| C-005 | Auth tiers | 4 tiers including Anonymous (with strictest limits) | NO anonymous; gateway-layer-only enforcement | No anonymous in production; sandbox-only anonymous | High — see X-001 |
| C-006 | Persisted operations posture | Tiered: partner ENFORCED, API-key incentivized, anonymous open | Persisted operations only in production; ad-hoc only in sandbox | Persisted operations REQUIRED for production public clients | High — see X-003 |
| C-007 | Mutation idempotency | Not addressed | Not addressed | Full contract: idempotency key, 24h TTL (7d for billing), conflict semantics, IDEMPOTENCY_IN_PROGRESS | High — V3 unique |
| C-008 | Error contract | Generic mention | Generic mention | Detailed envelope: code, category, retryable, retryAfterSeconds, requestId, operationId, fieldPath, documentationUrl | High — V3 unique |
| C-009 | Consistency guarantees | Not addressed | Not addressed | Explicit table: strict for writes, read-your-write 2s, eventual 60s for aggregates, region semantics | High — V3 unique |

## Contradictions

| # | Point of conflict | V1 position | V2 position | V3 position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Anonymous access to the public graph | Allowed as Tier 1 with strictest cost/depth limits | "No anonymous access to the graph. Anonymous access is the #1 enabler of abuse" | Anonymous only in sandbox; production requires auth | High — affects MVP scope, abuse posture, and DX for casual exploration |
| X-002 | Standard deprecation window | 6 months minimum (12 for partner) | 6 months public / 12 months partner | 12 months fields / 18 months mutations and enums | Medium — V3's longer windows reduce schema churn risk but slow evolution; V1/V2 windows allow faster iteration |
| X-003 | Persisted operations default in production | Tiered (only partner enforced) | Allowlist-only by default in production | Required for production public clients by default | Medium — All converge on "needed for security" but disagree on whether anon/API-key get an ad-hoc path |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | `@owner` directive + per-domain schema folders as "federation-readiness scaffolding" | High — concrete maintainability lever |
| U-002 | V1 | Three named governance roles (Steward, Breaking-Change Reviewer, Deprecation Gatekeeper) with bus-factor rationale | High — addresses the "schema governance" gap directly |
| U-003 | V1 | CI-enforced resolver layering rules (resolvers→services→data, no cross-layer imports) | Medium — useful but stack-specific |
| U-004 | V1 | `@cost` and `@requiresScope` directives mandatory in CI | Medium — operationally valuable |
| U-005 | V2 | Premortem ("most likely failure in 18 months") attached to every decision | High — promotes structural over tactical thinking |
| U-006 | V2 | "If validation has not occurred, the recommendation is: do not adopt GraphQL. Stop here." rejection-first framing | High — guards against bandwagon adoption |
| U-007 | V2 | Quantified decision matrix in §9 (consumer type / data shape / team / maturity / timeline / existing surface) | High — gives organization a self-test |
| U-008 | V3 | Full mutation idempotency contract with explicit TTL, conflict, in-progress semantics | High — critical for any public mutation surface |
| U-009 | V3 | Detailed error envelope (code, category, retryable, retryAfterSeconds, requestId, operationId, fieldPath, documentationUrl) | High — contract gap in V1 and V2 |
| U-010 | V3 | Explicit consistency guarantees table (strict / read-your-write 2s / eventual 60s) | High — public APIs that ignore consistency confuse callers |
| U-011 | V3 | Concrete numerical defaults for everything (depth 10, complexity 1000, page size 25/max 100, query timeout 10s/mutation 30s) | High — actionable vs. abstract |
| U-012 | V3 | Pagination-contract section with cursor opacity, 24h cursor TTL, deterministic ordering, no arbitrary filter expressions in v1 | Medium-High — addresses a common GraphQL footgun |

## Shared Assumptions

| # | Assumption | Source agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | Schema-first / SDL-as-contract is the right approach (no code-first generation) | All three implicitly assume schema-first | Locks the org into a workflow some tooling discourages | STATED across all 3 |
| A-002 | A schema registry SaaS or self-hosted equivalent is available at launch | All three list it as a launch requirement without addressing build/buy or cost | If the org cannot afford Apollo Studio / GraphQL Hive AND cannot operate self-hosted, the entire governance story collapses | UNSTATED — promoted to [SHARED-ASSUMPTION] |
| A-003 | The target product / data model is decidable separately from the API technology choice | All three sidestep "what data does this serve" — the spec is written as if the data model is given | Without a target product, the spec cannot be implemented; it remains a meta-design | UNSTATED — promoted to [SHARED-ASSUMPTION] |
| A-004 | The authentication/identity infrastructure already exists or is straightforwardly buildable (JWT issuance, OAuth provider, key management) | V1, V2, V3 all assume tokens/keys are issuable but none address the identity provider | "Add OAuth" is many quarters of work if the org has no identity system | UNSTATED — promoted to [SHARED-ASSUMPTION] |
| A-005 | The team can sustain governance discipline for 18+ months without leadership churn breaking it | All three name roles/processes that require sustained organizational will | A single re-org or layoff event can dismantle the governance and the spec's value evaporates | UNSTATED — promoted to [SHARED-ASSUMPTION] |

## Summary

- Total structural differences: 5
- Total content differences: 9
- Total contradictions: 3
- Total unique contributions: 12
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-003, C-005, C-006, C-007, C-008, C-009, X-001
- Total comparable diff points (S+C+X+A): 22 (5 + 9 + 3 + 5)
- Similarity check: total differences (22) > 10% of comparable items — proceeding to debate (NOT skipping per too-similar rule)
