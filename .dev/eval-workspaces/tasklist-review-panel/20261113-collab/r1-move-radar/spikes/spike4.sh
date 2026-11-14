#!/usr/bin/env bash
# spike4.sh <panel> [<rep> <rep> <rep> ...]   (DESIGN.md 6.3, Spike 4)
# Runs the collab-0 rows <panel>-c0-r<rep> one after another (default reps 1 2 3; each is a full row of three packages with
# planning values and the 2.0 x planning-B hang guard), then writes values/<panel>/<pkg>.json with tools/values.py.
# values.py refuses fewer than 3 rows and refuses to overwrite an existing values file. Not run by the implementation session:
# it is nine reviewer sessions per rep.
set -u -o pipefail
TOOLS=$(cd "$(dirname "${BASH_SOURCE[0]}")/../tools" && pwd)
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
PANEL=${1:?usage: spike4.sh <panel> [<rep> ...]}; shift
REPS=("$@"); [ ${#REPS[@]} -gt 0 ] || REPS=(1 2 3)
ROWS=()
for r in "${REPS[@]}"; do
  PANEL_COLLAB=0 bash "$TOOLS/launch.sh" "$PANEL" "$r" || echo "spike4: row $PANEL-c0-r$r finished with a failing package" >&2
  ROWS+=("$PANEL-c0-r$r")
done
cd "$REPO" && uv run python "$TOOLS/values.py" spike4 "$PANEL" "${ROWS[@]}"
