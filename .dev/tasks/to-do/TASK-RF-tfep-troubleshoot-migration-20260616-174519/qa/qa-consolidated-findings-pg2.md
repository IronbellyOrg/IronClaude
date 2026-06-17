# Consolidated QA Findings — Phase Gate 2 (Terminology Rename)

**Date:** 2026-06-16
**Gate:** PG2 (M3 standard intensity — 7 report-only lenses)
**Reports consolidated:** 7 (3 structural rf-qa + 3 content rf-qa-qualitative + 1 domain)

## Per-lens verdicts (as reported)

| Lens | Verdict | Notes |
|------|---------|-------|
| structural / template-conformance | PASS | 8/8 checks; declaration well-formed, headings intact, no broken markdown, no sentinels |
| structural / internal-consistency | FAIL | 3 findings (see classification) |
| structural / scope-confinement | PASS | 11/11; only the 2 in-scope src files touched, all edits inside §4.5, structural tokens TFEP/context.yaml/return-contract.yaml preserved |
| content / backend-neutrality | FAIL | 5 findings (see classification) |
| content / domain-accuracy | FAIL | 3 findings; both Phase-2-scoped sub-claims (escalation-count semantics, task.md:48 warning) PASSED |
| content / crossref-chain | FAIL | 5 findings; "What is correctly migrated" section confirms EVERY Phase 2 target PASSED |
| domain / no-orphaned-forensic-refs | PASS | the 4 surviving forensic hits (214/218/260/261) match the allow-listed deferral set exactly |

## Deduplicated findings + disposition classification

All FAIL findings deduplicate to THREE root buckets. NONE is a legitimate, in-scope,
actionable Phase 2 defect. Rationale per bucket below.

### Bucket A — Intentionally DEFERRED to Phase 5/6 (the 4 surviving forensic tokens)
Lines 214 (`/sc:forensic` invocation), 218 ("forensic return contract" read line),
260–261 (Escalation Budget `/sc:forensic --tier` lines).

- Sources: domain-accuracy #1/#3; crossref F1/F2/F3/F4; internal-consistency Finding 2 (the `--depth quick` side).
- Severity as-reported: CRITICAL/IMPORTANT.
- **Disposition: NOT FIXED NOW — by design.** The Phase 2 preamble in the task file states verbatim:
  "The `/sc:forensic` INVOCATION strings (Step 3 dispatch, escalation-budget lines) and the
  `return-contract.yaml` read line carry both a terminology and a flag-translation concern and are
  deferred to Phases 5 and 6." The purpose-built **no-orphaned-forensic-refs** domain lens PASSED,
  confirming these 4 hits are exactly the allow-listed deferrals. Fixing them now (flag translation
  `--tier`→`--depth`, etc.) IS the Phase 5 (Steps 5.2/5.3) and Phase 6 (Step 6.4) work; doing it here
  would violate phase sequencing. These are resolved within THIS SAME TASK before completion, and the
  Phase 7 + PC.3 whole-migration gates re-verify zero live forensic residue.

### Bucket B — Pre-existing prose OUTSIDE Phase 2's edit scope (never touched)
L144 prohibition rule "without adversarial validation"; L178–179 gradient sub-bullets
("adversarial debate"/"winner/tie"); L229 "## Failure Remediation Plan (Adjudicated)" heading.

- Sources: backend-neutrality #2/#3/#4.
- **Disposition: NOT FIXED — out of scope + premise weak.** Phase 2 Step 2.2 EXPLICITLY left the
  gradient sub-bullets "untouched"; the task never scoped L144 or L229 as edit targets. The
  scope-confinement lens PASSED *because* Phase 2 stayed in bounds — editing these would BREAK that
  invariant. Moreover the leak premise does not hold against the actually-wired backend: `troubleshoot`
  is itself phased (Waves 0–5) and runs an adversarial fix debate (Tier 2), so "through all its
  phases" / "adversarial" / "Adjudicated" are NOT forensic-specific. (The backend-neutrality lens
  reasoned about a hypothetical single-pass backend, not the real one.) If a future maintainer wants a
  deeper neutrality sweep of pre-existing TFEP prose, that is a separate, out-of-scope change — logged
  as a non-blocking follow-up, not a Phase 2 fix.

### Bucket C — Task-mandated exact text / forward-looking declaration
L137 `**Diagnostic backend:** troubleshoot` declaration; L215 "diagnostic escalation backend runs
autonomously through all its phases…"; L208 "Determine the diagnostic depth based on escalation count".

- Sources: domain-accuracy #2 + decl; crossref F5; backend-neutrality #1/#5; internal-consistency #1.
- **Disposition: NOT FIXED — execute as written (F1 Rule #4).** L137/L215/L208 are the EXACT text that
  task Steps 2.1/2.5/2.4 mandate (L137 is "verbatim from R-005"). F1 Rule #4 forbids reinterpreting or
  "improving" mandated checklist text. The declaration describes the migration END STATE and becomes
  literally true at Phase 7; the "invocation string" it references is the dispatch line (flags included),
  which Phase 5 rewrites. The mid-migration tension between a forward-looking declaration and a
  not-yet-swapped invocation is inherent to any sequenced migration and is the task's deliberate design.

## Consolidated verdict

- **Phase 2 work product (Steps 2.1–2.10): DEFECT-FREE.** All three purpose-built structural/scope/orphan
  lenses PASSED; every cross-cutting report independently confirms each Phase 2 TARGET migrated correctly.
- **Actionable in-scope Phase 2 fix set: EMPTY.** Every FAIL finding is deferred-by-design (A),
  pre-existing-out-of-scope (B), or task-mandated-text (C). Applying them would violate phase sequencing,
  scope-confinement, or Rule #4 respectively.
- **Decision: NO FIXES APPLIED. Proceed to PG2.6 verification, then Phase 3.** The transient §4.5
  inconsistency is resolved by Phases 5/6 of this same task and re-verified by the Phase 7 / PC.3 gates.
  Phase 3 edits orthogonal files (troubleshoot command/skill), so proceeding does not compound it.

## PG2.5 fix step — NO FIXES NEEDED

Disposition: **No fixes applied this cycle.** Per the classification above, the actionable in-scope
Phase 2 defect set is EMPTY — every FAIL finding is (A) deferred-by-design to Phase 5/6, (B) pre-existing
prose outside Phase 2's edit scope, or (C) task-mandated exact text. No `fix_authorization: true` agent was
spawned because there is no legitimate in-scope edit to apply, and a fix-authorized agent acting on the
deferred/out-of-scope/mandated findings would violate phase sequencing, scope-confinement, or F1 Rule #4.
verify-sync remains green from Step 2.10 (no file changed since). Proceeding to PG2.6 verification, which
independently confirms the Phase 2 work product is defect-free and the FAIL findings are correctly classified.

## Non-blocking follow-up (logged, not a Phase 2 blocker)
- Optional deeper neutrality sweep of pre-existing TFEP prose (L144/L178–179/L229) and a cross-reference
  between the gradient ladder (L174) and the Escalation Budget (L257) to prevent future drift. Out of
  scope for this migration task.
