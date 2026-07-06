# FX3 + FX5 full pr_submit-suite summary (Step 2.8)

**Command:** `uv run pytest tests/pr_submit/ -v`
**Run:** 2026-07-03, pytest-9.1.1, Python 3.13.11
**Overall:** 311 passed, 6 failed — all 6 failures PRE-EXISTING and UNRELATED to FX3/FX5.

| Metric | Count |
|--------|-------|
| Collected | 317 |
| Passed | 311 |
| Failed | 6 (pre-existing, see below) |
| FX3 tests (`test_setup_questions_resolution.py`) | 4 / 4 PASSED |
| FX5 differential pairs (`test_gate_helper_differentials.py`) | 22 / 22 PASSED |
| FX5 per-helper coverage (`test_gate_helper_coverage.py`) | 11 / 11 PASSED |
| Existing `test_contract_setup_*` | 80 / 80 PASSED (no regression) |

## FX5 per-helper coverage — every enforced-registry helper green
All 11 registered helpers reported as their own green test id:
`candidate._path_resolves`, `candidate._findings_locus`, `candidate._review_completeness_signal`,
`candidate._selected_identity`, `candidate._selected_app_slug`, `lockgate._paths_resolve`,
`lockgate._emission_shape_observed`, `diagnosis._resolve_optional_path`, `diagnosis._stale_blockers`,
`candidate.CandidateContract.required_unobserved`, `validation._negative_control_checks`.

## The 6 failures are PRE-EXISTING infra gaps, NOT regressions

All 6 failures are in `test_hook_update.py` (4) and `test_static_grep.py` (2). Root cause:
`src/superclaude/hooks/scripts/offer-pr-review.sh` does not exist in this worktree
(`git ls-files` returns nothing → the file is not tracked and is absent at HEAD 46a787da).
The failures are `FileNotFoundError` / exit-127 for that missing shell script.

Evidence these are NOT caused by the FX3/FX5 additions:
- The FX3/FX5 changes are purely additive Python test files + additive conftest code
  (`test_setup_questions_resolution.py`, `test_gate_helper_differentials.py`,
  `test_gate_helper_coverage.py`, appended `conftest.py` collector). None touches hooks.
- No FAILED line references any FX3/FX5/conftest surface.
- All 80 pre-existing `test_contract_setup_*` tests still pass — the conftest additions
  (new `pytest_generate_tests` scoped by test-name + a new fixture + module-level constants)
  regressed nothing.

**Conclusion:** FX3 green, every FX5 per-helper coverage case green, no pre-existing pr_submit
test regressed by the conftest additions. The 6 failures are an out-of-scope environmental gap
(missing untracked hook script) logged in Phase 2 Findings; they are not a mis-authored new test
nor a conftest conflict, so no corrective action applies under Step 2.8.
