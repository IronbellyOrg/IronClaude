# Hypothesis: dashboard_summary triggers N+1 queries on owner, last_edit.editor, and tags

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:30:45Z
**Cause class**: Performance / resource (N+1 query)

## Claim

`dashboard_summary()` loads ~50 `Widget` rows in one query, then per-widget triggers three additional lazy SQL loads (`owner`, `last_edit` plus its `editor`, and `tags`). All three relationships default to `lazy='select'`, so each widget produces 3–4 follow-up round-trips. For a 50-widget user that is 1 + ~200 queries instead of a single eager-loaded plan. The DB read replica being pegged at 80% with normal memory is the canonical N+1 fingerprint, and the symptom appeared after a refactor that introduced exactly this access pattern.

## Evidence

- `views/dashboard.py` (user-provided snippet) — inside the list comprehension over `widgets`, each iteration accesses `w.owner.full_name`, `w.last_edit.editor.full_name`, and `[t.name for t in w.tags]` — three lazy-loaded relationships per row.
- `models/widget.py` (user-provided snippet) — `owner = db.relationship('User', foreign_keys=[user_id])`, `tags = db.relationship('Tag', secondary='widget_tags')`, `last_edit = db.relationship('WidgetEdit', uselist=False)` — all use the SQLAlchemy default `lazy='select'`, which emits a fresh SELECT on first attribute access.
- Operational signal from the user: "read replica CPU pegged at 80%, memory normal" — high query count, low payload size — classic N+1 (vs. a memory-blown result set which would also show RAM pressure).
- Regression timing: jump occurred after the merge that touched these two files — the diff introduced the relationship accesses inside the loop.

## Proposed Fix

Eager-load the three relationships in the query that drives the endpoint. Replace `Widget.query.filter_by(user_id=current_user.id).all()` with a query that pre-loads `owner`, `last_edit → editor`, and `tags` so the per-widget attribute accesses hit the identity map instead of the database.

Files that would change:

- `views/dashboard.py` — change the query to use `db.session.query(Widget).options(joinedload(Widget.owner), joinedload(Widget.last_edit).joinedload(WidgetEdit.editor), selectinload(Widget.tags)).filter_by(user_id=current_user.id).all()` (exact loader strategy is the question Tier 2 should settle).

Test to verify:

- New regression test: assert SQL query count for `dashboard_summary()` is ≤ 4 (one widgets, one or two joins, one selectin for tags) regardless of widget count, using a `sqlalchemy.event.listen('before_cursor_execute', ...)` counter or `pytest-sqlalchemy-mock`.
- Latency regression test (if benchmark harness exists): p99 < 200 ms at 50 widgets.

## Confidence

Self-reported confidence: 0.80

Per-dimension self-assessment:

- Evidence grounding: 1.0 — exact lines of the inline snippets cite the lazy attribute accesses and the relationship declarations.
- Symptom coverage: 0.5 — explains the latency jump direction and the DB-CPU signal, but does not arithmetic-prove the ~15x ratio (200 vs 1 query ≠ 15x by itself — network RTT/connection overhead would need to be modeled).
- Reproducibility fit: 0.5 — symptom is deterministic given a typical user, but no repro attempted in Tier 1 (no test DB, no benchmark run).
- Fix directness: 1.0 — eager-loading via `joinedload`/`selectinload` is a small, idiomatic, localized change in the query.
- Domain coherence: 1.0 — single domain: ORM query patterns. No cross-cutting concerns.

Mean = 0.80

## Risks

- **Row explosion**: using `joinedload` on `tags` (many-to-many) would multiply row count by tag count per widget; the snippet correctly distinguishes `selectinload` for the collection.
- **Read replica plan change**: the new eager-loaded query may change the chosen index. Validate with `EXPLAIN ANALYZE` on the read replica.
- **Identity-map confusion**: if some callers of `Widget.query` already rely on lazy loading for different access patterns, a global change to the relationship default would surprise them — the fix is per-query (`options(...)`), not per-relationship default, to avoid this.

## If I'm wrong, it's probably because

The DB CPU spike has a second cause (e.g., a missing index on `widget_tags(widget_id)` introduced in the refactor, or `current_user.id` resolution itself doing extra work) that eager-loading alone won't fix.

## Alternatives considered

- **Materialized view / read-side cache**: lower priority — caching a stale dashboard is a real fix but a heavier hammer; eager-loading should be tried first.
- **Pagination**: 50 widgets is small; pagination would treat the symptom but not the cause and would be UX-degrading.
- **Switching relationship defaults to `lazy='joined'`**: too coarse — affects every query against Widget, not just this endpoint.

## Grounding gaps

- Source files are **inline snippets in the user prompt, not on disk** in this repo — no MCP/serena/auggie grounding was possible; the eval harness instructed inline citation.
- No reproducer run: no test DB, no benchmark, no `EXPLAIN ANALYZE` output.
- SQLAlchemy version unknown — assumed 1.4+/2.0 idiom for `selectinload`/`joinedload`. If on an older version, loader syntax differs.
- Whether other consumers of `Widget.query` rely on current lazy behavior — not investigated in Tier 1.
