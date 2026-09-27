---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-analyst-synthesis-review"
title: "analyst-synthesis-review_report_template"
description: "Shared report template for the rf-analyst Synthesis Quality Review analysis type: verifies synthesis files against source research files, per-file and in aggregate."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.21"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/agents/rf-analyst.md:271-306 (Synthesis Quality Review output format), 249-269 (10-item checklist and process)"
related_docs:
  - ".claude/agents/rf-analyst.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - qa-report
  - template
  - synthesis-gate
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Analyst Synthesis Review"
template_version: "1.0.0"
sections: 4
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-analyst-synthesis-review-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task-builder" # status: confirmed
  - "rf-analyst" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the rf-analyst Synthesis Quality Review report, produced at the
Phase 5 synthesis gate (per /task Phase-Gate QA and /task-builder's
synthesis-gate agent mix) to verify every synthesis file faithfully
represents its underlying research files, with no fabrication and no
dropped findings.

SCOPE:
Fully specified at rf-analyst.md:271-306. Fixed 4-section order, no
Confidence Gate (rf-analyst carries no Confidence Gate Protocol machinery,
same as qa-task-research-alignment_report_template.md). This is a
read-only report-only lens: rf-analyst.md:341-348 states "Fix nothing
yourself -- read-only on research/synthesis files."

THE SECTIONS (fixed order, all 4 required):
1. Overall Verdict -- PASS or FAIL, with issue count
2. Per-File Review -- one block per synthesis file reviewed: Sections covered, Verdict, and a per-file check table
3. Issues Requiring Fixes -- one row per finding, present even on PASS (empty body)
4. Summary -- files passed/failed, total issues, critical issues

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row
- The Per-File Review block itself repeats once per synthesis file reviewed;
  its own repeat marker is `{{RF_PLACEHOLDER:PER_FILE_BLOCK}}`, placed
  directly beneath one filled example block

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Verdict is EXACTLY one of: PASS | FAIL
- Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR
################################################################################ -->

## PART 2: THE ANALYST SYNTHESIS REVIEW SCAFFOLD (copy everything below this line)

# Analyst Synthesis Review

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

<!-- PASS or FAIL, with issue count, e.g. "PASS (0 issues)" or "FAIL (3 issues, 1 CRITICAL)" -->

## Per-File Review

<!-- one block per synthesis file reviewed against its source research files -->

### {{RF_PLACEHOLDER:SYNTHESIS_FILE}}

**Sections covered:** {{RF_PLACEHOLDER:SECTIONS_COVERED}}

**Verdict:** {{RF_PLACEHOLDER:FILE_VERDICT}}

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|-----------------|
| {{RF_PLACEHOLDER:CHECK_NUM}} | {{RF_PLACEHOLDER:CHECK}} | {{RF_PLACEHOLDER:RESULT}} | {{RF_PLACEHOLDER:EVIDENCE_OR_ISSUE}} |
{{RF_PLACEHOLDER:PER_FILE_BLOCK}}

## Issues Requiring Fixes

<!-- canonical issue shape: synthesis claim not traceable to any research file, research finding dropped from synthesis, synthesis fact contradicting its cited source, source attribution missing or incorrect -->

| # | File | Check | Issue | Required Fix |
|---|------|-------|-------|---------------|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:FILE}} | {{RF_PLACEHOLDER:CHECK}} | {{RF_PLACEHOLDER:ISSUE}} | {{RF_PLACEHOLDER:REQUIRED_FIX}} |
{{RF_PLACEHOLDER:ISSUE_ROW}}

## Summary

- **Files passed / failed:** {{RF_PLACEHOLDER:FILES_PASSED}} / {{RF_PLACEHOLDER:FILES_FAILED}}
- **Total issues:** {{RF_PLACEHOLDER:TOTAL_ISSUES}}
- **Critical issues:** {{RF_PLACEHOLDER:CRITICAL_COUNT}}
