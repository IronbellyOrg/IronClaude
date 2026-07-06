# QA Report — task-qualitative (Phase 4, no-side-effect test-strength lens)

**Topic:** Locked Detection Contract Setup Flow — Phase 4 no-side-effect test strength
**Date:** 2026-07-02
**Phase:** task-qualitative (QA_MODE: task-integrity / synthesis-gate-equivalent)
**Lens:** no-side-effect-test-strength
**Fix cycle:** N/A (fix_authorization: false — report only)

---

## VERDICT: PASS

Every no-side-effect boundary named in the checklist is **exercised** by at least one
binding test verified against real production source. One MINOR test-strength weakness
was found (a vacuous recorder loop in integration test 5) but it does **not** leave any
boundary unexercised — the same boundary is redundantly and bindingly covered by a
static import audit and by the arithmetic in tests 1/3/4. Per the stated PASS/FAIL rule
("FAIL on any *unexercised* no-side-effect boundary"), no boundary is unexercised.

---

## Adversarial stance applied

Assumed a setup/readiness/write path silently arms or mutates and the tests fail to
catch it. I hunted specifically for: (a) recorder assertions that are tautologically
true because the recorder is never wired, (b) a fail-closed gate that is stubbed rather
than really raised, (c) a `contract-status`/diagnose/write path that could reach an FSM
seam or a lock write, (d) a discriminating baseline missing (arm==0 asserted but the
recorder never proven capable of reaching 1). All four were probed against real source.

---

## Boundary → test-name matrix

| # | No-side-effect boundary | Bound by test(s) | Source-verified? | Strength |
|---|--------------------------|-------------------|------------------|----------|
| 1a | Six real FSM seams (`arm_monitor`, `do_push`, `do_reply`, `do_resolve`, `do_retrigger`, `invoke_auggie_review`) never invoked by the **writer** path | `test_writer_package_imports_no_fsm_seams`, `test_confirmed_write_performs_no_pr_side_effects` | YES — `RunConfig` fields fsm.py:747-760; static graph import audit + `arm_monitor` tripwire | STRONG |
| 1b | Same seams never invoked by **diagnose/render** path | `test_diagnose_and_render_perform_no_side_effects` (structural) + grep audit | YES — `diagnosis.py` has ZERO refs to `run_skill`/`arm_monitor`/`RunConfig`/`fsm` (grep exit=1) | STRONG structurally; recorder loop VACUOUS (see F-1) |
| 2 | Monitor arm count == 0 on missing-contract halt (`for_arming()` raises before arm) | `test_missing_contract_for_arming_halts_before_monitor_arm`, `test_unlocked_local_override_for_arming_halts` | YES — `run_skill` calls `config.arm_monitor(...)` at fsm.py:919, strictly downstream of the `for_arming()` raise; `for_arming→load(require_locked)→raise DetectionContractLocked` detection.py:172-199 | STRONG |
| 3 | `--monitor 0` never arms / stays `S0_IDLE` | `test_monitor_zero_never_arms_and_stays_idle` | YES — `gate_arm(0)==False` fsm.py:128-130; `run_skill` L0 early-return fsm.py:916-918; baseline arm==1 proven by `test_post_lock_for_arming_returns_locked_contract` | STRONG (discriminating baseline present) |
| 4 | Fail-closed gate is real, not stubbed (the `DetectionContractLocked` raise + the LockGate) | `test_missing_contract_for_arming_halts_before_monitor_arm` (raise), all `test_contract_setup_writer.py` gate tests | YES — raise is production code detection.py:172-189; `LockGate.evaluate` runs 12 real predicates incl. `_user_confirmed` lockgate.py:64/182-184; no test monkeypatches the raise or the gate | STRONG |
| 5 | `contract-status` does NOT launch `ReflectRunner`/`resolve_config`/`ClaudeProcess`, and writes no lock by default (even `--validate`) | `test_contract_status_does_not_launch_reflect_audit_machinery`, `test_contract_status_validate_does_not_write_lock_by_default`, `test_contract_status_output_is_metadata_only` | YES — `contract_status` imports only `diagnose/derive_candidate/load_evidence/validate_candidate/write_report` (commands.py:99-106), never `write_lock`; audit machinery lazily imported only inside `reflect run()` commands.py:345-346; `--validate` branch calls `write_report` (probes-only), never `write_lock` (commands.py:113-134) | STRONG |

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Six real seams asserted zero across setup/readiness/write | none | PASS | Six seams confirmed as real `RunConfig` fields (fsm.py:747-760). Writer path covered by static import audit + `arm_monitor` tripwire; diagnose/render path covered structurally (grep exit=1) + test-1 recorder. Boundary exercised. (MINOR strength note F-1 on the inert recorder loop in test 5.) |
| 2 | Arm count zero on missing-contract halt (`for_arming` raises pre-arm) | none | PASS | `run_skill` arms at fsm.py:919 (downstream of the raise); integration tests place `run_skill(...)` after `for_arming()` inside `pytest.raises`, and independently assert `arm_recorder.calls == 0`. Real raise, real seam, real ordering. |
| 3 | `--monitor 0` unaffected / stays S0_IDLE, never arms | none | PASS | `gate_arm(0)==False` (fsm.py:128-130) and `run_skill` early-returns at L0 (fsm.py:916-918). Recorder is discriminating: same `_Recorder` reaches `calls==1` when armed at L1 post-lock. |
| 4 | Fail-closed gate not mocked away (DetectionContractLocked raise is real) | none | PASS | Raise is production code (detection.py:172-189); the 12-predicate LockGate incl. `_user_confirmed` is real (lockgate.py). No test stubs the raise or the gate. |
| 5 | reflect contract-status does not launch ReflectRunner/ClaudeProcess and writes no lock by default | none | PASS | Command imports only contract_setup readiness helpers + `write_report` (never `write_lock`); audit machinery lazily imported only in `reflect run()`; `--validate` no-evidence path emits "validation skipped" and creates no lock file (test asserts `not lock_exists`). |

---

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Boundaries unexercised: 0  (**verdict-determining metric — all covered**)
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (test-strength; non-blocking under the stated PASS/FAIL rule)
- Assigned test suite: **81 passed in 0.30s** (all seven assigned test files run against real source)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F-1 | MINOR | `tests/pr_submit/test_contract_setup_pr_submit_integration.py:200-219` (`test_diagnose_and_render_perform_no_side_effects`) | The six recorders (`arm_rec`..`auggie_rec`) are constructed but **never wired** into any `RunConfig` or passed to `diagnose`/`render` (which take no seam args). The loop `for rec in (...): assert rec.calls == 0` is therefore **tautologically true** — it would pass even if diagnose/render *did* arm, because these particular recorder objects are inert locals. The intended boundary (diagnose/render invoke no seam) is nonetheless genuinely covered by the static import audit in `test_writer_package_imports_no_fsm_seams` and by `diagnosis.py` having zero FSM references — so the boundary is NOT unexercised, only this specific assertion is weak/decorative. | Either (a) delete the six-recorder loop and rely on the (real) `next_command`/`Next safe step:` string assertions + the static import audit, or (b) make the assertion binding by giving `diagnosis`/`render` an injectable-seam surface and threading the recorders through it. As-is it risks giving false confidence in future refactors. Not authorized to fix (report-only). |

Note: no CRITICAL/IMPORTANT issues. The lens's core worry — a silently-arming or silently-mutating setup/readiness path — is refuted: diagnose/render are structurally seam-free (grep), the writer package is statically FSM-free with a live tripwire, and the CLI never imports `write_lock`.

## Actions Taken

None. `fix_authorization: false` — report only. No files modified.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt, so there
  were no machine-verified PASS items to rely on. I performed full independent structural
  + semantic verification (fallback / standalone behavior per Critical Rule #11).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Verified the six FSM seams named in the checklist note are the *real* injected seams — read `RunConfig` (fsm.py:747-760); confirmed `arm_monitor`/`do_push`/`do_reply`/`do_resolve`/`do_retrigger`/`invoke_auggie_review` exist and `run_skill` invokes them (fsm.py:919, 1008-1023).
- Verified the fail-closed raise is real, not stubbed — read `for_arming`/`load`/`DetectionContractLocked` (detection.py:71-199); confirmed `arm_monitor` is called strictly downstream (fsm.py:919) so the "arm==0" assertion binds.
- Verified `--monitor 0` has a *discriminating* baseline — read `gate_arm` (fsm.py:128-130) and confirmed the same recorder reaches 1 when armed (integration test line 183) so `calls==0` is not vacuous.
- Verified the CLI does not reach audit machinery or a lock write — read `contract_status` (commands.py:95-142); confirmed it imports `write_report` not `write_lock`, and `ReflectRunner`/`resolve_config`/`ClaudeProcess` are imported only inside `reflect run()` (commands.py:345-346).
- Verified the LockGate is 12 real predicates incl. `_user_confirmed` (lockgate.py:64, 182-184) — the writer tests exercise the real gate, not a mock.
- Adversarial discovery: found the inert-recorder weakness (F-1) by grepping whether the six recorders in integration test 5 are ever wired (they are not).
- Ran the assigned suite: 81 passed, confirming every seam/gate binds against current source.

---

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 6 | Glob: 0 | Bash: 9 (incl. the 81-test run)
- Every checklist item was verified with tool evidence citing specific `file:line`.
- No web research was performed (all verification was local-file / source-bound), so no
  Tavily-vs-fallback record is applicable.

---

## Recommendations

1. (MINOR, non-blocking) Address F-1 before this test is relied on as the guarantor of the
   diagnose/render no-seam boundary — today that guarantee actually rests on the static
   import audit and the grep-verified absence of FSM references in `diagnosis.py`, not on
   test 5's recorder loop. Tighten or remove the decorative loop.
2. Proceed — the fail-closed arm gate, the `--monitor 0` opt-out, the writer LockGate, and
   the reflect `contract-status` diagnose-only surface are all genuinely, bindingly tested.

## QA Complete
