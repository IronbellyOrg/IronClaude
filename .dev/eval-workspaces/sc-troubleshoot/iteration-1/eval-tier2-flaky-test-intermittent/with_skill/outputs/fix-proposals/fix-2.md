# Fix Proposal 2 — Add DB `UNIQUE` constraint on `Session.user_id` + `IntegrityError`-handled insert

**Champion**: quality-engineer
**Philosophy**: make the database enforce the invariant

## Problem statement

The same race as Fix-1, but the deeper problem: the system is using a process-local Python dict (`_session_cache`) to enforce a business invariant ("one session per user") that *should be* enforced at the database layer. The Tier 1 lock fixes the immediate test but leaves the invariant unenforced across multiple worker processes, container restarts, or any concurrent path that doesn't go through `get_or_create_session`. The right place to enforce uniqueness is the database, via a `UNIQUE` constraint, with `IntegrityError` handling for the race-loser.

## Proposed change

Two coordinated changes:

### Schema

```sql
-- migration: add unique constraint
ALTER TABLE sessions ADD CONSTRAINT uq_sessions_user_id UNIQUE (user_id);
```

If the table is defined via SQLAlchemy declarative, add a `UniqueConstraint`:

```python
# api/models.py
from sqlalchemy import UniqueConstraint

class Session(Base):
    __tablename__ = "sessions"
    # ... existing columns ...
    __table_args__ = (UniqueConstraint("user_id", name="uq_sessions_user_id"),)
```

### Application

```python
# api/session.py
from sqlalchemy.exc import IntegrityError

def get_or_create_session(user: User) -> Session:
    cached = _session_cache.get(user.id)
    if cached is not None:
        return cached
    existing = db_session.query(Session).filter_by(user_id=user.id).one_or_none()
    if existing is not None:
        _session_cache[user.id] = existing
        return existing
    candidate = Session(user_id=user.id, token=_generate_token())
    try:
        db_session.add(candidate)
        db_session.commit()
        _session_cache[user.id] = candidate
        return candidate
    except IntegrityError:
        db_session.rollback()
        existing = db_session.query(Session).filter_by(user_id=user.id).one()
        _session_cache[user.id] = existing
        return existing
```

(The cache remains as a read-through perf layer; it is no longer the correctness mechanism.)

## Evidence

- Inline snippet `api/session.py:10-12`: `db_session.add(session); db_session.commit()` with no DB-level uniqueness check.
- Inline snippet `tests/api/test_user_session.py:3-4`: the assertion checks only the *returned* in-memory objects; it does not verify the DB contains exactly one row. A green test with this assertion does not guarantee DB uniqueness — it only guarantees the in-process cache returned the same object 4 times.
- SQLAlchemy / general RDBMS knowledge: `UNIQUE` constraints are the canonical mechanism for "at most one row matching this key". `INSERT … ON CONFLICT DO NOTHING` (Postgres) or `INSERT IGNORE` (MySQL) provide atomic insert-or-skip; the `try/except IntegrityError + SELECT` pattern is the database-agnostic equivalent.

## Risks

- **Migration may fail on existing data.** If the database already has duplicate `(user_id)` rows (from prior CI runs or from the very bug this fixes), the `UNIQUE` constraint will refuse to apply. **Mitigation**: pre-migration step to deduplicate, e.g. `DELETE FROM sessions s1 USING sessions s2 WHERE s1.id > s2.id AND s1.user_id = s2.user_id;` (Postgres syntax).
- **Invariant may be wrong.** The change assumes "exactly one Session row per user" is the desired invariant. If the product actually supports multiple concurrent sessions (e.g. one per device, mobile + web), then the right uniqueness key is `(user_id, device_id)` or there is no uniqueness invariant at all. **Mitigation required**: confirm with product owner before shipping the migration.
- **`db_session.commit()` failure mode changes.** Today a duplicate insert succeeds (creating a duplicate row); after this change it raises `IntegrityError`. Any caller of `get_or_create_session` that already swallowed exceptions silently will see new behaviour. **Mitigation**: grep for call sites and audit error handling.
- **`db_session` thread-safety not addressed.** Same risk as Fix-1: if `db_session` is a singleton across threads, the SQLAlchemy Session corruption bug remains; the rollback in the `except` branch is *especially* fragile because rollback on a shared Session affects all in-flight units of work.

## Test plan

- [ ] `tests/api/test_user_session.py::test_concurrent_session_creation` passes 100/100 in CI.
- [ ] New: `test_db_uniqueness_enforced` — direct insert of duplicate `(user_id)` raises `IntegrityError` at the DB layer.
- [ ] New: `test_session_dedupe_across_processes` — spawn two subprocesses, each calling `create_sessions_async(test_user)`. Assert `SELECT COUNT(*) FROM sessions WHERE user_id = ?` = 1.
- [ ] Migration smoke test: apply the migration on a copy of production data; confirm no orphaned duplicates remain.
