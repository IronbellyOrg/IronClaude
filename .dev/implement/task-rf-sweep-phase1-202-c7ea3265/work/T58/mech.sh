#!/usr/bin/env bash
# T58: R3-B3 mechanical gate checks. Read-only on the design; writes only the output file.
set -u
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
M=docs/designs/orchestrator-mode.md
OUT=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r3-b3-mechanical.md
total=$(wc -l < $M)
s72=$(grep -n '^### 7.2 Data model' $M | cut -d: -f1); e72=$(grep -n '^### 7.3 Allowlist' $M | cut -d: -f1); e72=$((e72-1))
s74=$(grep -n '^### 7.4 JSON schema' $M | cut -d: -f1); e74=$(grep -n '^### 7.5 Report layout' $M | cut -d: -f1); e74=$((e74-1))
s11=$(grep -n '^## 11\. ' $M | cut -d: -f1); e11=$(grep -n '^## 12\. ' $M | cut -d: -f1); e11=$((e11-1))
in72(){ sed -n "${s72},${e72}p" $M | grep -cF -- "$1"; }
in74(){ sed -n "${s74},${e74}p" $M | grep -cF -- "$1"; }
in11(){ sed -n "${s11},${e11}p" $M | grep -cF -- "$1"; }
FAILS=0
pass(){ echo "- Check $1: PASS - $2"; }
fail(){ echo "- Check $1: FAIL - $2"; FAILS=$((FAILS+1)); }
L1='origin unknown: Orca unavailable'; L2='origin unknown: worker list truncated'; L3='origin unknown: worker list call failed'
{
echo "# R3-B3 mechanical gate checks (item 4.6)"
echo
echo "Design file: \`$M\` ($total lines). Section 7.2 is lines $s72-$e72, section 7.4 is lines $s74-$e74, section 11 is lines $s11-$e11. Run on $(date -u +%Y-%m-%dT%H:%M:%SZ)."
echo
echo '## Command 1: section map'
echo '```'; echo "\$ grep -n '^## \\|^### ' $M"; grep -n '^## \|^### ' $M | cut -c1-90; echo '```'
echo
echo '## Command 2: outage and uncaptured continuation'
echo '```'; echo "\$ grep -n 'outage\\|uncaptured continuation' $M"; grep -n 'outage\|uncaptured continuation' $M | cut -c1-70; echo '```'
echo
echo '## Command 3: the origin unknown literals'
echo '```'; echo "\$ grep -n 'origin unknown:' $M"; grep -n 'origin unknown:' $M | cut -c1-70; echo '```'
echo
n4=$(grep -c 'four incomplete cases' $M)
echo '## Command 4: "four incomplete cases" count'
echo '```'; echo "\$ grep -c 'four incomplete cases' $M"; echo "$n4"; echo '```'
echo
echo '## Command 5: the per-Run source row name'
echo '```'; echo "\$ grep -n 'orca worker-list <run>' $M"; grep -n 'orca worker-list <run>' $M | cut -c1-70; echo '```'
echo
em=$(grep -c '—' $M)
echo '## Command 6: em-dash count'
echo '```'; echo "\$ grep -c '—' $M"; echo "$em"; echo '```'
echo
echo '## Command 7: TODO or TBD'
echo '```'; echo "\$ grep -nw 'TODO\\|TBD' $M"; grep -nw 'TODO\|TBD' $M; echo "(no output expected; grep exit status 1 means no match)"; echo '```'
echo
echo '## Command 8: deviation total'
echo '```'; echo "\$ grep -n '^Total: 9 deviations.' $M"; grep -n '^Total: 9 deviations.' $M; echo '```'
echo
echo '## Command 9: open-item total'
echo '```'; echo "\$ grep -n '^Total: 23 open items.' $M"; grep -n '^Total: 23 open items.' $M; echo '```'
echo
echo '## Pass-rule counts (lines per section range)'
echo
echo '| Text | 7.2 | 7.4 | 11 |'
echo '|---|---|---|---|'
for t in "$L1" "$L2" "$L3" 'orca worker-list <run>' 'outage' 'uncaptured continuation' 'four incomplete cases'; do echo "| \`$t\` | $(in72 "$t") | $(in74 "$t") | $(in11 "$t") |"; done
echo
echo '## Checks'
echo
{ [ "$(in11 outage)" -ge 1 ] && [ "$(in11 'uncaptured continuation')" -ge 1 ]; } && pass 1 '"outage" and "uncaptured continuation" appear in section 11' || fail 1 'a word is missing from section 11'
{ [ "$(in72 "$L1")" -ge 1 ] && [ "$(in72 "$L2")" -ge 1 ] && [ "$(in72 "$L3")" -ge 1 ]; } && pass 2 'the three origin unknown literals are in 7.2' || fail 2 'a literal is missing from 7.2'
{ [ "$(in11 "$L1")" -ge 1 ] && [ "$(in11 "$L2")" -ge 1 ] && [ "$(in11 "$L3")" -ge 1 ]; } && pass 3 'the three origin unknown literals are in section 11' || fail 3 'a literal is missing from section 11'
a=$(grep -n -o -F -e "$L1" -e "$L2" -e "$L3" $M | sed -n "1,3p" | cut -d: -f2- | tr '\n' '|')
s18=$(grep -n '^## 18\. ' $M | cut -d: -f1); outside=$(grep -n 'four incomplete cases' $M | cut -d: -f1 | awk -v s=$s18 '$1<s' | wc -l)
if [ "$(in11 'four incomplete cases')" = 0 ] && [ "$outside" = 0 ]; then pass 4 "\"four incomplete cases\" is absent from section 11 and from every section before 18; the $n4 remaining hit(s) are in section 18 (the Fix cycle 3 R3-B3 row quotes cycle 2's wording to correct it)"; else fail 4 "section 11 has $(in11 'four incomplete cases') hit(s), $outside hit(s) before section 18"; fi
{ [ "$(in72 'orca worker-list <run>')" -ge 1 ] && [ "$(in74 'orca worker-list <run>')" -ge 1 ]; } && pass 5 'the source row name appears in 7.2 and in 7.4' || fail 5 'the name is missing from 7.2 or 7.4'
[ "$em" = 0 ] && pass 6 "em-dash count is 0" || fail 6 "em-dash count is $em"
n7=$(grep -cw 'TODO\|TBD' $M); [ "$n7" = 0 ] && pass 7 "no TODO or TBD" || fail 7 "$n7 hit(s)"
n8=$(grep -c '^Total: 9 deviations\.' $M); [ "$n8" = 1 ] && pass 8 "one 'Total: 9 deviations.' hit" || fail 8 "$n8 hits"
n9=$(grep -c '^Total: 23 open items\.' $M); [ "$n9" = 1 ] && pass 9 "one 'Total: 23 open items.' hit" || fail 9 "$n9 hits"
echo
echo "Result: $((9-FAILS)) of 9 checks PASS."
} > "$OUT"
sed -n '/^## Pass-rule counts/,$p' "$OUT"
