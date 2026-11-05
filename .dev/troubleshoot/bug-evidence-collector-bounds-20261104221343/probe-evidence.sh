#!/usr/bin/env bash
# Probe for collect-conflict-evidence.sh: C1 (second collection into the same --out) and
# A2 (no `timeout` on PATH: a hung git read is not bounded). Scratch repo only.
set -u
EV="$1"
S=$(mktemp -d /tmp/ev-probe.XXXXXX)
trap 'rm -rf "$S"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 HOME="$S/home"
export GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@e
mkdir -p "$HOME"
git init -q -b main "$S/r"; cd "$S/r" || exit 1
printf 'base\n' > f.txt; git add f.txt; git commit -qm base
git checkout -qb pr; printf 'ours\n' > f.txt; git commit -qam pr
git checkout -q main; printf 'theirs\n' > f.txt; git commit -qam main
BASE=$(git rev-parse main); git checkout -q pr; MB=$(git merge-base pr main)
git -c merge.conflictStyle=zdiff3 merge --no-commit --no-ff "$BASE" >/dev/null 2>&1

echo "== C1: first attempt collects into sync/sync-1/1/"
"$EV" --path f.txt --out "$S/out/sync/sync-1/1/" --base-sha "$BASE" --merge-base "$MB" 2>/dev/null | cut -c1-60; echo "exit=${PIPESTATUS[0]}"
echo "== C1: resume restart (same cycle_id) collects into the same directory"
"$EV" --path f.txt --out "$S/out/sync/sync-1/1/" --base-sha "$BASE" --merge-base "$MB" 2>/dev/null; echo "exit=$?"

echo "== A2: PATH without timeout; git replaced by a wrapper that hangs on 'show'"
mkdir -p "$S/bin"
REALGIT=$(command -v git)
printf '#!/bin/bash\nfor a in "$@"; do [ "$a" = show ] && sleep 65; done\nexec %s "$@"\n' "$REALGIT" > "$S/bin/git"; chmod +x "$S/bin/git"
for t in bash jq tr cut wc head ls mkdir cat rm printf sed grep mktemp env dirname basename sleep; do
  p=$(command -v "$t") && ln -sf "$p" "$S/bin/$t"
done
start=$SECONDS
PATH="$S/bin" LIMIT_PROBE=1 "$EV" --path f.txt --out "$S/out2/" --base-sha "$BASE" --merge-base "$MB" >/dev/null 2>&1; rc=$?
echo "timeout on PATH: $(PATH="$S/bin" command -v timeout || echo none); exit=$rc; elapsed=$((SECONDS - start))s (the first 'git show' sleeps 65s; a bounded run would stop at 60s)"
