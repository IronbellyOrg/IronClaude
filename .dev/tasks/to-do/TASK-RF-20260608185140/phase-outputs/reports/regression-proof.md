# Regression Proof — fail-on-base / pass-on-fix

Each new positive test was run against the base commit `c0d56f18` (pre-fix) and after the fix, proving it catches the reflect-confirmed defect.

| Fix | New positive test | Failed-on-base | Passed-on-fix |
|-----|-------------------|----------------|---------------|
| FIX-1 (DEV-1, Regression HIGH) | `test_primary_argv_includes_index_path_positional` + `test_primary_argv_parses_through_click_command` | ✅ Y — `ImportError` (helper absent) + control test proved base no-positional argv → exit-2 `Missing argument 'INDEX_PATH'` (`fix1-test-fail-on-base.txt`) | ✅ Y — 3 passed (`fix1-test-pass-on-fix.txt`) |
| FIX-2 (DEV-2, Regression MED) | `test_recovered_report_never_injects_gate_tokens` | ✅ Y — rendered report contained `**RESULT**: PASS` via `entry.name` (`fix2-test-fail-on-base.txt`) | ✅ Y — 4 passed (`fix2-test-pass-on-fix.txt`) |
| FIX-3 (DEV-3, Drift MED) | `test_merge_partial_when_declared_not_landed_in_canonical` | ✅ Y — base returned `RecoveryStatus.SUCCESS` (masking) (`fix3-test-fail-on-base.txt`) | ✅ Y — 2 passed (`fix3-test-pass-on-fix.txt`) |
| FIX-4 (test hardening) | 4 checkpoint tests (BLOCKED, body-only, idempotent re-fire, default-off) | n/a — coverage tests (untested paths), pass on fixed code | ✅ Y — 5 passed |

**Overall:** The two MANDATORY new positive tests (FIX-1 PRIMARY integration, FIX-2 injection) plus the FIX-3 strengthened case each FAILED against the base commit and PASS after the fix — proving they catch DEV-1/DEV-2/DEV-3. Full sprint suite: 1172 passed, 0 failed. Ruff: clean + idempotent.
