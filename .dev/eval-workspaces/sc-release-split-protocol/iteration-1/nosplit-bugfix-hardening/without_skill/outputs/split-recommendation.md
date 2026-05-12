# Split Analysis: v2.28 Sprint Executor Timeout & Retry Hardening

## Recommendation: DO NOT SPLIT

This release should ship as a single unit. Splitting would add overhead with no meaningful benefit.

---

## Analysis

### 1. Shared Root Cause

All three bugs originate from the same architectural gap: the poll loop in `executor.py` treats non-fatal conditions as terminal errors. Bug 1 (timeout classification), Bug 2 (transient I/O retry), and Bug 3 (zombie cleanup race) are all consequences of the poll loop's overly simplistic error handling. Fixing any one of them in isolation would leave the others as ongoing regressions and would still require touching the same functions.

### 2. Minimal Scope

- **2 files changed**: `executor.py` and `models.py`
- **3 functions modified**: `_poll_subprocess()`, `_cleanup_subprocess()`, `execute_phase()`
- **1 enum added**: `TimeoutClassification`
- **150-200 lines of production code** estimated
- **4 regression tests**

This is well within the scope of a single coherent change. There is no complexity argument for splitting.

### 3. Tight Coupling Between Fixes

The fixes are not independent:

- **R1 and R2** both modify `_poll_subprocess()`. Splitting them into separate releases would require two sequential changes to the same function, increasing merge risk and review cost.
- **R1 and R3** interact at the `execute_phase()` level: the timeout classification (R1) determines whether cleanup (R3) runs in a "cancelled" or "completed" path. Testing R3 in isolation without R1's correct classification would require mocking behavior that R1 is supposed to provide.
- **R2 and R3** share the subprocess lifecycle: retrying I/O reads (R2) while also fixing process cleanup (R3) ensures that a retry loop does not interact with a half-cleaned-up zombie. Deploying R2 without R3 could surface new edge cases.

### 4. Split Would Increase Risk, Not Reduce It

Splitting a tightly coupled bugfix set creates:

- **Intermediate states** where some bugs are fixed and others are not, producing behavior that was never tested together
- **Doubled review and QA overhead** for what amounts to one logical change
- **Two deployments** instead of one, doubling rollout risk for a P0 fix
- **Branch management overhead** for no architectural benefit

### 5. No Organizational Reason to Split

- Single domain (backend, 90%)
- No separate teams or ownership boundaries involved
- No feature flags or gradual rollout needed (these are deterministic bug fixes)
- Direct deployment with simple revert path

---

## Scoring Summary

| Factor | Assessment | Supports Split? |
|--------|-----------|-----------------|
| Shared root cause | All 3 bugs stem from poll loop error handling | No |
| File overlap | 2 files, 3 functions — heavy overlap | No |
| Code size | 150-200 lines — small | No |
| Inter-fix dependencies | R1+R2 share a function; R1+R3 interact on phase transitions | No |
| Domain distribution | 90% backend, single team | No |
| Priority | All P0/P1, all needed urgently | No |
| Deployment complexity | Direct deploy, simple revert | No |

**Verdict: 0 of 7 factors support splitting.**

---

## Conclusion

This is a textbook single-release bugfix: small scope, shared root cause, overlapping code paths, single domain, and no organizational reason to split. Splitting would add process overhead and introduce risk from partially-fixed intermediate states. Ship it as v2.28.0.
