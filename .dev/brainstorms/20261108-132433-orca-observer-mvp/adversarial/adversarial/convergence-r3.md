# Convergence After Round 3 (final check)

## Method

- Same rule as `convergence-r2.md` (Method): a point is AGREED when all 3 advocates, or at least 2 of 3, back the same superior approach; the majority choice wins; with no majority the point is UNRESOLVED. Score = agreed points / 57, to 2 decimals. Threshold for this brainstorm: 0.75. Round 3 ran because the invariant probe found one HIGH finding (INV-019) that the Round 2 consensus did not address.
- A strict score (3/3 only) is also given, because Round 3 reopened points and a majority score alone hides that.
- Inputs read: `debate-r3-variant-1.md` (Signal Bridge, opus:architect) Final Position, INV-019 response, Per-Point Final Positions (lines 88-101, which list only the points V1 changes; unlisted points keep V1's Round 2 stance); `debate-r3-variant-2.md` (Attention Ledger, opus:analyzer) the same sections (Per-Point lines 93-107, same convention); `debate-r3-variant-3.md` (Decision Desk, haiku:backend) Final Position, INV-019 response, MEDIUM table, Remaining Disagreements, Final Concessions and the full 57-row Per-Point table (lines 73-135).
- A "no" in a Round 3 per-point table means the advocate changes or adds to the Round 2 consensus. When all three make the same change (for example restoring the human selection gate), the point is AGREED on the changed approach.
- V3 wrote last and saw V1 and V2's Round 3 files; V1 and V2 did not see V3's Round 3 file. Where V3 adds a refinement the others could not answer, it is counted as agreed only when it is stricter than, and compatible with, the majority approach (S-008 acquisition rule); otherwise it is a dissent.

## Per-Point Final Positions

Only points whose Round 3 status differs from a plain 3/3 carry-over of Round 2 are listed. The other 44 points are 3/3 agreed, unchanged from `convergence-r2.md` lines 15-71 (V3's table marks each `yes`; V1 and V2 leave them unlisted).

| Point | V1 (Signal Bridge) | V2 (Attention Ledger) | V3 (Decision Desk) | Agreement | Winner approach |
|---|---|---|---|---|---|
| S-007 gate table | Add DIRECTION-SELECTED gate after R0; "production integration" = registering `superclaude observe` or any live Orca subprocess outside the fake runner (UNVERIFIED reading) | Accepts V1 gate and reading | Accepts gate; proposes boundary = first wiring into the shipped product, live read-only capture as research; stricter reading applies until the owner confirms | 3/3 on the gate; 2/3 on the boundary reading | R0, then DIRECTION-SELECTED, then R1; boundary is an owner decision, offline-only until confirmed |
| S-008 owner list | Restore visual direction as owner decision 1 | Owner-list rule: human-only, issue-assigned, or departs from issue preference; restores stack confirmation | Accepts both; adds acquisition permission before the call | 3/3 | V2 rule plus V1 item 1; V3 acquisition rule adopted as a compatible refinement |
| S-006 acceptance | Reviewer-checked selection-record AC | Accepts | Accepts | 3/3 | Selection record (date, option, who) checked by a reviewer, never reported as an automated test |
| C-001 default screen | Status: owner selects; recommends B after QUESTION-OBSERVATION | Same | Owner selects; recommends C as the post-link composition | 3/3 that the owner selects; 2/3 on the recommendation | Recommend A for R1, B after QUESTION-OBSERVATION, C behind QUESTION-LINK; V3 dissent recorded |
| C-002 / X-007 verb and budget | `check --all --run` reworded to a candidate verb | Same | Same; default at most one message call per cycle under the five-call cap | 3/3 on the wording; 2/3 on the budget (open parameter) | Candidate verb behind QUESTION-OBSERVATION; per-cycle message calls set by measurement |
| C-006 / C-011 deadline | Accepts 15 s budget | Restores the threshold the consensus dropped: 15 s cycle, STALE after 3 intervals | Accepts 15 s, STALE after 45 s monotonic | 3/3 | 15 s cycle, at most 5 subprocesses, STALE after 3 intervals (45 s) |
| C-008 / A-003 `page.total` | Required field | Optional, "reported unknown" | Optional | 2/3 | Optional; V1 dissent recorded |
| C-010 overflow | Closes the parameter | Closes the parameter | `unknown (retention exceeded)` plus retained count | 3/3 | V3 notation |
| C-017 export | One view model, two renderers | Same | Accepts (Final Concession 5) | 3/3 | Screen renderer bounded by width; record export lossless for permitted values |
| A-001 side-effect observables | Before/after unread IDs and lease fields | Adds quiet-scope repetition | QUALIFY: those observables are UNVERIFIED until samples establish them | 3/3 on QUALIFY | Quiet-scope test that first establishes readable identity fields |
| A-008 label | QUALIFY | QUALIFY | REJECT | 2/3 | Label only; caps are per process and disclosed; no singleton |

## Invariant Gate Re-Check

- INV-019 (HIGH, human visual-direction selection dropped): **resolved in the design** by all three advocates. The merge must carry (a) visual direction as owner decision 1, (b) the DIRECTION-SELECTED gate between R0 and R1 with missing, stale and contradictory rules, and (c) the reviewer-checked selection-record AC (refactor-plan Changes 22, 23, 31, 32). This resolves the design defect only; no owner selection exists, so the gate itself has not passed.
- INV-020 (HIGH, `check --all --run` presented as settled): **resolved** by rewording it to a candidate verb with three UNVERIFIED proofs (refactor-plan Change 24). All three advocates accept.
- MEDIUM findings (16, of which 14 were UNADDRESSED after Round 2): each of the 14 has a response in V1, V2 and V3 Round 3 (V1 and V2: fixes for 13, INV-007 accepted as a disclosed risk; V3 table lines 30-47); none is disputed as a defect. They are warnings carried into the merge through refactor-plan Changes 12-32, not blockers.
- LOW findings: carried as notes (V3 Final Concession 7; V1 line 60).
- Unaddressed HIGH invariants after Round 3: none.

## Summary

- Agreed (majority rule): 57 / 57; score **1.00**. Of these, 50 are 3/3 and 7 are 2/3 (S-007 boundary reading, C-001 recommendation, C-002 and X-007 budget, C-008 and A-003 `page.total`, A-008 label).
- Strict score (3/3 only): 50 / 57 = **0.88**.
- Threshold 0.75: **met** under both counts. No force-select needed.
- The 2/3 points are recorded as dissents or open parameters, not settled facts. Two of them belong to the owner (the post-link default and the production-integration boundary); the budget waits on measurement; `page.total` and the A-008 label are merge choices.

## Changes to the Round 2 Consensus

1. The owner selects the visual direction; the debate only recommends. The Round 2 statement that B "is the default" after the question-row gate becomes a recommendation pending the owner (C-001, S-008).
2. New DIRECTION-SELECTED gate between R0 and R1, with a dated owner record, renders of A, B and C at 160, 116 and 80 columns marked "synthetic fixture, not live evidence", realistically degraded versions beside them, and C's find-and-inspect walkthrough task (S-007).
3. "Production integration" is defined for the gate, with two UNVERIFIED readings; the stricter one applies until the owner confirms (S-007).
4. Owner-list rule restores visual direction, stack confirmation (Rich departs from the issue's Go preference), capture permission, exposure policy, question-type choices, command name and any multi-observer restriction (S-008).
5. `check --all --run` is a candidate verb, never an available one; the question area stays "bounded best effort; coverage unknown" even after admission; V2's "real bound" rate argument is withdrawn (C-002, X-007, C-014).
6. Collection bounds restored: 15 s cycle, at most 5 subprocesses, STALE after 3 intervals, the 30 s deadline withdrawn (C-006, C-011).
7. Export and screen get separate renderers over one view model (C-017).
8. Acquisition permission is checked before a message call, separately from display and export permission (S-008, INV-017).
9. Overflow notation settled: `unknown (retention exceeded)` (C-010).
