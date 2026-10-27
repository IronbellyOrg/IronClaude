# D-0019: Spec Version Detection and Pre-v3.05 Compatibility Evidence

## Spec Hash Change Reset
- `load_or_create()` compares saved `spec_hash` with provided value
- Mismatch triggers full reset (empty runs and findings)
- Test: `TestBackwardCompatibility::test_registry_resets_on_spec_hash_change` PASS

## Pre-v3.05 Backward Compatibility
- `load_or_create()` defaults missing fields on load:
  - `source_layer` -> `"structural"`
  - `first_seen_run` -> `1`
  - `last_seen_run` -> `1`
- Test: `TestBackwardCompatibility::test_pre_v305_registry_loads_with_default_source_layer` PASS

## ACTIVE Status Accepted
- `VALID_FINDING_STATUSES` includes `"ACTIVE"`
- Test: `TestBackwardCompatibility::test_active_status_accepted` PASS

## Serialization Preserves Fields
- JSON output includes all new fields (`source_layer`, `first_seen_run`, `last_seen_run`, `stable_id`)
- Test: `TestBackwardCompatibility::test_registry_serialization_preserves_fields` PASS
