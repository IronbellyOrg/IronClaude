persona: qa
model_class: haiku
model: claude-haiku-5-5
model_observed: gpt-6-luna

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Task 11 requires the scenario tests in prose, but its acceptance criteria only require the test names and acceptance trace; they do not mechanically verify the release-failure retry, unreadable-timeline-never-readies, or moved-head behaviors.","refs":["INF-039","INF-041"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":166,"line_end":173},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":305,"line_end":320}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"The plan requires protocol prose to omit file:NNN pointers, but no acceptance criterion checks that constraint.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":23,"line_end":23},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":124,"line_end":130},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":369,"line_end":369}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 7 makes adding the script to _RESOLUTION_SCRIPTS conditional on Task 1's investigation, but its acceptance criterion requires the script to pass that list's origin-URL tests without requiring or specifying list membership. The check may therefore be vacuous.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":108,"line_end":108},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":113,"line_end":114},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":339,"line_end":341}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 9 requires the Wave 0 bullet to include the L3/off message, but its acceptance criterion says the test fails when the bullet names an L3 condition. Unless that prohibition is scoped to the ref-loading gate, the required L3/off wording makes the criterion fail.","refs":["INF-002","INF-031"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":137,"line_end":141},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":241,"line_end":241}]}
```

coverage_rows_checked: INF-001, INF-002, INF-003, INF-004, INF-005, INF-006, INF-007, INF-008, INF-009, INF-010, INF-011, INF-012, INF-013, INF-014, INF-015, INF-016, INF-017, INF-018, INF-019, INF-020, INF-021, INF-022, INF-023, INF-024, INF-025, INF-026, INF-027, INF-028, INF-029, INF-030, INF-031, INF-032, INF-033, INF-034, INF-035, INF-036, INF-037, INF-038, INF-039, INF-040, INF-041, INF-042, INF-043, INF-044, INF-045, INF-046, INF-047, INF-048
reviewer_model_self_report: gpt-6-luna

calibration:
  per_finding:
    F1: 0.85
    F2: 0.90
    F3: 0.70
    F4: 0.85
