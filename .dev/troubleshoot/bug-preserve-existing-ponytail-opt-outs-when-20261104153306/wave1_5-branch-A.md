```json
{
  "release_slug": "issue-330-ponytail-plugin-install (no .dev/releases hit; brainstorm 20261104-063430 + TASK-WF-closeIronbellyOr-20261104-124207)",
  "artifact_paths": [
    "/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md",
    "/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/.dev/brainstorms/20261104-063430-ponytail-plugin-install/adversarial/merged-output.md",
    "/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/.dev/tasks/done/TASK-WF-closeIronbellyOr-20261104-124207/TASK-WF-closeIronbellyOr-20261104-124207.md"
  ],
  "summary": "The brainstorm sets the only opt-out as \"ponytail@ponytail\": false in enabledPlugins, says apply_settings_defaults keeps a key that is already present, and warns users not to delete that key (merged-requirements.md:170). AC-M2 requires that after a rerun the value stays false and no Ponytail command runs (merged-requirements.md:287); the plan's T3/T4 Leg 2 requires a user ponytail@ponytail = False to be unchanged after apply (TASK-WF...md:44), documented opt-out text at :81. All were written before the key was renamed to ponytail@ironclaude (1de47e82); no artifact covers migrating an existing ponytail@ponytail: false, so the rename breaks the opt-out these artifacts guarantee.",
  "confidence": 0.85,
  "degraded": true
}
```

Notes: `.dev/releases/` has no artifact for these components (only unrelated "Ponytail" principle mentions at `.dev/releases/current/WorkflowV3/merged-requirements.md:158`, `.dev/releases/current/WorkflowV3/adversarial/merged-output.md:156`). degraded: auggie unavailable, Grep/Read used.
