# D-0023: wiring_gate_mode Field in SprintConfig

## Deliverable
`wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` field added to `SprintConfig` dataclass in `src/superclaude/cli/sprint/models.py`.

## Implementation
- Added `from typing import Literal` import (alongside existing `Optional`)
- Added field after `shadow_gates` with default `"shadow"` per section 5.8
- Field semantics: off=disabled, shadow=log only, soft=warn on critical, full=block on critical+major

## Verification
- `SprintConfig()` instantiates with `wiring_gate_mode="shadow"` by default
- All four mode values accepted: off, shadow, soft, full
- Existing `SprintConfig` instantiations remain backward compatible (no required args added)
- Field accessible as `config.wiring_gate_mode` with correct `Literal` type

## Evidence
```
T05.01 PASS: SprintConfig.wiring_gate_mode works correctly
```
