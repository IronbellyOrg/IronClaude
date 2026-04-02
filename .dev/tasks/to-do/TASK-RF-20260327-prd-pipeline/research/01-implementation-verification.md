# Implementation Plan Verification Report

**Track**: PRD Pipeline Integration
**Date**: 2026-03-27
**Status**: Complete
**Agent**: research-impl-verify

## Purpose
Verify that the implementation plan's line numbers, function signatures, and insertion points are still accurate against the current code.

---

## File 1: `src/superclaude/cli/roadmap/models.py`

### Plan Claims
- `tdd_file` at L115 of `RoadmapConfig`
- Insert `prd_file: Path | None = None` after `tdd_file` at L115

### Actual State
- `tdd_file` is at **L115** (confirmed exact match): `tdd_file: Path | None = None`
- `RoadmapConfig` dataclass starts at **L94-95** (`@dataclass` + `class RoadmapConfig(PipelineConfig):`)
- `input_type` is at L114, `tdd_file` at L115
- The class ends at L115 (last field), followed by blank line at L116

### Verdict: ACCURATE
- Plan line number L115 is correct.
- Insertion point: add `prd_file: Path | None = None` as L116 (after L115). Clean insertion, no drift.

---

## File 2: `src/superclaude/cli/roadmap/commands.py`

### Plan Claims
- `--input-type` at ~L107
- `run()` signature at L112-127
- `config_kwargs` at L170-181
- Insert `--prd-file` option after `--input-type` (~L110)
- Add `prd_file: Path | None` to `run()` signature
- Add `prd_file` to `config_kwargs`

### Actual State
- `--input-type` option defined at **L105-110** (`@click.option` decorator)
- `@click.pass_context` at L111
- `run()` function signature starts at **L112**, params span L112-127 (exact match to plan)
- Last param is `input_type: str` at L126
- `config_kwargs` dict spans **L170-181** (exact match)
- `input_type` is last entry in config_kwargs at L180

### Verdict: ACCURATE
- All line numbers match exactly.
- Insert `@click.option("--prd-file", ...)` after L110 (after `--input-type` option block, before `@click.pass_context`).
- Add `prd_file: Path | None` param after `input_type: str` in signature.
- Add `"prd_file": prd_file.resolve() if prd_file is not None else None` to config_kwargs after L180.
- **Note**: After inserting the new `@click.option` decorator (6-7 lines), all subsequent line numbers will shift by that amount. The plan correctly identifies the relative positions.

---

## File 3: `src/superclaude/cli/roadmap/executor.py`

### Plan Claims
- `detect_input_type()` exists for auto-detection
- `_build_steps()` at L843-1012
- Extract step's `inputs` list at ~L901
- `build_extract_prompt()` call at L893, `build_extract_prompt_tdd()` at L888
- `build_spec_fidelity_prompt()` call at L990
- `build_test_strategy_prompt()` call at L980
- `build_generate_prompt()` calls at L908, L918
- `build_score_prompt()` call at L950

### Actual State
- `detect_input_type()` at **L59-119** (confirmed)
- `_build_steps()` at **L843** (confirmed exact match), ends at L1012
- Extract step `inputs=[config.spec_file]` at **L901** (confirmed exact)
- `build_extract_prompt_tdd()` call at **L888** (confirmed exact)
- `build_extract_prompt()` call at **L893** (confirmed exact)
- `build_generate_prompt(agent_a, extraction)` at **L908** (confirmed exact)
- `build_generate_prompt(agent_b, extraction)` at **L918** (confirmed exact)
- `build_score_prompt(debate_file, roadmap_a, roadmap_b)` at **L950** (confirmed exact)
- `build_test_strategy_prompt(merge_file, extraction)` at **L980** (confirmed exact)
- `build_spec_fidelity_prompt(config.spec_file, merge_file)` at **L990** (confirmed exact)
- Spec-fidelity step `inputs=[config.spec_file, merge_file]` at **L994** (confirmed)
- Test-strategy step `inputs=[merge_file, extraction]` at **L984** (confirmed)
- Generate-A step `inputs=[extraction]` at **L912** (confirmed)
- Generate-B step `inputs=[extraction]` at **L922** (confirmed)

### Verdict: ACCURATE
- Every line number in the plan matches the current code exactly.
- Insertion points for `prd_file` wiring are all valid.
- **State file handling**: `.roadmap-state.json` is managed by `execute_pipeline()` in `pipeline/executor.py` (not in this file). The plan does not need to modify state handling.

---

## File 4: `src/superclaude/cli/roadmap/prompts.py`

### Plan Claims
- 10 builder functions total
- `build_extract_prompt` signature at L82
- `build_extract_prompt_tdd` signature at L161
- `build_generate_prompt` signature at L288 (uses single return, needs refactor to base pattern)
- `build_diff_prompt` signature at L338
- `build_debate_prompt` signature at L363
- `build_score_prompt` signature at L390 (uses single return, needs refactor)
- `build_merge_prompt` signature at L416
- `build_spec_fidelity_prompt` signature at L448 (uses single return, needs refactor)
- `build_test_strategy_prompt` signature at L586 (uses single return, needs refactor)
- `build_wiring_verification_prompt` signature at L528

### Actual State
- `build_extract_prompt` at **L82** -- uses `base = (...); return base + _OUTPUT_FORMAT_BLOCK` (base pattern). Confirmed.
- `build_extract_prompt_tdd` at **L161** -- uses base pattern. Confirmed.
- `build_generate_prompt` at **L288** -- uses `return (...) + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK` (single return expression, NOT base pattern). **Plan correctly identifies need for refactor.**
- `build_diff_prompt` at **L338** -- uses `return (...) + _OUTPUT_FORMAT_BLOCK` (single return). Confirmed.
- `build_debate_prompt` at **L363** -- uses `return (...) + _OUTPUT_FORMAT_BLOCK` (single return). Confirmed.
- `build_score_prompt` at **L390** -- uses `return (...) + _OUTPUT_FORMAT_BLOCK` (single return). **Plan correctly identifies need for refactor.**
- `build_merge_prompt` at **L416** -- uses `return (...) + _OUTPUT_FORMAT_BLOCK` (single return). Confirmed.
- `build_spec_fidelity_prompt` at **L448** -- uses `return (...) + _OUTPUT_FORMAT_BLOCK` (single return). **Plan correctly identifies need for refactor.**
- `build_wiring_verification_prompt` at **L528**. Confirmed.
- `build_test_strategy_prompt` at **L586** -- uses `return (...) + _OUTPUT_FORMAT_BLOCK` (single return). **Plan correctly identifies need for refactor.**

### Pattern Analysis (base vs single-return)
| Function | Line | Pattern | Plan Refactor Needed? |
|----------|------|---------|----------------------|
| `build_extract_prompt` | L82 | base pattern | No (already base) |
| `build_extract_prompt_tdd` | L161 | base pattern | No (already base) |
| `build_generate_prompt` | L288 | single return | Yes -- plan says so |
| `build_diff_prompt` | L338 | single return | No (P3 deferred, param only) |
| `build_debate_prompt` | L363 | single return | No (P3 deferred, param only) |
| `build_score_prompt` | L390 | single return | Yes -- plan says so |
| `build_merge_prompt` | L416 | single return | No (P3 deferred, param only) |
| `build_spec_fidelity_prompt` | L448 | single return | Yes -- plan says so |
| `build_wiring_verification_prompt` | L528 | single return | No (not targeted by plan) |
| `build_test_strategy_prompt` | L586 | single return | Yes -- plan says so |

### Verdict: ACCURATE
- All 10 function signatures are at the exact lines the plan specifies.
- The plan's identification of which functions need refactoring to base pattern is correct.
- `build_spec_fidelity_prompt` return block spans L461-525 (plan says 461-525, confirmed).
- `build_test_strategy_prompt` return block spans L596-629 (plan says 596-629, confirmed).
- `build_generate_prompt` return block spans L295-335 (plan says 295-335, confirmed).

---

## File 5: `src/superclaude/cli/tasklist/models.py`

### Plan Claims
- `tdd_file` at L25
- Insert `prd_file: Path | None = None` after `tdd_file` at L25

### Actual State
- `TasklistValidateConfig` dataclass at L14-25
- `tdd_file: Path | None = None` at **L25** (confirmed exact match)
- This is the last field in the dataclass

### Verdict: ACCURATE
- Insertion point: add `prd_file: Path | None = None` at L26 after L25. Clean insertion.

---

## File 6: `src/superclaude/cli/tasklist/commands.py`

### Plan Claims
- `--tdd-file` option at L61-66
- Add `--prd-file` option after L66
- Add `prd_file: Path | None` to `validate()` signature at L74
- Add `prd_file` to config construction at L114

### Actual State
- `--tdd-file` option at **L61-66** (confirmed exact match):
  - L61: `@click.option(`
  - L62: `"--tdd-file",`
  - L63: `type=click.Path(exists=True, path_type=Path),`
  - L64: `default=None,`
  - L65: `help="Path to the TDD file used as an additional validation input.",`
  - L66: `)`
- `validate()` function signature at L67-75, `tdd_file: Path | None` param at **L74** (confirmed)
- `TasklistValidateConfig(...)` construction spans L106-115
- `tdd_file=tdd_file.resolve() if tdd_file is not None else None` at **L114** (confirmed exact)

### Verdict: ACCURATE
- All line numbers match exactly.
- Insert `@click.option("--prd-file", ...)` after L66 (before `def validate`).
- Add `prd_file: Path | None` param after L74 in signature.
- Add `prd_file=prd_file.resolve() if prd_file is not None else None` after L114 in config construction.

---

## File 7: `src/superclaude/cli/tasklist/executor.py`

### Plan Claims
- `tdd_file` wiring at L193-194 in `_build_steps()`
- `all_inputs` list at L191
- `build_tasklist_fidelity_prompt()` call at L199-203
- Insert `prd_file` appending after TDD block

### Actual State
- `_build_steps()` at **L188** (plan says 188-211, confirmed)
- `all_inputs = [config.roadmap_file] + tasklist_files` at **L191** (confirmed)
- TDD integration block at **L192-194** (confirmed):
  - L192: `# TDD integration: include TDD file in validation inputs when provided`
  - L193: `if config.tdd_file is not None:`
  - L194: `all_inputs.append(config.tdd_file)`
- `build_tasklist_fidelity_prompt(...)` call at **L199-203** (confirmed):
  - L199: `prompt=build_tasklist_fidelity_prompt(`
  - L200: `config.roadmap_file,`
  - L201: `config.tasklist_dir,`
  - L202: `tdd_file=config.tdd_file,`
  - L203: `),`

### Verdict: ACCURATE
- Every line number matches exactly.
- Insert PRD appending after L194: `if config.prd_file is not None: all_inputs.append(config.prd_file)`
- Add `prd_file=config.prd_file` kwarg to the prompt builder call after L202.

---

## File 8: `src/superclaude/cli/tasklist/prompts.py`

### Plan Claims
- `tdd_file` param at L20 of `build_tasklist_fidelity_prompt`
- Conditional TDD block at L111-123
- Add `prd_file: Path | None = None` param after `tdd_file`
- Add PRD block after L123, before `return base + _OUTPUT_FORMAT_BLOCK` at L125

### Actual State
- `build_tasklist_fidelity_prompt` signature at **L17-21** (confirmed):
  - L17: `def build_tasklist_fidelity_prompt(`
  - L18: `roadmap_file: Path,`
  - L19: `tasklist_dir: Path,`
  - L20: `tdd_file: Path | None = None,`
  - L21: `) -> str:`
- Conditional TDD block at **L110-123** (confirmed):
  - L110: `# TDD integration: append supplementary validation when TDD file is provided`
  - L111: `if tdd_file is not None:`
  - L112-123: TDD supplementary block content
- `return base + _OUTPUT_FORMAT_BLOCK` at **L125** (confirmed)

### Verdict: ACCURATE
- All line numbers match exactly.
- Add `prd_file: Path | None = None,` after L20 (as new L21, shifting `) -> str:` down).
- Add PRD conditional block after L123, before L125's return statement.

---

## Summary

| File | Plan Line Numbers | Drift | Verdict |
|------|-------------------|-------|---------|
| `roadmap/models.py` | tdd_file@L115 | None | ACCURATE |
| `roadmap/commands.py` | --input-type@L105-110, run()@L112-127, config_kwargs@L170-181 | None | ACCURATE |
| `roadmap/executor.py` | detect_input_type@L59, _build_steps@L843, all step calls verified | None | ACCURATE |
| `roadmap/prompts.py` | All 10 builder signatures verified at exact lines | None | ACCURATE |
| `tasklist/models.py` | tdd_file@L25 | None | ACCURATE |
| `tasklist/commands.py` | --tdd-file@L61-66, validate sig@L74, config@L114 | None | ACCURATE |
| `tasklist/executor.py` | _build_steps@L188, tdd wiring@L193-194, prompt call@L199-203 | None | ACCURATE |
| `tasklist/prompts.py` | tdd_file param@L20, TDD block@L111-123, return@L125 | None | ACCURATE |

### Overall Assessment

**Zero drift detected.** All 8 target files have line numbers, function signatures, and insertion points that match the implementation plan exactly. The plan is ready for task file construction with no corrections needed.

### Additional Observations

1. **Refactoring targets confirmed**: 4 prompt builders (`build_generate_prompt`, `build_score_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`) correctly identified as needing refactor from single-return to base pattern.
2. **Executor wiring is straightforward**: All `_build_steps()` modifications involve adding kwargs to existing builder calls and appending to existing `inputs` lists -- no structural changes needed.
3. **Pattern consistency**: The `tdd_file` integration pattern in tasklist (models -> commands -> executor -> prompts) provides a direct template for `prd_file` in both pipelines.
4. **No state file changes needed**: `.roadmap-state.json` handling in `pipeline/executor.py` does not need modification for `prd_file`.
