# F-22: EXEMPT/LIGHT enforcement tiers not recognized by PRD `_evaluate_gate`

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P2, P7
**Identified by**: B-4
**File:line**: `src/superclaude/cli/prd/gates.py:300, 356, 404, 504`; consumer `src/superclaude/cli/prd/executor.py:531-540`

## Evidence

```python
# gates.py -- four entries declare non-STRICT enforcement
"check-existing": GateCriteria(..., enforcement_tier="EXEMPT")    # :300
"template-triage": GateCriteria(..., enforcement_tier="EXEMPT")   # :356
"preparation": GateCriteria(..., enforcement_tier="LIGHT")        # :404
"present-complete": GateCriteria(..., enforcement_tier="LIGHT")   # :504

# executor.py:531-540 -- only STRICT is recognized
if gate and status.is_success:
    gate_passed = self._evaluate_gate(step_id, gate, gate_content)
    if not gate_passed:
        if gate.enforcement_tier == "STRICT":
            status = PrdStepStatus.HALT
        else:
            status = PrdStepStatus.VALIDATION_FAIL
```

## Trace

- `grep -n "EXEMPT|LIGHT" src/superclaude/cli/prd/executor.py` returns zero hits. The generic `pipeline/gates.py` treats `EXEMPT` as "always pass" and `LIGHT` as "report-only", but PRD's bespoke `_evaluate_gate` ignores both.
- Net behavior: `EXEMPT` and `LIGHT` gates ARE evaluated and CAN set status to `VALIDATION_FAIL`. The label is decorative.
- Today the four steps happen to pass because they have `min_lines=0` and no `semantic_checks`. But adding any check (e.g. someone bumping `present-complete`'s `min_lines`) would silently start failing the run contrary to the declared "EXEMPT" intent.

## Reproduction sketch

Add `min_lines=10` to the `"preparation"` entry (LIGHT). A step producing 5 lines of output sets `PrdStepStatus.VALIDATION_FAIL` and surfaces as a pipeline failure, even though LIGHT semantically means "informational only."

## Confidence (aggregated)

0.90 -- Agent B verified via grep. The latent failure requires a future config change to manifest today.

## Cross-agent corroboration

- **Agent B** identified the mismatch between the declared enforcement tiers and the executor's actual handling, noting that the four exempt/light gates happen to pass today only because they have nothing to check.
