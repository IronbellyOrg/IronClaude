#!/usr/bin/env bash
# usage: run-panel.sh --arm {Z0-raw|Z0|K|RL} --panel {primary|haiku|sonnet} --doc <document id> --replicate <n> --block <n>
#                     --seed <int> --run-id <id> [--b <seconds>] [--b-min <seconds>] [--c-luna <seconds>] [--dry-run]
# One panel (three reviewers in parallel) on one document, written to RL/runs/<run-id>/ (DESIGN 2.2, 9.1, 9.3, 9.4, 9.6).
# The sandbox (bin/build-sandbox.sh) must exist. NOFALLBACK=1 is required (one attempt per reviewer, DD-8).
#
#   --b        this run's b in seconds (the same-block Z0 median of the slowest reviewer): the hang guard and the ember
#              re-ask condition. Default: the planning value of config/values.json for the document.
#   --b-min    the b the lens row cap is derived from (the smallest b of the panel in the stage, DR-4). Default: the
#              smallest b of the panel in config/values.json. A value too small for the lens exits 3 (no_budget).
#   --c-luna   seconds per ledger row of a luna reviewer, for the lens row cap lens_row_cap(b_min, c_luna) (RL arm only).
#              Default: the planning value of config/values.json. bin/run-schedule.sh passes the timing spike's c.
#   --dry-run  writes briefs/, lens/ and run.json, prints the three claude command lines with the brief sha256, starts nothing.
# Environment: RL_SANDBOX_SUB is set here (repo, or repo-raw for Z0-raw); RL_LENSES (a lens table under /tmp or RL) and
# RL_RUNS_ROOT (the folder of run folders, default RL/runs; under /tmp or RL) are test hooks; RL_FORCE_EXC=lens|check|reask raises in that component (bin/rl-env.sh); VERIFIER must be 0 (REQ-46: the
# optional verifier is not built and never sits on the clock).
# Order: sandbox check, t0, render (RL: lens render, else Z0, K or Z0-raw briefs), reviewers in parallel (rev_end, and for
# the ember a re-ask as soon as its report is read), check (RL), stop the clock, then outside it H2, merge, the sandbox
# check and the records. The clock is the epoch in seconds of `date +%s.%3N`, one clock for every stamp.
# Exit codes: 0 done (also fallback, killed reviewer, check_skipped, merge_refused); 2 usage error, sandbox or run folder
# invalid, or a sandbox that a reviewer left dirty; 3 no_budget; 4 refused (NOFALLBACK, a model outside the allowlist,
# or the sibling's sandbox root).
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

usage() {
  echo "usage: run-panel.sh --arm {Z0-raw|Z0|K|RL} --panel {primary|haiku|sonnet} --doc <id> --replicate <n> --block <n> --seed <int> --run-id <id> [--b <s>] [--b-min <s>] [--c-luna <s>] [--dry-run]" >&2
  exit 2
}
ARM= PANEL= DOC= REP= BLOCK= SEED= RUN_ID= B= BMIN= CLUNA= DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --arm | --panel | --doc | --replicate | --block | --seed | --run-id | --b | --b-min | --c-luna)
      [ $# -ge 2 ] || usage
      case "$1" in
        --arm) ARM=$2 ;; --panel) PANEL=$2 ;; --doc) DOC=$2 ;; --replicate) REP=$2 ;; --block) BLOCK=$2 ;;
        --seed) SEED=$2 ;; --run-id) RUN_ID=$2 ;; --b) B=$2 ;; --b-min) BMIN=$2 ;; --c-luna) CLUNA=$2 ;;
      esac
      shift
      ;;
    *) usage ;;
  esac
  shift
done
NUM='^[0-9]+(\.[0-9]+)?$'
ID='^[A-Za-z0-9][A-Za-z0-9._-]*$'
case $ARM in Z0-raw | Z0 | K | RL) ;; *) usage ;; esac
case $PANEL in primary | haiku | sonnet) ;; *) usage ;; esac
[[ $DOC =~ $ID && $RUN_ID =~ $ID ]] || usage
[[ $REP =~ ^[0-9]+$ && $BLOCK =~ ^[0-9]+$ && $SEED =~ ^-?[0-9]+$ ]] || usage
[ -z "$B" ] || { [[ $B =~ $NUM ]] && awk -v v="$B" 'BEGIN{exit !(v > 0)}'; } || usage
[ -z "$BMIN" ] || { [[ $BMIN =~ $NUM ]] && awk -v v="$BMIN" 'BEGIN{exit !(v > 0)}'; } || usage
[ -z "$CLUNA" ] || { [[ $CLUNA =~ $NUM ]] && awk -v v="$CLUNA" 'BEGIN{exit !(v > 0)}'; } || usage

sw_assert_nofallback || exit 4
VERIFIER=${VERIFIER:-0}
[ "$VERIFIER" = 0 ] || { echo "E_VERIFIER: the optional verifier is not built; VERIFIER must be 0" >&2; exit 2; }

LENSES=${RL_LENSES:-$SW/config/lenses.json}
[ -f "$LENSES" ] || { echo "E_USAGE: no lens table $LENSES" >&2; exit 2; }
sw_assert_writable "$LENSES" || exit 2
ROLES=$(jq -r --arg p "$PANEL" '.panels[$p].roles | to_entries[] | "\(.value.rid) \(.value.model)"' "$LENSES" 2>/dev/null)
[ -n "$ROLES" ] || { echo "E_USAGE: no roles for panel $PANEL in $LENSES" >&2; exit 2; }
while read -r _rid model; do
  sw_assert_model "$model" || exit 4
done <<<"$ROLES"

# 1. the sandbox (K4): present and clean before the run
SUBDIR=repo
[ "$ARM" != Z0-raw ] || SUBDIR=repo-raw
export RL_SANDBOX_SUB=$SUBDIR
REPO_SB=$SB/$DOC/$SUBDIR
CAND=$SB/cand/$DOC/candidate.md
SOURCE=$SB/cand/$DOC/source.md
[ -f "$SOURCE" ] || SOURCE=
{ [ -d "$REPO_SB/.git" ] && [ -f "$CAND" ]; } || { echo "E_SANDBOX: no sandbox for $DOC under $SB (run bin/build-sandbox.sh first, with --raw for Z0-raw)" >&2; exit 2; }
sandbox_state() { git -C "$REPO_SB" status --porcelain --ignored; }
[ -z "$(sandbox_state)" ] || { echo "E_SANDBOX_DIRTY: $REPO_SB; rebuild it" >&2; exit 2; }

RUN=${RL_RUNS_ROOT:-$SW/runs}/$RUN_ID
[ ! -e "$RUN" ] || { echo "E_RUN_EXISTS: $RUN; remove it or use another --run-id" >&2; exit 2; }
sw_assert_writable "$RUN" || exit 2

PLAN=$(sw_py "$HERE/../rl/cli.py" plan --arm "$ARM" --panel "$PANEL" --doc "$DOC" ${B:+--b "$B"}) || exit 2
B=$(jq -r .b <<<"$PLAN")
HANG=$(jq -r .hang_s <<<"$PLAN")
mkdir -p "$RUN/stamps" || exit 2
# other panels of either build that are running now (the gateway limit of DESIGN 9.5); pgrep runs in this shell, so the
# only match of this script is $$
pgrep -f '^(/[a-z/]*/)?bash [^ ]*bin/run-panel\.sh' >"$RUN/stamps/panels.pids"
CONC=$(grep -vxc "$$" "$RUN/stamps/panels.pids")
log() { echo "$(sw_now) $*" >>"$RUN/run.log"; }
FREEZE_TAG=$(jq -r '.freeze_tag // .tag // empty' "$SW/config/freeze.json" 2>/dev/null)
jq -n --arg arm "$ARM" --arg panel "$PANEL" --arg doc "$DOC" --arg run_id "$RUN_ID" --argjson rep "$REP" \
  --argjson block "$BLOCK" --argjson seed "$SEED" --argjson b "$B" --argjson hang "$HANG" --argjson conc "${CONC:-0}" \
  --arg rlv "$(jq -r .version "$LENSES")" --arg regv "$(jq -r .version "$SW/recipes/recipes.json")" \
  --arg freeze "$FREEZE_TAG" --arg csha "$(sha256sum "$CAND" | cut -d' ' -f1)" \
  --arg ssha "$([ -z "$SOURCE" ] || sha256sum "$SOURCE" | cut -d' ' -f1)" --arg sandbox "$REPO_SB" --argjson dry "$DRY" '{
    arm: $arm, panel: $panel, doc: $doc, run_id: $run_id, replicate: $rep, block: $block, seed: $seed, b: $b,
    hang_s: $hang, rl_version: $rlv, registry_version: $regv, freeze_tag: (if $freeze == "" then null else $freeze end),
    candidate_sha256: $csha, source_sha256: (if $ssha == "" then null else $ssha end), sandbox: $sandbox,
    concurrent_panels_at_start: $conc, dry_run: ($dry == 1)}' >"$RUN/run.json" || exit 2

# 2. the panel clock starts before the render
T0=$(sw_now)
log "t0 arm=$ARM panel=$PANEL doc=$DOC b=$B hang_s=$HANG"
FALLBACK=0
CLI=("$HERE/../rl/cli.py")
if [ "$ARM" = RL ]; then
  LENS=(sw_py "${CLI[0]}" lens --panel "$PANEL" --doc "$DOC" --candidate-sb "$CAND" --out "$RUN" --lenses "$LENSES")
  [ -z "$SOURCE" ] || LENS+=(--source "$SOURCE")
  [ -z "$BMIN" ] || LENS+=(--b "$BMIN")
  [ -z "$CLUNA" ] || LENS+=(--c-luna "$CLUNA")
  LRC=0
  "${LENS[@]}" 2>"$RUN/lens.err" || LRC=$?
  cat "$RUN/lens.err" >&2
  case $LRC in
    0) ;;
    3)
      log "no_budget"
      echo "no_budget: the row cap is below the number of recipes of a lens; RL is refused on this panel" >&2
      exit 3
      ;;
    1) # the fallback is decided here, before any reviewer starts (DESIGN 8 rows 1 and 2, INV-012)
      REASON=$(jq -r '.reason // "error"' "$RUN/lens/error.json" 2>/dev/null || echo error)
      (unset RL_FORCE_EXC; "${LENS[@]}" --fallback "$REASON") || { echo "E_FALLBACK: the Z0 briefs could not be written" >&2; exit 2; }
      FALLBACK=1
      jq --argjson t "$(sw_now)" '.fallback_at = $t' "$RUN/run.json" >"$RUN/run.json.tmp" && mv "$RUN/run.json.tmp" "$RUN/run.json"
      log "fallback reason=$REASON"
      ;;
    *) echo "E_LENS: the lens step failed with $LRC" >&2; exit 2 ;;
  esac
else
  BR=(sw_py "${CLI[0]}" briefs --arm "$ARM" --panel "$PANEL" --doc "$DOC" --candidate-sb "$CAND" --out "$RUN" --lenses "$LENSES")
  [ -z "$SOURCE" ] || BR+=(--source "$SOURCE")
  "${BR[@]}" || { echo "E_BRIEFS: the briefs could not be rendered" >&2; exit 2; }
fi
RENDER_S=$(awk -v n="$(sw_now)" -v t="$T0" 'BEGIN { printf "%.3f", n - t }')

# 3. --dry-run stops here
if [ "$DRY" = 1 ]; then
  while read -r rid model; do
    printf '%s\n' "(cd $REPO_SB && claude -p --model $model --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <$RUN/briefs/$rid.txt)  # $rid brief sha256 $(cat "$RUN/briefs/$rid.sha256") hang_s $HANG"
  done <<<"$ROLES"
  exit 0
fi

# 4. three reviewers in parallel under the hang guard; the ember is re-asked as soon as its report is read (DESIGN 7.6)
DO_REASK=0
{ [ "$ARM" = RL ] && [ "$FALLBACK" = 0 ]; } && DO_REASK=1
run_one() {
  local rid=$1 model=$2 t used rc ask
  t=$(sw_now)
  echo "$t" >"$RUN/stamps/$rid.start"
  used=$(awk -v n="$t" -v t0="$T0" 'BEGIN { printf "%.3f", n - t0 }')
  bash "$HERE/run-reviewer.sh" "$RUN" "$DOC" "$rid" "$model" "$RUN/briefs/$rid.txt" "$HANG" "$used" 2>"$RUN/stamps/$rid.err"
  rc=$?
  sw_now >"$RUN/stamps/$rid.end"
  echo "$rc" >"$RUN/stamps/$rid.rc"
  [ "$DO_REASK" = 1 ] && [ "$rc" = 0 ] || return 0
  ask=$(jq -r '.reask // false' "$RUN/lens/$rid.json" 2>/dev/null)
  [ "$ask" = true ] && [ "$(jq -r .status "$RUN/reviews/$rid.meta.json" 2>/dev/null)" = ok ] || return 0
  # reask decides (role, ledger_missing, once, clock) and records reviews/<rid>.reask.json; it never fails the run
  sw_py "${CLI[0]}" reask --run "$RUN" --rid "$rid" --cwd "$REPO_SB" --b "$B" \
    --now-s "$(awk -v n="$(sw_now)" -v t0="$T0" 'BEGIN { printf "%.3f", n - t0 }')" >"$RUN/stamps/$rid.reask.out" 2>>"$RUN/run.log"
}
while read -r rid model; do
  run_one "$rid" "$model" &
done <<<"$ROLES"
wait
if grep -qx 4 "$RUN"/stamps/*.rc 2>/dev/null; then
  echo "E_REFUSED: a reviewer was refused" >&2
  exit 4
fi

# 5. R3 (arm RL with a lens): the check; a repaired report is checked with --via-reask; any failure skips the whole check
CHECK_SKIPPED=0 CHECK_RAN=0 CHECK_S=0
if [ "$DO_REASK" = 1 ]; then
  VIA=()
  for f in "$RUN"/reviews/*.reask.json; do
    [ -f "$f" ] || continue
    [ "$(jq -r .accepted "$f")" != true ] || VIA+=(--via-reask "$(jq -r .rid "$f")")
  done
  CHK=(sw_py "${CLI[0]}" check --run "$RUN" --candidate "$CAND")
  [ -z "$SOURCE" ] || CHK+=(--source "$SOURCE")
  CS=$(sw_now)
  if "${CHK[@]}" ${VIA[@]+"${VIA[@]}"} 2>"$RUN/check.err"; then
    CHECK_RAN=1
  else
    CHECK_SKIPPED=1
    mkdir -p "$RUN/check"
    cp "$RUN/check.err" "$RUN/check/error.log"
    log "check_skipped"
  fi
  CHECK_S=$(awk -v n="$(sw_now)" -v t="$CS" 'BEGIN { printf "%.3f", n - t }')
fi
R3_END=$(sw_now)
# 6. the clock stops here. Outside it: H2, the merge (a killed or invalid reviewer is absent), the sandbox check, the records
PM=(sw_py "${CLI[0]}" prepare-merge --run "$RUN")
[ "$CHECK_RAN" = 0 ] || PM+=(--checked)
PMOUT=$("${PM[@]}") || { echo "E_H2: the merge input could not be prepared" >&2; exit 2; }
MARGS=()
for rid in $(jq -r '.used[]' <<<"$PMOUT"); do
  MARGS+=(--report "$rid=$RUN/normalised/$rid.md")
done
MERGE_EXIT=0
if [ ${#MARGS[@]} -eq 0 ]; then
  MERGE_EXIT=1
  echo "no reviewer report to merge" >"$RUN/merged/merge.err"
else
  uv run --frozen --project "$REPO" superclaude review merge --ledger "$RUN/merged/ledger.json" --doc "$CAND" --round 1 \
    "${MARGS[@]}" --resolution "$RUN/resolution.json" --out "$RUN/merged/merged-1.md" \
    >"$RUN/merged/merge.out.json" 2>"$RUN/merged/merge.err" || MERGE_EXIT=$?
  [ "$MERGE_EXIT" = 0 ] || log "merge_refused exit=$MERGE_EXIT"
fi
DIRTY=0
[ -z "$(sandbox_state)" ] || DIRTY=1
REC=(--run "$RUN" --arm "$ARM" --t0 "$T0" --render-s "$RENDER_S" --check-s "$CHECK_S" --r3-end "$R3_END" --merge-exit "$MERGE_EXIT")
[ "$CHECK_SKIPPED" = 0 ] || REC+=(--check-skipped)
[ "$CHECK_RAN" = 0 ] || REC+=(--check-ran)
[ "$DIRTY" = 0 ] || REC+=(--sandbox-dirty)
sw_py "${CLI[0]}" record "${REC[@]}" || { echo "E_RECORD: run.json and timing.json could not be written" >&2; exit 2; }
echo "run $RUN_ID: arm=$ARM panel=$PANEL fallback=$FALLBACK check_skipped=$CHECK_SKIPPED merged=$(jq -r '.used | length' <<<"$PMOUT") merge_exit=$MERGE_EXIT elapsed_s=$(jq -r .panel_elapsed_s "$RUN/timing.json")"
if [ "$DIRTY" = 1 ]; then
  echo "E_SANDBOX_DIRTY: a reviewer left files in $REPO_SB; the run is flagged sandbox_dirty and the sandbox must be rebuilt" >&2
  exit 2
fi
exit 0
