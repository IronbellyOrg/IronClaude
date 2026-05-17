# Adversarial QA Report — Integration, Consistency & Gap Focus

**Date:** 2026-03-28
**Phase:** adversarial-qa / integration-consistency-gaps
**Fix authorization:** REPORT ONLY

---

## Overall Verdict: FAIL (11 CRITICAL, 7 IMPORTANT, 5 MINOR)

---

## Section 1: CLI <-> Skill Layer Consistency

### Finding F-01: Detection rule divergence between CLI and skill layer

**Severity:** CRITICAL
**Category:** consistency-issue
**Files:** `src/superclaude/cli/roadmap/executor.py` L60-120, `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` L7-12, `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` L143-148

**What's wrong:** The CLI `detect_input_type()` uses a **4-signal weighted scoring system** with threshold >= 5:
1. Numbered headings count (>=20: +3, >=15: +2, >=10: +1)
2. TDD-exclusive frontmatter fields (`parent_doc`, `coordinator`) at +2 each
3. TDD-specific section names (8 patterns) at +1 each
4. "Technical Design Document" in first 1000 chars at +2

The skill layer (`scoring.md` L7-12 and `extraction-pipeline.md` L143-148) uses a **3-signal boolean OR rule**: input contains `## 10. Component Inventory` heading, OR frontmatter type containing "Technical Design Document", OR >= 20 section headings matching `## N. Heading`.

These are fundamentally different algorithms. The CLI uses additive weighted scoring; the skill uses disjunctive boolean checks. A document with `parent_doc` + `coordinator` + 5 TDD section names would score 9 in CLI (TDD) but could be classified as spec in the skill layer (no `## 10. Component Inventory`, no type field, < 20 headings).

**What should be done:** Align the skill layer detection rule with the CLI. Document the canonical detection algorithm in ONE place and reference it from both. The CLI implementation is the more robust version.

### Finding F-02: Extraction sections naming mismatch

**Severity:** IMPORTANT
**Category:** consistency-issue
**Files:** `src/superclaude/cli/roadmap/prompts.py` L267-296, `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` L151-207

**What's wrong:** The CLI `build_extract_prompt_tdd()` asks for 6 TDD sections with these headings:
1. `## Data Models and Interfaces`
2. `## API Specifications`
3. `## Component Inventory`
4. `## Testing Strategy`
5. `## Migration and Rollout Plan`
6. `## Operational Readiness`

The skill layer Steps 9-15 define 7 steps with these storage keys:
- Step 9: `component_inventory` (from `## 10. Component Inventory`)
- Step 10: `migration_phases` (from S19.3/S19.4)
- Step 11: `release_criteria` (from S24.1/S24.2) **<-- NO CLI EQUIVALENT**
- Step 12: `observability` (from S14.2/S14.4/S14.5)
- Step 13: `testing_strategy` (from S15)
- Step 14: `api_surface` (from S8.1)
- Step 15: `data_model_complexity` (from S7.1)

The skill defines 7 steps; the CLI asks for 6 sections. `release_criteria` (Step 11) has no corresponding CLI section. Additionally, the skill's `observability` maps roughly to the CLI's `## Operational Readiness` but covers different sub-sections (S14 metrics/alerts/dashboards vs. the CLI's runbook/on-call/capacity).

**What should be done:** Either add a `## Release Criteria` section to `build_extract_prompt_tdd()` or remove Step 11 from the skill. Reconcile the observability/operational readiness naming.

### Finding F-03: TDD complexity scoring formula not implemented in CLI

**Severity:** CRITICAL
**Category:** integration-gap
**Files:** `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` L70-108, `src/superclaude/cli/roadmap/gates.py`, `src/superclaude/cli/roadmap/prompts.py`

**What's wrong:** The skill layer defines a 7-factor TDD complexity scoring formula with specific weights (0.20/0.20/0.15/0.10/0.15/0.10/0.10) and two new factors (`api_surface`, `data_model_complexity`). The CLI does NOT implement this formula anywhere. The CLI extraction prompt asks for `complexity_score` and `complexity_class` as LLM-generated frontmatter fields, but there is no programmatic implementation of the scoring formula. The LLM is free to compute complexity however it wants.

The EXTRACT_GATE validates `complexity_class` is one of LOW/MEDIUM/HIGH, but it does not verify the `complexity_score` was computed using the specified formula. The skill layer expects this formula to be deterministic; the CLI lets the LLM improvise.

**What should be done:** Either (a) implement the 7-factor formula in the CLI's extract step (post-processing the extraction output to recompute complexity), or (b) document that the CLI delegates complexity scoring to the LLM and the skill formula is advisory. The current situation is ambiguous -- downstream consumers of `complexity_score` may assume deterministic computation.

### Finding F-04: Spec-fidelity dimensions count divergence

**Severity:** IMPORTANT
**Category:** consistency-issue
**Files:** `src/superclaude/cli/roadmap/prompts.py` L579-635, `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`

**What's wrong:** `build_spec_fidelity_prompt()` defines:
- Dimensions 1-6: Signatures, Data Models, Gates, CLI Options, NFRs, Integration Wiring (standard)
- Dimensions 7-11: API Endpoints, Component Inventory, Testing Strategy, Migration & Rollout, Operational Readiness (TDD-specific, always present in prompt)
- Dimensions 12-15: Persona Coverage, Business Metric Traceability, Compliance & Legal, Scope Boundary (PRD-conditional)

The prompt ALWAYS includes dimensions 7-11, even for spec-only inputs. These TDD-specific dimensions will produce noise or empty results when the spec has no API endpoints, component inventories, etc. The skill layer describes these as conditional on TDD detection. The tests in `test_spec_fidelity.py` only verify dimensions 1-5 ("Signatures", "Data Models", "Gates", "CLI Options", "NFRs") and do not test the TDD or PRD dimensions at all.

**What should be done:** Make dimensions 7-11 conditional on `effective_input_type == "tdd"` or on the extraction actually containing TDD sections. Currently they are unconditional, which could cause false deviation reports on spec-only inputs.

---

## Section 2: Test Coverage Gaps

### Finding F-05: No integration tests for full data flow

**Severity:** CRITICAL
**Category:** test-gap
**Files:** `tests/roadmap/`, `tests/tasklist/`, `tests/cli/`

**What's wrong:** There are NO integration tests that verify the full data flow: detect_input_type -> build_extract_prompt_tdd -> gate evaluation -> state persistence -> auto-wire. Every test file tests a single function or a single interaction in isolation:

- `test_tdd_extract_prompt.py`: Tests prompt string content, config defaults, and detection logic independently
- `test_prd_prompts.py`: Tests prompt builder string content (presence/absence of markers) -- no execution
- `test_prd_cli.py`: Tests Click flag parsing only -- dry-run, never executes pipeline
- `test_spec_fidelity.py`: Tests `_build_steps()` ordering and `_save_state` -- never runs a real step
- `test_autowire.py`: Tests auto-wire logic by reimplementing it inline, not by calling actual tasklist commands

The auto-wire test (`test_autowire.py`) is particularly concerning: it copies the auto-wire logic from `tasklist/commands.py` into the test rather than calling the actual function. If `commands.py` changes its auto-wire logic, these tests pass but don't test the real code.

**What should be done:** Create integration tests that:
1. Write a TDD file, run `detect_input_type`, verify correct detection
2. Build the extract prompt, verify TDD sections AND PRD blocks are present/absent correctly
3. Write a state file with tdd_file/prd_file, invoke `tasklist validate` (or at minimum, the command's auto-wire logic directly), verify correct auto-wiring
4. Test the _build_steps pipeline construction with tdd_file and prd_file, verify inputs lists are correct

### Finding F-06: No tests for build_extract_prompt_tdd with prd_file parameter

**Severity:** IMPORTANT
**Category:** test-gap
**Files:** `tests/cli/test_tdd_extract_prompt.py`

**What's wrong:** `TestBuildExtractPromptTdd` has 6 tests, none of which pass `prd_file`. The test `test_with_retrospective` tests the retrospective parameter, but prd_file is never tested on the TDD prompt builder in this file. The tests in `tests/roadmap/test_prd_prompts.py` do test `build_extract_prompt_tdd(SPEC, prd_file=PRD)` (3 tests), which partially covers this, but those tests only check for marker strings -- they don't verify the PRD block content or positioning relative to TDD sections.

**What should be done:** Add tests to `test_tdd_extract_prompt.py` that verify `build_extract_prompt_tdd(dummy_path, prd_file=PRD)` produces correct output with both TDD sections AND PRD enrichment block, and that the PRD block appears after the TDD sections.

### Finding F-07: No tests for state file backward compatibility

**Severity:** IMPORTANT
**Category:** test-gap
**Files:** `tests/tasklist/test_autowire.py`

**What's wrong:** No test verifies what happens when a state file from the OLD schema (before `tdd_file`/`prd_file`/`input_type` fields were added) is read by the auto-wire logic. The `read_state()` function returns the full dict, and `state.get("tdd_file")` returns `None` when the field is absent, so it likely works -- but there is no test proving this. Since `_save_state` writes `schema_version: 1` both before and after the field additions, there's no way to detect an old-format state file.

**What should be done:** Add a test with a minimal state file `{"schema_version": 1, "spec_file": "...", "steps": {}}` (no tdd_file, no prd_file, no input_type) and verify auto-wire handles it gracefully.

---

## Section 3: Edge Cases Not Handled

### Finding F-08: No validation of --prd-file content type

**Severity:** IMPORTANT
**Category:** edge-case
**Files:** `src/superclaude/cli/roadmap/commands.py` L120, `src/superclaude/cli/tasklist/commands.py` L69

**What's wrong:** `--prd-file` accepts any file that exists (Click's `exists=True`). There is no validation that the file is actually a PRD. If a user passes `--prd-file my-tdd.md`, the TDD content would be injected as "PRD context" into extraction, generating, scoring, etc. The PRD supplementary blocks reference specific PRD sections (S5, S6, S7, S12, S17, S19, S22) that won't exist in a TDD, causing the LLM to hallucinate or produce garbage enrichment.

Similarly, `--tdd-file` has no content validation. The CLI warns in `commands.py` if `--input-type tdd` is used with a file that doesn't contain "Technical Design Document" in the first 500 bytes, but `--tdd-file` (the supplementary flag) has no such check.

**What should be done:** Add a lightweight content check (similar to the input-type warning) for both `--prd-file` and `--tdd-file` supplementary flags. At minimum, emit a warning if `--prd-file` doesn't contain common PRD markers ("User Personas", "Success Metrics", "Product Requirements") in the first 1000 bytes.

### Finding F-09: Same file for --tdd-file and --prd-file

**Severity:** MINOR
**Category:** edge-case
**Files:** `src/superclaude/cli/roadmap/commands.py`

**What's wrong:** If a user passes `--tdd-file doc.md --prd-file doc.md` (same file), the document would be embedded twice in every step that uses both (extract, generate, score, test-strategy, spec-fidelity). This doubles the prompt size for no benefit and could cause confusion as the LLM processes the same content twice with different framing ("TDD context" vs "PRD context").

**What should be done:** Add a check in the `run` command that warns if `tdd_file == prd_file` after resolution.

### Finding F-10: Threshold boundary behavior at score=5

**Severity:** MINOR
**Category:** edge-case
**Files:** `src/superclaude/cli/roadmap/executor.py` L118

**What's wrong:** `detect_input_type()` uses `score >= 5` as the TDD threshold. There is a test for documents that score high (20+ headings) and documents that score low (12 headings), but no test for a document that scores exactly 5. The existing `test_detects_tdd_from_section_names` creates a file with 5 TDD section names (5 points) that hits exactly the threshold, but this is incidental -- there's no test that explicitly targets the boundary.

A document with `parent_doc` (2) + `coordinator` (2) + 1 TDD section name (1) = 5 = TDD. But `parent_doc` (2) + 3 TDD section names (3) = 5 = TDD while `coordinator` (2) + 2 TDD section names (2) = 4 = spec. These edge cases aren't tested.

**What should be done:** Add explicit boundary tests at score=4 (spec) and score=5 (tdd) with different signal combinations.

---

## Section 4: Cross-Reference E2E Findings

### Finding F-11: Anti-instinct gate blocker unfixed across two E2E rounds

**Severity:** CRITICAL
**Category:** code-bug
**Files:** `src/superclaude/cli/roadmap/gates.py` L1003-1028, `src/superclaude/cli/roadmap/obligation_scanner.py`, `src/superclaude/cli/roadmap/integration_contracts.py`

**What's wrong:** Both E2E reports (TDD: 2026-03-27, PRD: 2026-03-31) flag the anti-instinct gate as the primary blocker. The TDD E2E found: undischarged_obligations=5, uncovered_contracts=4 (TDD path); uncovered_contracts=3 (spec path). The PRD E2E confirmed all 4 runs fail at anti-instinct. The TDD follow-up `follow-up-action-items.md` lists it as priority #1. The PRD follow-up lists it as priority #1 again.

Despite being flagged as **HIGH priority** in BOTH follow-up reports, there is NO evidence of any fix attempt. The gate code, obligation scanner, and integration contract checker are unchanged. This blocks:
- Test-strategy verification (skipped in all E2E runs)
- Spec-fidelity verification (skipped in all E2E runs)
- Deviation analysis (never reached)
- The entire remediation/certification pipeline

**What should be done:** Three options were proposed in the TDD follow-up; none were executed:
(a) Relax the gate to allow small uncovered_contracts counts (threshold > 0)
(b) Improve the merge prompt to address integration contracts
(c) Make anti-instinct TRAILING mode like wiring-verification
Option (c) is the fastest path to unblocking. The gate mode change is a single-field edit on `ANTI_INSTINCT_GATE` Step definition at executor.py L988.

### Finding F-12: Fingerprint regression with TDD+PRD not investigated

**Severity:** IMPORTANT
**Category:** code-bug
**Files:** `src/superclaude/cli/roadmap/fingerprint.py`, `src/superclaude/cli/roadmap/prompts.py`

**What's wrong:** The PRD E2E report documents a fingerprint_coverage regression from 0.76 (TDD-only) to 0.69 (TDD+PRD), dropping below the 0.7 threshold. The follow-up marks this as MEDIUM priority and says "Investigate whether the PRD block instructions should explicitly tell the LLM to preserve backticked identifier density." No investigation was done. The fingerprint extraction (`fingerprint.py`) extracts backtick-delimited identifiers from the SPEC, then checks their presence in the ROADMAP. PRD content in the prompt may cause the LLM to use more natural language and fewer backticked identifiers in the roadmap output.

**What should be done:** Either (a) add a prompt instruction in the PRD blocks to "preserve technical identifier formatting (backticked names)" or (b) adjust the fingerprint threshold when prd_file is provided (e.g., 0.6 instead of 0.7). The current situation means TDD+PRD pipelines will consistently fail at anti-instinct's fingerprint check even if the other anti-instinct issues are fixed.

### Finding F-13: DEVIATION_ANALYSIS_GATE field mismatch still unfixed

**Severity:** CRITICAL
**Category:** code-bug
**Files:** `src/superclaude/cli/roadmap/gates.py` L1030-1081

**What's wrong:** The TDD E2E follow-up (BUG B-1) documents that `DEVIATION_ANALYSIS_GATE` uses `ambiguous_deviations` (L382 check function) but the gate's `required_frontmatter_fields` list (L1038) uses `ambiguous_count`. The gate check function (`_no_ambiguous_deviations`) checks for `ambiguous_deviations` in frontmatter (L382), while the prompt presumably asks the LLM to produce `ambiguous_count`. This mismatch means the gate ALWAYS fails on the semantic check because `ambiguous_deviations` field is never present.

Examining the code: `_no_ambiguous_deviations()` at L382 reads `fm.get("ambiguous_deviations")`. The gate at L1038 requires `ambiguous_count` in frontmatter. But `_total_analyzed_consistent()` at L539 reads `ambiguous_count`. So the SAME gate has two inconsistent field names for the same concept:
- `required_frontmatter_fields` requires `ambiguous_count`
- `_no_ambiguous_deviations` semantic check reads `ambiguous_deviations`
- `_total_analyzed_consistent` reads `ambiguous_count`

This means if the LLM produces `ambiguous_count: 0` (matching the required field), the semantic check for `ambiguous_deviations` returns False (field missing). If the LLM produces `ambiguous_deviations: 0`, the required field check for `ambiguous_count` fails.

**What should be done:** Rename `ambiguous_deviations` to `ambiguous_count` in `_no_ambiguous_deviations()` at L382, or vice versa. Both functions in the same gate must use the same field name.

---

## Section 5: Deferred Work Items Review

### Finding F-14: Tasklist generate CLI missing -- blocks full pipeline chain

**Severity:** CRITICAL
**Category:** design-gap
**Files:** `src/superclaude/cli/tasklist/commands.py`, `src/superclaude/cli/tasklist/prompts.py` L144-230

**What's wrong:** `build_tasklist_generate_prompt()` exists and is fully functional (tested in `test_prd_prompts.py` for all 4 scenarios), but there is no `superclaude tasklist generate` CLI command. The function has an explicit NOTE in its docstring (L151-154): "This function is used by the /sc:tasklist skill protocol for inference-based generation workflows. It is NOT currently called by the CLI tasklist validate executor."

The PRD E2E follow-up flags this as HIGH priority with "blocks full pipeline chain." Both E2E reports confirm tasklist validation enrichment is INCONCLUSIVE because there is no tasklist artifact to validate against.

This means the full pipeline chain (roadmap run -> tasklist generate -> tasklist validate) cannot be exercised end-to-end through the CLI. The only way to generate a tasklist is through the /sc:tasklist skill (inference-based), which uses a completely separate execution path.

**What should be done:** Implement `superclaude tasklist generate` as a CLI command that uses `build_tasklist_generate_prompt()` with the same subprocess pattern as `roadmap run`. Without this, the CLI pipeline chain is incomplete.

### Finding F-15: TDD-aware generate prompt comment says "deferred"

**Severity:** CRITICAL
**Category:** design-gap
**Files:** `src/superclaude/cli/roadmap/prompts.py` L360-367

**What's wrong:** `build_generate_prompt()` contains a code comment at L360-367:
```python
# TDD mode: extraction.md may contain additional frontmatter fields
# ... and additional body sections ... when generated by
# build_extract_prompt_tdd(). The roadmap should address these sections when present.
# Full TDD-aware generate prompt update is deferred — see TASK-RF-20260325-cli-tdd
# Deferred Work Items.
```

The generate prompt does NOT instruct the LLM to use TDD-specific extraction sections (Data Models, API Specs, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness). It only mentions standard extraction fields. When TDD extraction produces 14 sections, the generate prompt only tells the LLM about 8-section extraction format. The 6 TDD-specific sections are embedded as inputs but the prompt doesn't tell the LLM to use them.

This means TDD-specific content in extraction.md is available to the LLM (via inline embedding) but the prompt gives no guidance on how to incorporate it into the roadmap. The LLM may ignore Data Models, API specs, etc. because the prompt doesn't mention them.

**What should be done:** Add TDD-section awareness to `build_generate_prompt()`. At minimum, add: "When the extraction document contains additional TDD sections (Data Models, API Specifications, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness), address each section in the roadmap with specific implementation phases and tasks."

### Finding F-16: Merge prompt has no PRD/TDD awareness

**Severity:** IMPORTANT
**Category:** design-gap
**Files:** `src/superclaude/cli/roadmap/prompts.py` L505-534

**What's wrong:** `build_merge_prompt()` is the ONLY prompt builder that accepts neither `tdd_file` nor `prd_file` parameters. Every other builder (extract, generate, score, test-strategy, spec-fidelity) has been updated with PRD/TDD supplementary blocks. The merge step produces `roadmap.md`, which is the final merged roadmap consumed by all downstream steps.

This means:
- PRD context used during generate and score is invisible to the merge step
- The merge may drop PRD-driven prioritization or persona coverage from the variants
- TDD technical detail from extraction may be lost in the merge

The `_build_steps()` function at L974-982 confirms: merge step inputs are `[score_file, roadmap_a, roadmap_b, debate_file]` -- no tdd_file or prd_file.

**What should be done:** Add `prd_file` and `tdd_file` parameters to `build_merge_prompt()` with supplementary blocks instructing the merge to preserve PRD-driven prioritization and TDD technical specificity from the variants.

---

## Section 6: Anti-Instinct Gate Analysis

### Finding F-17: Obligation scanner "skeleton" pattern too aggressive

**Severity:** CRITICAL
**Category:** code-bug
**Files:** `src/superclaude/cli/roadmap/obligation_scanner.py` L22-33

**What's wrong:** `SCAFFOLD_TERMS` includes `\bskeleton\b`, `\bplaceholder\b`, `\bscaffold\b`, `\btemporary\b`, and `\bmock\b`. In a generated roadmap, these terms naturally appear in task descriptions like "Create project skeleton structure", "Set up placeholder configuration", "Mock API endpoints during Phase 1." These are DESCRIPTIONS OF WHAT TO DO, not undischarged obligations.

The scanner treats every mention of a scaffold term as an obligation, then requires a corresponding discharge term in a LATER phase. But in a roadmap, "Phase 1: Create skeleton" followed by "Phase 2: Implement features" may not use explicit discharge vocabulary ("replace", "wire up", etc.) -- the implementation IS the discharge, but it doesn't use the required vocabulary.

The E2E results show 5 undischarged obligations in TDD path and 1 in spec+PRD path. These are likely false positives from roadmap description text that uses scaffold vocabulary to describe implementation tasks.

**What should be done:** Add context-awareness: if a scaffold term appears in a task title/description (not in a "Phase N already has X" reference), it's describing planned work, not an undischarged obligation. Alternatively, lower the severity or make the check informational rather than gate-blocking.

### Finding F-18: Integration contract checker catches too many false positives

**Severity:** CRITICAL
**Category:** code-bug
**Files:** `src/superclaude/cli/roadmap/integration_contracts.py` L22-71

**What's wrong:** `DISPATCH_PATTERNS` includes broad patterns like `\bmiddleware\b` (Category 5), `\bsubscribe\b` and `\badd_listener\b` (Category 6), and `\bstrategy\b` (Category 4). These patterns match mentions of these concepts in the SPEC, then require explicit wiring tasks in the ROADMAP.

For a product spec that mentions "middleware chain" or "event subscription" conceptually (not as explicit dispatch tables), the checker will flag uncovered contracts. The E2E consistently shows 3-4 uncovered contracts across all runs.

The `WIRING_TASK_PATTERNS` (L74+) that check for coverage require very specific phrasing like "create the dispatch table" or "populate the registry." A roadmap that says "Implement middleware layer" won't match because it doesn't use the verb-anchored patterns.

**What should be done:** Either narrow the spec-side patterns to require code-formatted references (backtick-delimited), or broaden the roadmap-side coverage patterns to accept implementation verbs like "implement", "build", "develop" alongside "create", "populate", "wire".

### Finding F-19: 0.7 fingerprint threshold may be too strict

**Severity:** MINOR
**Category:** design-gap
**Files:** `src/superclaude/cli/roadmap/gates.py` L332-347

**What's wrong:** The fingerprint_coverage threshold is hardcoded at 0.7 (L345). The PRD E2E shows TDD+PRD drops to 0.69, and the TDD-only baseline was 0.76. A threshold that fails at 0.69 but passes at 0.72 provides very little margin. The threshold was set without empirical calibration against a corpus of known-good roadmaps.

**What should be done:** Empirically calibrate the threshold against the 4 E2E runs (0.69, 0.72, 0.76, 0.78). Consider lowering to 0.65 or making it configurable via `--fingerprint-threshold`.

---

## Section 7: Backward Compatibility

### Finding F-20: Spec-fidelity dimensions 7-11 always emitted (potential regression)

**Severity:** IMPORTANT
**Category:** consistency-issue
**Files:** `src/superclaude/cli/roadmap/prompts.py` L587-591

**What's wrong:** As noted in F-04, dimensions 7-11 (API Endpoints, Component Inventory, Testing Strategy, Migration & Rollout, Operational Readiness) are always included in the spec-fidelity prompt, even for spec-only runs. Before the TDD integration, the prompt had only dimensions 1-5 (Signatures, Data Models, Gates, CLI Options, NFRs) plus dimension 6 (Integration Wiring).

This means `superclaude roadmap run spec.md` (no flags) now produces a spec-fidelity prompt with 11 dimensions instead of the previous 6. The LLM will attempt to check for API endpoints, component inventories, etc. against a spec that may not have them. This could generate false MEDIUM/LOW deviations in the fidelity report, changing behavior for existing users.

**What should be done:** Make dimensions 7-11 conditional on TDD input type, or at minimum add "If the source document does not contain these sections, skip this dimension" to each TDD-specific dimension.

### Finding F-21: build_generate_prompt TDD comment vs actual behavior

**Severity:** MINOR
**Category:** consistency-issue
**Files:** `src/superclaude/cli/roadmap/prompts.py` L360-367

**What's wrong:** The code comment at L360-367 says "Full TDD-aware generate prompt update is deferred." But `build_generate_prompt()` DOES accept `tdd_file` and `prd_file` parameters (added in PRD integration) and DOES include a PRD supplementary block. The comment is stale -- it was written during TDD integration but the function was partially updated during PRD integration. The TDD-specific generate enhancement IS deferred (see F-15), but the comment implies neither TDD nor PRD work was done on this function.

**What should be done:** Update the comment to accurately reflect current state: "TDD-specific section awareness in generate prompt is deferred. PRD supplementary block is active."

### Finding F-22: Step numbering inconsistency in _build_steps

**Severity:** MINOR
**Category:** consistency-issue
**Files:** `src/superclaude/cli/roadmap/executor.py` L993, L1003

**What's wrong:** The comment at L993 says "# Step 8: Test Strategy" and L1003 says "# Step 8: Spec Fidelity". Both are labeled Step 8. The actual pipeline step ordering is: extract (1), generate-A+B (2), diff (3), debate (4), score (5), merge (6), anti-instinct (7), test-strategy (8), spec-fidelity (9), wiring-verification (10). The comments misnumber spec-fidelity as step 8 instead of 9.

**What should be done:** Fix comment: `# Step 9: Spec Fidelity` at L1003.

### Finding F-23: `prd_file` config field not defaulted in RoadmapConfig for older state restoration

**Severity:** MINOR
**Category:** edge-case
**Files:** `src/superclaude/cli/roadmap/models.py` L116

**What's wrong:** `RoadmapConfig.prd_file` defaults to `None`, which is correct. However, when `--resume` restores state from `.roadmap-state.json` and the state file was written by a pre-PRD version of the pipeline, the state file will have `prd_file: null`. The resume logic in the executor reads `state.get("prd_file")` and the config construction handles `None` correctly. This is NOT a bug -- the default is correct. But there is no explicit test for this resume path with a pre-PRD state file, which means a regression could silently break it.

**What should be done:** Add a test that creates a state file without `prd_file` field and verifies `--resume` handles it correctly.

---

## Summary

| # | Severity | Category | Location | Issue | Required Fix |
|---|----------|----------|----------|-------|-------------|
| F-01 | CRITICAL | consistency-issue | executor.py / scoring.md / extraction-pipeline.md | Detection rule algorithm divergence between CLI and skill | Align skill to CLI algorithm |
| F-02 | IMPORTANT | consistency-issue | prompts.py / extraction-pipeline.md | 6 CLI sections vs 7 skill steps (release_criteria missing) | Add release_criteria or remove Step 11 |
| F-03 | CRITICAL | integration-gap | scoring.md / gates.py | 7-factor TDD scoring formula not implemented in CLI | Implement formula or document delegation |
| F-04 | IMPORTANT | consistency-issue | prompts.py | Spec-fidelity dims 7-11 always present, not conditional on TDD | Make conditional or add skip instructions |
| F-05 | CRITICAL | test-gap | tests/ | No integration tests for full detect->extract->gate->state flow | Create integration test suite |
| F-06 | IMPORTANT | test-gap | test_tdd_extract_prompt.py | No tests for build_extract_prompt_tdd with prd_file | Add prd_file parameter tests |
| F-07 | IMPORTANT | test-gap | test_autowire.py | No tests for old-schema state file backward compat | Add legacy state file test |
| F-08 | IMPORTANT | edge-case | commands.py | No content validation on --prd-file / --tdd-file | Add lightweight content checks |
| F-09 | MINOR | edge-case | commands.py | Same file for --tdd-file and --prd-file not caught | Add duplicate file check |
| F-10 | MINOR | edge-case | executor.py | No explicit boundary tests at score=5 threshold | Add boundary tests |
| F-11 | CRITICAL | code-bug | gates.py / obligation_scanner.py / integration_contracts.py | Anti-instinct gate unfixed after 2 E2E rounds | Make TRAILING mode or relax thresholds |
| F-12 | IMPORTANT | code-bug | fingerprint.py / prompts.py | TDD+PRD fingerprint regression uninvestigated | Add identifier-density instruction or adjust threshold |
| F-13 | CRITICAL | code-bug | gates.py L382/L1038/L539 | DEVIATION_ANALYSIS_GATE ambiguous_count vs ambiguous_deviations | Unify field name |
| F-14 | CRITICAL | design-gap | tasklist/commands.py | No `tasklist generate` CLI -- blocks full pipeline | Implement CLI command |
| F-15 | CRITICAL | design-gap | prompts.py L360-367 | Generate prompt ignores TDD extraction sections | Add TDD section instructions |
| F-16 | IMPORTANT | design-gap | prompts.py L505-534 | Merge prompt has no PRD/TDD awareness | Add supplementary blocks |
| F-17 | CRITICAL | code-bug | obligation_scanner.py | Scaffold terms in task descriptions cause false positives | Add context-awareness |
| F-18 | CRITICAL | code-bug | integration_contracts.py | Broad patterns cause false uncovered contracts | Narrow spec patterns or broaden roadmap patterns |
| F-19 | MINOR | design-gap | gates.py L345 | 0.7 fingerprint threshold not empirically calibrated | Calibrate or make configurable |
| F-20 | IMPORTANT | consistency-issue | prompts.py L587-591 | Dims 7-11 unconditional -- regression for spec-only users | Make conditional on input type |
| F-21 | MINOR | consistency-issue | prompts.py L360-367 | Stale "deferred" comment after PRD update | Update comment |
| F-22 | MINOR | consistency-issue | executor.py L1003 | Step numbering comment says "Step 8" for step 9 | Fix comment |
| F-23 | MINOR | edge-case | models.py / executor.py | No test for resume with pre-PRD state file | Add backward compat test |

**Totals:** CRITICAL: 11, IMPORTANT: 7, MINOR: 5

**Priority ordering for fixes:**
1. **F-11/F-17/F-18** (anti-instinct gate) — Unblocks test-strategy, spec-fidelity, and full pipeline
2. **F-13** (deviation analysis field mismatch) — Simple one-line fix, unblocks deviation analysis
3. **F-15** (generate prompt TDD awareness) — High-value fix for TDD pipeline quality
4. **F-01/F-03** (CLI/skill alignment) — Prevents user-facing inconsistencies between execution paths
5. **F-14** (tasklist generate CLI) — Completes the pipeline chain
6. **F-05** (integration tests) — Prevents regression in all of the above

