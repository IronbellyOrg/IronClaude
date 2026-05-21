# Candidate Fixes — Tier 2

## Fix 1 — Rewrite test assertions to validate per-device contract; do NOT change api/session.py

**Supporting agents**: quality-engineer (0.90), root-cause-analyst (0.90), refactoring-expert (0.90)
**Verdict**: **consensus**

All three Tier 2 agents converged on the same fix-of-record: update
`tests/api/test_user_session.py::test_concurrent_session_creation` to assert the new per-device contract (one session per
device, distinct ids, distinct tokens, all attributable to `test_user`). Explicit instruction across all three cards:
**do NOT modify `api/session.py`** — doing so would regress the shipped per-device feature.

Differences are stylistic only:
- quality-engineer: minimal rewrite with 4 contract-shaped assertions
- root-cause-analyst: same minimal rewrite + raises a separate ticket for SQLAlchemy thread-safety in `create_sessions_async`
- refactoring-expert: structured contract block (named properties), reduces brittleness for future pivots

No competing fix proposals. **Wave 4 (adversarial debate) is SKIPPED** per Wave 3 exit criteria: "All agents converge with
high confidence → Skip Wave 4 (adversarial); jump to Wave 5."

## Out-of-scope follow-ups surfaced (not part of the chosen fix)

1. **SQLAlchemy thread-safety in `create_sessions_async`** (root-cause-analyst): module-level singleton
   `ThreadPoolExecutor` calling `db_session.add/commit` from up to 8 workers against a typically-shared session is a known
   concurrency hazard. May explain the 1/5 local-pass mystery; may also be a latent production-data-corruption risk. Open
   as a separate ticket; do not bundle.
2. **Fixture state leakage** (quality-engineer): the 1/5-pass rate suggests `test_user` and/or `db_session` fixtures may
   have scoping wider than `function` or imperfect teardown. Investigate `conftest.py`.

Both follow-ups are independent of the test fix and should NOT block it.
