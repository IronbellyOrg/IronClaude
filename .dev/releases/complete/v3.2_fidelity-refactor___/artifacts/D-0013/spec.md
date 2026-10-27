# D-0013: SprintConfig Fields and Migration Shim

## Location
`src/superclaude/cli/sprint/models.py` — SprintConfig dataclass

## New Fields
- `wiring_gate_scope: str = "task"` — scope for `resolve_gate_mode()` (Goal-5d)
- `wiring_analysis_turns: int = 1` — turns per wiring analysis (OQ-2 default)
- `remediation_cost: int = 2` — turns per remediation attempt (OQ-2 default)

## Migration Shim (`__post_init__`)
Migrates deprecated field names to new canonical names:
- `wiring_budget_turns` -> `wiring_analysis_turns`
- `wiring_remediation_cost` -> `remediation_cost`
- `wiring_scope` -> `wiring_gate_scope`

Emits `DeprecationWarning` via `warnings.warn()` when old names are used.

**NFR-007**: Shim is clearly scoped to 1 release and marked for removal.

## Verification
- New fields have correct defaults: scope="task", turns=1, cost=2
- Migration shim emits DeprecationWarning for old field names
- Old field values correctly migrate to new field names
