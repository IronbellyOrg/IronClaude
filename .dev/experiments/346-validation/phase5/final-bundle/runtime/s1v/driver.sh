#!/usr/bin/env bash
# usage: driver.sh <variant>   (sequence file: /tmp/impl/s1v/seq-<variant>.txt ; state: /tmp/impl/s1v/state-<variant>)
# Sequence lines (tab-separated):
#   W<TAB>label<TAB>brief-file                 dispatch a worker step with the brief, wait for worker_done
#   S<TAB>label<TAB>shell command (run in the variant worktree)
#   P<TAB>label                                pause: stop here (coordinator fills or decides); resume by re-running
# The driver resumes after the last completed line (state file holds the number of completed lines).
# On a worker question/escalation/failure/stall it stops with status in /tmp/impl/s1v/status-<variant>.
set -u
V="$1"; D=/tmp/impl/s1v
WT=/home/coder/workspaces/worktrees/IronClaude/exp346-v-$V
OLD=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
LOG=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase5/s1v-log.md
SEQ=$D/seq-$V.txt; ST=$D/state-$V; STAT=$D/status-$V
[ -f $ST ] || echo 0 > $ST
[ -f $LOG ] || printf '# S1 variant re-runs: dispatch log (one row per step)\n\n| time UTC | variant | step | dispatch | task | note |\n|---|---|---|---|---|---|\n' > $LOG
say() { echo "$(date -u +%FT%TZ) $V: $*" | tee -a $D/driver-$V.log; echo "$*" > $STAT; }
n=$(wc -l < $SEQ)
while true; do
  i=$(cat $ST); [ "$i" -ge "$n" ] && { say "SEQUENCE COMPLETE"; exit 0; }
  line=$(sed -n "$((i+1))p" $SEQ); kind=$(echo "$line" | cut -f1); label=$(echo "$line" | cut -f2); arg=$(echo "$line" | cut -f3-)
  case "$kind" in
    P) echo $((i+1)) > $ST; say "PAUSE at $label"; exit 10;;
    S) say "shell step $label"; ( cd $WT && bash -c "$arg" ) >> $D/driver-$V.log 2>&1 || { say "SHELL STEP FAILED: $label"; exit 11; }
       printf '| %s | %s | %s | (shell) | | %s |\n' "$(date -u +%FT%TZ)" "$V" "$label" "$(echo "$arg" | cut -c1-120)" >> $LOG; echo $((i+1)) > $ST;;
    W) text=$(sed "s#$OLD#$WT#g" "$arg"); cnt=$(grep -o -F "$OLD" "$arg" | wc -l)
       cd /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence
       if [ -n "${RESUME_DISP:-}" ]; then disp=$RESUME_DISP; EVFILTER='select(.type=="worker_done" or .type=="escalation")'; unset RESUME_DISP; say "resuming wait on existing dispatch $disp for $label"
       else
       EVFILTER='select(.type!="heartbeat" and .type!="status")'
       orca orchestration worker-start --spec "$text" --task-title "S1v $V $label" --worktree path:$WT --agent claude --model claude-opus-5-5 --run run_58af03dbfa92 --json > $D/start-$V-$label.json 2>&1
       disp=$(jq -r '.result.dispatchId // "FAILED"' $D/start-$V-$label.json); task=$(jq -r '.result.taskId // "-"' $D/start-$V-$label.json)
       printf '| %s | %s | %s | %s | %s | brief %s sha %s repo-root subst %s |\n' "$(date -u +%FT%TZ)" "$V" "$label" "$disp" "$task" "$(basename $arg)" "$(sha256sum $arg | cut -c1-12)" "$cnt" >> $LOG
       fi
       [ "$disp" = "FAILED" ] && { say "DISPATCH FAILED: $label (see $D/start-$V-$label.json)"; exit 12; }
       say "dispatched $label as $disp"; start=$(date +%s)
       while true; do
         ev=$(grep -F "\"dispatch\":\"$disp\"" $D/events.jsonl 2>/dev/null | jq -c "$EVFILTER" | tail -1)
         if [ -n "$ev" ]; then
           et=$(echo "$ev" | jq -r .type)
           echo "$ev" > $D/last-$V-$label.json
           if [ "$et" = "worker_done" ]; then
             oc=$(echo "$ev" | jq -r '.payload | (try fromjson catch {}) | .outcome // "?"')
             [ "$oc" = "succeeded" ] || { say "WORKER REPORTED $oc: $label ($disp)"; exit 13; }
             echo $((i+1)) > $ST; say "done $label ($disp)"; break
           else say "WORKER $et needs coordinator: $label ($disp)"; exit 14; fi
         fi
         b=$D/beats/$disp; now=$(date +%s); last=$([ -f $b ] && cat $b || echo $start)
         # A resumed wait gets its own timeout window; never fabricate a heartbeat.
         [ "$last" -lt "$start" ] && last=$start
         [ $((now-last)) -gt 1500 ] && { say "STALLED (no heartbeat 25 min): $label ($disp)"; exit 15; }
         sleep 5
       done;;
    *) say "BAD SEQUENCE LINE $((i+1))"; exit 16;;
  esac
done
