| Status | Result |
|---|---|
| DONE | Wrote `DESIGN.md` (822 lines), `TESTING.md` (292) and `IMPLEMENTATION.md` (194) in `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/`. |
| DONE | Mapped every requirement in sections 6.1, 6.3 and 6.5 to 6.8 to a runnable test or a labelled manual check. A script check found no requirement missing. |
| DONE | Checked that nothing outside that folder changed and nothing is staged. |
| NEXT | Make the owner decisions below, then run the three no-model checks in `IMPLEMENTATION.md` section 1. |

**WHAT:** The design is complete, but it is untested. Nothing was built, run or measured, no model was started, and I opened no `ground-truth*.json`. I did read `COMBO-REPORT.md`, which prints ground-truth legends, and the first 44 lines of one study plan. I used nothing from either; every example is invented. The design also plans a lint to enforce this.

**Where the design departs from `merged-requirements.md`** (15 rows, listed in `DESIGN.md` section 1.3):
- **`quote_other` check:** the spec allows only the source or a printed tool line. That would demote every true row where a plan contradicts itself. I widened it to also accept the plan and the reviewer's own tool results.
- **Blocking rule:** I applied it to findings linked to sheet items only, so SS stays comparable to Z0.
- **Item quota:** I reconciled the spec's two conflicting quota rules with a fair-share ceiling.
- **Retries:** counted runs use one attempt and no model fallback, to match the zero-findings rule.
- **Brief edits:** the CB edits stay in the study folder; I did not touch the production brief file.

**Not verified:**
- The 8 s pre-pass figure is a planning value. The git-grep cost on a full-size tree has never been measured, and it is the biggest unknown.
- `merged-requirements.md` says the merge accepts the extra `class`, `probe` and `src` keys. I read that in the code but have not tested it.
- No independent reviewer read these files, because you allowed no models. The checks I ran were mechanical only.
- My arithmetic reproduces the spec's time figures (for example, +29.0% at b = 100, tightest cell 131 s against a 135 s cap), but these remain planning values.

**RECOMMENDED ACTION:** Run `IMPLEMENTATION.md` section 1, which has three checks and needs no model: the existing review tests, the search-cost measurement on the real repository, and the merge-keys probe. If the search takes more than 4 s, the time table changes before any code is written. Then decide the owner items in `DESIGN.md` section 15.1: the G0 floor (I recommend 0.45), the per-class act bands, whether to reword CB-2 (it mentions a ledger that Z0 does not have), and approval of the K-arm lead-in. Those are needed at the freeze, not before the build.
