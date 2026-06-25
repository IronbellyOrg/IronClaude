# QA Report — Phase 6 Non-Mocked Stub Integration Proof

**Topic:** FR-RH2 headless ensemble Phase 6 proof non-vacuity
**Date:** 2026-06-20
**Phase:** phase-6-proof-validation
**Fix cycle:** N/A

---

## Overall Verdict: PASS

Phase 6 now passes. I found and fixed one genuine non-vacuity assertion gap: I6 did not explicitly assert `_i1_positive_holds(contract) is False`. After adding that assertion and refreshing the captured outputs, the I1-I9 suite passes and the wider reflect suite passes.

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 20 | Grep: 0 | Glob: 0 | Bash: 13 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FR-RH2.5 / NFR-RH2.4 real stub fan-out, zero network, no canned ClaudeProcess fixture | PASS | Read `tests/cli/reflect/test_ensemble_stub_integration.py` lines 84-98 and 117-147: `_run` calls `run_tier2_ensemble(... transport_for_slot=..., adversarial_score_fn=_const_score)`, then `parse_contract` and `derive_verdict`; I1 patches `ensemble_mod.ClaudeProcess` to raise on construction and asserts tier/merge/reviewer/diversity/PASS signals. Read `src/superclaude/cli/reflect/ensemble.py` lines 147-191: driver calls real `dispatch_wave1`, `normalize_wave2`, and `reduce_wave3`. Read `src/superclaude/cli/swarm/transports/stub.py` lines 70-149: `StubTransport.send` is deterministic in-process and returns `WorkerResult(status='success', http_code=200)` with no network client. Grep via Bash found no `httpx`/`requests` network reference in the integration test and found the conftest fixture is only named in comments/docstrings, not used as a fixture parameter. |
| 2 | Pass-critical signals are computed, not fixture constants | PASS | Read `ensemble.py` lines 163-191 and 277-334: `reviewer_count` is `len(succeeded)`, `tier_reached` and `merge_method` are derived from `reviewer_count`, and `t2_model_class_diversity` is computed from distinct succeeded `WorkerResult.model_id` values. Read `dispatch.py` lines 444-508: `transport_for_slot(slot_index)` is invoked per worker and real worker results are collected. No code path copies `tests/cli/reflect/fixtures/pass.yaml` or conftest fixture bytes. |
| 3 | Adversarial convergence score seam legitimacy | PASS | Read `ensemble.py` lines 195-207 and 218-246: production path launches `run_adversarial_scorer` via top-level `ClaudeProcess` only when no injected score function is supplied; the test injects only `adversarial_score_fn`, leaving fan-out/reduce/verdict computation real. This is a legitimate credit-free seam for separate adversarial telemetry, not a formation-proof vacuity hole. |
| 4 | NFR-RH2.3 exact non-vacuity / falsifier set | PASS after fix | Read `_i1_positive_holds` at test lines 101-114: exactly `tier_reached==2`, `merge_method!='single-reviewer-fallback'`, `reviewer_count>=2`, `t2_model_class_diversity=='full'`. I2/I4/I5 already asserted the helper false. I6 originally lacked the direct helper assertion; I added lines 274-275 asserting `_i1_positive_holds(contract) is False`. Refreshed `phase6-i6-output.txt` and `phase6-integration-full-output.txt`; both pass. |
| 5 | FR-RH2.9 (M,N) divergence and failing transport semantics | PASS | Read `_FailingTransport` at test lines 43-66: returns `WorkerResult(status='proxy_error', http_code=None, attempts=1)`. Read `dispatch.retry_policy` lines 247-262: `proxy_error` with `http_code=None` buckets as `other` and is not retried. Read `reduce_wave3` lines 647-649: M is `sum(w.status == 'success')`, so proxy errors do not count. Read I3-I6 assertions: I3 M=2 distinct PASS/exit0; I4 M=2 duplicate DEGRADED/exit11; I5 M=1 exit11 single-reviewer fallback; I6 M=0 no contract, BLOCKED/exit2, `contract-missing`. |
| 6 | I7 contract shape, I8 path confinement, I9 done.json DM-017, and test reruns | PASS | Read I7-I9 test bodies and `DoneSentinel` shape at `models.py` lines 1479-1481 plus `emit_done_sentinel` lines 402-459. Re-ran `uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -v`: 9 passed. Re-ran `uv run pytest tests/cli/reflect -q`: 98 passed, 1 xpassed. Ran `uv run ruff check tests/cli/reflect/test_ensemble_stub_integration.py`: all checks passed. Ran `uv run ruff format --check tests/cli/reflect/test_ensemble_stub_integration.py src/superclaude/cli/reflect/ensemble.py`: 2 files already formatted. |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Important issues: 1 fixed before verdict
- Minor issues: 0
- Issues fixed in-place: 1

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `tests/cli/reflect/test_ensemble_stub_integration.py::test_i6_m_zero_blocked_exit2` | I6 proved BLOCKED/exit2/`contract-missing`, but did not explicitly assert the canonical I1-positive helper was false. That left the NFR-RH2.3 assertion set incompletely mirrored across I2/I4/I5/I6. | Add `assert _i1_positive_holds(contract) is False` to I6 and rerun I6 plus the full I1-I9 suite. |

## Actions Taken
- Fixed I6 by adding the missing explicit NFR-RH2.3 falsifier assertion: `assert _i1_positive_holds(contract) is False`.
- Refreshed `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/phase-outputs/test-results/phase6-i6-output.txt`.
- Refreshed `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/phase-outputs/test-results/phase6-integration-full-output.txt`.
- Verified with `uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -v` → 9 passed.
- Verified with `uv run pytest tests/cli/reflect -q` → 98 passed, 1 xpassed.
- Verified lint/format with `uv run ruff check tests/cli/reflect/test_ensemble_stub_integration.py` and `uv run ruff format --check tests/cli/reflect/test_ensemble_stub_integration.py src/superclaude/cli/reflect/ensemble.py`.

## Recommendations
- Proceed: Phase 6 proof is non-mocked and non-vacuity is now explicitly asserted for I2/I4/I5/I6.
- Do not weaken the `ClaudeProcess` hard-fail patch in I1; it is load-bearing evidence that the canned fixture path is not constructing the proof.
- Treat the injected adversarial convergence score as telemetry-only in this test. Future changes must not move formation signals behind that injected constant.

## QA Complete
