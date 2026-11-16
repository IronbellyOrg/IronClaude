#!/usr/bin/env bash
# Owner order 2026-11-14 ("build it"): step 1 of IMPLEMENTATION.md section 0: write the checked plan for DESIGN.md steps 0 to 13 with /sc:workflow
# (level 3 of the routing guide). Sonnet only (Opus is reserved for blind scoring). The plan package goes under .dev/tasks/to-do/ as the workflow
# protocol requires; no existing package there is touched. No model runs for scoring are part of this plan.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
mkdir -p "$SW/workflow-report"
PROMPT="/sc:workflow \"Implement $SW/DESIGN.md steps 0 to 13 as ordered in $SW/IMPLEMENTATION.md section 2, writing only under $SW; tests per $SW/TESTING.md. Step 0 is already done: its results are in $SW/results/step0.md (126 review tests pass, search 0.9 s, merge accepts and drops class/probe/src keys). Steps 14 to 16 are out of scope (they need models and owner decisions). Every file is created under $SW; src/, tests/, .claude/ and every existing folder under .dev/tasks/ are not touched, nothing is staged, committed or pushed by the build, and no reviewer or judge model is started (use the fake claude of TESTING F-FAKE). Python through uv. Never open any ground-truth*.json.\" --depth standard --handoff none"
S=$(date +%s)
( cd "$REPO" && timeout 3600 claude -p --model claude-sonnet-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$SW/workflow-report/session.json" 2>"$SW/workflow-report/session.err"
RC=$?
jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$SW/workflow-report/session.json" > "$SW/workflow-report/session-reply.md" 2>/dev/null
echo "END workflow rc=$RC wall=$(( $(date +%s)-S ))s $(date -u +%T)"
