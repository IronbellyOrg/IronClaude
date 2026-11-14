# Refactoring Plan: merged reviewer verdict, base Variant 2 (sc:adversarial step 4, Mode A, depth standard, sc:reflect UC-1 run 4)

- Written: 2026-11-10 by the merge executor (steps 3 to 5). Status: complete. Auto-approved (no `--interactive`).
- Aliases. ADV = this folder. TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (sha256 prefix `eb291f0bdd1a7871`, 3020 lines, re-hashed in this step). BASE = `.../revisions/plan-defect-fixes-20261110/baseline/task-before-rev2.md`. DM = the first revision's `.../revisions/chat-output-exception-20261109-133150/delta-manifest.md`. BR = the second revision's `.../revisions/plan-defect-fixes-20261110/BUILD-REQUEST.md`. ADD = `.../revisions/chat-output-exception-20261109-133150/design-addendum.md`. DESIGN = `docs/designs/orchestrator-mode.md`. SK = `/home/coder/.claude/skills/task/SKILL.md`. CONS = `debate/consensus.md`. PROBE = `invariant-probe.md`. T1 = `../reflection-card-t1.yaml` (reference only).

## Overview

- Base: Variant 2 (reviewer 2, qa, calibrated C 0.86), `variant-2-original.md`; selected in `base-selection.md` with 0.950 against V3 0.883 and V1 0.850 (margin 6.7 points, no tiebreaker).
- Incorporating from: Variant 1 (R1-F1..F5), Variant 3 (R3-F3), the diff analysis (O-001, O-002), the invariant probe (fix corrections), and the Tier 1 card as corroboration.
- Output: `merged-verdict.yaml` (schema `sc-reflect-merged-verdict/v1`, the shape of the run 3 file, with `{ref, quote}` evidence pairs that are re-checked mechanically), plus `merge-log.md` and `return-contract.yaml`.
- Source of truth: CONS section 1 for the finding list, final severity and scope; PROBE for corrections of fix wording that CONS did not settle. No finding's severity or scope departs from CONS.
- Planned changes: 11 (nine finding changes M-01..M-09, one header and invariants change, one closing-blocks change).
- Overall risk: Low. Every change edits the merged verdict only. Nothing is applied to the task file, DESIGN, the addendum, either revision folder outside `reflect/pre/adversarial/`, the ledger or any source.
- Convergence: 0.935 (29 of 31 diff points with stated prose positions; CONS primary reading) and 0.774 (24 of 31, `POINT` lines only). Threshold 0.80 met on the primary reading. Invariant gate: BLOCKED_BY_INVARIANTS, because PROBE left INV-R4-003 UNADDRESSED (HIGH) and INV-R4-011 PARTIAL (HIGH, counted as unaddressed by the gate). Both are carried in findings; neither is recorded as accepted risk.

## Final findings (copied from CONS section 1; the merged verdict uses exactly these)

| Merged id | Defect (short) | Final severity | In the 85 allowed labels? | Origin |
|---|---|---|---|---|
| M-01 | 7.17 Verification demands PENDING and a halt that its own resume clears; Action step 1 rewrites PENDING on resume (O-001 folded) | HIGH, conditional on the owner allowlist branch firing (approval or refusal) | no: needs new bounded authorization (7.17 has no DM row) | pre-existing |
| M-02 | 7.24 lens rejects an owner-approved OQ-17/OQ-18 change; 7.24 missing from the 7.17 step 2 follow-up list | HIGH, conditional on the branch firing, owner approval, follow-up before the 7.21-7.28 panel | yes (DM:27); not one of F-01..F-10, owner acceptance by name advised | pre-existing |
| M-03 | 7.30/7.34 write the sha256 baseline into the fix agent's own output file | MEDIUM | yes (DM:32, DM:35; 14.x parity DM:100, 103, 110, 113) | introduced by the second revision at 7.30/7.34 |
| M-04 | 7.30/7.34 re-run lists omit the 7.20 authorization-section check | LOW | yes | introduced with the second revision's re-run list |
| M-05 | 7.10 Branch 2 has no resume/retry rule for an existing section or style edit | LOW | yes (DM:21) | second revision text (F-04) |
| M-06 | 7.10 omits the ADD:17 and ADD:19 clauses and rewords the ADD:19 quote | LOW | yes (DM:21); the two clauses are outside the F-03 list (BR:27) | second revision text (F-03) |
| M-07 | 7.20 matches an executor-written quote against an authority that points both ways; later-message branch has no comparator | LOW | 7.20 yes (DM:23); root cause BR:9 is outside the plan | deliberate second-revision edit B2-1 |
| M-08 | 13.18/13.22 fix agents may edit the docs with no DESIGN hash guard | LOW | yes (DM:73, DM:76) | pre-existing |
| M-09 | 7.17 Context and the OQ-17/OQ-18 entries cite stale DESIGN line numbers | LOW (navigation) | no | pre-existing |

Dropped: R3-F2 withdrawn (13.1 credits ticked 5.2; TL:2265 is true as written; all three advocates, CONS section 1 row "withdrawn"). Closed: R3-F1 and O-003 (the run-4 coverage matrix was stale when V3 read it; it was rebuilt at 05:56:15, line 7 now reads `run: 4`, and `status: partial` is only on line 225; CONS section 1 row "closed").

## Planned Changes

Evidence rule for every change: each `evidence` entry in the merged verdict is `{ref: 'ALIAS:line' or 'ALIAS:a-b', quote}` where the quote is a verbatim substring of the cited range, read in this step. Before finishing, every quote is re-checked by a script; a quote that does not match is fixed or dropped.

### Change 1: M-01 (HIGH-conditional, outside the 85) from the base
- **Source**: Base V2 R2-F1 (claim, case walk, "needs a bounded authorization extension"); diff analysis O-001 (Action step 1 rewrites PENDING on resume), folded per CONS section 2 row O-001.
- **Target**: finding M-01 (replace the base claim with the CONS 4.2 trace; append the O-001 part).
- **Rationale**: CONS 4.2: the Verification is read after the resume (TL:195 "do not tick the item"; SK:535 "This is where execution resumes."), when step 3 has set RESOLVED and cleared the halt (TL:1272); Verification and Completion gate (TL:1275) cannot both hold. Unanimous HIGH in Round 2 (R2v1:75, R2v2:119, R2v3:104).
- **Integration**: fix keeps V2's split (first-halt proof moves to the append-only Execution Log row; completion requires RESOLVED, filled owner lines, the refusal record or the approval follow-up, no open HALT) and adds from PROBE: skip Action step 1 when the record exists (INV-R4-005), both outcomes can fire and a still-PENDING record blocks completion (INV-R4-004), keep one physical line (INV-R4-006), and the extension must also cover the approval follow-up of TL:1271, whose "DESIGN edit item ... with its own review gate" does not exist and whose R5 re-run targets ticked items (INV-R4-003, HIGH, UNADDRESSED).
- **Base weakness addressed**: V2's fix asks for "the applicable approval follow-up" without noticing that no item can produce it; INV-R4-003 (raised in Round 2 by V1 and V3 advocates, R2v1:45, R2v3:15) supplies it.
- **Risk**: Low (merged verdict only).

### Change 2: M-02 (HIGH-conditional, inside the 85) from the base, corrected by the probe
- **Source**: Base V2 R2-F2; CONS 4.1 (halt chain to the monotonicity HALT); PROBE INV-R4-009, 011, 012, 013, 014.
- **Target**: finding M-02 (keep the base claim; replace the fix).
- **Rationale**: Round 2 votes H/M/H; CONS 4.1 rejects V2's own downgrade to M ("V2's owner-intervention workaround is the owner revising the plan, which is available for every defect").
- **Integration**: the fix names all three breaching checks of TL:1321 (probe commands limited to templates 1 to 8, forbidden `run-current --json`, ten ALLOWED_ORCA templates) instead of the one-clause restatement in the diff analysis, which covered only two (INV-R4-011, HIGH, PARTIAL); takes the approval from the RESOLVED OQ-17/OQ-18 record, which the fixer may not change, not from 1.0a-facts.md, which it may (INV-R4-009); keeps ten templates on the default and refusal paths (INV-R4-014) and every halt (INV-R4-013). V2's sub-fix "Apply the same qualification to the reused R5 review inputs" is dropped: it would edit ticked completed bodies (INV-R4-012); the 7.24 slot on the 7.17 follow-up list rides with the M-01 extension.
- **Base weakness addressed**: partial fix (INV-R4-011) and an infeasible sub-fix (INV-R4-012); better from PROBE.
- **Risk**: Low.

### Change 3: M-03 (MEDIUM, inside the 85) from Variant 1
- **Source**: V1 R1-F3; T1 L1 (corroboration; adds the sentence order and the missing FAIL branch); PROBE INV-R4-015..019.
- **Target**: new finding M-03.
- **Rationale**: CONS 4.3, votes L/M/M; facts checked by all three; introduced by the second revision (BASE has `sha256sum` only on 2614, 2642, 2705, 2733).
- **Integration**: fix from V1 (separate orchestrator-owned sums file, not passed to the fixer) plus "do not re-record on a resume" (INV-R4-015), "Then spawn" before the re-check and a FAIL branch (T1 L1), and the 14.x parity as an owner-acceptance item (INV-R4-019; T1 L5 adds the second revision request to the 14.x sum lists).
- **Risk**: Low.

### Change 4: M-04 (LOW, inside the 85) from Variant 1
- **Source**: V1 R1-F4; T1 L2; PROBE INV-R4-020.
- **Target**: new finding M-04.
- **Integration**: V1's "plus a sha256 of that section" is replaced by re-running the full 7.20 read-and-match step, because a heading count stays 1 when the quote is changed in place and a section hash needs an extraction command the plan does not define (INV-R4-020).
- **Risk**: Low.

### Change 5: M-05 (LOW, inside the 85) from Variant 1
- **Source**: V1 R1-F2 (MEDIUM, downgraded to LOW by all three, R1v1:15-18); T1 L3; PROBE INV-R4-021, 022.
- **Target**: new finding M-05.
- **Integration**: fix from V1, with two corrections: apply the qualifier per site only where absent, because `grep -c` counts lines and a doubled prefix still counts 6 (INV-R4-021; counting occurrences would change a 7.20 command, which G5 forbids); take "before" excerpts from the original start `a09f6a12...`, not HEAD (INV-R4-022).
- **Risk**: Low.

### Change 6: M-06 (LOW, inside the 85) from Variant 1
- **Source**: V1 R1-F5 (MEDIUM, downgraded to LOW); T1 L6; PROBE INV-R4-024, 025.
- **Target**: new finding M-06.
- **Integration**: fix from V1. INV-R4-025 (which literal is authoritative) is settled here by reading both: BR:27 and ADD:19 say "advice prohibited by the sweep skill"; the run 3 merged verdict's F-03 claim paraphrased it as "advice the sweep skill prohibits", which is the wording TL:1210 copied. Quote ADD:19, the normative source. T1 L6's extra clause (ADD:21 sentence 3) is added as optional, labelled not debated.
- **Risk**: Low.

### Change 7: M-07 (LOW; 7.20 inside the 85, root cause outside) from Variant 1
- **Source**: V1 R1-F1 (MEDIUM, downgraded to LOW; V1 conceded its "Today 7.20 returns PASS" was overstated, R1v1:58); T1 L8; PROBE INV-R4-026, 027.
- **Target**: new finding M-07.
- **Integration**: V1's fix (owner saves the message to a file and the BR match target is dropped) is not carried: it reverses the deliberate edit B2-1 and invents an owner action (INV-R4-027). Carried instead: keep the match target; optional owner clarification of BR:9; optional 7.20 clause for the later-message-plus-resume case, whose FAIL route loops to ticked 7.10 (INV-R4-026, MEDIUM, conditional, UNADDRESSED in the debate).
- **Risk**: Low.

### Change 8: M-08 (LOW, inside the 85) from Variant 3
- **Source**: V3 R3-F3; PROBE INV-R4-028, 029.
- **Target**: new finding M-08.
- **Integration**: fix from V3's first option, writing the 13.x baseline to a separate orchestrator-owned file so the parity edit does not copy the M-03 collision (INV-R4-028). V3's second option (compare DESIGN with the frozen hash `e4a06d0c...`) is not carried (withdrawn, R2v3:19, :90).
- **Risk**: Low.

### Change 9: M-09 (LOW, outside the 85) from the diff analysis
- **Source**: diff analysis O-002 (all three advocates LOW, R2v1:179, R2v2:137, R2v3:200); PROBE INV-R4-030.
- **Target**: new finding M-09.
- **Integration**: cite the DESIGN sentences by quoted text or section rather than corrected line numbers, because an approved DESIGN 7.3 edit would move them again (INV-R4-030). Rides with the M-01 extension. Executor observation added as a note: TL:1272 and the OQ entries also use the shorthand "DESIGN 973" and "DESIGN 971".
- **Risk**: Low.

### Change 10: header and invariant blocks
- **Source**: CONS section 5; PROBE sections 2 to 4.
- **Target**: header comments, `convergence_score` 0.935 with both readings, `convergence_status: BLOCKED_BY_INVARIANTS`, `unaddressed_invariants_high` (INV-R4-003 in M-01, INV-R4-011 in M-02), `unaddressed_invariants_medium` (009, 012, 015, 026), `unaddressed_invariants_low` (006, 019, 020, 021, 022, 025, 030), `invariants_addressed` (19 items).
- **Risk**: Low.

### Change 11: closing blocks
- **Target**: `f_closure` for the run 3 F-01..F-10 (from the three cards, CONS C-001..C-004, X-001..X-003 and the T1 verifier runs, each re-quoted from TL), `tier1_verdicts` (T1 L1..L9), `not_carried`, `departures_from_consensus`, `row_coverage` (coverage matrix summary and the four rows that changed or stay unmapped), `consequence_note`, `residual_notes`, `best_practice_grade`, `confidence_calibrated`, `verdict_recommendation`.
- **Risk**: Low.

## Base weaknesses and the better source

| Base (V2) weakness | Better source | Fix approach |
|---|---|---|
| No finding below HIGH; misses the sha256 baseline collision, the re-run gap, the 7.10 resume and clause gaps, the record-only 7.20 check | V1 (R1-F1..F5), V3 (R3-F3) | Add M-03..M-08 |
| F-07 closure "fixed" | V1 "partial" (CONS X-003 winner V1, "fixed with a residual") | f_closure F-07 partial, residual M-03 |
| F-04 closure "fixed" with no residual named | V1 "fixed with new defects" (CONS X-002 winner V3 on severity: residuals are LOW) | f_closure F-04 fixed, residuals M-04, M-05, M-07 |
| 7.24 fix covers two of three breaching checks | PROBE INV-R4-011 | Fix names all three |
| R5 sub-fix edits ticked items | PROBE INV-R4-012 | Dropped |
| 7.17 fix silent on the missing follow-up items | PROBE INV-R4-003; R2v1:45, R2v3:15 | Part (4) of the M-01 fix |

## Changes NOT Being Made (with rationale)

| Item | Non-base or alternative approach | Why it is not carried |
|---|---|---|
| R3-F2 | 13.1 should credit R4-F5 for the current DESIGN wording | Withdrawn by all three; TL:2265 is true as written (CONS row "withdrawn", R1v3:29) |
| R3-F1, O-003 | Rebuild the coverage matrix | Already done on disk (matrix line 7 `run: 4`; only line 225 `status: partial`); closed (CONS) |
| R1-F1 fix | Owner saves the message to `execution-authorization.md`; drop the BR section as match target | Reverses edit B2-1 and invents an owner action (INV-R4-027; R1v1:58, R2v2:51, R2v3:122) |
| R1-F1 verifier | "Today 7.20 returns PASS" | Overstated; conceded by V1 (R1v1:58), rejected by all (CONS X-005) |
| R3-F3 second option | Compare DESIGN with the frozen hash at the start of 14.25 | Withdrawn (R2v3:19, :90) |
| R2-F2 sub-fix | Qualify the reused R5 review inputs | Would edit ticked completed bodies (INV-R4-012) |
| R1-F4 section hash | sha256 of the authorization section | Needs an undefined extraction command; re-running the 7.20 read-and-match is enough (INV-R4-020) |
| M-05 occurrence count | Change the 7.20 grep to count occurrences | Would change a 7.20 command (invariant G5, INV-R4-032); per-site "only where absent" instead |
| M-02 at MEDIUM | V2 advocate's downgrade (R2v2:120) | CONS 4.1: a correct approved run cannot reach `Decisions gate: PASS`; HIGH-conditional kept |
| M-03 at LOW | V1 advocate's downgrade (R2v1:96) | CONS 4.3: 2 of 3 on MEDIUM; durable evidence placed where an instructed write can remove it |
| R1-F1, R1-F2, R1-F5 at MEDIUM | V1's card severities | All three advocates accept LOW (CONS 4.4; V1's own downgrades R1v1:15-18) |
| T1 L4, L7, L9 as findings | Tier 1 LOW items not raised by any card | Not debated; kept as residual notes, not findings |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 1, 2 | Low | A HIGH-conditional finding mis-scoped; caught by the quote check and the scope table above | Restore the base V2 claim and fix text |
| 3-9 | Low | Additive findings; a bad quote is dropped by the mechanical check | Remove the finding |
| 10, 11 | Low | Header or bookkeeping error | Re-derive from CONS and PROBE |

## Review Status
- [x] Auto-approved (default; no `--interactive`)
- [ ] User-approved
- Approved by: auto
- Approval timestamp: 2026-11-10 (date only; no clock time was recorded for this step)

