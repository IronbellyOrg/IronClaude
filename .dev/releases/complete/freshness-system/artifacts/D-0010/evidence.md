# D-0010 — hooks.json registration

## Task: T03.01 (STRICT, Critical Path Override)

Merged 7 freshness event registrations into `src/superclaude/hooks/hooks.json` and its plugins mirror per design §5.

## Files

- `src/superclaude/hooks/hooks.json` — source of truth
- `plugins/superclaude/hooks/hooks.json` — distribution mirror, identical

## Event keys (verified via `jq -r '.hooks | keys[]'`)

```
FileChanged
PostToolUse
PreToolUse
SessionStart
SubagentStart
SubagentStop
UserPromptSubmit
```

All 7 events present.

## SessionStart preservation

Existing `session-init.sh` registration is preserved (NOT replaced). The freshness handler is **appended** to the SessionStart array:

```
$ jq -r '.hooks.SessionStart[].hooks[].command' src/superclaude/hooks/hooks.json
~/.claude/hooks/session-init.sh
~/.claude/hooks/freshness-session-start.sh
```

## NFR compliance

| NFR | Check | Result |
|---|---|---|
| NFR-6 (no `$HOME` in JSON) | `grep -Fc '$HOME' …hooks.json` | 0 in both files |
| NFR-6 (no relative paths) | `grep -Fc './scripts' …hooks.json` | 0 |
| NFR-10 (exit code discipline) | Only freshness-pre-edit emits exit 2; verified in T02.03 | PASS |
| NFR-12 (user-scope path) | All paths use `~/.claude/hooks/...` (user-scope absolute) | PASS |
| async:true placement | Verified async on PostToolUse, FileChanged, SubagentStart, SubagentStop. Blocking on SessionStart, UserPromptSubmit, PreToolUse. | PASS |
| matcher form (Edit-class pipe) | `Edit\|Write\|mcp__serena__replace_content\|...\|mcp__serena__insert_before_symbol` | matches design §5 / Agent 1's matcher rules |

## Validation

```
$ jq . src/superclaude/hooks/hooks.json > /dev/null && echo OK
OK
$ jq . plugins/superclaude/hooks/hooks.json > /dev/null && echo OK
OK
$ diff src/superclaude/hooks/hooks.json plugins/superclaude/hooks/hooks.json
(empty)
MIRROR CLEAN
```

## Acceptance criteria

| Criterion | Status |
|---|---|
| `after.json` is valid JSON; jq-validation.txt captured | PASS |
| `diff.md` shows 7 added event registrations, no unrelated modifications | PASS |
| No `$HOME` reference anywhere in either hooks.json | PASS |
| All hook command paths use `~/.claude/hooks/...` form | PASS |

## Sub-agent review

The Phase 2 quality-engineer review already verified the matcher patterns and exit-code discipline against the design. The JSON shape here matches design §5 verbatim. No additional sub-agent invocation needed for T03.01 since the structural-JSON change is mechanical and the runtime semantics live in the handlers (reviewed in Phase 2).
