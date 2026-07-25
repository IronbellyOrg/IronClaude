#!/usr/bin/env bash
# bootstrap_scan.sh — fast read-only signal inventory for one project.
# Usage: bootstrap_scan.sh <project-path> [--since 72h]
#
# Outputs JSON to stdout. No network, no writes. Designed to run in <2s
# so the orchestrator can decide which investigators to spawn.

set -euo pipefail

PROJECT="${1:-$(pwd)}"
SINCE_HOURS=72
if [[ "${2:-}" == "--since" ]]; then
  RAW="${3:-72h}"
  case "$RAW" in
    *h) SINCE_HOURS="${RAW%h}" ;;
    *d) SINCE_HOURS=$(( ${RAW%d} * 24 )) ;;
    *)  SINCE_HOURS=72 ;;
  esac
fi

if [[ ! -d "$PROJECT" ]]; then
  echo "{\"error\":\"project path not found\",\"path\":\"$PROJECT\"}" >&2
  exit 2
fi

cd "$PROJECT"
ABS_PROJECT="$(pwd)"
PROJECT_NAME="$(basename "$ABS_PROJECT")"

# Encode cwd for ~/.claude/projects/ lookup: leading slash dropped, then '/' -> '-'.
ENCODED_CWD="-$(echo "$ABS_PROJECT" | sed 's|^/||; s|/|-|g')"
SESSION_DIR="$HOME/.claude/projects/$ENCODED_CWD"

# Helper: print most-recent mtime in a tree as ISO-ish or "" if none.
mtime_of() {
  local dir="$1"
  [[ -d "$dir" ]] || { echo ""; return; }
  find "$dir" -type f -printf '%T@ %p\n' 2>/dev/null \
    | sort -n -r | head -1 \
    | awk '{print $1}' \
    | xargs -I{} date -u -d "@{}" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo ""
}

count_in() {
  local dir="$1"
  [[ -d "$dir" ]] || { echo 0; return; }
  find "$dir" -type f 2>/dev/null | wc -l | tr -d ' '
}

# Find pipeline state files newer than SINCE_HOURS, anywhere under project.
recent_files() {
  local pattern="$1"
  find . -type f -name "$pattern" -mmin "-$(( SINCE_HOURS * 60 ))" 2>/dev/null \
    | head -20 | sed 's|^\./||'
}

# Recent claude session logs for this cwd, last 3 by mtime.
recent_sessions() {
  [[ -d "$SESSION_DIR" ]] || return
  find "$SESSION_DIR" -maxdepth 1 -type f -name "*.jsonl" -printf '%T@ %p\n' 2>/dev/null \
    | sort -n -r | head -3 | awk '{print $2}'
}

# Git state, if repo.
git_state() {
  if [[ -d "$ABS_PROJECT/.git" ]]; then
    local dirty unstaged untracked last_commit
    dirty=$(git -C "$ABS_PROJECT" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    unstaged=$(git -C "$ABS_PROJECT" diff --shortstat 2>/dev/null | tr -d '\n')
    untracked=$(git -C "$ABS_PROJECT" ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
    last_commit=$(git -C "$ABS_PROJECT" log -1 --format='%ci %h %s' 2>/dev/null | head -1)
    printf '{"is_repo":true,"dirty_files":%s,"untracked":%s,"unstaged":"%s","last_commit":"%s"}' \
      "$dirty" "$untracked" "${unstaged//\"/\\\"}" "${last_commit//\"/\\\"}"
  else
    printf '{"is_repo":false}'
  fi
}

# Sprint state: for each .dev/releases/current/* with a manifest, summarize.
sprints_state() {
  local base="$ABS_PROJECT/.dev/releases/current"
  [[ -d "$base" ]] || { echo "[]"; return; }
  local first=1
  printf '['
  for d in "$base"/*/; do
    [[ -d "$d" ]] || continue
    local name exit_code log_tail manifest_status state_sentinel
    name=$(basename "$d")
    exit_code=""
    # Reads .sprint-exitcode from .dev/sprint-state/<release-name>/ (post-FU-001)
    # with fallback to in-release path for legacy archives.
    state_sentinel="$ABS_PROJECT/.dev/sprint-state/$name/.sprint-exitcode"
    if [[ -f "$state_sentinel" ]]; then
      exit_code=$(tr -d '[:space:]' < "$state_sentinel" 2>/dev/null || echo "")
    elif [[ -f "$d/.sprint-exitcode" ]]; then
      exit_code=$(tr -d '[:space:]' < "$d/.sprint-exitcode" 2>/dev/null || echo "")
    fi
    log_tail=""
    if [[ -f "$d/execution-log.jsonl" ]]; then
      log_tail=$(tail -1 "$d/execution-log.jsonl" 2>/dev/null | tr '\n' ' ' | sed 's/"/\\"/g' | cut -c1-300)
    fi
    manifest_status=""
    [[ -f "$d/manifest.json" ]] && manifest_status="present"
    [[ $first -eq 0 ]] && printf ','
    printf '{"name":"%s","exit_code":"%s","manifest":"%s","last_log_event":"%s"}' \
      "$name" "$exit_code" "$manifest_status" "$log_tail"
    first=0
  done
  printf ']'
}

# MDTM task state.
task_state() {
  local todo_dir="$ABS_PROJECT/.dev/tasks/to-do"
  local done_dir="$ABS_PROJECT/.dev/tasks/done"
  local todo_count=$(count_in "$todo_dir")
  local done_count=$(count_in "$done_dir")
  local recent_todo
  recent_todo=$(find "$todo_dir" -maxdepth 2 -name "*.md" -mmin "-$(( SINCE_HOURS * 60 ))" 2>/dev/null | head -5 | sed "s|$ABS_PROJECT/||")
  local recent_todo_json="[]"
  if [[ -n "$recent_todo" ]]; then
    recent_todo_json=$(echo "$recent_todo" | awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')
  fi
  printf '{"todo_count":%s,"done_count":%s,"recent_modified":%s}' \
    "$todo_count" "$done_count" "$recent_todo_json"
}

# Build JSON output.
SESSIONS=$(recent_sessions | awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')
ROADMAP_STATES=$(recent_files ".roadmap-state.json" | awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')
MANIFESTS=$(recent_files "manifest.json" | awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')
EXEC_LOGS=$(recent_files "execution-log.jsonl" | awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')
# recent_files uses find -name so new state_dir paths (.dev/sprint-state/**/.sprint-exitcode) are picked up automatically post-FU-001
EXIT_CODES=$(recent_files ".sprint-exitcode" | awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')

cat <<JSON
{
  "project": "$PROJECT_NAME",
  "path": "$ABS_PROJECT",
  "since_hours": $SINCE_HOURS,
  "session_log_dir": "$SESSION_DIR",
  "session_log_dir_exists": $([[ -d "$SESSION_DIR" ]] && echo true || echo false),
  "recent_sessions": $SESSIONS,
  "has_dev": $([[ -d "$ABS_PROJECT/.dev" ]] && echo true || echo false),
  "has_docs": $([[ -d "$ABS_PROJECT/docs" ]] && echo true || echo false),
  "has_serena": $([[ -d "$ABS_PROJECT/.serena/memories" ]] && echo true || echo false),
  "serena_memory_count": $(count_in "$ABS_PROJECT/.serena/memories"),
  "git": $(git_state),
  "sprints": $(sprints_state),
  "tasks": $(task_state),
  "recent_roadmap_states": $ROADMAP_STATES,
  "recent_manifests": $MANIFESTS,
  "recent_execution_logs": $EXEC_LOGS,
  "recent_exit_codes": $EXIT_CODES,
  "most_recent_mtimes": {
    "dev_releases_current": "$(mtime_of "$ABS_PROJECT/.dev/releases/current")",
    "dev_tasks_to_do":      "$(mtime_of "$ABS_PROJECT/.dev/tasks/to-do")",
    "dev_research":         "$(mtime_of "$ABS_PROJECT/.dev/research")",
    "docs":                 "$(mtime_of "$ABS_PROJECT/docs")",
    "claudedocs":           "$(mtime_of "$ABS_PROJECT/claudedocs")"
  }
}
JSON
