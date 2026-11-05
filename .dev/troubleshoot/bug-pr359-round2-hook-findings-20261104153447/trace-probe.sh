#!/usr/bin/env bash
# Read-only observation (round 2): runs a COPY of the hook's awk scanner with one
# extra print of every chosen command word, plus the real hook's exit status, on
# the three round-2 inputs. The hook file itself is not modified.
set -u
HOOK="$1"
SCANNER="$(sed -n "/^read -r -d '' SCANNER <<'AWK'$/,/^AWK$/p" "$HOOK" | sed '1d;$d')"
TRACE="${SCANNER/need\[o\] = 0; cmd\[o\] = b/need[o] = 0; cmd[o] = b; print \"cmdword=\" b}"
[ "$TRACE" != "$SCANNER" ] || { echo "trace insertion failed"; exit 1; }
while IFS= read -r cmd; do
    printf '== %s\n' "$cmd"
    printf '%s' "$cmd" | LC_ALL=C awk "$TRACE" 2>&1
    jq -cn --arg c "$cmd" '{tool_name:"Bash",tool_input:{command:$c}}' | bash "$HOOK" >/dev/null 2>&1
    printf 'hook_exit=%s\n' "$?"
done <<'CASES'
\[\[ a \]\]; python3 x
< <(printf "") python3 -c 1
echo $(( `python3 -c 1` + 1 ))
CASES
