# D-0024: Performance Benchmark Evidence

## Task: T04.04
## Status: PASS
## Validated: 2026-03-21 (Phase 4)

## SC-009 / NFR-001 Performance Threshold Validation

### Benchmark Configuration
- **Fixture**: 50-file Python package with realistic content (classes, registries, callables, services)
- **Iterations**: 10
- **Analyzer**: Full `run_wiring_analysis()` pipeline (G-001 + G-002 + G-003)
- **Config**: `WiringConfig(exclude_patterns=['__init__.py'], rollout_mode='shadow')`

### Results
```
Iterations: 10
p50:  0.0104s
p95:  0.0112s
Max:  0.0133s
```

### SC-009 Threshold
**p95 < 5s: PASS (0.0112s)**

The analyzer completes in ~11ms at p95, which is 446x faster than the 5s threshold.
This confirms AST-only analysis imposes negligible overhead on the sprint loop.

### Report Summary (last iteration)
```
Files analyzed: 50
Unwired callables: 0
Orphan modules: 0
Unwired registries: 10
Total findings: 10
```

### All Timings (seconds)
```
[0.0099, 0.0102, 0.0102, 0.0103, 0.0104, 0.0104, 0.0106, 0.0107, 0.0112, 0.0133]
```

### Environment
- Platform: Linux 6.8.0-106-generic
- Python: 3.12.3
- Analysis: Pure AST (no external tools)

### Acceptance Criteria Disposition

| Criterion | Status |
|---|---|
| Benchmark on 50-file package with p95 < 5s (SC-009) | PASS |
| Minimum 10 iterations for statistical validity | PASS (10 iterations) |
| Results include p50, p95, max timings | PASS |
| Report archived at D-0024/evidence.md | PASS |
