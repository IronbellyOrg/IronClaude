# Hypothesis: N+1 is the immediate cause; the deeper issue is endpoint shape — eager load AND add a serializer + short TTL cache

**Agent**: system-architect
**Tier**: 2
**Timestamp**: 2026-05-21T05:32:00Z
**Cause class**: Performance / resource (N+1) — with architectural follow-up

## Claim

Agree with the diagnosis: lazy `owner`, `last_edit→editor`, and `tags` produce ~200 queries per request. The fix must include eager-loading. But the endpoint is also doing model-to-JSON serialization inline inside a view function and has no caching despite being a per-user read-heavy dashboard. The minimum fix is loader-options; the durable fix is a DTO/serializer plus a 30-60s per-user cache so a polled dashboard does not re-issue the query every refresh.

## Evidence

- `views/dashboard.py` inline — list comprehension constructs the dict shape inline; no `Schema`/`Serializer`/`@dataclass` layer.
- `views/dashboard.py` inline — no `@cache`, no `flask_caching` decorator, no `If-Modified-Since` handling.
- `models/widget.py` inline — three lazy relationships, same as other agents.
- Operational shape: per-user dashboard endpoints typically receive polling traffic from open browser tabs — the same payload is regenerated many times per minute per user.

## Proposed Fix

Two-phase:

**Phase 1 (immediate, this PR)**: same loader-options change as performance-engineer (joinedload for singles, selectinload for tags).

**Phase 2 (follow-up PR, recommended in this report)**:

- Introduce a `WidgetSummaryDTO` (or marshmallow/pydantic schema) so the view function builds it from already-loaded data and is not coupled to ORM iteration semantics.
- Add a `flask_caching` decorator on the endpoint with a 30-60s per-user TTL: `@cache.memoize(timeout=60, make_name=lambda f: f'{f}:{current_user.id}')`.

Files to change:

- Phase 1: `views/dashboard.py` only.
- Phase 2: new `views/dto/widget.py`; modify `views/dashboard.py` to use it and add cache decorator.

Test to verify:

- Phase 1 query-count test as in other cards.
- Phase 2: cache-hit integration test; assert second identical request inside 30s returns < 10 ms.

## Confidence

Self-reported confidence: 0.78

Per-dimension self-assessment:

- Evidence grounding: 1.0 for the N+1; 0.5 for the cache claim (relies on operational pattern, not measured traffic).
- Symptom coverage: 1.0 for N+1; cache is preventive, not diagnostic.
- Reproducibility fit: 0.5
- Fix directness: 0.5 — Phase 2 is broader than a regression fix should be.
- Domain coherence: 0.5 — mixes ORM and caching domains.

Mean = 0.70

## Risks

- **Cache invalidation**: adding cache without invalidation hooks means stale widget data after edits; needs explicit invalidation on widget mutations.
- **Scope creep**: Phase 2 is real work that competes with shipping the regression fix today.
- **DTO refactor risk**: introducing a serializer layer touches more than one endpoint over time — needs its own design review.

## If I'm wrong, it's probably because

The operational team prefers the smallest fix that resolves the SLO breach (Phase 1 only), and Phase 2 belongs in a roadmap ticket, not in this troubleshoot report.

## Alternatives considered

- **Phase 1 only** (the other agents' position) — minimum safe fix; what most teams will ship.
- **HTTP-level cache (CDN/edge)** — not appropriate for per-user authenticated data.

## Grounding gaps

- No traffic/polling data; the caching value is inferred from endpoint shape.
- No information on whether widgets mutate frequently — affects whether 60s cache TTL is sensible.
- Inline snippets only.
