---
release: event-processing-pipeline-v2.0
version: 2.0.0
status: draft
date: 2026-03-18
priority: P0
estimated_scope: 1400-1800 lines production code
predecessor_releases:
  - message-bus-v1.2
  - dead-letter-queue-v1.0
processing_model: "3-tier: ingestion -> classification -> dispatch"
routing_strategy: "content-based with fallback chain"
---

# Event Processing Pipeline v2.0 — Release Specification

## 1. Problem Statement

The current event processing system handles events through a monolithic `process_event()` function with no formal classification, no structured error recovery, and no backpressure mechanism. Three production incidents exposed fundamental gaps:

| Incident | Date | Root Cause | Impact |
|----------|------|-----------|--------|
| INC-063 | 2026-02-20 | Malformed events entered processing without validation — no schema check at ingestion boundary | 14,000 poison events consumed 23 hours of retry budget before manual intervention |
| INC-071 | 2026-03-01 | Burst of 50K events/sec exceeded consumer capacity — no backpressure, no shedding | Memory exhaustion, OOM kill, 47-minute outage |
| INC-078 | 2026-03-12 | Event routed to wrong handler due to stale classification cache — cache TTL was infinite | 2,300 payment events processed as notifications, funds not settled for 6 hours |

### 1.1 Current Architecture Deficiencies

The monolithic processor conflates three concerns that MUST be separated:

1. **Ingestion**: Accepting events from external sources. Currently has no schema validation, no rate limiting, no backpressure signaling.
2. **Classification**: Determining event type and routing destination. Currently a single `if/elif` chain with 34 branches and no fallback for unrecognized event types.
3. **Dispatch**: Delivering classified events to handlers. Currently synchronous, blocking, with no timeout and no retry differentiation between transient and permanent failures.

## 2. Requirements

### R1: Ingestion Layer (P0)

All events enter the pipeline through a single ingestion endpoint that performs validation, rate limiting, and backpressure management.

**Schema validation contract**:
- Every event MUST be validated against the registered schema for its `event_type` field before entering the processing queue
- Events with no `event_type` field are rejected with error code `EVT-001: Missing required field 'event_type'`
- Events with an unrecognized `event_type` are rejected with error code `EVT-002: Unrecognized event_type '{type}'. Registered types: {comma_separated_list}`
- Events that fail schema validation are rejected with error code `EVT-003: Schema validation failed for event_type '{type}': {validation_errors}`
- Rejected events are written to the `rejected_events` topic with the original payload plus rejection metadata. They are NOT written to the dead-letter queue — the DLQ is reserved for events that PASSED validation but FAILED during processing (see R4).

**Rate limiting** (defined in terms of the backpressure thresholds from R3):
- Ingestion rate limit is dynamically calculated as: `base_rate_limit * (1 - current_queue_depth / backpressure_high_watermark)` where `base_rate_limit = 10,000 events/sec` and `backpressure_high_watermark` is the value defined in R3 Section "Backpressure thresholds"
- When `current_queue_depth >= backpressure_high_watermark`, the effective rate limit drops to 0 (full backpressure — ingestion stops accepting events)
- When `current_queue_depth <= backpressure_low_watermark` (also defined in R3), the rate limit returns to `base_rate_limit`
- Rate-limited events receive HTTP 429 with `Retry-After` header set to `ceil(current_queue_depth / drain_rate_per_sec)` seconds, where `drain_rate_per_sec` is the measured average consumption rate over the last 60-second window

**Ingestion queue**:
- Maximum queue depth: 100,000 events
- Queue implementation: bounded ring buffer with FIFO ordering
- When queue is full AND backpressure is active, new events are rejected with HTTP 503 (Service Unavailable) — they are NOT silently dropped, NOT written to overflow storage, NOT queued in memory beyond the 100,000 limit
- Queue persistence: events in the queue are durable (written to WAL before acknowledgment). Queue survives process restart without event loss.

### R2: Classification Engine (P0)

Events are classified into one of four severity tiers and one of six routing categories. Classification determines ALL downstream behavior — retry policy, timeout, handler selection, and SLA.

**Severity tiers** (defined here, referenced by R4 and R5):

| Tier | Name | Examples | Max Processing Latency | Retry Budget |
|------|------|----------|----------------------|--------------|
| T1 | Critical | `payment.completed`, `account.locked`, `fraud.detected` | 500ms | 5 retries, 60s total |
| T2 | Standard | `order.created`, `inventory.updated`, `user.registered` | 2,000ms | 3 retries, 30s total |
| T3 | Bulk | `analytics.pageview`, `metrics.collected`, `log.ingested` | 10,000ms | 1 retry, 10s total |
| T4 | Best-effort | `notification.preference`, `ui.theme_changed`, `cache.warmed` | 30,000ms | 0 retries |

**Routing categories**:

| Category | Handler Pool | Concurrency | Queue Priority |
|----------|-------------|-------------|----------------|
| `financial` | `financial_handler_pool` | 5 workers | Highest — always dequeued before other categories |
| `security` | `security_handler_pool` | 3 workers | Highest — same priority as financial, ties broken by arrival order |
| `lifecycle` | `lifecycle_handler_pool` | 8 workers | Standard |
| `telemetry` | `telemetry_handler_pool` | 15 workers | Lowest |
| `configuration` | `configuration_handler_pool` | 2 workers | Standard |
| `unclassified` | `default_handler_pool` | 3 workers | Lowest — same priority as telemetry, ties broken by arrival order |

**Classification rules** (order matters — first match wins):

1. If `event_type` starts with `payment.` or `billing.` or `settlement.` → category `financial`, tier T1
2. If `event_type` starts with `fraud.` or `account.locked` or `auth.breach` → category `security`, tier T1
3. If `event_type` starts with `order.` or `inventory.` or `shipping.` → category `lifecycle`, tier T2
4. If `event_type` starts with `user.` or `account.` (EXCLUDING `account.locked`) → category `lifecycle`, tier T2
5. If `event_type` starts with `analytics.` or `metrics.` or `log.` → category `telemetry`, tier T3
6. If `event_type` starts with `notification.` or `ui.` or `cache.` → category `configuration`, tier T4
7. If `event_type` starts with `config.` or `feature.` or `setting.` → category `configuration`, tier T2
8. Default (no match): category `unclassified`, tier T3

**Critical classification constraint**: Rule 4 contains an EXCLUSION — `account.locked` is matched by Rule 2 (security/T1), NOT Rule 4 (lifecycle/T2). The `account.*` pattern in Rule 4 applies to all `account.` events EXCEPT those already matched by a preceding rule. Since rules are evaluated first-match-wins, `account.locked` will never reach Rule 4. This exclusion MUST be preserved in any split or reorganization of these rules.

**Classification cache**:
- Cache TTL: 300 seconds (5 minutes). NOT infinite (INC-078 root cause)
- Cache key: `event_type` string (exact match, not prefix)
- Cache invalidation: On rule change, ALL cached entries MUST be invalidated immediately (not on next TTL expiry)
- Cache size: maximum 10,000 entries, LRU eviction

### R3: Backpressure and Flow Control (P0)

The pipeline implements multi-level backpressure to prevent resource exhaustion.

**Backpressure thresholds** (referenced by R1 rate limiting formula):
- `backpressure_low_watermark`: 20,000 events (below this, no backpressure active)
- `backpressure_high_watermark`: 80,000 events (at or above this, full backpressure — ingestion stops)
- `backpressure_critical_watermark`: 95,000 events (at or above this, load shedding activates)

**Backpressure levels**:

| Level | Queue Depth Range | Behavior |
|-------|------------------|----------|
| `green` | 0 — 19,999 | Normal operation. No throttling. |
| `yellow` | 20,000 — 79,999 | Proportional throttling. Ingestion rate reduced linearly per R1 formula. T4 events may be shed (see load shedding). |
| `red` | 80,000 — 94,999 | Full backpressure. Ingestion paused. T3 and T4 events shed. T1 and T2 continue processing from queue. |
| `critical` | 95,000+ | Emergency shedding. Only T1 events accepted. T2, T3, T4 shed. Queue draining prioritized. |

**Load shedding rules** (these rules define which events are dropped during backpressure — the tier definitions from R2 determine eligibility):
- `yellow` level: T4 (best-effort) events are shed. Shed events receive HTTP 503 with `X-Event-Shed: true` header and `shed_reason: backpressure_yellow`.
- `red` level: T3 and T4 events are shed. T3 shed events are written to the `shed_events` overflow topic for later replay.
- `critical` level: T2, T3, and T4 events are shed. T2 shed events are written to BOTH the `shed_events` topic AND the `deferred_processing` queue for automatic replay when backpressure returns to `green`.
- T1 events are NEVER shed under ANY backpressure level. If the queue is full and a T1 event arrives, the oldest T4 event in the queue is evicted to make room. If no T4 events exist, the oldest T3 event is evicted. If no T3 events exist, the T1 event is rejected with HTTP 503 — it is NOT allowed to evict T2 events.

**Critical constraint on T1 eviction behavior**: The eviction cascade for T1 events is strictly T4 → T3 → reject. It MUST NOT extend to T2. A T1 event that cannot find a T4 or T3 event to evict MUST be rejected rather than evicting a T2 event. This prevents a burst of T1 events from starving T2 processing entirely.

### R4: Error Handling and Recovery (P0)

Error handling behavior is defined per-tier. Each tier has distinct retry, timeout, and failure disposition semantics. The tier definitions in R2 set the retry budget; this section defines the retry BEHAVIOR.

**Retry policies by tier** (parameters from R2 tier table):

**T1 (Critical) retry flow**:
1. First failure: retry immediately (no delay)
2. Second failure: retry after 1,000ms
3. Third failure: retry after 2,000ms
4. Fourth failure: retry after 4,000ms
5. Fifth failure: retry after 8,000ms
6. Sixth attempt fails: route to `critical_failure_handler` which pages on-call AND writes to DLQ AND emits `critical_event_failed` alert
- Total retry window: 60 seconds. If retries are still pending when the 60-second window expires, remaining retries are ABANDONED and the event proceeds directly to `critical_failure_handler`.
- T1 retry delay formula: `delay_ms = 2^(attempt-2) * 1000` for attempt >= 2, with `delay_ms = 0` for attempt 1

**T2 (Standard) retry flow**:
1. First failure: retry after 2,000ms
2. Second failure: retry after 5,000ms
3. Third failure: retry after 10,000ms
4. Fourth attempt fails: write to DLQ with `disposition: requires_manual_review`
- Total retry window: 30 seconds
- T2 events in the DLQ MUST include the original event payload, all attempt timestamps, and the failure reason for each attempt

**T3 (Bulk) retry flow**:
1. First failure: retry after 5,000ms
2. Second attempt fails: write to DLQ with `disposition: auto_retry_eligible`
- Total retry window: 10 seconds
- T3 events in the DLQ are eligible for automatic batch retry every 15 minutes

**T4 (Best-effort) retry flow**:
- No retries. Single attempt only.
- On failure: discard event. Emit `best_effort_event_dropped` metric. Do NOT write to DLQ.
- T4 events MUST NOT appear in the DLQ under any circumstances. If a T4 event is found in the DLQ, it indicates a classification or routing bug.

**Error classification** (determines retry eligibility):
- `transient_error`: Network timeout, connection reset, HTTP 5xx from downstream. RETRYABLE per tier policy.
- `permanent_error`: Schema mismatch in handler, business rule violation, HTTP 4xx from downstream. NOT retryable — immediately route to failure disposition (DLQ for T1-T3, discard for T4).
- `poison_event`: Event causes handler crash (unhandled exception). NOT retryable — immediately quarantine in `poison_events` topic with handler crash dump. This is DISTINCT from DLQ — poison events go to their own topic, not the general DLQ.

**Critical error classification constraint**: The retry flow MUST check error classification BEFORE attempting retry. A `permanent_error` on the first attempt MUST skip all retries and proceed directly to failure disposition. The retry budget is ONLY consumed by `transient_error` failures. This prevents the pathological case from INC-063 where poison events consumed the full retry budget before being quarantined.

### R5: Handler Contract (P1)

Handlers implement a uniform interface with tier-aware SLA enforcement.

**Handler interface**:
```python
class EventHandler(Protocol):
    async def handle(self, event: ClassifiedEvent) -> HandlerResult:
        """Process a classified event. MUST complete within the tier's max_processing_latency."""

    async def health_check(self) -> HealthStatus:
        """Return handler pool health. Called every 30 seconds."""

    def supported_event_types(self) -> frozenset[str]:
        """Return the set of event_types this handler can process. Immutable after registration."""
```

**SLA enforcement** (latency thresholds from R2 tier table):
- Handler execution is wrapped in a timeout equal to the tier's `max_processing_latency`
- Timeout is measured from handler invocation start, NOT from event arrival time
- On timeout: the handler invocation is cancelled, the event is treated as a `transient_error` (eligible for retry per R4 policy), and `handler_timeout` metric is incremented
- If a handler exceeds its SLA on more than 20% of events in a 5-minute window, the handler pool is marked `degraded` and the `handler_pool_degraded` alert fires
- A degraded handler pool continues processing but its events are routed through a `shadow_handler` in parallel for comparison (similar to the canary pattern)

**Handler registration invariant**: A handler's `supported_event_types()` return value MUST be frozen at registration time. If a handler attempts to modify its supported types after registration, the modification MUST be rejected with `HandlerRegistrationError: Event type set is immutable after registration`. This prevents the stale-routing class of bugs (INC-078).

**Cross-handler routing prohibition**: An event MUST be processed by EXACTLY ONE handler. If classification maps an event to a handler that does not list the event's type in `supported_event_types()`, the event is routed to `default_handler_pool` — it is NOT retried with a different handler, NOT bounced between handlers, and NOT silently dropped.

### R6: Dead-Letter Queue Management (P1)

The DLQ has structured disposition rules that differ by tier. These rules reference the tier definitions from R2 and the failure dispositions from R4.

**DLQ entry schema**:
```python
@dataclass
class DLQEntry:
    event_id: str
    event_type: str
    original_payload: bytes
    tier: Literal["T1", "T2", "T3"]  # T4 NEVER appears in DLQ
    category: str
    disposition: Literal[
        "requires_immediate_attention",   # T1 only
        "requires_manual_review",          # T2 only
        "auto_retry_eligible",             # T3 only
    ]
    failure_history: list[FailureRecord]  # one per attempt
    first_failure_utc: datetime
    last_failure_utc: datetime
    retry_count: int
    handler_id: str
    ingestion_timestamp_utc: datetime     # when event first entered pipeline
    classification_timestamp_utc: datetime # when event was classified
    dlq_entry_timestamp_utc: datetime     # when event entered DLQ
```

**DLQ disposition rules** (tier-specific, referencing R4 failure dispositions):
- T1 (`requires_immediate_attention`): Pages on-call via PagerDuty integration. Auto-retry after 5 minutes. If auto-retry fails, escalate to `critical_dlq_review` channel. Maximum 3 auto-retries from DLQ before requiring manual intervention.
- T2 (`requires_manual_review`): No auto-retry. Events appear in review dashboard. Retention: 30 days, then archived.
- T3 (`auto_retry_eligible`): Batch auto-retry every 15 minutes. Maximum 10 auto-retries from DLQ. After 10 failures, disposition changes to `requires_manual_review` (promoted from T3 handling to T2 handling).

**DLQ capacity**: Maximum 50,000 entries. When DLQ reaches 90% capacity (45,000 entries), emit `dlq_capacity_warning` alert. When DLQ reaches 100% capacity, the oldest `auto_retry_eligible` (T3) entries are evicted to make room. T1 and T2 entries are NEVER evicted — if no T3 entries exist and the DLQ is full, new DLQ entries are written to an overflow file with `dlq_overflow` alert.

**DLQ-to-rejected-events boundary**: Events that fail validation at ingestion (R1) go to `rejected_events`. Events that pass validation but fail during processing go to DLQ (T1-T3) or are discarded (T4). Events that crash the handler go to `poison_events`. These three destinations are MUTUALLY EXCLUSIVE — an event MUST end up in exactly one of: successfully processed, rejected_events, DLQ, poison_events, or discarded(T4 only).

### R7: Observability and Metrics (P1)

The pipeline emits structured metrics and maintains operational dashboards. Metric definitions reference thresholds and categories defined in R1-R6.

**Core metrics**:

| Metric | Type | Labels | Source Requirement |
|--------|------|--------|--------------------|
| `ep.ingestion.rate` | Gauge | — | R1 |
| `ep.ingestion.rejected` | Counter | `error_code` | R1: EVT-001, EVT-002, EVT-003 |
| `ep.classification.duration_ms` | Histogram | `tier`, `category` | R2 |
| `ep.classification.cache_hit_rate` | Gauge | — | R2 cache |
| `ep.backpressure.level` | Gauge | — | R3: green/yellow/red/critical |
| `ep.backpressure.events_shed` | Counter | `tier`, `level` | R3 shedding rules |
| `ep.handler.latency_ms` | Histogram | `handler_pool`, `tier` | R5 SLA |
| `ep.handler.timeout` | Counter | `handler_pool`, `tier` | R5 SLA enforcement |
| `ep.handler.degraded` | Gauge | `handler_pool` | R5 degradation |
| `ep.dlq.depth` | Gauge | `tier`, `disposition` | R6 |
| `ep.dlq.auto_retry.success` | Counter | `tier` | R6 auto-retry |
| `ep.dlq.evictions` | Counter | `tier` | R6 capacity |
| `ep.error.classification` | Counter | `error_type` | R4: transient/permanent/poison |
| `ep.retry.attempts` | Counter | `tier`, `attempt_number` | R4 retry flows |
| `ep.retry.budget_exhausted` | Counter | `tier` | R4 retry window |
| `ep.event.e2e_latency_ms` | Histogram | `tier`, `category` | All — ingestion to completion |
| `ep.poison.quarantined` | Counter | `handler_pool` | R4 poison events |

**Alerting thresholds** (derived from R2 SLA and R3 backpressure):
- `ep.handler.latency_ms` p99 exceeds 2x tier max_processing_latency for 5 consecutive minutes → `handler_sla_breach` alert
- `ep.backpressure.level` stays at `red` or `critical` for more than 10 minutes → `sustained_backpressure` alert
- `ep.dlq.depth` for any tier exceeds 1,000 entries → `dlq_depth_warning` alert
- `ep.poison.quarantined` increases by more than 10 in a 5-minute window → `poison_event_surge` alert
- `ep.ingestion.rejected` with error_code `EVT-001` increases by more than 100 in a 1-minute window → `malformed_event_surge` alert (potential upstream schema change)

### R8: Pipeline Lifecycle and Graceful Shutdown (P1)

The pipeline has a defined startup and shutdown sequence that preserves event processing guarantees.

**Startup sequence** (steps MUST execute in this exact order):
1. Load event type schemas from schema registry
2. Initialize classification engine and warm classification cache with top-100 event types
3. Initialize handler pools and run health checks — ALL handler pools MUST pass health check before accepting traffic
4. Initialize DLQ consumer (for auto-retry processing)
5. Set backpressure level to `green`
6. Open ingestion endpoint

**Critical startup constraint**: Step 6 (open ingestion) MUST NOT execute before step 3 (handler health check) completes. Accepting events before handlers are healthy caused a variant of INC-063 where events queued during startup exhausted the queue before handlers were ready.

**Shutdown sequence** (steps MUST execute in this exact order):
1. Close ingestion endpoint (stop accepting new events)
2. Wait for in-flight events to complete, up to `shutdown_grace_period = 30 seconds`
3. After grace period: events still in `processing` state are returned to the queue head (not tail) for reprocessing after restart
4. Flush all metrics and audit records
5. Close handler pools (handlers receive `shutdown_signal` and have 10 seconds to clean up)
6. Persist queue state to WAL
7. Close DLQ consumer

**Shutdown ordering constraint**: Step 3 specifies events returned to queue HEAD (not tail). This ensures partially-processed events are retried BEFORE new events after restart, preventing starvation. The head-insertion MUST be atomic with the queue state persistence in step 6 — if the process crashes between steps 3 and 6, the WAL from the last successful checkpoint is used, and in-flight events are recovered from the handler's idempotency log.

**Drain timeout escalation**: If the queue has not drained to 0 within `drain_timeout = 300 seconds` (5 minutes) after ingestion closes, the pipeline logs a `drain_timeout_exceeded` warning and proceeds to step 3 regardless. Events remaining in the queue are persisted via WAL and processed after restart. The drain timeout is SEPARATE from the shutdown grace period — the grace period applies to in-flight events (step 2), the drain timeout applies to queued-but-not-started events.

### R9: Event Ordering Guarantees (P2)

The pipeline provides ordering guarantees that vary by category.

**Per-category ordering**:
- `financial`: Strict FIFO ordering within the same `entity_id` (e.g., all events for payment P-123 are processed in arrival order). Cross-entity ordering is NOT guaranteed.
- `security`: Strict FIFO ordering within the same `entity_id`. Security events for the same account MUST be processed sequentially — no concurrent processing of same-entity security events.
- `lifecycle`: FIFO ordering within the same `entity_id`, best-effort. Reordering is permitted during retry (a retried event may be processed after a later event for the same entity).
- `telemetry`: No ordering guarantee. Events may be processed in any order.
- `configuration`: Strict FIFO ordering within the same `entity_id`. Configuration changes MUST be applied in order — a stale config event processed after a newer one would corrupt state.
- `unclassified`: No ordering guarantee.

**Ordering enforcement mechanism**: For categories with strict FIFO (financial, security, configuration), the dispatcher maintains a per-entity lock. Events for the same entity_id in these categories are serialized through this lock. The lock is acquired before dispatch and released after handler completion (including retries). This means retry delays block subsequent events for the same entity — this is intentional and required for correctness.

**Critical ordering interaction with R4 retry**: When a financial/security/configuration event is retrying, ALL subsequent events for the same `entity_id` are BLOCKED waiting for the retry to complete or exhaust its budget. This blocking is bounded by the tier's total retry window (R4: 60s for T1, 30s for T2). After the retry window expires, the failed event is sent to DLQ and the entity lock is released, allowing queued events to proceed. Events that were blocked do NOT consume their own retry budget during the wait — the retry budget timer starts only when the event is dispatched to a handler.

### R10: Configuration and Tuning (P2)

All quantitative parameters in R1-R9 are configurable at runtime without pipeline restart.

**Configuration hierarchy** (highest precedence first):
1. Runtime override via admin API (ephemeral — lost on restart)
2. Environment variables (`EP_*` prefix)
3. Configuration file (`event_pipeline.yaml`)
4. Hardcoded defaults (values stated in this spec)

**Immutable configuration** (CANNOT be changed at runtime — requires restart):
- Queue implementation type (ring buffer)
- Handler pool worker counts (R2 concurrency table)
- WAL storage location
- Schema registry endpoint

**Mutable configuration** (CAN be changed at runtime):
- All backpressure thresholds (R3)
- All retry delays and budgets (R4)
- Classification cache TTL (R2)
- Alerting thresholds (R7)
- Shutdown grace period and drain timeout (R8)

**Configuration change audit**: Every runtime configuration change MUST be logged with: `parameter_name`, `old_value`, `new_value`, `changed_by`, `timestamp_utc`, `change_reason` (minimum 10 characters). Changes without a reason are rejected with `ConfigChangeError: Reason must be at least 10 characters (got {len})`.

## 3. Interface Contracts

### 3.1 Ingestion API

```python
class IngestionEndpoint:
    async def accept_event(self, raw_event: bytes) -> IngestionResult:
        """Validate schema, check rate limits, enqueue if valid.
        Returns IngestionResult with status and event_id."""

    def current_backpressure_level(self) -> Literal["green", "yellow", "red", "critical"]:
        """Return current backpressure level for health checks."""
```

**IngestionResult**:
```python
@dataclass
class IngestionResult:
    accepted: bool
    event_id: str | None          # None if rejected
    rejection_code: str | None     # EVT-001, EVT-002, EVT-003, or None
    rejection_detail: str | None
    queue_depth_at_acceptance: int
    backpressure_level: str
```

### 3.2 Classification API

```python
class ClassificationEngine:
    def classify(self, event: ValidatedEvent) -> ClassificationResult:
        """Apply classification rules (R2) and return tier + category.
        Uses cache when available. MUST be deterministic for the same event_type."""

    def invalidate_cache(self) -> int:
        """Invalidate all cached classifications. Returns count of evicted entries."""
```

### 3.3 Dispatch API

```python
class EventDispatcher:
    async def dispatch(self, event: ClassifiedEvent) -> DispatchResult:
        """Route event to appropriate handler pool with tier-aware timeout.
        Implements retry logic per R4. Returns final disposition."""

    async def drain(self, timeout_seconds: int = 300) -> DrainResult:
        """Wait for in-flight events to complete. Used during shutdown."""
```

## 4. Cross-Requirement Dependency Map

This section documents the explicit dependencies between requirements. When splitting this spec, ALL requirements connected by a dependency edge MUST either land in the same release OR the dependency must be explicitly re-documented in both releases.

```
R1 (Ingestion) ──references──> R3 (Backpressure thresholds for rate limit formula)
R2 (Classification) ──defines──> Tier parameters used by R4, R5, R6, R7
R3 (Backpressure) ──references──> R2 (Tier definitions for shedding eligibility)
R4 (Error Handling) ──references──> R2 (Tier retry budgets) AND R6 (DLQ dispositions)
R5 (Handlers) ──references──> R2 (Tier SLA latencies) AND R4 (Error classification)
R6 (DLQ) ──references──> R2 (Tier for disposition rules) AND R4 (Failure flow destinations)
R7 (Observability) ──references──> ALL other requirements for metric definitions
R8 (Lifecycle) ──references──> R1 (Ingestion), R3 (Backpressure), R6 (DLQ)
R9 (Ordering) ──references──> R2 (Category definitions) AND R4 (Retry blocking behavior)
R10 (Config) ──references──> ALL quantitative parameters from R1-R9
```

**Strongest coupling**: R2 (Classification) is referenced by every other requirement. It CANNOT be split from any requirement that uses tier definitions or category definitions without losing semantic meaning.

## 5. Testing Strategy

### 5.1 Integration Tests

- **Ingestion → Classification → Dispatch**: End-to-end flow for each of the 6 categories
- **Backpressure cascade**: Simulate queue fill from green → yellow → red → critical and verify shedding behavior at each level
- **Error classification → retry → DLQ**: For each tier, verify the complete failure path including retry delays, budget enforcement, and DLQ entry
- **Ordering guarantee**: Concurrent events for the same entity_id in financial category must be serialized

### 5.2 Incident Regression Tests

- **INC-063**: Submit a poison event → verify it is quarantined after first crash, NOT retried
- **INC-071**: Submit 50K events/sec burst → verify backpressure activates, shedding engages, no OOM
- **INC-078**: Modify classification rules → verify cache is invalidated immediately, not on TTL expiry

### 5.3 Chaos Tests

- Kill handler pool during processing → verify in-flight events return to queue head
- Fill DLQ to 90% → verify capacity warning alert fires
- Simulate sustained red backpressure for 10 minutes → verify alert fires

## 6. Non-Functional Requirements

- Ingestion throughput: sustained 10,000 events/sec at green backpressure level
- Classification latency: p99 < 5ms (cached), p99 < 20ms (uncached)
- End-to-end latency (ingestion to handler completion): p99 < tier max_processing_latency * 1.5
- DLQ write latency: p99 < 10ms
- Backpressure level transition latency: < 100ms from threshold crossing to behavior change
- Queue persistence (WAL) write latency: p99 < 2ms per event
- Graceful shutdown completes within `shutdown_grace_period + drain_timeout + 10` seconds maximum (30 + 300 + 10 = 340 seconds)
- Memory footprint: < 500MB for 100,000 queued events with average payload size 2KB

## 7. File Manifest

| File | Action | LOC | Purpose |
|------|--------|-----|---------|
| `src/superclaude/events/ingestion.py` | CREATE | 250-300 | Ingestion endpoint, schema validation, rate limiting |
| `src/superclaude/events/classification.py` | CREATE | 180-220 | Classification engine, tier/category rules, cache |
| `src/superclaude/events/backpressure.py` | CREATE | 150-180 | Backpressure controller, watermarks, shedding |
| `src/superclaude/events/dispatcher.py` | CREATE | 300-350 | Event dispatch, retry logic, timeout enforcement |
| `src/superclaude/events/handlers.py` | CREATE | 120-150 | Handler protocol, registration, health checks |
| `src/superclaude/events/dlq.py` | CREATE | 200-240 | DLQ management, disposition rules, auto-retry |
| `src/superclaude/events/ordering.py` | CREATE | 100-120 | Per-entity ordering locks, FIFO enforcement |
| `src/superclaude/events/lifecycle.py` | CREATE | 80-100 | Startup/shutdown sequences, WAL integration |
| `src/superclaude/events/metrics.py` | CREATE | 60-80 | Metric definitions and emission |
| `src/superclaude/events/config.py` | CREATE | 80-100 | Configuration hierarchy, runtime overrides |
| `tests/events/test_ingestion.py` | CREATE | 150-200 | Schema validation, rate limiting, rejection codes |
| `tests/events/test_classification.py` | CREATE | 120-150 | Rule matching, cache behavior, exclusion patterns |
| `tests/events/test_backpressure.py` | CREATE | 150-180 | Watermark transitions, shedding by tier |
| `tests/events/test_error_handling.py` | CREATE | 200-250 | Per-tier retry flows, error classification |
| `tests/events/test_dlq.py` | CREATE | 120-150 | Disposition rules, capacity management, eviction |
| `tests/events/test_ordering.py` | CREATE | 100-120 | FIFO enforcement, retry blocking |
| `tests/events/test_incidents.py` | CREATE | 80-100 | INC-063, INC-071, INC-078 regression |
