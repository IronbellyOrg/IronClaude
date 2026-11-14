#!/usr/bin/env bash
# build-sandbox.sh [--rebuild]: H3/H4 sandboxes plus candidate and source copies (design 1.2).
# Reads R4_SBR and R4_OUT (defaults /tmp/evalsb-collab-r4 and this folder).
set -u -o pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
REPO=${R4_REPO:-$(cd "$HERE/../../../../.." && pwd)}
EVAL="$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
SBR=${R4_SBR:-/tmp/evalsb-collab-r4}
OUT=${R4_OUT:-$HERE}
REBUILD=0; [ "${1:-}" = --rebuild ] && REBUILD=1
LEAKS=".dev/tasks/done .dev/eval-workspaces .dev/research .dev/reflect"
mkdir -p "$SBR/sb" "$SBR/cand" "$OUT"
fail=0
MAN="[]"
while IFS=$'\t' read -r PKG TREE; do
  SB="$SBR/sb/$PKG"; REPO_SB="$SB/repo"; CD="$SBR/cand/$PKG"
  if [ "$REBUILD" = 1 ] || [ "$(jq -r .tree "$SB/built.json" 2>/dev/null)" != "$TREE" ]; then
    rm -rf -- "$SB"; mkdir -p "$REPO_SB"
    git -C "$REPO" archive "$TREE" | tar -x -C "$REPO_SB" || { echo "archive failed: $PKG" >&2; fail=1; continue; }
    removed=()
    for d in $LEAKS; do [ -e "$REPO_SB/$d" ] && { rm -rf -- "${REPO_SB:?}/$d"; removed+=("$d"); }; done
    git -C "$REPO_SB" init -q
    git -C "$REPO_SB" add -A -f
    git -C "$REPO_SB" -c user.name=r4 -c user.email=r4@local commit -qm snap
    NF=$(git -C "$REPO_SB" ls-files | wc -l)
    jq -n --arg t "$TREE" --argjson n "$NF" --argjson rm "$(printf '%s\n' "${removed[@]}" | jq -R . | jq -s 'map(select(length>0))')" \
      '{tree:$t,files:$n,removed:$rm}' > "$SB/built.json"
  fi
  mkdir -p "$CD"
  cp "$EVAL/$PKG/candidate.md" "$CD/candidate.md"
  cp "$REPO/.dev/tasks/done/$PKG/source.md" "$CD/source.md"
  tr -s '[:space:]' ' ' < "$CD/candidate.md" | sed 's/^ //; s/ $//' > "$CD/candidate.flat"
  for d in $LEAKS; do [ -e "$REPO_SB/$d" ] && { echo "leak dir still present: $PKG $d" >&2; fail=1; }; done
  CSHA=$(sha256sum "$CD/candidate.md" | cut -d' ' -f1)
  [ "$CSHA" = "$(sha256sum "$EVAL/$PKG/candidate.md" | cut -d' ' -f1)" ] || { echo "candidate copy differs: $PKG" >&2; fail=1; }
  SSHA=$(sha256sum "$CD/source.md" | cut -d' ' -f1)
  FIRST=$(git -C "$REPO" log --format=%H --reverse -- ".dev/tasks/*/$PKG" | head -1)
  PARENT=""; PTREE=""; [ -n "$FIRST" ] && PARENT=$(git -C "$REPO" rev-parse -q --verify "$FIRST^" 2>/dev/null) && PTREE=$(git -C "$REPO" rev-parse "$PARENT^{tree}")
  MAN=$(jq --arg p "$PKG" --arg t "$TREE" --slurpfile b "$SB/built.json" --arg c "$CSHA" --arg s "$SSHA" \
    --arg head "$(git -C "$REPO_SB" rev-parse HEAD)" --arg first "$FIRST" --arg parent "$PARENT" --arg pt "$PTREE" \
    '. + [{package:$p, base_tree:$t, files:$b[0].files, removed_leak_dirs:$b[0].removed, candidate_sha256:$c, source_sha256:$s,
      sandbox_head:$head, first_commit:$first, first_commit_parent:$parent, parent_tree_equals_base:($pt == $t)}]' <<<"$MAN")
done < <(jq -r '.[] | [.id, .base_tree] | @tsv' "$HERE/frozen/packages.json")
jq --arg sbr "$SBR" '{sbr:$sbr, packages:.}' <<<"$MAN" > "$OUT/manifest.json"
exit $fail
