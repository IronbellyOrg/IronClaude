# Hypothesis: N+1 query storm from lazy relationships; uniform selectinload is the safest fix

**Agent**: root-cause-analyst
**Tier**: 2
**Timestamp**: 2026-05-21T05:31:55Z
**Cause class**: Performance / resource (N+1 query)

## Claim

Same root cause as Tier 1: three lazy relationships fired inside a per-widget comprehension produce a ~1 + 3N query storm. The fix should prefer uniform `selectinload` for all three relationships. `selectinload` issues one extra `SELECT ... WHERE id IN (...)` per relationship — totally predictable, immune to Cartesian row explosion, and uniform across cardinalities so future contributors do not have to reason about loader choice per relationship.

## Evidence

- `views/dashboard.py` inline snippet — `w.owner.full_name`, `w.last_edit.editor.full_name`, `[t.name for t in w.tags]` in the comprehension body.
- `models/widget.py` inline snippet — all three relationships use SQLAlchemy default `lazy='select'`. Confirmed by absence of `lazy=` kwarg.
- DB read-replica CPU at 80%, memory normal — query-count signature.
- Refactor timing — symptom started after the merge that introduced these access paths.

## Proposed Fix

Use `selectinload` for all three:

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

Files to change:

- `views/dashboard.py`.

Test to verify:

- Query-count test: assert exactly 4 queries (1 widgets, 1 owners, 1 last_edits, 1 editors via second selectin, 1 tags) — the contract is "constant query count regardless of N".
- Latency test at p99 < 250 ms for N=50.

## Confidence

Self-reported confidence: 0.85

Per-dimension self-assessment:

- Evidence grounding: 1.0
- Symptom coverage: 1.0 — same N+1 model
- Reproducibility fit: 0.5 — no benchmark
- Fix directness: 1.0
- Domain coherence: 1.0

Mean = 0.90

## Risks

- **Slightly more round-trips than `joinedload`** for the single-row relationships — 4 round-trips vs ~2 with a mixed strategy. At application scale this is a few extra ms.
- **`selectinload` of a single-row relationship is non-idiomatic** — most SQLAlchemy reviewers would flag it as "why not joinedload here". Defensible but worth a comment.
- **Plan stability**: simple `WHERE id IN (...)` is the most stable plan to predict — actually a *plus* for the read replica.

## If I'm wrong, it's probably because

`joinedload` would have been measurably faster than `selectinload` for the two single-row relationships and the small extra round-trips matter at the tail latency the user is watching.

## Alternatives considered

- **Per-cardinality strategy (performance-engineer's pick)**: cheaper but two reviewer questions ("why joinedload here, selectinload there?") forever after.
- **Default `lazy='selectin'` on the model**: would help every query, but a global change is out of scope for a single endpoint regression.

## Grounding gaps

- No on-disk source; inline only.
- SQLAlchemy version assumed 1.4+.
- No benchmark run.
