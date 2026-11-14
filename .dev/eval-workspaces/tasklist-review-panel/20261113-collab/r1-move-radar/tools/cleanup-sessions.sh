#!/usr/bin/env bash
# cleanup-sessions.sh <row> [--root R1] [--sb SB] [--projects DIR]   (R-46, K-7)
# Deletes only the Claude session files whose ids this row recorded (reviews/<rid>.meta.json session_ids and
# collab.json reviewers.*.session_ids), from <projects>/<encoded SB/<pkg>/repo>/<id>.jsonl. Never a directory.
# Writes runs/<row>/cleanup.log (one DELETED or ABSENT line per id).
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
SB=/tmp/evalsb-collab-r1; PROJ=$HOME/.claude/projects
ROW=${1:?usage: cleanup-sessions.sh <row> [--root R1] [--sb SB] [--projects DIR]}; shift
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --projects) PROJ=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
LOG=$R1/runs/$ROW/cleanup.log; : > "$LOG"
for D in "$R1/runs/$ROW"/*/; do
  PKG=$(basename "$D"); [ -d "$D/reviews" ] || continue
  ENC=$(printf '%s' "$SB/$PKG/repo" | sed 's/[^A-Za-z0-9]/-/g')   # Claude's project-dir encoding of the cwd
  { jq -r '.session_ids[]? // empty' "$D"/reviews/*.meta.json 2>/dev/null
    jq -r '.reviewers[]?.session_ids[]? // empty' "$D/collab.json" 2>/dev/null; } | sort -u | while IFS= read -r ID; do
    case $ID in ''|*/*|*..*) continue;; esac   # an id is a bare name, never a path
    F=$PROJ/$ENC/$ID.jsonl
    if [ -f "$F" ] && [ ! -L "$F" ]; then rm -f -- "$F" && echo "DELETED $F"; else echo "ABSENT $F"; fi
  done >> "$LOG"
done
cat "$LOG"
