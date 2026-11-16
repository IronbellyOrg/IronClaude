#!/usr/bin/env bash
# usage: check-order.sh {freeze|prereg|gt-hash|twins} [MANIFEST]                    (REQ-33, REQ-36, REQ-44)
# Read-only checks of the order in which things were written. They only read git history and files; no git write.
#
#   freeze    the tag named by config/freeze.json exists, its time is earlier than the first commit of a hold-out ground-truth
#             file, and `freeze.sh --check` finds no changed, added or removed frozen file. The time of the tag is the later
#             of its commit's committer time and, for an annotated tag, its tagger date (a tag made late on an old commit
#             does not pass). Fails (1) when no ground-truth file is committed yet: the order cannot be shown.
#   prereg    the commit that first added config/prereg.json is earlier than the first run.json under the runs folder
#             (RL_RUNS_ROOT, default runs/, inside the root). A committed run.json counts at its first commit, an
#             uncommitted one at its modification time. Folders named rehearsal-* are skipped (the fake-claude rehearsal
#             of TESTING 5.1 A7 is not a hold-out run). No run.json at all passes.
#   gt-hash   config/prereg.json holds gt_sha256 {path relative to the root: sha256}; every ground-truth file matches its
#             entry and none is missing from it (REQ-36).
#   twins     MANIFEST (default holdout-gt/planted-set.json) is {"planted": [{"plan": path, "twin": path}, ...]} with paths
#             relative to the root; every planted entry names a twin file that exists (REQ-36).
#
# Ground-truth files are those that match GT_GLOB (default holdout-gt/**/ground-truth*.json, relative to the root). A person
# runs these when the hold-out ground truth is committed and pastes the output into results/attestations.md.
# RL_ROOT (default: the folder above bin/) is the root; git is run in it, so it may be a folder inside a larger repository.
# Output holds paths and times, never file content. Exit: 0 holds, 1 does not hold, 2 usage or a record is missing.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
ROOT=${RL_ROOT:-$(cd "$HERE/.." && pwd -P)}
GT_GLOB=${GT_GLOB:-holdout-gt/**/ground-truth*.json}
help() { sed -n '2,/^set -u/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; }
case "${1:-}" in -h | --help) help; exit 0 ;; esac
MODE=${1:-}
MANIFEST=${2:-holdout-gt/planted-set.json}
case "$MODE" in freeze | prereg | gt-hash | twins) ;; *) echo "usage: check-order.sh {freeze|prereg|gt-hash|twins} [MANIFEST]" >&2; exit 2 ;; esac
cd "$ROOT" || { echo "E_ROOT: cannot enter $ROOT" >&2; exit 2; }
RUNS=${RL_RUNS_ROOT:-$ROOT/runs}
FAIL=0
fail() { echo "FAIL: $*"; FAIL=1; }

g() { git -C "$ROOT" "$@"; }
# first_commit_time <pathspec>...: the earliest committer time of a commit that added a matching path (empty if none)
first_commit_time() { g log --diff-filter=A --format=%ct -- "$@" 2>/dev/null | sort -n | head -n 1; }
# the ground-truth files in the working tree, relative to the root
gt_files() {
  local f
  shopt -s globstar nullglob
  # shellcheck disable=SC2086
  for f in $GT_GLOB; do [ -f "$f" ] && echo "$f"; done
}

case "$MODE" in
  freeze)
    [ -f config/freeze.json ] || { echo "E_NO_FREEZE: config/freeze.json does not exist" >&2; exit 2; }
    TAG=$(jq -r '.freeze_tag // .tag // empty' config/freeze.json 2>/dev/null)
    [ -n "$TAG" ] || { echo "E_FREEZE_JSON: config/freeze.json has no freeze_tag" >&2; exit 2; }
    if COMMIT=$(g rev-parse -q --verify "refs/tags/$TAG^{commit}"); then
      TAG_T=$(g log -1 --format=%ct "$COMMIT")
      TAGGER=$(g for-each-ref --format='%(taggerdate:unix)' "refs/tags/$TAG")
      [ -z "$TAGGER" ] || [ "$TAGGER" -le "$TAG_T" ] || TAG_T=$TAGGER
      GT_T=$(first_commit_time ":(glob)$GT_GLOB")
      echo "tag $TAG time $TAG_T"
      if [ -z "$GT_T" ]; then
        fail "no ground-truth file is committed, so the order cannot be shown"
      else
        echo "first ground-truth commit time $GT_T"
        [ "$TAG_T" -lt "$GT_T" ] || fail "the tag is not earlier than the first ground-truth commit"
      fi
    else
      fail "tag $TAG does not exist (a person creates it, K5)"
    fi
    if OUT=$(RL_ROOT=$ROOT bash "$HERE/freeze.sh" --check); then echo "$OUT"; else echo "$OUT"; fail "frozen files differ from config/freeze.json"; fi
    ;;
  prereg)
    PRE_T=$(first_commit_time config/prereg.json)
    if [ -z "$PRE_T" ]; then
      fail "config/prereg.json is not committed"
    else
      echo "prereg.json first commit time $PRE_T"
      FIRST=
      while IFS= read -r f; do
        rel=$(realpath --relative-to="$ROOT" "$f")
        if g ls-files --error-unmatch -- "$rel" >/dev/null 2>&1; then t=$(first_commit_time "$rel"); fi
        [ -n "${t:-}" ] || t=$(stat -c %Y "$f")
        { [ -n "$FIRST" ] && [ "$FIRST" -le "$t" ]; } || FIRST=$t
        unset t
      done < <(find "$RUNS" -mindepth 2 -maxdepth 2 -name run.json -not -path '*/rehearsal-*/*' 2>/dev/null | sort)
      if [ -z "$FIRST" ]; then
        echo "no run.json yet"
      else
        echo "first run.json time $FIRST"
        [ "$PRE_T" -lt "$FIRST" ] || fail "prereg.json is not earlier than the first run.json"
      fi
    fi
    ;;
  gt-hash)
    [ -f config/prereg.json ] || { echo "E_NO_PREREG: config/prereg.json does not exist" >&2; exit 2; }
    FOUND=0
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      FOUND=$((FOUND + 1))
      want=$(jq -r --arg p "$f" '.gt_sha256[$p] // empty' config/prereg.json)
      if [ -z "$want" ]; then
        fail "$f has no entry in prereg.json gt_sha256"
      elif [ "$(sha256sum -- "$f" | cut -d' ' -f1)" != "$want" ]; then
        fail "$f does not match its prereg.json hash"
      fi
    done < <(gt_files | sort -u)
    [ "$FOUND" -gt 0 ] || fail "no ground-truth file under $GT_GLOB"
    while IFS= read -r p; do
      [ -f "$p" ] || fail "prereg.json hashes $p, which does not exist"
    done < <(jq -r '(.gt_sha256 // {}) | keys[]' config/prereg.json)
    [ "$FAIL" = 1 ] || echo "ground-truth hashes match $FOUND files"
    ;;
  twins)
    [ -f "$MANIFEST" ] || { echo "E_NO_MANIFEST: $MANIFEST does not exist" >&2; exit 2; }
    N=0
    while IFS=$'\t' read -r plan twin; do
      N=$((N + 1))
      if [ -z "$twin" ]; then fail "planted plan $plan names no twin"; elif [ ! -f "$twin" ]; then fail "twin $twin of $plan does not exist"; fi
    done < <(jq -r '.planted[] | [.plan // "?", .twin // ""] | @tsv' "$MANIFEST")
    [ "$N" -gt 0 ] || fail "$MANIFEST lists no planted plan"
    [ "$FAIL" = 1 ] || echo "every one of $N planted plans has a twin"
    ;;
esac
[ "$FAIL" = 0 ] || exit 1
echo OK
