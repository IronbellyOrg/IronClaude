persona: qa
model_class: haiku
model: claude-haiku-5-5
model_observed: OpenAI GPT assistant; exact deployment model identifier unavailable in this session.

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"The inferred matrix omits the loop-guard enumeration update, state-machine overlay and public exports. Tasks 2, 10 and 5 cover them, but 45/45 measures only extracted rows, not the full spec.","refs":[],"coverage_rows":["INF-022","INF-023","INF-024","INF-025","INF-026","INF-027","INF-028","INF-029","INF-030","INF-031","INF-032","INF-033","INF-034","INF-035","INF-036","INF-037","INF-038"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":242,"line_end":243},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":291,"line_end":291},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":44,"line_end":49},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":85,"line_end":89},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":150,"line_end":154}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Tasks 9, 10 and 12 consume Task 1's recorded pins or literal text but omit explicit Depends on: Task 1 lines, contrary to section 10. Transitive dependencies preserve ordering, so this is declaration drift, not a blocker.","refs":["INF-041"],"coverage_rows":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":363,"line_end":363},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":134,"line_end":137},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":148,"line_end":154},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":179,"line_end":182}]}
```

```yaml
calibration:
  per_finding:
    F1: 0.45
    F2: 0.7
```
