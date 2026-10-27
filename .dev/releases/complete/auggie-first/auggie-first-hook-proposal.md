# Proposal: auggie-first nag in freshness hooks

**Target project for application:** `/config/workspace/IronClaude/`
**Author of proposal:** Claude (drafted 2026-05-14 from `/config/workspace/InfraDocs`)
**Source-of-truth hooks during drafting:** `~/.claude/hooks/freshness-*.sh` (read on 2026-05-14)
**Apply via:** new chat in IronClaude with this file as input; do **not** apply from the InfraDocs chat.

---

## 1. Locked design (from /sc:brainstorm Q1–Q6, 2026-05-14)

| # | Decision | Implication |
|---|---|---|
| Q1 | **(c)** — fire on `SessionStart source=resume` AND on in-session Δ ≥ **10800s (3h)** | Two trigger points; fresh sessions (`source=startup`) get no nag. |
| Q2 | **(a)** — trust `~/.claude.json:.mcpServers` registration | Sub-ms check via `jq`. False positives (registered-but-down) tolerated. |
| Q3 | **(c-modified)** — always-on with project-aware behavior | Two paths: indexed projects get full nag; unindexed get a one-time warn + auto-dismiss. User can re-enable warn or promote to full nag by editing config. |
| Q4 | **(b)** — own line in the envelope | `  auggie_first_required=1` or `  auggie_project_not_indexed=1 (...)`. |
| Q5 | **(b)** — sticky-until-acted-on | New PostToolUse hook clears sticky on auggie tool call. |
| Q6 | **(a)** — highest priority, never truncated | Emitted before `changed_since_last_turn` and `RESUMED_FLAG` in the envelope. |

## 2. Files affected (paths under IronClaude project)

Assuming IronClaude project keeps hooks in the same layout (`~/.claude/hooks/` global + `<project>/.claude/settings.json`):

1. **MODIFY** `~/.claude/hooks/freshness-user-prompt.sh` — add §6.5 auggie-flag block + extend `build_envelope()`.
2. **MODIFY** `~/.claude/hooks/freshness-session-start.sh` — set sticky file on `source=resume`.
3. **CREATE** `~/.claude/hooks/auggie-flag-clear.sh` — PostToolUse handler to clear sticky.
4. **MODIFY** settings.json (project-level or `~/.claude/settings.json`) — add PostToolUse entry for `mcp__auggie__codebase-retrieval`.
5. **CREATE** `~/.claude/auggie-projects.txt` — one CWD path per line; the indexed-projects list.

## 3. State directory layout (created on demand)

```
~/.claude/state/
├── auggie-first-pending/<session_id>.txt   # sticky flag; existence = nag pending
└── auggie-no-warn/<project_key>            # sentinel; existence = warn already fired for this project

# where project_key = CWD with / replaced by - (matches existing memory dir convention)
```

`~/.claude/auggie-projects.txt` (user-editable, one path per line):

```
/config/workspace/InfraDocs
/config/workspace/IronClaude
```

## 4. Diff 1 — `~/.claude/hooks/freshness-user-prompt.sh`

Insert a new section between current step **6 (Conditional items)** and step **7 (RESUMED flag)**. Also extend `build_envelope()` signature and update all call sites.

```diff
@@ existing section 6 (Conditional items) ends here @@
 if [ "$BG_COUNT" -gt 0 ] 2>/dev/null; then
     ITEMS+="bg=$BG_COUNT "
 fi

+# 6.5. Auggie-first flag (Q1=c: in-session Δ≥10800s OR sticky carry-over from SessionStart=resume)
+#      Q2=a: trust ~/.claude.json:.mcpServers registration.
+#      Q3=c: full nag for indexed projects; one-time warn for unindexed (auto-dismisses).
+#      Q5=b: sticky-until-acted-on — cleared by PostToolUse on auggie tool call.
+AUGGIE_FLAG=""
+AUGGIE_WARN=""
+PROJECT_KEY=$(printf '%s' "$CWD" | sed 's|/|-|g' 2>/dev/null || true)
+STICKY_FILE="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
+THRESHOLD_S=10800   # 3h. Bump to 14400 for 4h.
+
+CROSSED=false
+if [ -f "$STICKY_FILE" ]; then
+    CROSSED=true
+elif [ -n "$DELTA_SEC" ] && [ "$DELTA_SEC" -ge "$THRESHOLD_S" ] 2>/dev/null; then
+    CROSSED=true
+fi
+
+if [ "$CROSSED" = true ]; then
+    AUGGIE_REG=false
+    if [ -r "$HOME/.claude.json" ] && command -v jq >/dev/null 2>&1; then
+        if jq -e '.mcpServers // {} | has("auggie")' "$HOME/.claude.json" >/dev/null 2>&1; then
+            AUGGIE_REG=true
+        fi
+    fi
+
+    if [ "$AUGGIE_REG" = true ]; then
+        INDEXED_LIST="$HOME/.claude/auggie-projects.txt"
+        IS_INDEXED=false
+        if [ -r "$INDEXED_LIST" ] && [ -n "$CWD" ]; then
+            if grep -Fxq "$CWD" "$INDEXED_LIST" 2>/dev/null; then
+                IS_INDEXED=true
+            fi
+        fi
+
+        DISMISS_FILE="$STATE_DIR/auggie-no-warn/$PROJECT_KEY"
+
+        if [ "$IS_INDEXED" = true ]; then
+            mkdir -p "$STATE_DIR/auggie-first-pending" 2>/dev/null || true
+            [ ! -f "$STICKY_FILE" ] && echo "$NOW_ISO" > "$STICKY_FILE" 2>/dev/null || true
+            AUGGIE_FLAG="auggie_first_required=1"
+        elif [ ! -e "$DISMISS_FILE" ]; then
+            mkdir -p "$(dirname "$DISMISS_FILE")" 2>/dev/null || true
+            : > "$DISMISS_FILE" 2>/dev/null || true
+            rm -f "$STICKY_FILE" 2>/dev/null || true
+            AUGGIE_WARN="auggie_project_not_indexed=1 (consider indexing $CWD with auggie; warning silenced — delete $DISMISS_FILE to re-enable, OR add $CWD to $INDEXED_LIST to activate auggie-first nag)"
+        fi
+    fi
+fi
+
 # 7. RESUMED flag
 RESUMED_FLAG=""
 if [ -n "$DELTA_SEC" ] && [ "$DELTA_SEC" -ge 3600 ] 2>/dev/null; then
     RESUMED_FLAG="RESUMED_AFTER_LONG_PAUSE; rich refresh fired in SessionStart"
 fi

 # 8. Build envelope with truncation cascade
 build_envelope() {
     local changed_field="$1"
     local resumed_line="$2"
+    local auggie_flag="$3"
+    local auggie_warn="$4"
     {
         echo "<session-context>"
         printf '  ts=%s turn=%d' "$NOW_ISO" "$TURN"
         if [ -n "$ITEMS" ]; then
             printf ' %s' "${ITEMS% }"
         fi
         echo
+        # Q6=a: auggie fields are highest priority — never truncated.
+        if [ -n "$auggie_flag" ]; then
+            echo "  $auggie_flag"
+        fi
+        if [ -n "$auggie_warn" ]; then
+            echo "  $auggie_warn"
+        fi
         if [ -n "$changed_field" ]; then
             echo "  changed_since_last_turn=$changed_field"
         fi
         if [ -n "$resumed_line" ]; then
             echo "  $resumed_line"
         fi
         echo "</session-context>"
     }
 }

 CHANGED_FULL=""
 if [ "$CHANGED_COUNT" -gt 0 ]; then
     CHANGED_FULL=$(printf '%s\n' "$CHANGED_PATHS" | grep -v '^$' | paste -sd ',' -)
 fi
-ENVELOPE=$(build_envelope "$CHANGED_FULL" "$RESUMED_FLAG")
+ENVELOPE=$(build_envelope "$CHANGED_FULL" "$RESUMED_FLAG" "$AUGGIE_FLAG" "$AUGGIE_WARN")
 TRUNCATED=false
 FIRST_THREE=""
 DROPPED=0

 # Truncate changed_since_last_turn first
 if [ ${#ENVELOPE} -gt 9000 ] && [ "$CHANGED_COUNT" -gt 3 ]; then
     FIRST_THREE=$(printf '%s\n' "$CHANGED_PATHS" | grep -v '^$' | head -3 | paste -sd ',' -)
     DROPPED=$((CHANGED_COUNT - 3))
     CHANGED_TRUNC="${FIRST_THREE},...(${DROPPED} more)"
-    ENVELOPE=$(build_envelope "$CHANGED_TRUNC" "$RESUMED_FLAG")
+    ENVELOPE=$(build_envelope "$CHANGED_TRUNC" "$RESUMED_FLAG" "$AUGGIE_FLAG" "$AUGGIE_WARN")
     TRUNCATED=true
 fi
 # Drop RESUMED if still over
 if [ ${#ENVELOPE} -gt 9000 ] && [ -n "$RESUMED_FLAG" ]; then
     if [ -n "$FIRST_THREE" ]; then
-        ENVELOPE=$(build_envelope "${FIRST_THREE},...(${DROPPED} more)" "")
+        ENVELOPE=$(build_envelope "${FIRST_THREE},...(${DROPPED} more)" "" "$AUGGIE_FLAG" "$AUGGIE_WARN")
     else
-        ENVELOPE=$(build_envelope "$CHANGED_FULL" "")
+        ENVELOPE=$(build_envelope "$CHANGED_FULL" "" "$AUGGIE_FLAG" "$AUGGIE_WARN")
     fi
     TRUNCATED=true
 fi
```

## 5. Diff 2 — `~/.claude/hooks/freshness-session-start.sh`

Add a block immediately AFTER the `build_context()` function definition closes and BEFORE the `CONTEXT=$(build_context "$SOURCE" …)` invocation. It's a pure state side-effect, not envelope content.

```diff
@@ end of build_context() function, before CONTEXT=… invocation @@
         echo "</session-context>"
     }
 }

+# Auggie-first sticky setup on resume (Q1=c).
+# Only sets the sentinel — user-prompt hook reads it and decides nag vs warn vs silent.
+if [ "$SOURCE" = "resume" ]; then
+    AUGGIE_REG=false
+    if [ -r "$HOME/.claude.json" ] && command -v jq >/dev/null 2>&1; then
+        if jq -e '.mcpServers // {} | has("auggie")' "$HOME/.claude.json" >/dev/null 2>&1; then
+            AUGGIE_REG=true
+        fi
+    fi
+    if [ "$AUGGIE_REG" = true ]; then
+        mkdir -p "$STATE_DIR/auggie-first-pending" 2>/dev/null || true
+        : > "$STATE_DIR/auggie-first-pending/$SESSION_ID.txt" 2>/dev/null || true
+    fi
+fi
+
 CONTEXT=$(build_context "$SOURCE" 2>/dev/null || echo "<session-context source=\"$SOURCE\">ts=$NOW_ISO</session-context>")
```

## 6. New file — `~/.claude/hooks/auggie-flag-clear.sh`

```bash
#!/usr/bin/env bash
# PostToolUse: clear the auggie-first sticky flag once auggie codebase-retrieval has been called.
# Per Q5=b: sticky-until-acted-on. Fail-open per NFR-3.
set -u

STATE_DIR="$HOME/.claude/state"
INPUT="$(cat 2>/dev/null || true)"

SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || true)

if [ "$TOOL_NAME" = "mcp__auggie__codebase-retrieval" ]; then
    rm -f "$STATE_DIR/auggie-first-pending/$SESSION_ID.txt" 2>/dev/null || true
fi
exit 0
```

After creating: `chmod +x ~/.claude/hooks/auggie-flag-clear.sh`.

## 7. Diff 3 — settings.json (PostToolUse array)

Existing:

```json
"PostToolUse": [
  {
    "matcher": "Read",
    "hooks": [
      {"type": "command", "command": "~/.claude/hooks/freshness-post-read.sh", "timeout": 1, "async": true}
    ]
  }
]
```

Patched:

```json
"PostToolUse": [
  {
    "matcher": "Read",
    "hooks": [
      {"type": "command", "command": "~/.claude/hooks/freshness-post-read.sh", "timeout": 1, "async": true}
    ]
  },
  {
    "matcher": "mcp__auggie__codebase-retrieval",
    "hooks": [
      {"type": "command", "command": "~/.claude/hooks/auggie-flag-clear.sh", "timeout": 1, "async": true}
    ]
  }
]
```

## 8. New file — `~/.claude/auggie-projects.txt`

Seed content (one CWD per line; comments not supported by `grep -Fxq`):

```
/config/workspace/InfraDocs
/config/workspace/IronClaude
```

Future projects are added by appending a line. Removal demotes the project from full-nag back to one-time-warn mode (or silent if dismiss file exists).

## 9. Test scenarios

| # | Setup | Action | Expected |
|---|---|---|---|
| 1 | Indexed project, fresh session, `source=startup` | First prompt | No auggie line in envelope. (Q1=c excludes startup.) |
| 2 | Indexed project, resumed session, `source=resume` | First prompt | `auggie_first_required=1` line in envelope. Sticky persists. |
| 3 | Same as 2, then auggie tool called | Second prompt | No auggie line. Sticky cleared by PostToolUse. |
| 4 | Indexed project, in-session Δ=10801s | Next prompt | `auggie_first_required=1` line. Sticky persists. |
| 5 | Indexed project, in-session Δ=10799s | Next prompt | No auggie line. (Below threshold.) |
| 6 | Unindexed project (not in `auggie-projects.txt`), resumed session, first time at threshold | First prompt | `auggie_project_not_indexed=1 (...)` line. Dismiss file created. Sticky cleared. |
| 7 | Same as 6, second resumed session same project | First prompt | No auggie line. (Dismiss file exists.) |
| 8 | Auggie NOT in `~/.claude.json:.mcpServers` (uninstalled) | Any prompt, any project | No auggie line. No warn. Silent. |
| 9 | `~/.claude.json` malformed JSON | Any prompt | `jq -e` fails → AUGGIE_REG=false → no auggie line. Fail-open. |
| 10 | Envelope hits 9000-char truncation cascade | Truncation pass | `auggie_*` line preserved; `changed_since_last_turn` and/or RESUMED dropped first per Q6=a. |

## 10. Acceptance criteria

- ✅ Adding the auggie line never breaks an existing envelope (truncation cascade unchanged for non-auggie fields).
- ✅ Uninstalling auggie (removing from `.mcpServers`) silences the feature entirely.
- ✅ A user can dismiss the unindexed warning by inaction — no flag-passing required; the hook auto-dismisses after one warn.
- ✅ A user can promote a project from warn-mode to full-nag by appending a line to `~/.claude/auggie-projects.txt`.
- ✅ A user can re-enable warnings for a dismissed project by `rm ~/.claude/state/auggie-no-warn/<project_key>`.
- ✅ Calling `mcp__auggie__codebase-retrieval` clears the sticky flag for the rest of that session.
- ✅ Hook total latency within existing 3s UserPromptSubmit budget (added ops: 1× `jq`, 1× `grep -Fxq`, 1× file existence check — all sub-ms).

## 11. Open questions for IronClaude-side reviewer

- **OQ-1.** Threshold: 3h (10800s) as written, or 4h (14400s)? Single-line edit at `THRESHOLD_S=` in Diff 1.
- **OQ-2.** Should the warning text in the `auggie_project_not_indexed` line include a literal `auggie index <path>` command, or leave indexing instructions to chat? Currently leaves it to chat — the warning just says "consider indexing."
- **OQ-3.** Should `source=startup` ALSO trigger the flag? Q1=c says no, but the same staleness argument applies. Current proposal honors Q1=c strictly.
- **OQ-4.** The hook reads `~/.claude.json` on every UserPromptSubmit. Should we cache the auggie-registered state in `~/.claude/state/auggie-reg.txt` and refresh it only when `~/.claude.json` mtime changes? Probably premature — `jq -e` on a small JSON file is sub-ms.

## 12. Provenance

- Existing hook source on 2026-05-14: `~/.claude/hooks/freshness-user-prompt.sh` (~153 lines), `~/.claude/hooks/freshness-session-start.sh` (~98 lines). Diffs in this proposal computed against those exact versions.
- MCP registry path verified by `jq 'keys' ~/.claude.json` returning `mcpServers` among top-level keys, and project-level `.mcp.json` listing `auggie` under `mcpServers`.
- All bash/jq syntax pattern-matched from the existing hook code; no fabricated APIs.
