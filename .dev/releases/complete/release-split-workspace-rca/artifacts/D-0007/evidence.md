# D-0007 — Evidence

**Task:** T03.01 — Add PreToolUse hook rejecting writes to `.claude/skills/*-workspace/**`
**Captured:** 2026-05-13 (probes executed against installed artefacts in working tree)
**Hook script SHA-256:** `e06e5e6a215a9a1b9d35c505267a9bb2def15f05a18f63c8a498670050fa5da4`

## Artefacts under test

### `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "description": "Reject-with-redirect: writes to `.claude/skills/*-workspace/**` are denied with a message naming the correct destination `.dev/eval-workspaces/<skill>/<remainder>`. Semantics are deny + explanatory message (Claude Code hooks do not transparently rewrite paths) — Claude is expected to retry against the redirected path. Source: phase-3-tasklist.md T03.01, FR-L1.1, R-007. Pattern precision (R-01): only `<...>/.claude/skills/<X>-workspace/<remainder>` matches; `.claude/skills/<X>/workspace.md` and `.claude/skills/<X>/file.md` are NOT affected.",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/reject-workspace-writes.sh",
            "timeout": 3
          }
        ]
      }
    ]
  }
}
```

### `.claude/hooks/reject-workspace-writes.sh` (header)

```bash
#!/usr/bin/env bash
# PreToolUse(Write|Edit) — reject-with-redirect for skill-creator sibling-workspace convention.
# Semantics: deny + explanatory message (Claude Code hooks do not transparently rewrite paths).
# Source: phase-3-tasklist.md T03.01, FR-L1.1, R-007.
#
# Decision contract:
#   - exit 0          → allow (path does not match `.claude/skills/*-workspace/<remainder>`)
#   - exit 2 + stderr → block; stderr is surfaced to Claude as the deny reason
```

(Full script: `.claude/hooks/reject-workspace-writes.sh`, mode `0755`.)

## Probe results

Probes invoke the hook directly via stdin with synthetic Claude Code tool-call JSON. The hook is decoupled from the harness so this isolates the matcher logic from any orchestration concerns.

### Probe 1 — POSITIVE (acceptance criterion 2)

**Target:** `.claude/skills/_probe-workspace/file.md`

stdin:
```json
{"tool_name":"Write","tool_input":{"file_path":"/config/workspace/IronClaude/.claude/skills/_probe-workspace/file.md"}}
```

**Exit:** `2`
**Stderr:**
```
Workspace path rejected: write to `.claude/skills/_probe-workspace/file.md` blocked. Use `.dev/eval-workspaces/_probe/file.md` instead.

Reason: skill-creator's sibling-workspace convention places eval workspaces next to the skill directory under `.claude/skills/`, which mixes throwaway artifacts with the source-of-truth skill packages. This project relocates them under `.dev/eval-workspaces/<skill-name>/`. See `.dev/README.md` for the published convention, or run `make eval-skill SKILL=_probe` to create the correct destination.
```

✅ AC met: stderr contains the substring `.dev/eval-workspaces/`; exit status `2` blocks the tool call.
✅ Filesystem confirmation: `.claude/skills/_probe-workspace/file.md` does **not** exist after probe (write blocked, no side effect).

### Probe 2 — NEGATIVE-1 (acceptance criterion 3)

**Target:** `.claude/skills/sc-tasklist-protocol/SKILL.md` (existing legitimate skill file)

stdin:
```json
{"tool_name":"Edit","tool_input":{"file_path":"/config/workspace/IronClaude/.claude/skills/sc-tasklist-protocol/SKILL.md"}}
```

**Exit:** `0`
**Stderr:** *(empty)*

✅ AC met: hook does not fire; the legitimate skill file is unaffected.

### Probe 3 — NEGATIVE-2 (acceptance criterion 4)

**Target:** `.claude/skills/_probe/workspace.md` (single-file `workspace.md`, NOT a `-workspace/` directory)

stdin:
```json
{"tool_name":"Write","tool_input":{"file_path":"/config/workspace/IronClaude/.claude/skills/_probe/workspace.md"}}
```

**Exit:** `0`
**Stderr:** *(empty)*

✅ AC met: hook does not fire; pattern precision R-01 verified.

### Probe 4 — EDGE (R-01 stress: directory segment containing `-workspace-`)

**Target:** `.claude/skills/my-workspace-test/file.md` (segment is `my-workspace-test`, ends in `-test` not `-workspace`)

stdin:
```json
{"tool_name":"Write","tool_input":{"file_path":"/config/workspace/IronClaude/.claude/skills/my-workspace-test/file.md"}}
```

**Exit:** `0`
**Stderr:** *(empty)*

✅ Confirms `([^/]+)-workspace/` requires the segment to terminate exactly at `-workspace/`.

### Probe 5 — EDGE (R-01 stress: filename `-workspace.md` suffix)

**Target:** `.claude/skills/foo/bar-workspace.md` (file named `bar-workspace.md`, not a directory)

stdin:
```json
{"tool_name":"Write","tool_input":{"file_path":"/config/workspace/IronClaude/.claude/skills/foo/bar-workspace.md"}}
```

**Exit:** `0`
**Stderr:** *(empty)*

✅ Confirms trailing `/` requirement: `-workspace` followed by `.md` does not match.

### Probe 6 — FAIL-OPEN (NFR-3 mirror)

**Target:** missing `file_path` in `tool_input`

stdin:
```json
{"tool_name":"Write","tool_input":{}}
```

**Exit:** `0`
**Stderr:** *(empty)*

✅ Hook fails open when there is no path to inspect — cannot falsely block tool calls lacking the field.

## Acceptance criteria matrix

| AC | Bullet | Result |
|---|---|---|
| AC1 | `.claude/settings.json` contains PreToolUse hook matching `.claude/skills/*-workspace/**` for `Write` and `Edit`. | ✅ Matcher `Write\|Edit` registered; pattern enforced via the script. |
| AC2 | Positive case rejected with message containing `.dev/eval-workspaces/`. | ✅ Probe 1, exit=2, stderr contains literal substring `.dev/eval-workspaces/_probe/file.md`. |
| AC3 | Negative case 1 (`<existing-skill>/SKILL.md`) proceeds without firing. | ✅ Probe 2, exit=0, empty stderr. |
| AC4 | Negative case 2 (`workspace.md` filename) proceeds without firing. | ✅ Probe 3, exit=0, empty stderr. |

## Source-of-truth placement

Per project convention (CLAUDE.md), `src/superclaude/` is the canonical home for distributable artefacts. `.claude/hooks/` is generated by `make sync-dev` (Makefile L136-141 copies `src/superclaude/hooks/scripts/*.sh` → `.claude/hooks/`).

Canonical script: `src/superclaude/hooks/scripts/reject-workspace-writes.sh`
Sync target:     `.claude/hooks/reject-workspace-writes.sh`

`make verify-sync` reports: `✅ All components in sync.`
`diff` between canonical and dev copy: identical.

## Conclusion

PreToolUse(Write\|Edit) hook is installed and behaves per spec. R-01 (pattern precision) is verified by 2 mandatory negative probes plus 2 additional edge cases (`my-workspace-test/`, `bar-workspace.md`) that stress the regex boundary. No legitimate skill paths are affected; the positive case is blocked deterministically with the redirect message naming `.dev/eval-workspaces/<X>/<remainder>`.
