# Reviewer-only measurement on spec E (2026-11-19)

Nine reviewers (sonnet), three per arm, briefs 1 to 3 of the E re-run. Cards are in control/, brainstorm/, troubleshoot/ next to this file. Scored by the main session reading the "What diverged" cell of each row; counts are not rechecked by a second reader.

| Test finding | control (current master) | brainstorm variant | troubleshoot variant |
|---|---|---|---|
| M-03 `csv2jsonl: ` prefix graded Blocking | 1 of 3 | 3 of 3 | 3 of 3 |
| M-02 "no output written" graded Blocking | 0 of 3 | 3 of 3 | 1 of 3 (r2 only) |
| Blocking rows in total (3 cards) | 5 | 10 | 12 (+1 Safety) |
| Thin test list (M-06) graded Blocking | 0 of 3 | 0 of 3 | 1 of 3 (r2) |
| Exit 0 on success graded Blocking on its own | 0 | 0 | 1 (r2 row 3) |

Troubleshoot reviewer 2 graded 7 of 10 rows Blocking, including the thin test list, the undefined row-number base and exit 0. Brainstorm reviewer 1 graded the output-open ordering Blocking (Missing); that is the same finding as M-02.

Limits: one spec, three reviewers per arm, same model, the brief carries the first-pass hints for every arm, the brainstorm variant names the two E findings as examples (it was tuned on this spec), and the merge step is not tested.
