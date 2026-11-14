#!/usr/bin/env bash
# H3 + H4: base tarball per package. build-sandbox.sh <pkg>
# exit 0 prints the tar sha256; 2 base_sha missing from the manifest; 3 a removed directory is still in the tar.
set -u -o pipefail
. "$(dirname "$0")/lib/common.sh"
PKG=$1
BASE=$(jq -r --arg p "$PKG" '.base_sha[$p] // empty' "$MANIFEST")
[ -n "$BASE" ] || { echo "base_sha missing for $PKG in $MANIFEST" >&2; exit 2; }
mkdir -p "$SBR/base"
TAR=$SBR/base/$PKG.tar; REC=$TAR.sha256
if [ -f "$TAR" ] && [ -f "$REC" ] && [ "$(sha256sum "$TAR" | cut -d' ' -f1)" = "$(cut -d' ' -f1 "$REC")" ] \
   && [ "$(cut -d' ' -f2 "$REC")" = "$BASE" ]; then
  cut -d' ' -f1 "$REC"; exit 0
fi
TMP=$(mktemp -d /tmp/collab-r2/build.XXXXXX 2>/dev/null || { mkdir -p /tmp/collab-r2; mktemp -d /tmp/collab-r2/build.XXXXXX; })
trap 'rm -rf "$TMP"' EXIT
git -C "$REPO" archive "$BASE" | tar -x -C "$TMP" || { echo "git archive failed" >&2; exit 1; }
rm -rf "$TMP/.dev/tasks/done" "$TMP/.dev/eval-workspaces" "$TMP/.dev/research" "$TMP/.dev/reflect"
tar -cf "$TAR.tmp" -C "$TMP" .
if tar -tf "$TAR.tmp" | grep -qE '^(\./)?\.dev/(tasks/done|eval-workspaces|research|reflect)(/|$)'; then
  rm -f "$TAR.tmp"; echo "leak directory still in tar" >&2; exit 3
fi
mv "$TAR.tmp" "$TAR"
H=$(sha256sum "$TAR" | cut -d' ' -f1)
echo "$H $BASE" > "$REC"
echo "$H"
