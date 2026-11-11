# runs/

- `baseline/` = unmodified master (`0c2b41f8`), `after/` = this branch; both made by `../run_suite.sh <label>`.
- `comparison.md` is the authoritative test-by-test comparison. It was built from the `test-ids.txt.gz` files
  (lines `STATUS tests/...::id` taken from the `-rA` summary of `test.log.gz`).
- `*-results.txt*`, `*-new.txt` and `*-regressions.txt` come from a first, unfiltered pass that also caught log noise
  (captured ERROR lines, skip reasons with temp-dir names). They are kept, but do not use them for counts.
- `before-fix/` = the new tests run on unmodified source; `after-fix/` = the same tests after the fix.
