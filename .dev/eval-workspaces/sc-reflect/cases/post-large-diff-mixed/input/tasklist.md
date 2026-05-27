# STUB — iteration-1 follow-up fleshes out content. Spec §12.3 row 3.
# 15-item tasklist for the mixed-deviation post-execution fixture.

- Task 1: Add `users.py` skeleton with `list_users()` returning the legacy flat list shape.
- Task 2: Add JSON schema for user object.
- Task 3: Wire users.py into the v1 router.
- Task 4: Add unit tests for users.py CRUD happy paths.
- Task 5: Document the users API contract in `docs/api/v1/users.md`.
- Task 6: Add structured logging to users.py at INFO level.
- Task 7: Implement a thread-pool-based job dispatcher in `queue/dispatcher.py`.
- Task 8: Add tests for dispatcher under load.
- Task 9: Implement an LRU cache helper with default capacity = 128.
- Task 10: Add tests for the LRU cache.
- Task 11: Implement OAuth code exchange in `auth/oauth.py` per the standard flow.
- Task 12: Add tests for the OAuth flow.
- Task 13: Add a `/health` endpoint.
- Task 14: Wire Prometheus metrics emitter at `metrics/emit.py`. Authorized: may add StatsD alongside Prometheus if convenient.
- Task 15: Add a smoke-test CI job.
