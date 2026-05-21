# Troubleshoot Report

**Target**: `/api/dashboard/summary` p99 latency regressed from 120 ms to 1.8 s after dashboard widget refactor
**Type**: performance
**Tier reached**: 2
**Confidence**: 0.92
**Status**: success
**Escalation reason**: low_confidence (Tier 1 confidence 0.80 < 0.85 threshold)
**Duration**: ~240 s
**Date**: 2026-05-21T05:34:00Z

---

## Summary

The endpoint triggers a classic SQLAlchemy N+1 query storm: the post-refactor list comprehension over ~50 widgets touches three lazy-loaded relationships per row (`owner`, `last_edit` then `editor`, `tags`), producing roughly 1 + 3N ~= 200 SQL round-trips per request and saturating the read replica. The fix is to add per-cardinality eager-loading options to the driving query — `joinedload` for the two single-row relationships and `selectinload` for the tag collection. This is a six-line change in `views/dashboard.py` with no schema or model-default changes; expected p99 returns to <= 200 ms.

## Diagnosis

**Root cause**: Three lazy SQLAlchemy relationships on `Widget` (`owner`, `last_edit` then `editor`, `tags`) are accessed inside a per-widget comprehension, each emitting a separate SQL `SELECT` on first attribute access. With ~50 widgets per typical user, this produces ~200 round-trips per request instead of the 1-3 a properly eager-loaded query would issue.

**Cause class**: Performance / resource — N+1 query (from the triage checklist).

**Detailed explanation**: The user-supplied `models/widget.py` snippet declares `owner`, `tags`, and `last_edit` with no `lazy=` kwarg, so they default to SQLAlchemy's `lazy='select'`, which lazy-loads each relationship via a separate SQL statement on first attribute access. The user-supplied `views/dashboard.py` snippet then iterates `widgets` and inside each iteration reads `w.owner.full_name`, `w.last_edit.editor.full_name` (a chained lazy access — two loads, not one), and `[t.name for t in w.tags]`. Each of those is a network round-trip to the read replica. The operational signal — DB-CPU pegged at 80% with normal memory — is the canonical query-count-bound footprint (vs. a memory-bound symptom, which would also show RAM pressure). The 15x latency multiplier is consistent with ~200 round-trips times typical replica RTT.

## Evidence

1. `views/dashboard.py` (inline user-supplied snippet) — inside the list comprehension over `widgets`, each iteration accesses `w.owner.full_name`, `w.last_edit.editor.full_name`, and `[t.name for t in w.tags]`. Three lazy attribute accesses per row, one of them chained.
2. `models/widget.py` (inline user-supplied snippet) — `owner = db.relationship('User', foreign_keys=[user_id])`, `tags = db.relationship('Tag', secondary='widget_tags')`, `last_edit = db.relationship('WidgetEdit', uselist=False)`. All three relationships use the SQLAlchemy default `lazy='select'` (no `lazy=` kwarg overrides it).
3. User-supplied operational signal — "Database CPU on the read replica is pegged at 80%. Memory profile looks normal." This is the textbook N+1 fingerprint (query-count-bound, not result-size-bound).
4. Regression timing — symptom appeared after the merge that touched these two files; the diff introduced the lazy access pattern inside the comprehension.
5. Latency arithmetic — ~50 widgets x ~4 lazy loads/row ~= 200 round-trips x ~8 ms typical replica RTT ~= 1.6 s, consistent with the observed 1.8 s p99.

## Proposed Fix

Add per-cardinality eager-loading options to the driving query in `views/dashboard.py`. Use `joinedload` for the two single-row relationships (`owner`, `last_edit` then `editor`) and `selectinload` for the `tags` many-to-many collection.

```python
from sqlalchemy.orm import joinedload, selectinload  # add import

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

**Files to change**:

- `views/dashboard.py` — change the driving query as above; add the `joinedload, selectinload` import. No change to `models/widget.py` (relationship defaults stay `lazy='select'` so other endpoints are unaffected).

**Test to verify**:

- New: query-count regression test using `sqlalchemy.event.listen('before_cursor_execute', ...)` to assert <= 3 SQL statements regardless of widget count (verify with N=1, N=50, N=200).
- New (or extend existing): latency regression test asserting endpoint p99 < 200 ms with 50 widgets seeded.
- Existing endpoint tests must continue to pass — response payload shape is unchanged.

**Mandatory validation follow-up**: run `EXPLAIN ANALYZE` on the read replica with a representative user to confirm the joined plan uses expected indices on `users.id`, `widget_edits.id`, `widget_edits.editor_id`, and `widget_tags.widget_id`.

**Apply with**: re-run `/sc:troubleshoot --type performance --fix "..."` to enter the Tier 3 task-builder chain, or apply manually with the diff above.

## Alternative Fixes Considered

- **Fix 2 — Uniform `selectinload` for all three relationships** (from `root-cause-analyst` Tier 2). Rejected because: 4 round-trips vs 2-3 with the per-cardinality strategy, and `selectinload` on a single-row relationship is non-idiomatic SQLAlchemy. Retained as the documented fallback if Fix 1 shows row-explosion in production (`EXPLAIN ANALYZE` validation step).
- **Fix 3 — Fix 1 in Phase 1 plus DTO/serializer plus `flask_caching` per-user TTL in Phase 2** (from `system-architect`). Rejected because: Phase 1 is identical to Fix 1; Phase 2 (caching + serializer refactor) is out of scope for a regression hotfix and introduces cache-invalidation risk. Phase 2 is correctly handled as a separate `/sc:improve` invocation — see Next Steps.

## Risk + Rollback

- **Likelihood of regression**: low — the change is per-query (`options(...)`), not a model default, so other consumers of `Widget.query` are unaffected.
- **Test coverage of the changed code**: partial — endpoint tests exist (assumed) but no query-count test; the proposed fix ships one.
- **Plan-shift risk**: medium until validated — the joined query may pick a different index than the pre-refactor lazy-loaded sequence. Mitigated by the mandatory `EXPLAIN ANALYZE` follow-up before merge to prod.
- **Row-explosion risk**: low at current scale — `selectinload(tags)` correctly avoids Cartesian explosion on the many-to-many; `joinedload` on `last_edit` to `editor` is a 1:1 path so width grows by a fixed number of columns, not rows.
- **Rollback**: single-query change; `git revert <commit>` restores prior behavior. If Fix 1 underperforms, swap to Fix 2 (uniform `selectinload`) — also a textual change.

## Grounding Gaps

- **Source files are inline snippets in the user prompt, not on disk** in this repo (`views/dashboard.py` and `models/widget.py` do not exist in this codebase). The eval harness instructed inline citation; MCP `auggie`/`serena` queries were therefore not applicable, and the Wave 5 file:line validation pass confirmed the inline snippet quotations match the prompt verbatim but could not be cross-checked against a working tree.
- **No reproducer run**: no test DB seeded, no benchmark executed, no `EXPLAIN ANALYZE` captured — those are part of the recommended pre-merge validation, not part of the diagnosis.
- **SQLAlchemy version unstated**: the fix syntax assumes 1.4+ / 2.0 idiom for `joinedload`/`selectinload`. On 1.3 or older, swap `selectinload` for `subqueryload`.

## Next Steps

- **Apply the fix**: re-run with `--fix` to enter the Tier 3 task-builder chain — `/sc:troubleshoot --type performance --fix "p99 latency jumped from 120ms to 1.8s on /api/dashboard/summary..."` — or apply the diff manually.
- **Pre-merge validation**: run `EXPLAIN ANALYZE` on the read replica with a representative user; confirm joined plan uses expected indices.
- **Follow-up improvement (separate ticket)**: consider `/sc:improve --type architecture views/dashboard.py` to introduce a `WidgetSummaryDTO` and per-user response cache. This is Phase 2 of Fix 3 — out of scope for this regression hotfix, but a sensible next step once the SLO is restored.

## Audit

- **Hypothesis cards**: `tier1-hypothesis.md`, `tier2-performance-engineer-hypothesis.md`, `tier2-root-cause-analyst-hypothesis.md`, `tier2-system-architect-hypothesis.md`
- **Candidate fixes index**: `candidate-fixes.md`
- **Fix proposals**: `fix-proposals/fix-1.md`, `fix-proposals/fix-2.md`, `fix-proposals/fix-3.md`
- **Adversarial artifacts**: `adversarial/debate-transcript.md`, `adversarial/merged-output.md`
- **Self-review**: PASS (recorded in `adversarial/merged-output.md` and `audit.log`)
- **Task file**: not generated — `--fix` was not set
- **Audit log**: `audit.log`
