persona: analyzer
model_class: sonnet
model: claude-sonnet-5-5
model_observed: claude-gw-tier1b (Claude, Anthropic)

## Findings block

```findings-v2
{"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Fold returns a dict (subscripted in Task 5 acceptance) but decision functions read guard.phase/.baseline by attribute; plan never fixes the type or Phase string values, so Task 4 and Task 5 criteria can conflict.","refs":["INF-014","INF-017"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":187,"line_end":192,"quote":"returns `None` or this dict"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":118,"line_end":119,"quote":"observed = read.transitions - guard.baseline"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":90,"line_end":90,"quote":"state[\"draft_guard\"][\"phase\"] == \"held\""}]}
{"id":"F2","severity":"MAJOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"resume_decision row 4 must re-enter release_decision but has no cycle_id/target_sha/applied_edits inputs; Task 4 criterion gives no expected action/cause for row 4, so the contract is unimplementable as stated.","refs":["INF-015","INF-016"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":109,"line_end":109,"quote":"resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":166,"line_end":166},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":77,"line_end":77,"quote":"each re-enter `release_decision` with `push_completed=True`"}]}
{"id":"F3","severity":"MAJOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Fold row for settled(any, skipped, user_override) does not set disabled_cause, yet guard_status keys user_override off it; plan tests fold and status separately so a wrong report of off/unavailable would pass.","refs":["INF-018"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":206,"line_end":206},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":112,"line_end":112},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":60,"line_end":61}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Spec section 3 says resume reconciles unsettled requests at any ordinal, but resume row 2 returns REPORT_HELD first below ordinal 3 or in off mode; plan pins row-2 precedence without noting that pending requests stay unreconciled.","refs":["INF-016"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":58,"line_end":58},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":164,"line_end":165},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":76,"line_end":76}]}
```

```yaml
calibration:
  per_finding:
    F1: 0.8
    F2: 0.8
    F3: 0.7
    F4: 0.6
```
