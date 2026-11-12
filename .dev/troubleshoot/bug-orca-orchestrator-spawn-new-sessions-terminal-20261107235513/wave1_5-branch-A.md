# Wave 1.5 Branch A (release-doc lookup), returned by troubleshoot-analyst, persisted by parent

```json
{
  "release_slug": "none (no .dev/releases/current or complete entry scopes this issue). The only scoping artifact is the managed task package TASK-WF-fixIssue412SVeri-20261106-215543, the earlier fix for issue #412.",
  "artifact_paths": [
    "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/source.md",
    "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md",
    "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/artifacts/final-review.md",
    "/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/tasks/done/TASK-WF-fixIssue412SVeri-20261106-215543/artifacts/reflect-pre-20261106-215816/artifacts/orca-discovery.md"
  ],
  "summary": "The #412 package added a globally loaded rule (src/superclaude/core/CLAUDE.md:45-53) and matching ccsession-tag README text (:228-237): new ccsession-backed Claude sessions use Claude (CLI), never New Terminal; programmatic creation uses `agent launch` or `worktree create --agent`; `terminal create` is for shells. It also repaired install_user_setup(force=True) so existing Orca guides get a safe refresh. Its final review states these are selection instructions only, with no claim that a UI route was tested; source.md leaves the runtime cause UNDETERMINED and the failing agent transcript unverified. No .dev/releases artifact scopes the subject.",
  "confidence": 0.9
}
```
