#!/usr/bin/env bash
# Batch 6: top-5 muse-wonder rows re-run with muse-ember-1.0 (+ the pending muse-luna2 slot).
# Parallel streams: ember (muse-ember runs) -P4, others -P6 => 10 concurrent, 4 muse-ember max.
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
DS=TASK-WF-designSpec-20261107-075614
AL=TASK-WF-makeTheAliasOnly-20261105-051649
DE=TASK-WF-design-20261108-041415
EMBER=/tmp/b6-ember.txt; OTHER=/tmp/b6-other.txt; : > "$EMBER"; : > "$OTHER"
add() { case "$4" in muse-ember-1.0) echo "$2 $3 $4 $1" >> "$EMBER";; *) echo "$2 $3 $4 $1" >> "$OTHER";; esac }
# 1. r2-sonnet-ember (haiku x2, grok, sonnet, muse-ember)
for p in $DS $AL $DE; do add r2-sonnet-ember "$p" t4-1 claude-haiku-5-5; add r2-sonnet-ember "$p" t3-1 claude-haiku-5-5; add r2-sonnet-ember "$p" t4-2 grok-4.7; add r2-sonnet-ember "$p" t1b-1 claude-sonnet-5-5; add r2-sonnet-ember "$p" t2b-1 muse-ember-1.0; done
# 2. n4-sonnet-ember (muse-ember, haiku, sonnet)
for p in $DS $AL $DE; do add n4-sonnet-ember "$p" t2b-1 muse-ember-1.0; add n4-sonnet-ember "$p" t4-1 claude-haiku-5-5; add n4-sonnet-ember "$p" t1b-1 claude-sonnet-5-5; done
# 3. terra-muse-haiku-ember (terra, muse-ember, haiku)
for p in $DS $AL $DE; do add terra-muse-haiku-ember "$p" t2-1 gpt-6.1-terra; add terra-muse-haiku-ember "$p" t2b-1 muse-ember-1.0; add terra-muse-haiku-ember "$p" t4-1 claude-haiku-5-5; done
# 4. terra-luna-muse-ember (terra, muse-ember, luna)
for p in $DS $AL $DE; do add terra-luna-muse-ember "$p" t2-1 gpt-6.1-terra; add terra-luna-muse-ember "$p" t2b-1 muse-ember-1.0; add terra-luna-muse-ember "$p" t4-1 gpt-6-luna; done
# 5. n5-sonnet-ember (muse-ember, luna, sonnet)
for p in $DS $AL $DE; do add n5-sonnet-ember "$p" t2b-1 muse-ember-1.0; add n5-sonnet-ember "$p" t4-1 gpt-6-luna; add n5-sonnet-ember "$p" t1b-1 claude-sonnet-5-5; done
# 6. b4-muse-ember-luna2 (muse-ember + 2x luna; the pending 7th-shortlist slot)
for p in $DS $AL $DE; do add b4-muse-ember-luna2 "$p" t2b-1 muse-ember-1.0; add b4-muse-ember-luna2 "$p" t4-1 gpt-6-luna; add b4-muse-ember-luna2 "$p" t3-1 gpt-6-luna; done
echo "ember jobs: $(wc -l < $EMBER), other jobs: $(wc -l < $OTHER)"
# Workers reuse /tmp/b4-job-one.sh (run-reviewer.sh now has the fallback ladder).
nohup bash -c 'xargs -P 4 -L 1 bash /tmp/b4-job-one.sh < /tmp/b6-ember.txt >> /tmp/b6-ember.log 2>&1; echo EMBER6_DONE >> /tmp/b6-ember.log' >/dev/null 2>&1 &
nohup bash -c 'xargs -P 6 -L 1 bash /tmp/b4-job-one.sh < /tmp/b6-other.txt >> /tmp/b6-other.log 2>&1; echo OTHER6_DONE >> /tmp/b6-other.log' >/dev/null 2>&1 &
echo "launched batch 6"
