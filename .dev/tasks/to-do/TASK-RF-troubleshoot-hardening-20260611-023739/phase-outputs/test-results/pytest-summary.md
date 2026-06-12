# pytest summary — tests/troubleshoot/

**Overall result:** PASSED (exit 0)

- **Collected:** 18
- **Passed:** 18
- **Failed:** 0

| Module | Tests | Result |
|--------|-------|--------|
| `test_hardening_h0.py` | 2 (test_h0_applicability_skip_requires_boundary_scan, test_h0_boundary_scan_schema_rejects_bare_local_reason) | PASS |
| `test_hardening_h1.py` | 1 (test_h1_runtime_card_requires_negative_and_positive_witness) | PASS |
| `test_hardening_h2.py` | 2 (test_h2_empty_ledger_fails, test_h2_sibling_sweep_required_when_concept_shared — NEW G-PRE-1) | PASS |
| `test_hardening_h3.py` | 3 (word_boundary, small_grammar, sweep_card) | PASS |
| `test_hardening_h4.py` | 2 (nonempty_wrong_surface, manifest_intersection_proof) | PASS |
| `test_hardening_verdict.py` | 5 (3 unit: waiver_latch_one_way, h5_decision_maps, known_escapes_requires_cited_card; 2 integration: verdict_aggregation_from_h_statuses, downstream_success_cannot_override_latched) | PASS |
| `test_hardening_output_contract.py` | 3 integration (output_contract_backward_compat, backtest_status_advisory_until_complete, report_closure_not_proven_blockers) | PASS |

**Total: 13 unit + 5 integration = 18.** The two highest-risk guards both pass:
`test_verdict_aggregation_from_h_statuses` (all 7 §5.4 rows incl. both advisory rows 5/6) and
`test_downstream_success_cannot_override_latched_hardening_verdict` (FR-12↔NFR-4 pairing).

One test-authoring fix during the run: `test_backtest_status_keeps_pipeline_health_advisory_until_complete`
initially asserted `"advisory with missing escape IDs"` (dropped the backtick after `advisory`); the ref
correctly reads `` `advisory` with missing escape IDs listed `` — the **test** was corrected to assert
`"with missing escape IDs listed"`, not the ref (the ref content was right). Raw output: `pytest-output.txt`.

The 6 E2E backtest scenarios (E1–E5 + Waiver re-green) are documented in
`tests/troubleshoot/e2e-backtest-scenarios.md` (not pytest-collected; NFR-1 replay execution deferred to M5).
