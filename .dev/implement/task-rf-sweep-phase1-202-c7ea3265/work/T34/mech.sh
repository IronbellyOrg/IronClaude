#!/usr/bin/env bash
# T34: R3-B2 mechanical gate checks. Read-only on the design; writes only the output file.
set -u
cd /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
M=docs/designs/orchestrator-mode.md
OUT=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r3-b2-mechanical.md
total=$(wc -l < $M)
s=$(grep -n '^### 7.2 Data model' $M | cut -d: -f1); e=$(grep -n '^### 7.3 Allowlist' $M | cut -d: -f1); e=$((e-1))
w=$(grep -n '^- A worker, for FR-010' $M | cut -d: -f1)
s11=$(grep -n '^## 11\. ' $M | cut -d: -f1); e11=$(grep -n '^## 12\. ' $M | cut -d: -f1); e11=$((e11-1))
in72(){ sed -n "${s},${e}p" $M | grep -cF -- "$1"; }
in11(){ sed -n "${s11},${e11}p" $M | grep -cF -- "$1"; }
FAILS=0
pass(){ echo "- Check $1: PASS - $2"; }
fail(){ echo "- Check $1: FAIL - $2"; FAILS=$((FAILS+1)); }
{
echo "# R3-B2 mechanical gate checks (item 3.5)"
echo
echo "Design file: \`$M\` ($total lines). Section 7.2 is lines $s-$e, the worker bullet is line $w, section 11 is lines $s11-$e11. Run on $(date -u +%Y-%m-%dT%H:%M:%SZ)."
echo
echo '## Command 1: section map'
echo '```'; echo "\$ grep -n '^## \\|^### ' $M"; grep -n '^## \|^### ' $M | cut -c1-90; echo '```'
echo
echo '## Command 2: note literals'
echo '```'; echo "\$ grep -n 'conflict: one pane session\\|pane moved to a later session\\|joined by pane: latest session' $M"; grep -n 'conflict: one pane session\|pane moved to a later session\|joined by pane: latest session' $M | cut -c1-60; echo '```'
echo
echo '## Command 3: rule wording in rows'
echo '```'; echo "\$ grep -n 'exactly one window holding it\\|several rows matching one pane session' $M"; grep -n 'exactly one window holding it\|several rows matching one pane session' $M | cut -c1-30; echo '```'
echo
em=$(grep -c '—' $M)
echo '## Command 4: em-dash count'
echo '```'; echo "\$ grep -c '—' $M"; echo "$em"; echo '```'
echo
echo '## Command 5: TODO or TBD'
echo '```'; echo "\$ grep -nw 'TODO\\|TBD' $M"; grep -nw 'TODO\|TBD' $M; echo "(no output expected; grep exit status 1 means no match)"; echo '```'
echo
echo '## Command 6: deviation total'
echo '```'; echo "\$ grep -n '^Total: 9 deviations.' $M"; grep -n '^Total: 9 deviations.' $M; echo '```'
echo
echo '## Command 7: open-item total'
echo '```'; echo "\$ grep -n '^Total: 23 open items.' $M"; grep -n '^Total: 23 open items.' $M; echo '```'
echo
echo '## Outcome-to-fixture table (check 2 reads it)'
echo
echo '| Outcome | 7.2 sentence (worker bullet, line '$w') | Fixture in section 11 | Hits in 7.2 | Hits in 11 |'
echo '|---|---|---|---|---|'
echo "| One matching row's window holds the transcript | \"If exactly one matching row's window holds the transcript, the transcript joins that row only and is False with note \`joined by pane: latest session of the pane\`\" | \`test_path_b_pane_reused_joins_later_row_only\` | $(in72 "If exactly one matching row's window holds the transcript") | $(in11 test_path_b_pane_reused_joins_later_row_only) |"
echo "| Two or more matching rows' windows hold it | \"If two or more matching rows' windows hold it, it joins none of them\" (note \`conflict: one pane session matches several Dispatch rows\`) | \`test_path_b_two_windows_hold_session_is_conflict\` and \`test_path_b_shared_boundary_second_is_conflict\` | $(in72 "If two or more matching rows' windows hold it") | $(in11 test_path_b_two_windows_hold_session_is_conflict) and $(in11 test_path_b_shared_boundary_second_is_conflict) |"
echo "| No matching row's window holds it | \"If no matching row's window holds it, every matching row is could not determine with its note\" | \`test_path_b_no_matching_window_holds\` | $(in72 "If no matching row's window holds it") | $(in11 test_path_b_no_matching_window_holds) |"
echo
echo '## Checks'
echo
# (1) one sentence per outcome in 7.2
a=$(in72 "If exactly one matching row's window holds the transcript"); b=$(in72 "If two or more matching rows' windows hold it"); c=$(in72 "If no matching row's window holds it")
[ "$a" = 1 ] && [ "$b" = 1 ] && [ "$c" = 1 ] && pass 1 "7.2 gives exactly one sentence for each of the three outcomes (one holds, two or more hold, none holds)" || fail 1 "outcome sentence counts in 7.2: $a $b $c"
# (2) fixtures
ok=1; for f in test_path_b_pane_reused_joins_later_row_only test_path_b_two_windows_hold_session_is_conflict test_path_b_shared_boundary_second_is_conflict test_path_b_no_matching_window_holds; do [ "$(in11 $f)" -ge 1 ] || ok=0; done
[ $ok = 1 ] && pass 2 "each outcome has a fixture in section 11 (table above)" || fail 2 "a fixture is missing from section 11"
# (3) D9, SP-29, FR-010 agree
d9=$(grep -n '^| D9 ' $M | grep -c 'exactly one window holding it'); sp=$(grep -n '^| SP-29' $M | grep -c 'exactly one window holding it'); fr=$(grep -n '^| FR-010 ' $M | grep -c 'one rule for several rows matching one pane session')
[ "$d9" = 1 ] && [ "$sp" = 1 ] && [ "$fr" = 1 ] && pass 3 "D9, SP-29 and the FR-010 row carry the several-rows wording ($d9 $sp $fr)" || fail 3 "D9 $d9 SP-29 $sp FR-010 $fr"
[ "$em" = 0 ] && pass 4 "em-dash count is 0" || fail 4 "em-dash count is $em"
n5=$(grep -cw 'TODO\|TBD' $M); [ "$n5" = 0 ] && pass 5 "no TODO or TBD" || fail 5 "$n5 hit(s)"
n6=$(grep -c '^Total: 9 deviations\.' $M); [ "$n6" = 1 ] && pass 6 "one 'Total: 9 deviations.' hit" || fail 6 "$n6 hits"
n7=$(grep -c '^Total: 23 open items\.' $M); [ "$n7" = 1 ] && pass 7 "one 'Total: 23 open items.' hit" || fail 7 "$n7 hits"
echo
echo "Result: $((7-FAILS)) of 7 checks PASS."
} > "$OUT"
sed -n '/^## Outcome-to-fixture/,$p' "$OUT"
