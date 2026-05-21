# Merged Fix Proposal (Adversarial Output)

## Chosen fix

**Fix 1 — Per-cardinality loader strategy** wins the debate on correctness directness, minimum risk, and minimum diff size.

## Change

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

No change to `models/widget.py`. Defaults remain `lazy='select'`; the per-query `options(...)` overrides them only for this endpoint, preserving lazy behavior elsewhere.

## Test plan

1. **Query-count regression test** (new): hook `sqlalchemy.event.listen('before_cursor_execute', ...)`, hit `/api/dashboard/summary`, assert ≤ 3 SQL statements regardless of widget count (verify with N=1, N=50, N=200).
2. **Latency regression test** (new or extend existing): assert endpoint p99 < 200 ms with 50 widgets seeded for the current user.
3. **Existing endpoint tests** must continue to pass; correctness of the response payload is unchanged.

## Validation follow-up (mandatory before merge to prod)

- Run `EXPLAIN ANALYZE` on the read replica with a representative user to confirm the joined plan uses expected indices on `users.id`, `widget_edits.id`, `widget_edits.editor_id`, and `widget_tags.widget_id`.

## Rollback

Single-query edit. Revert with `git revert <commit>`.

## Edge cases verified in debate

- User with 0 widgets → query returns empty list; no relationship loads occur. Safe.
- Widget with `last_edit = None` → `joinedload(...).joinedload(...)` produces a left outer join; missing edit yields `None` and the existing conditional `w.last_edit.editor.full_name if w.last_edit else None` keeps working. Safe.
- Widget with empty tags → `selectinload(tags)` issues the IN-clause query and returns no rows for that widget. Safe.

## Self-review result

**PASS.** Self-review checked: (a) tests called out ✓, (b) edge cases covered ✓, (c) requirements met (latency reduction, no behavior change) ✓, (d) follow-up to validate SQL plan on read replica flagged ✓. No blockers.

## Fallback (if Fix 1 underperforms in production validation)

Swap `joinedload` → `selectinload` for `owner` and `last_edit→editor` (Fix 2). Trivial textual swap. No schema change required.
