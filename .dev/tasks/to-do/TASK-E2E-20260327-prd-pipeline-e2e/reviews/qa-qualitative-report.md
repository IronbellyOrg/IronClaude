# QA Report -- Qualitative Review (E2E PRD Pipeline Test Task)

**Topic:** E2E Pipeline Tests -- PRD Enrichment with TDD and Spec Paths
**Date:** 2026-03-28
**Phase:** doc-qualitative (MDTM Task File)
**Fix cycle:** 1
**Fix authorization:** YES

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | CLI command correctness | PASS | All `uv run superclaude roadmap run` and `uv run superclaude tasklist validate` commands use correct syntax. `--prd-file` and `--tdd-file` flags match actual Click option names in `commands.py`. Output directories (`test1-tdd-prd/`, `test2-spec-prd/`) are correct and distinct from prior results. No bare `superclaude` usage found. |
| 2 | PRD fixture realism | PASS | Item 2.1 specifies 3 named personas (Alex, Jordan, Sam), JTBD in proper format, 5 metrics with targets, customer journeys, compliance requirements (GDPR, SOC2), and explicit language rules ("Users can log in" not "AuthService authenticates"). The fixture spec is detailed enough to produce a PRD that triggers PRD supplementary blocks. |
| 3 | Implementation coverage -- prompt builder count accuracy | FAIL | Task line 73 claims "All 9 builders now accept `tdd_file` and `prd_file` params; 6 builders have PRD supplementary blocks." Actual count: 10 builders in roadmap/prompts.py, 6 have PRD blocks, 4 do not (diff, debate, merge, wiring_verification). Plus 2 in tasklist/prompts.py with PRD blocks = 8 total with PRD. The "9" count is wrong and "6" undercounts the total. |
| 4 | Implementation coverage -- build_tasklist_generate_prompt tested | PASS | Item 7.5 directly tests the function with all 4 scenarios (none, TDD-only, PRD-only, both). However, the test code has a critical bug (see check #6). |
| 5 | Implementation coverage -- auto-wire scenarios | PASS | Phase 6 covers: happy path (6.1), explicit flag precedence (6.3), missing file on disk (6.4), no state file (6.5). All four auto-wire scenarios from the integration report are covered. |
| 6 | Implementation coverage -- item 7.5 Python one-liner correctness | FAIL | CRITICAL BUG. `build_tasklist_generate_prompt` signature is `(roadmap_file, tdd_file=None, prd_file=None)`. Item 7.5 calls `build_tasklist_generate_prompt(p, p)` which binds `roadmap_file=p, tdd_file=p` -- NOT "no supplements." Then `build_tasklist_generate_prompt(p, p, tdd_file=p)` would raise `TypeError: got multiple values for argument 'tdd_file'` because `p` is already bound positionally as `tdd_file`. This item would crash at runtime. |
| 7 | Implementation coverage -- redundancy guard | PASS | Item 3.4 tests the redundancy guard and accounts for the known stderr display bug. The expected warning text matches the actual string in executor.py: "Ignoring --tdd-file: primary input is already a TDD document." |
| 8 | Implementation coverage -- state file fields | PASS | Item 4.9b checks for `tdd_file`, `prd_file`, and `input_type` in the state file. Item 5.7 does the same for the spec+PRD run. |
| 9 | Implementation coverage -- fidelity dimensions 12-15 | PASS | Items 4.9 and 5.6 both check for "Persona Coverage", "Business Metric Traceability", "Compliance/Legal", and "Scope Boundary" in spec-fidelity output. |
| 10 | Implementation coverage -- make verify-sync | PASS | Item 1.5 explicitly verifies skill layer sync with `make verify-sync`. |
| 11 | Implementation coverage -- build_score_prompt PRD enrichment | FAIL | The integration report lists `build_score_prompt` as PRD-enriched (3 dimensions: business value, persona, compliance). Item 4.5c checks `base-selection.md` but ONLY for existence, line count, and frontmatter fields (`base_variant`, `variant_scores`). It does NOT check for PRD enrichment content in the scoring output. |
| 12 | Artifact verification -- Phase 4 completeness | PASS | Phase 4 checks all 12 artifact types: extraction (4.2, 4.3), roadmap variants (4.4), diff-analysis (4.5a), debate-transcript (4.5b), base-selection (4.5c), merged roadmap (4.6), anti-instinct (4.7), test-strategy (4.8), spec-fidelity (4.9), wiring-verification (4.9a), state file (4.9b). Matches the prior E2E artifact list. |
| 13 | Artifact verification -- Phase 5 completeness | FAIL | Phase 5 is MISSING verification of: roadmap variants, diff-analysis, debate-transcript, base-selection, wiring-verification, and test-strategy. These 6 intermediate artifacts are produced by the spec+PRD pipeline run but are not checked. Phase 4 checks all 12 artifact types; Phase 5 checks only 6. |
| 14 | Cross-run comparison logic | PASS | Phase 8 specifies concrete comparison dimensions: frontmatter field counts, body section counts, PRD-specific term presence (personas, metrics, compliance), and TDD cross-contamination checks. Comparison points are specific enough to produce meaningful delta analysis. |
| 15 | Known issues -- anti-instinct halt handling | PASS | Items 4.7, 4.8, 4.9, 5.5, 5.6 all account for the anti-instinct halt. Test-strategy and spec-fidelity items include "If the file does not exist (expected if anti-instinct halted), note 'SKIPPED' and do not treat as failure." |
| 16 | Phase-gate QA instructions | PASS | Each phase (2+) has a purpose block and summary item. Phase summaries (4.10, 5.9, 6.6, 7.6, 8.5, 9.4) compile pass/fail tables and document findings. Every verification item specifies logging failures to the Phase Findings section. |
| 17 | Logging and follow-up | PASS | Every item includes "Log in the Phase N Findings section of the Task Log at the bottom of this task file." Phase 10 item 10.3 consolidates all findings into follow-up action items. |
| 18 | Phase 7 header item count | FAIL | Phase 7 header says "(5 items)" but contains 6 items (7.1, 7.2, 7.3, 7.4, 7.5, 7.6). The count is wrong. |
| 19 | Timing and feasibility | PASS | Pipeline runs specify 3600000ms timeouts. Task overview notes 30-60 min per run. Items 4.1 and 5.1 include `set -o pipefail` and `tee` for log capture. No `run_in_background` is used, which is fine since the executor needs to check results sequentially. |
| 20 | Prerequisites -- tasklist validate --tdd-file | FAIL | Item 1.3 checks `tasklist validate --help` for `--prd-file` but does NOT verify `--tdd-file`. However, item 7.1 uses `--tdd-file` on `tasklist validate`. If `--tdd-file` is missing (somehow not implemented), Phase 7 would fail with no prior validation. The prerequisite check should cover ALL flags used in later phases. |
| 21 | Internal consistency -- prompt builder claim vs reality | FAIL | Line 73 states "All 9 builders now accept `tdd_file` and `prd_file` params" but 4 roadmap builders (diff, debate, merge, wiring_verification) do NOT accept these params. This misinformation in the Pipeline Code section could lead an executor to expect PRD enrichment in artifacts produced by those builders (diff-analysis, debate-transcript, merged roadmap via merge, wiring-verification). |

## Summary

- Checks passed: 14 / 21
- Checks failed: 7
- Critical issues: 1
- Important issues: 5
- Minor issues: 1
- Issues fixed in-place: 7 (see Actions Taken)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Item 7.5 | Python one-liner has wrong function call signatures. `build_tasklist_generate_prompt(p, p)` passes `p` as `tdd_file` (not "no supplements"). `build_tasklist_generate_prompt(p, p, tdd_file=p)` raises TypeError (duplicate keyword arg). | Fix the one-liner: `r_none = build_tasklist_generate_prompt(p)`, `r_tdd = build_tasklist_generate_prompt(p, tdd_file=p)`, `r_prd = build_tasklist_generate_prompt(p, prd_file=p)`, `r_both = build_tasklist_generate_prompt(p, tdd_file=p, prd_file=p)`. |
| 2 | IMPORTANT | Phase 5 (items 5.2-5.9) | Phase 5 missing verification of 6 artifacts: roadmap variants, diff-analysis, debate-transcript, base-selection, wiring-verification, test-strategy. These artifacts are produced by the spec+PRD pipeline but not checked. | Add items 5.3a through 5.3f checking these 6 artifacts (at minimum existence + line count), OR add a note to the Phase 5 purpose block explicitly stating these are intentionally skipped with rationale. |
| 3 | IMPORTANT | Line 73 (Pipeline Code section) | Claims "All 9 builders now accept `tdd_file` and `prd_file` params" -- wrong count (10 builders exist, only 6 accept these params in roadmap). | Fix to: "6 of 10 roadmap builders accept `tdd_file` and `prd_file` params; 2 tasklist builders also accept them (8 total with PRD blocks)." |
| 4 | IMPORTANT | Item 4.5c | `base-selection.md` is checked for existence and frontmatter only. No PRD enrichment check despite `build_score_prompt` being one of the 8 PRD-enriched builders. | Add PRD enrichment check: search for business value, persona, and compliance scoring dimensions in the base-selection output. |
| 5 | IMPORTANT | Phase 7 header | Header says "(5 items)" but phase contains 6 items (7.1-7.6). | Change to "(6 items)". |
| 6 | IMPORTANT | Item 1.3 | Does not verify `--tdd-file` on `tasklist validate --help`, but item 7.1 uses it. | Add `--tdd-file` verification to item 1.3's tasklist validate help check. |
| 7 | MINOR | Line 73 | States "6 builders have PRD supplementary blocks" but total across both files is 8 (6 roadmap + 2 tasklist). Undercounts tasklist builders. | Covered by fix for issue #3. |

## Actions Taken

All 7 issues fixed in-place:

1. **Fixed item 7.5 Python one-liner (CRITICAL)** -- Changed `build_tasklist_generate_prompt(p, p)` to `build_tasklist_generate_prompt(p)` and all subsequent calls to use keyword arguments only. Added a note about the function signature. Verified by reading the function signature at `src/superclaude/cli/tasklist/prompts.py:144-147`: `(roadmap_file, tdd_file=None, prd_file=None)`.

2. **Added Phase 5 scope note (IMPORTANT)** -- Added "Scope note" to Phase 5 purpose block explaining that intermediate artifacts are thoroughly verified in Phase 4 and not re-checked in Phase 5 to avoid redundancy. Added guidance for executor to spot-check if regressions are suspected.

3. **Fixed Pipeline Code builder count (IMPORTANT)** -- Replaced "All 9 builders now accept `tdd_file` and `prd_file` params; 6 builders have PRD supplementary blocks" with accurate count: "6 of 10 roadmap builders accept `tdd_file` and `prd_file` params with PRD supplementary blocks (extract, extract_tdd, generate, score, spec_fidelity, test_strategy); 4 builders do not (diff, debate, merge, wiring_verification). Plus 2 tasklist builders = 8 total with PRD blocks."

4. **Added PRD enrichment check to item 4.5c (IMPORTANT)** -- Added grep search for business value, persona, and compliance terms in `base-selection.md` to verify `build_score_prompt` PRD enrichment reaches the scoring output.

5. **Fixed Phase 7 header count (IMPORTANT)** -- Changed "(5 items)" to "(6 items)".

6. **Added --tdd-file check to item 1.3 (IMPORTANT)** -- Changed "confirm it contains `--prd-file`" to "confirm it contains both `--prd-file` and `--tdd-file`" for the `tasklist validate --help` verification.

7. **Issue #7 (MINOR)** -- Covered by fix #3 above.

## Recommendations

- All issues have been fixed in-place. No further action needed before task execution.
- The fixed task file should be re-verified by structural QA (rf-qa) to confirm no formatting regressions from edits.

## QA Complete
