#!/usr/bin/env bash
# Read-only probe: feeds each case to the hook and to its awk scanner alone.
# Arg 1: path to block-bare-python.sh. Prints hook exit status and scanner output.
set -u
HOOK="$1"
SCANNER="$(sed -n "/^read -r -d '' SCANNER <<'AWK'$/,/^AWK$/p" "$HOOK" | sed '1d;$d')"
run() {
    local cmd="$1" payload rc out
    payload="$(jq -cn --arg c "$cmd" '{tool_name:"Bash",tool_input:{command:$c}}')"
    printf '%s' "$payload" | bash "$HOOK" >/dev/null 2>&1; rc=$?
    out="$(printf '%s' "$cmd" | LC_ALL=C awk "$SCANNER" 2>&1)"
    printf 'hook_exit=%s scanner_out=%-8s | %s\n' "$rc" "${out:-<none>}" "$cmd"
}
echo "== finding 1 (ANSI-C) =="
run "\$'\\160ython3' -c 1"
run "\$'\\x70ython3' -c 1"
run "\$'\\u0070ython3' -c 1"
run "\$'python3' -c 1"
echo "== finding 2 (long options) =="
run "timeout --signal TERM 30 python3 x"
run "timeout --kill-after 5 30 python3 x"
run "sudo --user U python3 x"
run "nice --adjustment 5 python3 x"
run "env --unset X python3 x"
run "env --chdir D python3 x"
run "timeout --signal=TERM 30 python3 x"
run "timeout -s TERM 30 python3 x"
echo "== finding 3 ([[ ]]) =="
run "[[ \"\$tool\" =~ ^(python|python3|pip|pip3)\$ ]] && echo matched"
run "[[ -n x ]] && python3 x"
