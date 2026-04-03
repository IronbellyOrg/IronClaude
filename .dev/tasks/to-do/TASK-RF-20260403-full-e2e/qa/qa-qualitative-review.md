# QA Report -- Task Qualitative Review

**Topic:** E2E Pipeline Tests -- Full Roadmap + Tasklist Generation + Validation
**Date:** 2026-04-02
**Phase:** task-qualitative
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Gate/command dry-run | PASS | Verified all CLI commands referenced in Phases 1-4 against actual Click command definitions in `commands.py`. `roadmap run` accepts `--prd-file`, `--tdd-file`, `INPUT_FILES` (nargs=-1). `tasklist validate` accepts `--prd-file`, `--tdd-file`. `--input-type` choices are `[auto, tdd, spec]` per `commands.py:108`. All commands would succeed given correct fixtures. |
| 2 | Project convention compliance | PASS | Task correctly uses `uv run superclaude` throughout (never bare `superclaude`). Edits no source files (this is a verification task). Output directories are new v2 dirs avoiding overwrites. Task references `src/superclaude/cli/` source paths correctly. |
| 3 | Intra-phase execution order simulation | PASS | Phase 5 (generate TDD+PRD tasklist) runs before Phase 7 (validate against it). Phase 6 (generate Spec+PRD tasklist) runs before Phase 8 (validate). Phase 7 item 7.3 copies fidelity report before 7.4 overwrites it. Phase 8 item 8.1 copies backup before 8.2 overwrites. Execution order is sound. |
| 4 | Function signature verification | PASS | Verified `build_tasklist_generate_prompt(roadmap_file, tdd_file=None, prd_file=None)` at `tasklist/prompts.py:151`. Verified `build_tasklist_fidelity_prompt(roadmap_file, tasklist_dir, tdd_file=None, prd_file=None)` at `tasklist/prompts.py:17`. Verified `_route_input_files(input_files, explicit_tdd, explicit_prd, explicit_input_type)` at `executor.py:188`. Verified `detect_input_type(spec_file)` at `executor.py:63`. All match task descriptions. |
| 5 | Module context analysis | PASS | Verified `_OUTPUT_FORMAT_BLOCK` is imported from `roadmap/prompts.py` into `tasklist/prompts.py:14`. Verified `TASKLIST_FIDELITY_GATE` is imported in `tasklist/executor.py:28`. Verified `_collect_tasklist_files` uses `glob("*.md")` at `executor.py:44`. Module-level patterns are accounted for. |
| 6 | Downstream consumer analysis | FAIL | **IMPORTANT finding.** See Issue #1 below. `_collect_tasklist_files` at `executor.py:44` collects ALL `.md` files in the output directory, not just tasklist phase files. When validation runs on `test1-tdd-prd-v2/`, it will embed `extraction.md`, `roadmap.md`, `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `roadmap-opus-architect.md`, `roadmap-haiku-architect.md`, `wiring-verification.md`, `anti-instinct-audit.md` AND the tasklist files into the prompt. The task does not acknowledge or account for this. |
| 7 | Test validity | PASS | Phase 1 items verify fixtures with `wc -l` and `grep` against actual content. Phase 2 items dry-run actual CLI commands. Phases 3-4 run real pipeline processes. Phase 5-6 invoke real skill. Phase 8 item 8.5 directly tests `build_tasklist_generate_prompt` with 4 scenarios. All verification is substantive. |
| 8 | Test coverage of primary use case | PASS | The primary use case (full pipeline: roadmap + tasklist generation + validation) is tested end-to-end across Phases 3-8. Both TDD+PRD and Spec+PRD paths are covered. Cross-run comparison in Phase 9 verifies enrichment deltas. |
| 9 | Error path coverage | PASS | Phase 7 items 7.4 (nonexistent auto-wired file) and 7.5 (no state file) test degradation paths. Phase 2 item 2.4 tests redundancy guard. Phase 1 item 1.4 tests invalid `--input-type prd`. |
| 10 | Runtime failure path trace | FAIL | **IMPORTANT finding.** See Issue #2 below. Item 8.2 attempts to use `/dev/null` as `--tdd-file` and `--prd-file` but these Click options have `exists=True` validation. While `/dev/null` passes `Path.exists()` on macOS (confirmed: it's a character device), it's a zero-byte file that will cause `_embed_inputs` to embed empty content. The task acknowledges the Click issue but does not fully analyze the behavior. More critically: the auto-wire from `.roadmap-state.json` will STILL inject the real `tdd_file` and `prd_file` paths even when `/dev/null` is passed as explicit flags -- because the explicit flag overrides happen in `tasklist/commands.py` BEFORE auto-wire runs. Actually, re-reading the code: explicit flags are checked first (lines 63-73), then auto-wire runs only for flags that are still None (lines 117-159). So passing `/dev/null` does suppress auto-wire correctly. The test intent is sound but fragile. |
| 11 | Completion scope honesty | PASS | Open questions AI-1, TG-1, TG-2, VE-1 all have corresponding verification phases (10, 5-6, 5, 8). Deferred work items (CLI generate command, anti-instinct fix, --input-type prd) are appropriately marked as out of scope. |
| 12 | Ambient dependency completeness | PASS | No code modifications are made. All skill/CLI/function dependencies are correctly referenced. The `/sc:tasklist` skill is correctly identified at `.claude/skills/sc-tasklist-protocol/SKILL.md`. The `build_tasklist_generate_prompt` is correctly identified at `tasklist/prompts.py`. |
| 13 | Kwarg sequencing red flags | PASS | No new kwargs or parameters are being added. This is a verification task that exercises existing code paths. |
| 14 | Function existence claims -- verification | PASS | Verified via Grep: `detect_input_type` exists at `executor.py:63`, `_route_input_files` at `executor.py:188`, `build_tasklist_generate_prompt` at `tasklist/prompts.py:151`, `build_tasklist_fidelity_prompt` at `tasklist/prompts.py:17`, `_collect_tasklist_files` at `tasklist/executor.py:37`, `_save_state` at `executor.py:1834`, `read_state` at `executor.py:2109`. All exist. |
| 15 | Cross-reference accuracy for templates | PASS | No template modifications in this task. Task correctly references EXTRACT_TDD_GATE (19 fields, verified at `gates.py:797-820`), EXTRACT_GATE (13 fields, verified at `gates.py:765-793`). Skill argument-hint `"<roadmap-path> [--spec <spec-path>] [--output <output-dir>]"` verified at SKILL.md line 9. |

---

## Summary

- Checks passed: 13 / 15
- Checks failed: 2
- Critical issues: 0
- Important issues: 2
- Minor issues: 1
- Issues fixed in-place: 0

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Task items 7.1, 7.2, 8.1, 8.4 | **Tasklist validation collects ALL .md files, not just tasklists.** `_collect_tasklist_files` at `tasklist/executor.py:44` uses `glob("*.md")` on the output directory. When validation runs on `test1-tdd-prd-v2/`, it will embed ALL markdown files (extraction.md, roadmap.md, diff-analysis.md, debate-transcript.md, base-selection.md, roadmap-opus-architect.md, roadmap-haiku-architect.md, anti-instinct-audit.md, wiring-verification.md, test-strategy.md, spec-fidelity.md, AND tasklist-index.md + phase-*.md). This inflates the prompt with ~15 non-tasklist files. The task should acknowledge this behavior and either: (a) add a `--tasklist-dir` flag pointing to a subdirectory, or (b) note that all .md files get embedded and verify the validator still produces meaningful results despite the noise. The fidelity report quality could be degraded by non-tasklist content in the prompt. | Add a note in Phase 7 and 8 descriptions acknowledging that `_collect_tasklist_files` includes all `.md` files in the output directory. Consider whether items should use `--tasklist-dir` to point at a subdirectory, or add verification that the fidelity report specifically references tasklist files (not extraction.md or roadmap.md) as the downstream artifact. |
| 2 | IMPORTANT | Task item 8.2 | **Baseline test approach is fragile and may not achieve intended isolation.** Item 8.2 attempts to pass `/dev/null` as `--tdd-file` and `--prd-file` to suppress enrichment, but: (a) `/dev/null` is a character device, not a regular file -- behavior when `_embed_inputs` reads it is a zero-byte string, which may cause unexpected prompt construction; (b) the task acknowledges this might fail and suggests using "a minimal dummy file" as alternative but does not specify what that file would contain or where it would be; (c) a cleaner approach would be to create explicit empty stub files or simply omit the flags entirely and verify auto-wire doesn't kick in (which it will since `.roadmap-state.json` exists). The test needs a concrete, reliable approach to suppress enrichment. | Replace the `/dev/null` approach with one of: (a) Create minimal stub .md files (e.g., `echo "---\nstub: true\n---" > /tmp/stub.md`) and pass those as `--tdd-file /tmp/stub.md --prd-file /tmp/stub.md`, or (b) Move/rename `.roadmap-state.json` temporarily, then run `uv run superclaude tasklist validate` without any supplementary flags, then restore the state file. Approach (b) is cleaner and more reliable. |
| 3 | MINOR | Task item 5.1 / skill argument-hint | **Skill argument-hint does not list `--prd-file`.** The skill's `argument-hint` in SKILL.md frontmatter is `"<roadmap-path> [--spec <spec-path>] [--output <output-dir>]"` and does NOT include `--prd-file`. The task instructs invoking the skill with `--prd-file` in the args string. While the skill body (section 4.1b) does describe `--prd-file` handling, the argument-hint mismatch could cause confusion. The skill protocol will likely still parse `--prd-file` from the args since it reads the full args string, but this is undocumented in the hint. | Add a note in item 5.1 acknowledging the argument-hint omission and stating that `--prd-file` is supported per section 4.1b of the skill protocol even though not in the argument-hint. Alternatively, update the skill's argument-hint to include `[--prd-file <prd-path>]`. |

---

## Actions Taken

No fixes applied. Fix authorization was granted but the issues found are in the task file's instructions/assumptions, not in code that can be silently fixed. The issues require task author decision on approach.

---

## Confidence Gate

### Item Categorization

- [x] 1. Gate/command dry-run -- Verified via Read/Grep of `commands.py`, `executor.py`, `prompts.py`
- [x] 2. Project convention compliance -- Verified all `uv run` patterns and output paths in task
- [x] 3. Intra-phase execution order -- Traced dependencies across all 12 phases, verified copy-before-overwrite patterns
- [x] 4. Function signature verification -- Grep-verified all function signatures in `prompts.py`, `executor.py`, `commands.py`
- [x] 5. Module context analysis -- Read imports in `tasklist/prompts.py`, `tasklist/executor.py`
- [x] 6. Downstream consumer analysis -- Read `_collect_tasklist_files` at `executor.py:37-49`, traced how it feeds into `_build_steps`
- [x] 7. Test validity -- Reviewed all verification items across Phases 1-8 for substantive testing
- [x] 8. Test coverage -- Confirmed both TDD+PRD and Spec+PRD paths exercised end-to-end
- [x] 9. Error path coverage -- Reviewed items 7.4, 7.5, 2.4, 1.4 for degradation testing
- [x] 10. Runtime failure path trace -- Traced `/dev/null` through Click validation, auto-wire logic, `_embed_inputs`
- [x] 11. Completion scope honesty -- Cross-referenced Open Questions with verification phases
- [x] 12. Ambient dependency completeness -- Verified all referenced files, functions, skills exist
- [x] 13. Kwarg sequencing -- Confirmed no new kwargs introduced (verification task)
- [x] 14. Function existence verification -- Grep-verified all claimed functions: `detect_input_type`, `_route_input_files`, `build_tasklist_generate_prompt`, `build_tasklist_fidelity_prompt`, `_collect_tasklist_files`, `_save_state`, `read_state`
- [x] 15. Cross-reference accuracy -- Verified EXTRACT_TDD_GATE (19 fields), EXTRACT_GATE (13 fields), skill argument-hint

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

**Tool engagement:** Read: 18 | Grep: 12 | Glob: 2 | Bash: 4

### Self-Audit

1. **How many factual claims independently verified against source code?** 23+ claims verified: function signatures (7), gate field counts (2), Click option definitions (5), skill argument-hint (1), fixture file existence and line counts (3), state file field storage (3), redundancy guard message (1), `_collect_tasklist_files` glob pattern (1).
2. **What specific files read to verify claims?** `src/superclaude/cli/tasklist/commands.py` (full), `src/superclaude/cli/tasklist/executor.py` (full), `src/superclaude/cli/tasklist/prompts.py` (full), `src/superclaude/cli/roadmap/commands.py` (full), `src/superclaude/cli/roadmap/executor.py` (partial -- _route_input_files, _save_state, read_state, detect_input_type), `src/superclaude/cli/roadmap/gates.py` (partial -- EXTRACT_GATE, EXTRACT_TDD_GATE), `src/superclaude/cli/roadmap/prompts.py` (partial -- _OUTPUT_FORMAT_BLOCK), `.claude/skills/sc-tasklist-protocol/SKILL.md` (partial -- argument-hint, sections 4.1a-4.1c), `.dev/test-fixtures/test-prd-user-auth.md` (grep for personas), `.dev/test-fixtures/` directory listing.
3. **If 0 issues found, why trust thoroughness?** N/A -- 3 issues found. The issues are non-obvious: Issue #1 required reading `_collect_tasklist_files` implementation and reasoning about which files exist in the output directory after a full pipeline run. Issue #2 required testing `/dev/null` on macOS and tracing the Click validation + auto-wire interaction. Issue #3 required comparing skill argument-hint to skill body behavior.

---

## Recommendations

1. **Issue #1 (IMPORTANT):** The `_collect_tasklist_files` behavior of globbing all `.md` files is a pre-existing design concern in the validation executor. For this task, the pragmatic fix is to add `--tasklist-dir` pointing to a subdirectory (if the skill outputs to one) or add notes acknowledging the behavior. If the skill writes `phase-*.md` and `tasklist-index.md` into the same directory as `roadmap.md`, the validator will embed everything. The fidelity report may still be usable (the LLM can distinguish roadmap from tasklist content), but the task should set explicit expectations about this.

2. **Issue #2 (IMPORTANT):** Replace the `/dev/null` approach with a reliable baseline isolation method. Recommend temporarily renaming `.roadmap-state.json` before the baseline run and restoring it after, then omitting `--tdd-file` and `--prd-file` flags entirely. This cleanly isolates the baseline.

3. **Issue #3 (MINOR):** Update the skill's `argument-hint` to `"<roadmap-path> [--spec <spec-path>] [--prd-file <prd-path>] [--output <output-dir>]"` for consistency with skill body behavior. This is a one-line fix in SKILL.md frontmatter.

---

## QA Complete
