#!/usr/bin/env bash
# Owner order 2026-11-13: 5 parallel /sc:design sessions, one per finalized redesign from the brainstorm
# (.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md). Each design must cover implementation and full testing.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
MR=$REPO/.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md
EVAL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
# n | folder | redesign heading in merged-requirements.md | its section-5 requirements
SPECS=(
"1|r1-move-radar|Redesign 1: Move Radar (F3)|5.7"
"2|r2-idle-shift-sweeper|Redesign 2: Idle-Shift Sweeper (F4)|5.4"
"3|r3-axis-flip-challenge|Redesign 3: Axis-Flip Challenge (F1)|5.3"
"4|r4-flag-and-adjudicate|Redesign 4: Flag-and-Adjudicate (F7)|5.8"
"5|r5-coverage-deflection|Redesign 5: Coverage Deflection (F6)|5.9"
)
run_one() {
  IFS='|' read -r N DIR NAME REQ <<<"$1"
  D=$C/$DIR; mkdir -p "$D/design-report"
  PROMPT="/sc:design \"Implementation and test design for ${NAME}, one of five panel-collaboration redesigns for the tasklist review panel. Source of truth: $MR. Read its sections 1 (theories), 2.0 (shared building blocks), the ${NAME} section, 3 (comparison), 4 (experiment) and 5.1, 5.2, 5.5, 5.6, 5.10 and ${REQ} (requirements). Also read the existing harness it extends: $EVAL/tools/run-reviewer.sh (reviewer launcher), $EVAL/tools/tmp-scripts/judge-one.sh (blind judge), $EVAL/tools/tmp-scripts/anon-*.sh (anonymiser), $EVAL/analysis/merge-b11.sh and b11-launch.sh (merge and launch pattern), $EVAL/combos/SPEC.md (procedure and hard limits), and the superclaude review merge code under src/superclaude/cli/review/. Produce a specification an implementer can build from without further research, covering: (1) every file to create, with path, purpose and interface; all code lives ONLY under $D/ (its own copy of any shared substrate it needs, including the harness fixes H1-H4 of section 5.1 and the board/hook substrate of section 2.0; its own sandbox root /tmp/evalsb-collab-r${N}/; no edits to src/, to $EVAL/ or to any other redesign's folder, so five implementers can work in parallel without conflicts); (2) exact behaviour, message schema, schedules, caps, time guards and contamination safeguards from the source; (3) how the design runs on EACH of the three panels the owner will test: ember + 2x luna, sonnet + 2x luna, and haiku + 2x luna, naming which model plays each role on each panel and stating any adaptation where the source assumes a model the panel lacks; (4) a PANEL_COLLAB=0 switch that runs the same panel isolated with the same harness fixes, as the baseline; (5) one launch script that runs one panel on all three packages (TASK-WF-designSpec-20261107-075614, TASK-WF-makeTheAliasOnly-20261105-051649, TASK-WF-design-20261108-041415), merges each with superclaude review merge, anonymises and judges with the unchanged judge-one.sh, and writes a results row (found /14, real blocking /8, judge blocking, wrong blockers, control found /2, control wrong blockers, output tokens, elapsed per package, collaboration counters) to a JSON file; (6) a full test plan: unit tests (uv run pytest, or bats for shell) for every validator, hook, combiner and guard, a fault-injection test per failure mode, the Gate 0 spikes the design depends on, a one-package smoke test, and acceptance criteria that are pass/fail; (7) risks and open questions. Constraints: models only ember (muse-ember-1.0), luna (gpt-6-luna), haiku (claude-haiku-5-5), sonnet (claude-sonnet-5-5), grok (grok-4.7); never Qwen or glm; Opus only as the blind judge; reviewers read-only; reviewers never see ground truth; NOFALLBACK=1; UV for any Python.\" --type component --format spec --unattended --report-dir $D/design-report --output $D/DESIGN.md"
  local S=$(date +%s)
  ( cd "$REPO" && timeout 3600 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$D/design-report/session.json" 2>"$D/design-report/session.err"
  local RC=$?
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$D/design-report/session.json" > "$D/design-report/session-reply.md" 2>/dev/null
  echo "END design-$N $DIR rc=$RC wall=$(( $(date +%s)-S ))s design_lines=$(wc -l <"$D/DESIGN.md" 2>/dev/null || echo 0)"
}
for s in "${SPECS[@]}"; do run_one "$s" & done
wait; echo ALLDONE
