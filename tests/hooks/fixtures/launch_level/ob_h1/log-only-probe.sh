#!/bin/bash
# Log-only probe for a real observation (OB-H1, OB-H2, OB-H3, OB-CTX): appends the hook input as one line to the
# file named by LAUNCH_LEVEL_PROBE_LOG and always exits 0. It never blocks, never writes to stdout or stderr.
input=$(cat 2>/dev/null) || exit 0
[[ -n ${LAUNCH_LEVEL_PROBE_LOG:-} ]] || exit 0
if command -v jq >/dev/null 2>&1 && line=$(printf '%s' "$input" | jq -c . 2>/dev/null) && [[ -n $line ]]; then
    :
else
    line=$(printf '%s' "$input" | tr '\n' ' ')
fi
{ printf '%s\n' "$line" >> "$LAUNCH_LEVEL_PROBE_LOG"; } 2>/dev/null
exit 0
