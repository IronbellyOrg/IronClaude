# Consolidated QA Findings — Phase Gate 5 (Consume/Ownership Rewrite)

**Date:** 2026-06-16
**Gate:** PG5 (M3 standard intensity — 7 report-only lenses)

## Per-lens verdicts

| Lens | Verdict |
|------|---------|
| structural / template-conformance | PASS |
| structural / field-resolution | PASS (all 7 consumed fields resolve to producers; enums exact-match) |
| structural / flag-translation-accuracy | PASS (12/12; dispatch uses only real troubleshoot flags, no --fix) |
| content / ownership-decision-fidelity | PASS (Option 1 faithfully encoded; 9/9 checkpoints) |
| content / crossref-chain | FAIL |
| content / domain-accuracy | FAIL |
| domain / freeze-invariant-preserved | PASS (freeze block byte-identical; no --fix in dispatch) |

## Deduplicated findings + disposition

### Group 1 — IN-SCOPE Phase 5 fixes (apply now)
- **C1 (CRITICAL, crossref) — unbound `{context_path}`.** Step 2 writes `{output_dir}/context.yaml`;
  Step 3 dispatch passes `--context {context_path}` with no binding. FIX: bind them — Step 2 names
  `{context_path}` = `{output_dir}/context.yaml`. (Task Step 5.3 preserves the `{context_path}` token;
  binding clarifies it without removing it.)
- **C2 (IMPORTANT, crossref + ownership-MINOR + template-advisory) — wrong "Step 5 mapping" ref.** The
  Step 3 dispatch says "determined by the Step 5 mapping above" but the depth mapping is in Step 3
  (sub-step 5), and "Step 5" collides with the "Step 5: Tasklist insertion" heading. FIX: reword to
  "the depth mapping above (this step's bullets)".
- **F6 (MINOR, domain) — "based on escalation count" vs systemic override.** Sub-step 5 says depth is
  "based on escalation count" but a systemic/≥3-new-tests 1st trigger jumps to deep (severity, not count).
  FIX: "based on escalation count and failure severity".
- **C6 + F3 + F7 + F5 — Step 4 branch loop/precedence/termination discipline.** FIX (clauses, not a
  rewrite): (a) first-match-wins precedence with the asymmetric-cost gate checked first (F5); (b)
  retry/escalate_depth "(re-enter Step 3; increment `escalation_count`)" for loop discipline + the
  3rd-trigger bound (C6); (c) `escalate_depth` from an already-`--depth deep` run → FULL STOP (no depth
  above deep) (F3); (d) a backend-returned `halt`/`status==failed` is an immediate FULL STOP regardless
  of `escalation_count` (F7).
- **F4 (IMPORTANT, domain) — no docs asymmetric-cost branch.** The consumer special-cases
  `test_is_wrong` (present-to-user, don't auto-fix) but not the symmetric docs case. FIX: add a branch
  `If behavior_is_documented == true (or remediation_target == "docs"): present to user for
  spec/stakeholder review; do NOT auto-insert a code remediation` — mirrors the existing in-protocol
  `test_is_wrong` pattern (not speculative; the docs asymmetric-cost flag already exists in the contract).
- **F2 (CRITICAL, domain) — `partial` fall-through.** A `status=="partial"` run with
  `recommended_escalation=="none"` would hit the insert+resume branch. FIX (clause): note that a
  `partial` diagnosis is routed by `recommended_escalation` (retry/escalate_depth per the backend
  derivation) and the `none`→insert+resume branch applies to a non-degraded (success / clean) result.

### Group 2 — DEFERRED to Phase 6 (NOT fixed here)
- **C3 (crossref) / incident `rca-verdict.md` + `solution-verdict.md` sources** → Phase 6 Steps 6.1/6.2.
- **C4/C5 (crossref) + F1 (domain) / Escalation Budget `/sc:forensic --tier` lines** → Phase 6 Step 6.4.
  These are the LAST live `/sc:forensic` strings; the budget restatement is Phase 6's explicit deliverable.

### Group 3 — NOT fixed (harmless / by-design)
- **F8 (MINOR) — `status==success` and `recommended_escalation==none` redundancy.** The report itself
  calls it "harmless"; kept separate for defensive clarity. No fix.

## Consolidated verdict
- **FAIL** by the "any issue" rule → fix cycle required.
- Actionable in-scope fix set: **Group 1** (C1, C2, F6, the loop/precedence/termination clauses C6/F3/F7/F5,
  the F4 docs branch, the F2 partial guard) — all preserve the task-mandated 6 enum branches verbatim and
  only ADD hardening (consistent with the in-protocol `test_is_wrong` pattern; required for loop termination).
- Group 2 deferred to Phase 6 by design; Group 3 not fixed.
- One serialized rf-qa fix agent applies Group 1, then sync-dev + verify-sync.
