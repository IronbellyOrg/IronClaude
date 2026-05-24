#!/usr/bin/env bash
# Driver: Opus-vs-Sonnet adversarial-debate eval. (RESTORED 2026-05-22 after wipe)
#
# See README.md for the full design. Two modes:
#   roadmap → /sc:roadmap ... --multi-roadmap --no-validate
#   direct  → /sc:adversarial --source ... --generate roadmap
#
# Usage:
#   ./run-eval.sh pilot
#   ./run-eval.sh direct-remaining
#   ./run-eval.sh direct-all
#   ./run-eval.sh single direct A 4
#
set -euo pipefail

ROOT=/config/workspace/IronClaude
EVAL_DIR="$ROOT/.dev/eval-roadmap"
GROUP_A_SPEC="$ROOT/tests/sc-roadmap/fixtures/sample_spec.md"
GROUP_B_SPEC="$EVAL_DIR/inputs/merged-prd-tdd-user-auth.md"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

run_one() {
  local mode=$1; local group=$2; local n=$3
  local spec
  case "$group" in
    A) spec="$GROUP_A_SPEC" ;;
    B) spec="$GROUP_B_SPEC" ;;
    *) echo "unknown group: $group" >&2; return 2 ;;
  esac

  local out prompt
  case "$mode" in
    roadmap)
      out="$EVAL_DIR/group$group/run$n"
      mkdir -p "$out"
      prompt="/sc:roadmap $spec --multi-roadmap --agents opus,sonnet --depth standard --no-validate --output $out"
      ;;
    direct)
      out="$EVAL_DIR/group$group-direct/run$n"
      mkdir -p "$out"
      prompt="/sc:adversarial --source $spec --generate roadmap --agents opus,sonnet --depth standard --output $out"
      ;;
    *) echo "unknown mode: $mode" >&2; return 2 ;;
  esac

  echo "[$(date -Iseconds)] START mode=$mode group=$group run=$n out=$out" | tee -a "$EVAL_DIR/eval.log"
  echo "  prompt: $prompt" >> "$EVAL_DIR/eval.log"

  local rc=0
  "$CLAUDE_BIN" -p --dangerously-skip-permissions "$prompt" \
    > "$out/session-stdout.log" 2> "$out/session-stderr.log" || rc=$?

  echo "[$(date -Iseconds)] END   mode=$mode group=$group run=$n rc=$rc" | tee -a "$EVAL_DIR/eval.log"
  return $rc
}
export -f run_one
export EVAL_DIR GROUP_A_SPEC GROUP_B_SPEC CLAUDE_BIN

batch_pair() {
  run_one "$1" "$2" "$3" &
  local p1=$!
  run_one "$4" "$5" "$6" &
  local p2=$!
  wait "$p1" || echo "WARN: $1/$2/run$3 exited non-zero"
  wait "$p2" || echo "WARN: $4/$5/run$6 exited non-zero"
}

mode="${1:-pilot}"
case "$mode" in
  pilot)
    batch_pair roadmap A 1 roadmap B 1
    batch_pair direct  A 1 direct  B 1
    ;;
  roadmap-remaining)
    batch_pair roadmap A 2 roadmap B 2
    batch_pair roadmap A 3 roadmap B 3
    batch_pair roadmap A 4 roadmap B 4
    batch_pair roadmap A 5 roadmap B 5
    ;;
  roadmap-all)
    batch_pair roadmap A 1 roadmap B 1
    batch_pair roadmap A 2 roadmap B 2
    batch_pair roadmap A 3 roadmap B 3
    batch_pair roadmap A 4 roadmap B 4
    batch_pair roadmap A 5 roadmap B 5
    ;;
  direct-remaining)
    batch_pair direct A 2 direct B 2
    batch_pair direct A 3 direct B 3
    batch_pair direct A 4 direct B 4
    batch_pair direct A 5 direct B 5
    ;;
  direct-all)
    batch_pair direct A 1 direct B 1
    batch_pair direct A 2 direct B 2
    batch_pair direct A 3 direct B 3
    batch_pair direct A 4 direct B 4
    batch_pair direct A 5 direct B 5
    ;;
  single)
    run_one "${2:?mode}" "${3:?group}" "${4:?run-id}"
    ;;
  *)
    echo "Usage: $0 {pilot|roadmap-remaining|roadmap-all|direct-remaining|direct-all|single MODE GROUP N}" >&2
    exit 2
    ;;
esac
