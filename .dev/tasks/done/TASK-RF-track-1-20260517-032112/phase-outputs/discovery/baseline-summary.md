# Baseline Summary (pre-fix)

**Captured:** 2026-05-17 03:48
**Branch:** fix/ci-rot-pr1-ruff-autofix
**Ruff version:** 0.15.13

## Whole-tree (all rule classes)

Total: **1037 errors** (research-notes baseline: 1036; +1 drift = +0.1%, within ±5% tolerance)

| Count | Rule  | Description                              |
|-------|-------|------------------------------------------|
| 645   | F401  | unused-import                            |
| 243   | I001  | unsorted-imports                         |
| 46    | F841  | unused-variable                          |
| 36    | E402  | module-import-not-at-top-of-file         |
| 20    | N806  | non-lowercase-variable-in-function       |
| 18    | F541  | f-string-missing-placeholders            |
| 11    | E741  | ambiguous-variable-name                  |
| 8     | F821  | undefined-name                           |
| 3     | E731  | lambda-assignment                        |
| 3     | N811  | constant-imported-as-non-constant        |
| 2     | F811  | redefined-while-unused                   |
| 1     | (n/a) | invalid-syntax                           |
| 1     | E401  | multiple-imports-on-one-line             |

[*] 899 fixable with `--fix`; 48 hidden fixes available with `--unsafe-fixes`.

## Targeted (this PR's scope: F401 + I001 + F841)

Total: **935 errors** in targeted scope (vs research-notes 934 = +1 drift = +0.1%)

| Count | Rule           | Auto-fixable |
|-------|----------------|--------------|
| 645   | F401           | yes          |
| 243   | I001           | yes          |
| 46    | F841           | yes          |
| 1     | invalid-syntax | no (file unparseable; will be reported separately) |

Drift vs research-notes (1036→1037 / 934→935): trivial — within ±5% tolerance, no action required. Proceed with autofix. Diff is +1 F401 + 1 I001 (-1 each) — likely from a recent commit between research and execution.

## Note on `invalid-syntax`

Ruff reports 1 file with a syntax error. This file cannot be auto-fixed because ruff can't parse it. The autofix will skip it; the post-fix verification (Step 3.1) will explicitly report this 1 unfixable error. If it's a real syntax bug, it's pre-existing and out of scope for this mechanical-bulk-fix PR; document it as a follow-up.

## Expected post-fix state (success criterion for Step 3.1)

After `ruff check --fix --select F401,I001,F841` runs successfully:
- F401: 0 (or N residual if ruff can't auto-fix some — e.g., F401 inside `__all__`-export modules)
- I001: 0
- F841: 0 (or N residual if ruff can't auto-fix some — e.g., F841 with side-effect calls)
- Total cleared: 934/935 = 99.9% (target rule classes)
- Remaining whole-tree errors: ~102 (E402 + N806 + F541 + E741 + F821 + E731 + N811 + F811 + invalid-syntax + E401) — out of scope for PR1, routed to PR2-PR5.
