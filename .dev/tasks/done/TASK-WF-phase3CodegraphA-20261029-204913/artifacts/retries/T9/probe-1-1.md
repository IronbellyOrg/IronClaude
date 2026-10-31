889a6e1761a021b181184fc4dc8f0a06be41a255
family=impact-self-row
defect form: an impact-result row that is the queried definition itself is counted or listed as a dependent
command: grep -n -E -e "source: impact" -e "affected\[\]" -e "transitive" -- src/superclaude/skills/sc-impact-protocol/SKILL.md
before:
43:| 5 | Transitive dependents | per definition: `mcp__codegraph__codegraph_impact {"symbol": "<sym>", "file": "<def file>", "depth": <--dep
44:| 5' | Status-only branch transport (CLI, before any Grep fallback) | when step 2 chose the CLI transport, steps 3-5 use the CLI forms ca
86:| `symbols[]` | list[map] | per definition: `name`, `file`, `start_line` (int or null), `end_line` (int or null), `mapped_by` (`name` \| 
127:  - {name: example_symbol, file: pkg/module.py, start_line: 10, end_line: 42, mapped_by: name, prod: {shown: 2, total: 2}, test: {shown:
144:1. `## Summary`: one paragraph, then a table `symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated`.
coupled sites: step 5' CLI row (affected[] first row is the symbol itself, E2-help.md:13); contract symbols[].transitive {count, depth}; impact.md Summary transitive column

after:
43:| 5 | Transitive dependents | per definition: `mcp__codegraph__codegraph_impact {"symbol": "<sym>", "file": "<def file>", "depth": <--dep
44:| 5' | Status-only branch transport (CLI, before any Grep fallback) | when step 2 chose the CLI transport, steps 3-5 use the CLI forms ca
86:| `symbols[]` | list[map] | per definition: `name`, `file`, `start_line` (int or null), `end_line` (int or null), `mapped_by` (`name` \| 
127:  - {name: example_symbol, file: pkg/module.py, start_line: 10, end_line: 42, mapped_by: name, prod: {shown: 2, total: 2}, test: {shown:
144:1. `## Summary`: one paragraph, then a table `symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated`.
