# Merged Fix — Layered Mitigation + Permanent Fix + Optional Restructure

## Diagnosis (consensus across all 4 Tier-2 agents)

The integration test `tests/api/test_user_session.py::test_concurrent_session_creation` is failing intermittently (~1 in 5 runs) on the 8-core CI runner because of a **classic check-then-act race** in `api/session.py:7-14`, which became reachable only after commit `7f3a9c1` moved session creation into `ThreadPoolExecutor(max_workers=8)`:

```python
def get_or_create_session(user: User) -> Session:
    if user.id in _session_cache:           # READ — no lock
        return _session_cache[user.id]
    session = Session(user_id=user.id, token=_generate_token())
    db_session.add(session)
    db_session.commit()                     # blocking I/O, GIL releases
    _session_cache[user.id] = session       # WRITE — happens AFTER commit
    return session
```

Two worker threads can both observe the cache miss, both construct a new `Session`, both `db_session.commit()`, and both write into `_session_cache` (the last write wins for the dict, but the test sees 2+ committed Session IDs in the returned list because each `future.result()` returned its own freshly-constructed Session object). Locally, the single-core Docker box serialises GIL releases at coarser granularity around `commit()`, making the race almost impossible to lose; the 8-core CI runner exposes it ~20% of the time.

## Recommended fix (layered)

### PR-0 — Pre-flight audit (blocker)

Before any code change, confirm:

1. Whether `db_session` in `api/db.py` is a `scoped_session` (thread-local) or a plain `Session` singleton. **If singleton: stop here. Migrate to `scoped_session` first** — sharing a plain SQLAlchemy `Session` across threads has its own correctness problems and any fix that ignores this leaves a latent bug.
2. With product: confirm "exactly one Session row per user" is the correct invariant. If not, adjust the UNIQUE constraint key in PR-2 accordingly.
3. Run `git grep _session_cache` — confirm no external callers depend on the cache being a module-global.

### PR-1 — Short-term mitigation (lands today, ≤ 1 hour)

Add a `threading.Lock` and use double-checked locking around the cache miss path in `api/session.py`:

```python
import threading
_cache_lock = threading.Lock()  # NEW — module level

def get_or_create_session(user: User) -> Session:
    cached = _session_cache.get(user.id)
    if cached is not None:
        return cached
    with _cache_lock:
        cached = _session_cache.get(user.id)   # double-check under lock
        if cached is not None:
            return cached
        session = Session(user_id=user.id, token=_generate_token())
        db_session.add(session)
        db_session.commit()
        _session_cache[user.id] = session
        return session
```

Also strengthen the existing test with a DB-readback assertion:

```python
def test_concurrent_session_creation(test_user, db_session):
    api.session._session_cache.clear()
    sessions = api.session.create_sessions_async([test_user] * 4)
    assert len({s.id for s in sessions}) == 1
    assert db_session.query(api.models.Session).filter_by(user_id=test_user.id).count() == 1
```

### PR-2 — Permanent fix (this week)

1. **Schema migration** — deduplicate existing rows, then add UNIQUE constraint:

   ```sql
   DELETE FROM sessions s1 USING sessions s2
     WHERE s1.user_id = s2.user_id AND s1.id > s2.id;
   ALTER TABLE sessions ADD CONSTRAINT uq_sessions_user_id UNIQUE (user_id);
   ```

2. **Application** — rewrite `get_or_create_session` to query, insert, and handle `IntegrityError` (full code in `fix-proposals/fix-2.md`). The `_cache_lock` from PR-1 is retained as a performance optimisation, no longer the correctness mechanism.
3. **New tests** — `test_db_uniqueness_enforced` (direct duplicate insert raises `IntegrityError`); `test_session_dedupe_across_processes` (two subprocesses, assert 1 row).

### PR-3 — Structural follow-up (optional, next sprint, conditional on measurement)

Apply `fix-proposals/fix-4.md` (delete `_session_cache`, switch to `SessionLocal()` context per call) **only if** profiling shows the cache is not load-bearing. Measure first; refactor second.

## Risk & rollback

- **PR-1 rollback**: revert the 5-line commit. Test goes back to failing 1/5; no data impact.
- **PR-2 rollback**: drop the UNIQUE constraint (`ALTER TABLE sessions DROP CONSTRAINT uq_sessions_user_id`). Application code revert is a single PR.
- **What to watch after PR-1**: throughput regression under load. The global lock serialises all session creation in the process. If profiling shows >5% latency regression on this code path, prioritise PR-2 to remove the lock's correctness role (cache becomes optimisation only), or evaluate per-key locking (Fix-5).
- **What to watch after PR-2**: `IntegrityError` rate on `sessions.user_id` UNIQUE constraint should be near-zero in steady state; a non-zero rate indicates the cache layer is missing hot paths.
- **What to watch overall**: any spike in "user logged in but session token doesn't work" reports — could indicate that the cache and DB have diverged (e.g. due to a failed-mid-commit scenario in PR-2's `IntegrityError` branch).

## Confidence on the merged plan

**0.88** — high enough to recommend without further escalation. Two open assumptions (PR-0 pre-flight items) are documented as blockers, not as risks to the plan's correctness.
