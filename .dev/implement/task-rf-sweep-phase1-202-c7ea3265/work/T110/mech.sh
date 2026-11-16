#!/usr/bin/env bash
# T110: R5 mechanical gate checks (item 6.4). Read-only on the design; writes only the output file.
set -u
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
M=docs/designs/orchestrator-mode.md
OUT=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r5-mechanical.md
mkdir -p "$(dirname "$OUT")"
FAILS=0; N=0
chk(){ N=$((N+1)); if [ "$1" = ok ]; then echo "- Check $N: PASS - $2"; else echo "- Check $N: FAIL - $2"; FAILS=$((FAILS+1)); fi; }
s4=$(grep -n '^## 4\. ' $M | cut -d: -f1); s5=$(grep -n '^## 5\. ' $M | cut -d: -f1)
fc3=$(grep -n '^### Fix cycle 3' $M | cut -d: -f1)
{
echo "# R5 mechanical gate checks (item 6.4)"
echo
echo "Design file: \`$M\` ($(wc -l < $M) lines). Section 4 is lines $s4-$((s5-1)); \`### Fix cycle 3\` is at line $fc3. Run on $(date -u +%Y-%m-%dT%H:%M:%SZ)."
echo
echo '## Command 1: agent-wait hits'
echo '```'; echo "\$ grep -n 'agent-wait' $M"; grep -n 'agent-wait' $M | cut -c1-120; echo '```'
echo
echo '## Command 2: the Fix cycle 3 R5 row'
echo '```'; echo "\$ grep -n '^| R5 | Master' $M"; grep -n '^| R5 | Master' $M | cut -c1-100; echo '```'
echo
em=$(grep -c '—' $M)
echo '## Command 3: em-dash count'
echo '```'; echo "\$ grep -c '—' $M"; echo "$em"; echo '```'
echo
echo '## Command 4: TODO or TBD'
echo '```'; echo "\$ grep -nw 'TODO\\|TBD' $M"; grep -nw 'TODO\|TBD' $M; echo "(no output expected; grep exit status $(grep -qw 'TODO\|TBD' $M; echo $?))"; echo '```'
echo
echo '## Command 5: deviation total'
echo '```'; echo "\$ grep -n '^Total: 10 deviations.' $M"; grep -n '^Total: 10 deviations.' $M; echo '```'
echo
echo '## Command 6: open-item total'
echo '```'; echo "\$ grep -n '^Total: 23 open items.' $M"; grep -n '^Total: 23 open items.' $M; echo '```'
echo
echo '## Command 7: eight or 8 templates'
echo '```'; echo "\$ grep -n 'eight\\|8 templates' $M"; grep -n 'eight\|8 templates' $M | cut -c1-120; echo '```'
echo
echo '## Command 8: the section 4 extension-point sentence'
echo '```'; echo "\$ grep -n 'recorded owner decision (R5, 2026-11-08)' $M"; grep -n 'recorded owner decision (R5, 2026-11-08)' $M | cut -c1-80; echo '```'
echo
echo '## Command 9: FORBIDDEN_TOKENS'
echo '```'; echo "\$ grep -n 'FORBIDDEN_TOKENS = frozenset' $M"; grep -n 'FORBIDDEN_TOKENS = frozenset' $M; echo '```'
echo
echo '## Command 10: the ps templates'
echo '```'; echo "\$ grep -n '(\"worktree\", \"ps\"' $M"; grep -n '("worktree", "ps"' $M; echo '```'
echo
echo '## Checks'
echo
# 1: no agent-wait hit forbids it; the allowing hits are present
bad=0; while IFS=: read -r ln rest; do
  case "$rest" in
    '| GQ-109 |'*|*'("worktree", "ps"'*|'| D10 |'*|*'is allowed by R5 but is not run in step 1.0a'*|'| R5 | Master'*|*'a positive case that both `worktree ps --agent-wait`'*|*'/sc:sweep'*|*'and also for both `worktree ps --agent-wait` templates'*) ;;
    *) bad=$((bad+1)); echo "unclassed agent-wait hit at line $ln";; esac
done < <(grep -n 'agent-wait' $M)
t73=$(grep -c '("worktree", "ps", "--agent-wait"' $M); t11=$(grep -c 'a positive case that both `worktree ps --agent-wait`' $M); t13=$(grep -c '^| D10 .*agent-wait' $M); t151=$(grep -c 'is allowed by R5 but is not run in step 1.0a' $M)
[ "$bad" = 0 ] && [ "$t73" = 2 ] && [ "$t11" = 1 ] && [ "$t13" = 1 ] && [ "$t151" = 1 ] && chk ok "no agent-wait hit forbids the flag; the allowing hits are present: 7.3 templates ($t73), section 11 positive case ($t11), section 13 D10 ($t13), section 15.1 sentence ($t151); the GQ-109, R5 and /sc:sweep lines allow or do not concern the allowlist" || chk bad "unclassed=$bad 7.3=$t73 11=$t11 13=$t13 15.1=$t151"
# 2: section 4 sentence once, in section 4
l=$(grep -n 'recorded owner decision (R5, 2026-11-08)' $M | cut -d: -f1); c=$(echo "$l" | grep -c .)
{ [ "$c" = 1 ] && [ "$l" -ge "$s4" ] && [ "$l" -lt "$s5" ]; } && chk ok "'recorded owner decision (R5, 2026-11-08)' appears once, in section 4 (line $l)" || chk bad "count=$c line=$l"
# 3: FORBIDDEN_TOKENS
f=$(grep 'FORBIDDEN_TOKENS = frozenset' $M); case "$f" in *'frozenset({"--include-remote"})'*) chk ok "FORBIDDEN_TOKENS holds only --include-remote";; *) chk bad "$f";; esac
# 4: R5 row once, after Fix cycle 3
r=$(grep -n '^| R5 | Master' $M | cut -d: -f1); rc=$(echo "$r" | grep -c .)
{ [ "$rc" = 1 ] && [ "$r" -gt "$fc3" ]; } && chk ok "the Fix cycle 3 R5 row exists once (line $r, after line $fc3); the section 9 routing row R5 starts with a different cell" || chk bad "count=$rc line=$r"
# 5-8
[ "$em" = 0 ] && chk ok "em-dash count is 0" || chk bad "em-dash count is $em"
n4=$(grep -cw 'TODO\|TBD' $M); [ "$n4" = 0 ] && chk ok "no TODO or TBD" || chk bad "$n4 hit(s)"
n5=$(grep -c '^Total: 10 deviations\.' $M); [ "$n5" = 1 ] && chk ok "one 'Total: 10 deviations.' hit (D10 added)" || chk bad "$n5 hits"
n6=$(grep -c '^Total: 23 open items\.' $M); [ "$n6" = 1 ] && chk ok "one 'Total: 23 open items.' hit (unchanged)" || chk bad "$n6 hits"
# 9: eight templates
e=$(grep -n 'eight\|8 templates' $M | grep -vc '^[0-9]*:| D10 '); [ "$e" = 0 ] && chk ok "no 'eight' or '8 templates' hit says the allowlist has eight templates (the one hit is the D10 row, which says ten, not eight)" || chk bad "$e hit(s) outside D10"
# 10: ps templates
p=$(grep -c '("worktree", "ps"' $M); [ "$p" = 3 ] && chk ok "3 ps templates in 7.3 (ps --json, ps --agent-wait, ps --agent-wait --json)" || chk bad "$p"
# 11: stale 9
s9=$(grep -c '9 deviations' $M); [ "$s9" = 0 ] && chk ok "no stale '9 deviations' text" || chk bad "$s9 hit(s)"
# 12: the section 3 diagram labels and any "N read templates" or "ALLOWED_ORCA (N)" count
d=$(grep -c 'ALLOWED_ORCA (8)\|[^0-9]8 read templates' $M); dd=$(grep -c 'ALLOWED_ORCA (10)\|10 read templates' $M)
{ [ "$d" = 0 ] && [ "$dd" = 2 ]; } && chk ok "the diagram labels say ALLOWED_ORCA (10) and 10 read templates; no 8-template label is left" || chk bad "stale 8-labels=$d, 10-labels=$dd"
echo
echo "Result: $((N-FAILS)) of $N checks PASS."
} > "$OUT"
sed -n '/^## Checks/,$p' "$OUT"
