#!/usr/bin/env bash
# gate0-check.sh [--root <R1>] [--sb <SB>]: decides each Gate 0 pass condition (DESIGN.md 6.3) from the spike
# records and writes spikes/gate0.json = {"G-BASE":..,"G-PINS":..,"S0":..,"S2":..,"REQ-S3":..,"S3":..,"Spike 4":..,
# "reasons":{..},"checked_utc":..}. Values: pass | fail | recorded | missing.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
SB=/tmp/evalsb-collab-r1
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; *) echo "bad arg $1" >&2; exit 1;; esac; done
PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
declare -A SQUASH=([TASK-WF-designSpec-20261107-075614]=0b8a5801d [TASK-WF-makeTheAliasOnly-20261105-051649]=4eb75698d [TASK-WF-design-20261108-041415]=54e21668f)
declare -A RES WHY
M=$R1/manifest.json

# G-BASE: 3 base shas; each sandbox lacks .dev/reflect and the package's plan folder; every src/ file the package's
# squash commit changed is absent from the sandbox or differs from its squash-commit version (R-03 repaired-code check)
RES[G-BASE]=pass; WHY[G-BASE]=""
fail() { RES[$1]=fail; WHY[$1]="${WHY[$1]}$2; "; }
n=$(jq '[.base_commits[]?|select(.sha|test("^[0-9a-f]{40}$"))]|length' "$M" 2>/dev/null || echo 0)
[ "$n" = 3 ] || fail G-BASE "manifest has $n base shas"
for P in $PKGS; do
  RR=$SB/$P/repo
  [ -f "$SB/$P/repo.ok" ] || { fail G-BASE "$P sandbox not built"; continue; }
  [ -e "$RR/.dev/reflect" ] && fail G-BASE "$P sandbox has .dev/reflect"
  [ -n "$(find "$RR/.dev" -type d -name "$P" 2>/dev/null | head -1)" ] && fail G-BASE "$P plan folder present"
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if [ -f "$RR/$f" ] && git -C "$REPO" show "${SQUASH[$P]}:$f" 2>/dev/null | cmp -s - "$RR/$f"; then fail G-BASE "$P $f equals its repaired version"; fi
  done < <(git -C "$REPO" diff-tree --no-commit-id --name-only -r --diff-filter=AM "${SQUASH[$P]}" -- src/)
done

# G-PINS: pins equal the live files; catalogue has 0 ground-truth hits
RES[G-PINS]=pass; WHY[G-PINS]=""
A1DIR=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
[ "$(jq -r .catalogue_sha256 "$M")" = "$(sha256sum "$R1/config/catalogue.json" | cut -d' ' -f1)" ] || fail G-PINS "catalogue pin"
[ "$(jq -r .brief_sha256 "$M")" = "$(sha256sum "$R1/config/brief.txt" | cut -d' ' -f1)" ] || fail G-PINS "brief pin"
[ "$(jq -r .judge_one_sha256 "$M")" = "$(sha256sum "$A1DIR/tools/tmp-scripts/judge-one.sh" | cut -d' ' -f1)" ] || fail G-PINS "judge pin"
jq -e '.pass == true and (.hits|length) == 0' "$R1/spikes/g-cat.json" >/dev/null 2>&1 || fail G-PINS "g-cat.json not clean"

# Live spikes: their records decide (each record carries its own "pass" computed by the spike script)
rec() { # rec <name> <file> <jq pass expr>
  if [ ! -f "$2" ]; then RES[$1]=missing; WHY[$1]="no record $2"; return; fi
  if jq -e "$3" "$2" >/dev/null 2>&1; then RES[$1]=pass; WHY[$1]=""; else RES[$1]=fail; WHY[$1]="condition false in $2"; fi
}
S0OK=pass; S0W=""
for m in muse-ember-1.0 gpt-6-luna claude-sonnet-5-5 claude-haiku-5-5; do
  rec S0 "$R1/spikes/s0/$m.json" '.pass == true'; [ "${RES[S0]}" = pass ] || { S0OK=${RES[S0]}; S0W="$S0W$m: ${WHY[S0]}; "; }
done
RES[S0]=$S0OK; WHY[S0]=$S0W
S2OK=pass; S2W=""
for m in muse-ember-1.0 gpt-6-luna claude-sonnet-5-5 claude-haiku-5-5; do
  rec S2 "$R1/spikes/s2/$m.json" '.pass == true'; [ "${RES[S2]}" = pass ] || { S2OK=${RES[S2]}; S2W="$S2W$m: ${WHY[S2]}; "; }
done
RES[S2]=$S2OK; WHY[S2]=$S2W
if [ -f "$R1/spikes/reqs3.json" ]; then RES[REQ-S3]=recorded; WHY[REQ-S3]=""; else RES[REQ-S3]=missing; WHY[REQ-S3]="no reqs3.json"; fi
rec S3 "$R1/spikes/s3.json" '.pass == true'
# Spike 4: one values file per panel and package with a matching .sha256 (the gate for a panel's collab-1 rows)
S4=pass; S4W=""
for panel in el2 sl2 hl2; do for P in $PKGS; do
  V=$R1/values/$panel/$P.json
  if [ ! -f "$V" ] || [ "$(sha256sum "$V" | cut -d' ' -f1)" != "$(cut -d' ' -f1 "$V.sha256" 2>/dev/null)" ]; then S4=missing; S4W="$S4W$panel/$P; "; fi
done; done
RES[Spike 4]=$S4; WHY[Spike 4]=$S4W

{ for k in G-BASE G-PINS S0 S2 REQ-S3 S3 "Spike 4"; do printf '%s\t%s\t%s\n' "$k" "${RES[$k]}" "${WHY[$k]}"; done; } |
  jq -R -s --arg t "$(date -u +%FT%TZ)" 'split("\n")|map(select(length>0)|split("\t"))
    | (map({(.[0]):.[1]})|add) + {reasons:(map({(.[0]):.[2]})|add), checked_utc:$t}' > "$R1/spikes/gate0.json"
jq -c 'del(.reasons)' "$R1/spikes/gate0.json"
