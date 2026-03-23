# D-0005: Wiring Manifest YAML Schema

## Deliverable
`tests/v3.3/wiring_manifest_schema.yaml` — YAML schema defining the contract for the FR-4 reachability gate's wiring manifest.

## Schema Sections

### `entry_points` (required, non-empty list)

| Field | Type | Required | Description |
|---|---|---|---|
| `module` | str | Yes | Fully-qualified Python module path (dotted notation) |
| `function` | str | Yes | Function or class name within the module |

### `required_reachable` (required, non-empty list)

| Field | Type | Required | Description |
|---|---|---|---|
| `target` | str | Yes | Fully-qualified symbol path (module.symbol) |
| `from_entry` | str | Yes | Function name from `entry_points` that must reach this target |
| `spec_ref` | str | Yes | Specification reference for traceability (e.g. "v3.1-T04") |

## Validation Rules
1. Every `from_entry` must reference a `function` declared in `entry_points`
2. Every `target` must be a fully-qualified path (contains at least one dot)
3. Every entry must have a non-empty `spec_ref`
4. No duplicate `(target, from_entry)` pairs

## Constraints
- Parseable by `yaml.safe_load()` (PyYAML or stdlib)
- All fields documented with inline YAML comments
- Schema is consumed by `ReachabilityAnalyzer` (T01.06)
- Populated manifest (T01.07) at `tests/v3.3/wiring_manifest.yaml` must conform to this schema

## Spec References
- FR-4.1: Spec-Driven Wiring Manifest
- Authoritative manifest: v3.3 requirements spec §Wiring Manifest (13 entries)
