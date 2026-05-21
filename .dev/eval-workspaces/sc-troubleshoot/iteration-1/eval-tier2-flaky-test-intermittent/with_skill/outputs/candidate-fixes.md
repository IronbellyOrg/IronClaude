# Candidate Fixes — Tier 2 Cluster Index

All four agents agree on the **root cause class**: a concurrency race exposed when commit `7f3a9c1` moved session creation into `ThreadPoolExecutor(max_workers=8)`, with a multi-core CI runner amplifying the race window. They diverge on **where the fix belongs** (Python lock vs. DB constraint vs. DB-session lifecycle vs. structural rewrite).

## Cluster summary

| Fix # | Title | Supporting agent(s) | Layer | Verdict |
|-------|-------|---------------------|-------|---------|
| 1 | Add `threading.Lock` + double-checked locking around `_session_cache` | `root-cause-analyst (Tier 1)` | Application (Python) | **competing** |
| 2 | Add DB `UNIQUE` constraint on `Session.user_id` + `IntegrityError`-handled insert | `quality-engineer` | Schema + Application | **competing** |
| 3 | Fix DB session scoping: per-thread / per-call `scoped_session` instead of singleton `db_session` | `root-cause-analyst (Tier 2)` | DB session infrastructure | **supporting** (layered with 1 or 2) |
| 4 | Delete `_session_cache` entirely + rely on DB UNIQUE + IntegrityError pattern | `refactoring-expert` | Application (structural) + Schema | **competing** (superset of 2) |
| 5 | Per-`user_id` striped lock instead of global lock | `performance-engineer` | Application (Python) | **competing** (variant of 1) |

## Competing vs. consensus

- **Consensus**: there is a race, and `7f3a9c1` introduced it. Single-core local vs. multi-core CI explains the 1/5 failure rate. The `_session_cache` check-then-act on lines 8-13 is the proximate site.
- **Competing**: where the fix belongs. Fixes 1, 2, 4, and 5 propose materially different changes (one-line lock vs. schema migration vs. module rewrite vs. striped lock). Fix 3 is layered — it argues all of 1/2/4/5 are insufficient without also fixing `db_session`'s thread-safety contract.

Because **≥ 2 fixes are substantively different** (1 vs. 2 vs. 4 are the strongest representatives of three distinct philosophies), this cluster meets the **`competing` threshold** in Wave 3's exit criteria. **Wave 4 (adversarial fix debate) triggers.**

## Strongest representatives selected for adversarial debate

To keep the debate to 2-3 proposals (per protocol Wave 4 default), we pick the strongest of each philosophy:

- **Fix-1: Python lock** — represents the "minimal, targeted, ship-today" school. Champion: `root-cause-analyst (Tier 1)`.
- **Fix-2: DB UNIQUE constraint + IntegrityError pattern** — represents the "make the database enforce the invariant" school. Champion: `quality-engineer`.
- **Fix-4: Delete cache + DB UNIQUE + rewrite** — represents the "the construction is the bug, restructure" school. Champion: `refactoring-expert`.

**Excluded from adversarial debate** (but retained in the final report as alternatives considered):

- **Fix-3 (DB session scoping)** — supporting / layered concern, not a competing fix. Will be addressed in the merged fix's "must-also-confirm" section.
- **Fix-5 (per-key lock)** — variant of Fix-1; if Fix-1 wins the debate, the merged fix should consider Fix-5 as a follow-up optimisation, not a replacement.

## Domain coverage check

| Concern | Fix 1 | Fix 2 | Fix 4 |
|---------|-------|-------|-------|
| Closes test failure deterministically | ✓ | ✓ | ✓ |
| Survives multi-process deployment | ✗ | ✓ | ✓ |
| Preserves cache performance | ✓ | ✓ (cache retained) | ✗ (cache removed) |
| Minimal diff | ✓ | ✗ | ✗ |
| Requires DB migration | ✗ | ✓ | ✓ |
| Forces re-examination of `db_session` thread-safety | ✗ (recommended in risk) | ✗ | ✓ |
| Test changes required | ✗ | + new test | + remove `cache.clear()` line, + new test |

This table feeds the adversarial debate's correctness / risk / test-coverage focus.
