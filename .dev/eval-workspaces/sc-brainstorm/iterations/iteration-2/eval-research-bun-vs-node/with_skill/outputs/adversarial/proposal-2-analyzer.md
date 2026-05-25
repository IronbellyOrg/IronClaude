---
proposal_id: 2
persona: analyzer
model: sonnet
lens: evidence quality, benchmark interpretation, risk decomposition
---

# Proposal 2 — Analyzer: Bun Wins Only on WebSockets at Our Scale; Pilot a Lower-Blast-Radius Service First

## Position

The evidence in the enrichment material doesn't support a general "Bun is faster" claim at our workload shape — it supports a specific "Bun is materially better at WebSocket fanout" claim plus a "Bun has nicer DX" claim. The architect's instinct to pilot is right; the choice to pilot *on the WebSocket gateway* is wrong. **Pilot on a lower-blast-radius service first.** The WebSocket gateway is exactly the wrong place to discover that Bun's tail-latency under broadcast load is worse than published numbers suggest.

## Reading the benchmark data correctly

The HTTP-throughput numbers degrade rapidly with realistic work-per-request:
- Microbenchmark: 2.3x
- "JWT + Redis + JSON": 1.3x
- Real NestJS prod workload (the most relevant public data point): **1.0x**

For our Fastify-heavy fleet doing real work, the expected HTTP-throughput delta is 1.0x-1.3x. This does NOT clear our "substantially better" bar (seed brief Q4). The memory delta (15-30% lower RSS) is real but doesn't move the decision — we're not memory-bound in production today.

The WebSocket numbers are different:
- PocketIO 10k-connection broadcast: ~2.1x throughput, ~40% less memory per connection
- BUT: "occasional spikes" in tail latency under sustained 8k+ msg/s broadcast that didn't appear on Node

That last sentence is the load-bearing detail. The architecture team's pilot proposal puts the test workload on the exact axis where tail-latency anomalies appear. If the WebSocket gateway is the pilot and we hit those spikes in production, we have a SEV with a customer-visible symptom on the most-hyped Bun strength.

## Recommended pilot scope (counter-architect)

**Pilot service**: A *lower-blast-radius* greenfield service. Concrete candidates from the fleet today:
- A new internal-only data-validation API (low traffic, no customer impact if degraded).
- The forthcoming feature-flag-eval gateway (high QPS but well-isolated from user-facing latency; degrades to default flags gracefully).
- A batch-ingestion HTTP receiver (no real-time SLO).

Any of these surfaces Bun's runtime behavior under our deploy pipeline, observability stack, and ops practices without putting a customer-facing critical path on a runtime we haven't validated on our infra.

**Why not the WebSocket gateway**: The WebSocket gateway is the service where the *value* of Bun is highest *and* the *cost of regression* is highest. Either we ship it on Node first (catch the operational baseline, build the team's Bun familiarity on a smaller service, then port if numbers warrant), or we accept that the pilot itself carries SEV risk on a critical-path customer experience.

## Evidence quality bar for the report (FR4)

Every claim in the workload-axis comparison report must satisfy:

1. **Source attribution**: name + URL + date of publication.
2. **Version stamps**: Bun version and Node version under test. ("Bun is faster" with no version is unfalsifiable.)
3. **Workload shape disclosure**: req/s? msg/s? connection count? payload size? At least one paragraph per benchmark describing what was actually measured.
4. **Internal corroboration**: at least one internal benchmark on a workload representative of *our* services, run on *our* deploy pipeline. External benchmarks are signals; internal benchmarks are evidence.

Without this bar, the report becomes "we picked some numbers that supported the decision we already made." With it, the report is auditable.

## Native-dep risk decomposition

The seed brief flags `bcrypt`, `node-rdkafka`, `sharp`. My read of the enrichment data:

- `bcrypt` and `sharp`: low risk. Both work; sharp via NAPI is well-validated by the broader Bun community.
- `node-rdkafka`: medium risk. Producer path historically had a segfault; status reported "patched" in 2026-Q1 but I'd want **direct verification on the exact Bun version at pilot start**, not "the community says it's fine." Kafka-producer regressions in production are catastrophic — they look like "messages succeeded then disappeared," which is the worst kind of failure to debug.

**Recommendation**: If `node-rdkafka` is `works-with-caveats` on the pilot Bun version, **exclude Kafka-producer services from the allowlist** for v1 of the policy. This is FR3 / NFR3. Revisit when status is `works` on two consecutive Bun minor releases.

## Risk that's underweighted in the architect's proposal

**Observability parity risk** (R2 in merged requirements) is severity HIGH for a reason: the pilot service is the most experimental thing we're running, AND it's the place we have least telemetry on. If dd-trace runtime metrics has a gap and the gap hides a memory leak, the SEV will look like "service started OOMing and we don't know when it started." This must be addressed before pilot traffic — not addressed in parallel with it.

## What I'd push back on

The architect's "pilot the WebSocket gateway" framing optimizes for proving the strongest Bun claim, which is methodologically correct but operationally risky. The scribe's "produce a clear policy" framing is necessary but underspecifies the *evidence* the policy is built on. Combine: produce the policy AND make the policy contingent on a lower-blast-radius pilot, then graduate to WebSocket if the pilot succeeds.

## Cost

Same as architect's 4-week estimate, but spent on a smaller pilot service. The WebSocket gateway proceeds on Node in parallel; if pilot graduates, the WebSocket team's *second* version is on Bun in 2026-Q4 with operational confidence — not their first version on a runtime we haven't validated.
