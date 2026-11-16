#!/usr/bin/env bash
# run-panel.sh --arm {Z0-raw|Z0|K|SS} --panel {primary|haiku|sonnet} --doc DOC --run RUN [options]   (DESIGN 2.1, 2.2, 10, 11)
# One panel run on one document: S0 sandbox check, S1 pre-pass (SS only) under `timeout`, brief render, three reviewers in
# parallel under the hang guard, S5 check (SS only), H2, the real `superclaude review merge`. It writes under RUN:
#   run.json timing.json resolution.json briefs/ prepass/ reviews/ check/ normalised/ merged/ clock-events.tsv launcher.log
# Options:
#   --seed N --replicate N --block N --concurrent N   recorded in run.json (seed 1 when not given; the rest are null)
#   --values FILE     a values file instead of config/values.json (test hook; accepted only under /tmp/)
#   --packages FILE   passed to build-sandbox.sh (test hook; accepted only under /tmp/)
#   --unavailable RID   a reviewer that cannot be launched (a model probe failed, DESIGN 10 row 9); repeatable
# Environment: NOFALLBACK=1 is required (DD-8). VERIFIER defaults to 0; the optional verifier is not built, so any other
# value is refused. Overrides of the tests, judged by bin/common.sh: SW_PREPASS_CMD (a `sleep N` or `false` stub that
# replaces the pre-pass), SW_RENDER_CMD (`false`: the SS brief render fails), SW_KILL_S (the kill limit, 0.1 to 15 s).
# CHECK_SCOPE is read by `sweep check` (DD-3); a bad value makes S5 raise, which is how the tests force row 11.
# Exit: 0 the run is finished and recorded; 2 refused before any reviewer started (sandbox missing or dirty, bad
# argument, run folder in use); 3 finished, but the sandbox was dirty afterwards (`sandbox_dirty`: K4, rebuild it);
# 4 the SS start was refused because the time budget is under 8 s (`no_budget`, DESIGN 12.3).
# Order inside a run (DD-9): S5 on the raw reports, then H2, then the merge. The fallback decision (pre-pass error, kill,
# render error) is taken before any reviewer starts, so a running reviewer's brief never changes (INV-012).
# Git: only `git -C <sandbox> status --porcelain`, read-only, on the sandbox. The real repository is never touched.
# Gaps in the design resolved here (each is a choice the design leaves open):
#   P1  S0 refuses a missing sandbox (row 7: it must be rebuilt), then runs build-sandbox.sh, which also checks it.
#   P2  Z0-raw uses SB/<doc>/repo-raw, skips S1, S5 and H2 (DESIGN 2.1), and its merge reads reviews/<rid>.md as written.
#   P3  `reason` in run.json: kill (S1 hit the kill limit), error (S1 failed or left no prepass.json), render (the SS
#       brief render failed); null without a fallback. A fallback removes prepass/ and prepass.tmp/ so no step reads a
#       pre-pass that was not used; prepass.error.json stays.
#   P4  `no_trigger` is the pre-pass's own no_trigger (no item at all). A fallback or a no-trigger run skips the check:
#       the reviewers had no ledger rule, so a missing ledger is not counted (`check_ran` false). The S5 stage still
#       gets its start and end (about 0 s), so panel_elapsed_s of arm SS stays defined.
#   P5  Only reviewers with status ok (run-reviewer.sh) go to S5, H2 and the merge; the rest are absent from the merge and
#       scored zero findings (row 8). `lost_replica` lists the items assigned to them. A merge that is refused, or that
#       has no report to read, is recorded `merge_refused` and is not repeated (DESIGN 11.7).
#   P6  `--unavailable` is the pre-launch decision. The model probe itself is the caller's: it starts no model here. With
#       fewer than three reviewers the pre-pass re-runs assign with the available set (replicas 1, DESIGN 7.3).
#   P7  run.json holds the values used (`values`), `registry_version` (sha256 of cards/C*.json, first 16 hex characters) and
#       `freeze_tag` (config/freeze.json, null before the freeze). A run folder that holds run.json is never reused.
#   P8  timing.json is made by `sweep clock timing` from the event times in clock-events.tsv; it adds `stage_t` (the raw
#       start and end of each stage) to the fields of DESIGN 11.4.
set -u -o pipefail
source "$(dirname "$0")/common.sh"

VERIFIER=${VERIFIER:-0}
usage() {
  sed -n '2,3p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
ARM= PANEL= DOC= RUN= SEED=1 REPLICATE=null BLOCK=null CONCURRENT=null VALUES= PKFILE=
UNAVAIL=()
while [ $# -gt 0 ]; do
  case "$1" in
    --arm | --panel | --doc | --run | --seed | --replicate | --block | --concurrent | --values | --packages | --unavailable)
      [ $# -ge 2 ] || usage
      case "$1" in
        --arm) ARM=$2 ;;
        --panel) PANEL=$2 ;;
        --doc) DOC=$2 ;;
        --run) RUN=$2 ;;
        --seed) SEED=$2 ;;
        --replicate) REPLICATE=$2 ;;
        --block) BLOCK=$2 ;;
        --concurrent) CONCURRENT=$2 ;;
        --values) VALUES=$2 ;;
        --packages) PKFILE=$2 ;;
        --unavailable) UNAVAIL+=("$2") ;;
      esac
      shift
      ;;
    *) usage ;;
  esac
  shift
done
case "$ARM" in Z0-raw | Z0 | K | SS) ;; *) echo "E_ARM: --arm must be Z0-raw, Z0, K or SS" >&2; exit 2 ;; esac
[[ $DOC =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "E_DOC: bad document id: $DOC" >&2; exit 2; }
[ -n "$RUN" ] || usage
for v in SEED; do [[ ${!v} =~ ^[0-9]+$ ]] || { echo "E_ARG: --seed is not a number" >&2; exit 2; }; done
for v in REPLICATE BLOCK CONCURRENT; do
  { [ "${!v}" = null ] || [[ ${!v} =~ ^[0-9]+$ ]]; } || { echo "E_ARG: $v is not a number" >&2; exit 2; }
done
for f in "$VALUES" "$PKFILE"; do
  [ -z "$f" ] && continue
  case "$(realpath -m -- "$f")/" in /tmp/?*) ;; *) echo "E_OVERRIDE: $f is outside /tmp/" >&2; exit 2 ;; esac
done
sw_assert_nofallback || exit 2
[ "$VERIFIER" = 0 ] || { echo "E_VERIFIER: VERIFIER=$VERIFIER, but the optional verifier is not built (REQ-46); leave it 0" >&2; exit 2; }
sw_assert_writable "$RUN" || exit 2
[ ! -e "$RUN/run.json" ] || { echo "E_RUN_EXISTS: $RUN/run.json exists; a counted run is never repeated" >&2; exit 2; }

# Reviewers of the panel (S, L1, L2), minus the unavailable ones; every model must be on the allowlist (K2).
PANELS_FILE=${SW_PANELS:-$SW/config/panels.json} # SW_PANELS: the panel file of a schedule run with the spike fallback caps (Task 32)
jq -e --arg p "$PANEL" '.panels[$p]' "$PANELS_FILE" >/dev/null 2>&1 || { echo "E_PANEL: unknown panel $PANEL" >&2; exit 2; }
RIDS=()
declare -A MODEL_OF
for role in S L1 L2; do
  rid=$(jq -r --arg p "$PANEL" --arg r "$role" '.panels[$p][$r].rid' "$PANELS_FILE")
  model=$(jq -r --arg p "$PANEL" --arg r "$role" '.panels[$p][$r].model' "$PANELS_FILE")
  sw_assert_model "$model" || exit 2
  MODEL_OF[$rid]=$model
  skip=0
  for u in ${UNAVAIL[@]+"${UNAVAIL[@]}"}; do [ "$u" = "$rid" ] && skip=1; done
  [ "$skip" = 1 ] || RIDS+=("$rid")
done
for u in ${UNAVAIL[@]+"${UNAVAIL[@]}"}; do
  [ -n "${MODEL_OF[$u]:-}" ] || { echo "E_ARG: --unavailable $u is not a reviewer of panel $PANEL" >&2; exit 2; }
done
[ ${#RIDS[@]} -ge 1 ] || { echo "E_ARG: no reviewer is available" >&2; exit 2; }

# S0: the sandbox must exist (built once and reused), be valid and be clean (row 7); the run is refused otherwise.
if [ "$ARM" = Z0-raw ]; then SUB=repo-raw; else SUB=repo; fi
SBD=$SB/$DOC
SANDBOX=$SBD/$SUB
CAND=$SB/cand/$DOC/candidate.md
SRC=$SB/cand/$DOC/source.md
[ -d "$SANDBOX" ] || { echo "E_SANDBOX_MISSING: $SANDBOX; build it with bin/build-sandbox.sh" >&2; exit 2; }
BS_ARGS=()
[ "$ARM" = Z0-raw ] && BS_ARGS+=(--raw)
[ -n "$PKFILE" ] && BS_ARGS+=(--packages "$PKFILE")
bash "$SW/bin/build-sandbox.sh" ${BS_ARGS[@]+"${BS_ARGS[@]}"} "$DOC" >/dev/null || { echo "E_SANDBOX_DIRTY: build-sandbox.sh refused $SANDBOX" >&2; exit 2; }
[ -z "$(git -C "$SANDBOX" status --porcelain 2>&1)" ] || { echo "E_SANDBOX_DIRTY: $SANDBOX is not clean before the run" >&2; exit 2; }
[ -f "$CAND" ] || { echo "E_CANDIDATE: $CAND missing" >&2; exit 2; }
HAS_SRC=true
[ -f "$SRC" ] || HAS_SRC=false
SRC_ARGS=()
$HAS_SRC && SRC_ARGS=(--source "$SRC")

mkdir -p "$RUN"
TMPW=$(mktemp -d /tmp/run-panel.XXXXXXXX) || exit 2
trap 'rm -rf -- "$TMPW"' EXIT
CLI=("$SW/sweep/cli.py")

# The numbers of the run: b, the kill limit and the hang guard (scaffold/clock.py through `sweep clock plan`).
PLAN_ARGS=(--arm "$ARM" --panel "$PANEL" --doc "$DOC")
[ -n "$VALUES" ] && PLAN_ARGS+=(--values "$VALUES")
PLAN=$(sw_py "${CLI[@]}" clock plan "${PLAN_ARGS[@]}") || { echo "E_NO_B: no b for panel $PANEL and document $DOC in the values file" >&2; exit 2; }
B=$(jq -r .b <<<"$PLAN")
HANG_S=$(jq -r .hang_s <<<"$PLAN")
KILL=${SW_KILL_S:-$(jq -r .kill_s <<<"$PLAN")}

FT=$(jq -r '.freeze_tag // empty' "$SW/config/freeze.json" 2>/dev/null || true)
REGV=$(cat "$SW"/cards/C*.json | sha256sum | cut -c1-16)
RUNJ=$RUN/run.json
jq -n --arg arm "$ARM" --arg panel "$PANEL" --arg doc "$DOC" --argjson seed "$SEED" --argjson replicate "$REPLICATE" \
  --argjson block "$BLOCK" --argjson conc "$CONCURRENT" --arg ft "$FT" --arg regv "$REGV" \
  --arg csha "$(sha256sum "$CAND" | cut -d' ' -f1)" --arg ssha "$($HAS_SRC && sha256sum "$SRC" | cut -d' ' -f1)" \
  --argjson hs "$($HAS_SRC && echo true || echo false)" --argjson plan "$PLAN" --argjson n "${#RIDS[@]}" \
  --argjson unav "$(printf '%s\n' ${UNAVAIL[@]+"${UNAVAIL[@]}"} | jq -R . | jq -sc 'map(select(length>0))')" \
  '{arm:$arm,panel:$panel,doc:$doc,replicate:$replicate,seed:$seed,block:$block,
    sweep_version:$plan.sweep_version,registry_version:$regv,freeze_tag:(if $ft=="" then null else $ft end),
    candidate_sha256:$csha,source_sha256:(if $hs then $ssha else null end),briefs:{},
    fallback:false,reason:null,no_trigger:false,no_source:($hs|not),check_skipped:false,check_ran:false,
    sandbox_dirty:false,merge_refused:false,time_cap_exception:false,concurrent_panels_at_start:$conc,
    reviewers:$n,reviewers_unavailable:$unav,b:$plan.b,expected_overhead_s:$plan.expected_overhead_s,
    kill_s:$plan.kill_s,hang_s:$plan.hang_s,no_budget:false,values:$plan.values}' >"$RUNJ"
runset() { # runset KEY JSON-VALUE: update one key of run.json
  jq --arg k "$1" --argjson v "$2" '.[$k] = $v' "$RUNJ" >"$RUNJ.tmp" && mv -- "$RUNJ.tmp" "$RUNJ"
}
if [ "$ARM" = SS ] && [ "$(jq -r .no_budget <<<"$PLAN")" = true ]; then
  runset no_budget true
  echo "no_budget: b=$B leaves under 8 s for the items; the SS run is refused (DESIGN 12.3)" >&2
  exit 4
fi

# The panel clock (DESIGN 11.4): t0 comes before S1 (SS) or before the first brief is rendered (other arms).
EV=$RUN/clock-events.tsv
: >"$EV"
ev() { printf '%s\t%s\n' "$1" "${2:-$(sw_now)}" >>"$EV"; }
T0=$(sw_now)
ev t0 "$T0"

FALLBACK=false
REASON=null
NO_TRIGGER=false
RUN_FALLBACK() { # RUN_FALLBACK reason: the decision is taken here, before any reviewer starts
  FALLBACK=true
  REASON=\"$1\"
  rm -rf -- "$RUN/prepass" "$RUN/prepass.tmp"
  runset fallback true
  runset reason "$REASON"
}

# S1: the pre-pass, serial, under timeout at the kill limit; a failed or killed pre-pass means the Z0 briefs.
if [ "$ARM" = SS ]; then
  ev prepass_start
  if [ -n "${SW_PREPASS_CMD:-}" ]; then
    read -r -a STUB <<<"$SW_PREPASS_CMD"
    timeout -k 2 "$KILL" "${STUB[@]}" >"$RUN/prepass.out" 2>"$RUN/prepass.err"
  else
    PP=(--candidate "$CAND" ${SRC_ARGS[@]+"${SRC_ARGS[@]}"} --repo "$SANDBOX" --seed "$SEED" --panel "$PANEL" --out "$RUN")
    [ ${#UNAVAIL[@]} -eq 0 ] || PP+=(--available "$(IFS=,; echo "${RIDS[*]}")")
    timeout -k 2 "$KILL" uv run --frozen --project "$REPO" python "${CLI[@]}" prepass "${PP[@]}" >"$RUN/prepass.out" 2>"$RUN/prepass.err"
  fi
  PRC=$?
  ev prepass_end
  if [ "$PRC" -eq 124 ] || [ "$PRC" -eq 137 ]; then
    RUN_FALLBACK kill
  elif [ "$PRC" -ne 0 ] || [ ! -f "$RUN/prepass/prepass.json" ]; then
    RUN_FALLBACK error
  else
    NO_TRIGGER=$(jq -r .no_trigger "$RUN/prepass/prepass.json")
  fi
  [ "$NO_TRIGGER" = true ] && runset no_trigger true
  ev render_start
fi

# Brief render: one `sweep brief` per reviewer, in parallel; each writes briefs/<rid>.txt and briefs/<rid>.sha256.
mkdir -p "$RUN/briefs" "$RUN/reviews"
render_all() { # render_all normal|fallback; returns non-zero when any reviewer's brief failed
  local mode=$1 rid pids=() bad=0 i=0
  for rid in "${RIDS[@]}"; do
    (
      if [ "$mode" = normal ] && [ "$ARM" = SS ] && [ -n "${SW_RENDER_CMD:-}" ]; then
        "$SW_RENDER_CMD"
      else
        A=(--arm "$ARM" --candidate-sb "$CAND" ${SRC_ARGS[@]+"${SRC_ARGS[@]}"} --out "$RUN/briefs/$rid.txt")
        if [ "$ARM" = SS ]; then
          [ "$mode" = fallback ] && A+=(--fallback)
          # a no-trigger pre-pass may leave no sheet file for a reviewer: that is an empty sheet, not a render error
          if [ "$mode" = normal ] && { [ -f "$RUN/prepass/sheets/$rid.md" ] || [ "$NO_TRIGGER" != true ]; }; then
            A+=(--sheet "$RUN/prepass/sheets/$rid.md")
          fi
        fi
        sw_py "${CLI[@]}" brief "${A[@]}" >"$TMPW/brief.$rid.json" 2>>"$TMPW/brief.err"
      fi
    ) &
    pids+=($!)
  done
  for rid in "${RIDS[@]}"; do
    wait "${pids[$i]}" || bad=1
    i=$((i + 1))
  done
  return $bad
}
if [ "$ARM" = SS ] && ! $FALLBACK; then
  render_all normal || RUN_FALLBACK render
fi
if $FALLBACK || [ "$ARM" != SS ]; then
  [ "$ARM" = SS ] && MODE=fallback || MODE=plain
  render_all "$MODE" || { cat "$TMPW/brief.err" >&2; echo "E_RENDER: the briefs could not be rendered, no fallback is left" >&2; exit 2; }
fi
[ "$ARM" = SS ] && ev render_end
BR=$(for rid in "${RIDS[@]}"; do jq -nc --arg r "$rid" --arg s "$(tr -d '\n' <"$RUN/briefs/$rid.sha256")" '{($r):$s}'; done | jq -sc 'add')
runset briefs "$BR"

# S4: three reviewers in parallel, one attempt each, each under the hang guard measured from t0.
RRARGS=()
[ "$ARM" = Z0-raw ] && RRARGS+=(--raw)
rev_run() { # rev_run rid
  local rid=$1 now left
  now=$(sw_now)
  left=$(awk -v h="$HANG_S" -v t0="$T0" -v n="$now" 'BEGIN{r = h - (n - t0); if (r < 1) r = 1; printf "%.3f", r}')
  ev "rev_start:$rid" "$now"
  bash "$SW/bin/run-reviewer.sh" ${RRARGS[@]+"${RRARGS[@]}"} "$RUN" "$DOC" "$rid" "${MODEL_OF[$rid]}" "$left" \
    <"$RUN/briefs/$rid.txt" >"$TMPW/rev.$rid.log" 2>&1
  ev "rev_end:$rid"
}
for rid in "${RIDS[@]}"; do rev_run "$rid" & done
wait
for rid in "${RIDS[@]}"; do sed "s/^/[$rid] /" "$TMPW/rev.$rid.log" >>"$RUN/launcher.log"; done

# K4: the sandbox must still be clean; a reviewer that wrote into it flags the run.
DIRTY=$(git -C "$SANDBOX" status --porcelain 2>&1)
if [ -n "$DIRTY" ]; then
  runset sandbox_dirty true
  printf '%s\n' "$DIRTY" >"$RUN/sandbox-dirty.txt"
fi

# Who finished (row 8): status ok goes on; killed, invalid and error are absent from the merge and score zero.
OK=()
STAT=$(
  for rid in "${RIDS[@]}"; do
    s=error
    [ -f "$RUN/reviews/$rid.meta.json" ] && s=$(jq -r .status "$RUN/reviews/$rid.meta.json")
    jq -nc --arg r "$rid" --arg m "${MODEL_OF[$rid]}" --arg s "$s" '{($r):{model:$m,status:$s}}'
  done | jq -sc 'add'
)
runset reviewer_status "$STAT"
for rid in "${RIDS[@]}"; do
  [ "$(jq -r --arg r "$rid" '.[$r].status' <<<"$STAT")" = ok ] && OK+=("$rid")
done
if [ "$ARM" = SS ] && ! $FALLBACK && [ -f "$RUN/prepass/assignment.json" ]; then
  FAILED=$(for rid in "${RIDS[@]}"; do jq -r --arg r "$rid" 'select(.[$r].status != "ok") | $r' <<<"$STAT"; done | jq -R . | jq -sc 'map(select(length>0))')
  runset lost_replica "$(jq -c --argjson f "$FAILED" '[$f[] as $r | .reviewers[$r][]?] | unique' "$RUN/prepass/assignment.json")"
fi

# S5: the check on the raw reports, caught as a whole (row 11); skipped when the reviewers had no ledger rule (P4).
if [ "$ARM" = SS ]; then
  ev s5_start
  if ! $FALLBACK && [ "$NO_TRIGGER" != true ]; then
    if sw_py "${CLI[@]}" check --run "$RUN" --candidate "$CAND" ${SRC_ARGS[@]+"${SRC_ARGS[@]}"} >/dev/null 2>"$TMPW/check.err"; then
      runset check_ran true
    else
      runset check_skipped true
      mkdir -p "$RUN/check"
      cp -- "$TMPW/check.err" "$RUN/check/error.log"
    fi
  fi
  ev s5_end
fi
CHECK_RAN=$(jq -r .check_ran "$RUNJ")

# H2 (every arm but Z0-raw), then the merge. Inputs: checked reports when S5 ran, else the raw reports.
MERGE_ARGS=()
RES=
H2_FAILED=()
for rid in ${OK[@]+"${OK[@]}"}; do
  IN=$RUN/reviews/$rid.md
  [ "$CHECK_RAN" = true ] && [ -f "$RUN/check/$rid.checked.md" ] && IN=$RUN/check/$rid.checked.md
  if [ "$ARM" != Z0-raw ]; then
    if sw_py "${CLI[@]}" normalise --report "$IN" --out-dir "$RUN/normalised" --rid "$rid" >/dev/null 2>>"$RUN/launcher.log"; then
      IN=$RUN/normalised/$rid.md
    else
      H2_FAILED+=("$rid")
      continue
    fi
  fi
  MERGE_ARGS+=(--report "$rid=$IN")
  RES+=$(printf '%s\t%s' "$rid" "${MODEL_OF[$rid]}")$'\n'
done
runset h2_failed "$(printf '%s\n' ${H2_FAILED[@]+"${H2_FAILED[@]}"} | jq -R . | jq -sc 'map(select(length>0))')"
jq -n --arg t "$RES" '{reviewers: ($t | split("\n") | map(select(length > 0) | split("\t") | {reviewer_id: .[0], model: .[1]}))}' >"$RUN/resolution.json"
mkdir -p "$RUN/merged"
if [ ${#MERGE_ARGS[@]} -eq 0 ]; then
  runset merge_refused true
  echo "merge: no reviewer report is left to merge" >>"$RUN/launcher.log"
elif ! uv run --frozen --project "$REPO" superclaude review merge --ledger "$RUN/merged/ledger.json" --doc "$CAND" --round 1 \
  "${MERGE_ARGS[@]}" --resolution "$RUN/resolution.json" --out "$RUN/merged/merged-1.md" \
  >"$RUN/merged/merge.out.json" 2>"$RUN/merged/merge.err"; then
  runset merge_refused true
fi

sw_py "${CLI[@]}" clock timing --arm "$ARM" --events "$EV" --out "$RUN/timing.json" || { echo "E_TIMING: timing.json was not written" >&2; exit 1; }
[ "$(jq -r .sandbox_dirty "$RUNJ")" = true ] && { echo "sandbox_dirty: a reviewer changed $SANDBOX" >&2; exit 3; }
exit 0
