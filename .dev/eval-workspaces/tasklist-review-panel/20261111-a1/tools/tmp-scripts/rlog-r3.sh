#!/bin/bash
# usage: rlog-r3.sh wave step outcome evidence
OUT=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboE-r3
w="$1"; s="$2"; o="$3"; e="$4"
jq -cn --arg w "$w" --arg s "$s" --arg o "$o" --arg e "$e" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '{wave:(if ($w|test("^[0-9]+$")) then ($w|tonumber) else $w end), step:$s, timestamp:$t, outcome:$o, evidence_ref:$e}' >> "$OUT/audit.log"
