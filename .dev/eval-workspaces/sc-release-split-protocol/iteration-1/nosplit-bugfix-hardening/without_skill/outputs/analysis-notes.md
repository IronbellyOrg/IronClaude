# Analysis Notes: v2.28 Split Assessment

## Input Characteristics

- **Spec file**: spec-nosplit-bugfix.md
- **Release type**: Bugfix (3 related bugs)
- **Complexity class**: LOW
- **Estimated scope**: 150-200 lines production code
- **Files affected**: 2 (executor.py, models.py)
- **Functions modified**: 3 (_poll_subprocess, _cleanup_subprocess, execute_phase)
- **Priority**: P0

## Key Decision Factors

### Why this is obviously a no-split case

1. **Root cause unity**: The spec itself states "All three share the same root cause: the poll loop treats timeouts as terminal errors instead of retriable conditions." When bugs share root cause and fix location, splitting them apart is artificial.

2. **Function-level overlap**: R1 and R2 both modify `_poll_subprocess()`. You cannot split changes to the same function across releases without creating merge conflicts or requiring one release to be aware of the other's planned changes.

3. **Size**: 150-200 lines across 2 files is a small change by any standard. There is no cognitive overload argument.

4. **No natural seam**: If you tried to split, the most natural boundary would be {R1+R2} (poll loop changes) vs {R3} (cleanup changes). But even this fails because the timeout classification from R1 affects whether cleanup in R3 runs in the right code path. Testing R3 without R1 means testing against the wrong (buggy) timeout classification.

## If Forced to Split

The least-bad split would be:

- **Part A**: R1 (timeout classification) + R2 (I/O retry) — both in `_poll_subprocess()` + `execute_phase()`
- **Part B**: R3 (zombie cleanup) — `_cleanup_subprocess()` only

But this is still worse than shipping together because:
- Part B's test would need to mock timeout classification that Part A changes
- Two deployments for a P0 fix delays resolution
- The "zombie holds file locks" bug (R3) can be triggered by the timeout bug (R1), so fixing R1 without R3 still leaves users hitting file lock errors

## Confidence

**Confidence in no-split recommendation: 95%**

The only scenario where splitting might make sense is if there were a political/organizational reason (e.g., different teams own executor.py vs models.py). The spec gives no indication of this.
