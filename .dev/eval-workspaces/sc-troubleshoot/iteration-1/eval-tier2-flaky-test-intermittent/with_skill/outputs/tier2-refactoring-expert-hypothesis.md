# Hypothesis: The whole construction is the bug — a module-level mutable cache + module-level executor + module-level DB session + thread-pool fan-out from a function with no scoping is structurally racy; the smallest-correct fix is to remove the module-level cache entirely and let the DB handle uniqueness

**Agent**: refactoring-expert
**Tier**: 2
**Timestamp**: 2026-05-21T05:18:25Z
**Cause class**: Logic regression (architectural) + Race / concurrency

## Claim

The Tier 1 lock fix and the per-thread Session fix both treat symptoms of a deeper smell: `api/session.py` has three module-level mutable singletons (`_executor`, `_session_cache`, and the imported `db_session`) interacting in ways that make every concurrent call a candidate for one of several races. The structurally simplest "correct" fix is to delete `_session_cache` outright and rely on the database as the source of truth for "does this user already have a session?" — which both eliminates the dict race (Tier 1's target) and forces the team to face the DB-uniqueness gap (quality-engineer's target) head-on. Code that reads `SELECT ... WHERE user_id = ?` is naturally race-free if the DB has a UNIQUE constraint, because the database itself is the synchroniser; no Python locks required.

## Evidence

- **Inline snippet `api/session.py:5-6`**: `_executor = ThreadPoolExecutor(max_workers=8)` and `_session_cache: dict[str, Session] = {}` are both module-level mutable state. Module-level state shared across threads is a code smell because it makes scoping invisible and lifecycle implicit.
- **Inline snippet `api/session.py:7-14`**: the function has *no parameters that scope the operation* — it takes a `User`, but otherwise reads and writes shared mutable state with no transaction boundary, no lock, no context manager. The function's contract ("return the one session for this user") is enforced by external coordination that does not exist.
- **Code review heuristic**: "a get_or_create function with a process-local cache, a DB write, and concurrent callers" is a classic pre-LLM-era footgun. The refactor in `7f3a9c1` introduced concurrency without revisiting the get_or_create contract — that's the regression.
- **Inline snippet `tests/api/test_user_session.py:2`**: `api.session._session_cache.clear()` — the test reaches into private state to reset it. This is a strong tell that the cache is an implementation detail leaking into tests; if the test has to know about the cache to make the system testable, the cache is in the wrong place.

## Proposed Fix

Restructure `api/session.py` to:

1. **Delete `_session_cache`** entirely.
2. **Add a UNIQUE constraint on `Session.user_id`** at the DB layer (overlaps with quality-engineer's proposal).
3. **Rewrite `get_or_create_session` to query + insert + handle IntegrityError**:

   ```python
   from sqlalchemy.exc import IntegrityError
   from api.db import SessionLocal

   def get_or_create_session(user: User) -> Session:
       with SessionLocal() as db:
           existing = db.query(Session).filter_by(user_id=user.id).one_or_none()
           if existing is not None:
               return existing
           candidate = Session(user_id=user.id, token=_generate_token())
           try:
               db.add(candidate)
               db.commit()
               return candidate
           except IntegrityError:
               db.rollback()
               return db.query(Session).filter_by(user_id=user.id).one()
   ```

4. **Optional perf layer** (only if profiling shows DB pressure): re-introduce a *read-through* LRU cache *outside* the get_or_create function, with TTL and an explicit thread-safety contract (e.g. `cachetools.TTLCache` + `threading.RLock` or `functools.lru_cache` with care).
5. **Optional: scope the executor.** If `_executor = ThreadPoolExecutor(max_workers=8)` is being shared across the whole module's lifetime, prefer scoping it to the caller (`with ThreadPoolExecutor(...) as ex:`) so lifetime is explicit.

Files that would change:

- `api/session.py` — significant rewrite (delete cache, rewrite get_or_create, optionally scope executor).
- `api/models.py` (or wherever `Session` lives) — add `UniqueConstraint('user_id')`.
- Migration file — apply unique index.
- `tests/api/test_user_session.py` — remove the `_session_cache.clear()` line (it no longer exists); add a DB-readback assertion.

Test that would prove the fix:

- Existing test passes deterministically *and* the test's `_session_cache.clear()` line is deleted (proving the cache no longer leaks into tests).
- New: `test_db_uniqueness_enforced` — direct DB insert of duplicate `user_id` raises `IntegrityError`.

## Confidence

Self-reported confidence: **0.70**

Per-dimension self-assessment:

- Evidence grounding: **0.5** — inline-snippet evidence; the "module-level state smell" is real but is an interpretation, not a citation.
- Symptom coverage: **1.0** — by eliminating both the cache race and the DB-uniqueness gap, every articulated symptom is addressed.
- Reproducibility fit: **0.5** — same intermittent constraint.
- Fix directness: **0.0** — this is the *least direct* fix; it touches the most files and requires schema + test changes. Justified only if the team is willing to revisit the design.
- Domain coherence: **0.5** — spans application, DB, and tests.

## Risks

- **Scope creep.** The user asked "why is my test flaky?" and this proposal answers "redesign the module." That is sometimes the right answer, but if the team is mid-sprint, the Tier 1 lock fix is the lower-risk landing.
- **Behavioural change.** Deleting `_session_cache` removes a hot-path optimisation. If session lookups are frequent and the DB query is expensive, response latency could regress noticeably. Mitigation: reintroduce the cache as a *read-through* layer with explicit thread-safety (item 4 above), after measuring.
- **Test changes required.** The `_session_cache.clear()` line in the test breaks — easy fix, but requires editing the test as part of the patch (which makes the diff larger and the review harder).
- **Migration coordination.** UNIQUE constraint addition has the same "may fail if duplicates exist" risk as the quality-engineer's proposal.

## If I'm wrong, it's probably because

…the `_session_cache` is load-bearing for a hot-path use case I cannot see from the snippet (e.g. internal microservice with 10k QPS for the same handful of users), in which case ripping it out is a perf regression and the right call is to make the cache thread-safe (Tier 1) and add the DB UNIQUE constraint (quality-engineer) in parallel.

## Alternatives considered

- **Keep the cache, just lock it (Tier 1)** — workable for the immediate test failure but leaves the test reaching into private state and leaves the multi-process race unsolved.
- **Replace `_session_cache` with `functools.lru_cache`** — `lru_cache` is *thread-safe for hits* but `dict.setdefault`-style atomic "create if missing" still requires either a lock or a `weakref.WeakValueDictionary` pattern; not a free fix.
- **Move dedup to caller** — pushes the problem out, doesn't solve it; callers would just race in turn.

## Grounding gaps

- Cannot measure actual DB pressure to know whether the cache is load-bearing or merely habit. The decision between "delete the cache" and "lock the cache" depends on that measurement.
- Cannot see the rest of `api/session.py` (only the snippet provided) — there may be other code paths that depend on `_session_cache` being a module-global (e.g. an admin endpoint that inspects the cache for diagnostics).
- Cannot verify the test suite passes with the rewritten module without running it.
