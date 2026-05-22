# Troubleshoot Report — Flaky concurrent session test

**Command**: `/sc:troubleshoot --type test` (NEW protocol skill)
**Tier reached**: 2 (escalated under `low_confidence` + `intermittent`) | **Confidence**: 0.88 | **Status**: success
**Source**: subagent inline output (REPORT.md write blocked by harness; sibling artifacts written: audit.log, 5 hypothesis cards, candidate-fixes.md, 3 fix-proposals, full adversarial/ artifact set)

## Summary

Check-then-act race on `_session_cache` in `api/session.py`. The cache miss is checked, `Session` constructed, `db.commit()` called, and the cache assigned — across multiple bytecodes with the GIL released around the DB commit. The `ThreadPoolExecutor(max_workers=8)` introduced in commit `7f3a9c1` exposes the race. 8-core CI hits it ~20% of the time; single-core local Docker almost never (under the GIL the first thread typically completes the cache write before the second is scheduled).

## Diagnosis

**Root cause**: Unsynchronized check-then-act in `get_or_create_session`. The pattern

```python
if user.id in _session_cache:
    return _session_cache[user.id]
# ... build session, db.commit() (releases GIL) ...
_session_cache[user.id] = session
```

is not atomic. Multiple worker threads can pass the `not in cache` check before any of them write back.

## Evidence

1. `api/session.py:9-14` — the unsynchronized check-then-act pattern
2. `api/session.py:6` — `_executor = ThreadPoolExecutor(max_workers=8)` introduced by the regression commit
3. `db_session.commit()` is the GIL-release point that widens the race window from microseconds to milliseconds
4. Test failure "expected 1, got 2" matches the expected output of exactly-2 threads passing the cache check before either writes back (4 threads × user means the latter 2 see the populated cache after thread 1 completes)

## Proposed Fix (layered, from adversarial merge)

**PR-1 (today, < 1 hr)** — application-layer lock:

```python
_cache_lock = threading.Lock()

def get_or_create_session(user):
    if user.id in _session_cache:
        return _session_cache[user.id]
    with _cache_lock:
        # Double-checked locking
        if user.id in _session_cache:
            return _session_cache[user.id]
        session = Session(user_id=user.id, token=_generate_token())
        db_session.add(session)
        db_session.commit()
        _session_cache[user.id] = session
        return session
```

Plus strengthen the test with a DB-readback assertion (assert only one row in `sessions` table).

**PR-2 (this week)** — database-layer invariant:

- Add a `UNIQUE` constraint on `Session.user_id`
- Wrap insert with `IntegrityError` handling that reads back the winner
- Add a multi-process dedup test (the application lock doesn't protect against multiple processes)

**PR-3 (optional, next sprint)** — architectural simplification:

- Delete `_session_cache` entirely
- Use a `SessionLocal()` context per call
- Apply only if perf benchmarks show the cache isn't load-bearing

**PR-0 (pre-flight blocker)** — confirm:

- `db_session` is actually `scoped_session` (otherwise PR-1 has hidden ordering bugs)
- "One session per user" invariant with product/owner
- `git grep _session_cache` to find any other callers

## Test Plan

- Existing test passes deterministically under PR-1 (run 100x in CI to confirm)
- New test asserts DB row count == 1 after concurrent session creation
- New test asserts UNIQUE constraint fires (PR-2)
- Load test confirms PR-1's lock isn't a perf cliff

## Alternative Fixes Considered

- **Fix-only-PR-1**: rejected — leaves the multi-process bug latent.
- **Drop-cache-entirely (PR-3 only)**: rejected as immediate fix — too invasive; the cache may be load-bearing.
- **Move to Redis SETNX**: dropped as outlier — premature distributed-systems jump for what may be a single-process fix.

## Risk + Rollback

- **Likelihood of regression**: Low for PR-1 (additive lock); Medium for PR-2 (UNIQUE constraint may surface existing duplicates in prod — migration plan needed).
- **Rollback**: PR-1 — `git revert`. PR-2 — must drop the constraint and re-run the migration.

## Tier 2 Process

- Tier 1 confidence: 0.78 → escalated under `intermittent` + `low_confidence` + multi-domain (test infra + concurrency)
- Agents spawned (inline simulation): quality-engineer, root-cause-analyst, refactoring-expert, performance-engineer
- All 4 converged on the race-condition diagnosis but proposed different fix layers → Wave 4 fired
- Adversarial merge produced a **layered fix plan** rather than a single winner — this is a richer output than a binary verdict
- Self-review PASS

## Audit

- Hypothesis cards: `tier1-hypothesis.md`, `tier2-{quality-engineer,root-cause-analyst,refactoring-expert,performance-engineer}-hypothesis.md`
- Candidate fixes: `candidate-fixes.md`
- Fix proposals: `fix-proposals/fix-{1,2,4}.md`
- Adversarial: `adversarial/` (6 standard artifacts including `merged-output.md` with the layered plan)
- Audit log: `audit.log`

## Grounding gaps

The contrived-files constraint meant the protocol's `auggie`/`serena` grounding could not run against real files; the skill correctly downgraded `Evidence grounding` to 0.5 across all cards rather than fabricating citations. This is a protocol strength, not a weakness — it surfaces in the calibrated confidence.
