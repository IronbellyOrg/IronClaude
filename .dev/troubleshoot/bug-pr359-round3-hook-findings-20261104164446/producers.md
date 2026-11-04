observation-kind: categorical
producer-count: 5 (executable exit 0 hits: 4; exit 2 hits: 1; rows: 5)

## Producers
| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving=yes|no |
|---|---|---|---|---|---|---|---|
| P1 | src/superclaude/hooks/scripts/block-bare-python.sh:66 | exit 0 (jq missing) | src/superclaude/hooks/scripts/block-bare-python.sh:336 observed taken (scanner ran) | n/a | yes | yes | no |
| P2 | src/superclaude/hooks/scripts/block-bare-python.sh:70 | exit 0 (awk missing) | src/superclaude/hooks/scripts/block-bare-python.sh:336 observed taken (scanner ran) | n/a | yes | yes | no |
| P3 | src/superclaude/hooks/scripts/block-bare-python.sh:328 | exit 0 (empty input) | src/superclaude/hooks/scripts/block-bare-python.sh:336 observed taken (input non-empty) | n/a | yes | yes | no |
| P4 | src/superclaude/hooks/scripts/block-bare-python.sh:336 | `*) exit 0` when WORD is not python/python3/pip/pip3 (finding 2) | none | n/a | yes | yes | yes |
| P5 | src/superclaude/hooks/scripts/block-bare-python.sh:340 | `exit 2` after the block message (finding 1) | none | n/a | yes | yes | yes |
