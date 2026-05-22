# Fix Proposal 1 — Add `threading.Lock` + double-checked locking around `_session_cache`

**Champion**: root-cause-analyst (Tier 1)
**Philosophy**: minimal, targeted, ship-today

## Problem statement

`api/session.py:7-14` performs a non-atomic check-then-act on `_session_cache`. Under `ThreadPoolExecutor(max_workers=8)` (added in commit `7f3a9c1`), two or more worker threads on a multi-core CI runner can interleave between the `if user.id in _session_cache:` check (line 8) and the `_session_cache[user.id] = session` write (line 13), each constructing and committing its own `Session` row before either populates the cache. The test `tests/api/test_user_session.py::test_concurrent_session_creation` asserts `len({s.id for s in sessions}) == 1` and fails ~20% of the time on the 8-core CI runner because 2+ distinct Session IDs are returned.

## Proposed change

Add a module-level `threading.Lock` and use the **double-checked locking** pattern around the cache-miss path. The fast path (cache hit) remains lock-free.

```python
# api/session.py
import threading
from concurrent.futures import ThreadPoolExecutor
from api.models import Session, User
from api.db import db_session

_executor = ThreadPoolExecutor(max_workers=8)
_session_cache: dict[str, Session] = {}
_cache_lock = threading.Lock()                            # NEW

def get_or_create_session(user: User) -> Session:
    cached = _session_cache.get(user.id)
    if cached is not None:
        return cached
    with _cache_lock:                                     # NEW
        cached = _session_cache.get(user.id)              # NEW — double-check
        if cached is not None:                            # NEW
            return cached                                 # NEW
        session = Session(user_id=user.id, token=_generate_token())
        db_session.add(session)
        db_session.commit()
        _session_cache[user.id] = session
        return session
```

## Evidence

- Inline snippet `api/session.py:7-14` (verbatim from issue): no lock, no `setdefault`, no atomic operation between the check and the write.
- Inline snippet `tests/api/test_user_session.py:1-4`: submits 4 references to the same user; asserts a single distinct `s.id`. Race is precisely the failure mode.
- Single-core local Docker vs. 8-core CI explains the 0% / 20% failure-rate differential.

## Risks

- **`db_session` may not be thread-safe.** SQLAlchemy `Session` is not thread-safe by design; if `db_session` is a singleton (not `scoped_session`), this fix closes the cache race but leaves the DB-session corruption bug latent. **Mitigation required**: confirm that `db_session` is a `scoped_session` before shipping. If not, this fix is incomplete and must be paired with Fix-3 (DB session scoping).
- **Multi-process deployment is unprotected.** The lock is process-local. A multi-worker gunicorn / uvicorn deployment can still produce 2+ committed `Session` rows because each process has its own cache and lock. The test will pass because the test runs in a single process, but production may still violate "one session per user". **Mitigation recommended**: add DB UNIQUE constraint in a follow-up (Fix-2 in part).
- **Lock held across `db_session.commit()`** — blocking I/O under the lock; throughput caps at ~1 commit / commit-latency for the whole process. Acceptable for typical session-creation rates (< 100 / sec / process); not acceptable for hot-path microservice workloads. **Mitigation recommended**: if profiling shows contention, switch to per-key lock (Fix-5).

## Test plan

- [ ] `tests/api/test_user_session.py::test_concurrent_session_creation` passes 100/100 runs locally and in CI.
- [ ] CI run is re-triggered 5× on the merge commit to confirm zero failures of this test.
- [ ] Stress test: `[test_user] * 64` returns exactly 1 distinct `Session.id`.
- [ ] (Optional, follow-up) `test_concurrent_distinct_users_throughput` baseline — record current throughput for regression detection if Fix-5 is later applied.
