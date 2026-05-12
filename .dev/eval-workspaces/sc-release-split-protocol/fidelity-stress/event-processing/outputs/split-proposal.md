# Split Proposal — Event Processing Pipeline v2.0

## Discovery Analysis

### Spec Summary

Event Processing Pipeline v2.0 contains 10 requirements (R1-R10) covering ingestion, classification, dispatch, error handling, handler contracts, DLQ management, observability, lifecycle management, ordering guarantees, and runtime configuration. The spec is 460 lines with deeply cross-referenced requirements.

### Dependency Chain Analysis

**R2 (Classification) is the universal dependency hub.** Every other requirement references R2's tier definitions (T1-T4) or category definitions (financial, security, lifecycle, telemetry, configuration, unclassified). This makes R2 impossible to isolate.

**Cross-requirement formula dependencies:**
- R1's rate limit formula: `base_rate_limit * (1 - current_queue_depth / backpressure_high_watermark)` — directly references R3's `backpressure_high_watermark` (80,000 events) and `backpressure_low_watermark` (20,000 events)
- R4's retry policies reference R2's tier table for retry budgets: T1 = 5 retries/60s, T2 = 3 retries/30s, T3 = 1 retry/10s, T4 = 0 retries
- R9's ordering enforcement blocks on R4's retry windows: financial/security/configuration events block same-entity events during retry, bounded by T1=60s, T2=30s total retry windows
- R3's load shedding references R2's tier definitions for eligibility: yellow sheds T4, red sheds T3+T4, critical sheds T2+T3+T4, T1 never shed
- R6's DLQ disposition rules map directly to R2's tiers: T1=`requires_immediate_attention`, T2=`requires_manual_review`, T3=`auto_retry_eligible`, T4 never in DLQ
- R5's SLA enforcement uses R2's `max_processing_latency` per tier: T1=500ms, T2=2000ms, T3=10000ms, T4=30000ms

### Standalone Value Assessment

**Can any subset deliver standalone value and be validated through real-world use?**

No. The three processing stages (ingestion, classification, dispatch) form a pipeline — ingestion without classification produces a queue of unrouted events. Classification without dispatch produces classified events with nowhere to go. Dispatch without ingestion and classification has no events to dispatch.

The spec explicitly states the three-tier processing model: `ingestion -> classification -> dispatch`. These are not separable stages that can be deployed independently.

### Cost of Splitting

- **Integration overhead**: HIGH. Because R2's tier definitions are consumed by R1, R3, R4, R5, R6, R7, R9, and R10, splitting would require duplicating the entire tier/category schema in both releases while maintaining exact fidelity of every formula, error code, and threshold.
- **Context switching**: HIGH. The error handling flow (R4) crosses ingestion (rejected events), classification (cache invalidation), dispatch (handler timeout → transient_error), DLQ (failure disposition), and ordering (retry blocking). Splitting this flow across releases creates ambiguous intermediate states.
- **Rework risk**: MEDIUM-HIGH. If Release 1 discovers that the tier definitions need adjustment, it invalidates Release 2's retry policies, SLA thresholds, backpressure shedding rules, and DLQ dispositions simultaneously.

### Cost of NOT Splitting

- **Big-bang risk**: MEDIUM. The spec is 1400-1800 LOC, which is substantial but not extraordinary. The incident regression tests (INC-063, INC-071, INC-078) provide concrete validation scenarios.
- **Delayed feedback**: LOW-MEDIUM. The spec already includes staged testing (integration tests, incident regression, chaos tests) that provide feedback within a single release.
- **Root-cause isolation**: MEDIUM. If something fails, the tightly coupled nature means debugging crosses requirement boundaries — but this is equally true whether split or not.

### Foundation vs. Application Boundary?

The closest candidate for a natural seam would be:
- Foundation: R2 (classification) + R1 (ingestion) + R3 (backpressure)
- Application: R4 (error handling) + R5 (handlers) + R6 (DLQ) + R9 (ordering)
- Cross-cutting: R7 (observability), R8 (lifecycle), R10 (config)

However, this fails the independence test:
- R1 (ingestion) needs R3 (backpressure) for its rate limit formula, and R3 needs R2 (classification) for shedding eligibility — all three must be co-present
- R4 (error handling) needs R2's tier definitions to function — it cannot exist without R2
- R5 (handlers) need R2's SLA latencies AND R4's error classification — it needs both foundation and application
- The "foundation" without dispatch/error-handling produces a system that accepts and classifies events but cannot process them, creating a misleading intermediate state

### Could Splitting Increase Risk?

YES. Shipping ingestion + classification + backpressure without dispatch/error-handling/DLQ creates a system that:
1. Accepts events into a queue with no consumers — guaranteed queue fill and backpressure activation
2. Validates events but cannot process them — the validation is untestable in isolation because processing IS the validation
3. Creates a false sense of confidence: "ingestion works" when the real risk is in the retry/dispatch/ordering interactions that caused INC-063, INC-071, and INC-078

## Recommendation: DO NOT SPLIT

**Confidence: 0.92**

The Event Processing Pipeline v2.0 spec should remain intact as a single release. The evidence shows:

1. **No natural seam exists.** R2 (Classification) is referenced by 8 of 9 other requirements. The pipeline's three stages (ingestion -> classification -> dispatch) are not independently deployable or testable.

2. **The cross-requirement references are load-bearing.** R1's rate formula depends on R3's watermarks. R4's retry flow depends on R2's tier budgets. R9's ordering blocks depend on R4's retry windows. These are not cross-references that can be deferred — they are definitional dependencies.

3. **Splitting would create a misleading intermediate state.** An ingestion+classification system without dispatch cannot be meaningfully validated in real-world conditions. Events would queue but never process.

4. **The incidents that motivate the spec (INC-063, INC-071, INC-078) span the entire pipeline.** INC-063 (poison events consuming retry budget) involves ingestion -> classification -> retry -> DLQ. INC-071 (burst overload) involves ingestion -> backpressure -> shedding. INC-078 (stale cache) involves classification -> dispatch -> handler. These cannot be regression-tested without the full pipeline.

5. **The scope (1400-1800 LOC) is manageable as a single release.** This is not a case where sheer size demands splitting.

### Risks of Keeping Intact (and mitigations)

| Risk | Mitigation |
|------|------------|
| Big-bang deployment | Staged rollout: deploy with feature flags, enable stages incrementally |
| Late feedback | Implement integration tests early; the spec's chaos tests provide real validation |
| Debugging difficulty | The observability layer (R7) provides comprehensive metrics; deploy it alongside the pipeline |

### Alternative Strategies for Early Validation Without Splitting

1. **Incremental development, single deployment**: Build R2 (classification) first, then R1 (ingestion) + R3 (backpressure), then R4-R6 (dispatch/error/DLQ), testing each layer as it's added — but deploy as one release.
2. **Shadow mode deployment**: Deploy the full pipeline in shadow mode alongside the existing monolithic processor. Compare outputs without serving live traffic.
3. **Canary with traffic splitting**: Deploy to a canary environment with 1% of traffic, validating the full pipeline end-to-end before ramping.
