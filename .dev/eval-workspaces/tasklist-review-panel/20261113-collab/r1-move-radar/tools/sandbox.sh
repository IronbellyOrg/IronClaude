#!/usr/bin/env bash
# sandbox.sh <pkg> [--root <R1>] [--sb <SB>]   (H1, H3, H4; idempotent)
# Builds SB/<pkg>/repo from the package's base commit (manifest.json) without the leak directories,
# as its own throwaway git repo, and copies candidate.md and source.md to SB/cand/<pkg>/.
# Exit 0 ok, 2 when SB/<pkg>/repo.ok names a different base sha, 1 on any other failure.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
A1DIR=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
SB=/tmp/evalsb-collab-r1
PKG=${1:?usage: sandbox.sh <pkg> [--root R1] [--sb SB]}; shift
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; *) echo "bad arg $1" >&2; exit 1;; esac; done
SHA=$(jq -r --arg p "$PKG" '.base_commits[$p].sha // empty' "$R1/manifest.json")
[ -n "$SHA" ] || { echo "FAIL no base sha for $PKG in manifest.json" >&2; exit 1; }
D=$SB/$PKG; C=$SB/cand/$PKG
if [ -f "$D/repo.ok" ]; then
  [ "$(cat "$D/repo.ok")" = "$SHA" ] || { echo "REFUSE $D/repo.ok names $(cat "$D/repo.ok"), manifest says $SHA" >&2; exit 2; }
else
  rm -rf "$D/repo"; mkdir -p "$D/repo"   # a partial build (no repo.ok) is rebuilt from scratch
  git -C "$REPO" archive "$SHA" | tar -x -C "$D/repo" || { echo "FAIL archive $SHA" >&2; exit 1; }
  rm -rf "$D/repo/.dev/tasks/done" "$D/repo/.dev/eval-workspaces" "$D/repo/.dev/research" "$D/repo/.dev/reflect"
  [ -d "$D/repo/.dev" ] && find "$D/repo/.dev" -depth -type d -name "$PKG" -exec rm -rf {} +   # the package's own plan folder
  ( cd "$D/repo" && git init -q && git add -A && git -c user.name=sandbox -c user.email=sandbox@localhost commit -qm snapshot ) || { echo "FAIL git snapshot" >&2; exit 1; }
  echo "$SHA" > "$D/repo.ok"
fi
mkdir -p "$C"
cmp -s "$A1DIR/$PKG/candidate.md" "$C/candidate.md" || cp "$A1DIR/$PKG/candidate.md" "$C/candidate.md"
cmp -s "$REPO/.dev/tasks/done/$PKG/source.md" "$C/source.md" || cp "$REPO/.dev/tasks/done/$PKG/source.md" "$C/source.md"
echo "OK $D/repo $SHA"
