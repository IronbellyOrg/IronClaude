#!/bin/bash
# ob-probe.sh <label>: log-only hook for issue 442. Never prints, never blocks, always exits 0.
OB=${OB_DIR:-/tmp/ob}
label=${1:-unlabelled}
input=$(cat 2>/dev/null) || exit 0
{
    tree= p=$PPID n=0
    while [ -n "$p" ] && [ "$p" -gt 1 ] && [ "$n" -lt 12 ]; do
        tree+=$(ps -o pid=,ppid=,pgid=,sid=,lstart=,comm= -p "$p")$'\n'
        p=$(ps -o ppid= -p "$p" | tr -d ' ') n=$((n + 1))
    done
    sid=$(printf '%s' "$input" | jq -r '.session_id // empty')
    level='<no-sid>'
    if [[ $sid =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]]; then
        f="$HOME/.claude/state/launch-level/sessions/$sid"
        if [ -f "$f" ]; then level=$(head -c 64 "$f" | tr -d '\n'); else level='<no-session-file>'; fi
        [ -e "$f.ok" ] && level+=' +ok'
    fi
    jq -cn --arg label "$label" --arg home "${HOME-}" --arg ccd "${CLAUDE_CONFIG_DIR-<unset>}" \
        --arg pid "$$" --arg tree "$tree" --arg at "$(date -u +%FT%T.%3NZ)" --arg level "$level" \
        '{probe_env:{label:$label,at:$at,HOME:$home,CLAUDE_CONFIG_DIR:$ccd,hook_pid:$pid,session_file:$level,ancestors:$tree}}' \
        >> "$OB/logs/$label.env.jsonl"
    printf '%s' "$input" | LAUNCH_LEVEL_PROBE_LOG="$OB/logs/$label.jsonl" "$OB/bin/log-only-probe.sh"
} 2>/dev/null
exit 0
