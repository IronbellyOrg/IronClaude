#!/usr/bin/env bash
# build-sandbox.sh <pkg>: SB/<pkg>/repo from the package's base commit (H3, H4) and SB/cand/<pkg>/ (section 5.1).
# exit 0 built or already valid; 2 invalid (E_SANDBOX_DIRTY or a failed check).
set -u -o pipefail
source "$(dirname "$0")/../lib/common.sh"
PKG=$1
# test-only overrides (must live under /tmp/)
SRC_REPO=${R3_SRC_REPO:-$REPO}
PKFILE=${R3_PACKAGES_FILE:-$R3/config/packages.json}
for v in "$SRC_REPO" "$PKFILE"; do
  case "$v" in "$REPO"|"$R3/config/packages.json"|/tmp/*) ;; *) echo "E_OVERRIDE: $v" >&2; exit 2;; esac
done
base=$(jq -r --arg p "$PKG" '.packages[$p].base // empty' "$PKFILE")
[ -n "$base" ] || { echo "unknown package $PKG" >&2; exit 2; }
mapfile -t MASKED < <(jq -r --arg p "$PKG" '.packages[$p].masked_paths[]' "$PKFILE")
D=$SB/$PKG
r3_assert_writable "$D" || exit 2
mkdir -p "$D/active" "$SB/cand/$PKG"

masked_ok() { # $1 = repo dir
  local f
  for f in "${MASKED[@]}"; do
    if git -C "$SRC_REPO" cat-file -e "$base:$f" 2>/dev/null; then
      cmp -s <(git -C "$SRC_REPO" show "$base:$f") "$1/$f" || { echo "masked path differs from base: $f" >&2; return 1; }
    else
      [ ! -e "$1/$f" ] || { echo "masked path present but absent at base: $f" >&2; return 1; }
    fi
  done
}

if [ -d "$D/repo" ]; then
  if masked_ok "$D/repo" && [ -z "$(git -C "$D/repo" status --porcelain 2>&1)" ]; then
    echo "sandbox valid: $D/repo"
  else
    echo "E_SANDBOX_DIRTY: $D/repo" >&2; exit 2
  fi
else
  T=$D/repo.tmp; rm -rf "$T"; mkdir -p "$T"
  git -C "$SRC_REPO" archive "$base" | tar -x -C "$T" || { echo "archive failed" >&2; exit 2; }
  rm -rf "$T/.dev/tasks/done" "$T/.dev/eval-workspaces" "$T/.dev/research" "$T/.dev/reflect"
  for id in $(jq -r '.packages|keys[]' "$PKFILE"); do
    if [ -n "$(cd "$T" && find . -path "*$id*" -print -quit)" ]; then echo "package path remains: $id" >&2; exit 2; fi
  done
  masked_ok "$T" || exit 2
  # -f: files tracked at base that the base .gitignore matches stay in the snapshot (same sandbox in both arms)
  ( cd "$T" && git init -q && git add -A -f && git -c user.name=r3 -c user.email=r3@localhost commit -q -m snap ) || exit 2
  [ -z "$(git -C "$T" status --porcelain)" ] || { echo "dirty after snap" >&2; exit 2; }
  mv "$T" "$D/repo"
  jq -n --arg base "$base" --arg tree "$(git -C "$D/repo" rev-parse 'HEAD^{tree}')" --arg t "$(date -u +%FT%TZ)" \
    '{base:$base,tree:$tree,built_at:$t}' > "$D/sandbox.json"
  echo "sandbox built: $D/repo"
fi
CS=$EVAL/$PKG/candidate.md
SS=$SRC_REPO/.dev/tasks/done/$PKG/source.md
[ "$SRC_REPO" = "$REPO" ] || SS=$REPO/.dev/tasks/done/$PKG/source.md
[ -f "$SS" ] || { echo "source.md missing: $SS" >&2; exit 2; }
cmp -s "$CS" "$SB/cand/$PKG/candidate.md" || cp "$CS" "$SB/cand/$PKG/candidate.md"
cmp -s "$SS" "$SB/cand/$PKG/source.md" || cp "$SS" "$SB/cand/$PKG/source.md"
exit 0
