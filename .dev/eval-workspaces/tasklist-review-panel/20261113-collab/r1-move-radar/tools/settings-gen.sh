#!/usr/bin/env bash
# settings-gen.sh <BOARD> <RUN> <RID> <ROLE> <T0_MS> <FINISH_MS> <GUARD_MS> <K> <CP1> <CP2> <ORDER> <PKG> <CLOCK_FILE>
# Prints the per-reviewer --settings JSON (R-21): one PostToolUse handler, matcher "*", timeout 5, every value
# single-quoted and baked into the command string. Refuses (exit 2) a value containing a quote, a $ or a newline.
set -u -o pipefail
[ $# -eq 13 ] || { echo "usage: settings-gen.sh <13 hook arguments>" >&2; exit 2; }
HOOK=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/radar-hook.sh
CMD="bash $HOOK"
for v in "$@"; do
  case $v in *"'"*|*'$'*|*$'\n'*|*'`'*|*'\'*) echo "REFUSE unsafe value: $v" >&2; exit 2;; esac
  CMD="$CMD '$v'"
done
case $CMD in *'$'*) echo "REFUSE \$ in command" >&2; exit 2;; esac
jq -n -c --arg cmd "$CMD" '{hooks: {PostToolUse: [{matcher: "*", hooks: [{type: "command", command: $cmd, timeout: 5}]}]}}'
