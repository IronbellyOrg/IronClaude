# Research: Gate Compatibility Analysis

**Investigation type:** Architecture Analyst
**Scope:** roadmap/gates.py, pipeline/gates.py, tasklist/gates.py
**Status:** Complete
**Date:** 2026-03-25

---

## Pipeline Gate Engine (`gate_passed()`)

Source: `src/superclaude/cli/pipeline/gates.py`

**Format-agnostic.** Tier behaviors:
- **EXEMPT** — always passes
- **LIGHT** — file exists + non-empty
- **STANDARD** — + min_lines + required frontmatter key presence
- **STRICT** — + semantic check functions (pure Python content → bool)

The gate engine is NOT spec-specific. Spec-specificity lives entirely in the field names and semantic checks attached to each gate definition.

---

## EXTRACT_GATE

**Required YAML fields (13):** `spec_source`, `generated`, `generator`, `functional_requirements`, `nonfunctional_requirements`, `total_requirements`, `complexity_score`, `complexity_class`, `domains_detected`, `risks_identified`, `dependencies_identified`, `success_criteria_count`, `extraction_mode`

**Semantic checks:**
1. `_complexity_class_valid` — `complexity_class` must be `LOW|MEDIUM|HIGH`
2. `_extraction_mode_valid` — `extraction_mode` must be `standard` or starts with `chunked`

**TDD Compatible:** CONDITIONAL — Claude receiving TDD content could still emit these fields if explicitly instructed, but `spec_source` is spec-labeled and requirement-count fields are spec-centric

**Changes needed:** Alias/rename `spec_source` → `source_document`; decide how TDD content maps to `functional_requirements`/`nonfunctional_requirements` counters; optionally add TDD-specific count fields

---

## GENERATE_A_GATE

**Required YAML fields (3):** `spec_source`, `complexity_score`, `primary_persona`

**Semantic checks:**
1. `_frontmatter_values_non_empty` — no empty values
2. `_has_actionable_content` — at least one markdown list item

**TDD Compatible:** CONDITIONAL — `spec_source` is the only blocker; roadmap can be TDD-derived and still be actionable

**Changes needed:** Alias/rename `spec_source`

---

## GENERATE_B_GATE

Same as GENERATE_A_GATE.

**TDD Compatible:** CONDITIONAL
**Changes needed:** Alias/rename `spec_source`

---

## DIFF_GATE

**Required YAML fields (2):** `total_diff_points`, `shared_assumptions_count`
**Semantic checks:** None
**TDD Compatible:** **YES** — comparison summary metadata; no spec-labeled fields
**Changes needed:** None

---

## DEBATE_GATE

**Required YAML fields (2):** `convergence_score`, `rounds_completed`
**Semantic checks:** `_convergence_score_valid` — float in [0.0, 1.0]
**TDD Compatible:** **YES** — debate convergence is independent of input type
**Changes needed:** None

---

## SCORE_GATE

**Required YAML fields (2):** `base_variant`, `variant_scores`
**Semantic checks:** None
**TDD Compatible:** **YES** — variant scoring is generic
**Changes needed:** None

---

## MERGE_GATE

**Required YAML fields (3):** `spec_source`, `complexity_score`, `adversarial`
**Semantic checks:**
1. `_no_heading_gaps` — heading levels don't skip (H2→H4 fails)
2. `_cross_refs_resolve` — "See section X" refs have matching headings (warning-only; returns True)
3. `_no_duplicate_headings` — no duplicate H2/H3 text

**TDD Compatible:** CONDITIONAL — heading checks are generic; `spec_source` is the only blocker

**Changes needed:** Alias/rename `spec_source`

---

## ANTI_INSTINCT_GATE

**Required YAML fields (3):** `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`
**Semantic checks:**
1. `_no_undischarged_obligations` — `undischarged_obligations == 0`
2. `_integration_contracts_covered` — `uncovered_contracts == 0`
3. `_fingerprint_coverage_check` — `fingerprint_coverage >= 0.7`

**TDD Compatible:** CONDITIONAL / likely NO unless analysis logic is refined

**Reasoning:** The gate metadata is syntactically generic but semantically fidelity-oriented:
- `fingerprint_coverage` failure message says "spec code-level identifiers insufficiently represented in roadmap" — spec-specific wording
- `uncovered_contracts` assumes spec-style integration contract extraction
- For TDD input: `integration_contracts.py` will extract from TDD §6 Architecture (likely works); `fingerprint.py` will extract MORE identifiers from TDD (may actually improve coverage); `obligation_scanner.py` scans roadmap (unaffected)
- Net effect: gate *may* pass more easily for TDD inputs due to richer identifier density

**Changes needed:** Generalize gate failure messages from "spec code-level identifiers" to "source-document code-level identifiers"; verify that `integration_contracts.py` TDD extraction produces meaningful results

---

## TEST_STRATEGY_GATE

**Required YAML fields (9):** `spec_source`, `generated`, `generator`, `complexity_class`, `validation_philosophy`, `validation_milestones`, `work_milestones`, `interleave_ratio`, `major_issue_policy`

**Semantic checks:**
1. `_complexity_class_valid` — `LOW|MEDIUM|HIGH`
2. `_interleave_ratio_consistent` — LOW→1:3, MEDIUM→1:2, HIGH→1:1
3. `_milestone_counts_positive` — both milestone fields > 0
4. `_validation_philosophy_correct` — exactly `continuous-parallel`
5. `_major_issue_policy_correct` — exactly `stop-and-fix`

**TDD Compatible:** CONDITIONAL — schema is mostly workflow-specific; `spec_source` is the only spec-labeled field; TDD-derived test strategy can still satisfy all semantic checks

**Changes needed:** Alias/rename `spec_source`

---

## SPEC_FIDELITY_GATE

**Required YAML fields (6):** `high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready`

**Semantic checks:**
1. `_high_severity_count_zero` — `high_severity_count == 0`
2. `_tasklist_ready_consistent` — if `tasklist_ready=true` then `high_severity_count==0` AND `validation_complete==true`

**TDD Compatible:** CONDITIONAL / conceptually NO as named

**Reasoning:** Gate code checks are generic deviation counts and readiness consistency. Could technically work for TDD fidelity if upstream step emits the same schema. But the gate is explicitly "spec fidelity" — semantically wrong for TDD.

**Changes needed:** Rename to `SOURCE_FIDELITY_GATE` or create parallel `TDD_FIDELITY_GATE`; code-level semantic checks can stay unchanged

---

## WIRING_GATE

Source: `src/superclaude/cli/audit/wiring_gate.py`

**Required YAML fields (16):** `gate`, `target_dir`, `files_analyzed`, `rollout_mode`, `analysis_complete`, `unwired_callable_count`, `orphan_module_count`, `unwired_registry_count`, `critical_count`, `major_count`, `info_count`, `total_findings`, `blocking_findings`, `whitelist_entries_applied`, `files_skipped`, `audit_artifacts_used`

**Semantic checks (5):** `analysis_complete==true`, `rollout_mode` in {shadow,soft,full}, finding counts consistent, severity summary consistent, `blocking_findings==0`

**TDD Compatible: YES** — analyzes code wiring, completely independent of whether source document is spec or TDD

**Changes needed:** None

---

## DEVIATION_ANALYSIS_GATE

**Required YAML fields (9):** `schema_version`, `total_analyzed`, `slip_count`, `intentional_count`, `pre_approved_count`, `ambiguous_count`, `routing_fix_roadmap`, `routing_no_action`, `analysis_complete`

**Semantic checks (7):** `_no_ambiguous_deviations` (checks `ambiguous_deviations==0`), `_validation_complete_true`, `_routing_ids_valid` (DEV-\d+ pattern), `_slip_count_matches_routing`, `_pre_approved_not_in_fix_roadmap`, `_total_analyzed_consistent`, `_deviation_counts_reconciled`

**TDD Compatible: NO** — strongly spec-coupled

**Spec-specific assumptions:**
- `routing_update_spec` is explicitly spec-specific (requires update to the spec document)
- `DEV-\d+` routing ID namespace assumes current spec-deviation tracking taxonomy
- Deviation routing model (slip/intentional/pre-approved/spec-update) assumes spec as remediation target

**Changes needed (Required):** Replace `routing_update_spec` with `routing_update_source` or support both; reconsider `DEV-\d+` ID pattern if TDD uses different namespace; clarify whether slip/intentional/pre-approved taxonomy applies to TDD-derived deviations

**Additional schema consistency issue:** Required field list includes `ambiguous_count` but semantic check `_no_ambiguous_deviations` reads `ambiguous_deviations` — possible mismatch regardless of TDD.

---

## REMEDIATE_GATE

**Required YAML fields (6):** `type`, `source_report`, `source_report_hash`, `total_findings`, `actionable`, `skipped`

**Semantic checks:**
1. `_frontmatter_values_non_empty` — no empty values
2. `_all_actionable_have_status` — all unchecked `- [ ] F-XX |` entries have status FIXED or FAILED

**TDD Compatible: YES** — validates remediation-tasklist structure; `source_report` can point to any report

**Changes needed:** None

---

## CERTIFY_GATE

**Required YAML fields (5):** `findings_verified`, `findings_passed`, `findings_failed`, `certified`, `certification_date`

**Semantic checks:**
1. `_frontmatter_values_non_empty`
2. `_has_per_finding_table` — requires table header `Finding | Severity | Result | Justification` + rows matching `| F-\d+ |`
3. `_certified_is_true` — `certified.lower() == "true"`

**TDD Compatible:** CONDITIONAL — gate is mostly generic but `_has_per_finding_table` hardcodes `F-\d+` row pattern

**Changes needed:** If TDD mode uses different finding IDs, relax regex to accept broader ID pattern; otherwise none

---

## TASKLIST_FIDELITY_GATE

Source: `src/superclaude/cli/tasklist/gates.py`

**Required YAML fields (6):** `high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready`

**Semantic checks:** `_high_severity_count_zero`, `_tasklist_ready_consistent` (same as SPEC_FIDELITY_GATE)

**TDD Compatible:** CONDITIONAL — structurally generic; semantically source-fidelity-oriented; can pass if upstream deviation analysis emits same schema

**Changes needed:** Prefer generic "source fidelity" naming or TDD-specific equivalent

---

## Summary Table

| Gate Name | Required Fields | Semantic Checks | TDD Compatible? | Changes Needed |
|---|---|---|---|---|
| EXTRACT_GATE | 13 | 2 | CONDITIONAL | Alias `spec_source`; map TDD content to requirement-count fields |
| GENERATE_A_GATE | 3 | 2 | CONDITIONAL | Alias `spec_source` |
| GENERATE_B_GATE | 3 | 2 | CONDITIONAL | Alias `spec_source` |
| DIFF_GATE | 2 | 0 | **YES** | None |
| DEBATE_GATE | 2 | 1 | **YES** | None |
| SCORE_GATE | 2 | 0 | **YES** | None |
| MERGE_GATE | 3 | 3 | CONDITIONAL | Alias `spec_source` |
| ANTI_INSTINCT_GATE | 3 | 3 | CONDITIONAL | Generalize failure messages; verify TDD contract/fingerprint output |
| TEST_STRATEGY_GATE | 9 | 5 | CONDITIONAL | Alias `spec_source` |
| SPEC_FIDELITY_GATE | 6 | 2 | CONDITIONAL | Rename to SOURCE_FIDELITY_GATE |
| WIRING_GATE | 16 | 5 | **YES** | None |
| DEVIATION_ANALYSIS_GATE | 9 | 7 | **NO** | Replace `routing_update_spec`; reconsider `DEV-\d+` and deviation taxonomy |
| REMEDIATE_GATE | 6 | 2 | **YES** | None |
| CERTIFY_GATE | 5 | 3 | CONDITIONAL | Relax `F-\d+` row check if TDD uses different finding IDs |
| TASKLIST_FIDELITY_GATE | 6 | 2 | CONDITIONAL | Generic naming preferred |

---

## Gaps and Questions

1. `spec_source` appears in EXTRACT, GENERATE_A, GENERATE_B, MERGE, TEST_STRATEGY gates — it is the most common blocker but if TDD outputs still emit this field (using TDD filename), many gates can pass unchanged
2. DEVIATION_ANALYSIS_GATE is the only gate with hard structural incompatibility (`routing_update_spec`, `DEV-\d+` IDs)
3. CERTIFY_GATE's `F-\d+` row expectation is an implicit ID convention that may conflict with TDD finding ID patterns
4. ANTI_INSTINCT_GATE will likely produce BETTER results for TDD inputs (more fingerprints, richer architecture contracts) — test this hypothesis before changing the gate
5. WIRING_GATE is completely orthogonal to input source type — safe without any changes

## Summary

**Three classes of gates:**
1. **Already TDD-compatible:** DIFF, DEBATE, SCORE, WIRING, REMEDIATE
2. **TDD-compatible if outputs preserve current schema:** EXTRACT, GENERATE_A/B, MERGE, TEST_STRATEGY, SPEC_FIDELITY, TASKLIST_FIDELITY, CERTIFY — primary blocker is `spec_source` field name and spec-oriented naming
3. **Requires schema/semantic redesign:** DEVIATION_ANALYSIS (structural incompatibility), ANTI_INSTINCT (needs verification)

The gate enforcement engine (`gate_passed()`) is format-agnostic. All incompatibilities are in gate-specific field requirements and semantic assumptions.
