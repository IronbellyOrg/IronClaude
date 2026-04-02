# QA Report -- Adversarial QA Round 5, Agent 9

**Topic:** TDD/PRD Pipeline E2E Integration
**Date:** 2026-03-28
**Phase:** doc-qualitative (adversarial deep-dive)
**Fix cycle:** N/A (report only)

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | run_semantic_layer call-site vs definition signature | FAIL | Call passes keyword args that do not exist in the function definition |
| 2 | _frontmatter_values_non_empty checks ALL fields | FAIL | Blocks on non-required optional empty fields |
| 3 | _parse_frontmatter YAML list handling | FAIL | domains_detected parsed as string, not list |
| 4 | sys.path.insert in main.py | FAIL | Unconditional sys.path mutation at import time |
| 5 | scripts hardcoded absolute paths | FAIL | /config/workspace/ path does not exist on dev machines |
| 6 | prd/tdd skills not filtered by _has_corresponding_command | FAIL | No prd.md or tdd.md command file; skills installed as standalone AND via /sc: |
| 7 | _embed_inputs no error handling for missing files | FAIL | read_text raises unhandled FileNotFoundError |
| 8 | _build_steps double auto-detection | FAIL | detect_input_type called twice on the same file |
| 9 | build_extract_prompt_tdd ignores tdd_file param | FAIL | Parameter accepted but never used in prompt body |

## Summary
- Checks passed: 0 / 9
- Checks failed: 9
- Critical issues: 3
- Important issues: 4
- Minor issues: 2

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| C-79 | CRITICAL | executor.py:671-677 vs semantic_layer.py:377-384 | **run_semantic_layer call-site signature mismatch**: The call in `_run_checkers()` passes `spec_path=str(...)`, `roadmap_path=str(...)` as keyword arguments, but `run_semantic_layer()` defines positional parameters `spec_sections: list[Any]`, `roadmap_sections: list[Any]`. The function expects parsed section objects, not file path strings. This call will always fail with a TypeError (or silently produce garbage if it somehow proceeds), meaning the semantic layer NEVER executes in convergence mode. The `except Exception` on line 680 swallows the error silently. | Fix the call-site to parse spec/roadmap into section objects before passing, OR add a path-based overload to `run_semantic_layer`. Also log the exception at WARNING level instead of silently swallowing it. |
| C-80 | CRITICAL | gates.py:110-118 | **_frontmatter_values_non_empty rejects valid frontmatter with empty optional fields**: This semantic check iterates ALL frontmatter fields and fails if ANY has an empty value. But frontmatter often contains optional fields that may legitimately be empty (e.g., `routing_fix_roadmap: `, `stable_id: `). The check is applied to GENERATE_A_GATE, GENERATE_B_GATE, SPEC_FIDELITY_GATE, and CERTIFY_GATE. If an LLM emits any frontmatter field with an empty value -- even one not in `required_frontmatter_fields` -- the gate fails. The check should only validate fields listed in the gate's `required_frontmatter_fields`, not all fields. | Modify `_frontmatter_values_non_empty` to accept the gate's required fields list and check only those, OR make it a parameterized closure that knows which fields are required. |
| C-81 | CRITICAL | gates.py:147-168, gates.py:775 | **_parse_frontmatter treats YAML lists as strings, breaking domains_detected**: `EXTRACT_GATE` requires `domains_detected` in frontmatter. LLMs emit this as `domains_detected: [backend, security, frontend]`. The `_parse_frontmatter` function splits on the first `:`, yielding value `[backend, security, frontend]` as a raw string. The `_frontmatter_values_non_empty` check calls `.strip()` on this string, which works, but any downstream consumer expecting an actual list gets a string. More critically, if the LLM emits the YAML list across multiple lines (indented block style), `_parse_frontmatter` silently drops continuation lines because it only processes `key: value` lines. This means `domains_detected` could appear missing even when present, causing the EXTRACT_GATE to fail spuriously. | Use `yaml.safe_load` for frontmatter parsing instead of hand-rolled line splitting, or at minimum handle YAML block-style lists by detecting indented continuation lines. |
| I-01 | IMPORTANT | executor.py:844-856 vs executor.py:1821-1823 | **Double auto-detection of input_type**: `execute_roadmap()` at line 1821 resolves `input_type=auto` to a concrete type and replaces the config. Then `_build_steps()` at line 853-856 checks again if `effective_input_type == "auto"` and calls `detect_input_type()` a second time. Since `execute_roadmap` already replaced it, the second check is dead code. However, if `_build_steps` is ever called directly (e.g., in tests or dry-run paths that bypass `execute_roadmap`), the auto-detection still works. The real issue: the `config = dataclasses.replace(...)` on line 859 creates a NEW config object that is NOT propagated back to the caller (it shadows the parameter). If `_build_steps` is called from `execute_roadmap`, the config in `execute_roadmap` still has the OLD resolved type, and `_save_state` will save the pre-`_build_steps` config. | Remove the redundant detection in `_build_steps` since `execute_roadmap` already resolves it, OR have `_build_steps` return the modified config alongside the steps. |
| I-02 | IMPORTANT | main.py:13 | **sys.path.insert(0, ...) at import time pollutes sys.path**: Line 13 unconditionally inserts the grandparent directory of `main.py` into `sys.path[0]` every time the module is imported. Since `main.py` is imported by the package's CLI entry point, this runs for every `superclaude` CLI invocation. It pushes `src/` (or the installed package root) to the front of `sys.path`, potentially shadowing system packages with same-named modules. This is a development convenience that should not be in production code -- the package is installed via pip/pipx and does not need path manipulation. | Remove the `sys.path.insert` line. The package is installed as `superclaude` and `from superclaude import __version__` works without path manipulation. If needed for development, guard with `if __name__ == "__main__"`. |
| I-03 | IMPORTANT | executor.py:134-147 | **_embed_inputs raises unhandled FileNotFoundError**: `_embed_inputs` calls `Path(p).read_text(encoding="utf-8")` on each input path without try/except. If any input file does not exist (e.g., extraction.md before the extract step runs, or a deleted --tdd-file), the entire step crashes with an unhandled exception. The function is called from `roadmap_run_step` (line 509) which has no exception handling around it for this case. | Wrap the read_text call in try/except FileNotFoundError, log a warning, and either skip the missing file or return an error result. |
| I-04 | IMPORTANT | prompts.py:184-189 | **build_extract_prompt_tdd accepts tdd_file parameter but never uses it**: The function signature includes `tdd_file: Path | None = None` but the function body never references `tdd_file`. The parameter is passed from `_build_steps` (executor.py:903) but has no effect on the prompt. If the intent is to mention the TDD file path in the prompt (for context about what's being extracted), the parameter is silently ignored. Note: this is distinct from C-05 (dead tdd_file in generate builders) -- this is about the TDD *extraction* prompt itself. | Either use `tdd_file` in the prompt body (e.g., to reference the source document name) or remove the parameter. |
| M-01 | MINOR | scripts/run-fidelity-batch.sh:17, scripts/run-fidelity-batch-refactored.sh:14 | **Scripts use hardcoded /config/workspace/ path**: Both fidelity batch scripts hardcode `BASE="/config/workspace/IronClaude/.dev/releases/complete"`, which is a container-specific path. These scripts will not work on developer machines without modification. | Parameterize BASE as a command-line argument or derive from `$SCRIPT_DIR`. |
| M-02 | MINOR | install_skills.py:19-29 | **New prd/tdd skills not filtered by _has_corresponding_command**: `_has_corresponding_command` checks for `src/superclaude/commands/{name}.md` to filter sc-* prefixed skills. The new `prd` and `tdd` skills do NOT have the `sc-` prefix, so they pass through the filter and are installed as standalone skills to `~/.claude/skills/`. However, they are ALSO loaded via `/sc:prd` and `/sc:tdd` skill dispatching (visible in the skills list in system-reminder). This means they may appear twice in autocomplete or session context. The filter logic only catches `sc-` prefixed skills, not skills that happen to share names with available `/sc:` commands. | Extend `_has_corresponding_command` to also check for non-sc-prefixed skills that have corresponding /sc: command mappings, or document this as intentional. |

## Actions Taken
None (report-only mode).

## Recommendations
1. **C-79 is the highest priority**: The semantic layer in convergence mode is completely broken due to the call-site passing strings where section objects are expected. This means convergence-mode fidelity checks have no semantic layer -- only structural checkers run.
2. **C-80 and C-81 can cause spurious gate failures**: Any LLM output with an empty optional frontmatter field or a block-style YAML list will fail gates that should pass. These are production-impacting.
3. **I-01 through I-04** should be addressed before the pipeline is considered E2E-complete.

## QA Complete
