# Diff Analysis — Fix-1 vs Fix-2 vs Fix-4

## Diff dimensions

| Dimension | Fix-1 (Lock) | Fix-2 (UNIQUE + IntegrityError) | Fix-4 (Delete cache + UNIQUE + restructure) |
|-----------|--------------|----------------------------------|---------------------------------------------|
| Files touched | 1 (`api/session.py`) | 3 (`api/session.py`, `api/models.py`, migration) | 4 (above + `tests/api/test_user_session.py`) |
| Lines changed (estimate) | ~5 | ~25 | ~45 |
| Requires DB migration | No | Yes | Yes |
| Requires test edit | No | New test only | Existing test edited + new tests |
| Closes the immediate test | Yes (in-process only) | Yes (always) | Yes (always) |
| Closes the production bug | Partial — single-process only | Yes | Yes |
| Reversible without data loss | Yes (trivial) | Migration reversible; data may have grown | Yes (cache reintroducible) |
| Time-to-ship estimate | < 1 hour | 2-4 hours | 1-2 days |
| Throughput impact | Negative under contention | Neutral (cache retained) | Negative until cache reintroduced |
| Forces team to confront `db_session` thread-safety | Risk-section recommendation only | Risk-section recommendation only | Implicitly — by switching to `SessionLocal()` context |

## Differences in fault model

- **Fix-1** assumes the fault is a Python-level race in a process-local dict and treats the database as innocent. **Fault model: incomplete** — does not survive multi-process deployment.
- **Fix-2** assumes the fault is a missing database invariant and uses application code to remedy a race the DB should refuse. **Fault model: complete for "one session per user"** if and only if that invariant is correct.
- **Fix-4** assumes the fault is a structural mismatch: enforcing a database invariant in Python state. Removes the mismatch entirely. **Fault model: complete and forward-compatible**, but pays for it with diff size.

## Overlap

- All three close the immediate test failure on the 8-core CI runner.
- Fix-2 and Fix-4 share the schema change.
- Fix-1 and Fix-4 are the most extreme on the diff-size axis (smallest / largest); Fix-2 sits between.

## Orthogonal concerns each proposal does **not** address

- None of the three explicitly fixes `db_session` thread-safety (Fix-4 does so implicitly via `SessionLocal()` context). If `db_session` is a singleton plain Session, Fix-1 and Fix-2 leave the latent corruption bug.
- None of the three addresses whether the "one session per user" invariant is correct in the first place; that is a product question that should bound the choice.
- None proposes a per-key lock (Fix-5) — that variant of Fix-1 would preserve same-user serialisation without serialising all sessions. Worth folding into the merge as a follow-up if Fix-1 wins.
