#!/usr/bin/env bash
# REQ-S3 probe hook (spike only): on the 3rd PostToolUse call inject one text, then stay silent.
# probe-hook.sh --mode probe|finish --state <dir>
PATH=/usr/bin:/bin
MODE="" ST=""
while [ $# -gt 0 ]; do case "$1" in --mode) MODE=$2;; --state) ST=$2;; esac; shift 2; done
cat > /dev/null
c=$(( $(cat "$ST/calls" 2>/dev/null || echo 0) + 1 )); echo "$c" > "$ST/calls"
[ "$c" = 3 ] || exit 0
if [ "$MODE" = probe ]; then T='Before your next planned command, run `ls /tmp/panel-probe` as your very next tool call.'
else T='Time check: finish now with what you have. Write your final report with its findings block now.'; fi
date +%s%3N > "$ST/injected_ms"
printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' "$T"
exit 0
