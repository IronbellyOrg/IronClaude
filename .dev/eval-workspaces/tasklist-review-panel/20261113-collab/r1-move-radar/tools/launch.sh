#!/usr/bin/env bash
# launch.sh: PANEL_COLLAB=<0|1> bash tools/launch.sh [--root R1] [--sb SB] [--a1 A1DIR] [--prebuilt] <panel> <rep> [<pkg> ...]
#            bash tools/launch.sh --order <rid> <searcher|reader>   (prints the receiver's move order, section 2.5)
# One launch = one results row <panel>-c<collab>-r<rep> over the requested packages (default DS, AL, DE), DESIGN.md section 5.
# Exit 0: row written and every requested package ok. 1: row written, some package invalid, quarantined or judge_failed.
# 2: a preflight refusal (nothing run). Log: runs/<row>/launch.log. Never prompts.
# --root/--sb/--a1/--prebuilt exist for the tests (--prebuilt: sandbox and index were built by the test, skip those two steps).
set -u -o pipefail
order() { # rotate the role list left by int(sha256(rid)[0:8], 16) mod len
  local rid=$1 role=$2 list h off i out=()
  if [ "$role" = searcher ]; then list=(M1 M2 M7 M4); else list=(M3 M5 M6 M9 M8 M10); fi
  h=$(printf %s "$rid" | sha256sum | cut -c1-8); off=$(( 16#$h % ${#list[@]} ))
  for ((i = 0; i < ${#list[@]}; i++)); do out+=("${list[(i + off) % ${#list[@]}]}"); done
  (IFS=,; echo "${out[*]}")
}
if [ "${1:-}" = --order ]; then order "$2" "$3"; exit 0; fi

REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
TOOLS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
R1=$(dirname "$TOOLS")
A1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
SB=/tmp/evalsb-collab-r1
PREBUILT=0
refuse() { echo "REFUSE $*" >&2; exit 2; }
POS=()
while [ $# -gt 0 ]; do case $1 in
  --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --a1) A1=$2; shift 2;; --prebuilt) PREBUILT=1; shift;; *) POS+=("$1"); shift;;
esac; done
R1=$(realpath -m "$R1"); SB=$(realpath -m "$SB")
[ ${#POS[@]} -ge 2 ] || refuse "usage: launch.sh [options] <panel> <rep> [<pkg> ...]"
PANEL=${POS[0]}; REP=${POS[1]}; PKGS=("${POS[@]:2}")
DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649; DE=TASK-WF-design-20261108-041415
[ ${#PKGS[@]} -gt 0 ] || PKGS=($DS $AL $DE)

# ---------------------------------------------------------------- 1. preflight
COLLAB=${PANEL_COLLAB-1}  # unset-only default: a set-but-empty value is refused by the case below
case $COLLAB in 0|1) ;; *) refuse "PANEL_COLLAB must be 0 or 1, got $COLLAB";; esac
case $PANEL in el2|sl2|hl2) ;; *) refuse "panel must be el2, sl2 or hl2";; esac
[[ $REP =~ ^[0-9]+$ ]] || refuse "rep must be a non-negative integer"
for p in "${PKGS[@]}"; do case $p in $DS|$AL|$DE) ;; *) refuse "unknown package $p";; esac; done
case ${NOFALLBACK-1} in 1) ;; *) refuse "NOFALLBACK must be unset or 1";; esac
export NOFALLBACK=1
for c in claude jq flock uv superclaude sha256sum; do command -v "$c" >/dev/null 2>&1 || refuse "$c is not on PATH"; done
M=$R1/manifest.json
sha() { sha256sum "$1" | cut -d' ' -f1; }
JUDGE=$A1/tools/tmp-scripts/judge-one.sh
[ "$(jq -r .catalogue_sha256 "$M")" = "$(sha "$R1/config/catalogue.json")" ] || refuse "catalogue.json does not match its pin in manifest.json"
[ "$(jq -r .brief_sha256 "$M")" = "$(sha "$R1/config/brief.txt")" ] || refuse "brief.txt does not match its pin in manifest.json"
[ "$(jq -r .judge_one_sha256 "$M")" = "$(sha "$JUDGE")" ] || refuse "judge-one.sh does not match its pin in manifest.json"
for p in "${PKGS[@]}"; do
  jq -e --arg p "$p" '.base_commits[$p].sha|test("^[0-9a-f]{40}$")' "$M" >/dev/null 2>&1 || refuse "manifest.json has no base sha for $p"
  if [ "$COLLAB" = 1 ]; then
    V=$R1/values/$PANEL/$p.json
    [ -f "$V" ] && [ "$(sha "$V")" = "$(cut -d' ' -f1 "$V.sha256" 2>/dev/null)" ] || refuse "PANEL_COLLAB=1 needs values/$PANEL/$p.json with a matching .sha256 (Spike 4)"
  fi
done
gate() { jq -r --arg k "$1" '.[$k] // "missing"' "$R1/spikes/gate0.json" 2>/dev/null || echo missing; }
NEED=(G-BASE G-PINS)
[ "$COLLAB" = 1 ] && NEED+=(S0 S2)
[ "$COLLAB" = 1 ] && [ "$REP" -ge 1 ] && NEED+=(S3)
for g in "${NEED[@]}"; do [ "$(gate "$g")" = pass ] || refuse "Gate 0: $g is $(gate "$g"), not pass (gate order, DESIGN.md 6.3)"; done
ROW=$PANEL-c$COLLAB-r$REP
[ ! -f "$R1/results/$ROW.json" ] || refuse "row $ROW is finished (results/$ROW.json exists)"
mkdir -p "$R1/runs/$ROW"
LOG=$R1/runs/$ROW/launch.log
log() { printf '%s %s %s\n' "$(date -u +%FT%TZ)" "$1" "${*:2}" >> "$LOG"; }
[ -f "$R1/runs/$ROW/run.json" ] || jq -n -c --arg row "$ROW" --arg panel "$PANEL" --argjson c "$COLLAB" --argjson rep "$REP" --arg t "$(date -u +%FT%TZ)" \
  '{row:$row,panel:$panel,collab:$c,rep:$rep,started_utc:$t}' > "$R1/runs/$ROW/run.json"

# ---------------------------------------------------------------- 2-7. per package
CFG=$R1/config/panels.json
py() { (cd "$REPO" && uv run python "$@"); }
run_package() { # run_package <pkg>; writes runs/<row>/<pkg>/status
  local pkg=$1 d=$R1/runs/$ROW/$1 t0 dl rid role model cp1 cp2 k ord fin guard rc n=0 any_bad=0 spec prev keep
  if [ -f "$d/status" ]; then  # a package that reached score.json (status ok) is skipped; any other earlier attempt is kept aside, never deleted
    prev=$(cat "$d/status")
    [ "$prev" = ok ] && { log SKIP "$pkg (already ok)"; return; }
    keep="$d.prev-$(date +%s)"; mv "$d" "$keep" && log KEEP "$pkg earlier attempt (status $prev) kept in $keep"
  fi
  log START "$pkg"; mkdir -p "$d/reviews" "$d/rc"
  if [ "$PREBUILT" = 0 ]; then
    bash "$TOOLS/sandbox.sh" "$pkg" --root "$R1" --sb "$SB" >> "$LOG" 2>&1 || { log FAIL "$pkg sandbox"; echo invalid > "$d/status"; return; }
    bash "$TOOLS/radar-index.sh" "$pkg" --root "$R1" --sb "$SB" >> "$LOG" 2>&1 || { log FAIL "$pkg radar-index"; echo invalid > "$d/status"; return; }
  fi
  # reviewers of the panel: rid:role:model:cp1:cp2
  local -a REV=()
  while IFS= read -r spec; do REV+=("$spec"); done < <(jq -r --arg p "$PANEL" '.[$p].roles as $r
    | ($r.searcher|"\(.rid):searcher:\(.model):\(.checkpoints[0]):\(.checkpoints[1])"),
      ($r.reader|.model as $m|.checkpoints as $c|.rids[]|"\(.):reader:\($m):\($c[0]):\($c[1])")' "$CFG")
  t0=$(date +%s%3N)
  dl=$(py "$TOOLS/values.py" deadlines "$PANEL" "$pkg" "$COLLAB" "$t0" --root "$R1") || { log FAIL "$pkg deadlines"; echo invalid > "$d/status"; return; }
  fin=$(jq -r .FINISH_MS <<<"$dl"); guard=$(jq -r .GUARD_MS <<<"$dl")
  local roles='{}' models='{}' orders='{}'
  for spec in "${REV[@]}"; do
    IFS=: read -r rid role model cp1 cp2 <<<"$spec"; ord=$(order "$rid" "$role")
    roles=$(jq -c --arg r "$rid" --arg v "$role" '.+{($r):$v}' <<<"$roles"); models=$(jq -c --arg r "$rid" --arg v "$model" '.+{($r):$v}' <<<"$models")
    orders=$(jq -c --arg r "$rid" --arg v "$ord" '.+{($r):$v}' <<<"$orders")
  done
  jq -n -c --arg row "$ROW" --arg pkg "$pkg" --arg panel "$PANEL" --argjson c "$COLLAB" --argjson t0 "$t0" --argjson dl "$dl" \
    --argjson roles "$roles" --argjson models "$models" --argjson orders "$orders" --arg cs "$(sha "$SB/cand/$pkg/candidate.md")" \
    '{row:$row,pkg:$pkg,panel:$panel,collab:$c,T0_MS:$t0,FINISH_MS:$dl.FINISH_MS,GUARD_MS:$dl.GUARD_MS,HANG_MS:$dl.HANG_MS,B:$dl.B,
      values:$dl.values,k:$dl.k,T_report:$dl.T_report,role:$roles,model:$models,order:$orders,cand_sha256:$cs}' > "$d/run.json"
  if [ "$COLLAB" = 1 ]; then
    mkdir -p "$d/settings" "$d/board"/{tele,msgs,metrics,snap,state,ctx}  # ctx/: the hook's frozen inputs (radar-hook.sh header)
    cp "$R1/config/catalogue.json" "$d/board/ctx/catalogue.json"; cp "$R1/index/$pkg.json" "$d/board/ctx/index.json"
    jq -c --arg p "$PANEL" --arg src "$SB/cand/$pkg/source.md" '.[$p].roles|{searcher:.searcher.rid,readers:.reader.rids,srcpath:$src}' "$CFG" \
      > "$d/board/ctx/panel.json" || { log FAIL "$pkg board ctx"; echo invalid > "$d/status"; return; }
    for spec in "${REV[@]}"; do
      IFS=: read -r rid role model cp1 cp2 <<<"$spec"; k=$(jq -r --arg r "$role" '.k[$r]' "$d/run.json")
      bash "$TOOLS/settings-gen.sh" "$d/board" "$ROW/$pkg" "$rid" "$role" "$t0" "$fin" "$guard" "$k" "$cp1" "$cp2" "$(order "$rid" "$role")" "$pkg" "" \
        > "$d/settings/$rid.json" || { log FAIL "$pkg settings-gen $rid"; echo invalid > "$d/status"; return; }
    done
  fi
  for spec in "${REV[@]}"; do
    IFS=: read -r rid role model cp1 cp2 <<<"$spec"
    ( bash "$TOOLS/run-reviewer.sh" "$ROW" "$pkg" "$rid" "$model" "$COLLAB" "$t0" --root "$R1" --sb "$SB" >> "$d/reviews/$rid.runner.log" 2>&1; echo $? > "$d/rc/$rid" ) &
  done
  wait
  for spec in "${REV[@]}"; do rid=${spec%%:*}; [ "$(cat "$d/rc/$rid" 2>/dev/null)" = 0 ] || { any_bad=1; log FAIL "$pkg reviewer $rid rc=$(cat "$d/rc/$rid" 2>/dev/null)"; }; done
  py "$TOOLS/collab_summary.py" pre "$ROW" "$pkg" --root "$R1" --sb "$SB" --a1 "$A1" >> "$d/summary.log" 2>&1; rc=$?
  [ -f "$d/collab.json" ] && while IFS= read -r a; do log ALARM "$a"; echo "ALARM $a" >&2; done < <(jq -r '.alarms[]?' "$d/collab.json")
  if [ $rc = 3 ]; then log FAIL "$pkg quarantined: $(cat "$d/QUARANTINED" 2>/dev/null)"; echo quarantined > "$d/status"; return; fi
  if [ $rc != 0 ]; then log FAIL "$pkg collab_summary pre rc=$rc"; echo invalid > "$d/status"; return; fi
  if [ $any_bad = 1 ]; then echo invalid > "$d/status"; return; fi
  local -a RARGS=(); for spec in "${REV[@]}"; do rid=${spec%%:*}; RARGS+=(--report "$rid=$d/reviews/$rid.md"); done
  jq -c --argjson rev "$(jq -c --slurpfile run "$d/run.json" --arg p "$PANEL" '.[$p].resolution as $res | $run[0].model as $m
      | [$run[0].role|keys[] | {reviewer_id:., model:$m[.], alias:$res[.].alias, tier:$res[.].tier, strategy:"fixed", stand_in:false,
          fallback_depth:0, fallbacks:[], launch:null, seed:null, slot_id:(split("-")[0])}]' "$CFG")" \
    '.reviewers=$rev' "$A1/$pkg/resolution-live7.json" > "$d/resolution.json" || { log FAIL "$pkg resolution"; echo invalid > "$d/status"; return; }
  superclaude review merge --ledger "$d/ledger.json" --doc "$A1/$pkg/candidate.md" --round 1 "${RARGS[@]}" \
    --resolution "$d/resolution.json" --out "$d/merged-1.md" > "$d/merge-stdout.txt" 2>&1 || { log FAIL "$pkg merge refused"; echo invalid > "$d/status"; return; }
  bash "$TOOLS/anon.sh" "$ROW" "$pkg" --root "$R1" >> "$d/summary.log" 2>&1 || { log FAIL "$pkg anon"; echo invalid > "$d/status"; return; }
  py "$TOOLS/collab_summary.py" post "$ROW" "$pkg" --root "$R1" --sb "$SB" --a1 "$A1" >> "$d/summary.log" 2>&1 || { log FAIL "$pkg collab_summary post"; echo invalid > "$d/status"; return; }
  n=$(jq -r '.anon_leak // 0' "$d/collab.json")
  if [ "$n" -gt 0 ]; then echo "anon_leak=$n" > "$d/QUARANTINED"; log FAIL "$pkg quarantined: anon_leak=$n"; echo quarantined > "$d/status"; return; fi
  local op lab c sc
  op=$(jq -r .opaque "$d/label-key.json"); lab=$(jq -r .label "$d/label-key.json")
  c=$(realpath -m --relative-to="$A1/arms/scoring/combos" "$R1/scoring/$op"); sc=$R1/scoring/$op/$pkg/$lab/score.json
  for n in 1 2; do  # the unchanged judge; it skips when score.json exists, so a second call only follows a failed first one
    bash "$JUDGE" "$c" "$pkg" "$lab" >> "$d/judge-run.log" 2>&1
    jq -e . "$sc" >/dev/null 2>&1 && break
  done
  if jq -e . "$sc" >/dev/null 2>&1; then echo ok > "$d/status"; log END "$pkg ok"; else echo judge_failed > "$d/status"; log FAIL "$pkg judge_failed"; fi
}
for p in "${PKGS[@]}"; do run_package "$p"; done

# ---------------------------------------------------------------- 8. results
bad=0; for p in "${PKGS[@]}"; do [ "$(cat "$R1/runs/$ROW/$p/status" 2>/dev/null)" = ok ] || bad=1; done
if out=$(py "$TOOLS/results.py" "$ROW" --root "$R1" --a1 "$A1" 2>&1); then echo "$out"; log END "row $ROW $out"; else echo "$out" >&2; log FAIL "results.py: $out"; bad=1; fi
bash "$TOOLS/cleanup-sessions.sh" "$ROW" --root "$R1" --sb "$SB" >> "$LOG" 2>&1 || log FAIL "cleanup-sessions"
exit $bad
