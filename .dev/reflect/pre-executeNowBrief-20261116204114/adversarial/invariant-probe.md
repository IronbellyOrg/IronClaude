# Invariant Probe Results (Round 2.5, fault-finder agent a13b1a875a4e52024)
| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | interaction_effects | Task 10 may freely rewrite the comment at commands.py:63-66 | UNADDRESSED | MEDIUM | tests/observe/test_commands.py:750 asserts "release-gates.md" and "Task 18" are in commands.py; both exist only at commands.py:64-65 (orchestrator re-Read: confirmed) |
| INV-002 | sufficiency_challenge | A run-use grep over the package would pass | REFUTED by orchestrator | LOW | `grep -rn "run-use" src/superclaude/cli/observe/` printed exactly two lines (adapter.py:43, commands.py:90) and no binary match; __pycache__ is git-ignored |
| INV-003 | count_divergence | plan counts right (9, 21 fields, 684) | ADDRESSED | LOW | test_terminal.py:56,65,73,80; view.py:199-220 |
| INV-004 | guard_conditions | len(overflow) == 1 holds | ADDRESSED (not run) | LOW | test_render.py:101 |
| INV-005 | collection_boundaries | test_fixtures.py:185-191 scans goldens | ADDRESSED | LOW | test_fixtures.py:25-30 |
| INV-006 | state_variables | Task 5 keeps retention coverage | ADDRESSED | LOW | test_collector.py:568,600 |
| INV-007 | state_variables | Task 3 helper needs no ValueError | ADDRESSED | LOW | test_fixtures.py:41-43 |
| INV-008 | interaction_effects | Task 8 only changes tests | UNADDRESSED | LOW | export.py:32-34 (accepted by the debate) |
| INV-009 | guard_conditions | Task 12 grep -c row check is stable | UNADDRESSED | LOW | acceptance-tests.md:25,28,51,56 |
## Summary
- Total 9; UNADDRESSED: HIGH 0, MEDIUM 1 (INV-001), LOW 2 (INV-008, INV-009); INV-002 refuted on disk by the orchestrator
