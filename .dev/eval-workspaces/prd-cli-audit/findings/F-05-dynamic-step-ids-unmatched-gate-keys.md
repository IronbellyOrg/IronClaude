# F-05: Dynamic step IDs not matched by static GATE_CRITERIA keys

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P1, P3
**Identified by**: A-3, B-3
**File:line**: `src/superclaude/cli/prd/executor.py:727, 745, 757` (dynamic ID generation); `src/superclaude/cli/prd/gates.py:407, 426, 432` (static keys)

## Evidence

```python
# executor.py:727, 745, 757 -- step IDs are minted dynamically
step_id = f"investigation-{i + 1}"
f"web-research-{i + 1}"
f"synthesis-{i + 1}"
# executor.py:886 -- fix cycles too
f"{qa_step_id}-fix-{cycle + 1}"

# gates.py:407, 426, 432 -- keys have no numeric suffix
"investigation":   GateCriteria(...),
"web-research":    GateCriteria(...),
"synthesis":       GateCriteria(...),

# executor.py:530 -- exact-match lookup
gate = GATE_CRITERIA.get(step_id)  # "investigation-1" -> None
```

## Trace

- **Writer**: `_build_investigation_steps` / `_build_web_research_steps` / `_build_synthesis_steps` generate `investigation-1`, `web-research-2`, `synthesis-3`, etc.
- **Reader**: `_execute_step` at executor.py:530 calls `GATE_CRITERIA.get(step_id)` with exact-match. `GATE_CRITERIA.get("investigation-1")` returns `None`. No gate runs for any individual investigation, web-research, or synthesis agent.
- **Gate dead code**: The "STANDARD" gates defined in gates.py for `"investigation"`, `"web-research"`, `"synthesis"` are unreachable at the executor layer.
- **TUI gap**: Stage B steps never appear in the TUI step list (executor.py:366-367 only registers Stage A).
- **Persistence gap**: `_persist_step_artifact` also silently does nothing for these step IDs.

## Reproduction sketch

Add `print(gate)` after `GATE_CRITERIA.get(step_id)` in `_run_subprocess_step`. Every `investigation-N` / `web-research-N` / `synthesis-N` prints `None`. A `synthesis-3` agent emitting a 5-line stub passes with no gate check.

## Confidence (aggregated)

0.96 -- Both agents verified the key strings and lookup site independently. Agent A traced the full executor chain; Agent B traced the gate-side key mismatch.

## Cross-agent corroboration

- **Agent A** identified the absence of a canonical Stage B step registry and showed that `_STAGE_A_STEPS` does not cover these dynamic steps.
- **Agent B** independently confirmed that `GATE_CRITERIA.get("investigation-1")` returns `None` and traced the exact gate-dead-code consequence.
