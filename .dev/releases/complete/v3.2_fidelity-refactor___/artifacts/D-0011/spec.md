# D-0011: Phase 2 Entry Prerequisites — OQ-2 and OQ-6 Resolution

## OQ-2: Budget Constants

**Decision**: Set conservative defaults with SprintConfig overrides.

| Constant | Default Value | Rationale |
|----------|--------------|-----------|
| `WIRING_ANALYSIS_TURNS` | 1 | Analyze only the most recent turn's output. Minimizes budget impact during shadow rollout. |
| `REMEDIATION_COST` | 2 | Two turns per remediation attempt (matches `attempt_remediation` retry-once semantics in `trailing_gate.py`). |

**SprintConfig override fields** (added to `sprint/models.py`):
- `wiring_analysis_turns: int = 1` — overrides `WIRING_ANALYSIS_TURNS`
- `remediation_cost: int = 2` — overrides `REMEDIATION_COST`
- `wiring_gate_scope: str = "task"` — scope for `resolve_gate_mode()` (Goal-5d)

These fields feed into `resolve_gate_mode(scope, grace_period)` per Goal-5d, replacing the string-switch `wiring_gate_mode`.

## OQ-6: SprintGatePolicy Constructor Compatibility

**Decision**: No compatibility issues. Interface contract documented below.

### Source Validation

`TrailingGatePolicy` (in `pipeline/trailing_gate.py`) is a `typing.Protocol`:
- `build_remediation_step(self, gate_result: TrailingGateResult) -> Step`
- `files_changed(self, step_result: StepResult) -> set[Path]`

`SprintGatePolicy` (in `sprint/executor.py`) implements this protocol:
- Constructor: `__init__(self, config: SprintConfig)` — single argument
- Both protocol methods implemented with correct signatures

### Callable-Based Remediation Interface (Constraint 7)

The `attempt_remediation()` function in `trailing_gate.py` uses callable parameters:
- `can_remediate: Callable[[], bool]` — budget check without TurnLedger import
- `debit: Callable[[int], None]` — budget debit without TurnLedger import

This design satisfies Constraint 7: no TurnLedger import in `pipeline/trailing_gate.py`.

The `run_post_task_wiring_hook()` in `sprint/executor.py` will pass:
- `can_remediate=ledger.can_remediate` (when ledger is not None)
- `debit=ledger.debit` (when ledger is not None)

## Traceability

- OQ-2: Roadmap Phase 2 Entry Prerequisites table, row 1
- OQ-6: Roadmap Phase 2 Entry Prerequisites table, row 2
- Constraint 7: Roadmap Milestone 2.2 architectural note
- Goal-5d: Roadmap Milestone 2.2 (`resolve_gate_mode` replaces string-switch)
