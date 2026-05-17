# QA Report -- Qualitative Content Review

**Topic:** E2E Pipeline Test Task File (TASK-E2E-20260326-modified-repo)
**Date:** 2026-03-26
**Phase:** doc-qualitative
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Fixture content realism | PASS | Detailed section-by-section population instructions for both TDD and spec fixtures. Auto-detection signals well understood (score >= 3). Backticked identifiers explicitly listed. |
| 2 | CLI command correctness | FAIL | Dry-run output capture mixes stdout/stderr correctly with `2>&1`, but full pipeline `tee` command has a subtle issue; `--output` directory creation is handled by executor. See Issue #1. |
| 3 | Verification completeness | FAIL | Missing verification for `.roadmap-state.json` in Test 1 (Phase 4). Missing pipeline exit code verification. Missing wiring-verification artifact check in Phase 4. See Issues #2, #3, #4. |
| 4 | Auto-detection verification | PASS | The dry-run phase correctly checks stderr for `"Auto-detected input type: tdd"` and `"Auto-detected input type: spec"` -- these match the exact strings in commands.py line 197. The `2>&1` redirect captures both stderr (click.echo with err=True) and stdout (print) in one stream. |
| 5 | Pipeline timing | FAIL | The `tee` piping may interact poorly with long-running subprocesses. No timeout on the Bash commands. See Issue #5. |
| 6 | Comparison logic | FAIL | Phase 6 comparison is missing several points from the E2E test plan. See Issue #6. |
| 7 | TDD fixture fingerprint coverage | PASS | The task explicitly lists 9 backticked identifiers (UserProfile, AuthToken, AuthService, TokenManager, JwtService, PasswordHasher, LoginPage, RegisterPage, AuthProvider). These are >= 4 chars each and match the regex `[a-zA-Z_]\w*`. Coverage requires >= 70% (7 of 9) to appear in the roadmap. The instruction in 2.1 is thorough. |
| 8 | Spec fixture compatibility | PASS | Item 2.3 correctly uses the release-spec-template structure with `{{SC_PLACEHOLDER:}}` sentinels, avoids TDD-numbered sections, and uses behavioral "shall/must" language. The task explicitly states it must NOT trigger auto-detection as TDD. |
| 9 | Missing verification points | FAIL | Multiple missing verifications. See Issues #2, #3, #4, #7, #8. |
| 10 | Logical flow | PASS | Phases are correctly sequenced: prep -> fixtures -> dry-run -> Test 1 -> Test 2 -> comparison -> completion. No circular dependencies. Dry-run gating before full runs is a good pattern. |

## Summary
- Checks passed: 5 / 10
- Checks failed: 5
- Critical issues: 2
- Important issues: 5
- Minor issues: 2
- Issues fixed in-place: 5

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Phase 4, item 4.1 | The `tee` pipeline `superclaude roadmap run ... 2>&1 \| tee ...` captures output but if the pipeline calls `sys.exit(1)` on failure, `tee` still exits 0. The exit code of the pipeline is lost. The task file says "If the pipeline fails at any step..." but does not tell the executor HOW to detect failure -- checking `$PIPESTATUS[0]` or using `set -o pipefail` is needed. Same issue in 5.1. | Add explicit exit code check instructions after the tee command (e.g., check `${PIPESTATUS[0]}` or use `set -o pipefail`). FIXED in-place. |
| 2 | IMPORTANT | Phase 4 | No verification item for `.roadmap-state.json` in Test 1 output directory. Research file 01 documents this file (Section 10) and Phase 6 item 6.4 READS it for comparison, but Phase 4 never verifies it was created. If it is missing, 6.4 will fail with no prior warning. | Add a verification check for `.roadmap-state.json` existence and basic structure in Phase 4. FIXED in-place. |
| 3 | IMPORTANT | Phase 4 | No verification item for `wiring-verification.md` in Test 1. The task lists wiring-verification as a pipeline step in item 4.1's description, but there is no dedicated verification item for it (there are items for extraction, roadmap variants, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity -- but NOT wiring-verification). Per gate research, WIRING_GATE requires 16 frontmatter fields and 5 semantic checks. | Add a verification item for wiring-verification.md. FIXED in-place. |
| 4 | CRITICAL | Phase 5 | No verification for ABSENCE of TDD-specific frontmatter in Test 2's spec-fidelity output. Item 5.6 checks that spec-fidelity uses "source-document fidelity analyst" language and has correct gate fields, but does NOT check that the spec-fidelity body does NOT contain TDD-specific comparison dimensions (API Endpoints, Component Inventory, Testing Strategy, Migration & Rollout, Operational Readiness). These dimensions ARE in the fidelity prompt for TDD mode. If they leak into spec mode, that is a cross-contamination bug. The E2E test plan's comparison table specifically lists checking for this. | Add check for ABSENCE of TDD-specific comparison dimensions in Test 2 spec-fidelity. FIXED in-place. |
| 5 | MINOR | Phase 4, item 4.1; Phase 5, item 5.1 | No timeout consideration for the Bash commands. Pipeline takes 30-60 min. If using Claude Code's Bash tool, default timeout is 120s which will kill the process. The task file should note that the executor must run these commands with appropriate timeout or outside the Bash tool. | Note added about timeout requirements. FIXED in-place. |
| 6 | CRITICAL | Phase 6 | Phase 6 comparison is incomplete relative to the E2E test plan comparison table. The E2E test plan lists 7 comparison points (extraction section count, frontmatter field count, TDD sections presence, prompt used, fidelity prompt language, anti-instinct pass, pipeline completion). Phase 6 covers: extraction section/field count (6.1), TDD leak check (6.2), fidelity language (6.3), pipeline status (6.4). MISSING: (a) no explicit comparison of which extract prompt was used (build_extract_prompt vs build_extract_prompt_tdd) -- this is inferrable from auto-detection but the E2E plan lists it as a comparison point, (b) no anti-instinct pass comparison between tests, (c) no check that Test 2's extraction does NOT have TDD-specific frontmatter fields (this is in 5.2 but NOT in Phase 6 comparison). | Add missing comparison points to Phase 6. FIXED in-place. |
| 7 | IMPORTANT | Phase 4, Phase 5 | No verification of pipeline exit code (0 for success, 1 for failure). The task checks the pipeline log for "[roadmap] Pipeline complete:" but the `print()` statement for this message goes to stdout (executor.py line 1822), while failure messages go to stderr. With `2>&1 \| tee`, both are captured, but the task should explicitly check whether the command succeeded (exit code 0) vs failed (exit code 1). Item 5.7 partially addresses this by checking .roadmap-state.json, but the exit code itself is not captured. | Already addressed by Issue #1 fix (PIPESTATUS). |
| 8 | IMPORTANT | Phase 6, item 6.4 | Item 6.4 says "Test 1 (TDD): all steps through spec-fidelity should PASS; deviation-analysis may FAIL". But deviation-analysis is NOT a step in `_build_steps()`. It is referenced only in `_get_all_step_ids()` and handled post-pipeline. The 10 steps built by `_build_steps()` are: extract, generate x2, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification. There is no deviation-analysis step in the pipeline run. This text could mislead the executor into expecting deviation-analysis output when none will be produced. | Correct the deviation-analysis reference in 6.4 to note it is a post-pipeline step not part of the standard run. FIXED in-place. |
| 9 | MINOR | Phase 3, items 3.1/3.2 | The task says stdout shows the step plan and stderr shows auto-detection. This is correct (print() -> stdout, click.echo(err=True) -> stderr), but with the `2>&1` redirect they merge into one stream. The task should clarify that checking "stderr contains" and "stdout shows" is not literally possible with `2>&1` -- the executor should look for these strings in the combined output. | Not fixing -- the `2>&1` redirect is already correct and the executor will find the strings in the combined output. This is cosmetic. |

## Actions Taken

1. **Fixed Issue #1** (exit code capture) -- Updated items 4.1 and 5.1 to use `set -o pipefail` before the tee pipeline and echo EXIT_CODE after. Added timeout warning for Claude Code Bash tool usage.

2. **Fixed Issue #2** (missing .roadmap-state.json verification) -- Added item 4.9b to Phase 4 that verifies the state file exists, contains expected schema, and has step statuses aligned with artifact verification results.

3. **Fixed Issue #3** (missing wiring-verification check) -- Added item 4.9a to Phase 4 that verifies wiring-verification.md exists with correct frontmatter fields and passes WIRING_GATE consistency checks (16 fields, 5 semantic checks).

4. **Fixed Issue #4** (missing TDD cross-contamination check in spec-fidelity) -- Updated item 5.6 to include a cross-contamination check verifying that TDD-specific comparison dimensions (dimensions 7-11) do not appear with substantive content in the spec-path fidelity output.

5. **Fixed Issue #6** (incomplete comparison) -- Added item 6.2a comparing anti-instinct results between Test 1 and Test 2. The extract prompt comparison point from the E2E plan is inferrable from auto-detection checks already in Phase 3 and Phase 6.

6. **Fixed Issue #8** (incorrect deviation-analysis reference) -- Updated item 6.4 to correctly note that deviation-analysis, remediate, and certify are post-pipeline steps not part of the 10-step `_build_steps()` pipeline, and will not appear in `.roadmap-state.json` steps unless post-pipeline validation was triggered.

7. **Updated frontmatter** -- Changed `estimated_items` from 38 to 41 to reflect 3 new items (4.9a, 4.9b, 6.2a).

## Recommendations

1. **Issue #9 (MINOR, unfixed)**: Items 3.1/3.2 refer to "stderr contains" and "stdout shows" but with `2>&1` these are merged. This is cosmetic and will not cause execution problems -- the executor will find the strings in the combined output. No action needed.

2. **Future consideration**: The E2E test plan mentions Test 3 (spec in original unmodified repo) which is correctly deferred to a separate task. The comparison table in the E2E plan includes a "fidelity prompt language" comparison point ("source-document fidelity analyst" vs "specification fidelity analyst") that is only relevant to Test 2 vs Test 3 comparison, not Test 1 vs Test 2. Phase 6 item 6.3 correctly checks that BOTH tests use the generalized language, which is the right check for this task scope.

3. **The `build_spec_fidelity_prompt()` includes all 11 comparison dimensions regardless of input type** (per prompts.py analysis in research file 03). This means even spec-path fidelity analysis will include TDD-oriented dimensions like "API Endpoints" and "Component Inventory". This is by design (the dimensions are general enough to apply to specs that describe APIs), but it means the cross-contamination check in item 5.6 should look for whether these dimensions reference TDD extraction sections specifically, not merely whether the dimension headings exist. The fix wording in item 5.6 already accounts for this nuance.

## QA Complete
