# Fix Proposal 2 — Uniform selectinload

## Problem statement

Same diagnosis as Fix 1: N+1 storm from three lazy relationships in the dashboard comprehension.

## Proposed change

In `views/dashboard.py`:

```python
from sqlalchemy.orm import selectinload

widgets = (
    Widget.query
    .options(
        selectinload(Widget.owner),
        selectinload(Widget.last_edit).selectinload(WidgetEdit.editor),
        selectinload(Widget.tags),
    )
    .filter_by(user_id=current_user.id)
    .all()
)
```

## Evidence

- Same inline-snippet evidence as Fix 1.
- `selectinload` issues one extra `WHERE id IN (...)` per relationship — predictable, uniform, immune to Cartesian row explosion.

## Risks

- 4 round-trips instead of 2 with a mixed strategy — modest extra tail latency.
- Using `selectinload` for a single-row relationship is non-idiomatic; will draw reviewer questions.

## Test plan

- New: query-count test asserting exactly 4 queries.
- New: integration latency test asserting p99 < 250 ms with 50 seeded widgets.
