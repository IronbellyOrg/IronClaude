#!/usr/bin/env bash
# Wait for an actionable orchestration delivery. Heartbeat-only deliveries are
# acknowledged (nothing to process) and the wait continues. Prints the first
# delivery that holds a worker_done, escalation or question, unacknowledged.
set -u -o pipefail
deadline=$(( $(date +%s) + ${1:-3000} ))
while [ "$(date +%s)" -lt "$deadline" ]; do
  out=$(orca orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 600000 --json 2>&1) || { echo "$out"; exit 1; }
  # The stream holds keepalive objects before the final result object.
  json=$(printf '%s' "$out" | jq -s 'map(select(.result != null)) | last')
  count=$(printf '%s' "$json" | jq -r '.result.count // 0')
  [ "$count" = "0" ] && continue
  # Informational messages (status, heartbeat bodies) go to a log, not a wake-up.
  printf '%s' "$json" | jq -c '.result.messages[] | select(.type != "heartbeat") | {created_at, type, subject, body, payload}' >> "$(dirname "$0")/messages.log"
  actionable=$(printf '%s' "$json" | jq -r '[.result.messages[] | select(.type == "worker_done" or .type == "escalation" or .type == "question")] | length')
  if [ "$actionable" != "0" ]; then printf '%s\n' "$json"; exit 0; fi
  delivery=$(printf '%s' "$json" | jq -r '.result.deliveryId')
  orca orchestration check --ack "$delivery" --json >/dev/null
done
echo '{"timeout":true}'
