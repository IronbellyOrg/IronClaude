#!/usr/bin/env bash
# Runs the three proposal sessions, at most 2 at once. Each is its own headless claude -p
# session with its own model (sonnet or haiku only). stdout is the proposal.
set -u
OUT=.dev/brainstorms/20261114-jev-model-validation-hook
mkdir -p "$OUT/proposals" "$OUT/logs"

lens_1='LENS A (architect): layered defence. Make the native Claude Code availableModels and deniedModels layer the floor, and design the PreToolUse hook as the per-stage layer above it, with a launcher-side check for Python launchers. Jev only for the residue.'
lens_2='LENS B (analyzer): chokepoint and evidence. Put enforcement at the smallest number of chokepoints (one shared launch helper plus a thin hook), and make visibility and coverage honest: a coverage matrix of what is seen, not seen and why, with a replay-based offline test plan over real historical claude launches. Decide Jev use by measured need.'
lens_3='LENS C (devops): policy and operations. Focus on the policy file format, scoping, precedence, install and sync, rollout (observe-only then enforce), the override record, failure modes per event, and the implementation plan. Keep the checking logic deterministic.'

run() { # id model lens
  local id=$1 model=$2 lens=$3
  local start end
  start=$(date +%s)
  { cat "$OUT/tools/common-brief.md"; printf '\n%s\n' "$lens"; } \
    | timeout 2400 claude -p --model "$model" --allowedTools Read Grep Glob \
        > "$OUT/proposals/proposal-$id.md" 2> "$OUT/logs/proposal-$id.err"
  local rc=$?
  end=$(date +%s)
  echo "$id model=$model rc=$rc seconds=$((end-start)) bytes=$(wc -c < "$OUT/proposals/proposal-$id.md")" >> "$OUT/logs/proposals.log"
}

: > "$OUT/logs/proposals.log"
run A claude-sonnet-5-5 "$lens_1" &
run B claude-haiku-5-5  "$lens_2" &
wait -n          # start the third as soon as one of the first two finishes
run C claude-sonnet-5-5 "$lens_3" &
wait
echo ALL_DONE >> "$OUT/logs/proposals.log"
