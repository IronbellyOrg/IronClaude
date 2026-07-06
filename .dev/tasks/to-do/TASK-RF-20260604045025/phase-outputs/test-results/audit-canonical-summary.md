# Audit CanonicalFixtureParity Summary — Step 3.1 (Bug A)

**Timestamp:** 2026-06-04 05:18
**Overall result:** PASSED ✅

## Command

```
uv run pytest tests/audit/test_slow_shrink_continues.py tests/audit/test_monotonicity_halt_F_5_5_5.py tests/audit/test_synthetic_dnsp_dedup_not_regression.py tests/audit/test_regression_halt_pass1_fail2.py -k Canonical
```

## Counts

- **Passed:** 27
- **Failed:** 0
- **Skipped:** 0
- **Deselected:** 67 (non-Canonical tests filtered out by `-k Canonical`)
- **Process exit code:** 0

## Final pytest summary line

```
====================== 27 passed, 67 deselected in 0.08s =======================
```

## Expected `27 passed` observed?

**YES** — exactly 27 passed, matching the research evidence prediction (`01-fix-evidence.md`: "uv run pytest <4 audit files> -k Canonical → 27 passed"). All `TestCanonicalFixtureParity` tests across the 4 audit files now pass against the tracked fixtures committed in Step 2.2 (SHA `b9d533ff`). This confirms Bug A's fix: the fixtures are now present/tracked so `test_canonical_log_present` assertions and the `canonical_log_text` `read_text` fixtures succeed.

Raw output preserved at: `phase-outputs/test-results/audit-canonical.txt`.
