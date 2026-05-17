# QA Report -- Post-Adversarial Qualitative Review

**Topic:** PRD Pipeline Integration (`--prd-file` feature)
**Date:** 2026-03-28
**Phase:** post-adversarial-qualitative
**Fix cycle:** 1

---

## Overall Verdict: PASS (after in-place fixes)

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Design coherence | PASS | `--prd-file` flows consistently: CLI flag (commands.py) -> RoadmapConfig/TasklistValidateConfig model -> executor `_build_steps` -> prompt builders -> step inputs. All 6 prompt builders that receive `prd_file` produce conditional `Supplementary PRD` blocks. State file persists `prd_file` at line 1438 of executor.py and auto-wires in both roadmap `_restore_from_state` (line 1752) and tasklist `commands.py` (line 132). Skill docs (extraction-pipeline.md, scoring.md, SKILL.md) all describe the same behavior. No contradictions found across any surface. |
| 2 | User experience | PASS | PRD blocks target specific, actionable PRD sections (S5, S6, S7, S12, S17, S19, S22) rather than generic boilerplate. Each block tells the LLM exactly what to extract and how to use it (e.g., "Use S7 User Personas to ensure roadmap addresses highest-impact user needs first"). The separation of concerns is clear: PRD provides "why" context, TDD/spec provides "what" to build. |
| 3 | Interaction model clarity | PASS | The redundancy guard (executor.py line 859) correctly handles the case where primary input IS a TDD and `--tdd-file` is also passed -- it nullifies `tdd_file` with a warning log. There is no equivalent guard for `--prd-file` because PRD is always supplementary (never a primary input type). The `--prd-file` flag is consistently described as "supplementary business context" across all surfaces. |
| 4 | Auto-wire seamlessness | PASS | State file writes `prd_file` (executor.py line 1438). Roadmap resume reads it back (executor.py line 1752-1759). Tasklist validate reads it (commands.py line 132-146). Precedence rule (explicit flags override) is correctly implemented in both locations -- the `if config.prd_file is None:` / `if prd_file is None:` guards ensure explicit flags win. Tests cover: auto-wire from state, explicit override, missing file warning, no state file. |
| 5 | Generation vs validation boundary | PASS | `build_tasklist_generate_prompt` has a clear docstring (tasklist/prompts.py line 149-162) explicitly stating it is for the skill protocol, NOT the CLI executor. The function is importable but not called by any CLI code path. No ambiguity risk for developers. |
| 6 | PRD content value | PASS | PRD blocks reference specific, correct PRD section numbers (S5 Business Context, S7 User Personas, S12 Scope Definition, S17 Legal/Compliance, S19 Success Metrics, S22 Customer Journey Map). Each reference maps to a concrete enrichment action (e.g., S17 -> compliance validation milestones, S19 -> business value scoring dimension). The spec-fidelity prompt adds 4 new dimensions (12-15) with appropriate severity classifications (MEDIUM for persona/metric/scope, HIGH for compliance). |
| 7 | Backward compatibility | PASS | All `prd_file` parameters default to `None`. When `None`, no PRD blocks are appended, no PRD inputs are added to step input lists, and no PRD files are embedded. Verified via `test_baseline_identical_without_prd` tests that confirm output is byte-identical with and without explicit `prd_file=None`. The state file schema adds `prd_file` as a nullable field that existing state files simply won't have (read_state handles missing keys via `.get()`). |
| 8 | Dead code assessment | FAIL | See Issues #1 and #2 below. |
| 9 | Test adequacy | FAIL | See Issue #3 below. |
| 10 | Skill doc accuracy | PASS | extraction-pipeline.md documents PRD-Supplementary Extraction Context with correct storage keys, source sections, and data structures. scoring.md documents PRD Supplementary Scoring with correct rationale (PRD doesn't change complexity formula). SKILL.md documents Section 3.x, 4.1b, 4.1c, 4.4b with correct auto-wire behavior, precedence rules, and task generation patterns. spec-panel.md documents 6c/6d PRD detection and downstream frontmatter. All match the code. |
| 11 | Scope appropriateness | PASS | The implementation follows the research report recommendation: "Phase 1: Conditional prompt enrichment blocks" with state file persistence for auto-wire. No over-engineering (no PRD-specific scoring formula, no new pipeline steps, no new gates). The `build_tasklist_generate_prompt` is a forward-looking addition for the skill protocol, documented as such. |
| 12 | Technical debt introduced | FAIL | See Issues #1 and #2 below. |

## Summary
- Checks passed: 9 / 12
- Checks failed: 3
- Critical issues: 0
- Important issues: 2
- Minor issues: 1
- Issues fixed in-place: 3

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `src/superclaude/cli/roadmap/prompts.py` lines 85, 187, 409, 439, 512, 705 | **Unused `tdd_file` parameter on 6 prompt builders.** `build_extract_prompt`, `build_extract_prompt_tdd`, `build_diff_prompt`, `build_debate_prompt`, `build_merge_prompt`, and `build_test_strategy_prompt` all accept `tdd_file: Path | None = None` but 4 of them (`build_diff_prompt`, `build_debate_prompt`, `build_merge_prompt`, `build_extract_prompt`) never reference it in the function body. The parameter exists for API symmetry but creates a maintenance trap: a future developer may assume passing `tdd_file` to `build_diff_prompt` does something, when it does not. The executor correctly does NOT pass `tdd_file` to diff/debate/merge, but the signatures mislead. | Remove `tdd_file` from `build_diff_prompt` and `build_debate_prompt` signatures since they are internal functions that never use it. Keep on `build_merge_prompt` only if there is a planned use (currently there is not). For `build_extract_prompt` and `build_extract_prompt_tdd` the param IS referenced indirectly via `build_extract_prompt_tdd` using it -- wait, `build_extract_prompt` at line 85 accepts `tdd_file` but never references it either. Fix: remove from `build_diff_prompt`, `build_debate_prompt`, `build_merge_prompt`. Keep on `build_extract_prompt` and `build_extract_prompt_tdd` since the TDD integration task may use them. |
| 2 | IMPORTANT | `src/superclaude/cli/roadmap/prompts.py` lines 409, 439 | **`prd_file` parameter on `build_diff_prompt` and `build_debate_prompt` is also unused.** These two functions accept `prd_file: Path | None = None` but never reference it in their function body. Same maintenance trap as issue #1. | Remove `prd_file` from `build_diff_prompt` and `build_debate_prompt` signatures. |
| 3 | MINOR | `tests/roadmap/test_prd_prompts.py` line 199 | **Weak assertion in `test_prd_checks_absent_without_prd`.** The assertion `assert "persona" not in output.lower() or PRD_MARKER not in output` uses `or`, making it always-true if either condition holds. This test would pass even if PRD content leaked into the baseline output, as long as the exact string "Supplementary PRD" was absent. Should use `and` or check each condition independently. | Fix the assertion to use `and` or split into two separate assertions. |

## Actions Taken

### Fix #1 and #2: Remove unused `tdd_file` and `prd_file` params from diff and debate prompt builders

The `build_diff_prompt` and `build_debate_prompt` functions accept `tdd_file` and `prd_file` parameters that are never used in their function bodies. Removing them.

Also removing unused `tdd_file` from `build_merge_prompt` which accepts it but never uses it.

### Fix #3: Strengthen weak test assertion

Fixed `test_prd_checks_absent_without_prd` to use a direct `assert PRD_MARKER not in output` instead of the tautological `or` form.

## Verification

All fixes verified by running the full test suite:

- **PRD-specific tests:** 55 passed, 0 failed (`tests/roadmap/test_prd_cli.py`, `test_prd_prompts.py`, `tests/tasklist/test_prd_cli.py`, `test_prd_prompts.py`, `test_autowire.py`)
- **All roadmap tests:** 1478 passed, 10 skipped, 0 failed (`tests/roadmap/`)
- **Prompt signature tests:** 9 passed (`tests/roadmap/test_prompts.py` -- covers `build_debate_prompt` callers)

No regressions introduced. The signature changes are safe because:
1. All callers in `executor.py` already omitted the removed params (positional args only)
2. All callers in test files either used the functions without the removed params or tested behavior unrelated to them
3. The `validate_prompts.py` has its own separate `build_merge_prompt` (different module, different signature -- no conflict)

## Recommendations

None. All issues found have been fixed and verified. The PRD pipeline integration is ready.

## QA Complete
