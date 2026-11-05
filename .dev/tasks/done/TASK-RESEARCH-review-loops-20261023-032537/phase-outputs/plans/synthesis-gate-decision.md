# QA Report: Phase 5 Synthesis Gate Decision

**Topic:** Assembly readiness of the six synthesis components and five hypothesis cards
**Date:** 2026-10-24
**Status:** USER-AUTHORIZED ADVANCE after cycle 2 fixes, without cycle-2 verification (not a verified PASS); see the dated record at the end
**Record framing:** The cycle-1 FAIL/HALT below is dated history and remains valid; it is not rewritten.
**Phase:** Phase 5 synthesis gate, Step 5.27
**Fix cycle:** 1 of 2 used; halted by the regression guard before monotonicity and cap handling
**Governing template:** Task Standard QA Report Output Format; Step 5.27 ordered guards

## Overall Verdict
**FAIL and HALT at cycle 1.** Cycle 0: ten reviewers, all FAIL, 33 consolidated groups (11 IMPORTANT, 22 MINOR). Cycle 1: one fixer, 102 patches applied byte-exactly. Both fresh verifiers FAIL. The structural verifier found one frozen cycle-0 PASS identity now failing, which the parent confirmed on disk. The regression guard therefore halts, regardless of the large failure-count shrink.

## Items Reviewed
- Cycle-0 baseline: `qa/qa-consolidated-findings-phase5.md` (33 groups; frozen PASS identities per report).
- Correction and application: `qa/qa-synthesis-fix-log.md` with its Parent Application Record (all 11 start and end hashes matched).
- Structural verification: `qa/qa-synthesis-verification-structural.md`, FAIL: 1 regression (R1), 1 unresolved (P5-18 remainder), 8 new MINOR findings S25-N1..N8; 69 of 70 protected PASS identities hold.
- Content verification: `qa/qa-synthesis-verification-content.md`, FAIL: 0 regressions, 1 unresolved (U-1, P5-18 remainder, MINOR), 3 new IMPORTANT contradictions N-1..N-3 (overlapping S25-N4, S25-N5 and S25-N3).
- Parent check of R1: `qa/qa-synthesis-content-2.md` row 10 ("Content rules ... tables over prose") was PASS at cycle 0. `synthesis/synth-04-options-recommendation.md` §7.7 "Excluded with rationale" paragraph, added at Step 5.24 for P5-18, now lists six controls with anchors, placements and reasons as one prose paragraph, against `tech-research/SKILL.md:1598` "Tables over prose whenever presenting multi-item data". The consolidation treated the same pattern as a defect (P5-15). Confirmed.

## Cycle History and Ordered Guards
| Stage | Evidence | Failure groups | Outcome |
|---|---|---|---|
| Cycle 0 | 10 reviews, all FAIL | 33 | FAIL |
| Cycle 1 application | 102 hash-guarded patches | not closed by application | applied |
| Cycle 1 verification | structural FAIL, content FAIL | about 9 after merging overlaps | FAIL; regression halt |

**Guard 1, regression: TRIGGERED.**

```text
Regression detected on Item content-2.10 — previously PASS at cycle 0, now FAIL. Halt overrides monotonicity check.
```

The item is Items Reviewed row 10 of `qa/qa-synthesis-content-2.md`. The regression is a presentation defect introduced by the cycle-1 fix itself (prose instead of a table), not a change to any causal finding.

**Guard 2, monotonicity: NOT used to proceed.** The set shrank from 33 to about 9, but shrink cannot override the triggered first guard.

**Guard 3, cap: NOT a waiver.** One more cycle exists under the cap, but it is not automatic after a regression halt.

**Guard 4, advancement: DENIED.** Assembly (Phase 6) does not start.

## Issues Found
Current open set after merging the two verifiers' overlaps (all wording, citation or presentation; none changes a rank, the displayed order V1 > V3 > V2 > V5 > V4, a card's causal meaning or a historical classification):
- R1 / S25-N2: synth-04 §7.7 control placements written as prose; convert to a table.
- P5-18 remainder (U-1): Options B and E and synth-05 Phase 3 cite the Session 10, Session 17 Task 8 and Session 17 FINAL controls without the deck's stated limits.
- N-1 / S25-N4: synth-06 says unmarked rows are unchanged historical rows, but three rows were corrected in place at Step 5.24.
- N-2 / S25-N5: synth-04 §7.8 reading-limits table contradicts reads used by the Step 5.24 fixes.
- N-3 / S25-N3: synth-05 still says "five" checks and lists an unlisted input; the order-4 row sits inside Phase 2 despite having no existing input.
- S25-N1: synth-01 "parent 1932" lacks its deck:350 citation.
- S25-N6: synth-04 provenance block says header lines were moved unchanged, but one Status sentence was split.
- S25-N7: cards' 10.5 records state pre-fix body hashes; no amendment receipt for the chapter-1 note.
- S25-N8: fix-log per-file patch counts sum to 107, not 102 (process record only).

## Recommendations
User decision required before any further correction. Recommended: authorize the second (final) correction cycle, narrowly limited to the open set above, by one fixer, followed by two fresh verifiers that re-check every frozen PASS identity again. No waiver of the failed check and no change to ranks, order, cards' causal text, variants or debate artifacts.

## QA Complete
**VERDICT: FAIL. HALT: previously-PASS-to-current-FAIL guard.** Task Blocked pending an explicit user decision. Phase 6 not started.


## User-Authorized Cycle 2 and Advancement Record (2026-10-24)

| Item | Record |
|---|---|
| Authorization | User, 2026-10-24T03:41Z: "I authorize the fixes but not the verifiers.. once fixes are in you are authorized to move on". Clarified 03:45Z: keep the separate Phase 5 review only "if valuable"; the parent judged it duplicative of Phase 6 and did not run it. |
| Cycle 2 correction | One rf-qa fixer covered all nine open groups: 19 literal patches across synth-01, synth-04, synth-05, synth-06 and the five cards' amendment receipts, plus a recorded count correction for the cycle-1 log. Log: `qa/qa-synthesis-fix-log-cycle2.md`. |
| Application | All 9 start and end SHA-256 values matched; card originals preserved exactly once; the regression item (synth-04 section 7.7) is now a six-row table with the "advocates did not weigh" sentence kept. |
| Verification | Not run, by user decision. Whether the nine groups are resolved, and whether cycle 2 caused any new regression, is unverified at this gate. |
| Gate state | Not a PASS. Advancement to Phase 6 is authorized by the user, and Phase 6's final-report lenses, source-fidelity and anti-omission gates review the assembled content. |
| Unchanged | Ranks, the non-consensus displayed order V1 > V3 > V2 > V5 > V4, card causal text, immutable variants, debate artifacts and historical classifications. |
