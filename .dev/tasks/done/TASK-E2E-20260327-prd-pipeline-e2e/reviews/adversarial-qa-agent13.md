# Adversarial QA Report — Round 7, Agent 13

**Date:** 2026-03-28
**Phase:** adversarial-qualitative
**Fix cycle:** N/A (report only)
**Prior findings:** 116 across 6 rounds

---

## Overall Verdict: FAIL (5 new findings)

## New Findings

### C-117 [TDD] IMPORTANT — EXTRACT_GATE does not validate TDD-specific frontmatter fields

**Location:** `src/superclaude/cli/roadmap/gates.py:765-795`

**Issue:** `build_extract_prompt_tdd()` (prompts.py:205-331) instructs the extraction agent to emit 6 additional frontmatter fields: `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`. However, `EXTRACT_GATE` (gates.py:765-795) only validates the original 13 fields in its `required_frontmatter_fields` list. The 6 TDD-specific fields are never checked by any gate.

**Evidence:** Grep for any of the 6 field names in `gates.py` returns zero matches. The same `EXTRACT_GATE` is used for both spec and TDD extraction paths (executor.py maps "extract" to `EXTRACT_GATE` at line ~1085). There is no conditional gate or TDD-specific gate variant.

**Impact:** A TDD extraction that omits all 6 TDD-specific fields (e.g., an LLM that ignores those instructions) will still pass the EXTRACT_GATE. Downstream consumers (generate, spec-fidelity) that rely on those fields will silently receive incomplete data. The entire TDD-enriched extraction pipeline becomes unreliable because the quality gate does not actually enforce TDD completeness.

**Required Fix:** Either (a) create a `EXTRACT_GATE_TDD` with the 6 additional required fields and route TDD extractions to it, or (b) add the 6 fields to the existing gate with `or 0 if section absent` validation (matching the prompt's "or 0 if section absent" instruction) so they are at least presence-checked.

---

### C-118 [PRE-EXISTING] IMPORTANT — `_get_absolute_position` in obligation_scanner.py uses fragile `content.find(section_text)` that matches the wrong section on duplicate content

**Location:** `src/superclaude/cli/roadmap/obligation_scanner.py:294-306`

**Issue:** The function converts a relative position within a section to an absolute position in the original content by calling `content.find(section_text)`. `str.find()` returns the position of the **first** occurrence. If two sections have identical text (or one section's text is a prefix/substring of another's), this will always return the position of the **first** matching section, even when `section_idx` refers to a later section.

**Evidence:** `_split_into_phases` (line 186-216) extracts section text as `content[start:end]` between headings. If two adjacent headings have very similar or identical body content (common in template-generated roadmaps where phases repeat boilerplate), `content.find(section_text)` for the second section will return the byte offset of the first section. This causes `_determine_severity` to check the wrong position against `code_block_ranges`, potentially misclassifying a scaffold term inside a code block as HIGH (or vice versa).

**Impact:** Severity misclassification (HIGH vs MEDIUM) for scaffold terms in sections that share content with earlier sections. This silently alters the `undischarged_count` property (line 94-98) which gates on `severity != "MEDIUM"`.

**Required Fix:** Track the absolute start offset of each section during `_split_into_phases` (which already computes `start` as `m.end()`) and pass it directly to `_get_absolute_position` instead of using `content.find()`. Change the function to: `return section_abs_start + relative_pos`.

---

### C-119 [TDD] MINOR — `build_generate_prompt` includes `_INTEGRATION_ENUMERATION_BLOCK` but not PRD supplementary block ordering guarantee

**Location:** `src/superclaude/cli/roadmap/prompts.py:388-406`

**Issue:** In `build_generate_prompt`, when `prd_file is not None`, the PRD supplementary block is appended to `base` (line 389-404), then `_INTEGRATION_ENUMERATION_BLOCK` + `_OUTPUT_FORMAT_BLOCK` are appended (line 406). This means the PRD block appears BEFORE the Integration Points block in the final prompt. Meanwhile in `build_spec_fidelity_prompt`, `_INTEGRATION_WIRING_DIMENSION` is embedded inline within the comparison dimensions (line 586), and the PRD block comes AFTER (line 618-635). The ordering inconsistency means the generate prompt instructs the agent to think about PRD context first, then integration wiring, but the fidelity prompt checks integration wiring first, then PRD dimensions 12-15. This is not a functional bug, but the inconsistent prompt structure increases the risk that the LLM under-weights whichever block comes later in the prompt.

**Evidence:** `build_generate_prompt` line 406: `return base + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK` — the PRD block was appended to `base` at line 389. `build_spec_fidelity_prompt` line 586: `_INTEGRATION_WIRING_DIMENSION` is inline, PRD block at line 618.

**Required Fix:** Consider reordering `build_generate_prompt` so Integration Enumeration block is appended to `base` before the PRD conditional, ensuring integration wiring instructions always appear before supplementary context in both prompts.

---

### C-120 [PRE-EXISTING] MINOR — Synthesis quality checklist item 13 references `synth-04` but FR traceability may span multiple synth files

**Location:** `.claude/skills/tdd/SKILL.md:1149`

**Issue:** Checklist item 13 states: "spot-check 3 FRs in the synth-04 output: each must cite a PRD epic ID in its Source column." However, `synth-04-data-api.md` covers sections 7 (Data Models) and 8 (API Specifications) per the mapping table — not section 5 (Technical Requirements) where FRs are defined. FRs live in `synth-02-requirements.md` which covers section 5. The checklist directs QA to spot-check FRs in the wrong file.

**Evidence:** Synthesis Mapping Table (SKILL.md:1111-1121): `synth-02-requirements.md` maps to "5. Technical Requirements", while `synth-04-data-api.md` maps to "7. Data Models, 8. API Specifications". FRs (FR-NNN identifiers) are primarily in section 5. synth-04 may contain data model definitions and API specs that reference FRs, but the FR rows with "Source" columns live in synth-02.

**Impact:** QA agents following this checklist literally will look for FR rows in synth-04 (where they may not exist in the expected format), leading to either false FAILs (no FRs found) or skipped checks (agent interprets absence as N/A).

**Required Fix:** Change "synth-04" to "synth-02" in checklist item 13, or change the check to "spot-check 3 FRs in the synth-02 output (Section 5 Technical Requirements table)."

---

### C-121 [PRE-EXISTING] MINOR — `_extract_component_context` lowercases all component names, preventing case-sensitive discharge matching

**Location:** `src/superclaude/cli/roadmap/obligation_scanner.py:222-243`

**Issue:** `_extract_component_context` returns all component names lowercased (lines 235, 239, 243). The discharge check `_has_discharge` (line 258-270) then does `component.lower() in content.lower()` (line 269). Since `component` is already lowercased, this works for matching. However, the lowercasing at extraction time means the `Obligation.component` field (stored at line 160) always contains a lowercased string. This is not a bug in the matching logic, but it degrades diagnostic quality: the obligation report shows `"executor skeleton"` instead of `"Executor Skeleton"`, making it harder for users to locate the exact term in the roadmap. The `component` field is also used in the `Obligation` dataclass's `context` display and any downstream reporting.

**Evidence:** Line 235: `return code_terms[0].lower()`. Line 239: `return cap_terms[0].lower()`. Line 243: `return _get_context_line(text, pos).lower()`.

**Impact:** Degraded diagnostic readability in obligation reports. The component name in the report does not match the casing in the roadmap, requiring users to mentally re-case or search case-insensitively.

**Required Fix:** Store the original-cased component name in the `Obligation.component` field. Only lowercase in the `_has_discharge` comparison (which already lowercases both sides at line 269).

---

## Areas Investigated With No New Findings

1. **Click decorator ordering** (commands.py:32-123): The decorator stack is correct. Click processes decorators bottom-up, meaning the last decorator before the function definition is processed first. The argument `spec_file` is the innermost (line 33), and all options stack above it. The `@click.pass_context` at line 123 is outermost, which is correct for Click context passing. No ordering bugs found.

2. **`convergence.py` TDD/PRD interaction**: The convergence engine is input-type-agnostic — it operates on findings (structural + semantic) regardless of whether the source was TDD or spec. `DeviationRegistry.merge_findings` (line 144-203) and `execute_fidelity_with_convergence` (line 386-607) have no code paths that branch on input type. No TDD-specific interaction issues found beyond previously reported items.

3. **`_INTEGRATION_ENUMERATION_BLOCK` and `_INTEGRATION_WIRING_DIMENSION` conflict with PRD blocks**: These constants define integration-wiring instructions. They are appended/embedded in prompts independently of PRD blocks. The PRD blocks add supplementary dimensions (persona, compliance, etc.) that are orthogonal to integration wiring. No content conflict or duplication found — they address different concerns (technical wiring vs. business context).

4. **Test assertions**: The test files examined (`test_tdd_extract_prompt.py`, `test_prd_prompts.py`, `test_prd_cli.py`, `test_prd_prompts.py` in tasklist, `test_autowire.py`) have correct assertions. The `TestAutoDetection` tests in `test_tdd_extract_prompt.py:120-182` use real `detect_input_type` calls with synthetic files and check both positive and negative cases. The `TestRedundancyGuard` (line 215-254) correctly simulates the executor's guard logic using `dataclasses.replace`. No tests found that pass for the wrong reason.

5. **`spec_structural_audit.py`**: Beyond the previously reported C-49 (divide-by-zero), the module is clean. The 7 indicator counters use correct regex patterns, the deduplication of `test_name_count` via `set()` (line 59) is correct, and the `check_extraction_adequacy` threshold logic (line 95-118) handles the zero-indicator edge case (line 114).

6. **`integration_contracts.py`**: Beyond C-41, the pattern matching is reasonable. The `_classify_mechanism` function (line 262-291) has comprehensive keyword coverage. The `_extract_identifiers` function (line 294-303) correctly extracts UPPER_SNAKE_CASE and PascalCase identifiers. The `check_roadmap_coverage` dual-path (wiring patterns then identifiers) is sound. One minor note: `_classify_mechanism` checks `"command_map"` (with underscore) at line 266, but the DISPATCH_PATTERNS regex at line 25 uses `command[_\s]?map` (allowing space or underscore). The classification function would fail to match `"command map"` (with space) to `"command_map"`, but this is harmless since the function receives the regex match group which preserves the original text, and the fallback returns `"integration_point"` which is acceptable.

## Summary

| # | ID | Severity | Location | Tag | Issue |
|---|-----|----------|----------|-----|-------|
| 1 | C-117 | IMPORTANT | gates.py:765-795 | [TDD] | EXTRACT_GATE has no TDD-specific field validation |
| 2 | C-118 | IMPORTANT | obligation_scanner.py:294-306 | [PRE-EXISTING] | `content.find()` matches wrong section on duplicate content |
| 3 | C-119 | MINOR | prompts.py:388-406 | [TDD] | Inconsistent PRD/integration block ordering across prompts |
| 4 | C-120 | MINOR | SKILL.md:1149 | [PRE-EXISTING] | QA checklist item 13 references wrong synth file for FR traceability |
| 5 | C-121 | MINOR | obligation_scanner.py:222-243 | [PRE-EXISTING] | Component names always lowercased, degrading report readability |

- **CRITICAL:** 0
- **IMPORTANT:** 2
- **MINOR:** 3
- **New findings:** 5
- **Duplicate of prior findings:** 0

## QA Complete
