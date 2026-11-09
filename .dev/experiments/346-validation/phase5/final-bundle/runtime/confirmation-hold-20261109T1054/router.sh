#!/usr/bin/env bash
# Router: the only consumer of the run inbox during the S1 variant re-runs.
# Appends every message as one JSON line to events.jsonl: {t, type, id, dispatch, subject, body, payload}.
# Heartbeats also update beats/<dispatch>.
RUN=run_58af03dbfa92
D=/tmp/impl/s1v
mkdir -p $D/beats
echo $$ > $D/router.pid
while true; do
  r=$(orca orchestration check --run $RUN --wait --timeout-ms 60000 --json 2>/dev/null | jq -c 'select(.result.count != null)' | tail -1)
  [ -z "$r" ] && { sleep 2; continue; }
  d=$(echo "$r" | jq -r '.result.deliveryId // empty')
  echo "$r" | jq -c --arg t "$(date -u +%FT%TZ)" '.result.messages[]? | {t: $t, type, id, subject, body: (.body // ""), payload: (.payload // ""), dispatch: ((.payload // "{}" | (try fromjson catch {}) | .dispatchId) // null)}' >> $D/events.jsonl
  echo "$r" | jq -r '.result.messages[]? | select(.type=="heartbeat") | (.payload // "{}" | (try fromjson catch {}) | .dispatchId // empty)' | while read -r disp; do [ -n "$disp" ] && date -u +%s > "$D/beats/$disp"; done
  [ -n "$d" ] && orca orchestration check --run $RUN --ack "$d" --json >/dev/null 2>&1
done
