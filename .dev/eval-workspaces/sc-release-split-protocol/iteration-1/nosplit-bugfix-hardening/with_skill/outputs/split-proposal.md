# Split Proposal — v2.28 Sprint Executor Timeout & Retry Hardening

## Discovery Analysis

### Spec Summary

v2.28 fixes 3 related bugs in the sprint executor's subprocess management. All three share the same root cause: the poll loop treats timeouts as terminal errors instead of retriable conditions. The release scope is:

- **R1**: Reclassify max_turns timeout (P0) — `TimeoutError` should map to `PASS_NO_SIGNAL`, not `FAILED`
- **R2**: Add transient I/O retry (P0) — empty reads from subprocess stdout need retry with backoff
- **R3**: Fix zombie cleanup (P1) — `_cleanup_subprocess()` must wait for process exit and escalate
- **R4**: Regression tests for all three (P1)

All changes touch 2 files: `executor.py` (poll loop, cleanup, classification) and `models.py` (new enum).

Estimated scope: 150-200 lines production code. Complexity: LOW.

### Dependency Chain Analysis

```
models.py: TimeoutClassification enum (new)
     ↓
executor.py: _poll_subprocess() ← uses enum (R1) + adds retry logic (R2)
executor.py: _cleanup_subprocess() ← wait + escalate (R3)
executor.py: execute_phase() ← maps TURN_LIMIT to PASS_NO_SIGNAL (R1)
     ↓
R4 tests: cover all three behaviors
```

R1 and R2 share the same function (`_poll_subprocess`). R1 depends on the new enum from `models.py`. R3 is in a different function but in the same file, and is triggered by the same error-handling flow. R4 depends on all three.

The dependency chain is **linear and tightly coupled**. R1 and R2 modify the same function. R3 is called from the same error path. There is no natural seam — you cannot ship R1 without R2 because they modify the same function body.

### Discovery Questions

**1. What are the dependency chains? Which items are prerequisites for others?**

All three bugs are in the same error-handling flow within `_poll_subprocess()` and `_cleanup_subprocess()`. R1 and R2 literally modify the same function. R3 is called when R1/R2's error path triggers cleanup. The dependency is not sequential (R1 then R2 then R3) — it is lateral. They are facets of the same fix.

**2. Are there components that deliver standalone value and can be validated through real-world use before the rest ships?**

No. Shipping only R1 (timeout reclassification) without R2 (retry) would leave the poll loop in an inconsistent state: timeouts are handled correctly but I/O errors still kill the phase. The real-world validation scenario (run a sprint under load) would exercise both paths. Validating R1 alone would require carefully avoiding I/O pressure, which is the opposite of real-world testing.

Shipping R1+R2 without R3 (zombie cleanup) is closer to viable, but the zombie problem (R3) is triggered by the same conditions that R1 and R2 address — a phase that times out or encounters I/O errors then needs cleanup. Testing R1+R2 in real-world conditions would immediately expose R3.

**3. What is the cost of splitting?**

- **Integration overhead**: Modifying `_poll_subprocess()` twice (once for R1+R2 in Release 1, then again if R3 interactions need adjustment in Release 2) creates merge risk in a function that is already the root cause of all three bugs.
- **Context switching**: Two PRs, two reviews, two deploy cycles for 150-200 total lines of code.
- **Release management burden**: Disproportionate to the scope. The coordination overhead of two releases likely exceeds the implementation effort of the entire fix.
- **Rework risk**: R3's zombie cleanup interacts with the error classification from R1. Splitting them means the R3 fix may need to account for intermediate states that won't exist in the final version.

**4. What is the cost of NOT splitting?**

- **Delayed feedback**: Minimal. The entire fix is 150-200 lines with clear before/after behavior.
- **Big-bang risk**: Low. All three bugs are well-understood with evidence from logs and CI data. The fix is not speculative.
- **Root-cause isolation**: Easier as a single release because the shared root cause means any regression points to the poll loop refactor.

**5. Is there a natural foundation vs. application boundary?**

No. All three requirements are at the same abstraction level: they are all patches to the poll loop's error handling. There is no "foundation" that R2 consumes from R1. The `TimeoutClassification` enum (R1) is a supporting detail, not a foundation.

**6. Could splitting INCREASE risk?**

Yes. Splitting R1+R2 from R3 would ship an incomplete fix for the poll loop. Users who hit the zombie process bug (R3) after Release 1 would see a confusing intermediate state: timeouts are classified correctly (R1) and I/O retries work (R2), but cancelled phases still leave zombies that corrupt the next phase. This is arguably worse than the current state because users might trust the "fixed" poll loop and be surprised by zombie corruption.

### R1-Scope Assessment (fidelity-schema default)

The fidelity-schema bias asks: is there a subset focused on planning fidelity and schema hardening? The `TimeoutClassification` enum (R1) could be considered "schema hardening," but it is a 5-line enum that exists solely to support the behavioral fix in `execute_phase()`. Shipping it alone provides zero user-facing value.

### Smoke Gate Assessment (r2 default)

Not applicable — there is no natural Release 2 to place a smoke gate in.

---

## Recommendation: DO NOT SPLIT

**Confidence: 0.95**

### Rationale

This release is a textbook example of a change that should NOT be split:

1. **Shared root cause**: All three bugs stem from the poll loop treating errors as terminal. The fix is conceptually one change expressed across three manifestations.
2. **Shared code**: R1 and R2 modify the same function. R3 is in the cleanup function called from the same error path.
3. **No natural seam**: There is no point where "Release 1 delivers independently testable value" because the value is the complete fix to error handling.
4. **Disproportionate overhead**: Two releases for 150-200 lines of code in 2 files creates more coordination cost than the entire implementation.
5. **Splitting increases risk**: An intermediate state with partial error handling fixes is more confusing than the current broken state.

### Risks of Not Splitting (and Mitigations)

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| All three fixes interact badly | Low — they are well-isolated within their functions | Code review focuses on poll loop state transitions |
| Regression in one fix masks another | Low — R4 tests each behavior independently | Test each requirement in isolation before integration test |
| Rollback is all-or-nothing | Acceptable — if any fix regresses, all three should revert since they share root cause | Git revert is single commit |

### Alternative Strategies for Early Validation Without Splitting

1. **Staged code review**: Review R1 (classification) → R2 (retry) → R3 (cleanup) as sequential commits within a single PR, validating each before proceeding.
2. **Feature flag**: Gate the retry behavior (R2) behind a flag if there is concern about backoff timing. But this is likely over-engineering for a 100ms retry.
3. **CI canary**: Deploy to CI first with the artificial max_turns integration test. Monitor `test_sprint_parallel` flake rate for 24 hours before production deploy.
