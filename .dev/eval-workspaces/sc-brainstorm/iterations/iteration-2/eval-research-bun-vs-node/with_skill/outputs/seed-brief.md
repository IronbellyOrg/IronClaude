---
topic: "evaluate Bun vs Node for our backend services"
domain: research
strategy: systematic
depth: standard
proposal_count: 3
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: bun-vs-node-backend-evaluation

## Socratic Dialogue Record

The following 10 questions (research-domain STANDARD tier: Decision-frame + Validate batches) were posed and answered to ground the topic.

### Decision-frame batch

**Q1. What's the decision you're trying to support — full migration, selective adoption (new services only), or just an informed "no for now"?**
A: Selective adoption for new services first. We don't want to migrate the existing fleet (~40 Node services on Node 20 LTS) unless a small pilot shows a compelling reason. The output of this brainstorm should make the "yes for next greenfield service" or "no, stay Node" call defensible.

**Q2. What's the time horizon — decide this quarter, this year, or "when Bun looks more stable"?**
A: Decide this quarter. We have a new service (a real-time WebSocket gateway) starting design in 6 weeks; that team is asking whether they can pick Bun. If we don't decide, they'll pick Node by default — which is fine, but we'd like a real answer.

**Q3. What workloads matter most — HTTP API throughput, WebSocket fanout, CPU-bound work, cold-start latency, build tooling speed?**
A: WebSocket fanout (10k+ concurrent connections, sub-100ms message delivery) and HTTP API throughput (the existing fleet sits at ~50k req/s aggregate). Build tooling speed matters secondarily because CI is slow today. Cold-start doesn't matter — we run long-lived processes, not Lambda.

**Q4. What's the bar that "Bun wins" must clear — same as Node, marginally better, or substantially better (e.g., 2x)?**
A: Substantially better on at least one axis we care about (WebSocket fanout, throughput, or developer experience) AND no worse on operational stability. A 10% throughput edge doesn't move the needle against the cost of a new runtime in the supportable surface.

**Q5. What's the cost frame — what would we spend to switch a service? what risk is unacceptable?**
A: Cost: ~2 engineering weeks to port a typical service, plus ~1 week of ops work (observability adapters, deploy pipeline updates). Unacceptable risk: a production incident traceable to Bun runtime instability that we can't quickly fix or revert. We need a credible revert path.

### Validate batch

**Q6. What does our current stack look like — frameworks, observability, deploy targets?**
A: Node 20 LTS on Kubernetes (EKS). Frameworks: Fastify (most services), Express (older), NestJS (one large service). Observability: OpenTelemetry SDK + Datadog APM + pino logs to Vector → Loki. Deploy: container images via Buildkite → ECR → ArgoCD.

**Q7. What ecosystem dependencies are load-bearing — native modules, specific npm packages, TypeScript transpilation?**
A: TypeScript everywhere (esbuild for builds today). Native deps: `bcrypt`, `node-rdkafka`, `sharp` are the three that matter. About 30% of services use one or more. The rest are pure-JS npm.

**Q8. Are there organizational signals — team appetite for new runtimes, hiring concerns, existing internal libraries that assume Node?**
A: Team appetite is mixed. Two senior engineers are enthusiastic, six are skeptical, the rest are neutral. Hiring: we hire JS/TS engineers, not "Bun engineers" — but anyone hireable would learn Bun quickly. Internal libraries (~12 packages) target Node 20+; most are pure-JS but two use `worker_threads` directly.

**Q9. What's the failure mode of "we pick Bun and regret it"? What's the failure mode of "we stay on Node and regret it"?**
A: Regret Bun: production incident from a runtime bug, no upstream fix in time, expensive revert. Regret Node: 12 months from now we're paying real money on infra that Bun would have shaved, OR our DX is visibly worse than peer companies and it hurts hiring. Both are possible; the Bun regret is sharper-edged (single incident), the Node regret is dull-but-cumulative.

**Q10. Who consumes this brainstorm — engineering leadership, platform team, individual service teams?**
A: Platform team owns the decision (we set the runtime allowlist). Engineering leadership signs off if there's a material risk or cost. Individual service teams consume the resulting policy — they don't get to pick freely either way.

## Problem Statement

The platform team must decide this quarter whether to allow Bun for new backend services, starting with a planned real-time WebSocket gateway. The decision frame is **selective adoption, not migration**: we are not moving the existing 40-service Node 20 LTS fleet. The bar "Bun wins" must clear is **substantially better on at least one workload axis we care about (WebSocket fanout, HTTP throughput, or DX) AND no worse on operational stability**. A 10% edge is insufficient; a 2x edge with stable ops is sufficient. The forcing function is the WebSocket gateway team requesting a runtime decision in ~6 weeks; without an answer, they will default to Node, which is acceptable but leaves the question unresolved.

## Known Context

- Existing fleet: ~40 Node 20 LTS services on EKS, ~50k req/s aggregate steady-state.
- Frameworks: Fastify (most), Express (older), NestJS (one large service).
- Observability: OpenTelemetry SDK + Datadog APM + pino → Vector → Loki.
- Deploy: Buildkite → ECR → ArgoCD.
- TypeScript everywhere (esbuild builds).
- Load-bearing native deps used by ~30% of services: `bcrypt`, `node-rdkafka`, `sharp`.
- Internal libraries: ~12 packages, two use `worker_threads`.
- New service (WebSocket gateway): 10k+ concurrent connections, sub-100ms message delivery, design starts in 6 weeks.
- Team appetite: 2 enthusiastic, 6 skeptical, rest neutral.
- Bun version at evaluation time: 1.2.x stable line (as of 2026-Q2).

## Constraints

- Decision must be defensible to engineering leadership (data, not vibes).
- Must not require touching the existing 40-service fleet.
- Production incident from Bun runtime instability is an unacceptable risk without a credible revert path (estimate: ≤1 sprint to revert).
- OpenTelemetry + Datadog + pino observability surface must be preserved or equivalent.
- The three native deps (`bcrypt`, `node-rdkafka`, `sharp`) must work or have documented equivalents.
- TypeScript-everything must continue to work.
- Decision deadline: end of this quarter (Q2 2026).

## Success Criteria

- A written policy stating allowlist status (allow / pilot-only / disallow) for Bun across new services, with conditions.
- For each of the three workload axes (WebSocket, HTTP, DX), a quantitative or evidence-based comparison.
- Documented revert path for any pilot service.
- Native-dep compatibility matrix (works / works-with-shim / blocked).
- Risk register with severity, mitigation, and explicit out-of-scope items.

## Open Questions

- Bun's Node compat layer fidelity for our specific surface: does it cover all of OpenTelemetry's auto-instrumentation hooks? Datadog dd-trace internal pollyfills?
- Real-world WebSocket performance under our exact load shape (10k+ connections, broadcast pattern) — published benchmarks are mostly request/response.
- Memory profile under sustained load — Bun's GC tuning surface is smaller than V8's; do we lose flexibility we'll regret?
- Worker-thread story — two internal libraries use `worker_threads`; Bun has partial parity but the gaps aren't well documented.
- Long-term governance: who owns the Bun-version bump cadence inside the platform team? Node LTS is well-understood; Bun's stability cadence is younger.
- License + supply chain: Bun is MIT, Oven raised series-A in 2024 — what's the "if Oven pivots away" failover?

## Enrichment Context

Research-deep enrichment ran (`research-deep` track, quality_tier: primary). Full output at `enrichment/research-deep.md`. Key signals folded into the brief:

- Bun 1.2 (2026 line) closes most Node-compat gaps for stock HTTP/Express/Fastify; benchmarks from independent sources show 2-3x HTTP throughput on simple endpoints, narrowing to 1.2-1.5x on realistic middleware stacks.
- WebSocket implementation in Bun uses uWebSockets.js under the hood, distinct from Node's `ws` — published benchmarks (PocketIO comparison, 2025) show ~2x message-throughput at 10k connections, but tail latency under broadcast load is less well-characterized.
- OpenTelemetry support is via Bun's Node-compat layer; auto-instrumentation works for HTTP + most major libraries; gaps reported in `@opentelemetry/instrumentation-grpc` and some pg drivers.
- Native deps: `bcrypt` works (pure-JS fallback in Bun stdlib is fast), `sharp` works via NAPI, `node-rdkafka` partially works (segfault reported in 2025 on heavy producer load; status mixed in 2026).
- Adoption signal: ~15% of new TypeScript backend services started in 2025 chose Bun per State-of-JS 2025; ~40% of those chose it specifically for build/test speed, not runtime.
- Revert path: Bun ships drop-in `package.json` compatibility; revert to Node is `node` instead of `bun` at entrypoint, plus removing any Bun-specific APIs (`Bun.file`, `Bun.serve` shorthand). If discipline is enforced via lint, revert is a few hours.

Confidence on enrichment: medium-high. Quantitative benchmarks are from public sources and may not match our exact workload — pilot data will be more authoritative.
