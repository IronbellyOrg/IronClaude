# Refactoring Plan

## Overview

- Base variant: Variant 3 (opus, refactorer), combined score 0.900
- Incorporated variants: Variant 1 (3 items), Variant 2 (1 item)
- Planned changes: 5 incorporations, 2 weakness fixes in the base; 3 changes considered and not made
- Overall risk: Low (all changes add or reconcile finding text; no finding is deleted)

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Reconcile the severity of the stale "default" clause | V1 F1, V2 F2, V3 F1 | V3 F1 | restructure | C-001 and X-001 were unresolved (votes: tie, V1, V3 and tie, V2, V1). The finding is unanimous. V3's own advocate conceded "a medium-high merge is fair" and V1's conceded blocking is defensible. The merge grades it Medium by the review rubric: a false sentence about the default, with nothing named that rests on it, and the STOP rule still fires. It stays a must-fix before execution | Low |
| 2 | Add the final-output test gap | V2 F1 | new finding after V3 F4 | append | C-004 unanimous for V2 (90 mean confidence); no assertion pins that the final output repeats the `Level:` line | Low |
| 3 | Use V1's narrower fix for the re-claim case | V1 F2 | V3 F4 fix | replace the fix text | C-003: V3 won 2 of 3 votes but V1's fix (print for `launched`, show the stored level for `already_launched`, pin one phrase) is the one the advocates called cleanest; keep V3's extension to failed worktree and failed launch | Low |
| 4 | Order of the two rules | V1 F3 | V3 F2 | merge fix text | C-002 unanimous for V3; V1 adds the test shape (compare the index of the two sentences) | Low |
| 5 | Add the `-k` filter note | V1 F4 | new note | append | C-007 unanimous for V1 | Low |
| 6 | Mark the severity of the single-source tension as drift risk | V3 concession | V3 F3 | reword | V3's own advocate conceded it is a no-test drift risk, not a direct contradiction | Low |
| 7 | Mark the cite-drift finding as a follow-up candidate | V3 F7, V2 advocate | V3 F7 | reword | C-009: two advocates say it is out of scope | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Why not |
|---|---|---|
| S-001 | V1 and V2 verdict PASS-WITH-GAPS | the merged verdict is derived from the merged findings (PASS-WITH-GAPS), not copied from any card; V3's FAIL rested on the one finding now graded Medium |
| C-006 | V1's coverage note on line 92 | V3 F5 already carries the same note |
| X-002 | V2's claim "all 16 covered" | the debate (unanimous for V3) showed two partly covered units; V2's claim is not carried into the merge |

## Risk Summary

All changes are text edits to a review card. Rollback: restore `reviewer-3-card.md` as the merge base.

## Review Status

Auto-approved (non-interactive).
