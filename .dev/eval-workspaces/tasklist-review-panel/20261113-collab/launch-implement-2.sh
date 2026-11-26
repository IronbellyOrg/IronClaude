#!/usr/bin/env bash
# Restart of the implementation stage (owner order 2026-11-13): the first run (launch-implement.sh) died when the Claude Code
# session ended, with 5 sessions in parallel. This run: at most 2 sessions at once, all five designs, each RESUMED from the
# work and ledger already on disk (nothing is deleted; old session files are kept as session-attempt1.*).
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
MODEL=claude-sonnet-5-5   # standing rule: Opus is for scoring only
export REPO C MODEL
# order: designs that need real work first, then the two that reported success and only need independent verification
DIRS=(r1-move-radar r3-axis-flip-challenge r2-idle-shift-sweeper r4-flag-and-adjudicate r5-coverage-deflection)

run_one() {
  local DIR=$1 D=$C/$1 N
  N=${DIR#r}; N=${N%%-*}
  mkdir -p "$D/implement-report"
  for f in session.json session.err session-reply.md; do [ -e "$D/implement-report/$f" ] && mv "$D/implement-report/$f" "$D/implement-report/${f%.*}-attempt1.${f##*.}"; done
  PROMPT="/sc:implement $D/DESIGN.md --ledger .dev/implement/collab-$DIR/progress.md --resume

RESUME CONTEXT (from the orchestrator): a first implementation session for this design was killed when its host session ended. Its work is on disk: files under $D/, the ledger .dev/implement/collab-$DIR/progress.md, and possibly $D/IMPLEMENTATION.md. Do NOT start over and do not delete anything. First read the ledger, IMPLEMENTATION.md (if present) and the file tree; run the existing tests to see the true state (do not trust earlier claims); then continue from the first task that is not verified complete, fix anything blocked or failing (for example failing lint or tests), and bring every ledger line to complete. If the earlier work already satisfies a task, verify it against the design's acceptance criteria and mark it complete rather than rebuilding it.

Orchestrator constraints (one other session implements a sibling design in the same worktree at the same time):
- Create and edit files ONLY under $D/ (plus .dev/implement/collab-$DIR/, and scratch under /tmp/evalsb-collab-r$N/ and /tmp/collab-r$N/). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder. Do not stage, commit or push.
- Use uv for all Python (uv run pytest, uv run --no-project python -I). Run every unit and fault-injection test the design lists.
- Run the Gate 0 spikes and the one-package smoke test the design lists, but no full panel runs (the orchestrator runs those). Keep at most 3 reviewer or judge model sessions running at once. Models allowed: muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus (claude-opus-5-5) only as the blind judge; never Qwen or glm; NOFALLBACK=1. Reuse spike and smoke results already on disk if they are valid; do not repeat model sessions that already have a recorded result.
- Finish by rewriting $D/IMPLEMENTATION.md so it is true: what was built (file list), how to run one panel on all three packages (exact command for each of ember + 2x luna, sonnet + 2x luna and haiku + 2x luna, plus PANEL_COLLAB=0), test results with counts, spike and smoke results, and every requirement or acceptance criterion that is not met, with the reason."
  local S=$(date +%s)
  ( cd "$REPO" && timeout 10800 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$D/implement-report/session.json" 2>"$D/implement-report/session.err"
  local RC=$?
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$D/implement-report/session.json" > "$D/implement-report/session-reply.md" 2>/dev/null
  echo "END implement-$N $DIR rc=$RC wall=$(( $(date +%s)-S ))s impl_md=$( [ -s "$D/IMPLEMENTATION.md" ] && echo yes || echo no) $(date -u +%T)"
}
export -f run_one
echo "START $(date -u +%T) model=$MODEL max_parallel=2 order=${DIRS[*]}"
printf '%s\n' "${DIRS[@]}" | xargs -P 2 -I{} bash -c 'run_one {}'
echo ALLDONE
