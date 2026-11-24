observation-kind: string
producer-count: 1

## Producers
| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving |
|---|---|---|---|---|---|---|---|
| P1 | src/superclaude/cli/swarm/lenses/refactor_find.py:53 | recommended_next_command_template=("/sc:code-review --apply {compare_files}") | n/a: module-level constant, no function early exit | before CLI dispatch; persists into contract after dispatch | yes: deterministic | local-cli-stub-1 return-contract.yaml:64 | yes |

This is a string recommendation, not a categorical status. The exact literal has one source in the lens; commands.py:2141-2143 supplies paths and reduce.py:672-697 formats and carries the string. Those are transformers of this producer, not alternative causes. No producer was excluded. discriminator-required: no (one known producer, disputed string present in captured failing output).
