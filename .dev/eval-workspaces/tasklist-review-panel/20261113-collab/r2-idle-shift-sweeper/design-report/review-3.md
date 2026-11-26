# Review 3 of DESIGN.md (Redesign 2, Idle-Shift Sweeper): re-check of N-1, N-2 and B-4's test

Reviewer: independent (did not write the design). Date: 2026-11-14.
Document: `R2/DESIGN.md` (750 lines; read this run: lines 137-356 and 496-685, plus greps of the whole file). Prior review: `design-report/review-2.md` lines 1-50.
Scope: (1) is N-1 fixed; (2) is N-2 fixed and does B-4 now have a shared-cap test; (3) did the last edits add a new blocking defect.
Grading: blocking = wrong behaviour, false claim, missing required deliverable, security or data-loss risk; anything else is a note.

## Prior findings

- N-1 fixed. 5.1 step 0 (line 509): "A package directory without `DONE` is moved to `runs/<row>/<pkg>.incomplete-<UTC>` (quarantine in place, never deleted), and so are its sandbox `SBR/sb/<runid>/<pkg>` and its board `SBR/board/<runid>/<pkg>` ... re-run on a freshly built sandbox and an empty board, so no old seal, delivery, call counter or fact carries over." New 6.2 row "Resume of an unfinished package" (line 637): kill while package 2 runs after a delivery, resume, assert old run dir, sandbox and board moved to `*.incomplete-<UTC>` and "call counters at 0, no seal, no delivered list and an empty board". Because the sandbox path no longer exists, the `git init; git add -A; git commit -qm snap` of 2.1 (line 156) runs on a fresh directory, so the "nothing to commit" failure is gone too. The existing row "Resume after interruption" (line 636) still covers the merge-to-judge case.
- N-2 fixed. The "hv cap" wording is gone (grep for `hv cap` returns nothing). `test_harvest_hook.py` (line 599) now has: "the shared 2k cap holds across both writers: with k = 1, one `panel-post` fact plus one harvested fact fill the cap and a third post of either kind is rejected `over_cap`". With two separate counters each would be at 1 of 2 and the third post would be accepted, so this test fails the B-4 defect.
- B-4 test present. Rule 11 (line 244) "the sweeper's posts and the harvested facts together (`from` in `{sw-1, hv-1}`) are at most 2k per package, counted under the board lock" and harvest step 6 (line 292) "under the shared 2k cap" agree with the new test. The single-source cases (line 596 "the 2k+1-th sweeper post (`over_cap`)", line 622 "fake sweeper posts 3k facts") remain and are consistent with a shared cap.

## New blocking findings

None. The new step 0 text and the two 6.2 rows do not contradict 2.1, 2.3, 2.5.1, step 1 ("On a first launch only", line 510) or step 4 ("created once per row in step 1", line 523). Reusing the same `runid` on the re-run keeps `deal_r` (2.5.2, line 324) and the anonymiser's `<runid>` self-check (line 538) consistent. The quarantined board stays under `SBR/board/`, so the reviewer audit pattern `SBR/board/*` (line 393) still covers it.

## Notes (minor)

- n-1 (carried from review 2, not fixed): 2.8 row "Independent first pass" (line 387) still cites "receiver hook step 6" for the seal; the seal is step 9 (line 319).
- n-2: step 0 (line 509) says "`test_preflight.py` covers a resume after an interruption between merge and judge", but the 6.1 `test_preflight.py` row (line 612) does not list that case; it is listed only as 6.2 row line 636. Since AC-1 (line 674) checks "every test in 6.1 and 6.2", name the case in one place consistently.
- n-3: "a third post of either kind" (line 599) reads as one test; to pin both directions, run it twice (third post from `sw-1`, third post from `hv-1`).
- n-4 (outside the last edits): line 117 does not say whether `run-package.sh` writes `DONE` when it exits 1 with `INVALID`. If it does, a resume skips an INVALID package, which is consistent with step 2 but conflicts with line 262's "re-run under the study's quarantine-in-place convention" unless that re-run is a new row. One sentence would settle it.

## Verdict

verdict: PASS

N-1 fixed, N-2 fixed, and B-4 now has a test of the shared cap across sweeper and harvested posts. 0 new blocking findings, 4 notes.

What I checked: DESIGN.md 5.1 step 0 and steps 1-4 (lines 498-529), 6.1 (lines 592-612), 6.2 (lines 614-642), 6.5 (lines 670-685), 2.1-2.5 (lines 137-356), the line 117/120/122 interface rows, the 2.8 audit rows (lines 387, 393) and Appendix A R-18 (line 732); and a grep of the whole document for `hv cap`, `2k cap`, `over_cap`, `incomplete`, `resum`, `quarantin` and `runid`. I did not re-read the rest of the document or any source script.
