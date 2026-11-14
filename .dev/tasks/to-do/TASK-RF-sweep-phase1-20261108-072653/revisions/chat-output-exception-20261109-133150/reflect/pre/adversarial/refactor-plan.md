# Refactoring Plan: merged reviewer verdict (sc:adversarial step 4, Mode A, depth standard)

Aliases. TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`. ADD = `.../revisions/chat-output-exception-20261109-133150/design-addendum.md`. DM = that folder's `delta-manifest.md`. BR = that folder's `BUILD-REQUEST.md`. DES = `docs/designs/orchestrator-mode.md`. STYLE = `src/superclaude/output-styles/pragmatic.md`. CONS = `debate/consensus.md`. PROBE = `invariant-probe.md`. All paths in this folder are relative to `reflect/pre/adversarial/`.

## Overview

- Base variant: Variant 2 (reviewer 2, qa, haiku slot, calibrated C 0.86), `variant-2-original.md`. Selected by `base-selection.md`: combined V3 0.950, V2 0.933, V1 0.902; margin 1.7 percentage points is under 5, so tiebreaker level 1 (debate points won V2 10, V3 4) chose V2.
- Incorporated variants: Variant 1 (findings R1-F2, R1-F4, R1-F5; verifier text) and Variant 3 (findings R3-F1, R3-F2, R3-F3; verifier text). The merged card keeps V2's table frame (finding id, severity, class, location, what is wrong, evidence, smallest fix and verifier, confidence).
- Output: `merged-verdict.yaml` (schema `sc-reflect-merged-verdict/v1`, shape of the run 2 file but with `{ref, quote}` evidence pairs) and `merge-log.md`.
- Planned changes: 12 (ten finding changes, one convergence-status change, one residual-notes change). Source of truth for severities and fixes: CONS "Merge candidates" as corrected by PROBE where PROBE found a candidate wrong or insufficient. Where PROBE and CONS differ, PROBE wins and the change says so.
- Overall risk: Low. Every change edits the merged card only. No change edits the task file, the design, the addendum, the ledger, or any source.
- Convergence: diff-point convergence is 36 of 38 = 0.947 (CONS), but the invariant gate is BLOCKED_BY_INVARIANTS: PROBE has 1 HIGH UNADDRESSED item (INV-005). It is folded into F-02 below (Change 2) and is not recorded as accepted risk.

## Planned Changes

Evidence rule for every change: each `evidence` entry is `{ref, quote}` where the quote is a verbatim line the merge-executor Read in this pass (TL, DES, ADD, DM, BR, STYLE or the OQ-6 record), with a path alias from `path_aliases`. A line it cannot re-read is dropped, not carried.

### Change 1: F-01 (HIGH, unsound-check) from M-01, widened by INV-013, INV-015, INV-019, INV-020
- Source: V2 R2-F1 (base, HIGH), V1 R1-F3, T1 F3, U-004; PROBE corrections.
- Target in merged card: finding F-01 with location TL:1293 (7.20), TL:1363 (7.30), TL:1391 (7.34); optional lens-input lines TL:1299-1404 and TL:2572.
- Content: the exact-8 `wc -l` check fails a correct run when a 7.17 branch writes OQ-17 or OQ-18 (TL:1270, TL:1272). Fix in three parts, all inside the 82 revised bodies (DM:21-116): (a) count only `OQ-[1-8]-*-decision.md` and check each existing OQ-17 or OQ-18 file separately with a skip-if-absent form (INV-013); (b) the lens-input wording "OQ-1 to OQ-8" on the twelve lens lines and TL:2572 must be reworded, not optional, because the glob hands the lens nine or ten files (INV-015; CONS marked it optional while V1 and V3 said required, and no concession exists); (c) give the second 7.20 grep (`does NOT authorize adoption`) an expected value for OQ-17 and OQ-18 (INV-019, expected 1 each when present).
- Sufficiency note (INV-020, MEDIUM, conditional on a branch firing): even with the count fixed, 7.13 writes seven rows to `owner-decisions.md` (TL:1231-1233), 7.22 checks seven rows (TL:1307) and 7.25 checks that every RESOLVED decision file is matched (TL:1328). An OQ-17 row is added by nobody, so the gate can halt at the regression halt (TL:1384 a) or the monotonicity halt (TL:1384 b). The fix must also say who adds the row and make the 7.22 count "seven plus one per resolved optional decision". State this as part of F-01, not as a separate finding.
- Verifier: three file sets (eight prerequisites; plus one optional resolved decision; plus both) pass, an unresolved required record fails, and 7.22 and 7.25 give the same answer on all three sets.
- Risk: Low.

### Change 2: F-02 (HIGH, unsound-check; needs new authorization) from M-02, INV-005, INV-022
- Source: V2 R2-F2 (base, HIGH), T1 F1; PROBE INV-005 (the HIGH invariant) and INV-022.
- Location: TL:2265 (13.1 Action), TL:2267 (13.1 Verification), DES:716.
- Content: the 13.1 Verification greps the old R2 sentence while the Action says to copy the DESIGN text; following the Action fails the item's own check, and keeping the old text fails the 13.12 lens (TL:2342). Text fix: replace the quoted example and first grep with the DES:716 wording, using `grep -nF` because DES:716 holds inner double quotes and backticks (INV-022), keep the placement check against neighbouring bullets, do not touch ticked item 5.2 (TL:774-778).
- Authorization gap (INV-005, HIGH, UNADDRESSED in CONS): 13.1 is unticked (TL:2263) but is not one of the 82 labels (DM:65-78 lists 13.9 to 13.24 only). DM:13 allows differences only inside the listed labels and BR:53 requires hunks only in approved bodies. Applying the text fix would break the preservation comparison, and not applying it leaves 13.1 unable to be ticked. Both branches block. The card must say that this fix needs a new bounded authorization or a manifest amendment, and must NOT present it as an edit the revision can make. This change folds INV-005 into the finding; it is not recorded as accepted risk.
- Verifier: after an authorized edit, the edited grep prints line 404 on `src/superclaude/core/HOW-WE-WORK.md` and the old sentence has no hit outside TL:776 and TL:778.
- Risk: Low for the card; the plan itself is blocked at 13.1 until authorized.

### Change 3: F-03 (MEDIUM, partial) from M-03 with INV-016, INV-023
- Source: V3 R3-F2 (MEDIUM), V1 R1-F4, T1 F5.
- Location: TL:1210 (7.10 Action) against ADD:15, 17, 19, 21 and TL:1980 (11.4 pins).
- Content: 7.10 omits operative clauses that 11.4 tests (same-message case, "Formatting never authorizes...", "chat-presentation only"). Fix: embed the missing sentences on the same physical line; restate ADD:21 sentence 4 in the present tense and do not copy "proposed". Add no new substring assertion to 11.4. Probe additions: (a) 11.4 pins must check the presence of eligibility clauses and never the absence of the words "runtime detector" or "tool allowlist", which the embedded clauses contain (INV-016); (b) ADD:19 sentence 1 (blockers, parse errors, missing required output, unsuccessful report Reads) is not in the clause list and should be (INV-023).
- Verifier: `grep -n` for "same message", "Formatting never" and "chat-presentation" on TL hits line 1210 as well as 1973.
- Risk: Low.

### Change 4: F-04 (MEDIUM, missing) from M-04 with INV-001, INV-024
- Source: V1 R1-F2 (relabelled from gate-bypass), T1 F4.
- Location: TL:1210 Branch 1, TL:1213, TL:1293.
- Content: 7.10 fails closed but names no carrier for the user's separate execution authorization or the fresh sign-off reports. Fix: the step-7.10 result file (`phase-outputs/test-results/step-7.10-style-exception.md`, TL:1211) holds the dated verbatim quote and the supplied report paths and is written BEFORE the style edit (INV-001: the Execution Log row is only appended at completion, TL:1213, so after a failed check a resumed session would see Branch 1). The PRE report path is "as supplied with the authorization", not a fixed path, because it does not exist yet (INV-024 falsifier 2). State plainly that a quote written by the same executor is a record, not independent evidence (INV-024 falsifier 1), and give 7.20 a command and expected value for checking the quote (INV-024 falsifier 3, the defect class of F-08).
- Verifier: the result file exists with a dated quote before the first style diff; `grep -n` of the quote header hits it.
- Risk: Low.

### Change 5: F-05 (LOW, partial) from M-05 with INV-003
- Source: V1 R1-F1 (downgraded from MEDIUM), T1 F2.
- Location: TL:1982 (11.4 Verification), convention TL:1295, fixer 11.14 at TL:2048-2050.
- Content: 11.4 omits "re-run this item" so the in-place repair route is implicit; no stall is proven. Correction from PROBE INV-003: sending a style defect back to the ticked item 7.10 is a retry that can run into the legacy retry restore which erases the design append (ADD:45; TL:1210 final sentence says STOP). So the fix has two forms: for a defect in `sweep.md` or `SKILL.md`, re-run 11.1 or 11.3 in place per TL:1295; for a defect in STYLE, HALT with a named blocker and a next step (not a silent "stop incomplete"). Drop the proposed "fresh authorization only if the original scope does not cover the repair" rule (undefined, clashes with F-04).
- Verifier: `grep -n 're-run this item'` hits TL:1982 and every 11.4 failure branch ends in a named next step.
- Risk: Low.

### Change 6: F-06 (MEDIUM, stale-text) from M-06 with INV-012, INV-025
- Source: V3 R3-F1 (MEDIUM, lowered to LOW in the debate), T1 U-005.
- Location: the phrase "(unqualified table mandate, not an implemented exception)" in 59 Context lines (TL:1209 plus 58 later items).
- Content: the label is true only until 7.10 runs. Severity: the debate agreed LOW, but PROBE INV-025 shows that the mitigation CONS proposed (a note appended after TL:3018) cannot reach the spawned lens and verifier agents, which receive the item's Context and prompt, not the task file; so a lens that trusts the label can raise a false BLOCKING finding in a gate with a two-cycle cap. Merge severity: MEDIUM, with the reason recorded. CONS's reason for not editing the 58 Contexts ("only line-stable changes are allowed") is wrong: all 58 are inside the 82 bodies and a line-stable in-place edit is allowed (DM:21-116, TL:3016). Fix: reword the 58 Context lines in place to "Pre-7.10 source anchor: STYLE:22 held the unqualified table mandate; after item 7.10 it holds the scoped sweep exception." Keep the 7.10 line as is. The reworded sentence must not repeat the literal "not an implemented exception" (INV-012: it would raise the grep count from 59).
- Verifier: `grep -c 'not an implemented exception'` on TL prints 1 (the 7.10 line) after the edit, or 59 if the cheaper note-only form is chosen.
- Risk: Low.

### Change 7: F-07 (LOW, authority) from M-07 with INV-026
- Source: V3 R3-F3.
- Location: TL:1363 (7.30), TL:1391 (7.34) against `sha256sum` at TL:2614, 2642, 2705, 2733.
- Content: the early fixers guard authority by prose, the 14.x fixers by hash. Fix: record sums of the addendum, BR and the OQ-6 record BEFORE the spawn sentence (a before/after attached to the post-return re-run list has no before value, INV-026) and re-run after; hash only the OQ-6 file, not the whole `plans/` folder (7.30 lets the fixer correct other decision records). Optional.
- Verifier: the fix log shows equal sums before and after; `grep -c sha256sum` on TL rises by two.
- Risk: Low.

### Change 8: F-08 (LOW, missing) from M-08
- Source: V1 U-001.
- Location: last sentence of TL:1293 (7.20 style checks) against TL:1295.
- Content: the style check has no command or expected value although TL:1295 says each check is decided by the expected value beside its command. Fix: add `grep -c 'Except for the sweep chat-summary exception above,' src/superclaude/output-styles/pragmatic.md` (expect 6, confirmed by PROBE INV-017: STYLE lines 53, 58, 60, 69, 80, 90) with a PASS or FAIL line, in the same edit as F-01.
- Risk: Low.

### Change 9: F-09 (LOW, ordering) from M-09 with INV-002
- Source: V1 R1-F5, T1 F7.
- Location: TL:1143 (Phase 7 preamble Branch 2) against TL:1210, TL:1213, TL:3018.
- Content: letter conflict, settled by TL:1213 and the TL:3018 note. Fix: a one-clause pointer in 7.10. Probe note (INV-002, MEDIUM, conditional on how the resume engine reads Blocked, UNVERIFIED): the pointer fixes reading order, not the state during the Action. Record that as a note and mark the finding optional.
- Risk: Low.

### Change 10: F-10 (LOW, stale-text; needs new authorization) from M-10 with INV-006
- Source: T1 F6 as confirmed by V3.
- Location: TL:1551 (8.19) and TL:1812 (10.5) against the OQ-6 record line 12.
- Content: both lines tie the report layout to GQ-63, which affects only the skill's chat reply. Fix: reword so GQ-63 governs the chat reply and GQ-35 the report layout. Neither item is among the 82 bodies (DM lists 8.12 only for Phase 8 and nothing for Phase 10), so this needs the same new authorization as F-02 (INV-006). Optional.
- Risk: Low.

### Change 11: convergence status and unaddressed invariants
- Content: header `convergence_score: 0.947`, `convergence_detail: "36 of 38 diff points; 32 of 38 on the conservative reading"`, `convergence_status: BLOCKED_BY_INVARIANTS`, `unaddressed_invariants_high: [INV-005]` with `folded_into: F-02`. List the MEDIUM UNADDRESSED probe items and where each is carried (INV-001 to F-04, INV-002 to F-09, INV-003 to F-05, INV-006 to F-10, INV-008 to the consequence note in Change 12, INV-015, INV-019, INV-020 to F-01, INV-016 and INV-023 to F-03, INV-024 to F-04, INV-025 to F-06) and the LOW ones (INV-012 to F-06, INV-022 to F-02, INV-026 to F-07).
- Risk: Low.

### Change 12: consequence note and residual notes
- Content: INV-008 (MEDIUM): applying any of F-01 to F-10 changes the compared plan, so the fresh structural, alignment, QA and PRE checks that the revision's 7.10 requires to "name this revised plan" and the preservation proof (355 headers, 137 completed bodies, constraints 157-168) must be re-run after the edits. Each edit must stay on its single physical line. Also carry INV-011 (the "three Follow-Up entries" text in 14.46, TL:2761-2763, is pre-existing, not among the 82, and a fix would need the same new authorization as F-02) and the dropped candidates with reasons from CONS (R2-F3, R3-F4, U-002, U-003, U-007, U-009, U-010, U-011, T1 F8, F9, F10).
- Risk: Low.

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach was kept |
|---|---|---|
| C-005 / X-007 | V3: copy ADD:13-21 whole and add a substring assertion to 11.4 | Rejected by all three in Round 2: ADD:21 sentence 4 is planning language, and 11.4 pins semantic cases (TL:1980). Embed the missing clauses only. |
| X-001 | V1: severity MEDIUM, "cursor branch is likely" | Withdrawn by V1 (DES:760 calls the cursor field UNVERIFIED); HIGH under the brief definition. |
| C-004 | V1: new file `OQ-6-style-execution-authorization.md` | Dropped by V1; the existing step-7.10 result file is the carrier (INV-018: it is not under `plans/` and no 7.20 glob counts it). |
| C-009 | V2: matrix recall finding R2-F3 | Withdrawn by V2; delivery exists in 8.12 and 10.5. |
| U-007 | V3: R3-F4, "three" Follow-Up entries | Withdrawn by V3 (TL:2999 was added by R-05, TL:2881); residual noted in Change 12. |
| C-007, C-008 | T1 F9 (run severity modules at 7.10), F10 (seven vs eight mentions) | Not defects (ADD:25, 27, 31; STYLE:25). |
| C-010 | T1 F8 (install follow-up) | ADD:39 excludes installation; informational. |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 1 to 12 | Low | A merged finding carries a wrong line, severity or fix | Re-run the merge from this plan; the variants and CONS are untouched |

## Review Status

Auto-approved after independent review (`refactor-plan-review.md`).
