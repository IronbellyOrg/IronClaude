#!/usr/bin/env bash
# Copy the shared Sweep Sheet pieces into RL and record their hashes (DESIGN 3.1, 3.2; K8).
# The sibling folder is only a source: this script runs sha256sum, cp, diff and stat on it, nothing else.
#
#   copy-shared.sh                 copy per config/shared-list.json, write config/shared-manifest.json
#   copy-shared.sh --check         re-hash every copy (edited copy: exit 1), report sibling drift (warning, exit 0)
#   copy-shared.sh --diff <path>   unified diff of a local file against the sibling's file of the same name
# Options: --sibling DIR (default: the sweep-sheet folder), --dest DIR (default: RL), --list FILE,
#          --gap SECONDS (default 60: the pause between the two reads of the Tier B files).
# Exit: 0 ok, 1 edited copy (--check), 2 usage, 3 refused (missing Tier A/S/T file, unstable Tier B file, bad copy).
set -u -o pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
RL=$(cd "$HERE/.." && pwd -P)
REPO=$(cd "$RL/../../../.." && pwd -P)
SIB=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
DEST=$RL
LIST=""
GAP=60
MODE=copy
DIFFPATH=""

usage() { sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }
die() { echo "$1" >&2; exit "${2:-3}"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --help | -h) usage; exit 0 ;;
    --check) MODE=check ;;
    --diff) MODE=diff; shift; [ $# -ge 1 ] || die "--diff needs a path" 2; DIFFPATH=$1 ;;
    --sibling) shift; [ $# -ge 1 ] || die "--sibling needs a folder" 2; SIB=$1 ;;
    --dest) shift; [ $# -ge 1 ] || die "--dest needs a folder" 2; DEST=$1 ;;
    --list) shift; [ $# -ge 1 ] || die "--list needs a file" 2; LIST=$1 ;;
    --gap) shift; [ $# -ge 1 ] || die "--gap needs seconds" 2; GAP=$1 ;;
    *) die "unknown option: $1" 2 ;;
  esac
  shift
done
[[ $GAP =~ ^[0-9]+$ ]] || die "--gap must be whole seconds" 2
[ -n "$LIST" ] || LIST=$DEST/config/shared-list.json
[ -f "$LIST" ] || die "no list: $LIST" 2
MANIFEST=$DEST/config/shared-manifest.json

# The copy never lands in the sibling (K8).
rs=$(realpath -m -- "$SIB")
rd=$(realpath -m -- "$DEST")
case "$rd/" in "$rs"/*) die "E_DEST_IN_SIBLING: $DEST is inside $SIB" 2 ;; esac

hash_of() { sha256sum -- "$1" | cut -d' ' -f1; }
size_of() { stat -c %s -- "$1"; }
tier_paths() { jq -r --arg t "$1" '.tiers[$t][] | if type == "object" then .path else . end' "$LIST"; }
swd_of() { jq -r --arg p "$1" '.tiers.B[] | select(.path == $p) | .swd' "$LIST"; }
prev_kind() { [ -f "$MANIFEST" ] && jq -r --arg p "$1" '.files[$p].kind // ""' "$MANIFEST" || echo ""; }
prev_entry() { jq -c --arg p "$1" '.files[$p] | select(. != null) | . + {path: $p}' "$MANIFEST"; }

if [ "$MODE" = diff ]; then
  [ -e "$DEST/$DIFFPATH" ] || die "no local file: $DEST/$DIFFPATH" 2
  [ -e "$SIB/$DIFFPATH" ] || { echo "the sibling has no file $DIFFPATH"; exit 0; }
  diff -u --label "SW/$DIFFPATH" --label "RL/$DIFFPATH" -- "$SIB/$DIFFPATH" "$DEST/$DIFFPATH"
  exit 0
fi

if [ "$MODE" = check ]; then
  [ -f "$MANIFEST" ] || die "no manifest: $MANIFEST" 2
  checked=0 drift=0 failed=0
  while IFS=$'\t' read -r p tier kind sha; do
    [ "$tier" != S ] || continue
    checked=$((checked + 1))
    if [ "$kind" = copied ]; then
      if [ ! -f "$DEST/$p" ]; then
        echo "FAIL $p: the copy is missing"; failed=$((failed + 1)); continue
      elif [ "$(hash_of "$DEST/$p")" != "$sha" ]; then
        echo "FAIL $p: the copy was edited (hash differs from the manifest)"; failed=$((failed + 1)); continue
      fi
      if [ ! -f "$SIB/$p" ]; then
        echo "drift $p: the sibling no longer has this file"; drift=$((drift + 1))
      elif [ "$(hash_of "$SIB/$p")" != "$sha" ]; then
        echo "drift $p: the sibling's file changed since the copy"; drift=$((drift + 1))
      fi
    elif [ -f "$SIB/$p" ]; then
      echo "drift $p: built-local, but the sibling now has a file of that name (run --diff $p)"
      drift=$((drift + 1))
    fi
  done < <(jq -r '.files | to_entries[] | [.key, .value.tier, .value.kind, .value.sha256] | @tsv' "$MANIFEST")
  echo "check: $checked checked, $drift drift (warning), $failed failed"
  [ "$failed" -eq 0 ]
  exit $?
fi

# ---- copy mode ----
TMP=$(mktemp -d /tmp/rl-copyshared.XXXXXXXX) || die "mktemp failed"
trap 'rm -rf -- "$TMP"' EXIT
ENT=$TMP/entries.jsonl
: >"$ENT"

emit() { # path tier sha bytes copied_at kind swd
  jq -nc --arg path "$1" --arg tier "$2" --arg sha "$3" --argjson bytes "$4" --arg at "$5" --arg kind "$6" --arg swd "$7" \
    '{path: $path, tier: $tier, source: ("SW/" + $path), sha256: $sha, bytes: $bytes,
      copied_at: (if $at == "" then null else $at end), kind: $kind} + (if $swd == "" then {} else {swd: $swd} end)' >>"$ENT"
}
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }

# Step 1: every Tier A, S and T file must exist before anything is copied.
mapfile -t A < <(tier_paths A)
mapfile -t S < <(tier_paths S)
mapfile -t T < <(tier_paths T)
mapfile -t B < <(tier_paths B)
missing=0
for p in "${A[@]}" "${T[@]}"; do
  [ -f "$SIB/$p" ] || { echo "E_MISSING: $p is missing in the sibling" >&2; missing=1; }
done
for p in "${S[@]}"; do
  [ -f "$DEST/$p" ] && [ -n "$(prev_kind "$p")" ] && continue
  [ -f "$SIB/$p" ] || { echo "E_MISSING: $p is missing in the sibling" >&2; missing=1; }
done
[ "$missing" -eq 0 ] || die "stopped: a Tier A, S or T file is missing; nothing was copied and nothing may be rebuilt by hand" 3

# Step 2: Tier B files that exist are read twice, GAP seconds apart. A file that built-local protects is not read.
declare -A H1 PROT
anyb=0
for p in "${B[@]}"; do
  if [ "$(prev_kind "$p")" = built-local ] && [ -f "$DEST/$p" ]; then
    PROT[$p]=1
  elif [ -f "$SIB/$p" ]; then
    H1[$p]=$(hash_of "$SIB/$p"); anyb=1
  fi
done
[ "$anyb" -eq 0 ] || sleep "$GAP"
for p in "${!H1[@]}"; do
  if [ ! -f "$SIB/$p" ] || [ "$(hash_of "$SIB/$p")" != "${H1[$p]}" ]; then
    die "E_UNSTABLE: $p changed between two reads $GAP s apart; the sibling is still writing it; nothing was copied" 3
  fi
done

# Step 3: copy, then hash the copy and compare.
copy_one() { # rel expected_hash
  local rel=$1 want=$2 got
  mkdir -p -- "$(dirname -- "$DEST/$rel")"
  cp -- "$SIB/$rel" "$DEST/$rel" || die "E_COPY: cp failed for $rel" 3
  got=$(hash_of "$DEST/$rel")
  [ "$got" = "$want" ] || die "E_COPY: $rel changed while it was copied (source $want, copy $got)" 3
}
for p in "${A[@]}" "${T[@]}"; do
  t=A
  [[ $p == tests/* || $p == fixtures/* ]] && t=T
  h=$(hash_of "$SIB/$p")
  copy_one "$p" "$h"
  emit "$p" "$t" "$h" "$(size_of "$DEST/$p")" "$(now)" copied ""
done
for p in "${S[@]}"; do
  if [ -f "$DEST/$p" ] && [ -n "$(prev_kind "$p")" ]; then
    prev_entry "$p" >>"$ENT"
    continue
  fi
  h=$(hash_of "$SIB/$p")
  copy_one "$p" "$h"
  emit "$p" S "$h" "$(size_of "$DEST/$p")" "$(now)" copied ""
done
for p in "${B[@]}"; do
  if [ -n "${H1[$p]:-}" ]; then
    copy_one "$p" "${H1[$p]}"
    emit "$p" B "${H1[$p]}" "$(size_of "$DEST/$p")" "$(now)" copied ""
    continue
  fi
  if [ -f "$DEST/$p" ]; then
    emit "$p" B "$(hash_of "$DEST/$p")" "$(size_of "$DEST/$p")" "" built-local "$(swd_of "$p")"
  else
    emit "$p" B ABSENT null "" built-local "$(swd_of "$p")"
  fi
  [ -z "${PROT[$p]:-}" ] || [ ! -f "$SIB/$p" ] || echo "note: $p is built-local and the sibling now has it; run --diff $p"
done

# Step 4: the manifest.
mkdir -p -- "$DEST/config"
jq -S -s '{schema: "rl-shared-manifest/1",
           note: "sha256 ABSENT marks a built-local file that has not been written yet; bin/copy-shared.sh records its hash when it exists",
           files: (map({(.path): del(.path)}) | add)}' "$ENT" >"$TMP/manifest.json" || die "manifest write failed" 3
cp -- "$TMP/manifest.json" "$MANIFEST"
echo "copied: $(jq '[.files[] | select(.kind == "copied")] | length' "$MANIFEST") files, built-local: $(jq '[.files[] | select(.kind == "built-local")] | length' "$MANIFEST"); manifest $MANIFEST"
