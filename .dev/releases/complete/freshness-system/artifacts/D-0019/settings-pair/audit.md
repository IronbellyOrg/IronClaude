# Audit — `~/.claude/settings.json` before vs after install (T05.01)

**Generated:** 2026-05-12

## Summary: ADDITIVE MERGE CONFIRMED

The install introduced exactly one change: addition of the top-level `hooks` key
with 7 freshness event registrations. No pre-existing keys were modified.

## Pre-install state (96 bytes)

```json
{
  "model": "opus[1m]",
  "effortLevel": "high",
  "skipDangerousModePermissionPrompt": true
}
```

(No `hooks` key — `jq '.hooks // "ABSENT"'` returned `"ABSENT"`)

## Post-install state

```json
{
  "model": "opus[1m]",
  "effortLevel": "high",
  "skipDangerousModePermissionPrompt": true,
  "hooks": {
    "SessionStart": [ ... session-init + freshness-session-start ... ],
    "UserPromptSubmit": [ ... freshness-user-prompt ... ],
    "PreToolUse": [ ... freshness-pre-edit (Edit|Write|mcp__serena__replace_*|insert_*_symbol matcher) ... ],
    "PostToolUse": [ ... freshness-post-read (Read matcher, async) ... ],
    "FileChanged": [ ... freshness-file-changed (.* matcher, async) ... ],
    "SubagentStart": [ ... freshness-subagent-start (async) ... ],
    "SubagentStop": [ ... freshness-subagent-stop (async) ... ]
  }
}
```

## Per-criterion audit

| Audit point | Status |
|---|---|
| (a) Existing user hooks preserved | N/A — user had no pre-existing hooks key. Vacuously satisfied. |
| (b) Only the 7 freshness registrations added (plus session-init.sh under SessionStart, which is from src/superclaude/hooks/hooks.json's own preserved entry) | PASS — `jq '.hooks | keys[]'` lists exactly the 7 expected event keys. |
| (c) No other key changes | PASS — `model`, `effortLevel`, `skipDangerousModePermissionPrompt` bit-identical to before.json. |

## Backup confirmed

```
$ ls ~/.claude/settings.json.bak.*
/config/.claude/settings.json.bak.20260512T225700Z  (96 bytes — bit-identical to before.json)
```

## Organic validation

Within the SAME session as the install, a subsequent `Write` tool call to
`/tmp/freshness-test-1/compose.yml` was correctly blocked by the freshness gate
with `reason=no_prior_read`. Telemetry row landed at
`~/.claude/logs/freshness-hook.jsonl`:

```json
{"ts":"2026-05-12T23:27:41+00:00","event":"PreToolUse","tool":"Write","path":"/tmp/freshness-test-1/compose.yml","session_id":"65f93d77-669a-48a6-a37a-9e7c5e48bf1f","tool_call_idx":1,"recent_read_age_sec":null,"external_change_seen":false,"decision":"block","reason":"no_prior_read"}
```

This is an end-to-end validation of: hook registration → settings.json parsing
by Claude Code → script execution at PreToolUse → telemetry append → stderr
block message → exit 2.
