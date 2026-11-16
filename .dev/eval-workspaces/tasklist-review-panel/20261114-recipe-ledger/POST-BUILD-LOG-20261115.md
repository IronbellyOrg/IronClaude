# Recipe Ledger: what happened after the build (2026-11-15)

**Context for a reader who has seen nothing else.** Recipe Ledger (RL) is one of two redesigns of a "Review Panel" evaluation: cheap reviewer models (ember, luna) review a plan, and a blind judge scores them. RL asks each reviewer to run eight written recipes and to write a ledger of one row per recipe step. The build is described in `IMPLEMENTATION-REPORT.md` (written 2026-11-15 at 03:46 UTC, before the events below). The background, who is who and every open question for the human owner are in `../OPEN-DECISIONS-20261115.md`. The working agreement with the other redesign session (Sweep Sheet) is `../20261114-collab-process/PROCESS.md`. This file records only what changed or was measured since the build report. All times UTC.

## Verified results (from files in this folder)

| What | Result | Where |
|---|---|---|
| Fast tests | 511 passed, 1 skipped (the byte-for-byte recipe pin, skipped by the override), 59 deselected, 0 failed (28 s) | `uv run pytest tests -q -m "not slow and not freeze"` |
| Integration tests (fake claude) | 56 passed (rerun after the allowances were added, 129 s) | `-m slow` |
| `freeze` tests | review-record test passes (all 8 rows DONE); the two real-answer-file lint tests are NOT run (they need a person who may read the real ground truth) | `tests/test_lint.py`, `tests/test_lint_rl.py` |
| Recipe second-author review | Round 1: C1, C3, C6, C7 PASS; C2, C4, C5, C8 FAIL. Owner approved rewording; round 2 (fresh Sonnet session, copies of recipe files only, tool calls checked): all 8 PASS | `implement-report/recipe-review/`, `recipes/REVIEWS.md` |
| Recipe rewording | C2, C4, C5, C6, C8 reworded (recipe version 2), recorded as `override` in `recipes/recipes.json`; applied text kept in `implement-report/recipe-review/recipes-proposed-1.json` | owner order 2026-11-15 |
| Compliance spike, attempt 1 (strict check) | FAILED the gate: 2 of 14 reports without a valid ledger = 14.3% (limit 10%). One luna wrote no ledger; one put a Follow-up section between ledger and findings; one run was killed with no output (not counted). Ember row ids written `R-C4.1`, counted as "recipes not run" | `results/spikes/compliance-attempt1.*` |
| Compliance spike, attempt 2 (after the owner-approved allowances) | PASSED: 0 of 15 (limit 10%), 0 format errors, no recipes missing, quote validity 158 of 186 (84.9%), 10.8 to 13.2 rows per reviewer | `results/spikes/compliance-2.*` |
| Timing spike, attempt 1 | Stopped after 3 + 3 usable runs: a reviewer left `uv.lock` in the sandbox and the launcher refused the next run | `results/spikes/timing-attempt1.log` |
| Timing spike, attempt 2 (sandbox rebuilt between runs) | 5 RL runs, 4 control runs: `c_luna` = 2.278 s per ledger row; median 133.0 s (RL) vs 98.5 s (control) = x1.35; mean 13.4 rows. Written to `config/values.json` key `spike` | `results/spikes/timing-2.log` |

## Reading the timing numbers

The planning break-even was 2.07 s per row at b = 100 s and 14 rows; the measured 2.278 s is above it, so the design's row cap falls below 14 when the control's slowest reviewer takes about 100 s or less (cap 12 at b = 98.5). Attempt 1 gave 0.50 s per row and a ratio of 1.08, so the two attempts disagree widely: with 4 to 5 runs per arm the timing is not settled. The time rule for adoption (median at most 1.35 x the control) is met at the limit in attempt 2 and comfortably in attempt 1. A single document was used (the first study package), so this says nothing about other documents.

## Changes made since the build report (all owner-approved or owner-ordered)

1. **Recipe rewording** (above).
2. **Row-id prefix or suffix forgiven** (`R-C4.1`, `C4.1:`, `C4.1a`; at most 6 extra characters; `C4.1.1` and longer numbers are not forgiven; raw id kept as `item_raw`). Probe ids in findings follow the same rule. In `scaffold/ledgerv1.py` (`canon_item`).
3. **A heading between the ledger block and the findings block no longer makes the ledger missing** (flag `loose_layout`).
4. **Approved list of further allowances, built 2026-11-15 14:55**: heading `Ledger:` or `### Ledger:`; fence label in other case or with spaces (`Ledger-V1`, "``` ledger-v1"); a trailing comma or stray spaces on a ledger JSON line. All are recorded in a `forgiven` list per reviewer report. The findings block is parsed by the unchanged merge code and nothing is forgiven there in any arm.
5. **Strict reading reported next to the lenient one**: `analysis/analyze.py compliance` now prints "strict reading (nothing forgiven)" with the forgiven counts per kind, so a comparison per arm can be made both ways.
6. **`bin/run-spike.sh` rebuilds a dirty sandbox between runs.** It is safe only because the spike runs one panel at a time. The full schedule (`bin/run-schedule.sh`) runs several panels at once on one sandbox and does NOT have this fix: it needs one sandbox copy per run or a rule for `uv.lock`. Open (owner preference asked).
7. **Tests updated**: the heading-between tests now expect acceptance; the "no spike record in the real values file" test is skipped now that the real record exists; the word-count pin follows the reworded recipes.
8. **`tests/judge_support.py` added to the shared list** because the other session's new `test_briefs.py` imports it. The three shared files that had drifted (`bin/common.sh`, `tests/test_briefs.py`, `tests/test_paths.py`) were re-copied on 2026-11-15 13:3x and match the hashes the other session published; they stay provisional until its freeze tag.

## What did not happen

- No experiment arm, parity test or shared-control run (they wait for both freezes and the hold-out documents).
- No freeze: blocked on people tasks (second author for the other session's cards, ground-truth author, tests that read the real answer files).
- The 3 maintainer-only tests were not run.
- A mistake to know about: my first sandbox build wrote into `/tmp/evalsb-sweep/` (the other session's root name). The folder did not exist before; I removed my copy and rebuilt under `/tmp/evalsb-recipe/`. Nothing in the repository was affected.

## Update 2026-11-16 01:00 UTC: Sweep Sheet stopped

The other redesign (Sweep Sheet, session SS) was stopped by the owner in its own session. Its freeze gate (extractor recall of at least 0.8 on independently seeded plans) failed twice: 7 of 34 seeds located. Consequences for RL, as reported by SS (details: `../20261114-sweep-sheet/results/freeze-check-20261115-rerun.md`, not read by RL):
1. The shared pieces RL copied from SS (class cards, briefs, `bin/common.sh`, tests, the Z0 and K definitions; list in `config/shared-manifest.json`) are **copied provisional, SS stopped**: they will never be frozen by SS. RL keeps using them as they are; RL's own freeze tag will pin them.
2. The shared-control question is void as written: there is no second launcher to compare with. RL's Z0 arm (its own control, built and run in the timing spike) is the control for RL. Any other control arrangement is the owner's decision.
3. The parity test between the two launchers is void.
4. The PROCESS.md rules for slots, pushes and "no ground truth" still hold.
RL's own freeze is still blocked by people tasks (second author records for the cards RL copied, a ground-truth author, the tests that read the real answer files) and by the hold-out document list. Open questions are in `../OPEN-DECISIONS-20261115.md` (the owner is editing it; this section is not copied there).

## Stopped 2026-11-16 01:42 UTC (owner order: "stop recipe ledger too")

Recipe Ledger is stopped. State at the stop, verified on disk: no `claude`, spike, panel or schedule process running; both lock slots free; no scheduled jobs. The build, its tests (511 fast, 56 integration), the second-author recipe review, the compliance spike (attempt 2 passed, 0 of 15) and the timing spike are complete and were committed and pushed as ff5ddab48. Not done and not planned: the freeze, the maintainer-only tests, any experiment arm, any parity or control run, the sandbox-per-run fix for the full schedule. The recipe `override` entries, the strict-and-lenient reporting and the small allowances stay in the code as built. To restart: read `../OPEN-DECISIONS-20261115.md`, then `IMPLEMENTATION-REPORT.md` section 5.1 and this file; the people tasks listed above would be the first thing to settle.

## Where to go next

Open questions for the owner: `../OPEN-DECISIONS-20261115.md`. Requirements not met or partly met: `IMPLEMENTATION-REPORT.md` section 5.1.
