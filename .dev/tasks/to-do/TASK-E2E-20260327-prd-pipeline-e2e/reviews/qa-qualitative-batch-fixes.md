# QA Report -- Qualitative Review (TDD/PRD Batch Fixes)

**Date:** 2026-04-02
**Phase:** batch-fix-review
**Reviewer:** rf-qa-qualitative (adversarial)

---

## Overall Verdict: FAIL

**Summary:** 12 fixes reviewed. 10 pass. 1 has a confirmed interaction bug (C-08 vs C-111 redundancy guard). 1 has a missing test gap. Additionally, 1 cross-cutting concern identified regarding test coverage of the C-08 scenario.

---

## Items Reviewed

| # | Finding | Fix Location | Result | Evidence |
|---|---------|-------------|--------|----------|
| 1 | C-84: Dead auto-detection code in `_build_steps` | `executor.py:_build_steps` | **PASS** | `_build_steps` no longer contains auto-detection logic. Auto-detection now runs once in `execute_roadmap` (line 1838-1841) before `_build_steps` is called. The resolved `input_type` flows through `config` cleanly. |
| 2 | C-113: `effective_input_type` alias removed | `executor.py` | **PASS** | Grep confirms zero occurrences of `effective_input_type` in the file. All references use `config.input_type` directly. |
| 3 | C-111: Redundancy guard moved to `execute_roadmap` | `executor.py:1861-1868` | **PASS** | Guard now runs in `execute_roadmap` after auto-detection resolves `input_type`, and before `_build_steps`. Uses `dataclasses.replace` so the nulled `tdd_file` persists to `_save_state`. State file will correctly record `tdd_file: null` for TDD-primary inputs. |
| 4 | C-91: `input_type` restoration from state | `executor.py:1734-1739` | **PASS** | Restores `input_type` from state when current config is `"auto"` and saved value is not `"auto"`. Prevents re-running detection on resume. Condition is correct: only overrides when the CLI did not explicitly set `input_type`. |
| 5 | C-08: TDD fallback in `_restore_from_state` | `executor.py:1751-1762` | **FAIL** | See Issues Found #1. The fallback sets `config.tdd_file = spec_path` when `input_type=tdd` and `tdd_file` is null in state. But then `execute_roadmap` line 1863-1868 runs the redundancy guard which nulls `tdd_file` when `input_type == "tdd"`. The C-08 fix is immediately undone by C-111. |
| 6 | C-27: Explicit `--prd-file` CLI override | `executor.py:1764-1781` | **PASS** | Two branches: (a) `config.prd_file is None` restores from state, (b) else-branch logs when CLI value differs from state. Logic is correct. The else branch only fires when `config.prd_file` was already set by CLI, which is the right condition. |
| 7 | C-50: Debug logging for TDD/PRD decisions | `executor.py:1843-1847` | **PASS** | Logs `tdd_file` and `prd_file` at INFO level before the guards run. Placement is correct -- appears after auto-detection resolves but before guards modify values, so the log captures the pre-guard state. |
| 8 | C-20: Same-file guard | `executor.py:1849-1859` | **PASS** | Uses `.resolve()` for path comparison (handles symlinks, relative paths). Raises `SystemExit(1)` with clear error. Placement is correct: after logging, before redundancy guard. One edge case: if both are None, the short-circuit `is not None` checks prevent a crash. |
| 9 | C-103: Borderline detection warning | `executor.py:120-126` | **PASS** | Warns for scores 3-6. The threshold is `>= 5`, so scores 3-4 are spec (warned), score 5-6 are tdd (warned). Score 7+ is confident TDD, score 0-2 is confident spec. Range is appropriate. |
| 10 | C-06: Merge prompt with TDD/PRD blocks | `prompts.py:592-654` | **PASS** | `build_merge_prompt` now accepts `tdd_file` and `prd_file` kwargs. Conditionally appends TDD block (identifiers, API contract preference, task retention) and PRD block (personas S7, metrics S19, compliance S17, tie-breaking). Blocks are additive and non-conflicting. The `_build_steps` call at line 966 correctly passes both kwargs. |
| 11 | C-88: CLI help text expansion | `commands.py:115-131` | **PASS** | Help text for `--tdd-file` explains it is supplementary context, notes it is ignored when primary input is TDD. Help text for `--prd-file` explains personas/metrics/compliance enrichment and auto-wiring from state on resume. Both are accurate descriptions of actual behavior. |
| 12 | C-61: TDD template sentinel fix | `tdd_template.md:17-18` | **PASS** | `complexity_score` and `complexity_class` comments now read "computed by sc:roadmap; provide estimated value if known" and line 64/67 confirm the pipeline consumption notes are consistent. |
| 13 | C-75: Tasklist PRD section references | `tasklist/prompts.py:136-137` | **PASS** | Changed from S7/S22 to S12/S22. Verified: S12 = Scope Definition (contains acceptance scenarios), S22 = Customer Journey Map. This is correct for a PRD -- S7 is User Personas (used elsewhere at line 132 for persona coverage, which is the right context). S12 for acceptance scenarios is the correct reference. |
| 14 | C-93: Test docstring dimension count | `test_spec_fidelity.py:103` | **PASS** | Docstring now reads "6 base comparison dimensions (7-11 are TDD-conditional, 12-15 are PRD-conditional)". This matches the prompt structure where base dimensions are always present and TDD/PRD dimensions are conditional. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | **CRITICAL** | `executor.py:1751-1762` vs `executor.py:1861-1868` | **C-08 fix is nullified by C-111 redundancy guard.** When resuming a TDD-primary run: (a) `_restore_from_state` sets `config.input_type = "tdd"` (C-91, line 1739), (b) C-08 fallback sets `config.tdd_file = spec_path` (line 1762), (c) auto-detection is skipped because `input_type != "auto"` (line 1838), (d) redundancy guard at line 1863 sees `input_type == "tdd"` AND `tdd_file is not None`, so it nulls `tdd_file` with a warning. **Result:** The C-08 fallback is dead code on resume. The `tdd_file` is set and then immediately cleared. | Two options: **(A)** Remove the C-08 fallback entirely -- it cannot work as long as the redundancy guard exists, and its purpose (providing TDD context to downstream steps) is already served by the spec_file being the TDD. The redundancy guard's logic is correct: when the primary input IS a TDD, the supplementary `--tdd-file` slot is meaningless. **(B)** If the intent is that downstream prompts need an explicit `tdd_file` pointer even when it is the same as `spec_file`, then the redundancy guard must be modified to allow `tdd_file == spec_file` as a special case. Option A is simpler and correct. |
| 2 | **IMPORTANT** | `tests/cli/test_tdd_extract_prompt.py` | **No test covers the C-08 resume scenario.** `TestOldSchemaStateBackwardCompat` tests old state files without TDD/PRD fields, but there is no test for: (a) state with `input_type=tdd` and `tdd_file=null` triggering the fallback, (b) verifying the interaction with the redundancy guard in `execute_roadmap`. The C-08 code path is untested. | Add a test in `TestOldSchemaStateBackwardCompat` or a new class that creates a state file with `input_type: "tdd"`, `tdd_file: null`, `spec_file: "/path/to/tdd.md"`, calls `_restore_from_state`, and verifies the resulting `config.tdd_file`. Then add an integration-level test that runs the relevant section of `execute_roadmap` to verify the redundancy guard interaction. |
| 3 | **MINOR** | `executor.py:1849-1859` | **Same-file guard does not account for state-wired paths.** The C-20 same-file guard runs after `_restore_from_state` on resume, which is correct. However, if a state file was manually edited (or corrupted) to have `tdd_file` and `prd_file` pointing to the same path, the guard will catch it and `SystemExit(1)`. This is correct behavior but the error message says "--tdd-file and --prd-file point to the same file" which implies CLI flags, when the values may have come from state restoration. Consider a more accurate message that says "tdd_file and prd_file resolve to the same file" without implying CLI origin. | Update error message to: `"tdd_file and prd_file resolve to the same file: %s. These must be different documents (check CLI flags or .roadmap-state.json)."` |

---

## Test Adequacy Assessment

| Test Class | Fixes Covered | Adequacy | Notes |
|-----------|--------------|----------|-------|
| `TestExtractPromptTddWithPrd` (6 tests) | C-16 (PRD blocks in extract prompts) | **Good** | Tests presence/absence of PRD and TDD blocks, advisory guardrail. Covers both `build_extract_prompt_tdd` and `build_extract_prompt`. |
| `TestMergePromptTddPrd` (4 tests) | C-06 (merge prompt TDD/PRD) | **Good** | Tests baseline (no TDD/PRD), TDD-only, PRD-only, and both. Asserts on specific content markers. |
| `TestOldSchemaStateBackwardCompat` (2 tests) | C-17 (old state compat) | **Adequate** | Tests that old state files load without crash and that missing fields default to None. Does not test C-08 fallback. |
| `TestDetectionThresholdBoundary` (4 tests) | C-18, C-103 (detection threshold) | **Good** | Tests score=0 (spec), score=4 (spec), score=5 (tdd), score=6 (tdd). Directly validates the threshold boundary at 5. Score calculations verified by constructing documents with known signal counts. |

**Missing test coverage:**
- C-08: TDD fallback in `_restore_from_state` (zero tests)
- C-20: Same-file guard (zero tests -- should test `SystemExit(1)` on same file, and PASS on different files)
- C-27: Explicit `--prd-file` override (zero tests -- should test that CLI value is not overwritten by state)
- C-111: Redundancy guard interaction with `_save_state` (zero tests verifying state file records `tdd_file: null`)

---

## Recommendations

1. **Resolve C-08 vs C-111 conflict (CRITICAL).** The C-08 fallback in `_restore_from_state` is dead code. Either remove it (Option A) or adjust the redundancy guard to permit the `tdd_file == spec_file` case (Option B). Option A is recommended -- the spec_file already IS the TDD in this scenario, and all prompt builders already receive `config.spec_file` as their primary input.

2. **Add tests for C-08, C-20, C-27, C-111.** Four fixes have zero dedicated tests. The C-08 gap is particularly important because the bug would be caught immediately by a test.

3. **Minor: Improve C-20 error message** to not assume CLI origin of the conflicting paths.

4. **All other fixes are sound.** The prompt changes (C-06), detection improvements (C-103), state restoration (C-91, C-27), and template fixes (C-61, C-75, C-93) are correctly implemented and do what they claim.

---

## QA Complete
