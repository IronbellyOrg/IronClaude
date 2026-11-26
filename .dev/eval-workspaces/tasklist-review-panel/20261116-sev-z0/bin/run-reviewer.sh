#!/usr/bin/env bash
# usage: run-reviewer.sh <RUN dir> <doc id> <reviewer id> <model> <brief file> <hang_s> [<used_s>]
# One reviewer, one attempt, in a fresh `claude -p` session in the sandbox repo SB/<doc>/repo (DESIGN 9.2, SWD 11.1).
# Built locally to the sibling's written contract. No model ladder, no second attempt (DD-8): NOFALLBACK=1 is required.
# The brief is read from the file on stdin. The call runs under `timeout <hang_s - used_s>` (hang guard, REQ-30);
# used_s is what the panel clock has already used (default 0). Tools are read-only for files (K4).
#
# Writes RUN/reviews/<rid>.attempt1.{json,err,md,meta.json}, <rid>.{md,meta.json,cost.json}. meta.json holds
#   status (ok | killed | invalid | error), killed, invalid and error (booleans that agree with status), model_ok,
#   findings_block / block_ok (FND.parse_block ok after H2 on a temporary copy; a missing ledger-v1 block is not
#   a block error), hang_s, prompt_sha256, wall_s, exit, reviewer_id, expected_model, observed_model, tokens.
# Exit codes: 0 a meta.json was written (whatever its status); 2 usage error or no sandbox repo; 4 refused
# (NOFALLBACK not 1, a model outside the allowlist, or the sibling's sandbox root).
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

if [ $# -lt 6 ] || [ $# -gt 7 ]; then
  echo "usage: run-reviewer.sh <RUN dir> <doc id> <reviewer id> <model> <brief file> <hang_s> [<used_s>]" >&2
  exit 2
fi
RUN=$1 DOC=$2 RID=$3 MODEL=$4 BRIEF=$5 HANG_S=$6 USED_S=${7:-0}

sw_assert_nofallback || exit 4
sw_assert_model "$MODEL" || exit 4
NUM='^[0-9]+(\.[0-9]+)?$'
[[ $HANG_S =~ $NUM ]] && [[ $USED_S =~ $NUM ]] || { echo "E_USAGE: hang_s and used_s are numbers" >&2; exit 2; }
[[ $DOC =~ ^[A-Za-z0-9._-]+$ && $RID =~ ^[A-Za-z0-9._-]+$ ]] || { echo "E_USAGE: bad doc or reviewer id" >&2; exit 2; }
[ -f "$BRIEF" ] || { echo "E_USAGE: no brief file $BRIEF" >&2; exit 2; }
BRIEF=$(realpath -- "$BRIEF") # the call runs after a cd into the sandbox repo
SUB=${RL_SANDBOX_SUB:-repo} # `repo-raw` for arm Z0-raw (set by run-panel.sh)
[[ $SUB =~ ^repo(-raw)?$ ]] || { echo "E_USAGE: RL_SANDBOX_SUB is repo or repo-raw" >&2; exit 2; }
REPO_SB=$SB/$DOC/$SUB
[ -d "$REPO_SB" ] || { echo "E_USAGE: no sandbox repo $REPO_SB" >&2; exit 2; }
sw_assert_writable "$RUN" || exit 2

OUT=$RUN/reviews
mkdir -p "$OUT"
A=$OUT/$RID.attempt1
PROMPT_SHA=$(sha256sum "$BRIEF" | cut -d' ' -f1)
LEFT=$(awk -v h="$HANG_S" -v u="$USED_S" 'BEGIN { r = h - u; if (r < 0.1) r = 0.1; printf "%.3f", r }')

S=$(sw_now)
(cd "$REPO_SB" && timeout --kill-after=2 "$LEFT" claude -p --model "$MODEL" --output-format json --no-session-persistence \
  --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <"$BRIEF") >"$A.json" 2>"$A.err"
RC=$?
WALL=$(awk -v s="$S" -v e="$(sw_now)" 'BEGIN { printf "%.3f", e - s }')

KILLED=false
{ [ "$RC" -eq 124 ] || [ "$RC" -eq 137 ]; } && KILLED=true
jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$A.json" >"$A.md" 2>/dev/null || : >"$A.md"
OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$A.json" 2>/dev/null)
TOK=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$A.json" 2>/dev/null)
TOKALL=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$A.json" 2>/dev/null)
APIERR=false
grep -q 'API Error' "$A.md" 2>/dev/null && APIERR=true
LOWOBS=$(echo "$OBS" | tr 'A-Z' 'a-z')
LOWEXP=$(echo "$MODEL" | tr 'A-Z' 'a-z')
MODEL_OK=false
if [ -n "$OBS" ] && [ "$OBS" != "<synthetic>" ] && { [ "$LOWOBS" = "$LOWEXP" ] || [ "$LOWOBS" = "$LOWEXP-build" ]; }; then
  MODEL_OK=true
fi

# BLOCK_OK: the findings block parses with FND.parse_block after H2, on a temporary copy (the report stays raw)
BLOCK_OK=false
if [ -s "$A.md" ]; then
  TMP=$(mktemp -d "${TMPDIR:-/tmp}/rl-block.XXXXXXXX") || exit 2
  trap 'rm -rf "$TMP"' EXIT
  cp "$A.md" "$TMP/in.md"
  BLOCK_OK=$(sw_py -I -B -c '
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scaffold import normalise
tmp = Path(sys.argv[2])
try:
    print("true" if normalise.normalise_file(tmp / "in.md", tmp / "out", "r")["ok"] else "false")
except Exception:
    print("false")
' "$SW" "$TMP" 2>/dev/null) || BLOCK_OK=false
  [ "$BLOCK_OK" = true ] || BLOCK_OK=false
fi

STATUS=ok INVALID=false ERROR=false
if $KILLED; then
  STATUS=killed
elif [ "$RC" -ne 0 ] || $APIERR || [ ! -s "$A.md" ]; then
  STATUS=error ERROR=true
elif ! $MODEL_OK || ! $BLOCK_OK; then
  STATUS=invalid INVALID=true
fi

jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$OBS" --argjson mok "$MODEL_OK" --argjson bok "$BLOCK_OK" \
  --argjson w "$WALL" --argjson tok "${TOK:-0}" --argjson tokall "${TOKALL:-0}" --argjson rc "$RC" \
  --argjson hang "$HANG_S" --argjson killed "$KILLED" --argjson invalid "$INVALID" --argjson err "$ERROR" \
  --arg status "$STATUS" --arg sha "$PROMPT_SHA" '{
    reviewer_id: $rid, expected_model: $exp, observed_model: $obs, model_ok: $mok,
    findings_block: $bok, block_ok: $bok, attempt: 1, wall_s: $w, output_tokens_main: $tok,
    output_tokens_all: $tokall, exit: $rc, hang_s: $hang, status: $status, killed: $killed,
    invalid: $invalid, error: $err, prompt_sha256: $sha}' >"$A.meta.json"
cp "$A.md" "$OUT/$RID.md"
cp "$A.meta.json" "$OUT/$RID.meta.json"
jq '{attempts: 1, total_wall_s: .wall_s, total_output_tokens_all: .output_tokens_all}' "$A.meta.json" >"$OUT/$RID.cost.json"
