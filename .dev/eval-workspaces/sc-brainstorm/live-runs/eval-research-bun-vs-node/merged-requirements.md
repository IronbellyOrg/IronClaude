---
schema_version: "1.0"
source_seed_brief_path: .dev/eval-workspaces/sc-brainstorm/live-runs/eval-research-bun-vs-node/seed-brief.md
domain: research
strategy: systematic
adversarial_status: pass
convergence_score: 0.82
fit_to_intent: pass
unresolved_conflicts: []
---

# Merged Requirements — Bun vs Node.js Backend Runtime Evaluation

This is the canonical brainstorm output for the operator's request: a structured, evidence-based comparative evaluation of Bun and Node.js as candidate runtimes for backend services. Output supports a workload-scoped adoption decision, not an implementation plan.

## Functional Requirements

- **FR-1** — Produce a structured comparison of Bun and Node.js across six explicit axes: (1) runtime architecture, (2) performance, (3) ecosystem & library compatibility, (4) operations & supportability, (5) tooling & developer experience, (6) risk.
- **FR-2** — For each axis, document evidence-grounded findings sourced from deep external research (official runtime docs, public benchmarks, vendor support pages, migration write-ups). Findings must be attributable, not asserted.
- **FR-3** — Scope all findings and recommendations to *backend services* workloads. Browser, frontend, and edge-only deployment scenarios are excluded.
- **FR-4** — Within the ecosystem axis, treat native-module compatibility, APM / observability agent support, and managed FaaS hosting support as top-line concerns — not buried sub-bullets.
- **FR-5** — Produce a workload-scoped recommendation framework expressed as a decision rule: "adopt where X, pilot where Y, defer where Z, reject where W." The framework must be actionable — it must let the operator classify a given workload into one of these outcomes.
- **FR-6** — Surface a structured risk register covering ecosystem-compatibility, operational maturity, tooling coverage, hosting, talent / hiring, lock-in, and mirror risk of staying on Node without revisiting workflow.
- **FR-7** — Surface explicit open questions that the operator must answer before applying the decision rule (workload class, risk tolerance, hard library dependencies, hosting model, evaluation horizon).

## Non-Functional Requirements

- **NFR-1 (Evidence rigor)** — Every comparison axis must cite or reference external research. No-source assertions are not acceptable.
- **NFR-2 (Comparative honesty)** — Trade-offs must be explicit. False equivalence ("both are fine") and uncritical advocacy ("Bun is just faster") are both unacceptable framings.
- **NFR-3 (Performance interpretation)** — Performance comparisons must distinguish synthetic-microbenchmark numbers from realistic-stack measurements, and must call out that public, statistically-rigorous tail-latency comparisons are scarce.
- **NFR-4 (Compatibility surface)** — The evaluation must explicitly enumerate the categories of native modules, APM / observability agents, and hosting platforms where Bun support is incomplete or evolving, and require case-by-case validation rather than assumption.
- **NFR-5 (Operational maturity framing)** — Node.js's LTS policy, security working group cadence, and incident track record must be presented as the key operational-maturity differentiator. Bun's posture must be characterized accurately as a younger runtime with no Node-equivalent LTS commitment at evaluation time.
- **NFR-6 (Research-only enrichment)** — The evaluation must rely on deep external research; codebase introspection is excluded per operator constraint. Provenance must record this constraint.
- **NFR-7 (Freshness caveat)** — The evaluation must include a freshness statement noting Bun's rapid release cadence and the need to re-validate compatibility / performance claims against the runtime release current at decision time.
- **NFR-8 (Decision-rule actionability)** — The recommendation framework must be expressible as a checklist or rule a reviewer can apply to any candidate workload, not just narrative prose.

## Acceptance Criteria

- **AC-1** — Six comparison axes are present, each with a non-empty evidence-grounded findings section keyed to backend-services workloads.
- **AC-2** — Performance, ecosystem, and operations axes each explicitly distinguish "Bun advantage", "Node advantage", and "context-dependent" findings.
- **AC-3** — Native-module, APM / observability, and managed FaaS hosting compatibility appear as distinct, top-line elements of the ecosystem axis (not buried).
- **AC-4** — A decision-rule framework (adopt / pilot / defer / reject) is present and uses workload-scoped predicates, not blanket advice.
- **AC-5** — Pilot exit criteria are documented: performance gates, compatibility gates, operability gates, and a time-bound review window.
- **AC-6** — A structured risk register exists with at least likelihood and mitigation columns, and includes mirror-risk on Node (DX / cold-start / install-speed advantages forfeited if Node is retained without revisiting workflow).
- **AC-7** — All open questions from the seed brief are either resolved in requirements or surfaced explicitly in `## Open Questions` — none silently dropped.
- **AC-8** — All `must_preserve` anchors from the seed brief are traceable to at least one requirement, acceptance criterion, or risk row (see `## Provenance`).

## Risks

| ID | Risk | Likelihood | Mitigation |
|----|------|------------|------------|
| R-1 | Native-module / N-API compatibility gaps on Bun (Sharp, bcrypt, native DB drivers, custom addons) | Medium | Enumerate critical native dependencies pre-pilot; validate each on the target Bun release; treat unsupported modules as pilot-blockers. |
| R-2 | APM / observability agent gaps on Bun (Datadog, New Relic, OpenTelemetry, Sentry) | Medium | Consult each vendor's current Bun support statement; validate end-to-end traces / metrics / errors on a pilot workload before broader rollout. |
| R-3 | Managed FaaS hosting does not offer Bun as a first-class runtime | Medium-High (workload-specific) | Confirm hosting platform Bun support before pilot scoping; fall back to container deployment if FaaS is mandatory. |
| R-4 | Operational maturity gap — no Node-equivalent LTS / security WG commitment from Bun | High (for regulated / risk-averse environments) | Treat as a hard gating criterion for mission-critical workloads; pilot only on lower-criticality services. |
| R-5 | Tooling coverage gaps (debugger, profiler, flame-graph workflows) | Medium | Validate observability and debugging workflows on the target Bun release before pilot; document gaps with workarounds. |
| R-6 | Lock-in to Bun-only APIs (`Bun.serve`, `Bun.file`, native bundler) | Medium | Restrict pilot code to portable APIs unless Bun-specific gains are explicit and justified; document any Bun-specific dependencies. |
| R-7 | Talent / hiring risk — Bun-specific operational experience scarcer than Node | Low-Medium | Plan onboarding documentation and runbook coverage; do not pilot on a team with no Bun exposure. |
| R-8 | Strategic-bet risk — Bun is a single-vendor-led runtime; long-term governance and funding posture differ from foundation-governed runtimes | Low-Medium | Re-validate strategic posture at each pilot review; do not over-index a roadmap on a single Bun-only adoption. |
| R-9 | Mirror risk on Node — staying on Node without revisiting workflow forfeits documented DX / cold-start / install-speed gains | Medium | Even if Bun is rejected runtime-wide, evaluate `bun install` / `bun test` / `bun --bun` selectively at the tooling layer. |
| R-10 | Freshness drift — Bun's rapid release cadence outdates compatibility / performance findings quickly | High | Include freshness caveat (NFR-7); re-validate at decision time and at each pilot checkpoint. |

## Open Questions

- **OQ-1** — Which specific backend workload classes is the team evaluating (HTTP APIs, queue workers, long-running daemons, edge / FaaS handlers)? The decision rule's predicates depend on this.
- **OQ-2** — What is the team's risk tolerance for adopting a younger runtime (Bun) versus an established one (Node.js LTS)? What is the evaluation horizon (next quarter, next year, next platform refresh)?
- **OQ-3** — Are there hard library / framework dependencies (native modules, AWS SDK quirks, instrumentation agents) that gate Bun adoption? These must be validated before pilot scoping.
- **OQ-4** — Is the desired outcome an immediate adoption decision, a pilot, or a watch-and-revisit posture? This shapes how aggressively the decision rule is applied.
- **OQ-5** — Are managed FaaS platforms (Lambda, Cloud Functions, Vercel, etc.) in scope, or is container-based deployment acceptable? Hosting model materially constrains the option set.
- **OQ-6** — How should performance vs. ecosystem-maturity weighting be calibrated across workload classes? The decision rule encodes this implicitly; an explicit policy may be valuable.

## Provenance

This section attributes each requirement, criterion, risk, and open question to its source variant(s) and seed-brief anchor(s). It is mandatory and brainstorm-owned; it is not in the adversarial merge internals.

### Functional Requirements

- **FR-1** (six-axis comparison) — V1 (analyzer/opus) base; reinforced by V2 (architect/sonnet). Seed anchor: "comparative evaluation (Bun vs Node)" + Success Criterion "comparative axes explicitly enumerated."
- **FR-2** (evidence-grounded findings) — V1 + V3 (scribe/haiku). Seed anchor: "deep research enrichment required."
- **FR-3** (scope: backend services) — V1 + seed brief. Seed anchor: "backend services" (component) + Out of Scope items.
- **FR-4** (native modules / APM / FaaS top-line) — V2. Seed anchor: "ecosystem maturity and library compatibility."
- **FR-5** (decision-rule framework) — V3 (introduced decision rule); V1 (workload scoping) integrated. Seed anchor: "evaluation produces an actionable adoption / retention / pilot decision."
- **FR-6** (risk register) — V3 (formal layout) + V2 (compatibility surfaces). Seed Success Criterion: "risks and unknowns are surfaced."
- **FR-7** (open questions) — V3 (structured open-question framing) + seed brief Open Questions section.

### Non-Functional Requirements

- **NFR-1** (evidence rigor) — V1 + V3. Seed Constraint: "deep research is required (not light)."
- **NFR-2** (comparative honesty) — V1. Seed Success Criterion: "trade-offs are made explicit — no false-equivalence framing."
- **NFR-3** (performance interpretation) — V1 + research-deep.md §2.
- **NFR-4** (compatibility surface enumeration) — V2 + research-deep.md §3.
- **NFR-5** (operational-maturity framing) — V2 + research-deep.md §4.
- **NFR-6** (research-only enrichment) — Brainstorm normalization. Seed anchor: "no codebase enrichment (explicit operator constraint)."
- **NFR-7** (freshness caveat) — research-deep.md §8 "Note on freshness."
- **NFR-8** (decision-rule actionability) — V3.

### Acceptance Criteria

- **AC-1** — V1 (six-axis structure).
- **AC-2** — V1 + V2 (advantage breakdown).
- **AC-3** — V2 (top-line elevation).
- **AC-4** — V3 (decision-rule framework). Seed anchor: "evaluation produces an actionable adoption / retention / pilot decision."
- **AC-5** — V3 (pilot exit criteria).
- **AC-6** — V3 (risk register format) + V1 (mirror-risk on Node).
- **AC-7** — Brainstorm normalization (open-question completeness check).
- **AC-8** — Brainstorm normalization (anchor traceability gate).

### Risks

- **R-1, R-2, R-3, R-5, R-6** — V2 (compatibility / tooling / hosting surfaces) reinforced by research-deep.md §3, §4.
- **R-4, R-8** — V1 + V2 (operational maturity / strategic-bet framing).
- **R-7** — V2 + V3 (talent / hiring).
- **R-9** — V1 (mirror-risk on Node).
- **R-10** — research-deep.md §8 (freshness).

### Open Questions

- **OQ-1 through OQ-5** — Carried verbatim from seed-brief `## Open Questions`. Not resolved by adversarial debate.
- **OQ-6** — Surfaced during V1↔V2 round-2 tension on performance vs. ecosystem weighting. Logged in `adversarial/debate-transcript.md` round 2.

### Seed-Brief Anchor Traceability

Every `must_preserve` anchor maps to at least one requirement / criterion / risk:

| Anchor | Mapped to |
|--------|-----------|
| Bun runtime as primary candidate under evaluation | FR-1, FR-2, FR-3 |
| Node.js runtime as incumbent / comparator | FR-1, FR-2 |
| backend services as the workload context | FR-3, AC-1, AC-3 |
| deep research enrichment required | NFR-1, NFR-6, Provenance |
| no codebase enrichment (explicit operator constraint) | NFR-6, Provenance |
| evaluation produces an actionable adoption / retention / pilot decision | FR-5, AC-4, AC-5 |

No `out_of_scope` anchor was promoted into a requirement. No `must_preserve` anchor was silently dropped.

### Codebase enrichment

Skipped per operator constraint ("No codebase enrichment"). Recorded in NFR-6 and in this Provenance section.

### Research enrichment

Quality tier: `primary`. Artifact: `enrichment/research-deep.md`. Sources: official Node.js and Bun docs; public HTTP and runtime benchmarks; vendor APM / observability documentation; hosting platform documentation; migration and post-mortem write-ups from teams piloting Bun in backend services.
