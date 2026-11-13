persona: refactorer
model_class: opus
model: claude-opus-5-5

## Findings block
```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"missing-requirement","claim":"The agent rule is hand-copied into guide section 4 and an unmarked CLAUDE.md paragraph, and no plan task adds a test pinning the two copies (only a manual AC), so that mirror can drift silently.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/TASK-WF-implementFrOnb1O-20261023-180618.md","line_start":96,"line_end":104},{"role":"test","path":".dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/artifacts/t7.diff","line_start":47,"line_end":54}],"self_confidence":0.4}
```

calibration:
  per_finding:
    F1: 0.68
