#!/usr/bin/env bash
# Wait on the run until a worker_done/question/escalation arrives; heartbeats are acked silently.
# usage: waiter.sh <out-file> [max-seconds]
out="$1"; max="${2:-560}"; start=$(date +%s)
RUN=run_58af03dbfa92
while true; do
  left=$(( max - ($(date +%s) - start) ))
  [ "$left" -le 5 ] && { echo '{"timeout":true}' > "$out"; exit 0; }
  r=$(orca orchestration check --run $RUN --wait --types "worker_done,escalation,question" --timeout-ms $(( left * 1000 )) --json 2>/dev/null | jq -c 'select(.result.count != null)' | tail -1)
  [ -z "$r" ] && continue
  n=$(echo "$r" | jq '[.result.messages[] | select(.type != "heartbeat")] | length')
  d=$(echo "$r" | jq -r '.result.deliveryId // empty')
  if [ "${n:-0}" -gt 0 ]; then
    echo "$r" > "$out"
    exit 0
  fi
  [ -n "$d" ] && orca orchestration check --run $RUN --ack "$d" --json >/dev/null 2>&1
done
