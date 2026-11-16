#!/usr/bin/env bash
# T11: R3-B1 mechanical gate checks. Read-only on the design; writes only the output file.
set -u
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
M=docs/designs/orchestrator-mode.md
OUT=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r3-b1-mechanical.md
total=$(wc -l < $M)
# section line ranges taken from the heading map below (computed from `grep -n '^## \|^### '`)
declare -A LO=( [7.1]=353 [7.2]=447 [2.2]=51 [11]=726 [15.1]=868 [17]=965 [18]=997 )
declare -A HI=( [7.1]=446 [7.2]=515 [2.2]=73 [11]=750 [15.1]=901 [17]=996 [18]=$total )
MODEL=(first_record_ts dispatch_started dispatch_ended dispatch_status)
SRC=('dispatch.dispatchedAt' 'dispatch.completedAt' 'dispatch.status')
cnt(){ sed -n "${LO[$1]},${HI[$1]}p" $M | grep -cF -- "$2"; }
{
echo "# R3-B1 mechanical gate checks (item 2.7)"
echo
echo "Design file: \`$M\` ($total lines). Run on $(date -u +%Y-%m-%dT%H:%M:%SZ)."
echo
echo '## Command 1: section map'
echo '```'; echo "\$ grep -n '^## \\|^### ' $M"; grep -n '^## \|^### ' $M | cut -c1-90; echo '```'
echo
echo '## Command 2: model names'
echo '```'; echo "\$ grep -n 'first_record_ts\\|dispatch_started\\|dispatch_ended\\|dispatch_status' $M"; grep -n 'first_record_ts\|dispatch_started\|dispatch_ended\|dispatch_status' $M | cut -c1-110; echo '```'
echo
echo '## Command 3: Orca source names'
echo '```'; echo "\$ grep -n 'dispatch\\.dispatchedAt\\|dispatch\\.completedAt\\|dispatch\\.status' $M"; grep -n 'dispatch\.dispatchedAt\|dispatch\.completedAt\|dispatch\.status' $M | cut -c1-110; echo '```'
echo
em=$(grep -c '—' $M)
echo '## Command 4: em-dash count'
echo '```'; echo "\$ grep -c '—' $M"; echo "$em"; echo '```'
echo
echo '## Command 5: TODO or TBD'
echo '```'; echo "\$ grep -nw 'TODO\\|TBD' $M"; grep -nw 'TODO\|TBD' $M | cut -c1-110; echo "(exit $?)"; echo '```'
echo
echo '## Command 6: deviation total'
echo '```'; echo "\$ grep -n '^Total: 9 deviations.' $M"; grep -n '^Total: 9 deviations.' $M; echo '```'
echo
echo '## Command 7: open-item total'
echo '```'; echo "\$ grep -n '^Total: 23 open items.' $M"; grep -n '^Total: 23 open items.' $M; echo '```'
echo
echo '## Section-by-field matrix (line counts per section range)'
echo
echo '| Section | Lines | first_record_ts | dispatch_started | dispatch_ended | dispatch_status | dispatch.dispatchedAt | dispatch.completedAt | dispatch.status |'
echo '|---|---|---|---|---|---|---|---|---|'
for s in 7.1 7.2 2.2 11 15.1 17 18; do
  row="| $s | ${LO[$s]}-${HI[$s]} |"
  for f in "${MODEL[@]}" "${SRC[@]}"; do row="$row $(cnt $s "$f") |"; done
  echo "$row"
done
echo
echo '## Checks'
echo
pass(){ echo "- Check $1: PASS - $2"; }
fail(){ echo "- Check $1: FAIL - $2"; FAILS=$((FAILS+1)); }
FAILS=0
# (1) per-section rule
ok1=1; why=""
for f in "${MODEL[@]}"; do for s in 7.2 2.2 18; do [ "$(cnt $s $f)" -ge 1 ] || { ok1=0; why="$why $s lacks $f;"; }; done; done
[ "$(cnt 7.1 first_record_ts)" -ge 1 ] || { ok1=0; why="$why 7.1 lacks first_record_ts;"; }
for f in first_record_ts dispatch_started dispatch_ended dispatch_status; do [ "$(cnt 11 $f)" -ge 1 ] || { ok1=0; why="$why 11 lacks $f;"; }; done
for s in 15.1 17; do for f in "${SRC[@]}"; do [ "$(cnt $s "$f")" -ge 1 ] || { ok1=0; why="$why $s lacks $f;"; }; done; done
[ $ok1 = 1 ] && pass 1 "the matrix meets the per-section rule" || fail 1 "$why"
# (2) worker bullet window rule
wl=$(grep -n '^- A worker, for FR-010' $M | cut -d: -f1)
ok2=1; for f in "${MODEL[@]}"; do sed -n "${wl}p" $M | grep -qF -- "$f" || ok2=0; done
[ $ok2 = 1 ] && pass 2 "worker bullet (line $wl) names all four model fields" || fail 2 "worker bullet (line $wl) lacks a model field"
# (3) GQ-103(3) row
g=$(grep -n '^| GQ-103(3)' $M | cut -d: -f1)
ok3=1; for f in dispatch_started dispatch_ended dispatch_status first_record_ts; do sed -n "${g}p" $M | grep -qF -- "$f" || ok3=0; done
[ $ok3 = 1 ] && pass 3 "GQ-103(3) row (line $g) lists dispatch_started, dispatch_ended, dispatch_status and first_record_ts" || fail 3 "GQ-103(3) row (line $g) lacks a field"
[ "$em" = 0 ] && pass 4 "em-dash count is 0" || fail 4 "em-dash count is $em"
n5=$(grep -cw 'TODO\|TBD' $M)
[ "$n5" = 0 ] && pass 5 "no TODO or TBD" || fail 5 "$n5 hit(s)"
n6=$(grep -c '^Total: 9 deviations\.' $M); [ "$n6" = 1 ] && pass 6 "one 'Total: 9 deviations.' hit" || fail 6 "$n6 hits"
n7=$(grep -c '^Total: 23 open items\.' $M); [ "$n7" = 1 ] && pass 7 "one 'Total: 23 open items.' hit" || fail 7 "$n7 hits"
echo
echo "Result: $((7-FAILS)) of 7 checks PASS."
} > "$OUT"
sed -n '/^## Section-by-field/,$p' "$OUT"
