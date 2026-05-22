# F-17: STRICT gate failures in structural-qa/qualitative-qa not propagated to outcome

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P8
**Identified by**: A-8
**File:line**: `src/superclaude/cli/prd/executor.py:392-409, 692-705`

## Evidence

```python
# 392-409 in run()
if result.outcome != "halt":
    self._execute_stage_b(result)

if result.outcome != "halt":
    ...
    completion_result = self._execute_step("present-complete", ...)
if result.outcome != "halt":
    result.outcome = "success"
```

The assembly branch in `_execute_stage_b` correctly checks for halt:
```python
# 676-689
if assembly_result.status.is_failure:
    gate = GATE_CRITERIA.get("assembly")
    if gate and gate.enforcement_tier == "STRICT":
        result.outcome = "halt"
        result.halt_step = "assembly"
        return
```

But structural-qa (executor.py:692-697) and qualitative-qa (700-705) results are appended but their failure does NOT halt the pipeline:
```python
# 692-697 -- no is_failure / STRICT check
struct_result = self._execute_step("structural-qa", ...)
self._step_results.append(struct_result)
result.step_results.append(struct_result)
```

## Trace

- **Writer**: `_execute_step` returns a PrdStepResult with status HALT/VALIDATION_FAIL on STRICT gate failure.
- **Reader**: Stage B's assembly branch checks it; structural-qa and qualitative-qa branches do NOT. The STRICT enforcement_tier defined in gates.py:475, 488 is honored inside `_run_subprocess_step:534` (which sets status=HALT on STRICT gate fail), but the higher-level outcome propagation only fires for assembly.

## Reproduction sketch

Force a STRICT semantic-check failure in structural-qa output. Step status=HALT but result.outcome="success". `superclaude prd run` exits 0 despite the documented STRICT gate.

## Confidence (aggregated)

0.80 -- Agent A verified the Stage B control flow. Semantics of "STRICT" enforcement are confirmed in the gate evaluation but not propagated to outcome.

## Cross-agent corroboration

- **Agent A** traced the full Stage B control flow and identified the inconsistency: assembly correctly propagates STRICT failures to `result.outcome`, but structural-qa and qualitative-qa -- both marked STRICT in gates.py -- do not have the same propagation logic.
