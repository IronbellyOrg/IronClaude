# 05 Gate Architecture -- Roadmap Pipeline

Status: Complete
Investigator: Claude Opus 4.6
Date: 2026-04-04
Investigation Type: Code Tracer

## Source Files

| File | Role |
|------|------|
| `src/superclaude/cli/roadmap/gates.py` | 14 gate constants + 31 semantic check functions |
| `src/superclaude/cli/audit/wiring_gate.py` | WIRING_GATE constant + 5 semantic check functions |
| `src/superclaude/cli/pipeline/gates.py` | Generic `gate_passed()` + `_check_frontmatter()` enforcement engine |
| `src/superclaude/cli/pipeline/models.py` | `GateMode`, `GateCriteria`, `SemanticCheck` dataclasses |
| `src/superclaude/cli/pipeline/trailing_gate.py` | `TrailingGateRunner`, `GateResultQueue`, remediation infrastructure |
| `src/superclaude/cli/roadmap/executor.py` | Step definitions mapping gates to pipeline steps |

---

## Gate Enforcement Engine

### Enforcement Tiers (pipeline/gates.py `gate_passed()`)

| Tier | Checks Applied |
|------|---------------|
| **EXEMPT** | Always passes. No checks. |
| **LIGHT** | File exists + non-empty |
| **STANDARD** | LIGHT + min_lines + YAML frontmatter field presence |
| **STRICT** | STANDARD + all semantic checks must pass |

### Frontmatter Detection (`_check_frontmatter`)

Uses regex `^---[ \t]*\n((?:[ \t]*\w[\w\s]*:.*\n)+)---[ \t]*$` with `re.MULTILINE`. This means:
- Frontmatter does NOT have to be at byte 0 -- it can appear after conversational preamble
- Horizontal rules (`---` with no key:value content) are rejected
- Only checks field **presence**, not value validity (value checks are semantic checks)

### GateMode (pipeline/models.py)

| Mode | Behavior |
|------|----------|
| **BLOCKING** (default) | Step must pass gate before next step begins |
| **TRAILING** | Step runs but does not block subsequent steps; failures evaluated after grace period |

Only one step uses TRAILING mode: `wiring-verification`.

---

## Per-Gate Analysis

### ALL_GATES Pipeline Order (from `gates.py` lines 1124-1139)

The `ALL_GATES` list defines 14 entries. The `EXTRACT_TDD_GATE` is a conditional alternative to `EXTRACT_GATE` (not separately listed).

---

### Gate 1: EXTRACT_GATE

| Property | Value |
|----------|-------|
| **Constant** | `EXTRACT_GATE` |
| **Step ID** | `extract` (when `input_type != "tdd"`) |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 50 |
| **Frontmatter Fields (13)** | `spec_source`, `generated`, `generator`, `functional_requirements`, `nonfunctional_requirements`, `total_requirements`, `complexity_score`, `complexity_class`, `domains_detected`, `risks_identified`, `dependencies_identified`, `success_criteria_count`, `extraction_mode` |
| **Semantic Checks (2)** | `complexity_class_valid` -- must be LOW/MEDIUM/HIGH; `extraction_mode_valid` -- must be "standard" or start with "chunked" |

**Would break if format changes:** YES. The 13 frontmatter fields are tightly coupled to the extraction prompt's one-shot output format. Template-driven output would need to emit identical frontmatter keys or the gate must be updated. Semantic checks on `complexity_class` and `extraction_mode` are value-format-dependent.

---

### Gate 1b: EXTRACT_TDD_GATE

| Property | Value |
|----------|-------|
| **Constant** | `EXTRACT_TDD_GATE` |
| **Step ID** | `extract` (when `input_type == "tdd"`) |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 50 |
| **Frontmatter Fields (19)** | All 13 from EXTRACT_GATE + `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified` |
| **Semantic Checks (2)** | Same as EXTRACT_GATE: `complexity_class_valid`, `extraction_mode_valid` |

**Would break if format changes:** YES. Same as EXTRACT_GATE plus 6 additional TDD-specific fields. Even more tightly coupled.

---

### Gate 2: GENERATE_A_GATE

| Property | Value |
|----------|-------|
| **Constant** | `GENERATE_A_GATE` |
| **Step ID** | `generate-{agent_a.id}` (typically `generate-haiku-architect`) |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 100 |
| **Frontmatter Fields (3)** | `spec_source`, `complexity_score`, `primary_persona` |
| **Semantic Checks (2)** | `frontmatter_values_non_empty` -- all FM values must be non-empty; `has_actionable_content` -- at least one `- ` or `1. ` list item |

**Would break if format changes:** MAYBE. Frontmatter is minimal (3 fields). The `has_actionable_content` check just looks for list items anywhere in content, so template-driven output would pass if it contains any markdown lists. Low risk.

---

### Gate 3: GENERATE_B_GATE

| Property | Value |
|----------|-------|
| **Constant** | `GENERATE_B_GATE` |
| **Step ID** | `generate-{agent_b.id}` (typically `generate-opus-architect`) |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 100 |
| **Frontmatter Fields (3)** | `spec_source`, `complexity_score`, `primary_persona` |
| **Semantic Checks (2)** | Same as GENERATE_A_GATE |

**Would break if format changes:** MAYBE. Same assessment as GENERATE_A_GATE.

---

### Gate 4: DIFF_GATE

| Property | Value |
|----------|-------|
| **Constant** | `DIFF_GATE` |
| **Step ID** | `diff` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STANDARD |
| **Min Lines** | 30 |
| **Frontmatter Fields (2)** | `total_diff_points`, `shared_assumptions_count` |
| **Semantic Checks** | None |

**Would break if format changes:** MAYBE. Only checks 2 frontmatter fields and min lines. If diff output still emits those fields, it passes. Low risk but depends on whether diff step output format changes.

---

### Gate 5: DEBATE_GATE

| Property | Value |
|----------|-------|
| **Constant** | `DEBATE_GATE` |
| **Step ID** | `debate` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 50 |
| **Frontmatter Fields (2)** | `convergence_score`, `rounds_completed` |
| **Semantic Checks (1)** | `convergence_score_valid` -- must parse as float in [0.0, 1.0] |

**Would break if format changes:** MAYBE. Light requirements. Only breaks if debate output drops the `convergence_score` frontmatter field or format.

---

### Gate 6: SCORE_GATE

| Property | Value |
|----------|-------|
| **Constant** | `SCORE_GATE` |
| **Step ID** | `score` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STANDARD |
| **Min Lines** | 20 |
| **Frontmatter Fields (2)** | `base_variant`, `variant_scores` |
| **Semantic Checks** | None |

**Would break if format changes:** NO (unlikely). STANDARD tier with 2 fields and no semantic checks. Very resilient.

---

### Gate 7: MERGE_GATE

| Property | Value |
|----------|-------|
| **Constant** | `MERGE_GATE` |
| **Step ID** | `merge` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 150 |
| **Frontmatter Fields (3)** | `spec_source`, `complexity_score`, `adversarial` |
| **Semantic Checks (3)** | `no_heading_gaps` -- heading levels increment by at most 1; `cross_refs_resolve` -- cross-references have matching headings (warning-only, always returns True); `no_duplicate_headings` -- no duplicate H2/H3 text |

**Would break if format changes:** YES (structural checks). The semantic checks validate markdown structure (heading hierarchy, duplicates). Template-driven output that changes heading structure could trigger `no_heading_gaps` or `no_duplicate_headings`. The `cross_refs_resolve` check is warning-only (always returns True per OQ-001).

---

### Gate 8: ANTI_INSTINCT_GATE

| Property | Value |
|----------|-------|
| **Constant** | `ANTI_INSTINCT_GATE` |
| **Step ID** | `anti-instinct` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 10 |
| **Frontmatter Fields (3)** | `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage` |
| **Semantic Checks (3)** | `no_undischarged_obligations` -- `undischarged_obligations` must be 0; `integration_contracts_covered` -- `uncovered_contracts` must be 0; `fingerprint_coverage_check` -- `fingerprint_coverage` >= 0.7 |
| **Notes** | Non-LLM deterministic step (prompt is empty string). Format-agnostic per TDD compatibility notes. |

**Would break if format changes:** NO. This is a non-LLM deterministic step that generates its own output. It reads the spec and roadmap as inputs but produces its own frontmatter. Gate validates that output, not LLM-generated content.

---

### Gate 9: TEST_STRATEGY_GATE

| Property | Value |
|----------|-------|
| **Constant** | `TEST_STRATEGY_GATE` |
| **Step ID** | `test-strategy` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 40 |
| **Frontmatter Fields (9)** | `spec_source`, `generated`, `generator`, `complexity_class`, `validation_philosophy`, `validation_milestones`, `work_milestones`, `interleave_ratio`, `major_issue_policy` |
| **Semantic Checks (5)** | `complexity_class_valid` -- LOW/MEDIUM/HIGH; `interleave_ratio_consistent` -- must match complexity (LOW->1:3, MEDIUM->1:2, HIGH->1:1); `milestone_counts_positive` -- both milestone counts > 0; `validation_philosophy_correct` -- must be exactly "continuous-parallel"; `major_issue_policy_correct` -- must be exactly "stop-and-fix" |

**Would break if format changes:** YES. 9 frontmatter fields with 5 semantic checks including cross-field consistency (interleave_ratio must match complexity_class). Tight coupling to specific frontmatter values. Template-driven output must replicate exact field names and value formats.

---

### Gate 10: SPEC_FIDELITY_GATE

| Property | Value |
|----------|-------|
| **Constant** | `SPEC_FIDELITY_GATE` |
| **Step ID** | `spec-fidelity` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 20 |
| **Frontmatter Fields (6)** | `high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready` |
| **Semantic Checks (2)** | `high_severity_count_zero` -- must be integer 0 (TypeError raised if unparseable); `tasklist_ready_consistent` -- if tasklist_ready=true, requires high_severity_count=0 AND validation_complete=true |
| **Notes** | Gate is set to `None` when `config.convergence_enabled` is True (gate bypassed in convergence mode). |

**Would break if format changes:** YES. The semantic checks enforce cross-field consistency (tasklist_ready requires both other fields to have specific values). All 6 fields must be present with correct types.

---

### Gate 11: WIRING_GATE (from audit/wiring_gate.py)

| Property | Value |
|----------|-------|
| **Constant** | `WIRING_GATE` (imported from `..audit.wiring_gate`) |
| **Step ID** | `wiring-verification` |
| **GateMode** | **TRAILING** (only trailing gate in the pipeline) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 10 |
| **Frontmatter Fields (16)** | `gate`, `target_dir`, `files_analyzed`, `rollout_mode`, `analysis_complete`, `unwired_callable_count`, `orphan_module_count`, `unwired_registry_count`, `critical_count`, `major_count`, `info_count`, `total_findings`, `blocking_findings`, `whitelist_entries_applied`, `files_skipped`, `audit_artifacts_used` |
| **Semantic Checks (5)** | `analysis_complete_true`; `recognized_rollout_mode` -- shadow/soft/full; `finding_counts_consistent` -- total == unwired + orphan + registry; `severity_summary_consistent` -- total == critical + major + info; `zero_blocking_findings_for_mode` -- blocking_findings must be 0 |

**Would break if format changes:** NO. This is a non-LLM step that generates its own structured output via the wiring analysis engine. Its frontmatter is emitted by `emit_report()` in `wiring_gate.py`, not by LLM prompts. Gate validates its own output format.

---

### Gate 12: DEVIATION_ANALYSIS_GATE

| Property | Value |
|----------|-------|
| **Constant** | `DEVIATION_ANALYSIS_GATE` |
| **Step ID** | `deviation-analysis` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 20 |
| **Frontmatter Fields (9)** | `schema_version`, `total_analyzed`, `slip_count`, `intentional_count`, `pre_approved_count`, `ambiguous_count`, `routing_fix_roadmap`, `routing_no_action`, `analysis_complete` |
| **Semantic Checks (7)** | `no_ambiguous_deviations` -- ambiguous_deviations must be 0; `validation_complete_true` -- analysis_complete must be true; `routing_ids_valid` -- all routing IDs match `DEV-\d+`; `slip_count_matches_routing` -- slip_count == count of IDs in routing_fix_roadmap; `pre_approved_not_in_fix_roadmap` -- no overlap between routing_no_action and routing_fix_roadmap; `total_analyzed_consistent` -- total == slip + intentional + pre_approved + ambiguous; `deviation_counts_reconciled` -- total unique routed IDs == total_analyzed (SC-008) |
| **Notes** | Non-LLM deterministic step. NOT TDD-compatible per comment at top of gates.py. Known bug B-1: ambiguous_count/ambiguous_deviations field mismatch. |

**Would break if format changes:** NO (for roadmap output changes). This is a non-LLM step that reads spec-fidelity output and produces its own structured output. However, it DOES depend on the spec-fidelity output format as INPUT. If spec-fidelity output changes, this step's analyzer could break even though its gate validates its own output.

---

### Gate 13: REMEDIATE_GATE

| Property | Value |
|----------|-------|
| **Constant** | `REMEDIATE_GATE` |
| **Step ID** | `remediate` |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 10 |
| **Frontmatter Fields (6)** | `type`, `source_report`, `source_report_hash`, `total_findings`, `actionable`, `skipped` |
| **Semantic Checks (2)** | `frontmatter_values_non_empty` -- all FM values non-empty; `all_actionable_have_status` -- all unchecked `F-XX` entries have FIXED or FAILED status (not PENDING) |

**Would break if format changes:** NO. Non-LLM deterministic step that generates its own output. The `all_actionable_have_status` check looks for a specific checklist format (`- [ ] F-XX | file | STATUS -- desc`) which is emitted by the remediation engine, not LLM.

---

### Gate 14: CERTIFY_GATE

| Property | Value |
|----------|-------|
| **Constant** | `CERTIFY_GATE` |
| **Step ID** | `certify` (constructed dynamically after remediate) |
| **GateMode** | BLOCKING (default) |
| **Enforcement Tier** | STRICT |
| **Min Lines** | 15 |
| **Frontmatter Fields (5)** | `findings_verified`, `findings_passed`, `findings_failed`, `certified`, `certification_date` |
| **Semantic Checks (3)** | `frontmatter_values_non_empty`; `per_finding_table_present` -- must contain markdown table with columns Finding/Severity/Result/Justification and at least one `F-XX` data row; `certified_is_true` -- `certified` must be "true" (case-insensitive) |

**Would break if format changes:** MAYBE. The certify step is LLM-driven (has a prompt). The `per_finding_table_present` check looks for a specific table format. If the LLM prompt changes to template-driven output, the table format must be preserved.

---

## Summary Table

| # | Gate Name | Step ID | GateMode | Tier | FM Fields | Semantic Checks | Would Break? |
|---|-----------|---------|----------|------|-----------|----------------|-------------|
| 1 | EXTRACT_GATE | extract | BLOCKING | STRICT | 13 | 2 | YES |
| 1b | EXTRACT_TDD_GATE | extract (tdd) | BLOCKING | STRICT | 19 | 2 | YES |
| 2 | GENERATE_A_GATE | generate-{A} | BLOCKING | STRICT | 3 | 2 | MAYBE |
| 3 | GENERATE_B_GATE | generate-{B} | BLOCKING | STRICT | 3 | 2 | MAYBE |
| 4 | DIFF_GATE | diff | BLOCKING | STANDARD | 2 | 0 | MAYBE |
| 5 | DEBATE_GATE | debate | BLOCKING | STRICT | 2 | 1 | MAYBE |
| 6 | SCORE_GATE | score | BLOCKING | STANDARD | 2 | 0 | NO |
| 7 | MERGE_GATE | merge | BLOCKING | STRICT | 3 | 3 | YES |
| 8 | ANTI_INSTINCT_GATE | anti-instinct | BLOCKING | STRICT | 3 | 3 | NO |
| 9 | TEST_STRATEGY_GATE | test-strategy | BLOCKING | STRICT | 9 | 5 | YES |
| 10 | SPEC_FIDELITY_GATE | spec-fidelity | BLOCKING | STRICT | 6 | 2 | YES |
| 11 | WIRING_GATE | wiring-verification | TRAILING | STRICT | 16 | 5 | NO |
| 12 | DEVIATION_ANALYSIS_GATE | deviation-analysis | BLOCKING | STRICT | 9 | 7 | NO |
| 13 | REMEDIATE_GATE | remediate | BLOCKING | STRICT | 6 | 2 | NO |
| 14 | CERTIFY_GATE | certify | BLOCKING | STRICT | 5 | 3 | MAYBE |

**Totals:** 15 gate constants (including EXTRACT_TDD_GATE), 36 semantic check instances (some functions reused), 31 unique checker functions (26 in roadmap/gates.py + 5 in audit/wiring_gate.py).

---

## Checker Function Inventory

### roadmap/gates.py -- 26 unique functions

| Function | Used By | What It Checks |
|----------|---------|---------------|
| `_no_heading_gaps` | MERGE | Heading levels increment by at most 1 |
| `_cross_refs_resolve` | MERGE | Cross-references resolve to headings (warning-only, always True) |
| `_no_duplicate_headings` | MERGE | No duplicate H2/H3 heading text |
| `_frontmatter_values_non_empty` | GENERATE_A, GENERATE_B, REMEDIATE, CERTIFY | All FM field values are non-empty strings |
| `_has_actionable_content` | GENERATE_A, GENERATE_B | At least one bulleted or numbered list item |
| `_high_severity_count_zero` | SPEC_FIDELITY | `high_severity_count` is integer 0 |
| `_has_per_finding_table` | CERTIFY | Table with Finding/Severity/Result/Justification + F-XX rows |
| `_all_actionable_have_status` | REMEDIATE | All unchecked F-XX entries have FIXED/FAILED status |
| `_tasklist_ready_consistent` | SPEC_FIDELITY | tasklist_ready=true requires high_severity=0 + validation_complete=true |
| `_no_undischarged_obligations` | ANTI_INSTINCT | `undischarged_obligations` is 0 |
| `_integration_contracts_covered` | ANTI_INSTINCT | `uncovered_contracts` is 0 |
| `_fingerprint_coverage_check` | ANTI_INSTINCT | `fingerprint_coverage` >= 0.7 |
| `_convergence_score_valid` | DEBATE | `convergence_score` is float in [0.0, 1.0] |
| `_no_ambiguous_deviations` | DEVIATION_ANALYSIS | `ambiguous_deviations` is 0 |
| `_certified_is_true` | CERTIFY | `certified` is "true" (case-insensitive) |
| `_validation_complete_true` | DEVIATION_ANALYSIS | `analysis_complete` is "true" |
| `_routing_ids_valid` | DEVIATION_ANALYSIS | All routing IDs match `DEV-\d+` |
| `_slip_count_matches_routing` | DEVIATION_ANALYSIS | slip_count == len(routing_fix_roadmap IDs) |
| `_routing_consistent_with_slip_count` | (alias, unused directly) | Alias for `_slip_count_matches_routing` |
| `_pre_approved_not_in_fix_roadmap` | DEVIATION_ANALYSIS | No overlap between routing_no_action and routing_fix_roadmap |
| `_total_analyzed_consistent` | DEVIATION_ANALYSIS | total == slip + intentional + pre_approved + ambiguous |
| `_total_annotated_consistent` | (defined but unused) | total_annotated == slip + intentional + pre_approved (optional) |
| `_deviation_counts_reconciled` | DEVIATION_ANALYSIS | Unique routed IDs count == total_analyzed |
| `_complexity_class_valid` | EXTRACT, EXTRACT_TDD, TEST_STRATEGY | complexity_class in {LOW, MEDIUM, HIGH} |
| `_extraction_mode_valid` | EXTRACT, EXTRACT_TDD | extraction_mode is "standard" or starts with "chunked" |
| `_interleave_ratio_consistent` | TEST_STRATEGY | ratio matches complexity: LOW->1:3, MEDIUM->1:2, HIGH->1:1 |
| `_milestone_counts_positive` | TEST_STRATEGY | validation_milestones and work_milestones > 0 |
| `_validation_philosophy_correct` | TEST_STRATEGY | Must be exactly "continuous-parallel" |
| `_major_issue_policy_correct` | TEST_STRATEGY | Must be exactly "stop-and-fix" |

### audit/wiring_gate.py -- 5 unique functions

| Function | Used By | What It Checks |
|----------|---------|---------------|
| `_analysis_complete_true` | WIRING | `analysis_complete` is "true" |
| `_recognized_rollout_mode` | WIRING | `rollout_mode` in {shadow, soft, full} |
| `_finding_counts_consistent` | WIRING | total == unwired + orphan + registry |
| `_severity_summary_consistent` | WIRING | total == critical + major + info |
| `_zero_blocking_findings_for_mode` | WIRING | `blocking_findings` is 0 |

### Helper functions (not semantic checks)

| Function | File | Purpose |
|----------|------|---------|
| `_parse_frontmatter` | roadmap/gates.py | Extract YAML FM key-value pairs (used by most semantic checks) |
| `_strip_yaml_quotes` | roadmap/gates.py | Strip matching outer quotes from FM values |
| `_extract_frontmatter_values` | audit/wiring_gate.py | Local FM parser for wiring gate (separate implementation) |
| `_check_frontmatter` | pipeline/gates.py | Regex-based FM field presence check (the enforcement engine) |

---

## Gaps and Questions

1. **Two frontmatter parsers.** `_parse_frontmatter` in roadmap/gates.py requires frontmatter at byte 0 (`content.lstrip().startswith("---")`). `_check_frontmatter` in pipeline/gates.py uses `re.MULTILINE` and allows frontmatter anywhere after conversational preamble. This means the enforcement engine can find frontmatter that the semantic checks cannot -- a semantic check could fail on valid content if the LLM emits preamble before `---`. This is a latent bug for any step where both are applied (all STRICT gates).

2. **Field name mismatch (B-1).** The DEVIATION_ANALYSIS_GATE requires frontmatter field `ambiguous_count` but the semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations`. These are different field names. The gate checks field presence for `ambiguous_count` and semantic check reads `ambiguous_deviations`. If the output has `ambiguous_count: 0` but not `ambiguous_deviations`, the frontmatter check passes but the semantic check fails. Documented in comment at top of gates.py as known bug B-1.

3. **Unused functions.** `_routing_consistent_with_slip_count` is an alias never used in any gate. `_total_annotated_consistent` is defined but not registered on any gate.

4. **`_cross_refs_resolve` is no-op.** Always returns True (warning-only mode per OQ-001). Could be removed without behavioral change.

5. **Convergence mode gate bypass.** When `config.convergence_enabled` is True, SPEC_FIDELITY_GATE is set to `None`, completely bypassing validation. This means in convergence mode, the pipeline has no spec-fidelity quality gate.

---

## Stale Documentation Found

- The comment "Step 8: Spec Fidelity" in executor.py (line 1444) reuses step number 8, same as "Step 8: Test Strategy" (line 1434). Spec-fidelity is actually step 9 or later in the pipeline sequence.
- The `_build_steps` docstring says "9-step pipeline" but the actual pipeline has 12+ steps (including anti-instinct, wiring-verification, deviation-analysis, remediate, and dynamically-added certify).
- TDD compatibility note says DEVIATION_ANALYSIS_GATE is "NOT TDD-compatible" but no code enforces this restriction.

---

## Impact Assessment for Format Migration

### High Risk (will definitely break -- YES gates)

These gates have many frontmatter fields and/or cross-field semantic consistency checks that are tightly coupled to the current one-shot LLM output format:

1. **EXTRACT_GATE / EXTRACT_TDD_GATE** -- 13/19 frontmatter fields each. Template must emit all fields.
2. **TEST_STRATEGY_GATE** -- 9 fields with 5 semantic checks including cross-field consistency.
3. **SPEC_FIDELITY_GATE** -- 6 fields with cross-field consistency (tasklist_ready depends on 2 other fields).
4. **MERGE_GATE** -- Structural markdown checks (heading hierarchy, no duplicates).

### Medium Risk (might break -- MAYBE gates)

5. **GENERATE_A/B_GATE** -- Only 3 fields, but `has_actionable_content` needs list items.
6. **DIFF_GATE / DEBATE_GATE** -- Light requirements, but still need specific frontmatter.
7. **CERTIFY_GATE** -- Needs specific table format in body.

### Low Risk (will not break -- NO gates)

8. **ANTI_INSTINCT_GATE** -- Non-LLM step, self-generates output.
9. **WIRING_GATE** -- Non-LLM step, self-generates output.
10. **DEVIATION_ANALYSIS_GATE** -- Non-LLM step, self-generates output (but depends on spec-fidelity INPUT format).
11. **REMEDIATE_GATE** -- Non-LLM step, self-generates output.
12. **SCORE_GATE** -- STANDARD tier, 2 fields, no semantic checks.

### Key Insight

The non-LLM deterministic steps (anti-instinct, wiring, deviation-analysis, remediate) are immune to output format changes because they generate their own output. However, they may break if the FORMAT OF THEIR INPUTS changes -- particularly deviation-analysis which reads spec-fidelity output, and remediate which reads deviation-analysis output. A format change to LLM-generated steps cascades through the deterministic steps via input dependencies, not gate checks.
