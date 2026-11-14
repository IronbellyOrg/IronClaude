#!/usr/bin/env bash
# judge.sh <pkgdir> <merged-anon.md>: runs the unchanged judge-one.sh on one anonymised report (design 5.1 step 5).
# Staging lives in a mktemp /tmp/jdg.* directory outside SBR and EVAL, deleted on every exit path.
# Writes <pkgdir>/scoring/judge-status (ok|judge_failed|judge_wrote_into_eval|judge_setup_failed); exit 0 only on ok.
set -u -o pipefail
PKGDIR=$1; ANON=$2
HERE=$(cd "$(dirname "$0")/.." && pwd)
REPO=${R4_REPO:-$(cd "$HERE/../../../../.." && pwd)}
EVAL="$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
JUDGE="$EVAL/tools/tmp-scripts/judge-one.sh"
SC="$PKGDIR/scoring"; mkdir -p "$SC"
PKG=$(jq -r .pkg "$PKGDIR/panel.json")
status() { echo "$1" > "$SC/judge-status"; }

STAGE=$(mktemp -d /tmp/jdg.XXXXXXXX) || { status judge_setup_failed; exit 1; }
cleanup() { case "$STAGE" in /tmp/jdg.?*) rm -rf -- "$STAGE" ;; esac; }
trap cleanup EXIT
trap 'exit 130' INT TERM HUP

L=$(tr -dc 'A-Z' </dev/urandom | head -c 4)
D="$STAGE/$PKG/$L"; mkdir -p "$D"
cp "$ANON" "$D/merged-anon.md"
C=$(realpath -m --relative-to="$EVAL/arms/scoring/combos" "$STAGE")
if [ "$(realpath -m "$EVAL/arms/scoring/combos/$C")" != "$STAGE" ]; then status judge_setup_failed; exit 1; fi
case "$STAGE/" in "$EVAL"/*) status judge_setup_failed; exit 1 ;; esac
STAMP="$STAGE/.stamp"; touch "$STAMP"; sleep 1

ok=0
for try in 1 2; do
  (cd "$STAGE" && bash "$JUDGE" "$C" "$PKG" "$L") > "$STAGE/judge-one.$try.out" 2>&1
  if jq -e 'has("gt_covered_any") and has("gt_covered_blocking") and has("wrong_blockers")' "$D/score.json" >/dev/null 2>&1 \
     && ! jq -r '[.[]?|select(.type=="result")|.result]|.[0] // ""' "$D/judge.json" 2>/dev/null | grep -q 'API Error'; then
    ok=1; break
  fi
  for f in score.json judge.json judge.err; do [ -e "$D/$f" ] && mv "$D/$f" "$D/${f%.*}.attempt$try.${f##*.}"; done
done
if [ -n "$(find "$EVAL" -newer "$STAMP" -print -quit 2>/dev/null)" ]; then st=judge_wrote_into_eval; ok=0
elif [ "$ok" = 1 ]; then st=ok; else st=judge_failed; fi
for f in "$D"/score.json "$D"/judge.json "$D"/judge.err "$D"/*.attempt*.*; do [ -e "$f" ] && cp "$f" "$SC/"; done
KEY="$SC/label-key.json"; [ -f "$KEY" ] || echo '{}' > "$KEY"
jq --arg l "$L" --arg s "$STAGE" --arg c "$C" '. + {label:$l, stage:$s, C:$c}' "$KEY" > "$KEY.tmp" && mv "$KEY.tmp" "$KEY"
status "$st"
[ "$st" = ok ]
