# Adversarial QA Report -- Agent 6: Edge Cases, Error Paths, and Untested Combinations

**Date:** 2026-03-28
**Phase:** Adversarial Round 3, Agent 6
**Focus:** Edge cases, error paths, unusual flag combinations, encoding issues, concurrency, prompt quality, template correctness, downstream pipeline awareness
**Fix Authorization:** Report only (no fixes)

---

## Overall Verdict: FAIL

---

## Issues Found

### E-01: Dead `tdd_file` parameter in `build_extract_prompt()` (spec path)

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/prompts.py` |
| **Lines** | 82-87, 147 (end of function body) |
| **Issue** | `build_extract_prompt()` accepts a `tdd_file: Path | None = None` parameter but never uses it anywhere in the function body. The spec-mode extract prompt only conditionally appends blocks for `retrospective_content` (line 149) and `prd_file` (line 160). The `tdd_file` parameter is silently ignored. This means when a user passes `--tdd-file` with a spec-type primary input, the TDD file is included in step inputs (embedded as file content) but the prompt gives the LLM no instructions on how to use TDD supplementary context during spec extraction. The LLM sees the TDD content embedded but has no guidance for what to do with it. |
| **Required Fix** | Either (a) add a conditional block in `build_extract_prompt()` analogous to the `prd_file` block that instructs the LLM how to use TDD supplementary context for enriching spec extraction, or (b) remove the `tdd_file` parameter from `build_extract_prompt()` and stop passing it in `_build_steps()`. Option (a) is the intended design per the feature spec. |

---

### E-02: No validation of `--input-type` vs actual file content mismatch

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/executor.py` |
| **Lines** | 852-858 (`_build_steps`) |
| **Issue** | When a user forces `--input-type tdd` on a file that is actually a spec (e.g., `superclaude roadmap run spec.md --input-type tdd`), or forces `--input-type spec` on a TDD file, there is no warning or validation. The pipeline silently uses the wrong extraction prompt. For `--input-type tdd` on a spec, `build_extract_prompt_tdd()` will be used, which expects 14 sections including "Data Models and Interfaces", "API Specifications", etc. -- sections a spec file will not contain. The extraction will produce empty or hallucinated TDD-specific sections. For `--input-type spec` on a TDD, the opposite: 6 rich TDD-specific sections are lost. |
| **Required Fix** | When `--input-type` is explicitly forced (not "auto"), run `detect_input_type()` anyway and log a WARNING if the forced type disagrees with auto-detection. Example: `"WARNING: --input-type=tdd forced but auto-detection identifies input as spec. Proceeding with forced type."` This does not block execution but alerts users to potential misuse. |

---

### E-03: `_embed_inputs()` crashes on UTF-16 encoded files

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/executor.py` |
| **Lines** | 134-147 |
| **Issue** | `_embed_inputs()` calls `Path(p).read_text(encoding="utf-8")` with no error handling. If a user provides a TDD or PRD file that is UTF-16 encoded (common with some Windows tools and editors), `read_text(encoding="utf-8")` will raise `UnicodeDecodeError` and crash the pipeline with an unhelpful traceback. Note that `detect_input_type()` (line 72) correctly uses `errors="replace"` for graceful degradation, but `_embed_inputs()` does not. The same issue exists in `src/superclaude/cli/tasklist/executor.py` line 58. |
| **Required Fix** | Add `errors="replace"` to the `read_text()` call in `_embed_inputs()`, or wrap it in a try/except that catches `UnicodeDecodeError`, logs a warning, and falls back to `errors="replace"`. Apply to both the roadmap and tasklist `_embed_inputs()` functions. |

---

### E-04: Passing a PRD as primary input silently misclassifies

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/executor.py` |
| **Lines** | 60-120 (`detect_input_type`) |
| **Issue** | `detect_input_type()` returns either "tdd" or "spec" -- there is no "prd" classification. If a user runs `superclaude roadmap run prd.md`, the PRD will be classified as "spec" (it will score low on TDD signals). The pipeline will then attempt to extract functional/non-functional requirements from a PRD, which has a completely different structure (user personas, JTBD, market context, etc.). The extraction prompt is designed for release specs, not PRDs. The result will be a poor extraction with hallucinated requirement IDs and missed PRD-specific content. There is no user-facing guidance that PRDs should be passed via `--prd-file`, not as the primary input. |
| **Required Fix** | Add PRD detection signals to `detect_input_type()` (e.g., presence of "User Personas", "Jobs To Be Done", "Customer Journey Map", "Product Requirements Document" in content). When detected, either (a) return a "prd" type and handle it as an error with a clear message: `"ERROR: Input file appears to be a PRD. PRDs should be passed via --prd-file, not as the primary input. The primary input should be a spec or TDD."`, or (b) log a prominent WARNING. |

---

### E-05: Same file as both primary and supplementary produces doubled content

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/executor.py` |
| **Lines** | 917 (`_build_steps`, inputs construction) |
| **Issue** | Running `superclaude roadmap run tdd.md --prd-file tdd.md` (or `spec.md --tdd-file spec.md`) will include the same file twice in step inputs. The `_embed_inputs()` function will embed the file content twice, doubling the prompt size. There is no deduplication check on input file paths. While not a crash, it wastes ~50% of the prompt budget and may cause the prompt to exceed `_EMBED_SIZE_LIMIT`. The redundancy guard at line 862 only catches the case where `effective_input_type == "tdd"` AND `config.tdd_file` is set -- it does not catch `spec + --tdd-file=same-spec` or `tdd + --prd-file=same-tdd`. |
| **Required Fix** | Add a deduplication check in `_build_steps()` that compares resolved paths: `if config.tdd_file and config.tdd_file.resolve() == config.spec_file.resolve(): log warning and set tdd_file=None`. Same for `prd_file`. Alternatively, deduplicate in `_embed_inputs()` by resolving all paths and skipping duplicates. |

---

### E-06: No lock or advisory mechanism on `.roadmap-state.json` for concurrent runs

| Field | Value |
|-------|-------|
| **Severity** | MINOR |
| **File** | `src/superclaude/cli/roadmap/executor.py` |
| **Lines** | 1642-1649 (`write_state`) |
| **Issue** | While `write_state()` uses atomic `os.replace()` for individual writes (preventing partial writes), there is no file-level lock or advisory mechanism. Two concurrent `roadmap run` invocations targeting the same `--output` directory will race on `.roadmap-state.json`. The `_save_state` function reads existing state, merges, then writes -- a classic read-modify-write race. The `accept-spec-change` command docstring (line 249) explicitly warns about this: "Do not run concurrent roadmap operations on the same output directory." However, the `roadmap run` command has no such warning, and there is no programmatic detection or prevention. |
| **Required Fix** | Add a lockfile mechanism (`output_dir/.roadmap-lock`) using `fcntl.flock()` or a PID-based advisory lock. Alternatively, add a "concurrent execution" warning to the `roadmap run` help text matching the existing warning on `accept-spec-change`. At minimum, document the limitation. |

---

### E-07: Prompt injection via malicious PRD/TDD file content

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/executor.py` |
| **Lines** | 134-147 (`_embed_inputs`) |
| **Issue** | The `_embed_inputs()` function reads file content and wraps it in markdown fenced code blocks (`\`\`\``). However, if a malicious PRD or TDD file contains the sequence `\`\`\`\n\n<system>Ignore all previous instructions...` (breaking out of the fenced block), the injected content becomes part of the prompt itself. The `_sanitize_output()` function sanitizes LLM *output*, but there is no sanitization of *input* content before embedding. Since PRD/TDD files may come from external sources (downloaded specs, shared documents), this is a realistic attack vector. |
| **Required Fix** | Sanitize embedded file content by escaping or replacing backtick sequences that could break out of fenced blocks. For example, replace any `\`\`\`` sequence within file content with an escaped version, or use a unique fence delimiter (e.g., `\`\`\`\`\``) that is unlikely to appear in the source document. |

---

### E-08: `build_extract_prompt_tdd()` docstring claims TDD-only parameters but function signature mirrors spec version

| Field | Value |
|-------|-------|
| **Severity** | MINOR |
| **File** | `src/superclaude/cli/roadmap/prompts.py` |
| **Lines** | 184-204 |
| **Issue** | The docstring for `build_extract_prompt_tdd()` only documents `spec_file` and `retrospective_content` parameters. The `tdd_file` and `prd_file` parameters are undocumented in the docstring. Additionally, the `tdd_file` parameter is accepted but never used in the function body (same issue as E-01 but for the TDD extraction path). When `input_type=tdd`, the primary input IS the TDD, so `tdd_file` (supplementary TDD) is correctly nullified by the redundancy guard at executor line 862. However, the parameter still exists in the function signature with no documentation. |
| **Required Fix** | Either remove `tdd_file` from `build_extract_prompt_tdd()` signature (since the redundancy guard always nullifies it) or document it in the docstring with a note that it is unused when input_type=tdd. |

---

### E-09: `--agents` with empty string crashes with IndexError

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/commands.py` |
| **Lines** | 159-163, then `executor.py` line 870 |
| **Issue** | If a user passes `--agents ""` (empty string), the code at line 159 checks `if agents is not None` (it won't be None -- it will be `""`), then splits on comma: `"".split(",")` produces `[""]`. `AgentSpec.parse("")` returns `AgentSpec(model="", persona="architect")` -- a spec with an empty model string. This propagates to `config.agents = [AgentSpec("", "architect")]`. At line 870, `agent_a = config.agents[0]` gets this empty-model spec. The empty model string will be passed to `ClaudeProcess` as `--model ""`, which will likely cause a subprocess failure with an unhelpful error message. |
| **Required Fix** | Add validation in `AgentSpec.parse()` to raise `click.BadParameter` if the model string is empty. Alternatively, validate in the `run()` command before constructing `RoadmapConfig`. |

---

### E-10: PRD supplementary blocks reference hardcoded section numbers that may not exist

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/prompts.py` |
| **Lines** | 160-178 (extract), 389-403 (generate), 488-499 (score), 618-635 (spec-fidelity) |
| **Issue** | All PRD supplementary blocks reference specific PRD section numbers: "S5" (Business Context), "S6" (JTBD), "S7" (User Personas), "S12" (Scope Definition), "S17" (Legal & Compliance), "S19" (Success Metrics), "S22" (Customer Journey Map). These section numbers are hardcoded and assume a specific PRD template structure. If the user's PRD uses a different template or numbering scheme, the LLM will look for sections that don't exist (e.g., "S19" might be "Glossary" in a different template). The instructions become misleading guidance. |
| **Required Fix** | Change the section references to use section NAMES instead of numbers (or both): "the PRD's Success Metrics section (commonly S19)" or "the PRD's section titled 'Success Metrics'". This gives the LLM a fallback when section numbers don't match. Alternatively, add a caveat: "Section numbers reference the standard PRD template; adapt to the actual PRD structure if numbering differs." |

---

### E-11: `build_merge_prompt()` does not receive PRD/TDD supplementary context

| Field | Value |
|-------|-------|
| **Severity** | IMPORTANT |
| **File** | `src/superclaude/cli/roadmap/prompts.py` |
| **Lines** | 505-535 |
| **Issue** | `build_merge_prompt()` does not accept `tdd_file` or `prd_file` parameters, and the merge step in `_build_steps()` (executor.py line 974-982) does not pass supplementary files. This means the merge step -- which produces the FINAL roadmap -- has no PRD/TDD context. The score step (which selects the base variant) does have PRD context, but the actual merge that synthesizes the final document does not. The merge agent cannot verify scope boundaries, validate persona coverage, or incorporate TDD-specific design decisions because it never sees those files. |
| **Required Fix** | Add `tdd_file` and `prd_file` parameters to `build_merge_prompt()` and add supplementary blocks instructing the merge agent to preserve PRD/TDD-aligned elements from both variants. Update `_build_steps()` to pass the supplementary files in the merge step's inputs list. |

---

### E-12: TDD template `spec_type` enum and release-spec-template `spec_type` enum are out of sync

| Field | Value |
|-------|-------|
| **Severity** | MINOR |
| **File** | `src/superclaude/examples/tdd_template.md` line 16, `src/superclaude/examples/release-spec-template.md` line 26 |
| **Issue** | The TDD template lists `spec_type` enum as: `new_feature | refactoring | portification | migration | infrastructure | security | performance | docs` (8 values). The release-spec-template lists its spec_type placeholder as: `new_feature_or_refactoring_or_portification_or_migration_or_infrastructure_or_security_or_performance_or_docs` (same 8 values). However, the release-spec-template's prose header (line 4) only mentions 4 types: "New feature, refactoring, portification, infrastructure" -- missing `migration`, `security`, `performance`, and `docs`. The `detect_input_type()` function does not check `spec_type` at all, so there is no code-level conflict, but the template documentation is inconsistent. |
| **Required Fix** | Update the release-spec-template prose header (line 4) to list all 8 supported spec types, matching the YAML enum. |

---

### E-13: Step numbering comments are wrong in `_build_steps()`

| Field | Value |
|-------|-------|
| **Severity** | MINOR |
| **File** | `src/superclaude/cli/roadmap/executor.py` |
| **Lines** | 993-1003 |
| **Issue** | The comment on the test-strategy step says `# Step 8: Test Strategy` and the spec-fidelity step says `# Step 8: Spec Fidelity`. Both are labeled "Step 8". The test-strategy is actually Step 8 and spec-fidelity is Step 9 (or per the function docstring, 9 steps total). Additionally, the anti-instinct step at line 983 is labeled `# Step 7` but the wiring-verification at line 1013 has no step number. The numbering in comments is inconsistent with the "9-step pipeline" described in the module docstring. |
| **Required Fix** | Fix comment numbering: anti-instinct = Step 7, test-strategy = Step 8, spec-fidelity = Step 9, wiring-verification = Step 10 (or "trailing gate"). Update the module docstring count if needed. |

---

### E-14: `_restore_from_state` mutates `config` directly on a dataclass

| Field | Value |
|-------|-------|
| **Severity** | MINOR |
| **File** | `src/superclaude/cli/roadmap/executor.py` |
| **Lines** | 1725, 1742, 1751, 1763 |
| **Issue** | `_restore_from_state()` mutates `config.agents`, `config.depth`, `config.tdd_file`, and `config.prd_file` directly on the dataclass instance. Meanwhile, `_build_steps()` uses `dataclasses.replace()` (line 859, 867) to avoid mutation. This inconsistency means some code paths create new config instances while others mutate in place. In `_build_steps()`, the replaced config is a local variable and the original `config` passed to `execute_roadmap()` still has `input_type="auto"` -- but `_save_state()` receives the original `config`, not the replaced one. This means `_save_state()` may record `input_type: "auto"` instead of the resolved type. |
| **Required Fix** | `_build_steps()` should return the modified config alongside the steps (or `execute_roadmap` should call `detect_input_type` before `_build_steps` and update `config` at the top level). Alternatively, have `_build_steps()` mutate `config.input_type` directly for consistency with `_restore_from_state()`. The key requirement: `_save_state()` must receive the resolved input_type, not "auto". |

---

### E-15: Guardrail instruction "do NOT treat PRD content as hard requirements" may be ineffective

| Field | Value |
|-------|-------|
| **Severity** | MINOR |
| **File** | `src/superclaude/cli/roadmap/prompts.py` |
| **Lines** | 178, 328, 403 |
| **Issue** | Multiple prompt blocks end with variations of "do NOT treat PRD content as hard requirements unless they are also stated in the specification." This is a negative instruction -- it tells the LLM what NOT to do. LLMs are known to have difficulty reliably following negative instructions, especially when the PRD content is large and contains assertive language ("MUST", "SHALL", "REQUIRED"). The guardrail is present but its effectiveness is unvalidated. If a PRD contains 50 "MUST" requirements and the spec contains 20, there is a realistic risk the LLM will treat all 50 as requirements despite the guardrail. |
| **Required Fix** | Strengthen the guardrail by (a) explicitly labeling PRD content in the embedded input with a prefix like `[PRD-ADVISORY]` before each embedded block, and (b) adding a positive instruction: "Treat the specification as the source of truth for all requirements. The PRD provides context ONLY." Consider adding a post-extraction validation check that counts requirements and flags if the count significantly exceeds what the spec alone would produce. |

---

### E-16: TDD template sentinel self-check references `complexity_score` and `complexity_class` as "may remain empty" but pipeline expects them

| Field | Value |
|-------|-------|
| **Severity** | MINOR |
| **File** | `src/superclaude/examples/tdd_template.md` |
| **Lines** | 60-68 |
| **Issue** | The sentinel self-check (lines 60-65) says "complexity_score and complexity_class may remain empty (computed by sc:roadmap)." The pipeline field consumption note (lines 67-68) says these are "Computed by sc:roadmap during extraction (not read from frontmatter). Pre-populated values are advisory only." This is internally consistent. However, `detect_input_type()` does NOT check these fields at all -- the detection is based on headings, exclusive fields (`parent_doc`, `coordinator`), section names, and type field. If a user pre-populates these fields in a spec file, it has no effect on detection. This is fine for detection, but it means the pipeline note is misleading: it says "computed by sc:roadmap" but actually the extraction LLM computes them in the extraction output, not from the template frontmatter. The template note implies sc:roadmap reads from the TDD frontmatter, which it does not. |
| **Required Fix** | Clarify the pipeline field consumption note: "Computed by the extraction step's LLM based on document content analysis. Template frontmatter values are not consumed by the pipeline." |

---

## Summary

| Metric | Count |
|--------|-------|
| Total findings | 16 |
| CRITICAL | 0 |
| IMPORTANT | 9 (E-01, E-02, E-03, E-04, E-05, E-07, E-09, E-10, E-11) |
| MINOR | 7 (E-06, E-08, E-12, E-13, E-14, E-15, E-16) |

### High-Impact Findings (Action Required)

1. **E-01 + E-08: Dead `tdd_file` parameter** -- Two prompt builders accept `tdd_file` but never use it. The LLM receives embedded TDD content with no instructions for how to process it.

2. **E-07: Prompt injection via embedded file content** -- No sanitization of backtick sequences in user-provided files. Fenced code blocks can be escaped by crafted input.

3. **E-11: Merge step lacks PRD/TDD context** -- The final roadmap synthesis step has no access to supplementary business or technical context, creating a gap in the pipeline's context chain.

4. **E-14: `_save_state` may record `input_type: "auto"`** -- The dataclass replacement in `_build_steps` is local. The original config with `input_type: "auto"` may reach `_save_state`, causing downstream consumers (tasklist validate) to re-run auto-detection unnecessarily.

5. **E-04: PRD as primary input silently misclassifies** -- No detection or warning when a PRD file structure is passed as the primary input.

---

## QA Complete
