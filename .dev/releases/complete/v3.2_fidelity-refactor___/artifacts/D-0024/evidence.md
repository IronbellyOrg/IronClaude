# D-0024: Performance Benchmark Evidence

## Task: T04.04
## SC-009 / NFR-001 Performance Threshold Validation

### Benchmark Configuration
- **Fixture**: 50-file Python package with realistic content (classes, registries, callables)
- **Iterations**: 15
- **Analyzer**: Full `run_wiring_analysis()` pipeline (G-001 + G-002 + G-003)
- **Config**: `WiringConfig(exclude_patterns=['__init__.py'], rollout_mode='shadow')`

### Results
```
Iterations: 15
Mean: 0.0627s
p50:  0.0625s
p95:  0.0681s
Max:  0.0681s
```

### SC-009 Threshold
**p95 < 5s: PASS (0.0681s)**

The analyzer completes in ~68ms at p95, which is 73x faster than the 5s threshold.
This confirms AST-only analysis imposes negligible overhead on the sprint loop.

### Report Summary (last iteration)
```
Files analyzed: 50
Unwired callables: 0
Orphan modules: 0
Unwired registries: 0
Total findings: 0
```

### All Timings (seconds)
```
[0.0620, 0.0594, 0.0628, 0.0633, 0.0613, 0.0593, 0.0642, 0.0602,
 0.0644, 0.0625, 0.0673, 0.0639, 0.0613, 0.0607, 0.0681]
```

### Environment
- Platform: Linux 6.8.0-106-generic
- Python: 3.12.3
- Analysis: Pure AST (no external tools)
