# D-0001 — hooks.json session-init.sh path rewrite

## Task: T01.01

Rewrite the fragile relative-path `./scripts/session-init.sh` to the post-install absolute form `~/.claude/hooks/session-init.sh` in both source and plugins mirror. Per `docs/analysis/hooks-json-relative-path-issue.md` Option B.

## Changes

### `src/superclaude/hooks/hooks.json`

```diff
@@ -5,7 +5,7 @@
         "hooks": [
           {
             "type": "command",
-            "command": "./scripts/session-init.sh",
+            "command": "~/.claude/hooks/session-init.sh",
             "timeout": 10
           }
         ]
```

### `plugins/superclaude/hooks/hooks.json`

Identical one-line change (mirror).

## Validation

| Check | Command | Result |
|---|---|---|
| Source JSON valid | `jq . src/superclaude/hooks/hooks.json` | exit 0 |
| Plugins JSON valid | `jq . plugins/superclaude/hooks/hooks.json` | exit 0 |
| Mirror identical | `diff src/.../hooks.json plugins/.../hooks.json` | empty (clean) |
| No `./scripts` reference | `grep -c './scripts' …` | 0 in both |
| Command resolves to expected | `jq -r '.hooks.SessionStart[0].hooks[0].command' …` | `~/.claude/hooks/session-init.sh` (both) |

## Acceptance — PASS

- One-line change in each of the two hooks.json files.
- `jq .` returns exit 0 for both.
- No `./scripts/` occurrences remain.
- notes.md documents current location of `session-init.sh` for T04.01 inclusion.
