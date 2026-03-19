# D-0039: Alias and Re-Export Noise Floor Characterization

**Task**: T08.04
**Status**: COMPLETE
**Date**: 2026-03-19

## R6 Risk Assessment: Alias/Re-Export False Positive Noise

### Codebase Alias/Re-Export Statistics
| Pattern | Count |
|---------|-------|
| `import X as Y` aliases | 5 |
| `__init__.py` re-exports | 89 |
| `__init__.py` files with re-exports | 8 |

### Impact on Findings

| Configuration | Files Analyzed | Total Findings | Delta |
|---------------|---------------|----------------|-------|
| With `__init__.py` included | 192 | 8 | +1 |
| With `__init__.py` excluded (default) | 161 | 7 | baseline |

The single additional finding when including `__init__.py` is `cli.cli_portify.steps.__init__` — the `__init__.py` file in the `steps/` provider directory, which is correctly flagged as having zero inbound imports (same dynamic dispatch pattern as the other step modules).

### Classification of False Positives by Cause

| Cause | FP Count | % of Total FP |
|-------|----------|---------------|
| Dynamic dispatch (subprocess-invoked steps) | 7 | 100% |
| `__init__.py` re-export aliases | 0 | 0% |
| `import X as Y` aliases | 0 | 0% |

### Separability Assessment

**Result: SEPARABLE** — The alias/re-export noise floor is **zero** in this codebase.

All 7 false positives are caused by the dynamic dispatch architecture in `cli_portify/steps/`, not by alias or re-export patterns. The default configuration already excludes `__init__.py` from analysis, which prevents the only potential alias-related finding.

**Evidence supporting separability:**
1. The 5 `import X as Y` aliases in the codebase do not produce any false positives — they rename imported symbols but don't affect orphan module detection
2. The 89 `__init__.py` re-exports are excluded by default (`__init__.py` is in `exclude_patterns`)
3. When `__init__.py` is included, only 1 additional finding appears, and it's a genuine orphan (same dynamic dispatch pattern), not an alias-caused FP

### R6 Mitigation Status

R6 predicted 30-70% FPR attributable to aliases. **Actual: 0%**. The alias noise is fully separable from genuine wiring defect signal because:
1. Default `exclude_patterns` already filters `__init__.py`
2. No `as` aliases create phantom orphan findings
3. All observed FPs come from a single architectural pattern (dynamic step dispatch) that is addressable via whitelist

### Recommendation
- **No blocking concern** for soft-mode activation from alias noise
- The 7 dynamic dispatch FPs can be addressed by adding `cli_portify/steps/` modules to the whitelist if needed
- No need to extend shadow period for alias characterization

## Acceptance Criteria
- [x] Report quantifies alias/re-export false positives as percentage of total (0%)
- [x] Separability assessment documented with evidence: "separable — zero alias-caused FPs"
- [x] Analysis covers both `__init__.py` re-exports and `import X as Y` aliases
- [x] If not separable → N/A (noise floor is zero, fully separable)
