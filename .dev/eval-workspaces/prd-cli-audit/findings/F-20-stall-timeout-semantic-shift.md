# F-20: Stall timeout semantic shift -- named for stall cadence, used as wall-clock via 30x multiplier

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P4, P7, P8
**Identified by**: A-13, D-3
**File:line**: `src/superclaude/cli/prd/executor.py:499`; `src/superclaude/cli/prd/models.py:190-191`

## Evidence

```python
# executor.py:499
timeout_seconds=self._config.stall_timeout * 30,

# models.py:190
stall_timeout: int = 120   # 120 * 30 = 3600s wall-clock
```

## Trace

- `PrdConfig.stall_timeout` field name suggests "kill on N seconds of no output" (stall detection cadence).
- The value is silently multiplied by 30 and used as total wall-clock subprocess timeout.
- There is no separate field for wall-clock timeout vs. stall threshold -- collapsed into a single field whose meaning depends on the consumer.
- Combined with F-11 (stall detection is dead code): the field's name is actively misleading because no stall detection runs at all. Only the 30x-scaled wall-clock timeout fires.
- `stall_action` is also never read anywhere in PRD code, so the "warn"/"halt" distinction does not exist.

## Reproduction sketch

User sets `stall_timeout=30` (thinking they tighten stall detection) -> overall timeout becomes 900s, cutting off long subprocesses. Or user raises to 600 for long quiet periods -> every step's wall-clock cap becomes 5 hours.

## Confidence (aggregated)

0.90 -- Both agents independently identified the semantic confusion. Agent A flagged the magic multiplier; Agent D traced the full implication.

## Cross-agent corroboration

- **Agent A** identified the magic `* 30` multiplier and the semantic confusion between stall cadence and wall-clock budget.
- **Agent D** traced the full implication: the field name is actively misleading because no stall detection exists (per F-11), so `stall_timeout` only controls wall-clock timeout, and `stall_action` is also dead code.
