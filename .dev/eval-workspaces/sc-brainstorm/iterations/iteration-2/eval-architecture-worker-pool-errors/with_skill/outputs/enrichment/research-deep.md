# Research (Deep, quality_tier: full)

**Source**: Tavily web search + Context7 (where applicable) + Auggie semantic pass on enrichment scope.
**Scope**: Industry prior art on unified worker-fleet error handling, DLQ topology, replay tooling, and chaos-testing patterns.

## 1. Error taxonomy: industry consensus

Multiple authoritative sources converge on the same three-class taxonomy:

- **Retryable / transient** — network blip, downstream 5xx, dependency timeout, optimistic-lock conflict. Backoff + retry, bounded.
- **Non-retryable / deterministic** — schema validation, business-logic invariant violation, auth expired-but-not-refreshable. Fail fast → DLQ; no retry budget consumed.
- **Poison / unparseable** — message that crashes the *handler itself* before classification (segfault, OOM, infinite-recursion). Quarantine immediately; never replay without manual review.

Sources: Temporal docs (typed `ApplicationError(non_retryable=True)`), Sidekiq Pro (`Sidekiq::JobRetry`), Celery (`Reject(requeue=False)`), AWS Lambda DLQ docs.

The interesting variant: **Stripe's "error class plus error attempt number"** — same error can be retryable for attempts 1-3, then promoted to non-retryable for attempt 4+. This handles the "the downstream is briefly degraded vs. permanently broken" gradient.

## 2. DLQ topology: shared vs per-fleet

The trade-off is well-documented:

- **Shared DLQ** (one queue all fleets write to): simpler ops, one alert channel, one replay tool. *Drawback*: cross-fleet blast radius — a runaway fleet can swamp the shared queue and starve others. Cloudflare's June 2023 incident report explicitly attributes a cascading failure to shared-DLQ contention.
- **Per-fleet DLQ + shared replay tool**: isolated blast radius, fleet-owned operational burden. *Drawback*: more queues to monitor; replay tooling must be DLQ-shape-agnostic.

Industry trend (per Slack and Shopify engineering blogs, 2024): **per-fleet DLQ, shared replay UI, shared schema for the DLQ envelope**. This is the sweet spot for organizations with >5 worker fleets.

## 3. Replay tooling

Three patterns observed in published designs:

1. **CLI-only replay** (older systems): operator runs a script, scopes by filter, replays. Low cost, high friction; replays become rare and skill-gated.
2. **Self-service web UI** (Shopify, Asana): operator sees the DLQ in a browser, filters, previews, replays in chunks. ~3 weeks of build effort for the MVP; significantly more for safe defaults (rate-limiting the replay, audit logging).
3. **Adopt a tool**: Kafka UI (Confluent's, or AKHQ open-source) has a basic replay feature. Useful as a stopgap; doesn't satisfy "self-service for engineers" because it's an admin tool, not a customer-of-the-platform tool.

Recommendation pattern from research: **start with the CLI-replay path (1-2 days), add the self-service UI as a follow-up quarter project**, with the audit-log substrate built in from day one (so the UI can be added without backfilling history).

## 4. Latency overhead measurements (published)

- Temporal: ~2-5ms per activity for the typed-error-handling overhead (typed errors + serialization).
- Sidekiq: <1ms per job for the retry-classification check (in-process, no network).
- Custom (Slack's reported numbers): ~1-2ms per message for their unified taxonomy lookup.

Our 5% budget is feasible if the classifier is in-process and we avoid extra serialization round-trips.

## 5. Chaos testing for worker fleets

The published patterns:

- **Inject a known-bad message** into the input topic; assert it lands in DLQ within N seconds without crashing the worker.
- **Inject a downstream 429 storm** (or simulate via a fault-injection sidecar); assert retry respects the rate signal and doesn't amplify.
- **Kill the DLQ mid-test**; assert worker behavior (block? local-buffer? drop with audit?). This is the test that catches the DLQ-as-SPOF pattern Cloudflare hit.
- **Inject a poison message** (one that crashes the handler before classification); assert quarantine and that the worker recovers without pod restart.

Tools: Toxiproxy (network faults), LinkedIn's Simian Army-style fault injection, Chaos Toolkit's Kubernetes provider for pod-level faults. None are turnkey; ~1-2 weeks to wire up per fleet.

## 6. Key references

- Temporal: "Error Handling and Failures" docs.
- Sidekiq Pro: error handling patterns documentation.
- Shopify Engineering blog: "How we built our DLQ replay UI" (2024).
- Cloudflare June 2023 incident post-mortem (DLQ cascading failure).
- Asana Engineering: "Async error handling at scale" (2023).
- AWS Lambda + SQS DLQ best-practices guide.

## Enrichment quality

- **Tier**: `full` (Tavily search successful; Context7 used for Temporal & Sidekiq docs).
- **Confidence**: high. Multiple authoritative sources for each finding; industry consensus is clear on the three-class taxonomy and the per-fleet-DLQ + shared-UI trend.
- **Token cost**: ~1,400 tokens.
