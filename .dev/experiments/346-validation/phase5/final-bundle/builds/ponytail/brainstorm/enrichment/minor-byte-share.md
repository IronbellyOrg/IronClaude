# Byte share of fix edits that cite only minor findings (flg-r2)

Measured 2026-11-08 with `enrichment/minor_share.py` (`uv run --no-project python -I minor_share.py`), read-only on `exp346-ab-flg-r2/.dev/orca-command-refactor/specs/history/`.

Method: line-level `difflib.SequenceMatcher` between the saved copies; for each changed hunk, added characters are counted with a character-level diff; a hunk is `blocking-involved` if its new text cites any blocking id, `minor-only` if it cites only minor ids, else `untagged`. Ids and grades come from the run's own disposition tables (cycle 1: F1-F13 blocking, F14-F22 minor; cycle 2: N1-N6 blocking; N7-N11, C9, C12, C13, C14 minor).

| Cycle | Added chars | minor-only | blocking-involved | untagged |
|---|---|---|---|---|
| 1 (v1 -> v2) | 13,225 | 776 (6%) | 12,435 (94%) | 14 (0%) |
| 2 (v2 -> v3) | 6,301 | 1,726 (27%) | 4,575 (73%) | 0 |

Reading:
- Most minor fixes share a line with a blocking fix, so a whole-line (hunk) revert of minor-only hunks would remove about 2,500 of 19,500 added characters in this run: growth 32.1% would fall to about 27.8%, not to the 19% the equal-bytes estimate in `evidence-attribution.md` gives.
- Larger growth cuts need sentence-level revert or shrink rows inside mixed lines, which a script cannot derive from the diff alone; a model must write them as exact old/new text.
- One run only (flg-r1 uses bare numeric ids that cannot be matched in the text; the other runs were not measured). Treat as an indication, not a rate.

## Re-measure after verification (2026-11-08, cycle 2 of flg-r2 only)
The first count ignored cycle-1 ids (F1-F22) on changed lines. Two stricter rules, same method, run inline (not kept as a script):
| Rule | minor-only | protected | untagged |
|---|---|---|---|
| any foreign (cycle-1) id anywhere in the hunk's new text protects the hunk | 496 (8%) | 5,805 (92%) | 0 |
| only ids in the words cycle 2 added count (ids already in the baseline line are context, and a revert to the baseline restores that text unchanged) | 1,468 (23%) | 4,833 (77%) | 0 |
The second rule is close to the one SPEC.md adopts: reverting a hunk to the baseline cannot undo a cycle-1 fix that the baseline already contains. SPEC.md's final rule also ignores the document's own labels (for example `WC-5`), which this inline count treated as foreign ids; the independent re-count with the final rule gives 1,726 characters (27%, about 3.0 growth points), and other readings give 12.5% to 33% (`verification/spec-check.md`). SPEC.md uses 27%.
