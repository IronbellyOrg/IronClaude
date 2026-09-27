---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-analyst-completeness"
title: "analyst-completeness_report_template"
description: "Shared report template for the rf-analyst Research Completeness Verification output: coverage audit, evidence quality, documentation staleness, completeness, contradictions, compiled gaps, depth assessment, and recommendations."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.11"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/agents/rf-analyst.md:156-209 (Research Completeness Verification)"
related_docs:
  - ".claude/agents/rf-analyst.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - analyst-report
  - template
  - research-gate
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Analyst Completeness"
template_version: "1.0.0"
sections: 9
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-analyst-completeness-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task-builder" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the rf-analyst Research Completeness Verification output, the report
one or more rf-analyst agents produce at the /task-builder A.8 research
quality gate (before rf-qa runs its own structural/gap lenses in parallel).

SCOPE:
This template covers ONLY the Research Completeness Verification analysis
type. Other rf-analyst analysis types (Cross-Validation, Synthesis Quality
Review, Gap Analysis, Coverage Audit) use their own templates.

THE SECTIONS (header block plus 9 required `##` sections, fixed order):
- header block (Topic, Date, Files analyzed, Depth tier) -- prose, not a counted section
1. Verdict -- PASS or FAIL, with gap count
2. Coverage Audit -- Scope Item / Covered By / Status table
3. Evidence Quality -- Research File / Evidenced Claims / Unsupported Claims / Quality Rating table
4. Documentation Staleness -- Claim / Source Doc / Verification Tag / Status table
5. Completeness -- Research File / Status / Summary / Gaps Section / Key Takeaways / Rating table
6. Contradictions Found -- bullet list, each citing both files
7. Compiled Gaps -- three `###` sub-sections: Critical Gaps (block synthesis), Important Gaps (affect quality), Minor Gaps (must still be fixed)
8. Depth Assessment -- Expected depth / Actual depth achieved / Missing depth elements
9. Recommendations -- specific actions to address gaps before proceeding

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row in each table

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Every table uses the exact column set from rf-analyst.md:156-209, never
  merged or renamed
- Quality Rating is EXACTLY one of: Strong | Adequate | Weak
- Completeness Rating is EXACTLY one of: Complete | Incomplete
################################################################################ -->

## PART 2: THE ANALYST COMPLETENESS SCAFFOLD (copy everything below this line)

# Research Completeness Verification

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Files analyzed:** {{RF_PLACEHOLDER:FILES_ANALYZED_COUNT}}
- **Depth tier:** {{RF_PLACEHOLDER:DEPTH_TIER}}

---

## Verdict: {{RF_PLACEHOLDER:VERDICT}}

<!-- Verdict enum: PASS | FAIL, with a gap count e.g. "FAIL, 3 gaps" -->

## Coverage Audit

| Scope Item | Covered By | Status |
|-----------|-----------|--------|
| {{RF_PLACEHOLDER:COVERAGE_SCOPE_ITEM}} | {{RF_PLACEHOLDER:COVERAGE_COVERED_BY}} | {{RF_PLACEHOLDER:COVERAGE_STATUS}} |
{{RF_PLACEHOLDER:COVERAGE_AUDIT_ROW}}

<!-- Status is EXACTLY one of: COVERED | GAP -->

## Evidence Quality

| Research File | Evidenced Claims | Unsupported Claims | Quality Rating |
|--------------|-----------------|-------------------|---------------|
| {{RF_PLACEHOLDER:EVIDENCE_FILE}} | {{RF_PLACEHOLDER:EVIDENCE_CLAIMS_COUNT}} | {{RF_PLACEHOLDER:EVIDENCE_UNSUPPORTED_COUNT}} | {{RF_PLACEHOLDER:EVIDENCE_QUALITY_RATING}} |
{{RF_PLACEHOLDER:EVIDENCE_QUALITY_ROW}}

<!-- Quality Rating is EXACTLY one of: Strong | Adequate | Weak -->

## Documentation Staleness

| Claim | Source Doc | Verification Tag | Status |
|-------|----------|-----------------|--------|
| {{RF_PLACEHOLDER:STALENESS_CLAIM}} | {{RF_PLACEHOLDER:STALENESS_SOURCE_DOC}} | {{RF_PLACEHOLDER:STALENESS_VERIFICATION_TAG}} | {{RF_PLACEHOLDER:STALENESS_STATUS}} |
{{RF_PLACEHOLDER:DOCUMENTATION_STALENESS_ROW}}

<!-- Status is EXACTLY one of: OK | FLAG. Verification Tag or the literal "MISSING". -->

## Completeness

| Research File | Status | Summary | Gaps Section | Key Takeaways | Rating |
|--------------|--------|---------|-------------|---------------|--------|
| {{RF_PLACEHOLDER:COMPLETENESS_FILE}} | {{RF_PLACEHOLDER:COMPLETENESS_STATUS}} | {{RF_PLACEHOLDER:COMPLETENESS_SUMMARY_PRESENT}} | {{RF_PLACEHOLDER:COMPLETENESS_GAPS_PRESENT}} | {{RF_PLACEHOLDER:COMPLETENESS_KEY_TAKEAWAYS_PRESENT}} | {{RF_PLACEHOLDER:COMPLETENESS_RATING}} |
{{RF_PLACEHOLDER:COMPLETENESS_ROW}}

<!-- Summary/Gaps Section/Key Takeaways columns are Y/N. Rating is EXACTLY one of: Complete | Incomplete -->

## Contradictions Found

{{RF_PLACEHOLDER:CONTRADICTIONS_FOUND_BODY}}

<!-- Bullet list; each contradiction cites both files involved -->

## Compiled Gaps

### Critical Gaps (block synthesis)

{{RF_PLACEHOLDER:CRITICAL_GAPS_BODY}}

### Important Gaps (affect quality)

{{RF_PLACEHOLDER:IMPORTANT_GAPS_BODY}}

### Minor Gaps (must still be fixed)

{{RF_PLACEHOLDER:MINOR_GAPS_BODY}}

## Depth Assessment

- **Expected depth:** {{RF_PLACEHOLDER:DEPTH_EXPECTED}}
- **Actual depth achieved:** {{RF_PLACEHOLDER:DEPTH_ACTUAL}}
- **Missing depth elements:** {{RF_PLACEHOLDER:DEPTH_MISSING_ELEMENTS}}

## Recommendations

{{RF_PLACEHOLDER:RECOMMENDATIONS_BODY}}
