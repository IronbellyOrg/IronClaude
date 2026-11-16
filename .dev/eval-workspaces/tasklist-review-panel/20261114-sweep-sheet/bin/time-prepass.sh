#!/usr/bin/env bash
# time-prepass.sh [options] <snapshot>   (DESIGN 12.1, 12.5, DD-5, DD-10; IMPLEMENTATION step 9 checkpoint)
# Runs `sweep prepass` once on a repository snapshot and prints and records the wall-clock seconds (S1).
# The seconds cover the whole command, Python start-up included, as the launcher's `timeout` sees it.
#   --candidate FILE   the candidate plan   (default: fixtures/plans/p_basic.md)
#   --source FILE      the source document  (default: fixtures/plans/source.md; "none" runs without one)
#   --seed N           the seed             (default: 1)
#   --panel NAME       the panel            (default: primary)
#   --record FILE      TSV file that gets one appended line (default: SW/results/prepass-timing.tsv)
#   --doc DOC          the snapshot is SB/DOC/repo, the candidate SB/cand/DOC/candidate.md and the source
#                      SB/cand/DOC/source.md (what bin/build-sandbox.sh built); no <snapshot> argument
# The snapshot is only read (git ls-files, git grep). The pre-pass output goes to a private folder under /tmp that is
# removed on exit; the record file must resolve under SW, SB or /tmp (K1).
# Exit 0: the pre-pass succeeded. Exit 1: it failed or was cut off after 300 s (the seconds are still printed and
# recorded). Exit 2: a usage error. Output: `prepass_s=<seconds> rc=<n> snapshot=<path>` then `scope: <string>`.
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
CAND=$SW/fixtures/plans/p_basic.md
SRC=$SW/fixtures/plans/source.md
SEED=1
PANEL=primary
RECORD=$SW/results/prepass-timing.tsv
DOC=
SNAP=
while [ $# -gt 0 ]; do
  case "$1" in
    -h | --help) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    --candidate | --source | --seed | --panel | --record | --doc)
      [ $# -ge 2 ] || usage
      case "$1" in
        --candidate) CAND=$2 ;;
        --source) SRC=$2 ;;
        --seed) SEED=$2 ;;
        --panel) PANEL=$2 ;;
        --record) RECORD=$2 ;;
        --doc) DOC=$2 ;;
      esac
      shift
      ;;
    -*) usage ;;
    *)
      [ -z "$SNAP" ] || usage
      SNAP=$1
      ;;
  esac
  shift
done
if [ -n "$DOC" ]; then
  [ -z "$SNAP" ] || usage
  [[ $DOC =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "E_DOC: bad document id: $DOC" >&2; exit 2; }
  SNAP=$SB/$DOC/repo
  CAND=$SB/cand/$DOC/candidate.md
  SRC=$SB/cand/$DOC/source.md
fi
[ -n "$SNAP" ] || usage
[[ $SEED =~ ^[0-9]+$ ]] || { echo "E_SEED: not a number: $SEED" >&2; exit 2; }
[ -d "$SNAP" ] || { echo "E_SNAPSHOT: not a directory: $SNAP" >&2; exit 2; }
[ -f "$CAND" ] || { echo "E_CANDIDATE: not a file: $CAND" >&2; exit 2; }
SRC_ARGS=()
if [ "$SRC" != none ]; then
  [ -f "$SRC" ] || { echo "E_SOURCE: not a file: $SRC" >&2; exit 2; }
  SRC_ARGS=(--source "$SRC")
fi
sw_assert_writable "$RECORD" || exit 2
mkdir -p "$(dirname "$RECORD")"

umask 077
OUT=$(mktemp -d /tmp/time-prepass.XXXXXXXX) || exit 2
trap 'rm -rf -- "$OUT"' EXIT

T0=$(sw_now)
timeout 300 uv run --frozen --project "$REPO" python "$SW/sweep/cli.py" prepass \
  --candidate "$CAND" ${SRC_ARGS[@]+"${SRC_ARGS[@]}"} --repo "$SNAP" --seed "$SEED" --panel "$PANEL" --out "$OUT" \
  >"$OUT/stdout.txt" 2>"$OUT/stderr.txt"
RC=$?
T1=$(sw_now)
SECS=$(awk -v a="$T0" -v b="$T1" 'BEGIN{printf "%.2f", b - a}')

SCOPE=$(jq -r '.scope // empty' "$OUT/prepass/prepass.json" 2>/dev/null)
[ -n "$SCOPE" ] || SCOPE="(no prepass.json)"
[ "$RC" -eq 0 ] || cat "$OUT/stderr.txt" >&2

printf 'prepass_s=%s rc=%s snapshot=%s\n' "$SECS" "$RC" "$SNAP"
printf 'scope: %s\n' "$SCOPE"
printf '%s\t%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$SNAP" "$SECS" "$RC" "$SCOPE" >>"$RECORD"
[ "$RC" -eq 0 ] || exit 1
exit 0
