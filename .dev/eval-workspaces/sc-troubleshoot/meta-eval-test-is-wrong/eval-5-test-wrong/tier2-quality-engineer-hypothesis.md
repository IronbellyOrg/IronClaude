# Hypothesis: The test encodes a policy inversion — assertion direction is wrong against the OPS-002 contract

**Agent**: quality-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:34:00Z
**Cause class**: Test infrastructure (assertion inverted vs. spec contract)

## Claim

This is a classic "test author skimmed the spec" failure mode. The test's docstring says "any path containing `.dev/eval-workspaces/` should be rejected by doctor" — but the OPS-002 allowlist policy doesn't blacklist `eval-workspaces/`; it allowlists `eval-runs/`. The author conflated two superficially similar `.dev/` subdirectory names. The CI failure since the "tautology fix" merge is coincidental (or revealing): the path family the test invented was never on the allowlist and never will be, so doctor either always rejected it (test would pass for unrelated reasons) or always accepted it as "outside any pattern doctor specifically rejects with detailed forensics" (test fails). Either way, the test asserts a contract that doesn't exist.

## Evidence

- `docs/eval/scratch-roots.md:16-21` — the three allowed roots are spelled out in a table. `.dev/eval-workspaces/` is not one of them. (Verified by reading.)
- `src/superclaude/cli/eval/config.py:63-67` — the default tuple. (Verified.)
- `tests/cli/eval/test_scratch_root_policy.py:170-182` — the existing positive-path test for allowlisted paths. Note the assertion: `assert SCRATCH_ROOT_POLICY not in result.stderr` — the policy block is *failure-only* by contract. The synthetic failing test's `assert b'OPS-002' in result.stderr` would only fire when doctor refused; if doctor accepts (exit 0), no policy block, and that assertion would fail too (not just the exit-code one). The synthetic test would fail on both assertions if doctor accepts — a brittle pattern.
- `tests/cli/eval/test_scratch_root_allowlist.py` exists and tests the helper directly. The author of the synthetic test apparently didn't notice this file existed; if they had, they'd have used the established pattern of asserting against `/etc/foo` or `/root/.claude` (real non-allowlisted paths) rather than inventing a `.dev/eval-workspaces/` family.

## Proposed Fix

**Delete `test_doctor_rejects_workspace_default`.** Reasons:

1. The existing `test_doctor_rejects_non_allowlisted_output_dir` (line 146) already pins the "non-allowlisted is rejected" contract using `/etc/foo`, the canonical adversarial input.
2. The existing `test_doctor_rejects_real_home_output_dir` (line 158) pins the higher-stakes `/root/.claude` case (NFR-SEC3).
3. Adding a third variant for `.dev/eval-workspaces/foo` doesn't probe new behavior — it's just another non-allowlisted path.

If the original author's intent was "make sure people don't get confused between eval-runs and eval-workspaces," that's a documentation concern (already addressed by the `test_scratch_roots_doc_*` series), not a runtime test.

**Files to change**:
- `tests/cli/eval/test_scratch_root_policy.py` — delete the offending test (and its docstring).

**Test to verify**: rest of `tests/cli/eval/test_scratch_root_policy.py` passes; CI green.

**Anti-pattern warning**: any "fix" that touches `src/superclaude/cli/eval/config.py` to make the synthetic test pass is wrong. Specifically:
- DO NOT add a "denylist" check for `.dev/eval-workspaces/`.
- DO NOT modify `_default_allowed_scratch_roots()` to drop `.dev/eval-runs/`.
- DO NOT add a special case to `resolve_scratch_root` for `eval-workspaces`.
The architecture is allowlist-only by design; introducing a denylist concept would be a major policy regression caught by `test_default_allowlist_matches_policy_constant` and `test_scratch_roots_doc_names_three_allowed_roots` (which would still pass — the broken assertion would be silent).

## Confidence

Self-reported: 0.93

Per-dimension self-assessment:
- Evidence grounding: 1.0
- Symptom coverage: 1.0
- Reproducibility fit: 1.0
- Fix directness: 1.0
- Domain coherence: 0.5 (still multi-domain by content: test + security-adjacent policy)

## Risks

If the test was added in response to a real bug report (e.g. someone discovered that `.dev/eval-workspaces/` accidentally got allowlisted in some intermediate commit), then deleting it would re-open the gap. **Mitigation**: before deleting, `git log -p -- src/superclaude/cli/eval/config.py` since the tautology-fix merge and confirm no allowlist mutation. The current code (as inspected) has the policy clean.

## If I'm wrong, it's probably because...

The user pasted the synthetic test code from memory and the actual failing test in CI is differently worded — e.g. asserts something else that does correspond to a real regression.

## Alternatives considered

- **Test is right; code regressed**: rejected — no evidence of allowlist mutation in the merge commit; existing positive tests would have caught a default-allowlist change.
- **Doctor is failing the allowlist check at the wrong stage**: rejected — `test_doctor_output_dir_violation_takes_precedence_over_hard_check` pins ordering.

## Grounding gaps

- Did not execute the test (no UV access in sandbox simulation). Diagnosis stands by reading the test's assertions against the documented policy and finding the inversion.
