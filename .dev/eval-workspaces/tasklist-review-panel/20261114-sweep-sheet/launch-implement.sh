#!/usr/bin/env bash
# /sc:implement of the checked plan for Sweep Sheet steps 0 to 13 (owner "build it", 2026-11-14). Sonnet only. One session.
# Resumable: run again and /sc:implement continues from the first unfinished step.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
PLAN=$REPO/.dev/tasks/to-do/TASK-WF-implementHomeCod-20261114-200449/TASK-WF-implementHomeCod-20261114-200449.md
mkdir -p "$SW/implement-report"
PROMPT="/sc:implement $PLAN

Owner constraints for this run: write only under $SW (plus scratch under /tmp) and the plan package's own progress file; do not edit src/, tests/, .claude/ or any other folder; do not stage, commit or push; start no reviewer or judge model (tests use the fake claude); never open any ground-truth*.json; if a QA step needs a model, use claude-sonnet-5-5 or claude-haiku-5-5 only (Opus is reserved for blind scoring)."
S=$(date +%s)
( cd "$REPO" && timeout 14400 claude -p --model claude-sonnet-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$SW/implement-report/session.json" 2>"$SW/implement-report/session.err"
RC=$?
jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$SW/implement-report/session.json" > "$SW/implement-report/session-reply.md" 2>/dev/null
echo "END implement rc=$RC wall=$(( $(date +%s)-S ))s $(date -u +%T)"
