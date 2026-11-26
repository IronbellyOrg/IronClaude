#!/usr/bin/env bash
# msg-validate.sh <catalogue.json> <searcher rid> <reader rid,reader rid>
# panel-msg/1 validator, F3 subset (R-06, R-08, leak lookup). stdin: one envelope per line,
# {"line":"<serialised board line>","text":"<rendered text>"}. Valid board lines go to stdout, rejects to stderr as
# {"reject":"<reason>","line":..}. Exit 0 when every line is valid, 1 otherwise. DESIGN.md section 2.2.
set -u -o pipefail
CAT=${1:?usage: msg-validate.sh <catalogue.json> <searcher rid> <reader rids comma list>}; SEARCHER=${2:?}; READERS=${3:?}
rc=0
while IFS= read -r env || [ -n "$env" ]; do
  out=$(printf '%s' "$env" | jq -R -r -c --slurpfile cat "$CAT" --arg s "$SEARCHER" --arg r "$READERS" '
    ($cat[0]) as $c | ([$s] + ($r | split(","))) as $ids
    | (try fromjson catch null) as $e
    | if ($e | type) != "object" or ($e.line | type) != "string" then ["REJ", {reject: "not_json", line: .}]
      else ($e.line) as $l | ($e.text // null) as $text
      | if ($l | utf8bytelength) > 600 then ["REJ", {reject: "too_long", line: $l}]
        else (try ($l | fromjson) catch null) as $m
        | if ($m | type) != "object" then ["REJ", {reject: "not_json", line: $l}]
          else ([$m | keys[] | select(IN("v", "id", "run", "from", "to", "t", "kind", "move") | not)] | first) as $bk
          | if $bk then ["REJ", {reject: "bad_key:\($bk)", line: $l}]
            else ([
                (if $m.v != "panel-msg/1" then "v" else empty end),
                (if ($m.id | type) != "string" then "id" else empty end),
                (if ($m.run | type) != "string" then "run" else empty end),
                (if $m.from != "radar" then "from" else empty end),
                (if ($ids | index($m.to)) == null then "to" else empty end),
                (if ($m.t | type) != "number" or ($m.t | floor) != $m.t then "t" else empty end),
                (if $m.kind != "move" then "kind" else empty end)] | first) as $bf
            | if $bf then ["REJ", {reject: "bad_field:\($bf)", line: $l}]
              elif ($m | has("move")) and (($m.move | type) != "string" or ($m.move | test("^M([1-9]|10)$") | not)) then ["REJ", {reject: "bad_move", line: $l}]
              else (if ($m | has("move")) | not then $c.src_text
                    elif ($c.observable | index($m.move)) != null and $m.to == $s then $c.moves[$m.move] + $c.observable_suffix
                    else $c.moves[$m.move] end) as $want
              | if $text != $want then ["REJ", {reject: "leak", line: $l}] else ["OK", $l] end
              end
            end
          end
        end
      end
    | if .[0] == "OK" then "OK\t\(.[1])" else "REJ\t\(.[1] | tojson)" end' 2>/dev/null) || out="REJ	{\"reject\":\"not_json\",\"line\":null}"
  case $out in
    OK$'\t'*) printf '%s\n' "${out#OK$'\t'}";;
    *) printf '%s\n' "${out#REJ$'\t'}" >&2; rc=1;;
  esac
done
exit $rc
