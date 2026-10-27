# D-0042 -- T05.06: Certify Behavior Alignment

## Summary

`_certified_is_true()` blocks certification on `certified: false`. Manual-fix recovery path works after repeated certification failure. Recovery does not bypass gate checks.

## Verification

### 1. _certified_is_true() blocks on certified: false

Verified in T05.04 (D-0040). `_certified_is_true()` is now a semantic check in `CERTIFY_GATE`, so `certified: false` causes gate failure.

### 2. Manual-fix recovery path

In v2.26, the manual-fix recovery path works as follows:
1. CERTIFY_GATE fails (certified: false)
2. Operator receives `_print_terminal_halt()` output with per-finding details and fix instructions
3. Operator manually fixes findings and updates certification report to `certified: true`
4. Operator runs `superclaude roadmap run <spec> --resume`
5. `_apply_resume()` skips already-passed steps and re-runs from certify step
6. CERTIFY_GATE checks `_certified_is_true()` -- now passes with `certified: true`

The `_apply_resume_after_spec_patch()` function is dormant (retained but not called), confirming spec-patch auto-resume is retired. Manual intervention is required.

### 3. Recovery does not bypass gate checks

The `--resume` path calls `gate_passed()` for each previously-completed step. If a step's gate fails on re-check, the step re-runs. The CERTIFY_GATE semantic check `certified_is_true` is always evaluated -- no bypass path exists.

**Confirmed by:**
- `tests/sprint/test_executor.py::TestSpecPatchRetirement::test_spec_patch_not_called_on_failure` -- spec-patch auto-resume is NOT invoked
- `tests/sprint/test_phase5_negative_validation.py::TestFalseCertification::test_true_certification_passes_certify_gate` -- certified: true passes gate after fix

## Test Run

**Validation command:** `uv run pytest tests/sprint/ -v -k "certif"`

**Result:** 10 passed, 0 failed

## Acceptance Criteria Verification

- [x] `_certified_is_true()` blocks on `certified: false` (verified in T05.04)
- [x] Manual-fix recovery path: fix applied -> resume -> certification succeeds
- [x] Recovery does not bypass gate checks (gate re-evaluated on --resume)
- [x] `uv run pytest tests/sprint/ -v -k "certif"` exits 0
