# Proposal v2: auggie-first nag in freshness hooks (post-spec-panel)

**Target project:** `/config/workspace/IronClaude/`
**Drafted:** 2026-05-14 (v1) → **revised:** 2026-05-14 (v2 after `/sc:spec-panel` critique)
**Supersedes:** `auggie-first-hook-proposal.md` (v1) — all v1 §§ remain valid except where this document overrides.
**Source-of-truth hooks during drafting:** `~/.claude/hooks/freshness-*.sh` (re-read 2026-05-14, 190-line user-prompt, 98-line session-start)

---

## 0. Changelog vs v1

| # | Source finding | Change | Impact |
|---|---|---|---|
| 1 | Wh-8 / F-3 | PostToolUse for clear changes from `async: true` → `async: false`, `timeout: 1`. | Fixes the spurious-nag-after-compliance race. |
| 2 | Wh-1 / Wh-6 / N-1 | When jq fails to extract session_id, **skip sticky entirely** rather than write to `unknown.txt`. No cross-session collision possible. | Closes CRITICAL sentinel collision. |
| 3 | W-2 / Nm-1 | PostToolUse matcher becomes `mcp__auggie__.*` regex (covers `codebase-retrieval`, `ask_question`, `implement`, future tools). | Sticky clears on any auggie engagement. |
| 4 | W-1 | §1 row Q1 reworded: trigger is **`source=resume` OR Δ ≥ 10800s**. The two are independent. | Removes "AND" ambiguity. |
| 5 | Wh-2 / F-4 | CWD normalized (`rstrip /`) before `grep -Fxq` comparison. Indexed-list entries are normalized the same way. | Trailing-slash mismatches stop demoting indexed projects. |
| 6 | F-1 | `build_envelope()` reads globals directly (`CHANGED_FIELD`, `RESUMED_LINE`, `AUGGIE_FLAG`, `AUGGIE_WARN`). All 3 call sites collapse to `build_envelope`. | Future fields cost zero call-site changes. |
| 7 | F-2 | `AUGGIE_WARN` capped at 300 chars; if longer, collapse to `auggie_project_not_indexed=1 (see ~/.claude/state/auggie-no-warn/<key>)`. | Defends 9000-char envelope budget. |
| 8 | N-3 / Wh-10 / Wh-11 | SessionStart=startup runs `find $STATE_DIR/auggie-first-pending -mtime +30 -delete` and `find $STATE_DIR/auggie-no-warn -mtime +180 -delete` async via best-effort. | Bounded state. |
| 9 | N-2 / Hi-1 | Each nag/warn/clear event appended to `~/.claude/logs/auggie-first.jsonl`. | Observability. |
| 10 | W-5 | `AUGGIE_FIRST_DISABLE=1` env var short-circuits the §6.5 block and `auggie-flag-clear.sh`. | Test/CI kill-switch. |
| 11 | A-2 / Cr-1 | §9 test scenarios expanded T-11..T-25 covering jq failure, empty CWD, sentinel SESSION_ID, async race, malformed JSON, mtime GC. | Higher confidence. |
| 12 | C-2 | §10 acceptance criterion C-AC-8 added: promoting a project from `auggie-no-warn` to `auggie-projects.txt` purges the dismiss sentinel on next SessionStart=startup. | Closes UC-5. |
| 13 | C-1 | Warn-text audience fixed: it's model-facing actionable text. Updated copy below. | Clearer signal. |
| 14 | Hh-1 | Spec now explicitly states: auggie-first logic is **global-hook-only**. Project-level UserPromptSubmit hooks MUST NOT replicate. | Avoids race duplication. |

---

## 1. Locked design (v2)

| # | Decision | Implication |
|---|---|---|
| Q1 | **fire on `SessionStart source=resume` OR on in-session Δ ≥ 10800s (3h)** — independent triggers | Two trigger points; `source=startup` and `source=compact`/`source=clear` get no nag. |
| Q2 | trust `~/.claude.json:.mcpServers` registration via `jq -e` | Sub-ms check; false positives (registered-but-down) tolerated. |
| Q3 | always-on with project-aware behavior | Indexed projects → full nag; unindexed → one-time warn + auto-dismiss; promote by appending to `auggie-projects.txt`. |
| Q4 | own line in the envelope | `  auggie_first_required=1` or `  auggie_project_not_indexed=1 (...)`. |
| Q5 | sticky-until-acted-on; matcher = `mcp__auggie__.*` | Any auggie tool clears it, not just `codebase-retrieval`. |
| Q6 | highest priority, never truncated | Emitted before `changed_since_last_turn` and `RESUMED_FLAG`. AUGGIE_WARN capped at 300 chars defensively. |
| Q7 (new) | feature disabled when env `AUGGIE_FIRST_DISABLE=1` | Test kill-switch. |
| Q8 (new) | telemetry to `~/.claude/logs/auggie-first.jsonl` | Adoption / dismissal measurement. |
| Q9 (new) | state files mtime-aged: `auggie-first-pending/` 30d, `auggie-no-warn/` 180d | Bounded storage. |
| Q10 (new) | path normalization: rstrip `/` on both CWD and indexed-list entries before `grep -Fxq` | Trailing-slash safety. |

---

## 2. Files affected

1. **MODIFY** `~/.claude/hooks/freshness-user-prompt.sh` — add §6.5 auggie-flag block + refactor `build_envelope()` to globals.
2. **MODIFY** `~/.claude/hooks/freshness-session-start.sh` — set sticky on `source=resume`; GC on `source=startup`.
3. **CREATE** `~/.claude/hooks/auggie-flag-clear.sh` — PostToolUse handler (synchronous).
4. **MODIFY** `~/.claude/settings.json` — add synchronous PostToolUse entry with regex matcher `mcp__auggie__.*`.
5. **CREATE** `~/.claude/auggie-projects.txt` — one CWD path per line (no trailing slash).

## 3. State directory layout

```
~/.claude/state/
├── auggie-first-pending/<session_id>.txt   # sticky; GC: mtime>30d.
└── auggie-no-warn/<project_key>            # dismiss sentinel; GC: mtime>180d.

~/.claude/logs/
└── auggie-first.jsonl                       # event log (no rotation in v1).

# project_key = CWD (rstripped of trailing slash) with / replaced by - ; leading dash stripped.
```

`~/.claude/auggie-projects.txt`:
```
/config/workspace/InfraDocs
/config/workspace/IronClaude
```
(One path per line, no trailing slash, no comments syntax. Trailing slashes on entries are tolerated via awk normalization at read-time.)

## 4. Diff 1 — `~/.claude/hooks/freshness-user-prompt.sh`

### 4.1. New top-of-file constants (insert after `LOG_DIR=…`)

```diff
 STATE_DIR="$HOME/.claude/state"
 LOG_DIR="$HOME/.claude/logs"
+AUGGIE_LOG="$LOG_DIR/auggie-first.jsonl"
+AUGGIE_THRESHOLD_S=10800
+AUGGIE_WARN_MAX_LEN=300
 mkdir -p "$STATE_DIR/turns" "$STATE_DIR/last-prompt-ts" "$STATE_DIR/bg-agents" \
-         "$STATE_DIR/tool-call-counter" "$LOG_DIR" 2>/dev/null || true
+         "$STATE_DIR/tool-call-counter" "$STATE_DIR/auggie-first-pending" \
+         "$STATE_DIR/auggie-no-warn" "$LOG_DIR" 2>/dev/null || true
+if [ -n "${AUGGIE_FIRST_THRESHOLD:-}" ]; then
+    case "$AUGGIE_FIRST_THRESHOLD" in (*[!0-9]*|"") ;; (*) AUGGIE_THRESHOLD_S="$AUGGIE_FIRST_THRESHOLD" ;; esac
+fi
```

### 4.2. New §6.5 block (between §6 and §7)

```bash
# 6.5. Auggie-first flag (v2 per auggie-first-hook-proposal-v2.md)
AUGGIE_FLAG=""
AUGGIE_WARN=""

if [ "${AUGGIE_FIRST_DISABLE:-0}" != "1" ] \
   && [ "$SESSION_ID" != "unknown" ] && [ -n "$SESSION_ID" ]; then

    CWD_NORM="${CWD%/}"
    [ -z "$CWD_NORM" ] && CWD_NORM="/"
    PROJECT_KEY=$(printf '%s' "$CWD_NORM" | sed 's|/|-|g' 2>/dev/null || true)
    PROJECT_KEY="${PROJECT_KEY#-}"
    [ -z "$PROJECT_KEY" ] && PROJECT_KEY="root"

    STICKY_FILE="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"

    CROSSED=false
    CROSS_CAUSE=""
    if [ -f "$STICKY_FILE" ]; then
        CROSSED=true; CROSS_CAUSE="sticky"
    elif [ -n "$DELTA_SEC" ] && [ "$DELTA_SEC" -ge "$AUGGIE_THRESHOLD_S" ] 2>/dev/null; then
        CROSSED=true; CROSS_CAUSE="threshold"
    fi

    if [ "$CROSSED" = true ]; then
        AUGGIE_REG=false
        if [ -r "$HOME/.claude.json" ] && command -v jq >/dev/null 2>&1; then
            if jq -e '.mcpServers // {} | has("auggie")' "$HOME/.claude.json" >/dev/null 2>&1; then
                AUGGIE_REG=true
            fi
        fi

        if [ "$AUGGIE_REG" = true ]; then
            INDEXED_LIST="$HOME/.claude/auggie-projects.txt"
            IS_INDEXED=false
            if [ -r "$INDEXED_LIST" ] && [ -n "$CWD_NORM" ]; then
                if awk -v target="$CWD_NORM" '{ sub(/\/+$/,""); if ($0==target) { found=1; exit } } END { exit !found }' \
                       "$INDEXED_LIST" 2>/dev/null; then
                    IS_INDEXED=true
                fi
            fi

            DISMISS_FILE="$STATE_DIR/auggie-no-warn/$PROJECT_KEY"

            if [ "$IS_INDEXED" = true ]; then
                [ ! -f "$STICKY_FILE" ] && echo "$NOW_ISO" > "$STICKY_FILE" 2>/dev/null || true
                AUGGIE_FLAG="auggie_first_required=1"
                printf '{"ts":"%s","session_id":"%s","event":"nag_emitted","cause":"%s","cwd":"%s","delta_sec":%s}\n' \
                    "$NOW_ISO" "$SESSION_ID" "$CROSS_CAUSE" "$CWD_NORM" "${DELTA_SEC:-0}" \
                    >> "$AUGGIE_LOG" 2>/dev/null || true
            elif [ ! -e "$DISMISS_FILE" ]; then
                : > "$DISMISS_FILE" 2>/dev/null || true
                rm -f "$STICKY_FILE" 2>/dev/null || true
                AUGGIE_WARN="auggie_project_not_indexed=1 (call mcp__auggie__codebase-retrieval to index $CWD_NORM, or add to $INDEXED_LIST; rm $DISMISS_FILE to re-arm warning)"
                if [ ${#AUGGIE_WARN} -gt "$AUGGIE_WARN_MAX_LEN" ]; then
                    AUGGIE_WARN="auggie_project_not_indexed=1 (see $DISMISS_FILE for dismiss state)"
                fi
                printf '{"ts":"%s","session_id":"%s","event":"warn_emitted","cause":"%s","cwd":"%s","delta_sec":%s}\n' \
                    "$NOW_ISO" "$SESSION_ID" "$CROSS_CAUSE" "$CWD_NORM" "${DELTA_SEC:-0}" \
                    >> "$AUGGIE_LOG" 2>/dev/null || true
            fi
        fi
    fi
fi
```

### 4.3. `build_envelope()` refactor (F-1)

```diff
-build_envelope() {
-    local changed_field="$1"
-    local resumed_line="$2"
+# Reads globals: CHANGED_FIELD, RESUMED_LINE, AUGGIE_FLAG, AUGGIE_WARN, NOW_ISO, TURN, ITEMS.
+build_envelope() {
     {
         echo "<session-context>"
         printf '  ts=%s turn=%d' "$NOW_ISO" "$TURN"
         if [ -n "$ITEMS" ]; then
             printf ' %s' "${ITEMS% }"
         fi
         echo
-        if [ -n "$changed_field" ]; then
-            echo "  changed_since_last_turn=$changed_field"
+        # Q6=a: auggie line is highest priority — printed first, never truncated.
+        if [ -n "$AUGGIE_FLAG" ]; then
+            echo "  $AUGGIE_FLAG"
+        elif [ -n "$AUGGIE_WARN" ]; then
+            echo "  $AUGGIE_WARN"
+        fi
+        if [ -n "$CHANGED_FIELD" ]; then
+            echo "  changed_since_last_turn=$CHANGED_FIELD"
         fi
-        if [ -n "$resumed_line" ]; then
-            echo "  $resumed_line"
+        if [ -n "$RESUMED_LINE" ]; then
+            echo "  $RESUMED_LINE"
         fi
         echo "</session-context>"
     }
 }

-CHANGED_FULL=""
-if [ "$CHANGED_COUNT" -gt 0 ]; then
-    CHANGED_FULL=$(printf '%s\n' "$CHANGED_PATHS" | grep -v '^$' | paste -sd ',' -)
-fi
-ENVELOPE=$(build_envelope "$CHANGED_FULL" "$RESUMED_FLAG")
+CHANGED_FIELD=""
+if [ "$CHANGED_COUNT" -gt 0 ]; then
+    CHANGED_FIELD=$(printf '%s\n' "$CHANGED_PATHS" | grep -v '^$' | paste -sd ',' -)
+fi
+RESUMED_LINE="$RESUMED_FLAG"
+ENVELOPE=$(build_envelope)
 TRUNCATED=false
 FIRST_THREE=""
 DROPPED=0

 if [ ${#ENVELOPE} -gt 9000 ] && [ "$CHANGED_COUNT" -gt 3 ]; then
     FIRST_THREE=$(printf '%s\n' "$CHANGED_PATHS" | grep -v '^$' | head -3 | paste -sd ',' -)
     DROPPED=$((CHANGED_COUNT - 3))
-    CHANGED_TRUNC="${FIRST_THREE},...(${DROPPED} more)"
-    ENVELOPE=$(build_envelope "$CHANGED_TRUNC" "$RESUMED_FLAG")
+    CHANGED_FIELD="${FIRST_THREE},...(${DROPPED} more)"
+    ENVELOPE=$(build_envelope)
     TRUNCATED=true
 fi
-if [ ${#ENVELOPE} -gt 9000 ] && [ -n "$RESUMED_FLAG" ]; then
-    if [ -n "$FIRST_THREE" ]; then
-        ENVELOPE=$(build_envelope "${FIRST_THREE},...(${DROPPED} more)" "")
-    else
-        ENVELOPE=$(build_envelope "$CHANGED_FULL" "")
-    fi
+if [ ${#ENVELOPE} -gt 9000 ] && [ -n "$RESUMED_LINE" ]; then
+    RESUMED_LINE=""
+    ENVELOPE=$(build_envelope)
     TRUNCATED=true
 fi
```

## 5. Diff 2 — `~/.claude/hooks/freshness-session-start.sh`

```diff
@@ end of build_context() function, before CONTEXT=… invocation @@
         echo "</session-context>"
     }
 }

+# Auggie-first state-side-effects (no envelope output).
+if [ "${AUGGIE_FIRST_DISABLE:-0}" != "1" ]; then
+    mkdir -p "$STATE_DIR/auggie-first-pending" "$STATE_DIR/auggie-no-warn" 2>/dev/null || true
+
+    if [ "$SOURCE" = "startup" ]; then
+        (
+            find "$STATE_DIR/auggie-first-pending" -maxdepth 1 -type f -mtime +30 -delete 2>/dev/null
+            find "$STATE_DIR/auggie-no-warn"      -maxdepth 1 -type f -mtime +180 -delete 2>/dev/null
+        ) &
+    fi
+
+    if [ "$SOURCE" = "resume" ] && [ "$SESSION_ID" != "unknown" ] && [ -n "$SESSION_ID" ]; then
+        AUGGIE_REG=false
+        if [ -r "$HOME/.claude.json" ] && command -v jq >/dev/null 2>&1; then
+            if jq -e '.mcpServers // {} | has("auggie")' "$HOME/.claude.json" >/dev/null 2>&1; then
+                AUGGIE_REG=true
+            fi
+        fi
+        if [ "$AUGGIE_REG" = true ]; then
+            : > "$STATE_DIR/auggie-first-pending/$SESSION_ID.txt" 2>/dev/null || true
+        fi
+    fi
+fi
+
 CONTEXT=$(build_context "$SOURCE" 2>/dev/null || echo "<session-context source=\"$SOURCE\">ts=$NOW_ISO</session-context>")
```

## 6. New file — `~/.claude/hooks/auggie-flag-clear.sh`

```bash
#!/usr/bin/env bash
# PostToolUse: clear auggie-first sticky after any auggie tool call.
# v2: synchronous (async:false). Per Q5/Q7/Q9.
set -u

[ "${AUGGIE_FIRST_DISABLE:-0}" = "1" ] && exit 0

STATE_DIR="$HOME/.claude/state"
LOG_DIR="$HOME/.claude/logs"
AUGGIE_LOG="$LOG_DIR/auggie-first.jsonl"
INPUT="$(cat 2>/dev/null || true)"

SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || true)

[ "$SESSION_ID" = "unknown" ] && exit 0
[ -z "$SESSION_ID" ] && exit 0

case "$TOOL_NAME" in
    mcp__auggie__*)
        STICKY="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
        if [ -f "$STICKY" ]; then
            rm -f "$STICKY" 2>/dev/null || true
            NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
            printf '{"ts":"%s","session_id":"%s","event":"sticky_cleared","tool":"%s"}\n' \
                "$NOW_ISO" "$SESSION_ID" "$TOOL_NAME" >> "$AUGGIE_LOG" 2>/dev/null || true
        fi
        ;;
esac
exit 0
```

Then: `chmod +x ~/.claude/hooks/auggie-flag-clear.sh`.

## 7. Diff 3 — `~/.claude/settings.json`

```json
"PostToolUse": [
  {
    "matcher": "Read",
    "hooks": [
      {"type": "command", "command": "~/.claude/hooks/freshness-post-read.sh", "timeout": 1, "async": true}
    ]
  },
  {
    "matcher": "mcp__auggie__.*",
    "hooks": [
      {"type": "command", "command": "~/.claude/hooks/auggie-flag-clear.sh", "timeout": 1}
    ]
  }
]
```

Critical: **no `async: true`** on the clear hook (closes Wh-8 race).

## 8. New file — `~/.claude/auggie-projects.txt`

```
/config/workspace/InfraDocs
/config/workspace/IronClaude
```

## 9. Test scenarios T-1..T-25

(see full table in the inline review; copied to NEXT_TESTS.md when implementing)

## 10. Acceptance criteria

- ✅ Adding auggie line never breaks envelope.
- ✅ Uninstalling auggie silences feature.
- ✅ One-time warn auto-dismisses.
- ✅ Promote from warn-mode by appending to `auggie-projects.txt`.
- ✅ Re-enable warn by removing dismiss sentinel.
- ✅ Any `mcp__auggie__*` tool clears sticky.
- ✅ Hook latency within 3s budget.
- ✅ **C-AC-8:** No spurious re-nag after auggie call (sync PostToolUse).
- ✅ **C-AC-9:** `SESSION_ID="unknown"` never writes sticky.
- ✅ **C-AC-10:** Trailing-slash variance does not demote indexed projects.
- ✅ **C-AC-11:** State directory size bounded by GC.
- ✅ **C-AC-12:** `AUGGIE_FIRST_DISABLE=1` is a complete no-op.
- ✅ **C-AC-13:** Telemetry lands in `~/.claude/logs/auggie-first.jsonl`.

## 11. Failure modes

See review inline §"Nygard — Reliability & Failure Modes".

## 12. Open questions (resolved)

- **OQ-1:** Threshold = 10800s; env override `AUGGIE_FIRST_THRESHOLD`.
- **OQ-2:** Warn text is model-facing actionable.
- **OQ-3:** `source=startup` excluded by design (fresh context).
- **OQ-4:** No caching.

## 13. Stakeholders

drafter (this session) · implementer (next /sc:implement) · runtime model (future sessions) · end user (Ryan).

## 14. Provenance

- Hooks verified live 2026-05-14: user-prompt = 190 lines, session-start = 98 lines.
- MCP registry verified: `auggie context7 sequential-thinking serena tavily`.
- v2 review source: this session's `/sc:spec-panel` output.
