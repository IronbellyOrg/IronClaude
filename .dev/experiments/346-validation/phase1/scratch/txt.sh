#!/bin/bash
# usage: txt.sh FILE [N chars] ; prints "line type ts text"
F="$1"; N="${2:-300}"
jq -r --argjson n "$N" '
 def txt: if (.message.content|type)=="string" then .message.content
          elif (.message.content|type)=="array" then ([.message.content[]|
              if .type=="text" then .text
              elif .type=="tool_use" then "[TOOL_USE "+.name+"] "+((.input|tostring)|.[0:200])
              elif .type=="tool_result" then "[TOOL_RESULT] "+((.content|if type=="array" then (map(.text? // "")|join(" ")) else tostring end)|.[0:200])
              else "" end]|join(" | "))
          else "" end;
 select(.type=="user" or .type=="assistant") | "\(input_line_number)\t\(.type)\t\(.timestamp // "")\t\(txt|gsub("\n";" ")|.[0:$n])"' "$F"
