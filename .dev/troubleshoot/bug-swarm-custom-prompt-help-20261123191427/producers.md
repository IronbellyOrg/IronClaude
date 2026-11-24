observation-kind: string

## Producers

| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving |
|---|---|---|---|---|---|---|---|
| P1 | src/superclaude/cli/swarm/commands.py:438 | validate-lenses help docstring names --custom-prompt-dir | help parser exits before callback | no job started | yes | captured validate-lenses-help.txt | yes |
| P2 | src/superclaude/cli/swarm/commands.py:3785 | scaffold lens option help names --custom-prompt-dir | help parser exits before callback | no job started | yes | captured scaffold-help.txt | yes |

String observation, not categorical enumeration: these are the two public help producers named by the issue, not an exhaustive enum/exit-token census. Both directly observed in separate captured help outputs; no competing unique producer inference. The parser rejection is a separate captured consumer boundary, not an unexplained categorical symptom.
