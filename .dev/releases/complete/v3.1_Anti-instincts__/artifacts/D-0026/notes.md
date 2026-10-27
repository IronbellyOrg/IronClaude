# D-0026: Shadow Mode Configuration Evidence

## Configuration Applied

All test sprint configurations use `gate_rollout_mode=shadow` for anti-instinct gate evaluation:

```python
# SprintConfig field (src/superclaude/cli/sprint/models.py:325)
gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"

# Shadow mode activated in test configurations:
config = SprintConfig(
    gate_rollout_mode="shadow",  # evaluate + record, no behavioral impact
    wiring_gate_mode="off",      # isolate anti-instinct from wiring
)
```

## Shadow Mode Semantics

Per the rollout mode matrix (executor.py:515-568):
- **off**: evaluate + ignore (no metrics recorded)
- **shadow**: evaluate + record metrics via ShadowGateMetrics (FR-SPRINT.4)
- **soft**: evaluate + record + credit on PASS / remediate on FAIL
- **full**: evaluate + record + credit on PASS / FAIL task on gate FAIL

Shadow mode causes **no behavioral change** to sprint task execution — the gate evaluates but the result is ignored per shadow mode semantics.

## Test Configurations Verified

| Test File | gate_rollout_mode | Verification |
|---|---|---|
| `tests/sprint/test_shadow_mode.py` | shadow (lines 124-134) | 15 tests PASS |
| `tests/sprint/test_anti_instinct_sprint.py` | shadow + all modes (lines 35-44) | 17 tests PASS |
| `tests/pipeline/test_full_flow.py` | shadow (lines 362-369) | Tests PASS |

## Validation

- All 32 shadow/anti-instinct tests pass (0 failures)
- All 101 anti-instinct module tests pass (fingerprint, obligation scanner, integration contracts, structural audit)
- Total: **133 tests PASS** across all anti-instinct test suites
