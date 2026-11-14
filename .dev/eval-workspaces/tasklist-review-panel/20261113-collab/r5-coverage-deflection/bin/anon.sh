#!/usr/bin/env bash
# Anonymise one merged report for the blind judge (DESIGN 5.3; anon-b11.sh:17-25). Prints "<token> <label>".
# usage: anon.sh <row> <pkg>; exit 1 = anon_failed (post-check matched; the package is not judged)
set -u -o pipefail
ROW=$1; PKG=$2
R5=$(cd "$(dirname "$0")/.." && pwd); OUTR=${R5_OUT:-$R5}
EVAL=${R5_EVAL:-$(cd "$R5/../../20261111-a1" && pwd)}
D=$OUTR/runs/$ROW/$PKG; SRC=$D/merged-1.md
ARM=$(jq -r .arm "$D/run.json")
TOKEN=$(openssl rand -hex 6); L=$(printf 'Q\nR\nS\nT\nU\nV\n' | shuf -n1)
DD=$OUTR/scoring/$TOKEN/$PKG/$L; mkdir -p "$DD"; F=$DD/merged-anon.md
esc() { printf '%s' "$1" | sed 's/[][\.*^$/|]/\\&/g'; }
IDRE='\b(t1b-1|t2b-1|t3-1|t4-1|t4-2)\b'
MARKRE='\bM(10|[1-9])\b|panel request|catalogue moves?|peer coverage|requested Tasks?'
REDACT=$(grep -oiE "$MARKRE|\"origin\"[[:space:]]*:[[:space:]]*\"(peer|own)\"|[^[:space:]]*(r5-coverage-deflection|evalsb-collab-r5|20261113-collab)[^[:space:]]*" "$SRC" | wc -l)
cp "$SRC" "$F"
i=1
for ID in $(grep -oiE "$IDRE" "$SRC" | tr 'A-Z' 'a-z' | sort -u); do sed -i -E "s/\b$ID\b/R$i/gI" "$F"; i=$((i+1)); done
sed -i "s|$(esc "$EVAL")|<EVAL>|gI" "$F"
sed -i 's|^candidate: <EVAL>/[^ ]*/candidate.md sha256|candidate: <candidate file> sha256|' "$F"
sed -i 's|report <EVAL>/[^ ,]*|report <redacted>|g' "$F"
sed -i -E 's#[^[:space:]]*(r5-coverage-deflection|evalsb-collab-r5|20261113-collab)[^[:space:]]*#<redacted>#gI' "$F"
sed -i -E 's/,?[[:space:]]*"origin"[[:space:]]*:[[:space:]]*"(peer|own)"//gI' "$F"
sed -i -E "s/$MARKRE/<redacted>/gI" "$F"
N=$(grep -ciE '"origin"[[:space:]]*:|/board/|evalsb-collab|20261113-collab|coverage-deflection|\b(t1b-1|t2b-1|t3-1|t4-1|t4-2)\b|\bM(10|[1-9])\b|panel request|catalogue move|peer coverage|requested task' "$F")
ST=ok; [ "$N" -eq 0 ] || ST=anon_failed
mkdir -p "$OUTR/results"
jq -nc --arg t "$TOKEN" --arg r "$ROW" --arg p "$PKG" --arg l "$L" --arg a "$ARM" --argjson n "$REDACT" --arg s "$ST" \
  '{token:$t,row:$r,pkg:$p,label:$l,arm:$a,redactions:$n,status:$s}' >> "$OUTR/results/scoring-keys.jsonl"
f=$D/pkg-status.json; [ -f "$f" ] || echo '{}' > "$f"
jq --arg s "$ST" --argjson n "$N" '.anon=$s|.anon_postcheck=$n' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
echo "$TOKEN $L"
[ "$ST" = ok ]
