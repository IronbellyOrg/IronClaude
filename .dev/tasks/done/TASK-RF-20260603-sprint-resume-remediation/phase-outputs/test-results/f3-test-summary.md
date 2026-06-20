# F-3 Test Summary (Phase 2)

**Command:** `uv run pytest "tests/sprint/test_resume.py::TestDriftAssessor" -v`
**Overall:** ✅ PASS — 6 passed in 0.23s (full output: `cg2-green.txt`)

## Per-test results

| Test | AC / Gap | Result | Note |
|------|----------|--------|------|
| `test_inv001_tier0_exact_hash_match` | INV-001 | ✅ PASS | Tier-0 exact match still 1.0/hash |
| `test_drift_trailing_whitespace_high_conf` | **AC-4** | ✅ PASS | ≥0.8, `cosmetic_only is True`. **Proves the Step 2.2 `_build_task_interrupted` co-edit persisted `tasklist_sha256_ws`** — the WS-normalized hash of `_P3` matches the WS-normalized hash of `_P3 + "   \n"`, so the cosmetic branch is kept. Had the co-edit been missed, this would have hit the "WS-missing ⇒ <0.8" fallback and FAILED. |
| `test_drift_material_edit_low_conf` | **AC-5** (ID removal) | ✅ PASS | <0.8, `"T03.01" in explanation`, `cosmetic_only is False`. ID-removal branch unaffected by the fix. |
| `test_drift_same_id_material_body_edit_low_conf` | **CG-2 / F-3** | ✅ PASS (was RED) | <0.8, `cosmetic_only is False`. RED→GREEN: RED captured in `cg2-red.txt` (`assert 0.9 < 0.8` failed); now GREEN because the same-ID deliverable edit's WS hash differs from the recorded `_P3` WS hash. |
| `test_drift_not_yet_run_change_advisory` | advisory | ✅ PASS | ~0.85 not-yet-run branch unaffected. |
| `test_drift_missing_recorded_hash_no_crash` | backward-compat | ✅ PASS | No recorded hash ⇒ `tier != "hash"`, no crash. (Now lands on the conservative <0.8 same-ID branch, but the test asserts only `tier != "hash"` + `explanation`, so non-regressed.) |

## RED→GREEN evidence

- **RED:** `cg2-red.txt` — `test_drift_same_id_material_body_edit_low_conf` FAILED on `assert 0.9 < 0.8` (DriftAssessment confidence=0.9, cosmetic_only=True), the exact F-3 defect.
- **GREEN:** `cg2-green.txt` — same test PASSES; confidence now <0.8 (0.5), cosmetic_only=False.

## Non-regression confirmation

- **AC-4 (`test_drift_trailing_whitespace_high_conf`) PASSES** — the principled WS-hash fix did NOT regress the cosmetic path. This PASS specifically validates the Step 2.2 `_build_task_interrupted` helper co-edit (persisting `tasklist_sha256_ws` of the recorded body). If AC-4 had failed with `confidence < 0.8`, the helper co-edit would have been the culprit (Step 2.2), NOT the test.
- **AC-5 (`test_drift_material_edit_low_conf`) PASSES** — ID-removal path intact.

No fabricated results — all rows reflect the actual pytest output above.
