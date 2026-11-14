#!/usr/bin/env bash
# Build SB/<pkg>/repo (H3 base snapshot, H4 exclusions) and SB/cand/<pkg>/ (DESIGN 1.2; R-03, R-09).
# usage: sandbox-build.sh [--rebuild] [pkg...]; exit 0 when every sandbox exists and matches SB/manifest.json
# env (tests): R5_REPO, R5_SB, R5_CONFIG, R5_EVAL
set -u -o pipefail
R5=$(cd "$(dirname "$0")/.." && pwd); CFG=${R5_CONFIG:-$R5/config}
REPO=${R5_REPO:-$(git -C "$R5" rev-parse --show-toplevel)}
EVAL=${R5_EVAL:-$(cd "$R5/../../20261111-a1" && pwd)}
SB=$(mkdir -p "${R5_SB:-/tmp/evalsb-collab-r5}" && cd "${R5_SB:-/tmp/evalsb-collab-r5}" && pwd)
REBUILD=0; [ "${1:-}" = --rebuild ] && { REBUILD=1; shift; }
PKGS=("$@"); [ ${#PKGS[@]} -gt 0 ] || mapfile -t PKGS < <(jq -r 'keys[]' "$CFG/bases.json")
MAN=$SB/manifest.json; [ -f "$MAN" ] || echo '{}' > "$MAN"
inside() { local r; r=$(realpath -m "$1"); [ "${r#"$SB"/}" != "$r" ] && [ "$r" != "$SB" ]; }
rc=0
for P in "${PKGS[@]}"; do
  case "$P" in */*|.*|'') echo "refused: package name '$P'" >&2; exit 2;; esac
  R=$SB/$P; C=$SB/cand/$P
  inside "$R" && inside "$C" || { echo "refused: $R is outside $SB" >&2; exit 2; }
  BASE=$(jq -r --arg p "$P" '.[$p].base // empty' "$CFG/bases.json"); [ -n "$BASE" ] || { echo "no base for $P" >&2; exit 2; }
  if [ $REBUILD = 1 ]; then rm -rf -- "$R" "$C"; jq --arg p "$P" 'del(.[$p])' "$MAN" > "$MAN.tmp" && mv "$MAN.tmp" "$MAN"; fi
  if [ ! -d "$R/repo/.git" ]; then
    rm -rf -- "$R"; mkdir -p "$R/repo"
    git -C "$REPO" archive "$BASE" -- . ':(exclude).dev/tasks/done' ':(exclude).dev/eval-workspaces' \
      ':(exclude).dev/research' ':(exclude).dev/reflect' | tar -x -C "$R/repo" || { echo "archive failed for $P" >&2; exit 1; }
    ( cd "$R/repo" && git init -q && git add -A && git -c user.name=r5 -c user.email=r5@local -c commit.gpgsign=false \
        -c core.hooksPath=/dev/null commit -qm snapshot ) || { echo "sandbox commit failed for $P" >&2; exit 1; }
  fi
  mkdir -p "$C"
  cmp -s "$EVAL/$P/candidate.md" "$C/candidate.md" || cp "$EVAL/$P/candidate.md" "$C/candidate.md"
  cmp -s "$REPO/.dev/tasks/done/$P/source.md" "$C/source.md" || cp "$REPO/.dev/tasks/done/$P/source.md" "$C/source.md"
  TREE=$(git -C "$R/repo" rev-parse 'HEAD^{tree}')
  CS=$(sha256sum "$C/candidate.md" | cut -d' ' -f1); SS=$(sha256sum "$C/source.md" | cut -d' ' -f1)
  OLD=$(jq -c --arg p "$P" '.[$p] // empty' "$MAN")
  NEW=$(jq -nc --arg b "$BASE" --arg t "$TREE" --arg c "$CS" --arg s "$SS" '{base:$b,tree:$t,candidate_sha256:$c,source_sha256:$s}')
  if [ -z "$OLD" ]; then
    jq --arg p "$P" --argjson v "$NEW" '.[$p]=$v' "$MAN" > "$MAN.tmp" && mv "$MAN.tmp" "$MAN"
  elif [ "$OLD" != "$NEW" ]; then echo "MISMATCH $P manifest=$OLD now=$NEW" >&2; rc=1; continue; fi
  [ -z "$(git -C "$R/repo" status --porcelain)" ] || { echo "DIRTY $P" >&2; rc=1; continue; }
  echo "OK $P base=$BASE tree=$TREE"
done
exit $rc
