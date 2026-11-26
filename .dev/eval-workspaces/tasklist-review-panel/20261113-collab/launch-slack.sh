#!/usr/bin/env bash
# Owner order 2026-11-14 ("Let them all finish. An extra 30 seconds is fine"): the measured spikes gave k = 0 for most design/panel pairs
# because the receivers' turn times (12-44 s) are far above the 6.4 s the designs assumed. The owner allows 30 s on top of the +35% cap.
# One sonnet session per design (at most 2 at once) adds a SLACK_S term, recomputes the values files from the spike rows already on disk, and re-pins.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
export REPO C
# dir | where the k and finish-offset formulas live | how the values are (re)built from existing spike rows
SPECS=(
"r1-move-radar|tools/values.py: k_for, finish_offset, guard_offset (spike rows el2-c0-r1..3, hl2-c0-r1..3, sl2-c0-r1..3)|tools/values.py spike4 <panel> <rows> refuses to overwrite: write the slack values to values-slack30/<panel>/ instead and make launch.sh read them when PANEL_SLACK_S=30"
"r2-idle-shift-sweeper|py/values.py: finish_at, k, k_r42 (and summarize_arm.py SLO check at 1.35 * B_c)|py/values.py compute/freeze from the Spike 4 rows in runs/ (look at spikes/spike4-values.sh for the exact calls); write the slack values to config/values-slack30/<panel>/ and re-pin config/manifest.json in a copy manifest-slack30.json"
"r3-axis-flip-challenge|r3lib/values.py: compute_k, finish_offset (also compute_n if its box depends on the cap) and r3lib/metrics.py over_135/median_ok|r3_py values-freeze --panel <p> --runs <run ids> (run ids are in spike4-logs/r3-s4-<p>.log lines run_id=...); write to values-slack30/<panel>.json"
"r4-flag-and-adjudicate|lib/values.py: k_of, finish_offset, slowdown_limit (integer-ms arithmetic: keep it) |values.py build/srun/slowdown; rows are runs/s4-a1-<panel>-1..4 (EL2 rows exist; the HL2 and SL2 rows are being rerun right now and exist when this session starts); write to values-slack30/<P>.json, <P>-srun.json, <P>-slowdown.json, and update frozen/pins.sha256 only if you edit a pinned file, then run its sha check"
"r5-coverage-deflection|lib/r5/timing.py: k, finish_offset, slowdown_limit|python -m r5.timing spike4 --panel <p> --rows <a1 rows> --kit-rows <a2 rows> (rows s4-a1-<p>-r1..4 and s4-a2-<p>-r1..2; panels el2 and hl2 only: design 5 never runs on sl2 by owner order); write to config/values-slack30/<p>/ and update config/SHA256SUMS accordingly"
)
run_one() {
  IFS='|' read -r DIR FORMULAS BUILD <<<"$1"
  local D=$C/$DIR; mkdir -p "$D/slack-report"
  local PROMPT="You are changing ONE design's timing rule. Folder: $D (read its DESIGN.md and IMPLEMENTATION.md first). Change ONLY files under $D/.

Owner decision (2026-11-14): the designs' time cap is +35% elapsed (1.35 x B). The spikes measured receiver turn times of 12-44 s, far above the 6.4 s planning value, so k (messages a reviewer may act on) came out 0 on most panels. The owner now allows an extra 30 seconds on top of the cap and wants every reviewer to be allowed to finish. So the cap becomes 1.35 x B + SLACK_S with SLACK_S = 30.

Do exactly this:
1. Introduce SLACK_S in the code that computes the timing: $FORMULAS. Read it from the environment variable PANEL_SLACK_S, default 0 (so the existing pinned tests and fixtures still pass unchanged). Every place the cap 0.35 x B or 1.35 x B is used to derive k, the finish offset, the guard offset, the slowdown limit or an n/box limit gets + SLACK_S (the hang guard 1.5 x B and any other limit not derived from the 35% cap are unchanged). Keep integer-ms arithmetic where the file uses it.
2. Add unit tests for SLACK_S = 30 (at least: k changes for a measured case that was 0 before, finish offset +30, default 0 unchanged) and run the design's FULL unit-test suite (command in IMPLEMENTATION.md; no model calls): it must pass.
3. Recompute the frozen values from the Spike 4 rows already on disk (NO new model sessions): $BUILD. Use PANEL_SLACK_S=30. Do not overwrite or delete the existing values files; write new files as described, keep every hash or pin the design uses consistent for the NEW files, and make the launcher use the slack values when PANEL_SLACK_S=30 and exit 2 with a clear message if PANEL_SLACK_S=30 and the slack values for the panel are missing.
4. Write $D/SLACK.md: what changed (files, lines), the exact environment and command to launch one panel on all three packages for each of ember + 2x luna, sonnet + 2x luna and haiku + 2x luna (collab 1 and PANEL_COLLAB=0) with PANEL_SLACK_S=30, a table of the new k (or n) per panel and package next to the old one, test results with counts, and anything that still refuses to run and why.
Rules: uv only for Python; no model sessions of any kind; do not edit src/, .claude/, .dev/tasks/, the 20261111-a1 folder or another design's folder; do not stage, commit or push. Final reply: 5 lines."
  local S=$(date +%s)
  ( cd "$REPO" && timeout 5400 claude -p --model claude-sonnet-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$D/slack-report/session.json" 2>"$D/slack-report/session.err"
  local RC=$?
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$D/slack-report/session.json" > "$D/slack-report/session-reply.md" 2>/dev/null
  echo "END slack-$DIR rc=$RC wall=$(( $(date +%s)-S ))s slack_md=$( [ -s "$D/SLACK.md" ] && echo yes || echo no) $(date -u +%T)"
}
export -f run_one
echo "START $(date -u +%T) max_parallel=2"
printf '%s\n' "${SPECS[@]}" | xargs -P 2 -I{} bash -c 'run_one "{}"'
echo ALLDONE
