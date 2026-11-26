#!/usr/bin/env bash
# Sweeper PostToolUse hook: harvest unopened paths from the sweeper's own search output into facts (DESIGN 2.4).
# Never prints context; posts at most one harvested fact per call; always exits 0.
PATH=/usr/bin:/bin
START_MS=$(date +%s%3N)
JQ=/usr/bin/jq B=""
while [ $# -gt 0 ]; do case "$1" in --jq) JQ=$2;; --board) B=$2;; esac; shift 2; done
LIB=$(cd "$(dirname "$0")/../lib" && pwd)
INPUT=$(cat)

mlog() { printf '%s\n' "$1" >> "$B/metrics/sw-1.jsonl"; }

main() {
  set -e -o pipefail
  . "$LIB/common.sh"
  . "$LIB/validate-msg.sh"
  local tool cmd repo cand pat path move="" words tok first recursive=0 list=0 count=0 dot=0 tests=0 rootfile=0 text
  tool=$("$JQ" -r '.tool_name // ""' <<<"$INPUT")
  repo=$("$JQ" -r .repo "$B/conf.json"); cand=$("$JQ" -r .cand_dir "$B/conf.json")
  case "$tool" in
    Bash) cmd=$("$JQ" -r '.tool_input.command // ""' <<<"$INPUT");;
    Grep) pat=$("$JQ" -r '.tool_input.pattern // ""' <<<"$INPUT"); path=$("$JQ" -r '.tool_input.path // "."' <<<"$INPUT")
          path=${path#"$repo"/}; [ "$path" = "$repo" ] && path=.
          cmd="grep -rn -- '$pat' $path";;
    Glob) pat=$("$JQ" -r '.tool_input.pattern // ""' <<<"$INPUT"); cmd="find . -path './$pat'";;
    *) return 0;;
  esac
  check_cmd "$cmd" "$cand" || { mlog "$("$JQ" -cn --argjson t "$(now_ms)" --arg c "$cmd" '{ev:"harvest_skip",t:$t,reason:"bad_cmd",cmd:$c}')"; return 0; }
  # move by observable signature (first pipeline segment's words; quotes honoured by xargs)
  words=$(printf '%s' "${cmd%%|*}" | xargs -n1 printf '%s\n' 2>/dev/null) || return 0
  first=$(head -n1 <<<"$words")
  while IFS= read -r tok; do
    case "$tok" in
      --*) ;;
      -*) [[ $tok == *[rR]* ]] && recursive=1; [[ $tok == *l* ]] && list=1; [[ $tok == *c* ]] && count=1;;
      .|./) dot=1;;
      tests|tests/*|./tests|./tests/*) tests=1;;
      */*) ;;
      *) [ -f "$repo/$tok" ] && [ "$tok" != "$first" ] && rootfile=1;;
    esac
  done <<<"$words"
  case "$first" in rg) recursive=1;; git) recursive=1;; esac
  local search=0; case "$first" in grep|rg|git|find) search=1;; esac
  if [ $search = 1 ] && [ $recursive = 1 ] && [ $tests = 1 ] && [ "$first" != find ]; then move=M1
  elif { [ "$first" = grep ] && { [ $list = 1 ] || [ $count = 1 ]; }; } || [ "$first" = find ] || [[ $cmd =~ \|[[:space:]]*wc[[:space:]]+-l ]]; then move=M2
  elif [ $search = 1 ] && { [ $dot = 1 ] || [ $rootfile = 1 ]; }; then move=M7
  else return 0; fi
  # paths in the output, minus named, opened and already-posted paths
  text=$("$JQ" -r '.tool_response | if type=="string" then . elif type=="object" then
      ((.stdout // .content // "") + "\n" + ((.filenames // [])|join("\n"))) else "" end' <<<"$INPUT" | head -n 3000)
  local -A seen=()
  local onboard line p ln cand_paths=()
  onboard=$("$JQ" -r '.items[]? | sub(":[0-9]+$"; "")' "$B/msgs/board.jsonl" 2>/dev/null || true)
  local re='^\.?/?([A-Za-z0-9_.@+-]+/)*[A-Za-z0-9_.@+-]+(:[0-9]+)?'
  while IFS= read -r line; do
    [[ $line =~ $re ]] || continue
    p=${BASH_REMATCH[0]}; ln=""
    [[ $p =~ :([0-9]+)$ ]] && { ln=${BASH_REMATCH[1]}; p=${p%:*}; }
    p=${p#"$repo"/}; p=${p#./}
    [[ $p == /* ]] && continue
    [ -n "${seen[$p]:-}" ] && continue
    seen[$p]=1
    [ -f "$repo/$p" ] && [ ! -L "$repo/$p" ] || continue
    grep -qxF -- "$p" "$B/named.txt" 2>/dev/null && continue
    grep -qxF -- "$p" "$B/state/opened.txt" 2>/dev/null && continue
    grep -qxF -- "$p" <<<"$onboard" && continue
    cand_paths+=("$(rank_class "$p" "$B/named.txt")"$'\t'"${#cand_paths[@]}"$'\t'"$p${ln:+:$ln}")
  done <<<"$text"
  [ ${#cand_paths[@]} -gt 0 ] || return 0
  local items partial res
  items=$(printf '%s\n' "${cand_paths[@]}" | sort -t$'\t' -k1,1n -k2,2n | head -n 8 | cut -f3-)
  partial=$("$JQ" -cn --arg move "$move" --arg cmd "$cmd" --arg items "$items" \
    '{move:$move, items:($items|split("\n")|map(select(length>0))), cmd:$cmd}')
  res=$(board_post "$B" hv-1 "$partial" || true)
  mlog "$("$JQ" -cn --argjson t "$(now_ms)" --arg r "$res" --arg m "$move" '{ev:"harvest",t:$t,move:$m,result:$r}')"
}

ERRF=$(mkdir -p /tmp/collab-r2 2>/dev/null; mktemp /tmp/collab-r2/r2-hhook.XXXXXX 2>/dev/null || echo /dev/null)
( main ) >/dev/null 2>"$ERRF"; RC=$?
if [ $RC -ne 0 ]; then
  MSG=$(head -c 300 "$ERRF" 2>/dev/null | tr -cd 'A-Za-z0-9 ._:/=-')
  printf '{"ev":"hook_error","t":%s,"rc":%s,"msg":"%s"}\n' "$(date +%s%3N)" "$RC" "$MSG" >> "$B/metrics/sw-1.jsonl" 2>/dev/null
fi
printf '{"ev":"call","t":%s,"ms":%s}\n' "$(date +%s%3N)" "$(( $(date +%s%3N) - START_MS ))" >> "$B/metrics/sw-1.jsonl" 2>/dev/null
[ "$ERRF" = /dev/null ] || rm -f "$ERRF"
exit 0
