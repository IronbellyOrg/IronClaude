# Pre-Fix Pollution Baseline — Phase 1.3

**Captured:** 2026-05-19 02:03 UTC
**Repository root:** /config/workspace/IronClaude-T2-reflexion (working branch: fix/reflexion-test-pollution)
**Note:** Task file references `/config/workspace/IronClaude`; actual repo cwd is `/config/workspace/IronClaude-T2-reflexion`. Commands were executed against the actual repo path; semantics unchanged.

## (1) Total file count in `docs/mistakes/`

- Count: **84** (matches expected ~84 per research/02-test-fixtures.md §2)
- Command: `ls -1 docs/mistakes/ | wc -l`

## (2) Total line count in `docs/memory/solutions_learned.jsonl`

- Count: **588** (matches expected ~588 per research/02-test-fixtures.md §2)
- Command: `wc -l docs/memory/solutions_learned.jsonl` → `588 docs/memory/solutions_learned.jsonl`

## (3) Filename listing (`docs/mistakes/`)

All 84 files match the test-pollution shapes `test_*-YYYY-MM-DD.md` and `unknown-YYYY-MM-DD.md`. Three test names dominate (one per recorded test run date):

- `test_database_connection-<DATE>.md` — 28 files
- `test_reflexion_with_real_exception-<DATE>.md` — 28 files
- `unknown-<DATE>.md` — 28 files

Date range observed: `2025-11-11` through `2026-05-15` (sparse, one entry per test-run day). Full listing follows:

```
test_database_connection-2025-11-11.md
test_database_connection-2025-11-14.md
test_database_connection-2026-02-20.md
test_database_connection-2026-02-21.md
test_database_connection-2026-02-26.md
test_database_connection-2026-03-03.md
test_database_connection-2026-03-06.md
test_database_connection-2026-03-08.md
test_database_connection-2026-03-09.md
test_database_connection-2026-03-16.md
test_database_connection-2026-03-18.md
test_database_connection-2026-03-19.md
test_database_connection-2026-03-21.md
test_database_connection-2026-03-22.md
test_database_connection-2026-03-23.md
test_database_connection-2026-03-25.md
test_database_connection-2026-03-26.md
test_database_connection-2026-03-30.md
test_database_connection-2026-03-31.md
test_database_connection-2026-04-02.md
test_database_connection-2026-04-03.md
test_database_connection-2026-04-04.md
test_database_connection-2026-04-15.md
test_database_connection-2026-04-17.md
test_database_connection-2026-04-18.md
test_database_connection-2026-04-21.md
test_database_connection-2026-05-14.md
test_database_connection-2026-05-15.md
test_reflexion_with_real_exception-2025-11-11.md
test_reflexion_with_real_exception-2025-11-14.md
test_reflexion_with_real_exception-2026-02-20.md
test_reflexion_with_real_exception-2026-02-21.md
test_reflexion_with_real_exception-2026-02-26.md
test_reflexion_with_real_exception-2026-03-03.md
test_reflexion_with_real_exception-2026-03-06.md
test_reflexion_with_real_exception-2026-03-08.md
test_reflexion_with_real_exception-2026-03-09.md
test_reflexion_with_real_exception-2026-03-16.md
test_reflexion_with_real_exception-2026-03-18.md
test_reflexion_with_real_exception-2026-03-19.md
test_reflexion_with_real_exception-2026-03-21.md
test_reflexion_with_real_exception-2026-03-22.md
test_reflexion_with_real_exception-2026-03-23.md
test_reflexion_with_real_exception-2026-03-25.md
test_reflexion_with_real_exception-2026-03-26.md
test_reflexion_with_real_exception-2026-03-30.md
test_reflexion_with_real_exception-2026-03-31.md
test_reflexion_with_real_exception-2026-04-02.md
test_reflexion_with_real_exception-2026-04-03.md
test_reflexion_with_real_exception-2026-04-04.md
test_reflexion_with_real_exception-2026-04-15.md
test_reflexion_with_real_exception-2026-04-17.md
test_reflexion_with_real_exception-2026-04-18.md
test_reflexion_with_real_exception-2026-04-21.md
test_reflexion_with_real_exception-2026-05-14.md
test_reflexion_with_real_exception-2026-05-15.md
unknown-2025-11-11.md
unknown-2025-11-14.md
unknown-2026-02-20.md
unknown-2026-02-21.md
unknown-2026-02-26.md
unknown-2026-03-03.md
unknown-2026-03-06.md
unknown-2026-03-08.md
unknown-2026-03-09.md
unknown-2026-03-16.md
unknown-2026-03-18.md
unknown-2026-03-19.md
unknown-2026-03-21.md
unknown-2026-03-22.md
unknown-2026-03-23.md
unknown-2026-03-25.md
unknown-2026-03-26.md
unknown-2026-03-30.md
unknown-2026-03-31.md
unknown-2026-04-02.md
unknown-2026-04-03.md
unknown-2026-04-04.md
unknown-2026-04-15.md
unknown-2026-04-17.md
unknown-2026-04-18.md
unknown-2026-04-21.md
unknown-2026-05-14.md
unknown-2026-05-15.md
```

All 84 filenames match the test-pollution patterns `test_*.md` or `unknown-*.md` — no legitimate human-authored mistake docs are present in `docs/mistakes/`.

## (4) Last-commit reference for `docs/memory/solutions_learned.jsonl`

- SHA: `b3fdfb6057d4b053ec025452ce0e22c65ef07a04`
- Commit date: `2026-05-15 19:36:47 +0000`
- Command: `git log -1 --format="%H %ci" -- docs/memory/solutions_learned.jsonl`

## (5) Verdict

**BASELINE_CAPTURED: 84 files, 588 lines**
