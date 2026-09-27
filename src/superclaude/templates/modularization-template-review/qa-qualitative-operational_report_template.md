---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-qualitative-operational"
title: "qa-qualitative-operational_report_template"
description: "Shared report template for the /task-builder A.10.5 rf-qa-qualitative operational-correctness lens: the full task-qualitative unified format including the AX-1..AX-5 axis column, the Self-Audit INV-019 subsection, and the mandatory Confidence Gate."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.19"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on:
  - "qa-lens_report_template.md"
spec_path: ".claude/agents/rf-qa-qualitative.md:819-891 (Output Format), 660-739 (15-item checklist), 580-658 (AX-1..AX-5 axes), 1001-1129 (Self-Audit INV-019), 914-967 (Confidence Gate Protocol)"
related_docs:
  - ".claude/templates/reports/qa-lens_report_template.md"
  - ".claude/agents/rf-qa-qualitative.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - qa-report
  - template
  - task-integrity
  - task-qualitative
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "QA Qualitative Operational"
template_version: "1.0.0"
sections: 9
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-qualitative-operational-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task-builder" # status: confirmed
  - "task" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the FULL task-qualitative unified output format used by
rf-qa-qualitative for the task-qualitative phase (the 15-item Operational
Simulation / Code Compatibility / Test-Verification / Failure-Mode
checklist at rf-qa-qualitative.md:660-739), consumed by /task-builder
A.10.5 Agent 1 (operational-correctness lens) and reusable at /task
task-integrity gates. Unlike the qa-research-* and qa-task-validation-*
templates (non-task-qualitative, report-only, 6-section abbreviated
shape), this is a task-qualitative phase and carries the FULL format:
axis column, Self-Audit INV-019, Actions Taken, Recommendations.

SCOPE:
This extends the base qa-lens_report_template.md 8-section shape with
exactly ONE new section (Self-Audit / Inherited Structural Verdict,
INV-019) plus two in-place modifications to existing sections: the
Items Reviewed table gains a required `axis` column, and the Summary
section gains a mandatory `Axis lens status` bullet. All three additions
are mandatory per rf-qa-qualitative.md:819-891 and 1001-1129 -- omitting
any one of them breaks the gate.

THE SECTIONS (fixed order, all 9 required):
1. Overall Verdict -- PASS or FAIL for this lens
2. Items Reviewed -- one row per of the 15 task-qualitative checks, WITH the axis column
3. Summary -- pass/fail counts, critical issues, PLUS the Axis lens status bullet
4. Issues Found -- one row per finding, severity and required fix
5. Actions Taken -- fixes applied in-place, only if fix_authorization is true
6. Self-Audit -- (a) Reliance list + (b) Independent semantic checks (>=1 required, INV-019); heading may alternatively read "Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)"
7. Recommendations -- actions needed before the next phase/step can proceed
8. Confidence Gate -- the MANDATORY computed-confidence block (never self-assessed)
9. QA Complete -- closing marker plus the final VERDICT line

AXIS COLUMN VOCABULARY (closed set, PR-07 canonical annotation rules):
`AX-1` (drift) | `AX-2` (contradictions) | `AX-3` (omissions) |
`AX-4` (weakened-criteria) | `AX-5` (invented-content) | `none`.
`none` = the axis lens was applied and nothing fired (used on PASS rows).
One of AX-1..AX-5 = that axis fired (used on FAIL rows). N/A is FORBIDDEN
in this column. `drift-axis-inactive` is a Summary-block annotation only
(emitted when the AX-1 drift baseline, the BUILD_REQUEST.GOAL verbatim
capture, is absent) -- it is NEVER a value in the axis column itself.

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Verdict is EXACTLY one of: PASS | FAIL
- Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR
- Self-Audit category (b) MUST have at least 1 entry (INV-019); zero entries
  is a violation regardless of category (a) contents
- Confidence and coverage figures are COMPUTED per the Confidence Gate
  Protocol (rf-qa-qualitative.md:914-967), never self-assessed
################################################################################ -->

## PART 2: THE QA QUALITATIVE OPERATIONAL SCAFFOLD (copy everything below this line)

# QA Report - {{RF_PLACEHOLDER:PHASE}} - {{RF_PLACEHOLDER:LENS}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** {{RF_PLACEHOLDER:PHASE}}
- **Lens:** operational-correctness
- **Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}}
- **fix_authorization:** {{RF_PLACEHOLDER:FIX_AUTHORIZATION}}

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

## Items Reviewed

<!-- one row per of the 15 task-qualitative checks (Operational Simulation 1-3,
     Code Compatibility 4-6, Test/Verification Quality 7-8, Failure Mode
     Analysis 9-15); axis is REQUIRED on every row: none on PASS, one of
     AX-1..AX-5 on FAIL, N/A forbidden -->

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| {{RF_PLACEHOLDER:ITEM_NUM}} | {{RF_PLACEHOLDER:ITEM_CHECK}} | {{RF_PLACEHOLDER:ITEM_AXIS}} | {{RF_PLACEHOLDER:ITEM_RESULT}} | {{RF_PLACEHOLDER:ITEM_EVIDENCE}} |
{{RF_PLACEHOLDER:ITEMS_REVIEWED_ROW}}

## Summary

- Checks passed: {{RF_PLACEHOLDER:CHECKS_PASSED}}/{{RF_PLACEHOLDER:CHECKS_TOTAL}}
- Checks failed: {{RF_PLACEHOLDER:CHECKS_FAILED}}
- Critical issues: {{RF_PLACEHOLDER:CRITICAL_ISSUES_COUNT}}
- Issues fixed in-place: {{RF_PLACEHOLDER:ISSUES_FIXED_COUNT}} (if fix-authorized, otherwise N/A)
- Axis lens status: {{RF_PLACEHOLDER:AXIS_LENS_STATUS}} <!-- emit literal "drift-axis-inactive" when the AX-1 drift baseline is absent -->

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|---------------|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:ISSUE_SEVERITY}} | {{RF_PLACEHOLDER:ISSUE_LOCATION}} | {{RF_PLACEHOLDER:ISSUE_DESCRIPTION}} | {{RF_PLACEHOLDER:ISSUE_REQUIRED_FIX}} |
{{RF_PLACEHOLDER:ISSUES_FOUND_ROW}}

## Actions Taken

{{RF_PLACEHOLDER:ACTIONS_TAKEN_BODY}}
<!-- If fix_authorization is true, list every fix applied (file:change). If false, state explicitly: "No fixes authorized this round; findings reported only." -->

## Self-Audit

<!-- Alternative heading (equally schema-conformant, TEST-009): "## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)" -->

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- {{RF_PLACEHOLDER:RELIANCE_ITEM}}
{{RF_PLACEHOLDER:RELIANCE_ITEM_ROW}}

**(b) Independent semantic checks (at least 1 required, INV-019):**
- {{RF_PLACEHOLDER:SEMANTIC_CHECK}} - verified by {{RF_PLACEHOLDER:SEMANTIC_CHECK_EVIDENCE}}
{{RF_PLACEHOLDER:SEMANTIC_CHECK_ROW}}

## Recommendations

{{RF_PLACEHOLDER:RECOMMENDATIONS_BODY}}
<!-- Actions needed before the next phase/step can proceed. -->

## Confidence Gate

<!-- MANDATORY section (rf-qa-qualitative.md:914-967 Confidence Gate Protocol, same COMPUTED
     confidence machinery as rf-qa). Confidence is COMPUTED as VERIFIED / (TOTAL - UNVERIFIABLE) * 100,
     NEVER self-assessed. Omitting this section breaks the gate. -->

- **Confidence:** "Verified: {{RF_PLACEHOLDER:CONF_VERIFIED}}/{{RF_PLACEHOLDER:CONF_TOTAL}} | Unverifiable: {{RF_PLACEHOLDER:CONF_UNVERIFIABLE}} | Unchecked: {{RF_PLACEHOLDER:CONF_UNCHECKED}} | Confidence: {{RF_PLACEHOLDER:CONF_PERCENT}}%"
- **Tool engagement:** "Read: {{RF_PLACEHOLDER:TOOL_READ_COUNT}} | Grep: {{RF_PLACEHOLDER:TOOL_GREP_COUNT}} | Glob: {{RF_PLACEHOLDER:TOOL_GLOB_COUNT}} | Bash: {{RF_PLACEHOLDER:TOOL_BASH_COUNT}}"

**Unchecked items (with reason):**
- {{RF_PLACEHOLDER:UNCHECKED_ITEM}} (reason: {{RF_PLACEHOLDER:UNCHECKED_ITEM_REASON}})
{{RF_PLACEHOLDER:UNCHECKED_ITEM_ROW}}

**Unverifiable items (with blocker):**
- {{RF_PLACEHOLDER:UNVERIFIABLE_ITEM}} (blocker: {{RF_PLACEHOLDER:UNVERIFIABLE_ITEM_BLOCKER}})
{{RF_PLACEHOLDER:UNVERIFIABLE_ITEM_ROW}}

## QA Complete

VERDICT: {{RF_PLACEHOLDER:FINAL_VERDICT}}
