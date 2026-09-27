---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-claim-evidence-matrix"
title: "claim-evidence-matrix_template"
description: "Report template for the FR-PFL.7 claim-to-evidence matrix: TWO key-space blocks (criterion-keyed and capability-keyed), each with its own fixed ten-column table, its own N/total summary line, and the quarantine forcing rule (any undischarged row forces QUARANTINE)."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-08-09"
updated_date: "2026-08-09"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-acceptance-proof-20260805-154602 Step 6.7"
autogen: true
autogen_method: "/task executor, acceptance-proof Phase 6"
autogen_source:
  - ".claude/templates/modularization-template-review/analyst-coverage-matrix_template.md"
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-acceptance-proof-20260805-154602"
depends_on: []
spec_path: ".dev/research/persona-agent-deep-runs/SPEC-PERSONA-BRAIN-FINISH-LINE-20260729.md:883-889 (matrix row shape), :291, :411-414, :901"
related_docs:
  - ".claude/skills/persona-agent/templates/claim-evidence-matrix.schema.md"
  - ".claude/skills/persona-agent/templates/required-class-assignment.schema.md"
related_prd: ""
related_tdd: ""
tags:
  - acceptance-proof
  - claim-evidence-matrix
  - template
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-fable-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Claim-to-Evidence Matrix"
template_version: "1.0.0"
sections: 5
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-claim-evidence-matrix-report"
family: "acceptance-proof"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "run4-harness/harness.py matrix generator" # status: confirmed
  - "acceptance-methodology auditor" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
The report rendering of the FR-PFL.7 claim-to-evidence matrix. Derived from the
donor template analyst-coverage-matrix_template.md (read first, then adapted):
retained from the donor are (1) the FIXED column order, (2) the repeating-row
{{RF_PLACEHOLDER:*_ROW}} placeholder discipline, (3) the count-over-total
summary line, and (4) the forcing rule, here strengthened from the donor's
"any NO or PARTIAL forces FAIL" to "ANY undischarged row forces QUARANTINE".

TWO KEY SPACES (both blocks REQUIRED; a single-block instance is MALFORMED):
The criterion-keyed block covers every acceptance criterion (253-row
denominator from required-class-assignment.json). The capability-keyed block
covers every ledger capability (22-row denominator, set-diffed against
capability-ledger.json). Neither coverage obligation satisfies the other.
Each block has ITS OWN table and ITS OWN summary line.

COLUMN SCHEMA (FIXED order, both tables), TEN columns, with each column's source.
(Corrected 2026-08-10, finding PC-M04: this list previously omitted Control
artifact, so PART 1 named 9 columns while the PART 2 scaffold header carries 10.
The frontmatter description's "seven-column" wording was wrong on the same count
and now reads ten-column.) The columns
map ONE-TO-ONE onto the JSON field set in claim-evidence-matrix.schema.md
Section 2; there is no column without a field and no author-written field
without a column:
Row key | Claim | Required class | Observed class | Artifact | Observed fact | Provenance | Control shape | Control artifact | Discharged
- Row key (JSON `row_key`): the criterion_id from the assignment table, or the
  capability_id from the capability ledger. Unique within its block.
- Claim (JSON `claim`): generator-written. For a criterion row the claim CARRIES
  THE SPEC LINE, in the form "FR-PFL.2.C01 (spec line 289)". There is no separate
  Spec line column: the schema has no such field, and a column with no backing
  field is exactly how a template and its instances drift apart.
- Required class (JSON `required_class`): LOADER-INJECTED from the assignment
  table and NEVER author-written. Capability rows are always DEMONSTRATED.
- Observed class, Artifact, Observed fact: filled by the matrix author.
  Artifact MUST be a CONCRETE resolvable path, never a bracket placeholder such
  as <session>/... on a filled row. Observed fact MUST be verifiable at that
  artifact and must clear the substance floor (at least 20 characters, and not a
  placeholder token such as TODO or ".").
- Provenance (JSON `evidence_provenance`): EXACTLY `fire` or `fixture`,
  MANDATORY on every filled row. Fixture provenance can never establish
  DEMONSTRATED.
- Control shape (JSON `control_shape_source`): on a DEMONSTRATED-required filled
  row it MUST positively read `real-artifact`. Leaving it blank does NOT skip the
  check: silence is treated as design-assumed and blocks the row (spec line 311).
- Control artifact (JSON `control_shape_artifact`): MANDATORY once Control shape
  reads `real-artifact`. It NAMES the real artifact the control shape was
  re-derived from. It must be a concrete resolvable path (no bracket placeholder)
  and must be a DIFFERENT path from this row's own Artifact, because a row cannot
  be its own negative control. Leave it blank only on rows that are not
  DEMONSTRATED-required, where the Control shape column is itself blank.
- Discharged: LOADER-COMPUTED from the class comparison
  (DECLARED < INSPECTED < TESTED < DEMONSTRATED). NEVER author-written.
(The capability table uses Capability ID in place of Row key; its Claim column
carries the ledger capability claim rather than a spec line.)

PLACEHOLDER DISCIPLINE:
- Single-value slots: {{RF_PLACEHOLDER:NAME}}
- Repeating-row markers: {{RF_PLACEHOLDER:NAME_ROW}} on its own line directly
  beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Observed class is EXACTLY one of: DECLARED | INSPECTED | TESTED | DEMONSTRATED
- Required class is EXACTLY one of: INSPECTED | TESTED | DEMONSTRATED
  (DECLARED is never a required class; a row carrying it is schema-invalid)
- Discharged is EXACTLY one of: YES | NO
- FORCING RULE: any row with Discharged = NO forces the block verdict to
  QUARANTINE. There is no partial credit and no sampling.

OPEN QUESTION (recorded, NOT fixed here; out of this build request's scope):
The library INDEX.md at this directory lists every template's Storage column
as .claude/templates/reports/<file>, but that directory was removed 2026-07-04
and the files physically live in modularization-template-review/. This
template is therefore placed where the registered templates PHYSICALLY live,
and the INDEX Storage-column defect is left to its owning workstream.
################################################################################ -->

## PART 2: THE CLAIM-TO-EVIDENCE MATRIX SCAFFOLD (copy everything below this line)

# Claim-to-Evidence Matrix

- **Session / subject:** {{RF_PLACEHOLDER:SUBJECT}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Assignment table:** {{RF_PLACEHOLDER:ASSIGNMENT_PATH}} (spec sha256 {{RF_PLACEHOLDER:SPEC_SHA256}})
- **Matrix instance:** {{RF_PLACEHOLDER:MATRIX_JSON_PATH}}

## Criterion Block

<!-- column order is FIXED; Required class and Discharged are NOT author-writable:
     Required class is loader-injected from the assignment table and Discharged is
     loader-computed from the class comparison -->

| Row key | Claim | Required class | Observed class | Artifact | Observed fact | Provenance | Control shape | Control artifact | Discharged |
|---------|-------|----------------|----------------|----------|---------------|------------|---------------|------------------|------------|
| {{RF_PLACEHOLDER:CRITERION_ID}} | {{RF_PLACEHOLDER:CLAIM}} | {{RF_PLACEHOLDER:REQUIRED_CLASS}} | {{RF_PLACEHOLDER:OBSERVED_CLASS}} | {{RF_PLACEHOLDER:ARTIFACT}} | {{RF_PLACEHOLDER:OBSERVED_FACT}} | {{RF_PLACEHOLDER:EVIDENCE_PROVENANCE}} | {{RF_PLACEHOLDER:CONTROL_SHAPE_SOURCE}} | {{RF_PLACEHOLDER:CONTROL_SHAPE_ARTIFACT}} | {{RF_PLACEHOLDER:DISCHARGED}} |
{{RF_PLACEHOLDER:CRITERION_MATRIX_ROW}}

### Criterion Block Summary

{{RF_PLACEHOLDER:CRITERION_DISCHARGED_COUNT}}/{{RF_PLACEHOLDER:CRITERION_TOTAL}} criteria discharged

**Criterion block verdict:** {{RF_PLACEHOLDER:CRITERION_VERDICT}} <!-- any Discharged = NO row forces QUARANTINE -->

## Capability Block

<!-- column order is FIXED; same non-author-writable rules apply -->

| Capability ID | Claim | Required class | Observed class | Artifact | Observed fact | Provenance | Control shape | Control artifact | Discharged |
|---------------|-------|----------------|----------------|----------|---------------|------------|---------------|------------------|------------|
| {{RF_PLACEHOLDER:CAPABILITY_ID}} | {{RF_PLACEHOLDER:CAP_CLAIM}} | {{RF_PLACEHOLDER:CAP_REQUIRED_CLASS}} | {{RF_PLACEHOLDER:CAP_OBSERVED_CLASS}} | {{RF_PLACEHOLDER:CAP_ARTIFACT}} | {{RF_PLACEHOLDER:CAP_OBSERVED_FACT}} | {{RF_PLACEHOLDER:CAP_EVIDENCE_PROVENANCE}} | {{RF_PLACEHOLDER:CAP_CONTROL_SHAPE_SOURCE}} | {{RF_PLACEHOLDER:CAP_CONTROL_SHAPE_ARTIFACT}} | {{RF_PLACEHOLDER:CAP_DISCHARGED}} |
{{RF_PLACEHOLDER:CAPABILITY_MATRIX_ROW}}

### Capability Block Summary

{{RF_PLACEHOLDER:CAPABILITY_DISCHARGED_COUNT}}/{{RF_PLACEHOLDER:CAPABILITY_TOTAL}} capabilities discharged

**Capability block verdict:** {{RF_PLACEHOLDER:CAPABILITY_VERDICT}} <!-- any Discharged = NO row forces QUARANTINE; a capability with NO ROW AT ALL is a discharge failure, not a default pass -->

## Overall

**Overall verdict:** {{RF_PLACEHOLDER:OVERALL_VERDICT}} <!-- QUARANTINE unless BOTH blocks fully discharge -->

