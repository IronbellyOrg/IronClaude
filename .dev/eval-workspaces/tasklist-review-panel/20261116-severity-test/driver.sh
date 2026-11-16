#!/usr/bin/env bash
# Severity-rule test driver: runs the schedule serially, one panel at a time, arms Z0 (harness-z0) and S (harness-s) interleaved.
# Usage (hold one slot): bash ../20261114-collab-process/with-slot.sh sev-test bash driver.sh schedule.tsv
# Own sandbox root (/tmp/evalsb-sev) so it never touches the sandboxes of other sessions; a sandbox with leftovers (uv.lock, .venv)
# is rebuilt before the run. Skips a run whose run.json exists. NOFALLBACK=1 is required.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
SCHED=${1:?schedule file}
[ "${NOFALLBACK:-}" = 1 ] || { echo "E_NOFALLBACK: set NOFALLBACK=1" >&2; exit 2; }
# the harness writes run folders only under /tmp or its own folder (E_NOT_WRITABLE otherwise); results are copied here afterwards
export SW_SB_ROOT=/tmp/evalsb-sev RL_RUNS_ROOT=/tmp/sev-runs
mkdir -p "$RL_RUNS_ROOT"
LOG=/tmp/sev-runs/driver.log
while IFS=$'\t' read -r block arm doc run; do
  case $block in \#* | block) continue ;; esac
  [ -e "$RL_RUNS_ROOT/$run/run.json" ] && { echo "SKIP $run" >>"$LOG"; continue; }
  h=$HERE/../20261116-sev-z0; [ "$arm" = S ] && h=$HERE/../20261116-sev-s
  sbx=$SW_SB_ROOT/$doc
  if [ ! -d "$sbx/repo/.git" ]; then bash "$h/bin/build-sandbox.sh" "$doc" >>"$LOG" 2>&1 || { echo "FAIL sandbox $doc" >>"$LOG"; continue; }
  elif [ -n "$(git -C "$sbx/repo" status --porcelain --ignored)" ]; then
    echo "REBUILD $doc" >>"$LOG"
    case "$(realpath -m -- "$sbx")/" in /tmp/evalsb-sev/?*) ;; *) echo "E_SANDBOX $sbx" >&2; exit 2 ;; esac
    rm -rf -- "$sbx" && bash "$h/bin/build-sandbox.sh" "$doc" >>"$LOG" 2>&1 || { echo "FAIL rebuild $doc" >>"$LOG"; continue; }
  fi
  echo "START $run $(date -u +%T)" >>"$LOG"
  bash "$h/bin/run-panel.sh" --arm Z0 --panel primary --doc "$doc" --replicate "${run##*-r}" --block "$block" --seed 20261121 --run-id "$run" >>"$LOG" 2>&1
  echo "END $run rc=$? $(date -u +%T)" >>"$LOG"
done <"$SCHED"
echo "DRIVER DONE $(date -u +%T)" >>"$LOG"
