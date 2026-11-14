#!/usr/bin/env bash
# Anonymiser (DESIGN 5.2): anon-b11.sh plus collaboration-trace stripping and a self-check (exit 4 on a leak).
# anon.sh --merged <runs/row/pkg/merged-1.md> --out-dir <scoring/opaque/pkg> [--row <row>] [--runid <runid>]
set -u -o pipefail
. "$(dirname "$0")/lib/common.sh"
SRC="" D="" ROW="" RUNID=""
while [ $# -gt 0 ]; do case "$1" in
  --merged) SRC=$2;; --out-dir) D=$2;; --row) ROW=$2;; --runid) RUNID=$2;; *) echo "unknown arg $1" >&2; exit 2;; esac; shift 2; done
mkdir -p "$D"
OPAQUE=$(basename "$(dirname "$D")")
FREE=$(for l in Q R S T U V; do [ -e "$D/$l" ] || echo $l; done)
[ -n "$FREE" ] || { echo "no free label in $D" >&2; exit 3; }
L=$(shuf -n1 <<<"$FREE")
DD=$D/$L; mkdir -p "$DD"
F=$DD/merged-anon.md
IDS=$(grep -oE '\bt[0-9a-z]+-[0-9]+\b' "$SRC" | sort -u)
sed -e "s|$EVAL|<EVAL>|g" -e "s|$OUT|<EVAL>|g" -e "s|$R2_HOME|<EVAL>|g" -e "s|$SBR|<SANDBOX>|g" "$SRC" > "$F"
i=1
for ID in $IDS; do sed -i "s/\b$ID\b/R$i/g" "$F"; i=$((i + 1)); done
sed -i 's|^candidate: <EVAL>/[^ ]*/candidate.md sha256|candidate: <candidate file> sha256|' "$F"
sed -i -E 's/report [^[:space:],]+/report <redacted>/g' "$F"
# BEGIN strip (collaboration traces)
sed -i -E \
  -e 's/,[[:space:]]*"origin"[[:space:]]*:[[:space:]]*"(own|peer)"//g' \
  -e 's/"origin"[[:space:]]*:[[:space:]]*"(own|peer)"[[:space:]]*,?[[:space:]]*//g' \
  -e 's#[^[:space:]]*/board/[^[:space:]]*#<redacted>#g' \
  -e 's/\bf-[0-9]+\b//g' -e 's/\bsw-1\b//g' -e 's/\bhv-1\b//g' \
  -e 's#panel-msg/1##g' -e 's/panel-post//g' -e 's/board\.jsonl//g' \
  -e 's/Search result to check yourself//g' -e 's/not a finding; no conclusion attached//g' "$F"
# END strip
jq -n --arg l "$L" --arg o "$OPAQUE" '{label:$l,opaque:$o}' > "$D/label-key.json"
PAT='"origin"[[:space:]]*:|/board/|panel-(msg|post)|\bf-[0-9]+\b|\bsw-1\b|\bhv-1\b|evalsb-collab|Search result to check'
# whole-word: a short row name such as "res" must not match "restating" in the merge boilerplate
[ -n "$ROW" ] && PAT="$PAT|(^|[^A-Za-z0-9-])$ROW([^A-Za-z0-9-]|\$)"
[ -n "$RUNID" ] && PAT="$PAT|\\b$RUNID\\b"
N=$(grep -cE -- "$PAT" "$F" || true)
if [ "${N:-0}" != 0 ]; then echo "anonymiser self-check failed: $N line(s) leak" >&2; exit 4; fi
echo "$L"
