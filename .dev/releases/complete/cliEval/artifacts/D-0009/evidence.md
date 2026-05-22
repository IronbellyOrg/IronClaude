# D-0009 — Evidence

## Test execution

Command:

```
uv run pytest tests/cli/eval/test_capability_report.py -v
```

Result: **10 passed** (see `../../evidence/T01.10/pytest.log`).

| Test | Acceptance criterion |
|---|---|
| `test_capability_report_has_six_list_fields` | Class exposes the 6 list fields named in DM-008. |
| `test_capability_report_is_frozen` | `@dataclass(frozen=True)` invariant. |
| `test_capability_report_defaults_to_empty_tuples` | `CapabilityReport()` constructs an empty-but-valid report. |
| `test_capability_report_to_json_returns_mapping` | `to_json()` produces a JSON-serialisable mapping (round-trips through `json.dumps` / `json.loads`). |
| `test_capability_report_empty_to_json_canonical_shape` | Empty report serialises to the documented canonical form. |
| `test_capability_report_populated_to_json_roundtrips` | Populated report keys preserve dataclass field order; tuples → arrays; nested `CapabilityStatus` → dicts. |
| `test_capability_report_equality_is_structural` | `@dataclass`-generated `__eq__` compares all 6 fields. |
| `test_capability_status_has_required_fields` | Helper `CapabilityStatus` exposes the 6 row fields. |
| `test_capability_status_rejects_invalid_failure_mode` | `__post_init__` validates `failure_mode` membership. |
| `test_capability_status_to_dict_is_json_safe` | `CapabilityStatus.to_dict()` is `json.dumps`-safe. |

## Module surface

- `superclaude.cli.eval.capabilities.CapabilityReport` — 6-field frozen
  dataclass + `to_json()`.
- `superclaude.cli.eval.capabilities.CapabilityStatus` — per-row helper
  with `to_dict()`.
- `Capability` (T01.09) unchanged.

## Cross-task traceability

- **Roadmap DM-008** — fields list match: `report[], blocked_evals[],
  skip_flags[], hard_failures[], soft_skips[], soft_xfails[]`.
- **Validation report L2** — determinism AC softened; this
  implementation provides stable key order but does not assert
  byte-level determinism (Notes captured in spec.md).
- **Downstream T01.11 (COMP-009)** — `CapabilityGates.check_all()` will
  construct `CapabilityReport` instances using these dataclasses.
- **Downstream T01.13 (FR-CLI4)** — `eval doctor --json` will emit
  `report.to_json()`.
