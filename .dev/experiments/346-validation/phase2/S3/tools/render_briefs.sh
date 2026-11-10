#!/usr/bin/env bash
# Render the S3 briefs for a replay worktree: the ONLY change is the worktree path.
# Usage: render_briefs.sh <S3 package dir> <replay worktree> <out dir>
# Original path in every brief: /home/coder/workspaces/worktrees/IronClaude/hook-launch-level-394
set -eu -o pipefail
PKG=$1; WT=$2; OUT=$3
OLD=/home/coder/workspaces/worktrees/IronClaude/hook-launch-level-394
case "$WT" in /*) ;; *) echo "worktree path must be absolute" >&2; exit 2;; esac
mkdir -p "$OUT"
for f in "$PKG"/briefs/R*.md "$PKG"/briefs/RECONSTRUCTED-*.md; do
  [ -e "$f" ] || continue
  sed "s#$OLD#$WT#g" "$f" > "$OUT/$(basename "$f")"
done
# self-check: reversing the substitution must give back the verbatim brief
for f in "$PKG"/briefs/R*.md; do
  if [ "$WT" != "$OLD" ]; then
    sed "s#$WT#$OLD#g" "$OUT/$(basename "$f")" | cmp -s - "$f" || { echo "ROUNDTRIP FAIL $(basename "$f")" >&2; exit 1; }
  fi
done
echo "rendered $(ls "$OUT" | wc -l) briefs into $OUT (roundtrip OK)"
