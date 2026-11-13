persona: refactorer
model_class: opus
model: claude-gw-tier1a[1m]

## Findings block

```findings-v2
{"id": "F1", "severity": "MINOR", "blocking": false, "category": "other", "claim": "Tasks 1-8 and 10 say one bullet at the end of the Key Actions list, but every target list is numbered with bold labels; the executor supplies the number and label, and the AC cannot tell a correct item from a stray bullet.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md", "line_start": 28, "line_end": 28}, {"role": "source", "path": "src/superclaude/agents/system-architect.md", "line_start": 30, "line_end": 35}], "lens": "reflect-pre", "self_confidence": 0.85}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "missing-requirement", "claim": "Task 11 syncs src/superclaude to .claude only; the ten agents also have tracked copies in plugins/superclaude/agents that the plan never mentions and that still lack the rule.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md", "line_start": 102, "line_end": 102}, {"role": "source", "path": "plugins/superclaude/agents/system-architect.md", "line_start": 30, "line_end": 35}], "lens": "reflect-pre", "self_confidence": 0.7}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "contradiction", "claim": "Constraints:19 claims the rule text is the wording used in the four existing agents, but their wording is narrower (no checked_at, worktree_root, callees, impact); two versions of the shared rule now exist.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md", "line_start": 19, "line_end": 19}, {"role": "source", "path": "src/superclaude/agents/reflect-reviewer.md", "line_start": 64, "line_end": 64}], "lens": "reflect-pre", "self_confidence": 0.85}
{"id": "F4", "severity": "MINOR", "blocking": false, "category": "other", "claim": "Task 11 has the executor find the agent-file tests with grep instead of naming them, so the pass condition depends on what the executor picks.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md", "line_start": 102, "line_end": 102}, {"role": "plan", "path": ".dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md", "line_start": 105, "line_end": 105}], "lens": "reflect-pre", "self_confidence": 0.6}
```

```yaml
calibration:
  per_finding:
    F1: 0.88
    F2: 0.65
    F3: 0.65
    F4: 0.5
```
