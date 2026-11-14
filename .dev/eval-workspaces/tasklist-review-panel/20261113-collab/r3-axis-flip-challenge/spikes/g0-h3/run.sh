#!/usr/bin/env bash
# G0-H3: build each sandbox; every masked path must differ from the implementing commit's version (or be absent at base).
set -u -o pipefail
R3=$(cd "$(dirname "$0")/../.." && pwd -P); source "$R3/lib/common.sh"
declare -A IMPL=([TASK-WF-designSpec-20261107-075614]=0b8a5801d [TASK-WF-makeTheAliasOnly-20261105-051649]=4eb75698d [TASK-WF-design-20261108-041415]=54e21668f)
OUT='[]'
for p in $(jq -r '.order[]' "$R3/config/packages.json"); do
  b=$(bash "$R3/bin/build-sandbox.sh" "$p" 2>&1); brc=$?
  base=$(jq -r --arg p "$p" '.packages[$p].base' "$R3/config/packages.json")
  par=$(git -C "$REPO" rev-parse "${IMPL[$p]}^")
  rows='[]'
  for f in $(jq -r --arg p "$p" '.packages[$p].masked_paths[]' "$R3/config/packages.json"); do
    if [ -e "$SB/$p/repo/$f" ]; then
      if git -C "$REPO" cat-file -e "${IMPL[$p]}:$f" 2>/dev/null && cmp -s <(git -C "$REPO" show "${IMPL[$p]}:$f") "$SB/$p/repo/$f"; then st=same_as_impl; else st=differs_from_impl; fi
    else st=absent_at_base; fi
    rows=$(jq -c --arg f "$f" --arg s "$st" '.+[{path:$f,status:$s}]' <<<"$rows")
  done
  leak=$(cd "$SB/$p/repo" && find . -path '*TASK-WF-designSpec-20261107-075614*' -o -path '*TASK-WF-makeTheAliasOnly-20261105-051649*' -o -path '*TASK-WF-design-20261108-041415*' | head -3 | tr '\n' ' ')
  refl=$([ -e "$SB/$p/repo/.dev/reflect" ] && echo present || echo absent)
  OUT=$(jq -c --arg p "$p" --arg b "$base" --arg par "$par" --argjson brc $brc --argjson rows "$rows" --arg leak "$leak" --arg refl "$refl" --arg msg "$b" \
    '.+[{pkg:$p,base:$b,impl_parent:$par,base_is_impl_parent:($b==$par),build_rc:$brc,build_msg:$msg,masked:$rows,pkg_paths_left:$leak,dev_reflect:$refl,
        pass:($brc==0 and ($rows|all(.status!="same_as_impl")) and $leak=="" and $refl=="absent")}]' <<<"$OUT")
done
jq '{spike:"G0-H3",rows:.,pass:(map(.pass)|all)}' <<<"$OUT" | tee "$R3/spikes/g0-h3/result.json"
