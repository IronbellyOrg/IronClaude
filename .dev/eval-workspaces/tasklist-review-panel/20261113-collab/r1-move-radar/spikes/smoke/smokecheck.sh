#!/usr/bin/env bash
# smokecheck.sh <R1root> <row> <collab 0|1> [<sb>]: decides the seven conditions of DESIGN.md 6.4 for one smoke row (one package).
set -u -o pipefail
ROOT=$1; ROW=$2; COLLAB=$3; SB=${4:-/tmp/evalsb-collab-r1}
DS=${SMOKE_PKG:-TASK-WF-designSpec-20261107-075614}  # SMOKE_PKG: the package of an override smoke row (OVERRIDE.md)
D=$ROOT/runs/$ROW/$DS
A1=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
res() { printf '%s\t%s\t%s\n' "$1" "$2" "$3"; }
echo "status=$(cat "$D/status" 2>/dev/null)"
# 1 models
ok1=true; for f in "$D"/reviews/*.meta.json; do case $f in *.attempt*) continue;; esac
  jq -e '.model_ok == true and .valid == true and .expected_model == .observed_model' "$f" >/dev/null || ok1=false; done
res 1 "$ok1" "$(for f in "$D"/reviews/*.meta.json; do case $f in *.attempt*) continue;; esac; jq -r '"\(.reviewer_id):\(.observed_model):model_ok=\(.model_ok)"' "$f"; done | tr '\n' ' ')"
# 2 dropped lines
ok2=true; det=""; for f in "$D"/reviews/*.meta.json; do case $f in *.attempt*) continue;; esac
  dl=$(jq -r '.dropped_lines' "$f"); ra=$(jq -r '.reask_s' "$f"); det="$det $(jq -r .reviewer_id "$f"):dropped=$dl,reask=$ra"
  [ "$dl" = 0 ] || [ "$ra" != null ] || ok2=false; done
res 2 "$ok2" "$det"
# 3 hooks / kill switch
if [ "$COLLAB" = 1 ]; then
  C=$D/collab.json; GUARD=$(jq -r .GUARD_MS "$D/run.json")
  ok3=$(jq -r --argjson g "$GUARD" '([.reviewers[]|(.hook_calls>0 and .msgs_received<=.k)]|all)
        and ([.slots[]|.t < $g]|all) and ([.reviewers[]|select(.msgs_received>0)|(.seal_t != null and .seal_t <= .first_delivery_t)]|all)' "$C")
  a=$(jq -r '.leak_violations' "$D/audit.json"); [ "$a" = 0 ] || ok3=false
  # seal event precedes the inject event in each reviewer's metrics file (the same clock reading can give equal ms)
  for m in "$D"/board/metrics/*.jsonl; do jq -s -e '(to_entries|map(select(.value.ev=="seal"))[0].key) as $a | (to_entries|map(select(.value.ev=="inject"))[0].key) as $b | ($b == null or ($a != null and $a < $b))' "$m" >/dev/null 2>&1 || ok3=false; done
  res 3 "$ok3" "$(jq -c '[.reviewers|to_entries[]|{(.key):{hook_calls:.value.hook_calls,inj:.value.msgs_received,k:.value.k,seal_t:.value.seal_t,first:.value.first_delivery_t}}]|add' "$C") leak_violations=$a"
else
  ok3=true; [ -d "$D/settings" ] && ok3=false; [ -d "$D/board/msgs" ] && ok3=false
  grep -l -e '--settings' "$D"/reviews/*.meta.json >/dev/null 2>&1 && ok3=false
  res 3 "$ok3" "settings_dir=$([ -d "$D/settings" ] && echo yes || echo no) msgs_dir=$([ -d "$D/board/msgs" ] && echo yes || echo no) settings_in_argv=$(grep -l -e '--settings' "$D"/reviews/*.meta.json 2>/dev/null | wc -l)"
fi
# 4 merge
ok4=true; [ -s "$D/merged-1.md" ] || ok4=false
for r in $(jq -r '.role|keys[]' "$D/run.json"); do grep -q "$r" "$D/merged-1.md" || ok4=false; done
res 4 "$ok4" "merge_stdout_tail=$(tail -c 160 "$D/merge-stdout.txt" | tr '\n' ' ')"
# 5 anon + judge + A1DIR untouched
OP=$(jq -r .opaque "$D/label-key.json"); L=$(jq -r .label "$D/label-key.json")
ok5=true; jq -e . "$ROOT/scoring/$OP/$DS/$L/score.json" >/dev/null 2>&1 || ok5=false
[ "$(jq -r .anon_leak "$D/collab.json")" = 0 ] || ok5=false
NEWER=$(find "$A1" -newer "$(dirname "$(dirname "$(dirname "$(realpath "${BASH_SOURCE[0]}")")")")/manifest.json" 2>/dev/null | head -3)  # AC-5: nothing under A1DIR newer than R1/manifest.json
[ -z "$NEWER" ] || ok5=false
res 5 "$ok5" "anon_leak=$(jq -r .anon_leak "$D/collab.json") score=$(jq -c '{gt_covered_any,wrong_blockers}' "$ROOT/scoring/$OP/$DS/$L/score.json" 2>/dev/null) a1_newer_than_manifest=${NEWER:-none}"
# 6 results shape
ok6=true; RJ=$ROOT/results/$ROW.json
jq -e '.schema=="r1-results/1" and .design=="r1-move-radar" and (.packages|keys|length)==3 and has("collab_counters") and .status=="incomplete" and (.output_tokens==null)' "$RJ" >/dev/null || ok6=false
res 6 "$ok6" "status=$(jq -r .status "$RJ") found_14=$(jq -r .found_14 "$RJ") output_tokens=$(jq -r .output_tokens "$RJ")"
# 7 sandbox clean, candidate sha, cleanup
ok7=true; [ -z "$(git -C "$SB/$DS/repo" status --porcelain)" ] || ok7=false
[ "$(jq -r .candidate_sha_unchanged "$D/audit.json")" = true ] || ok7=false
nsess=$(for f in "$D"/reviews/*.meta.json; do case $f in *.attempt*) continue;; esac; jq -r '.session_ids[]' "$f"; done | sort -u | wc -l)
ndel=$(grep -c '^DELETED' "$ROOT/runs/$ROW/cleanup.log" 2>/dev/null); nabs=$(grep -c '^ABSENT' "$ROOT/runs/$ROW/cleanup.log" 2>/dev/null)
[ "$ndel" = "$nsess" ] || ok7=false
res 7 "$ok7" "git_clean=$([ -z "$(git -C "$SB/$DS/repo" status --porcelain)" ] && echo yes || echo no) cand_sha_unchanged=$(jq -r .candidate_sha_unchanged "$D/audit.json") sessions=$nsess deleted=$ndel absent=$nabs"
