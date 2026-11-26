#!/usr/bin/env bash
# Owner order 2026-11-13: 5 parallel sessions, each implementing one redesign's DESIGN.md (committed in fd69a006d).
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
DIRS=(r1-move-radar r2-idle-shift-sweeper r3-axis-flip-challenge r4-flag-and-adjudicate r5-coverage-deflection)
run_one() {
  local N=$1 DIR=$2 D=$C/$2
  mkdir -p "$D/implement-report"
  PROMPT="/sc:implement $D/DESIGN.md --ledger .dev/implement/collab-$DIR/progress.md

Orchestrator constraints for this run (four other sessions implement sibling designs in the same worktree at the same time):
- Create and edit files ONLY under $D/ (plus the ledger folder .dev/implement/collab-$DIR/ and scratch under /tmp/evalsb-collab-r$N/ and /tmp/collab-r$N/). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder. Do not stage, commit or push.
- Use uv for all Python (uv run pytest, uv run --no-project python -I). Run every unit and fault-injection test the design lists and fix failures.
- Run the Gate 0 spikes and the one-package smoke test the design lists, but no full panel runs (the orchestrator runs those). Any step that launches reviewer or judge model sessions must hold the shared lock: wrap it as flock /tmp/collab-gateway.lock <command>, so at most one implementer uses the gateway at a time. Models allowed: muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus (claude-opus-5-5) only as the blind judge; never Qwen or glm; NOFALLBACK=1.
- Finish by writing $D/IMPLEMENTATION.md: what was built (file list), how to run one panel on all three packages (exact command for each of ember + 2x luna, sonnet + 2x luna and haiku + 2x luna, plus PANEL_COLLAB=0), test results with counts, spike and smoke-test results, and every requirement or acceptance criterion that is not met, with the reason."
  local S=$(date +%s)
  ( cd "$REPO" && timeout 10800 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$D/implement-report/session.json" 2>"$D/implement-report/session.err"
  local RC=$?
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$D/implement-report/session.json" > "$D/implement-report/session-reply.md" 2>/dev/null
  echo "END implement-$N $DIR rc=$RC wall=$(( $(date +%s)-S ))s impl_md=$( [ -s "$D/IMPLEMENTATION.md" ] && echo yes || echo no)"
}
i=0; for d in "${DIRS[@]}"; do i=$((i+1)); run_one $i "$d" & done
wait; echo ALLDONE
