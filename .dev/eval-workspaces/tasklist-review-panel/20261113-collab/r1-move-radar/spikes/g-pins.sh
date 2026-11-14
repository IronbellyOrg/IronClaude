#!/usr/bin/env bash
# G-PINS (R-07): sha256 pins of catalogue, brief, judge-one.sh; catalogue ground-truth check -> spikes/g-cat.json
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=${1:-$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar}
A1DIR=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
M=$R1/manifest.json
[ -f "$M" ] || { echo "FAIL run g-base.sh first" >&2; exit 1; }
cd "$R1" && sha256sum -c --quiet config/catalogue.sha256 || { echo "FAIL catalogue.json differs from config/catalogue.sha256" >&2; exit 1; }
CAT=$(sha256sum "$R1/config/catalogue.json" | cut -d' ' -f1)
BRIEF=$(sha256sum "$R1/config/brief.txt" | cut -d' ' -f1)
JUDGE=$(sha256sum "$A1DIR/tools/tmp-scripts/judge-one.sh" | cut -d' ' -f1)
jq --arg c "$CAT" --arg b "$BRIEF" --arg j "$JUDGE" '.catalogue_sha256=$c|.brief_sha256=$b|.judge_one_sha256=$j' "$M" > "$M.tmp" && mv "$M.tmp" "$M"
cd "$REPO" && uv run python "$R1/tools/collab_summary.py" catcheck "$R1/config/catalogue.json" "$A1DIR"/TASK-WF-*/ground-truth.json > "$R1/spikes/g-cat.json"
jq -c . "$R1/spikes/g-cat.json"
