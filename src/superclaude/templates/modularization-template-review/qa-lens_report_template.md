---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-lens"
title: "qa-lens_report_template"
description: "FILLED template for QA lens reports produced across /task phase-gate, post-completion, and fidelity-gate stages. Scaffolds the standard QA report shape shared by rf-qa (structural lenses) and rf-qa-qualitative (content lenses): verdict, items reviewed, summary, issues found, actions taken, recommendations, mandatory confidence gate. Carries no computation, only layout."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.1"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: "SPEC-1-templated-reports-canonical-rule-20260701.md s2 L28-34 (Group 1 row 1)"
related_docs:
- path: ".claude/skills/task/SKILL.md"
  description: "Standard QA Report Output Format block (L457-497), the canonical shape this template matches"
- path: ".claude/agents/rf-qa.md"
  description: "QA Report output format (409-448) and Confidence Gate Protocol (471-521), source of the mandatory confidence-gate section"
related_prd: ""
related_tdd: ""
tags:
- "templated-reports"
- "qa-report"
- "template"
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
# --- Template-side fields ---
template_name: "QA Lens Report"
template_version: "1.0.0"
sections: 9
placeholder_prefix: "RF_PLACEHOLDER"
# --- Modularization fields (template-side) ---
spec_id: "SPEC-qa-lens-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
# ^ net-new; promote to SHARED once a 2nd consumer confirms.
consumers:
- "task"   # status: confirmed
- "task-builder"   # status: confirmed
- "rf-qa"   # status: confirmed
- "rf-qa-qualitative"   # status: confirmed
---

<!--
################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS                                      ##
##  (for whoever FILLS this scaffold; never copied into the output report.)    ##
################################################################################

WHAT THIS IS. A FILLED template. Any lens agent (rf-qa structural, rf-qa-qualitative
content, or a domain-specific lens agent) copies PART 2 and replaces every
{{RF_PLACEHOLDER:*}} slot with a concrete value. The output is one QA report per
lens per gate invocation.

SCOPE. This file defines the report LAYOUT shared by every QA lens at every gate
(/task phase-gate Steps 3/4/5/8, Post-Completion Steps 1/2, Fidelity Gate agents
that are lens-shaped). It does not define which checks a given lens runs, nor any
computation; the filler supplies already-computed verdicts, counts, and evidence.
Consolidated-findings, fix-summary, and source-fidelity reports are DISTINCT
templates (qa-consolidated-findings, qa-fix-summary, qa-source-fidelity) and are
NOT scaffolded here.

THE SECTIONS (fixed order).
  1. Overall Verdict - PASS or FAIL for this lens.
  2. Items Reviewed - one row per check this lens ran, with evidence.
  3. Summary - pass/fail counts and critical-issue count.
  4. Issues Found - one row per finding, with severity and required fix.
  5. Actions Taken - fixes applied in-place, ONLY when fix_authorization is true;
     otherwise this section states no fixes were authorized this round.
  6. Recommendations - actions needed before the next phase/step can proceed.
  7. Self-Audit (content lenses) - conditionally required when Lens is a content
     lens (rf-qa-qualitative): (a) Reliance list of rf-qa PASS items skipped for
     structural re-check, plus (b) Independent semantic checks (at least 1
     required, INV-019). May be omitted for purely structural (rf-qa) lens
     invocations.
  8. Confidence Gate - the MANDATORY computed-confidence block (never self-assessed;
     omitting this section breaks the gate per SPEC-1 flag 2).
  9. QA Complete - closing marker plus the final VERDICT line a downstream
     consolidation step greps for.

PLACEHOLDER DISCIPLINE. Every {{RF_PLACEHOLDER:*}} is a fill slot. Repeating rows
(one per check, one per issue) are shown once with an {{RF_PLACEHOLDER:*_ROW}}
marker; the filler repeats the row as needed.

WRITING DISCIPLINE. No em dashes (U+2014), no en dashes (U+2013). Tables over
prose. Mark anything not yet computable as a slot, never as a fabricated number.
Confidence and coverage figures are COMPUTED per the Confidence Gate Protocol
(rf-qa.md:471-521), never self-assessed.
################################################################################
-->

---

## PART 2: THE QA LENS REPORT SCAFFOLD (copy everything below this line)

# QA Report - {{RF_PLACEHOLDER:PHASE}} - {{RF_PLACEHOLDER:LENS}}

**Topic:** {{RF_PLACEHOLDER:TOPIC}}
**Date:** {{RF_PLACEHOLDER:DATE}}
**Phase:** {{RF_PLACEHOLDER:PHASE}}
**Lens:** {{RF_PLACEHOLDER:LENS}}
**Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}}
**fix_authorization:** {{RF_PLACEHOLDER:FIX_AUTHORIZATION}}

---

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| {{RF_PLACEHOLDER:ITEM_NUM}} | {{RF_PLACEHOLDER:ITEM_CHECK}} | {{RF_PLACEHOLDER:ITEM_RESULT}} | {{RF_PLACEHOLDER:ITEM_EVIDENCE}} |

<!-- One row per check this lens ran; repeat the row above as needed. -->
{{RF_PLACEHOLDER:ITEMS_REVIEWED_ROW}}

---

## Summary

- Checks passed: {{RF_PLACEHOLDER:CHECKS_PASSED}}/{{RF_PLACEHOLDER:CHECKS_TOTAL}}
- Checks failed: {{RF_PLACEHOLDER:CHECKS_FAILED}}
- Critical issues: {{RF_PLACEHOLDER:CRITICAL_ISSUES_COUNT}}
- Issues fixed in-place: {{RF_PLACEHOLDER:ISSUES_FIXED_COUNT}} (if fix-authorized; otherwise `N/A`)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:ISSUE_SEVERITY}} | {{RF_PLACEHOLDER:ISSUE_LOCATION}} | {{RF_PLACEHOLDER:ISSUE_DESCRIPTION}} | {{RF_PLACEHOLDER:ISSUE_REQUIRED_FIX}} |

<!-- One row per finding; Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR. Repeat the row above as needed. -->
{{RF_PLACEHOLDER:ISSUES_FOUND_ROW}}

---

## Actions Taken

{{RF_PLACEHOLDER:ACTIONS_TAKEN_BODY}}

<!-- If fix_authorization is true, list every fix applied (file:change). If fix_authorization is false, state explicitly: "No fixes authorized this round; findings reported only." -->

---

## Recommendations

{{RF_PLACEHOLDER:RECOMMENDATIONS_BODY}}

<!-- Actions needed before the next phase/step can proceed. -->

---

## Self-Audit

<!-- Conditionally required: mandatory when Lens is a content lens (rf-qa-qualitative,
     per the "(content lenses)" qualifier); may be omitted for purely structural
     (rf-qa) lens invocations. Alternative heading (equally schema-conformant,
     TEST-009): "## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)" -->

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- {{RF_PLACEHOLDER:RELIANCE_ITEM}}
{{RF_PLACEHOLDER:RELIANCE_ITEM_ROW}}

**(b) Independent semantic checks (at least 1 required, INV-019):**
- {{RF_PLACEHOLDER:SEMANTIC_CHECK}} - verified by {{RF_PLACEHOLDER:SEMANTIC_CHECK_EVIDENCE}}
{{RF_PLACEHOLDER:SEMANTIC_CHECK_ROW}}

---

## Confidence Gate

<!-- MANDATORY section (rf-qa.md:471-521 Confidence Gate Protocol, Step 5 report fields, rf-qa.md:500-509).
     Confidence is COMPUTED as VERIFIED / (TOTAL - UNVERIFIABLE) * 100, NEVER self-assessed.
     Omitting this section breaks the gate (SPEC-1 flag 2). -->

- **Confidence:** "Verified: {{RF_PLACEHOLDER:CONF_VERIFIED}}/{{RF_PLACEHOLDER:CONF_TOTAL}} | Unverifiable: {{RF_PLACEHOLDER:CONF_UNVERIFIABLE}} | Unchecked: {{RF_PLACEHOLDER:CONF_UNCHECKED}} | Confidence: {{RF_PLACEHOLDER:CONF_PERCENT}}%"
- **Tool engagement:** "Read: {{RF_PLACEHOLDER:TOOL_READ_COUNT}} | Grep: {{RF_PLACEHOLDER:TOOL_GREP_COUNT}} | Glob: {{RF_PLACEHOLDER:TOOL_GLOB_COUNT}} | Bash: {{RF_PLACEHOLDER:TOOL_BASH_COUNT}}"
  <!-- If web research was performed, this line MUST also report tavily_search / tavily_extract / web_search_fallback / web_fetch_fallback counts with a one-line reason for any non-zero fallback count. -->

**Unchecked items (with reason):**
- {{RF_PLACEHOLDER:UNCHECKED_ITEM}} (reason: {{RF_PLACEHOLDER:UNCHECKED_ITEM_REASON}})
{{RF_PLACEHOLDER:UNCHECKED_ITEM_ROW}}

**Unverifiable items (with blocker):**
- {{RF_PLACEHOLDER:UNVERIFIABLE_ITEM}} (blocker: {{RF_PLACEHOLDER:UNVERIFIABLE_ITEM_BLOCKER}})
{{RF_PLACEHOLDER:UNVERIFIABLE_ITEM_ROW}}

---

## QA Complete

VERDICT: {{RF_PLACEHOLDER:FINAL_VERDICT}}
