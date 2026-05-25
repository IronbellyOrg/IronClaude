---
proposal_id: 5
persona: performance
model: sonnet
lens: latency budget, throughput, resource cost, hot-path overhead
---

# Proposal 5 — Performance: The 5% Latency Budget Is The Hard Constraint

## Position

The seed brief sets a ≤5% per-message latency overhead constraint. That is not a "nice to hit" — it's a budget the new subsystem will accidentally blow if every prior proposal's additions land naively. Typed-error classes are cheap (~5µs); audit-log writes are not (Postgres write, ~3-5ms); PII redaction on hot path is not (~50µs per regex scan × N fields); replay-rate-limit checks via a shared counter are not (~1ms Redis lookup). Without explicit budget allocation per feature, we ship a 15% regression and back out half the subsystem in Q4.

## Latency budget allocation (with measurements)

Per-message overhead breakdown (from `research-deep.md` benchmarks + projected costs):

| Subsystem feature | Projected p99 overhead | Hot path? |
|---|---|---|
| Typed-error classification (in-process) | ~10µs | yes |
| Retry policy lookup | ~5µs | yes |
| Per-fleet metrics emission | ~50µs | yes |
| PII redaction at DLQ write | ~80µs | only on error |
| DLQ write (Kafka) | ~2ms | only on error |
| DLQ write (Postgres) | ~5ms | only on error |
| Audit log write | ~3ms | only on replay / DLQ-write |

**Hot-path budget**: ~65µs total. On a 10ms baseline, that's 0.65% — well inside 5%.
**Error-path budget**: ~10ms (Postgres) or ~5ms (Kafka). On a 10ms baseline, that's 50-100% — but it's the error path, by definition the message has already failed.

## Performance requirements

- **NFR-perf-1** — Hot-path overhead ≤ 100µs p99 measured on a representative production handler. Verified by a per-PR benchmark (the harness QA proposes can do this).
- **NFR-perf-2** — DLQ write latency must not block worker liveness. Use async writes with a bounded queue; if the queue is full, the policy decision is per-fleet (block, drop-with-audit, or local-spool).
- **NFR-perf-3** — Audit log writes are batched (1000 entries or 1 second, whichever first). Sync mode available for security-critical replays where audit immediacy matters more than throughput.
- **NFR-perf-4** — Replay throughput: 100 msg/sec default (DevOps + security agree on this for rate-limit/audit reasons). For "all hands on deck" recovery scenarios, an SRE-only mode supports up to 10k msg/sec with explicit audit.
- **NFR-perf-5** — Cost overhead: aggregate cloud cost of the new subsystem (Kafka/Postgres DLQ storage, audit log, metrics emission) ≤ 20% of the current `$40k/quarter` retry cost baseline. The math: 4× retry-cost reduction (per seed brief success criterion) - 1× subsystem cost = net 3× saving.

## Where I push back

**Architect**: "metrics emission" is one bullet in §observability. Naive metric emission at the per-message granularity with high-cardinality labels is the classic Prometheus-cardinality-explosion footgun. Specify: per-fleet metrics use bounded label sets (`error_class`, `outcome`, `fleet`); per-message context is *traced*, not counted. Otherwise the metrics infrastructure becomes the new failure mode.

**DevOps**: migrating `email-dispatch` first is right operationally but `email-dispatch` is also the *highest-volume* fleet (~5M messages/day). It's the worst place to discover a latency regression. Run the new subsystem against `email-dispatch` in shadow mode (log decision, don't enforce) for one week before flipping enforcement.

**QA**: chaos tests don't measure latency. Add a 10th test class: **latency regression test** — measure p99 overhead with full subsystem vs baseline, fail PR if delta > budget. This is what catches "an audit-log write was synchronously inserted in the hot path by mistake."

**Security**: PII redaction *at write time* is the right place (vs at read time, which is too late). But: pre-compute the redaction-field set per producer schema *at deploy time*; do NOT do regex-discovery per message.

## Throughput floor

Current worker fleets aggregate throughput: ~15M messages/hour across all 12 fleets. **The new subsystem must not reduce this to <13M/hour** (≤15% degradation absolute, with the budget being ≤5% per message — the difference is GC, scheduling, sidecar contention).

## What I'd push back on hardest

Anyone who treats the 5% latency budget as a soft goal will discover, six months in, that the subsystem they shipped is being silently disabled by fleets that can't tolerate the overhead. Hard budgets enforced by CI benchmarks, or the subsystem becomes a recommendation rather than a platform.

## Cost

~0.5 sprint for the per-PR benchmark harness. Latency-regression-test integration with the chaos suite: included in QA's 1.5 sprints (joint cost). Cardinality audit on metrics: 1 day.
