# Consolidated QA Findings — Phase Gate 3 (Flag Ingestion)

**Date:** 2026-06-16
**Gate:** PG3 (M3 standard intensity — 7 report-only lenses)

## Per-lens verdicts

| Lens | Verdict |
|------|---------|
| structural / template-conformance | PASS (6/6) |
| structural / flag-completeness | PASS (all 9 sites wired exactly once) |
| structural / internal-consistency | FAIL |
| content / actionability | FAIL |
| content / thin-command-fidelity | PASS |
| content / domain-accuracy | FAIL |
| domain / convention-fidelity | FAIL |

## Deduplicated findings + disposition

### Cluster 1 — Wave 5 emission BODY absent → DEFERRED to Phase 4 (NOT fixed here)
Sources: internal-consistency #1 (CRITICAL), #3 (IMPORTANT), #4 (MINOR); actionability F1 (CRITICAL).
- Finding: `caller=task-unified` → `return-contract.yaml` emission is advertised by the command `--caller`
  row, the skill Wave 0 step 6 "(see Wave 5)", and the reserved `return_contract_path:` footer key, but
  the Wave 5 BODY has no emission step; the "(see Wave 5)" forward-reference currently lands on nothing.
- **Disposition: DEFERRED — by design.** The Wave 5 emission step is the explicit deliverable of
  **Phase 4 Step 4.7** ("Add the conditional Wave 5 return-contract.yaml emission step"). Phase 3 Step 3.7
  verbatim says the new step 6 "references the audit header and Wave 5 emission added in this and **the next
  phase**." So Phase 3 deliberately wires the trigger + footer key and defers the emission BODY to Phase 4.
  The QA agents correctly observed the ABSENCE but were not briefed that the body is Phase 4's first concern.
  PG4's contract-producer-consumer + completeness lenses re-verify the body lands. NOT a Phase 3 defect.

### Cluster 2 — `--context` "echoed in the Wave 5 return" lacks a `context_path` footer key → FIX
Sources: internal-consistency #2 (IMPORTANT); domain-accuracy (FAIL).
- Finding: the command `--context` Options row (task-mandated, Step 3.2) promises the context is "echoed
  in the Wave 5 return," but the SUMMARY footer (the Wave 5 machine-readable return) records only `caller:`
  and `return_contract_path:` — there is no `context_path:` echo. Phase 4 does not add one either (its
  return-contract carries status/test_is_wrong/etc., not context_path), so the promise stays unfulfilled
  unless reconciled now.
- **Disposition: FIX (in-scope).** Apply option (a): add `context_path: <abs-path|none>` to the Wave 5
  SUMMARY footer. This is additive, mirrors the existing TARGET-header `context_path:` key + the footer
  style, fulfills the task-mandated `--context` promise (preferred over softening mandated text per Rule #4),
  and makes the cross-surface claim self-consistent.

### Cluster 3 — backtick convention deviations on troubleshoot.md:69 → FIX
Sources: convention-fidelity #1, #2 (both IMPORTANT).
- Finding: the new surface clause renders `(if caller=task-unified)` and bare `return-contract.yaml`,
  but the sibling exemplars on the same line backtick their inner token (`(if \`--fix\`)`,
  `(if \`pipeline_hardening_applicable\`)`) and `return-contract.yaml` is backticked everywhere else
  (rows L59/L60, skill L143).
- **Disposition: FIX (in-scope).** Backtick both tokens so L69 reads:
  ``…and (if `caller=task-unified`) the emitted `return-contract.yaml` path.``
  This better fulfills Step 3.5's own stated intent ("mirrors the existing `(if ...)` convention").

## Consolidated verdict
- **FAIL** by the "any issue" rule → fix cycle required.
- Actionable in-scope fix set: **2 fixes** (Cluster 2 footer key + Cluster 3 backticks).
- Cluster 1 (CRITICAL Wave 5 body) is DEFERRED to Phase 4 by explicit task design — NOT fixed in PG3.
- One serialized rf-qa fix agent will apply the 2 fixes, then sync-dev + verify-sync.
