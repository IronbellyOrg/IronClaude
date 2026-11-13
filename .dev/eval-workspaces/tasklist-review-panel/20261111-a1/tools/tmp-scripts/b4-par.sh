#!/usr/bin/env bash
# Batch 4 continuation: NO glm, 10 concurrent reviewers max, max 4 concurrent muse runs.
# Job list -> parallel dispatch with a muse semaphore (fd-based) and global semaphore (fd 9).
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
RR="$EVAL/tools/run-reviewer.sh"
DS=TASK-WF-designSpec-20261107-075614
AL=TASK-WF-makeTheAliasOnly-20261105-051649
DE=TASK-WF-design-20261108-041415

JOBS=/tmp/b4-jobs.txt; : > "$JOBS"
have() { [ -f "$EVAL/$1/reviews/combos/$2/$3.md" ] && [ -f "$EVAL/$1/reviews/combos/$2/$3.meta.json" ]; }

# n4-sonnet-src (muse skip-if-done, haiku, sonnet)
for p in $DS $AL $DE; do
  have "$p" n4-sonnet-src t2b-1 || echo "$p t2b-1 muse-wonder-1.0 n4-sonnet-src" >> "$JOBS"
  echo "$p t4-1 claude-haiku-5-5 n4-sonnet-src" >> "$JOBS"
  echo "$p t1b-1 claude-sonnet-5-5 n4-sonnet-src" >> "$JOBS"
done
# n5-sonnet-src (muse, luna, sonnet)
for p in $DS $AL $DE; do
  echo "$p t2b-1 muse-wonder-1.0 n5-sonnet-src" >> "$JOBS"
  echo "$p t4-1 gpt-6-luna n5-sonnet-src" >> "$JOBS"
  echo "$p t1b-1 claude-sonnet-5-5 n5-sonnet-src" >> "$JOBS"
done
# r2-sonnet-src
for p in $DS $AL $DE; do
  echo "$p t4-1 claude-haiku-5-5 r2-sonnet-src" >> "$JOBS"
  echo "$p t3-1 claude-haiku-5-5 r2-sonnet-src" >> "$JOBS"
  echo "$p t4-2 grok-4.7 r2-sonnet-src" >> "$JOBS"
  echo "$p t1b-1 claude-sonnet-5-5 r2-sonnet-src" >> "$JOBS"
done
# r1-haiku-luna2-src
for p in $DS $AL $DE; do
  echo "$p t4-1 claude-haiku-5-5 r1-haiku-luna2-src" >> "$JOBS"
  echo "$p t4-2 gpt-6-luna r1-haiku-luna2-src" >> "$JOBS"
  echo "$p t3-1 gpt-6-luna r1-haiku-luna2-src" >> "$JOBS"
done
# n2-muse-haiku-grok-src
for p in $DS $AL $DE; do
  echo "$p t2b-1 muse-wonder-1.0 n2-muse-haiku-grok-src" >> "$JOBS"
  echo "$p t4-1 claude-haiku-5-5 n2-muse-haiku-grok-src" >> "$JOBS"
  echo "$p t4-2 grok-4.7 n2-muse-haiku-grok-src" >> "$JOBS"
done
# n5-muse-luna-src (glm dropped)
for p in $DS $AL $DE; do
  echo "$p t2b-1 muse-wonder-1.0 n5-muse-luna-src" >> "$JOBS"
  echo "$p t4-1 gpt-6-luna n5-muse-luna-src" >> "$JOBS"
done

TOTAL=$(wc -l < "$JOBS")
echo "jobs queued: $TOTAL (glm excluded per owner)"

# global semaphore: 10 slots; muse semaphore: 4 slots
mkdir -p /tmp/b4-locks
exec 9> /tmp/b4-locks/global.lock
exec 8> /tmp/b4-locks/muse.lock

one() {
  local p="$1" rid="$2" model="$3" C="$4"
  # muse slot
  case "$model" in muse-*) flock 8; while [ "$(pgrep -fc "run-reviewer.sh.*$C.*$rid muse" 2>/dev/null)" -ge 4 ]; do sleep 5; done; flock -u 8;; esac
  echo "START $(date -u +%T) $C/$p/$rid=$model"
  bash "$RR" "$EVAL" "$p" "$rid" "$model" "combos/$C"
  echo "END $(date -u +%T) $C/$p/$rid $(jq -c '[.observed_model,.model_ok,.findings_block]' "$EVAL/$p/reviews/combos/$C/$rid.meta.json" 2>/dev/null)"
}
export -f one 2>/dev/null || true
export EVAL RR

n=0
while read -r p rid model C; do
  n=$((n+1))
  # global cap: wait while 10 reviewer processes live
  while [ "$(pgrep -fc 'tools/run-reviewer.sh' 2>/dev/null)" -ge 10 ]; do sleep 5; done
  one "$p" "$rid" "$model" "$C" &
  sleep 1
done < "$JOBS"
wait
echo ALLDONE_NOGLM
