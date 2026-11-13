#!/usr/bin/env bash
DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649; DE=TASK-WF-design-20261108-041415
: > /tmp/b5-muse.txt; : > /tmp/b5-other.txt
add() { # combo pkg rid model
  case "$4" in muse-*) echo "$2 $3 $4 $1" >> /tmp/b5-muse.txt;; *) echo "$2 $3 $4 $1" >> /tmp/b5-other.txt;; esac
}
# b4-terra-muse-haiku (t2-1 terra, t2b-1 muse, t4-1 haiku)
for p in $DS $AL $DE; do add b4-terra-muse-haiku "$p" t2-1 gpt-6.1-terra; add b4-terra-muse-haiku "$p" t2b-1 muse-wonder-1.0; add b4-terra-muse-haiku "$p" t4-1 claude-haiku-5-5; done
# b4-terra-luna-muse (t2-1 terra, t2b-1 muse, t4-1 luna)
for p in $DS $AL $DE; do add b4-terra-luna-muse "$p" t2-1 gpt-6.1-terra; add b4-terra-luna-muse "$p" t2b-1 muse-wonder-1.0; add b4-terra-luna-muse "$p" t4-1 gpt-6-luna; done
# b4-muse-luna2 (t2b-1 muse, t4-1 luna, t3-1 luna)
for p in $DS $AL $DE; do add b4-muse-luna2 "$p" t2b-1 muse-wonder-1.0; add b4-muse-luna2 "$p" t4-1 gpt-6-luna; add b4-muse-luna2 "$p" t3-1 gpt-6-luna; done
# b4-sonnet-luna2 (t1b-1 sonnet, t4-1 luna, t3-1 luna)
for p in $DS $AL $DE; do add b4-sonnet-luna2 "$p" t1b-1 claude-sonnet-5-5; add b4-sonnet-luna2 "$p" t4-1 gpt-6-luna; add b4-sonnet-luna2 "$p" t3-1 gpt-6-luna; done
# b4-sonnet-terra (t1b-1 sonnet, t2-1 terra)
for p in $DS $AL $DE; do add b4-sonnet-terra "$p" t1b-1 claude-sonnet-5-5; add b4-sonnet-terra "$p" t2-1 gpt-6.1-terra; done
echo "muse jobs: $(wc -l < /tmp/b5-muse.txt), other jobs: $(wc -l < /tmp/b5-other.txt)"
