# Post-Lint Delta Check

**Source file:** `src/superclaude/agents/confidence-calibrator.md`

## Metrics

- **Post-lint line count:** 141 (unchanged from post-edit count — markdownlint applied no auto-fixes)
- **Fence count (`grep -c '^```'`):** 2 — exactly one open/close pair, fence integrity preserved
- **`## Claim-class handling` heading present (outside fence):** 1 match ✅
- **`## Stage-2 trace (REQUIRED)` heading present (inside fence):** 1 match ✅

## Stage-2 trace 7-row data presence verification

| Expected literal string | Match count | Status |
|-------------------------|-------------|--------|
| `arithmetic_mean(all_six)` | 2 (Stage-2 trace row + Formula applied bullet + Responsibilities #5 formula) | PASS — present |
| `gate_M1:` | 1 (Stage-2 trace row) | PASS — present |
| `gate_M2:` | 1 (Stage-2 trace row) | PASS — present |
| `gated_min` | 1 (Stage-2 trace row) | PASS — present |
| `verdict_cap` | 1 (Stage-2 trace row) | PASS — present |
| `**calibrated**` | 1 (Stage-2 trace bolded row label) | PASS — present, bold preserved |
| `spot_check_unverifiable` | 2 (Stage-2 trace row + Responsibilities #3a) | PASS — present |

All 7 Stage-2 trace data row markers found. Counts ≥ 1 for each. `**calibrated**` bold emphasis preserved.

## Verdict

**PASS** — markdownlint left the file untouched (no `--fix` modifications), all critical structural markers from Phase 2 remain in place, and Stage-2 trace rows are intact.
