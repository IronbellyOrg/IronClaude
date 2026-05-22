# Troubleshoot Report: `/api/dashboard/summary` p99 120ms → 1.8s

**Command**: `/sc:troubleshoot` (old, snapshot baseline) | **Type**: performance | **Mode**: diagnose-only (no `--fix`)
**Source**: subagent inline output (harness blocked direct file write)

## 1. Analyze

DB-bound regression: replica CPU 80%, memory normal, ~15x latency jump after a refactor that expanded the serialised payload. Signature = query-volume regression, not slow individual query.

## 2. Investigate — Root Cause

The list comprehension touches four lazy relationships per widget; none use eager-load options. With `lazy='select'` defaults:

| Per-row access | Queries per widget |
|---|---|
| `w.owner.full_name` | 1 (User) |
| `w.last_edit` | 1 (WidgetEdit) |
| `w.last_edit.editor.full_name` | 1 (User) |
| `[t.name for t in w.tags]` | 1 (Tag via widget_tags) |

For 50 widgets: 1 (widgets) + 50*4 = **~201 SELECTs per request**. At ~8ms each ≈ 1.6s — matches observed 1.8s. Replica CPU saturation is consistent with hundreds of tiny PK lookups under load.

**Why now**: pre-refactor response likely only returned `id`/`title`/`data`. The new `owner_name`/`last_editor`/`tag_names` fields each dereference a lazy relationship inside the 50-row loop — classic SQLAlchemy N+1.

**Ruled out**: memory leaks (profile normal), missing indexes (PK lookups, would slow individual queries not multiply them), `compute_data` alone (wouldn't pin replica).

## 3. Debug — Evidence

- Enable `SQLALCHEMY_ECHO=True` for one staging request → expect ~200 statements.
- Verify `compute_data()` isn't itself issuing queries (potential 5th N+1 source).
- `EXPLAIN` on a per-row query to confirm single-row PK lookup (not index issue).

## 4. Propose — Ranked Solutions

### Option A (recommended): Eager-load at the query site

```python
from sqlalchemy.orm import selectinload, joinedload

widgets = (Widget.query
    .filter_by(user_id=current_user.id)
    .options(
        joinedload(Widget.owner),
        selectinload(Widget.tags),
        selectinload(Widget.last_edit).joinedload('editor'),
    ).all())
```

- Query count drops ~201 → ~4 regardless of widget count.
- Risk: **low**. Read-side only, no schema/API change. Effort: minutes.
- Pitfall: `joinedload` on `tags` (M2M) would duplicate parent rows — use `selectinload`.

### Option B: Cache `compute_data()` per widget (invalidate on edit)

Orthogonal; apply only if p99 still exceeds target after A.

### Option C: Denormalise `owner_name`/`last_editor_name` onto `Widget`

Last resort.

## 5. Resolve — Verification Plan (when `--fix` is approved)

1. Apply Option A.
2. SQL echo on staging: confirm ~200 → ~4 statements for 50-widget fixture.
3. p99 target: ≤150ms (restore baseline).
4. Add regression test: assert query count ≤5 for 50-widget fixture.

## 6. Diagnosis-Only Notice

No files modified (no `--fix` flag).
