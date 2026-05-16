#!/usr/bin/env bash
# SessionStart hook per design §3.1.
# Two branches: startup vs resume. Output wrapped in <session-context source="...">.
# Fail-open per NFR-3: any subcommand failure → omit that field silently.

set -u

STATE_DIR="$HOME/.claude/state"
LOG_DIR="$HOME/.claude/logs"
INPUT="$(cat 2>/dev/null || true)"

SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
SOURCE=$(printf '%s' "$INPUT" | jq -r '.source // "startup"' 2>/dev/null || echo "startup")
CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
[ -z "${CWD:-}" ] && CWD="$PWD"

mkdir -p "$STATE_DIR/turns" "$STATE_DIR/last-prompt-ts" "$STATE_DIR/bg-agents" \
         "$STATE_DIR/tool-call-counter" "$LOG_DIR" 2>/dev/null || true
for d in turns bg-agents tool-call-counter; do
    fp="$STATE_DIR/$d/$SESSION_ID.txt"
    [ -f "$fp" ] || echo "0" > "$fp" 2>/dev/null || true
done

NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
TODAY=$(date '+%Y-%m-%d' 2>/dev/null || true)
PROJECT_BASE=$(basename "$CWD" 2>/dev/null || true)

# Memory index: first line of each ~/.claude/projects/<key>/memory/[a-z]*.md (max 8, trim 80)
MEMORY_KEY=$(printf '%s' "$CWD" | sed 's|/|-|g' 2>/dev/null || true)
MEMORY_DIR="$HOME/.claude/projects/${MEMORY_KEY}/memory"
MEM_INDEX=""
if [ -d "$MEMORY_DIR" ]; then
    MEM_INDEX=$(find "$MEMORY_DIR" -maxdepth 1 -name '[a-z]*.md' -type f 2>/dev/null | head -8 | while read -r f; do
        head -n 1 "$f" 2>/dev/null | cut -c1-80
    done | paste -sd ';' - 2>/dev/null || true)
fi

build_context() {
    local mode="$1"
    {
        echo "<session-context source=\"$mode\">"
        echo "  ts=$NOW_ISO"

        if [ "$mode" = "resume" ]; then
            local lp="$STATE_DIR/last-prompt-ts/$SESSION_ID.txt"
            if [ -f "$lp" ]; then
                local last_ts last_unix now_unix delta
                last_ts=$(cat "$lp" 2>/dev/null || true)
                if [ -n "$last_ts" ]; then
                    last_unix=$(date -d "$last_ts" +%s 2>/dev/null || echo 0)
                    now_unix=$(date +%s 2>/dev/null || echo 0)
                    if [ "$last_unix" -gt 0 ] && [ "$now_unix" -gt 0 ]; then
                        delta=$((now_unix - last_unix))
                        echo "  resumed_after=${delta}s"
                    fi
                fi
            fi
        fi

        echo "  cwd=$CWD"

        if [ "$mode" = "startup" ]; then
            [ -n "$PROJECT_BASE" ] && echo "  project=$PROJECT_BASE"
            [ -n "$TODAY" ] && echo "  date=$TODAY"
        fi

        if [ "$mode" = "resume" ] && (cd "$CWD" 2>/dev/null && git rev-parse --git-dir >/dev/null 2>&1); then
            local branch porcelain commits
            branch=$(cd "$CWD" && git branch --show-current 2>/dev/null || true)
            porcelain=$(cd "$CWD" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo 0)
            commits=$(cd "$CWD" && git log --oneline -5 2>/dev/null | paste -sd ';' - || true)
            [ -n "$branch" ] && echo "  git=$branch status=$porcelain"
            [ -n "$commits" ] && echo "  recent_commits=$commits"
        fi

        [ -n "$MEM_INDEX" ] && echo "  memory_index=$MEM_INDEX"

        if [ "$mode" = "resume" ] && [ -d /opt/docker ]; then
            local df
            df=$(docker system df --format '{{.Type}}:{{.Size}}' 2>/dev/null | paste -sd ',' - || true)
            [ -n "$df" ] && echo "  docker_df=$df"
        fi

        echo "</session-context>"
    }
}

# Auggie-first state-side-effects (no envelope output).
# auggie-first-hook-proposal-v2.1.md: GC on startup, sticky on resume.
if [ "${AUGGIE_FIRST_DISABLE:-0}" != "1" ]; then
    mkdir -p "$STATE_DIR/auggie-first-pending" "$STATE_DIR/auggie-no-warn" 2>/dev/null || true

    if [ "$SOURCE" = "startup" ]; then
        (
            find "$STATE_DIR/auggie-first-pending" -maxdepth 1 -type f -mtime +30 -delete 2>/dev/null
            find "$STATE_DIR/auggie-no-warn"      -maxdepth 1 -type f -mtime +180 -delete 2>/dev/null
        ) &
    fi

    if [ "$SOURCE" = "resume" ] && [ "$SESSION_ID" != "unknown" ] && [ -n "$SESSION_ID" ]; then
        AUGGIE_REG=false
        if [ -r "$HOME/.claude.json" ] && command -v jq >/dev/null 2>&1; then
            if jq -e '.mcpServers // {} | has("auggie")' "$HOME/.claude.json" >/dev/null 2>&1; then
                AUGGIE_REG=true
            fi
        fi
        if [ "$AUGGIE_REG" = true ]; then
            : > "$STATE_DIR/auggie-first-pending/$SESSION_ID.txt" 2>/dev/null || true
        fi
    fi
fi

CONTEXT=$(build_context "$SOURCE" 2>/dev/null || echo "<session-context source=\"$SOURCE\">ts=$NOW_ISO</session-context>")

jq -nc --arg ctx "$CONTEXT" '{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": $ctx
  }
}' 2>/dev/null || printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"<session-context source=\"%s\">ts=%s</session-context>"}}\n' "$SOURCE" "$NOW_ISO"

exit 0
