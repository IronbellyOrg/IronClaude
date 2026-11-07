# Evidence validation of the merged card (round 2)

Validator: `evidence-validator` agent (id a488cf5d54c4e694d), read-only (Read, Grep, Glob). It could not write this file, so the orchestrating session (the reflect run) wrote it from the validator's reply. Target: `adversarial/merged-review-card.md`. Run at HEAD `0b443745`, with the plan edited in place after the review (see "Moved" below).

## Counts

| | Total | Verified | Moved | Unfounded |
|---|---|---|---|---|
| Findings table, rows 1-11 | 60 | 40 | 19 | 1 |
| Advisory 1-6 | 26 | 19 | 7 | 0 |
| Notes and not-checked | 29 | 24 | 5 | 0 |
| **Total** | **115** | **83** | **31** | **1** |

Each citation is counted once per place it appears in the card. `citations_dropped` = 1.

## Unfounded (1) and what was done

- Row 1, `post-fix-rechecks.md row 2`: the card defined this file as "one level up from the debate folder". That file lists revision 2 and did not exist when the review ran; its row 2 is the clean-tree finding, not "compares only changed command files; spec says every file". The claim is true in the round-1 file `.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105165021/post-fix-rechecks.md`, row 2, line 8 (re-read by the reflect run after the validator reported). The original citation is dropped from the card and replaced by the round-1 path, in row 1 and in the header definition (`merged-review-card.md` lines 9 and 17). The finding itself (row 1) is unchanged.

## Moved (31)

Every `plan:NN` citation after line 53 is shifted by +2, because revision 2 added the owner-instruction marker line after line 52 and the "Task order" bullet at line 54. Lines up to 53 are unchanged. Revision 3 (fix cycle 2) then changed the plan's line count only inside existing lines and the Task 24 acceptance list (one line added), so lines after Task 24's list moved by one more; the card is a review-time record and is not renumbered.

| Card line | Now at (after revision 2) |
|---|---|
| plan:58 / 61 / 64 / 65 | 60 / 63 / 66 / 67 |
| plan:227 | 229 |
| plan:405 | 407 |
| plan:447-467, 451, 465, 473, 495 | 449-469, 453, 467, 475, 497 |
| plan:541, 544 | 543, 546 |
| plan:552, 554, 556, 556-566 | 554, 556, 558, 558-568 |
| plan:580, 584 | 582, 586 |
| plan:54-58 | 56-60 |
| plan:73 | 75 |

Under many moved citations the claim was true when the review ran and revision 2 has since fixed it (rows 1, 2, 3, 5, 7, 11, advisories 2 to 5, the C-013 note). Treat those rows as resolved, not as open defects.

## Verified with caveats

- C-009 note: spec lines 321-322 are AC-1.5 and AC-1.6. Only line 322 supports "expects a written contract"; line 321 says "no file written", so it is the contrast.
- Row 9: spec 7.2 step 1 (line 283) backs the section check; it does not mention the gate line at plan:36.
- C-010 note: the seven uncovered spans match the coverage-matrix citations. The matrix also has no row for `source.md:3` or `:12`, so "seven" undercounts. Not a citation error.
- Row 4: the plan cites `APPROVED.md` only at plan:31 (H1), never G1.

## Not checked

The validator had no Bash. Five command results were passed through as attributed, not independently verified: `cmp` rc=2 for `README.md` and `__init__.py`, 325 tracked `return-contract.yaml` paths, the `pgrep` wrapper match, the clean tree at `0b443745`, and the plan file being tracked. Each is quoted in `adversarial/invariant-probe.md` or the round 2 rebuttals.
