# Consolidated QA Findings — Phase Gate 4 (Return-Contract Adapter)

**Date:** 2026-06-16
**Gate:** PG4 (M3 standard intensity — 7 report-only lenses)

## Per-lens verdicts

| Lens | Verdict |
|------|---------|
| structural / template-conformance | PASS (1 MINOR cosmetic: `4.5.` not strict-CommonMark, pre-existing pattern) |
| structural / completeness | PASS (5/5 adapter elements present) |
| structural / internal-consistency | PASS (field names + both enums byte-identical across 3 surfaces) |
| content / domain-accuracy | PASS (all 5 fields cite donors that exist) |
| content / actionability | FAIL (5 derivation-specificity findings) |
| content / backward-compat | PASS (additive; only contract_version row edited; 30 prior fields intact) |
| domain / contract-producer-consumer-integrity | PASS (all 4 consumer tokens have producers) |

## Deduplicated findings + disposition

### Cluster A — emission-step derivation specificity (actionability FAIL) → FIX (proportionate)
The emission step 4.5 (task-mandated text) lists 7 fields; 6 have source clauses, and the lens wants
tighter derivation for several. Applying proportionate clarifying clauses — bounded to the skill's
existing prose-derivation style and the task's additive-rows + Option-1 ownership design (NOT a
maximalist truth table, since the skill is LLM-executed prose and the enum→action mapping lives on the
Phase 5 consumer side per the Step 4.1 design note):

- **I-1 (CRITICAL) — `tasklist_insertion_path` has no source clause.** Real omission (only field of 7
  without one). FIX: add a source clause aligned with Option 1 — default `null` in TFEP diagnosis-only
  mode; the task-protocol composes the `## Failure Remediation Plan (Adjudicated)` block from
  `remediation_target`/`root_cause_summary`/`solution_summary` (Phase 5 Step 5.8). Populated only if
  troubleshoot wrote a standalone adjudicated remediation-plan file. (Avoids inventing a new artifact.)
- **I-4 (IMPORTANT) — `test_file_path` not in the 7-field wire set though `remediation_target=test`
  pairs with it.** FIX: add a one-clause note that `test_file_path` stays in the broader Output
  Contract / REPORT.md (not duplicated into the TFEP wire set); the consumer's asymmetric-cost branch
  presents to the user and does not need the path duplicated.
- **I-2 (IMPORTANT) — abs vs repo-relative path form.** FIX: state inline that path-valued fields in
  the emitted return-contract.yaml are absolute (matches the `(abs path)` typing on `tasklist_insertion_path`).
- **I-3 (IMPORTANT) — `recommended_escalation` inputs named, no enum mapping.** FIX (light): add a
  brief deterministic hint (failed/hard-stop→halt; partial+low-confidence→escalate_depth;
  partial+tier<2→retry; success→none). Not a full truth table — the consumer-side action mapping is
  Phase 5 Step 5.6; this is a producer-side tie-break hint to reduce divergence.
- **I-5 (MINOR) — `status` un-sourced + `failed` reachability.** FIX: add "`status`: copy from the
  Output Contract `status` (step 3)". The 3-value `success|partial|failed` matches the Output Contract
  `status` row; the 2-value audit footer is pre-existing and out of scope.

### Cluster B — §4.5 line 214 still `/sc:forensic` → DEFERRED to Phase 5 (NOT fixed here)
Source: contract-producer-consumer lens (IMPORTANT, flagged "for Phase 5").
- The consumer-side invocation in `sc-task-protocol/SKILL.md` §4.5 still says `/sc:forensic --tier/--intent`.
- **Disposition: DEFERRED — Phase 5 Step 5.3 rewrites the dispatch to `/sc:troubleshoot`.** Not a Phase 4
  defect; the producer/consumer TOKEN integrity (this lens's actual scope) PASSED.

### Cosmetic (no fix)
- template-conformance MINOR: `4.5.` numbering / footer-fence list-break is a pre-existing markdown
  pattern with no executable impact. Not fixed.

## Consolidated verdict
- **FAIL** by the "any issue" rule → fix cycle required.
- Actionable in-scope fix set: **Cluster A** (5 proportionate clarifications to the Wave 5 step 4.5 emission).
- Cluster B deferred to Phase 5 by design; cosmetic MINOR not fixed.
- One serialized rf-qa fix agent applies Cluster A, then sync-dev + verify-sync.
