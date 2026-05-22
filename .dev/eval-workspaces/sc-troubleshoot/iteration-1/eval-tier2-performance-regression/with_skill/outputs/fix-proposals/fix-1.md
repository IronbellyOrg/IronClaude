# Fix Proposal 1 — Per-cardinality loader strategy

## Problem statement

`/api/dashboard/summary` p99 regressed from 120 ms → 1.8 s after the widget refactor. Three lazy SQLAlchemy relationships (`Widget.owner`, `Widget.last_edit → editor`, `Widget.tags`) are accessed inside a per-widget comprehension over ~50 widgets, producing ~1 + 3N ≈ 200 SQL round-trips per request. DB read-replica CPU at 80% confirms the query-count-bound signature.

## Proposed change

In `views/dashboard.py`:

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

## Evidence

- Inline `views/dashboard.py` shows three lazy attribute accesses per row inside the comprehension.
- Inline `models/widget.py` declares all three relationships with the SQLAlchemy default `lazy='select'`.
- DB-CPU=80%, memory normal — N+1 fingerprint.
- Latency math: 200 round-trips × ~8 ms typical replica RTT ≈ 1.6 s — consistent with the observed 1.8 s.

## Risks

- `joinedload` on the chained `last_edit→editor` introduces a 3-table outer join; verify with `EXPLAIN ANALYZE` that the planner uses the expected indices.
- `selectinload(tags)` uses `WHERE id IN (...)` — safe at N=50, may hit planner cliffs at N≫1000 (not in scope here).

## Test plan

- New: query-count test using `sqlalchemy.event.listen('before_cursor_execute', ...)` — assert ≤ 3 queries regardless of widget count.
- New: integration latency test asserting p99 < 200 ms with 50 seeded widgets.
- Existing endpoint tests must continue to pass unchanged.
