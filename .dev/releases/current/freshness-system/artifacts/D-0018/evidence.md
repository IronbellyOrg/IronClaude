# D-0018 — make sync-dev && superclaude install --force

## Task: T05.01 (STANDARD, Critical Path Override)

**Date executed:** 2026-05-12T22:57:00Z (UTC)

## Sequence

1. `make sync-dev` — copied 19 skills, 35 agents, 40 commands, 8 hooks to `.claude/`.
2. `uv run superclaude install --force` — installed all 4 components to `~/.claude/` PLUS the new step 5 `install_hooks` which copied 8 scripts and merged 7 freshness event registrations into `~/.claude/settings.json`.

## Output excerpt

```
📦 Installing hooks to ~/.claude/hooks/...

✅ Copied 8 hook script(s) to /config/.claude/hooks:
   - freshness-session-start.sh
   - freshness-user-prompt.sh
   - freshness-pre-edit.sh
   - freshness-post-read.sh
   - freshness-file-changed.sh
   - freshness-subagent-start.sh
   - freshness-subagent-stop.sh
   - session-init.sh

📋 settings.json merge: events=7 added=8
💾 Backup: /config/.claude/settings.json.bak.20260512T225700Z
```

(Note: `added=8` reflects 7 event keys; the SessionStart array gained both the
preserved `session-init.sh` registration AND the new `freshness-session-start.sh`
— see audit.md for the matcher-collision logic that allowed both to land.)

## Post-install state

| File / Resource | Expected | Got |
|---|---|---|
| `~/.claude/settings.json` jq parse | exit 0 | exit 0 ✓ |
| Hook events registered | 7 freshness events | FileChanged, PostToolUse, PreToolUse, SessionStart, SubagentStart, SubagentStop, UserPromptSubmit ✓ |
| Scripts in `~/.claude/hooks/` | 7 freshness + session-init = 8 | 8 ✓, all mode 0755, all `bash -n` clean |
| `~/.claude/CLAUDE.md` contains freshness section | "## Context freshness discipline" present | ✓ |
| Backup created BEFORE write | `~/.claude/settings.json.bak.<UTC-ISO-Z>` exists | ✓ `~/.claude/settings.json.bak.20260512T225700Z` |

## Organic validation (within-session)

A subsequent `Write` to `/tmp/freshness-test-1/compose.yml` was blocked by the
freshness gate:

```
PreToolUse:Write hook error: [~/.claude/hooks/freshness-pre-edit.sh]:
You have not Read `/tmp/freshness-test-1/compose.yml` in this session.
Read it before editing.
```

Telemetry row landed correctly (see `~/.claude/logs/freshness-hook.jsonl`):

```json
{"ts":"2026-05-12T23:27:41+00:00","event":"PreToolUse","tool":"Write","path":"/tmp/freshness-test-1/compose.yml","session_id":"65f93d77-669a-48a6-a37a-9e7c5e48bf1f","tool_call_idx":1,"recent_read_age_sec":null,"external_change_seen":false,"decision":"block","reason":"no_prior_read"}
```

State directories were created lazily:
```
~/.claude/state/
├── bg-agents/
└── tool-call-counter/65f93d77-669a-48a6-a37a-9e7c5e48bf1f.txt  (counter=1)
```

This is end-to-end live validation: hook registered → Claude Code parsed
settings.json → script fired at PreToolUse(Write) → no-prior-Read branch hit
→ stderr message + exit 2 → tool call blocked → telemetry appended.

## Acceptance criteria

| Criterion | Status |
|---|---|
| `jq -r '.hooks | keys[]' ~/.claude/settings.json` includes 7 freshness events | PASS |
| `~/.claude/hooks/` contains 7 mode-0755 freshness-*.sh files | PASS |
| `~/.claude/CLAUDE.md` contains "## Context freshness discipline" | PASS |
| `audit.md` confirms additive merge | PASS (see D-0019/settings-pair/audit.md) |
| Fresh-session SessionStart smoke (step 12) | DEFERRED to user's next session; documented in phase-5-runbook.md |
