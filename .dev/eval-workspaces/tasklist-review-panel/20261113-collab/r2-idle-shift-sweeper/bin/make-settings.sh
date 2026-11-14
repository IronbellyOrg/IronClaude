#!/usr/bin/env bash
# Writes a per-session --settings JSON with every constant baked into the hook command (R-21).
# make-settings.sh receiver --board B --rid <rid> --recv-index <0|1> --t0-ms <ms> --finish-ms <ms> --k <k> --deal-r <r> --out <file>
# make-settings.sh sweeper  --board B --t0-ms <ms> --finish-ms <ms> --out <file>
set -u -o pipefail
. "$(dirname "$0")/lib/common.sh"
kind=$1; shift
declare -A A
while [ $# -gt 0 ]; do A[${1#--}]=$2; shift 2; done
BASH_BIN=$(command -v bash); JQ_BIN=$(command -v jq)
q() { printf '%q' "$1"; }
case "$kind" in
  receiver)
    cmd="$(q "$BASH_BIN") $(q "$R2_HOME/bin/hooks/receiver-hook.sh") --jq $(q "$JQ_BIN") --board $(q "${A[board]}") --rid ${A[rid]} --recv-index ${A[recv-index]} --t0-ms ${A[t0-ms]} --finish-ms ${A[finish-ms]} --k ${A[k]} --deal-r ${A[deal-r]} --catalogue $(q "$CATALOGUE")";;
  sweeper)
    cmd="$(q "$BASH_BIN") $(q "$R2_HOME/bin/hooks/harvest-hook.sh") --jq $(q "$JQ_BIN") --board $(q "${A[board]}") --t0-ms ${A[t0-ms]} --finish-ms ${A[finish-ms]}";;
  *) echo "usage: make-settings.sh receiver|sweeper ..." >&2; exit 2;;
esac
mkdir -p "$(dirname "${A[out]}")"
jq -n --arg cmd "$cmd" '{hooks:{PostToolUse:[{matcher:"*",hooks:[{type:"command",timeout:5,command:$cmd}]}]}}' > "${A[out]}"
