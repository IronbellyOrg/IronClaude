# Fix Proposal 3 — Loader options + serializer + per-user cache

## Problem statement

Same N+1 diagnosis as Fix 1 and Fix 2; additionally, the endpoint serializes ORM models inline and has no caching despite being a polled per-user dashboard.

## Proposed change

**Phase 1** (regression hotfix, same PR): apply Fix 1.

**Phase 2** (follow-up PR):

- Add `WidgetSummaryDTO` (marshmallow or pydantic schema) and serialize through it.
- Decorate the endpoint with `@cache.memoize(timeout=60, ...)` keyed on `current_user.id`.
- Add cache-invalidation hooks on widget mutation endpoints.

## Evidence

- Inline `views/dashboard.py` builds JSON shape inline, no schema layer.
- Inline `views/dashboard.py` has no caching decorator.
- Operational assumption: dashboards typically receive polling traffic.

## Risks

- Cache without invalidation hooks → stale data after edits.
- Scope creep — Phase 2 expands a regression fix into an architectural change.
- DTO refactor has its own design surface.

## Test plan

- Phase 1: same as Fix 1.
- Phase 2: cache-hit integration test (second identical request < 10 ms within TTL); cache-bust test after widget mutation.
