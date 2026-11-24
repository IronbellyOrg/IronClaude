# Contract Enumeration Ledger

## Rows
| contract_token | role | component_path | discovery_method | classification | unreachability_proof |
|---|---|---|---|---|---|
| recommended_next_command_template | producer | cli/swarm/lenses/{refactor_find,bare_review,edge_case_hunt,spec_completeness,feasibility_probe,troubleshoot_hypothesis,doc_completeness,reflect_review}.py | exact search of 8 files | classified: live registry entries | n/a |
| recommended_next_command_template | transformer | cli/swarm/preflight.py:540-543 | source Read | classified: caller wins/default copy | n/a |
| template/substitutions | transformer | cli/swarm/commands.py:929-930,2129-2157 | source Read + CLI capture | classified: fresh run | n/a |
| command on resume | consumer | cli/swarm/commands.py:2578-2586 | call-site Read | classified: no template passed; separate pre-existing behavior | n/a |
| template/substitutions | producer | cli/reflect/ensemble.py:394-419 | source Read | classified: own reflect template/prefix | n/a |
| rendered command | transformer | cli/swarm/reduce.py:448-467,672-702 | source Read + real CLI | classified: format/store/emit | n/a |
| rendered command | transformer | cli/swarm/models.py:957-960; cli/swarm/schema.py | field search + field-semantics Read | classified: type/schema declarations | n/a |
| suspect placeholder | evaluator | cli/swarm/lenses/_validate.py:393-430,603-609 | source Read | classified: no shipped-command check | n/a |
| recommended_next_command | consumer | skills/sc-swarm-wizard-protocol/SKILL.md:159-164,181 | Read | classified: parse/display | n/a |
| recommended_next_command | consumer | skills/sc-swarm-wizard-protocol/refs/run-monitor-summarize.md:88 | Read | classified: verbatim display | n/a |
| recommended_next_command | consumer | skills/sc-swarm-wizard-protocol/templates/summary.md:19 | Read | classified: presentation | n/a |
| recommended_next_command | consumer | skills/sc-swarm-wizard-protocol/refs/cli-contract.md:105 | exact reference search | classified: field documentation | n/a |
| recommended_next_command | consumer | skills/sc-bare-review/SKILL.md:47-76 | Read | classified: wrapper contract, preserve suspect coupling | n/a |
| --compare files | consumer | /home/coder/.claude/skills/sc-adversarial-protocol/SKILL.md:54-62 | active contract Read | classified: 2-10 readable existing comma-separated inputs | n/a |
| template/command | evaluator | tests/swarm/test_reduce.py:305-314; test_bundled_lenses.py:102-122,187-202; test_e2e_user_guide.py:179-198 | Read + 76 baseline passes | classified: interpolation/presence only in cited tests | n/a |

## Sibling sweep
Exact recommended_next_command search in src/superclaude returned 20 files, covered by grouped rows above. All eight live lens template files inventoried; custom placeholder emits no template by default. Callgraph returned 48 rows including tests/imports; three production reducer callers were verified at actual call sites in tier1-callers.md. No live runtime consumer in this discovered source family is unclassified. Canonical source paths above are relative to src/superclaude unless installed/test prefixes say otherwise. No plugin lens file found by scoped name search; not a claim of whole-plugin absence.

## Verdict
HC2: PASS for bounded contract discovery and fresh-run path proof, not a repair acceptance verdict. Keep refactor-specific correction from mutating bare/reflect prefix and suspect contracts. Resume behavior is classified, not silently repaired or certified.
