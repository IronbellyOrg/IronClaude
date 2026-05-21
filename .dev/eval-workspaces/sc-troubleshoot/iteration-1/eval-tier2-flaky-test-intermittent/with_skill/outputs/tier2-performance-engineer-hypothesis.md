# Hypothesis: The bug is the same race Tier 1 identifies, but the minimal-cost fix is to keep the existing cache and serialize on a per-`user_id` key (not a global lock) — locking the whole cache will serialise all session creation and cap throughput at 1 commit at a time

**Agent**: performance-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:18:33Z
**Cause class**: Race / concurrency (with throughput-cost overlay)

## Claim

Tier 1's "wrap a `threading.Lock` around the cache" fix is correct *for correctness* but is a significant performance regression once it lands: every `get_or_create_session` call holds the global lock across `db_session.commit()`, which is a blocking I/O call. With `max_workers=8` and any meaningful commit latency (e.g. 5-20 ms typical, longer under load), throughput collapses to ~50-200 ops/s regardless of how many workers exist. The structurally correct fix that preserves the parallelism the refactor was designed to provide is **per-key locking** — a striped lock or a `dict[user_id, threading.Lock]` so that concurrent creations *for different users* run in parallel, and only concurrent creations *for the same user* serialise. This is the textbook "stripe lock" pattern (cf. Guava's `Striped<Lock>`, Java's `ConcurrentHashMap.compute`, Python's per-key recipe with `WeakValueDictionary`).

## Evidence

- **Inline snippet `api/session.py:10-12`**: `db_session.add(session); db_session.commit()` is the slow path. Commit is I/O-bound, so a global lock around it serialises all session-creation throughput in the whole process.
- **Inline snippet `api/session.py:5`**: `_executor = ThreadPoolExecutor(max_workers=8)` — the explicit choice of 8 workers tells me the team *wants* 8-way parallelism. A fix that destroys that parallelism is a regression even if it fixes the test.
- **Inline snippet `tests/api/test_user_session.py:3`**: `create_sessions_async([test_user] * 4)` — the test exercises the *same-user* path, where serialisation is required. A real workload exercising 4 *different* users would want 4-way parallelism, which a per-key lock provides and a global lock does not.
- **Throughput math** (back-of-envelope): assume `db_session.commit()` averages 10 ms in CI. Under a global lock, max throughput = 100 ops/s on the whole process. Under per-key locking with N distinct users, max throughput ≈ N × 100 ops/s up to `max_workers=8`, i.e. 800 ops/s at saturation. That is the cost of choosing the global lock.

## Proposed Fix

Replace the single global lock with a per-user-id lock. Two implementation shapes:

**Shape A (simple, idiomatic):**

```python
import threading
from collections import defaultdict

_cache_lock = threading.Lock()                       # guards _locks itself
_locks: dict[str, threading.Lock] = defaultdict(threading.Lock)

def get_or_create_session(user: User) -> Session:
    cached = _session_cache.get(user.id)
    if cached is not None:
        return cached
    with _cache_lock:
        per_user_lock = _locks[user.id]              # atomic get-or-create
    with per_user_lock:
        cached = _session_cache.get(user.id)
        if cached is not None:
            return cached
        session = Session(user_id=user.id, token=_generate_token())
        db_session.add(session)
        db_session.commit()
        _session_cache[user.id] = session
        return session
```

**Shape B (no leaked locks):** use `WeakValueDictionary` for `_locks` so locks are garbage-collected after the per-user creation completes, avoiding a memory leak for systems with high user-id cardinality.

Files that would change:

- `api/session.py` — add `_cache_lock` + `_locks` and replace the cache write block with the pattern above.

Test that would prove the fix:

- Existing `test_concurrent_session_creation` — passes deterministically (same-user case still serialises correctly).
- New: `test_concurrent_distinct_users_parallel` — submit `[user_a, user_b, user_c, user_d]` and assert wall-clock time is closer to 1× commit-latency than 4×.
- New (load): a benchmark asserting throughput ≥ `(N_users * 1/commit_latency)` to catch future regressions to a global lock.

## Confidence

Self-reported confidence: **0.65**

Per-dimension self-assessment:

- Evidence grounding: **0.5** — inline-snippet citation; throughput math is illustrative not measured.
- Symptom coverage: **0.5** — fixes the failing test but adds *throughput preservation*, which the user did not ask about. May be solving a problem they don't have yet.
- Reproducibility fit: **0.5** — same intermittent constraint.
- Fix directness: **0.5** — fix is in the right function but larger than the Tier 1 lock.
- Domain coherence: **1.0** — correctness + perf trade-off is one coherent domain.

## Risks

- **Adds complexity for a problem the user may not have.** If the production workload never hits enough concurrent same-process session creations for the global-lock contention to matter, this fix is over-engineering.
- **`defaultdict` is not thread-safe.** The pattern above wraps `_locks[user.id]` in `_cache_lock` for that reason; a careless implementation that omits the outer lock reintroduces a (less harmful but real) race.
- **Memory leak if not using `WeakValueDictionary`.** Long-running processes accumulate one `Lock` per unique user id ever seen. Shape B fixes this; Shape A may leak in production over weeks.

## If I'm wrong, it's probably because

…the actual bottleneck is not in this function at all (it's downstream in the DB), in which case the global lock has identical real-world throughput to per-key locking and the simplicity wins.

## Alternatives considered

- **Single global lock (Tier 1)** — correct, simpler, but caps throughput.
- **`functools.lru_cache(maxsize=...)` with explicit thread-safety** — `lru_cache` is thread-safe for reads but does not solve the "create if missing" race; same problem in different clothes.
- **Move dedup to DB UNIQUE constraint** (quality-engineer's hypothesis) — solves correctness fully *and* sidesteps the locking question; arguably the better destination, but requires schema change.

## Grounding gaps

- Cannot measure the production workload — without numbers, the per-key-vs-global lock decision is judgement, not data.
- Cannot verify whether `db_session.commit()` is actually expensive enough to make the global lock contention matter.
- Did not benchmark the Tier 1 fix to confirm it actually causes throughput collapse — the claim is from `commit()`-is-I/O reasoning, not measurement.
