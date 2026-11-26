| Status | Result |
|---|---|
| DONE | All 106 tests pass (`ruff check` clean, was 13 findings). Ledger `.dev/implement/collab-r4-flag-and-adjudicate/progress.md` is complete: one task, verdict compliant. |
| DONE | The one-package smoke test (EL2 on the control package) passes every condition for both the collaboration row and the isolated row. |
| DONE | `IMPLEMENTATION.md` is rewritten against the files on disk. It holds the file list, the six run commands, test counts, spike and smoke results, and every unmet requirement. |
| NEXT | You decide whether to run F7 at all, because luna's act rate is 0 of 5 (below). |
| NEXT | Run the full panels and the missing design measurement runs yourself. |

**A bug in my own build, found and fixed.** The first smoke row showed `r4-hook` delivering one card twice and blocking later cards falsely when a reviewer makes parallel tool calls. I fixed it with a per-reviewer lock and added a test that failed before the fix. Rows `smoke-f7-el2-1` and `-2` stay on disk as invalid evidence. Row `-1` died with the first session.

**Not met or not run:**
- **Luna act rate:** 0 of 5 on the design's unannounced-instruction probe. The design says the F7 arm then shouldn't run. In the smoke, luna did settle announced cards (2 passed lines, 2 conversions).
- **Spike 4 and its values files:** not run, because full panel runs are yours. So AC-11 is only partly met and AC-12 is not met.
- **SL2 and HL2 smoke:** not run. The HL2 F7 command is refused at planning values, as the design says.
- **Spike S2 on haiku:** a strict fail. It repeated `ALPHA` but not `BETA`.
- **Hook speed:** p95 is 143 ms and 90 ms on the lunas, above the roughly 0.1 s per call the design budgets.

**Two things to know:**
- **`lib/` is git-ignored** (`.gitignore:13`), so a plain `git add` skips the six Python modules and `card.jq`. Committing needs `git add -f R4/lib`.
- **I skipped the protocol's revert step.** An independent review found five blocking defects in `IMPLEMENTATION.md`. The ledger's retry ladder would then have reverted files, which your "do not delete anything" forbids. I fixed them in place and ran one more review, which found none. The ledger records this in `retries/T1/repair-2-1.md`.

RUNS: all of the above. NOT BUILT: Spike 4 values files, full-row evidence for AC-12, SL2 smoke. Nothing was staged, committed or pushed. Writes were limited to the `r4-flag-and-adjudicate` folder, `.dev/implement/collab-r4-flag-and-adjudicate/` and `/tmp`.

**RECOMMENDED ACTION:** decide on the luna act-rate gate first, because it decides whether the F7 runs are worth their cost. If you proceed, use the exact commands in section 3 of `R4/IMPLEMENTATION.md`.
