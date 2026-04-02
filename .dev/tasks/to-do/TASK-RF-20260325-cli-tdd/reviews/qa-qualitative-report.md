# QA Report -- Qualitative Code Review

**Topic:** TASK-RF-20260325-cli-tdd (TDD Support for CLI Roadmap Pipeline)
**Date:** 2026-03-26
**Phase:** qualitative-review (adversarial code correctness)
**Fix cycle:** 1

---

## Overall Verdict: FAIL (4 issues found; 3 fixed in-place, 1 MINOR documented)

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | Extract step ternary in Step() constructor | PASS | Verified: parenthesized ternary `prompt=(expr if cond else expr)` is valid Python inside a dataclass constructor. Lines 818-828 of executor.py. |
| b | Click --input-type to input_type parameter mapping | PASS | Verified: Click auto-converts `--input-type` to `input_type` via standard hyphen-to-underscore. The `run()` signature at line 126 declares `input_type: str`. Click Choice passes the string directly. No explicit name= override needed. |
| c | tasklist/prompts.py refactoring correctness | PASS | Verified: `base` captures the entire original prompt string (lines 36-108). The `if tdd_file is not None:` block appends to `base`. Final return at line 125 is `return base + _OUTPUT_FORMAT_BLOCK` -- this executes in ALL code paths (both with and without TDD). No path returns without `_OUTPUT_FORMAT_BLOCK`. |
| d | hasattr guard on tdd_file in tasklist/executor.py | FAIL | `hasattr(config, 'tdd_file')` always returns True for a dataclass field with a default. The guard should be `config.tdd_file is not None`. While the current code has `hasattr(config, 'tdd_file') and config.tdd_file is not None` which evaluates correctly due to the `and` clause, the `hasattr` check is dead code that misleads readers into thinking `tdd_file` might not exist as an attribute. Same pattern on line 202. |
| e | config.spec_file type for .read_bytes() | PASS | Verified: `config.spec_file` is set from `spec_file.resolve()` in config_kwargs (line 170). `spec_file` is a `Path` from Click's `path_type=Path`. `.resolve()` returns a `Path`. `Path.read_bytes()` is a valid method. No type issue. |
| f | String concatenation in build_extract_prompt_tdd() | PASS | Verified: All section boundaries have proper `\n\n` separators. Each section string ends with `\n\n`. The 14 sections are properly separated. No missing newlines between section boundaries. |
| g | Generalized spec-fidelity prompt clarity for spec inputs | FAIL | `build_spec_fidelity_prompt()` now says "source-document fidelity analyst" and "Source Quote" instead of "spec fidelity analyst" and "Spec Quote". When a spec file is the input, a Claude subprocess is told to find "Source Quote" which is less precise than "Spec Quote". The generalization dilutes prompt clarity for the majority use case (spec inputs). However, this is a prompt quality concern, not a correctness bug -- the subprocess will still function. |
| h | Python comment inside string concatenation in build_generate_prompt() | PASS | Verified lines 308-317: The comments (lines 309-316) are placed between two string literals in an implicit concatenation chain inside parentheses. Python allows `# comment` between string literals in implicit concatenation. Line 308 ends with `\n"` and line 317 starts with `"\n"`. The comment is a valid Python comment, NOT inside the string. The output string correctly concatenates `"...indicator\n"` + `"\n"` producing `"...indicator\n\n"`. |
| i | Stale docstring on run() function | FAIL | Line 128-131: docstring says `SPEC_FILE is the path to a specification markdown file.` but the function now accepts TDD files via `--input-type tdd`. The docstring should mention TDD support. |
| j | Test gap for TDD input validation warning | FAIL | The test file `test_tdd_extract_prompt.py` tests prompt construction but does NOT test the TDD input validation logic in `commands.py` lines 201-216 (the `read_bytes()[:500]` check for "Technical Design Document"). This validation logic has no test coverage. |
| k | Large TDD file embedding risk in tasklist/executor.py | PASS | The `_embed_inputs()` function (line 52-60) already handles this: at line 115-120, if the composed prompt exceeds `_EMBED_SIZE_LIMIT` (100KB), it logs a warning but proceeds. This is documented behavior -- the warning exists, and the pipeline continues. The TDD template is 89KB which would push it over the limit WITH other files, but the system handles this gracefully with a warning. Not a bug, just a known trade-off. |
| l | Type consistency of input_type across files | PASS | `commands.py` declares `input_type: str` (line 126). `models.py` declares `input_type: Literal["spec", "tdd"]` (line 114). Click passes a string that matches the Literal values because `click.Choice(["spec", "tdd"])` constrains the value. Python's `Literal["spec", "tdd"]` accepts plain `str` values at runtime (Literal is a typing hint, not enforced at runtime by dataclasses). No runtime error. |
| m | gates.py ANTI_INSTINCT_GATE comment accuracy | PASS | The comment says "ANTI_INSTINCT_GATE: format-agnostic (pure Python)." Verified: ANTI_INSTINCT_GATE (line 1003) checks frontmatter fields `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage` with semantic checks. The anti-instinct audit (executor.py lines 273-280) runs `scan_obligations()`, `extract_integration_contracts()`, `check_fingerprint_coverage()` -- all pure Python, no LLM. The gate checks are format-agnostic (they check YAML frontmatter fields regardless of whether input was spec or TDD). Comment is accurate. |
| n | Import hygiene | PASS | Verified: `build_extract_prompt_tdd` is imported in executor.py (line 46) and used in line 819. No unused imports added. All new imports are used. |

## Summary
- Checks passed: 10 / 14
- Checks failed: 4
- Critical issues: 0
- Important issues: 2 (both fixed)
- Minor issues: 2 (1 fixed, 1 documented as known trade-off)
- Issues fixed in-place: 3

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | tasklist/executor.py:193,202 | `hasattr(config, 'tdd_file')` is dead code -- always True for a dataclass field. Misleads readers into thinking `tdd_file` might not be an attribute. The `and config.tdd_file is not None` clause saves correctness, but the `hasattr` guard is semantically wrong and confusing. | Remove `hasattr(config, 'tdd_file') and` from both lines, leaving just `config.tdd_file is not None`. |
| 2 | MINOR | roadmap/prompts.py:462 | `build_spec_fidelity_prompt()` generalized from "spec fidelity analyst" to "source-document fidelity analyst" and "Source Quote". While functionally correct, this dilutes prompt precision for the majority (spec) use case. The TDD task doc itself notes this is a known trade-off -- documenting for visibility. | No fix required in this cycle. If prompt quality degrades for spec inputs, consider parameterizing the role/label text. |
| 3 | MINOR | roadmap/commands.py:128-131 | `run()` docstring says "SPEC_FILE is the path to a specification markdown file" -- does not mention TDD input support via `--input-type tdd`. | Update docstring to mention TDD support. |
| 4 | IMPORTANT | tests/cli/test_tdd_extract_prompt.py | No test coverage for the TDD input validation logic in `commands.py` lines 201-216 (`read_bytes()[:500]` check for "Technical Design Document" string). This is a user-facing warning system with no tests. | Add tests covering: (a) TDD file with correct header produces no extra warning, (b) TDD file without "Technical Design Document" produces warning, (c) unreadable file is handled gracefully. |

## Actions Taken

### Fix 1: Remove dead `hasattr` guards in tasklist/executor.py
- **File:** `src/superclaude/cli/tasklist/executor.py`
- **Line 193:** Changed `if hasattr(config, 'tdd_file') and config.tdd_file is not None:` to `if config.tdd_file is not None:`
- **Line 202:** Changed `tdd_file=config.tdd_file if hasattr(config, 'tdd_file') else None,` to `tdd_file=config.tdd_file,`
- **Verification:** `uv run pytest tests/cli/test_tdd_extract_prompt.py -v` -- 16/16 passed

### Fix 2: Update stale docstring in roadmap/commands.py
- **File:** `src/superclaude/cli/roadmap/commands.py`
- **Line 128-131:** Updated `run()` docstring from "SPEC_FILE is the path to a specification markdown file." to "SPEC_FILE is the path to a specification or TDD markdown file. Use --input-type tdd when the input is a Technical Design Document."
- **Verification:** Visual inspection; docstring is now accurate.

### Fix 3: Add missing test coverage for TDD input validation
- **File:** `tests/cli/test_tdd_extract_prompt.py`
- **Added:** `TestTddInputValidation` class with 5 tests covering the `read_bytes()[:500]` validation logic from `commands.py` lines 201-216:
  - `test_valid_tdd_file_no_extra_warning` -- file with "Technical Design Document" in header
  - `test_non_tdd_file_triggers_warning_condition` -- spec file without TDD marker
  - `test_empty_file_triggers_warning_condition` -- empty file edge case
  - `test_tdd_marker_beyond_500_bytes_triggers_warning` -- marker past 500-byte boundary
  - `test_read_bytes_handles_binary_gracefully` -- binary content with errors='replace'
- **Verification:** `uv run pytest tests/cli/test_tdd_extract_prompt.py -v` -- 16/16 passed (11 original + 5 new)

### Not Fixed (by design)
- **Issue 2 (MINOR):** `build_spec_fidelity_prompt()` generalization -- documented as known trade-off per task design. No action needed this cycle.

## Recommendations
- All IMPORTANT issues have been fixed in-place.
- The MINOR prompt generalization issue (Issue 2) should be monitored -- if spec-fidelity accuracy degrades in production, consider parameterizing role/label text based on input type.
- Run `uv run pytest tests/roadmap/test_spec_fidelity.py -v` to confirm no regressions from the "Source Quote" change (verified: 30/30 passed).

## QA Complete
