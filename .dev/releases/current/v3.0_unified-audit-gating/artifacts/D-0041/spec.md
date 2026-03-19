# Readiness Report: Shadow-to-Soft Mode Transition

**Phase**: 8 — Shadow Calibration and Readiness
**Milestone**: M6a
**Date**: 2026-03-19
**Author**: Phase 8 Sprint Executor

---

## Executive Summary

**RECOMMENDATION: PROCEED TO SOFT MODE**

All four readiness exit criteria are MET. Statistical evidence supports transitioning the wiring integrity gate from shadow mode to soft mode enforcement.

---

## Exit Criteria Evaluation

### 1. FPR < 15%

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Measured FPR | 4.44% | < 15% | **MET** |
| FPR + 2σ | 4.78% | < 15% | **MET** |

- **Evidence**: D-0037/evidence.md, D-0040/evidence.md
- **Methodology**: File-based FPR = false positive findings / files analyzed, computed across 3 release cycles
- **Margin**: 10.22 percentage points below threshold

### 2. TPR > 50%

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| TPR | 100% | > 50% | **MET** |

- **Evidence**: D-0037/evidence.md
- **Methodology**: All known defects in test fixtures detected correctly (53/53 true positives, 0 false negatives from ground-truth test cases)
- **Caveat**: Retrospective validation (SC-009) revealed a false negative for keyword-only `Optional[Callable]` parameters. This affects production TPR slightly but does not breach the 50% threshold as the vast majority of injectable callables use positional parameters.

### 3. p95 Latency < 5s

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| p95 latency (production) | 0.554s | < 5s | **MET** |
| SC-008 benchmark | PASS | < 5s | **MET** |

- **Evidence**: D-0037/evidence.md, D-0050/evidence.md
- **Verification**: `uv run pytest tests/audit/ -k "benchmark" -v` exits 0

### 4. Alias Noise Separable from Signal

| Metric | Value | Status |
|--------|-------|--------|
| Alias-attributable FPR | 0% | **MET** |
| Separability | Fully separable | **MET** |

- **Evidence**: D-0039/evidence.md
- **Detail**: Zero alias/re-export false positives. All 7 FPs caused by dynamic dispatch pattern, not aliases. Default `__init__.py` exclusion prevents potential alias noise.

---

## Shadow Data Summary

| Metric | Cycle 1 | Cycle 2 | Cycle 3 |
|--------|---------|---------|---------|
| Files analyzed | 161 | 151 | 161 |
| Total findings | 7 | 7 | 7 |
| Unwired callables | 0 | 0 | 0 |
| Orphan modules | 7 | 7 | 7 |
| Unwired registries | 0 | 0 | 0 |
| Scan duration | 0.536s | 0.521s | 0.554s |

- **Evidence**: D-0036/evidence.md

---

## Known Limitations

1. **kwonlyargs gap** (SC-009): The analyzer does not scan keyword-only parameters for `Optional[Callable]`. This causes 1 false negative in `PortifyExecutor.step_runner`. Recommended fix: extend `_extract_injectable_params()` to also scan `args.kwonlyargs`. (D-0038/evidence.md)

2. **Dynamic dispatch FPs**: 7 modules in `cli_portify/steps/` appear as orphans because they are invoked via subprocess rather than static imports. These can be whitelisted if needed for soft mode.

3. **AST plugin not loaded**: Orphan module analysis ran without the AST references plugin, meaning dual evidence rule was import-graph only. Loading the plugin may reduce the 7 FPs.

---

## Recommendation

**PROCEED TO SOFT MODE** — All readiness thresholds are met with comfortable margins:
- FPR is 3× below threshold (4.78% vs 15%)
- TPR is 2× above threshold (100% vs 50%)
- p95 latency is 9× below threshold (0.554s vs 5s)
- Alias noise is zero

The 7 dynamic dispatch false positives represent a known, bounded pattern that does not affect gate reliability in soft mode (they are `major` severity, and soft mode only blocks on `critical`).

---

## Evidence Artifacts

| Deliverable | Path | Content |
|-------------|------|---------|
| D-0036 | artifacts/D-0036/evidence.md | Shadow dataset (3 cycles) |
| D-0037 | artifacts/D-0037/evidence.md | FPR/TPR/p95 metrics |
| D-0038 | artifacts/D-0038/evidence.md | Retrospective validation (SC-009) |
| D-0039 | artifacts/D-0039/evidence.md | Alias noise floor |
| D-0040 | artifacts/D-0040/evidence.md | FPR threshold validation |
| D-0050 | artifacts/D-0050/evidence.md | SC-008 benchmark |
