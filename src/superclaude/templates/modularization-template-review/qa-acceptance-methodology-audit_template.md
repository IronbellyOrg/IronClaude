---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-acceptance-methodology-audit"
title: "qa-acceptance-methodology-audit_template"
description: "Report template for the FR-PFL.7 acceptance-methodology audit: the hostile, non-authoring re-derivation of every claim-to-evidence matrix row. Retains the qa-lens donor's mandatory Confidence Gate block VERBATIM (the anti-sampling arithmetic) and adds the four audit-contract addendum sections: independence evidence with matrix-hash bracketing, the re-derivation ledger with method column and four-value directional result enum, the three exhaustiveness arithmetic checks, and the disagreement disposition rule."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-08-09"
updated_date: "2026-08-09"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-acceptance-proof-20260805-154602 Step 6.8"
autogen: true
autogen_method: "/task executor, acceptance-proof Phase 6"
autogen_source:
  - ".claude/templates/modularization-template-review/qa-lens_report_template.md"
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-acceptance-proof-20260805-154602"
depends_on: []
spec_path: ".dev/research/persona-agent-deep-runs/SPEC-PERSONA-BRAIN-FINISH-LINE-20260729.md:411-418 (FR-PFL.7 audit criteria), :1688"
related_docs:
  - ".claude/templates/modularization-template-review/claim-evidence-matrix_template.md"
  - ".claude/skills/persona-agent/templates/claim-evidence-matrix.schema.md"
related_prd: ""
related_tdd: ""
tags:
  - acceptance-proof
  - methodology-audit
  - qa-report
  - template
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-fable-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "QA Acceptance Methodology Audit"
template_version: "1.0.0"
sections: 8
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-acceptance-methodology-audit-report"
family: "acceptance-proof"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "acceptance-methodology auditor agent" # status: confirmed
---

<!--
################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS                                      ##
##  (for whoever FILLS this scaffold; never copied into the output report.)    ##
################################################################################

WHAT THIS IS. The report the acceptance-methodology auditor fills after
hostilely re-deriving every row of a claim-to-evidence matrix. The auditor
assumes the gate is hollow and tries to prove a false pass; it did NOT author
the matrix; it re-derives every observed class directly from the underlying
artifact rather than accepting the matrix's own label.

DONOR. Derived from qa-lens_report_template.md. The Confidence Gate section is
retained VERBATIM from the donor (it is the anti-sampling arithmetic: computed
confidence plus mandatory enumeration of every unchecked item with a reason
and every unverifiable item with a blocker). Do not paraphrase that block.

THE SECTIONS (fixed order).
  1. Overall Verdict
  2. Independence Evidence - the three separations, evidenced on disk, plus
     MATRIX-HASH BRACKETING: the matrix file's sha256 recorded at audit START
     and again at audit END. Any change between the two INVALIDATES the audit,
     because the artifact under review moved while being reviewed.
  3. Re-derivation Ledger - one row per criterion, six columns INCLUDING the
     re-derivation method column (a specific executable action, never "read
     the report") and the FOUR-VALUE result enum:
     AGREE | DISAGREE-HIGHER | DISAGREE-LOWER | UNVERIFIABLE.
     The direction of a disagreement is preserved because DISAGREE-LOWER (the
     artifact supports a LOWER class than the matrix claimed) is the
     hollow-pass signature and must be separately countable from the
     conservative DISAGREE-HIGHER, even though both block.
  4. Exhaustiveness Arithmetic - the three checks (A: denominator fixed FROM
     THE SPECIFICATION before the matrix is opened; B: criterion total =
     re-derived + unverifiable + absent, with the last two individually
     listed; C: capability-side set-difference membership).
  5. Disagreement Disposition - the rule applied to every DISAGREE row.
  6. Issues Found
  7. Confidence Gate - VERBATIM donor block, MANDATORY, never self-assessed.
  8. QA Complete - final greppable VERDICT line.

THE EVIDENCE-CLASS ORDERING, stated literally because every comparison in this
report depends on it:

    DECLARED < INSPECTED < TESTED < DEMONSTRATED

A HIGHER class discharges a LOWER requirement; a lower observation NEVER
discharges a higher requirement. DECLARED is never a required class (spec line
1557), so it appears only as an observed class.

WRITING DISCIPLINE. No em dashes (U+2014), no en dashes (U+2013). Tables over
prose. Both disagreement directions force the row undischarged; a disagreement
is NEVER averaged, NEVER resolved in the matrix author's favor, and NEVER
silently settled toward the lower class as a substitute for adjudication.
################################################################################
-->

---

## PART 2: THE ACCEPTANCE METHODOLOGY AUDIT SCAFFOLD (copy everything below this line)

# Acceptance Methodology Audit - {{RF_PLACEHOLDER:SUBJECT}}

**Matrix instance:** {{RF_PLACEHOLDER:MATRIX_PATH}}
**Date:** {{RF_PLACEHOLDER:DATE}}
**Auditor identity (agent instance):** {{RF_PLACEHOLDER:AUDITOR_IDENTITY}}
**Matrix author (must differ from auditor):** {{RF_PLACEHOLDER:MATRIX_AUTHOR}}

---

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

---

## Independence Evidence

| Separation | Requirement | Evidence on disk |
|---|---|---|
| S1 separate instance | The auditor received only the matrix path and artifact roots, never the authoring agent's reasoning | {{RF_PLACEHOLDER:S1_EVIDENCE}} |
| S2 tool scope | Read, Grep, Glob only on the matrix path; no Write, Edit, or shell on it; any genuinely required shell step named explicitly | {{RF_PLACEHOLDER:S2_EVIDENCE}} |
| S3 model family (recommended) | Different model family from the matrix author | {{RF_PLACEHOLDER:S3_EVIDENCE}} |

**Matrix-hash bracketing (audit-invalidating on mismatch):**

- Matrix sha256 at audit START: {{RF_PLACEHOLDER:MATRIX_SHA_START}}
- Matrix sha256 at audit END: {{RF_PLACEHOLDER:MATRIX_SHA_END}}
- Match: {{RF_PLACEHOLDER:MATRIX_SHA_MATCH}} <!-- YES | NO; NO invalidates this audit outright: the artifact under review moved while being reviewed -->

---

## Re-derivation Ledger

<!-- One row per criterion. Method must name a specific executable action
     ("Bash reducer replay", "recomputed sha256", "in-process gate call"),
     never "read the report". Result is EXACTLY one of:
     AGREE | DISAGREE-HIGHER | DISAGREE-LOWER | UNVERIFIABLE. -->

| Criterion ID | Matrix observed class | Re-derived class | Re-derivation method | Artifact re-derived from | Review order | Result |
|--------------|----------------------|------------------|----------------------|--------------------------|--------------|--------|
| {{RF_PLACEHOLDER:LEDGER_CRITERION_ID}} | {{RF_PLACEHOLDER:LEDGER_MATRIX_CLASS}} | {{RF_PLACEHOLDER:LEDGER_REDERIVED_CLASS}} | {{RF_PLACEHOLDER:LEDGER_METHOD}} | {{RF_PLACEHOLDER:LEDGER_ARTIFACT}} | {{RF_PLACEHOLDER:LEDGER_ORDER}} | {{RF_PLACEHOLDER:LEDGER_RESULT}} |
{{RF_PLACEHOLDER:LEDGER_ROW}}

**Directional disagreement counts (kept separate; DISAGREE-LOWER is the hollow-pass signature):**

- AGREE: {{RF_PLACEHOLDER:COUNT_AGREE}}
- DISAGREE-HIGHER (conservative matrix): {{RF_PLACEHOLDER:COUNT_DISAGREE_HIGHER}}
- DISAGREE-LOWER (hollow-pass signature): {{RF_PLACEHOLDER:COUNT_DISAGREE_LOWER}}
- UNVERIFIABLE: {{RF_PLACEHOLDER:COUNT_UNVERIFIABLE}}

---

## Exhaustiveness Arithmetic

**Check A (denominator fixed from the specification, BEFORE the matrix was opened; deriving it from the matrix is circular and makes an omission invisible):**

- Spec-parsed criterion denominator: {{RF_PLACEHOLDER:CHECKA_SPEC_DENOMINATOR}}
- Fixed at (timestamp/step): {{RF_PLACEHOLDER:CHECKA_FIXED_AT}}

**Check B (count reconciliation; every unverifiable and absent member individually listed):**

- Criterion total {{RF_PLACEHOLDER:CHECKB_TOTAL}} = re-derived {{RF_PLACEHOLDER:CHECKB_REDERIVED}} + unverifiable {{RF_PLACEHOLDER:CHECKB_UNVERIFIABLE}} + absent {{RF_PLACEHOLDER:CHECKB_ABSENT}}
- Reconciles: {{RF_PLACEHOLDER:CHECKB_RECONCILES}} <!-- YES | NO -->
- Unverifiable rows (each with its blocker): {{RF_PLACEHOLDER:CHECKB_UNVERIFIABLE_LIST}}
- Absent rows (each individually named): {{RF_PLACEHOLDER:CHECKB_ABSENT_LIST}}

**Check C (capability-side set-difference membership):**

- Ledger capabilities: {{RF_PLACEHOLDER:CHECKC_LEDGER_COUNT}} | Matrix capability rows: {{RF_PLACEHOLDER:CHECKC_MATRIX_COUNT}} | Set difference: {{RF_PLACEHOLDER:CHECKC_SET_DIFF}}
- Reconciles: {{RF_PLACEHOLDER:CHECKC_RECONCILES}} <!-- YES | NO; any missing capability row is a discharge failure -->

<!-- Partitioning across auditors by disjoint criterion range is a SCALING
     mechanism; sampling is a COVERAGE REDUCTION. The two are never conflated:
     an omitted criterion is a hard block regardless of class. -->

**Ordering verification (higher-class-first, computed mechanically):**

- Max review order among DEMONSTRATED/TESTED rows: {{RF_PLACEHOLDER:ORDER_MAX_HIGH}}
- Min review order among INSPECTED/DECLARED rows: {{RF_PLACEHOLDER:ORDER_MIN_LOW}}
- Ordering held: {{RF_PLACEHOLDER:ORDER_HELD}} <!-- YES | NO; NO is a recorded PROCESS DEFECT and never excuses an omission -->

---

## Disagreement Disposition

<!-- The rule: any row where matrix_observed_class != rederived_observed_class
     forces discharged: false for that row, unconditionally, pending human or
     spec-level adjudication. BOTH disagreement directions force the row
     undischarged. Three resolutions are FORBIDDEN: never averaged; never
     resolved in the matrix author's favor; never silently settled toward the
     lower class as a substitute for adjudication. -->

| Criterion ID | Direction | Forced undischarged? | Adjudication status |
|--------------|-----------|----------------------|---------------------|
| {{RF_PLACEHOLDER:DISP_CRITERION_ID}} | {{RF_PLACEHOLDER:DISP_DIRECTION}} | {{RF_PLACEHOLDER:DISP_FORCED}} | {{RF_PLACEHOLDER:DISP_ADJUDICATION}} |
{{RF_PLACEHOLDER:DISPOSITION_ROW}}

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:ISSUE_SEVERITY}} | {{RF_PLACEHOLDER:ISSUE_LOCATION}} | {{RF_PLACEHOLDER:ISSUE_DESCRIPTION}} | {{RF_PLACEHOLDER:ISSUE_REQUIRED_FIX}} |

<!-- One row per finding; Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR. Repeat the row above as needed. -->
{{RF_PLACEHOLDER:ISSUES_FOUND_ROW}}

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

