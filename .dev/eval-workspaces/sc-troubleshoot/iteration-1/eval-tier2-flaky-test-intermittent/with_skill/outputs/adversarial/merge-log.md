# Merge Log

## Source proposals

- `fix-proposals/fix-1.md` — Python `threading.Lock` (root-cause-analyst, Tier 1)
- `fix-proposals/fix-2.md` — DB UNIQUE + IntegrityError (quality-engineer)
- `fix-proposals/fix-4.md` — Delete cache + UNIQUE + restructure (refactoring-expert)

## Merge decisions

| Element | Source | Disposition |
|---------|--------|-------------|
| Diagnosis: cache check-then-act race exposed by `7f3a9c1` thread pool | All three | **Accepted** — consensus |
| Diagnosis: race amplified by single-core local vs 8-core CI | Fix-1 + Fix-2 + Fix-4 | **Accepted** — consensus |
| Fix shape: `threading.Lock` + double-checked locking | Fix-1 | **Accepted as PR-1** (short-term) |
| Fix shape: DB UNIQUE constraint | Fix-2 + Fix-4 | **Accepted as PR-2** (permanent) |
| Fix shape: `IntegrityError`-handled insert pattern | Fix-2 + Fix-4 | **Accepted as PR-2** |
| Fix shape: delete `_session_cache` | Fix-4 | **Deferred to PR-3** (conditional on perf measurement) |
| Fix shape: switch to `SessionLocal()` context per call | Fix-4 | **Deferred to PR-3** (with `_session_cache` deletion) |
| Test improvement: add DB-readback assertion | Fix-2 + Fix-4 | **Accepted in PR-1** (free improvement) |
| Test cleanup: remove `_session_cache.clear()` | Fix-4 | **Deferred to PR-3** (only valid if cache is deleted) |
| Pre-flight: confirm `db_session` is `scoped_session` | All three (risk sections) | **Accepted as PR-0** (blocker) |
| Pre-flight: confirm "one session per user" invariant | Fix-2 + Fix-4 | **Accepted as PR-0** (blocker) |
| Per-key (striped) lock pattern | Fix-5 (excluded from debate, retained as alt) | **Documented in alternatives**; conditional follow-up if global lock contends |
| Full `scoped_session` migration as same-PR change | Fix-3 (excluded from debate, retained as alt) | **Documented in alternatives**; conditional follow-up if pre-flight fails |

## Concessions made

- **Fix-1** concedes that it is not the *permanent* fix — only the *immediate* mitigation. The merge demotes Fix-1 from "the fix" to "the bandage that buys time for PR-2".
- **Fix-2** concedes that its migration coordination is not zero-effort, and accepts PR-1's lock as a layered short-term complement.
- **Fix-4** concedes that its full proposal is too large to ship in response to a CI failure, and accepts a phased approach where its structural improvements ride into PR-3 conditional on measurement.

## Self-review (executed inline by `self-review` agent simulation)

Standard four-question self-check on the merged plan:

1. **Are there tests for the change?** Yes — PR-1 adds DB-readback assertion; PR-2 adds `test_db_uniqueness_enforced` and `test_session_dedupe_across_processes`.
2. **Are edge cases covered?** Mostly — multi-process is covered by PR-2; multi-host / distributed deployment is out of scope but should be raised in the report.
3. **Does the change match the requirement?** Yes — the requirement is "diagnose and recommend a fix"; the merged plan provides both.
4. **Is there a follow-up needed?** Yes — PR-0 pre-flight (confirm `db_session` scoping, confirm invariant) is a blocker; PR-3 is an optional structural follow-up.

**Self-review verdict**: **OK — no blockers in the merged plan.** Pre-flight items are dependencies, not defects.
