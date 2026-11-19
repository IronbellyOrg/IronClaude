# Baseline measurements (plan Phase 1, spec step 0.8)

Measured at the start commit of this work (observer unchanged, `git diff --stat -- src/` empty), from the harness output in the package folder `artifacts/gates/p0/iter-1/`.

RB-22 threshold N: 18

The number is the longest run of consecutive spaces between two non-space characters inside a ledger row line of the `ledger` screen (`base` fixture) at 160 columns (37 row lines). The same measure at 116 columns is 48 and at 80 columns is 34, so RB-22 fails on the baseline for both (a wide blank band after the id column, finding M-17).

Height test (`tests/observe/test_height_budget.py`): all 18 cases pass on today's code, heights 24, 40 and 44 at widths 160, 116 and 80 with 3 and 20 questions. No failing height set exists, so none is excluded.

PNG route: FAIL (no browser installed); the scores below come from the text and ANSI tier (`png-route.md`).
