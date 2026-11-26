#!/usr/bin/env bash
# build-sandbox.sh [--raw] [--packages FILE] <doc>   (DESIGN 11.2 H3 and H4, DD-15, section 10 row 7)
# Builds SB/<doc>/repo (the document's base snapshot) and SB/cand/<doc>/{candidate.md,source.md}.
#   --raw       arm Z0-raw: SB/<doc>/repo-raw, repository HEAD minus ground-truth files and .dev/eval-workspaces.
#   --packages  test hook: another packages file; accepted only under /tmp/.
# Exit 0: built, or already valid. Exit 2: invalid (E_SANDBOX_DIRTY, E_LEAK, E_BASE or a failed step).
# Git is read on SRC_REPO (archive, cat-file, show, rev-parse) and written only inside the throwaway
# sandbox directory SBT, always as "git -C $SBT ..." (K5; the check of Task 8 greps bin/ for any other form).
# Test overrides (SW_SB_ROOT, SW_SRC_REPO) are refused by bin/common.sh unless they point under /tmp/.
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  echo "usage: build-sandbox.sh [--raw] [--packages FILE] <doc>" >&2
  exit 2
}
RAW=0
PKFILE=$SW/config/packages.json
DOC=
while [ $# -gt 0 ]; do
  case "$1" in
    --raw) RAW=1 ;;
    --packages)
      shift
      [ $# -gt 0 ] || usage
      PKFILE=$1
      ;;
    -*) usage ;;
    *)
      [ -z "$DOC" ] || usage
      DOC=$1
      ;;
  esac
  shift
done
[ -n "$DOC" ] || usage
[[ $DOC =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "E_DOC: bad document id: $DOC" >&2; exit 2; }
if [ "$PKFILE" != "$SW/config/packages.json" ]; then
  case "$(realpath -m -- "$PKFILE")/" in
    /tmp/?*) ;;
    *) echo "E_OVERRIDE: --packages $PKFILE is outside /tmp/" >&2; exit 2 ;;
  esac
fi
[ -f "$PKFILE" ] || { echo "E_PACKAGES: $PKFILE not found" >&2; exit 2; }
jq -e --arg p "$DOC" '.packages[$p]' "$PKFILE" >/dev/null 2>&1 || { echo "unknown package $DOC" >&2; exit 2; }

BASE=$(jq -r --arg p "$DOC" '.packages[$p].base // empty' "$PKFILE")
CAND_REL=$(jq -r --arg p "$DOC" '.packages[$p].candidate // empty' "$PKFILE")
SRC_REL=$(jq -r --arg p "$DOC" '.packages[$p].source // empty' "$PKFILE")
mapfile -t MASKED < <(jq -r --arg p "$DOC" '.packages[$p].masked_paths // [] | .[]' "$PKFILE")
mapfile -t IDS < <(jq -r '.packages | keys[]' "$PKFILE")

D=$SB/$DOC
if [ "$RAW" = 1 ]; then SUB=repo-raw META=sandbox-raw.json; else SUB=repo META=sandbox.json; fi
TARGET=$D/$SUB
SBT=$D/$SUB.tmp # the temporary sandbox directory; the only place a git write may happen
sw_assert_writable "$D" || exit 2
sw_assert_writable "$SB/cand/$DOC" || exit 2

# KIND: commit (a base commit, read with git archive), tree (a recorded working tree), raw (HEAD, DD-15)
TREEDIR=
if [ "$RAW" = 1 ]; then
  KIND=raw
  BASE=$(git -C "$SRC_REPO" rev-parse --verify -q 'HEAD^0') || { echo "E_BASE: no HEAD in $SRC_REPO" >&2; exit 2; }
elif [ -z "$BASE" ]; then
  echo "E_BASE: package $DOC has no base" >&2
  exit 2
elif [ "${BASE#tree:}" != "$BASE" ]; then
  KIND=tree
  TREEDIR=${BASE#tree:}
  case "$TREEDIR" in /*) ;; *) TREEDIR=$SRC_REPO/$TREEDIR ;; esac
  [ -d "$TREEDIR" ] || { echo "E_BASE: tree directory missing: $TREEDIR" >&2; exit 2; }
else
  KIND=commit
  git -C "$SRC_REPO" rev-parse --verify -q "$BASE^0" >/dev/null 2>&1 || { echo "E_BASE: $BASE is not a commit in $SRC_REPO" >&2; exit 2; }
fi

base_has() { # does the base hold path $1
  if [ "$KIND" = tree ]; then [ -e "$TREEDIR/$1" ]; else git -C "$SRC_REPO" cat-file -e "$BASE:$1" 2>/dev/null; fi
}
base_same() { # is file $2 the base version of path $1
  if [ "$KIND" = tree ]; then
    cmp -s -- "$TREEDIR/$1" "$2"
  else
    cmp -s <(git -C "$SRC_REPO" show "$BASE:$1" 2>/dev/null) "$2"
  fi
}
masked_ok() { # $1 = sandbox directory: each masked path is the base version, or absent where the base has none (REQ-03)
  local f
  [ "$RAW" = 1 ] && return 0
  for f in "${MASKED[@]}"; do
    if base_has "$f"; then
      base_same "$f" "$1/$f" || { echo "masked path differs from base: $f" >&2; return 1; }
    else
      [ ! -e "$1/$f" ] || { echo "masked path present but absent at base: $f" >&2; return 1; }
    fi
  done
}
leak_check() { # $1 = sandbox directory; any finding makes the sandbox invalid (REQ-04, REQ-34)
  local d=$1 bad=0 out id p
  out=$(cd "$d" && find . -path ./.git -prune -o -name 'ground-truth*' -print -quit)
  [ -z "$out" ] || { echo "E_LEAK: ground-truth file remains: $out" >&2; bad=1; }
  [ ! -e "$d/.dev/eval-workspaces" ] || { echo "E_LEAK: .dev/eval-workspaces remains" >&2; bad=1; }
  if [ "$RAW" != 1 ]; then
    for p in .dev/reflect .dev/tasks/done .dev/research; do
      [ ! -e "$d/$p" ] || { echo "E_LEAK: $p remains" >&2; bad=1; }
    done
    out=$(cd "$d" && find . -path ./.git -prune -o \( \( -name artifacts -type d \) -o -name progress.md \) -print -quit)
    [ -z "$out" ] || { echo "E_LEAK: artifacts or progress.md remains: $out" >&2; bad=1; }
    for id in "${IDS[@]}"; do
      out=$(cd "$d" && find . -path ./.git -prune -o -path "*$id*" -print -quit)
      [ -z "$out" ] || { echo "E_LEAK: path with document id remains: $out" >&2; bad=1; }
    done
    out=$(cd "$d" && grep -rIl --exclude-dir=.git -F -- "$DOC" . | head -n 3)
    [ -z "$out" ] || { echo "E_LEAK: document id $DOC in contents of: $out" >&2; bad=1; }
  fi
  return $bad
}
fail() { # a failed build leaves no half-built sandbox
  echo "$1" >&2
  rm -rf "$SBT"
  exit 2
}
resolve_rel() { # a package path: absolute, else under SRC_REPO when present there, else under REPO
  case "$1" in
    /*) echo "$1" ;;
    *) if [ -e "$SRC_REPO/$1" ]; then echo "$SRC_REPO/$1"; else echo "$REPO/$1"; fi ;;
  esac
}

mkdir -p "$D" "$SB/cand/$DOC"
if [ -d "$TARGET" ]; then
  if masked_ok "$TARGET" && [ -z "$(git -C "$TARGET" status --porcelain 2>&1)" ] && leak_check "$TARGET"; then
    echo "sandbox valid: $TARGET"
  else
    echo "E_SANDBOX_DIRTY: $TARGET" >&2
    exit 2
  fi
else
  rm -rf "$SBT"
  mkdir -p "$SBT"
  if [ "$KIND" = tree ]; then
    tar -C "$TREEDIR" --exclude=./.git -cf - . | tar -x -C "$SBT" || fail "copy of $TREEDIR failed"
  else
    git -C "$SRC_REPO" archive "$BASE" | tar -x -C "$SBT" || fail "archive of $BASE failed"
  fi
  # H4. Raw mode (DD-15) removes only the eval-workspace folders and the ground-truth files.
  if [ "$RAW" = 1 ]; then
    (cd "$SBT" && rm -rf .dev/eval-workspaces) || fail "removal failed"
  else
    (cd "$SBT" && rm -rf .dev/reflect .dev/tasks/done .dev/eval-workspaces .dev/research) || fail "removal failed"
    (cd "$SBT" && find . -name artifacts -type d -prune -exec rm -rf -- {} +) || fail "removal failed"
    (cd "$SBT" && find . -name progress.md -type f -exec rm -f -- {} +) || fail "removal failed"
    for id in "${IDS[@]}"; do
      (cd "$SBT" && find . -path "*$id*" -prune -exec rm -rf -- {} +) || fail "removal failed"
    done
  fi
  (cd "$SBT" && find . -name 'ground-truth*' -prune -exec rm -rf -- {} +) || fail "removal failed"
  masked_ok "$SBT" || fail "E_SANDBOX_DIRTY: masked path check failed"
  leak_check "$SBT" || fail "E_LEAK: the sandbox was refused"
  # The snapshot keeps files that the base ignore rules match, so every arm sees the same tree.
  git -C "$SBT" init -q || fail "snapshot failed (init)"
  git -C "$SBT" add -A -f || fail "snapshot failed (stage)"
  git -C "$SBT" -c user.name=sw -c user.email=sw@localhost -c core.hooksPath=/dev/null -c commit.gpgsign=false commit -q -m snap || fail "snapshot failed (snapshot)"
  [ -z "$(git -C "$SBT" status --porcelain)" ] || fail "E_SANDBOX_DIRTY: dirty after the snapshot"
  mv "$SBT" "$TARGET" || fail "move failed"
  TREE=$(git -C "$TARGET" rev-parse 'HEAD^{tree}')
  jq -n --arg doc "$DOC" --arg kind "$KIND" --arg base "$BASE" --arg tree "$TREE" --arg t "$(date -u +%FT%TZ)" \
    '{schema: "sweep-sandbox/1", doc: $doc, kind: $kind, base: $base, tree: $tree, built_at: $t}' >"$D/$META"
  echo "sandbox built: $TARGET"
fi

# SB/cand/<doc>: the candidate plan and its source, the only inputs a reviewer reads besides the sandbox.
CS=$(resolve_rel "$CAND_REL")
{ [ -n "$CAND_REL" ] && [ -f "$CS" ]; } || { echo "candidate.md missing: ${CS:-<not set>}" >&2; exit 2; }
cmp -s "$CS" "$SB/cand/$DOC/candidate.md" || cp -- "$CS" "$SB/cand/$DOC/candidate.md"
if [ -n "$SRC_REL" ]; then
  SS=$(resolve_rel "$SRC_REL")
  [ -f "$SS" ] || { echo "source.md missing: $SS" >&2; exit 2; }
  cmp -s "$SS" "$SB/cand/$DOC/source.md" || cp -- "$SS" "$SB/cand/$DOC/source.md"
else
  rm -f "$SB/cand/$DOC/source.md" # no source: CB-1 is not rendered, E5 returns nothing (section 10 row 5)
fi
exit 0
