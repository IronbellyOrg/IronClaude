# Hypothesis: `_session_cache` check-then-act has no lock, so two threads can both miss the cache and each create a Session row before either populates `_session_cache`

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:14:30Z
**Cause class**: Race / concurrency

## Claim

`get_or_create_session` performs a classic non-atomic check-then-act on the in-process `_session_cache` dict, with no `threading.Lock` guarding the read-then-write. Under the `ThreadPoolExecutor(max_workers=8)` introduced by commit `7f3a9c1`, on multi-core CI runners two or more workers can interleave between the `if user.id in _session_cache:` check on line 8 and the `_session_cache[user.id] = session` write on line 13, causing each thread to construct and commit its own `Session` row for the same `user.id`. The test then sees `len({s.id for s in sessions}) > 1` and fails. Locally the test passes because the single-core Docker dev box serialises GIL releases at coarser granularity around the `db_session.commit()` blocking call, making the race almost impossible to lose; the 8-core CI runner exposes it ~20% of the time.

## Evidence

- **Inline snippet `api/session.py` lines 7-14** (verbatim from issue):

  ```
  def get_or_create_session(user: User) -> Session:
      if user.id in _session_cache:           # line 8 — READ
          return _session_cache[user.id]
      session = Session(user_id=user.id, token=_generate_token())
      db_session.add(session)
      db_session.commit()                     # line 12 — blocking I/O, releases GIL
      _session_cache[user.id] = session       # line 13 — WRITE happens AFTER commit
      return session
  ```

  No `threading.Lock`, no `dict.setdefault`, no `_executor`-level deduplication — the read on line 8 and the write on line 13 are not atomic with respect to each other, and `db_session.commit()` between them is a guaranteed GIL-releasing blocking call.

- **Inline snippet `tests/api/test_user_session.py`**: the test submits `[test_user] * 4` — four references to the *same* user — to the executor. The assertion expects exactly one Session ID. The only way to see 2+ IDs is if 2+ threads both took the "cache miss" branch concurrently.

- **Environment delta from issue**: local = single-core Docker, CI = 8-core. Single-core severely reduces the probability of true thread interleaving inside the cache-miss window; 8-core multiplies it. This matches the observed "passes locally every time, fails 1/5 in CI" symptom exactly.

- **Commit-ish from issue**: `7f3a9c1` ("moved session creation into a thread pool") introduces the `ThreadPoolExecutor`, which is the moment the race becomes reachable. Before the refactor, presumably the same code ran sequentially per request and the race was unreachable.

## Proposed Fix

Guard the check-then-act with a `threading.Lock` (or use `dict.setdefault` with double-checked locking) inside `get_or_create_session`. Minimum diff in `api/session.py`:

```python
import threading
_cache_lock = threading.Lock()

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

Files that would change:

- `api/session.py` — add module-level lock + double-checked locking around the cache miss path.

Test that would prove the fix:

- Existing `tests/api/test_user_session.py::test_concurrent_session_creation` — should pass on 8-core CI deterministically once the race is closed.
- Suggested new test: stress version with 64 submissions and an explicit assertion of `len(set(s.id))==1` (run inside CI's multi-core runner).

## Confidence

Self-reported confidence: **0.78**

Per-dimension self-assessment (re-graded below per rubric):

- Evidence grounding: **0.5** — citation is the user-provided inline snippet, not a real `file:line` in this repo; the snippet itself unambiguously shows the race but we cannot run/observe the test.
- Symptom coverage: **1.0** — race explains intermittent failure, "passes locally on single-core", "fails ~1/5 on 8-core CI", started after commit `7f3a9c1`, and the specific assertion that fires (2 distinct Session IDs).
- Reproducibility fit: **0.5** — the symptom is *intermittent by nature*; we have the user's report but no local repro attempt.
- Fix directness: **1.0** — proposed lock is a 4-line change in the exact function whose race is identified.
- Domain coherence: **0.5** — primary domain is concurrency, but DB session lifecycle (`db_session` is module-global — is it thread-safe? typically `scoped_session` is required) and possibly DB UNIQUE-constraint design overlap. That overlap is exactly why one hypothesis may not be enough.

**Re-graded confidence (skill, not agent)** = mean(0.5, 1.0, 0.5, 1.0, 0.5) = **0.70**

## Risks

- **`db_session` itself may not be thread-safe.** In SQLAlchemy, a bare `Session` object is *not* designed for concurrent use across threads; the standard pattern is `scoped_session(sessionmaker(...))`. If `db_session` in the user's codebase is a plain Session shared across threads, the lock around the cache hides a second, deeper concurrency bug (state corruption inside the Session) that will surface elsewhere. The fix must therefore *also* be paired with confirming that `db_session` is a `scoped_session` (one Session per thread), otherwise we are putting a bandage on a wound that bleeds elsewhere.
- **The cache is process-local** — if the application runs multiple worker processes (gunicorn, uvicorn --workers N), the lock does nothing across processes and the same race is reachable inter-process. The "real" deduplication must live at the database layer (UNIQUE constraint on `(user_id)` + `ON CONFLICT DO NOTHING` or equivalent SELECT FOR UPDATE).
- **Lock could be held during `db_session.commit()`** — if commit is slow, this serialises all session creation. Acceptable for typical workloads but worth noting.

## If I'm wrong, it's probably because

…the actual race isn't in `_session_cache` at all — it's that `db_session` is shared across threads and `db_session.add()` + `db_session.commit()` corrupts the unit-of-work, with the visible symptom being multiple committed rows. In that case the fix is "use `scoped_session`" or "open a per-call Session", not "lock the cache".

## Alternatives considered

- **Test fixture leakage / shared `_session_cache` between tests** — rejected because the test explicitly calls `_session_cache.clear()` on its first line.
- **Token collision in `_generate_token()` producing duplicate IDs** — rejected because the assertion counts distinct `s.id`, not tokens; duplicate tokens would not cause this symptom (and would likely violate a UNIQUE constraint elsewhere).
- **DB-level race (UNIQUE violation handled silently)** — possible but secondary; would still require the cache-write to be racing to see 2 rows commit before either populates the cache.

## Grounding gaps

- The codebase is contrived — files do not actually exist in any repo; I cannot run `auggie__codebase-retrieval`, `serena__find_symbol`, or open `api/session.py` at a real path. The skill noted this explicitly in the audit log and downgraded `Evidence grounding` to 0.5.
- Could not execute the failing test or `git log -p` for commit `7f3a9c1` — the symptom analysis relies on the user's narrative (which is internally consistent: single-core local vs 8-core CI is a textbook concurrency-race tell).
- Could not verify whether `db_session` is `scoped_session` vs. a plain Session — this is the highest-impact unknown and is exactly the "If I'm wrong" branch.
