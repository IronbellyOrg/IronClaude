# QA Report — Task Qualitative (Step 3.G4 stub-integration actionability lens)

**Topic:** reflect Tier-2 fallback ladder — stub-integration + config tests
**Date:** 2026-07-06
**Phase:** task-qualitative (Step 3.G4 actionability lens)
**Fix cycle:** N/A (report-only, fix_authorization: false)

---

## Overall Verdict: FAIL

The two test files are **largely well-built** — they drive the REAL `run_fallback_ladder`
controller + REAL `build_reflect_contract` + REAL `derive_verdict`, so `reviewer_count`,
`tier_reached`, `terminal_reason`, `merge_method`, and the PASS/DEGRADED verdict are all
genuinely COMPUTED (not fixture-copied), and both files pass (7/7). Verification items 1, 2,
3, and 5 are satisfied at the letter and are concrete.

However, the adversarial pass surfaced **six actionability defects** (2 IMPORTANT, 4 MINOR)
that weaken regression-catching power and make verification items 4 and 6 only partially
true. Per the "any issue regardless of severity = FAIL" rule, verdict is **FAIL** — but note
the severity ceiling is IMPORTANT (no CRITICAL: nothing here produces a false-GREEN verdict
on the happy path, and the core computed assertions are sound).

## Items Reviewed
| # | Check (verification item) | axis | Result | Evidence |
|---|---------------------------|------|--------|----------|
| 1 | Incident replay: contributing set + reviewer_count=2 + tier_reached=2 + PASS/exit0 + certified_with_fallback=true | AX-4 | FAIL | test L120-147: set/count/tier/verdict all present & COMPUTED; but `certified`/preserved sub-claim weak (see I-2). Contributing set order/values pinned exactly (L121). |
| 2 | Counter-case: reviewer_count=1 + tier_reached=1 + degraded-tier1/exit11 + terminal_reason=fallback_pool_exhausted | none | PASS | test L171-193; traced controller: both slots attempted → `all(slot in attempts_made)` True → `fallback_pool_exhausted` (fallback.py L490-493); `_degraded_reason` Trigger 6 fires first (contract.py L271) → `degraded-tier1`. Correct & concrete. |
| 3 | F2: stable non-empty `final_path` on fallback worker | AX-4 | FAIL | test L124-126: `_raw_fallback` omits final_path (L36) → `_stamp` fills it → proves stamp-before-normalize order & survival; but uses bespoke stub stamp, not prod `_stamp_worker_paths` (see I-4). |
| 4 | Force fallback ON for stub lane; network-free | AX-3 | FAIL | Network-free: YES (`_trivial_factory`→`object()`, injected dispatch/normalize/stamp, no ClaudeProcess/StubTransport). "Force ON": the `tier2_fallback_enabled=True` flip is INERT (see I-1). |
| 5 | Config test: stub-OFF + explicit-OFF + ladder/max defaults | none | PASS | test_fallback_config.py L25-55: 5 tests map 1:1 to config.py L334 (`and resolved_transport != "stub"`) + ReflectConfig defaults (models.py L115-117). Concrete. |
| 6 | Tests concrete (fail on real regression), not tautological/aspirational | AX-4 | FAIL | Most assertions COMPUTED & concrete; two are weakened (`primary_failures_preserved` truthy-only I-2; inert enable-flag I-1). |

## Summary
- Checks passed: 2 / 6 (items 2, 5 clean; items 1, 3, 4, 6 carry defects)
- Checks failed: 4
- Critical issues: 0
- Important issues: 2
- Minor issues: 4
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | IMPORTANT | test_ensemble_fallback_stub.py L99-100 (`_config`) + L107/L154 | The `dataclasses.replace(config, tier2_fallback_enabled=True)` "force ON" flip is a **no-op for the code path under test**. `run_fallback_ladder` never reads `tier2_fallback_enabled` (grep: NONE in fallback.py); the enable-gate lives in `run_tier2_ensemble` (ensemble.py L296), which neither test file calls. So the stub-integration suite does NOT verify that enabling fallback engages the ladder, nor that disabling skips it. The comment ("Stub defaults fallback OFF; force ON for this stub-lane replay") claims protection the test does not provide → false confidence for verification item 4. | Either (a) add one integration test that calls `run_tier2_ensemble(config, transport_for_slot=…, env=…)` with `transport=stub` and asserts the ladder engages when `tier2_fallback_enabled=True` and is byte-skipped (t2_fallback=None) when False; or (b) drop/soften the "force ON" comment and document that `run_fallback_ladder` is unconditional and the enable-gate is covered only at config-resolution level (test_fallback_config.py). |
| I-2 | IMPORTANT | test_ensemble_fallback_stub.py L131 | `assert outcome.metadata["primary_failures_preserved"]` is a **truthy-only** check. It passes for ANY non-empty list — a regression that preserved the wrong ids, or only one of the two failures, would still pass. Verification item 1's "primary failures preserved" is therefore not concretely pinned (AX-4 weakened criterion; §8 expects the exact set). | Assert exact contents: `== ["primary:01", "primary:02"]` (the eligible-failure ids for this fixture: index1 qwen proxy_error, index2 gpt parse_error → `_primary_attempt_id`). |
| I-3 | MINOR | test_ensemble_fallback_stub.py L82-88 vs design §8 (L638-655) | The test claims to "replay the §8 incident" (docstring L1, function name `test_incident_replay_…`) but the primary index arrangement diverges: §8 puts the surviving primary at index 1 (`T2Model02`) with failures at `[primary:00, primary:02]`; the test puts the survivor at index 0 with failures at `[primary:01, primary:02]`. Because I-2 only truthy-checks the preserved set, the divergence is invisible. The semantic shape (1 survivor + 2 eligible failures) is preserved, but the "faithful replay" claim is loose. | Align `_incident_primaries` index arrangement with §8 (survivor at index 1), OR soften the "replay the §8 incident" wording to "reproduce the §8 incident *shape*". Combined with I-2's exact-id assert this becomes self-documenting. |
| I-4 | MINOR | test_ensemble_fallback_stub.py L56-70 (`_stamp`) | The injected `_stamp` stub is a **different implementation** than production `_stamp_worker_paths` (ensemble.py L734: uses `_slugify_model` + `{REFLECT_REVIEW_LENS}-{index:02d}-{slug}`; the stub uses `fallback-{i:02d}`). The F2 test proves the controller calls stamp BEFORE normalize and returns the stamped worker, but does NOT exercise the real stamp through the ladder. No test in these two files runs prod `_stamp_worker_paths` via `run_fallback_ladder`. | Acknowledge as a scoped coverage gap (the ensemble wires the real `stamp=_stamp_worker_paths`, ensemble.py L308). Add a note or one integration case exercising the real stamp so F2's "stable final_path" is proven against production path-stamping, not just a stub. |
| I-5 | MINOR | test_ensemble_fallback_stub.py L110 | The test uses `_trivial_factory` and never exercises the real credit-free stub factory `resolve_t1_fallback_factory(transport="stub")` (ensemble.py L204-213) nor the `_T1_PROXY_BINDING` needs_human_decision gate (L215-224) that folds `openai_compat` into `fallback_config_missing`. So the real stub fallback resolution and the config-missing degrade path are untested at integration level. | Add a small test binding `transport_for_fallback_slot=resolve_t1_fallback_factory("stub", ladder=…)` to prove the real stub factory certifies, and one asserting the `openai_compat` gated factory raises `TransportEnvError` → `terminal_reason=fallback_config_missing`. |
| I-6 | MINOR | test_ensemble_fallback_stub.py L128-131 | The incident case never asserts `engaged is True` or `fallback_attempt_count == 1`, and never asserts `exhausted is False` (the counter-case does assert `exhausted is True`). The metadata carries all three; asymmetric coverage lets a regression that mis-counts attempts pass. | Add `assert outcome.metadata["engaged"] is True`, `assert outcome.metadata["fallback_attempt_count"] == 1`, `assert outcome.metadata["exhausted"] is False`. |

## Actions Taken
None — report-only (`fix_authorization: false`). All findings documented above for the
Step 3.G4 orchestrator.

## What Was Verified As CORRECT (non-inflation evidence)
- Verdicts are genuinely COMPUTED: traced `derive_verdict` for both cases against
  `contract.py` L256-351. Incident: tier_reached=2, mcd=full (deepseek+gemini distinct),
  vendor=multi (deepseek vs google), convergence 0.86 ≥ 0.80, `verification_skip_reason ==
  "no-verification-stage"` (exempt) → `_degraded_reason` returns None → **PASS/exit 0**.
  Counter-case: expected_tier 2 & tier_reached 1 → Trigger 6 `degraded-tier1` fires BEFORE
  Trigger 10 `single-reviewer-fallback` → **exit 11**, reason exactly `degraded-tier1`. Both
  test assertions match the real first-match chain.
- `terminal_reason == "fallback_pool_exhausted"` (not `fallback_attempts_failed`) is the
  CORRECT disambiguation for the default 2/2 ladder both-fail case (design §6 L458-466);
  traced controller L435-496 to confirm `all(slot in attempts_made for slot in ladder)` → True.
- Network-free confirmed: no `ClaudeProcess`, no real `Transport`, no `StubTransport` in the
  execution path; `_trivial_factory` returns `object()` and all I/O seams are injected stubs.
- Config tests map 1:1 to `config.py` L334 and `ReflectConfig` defaults; both files run green
  (`uv run pytest … -q` → 7 passed in 0.16s).

## Confidence Gate
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 2 | Glob: 0 | Bash: 3
- All 6 verification items checked against source (fallback.py, ensemble.py, contract.py,
  config.py, models.py, _diversity.py, conftest.py) + live pytest run. Tool-call count (14) ≥
  checklist items (6) — not suspect.
- No web research performed (all verification local-file-bound). Tavily not required.

## Recommendations
1. **Must-fix before this test surface is treated as regression-grade:** I-1 (inert enable
   flag → add ensemble-level engage/skip test) and I-2 (exact-id assert on
   `primary_failures_preserved`). These two remove the only false-confidence gaps.
2. **Should-fix:** I-3 (align incident indices with §8 or soften the "replay" claim), I-6
   (symmetric metadata asserts on the incident case).
3. **Nice-to-have:** I-4 + I-5 (integration coverage of the real `_stamp_worker_paths` and
   the real `resolve_t1_fallback_factory` stub/gated arms) — arguably belong to a separate
   ensemble-level test file rather than these two.

## QA Complete
