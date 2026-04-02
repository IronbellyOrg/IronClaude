# QA Report -- Final Structural Pass (Pass 3)

**Topic:** PRD Pipeline Integration
**Date:** 2026-03-28
**Phase:** final-structural-pass
**Fix cycle:** 3

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | build_extract_prompt signature vs call sites | PASS | Sig: (spec_file, retrospective_content=None, tdd_file=None, prd_file=None). Executor L904-908 uses kwargs. Tests L46-64 use kwargs. All match. |
| 2 | build_extract_prompt_tdd signature vs call sites | PASS | Sig: (spec_file, retrospective_content=None, tdd_file=None, prd_file=None). Executor L897-901 uses kwargs. Tests L74-83 use kwargs. All match. |
| 3 | build_generate_prompt signature vs call sites | PASS | Sig: (agent, extraction_path, tdd_file=None, prd_file=None). Executor L921, L931 pass 2 positional + kwargs. Tests L92-101 pass 2 positional + kwargs. All match. |
| 4 | build_diff_prompt P3 cleanup | PASS | Sig: (variant_a_path, variant_b_path) -- 2 positional only. No tdd/prd params. Executor L943 passes 2 args. No test calls. Clean. |
| 5 | build_debate_prompt P3 cleanup | PASS | Sig: (diff_path, variant_a_path, variant_b_path, depth) -- 4 positional only. No tdd/prd params. Executor L953 passes 4 args. No test calls. Clean. |
| 6 | build_score_prompt signature vs call sites | PASS | Sig: (debate_path, variant_a_path, variant_b_path, tdd_file=None, prd_file=None). Executor L963 passes 3 positional + kwargs. Tests L111, L115 pass 3 positional + optional kwargs. All match. |
| 7 | build_merge_prompt P3 cleanup | PASS | Sig: (base_selection_path, variant_a_path, variant_b_path, debate_path) -- 4 positional only. No tdd/prd params. Executor L973 passes 4 args. No test calls. Clean. |
| 8 | build_spec_fidelity_prompt signature vs call sites | PASS | Sig: (spec_file, roadmap_path, tdd_file=None, prd_file=None). Executor L1003 passes 2 positional + kwargs. Tests L125-188 pass 2 positional + optional kwargs. All match. |
| 9 | build_wiring_verification_prompt signature vs call sites | PASS | Sig: (merge_file, spec_source) -- 2 positional. Executor L1013-1014 passes (merge_file, config.spec_file.name). Match. |
| 10 | build_test_strategy_prompt signature vs call sites | PASS | Sig: (roadmap_path, extraction_path, tdd_file=None, prd_file=None). Executor L993 passes 2 positional + kwargs. Tests L140-208 pass 2 positional + optional kwargs. All match. |
| 11 | build_tasklist_fidelity_prompt signature vs call sites | PASS | Sig: (roadmap_file, tasklist_dir, tdd_file=None, prd_file=None). Executor (tasklist) L202-206 passes 2 positional + kwargs. Tests L36-63 pass 2 positional + optional kwargs. All match. |
| 12 | build_tasklist_generate_prompt signature vs call sites | PASS | Sig: (roadmap_file, tdd_file=None, prd_file=None). Not called from executor (used by skill protocol only). Tests L72-105 pass 1 positional + optional kwargs. All match. |
| 13 | P3 stub cleanup -- no dead params in diff/debate/merge | PASS | build_diff_prompt: no tdd/prd params in sig. build_debate_prompt: no tdd/prd params in sig. build_merge_prompt: no tdd/prd params in sig. Executor passes no tdd/prd to any of them. No tests pass tdd/prd to them. Clean. |
| 14 | Auto-wire code path | PASS | tasklist/commands.py L113-146: read_state imported from ..roadmap.executor. State file path = resolved_output / ".roadmap-state.json". Both tdd_file (L117-131) and prd_file (L132-146) auto-wire blocks present. Precedence correct: only fills when CLI flag is None. Missing file warnings at L129-131 and L143-145. |
| 15 | State file write includes tdd_file and prd_file | PASS | executor.py L1437: "tdd_file": str(config.tdd_file) if config.tdd_file else None. L1438: "prd_file": str(config.prd_file) if config.prd_file else None. Both stored. |
| 16 | Redundancy guard uses effective_input_type | PASS | executor.py L853-864: effective_input_type resolves "auto" via detect_input_type() at L854-856 BEFORE the guard at L859. Guard condition: `effective_input_type == "tdd"`. Correct -- fires after auto-detection. |
| 17 | Test assertion: tautological "Compliance" check | FAIL | tests/roadmap/test_prd_prompts.py L127: `assert "Compliance" not in output or "Compliance/Legal Coverage" not in output`. The actual prompt text at prompts.py L629 is "Compliance & Legal Coverage" (ampersand), NOT "Compliance/Legal Coverage" (slash). The second branch checks for a string that never exists in any output, making the `or` tautologically true. This assertion can never fail regardless of output content. |
| 18 | Test assertion: weak `or` patterns in spec fidelity tests | PASS | L131: `assert PRD_MARKER in output or "Persona Coverage" in output` -- functionally correct because PRD_MARKER is always present when PRD block is injected. Weak but not broken. L189: same pattern, also functionally correct. |
| 19 | Redundancy guard test assertions | PASS | Tests L226-254: test_redundancy_guard_logic correctly simulates the guard and asserts tdd_file is None. test_no_guard_when_spec_input correctly asserts tdd_file is preserved. Both test the right variable. |
| 20 | Tasklist test assertions | PASS | All assertions in tests/tasklist/test_prd_prompts.py use exact markers (PRD_MARKER, TDD_MARKER) with `in`/`not in` checks. Ordering assertion at L62-63 uses correct index comparison. No tautological patterns. |

## Summary
- Checks passed: 19 / 20 (pre-fix) -> 20 / 20 (post-fix)
- Checks failed: 1 -> 0 (fixed in-place)
- Critical issues: 0
- Issues fixed in-place: 1

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | tests/roadmap/test_prd_prompts.py:127 | Tautological assertion: checks for `"Compliance/Legal Coverage"` (slash) but the actual prompt text uses `"Compliance & Legal Coverage"` (ampersand). The second branch of the `or` is always True because the slash variant never appears in any output, making the entire assertion vacuously true -- it can never fail even if the PRD block is incorrectly injected. | Replace with `assert "Compliance & Legal Coverage" not in output`. |

## Actions Taken
- Fixed L127 in tests/roadmap/test_prd_prompts.py: replaced `assert "Compliance" not in output or "Compliance/Legal Coverage" not in output` with `assert "Compliance & Legal Coverage" not in output`. This directly checks for the exact string from the PRD block in prompts.py L629.
- Verified fix by running all 46 PRD pipeline tests: 46 passed in 0.09s.

## Recommendations
- No blocking issues remain. All 20 structural checks pass after the fix.
- The fix was MINOR severity (wrong separator character in test string), not a logic error in production code. All production code paths (prompts.py, executor.py, commands.py) verified clean across all 3 passes.

## QA Complete