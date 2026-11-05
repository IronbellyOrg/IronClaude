# Wider run compare

- Baseline: 6616 passed, 29 skipped, 1 xpassed, 5 warnings in 317.10s (0:05:17)
- Current: 6621 passed, 29 skipped, 1 xpassed, 5 warnings in 318.35s (0:05:18) (rc=0)
- Baseline-passing tests that now fail: 0
- Verdict: PASS

## The sixteen pre-existing test files of the Constraints (each run alone)

- tests/commands/test_workflow_command.py: ============================== 18 passed in 0.25s ==============================
- tests/commands/test_graph_command.py: ============================== 52 passed in 0.12s ==============================
- tests/commands/test_impact_command.py: ============================== 81 passed in 0.11s ==============================
- tests/commands/test_routing_plugin_parity.py: ============================== 5 passed in 0.03s ===============================
- tests/skills/test_brainstorm_protocol.py: ============================== 2 passed in 0.02s ===============================
- tests/skills/test_codegraph_adoption.py: ============================== 50 passed in 0.08s ==============================
- tests/skills/test_primitive_dual_surface_lookup.py: ============================== 3 passed in 0.02s ===============================
- tests/skills/test_tier2_tavily_consistency.py: ============================== 5 passed in 0.03s ===============================
- tests/skills/test_repo_inventory_nongit.py: ============================== 5 passed in 0.25s ===============================
- tests/skills/test_worker_contract.py: ============================= 394 passed in 0.66s ==============================
- tests/cli_portify/test_brainstorm_gaps.py: ============================== 16 passed in 0.27s ==============================
- tests/cli/test_init_lite.py: ============================== 44 passed in 0.33s ==============================
- tests/unit/test_cli_install.py: ============================== 96 passed in 0.63s ==============================
- tests/roadmap/test_threshold_registry.py: ============================== 23 passed in 5.38s ==============================
- tests/core/test_how_we_work_routing_table.py: ============================== 79 passed in 0.21s ==============================
- tests/recommend/test_routing_refresh.py: ============================= 248 passed in 1.45s ==============================
