# Hypothesis: N+1 across owner (M:1) + last_edit→editor (1:1) + tags (M:M); fix with per-relationship loader strategy

**Agent**: performance-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:31:50Z
**Cause class**: Performance / resource (N+1 query)

## Claim

The endpoint executes 1 + 3N round-trips (1 widgets query, then per-widget: owner, last_edit-then-editor, tags). For N=50 typical, that is ~200 queries per request. Eager-loading via `options(...)` on the driving query collapses this to a small constant. The loader strategy should be chosen per-cardinality: `joinedload` for the two single-row relationships (`owner`, `last_edit` → `editor`), `selectinload` for the collection (`tags`) to avoid Cartesian row explosion.

## Evidence

- `views/dashboard.py` inline — `widgets = Widget.query.filter_by(user_id=current_user.id).all()` followed by a comprehension accessing `w.owner.full_name`, `w.last_edit.editor.full_name`, `[t.name for t in w.tags]`. Three lazy attribute accesses per row.
- `models/widget.py` inline — `owner`, `tags`, and `last_edit` all default to `lazy='select'`. `last_edit` is a chained access (`w.last_edit.editor`) which is two lazy loads, not one.
- DB read-replica CPU at 80% with normal memory is the textbook N+1 footprint (query-count-bound, not result-size-bound).
- Symptom appeared after a merge that introduced the relationship accesses — pre-refactor either did not touch those attributes or used a different access pattern.

## Proposed Fix

Replace the driving query with:

```python
from sqlalchemy.orm import joinedload, selectinload

widgets = (
    Widget.query
    .options(
        joinedload(Widget.owner),
        joinedload(Widget.last_edit).joinedload(WidgetEdit.editor),
        selectinload(Widget.tags),
    )
    .filter_by(user_id=current_user.id)
    .all()
)
```

Files to change:

- `views/dashboard.py` — query change as above; add the import.

Test to verify:

- New query-count test using `sqlalchemy.event.listen('before_cursor_execute', ...)` — assert ≤ 3 queries (1 widgets+joins, 1 selectin for tags; sometimes 1 extra for the join-fan if the planner splits).
- Latency assertion at the integration layer: p99 < 200 ms with 50 widgets seeded.

## Confidence

Self-reported confidence: 0.92

Per-dimension self-assessment:

- Evidence grounding: 1.0 — every cited code path is in the user-supplied snippets.
- Symptom coverage: 1.0 — 1 + 3N model directly predicts the 15x latency jump (200 queries × ~9 ms = 1.8 s vs ~120 ms single round-trip).
- Reproducibility fit: 0.5 — model is deterministic; no benchmark run.
- Fix directness: 1.0 — change is per-query, six new lines, no schema or default change.
- Domain coherence: 1.0 — single domain (SQLAlchemy ORM loader strategy).

Mean = 0.90

## Risks

- **`joinedload` on `last_edit → editor` doubles the join width**: small risk on row-byte size; acceptable because each widget has at most one last_edit (`uselist=False`).
- **`selectinload(Widget.tags)` issues a second query** that uses `IN (...)` against the collected widget ids; large widget counts can hit the IN-clause planner cliff. At N=50 this is safe; at N=10000 you would need batching.
- **Plan change on the read replica**: the joined query may pick a different index. Validate with `EXPLAIN ANALYZE`.
- **No existing test covers query count** — a future refactor could silently regress; the new query-count test mitigates this.

## If I'm wrong, it's probably because

There is a missing index on a join column (`widget_edits.widget_id` or `widget_tags.widget_id`) introduced or removed in the same refactor, and the queries are slow per-call, not just numerous.

## Alternatives considered

- **Uniform `selectinload` for all three** (root-cause-analyst's likely pick) — simpler, harder to row-explode, but does extra round-trips for the single-row relationships where `joinedload` would be cheaper.
- **Switch defaults to `lazy='joined'` on the model** — too coarse; affects every consumer of `Widget`.
- **Add a cache** — addresses symptom not cause; separate decision.

## Grounding gaps

- Source files are inline; no on-disk MCP queries possible.
- SQLAlchemy version not stated — fix syntax assumes 1.4+. On 1.3, swap `selectinload`/`joinedload` to the older `subqueryload`/`joinedload` idiom.
- No `EXPLAIN ANALYZE` against the read replica.
