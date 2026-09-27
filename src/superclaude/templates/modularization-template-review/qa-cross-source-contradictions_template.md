---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-cross-source-contradictions"
title: "qa-cross-source-contradictions_template"
description: "Shared report template for the /task Fidelity Gate's source-to-source-only contradiction check: one rf-qa agent reads ALL source documents (never the output) and checks for contradictions between them."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.7"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/skills/task/SKILL.md:390 (Fidelity Gate Step 3)"
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
template_name: "QA Cross-Source Contradictions"
template_version: "1.0.0"
sections: 6
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-cross-source-contradictions-report"
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
This is the /task Fidelity Gate Step 3 report. ONE rf-qa agent reads ALL source
documents (e.g. the PRD and the TDD it drove) and checks for contradictions
between them (example: PRD says 8 error codes, TDD says 12). This agent does
NOT read the assembled output at all -- source-to-source consistency only.

SCOPE:
This template covers ONLY the source-to-source contradiction check. It does
NOT cover source-vs-output fidelity (that is qa-source-fidelity_template.md).

THE SECTIONS (fixed order, exactly 6, firm per GAP-5; the header/frontmatter
block, Topic, Date, Phase, Fix cycle, precedes the numbered sections and is
excluded from the count, consistent with every sibling template's PART1
convention):
1. Source Documents Compared -- proves every source was read AND the output was NOT
2. Overall Verdict -- PASS (no contradictions) or FAIL (at least one)
3. Contradictions Found -- the two-sided claim table
4. Consistency Checks Performed (No Contradiction) -- makes a PASS evidence-bearing
5. Summary -- counts
6. QA Complete

REPORT-ONLY, NO FIX SECTION:
This template MUST NOT include an `## Actions Taken` section. Fixes for any
contradiction found here happen in a separate Fidelity Step 5 fix agent, not
in this report. Adding an Actions Taken section is a protocol violation.

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row in each table

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Verdict is EXACTLY one of: PASS | FAIL
- Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR
################################################################################ -->

## PART 2: THE QA CROSS-SOURCE CONTRADICTIONS SCAFFOLD (copy everything below this line)

# QA Cross-Source Contradictions - {{RF_PLACEHOLDER:PHASE}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** cross-source-contradiction
- **Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}} / 3

## Source Documents Compared

| Source Doc | Line Count |
|------------|------------|
| {{RF_PLACEHOLDER:SOURCE_PATH}} | {{RF_PLACEHOLDER:SOURCE_LINE_COUNT}} |
{{RF_PLACEHOLDER:SOURCE_DOCUMENTS_ROW}}

<!-- Every source document read goes here. The assembled output is NEVER listed here and NEVER read by this gate. -->

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

<!-- Verdict enum: PASS (no contradictions) | FAIL (at least one contradiction) -->

## Contradictions Found

| # | Claim (Source A) | Source A location | Conflicting Claim (Source B) | Source B location | Severity | Notes |
|---|---------------------|----------------------|---------------------------------|----------------------|----------|-------|
| {{RF_PLACEHOLDER:CONTRADICTION_NUM}} | {{RF_PLACEHOLDER:CLAIM_A}} | {{RF_PLACEHOLDER:LOCATION_A}} | {{RF_PLACEHOLDER:CLAIM_B}} | {{RF_PLACEHOLDER:LOCATION_B}} | {{RF_PLACEHOLDER:CONTRADICTION_SEVERITY}} | {{RF_PLACEHOLDER:CONTRADICTION_NOTES}} |
{{RF_PLACEHOLDER:CONTRADICTIONS_FOUND_ROW}}

<!-- Example shape: PRD says 8 error codes, TDD says 12. Severity enum: CRITICAL | IMPORTANT | MINOR -->

## Consistency Checks Performed (No Contradiction)

| # | Claim Checked | Sources Compared | Result |
|---|------------------|----------------------|--------|
| {{RF_PLACEHOLDER:CHECK_NUM}} | {{RF_PLACEHOLDER:CHECK_CLAIM}} | {{RF_PLACEHOLDER:CHECK_SOURCES}} | Consistent |
{{RF_PLACEHOLDER:CONSISTENCY_CHECKS_ROW}}

<!-- Makes a PASS verdict evidence-bearing rather than silent absence of findings. -->

## Summary

- **Sources compared:** {{RF_PLACEHOLDER:SOURCES_COMPARED_COUNT}}
- **Pairwise checks:** {{RF_PLACEHOLDER:PAIRWISE_CHECKS_COUNT}}
- **Contradictions found:** {{RF_PLACEHOLDER:CONTRADICTIONS_TOTAL}} (CRITICAL: {{RF_PLACEHOLDER:CONTRADICTIONS_CRITICAL_COUNT}}, IMPORTANT: {{RF_PLACEHOLDER:CONTRADICTIONS_IMPORTANT_COUNT}}, MINOR: {{RF_PLACEHOLDER:CONTRADICTIONS_MINOR_COUNT}})

## QA Complete

VERDICT: {{RF_PLACEHOLDER:FINAL_VERDICT}}
