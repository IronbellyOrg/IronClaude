persona: qa
model_class: haiku
model: claude-gw-tier2[1m]

## Findings block

```findings-v2
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "claim": "Tasks 1-10 check token presence and diff shape without explicitly verifying the complete freshness metadata and fallback contract required by the spec.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md", "line_start": 31, "line_end": 31}, {"role": "plan", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md", "line_start": 94, "line_end": 94}, {"role": "spec", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/source.md", "line_start": 1, "line_end": 1}], "lens": "reflect-pre", "self_confidence": 0.91}
{"id": "F2", "severity": "MINOR", "blocking": false, "category": "contradiction", "claim": "The plan falsely attributes its composed rule text to all four reference agents instead of distinguishing their shared pattern from the spec-added metadata conditions.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md", "line_start": 19, "line_end": 19}, {"role": "spec", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/source.md", "line_start": 1, "line_end": 1}, {"role": "source", "path": "src/superclaude/agents/troubleshoot-analyst.md", "line_start": 27, "line_end": 27}, {"role": "source", "path": "src/superclaude/agents/reflect-reviewer.md", "line_start": 64, "line_end": 64}, {"role": "source", "path": "src/superclaude/agents/reuse-auditor.md", "line_start": 50, "line_end": 50}, {"role": "source", "path": "src/superclaude/agents/auggie-reviewer.md", "line_start": 79, "line_end": 79}], "lens": "reflect-pre", "self_confidence": 0.99}
```

```yaml
calibration:
  per_finding:
    F1: 0.85
    F2: 0.92
```
