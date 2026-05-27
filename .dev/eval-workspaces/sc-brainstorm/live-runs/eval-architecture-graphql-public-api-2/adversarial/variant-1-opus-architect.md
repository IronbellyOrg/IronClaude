---
variant: 1
agent_spec: opus:architect
persona: architect
custom_instruction: "prioritize maintainability and extension scaffolding for architecture domain"
generated_for: explore-graphql-for-public-api
---

# Public-Facing GraphQL API Specification: Maintainability-First Architecture

## 0. Executive Stance and Scope Declaration

This specification is written under the architect persona with an explicit bias toward **long-term maintainability and extension scaffolding**. Where tradeoffs surface, the heavier weight is given to: (a) the cost of changing the schema five years from now, (b) the cost of onboarding a new team to own a slice of the graph, and (c) the cost of removing a field without breaking a partner integration. Speed-to-MVP is a secondary axis.

Because the seed brief confirms the host codebase (SuperClaude) currently exposes no public API surface, this spec is written as **stack-agnostic decision-grade requirements** for a hypothetical product team adopting GraphQL as a greenfield public API. Where target-specific decisions are unavoidable, an assumption is stated explicitly and the alternative path is named.

**Assumed product context** (stated, not discovered):
- Multi-team backend (3+ product domains: identity, content, billing-or-equivalent).
- Mixed consumer profile: a small set of high-value partner integrations (deep contracts, low N) plus a larger long-tail of third-party developers (shallow contracts, high N).
- Stability expectation is partner-grade: minimum 6-month deprecation windows, hard breaking changes are governed and rare.
- Backend language is not assumed; server-library selection is delegated to a stack-resolution decision (see Section 12).

## 1. Topology Decision: Federation-Ready Monolith

### 1.1 Decision

**Ship v1 as a monolithic graph that is federation-ready by construction.** Defer the actual subgraph split until the second domain team has shipped a feature end-to-end and the cross-team coordination tax has been observed empirically.

### 1.2 Rationale

The two failure modes the seed brief warns against are equally bad and live at opposite ends of the topology axis:

| Failure mode | Cause | Cost |
|---|---|---|
| Premature federation | Splitting subgraphs before domain boundaries are stable | Months of router config, schema-composition CI, and entity-key arguments for boundaries that move | 
| Permanent monolith | Single-graph hardens around one team's resolver patterns | Schema becomes a god-object; second team forks rather than contributes |

The architect-grade move is to **encode federation-readiness as a discipline in the monolith** so the migration cost is paid in tooling and conventions, not in retroactive refactors. Concretely this means:

1. **Type ownership headers in SDL** — every type has a `@owner(team: "...")` directive (or comment convention if directives are unavailable in the chosen server library). This is the same metadata Apollo Federation uses for `@key`/`@external` and survives the migration intact.
2. **Resolver layering by domain, not by type** — resolvers live under `resolvers/<domain>/<Type>.ts` (or equivalent), never under a flat `resolvers/` directory. The folder structure is the future subgraph boundary.
3. **No cross-domain resolver calls inside a single resolver function** — domain B's data is fetched via the same DataLoader interface a federated router would use. Cross-domain joins go through a `services/` layer that is identical in shape to what a federation gateway would invoke.
4. **Entity-key documentation up front** — every type that could become a federated entity declares its key field in a schema comment (`# @federation-key: id`) even if the directive isn't yet active.

### 1.3 Migration trigger to federation

Federation is adopted when **any two of these three signals fire**:

- A second team owns >30% of the schema's type surface and has merge conflicts in resolver files >2x per sprint.
- Deployment coupling (one team's release blocked by another's) has occurred 3+ times in a quarter.
- A type's resolver fan-out crosses 4+ backing services and the resolver file is >500 lines.

### 1.4 Rejected alternatives

- **Schema stitching** — rejected per 2026 best practice. It is legacy tooling; new builds should not adopt it.
- **Federated supergraph from day 1** — rejected because it forces premature boundary decisions and adds router infrastructure (Apollo Router or Cosmo Router) before there is a second team to justify the gateway tax.
- **Pure monolith with no federation hooks** — rejected because the architect mandate is to make tomorrow's pivot cheap, not to optimize today's line count.

## 2. Schema Modularization and Namespacing

The single most important maintainability lever is preventing the schema from becoming a flat namespace where every team's types collide.

### 2.1 Schema module structure

The SDL is composed from per-domain `.graphql` files concatenated at build time:

```
schema/
  core/                  # shared scalars, interfaces, errors, pagination
    pagination.graphql
    errors.graphql
    scalars.graphql
  identity/              # one domain
    User.graphql
    Session.graphql
    queries.graphql
    mutations.graphql
  content/               # second domain
    Article.graphql
    Comment.graphql
    queries.graphql
    mutations.graphql
  billing/
    ...
  composed.graphql       # build artifact, never hand-edited
```

### 2.2 Naming conventions (enforced by lint)

- Types are PascalCase, unprefixed at the schema level (no `IdentityUser` — federation directives carry ownership, not the type name).
- Fields are camelCase. Boolean fields read as predicates (`isPublished`, not `published`).
- Mutations follow `verbObject` (`createArticle`, `archiveUser`). Input types end in `Input`. Payload types end in `Payload`. This is non-negotiable because IDE autocompletion ranking depends on it.
- Enums are SCREAMING_SNAKE_CASE for values. Every enum reserves `UNKNOWN` as the zero value to keep forward-compatibility on client SDKs that pin to old generated types.
- Connection types (Relay-style cursor pagination) are mandatory for any list field whose unbounded growth is plausible. No `[Article!]!` at the root — always `ArticleConnection!`.

### 2.3 Extension scaffolding pattern

New product capabilities slot in via three explicit extension points:

1. **New type addition** — drop a new `.graphql` file into the relevant domain folder. CI validates SDL composes without conflict. Zero coordination cost.
2. **New field on existing type** — `extend type User { ... }` in a separate file when added by a different team than the type owner. The `@owner` directive on the extension declares the new field's ownership independently of the parent type's ownership. This is the single biggest scaffolding decision in the spec — it is what lets a second team add to `User` without touching the identity team's files.
3. **Cross-domain composition** — a new domain that needs to reference an existing type uses the federated-entity pattern (declaring the type as an entity in its own subgraph) even pre-federation, so the resolver shape is migration-ready.

## 3. Resolver Layering Boundaries

Resolvers are the layer most often eroded by tactical edits. The architecture mandates three immovable layers:

```
┌─────────────────────────────────────────┐
│  GraphQL resolver layer                 │  thin; only resolves field → service call
│  (lives under resolvers/<domain>/)      │
├─────────────────────────────────────────┤
│  Domain service layer                   │  business logic; framework-agnostic
│  (lives under services/<domain>/)       │  unit-testable without GraphQL
├─────────────────────────────────────────┤
│  Data-access layer                      │  DataLoaders, ORM, HTTP clients
│  (lives under data/)                    │
└─────────────────────────────────────────┘
```

**Architectural rules** (enforceable by import-linter or equivalent):

- The resolver layer **never** imports from `data/` directly. Only `services/`.
- The service layer **never** imports from GraphQL schema types. It returns domain objects; the resolver maps to GraphQL types.
- DataLoaders are **always** the path from resolvers to data — direct ORM/HTTP calls in resolvers are a CI-failing offense because they make N+1 detection structurally impossible.
- Cross-domain calls (resolver in domain A needs data from domain B) go through `services/B/`'s public interface, not through `data/`. This is the federation-readiness rule.

The reason these boundaries are non-negotiable is that the resolver layer is the most volatile (schema changes, client demands, performance fixes), and without these rules, business logic leaks into resolvers and becomes unmovable when federation arrives.

## 4. Schema Evolution Policy

This is the section that turns "public API" from a slogan into a contract.

### 4.1 Change classification

| Change class | Definition | Process | Window |
|---|---|---|---|
| **Additive** | New type, new field, new enum value (with `UNKNOWN` fallback), new optional input field | Free; merge after schema-lint passes | None |
| **Deprecation** | Existing field marked `@deprecated(reason: "...")` with replacement guidance | Schema steward sign-off; analytics alert configured | Minimum 6 months between deprecation and removal; longer if usage analytics show active consumers |
| **Breaking** | Field removal, type removal, required-arg addition, nullability tightening, enum value removal, semantic change without rename | Breaking-change reviewer + product sign-off; documented in changelog and partner communication | Rare governed event; minimum 12 months notice for partner-tier consumers |

### 4.2 What "breaking" specifically means

The breaking-change list is enumerated so there is no ambiguity in PR review:

1. Removing a type, field, enum value, or directive.
2. Renaming any of the above (rename = remove + add).
3. Changing a field's type to one not assignment-compatible (e.g., `Int` → `String`).
4. Changing a nullable field to non-nullable (`String` → `String!`).
5. Adding a required argument to an existing field.
6. Changing a default value in a way that alters returned data.
7. Changing the semantics of a field without changing its signature (this is the most insidious; it requires a documented changelog entry and is treated as breaking even though GraphQL Inspector won't flag it).

### 4.3 Schema governance roles

Three named roles, with the explicit goal that the bus factor on schema decisions is greater than 1:

- **Schema Steward** — owns the full SDL, runs the weekly schema review, holds merge authority on cross-domain changes. Rotates quarterly between domain leads to prevent capture.
- **Breaking-Change Reviewer** — required signoff on any change in the breaking-change list. Distinct from the Steward to provide independent review. Typically a senior architect or principal engineer not embedded in a single domain.
- **Deprecation Gatekeeper** — monitors `@deprecated` field usage via operational analytics; refuses removal until usage is below an agreed threshold (proposed: <0.01% of weekly queries for 4 consecutive weeks, AND zero hits from partner-tier API keys).

### 4.4 Governance tooling (required at launch)

| Tool category | Purpose | Specific candidates |
|---|---|---|
| Schema diff | Detect breaking changes in PRs | GraphQL Inspector (open source) or Apollo Studio schema checks |
| Schema lint | Enforce naming, descriptions, pagination patterns | GraphQL ESLint or `graphql-schema-linter` |
| Usage analytics | Power Deprecation Gatekeeper decisions | Apollo Studio, GraphQL Hive, or self-hosted (Inspector + Prometheus) |
| Schema registry | Single source of truth, versioned | Apollo Studio, GraphQL Hive, Cosmo registry |
| Composition CI | When federation arrives, validate subgraph composition | Rover (Apollo) or wgc (Cosmo) |

The cost of these tools is real (annual SaaS contract or self-hosted ops burden) but the cost of *not* having them in a public API is far higher: it's the cost of an unintentional breaking change reaching a production partner.

### 4.5 The schema evolution playbook (one page, lived-by)

```
Want to add something?     → Additive. Open PR. Schema-lint must pass. Merge after one review.
Want to change something?  → It's a deprecation. @deprecated with reason and replacement field.
                              Removal scheduled for now + 6 months minimum.
Want to remove something?  → Has it been deprecated for 6+ months AND has usage dropped below
                              the Gatekeeper threshold? If no, wait. If yes, breaking-change
                              reviewer + changelog + partner notice.
Want to rename something?  → That is a remove + add. Both deprecation window and breaking-change
                              process apply.
```

## 5. Authentication and Authorization Model

### 5.1 Authentication tiers

Three tiers, named explicitly to avoid the "we'll figure out auth later" failure mode:

| Tier | Mechanism | Use case | Rate limit class |
|---|---|---|---|
| **Anonymous** | No auth | Public read-only fields (e.g., catalog browse) | Lowest; per-IP |
| **API Key** | Bearer token in `Authorization` header | Third-party developer access; long-tail integrations | Medium; per-key |
| **OAuth 2.0** | Bearer JWT, standard authorization-code or client-credentials flow | End-user-acting-on-behalf scenarios; partner apps | Higher; per-user or per-client |
| **mTLS** | Client certificate at the edge | Partner-tier high-trust integrations | Highest; bypasses public rate limits |

OAuth uses **standard RFCs (6749, 7636 for PKCE, 8252 for native apps)** — no custom flows. JWTs are short-lived (15min access, longer refresh) and validated at the edge before reaching the GraphQL server.

### 5.2 Authorization model: field-level with directive-based enforcement

Authorization is enforced **at the field-resolver level, not at the query entry point**, because GraphQL's query shape makes endpoint-level authorization meaningless.

The recommended pattern is a `@requiresScope(scope: "...")` schema directive that resolves to a middleware check before the field's resolver runs:

```graphql
type Article {
  id: ID!
  title: String!
  body: String!
  draftNotes: String @requiresScope(scope: "article:read-internal")
  author: User!
}
```

This means:
- The schema **documents** the authorization model — anyone reading the SDL sees what's protected.
- The check is **declarative**, not hidden in resolver bodies.
- Auth changes show up in schema diffs, which means the Schema Steward sees them.

### 5.3 Introspection policy

Per 2026 best practice: **introspection is disabled in production**. The schema is published via:
- A docs site generated from SDL at release time.
- A downloadable SDL file at a versioned URL (`/schema/v1.graphql`).
- Optionally introspection enabled behind authentication for partner-tier consumers who need it for codegen.

## 6. Abuse-Protection Envelope

The seed brief flags abuse protection as a "designed-in, not bolted-on" requirement. This section names the full envelope.

### 6.1 Layered defenses

| Layer | Defense | Rationale |
|---|---|---|
| 1. Transport | TLS, request size limit (default 1MB), connection rate limit at the LB | Pre-GraphQL; catches the dumbest attacks cheaply |
| 2. Query parsing | Max depth (default 8), max breadth (default 100 selections per type) | Prevents pathological queries before validation |
| 3. Query validation | Cost analysis with per-field cost weights; reject queries above threshold (default 1000) | Catches expensive query shapes that depth/breadth alone miss |
| 4. Persisted operations | **Allowlist mode for partner-tier**; open mode for anonymous/API-key with stricter cost limits | The biggest single safety lever for public GraphQL |
| 5. Rate limiting | Per-IP for anonymous, per-key for API-key, per-user-and-per-client for OAuth, separate budget for mutations | Outermost defense |

### 6.2 Persisted operations: the central decision

Per the seed brief's enrichment: **the persisted-operations posture is a security fork, not a deployment detail**. This spec takes a tiered position:

- **Partner-tier (mTLS / high-value OAuth clients)**: persisted-operations allowlist *enforced* — only registered query hashes accepted. New queries go through a registration workflow.
- **API-key tier (third-party developers)**: persisted-operations *optional but incentivized* — registered queries get higher rate limits and lower cost weights.
- **Anonymous tier**: persisted-operations not required, but ad-hoc queries face the strictest cost analysis and depth limits.

The justification for not enforcing persisted operations on the anonymous tier is DX: third-party developers exploring the API in a playground should not need to register every query. The justification for enforcing it on the partner tier is risk: high-volume partner traffic should be reviewable and replayable, which only persisted operations provide.

### 6.3 Query cost analysis

Field cost weights are declared via a `@cost(complexity: N, multipliers: [...])` directive on resolver-heavy fields:

```graphql
type Query {
  articles(first: Int!, filter: ArticleFilter): ArticleConnection!
    @cost(complexity: 5, multipliers: ["first"])
}
```

A cost weight is required on any field that:
- Hits a backing service (default 5).
- Has a pagination argument (multiplier: the page size argument).
- Aggregates or computes across rows (default 10+).

CI fails if a new resolver lacks a `@cost` declaration on a flagged field. This is the only way to keep cost analysis accurate as the schema grows — making it part of the schema-evolution discipline rather than ops afterthought.

## 7. Operational and Observability Surface

### 7.1 Required signals at launch (non-negotiable)

| Signal | Granularity | Tool |
|---|---|---|
| Request rate, error rate, p50/p95/p99 latency | Per operation name | Prometheus + Grafana, or APM equivalent |
| Resolver-level latency | Per field on hot types | Apollo tracing format or OpenTelemetry spans |
| N+1 detection | Per resolver, per request | DataLoader metrics + alerts on per-request resolver call counts |
| Slow-query detection | Per persisted-query hash | Operational analytics; alert on p99 > threshold |
| Schema usage | Per field, per consumer tier | Apollo Studio / GraphQL Hive |
| Deprecation usage | Per deprecated field, per consumer | Powers the Deprecation Gatekeeper |
| Cost analysis hits | Distribution of query cost, blocked-query rate | Custom metric from cost middleware |

### 7.2 Alert thresholds (proposed starting values)

- Per-resolver p99 latency > 500ms for 5 minutes → page on-call.
- N+1 detector: any resolver firing >50 times in a single request → alert (not page).
- Cost-rejection rate >1% for any consumer tier → alert; >5% → page.
- Schema introspection request when introspection is disabled → log + count; spike → security alert.
- New `@deprecated` field with non-zero traffic after window expiry → alert to Deprecation Gatekeeper.

### 7.3 Schema linting in CI

A required CI gate runs on every PR that touches `schema/`:

1. SDL composes without errors.
2. Naming conventions (Section 2.2) hold.
3. Every type has a description; every field has a description (enforced strictly because public-API docs are generated from these).
4. Every list field uses Connection pagination (no raw `[T!]!` at the root).
5. Every field with a backing service has a `@cost` directive.
6. Every protected field has a `@requiresScope` directive matching a known scope.
7. GraphQL Inspector diff vs. main branch: no breaking changes without the `breaking-change-approved` label (which requires the Breaking-Change Reviewer's PR review).

## 8. REST Coexistence and Deprecation Strategy

### 8.1 Coexistence stance

**Parallel run is mandatory; sunset is data-driven, never date-driven alone.**

If a REST surface exists (per the brief's open question), GraphQL ships **alongside** REST, not as a replacement. The REST surface continues to receive bug fixes and security patches throughout the parallel-run period. New features may go GraphQL-only after a transition window, but existing features cannot be removed from REST until usage drops below threshold.

### 8.2 Sunset criteria

REST sunset is triggered when **all four** hold simultaneously:

1. Functional parity: every REST endpoint has a GraphQL equivalent and the equivalent has been live ≥6 months.
2. Migration tooling: a documented migration guide exists, with code examples in the top 3 SDK languages.
3. Usage threshold: REST endpoint traffic from non-archived consumers is <5% of equivalent GraphQL traffic for 4 consecutive weeks.
4. Partner-tier signoff: every partner-tier consumer has been notified and either migrated or granted an extension.

Any REST endpoint that fails criterion 3 or 4 stays live indefinitely. The portfolio approach is the maintainability win: don't fight to kill the long tail of low-traffic endpoints — they cost very little to keep running, and forcing migrations destroys partner trust.

### 8.3 Greenfield case

If no REST surface exists (the SuperClaude case per the codebase scan), GraphQL is the first public surface and this section is moot. The MVP scope (Section 9) becomes the entire launch decision.

## 9. MVP Scope vs. Full Vision

### 9.1 MVP (smallest viable shipping unit)

The MVP is the minimum surface that makes the schema-evolution policy meaningful — anything smaller doesn't prove the governance machinery.

**MVP includes:**
- Single monolithic graph, federation-ready by construction (Section 1).
- One domain fully modeled (e.g., the most-requested partner-integration target).
- Anonymous + API-key auth tiers. OAuth deferred to v1.1 unless a launch partner blocks on it.
- Persisted operations *available but not enforced* — registration workflow exists, partner tier opt-in.
- Cost analysis, depth limits, rate limiting all live.
- Observability: operation-level metrics, slow-query detection, deprecation tracking. Field-level resolver tracing deferred to v1.1 if it slows launch.
- Schema governance: all three roles named and one schema-review cycle completed before launch.
- Docs site with full SDL, generated examples, and a hosted playground (auth required).
- No subscriptions. No file uploads (deferred to v1.2).

**MVP explicitly excludes** (deferred to vision):
- Federated supergraph (Section 1.3 triggers determine adoption timing).
- OAuth 2.0 (unless a launch partner blocks).
- mTLS partner tier (added when first partner-tier integration arrives).
- Subscriptions / live queries.
- File uploads (multipart-form GraphQL or direct-upload pre-signed URL pattern).
- SDK generation for >2 languages.

### 9.2 Full vision (18–24 months out)

- Federated supergraph spanning 3+ domain subgraphs with a managed router.
- OAuth + mTLS partner tier live; persisted-operations allowlist enforced for partner tier.
- Subscriptions for selected real-time use cases (notifications, presence) via WebSocket or SSE — never for general data freshness.
- Multi-language SDK generation (TypeScript, Python, Go, Swift, Kotlin at minimum) from the schema registry.
- Schema registry with full version history, automated changelog, partner-facing migration guides.
- Cost analysis tuned by ML from observed traffic, not hand-set.
- Distributed caching at the gateway (per-operation HTTP cache for persisted queries).

## 10. Risks Justifying Rejection of GraphQL Entirely

The architect mandate requires naming the conditions under which the recommendation flips to REST/JSON+OpenAPI:

### 10.1 Reject GraphQL if any of these hold

1. **Single-team backend with no growth horizon**. The federation upside doesn't apply; the schema-governance overhead is pure cost. REST + OpenAPI is lower friction.
2. **Consumer base is purely third-party developers building hobbyist integrations**. GraphQL's learning curve and tooling expectations are higher than REST's. If the DX win of "ask for what you need" doesn't outweigh the onboarding tax, REST wins.
3. **Caching is the central performance requirement and queries are highly cacheable by URL**. REST's HTTP cache story is genuinely simpler than GraphQL's persisted-query + normalized-client cache stack. Don't pay GraphQL's caching tax if URL-based caching solves the problem.
4. **The team lacks the operational maturity to ship cost analysis, persisted operations, depth limits, and schema linting at launch**. Half-built GraphQL on a public surface is more dangerous than well-built REST. The 2026 enrichment is explicit: "fully open" GraphQL is no longer safe.
5. **The schema-evolution discipline cannot be staffed**. The three governance roles (Steward, Breaking-Change Reviewer, Deprecation Gatekeeper) are non-negotiable. If they can't be staffed, the public API will accumulate breaking changes and lose partner trust. REST + OpenAPI versioning is the safer fallback.
6. **The product is fundamentally CRUD on simple resources with predictable shapes**. GraphQL's flexibility is wasted; REST's simplicity is a feature.

### 10.2 Reject persisted-only GraphQL (but keep GraphQL) if

- The primary consumer is third-party developers in early exploration who would be blocked by a query registration workflow. Mixed-mode (Section 6.2) is the answer; don't force allowlist on the long tail.

### 10.3 Reject federation specifically (but keep GraphQL) if

- The Section 1.3 federation triggers haven't fired and the schema is <200 types. Stay monolithic. Federation has a real ops tax (router infrastructure, composition CI, subgraph deployment coordination) that only pays off above a certain team-and-schema scale.

## 11. Comparison Against REST (Three Axes)

| Axis | GraphQL (this spec) | REST + OpenAPI |
|---|---|---|
| **Developer experience** | Higher ceiling: one endpoint, exact-shape responses, generated SDKs from schema, in-IDE autocomplete. Higher floor: learning curve, persisted-operations workflow, depth/cost limits. Net: better for serious integrators, worse for casual ones. | Lower ceiling: over/under-fetching, version proliferation, hand-written client code. Lower floor: every web dev already knows it. Net: better for hobbyists, worse for deep integrations. |
| **Cost (infra + people)** | Higher: schema-governance roles staffed, schema registry SaaS or self-hosted, cost analysis CI, persisted-operations infrastructure, multi-layer caching. | Lower: HTTP cache solves most caching, no schema registry needed, no resolver tracing, OpenAPI tools are mature and cheap. |
| **Operational complexity** | Higher: query-level metrics, N+1 alerts, persisted-operation lifecycle, schema-diff CI gates. Failure modes are more varied. | Lower: 200/4xx/5xx baseline, endpoint-level metrics are sufficient, fewer dimensions to alert on. |

The architect-grade reading: GraphQL pays an upfront tax in governance and ops in exchange for **slower schema decay over time**. REST is cheaper at launch and erodes faster — version proliferation and endpoint sprawl are REST's long-term debt. This spec's whole point is to ensure the upfront tax actually buys the long-term win, by hardwiring the maintainability scaffolding from day 1.

## 12. Stack-Resolution Open Questions

These remain genuinely open and depend on the target product:

1. **Server library** — depends on backend language. Python: Strawberry (schema-first, type-hint-driven). TypeScript/Node: Apollo Server or GraphQL Yoga. Go: gqlgen. Rust: async-graphql. .NET: Hot Chocolate. The library choice does not affect this spec's architectural decisions; it only changes the syntax for directives and middleware.
2. **Schema registry / governance SaaS** — Apollo Studio, GraphQL Hive, Cosmo Studio, or self-hosted. Recommend Apollo Studio or GraphQL Hive for v1 unless cost or data-residency forces self-hosting.
3. **Router (when federation arrives)** — Apollo Router (Rust, mature) or Cosmo Router (newer, more open). Defer until federation triggers fire.
4. **Hosting** — out of scope here, but the parallel-run with REST mandates that the GraphQL server be independently deployable from the REST API.

## 13. Summary of Distinctive Stances

This spec's distinctive bias toward maintainability and extension scaffolding shows up in specific decisions other variants might soften:

1. **Federation-readiness as monolith discipline** (Section 1) — not "monolith now, federation later", but "monolith built so federation is a tooling change, not a refactor".
2. **Three named governance roles** (Section 4.3) — Steward, Breaking-Change Reviewer, Deprecation Gatekeeper. The bus factor on schema decisions must be >1.
3. **Resolver-layering as a CI-enforced rule** (Section 3) — not a convention. Import-linter or equivalent fails the build.
4. **`@cost` and `@requiresScope` directives mandatory in CI** (Sections 6.3 and 7.3) — the schema is where authorization and cost live, not buried in middleware.
5. **Tiered persisted-operations posture** (Section 6.2) — partner-tier enforced, anonymous-tier open. Refuses the false binary.
6. **Sunset criteria are data-driven AND partner-signoff-gated** (Section 8.2) — never date-only. Trust over speed.
7. **`@owner` directive and per-domain schema folders** (Section 2) — the schema is structurally ready to be split by team, even if it isn't yet.
8. **MVP defined by the minimum that proves the governance machinery works** (Section 9.1) — not the minimum that gets a query to return data. Anything smaller doesn't validate the model.

The deliberate architectural opinion: **a public GraphQL API's primary cost is not infrastructure, it is the cost of changing the schema for the next decade**. Every scaffolding decision in this spec is paid up front to keep that cost low.
