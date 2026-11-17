persona: qa
model_class: haiku
model: claude-haiku-5-5

## Findings block
```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Tasks 9 and 12 consume Task 1's pre-build record without declaring Task 1 dependencies, contrary to the explicit producer-consumer dependency rule. Transitive paths preserve ordering, so no execution failure is established.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":363,"line_end":363,"quote":"a task depends on every earlier task whose output it imports or consumes"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":134,"line_end":137},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":179,"line_end":182}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Task 13 gives the flags guide only a values/default row; the specified explanatory paragraph, clear command and held meaning are assigned only to the commands guide. Its acceptance criterion permits the flags-guide omission.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":245,"line_end":245,"quote":"Flag row and a paragraph: what it does, the clear command, `held` meaning, default on."},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":195,"line_end":198}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The coverage matrix omits the requested/settled event-payload contracts and complete-dependency instruction. A builder using it as a completion checklist could miss malformed event construction or missing dependency edges; its percentage is not full-spec coverage.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":184,"line_end":185},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":363,"line_end":363},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":56,"line_end":62}]}
```

```yaml
calibration:
  card_confidence: 0.76
  per_finding:
    F1: 0.85
    F2: 0.60
    F3: 0.55
```
