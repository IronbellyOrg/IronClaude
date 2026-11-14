#!/usr/bin/env bash
# G-BASE (H3): base commit per package -> manifest.json base_commits. Usage: g-base.sh [<R1 root>]
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=${1:-$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar}
M=$R1/manifest.json
declare -A FALLBACK=(
  [TASK-WF-designSpec-20261107-075614]=0e486ab8d0eb24c6f2738ce1f895cc16755b26c1
  [TASK-WF-makeTheAliasOnly-20261105-051649]=38eb3c58afe6988b51060ae14117172869ea4c1e
  [TASK-WF-design-20261108-041415]=5fa680778718af9087ccbe7a823e3909f1bcceb6)
[ -f "$M" ] || jq -n --arg t "$(date -u +%FT%TZ)" '{base_commits:{},merge_cli:"superclaude review merge",created_utc:$t}' > "$M"
for P in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
  T1=$(sed -n 's/^T1: start sha=\([0-9a-f]\{40\}\)$/\1/p' "$REPO/.dev/tasks/done/$P/progress.md" | head -1)
  if [ -n "$T1" ] && { git -C "$REPO" cat-file -e "$T1^{commit}" 2>/dev/null || { timeout 60 git -C "$REPO" fetch -q origin "$T1" 2>/dev/null && git -C "$REPO" cat-file -e "$T1^{commit}" 2>/dev/null; }; }; then
    SHA=$T1; METHOD=t1-start
  else
    SHA=${FALLBACK[$P]}; METHOD=squash-first-parent
  fi
  git -C "$REPO" cat-file -e "$SHA^{commit}" || { echo "FAIL $P base $SHA not in repo" >&2; exit 1; }
  jq --arg p "$P" --arg s "$SHA" --arg m "$METHOD" --arg t "$T1" '.base_commits[$p]={sha:$s,method:$m,t1_start:$t}' "$M" > "$M.tmp" && mv "$M.tmp" "$M"
  echo "$P $SHA $METHOD"
done
