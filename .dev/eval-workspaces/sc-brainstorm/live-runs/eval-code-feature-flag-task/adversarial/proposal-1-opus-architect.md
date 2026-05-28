# Proposal 1 — opus / architect

## Stance

Build an OpenFeature-spec-compatible feature flag system with a layered
architecture: SDK -> Provider Interface -> Bespoke Provider -> Control
Plane. Prioritize the SDK boundary as the stable contract so the
provider can be swapped later without touching call sites.

## Core Design

- **SDK layer** (`feature_flags/sdk/`): Implements OpenFeature Python SDK
  surface — `Client.get_boolean_value`, `get_string_value`,
  `get_object_value` — with hooks for logging, metrics, and audit
  emission.
- **Provider interface** (`feature_flags/provider/`): Abstract base class
  with `resolve_boolean`, `resolve_string`, `resolve_object`. In-house
  provider implements via local cache lookup.
- **Local cache** (`feature_flags/cache/`): In-process LRU/dict keyed by
  flag name, populated by a background poller pulling from control
  plane every 10 seconds. Sub-millisecond evaluation via dict access.
- **Control plane** (`feature_flags/control_plane/`): FastAPI service
  exposing CRUD on flags, with Postgres backing store. Emits audit
  events to a dedicated audit log table on every mutation.
- **Bucketing** (`feature_flags/bucketing/`): MurmurHash3 of
  `<flag-key>:<targeting-key>` mod 10000 for percentage rollouts.
  Deterministic and sticky.

## Configuration

- Flag definitions in Postgres `flags` table (key, type, default, rules).
- Rules support: percentage rollouts, allowlist/blocklist on context
  attributes, kill switch (force-off override).
- Local cache TTL configurable (default 10s); stale-cache fallback when
  control plane unreachable, with a `cache_age_seconds` metric.

## Failure Modes

- Cache unreachable on cold start → fail-closed (return default value
  from flag definition shipped in code) and emit alert.
- Control plane unreachable → continue serving from stale cache;
  alert when stale > 5 minutes.
- Bad flag definition (missing type) → reject at control plane on
  write; never reaches cache.

## Tradeoffs

- Pro: Standard architecture, OpenFeature compat means future
  vendor-swap is cheap.
- Pro: Local cache + background poll = sub-ms eval, network-decoupled
  hot path.
- Con: Requires a Postgres dependency + a long-running control plane
  service. Operational footprint is non-trivial for v1.
- Con: 10s propagation floor for non-kill-switch changes. Kill
  switches need a separate push-based path (SSE or webhook) to hit
  the 30s budget reliably.

## Acceptance Criteria

- SDK passes OpenFeature spec conformance tests (subset for booleans
  + strings; objects deferred).
- Cache evaluation p99 < 1ms measured via benchmark suite.
- Control plane CRUD covered by integration tests against a
  containerized Postgres.
- Audit events visible in a dedicated log/table within 5s of mutation.
- Kill-switch path documented and tested separately (push-based, not
  poll-based).
