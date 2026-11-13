persona: qa
model_class: haiku
model: claude-haiku-5-5

## Findings block
```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"The supplied matrix slice omits the event-field contracts. Task 8 excludes section 4.2, and no writer-side acceptance check enforces attempt-scoped request keys or first-request-only baseline fields; a protocol that reuses retry keys can pass while breaking crash matching.","refs":["FR-21"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":184,"line_end":185},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":124,"line_end":130}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"INF-048 requires one cycle_id across guard, push and re-trigger, but acceptance checks only the minting location and event order. A rereview_requested carrying a different cycle_id passes those checks and the published=True check, violating shared-cycle correlation.","refs":["INF-048","INF-050"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":251,"line_end":251},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":127,"line_end":129},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":170,"line_end":171}]}
```

calibration:
  per_finding:
    F1: 0.45
    F2: 0.6
