#!/bin/bash
# ob-tree.sh <label>: appends this process's ancestor chain to $OB_DIR/logs/tree-<label>.txt. Never prints, exits 0.
OB=${OB_DIR:-/tmp/ob}
label=${1:-unlabelled}
{
    printf '== %s at %s pid=%s\n' "$label" "$(date -u +%FT%T.%3NZ)" "$$"
    p=$$ n=0
    while [ -n "$p" ] && [ "$p" -gt 0 ] && [ "$n" -lt 16 ]; do
        ps -o pid=,ppid=,pgid=,sid=,lstart=,comm= -p "$p"
        [ "$p" -eq 1 ] && break
        p=$(ps -o ppid= -p "$p" | tr -d ' ') n=$((n + 1))
    done
} 2>/dev/null >> "$OB/logs/tree-$label.txt"
exit 0
