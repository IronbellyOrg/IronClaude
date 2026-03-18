---
parent-spec: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/evals/files/spec-nosplit-bugfix.md
split-analysis: "no-split-recommended"
rationale: "3 bugs sharing root cause in 2 files with 150-200 lines total scope — no natural seam, no independently valuable subset, splitting increases risk"
status: validated
---

# v2.28 — Sprint Executor Timeout & Retry Hardening — Validated Spec

## Why This Release Stays Intact

The split analysis evaluated all plausible split points and found none that satisfy the protocol's requirements for a valid split:

1. **No natural seam**: R1 (timeout classification) and R2 (I/O retry) modify the same function (`_poll_subprocess()`). R3 (zombie cleanup) is called from the same error path. There is no boundary where one subset delivers independently testable value.

2. **Shared root cause**: All three bugs stem from the poll loop treating every non-success as a terminal error. The fix is conceptually one change with three manifestations.

3. **Splitting increases risk**: An intermediate state where timeouts are reclassified (R1) and I/O is retried (R2) but zombies are not cleaned up (R3) is arguably more confusing than the current state, because users would trust the "fixed" poll loop and be surprised by zombie corruption.

4. **Disproportionate overhead**: Two release cycles for 150-200 lines of code creates more process cost than implementation cost.

## Risks Addressed Without Splitting

| Risk | How Mitigated |
|------|--------------|
| All three fixes deployed simultaneously | R4 regression tests validate each behavior independently; failures are isolatable via test output |
| Poll loop is critical path | CI canary with artificial timeout integration test; 24-hour soak before production deploy |
| Windows-specific cleanup behavior | Test on both Linux and Windows CI runners |
| Regression in shared function | Staged code review: R1 changes → R2 changes → R3 changes as sequential commits within single PR |

## Validation Strategy

Since the release is kept intact, early feedback is obtained through:

1. **Staged code review**: Review R1 (classification), R2 (retry), R3 (cleanup) as sequential commits. Each commit is reviewable independently even though they deploy together.

2. **CI canary deployment**: Deploy to CI environment first. Run the integration test with artificial `max_turns` limit. Monitor `test_sprint_parallel` flake rate for 24 hours.

3. **Targeted regression testing**: R4 tests each bug fix independently:
   - Test: max_turns timeout produces `PASS_NO_SIGNAL` status
   - Test: empty stdout read is retried (mock pipe buffer pressure for unit test, real load for integration)
   - Test: zombie process is fully cleaned up before next phase
   - Test: file locks released after cleanup

4. **Real-world validation**: After CI canary passes, run a full sprint with known timeout conditions on a staging environment. Verify:
   - Phases that hit max_turns are classified as `PASS_NO_SIGNAL` (check sprint log)
   - CI flake rate on `test_sprint_parallel` drops below 3% within 1 week
   - `Ctrl+C` during a phase leaves no zombie processes (check process table)
   - Next phase after cancellation can write result files without `PermissionError`

## Original Spec Updates

The following improvements were identified during the analysis and are incorporated:

### Clarification: R1 and R2 share implementation scope

The original spec lists R1 and R2 as separate requirements, which is correct from a requirements perspective. However, the architecture section should note explicitly that both modify `_poll_subprocess()` and should be implemented as a single refactor of that function, not as two independent patches.

### Addition: Cross-platform cleanup validation

R3 mentions Windows-specific behavior (`process.terminate()` + `process.wait()`). The testing strategy (R4) should explicitly include cross-platform CI validation, not just "run on Windows." Specifically:
- Linux CI: verify SIGTERM → wait → SIGKILL escalation
- Windows CI: verify `terminate()` → `wait()` flow
- Both: verify file lock release

### Clarification: Retry counter observability

R2 specifies adding a retry counter to phase metrics. The success criteria should include verifying that this counter is visible in sprint logs and that it resets between phases.

## Traceability

All original requirements are preserved in this validated spec:

| Original Req | Status | Notes |
|-------------|--------|-------|
| R1: Reclassify max_turns timeout | PRESERVED | No changes to scope or criteria |
| R2: Add transient I/O retry | PRESERVED | No changes to scope or criteria |
| R3: Fix zombie cleanup | PRESERVED | No changes to scope or criteria |
| R4: Add regression tests | PRESERVED | Cross-platform testing clarification added |
| Architecture: 2 files only | PRESERVED | No new modules or interfaces |
| Rollout: Direct deployment | PRESERVED | CI canary strategy added as validation, not a gating change |
| Success criteria: 4 items | PRESERVED | All four criteria unchanged |
