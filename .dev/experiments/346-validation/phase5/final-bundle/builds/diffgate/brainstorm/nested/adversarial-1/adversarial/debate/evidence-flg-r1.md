# Orchestrator evidence note: flg-r1 composition (resolves shared assumption A-006)

Written by the brainstorm orchestrator, 2026-11-08, from read-only reads of `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r1/.dev/orca-command-refactor/review/` (the Arm B replicate with R3 proxy 6). This is data for Round 2, not an argument for any variant.

## Review 3 of flg-r1 (`spec-panel-round3.md` lines 141-150, verdict FAIL at line 222)

| ID | Severity | 427 grade | Origin (reviewer tag) |
|---|---|---|---|
| R3-1 | MAJOR | blocking | changed (SPEC3:67, 188) |
| R3-2 | MAJOR | blocking | changed (SPEC3:183, 189) |
| R3-3 | MAJOR | blocking | changed (SPEC3:88-90, 162) |
| R3-4 | MAJOR | blocking | changed (SPEC3:64, 102-128) |
| R3-5 | MINOR | minor | changed (SPEC3:67) |
| R3-6 | MINOR | minor | changed (SPEC3:112) |
| R3-7 | MAJOR (FR-8 GAP) | minor | changed (SPEC3:70, 107) |
| R3-8 | MAJOR (FR-9 blank) | minor | changed (SPEC3:64) |
| R3-9 | MINOR | minor | changed (SPEC3:183) |
| R3-10 | MINOR | minor | changed (SPEC3:93, 162) |

Proxy (CRITICAL+MAJOR labels) = 6; 427-blocking = 4. Every finding is `origin=changed`.

## Which fix wrote those lines (`disposition-round2.md`, 14 rows: 4 blocking, 8 minor, 2 citation; "Totals" line 32)

- R2-1 (blocking) changed SPEC3:64, 79, 82, 84-95, 88-89, 93, 102-128, 112, 115, 151, 162.
- R2-2 (blocking) changed SPEC3:67, 188, 198.
- R2-3 (blocking) changed SPEC3:182, 183, 189.
- R2-4 (blocking) changed SPEC3:53, 64, 151, 203, 204, 206, 208, 212-214.
- R2-7 (minor, MAJOR FR-8 graded minor) changed SPEC3:70, 107. R2-6 (minor) changed SPEC3:64. Others: R2-5 234, R2-8 62, R2-9 79, R2-10 202-204, R2-11 198, R2-12 62.

So: R3-1 sits on R2-2's fix; R3-2 on R2-3's fix; R3-3 on R2-1's fix; R3-4 on R2-1/R2-4's fix. Only R3-7 (proxy, not blocking) sits only on a minor fix (R2-7). R3-8 sits on line 64, touched by blocking and minor fixes alike.

## Where the review-2 blockers came from (`spec-panel-round2.md` lines 145-148; `disposition.md` rows 1-22)

- R2-1 origin changed (SPEC2:64, 79): round-1 finding 2 (CRITICAL, blocking) wrote SPEC2:64 and 79.
- R2-2 origin changed (SPEC2:67, 188): round-1 finding 8 (MAJOR, blocking) wrote SPEC2:67 and 188.
- R2-3 origin changed (SPEC2:183, 189): round-1 finding 9 (MAJOR, blocking) wrote SPEC2:182 and 189.
- R2-4 origin changed (SPEC2:64, 202): round-1 finding 6 (MAJOR, blocking) wrote SPEC2:202; line 64 was written by findings 1, 2, 17 and 21.
- Round 1 applied 21 of 22 rows (11 blocking, 10 minor; `disposition.md` line 39).

## Reading

In flg-r1 every blocker forms a chain through blocking fixes only: finding 8 -> R2-2 -> R3-1, finding 9 -> R2-3 -> R3-2, finding 2 -> R2-1 -> R3-3, findings 2/6 -> R2-1/R2-4 -> R3-4. A blocking-only fix gate (all three variants) would have removed R3-7 from the proxy (6 to 5) and none of the 4 blockers. Round 3 here shows about one new blocker per blocking fix (4 fixes, 4 new blockers). This is the "wrong lever" case of Variant B's falsification F1 and contradicts the flg-r2-based stories (F22 -> N5 -> N12) as a general mechanism. A-006 is therefore answered: the flg-r2 composition does NOT hold for flg-r1.
