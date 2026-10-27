# D-0041: Pipeline Integration — Step 8 End-to-End (FR-7)

## Wiring Implemented

### Convergence Mode Activation
When `config.convergence_enabled=True`:
1. Step "spec-fidelity" has `gate=None` (line 709 in executor.py)
2. `roadmap_run_step()` detects convergence mode and delegates to `_run_convergence_spec_fidelity()`

### Step 8 Call Chain
```
roadmap_run_step("spec-fidelity", config)
  → _run_convergence_spec_fidelity()
    → execute_fidelity_with_convergence()
      → run_checkers (structural_checkers.run_all_checkers + semantic_layer.run_semantic_layer)
      → convergence evaluation (pass if active_highs == 0)
      → run_remediation (remediate_executor.execute_remediation)
      → repeat up to 3 runs
    → _write_convergence_report() to spec-fidelity.md
```

### Steps 1-7 Unaffected
- Steps 1-7 (extract through anti-instinct) are unaffected by `convergence_enabled=true`
- They execute identically regardless of convergence mode
- Only the spec-fidelity step (step 8) has conditional behavior

### Step 9 Unaffected
- Wiring-verification (step 9) receives `spec_fidelity_file` as input
- In convergence mode, spec-fidelity output is written by `_write_convergence_report()`
- Wiring-verification bypass preserved

### Wiring-Verification Bypass
- Wiring-verification runs in `gate_mode=GateMode.TRAILING` (shadow mode)
- Independent of convergence mode

## Verification
- `uv run pytest tests/roadmap/ -v` — 1447 passed, 1 pre-existing failure
- Pre-existing failure: `test_turnledger_not_in_legacy_path` (not caused by T06.03)
