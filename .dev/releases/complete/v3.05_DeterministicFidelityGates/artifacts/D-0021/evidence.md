# D-0021: 3-Run Simulation Integration Test Evidence

## Test: `TestThreeRunSimulation::test_three_run_simulation`

### Run 1: Seed
- 2 structural HIGHs (STR-001, STR-002) + 1 semantic HIGH (SEM-001)
- Verified: structural_high_count=2, semantic_high_count=1, total=3
- Registry saved and reloaded

### Run 2: Partial Fix + New Finding
- STR-002 removed (FIXED), SEM-002 added
- Verified: STR-002 status=FIXED, SEM-002 first_seen_run=2
- Counts: structural=1, semantic=2, total=3
- Registry saved and reloaded

### Run 3: Cumulative Verification
- SEM-002 removed (FIXED)
- Final state: 4 unique findings, 2 ACTIVE (STR-001, SEM-001), 2 FIXED (STR-002, SEM-002)
- Counts: structural=1, semantic=1, total=2
- All stable IDs unique (collision-free)
- All run metadata complete with split counts

### Additional Test: Stable ID Consistency
- `test_three_run_stable_id_consistency`: verifies same finding retains same stable ID across save/load cycles

## Result
All assertions pass. 28/28 tests green.
