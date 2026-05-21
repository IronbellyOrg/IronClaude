# Hypothesis: The actual race is `db_session` being shared across executor threads — the `_session_cache` race is a symptom but not the deepest cause; the fix is per-thread (or per-call) DB Session scoping

**Agent**: root-cause-analyst (Tier 2 pass)
**Tier**: 2
**Timestamp**: 2026-05-21T05:18:14Z
**Cause class**: Race / concurrency (DB session lifecycle, not just dict)

## Claim

`db_session` in the snippet is a module-level singleton imported from `api.db`. SQLAlchemy's `Session` is explicitly documented as **not thread-safe** — sharing a single `Session` across threads corrupts its identity map, unit-of-work, and connection ownership. The `ThreadPoolExecutor(max_workers=8)` introduced in `7f3a9c1` puts up to 8 threads through `db_session.add()` and `db_session.commit()` *simultaneously*, and the visible symptom — two committed `Session` rows for the same user — is one of the many possible failure modes of that misuse (others include phantom rollbacks, "object already attached", and stale identity-map reads). The `_session_cache` race in the Tier 1 hypothesis exists, but closing it does not address the underlying SQLAlchemy misuse: even with the cache locked, `db_session` is still being driven by 8 threads simultaneously and *will* eventually emit a different concurrency bug (e.g. "Session is already flushing").

## Evidence

- **Inline snippet `api/session.py:1-3`**: `from api.db import db_session` — singular, suggesting a module-level Session, not a `scoped_session` factory. (Compare with the idiomatic `db.session = scoped_session(sessionmaker(...))` where `db.session` proxies to a thread-local Session.)
- **Inline snippet `api/session.py:10-12`**: `db_session.add(session); db_session.commit()` is called from inside a function passed to `_executor.submit(...)` — i.e. from inside a worker thread that is *not* the thread that imported / configured `db_session`. This is the textbook SQLAlchemy anti-pattern.
- **SQLAlchemy docs (well-known)**: `Session` objects are not safe for use in concurrent threads; the recommended pattern is `scoped_session` or "one Session per request / per logical operation" with explicit lifecycle (open → use → close). Source: SQLAlchemy Session FAQ — "Is the Session thread-safe?" → "No, it is not."
- **Commit `7f3a9c1` shape from issue narrative**: the refactor *moved session creation into a thread pool*, which is the precise moment the thread-safety contract was violated. Before the refactor, presumably the caller held `db_session` on the request thread and the contract was satisfied.

## Proposed Fix

Replace the singleton `db_session` usage inside thread-pool tasks with a per-call DB Session. Two viable shapes:

**Shape A (minimal):** open a new Session inside the worker function:

```python
from api.db import SessionLocal  # the sessionmaker, not a Session instance

def get_or_create_session(user: User) -> Session:
    if user.id in _session_cache:
        return _session_cache[user.id]
    db = SessionLocal()
    try:
        session = Session(user_id=user.id, token=_generate_token())
        db.add(session)
        db.commit()
        _session_cache[user.id] = session
        return session
    finally:
        db.close()
```

**Shape B (idiomatic):** use `scoped_session` keyed by thread:

```python
# api/db.py
db_session = scoped_session(sessionmaker(bind=engine))
# api/session.py — usage unchanged, but db_session now returns a thread-local Session
# Add a teardown in the executor's task wrapper: db_session.remove() after the task.
```

Files that would change:

- `api/db.py` — switch `db_session` to a `scoped_session` *or* expose a `SessionLocal` factory.
- `api/session.py` — open + close a Session per task (Shape A) or add `db_session.remove()` teardown (Shape B).

The `_session_cache` race is real but is a *secondary* concern. Once each thread has its own DB Session, the dict race produces at worst two committed rows that violate a DB UNIQUE constraint — which is the quality-engineer's concern, not this one's. A complete fix is layered:

1. Per-thread DB Session (this hypothesis).
2. UNIQUE constraint at DB layer (quality-engineer hypothesis).
3. Optional: lock the cache to avoid the wasted SQL round-trips.

Test that would prove the fix:

- Existing `test_concurrent_session_creation` becomes deterministic (because the underlying Session corruption is gone *and* the dedup is enforced at the DB layer).
- New: a SQLAlchemy `Session.info` inspection test that confirms each executor thread sees a distinct Session identity.

## Confidence

Self-reported confidence: **0.72**

Per-dimension self-assessment:

- Evidence grounding: **0.5** — citation is inline snippet; the SQLAlchemy thread-safety claim is well-documented but I cannot point to a `file:line` for `db_session`'s actual definition in this contrived repo.
- Symptom coverage: **0.5** — explains the underlying misuse but the *immediate* observable symptom (two distinct `Session.id` values) is more directly produced by the dict race. This hypothesis covers the deeper bug; Tier 1 covers the proximate one.
- Reproducibility fit: **0.5** — same intermittent-CI evidence; deeper bug may be even harder to reproduce.
- Fix directness: **0.5** — fix is larger than Tier 1's single lock; touches two files including DB infra.
- Domain coherence: **1.0** — concurrency + DB session lifecycle is one coherent domain.

## Risks

- **`db_session` may already be `scoped_session`.** If `api/db.py` already wraps `sessionmaker` in `scoped_session`, then the thread-safety concern is moot and this hypothesis is wrong (or only partially right — the `_session_cache` race remains). Cannot verify without the file.
- **`scoped_session` requires teardown** — without `db_session.remove()` after each task, threads accumulate Sessions that never get garbage-collected, leading to a slow connection-pool leak. Important to wire teardown into the executor task wrapper.
- **Changing DB session scope can break callers** that rely on the current singleton behaviour (e.g. tests that import `db_session` and pre-populate it). Migration needs to audit call sites.

## If I'm wrong, it's probably because

…`db_session` is already a `scoped_session` and the surface bug is purely the dict race, in which case the Tier 1 fix is sufficient and this hypothesis is over-reaching.

## Alternatives considered

- **Refactor to async / `asyncio`** — out of scope; the user's refactor moved *to* threads, not away from them.
- **Use a single-worker executor (`max_workers=1`)** — defeats the purpose of the refactor; not a real fix, just hides the bug.
- **Add a `threading.local()` to wrap `db_session`** — equivalent to `scoped_session`; reinventing wheel.

## Grounding gaps

- Cannot read `api/db.py` to confirm whether `db_session` is `scoped_session` or a plain `Session`. **This is the single highest-leverage unknown.** If it's already scoped, my hypothesis collapses into "the cache race only" (Tier 1).
- Cannot inspect SQLAlchemy version pin (older versions had different thread-safety nuances).
- Cannot observe whether the test actually sees two committed rows (DB-level) or just two cached objects (cache-level) — both produce the symptom, but the fixes diverge.
