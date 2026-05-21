# Troubleshoot Report — Flaky concurrent session test

**Command**: `/sc:troubleshoot` (old, snapshot baseline) | **Mode**: diagnose-only (no `--fix`)
**Source**: subagent inline output (harness blocked direct file write)

## Diagnosis

**Unsynchronized check-then-act race in `get_or_create_session`.**

Two `ThreadPoolExecutor` workers both observe `user.id not in _session_cache`, both build a `Session`, both `db.commit()`, both write the cache. The check and the write are separate bytecodes; the GIL gives no protection across them, and the DB commit makes the critical section milliseconds wide.

## Why CI-only

8-core CI runs workers truly in parallel; the single-core local box time-slices under the GIL so the first task almost always finishes the cache write before the second is scheduled, hiding the race. Regression matches commit `7f3a9c1` which introduced the pool. "got 2" (not 4) is the expected outcome — first 2 threads collide, later ones hit the now-populated cache.

## Proposed Fix (Option A)

Wrap the miss path in a `threading.Lock`:

```python
_cache_lock = threading.Lock()
def get_or_create_session(user):
    with _cache_lock:
        if user.id in _session_cache:
            return _session_cache[user.id]
        s = Session(user_id=user.id, token=_generate_token())
        db_session.add(s); db_session.commit()
        _session_cache[user.id] = s
        return s
```

## Latent follow-up

Module-global `db_session` shared across pool workers is SQLAlchemy-unsafe — audit separately.

## Mode

No fix applied (no `--fix` flag).
