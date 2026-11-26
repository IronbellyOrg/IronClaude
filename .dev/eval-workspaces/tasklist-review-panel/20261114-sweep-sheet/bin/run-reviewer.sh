#!/usr/bin/env bash
# run-reviewer.sh [--raw] <RUN abs> <doc> <reviewer_id> <model> <hang_s>   < brief file   (DESIGN 11.1, 10 row 8, DD-8)
# Runs ONE first-review reviewer in a fresh `claude -p` session. Adapted from RR (tools/run-reviewer.sh); the changes
# are the rows of DESIGN 11.1:
#   RR 6-12   output goes to RUN/reviews; the candidate and the source are SB/cand/<doc>/ (built by build-sandbox.sh)
#   RR 13-17  the brief is the file on stdin (scaffold/briefs.py wrote it); its sha256 goes to the meta file
#   RR 19-44, 65-83  the model ladder and the second attempt are gone: NOFALLBACK=1 is required, one attempt, no retry
#   RR 48     `cd SB/<doc>/repo` (repo-raw with --raw), `timeout <hang_s>`, the flags of RR line 48 unchanged
#   RR 50-56  only the final result message is kept; the model-identity check is kept
#   RR 57     BLOCK_OK is `parse_block` ok after H2 on a temporary copy (sweep normalise); a missing ledger-v1 block
#             does not make it false (DESIGN 9.1). With --raw (arm Z0-raw, which skips H2) it is `parse_block` ok on
#             the raw text.
#   RR 58, 85-87  meta.json and cost.json, plus hang_s, killed and prompt_sha256
# Files written under RUN/reviews: <rid>.attempt1.{json,err,md,meta.json}, <rid>.meta.json, <rid>.cost.json and, only
# when the reviewer is accepted (status ok), <rid>.md (the report the check, H2 and the merge read).
# Gaps in the design resolved here:
#   R1  `status` in meta.json is one of ok, killed, invalid, error (DESIGN 10 row 8 names the three failures, not the
#       tests): killed = the hang guard fired (timeout exit 124, or 137 after the KILL that follows it); error = an API
#       error text, an is_error result, a non-zero exit or an empty report; invalid = a clean run whose model identity
#       differs from the one asked for, or whose findings block does not parse. The first match wins in that order.
#   R2  hang_s, killed and prompt_sha256 are written to both meta.json and cost.json (11.1 row 58 names the two files
#       together).
#   R3  the scripts start no model unless the first `claude` on PATH is the fake of the tests, whenever a FAKE_*
#       variable is set (a test environment): E_NOT_FAKE otherwise.
# Exit: 0 reviewer accepted; 1 reviewer recorded as killed, invalid or error; 2 usage or refusal (nothing was run).
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  sed -n '2,3p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
RAW=0
if [ "${1:-}" = "--raw" ]; then RAW=1; shift; fi
[ $# -eq 5 ] || usage
RUN=$1 DOC=$2 RID=$3 MODEL=$4 HANG=$5
[[ $DOC =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "E_DOC: bad document id: $DOC" >&2; exit 2; }
[[ $RID =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "E_RID: bad reviewer id: $RID" >&2; exit 2; }
[[ $HANG =~ ^[0-9]+(\.[0-9]+)?$ ]] || { echo "E_HANG: not a number of seconds: $HANG" >&2; exit 2; }
sw_assert_nofallback || exit 2
sw_assert_model "$MODEL" || exit 2
sw_assert_writable "$RUN" || exit 2
if [ -n "${FAKE_CALL_LOG:-}${FAKE_SCENARIO:-}${FAKE_SCENARIOS:-}${FAKE_WRITE:-}${FAKE_PROBE:-}" ] &&
  [ "$(command -v claude)" != "$SW/tests/fakes/claude" ]; then
  echo "E_NOT_FAKE: a FAKE_* variable is set but the first claude on PATH is $(command -v claude)" >&2
  exit 2
fi

if [ "$RAW" = 1 ]; then SUB=repo-raw; else SUB=repo; fi
REPO_SB=$SB/$DOC/$SUB
[ -d "$REPO_SB" ] || { echo "E_SANDBOX_MISSING: $REPO_SB" >&2; exit 2; }
[ -f "$SB/cand/$DOC/candidate.md" ] || { echo "E_CANDIDATE: $SB/cand/$DOC/candidate.md missing" >&2; exit 2; }
OUT=$RUN/reviews
mkdir -p "$OUT"

umask 077
TMPD=$(mktemp -d /tmp/run-reviewer.XXXXXXXX) || exit 2
trap 'rm -rf -- "$TMPD"' EXIT
PROMPT=$TMPD/prompt.txt
cat >"$PROMPT"
[ -s "$PROMPT" ] || { echo "E_BRIEF: the brief on stdin is empty" >&2; exit 2; }
PSHA=$(sha256sum "$PROMPT" | cut -d' ' -f1)

A=$OUT/$RID.attempt1
S=$(sw_now)
( cd "$REPO_SB" && timeout -k 5 "$HANG" claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <"$PROMPT" ) >"$A.json" 2>"$A.err"
RC=$?
W=$(awk -v a="$S" -v b="$(sw_now)" 'BEGIN{printf "%.3f", b - a}')
KILLED=false
{ [ "$RC" -eq 124 ] || [ "$RC" -eq 137 ]; } && KILLED=true

jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$A.json" >"$A.md" 2>/dev/null || : >"$A.md"
OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$A.json" 2>/dev/null)
TOK=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$A.json" 2>/dev/null)
TOKALL=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$A.json" 2>/dev/null)
ISERR=$(jq -r '[.[]|select(.type=="result")|.is_error]|.[0] // false' "$A.json" 2>/dev/null)
APIERR=false
{ grep -q 'API Error' "$A.md" 2>/dev/null || [ "$ISERR" = true ]; } && APIERR=true
LOWOBS=$(echo "$OBS" | tr 'A-Z' 'a-z')
LOWEXP=$(echo "$MODEL" | tr 'A-Z' 'a-z')
MODEL_OK=false
[ -n "$OBS" ] && [ "$OBS" != "<synthetic>" ] && { [ "$LOWOBS" = "$LOWEXP" ] || [ "$LOWOBS" = "$LOWEXP-build" ]; } && MODEL_OK=true

# BLOCK_OK: parse_block after H2 on a temporary copy (a prefix of an exact quote is an exact quote, DESIGN 11.2 H2).
BLOCK_OK=false
if [ -s "$A.md" ]; then
  H2=$(sw_py "$SW/sweep/cli.py" normalise --report "$A.md" --out-dir "$TMPD/h2" --rid "$RID" 2>/dev/null) || H2=
  if [ "$RAW" = 1 ]; then # Z0-raw skips H2: the raw text must parse as written, so no field may have been cut
    [ "$(jq -r '.ok and (.changed | length == 0)' <<<"${H2:-null}" 2>/dev/null)" = true ] && BLOCK_OK=true
  else
    [ "$(jq -r '.ok' <<<"${H2:-null}" 2>/dev/null)" = true ] && BLOCK_OK=true
  fi
fi

if $KILLED; then STATUS=killed
elif $APIERR || [ "$RC" -ne 0 ] || [ ! -s "$A.md" ]; then STATUS=error
elif ! $MODEL_OK || ! $BLOCK_OK; then STATUS=invalid
else STATUS=ok; fi

jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$OBS" --arg st "$STATUS" --arg psha "$PSHA" \
  --argjson mok "$MODEL_OK" --argjson bok "$BLOCK_OK" --argjson w "$W" --argjson hang "$HANG" \
  --argjson tok "${TOK:-0}" --argjson tokall "${TOKALL:-0}" --argjson rc "$RC" --argjson killed "$KILLED" \
  '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:$mok,findings_block:$bok,attempt:1,wall_s:$w,
    output_tokens_main:$tok,output_tokens_all:$tokall,exit:$rc,status:$st,hang_s:$hang,killed:$killed,prompt_sha256:$psha}' \
  >"$A.meta.json"
cp -- "$A.meta.json" "$OUT/$RID.meta.json"
jq '{attempts:1,total_wall_s:.wall_s,total_output_tokens_all:.output_tokens_all,hang_s:.hang_s,killed:.killed,prompt_sha256:.prompt_sha256}' \
  "$A.meta.json" >"$OUT/$RID.cost.json"
rm -f -- "$OUT/$RID.md"
if [ "$STATUS" = ok ]; then
  cp -- "$A.md" "$OUT/$RID.md"
  echo "reviewer $RID ($MODEL): ok in ${W}s"
  exit 0
fi
echo "reviewer $RID ($MODEL): $STATUS in ${W}s" >&2
exit 1
