#!/usr/bin/env bash
# 10 concurrent total; muse stream capped at 4, non-muse stream gets the rest (6).
# Muse jobs: xargs -P4 over /tmp/b4-muse.txt; others: xargs -P6 over /tmp/b4-other.txt.
nohup bash -c 'xargs -P 4 -L 1 bash /tmp/b4-job-one.sh < /tmp/b4-muse.txt >> /tmp/b4-par-muse.log 2>&1; echo MUSE_STREAM_DONE >> /tmp/b4-par-muse.log' >/dev/null 2>&1 &
nohup bash -c 'xargs -P 6 -L 1 bash /tmp/b4-job-one.sh < /tmp/b4-other.txt >> /tmp/b4-par-other.log 2>&1; echo OTHER_STREAM_DONE >> /tmp/b4-par-other.log' >/dev/null 2>&1 &
wait_for_both() {
  while ! (grep -q MUSE_STREAM_DONE /tmp/b4-par-muse.log 2>/dev/null && grep -q OTHER_STREAM_DONE /tmp/b4-par-other.log 2>/dev/null); do sleep 30; done
  echo ALLDONE_NOGLM_PAR
}
wait_for_both
