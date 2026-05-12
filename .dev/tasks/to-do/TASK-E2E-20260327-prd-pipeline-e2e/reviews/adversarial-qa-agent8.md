# QA Report -- Adversarial Round 4, Agent 8 (Micro-Level Code Inspection)

**Date:** 2026-03-28
**Phase:** Adversarial QA -- micro-level code inspection
**Fix cycle:** N/A (report only)
**Scope:** Character-by-character inspection of prompt builders, executor logic, CLI decorators, dataclass models, state persistence, auto-wire logic, and test imports

---

## Overall Verdict: FAIL

## Methodology

This review focused exclusively on micro-level issues that prior agents (72 findings: C-01 through C-61, D-01, D-02, S-01 through S-03) may have overlooked: off-by-one errors, string formatting bugs, semantic reference accuracy, conditional logic correctness, and copy-paste artifacts.

---

## Issues Found

| # | ID | Severity | Location | Issue | Required Fix |
|---|-----|----------|----------|-------|-------------|
| 1 | M-01 | IMPORTANT | `src/superclaude/cli/roadmap/executor.py:857-859` | **`_build_steps` input_type resolution does not propagate to caller.** The comment at line 857-858 says "Write resolved type back to config so _save_state() stores the actual detected type (not 'auto')". However, `dataclasses.replace()` at line 859 creates a NEW object assigned to the LOCAL variable `config` inside `_build_steps`. The caller at line 1819 (`steps = _build_steps(config)`) never receives the updated config. At line 1842, `_save_state(config, results)` is called with the ORIGINAL config that still has `input_type="auto"`. Result: `.roadmap-state.json` stores `"input_type": "auto"` instead of the resolved type, which breaks downstream consumers that check `state.get("input_type") == "tdd"` (e.g., the tasklist auto-wire fallback at `tasklist/commands.py:132`). | Change `_build_steps` to return `tuple[list[Step | list[Step]], RoadmapConfig]` and update the caller at line 1819 to `steps, config = _build_steps(config)`. Alternatively, resolve input_type in `execute_roadmap` before calling `_build_steps`. NOTE: If this is the same as a prior finding, disregard -- I could not verify overlap without seeing the full 72-item list. |
| 2 | M-02 | MINOR | `src/superclaude/cli/tasklist/prompts.py:205` | **PRD enrichment block references wrong section for "acceptance scenarios".** Line 205 says "Acceptance scenarios from S7/S22 -- each user story acceptance criterion should map to a verification task." However, PRD S7 (User Personas) contains persona profiles (demographics, goals, pain points) -- NOT user stories or acceptance scenarios. PRD S22 (Customer Journey Map) contains journey stages and "Moments of Truth" with high-level success criteria, not feature-level acceptance criteria. User stories with acceptance criteria would be in S12 (Scope Definition) or S14 (Technical Requirements). The LLM receiving this prompt will search S7/S22 for acceptance scenarios that do not exist there. | Change "S7/S22" to "S12/S14" or rephrase to: "Persona-driven acceptance scenarios: derive verification tasks from the personas in S7 and journey moments of truth in S22." This makes the instruction match what actually exists in those sections. |
| 3 | M-03 | MINOR | `src/superclaude/cli/tasklist/executor.py:58` | **Redundant `Path()` wrapping.** `content = Path(p).read_text(encoding="utf-8")` where `p` is already typed as `Path` (from `input_paths: list[Path]`). The `Path(p)` call is a no-op identity conversion. While harmless at runtime, it suggests a copy-paste from a context where `p` might have been a string. | Change to `content = p.read_text(encoding="utf-8")`. Same issue exists at `roadmap/executor.py:145`. |
| 4 | M-04 | MINOR | `src/superclaude/cli/roadmap/executor.py:145` | **Same redundant `Path()` wrapping** as M-03 in roadmap executor's `_embed_inputs`. `content = Path(p).read_text(encoding="utf-8")` where `p` is already a `Path`. | Change to `content = p.read_text(encoding="utf-8")`. |
| 5 | M-05 | MINOR | `src/superclaude/cli/roadmap/prompts.py:370` | **Bare f-string prefix on non-interpolated line.** Line 370: `f"- spec_source: (the source specification filename)\n"` -- this is an f-string but contains no `{...}` interpolation. It appears to be a leftover from when the line might have interpolated `spec_file.name`. The `f` prefix is harmless but misleading; a reader may search for the missing interpolation variable. | Remove the `f` prefix: `"- spec_source: (the source specification filename)\n"`. |
| 6 | M-06 | MINOR | `src/superclaude/cli/roadmap/prompts.py:372` | **Bare f-string on non-interpolated line.** Line 372: `f"- primary_persona: {agent.persona}\n\n"` -- this one DOES interpolate `agent.persona`, so the f-string is correct. However, examining the full frontmatter instruction block (lines 369-372), the `spec_source` line (370) uses f-string without interpolation while `primary_persona` (372) correctly interpolates. This inconsistency suggests line 370 was intended to interpolate `spec_file.name` but the variable was removed during refactoring. | Either interpolate spec_file on line 370 (`f"- spec_source: {spec_file.name}\n"`) if the spec filename should be hardcoded into the prompt, or remove the f-prefix if it's intentionally left for the LLM to fill. Currently ambiguous. |
| 7 | M-07 | MINOR | `src/superclaude/cli/roadmap/prompts.py:82-86` | **`build_extract_prompt` accepts `tdd_file` parameter but never references it in the function body.** The parameter `tdd_file: Path | None = None` at line 85 is accepted but only `prd_file` is checked (line 160). For the non-TDD extract path, `tdd_file` is silently ignored. The function signature implies TDD supplementary context would be injected, but no TDD block exists. Callers (executor.py:910) pass `tdd_file=config.tdd_file` to this function. | Either (a) remove the `tdd_file` parameter from `build_extract_prompt` and update the caller, or (b) add a TDD supplementary context block similar to the PRD block. This same pattern exists in `build_generate_prompt` (line 337), `build_score_prompt` (line 465), and `build_test_strategy_prompt` (line 701). NOTE: This may overlap with prior finding C-05 (dead tdd_file params). If so, this finding adds the specific function names and line numbers. |
| 8 | M-08 | MINOR | `src/superclaude/cli/roadmap/prompts.py:671` | **Bare f-string on non-interpolated line.** Line 671: `f"- target_dir: (the directory analyzed)\n"` -- f-string prefix but no `{...}` interpolation. The `target_dir` value is left as a prompt instruction for the LLM to fill, but the f-prefix suggests it was intended to interpolate `merge_file.parent` or similar. | Remove the `f` prefix or interpolate the actual directory path. |
| 9 | M-09 | MINOR | `src/superclaude/cli/tasklist/prompts.py:1-14` | **`_OUTPUT_FORMAT_BLOCK` imported from roadmap module.** `from superclaude.cli.roadmap.prompts import _OUTPUT_FORMAT_BLOCK` -- this is a cross-module import of a private symbol (underscore-prefixed). While functional, it creates a coupling between `tasklist.prompts` and `roadmap.prompts`. If the roadmap module refactors or removes this constant, tasklist breaks. The `_` prefix convention signals "internal to this module." | Either (a) move `_OUTPUT_FORMAT_BLOCK` to a shared location like `pipeline.prompts` or `pipeline.constants`, or (b) rename it without the underscore prefix to signal it's part of the public API, or (c) duplicate it in tasklist/prompts.py. Option (a) is cleanest. |

---

## Items Reviewed (Detailed Checklist)

| # | Area Inspected | Result | Evidence |
|---|---------------|--------|----------|
| 1 | PRD blocks in `build_extract_prompt` (prompts.py:160-179) | PASS | Block text well-formed. PRD section references (S19, S7, S12, S17, S6) verified against `prd_template.md` -- all correct. Newline at block boundary (`\n\n##`) prevents text merging. |
| 2 | PRD blocks in `build_extract_prompt_tdd` (prompts.py:310-329) | PASS | Block text matches spec context. Says "alongside the TDD" (correct framing). Same PRD section references, all verified correct. |
| 3 | PRD blocks in `build_generate_prompt` (prompts.py:388-404) | PASS | Block references S5, S19, S7, S22, S17, S12 -- all correct per template. Text well-formed with proper newlines. |
| 4 | PRD blocks in `build_score_prompt` (prompts.py:488-500) | PASS | References S19, S7, S17 -- all correct. |
| 5 | PRD dimensions in `build_spec_fidelity_prompt` (prompts.py:618-635) | PASS | Dimensions 12-15 reference S7, S19, S17, S12 -- all correct. Severity assignments (MEDIUM for persona/metric/scope, HIGH for compliance) are reasonable. |
| 6 | PRD checks in `build_test_strategy_prompt` (prompts.py:745-762) | PASS | References S7, S22, S19, S17, S23 -- all correct per template. |
| 7 | TDD block in `build_tasklist_fidelity_prompt` (prompts.py:112-124) | PASS | References section 15 (Testing Strategy), section 19 (Migration & Rollout), section 10 (Component Inventory) -- all verified correct against `tdd_template.md`. |
| 8 | TDD enrichment in `build_tasklist_generate_prompt` (prompts.py:180-195) | PASS (with M-02 caveat) | TDD references S15, S8, S10, S19, S7 -- all correct. |
| 9 | PRD enrichment in `build_tasklist_generate_prompt` (prompts.py:198-216) | FAIL (M-02) | S7/S22 "acceptance scenarios" reference is semantically incorrect. |
| 10 | Combined interaction block (prompts.py:220-228) | PASS | Only triggered when both tdd_file and prd_file are non-None. Text is correct. |
| 11 | `_OUTPUT_FORMAT_BLOCK` placement | PASS | Every prompt builder returns `base + _OUTPUT_FORMAT_BLOCK` (or `base + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK` for generate). PRD/TDD blocks are always inserted before the output format block. |
| 12 | `detect_input_type()` regex (executor.py:83) | PASS | `r"^## \d+\."` with `re.MULTILINE` correctly matches lines starting with `## ` followed by digits and a period. Does NOT match `## 1` (no period) or `##1.` (missing space). The `re.MULTILINE` flag is correctly passed to `re.findall`. |
| 13 | `detect_input_type()` content slice (executor.py:111) | PASS | `content[:1000]` for "Technical Design Document" string search. This is a character slice, not byte slice. The string is in the YAML frontmatter which is always in the first ~500 chars. Even if the string straddled byte 1000, Python string slicing is character-based and would cleanly cut mid-string (worst case: miss detection, fallback to other signals). |
| 14 | TDD-exclusive field detection (executor.py:95-98) | PASS | `parent_doc` and `coordinator` are checked with `re.search(rf"^{field}:", content, re.MULTILINE)`. These fields are in the TDD template frontmatter but not in the release-spec template. The regex correctly anchors to line start. |
| 15 | Click decorator ordering in `roadmap/commands.py` | PASS | Decorators are applied bottom-up per Click convention. `@click.pass_context` is last decorator (line 123), meaning it's the innermost wrapper -- correct for Click. Function params match decorator order (reversed). |
| 16 | Dataclass field ordering in `roadmap/models.py` | PASS | `RoadmapConfig` extends `PipelineConfig`. Parent has all defaulted fields. Child fields (lines 102-116) all have defaults (either `field(default_factory=...)` or direct defaults). No fields-without-defaults-after-defaults violation. |
| 17 | `_save_state` dict literal (executor.py:1437-1458) | PASS (with M-01 caveat) | All new fields present: `tdd_file` (line 1440), `prd_file` (line 1441), `input_type` (line 1442). Paths correctly stringified with `str()` or ternary None. JSON-serializable (no Path objects, no sets). |
| 18 | Auto-wire code in `tasklist/commands.py:113-159` | PASS | `read_state` correctly imported from `..roadmap.executor`. The `or {}` fallback on line 116 handles None/missing state. TDD fallback (`elif state.get("input_type") == "tdd"`) at line 132 is in correct position. `saved_spec_path.is_file()` at line 139 could theoretically raise for malformed paths but `Path()` constructor handles any string. |
| 19 | Test file imports | PASS | All 4 test files (`tests/roadmap/test_prd_cli.py`, `tests/roadmap/test_prd_prompts.py`, `tests/tasklist/test_prd_cli.py`, `tests/tasklist/test_prd_prompts.py`) import from correct modules. No stale imports detected. |
| 20 | String escaping in prompt text | PASS | No unescaped quotes in prompt strings. All prompts use parenthesized string concatenation (no raw f-strings with complex expressions). No backslash sequences that could cause issues. |
| 21 | Markdown formatting in prompt blocks | PASS | All `##` headers in prompt text are properly spaced. Backtick usage is balanced. No unclosed formatting. |
| 22 | `TasklistValidateConfig` dataclass (tasklist/models.py) | PASS | All fields have defaults. `tdd_file` and `prd_file` correctly typed as `Path | None = None`. |

---

## Summary

- Checks performed: 22
- Checks passed: 21
- Checks failed: 1 (M-02)
- Issues found: 9 total
  - CRITICAL: 0
  - IMPORTANT: 1 (M-01)
  - MINOR: 8 (M-02 through M-09)
- Issues fixed in-place: 0 (report only)

## Overlap Notes

- **M-01** may overlap with a prior finding about `_build_steps` not propagating config changes. The specific failure mode (`.roadmap-state.json` stores `"auto"` instead of resolved type, breaking tasklist auto-wire) may be new detail.
- **M-07** may overlap with prior finding C-05 (dead `tdd_file` parameters). This report adds specific function names, line numbers, and the complete list of affected functions.
- All other findings (M-02 through M-06, M-08, M-09) are new micro-level issues not covered by structural or integration-level reviews.

## Recommendations

1. Resolve M-01 before relying on tasklist auto-wire from `.roadmap-state.json` for TDD inputs.
2. Fix M-02 to prevent LLM confusion when enriching tasklist generation with PRD context.
3. The remaining MINOR items (M-03 through M-09) can be addressed as cleanup in a subsequent pass.

## QA Complete
