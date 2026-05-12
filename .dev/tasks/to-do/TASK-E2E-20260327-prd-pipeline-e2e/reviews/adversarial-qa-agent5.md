# Adversarial QA Report -- Round 3, Agent 5

**Date:** 2026-03-28
**Scope:** Deep-dive into convergence, validation, remediation, obligation scanner, integration contracts, fingerprint, spec_patch, type annotations, thread safety, logging, and prompt interactions
**Prior findings excluded:** 41 items (C-01 through D-02, S-01 through S-03)

---

## Findings

### E-01 [IMPORTANT] -- Validation sub-pipeline has zero TDD/PRD awareness

**File:** `src/superclaude/cli/roadmap/validate_executor.py` lines 34-36, `validate_prompts.py` lines 16-75
**Evidence:** `_REQUIRED_INPUTS = ("roadmap.md", "test-strategy.md", "extraction.md")` -- the validation executor hardcodes exactly 3 input files. When `--tdd-file` or `--prd-file` is provided, those supplementary documents are embedded into extraction/generate/score/test-strategy/spec-fidelity steps but are completely invisible to the validation sub-pipeline. The `build_reflect_prompt` and `build_merge_prompt` in `validate_prompts.py` accept only `(roadmap, test_strategy, extraction)` paths and have no parameters for TDD/PRD files. The `ValidateConfig` dataclass (models.py:119-134) has no `tdd_file` or `prd_file` fields, and the `validate` CLI command (commands.py:263-337) has no `--tdd-file` or `--prd-file` options. This means the validation agents cannot verify whether PRD persona coverage, TDD data model coverage, or compliance requirements were properly addressed in the roadmap -- they literally never see those documents.
**Required fix:** Add `tdd_file` and `prd_file` fields to `ValidateConfig`, add CLI options to the `validate` command, pass them through `_validate_input_files`, and update `build_reflect_prompt` to include supplementary document dimensions.

---

### E-02 [IMPORTANT] -- Remediation sub-pipeline has zero TDD/PRD awareness

**File:** `src/superclaude/cli/roadmap/remediate_prompts.py` lines 17-76, `remediate_executor.py` lines 207-258
**Evidence:** `build_remediation_prompt(target_file, findings)` accepts only a target file and findings list. When the roadmap has TDD/PRD-derived findings (e.g., missing API endpoints from TDD, missing compliance gates from PRD), the remediation agent receives no context about the source TDD/PRD to inform its fixes. The `_run_agent_for_file` function (remediate_executor.py:208) builds the prompt and embeds only the target file content -- never the TDD or PRD. The `execute_remediation` function signature has no TDD/PRD parameters. Remediation of TDD/PRD-sourced deviations will produce lower-quality fixes because the agent has no access to the source documents that define the missing requirements.
**Required fix:** Thread `tdd_file`/`prd_file` through `execute_remediation` -> `_run_agent_for_file` -> `build_remediation_prompt` and include relevant source context in the prompt.

---

### E-03 [IMPORTANT] -- Convergence fidelity checker scans hardcoded `src/superclaude` path

**File:** `src/superclaude/cli/roadmap/executor.py` lines 685-686
**Evidence:** `source_dir = Path("src/superclaude") if Path("src/superclaude").exists() else Path(".")` -- the fidelity checker in convergence mode uses a hardcoded relative path to find the codebase to scan. This is the IronClaude project's own source directory, not the user's project. When a user runs `superclaude roadmap run` on their own project's spec, the fidelity checker will search IronClaude's source code for implementation evidence of the user's spec's FRs -- producing nonsensical results. The same hardcoded path appears at line 494 for wiring verification.
**Required fix:** Derive source directory from the spec file's location or add a `--source-dir` CLI option. At minimum, document that fidelity checking is only meaningful when running from within the IronClaude repo.

---

### E-04 [IMPORTANT] -- `_get_absolute_position` in obligation scanner uses `content.find(section_text)` which can match wrong section

**File:** `src/superclaude/cli/roadmap/obligation_scanner.py` lines 294-306
**Evidence:** The function converts a relative position within a section to an absolute content position by doing `section_start = content.find(section_text)`. When two sections share identical content (e.g., both contain "placeholder implementation"), `content.find()` will always return the FIRST occurrence, not the section the match actually belongs to. This corrupts the absolute position calculation, causing incorrect severity determination (code-block vs. prose detection) for obligations in later sections that share text with earlier sections.
**Required fix:** Track the absolute start offset of each section during `_split_into_phases` and pass it through instead of using `content.find()`.

---

### E-05 [IMPORTANT] -- `check_roadmap_coverage` in integration_contracts matches ANY wiring task to ANY contract

**File:** `src/superclaude/cli/roadmap/integration_contracts.py` lines 195-256
**Evidence:** The coverage check iterates `WIRING_TASK_PATTERNS` across ALL roadmap lines for EACH contract. If the roadmap contains a single wiring task like "wire handlers into dispatch table", that line will match the wiring pattern for EVERY contract, marking them all as covered. The function never correlates the specific mechanism named in the contract with the mechanism named in the roadmap wiring task. A roadmap that says "wire event handlers into event bus" would falsely cover a contract about "populate dispatch table with step runners." The only correlation attempt is the `_extract_identifiers` fallback, but the primary `WIRING_TASK_PATTERNS` loop has zero per-contract filtering.
**Required fix:** After matching a wiring task pattern, verify that the matched line also references the specific mechanism or component from the contract being checked (similar to the dual-condition approach in the obligation scanner's `_has_discharge`).

---

### E-06 [IMPORTANT] -- `convergence.py` regression handler copies registry but does not re-run checkers

**File:** `src/superclaude/cli/roadmap/convergence.py` lines 610-716
**Evidence:** The `handle_regression` function creates 3 independent temp directories with copies of the spec, roadmap, and registry, then loads the registry copies and reads their existing active HIGHs. But it never runs the checkers again in those temp dirs -- it just reads findings that were already in the copied registry. The 3 "agent" instances are reading the same data from the same snapshot, so the "parallel validation" produces 3 identical results. The function's docstring says "Spawns 3 agents... each running the full checker suite independently" but no checker suite is actually invoked. The `merge by stable ID` at line 676 produces the union, which is just the original set.
**Required fix:** Either (a) actually invoke `run_all_checkers` inside each validation directory, or (b) document that this is a stub awaiting real multi-agent validation and remove the misleading "3 agents" architecture.

---

### E-07 [CRITICAL] -- `_restore_from_state` mutates frozen dataclass field `depth` with invalid value

**File:** `src/superclaude/cli/roadmap/executor.py` line 1742
**Evidence:** `config.depth = saved_depth` -- `RoadmapConfig.depth` is typed as `Literal["quick", "standard", "deep"]`. The state file stores whatever string was in `config.depth` at save time, but `read_state` returns raw JSON with no validation. If the state file contains a corrupted or manually-edited depth value (e.g., `"invalid"`), it will be assigned to `config.depth` without type checking, violating the Literal type contract. This applies to `config.agents` at line 1725 as well -- while there is a `try/except` for `KeyError/TypeError`, it does not validate model/persona string contents.
**Required fix:** Validate `saved_depth in ("quick", "standard", "deep")` before assignment. Add similar validation for agent model/persona values.

---

### E-08 [IMPORTANT] -- Duplicate `_embed_inputs` and `_sanitize_output` implementations

**File:** `src/superclaude/cli/roadmap/executor.py` lines 134-147, `validate_executor.py` lines 38-46 and 49-75
**Evidence:** Both `executor.py` and `validate_executor.py` define their own `_embed_inputs` and `_sanitize_output` functions with nearly identical logic. The executor.py version of `_sanitize_output` (lines 150-205) is more robust -- it handles leading whitespace stripping before checking for `---`, while the validate_executor.py version (lines 49-75) does not strip leading whitespace. A validate step output that starts with `\n---` would fail to sanitize in validate_executor but succeed in executor. The `_embed_inputs` implementations are identical but independently maintained, creating a divergence risk.
**Required fix:** Extract shared utilities into a common module (e.g., `pipeline/prompt_utils.py`) and import from both executors.

---

### E-09 [IMPORTANT] -- `spec_patch.py` does not handle TDD/PRD file references in state

**File:** `src/superclaude/cli/roadmap/spec_patch.py` lines 162-282
**Evidence:** `prompt_accept_spec_change` reads `spec_file` from the state file and recomputes its hash, but only checks the spec file hash. When `--tdd-file` or `--prd-file` were used in the original run, changes to those supplementary files do not trigger any hash mismatch -- the spec-patch workflow has no concept of TDD/PRD file hashes. A user could modify their TDD file, run `--resume`, and the pipeline would skip steps using stale TDD content because the spec hash still matches. The state file stores `tdd_file` and `prd_file` paths (executor.py:1440-1441) but `spec_patch.py` never reads them.
**Required fix:** Compute and store hashes for `tdd_file` and `prd_file` in the state file, and check them during the accept-spec-change workflow and during resume.

---

### E-10 [IMPORTANT] -- `_write_convergence_report` hardcodes medium/low counts to 0

**File:** `src/superclaude/cli/roadmap/executor.py` lines 761-801
**Evidence:** Lines 776-777: `"medium_severity_count: 0"` and `"low_severity_count: 0"` -- the convergence report always writes zero for MEDIUM and LOW severity counts regardless of what the registry actually contains. The `DeviationRegistry` tracks findings with any severity, and the convergence engine only gates on HIGHs, but the report should still accurately reflect MEDIUM/LOW counts for user visibility. The `SPEC_FIDELITY_GATE` checks `high_severity_count` in frontmatter, so the gate still works, but the report misleads users about the actual deviation landscape.
**Required fix:** Query the registry for MEDIUM and LOW counts and write actual values.

---

### E-11 [IMPORTANT] -- Thread safety: `_active_validation_dirs` module-level mutable list

**File:** `src/superclaude/cli/roadmap/convergence.py` lines 335, 358, 370
**Evidence:** `_active_validation_dirs: list[Path] = []` is a module-level mutable list modified by `_create_validation_dirs` (append) and `_cleanup_validation_dirs` (remove). If two pipeline runs execute concurrently in the same process (e.g., via threading or async), both would share this list. One run's `_atexit_cleanup` could delete another run's temp directories. The `list.remove()` at line 370 is also not atomic and could raise `ValueError` if another thread already removed the path. Similarly, the `_FINDING_COUNTER` dead global (already found as C-33) and the module-level `SEVERITY_RULES` dict are read-only and safe, but this mutable list is not.
**Required fix:** Use a threading lock around `_active_validation_dirs` mutations, or use a `threading.local()` to scope the list per thread.

---

### E-12 [MINOR] -- `certify_prompts.py` `parse_certification_output` regex only matches `F-\d+` format

**File:** `src/superclaude/cli/roadmap/certify_prompts.py` lines 258-273
**Evidence:** The regex `(F-\d+)\s*:\s*(PASS|FAIL)\s*--\s*(.+)` only matches finding IDs in `F-NN` format. But the convergence engine produces finding IDs from `compute_stable_id` as hex strings (e.g., `fidelity-impl_gap-a3b2c1d4`), and the remediation parser produces IDs like `F-01`. If the certification step receives findings with non-`F-NN` IDs (which happens in convergence mode), the parser will fail to extract any results, causing `route_certification_outcome` to return `certified-with-caveats` with 0 findings -- a silent false failure.
**Required fix:** Broaden the regex to `([\w-]+)\s*:\s*(PASS|FAIL)\s*--\s*(.+)` to match any alphanumeric-plus-hyphen ID format.

---

### E-13 [IMPORTANT] -- `obligation_scanner.py` false positive on discharge: `_has_discharge` checks component name as substring

**File:** `src/superclaude/cli/roadmap/obligation_scanner.py` lines 258-270
**Evidence:** `has_component = component.lower() in content.lower()` -- this is a substring match. A component context of `"log"` would match against `"catalog"`, `"dialog"`, or `"prologue"` in later phases. The `_extract_component_context` function returns short backtick-delimited terms (e.g., `"api"`, `"cli"`, `"log"`) that are especially prone to substring false positives. A false discharge means a genuinely undischarged obligation would not be flagged, silently suppressing a real issue. This is distinct from C-02 (which covers anti-instinct gate blocking); this is about the scanner's internal matching accuracy.
**Required fix:** Use word-boundary matching: `re.search(rf"\b{re.escape(component.lower())}\b", content.lower())`.

---

### E-14 [IMPORTANT] -- `build_extract_prompt` passes `tdd_file` parameter but never uses it

**File:** `src/superclaude/cli/roadmap/prompts.py` lines 82-87, 160-181
**Evidence:** `build_extract_prompt(spec_file, retrospective_content, tdd_file, prd_file)` accepts a `tdd_file` parameter but the function body never references it. There is no `if tdd_file is not None:` block -- only `if prd_file is not None:` at line 160. The TDD file is passed as an input to the step (executor.py:917) so Claude receives it inline, but the prompt gives zero instructions about what to do with TDD content during standard spec extraction. The agent receives a raw TDD file embedded after the prompt with no framing. This is the exact issue noted in C-05 (dead tdd_file param) but this finding is specifically about the semantic consequence: **the TDD content is present but uninterpreted**. The extract prompt for standard spec mode should either (a) include TDD-aware instructions or (b) not embed the TDD file.
**Required fix:** Add a `if tdd_file is not None:` block similar to the PRD block, instructing the extraction agent how to use supplementary TDD context during spec extraction.

---

### E-15 [MINOR] -- `detect_input_type` reads entire file content but only needs first ~2000 lines

**File:** `src/superclaude/cli/roadmap/executor.py` lines 60-120
**Evidence:** `content = spec_file.read_text(encoding="utf-8", errors="replace")` reads the entire file. For large spec/TDD documents (10K+ lines), this is wasteful. The detection logic only examines: numbered headings (anywhere), frontmatter fields (first ~20 lines), section names (headings, so sparse), and type field (first 1000 chars). All signals can be detected from the first ~200 headings, meaning the full file read is unnecessary. Minor efficiency concern, but also means `"Technical Design Document" in content[:1000]` at line 111 only checks the first 1000 characters while the full content is in memory.
**Required fix:** Consider reading only the first N lines for detection, or document that full read is intentional.

---

### E-16 [IMPORTANT] -- `_build_steps` step numbering comment says "Step 8" for both test-strategy and spec-fidelity

**File:** `src/superclaude/cli/roadmap/executor.py` lines 993, 1003
**Evidence:** Line 993: `# Step 8: Test Strategy` and line 1003: `# Step 8: Spec Fidelity`. Both steps are labeled as "Step 8" in the comments. The actual step ordering is: extract(1), generate(2a+2b), diff(3), debate(4), score(5), merge(6), anti-instinct(7), test-strategy(8), spec-fidelity(9), wiring-verification(10). The docstring at line 1 says "9-step roadmap pipeline" but there are actually 10 steps (including wiring-verification). This is related to but distinct from C-10 (which found step numbering in a different location); this is in `_build_steps` where the actual pipeline is constructed.
**Required fix:** Renumber comments: test-strategy=8, spec-fidelity=9, wiring-verification=10. Update docstring to "10-step pipeline."

---

### E-17 [MINOR] -- `generate_certification_report` says "CERTIFIED WITH CAVEATS" when findings fail, but `route_certification_outcome` calls it "certified-with-caveats"

**File:** `src/superclaude/cli/roadmap/certify_prompts.py` lines 234-245, 276-310
**Evidence:** The report generator at line 245 outputs `"Certification: **CERTIFIED WITH CAVEATS**."` (spaces, uppercase), while `route_certification_outcome` at line 303 returns `"status": "certified-with-caveats"` (hyphenated, lowercase). Any downstream consumer that checks the certification status from the report body vs. the routing outcome would see inconsistent naming. The frontmatter uses `certified: false` (boolean). Three different representations of the same status across one module.
**Required fix:** Standardize on one naming convention; prefer the hyphenated machine-readable form and map to display form only in the report text.

---

### E-18 [IMPORTANT] -- `_check_cross_file_coherence` in remediate_executor can remove from list during iteration

**File:** `src/superclaude/cli/roadmap/remediate_executor.py` lines 450-480, 810-816
**Evidence:** At lines 813-815: `for f in cascade_rolled_back: successful_files.remove(f)` -- if `cascade_rolled_back` contains a file that was already moved to `failed_files` in the main loop (e.g., due to a race between `as_completed` processing and coherence checking), `successful_files.remove(f)` will raise `ValueError`. Additionally, `_check_cross_file_coherence` calls `_handle_file_rollback` for cascaded files, but those files may have already been snapshotted/cleaned by the main loop. The function does not check whether a file is still in `successful_files` before removing it.
**Required fix:** Guard with `if f in successful_files: successful_files.remove(f)`.

---

### E-19 [MINOR] -- `_extract_by_section` heading level calculation is wrong

**File:** `src/superclaude/cli/roadmap/certify_prompts.py` lines 145-172
**Evidence:** Line 156: `target_level = len(stripped) - len(stripped.lstrip("#"))` -- `stripped` is already `line.lstrip()`, so this calculates the number of `#` characters. But line 153: `stripped = line.lstrip()` means if the original line has leading spaces (which is valid markdown for indented code blocks, though unusual for headings), the lstrip removes them. More critically, the end-detection at line 166: `level = len(stripped) - len(stripped.lstrip("#"))` uses a fresh `stripped = lines[i].lstrip()` but this is correct. However, the actual bug is that when `section_ref = "2"`, it matches `section_ref in stripped` at line 154, which would match headings like "## 12. Extended Features" or "## Phase 2.5" -- any heading containing the digit "2". The substring match is too loose for section number lookup.
**Required fix:** Use word-boundary matching or anchor to heading number format: `re.search(rf"\b{re.escape(section_ref)}\b", stripped)`.

---

### E-20 [IMPORTANT] -- No logging of TDD/PRD auto-detection or enrichment decisions

**File:** `src/superclaude/cli/roadmap/executor.py` lines 850-870
**Evidence:** When `input_type="auto"` resolves to "tdd" or "spec", there is a `_log.info()` at line 858. But there is NO logging when:
- `--tdd-file` is silently ignored because primary input is TDD (line 863 has `_log.warning` but only to logger, not to user via `click.echo`)
- `--prd-file` is provided and used (no log entry anywhere)
- A state file auto-wires `tdd_file`/`prd_file` during resume (lines 1749, 1761 have `_log.info` but these only go to debug log, not to user)
- The extract prompt builder decides to use TDD vs spec extraction (no log)

A user running with `--debug` can see some of this, but a normal user gets only the auto-detection type message and the TDD warning. They cannot diagnose why their `--tdd-file` was ignored or why their `--prd-file` content did not appear in the extraction.
**Required fix:** Add `click.echo` messages for all supplementary file decisions: ignored, used, auto-wired from state, or file not found.

---

### E-21 [MINOR] -- `spec_structural_audit.py` `check_extraction_adequacy` divides by zero when total_structural_indicators is 0

**File:** `src/superclaude/cli/roadmap/spec_structural_audit.py` lines 95-118
**Evidence:** Actually, line 114 guards with `if audit.total_structural_indicators == 0: return True, audit`. This is correct. However, line 117 `ratio = extraction_total_requirements / audit.total_structural_indicators` would divide by zero if the guard were removed. This is a non-issue -- retracted. Replacing with the actual finding:

The `pseudocode_blocks` counter at line 63-67 uses a regex that looks for code blocks containing `if/elif/else/for/while` keywords. But this regex will also match English prose in code blocks (e.g., `if the user provides...` in a README-style code block). For TDD documents that contain design rationale in code blocks, this inflates the indicator count and makes the extraction adequacy ratio more conservative, potentially producing false warnings.

---

### E-22 [IMPORTANT] -- `build_score_prompt` accepts `tdd_file` parameter but never uses it

**File:** `src/superclaude/cli/roadmap/prompts.py` lines 461-502
**Evidence:** `build_score_prompt(debate_path, variant_a_path, variant_b_path, tdd_file=None, prd_file=None)` accepts `tdd_file` but the function body has no `if tdd_file is not None:` block. Only `prd_file` is checked at line 488. The TDD file IS embedded into the score step inputs (executor.py:970), so the scoring agent receives TDD content without any instructions about how to use it. Same pattern as E-14 (extract prompt) and the already-found C-05 (dead tdd_file param), but this is about the score step specifically -- where the TDD's technical constraints should inform variant scoring (e.g., does the variant respect the TDD's API contract design? Does it honor the TDD's data model?).
**Required fix:** Add a `if tdd_file is not None:` block with TDD-specific scoring dimensions.

---

### E-23 [MINOR] -- `_validate_input_files` in validate_executor raises FileNotFoundError with absolute path but may confuse users

**File:** `src/superclaude/cli/roadmap/validate_executor.py` lines 178-189
**Evidence:** `raise FileNotFoundError(f"Required validation input not found: {p}")` -- `p` is `output_dir / name`, which expands to an absolute path. This is fine for debugging. But the error message does not suggest what the user should do (run `roadmap run` first). Compare with `spec_patch.py` line 173-176 which says "Run `roadmap run` first." The validate command's error is less helpful.
**Required fix:** Add guidance text to the error message.

---

### E-24 [IMPORTANT] -- `convergence.py` `DeviationRegistry.save()` does not flush the `runs` list's budget snapshot before write

**File:** `src/superclaude/cli/roadmap/convergence.py` lines 264-276, 468-475
**Evidence:** Budget snapshots are written to `registry.runs[-1]["budget_snapshot"]` at lines 470-475 AFTER the checker run begins. But `registry.save()` at line 590 is called AFTER remediation. If the process crashes between the checker run and the save, the budget snapshot is lost. More critically, if `registry.save()` is never called (e.g., budget exhaustion at line 450 returns early without calling save), then the entire run's findings and budget snapshot are lost. The `begin_run` at line 462 mutates the registry's in-memory state but `save()` only happens at line 590 inside the remediation branch. The early-return paths at lines 451-458 and 535-543 do not call `registry.save()`.
**Required fix:** Call `registry.save()` before every return from the convergence loop, or use a context manager pattern.

---

### E-25 [MINOR] -- `_split_into_phases` fallback to any H2/H3 heading creates one-section-per-heading granularity

**File:** `src/superclaude/cli/roadmap/obligation_scanner.py` lines 186-216
**Evidence:** When no phase-pattern headings are found (e.g., a roadmap that uses "## Infrastructure" / "## API Layer" instead of "## Phase 1"), the fallback splits on ANY H2/H3 heading. This creates very small sections, and since discharge search only looks in "later" sections (index > current), an obligation and its discharge in the same heading's content will not be matched. In the phase-pattern case this is correct (discharge should be in a LATER phase), but in the fallback case, a section like "## API Layer" might contain both "mock the auth endpoint" and "replace mock with real auth" in the same prose, and the scanner would miss the discharge because they are in the same section.
**Required fix:** In fallback mode, consider treating same-section discharge as valid, or document this limitation.

---

## Summary

| # | ID | Severity | Category |
|---|-----|----------|----------|
| 1 | E-01 | IMPORTANT | Validation sub-pipeline missing TDD/PRD |
| 2 | E-02 | IMPORTANT | Remediation sub-pipeline missing TDD/PRD |
| 3 | E-03 | IMPORTANT | Hardcoded source_dir in fidelity checker |
| 4 | E-04 | IMPORTANT | content.find() position mismatch in obligation scanner |
| 5 | E-05 | IMPORTANT | Integration contract coverage false positives |
| 6 | E-06 | IMPORTANT | Regression handler is a no-op stub |
| 7 | E-07 | CRITICAL | Unvalidated depth/agent restore from state file |
| 8 | E-08 | IMPORTANT | Duplicate _embed_inputs/_sanitize_output implementations |
| 9 | E-09 | IMPORTANT | spec_patch ignores TDD/PRD file changes |
| 10 | E-10 | IMPORTANT | Convergence report hardcodes medium/low to 0 |
| 11 | E-11 | IMPORTANT | Thread-unsafe module-level mutable list |
| 12 | E-12 | MINOR | Certification parser regex too narrow |
| 13 | E-13 | IMPORTANT | Obligation discharge substring false positive |
| 14 | E-14 | IMPORTANT | build_extract_prompt accepts but ignores tdd_file |
| 15 | E-15 | MINOR | Full file read for input type detection |
| 16 | E-16 | IMPORTANT | Step numbering comments say "Step 8" twice |
| 17 | E-17 | MINOR | Inconsistent certification status naming |
| 18 | E-18 | IMPORTANT | List remove ValueError in cross-file coherence |
| 19 | E-19 | MINOR | Section reference substring match too loose |
| 20 | E-20 | IMPORTANT | Insufficient logging of TDD/PRD decisions |
| 21 | E-21 | MINOR | Pseudocode regex matches English prose |
| 22 | E-22 | IMPORTANT | build_score_prompt accepts but ignores tdd_file |
| 23 | E-23 | MINOR | Unhelpful validate error message |
| 24 | E-24 | IMPORTANT | Registry not saved on early convergence exit |
| 25 | E-25 | MINOR | Fallback phase splitting misses same-section discharge |

**Totals:** 25 new findings (1 CRITICAL, 16 IMPORTANT, 8 MINOR)
