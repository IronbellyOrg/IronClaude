#!/usr/bin/env bash
# anon.sh SRC OUTROOT   (DESIGN 11.3, REQ-43)
# Anonymises one merged report for the blind judge. SRC is RUN/merged/merged-1.md. The copy is written to
# OUTROOT/<label>/merged-anon.md; the random label (j plus six hex digits, never a folder that already exists in OUTROOT)
# is the only line printed on stdout. The caller keeps the label-to-run key; this script writes none.
# The rules are those of EVAL/tools/tmp-scripts/anon-b11.sh (results/anon-rules.md):
#   1. every root path (the run folder, SB, EVAL, SW, REPO) becomes <RUN>, <SB>, <EVAL>, <SW>, <REPO>
#   2. the line `candidate: <path> sha256 ...` loses its path: `candidate: <candidate file> sha256 ...`
#   3. `report <path>` (the reviewers list of the merged report) becomes `report <redacted>`
#   4. every reviewer id (t1b-1, t2b-1, t3-1 ...) becomes R1 ... Rn, numbered in sorted order of the ids
# The judge therefore sees no arm, run, reviewer or model name that the report itself does not carry.
set -u -o pipefail
source "$(dirname "$0")/common.sh"
SRC=${1:?usage: anon.sh SRC OUTROOT}
OUT=${2:?usage: anon.sh SRC OUTROOT}
[ -f "$SRC" ] || { echo "E_ARG: $SRC is not a file" >&2; exit 2; }
sw_assert_writable "$OUT" || exit 2
RUN=$(dirname "$(dirname "$(realpath -m -- "$SRC")")")

esc() { printf '%s' "$1" | sed 's/[][\.*^$|/]/\\&/g'; }
TMPD=$(mktemp -d /tmp/sw-anon.XXXXXXXX) || exit 2
trap 'rm -rf "$TMPD"' EXIT

PATHS=(-e "s|$(esc "$RUN")|<RUN>|g")
names=(SB EVAL SW REPO)
roots=("$SB" "$EVAL" "$SW" "$REPO")
for i in "${!roots[@]}"; do
  PATHS+=(-e "s|$(esc "${roots[$i]}")|<${names[$i]}>|g")
done
PATHS+=(
  -e 's|^candidate: .* sha256|candidate: <candidate file> sha256|'
  -e 's|report <[A-Z]*>[^ ,]*|report <redacted>|g'
  -e 's|report /[^ ,]*|report <redacted>|g'
)
sed "${PATHS[@]}" "$SRC" >"$TMPD/p.md" || exit 2

# Reviewer ids: the pattern of the panel ids, plus every id named in the reviewers list.
IDS=$({
  grep -oE '\bt[0-9]+[a-z]*-[0-9]+\b' "$TMPD/p.md"
  sed -nE 's/^- ([^ :]+): report .*/\1/p' "$TMPD/p.md"
} | sort -u)
IDX=()
i=1
for id in $IDS; do
  IDX+=(-e "s/\\b$(esc "$id")\\b/R$i/g")
  i=$((i + 1))
done
mkdir -p "$OUT" || exit 2
while :; do
  L=$(printf 'j%06x' "$(shuf -n1 -i 0-16777215)")
  mkdir "$OUT/$L" 2>/dev/null && break
done
if [ ${#IDX[@]} -gt 0 ]; then
  sed "${IDX[@]}" "$TMPD/p.md" >"$OUT/$L/merged-anon.md" || exit 2
else
  cp "$TMPD/p.md" "$OUT/$L/merged-anon.md" || exit 2
fi
printf '%s\n' "$L"
