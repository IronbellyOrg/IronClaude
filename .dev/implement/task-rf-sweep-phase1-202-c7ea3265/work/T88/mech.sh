#!/usr/bin/env bash
# T88: R4 mechanical gate checks (item 5.12). Read-only on the design; writes only the output file.
set -u
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
M=docs/designs/orchestrator-mode.md
OUT=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r4-mechanical.md
mkdir -p "$(dirname "$OUT")"
sec(){ # section number -> "start end"
  local s e
  s=$(grep -n "^## $1\. " $M | cut -d: -f1); e=$(grep -n "^## $(( $1 + 1 ))\. " $M | cut -d: -f1)
  [ -z "$e" ] && e=$(wc -l < $M) || e=$((e-1))
  echo "$s $e"
}
FAILS=0; N=0
chk(){ N=$((N+1)); if [ "$1" = ok ]; then echo "- Check $N: PASS - $2"; else echo "- Check $N: FAIL - $2"; FAILS=$((FAILS+1)); fi; }
{
echo "# R4 mechanical gate checks (item 5.12)"
echo
echo "Design file: \`$M\` ($(wc -l < $M) lines). Run on $(date -u +%Y-%m-%dT%H:%M:%SZ)."
echo
echo '## Command 1: section map'
echo '```'; echo "\$ grep -n '^## \\|^### ' $M"; grep -n '^## \|^### ' $M | cut -c1-90; echo '```'
echo
echo '## Command 2: WC-14 hits'
echo '```'; echo "\$ grep -n 'WC-14' $M"; grep -n 'WC-14' $M | cut -c1-110; echo '```'
echo
echo '## Command 3: WC-16 hits'
echo '```'; echo "\$ grep -n 'WC-16' $M"; grep -n 'WC-16' $M | cut -c1-110; echo '```'
echo
echo '## Command 4: old insertion text'
echo '```'; echo "\$ grep -n 'after line 561\\|519-561' $M"; grep -n 'after line 561\|519-561' $M; echo "(no output expected; grep exit status $(grep -q 'after line 561\|519-561' $M; echo $?))"; echo '```'
echo
echo '## Command 5: cadence phrase'
echo '```'; echo "\$ grep -n 'at most once every 5 minutes' $M"; grep -n 'at most once every 5 minutes' $M | cut -c1-110; echo '```'
echo
echo '## Command 6: step 1.16a hits'
echo '```'; echo "\$ grep -n '1.16a' $M"; grep -n '1.16a' $M | cut -c1-110; echo '```'
echo
em=$(grep -c '—' $M)
echo '## Command 7: em-dash count'
echo '```'; echo "\$ grep -c '—' $M"; echo "$em"; echo '```'
echo
echo '## Command 8: TODO or TBD'
echo '```'; echo "\$ grep -nw 'TODO\\|TBD' $M"; grep -nw 'TODO\|TBD' $M; echo "(no output expected; grep exit status $(grep -qw 'TODO\|TBD' $M; echo $?))"; echo '```'
echo
echo '## Command 9: deviation total'
echo '```'; echo "\$ grep -n '^Total: 9 deviations.' $M"; grep -n '^Total: 9 deviations.' $M; echo '```'
echo
echo '## Command 10: open-item total'
echo '```'; echo "\$ grep -n '^Total: 23 open items.' $M"; grep -n '^Total: 23 open items.' $M; echo '```'
echo
echo '## Checks'
echo
# 1 WC-14 hits: each is the section 8 "on master" sentence, or a section 13 historical name followed by "(WC-16 in this design)"
wr=0; bad=0; while IFS=: read -r ln rest; do
  case "$rest" in *"WC-14 and WC-15 on master"*) ;; *"already has WC-14 and WC-15"*) wr=$((wr+1));; *"WC-14 (WC-16 in this design)"*) ;; *) bad=$((bad+1)); echo "unclassed WC-14 hit at line $ln";; esac
done < <(grep -n 'WC-14' $M)
s13=$(sec 13); s8=$(sec 8)
hist=$(grep -n 'WC-14 (WC-16 in this design)' $M | cut -d: -f1 | awk -v a=${s13% *} -v b=${s13#* } '$1>=a && $1<=b' | wc -l)
mast=$(grep -n 'WC-14 and WC-15 on master' $M | cut -d: -f1 | awk -v a=${s8% *} -v b=${s8#* } '$1>=a && $1<=b' | wc -l)
[ "$bad" = 0 ] && [ "$hist" = 2 ] && [ "$mast" = 1 ] && [ "$wr" = 1 ] && chk ok "every WC-14 hit is a worker rule (keep) hit (the section 8 on-master sentence, $mast, and the section 18 R4 row that names master WC-14, $wr) or one of the two section 13 historical names ($hist), each followed by (WC-16 in this design)" || chk bad "unclassed=$bad historical_in_13=$hist on_master_in_8=$mast"
# 2 WC-16 hits per section
miss=""; for s in 1 8 9 10 12 13 15 16 17; do r=$(sec $s); c=$(grep -n 'WC-16' $M | cut -d: -f1 | awk -v a=${r% *} -v b=${r#* } '$1>=a && $1<=b' | wc -l); [ "$c" -ge 1 ] || miss="$miss $s"; done
[ -z "$miss" ] && chk ok "WC-16 appears in sections 1, 8, 9, 10, 12, 13, 15, 16 and 17" || chk bad "no WC-16 hit in section(s):$miss"
# 3 no 561 insertion text
c=$(grep -c 'after line 561\|519-561' $M); [ "$c" = 0 ] && chk ok "no 'after line 561' or '519-561' text; 'after line 565' appears $(grep -c 'after line 565' $M) times" || chk bad "$c hit(s)"
# 4 cadence phrase in section 8 and the WC-16 block
r=$(sec 8); c8=$(sed -n "${r% *},${r#* }p" $M | grep -c 'at most once every 5 minutes'); blk=$(sed -n '/^### WC-16. Coordinator loop/,/^```$/p' $M | grep -c 'at most once every 5 minutes')
[ "$c8" -ge 1 ] && [ "$blk" -ge 1 ] && chk ok "the cadence phrase is in section 8 ($c8 lines) and in the WC-16 block ($blk)" || chk bad "section 8 lines=$c8, WC-16 block=$blk"
# 5 step 1.16a record-only
w=$(grep -n '1\.16a' $M | grep -ic 'wait for\|follow-up PR\|rebase\|if #422 is open'); [ "$w" = 0 ] && chk ok "no 'wait for', 'follow-up PR', 'rebase' or 'if #422 is open' wording on any 1.16a line" || chk bad "$w line(s) with old wording"
# 6 em dash
[ "$em" = 0 ] && chk ok "em-dash count is 0" || chk bad "em-dash count is $em"
# 7 TODO TBD
n7=$(grep -cw 'TODO\|TBD' $M); [ "$n7" = 0 ] && chk ok "no TODO or TBD" || chk bad "$n7 hit(s)"
# 8 totals
n8=$(grep -c '^Total: 9 deviations\.' $M); [ "$n8" = 1 ] && chk ok "one 'Total: 9 deviations.' hit" || chk bad "$n8 hits"
n9=$(grep -c '^Total: 23 open items\.' $M); [ "$n9" = 1 ] && chk ok "one 'Total: 23 open items.' hit" || chk bad "$n9 hits"
# 9 section map count
s=$(grep -c '^## [0-9]*\. ' $M); [ "$s" = 18 ] && chk ok "18 numbered ## sections, as before" || chk bad "$s numbered sections"
echo
echo "Result: $((N-FAILS)) of $N checks PASS."
} > "$OUT"
sed -n '/^## Checks/,$p' "$OUT"
