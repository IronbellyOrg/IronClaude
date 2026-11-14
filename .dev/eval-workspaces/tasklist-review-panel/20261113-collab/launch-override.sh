#!/usr/bin/env bash
# Owner order 2026-11-14: "let them all run, we can make exceptions to the 35% rule".
# Spike 4 measured luna/haiku/sonnet turn times far above the designs' planning values, so k = 0 (no mid-run message fits) on most panels
# and several designs refuse to start a collaboration arm. One session per design (sonnet; at most 2 at once) adds an explicit, owner-authorised
# time-cap exception to its own folder so the collaboration arm runs, and smoke-tests it.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
export REPO C
# design dir | panels the owner wants (design 5 is excluded from sl2 by owner order)
JOBS=("r4-flag-and-adjudicate|EL2 HL2 SL2" "r1-move-radar|el2 hl2 sl2" "r2-idle-shift-sweeper|EL2 HL2 SL2" "r3-axis-flip-challenge|el2 hl2 sl2" "r5-coverage-deflection|el2 hl2")
run_one() {
  IFS='|' read -r DIR PANELS <<<"$1"
  D=$C/$DIR; mkdir -p "$D/override-report"
  for f in session.json session.err session-reply.md; do [ -e "$D/override-report/$f" ] && mv "$D/override-report/$f" "$D/override-report/${f%.*}-prev.${f##*.}"; done
  PROMPT="Work in $D (design folder; read DESIGN.md and IMPLEMENTATION.md first). OWNER DECISION 2026-11-14: the +35% elapsed-time rule may be exceeded. Spike 4 has measured turn times far above the planning values, so the number of messages k (or challenges n) that fit inside the +35% window is 0 on most panels, and the design's launcher refuses or runs a collaboration arm that does nothing. The owner wants the collaboration arm to RUN on these panels: $PANELS (el2 = muse-ember-1.0 + 2x gpt-6-luna; hl2 = claude-haiku-5-5 + 2x luna; sl2 = claude-sonnet-5-5 + 2x luna).

Task: add a minimal, explicit, owner-authorised time-cap exception to this design, inside this folder only:
1. An override (an environment variable such as TIME_CAP_EXCEPTION=<k or n> or a flag, default off) that makes the design use a forced k (or n) of 1 for mid-run designs, or n = 1 for between-phase designs, on any package where the measured value is 0, WITHOUT changing any value computed when the override is off. Keep the finish signal, hang guard and kill timers, but when the override is on, widen them so the extra messages are not cut off: hang guard = max(existing, 3.0 x the measured baseline B_A1 of that package), finish offset adjusted accordingly. State your exact numbers in OVERRIDE.md.
2. Every row produced with the override on must be stamped time_cap_exception: true in its results JSON, and record: baseline B_A1 (from the Spike 4 values file), measured elapsed per package, elapsed/baseline ratio, the forced k or n, and the number of messages or challenges actually delivered per reviewer. The summariser must report these columns and must not mix such rows with rows that obeyed the cap.
3. Re-pin whatever the design pins by sha256 using the design's own documented procedure, so its launcher preflight passes; do not weaken any other check, identity check (observed model must equal requested; NOFALLBACK=1), contamination safeguard, or the blind judge.
4. Add unit tests for the override (on and off) and keep ALL existing tests passing; run the design's full test suite (with the command documented in IMPLEMENTATION.md).
5. Run ONE real smoke row with the override on the primary panel and package named below, exactly as the design documents, so the collaboration path is exercised on real models, and check the 6.4-style smoke conditions the design defines. Smoke package: TASK-WF-design-20261108-041415 on the first panel in your list. Hold at most 3 reviewer sessions at once. Models allowed: muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5; Opus (claude-opus-5-5) only as the blind judge; never Qwen, glm or grok; NOFALLBACK=1.
6. Write $D/OVERRIDE.md: what changed (files and lines), the numbers above, the smoke result, and the exact launch command to run one collaboration row (one panel, all three packages, judged) for EACH panel in your list, and the matching command for the isolated baseline row with the same harness if the design has one.
Constraints: create and edit files only under $D/ (plus scratch under /tmp). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 folder, or any other design's folder. Do not stage, commit or push. Do not run full three-package panel rows other than the one smoke package (the orchestrator runs them). Use uv for Python."
  local S=$(date +%s)
  ( cd "$REPO" && timeout 10800 claude -p --model claude-sonnet-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$D/override-report/session.json" 2>"$D/override-report/session.err"
  local RC=$?
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$D/override-report/session.json" > "$D/override-report/session-reply.md" 2>/dev/null
  echo "END override $DIR rc=$RC wall=$(( $(date +%s)-S ))s override_md=$( [ -s "$D/OVERRIDE.md" ] && echo yes || echo no) $(date -u +%T)"
}
export -f run_one
echo "START $(date -u +%T) max_parallel=2"
printf '%s\n' "${JOBS[@]}" | xargs -P 2 -I{} bash -c 'run_one "{}"'
echo ALLDONE
