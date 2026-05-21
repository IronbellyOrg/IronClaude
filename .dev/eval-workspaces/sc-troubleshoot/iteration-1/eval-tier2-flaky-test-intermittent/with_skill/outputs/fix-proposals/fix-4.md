# Fix Proposal 4 — Delete `_session_cache` + DB UNIQUE constraint + `IntegrityError` insert (structural)

**Champion**: refactoring-expert
**Philosophy**: the construction is the bug — restructure

## Problem statement

`api/session.py` has three module-level mutable singletons (`_executor`, `_session_cache`, imported `db_session`) interacting with no scoping discipline. The dict race in Fix-1 and the missing DB constraint in Fix-2 are both *symptoms* of treating a database invariant as a Python-dict invariant. The structurally correct fix is to delete `_session_cache` outright, let the database be the source of truth for "does this user have a session?", and (optionally) reintroduce a cache as a *read-through* performance layer later, with explicit thread-safety, after measurement.

## Proposed change

```python
# api/session.py
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.exc import IntegrityError
from api.models import Session, User
from api.db import SessionLocal                # sessionmaker factory, not a Session instance

_executor = ThreadPoolExecutor(max_workers=8)

def get_or_create_session(user: User) -> Session:
    with SessionLocal() as db:
        existing = db.query(Session).filter_by(user_id=user.id).one_or_none()
        if existing is not None:
            return existing
        candidate = Session(user_id=user.id, token=_generate_token())
        try:
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            return candidate
        except IntegrityError:
            db.rollback()
            return db.query(Session).filter_by(user_id=user.id).one()

def create_sessions_async(users: list[User]) -> list[Session]:
    futures = [_executor.submit(get_or_create_session, u) for u in users]
    return [f.result() for f in futures]
```

Plus the schema change from Fix-2 (UNIQUE constraint on `Session.user_id`) and the test update:

```python
# tests/api/test_user_session.py
def test_concurrent_session_creation(test_user):
    # NOTE: _session_cache.clear() removed — cache no longer exists
    sessions = api.session.create_sessions_async([test_user] * 4)
    assert len({s.id for s in sessions}) == 1, f"expected 1 session, got {len({s.id for s in sessions})}"
    # New: verify DB-level uniqueness, not just in-memory dedup
    with SessionLocal() as db:
        assert db.query(api.models.Session).filter_by(user_id=test_user.id).count() == 1
```

## Evidence

- Inline snippet `api/session.py:5-6`: two module-level mutable singletons (`_executor`, `_session_cache`).
- Inline snippet `api/session.py:7-14`: function takes a `User` but reads + writes shared mutable state with no transaction boundary, no lock, no context manager — the contract ("one session per user") relies on external coordination that does not exist.
- Inline snippet `tests/api/test_user_session.py:2`: `api.session._session_cache.clear()` — the test reaches into private state, a strong tell that the cache is leaking into the public contract.
- General code-review heuristic: a `get_or_create` function with (a) a process-local cache, (b) a DB write, and (c) concurrent callers is a known footgun pattern. The refactor in `7f3a9c1` added (c) without revisiting (a) — that's the regression.

## Risks

- **Largest diff of the three proposals.** Touches `api/session.py`, `api/models.py`, a migration file, *and* the test file. Larger blast radius for review and revert.
- **Performance regression possible.** Removing the cache means every call hits the DB. If the workload genuinely benefits from caching (hot users, many lookups per request), wall-clock latency could regress noticeably. **Mitigation**: measure before deleting; if cache is load-bearing, reintroduce it as a *read-through* layer with `cachetools.TTLCache` + explicit `threading.RLock`.
- **Cache may be load-bearing elsewhere.** Inline snippet doesn't show all callers; `_session_cache` could be referenced from other modules (e.g. an admin diagnostic endpoint). **Mitigation required**: grep for `_session_cache` across the repo before deleting.
- **Test must be edited in the same PR.** This couples the bug fix to a test change, increasing review surface. Some teams prefer to keep "fix the bug" and "improve the test" as separate PRs; this proposal forces them to land together.
- **Same `db_session` thread-safety concern.** This proposal uses `SessionLocal()` as a context manager — a fresh Session per call — which actually *fixes* the thread-safety concern as a side effect. That's a feature, but it means the proposal is also implicitly a `db_session` lifecycle change, which has its own review surface.

## Test plan

- [ ] `tests/api/test_user_session.py::test_concurrent_session_creation` passes 100/100 in CI (with the updated assertion that includes DB readback).
- [ ] All other tests that reference `api.session._session_cache` (if any) are updated or fail-fast with a clear migration message.
- [ ] New: `test_db_uniqueness_enforced` — direct duplicate insert raises `IntegrityError`.
- [ ] New: `test_session_dedupe_across_processes` — two subprocesses, one row in DB.
- [ ] Benchmark: `test_get_or_create_latency_p99` — record p99 latency before / after, gate the merge on p99 ≤ +20% (or whatever the team's perf budget is).
