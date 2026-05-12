# 03 — Gate Verification Criteria Research

**Status**: Complete
**Researcher**: researcher-gates
**Files Investigated**:
- `src/superclaude/cli/roadmap/gates.py` (1100 lines)
- `src/superclaude/cli/roadmap/prompts.py` (630 lines)
- `src/superclaude/cli/roadmap/fingerprint.py` (170 lines)
- `src/superclaude/cli/pipeline/models.py` (GateCriteria dataclass)
- `src/superclaude/cli/audit/wiring_gate.py` (WIRING_GATE definition)

---

## 1. GateCriteria Model

**File**: `src/superclaude/cli/pipeline/models.py`, lines 67-74

```python
@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
```

A gate passes when:
1. Output file exists and has >= `min_lines` lines
2. YAML frontmatter (delimited by `---`) contains all `required_frontmatter_fields`
3. All `semantic_checks` (pure Python functions on file content) return `True`

Enforcement tiers define strictness but the tier itself is just a label stored on the criteria -- actual enforcement behavior is determined by the pipeline executor reading this field.

---

## 2. Gate-by-Gate Reference

### 2.1 EXTRACT_GATE
**Lines**: 765-795 | **Tier**: STRICT | **min_lines**: 50
**Output file**: `extraction.md`

**Required frontmatter (13 fields)**:
- `spec_source` (string)
- `generated` (ISO-8601 timestamp)
- `generator` (string)
- `functional_requirements` (integer)
- `nonfunctional_requirements` (integer)
- `total_requirements` (integer)
- `complexity_score` (float 0.0-1.0)
- `complexity_class` (LOW | MEDIUM | HIGH)
- `domains_detected` (list)
- `risks_identified` (integer)
- `dependencies_identified` (integer)
- `success_criteria_count` (integer)
- `extraction_mode` (standard | chunked*)

**Semantic checks (2)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `complexity_class_valid` | `_complexity_class_valid` | Value is LOW, MEDIUM, or HIGH (case-insensitive) |
| `extraction_mode_valid` | `_extraction_mode_valid` | Value is "standard" or starts with "chunked" (case-insensitive) |

**TDD mode note**: When `build_extract_prompt_tdd()` is used, the output has **19 frontmatter fields** (13 standard + 6 TDD-specific). However, EXTRACT_GATE only validates the 13 standard fields. The 6 TDD-specific fields are NOT gate-checked:
- `data_models_identified`
- `api_surfaces_identified`
- `components_identified`
- `test_artifacts_identified`
- `migration_items_identified`
- `operational_items_identified`

---

### 2.2 GENERATE_A_GATE / GENERATE_B_GATE
**Lines**: 797-831 | **Tier**: STRICT | **min_lines**: 100
**Output files**: `roadmap-A.md`, `roadmap-B.md`

**Required frontmatter (3 fields)**:
- `spec_source`
- `complexity_score`
- `primary_persona`

**Semantic checks (2)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `frontmatter_values_non_empty` | `_frontmatter_values_non_empty` | All frontmatter values are non-empty strings |
| `has_actionable_content` | `_has_actionable_content` | At least one markdown list item (`- `, `* `, `1. `) exists |

---

### 2.3 DIFF_GATE
**Lines**: 833-837 | **Tier**: STANDARD | **min_lines**: 30
**Output file**: `diff-analysis.md`

**Required frontmatter (2 fields)**:
- `total_diff_points` (integer)
- `shared_assumptions_count` (integer)

**Semantic checks**: None

---

### 2.4 DEBATE_GATE
**Lines**: 839-850 | **Tier**: STRICT | **min_lines**: 50
**Output file**: `debate-transcript.md`

**Required frontmatter (2 fields)**:
- `convergence_score` (float)
- `rounds_completed` (integer)

**Semantic checks (1)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `convergence_score_valid` | `_convergence_score_valid` | Float in [0.0, 1.0] |

---

### 2.5 SCORE_GATE
**Lines**: 852-856 | **Tier**: STANDARD | **min_lines**: 20
**Output file**: `base-selection.md`

**Required frontmatter (2 fields)**:
- `base_variant` (string)
- `variant_scores` (string, e.g. "A:78 B:72")

**Semantic checks**: None

---

### 2.6 MERGE_GATE
**Lines**: 858-879 | **Tier**: STRICT | **min_lines**: 150
**Output file**: `roadmap.md`

**Required frontmatter (3 fields)**:
- `spec_source`
- `complexity_score`
- `adversarial` (must be `true`)

**Semantic checks (3)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `no_heading_gaps` | `_no_heading_gaps` | Heading levels increment by at most 1 (no H2->H4 skip) |
| `cross_refs_resolve` | `_cross_refs_resolve` | Internal cross-refs have matching headings (WARNING-ONLY per OQ-001, always returns True) |
| `no_duplicate_headings` | `_no_duplicate_headings` | No duplicate H2 or H3 heading text |

**Note**: `_cross_refs_resolve` is effectively a no-op gate -- it warns but always returns `True`.

---

### 2.7 ANTI_INSTINCT_GATE
**Lines**: 1003-1028 | **Tier**: STRICT | **min_lines**: 10
**Output file**: `anti-instinct-audit.md`

**Required frontmatter (3 fields)**:
- `undischarged_obligations` (integer, must be 0)
- `uncovered_contracts` (integer, must be 0)
- `fingerprint_coverage` (float, must be >= 0.7)

**Semantic checks (3)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `no_undischarged_obligations` | `_no_undischarged_obligations` | `undischarged_obligations` == 0. Fail-closed. |
| `integration_contracts_covered` | `_integration_contracts_covered` | `uncovered_contracts` == 0. Fail-closed. |
| `fingerprint_coverage_check` | `_fingerprint_coverage_check` | `fingerprint_coverage` >= 0.7. Fail-closed. |

**fingerprint_coverage explanation**: See Section 3 below. This is the ratio of spec code-level identifiers found in the roadmap. The 0.7 threshold is hardcoded in `_fingerprint_coverage_check` (line 345: `float(value) >= 0.7`) and also defaults in `fingerprint.py`'s `check_fingerprint_coverage()` and `fingerprint_gate_passed()`.

---

### 2.8 TEST_STRATEGY_GATE
**Lines**: 881-922 | **Tier**: STRICT | **min_lines**: 40
**Output file**: `test-strategy.md`

**Required frontmatter (9 fields)**:
- `spec_source`
- `generated`
- `generator`
- `complexity_class` (LOW | MEDIUM | HIGH)
- `validation_philosophy` (must be exactly `continuous-parallel`)
- `validation_milestones` (positive integer)
- `work_milestones` (positive integer)
- `interleave_ratio` (must match complexity: LOW->1:3, MEDIUM->1:2, HIGH->1:1)
- `major_issue_policy` (must be exactly `stop-and-fix`)

**Semantic checks (5)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `complexity_class_valid` | `_complexity_class_valid` | LOW, MEDIUM, or HIGH |
| `interleave_ratio_consistent` | `_interleave_ratio_consistent` | Ratio matches complexity class mapping |
| `milestone_counts_positive` | `_milestone_counts_positive` | Both milestone counts > 0 |
| `validation_philosophy_correct` | `_validation_philosophy_correct` | Exactly `continuous-parallel` (hyphenated, not underscored) |
| `major_issue_policy_correct` | `_major_issue_policy_correct` | Exactly `stop-and-fix` |

**DISCREPANCY FOUND**: `build_test_strategy_prompt()` (prompts.py lines 586-629) only instructs the LLM to emit 6 frontmatter fields: `complexity_class`, `validation_philosophy`, `validation_milestones`, `work_milestones`, `interleave_ratio`, `major_issue_policy`. The gate requires 9 fields (adds `spec_source`, `generated`, `generator`). The prompt does NOT ask for these 3 fields, so the LLM may not emit them, causing gate failure.

---

### 2.9 SPEC_FIDELITY_GATE
**Lines**: 924-947 | **Tier**: STRICT | **min_lines**: 20
**Output file**: `spec-fidelity.md`

**Required frontmatter (6 fields)**:
- `high_severity_count` (integer, must be 0 for pass)
- `medium_severity_count` (integer)
- `low_severity_count` (integer)
- `total_deviations` (integer)
- `validation_complete` (boolean)
- `tasklist_ready` (boolean -- true only if high_severity_count==0 AND validation_complete==true)

**Semantic checks (2)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `high_severity_count_zero` | `_high_severity_count_zero` | `high_severity_count` parses as int and == 0. Raises TypeError on non-int. |
| `tasklist_ready_consistent` | `_tasklist_ready_consistent` | If tasklist_ready=true, then high_severity_count must be 0 AND validation_complete must be true. If tasklist_ready=false, always consistent. |

**Language note**: The prompt (line 462) uses "source-document fidelity analyst" and refers to "source specification or TDD file" and "source document" throughout. It uses the term "specification" in heading "Comparison Dimensions" but the body consistently says "source document".

---

### 2.10 WIRING_GATE (imported from audit module)
**File**: `src/superclaude/cli/audit/wiring_gate.py`, lines 1029-1082
**Tier**: STRICT | **min_lines**: 10
**Output file**: `wiring-verification.md`

**Required frontmatter (16 fields)**:
- `gate`
- `target_dir`
- `files_analyzed`
- `rollout_mode` (shadow | soft | full)
- `analysis_complete` (must be true)
- `unwired_callable_count` (integer)
- `orphan_module_count` (integer)
- `unwired_registry_count` (integer)
- `critical_count` (integer)
- `major_count` (integer)
- `info_count` (integer)
- `total_findings` (integer)
- `blocking_findings` (integer, must be 0)
- `whitelist_entries_applied` (integer)
- `files_skipped` (integer)
- `audit_artifacts_used` (integer)

**Semantic checks (5)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `analysis_complete_true` | `_analysis_complete_true` | `analysis_complete` == "true" |
| `recognized_rollout_mode` | `_recognized_rollout_mode` | `rollout_mode` in {shadow, soft, full} |
| `finding_counts_consistent` | `_finding_counts_consistent` | total_findings == unwired_callable_count + orphan_module_count + unwired_registry_count |
| `severity_summary_consistent` | `_severity_summary_consistent` | critical_count + major_count + info_count == total_findings |
| `zero_blocking_findings_for_mode` | `_zero_blocking_findings_for_mode` | blocking_findings == 0 |

---

### 2.11 DEVIATION_ANALYSIS_GATE
**Lines**: 1030-1081 | **Tier**: STRICT | **min_lines**: 20
**Output file**: `deviation-analysis.md`

**Required frontmatter (9 fields)**:
- `schema_version`
- `total_analyzed` (integer)
- `slip_count` (integer)
- `intentional_count` (integer)
- `pre_approved_count` (integer)
- `ambiguous_count` (integer, must be 0)
- `routing_fix_roadmap` (DEV-\d+ IDs, comma/space-separated)
- `routing_no_action` (DEV-\d+ IDs)
- `analysis_complete` (must be true)

**Semantic checks (7)** -- the most heavily validated gate:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `no_ambiguous_deviations` | `_no_ambiguous_deviations` | `ambiguous_deviations` == 0 (**NOTE**: checks field `ambiguous_deviations`, not `ambiguous_count`) |
| `validation_complete_true` | `_validation_complete_true` | `analysis_complete` == true |
| `routing_ids_valid` | `_routing_ids_valid` | All IDs in routing_fix_roadmap, routing_update_spec, routing_no_action, routing_human_review match DEV-\d+ |
| `slip_count_matches_routing` | `_slip_count_matches_routing` | slip_count == count of IDs in routing_fix_roadmap |
| `pre_approved_not_in_fix_roadmap` | `_pre_approved_not_in_fix_roadmap` | No overlap between routing_no_action and routing_fix_roadmap IDs |
| `total_analyzed_consistent` | `_total_analyzed_consistent` | total_analyzed == slip_count + intentional_count + pre_approved_count + ambiguous_count |
| `deviation_counts_reconciled` | `_deviation_counts_reconciled` | Count of unique DEV-\d+ IDs across ALL 4 routing fields == total_analyzed |

**TDD INCOMPATIBILITY (gates.py lines 12-16)**: Explicitly marked "NOT TDD-compatible" with a pre-existing bug B-1: the semantic check `_no_ambiguous_deviations` reads the field `ambiguous_deviations` (line 382) but the required frontmatter field is `ambiguous_count` (line 1037). These are different field names. The gate requires `ambiguous_count` in frontmatter (field presence check), but the semantic check validates `ambiguous_deviations` (a different field entirely). If the LLM emits `ambiguous_count: 0` but not `ambiguous_deviations: 0`, the frontmatter check passes but the semantic check fails.

---

### 2.12 REMEDIATE_GATE
**Lines**: 949-972 | **Tier**: STRICT | **min_lines**: 10
**Output file**: `remediation-tasklist.md`

**Required frontmatter (6 fields)**:
- `type`
- `source_report`
- `source_report_hash`
- `total_findings`
- `actionable`
- `skipped`

**Semantic checks (2)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `frontmatter_values_non_empty` | `_frontmatter_values_non_empty` | All frontmatter values non-empty |
| `all_actionable_have_status` | `_all_actionable_have_status` | All unchecked `- [ ] F-XX | file | STATUS -- desc` entries have STATUS of FIXED or FAILED (not PENDING) |

---

### 2.13 CERTIFY_GATE
**Lines**: 974-1001 | **Tier**: STRICT | **min_lines**: 15
**Output file**: `certification.md`

**Required frontmatter (5 fields)**:
- `findings_verified`
- `findings_passed`
- `findings_failed`
- `certified` (must be true)
- `certification_date`

**Semantic checks (3)**:
| Check | Function | Pass condition |
|-------|----------|---------------|
| `frontmatter_values_non_empty` | `_frontmatter_values_non_empty` | All values non-empty |
| `per_finding_table_present` | `_has_per_finding_table` | Markdown table with columns `Finding | Severity | Result | Justification` AND at least one `F-XX` data row |
| `certified_is_true` | `_certified_is_true` | `certified` field == "true" (case-insensitive) |

---

## 3. Fingerprint Extraction (fingerprint.py)

**File**: `src/superclaude/cli/roadmap/fingerprint.py`

### 3.1 `extract_code_fingerprints(content: str) -> list[Fingerprint]`
Extracts code-level identifiers from three sources (FR-MOD3.1):

| Source | Regex | Category | Min length |
|--------|-------|----------|-----------|
| Backtick identifiers | `` `([a-zA-Z_]\w*(?:\(\))?)` `` | `identifier` | >= 4 chars (after stripping `()`) |
| Code block definitions | `(?:def\|class)\s+(\w+)` inside ` ```python? ``` ` blocks | `definition` | None |
| ALL_CAPS constants | `\b([A-Z][A-Z_]{3,})\b` | `constant` | >= 4 chars (implicit from regex `{3,}` + 1 leading char) |

**Exclusion list** (`_EXCLUDED_CONSTANTS`, lines 30-54): 22 common non-specific constants are excluded:
`TRUE, FALSE, NONE, TODO, NOTE, WARNING, HIGH, MEDIUM, LOW, YAML, JSON, STRICT, STANDARD, EXEMPT, LIGHT, PASS, FAIL, INFO, DEBUG, ERROR, CRITICAL`

**Deduplication** (FR-MOD3.2): By `.text` value, first occurrence wins.

### 3.2 `check_fingerprint_coverage(spec_content, roadmap_content, min_coverage_ratio=0.7)`
- Extracts fingerprints from spec, checks case-insensitive presence in roadmap (FR-MOD3.3)
- **Empty passthrough** (FR-MOD3.4): If no fingerprints extracted, returns `(0, 0, [], 1.0)` -- auto-pass
- Returns `(total, found, missing_list, ratio)`

### 3.3 `fingerprint_gate_passed(spec_content, roadmap_content, min_coverage_ratio=0.7)`
- Returns `True` when `ratio >= 0.7` or fingerprint set is empty
- **Threshold**: 0.7 (70%) hardcoded as default, also hardcoded in `_fingerprint_coverage_check` in gates.py

---

## 4. Prompt Analysis

### 4.1 `build_extract_prompt()` (standard spec mode)
**Lines**: 82-158 | **Output**: extraction.md

- Requests **13 frontmatter fields** (matching EXTRACT_GATE exactly)
- Requests **8 body sections**: Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions
- Optional `retrospective_content` appended as advisory-only context (RSK-004)
- Ends with `_OUTPUT_FORMAT_BLOCK` enforcing frontmatter-first output

### 4.2 `build_extract_prompt_tdd()` (TDD mode)
**Lines**: 161-285 | **Output**: extraction.md

- Requests **19 frontmatter fields**: 13 standard + 6 TDD-specific:
  - `data_models_identified` (integer)
  - `api_surfaces_identified` (integer)
  - `components_identified` (integer)
  - `test_artifacts_identified` (integer)
  - `migration_items_identified` (integer)
  - `operational_items_identified` (integer)
- Requests **14 body sections**: 8 standard + 6 TDD-specific:
  - Data Models and Interfaces
  - API Specifications
  - Component Inventory
  - Testing Strategy
  - Migration and Rollout Plan
  - Operational Readiness
- Same retrospective advisory and output format as standard

### 4.3 `build_spec_fidelity_prompt()`
**Lines**: 448-525

- Role: "source-document fidelity analyst"
- **11 comparison dimensions**:
  1. Signatures
  2. Data Models
  3. Gates
  4. CLI Options
  5. NFRs
  6. Integration Wiring Completeness (from `_INTEGRATION_WIRING_DIMENSION`)
  7. API Endpoints
  8. Component Inventory
  9. Testing Strategy
  10. Migration & Rollout
  11. Operational Readiness
- **Severity definitions** embedded (RSK-007 mitigation): HIGH/MEDIUM/LOW with concrete examples
- Requests **6 frontmatter fields** matching SPEC_FIDELITY_GATE
- Body requires: Deviation Report (DEV-NNN entries with Severity, Source Quote, Roadmap Quote, Impact, Recommended Correction) + Summary

### 4.4 `build_test_strategy_prompt()`
**Lines**: 586-629

- Requests **6 frontmatter fields** in prompt: `complexity_class`, `validation_philosophy`, `validation_milestones`, `work_milestones`, `interleave_ratio`, `major_issue_policy`
- **Gate requires 9 fields** (adds `spec_source`, `generated`, `generator`) -- prompt/gate mismatch

---

## 5. ALL_GATES Pipeline Order

From `ALL_GATES` list (lines 1084-1099):

| # | Step ID | Gate Constant | Tier | Frontmatter Fields | Semantic Checks |
|---|---------|--------------|------|-------------------|-----------------|
| 1 | extract | EXTRACT_GATE | STRICT | 13 | 2 |
| 2 | generate-A | GENERATE_A_GATE | STRICT | 3 | 2 |
| 3 | generate-B | GENERATE_B_GATE | STRICT | 3 | 2 |
| 4 | diff | DIFF_GATE | STANDARD | 2 | 0 |
| 5 | debate | DEBATE_GATE | STRICT | 2 | 1 |
| 6 | score | SCORE_GATE | STANDARD | 2 | 0 |
| 7 | merge | MERGE_GATE | STRICT | 3 | 3 |
| 8 | anti-instinct | ANTI_INSTINCT_GATE | STRICT | 3 | 3 |
| 9 | test-strategy | TEST_STRATEGY_GATE | STRICT | 9 | 5 |
| 10 | spec-fidelity | SPEC_FIDELITY_GATE | STRICT | 6 | 2 |
| 11 | wiring-verification | WIRING_GATE | STRICT | 16 | 5 |
| 12 | deviation-analysis | DEVIATION_ANALYSIS_GATE | STRICT | 9 | 7 |
| 13 | remediate | REMEDIATE_GATE | STRICT | 6 | 2 |
| 14 | certify | CERTIFY_GATE | STRICT | 5 | 3 |

---

## 6. Known Issues / Discrepancies for E2E Testing

1. **B-1: DEVIATION_ANALYSIS field mismatch** (gates.py line 16): Required frontmatter has `ambiguous_count` but semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations`. Tests must emit BOTH fields or the semantic check fails.

2. **TEST_STRATEGY prompt/gate mismatch**: Prompt requests 6 fields, gate requires 9 (missing `spec_source`, `generated`, `generator` from prompt). E2E tests should verify whether the executor injects these fields or if this is a latent bug.

3. **DEVIATION_ANALYSIS TDD incompatibility**: Explicitly marked not TDD-compatible (line 15). The deviation analysis step was designed for spec-mode only. TDD pipelines should skip or adapt this gate.

4. **cross_refs_resolve is warning-only**: `_cross_refs_resolve` always returns True (line 87). It warns on unresolved refs but never blocks. Tests should not expect this check to fail a gate.

5. **Fingerprint empty passthrough**: When no code-level identifiers are extracted from the spec, `fingerprint_gate_passed()` returns True with ratio 1.0. E2E tests with minimal specs will auto-pass the fingerprint portion of ANTI_INSTINCT_GATE.

---

## Summary

This document catalogues all 14 gates in the roadmap pipeline with their exact frontmatter fields, semantic check functions, pass/fail thresholds, and enforcement tiers. Key findings for E2E test construction:

- All gates except DIFF and SCORE are STRICT tier
- The heaviest gates are DEVIATION_ANALYSIS (7 semantic checks), TEST_STRATEGY and WIRING (5 each)
- Two prompt/gate mismatches exist (TEST_STRATEGY missing 3 fields, DEVIATION_ANALYSIS field name mismatch B-1)
- Fingerprint coverage threshold is 0.7 (70%) with an empty-set passthrough
- SPEC_FIDELITY pass requires high_severity_count == 0 and consistency between tasklist_ready and severity counts
- WIRING_GATE is the only gate defined outside gates.py (in audit/wiring_gate.py)
