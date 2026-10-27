# D-0062: Verify Module Generation Order (NFR-006)

## Status: COMPLETE

## Deliverable
`tests/cli_portify/test_nfr006_module_order.py` — 10 tests asserting NFR-006 order

## NFR-006 Mandated Order (AC-012)
models → gates → prompts → config → inventory → monitor →
process → executor → tui → logging_ → diagnostics → commands → __init__

## Tests
1. `test_nfr006_step_count` — 13 modules exactly
2. `test_nfr006_exact_order` — exact sequence matches NFR-006
3. `test_nfr006_get_step_order_matches` — get_step_order() consistent
4. `test_nfr006_consecutive_pairs_ordered` — each pair in correct order
5. `test_nfr006_assert_step_order_passes_for_valid` — no raise for valid order
6. `test_nfr006_assert_step_order_raises_for_swapped` — raises for swapped order (anti-false-pass)
7. `test_nfr006_all_module_names_present` — all 13 names present
8. `test_nfr006_commands_before_init` — commands immediately before __init__
9. `test_nfr006_models_is_first` — models is first
10. `test_nfr006_init_is_last` — __init__ is last

## Verification
```
uv run pytest tests/cli_portify/test_nfr006_module_order.py -k "nfr006" -v
```
Result: 10 passed ✓

Reorder-detection test (test_nfr006_assert_step_order_raises_for_swapped) catches any reordering with pytest.raises(AssertionError) ✓
