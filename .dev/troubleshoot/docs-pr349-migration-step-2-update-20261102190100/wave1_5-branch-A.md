# Wave 1.5 Branch A — release-doc lookup (returned by troubleshoot-analyst; persisted by parent on receipt)

```json
{
  "release_slug": "v5.0.0",
  "artifact_paths": [
    "/home/coder/workspaces/worktrees/IronClaude/release-v5.0.0/.dev/releases/current/v5.0.0/DECISIONS.md",
    "/home/coder/workspaces/worktrees/IronClaude/release-v5.0.0/.dev/releases/current/v5.0.0/RELEASE-READINESS.md",
    "/home/coder/workspaces/worktrees/IronClaude/release-v5.0.0/.dev/releases/current/v5.0.0/A3-RESULT.md"
  ],
  "summary": "DECISIONS.md:7 (decision 7.6) says to upgrade with '`superclaude update` (or `./update.sh`)', and RELEASE-READINESS.md:67, :151 and :180 call the two interchangeable because every installer call in main.py:365-404 passes force=True; A3-RESULT.md:13 repeats this. No artifact checks whether `update` runs the codegraph install phase or the codebase-memory/Serena retire step. The only stated upgrade gate, G7 (RELEASE-READINESS.md:198), runs `./update.sh` (`superclaude install --force`), so it never tests the `superclaude update` path the release notes recommend.",
  "confidence": 0.85,
  "degraded": true
}
```

Notes: `.dev/releases/complete/` does not exist; only `current/` searched. Grep/Glob plus Read (auggie and codegraph not used).
