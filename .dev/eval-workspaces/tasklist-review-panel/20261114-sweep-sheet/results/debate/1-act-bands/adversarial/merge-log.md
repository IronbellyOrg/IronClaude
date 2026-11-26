# Merge log

Executor: the main session (`claude-sonnet-5-5`). Merged output: `DESIGN.md` section 15.1a and its pointers (the base text lives there once). No staging, commit or push.

## Metadata
- Changes planned 7, applied 7, failed 0, skipped 0.

## Changes applied
| # | File | What | Status |
|---|---|---|---|
| 1 | `DESIGN.md` 15.1 row 2 | numbers kept; registration widened to numbers, measure and consequence; pointer to 15.1a | applied |
| 2, 3, 4 | `DESIGN.md` new section 15.1a (after the 15.1 table) | registered text items 1 to 5 | applied |
| 5 | `DESIGN.md` 14.3 `stages.jsonl` row | clause that stage `act` differs from the band measure | applied |
| 6 | `DESIGN.md` 15.2 | two bullets added before the closing "No model was started" bullet | applied |
| 7 | `results/owner-decisions.md` | the "Still open" bullet for the act bands replaced | applied |

Deviation from the refactor plan: V2 and V3 wrote the text into the table cell. It was put in a short new subsection and the table row points to it, so the table stays readable and the text exists once.

## Post-merge validation
- Structure: `DESIGN.md` headings in order (15.1, 15.1a, 15.2); no heading level gap.
- References: `TESTING.md` 149, `MR` 357, 539, 662, `analysis/analyze.py` `stage_rows`, `WILSON_Z` (1.96, line 49) re-read this session.
- Contradictions: none introduced; the 15.2 bullet that calls every act band a planning value is unchanged and consistent.
- Tests: `uv run --frozen --project REPO pytest -p no:cacheprovider SW/tests -q -m 'not freeze'` -> exit 0, last line `749 passed, 4 deselected in 219.26s (0:03:39)`. No test was changed; none pins the 15.1 wording.
