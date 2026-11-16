#!/usr/bin/env bash
# T69: item 4.17 re-check of the nine item 4.6 commands after the fix agent. Read-only on the design; appends to the fix log.
set -u
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
M=docs/designs/orchestrator-mode.md
LOG=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b3/fix-log-cycle1.md
s72=$(grep -n '^### 7.2 Data model' $M | cut -d: -f1); e72=$(( $(grep -n '^### 7.3 Allowlist' $M | cut -d: -f1) - 1 ))
s74=$(grep -n '^### 7.4 JSON schema' $M | cut -d: -f1); e74=$(( $(grep -n '^### 7.5 Report layout' $M | cut -d: -f1) - 1 ))
s11=$(grep -n '^## 11\. ' $M | cut -d: -f1); e11=$(( $(grep -n '^## 12\. ' $M | cut -d: -f1) - 1 ))
s18=$(grep -n '^## 18\. ' $M | cut -d: -f1)
in72(){ sed -n "${s72},${e72}p" $M | grep -cF -- "$1"; }
in74(){ sed -n "${s74},${e74}p" $M | grep -cF -- "$1"; }
in11(){ sed -n "${s11},${e11}p" $M | grep -cF -- "$1"; }
FAILS=0
res(){ if [ "$1" = ok ]; then echo "Check $2: PASS ($3)"; else echo "Check $2: FAIL ($3)"; FAILS=$((FAILS+1)); fi; }
{
echo
echo "## Orchestrator re-check (item 4.6 commands, run after the fix agent returned)"
echo
echo "Design file: \`$M\` ($(wc -l < $M) lines). Section 7.2 is lines $s72-$e72, 7.4 is lines $s74-$e74, section 11 is lines $s11-$e11, section 18 starts at line $s18."
L="origin unknown:"
echo
echo "### Command 1"; echo '```'; echo "\$ grep -n '^## \\|^### ' $M"; grep -n '^## \|^### ' $M | cut -c1-90; echo '```'
n=$(grep -c '^## [0-9]*\. ' $M); [ "$n" = 18 ] && res ok 1 "section map listed; $n numbered ## headings, same 18 sections as before" || res bad 1 "$n numbered ## headings, expected 18"
echo
echo "### Command 2"; echo '```'; echo "\$ grep -n 'outage\\|uncaptured continuation' $M"; grep -n 'outage\|uncaptured continuation' $M | cut -c1-70; echo '```'
{ [ "$(in11 outage)" -ge 1 ] && [ "$(in11 'uncaptured continuation')" -ge 1 ]; } && res ok 2 "both words appear in section 11" || res bad 2 "a word is missing from section 11"
echo
echo "### Command 3"; echo '```'; echo "\$ grep -n 'origin unknown:' $M"; grep -n 'origin unknown:' $M | cut -c1-70; echo '```'
ok=ok; for lit in 'origin unknown: Orca unavailable' 'origin unknown: worker list truncated' 'origin unknown: worker list call failed' 'origin unknown: Run not confirmed' 'origin unknown: tab map unreadable'; do
  [ "$(in72 "$lit")" -ge 1 ] && [ "$(in11 "$lit")" -ge 1 ] || { ok=bad; echo "missing in 7.2 or 11: $lit"; }; done
[ $ok = ok ] && res ok 3 "the five origin unknown literals (the three SPEC FR-010 literals, the tab map unreadable literal and the Run not confirmed literal) are in 7.2 and in section 11" || res bad 3 "a literal is missing from 7.2 or section 11"
echo
echo "### Command 4"; echo '```'; echo "\$ grep -c 'four incomplete cases' $M"; n4=$(grep -c 'four incomplete cases' $M); echo "$n4"; echo '```'
outside=$(grep -n 'four incomplete cases' $M | cut -d: -f1 | awk -v s=$s18 '$1<s' | wc -l)
{ [ "$(in11 'four incomplete cases')" = 0 ] && [ "$outside" = 0 ]; } && res ok 4 "absent from section 11 and from every section before 18; the $n4 remaining hit(s) are in section 18 (the Fix cycle 3 R3-B3 row quotes cycle 2's wording to correct it)" || res bad 4 "section 11 has $(in11 'four incomplete cases') hit(s), $outside hit(s) before section 18"
echo
echo "### Command 5"; echo '```'; echo "\$ grep -n 'orca worker-list <run>' $M"; grep -n 'orca worker-list <run>' $M | cut -c1-70; echo '```'
{ [ "$(in72 'orca worker-list <run>')" -ge 1 ] && [ "$(in74 'orca worker-list <run>')" -ge 1 ]; } && res ok 5 "the source row name appears in 7.2 and in 7.4" || res bad 5 "the name is missing from 7.2 or 7.4"
echo
echo "### Command 6"; echo '```'; echo "\$ grep -c '—' $M"; em=$(grep -c '—' $M); echo "$em"; echo '```'
[ "$em" = 0 ] && res ok 6 "expected 0" || res bad 6 "em-dash count is $em"
echo
echo "### Command 7"; echo '```'; echo "\$ grep -nw 'TODO\\|TBD' $M"; grep -nw 'TODO\|TBD' $M; echo "(no output; grep exit status $(grep -qw 'TODO\|TBD' $M; echo $?); 1 means no match)"; echo '```'
grep -qw 'TODO\|TBD' $M && res bad 7 "a hit exists" || res ok 7 "expected no output"
echo
echo "### Command 8"; echo '```'; echo "\$ grep -n '^Total: 9 deviations.' $M"; grep -n '^Total: 9 deviations.' $M; echo '```'
[ "$(grep -c '^Total: 9 deviations\.' $M)" = 1 ] && res ok 8 "one hit" || res bad 8 "not exactly one hit"
echo
echo "### Command 9"; echo '```'; echo "\$ grep -n '^Total: 23 open items.' $M"; grep -n '^Total: 23 open items.' $M; echo '```'
[ "$(grep -c '^Total: 23 open items\.' $M)" = 1 ] && res ok 9 "one hit" || res bad 9 "not exactly one hit"
echo
echo "Result: $((9-FAILS)) of 9 checks PASS."
} >> "$LOG"
sed -n '/^## Orchestrator re-check/,$p' "$LOG" | grep -E '^Check|^Result|missing in'
