#!/usr/bin/env bash
# Read-only observation: runs a COPY of the hook's awk scanner with one extra
# print of every chosen command word (cmd[o] = b at endword), on the three
# symptom inputs. The hook file itself is not modified.
set -u
HOOK="$1"
SCANNER="$(sed -n "/^read -r -d '' SCANNER <<'AWK'$/,/^AWK$/p" "$HOOK" | sed '1d;$d')"
TRACE="${SCANNER/need\[o\] = 0; cmd\[o\] = b/need[o] = 0; cmd[o] = b; print \"cmdword=\" b}"
[ "$TRACE" != "$SCANNER" ] || { echo "trace insertion failed"; exit 1; }
for cmd in "\$'\\160ython3' -c 1" "timeout --signal TERM 30 python3 x" "[[ \"\$tool\" =~ ^(python|python3|pip|pip3)\$ ]] && echo matched"; do
    printf '== %s\n' "$cmd"
    printf '%s' "$cmd" | LC_ALL=C awk "$TRACE" 2>&1
done
