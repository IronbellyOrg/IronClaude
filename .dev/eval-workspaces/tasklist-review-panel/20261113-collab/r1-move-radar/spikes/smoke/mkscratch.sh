#!/usr/bin/env bash
# Builds /tmp/collab-r1/r1scratch: a scratch R1 root for the PROVISIONAL collab-1 smoke (planning values, gate file written by hand).
# Nothing here is written into the real R1; the real launch.sh gate (Spike 4, S3) stays closed there.
set -eu -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
X=/tmp/collab-r1/r1scratch
DS=TASK-WF-designSpec-20261107-075614
rm -rf "$X"; mkdir -p "$X/config" "$X/spikes" "$X/values/el2"
cp "$R1"/config/* "$X/config/"; cp "$R1/manifest.json" "$X/manifest.json"
bash "$R1/tools/radar-index.sh" "$DS" --root "$X" --sb /tmp/evalsb-collab-r1 >/dev/null
(cd "$REPO" && uv run python "$R1/tools/values.py" show el2 "$DS" --root "$R1") > "$X/values/el2/$DS.json"
(cd "$X/values/el2" && sha256sum "$DS.json" > "$DS.json.sha256")
jq -n '{"G-BASE":"pass","G-PINS":"pass","S0":"pass","S2":"pass","S3":"missing","Spike 4":"PROVISIONAL-planning-values-not-spike4","REQ-S3":"recorded"}' > "$X/spikes/gate0.json"
ls -R "$X" | head -20
