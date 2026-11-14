#!/usr/bin/env bash
# anon.sh <merged-1.md> <merged-anon.md>: anonymiser for judging (design 5.1 step 4, R-29).
# Writes label-key.json next to the output. Exit 1 when a forbidden string survives (anon_failed).
set -u -o pipefail
IN=$1; OUT=$2
HERE=$(cd "$(dirname "$0")/.." && pwd)
REPO=${R4_REPO:-$(cd "$HERE/../../../../.." && pwd)}
EVAL="$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
KEY="$(dirname "$OUT")/label-key.json"
mkdir -p "$(dirname "$OUT")"
# every reviewer id the panels use
mapfile -t ALL < <(jq -r '.panels[] | .flagger.rid, .adjudicators[].rid' "$HERE/frozen/panels.json" | sort -u)
PRESENT=(); for id in "${ALL[@]}"; do grep -qw -- "$id" "$IN" && PRESENT+=("$id"); done
mapfile -t SHUF < <(printf '%s\n' "${PRESENT[@]}" | shuf)
cp "$IN" "$OUT.tmp"
MAP="{}"; i=1
for id in "${SHUF[@]}"; do
  [ -n "$id" ] || continue
  # case-sensitive whole-word replacement; the check below is case-insensitive
  perl -pi -e "s/(?<![A-Za-z0-9_-])\Q$id\E(?![A-Za-z0-9_-])/R$i/g" "$OUT.tmp"
  MAP=$(jq --arg k "$id" --arg v "R$i" '. + {($k): $v}' <<<"$MAP"); i=$((i + 1))
done
E="$EVAL" perl -pi -e '
  s{^candidate: \S+ sha256 ([0-9a-f]{8})[0-9a-f]*}{candidate: <candidate file> sha256 $1};
  s{report \S+?(?=,|\s|$)}{report <redacted>}g;
  s{[^\s"'"'"'()<>]*(?:evalsb-collab-r4|r4-flag-and-adjudicate|20261113-collab)[^\s"'"'"'()<>,]*}{<redacted>}g;
  s{\Q$ENV{E}\E}{<EVAL>}g;
  s{,?\s*"origin"\s*:\s*"(?:own|peer)"\s*,?}{ my $m=$&; ($m=~/^,/ && $m=~/,$/) ? "," : "" }ge;
  s{\[panel card c[0-9]+\]}{}gi;
  s{panel card c[0-9]+}{}gi;
  s{\bcards? c[0-9]+: passed}{}gi;
  s{panel card}{}gi;
  s{\bcards? c[0-9]+\b}{}gi;
  s{\b(?:a|another|the) peer reviewer\b}{a reviewer}gi;
' "$OUT.tmp"
mv "$OUT.tmp" "$OUT"
jq -n --argjson m "$MAP" '{reviewer_labels:$m}' > "$KEY"
# forbidden strings: only a rule bug lets one survive
PAT='"origin":|panel card|\bcards? c[0-9]+\b|evalsb-collab|/tmp/jdg|r4-flag|20261113-collab'
for id in "${ALL[@]}"; do PAT="$PAT|(^|[^A-Za-z0-9_-])${id}([^A-Za-z0-9_-]|$)"; done
if grep -qiP -- "$PAT" "$OUT"; then
  grep -noiP -- "$PAT" "$OUT" | head -5 >&2
  echo "anon_failed" >&2
  exit 1
fi
exit 0
