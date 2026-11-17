persona: refactorer
model_class: opus
model: claude-opus-5-5

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The spec asks for README guidance that matches core/CLAUDE.md, but Task 1's criteria only list items each copy must contain and never compare the copies, so the shared guidance can drift; the delivered copies already differ on the ccsession-orca sentence.","refs":["INF-001"],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md","line_start":1,"line_end":1,"quote":"Add an explicit globally loaded rule in src/superclaude/core/CLAUDE.md and matching src/superclaude/skills/ccsession-tag/README.md guidance"},{"role":"plan","path":".dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md","line_start":35,"line_end":36,"quote":"Both instruction surfaces explicitly distinguish Claude (CLI) for ccsession-backed Claude sessions from New Terminal"}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"The Task 2 clause 'existing edited-guide contents are not rewritten by IronClaude' cannot fail: install_orca_skills never writes guide files and the tests stub out Orca, so only the no---force check actually enforces the spec's do-not-overwrite rule.","refs":[],"citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md","line_start":1,"line_end":1,"quote":"Do not forward --force to Orca or overwrite edited guides"},{"role":"plan","path":".dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md","line_start":50,"line_end":50,"quote":"The external command never gains --force and existing edited-guide contents are not rewritten by IronClaude."}]}
```

```yaml
calibration:
  per_finding:
    F1: 0.65
    F2: 0.75
```
