#!/usr/bin/env bash
# check-order.sh {freeze|prereg|twins} [options]   (DESIGN AO-5, REQ-33, REQ-36, REQ-44; read-only)
# Checks the order of the things that the experiment must do in a fixed order, by commit times, and the hashes that tie them.
# It only reads: git log, git rev-parse (a tag is read with those, never made), sha256sum, jq. Exit 0 the order holds, 1 it does
# not (the reason is printed), 2 a bad argument or a missing input.
#   freeze  --repo DIR --freeze FILE --gt PATH [--gt PATH ...]
#           The freeze tag named by `freeze_tag` in FILE (default <SW>/config/freeze.json) exists and its commit time is earlier
#           than the first commit that added any file under a --gt path (default <SW>/holdout-gt); the ground truth must also
#           be committed (an uncommitted ground truth proves nothing). And every file in FILE's `files` still has the recorded
#           sha256 (an extractor changed after the freeze fails here). The tree of the files is the folder above FILE's folder.
#   prereg  --repo DIR --prereg FILE --runs DIR [--gt-dir DIR]
#           FILE (default <SW>/config/prereg.json) is committed, and its first commit is earlier than the first run.json under
#           DIR (default <SW>/runs): the first commit that added one, or, for runs that are not committed, the oldest file time.
#           With no run.json yet the order holds. If FILE has `ground_truth_sha256` {document: sha256}, each ground-truth file
#           (DIR/<doc>.json or DIR/<doc>/ground-truth.json under --gt-dir, default <SW>/holdout-gt) must have that sha256.
#   twins   --manifest FILE
#           Every entry of `planted` in the manifest names a `twin` file (relative to the manifest's folder) that exists.
# --repo defaults to the repository that holds this script. Times are commit times (%ct, whole seconds): equal times fail,
# because the order cannot be shown.
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
MODE=${1:-}
case "$MODE" in freeze | prereg | twins) shift ;; *) usage ;; esac
REPOD=$REPO FREEZE=$SW/config/freeze.json PREREG=$SW/config/prereg.json RUNS=$SW/runs GTDIR=$SW/holdout-gt MANIFEST=
GTS=()
while [ $# -gt 0 ]; do
  [ $# -ge 2 ] || usage
  case "$1" in
    --repo) REPOD=$2 ;;
    --freeze) FREEZE=$2 ;;
    --gt) GTS+=("$2") ;;
    --prereg) PREREG=$2 ;;
    --runs) RUNS=$2 ;;
    --gt-dir) GTDIR=$2 ;;
    --manifest) MANIFEST=$2 ;;
    *) usage ;;
  esac
  shift 2
done

fail() { echo "ORDER_FAIL: $*" >&2; exit 1; }
rel() { # rel PATH: PATH relative to the repository top, for git log
  local top p
  top=$(git -C "$REPOD" rev-parse --show-toplevel) || exit 2
  p=$(realpath -m -- "$1")
  echo "${p#"$(realpath -m -- "$top")"/}"
}
first_add_time() { # first_add_time PATHSPEC...: the earliest commit time of a commit that added a file under the pathspecs
  local p t out=""
  for p in "$@"; do
    # the smallest commit time among the commits that added a file (history order is not time order after a rebase)
    t=$(git -C "$REPOD" log --diff-filter=A --format=%ct -- "$p" 2>/dev/null | sort -n | head -n 1)
    if [ -n "$t" ] && { [ -z "$out" ] || [ "$t" -lt "$out" ]; }; then
      out=$t
    fi
  done
  echo "$out"
}
rel_all() { # rel_all PATH...: each path relative to the repository top
  local p
  for p in "$@"; do rel "$p"; done
}

case "$MODE" in
  freeze)
    [ -f "$FREEZE" ] || { echo "E_ARG: no freeze record $FREEZE" >&2; exit 2; }
    [ ${#GTS[@]} -gt 0 ] || GTS=("$GTDIR")
    NAME=$(jq -r '.freeze_tag // empty' "$FREEZE")
    [ -n "$NAME" ] || fail "$FREEZE records no freeze_tag"
    REF=refs/tags/$NAME
    git -C "$REPOD" rev-parse -q --verify "$REF" >/dev/null || fail "the freeze tag $NAME does not exist in $REPOD (a person makes it; bin/freeze.sh prints the command)"
    T_FREEZE=$(git -C "$REPOD" log -1 --format=%ct "$REF") || exit 2
    mapfile -t GT_SPECS < <(rel_all "${GTS[@]}")
    T_GT=$(first_add_time "${GT_SPECS[@]}")
    [ -n "$T_GT" ] || fail "the ground truth under ${GTS[*]} is not committed, so its order cannot be shown"
    [ "$T_FREEZE" -lt "$T_GT" ] || fail "the freeze tag $NAME ($T_FREEZE) is not earlier than the first ground-truth commit ($T_GT)"
    TREE=$(dirname "$(dirname "$(realpath -m -- "$FREEZE")")")
    BAD=0
    while IFS=$'\t' read -r f h; do
      [ -n "$f" ] || continue
      now=$(sha256sum -- "$TREE/$f" 2>/dev/null | cut -d' ' -f1)
      if [ "$now" != "$h" ]; then
        echo "ORDER_FAIL: $f changed after the freeze (recorded ${h:0:12}, now ${now:0:12})" >&2
        BAD=1
      fi
    done < <(jq -r '.files | to_entries[] | [.key, .value] | @tsv' "$FREEZE")
    [ "$BAD" = 0 ] || exit 1
    echo "ORDER_OK freeze: tag $NAME ($T_FREEZE) is earlier than the first ground-truth commit ($T_GT); every frozen file is unchanged"
    ;;
  prereg)
    [ -f "$PREREG" ] || fail "$PREREG does not exist: write it with analysis/analyze.py prereg --write"
    T_PRE=$(first_add_time "$(rel "$PREREG")")
    [ -n "$T_PRE" ] || fail "$PREREG is not committed, so its order cannot be shown"
    T_RUN=$(first_add_time ":(glob)$(rel "$RUNS")/**/run.json")
    if [ -z "$T_RUN" ] && [ -d "$RUNS" ]; then
      T_RUN=$(find "$RUNS" -name run.json -printf '%T@\n' 2>/dev/null | sort -n | head -n 1)
      T_RUN=${T_RUN%.*}
    fi
    if [ -n "$T_RUN" ]; then
      [ "$T_PRE" -lt "$T_RUN" ] || fail "$PREREG ($T_PRE) is not earlier than the first run.json ($T_RUN)"
    fi
    BAD=0
    while IFS=$'\t' read -r doc want; do
      [ -n "$doc" ] || continue
      gt=
      for c in "$GTDIR/$doc.json" "$GTDIR/$doc/ground-truth.json"; do [ -f "$c" ] && gt=$c && break; done
      [ -n "$gt" ] || { echo "ORDER_FAIL: no ground-truth file for $doc under $GTDIR" >&2; BAD=1; continue; }
      have=$(sha256sum -- "$gt" | cut -d' ' -f1)
      [ "$have" = "$want" ] || { echo "ORDER_FAIL: the ground truth of $doc has sha256 ${have:0:12}, prereg.json records ${want:0:12}" >&2; BAD=1; }
    done < <(jq -r '(.ground_truth_sha256 // {}) | to_entries[] | [.key, .value] | @tsv' "$PREREG")
    [ "$BAD" = 0 ] || exit 1
    WHEN="any run (none has started)"
    [ -z "$T_RUN" ] || WHEN="the first run.json ($T_RUN)"
    echo "ORDER_OK prereg: ${PREREG##*/} ($T_PRE) is earlier than $WHEN; the ground-truth hashes match"
    ;;
  twins)
    [ -f "$MANIFEST" ] || { echo "E_ARG: --manifest FILE is required" >&2; exit 2; }
    DIR=$(dirname "$MANIFEST")
    BAD=0
    N=0
    while IFS=$'\t' read -r plan twin; do
      N=$((N + 1))
      if [ -z "$twin" ]; then
        echo "ORDER_FAIL: planted plan $plan has no clean twin" >&2
        BAD=1
      elif [ ! -f "$DIR/$twin" ]; then
        echo "ORDER_FAIL: the twin $twin of $plan does not exist" >&2
        BAD=1
      fi
    done < <(jq -r '.planted[] | [(.plan // .id // "?"), (.twin // "")] | @tsv' "$MANIFEST")
    [ "$BAD" = 0 ] || exit 1
    echo "ORDER_OK twins: all $N planted plans have an existing twin"
    ;;
esac
