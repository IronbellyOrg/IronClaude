#!/usr/bin/env bash
# Sweeper launcher (DESIGN 2.4). Never writes a findings block; never a merge input; no retry.
# run-sweeper.sh --pkgdir <runs/row/pkg> --sb <SBR/sb/runid/pkg> --board <B> --model <m> --kill-ms <T0+kill> --k <k> --settings <file>
set -u -o pipefail
. "$(dirname "$0")/lib/common.sh"
shopt -u patsub_replacement 2>/dev/null || true
PKGDIR="" SB="" B="" MODEL="" KILL="" K="" SETTINGS=""
while [ $# -gt 0 ]; do case "$1" in
  --pkgdir) PKGDIR=$2;; --sb) SB=$2;; --board) B=$2;; --model) MODEL=$2;; --kill-ms) KILL=$2;; --k) K=$2;;
  --settings) SETTINGS=$2;; *) echo "unknown arg $1" >&2; exit 2;; esac; shift 2; done
OUT=$PKGDIR/sweeper; mkdir -p "$OUT"
S=$(now_ms)
meta_skip() { jq -n --arg m "$MODEL" --argjson s "$S" --arg why "$1" \
  '{model:$m,model_ok:null,skipped_late:($why=="late"),skipped_k0:($why=="k0"),start_ms:null,end_ms:null,decided_ms:$s,exit:null,output_tokens:0,session_id:""}' > "$OUT/sw-1.meta.json"; }
if [ "$K" -le 0 ]; then meta_skip k0; exit 0; fi
TO=$(awk -v d="$KILL" -v n="$S" 'BEGIN{printf "%.3f", (d-n)/1000}')
if awk -v t="$TO" 'BEGIN{exit !(t <= 10)}'; then meta_skip late; exit 0; fi
T=$(cat "$R2_HOME/config/sweeper-brief.tmpl")
T=${T//\{CAND\}/$SB/cand/candidate.md}; T=${T//\{SRC\}/$SB/cand/source.md}; T=${T//\{POST\}/$B/bin/panel-post}
T=${T//\{CAP\}/$((2 * K))}
for m in M1 M2 M6 M7 M9; do T=${T//\{$m\}/$(jq -r --arg m $m '.moves[$m]' "$CATALOGUE")}; done
( cd "$SB/repo" && timeout "$TO" claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
    --disallowedTools Edit Write NotebookEdit --settings "$SETTINGS" <<<"$T" ) > "$OUT/sw-1.json" 2> "$OUT/sw-1.err"
RC=$?; E=$(now_ms)
jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$OUT/sw-1.json" > "$OUT/sw-1.md" 2>/dev/null
OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$OUT/sw-1.json" 2>/dev/null)
TOKALL=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/sw-1.json" 2>/dev/null)
SID=$(jq -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$OUT/sw-1.json" 2>/dev/null)
LOWOBS=$(echo "$OBS" | tr 'A-Z' 'a-z'); LOWEXP=$(echo "$MODEL" | tr 'A-Z' 'a-z')
MOK=false; [ -n "$OBS" ] && [ "$OBS" != "<synthetic>" ] && { [ "$LOWOBS" = "$LOWEXP" ] || [ "$LOWOBS" = "$LOWEXP-build" ]; } && MOK=true
jq -n --arg m "$MODEL" --arg obs "$OBS" --argjson mok $MOK --argjson s "$S" --argjson e "$E" --argjson rc $RC \
  --argjson tok "${TOKALL:-0}" --arg sid "$SID" --argjson to "$TO" \
  '{model:$m,observed_model:$obs,model_ok:$mok,skipped_late:false,skipped_k0:false,start_ms:$s,end_ms:$e,timeout_s:$to,
    exit:$rc,killed:($rc==124),output_tokens:$tok,session_id:$sid}' > "$OUT/sw-1.meta.json"
$MOK
