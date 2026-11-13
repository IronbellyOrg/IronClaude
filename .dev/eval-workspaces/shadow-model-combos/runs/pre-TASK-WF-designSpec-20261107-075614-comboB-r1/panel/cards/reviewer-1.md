persona: analyzer
model_class: sonnet
model: claude-sonnet-5-5

## Findings block
```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"No task assigns the conversion of the --read JSON (isDraft, headRefOid, autoMergeRequest) into the GuardRead dataclass; Task 3 creates only the type, so Task 11's driver or the SKILL prose must invent the mapping.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":88,"line_end":88,"quote":"class GuardRead:              # parsed output of `--read`"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":230,"line_end":230},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":52,"line_end":52}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 7 criterion 3 requires the script to pass the _RESOLUTION_SCRIPTS tests, but the same task adds it to that list only after Task 1 O2 confirms the list's purpose; if O2 says not to add it, the criterion cannot be met.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":108,"line_end":108,"quote":"only after reading the purpose of that list (Task 1 O2)"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":113,"line_end":113,"quote":"the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests"}]}
```

```yaml
calibration:
  card_confidence: 0.57
  per_finding:
    F1: 0.75
    F2: 0.65
```
