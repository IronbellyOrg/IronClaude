# QA Report -- Phase 4 Gate (Prompt Builder Refactoring + P1 Enrichment)

**Topic:** PRD Pipeline Integration -- Phase 4
**Date:** 2026-03-27
**Phase:** phase-gate
**Fix cycle:** 1

---

## Overall Verdict: PASS (after 2 in-place fixes)

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 4.1 | `build_extract_prompt` has `prd_file` param and 5-check PRD block | PASS | Signature at line 82-86: `prd_file: Path \| None = None`. PRD block at lines 159-178 contains 5 numbered checks (S19, S7, S12, S17, S6). Verified via import test. |
| 4.2 | `build_generate_prompt` refactored to base pattern with `prd_file` param | PASS | Signature at line 328-331: `prd_file: Path \| None = None`. Uses `base = (...)` pattern with conditional append. |
| 4.3 | `build_generate_prompt` has 4-check PRD block between base and return | PASS | PRD block at lines 363-379 contains 4 numbered checks (value-based phasing, persona-driven sequencing, compliance gates, scope guardrails). Verified 4 checks via automated count. |
| 4.4 | `build_spec_fidelity_prompt` refactored with `prd_file` param and dimensions 12-15 | PASS | Signature at line 529-532: `prd_file: Path \| None = None`. PRD block at lines 591-608 adds dimensions 12 (Persona Coverage), 13 (Business Metric Traceability), 14 (Compliance & Legal Coverage), 15 (Scope Boundary Enforcement). All 4 dimensions verified present. |
| 4.5 | `build_test_strategy_prompt` refactored with `prd_file` param and 5-check block | PASS | Signature at line 689-692: `prd_file: Path \| None = None`. PRD block at lines 717-734 contains 5 numbered checks (persona-based acceptance, customer journey E2E, KPI validation, compliance test category, edge case coverage). Verified 5 checks. |
| 4.6 | `build_score_prompt` refactored with `prd_file` param and 3-dimension block | PASS | Signature at line 454-458: `prd_file: Path \| None = None`. PRD block at lines 462-474 contains 3 numbered dimensions (business value delivery, persona coverage, compliance alignment). Verified 3 dimensions. |
| 4.7 | `build_tasklist_fidelity_prompt` has `prd_file` param and 3-check block after TDD block | PASS | Signature at line 17-22: `prd_file: Path \| None = None`. PRD block at lines 127-139 appears AFTER TDD block (line 112). Contains 3 numbered checks (persona coverage, success metrics, acceptance scenarios). Verified ordering and count. |
| 4.7b | Tasklist executor passes `prd_file=config.prd_file` to builder | PASS | `executor.py` line 206: `prd_file=config.prd_file` in `build_tasklist_fidelity_prompt()` call. `TasklistValidateConfig` has `prd_file: Path \| None = None` field. |
| 4.8 | All 6 builders import and run without errors when `prd_file=None` | PASS | Ran `uv run python` import test: all 6 builders (`build_extract_prompt`, `build_generate_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`, `build_score_prompt`, `build_tasklist_fidelity_prompt`) return `str` with `prd_file=None`. Also verified `build_extract_prompt_tdd` after fix. |
| 4.8b | 7 roadmap executor call sites pass `prd_file=config.prd_file` | PASS | Grep confirmed 7 call sites in `roadmap/executor.py`: lines 891, 897, 910, 920, 952, 982, 992. All pass `prd_file=config.prd_file`. |
| CRIT | No premature kwargs -- all `prd_file` kwargs added after builder signatures updated | PASS | Builder signatures in `prompts.py` accept `prd_file` param; executor call sites in `executor.py` pass the kwarg. Both files modified in same phase. No ordering issue since builders were updated first. |

## Summary

- Checks passed: 11 / 11 (after fixes)
- Checks failed: 0 (after fixes)
- Critical issues found: 2 (both fixed in-place)
- Issues fixed in-place: 2

## Issues Found (Pre-Fix)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `src/superclaude/cli/roadmap/prompts.py:183-186` | `build_extract_prompt_tdd()` was missing `prd_file` parameter. Executor line 891 passes `prd_file=config.prd_file` to it, which causes `TypeError: build_extract_prompt_tdd() got an unexpected keyword argument 'prd_file'` at runtime when `input_type == "tdd"` and `prd_file` is set. | Add `prd_file: Path \| None = None` param and corresponding PRD enrichment block (matching the 5-check pattern from `build_extract_prompt`). |
| 2 | MEDIUM | `src/superclaude/cli/roadmap/executor.py:956` | Score step `inputs` list was `[debate_file, roadmap_a, roadmap_b]` -- missing `config.prd_file`. The prompt references PRD content via `build_score_prompt(..., prd_file=config.prd_file)` but the PRD file would not be inline-embedded into the subprocess prompt, making the PRD scoring dimensions ungrounded. | Add `+ ([config.prd_file] if config.prd_file else [])` to score step inputs, matching all other PRD-aware steps. |

## Actions Taken

1. **Fixed `build_extract_prompt_tdd` missing `prd_file` param** in `src/superclaude/cli/roadmap/prompts.py`:
   - Added `prd_file: Path | None = None` to function signature (line 185)
   - Added 5-check PRD enrichment block (matching `build_extract_prompt` pattern but referencing "TDD" instead of "specification") inserted after the retrospective block and before the return statement
   - Verified fix: `build_extract_prompt_tdd(Path(...), prd_file=Path(...))` now returns str with "Supplementary PRD" block present. Backward compat confirmed with `prd_file=None`.

2. **Fixed score step missing PRD in `inputs` list** in `src/superclaude/cli/roadmap/executor.py`:
   - Changed line 956 from `inputs=[debate_file, roadmap_a, roadmap_b]` to `inputs=[debate_file, roadmap_a, roadmap_b] + ([config.prd_file] if config.prd_file else [])`
   - Verified fix via grep: score step inputs now conditionally includes `config.prd_file`, matching the pattern used by extract, generate-a, generate-b, test-strategy, and spec-fidelity steps.

## Verification Note on phase4-import-verification.md

The existing import verification report at `phase-outputs/test-results/phase4-import-verification.md` claims all 6 builders PASS. This is accurate for the 6 listed builders (`build_extract_prompt`, `build_generate_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`, `build_score_prompt`, `build_tasklist_fidelity_prompt`). However, it does NOT cover `build_extract_prompt_tdd`, which is the 7th builder that also receives `prd_file` from the executor. The critical bug was in this uncovered builder.

## Recommendations

- Phase 4 is now PASS after fixes. Green light to proceed to Phase 5.
- The import verification checklist should be expanded to include `build_extract_prompt_tdd` since it is also called with `prd_file` from the executor.

## QA Complete
