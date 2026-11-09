# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent reflect-reviewer agent (opus), read-only; inputs: diff-analysis.md, Round 1 and Round 2 statements, plan and spec.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Adding "spec-panel-minfix" to `_POST_REFRESH_ADDITIONS` and running that test in Task 5 resolves C-001 | UNADDRESSED | HIGH | plan:119 says any failure caused by the new command other than a plugin-mirror parity demand "stops this task as blocked"; tests/recommend/test_routing_refresh.py:647-648 is exactly such a failure, so an executor following plan:119 must stop instead of editing the test; the fix must also rewrite plan:119 to permit this one edit and name the test file in Task 5 |
| INV-002 | interaction_effects | The C-002 (and INF-032) sentence can be added without hitting the 500-line limit | UNADDRESSED | MEDIUM | spec-panel.md 486 lines; remove 451-462 (12); add source.md:104-128 plus blank (26); 486 - 12 + 26 = 500; Makefile:403 fails above 500; CI runs make lint-architecture (.github/workflows/test.yml:133-135); Task 5 has no wc -l check; new sentences must be appended inside the existing source.md:120 paragraph, as plan:117 does |
| INV-003 | count_divergence | Among source.md:46 step-3 requirements only C-002 is missing from the shipped text | UNADDRESSED | HIGH | (a) reviewer exit-2 retry absent (C-002); (b) review-3 escalation "also listing each budget escalation with its need and each GRADE-CONFLICT" absent — Review Loop bullet 4 (spec-panel.md:261) escalates only "with the open blocking findings" and the block never mentions GRADE-CONFLICT (INF-032); (c) "authoritative" covered by block:120. Under A-003, (b) is the same kind of missing deliverable as (a) |
| INV-004 | guard_conditions | "Corrected once and re-run" covers every outcome of exit 2 | UNADDRESSED | LOW | neither reviser path (source.md:43, :127) nor reviewer path (source.md:46) says what a second exit 2 does; the C-002 sentence copies the gap; one clause (second exit 2 handled like exit 3) closes it |
| INV-005 | state_variables | `sys.dont_write_bytecode` is a full fix for C-009 | UNADDRESSED | MEDIUM | `__pycache__` is first written in Task 1 (plan:50) and persists through Tasks 2-3; `make clean` (Makefile:61) is in no task; a later setting leaves the old .pyc; `--exclude-dir=__pycache__` in the plan:104 grep works regardless |
| INV-006 | sufficiency_challenge | The C-009 fix alone makes every consumer of the skill folder pass | ADDRESSED | LOW | sync-dev skips (Makefile:117), verify-sync excludes (Makefile:178), test_worker_contract.py:1988-1991 skips UnicodeDecodeError, test_model_alias_policy.py:110 and test_tavily_doc_alignment.py:54 filter by suffix, test_routing_plugin_parity.py:25 excludes __pycache__; residual: install_skill.py:52 copytree and source.md:172 cp -rn copy the .pyc (harmless); a C-012 skill-folder scan must skip __pycache__ |
| INV-007 | sufficiency_challenge | The C-001 fix alone covers every test that enumerates src/superclaude/commands or skills | ADDRESSED | LOW | enumeration: test_routing_refresh.py:647 (fixed by C-001); test_worker_contract.py:834 (passes, Unattended heading removed per plan:115); test_worker_contract.py:1985 (passes unless C-011 tokens added); test_model_alias_policy.py:85-86; test_how_we_work_routing_table.py:352; test_graph_command.py:222; test_cli_install.py:541,598; test_routing_plugin_parity.py:41; make lint-architecture checks 1, 2, 6, 8 do not apply |
| INV-008 | interaction_effects | The C-002 and INF-032 sentences reach the build file without breaking Task 7 byte identity | ADDRESSED | LOW | Task 7 (plan:144) applies regions 1, 3, 4 of Task 5 and its AC (plan:147) compares `## Fix Budget` byte for byte; holds if the sentences are written into the region-4 definition at plan:117 |

## Summary

- **Total findings**: 8
- **ADDRESSED**: 3
- **UNADDRESSED**: 5
  - HIGH: 2 (INV-001, INV-003)
  - MEDIUM: 2 (INV-002, INV-005)
  - LOW: 1 (INV-004)

CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-003
These invariant violations must be resolved before convergence can be declared.
Action at --depth standard (no Round 3): recorded as unresolved conflicts; carried into the refactor plan as amendments with provenance, and reported in the return contract.

WARNING: 2 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-002, INV-005
These items do not block convergence but should be reviewed.

Not checked by the fault-finder: the 95f2c6e4 bullet-6 text; the write-verb regex count on spec-panel.md (relied on round2-v3.md).
