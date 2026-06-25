# QA Report — M-N Divergence Verdict Correctness

**Topic:** FR-RH2 final QA gate — M,N divergence verdict/exit/slug correctness
**Date:** 2026-06-20
**Phase:** doc-qualitative
**Fix cycle:** N/A

---

## Overall Verdict: PASS

No M,N divergence verdict/exit/slug defects found in the reviewed scope. The implementation and I3-I6 tests correctly map success-count M and model-class diversity to the expected reflect verdicts, with the Q6-resolved M==0 slug `contract-missing` rather than the superseded spec-table slug `ensemble-empty`.

## Scope Notes

- The user-provided absolute spec path `/config/workspace/IronClaude/.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` did not exist in this worktree checkout.
- I located and read the worktree-local spec path from the scope manifest: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`.
- Fix authorization was false; no source files were modified.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Scope manifest identifies relevant implementation/test/evidence files | PASS | Read `qa-gate-scope.md` lines 8-20 and 22-42: ensemble.py, contract.py, test_ensemble_stub_integration.py, Q6 decision, and phase6 I1-I9 outputs are all in scope. |
| 2 | Spec oracle for `mn_guard_table`, `worker_status_to_m`, and `transport_enum` | PASS | Read spec lines 243-266 for FR-RH2.9 and lines 446-463 for `mn_guard_table`, `worker_status_to_m`, and `transport_enum`. |
| 3 | M==0 maps to blocked / exit 2 / Q6 slug `contract-missing` | PASS | `build_reflect_contract` returns `None` when `reviewer_count == 0` (ensemble.py lines 285-288); `_emit_reflect_contract` unlinks/omits the top-level contract for `None` (lines 396-402); `derive_verdict(None, child_rc=0)` returns BLOCKED with `contract-missing` (contract.py lines 160-164); `Verdict.BLOCKED.exit_code == 2` (models.py lines 43-48); I6 asserts contract is None, BLOCKED, exit 2, reason `contract-missing` (test lines 272-279); captured phase6-i6 output passed. |
| 4 | M==1 maps to degraded / exit 11 and spec-compliant slug behavior | PASS | For one survivor, `build_reflect_contract` sets `tier_reached = 1` and `merge_method = single-reviewer-fallback` (ensemble.py lines 290-291). `derive_verdict` checks degraded trigger 6 (`expected_tier >= 2 and tier_reached == 1`) before fallback trigger 10 (contract.py lines 262-281), so the actual reason may be `degraded-tier1`, not `single-reviewer-fallback`; this is spec-compliant because FR-RH2.9 accepts `single-reviewer-fallback` and/or `tier_reached==1` (spec lines 253-264). `Verdict.DEGRADED.exit_code == 11` (models.py lines 43-48). I5 asserts non-PASS, exit 11, fallback/tier1 signals, and failed I1-positive predicate (test lines 242-253); captured phase6-i5 output passed. |
| 5 | M>=2 same-class maps to degraded-model-diversity / exit 11 | PASS | `compute_model_class_diversity` returns `full` only when at least two succeeded workers have distinct `model_id`s (ensemble.py lines 327-334). `derive_verdict` routes non-`full` `t2_model_class_diversity` to `degraded-model-diversity` before halted/pass (contract.py lines 267-269). I4 creates two successful survivors with duplicate `model_id="stub-model-dup"` and asserts reviewer_count 2, diversity not full, DEGRADED, exit 11, and falsified I1-positive predicate (test lines 210-224); captured phase6-i4 output passed. |
| 6 | M>=2 distinct maps to pass-eligible / exit 0 | PASS | I3 creates N=3 with slot 2 failing and two distinct successful stub models in slots 0 and 1 (test lines 184-190). The contract asserts reviewer_count 2, `t2_model_class_diversity == full`, `tier_reached == 2`, PASS, exit 0 (test lines 192-197). `derive_verdict` reaches PASS only after blocked, degraded, and halted checks are skipped, with `status == success` and `tier_reached == expected_tier` (contract.py lines 211-238). Targeted pytest rerun of I3-I6 passed (`4 passed in 0.16s`). |
| 7 | M is derived from successful workers, not requested N | PASS | Reflect contract counts succeeded normalized workers only (`succeeded = [worker for worker in workers if worker.status == "success"]`, `reviewer_count = len(succeeded)`) in ensemble.py lines 285-286. Swarm reduce also counts `workers_succeeded = sum(1 for w in worker_results if w.status == "success")` and failed as non-success (reduce.py lines 647-649). This matches spec `worker_status_to_m` lines 453-458. |
| 8 | `derive_verdict` ordering blocked → degraded → halted → pass is preserved | PASS | Contract module docstring states exact ordering (contract.py lines 10-13). Implementation performs child/contract/version/malformed BLOCKED checks first (lines 147-210), then `_degraded_reason` (lines 211-225), then `_halted_reason` (lines 227-232), then PASS (lines 234-238). This preserves the requested order. |
| 9 | Process exit uses `Verdict.exit_code` map | PASS | `Verdict.exit_code` maps PASS=0, HALTED=10, DEGRADED=11, BLOCKED=2 (models.py lines 37-48). CLI exits with `result.verdict.exit_code` (commands.py lines 253-269). |
| 10 | I1-positive non-vacuity predicate is a real falsifier, not a tautology | PASS | `_i1_positive_holds` returns false for absent contracts and requires all four independent pass-critical signals: `tier_reached == 2`, `merge_method != single-reviewer-fallback`, `reviewer_count >= 2`, and `t2_model_class_diversity == full` (test lines 101-114). I1 asserts it is true for the positive path (lines 136-147); I2, I4, I5, and I6 assert it is false for negative paths (lines 168-172, 223-224, 249-253, 272-275). This is falsifiable because each negative removes at least one required signal. |
| 11 | Negative tests would expose wrong full-diversity handling where relevant | PASS | I4 is the direct full-diversity falsifier: duplicate survivor model IDs must make diversity not full and verdict degraded (test lines 210-224), so a driver wrongly returning `full` for same-class survivors fails I4. I5 and I6 are not solely diversity-gated, but still falsify the I1-positive set through tier/reviewer-count/contract absence (test lines 249-253 and 272-275); a full-diversity-only bug cannot make them vacuously pass as Tier-2 because `tier_reached != 2`, `reviewer_count < 2`, or contract is absent. |
| 12 | Captured phase6 I3-I6 outputs match live rerun | PASS | Read captured phase6-i3 through phase6-i6 outputs: each targeted test passed. Independently reran `uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py::test_i3_partial_two_of_three_distinct_pass_eligible ... ::test_i6_m_zero_blocked_exit2 -q`; result: `4 passed in 0.16s`. |

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization=false)
- Confidence: Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 19 | Bash: 4 | rg searches via Bash: 2 | pytest reruns via Bash: 1 | Web/Tavily: 0 (not needed; all claims were local-source-bound)

## Issues Found

None.

## Detailed Findings

### M==0

PASS. The code does not emit a top-level reflect contract when no worker succeeds. `derive_verdict` therefore receives `contract is None` with `child_rc == 0` and returns BLOCKED / `contract-missing`; the exit-code map gives 2. This matches the resolved Q6 decision and intentionally differs from the raw `mn_guard_table` slug `ensemble-empty`.

### M==1

PASS. The implementation emits a contract with `tier_reached: 1` and `merge_method: single-reviewer-fallback`. Because degraded trigger 6 (`degraded-tier1`) fires before trigger 10 (`single-reviewer-fallback`), the reason slug can be `degraded-tier1`. This is compliant with the user-provided instruction and spec FR-RH2.9 because the accepted condition is fallback and/or `tier_reached == 1`; the verdict and exit are still DEGRADED / 11.

### M>=2 same-class

PASS. Diversity is computed over succeeded workers' `model_id` values, not N. Same-class survivors produce `t2_model_class_diversity != full`, which `derive_verdict` maps to DEGRADED / `degraded-model-diversity` / exit 11.

### M>=2 distinct

PASS, conditioned on the normal Tier-2 contract also carrying a non-null adversarial convergence score. I3 injects the production scorer seam with a fixed score and proves M=2 distinct survivors reach PASS / exit 0. If the adversarial scorer produces no score, `derive_verdict` would correctly degrade via `null-convergence`; that is a separate Tier-2 completeness failure, not an M,N mapping defect.

## Recommendations

- Keep the Q6 decision record with the tests; it is the reason `contract-missing` is correct for M==0 despite the spec table still naming `ensemble-empty`.
- Keep I4 as the primary non-vacuity guard for diversity-over-M. It is the test that directly fails if the implementation counts requested slots N or blindly returns `full`.
- No code changes recommended for this lens.

## QA Complete
