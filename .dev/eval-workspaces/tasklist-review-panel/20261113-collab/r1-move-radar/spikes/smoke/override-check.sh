#!/usr/bin/env bash
# override-check.sh <R1root> <row> <pkg> [<sb>]   (OVERRIDE.md)
# Decides one one-package smoke row run with TIME_CAP_EXCEPTION=1 (row id <panel>-c1x-r0): the seven 6.4 conditions (smokecheck.sh, collab 1,
# package <pkg>) plus the override conditions O1-O6. Prints "<id>\t<true|false>\t<detail>" per condition; exit 0 when all hold.
set -u -o pipefail
ROOT=$1; ROW=$2; PKG=$3; SB=${4:-/tmp/evalsb-collab-r1}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
D=$ROOT/runs/$ROW/$PKG; PANEL=${ROW%%-*}; V=$ROOT/values/$PANEL/$PKG.json
res() { printf '%s\t%s\t%s\n' "$1" "$2" "$3"; }
OUT=$(SMOKE_PKG=$PKG bash "$HERE/smokecheck.sh" "$ROOT" "$ROW" 1 "$SB"); echo "$OUT"
bad=0; grep -qP '^[1-7]\tfalse\t' <<<"$OUT" && bad=1; [ "$(grep -cP '^[1-7]\ttrue\t' <<<"$OUT")" = 7 ] || bad=1
ok() { [ "$1" = true ] || bad=1; }
# O1 the stamps: row id, row-level run.json, package run.json, collab.json, results row
o1=$(jq -n -e --arg row "$ROW" --slurpfile r "$ROOT/runs/$ROW/run.json" --slurpfile p "$D/run.json" --slurpfile c "$D/collab.json" --slurpfile s "$ROOT/results/$ROW.json" \
  '($row|test("^(el2|sl2|hl2)-c1x-r[0-9]+$")) and $r[0].time_cap_exception == true and $p[0].time_cap_exception == true
   and $c[0].time_cap_exception == true and $s[0].time_cap_exception == true' >/dev/null 2>&1 && echo true || echo false)
res O1 "$o1" "row=$ROW stamps: runs/<row>/run.json, <pkg>/run.json, collab.json, results row"; ok "$o1"
# O2 values file untouched, forced k = 1 exactly where the measured k is 0
o2=$(jq -n -e --slurpfile v "$V" --slurpfile p "$D/run.json" \
  '$p[0].cap_exception.k_measured == $v[0].k and ([$v[0].k|to_entries[]|select(.value == 0)|.key] | sort) == $p[0].cap_exception.forced_roles
   and ($p[0].k == ($v[0].k|with_entries(.value |= (if . == 0 then 1 else . end))))' >/dev/null 2>&1 && echo true || echo false)
[ "$(sha256sum "$V" | cut -d' ' -f1)" = "$(cut -d' ' -f1 "$V.sha256")" ] || o2=false
res O2 "$o2" "measured=$(jq -c .k "$V") used=$(jq -c .k "$D/run.json") forced_roles=$(jq -c .cap_exception.forced_roles "$D/run.json")"; ok "$o2"
# O3 timers: hang = max(old, 3.0 B_f); finish and guard moved with it (only when a k was forced)
o3=$(jq -n -e --slurpfile v "$V" --slurpfile p "$D/run.json" \
  '($p[0].cap_exception.forced_roles|length) as $n
   | ([$v[0].hang_offset_s, 3.0 * $v[0].B_f]|max) as $h
   | ($p[0].HANG_MS - $p[0].T0_MS) as $hang | ($p[0].FINISH_MS - $p[0].T0_MS) as $fin | ($p[0].GUARD_MS - $p[0].T0_MS) as $gd
   | if $n == 0 then ($hang - 1000 * $v[0].hang_offset_s | fabs) <= 1
     else (($hang - 1000 * $h | fabs) <= 1) and (($fin - 1000 * ($v[0].finish_offset_s + $h - $v[0].hang_offset_s) | fabs) <= 1) and $gd == $fin end' >/dev/null 2>&1 && echo true || echo false)
res O3 "$o3" "hang_s=$(jq '(.HANG_MS-.T0_MS)/1000' "$D/run.json") finish_s=$(jq '(.FINISH_MS-.T0_MS)/1000' "$D/run.json") guard_s=$(jq '(.GUARD_MS-.T0_MS)/1000' "$D/run.json") old_hang_s=$(jq .hang_offset_s "$V") old_finish_s=$(jq .finish_offset_s "$V") B_A1=$(jq .B_f "$V")"; ok "$o3"
# O4 the columns, in collab.json and in the results row, and the ratio is elapsed / B_A1
o4=$(jq -n -e --slurpfile c "$D/collab.json" --slurpfile s "$ROOT/results/$ROW.json" --arg pkg "$PKG" --slurpfile v "$V" \
  '$c[0] as $c | $s[0].packages[$pkg] as $q
   | ($c.B_A1 == $v[0].B_f) and ($c.elapsed_s != null) and (($c.elapsed_over_baseline - $c.elapsed_s / $c.B_A1) | fabs) < 1e-9
     and ($c.delivered|keys|length) == 3 and $c.forced_k == 1
     and $q.B_A1 == $c.B_A1 and $q.elapsed_over_baseline == $c.elapsed_over_baseline and $q.delivered == $c.delivered and $q.forced_k == 1' >/dev/null 2>&1 && echo true || echo false)
res O4 "$o4" "$(jq -c '{B_A1,elapsed_s,elapsed_over_baseline,forced_k,delivered}' "$D/collab.json")"; ok "$o4"
# O5 delivered = the inject events of each reviewer's metrics file and at most its k
o5=true
for rid in $(jq -r '.role|keys[]' "$D/run.json"); do
  n=$(grep -c '"ev":"inject"' "$D/board/metrics/$rid.jsonl" 2>/dev/null); k=$(jq -r --arg r "$rid" '.k[.role[$r]]' "$D/run.json")
  [ "$(jq -r --arg r "$rid" '.delivered[$r]' "$D/collab.json")" = "$n" ] && [ "$n" -le "$k" ] || o5=false
done
res O5 "$o5" "delivered=$(jq -c .delivered "$D/collab.json") k=$(jq -c .k "$D/run.json")"; ok "$o5"
# O6 identity and fallback (the checks of the design stay on): observed model equals requested, no fallback.log, NOFALLBACK argv rule
o6=true; for f in "$D"/reviews/*.meta.json; do case $f in *.attempt*) continue;; esac
  jq -e '.model_ok == true and .expected_model == .observed_model' "$f" >/dev/null || o6=false; done
[ -z "$(find "$ROOT/runs/$ROW" -name fallback.log 2>/dev/null | head -1)" ] || o6=false
res O6 "$o6" "fallback_logs=$(find "$ROOT/runs/$ROW" -name fallback.log 2>/dev/null | wc -l)"; ok "$o6"
# informational (not a condition): was any reviewer cut by the finish signal or the hang guard
res INFO - "finish_signals=$(jq -c '[.reviewers|to_entries[]|{(.key):.value.finish_signal_t}]|add' "$D/collab.json") hang_kill=$(jq -c '[.reviewers|to_entries[]|{(.key):.value.hang_kill}]|add' "$D/collab.json") slo_breach=$(jq .slo_breach "$D/collab.json")"
[ $bad = 0 ]
