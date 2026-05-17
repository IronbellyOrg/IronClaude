# QA Report -- Adversarial Qualitative Review

**Topic:** PRD Pipeline Integration Implementation
**Date:** 2026-03-28
**Phase:** prd-qualitative (adversarial)
**Fix cycle:** N/A (report-only, no fixes authorized)

---

## Overall Verdict: FAIL

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | End-to-end wiring: prd_file CLI->model->config->executor->prompt (roadmap) | PASS | Verified chain: commands.py L117-122 -> config_kwargs L196 -> executor _build_steps passes config.prd_file to all 7 enriched builders + adds to step inputs |
| 2 | End-to-end wiring: tdd_file CLI->model->config->executor->prompt (roadmap) | PASS | commands.py L112-116 -> config_kwargs L195 -> executor _build_steps passes config.tdd_file |
| 3 | End-to-end wiring: prd_file CLI->model->config->executor->prompt (tasklist) | PASS | commands.py L67-72 -> config L156-157 -> executor _build_steps passes config.prd_file to prompt builder + adds to inputs |
| 4 | Prompt builder consistency: all enriched builders use prd_file param | FAIL | See Issue #1 -- 6 builders accept tdd_file but never use it |
| 5 | Prompt builder consistency: P3 stub builders have params | PASS | build_diff_prompt, build_debate_prompt, build_merge_prompt all accept tdd_file and prd_file |
| 6 | Prompt builder consistency: P3 stubs unused params wired by executor | FAIL | See Issue #2 -- executor never passes tdd_file/prd_file to diff, debate, merge |
| 7 | Prompt builder consistency: P3 stubs never use params | PASS/expected | Per research report Phase 3.3, these are API-only stubs with no supplementary blocks. This is by design. |
| 8 | Auto-wire: state file stores tdd_file and prd_file | PASS | executor.py _save_state L1437-1438 writes both to state |
| 9 | Auto-wire: tasklist reads state correctly | PASS | tasklist/commands.py L113-146 reads and validates both |
| 10 | Auto-wire: roadmap resume reads state correctly | PASS | executor.py _restore_from_state L1741-1761 handles both |
| 11 | Auto-wire: explicit CLI override works | PASS | Both auto-wire blocks check `if tdd_file is None` / `if config.tdd_file is None` before reading state |
| 12 | Auto-wire: missing file warning | PASS | Both tasklist (L128-131, L143-146) and roadmap (L1750, L1761) emit warnings |
| 13 | Redundancy guard fires correctly | PASS | executor.py L858-864 checks effective_input_type == "tdd" and config.tdd_file is not None |
| 14 | Redundancy guard uses dataclasses.replace | PASS | L864: config = dataclasses.replace(config, tdd_file=None) |
| 15 | Redundancy guard for auto-detected TDD | PASS | Guard fires after detect_input_type resolves "auto" to "tdd" (L853-856) |
| 16 | Skill docs match CLI behavior: extraction-pipeline.md | PASS | Correctly describes PRD as conditional enrichment, state persistence |
| 17 | Skill docs match CLI behavior: scoring.md | PASS | Correctly states PRD uses standard 5-factor, no new scoring factors |
| 18 | Skill docs match CLI behavior: tasklist SKILL.md | FAIL | See Issue #5 -- skill docs describe generation enrichment behavior that has no executor wiring |
| 19 | spec-panel.md Steps 6c-6d | PASS | Steps 6c (PRD detection) and 6d (PRD downstream frontmatter) present and consistent |
| 20 | Test coverage: scenarios A-D for all enriched builders | PASS | Tests cover all 4 scenarios for extract, extract_tdd, generate, score, spec-fidelity, test-strategy |
| 21 | Test coverage: auto-wire tests | FAIL | See Issue #7 -- tests reimplement logic instead of testing actual commands.py code path |
| 22 | Test coverage: build_tasklist_generate_prompt | PASS | All 4 scenarios + interaction note + baseline tested |
| 23 | Test coverage: integration / E2E | FAIL | See Issue #8 -- no integration test invoking actual pipeline end-to-end |
| 24 | Test coverage: negative / edge cases | FAIL | See Issue #9 -- no tests for wrong document type, empty files, same file for both flags |
| 25 | Prompt section references accurate | PASS | PRD section numbers (S5, S6, S7, S12, S17, S19, S22, S23) correctly referenced |
| 26 | build_score_prompt test call signature | FAIL | See Issue #10 -- test passes wrong positional args |
| 27 | build_spec_fidelity_prompt test call signature | FAIL | See Issue #11 -- test passes wrong positional args |
| 28 | build_test_strategy_prompt test call signature | FAIL | See Issue #12 -- test passes args in wrong order |
| 29 | build_tasklist_generate_prompt executor wiring | FAIL | See Issue #3 -- function exists but is never called by any executor |
| 30 | Diff/debate/merge step inputs include prd_file | FAIL | See Issue #4 -- these steps never get prd_file in their inputs list |
| 31 | Design coherence: research report vs implementation | FAIL | See Issue #6 -- multiple deviations from research plan |
| 32 | Cross-cutting: hardcoded "spec" references | PASS | build_spec_fidelity_prompt already says "source specification or TDD file" |

---

## Summary

- Checks passed: 19 / 32
- Checks failed: 13
- Critical issues: 3
- Important issues: 7
- Minor issues: 3
- Issues fixed in-place: 0 (not authorized)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `roadmap/prompts.py` all 6 enriched builders | **Dead `tdd_file` parameter in 6 prompt builders.** `build_extract_prompt` (L82), `build_extract_prompt_tdd` (L184), `build_generate_prompt` (L334), `build_score_prompt` (L463), `build_spec_fidelity_prompt` (L541), `build_test_strategy_prompt` (L702) all accept `tdd_file: Path | None = None` as a parameter but NEVER reference it in the function body. The parameter is purely cosmetic -- passing a TDD file to these builders does nothing. The executor passes `config.tdd_file` to all of these, and it silently vanishes. This is not a regression (it was dead before too), but the implementation creates a false impression that TDD supplementary content enriches these prompts when it does not. | Either (a) add conditional TDD supplementary blocks to builders where TDD content would be valuable (extract, generate, spec-fidelity, test-strategy), or (b) remove the `tdd_file` parameter from builders that don't use it and stop passing it from the executor, or (c) document explicitly that `tdd_file` is an API-only stub for future use. Option (b) is cleanest -- API-only stubs that do nothing are misleading. |
| 2 | MINOR | `roadmap/executor.py` L940-978 | **Executor does not pass tdd_file/prd_file to diff, debate, merge builders.** The executor calls `build_diff_prompt(roadmap_a, roadmap_b)`, `build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth)`, and `build_merge_prompt(score_file, roadmap_a, roadmap_b, debate_file)` without passing `tdd_file` or `prd_file`. These are P3 API-only stubs per research report Phase 3.3, so this is by design. However, the executor also does NOT include `config.prd_file` or `config.tdd_file` in the `inputs` list for diff, debate, and merge steps. This is correct per P3 design -- these steps don't need source documents since they operate on derived artifacts. Rating as MINOR for documentation gap: the code should have a comment explaining why these steps intentionally omit supplementary inputs. | Add inline comments to the diff/debate/merge Step definitions in `_build_steps` explaining that supplementary files are intentionally omitted per P3 design (these steps operate on pipeline-internal artifacts, not source documents). |
| 3 | CRITICAL | `tasklist/prompts.py` L144 + `tasklist/executor.py` | **`build_tasklist_generate_prompt` is dead code -- defined, tested, documented, but never called.** The function exists at L144-224 of `tasklist/prompts.py` with full TDD, PRD, and combined enrichment blocks. It is imported by `tests/tasklist/test_prd_prompts.py` and tested across all 4 scenarios. The tasklist SKILL.md describes generation enrichment behavior (Sections 3.x, 4.4a, 4.4b) that this function would implement. However, `build_tasklist_generate_prompt` is NEVER imported or called by `tasklist/executor.py` or any other executor. The tasklist executor only builds a single `tasklist-fidelity` step using `build_tasklist_fidelity_prompt`. There is no `tasklist-generate` step. The function, its tests, and its skill docs describe behavior that cannot be triggered through the CLI. | Either (a) wire `build_tasklist_generate_prompt` into a new generation step in the tasklist executor that actually uses it, or (b) if generation is handled by the inference-based skill protocol (not the CLI pipeline), document this clearly in the function's docstring and the SKILL.md, noting that the function is provided for skill-based workflows and is not invoked by the CLI executor. The current state is misleading: tests pass, docs describe behavior, but the CLI never produces this output. |
| 4 | IMPORTANT | `roadmap/executor.py` L940-978 | **Diff, debate, and merge steps omit prd_file from `inputs` list even though they include it in the prompt builder signature.** While P3 stubs intentionally have no supplementary prompt blocks, the `inputs` list controls which files are embedded inline for the LLM to read. If a future P3 upgrade adds PRD blocks, the files won't be embedded unless `inputs` is also updated. This creates a latent inconsistency: the API says "I accept prd_file" but the pipeline never provides the file content. | Accept this as a known P3 limitation and add a `# P3: inputs intentionally omit supplementary files` comment. When P3 stubs are upgraded to P1/P2, both the prompt builder body AND the step inputs list must be updated simultaneously. |
| 5 | IMPORTANT | `tasklist SKILL.md` Sections 3.x, 4.4a, 4.4b | **Skill docs describe tasklist generation enrichment that has no CLI execution path.** Section 3.x "Source Document Enrichment" describes enrichment behavior during tasklist generation. Sections 4.4a and 4.4b describe supplementary task generation from TDD and PRD. The CLI `tasklist` command only has a `validate` subcommand -- there is no `generate` subcommand. The enrichment described in the skill docs can only be triggered through the inference-based skill protocol, not through `superclaude tasklist`. The SKILL.md does not distinguish between CLI-executable and skill-only behaviors. | Add a clear note in SKILL.md Sections 3.x, 4.4a, and 4.4b indicating that generation enrichment is a skill-protocol behavior, not a CLI pipeline behavior. The CLI `tasklist validate` command supports PRD/TDD enrichment for validation only. Generation enrichment requires invoking the skill protocol directly. |
| 6 | IMPORTANT | Implementation vs research report | **Multiple deviations from research report implementation plan.** The research report (Section 8, Phase 3.3) specifies that P3 stubs should have "prd_file parameter only, no supplementary blocks, no executor wiring changes." The implementation adds both `tdd_file` AND `prd_file` parameters (not just prd_file). The research report (Section 8, Phase 2) specifies that `build_generate_prompt` should be "refactored to base pattern." The implementation adds a conditional `prd_file` block but does not clearly delineate what "base pattern" refactoring was done -- the function still uses string concatenation, which may be the intended pattern. The research report (Section 4, Gap G-13) rates diff/debate/merge as LOW priority, which matches P3 status. However, the implementation adds `tdd_file` params to these stubs that the research never specified. | Document the deviations in the task's final report. The `tdd_file` additions to P3 stubs and enriched builders are harmless (dead params) but represent scope creep beyond the research recommendation. If intentional, note it as a forward-compatibility decision. If unintentional, remove the unused `tdd_file` params from builders that don't use them. |
| 7 | IMPORTANT | `tests/tasklist/test_autowire.py` | **Auto-wire tests reimplement logic instead of testing actual code.** All tests in `TestAutoWireLogic` (L62-148) manually reimplement the auto-wire logic pattern (read state, check if None, check is_file, assign) instead of calling the actual `tasklist/commands.py` validate function or `roadmap/executor.py` `_restore_from_state` function. This means the tests verify that the pattern works in isolation, but do NOT verify that the actual code in commands.py implements the pattern correctly. If someone modifies commands.py to break the auto-wire (e.g., swaps the condition), these tests will still pass. | Refactor the auto-wire tests to either (a) use Click's CliRunner to invoke `tasklist validate` with a pre-written state file and verify the config that reaches the executor, or (b) directly call `_restore_from_state` with a real state file and verify the returned config. The current tests provide confidence in the pattern but not in the implementation. |
| 8 | IMPORTANT | `tests/` | **No integration test for end-to-end pipeline invocation.** There is no test that invokes `superclaude roadmap run spec.md --prd-file prd.md --dry-run` via CliRunner and verifies that the dry-run output includes prd_file in the step plan. The existing `test_prd_file_defaults_to_none` invokes `--dry-run` but does not check that prd_file flows through to step definitions. An integration test would catch wiring breaks between commands.py -> executor.py -> _build_steps. | Add an integration test that: (1) creates tmp spec + prd files, (2) invokes `roadmap run spec.md --prd-file prd.md --dry-run` via CliRunner, (3) verifies exit code 0, and optionally (4) patches `_build_steps` to capture and assert the config passed to it includes prd_file. |
| 9 | MINOR | `tests/` | **No tests for edge cases: wrong document type, empty files, same file for both flags.** What happens if `--prd-file` points to a TDD, `--tdd-file` points to a PRD, both flags point to the same file, or either file is empty (0 bytes)? The implementation has no validation for document type correctness -- it trusts the user to provide the right files. This is arguably acceptable (GIGO principle) but should be tested to document the behavior. | Add edge case tests or document in --help text that file content is not validated: `--prd-file` simply makes the file available as supplementary context regardless of its actual content. |
| 10 | CRITICAL | `tests/roadmap/test_prd_prompts.py` L107-112 | **`build_score_prompt` test passes arguments in wrong positional order.** The test calls `build_score_prompt(Path("a.md"), Path("b.md"), EXTRACTION)` where EXTRACTION=Path("extraction.md"). The actual function signature is `build_score_prompt(debate_path: Path, variant_a_path: Path, variant_b_path: Path, ...)`. So the test passes EXTRACTION (extraction.md) as `variant_b_path`, which is semantically wrong. The test still passes because it only checks for marker string presence/absence, not the actual prompt content referencing correct file paths. This masks a potential runtime issue: if the score prompt ever uses variant_b_path in a path-dependent way, the test would not catch it. | Fix the test to use correct positional arguments: `build_score_prompt(Path("debate.md"), Path("a.md"), Path("b.md"), prd_file=PRD)`. The function takes `debate_path, variant_a_path, variant_b_path` -- the test should match this ordering. |
| 11 | CRITICAL | `tests/roadmap/test_prd_prompts.py` L121-128 | **`build_spec_fidelity_prompt` test passes 3 positional args but function only takes 2 required positional args.** The test calls `build_spec_fidelity_prompt(SPEC, Path("roadmap.md"), EXTRACTION)` where EXTRACTION=Path("extraction.md"). The actual function signature is `build_spec_fidelity_prompt(spec_file: Path, roadmap_path: Path, tdd_file: Path | None = None, prd_file: Path | None = None)`. So the test passes EXTRACTION as `tdd_file` (not as a third required positional). This means every "baseline" test for spec-fidelity is actually running with `tdd_file=Path("extraction.md")`, not with `tdd_file=None`. The test_scenario_a_no_prd_dimensions test claims to test "baseline" but actually tests "with a tdd_file set". Since tdd_file is a dead parameter (see Issue #1), this doesn't change the output, but it means the test is not testing what it claims. | Fix the test calls to match the actual function signature: `build_spec_fidelity_prompt(SPEC, Path("roadmap.md"))` for baseline, `build_spec_fidelity_prompt(SPEC, Path("roadmap.md"), prd_file=PRD)` for PRD scenario. Remove the erroneous third positional argument. |
| 12 | IMPORTANT | `tests/roadmap/test_prd_prompts.py` L138-145 | **`build_test_strategy_prompt` test passes args in wrong order.** The test calls `build_test_strategy_prompt(EXTRACTION, Path("roadmap.md"))` but the actual signature is `build_test_strategy_prompt(roadmap_path: Path, extraction_path: Path, ...)`. So the test passes EXTRACTION as `roadmap_path` and "roadmap.md" as `extraction_path` -- the arguments are swapped. Since the function only uses these paths for type annotation (not path-dependent operations), the test still passes, but the test is documenting incorrect usage. | Fix to `build_test_strategy_prompt(Path("roadmap.md"), EXTRACTION)` to match the actual parameter order. |
| 13 | MINOR | `roadmap/executor.py` _restore_from_state L1722 | **_restore_from_state mutates config in-place for agents and depth but uses auto-wire pattern for tdd_file/prd_file.** Lines 1722 (`config.agents = restored`) and 1739 (`config.depth = saved_depth`) mutate the config dataclass in-place. Lines 1748 and 1758 also mutate in-place (`config.tdd_file = tdd_path`, `config.prd_file = prd_path`). This is inconsistent with the redundancy guard pattern (L864) which uses `dataclasses.replace` to avoid mutation. While the in-place mutation works, it could cause subtle issues if the caller retains a reference to the original config expecting it to be unmodified. | Either use `dataclasses.replace` consistently throughout `_restore_from_state` (returning a new config), or document that this function mutates the config in-place by design. The current mixed approach (replace in redundancy guard, mutate in restore) is inconsistent. |

---

## Actions Taken

None -- fix authorization is false. All issues are documented for the implementer.

---

## Recommendations

### Must fix before shipping (CRITICAL):
1. **Issue #3**: `build_tasklist_generate_prompt` is dead code with tests that create a false sense of coverage. Either wire it into an executor or document it as skill-only.
2. **Issue #10**: Fix `build_score_prompt` test argument order -- test is passing wrong file as `variant_b_path`.
3. **Issue #11**: Fix `build_spec_fidelity_prompt` test -- baseline tests are inadvertently setting `tdd_file` instead of leaving it None.

### Should fix before shipping (IMPORTANT):
4. **Issue #1**: Decide whether `tdd_file` params in 6 builders are forward-compatibility stubs or dead code. Document or remove.
5. **Issue #5**: Skill SKILL.md should distinguish CLI-executable vs skill-only behaviors.
6. **Issue #7**: Auto-wire tests should test actual code, not reimplemented patterns.
7. **Issue #8**: Add at least one integration test covering the full flag->config->builder chain.
8. **Issue #12**: Fix `build_test_strategy_prompt` test argument order.
9. **Issue #6**: Document deviations from research report recommendations.
10. **Issue #4**: Add comments explaining P3 intentional omissions in executor.

### Low priority (MINOR):
11. **Issue #2**: Add inline comments for P3 design decisions.
12. **Issue #9**: Add edge case tests or document GIGO behavior.
13. **Issue #13**: Consistency of mutation vs replace patterns.

---

## QA Complete
