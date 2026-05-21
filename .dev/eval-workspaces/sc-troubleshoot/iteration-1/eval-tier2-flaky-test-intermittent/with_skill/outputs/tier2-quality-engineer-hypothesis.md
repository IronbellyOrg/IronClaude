# Hypothesis: The test asserts uniqueness from inside the same process that holds the racy cache — it cannot distinguish "no race" from "DB-level race"; the right fix is a DB UNIQUE constraint, not a Python lock

**Agent**: quality-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:18:02Z
**Cause class**: Race / concurrency (with test-design overlay)

## Claim

The Tier 1 hypothesis correctly identifies the check-then-act race in `_session_cache`, but it proposes a Python-level fix that papers over a more serious gap: the system has no database-level guarantee that a user gets at most one Session row. The test relies on a process-local dict to enforce a business invariant ("one session per user"), and the test is failing because that invariant is *not actually enforced* in the database. Slapping a `threading.Lock` around the dict makes the test green but leaves the production system exposed to the same bug across multiple worker processes (gunicorn `--workers N`, horizontal scaling, container restarts mid-request). The correct fix is a `UNIQUE` constraint on `Session.user_id` (or whatever the "one session per user" key is) plus `ON CONFLICT DO NOTHING` (or equivalent `INSERT ... ON DUPLICATE` / SAVEPOINT-and-retry) at the persistence layer. The cache then becomes a performance optimisation, not a correctness mechanism.

## Evidence

- **Inline snippet `api/session.py:10-13`**: `db_session.add(session); db_session.commit()` runs without any precondition that another concurrent commit hasn't already happened. No `SELECT ... FOR UPDATE`, no `INSERT ... ON CONFLICT`, no unique index implied by the code.
- **Inline snippet `tests/api/test_user_session.py:1-4`**: the test only inspects the *returned* `Session` objects from the in-process cache via `create_sessions_async([test_user] * 4)`. It does not query the database to verify how many rows were actually committed. **Even if the Python lock is added, the test could pass while leaving 2 committed rows** in a multi-process deployment — because each process has its own `_session_cache`.
- **Test-quality observation**: a test that asserts "one session per user" should ultimately read back from the DB: `assert db_session.query(Session).filter_by(user_id=test_user.id).count() == 1`. The current assertion is necessary but not sufficient.
- **Environment delta from issue**: 8-core CI exposes the race; production almost certainly runs on multi-core *and* multi-process (most ASGI/WSGI deployments do), so the bug is reachable in production too, not just in CI.

## Proposed Fix

Two-part fix; both parts are required:

1. **Schema (load-bearing):** add `UNIQUE` index on `Session.user_id` (assuming "one active session per user" is the invariant; if it's "one session per `(user_id, device_id)`" the constraint composes accordingly). Migration:

   ```sql
   ALTER TABLE sessions ADD CONSTRAINT uq_sessions_user_id UNIQUE (user_id);
   ```

2. **Application (load-bearing):** rewrite `get_or_create_session` to attempt insert and gracefully read back on UNIQUE violation:

   ```python
   def get_or_create_session(user: User) -> Session:
       existing = db_session.query(Session).filter_by(user_id=user.id).one_or_none()
       if existing is not None:
           return existing
       session = Session(user_id=user.id, token=_generate_token())
       try:
           db_session.add(session)
           db_session.commit()
           return session
       except IntegrityError:
           db_session.rollback()
           return db_session.query(Session).filter_by(user_id=user.id).one()
   ```

   The `_session_cache` dict can stay as a read-through cache for hot-path performance, but it is no longer the correctness mechanism.

Files that would change:

- `api/models.py` (or wherever `Session` is declared) — add `__table_args__ = (UniqueConstraint('user_id'),)` or equivalent.
- Migration file under `alembic/versions/` (or framework equivalent) — add the unique index.
- `api/session.py` — rewrite the function as above.

Test that would prove the fix:

- Existing test passes deterministically.
- New: `test_concurrent_session_creation_db_uniqueness` — same load pattern, but also asserts `db_session.query(Session).filter_by(user_id=test_user.id).count() == 1` after `create_sessions_async`.
- New: `test_session_dedupe_across_processes` — spawn two subprocesses each calling `create_sessions_async`, assert exactly one row.

## Confidence

Self-reported confidence: **0.80**

Per-dimension self-assessment:

- Evidence grounding: **0.5** — same inline-snippet constraint as Tier 1; the assertion-without-DB-readback observation is from the test snippet directly.
- Symptom coverage: **1.0** — explains the intermittent CI failure AND extends to a class of latent production bugs the Tier 1 fix would miss.
- Reproducibility fit: **0.5** — relies on the same single-/multi-core differential.
- Fix directness: **0.5** — fix is correct but larger: schema migration + application rewrite, two files instead of one.
- Domain coherence: **0.5** — spans application code + DB schema + test design.

## Risks

- **Migration is non-trivial.** If the database already has duplicate `user_id` rows (from prior CI runs that left orphan rows), the `UNIQUE` constraint will refuse to apply until the duplicates are cleaned. Mitigation: deduplication migration step first.
- **The "one session per user" assumption may be wrong.** If the product actually supports multiple concurrent sessions per user (e.g. one per device), then the right uniqueness key is composite. The test as written asserts uniqueness per user, but the *intent* may differ. This needs product confirmation before the schema change.
- **`IntegrityError` handling needs careful rollback** — if the surrounding transaction is part of a larger unit-of-work, the rollback may discard other pending changes. Safer to use a savepoint (`db_session.begin_nested()`).

## If I'm wrong, it's probably because

…the "one session per user" invariant is actually a soft invariant the product never wanted at the DB layer (e.g. sessions are short-lived and dedup is just a perf optimisation), in which case the Python lock from Tier 1 is the appropriate scoping and the schema change would be over-engineering.

## Alternatives considered

- **Python-level lock alone (Tier 1 fix)** — rejected as primary fix because it does not survive multi-process deployment. Acceptable as a *secondary* optimisation to reduce DB pressure.
- **`SELECT ... FOR UPDATE` on the user row before insert** — workable, but requires a `users` row to lock on and adds latency. UNIQUE constraint is cleaner.
- **Move dedup into `_executor` (one task per user)** — fragile; relies on caller serialising identical-user submissions, which contradicts the entire point of the test.

## Grounding gaps

- Cannot inspect the actual `Session` model to see if a UNIQUE constraint already exists (issue snippet only shows the function, not the model definition).
- Cannot determine whether `db_session` is a `scoped_session` or a plain `Session` — affects whether `IntegrityError` handling is safe in the proposed fix.
- Cannot run the failing test to confirm the symptom is "two committed rows" vs. "one committed row, two cached references" (the assertion `len({s.id for s in sessions}) == 1` would only fire on the former — confirming the DB-level bug suspicion).
