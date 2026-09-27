---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-source-fidelity"
title: "qa-source-fidelity_template"
description: "Shared report template for the /task Fidelity Gate's per-source semantic-fidelity assessment (semantic coverage, detail preservation, phantom-coverage check, operational completeness) of an assembled output against its cited source documents."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.6"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: "SPEC-1-templated-reports-canonical-rule-20260701.md s2 L33 (Group 1 row 5)"
related_docs:
  - ".claude/skills/task/SKILL.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - qa-report
  - template
  - fidelity-gate
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "QA Source Fidelity"
template_version: "1.0.0"
sections: 5
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-source-fidelity-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the /task Fidelity Gate's source-document fidelity report. It checks
whether an assembled output preserves the semantic meaning, detail, and
operational completeness of the source documents it was built from, and
whether it introduces phantom coverage (claims not supported by any source).

SCOPE:
This template covers ONLY the source-vs-output fidelity check. It does NOT
cover cross-source-only contradiction checks (that is
qa-cross-source-contradictions_template.md, which never reads the output).

THE SECTIONS (fixed order, all 5 required):
1. Sources Reviewed -- proves every source document was actually read
2. Per-Source Fidelity -- the four-dimension assessment table
3. Overall Verdict -- PASS or FAIL for the gate
4. Issues Found -- fidelity gaps by severity
5. QA Complete -- closing marker plus the final VERDICT line

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row in each table

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Each of the four fidelity dimensions (semantic coverage, detail
  preservation, phantom-coverage check, operational completeness) MUST be
  its own column in the Per-Source Fidelity table, never merged
- Verdict is EXACTLY one of: PASS | FAIL
################################################################################ -->

## PART 2: THE QA SOURCE FIDELITY SCAFFOLD (copy everything below this line)

# QA Source Fidelity - {{RF_PLACEHOLDER:PHASE}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** source-fidelity
- **Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}} / 3

## Sources Reviewed

| Source Doc | Assigned Section Range | Line Count |
|------------|--------------------------|------------|
| {{RF_PLACEHOLDER:SOURCE_PATH}} | {{RF_PLACEHOLDER:SOURCE_SECTION_RANGE}} | {{RF_PLACEHOLDER:SOURCE_LINE_COUNT}} |
{{RF_PLACEHOLDER:SOURCES_REVIEWED_ROW}}

<!-- One row per source document assigned to this gate; proves the source was read. -->

## Per-Source Fidelity

| Source | Semantic Coverage | Detail Preservation | Phantom-Coverage Check | Operational Completeness | Verdict |
|--------|---------------------|------------------------|---------------------------|------------------------------|---------|
| {{RF_PLACEHOLDER:FIDELITY_SOURCE}} | {{RF_PLACEHOLDER:FIDELITY_SEMANTIC_COVERAGE}} | {{RF_PLACEHOLDER:FIDELITY_DETAIL_PRESERVATION}} | {{RF_PLACEHOLDER:FIDELITY_PHANTOM_COVERAGE}} | {{RF_PLACEHOLDER:FIDELITY_OPERATIONAL_COMPLETENESS}} | {{RF_PLACEHOLDER:FIDELITY_VERDICT}} |
{{RF_PLACEHOLDER:PER_SOURCE_FIDELITY_ROW}}

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

<!-- Verdict enum: PASS | FAIL -->

## Issues Found

| # | Severity | Source | Issue | Required Fix |
|---|----------|--------|-------|---------------|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:ISSUE_SEVERITY}} | {{RF_PLACEHOLDER:ISSUE_SOURCE}} | {{RF_PLACEHOLDER:ISSUE_DESCRIPTION}} | {{RF_PLACEHOLDER:ISSUE_REQUIRED_FIX}} |
{{RF_PLACEHOLDER:ISSUES_FOUND_ROW}}

<!-- Severity enum: CRITICAL | IMPORTANT | MINOR -->

## QA Complete

VERDICT: {{RF_PLACEHOLDER:FINAL_VERDICT}}
