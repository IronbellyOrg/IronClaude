# Refactor Plan — Layered Merge

## Sequence

### PR-0 — Pre-flight audit (blocker, must complete before any PR-1+)

1. Confirm whether `db_session` in `api/db.py` is a `scoped_session` or a plain `Session` singleton.
   - If `scoped_session`: PR-1 can proceed unchanged.
   - If plain `Session`: stop. The bug is broader than the cache race. Migrate `db_session` to `scoped_session(sessionmaker(bind=engine))` (or expose `SessionLocal` factory) **first**, with its own PR. Fix-3 (root-cause-analyst Tier 2) becomes PR-1 in that case.
2. Confirm with product owner that "exactly one Session row per user" is the correct invariant.
   - If yes: proceed.
   - If "per (user, device)" or similar: amend the UNIQUE constraint key accordingly.
3. Run `git grep _session_cache` to find all references. If callers exist outside `api/session.py`, plan their migration in PR-3.

### PR-1 — Short-term mitigation (≤ 1 hour, lands today)

Apply **Fix-1** (process-local lock + double-checked locking) to `api/session.py`. This stops the CI failures immediately while the schema change is coordinated.

Diff:

```python
# api/session.py
+import threading
 import threading  # already there if not, ensure imported
 from concurrent.futures import ThreadPoolExecutor
 from api.models import Session, User
 from api.db import db_session

 _executor = ThreadPoolExecutor(max_workers=8)
 _session_cache: dict[str, Session] = {}
+_cache_lock = threading.Lock()

 def get_or_create_session(user: User) -> Session:
-    if user.id in _session_cache:
-        return _session_cache[user.id]
+    cached = _session_cache.get(user.id)
+    if cached is not None:
+        return cached
+    with _cache_lock:
+        cached = _session_cache.get(user.id)
+        if cached is not None:
+            return cached
+        session = Session(user_id=user.id, token=_generate_token())
+        db_session.add(session)
+        db_session.commit()
+        _session_cache[user.id] = session
+        return session
-    session = Session(user_id=user.id, token=_generate_token())
-    db_session.add(session)
-    db_session.commit()
-    _session_cache[user.id] = session
-    return session
```

Also update the test to add a DB-readback assertion (improvement borrowed from Fix-4):

```python
# tests/api/test_user_session.py
def test_concurrent_session_creation(test_user, db_session):
    api.session._session_cache.clear()
    sessions = api.session.create_sessions_async([test_user] * 4)
    assert len({s.id for s in sessions}) == 1, f"expected 1 session, got {len({s.id for s in sessions})}"
    # NEW: verify the invariant, not just the cache state
    assert db_session.query(api.models.Session).filter_by(user_id=test_user.id).count() == 1
```

### PR-2 — Permanent fix (this week)

Apply **Fix-2** (DB UNIQUE constraint + IntegrityError-handled insert). Migration runs first; deduplicate existing rows; then application code is updated.

1. Migration:

   ```sql
   -- Step 1: dedup existing duplicates (keep oldest row per user_id)
   DELETE FROM sessions s1
   USING sessions s2
   WHERE s1.user_id = s2.user_id AND s1.id > s2.id;

   -- Step 2: add the constraint
   ALTER TABLE sessions ADD CONSTRAINT uq_sessions_user_id UNIQUE (user_id);
   ```

2. Application: rewrite `get_or_create_session` to query + insert + handle `IntegrityError` (see Fix-2 for full code). The `_cache_lock` from PR-1 is retained but its role downgrades from "correctness" to "performance optimisation".
3. Tests: add `test_db_uniqueness_enforced` and `test_session_dedupe_across_processes`.

### PR-3 — Structural follow-up (optional, next sprint)

Apply **Fix-4** (delete `_session_cache`, switch to `SessionLocal()` context). Conditional on profiling showing the cache is not load-bearing.

1. Benchmark current `get_or_create_session` p99 latency.
2. Apply Fix-4 in a feature branch; rerun benchmark.
3. If p99 latency regression ≤ team's budget (typically +20%): merge. Else: keep the cache, harden it with `cachetools.TTLCache` + lock, file the structural improvement as tech debt.

## Why this sequence

- **PR-1 first** because the CI is currently failing and the team needs the signal back. A 5-line lock is faster to land than a schema migration.
- **PR-2 second** because it solves the *real* problem (DB invariant) without requiring the larger restructure.
- **PR-3 third** because it is a quality improvement, not a correctness fix, and should be measured before merged.

## Acceptance criteria

- After PR-1: `test_concurrent_session_creation` passes 100/100 in CI.
- After PR-2: `test_concurrent_session_creation` passes 100/100 *and* DB readback asserts 1 row *and* multi-process dedup test passes.
- After PR-3 (if undertaken): all of the above *and* p99 latency within budget *and* `_session_cache.clear()` no longer appears in any test.
