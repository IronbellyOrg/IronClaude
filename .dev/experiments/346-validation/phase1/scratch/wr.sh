#!/bin/bash
# usage: wr.sh FILE [pathregex] ; lists jsonl line, tool, path, size of Write/Edit calls
jq -r --arg re "${2:-.}" 'select(.type=="assistant") | . as $o | .message.content[]? | select(.type=="tool_use" and (.name=="Write" or .name=="Edit")) | select(.input.file_path|test($re)) | "\(input_line_number)\t\(.name)\t\(.input.file_path|split("/")|.[-2:]|join("/"))\t\((.input.content // .input.new_string // "")|length)"' "$1"
