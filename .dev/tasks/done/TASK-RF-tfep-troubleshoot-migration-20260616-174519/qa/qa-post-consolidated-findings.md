# Consolidated Post-Completion QA Findings (Step PC.3)

**Date:** 2026-06-16
**Gate:** PC.3 — Post-completion lens-based QA on the FULL migration (M3 standard, 7 lenses)

## Per-lens verdicts

| Lens | Verdict |
|------|---------|
| structural / template-conformance | PASS |
| structural / internal-consistency | FAIL (1 IMPORTANT + 2 MINOR) |
| structural / completeness | PASS (8/8 changes) + 1 IMPORTANT wiring gap |
| content / actionability | FAIL |
| content / domain-accuracy | FAIL (1 CRITICAL + 1 IMPORTANT) |
| content / crossref-chain | FAIL (1 CRITICAL + 1 MINOR) |
| domain / backend-neutrality | FAIL (3 borderline leaks); residual forensic sweep CLEAN (0 hits) |

## Deduplicated findings + disposition

### FIX-1 (CRITICAL — caught by domain-accuracy, crossref, actionability) — `behavior_is_documented` is a dead predicate
The §4.5 Step 4 docs branch (line 225) and the precedence note (line 222) reference `behavior_is_documented`,
but that field is NOT in the 7-field `return-contract.yaml` wire set (status, test_is_wrong,
recommended_escalation, tasklist_insertion_path, remediation_target, root_cause_summary, solution_summary —
SKILL.md:471, report-template TFEP Consumer block). `behavior_is_documented` is used INTERNALLY by step 4.5
to compose `remediation_target`. **This was introduced by the PG5 F4 docs-branch fix — exactly the kind of
cross-phase regression post-completion validation exists to catch.** FIX: key the docs branch on
`remediation_target == "docs"` ONLY (the wire-available field; per the Phase 4 row, `remediation_target=docs`
is set "when `behavior_is_documented` indicates a doc gap" — so it faithfully captures the docs asymmetric
case). Update the line-222 precedence note to name `remediation_target == "docs"` instead of
`behavior_is_documented`.

### FIX-2 (IMPORTANT — internal-consistency F1) — `--context` Options row mislabels the input brief
troubleshoot.md:59 `--context` row example reads "TFEP `return-contract.yaml` consumer brief", but `--context`
is the INPUT brief the caller passes IN (the `context.yaml` written by task-protocol Step 2);
`return-contract.yaml` is the OUTPUT troubleshoot emits. FIX: change the example to "TFEP `context.yaml`
consumer brief".

### FIX-3 (IMPORTANT — domain-accuracy IMPORTANT-1) — Step 5 item 10 vestigial vs item 11
Item 10 reads `tasklist_insertion_path` but it defaults to `null` in diagnosis-only mode (Phase 4 PG4 fix),
while item 11 composes the block from the summary fields. FIX: clarify item 10 — "when `null` (the default
in diagnosis-only mode), compose the block from the summary fields per item 11."

### FIX-4 (IMPORTANT — completeness) — `## TFEP Consumer` report-template block not wired to render
The report-template `## TFEP Consumer` section exists but no Wave 5 step explicitly renders it into REPORT.md
(step 2 compose-list omits it; step 4.5 only writes return-contract.yaml). The TFEP loop is FUNCTIONAL via
return-contract.yaml regardless, but the human-readable echo is orphaned. FIX: add a brief clause to Wave 5
step 4.5 noting the same fields are also rendered as the `## TFEP Consumer` section of REPORT.md (per
refs/report-template.md) when caller=task-unified.

### NOT FIXED — documented non-blocking follow-ups
- **escalation_count explicit comparison** (actionability F2/F4): `escalation_count` IS initialized in Step 2's
  failure_context (item 3) and the "3rd TFEP trigger → FULL STOP" trigger-count semantics are the ORIGINAL
  (pre-migration) design preserved verbatim. The prose-vs-predicate looseness is pre-existing, not migration-
  introduced. Follow-up only.
- **--output-dir slug path-join** (actionability F3): whether troubleshoot uses a caller `--output-dir`
  verbatim vs creating a sub-slug dir is a pre-existing troubleshoot output-dir behavior; reconciling it is a
  deeper design question outside this migration's scope. Follow-up only.
- **backend-neutrality 3 leaks** (Wave 5 cross-ref at L219, artifact filenames at L260, "troubleshoot" prose
  in the L239 ownership note): the artifact-filename question was already adjudicated in PG6 (report_path/
  audit_log_path are permitted artifact bindings); the Wave 5 cross-reference and the ownership note's naming
  of the wired backend are helpful pointers and the `**Diagnostic backend:**` declaration already names the
  backend. These are acceptable backend cross-references, not residual forensic leaks (the forensic sweep is
  CLEAN — 0 hits). Not re-fixing.
- template-conformance / crossref MINORs (CommonMark list interleave, fragile ordinal back-ref in
  report-template): cosmetic, pre-existing patterns. Not fixed.

## Consolidated verdict
- **FAIL** by the "any issue" rule → fix cycle 1.
- Actionable in-scope fix set: **FIX-1 … FIX-4** (cross-phase issues the post-completion gate legitimately
  caught, most importantly FIX-1 — a dead predicate introduced by the PG5 fix).
- One serialized rf-qa fix agent applies FIX-1..FIX-4, then sync-dev + verify-sync, then a 2-agent
  verification round.
