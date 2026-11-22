## Bug Summary

Launching via the `ccsession` launcher takes about 20 seconds and 5-10% CPU when the saved session list is large. Suspected cost centre is the per-session listing work the launcher performs before starting Claude.

## Environment (OS, version)

- OS: Not known yet
- Version: repo checkout at commit 495eb96d1 (branch docs/409-orca-dashboard-designs, 2026-11-17)

## Current Behavior

A `ccsession` launch takes ~20 seconds and 5-10% CPU when the session list is large. No further reproduction numbers are known yet.

## Expected Behavior

Launch should complete in a few seconds with minimal CPU regardless of the number of saved sessions; listing overhead should not scale per saved session on every launch.

## Steps to Reproduce

1. Not known yet (exact trigger inside the launch path not yet measured; a troubleshoot run will produce it)

## Impact Assessment (Severity, Blast Radius)

- Severity: medium — every launch is delayed tens of seconds for users with many sessions; no data loss or wrong behaviour.
- Blast Radius: All ccsession launches (`ccsession <topic>`, ccsession-orca terminal opens) on machines with a large `~/.claude/projects` session list.

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

- Launcher script: `src/superclaude/skills/ccsession-tag/ccsession` (1902 lines, bash).
- `list_sessions()` iterates every workspace dir under `~/.claude/projects` and every `topics/*.txt` label: src/superclaude/skills/ccsession-tag/ccsession:1446-1457.
- Per topic it spawns subprocesses: `head` (ccsession:1467), `session_transcript` fallback which runs `ls -t "$PROJECTS_DIR"/*/"$1".jsonl` over all workspaces (ccsession:1362, called at ccsession:1472), two `stat` calls `get_btime`/`get_mtime` (ccsession:1379, 1401; called at ccsession:1483-1484) and `date` formatting per row (ccsession:1415, 1489-1490) — O(sessions) process spawns, a plausible source of the 20 s / 5-10% CPU with a large list.
- The interactive path `ask_session_name()` (used by `ccsession-orca`, i.e. every Orca/Coder terminal open) calls the same listing machinery: ccsession:1538-1565 and `ensure_names_migrated` at ccsession:1564.
- Root cause is intentionally not diagnosed here; a troubleshoot run will confirm which step dominates.

## Related Issues

Not known yet (scout search for "ccsession launch slow" found no duplicates)

## Testing Notes

Not known yet

<!-- sc:issue:create template=issue-bug-simple -->
