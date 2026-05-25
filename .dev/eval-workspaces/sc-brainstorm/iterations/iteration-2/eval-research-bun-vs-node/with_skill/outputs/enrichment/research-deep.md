---
source: research-deep
quality_tier: primary
simulated: true
created: 2026-05-25T00:00:00Z
topic: "evaluate Bun vs Node for our backend services"
---

# Research-Deep: Bun vs Node Landscape (2026-Q2 snapshot)

## Bun Maturity Signals (2026-Q2)

**Release cadence.** Bun is on the 1.2.x line as of evaluation date. Oven shipped quarterly minor releases through 2025 with patch releases every 2-3 weeks. Major Node-compat regressions are tracked in the public issue tracker; the rate of new regressions in 2025 was lower than 2024 (Oven's own claim, corroborated by issue-close trend in the public GitHub data). Node, by contrast, follows the Node Foundation's LTS calendar: Node 22 is current LTS, Node 24 will go LTS in Oct 2026.

**Production adoption.** State-of-JS 2025 reports ~15% of newly-started TypeScript backend projects in 2025 chose Bun as their primary runtime; of those, ~40% cited build/test speed (not runtime) as the deciding factor. ~5% reported reverting to Node within 6 months, most commonly citing native-dep issues or observability gaps. Notable production users named publicly: Vercel (some internal services), Cal.com, and several mid-size SaaS shops; no FAANG-scale public adoption announcement at backend.

**Funding posture.** Oven (Bun's parent) closed a Series A in 2024 (~$7M, lead: Kleiner). No public Series B as of evaluation. Single-vendor concentration risk is real but not acute: the MIT license + portable codebase means a fork is technically possible if Oven pivots, though the practical maintenance lift would be substantial.

## HTTP Throughput Benchmarks

Three independent benchmarks consulted, all published 2025 or later, methodology summaries below. Numbers are illustrative — workload shape varies materially.

1. **TechEmpower Round 22 (2025)** — Bun's `bun.serve` posts ~2.3x raw req/s vs Node 22 `http` on the plaintext benchmark, narrowing to ~1.4x on the JSON benchmark, and ~1.15x on the database-fortunes benchmark. Conclusion: Bun's HTTP advantage shrinks dramatically as work-per-request increases.
2. **Cloudflare-published microbenchmark (2025)** — Fastify + Bun vs Fastify + Node 22 on a "validate JWT, query Redis, return JSON" workload: Bun ~1.3x throughput, ~10% lower p99. Memory: Bun ~30% lower steady-state RSS.
3. **Internal benchmark from a mid-size SaaS (public writeup, 2025-Q4)** — NestJS app on Bun vs Node 22, real production workload shape: Bun ~1.0x throughput (no meaningful difference), p99 within ±5%, memory ~20% lower. Conclusion from the writeup: "we expected a win and didn't get one; we got cheaper memory."

**Synthesis.** Bun's HTTP throughput claim is strongest on micro-benchmarks and weakest on realistic middleware stacks. For our existing Fastify-heavy fleet, the expected win is in the 1.0x-1.3x range on throughput and meaningful (15-30%) on memory. This does not clear our "substantially better" bar on its own.

## WebSocket Performance

**Architecture.** Bun's WebSocket implementation is built on top of uWebSockets.js (the C library), distinct from Node's userland `ws` package. uWebSockets is well-known for high connection-density and low memory-per-connection.

**Benchmarks.**
- **PocketIO 2025 comparison** — 10k concurrent WebSocket connections, broadcast pattern: Bun delivered ~2.1x message throughput at p99, ~40% lower memory per connection. Tail latency under sustained broadcast was less well-characterized; the writeup noted "occasional spikes" on Bun under sustained 8k+ msg/s broadcast load that did not appear on Node.
- **uWebSockets.js published numbers** — Bun-aligned, since it's the same library: ~1M messages/sec at 8k connections single-core, but these are isolated library numbers, not full-stack.

**Synthesis.** Bun's WebSocket story is materially stronger than its HTTP story. For the planned WebSocket gateway (10k+ connections, sub-100ms delivery target), the published evidence suggests a credible 2x throughput edge with a memory-density bonus, BUT with an open question on tail latency under sustained broadcast load. This is exactly the workload axis where Bun could clear our "substantially better" bar — pending pilot data on our specific message shape.

## Node Compatibility Surface (2026-Q2)

Bun's Node-compat layer covers most of the stable Node API surface. Specific gaps relevant to our stack:

- **`worker_threads`**: Partial parity. Basic spawn/message works; `MessagePort` transfer semantics have edge cases that have caused issues for libraries that lean heavily on it (one of our two internal libraries that uses worker_threads would need verification).
- **`async_hooks`**: Works for OpenTelemetry's context-propagation patterns; some less-common usages (custom hook lifecycles) have reported gaps.
- **`vm`**: Subset only. Not used in our stack today; flag for future.
- **`node:cluster`**: Bun's own cluster model differs; the API exists but the semantics around shared sockets are not identical. Most of our services use Kubernetes pod replicas, not in-process cluster, so this matters less.
- **`Buffer`** + **`Stream`**: Stable and well-tested.
- **`net`**, **`tls`**, **`http`**: Stable. dd-trace's patches attach correctly.

## Observability Surface (2026-Q2)

- **OpenTelemetry SDK**: Works under Bun via the Node-compat layer. Auto-instrumentation for HTTP, Fastify, Express, pg, ioredis: works in 2026-Q1 testing per a community report. Reported gaps: `@opentelemetry/instrumentation-grpc` (incomplete), some older pg driver versions (workaround documented). Manual instrumentation is unaffected.
- **Datadog APM (dd-trace)**: Officially supports Bun as of dd-trace v5.20+ (Q4 2025). Some plugin-level gaps remain — `@datadog/native-iast-taint-tracking` and the runtime-metrics module had compatibility caveats in 2025 that were partially closed by 2026-Q1.
- **pino**: Pure JS, works without changes. Output format identical.
- **Vector → Loki**: Transport-layer concerns only (stdout); no runtime dependency.

**Synthesis.** Observability parity is achievable on our specific stack with two caveats: gRPC instrumentation (not currently used) and Datadog runtime metrics (used; verify shim status before pilot).

## Native Dependency Matrix

| Dep | Status (2026-Q2) | Notes |
|---|---|---|
| `bcrypt` | works | Bun ships a pure-JS bcrypt-fallback; performance acceptable for auth-rate workloads. |
| `sharp` | works | NAPI binding works; verified on Bun 1.1+ in community reports. |
| `node-rdkafka` | works-with-caveats | Producer path stable in 2026-Q1 reports; historical segfault (2025-Q2) was patched; consumer side reported stable. **Verify on Bun version at pilot start.** |

## DX Signals

- **Install speed**: `bun install` is reproducibly 5-10x faster than `npm install` on our typical dependency tree size (~50-200 deps).
- **Test runner**: `bun test` is a Jest-API-compatible runner; benchmarks show 2-5x faster cold-start vs Jest, mostly from skipping transpile.
- **TypeScript**: First-class — no separate transpile step at runtime; build-time bundling via `bun build` competes with esbuild.
- **REPL/devloop**: `bun --watch` is faster than `node --watch` for our typical reload cycle.

DX wins are real and uncontested, but they accrue to *build/test* tooling, which is independently adoptable from runtime (see Out of Scope).

## Revert Path Mechanics

Bun maintains `package.json`-compatible semantics. A service that uses only stock Node APIs + npm packages can revert to Node by:

1. Change container entrypoint: `bun src/index.ts` → `node --import tsx src/index.ts` (or `node dist/index.js` if pre-built).
2. Remove any `Bun.*` API usage (`Bun.file`, `Bun.serve` shorthand, `Bun.password`, etc.). Lint rule recommended to enforce.
3. Re-run native-dep install if any deps had Bun-specific binary builds.
4. Re-attach observability shims that may have been Bun-specific.

If discipline is enforced via lint (`no-restricted-globals` rule for `Bun.*`), revert is measured in hours, not days. If not enforced, revert is measured in days-to-weeks depending on lock-in surface area.

## Confidence Statement

- **Tier**: `primary`
- **Token cost**: ~2400 tokens
- **Confidence**: medium-high on the published-benchmark synthesis; lower on the "what happens in *our* workload" question, which only pilot data answers.
