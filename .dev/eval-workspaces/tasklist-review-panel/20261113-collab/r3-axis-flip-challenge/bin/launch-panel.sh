#!/usr/bin/env bash
# PANEL_COLLAB=0|1 launch-panel.sh <el2|sl2|hl2> [--pkgs <id>...] [--tag <text>] [--no-judge]   (section 13)
# exit 0 every package valid and judged; 1 preflight refused; 2 a package invalid or not judged; 3 audit violation.
set -u -o pipefail
source "$(dirname "$0")/../lib/common.sh"
PANEL=${1:-}; shift || true
PKGS=(); TAG=""; NOJUDGE=0
while [ $# -gt 0 ]; do
  case $1 in
    --pkgs) shift; while [ $# -gt 0 ] && [ "${1#--}" = "$1" ]; do PKGS+=("$1"); shift; done;;
    --tag) TAG=$2; shift 2;;
    --no-judge) NOJUDGE=1; shift;;
    *) echo "unknown argument $1" >&2; exit 1;;
  esac
done
refuse() { echo "PREFLIGHT: $*" >&2; exit 1; }
# --- preflight (13.2 step 1)
for t in jq timeout flock realpath claude uv pgrep; do command -v $t >/dev/null || refuse "$t not on PATH"; done
[ "${NOFALLBACK:-1}" = 1 ] || refuse "E_NOFALLBACK: caller set NOFALLBACK=${NOFALLBACK}"
export NOFALLBACK=1
COLLAB=${PANEL_COLLAB:-1}
case $COLLAB in 0|1) ;; *) refuse "E_BAD_SWITCH: PANEL_COLLAB=$COLLAB";; esac
SMOKE=${R3_SMOKE:-0}; SPIKE4=${R3_SPIKE4:-0}
[ "$SPIKE4" = 1 ] && [ "$COLLAB" = 1 ] && refuse "R3_SPIKE4=1 needs PANEL_COLLAB=0"
[ "$SPIKE4" = 1 ] && NOJUDGE=1
jq -e --arg p "$PANEL" 'has($p)' "$R3/config/panels.json" >/dev/null || refuse "unknown panel '$PANEL'"
for m in $(jq -r --arg p "$PANEL" '.[$p] | ([.searcher] + .readers)[] | .model' "$R3/config/panels.json"); do
  r3_assert_model "$m" || refuse "model $m"
done
for v in R3_RUNS_ROOT R3_SB_ROOT R3_SCORING_ROOT R3_RESULTS_ROOT R3_VALUES_FILE R3_CLAUDE_PROJECTS; do
  [ -n "${!v:-}" ] && case "$(realpath -m -- "${!v}")/" in /tmp/*) ;; *) refuse "E_OVERRIDE $v";; esac
done
r3_py pin --check >/dev/null || refuse "E_PIN_MISMATCH (run: r3lib/cli.py pin --check)"
VF=(); [ "$SMOKE" = 1 ] && VF+=(--smoke); [ "$SPIKE4" = 1 ] && VF+=(--spike4)
VALS=$(r3_py values-show --panel "$PANEL" "${VF[@]}" 2>&1) || refuse "values: $VALS"
uv run --frozen --project "$REPO" superclaude review merge --help >/dev/null 2>&1 || refuse "superclaude review merge --help failed"
[ ${#PKGS[@]} -gt 0 ] || mapfile -t PKGS < <(jq -r '.order[]' "$R3/config/packages.json")
for p in "${PKGS[@]}"; do
  jq -e --arg p "$p" '.packages|has($p)' "$R3/config/packages.json" >/dev/null || refuse "unknown package $p"
  bash "$R3/bin/build-sandbox.sh" "$p" >/dev/null || refuse "E_SANDBOX_DIRTY or sandbox build failed: $p"
done
# --- run record (step 2)
RUN_ID="$PANEL-c$COLLAB-$(date -u +%Y%m%dT%H%M%SZ)-$(openssl rand -hex 2 2>/dev/null || printf '%04x' $RANDOM)"
RD=$RUNS_ROOT/$RUN_ID
r3_assert_writable "$RD" || refuse "run dir not writable"
mkdir -p "$RD"
jq -n --arg id "$RUN_ID" --arg panel "$PANEL" --argjson collab "$COLLAB" --argjson vals "$VALS" --arg pins "$(sha256sum "$R3/config/pins.json" | cut -d' ' -f1)" \
  --arg head "$(git -C "$REPO" rev-parse HEAD)" --arg tag "$TAG" --argjson smoke "$([ "$SMOKE" = 1 ] && echo true || echo false)" \
  --argjson spike4 "$([ "$SPIKE4" = 1 ] && echo true || echo false)" --argjson nj "$([ "$NOJUDGE" = 1 ] && echo true || echo false)" \
  --args '{run_id:$id,panel:$panel,collab:$collab,values_sha256:$vals.sha256,values_status:$vals.values.status,pins_sha256:$pins,
    repo_head:$head,NOFALLBACK:"1",tag:$tag,smoke:$smoke,spike4:$spike4,no_judge:$nj,pkgs:$ARGS.positional,
    env:{SUPERCLAUDE_CODEGRAPH_AUTOINIT:"0",PYTHONDONTWRITEBYTECODE:"1"}}' "${PKGS[@]}" > "$RD/run.json"
# --- packages in parallel (steps 3, 4)
PIDS=()
for p in "${PKGS[@]}"; do bash "$R3/lib/package.sh" "$RD" "$p" >"$RD/$p.package.log" 2>&1 & PIDS+=($!); done
INVALID=0; for pid in "${PIDS[@]}"; do wait "$pid" || INVALID=1; done
# --- anonymise and judge (step 5)
if [ "$NOJUDGE" = 0 ]; then
  echo '{}' > "$RD/scoring-keys.json"
  JUDGE_FAIL=0; JOBS=()
  judge_one() { # <rowdir> <pkg> <L>
    local row=$1 p=$2 L=$3 D C
    D=$row/$p/$L
    C=$(realpath --relative-to="$EVAL/arms/scoring/combos" "$row")
    [ "$(realpath -m "$EVAL/arms/scoring/combos/$C")" = "$(realpath -m "$row")" ] || { echo "judge path mismatch" >&2; return 1; }
    for try in 1 2; do
      bash "$EVAL/tools/tmp-scripts/judge-one.sh" "$C" "$p" "$L" > "$D/judge.stdout.$try" 2>&1
      if r3_py judge-ok --dir "$D"; then return 0; fi
      [ $try = 1 ] && { mkdir -p "$D/attempt1"; for f in score.json judge.json judge.err; do [ -e "$D/$f" ] && mv "$D/$f" "$D/attempt1/"; done; }
    done
    return 1
  }
  [ "$(sha256sum "$EVAL/tools/tmp-scripts/judge-one.sh" | cut -d' ' -f1)" = "$(jq -r '.sha256["judge-one.sh"]' "$R3/config/pins.json")" ] || { echo "E_JUDGE_CHANGED" >&2; exit 1; }
  for p in "${PKGS[@]}"; do
    KINDS=(full); [ "$COLLAB" = 1 ] && KINDS+=(sealed)
    for kind in "${KINDS[@]}"; do
      if [ $kind = full ]; then SRC=$RD/$p/merged/merged-1.md; else SRC=$RD/$p/merged-sealed/merged-1.md; fi
      [ -f "$SRC" ] || { JUDGE_FAIL=1; continue; }
      ROW=$SCORING_ROOT/s$(openssl rand -hex 5); L=$(printf '%s\n' {A..Z} | shuf -n1)
      r3_assert_writable "$ROW" || exit 1
      mkdir -p "$ROW/$p/$L"
      r3_py anon --in "$SRC" --out "$ROW/$p/$L/merged-anon.md" || { JUDGE_FAIL=1; echo "anon residue $p $kind" >&2; continue; }
      jq --arg k "$(basename "$ROW")/$p/$L" --arg id "$RUN_ID" --arg p "$p" --arg kind $kind --arg d "$ROW/$p/$L" \
        '.[$k]={run_id:$id,pkg:$p,kind:$kind,dir:$d}' "$RD/scoring-keys.json" > "$RD/scoring-keys.json.tmp" && mv "$RD/scoring-keys.json.tmp" "$RD/scoring-keys.json"
      while [ "$(jobs -rp | wc -l)" -ge 4 ]; do wait -n; done
      judge_one "$ROW" "$p" "$L" & JOBS+=($!)
    done
  done
  for j in "${JOBS[@]}"; do wait "$j" || JUDGE_FAIL=1; done
fi
# --- results row (step 6)
r3_py result --rundir "$RD" > "$RD/result.stdout"
CONT=$(jq -r .contaminated "$RD/result.json"); JOK=$(jq -r .judge_ok "$RD/result.json")
RC=0
{ [ "$INVALID" = 1 ] || [ "$(jq '.invalid_pkgs|length' "$RD/result.json")" != 0 ]; } && RC=2
[ "$NOJUDGE" = 0 ] && [ "$JOK" != true ] && RC=2
[ "$CONT" = true ] && RC=3
# --- one line (step 7)
echo "run_id=$RUN_ID $(jq -r '"found14=\(.found14) real_blocking8=\(.real_blocking8) control_found2=\(.control_found2) tokens=\(.output_tokens.total) elapsed=\(.elapsed_s|tojson)"' "$RD/result.json") exit=$RC"
# --- cleanup (step 8)
bash "$R3/bin/cleanup-sessions.sh" "$RD" >/dev/null 2>&1
exit $RC
