observation-kind: categorical
producer-count: 4 (grep hits for `exit 0` in the hook: 4; rows: 4)

## Producers
| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving=yes|no |
|---|---|---|---|---|---|---|---|
| P1 | src/superclaude/hooks/scripts/block-bare-python.sh:56 | exit 0 (jq missing) | src/superclaude/hooks/scripts/block-bare-python.sh:275 observed taken (scanner ran, so jq present) | n/a | yes | yes | no |
| P2 | src/superclaude/hooks/scripts/block-bare-python.sh:60 | exit 0 (awk missing) | src/superclaude/hooks/scripts/block-bare-python.sh:275 observed taken (scanner ran, so awk present) | n/a | yes | yes | no |
| P3 | src/superclaude/hooks/scripts/block-bare-python.sh:267 | exit 0 (empty input) | src/superclaude/hooks/scripts/block-bare-python.sh:275 observed taken (input non-empty) | n/a | yes | yes | no |
| P4 | src/superclaude/hooks/scripts/block-bare-python.sh:275 | `*) exit 0` when WORD is not python/python3/pip/pip3 | none | n/a | yes | yes | yes |
