#!/usr/bin/env bash
# Falsification probe for finish-merge.sh A1 (marker width) and C2 (mode-blind step 5).
# Runs entirely in a scratch directory; prints the script's stdout/exit per case.
set -u
FIN="$1"
S=$(mktemp -d /tmp/fin-probe.XXXXXX)
trap 'rm -rf "$S"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 HOME="$S/home"
export GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@e
mkdir -p "$HOME"

setup() { # setup <dir> <with_attr>
  git init -q -b main "$1"; cd "$1" || exit 1
  printf 'base\n' > f.txt; printf '#!/bin/sh\n' > run.sh; chmod 755 run.sh
  [ "$2" = yes ] && printf 'f.txt conflict-marker-size=9\n' > .gitattributes
  git add -A; git commit -qm base
  git checkout -qb pr; printf 'ours\n' > f.txt; git commit -qam pr
  git checkout -q main; printf 'theirs\n' > f.txt; git commit -qam main
  BASE=$(git rev-parse main); git checkout -q pr
  MT=$(git merge-tree --write-tree pr main | head -1)
  git ls-files -s f.txt >/dev/null
  git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff "$BASE" >/dev/null 2>&1
  STAGE1=$(git ls-files -u -- f.txt | awk '$3==1{print $2}')
  printf '%s\tf.txt\n' "$STAGE1" > "$S/manifest.$2"; printf 'merge\n' > "$S/msg"
}

echo "== A1: conflict-marker-size=9, markers left in f.txt and staged"
setup "$S/a1" yes
echo "marker line written by git: $(grep -m1 -E '^<+' f.txt | cut -c1-12)"
git add f.txt
"$FIN" --base-sha "$BASE" --merge-tree-oid "$MT" --manifest "$S/manifest.yes" --message-file "$S/msg" 2>/dev/null; echo "exit=$?"

echo "== C2: resolve f.txt, stage an unrelated mode change on run.sh"
setup "$S/c2" no
printf 'resolved\n' > f.txt; git add f.txt; chmod 644 run.sh; git add run.sh
echo "diff --cached --name-only vs merge tree: $(git diff --cached --name-only --no-renames "$MT" | tr '\n' ' ')"
"$FIN" --base-sha "$BASE" --merge-tree-oid "$MT" --manifest "$S/manifest.no" --message-file "$S/msg" 2>/dev/null; echo "exit=$?"
echo "committed run.sh mode: $(git ls-tree HEAD run.sh | cut -c1-6)"
