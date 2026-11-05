# Diagnosability tasklist (informational; verdict partial, trivial)
discriminator-required: no
## Emitter search
- none required: the execution is observed directly by probe-lock-trust.out (marker file written by the in-tree backend).
## Pending rows
- P-1: unit tests, one per trigger (backend-path, non-empty project.dynamic, path source, editable source), each returns the field name; plus a clean pyproject returning no finding. re-run permitted: yes
- P-2: the halt message names the triggering field (the reason string carried to `sync_tier3`). re-run permitted: yes
